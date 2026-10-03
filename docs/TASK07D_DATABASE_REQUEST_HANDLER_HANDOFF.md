# Task 07D — current database and ingestion handoff

Updated 2026-09-30 after the bounded 07D hardening follow-up. This is the
current executable reference for Task 07/07D callers.
The [07E handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md) now supplies shared logging,
bootstrap diagnostics, operator queries and the separate combined activation step.
The original Task 07 and watcher activation documents retain historical evidence;
their former directory arguments, local ingestion executor and result vocabulary
are superseded here. The rejected handler design and continuations were not used.

## Delivered boundary

Watcher, manual CLI and application clients use `HandlerClient` in
`pipeline/request_handler.py`. All reach the dedicated
`python -B -m ck3chronicle.pipeline.database_handler <exact-sqlite-file>` process.
No ordinary caller hosts the handler or opens a repository. The dedicated host
owns one in-memory database queue and one database worker thread; that thread
opens, uses and closes its sole runtime connection and `Database`.

One preparation thread in that host consumes ingestion submissions serially.
Hashing, protected copying, model loading, parsing and classification run there,
outside the database worker and transactions. Its lookups and complete
`Database.write_run` calls use the worker queue. Reads can run during preparation.
Serial preparation also prevents concurrent submissions of the same previously
unseen content from parsing twice. SQL still enforces the final duplicate check.
No priorities, SQL statement scheduling, read connections or parallel database
workers were added. No SQL or review format changes were needed.

`Database.write_run` retains its existing accounting, staging, transaction,
two-file review publication and commit boundary. On temporary SQLite BUSY/LOCKED,
the worker waits internally and retries the complete eligible operation. Prepared
input is retained, so final-write contention never repeats classification.
After a `RunWriteError`, the worker closes/reopens its connection, checks the
content hash and preserves accepted evidence before considering another write.
An accepted Run from that publication is returned; a competing accepted hash is
a duplicate. Unaccepted published evidence uses existing guarded cleanup.
An ordinary exception ends its request and does not poison subsequent work.

## Startup, transport and shutdown

The canonical resolved, case-normalized database file path determines one Windows
named-pipe address. Clients send JSON bytes using Python's `AF_PIPE` transport;
there is no pickle, arbitrary SQL or repository-object transport. The host binds
the exclusive first pipe instance before opening SQLite. A Windows launch mutex
serializes callers' availability checks and process launches only. It never
assigns the handler role or database work to a caller.

`submit` probes the pipe. If absent, it starts the same designated module using
the current Python executable with `CREATE_NO_WINDOW`, then connects. The host
continues after the launching caller exits; no watcher or permanent Windows
service is required. Existing/incompatible database errors are reported directly
at admission, without initialization, migration, discovery or fallback.

An ordinary client has no resource-owning close operation. The infrastructure
operator can explicitly call `HandlerClient(database_file).shutdown()`. Shutdown
stops admission, lets an executing database operation reach its safe boundary,
rejects unfinished work, releases capture locks, closes SQLite and exits. A
subsequent submission may start a fresh instance of the same module. References
from an earlier instance never cause work to be resubmitted or transferred.

Unexpected termination loses the in-memory queue. Surviving clients report
`NOT_COMPLETED` when that instance is unavailable. This does not prove a write
was rolled back. Normal resubmission checks accepted hashes. Only Runs,
diagnostics, review artifacts and protected captures are durable; no request
tables/files, receipts, journals, recovery protocol or automatic transfer exists.

## API and outcomes

```python
from pathlib import Path
from ck3chronicle.pipeline.request_handler import HandlerClient, COMPLETED
from ck3chronicle.pipeline.ingestion import ingest, ingest_result

database_file = Path(r'C:\evidence\runtime\ck3chronicle-schema3-20260929T120000Z.sqlite3')
client = HandlerClient(database_file)
ref = client.submit('ingest', {'capture_directory': Path(r'C:\evidence\pending\CAPTURE')})
print(ref.enqueued_at, client.status(ref))
snapshot = client.wait(ref, timeout=0.1)
# A timeout leaves ENQUEUED unchanged. result(ref, timeout=...) raises TimeoutError
# only when that caller's wait expires; result(ref) waits for a terminal envelope.
outcome = client.result(ref)
received = ingest_result(outcome)
print(received.status, received.run_id, received.warnings, received.error)

read = client.result(client.submit('latest_run'))
if read.status == COMPLETED:
    print(read.value)  # None is a successful read with no matching Run.

# Synchronous convenience; uses precisely the same submission/result path.
received = ingest(database_file, error_log=Path(r'C:\evidence\retained-error.log'),
                  captures_root=Path(r'C:\evidence\pending'))
```

