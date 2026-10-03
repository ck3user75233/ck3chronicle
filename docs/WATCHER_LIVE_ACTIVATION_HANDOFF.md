# Watcher live ingestion and database naming — 2026-09-29

This is the historical September 29 activation record, not a current live-status
check. The [current Task 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) supplies the runtime API and later activation
step. Its dedicated handler was not part of this earlier activation. Recorded
PIDs/counts below are historical observations only.

## Historical installation

- Worker PID: `5032`; virtual-environment launcher PID: `51116`.
- Started: `2026-09-28T21:19:39Z` (05:19:39 on September 29, Hong Kong time).
- Command: `.venv/Scripts/python.exe -B -m ck3chronicle.cli watch`, launched
  hidden from the repository root.
- Journal: `.ck3chronicle/wip/runtime/watch/events-20260928T211939.380814Z-5032.jsonl`.
- Database: `.ck3chronicle/wip/runtime/ck3chronicle-schema3-20260928T211854Z.sqlite3`.
- Configuration: the existing ignored `config.toml`, `[watcher]` section.
- Ingestion enabled; retention enabled; maintenance every 24 hours; raw-log
  age limit 30 elapsed days. The first maintenance pass is due one day after
  startup, when the worker is available. No expiry sweep was forced at activation.

The previous capture-only worker `46516` was stopped after checking its process
identity and verifying CK3 was absent. Its OS lease was released, the explicitly
configured database was verified and the replacement watcher was started. The
old launcher exited. No autostart task or additional resident service was added.

The startup caller accepted all five readable retained captures through the
same ingest API used after each newly published capture: 12,449 diagnostic
records, each Run with its captured playset and review files. No ingestion
failures occurred for those five inputs. The activation record
in ignored `.codex-tmp/watcher-live-activation/activation.json` records accepted
Run IDs, capture IDs, playset sizes, journal counts and heartbeat verification.
SQL playsets were checked against their published review manifests and both
review files were confirmed present. Twenty-two older capture directories
reported access denial and were skipped; their permissions were not changed.

The legacy runtime `ck3chronicle.db` was not deleted, renamed or opened as a
fallback. The new configured database is the sole active pipeline store.

## Approved database naming implemented

Production Python no longer exposes `Generation`, `create_generation`,
`open_generation` or `generation_id`. The owning repository now provides:

Current initialization/runtime-read examples live in the
[Task 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md). Runtime reads use
`HandlerClient`; repository APIs remain for initialization/offline verification.


`create_database(directory, initialized_at=None)` creates
`ck3chronicle-schema<N>-YYYYMMDDTHHMMSSZ.sqlite3`. The timestamp is UTC; the
optional supplied time must be timezone-aware. Exclusive file creation rejects
same-second collisions without changing any existing database. The containing
directory may already exist, so no separate production storage directory is
required. Failed initialization is not implicitly adopted or reset.

All subsequent open/ingest calls take the exact SQLite **file path**. The manual
command's `--database` argument and watcher configuration use that same file
path. No directory scanning, newest-file selection or compatibility alias exists.

The metadata table is `database_info`, with `database_id`, `schema_version` and
`created_at`. `Database.metadata`, Run processing lineage and `RunResult` use
`database_id`; review files remain under `review/<database_id>/<run_id>/`.
The ID comes from the initialized database's filename stem, not a separately
chosen processing-generation name.

Physical SQL schema and review manifest versions are now **3** because the
metadata/lineage names changed. Playset producer format remains **1**. Existing
incompatible databases are rejected intact. No migration or replay mechanism
was introduced. Per-Run processing versions and current Run/diagnostic/playset
semantics remain unchanged.

Changed owners: `pipeline/schema.py`, `repository.py`, `domain.py`, `review.py`,
the existing ingestion open call, CLI help and configuration validation.
Active requirement checks were updated to the explicit file-path interface.

## Verification

45 checks passed before production initialization/restart:

- 31 watcher/playset capture checks.
- 9 watcher caller checks, including real native ingestion through the lifecycle
  completion hook, error-only captures and invalid-playset acceptance.
- 3 database initialization checks: approved UTC filename, preservation of
  existing files, exclusive collision handling and explicit read paths.
- 2 Task 07 native ingestion/retention checks, including manual CLI calls,
  duplicate handling, SQL/review agreement and incompatible database refusal.

Task 07's updated native campaign passed in 25.995 seconds. Its disposable
evidence remains in `.codex-tmp/task07/d735ed8760ff4945a6610987a56ce7f0/`.
Production acceptance is separately recorded in the activation record above.

## Current continuation

Use the [current Task 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md). Shared coordination and watcher integration are
implemented; activation on that code is separate. Task 08 reports and explicit
Run-result replacement remain separate.
