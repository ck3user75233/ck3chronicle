"""Deterministic, evidence-scoped comparisons between classified sessions."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json
import sqlite3

from .db import repository
from .reporting import latest_session_id


class ComparisonError(RuntimeError):
    """A requested comparison cannot be made from compatible stored evidence."""


class PolicyError(RuntimeError):
    """A baseline or ignore policy request is invalid or conflicts with state."""


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


def _clean_text(value: str, label: str, *, maximum: int) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise PolicyError(f"{label} must not be empty")
    if len(cleaned) > maximum:
        raise PolicyError(f"{label} must be at most {maximum} characters")
    return cleaned


def create_baseline(
    conn: sqlite3.Connection,
    baseline_name: str,
    session_id: int,
    *,
    model_sha256: str | None = None,
    note: str | None = None,
) -> dict[str, object]:
    """Create an immutable named pointer to one session/model interpretation."""
    name = _clean_text(baseline_name, "baseline name", maximum=80)
    clean_note = _clean_text(note, "baseline note", maximum=500) if note else None
    session = repository.get_session(conn, session_id)
    if session is None:
        raise PolicyError(f"session_id {session_id} not found")
    run = _classification_run(conn, session_id, model_sha256)
    if run is None:
        raise PolicyError(f"session_id {session_id} has no compatible classification run")
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            """
            INSERT INTO session_baselines (
                baseline_name, session_id, model_sha256, created_at, note
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (name, session_id, run["model_sha256"], created_at, clean_note),
        )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        conn.rollback()
        raise PolicyError(f"baseline already exists: {name}") from exc
    except Exception:
        conn.rollback()
        raise
    return {
        "baseline_name": name,
        "session_id": session_id,
        "model_sha256": run["model_sha256"],
        "created_at": created_at,
        "note": clean_note,
    }


def get_baseline(conn: sqlite3.Connection, baseline_name: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM session_baselines WHERE baseline_name = ?",
        (baseline_name,),
    ).fetchone()


def list_baselines(conn: sqlite3.Connection) -> list[dict[str, object]]:
    return [
        dict(row)
        for row in conn.execute(
            """
            SELECT b.baseline_name, b.session_id, s.created_at AS captured_at,
                   b.model_sha256, b.created_at, b.note
            FROM session_baselines b
            JOIN sessions s ON s.session_id = b.session_id
            ORDER BY lower(b.baseline_name), b.baseline_name
            """
        ).fetchall()
    ]


def delete_baseline(conn: sqlite3.Connection, baseline_name: str) -> bool:
    try:
        conn.execute("BEGIN IMMEDIATE")
        deleted = conn.execute(
            "DELETE FROM session_baselines WHERE baseline_name = ?",
            (baseline_name,),
        ).rowcount
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return bool(deleted)


def previous_session_id(
    conn: sqlite3.Connection,
    session_id: int,
    *,
    model_sha256: str,
) -> int | None:
    """Return the preceding run's evidence session for the same exact model."""
    current = repository.get_session(conn, session_id)
    if current is None:
        raise ComparisonError(f"session_id {session_id} not found")
    observed = repository.latest_run_for_session(conn, session_id)
    if observed is not None:
        row = conn.execute(
            """
            SELECT co.session_id
            FROM capture_observations co
            JOIN classification_runs cr ON cr.session_id = co.session_id
            WHERE cr.model_sha256 = ?
              AND (
                  co.observed_ended_at < ?
                  OR (
                      co.observed_ended_at = ?
                      AND co.observation_id < ?
                  )
              )
            ORDER BY co.observed_ended_at DESC, co.observation_id DESC
            LIMIT 1
            """,
            (
                model_sha256,
                observed["observed_ended_at"],
                observed["observed_ended_at"],
                observed["observation_id"],
            ),
        ).fetchone()
        return int(row[0]) if row is not None else None

    # Compatibility for direct test/development registrations without a
    # watcher receipt. Production chronology is always run-based.
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


def assignment_pattern_id(
    contract_id: str | None,
    source_family: str,
    normalized_tokens_json: str,
) -> str:
    """Return the same stable identity used by reports, policy, and triage."""
    return _pattern_id(contract_id, source_family, normalized_tokens_json)


