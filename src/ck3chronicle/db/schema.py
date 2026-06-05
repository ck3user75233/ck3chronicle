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

# ---------------------------------------------------------------------------
# v2 additions: canonical issues + per-occurrence rows
# ---------------------------------------------------------------------------

ISSUES_DDL = """
CREATE TABLE IF NOT EXISTS issues (
    issue_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id               INTEGER NOT NULL REFERENCES sessions(session_id),
    signature                TEXT NOT NULL,
    category                 TEXT NOT NULL,
    error_type               TEXT NOT NULL,
    tags_json                TEXT NOT NULL DEFAULT '[]',
    engine_source            TEXT NOT NULL DEFAULT '',
    severity                 TEXT NOT NULL DEFAULT 'error',
    confidence               REAL NOT NULL DEFAULT 1.0,
    message_template         TEXT NOT NULL,
    sample_message           TEXT NOT NULL DEFAULT '',
    primary_file             TEXT,
    primary_line             INTEGER,
    referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
    referenced_objects_json  TEXT NOT NULL DEFAULT '[]',
    extra_json               TEXT NOT NULL DEFAULT '{}',
    occurrence_count         INTEGER NOT NULL DEFAULT 1,
    UNIQUE(session_id, signature)
);
"""

ISSUES_IDX_SESSION_SIG_DDL = """
CREATE INDEX IF NOT EXISTS idx_issues_session_signature
    ON issues(session_id, signature);
"""

ISSUES_IDX_CAT_TYPE_DDL = """
CREATE INDEX IF NOT EXISTS idx_issues_category_error_type
    ON issues(category, error_type);
"""

ISSUE_OCCURRENCES_DDL = """
CREATE TABLE IF NOT EXISTS issue_occurrences (
    issue_occurrence_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id               INTEGER NOT NULL REFERENCES sessions(session_id),
    signature                TEXT NOT NULL,
    log_relpath              TEXT NOT NULL,
    line_number              INTEGER NOT NULL,
    raw_block                TEXT NOT NULL,
    referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
    extra_json               TEXT NOT NULL DEFAULT '{}'
);
"""

ISSUE_OCCURRENCES_IDX_DDL = """
CREATE INDEX IF NOT EXISTS idx_issue_occurrences_session_sig
    ON issue_occurrences(session_id, signature);
"""


ALL_DDL = [
    SESSIONS_DDL,
    SESSION_FILES_DDL,
    SCHEMA_VERSIONS_DDL,
    ISSUES_DDL,
    ISSUES_IDX_SESSION_SIG_DDL,
    ISSUES_IDX_CAT_TYPE_DDL,
    ISSUE_OCCURRENCES_DDL,
    ISSUE_OCCURRENCES_IDX_DDL,
]

CURRENT_VERSION = 1
CANONICAL_ISSUES_VERSION = 2
