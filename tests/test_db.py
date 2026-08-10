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
    session_columns = {
        row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()
    }
    occurrence_columns = {
        row[1]
        for row in conn.execute("PRAGMA table_info(issue_occurrences)").fetchall()
    }
    conn.close()
    assert {
        "sessions",
        "session_files",
        "schema_versions",
        "source_blocks",
        "issues",
        "issue_occurrences",
    } <= tables
    assert "session_contexts" not in tables
    assert "session_mod_entries" not in tables
    assert {
        "parse_status",
        "parser_contract_version",
        "parse_source_blocks",
        "parse_silently_dropped_blocks",
    } <= session_columns
    assert {"source_block_id", "issue_ordinal"} <= occurrence_columns


def test_migration_preserves_legacy_context_table_without_creating_it_fresh(
    tmp_path: Path,
):
    """Legacy user tables survive C1 migration but do not imply parse success."""
    import sqlite3

    db_path = tmp_path / "legacy.db"
    legacy = sqlite3.connect(db_path)
    legacy.executescript(
        """
        CREATE TABLE sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_bundle_hash TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            log_count INTEGER NOT NULL,
            crash_present INTEGER NOT NULL,
            total_bytes INTEGER NOT NULL,
            forced_duplicate_of INTEGER
        );
        CREATE TABLE session_contexts (
            session_id INTEGER PRIMARY KEY,
            captured_at TEXT NOT NULL,
            status TEXT NOT NULL,
            confidence TEXT NOT NULL,
            game_version TEXT,
            in_game_date TEXT,
            save_path TEXT,
            save_modified_at TEXT,
            save_metadata_sha256 TEXT,
            save_source_format TEXT,
            save_delta_seconds REAL,
            mod_membership_hash TEXT NOT NULL,
            mod_count INTEGER NOT NULL,
            load_order_known INTEGER NOT NULL DEFAULT 0,
            session_state_path TEXT,
            session_state_written_at TEXT,
            source_name TEXT,
            save_only_refs_json TEXT NOT NULL DEFAULT '[]',
            session_only_refs_json TEXT NOT NULL DEFAULT '[]'
        );
        INSERT INTO sessions (
            evidence_bundle_hash, created_at, log_count, crash_present,
            total_bytes, forced_duplicate_of
        ) VALUES ('legacy', '2026-01-01T00:00:00Z', 1, 0, 10, NULL);
        INSERT INTO session_contexts (
            session_id, captured_at, status, confidence, mod_membership_hash,
            mod_count
        ) VALUES (1, '2026-01-01T00:00:00Z', 'legacy', 'low', 'hash', 1);
        """
    )
    legacy.commit()
    legacy.close()

    conn = open_db(db_path)
    context = conn.execute(
        "SELECT status FROM session_contexts WHERE session_id = 1"
    ).fetchone()
    session = conn.execute("SELECT * FROM sessions WHERE session_id = 1").fetchone()
    conn.close()

    assert context[0] == "legacy"
    assert session["parse_status"] == "not_started"
    assert session["capture_status"] == "legacy_unverified"
    assert session["parser_contract_version"] is None
    assert session["parse_source_blocks"] is None


def test_migration_failure_rolls_back_all_schema_changes(tmp_path: Path):
    """A late unique-index failure cannot leave a half-migrated database."""
    import sqlite3

    from ck3chronicle.db.migrations import apply_migrations

    db_path = tmp_path / "broken-legacy.db"
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """
        CREATE TABLE sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_bundle_hash TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            log_count INTEGER NOT NULL,
            crash_present INTEGER NOT NULL,
            total_bytes INTEGER NOT NULL,
            forced_duplicate_of INTEGER
        );
        CREATE TABLE issue_occurrences (
            issue_occurrence_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            signature TEXT NOT NULL,
            source_block_id TEXT,
            issue_ordinal INTEGER,
            log_relpath TEXT NOT NULL,
            line_number INTEGER NOT NULL,
            raw_block TEXT NOT NULL,
            occurrence_count INTEGER NOT NULL DEFAULT 1,
            referenced_symbols_json TEXT NOT NULL DEFAULT '[]',
            extra_json TEXT NOT NULL DEFAULT '{}',
            log_type TEXT NOT NULL DEFAULT 'error'
        );
        INSERT INTO sessions (
            evidence_bundle_hash, created_at, log_count, crash_present,
            total_bytes, forced_duplicate_of
        ) VALUES ('legacy-broken', '2026-01-01T00:00:00Z', 1, 0, 10, NULL);
        INSERT INTO issue_occurrences (
            session_id, signature, source_block_id, issue_ordinal,
            log_relpath, line_number, raw_block
        ) VALUES
            (1, 'a', 'duplicate', 0, 'error.log', 1, 'first'),
            (1, 'b', 'duplicate', 0, 'error.log', 2, 'second');
        """
    )
    conn.commit()

    with pytest.raises(sqlite3.IntegrityError):
        apply_migrations(conn)

    session_columns = {
        row[1] for row in conn.execute("PRAGMA table_info(sessions)").fetchall()
    }
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    conn.close()
    assert "parse_status" not in session_columns
    assert "source_blocks" not in tables
    assert "schema_versions" not in tables


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


def test_open_db_releases_handle_after_duplicate_manifest_migration_failure(
    tmp_path: Path,
):
    import sqlite3

    db_path = tmp_path / "duplicate-files.db"
    legacy = sqlite3.connect(db_path)
    legacy.executescript(
        """
        CREATE TABLE sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            evidence_bundle_hash TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            log_count INTEGER NOT NULL,
            crash_present INTEGER NOT NULL,
            total_bytes INTEGER NOT NULL,
            forced_duplicate_of INTEGER
        );
        CREATE TABLE session_files (
            session_file_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            rel_path TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            bytes INTEGER NOT NULL,
            kind TEXT NOT NULL
        );
        INSERT INTO sessions VALUES (1, 'hash', 'now', 1, 0, 1, NULL);
        INSERT INTO session_files (session_id, rel_path, sha256, bytes, kind)
        VALUES (1, 'error.log', 'a', 1, 'log'),
               (1, 'error.log', 'a', 1, 'log');
        """
    )
    legacy.commit()
    legacy.close()

    with pytest.raises(sqlite3.IntegrityError):
        open_db(db_path)

    renamed = tmp_path / "released.db"
    db_path.rename(renamed)
    assert renamed.is_file()