def _known_pattern_id(
    conn: sqlite3.Connection,
    model_sha256: str,
    pattern_id: str,
) -> bool:
    if conn.execute(
        """
        SELECT 1
        FROM classification_assignments ca
        JOIN classification_runs cr ON cr.run_id = ca.run_id
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        WHERE cr.model_sha256 = ? AND cp.contract_id = ?
        LIMIT 1
        """,
        (model_sha256, pattern_id),
    ).fetchone():
        return True
    if not pattern_id.startswith("r_"):
        return False
    rows = conn.execute(
        """
        SELECT DISTINCT cp.source_family, cp.normalized_tokens_json
        FROM classification_assignments ca
        JOIN classification_runs cr ON cr.run_id = ca.run_id
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        WHERE cr.model_sha256 = ? AND cp.contract_id IS NULL
        """,
        (model_sha256,),
    ).fetchall()
    return any(
        _pattern_id(None, row["source_family"], row["normalized_tokens_json"])
        == pattern_id
        for row in rows
    )


def ignore_pattern(
    conn: sqlite3.Connection,
    model_sha256: str,
    pattern_id: str,
    reason: str,
) -> dict[str, object]:
    """Attach a required human reason to a known model-bound pattern."""
    clean_pattern = _clean_text(pattern_id, "pattern ID", maximum=64)
    clean_reason = _clean_text(reason, "ignore reason", maximum=500)
    if repository.get_classification_model(conn, model_sha256) is None:
        raise PolicyError(f"classification model not found: {model_sha256}")
    if not _known_pattern_id(conn, model_sha256, clean_pattern):
        raise PolicyError(
            f"pattern {clean_pattern} is not present under model {model_sha256}"
        )
    created_at = datetime.now(timezone.utc).isoformat()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            """
            INSERT INTO ignored_patterns (
                model_sha256, pattern_id, reason, created_at
            ) VALUES (?, ?, ?, ?)
            """,
            (model_sha256, clean_pattern, clean_reason, created_at),
        )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        conn.rollback()
        raise PolicyError(f"pattern is already ignored: {clean_pattern}") from exc
    except Exception:
        conn.rollback()
        raise
    return {
        "model_sha256": model_sha256,
        "pattern_id": clean_pattern,
        "reason": clean_reason,
        "created_at": created_at,
    }


def list_ignored_patterns(
    conn: sqlite3.Connection,
    *,
    model_sha256: str | None = None,
) -> list[dict[str, object]]:
    if model_sha256 is None:
        rows = conn.execute(
            """
            SELECT * FROM ignored_patterns
            ORDER BY created_at, model_sha256, pattern_id
            """
        ).fetchall()
    else:
        rows = conn.execute(
            """
            SELECT * FROM ignored_patterns
            WHERE model_sha256 = ?
            ORDER BY created_at, pattern_id
            """,
            (model_sha256,),
        ).fetchall()
    return [dict(row) for row in rows]


def unignore_pattern(
    conn: sqlite3.Connection,
    model_sha256: str,
    pattern_id: str,
) -> bool:
    try:
        conn.execute("BEGIN IMMEDIATE")
        deleted = conn.execute(
            """
            DELETE FROM ignored_patterns
            WHERE model_sha256 = ? AND pattern_id = ?
            """,
            (model_sha256, pattern_id),
        ).rowcount
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return bool(deleted)


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
        SELECT MIN(cp.assignment_level) AS assignment_level,
               cp.contract_id,
               MIN(cp.source_family) AS source_family,
               MIN(cp.normalized_tokens_json) AS normalized_tokens_json,
               MIN(cp.l1_template) AS l1_template,
               MIN(cp.l2_template) AS l2_template,
               MIN(cc.template) AS catalog_template,
               MIN(cp.semantic_text) AS sample,
               COUNT(*) AS occurrences
        FROM classification_assignments ca
        JOIN classification_payloads cp ON cp.payload_pk = ca.payload_pk
        LEFT JOIN classification_contracts cc
          ON cc.model_sha256 = ?
         AND cc.contract_id = cp.contract_id
        WHERE ca.run_id = ?
        GROUP BY cp.contract_id,
                 CASE
                     WHEN cp.contract_id IS NULL THEN lower(cp.source_family)
                     ELSE NULL
                 END,
                 CASE
                     WHEN cp.contract_id IS NULL THEN cp.normalized_tokens_json
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


