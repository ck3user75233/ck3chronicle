# Current handoff

Updated: 2026-09-08

The canonical checkout is `C:\Users\nateb\Documents\ck3chronicle` on branch
`codex/ck3chronicle-reboot`. The active product plan is `PROJECT_PLAN.md`, with
Trusted Run first. The evidence and reasoning behind this handoff are recorded
in `DEVELOPMENT_RESTART_AUDIT_2026-09-08.md`.

## Owner decisions in force

- The watcher is a capture-only safety mechanism. After a CK3 process exit it
  protects the live-root `error.log` before CK3 can replace it. It performs no
  hashing, parsing, database work, or pending processing.
- "More data" currently means more distinct `error.log` captures. It does not
  authorize routine capture of `debug.log` or `game.log`.
- Every accepted run has one database `session_id`, and that value is its sole
  Run ID. A matching full-file
  `error.log` SHA-256 is an accidental repeated copy/upload and must fail
  loudly before parsing or creation of another session row. This is a settled,
  low-complexity guard, not a separate identity problem.
- No separate run-receipt subsystem is part of the product. The old protected
  JSON records are a one-time source for lifecycle/crash metadata belonging to
  the 22 old pending captures; they are not a future runtime dependency.
- All pre-reboot tests and evaluator artifacts are deleted. New tests may be
  added only when they trace directly to an active owner-directed requirement.
- Production `process-pending` remains disabled. The disposable rehearsal and
  explicit outcomes are complete; production now requires a fresh verified
  backup and separate owner approval.
- No long-running processor diagnosis may run without a durable stage journal,
  explicit session bounds, and a read-only plan recorded first.
- Do not restart the watcher in this handoff task. Review and verification come
  first; startup is an explicit follow-up.

## Completed in the 2026-09-08 recovery

- Confirmed the watcher is stopped; the last heartbeat was stale and no CK3
  watcher process held the runtime lease.
- Preserved and verified the production database plus its hot SQLite rollback
  journal at
  `.ck3chronicle/wip/runtime/backups/pre-hot-journal-recovery-20260908-01/`.
- Opened the production database with standard SQLite only, causing normal
  rollback recovery. No migration, parser, classifier, pending finalizer, or
  `process-pending` code ran.
- Post-recovery `quick_check` is `ok`, `foreign_key_check` is empty, and the
  rollback-journal file is gone.
- The database contains 38 finalized sessions; all 38 report parse status
  `succeeded`. Direct read-only SQLite queries work. Current application
  read commands now refuse to perform an implicit schema migration, so the
  production CLI will require the separately approved migration before it can
  report through the new working tree. A direct check returned that refusal and
  left the 725,381,120-byte production database at SHA-256
  `D5D4DB51D86CE7EA784B90A924EB80199CE8B3E5AE8994FD3D36596DB6C246E3`.
- A read-only audit reconciled 38 archives, 38 registered sessions, 1,484,106
  stored source blocks/raw timestamp headers, and 1,497,491 occurrences. It
  found no structural or foreign-key corruption. It still reports 15 older
  sessions without semantic-projection rows. Six logs reached CK3/Paradox's
  known 100,000-entry `error.log` cap; those are valid captured files whose
  totals are producer-censored, not suspected parser failures.
- Confirmed that each of the 22 old pending directories has exactly one
  matching valid protected metadata record. Seven records claim a captured
  `exception.txt`; all seven preserved files match the recorded byte count and
  SHA-256.
- Added a preview-first, one-time converter at
  `tools/migrate_legacy_pending_metadata.ps1`. A synthetic rehearsal proved
  preview, apply, exact exception copying, timestamp preservation, and
  idempotent rerun. It has not been applied to production.
- Reviewed and narrowed three watcher defects: optional exception-copy failure
  no longer discards an already protected `error.log`, only CK3 timestamped
  crash directories enter the crash inventory, and newly published pending
  directories now inherit the pending root's access rules. Requirement-derived
  checks were added under `tests/test_watcher_capture_requirements.py` and to CI.
- Ran the six requirement-derived watcher checks with the agent-accessible
  project `.venv`; all passed. Isolated package imports, CLI help, and
  `pip check` also passed against the current editable source tree.
- Removed the pre-reboot test/evaluation tree after owner review. The governing
  test policy and concise prohibitions are in `docs/BANNED_IDEAS.md`.
- Removed the rejected ingestion override hook and success-return branch.
  Capture schema v4 makes `sessions.session_id` the sole Run ID, stores useful
  lifecycle/capture/crash facts in exactly one keyed `run_metadata` row, and
  removes the old `capture_observations` and `run_file_origins` structures. A
  disposable v3-to-v4 migration preserved the metadata, removed both obsolete
  tables, and passed SQLite integrity checks. No production migration was run.
