"""Evidence-bearing investigation priorities over stored session intelligence."""

from __future__ import annotations

from collections import Counter, defaultdict
import re
import sqlite3

from .reporting import build_session_report, latest_session_id
from .session_intelligence import (
    ComparisonError,
    assignment_pattern_id,
    compare_sessions,
)
from .source_resolution import resolve_file_instances


class TriageError(RuntimeError):
    """The requested session cannot produce a defensible triage view."""


_FILE_LOCATION = re.compile(
    r"\bfile:\s*(?P<path>.+?)\s+(?:near\s+)?line:\s*\d+",
    re.IGNORECASE,
)


def _file_from_location(value: str | None) -> str | None:
    if not value:
        return None
    match = _FILE_LOCATION.search(value.replace("\\", "/"))
    if match is None:
        return None
    path = match.group("path").strip().strip("'\"")
    return (
        path
        if path
        and ("/" in path or "." in path)
        and not path.startswith(("/", "../"))
        and ":/" not in path
        else None
    )


def _latest_run(conn: sqlite3.Connection, session_id: int) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT * FROM classification_runs
        WHERE session_id = ?
        ORDER BY classified_at DESC, run_id DESC
        LIMIT 1
        """,
        (session_id,),
    ).fetchone()


def _pattern_files(
    conn: sqlite3.Connection,
    run_id: int,
) -> dict[str, Counter[str]]:
    mapping: dict[str, Counter[str]] = defaultdict(Counter)
    rows = conn.execute(
        """
        SELECT ca.contract_id, ca.source_family, ca.normalized_tokens_json,
               ca.location_evidence, sb.raw_block
        FROM classification_assignments ca
        JOIN source_blocks sb
          ON sb.session_id = ca.session_id
         AND sb.source_block_id = ca.source_block_id
        WHERE ca.run_id = ?
        """,
        (run_id,),
    ).fetchall()
    for row in rows:
        file = _file_from_location(row["location_evidence"]) or _file_from_location(
            row["raw_block"]
        )
        if file is None:
            continue
        pattern_id = assignment_pattern_id(
            row["contract_id"],
            row["source_family"],
            row["normalized_tokens_json"],
        )
        mapping[pattern_id][file] += 1
    return mapping


def build_triage(
    conn: sqlite3.Connection,
    session_id: int | None = None,
    against_session_id: int | None = None,
    *,
    limit: int = 20,
) -> dict[str, object]:
    """Rank observed regressions and attach bounded current source evidence."""
    if limit < 1:
        raise ValueError("triage limit must be positive")
    current_id = session_id if session_id is not None else latest_session_id(conn)
    if current_id is None:
        raise TriageError("no captured sessions exist")
    try:
        comparison = compare_sessions(
            conn,
            current_id,
            against_session_id,
            limit=1_000_000,
        )
    except ComparisonError as exc:
        raise TriageError(str(exc)) from exc
    run = _latest_run(conn, current_id)
    if run is None:
        raise TriageError(f"session_id {current_id} has not been classified")
    report = build_session_report(
        conn,
        current_id,
        model_sha256=str(run["model_sha256"]),
        limit=limit,
    )
    files_by_pattern = _pattern_files(conn, int(run["run_id"]))
    regressions: list[dict[str, object]] = []
    for item in comparison["changed_patterns"]:
        if item["status"] not in {"new", "worse"}:
            continue
        file_counts = files_by_pattern.get(str(item["pattern_id"]), Counter())
        dominant_file = None
        resolution = None
        if file_counts:
            dominant_file, _count = min(
                file_counts.items(),
                key=lambda pair: (-pair[1], pair[0].casefold(), pair[0]),
            )
            resolution = resolve_file_instances(conn, current_id, dominant_file)
        regressions.append(
            {
                **item,
                "priority_reasons": [
                    f"observed_{item['status']}_pattern",
                    f"occurrence_delta_{int(item['delta']):+d}",
                    *(["human_ignore_annotation"] if item["ignored"] else []),
                ],
                "location_evidence": {
                    "dominant_file": dominant_file,
                    "dominant_file_occurrences": (
                        int(file_counts[dominant_file]) if dominant_file else 0
                    ),
                    "distinct_files": len(file_counts),
                    "top_files": [
                        {"file": file, "occurrences": count}
                        for file, count in sorted(
                            file_counts.items(),
                            key=lambda pair: (-pair[1], pair[0].casefold(), pair[0]),
                        )[:5]
                    ],
                },
                "source_resolution": resolution,
            }
        )
        if len(regressions) >= limit:
            break
    return {
        "schema": "ck3chronicle.action-triage",
        "schema_version": 1,
        "current_session": comparison["current_session"],
        "previous_session": comparison["previous_session"],
        "model_sha256": comparison["model_sha256"],
        "evidence_quality": comparison["evidence_quality"],
        "runtime_context_delta": comparison["runtime_context_delta"],
        "summary": {
            "regression_patterns_total": sum(
                count
                for status, count in comparison["summary"]["pattern_counts"].items()
                if status in {"new", "worse"}
            ),
            "returned_regressions": len(regressions),
            "classification_review_occurrences": report["classification"][
                "review_required"
            ],
            "source_resolved_regressions": sum(
                item["source_resolution"] is not None
                and item["source_resolution"]["last_mounted_candidate"] is not None
                for item in regressions
            ),
        },
        "regressions": regressions,
        "classification_review": report["review_queue"],
        "caveat": (
            "Priorities describe observed count changes and current active-root "
            "file candidates; they do not prove causal ownership."
        ),
    }
