"""Deferred archive finalization, parsing, classification, and reporting."""

from __future__ import annotations

import json
import os
import platform
import secrets
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence, TextIO, TypeVar

from .archive_registry import reconcile_archives, register_archive
from .classification import Classifier, classify_session
from .classification.service import CLASSIFICATION_CONTRACT_VERSION
from .classification.projection_catalog import ProjectionCatalog
from .db import repository
from .harvester import (
    ArchiveIntegrityError,
    CapturedFile,
    finalize_pending,
    finalize_pending_captures,
    inspect_pending,
    read_snapshot,
    selected_pending_path,
)
from .parser.service import PARSER_CONTRACT_VERSION, parse_session
from .reporting import build_session_report, latest_report_target
from .runtime_context import parse_runtime_context
from .semantic_projection_service import (
    SEMANTIC_PROJECTION_CONTRACT_VERSION,
    project_classification_run,
)

T = TypeVar("T")
ProcessingEventSink = Callable[[str, dict[str, object]], None]
PROCESSING_EVENT_VERSION = 1


class ProcessorAlreadyRunning(RuntimeError):
    """Another process holds the runtime's processor lease."""


class ProcessorLease:
    """Hold a crash-releasing OS lock for the one allowed database processor."""

    def __init__(self, root: Path):
        self.path = Path(root).resolve() / "processing" / "processor.lock"
        self._stream = None

    def __enter__(self) -> ProcessorLease:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        stream = self.path.open("a+b")
        if stream.seek(0, os.SEEK_END) == 0:
            stream.write(b"\0")
            stream.flush()
            os.fsync(stream.fileno())
        stream.seek(0)
        try:
            if platform.system() == "Windows":
                import msvcrt

                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl

                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            stream.close()
            raise ProcessorAlreadyRunning(
                f"another ck3chronicle processor already holds {self.path}"
            ) from exc
        self._stream = stream
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._stream is None:
            return
        try:
            self._stream.seek(0)
            if platform.system() == "Windows":
                import msvcrt

                msvcrt.locking(self._stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(self._stream.fileno(), fcntl.LOCK_UN)
        finally:
            self._stream.close()
            self._stream = None


class ProcessingJournal:
    """Flush structured processing progress to a runtime-local JSONL file."""

    def __init__(self, root: Path):
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
        processing_root = Path(root).resolve() / "processing"
        self.path = processing_root / f"events-{timestamp}-{os.getpid()}.jsonl"
        self.status_path = processing_root / "processor-status.json"
        self._stream: TextIO | None = None
        self._sequence = 0
        self._emit_ns = 0
        self._append_fsync_ns = 0
        self._status_replace_ns = 0
        self._status_failures = 0
        self._status_last_error: str | None = None

    def __enter__(self) -> ProcessingJournal:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._stream = self.path.open("x", encoding="utf-8", newline="\n")
        return self

    def emit(self, event: str, fields: dict[str, object]) -> None:
        if self._stream is None:
            raise RuntimeError("processing journal is not open")
        emit_started_ns = time.perf_counter_ns()
        self._sequence += 1
        record = {
            "schema": "ck3chronicle.processing-event",
            "schema_version": PROCESSING_EVENT_VERSION,
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "processor_pid": os.getpid(),
            "sequence": self._sequence,
            "journal": str(self.path),
            "fields": fields,
        }
        append_started_ns = time.perf_counter_ns()
        self._stream.write(
            json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        )
        self._stream.flush()
        os.fsync(self._stream.fileno())
        self._append_fsync_ns += time.perf_counter_ns() - append_started_ns
        status_started_ns = time.perf_counter_ns()
        try:
            self._replace_status(record)
        except OSError as exc:
            # The append-only journal is authoritative. A replaceable status
            # snapshot must never turn a durably recorded stage into a failed
            # database operation.
            self._status_failures += 1
            self._status_last_error = f"{type(exc).__name__}: {exc}"
        finally:
            self._status_replace_ns += time.perf_counter_ns() - status_started_ns
            self._emit_ns += time.perf_counter_ns() - emit_started_ns

    def io_summary(self) -> dict[str, object]:
        """Return cumulative durable-journal cost before the next event."""
        return {
            "events_emitted": self._sequence,
            "emit_total_ms": round(self._emit_ns / 1_000_000, 3),
            "append_fsync_ms": round(self._append_fsync_ns / 1_000_000, 3),
            "status_replace_fsync_ms": round(
                self._status_replace_ns / 1_000_000,
                3,
            ),
            "status_replace_failures": self._status_failures,
            "status_replace_last_error": self._status_last_error,
        }

    def _replace_status(self, record: dict[str, object]) -> None:
        temporary = self.status_path.parent / (
            f".{self.status_path.name}-{os.getpid()}-{secrets.token_hex(4)}"
        )
        try:
            with temporary.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(
                    record,
                    stream,
                    ensure_ascii=False,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.status_path)
        finally:
            temporary.unlink(missing_ok=True)

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None


def _duration_ms(started_ns: int, monotonic_ns: Callable[[], int]) -> float:
    return round((monotonic_ns() - started_ns) / 1_000_000, 3)


def _timed_stage(
    stage: str,
    operation: Callable[[], T],
    *,
    event_sink: ProcessingEventSink | None,
    monotonic_ns: Callable[[], int],
    session_id: int | None = None,
    completion_fields: Callable[[T], dict[str, object]] | None = None,
) -> T:
    context: dict[str, object] = {"stage": stage}
    if session_id is not None:
        context["session_id"] = session_id
    if event_sink is not None:
        event_sink("stage_started", dict(context))
    started_ns = monotonic_ns()
    try:
        result = operation()
    except BaseException as exc:
        if event_sink is not None:
            try:
                event_sink(
                    "stage_failed",
                    {
                        **context,
                        "duration_ms": _duration_ms(started_ns, monotonic_ns),
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    },
                )
            except Exception:
                pass
        raise
    fields = {
        **context,
        "duration_ms": _duration_ms(started_ns, monotonic_ns),
    }
    if completion_fields is not None:
        fields.update(completion_fields(result))
    if event_sink is not None:
        event_sink("stage_completed", fields)
    return result


@dataclass(frozen=True)
class ProcessingResult:
    finalized_pending: int
    registered_archives: int
    registered_runs: int
    context_sessions: int
    parsed_sessions: int
    classified_sessions: int
    projected_sessions: int
    reconciliation_errors: tuple[str, ...]
    latest_report: dict[str, object] | None


@dataclass(frozen=True)
class PlannedSession:
    session_id: int
    evidence_bundle_hash: str
    archive_path: Path
    archive_manifest_sha256: str
    archive_file_count: int
    registered_at: str
    total_bytes: int
    source_blocks: int
    runtime_context: str
    parse: str
    classification: str
    semantic_projection: str

    def as_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "evidence_bundle_hash": self.evidence_bundle_hash,
            "archive": {
                "path": str(self.archive_path),
                "manifest_sha256": self.archive_manifest_sha256,
                "file_count": self.archive_file_count,
                "verified": True,
            },
            "registered_at": self.registered_at,
            "total_bytes": self.total_bytes,
            "source_blocks": self.source_blocks,
            "stages": {
                "runtime_context": self.runtime_context,
                "parse": self.parse,
                "classification": self.classification,
                "semantic_projection": self.semantic_projection,
            },
        }


