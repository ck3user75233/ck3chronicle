# Task 07E — Shared runtime logging and request traceability

## Owner correction to test guidance — 2026-10-02

The owner directed removal of synthetic and fault-injection checks, including
the pre-existing logging suite. `tests/test_runtime_logging_requirements.py` and
all seven of its test methods have been deleted. Do not restore those tests or
run the historical commands below expecting them to exist. The earlier test
counts remain historical records, not current acceptance evidence. The actual
source ownership checker `tools/check_runtime_logging.py` remains available.
No logging, handler or watcher runtime implementation was changed by this cleanup.

Delivered 2026-09-30; subsequently activated on explicit owner request at
00:27 UTC (08:27 Hong Kong). See the activation record below. The September 30
[07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) remains the receiving
API contract. Its **59 passing checks are inherited evidence**, distinct from
the fresh verification recorded below. No rejected handler design was used.

## Task 07E live activation - 2026-09-30 08:28 Hong Kong

Following owner authorization, the updated watcher was started hidden at
00:27:53 UTC. The previous PID was absent, its heartbeat was stale, the runtime
lease was free, and no old handler was listening. The exact configured database
passed read-only schema-3 verification. CK3 was already running, so the new
watcher attached to that process without interrupting the game.

Watcher PID 34340 (launcher 9792) observed CK3 PID 44816; a fresh heartbeat at
00:28:23 UTC confirmed `running`. Handler PID 308 reported `handler_ready`, with
instance `71d783fe8dc34ea6b4b0f7140de130b2`. Startup ingestion found all five
readable retained captures already stored and returned ordinary duplicate
non-completion. Twenty-two older inaccessible captures remain unavailable;
permissions were not changed. No watcher/handler ERROR events were observed;
bootstrap stderr was empty. Configuration, model selection and database identity
were unchanged; no reset or forced expiry was performed.

Evidence: ignored `.codex-tmp/task07e/activation.json`. Logs now use the 07E
paths in this handoff. The attached game's
exit was subsequently observed at 01:26:28 UTC and ingestion completed at
01:26:36 UTC as Run `20260930-BYVZUV`, request
`3f5002c984d94334b65205052b4916ed`. Its merged trace is retained under
`.codex-tmp/task07e/live-session-20260930-BYVZUV/`. Capture and ingestion took
7.657 seconds, with no warning/error/contention events for that request.
Attachment after game startup does not establish complete observed start-to-exit
Trusted Run acceptance. Task 08 and
Run-result replacement remain separate. The following implementation-delivery
checkpoint predates this separately authorized activation.

## Architecture and API

`src/ck3chronicle/runtime_logging.py` is the sole runtime logging owner. It uses
Python `logging` and `RotatingFileHandler`, without external dependencies.
Process entry points configure output and close it after their workers finish.
Components use `get_logger(component)` and `event(logger, name, **fields)`;
`level='WARNING'/'ERROR'` and `exc_info=True` use standard logging severity and
traceback support. `log_context(**fields)` scopes request fields on preparation;
`context_fields()` copies those fields into the existing database queue item.
This is observability metadata only, with no new request or persistence protocol.

The dedicated handler still owns one preparation thread and one database worker.
The listener binds exclusively **before configuring its rotating file**, so even
a direct second module launch cannot write to the live handler's file. All three
handler threads/components share that process output. CLI clients do not configure
a file and normal CLI JSON remains on stdout. The actual handler supplies their
runtime evidence. Direct `_Handler` construction is test infrastructure, not a
runtime configuration entry point.

`EventJournal` keeps its adapter API and existing watcher event vocabulary. Its
ordinary events now use the shared logger. The heartbeat remains the same
replaceable `watcher-heartbeat.json`, with the existing watcher PID, timestamp,
schema and cleanup behavior; heartbeat polls are not appended to JSONL.

## Files, settings and common fields

| Owner | File |
|---|---|
| Watcher holding the runtime lease | `<ROOT_CK3CHRONICLE>/watch/events-watcher.jsonl` |
| Watcher startup/lease failure | `<ROOT_CK3CHRONICLE>/watch/events-startup-<PID>.jsonl` |
| Handler, preparation and database worker | `<database-parent>/logging/<database-filename>/handler.jsonl` |
| Latest handler launch stderr | Same directory, `handler-bootstrap.log` |

The stable watcher file is bounded across restarts. Existing timestamped watcher
journals are untouched. Failed watcher launchers use their own PID file and do
not touch an active watcher's rotating file or heartbeat. Historical logs and
old failed-launch PID files are not automatically deleted by this task.

Optional repository-root `config.toml` settings (also in `config.example.toml`):

