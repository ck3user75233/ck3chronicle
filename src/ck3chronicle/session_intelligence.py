"""Deterministic, evidence-scoped comparisons between classified sessions."""

from __future__ import annotations

from hashlib import sha256
import json
import sqlite3

from .db import repository
from .reporting import latest_session_id


class ComparisonError(RuntimeError):
    """A requested comparison cannot be made from compatible stored evidence."""


def _classification_run(
    conn: sqlite3.Connection,
    session_id: int,
    model_sha256: str | None,
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


def previous_session_id(
    conn: sqlite3.Connection,
    session_id: int,
    *,
    model_sha256: str,
) -> int | None:
    """Return the preceding capture that has a run for the same exact model."""
    current = repository.get_session(conn, session_id)
    if current is None:
        raise ComparisonError(f"session_id {session_id} not found")
    row = conn.execute(
        """
        SELECT s.session_id
        FROM sessions s
        JOIN classification_runs cr ON cr.session_id = s.session_id
        WHERE cr.model_sha256 = ?
          AND (
              s.created_at < ?
              OR (s.created_at = ? AND s.session_id < ?)
          )
        ORDER BY s.created_at DESC, s.session_id DESC
        LIMIT 1
        """,
        (
            model_sha256,
            current["created_at"],
            current["created_at"],
            session_id,
        ),
    ).fetchone()
    return int(row[0]) if row is not None else None


def _residual_identity_tokens(tokens_json: str) -> tuple[str, ...]:
    """Canonicalize residual identity without reinterpreting its semantics.

    The production tokenizer already replaces path-plus-line spans with
    ``<LOCATOR>``. CK3 sometimes appends a parenthesized script-location chain
    after ``near file: <LOCATOR>``; that suffix is location evidence too and
    must never split an error pattern.
    """
    try:
        raw = json.loads(tokens_json)
    except json.JSONDecodeError as exc:
        raise ComparisonError("stored normalized tokens are not valid JSON") from exc
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ComparisonError("stored normalized tokens are not a string list")
    tokens = tuple(raw)
    folded = tuple(item.casefold() for item in tokens)
    for index, token in enumerate(tokens):
        if token != "<LOCATOR>":
            continue
        prefix = folded[max(0, index - 4) : index]
        if "near" in prefix and "file" in prefix:
            return tokens[: index + 1]
    return tokens


def _pattern_id(contract_id: str | None, source: str, tokens_json: str) -> str:
    if contract_id is not None:
        return contract_id
    tokens = json.dumps(
        _residual_identity_tokens(tokens_json),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    material = f"residual\0{source.casefold()}\0{tokens}"
    return "r_" + sha256(material.encode("utf-8")).hexdigest()[:16]


def _template(row: sqlite3.Row) -> str | None:
    if row["catalog_template"]:
        return str(row["catalog_template"])
    if row["assignment_level"] == "l1_l2" and row["l1_template"]:
        return f"{row['l1_template']} [ {row['l2_template']} ]"
    if row["assignment_level"] == "l1" and row["l1_template"]:
        return f"{row['l1_template']} [ <UNRESOLVED_REASON> ]"
    return None


def _patterns(
    conn: sqlite3.Connection,
    run: sqlite3.Row,
) -> dict[str, dict[str, object]]:
    rows = conn.execute(
        """
        SELECT MIN(ca.assignment_level) AS assignment_level,
               ca.contract_id,
               MIN(ca.source_family) AS source_family,
               MIN(ca.normalized_tokens_json) AS normalized_tokens_json,
               MIN(ca.l1_template) AS l1_template,
               MIN(ca.l2_template) AS l2_template,
               MIN(cc.template) AS catalog_template,
               MIN(ca.semantic_text) AS sample,
               COUNT(*) AS occurrences
        FROM classification_assignments ca
        LEFT JOIN classification_contracts cc
          ON cc.model_sha256 = ?
         AND cc.contract_id = ca.contract_id
        WHERE ca.run_id = ?
        GROUP BY ca.contract_id,
                 CASE
                     WHEN ca.contract_id IS NULL THEN lower(ca.source_family)
                     ELSE NULL
                 END,
                 CASE
                     WHEN ca.contract_id IS NULL THEN ca.normalized_tokens_json
                     ELSE NULL
                 END
        """,
        (run["model_sha256"], run["run_id"]),
    ).fetchall()
    patterns: dict[str, dict[str, object]] = {}
    for row in rows:
        pattern_id = _pattern_id(
            row["contract_id"],
            row["source_family"],
            row["normalized_tokens_json"],
        )
        item = {
            "pattern_id": pattern_id,
            "contract_id": row["contract_id"],
            "assignment_level": row["assignment_level"],
            "source_family": row["source_family"],
            "template": _template(row),
            "sample": row["sample"],
            "occurrences": int(row["occurrences"]),
        }
        existing = patterns.get(pattern_id)
        if existing is None:
            patterns[pattern_id] = item
            continue
        comparable = (
            "contract_id",
            "assignment_level",
            "source_family",
            "template",
        )
        if any(existing[key] != item[key] for key in comparable):
            raise ComparisonError(f"pattern identity collision: {pattern_id}")
        existing["occurrences"] = int(existing["occurrences"]) + int(
            item["occurrences"]
        )
        existing["sample"] = min(str(existing["sample"]), str(item["sample"]))
    return patterns


def _session_identity(session: sqlite3.Row) -> dict[str, object]:
    return {
        "session_id": int(session["session_id"]),
        "captured_at": session["created_at"],
        "evidence_bundle_hash": session["evidence_bundle_hash"],
    }


def compare_sessions(
    conn: sqlite3.Connection,
    current_session_id: int,
    against_session_id: int | None = None,
    *,
    model_sha256: str | None = None,
    limit: int = 50,
) -> dict[str, object]:
    """Compare observed semantic-pattern counts under one immutable model."""
    if limit < 1:
        raise ValueError("comparison limit must be positive")
    current_session = repository.get_session(conn, current_session_id)
    if current_session is None:
        raise ComparisonError(f"session_id {current_session_id} not found")
    current_run = _classification_run(conn, current_session_id, model_sha256)
    if current_run is None:
        raise ComparisonError(
            f"session_id {current_session_id} has no compatible classification run"
        )
    exact_model = str(current_run["model_sha256"])
    if against_session_id is None:
        against_session_id = previous_session_id(
            conn,
            current_session_id,
            model_sha256=exact_model,
        )
        if against_session_id is None:
            raise ComparisonError("no preceding classified session exists")
    if against_session_id == current_session_id:
        raise ComparisonError("a session cannot be compared with itself")
    against_session = repository.get_session(conn, against_session_id)
    if against_session is None:
        raise ComparisonError(f"session_id {against_session_id} not found")
    against_run = _classification_run(conn, against_session_id, exact_model)
    if against_run is None:
        raise ComparisonError(
            f"session_id {against_session_id} has no run for model {exact_model}"
        )

    before = _patterns(conn, against_run)
    after = _patterns(conn, current_run)
    changed: list[dict[str, object]] = []
    unchanged: list[dict[str, object]] = []
    pattern_counts = {
        "new": 0,
        "fixed": 0,
        "worse": 0,
        "improved": 0,
        "unchanged": 0,
    }
    occurrence_movement = {
        "introduced": 0,
        "eliminated": 0,
        "increased": 0,
        "reduced": 0,
    }
    for pattern_id in sorted(set(before) | set(after)):
        previous_item = before.get(pattern_id)
        current_item = after.get(pattern_id)
        previous_count = int(previous_item["occurrences"]) if previous_item else 0
        current_count = int(current_item["occurrences"]) if current_item else 0
        delta = current_count - previous_count
        if previous_count == 0:
            status = "new"
            occurrence_movement["introduced"] += current_count
        elif current_count == 0:
            status = "fixed"
            occurrence_movement["eliminated"] += previous_count
        elif delta > 0:
            status = "worse"
            occurrence_movement["increased"] += delta
        elif delta < 0:
            status = "improved"
            occurrence_movement["reduced"] += -delta
        else:
            status = "unchanged"
        pattern_counts[status] += 1
        representative = current_item or previous_item
        assert representative is not None
        comparison = {
            key: representative[key]
            for key in (
                "pattern_id",
                "contract_id",
                "assignment_level",
                "source_family",
                "template",
                "sample",
            )
        }
        comparison.update(
            {
                "status": status,
                "previous_occurrences": previous_count,
                "current_occurrences": current_count,
                "delta": delta,
            }
        )
        (unchanged if status == "unchanged" else changed).append(comparison)

    priority = {"new": 0, "fixed": 1, "worse": 2, "improved": 3}
    changed.sort(
        key=lambda item: (
            -abs(int(item["delta"])),
            priority[str(item["status"])],
            str(item["source_family"]),
            str(item["pattern_id"]),
        )
    )
    unchanged.sort(
        key=lambda item: (
            -int(item["current_occurrences"]),
            str(item["source_family"]),
            str(item["pattern_id"]),
        )
    )
    previous_total = int(against_run["semantic_occurrence_count"])
    current_total = int(current_run["semantic_occurrence_count"])
    return {
        "schema": "ck3chronicle.session-comparison",
        "schema_version": 1,
        "comparison_basis": "observed_semantic_occurrence_counts",
        "model_sha256": exact_model,
        "previous_session": _session_identity(against_session),
        "current_session": _session_identity(current_session),
        "summary": {
            "previous_occurrences": previous_total,
            "current_occurrences": current_total,
            "net_change": current_total - previous_total,
            "pattern_counts": pattern_counts,
            "occurrence_movement": occurrence_movement,
        },
        "changed_patterns": changed[:limit],
        "unchanged_patterns": unchanged[:limit],
        "changed_patterns_total": len(changed),
        "unchanged_patterns_total": len(unchanged),
    }


def compare_latest(
    conn: sqlite3.Connection,
    *,
    against_session_id: int | None = None,
    model_sha256: str | None = None,
    limit: int = 50,
) -> dict[str, object]:
    current = latest_session_id(conn)
    if current is None:
        raise ComparisonError("no captured sessions exist")
    return compare_sessions(
        conn,
        current,
        against_session_id,
        model_sha256=model_sha256,
        limit=limit,
    )