@dataclass(frozen=True)
class SelectedProcessingPlan:
    root: Path
    database: Path
    sessions: tuple[PlannedSession, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "schema": "ck3chronicle.selected-processing-plan",
            "schema_version": 1,
            "read_only": True,
            "root": str(self.root),
            "database": str(self.database),
            "bounds": {
                "pending_captures": 0,
                "historical_sessions": len(self.sessions),
            },
            "session_count": len(self.sessions),
            "sessions": [session.as_dict() for session in self.sessions],
            "scope": {
                "pending_finalization": "disabled",
                "archive_reconciliation": "disabled",
                "unselected_sessions": "untouched",
            },
        }


@dataclass(frozen=True)
class PendingProcessingPlan:
    """Read-only plan for exactly one protected pending capture."""

    root: Path
    database: Path
    pending_name: str
    pending_path: Path
    captured_at: str
    files: tuple[CapturedFile, ...]
    evidence_bundle_hash: str
    manifest_sha256: str
    manifest_present: bool
    metadata_present: bool
    archive_path: Path
    archive_present: bool
    model_revision_id: str
    model_sha256: str
    projection_catalog_revision_id: str
    projection_catalog_sha256: str

    @property
    def error_log_sha256(self) -> str:
        return next(
            item.sha256
            for item in self.files
            if item.kind == "log" and item.rel_path == "error.log"
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "schema": "ck3chronicle.pending-processing-plan",
            "schema_version": 1,
            "read_only": True,
            "root": str(self.root),
            "database": str(self.database),
            "bounds": {"pending_captures": 1, "historical_sessions": 0},
            "capture": {
                "pending_name": self.pending_name,
                "pending_path": str(self.pending_path),
                "captured_at": self.captured_at,
                "file_count": len(self.files),
                "total_bytes": sum(item.bytes for item in self.files),
                "error_log_sha256": self.error_log_sha256,
                "files": [
                    {
                        "rel_path": item.rel_path,
                        "kind": item.kind,
                        "bytes": item.bytes,
                        "sha256": item.sha256,
                    }
                    for item in self.files
                ],
                "metadata_present": self.metadata_present,
                "manifest_present": self.manifest_present,
            },
            "archive": {
                "evidence_bundle_hash": self.evidence_bundle_hash,
                "manifest_sha256": self.manifest_sha256,
                "path": str(self.archive_path),
                "already_present": self.archive_present,
            },
            "semantic_runtime": {
                "model_revision_id": self.model_revision_id,
                "model_sha256": self.model_sha256,
                "projection_catalog_revision_id": (
                    self.projection_catalog_revision_id
                ),
                "projection_catalog_sha256": self.projection_catalog_sha256,
            },
            "stages": {
                "finalize_selected_pending": (
                    "verify_existing" if self.archive_present else "run"
                ),
                "register_selected_archive": "run",
                "runtime_context": "ensure",
                "parse": "run",
                "classification": "run",
                "semantic_projection": "run",
                "latest_report": "disabled",
                "unselected_pending": "untouched",
                "historical_backfill": "disabled",
            },
        }


