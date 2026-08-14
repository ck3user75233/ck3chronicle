"""Fresh reboot acceptance tests for immutable canonical source blocks."""
from __future__ import annotations

from pathlib import Path
import sqlite3

import pytest

from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.parser.log_blocks import iter_log_blocks
from ck3chronicle.parser.service import ErrorLogEvidenceError, parse_session

from foundation_oracle import (
    LEXICAL_BLOCK_ORACLE,
    LEXICAL_ERROR_BYTES,
    SIX_LOG_BYTES,
    write_logs,
)


def _registered_session(tmp_path: Path, error_bytes: bytes):
    logs = tmp_path / "live-logs"
    runtime = tmp_path / "runtime"
    files = dict(SIX_LOG_BYTES)
    files["error.log"] = error_bytes
    # This debug line deliberately resembles a timestamped error. It must not
    # enter the canonical error occurrence stream.
    files["debug.log"] = b"[12:00:09][E][debug_only.cpp:1]: Not canonical\n"
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    conn = repository.open_db(runtime / "ck3chronicle.db")
    session_id, was_existing = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at="2026-08-13T00:00:00+00:00",
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness="complete",
        files=captured.files,
    )
    assert was_existing is False
    return runtime, captured, conn, session_id


def test_rparse_001_lexical_blocks_match_literal_byte_oracle(tmp_path: Path) -> None:
    """Oracle: exact byte spans, hashes, lines, and IDs were frozen independently."""
    path = tmp_path / "error.log"
    path.write_bytes(LEXICAL_ERROR_BYTES)
    blocks = list(iter_log_blocks(path, log_relpath="error.log"))

    assert len(blocks) == 3
    for block, expected in zip(blocks, LEXICAL_BLOCK_ORACLE, strict=True):
        assert block.line_number == expected["start_line"]
        assert block.end_line == expected["end_line"]
        assert block.raw_byte_length == expected["bytes"]
        assert block.raw_block_sha256 == expected["raw_sha256"]
        assert block.source_block_id == expected["source_block_id"]
        assert block.timestamp == expected["timestamp"]
        assert block.level == expected["level"]
        assert block.source_family == expected["source_family"]

    assert b"".join(block.raw_block.encode("utf-8") for block in blocks) == LEXICAL_ERROR_BYTES


def test_rparse_002_only_error_log_blocks_enter_canonical_storage(
    tmp_path: Path,
) -> None:
    """Oracle: two timestamped error blocks become two ordered source rows."""
    runtime, _captured, conn, session_id = _registered_session(
        tmp_path, LEXICAL_ERROR_BYTES
    )
    result = parse_session(conn, runtime, session_id)

    assert result.counters.as_dict() == {
        "source_blocks": 2,
        "preamble_blocks": 1,
        "issue_occurrences": 2,
        "issue_clusters": 2,
        "unclassified_occurrences": 2,
        "multi_issue_blocks": 0,
        "silently_dropped_blocks": 0,
    }
    rows = conn.execute(
        """
        SELECT sb.log_relpath, sb.start_line, sb.end_line, sb.source_family,
               rb.raw_block_sha256, rb.raw_byte_length, rb.raw_block,
               sb.issue_count
        FROM source_blocks sb
        JOIN raw_block_contents rb
          ON rb.raw_block_pk = sb.raw_block_pk
        WHERE sb.session_id = ?
        ORDER BY sb.start_line
        """,
        (session_id,),
    ).fetchall()
    assert [tuple(row) for row in rows] == [
        (
            "error.log",
            2,
            3,
            "first.cpp",
            LEXICAL_BLOCK_ORACLE[1]["raw_sha256"],
            62,
            "[12:00:00][E][first.cpp:10]: First semantic 'alpha'\r\ndetail A\n",
            1,
        ),
        (
            "error.log",
            4,
            4,
            "second.cpp",
            LEXICAL_BLOCK_ORACLE[2]["raw_sha256"],
            45,
            "[12:00:01][W][second.cpp:20]: Second semantic",
            1,
        ),
    ]
    assert conn.execute(
        "SELECT COUNT(*) FROM source_blocks WHERE source_family = 'debug_only.cpp'"
    ).fetchone()[0] == 0
    conn.close()


