"""Deterministic reports built exclusively from stored canonical records."""

from __future__ import annotations

import json
import sqlite3

from .db import repository


class ReportError(RuntimeError):
    """A stored session is absent or not ready for reporting."""


def latest_session_id(conn: sqlite3.Connection) -> int | None:
    """Return the latest captured session, never the greatest registry ID."""
    row = conn.execute(
        """
        SELECT session_id
        FROM sessions
        ORDER BY created_at DESC, session_id DESC
        LIMIT 1
        """
    ).fetchone()
    return int(row[0]) if row is not None else None


def _classification_run(
    conn: sqlite3.Connection, session_id: int, model_sha256: str | None
) -> sqlite3.Row | None:
    if model_sha256 is not None:
        return repository.get_classification_run(conn, session_id, model_sha256)
    return conn.execute(
        """
        SELECT *
        FROM classification_runs
        WHERE session_id = ?
        ORDER BY classified_at DESC, run_id DESC
        LIMIT 1
        """,
        (session_id,),
    ).fetchone()


def _summary_rows(
    conn: sqlite3.Connection, sql: str, parameters: tuple[object, ...]
) -> list[dict[str, object]]:
    return [dict(row) for row in conn.execute(sql, parameters).fetchall()]


def _pattern_template(row: sqlite3.Row) -> str | None:
    if row["catalog_template"]:
        return row["catalog_template"]
    if row["assignment_level"] == "l1_l2" and row["l1_template"]:
        return f"{row['l1_template']} [ {row['l2_template']} ]"
    if row["assignment_level"] == "l1" and row["l1_template"]:
        return f"{row['l1_template']} [ <UNRESOLVED_REASON> ]"
    return None


