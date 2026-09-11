# Project status

Updated: 2026-09-08

## Executive status

ck3chronicle is back in active development in its canonical standalone
checkout. The one-time runtime relocation is complete and the local Git object
store is intact. The reboot source/documentation checkpoint is not yet
committed, so the canonical remote does not yet represent the current working
tree.

Trusted Run remains the first active capability milestone. It is implemented
in substantial parts but is not accepted. The immediate development checkpoint
is runtime stabilization. The narrowed watcher is verified and the historical
session-processing stall is now measured and corrected. The remaining runtime
rehearsal and interruption/retry proof are complete. Final source/handoff
review and repository verification are complete. The remaining checkpoint work
is a recoverable Git checkpoint, the separate watcher-start decision, and an
explicitly approved production procedure.

## Repository state

- Canonical root: `C:\Users\nateb\Documents\ck3chronicle`.
- Canonical remote: `https://github.com/ck3user75233/ck3chronicle.git`.
- Branch: `codex/ck3chronicle-reboot`.
- Local HEAD and the existing local `origin/codex/ck3chronicle-reboot`
  tracking ref both identify `a5925fad8c209c206d8da10986d81c3183aa27c7`.
- The local `origin` fetchspec is narrowed to that one branch
  (`+refs/heads/codex/ck3chronicle-reboot:refs/remotes/origin/codex/ck3chronicle-reboot`),
  and no local `origin/main` ref exists. This must be restored to the normal
  all-branches fetchspec and fetched before the declared canonical `main` can
  be compared or updated.
- `git fsck --full` reports no missing or corrupt reachable objects. Its
  unreachable dangling trees are not repository corruption.
- The reboot is a large unstaged worktree containing the named-milestone plan,
  product/DB/capture changes, wholesale removal of the pre-reboot test and
  evaluator tree, and new current documents. It must be reviewed, staged,
  committed, and pushed
  before Git is a complete recoverable copy of this state.
- A throwaway index/object directory successfully staged the complete intended
  reboot tree, passed the staged whitespace check, and wrote a complete
  isolated tree; it was then removed. The separate local sandbox/security
  transfer package is retained locally but ignored.
- This task may write the worktree but not `.git`, so it cannot create the real
  checkpoint. That is an execution-policy boundary, not Git corruption.
- Outbound GitHub access fails in the current task, so the live remote has not
  been fetched or independently compared.

## Relocation state

The ignored runtime receipt at
`.ck3chronicle/wip/runtime/migration/runtime-import-receipt.json` records a
completed, hash-verified import on 2026-08-29: 251 files and 3,938,533,553 bytes
copied and verified from the former LocalAppData runtime into the canonical
checkout's runtime tree. Current configuration and watcher artifacts point at
the canonical tree. No active importer or old-root dependency remains.

This establishes physical runtime relocation. It does not make later watcher
captures part of the original receipt, and it does not substitute for
committing the current source worktree.

One approved immutable model artifact contains eight old LocalAppData paths as
historical `evidence.*.path` metadata. Code inspection confirms that the
production loader ignores those fields and no active component resolves them;
the source hashes and cluster contracts remain usable after relocation. The
strings should be removed only when publishing a deliberately reviewed,
newly hashed model revision, not by modifying the approved artifact in place.

## Runtime and recovery state

- Watcher: stopped intentionally after source verification, pending the
  separate owner startup decision.
- Database: recovered from an interrupted SQLite transaction on 2026-09-08;
  backup and exact hashes are recorded in the backup manifest.
- Database integrity: `quick_check=ok`, no foreign-key violations.
- Registered data: 38 finalized sessions, all with succeeded parse status.
- Derived-state debt: 15 older sessions lack semantic projection.
- Known producer limit: six sessions reached CK3/Paradox's 100,000-entry
  `error.log` cap. Their files were completely captured and parsed; totals are
  producer-censored beyond the cap.
- Protected backlog: 22 old-format pending captures, unmodified.
- Recoverable old metadata: 22/22 matching records; seven verified exception
  attachments.
- Rehearsal copy: all 22 pending captures are readable under
  `.ck3chronicle/wip/benchmarks/ingestion/legacy-pending-rehearsal-20260908-01/`.
  The copy contains 132 files and 728,770,249 bytes; its name/size/mtime
  inventory agrees with the watcher records, all retained metadata/exception
  hashes match, and its SHA-256 content-set digest is
  `5f8652229595606ba14d224488e27d64db9cad02910f1b60227d7ba4f3429387`.
- Rehearsal conversion: 22/22 metadata records and seven exception attachments
  were converted on the copy, with an idempotent zero-change second preview.
- Pending rehearsal outcomes: all 22 succeeded as session/Run IDs 39–60; the
  copied pending directory is empty. The set contains 702,113 source blocks,
  720,090 semantic occurrences, and 16,271 issue clusters; three captures
  reached the 100,000-entry cap. Rehash/reconciliation verified 139 archived
  files and found no lineage, counter, archive, or duplicate-hash error. The
  rehearsal database is at storage schema v6 with `quick_check=ok` and no
  foreign-key violations.
- Production `process-pending`: disabled. The CLI now separates one exact
  pending capture from one exact historical-session backfill, prints a
  read-only plan by default, and requires `--execute`; the former wide internal
  defaults reject before mutation.
- Run identity cleanup: capture schema v4 makes the existing
  `sessions.session_id` the sole Run ID. Useful capture/lifecycle/crash facts
  live in one `run_metadata` row keyed by that ID; the rejected
  `capture_observations` identity and unused `run_file_origins` projection are
  absent from the current schema/source. A disposable v3-to-v4 migration
  preserved metadata and passed `quick_check`/foreign-key checks. Production
  remains unmigrated.
