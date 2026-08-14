"""Functional command contracts for report, latest, and errors."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.classification import classify_session
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository

from test_classification_persistence_contract import _classifier, _session


def _ready(tmp_path, monkeypatch):
    runtime, _captured, conn, session_id = _session(tmp_path)
    classify_session(conn, session_id, _classifier())
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    return build_parser(), session_id


def test_rreportcli_001_report_json_exposes_evidence_and_review_state(
    tmp_path, monkeypatch, capsys
) -> None:
    parser, session_id = _ready(tmp_path, monkeypatch)
    args = parser.parse_args(
        ["report", "--session", str(session_id), "--limit", "5", "--json"]
    )

    assert args.func(args) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["schema"] == "ck3chronicle.command-result"
    assert envelope["command"] == "report"
    assert envelope["status"] == "succeeded"
    payload = envelope["result"]
    assert payload["schema"] == "ck3chronicle.session-report"
    assert payload["session"]["session_id"] == session_id
    assert payload["classification"]["review_required"] == 1
    assert payload["top_patterns"][0]["template"] == "Unknown trigger : <KEY>"


def test_rreportcli_002_latest_reports_latest_captured_session(
    tmp_path, monkeypatch, capsys
) -> None:
    parser, session_id = _ready(tmp_path, monkeypatch)
    args = parser.parse_args(["latest", "--json"])

    assert args.func(args) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["command"] == "latest"
    payload = envelope["result"]
    assert payload["session"]["session_id"] == session_id


def test_rreportcli_003_errors_is_a_bounded_stored_pattern_projection(
    tmp_path, monkeypatch, capsys
) -> None:
    parser, session_id = _ready(tmp_path, monkeypatch)
    args = parser.parse_args(
        ["errors", "--session", str(session_id), "--limit", "2", "--json"]
    )

    assert args.func(args) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["command"] == "errors"
    payload = envelope["result"]
    assert payload["schema"] == "ck3chronicle.errors"
    assert payload["schema_version"] == 1
    assert payload["session_id"] == session_id
    assert payload["total_occurrences"] == 5
    assert len(payload["patterns"]) == 2
    assert payload["patterns"][0]["occurrences"] == 3


def test_rreportcli_004_exact_run_selection_survives_evidence_reuse(
    tmp_path, monkeypatch, capsys
) -> None:
    parser, session_id = _ready(tmp_path, monkeypatch)
    runtime = config.ROOT_CK3CHRONICLE
    conn = repository.open_db(runtime / "ck3chronicle.db")
    first_id, _ = repository.register_run(
        conn,
        session_id=session_id,
        capture_id="first-observed-run",
        trigger="process_exit",
        observed_ended_at="2026-08-14T01:00:00+00:00",
    )
    second_id, _ = repository.register_run(
        conn,
        session_id=session_id,
        capture_id="second-observed-run",
        trigger="process_exit",
        observed_ended_at="2026-08-14T02:00:00+00:00",
    )
    conn.close()

    exact = parser.parse_args(["report", "--run", str(first_id), "--json"])
    assert exact.func(exact) == 0
    exact_payload = json.loads(capsys.readouterr().out)["result"]
    assert exact_payload["schema_version"] == 5
    assert exact_payload["run"]["run_id"] == first_id
    assert exact_payload["run"]["capture_id"] == "first-observed-run"

    by_evidence = parser.parse_args(
        ["report", "--session", str(session_id), "--json"]
    )
    assert by_evidence.func(by_evidence) == 0
    evidence_payload = json.loads(capsys.readouterr().out)["result"]
    assert evidence_payload["run"]["run_id"] == second_id
    assert evidence_payload["run"]["capture_id"] == "second-observed-run"


def test_rreportcli_005_json_failure_uses_the_common_command_envelope(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    conn = repository.open_db(runtime / "ck3chronicle.db")
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(
        ["report", "--session", "999", "--json"]
    )

    assert args.func(args) == 2
    streams = capsys.readouterr()
    payload = json.loads(streams.out)
    assert streams.err == ""
    assert payload["schema"] == "ck3chronicle.command-result"
    assert payload["command"] == "report"
    assert payload["status"] == "failed"
    assert payload["exit_code"] == 2
    assert payload["result"] is None
    assert payload["error"]["code"] == "report_unavailable"
    assert payload["error"]["stage"] == "report"
