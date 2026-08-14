"""SQLite schema migrations for ck3chronicle.

Idempotent: applying migrations to an already-current DB is a no-op.
Records component versions in the ``schema_versions`` table.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone

from .payloads import payload_sha256
from .schema import (
    ALL_DDL,
    CANONICAL_ISSUES_VERSION,
    CAPTURE_VERSION,
    CLASSIFICATION_ASSIGNMENTS_IDX_DDL,
    CLASSIFICATION_VERSION,
    CURRENT_VERSION,
    ISSUE_OCCURRENCES_IDX_DDL,
    RUNTIME_CONTEXT_VERSION,
    SESSION_RUNTIME_CONTEXTS_DDL,
    SESSION_CONTEXT_VERSION,
    SESSION_INTELLIGENCE_VERSION,
    SOURCE_BLOCKS_IDX_DDL,
    SOURCE_RESOLUTION_VERSION,
    STORAGE_VERSION,
)


# Phase 1 note: migrations are intentionally idempotent and non-destructive.
# We use CREATE TABLE IF NOT EXISTS and record canonical issue schema version so
# migration runs are safe to re-run while preserving existing data.
def apply_migrations(conn: sqlite3.Connection) -> bool:
    """Apply schema changes and report whether compact storage was migrated."""
    if conn.in_transaction:
        raise RuntimeError("schema migration requires a connection without a transaction")
    try:
        conn.execute("BEGIN IMMEDIATE")
        compact_storage_migrated = _apply_migrations(conn)
        conn.commit()
        return compact_storage_migrated
    except Exception:
        conn.rollback()
        raise


def _apply_migrations(conn: sqlite3.Connection) -> bool:
    cur = conn.cursor()
    for ddl in ALL_DDL:
        # Every schema constant is one statement. ``execute`` keeps SQLite DDL
        # inside our transaction; ``executescript`` would implicitly commit.
        cur.execute(ddl)
    capture_version_row = cur.execute(
        "SELECT version FROM schema_versions WHERE component = 'capture'"
    ).fetchone()
    capture_upgrade_needed = (
        capture_version_row is None
        or int(capture_version_row[0]) < CAPTURE_VERSION
    )

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

    # A content-addressed session is an evidence bundle, not a game run.
    # Extend the original observation table into the durable per-run index
    # without deleting the historical rows that first established this seam.
    observation_cols = {
        row[1]
        for row in cur.execute(
            "PRAGMA table_info(capture_observations)"
        ).fetchall()
    }
    observation_additions = {
        "capture_id": "TEXT",
        "observed_started_at": "TEXT",
        "observed_ended_at": "TEXT",
        "process_pid": "INTEGER",
        "process_started_ns": "INTEGER",
        "termination_kind": "TEXT NOT NULL DEFAULT 'unknown'",
        "crash_folder_name": "TEXT",
        "crash_folder_path": "TEXT",
        "crash_detected_at": "TEXT",
        "crash_association_method": "TEXT",
        "crash_association_confidence": "TEXT",
        "crash_exception_status": "TEXT NOT NULL DEFAULT 'unavailable'",
        "crash_exception_source_rel_path": "TEXT",
        "crash_exception_retained_path": "TEXT",
        "crash_exception_sha256": "TEXT",
        "crash_exception_bytes": "INTEGER",
        "crash_exception_source_mtime_ns": "INTEGER",
        "receipt_sha256": "TEXT",
    }
    for column, declaration in observation_additions.items():
        if column not in observation_cols:
            cur.execute(
                f"ALTER TABLE capture_observations ADD COLUMN {column} {declaration}"
            )
    cur.execute(
        """
        UPDATE capture_observations
        SET capture_id = 'legacy-observation-' || observation_id
        WHERE capture_id IS NULL
        """
    )
    cur.execute(
        """
        UPDATE capture_observations
        SET observed_ended_at = observed_at
        WHERE observed_ended_at IS NULL
        """
    )
    cur.execute(
        """
        UPDATE capture_observations
        SET crash_exception_status = 'not_applicable'
        WHERE termination_kind = 'normal'
          AND crash_exception_status = 'unavailable'
        """
    )
    cur.execute(
        """
        UPDATE capture_observations
        SET crash_exception_source_rel_path = 'exception.txt'
        WHERE termination_kind = 'crash'
          AND crash_exception_source_rel_path IS NULL
        """
    )
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_capture_observations_capture_id
        ON capture_observations(capture_id)
        """
    )
    # Imported archives may predate watcher observations. Give each evidence
    # bundle one explicit unknown legacy run so chronology remains queryable;
    # never imply that the archive proves whether CK3 exited normally.
    if capture_upgrade_needed:
        cur.execute(
            """
            INSERT INTO capture_observations (
                session_id, capture_id, observed_at, observed_ended_at,
                trigger, termination_kind
            )
            SELECT s.session_id,
                   'legacy-session-' || s.session_id,
                   s.created_at,
                   s.created_at,
                   'legacy_import',
                   'unknown'
            FROM sessions s
            WHERE NOT EXISTS (
                SELECT 1
                FROM capture_observations co
                WHERE co.session_id = s.session_id
            )
            """
        )

    # Runtime-context v2 expands the status vocabulary and binds the exact
    # Mounted Data block to its archived debug.log row and byte/line span.
    # SQLite cannot alter a CHECK constraint in place, so rebuild only the
    # small context summary table while preserving all v1 rows for reparse.
    runtime_context_cols = {
        row[1]
        for row in cur.execute(
            "PRAGMA table_info(session_runtime_contexts)"
        ).fetchall()
    }
    if "source_session_file_id" not in runtime_context_cols:
        cur.execute(
            "ALTER TABLE session_runtime_contexts "
            "RENAME TO session_runtime_contexts_v1"
        )
        cur.execute(SESSION_RUNTIME_CONTEXTS_DDL)
        cur.execute(
            """
            INSERT INTO session_runtime_contexts (
                session_id, context_contract_version, parsed_at, status,
                debug_log_sha256, mounted_entry_count, dlc_count, mod_count,
                unknown_mount_count, inventory_enabled_mod_count,
                inventory_dlc_count, warnings_json
            )
            SELECT session_id, context_contract_version, parsed_at, status,
                   debug_log_sha256, mounted_entry_count, dlc_count, mod_count,
                   unknown_mount_count, inventory_enabled_mod_count,
                   inventory_dlc_count, warnings_json
            FROM session_runtime_contexts_v1
            """
        )
        cur.execute("DROP TABLE session_runtime_contexts_v1")

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
    if "source_block_pk" not in cols and "source_block_id" not in cols:
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

    provenance_column = (
        "source_block_pk" if "source_block_pk" in cols else "source_block_id"
    )
    cur.execute(
        f"""
        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_issue_occurrences_source_ordinal
        ON issue_occurrences(session_id, {provenance_column}, issue_ordinal)
        WHERE {provenance_column} IS NOT NULL AND issue_ordinal IS NOT NULL
        """
    )

    compact_storage_migrated = _migrate_compact_storage(conn)

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
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("runtime_context", RUNTIME_CONTEXT_VERSION, now),
    )
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("source_resolution", SOURCE_RESOLUTION_VERSION, now),
    )
    cur.execute(
        """
        INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
        VALUES (?, ?, ?)
        """,
        ("storage", STORAGE_VERSION, now),
    )
    if has_legacy_context:
        cur.execute(
            """
            INSERT OR REPLACE INTO schema_versions (component, version, migrated_at)
            VALUES (?, ?, ?)
            """,
            ("session_context", SESSION_CONTEXT_VERSION, now),
        )
    return compact_storage_migrated


