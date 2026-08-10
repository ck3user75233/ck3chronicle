"""Thin data-access layer for ck3chronicle SQLite database."""
from __future__ import annotations

import sqlite3
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .migrations import apply_migrations
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
        apply_migrations(conn)
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


def record_capture_observation(
    conn: sqlite3.Connection,
    *,
    session_id: int,
    trigger: str,
    process_name: str | None = None,
    observed_at: str | None = None,
) -> int:
    """Record a run observation separately from deduplicated evidence bytes."""
    timestamp = observed_at or datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """
        INSERT INTO capture_observations (
            session_id, observed_at, trigger, process_name
        ) VALUES (?, ?, ?, ?)
        """,
        (session_id, timestamp, trigger, process_name),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return int(cur.lastrowid)


def list_sessions(
    conn: sqlite3.Connection, limit: int = 100
) -> list[sqlite3.Row]:
    cur = conn.execute(
        "SELECT * FROM sessions ORDER BY session_id DESC LIMIT ?",
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
) -> None:
    conn.execute(
        """
        INSERT INTO source_blocks (
            session_id, source_block_id, log_relpath, start_line, end_line,
            timestamp, level, source_tag, source_family, raw_block_sha256,
            raw_byte_length, raw_block, issue_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            session_id,
            block.source_block_id,
            block.log_relpath,
            block.start_line,
            block.end_line,
            block.timestamp,
            block.level,
            block.source_tag,
            block.source_family,
            block.raw_block_sha256,
            block.raw_byte_length,
            block.raw_block,
            block.issue_count,
        ),
    )


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
) -> None:
    issue = occurrence.issue
    conn.execute(
        """
        INSERT INTO issue_occurrences (
            session_id, signature, source_block_id, issue_ordinal,
            log_relpath, line_number, raw_block, occurrence_count,
            referenced_symbols_json, extra_json, log_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, ?, 'error')
        """,
        (
            session_id,
            issue.signature,
            occurrence.source_block_id,
            occurrence.issue_ordinal,
            issue.log_relpath,
            issue.line_number,
            issue.raw_block,
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

        for block in blocks:
            _insert_source_block(conn, session_id, block)
        for cluster in clusters:
            _insert_cluster(conn, session_id, cluster)
        for occurrence in occurrences:
            _insert_occurrence(conn, session_id, occurrence)

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
