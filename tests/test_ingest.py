"""Transactional registry acceptance tests for finalized capture."""
from __future__ import annotations

import sqlite3
import shutil
from pathlib import Path
from unittest import mock

import pytest

import ck3chronicle.config as cfg
import ck3chronicle.ingest as ingest_mod
from ck3chronicle.db.repository import open_db
from ck3chronicle.harvester import ArchiveIntegrityError, validate_snapshot


def test_first_capture_registers_one_finalized_session(
    fixture_logs_with_crash: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        result = ingest_mod.ingest(logs_root=fixture_logs_with_crash)

    assert result.session_id == 1
    assert result.was_duplicate is False
    assert result.archive_was_existing is False
    assert result.capture_status == "finalized"
    assert result.log_count == 2
    assert result.crash_count == 1
    assert result.total_files == 3
    assert result.evidence_completeness == "partial"
    assert result.missing_principal_logs == ("debug.log",)
    validate_snapshot(result.archive_dir, expected_hash=result.evidence_bundle_hash)

    conn = open_db(tmp_path / "ck3chronicle.db")
    session = conn.execute("SELECT * FROM sessions").fetchone()
    conn.close()
    assert session["capture_status"] == "finalized"
    assert session["capture_manifest_version"] == 1
    assert session["capture_manifest_sha256"]
    assert session["evidence_completeness"] == "partial"


def test_identical_capture_returns_same_session_without_duplicate_rows(
    fixture_logs_with_crash: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        first = ingest_mod.ingest(logs_root=fixture_logs_with_crash)
        second = ingest_mod.ingest(logs_root=fixture_logs_with_crash)

    assert second.session_id == first.session_id
    assert second.evidence_bundle_hash == first.evidence_bundle_hash
    assert second.was_duplicate is True
    assert second.archive_was_existing is True
    conn = open_db(tmp_path / "ck3chronicle.db")
    assert conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM session_files").fetchone()[0] == 3
    conn.close()


def test_registered_manifest_comes_from_archived_bytes(
    fixture_logs_with_crash: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        result = ingest_mod.ingest(logs_root=fixture_logs_with_crash)

    conn = open_db(tmp_path / "ck3chronicle.db")
    rows = conn.execute(
        """
        SELECT rel_path, sha256, bytes, kind
        FROM session_files WHERE session_id=? ORDER BY rel_path
        """,
        (result.session_id,),
    ).fetchall()
    conn.close()
    assert {row["kind"] for row in rows} == {"log", "crash"}
    for row in rows:
        archived = result.archive_dir / row["rel_path"]
        assert archived.is_file()
        assert archived.stat().st_size == row["bytes"]


def test_database_file_insert_failure_rolls_back_registry_but_keeps_archive(
    fixture_logs_minimal: Path, tmp_path: Path
):
    db_path = tmp_path / "ck3chronicle.db"
    conn = open_db(db_path)
    conn.execute(
        """
        CREATE TRIGGER injected_session_file_failure
        BEFORE INSERT ON session_files
        BEGIN
            SELECT RAISE(ABORT, 'injected registry failure');
        END
        """
    )
    conn.commit()
    conn.close()

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(sqlite3.IntegrityError, match="injected registry failure"):
            ingest_mod.ingest(logs_root=fixture_logs_minimal)

    conn = open_db(db_path)
    assert conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0] == 0
    assert conn.execute("SELECT COUNT(*) FROM session_files").fetchone()[0] == 0
    conn.execute("DROP TRIGGER injected_session_file_failure")
    conn.commit()
    conn.close()
    archives = [
        path
        for path in (tmp_path / "sessions").iterdir()
        if path.name != ".staging"
    ]
    assert len(archives) == 1
    validate_snapshot(archives[0])

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        recovered = ingest_mod.ingest(logs_root=fixture_logs_minimal)
    assert recovered.session_id == 1
    assert recovered.archive_was_existing is True
    assert recovered.was_duplicate is False


def test_registered_session_with_missing_archive_is_integrity_failure(
    fixture_logs_minimal: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        result = ingest_mod.ingest(logs_root=fixture_logs_minimal)
    # Deliberately simulate external archive loss without using product code.
    for path in sorted(result.archive_dir.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            path.rmdir()
    result.archive_dir.rmdir()

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(ArchiveIntegrityError, match="missing"):
            ingest_mod.ingest(logs_root=fixture_logs_minimal)


def test_registry_rejects_manifest_mismatch_for_existing_hash(
    fixture_logs_minimal: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        result = ingest_mod.ingest(logs_root=fixture_logs_minimal)
    conn = open_db(tmp_path / "ck3chronicle.db")
    conn.execute(
        "UPDATE session_files SET sha256 = ? WHERE session_id = ? AND rel_path = 'game.log'",
        ("0" * 64, result.session_id),
    )
    conn.commit()
    conn.close()

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        with pytest.raises(ValueError, match="disagrees"):
            ingest_mod.ingest(logs_root=fixture_logs_minimal)


def test_orphan_archive_is_reconciled_after_live_logs_change(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "error.log").write_bytes(b"run A")
    (logs / "game.log").write_bytes(b"game")
    db_path = tmp_path / "archive" / "ck3chronicle.db"
    conn = open_db(db_path)
    conn.execute(
        """
        CREATE TRIGGER injected_orphan_failure
        BEFORE INSERT ON sessions
        BEGIN SELECT RAISE(ABORT, 'leave orphan archive'); END
        """
    )
    conn.commit()
    conn.close()

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path / "archive"):
        with pytest.raises(sqlite3.IntegrityError, match="orphan"):
            ingest_mod.ingest(logs_root=logs)
    (logs / "error.log").write_bytes(b"run B")
    conn = open_db(db_path)
    conn.execute("DROP TRIGGER injected_orphan_failure")
    conn.commit()
    conn.close()

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path / "archive"):
        current = ingest_mod.ingest(logs_root=logs)
    conn = open_db(db_path)
    hashes = {
        row[0] for row in conn.execute("SELECT evidence_bundle_hash FROM sessions")
    }
    conn.close()
    assert len(hashes) == 2
    assert current.evidence_bundle_hash in hashes
    assert current.was_duplicate is False


def test_two_process_exits_preserve_two_observations_for_one_bundle(
    fixture_logs_minimal: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        first = ingest_mod.ingest(
            logs_root=fixture_logs_minimal,
            observation_trigger="process_exit",
            process_name="ck3.exe",
        )
        second = ingest_mod.ingest(
            logs_root=fixture_logs_minimal,
            observation_trigger="process_exit",
            process_name="ck3.exe",
        )
    conn = open_db(tmp_path / "ck3chronicle.db")
    sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
    observations = conn.execute(
        "SELECT session_id, trigger, process_name FROM capture_observations ORDER BY observation_id"
    ).fetchall()
    conn.close()
    assert first.session_id == second.session_id
    assert sessions == 1
    assert [tuple(row) for row in observations] == [
        (first.session_id, "process_exit", "ck3.exe"),
        (first.session_id, "process_exit", "ck3.exe"),
    ]


def test_missing_old_archive_is_reported_while_new_run_is_captured(tmp_path: Path):
    logs = tmp_path / "logs"
    logs.mkdir()
    (logs / "error.log").write_bytes(b"run A")
    (logs / "game.log").write_bytes(b"game")
    archive = tmp_path / "archive"
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", archive):
        old = ingest_mod.ingest(logs_root=logs)
    shutil.rmtree(old.archive_dir)
    (logs / "error.log").write_bytes(b"run B")

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", archive):
        new = ingest_mod.ingest(logs_root=logs)
    assert new.was_duplicate is False
    assert any(old.evidence_bundle_hash in error for error in new.reconciliation_errors)
