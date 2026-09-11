"""Legacy/manual archive import with existing-content-hash rejection."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import config
from .db import repository
from .harvester import (
    ArchiveIntegrityError,
    build_bundle,
    snapshot,
)


@dataclass(frozen=True)
class IngestResult:
    session_id: int
    evidence_bundle_hash: str
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
    """Import a stable external log set and register its immutable manifest.

    This compatibility API is for external or historical evidence. A repeated
    ``error.log`` hash fails before registration or parsing. There is no
    override. Parsing is deliberately outside this operation.
    """
    from .archive_registry import reconcile_archives

    root = Path(logs_root) if logs_root is not None else config.ROOT_LOGS
    db_path = _db_path()
    reconciliation = reconcile_archives(config.ROOT_CK3CHRONICLE, db_path)
    bundle = build_bundle(root)
    error_sha256 = bundle.identities["log:error.log"].sha256

    # An indexed import whose archive disappeared is corruption, not an
    # invitation to reconstruct it silently from the supplied files.
    if db_path.exists():
        existing_conn = repository.open_db(db_path)
        try:
            existing = repository.get_session_by_error_log_hash(
                existing_conn, error_sha256
            )
        finally:
            existing_conn.close()
        if existing is not None:
            expected_archive = (
                config.ROOT_CK3CHRONICLE
                / "sessions"
                / str(existing["evidence_bundle_hash"])
            )
            if not expected_archive.is_dir():
                raise ArchiveIntegrityError(
                    "registered session is missing its finalized evidence archive"
                )
            raise repository.ExistingErrorLogHashError(
                error_sha256,
                int(existing["session_id"]),
            )

    captured = snapshot(bundle, config.ROOT_CK3CHRONICLE)

    conn = repository.open_db(db_path)
    try:
        session_id, _ = repository.register_finalized_session(
            conn,
            evidence_bundle_hash=captured.evidence_bundle_hash,
            captured_at=captured.captured_at,
            manifest_version=captured.manifest_version,
            manifest_sha256=captured.manifest_sha256,
            evidence_completeness=(
                "partial" if captured.missing_principal_logs else "complete"
            ),
            files=captured.files,
        )
        if observation_trigger is not None:
            repository.record_run_metadata(
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
