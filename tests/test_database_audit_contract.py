"""Real-shape contracts for the read-only database audit boundary."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.cli import build_parser
from ck3chronicle.database_audit import audit_database
from ck3chronicle.db import repository

from test_triage_contract import _triage_sessions


def _auditable_runtime(tmp_path):
    runtime, conn, previous_id, current_id, _target = _triage_sessions(tmp_path)
    repository.record_capture_observation(
        conn,
        session_id=previous_id,
        trigger="process_exit",
        process_name="ck3.exe",
        observed_at="2026-08-14T00:00:00+00:00",
    )
    repository.record_capture_observation(
        conn,
        session_id=current_id,
        trigger="process_exit",
        process_name="ck3.exe",
        observed_at="2026-08-14T01:00:00+00:00",
    )
    return runtime, conn, previous_id, current_id


def test_rdbaudit_001_consistent_archive_and_canonical_rows_pass(tmp_path) -> None:
    runtime, conn, _previous_id, _current_id = _auditable_runtime(tmp_path)
    conn.close()

    result = audit_database(runtime, deep=True)

    assert result["schema"] == "ck3chronicle.database-audit"
    assert result["schema_version"] == 1
    assert result["status"] == "pass"
    assert result["read_only"] is True
    assert result["audit_depth"] == "deep"
    assert result["summary"]["registered_sessions"] == 2
    assert result["summary"]["archive_directories"] == 2
    assert result["summary"]["pending_directories"] == 0
    assert result["summary"]["source_blocks"] == 4
    assert result["summary"]["raw_timestamp_headers"] == 4
    assert result["summary"]["occurrences"] == 4
    assert result["findings"] == []


def test_rdbaudit_002_parser_counter_corruption_is_detected(tmp_path) -> None:
    runtime, conn, _previous_id, current_id = _auditable_runtime(tmp_path)
    conn.execute(
        "UPDATE sessions SET parse_source_blocks = parse_source_blocks + 1 "
        "WHERE session_id = ?",
        (current_id,),
    )
    conn.commit()
    conn.close()

    result = audit_database(runtime)

    assert result["status"] == "fail"
    parse_findings = [
        item for item in result["findings"] if item["code"] == "DB-PARSE-001"
    ]
    assert len(parse_findings) == 1
    assert parse_findings[0]["session_ids"] == [current_id]


def test_rdbaudit_003_unregistered_archive_is_visible_but_repairable(
    tmp_path,
) -> None:
    runtime, conn, _previous_id, _current_id = _auditable_runtime(tmp_path)
    conn.close()
    orphan = runtime / "sessions" / ("f" * 64)
    orphan.mkdir()
    (orphan / "manifest.json").write_text("{}", encoding="utf-8")

    result = audit_database(runtime)

    assert result["status"] == "warning"
    finding = next(
        item for item in result["findings"] if item["code"] == "DB-INDEX-001"
    )
    assert finding["details"]["count"] == 1
    assert finding["details"]["hashes"] == ["f" * 64]


def test_rdbaudit_004_cli_json_is_bounded_and_read_only(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, _previous_id, _current_id = _auditable_runtime(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(["audit-db", "--json"])

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "pass"
    assert payload["read_only"] is True
    assert payload["audit_depth"] == "standard"
    assert len(payload["sessions"]) == 2


def test_rdbaudit_005_runtime_block_hash_corruption_is_detected(tmp_path) -> None:
    runtime, conn, _previous_id, current_id = _auditable_runtime(tmp_path)
    conn.execute(
        "UPDATE session_runtime_contexts SET block_sha256 = ? WHERE session_id = ?",
        ("0" * 64, current_id),
    )
    conn.commit()
    conn.close()

    result = audit_database(runtime)

    assert result["status"] == "fail"
    finding = next(
        item for item in result["findings"] if item["code"] == "DB-CONTEXT-003"
    )
    assert finding["session_ids"] == [current_id]
