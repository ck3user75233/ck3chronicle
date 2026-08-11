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
    assert "preserved" in out


def test_ingest_duplicate_output(fixture_logs_with_crash: Path, tmp_path: Path, capsys):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit):
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
        capsys.readouterr()
        with pytest.raises(SystemExit) as exc:
            main(["ingest", "--logs", str(fixture_logs_with_crash)])
    assert exc.value.code == 0
    assert "already captured" in capsys.readouterr().out


def test_force_identity_option_is_removed(
    fixture_logs_with_crash: Path, tmp_path: Path, capsys
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit) as exc:
            main(["ingest", "--logs", str(fixture_logs_with_crash), "--force"])
    assert exc.value.code == 2
    assert "unrecognized arguments" in capsys.readouterr().err


def test_capture_command_only_creates_pending_copy(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch("ck3chronicle.watcher.is_process_running", return_value=False):
        with pytest.raises(SystemExit) as exc:
            main(["capture", "--logs", str(fixture_logs_minimal)])
    assert exc.value.code == 0
    assert "protected pending capture" in capsys.readouterr().out
    assert len(list((tmp_path / "pending").iterdir())) == 1
    assert (tmp_path / "watch" / "last_capture.json").is_file()
    assert not (tmp_path / "sessions").exists()
    assert not (tmp_path / "ck3chronicle.db").exists()


def test_capture_missing_error_exits_2(tmp_path: Path, capsys):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "debug.log").write_bytes(b"debug")
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path / "archive"), \
         mock.patch("ck3chronicle.watcher.is_process_running", return_value=False):
        with pytest.raises(SystemExit) as exc:
            main(["capture", "--logs", str(logs)])
    assert exc.value.code == 2
    assert "error.log" in capsys.readouterr().err


def test_watch_once_captures_current_stable_logs(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch("ck3chronicle.watcher.is_process_running", return_value=False):
        with pytest.raises(SystemExit) as exc:
            main(
                [
                    "watch",
                    "--once",
                    "--logs",
                    str(fixture_logs_minimal),
                    "--poll-seconds",
                    "0.01",
                ]
            )
    assert exc.value.code == 0
    assert "protected pending capture" in capsys.readouterr().out


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
    assert "id" in capsys.readouterr().out.lower()


def test_capture_refuses_to_copy_while_ck3_is_running(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path / "archive"), \
         mock.patch("ck3chronicle.watcher.is_process_running", return_value=True):
        with pytest.raises(SystemExit) as exc:
            main(["capture", "--logs", str(fixture_logs_minimal)])
    assert exc.value.code == 3
    assert "refusing to copy a live session" in capsys.readouterr().err


def test_ingest_database_failure_exits_5(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    from ck3chronicle.db.repository import open_db

    archive = tmp_path / "archive"
    conn = open_db(archive / "ck3chronicle.db")
    conn.execute(
        """
        CREATE TRIGGER injected_cli_db_failure
        BEFORE INSERT ON sessions
        BEGIN SELECT RAISE(ABORT, 'injected CLI failure'); END
        """
    )
    conn.commit()
    conn.close()
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", archive):
        with pytest.raises(SystemExit) as exc:
            main(["ingest", "--logs", str(fixture_logs_minimal)])
    assert exc.value.code == 5
    assert "database_failed" in capsys.readouterr().err


def test_reconcile_command_runs_full_archive_verification(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch("ck3chronicle.watcher.is_process_running", return_value=False):
        with pytest.raises(SystemExit):
            main(["capture", "--logs", str(fixture_logs_minimal)])
        capsys.readouterr()
        with pytest.raises(SystemExit) as exc:
            main(["reconcile"])
    assert exc.value.code == 0
    assert "scanned 1 archives" in capsys.readouterr().out


def test_reconcile_database_failure_exits_5(tmp_path: Path, capsys):
    archive = tmp_path / "archive"
    archive.mkdir()
    (archive / "ck3chronicle.db").write_bytes(b"not a sqlite database")

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", archive):
        with pytest.raises(SystemExit) as exc:
            main(["reconcile"])

    assert exc.value.code == 5
    assert "database_failed" in capsys.readouterr().err
