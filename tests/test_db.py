"""Tests for ck3chronicle.db (schema, migrations, repository)."""
from __future__ import annotations

from pathlib import Path

import pytest

from ck3chronicle.db.repository import (
    add_session_file,
    create_session,
    get_session_by_hash,
    list_sessions,
    open_db,
)


def test_schema_creation(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}
    conn.close()
    assert "sessions" in tables
    assert "session_files" in tables
    assert "schema_versions" in tables


def test_schema_version_recorded(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    row = conn.execute(
        "SELECT version FROM schema_versions WHERE component='core'"
    ).fetchone()
    conn.close()
    assert row is not None
    assert row[0] == 1


def test_create_and_get_session(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    sid = create_session(conn, "abc123", log_count=2, crash_present=False, total_bytes=1000)
    row = get_session_by_hash(conn, "abc123")
    conn.close()
    assert row is not None
    assert row["session_id"] == sid
    assert row["log_count"] == 2
    assert row["crash_present"] == 0
    assert row["total_bytes"] == 1000


def test_unique_hash_constraint(tmp_path: Path):
    import sqlite3

    conn = open_db(tmp_path / "test.db")
    create_session(conn, "dup_hash", log_count=1, crash_present=False, total_bytes=100)
    with pytest.raises(sqlite3.IntegrityError):
        create_session(conn, "dup_hash", log_count=1, crash_present=False, total_bytes=100)
    conn.close()


def test_add_session_file(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    sid = create_session(conn, "filehash", log_count=1, crash_present=False, total_bytes=50)
    fid = add_session_file(conn, sid, "error.log", "abc" * 21 + "ab", 50, "log")
    row = conn.execute(
        "SELECT * FROM session_files WHERE session_file_id=?", (fid,)
    ).fetchone()
    conn.close()
    assert row["rel_path"] == "error.log"
    assert row["kind"] == "log"


def test_list_sessions(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    create_session(conn, "hash1", log_count=1, crash_present=False, total_bytes=100)
    create_session(conn, "hash2", log_count=2, crash_present=True, total_bytes=200)
    rows = list_sessions(conn)
    conn.close()
    assert len(rows) == 2


def test_get_session_missing(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    row = get_session_by_hash(conn, "nonexistent_hash")
    conn.close()
    assert row is None


def test_list_sessions_limit(tmp_path: Path):
    conn = open_db(tmp_path / "test.db")
    for i in range(5):
        create_session(conn, f"hash{i}", log_count=1, crash_present=False, total_bytes=10)
    rows = list_sessions(conn, limit=3)
    conn.close()
    assert len(rows) == 3


def test_open_db_idempotent(tmp_path: Path):
    """Opening the same DB twice should not raise."""
    db_path = tmp_path / "test.db"
    c1 = open_db(db_path)
    c1.close()
    c2 = open_db(db_path)
    c2.close()
