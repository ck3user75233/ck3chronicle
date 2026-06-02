# CLI Contract

## MVP commands

```bash
ck3chronicle doctor
ck3chronicle ingest
ck3chronicle sessions
ck3chronicle report
ck3chronicle latest --json
```

## Standard options

The following options should be available where relevant:

```bash
--logs-dir <path>
--crashes-dir <path>
--archive-dir <path>
--db <path>
--config <path>
--format text|markdown|json
```

Tests should use explicit paths rather than relying on real CK3 directories.

## doctor

Checks environment and prints actionable status.

Should verify:

- logs dir exists if supplied
- crashes dir exists if supplied
- archive dir is writable or creatable
- database is writable or creatable
- schema version
- known logs present or absent
- product root is `root:repo/ck3chronicle/` when running in the ck3raven repo
- large artifact paths point to WIP/data locations, not repo paths

## ingest

Creates a session and snapshots evidence.

Should:

- copy configured logs
- hash logs
- record metadata
- detect crash folder
- inventory crash artifacts
- parse logs once parser exists
- store canonical issue records
- produce short summary

## sessions

Lists known sessions.

Suggested columns:

```text
session_id
ingested_at
logs_captured
crash_detected
unique_issues
```

## report

Shows latest session report by default.

Should include:

- session id
- captured logs
- missing logs
- crash detected yes/no
- crash folder linked yes/no
- unique issue count when parser exists
- top issues when parser exists

Important:

```text
report must consume canonical issue records
report must not parse raw logs directly
```

## latest --json

Outputs compact agent-friendly JSON.

Should avoid raw log dumps by default.

## Future source/context commands

```bash
ck3chronicle report --with-sources
ck3chronicle sources resolve
ck3chronicle suspects
ck3chronicle errors --file <path>
```
