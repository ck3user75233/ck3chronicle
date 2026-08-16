"""Functional contracts for evidence-scoped cross-session deltas."""

from __future__ import annotations

import json

import pytest

from ck3chronicle import config
from ck3chronicle.classification import classify_session
from ck3chronicle.classification.catalog import load_approved_projection_catalog
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.parser.service import parse_session
from ck3chronicle.runtime_context import parse_runtime_context
from ck3chronicle.session_intelligence import (
    PolicyError,
    compare_against_baseline,
    compare_sessions,
    create_baseline,
    ignore_pattern,
    list_baselines,
    list_ignored_patterns,
)
from ck3chronicle.semantic_projection_service import project_classification_run

from foundation_oracle import SIX_LOG_BYTES, write_logs
from test_classification_persistence_contract import _classifier, _session


def _classify_and_project(conn, session_id: int) -> None:
    classifier = _classifier()
    classify_session(conn, session_id, classifier)
    project_classification_run(
        conn, session_id, load_approved_projection_catalog(classifier.model)
    )


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

RUNTIME_A = (
    b"[12:00:00][D][jomini_game_setup.cpp:130]: DLC:\n"
    b"Core Pack|dlc/dlc001_core/dlc001.dlc\nMod:\n"
    b"Alpha Mod|mod/ugc_111.mod|Enabled\n"
    b"Local Patch|mod/Local Patch.mod|Enabled\n\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/CK3/game/dlc/dlc001_core\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/Steam/workshop/content/1158310/111\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/User/CK3/mod/LocalPatch\n"
    b"[12:00:01][D][virtualfilesystem.cpp:1]: Continue\n"
)
RUNTIME_B = (
    b"[12:00:00][D][jomini_game_setup.cpp:130]: DLC:\n"
    b"Core Pack|dlc/dlc001_core/dlc001.dlc\nMod:\n"
    b"Beta Mod|mod/ugc_222.mod|Enabled\n"
    b"Local Patch|mod/Local Patch.mod|Enabled\n\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/CK3/game/dlc/dlc001_core\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/User/CK3/mod/LocalPatch\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: C:/Steam/workshop/content/1158310/222\n"
    b"[12:00:01][D][virtualfilesystem.cpp:1]: Continue\n"
)


def _two_sessions(tmp_path):
    runtime, _captured, conn, previous_id = _session(tmp_path)
    _classify_and_project(conn, previous_id)
    parse_runtime_context(conn, runtime, previous_id)

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
    _classify_and_project(conn, current_id)
    parse_runtime_context(conn, runtime, current_id)
    return runtime, conn, previous_id, current_id


def _capture_classified(
    tmp_path,
    runtime,
    conn,
    name: str,
    error_log: bytes,
    captured_at: str,
    debug_log: bytes | None = None,
) -> int:
    logs = tmp_path / name
    files = dict(SIX_LOG_BYTES)
    files["error.log"] = error_log
    if debug_log is not None:
        files["debug.log"] = debug_log
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
    _classify_and_project(conn, session_id)
    parse_runtime_context(conn, runtime, session_id)
    return session_id


