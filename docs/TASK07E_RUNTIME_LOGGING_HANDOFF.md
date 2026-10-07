# Task 07E — Shared runtime logging and request traceability

**Current direction — 2026-10-07:** the Owner ordered Observer deletion.
[Pipeline replacement receiving](learner-next-release/OBSERVER_FREE_PIPELINE_RECEIVING.md)
records the cleaned backend, replacement artifact and actual receiving status.
Observer lifecycle and sole-stream confirmations in earlier sections are superseded
requirements, not passed checks. The required Watcher capture/timestamp/playset/
processing path is independent, as documented in the
[dependency review](WATCHER_OBSERVER_DEPENDENCY_REVIEW.md). CK3Chronicle execution
logging remains required. Historical delivery evidence below is preserved;
Observer-bearing artifacts are not the replacement candidate. External physical
placement remains a separate unresolved receiving obligation.

## TREK-6 Observer-free replacement — 2026-10-07

Fresh candidate: `.codex-tmp/trek6-removal-20261007/application/ck3chronicle-0.0.1-py3-none-any.whl`,
SHA-256 `1a325cd40eb29878e6c7c44a25615ea3eb3e47e4173eb6b72c3d6f8e596fb7ae`. Clean stage:
`.codex-tmp/trek6-removal-20261007/deployment`. Application identity:
`application-source-sha256:eb41a2f7aee62c55004e642e35deccb6f89c2233042f8be1af76b5246602924b`.
Learner `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485` /
manifest pin `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e`.
All 605 source/wheel/installed members correspond, all eight retained releases
authenticate, and Observer is absent including embedded copies. Approved defaults
and historical artifacts are preserved. Installed genuine Reporting yields 13
output comparisons, 15 normal call pairs and 64 real request links, plus the
default-console request. Catalog administration and retained isolated help log
one start/finish pair each. No production restart/activation.

**Receiving remains open:** Learner CMT-44 has not yet delivered genuine evaluation
for the changed identity; physical external payload placement also remains
unverified under checkout-only write access. Retained help is not evaluation.
Observer checks are superseded, not passed. Rotation/exception/periodic gaps stay
disclosed. Exact results, journal paths, raw measurements, per-record dispositions
and rollback are in [the consolidated receiving handoff](learner-next-release/OBSERVER_FREE_PIPELINE_RECEIVING.md).

## TREK-6 installed combination — required receiving open — 2026-10-06

Pipeline's fresh application wheel SHA-256 is
`cfdb38f68bbf0ed84ec326bf18951349411c53c6f5094bc884ce52bdc87b6dea`, at
`.codex-tmp/trek6-packaging-20261006/application/ck3chronicle-0.0.1-py3-none-any.whl`.
All 606 code/resource members match source, wheel and separate installation in
both directions, including the retained Learner backend/adapter and administrative
launcher. No backend, observer, foreground, Reporting or Learner source was edited
by packaging. Default model and current configuration remain unchanged.