- Audited the approved model's eight old LocalAppData `evidence.*.path`
  strings. They are inert historical metadata: the hash-validating production
  loader consumes no evidence path and no active component resolves them.
  Because the model and semantic catalog are hash-bound, path cleanup belongs
  in a deliberately reviewed new model revision rather than an in-place edit.
- Recovered the overlooked 2026-08-29 ingestion plan byte-for-byte from Git
  blob `e6084af5a604281ad68fe6da158de1369632ac13`, then revised the active
  `INGESTION_OPERATIONAL_RECOVERY_PLAN.md` to remove superseded receipt,
  evaluator, pre-reboot-test, and stale-inventory directions. Its useful
  processor lease, durable stage journal, read-only plan, explicit bounds, and
  production-scale disposable benchmark govern this recovery.
- Added a crash-releasing one-processor lease, flushed JSONL stage/progress
  journal plus current-status snapshot, exact-session planning/execution, and
  parse/classification/projection timing down to database sub-stages.
- Isolated and corrected the historical-session stall. Both tables that point
  to `source_blocks(source_block_pk)` lacked an index beginning with that
  foreign-key column. SQLite therefore scanned about 1.53 million
  classification assignments and 1.50 million occurrence rows once for every
  source block being replaced. Storage schema v3 adds both support indexes.
- Completed a bounded Run ID 14 rehearsal against a byte-identical production
  database copy and its byte-identical 139,932,278-byte archive. All 100,000
  blocks parsed, classified, and projected in 159.663 seconds with no failure;
  `quick_check=ok` and `foreign_key_check` was empty. Production was not opened
  by product code and retained its original SHA-256.
- Replaced the former wide operator surface. `process-pending` now requires one
  exact `--capture`, while `backfill-session` requires one exact `--session`.
  Both print a strict read-only plan by default, require `--execute` to mutate,
  acquire the processor lease, and journal the frozen scope. The internal old
  wide path rejects pending finalization/reconciliation before mutation.
- Verified the owner-made recovery copy at
  `.ck3chronicle/wip/benchmarks/ingestion/legacy-pending-rehearsal-20260908-01/`.
  Its pending set has the same 22 direct-child names as production. All 132
  copied files (728,770,249 bytes) are readable; filename, byte length, and
  source mtime agree with the watcher publication records. All 22 retained
  metadata records and all seven exception attachments match their recorded
  hashes. The old watcher records did not retain hashes for every principal
  log, so no claim of a source-versus-copy log-hash comparison is made; a
  SHA-256 content-set digest was calculated over the readable copy as its new
  verification baseline:
  `5f8652229595606ba14d224488e27d64db9cad02910f1b60227d7ba4f3429387`.
- Previewed and applied the one-time metadata conversion only in that
  rehearsal root: 22/22 metadata files converted and seven exceptions
  attached. A second preview proposed zero changes, proving idempotence.
- Successfully finalized and processed all 22 copied captures one at a time.
  They became rehearsal session/Run IDs 39–60: 15 normal and seven crash runs.
  The copied pending directory is empty; production still has all 22 originals.
  Together they contain 702,113 source blocks, 720,090 semantic occurrences,
  and 16,271 issue clusters. Three reached CK3's 100,000-entry producer cap.
- Profiled a repeated-block projection cost exposed by session 40. One
  21,287-character persistent-reader block produced 452 semantic units, and
  the old loop normalized and locator-scanned the complete block once per
  unit. Reusing immutable per-block evidence reduced the real 2,121-occurrence
  preparation benchmark from 11.712 seconds to 0.489 seconds (23.97x) with
  zero semantic-result differences.
- Added storage schema v4 indexes for the two projection-run foreign-key
  deletion probes. In the rehearsal database, prior-projection deletion fell
  from 1.618 seconds to 32.934 milliseconds. Detailed post-validation timing
  then exposed two competing occurrence joins; storage schemas v5 and v6 add
  projection/signature and projection/source-block composite indexes. Block
  and cluster reconciliation now take tens of milliseconds rather than an
  unbounded nested scan. Production has not been migrated and remains at
  storage schema v2.
- The third exact pending rehearsal completed in 5.78 seconds. It parsed 1,541
  source blocks into 2,149 occurrences and 97 issue clusters. Its journal
  measured semantic projection at 1.670 seconds, classification at 1.151
  seconds, parse at 0.866 seconds, and durable journal/status I/O at 1.074
  seconds over 140 emitted events. The rehearsal database remains
  `quick_check=ok` with no foreign-key violations.
