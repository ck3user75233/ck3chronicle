"""Functional contracts for active-runtime-only file resolution."""

from __future__ import annotations

import json

import pytest

from ck3chronicle import config
from ck3chronicle.cli import build_parser
from ck3chronicle.runtime_context import parse_runtime_context
from ck3chronicle.source_resolution import (
    SourceResolutionError,
    resolve_file_instances,
)

from test_runtime_context_contract import _captured_session


RELATIVE_PATH = "common/decisions/example.txt"


def _resolution_session(tmp_path):
    steam = tmp_path / "Steam"
    game = steam / "game"
    dlc = game / "dlc" / "dlc001_core"
    workshop = steam / "workshop" / "content" / "1158310" / "111"
    local = tmp_path / "CK3" / "mod" / "LocalPatch"
    inactive = steam / "workshop" / "content" / "1158310" / "999"
    for index, root in enumerate((game, dlc, workshop, local, inactive)):
        target = root.joinpath(*RELATIVE_PATH.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"instance-{index}", encoding="utf-8")
    debug = (
        "[12:00:00][D][jomini_game_setup.cpp:130]: DLC:\n"
        "Core Pack|dlc/dlc001_core/dlc001.dlc\n"
        "Mod:\n"
        "Workshop Mod|mod/ugc_111.mod|Enabled\n"
        "Inactive Mod|mod/ugc_999.mod|Disabled\n"
        "Local Patch|mod/Local Patch.mod|Enabled\n\n"
        "[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
        f"{dlc.as_posix()}\n"
        "[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
        f"{workshop.as_posix()}\n"
        "[12:00:00][D][virtualfilesystem_physfs.cpp:813]: Mounted Data: "
        f"{local.as_posix()}\n"
        "[12:00:01][D][virtualfilesystem.cpp:1]: Continue\n"
    ).encode("utf-8")
    runtime, _captured, conn, session_id = _captured_session(tmp_path, debug)
    parse_runtime_context(conn, runtime, session_id)
    return runtime, conn, session_id, local, inactive


def test_rresolve_001_only_recorded_roots_are_searched_in_mount_order(tmp_path) -> None:
    _runtime, conn, session_id, local, inactive = _resolution_session(tmp_path)

    result = resolve_file_instances(conn, session_id, RELATIVE_PATH)

    assert result["schema"] == "ck3chronicle.source-resolution"
    assert result["schema_version"] == 1
    assert result["projection"] == "current_filesystem_over_session_recorded_mounts"
    assert result["status"] == "multiple_instances"
    assert result["scope"] == {
        "recorded_roots": 4,
        "missing_current_roots": 0,
        "inactive_mod_roots_searched": 0,
    }
    assert [item["source_kind"] for item in result["instances"]] == [
        "base_game",
        "dlc",
        "workshop",
        "local",
    ]
    assert [item["mount_order"] for item in result["instances"]] == [0, 1, 2, 3]
    assert result["last_mounted_candidate"]["path"] == str(
        local.joinpath(*RELATIVE_PATH.split("/"))
    )
    assert all(str(inactive) not in item["path"] for item in result["instances"])
    assert all("sha256" not in item for item in result["instances"])
    conn.close()


@pytest.mark.parametrize("unsafe", ["../secrets.txt", "C:/absolute.txt", "/rooted"])
def test_rresolve_002_unsafe_paths_are_rejected(tmp_path, unsafe) -> None:
    _runtime, conn, session_id, _local, _inactive = _resolution_session(tmp_path)

    with pytest.raises(SourceResolutionError):
        resolve_file_instances(conn, session_id, unsafe)
    conn.close()


def test_rresolve_003_cli_json_preserves_scope_and_candidate(
    tmp_path, monkeypatch, capsys
) -> None:
    runtime, conn, session_id, local, _inactive = _resolution_session(tmp_path)
    conn.close()
    monkeypatch.setattr(config, "ROOT_CK3CHRONICLE", runtime)
    args = build_parser().parse_args(
        [
            "resolve-file",
            "--session",
            str(session_id),
            "--path",
            RELATIVE_PATH,
            "--json",
        ]
    )

    assert args.func(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["scope"]["inactive_mod_roots_searched"] == 0
    assert payload["last_mounted_candidate"]["source_kind"] == "local"
    assert payload["last_mounted_candidate"]["path"] == str(
        local.joinpath(*RELATIVE_PATH.split("/"))
    )
