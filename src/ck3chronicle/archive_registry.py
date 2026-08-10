"""Reconcile immutable filesystem archives with the rebuildable SQLite index."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .db import repository
from .harvester import (
    MANIFEST_NAME,
    MANIFEST_VERSION,
    adopt_legacy_archive,
    hash_file,
    read_snapshot,
)


@dataclass(frozen=True)
class ReconciliationSummary:
    scanned: int
    adopted_legacy: int
    registered: int
    already_registered: int
    registered_hashes: tuple[str, ...]
    errors: tuple[str, ...]


def reconcile_archives(
    archive_root: Path,
    db_path: Path,
    *,
    full_verify: bool = False,
) -> ReconciliationSummary:
    """Validate/register orphan archives and promote verified legacy rows.

    Invalid archives remain untouched and unfinalized; their content hashes are
    returned as errors so a damaged historical item cannot block new capture.
    """
    sessions_root = Path(archive_root) / "sessions"
    sessions_root.mkdir(parents=True, exist_ok=True)
    directories = sorted(
        path
        for path in sessions_root.iterdir()
        if path.is_dir() and path.name != ".staging"
    )
    conn = repository.open_db(db_path)
    adopted = 0
    registered = 0
    registered_hashes: list[str] = []
    existing_count = 0
    errors: list[str] = []
    try:
        directory_hashes = {directory.name for directory in directories}
        for row in repository.list_sessions(conn, limit=1_000_000):
            bundle_hash = row["evidence_bundle_hash"]
            if bundle_hash not in directory_hashes:
                errors.append(
                    f"{bundle_hash}: registered session is missing its archive"
                )
        for directory in directories:
            try:
                existing = repository.get_session_by_hash(conn, directory.name)
                manifest_path = directory / MANIFEST_NAME
                if (
                    not full_verify
                    and existing is not None
                    and existing["capture_status"] == "finalized"
                    and existing["capture_manifest_version"] == MANIFEST_VERSION
                    and manifest_path.is_file()
                    and existing["capture_manifest_sha256"] == hash_file(manifest_path)
                ):
                    existing_count += 1
                    continue

                if manifest_path.is_file():
                    captured = read_snapshot(directory)
                else:
                    captured = adopt_legacy_archive(directory)
                    adopted += 1
                _, was_existing = repository.register_finalized_session(
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
                if was_existing:
                    existing_count += 1
                else:
                    registered += 1
                    registered_hashes.append(captured.evidence_bundle_hash)
            except Exception as exc:
                errors.append(f"{directory.name}: {exc}")
    finally:
        conn.close()
    return ReconciliationSummary(
        scanned=len(directories),
        adopted_legacy=adopted,
        registered=registered,
        already_registered=existing_count,
        registered_hashes=tuple(registered_hashes),
        errors=tuple(errors),
    )
