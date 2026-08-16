"""Functional contracts for the deferred processing workflow."""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path

import pytest

from ck3chronicle import config
from ck3chronicle import processing
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
from ck3chronicle.harvester import ArchiveIntegrityError, spool_logs
from ck3chronicle.parser.service import PARSER_CONTRACT_VERSION
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
    assert first.projected_sessions == 1
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
    assert second.projected_sessions == 0
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
    assert result["schema_version"] == 4
    assert result["finalized_pending"] == 1
    assert result["registered_archives"] == 1
    assert result["registered_runs"] == 1
    assert result["context_sessions"] == 1
    assert result["parsed_sessions"] == 1
    assert result["classified_sessions"] == 1
    assert result["projected_sessions"] == 1
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
            projected_sessions=0,
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


def test_rprocess_006_registered_archive_corruption_is_a_hard_failure(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    archive = next(path for path in (runtime / "sessions").iterdir() if path.is_dir())
    error_log = archive / "error.log"
    original = error_log.read_bytes()
    error_log.write_bytes(bytes([original[0] ^ 1]) + original[1:])

    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    from ck3chronicle.classification import catalog

    monkeypatch.setattr(catalog, "load_approved_classifier", _classifier)
    args = build_parser().parse_args(["process-pending", "--json"])

    assert args.func(args) == 3
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "failed"
    assert payload["error"]["code"] == "archive_integrity"
    assert payload["error"]["stage"] == "archive"
    assert payload["error"]["retryable"] is False


def test_rprocess_007_unchanged_registered_archives_are_not_rehashed(
    tmp_path, monkeypatch
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    original_open = Path.open
    evidence_reads: list[str] = []

    def guarded_open(path, mode="r", *args, **kwargs):
        if (
            "r" in mode
            and path.name in SIX_LOG_BYTES
            and "sessions" in path.parts
        ):
            evidence_reads.append(path.name)
            raise AssertionError(f"unchanged archived evidence was reread: {path.name}")
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)
    result = process_pending(runtime, _classifier())

    assert result.reconciliation_errors == ()
    assert evidence_reads == []


def test_rprocess_008_harmless_archive_mtime_drift_uses_content_verification(
    tmp_path
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    archive = next(path for path in (runtime / "sessions").iterdir() if path.is_dir())
    error_log = archive / "error.log"
    old = error_log.stat()
    os.utime(error_log, ns=(old.st_atime_ns, old.st_mtime_ns + 1_000_000))
    assert error_log.stat().st_mtime_ns != old.st_mtime_ns

    result = process_pending(runtime, _classifier())

    assert result.reconciliation_errors == ()
    assert error_log.read_bytes() == SIX_LOG_BYTES["error.log"]


def test_rprocess_015_upgrades_old_parse_and_rebuilds_classification(
    tmp_path,
) -> None:
    """Normal deferred processing cannot strand an accepted old parser contract."""
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    first = process_pending(runtime, _classifier())
    session_id = first.latest_report["session"]["session_id"]

    conn = repository.open_db(runtime / "ck3chronicle.db")
    old_classification_id = conn.execute(
        "SELECT run_id FROM classification_runs WHERE session_id = ?",
        (session_id,),
    ).fetchone()[0]
    conn.execute(
        "UPDATE sessions SET parser_contract_version = '1.0.0' WHERE session_id = ?",
        (session_id,),
    )
    conn.commit()
    conn.close()

    upgraded = process_pending(runtime, _classifier())

    assert upgraded.parsed_sessions == 1
    assert upgraded.classified_sessions == 1
    assert upgraded.latest_report["parse"]["contract_version"] == PARSER_CONTRACT_VERSION
    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        rows = conn.execute(
            "SELECT run_id FROM classification_runs WHERE session_id = ?",
            (session_id,),
        ).fetchall()
        assert len(rows) == 1
        assert rows[0][0] != old_classification_id
        assert repository.get_session(conn, session_id)["parser_contract_version"] == (
            PARSER_CONTRACT_VERSION
        )
    finally:
        conn.close()

    repeated = process_pending(runtime, _classifier())
    assert repeated.parsed_sessions == 0
    assert repeated.classified_sessions == 0


def _assert_process_pending_archive_failure(runtime, monkeypatch, capsys) -> None:
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    from ck3chronicle.classification import catalog

    monkeypatch.setattr(catalog, "load_approved_classifier", _classifier)
    args = build_parser().parse_args(["process-pending", "--json"])
    assert args.func(args) == 3
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "failed"
    assert payload["error"]["code"] == "archive_integrity"
    assert payload["error"]["stage"] == "archive"


def test_rprocess_009_invalid_receipt_termination_is_archive_failure(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    receipt_path = (
        runtime / "run_receipts" / "finalized" / f"{pending.dest_dir.name}.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["termination_kind"] = "invented"
    receipt_path.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    _assert_process_pending_archive_failure(runtime, monkeypatch, capsys)


def test_rprocess_010_missing_indexed_receipt_is_archive_failure(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    receipt_path = (
        runtime / "run_receipts" / "finalized" / f"{pending.dest_dir.name}.json"
    )
    receipt_path.unlink()

    _assert_process_pending_archive_failure(runtime, monkeypatch, capsys)


def test_rprocess_011_registered_database_projection_tampering_is_archive_failure(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        conn.execute(
            "UPDATE session_files SET bytes = bytes + 1 WHERE rel_path = 'error.log'"
        )
        conn.commit()
    finally:
        conn.close()

    _assert_process_pending_archive_failure(runtime, monkeypatch, capsys)


def test_rprocess_012_archive_metadata_io_failure_is_archive_failure(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    from ck3chronicle import archive_registry

    def deny_metadata(_directory, **_kwargs):
        raise OSError("simulated archive metadata failure")

    monkeypatch.setattr(
        archive_registry, "snapshot_file_metadata_matches_manifest", deny_metadata
    )
    _assert_process_pending_archive_failure(runtime, monkeypatch, capsys)


def test_rprocess_013_malformed_receipt_projection_is_archive_failure(
    tmp_path, monkeypatch, capsys
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        conn.execute(
            "DELETE FROM capture_observations WHERE capture_id = ?",
            (pending.dest_dir.name,),
        )
        conn.commit()
    finally:
        conn.close()
    receipt_path = (
        runtime / "run_receipts" / "finalized" / f"{pending.dest_dir.name}.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["process"] = {
        "image_name": "ck3.exe",
        "pid": {"not": "an integer"},
        "started_ns": 1,
    }
    receipt_path.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    _assert_process_pending_archive_failure(runtime, monkeypatch, capsys)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("schema_version", True),
        ("process_pid", 1 << 80),
    ],
)
def test_rprocess_014_receipt_scalar_boundaries_are_archive_failures(
    tmp_path, monkeypatch, capsys, field, value
) -> None:
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    write_logs(logs, SIX_LOG_BYTES)
    pending = spool_logs(logs, runtime)
    process_pending(runtime, _classifier())

    conn = repository.open_db(runtime / "ck3chronicle.db")
    try:
        conn.execute(
            "DELETE FROM capture_observations WHERE capture_id = ?",
            (pending.dest_dir.name,),
        )
        conn.commit()
    finally:
        conn.close()
    receipt_path = (
        runtime / "run_receipts" / "finalized" / f"{pending.dest_dir.name}.json"
    )
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if field == "schema_version":
        receipt["schema_version"] = value
    else:
        receipt["process"] = {
            "image_name": "ck3.exe",
            "pid": value,
            "started_ns": 1,
        }
    receipt_path.write_text(
        json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    _assert_process_pending_archive_failure(runtime, monkeypatch, capsys)