- Reused immutable classification results for repeated `raw_block_pk` plus
  source-family identities. On real session 52 input, all 22,645 ordered block
  results and 23,254 semantic units were identical to uncached classification,
  while preparation fell from 23.411 seconds to 0.641 seconds (36.52x). A
  later 100,000-block pending run reused 96,133 analyses and prepared
  classification in 1.909 seconds.
- Intentionally interrupted session 52 during a demonstrably misplanned
  projection-validation query. The 882,556,928-byte database and
  5,033,680-byte hot rollback journal were preserved under the rehearsal
  root's `backups/interrupted-session52-v5-plan-20260908-01/`. Standard SQLite
  recovery restored the prior committed parsed/classified state, removed the
  hot journal, and released the processor lease. The exact read-only
  `backfill-session --session 52` plan verified the archive, skipped current
  parse/classification, and completed only projection after the v6 fix.
- Final rehearsal verification rehashed all 22 archives and reconciled their
  139 retained files (728,780,581 bytes) to SQLite. It found zero parse-lineage,
  classification, projection, source-count, occurrence-count, cluster-count,
  or duplicate-`error.log`-hash errors. `quick_check=ok` in 2.202 seconds and
  `foreign_key_check` returned zero rows in 1.936 seconds.
- Current requirement-derived verification is 14/14 passing, followed by
  compilation, isolated package/CLI imports, `pip check`, and
  `git diff --check`.

## Processing diagnosis and why production remains off

The first diagnostic run was correctly terminated once it was clear that it
had no useful stage telemetry. The overlooked approved recovery report was then
recovered and implemented. Two interrupted rehearsal roots are retained as
incident evidence; neither is a source for another run. A third fresh root,
`.ck3chronicle/wip/benchmarks/ingestion/session-14-current-code-20260908-03/`,
was copied directly from production and hash-verified before use.

The fresh journal proved that the apparent parser hang was the database cleanup
inside parse replacement. Before the fix, SQLite's foreign-key probe for both
`classification_assignments.source_block_pk` and
`issue_occurrences.source_block_pk` was `SCAN`; after adding leading-column
indexes it is `SEARCH`. `parse_delete_source_blocks` then completed in 217.344
ms, and the complete parse transaction completed in 11.696 seconds.

The successful 100,000-block rehearsal measured the actual cost centers:

- classification preparation: 115.783 seconds;
- semantic-projection preparation: 23.352 seconds;
- complete parse: 11.756 seconds, including 5.738 seconds of database appends;
- semantic-projection transaction: 4.404 seconds;
- classification transaction: 1.651 seconds; and
- database open plus storage-v3 index migration: 1.145 seconds.

This rehearsal does not support the report's tentative per-occurrence
projection-write bottleneck hypothesis. The entire 101,037-item projection
write loop took 2.456 seconds (1.140 seconds in cluster statements and 1.229
seconds in occurrence statements). Do not start a bulk-write rewrite on that
hypothesis; classification preparation is the measured dominant cost.

The copied pending rehearsals exposed a separate projection-preparation cost,
not a database-write hang: repeated semantic units from one source block each
reanalyzed that whole block. The current code analyzes each source block once
and shares only immutable locator evidence; per-unit slots and normalization
remain independent. A corrected before/after rebuild of session 40 produced
the same 90 issues and 2,121 occurrences with fingerprint
`7272e3e0a800408bea7a5acae8b9dd5a92742dd92e835d2ef758754a29bc4c1f`.

That rebuild also exposed missing indexes on
`issues.semantic_projection_run_id` and
`issue_occurrences.semantic_projection_run_id`. Storage schema v4 supplies
them. Later exact-query timings showed that cluster and block reconciliation
also need distinct composite access paths; storage schemas v5/v6 supply them.
After v6, session 52's complete post-validation took 119.156 milliseconds,
including 22.255 milliseconds for block reconciliation and 2.083 milliseconds
for cluster reconciliation. The rehearsal database is at storage v6;
production remains at storage v2.

The largest remaining measured preparation cost was classification repeatedly
running the same deterministic classifier over content already deduplicated in
`raw_block_contents`. A per-session cache now reuses the immutable result only
when both `raw_block_pk` and source family match. Direct real-data comparison
against uncached classification was exactly equal and produced fingerprint
`0e5a15b64d2f5be1e41b3a2a56cd123edd70f576d8a5dcb3370899b8ef7fbdd5`.

