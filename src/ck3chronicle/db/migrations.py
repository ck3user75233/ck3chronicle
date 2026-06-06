"""SQLite schema migrations for ck3chronicle.

Idempotent: applying migrations to an already-current DB is a no-op.
Records component versions in the ``schema_versions`` table.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from .schema import ALL_DDL, CANONICAL_ISSUES_VERSION, CURRENT_VERSION


# Phase 1 note: migrations are intentionally idempotent and non-destructive.
# We use CREATE TABLE IF NOT EXISTS and record canonical issue schema version so
# migration runs are safe to re-run while preserving existing data.
def apply_migrations(conn: sqlite3.Connection) -> None:
    """Apply all DDL statements and record component schema versions."""
    cur = conn.cursor()
    for ddl in ALL_DDL:
        cur.executescript(ddl)
    now = datetime.now(timezone.utc).isoformat()
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("core", CURRENT_VERSION, now),
    )
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("canonical_issues", CANONICAL_ISSUES_VERSION, now),
    )
    conn.commit()
