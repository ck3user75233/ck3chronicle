"""Functional contracts for same-run DLC and active-mod evidence."""

from __future__ import annotations

from dataclasses import replace
import json

import pytest

from ck3chronicle import config
from ck3chronicle.cli import build_parser
from ck3chronicle.db import repository
from ck3chronicle.harvester import MANIFEST_VERSION, finalize_pending, spool_logs
from ck3chronicle.runtime_context import RuntimeContextError, parse_runtime_context

from foundation_oracle import SIX_LOG_BYTES, write_logs


DEBUG_CONTEXT = (
    b"[12:00:00][D][jomini_game_setup.cpp:130]: DLC:\n"
    b"Alpha Pack|dlc/dlc001_alpha/dlc001.dlc\n"
    b"Beta Pack|dlc/dlc002_beta/dlc002.dlc\n"
    b"Mod:\n"
    b"Inactive Noise|mod/ugc_999.mod|Disabled\n"
    b"Active | Workshop|mod/ugc_222.mod|Enabled\n"
    b"Local Patch|mod/Local Patch.mod|Enabled\n"
    b"\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/CK3/game/dlc/dlc002_beta\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/CK3/game/dlc/dlc001_alpha\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/Steam/workshop/content/1158310/222\n"
    b"[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
    b"C:/Users/test/CK3/mod/Local Patch\n"
    b"[12:00:01][D][virtualfilesystem.cpp:339]: Startup continues\n"
)


def _captured_session(tmp_path, debug_log: bytes | None = DEBUG_CONTEXT):
    logs = tmp_path / "logs"
    runtime = tmp_path / "runtime"
    files = dict(SIX_LOG_BYTES)
    if debug_log is None:
        files.pop("debug.log")
    else:
        files["debug.log"] = debug_log
    write_logs(logs, files)
    captured = finalize_pending(spool_logs(logs, runtime), runtime)
    conn = repository.open_db(runtime / "ck3chronicle.db")
    session_id, _duplicate = repository.register_finalized_session(
        conn,
        evidence_bundle_hash=captured.evidence_bundle_hash,
        captured_at="2026-08-14T00:00:00+00:00",
        manifest_version=MANIFEST_VERSION,
        manifest_sha256=captured.manifest_sha256,
        evidence_completeness=("partial" if debug_log is None else "complete"),
        files=captured.files,
    )
    return runtime, captured, conn, session_id


def test_rcontext_001_mounted_data_is_authoritative_membership_and_order(
    tmp_path,
) -> None:
    runtime, _captured, conn, session_id = _captured_session(tmp_path)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.mutated is True
    assert result.status == "complete"
    assert result.warnings == ()
    assert result.inventory_dlc_count == 2
    assert result.inventory_enabled_mod_count == 2
    assert [item.dlc_key for item in result.dlcs] == [
        "dlc002_beta",
        "dlc001_alpha",
    ]
    assert [item.display_name for item in result.dlcs] == ["Beta Pack", "Alpha Pack"]
    assert [item.mod_key for item in result.mods] == ["222", "local:local patch"]
    assert [item.display_name for item in result.mods] == [
        "Active | Workshop",
        "Local Patch",
    ]
    assert [item.source_kind for item in result.mods] == ["workshop", "local"]
    assert [item.mount_ordinal for item in (*result.dlcs, *result.mods)] == [0, 1, 2, 3]
    assert all(item.mod_key != "999" for item in result.mods)
    stored = repository.get_runtime_context(conn, session_id)
    assert stored["mounted_entry_count"] == 4
    assert stored["debug_log_sha256"] == result.debug_log_sha256

    second = parse_runtime_context(conn, runtime, session_id)
    assert second.mutated is False
    assert second == replace(result, mutated=False)
    conn.close()


def test_rcontext_002_inventory_mismatch_is_visible_but_cannot_add_a_mod(
    tmp_path,
) -> None:
    debug = DEBUG_CONTEXT.replace(
        b"Local Patch|mod/Local Patch.mod|Enabled\n",
        b"Local Patch|mod/Local Patch.mod|Enabled\n"
        b"Not Mounted|mod/ugc_333.mod|Enabled\n",
    )
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "partial"
    assert result.inventory_enabled_mod_count == 3
    assert [item.mod_key for item in result.mods] == ["222", "local:local patch"]
    assert all(item.mod_key != "333" for item in result.mods)
    assert "enabled_only=['333']" in result.warnings[0]
    conn.close()


def test_rcontext_003_missing_debug_is_explicit_absent_state(tmp_path) -> None:
    runtime, _captured, conn, session_id = _captured_session(tmp_path, None)

    result = parse_runtime_context(conn, runtime, session_id)

    assert result.status == "absent"
    assert result.debug_log_sha256 is None
    assert result.dlcs == ()
    assert result.mods == ()
    assert result.warnings == ("captured debug.log is absent",)
    conn.close()


def test_rcontext_004_failed_reparse_preserves_prior_context(tmp_path) -> None:
    runtime, captured, conn, session_id = _captured_session(tmp_path)
    accepted = parse_runtime_context(conn, runtime, session_id)
    debug_path = captured.dest_dir / "debug.log"
    debug_path.write_bytes(debug_path.read_bytes() + b"corruption")

    with pytest.raises(RuntimeContextError, match="byte length"):
        parse_runtime_context(conn, runtime, session_id, reparse=True)

    preserved = parse_runtime_context(conn, runtime, session_id)
    assert preserved.status == accepted.status
    assert preserved.mods == accepted.mods
    assert preserved.mutated is False
    conn.close()


def test_rcontext_005_cli_json_exposes_complete_ordered_context(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, _captured, conn, session_id = _captured_session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(
        ["context", "--session", str(session_id), "--json"]
    )

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["schema"] == "ck3chronicle.runtime-context"
    assert payload["schema_version"] == 1
    assert payload["status"] == "complete"
    assert [item["dlc_key"] for item in payload["dlcs"]] == [
        "dlc002_beta",
        "dlc001_alpha",
    ]
    assert [item["mod_key"] for item in payload["active_mods"]] == [
        "222",
        "local:local patch",
    ]