```toml
[logging]
level = 'INFO'
max_bytes = 10485760
backup_count = 5
```

Defaults are INFO, 10 MiB and five backups per rotating stream. Sizes/counts must
be positive integers; levels are DEBUG, INFO, WARNING, ERROR or CRITICAL. These
settings are read on process startup. The already-running handler retains its
settings until separately restarted. Rotation keeps `.1` through `.5`, with `.1`
the newest backup. A single record can exceed the size threshold; there is no
global byte quota, compression or archival service.

Ordinary records are UTF-8 JSON Lines with `timestamp_utc` (UTC ISO timestamp),
`severity`, `event`, `component`, `process_id`, and `thread_name`. Applicable
events add `handler_instance`, `request_id`, `operation`, `database`,
`enqueued_at`, `capture_directory`, `run_id`, `elapsed_seconds` and
`queue_wait_seconds`. Manual preparation starts with `error_log` when no protected
capture directory exists yet. The watcher retains `schema_version` and
`watcher_pid` for its existing consumers. Tracebacks are escaped inside one JSON
string, so each event still occupies one physical line.

## Events, correlation and timing

| Component | Meaningful events |
|---|---|
| Handler | `handler_started`, `handler_ready`, `handler_shutdown_started`, `handler_stopped`, `handler_failed` |
| Request | `request_accepted`, `request_completed`, `request_not_completed` |
| Preparation | `preparation_started`, `preparation_completed`, `preparation_not_completed`, `capture_wait_started`, `capture_wait_resumed`, `ingestion_warning` |
| Database worker | `database_opened`, `database_closed`, `database_open_failed`, `database_operation_started`, `database_operation_completed`, `database_operation_not_completed`, `database_wait_started`, `database_wait_resumed`, `database_write_uncertain` |
| Watcher additions | `ingestion_accepted`; existing completion/warning events now include the accepted handler request reference |

The handler's existing request ID is the sole correlation identity. Watcher
acknowledgement carries it with handler instance, capture directory, trigger,
database and enqueue timestamp. Preparation passes the same ID through internal
hash lookups and `write_run`; it is never replaced with a database-operation ID.
Watcher terminal events retain it. The handler records one terminal event for
each ordinarily finished accepted request, independently of result-cache eviction.
No events are emitted for status polls.

Monotonic clocks measure elapsed time. Request duration runs from admission to
terminal completion. Preparation queue wait ends when its thread starts work;
preparation duration includes capture waiting, validation, initial database
lookups and classification, and ends **before** final `write_run` submission.
Duplicates complete preparation without a write. Database queue wait and execution
duration are separate; execution duration includes internal contention/recovery.
A wait duration runs from the first observed contention until the operation
resumes successfully. Each waiting episode has one start/resume pair at INFO;
there is no 50 ms retry event. Internal connection reopens during uncertain-write
recovery are DEBUG to keep ordinary contention compact.

Normal progress and duplicate non-completion are INFO. Optional playset/debug
degradation and unavailable outcomes are WARNING. Actual failed operations and
unexpected exceptions are ERROR, with Python traceback evidence where the
exception is caught. A recoverable uncertain write is WARNING. Severity does not
change the public state. Existing watcher warning events remain warnings.

## Failures and preserved semantics

The launcher opens the bootstrap stderr file before starting the designated
module. It contains the latest launch attempt only (overwritten on the next
launch); stdout remains suppressed for this background process. Windows sharing
permits deletion after shutdown even while the venv launcher is briefly exiting.
Failure to create that file raises visibly to the caller. Import, listener or
logging-configuration failures before normal logging is available retain their
traceback there. Once configured, processing exception evidence belongs in
`handler.jsonl`. Admission errors opening SQLite also have `database_open_failed`
there. A failed watcher logging configuration reports on stderr and exits nonzero
if its startup journal is unavailable.

After startup, the shared file handler suppresses write/rotation/formatting errors,
like `logging.raiseExceptions=False` scoped to this handler. The event helper is
also best effort. No logging exception is allowed to fail a request or roll back
a committed Run. There is no disk-error recovery subsystem; events may be lost
while output is unavailable. The heartbeat's existing filesystem behavior is
unchanged. Bootstrap stderr is a small fallback, not a rotating operational stream.

07D's three states, unfinished-request retention, latest 256 terminal outcomes,
`LookupError` for missing results, `exception_class`, and internal-only
`cleanup_unaccepted` remain intact. `ingestion_outcome_unavailable` still clears
the watcher reference without creating an outcome or scheduling an eviction
retry. SQL/review/playset formats, input handling, queue order, retries, raw
retention and model selection are unchanged.

