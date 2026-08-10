"""Tests for ck3chronicle CLI."""
from __future__ import annotations

from pathlib import Path
import shutil
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


def test_capture_command_is_parser_independent(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    from ck3chronicle.db.repository import open_db

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(SystemExit) as exc:
            main(["capture", "--logs", str(fixture_logs_minimal)])
    assert exc.value.code == 0
    assert "finalized evidence_bundle_hash" in capsys.readouterr().out
    conn = open_db(tmp_path / "ck3chronicle.db")
    row = conn.execute("SELECT capture_status, parse_status FROM sessions").fetchone()
    conn.close()
    assert tuple(row) == ("finalized", "not_started")


def test_capture_missing_error_exits_2(tmp_path: Path, capsys):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "debug.log").write_bytes(b"debug")
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path / "archive"):
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
                    "--stable-seconds",
                    "0",
                    "--poll-seconds",
                    "0.01",
                ]
            )
    assert exc.value.code == 0
    assert "preserved" in capsys.readouterr().out


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


def test_capture_source_mutation_exits_3_rejected_unstable(
    fixture_logs_minimal: Path,
    tmp_path: Path,
    capsys,
    monkeypatch: pytest.MonkeyPatch,
):
    import ck3chronicle.harvester as harvester

    logs = tmp_path / "logs"
    shutil.copytree(fixture_logs_minimal, logs)
    real_copy = harvester._copy_exact
    mutated = False

    def copy_then_mutate(src: Path, dst: Path) -> None:
        nonlocal mutated
        real_copy(src, dst)
        if src.name == "error.log" and not mutated:
            mutated = True
            with src.open("ab") as stream:
                stream.write(b"changed")

    monkeypatch.setattr(harvester, "_copy_exact", copy_then_mutate)
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path / "archive"):
        with pytest.raises(SystemExit) as exc:
            main(["capture", "--logs", str(logs)])
    assert exc.value.code == 3
    assert "rejected_unstable" in capsys.readouterr().err


def test_capture_database_failure_exits_5(
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
            main(["capture", "--logs", str(fixture_logs_minimal)])
    assert exc.value.code == 5
    assert "database_failed" in capsys.readouterr().err


def test_reconcile_command_runs_full_archive_verification(
    fixture_logs_minimal: Path, tmp_path: Path, capsys
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
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
