"""Read-only integrity audit for the real ck3chronicle evidence index."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re
import sqlite3


AUDIT_CONTRACT_VERSION = "database-real-corpus-audit-v1"
_HASH_DIRECTORY = re.compile(r"^[0-9a-f]{64}$")
_RAW_BLOCK_HEADER = re.compile(rb"^\[\d\d:\d\d:\d\d\]\[[A-Z]\]\[")
_REQUIRED_TABLES = {
    "sessions",
    "session_files",
    "raw_block_contents",
    "source_blocks",
    "issues",
    "issue_occurrences",
    "classification_runs",
    "classification_payloads",
    "classification_assignments",
    "session_runtime_contexts",
    "session_mounted_dlcs",
    "session_mounted_mods",
}


class DatabaseAuditError(RuntimeError):
    """The database could not be audited without mutation."""


def _readonly_connection(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise DatabaseAuditError(f"database not found: {path}")
    conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _counts(conn: sqlite3.Connection, table: str) -> dict[int, int]:
    return {
        int(row["session_id"]): int(row["count"])
        for row in conn.execute(
            f"SELECT session_id, COUNT(*) AS count FROM {table} GROUP BY session_id"
        )
    }


def _sums(
    conn: sqlite3.Connection, table: str, column: str
) -> dict[int, int]:
    return {
        int(row["session_id"]): int(row["total"] or 0)
        for row in conn.execute(
            f"SELECT session_id, SUM({column}) AS total FROM {table} GROUP BY session_id"
        )
    }


def _count_raw_block_headers(path: Path) -> int:
    """Independently count timestamped CK3 blocks without using the parser."""
    count = 0
    with path.open("rb") as handle:
        for line in handle:
            count += int(_RAW_BLOCK_HEADER.match(line) is not None)
    return count


def audit_database(root: Path, *, deep: bool = False) -> dict[str, object]:
    """Audit archive/index agreement and stored canonical invariants read-only.

    ``deep`` performs full per-block and per-signature distribution checks. It
    is intentionally opt-in because a full per-occurrence distribution scan can
    take several minutes on the real corpus.
    """
    evidence_root = Path(root)
    db_path = evidence_root / "ck3chronicle.db"
    sessions_root = evidence_root / "sessions"
    pending_root = evidence_root / "pending"
    conn = _readonly_connection(db_path)
    findings: list[dict[str, object]] = []

    def finding(
        severity: str,
        code: str,
        category: str,
        message: str,
        *,
        session_ids: list[int] | None = None,
        details: dict[str, object] | None = None,
    ) -> None:
        findings.append(
            {
                "severity": severity,
                "code": code,
                "category": category,
                "message": message,
                "session_ids": session_ids or [],
                "details": details or {},
            }
        )

    try:
        tables = {
            str(row["name"])
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        missing_tables = sorted(_REQUIRED_TABLES - tables)
        if missing_tables:
            finding(
                "error",
                "DB-SCHEMA-001",
                "index_integrity",
                "required database tables are missing",
                details={"missing_tables": missing_tables},
            )
            return _result(
                db_path, evidence_root, findings, [], {}, tables=tables, deep=deep
            )

        session_rows = list(
            conn.execute("SELECT * FROM sessions ORDER BY created_at, session_id")
        )
        session_ids = [int(row["session_id"]) for row in session_rows]
        db_hashes = {str(row["evidence_bundle_hash"]) for row in session_rows}

        archive_hashes: set[str] = set()
        manifestless_archives: list[str] = []
        if sessions_root.is_dir():
            for item in sessions_root.iterdir():
                if not item.is_dir() or not _HASH_DIRECTORY.fullmatch(item.name):
                    continue
                archive_hashes.add(item.name)
                if not (item / "manifest.json").is_file():
                    manifestless_archives.append(item.name)
        else:
            finding(
                "error",
                "DB-EVIDENCE-001",
                "evidence_integrity",
                "finalized sessions directory is missing",
            )

        missing_archives = sorted(db_hashes - archive_hashes)
        orphan_archives = sorted(archive_hashes - db_hashes)
        if missing_archives:
            missing_ids = [
                int(row["session_id"])
                for row in session_rows
                if row["evidence_bundle_hash"] in missing_archives
            ]
            finding(
                "error",
                "DB-EVIDENCE-002",
                "evidence_integrity",
                "registered sessions are missing finalized archive directories",
                session_ids=missing_ids,
                details={"hashes": missing_archives[:20], "count": len(missing_archives)},
            )
        if orphan_archives:
            finding(
                "warning",
                "DB-INDEX-001",
                "index_integrity",
                "finalized archives are not registered in SQLite",
                details={"hashes": orphan_archives[:20], "count": len(orphan_archives)},
            )
        if manifestless_archives:
            finding(
                "error",
                "DB-EVIDENCE-003",
                "evidence_integrity",
                "finalized archive directories are missing manifest.json",
                details={
                    "hashes": sorted(manifestless_archives)[:20],
                    "count": len(manifestless_archives),
                },
            )

        file_counts = _counts(conn, "session_files")
        block_counts = _counts(conn, "source_blocks")
        occurrence_counts = _counts(conn, "issue_occurrences")
        issue_counts = _counts(conn, "issues")
        issue_occurrence_sums = _sums(conn, "issues", "occurrence_count")
        block_issue_sums = _sums(conn, "source_blocks", "issue_count")
        context_counts = _counts(conn, "session_runtime_contexts")
        dlc_counts = _counts(conn, "session_mounted_dlcs")
        mod_counts = _counts(conn, "session_mounted_mods")

        session_summaries: list[dict[str, object]] = []
        capped_sessions: list[int] = []
        raw_block_total = 0
        for row in session_rows:
            session_id = int(row["session_id"])
            files = file_counts.get(session_id, 0)
            blocks = block_counts.get(session_id, 0)
            occurrences = occurrence_counts.get(session_id, 0)
            issues = issue_counts.get(session_id, 0)
            summary = {
                "session_id": session_id,
                "captured_at": row["created_at"],
                "capture_status": row["capture_status"],
                "parse_status": row["parse_status"],
                "manifest_files": files,
                "source_blocks": blocks,
                "raw_timestamp_headers": None,
                "occurrences": occurrences,
                "issues": issues,
                "classification_runs": 0,
                "classification_assignments": 0,
                "runtime_context": None,
            }
            session_summaries.append(summary)

            archived_error = (
                sessions_root / str(row["evidence_bundle_hash"]) / "error.log"
            )
            if archived_error.is_file():
                raw_headers = _count_raw_block_headers(archived_error)
                raw_block_total += raw_headers
                summary["raw_timestamp_headers"] = raw_headers
                if raw_headers != blocks:
                    finding(
                        "error",
                        "DB-RAW-001",
                        "canonical_parse",
                        "archived error.log block headers disagree with source_blocks",
                        session_ids=[session_id],
                        details={
                            "raw_timestamp_headers": raw_headers,
                            "source_blocks": blocks,
                        },
                    )

            if row["capture_status"] != "finalized":
                finding(
                    "error",
                    "DB-CAPTURE-001",
                    "evidence_integrity",
                    "session is not finalized",
                    session_ids=[session_id],
                )
            manifest_aggregate = conn.execute(
                """
                SELECT COUNT(*) AS files,
                       SUM(CASE WHEN kind = 'log' THEN 1 ELSE 0 END) AS logs,
                       SUM(CASE WHEN kind = 'crash' THEN 1 ELSE 0 END) AS crashes,
                       COALESCE(SUM(bytes), 0) AS bytes
                FROM session_files WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()
            expected_manifest = (
                int(row["log_count"]),
                int(row["crash_present"]),
                int(row["total_bytes"]),
            )
            actual_manifest = (
                int(manifest_aggregate["logs"] or 0),
                int((manifest_aggregate["crashes"] or 0) > 0),
                int(manifest_aggregate["bytes"] or 0),
            )
            if expected_manifest != actual_manifest:
                finding(
                    "error",
                    "DB-MANIFEST-001",
                    "evidence_integrity",
                    "session aggregates disagree with session_files",
                    session_ids=[session_id],
                    details={"stored": expected_manifest, "actual": actual_manifest},
                )

            parse_actual = (blocks, occurrences, issues, 0)
            parse_stored = (
                int(row["parse_source_blocks"] or 0),
                int(row["parse_issue_occurrences"] or 0),
                int(row["parse_issue_clusters"] or 0),
                int(row["parse_silently_dropped_blocks"] or 0),
            )
            if row["parse_status"] != "succeeded" or parse_stored != parse_actual:
                finding(
                    "error",
                    "DB-PARSE-001",
                    "canonical_parse",
                    "stored parser state disagrees with canonical rows",
                    session_ids=[session_id],
                    details={"stored": parse_stored, "actual": parse_actual},
                )
            if (
                block_issue_sums.get(session_id, 0) != occurrences
                or issue_occurrence_sums.get(session_id, 0) != occurrences
            ):
                finding(
                    "error",
                    "DB-PARSE-002",
                    "canonical_parse",
                    "canonical occurrence totals do not reconcile",
                    session_ids=[session_id],
                    details={
                        "occurrences": occurrences,
                        "block_issue_sum": block_issue_sums.get(session_id, 0),
                        "issue_occurrence_sum": issue_occurrence_sums.get(session_id, 0),
                    },
                )
            if blocks == 100_000:
                capped_sessions.append(session_id)

        if deep:
            per_block_mismatches = int(
                conn.execute(
                """
                SELECT COUNT(*) FROM (
                    SELECT sb.session_id, sb.source_block_pk
                    FROM source_blocks sb
                    LEFT JOIN issue_occurrences io
                      ON io.source_block_pk = sb.source_block_pk
                    GROUP BY sb.session_id, sb.source_block_pk, sb.issue_count
                    HAVING sb.issue_count != COUNT(io.issue_occurrence_id)
                )
                """
                ).fetchone()[0]
            )
            if per_block_mismatches:
                finding(
                    "error",
                    "DB-PARSE-003",
                    "canonical_parse",
                    "source-block issue counts disagree with occurrence rows",
                    details={"mismatched_blocks": per_block_mismatches},
                )

            per_signature_mismatches = int(
                conn.execute(
                """
                SELECT COUNT(*) FROM (
                    SELECT i.session_id, i.signature
                    FROM issues i
                    LEFT JOIN issue_occurrences io
                      ON io.session_id = i.session_id
                     AND io.signature = i.signature
                    GROUP BY i.session_id, i.signature, i.occurrence_count
                    HAVING i.occurrence_count != COUNT(io.issue_occurrence_id)
                )
                """
                ).fetchone()[0]
            )
            if per_signature_mismatches:
                finding(
                    "error",
                    "DB-PARSE-004",
                    "canonical_parse",
                    "issue-cluster counts disagree with occurrence rows",
                    details={"mismatched_issues": per_signature_mismatches},
                )

        runs = list(conn.execute("SELECT * FROM classification_runs ORDER BY run_id"))
        runs_by_session: dict[int, list[sqlite3.Row]] = {}
        for run in runs:
            runs_by_session.setdefault(int(run["session_id"]), []).append(run)
        assignment_counts = {
            (int(row["run_id"]), str(row["assignment_level"])): int(row["count"])
            for row in conn.execute(
                """
                SELECT ca.run_id, cp.assignment_level, COUNT(*) AS count
                FROM classification_assignments ca
                JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
                GROUP BY ca.run_id, cp.assignment_level
                """
            )
        }
        for summary in session_summaries:
            session_id = int(summary["session_id"])
            session_runs = runs_by_session.get(session_id, [])
            summary["classification_runs"] = len(session_runs)
            summary["classification_assignments"] = sum(
                assignment_counts.get((int(run["run_id"]), level), 0)
                for run in session_runs
                for level in ("full", "l1_l2", "l1", "unknown")
            )
            if not session_runs:
                finding(
                    "error",
                    "DB-CLASSIFY-001",
                    "classification",
                    "parsed session has no classification run",
                    session_ids=[session_id],
                )
            for run in session_runs:
                run_id = int(run["run_id"])
                actual = {
                    level: assignment_counts.get((run_id, level), 0)
                    for level in ("full", "l1_l2", "l1", "unknown")
                }
                expected = {
                    "full": int(run["full_count"]),
                    "l1_l2": int(run["l1_l2_count"]),
                    "l1": int(run["l1_count"]),
                    "unknown": int(run["unknown_count"]),
                }
                if (
                    actual != expected
                    or sum(actual.values()) != int(run["semantic_occurrence_count"])
                    or int(run["source_block_count"])
                    != block_counts.get(session_id, 0)
                ):
                    finding(
                        "error",
                        "DB-CLASSIFY-002",
                        "classification",
                        "classification run counters disagree with assignments",
                        session_ids=[session_id],
                        details={
                            "run_id": run_id,
                            "stored": expected,
                            "actual": actual,
                            "stored_source_blocks": int(run["source_block_count"]),
                            "actual_source_blocks": block_counts.get(session_id, 0),
                        },
                    )

        contexts = {
            int(row["session_id"]): row
            for row in conn.execute("SELECT * FROM session_runtime_contexts")
        }
        for summary in session_summaries:
            session_id = int(summary["session_id"])
            context = contexts.get(session_id)
            if context is None:
                finding(
                    "error",
                    "DB-CONTEXT-001",
                    "runtime_context",
                    "session has no processed runtime context",
                    session_ids=[session_id],
                )
                continue
            summary["runtime_context"] = context["status"]
            stored = (int(context["dlc_count"]), int(context["mod_count"]))
            actual = (dlc_counts.get(session_id, 0), mod_counts.get(session_id, 0))
            if stored != actual:
                finding(
                    "error",
                    "DB-CONTEXT-002",
                    "runtime_context",
                    "runtime-context counts disagree with mounted rows",
                    session_ids=[session_id],
                    details={"stored": stored, "actual": actual},
                )

        relational_orphans = {
            "occurrences_without_block": int(
                conn.execute(
                    """
                    SELECT COUNT(*) FROM issue_occurrences io
                    LEFT JOIN source_blocks sb
                      ON sb.source_block_pk = io.source_block_pk
                    WHERE sb.source_block_pk IS NULL
                    """
                ).fetchone()[0]
            ),
            "assignments_without_block": int(
                conn.execute(
                    """
                    SELECT COUNT(*) FROM classification_assignments ca
                    LEFT JOIN source_blocks sb
                      ON sb.source_block_pk = ca.source_block_pk
                    WHERE sb.source_block_pk IS NULL
                    """
                ).fetchone()[0]
            ),
            "blocks_without_raw_content": int(
                conn.execute(
                    """
                    SELECT COUNT(*) FROM source_blocks sb
                    LEFT JOIN raw_block_contents rb
                      ON rb.raw_block_pk = sb.raw_block_pk
                    WHERE rb.raw_block_pk IS NULL
                    """
                ).fetchone()[0]
            ),
            "assignments_without_payload": int(
                conn.execute(
                    """
                    SELECT COUNT(*) FROM classification_assignments ca
                    LEFT JOIN classification_payloads cp
                      ON cp.payload_pk = ca.payload_pk
                    LEFT JOIN classification_runs cr ON cr.run_id = ca.run_id
                    WHERE cp.payload_pk IS NULL
                       OR cr.run_id IS NULL
                       OR cp.model_sha256 != cr.model_sha256
                    """
                ).fetchone()[0]
            ),
        }
        if any(relational_orphans.values()):
            finding(
                "error",
                "DB-PROVENANCE-001",
                "index_integrity",
                "canonical/classification rows have no source-block provenance",
                details=relational_orphans,
            )

        if capped_sessions:
            finding(
                "warning",
                "DB-QUALITY-001",
                "evidence_quality",
                "sessions end at exactly 100,000 source blocks; the repeated boundary is observed but its cause is unverified",
                session_ids=capped_sessions,
            )

        observation_count = (
            int(conn.execute("SELECT COUNT(*) FROM capture_observations").fetchone()[0])
            if "capture_observations" in tables
            else 0
        )
        if observation_count < len(session_rows):
            finding(
                "warning",
                "DB-CHRONOLOGY-001",
                "index_integrity",
                "durable process-run chronology is incomplete for imported sessions",
                details={
                    "capture_observations": observation_count,
                    "sessions": len(session_rows),
                },
            )

        aggregates = {
            "archive_directories": len(archive_hashes),
            "registered_sessions": len(session_rows),
            "pending_directories": (
                len([item for item in pending_root.iterdir() if item.is_dir()])
                if pending_root.is_dir()
                else 0
            ),
            "source_blocks": sum(block_counts.values()),
            "raw_timestamp_headers": raw_block_total,
            "occurrences": sum(occurrence_counts.values()),
            "issues": sum(issue_counts.values()),
            "classification_runs": len(runs),
            "classification_assignments": sum(
                int(summary["classification_assignments"])
                for summary in session_summaries
            ),
        }
        return _result(
            db_path,
            evidence_root,
            findings,
            session_summaries,
            aggregates,
            tables=tables,
            deep=deep,
        )
    finally:
        conn.close()


def _result(
    db_path: Path,
    root: Path,
    findings: list[dict[str, object]],
    sessions: list[dict[str, object]],
    aggregates: dict[str, object],
    *,
    tables: set[str],
    deep: bool,
) -> dict[str, object]:
    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "schema": "ck3chronicle.database-audit",
        "schema_version": 1,
        "contract_version": AUDIT_CONTRACT_VERSION,
        "audited_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "database": str(db_path),
        "database_bytes": db_path.stat().st_size if db_path.is_file() else None,
        "status": "fail" if errors else "warning" if warnings else "pass",
        "summary": {
            "errors": errors,
            "warnings": warnings,
            **aggregates,
        },
        "findings": findings,
        "sessions": sessions,
        "tables": sorted(tables),
        "read_only": True,
        "audit_depth": "deep" if deep else "standard",
    }
