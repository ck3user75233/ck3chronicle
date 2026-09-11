"""Thin data-access layer for ck3chronicle SQLite database."""
from __future__ import annotations

import sqlite3
import json
import time
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence, TypeVar

from .migrations import apply_migrations, migrations_required
from .payloads import payload_sha256
from ..models.issue import NormalizedIssue
from ..models.parse import (
    ClusterRecord,
    OccurrenceRecord,
    ParseCounters,
    ParseResult,
    SourceBlockRecord,
)

T = TypeVar("T")
ProjectionEventSink = Callable[[str, dict[str, object]], None]


def _repository_stage(
    stage: str,
    operation: Callable[[], T],
    *,
    session_id: int,
    event_sink: ProjectionEventSink | None,
    monotonic_ns: Callable[[], int],
    completion_fields: Callable[[T], dict[str, object]] | None = None,
) -> T:
    context: dict[str, object] = {"stage": stage, "session_id": session_id}
    if event_sink is not None:
        event_sink("stage_started", dict(context))
    started_ns = monotonic_ns()
    try:
        result = operation()
    except BaseException as exc:
        if event_sink is not None:
            event_sink(
                "stage_failed",
                {
                    **context,
                    "duration_ms": round(
                        (monotonic_ns() - started_ns) / 1_000_000, 3
                    ),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
            )
        raise
    fields = {
        **context,
        "duration_ms": round((monotonic_ns() - started_ns) / 1_000_000, 3),
    }
    if completion_fields is not None:
        fields.update(completion_fields(result))
    if event_sink is not None:
        event_sink("stage_completed", fields)
    return result


def open_db(path: Path) -> sqlite3.Connection:
    """Open (or create) the ck3chronicle database, applying migrations."""
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        compact_storage_migrated = apply_migrations(conn)
        reclaim_marker = conn.execute(
            "SELECT version FROM schema_versions WHERE component = ?",
            ("storage_reclaimed",),
        ).fetchone()
        if compact_storage_migrated or reclaim_marker is None:
            quick_check = str(conn.execute("PRAGMA quick_check").fetchone()[0])
            foreign_key_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
            if quick_check != "ok" or foreign_key_errors:
                raise sqlite3.DatabaseError(
                    "refusing automatic page reclamation after failed integrity check"
                )
            # The logical migration has already committed. VACUUM changes no
            # logical content; it returns now-unreferenced legacy pages to the
            # OS. Record success only afterwards so an interrupted/failed
            # reclaim is retried on the next ordinary database open.
            if int(conn.execute("PRAGMA freelist_count").fetchone()[0]) > 0:
                conn.execute("VACUUM")
            conn.execute(
                """
                INSERT OR REPLACE INTO schema_versions
                    (component, version, migrated_at)
                VALUES (?, ?, ?)
                """,
                (
                    "storage_reclaimed",
                    1,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()
    except Exception:
        conn.close()
        raise
    return conn


class DatabaseMigrationRequired(sqlite3.DatabaseError):
    """A read-only operation found a database needing explicit migration."""


def open_db_readonly(path: Path) -> sqlite3.Connection:
    """Open an existing current database without any implicit migration.

    SQLite's read-only URI prevents accidental writes in downstream query code,
    while ``query_only`` provides a second explicit guard at the connection
    level. Schema changes require a separately authorized writable workflow.
    """
    resolved_path = Path(path).resolve()
    if not resolved_path.is_file():
        raise sqlite3.OperationalError(f"database is not a file: {resolved_path}")

    def connect_readonly() -> sqlite3.Connection:
        opened = sqlite3.connect(f"{resolved_path.as_uri()}?mode=ro", uri=True)
        opened.row_factory = sqlite3.Row
        opened.execute("PRAGMA foreign_keys = ON")
        opened.execute("PRAGMA query_only = ON")
        return opened

    conn = connect_readonly()
    try:
        if migrations_required(conn):
            raise DatabaseMigrationRequired(
                "database schema migration is required; read-only command did not "
                "modify it"
            )
    except Exception:
        conn.close()
        raise
    return conn


def get_session_by_hash(
    conn: sqlite3.Connection, evidence_bundle_hash: str
) -> sqlite3.Row | None:
    cur = conn.execute(
        "SELECT * FROM sessions WHERE evidence_bundle_hash = ?",
        (evidence_bundle_hash,),
    )
    return cur.fetchone()


class ExistingErrorLogHashError(ValueError):
    """An error.log hash is already assigned to a Run ID."""

    def __init__(self, sha256: str, session_id: int):
        self.sha256 = sha256
        self.session_id = session_id
        super().__init__(
            f"error.log SHA-256 {sha256} already exists; session_id={session_id}"
        )


def get_session_by_error_log_hash(
    conn: sqlite3.Connection, sha256: str
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT s.*
        FROM sessions s
        JOIN session_files sf ON sf.session_id = s.session_id
        WHERE sf.kind = 'log' AND sf.rel_path = 'error.log' AND sf.sha256 = ?
        ORDER BY s.session_id
        LIMIT 1
        """,
        (sha256,),
    ).fetchone()


def add_session_file(
    conn: sqlite3.Connection,
    session_id: int,
    rel_path: str,
    sha256: str,
    bytes_: int,
    kind: str,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO session_files (session_id, rel_path, sha256, bytes, kind)
        VALUES (?, ?, ?, ?, ?)
        """,
        (session_id, rel_path, sha256, bytes_, kind),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def validate_finalized_session_projection(
    conn: sqlite3.Connection,
    *,
    session: sqlite3.Row,
    manifest_version: int,
    manifest_sha256: str,
    evidence_completeness: str,
    files: Sequence[Any],
) -> None:
    """Validate the rebuildable DB projection against an archive manifest.

    This performs no writes and reads no archived evidence bytes.  It is the
    steady-state counterpart to ``register_finalized_session`` and prevents a
    trusted archive fast path from concealing corruption in SQLite.
    """
    if session["capture_status"] != "finalized":
        raise ValueError("existing session is not finalized")
    if session["capture_manifest_version"] != manifest_version:
        raise ValueError("registered capture manifest version disagrees")
    if session["capture_manifest_sha256"] != manifest_sha256:
        raise ValueError("registered capture manifest hash disagrees")

    expected_rows = sorted(
        (item.rel_path, item.sha256, int(item.bytes), item.kind) for item in files
    )
    actual_rows = sorted(
        tuple(row)
        for row in conn.execute(
            """
            SELECT rel_path, sha256, bytes, kind
            FROM session_files
            WHERE session_id = ?
            """,
            (session["session_id"],),
        ).fetchall()
    )
    if actual_rows != expected_rows:
        raise ValueError("registered session manifest disagrees with finalized archive")

    expected_aggregates = (
        sum(item.kind == "log" for item in files),
        int(any(item.kind == "crash" for item in files)),
        sum(int(item.bytes) for item in files),
    )
    actual_aggregates = (
        int(session["log_count"]),
        int(session["crash_present"]),
        int(session["total_bytes"]),
    )
    if actual_aggregates != expected_aggregates:
        raise ValueError("registered session aggregates disagree with manifest")
    if session["evidence_completeness"] != evidence_completeness:
        raise ValueError("registered evidence completeness disagrees")


def register_finalized_session(
    conn: sqlite3.Connection,
    *,
    evidence_bundle_hash: str,
    captured_at: str,
    manifest_version: int,
    manifest_sha256: str,
    evidence_completeness: str,
    files: Sequence[Any],
) -> tuple[int, bool]:
    """Atomically register a finalized archive and its exact file manifest.

    Returns ``(session_id, was_existing)``. An existing row is accepted only
    when every registered file agrees with the supplied finalized manifest.
    """
    log_count = sum(item.kind == "log" for item in files)
    crash_present = any(item.kind == "crash" for item in files)
    total_bytes = sum(int(item.bytes) for item in files)
    expected_rows = sorted(
        (item.rel_path, item.sha256, int(item.bytes), item.kind) for item in files
    )
    try:
        conn.execute("BEGIN IMMEDIATE")
        existing = get_session_by_hash(conn, evidence_bundle_hash)
        if existing is not None:
            raw_rows = sorted(
                tuple(row)
                for row in conn.execute(
                    """
                    SELECT rel_path, sha256, bytes, kind
                    FROM session_files
                    WHERE session_id = ?
                    """,
                    (existing["session_id"],),
                ).fetchall()
            )
            normalized_rows = sorted(
                (
                    (
                        (
                            rel_path
                            if rel_path.replace("\\", "/").startswith("crash/")
                            else f"crash/{rel_path.replace('\\', '/')}"
                        ),
                        sha256,
                        bytes_,
                        "crash",
                    )
                    if kind == "crash_artifact"
                    else (rel_path.replace("\\", "/"), sha256, bytes_, kind)
                )
                for rel_path, sha256, bytes_, kind in raw_rows
            )
            if normalized_rows != expected_rows:
                raise ValueError(
                    "registered session manifest disagrees with finalized archive"
                )
            if existing["capture_status"] not in {"legacy_unverified", "finalized"}:
                raise ValueError("existing session is not finalized")
            existing_version = existing["capture_manifest_version"]
            existing_manifest_hash = existing["capture_manifest_sha256"]
            legacy = (
                existing["capture_status"] == "legacy_unverified"
                or existing_version is None
                or existing_manifest_hash is None
            )
            if not legacy and existing_version != manifest_version:
                raise ValueError("registered capture manifest version disagrees")
            if (
                not legacy and existing_manifest_hash != manifest_sha256
            ):
                raise ValueError("registered capture manifest hash disagrees")
            expected_aggregates = (log_count, int(crash_present), total_bytes)
            actual_aggregates = (
                int(existing["log_count"]),
                int(existing["crash_present"]),
                int(existing["total_bytes"]),
            )
            if not legacy and actual_aggregates != expected_aggregates:
                raise ValueError("registered session aggregates disagree with manifest")
            if (
                not legacy
                and existing["evidence_completeness"] != evidence_completeness
            ):
                raise ValueError("registered evidence completeness disagrees")

            # Normalize pre-P1 crash rows only after their byte manifest has
            # independently validated against the archive.
            if raw_rows != expected_rows:
                conn.execute(
                    "DELETE FROM session_files WHERE session_id = ?",
                    (existing["session_id"],),
                )
                conn.executemany(
                    """
                    INSERT INTO session_files (
                        session_id, rel_path, sha256, bytes, kind
                    ) VALUES (?, ?, ?, ?, ?)
                    """,
                    [
                        (existing["session_id"], rel_path, sha256, bytes_, kind)
                        for rel_path, sha256, bytes_, kind in expected_rows
                    ],
                )
            # Non-destructively promote a verified pre-manifest row. Evidence
            # identity and original created_at do not change.
            conn.execute(
                """
                UPDATE sessions
                SET capture_status = 'finalized',
                    capture_manifest_version = ?,
                    capture_manifest_sha256 = ?,
                    evidence_completeness = ?,
                    log_count = ?,
                    crash_present = ?,
                    total_bytes = ?
                WHERE session_id = ?
                """,
                (
                    manifest_version,
                    manifest_sha256,
                    evidence_completeness,
                    log_count,
                    int(crash_present),
                    total_bytes,
                    existing["session_id"],
                ),
            )
            conn.commit()
            return int(existing["session_id"]), True

        error_rows = [
            item for item in files
            if item.kind == "log" and item.rel_path == "error.log"
        ]
        if len(error_rows) != 1:
            raise ValueError("finalized session requires exactly one error.log")
        duplicate = get_session_by_error_log_hash(conn, error_rows[0].sha256)
        if duplicate is not None:
            raise ExistingErrorLogHashError(
                error_rows[0].sha256,
                int(duplicate["session_id"]),
            )

        cur = conn.execute(
            """
            INSERT INTO sessions (
                evidence_bundle_hash, created_at, log_count, crash_present,
                total_bytes, capture_status, capture_manifest_version,
                capture_manifest_sha256, evidence_completeness
            ) VALUES (?, ?, ?, ?, ?, 'finalized', ?, ?, ?)
            """,
            (
                evidence_bundle_hash,
                captured_at,
                log_count,
                int(crash_present),
                total_bytes,
                manifest_version,
                manifest_sha256,
                evidence_completeness,
            ),
        )
        assert cur.lastrowid is not None
        session_id = int(cur.lastrowid)
        conn.executemany(
            """
            INSERT INTO session_files (
                session_id, rel_path, sha256, bytes, kind
            ) VALUES (?, ?, ?, ?, ?)
            """,
            [
                (session_id, rel_path, sha256, bytes_, kind)
                for rel_path, sha256, bytes_, kind in expected_rows
            ],
        )
        conn.commit()
        return session_id, False
    except Exception:
        conn.rollback()
        raise


def _register_run_metadata(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    capture_name: str,
    trigger: str,
    process_name: str | None = None,
    observed_at: str | None = None,
    observed_started_at: str | None = None,
    observed_ended_at: str | None = None,
    process_pid: int | None = None,
    process_started_ns: int | None = None,
    termination_kind: str = "unknown",
    crash_folder_name: str | None = None,
    crash_folder_path: str | None = None,
    crash_detected_at: str | None = None,
    crash_association_method: str | None = None,
    crash_association_confidence: str | None = None,
    crash_exception_status: str = "not_applicable",
    crash_exception_source_rel_path: str | None = None,
    crash_exception_retained_path: str | None = None,
    crash_exception_sha256: str | None = None,
    crash_exception_bytes: int | None = None,
    crash_exception_source_mtime_ns: int | None = None,
) -> tuple[int, bool]:
    """Idempotently store one metadata row for one accepted Run ID."""
    if termination_kind not in {"normal", "crash", "unknown"}:
        raise ValueError("invalid run termination kind")
    if crash_exception_status not in {
        "captured",
        "absent",
        "unavailable",
        "not_applicable",
    }:
        raise ValueError("invalid crash exception status")
    if crash_exception_status in {"captured", "absent"} and termination_kind != "crash":
        raise ValueError("non-crash run has crash exception evidence")
    if crash_exception_status == "not_applicable" and termination_kind == "crash":
        raise ValueError("crash run marks exception evidence not applicable")
    if crash_exception_status == "unavailable" and termination_kind == "normal":
        raise ValueError("normal run has unavailable crash exception evidence")
    if crash_exception_status == "captured":
        if termination_kind != "crash" or any(
            value is None
            for value in (
                crash_exception_source_rel_path,
                crash_exception_retained_path,
                crash_exception_sha256,
                crash_exception_bytes,
                crash_exception_source_mtime_ns,
            )
        ):
            raise ValueError("captured crash exception metadata is incomplete")
    elif any(
        value is not None
        for value in (
            crash_exception_retained_path,
            crash_exception_sha256,
            crash_exception_bytes,
            crash_exception_source_mtime_ns,
        )
    ):
        raise ValueError("uncaptured crash exception has retained metadata")
    captured_at = observed_at or datetime.now(timezone.utc).isoformat()
    values = (
        session_id,
        capture_name,
        captured_at,
        observed_started_at,
        observed_ended_at,
        trigger,
        process_name,
        process_pid,
        process_started_ns,
        termination_kind,
        crash_folder_name,
        crash_folder_path,
        crash_detected_at,
        crash_association_method,
        crash_association_confidence,
        crash_exception_status,
        crash_exception_source_rel_path,
        crash_exception_retained_path,
        crash_exception_sha256,
        crash_exception_bytes,
        crash_exception_source_mtime_ns,
    )
    try:
        conn.execute("BEGIN IMMEDIATE")
        existing = conn.execute(
            "SELECT * FROM run_metadata WHERE capture_name = ?",
            (capture_name,),
        ).fetchone()
        if existing is not None:
            if int(existing["session_id"]) != session_id:
                raise ValueError("capture metadata points to a different session")
            expected_projection = {
                "captured_at": captured_at,
                "observed_started_at": observed_started_at,
                "observed_ended_at": observed_ended_at,
                "trigger": trigger,
                "process_name": process_name,
                "process_pid": process_pid,
                "process_started_ns": process_started_ns,
                "termination_kind": termination_kind,
                "crash_folder_name": crash_folder_name,
                "crash_folder_path": crash_folder_path,
                "crash_detected_at": crash_detected_at,
                "crash_association_method": crash_association_method,
                "crash_association_confidence": crash_association_confidence,
                "crash_exception_status": crash_exception_status,
                "crash_exception_source_rel_path": crash_exception_source_rel_path,
                "crash_exception_retained_path": crash_exception_retained_path,
                "crash_exception_sha256": crash_exception_sha256,
                "crash_exception_bytes": crash_exception_bytes,
                "crash_exception_source_mtime_ns": (
                    crash_exception_source_mtime_ns
                ),
            }
            if any(
                existing[column] != value
                for column, value in expected_projection.items()
            ):
                raise ValueError(
                    "capture metadata disagrees with indexed session"
                )
            conn.commit()
            return session_id, True
        existing_for_session = conn.execute(
            "SELECT capture_name FROM run_metadata WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if existing_for_session is not None:
            raise ValueError(
                "Run ID already has capture metadata under capture_name="
                f"{existing_for_session['capture_name']}"
            )
        conn.execute(
            """
            INSERT INTO run_metadata (
                session_id, capture_name, captured_at, observed_started_at,
                observed_ended_at, trigger, process_name, process_pid,
                process_started_ns, termination_kind, crash_folder_name,
                crash_folder_path, crash_detected_at,
                crash_association_method, crash_association_confidence,
                crash_exception_status, crash_exception_source_rel_path,
                crash_exception_retained_path, crash_exception_sha256,
                crash_exception_bytes, crash_exception_source_mtime_ns
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
            )
            """,
            values,
        )
        conn.commit()
        return session_id, False
    except Exception:
        conn.rollback()
        raise


def record_run_metadata(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    trigger: str,
    process_name: str | None = None,
    observed_at: str | None = None,
) -> int:
    """Record manual-import metadata without inventing lifecycle facts."""
    run_id, _ = _register_run_metadata(
        conn,
        session_id=session_id,
        capture_name=f"manual-{uuid.uuid4().hex}",
        trigger=trigger,
        process_name=process_name,
        observed_at=observed_at,
    )
    return run_id


def register_capture_metadata(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    metadata: Mapping[str, Any],
    files: Sequence[Any],
) -> tuple[int, bool]:
    """Project one archive manifest's capture metadata into SQLite."""
    capture_name = metadata.get("capture_id")
    if not isinstance(capture_name, str) or not capture_name:
        raise ValueError("capture metadata requires capture_id")
    captured_at = metadata.get("captured_at")
    if not isinstance(captured_at, str) or not captured_at:
        raise ValueError("capture metadata requires captured_at")
    trigger = metadata.get("trigger", "unknown")
    if not isinstance(trigger, str) or not trigger:
        raise ValueError("capture metadata trigger is invalid")
    process = metadata.get("process")
    process = process if isinstance(process, Mapping) else {}
    crash = metadata.get("crash")
    crash = crash if isinstance(crash, Mapping) else {}
    exception = metadata.get("crash_exception")
    exception = exception if isinstance(exception, Mapping) else {}
    exception_file = next(
        (
            item
            for item in files
            if item.kind == "crash" and item.rel_path == "crash/exception.txt"
        ),
        None,
    )
    session = get_session(conn, session_id)
    if session is None:
        raise ValueError("capture metadata session does not exist")
    retained_exception_path = (
        f"sessions/{session['evidence_bundle_hash']}/crash/exception.txt"
        if exception_file is not None
        else None
    )
    exception_status = str(exception.get("status", "not_applicable"))
    return _register_run_metadata(
        conn,
        session_id=session_id,
        capture_name=capture_name,
        trigger=trigger,
        process_name=(str(process.get("image_name")) if process.get("image_name") else None),
        observed_at=captured_at,
        observed_started_at=(
            str(metadata["observed_started_at"])
            if metadata.get("observed_started_at")
            else None
        ),
        observed_ended_at=(
            str(metadata["observed_ended_at"])
            if metadata.get("observed_ended_at")
            else None
        ),
        process_pid=(int(process["pid"]) if process.get("pid") is not None else None),
        process_started_ns=(
            int(process["started_ns"])
            if process.get("started_ns") is not None
            else None
        ),
        termination_kind=str(metadata.get("termination_kind", "unknown")),
        crash_folder_name=(
            str(crash["folder_name"]) if crash.get("folder_name") else None
        ),
        crash_folder_path=(
            str(crash["folder_path"]) if crash.get("folder_path") else None
        ),
        crash_detected_at=(
            str(crash["detected_at"]) if crash.get("detected_at") else None
        ),
        crash_association_method=(
            str(crash["association_method"])
            if crash.get("association_method")
            else None
        ),
        crash_association_confidence=(
            str(crash["confidence"]) if crash.get("confidence") else None
        ),
        crash_exception_status=exception_status,
        crash_exception_source_rel_path=(
            str(exception["source_rel_path"])
            if exception.get("source_rel_path")
            else None
        ),
        crash_exception_retained_path=(
            retained_exception_path
        ),
        crash_exception_sha256=(
            exception_file.sha256 if exception_file is not None else None
        ),
        crash_exception_bytes=(
            int(exception_file.bytes) if exception_file is not None else None
        ),
        crash_exception_source_mtime_ns=(
            int(exception_file.source_mtime_ns)
            if exception_file is not None
            else None
        ),
    )


def get_run_by_capture_name(
    conn: sqlite3.Connection, capture_name: str
) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM run_metadata WHERE capture_name = ?", (capture_name,)
    ).fetchone()


def get_run(conn: sqlite3.Connection, run_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM run_metadata WHERE session_id = ?",
        (run_id,),
    ).fetchone()


def latest_run(
    conn: sqlite3.Connection, *, reportable_only: bool = False
) -> sqlite3.Row | None:
    readiness = """
        AND s.parse_status = 'succeeded'
        AND EXISTS (
            SELECT 1
            FROM semantic_projection_runs spr
            JOIN classification_runs cr
              ON cr.run_id = spr.classification_run_id
             AND cr.session_id = spr.session_id
            WHERE spr.session_id = s.session_id
        )
    """ if reportable_only else ""
    return conn.execute(
        f"""
        SELECT rm.*
        FROM run_metadata rm
        JOIN sessions s ON s.session_id = rm.session_id
        WHERE s.capture_status = 'finalized'
        {readiness}
        ORDER BY COALESCE(rm.observed_ended_at, rm.captured_at) DESC,
                 rm.session_id DESC
        LIMIT 1
        """
    ).fetchone()


def get_run_for_session(
    conn: sqlite3.Connection, session_id: int
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT *
        FROM run_metadata
        WHERE session_id = ?
        """,
        (session_id,),
    ).fetchone()


def list_sessions(
    conn: sqlite3.Connection, limit: int = 100
) -> list[sqlite3.Row]:
    cur = conn.execute(
        """
        SELECT
            sessions.*,
            COALESCE(
                (
                    SELECT capture_name
                    FROM run_metadata
                    WHERE run_metadata.session_id = sessions.session_id
                ),
                'legacy-session-' || sessions.session_id
            ) AS session_name
        FROM sessions
        ORDER BY created_at DESC, session_id DESC
        LIMIT ?
        """,
        (limit,),
    )
    return cur.fetchall()


def get_session(conn: sqlite3.Connection, session_id: int) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()


def has_legacy_session_context_schema(conn: sqlite3.Connection) -> bool:
    """Return whether both rejected development context tables already exist."""
    tables = {
        row[0]
        for row in conn.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name IN ('session_contexts', 'session_mod_entries')
            """
        ).fetchall()
    }
    return tables == {"session_contexts", "session_mod_entries"}


def get_error_log_manifest_row(
    conn: sqlite3.Connection,
    session_id: int,
) -> sqlite3.Row | None:
    """Return the sole Trusted Run issue-source manifest row, if unambiguous."""
    rows = conn.execute(
        """
        SELECT *
        FROM session_files
        WHERE session_id = ? AND kind = 'log' AND rel_path = 'error.log'
        ORDER BY session_file_id
        """,
        (session_id,),
    ).fetchall()
    if len(rows) != 1:
        return None
    return rows[0]


def get_log_manifest_row(
    conn: sqlite3.Connection,
    session_id: int,
    rel_path: str,
) -> sqlite3.Row | None:
    """Return one exact captured log row, or None when absent/ambiguous."""
    rows = conn.execute(
        """
        SELECT *
        FROM session_files
        WHERE session_id = ? AND kind = 'log' AND rel_path = ?
        ORDER BY session_file_id
        """,
        (session_id, rel_path),
    ).fetchall()
    return rows[0] if len(rows) == 1 else None


def get_runtime_context(
    conn: sqlite3.Connection,
    session_id: int,
) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM session_runtime_contexts WHERE session_id = ?",
        (session_id,),
    ).fetchone()


def get_mounted_dlcs(
    conn: sqlite3.Connection,
    session_id: int,
) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT * FROM session_mounted_dlcs
        WHERE session_id = ?
        ORDER BY dlc_order
        """,
        (session_id,),
    ).fetchall()


def get_mounted_mods(
    conn: sqlite3.Connection,
    session_id: int,
) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT * FROM session_mounted_mods
        WHERE session_id = ?
        ORDER BY load_order
        """,
        (session_id,),
    ).fetchall()


def replace_runtime_context(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    contract_version: str,
    parsed_at: str,
    status: str,
    debug_log_sha256: str | None,
    source_session_file_id: int | None,
    block_start_line: int | None,
    block_end_line: int | None,
    block_start_byte: int | None,
    block_end_byte: int | None,
    block_sha256: str | None,
    block_candidate_count: int,
    valid_mount_count: int,
    malformed_mount_count: int,
    termination_evidence: str | None,
    absence_reason: str | None,
    mounted_entry_count: int,
    dlcs: Sequence[Any],
    mods: Sequence[Any],
    unknown_mount_count: int,
    inventory_enabled_mod_count: int,
    inventory_dlc_count: int,
    warnings: Sequence[str],
    inventory_warnings: Sequence[str],
) -> None:
    """Atomically replace one session's derived Mounted Data interpretation."""
    if status not in {
        "complete",
        "partial",
        "absent",
        "malformed",
        "truncated",
        "ambiguous",
    }:
        raise ValueError("runtime context status is invalid")
    provenance = (
        block_start_line,
        block_end_line,
        block_start_byte,
        block_end_byte,
        block_sha256,
    )
    if any(value is None for value in provenance) and any(
        value is not None for value in provenance
    ):
        raise ValueError("runtime context block provenance is incomplete")
    if block_candidate_count < 0 or valid_mount_count < 0 or malformed_mount_count < 0:
        raise ValueError("runtime context block counters must be non-negative")
    if [item.dlc_order for item in dlcs] != list(range(len(dlcs))):
        raise ValueError("DLC ordinals are not contiguous")
    if [item.load_order for item in mods] != list(range(len(mods))):
        raise ValueError("mod load ordinals are not contiguous")
    mount_ordinals = [item.mount_ordinal for item in (*dlcs, *mods)]
    if len(mount_ordinals) != len(set(mount_ordinals)):
        raise ValueError("mounted entry ordinals are not unique")
    if mounted_entry_count != len(dlcs) + len(mods):
        raise ValueError("mounted entry count disagrees with derived rows")
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "DELETE FROM session_mounted_dlcs WHERE session_id = ?",
            (session_id,),
        )
        conn.execute(
            "DELETE FROM session_mounted_mods WHERE session_id = ?",
            (session_id,),
        )
        conn.execute(
            "DELETE FROM session_runtime_contexts WHERE session_id = ?",
            (session_id,),
        )
        conn.execute(
            """
            INSERT INTO session_runtime_contexts (
                session_id, context_contract_version, parsed_at, status,
                debug_log_sha256, source_session_file_id,
                block_start_line, block_end_line, block_start_byte,
                block_end_byte, block_sha256, block_candidate_count,
                valid_mount_count, malformed_mount_count,
                termination_evidence, absence_reason,
                mounted_entry_count, dlc_count, mod_count,
                unknown_mount_count, inventory_enabled_mod_count,
                inventory_dlc_count, warnings_json, inventory_warnings_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                contract_version,
                parsed_at,
                status,
                debug_log_sha256,
                source_session_file_id,
                block_start_line,
                block_end_line,
                block_start_byte,
                block_end_byte,
                block_sha256,
                block_candidate_count,
                valid_mount_count,
                malformed_mount_count,
                termination_evidence,
                absence_reason,
                mounted_entry_count,
                len(dlcs),
                len(mods),
                unknown_mount_count,
                inventory_enabled_mod_count,
                inventory_dlc_count,
                _json(list(warnings)),
                _json(list(inventory_warnings)),
            ),
        )
        conn.executemany(
            """
            INSERT INTO session_mounted_dlcs (
                session_id, mount_ordinal, dlc_order, dlc_key,
                display_name, descriptor_path, mount_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    session_id,
                    item.mount_ordinal,
                    item.dlc_order,
                    item.dlc_key,
                    item.display_name,
                    item.descriptor_path,
                    item.mount_path,
                )
                for item in dlcs
            ],
        )
        conn.executemany(
            """
            INSERT INTO session_mounted_mods (
                session_id, mount_ordinal, load_order, mod_key,
                display_name, descriptor_path, mount_path, source_kind
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    session_id,
                    item.mount_ordinal,
                    item.load_order,
                    item.mod_key,
                    item.display_name,
                    item.descriptor_path,
                    item.mount_path,
                    item.source_kind,
                )
                for item in mods
            ],
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def get_successful_parse_result(
    conn: sqlite3.Connection,
    session_id: int,
) -> ParseResult | None:
    row = get_session(conn, session_id)
    if row is None or row["parse_status"] != "succeeded":
        return None
    counter_columns = {
        "source_blocks": "parse_source_blocks",
        "preamble_blocks": "parse_preamble_blocks",
        "issue_occurrences": "parse_issue_occurrences",
        "issue_clusters": "parse_issue_clusters",
        "unclassified_occurrences": "parse_unclassified_occurrences",
        "multi_issue_blocks": "parse_multi_issue_blocks",
        "silently_dropped_blocks": "parse_silently_dropped_blocks",
    }
    values = {name: row[column] for name, column in counter_columns.items()}
    if row["parser_contract_version"] is None or any(
        value is None for value in values.values()
    ):
        # A partially migrated legacy row cannot masquerade as C1 success.
        return None
    return ParseResult(
        session_id=session_id,
        parser_contract_version=row["parser_contract_version"],
        counters=ParseCounters(**values),
        mutated=False,
    )


def _json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _insert_source_block(
    conn: sqlite3.Connection,
    session_id: int,
    block: SourceBlockRecord,
) -> int:
    conn.execute(
        """
        INSERT OR IGNORE INTO raw_block_contents (
            raw_block_sha256, raw_byte_length, raw_block
        ) VALUES (?, ?, ?)
        """,
        (block.raw_block_sha256, block.raw_byte_length, block.raw_block),
    )
    content = conn.execute(
        """
        SELECT raw_block_pk, raw_byte_length, raw_block
        FROM raw_block_contents
        WHERE raw_block_sha256 = ?
        """,
        (block.raw_block_sha256,),
    ).fetchone()
    if content is None or (
        int(content["raw_byte_length"]) != block.raw_byte_length
        or content["raw_block"] != block.raw_block
    ):
        raise ValueError("raw-block SHA-256 maps to conflicting content")
    cursor = conn.execute(
        """
        INSERT INTO source_blocks (
            session_id, log_relpath, start_line, end_line, timestamp, level,
            source_tag, source_family, raw_block_pk, issue_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            block.log_relpath,
            block.start_line,
            block.end_line,
            block.timestamp,
            block.level,
            block.source_tag,
            block.source_family,
            int(content["raw_block_pk"]),
            block.issue_count,
        ),
    )
    assert cursor.lastrowid is not None
    return int(cursor.lastrowid)


