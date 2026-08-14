"""Functional contracts for the deferred processing workflow."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
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
    assert first.context_sessions == 1
    assert first.parsed_sessions == 1
    assert first.classified_sessions == 1
    assert first.source_observations == 0
    assert first.reconciliation_errors == ()
    assert first.latest_report is not None
    assert first.latest_report["session"]["session_id"] == 1
    assert first.latest_report["classification"]["semantic_occurrences"] == 1
    assert first.latest_report["runtime_context"]["status"] == "absent"

    second = process_pending(runtime, _classifier())

    assert second.finalized_pending == 0
    assert second.registered_archives == 0
    assert second.context_sessions == 0
    assert second.parsed_sessions == 0
    assert second.classified_sessions == 0
    assert second.source_observations == 0
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
    assert payload["schema_version"] == 2
    assert payload["finalized_pending"] == 1
    assert payload["registered_archives"] == 1
    assert payload["context_sessions"] == 1
    assert payload["parsed_sessions"] == 1
    assert payload["classified_sessions"] == 1
    assert payload["source_observations"] == 0
    assert payload["reconciliation_errors"] == []
    assert payload["latest_report"]["session"]["session_id"] == 1


def test_rprocess_003_latest_session_sources_are_observed_automatically(
    tmp_path,
) -> None:
    steam = tmp_path / "Steam"
    dlc = steam / "game" / "dlc" / "dlc001_core"
    workshop = steam / "workshop" / "content" / "1158310" / "111"
    relative_file = "events/example.txt"
    target = workshop.joinpath(*relative_file.split("/"))
    target.parent.mkdir(parents=True)
    target.write_text("active source", encoding="utf-8")
    debug = (
        "[12:00:00][D][jomini_game_setup.cpp:130]: DLC:\n"
        "Core Pack|dlc/dlc001_core/dlc001.dlc\n"
        "Mod:\nWorkshop Mod|mod/ugc_111.mod|Enabled\n\n"
        "[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
        f"{dlc.as_posix()}\n"
        "[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
        f"{workshop.as_posix()}\n"
        "[12:00:01][D][virtualfilesystem.cpp:1]: Continue\n"
    ).encode("utf-8")
    error = (
        "[12:00:02][E][pdx_persistent_reader.cpp:3]: Error: \"Unknown "
        "trigger: sample_key, near line: 10\" in file: "
        f"{relative_file} line: 20\n"
    ).encode("utf-8")
    logs = tmp_path / "logs-with-source"
    runtime = tmp_path / "runtime-with-source"
    files = dict(SIX_LOG_BYTES)
    files["debug.log"] = debug
    files["error.log"] = error
    write_logs(logs, files)
    spool_logs(logs, runtime)

    result = process_pending(runtime, _classifier())

    assert result.source_observations == 1
    conn = repository.open_db(runtime / "ck3chronicle.db")
    observation = conn.execute(
        "SELECT * FROM source_resolution_observations"
    ).fetchone()
    instance = conn.execute("SELECT * FROM source_file_instances").fetchone()
    assert observation["relative_path"] == relative_file
    assert instance["source_kind"] == "workshop"
    assert instance["source_key"] == "111"
    assert instance["absolute_path"] == str(target)
    conn.close()
