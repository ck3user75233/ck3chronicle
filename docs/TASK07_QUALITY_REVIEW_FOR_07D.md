# Task 07 receiving review for Task 07D

2026-09-29. Advisory/source review of delivered Task 07 ingest, storage, playsets,
retention and their watcher integration. No implementation or live operation is
commissioned by this review itself. The separate [07D prompt](TASK07D_PROMPT.md)
assigns the owner's simplified handler and the bounded follow-ups below.

The rejected database-handler design and copies were not opened for this review.
Their assumptions are not review criteria or implementation authority. Current
owner direction is the supplied in-memory, three-state handler instruction.

## Delivered baseline worth preserving

- `ingestion.py` composes the selected package, raw read/hash correspondence,
  classifier, contracts, exact accumulation and existing Run writer. Duplicate
  checks precede model/parsing work. Originals stay in capture storage.
- Schema/review version 3, explicit database-file APIs and per-Run component
  lineage are delivered. The database-wide lineage lock is absent. The writer
  retains per-Run definition correspondence and the existing SQL/review completion
  boundary. SQL reads/rendering do not require raw logs or model loading.
- `playsets.py` receives ordered producer JSON with all six member fields and
  nulls/repeats; ingestion checks association with the captured pair. Missing data
  is unavailable. Invalid completed playsets yield warnings and unavailable data
  rather than rejecting otherwise valid error logs. SQL and manifest share values.
- Retention uses original capture time, configurable 30-day elapsed age and all
  completed captures, including unprocessed ones. It targets raw error/debug logs;
  metadata, playsets, SQL and review remain. Ingest/retention use the same capture
  lock. Watcher scheduling is daily and outside the lifecycle polling loop.
- The watcher adapter submits after completed publication, scans startup captures
  and reports individual outcomes. Live activation was reported separately in
  the operational handoff; this review did not inspect or restart that process.

## Findings and assignments

| ID | Finding and evidence | Assignment / acceptance |
|---|---|---|
| 07D-01 | `ingestion.py:95` opens a repository per caller, before preparation. `watcher_processing.py` serializes only its own calls. CLI exposes capture contention as exit 3; watcher retries contention during maintenance/startup. This is a confirmed limit against the newly assigned coordination requirement, not evidence that Task 07's SQL/classification must be rebuilt. | 07D routes existing runtime reads/writes through the shared owner, separates preparation, handles contention internally and proves cross-process/manual/watcher behavior. |
| 07D-02 | Current `IngestResult.status` is `ingested`/`duplicate`; CLI returns success for both and watcher emits `ingestion_completed` for both. The owner now explicitly requires duplicate ingestion to be a `NOT_COMPLETED` request. | 07D updates request/API/CLI/watcher semantics and affected checks together. Preserve the existing Run ID and data. Successful read lookups, including no match, remain `COMPLETED`. No legacy parallel route. |
| 07D-03 | The Task 07 handoff labels its body historical, but its runnable examples still use storage directories, removed `Generation` APIs, schema/manifest 2, playset rejection and proposed hourly maintenance. README's current section also mixes schema 3 with schema 2/current-generation descriptions. | 07D supplies one current API/handoff reference and repairs current guidance/ledger, retaining useful historical evidence separately. Exact file paths, Database APIs, versions 3/3/1, optional playsets and daily scheduling must agree. |

No independent defect in the core classification/aggregation/storage/playset path
has been established by source inspection. Do not invent a rewrite assignment
to give 07D more scope. Evidence limitations below remain limitations, not new
mandatory learner/parser campaigns.

## Implementation constraints exposed by source inspection

`Database.write_run` performs accounting, review staging, SQL insertion, review
publication and commit. "Database operations only" must not be interpreted as
permission to split its accepted-result protocol into unrelated queued statements.
Keep required publication work with the operation; keep parsing/classification
outside it. No new transaction/publication framework is warranted by this review.

Current failure behavior deliberately leaves a published shard untouched when a
commit outcome may be uncertain. Existing `cleanup_unaccepted` refuses accepted
Runs. The handler must use the existing hash lookup before retrying equivalent
persistence; a caller-side non-completion is not proof of rollback. This is already
part of the owner's bounded contention instruction, not a new recovery project.

Explicit initialization and disposable verification may use the owning repository
directly. The 07D ownership rule concerns ordinary runtime callers; do not build
another initializer or runtime bypass to keep obsolete examples working.

## Verification and limits

Receiving checks are recorded in ignored `.codex-tmp/task07d-advisory-review/`.
The current Task 07 native suite was selected after source inspection: complete
genuine retained logs, disposable copies/SQL and native review, using a task-owned
output root. Its bounded fault checks exercise existing completion/retention
requirements; no fabricated CK3 messages or records were added. Initialization
checks use disposable empty databases.

**Receiving result: all five checks passed, no skips (102.916 seconds).** Two are
the current Task 07 native ingestion/retention checks; three are database
initialization checks. They exercised three complete genuine logs via API/CLI,
both retained packages in the same database, duplicates, valid/missing playsets,
per-Run lineage, native diagnostic rendering and review accounting, SQL/manifest
agreement, retained SQL reads after disposable raw expiry, capture coordination,
bounded write-failure cleanup and explicit incompatible-schema refusal. Output:
`.codex-tmp/task07d-advisory-review/check-summary.json`; native campaign results:
`70be92cf9c1d47c1a37bd2550bba002d/results.json` under that directory.

Invalid-playset warning behavior was source-inspected, not separately rerun in
this receiving pass. Historical watcher/native tests are reported evidence; no
watcher lifecycle, live process, production DB/capture or installed build was used
for receiving verification. Test storage was task-owned and disposable; existing
native input bytes and production data were not changed.

The historical Task 07 and watcher handoffs report broader campaigns and activation.
Those are reported evidence unless explicitly rerun here. This review does not
establish current live status, installed-wheel behavior, all parser recovery or
continuation branches, every possible playset shape, or OS power-loss guarantees.
The shared handler does not exist in the inspected runtime source; its verification
and integration belong to 07D. Task 08 reports and Run-result replacement remain
separate, and complete Trusted Run acceptance remains outstanding.
