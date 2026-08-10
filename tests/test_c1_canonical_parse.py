"""Independent C1 acceptance tests for canonical parse persistence.

These tests exercise the public parse service and database state.  Expected
values come from literal evidence bytes and the Phase 1 contract; they do not
call Chronicle lexer, normalization, or persistence helpers to build oracles.
"""
from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pytest

from ck3chronicle.db import repository
from ck3chronicle.db.repository import add_session_file, create_session, open_db
from ck3chronicle.parser.service import (
    ErrorLogEvidenceError,
    parse_session,
)


EXACT_ERROR_LOG = (
    b"[10:00:01][E][localization.cpp:10]: Localization key 'ALPHA' not found.\r\n"
    b"[10:00:02][E][mystery.cpp:77]: Strange thing happened.\r\n"
    b"details remain here\r\n"
    b"[10:00:03][E][localization.cpp:10]: Localization key 'ALPHA' not found."
)


def _make_session(
    root: Path,
    files: dict[str, bytes],
    *,
    missing_from_snapshot: set[str] | None = None,
):
    """Create an ingested-session shape without invoking capture code."""
    missing_from_snapshot = missing_from_snapshot or set()
    conn = open_db(root / "ck3chronicle.db")
    bundle_hash = "a" * 64
    session_id = create_session(
        conn,
        bundle_hash,
        log_count=len(files),
        crash_present=False,
        total_bytes=sum(len(data) for data in files.values()),
    )
    snapshot = root / "sessions" / bundle_hash
    snapshot.mkdir(parents=True)
    for rel_path, data in files.items():
        add_session_file(
            conn,
            session_id,
            rel_path,
            hashlib.sha256(data).hexdigest(),
            len(data),
            "log",
        )
        if rel_path not in missing_from_snapshot:
            (snapshot / rel_path).write_bytes(data)
    # This is a parser-only fixture seam. Product code can reach finalized only
    # through verified capture registration.
    conn.execute(
        """
        UPDATE sessions
        SET capture_status='finalized',
            capture_manifest_version=1,
            capture_manifest_sha256=?
        WHERE session_id=?
        """,
        ("f" * 64, session_id),
    )
    conn.commit()
    return conn, session_id


