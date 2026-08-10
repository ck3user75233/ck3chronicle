"""Finalized CK3 evidence capture and transactional session registration."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import config
from .db import repository
from .harvester import (
    MANIFEST_VERSION,
    ArchiveIntegrityError,
    build_bundle,
    snapshot,
)


@dataclass(frozen=True)
class IngestResult:
    session_id: int
    evidence_bundle_hash: str
    was_duplicate: bool
    archive_was_existing: bool
    log_count: int
    crash_count: int
    total_files: int
    capture_status: str
    evidence_completeness: str
    missing_principal_logs: tuple[str, ...]
    archive_dir: Path
    reconciliation_errors: tuple[str, ...]


def _db_path() -> Path:
    return config.ROOT_CK3CHRONICLE / "ck3chronicle.db"


def ingest(
    logs_root: Path | None = None,
    *,
    observation_trigger: str | None = None,
    process_name: str | None = None,
) -> IngestResult:
    """Atomically archive a stable run and register its immutable manifest.

    Archival is completed before SQLite registration. If registration fails,
    the complete content-addressed archive remains recoverable; the next call
    validates it and transactionally registers the missing session row.
    Parsing is deliberately outside this operation.
    """
    from .archive_registry import reconcile_archives

    root = Path(logs_root) if logs_root is not None else config.ROOT_LOGS
    db_path = _db_path()
    reconciliation = reconcile_archives(config.ROOT_CK3CHRONICLE, db_path)
    bundle = build_bundle(root)

    # An indexed session whose archive disappeared is corruption, not an
    # invitation to silently reconstruct history from whatever is live now.
    if db_path.exists():
        existing_conn = repository.open_db(db_path)
        try:
            existing = repository.get_session_by_hash(
                existing_conn, bundle.evidence_bundle_hash
            )
        finally:
            existing_conn.close()
        expected_archive = (
            config.ROOT_CK3CHRONICLE
            / "sessions"
            / bundle.evidence_bundle_hash
        )
        if existing is not None and not expected_archive.is_dir():
            raise ArchiveIntegrityError(
                "registered session is missing its finalized evidence archive"
            )

    captured = snapshot(bundle, config.ROOT_CK3CHRONICLE)

    conn = repository.open_db(db_path)
    try:
        session_id, was_duplicate = repository.register_finalized_session(
            conn,
            evidence_bundle_hash=captured.evidence_bundle_hash,
            captured_at=captured.captured_at,
            manifest_version=MANIFEST_VERSION,
            manifest_sha256=captured.manifest_sha256,
            evidence_completeness=(
                "partial" if captured.missing_principal_logs else "complete"
            ),
            files=captured.files,
        )
        effective_duplicate = (
            was_duplicate
            and captured.evidence_bundle_hash not in reconciliation.registered_hashes
        )
        if observation_trigger is not None and (
            observation_trigger == "process_exit" or not effective_duplicate
        ):
            repository.record_capture_observation(
                conn,
                session_id=session_id,
                trigger=observation_trigger,
                process_name=process_name,
            )
    finally:
        conn.close()

    log_count = sum(item.kind == "log" for item in captured.files)
    crash_count = sum(item.kind == "crash" for item in captured.files)
    return IngestResult(
        session_id=session_id,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        was_duplicate=effective_duplicate,
        archive_was_existing=captured.was_existing,
        log_count=log_count,
        crash_count=crash_count,
        total_files=len(captured.files),
        capture_status="finalized",
        evidence_completeness=(
            "partial" if captured.missing_principal_logs else "complete"
        ),
        missing_principal_logs=captured.missing_principal_logs,
        archive_dir=captured.dest_dir,
        reconciliation_errors=reconciliation.errors,
    )
