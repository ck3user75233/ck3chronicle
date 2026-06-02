# Agent Prompt 03: Harvester and Crash Inventory

Implement `ck3chronicle ingest`.

Given:

- `--logs-dir`
- `--crashes-dir`
- `--archive-dir`
- `--db`

Behavior:

- create a new session
- snapshot configured log files into an archive/session folder
- compute sha256 and file size for each captured log
- record log snapshots in SQLite
- detect the newest crash folder, if present
- inventory crash artifacts
- record `dump_present` true/false
- skip missing logs with warnings, not fatal errors

Do not parse dump files.
Do not double-count crash-folder copied logs as primary logs.
Do not implement watch mode.
Do not place archive output inside `root:repo/ck3chronicle/`.

Acceptance criteria:

- Ingest works against test fixtures.
- Missing logs are warnings, not fatal errors.
- Crash folder copied-log artifacts are inventoried but not double-counted as parsed logs.
- Session can be listed after ingest.
- Tests cover logs present, missing logs, and crash folder present.
