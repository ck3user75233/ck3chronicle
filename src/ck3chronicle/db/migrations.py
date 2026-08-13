"""SQLite schema migrations for ck3chronicle.

Idempotent: applying migrations to an already-current DB is a no-op.
Records component versions in the ``schema_versions`` table.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from .schema import (
    ALL_DDL,
    CANONICAL_ISSUES_VERSION,
    CAPTURE_VERSION,
    CLASSIFICATION_VERSION,
    CURRENT_VERSION,
    SESSION_CONTEXT_VERSION,
    SESSION_INTELLIGENCE_VERSION,
)


# Phase 1 note: migrations are intentionally idempotent and non-destructive.
# We use CREATE TABLE IF NOT EXISTS and record canonical issue schema version so
# migration runs are safe to re-run while preserving existing data.
def apply_migrations(conn: sqlite3.Connection) -> None:
    """Apply all schema changes atomically and record component versions."""
    if conn.in_transaction:
        raise RuntimeError("schema migration requires a connection without a transaction")
    try:
        conn.execute("BEGIN IMMEDIATE")
        _apply_migrations(conn)
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def _apply_migrations(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    for ddl in ALL_DDL:
        # Every schema constant is one statement. ``execute`` keeps SQLite DDL
        # inside our transaction; ``executescript`` would implicitly commit.
        cur.execute(ddl)

    # C1 canonical parse state.  Legacy sessions remain explicitly
    # ``not_started`` with NULL version/counters until a successful reparse.
    session_cols = {
        row[1] for row in cur.execute("PRAGMA table_info(sessions)").fetchall()
    }
    session_additions = {
        "capture_status": "TEXT NOT NULL DEFAULT 'legacy_unverified'",
        "capture_manifest_version": "INTEGER",
        "capture_manifest_sha256": "TEXT",
        "evidence_completeness": "TEXT NOT NULL DEFAULT 'complete'",
        "parse_status": "TEXT NOT NULL DEFAULT 'not_started'",
        "parser_contract_version": "TEXT",
        "parse_source_blocks": "INTEGER",
        "parse_preamble_blocks": "INTEGER",
        "parse_issue_occurrences": "INTEGER",
        "parse_issue_clusters": "INTEGER",
        "parse_unclassified_occurrences": "INTEGER",
        "parse_multi_issue_blocks": "INTEGER",
        "parse_silently_dropped_blocks": "INTEGER",
    }
    for column, declaration in session_additions.items():
        if column not in session_cols:
            cur.execute(f"ALTER TABLE sessions ADD COLUMN {column} {declaration}")

    # A migrated database must enforce the same per-session manifest identity
    # as a fresh database. Legacy duplicates are corruption and intentionally
    # make this atomic migration fail for explicit repair.
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_session_files_identity
        ON session_files(session_id, kind, rel_path)
        """
    )

    # Backfill newer columns on existing DBs created before occurrence clustering.
    cols = {
        row[1]
        for row in cur.execute("PRAGMA table_info(issue_occurrences)").fetchall()
    }
    if "occurrence_count" not in cols:
        cur.execute(
            "ALTER TABLE issue_occurrences "
            "ADD COLUMN occurrence_count INTEGER NOT NULL DEFAULT 1"
        )
    if "source_block_id" not in cols:
        cur.execute("ALTER TABLE issue_occurrences ADD COLUMN source_block_id TEXT")
    if "issue_ordinal" not in cols:
        cur.execute("ALTER TABLE issue_occurrences ADD COLUMN issue_ordinal INTEGER")

    # Backfill log_type column added in v3.
    for tbl in ("issues", "issue_occurrences"):
        cols = {
            row[1]
            for row in cur.execute(f"PRAGMA table_info({tbl})").fetchall()
        }
        if "log_type" not in cols:
            cur.execute(
                f"ALTER TABLE {tbl} ADD COLUMN log_type TEXT NOT NULL DEFAULT 'error'"
            )

    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_issue_occurrences_source_ordinal
        ON issue_occurrences(session_id, source_block_id, issue_ordinal)
        WHERE source_block_id IS NOT NULL AND issue_ordinal IS NOT NULL
        """
    )

    # The mutable session-context model is rejected for fresh databases.  If a
    # user's legacy database already has it, keep it readable and non-destructively
    # add the historical compatibility columns; never create or drop the tables.
    tables = {
        row[0]
        for row in cur.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    has_legacy_context = "session_contexts" in tables
    if has_legacy_context:
        context_cols = {
            row[1]
            for row in cur.execute("PRAGMA table_info(session_contexts)").fetchall()
        }
        context_additions = {
            "membership_evidence": "TEXT NOT NULL DEFAULT 'unknown'",
            "debug_log_path": "TEXT",
            "debug_mod_block_sha256": "TEXT",
            "debug_enabled_count": "INTEGER",
            "debug_disabled_count": "INTEGER",
            "evidence_only_refs_json": "TEXT NOT NULL DEFAULT '[]'",
        }
        for column, declaration in context_additions.items():
            if column not in context_cols:
                cur.execute(
                    f"ALTER TABLE session_contexts ADD COLUMN {column} {declaration}"
                )
        if (
            "save_only_refs_json" in context_cols
            and "evidence_only_refs_json" not in context_cols
        ):
            cur.execute(
                "UPDATE session_contexts "
                "SET evidence_only_refs_json = save_only_refs_json"
            )

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
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("capture", CAPTURE_VERSION, now),
    )
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("classification", CLASSIFICATION_VERSION, now),
    )
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("session_intelligence", SESSION_INTELLIGENCE_VERSION, now),
    )
    if has_legacy_context:
        cur.execute(
            """
            INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
            VALUES (?, ?, ?)
            """,
            ("session_context", SESSION_CONTEXT_VERSION, now),
        )