def _session_identity(
    session: sqlite3.Row, observed_run: sqlite3.Row | None = None
) -> dict[str, object]:
    identity = {
        "session_id": int(session["session_id"]),
        "captured_at": (
            observed_run["observed_ended_at"]
            if observed_run is not None
            else session["created_at"]
        ),
        "evidence_bundle_hash": session["evidence_bundle_hash"],
    }
    if observed_run is not None:
        identity.update(
            {
                "run_id": int(observed_run["observation_id"]),
                "capture_id": observed_run["capture_id"],
                "observed_started_at": observed_run["observed_started_at"],
                "observed_ended_at": observed_run["observed_ended_at"],
                "termination_kind": observed_run["termination_kind"],
            }
        )
    return identity


def _previous_observed_run(
    conn: sqlite3.Connection,
    current_run: sqlite3.Row,
    model_sha256: str,
) -> sqlite3.Row | None:
    return conn.execute(
        """
        SELECT co.*
        FROM capture_observations co
        JOIN classification_runs cr ON cr.session_id = co.session_id
        WHERE cr.model_sha256 = ?
          AND (
              co.observed_ended_at < ?
              OR (
                  co.observed_ended_at = ?
                  AND co.observation_id < ?
              )
          )
        ORDER BY co.observed_ended_at DESC, co.observation_id DESC
        LIMIT 1
        """,
        (
            model_sha256,
            current_run["observed_ended_at"],
            current_run["observed_ended_at"],
            current_run["observation_id"],
        ),
    ).fetchone()


def _clock_seconds(value: str) -> int:
    try:
        hours, minutes, seconds = (int(part) for part in value.split(":"))
    except (TypeError, ValueError) as exc:
        raise ComparisonError(f"stored source-block timestamp is invalid: {value}") from exc
    if not (0 <= hours <= 23 and 0 <= minutes <= 59 and 0 <= seconds <= 59):
        raise ComparisonError(f"stored source-block timestamp is invalid: {value}")
    return hours * 3600 + minutes * 60 + seconds


def _evidence_quality(
    conn: sqlite3.Connection,
    session: sqlite3.Row,
    run: sqlite3.Row,
) -> dict[str, object]:
    row = conn.execute(
        """
        SELECT COUNT(*) AS source_blocks,
               MIN(timestamp) AS first_error_time,
               MAX(timestamp) AS last_error_time
        FROM source_blocks
        WHERE session_id = ?
        """,
        (session["session_id"],),
    ).fetchone()
    source_blocks = int(row["source_blocks"])
    first = row["first_error_time"]
    last = row["last_error_time"]
    span: int | None = None
    rate: float | None = None
    if first is not None and last is not None:
        first_seconds = _clock_seconds(str(first))
        last_seconds = _clock_seconds(str(last))
        if last_seconds < first_seconds:
            last_seconds += 24 * 60 * 60
        span = last_seconds - first_seconds
        if span > 0:
            rate = int(run["semantic_occurrence_count"]) * 3600.0 / span
    return {
        "source_blocks": source_blocks,
        "first_error_time": first,
        "last_error_time": last,
        "observed_error_span_seconds": span,
        "semantic_occurrences_per_observed_hour": rate,
        "exact_100000_source_blocks": source_blocks == 100_000,
    }