def _upsert_cluster_occurrence(
    conn: sqlite3.Connection,
    session_id: int,
    issue: NormalizedIssue,
) -> None:
    """Retain the first representative and increment one signature count."""
    conn.execute(
        """
        INSERT INTO issues (
            session_id, signature, category, error_type, tags_json,
            engine_source, severity, confidence, message_template,
            sample_message, primary_file, primary_line,
            referenced_symbols_json, referenced_objects_json, extra_json,
            occurrence_count, log_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, 'error')
        ON CONFLICT(session_id, signature) DO UPDATE SET
            occurrence_count = issues.occurrence_count + 1
        """,
        (
            session_id,
            issue.signature,
            issue.category,
            issue.error_type,
            _json(issue.tags),
            issue.engine_source,
            issue.severity,
            issue.confidence,
            issue.message_template,
            issue.sample_message,
            issue.primary_file,
            issue.primary_line,
            _json(issue.referenced_symbols),
            _json(issue.referenced_objects),
            _json(issue.extra_json),
        ),
    )


def _insert_occurrence(
    conn: sqlite3.Connection,
    session_id: int,
    occurrence: OccurrenceRecord,
    source_block_pk: int,
) -> None:
    issue = occurrence.issue
    conn.execute(
        """
        INSERT INTO issue_occurrences (
            session_id, signature, source_block_pk, issue_ordinal,
            log_relpath, line_number, occurrence_count,
            referenced_symbols_json, extra_json, log_type
        ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, 'error')
        """,
        (
            session_id,
            issue.signature,
            source_block_pk,
            occurrence.issue_ordinal,
            issue.log_relpath,
            issue.line_number,
            _json(issue.referenced_symbols),
            _json(issue.extra_json),
        ),
    )


