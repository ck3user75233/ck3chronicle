# Watcher source modification time — 2026-09-30

## Live activation — 2026-10-02

Owner-requested restart activated this change at 10:49:49 UTC (18:49 Hong Kong).
The previous watcher PID 34340 had remained running since September 30 at
00:27 UTC, before the timestamp implementation. Six subsequent captures were
successfully ingested using that older loaded code. Public-handler inspection
confirmed all 14 production Runs lacked the timestamp and their facts exactly
matched their retained capture metadata; the handler had not dropped the field.

After confirming no capture or ingestion was in flight, the old watcher was
stopped, its handler shut down, and the configured schema-3 database verified
read-only. New watcher PID 30816 attached to already-running CK3 PID 8204;
CK3 was not interrupted. Handler PID 23252 became ready with instance
`ca3faf45a4514e5cab542769c2a3c70f`. The fresh 10:50:19 UTC heartbeat confirmed
the watcher was running. Startup returned ordinary duplicates for all 14 Runs;
no watcher/handler ERROR events were observed. Existing Runs were not repaired.

Evidence: ignored `.codex-tmp/watcher-source-mtime/activation-20261002.json`.
The next genuine capture still needs to confirm the timestamp in production
Run facts. The implementation-delivery boundary below is historical; this
separately authorized activation supersedes its not-yet-restarted status.

`harvester.spool_logs` now adds `error_log_source_modified_at` to its existing
`capture-metadata.json` dictionary and JSON write. It is an explicit UTC ISO
timestamp with nine fractional digits and `+00:00`, preserving filesystem
nanoseconds without a floating-point conversion. Example from verification:
`2026-09-28T04:44:46.950967600+00:00`.

The value comes from the original input `error.log` stat validated during its
successful stable copy. `_copy_stable_without_hash` now returns that source's
post-copy stat instead of the destination stat, retaining its `os.stat_result`
return type. Its before/after size and mtime checks, destination-size check,
copy, fsync and metadata copying remain unchanged. `spool_logs` uses that source
stat for its existing `PendingFileStat` as well. The only other caller, manual
ingestion's `_protect_manual`, ignores the return value and remains unchanged.

The existing directory rename publishes the metadata with the capture.
`pipeline/ingestion.py` reads the same file and passes its dictionary as `facts`
to `write_run`; `repository.py` serializes it into `runs.facts_json` unchanged.
Neither receiving file nor the SQL schema needed modification. Existing metadata,
playset, publication, duplicate handling, retention and Run-ID behavior remain.
The new field is capture evidence, not a replacement for `captured_at` or the
retention/Run identity clock. Historical captures and Runs are not backfilled.

## Verification

All **43 checks passed**, with no failures, errors or skips, in **87.469 seconds**.

The new `tests/test_capture_source_mtime_requirements.py` uses complete genuine
retained CK3 logs supplied through `CK3_TASK07_EVIDENCE`. It checks:

- Exact source epoch nanoseconds against the UTC string; identical metadata
  bytes before and after publication; full metadata equality in SQL
  `runs.facts_json`; preserved playset members and duplicate behavior.
- A deliberately different destination mtime cannot supply the source fact.
- A source mtime change during copying rejects publication even when size is
  unchanged. Only a disposable source copy is modified for this check.

Evidence is ignored under `.codex-tmp/watcher-source-mtime/`: `evidence.json`
names the retained inputs and disposable output, `verify.py` reproduces the
checks, and `verification.txt` / `verification.json` record results. The native
capture/SQL case is `1c64fe13588b4fad8384ceff1922b4c3/result.json`, with source
mtime `1790570686950967600`, disposable Run `20260930-CWO6LH`, and log SHA-256
`42d27e6896d2a349fc64ecbfae0bc025cb83b7501c2e374844d615767d0fab56`.
The retained source's bytes and mtime were verified unchanged afterward.

Reproduce from the checkout with
`.\.venv\Scripts\python.exe -B .codex-tmp/watcher-source-mtime/verify.py`.
The runner includes the new source-mtime checks plus existing watcher capture,
playset, ingestion/retention and runtime logging requirements. Runtime logging
ownership checking, isolated imports and `pip check` also passed.

## Operational boundary

No historical captures/Runs, production configuration or model selection were
modified. No live process was restarted; disposable database handlers alone
were started and shut down for verification. No commit or push was made.
An already running watcher retains its loaded code; activation is separate and
was not performed. This delivery verifies retained-input capture and ingestion,
not a new observed live CK3 lifecycle.
