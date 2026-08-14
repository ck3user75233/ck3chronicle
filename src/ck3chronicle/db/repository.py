"""Thin data-access layer for ck3chronicle SQLite database."""
from __future__ import annotations

import sqlite3
import json
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .migrations import apply_migrations
from .payloads import payload_sha256
from ..models.parse import (
    ClusterRecord,
    OccurrenceRecord,
    ParseCounters,
    ParseResult,
    SourceBlockRecord,
)


def open_db(path: Path) -> sqlite3.Connection:
    """Open (or create) the ck3chronicle database, applying migrations."""
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        compact_storage_migrated = apply_migrations(conn)
        reclaim_receipt = conn.execute(
            "SELECT version FROM schema_versions WHERE component = ?",
            ("storage_reclaimed",),
        ).fetchone()
        if compact_storage_migrated or reclaim_receipt is None:
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


def get_session_by_hash(
    conn: sqlite3.Connection, evidence_bundle_hash: str
) -> sqlite3.Row | None:
    cur = conn.execute(
        "SELECT * FROM sessions WHERE evidence_bundle_hash = ?",
        (evidence_bundle_hash,),
    )
    return cur.fetchone()


def create_session(
    conn: sqlite3.Connection,
    evidence_bundle_hash: str,
    log_count: int,
    crash_present: bool,
    total_bytes: int,
    forced_duplicate_of: int | None = None,
) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """
        INSERT INTO sessions
            (evidence_bundle_hash, created_at, log_count, crash_present,
             total_bytes, forced_duplicate_of)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            evidence_bundle_hash,
            created_at,
            log_count,
            int(crash_present),
            total_bytes,
            forced_duplicate_of,
        ),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


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


def register_run(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    capture_id: str,
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
    receipt_sha256: str | None = None,
) -> tuple[int, bool]:
    """Idempotently index one game run separately from evidence bytes."""
    timestamp = observed_at or datetime.now(timezone.utc).isoformat()
    ended_at = observed_ended_at or timestamp
    values = (
        session_id,
        capture_id,
        timestamp,
        observed_started_at,
        ended_at,
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
        receipt_sha256,
    )
    try:
        conn.execute("BEGIN IMMEDIATE")
        existing = conn.execute(
            "SELECT * FROM capture_observations WHERE capture_id = ?",
            (capture_id,),
        ).fetchone()
        if existing is not None:
            if int(existing["session_id"]) != session_id:
                raise ValueError("run receipt points to a different evidence bundle")
            if (
                receipt_sha256 is not None
                and existing["receipt_sha256"] not in {None, receipt_sha256}
            ):
                raise ValueError("run receipt hash disagrees with indexed run")
            conn.commit()
            return int(existing["observation_id"]), True
        cur = conn.execute(
            """
            INSERT INTO capture_observations (
                session_id, capture_id, observed_at, observed_started_at,
                observed_ended_at, trigger, process_name, process_pid,
                process_started_ns, termination_kind, crash_folder_name,
                crash_folder_path, crash_detected_at,
                crash_association_method, crash_association_confidence,
                receipt_sha256
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )
        conn.commit()
        assert cur.lastrowid is not None
        return int(cur.lastrowid), False
    except Exception:
        conn.rollback()
        raise


def record_capture_observation(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    trigger: str,
    process_name: str | None = None,
    observed_at: str | None = None,
) -> int:
    """Compatibility wrapper for callers without a durable receipt."""
    run_id, _ = register_run(
        conn,
        session_id=session_id,
        capture_id=f"compat-{uuid.uuid4().hex}",
        trigger=trigger,
        process_name=process_name,
        observed_at=observed_at,
        observed_ended_at=observed_at,
    )
    return run_id


def get_run_by_capture_id(
    conn: sqlite3.Connection, capture_id: str
) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM capture_observations WHERE capture_id = ?", (capture_id,)
    ).fetchone()


def latest_run(
    conn: sqlite3.Connection, *, reportable_only: bool = False
) -> sqlite3.Row | None:
    readiness = """
        AND s.parse_status = 'succeeded'
        AND EXISTS (
            SELECT 1 FROM classification_runs cr
            WHERE cr.session_id = s.session_id
        )
    """ if reportable_only else ""
    return conn.execute(
        f"""
        SELECT co.*
        FROM capture_observations co
        JOIN sessions s ON s.session_id = co.session_id
        WHERE s.capture_status = 'finalized'
        {readiness}
        ORDER BY co.observed_ended_at DESC, co.observation_id DESC
        LIMIT 1
        """
    ).fetchone()


def latest_run_for_session(
    conn: sqlite3.Connection, session_id: int
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT *
        FROM capture_observations
        WHERE session_id = ?
        ORDER BY observed_ended_at DESC, observation_id DESC
        LIMIT 1
        """,
        (session_id,),
    ).fetchone()


def replace_run_file_origins(
    conn: sqlite3.Connection,
    observation_id: int,
    origins: Sequence[Mapping[str, Any]],
) -> None:
    """Atomically replace deterministic file-origin projections for one run."""
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "DELETE FROM run_file_origins WHERE observation_id = ?",
            (observation_id,),
        )
        conn.executemany(
            """
            INSERT INTO run_file_origins (
                observation_id, session_file_id, origin_kind, crash_rel_path,
                crash_sha256, crash_equivalence, preserved_crash_rel_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    observation_id,
                    int(item["session_file_id"]),
                    item["origin_kind"],
                    item.get("crash_rel_path"),
                    item.get("crash_sha256"),
                    item["crash_equivalence"],
                    item.get("preserved_crash_rel_path"),
                )
                for item in origins
            ],
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def get_run_file_origins(
    conn: sqlite3.Connection, observation_id: int
) -> list[sqlite3.Row]:
    return conn.execute(
        """
        SELECT rfo.*, sf.rel_path, sf.sha256 AS archived_sha256, sf.bytes
        FROM run_file_origins rfo
        JOIN session_files sf ON sf.session_file_id = rfo.session_file_id
        WHERE rfo.observation_id = ?
        ORDER BY sf.rel_path
        """,
        (observation_id,),
    ).fetchall()