def _migrate_compact_storage(conn: sqlite3.Connection) -> bool:
    """Normalize repeated evidence/payload text without losing any projection.

    Captured archives remain primary evidence. SQLite retains the same decoded
    source blocks and classifier fields, but stores each distinct raw block and
    complete classifier payload once. The migration is one transaction because
    ``apply_migrations`` owns the surrounding ``BEGIN IMMEDIATE``.
    """
    cur = conn.cursor()
    source_columns = {
        row[1] for row in cur.execute("PRAGMA table_info(source_blocks)").fetchall()
    }
    occurrence_columns = {
        row[1]
        for row in cur.execute("PRAGMA table_info(issue_occurrences)").fetchall()
    }
    assignment_columns = {
        row[1]
        for row in cur.execute(
            "PRAGMA table_info(classification_assignments)"
        ).fetchall()
    }
    needs_source = "source_block_pk" not in source_columns
    needs_occurrence = "source_block_pk" not in occurrence_columns
    needs_assignment = (
        "payload_pk" not in assignment_columns
        or "source_block_pk" not in assignment_columns
    )
    if not (needs_source or needs_occurrence or needs_assignment):
        return False
    if needs_source != needs_occurrence or needs_source != needs_assignment:
        raise sqlite3.DatabaseError(
            "storage is partially compacted; refusing ambiguous migration"
        )
    if needs_assignment and "source_family" not in assignment_columns:
        raise sqlite3.DatabaseError(
            "classification storage is neither legacy nor compact"
        )

    expected_source = int(cur.execute("SELECT COUNT(*) FROM source_blocks").fetchone()[0])
    expected_occurrence = int(
        cur.execute("SELECT COUNT(*) FROM issue_occurrences").fetchone()[0]
    )
    expected_assignment = int(
        cur.execute("SELECT COUNT(*) FROM classification_assignments").fetchone()[0]
    )

    if needs_source:
        if "raw_block" not in source_columns:
            raise sqlite3.DatabaseError(
                "legacy source blocks do not retain migratable raw content"
            )
        collision = cur.execute(
            """
            SELECT raw_block_sha256
            FROM source_blocks
            GROUP BY raw_block_sha256
            HAVING MIN(raw_byte_length) != MAX(raw_byte_length)
                OR MIN(raw_block) != MAX(raw_block)
            LIMIT 1
            """
        ).fetchone()
        if collision is not None:
            raise sqlite3.DatabaseError(
                "raw-block SHA-256 maps to conflicting stored content"
            )
        cur.execute(
            """
            INSERT OR IGNORE INTO raw_block_contents (
                raw_block_sha256, raw_byte_length, raw_block
            )
            SELECT raw_block_sha256, MIN(raw_byte_length), MIN(raw_block)
            FROM source_blocks
            GROUP BY raw_block_sha256
            """
        )
        conflict = cur.execute(
            """
            SELECT 1
            FROM source_blocks sb
            JOIN raw_block_contents rb
              ON rb.raw_block_sha256 = sb.raw_block_sha256
            WHERE rb.raw_byte_length != sb.raw_byte_length
               OR rb.raw_block != sb.raw_block
            LIMIT 1
            """
        ).fetchone()
        if conflict is not None:
            raise sqlite3.DatabaseError(
                "raw-block dictionary conflicts with canonical source content"
            )
        cur.execute(
            """
            CREATE TABLE source_blocks_compact (
                source_block_pk      INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id          INTEGER NOT NULL REFERENCES sessions(session_id),
                log_relpath         TEXT NOT NULL CHECK (log_relpath = 'error.log'),
                start_line          INTEGER NOT NULL CHECK (start_line >= 1),
                end_line            INTEGER NOT NULL CHECK (end_line >= start_line),
                timestamp           TEXT NOT NULL,
                level               TEXT NOT NULL,
                source_tag          TEXT NOT NULL,
                source_family       TEXT NOT NULL,
                raw_block_pk        INTEGER NOT NULL
                    REFERENCES raw_block_contents(raw_block_pk),
                issue_count         INTEGER NOT NULL CHECK (issue_count >= 1),
                UNIQUE (session_id, start_line)
            )
            """
        )
        cur.execute(
            """
            INSERT INTO source_blocks_compact (
                session_id, log_relpath, start_line, end_line, timestamp, level,
                source_tag, source_family, raw_block_pk, issue_count
            )
            SELECT sb.session_id, sb.log_relpath, sb.start_line, sb.end_line,
                   sb.timestamp, sb.level, sb.source_tag, sb.source_family,
                   rb.raw_block_pk, sb.issue_count
            FROM source_blocks sb
            JOIN raw_block_contents rb
              ON rb.raw_block_sha256 = sb.raw_block_sha256
            """
        )

        cur.execute(
            """
            CREATE TABLE issue_occurrences_compact (
                issue_occurrence_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id               INTEGER NOT NULL REFERENCES sessions(session_id),
                signature                TEXT NOT NULL,
                source_block_pk          INTEGER NOT NULL
                                         REFERENCES source_blocks_compact(source_block_pk),
                issue_ordinal            INTEGER NOT NULL CHECK (issue_ordinal >= 0),
                log_relpath              TEXT NOT NULL,
                line_number              INTEGER NOT NULL,
                occurrence_count         INTEGER NOT NULL DEFAULT 1
                                         CHECK (occurrence_count = 1),
                referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
                extra_json               TEXT NOT NULL DEFAULT '{}',
                log_type                 TEXT NOT NULL DEFAULT 'error',
                UNIQUE (session_id, source_block_pk, issue_ordinal)
            )
            """
        )
        cur.execute(
            """
            INSERT INTO issue_occurrences_compact (
                issue_occurrence_id, session_id, signature, source_block_pk,
                issue_ordinal, log_relpath, line_number, occurrence_count,
                referenced_symbols_json, extra_json, log_type
            )
            SELECT io.issue_occurrence_id, io.session_id, io.signature,
                   compact.source_block_pk, io.issue_ordinal, io.log_relpath,
                   io.line_number, io.occurrence_count,
                   io.referenced_symbols_json, io.extra_json, io.log_type
            FROM issue_occurrences io
            JOIN source_blocks legacy
              ON legacy.session_id = io.session_id
             AND legacy.source_block_id = io.source_block_id
            JOIN source_blocks_compact compact
              ON compact.session_id = legacy.session_id
             AND compact.start_line = legacy.start_line
            """
        )

    if needs_assignment:
        rows = cur.execute(
            """
            SELECT DISTINCT cr.model_sha256, ca.source_family,
                   ca.assignment_level, ca.contract_id, ca.confidence,
                   ca.semantic_text, ca.location_evidence,
                   ca.normalized_tokens_json, ca.l1_template, ca.l2_template,
                   ca.structured_slots_json
            FROM classification_assignments ca
            JOIN classification_runs cr ON cr.run_id = ca.run_id
            """
        ).fetchall()
        for row in rows:
            values = tuple(row)
            digest = payload_sha256(values)
            cur.execute(
                """
                INSERT OR IGNORE INTO classification_payloads (
                    payload_sha256, model_sha256, source_family,
                    assignment_level, contract_id, confidence, semantic_text,
                    location_evidence, normalized_tokens_json, l1_template,
                    l2_template, structured_slots_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (digest, *values),
            )
            stored = cur.execute(
                """
                SELECT model_sha256, source_family, assignment_level,
                       contract_id, confidence, semantic_text,
                       location_evidence, normalized_tokens_json, l1_template,
                       l2_template, structured_slots_json
                FROM classification_payloads
                WHERE payload_sha256 = ?
                """,
                (digest,),
            ).fetchone()
            if stored is None or tuple(stored) != values:
                raise sqlite3.DatabaseError(
                    "classification payload SHA-256 collision"
                )

        conn.create_function(
            "ck3chronicle_payload_sha256",
            11,
            lambda *values: payload_sha256(values),
            deterministic=True,
        )
        cur.execute(
            """
            CREATE TABLE classification_assignments_compact (
                classification_assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id              INTEGER NOT NULL,
                session_id          INTEGER NOT NULL,
                source_block_pk     INTEGER NOT NULL
                                    REFERENCES source_blocks_compact(source_block_pk),
                unit_ordinal        INTEGER NOT NULL CHECK (unit_ordinal >= 0),
                payload_pk          INTEGER NOT NULL
                                    REFERENCES classification_payloads(payload_pk),
                FOREIGN KEY (run_id, session_id)
                    REFERENCES classification_runs(run_id, session_id)
                    ON DELETE CASCADE,
                UNIQUE(run_id, source_block_pk, unit_ordinal)
            )
            """
        )
        cur.execute(
            """
            INSERT INTO classification_assignments_compact (
                classification_assignment_id, run_id, session_id,
                source_block_pk, unit_ordinal, payload_pk
            )
            SELECT ca.classification_assignment_id, ca.run_id, ca.session_id,
                   compact.source_block_pk, ca.unit_ordinal, cp.payload_pk
            FROM classification_assignments ca
            JOIN classification_runs cr ON cr.run_id = ca.run_id
            JOIN source_blocks legacy
              ON legacy.session_id = ca.session_id
             AND legacy.source_block_id = ca.source_block_id
            JOIN source_blocks_compact compact
              ON compact.session_id = legacy.session_id
             AND compact.start_line = legacy.start_line
            JOIN classification_payloads cp
              ON cp.payload_sha256 = ck3chronicle_payload_sha256(
                    cr.model_sha256, ca.source_family, ca.assignment_level,
                    ca.contract_id, ca.confidence, ca.semantic_text,
                    ca.location_evidence, ca.normalized_tokens_json,
                    ca.l1_template, ca.l2_template, ca.structured_slots_json
                 )
            """
        )

    if needs_assignment:
        cur.execute("DROP TABLE classification_assignments")
    if needs_source:
        cur.execute("DROP TABLE issue_occurrences")
        cur.execute("DROP TABLE source_blocks")
        cur.execute("ALTER TABLE source_blocks_compact RENAME TO source_blocks")
        cur.execute(
            "ALTER TABLE issue_occurrences_compact RENAME TO issue_occurrences"
        )
    if needs_assignment:
        cur.execute(
            "ALTER TABLE classification_assignments_compact "
            "RENAME TO classification_assignments"
        )

    cur.execute(SOURCE_BLOCKS_IDX_DDL)
    cur.execute(ISSUE_OCCURRENCES_IDX_DDL)
    cur.execute(CLASSIFICATION_ASSIGNMENTS_IDX_DDL)
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS
            idx_issue_occurrences_source_ordinal
        ON issue_occurrences(session_id, source_block_pk, issue_ordinal)
        WHERE source_block_pk IS NOT NULL AND issue_ordinal IS NOT NULL
        """
    )

    actual = (
        int(cur.execute("SELECT COUNT(*) FROM source_blocks").fetchone()[0]),
        int(cur.execute("SELECT COUNT(*) FROM issue_occurrences").fetchone()[0]),
        int(
            cur.execute("SELECT COUNT(*) FROM classification_assignments").fetchone()[0]
        ),
    )
    if actual != (expected_source, expected_occurrence, expected_assignment):
        raise sqlite3.DatabaseError(
            "compact-storage migration changed canonical row counts"
        )
    return True