def _validate_canonical_replacement(
    blocks: Sequence[SourceBlockRecord],
    occurrences: Sequence[OccurrenceRecord],
    clusters: Sequence[ClusterRecord],
    counters: ParseCounters,
) -> None:
    if counters.silently_dropped_blocks != 0:
        raise ValueError("C1 forbids silently dropped blocks")
    if len(blocks) != counters.source_blocks:
        raise ValueError("source-block counter does not match prepared rows")
    if len(occurrences) != counters.issue_occurrences:
        raise ValueError("occurrence counter does not match prepared rows")
    if len(clusters) != counters.issue_clusters:
        raise ValueError("cluster counter does not match prepared rows")
    if sum(block.issue_count for block in blocks) != len(occurrences):
        raise ValueError("source-block issue totals do not reconcile")
    if sum(cluster.occurrence_count for cluster in clusters) != len(occurrences):
        raise ValueError("cluster occurrence totals do not reconcile")
    if sum(
        occurrence.issue.category == "unclassified"
        for occurrence in occurrences
    ) != counters.unclassified_occurrences:
        raise ValueError("unclassified occurrence counter does not reconcile")
    if sum(block.issue_count > 1 for block in blocks) != counters.multi_issue_blocks:
        raise ValueError("multi-issue block counter does not reconcile")
    block_ids = {block.source_block_id for block in blocks}
    if len(block_ids) != len(blocks):
        raise ValueError("duplicate source_block_id in prepared rows")
    occurrence_keys = {
        (occurrence.source_block_id, occurrence.issue_ordinal)
        for occurrence in occurrences
    }
    if len(occurrence_keys) != len(occurrences):
        raise ValueError("duplicate source-block issue ordinal")
    if any(
        occurrence.source_block_id not in block_ids for occurrence in occurrences
    ):
        raise ValueError("occurrence references an unknown source block")
    occurrences_by_block: dict[str, list[OccurrenceRecord]] = defaultdict(list)
    for occurrence in occurrences:
        occurrences_by_block[occurrence.source_block_id].append(occurrence)
    for block in blocks:
        linked = occurrences_by_block[block.source_block_id]
        if len(linked) != block.issue_count:
            raise ValueError("source-block issue count does not match linked rows")
        if sorted(item.issue_ordinal for item in linked) != list(
            range(block.issue_count)
        ):
            raise ValueError("source-block issue ordinals are not contiguous")
        if any(
            item.issue.log_relpath != block.log_relpath
            or item.issue.line_number != block.start_line
            for item in linked
        ):
            raise ValueError("occurrence provenance disagrees with source block")
    cluster_counts = Counter(
        occurrence.issue.signature for occurrence in occurrences
    )
    if len({cluster.issue.signature for cluster in clusters}) != len(clusters):
        raise ValueError("duplicate signature in prepared clusters")
    if {
        cluster.issue.signature: cluster.occurrence_count for cluster in clusters
    } != dict(cluster_counts):
        raise ValueError("cluster counts do not match occurrence signatures")


