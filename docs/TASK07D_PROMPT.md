# Task 07D Prompt

Implement the owner's simplified database request handler and complete the bounded
Task 07 receiving repairs below. This is a separate implementation assignment;
Task 07's delivered ingest/storage/retention work is the baseline, not work to
rebuild. The owner has supplied implementation direction, not another design-only
exercise. Make routine implementation choices and proceed through verification
and handoff. Report a concrete blocker before expanding the architecture.

## Authority and reading boundary

Follow AGENTS.md, current owner instructions and BANNED_IDEAS.md. Use this prompt
and [the independent receiving review](TASK07_QUALITY_REVIEW_FOR_07D.md).
Read current owning source and the delivered ingestion/retention, watcher wiring
and activation handoffs for implementation evidence. The current API facts below
supersede historical examples in those handoffs.

The owner rejected the earlier "Shared database request handler — design".
Do not read, retrieve, recover, summarize or reuse it, including copies, Git
history, scratch artifacts or the shutdown/design continuation derived from it.
`PIPELINE_QUEUED_INGESTION_DESIGN.md`, its former follow-up prompt and
`QUEUE_DESIGN_SHUTDOWN_HANDOFF.md` are not required reading or implementation
authority. Do not follow historical links directing you back to them. The owner's
new direction, represented here, supersedes their review gates and continuation
instructions. Do not restore a rejected design under another name.

Current baseline: `create_database`, `open_database`, `open_database_readonly`,
`Database`; opening/ingestion takes an exact SQLite file path. SQL schema and
native review manifest are version 3; playset format is 1. Per-Run lineage is
already implemented. Missing or invalid playsets do not reject valid error logs;
invalid supplied playsets yield a warning and the existing unavailable value.
Retention is configurable, initially 30 elapsed days for all completed captures,
including failed/unprocessed ones; watcher maintenance is daily. Existing live
activation is historical evidence, not proof of the current process state.

## 1. Objective and shared boundary

Serialize database work rather than rejecting it because the database is occupied:

**callers → shared request handler → queued database operations → one database
worker → results returned to callers**

Watcher, manual CLI and application callers submit supported runtime reads and
writes through the same handler. A request identifies an operation and its
arguments. The handler accepts it, assigns/returns a reference, queues the required
work in memory and makes its eventual result available. Ordinary runtime callers
must not open SQLite independently or receive connections, cursors or repository
objects. Expose defined existing repository operations, not arbitrary SQL.

For each configured database, exactly one active database worker owns the runtime
connection/repository. It opens, uses and closes them in its own execution context.
Execute complete repository/database operations serially, not individual SQL
statements. Operation B waits for operation A. Do not add priorities, extra
schedulers or additional read workers/connections for hypothetical performance.

Preserve the existing Run persistence and native-review completion boundary.
The current `Database.write_run` owns both SQL and associated review-file work;
its required completion work may remain part of that operation. This does not
authorize moving parsing/classification into it or replacing its publication
protocol with a new framework.

## 2. Cross-process ownership

Separate processes must reach the same handler/worker; independent per-process
queues do not satisfy the requirement. Use the smallest local Windows transport
and ownership mechanism that meets this, such as a named pipe and an existing
OS ownership lock. One suitable existing caller process may host the owner when
none exists; other callers connect to it. Manual/API use works without a watcher.
No new resident Windows service, broker, generalized election or job platform.

References belong only to the current handler lifetime. If it exits, a later
caller can establish a new owner with a fresh in-memory queue. No cross-owner
reference lookup, request transfer or durable identity is required.

## 3. Exactly three public request states

| State | Meaning |
|---|---|
| `ENQUEUED` | Accepted and not terminal. Includes queue waiting, preparation, hashing/parsing/classification, database waits/execution and short internal contention retries. |
| `COMPLETED` | The requested operation succeeded. A successful read returning no matching record is completed. |
| `NOT_COMPLETED` | The request terminated without completing its requested work. Includes duplicate ingestion, unavailable input, ordinary exceptions and owner exit before completion. It does not necessarily mean a software failure. |

