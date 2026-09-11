"""Reconcile immutable filesystem archives with the rebuildable SQLite index."""
from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TypeVar

from .db import repository
from .harvester import (
    ArchiveIntegrityError,
    MANIFEST_NAME,
    adopt_legacy_archive,
    read_capture_metadata,
    read_snapshot,
    snapshot_file_metadata_matches_manifest,
    snapshot_manifest_projection,
)

T = TypeVar("T")
ArchiveEventSink = Callable[[str, dict[str, object]], None]


def _timed_archive_stage(
    stage: str,
    operation: Callable[[], T],
    *,
    event_sink: ArchiveEventSink | None,
    monotonic_ns: Callable[[], int],
    completion_fields: Callable[[T], dict[str, object]] | None = None,
) -> T:
    if event_sink is not None:
        event_sink("stage_started", {"stage": stage})
    started_ns = monotonic_ns()
    try:
        result = operation()
    except BaseException as exc:
        if event_sink is not None:
            event_sink(
                "stage_failed",
                {
                    "stage": stage,
                    "duration_ms": round(
                        (monotonic_ns() - started_ns) / 1_000_000,
                        3,
                    ),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
        raise
    fields: dict[str, object] = {
        "stage": stage,
        "duration_ms": round((monotonic_ns() - started_ns) / 1_000_000, 3),
    }
    if completion_fields is not None:
        fields.update(completion_fields(result))
    if event_sink is not None:
        event_sink("stage_completed", fields)
    return result


@dataclass(frozen=True)
class ReconciliationSummary:
    scanned: int
    adopted_legacy: int
    registered: int
    already_registered: int
    registered_hashes: tuple[str, ...]
    errors: tuple[str, ...]


@dataclass(frozen=True)
class ArchiveRegistration:
    """Result of registering one exact manifest-backed archive."""

    evidence_bundle_hash: str
    session_id: int
    was_existing: bool
    run_id: int | None
    run_was_existing: bool


def register_archive(
    archive_root: Path,
    db_path: Path,
    evidence_bundle_hash: str,
    *,
    event_sink: ArchiveEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> ArchiveRegistration:
    """Fully verify and register exactly one named finalized archive."""
    if (
        len(evidence_bundle_hash) != 64
        or evidence_bundle_hash != evidence_bundle_hash.lower()
        or any(character not in "0123456789abcdef" for character in evidence_bundle_hash)
    ):
        raise ArchiveIntegrityError("archive selection must be one lowercase SHA-256")
    directory = Path(archive_root).resolve() / "sessions" / evidence_bundle_hash
    if directory.is_symlink() or not directory.is_dir():
        raise ArchiveIntegrityError(
            f"selected finalized archive does not exist: {evidence_bundle_hash}"
        )
    if not (directory / MANIFEST_NAME).is_file():
        raise ArchiveIntegrityError(
            f"selected finalized archive has no manifest: {evidence_bundle_hash}"
        )

    captured = _timed_archive_stage(
        "archive_verify",
        lambda: read_snapshot(directory),
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda snapshot: {
            "evidence_bundle_hash": snapshot.evidence_bundle_hash,
            "file_count": len(snapshot.files),
            "total_bytes": sum(item.bytes for item in snapshot.files),
        },
    )
    conn = _timed_archive_stage(
        "archive_open_database",
        lambda: repository.open_db(db_path),
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    try:
        session_id, was_existing = _timed_archive_stage(
            "archive_register_session",
            lambda: repository.register_finalized_session(
                conn,
                evidence_bundle_hash=captured.evidence_bundle_hash,
                captured_at=captured.captured_at,
                manifest_version=captured.manifest_version,
                manifest_sha256=captured.manifest_sha256,
                evidence_completeness=(
                    "partial" if captured.missing_principal_logs else "complete"
                ),
                files=captured.files,
            ),
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda result: {
                "session_id": result[0],
                "session_was_existing": result[1],
            },
        )
        run_id: int | None = None
        run_was_existing = False
        metadata = _timed_archive_stage(
            "archive_read_capture_metadata",
            lambda: read_capture_metadata(directory),
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda value: {"metadata_present": value is not None},
        )
        if metadata is not None:
            run_id, run_was_existing = _timed_archive_stage(
                "archive_register_capture_metadata",
                lambda: repository.register_capture_metadata(
                    conn,
                    session_id=session_id,
                    metadata=metadata,
                    files=captured.files,
                ),
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
                completion_fields=lambda result: {
                    "run_id": result[0],
                    "run_was_existing": result[1],
                },
            )
    finally:
        conn.close()
    return ArchiveRegistration(
        evidence_bundle_hash=evidence_bundle_hash,
        session_id=session_id,
        was_existing=was_existing,
        run_id=run_id,
        run_was_existing=run_was_existing,
    )


def reconcile_archives(
    archive_root: Path,
    db_path: Path,
    *,
    full_verify: bool = False,
    strict_integrity: bool = False,
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
                message = f"{bundle_hash}: registered session is missing its archive"
                if strict_integrity:
                    raise ArchiveIntegrityError(message)
                errors.append(message)
        for directory in directories:
            try:
                existing = repository.get_session_by_hash(conn, directory.name)
                manifest_path = directory / MANIFEST_NAME
                if (
                    not full_verify
                    and existing is not None
                    and existing["capture_status"] == "finalized"
                    and manifest_path.is_file()
                ):
                    files, manifest_sha256, completeness, manifest_version = (
                        snapshot_manifest_projection(directory)
                    )
                    if (
                        existing["capture_manifest_version"] == manifest_version
                        and existing["capture_manifest_sha256"] == manifest_sha256
                        and snapshot_file_metadata_matches_manifest(
                            directory, files=files
                        )
                    ):
                        repository.validate_finalized_session_projection(
                            conn,
                            session=existing,
                            manifest_version=manifest_version,
                            manifest_sha256=manifest_sha256,
                            evidence_completeness=completeness,
                            files=files,
                        )
                        metadata = read_capture_metadata(directory)
                        if metadata is not None:
                            repository.register_capture_metadata(
                                conn,
                                session_id=int(existing["session_id"]),
                                metadata=metadata,
                                files=files,
                            )
                        existing_count += 1
                        continue

                if manifest_path.is_file():
                    captured = read_snapshot(directory)
                else:
                    captured = adopt_legacy_archive(directory)
                    adopted += 1
                session_id, was_existing = repository.register_finalized_session(
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
                metadata = read_capture_metadata(directory)
                if metadata is not None:
                    repository.register_capture_metadata(
                        conn,
                        session_id=session_id,
                        metadata=metadata,
                        files=captured.files,
                    )
                if was_existing:
                    existing_count += 1
                else:
                    registered += 1
                    registered_hashes.append(captured.evidence_bundle_hash)
            except repository.ExistingErrorLogHashError:
                raise
            except sqlite3.Error:
                raise
            except (ArchiveIntegrityError, OSError, ValueError) as exc:
                if strict_integrity:
                    raise ArchiveIntegrityError(
                        f"{directory.name}: {exc}"
                    ) from exc
                errors.append(f"{directory.name}: {exc}")
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
