"""Functional contracts for the deferred processing workflow."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.cli import build_parser
from ck3chronicle.harvester import spool_logs
from ck3chronicle.processing import process_pending

from foundation_oracle import SIX_LOG_BYTES, write_logs
from test_classification_persistence_contract import _classifier


def test_rprocess_001_pending_to_report_is_complete_and_idempotent(tmp_path) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)

    first = process_pending(runtime, _classifier())

    assert first.finalized_pending == 1
    assert first.registered_archives == 1
    assert first.parsed_sessions == 1
    assert first.classified_sessions == 1
    assert first.reconciliation_errors == ()
    assert first.latest_report is not None
    assert first.latest_report["session"]["session_id"] == 1
    assert first.latest_report["classification"]["semantic_occurrences"] == 1

    second = process_pending(runtime, _classifier())

    assert second.finalized_pending == 0
    assert second.registered_archives == 0
    assert second.parsed_sessions == 0
    assert second.classified_sessions == 0
    assert second.reconciliation_errors == ()
    assert second.latest_report == first.latest_report


def test_rprocess_002_cli_json_reports_each_completed_stage(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(["process-pending", "--json"])

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "ck3chronicle.processing-result"
    assert payload["schema_version"] == 1
    assert payload["finalized_pending"] == 1
    assert payload["registered_archives"] == 1
    assert payload["parsed_sessions"] == 1
    assert payload["classified_sessions"] == 1
    assert payload["reconciliation_errors"] == []
    assert payload["latest_report"]["session"]["session_id"] == 1