The pending-path and interruption/retry rehearsals are complete. Production
remains disabled because production mutation still requires a fresh verified
backup, review of this handoff/checkpoint, and a separate explicit owner
approval. The old combined command and unreadable-rehearsal blockers are
resolved in the working tree.

The original access failure has an exact cause and was not requested by Nate.
The parent
`pending` directory has inherited Modify access for `CodexSandboxUsers`, but
the old watcher created each staging directory with Python
`tempfile.mkdtemp()` and then renamed it. On this Windows runtime, a controlled
`mkdtemp()` probe reproduced a protected owner-only DACL containing SYSTEM,
Administrators, and OWNER RIGHTS; rename preserved it. All 22 affected
directories were created after the relocation by the long-running watcher.
The watcher now creates a collision-resistant ordinary directory so future
captures inherit the parent's rules. The original 22 directories remain
protected, but their content is not lost: Nate copied them into the readable
rehearsal root, where ordinary inherited access rules apply. No product-level
"stable identity" is needed.

A "disposable runtime copy" is simply a verified copy under a separate local
root where processing can change the copied database without risking production.
The successful focused benchmark contained the full database plus only Run ID
14's archive. The later pending rehearsal contains a verified production
database copy, all 22 copied pending directories, all 22 old metadata records,
and the seven exception attachments. Historical archives were intentionally
not copied because exact pending processing neither scans nor backfills them.

## Why the old command revisited historical sessions

There was a parser-contract change, and it explains the revisit. Commit
`1f4d8c2` changed parser contract `1.0.0` to `1.0.1` and changed processing so a
version mismatch forces a reparse. Commit `05afbe2` then changed the parser
contract to current version `1.0.2` and added semantic projection to the wide
pipeline. Production currently contains 15 sessions recorded as parser
contract `1.0.0` and 23 at `1.0.2`; consequently the old command selected the
first 15 for replacement.

The schema migration did not itself require those logs to be reparsed. It made
the replacement safe/current, while the missing foreign-key support indexes
made the parser-contract-driven deletion path catastrophically slow. The two
memories were therefore connected but distinct: parser lineage selected the
old sessions; database indexing made their replacement appear hung.

Three different journals must not be confused:

- `ck3chronicle.db-journal` is SQLite's temporary rollback file for an
  interrupted database transaction;
- `watch/events-*.jsonl` is the watcher's capture/lifecycle log; and
- `processing/events-*.jsonl` is the newly added durable processor-stage and
  timing journal used to locate stalls and failures.

## Watcher review status

The source now matches the narrow capture role: process observation, one
exit-triggered copy, mandatory nonempty live-root `error.log`, optional
associated root `exception.txt`, atomic pending publication, heartbeat/event
logging, and a single-process lease. There is no call to SQLite, hashing,
parsing, classification, reporting, or pending processing on that path.

Future pending directories inherit access from the pending root; the six
watcher requirements include a real Windows ACL check and rejection when the
mandatory source changes during its fsynced copy. This fixes future capture
publication but deliberately does not alter the 22 retained legacy captures. A
separate Windows probe also confirmed that atomic heartbeat-file replacement
inherits the ordinary parent ACL.

The current Codex sandbox cannot execute the optional owner-created
`.venv-owner-20260829` because its base interpreter is outside the executable
boundary. That is not a project-verification blocker: the project `.venv` is
agent-accessible, imports the current editable source, and passed the checks
listed above. Routine Python verification must be run by the agent through
`.venv`, not handed back to Nate. The watcher remains stopped until the
explicit startup decision below.

## Exact continuation order

The complete source/handoff review and final verification pass are complete:
14/14 requirement-derived checks, compilation, 52 isolated package imports,
CLI help, `pip check`, and `git diff --check` all succeeded through the
repository `.venv`.

1. Make the separate explicit decision to start one capture-only watcher. Do
   not start processing with it.
2. Stage, review, commit, and push the complete reboot checkpoint from this
   canonical repository. Until then, the remote is not a recoverable copy of
   the current worktree. An isolated throwaway index successfully staged and
   wrote the whole intended tree, but this task cannot write `.git` and cannot
   reach GitHub; use a task/environment with those capabilities for the real
   checkpoint. First restore `remote.origin.fetch` from its current single-branch
   mapping to the normal all-heads mapping, fetch/prune, and inspect the currently
   absent `origin/main` before deciding the branch promotion path.
3. Only after a fresh verified production backup and separate owner approval,
   execute one exact production pending capture or historical session at a
   time. Inspect its frozen plan, journal, integrity, and reconciliation before
   selecting another.