def begin_canonical_replacement(
    conn: sqlite3.Connection,
    session_id: int,
    *,
    event_sink: ProjectionEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> None:
    """Begin an atomic streaming replacement of one session's parse rows."""
    _repository_stage(
        "parse_begin_immediate",
        lambda: conn.execute("BEGIN IMMEDIATE"),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    # A successful reparse invalidates every derived classification. Keeping
    # this deletion in the same transaction means a failed reparse restores
    # both the prior canonical rows and their prior classification.
    _repository_stage(
        "parse_delete_classification",
        lambda: conn.execute(
            "DELETE FROM classification_runs WHERE session_id = ?", (session_id,)
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    _repository_stage(
        "parse_delete_occurrences",
        lambda: conn.execute(
            "DELETE FROM issue_occurrences WHERE session_id = ?", (session_id,)
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    _repository_stage(
        "parse_delete_source_blocks",
        lambda: conn.execute(
            "DELETE FROM source_blocks WHERE session_id = ?", (session_id,)
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    _repository_stage(
        "parse_delete_issues",
        lambda: conn.execute(
            "DELETE FROM issues WHERE session_id = ?", (session_id,)
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )


def append_canonical_block(
    conn: sqlite3.Connection,
    session_id: int,
    block: SourceBlockRecord,
    occurrences: Sequence[OccurrenceRecord],
) -> None:
    """Persist one prepared block while bounding Python memory to that block."""
    if block.issue_count < 1 or block.issue_count != len(occurrences):
        raise ValueError("source-block issue count does not match linked rows")
    if [item.issue_ordinal for item in occurrences] != list(range(block.issue_count)):
        raise ValueError("source-block issue ordinals are not contiguous")
    if any(item.source_block_id != block.source_block_id for item in occurrences):
        raise ValueError("occurrence references a different source block")
    if any(
        item.issue.log_relpath != block.log_relpath
        or item.issue.line_number != block.start_line
        for item in occurrences
    ):
        raise ValueError("occurrence provenance disagrees with source block")

    source_block_pk = _insert_source_block(conn, session_id, block)
    for occurrence in occurrences:
        _upsert_cluster_occurrence(conn, session_id, occurrence.issue)
        _insert_occurrence(conn, session_id, occurrence, source_block_pk)


def count_canonical_clusters(conn: sqlite3.Connection, session_id: int) -> int:
    """Count the distinct signatures staged in the current transaction."""
    return int(
        conn.execute(
            "SELECT COUNT(*) FROM issues WHERE session_id = ?", (session_id,)
        ).fetchone()[0]
    )


def _postvalidate_canonical_replacement(
    conn: sqlite3.Connection,
    session_id: int,
    counters: ParseCounters,
) -> None:
    """Prove persisted cardinality and provenance before marking success."""
    if counters.silently_dropped_blocks != 0:
        raise ValueError("canonical parsing forbids silently dropped blocks")

    totals = conn.execute(
        """
        SELECT
            (SELECT COUNT(*) FROM source_blocks WHERE session_id = ?) AS blocks,
            (SELECT COUNT(*) FROM issue_occurrences WHERE session_id = ?) AS occurrences,
            (SELECT COUNT(*) FROM issues WHERE session_id = ?) AS clusters,
            (SELECT COALESCE(SUM(issue_count), 0)
               FROM source_blocks WHERE session_id = ?) AS block_issue_sum,
            (SELECT COALESCE(SUM(occurrence_count), 0)
               FROM issues WHERE session_id = ?) AS cluster_occurrence_sum,
            (SELECT COUNT(*) FROM source_blocks
              WHERE session_id = ? AND issue_count > 1) AS multi_issue_blocks,
            (SELECT COUNT(*)
               FROM issue_occurrences io
               JOIN issues i
                 ON i.session_id = io.session_id AND i.signature = io.signature
              WHERE io.session_id = ? AND i.category = 'unclassified')
              AS unclassified_occurrences
        """,
        (session_id,) * 7,
    ).fetchone()
    expected = (
        counters.source_blocks,
        counters.issue_occurrences,
        counters.issue_clusters,
        counters.issue_occurrences,
        counters.issue_occurrences,
        counters.multi_issue_blocks,
        counters.unclassified_occurrences,
    )
    actual = tuple(int(value) for value in totals)
    if actual != expected:
        raise ValueError(
            f"persisted canonical totals disagree: expected={expected}, actual={actual}"
        )

    invalid_blocks = int(
        conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT sb.source_block_pk
                FROM source_blocks sb
                LEFT JOIN issue_occurrences io
                  ON io.session_id = sb.session_id
                 AND io.source_block_pk = sb.source_block_pk
                WHERE sb.session_id = ?
                GROUP BY sb.source_block_pk, sb.issue_count
                HAVING COUNT(io.issue_occurrence_id) != sb.issue_count
                    OR MIN(io.issue_ordinal) != 0
                    OR MAX(io.issue_ordinal) != sb.issue_count - 1
            )
            """,
            (session_id,),
        ).fetchone()[0]
    )
    invalid_clusters = int(
        conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT i.issue_id
                FROM issues i
                LEFT JOIN issue_occurrences io
                  ON io.session_id = i.session_id AND io.signature = i.signature
                WHERE i.session_id = ?
                GROUP BY i.issue_id, i.occurrence_count
                HAVING COUNT(io.issue_occurrence_id) != i.occurrence_count
            )
            """,
            (session_id,),
        ).fetchone()[0]
    )
    invalid_provenance = int(
        conn.execute(
            """
            SELECT COUNT(*)
            FROM issue_occurrences io
            LEFT JOIN source_blocks sb
              ON sb.source_block_pk = io.source_block_pk
             AND sb.session_id = io.session_id
            LEFT JOIN issues i
              ON i.session_id = io.session_id AND i.signature = io.signature
            WHERE io.session_id = ?
              AND (
                  sb.source_block_pk IS NULL OR i.issue_id IS NULL
                  OR io.log_relpath != sb.log_relpath
                  OR io.line_number != sb.start_line
              )
            """,
            (session_id,),
        ).fetchone()[0]
    )
    if invalid_blocks or invalid_clusters or invalid_provenance:
        raise ValueError(
            "persisted canonical distribution disagrees: "
            f"blocks={invalid_blocks}, clusters={invalid_clusters}, "
            f"provenance={invalid_provenance}"
        )


def finish_canonical_replacement(
    conn: sqlite3.Connection,
    session_id: int,
    counters: ParseCounters,
    parser_contract_version: str,
    *,
    event_sink: ProjectionEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> None:
    """Postvalidate, mark success last, and commit a streaming replacement."""
    _repository_stage(
        "parse_postvalidate",
        lambda: _postvalidate_canonical_replacement(conn, session_id, counters),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    updated = _repository_stage(
        "parse_mark_succeeded",
        lambda: conn.execute(
            """
            UPDATE sessions
            SET parse_status = 'succeeded',
                parser_contract_version = ?,
                parse_source_blocks = ?,
                parse_preamble_blocks = ?,
                parse_issue_occurrences = ?,
                parse_issue_clusters = ?,
                parse_unclassified_occurrences = ?,
                parse_multi_issue_blocks = ?,
                parse_silently_dropped_blocks = ?
            WHERE session_id = ?
            """,
            (
                parser_contract_version,
                counters.source_blocks,
                counters.preamble_blocks,
                counters.issue_occurrences,
                counters.issue_clusters,
                counters.unclassified_occurrences,
                counters.multi_issue_blocks,
                counters.silently_dropped_blocks,
                session_id,
            ),
        ),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
        completion_fields=lambda cursor: {"rowcount": cursor.rowcount},
    )
    if updated.rowcount != 1:
        raise ValueError(f"session_id {session_id} disappeared during parse")
    _repository_stage(
        "parse_commit",
        conn.commit,
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )


def replace_canonical_parse(
    conn: sqlite3.Connection,
    session_id: int,
    blocks: Sequence[SourceBlockRecord],
    occurrences: Sequence[OccurrenceRecord],
    clusters: Sequence[ClusterRecord],
    counters: ParseCounters,
    parser_contract_version: str,
) -> None:
    """Compatibility adapter for callers that already prepared complete lists."""
    _validate_canonical_replacement(blocks, occurrences, clusters, counters)
    occurrences_by_block: dict[str, list[OccurrenceRecord]] = defaultdict(list)
    for occurrence in occurrences:
        occurrences_by_block[occurrence.source_block_id].append(occurrence)
    try:
        begin_canonical_replacement(conn, session_id)
        for block in blocks:
            append_canonical_block(
                conn,
                session_id,
                block,
                occurrences_by_block[block.source_block_id],
            )
        finish_canonical_replacement(
            conn, session_id, counters, parser_contract_version
        )
    except Exception:
        conn.rollback()
        raise


def get_classification_run(
    conn: sqlite3.Connection, session_id: int, model_sha256: str
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT *
        FROM classification_runs
        WHERE session_id = ? AND model_sha256 = ?
        """,
        (session_id, model_sha256),
    ).fetchone()


def get_classification_source_blocks(
    conn: sqlite3.Connection, session_id: int
) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT sb.source_block_pk, sb.source_family, sb.raw_block_pk,
               rb.raw_block, sb.start_line
        FROM source_blocks sb
        JOIN raw_block_contents rb
          ON rb.raw_block_pk = sb.raw_block_pk
        WHERE sb.session_id = ?
        ORDER BY sb.start_line, sb.source_block_pk
        """,
        (session_id,),
    ).fetchall()


def _validate_classification_replacement(
    assignments: Sequence[Any], counts: dict[str, int]
) -> None:
    required = {
        "source_blocks",
        "semantic_occurrences",
        "full",
        "l1_l2",
        "l1",
        "unknown",
    }
    if set(counts) != required or any(
        not isinstance(value, int) or value < 0 for value in counts.values()
    ):
        raise ValueError("classification counters are invalid")
    if counts["semantic_occurrences"] != len(assignments):
        raise ValueError("classification occurrence counter does not reconcile")
    levels = Counter(item.result.assignment_level for item in assignments)
    if any(level not in {"full", "l1_l2", "l1", "unknown"} for level in levels):
        raise ValueError("classification assignment level is invalid")
    for level in ("full", "l1_l2", "l1", "unknown"):
        if levels[level] != counts[level]:
            raise ValueError(f"classification {level} counter does not reconcile")

    by_block: dict[int, list[int]] = defaultdict(list)
    for item in assignments:
        by_block[item.source_block_pk].append(item.unit_ordinal)
        has_contract = item.result.contract_id is not None
        if has_contract != (item.result.assignment_level in {"full", "l1_l2"}):
            raise ValueError("classification contract ID disagrees with assignment level")
    if len(by_block) != counts["source_blocks"]:
        raise ValueError("classification source-block counter does not reconcile")
    for ordinals in by_block.values():
        if sorted(ordinals) != list(range(len(ordinals))):
            raise ValueError("classification unit ordinals are not contiguous")


def _ensure_classification_model(conn: sqlite3.Connection, model: Any) -> None:
    registered_at = datetime.now(timezone.utc).isoformat()
    registered = conn.execute(
        "SELECT * FROM classification_models WHERE model_sha256 = ?",
        (model.sha256,),
    ).fetchone()
    expected_model = (
        model.revision_id,
        model.schema_version,
        model.normalizer_version,
        model.clusterer_version,
        float(model.threshold),
        len(model.clusters),
    )
    if registered is None:
        conn.execute(
            """
            INSERT INTO classification_models (
                model_sha256, revision_id, schema_version,
                normalizer_version, clusterer_version, threshold,
                cluster_count, registered_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (model.sha256, *expected_model, registered_at),
        )
    else:
        actual_model = (
            registered["revision_id"],
            registered["schema_version"],
            registered["normalizer_version"],
            registered["clusterer_version"],
            float(registered["threshold"]),
            registered["cluster_count"],
        )
        if actual_model != expected_model:
            raise ValueError("registered classification model metadata disagrees")

    expected_ids = {cluster.cluster_id for cluster in model.clusters}
    registered_ids = {
        row[0]
        for row in conn.execute(
            "SELECT contract_id FROM classification_contracts WHERE model_sha256 = ?",
            (model.sha256,),
        ).fetchall()
    }
    if registered_ids - expected_ids:
        raise ValueError("registered classification contracts disagree with model")
    missing = [
        cluster for cluster in model.clusters if cluster.cluster_id not in registered_ids
    ]
    conn.executemany(
        """
        INSERT INTO classification_contracts (
            model_sha256, contract_id, source_family, template,
            l1_template, l2_template, support_occurrences,
            support_evidence_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                model.sha256,
                cluster.cluster_id,
                cluster.source_family,
                cluster.template,
                cluster.layers.l1_template if cluster.layers else None,
                cluster.layers.l2_template if cluster.layers else None,
                cluster.support_occurrences,
                cluster.support_evidence_count,
            )
            for cluster in missing
        ],
    )

    rows = conn.execute(
        """
        SELECT contract_id, source_family, template, l1_template, l2_template,
               support_occurrences, support_evidence_count
        FROM classification_contracts
        WHERE model_sha256 = ?
        """,
        (model.sha256,),
    ).fetchall()
    actual = {
        row["contract_id"]: (
            row["source_family"],
            row["template"],
            row["l1_template"],
            row["l2_template"],
            row["support_occurrences"],
            row["support_evidence_count"],
        )
        for row in rows
    }
    expected = {
        cluster.cluster_id: (
            cluster.source_family,
            cluster.template,
            cluster.layers.l1_template if cluster.layers else None,
            cluster.layers.l2_template if cluster.layers else None,
            cluster.support_occurrences,
            cluster.support_evidence_count,
        )
        for cluster in model.clusters
    }
    if actual != expected:
        raise ValueError("registered classification contract metadata disagrees")


def ensure_classification_model(conn: sqlite3.Connection, model: Any) -> None:
    """Idempotently register exact model metadata and its compact contract catalog."""
    try:
        conn.execute("BEGIN IMMEDIATE")
        _ensure_classification_model(conn, model)
        conn.commit()
    except BaseException:
        conn.rollback()
        raise


def replace_classification_run(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    model: Any,
    assignments: Sequence[Any],
    counts: dict[str, int],
    classification_contract_version: str,
    event_sink: ProjectionEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> int:
    """Atomically replace one session/model classification projection."""
    _repository_stage(
        "classification_validate_prepared",
        lambda: _validate_classification_replacement(assignments, counts),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    registered_at = datetime.now(timezone.utc).isoformat()
    transaction_started_ns = monotonic_ns()
    if event_sink is not None:
        event_sink(
            "stage_started",
            {
                "stage": "classification_transaction",
                "session_id": session_id,
                "assignment_count": len(assignments),
            },
        )
    try:
        _repository_stage(
            "classification_begin_immediate",
            lambda: conn.execute("BEGIN IMMEDIATE"),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        _repository_stage(
            "classification_register_model",
            lambda: _ensure_classification_model(conn, model),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )

        _repository_stage(
            "classification_delete_previous",
            lambda: conn.execute(
                "DELETE FROM classification_runs "
                "WHERE session_id = ? AND model_sha256 = ?",
                (session_id, model.sha256),
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        cursor = _repository_stage(
            "classification_insert_lineage",
            lambda: conn.execute(
                """
                INSERT INTO classification_runs (
                    session_id, model_sha256, classification_contract_version,
                    classified_at, source_block_count, semantic_occurrence_count,
                    full_count, l1_l2_count, l1_count, unknown_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    session_id,
                    model.sha256,
                    classification_contract_version,
                    registered_at,
                    counts["source_blocks"],
                    counts["semantic_occurrences"],
                    counts["full"],
                    counts["l1_l2"],
                    counts["l1"],
                    counts["unknown"],
                ),
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        assert cursor.lastrowid is not None
        run_id = int(cursor.lastrowid)
        prepared_payloads: list[tuple[Any, str, tuple[Any, ...]]] = []
        unique_payloads: dict[str, tuple[Any, ...]] = {}
        payload_started_ns = monotonic_ns()
        if event_sink is not None:
            event_sink(
                "stage_started",
                {
                    "stage": "classification_prepare_payloads",
                    "session_id": session_id,
                    "total": len(assignments),
                },
            )
        for index, item in enumerate(assignments, start=1):
            values = (
                model.sha256,
                item.result.source_family,
                item.result.assignment_level,
                item.result.contract_id,
                float(item.result.confidence),
                item.result.semantic_text,
                item.result.location_evidence,
                _json(item.result.normalized_tokens),
                item.result.l1_template,
                item.result.l2_template,
                _json(item.result.structured_slots),
            )
            digest = payload_sha256(values)
            previous = unique_payloads.setdefault(digest, values)
            if previous != values:
                raise ValueError("classification payload SHA-256 collision")
            prepared_payloads.append((item, digest, values))
            if event_sink is not None and index % 10_000 == 0:
                event_sink(
                    "stage_progress",
                    {
                        "stage": "classification_prepare_payloads",
                        "session_id": session_id,
                        "completed": index,
                        "total": len(assignments),
                        "unique_payloads": len(unique_payloads),
                        "duration_ms": round(
                            (monotonic_ns() - payload_started_ns) / 1_000_000,
                            3,
                        ),
                    },
                )
        if event_sink is not None:
            event_sink(
                "stage_completed",
                {
                    "stage": "classification_prepare_payloads",
                    "session_id": session_id,
                    "completed": len(assignments),
                    "unique_payloads": len(unique_payloads),
                    "duration_ms": round(
                        (monotonic_ns() - payload_started_ns) / 1_000_000, 3
                    ),
                },
            )
        _repository_stage(
            "classification_insert_payloads",
            lambda: conn.executemany(
                """
                INSERT OR IGNORE INTO classification_payloads (
                    payload_sha256, model_sha256, source_family,
                    assignment_level, contract_id, confidence, semantic_text,
                    location_evidence, normalized_tokens_json, l1_template,
                    l2_template, structured_slots_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [(digest, *values) for digest, values in unique_payloads.items()],
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda _cursor: {
                "unique_payloads": len(unique_payloads)
            },
        )
        payload_rows = _repository_stage(
            "classification_load_payloads",
            lambda: conn.execute(
                """
                SELECT payload_pk, payload_sha256, model_sha256, source_family,
                       assignment_level, contract_id, confidence, semantic_text,
                       location_evidence, normalized_tokens_json, l1_template,
                       l2_template, structured_slots_json
                FROM classification_payloads
                WHERE model_sha256 = ?
                """,
                (model.sha256,),
            ).fetchall(),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda rows: {"payload_rows": len(rows)},
        )
        payload_pks: dict[str, int] = {}
        for row in payload_rows:
            values = tuple(row[column] for column in (
                "model_sha256", "source_family", "assignment_level",
                "contract_id", "confidence", "semantic_text",
                "location_evidence", "normalized_tokens_json", "l1_template",
                "l2_template", "structured_slots_json",
            ))
            digest = str(row["payload_sha256"])
            if digest in unique_payloads and unique_payloads[digest] != values:
                raise ValueError("stored classification payload disagrees with hash")
            payload_pks[digest] = int(row["payload_pk"])
        if any(digest not in payload_pks for digest in unique_payloads):
            raise ValueError("classification payload registration is incomplete")
        _repository_stage(
            "classification_insert_assignments",
            lambda: conn.executemany(
                """
                INSERT INTO classification_assignments (
                    run_id, session_id, source_block_pk, unit_ordinal,
                    payload_pk
                ) VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        run_id,
                        session_id,
                        item.source_block_pk,
                        item.unit_ordinal,
                        payload_pks[digest],
                    )
                    for item, digest, _values in prepared_payloads
                ],
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda _cursor: {
                "assignment_count": len(prepared_payloads)
            },
        )
        _repository_stage(
            "classification_commit",
            conn.commit,
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        if event_sink is not None:
            event_sink(
                "stage_completed",
                {
                    "stage": "classification_transaction",
                    "session_id": session_id,
                    "classification_run_id": run_id,
                    "duration_ms": round(
                        (monotonic_ns() - transaction_started_ns) / 1_000_000,
                        3,
                    ),
                },
            )
        return run_id
    except BaseException as exc:
        rollback_started_ns = monotonic_ns()
        was_in_transaction = conn.in_transaction
        try:
            conn.rollback()
        finally:
            if event_sink is not None:
                try:
                    event_sink(
                        "transaction_rolled_back",
                        {
                            "stage": "classification_rollback",
                            "session_id": session_id,
                            "was_in_transaction": was_in_transaction,
                            "duration_ms": round(
                                (monotonic_ns() - rollback_started_ns) / 1_000_000,
                                3,
                            ),
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        },
                    )
                    event_sink(
                        "stage_failed",
                        {
                            "stage": "classification_transaction",
                            "session_id": session_id,
                            "duration_ms": round(
                                (monotonic_ns() - transaction_started_ns)
                                / 1_000_000,
                                3,
                            ),
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        },
                    )
                except Exception:
                    pass
        raise


def get_classification_model(
    conn: sqlite3.Connection, model_sha256: str
) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM classification_models WHERE model_sha256 = ?",
        (model_sha256,),
    ).fetchone()


def get_semantic_projection_run(
    conn: sqlite3.Connection,
    session_id: int,
) -> sqlite3.Row | None:
    """Return the one currently accepted canonical semantic projection."""
    return conn.execute(
        """
        SELECT *
        FROM semantic_projection_runs
        WHERE session_id = ?
        """,
        (session_id,),
    ).fetchone()


def get_semantic_projection_inputs(
    conn: sqlite3.Connection,
    classification_run_id: int,
) -> list[sqlite3.Row]:
    """Return stored classifier assignments joined to immutable lexical blocks."""
    return conn.execute(
        """
        SELECT cr.run_id AS classification_run_id,
               cr.session_id,
               cr.model_sha256 AS run_model_sha256,
               cr.classification_contract_version,
               cm.revision_id AS model_revision_id,
               ca.source_block_pk,
               ca.unit_ordinal,
               cp.model_sha256 AS payload_model_sha256,
               cp.source_family AS classified_source_family,
               cp.assignment_level,
               cp.contract_id,
               cp.confidence,
               cp.semantic_text,
               cp.location_evidence,
               cp.normalized_tokens_json,
               cp.l1_template,
               cp.l2_template,
               cp.structured_slots_json,
               sb.log_relpath,
               sb.start_line,
               sb.end_line,
               sb.timestamp,
               sb.level,
               sb.source_tag,
               sb.source_family AS block_source_family,
               rb.raw_block_sha256,
               rb.raw_byte_length,
               rb.raw_block
        FROM classification_runs cr
        JOIN classification_models cm
          ON cm.model_sha256 = cr.model_sha256
        JOIN classification_assignments ca
          ON ca.run_id = cr.run_id AND ca.session_id = cr.session_id
        JOIN classification_payloads cp
          ON cp.payload_pk = ca.payload_pk
        JOIN source_blocks sb
          ON sb.source_block_pk = ca.source_block_pk
         AND sb.session_id = ca.session_id
        JOIN raw_block_contents rb
          ON rb.raw_block_pk = sb.raw_block_pk
        WHERE cr.run_id = ?
        ORDER BY sb.start_line, sb.source_block_pk, ca.unit_ordinal
        """,
        (classification_run_id,),
    ).fetchall()


def _semantic_projection_counts(
    occurrences: Sequence[Any],
) -> dict[str, int]:
    by_block: dict[int, list[int]] = defaultdict(list)
    signatures: set[str] = set()
    unclassified = 0
    for occurrence in occurrences:
        source_block_pk = int(occurrence.source_block_pk)
        unit_ordinal = int(occurrence.unit_ordinal)
        by_block[source_block_pk].append(unit_ordinal)
        signatures.add(occurrence.issue.signature)
        unclassified += occurrence.issue.category == "unclassified"
    return {
        "source_blocks": len(by_block),
        "semantic_occurrences": len(occurrences),
        "issue_clusters": len(signatures),
        "unclassified_occurrences": unclassified,
        "multi_issue_blocks": sum(len(items) > 1 for items in by_block.values()),
    }


def _validate_semantic_projection_prepared(
    conn: sqlite3.Connection,
    *,
    classification_run: sqlite3.Row,
    occurrences: Sequence[Any],
) -> dict[str, int]:
    counts = _semantic_projection_counts(occurrences)
    expected_keys = {
        (int(row["source_block_pk"]), int(row["unit_ordinal"]))
        for row in conn.execute(
            """
            SELECT source_block_pk, unit_ordinal
            FROM classification_assignments
            WHERE run_id = ? AND session_id = ?
            """,
            (
                int(classification_run["run_id"]),
                int(classification_run["session_id"]),
            ),
        ).fetchall()
    }
    actual_keys = {
        (int(item.source_block_pk), int(item.unit_ordinal))
        for item in occurrences
    }
    if len(actual_keys) != len(occurrences):
        raise ValueError("semantic projection contains duplicate block/unit keys")
    if actual_keys != expected_keys:
        raise ValueError(
            "semantic projection keys do not match stored classification assignments"
        )
    if counts["source_blocks"] != int(classification_run["source_block_count"]):
        raise ValueError("semantic projection source-block count does not reconcile")
    if counts["semantic_occurrences"] != int(
        classification_run["semantic_occurrence_count"]
    ):
        raise ValueError("semantic projection occurrence count does not reconcile")

    by_block: dict[int, list[Any]] = defaultdict(list)
    for occurrence in occurrences:
        by_block[int(occurrence.source_block_pk)].append(occurrence)
    block_rows = conn.execute(
        """
        SELECT source_block_pk, log_relpath, start_line
        FROM source_blocks
        WHERE session_id = ?
        """,
        (int(classification_run["session_id"]),),
    ).fetchall()
    blocks = {int(row["source_block_pk"]): row for row in block_rows}
    if set(by_block) != set(blocks):
        raise ValueError("semantic projection does not cover every source block")
    for source_block_pk, items in by_block.items():
        if sorted(int(item.unit_ordinal) for item in items) != list(range(len(items))):
            raise ValueError("semantic projection unit ordinals are not contiguous")
        block = blocks[source_block_pk]
        if any(
            item.issue.log_relpath != block["log_relpath"]
            or int(item.issue.line_number) != int(block["start_line"])
            for item in items
        ):
            raise ValueError("semantic projection provenance disagrees with source block")
    return counts


def _upsert_projected_cluster_occurrence(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    projection_run_id: int,
    issue: NormalizedIssue,
) -> None:
    conn.execute(
        """
        INSERT INTO issues (
            session_id, signature, category, error_type, tags_json,
            engine_source, severity, confidence, message_template,
            sample_message, primary_file, primary_line,
            referenced_symbols_json, referenced_objects_json, extra_json,
            occurrence_count, log_type, semantic_projection_run_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1,
                  'error', ?)
        ON CONFLICT(session_id, signature) DO UPDATE SET
            occurrence_count = issues.occurrence_count + 1
        """,
        (
            session_id,
            issue.signature,
            issue.category,
            issue.error_type,
            _json(issue.tags),
            issue.engine_source,
            issue.severity,
            issue.confidence,
            issue.message_template,
            issue.sample_message,
            issue.primary_file,
            issue.primary_line,
            _json(issue.referenced_symbols),
            _json(issue.referenced_objects),
            _json(issue.extra_json),
            projection_run_id,
        ),
    )


def _insert_projected_occurrence(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    projection_run_id: int,
    occurrence: Any,
) -> None:
    issue = occurrence.issue
    conn.execute(
        """
        INSERT INTO issue_occurrences (
            session_id, signature, source_block_pk, issue_ordinal,
            log_relpath, line_number, occurrence_count,
            referenced_symbols_json, referenced_objects_json,
            primary_file, primary_line, extra_json, log_type,
            semantic_projection_run_id
        ) VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, 'error', ?)
        """,
        (
            session_id,
            issue.signature,
            int(occurrence.source_block_pk),
            int(occurrence.unit_ordinal),
            issue.log_relpath,
            issue.line_number,
            _json(issue.referenced_symbols),
            _json(issue.referenced_objects),
            issue.primary_file,
            issue.primary_line,
            _json(issue.extra_json),
            projection_run_id,
        ),
    )


def _postvalidate_semantic_projection(
    conn: sqlite3.Connection,
    projection_run_id: int,
    *,
    event_sink: ProjectionEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> None:
    lineage = conn.execute(
        "SELECT * FROM semantic_projection_runs WHERE projection_run_id = ?",
        (projection_run_id,),
    ).fetchone()
    if lineage is None:
        raise ValueError("semantic projection lineage is missing")
    session_id = int(lineage["session_id"])
    classification_run_id = int(lineage["classification_run_id"])
    totals = _repository_stage(
        "projection_postvalidate_totals",
        lambda: conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM source_blocks WHERE session_id = ?) AS blocks,
                (SELECT COUNT(*) FROM issue_occurrences
                  WHERE session_id = ? AND semantic_projection_run_id = ?) AS occurrences,
                (SELECT COUNT(*) FROM issues
                  WHERE session_id = ? AND semantic_projection_run_id = ?) AS clusters,
                (SELECT COALESCE(SUM(issue_count), 0) FROM source_blocks
                  WHERE session_id = ?) AS block_issue_sum,
                (SELECT COALESCE(SUM(occurrence_count), 0) FROM issues
                  WHERE session_id = ? AND semantic_projection_run_id = ?)
                  AS cluster_occurrence_sum,
                (SELECT COUNT(*) FROM source_blocks
                  WHERE session_id = ? AND issue_count > 1) AS multi_issue_blocks,
                (SELECT COUNT(*)
                   FROM issue_occurrences io
                   JOIN issues i
                     ON i.session_id = io.session_id AND i.signature = io.signature
                  WHERE io.session_id = ?
                    AND io.semantic_projection_run_id = ?
                    AND i.category = 'unclassified') AS unclassified_occurrences
            """,
            (
                session_id,
                session_id, projection_run_id,
                session_id, projection_run_id,
                session_id,
                session_id, projection_run_id,
                session_id,
                session_id, projection_run_id,
            ),
        ).fetchone(),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    expected = (
        int(lineage["source_block_count"]),
        int(lineage["semantic_occurrence_count"]),
        int(lineage["issue_cluster_count"]),
        int(lineage["semantic_occurrence_count"]),
        int(lineage["semantic_occurrence_count"]),
        int(lineage["multi_issue_block_count"]),
        int(lineage["unclassified_occurrence_count"]),
    )
    actual = tuple(int(value) for value in totals)
    if actual != expected:
        raise ValueError(
            "persisted semantic projection totals disagree: "
            f"expected={expected}, actual={actual}"
        )

    invalid_blocks = int(
        _repository_stage(
            "projection_postvalidate_blocks",
            lambda: conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT sb.source_block_pk
                FROM source_blocks sb
                LEFT JOIN issue_occurrences io
                  ON io.session_id = sb.session_id
                 AND io.source_block_pk = sb.source_block_pk
                 AND io.semantic_projection_run_id = ?
                WHERE sb.session_id = ?
                GROUP BY sb.source_block_pk, sb.issue_count
                HAVING COUNT(io.issue_occurrence_id) != sb.issue_count
                    OR MIN(io.issue_ordinal) != 0
                    OR MAX(io.issue_ordinal) != sb.issue_count - 1
            )
            """,
                (projection_run_id, session_id),
            ).fetchone()[0],
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
    )
    invalid_clusters = int(
        _repository_stage(
            "projection_postvalidate_clusters",
            lambda: conn.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT i.issue_id
                FROM issues i
                LEFT JOIN issue_occurrences io
                  ON io.session_id = i.session_id
                 AND io.signature = i.signature
                 AND io.semantic_projection_run_id = i.semantic_projection_run_id
                WHERE i.session_id = ?
                  AND i.semantic_projection_run_id = ?
                GROUP BY i.issue_id, i.occurrence_count
                HAVING COUNT(io.issue_occurrence_id) != i.occurrence_count
            )
            """,
                (session_id, projection_run_id),
            ).fetchone()[0],
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
    )
    invalid_provenance = int(
        _repository_stage(
            "projection_postvalidate_provenance",
            lambda: conn.execute(
            """
            SELECT COUNT(*)
            FROM issue_occurrences io
            LEFT JOIN source_blocks sb
              ON sb.source_block_pk = io.source_block_pk
             AND sb.session_id = io.session_id
            LEFT JOIN issues i
              ON i.session_id = io.session_id AND i.signature = io.signature
            WHERE io.session_id = ?
              AND io.semantic_projection_run_id = ?
              AND (
                  sb.source_block_pk IS NULL OR i.issue_id IS NULL
                  OR i.semantic_projection_run_id != io.semantic_projection_run_id
                  OR io.log_relpath != sb.log_relpath
                  OR io.line_number != sb.start_line
              )
            """,
                (session_id, projection_run_id),
            ).fetchone()[0],
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
    )
    unmatched_occurrences = int(
        _repository_stage(
            "projection_postvalidate_unmatched",
            lambda: conn.execute(
            """
            SELECT COUNT(*)
            FROM issue_occurrences io
            LEFT JOIN classification_assignments ca
              ON ca.run_id = ?
             AND ca.session_id = io.session_id
             AND ca.source_block_pk = io.source_block_pk
             AND ca.unit_ordinal = io.issue_ordinal
            WHERE io.session_id = ?
              AND io.semantic_projection_run_id = ?
              AND ca.classification_assignment_id IS NULL
            """,
                (classification_run_id, session_id, projection_run_id),
            ).fetchone()[0],
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
    )
    missing_occurrences = int(
        _repository_stage(
            "projection_postvalidate_missing",
            lambda: conn.execute(
            """
            SELECT COUNT(*)
            FROM classification_assignments ca
            LEFT JOIN issue_occurrences io
              ON io.session_id = ca.session_id
             AND io.source_block_pk = ca.source_block_pk
             AND io.issue_ordinal = ca.unit_ordinal
             AND io.semantic_projection_run_id = ?
            WHERE ca.run_id = ? AND ca.session_id = ?
              AND io.issue_occurrence_id IS NULL
            """,
                (projection_run_id, classification_run_id, session_id),
            ).fetchone()[0],
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
    )
    session_counts = _repository_stage(
        "projection_postvalidate_session",
        lambda: conn.execute(
            """
            SELECT parse_source_blocks, parse_issue_occurrences,
                   parse_issue_clusters, parse_unclassified_occurrences,
                   parse_multi_issue_blocks
            FROM sessions WHERE session_id = ?
            """,
            (session_id,),
        ).fetchone(),
        session_id=session_id,
        event_sink=event_sink,
        monotonic_ns=monotonic_ns,
    )
    expected_session = (
        int(lineage["source_block_count"]),
        int(lineage["semantic_occurrence_count"]),
        int(lineage["issue_cluster_count"]),
        int(lineage["unclassified_occurrence_count"]),
        int(lineage["multi_issue_block_count"]),
    )
    actual_session = tuple(int(value) for value in session_counts)
    if (
        invalid_blocks
        or invalid_clusters
        or invalid_provenance
        or unmatched_occurrences
        or missing_occurrences
        or actual_session != expected_session
    ):
        raise ValueError(
            "persisted semantic projection distribution disagrees: "
            f"blocks={invalid_blocks}, clusters={invalid_clusters}, "
            f"provenance={invalid_provenance}, unmatched={unmatched_occurrences}, "
            f"missing={missing_occurrences}, session_counts="
            f"{actual_session != expected_session}"
        )


def validate_semantic_projection(
    conn: sqlite3.Connection,
    projection_run_id: int,
) -> None:
    """Revalidate a previously accepted projection without mutating storage."""
    _postvalidate_semantic_projection(conn, projection_run_id)


def replace_semantic_projection(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    classification_run_id: int,
    model_sha256: str,
    projection_catalog_sha256: str,
    projection_catalog_revision_id: str,
    projection_catalog_schema_version: int,
    projection_contract_version: str,
    occurrences: Sequence[Any],
    event_sink: ProjectionEventSink | None = None,
    monotonic_ns: Callable[[], int] = time.perf_counter_ns,
) -> int:
    """Atomically replace canonical issues from one stored classification run."""
    projected_at = datetime.now(timezone.utc).isoformat()
    transaction_started_ns = monotonic_ns()
    if event_sink is not None:
        event_sink(
            "stage_started",
            {
                "stage": "projection_transaction",
                "session_id": session_id,
                "occurrence_count": len(occurrences),
            },
        )
    try:
        _repository_stage(
            "projection_begin_immediate",
            lambda: conn.execute("BEGIN IMMEDIATE"),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        classification_run = _repository_stage(
            "projection_transaction_precondition",
            lambda: conn.execute(
                """
                SELECT * FROM classification_runs
                WHERE run_id = ? AND session_id = ?
                """,
                (classification_run_id, session_id),
            ).fetchone(),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        if classification_run is None:
            raise ValueError("classification run does not exist for session")
        if classification_run["model_sha256"] != model_sha256:
            raise ValueError("classification run model disagrees with projection")
        counts = _repository_stage(
            "projection_validate_prepared",
            lambda: _validate_semantic_projection_prepared(
                conn,
                classification_run=classification_run,
                occurrences=occurrences,
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda result: dict(result),
        )

        # Canonical issues are one current semantic view per session. Deleting
        # the old lineage cascades its rows; explicit deletes also remove legacy
        # parser rows whose projection lineage predates this schema.
        def delete_previous() -> None:
            conn.execute(
                "DELETE FROM semantic_projection_runs WHERE session_id = ?",
                (session_id,),
            )
            conn.execute(
                "DELETE FROM issue_occurrences WHERE session_id = ?", (session_id,)
            )
            conn.execute("DELETE FROM issues WHERE session_id = ?", (session_id,))

        _repository_stage(
            "projection_delete_previous",
            delete_previous,
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        cursor = _repository_stage(
            "projection_insert_lineage",
            lambda: conn.execute(
                """
                INSERT INTO semantic_projection_runs (
                    classification_run_id, session_id, model_sha256,
                    projection_catalog_sha256, projection_catalog_revision_id,
                    projection_catalog_schema_version, projection_contract_version,
                    projected_at, source_block_count, semantic_occurrence_count,
                    issue_cluster_count, unclassified_occurrence_count,
                    multi_issue_block_count
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    classification_run_id,
                    session_id,
                    model_sha256,
                    projection_catalog_sha256,
                    projection_catalog_revision_id,
                    projection_catalog_schema_version,
                    projection_contract_version,
                    projected_at,
                    counts["source_blocks"],
                    counts["semantic_occurrences"],
                    counts["issue_clusters"],
                    counts["unclassified_occurrences"],
                    counts["multi_issue_blocks"],
                ),
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        assert cursor.lastrowid is not None
        projection_run_id = int(cursor.lastrowid)

        by_block = Counter(int(item.source_block_pk) for item in occurrences)
        _repository_stage(
            "projection_update_blocks",
            lambda: conn.executemany(
                "UPDATE source_blocks SET issue_count = ? "
                "WHERE session_id = ? AND source_block_pk = ?",
                [
                    (count, session_id, source_block_pk)
                    for source_block_pk, count in by_block.items()
                ],
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda _cursor: {"block_count": len(by_block)},
        )
        write_loop_started_ns = monotonic_ns()
        cluster_write_ns = 0
        occurrence_write_ns = 0
        if event_sink is not None:
            event_sink(
                "stage_started",
                {
                    "stage": "projection_write_loop",
                    "session_id": session_id,
                    "total": len(occurrences),
                },
            )
        for index, occurrence in enumerate(occurrences, start=1):
            started_ns = monotonic_ns()
            _upsert_projected_cluster_occurrence(
                conn,
                session_id=session_id,
                projection_run_id=projection_run_id,
                issue=occurrence.issue,
            )
            cluster_write_ns += monotonic_ns() - started_ns
            started_ns = monotonic_ns()
            _insert_projected_occurrence(
                conn,
                session_id=session_id,
                projection_run_id=projection_run_id,
                occurrence=occurrence,
            )
            occurrence_write_ns += monotonic_ns() - started_ns
            if event_sink is not None and index % 5_000 == 0:
                elapsed_ms = round(
                    (monotonic_ns() - write_loop_started_ns) / 1_000_000, 3
                )
                event_sink(
                    "stage_progress",
                    {
                        "stage": "projection_write_loop",
                        "session_id": session_id,
                        "completed": index,
                        "total": len(occurrences),
                        "duration_ms": elapsed_ms,
                        "cluster_statement_ms": round(
                            cluster_write_ns / 1_000_000, 3
                        ),
                        "occurrence_statement_ms": round(
                            occurrence_write_ns / 1_000_000, 3
                        ),
                        "items_per_second": round(
                            index / (elapsed_ms / 1000), 3
                        ) if elapsed_ms else None,
                    },
                )
        if event_sink is not None:
            event_sink(
                "stage_completed",
                {
                    "stage": "projection_write_loop",
                    "session_id": session_id,
                    "completed": len(occurrences),
                    "duration_ms": round(
                        (monotonic_ns() - write_loop_started_ns) / 1_000_000,
                        3,
                    ),
                    "cluster_statement_ms": round(cluster_write_ns / 1_000_000, 3),
                    "occurrence_statement_ms": round(
                        occurrence_write_ns / 1_000_000, 3
                    ),
                },
            )

        updated = _repository_stage(
            "projection_update_session",
            lambda: conn.execute(
                """
                UPDATE sessions
                SET parse_issue_occurrences = ?,
                    parse_issue_clusters = ?,
                    parse_unclassified_occurrences = ?,
                    parse_multi_issue_blocks = ?
                WHERE session_id = ?
                  AND parse_status = 'succeeded'
                  AND parse_source_blocks = ?
                """,
                (
                    counts["semantic_occurrences"],
                    counts["issue_clusters"],
                    counts["unclassified_occurrences"],
                    counts["multi_issue_blocks"],
                    session_id,
                    counts["source_blocks"],
                ),
            ).rowcount,
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
            completion_fields=lambda rowcount: {"rowcount": rowcount},
        )
        if updated != 1:
            raise ValueError("semantic projection session parse state is stale")
        _repository_stage(
            "projection_postvalidate",
            lambda: _postvalidate_semantic_projection(
                conn,
                projection_run_id,
                event_sink=event_sink,
                monotonic_ns=monotonic_ns,
            ),
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        _repository_stage(
            "projection_commit",
            conn.commit,
            session_id=session_id,
            event_sink=event_sink,
            monotonic_ns=monotonic_ns,
        )
        if event_sink is not None:
            event_sink(
                "stage_completed",
                {
                    "stage": "projection_transaction",
                    "session_id": session_id,
                    "projection_run_id": projection_run_id,
                    "duration_ms": round(
                        (monotonic_ns() - transaction_started_ns) / 1_000_000,
                        3,
                    ),
                },
            )
        return projection_run_id
    except BaseException as exc:
        rollback_started_ns = monotonic_ns()
        was_in_transaction = conn.in_transaction
        try:
            conn.rollback()
        finally:
            if event_sink is not None:
                try:
                    event_sink(
                        "transaction_rolled_back",
                        {
                            "stage": "projection_rollback",
                            "session_id": session_id,
                            "was_in_transaction": was_in_transaction,
                            "duration_ms": round(
                                (monotonic_ns() - rollback_started_ns) / 1_000_000,
                                3,
                            ),
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        },
                    )
                    event_sink(
                        "stage_failed",
                        {
                            "stage": "projection_transaction",
                            "session_id": session_id,
                            "duration_ms": round(
                                (monotonic_ns() - transaction_started_ns)
                                / 1_000_000,
                                3,
                            ),
                            "error_type": type(exc).__name__,
                            "error": str(exc),
                        },
                    )
                except Exception:
                    pass
        raise


def list_classification_review_items(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    model_sha256: str,
    level: str,
    limit: int,
    max_confidence: float | None = None,
) -> list[sqlite3.Row]:
    if level not in {"all", "full", "l1_l2", "l1", "unknown"}:
        raise ValueError("review level is invalid")
    if limit < 1:
        raise ValueError("review limit must be positive")
    if max_confidence is not None and not 0.0 <= max_confidence <= 1.0:
        raise ValueError("review confidence must be between zero and one")
    levels = ("l1", "unknown") if level == "all" else (level,)
    placeholders = ",".join("?" for _ in levels)
    confidence_clause = ""
    confidence_parameters: tuple[float, ...] = ()
    if max_confidence is not None:
        confidence_clause = "AND cp.confidence <= ?"
        confidence_parameters = (max_confidence,)
    return conn.execute(
        f"""
        SELECT cp.assignment_level,
               cp.contract_id,
               cp.confidence,
               cp.source_family,
               cp.l1_template,
               cp.l2_template,
               MIN(cp.semantic_text) AS sample,
               COUNT(*) AS occurrences,
               MIN(sb.start_line) AS first_line
        FROM classification_assignments ca
        JOIN classification_runs cr ON cr.run_id = ca.run_id
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        JOIN source_blocks sb
          ON sb.session_id = ca.session_id
         AND sb.source_block_pk = ca.source_block_pk
        WHERE cr.session_id = ?
          AND cr.model_sha256 = ?
          AND cp.assignment_level IN ({placeholders})
          {confidence_clause}
        GROUP BY cp.assignment_level,
                 cp.contract_id,
                 cp.confidence,
                 cp.source_family,
                 cp.l1_template,
                 cp.l2_template,
                 cp.normalized_tokens_json
        ORDER BY occurrences DESC,
                 cp.source_family,
                 first_line
        LIMIT ?
        """,
        (session_id, model_sha256, *levels, *confidence_parameters, limit),
    ).fetchall()
