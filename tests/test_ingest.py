"""Tests for ck3chronicle.ingest."""
from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

import ck3chronicle.config as cfg
import ck3chronicle.ingest as ingest_mod


def test_first_ingest_creates_session(fixture_logs_with_crash: Path, tmp_path: Path):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path), \
         mock.patch.object(cfg, "ROOT_LOGS", fixture_logs_with_crash):
        result = ingest_mod.ingest(logs_root=fixture_logs_with_crash)
    assert result.session_id == 1
    assert result.was_duplicate is False
    assert result.log_count == 2
    assert result.crash_count == 1
    assert result.total_files == 3


def test_duplicate_ingest_no_force(fixture_logs_with_crash: Path, tmp_path: Path):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        r1 = ingest_mod.ingest(logs_root=fixture_logs_with_crash)
        r2 = ingest_mod.ingest(logs_root=fixture_logs_with_crash)
    assert r1.session_id == r2.session_id
    assert r2.was_duplicate is True


def test_force_duplicate_creates_new_session(
    fixture_logs_with_crash: Path, tmp_path: Path
):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        r1 = ingest_mod.ingest(logs_root=fixture_logs_with_crash)
        r2 = ingest_mod.ingest(logs_root=fixture_logs_with_crash, force=True)
    assert r2.session_id != r1.session_id
    assert r2.forced_duplicate_of == r1.session_id
    assert r2.was_duplicate is False


def test_force_hashes_differ(fixture_logs_with_crash: Path, tmp_path: Path):
    """Forced duplicate must have a unique evidence_bundle_hash."""
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        r1 = ingest_mod.ingest(logs_root=fixture_logs_with_crash)
        r2 = ingest_mod.ingest(logs_root=fixture_logs_with_crash, force=True)
    assert r1.evidence_bundle_hash != r2.evidence_bundle_hash


def test_ingest_minimal_no_crash(fixture_logs_minimal: Path, tmp_path: Path):
    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        result = ingest_mod.ingest(logs_root=fixture_logs_minimal)
    assert result.session_id == 1
    assert result.crash_count == 0
    assert result.log_count == 2


def test_session_files_recorded(fixture_logs_with_crash: Path, tmp_path: Path):
    from ck3chronicle.db.repository import open_db

    with mock.patch.object(cfg, "ROOT_CK3CHRONICLE", tmp_path):
        result = ingest_mod.ingest(logs_root=fixture_logs_with_crash)

    db_path = tmp_path / "ck3chronicle.db"
    conn = open_db(db_path)
    rows = conn.execute(
        "SELECT * FROM session_files WHERE session_id=?", (result.session_id,)
    ).fetchall()
    conn.close()
    kinds = {row["kind"] for row in rows}
    assert "log" in kinds
    assert "crash_artifact" in kinds
