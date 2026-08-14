"""Functional contracts for the deferred processing workflow."""

from __future__ import annotations

import json
import sqlite3

from ck3chronicle import config
from ck3chronicle import processing
from ck3chronicle.cli import build_parser
from ck3chronicle.harvester import ArchiveIntegrityError, spool_logs
from ck3chronicle.processing import ProcessingResult, process_pending

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
    assert first.registered_runs == 1
    assert first.context_sessions == 1
    assert first.parsed_sessions == 1
    assert first.classified_sessions == 1
    assert first.reconciliation_errors == ()
    assert first.latest_report is not None
    assert first.latest_report["session"]["session_id"] == 1
    assert first.latest_report["classification"]["semantic_occurrences"] == 1
    assert first.latest_report["runtime_context"]["status"] == "absent"

    second = process_pending(runtime, _classifier())

    assert second.finalized_pending == 0
    assert second.registered_archives == 0
    assert second.registered_runs == 0
    assert second.context_sessions == 0
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
    assert payload["schema"] == "ck3chronicle.command-result"
    assert payload["schema_version"] == 1
    assert payload["command"] == "process-pending"
    assert payload["status"] == "succeeded"
    assert payload["exit_code"] == 0
    assert payload["error"] is None
    result = payload["result"]
    assert result["schema"] == "ck3chronicle.processing-result"
    assert result["schema_version"] == 2
    assert result["finalized_pending"] == 1
    assert result["registered_archives"] == 1
    assert result["registered_runs"] == 1
    assert result["context_sessions"] == 1
    assert result["parsed_sessions"] == 1
    assert result["classified_sessions"] == 1
    assert result["reconciliation_errors"] == []
    assert result["latest_report"]["session"]["session_id"] == 1


def _raise(exc: Exception):
    def raising(*_args, **_kwargs):
        raise exc

    return raising


def test_rprocess_003_json_failure_is_one_versioned_archive_envelope(
    tmp_path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", tmp_path)
    monkeypatch.setattr(
        processing,
        "process_pending",
        _raise(ArchiveIntegrityError("altered archived evidence")),
    )
    args = build_parser().parse_args(["process-pending", "--json"])

    assert args.func(args) == 3
    streams = capsys.readouterr()
    payload = json.loads(streams.out)
    assert streams.err == ""
    assert payload == {
        "schema": "ck3chronicle.command-result",
        "schema_version": 1,
        "command": "process-pending",
        "status": "failed",
        "exit_code": 3,
        "result": None,
        "error": {
            "code": "archive_integrity",
            "message": "altered archived evidence",
            "stage": "archive",
            "retryable": False,
        },
    }


def test_rprocess_004_json_database_failure_has_distinct_exit_contract(
    tmp_path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", tmp_path)
    monkeypatch.setattr(
        processing,
        "process_pending",
        _raise(sqlite3.DatabaseError("database is locked")),
    )
    args = build_parser().parse_args(["process-pending", "--json"])

    assert args.func(args) == 5
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "failed"
    assert payload["exit_code"] == 5
    assert payload["error"] == {
        "code": "database_failed",
        "message": "database is locked",
        "stage": "database",
        "retryable": False,
    }


def test_rprocess_005_reconciliation_warning_retains_partial_result(
    tmp_path, monkeypatch, capsys
) -> None:
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", tmp_path)
    monkeypatch.setattr(
        processing,
        "process_pending",
        lambda *_args, **_kwargs: ProcessingResult(
            finalized_pending=1,
            registered_archives=0,
            registered_runs=0,
            context_sessions=0,
            parsed_sessions=0,
            classified_sessions=0,
            reconciliation_errors=("orphan receipt",),
            latest_report=None,
        ),
    )
    args = build_parser().parse_args(["process-pending", "--json"])

    assert args.func(args) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "warning"
    assert payload["exit_code"] == 1
    assert payload["error"]["code"] == "reconciliation_incomplete"
    assert payload["error"]["retryable"] is True
    assert payload["result"]["finalized_pending"] == 1
    assert payload["result"]["reconciliation_errors"] == ["orphan receipt"]
