"""Tests for ck3chronicle.doctor."""
from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

import ck3chronicle.config as cfg


def test_doctor_runs_without_error(tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch.object(cfg, "CONFIG_FILE_PATH", tmp_path / "config.toml"), \
         mock.patch.object(cfg, "ROOT_GAME", tmp_path / "game"), \
         mock.patch.object(cfg, "ROOT_STEAM", tmp_path / "steam"), \
         mock.patch.object(cfg, "ROOT_LOCAL_MODS", tmp_path / "mods"), \
         mock.patch.object(cfg, "ROOT_LOGS", tmp_path / "logs"), \
         mock.patch.object(cfg, "ROOT_WIP", tmp_path / "wip"):
        from ck3chronicle.doctor import run_doctor

        run_doctor()

    out = capsys.readouterr().out
    assert "ck3chronicle" in out
    assert "ROOT_GAME" in out


def test_doctor_shows_missing_paths(tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch.object(cfg, "CONFIG_FILE_PATH", tmp_path / "config.toml"), \
         mock.patch.object(cfg, "ROOT_GAME", tmp_path / "nonexistent_game"), \
         mock.patch.object(cfg, "ROOT_STEAM", tmp_path / "steam"), \
         mock.patch.object(cfg, "ROOT_LOCAL_MODS", tmp_path / "mods"), \
         mock.patch.object(cfg, "ROOT_LOGS", tmp_path / "logs"), \
         mock.patch.object(cfg, "ROOT_WIP", tmp_path / "wip"):
        from ck3chronicle.doctor import run_doctor

        run_doctor()

    out = capsys.readouterr().out
    assert "missing" in out


def test_doctor_creates_config_if_absent(tmp_path: Path, capsys):
    config_path = tmp_path / "config.toml"
    assert not config_path.exists()

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch.object(cfg, "CONFIG_FILE_PATH", config_path), \
         mock.patch.object(cfg, "ROOT_GAME", tmp_path / "game"), \
         mock.patch.object(cfg, "ROOT_STEAM", tmp_path / "steam"), \
         mock.patch.object(cfg, "ROOT_LOCAL_MODS", tmp_path / "mods"), \
         mock.patch.object(cfg, "ROOT_LOGS", tmp_path / "logs"), \
         mock.patch.object(cfg, "ROOT_WIP", tmp_path / "wip"):
        from ck3chronicle.doctor import run_doctor

        run_doctor()

    assert config_path.exists()
