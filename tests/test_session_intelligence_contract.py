"""Functional contracts for evidence-scoped cross-session deltas."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.classification import classify_session
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.parser.service import parse_session
from ck3chronicle.session_intelligence import compare_sessions

from foundation_oracle import SIX_LOG_BYTES, write_logs
from test_classification_persistence_contract import _classifier, _session


CURRENT_ERROR_LOG = (
    b"[12:00:00][E][pdx_persistent_reader.cpp:1]: Error: \""
    b"Unknown trigger: replacement_key, near line: 99"
    b"\" in file: events/changed.txt line: 100\n"
    b"[12:00:01][E][jomini_script_system.cpp:2]: Script system error! Error: "
    b"scope:actor.target trigger [ Entirely novel semantic cause ]\n"
    b"[12:00:02][E][databases.h:3]: Key poet not found at Database: common/traits\n"
    b"[12:00:03][E][databases.h:4]: Key poet not found at Database: common/culture\n"
)

DIV_ZERO_OLD = (
    b"[12:00:00][E][jomini_scriptvalue.cpp:244]: Div/0 near file: "
    b"common/character_interactions/example.txt line: 3572 "
    b"(contract_assistance_interaction:ai_accept)\n"
)
DIV_ZERO_NEW = (
    b"[12:00:00][E][jomini_scriptvalue.cpp:244]: Div/0 near file: "
    b"common/character_interactions/renamed.txt line: 9999 "
    b"(contract_assistance_interaction:ai_accept:add)\n"
)


def _two_sessions(tmp_path):
    runtime, _captured, conn, previous_id = _session(tmp_path)
    classify_session(conn, previous_id, _classifier())

    logs = tmp_path / "live-logs"
    files = dict(SIX_LOG_BYTES)
    files["error.log"] = CURRENT_ERROR_LOG
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    current_id, _duplicate = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at="2026-08-13T01:00:00+00:00",
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness="complete",
        files=captured.files,
    )
    parse_session(conn, runtime, current_id)
    classify_session(conn, current_id, _classifier())
    return runtime, conn, previous_id, current_id


def _capture_classified(
    tmp_path,
    runtime,
    conn,
    name: str,
    error_log: bytes,
    captured_at: str,
) -> int:
    logs = tmp_path / name
    files = dict(SIX_LOG_BYTES)
    files["error.log"] = error_log
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    session_id, _duplicate = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at=captured_at,
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness="complete",
        files=captured.files,
    )
    parse_session(conn, runtime, session_id)
    classify_session(conn, session_id, _classifier())
    return session_id


def test_rdelta_001_contracts_ignore_changed_keys_locators_and_line_numbers(
    tmp_path,
) -> None:
    _runtime, conn, previous_id, current_id = _two_sessions(tmp_path)

    result = compare_sessions(conn, current_id)

    assert result["schema"] == "ck3chronicle.session-comparison"
    assert result["schema_version"] == 1
    assert result["comparison_basis"] == "observed_semantic_occurrence_counts"
    assert result["previous_session"]["session_id"] == previous_id
    assert result["current_session"]["session_id"] == current_id
    assert result["summary"] == {
        "previous_occurrences": 5,
        "current_occurrences": 4,
        "net_change": -1,
        "previous_rate_per_observed_hour": 9000.0,
        "current_rate_per_observed_hour": 4800.0,
        "rate_delta_per_observed_hour": -4200.0,
        "pattern_counts": {
            "new": 1,
            "fixed": 1,
            "worse": 0,
            "improved": 1,
            "unchanged": 1,
        },
        "occurrence_movement": {
            "introduced": 2,
            "eliminated": 1,
            "increased": 0,
            "reduced": 2,
        },
    }
    changed = {item["status"]: item for item in result["changed_patterns"]}
    assert changed["new"]["template"] == "Key poet not found at Database : <LOCATOR>"
    assert changed["new"]["current_occurrences"] == 2
    assert changed["fixed"]["template"] == (
        "Duplicate localization key . Key ' <PARAM> ' is defined in both "
        "<LOCATOR> and <LOCATOR> ."
    )
    assert changed["improved"]["template"] == "Unknown trigger : <KEY>"
    assert changed["improved"]["previous_occurrences"] == 3
    assert changed["improved"]["current_occurrences"] == 1
    assert result["unchanged_patterns_total"] == 1
    assert result["unchanged_patterns"][0]["assignment_level"] == "l1"
    assert result["evidence_quality"] == {
        "previous": {
            "source_blocks": 3,
            "first_error_time": "12:00:00",
            "last_error_time": "12:00:02",
            "observed_error_span_seconds": 2,
            "semantic_occurrences_per_observed_hour": 9000.0,
            "exact_100000_source_blocks": False,
        },
        "current": {
            "source_blocks": 4,
            "first_error_time": "12:00:00",
            "last_error_time": "12:00:03",
            "observed_error_span_seconds": 3,
            "semantic_occurrences_per_observed_hour": 4800.0,
            "exact_100000_source_blocks": False,
        },
        "warnings": [],
    }
    conn.close()


def test_rdelta_002_compare_cli_selects_latest_and_previous_by_capture_time(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, previous_id, current_id = _two_sessions(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(["compare", "--limit", "2", "--json"])

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["previous_session"]["session_id"] == previous_id
    assert payload["current_session"]["session_id"] == current_id
    assert payload["changed_patterns_total"] == 3
    assert len(payload["changed_patterns"]) == 2


def test_rdelta_003_trailing_script_location_cannot_split_a_residual(
    tmp_path,
) -> None:
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    conn = repository.open_db(runtime / "ck3chronicle.db")
    previous_id = _capture_classified(
        tmp_path,
        runtime,
        conn,
        "old-logs",
        DIV_ZERO_OLD,
        "2026-08-13T00:00:00+00:00",
    )
    current_id = _capture_classified(
        tmp_path,
        runtime,
        conn,
        "new-logs",
        DIV_ZERO_NEW,
        "2026-08-13T01:00:00+00:00",
    )

    result = compare_sessions(conn, current_id, previous_id)

    assert result["changed_patterns_total"] == 0
    assert result["unchanged_patterns_total"] == 1
    assert result["summary"]["pattern_counts"] == {
        "new": 0,
        "fixed": 0,
        "worse": 0,
        "improved": 0,
        "unchanged": 1,
    }
    assert result["unchanged_patterns"][0]["assignment_level"] == "unknown"
    conn.close()