Do not expose submitting, preparing, waiting, executing, retrying or duplicate as
additional request states. Preserve useful ordinary warnings/exceptions rather
than inventing an error taxonomy, failure classes, commit-state machinery or
root-cause diagnosis. A duplicate can return the existing Run and a plain warning.
Keep an enqueue timestamp. A programming hang may leave a request `ENQUEUED`;
no watchdog, automatic hang diagnosis or cancellation feature is commissioned.

Use a small interface along these lines, with names following project conventions:

```python
submit(operation, arguments) -> RequestRef
status(ref) -> ENQUEUED | COMPLETED | NOT_COMPLETED
wait(ref, timeout=None) -> status/result
result(ref, timeout=None) -> result
```

`submit` returns only after acceptance. If acceptance fails, return/raise directly;
do not fabricate a pre-acceptance state. A caller wait timeout is not itself a
terminal request outcome. Retain only in-memory information needed to serve
references/results during the owner's lifetime. No explicit client release
protocol unless technically unavoidable. Do not add a public service lifecycle
state machine; the handler can accept/serve requests or it cannot.

## 4. Ingestion and duplicates

Keep copying, hashing, parsing and classification outside the database worker and
outside a database transaction. Preserve the existing composition, protected-input
handling, pre-parse hash lookup, final duplicate enforcement, contracts, accounting,
per-Run lineage, persistence, two-part review and raw-retention coordination.
Required lookups and final persistence go through the shared handler. Reads can
run during preparation through that owner without an extra connection or worker.
Preparation must not occupy the database worker while waiting for its own request.

An ingestion request for an accepted content hash returns `NOT_COMPLETED`, with
the existing Run ID/result where useful and a human-readable duplicate indication.
It creates no new Run and performs no replacement, even if another package was
requested. This is expected non-completion, not a software failure. A successful
lookup of that same Run remains a `COMPLETED` read operation. Internal lookup/write
requests do not change the meaning of the caller's enclosing ingestion request.

This explicitly changes the caller-facing treatment of duplicates from the old
`ingested`/`duplicate` success envelope. Update the owning caller/result handling
and checks together; do not maintain an alternative legacy ingestion path.

## 5. Contention and accepted-result preservation

Ordinary ck3chronicle concurrency waits. Temporary SQLite BUSY/LOCKED is handled
internally with the simplest appropriate wait/retry; the request stays `ENQUEUED`.
Do not rerun expensive preparation merely because final database work must wait.
Keep protected-input ownership sufficient for existing review preparation and
completion; merely enqueued work must not exempt untouched captures from expiry.

For a genuinely uncertain write outcome, use the existing Run/content-hash check
before attempting equivalent persistence again. Preserve accepted review evidence.
Reuse the existing guarded cleanup where actually needed for an unaccepted
publication; no new journal, recovery state machine or blind write replay.
`NOT_COMPLETED` after losing the owner is not proof that no SQL commit occurred;
normal subsequent ingestion still checks the accepted hash.

Ordinary failures preserve useful exception/warning information, end that request
and let later eligible work proceed. Source evidence remains under the existing
retention policy. Do not manufacture recovery requirements from hypothetical faults.

## 6. Shutdown and persistence

On graceful shutdown, stop admission, allow the executing database operation to
reach its safe boundary, close its resources and release ownership. Outstanding
work that does not finish becomes `NOT_COMPLETED`; it is not transferred.
On unexpected owner termination the in-memory queue disappears and outstanding
requests are not completed. Surviving callers can report loss of the owner; no
persisted terminal record or lookup through the next owner is promised.

A later caller can establish a new owner. Protected captures can be resubmitted
through normal startup/manual mechanisms, with existing duplicate checks. No
durable queue/result storage, SQL request tables, request files, receipts, recovery
journals, lost-acknowledgement protocol or automatic transfer of work between owners.
Durable outcomes remain SQL Runs/diagnostics, review artifacts and protected inputs.
No SQL/review schema change is required solely for this coordination feature.