def test_rdelta_001_contracts_ignore_changed_keys_locators_and_line_numbers(
    tmp_path,
) -> None:
    _runtime, conn, previous_id, current_id = _two_sessions(tmp_path)

    result = compare_sessions(conn, current_id)

    assert result["schema"] == "ck3chronicle.session-comparison"
    assert result["schema_version"] == 2
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
        "policy": {
            "ignored_changed_patterns": 0,
            "actionable_changed_patterns": 3,
            "ignored_current_occurrences": 0,
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


def test_rpolicy_001_named_baseline_pins_session_and_exact_model(tmp_path) -> None:
    _runtime, conn, previous_id, current_id = _two_sessions(tmp_path)

    baseline = create_baseline(
        conn,
        "before_patch",
        previous_id,
        note="Before the localization repair",
    )
    comparison = compare_against_baseline(
        conn,
        "BEFORE_PATCH",
        current_session_id=current_id,
    )

    assert baseline["session_id"] == previous_id
    assert list_baselines(conn)[0]["captured_at"] == "2026-08-13T00:00:00+00:00"
    assert comparison["baseline"]["baseline_name"] == "before_patch"
    assert comparison["baseline"]["note"] == "Before the localization repair"
    assert comparison["previous_session"]["session_id"] == previous_id
    with pytest.raises(PolicyError, match="already exists"):
        create_baseline(conn, "Before_Patch", current_id)
    conn.close()


def test_rpolicy_002_reasoned_ignore_is_visible_not_removed(tmp_path) -> None:
    _runtime, conn, previous_id, current_id = _two_sessions(tmp_path)
    initial = compare_sessions(conn, current_id, previous_id)
    target = next(
        item for item in initial["changed_patterns"] if item["status"] == "improved"
    )

    ignored = ignore_pattern(
        conn,
        initial["model_sha256"],
        target["pattern_id"],
        "Known vanilla noise during this investigation",
    )
    annotated = compare_sessions(conn, current_id, previous_id)
    visible = next(
        item
        for item in annotated["changed_patterns"]
        if item["pattern_id"] == target["pattern_id"]
    )

    assert ignored["reason"] == "Known vanilla noise during this investigation"
    assert visible["ignored"] is True
    assert visible["ignore_reason"] == ignored["reason"]
    assert visible["previous_occurrences"] == 3
    assert visible["current_occurrences"] == 1
    assert annotated["changed_patterns_total"] == 3
    assert annotated["summary"]["policy"] == {
        "ignored_changed_patterns": 1,
        "actionable_changed_patterns": 2,
        "ignored_current_occurrences": 1,
    }
    assert list_ignored_patterns(conn) == [ignored]
    with pytest.raises(PolicyError, match="already ignored"):
        ignore_pattern(
            conn,
            initial["model_sha256"],
            target["pattern_id"],
            "A conflicting second reason",
        )
    conn.close()


def test_rpolicy_003_cli_creates_baseline_and_compares_against_it(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, previous_id, current_id = _two_sessions(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()
    create_args = parser.parse_args(
        [
            "baseline",
            "create",
            "before_patch",
            "--session",
            str(previous_id),
            "--note",
            "Known starting point",
            "--json",
        ]
    )

    assert create_args.func(create_args) == 0
    created = json.loads(capsys.readouterr().out)
    assert created["session_id"] == previous_id

    compare_args = parser.parse_args(
        [
            "compare",
            "--session",
            str(current_id),
            "--baseline",
            "before_patch",
            "--json",
        ]
    )
    assert compare_args.func(compare_args) == 0
    comparison = json.loads(capsys.readouterr().out)
    assert comparison["baseline"]["baseline_name"] == "before_patch"
    assert comparison["summary"]["pattern_counts"]["fixed"] == 1


def test_rpolicy_004_cli_requires_and_preserves_ignore_reason(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, previous_id, current_id = _two_sessions(tmp_path)
    comparison = compare_sessions(conn, current_id, previous_id)
    target = next(
        item for item in comparison["changed_patterns"] if item["status"] == "new"
    )
    model_sha256 = comparison["model_sha256"]
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    parser = build_parser()
    args = parser.parse_args(
        [
            "ignore",
            "add",
            target["pattern_id"],
            "--reason",
            "Out of scope for the current patch",
            "--model-sha256",
            model_sha256,
            "--json",
        ]
    )

    assert args.func(args) == 0
    added = json.loads(capsys.readouterr().out)
    assert added["pattern_id"] == target["pattern_id"]
    assert added["reason"] == "Out of scope for the current patch"

    list_args = parser.parse_args(
        ["ignore", "list", "--model-sha256", model_sha256, "--json"]
    )
    assert list_args.func(list_args) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed["ignored_patterns"][0]["reason"] == added["reason"]


def test_rdelta_004_report_since_wraps_report_and_compatible_comparison(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, previous_id, current_id = _two_sessions(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(
        [
            "report",
            "--session",
            str(current_id),
            "--since",
            str(previous_id),
            "--json",
        ]
    )

    assert args.func(args) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["schema"] == "ck3chronicle.command-result"
    assert envelope["command"] == "report"
    payload = envelope["result"]
    assert payload["schema"] == "ck3chronicle.report-with-comparison"
    assert payload["schema_version"] == 2
    assert payload["report"]["session"]["session_id"] == current_id
    assert payload["comparison"]["previous_session"]["session_id"] == previous_id
    assert payload["comparison"]["current_session"]["session_id"] == current_id


def test_rdelta_005_comparison_exposes_authoritative_mount_changes(tmp_path) -> None:
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    conn = repository.open_db(runtime / "ck3chronicle.db")
    previous_id = _capture_classified(
        tmp_path,
        runtime,
        conn,
        "runtime-a",
        DIV_ZERO_OLD,
        "2026-08-13T00:00:00+00:00",
        RUNTIME_A,
    )
    current_id = _capture_classified(
        tmp_path,
        runtime,
        conn,
        "runtime-b",
        DIV_ZERO_NEW,
        "2026-08-13T01:00:00+00:00",
        RUNTIME_B,
    )

    delta = compare_sessions(conn, current_id, previous_id)["runtime_context_delta"]

    assert delta["available"] is True
    assert delta["runtime_changed"] is True
    assert delta["dlcs"] == {
        "previous_count": 1,
        "current_count": 1,
        "added": [],
        "removed": [],
        "moved": [],
        "order_changed": False,
    }
    assert [item["key"] for item in delta["active_mods"]["added"]] == ["222"]
    assert [item["key"] for item in delta["active_mods"]["removed"]] == ["111"]
    assert delta["active_mods"]["moved"] == [
        {
            "key": "local:localpatch",
            "previous_order": 1,
            "current_order": 0,
        }
    ]
    assert delta["scope"] == (
        "mounted identities and order; content updates are not fingerprinted"
    )
    conn.close()