def list_sessions(
    conn: sqlite3.Connection, limit: int = 100
) -> list[sqlite3.Row]:
    cur = conn.execute(
        "SELECT * FROM sessions ORDER BY created_at DESC, session_id DESC LIMIT ?",
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
    """Return the sole Phase 1 issue-source manifest row, if unambiguous."""
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


def _insert_cluster(
    conn: sqlite3.Connection,
    session_id: int,
    cluster: ClusterRecord,
) -> None:
    issue = cluster.issue
    conn.execute(
        """
        INSERT INTO issues (
            session_id, signature, category, error_type, tags_json,
            engine_source, severity, confidence, message_template,
            sample_message, primary_file, primary_line,
            referenced_symbols_json, referenced_objects_json, extra_json,
            occurrence_count, log_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'error')
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
            cluster.occurrence_count,
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


def replace_canonical_parse(
    conn: sqlite3.Connection,
    session_id: int,
    blocks: Sequence[SourceBlockRecord],
    occurrences: Sequence[OccurrenceRecord],
    clusters: Sequence[ClusterRecord],
    counters: ParseCounters,
    parser_contract_version: str,
) -> None:
    """Atomically replace all C1 rows and mark the session successful last."""
    _validate_canonical_replacement(blocks, occurrences, clusters, counters)
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "DELETE FROM issue_occurrences WHERE session_id = ?", (session_id,)
        )
        conn.execute("DELETE FROM source_blocks WHERE session_id = ?", (session_id,))
        conn.execute("DELETE FROM issues WHERE session_id = ?", (session_id,))

        source_block_pks = {
            block.source_block_id: _insert_source_block(conn, session_id, block)
            for block in blocks
        }
        for cluster in clusters:
            _insert_cluster(conn, session_id, cluster)
        for occurrence in occurrences:
            _insert_occurrence(
                conn,
                session_id,
                occurrence,
                source_block_pks[occurrence.source_block_id],
            )

        updated = conn.execute(
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
        )
        if updated.rowcount != 1:
            raise ValueError(f"session_id {session_id} disappeared during parse")
        conn.commit()
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
        SELECT sb.source_block_pk, sb.source_family, rb.raw_block, sb.start_line
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
    except Exception:
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
) -> int:
    """Atomically replace one session/model classification projection."""
    _validate_classification_replacement(assignments, counts)
    registered_at = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute("BEGIN IMMEDIATE")
        _ensure_classification_model(conn, model)

        conn.execute(
            "DELETE FROM classification_runs WHERE session_id = ? AND model_sha256 = ?",
            (session_id, model.sha256),
        )
        cursor = conn.execute(
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
        )
        assert cursor.lastrowid is not None
        run_id = int(cursor.lastrowid)
        prepared_payloads: list[tuple[Any, str, tuple[Any, ...]]] = []
        unique_payloads: dict[str, tuple[Any, ...]] = {}
        for item in assignments:
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
        conn.executemany(
            """
            INSERT OR IGNORE INTO classification_payloads (
                payload_sha256, model_sha256, source_family,
                assignment_level, contract_id, confidence, semantic_text,
                location_evidence, normalized_tokens_json, l1_template,
                l2_template, structured_slots_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [(digest, *values) for digest, values in unique_payloads.items()],
        )
        payload_rows = conn.execute(
            """
            SELECT payload_pk, payload_sha256, model_sha256, source_family,
                   assignment_level, contract_id, confidence, semantic_text,
                   location_evidence, normalized_tokens_json, l1_template,
                   l2_template, structured_slots_json
            FROM classification_payloads
            WHERE model_sha256 = ?
            """,
            (model.sha256,),
        ).fetchall()
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
        conn.executemany(
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
        )
        conn.commit()
        return run_id
    except Exception:
        conn.rollback()
        raise


def get_classification_model(
    conn: sqlite3.Connection, model_sha256: str
) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM classification_models WHERE model_sha256 = ?",
        (model_sha256,),
    ).fetchone()


def list_classification_review_items(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    model_sha256: str,
    level: str,
    limit: int,
) -> list[sqlite3.Row]:
    if level not in {"all", "l1", "unknown"}:
        raise ValueError("review level is invalid")
    if limit < 1:
        raise ValueError("review limit must be positive")
    levels = ("l1", "unknown") if level == "all" else (level,)
    placeholders = ",".join("?" for _ in levels)
    return conn.execute(
        f"""
        SELECT cp.assignment_level,
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
        GROUP BY cp.assignment_level,
                 cp.source_family,
                 cp.l1_template,
                 cp.l2_template,
                 cp.normalized_tokens_json
        ORDER BY occurrences DESC,
                 cp.source_family,
                 first_line
        LIMIT ?
        """,
        (session_id, model_sha256, *levels, limit),
    ).fetchall()
