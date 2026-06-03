"""Thin data-access layer for ck3chronicle SQLite database."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .migrations import apply_migrations


def open_db(path: Path) -> sqlite3.Connection:
    """Open (or create) the ck3chronicle database, applying migrations."""
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    apply_migrations(conn)
    return conn


def get_session_by_hash(
    conn: sqlite3.Connection, evidence_bundle_hash: str
) -> sqlite3.Row | None:
    cur = conn.execute(
        "SELECT * FROM sessions WHERE evidence_bundle_hash = ?",
        (evidence_bundle_hash,),
    )
    return cur.fetchone()


def create_session(
    conn: sqlite3.Connection,
    evidence_bundle_hash: str,
    log_count: int,
    crash_present: bool,
    total_bytes: int,
    forced_duplicate_of: int | None = None,
) -> int:
    created_at = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """
        INSERT INTO sessions
            (evidence_bundle_hash, created_at, log_count, crash_present,
             total_bytes, forced_duplicate_of)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            evidence_bundle_hash,
            created_at,
            log_count,
            int(crash_present),
            total_bytes,
            forced_duplicate_of,
        ),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def add_session_file(
    conn: sqlite3.Connection,
    session_id: int,
    rel_path: str,
    sha256: str,
    bytes_: int,
    kind: str,
) -> int:
    cur = conn.execute(
        """
        INSERT INTO session_files (session_id, rel_path, sha256, bytes, kind)
        VALUES (?, ?, ?, ?, ?)
        """,
        (session_id, rel_path, sha256, bytes_, kind),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def list_sessions(
    conn: sqlite3.Connection, limit: int = 100
) -> list[sqlite3.Row]:
    cur = conn.execute(
        "SELECT * FROM sessions ORDER BY session_id DESC LIMIT ?",
        (limit,),
    )
    return cur.fetchall()
