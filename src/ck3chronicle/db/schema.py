"""SQLite DDL for ck3chronicle."""

SESSIONS_DDL = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_bundle_hash TEXT NOT NULL UNIQUE,
    created_at           TEXT NOT NULL,
    log_count            INTEGER NOT NULL,
    crash_present        INTEGER NOT NULL,
    total_bytes          INTEGER NOT NULL,
    forced_duplicate_of  INTEGER REFERENCES sessions(session_id)
);
"""

SESSION_FILES_DDL = """
CREATE TABLE IF NOT EXISTS session_files (
    session_file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL REFERENCES sessions(session_id),
    rel_path        TEXT NOT NULL,
    sha256          TEXT NOT NULL,
    bytes           INTEGER NOT NULL,
    kind            TEXT NOT NULL
);
"""

SCHEMA_VERSIONS_DDL = """
CREATE TABLE IF NOT EXISTS schema_versions (
    component   TEXT PRIMARY KEY,
    version     INTEGER NOT NULL,
    migrated_at TEXT NOT NULL
);
"""

ALL_DDL = [SESSIONS_DDL, SESSION_FILES_DDL, SCHEMA_VERSIONS_DDL]

CURRENT_VERSION = 1