Abrupt process termination can leave accepted requests with no terminal event.
Missing log events are not proof of rollback, and logs are not a result-recovery
API. Rotation can remove old trace segments. No watchdog, hang termination,
resubmission, durable request trace or new background service was added.

## Operator queries

Run from the repository root. Obtain the configured paths without starting a
handler or processing captures:

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
$logPaths = & $python -B -c "import json; from ck3chronicle.config import ROOT_CK3CHRONICLE, watcher_settings; from ck3chronicle.runtime_logging import runtime_log_path, bootstrap_log_path; db=watcher_settings().database; print(json.dumps(dict(watcher=str(runtime_log_path(runtime_root=ROOT_CK3CHRONICLE)),handler=str(runtime_log_path(database=db)),bootstrap=str(bootstrap_log_path(db)))))" | ConvertFrom-Json
$files = Get-ChildItem -Path ($logPaths.watcher + '*'), ($logPaths.handler + '*') -File -ErrorAction SilentlyContinue
$events = $files | Get-Content -Encoding utf8 | ForEach-Object { $_ | ConvertFrom-Json }
```

Follow a known request across both processes and available rotations:

```powershell
$requestId = 'PASTE_REQUEST_ID'
$events | Where-Object request_id -eq $requestId | Sort-Object timestamp_utc |
    Select-Object timestamp_utc, component, event, operation, run_id, elapsed_seconds
```

Recent handler failures and their traceback:

```powershell
$events | Where-Object { $_.component -ne 'watcher' -and $_.severity -eq 'ERROR' } |
    Sort-Object timestamp_utc | Select-Object -Last 10 |
    Format-List timestamp_utc, event, request_id, exception_class, error, traceback
```

SQLite contention (optionally also filter `request_id`):

```powershell
$events | Where-Object { $_.event -in 'database_wait_started','database_wait_resumed' } |
    Sort-Object timestamp_utc | Select-Object timestamp_utc, request_id, operation, event, elapsed_seconds
```

Handler startup should show `handler_started`, `database_opened`, `handler_ready`
with one handler instance/PID. Absence of readiness may mean waiting or failure:

```powershell
$events | Where-Object { $_.event -in 'handler_started','handler_ready','database_open_failed','handler_failed' } |
    Sort-Object timestamp_utc | Select-Object -Last 10