@dataclass(frozen=True)
class PendingProcessingResult:
    pending_name: str
    evidence_bundle_hash: str
    session_id: int
    run_id: int
    archive_was_existing: bool
    run_was_existing: bool
    processing: ProcessingResult


def plan_pending_capture(
    root: Path,
    classifier: Classifier,
    projection_catalog: ProjectionCatalog,
    pending_name: str,
) -> PendingProcessingPlan:
    """Hash, validate, and duplicate-check one pending capture without writes."""
    import sqlite3

    evidence_root = Path(root).resolve()
    db_path = evidence_root / "ck3chronicle.db"
    if not db_path.is_file():
        raise sqlite3.OperationalError(f"database is not a file: {db_path}")
    pending_path = selected_pending_path(evidence_root, pending_name)
    inspection = inspect_pending(pending_path)
    if not inspection.metadata_present:
        raise ArchiveIntegrityError(
            "selected pending capture has no capture-metadata.json; "
            "migrate its retained metadata before processing"
        )
    error_file = next(
        (
            item
            for item in inspection.files
            if item.kind == "log" and item.rel_path == "error.log"
        ),
        None,
    )
    if error_file is None:
        raise ArchiveIntegrityError("pending capture is missing mandatory error.log")

    archive_path = evidence_root / "sessions" / inspection.evidence_bundle_hash
    archive_present = archive_path.exists()
    if archive_present:
        archived = read_snapshot(archive_path)
        planned_descriptor = sorted(
            (item.rel_path, item.sha256, item.bytes, item.kind)
            for item in inspection.files
        )
        archived_descriptor = sorted(
            (item.rel_path, item.sha256, item.bytes, item.kind)
            for item in archived.files
        )
        if archived_descriptor != planned_descriptor:
            raise ArchiveIntegrityError(
                "selected pending capture disagrees with its existing archive"
            )

    conn = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        duplicate = repository.get_session_by_error_log_hash(
            conn,
            error_file.sha256,
        )
    finally:
        conn.close()
    if duplicate is not None:
        raise repository.ExistingErrorLogHashError(
            error_file.sha256,
            int(duplicate["session_id"]),
        )

    return PendingProcessingPlan(
        root=evidence_root,
        database=db_path,
        pending_name=pending_name,
        pending_path=pending_path,
        captured_at=inspection.captured_at,
        files=inspection.files,
        evidence_bundle_hash=inspection.evidence_bundle_hash,
        manifest_sha256=inspection.manifest_sha256,
        manifest_present=inspection.manifest_present,
        metadata_present=inspection.metadata_present,
        archive_path=archive_path,
        archive_present=archive_present,
        model_revision_id=classifier.model.revision_id,
        model_sha256=classifier.model.sha256,
        projection_catalog_revision_id=projection_catalog.revision_id,
        projection_catalog_sha256=projection_catalog.sha256,
    )


