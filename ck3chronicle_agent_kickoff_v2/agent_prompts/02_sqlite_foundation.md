# Agent Prompt 02: SQLite Foundation

Implement the SQLite database foundation for ck3chronicle.

Create idempotent schema initialization and repository functions for:

- sessions
- log_snapshots
- crash_folders
- crash_artifacts
- issues
- issue_occurrences
- source_resolutions
- fixability_assessments
- baselines
- ignored_issues
- schema_migrations

Use a temporary database in tests.

Do not connect this to real CK3 paths yet.
Do not implement parsing.
Do not write raw SQL in CLI handlers; use repository functions.

Acceptance criteria:

- Database initializes idempotently.
- Schema version is recorded.
- Repository functions can create a session.
- Repository functions can attach log snapshots.
- Repository functions can attach crash folder metadata.
- Repository functions can insert canonical issue records.
- Repository functions can attach source resolution metadata.
- Repository functions can fetch latest session.
- Unit tests use a temporary SQLite database.