def build_session_report(
    conn: sqlite3.Connection,
    session_id: int,
    *,
    model_sha256: str | None = None,
    limit: int = 20,
) -> dict[str, object]:
    """Build one schema-versioned executive report without reopening logs."""
    if limit < 1:
        raise ValueError("report limit must be positive")
    session = repository.get_session(conn, session_id)
    if session is None:
        raise ReportError(f"session_id {session_id} not found")
    if session["parse_status"] != "succeeded":
        raise ReportError(f"session_id {session_id} has not been parsed")
    run = _classification_run(conn, session_id, model_sha256)
    if run is None:
        raise ReportError(f"session_id {session_id} has not been classified")
    model = repository.get_classification_model(conn, run["model_sha256"])
    if model is None:
        raise ReportError("classification model registry row is missing")

    semantic_occurrences = int(run["semantic_occurrence_count"])
    full = int(run["full_count"])
    l1_l2 = int(run["l1_l2_count"])
    l1 = int(run["l1_count"])
    unknown = int(run["unknown_count"])

    source_summary = _summary_rows(
        conn,
        """
        SELECT cp.source_family, COUNT(*) AS occurrences
        FROM classification_assignments ca
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        WHERE ca.run_id = ?
        GROUP BY cp.source_family
        ORDER BY occurrences DESC, cp.source_family
        LIMIT ?
        """,
        (run["run_id"], limit),
    )
    category_summary = _summary_rows(
        conn,
        """
        SELECT category, SUM(occurrence_count) AS occurrences
        FROM issues
        WHERE session_id = ?
        GROUP BY category
        ORDER BY occurrences DESC, category
        LIMIT ?
        """,
        (session_id, limit),
    )
    file_summary = _summary_rows(
        conn,
        """
        SELECT primary_file AS file, SUM(occurrence_count) AS occurrences
        FROM issues
        WHERE session_id = ? AND primary_file IS NOT NULL AND primary_file != ''
        GROUP BY primary_file
        ORDER BY occurrences DESC, primary_file
        LIMIT ?
        """,
        (session_id, limit),
    )
    pattern_rows = conn.execute(
        """
        SELECT cp.assignment_level,
               cp.contract_id,
               cp.source_family,
               cp.l1_template,
               cp.l2_template,
               cc.template AS catalog_template,
               MIN(cp.semantic_text) AS sample,
               COUNT(*) AS occurrences,
               MIN(sb.start_line) AS first_line
        FROM classification_assignments ca
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        JOIN source_blocks sb
          ON sb.session_id = ca.session_id
         AND sb.source_block_pk = ca.source_block_pk
        LEFT JOIN classification_contracts cc
         ON cc.model_sha256 = ?
         AND cc.contract_id = cp.contract_id
        WHERE ca.run_id = ?
        GROUP BY cp.assignment_level,
                 cp.contract_id,
                 cp.source_family,
                 cp.l1_template,
                 cp.l2_template,
                 CASE
                     WHEN cp.contract_id IS NOT NULL THEN cp.contract_id
                     ELSE cp.normalized_tokens_json
                 END,
                 cc.template
        ORDER BY occurrences DESC, cp.source_family, first_line
        LIMIT ?
        """,
        (run["model_sha256"], run["run_id"], limit),
    ).fetchall()
    top_patterns = [
        {
            "assignment_level": row["assignment_level"],
            "contract_id": row["contract_id"],
            "source_family": row["source_family"],
            "occurrences": int(row["occurrences"]),
            "first_line": int(row["first_line"]),
            "template": _pattern_template(row),
            "sample": row["sample"],
        }
        for row in pattern_rows
    ]
    review_rows = repository.list_classification_review_items(
        conn,
        session_id=session_id,
        model_sha256=run["model_sha256"],
        level="all",
        limit=limit,
    )
    review_queue = [
        {
            "assignment_level": row["assignment_level"],
            "source_family": row["source_family"],
            "occurrences": int(row["occurrences"]),
            "first_line": int(row["first_line"]),
            "l1_template": row["l1_template"],
            "l2_template": row["l2_template"],
            "sample": row["sample"],
        }
        for row in review_rows
    ]
    parse = {
        "contract_version": session["parser_contract_version"],
        "source_blocks": int(session["parse_source_blocks"]),
        "preamble_blocks": int(session["parse_preamble_blocks"]),
        "canonical_occurrences": int(session["parse_issue_occurrences"]),
        "issue_clusters": int(session["parse_issue_clusters"]),
        "unclassified_occurrences": int(session["parse_unclassified_occurrences"]),
        "multi_issue_blocks": int(session["parse_multi_issue_blocks"]),
    }
    classification = {
        "run_id": int(run["run_id"]),
        "contract_version": run["classification_contract_version"],
        "model_revision_id": model["revision_id"],
        "model_sha256": run["model_sha256"],
        "semantic_occurrences": semantic_occurrences,
        "counts": {
            "full": full,
            "l1_l2": l1_l2,
            "l1": l1,
            "unknown": unknown,
        },
        "full_rate": full / semantic_occurrences if semantic_occurrences else 1.0,
        "l1_or_better_rate": (
            (full + l1_l2 + l1) / semantic_occurrences
            if semantic_occurrences
            else 1.0
        ),
        "review_required": l1 + unknown,
    }
    runtime_row = repository.get_runtime_context(conn, session_id)
    runtime_context = None
    if runtime_row is not None:
        runtime_context = {
            "contract_version": runtime_row["context_contract_version"],
            "status": runtime_row["status"],
            "debug_log_sha256": runtime_row["debug_log_sha256"],
            "mounted_entry_count": int(runtime_row["mounted_entry_count"]),
            "dlc_count": int(runtime_row["dlc_count"]),
            "mod_count": int(runtime_row["mod_count"]),
            "unknown_mount_count": int(runtime_row["unknown_mount_count"]),
            "warnings": json.loads(runtime_row["warnings_json"]),
            "dlcs": [
                {
                    "dlc_order": int(row["dlc_order"]),
                    "dlc_key": row["dlc_key"],
                    "display_name": row["display_name"],
                    "descriptor_path": row["descriptor_path"],
                    "mount_path": row["mount_path"],
                }
                for row in repository.get_mounted_dlcs(conn, session_id)
            ],
            "active_mods": [
                {
                    "load_order": int(row["load_order"]),
                    "mod_key": row["mod_key"],
                    "display_name": row["display_name"],
                    "descriptor_path": row["descriptor_path"],
                    "mount_path": row["mount_path"],
                    "source_kind": row["source_kind"],
                }
                for row in repository.get_mounted_mods(conn, session_id)
            ],
        }
    return {
        "schema": "ck3chronicle.session-report",
        "schema_version": 2,
        "session": {
            "session_id": int(session["session_id"]),
            "captured_at": session["created_at"],
            "evidence_bundle_hash": session["evidence_bundle_hash"],
            "log_count": int(session["log_count"]),
            "crash_present": bool(session["crash_present"]),
            "total_bytes": int(session["total_bytes"]),
            "evidence_completeness": session["evidence_completeness"],
        },
        "parse": parse,
        "classification": classification,
        "runtime_context": runtime_context,
        "category_summary": category_summary,
        "source_summary": source_summary,
        "file_summary": file_summary,
        "top_patterns": top_patterns,
        "review_queue": review_queue,
    }
