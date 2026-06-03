"""Tests for ck3chronicle.config."""
from __future__ import annotations

import os
from pathlib import Path
from unittest import mock

import pytest

import ck3chronicle.config as cfg


def test_default_root_game_windows():
    with mock.patch("platform.system", return_value="Windows"):
        result = cfg.default_root("ROOT_GAME")
    assert "Crusader Kings III" in str(result)
    assert "game" in str(result).lower()


def test_default_root_game_linux():
    with mock.patch("platform.system", return_value="Linux"):
        result = cfg.default_root("ROOT_GAME")
    assert "Crusader Kings III" in str(result)


def test_default_root_all_names():
    for name in [
        "ROOT_GAME",
        "ROOT_STEAM",
        "ROOT_LOCAL_MODS",
        "ROOT_LOGS",
        "ROOT_CK3CHRONICLE",
        "ROOT_WIP",
    ]:
        result = cfg.default_root(name)
        assert isinstance(result, Path), f"{name} should return a Path"


def test_default_root_local_mods_windows_uses_userprofile():
    with mock.patch("platform.system", return_value="Windows"), \
         mock.patch.dict(os.environ, {"USERPROFILE": r"C:\Users\testuser"}):
        result = cfg.default_root("ROOT_LOCAL_MODS")
    assert "testuser" in str(result)


def test_default_root_ck3chronicle_windows_uses_localappdata():
    with mock.patch("platform.system", return_value="Windows"), \
         mock.patch.dict(os.environ, {"LOCALAPPDATA": r"C:\Users\testuser\AppData\Local"}):
        result = cfg.default_root("ROOT_CK3CHRONICLE")
    assert "testuser" in str(result)
    assert "ck3chronicle" in str(result).lower()


def test_default_root_unknown_raises():
    with pytest.raises(ValueError):
        cfg.default_root("NOT_A_ROOT")


def test_load_config_creates_file(tmp_path: Path):
    config_path = tmp_path / "config.toml"
    assert not config_path.exists()
    data = cfg.load_config(config_path)
    assert config_path.exists()
    assert "paths" in data


def test_load_config_idempotent(tmp_path: Path):
    config_path = tmp_path / "config.toml"
    data1 = cfg.load_config(config_path)
    data2 = cfg.load_config(config_path)
    assert data1 == data2


def test_load_config_override(tmp_path: Path):
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        '[paths]\nroot_game = "/custom/game/path"\n',
        encoding="utf-8",
    )
    data = cfg.load_config(config_path)
    assert data["paths"]["root_game"] == "/custom/game/path"


def test_resolve_root_uses_config_override(tmp_path: Path):
    override_path = str(tmp_path / "mygame")
    data = {"paths": {"root_game": override_path}}
    result = cfg._resolve_root("ROOT_GAME", data)
    assert result == Path(override_path)


def test_empty_string_falls_back_to_default(tmp_path: Path):
    config_path = tmp_path / "config.toml"
    config_path.write_text('[paths]\nroot_game = ""\n', encoding="utf-8")
    data = cfg.load_config(config_path)
    result = cfg._resolve_root("ROOT_GAME", data)
    default = cfg.default_root("ROOT_GAME")
    assert result == default


def test_module_level_constants_are_paths():
    assert isinstance(cfg.ROOT_GAME, Path)
    assert isinstance(cfg.ROOT_STEAM, Path)
    assert isinstance(cfg.ROOT_LOCAL_MODS, Path)
    assert isinstance(cfg.ROOT_LOGS, Path)
    assert isinstance(cfg.ROOT_CK3CHRONICLE, Path)
    assert isinstance(cfg.ROOT_WIP, Path)
    assert isinstance(cfg.CONFIG_FILE_PATH, Path)
