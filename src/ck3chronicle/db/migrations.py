"""SQLite schema migrations for ck3chronicle."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from .schema import ALL_DDL, CURRENT_VERSION


def apply_migrations(conn: sqlite3.Connection) -> None:
    """Apply all DDL statements and record schema version."""
    cur = conn.cursor()
    for ddl in ALL_DDL:
        cur.executescript(ddl)
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("core", CURRENT_VERSION, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
