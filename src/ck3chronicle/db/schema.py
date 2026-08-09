"""SQLite DDL for ck3chronicle."""

SESSIONS_DDL = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_bundle_hash TEXT NOT NULL UNIQUE,
    created_at           TEXT NOT NULL,
    log_count            INTEGER NOT NULL,
    crash_present        INTEGER NOT NULL,
    total_bytes          INTEGER NOT NULL,
    forced_duplicate_of  INTEGER REFERENCES sessions(session_id),
    parse_status         TEXT NOT NULL DEFAULT 'not_started'
                         CHECK (parse_status IN ('not_started', 'succeeded')),
    parser_contract_version          TEXT,
    parse_source_blocks              INTEGER CHECK (parse_source_blocks >= 0),
    parse_preamble_blocks            INTEGER CHECK (parse_preamble_blocks >= 0),
    parse_issue_occurrences          INTEGER CHECK (parse_issue_occurrences >= 0),
    parse_issue_clusters             INTEGER CHECK (parse_issue_clusters >= 0),
    parse_unclassified_occurrences   INTEGER CHECK (parse_unclassified_occurrences >= 0),
    parse_multi_issue_blocks         INTEGER CHECK (parse_multi_issue_blocks >= 0),
    parse_silently_dropped_blocks    INTEGER CHECK (parse_silently_dropped_blocks = 0)
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
# v3 additions: log_type column on both tables
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
    confidence               TEXT NOT NULL DEFAULT 'high',
    message_template         TEXT NOT NULL,
    sample_message           TEXT NOT NULL DEFAULT '',
    primary_file             TEXT,
    primary_line             INTEGER,
    referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
    referenced_objects_json  TEXT NOT NULL DEFAULT '[]',
    extra_json               TEXT NOT NULL DEFAULT '{}',
    occurrence_count         INTEGER NOT NULL DEFAULT 1,
    log_type                 TEXT NOT NULL DEFAULT 'error',
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
    source_block_id          TEXT NOT NULL,
    issue_ordinal            INTEGER NOT NULL CHECK (issue_ordinal >= 0),
    log_relpath              TEXT NOT NULL,
    line_number              INTEGER NOT NULL,
    raw_block                TEXT NOT NULL,
    occurrence_count         INTEGER NOT NULL DEFAULT 1 CHECK (occurrence_count = 1),
    referenced_symbols_json  TEXT NOT NULL DEFAULT '[]',
    extra_json               TEXT NOT NULL DEFAULT '{}',
    log_type                 TEXT NOT NULL DEFAULT 'error',
    FOREIGN KEY (session_id, source_block_id)
        REFERENCES source_blocks(session_id, source_block_id),
    UNIQUE (session_id, source_block_id, issue_ordinal)
);
"""

ISSUE_OCCURRENCES_IDX_DDL = """
CREATE INDEX IF NOT EXISTS idx_issue_occurrences_session_sig
    ON issue_occurrences(session_id, signature);
"""

SOURCE_BLOCKS_DDL = """
CREATE TABLE IF NOT EXISTS source_blocks (
    session_id          INTEGER NOT NULL REFERENCES sessions(session_id),
    source_block_id     TEXT NOT NULL,
    log_relpath         TEXT NOT NULL CHECK (log_relpath = 'error.log'),
    start_line          INTEGER NOT NULL CHECK (start_line >= 1),
    end_line            INTEGER NOT NULL CHECK (end_line >= start_line),
    timestamp           TEXT NOT NULL,
    level               TEXT NOT NULL,
    source_tag          TEXT NOT NULL,
    source_family       TEXT NOT NULL,
    raw_block_sha256    TEXT NOT NULL,
    raw_byte_length     INTEGER NOT NULL CHECK (raw_byte_length >= 0),
    raw_block           TEXT NOT NULL,
    issue_count         INTEGER NOT NULL CHECK (issue_count >= 1),
    PRIMARY KEY (session_id, source_block_id)
);
"""

SOURCE_BLOCKS_IDX_DDL = """
CREATE INDEX IF NOT EXISTS idx_source_blocks_session_line
    ON source_blocks(session_id, start_line);
"""

ALL_DDL = [
    SESSIONS_DDL,
    SESSION_FILES_DDL,
    SCHEMA_VERSIONS_DDL,
    ISSUES_DDL,
    ISSUES_IDX_SESSION_SIG_DDL,
    ISSUES_IDX_CAT_TYPE_DDL,
    SOURCE_BLOCKS_DDL,
    SOURCE_BLOCKS_IDX_DDL,
    ISSUE_OCCURRENCES_DDL,
    ISSUE_OCCURRENCES_IDX_DDL,
]

CURRENT_VERSION = 1
CANONICAL_ISSUES_VERSION = 4
SESSION_CONTEXT_VERSION = 1