def process_planned_pending_capture(
    plan: PendingProcessingPlan,
    classifier: Classifier,
    projection_catalog: ProjectionCatalog,
    *,
    event_sink: ProcessingEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> PendingProcessingResult:
    """Finalize, register, and derive only the capture named by a prior plan."""
    refreshed = _timed_stage(
        "validate_pending_plan",
        lambda: plan_pending_capture(
            plan.root,
            classifier,
            projection_catalog,
            plan.pending_name,
        ),
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda current: {
            "pending_name": current.pending_name,
            "evidence_bundle_hash": current.evidence_bundle_hash,
            "file_count": len(current.files),
            "total_bytes": sum(item.bytes for item in current.files),
        },
    )
    if (
        refreshed.evidence_bundle_hash != plan.evidence_bundle_hash
        or refreshed.manifest_sha256 != plan.manifest_sha256
        or refreshed.error_log_sha256 != plan.error_log_sha256
    ):
        raise ArchiveIntegrityError(
            "selected pending capture changed after its read-only plan"
        )

    finalized = _timed_stage(
        "finalize_selected_pending",
        lambda: finalize_pending(
            refreshed.pending_path,
            refreshed.root,
            expected_evidence_bundle_hash=plan.evidence_bundle_hash,
            expected_manifest_sha256=plan.manifest_sha256,
        ),
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda captured: {
            "pending_name": plan.pending_name,
            "evidence_bundle_hash": captured.evidence_bundle_hash,
            "archive": str(captured.dest_dir),
            "archive_was_existing": captured.was_existing,
            "file_count": len(captured.files),
            "total_bytes": sum(item.bytes for item in captured.files),
        },
    )
    registration = _timed_stage(
        "register_selected_archive",
        lambda: register_archive(
            refreshed.root,
            refreshed.database,
            finalized.evidence_bundle_hash,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        ),
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda registered: {
            "evidence_bundle_hash": registered.evidence_bundle_hash,
            "session_id": registered.session_id,
            "run_id": registered.run_id,
            "session_was_existing": registered.was_existing,
            "run_was_existing": registered.run_was_existing,
        },
    )
    if registration.run_id is None:
        raise ValueError("selected pending archive registered without a Run ID")
    processed = process_selected_sessions(
        refreshed.root,
        classifier,
        projection_catalog,
        (registration.session_id,),
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    return PendingProcessingResult(
        pending_name=plan.pending_name,
        evidence_bundle_hash=registration.evidence_bundle_hash,
        session_id=registration.session_id,
        run_id=registration.run_id,
        archive_was_existing=finalized.was_existing,
        run_was_existing=registration.run_was_existing,
        processing=processed,
    )


def plan_selected_sessions(
    root: Path,
    classifier: Classifier,
    projection_catalog: ProjectionCatalog,
    session_ids: Sequence[int],
) -> SelectedProcessingPlan:
    """Describe exact existing-session work using a strict read-only connection."""
    import sqlite3

    evidence_root = Path(root).resolve()
    db_path = evidence_root / "ck3chronicle.db"
    requested = tuple(int(session_id) for session_id in session_ids)
    if not requested:
        raise ValueError("session_ids must not be empty")
    if len(set(requested)) != len(requested):
        raise ValueError("session_ids contains duplicates")
    if not db_path.is_file():
        raise sqlite3.OperationalError(f"database is not a file: {db_path}")

    conn = sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA query_only = ON")
    conn.execute("PRAGMA foreign_keys = ON")
    planned: list[PlannedSession] = []
    try:
        for session_id in requested:
            session = repository.get_session(conn, session_id)
            if session is None or session["capture_status"] != "finalized":
                raise ValueError(
                    f"selected finalized session_id does not exist: {session_id}"
                )
            evidence_bundle_hash = str(session["evidence_bundle_hash"])
            archive_path = evidence_root / "sessions" / evidence_bundle_hash
            if archive_path.is_symlink() or not archive_path.is_dir():
                raise ArchiveIntegrityError(
                    "selected finalized session is missing its archive: "
                    f"{session_id} ({evidence_bundle_hash})"
                )
            archive = read_snapshot(archive_path)
            repository.validate_finalized_session_projection(
                conn,
                session=session,
                manifest_version=archive.manifest_version,
                manifest_sha256=archive.manifest_sha256,
                evidence_completeness=(
                    "partial" if archive.missing_principal_logs else "complete"
                ),
                files=archive.files,
            )
            parse_current = (
                session["parse_status"] == "succeeded"
                and session["parser_contract_version"] == PARSER_CONTRACT_VERSION
            )
            classification_run = repository.get_classification_run(
                conn,
                session_id,
                classifier.model.sha256,
            )
            classification_current = (
                parse_current
                and classification_run is not None
                and classification_run["classification_contract_version"]
                == CLASSIFICATION_CONTRACT_VERSION
            )
            projection = repository.get_semantic_projection_run(conn, session_id)
            projection_current = (
                classification_current
                and projection is not None
                and int(projection["classification_run_id"])
                == int(classification_run["run_id"])
                and projection["model_sha256"] == classifier.model.sha256
                and projection["projection_catalog_sha256"]
                == projection_catalog.sha256
                and projection["projection_catalog_revision_id"]
                == projection_catalog.revision_id
                and int(projection["projection_catalog_schema_version"])
                == projection_catalog.schema_version
                and projection["projection_contract_version"]
                == SEMANTIC_PROJECTION_CONTRACT_VERSION
            )
            planned.append(
                PlannedSession(
                    session_id=session_id,
                    evidence_bundle_hash=evidence_bundle_hash,
                    archive_path=archive_path,
                    archive_manifest_sha256=archive.manifest_sha256,
                    archive_file_count=len(archive.files),
                    registered_at=str(session["created_at"]),
                    total_bytes=int(session["total_bytes"]),
                    source_blocks=int(session["parse_source_blocks"] or 0),
                    runtime_context="ensure",
                    parse="skip_current" if parse_current else "run",
                    classification=(
                        "skip_current" if classification_current else "run"
                    ),
                    semantic_projection=(
                        "skip_current" if projection_current else "run"
                    ),
                )
            )
    finally:
        conn.close()
    return SelectedProcessingPlan(evidence_root, db_path, tuple(planned))


def process_pending(
    root: Path,
    classifier: Classifier,
    projection_catalog: ProjectionCatalog | None = None,
    *,
    event_sink: ProcessingEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
    finalize_captures: bool = True,
    reconcile_filesystem: bool = True,
    selected_session_ids: Sequence[int] | None = None,
    max_sessions: int | None = None,
    build_latest: bool = True,
) -> ProcessingResult:
    """Process an explicitly bounded set of finalized existing sessions.

    The watcher never calls this function. It operates only on protected
    pending copies and immutable archives after the time-critical exit path.
    """
    evidence_root = Path(root).resolve()
    db_path = evidence_root / "ck3chronicle.db"
    if max_sessions is not None and max_sessions < 1:
        raise ValueError("max_sessions must be positive")
    requested_session_ids = (
        None
        if selected_session_ids is None
        else tuple(int(session_id) for session_id in selected_session_ids)
    )
    if requested_session_ids is not None:
        if not requested_session_ids:
            raise ValueError("selected_session_ids must not be empty")
        if len(set(requested_session_ids)) != len(requested_session_ids):
            raise ValueError("selected_session_ids contains duplicates")
    if finalize_captures or reconcile_filesystem:
        raise ValueError(
            "wide pending finalization/reconciliation is disabled; use the "
            "exact pending-capture operation"
        )
    if requested_session_ids is None:
        raise ValueError("explicit selected_session_ids are required")
    pipeline_started_ns = monotonic_ns()
    if event_sink is not None:
        event_sink(
            "pipeline_started",
            {
                "root": str(evidence_root),
                "database": str(db_path),
                "finalize_captures": finalize_captures,
                "reconcile_filesystem": reconcile_filesystem,
                "selected_session_ids": (
                    list(requested_session_ids)
                    if requested_session_ids is not None
                    else None
                ),
                "max_sessions": max_sessions,
                "build_latest": build_latest,
            },
        )
    try:
        if projection_catalog is None:
            from .classification.catalog import load_approved_projection_catalog

            projection_catalog = _timed_stage(
                "load_projection_catalog",
                lambda: load_approved_projection_catalog(classifier.model),
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
            )
        pending_errors: list[str] = []
        if finalize_captures:
            finalized = _timed_stage(
                "finalize_pending",
                lambda: finalize_pending_captures(
                    evidence_root,
                    errors=pending_errors,
                ),
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
                completion_fields=lambda rows: {
                    "finalized_pending": len(rows),
                    "error_count": len(pending_errors),
                },
            )
        else:
            finalized = ()
            if event_sink is not None:
                event_sink(
                    "stage_skipped",
                    {"stage": "finalize_pending", "reason": "disabled_by_scope"},
                )
        reconciliation_registered = 0
        reconciliation_errors: tuple[str, ...] = ()
        if reconcile_filesystem:
            reconciliation = _timed_stage(
                "reconcile_archives",
                lambda: reconcile_archives(
                    evidence_root,
                    db_path,
                    strict_integrity=True,
                ),
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
                completion_fields=lambda result: {
                    "registered_archives": result.registered,
                    "existing_archives": result.already_registered,
                    "error_count": len(result.errors),
                },
            )
            reconciliation_registered = reconciliation.registered
            reconciliation_errors = reconciliation.errors
        elif event_sink is not None:
            event_sink(
                "stage_skipped",
                {"stage": "reconcile_archives", "reason": "disabled_by_scope"},
            )

        parsed = 0
        classified = 0
        projected = 0
        context_sessions = 0
        conn = _timed_stage(
            "open_database",
            lambda: repository.open_db(db_path),
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        try:
            sessions = _timed_stage(
                "list_sessions",
                lambda: repository.list_sessions(conn, limit=1_000_000),
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
                completion_fields=lambda rows: {"session_count": len(rows)},
            )
            finalized_sessions = [
                session
                for session in sessions
                if session["capture_status"] == "finalized"
            ]
            if requested_session_ids is not None:
                by_id = {
                    int(session["session_id"]): session
                    for session in finalized_sessions
                }
                missing = [
                    session_id
                    for session_id in requested_session_ids
                    if session_id not in by_id
                ]
                if missing:
                    raise ValueError(
                        "selected finalized session IDs do not exist: "
                        + ", ".join(str(session_id) for session_id in missing)
                    )
                finalized_sessions = [
                    by_id[session_id] for session_id in requested_session_ids
                ]
            if max_sessions is not None:
                finalized_sessions = finalized_sessions[:max_sessions]
            if event_sink is not None:
                event_sink(
                    "session_inventory",
                    {
                        "session_count": len(sessions),
                        "selected_finalized_session_count": len(finalized_sessions),
                        "selected_session_ids": [
                            int(session["session_id"])
                            for session in finalized_sessions
                        ],
                    },
                )
            # Chronology controls presentation, not processing correctness.
            # Every registered finalized archive reaches the same derived state.
            for index, session in enumerate(finalized_sessions, start=1):
                session_id = int(session["session_id"])
                session_started_ns = monotonic_ns()
                if event_sink is not None:
                    event_sink(
                        "session_started",
                        {
                            "session_id": session_id,
                            "index": index,
                            "total": len(finalized_sessions),
                            "parse_status": str(session["parse_status"]),
                            "parser_contract_version": session[
                                "parser_contract_version"
                            ],
                        },
                    )
                context = _timed_stage(
                    "runtime_context",
                    lambda: parse_runtime_context(conn, evidence_root, session_id),
                    event_sink=event_sink,
                    monotonic_ns=monotonic_ns,
                    session_id=session_id,
                    completion_fields=lambda result: {
                        "mutated": bool(result.mutated)
                    },
                )
                context_sessions += int(context.mutated)
                if (
                    session["parse_status"] != "succeeded"
                    or session["parser_contract_version"] != PARSER_CONTRACT_VERSION
                ):
                    parse_result = _timed_stage(
                        "parse",
                        lambda: parse_session(
                            conn,
                            evidence_root,
                            session_id,
                            event_sink=event_sink,
                            monotonic_ns=monotonic_ns,
                        ),
                        event_sink=event_sink,
                        monotonic_ns=monotonic_ns,
                        session_id=session_id,
                        completion_fields=lambda result: {
                            "mutated": bool(result.mutated)
                        },
                    )
                    parsed += int(parse_result.mutated)
                elif event_sink is not None:
                    event_sink(
                        "stage_skipped",
                        {
                            "stage": "parse",
                            "session_id": session_id,
                            "reason": "current_successful_parse",
                        },
                    )
                classification = _timed_stage(
                    "classification",
                    lambda: classify_session(
                        conn,
                        session_id,
                        classifier,
                        event_sink=event_sink,
                        monotonic_ns=monotonic_ns,
                    ),
                    event_sink=event_sink,
                    monotonic_ns=monotonic_ns,
                    session_id=session_id,
                    completion_fields=lambda result: {
                        "mutated": bool(result.mutated)
                    },
                )
                classified += int(classification.mutated)
                projection = _timed_stage(
                    "semantic_projection",
                    lambda: project_classification_run(
                        conn,
                        session_id,
                        projection_catalog,
                        event_sink=event_sink,
                        monotonic_ns=monotonic_ns,
                    ),
                    event_sink=event_sink,
                    monotonic_ns=monotonic_ns,
                    session_id=session_id,
                    completion_fields=lambda result: {
                        "mutated": bool(result.mutated)
                    },
                )
                projected += int(projection.mutated)
                if event_sink is not None:
                    event_sink(
                        "session_completed",
                        {
                            "session_id": session_id,
                            "index": index,
                            "total": len(finalized_sessions),
                            "duration_ms": _duration_ms(
                                session_started_ns,
                                monotonic_ns,
                            ),
                        },
                    )

            if build_latest:
                latest_target = _timed_stage(
                    "select_latest_report_target",
                    lambda: latest_report_target(conn),
                    event_sink=event_sink,
                    monotonic_ns=monotonic_ns,
                    completion_fields=lambda target: {
                        "target_found": target is not None
                    },
                )
                latest_report = (
                    _timed_stage(
                        "build_latest_report",
                        lambda: build_session_report(
                            conn,
                            latest_target,
                            model_sha256=classifier.model.sha256,
                        ),
                        event_sink=event_sink,
                        monotonic_ns=monotonic_ns,
                    )
                    if latest_target is not None
                    else None
                )
            else:
                latest_report = None
                if event_sink is not None:
                    event_sink(
                        "stage_skipped",
                        {
                            "stage": "build_latest_report",
                            "reason": "disabled_by_scope",
                        },
                    )
        finally:
            conn.close()

        result = ProcessingResult(
            finalized_pending=len(finalized),
            registered_archives=reconciliation_registered,
            registered_runs=reconciliation_registered,
            context_sessions=context_sessions,
            parsed_sessions=parsed,
            classified_sessions=classified,
            projected_sessions=projected,
            reconciliation_errors=(
                tuple(pending_errors) + reconciliation_errors
            ),
            latest_report=latest_report,
        )
        if event_sink is not None:
            event_sink(
                "pipeline_completed",
                {
                    "duration_ms": _duration_ms(
                        pipeline_started_ns,
                        monotonic_ns,
                    ),
                    "finalized_pending": result.finalized_pending,
                    "registered_archives": result.registered_archives,
                    "context_sessions": result.context_sessions,
                    "parsed_sessions": result.parsed_sessions,
                    "classified_sessions": result.classified_sessions,
                    "projected_sessions": result.projected_sessions,
                    "reconciliation_error_count": len(
                        result.reconciliation_errors
                    ),
                },
            )
        return result
    except BaseException as exc:
        if event_sink is not None:
            try:
                event_sink(
                    "pipeline_failed",
                    {
                        "duration_ms": _duration_ms(
                            pipeline_started_ns,
                            monotonic_ns,
                        ),
                        "error_type": type(exc).__name__,
                        "error": str(exc),
                    },
                )
            except Exception:
                pass
        raise


def process_selected_sessions(
    root: Path,
    classifier: Classifier,
    projection_catalog: ProjectionCatalog,
    session_ids: Sequence[int],
    *,
    event_sink: ProcessingEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> ProcessingResult:
    """Bring only explicitly named existing sessions to current derived state."""
    requested = tuple(int(session_id) for session_id in session_ids)
    return process_pending(
        root,
        classifier,
        projection_catalog,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        finalize_captures=False,
        reconcile_filesystem=False,
        selected_session_ids=requested,
        max_sessions=len(requested),
        build_latest=False,
    )