Get-Content -LiteralPath $logPaths.bootstrap -ErrorAction SilentlyContinue
```

## Developer enforcement and verification

Future runtime code uses the shared owner; do not create feature handlers,
formatters, rotation policies or destinations. `tools/check_runtime_logging.py`
AST-checks all `src/ck3chronicle` Python files except the canonical owner. It flags
configuration calls, including imported aliases of `basicConfig`, `FileHandler`,
`RotatingFileHandler`, other common handlers/formatters and attachment/configuration
methods. Tests and research/support tools are outside this runtime-source rule.
It is transparent, cheap enforcement, not a general linter or protection against
deliberate dynamic evasion.

```powershell
& $python -B tools/check_runtime_logging.py
$env:CK3_TASK07_EVIDENCE = (Resolve-Path '.codex-tmp/task07e/evidence.json').Path
& $python -B -m unittest discover -s tests -p test_runtime_logging_requirements.py -v
```

Fresh combined verification passed **66 checks with no failures, errors or skips**
in **86.156 seconds**: all 59 receiving checks were rerun and seven focused 07E
checks were added. The seven cover end-to-end watcher and manual ingestion,
accepted/terminal correlation, worker correlation, actual capture/SQLite lock
episodes, preparation versus write timing, INFO duplicate non-completion, CLI
JSON without contamination, durable exceptions followed by successful requests,
real pre-configuration startup failure, exclusive ownership on direct second
launch, graceful closure, heartbeat replacement, valid UTF-8 JSONL rotation,
committed Runs surviving logging-write failure, and static enforcement including
aliases. The receiving cases also recheck unavailable-result handling, bounded
retention, public cleanup refusal, SQL/review agreement, optional playsets,
disposable raw expiry and unchanged lifecycle behavior.

The combined patterns are `test_database_handler_requirements.py`,
`test_database_handler_hardening_requirements.py`,
`test_ingestion_retention_requirements.py`, `test_watcher_ingestion_requirements.py`,
`test_database_initialization_requirements.py`, `test_watcher_capture_requirements.py`,
`test_playset_capture_requirements.py`, and `test_runtime_logging_requirements.py`.
Run each through unittest discovery with the evidence environment variable above;
the ignored `verify.py` also reproduces the combined run. Isolated imports,
`pip check`, and the standalone static check passed.

The initial integration pass exposed a Windows bootstrap handle cleanup race;
the owner now opens stderr with read/write/delete sharing. A manual capture
publication reported a Windows access-denied error in that pass; the full rerun
passed without changing capture behavior. That first pass is retained as
`verification-first-pass.*`, rather than counted as successful evidence. Early
instrumentation/runner errors were corrected before the final combined run.

Evidence is ignored under `.codex-tmp/task07e/`: `evidence.json` names genuine
retained inputs and disposable output; `verification.txt` and `verification.json`
record the receiving run. Per-exercise directories contain JSONL and disposable
databases. Runtime checks create no fabricated CK3 diagnostics.

`request-trace.json` gives a concrete successful watcher trace:
request `4b4d68edbe224a69a3afc322b442a705`, handler instance
`e3c8ac371a7340a3b5923a5f8a02e2a7`, Run `20260929-MAR2IR`.
The trace records capture waiting, hash lookup, preparation (3.047 seconds),
final database write (0.500 seconds), and terminal completion. Its source watcher
and handler files are under the disposable
`51b4f2739b1c42bcb53ebcd13b1819b5` exercise directory. These measured durations
are examples, not performance requirements.

The full three-log receiving campaign is
`.codex-tmp/task07e/11b70c8addd6408cbfd4fb6be2fd139b/results.json`.
No live watcher activation, power-loss durability, OS-wide disk exhaustion or
arbitrary Windows security/session configuration was tested. Write failure was
injected at the real rotating handler while genuine ingestion committed; startup
failure used an actual unusable log-file path. These are focused checks, not a
claim that operational logs can never be lost.

Changed implementation: new `runtime_logging.py`; integration in `watcher.py`,
`watcher_processing.py`, `pipeline/request_handler.py`,
`pipeline/database_handler.py`, `pipeline/ingestion.py` and watcher CLI startup
failure reporting. New ownership check and logging tests accompany the updated
watcher test request-reference fixtures and example logging settings. Current
status/plan/handoff, task ledger, README and AGENTS guidance point here. The
pre-existing broad dirty tree, removed providers and selected models were preserved.

## Separate activation procedure - executed in the later activation above

1. Choose a quiet boundary with CK3 closed, completed capture publication and no
   in-flight ingestion. Keep other manual/API submitters idle through the restart.
   Read the actual current heartbeat/process command line; historical PIDs in
   earlier handoffs are not current identities. Check the existing `config.toml`
   database path and desired `[logging]` settings. Defaults need no config edit.
2. Stop the identified watcher. Use Ctrl+C for an attached console and let its
   processing close finish. For the existing hidden watcher there is no stop API;
   at the verified idle boundary, stop only its confirmed PID with
   `Stop-Process -Id <verified-watcher-PID>` and wait for that process to exit.
   Do not stop all Python processes or CK3. A forced stop does not promise a
   shutdown event and must not be used during capture/publication.
3. Shut down any old handler for the configured file, using the existing API:

   ```powershell
   Set-Location 'C:\Users\nateb\Documents\ck3chronicle'
   $python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
   & $python -B -c "from ck3chronicle.config import watcher_settings; from ck3chronicle.pipeline.request_handler import HandlerClient; HandlerClient(watcher_settings().database).shutdown()"
   ```

4. With runtime users stopped, verify that exact existing database read-only.
   This refuses incompatible storage; it does not initialize/reset/migrate:

   ```powershell
   & $python -B -c "from ck3chronicle.config import watcher_settings; from ck3chronicle.pipeline.repository import open_database_readonly; db=open_database_readonly(watcher_settings().database); print(db.path, db.metadata); db.close()"
   ```

   Stop if the check fails. Do not select a different file or package implicitly.
5. Start the updated watcher from this checkout, hidden as before:

   ```powershell
   Start-Process -FilePath $python -ArgumentList '-B','-m','ck3chronicle.cli','watch' -WorkingDirectory 'C:\Users\nateb\Documents\ck3chronicle' -WindowStyle Hidden
   ```

6. Inspect the new watcher log, replaceable heartbeat and handler startup events
   with the queries above. Startup scanning performs ordinary ingestion and
   duplicate checks; the handler starts lazily when a request is submitted. If
   there are no submissions, lack of handler events alone is not a startup failure.
   Existing daily maintenance remains due after its configured interval; do not
   force an expiry pass as activation verification. A real subsequent CK3 lifecycle
   should show `ingestion_accepted` and terminal outcome with matching request ID.

The original implementation delivery did not operate live processes, change production configuration
or selection, ingest production captures, reset databases or expire production
files. The later owner-authorized startup performed normal duplicate checks as
recorded above, without configuration changes, reset or forced expiry. No commit or push was made. Task 08 SQL reports, Run-result replacement,
and complete Trusted Run acceptance remain separate assignments.