def _canonical_export(conn, session_id: int) -> bytes:
    """Stable byte representation of every C1-owned persisted value."""
    session_columns = (
        "parse_status, parser_contract_version, parse_source_blocks, "
        "parse_preamble_blocks, parse_issue_occurrences, parse_issue_clusters, "
        "parse_unclassified_occurrences, parse_multi_issue_blocks, "
        "parse_silently_dropped_blocks"
    )
    payload: dict[str, object] = {
        "session": dict(
            conn.execute(
                f"SELECT {session_columns} FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        )
    }
    for table, order_by in (
        ("source_blocks", "source_block_id"),
        ("issues", "signature"),
        ("issue_occurrences", "source_block_id, issue_ordinal"),
    ):
        rows = conn.execute(
            f"SELECT * FROM {table} WHERE session_id = ? ORDER BY {order_by}",
            (session_id,),
        ).fetchall()
        payload[table] = [dict(row) for row in rows]
    return json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def test_parse_uses_only_captured_error_log(tmp_path: Path):
    conn, session_id = _make_session(
        tmp_path,
        {
            "error.log": b"[10:00:01][E][mystery.cpp:1]: error evidence\n",
            "debug.log": b"[10:00:02][E][mystery.cpp:2]: debug evidence\n",
            "game.log": b"[10:00:03][E][mystery.cpp:3]: game evidence\n",
        },
    )

    result = parse_session(conn, tmp_path, session_id)

    assert result.counters.source_blocks == 1
    assert {
        row[0]
        for row in conn.execute(
            "SELECT DISTINCT log_relpath FROM source_blocks WHERE session_id = ?",
            (session_id,),
        )
    } == {"error.log"}
    assert {
        row[0]
        for row in conn.execute(
            "SELECT DISTINCT log_relpath FROM issue_occurrences WHERE session_id = ?",
            (session_id,),
        )
    } == {"error.log"}
    conn.close()


def test_parse_missing_archived_error_log_fails_without_canonical_state(
    tmp_path: Path,
):
    conn, session_id = _make_session(
        tmp_path,
        {"error.log": b"[10:00:01][E][mystery.cpp:1]: missing\n"},
        missing_from_snapshot={"error.log"},
    )

    with pytest.raises(ErrorLogEvidenceError):
        parse_session(conn, tmp_path, session_id)

    session = conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    assert session["parse_status"] == "not_started"
    assert session["parser_contract_version"] is None
    assert session["parse_source_blocks"] is None
    assert conn.execute(
        "SELECT COUNT(*) FROM source_blocks WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 0
    assert conn.execute(
        "SELECT COUNT(*) FROM issues WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 0
    assert conn.execute(
        "SELECT COUNT(*) FROM issue_occurrences WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 0
    conn.close()


def test_manifest_hash_mismatch_fails_and_reparse_preserves_success(
    tmp_path: Path,
):
    conn, session_id = _make_session(tmp_path, {"error.log": EXACT_ERROR_LOG})
    parse_session(conn, tmp_path, session_id)
    before = _canonical_export(conn, session_id)
    session = repository.get_session(conn, session_id)
    archived = (
        tmp_path
        / "sessions"
        / session["evidence_bundle_hash"]
        / "error.log"
    )
    mutated = bytearray(EXACT_ERROR_LOG)
    mutated[-1] = ord("!")
    archived.write_bytes(bytes(mutated))

    with pytest.raises(ErrorLogEvidenceError, match="SHA-256"):
        parse_session(conn, tmp_path, session_id, reparse=True)

    assert _canonical_export(conn, session_id) == before
    conn.close()


def test_parse_zero_byte_error_log_commits_explicit_zero_parse(tmp_path: Path):
    conn, session_id = _make_session(tmp_path, {"error.log": b""})

    result = parse_session(conn, tmp_path, session_id)

    assert result.mutated is True
    assert result.counters.as_dict() == {
        "source_blocks": 0,
        "preamble_blocks": 0,
        "issue_occurrences": 0,
        "issue_clusters": 0,
        "unclassified_occurrences": 0,
        "multi_issue_blocks": 0,
        "silently_dropped_blocks": 0,
    }
    session = conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    assert session["parse_status"] == "succeeded"
    assert session["parser_contract_version"] == "1.0.0"
    assert session["parse_source_blocks"] == 0
    assert session["parse_silently_dropped_blocks"] == 0
    conn.close()


def test_malformed_preamble_long_line_invalid_utf8_and_no_final_newline_accounted(
    tmp_path: Path,
):
    long_continuation = b"x" * 100_000 + b"\xff\r\n"
    evidence = (
        b"\xef\xbb\xbfnot a timestamped header\r\n"
        b"[11:00:01][E][mystery.cpp:5]: first\n"
        + long_continuation
        + b"[11:00:02][E][mystery.cpp:6]: truncated final block"
    )
    conn, session_id = _make_session(tmp_path, {"error.log": evidence})

    result = parse_session(conn, tmp_path, session_id)

    assert result.counters.preamble_blocks == 1
    assert result.counters.source_blocks == 2
    assert result.counters.issue_occurrences == 2
    assert result.counters.silently_dropped_blocks == 0
    rows = conn.execute(
        """
        SELECT start_line, end_line, raw_byte_length, raw_block
        FROM source_blocks
        WHERE session_id = ?
        ORDER BY start_line
        """,
        (session_id,),
    ).fetchall()
    assert [(row["start_line"], row["end_line"]) for row in rows] == [(2, 3), (4, 4)]
    assert rows[0]["raw_byte_length"] == len(
        b"[11:00:01][E][mystery.cpp:5]: first\n" + long_continuation
    )
    assert "\ufffd" in rows[0]["raw_block"]
    assert not rows[1]["raw_block"].endswith(("\n", "\r"))
    conn.close()


def test_parse_persists_exact_source_blocks_and_reconciles_counts(tmp_path: Path):
    conn, session_id = _make_session(tmp_path, {"error.log": EXACT_ERROR_LOG})

    result = parse_session(conn, tmp_path, session_id)

    blocks = conn.execute(
        """
        SELECT source_block_id, start_line, end_line, timestamp, level,
               source_tag, source_family, raw_block_sha256, raw_byte_length,
               issue_count
        FROM source_blocks
        WHERE session_id = ?
        ORDER BY start_line
        """,
        (session_id,),
    ).fetchall()
    assert [tuple(row) for row in blocks] == [
        (
            "c3960651f20d5c7e9abdaf7866bd6cc9bb300507f35c6e81b41c8d5823a2fc99",
            1,
            1,
            "10:00:01",
            "E",
            "localization.cpp:10",
            "localization.cpp",
            "f9e46b58e3c0dcdb0b295d9ae61cf325420bf328d43fe8e7a429a213c91a034f",
            73,
            1,
        ),
        (
            "b425653a3c772e6598e50a355ad932dbd5fd686304aea37b8ad4c672209a0f93",
            2,
            3,
            "10:00:02",
            "E",
            "mystery.cpp:77",
            "mystery.cpp",
            "6bfa3ba80fbe845b74eba5a0135bfba1ce7affc18c98f7662dd34e34218a50d9",
            77,
            1,
        ),
        (
            "78d23a8207474d53b886b5d26c18955e9adda8e1163c2b08f7060d0701dea29d",
            4,
            4,
            "10:00:03",
            "E",
            "localization.cpp:10",
            "localization.cpp",
            "367d47fe7d77a3a9a9c40662c5bc77e4415b95bfc7298e809419a654ba6664e7",
            71,
            1,
        ),
    ]
    occurrences = conn.execute(
        """
        SELECT source_block_id, issue_ordinal,
               occurrence.occurrence_count AS occurrence_count, category
        FROM issue_occurrences AS occurrence
        JOIN issues USING (session_id, signature)
        WHERE occurrence.session_id = ?
        ORDER BY occurrence.line_number
        """,
        (session_id,),
    ).fetchall()
    assert [(row["issue_ordinal"], row["occurrence_count"]) for row in occurrences] == [
        (0, 1),
        (0, 1),
        (0, 1),
    ]
    assert [row["category"] for row in occurrences] == [
        "localization",
        "unclassified",
        "localization",
    ]
    assert len({row["source_block_id"] for row in occurrences}) == 3

    sums = conn.execute(
        """
        SELECT
          (SELECT COALESCE(SUM(issue_count), 0) FROM source_blocks WHERE session_id = ?) AS block_sum,
          (SELECT COUNT(*) FROM issue_occurrences WHERE session_id = ?) AS occurrence_rows,
          (SELECT COALESCE(SUM(occurrence_count), 0) FROM issues WHERE session_id = ?) AS cluster_sum
        """,
        (session_id, session_id, session_id),
    ).fetchone()
    assert tuple(sums) == (3, 3, 3)
    assert result.counters.issue_clusters == 2
    assert result.counters.unclassified_occurrences == 1
    assert result.counters.silently_dropped_blocks == 0
    conn.close()


def test_one_block_can_persist_multiple_ordered_issue_occurrences(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    from ck3chronicle.models.issue import IssueDraft
    from ck3chronicle.parser import service

    evidence = b"[12:00:01][E][compound.cpp:9]: compound evidence\n"
    conn, session_id = _make_session(tmp_path, {"error.log": evidence})

    def two_drafts(block):
        common = {
            "tags": [],
            "engine_source": block.source_tag,
            "primary_file": None,
            "primary_line": None,
            "referenced_symbols": [],
            "referenced_objects": [],
            "extra_json": {},
            "severity": "error",
            "confidence": "high",
            "raw_block": block.raw_block,
            "log_relpath": block.log_relpath,
            "line_number": block.line_number,
        }
        return [
            IssueDraft(
                category="event_system",
                error_type="first_issue",
                sample_message="first semantic issue",
                **common,
            ),
            IssueDraft(
                category="script_system",
                error_type="second_issue",
                sample_message="second semantic issue",
                **common,
            ),
        ]

    monkeypatch.setattr(service, "extract_block", two_drafts)
    result = parse_session(conn, tmp_path, session_id)

    assert result.counters.source_blocks == 1
    assert result.counters.issue_occurrences == 2
    assert result.counters.issue_clusters == 2
    assert result.counters.multi_issue_blocks == 1
    assert conn.execute(
        "SELECT issue_count FROM source_blocks WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 2
    ordinals = conn.execute(
        """
        SELECT issue_ordinal
        FROM issue_occurrences
        WHERE session_id = ?
        ORDER BY issue_ordinal
        """,
        (session_id,),
    ).fetchall()
    assert [row[0] for row in ordinals] == [0, 1]
    conn.close()


def test_replacement_validation_rejects_equal_total_distribution_swaps():
    """Global sums cannot conceal wrong per-block or per-signature counts."""
    from dataclasses import replace

    from ck3chronicle.models.issue import NormalizedIssue
    from ck3chronicle.models.parse import (
        ClusterRecord,
        OccurrenceRecord,
        ParseCounters,
        SourceBlockRecord,
    )

    def issue(signature: str, line: int) -> NormalizedIssue:
        return NormalizedIssue(
            signature=signature,
            message_template=signature,
            category="script_system",
            error_type=signature,
            tags=[],
            engine_source="test.cpp:1",
            sample_message=signature,
            primary_file=None,
            primary_line=None,
            referenced_symbols=[],
            referenced_objects=[],
            extra_json={},
            severity="error",
            confidence="high",
            raw_block=signature,
            log_relpath="error.log",
            line_number=line,
        )

    first = issue("first", 1)
    second = issue("second", 2)
    block_a = SourceBlockRecord(
        "a", "error.log", 1, 1, "12:00:01", "E", "test.cpp:1",
        "test.cpp", "a" * 64, 1, "a", 1,
    )
    block_b = SourceBlockRecord(
        "b", "error.log", 2, 2, "12:00:02", "E", "test.cpp:1",
        "test.cpp", "b" * 64, 1, "b", 2,
    )
    occurrences = [
        OccurrenceRecord("a", 0, first),
        OccurrenceRecord("b", 0, second),
        OccurrenceRecord("b", 1, second),
    ]
    clusters = [ClusterRecord(first, 1), ClusterRecord(second, 2)]
    counters = ParseCounters(2, 0, 3, 2, 0, 1, 0)

    with pytest.raises(ValueError, match="source-block issue count"):
        repository._validate_canonical_replacement(
            [replace(block_a, issue_count=2), replace(block_b, issue_count=1)],
            occurrences,
            clusters,
            counters,
        )

    with pytest.raises(ValueError, match="cluster counts"):
        repository._validate_canonical_replacement(
            [block_a, block_b],
            occurrences,
            [ClusterRecord(first, 2), ClusterRecord(second, 1)],
            counters,
        )


def test_parse_after_success_without_reparse_is_canonical_noop(tmp_path: Path):
    conn, session_id = _make_session(tmp_path, {"error.log": EXACT_ERROR_LOG})
    first = parse_session(conn, tmp_path, session_id)
    before = _canonical_export(conn, session_id)

    second = parse_session(conn, tmp_path, session_id)

    assert first.mutated is True
    assert second.mutated is False
    assert _canonical_export(conn, session_id) == before
    conn.close()


def test_reparse_failure_rolls_back_prior_canonical_export(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    conn, session_id = _make_session(tmp_path, {"error.log": EXACT_ERROR_LOG})
    parse_session(conn, tmp_path, session_id)
    before = _canonical_export(conn, session_id)
    original = repository._insert_occurrence
    calls = 0

    def fail_during_second_occurrence(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise RuntimeError("injected persistence failure")
        return original(*args, **kwargs)

    monkeypatch.setattr(repository, "_insert_occurrence", fail_during_second_occurrence)

    with pytest.raises(RuntimeError, match="injected persistence failure"):
        parse_session(conn, tmp_path, session_id, reparse=True)

    assert calls == 2
    assert _canonical_export(conn, session_id) == before
    conn.close()


def test_first_parse_failure_leaves_not_started_and_no_rows(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    conn, session_id = _make_session(tmp_path, {"error.log": EXACT_ERROR_LOG})

    def fail_first_occurrence(*args, **kwargs):
        raise RuntimeError("injected first-parse failure")

    monkeypatch.setattr(repository, "_insert_occurrence", fail_first_occurrence)

    with pytest.raises(RuntimeError, match="injected first-parse failure"):
        parse_session(conn, tmp_path, session_id)

    session = conn.execute(
        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
    ).fetchone()
    assert session["parse_status"] == "not_started"
    assert session["parser_contract_version"] is None
    assert all(
        conn.execute(
            f"SELECT COUNT(*) FROM {table} WHERE session_id = ?", (session_id,)
        ).fetchone()[0]
        == 0
        for table in ("source_blocks", "issues", "issue_occurrences")
    )
    conn.close()
