"""Functional command contracts for report, latest, and errors."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.classification import classify_session
from ck3chronicle.cli import build_parser

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
    payload = json.loads(capsys.readouterr().out)
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
    payload = json.loads(capsys.readouterr().out)
    assert payload["session"]["session_id"] == session_id


def test_rreportcli_003_errors_is_a_bounded_stored_pattern_projection(
    tmp_path, monkeypatch, capsys
) -> None:
    parser, session_id = _ready(tmp_path, monkeypatch)
    args = parser.parse_args(
        ["errors", "--session", str(session_id), "--limit", "2", "--json"]
    )

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "ck3chronicle.errors"
    assert payload["schema_version"] == 1
    assert payload["session_id"] == session_id
    assert payload["total_occurrences"] == 5
    assert len(payload["patterns"]) == 2
    assert payload["patterns"][0]["occurrences"] == 3