Installed genuine receiving passed 13 Reporting output comparisons, 15 scope pairs,
64 matched foreground request references plus one default-console reference,
all 44 preserved-byte occurrences, retained config-free evaluation and 13 console
commands. Only the task-started disposable handler was shut down. Runtime ownership
and installed dependency checks pass. See the [full Pipeline receipt](learner-next-release/PIPELINE_RECEIVING.md#trek-6-final-packaging--bounded-installed-receipt-required-checks-open--2026-10-06)
for exact sources/pins, results, raw measurements, verifier corrections and rollback.

**TREK-6 remains open.** Physical external payload placement is unavailable within
the session's writable checkout boundary. A fresh 21:04:51 Hong Kong process probe
found no CK3; installed observer/root execution and required natural lifecycle remain
unverified. Watcher's final caller/sole-stream confirmation remains on TREK-3/4.
Previous bounded genuine attachments and unchanged lifecycle evidence are reused
only within their limits; they do not certify changed installed execution.
Periodic/rotation and exceptional cases remain unrepresented as specified in plan G.
No owner acceptance, production activation/restart or project-wide completion is
inferred. Existing operator paths, queries and prior handoff sections remain valid.


## TREK-4 Pipeline foreground integration — 2026-10-06

**Implemented and verified on bounded genuine reads; consuming receipt remains
open.** The owner issued [Pipeline Integration](task09-deliverables/PIPELINE_INTEGRATION.md)
in the Pipeline chat on this date. TREK-4 stays `in_progress` through Reporting
receipt and Watcher compatibility disposition. Final Packaging is separate.
Earlier prepared/todo planning text is historical; the protected record carries
the current checkpoint. This delivery adds no new backend or component scopes.

### Configured foreground interface

After successful argument parsing, root `capture`, `ingest`, `runs`, `report` and
`doctor` dispatch through `_foreground(args)`. Their subcommands accept
`--log-dir PATH`; explicit paths resolve from the caller's cwd. The default is
`config.ROOT_CK3CHRONICLE / 'logging'`, using the existing configured path authority
and `runtime_logging.logging_settings()` validation. Shared `invocation_log_path`
names `<command>-<invocation_id>.jsonl`. Task 10 remains an eventual interface
supplier; no installer, configuration authority or doctor behavior was changed.

Setup opens one shared handler before dispatch; failure propagates without a
fallback. `log_context(invocation_id=..., foreground_invocation=True)` surrounds
actual dispatch, making existing component events and Reporting's future journal
scopes durable in that file. `invocation_started` records the operation, actual
source path and journal path. No input/model/application hash or lazy property is
computed for logging. `invocation_finished` reports the observed return code;
caught component failures keep their original nonzero code and error ownership.
Escaping `SystemExit`, interrupts and other exceptions are re-raised, with one
terminal observation; only the latter add the boundary's traceback. Context is
restored on exit and handler cleanup cannot replace the substantive outcome.
No argument dump, per-call identity or scope/context transport was introduced.

`watch` and `observe-logging` still dispatch directly. Their command bodies are
AST-identical to the saved baseline; neither gets a foreground flag, second
handler, call scope or terminal pair. `watch --once` also stays on its original
route. The observer/backend/adapter retain the exact received source hashes.

Standalone `pipeline.catalog.main` accepts `--log-dir PATH` **before** its
subcommand. It already uses no application configuration and retains that property:
default `<cwd>/.ck3chronicle/wip/model-release-logs`, file
`model-release-<invocation_id>.jsonl`, shared config-free settings. Dispatch alone
gets setup/start/outcome/cleanup. Listing, selection, registration and evaluation
algorithms are unchanged; no evaluator scope or post-write checkpoint was added.
Root/catalog stdout and stderr receive no new announcement. Help performs no
logging setup and remains configuration-independent.

The [07D section](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md#trek-4-foreground-request-links--2026-10-06)
documents the one foreground `request_accepted` event. It uses the real returned
reference and preserves Watcher's independent acceptance evidence and silent polls.

### Coordination, incoming receipt and ownership

Consumed Learner's CMT-9/CMT-12 coordination: the checker now also covers
`learner_loader.py`, `artifacts.py`, `records.py` and
`incremental_template_registry.py`; TREK-1's adapter/import-closure enforcement
is preserved. Static ownership does not authenticate retained copies or prove
isolated execution. Pipeline separately authenticated all 48 payloads of Learner
release `9c02a343c389aed3d6a4b679b10ac5df01d7dca76e8b1eb991f5138b09c1af12`
at external manifest pin
`0edc5b9e2149e0a64cd360502bbdfe74f3b9ff6753c76230e73dd93794cadfd3` and matched
the shared bytes to the current delivered backend/adapter. TREK-2 records that
interface receipt while retaining installed/external-placement follow-ups.
Unchanged genuine Learner two-log/isolated-execution evidence is reused with its
original limits; no training or immutable release creation was repeated.

Applied Learner's exact proposed RELEASES wording after verifying its source pin.
Git's patch application rejected the hunk despite that matching pin; direct
newline-aware application preserved the supplied wording. Watcher's delivered
07E section is preserved intact. Its bounded genuine observation and unchanged
lifecycle evidence are reused; final root caller/stream confirmation remains
Watcher-owned. Reporting TREK-5 was still prepared at intake; this delivery makes
its authorized future foreground integration possible without closing TREK-4.

### Genuine verification and limits

Evidence root **P4**: `.codex-tmp/trek4-pipeline-20261006/` (ignored). Commands and
raw stdout/stderr are in `before-output/`, `baseline-supplement/`, `after/` and
`commands.py`; `output-review.json` records the exact commands/cwd and assertions.
Only the existing disposable genuine receiving database was used. Examples:

```powershell
# From the existing disposable receiving config context; DB is the 07D path above.
python -B -m ck3chronicle.cli runs --database $DB --package-id 4ac4e8ee92346e6d14eacfbf --format json --log-dir $LOGS
python -B -m ck3chronicle.cli report 20261005-BND9AS --database $DB --preset frequent --format json --limit 5 --log-dir $LOGS
python -B -m ck3chronicle.cli report 20261005-BND9AS --database $DB --custom --query $P4/source-query.json --format json --verbose --log-dir $LOGS
python -B -m ck3chronicle.pipeline.catalog --log-dir $LOGS list
```

Actual commands use the repository `.venv/Scripts/python.exe`; paths/arguments
are fully recorded in the JSON evidence. Eighteen changed-code CLI commands
returned zero: genuine catalog list/selection, Run listing JSON/text, frequent
report JSON/text with history, verbose hotspots HTML/linked source appendix,
missing-source-time reporting, source-content query and nine help variants.
Ten output comparisons passed, excluding only labelled report-generation times
and named source-search duration measurements. JSON diagnostic/native/history/
source payloads, text/HTML contents, export paths and stderr otherwise agree.
The real content query on captured-playset file
`common/scripted_triggers/99_tct_scripted_triggers.txt`, literal
`saintdays_province`, retained 12 records / 49,853 occurrences, complete source
coverage and actual current-file content/excerpts. No fake source path was used.

Eleven reviewed journals each contain exactly one start/terminal pair; 50 unique
foreground acceptance references exactly match real handler acceptance and
completion. No journal adds an argument dump or traceback. The existing genuine
new-package syntax restriction was also exercised against the same stored Run:
both baseline/current return code 2 and the same `invalid_query` output; the new
terminal truthfully says `nonzero_exit`, code 2. This is an unchanged documented
Reporting limitation, not a newly failed acceptance check. Config-free catalog
listing with an explicit writable destination and root help also ran from
`C:/Windows`. Default and explicit journal destinations were both observed.

The initial baseline's first seven commands dispatched before the source edit;
missing-time/help were independently rerun from exact saved source to remove
timing ambiguity. The source query also used that preserved baseline entry.
No client or context was mocked/injected. A slow exploratory text diff was replaced
by bounded normalization/comparison; only the saved review is acceptance evidence.

`python -B tools/check_runtime_logging.py`, compile/AST boundary review and scoped
whitespace checks pass. Shared backend, adapter and observer source pins are
unchanged. **Unverified here:** escaping exceptions/interrupts, setup/write/cleanup
failures, actual rotation, capture/ingest/doctor execution, Watcher natural lifecycle,
new Reporting scopes and installed combined packaging. No synthetic suite or
fault injection was introduced. No raw retention, historical reingestion,
production registration/selection, activation/restart, publication, commit or push.
An optional process-command inventory was denied by CIM; psutil is not installed.
Neither is an acceptance dependency or a claim of production process inspection.

### Exact preservation and continuation

P4 `before.json` and `before/` preserve exact current bytes of only the four source
files plus 07D/07E/RELEASES. `source-review.json` records old/new SHA-256 and byte
counts, preserved AST boundaries and unchanged producer pins. `source.patch`
SHA-256 is `f97f23fc6669f88f57714393ef9624f40219583e563ff6369464f50b5b172dcd`.
`after.json`, `after-bytes/`, `delivery.patch` and `delivery-manifest.json` record the
complete source/document delivery. Wider immutable evidence is referenced in
`intake.json`, not copied into rollback storage. Rollback must reconcile any
intervening changes rather than blindly replacing shared files.

Next: Reporting receives foreground journaling/request links on TREK-4 through
its issued assignment; Watcher confirms final owned-stream/caller compatibility.
Natural-lifecycle/rollover limits in TREK-3 remain open, and Final Packaging owns
installed correspondence and combined receiving. Producer defects stay with their
owners. Delivery permits authorized consumption; it does not invent receipt,
close assigned follow-ups or authorize activation.

## TREK-3 observer backend integration - 2026-10-06

Watcher implemented the owner-issued [Watcher Integration assignment](task09-deliverables/WATCHER_INTEGRATION.md).
Pipeline's confirmation relayed in the Watcher chat established that the delivered
`observer_log_path` / `configure_runtime_logging` APIs were ready, the backend hash
was unchanged, and no Pipeline edits were underway to the observer or this handoff.
Pipeline confirmed **sole observer stream ownership**: root foreground dispatch
must not install a second handler for `observe-logging`. Pipeline Integration
retains that application-composition obligation. Shared API readiness is separate
from execution verification.

### Delivered behavior and operator effects

Only `src/ck3chronicle/logging_observer.py` and this added handoff section changed.
The observer passes its actual UTC filename timestamp and PID to the shared path
helper and returns the same `watch/log-progress-<timestamp>-<pid>.jsonl` path form.
Its ordinary events now use `configure_runtime_logging(destination=...)`,
`get_logger("logging_observer")`, `event` and `close_runtime_logging`.
The observer closes its handler before the existing heartbeat cleanup, including
when observation raises. No call scope, canonical invocation pair, extra counter,
measurement read, monitoring thread or alternate backend was added.

Existing event names, `schema_version`, states and process payloads remain.
Ordinary JSONL now has the standard formatter's `severity`, `component`,
`process_id` and `thread_name`; its `timestamp_utc` comes from the actual logging
record. JSON spacing/key order and non-ASCII presentation follow the shared
formatter rather than the old compact sorted serializer. Consumers should parse
JSON fields, not compare serialized line formatting.

The explicit destination uses the shared config-free defaults: INFO, 10 MiB,
five backups. Rollover belongs to the backend and uses the existing `.1`–`.5`
suffixes at this invocation's path. It is no longer an unbounded exclusive-create
writer: the standard handler opens in append mode. Actual timestamp/PID filenames
separate observations; this delivery does not rename, migrate or prune old
observation files. Setup failures still propagate; after setup ordinary logging
write/format/rotation and handler cleanup follow the shared best-effort policy.
No exception trace or success outcome is inferred from a missing record.

The replaceable `log-progress-heartbeat-<pid>.json` keeps its original compact
sorted schema, timestamp, actual measurements, atomic replacement and removal.
It is not emitted into ordinary JSONL. `IncrementalTimestampLog`, its byte reads,
timestamp-header accounting, poll timing and lifecycle loop are unchanged.

### Compatibility and unchanged genuine evidence

Source review confirms unchanged Watcher/handler destinations and startup-PID
path, lease-before-Watcher-logging and listener-before-handler-logging ordering.
Request acceptance uses the actual reference; queued polls stay silent; warning,
outcome-unavailable and existing exception/traceback ownership are unchanged.
No edits were made to `watcher.py`, `watcher_processing.py`, `harvester.py`, root
CLI, request handler, shared backend, adapter or checker.
The backend SHA-256 still matches TREK-1:
`d18a6888713d374b0b7266b733d3fd11302372dd8ea94fa06538017a73a1d2b5`.

The [2026-10-05 genuine lifecycle/capture receipt](learner-next-release/PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05)
remains evidence for unchanged behavior only: observed CK3 lifecycle, protected
capture, automatic ingestion, actual facts/playset and startup duplicate outcomes.
It is not fresh verification of this observer, the extended backend inside live
Watcher/handler processes, or final installed composition. Watcher supplies this
bounded compatibility disposition; Pipeline retains shared-owner defects and
records application receipt separately.

### Preservation and continuation

Evidence root: `.codex-tmp/trek3-watcher-20261006/` (ignored).
`before.json` and `before/` preserve and verify exactly the observer and this
handoff's prior bytes, including Pipeline's existing section. They were rechecked
after coordination before edits. `after.json`, `after/`, `source.patch` and
`delivery.patch` identify the exact delivered files; document hashes remain in
the manifest to avoid self-reference. `source-review.json` records AST equality
of the measurement classes/loop, signature, event payload construction, heartbeat
branch/cleanup and returned-path expression, plus the unchanged backend hash.
The required runtime ownership checker and targeted whitespace checks passed.

Rollback requires comparing current bytes and resolving intervening owner edits;
saved copies do not authorize overwriting later work. Prior sections and old
evidence are retained. No synthetic test, injected failure, raw expiry, historical
reingestion, production activation/restart, publication, commit or push occurred.

TREK-3 remains open for Pipeline's actual observer/application receiving and the
execution gaps recorded below. Component defects remain Watcher-owned. Technical
delivery does not imply owner acceptance or production activation.

### Fresh genuine observation and exact remaining gaps

At 10:41:51–10:44:02 UTC (18:41:51–18:44:02 Hong Kong), the saved baseline and
changed observer each made a sequential 64-second bounded attachment to genuine
CK3 PID 58904. Observer PID was 54992. Both used the existing `find_process`,
configured real `error.log` / `game.log`, default two-second polls and 30-second
heartbeats. The existing `stop_requested` callback bounded each observation;
CK3 and live Watcher/handler services were not stopped or restarted. The runner
used ignored `genuine/before` and `genuine/after` runtime destinations and no
second file handler. These are genuine execution checks, not synthetic process
or log fixtures. The runner and full results are `observe_genuine.py` and
`genuine-observation.json` in the evidence root.

Both executions emitted `observer_started`, `game_started` (attachment to the
already-running process), and `observer_stopped`; ordinary payloads matched after
excluding actual timestamps and the newly added standard formatter fields.
Each produced two distinct heartbeat snapshots, atomically replacing the same
PID-specific path; each removed that heartbeat on normal bounded stop. The returned
JSONL path contained its actual filename timestamp and PID and remained readable.
Shared-handler detachment/close restored the initial logger handler set.

Actual measurements, without rounding or inferred events:

| Log | Baseline heartbeat observations | Changed observer heartbeat observations |
|---|---|---|
| `error.log` | 839,564 bytes; 4,069 headers; last `18:36:51`, both snapshots | Identical, both snapshots |
| `game.log` | 477,645 bytes / 2,011 headers, then 477,765 / 2,012; last `18:36:51`, then `18:42:52` | 478,005 bytes / 2,014 headers; last `18:43:15`, both snapshots |

The game's log grew naturally between observations, so whole measurement snapshots
were correctly unequal. Independent regex counting over the corresponding real
log prefixes matched all eight byte/header/last-timestamp observations; each
observer's cumulative `bytes_read` matched its actual observed prefix length.
`measurements-verification.json` records those counts and prefix hashes. Later
prefix reads do not independently prove historical filesystem mtimes. The baseline
JSONL hash remained unchanged after the changed execution.

The changed execution used exactly one `_RuntimeFileHandler`, `_JsonFormatter`,
10,485,760-byte threshold and five backups. All three rows had actual observer PID,
`component=logging_observer`, `severity=INFO` and `thread_name=MainThread`.
No heartbeat was duplicated into JSONL and no canonical lifecycle pair was added.

**Still unverified:** changed-code observation of a natural CK3 start/exit or
replacement, rotation actually crossing its threshold, exceptional cleanup or
write failure, final root CLI composition and installed application receiving.
The game stayed running throughout the bounded observations. Rollover was not
forced by lowering limits or flooding events. The source reviews and old genuine
lifecycle evidence do not close these gaps. Pipeline must preserve sole-stream
dispatch and record receipt against the actual application combination; leave
required natural-lifecycle receiving open pending an appropriate opportunity or
explicit owner disposition. No fabricated exit or outcome is permitted.

## TREK-1 shared backend/API ready for consumers - 2026-10-06

Pipeline implemented the owner-issued [Shared Backend/API assignment](task09-deliverables/SHARED_BACKEND_PIPELINE.md)
under corrected plan B/C and H stage 1. This is implementation readiness for
consumer integration, not proof of Learner execution, component receipt, installed
packaging or activation. TREK-1 remains open for actual receiving dispositions.
The owner confirmed in this assignment chat that no other owner is editing this
handoff and Task 10 has not begun. Task 10 is not a prerequisite: it may later
supply a resolved destination/settings through this interface. Existing component
implementation ownership remains unchanged. The older delivery, test and activation
records below are historical; they do not authorize new synthetic tests or restarts.

### Delivered interface

```python
# ck3chronicle.runtime_logging
CHECKPOINT_INTERVAL_SECONDS = 5.0
def default_logging_settings() -> dict: ...
def logging_settings(): ...
def configure_runtime_logging(*, database=None, runtime_root=None,
                              startup_pid=None, settings=None,
                              destination=None): ...
def close_runtime_logging(handler): ...
def invocation_log_path(log_dir, component, invocation_id) -> Path: ...
def observer_log_path(runtime_root, *, timestamp, pid) -> Path: ...

# ck3chronicle.journal; imports only stdlib and the backend
def get_journal(component: str) -> Journal: ...
class Journal:
    def call(self) -> CallScope: ...
    def checkpoint(self, completed: int | None = None,
                   total: int | None = None) -> None: ...
```

`default_logging_settings()` returns a fresh INFO/10485760-byte/five-backup dict.
Setup selects supplied settings first, config-free defaults for an explicit
destination second, otherwise existing application settings. Validation accepts
the existing five level names and positive integer sizes/counts (not bools),
fills omitted keys with defaults, and copies selected values. Invalid explicit
settings raise `ValueError`; application configuration retains `ConfigurationError`.
The only config import is local to `logging_settings()`. An explicit destination
cannot be combined with any database/runtime-root/startup selector. Directory/file
opening occurs during setup and failures propagate before substantive work.

The return value remains the configured rotating handler. Existing legacy
keyword callers are unchanged. Call setup once in the stream-owning entry point;
the journal never configures output or adds a handler. Existing Watcher/observer
owners must retain their destination instead of adding a foreground handler.
`close_runtime_logging` independently attempts removal and close, suppressing
ordinary failures from either. Existing post-setup event/format/write/rotation
failure handling remains best effort and local to this backend.

`invocation_log_path` returns `<log_dir>/<component>-<invocation_id>.jsonl`;
component and invocation ID are caller-owned filename tokens, not discovered
paths or generated identities. `observer_log_path` returns the existing
`<runtime_root>/watch/log-progress-<timestamp>-<pid>.jsonl` using the supplied
timestamp/PID. Helpers do no I/O or configuration discovery. Legacy Watcher,
startup-PID, database-handler and bootstrap path functions are unchanged.

Use a fresh `with journal.call():` at a selected real call boundary. It emits
`call_started`, then `call_finished` only for a normal return, with monotonic
`elapsed_seconds`. A returned failure value is still a normal return; no success
or commit is inferred. An escaping exception (including `SystemExit(0)`) adds no
call terminal or traceback. The scope restores its enclosing `ContextVar` token
on exit and returns false. There are no call IDs, parent IDs or scope transport.

Both events and checkpoints include `module`, `function` (actual `co_qualname`),
`source_file` (actual filename), `function_line` (definition first line), and
`source_line` (executed hook line). Module identity prefers `__spec__.name`, then
`__name__`; normal-return records reuse entry identity rather than guessing the
return line. The immediate external `with`/checkpoint caller is inspected, without
frame skipping or symbol registries. Temporary frames are deleted in `finally`
before emission; retained identity contains scalars, not code/locals/arguments.
Existing backend invocation/request context continues to merge into events.

Bare checkpoints emit immediately without counts or changes to counted throttling.
Counted hooks accept nonnegative integers excluding bools; total requires completed
and `completed <= total`. Invalid observations are discarded without raising or
clamping. A matching component/function/source scope holds only the last counted
line/emission time. The first observation, a changed hook line, and observations
after five seconds emit. The exact bypass is
`completed is not None and total is not None and completed == total`, including
explicit `(0, 0)` and repeated complete totals. Outside a matching scope, counts
emit without retained throttle state. Helpers identify themselves. Nested calls
restore enclosing state; each fresh call starts fresh. No inferred final flush,
work discovery, count computation, routine bare hooks or component hooks were added.

### Preservation, exact source identity and patch

Evidence root (repository relative):
`.codex-tmp/task09-shared-backend-20261006/`. It is ignored storage.
`before.json` records the exact working bytes of the backend, checker and this
handoff plus prior absence of `journal.py`. Saved copies were hashed against the
source before editing and checked again during evidence generation. `after/`
and `after.json` retain all four delivered files and hashes; `source-after.json`
identifies the three implementation files. No imported dependencies were added
to the rollback set, and no retained release was changed.

| Source | Bytes | SHA-256 |
|---|---:|---|
| `src/ck3chronicle/runtime_logging.py` | 7738 | `d18a6888713d374b0b7266b733d3fd11302372dd8ea94fa06538017a73a1d2b5` |
| `src/ck3chronicle/journal.py` | 4558 | `b48a1fde03f31e7e8d42e91a0f114fc15ed239afecbd265cabbd0412ecc2e8cc` |
| `tools/check_runtime_logging.py` | 3191 | `997fcc95dcaed266bb167db13514aa776266d855214032ab96202a4b5c65d608` |

The byte-preserving unified source patch is
[source.patch](../.codex-tmp/task09-shared-backend-20261006/source.patch), SHA-256
`764f3560e93aecdeec31c6c6a4134b51e427110d971541ee8c1eda6f402ef533`.
It contains only the backend (+50/-13), new adapter (+115), and checker (+18).
[delivery.patch](../.codex-tmp/task09-shared-backend-20261006/delivery.patch)
also includes this handoff section; exact document hash belongs in `after.json`
to avoid a self-referential hash. Rollback must compare current bytes and resolve
intervening owner changes before applying the inverse patch; saved bytes are not
permission to overwrite later work. The broader pre-existing dirty tree is intact.

### Verification and receiving limits

- Required `.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py` passed.
  The checker scans the adapter under the existing ownership rule and now rejects
  adapter imports outside stdlib/the shared backend. It remains a small AST check,
  not a defense against dynamic evasion or retained-payload authentication.
- A fresh repository-Python import loaded both modules from this checkout and
  reported `ck3chronicle.config` absent from `sys.modules`. All three changed
  sources parsed successfully. Exact patch boundaries and whitespace were checked.
- Static AST comparison with saved bytes confirms unchanged `runtime_log_path`,
  `bootstrap_log_path`, `open_bootstrap_log`, formatter, rotating-handler subclass,
  logger/event helpers, scoped context and Watcher severity adapter. Source review
  covered lazy settings selection, setup propagation, best-effort removal/close,
  frame cleanup, nested context restoration, count validation and suppression.
- Existing real callers inspected: `watcher.EventJournal.__enter__/__exit__` and
  `pipeline.database_handler.serve` retain their original setup/cleanup keywords.
  The observer's existing filename construction matches the new helper. A read-only
  query using current application configuration returned INFO/10485760/five and
  the existing runtime Watcher path plus handler/bootstrap paths for
  `ck3chronicle-schema3-20261005T112504Z.sqlite3`; no handler was started or configured.
  This is current settings/path evidence and static compatibility, not fresh
  changed-code Watcher/handler execution. See `review.json` for the review record.
- No synthetic API harness, recursion/timing scenario, injected failure, event
  flooding or broad historical suite was created or executed. Dynamic bare/count
  throttling, nested/exception cleanup, rotation and error cases remain explicitly
  unverified. No overhead or retained execution claim is made. These limits do not
  block shared interface readiness under the issued assignment.

Learner receives the config-free retained import/payload interface and performs
genuine consumer integration under its own issued assignment, retaining the exact
two shared source files. That later work supplies authentication/import and real
consumer evidence; it is not a prerequisite to this implementation readiness.
Watcher still owes its compatibility disposition; Pipeline records the static
and current-configuration compatibility evidence above and retains actual shared
backend receiving defects. Record actual dispositions on TREK-1 without inventing
receipt, closing the producer early, or making all of Learner Integration a
prerequisite. No candidate generation, production activation/restart, publication,
commit or push was performed.

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