- Read commands: `open_db_readonly` no longer upgrades or vacuums a database.
  It fails loudly when an explicit schema migration is required, preventing a
  report or inspection command from becoming an unapproved production write.
- Processor recovery plan: the overlooked 2026-08-29 plan was recovered from
  dangling Git blob `e6084af5a604281ad68fe6da158de1369632ac13`.
  `INGESTION_OPERATIONAL_RECOVERY_PLAN.md` retains its useful operational
  method but removes superseded receipt, evaluator, old-test, and stale-count
  directions.
- Processor observability: an exclusive OS-held lease, flushed JSONL
  stage/progress journal, current-status snapshot, strict read-only plan, and
  exact-session bounded execution are implemented in the working tree. Journal
  summaries separately measure append/fsync and status-snapshot overhead and
  retain the last snapshot-replace error.
- Historical pipeline diagnosis: the stall was caused by missing leading-column
  indexes for two `source_block_pk` foreign keys. The old plans performed a
  child-table scan for every deleted source block. Storage schema v3 supplies
  both indexes and repairs missing ones idempotently.
- Historical revisit cause: parser-contract lineage, not a schema migration,
  selected the old rows. Commit `1f4d8c2` made a contract mismatch force
  reparse and advanced `1.0.0` to `1.0.1`; `05afbe2` advanced it to current
  `1.0.2`. Production has 15 sessions at `1.0.0` and 23 at `1.0.2`. The missing
  indexes made replacement of those 15 appear hung.
- Production-scale proof: a fresh byte-verified copy of the database and Run ID
  14's 139,932,278-byte archive completed all 100,000 blocks through parse,
  classification, and semantic projection in 159.663 seconds with no failure.
  Post-run `quick_check=ok` and `foreign_key_check` was empty. Production's
  database remained 725,381,120 bytes with SHA-256
  `D5D4DB51D86CE7EA784B90A924EB80199CE8B3E5AE8994FD3D36596DB6C246E3`.
  Classification preparation, not projection SQL, was the dominant measured
  cost; the 101,037-item projection write loop took only 2.456 seconds.
- Pending-path performance: immutable whole-block evidence is now reused for
  multiple semantic units belonging to one source block. On the real session
  40 inputs, projection preparation improved from 11.712 seconds to 0.489
  seconds (23.97x) with identical results. Classification now similarly reuses
  immutable results only for matching `raw_block_pk` and source family; a real
  22,645-block comparison was exactly equal and improved from 23.411 seconds to
  0.641 seconds (36.52x). Storage schemas v4–v6 add measured deletion and
  projection-validation access paths. A later capped 100,000-block run prepared
  classification in 1.909 seconds and completed without a stall.
- Interruption proof: session 52 was deliberately stopped inside a measured
  projection transaction after its database plus hot rollback journal were
  preserved. Standard SQLite recovery restored the complete prior
  parsed/classified state, removed the journal, and released the processor
  lease. The separate exact backfill plan verified its archive, skipped current
  stages, and completed projection after the query-plan fix.
- Legacy pending access: the exact cause was Python `tempfile.mkdtemp()` creating
  protected owner-only staging DACLs which survived rename. No owner request
  caused this. Future watcher captures now use an inheriting directory. The 22
  originals remain protected, but their content was recovered into the
  readable rehearsal copy; no content is known lost.

## Watcher implementation state

The working-tree watcher is copy-only and captures only live-root `error.log`.
It contains no database, parser, classifier, report, or pending-processor call.
An associated crash folder may contribute root `exception.txt` only.

The 2026-09-08 review corrected three issues before restart: optional exception
failure no longer blocks `error.log` publication, and unrelated new directories
are excluded from crash inference, and published directories inherit the
  pending root's Windows ACL. The mandatory copy is now fsynced and rejects a
  source whose size/mtime changes across the copy. New requirement-derived tests
  cover those behaviors, the one-log boundary, and exit-only triggering. They
  are wired into CI, and all six pass locally through the agent-accessible
  project `.venv`.
Isolated package imports, CLI help, and `pip check` also pass against the
current editable source. The optional owner-created environment remains outside
the Codex sandbox's executable boundary, but routine verification does not
depend on it and must not be delegated to the owner.

Every test/evaluator artifact inherited from the pre-reboot tree is deleted.
The only new tests are requirement-derived: six watcher/capture checks and
eight recovery/identity checks covering exact read-only plans, rejection of the
wide path, required foreign-key query plans, live journal visibility,
processor exclusivity, sole Run-ID storage, and genuinely non-mutating
read-only database access. All 14 pass locally. The rejected ingestion override
and success-return paths are also removed.
Existing-hash rejection remains mandatory before parsing or Run-ID creation,
with no override.

## Trusted Run implementation and gaps

Implemented foundations include explicit configuration, copy-first pending
capture, immutable archive manifests, SQLite schema/migrations/repositories,
run IDs and file hashes, parsing, classification, semantic projection, audits,
and provisional database read/report surfaces.

Still required for Trusted Run acceptance:

- separately approved, one-item-at-a-time production resumption from the
  successfully rehearsed legacy backlog;
- a verified hash rejection before parse/session creation for every ingestion
  entry point;
- native per-run review shard and compact diagnostic-record migration;
- database-only supported report contract and raw-path non-access proof;
- finite source, review-shard, exception, and database retention/pruning;
- supported backup/restore and interruption recovery;
- newly derived verification using representative real CK3 evidence;
- an exact approved candidate/revision set passing the ratified Trusted Run
  checks together.

Later milestone code remains provisional and earns no Trusted Run acceptance
credit.
