"""Functional contracts for evidence-bearing action triage."""

from __future__ import annotations

import json

from ck3chronicle import config
from ck3chronicle.classification import classify_session
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.parser.service import parse_session
from ck3chronicle.runtime_context import parse_runtime_context
from ck3chronicle.source_resolution import observe_file_instances
from ck3chronicle.triage import _file_from_location, build_triage

from foundation_oracle import SIX_LOG_BYTES, write_logs
from test_classification_persistence_contract import _classifier


RELATIVE_FILE = "events/example.txt"


def test_rtriage_000_empty_or_malformed_file_evidence_is_not_a_source() -> None:
    assert _file_from_location('in file: "" near line: 3') is None
    assert _file_from_location("file: near line: 3") is None
    assert _file_from_location("file: events/example.txt line: 12") == RELATIVE_FILE


def _persistent_error(keys: list[str]) -> bytes:
    return b"".join(
        (
            f"[12:00:{index:02d}][E][pdx_persistent_reader.cpp:3]: Error: \""
            f"Unknown trigger: {key}, near line: {10 + index}\" in file: "
            f"{RELATIVE_FILE} line: {20 + index}\n"
        ).encode("utf-8")
        for index, key in enumerate(keys)
    )


def _triage_sessions(tmp_path):
    steam = tmp_path / "Steam"
    dlc = steam / "game" / "dlc" / "dlc001_core"
    workshop = steam / "workshop" / "content" / "1158310" / "111"
    target = workshop.joinpath(*RELATIVE_FILE.split("/"))
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
    runtime = tmp_path / "runtime"
    conn = repository.open_db(runtime / "ck3chronicle.db")
    session_ids = []
    for ordinal, keys in enumerate((["old_key"], ["new_a", "new_b", "new_c"])):
        logs = tmp_path / f"logs-{ordinal}"
        files = dict(SIX_LOG_BYTES)
        files["error.log"] = _persistent_error(list(keys))
        files["debug.log"] = debug
        write_logs(logs, files)
        captured = finalize_pending(spool_logs(logs, runtime), runtime)
        session_id, _duplicate = repository.register_finalized_session(
            conn,
            evidence_bundle_hash=captured.evidence_bundle_hash,
            captured_at=f"2026-08-14T0{ordinal}:00:00+00:00",
            manifest_version=MANIFEST_VERSION,
            manifest_sha256=captured.manifest_sha256,
            evidence_completeness="complete",
            files=captured.files,
        )
        parse_session(conn, runtime, session_id)
        classify_session(conn, session_id, _classifier())
        parse_runtime_context(conn, runtime, session_id)
        session_ids.append(session_id)
    return runtime, conn, session_ids[0], session_ids[1], target


def test_rtriage_001_regression_links_stored_locator_to_active_source(tmp_path) -> None:
    _runtime, conn, previous_id, current_id, target = _triage_sessions(tmp_path)

    triage = build_triage(conn, current_id, previous_id, limit=5)

    assert triage["schema"] == "ck3chronicle.action-triage"
    assert triage["schema_version"] == 2
    assert triage["summary"] == {
        "regression_patterns_total": 1,
        "returned_regressions": 1,
        "classification_review_occurrences": 0,
        "source_resolved_regressions": 1,
    }
    item = triage["regressions"][0]
    assert item["status"] == "worse"
    assert item["previous_occurrences"] == 1
    assert item["current_occurrences"] == 3
    assert item["template"] == "Unknown trigger : <KEY>"
    assert item["location_evidence"] == {
        "dominant_file": RELATIVE_FILE,
        "dominant_file_occurrences": 3,
        "distinct_files": 1,
        "top_files": [{"file": RELATIVE_FILE, "occurrences": 3}],
    }
    assert item["source_resolution"]["scope"]["inactive_mod_roots_searched"] == 0
    assert item["source_resolution"]["last_mounted_candidate"]["path"] == str(target)
    assert item["source_resolution"]["last_mounted_candidate"]["display_name"] is None
    assert "do not prove causal ownership" in triage["caveat"]
    conn.close()


def test_rtriage_002_cli_json_is_bounded_and_schema_versioned(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, previous_id, current_id, _target = _triage_sessions(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(
        [
            "triage",
            "--session",
            str(current_id),
            "--against",
            str(previous_id),
            "--limit",
            "1",
            "--json",
        ]
    )

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "ck3chronicle.action-triage"
    assert payload["schema_version"] == 2
    assert len(payload["regressions"]) == 1
    assert payload["regressions"][0]["source_resolution"]["projection"] == (
        "current_filesystem_over_session_recorded_mounts"
    )


def test_rtriage_003_source_change_is_correlated_from_stored_observations(
    tmp_path,
) -> None:
    _runtime, conn, previous_id, current_id, target = _triage_sessions(tmp_path)
    _previous, previous_mutated = observe_file_instances(
        conn, previous_id, RELATIVE_FILE
    )
    target.write_text("updated active source", encoding="utf-8")
    _current, current_mutated = observe_file_instances(
        conn, current_id, RELATIVE_FILE
    )

    triage = build_triage(conn, current_id, previous_id, limit=5)
    delta = triage["regressions"][0]["source_observation_delta"]

    assert previous_mutated is True
    assert current_mutated is True
    assert delta["changed"] is True
    assert delta["file_layer_winner_changed"] is True
    assert delta["instances"] == [
        {
            "source_kind": "workshop",
            "source_key": "111",
            "status": "changed",
            "previous_sha256": delta["instances"][0]["previous_sha256"],
            "current_sha256": delta["instances"][0]["current_sha256"],
        }
    ]
    assert delta["instances"][0]["previous_sha256"] != (
        delta["instances"][0]["current_sha256"]
    )
    conn.close()
