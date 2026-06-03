"""Tests for ck3chronicle CLI."""
from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

import ck3chronicle.config as cfg
from ck3chronicle.cli import main


def test_doctor_exit_0(tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch.object(cfg, "CONFIG_FILE_PATH", tmp_path / "config.toml"), \
         mock.patch.object(cfg, "ROOT_GAME", tmp_path / "game"), \
         mock.patch.object(cfg, "ROOT_STEAM", tmp_path / "steam"), \
         mock.patch.object(cfg, "ROOT_LOCAL_MODS", tmp_path / "mods"), \
         mock.patch.object(cfg, "ROOT_LOGS", tmp_path / "logs"), \
         mock.patch.object(cfg, "ROOT_WIP", tmp_path / "wip"):
        with pytest.raises(SystemExit) as exc:
            main(["doctor"])
    assert exc.value.code == 0


def test_ingest_exit_0(fixture_logs_with_crash: Path, tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit) as exc:
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "session_id" in out
    assert "copied" in out


def test_ingest_duplicate_output(fixture_logs_with_crash: Path, tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit):
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
        capsys.readouterr()  # clear first ingest output
        with pytest.raises(SystemExit) as exc:
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "already ingested" in out


def test_ingest_force_output(fixture_logs_with_crash: Path, tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit):
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
        capsys.readouterr()
        with pytest.raises(SystemExit) as exc:
            main(["ingest", "--logs", str(fixture_logs_with_crash), "--force"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    assert "forced duplicate" in out


def test_sessions_no_db(tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit) as exc:
            main(["sessions"])
    assert exc.value.code == 0
    assert "No sessions" in capsys.readouterr().out


def test_sessions_after_ingest(fixture_logs_with_crash: Path, tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit):
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
        capsys.readouterr()
        with pytest.raises(SystemExit) as exc:
            main(["sessions"])
    assert exc.value.code == 0
    out = capsys.readouterr().out
    # Header row should be present
    assert "id" in out.lower()