def test_rparse_003_empty_error_log_is_an_explicit_zero_block_success(
    tmp_path: Path,
) -> None:
    """Oracle: present zero-byte evidence succeeds and persists zero counters."""
    runtime, _captured, conn, session_id = _registered_session(tmp_path, b"")
    result = parse_session(conn, runtime, session_id)

    assert result.counters.as_dict() == {
        "source_blocks": 0,
        "preamble_blocks": 0,
        "issue_occurrences": 0,
        "issue_clusters": 0,
        "unclassified_occurrences": 0,
        "multi_issue_blocks": 0,
        "silently_dropped_blocks": 0,
    }
    session = repository.get_session(conn, session_id)
    assert session["parse_status"] == "succeeded"
    conn.close()


def test_rparse_004_missing_archived_error_log_fails_without_canonical_rows(
    tmp_path: Path,
) -> None:
    """Oracle: a missing retained artifact is corruption, never an empty parse."""
    runtime, captured, conn, session_id = _registered_session(
        tmp_path, LEXICAL_ERROR_BYTES
    )
    (captured.dest_dir / "error.log").unlink()

    with pytest.raises(ErrorLogEvidenceError, match="missing"):
        parse_session(conn, runtime, session_id)

    assert conn.execute(
        "SELECT COUNT(*) FROM source_blocks WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 0
    assert repository.get_session(conn, session_id)["parse_status"] == "not_started"
    conn.close()


def test_rparse_005_identical_blocks_share_one_lossless_content_row(
    tmp_path: Path,
) -> None:
    """Oracle: two occurrences remain distinct while exact raw bytes are stored once."""
    repeated = b"[12:00:00][E][same.cpp:1]: Repeated diagnostic\n"
    runtime, _captured, conn, session_id = _registered_session(
        tmp_path, repeated + repeated
    )

    parse_session(conn, runtime, session_id)

    assert conn.execute(
        "SELECT COUNT(*) FROM source_blocks WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 2
    assert conn.execute("SELECT COUNT(*) FROM raw_block_contents").fetchone()[0] == 1
    assert conn.execute(
        "SELECT COUNT(*) FROM issue_occurrences WHERE session_id = ?", (session_id,)
    ).fetchone()[0] == 2
    assert "raw_block" not in {
        row[1] for row in conn.execute("PRAGMA table_info(source_blocks)")
    }
    assert "raw_block" not in {
        row[1] for row in conn.execute("PRAGMA table_info(issue_occurrences)")
    }
    stored = conn.execute(
        "SELECT raw_block FROM raw_block_contents"
    ).fetchone()[0]
    assert stored.encode("utf-8") == repeated
    conn.close()


def test_rparse_006_parser_uses_incremental_repository_boundary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Development guard: the service must not rebuild whole-session lists."""
    runtime, _captured, conn, session_id = _registered_session(
        tmp_path, LEXICAL_ERROR_BYTES
    )

    def reject_legacy_batch(*_args, **_kwargs):
        raise AssertionError("legacy whole-session replacement was called")

    monkeypatch.setattr(repository, "replace_canonical_parse", reject_legacy_batch)
    result = parse_session(conn, runtime, session_id)

    assert result.counters.source_blocks == 2
    assert result.counters.issue_occurrences == 2
    conn.close()


def test_rparse_007_nonsemantic_preamble_can_be_a_bounded_marker(
    tmp_path: Path,
) -> None:
    """Malformed headerless input need not be retained merely to count preamble."""
    path = tmp_path / "error.log"
    path.write_bytes(b"not a CK3 header\n" * 10_000)

    blocks = list(
        iter_log_blocks(path, log_relpath="error.log", retain_preamble=False)
    )

    assert len(blocks) == 1
    assert blocks[0].timestamp is None
    assert blocks[0].line_number == 1
    assert blocks[0].end_line == 10_000
    assert blocks[0].raw_block == ""
    assert blocks[0].continuation_lines == []


def _canonical_snapshot(conn: sqlite3.Connection, session_id: int) -> tuple:
    session = tuple(
        conn.execute(
            """
            SELECT parse_status, parser_contract_version, parse_source_blocks,
                   parse_preamble_blocks, parse_issue_occurrences,
                   parse_issue_clusters, parse_unclassified_occurrences,
                   parse_multi_issue_blocks, parse_silently_dropped_blocks
            FROM sessions WHERE session_id = ?
            """,
            (session_id,),
        ).fetchone()
    )
    blocks = tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT sb.source_block_pk, sb.start_line, sb.end_line, sb.issue_count,
                   rb.raw_block_sha256, rb.raw_block
            FROM source_blocks sb
            JOIN raw_block_contents rb ON rb.raw_block_pk = sb.raw_block_pk
            WHERE sb.session_id = ? ORDER BY sb.start_line
            """,
            (session_id,),
        ).fetchall()
    )
    issues = tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT issue_id, signature, category, occurrence_count
            FROM issues WHERE session_id = ? ORDER BY issue_id
            """,
            (session_id,),
        ).fetchall()
    )
    occurrences = tuple(
        tuple(row)
        for row in conn.execute(
            """
            SELECT issue_occurrence_id, signature, source_block_pk,
                   issue_ordinal, line_number
            FROM issue_occurrences WHERE session_id = ?
            ORDER BY issue_occurrence_id
            """,
            (session_id,),
        ).fetchall()
    )
    return session, blocks, issues, occurrences


def test_rparse_008_failed_streaming_reparse_restores_prior_rows(
    tmp_path: Path,
) -> None:
    """Injected failure after one new block leaves the accepted parse unchanged."""
    runtime, _captured, conn, session_id = _registered_session(
        tmp_path, LEXICAL_ERROR_BYTES
    )
    parse_session(conn, runtime, session_id)
    before = _canonical_snapshot(conn, session_id)
    conn.execute(
        f"""
        CREATE TEMP TRIGGER fail_second_streamed_block
        BEFORE INSERT ON source_blocks
        WHEN NEW.session_id = {session_id} AND NEW.start_line = 4
        BEGIN
            SELECT RAISE(ABORT, 'injected streamed-block failure');
        END
        """
    )

    with pytest.raises(sqlite3.IntegrityError, match="streamed-block failure"):
        parse_session(conn, runtime, session_id, reparse=True)

    assert _canonical_snapshot(conn, session_id) == before
    conn.close()


def test_rparse_009_postvalidate_rejects_equal_row_but_wrong_distribution(
    tmp_path: Path,
) -> None:
    """Persisted totals alone cannot hide a corrupted per-block distribution."""
    runtime, _captured, conn, session_id = _registered_session(
        tmp_path, LEXICAL_ERROR_BYTES
    )
    parse_session(conn, runtime, session_id)
    before = _canonical_snapshot(conn, session_id)
    conn.execute(
        f"""
        CREATE TEMP TRIGGER corrupt_first_block_count
        AFTER INSERT ON source_blocks
        WHEN NEW.session_id = {session_id} AND NEW.start_line = 4
        BEGIN
            UPDATE source_blocks
            SET issue_count = issue_count + 1
            WHERE session_id = NEW.session_id AND start_line = 2;
        END
        """
    )

    with pytest.raises(ValueError, match="persisted canonical totals disagree"):
        parse_session(conn, runtime, session_id, reparse=True)

    assert _canonical_snapshot(conn, session_id) == before
    conn.close()