## 7. Task 07 receiving repairs and integration

07D owns these bounded follow-ups identified by the receiving review:

1. **Complete runtime routing.** Refactor the direct repository use in
   `pipeline/ingestion.py`; integrate manual/API callers and the watcher submission
   adapter with the same handler. Replace the watcher's local ingest scheduling
   only as needed; preserve its lifecycle, startup resubmission, capture publication,
   warning delivery and daily retention. Do not leave integration as an unnamed
   team's unfinished prerequisite or retain a runtime bypass. Coordinate with the
   watcher owner if concurrent edits require it; live activation is separate.
2. **Reconcile outcomes.** Update CLI/API/watcher presentation and requirement checks
   for the three states, duplicate non-completion and waiting contention. Existing
   tests that expect capture contention to exit as failure or duplicates to be
   completed requests are superseded; tests are not product authority. Remove
   obsolete invalid-playset rejection guidance/branches where the current path
   cannot produce that outcome. Preserve genuine errors and playset warnings.
3. **Supply one current handoff.** Correct current API examples and documentation:
   exact SQLite file paths, `Database` APIs, schema/manifest 3, playset format 1,
   optional-playset handling and daily maintenance. Clearly separate historical
   Task 07 evidence from runnable instructions. Update README, the current task
   ledger, status/plan/execution order and continuation point. Do not leave the
   next team to reconcile several contradictory opening amendments.

Source/receiving checks have not established a need to replace classification,
aggregation, playset storage, the Run writer or retention. Extend their owners.
Retain learner findings and original review evidence without commissioning learner
work. Task 08 reports, Run-result replacement and full Trusted Run acceptance are
separate. No migration, legacy fallback, backwards-compatibility route or generation
replay. Preserve unrelated uncommitted work and the 06B rollback archive.

## 8. Required verification

Use disposable storage and complete genuine retained CK3 inputs. No fabricated
diagnostics or elaborate fault campaigns introduced to justify extra machinery.
Demonstrate:

1. Watcher/manual/API submissions, including separate processes, reach one owner
   and worker; database operations serialize instead of failing from internal
   contention. Include actual external SQLite contention and progress after release.
2. Watcher submission remains responsive during preparation, and a read can be
   served through the owner while preparation runs outside the database worker.
3. Duplicate ingestion returns `NOT_COMPLETED`, existing Run ID and a plain
   explanation, without parsing again or creating/replacing accepted Run data.
4. Successful reads/writes return `COMPLETED`, including a read with no match.
5. A genuine ordinary exception returns `NOT_COMPLETED`, reports its useful
   information and does not prevent later requests from completing.
6. Manual/API use establishes an owner without a watcher. Graceful shutdown
   releases ownership. After termination a new owner can start; normal resubmission
   of protected inputs respects accepted hashes without request recovery.
7. Current ingest/playset/SQL-review accounting and retained SQL rendering still
   work. Raw expiry retains its age policy and excludes inputs actively being read.
8. No durable requests, queue schema, parallel runtime SQLite path, new public
   lifecycle states, watcher service or reprocessing feature was introduced.

Distinguish source inspection, receiving checks, newly executed checks and historical
reported results. Carry native evidence gaps honestly; do not invent fixtures to
claim coverage. Do not operate production captures/retention, reset the live database,
change selection or restart/activate the watcher as verification.

## 9. Completion and escalation

Deliver working code, caller integration, focused verification and
`docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md`: final APIs, three-state lifecycle,
owner/worker lifetime, cross-process mechanism, supported repository operations,
ingestion and watcher integration, changed paths, checks and concrete limitations.
Update the current ledger so Task 07 delivered behavior and Task 07D remaining
work are unmistakable. Implementation/integration completion does not claim live
activation; identify the exact later operational step.

Do not stop after a design proposal or ask for routine design approval. If an
existing use case cannot be met within this direction, stop only that expansion
and report the concrete use case, exact failure and smallest additional mechanism
needed. Continue independent authorized work. Do not broaden the architecture
in anticipation of hypothetical needs.