`RequestRef` contains `instance`, `request_id`, and UTC `enqueued_at`. `submit`
returns only after acceptance. Admission failures raise directly.

The handler retains all unfinished requests plus the **256 most recently completed
terminal requests**, including both `COMPLETED` and `NOT_COMPLETED`. Completion
order determines eviction; reading an outcome does not refresh it. The fixed limit
counts requests, not bytes. There is no timer, release API, configuration setting,
size accounting or durable storage. An existing waiter holds the request object
independently and can receive its result after lookup-cache eviction.

Lookup of a result not retained by the connected handler (including an earlier
handler instance's reference) returns a transport `result_unavailable` response.
`status`, `wait` and `result` raise ordinary client-side
`LookupError("request result is no longer retained by this handler")`.
This is a lookup condition, not `NOT_COMPLETED` and not a fourth public state.
No automatic resubmission or outcome reconstruction follows eviction. Connection
loss still follows the existing handler-termination behavior described above;
a replacement host cannot recover the old reference.

Exactly three public states exist:

| State | Meaning |
|---|---|
| `ENQUEUED` | Accepted; includes preparation, queue waiting, execution and contention retries. |
| `COMPLETED` | Operation succeeded, including an empty/None read. |
| `NOT_COMPLETED` | Duplicate, unavailable input, ordinary exception or unfinished work at termination. |

`wait` and terminal `result` return `RequestResult(status, value, error,
exception_class, details)`. Ordinary exception text/type and available capture or
publication references are data, not a new failure classification system. The Python exception field
is named `exception_class` in 07D request/ingestion results and their CLI/watcher
consumers. Error Contract/SQL diagnostic `error_type` and unrelated historical
watcher-event schemas are unchanged; no legacy outcome-field alias is provided.
JSON results contain dictionaries/lists/scalars; resolved paths are strings.
`ingest_result` converts ingestion values to `IngestResult`, including its
existing `RunResult`/accounting/review dataclasses and Path capture reference.
`ingest` returns that same three-state ingestion result. Operation exceptions
after acceptance produce `NOT_COMPLETED` outcomes containing exception information.
An unavailable result lookup instead raises `LookupError`, as described above.

Duplicates return `NOT_COMPLETED`, the existing Run ID/hash and a plain warning.
They do not load the requested package, parse again, replace results or create a
manual copy. The package argument cannot override accepted content. A successful
standalone hash lookup remains `COMPLETED`.

Supported public operations, using the existing repository keyword arguments:
`metadata`, `find_run_by_log_hash`, `get_run`, `list_runs`, `latest_run`,
`read_diagnostics`, `read_playset`, `read_review_metadata`,
`resolve_review_reference`, and the composed `ingest`. Public
`cleanup_unaccepted` submissions are rejected at both client and host admission;
the repository guard and the worker's internal uncertain-write cleanup are unchanged.
Prepared `write_run` is an internal complete database operation; raw/classifier
objects never cross the client pipe. `cleanup_staging` is excluded because its
existing contract requires all writers stopped. No generic SQL operation exists.

## Storage, manual command and watcher

### Source modification timestamp receiving check — 2026-09-30

The existing path preserves the watcher's original `error.log` modification
timestamp exactly:

1. `pipeline/ingestion.py::_ingest` reads the existing
   `directory / "capture-metadata.json"` into `metadata`.
2. It submits `database_call('write_run', ..., facts=metadata)` through the
   dedicated handler's existing database worker queue.
3. `repository.py::Database.write_run` uses `schema.encode(facts)` (JSON string
   serialization) and inserts it into `runs.facts_json`.
4. `Database._run` JSON-decodes `facts_json` into `facts`; the handler's JSON
   transport preserves that string in public Run results.

For example, the public read is:

```python
outcome = client.result(client.submit('get_run', {'run_id': run_id}))
if outcome.status == COMPLETED:
    run = outcome.value
    source_modified_at = run['facts'].get('error_log_source_modified_at')
```

When supplied, `run["facts"]["error_log_source_modified_at"]` is the exact
string, including all nine fractional digits, for example
`2026-09-28T04:44:46.950967600+00:00`. `latest_run`, `list_runs` and
`find_run_by_log_hash` expose the same facts. No parsing, reformatting,
protected-copy stat lookup or timestamp substitution occurs on this path.
Missing historical/manual values remain unavailable (the key is absent when
not supplied); they neither reject valid inputs nor trigger backfill.
`process.started_ns` and `captured_at` retain their existing meanings. Run-ID
timing remains independent, and retention still reads `captured_at`.
Ordinary hash duplicates return before metadata loading/writing; the repository
also rejects an already stored hash before inserting a Run.

**Inherited evidence reviewed, not rerun:**
[WATCHER_SOURCE_MTIME_HANDOFF.md](WATCHER_SOURCE_MTIME_HANDOFF.md),
`tests/test_capture_source_mtime_requirements.py`, and its ignored
`verification.txt`, `verification.json` and native `result.json` record 43
passing checks. They include genuine source capture/publication, exact metadata
equality in SQL, repository Run readback, unchanged-metadata duplicate handling,
destination-mtime independence and unstable-source rejection. The included
ingestion/retention checks also exercised historical/manual inputs without this
field. Source review confirms missing values are neither required nor invented.

**Receiving checks actually run:** two focused checks passed, with no failures,
errors or skips (1.235 seconds), using a read-only SQLite backup of the inherited
disposable database and a fresh disposable copy of its capture. Public
`HandlerClient` reads through all four Run operations above returned the exact
timestamp and complete original facts. Duplicate ingestion after changing only
the disposable capture's timestamp to `2001-02-03T04:05:06.123456789+00:00`
returned `NOT_COMPLETED`, preserved the entire previously read Run, and left
one Run stored. Only the disposable handler was started and shut down.

Reproduce with
`.\.venv\Scripts\python.exe -B .codex-tmp/pipeline-source-mtime-receiving/verify.py`.
Actual results are ignored under
`.codex-tmp/pipeline-source-mtime-receiving/a94bc22228404039bec69a2fce60c2ce/`
in `verification.txt` and `verification.json`. This receiving pass did not repeat
capture/new-Run processing or the broader watcher suite; the backup retained
inherited Run `20260930-CWO6LH`.

No preservation gap was found. No implementation, metadata file contract, SQL
column, schema version or persistence route changed. No production ingestion,
live restart, historical mutation, commit or push occurred.

### Existing storage and caller contract

Explicit one-time initialization remains the existing repository API:

```python
from pathlib import Path
from ck3chronicle.pipeline.repository import create_database
with create_database(Path(r'C:\evidence\runtime')) as database:
    database_file = database.path  # persist this exact path in configuration
```

`create_database`, `open_database`, `open_database_readonly` and `Database` remain
the low-level owning APIs for explicit initialization/offline verification.
Ordinary runtime reads use the handler, including future Task 08 reporting.
Open/ingest arguments are exact existing SQLite **file paths**. SQL schema and
native-review manifest are **3**; producer playset format is **1**. Processing
lineage belongs to each Run. No database-wide package restriction was restored.

```powershell
.\.venv\Scripts\python.exe -B -m ck3chronicle.cli ingest --database C:\evidence\runtime\ck3chronicle-schema3-20260929T120000Z.sqlite3 --capture-directory C:\evidence\pending\CAPTURE
```

CLI JSON uses these three states. Exit 0 means `COMPLETED`; exit 1 means terminal
non-completion (including duplicate), failed admission or unavailable result
retrieval. Admission/retrieval errors go to stderr without a fabricated request
state; available accepted outcomes go to stdout with
warnings and ordinary error details. Retry failed protected manual input using
the returned capture directory, rather than creating another copy.

Missing playsets store the existing unavailable value. Invalid supplied playsets
produce that same value plus a warning; supplied JSON is preserved and the valid
error log proceeds. Optional debug/playset capture failure still permits error-log
publication. There is no obsolete invalid-playset rejection exit path.

The watcher dispatch thread admits startup/post-publication requests and runs
daily maintenance. A result monitor delivers warnings and terminal outcomes;
it does no ingestion or SQL work. Queued/preparing requests do not hold up later
admissions or daily retention. Duplicates emit `ingestion_not_completed` with the
existing ID/warning; ordinary failures remain visible and eligible for the
existing maintenance/startup retry paths. Lifecycle observation, publication and
journal ownership remain with their existing components. Watcher close waits
for submitted results but does not shut down the shared handler. A `LookupError`
from result retrieval instead emits `ingestion_outcome_unavailable`, with the
request/handler reference and explanation but no success/non-completion status.
The stale pending/scheduled reference is removed and eviction does not place the
capture on the maintenance retry list. Later ordinary startup scans retain their
existing behavior; no durable request recovery was added.

Defaults remain `maintenance_hours = 24`, `retention_days = 30`, with exact
database-file configuration. Retention is a filesystem operation, independent
of SQLite. It uses original capture time and the existing capture lock. Inputs
being hashed/parsed/published are protected; untouched queued captures can expire.
Metadata, playsets, SQL and review artifacts survive raw expiry.

## Verification and limits

The September 30 hardening verification passed **59 checks, no failures, errors
or skips**, in 162.549 seconds. Isolated imports and `pip check` passed. Six new
checks in `tests/test_database_handler_hardening_requirements.py` cover unfinished
request retention, both terminal outcomes counting toward the fixed bound,
eviction at the 257th completion, completion ordering unaffected by lookups,
an already-waiting caller receiving an evicted result, real named-pipe
`LookupError` mapping through status/wait/result, client and server rejection of
public cleanup, the scoped exception-field rename through CLI/ingestion results,
and watcher outcome-unavailable handling without retry. Existing handler,
ingestion/retention, watcher, initialization and capture/playset checks also passed,
including native SQL/review agreement and the worker's internal guarded cleanup.

Evidence is ignored under `.codex-tmp/task07d-hardening/`: `verification.txt`,
`verification.json`, `evidence.json`, and the native campaign
`b08ffa5a69684b18beb98d692c5a2ef2/results.json`. All outputs and expiry checks used
disposable storage. No production data, configuration, package selection or live
watcher was changed. Reproduce with the same discovery patterns below plus
`test_database_handler_hardening_requirements.py`, setting `CK3_TASK07_EVIDENCE`
to the hardening evidence JSON.

Hardening changed only `pipeline/database_handler.py`, `pipeline/request_handler.py`,
`pipeline/ingestion.py`, ingest CLI output, watcher outcome consumption, relevant
checks and current documentation. The repository's cleanup implementation and
uncertain-write policy, diagnostic schema and unrelated watcher fields are intact.
No bootstrap-logging code was added.

The original September 29 combined run passed **53 checks, with no failures, errors or skips**:
8 handler checks, 2 native ingestion/retention checks, 9 watcher ingestion checks,
3 initialization checks and 31 capture/playset checks. Isolated imports and
`pip check` also passed. All writes and expiry checks used disposable storage.
Complete genuine retained CK3 logs supplied native evidence; no diagnostics were
fabricated. Earlier receiving/activation counts are historical and are not counted
as newly executed 07D checks.

The handler checks exercised simultaneous separate-process startup, one host and
worker, API/watcher/CLI sharing, actual external SQLite contention, timeout without
state change, ordinary failure followed by successful work, successful empty reads,
graceful shutdown and termination/restart. Native checks covered reads during paused
preparation, active-input exclusion versus queued-input expiry, final-write waiting
without repeated preparation, and safe completion of an executing publication
during shutdown. A duplicate requested with an unavailable package completed no
ingestion and returned its existing Run, establishing pre-model duplicate lookup.
The three-log Task 07 campaign rechecked per-Run lineage, ordered playsets,
SQL/review accounting, exact native review output and SQL rendering after raw expiry.

Ignored evidence: `.codex-tmp/task07d/verification.txt`, `verification.json`, and
the three-log campaign `ba923dabde824145a494a66dc66bdbc0/results.json` under that
directory. `evidence.json` records the retained-input selection and disposable
output root. Reproduce with the repository Python and unittest discovery over
`test_database_handler_requirements.py`, `test_ingestion_retention_requirements.py`,
`test_watcher_ingestion_requirements.py`, `test_database_initialization_requirements.py`,
`test_watcher_capture_requirements.py`, and `test_playset_capture_requirements.py`;
set `CK3_TASK07_EVIDENCE` to that evidence JSON for the native ingestion suite.

Changed source: new `pipeline/request_handler.py`, `pipeline/database_handler.py`;
updated `pipeline/ingestion.py`, `watcher_processing.py`, CLI result presentation,
and connection-setup cleanup in `pipeline/repository.py`. Current requirement
checks and current documentation/ledger were reconciled. The substantial
pre-existing dirty tree, models, selection and runtime configuration were preserved.

Windows local IPC is the implemented platform. The 256-terminal-request cache
bounds retained request count, not individual result size or unfinished work.
A programming hang can remain `ENQUEUED`; there is no watchdog
or cancellation API. Installed-wheel packaging, OS power loss, arbitrary Windows
security/session configurations and the live watcher were not exercised. Native
coverage does not claim every parser recovery or playset shape.

**Historical 07D limitation, resolved by Task 07E:** bootstrap stderr formerly
went to `DEVNULL`. The [07E delivery](TASK07E_RUNTIME_LOGGING_HANDOFF.md) adds
durable bootstrap stderr, shared rotating runtime logs, request correlation and
tracebacks. The 59-check receiving result above remains 07D evidence; fresh 07E
verification is recorded separately in that handoff. Live activation is separate.

Implementation is separate from live activation. The later operational step is
to verify the intended existing schema-3 file, stop the old watcher safely, shut
down any old handler for that file, and start the watcher on this updated code.
Its startup submissions then perform normal duplicate checks. No production
database reset, raw expiry, package change or live restart was performed here.
Task 08 reports, explicit Run-result replacement and complete Trusted Run
acceptance remain separate work.