def _runtime_context_delta(
    conn: sqlite3.Connection,
    previous_session_id: int,
    current_session_id: int,
) -> dict[str, object]:
    previous_context = repository.get_runtime_context(conn, previous_session_id)
    current_context = repository.get_runtime_context(conn, current_session_id)
    if previous_context is None or current_context is None:
        return {
            "available": False,
            "runtime_changed": None,
            "reason": "runtime context has not been processed for both sessions",
        }

    def entry(row: sqlite3.Row, order_column: str, key_column: str) -> dict[str, object]:
        return {
            "key": row[key_column],
            "display_name": row["display_name"],
            "order": int(row[order_column]),
            "mount_path": row["mount_path"],
        }

    def difference(
        previous_rows: list[sqlite3.Row],
        current_rows: list[sqlite3.Row],
        *,
        order_column: str,
        key_column: str,
    ) -> dict[str, object]:
        previous = {str(row[key_column]): row for row in previous_rows}
        current = {str(row[key_column]): row for row in current_rows}
        added = [
            entry(current[key], order_column, key_column)
            for key in sorted(current.keys() - previous.keys())
        ]
        removed = [
            entry(previous[key], order_column, key_column)
            for key in sorted(previous.keys() - current.keys())
        ]
        moved = [
            {
                "key": key,
                "display_name": current[key]["display_name"],
                "previous_order": int(previous[key][order_column]),
                "current_order": int(current[key][order_column]),
            }
            for key in sorted(previous.keys() & current.keys())
            if int(previous[key][order_column]) != int(current[key][order_column])
        ]
        previous_sequence = [str(row[key_column]) for row in previous_rows]
        current_sequence = [str(row[key_column]) for row in current_rows]
        return {
            "previous_count": len(previous_rows),
            "current_count": len(current_rows),
            "added": added,
            "removed": removed,
            "moved": moved,
            "order_changed": previous_sequence != current_sequence,
        }

    dlcs = difference(
        repository.get_mounted_dlcs(conn, previous_session_id),
        repository.get_mounted_dlcs(conn, current_session_id),
        order_column="dlc_order",
        key_column="dlc_key",
    )
    mods = difference(
        repository.get_mounted_mods(conn, previous_session_id),
        repository.get_mounted_mods(conn, current_session_id),
        order_column="load_order",
        key_column="mod_key",
    )
    return {
        "available": True,
        "runtime_changed": bool(dlcs["order_changed"] or mods["order_changed"]),
        "previous_status": previous_context["status"],
        "current_status": current_context["status"],
        "dlcs": dlcs,
        "active_mods": mods,
        "scope": "mounted identities and order; content updates are not fingerprinted",
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
    current_observed_run = repository.latest_run_for_session(
        conn, current_session_id
    )
    against_observed_run = None
    if against_session_id is None:
        if current_observed_run is not None:
            against_observed_run = _previous_observed_run(
                conn, current_observed_run, exact_model
            )
            if against_observed_run is not None:
                against_session_id = int(against_observed_run["session_id"])
        else:
            against_session_id = previous_session_id(
                conn,
                current_session_id,
                model_sha256=exact_model,
            )
        if against_session_id is None:
            raise ComparisonError("no preceding classified run exists")
    else:
        against_observed_run = repository.latest_run_for_session(
            conn, against_session_id
        )
    if against_session_id == current_session_id and (
        current_observed_run is None
        or against_observed_run is None
        or current_observed_run["observation_id"]
        == against_observed_run["observation_id"]
    ):
        raise ComparisonError("a run cannot be compared with itself")
    against_session = repository.get_session(conn, against_session_id)
    if against_session is None:
        raise ComparisonError(f"session_id {against_session_id} not found")
    against_run = _classification_run(conn, against_session_id, exact_model)
    if against_run is None:
        raise ComparisonError(
            f"session_id {against_session_id} has no run for model {exact_model}"
        )

    previous_quality = _evidence_quality(conn, against_session, against_run)
    current_quality = _evidence_quality(conn, current_session, current_run)
    previous_span = previous_quality["observed_error_span_seconds"]
    current_span = current_quality["observed_error_span_seconds"]
    previous_hours = (
        float(previous_span) / 3600.0
        if previous_span is not None and int(previous_span) > 0
        else None
    )
    current_hours = (
        float(current_span) / 3600.0
        if current_span is not None and int(current_span) > 0
        else None
    )
    ignored = {
        str(row["pattern_id"]): str(row["reason"])
        for row in conn.execute(
            """
            SELECT pattern_id, reason
            FROM ignored_patterns
            WHERE model_sha256 = ?
            """,
            (exact_model,),
        ).fetchall()
    }
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
                "ignored": pattern_id in ignored,
                "ignore_reason": ignored.get(pattern_id),
                "previous_rate_per_observed_hour": (
                    previous_count / previous_hours
                    if previous_hours is not None
                    else None
                ),
                "current_rate_per_observed_hour": (
                    current_count / current_hours if current_hours is not None else None
                ),
            }
        )
        previous_rate = comparison["previous_rate_per_observed_hour"]
        current_rate = comparison["current_rate_per_observed_hour"]
        comparison["rate_delta_per_observed_hour"] = (
            float(current_rate) - float(previous_rate)
            if previous_rate is not None and current_rate is not None
            else None
        )
        (unchanged if status == "unchanged" else changed).append(comparison)

    priority = {"new": 0, "fixed": 1, "worse": 2, "improved": 3}
    changed.sort(
        key=lambda item: (
            bool(item["ignored"]),
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
    ignored_changed = [item for item in changed if item["ignored"]]
    quality_warnings: list[str] = []
    for label, session, quality in (
        ("previous", against_session, previous_quality),
        ("current", current_session, current_quality),
    ):
        if quality["exact_100000_source_blocks"]:
            quality_warnings.append(
                f"{label} session {session['session_id']} contains exactly 100,000 "
                "source blocks; totals and rates may be censored"
            )
        if not quality["observed_error_span_seconds"]:
            quality_warnings.append(
                f"{label} session {session['session_id']} has no measurable error "
                "timestamp span; rate comparison is unavailable"
            )
    return {
        "schema": "ck3chronicle.session-comparison",
        "schema_version": 2,
        "comparison_basis": "observed_semantic_occurrence_counts",
        "model_sha256": exact_model,
        "previous_session": _session_identity(
            against_session, against_observed_run
        ),
        "current_session": _session_identity(
            current_session, current_observed_run
        ),
        "evidence_quality": {
            "previous": previous_quality,
            "current": current_quality,
            "warnings": quality_warnings,
        },
        "runtime_context_delta": _runtime_context_delta(
            conn,
            against_session_id,
            current_session_id,
        ),
        "summary": {
            "previous_occurrences": previous_total,
            "current_occurrences": current_total,
            "net_change": current_total - previous_total,
            "previous_rate_per_observed_hour": previous_quality[
                "semantic_occurrences_per_observed_hour"
            ],
            "current_rate_per_observed_hour": current_quality[
                "semantic_occurrences_per_observed_hour"
            ],
            "rate_delta_per_observed_hour": (
                float(current_quality["semantic_occurrences_per_observed_hour"])
                - float(previous_quality["semantic_occurrences_per_observed_hour"])
                if current_quality["semantic_occurrences_per_observed_hour"] is not None
                and previous_quality["semantic_occurrences_per_observed_hour"] is not None
                else None
            ),
            "pattern_counts": pattern_counts,
            "occurrence_movement": occurrence_movement,
            "policy": {
                "ignored_changed_patterns": len(ignored_changed),
                "actionable_changed_patterns": len(changed) - len(ignored_changed),
                "ignored_current_occurrences": sum(
                    int(item["current_occurrences"]) for item in ignored_changed
                ),
            },
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


def compare_against_baseline(
    conn: sqlite3.Connection,
    baseline_name: str,
    *,
    current_session_id: int | None = None,
    limit: int = 50,
) -> dict[str, object]:
    baseline = get_baseline(conn, baseline_name)
    if baseline is None:
        raise ComparisonError(f"baseline not found: {baseline_name}")
    current = current_session_id
    if current is None:
        current = latest_session_id(conn)
    if current is None:
        raise ComparisonError("no captured sessions exist")
    comparison = compare_sessions(
        conn,
        current,
        int(baseline["session_id"]),
        model_sha256=str(baseline["model_sha256"]),
        limit=limit,
    )
    comparison["baseline"] = {
        "baseline_name": baseline["baseline_name"],
        "session_id": int(baseline["session_id"]),
        "model_sha256": baseline["model_sha256"],
        "created_at": baseline["created_at"],
        "note": baseline["note"],
    }
    return comparison
