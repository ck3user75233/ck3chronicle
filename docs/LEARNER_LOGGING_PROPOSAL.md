# Lightweight learner operational logging

**Superseded 2026-10-03.** The owner's
[Canonical Logging System v1](CANONICAL_LOGGING_SYSTEM_V1.md) uses actual code
symbols and source-position checkpoints, not the phase/progress model below.
Use [Task 09A](TASK09A_PROMPT.md) for planning. Historical ownership/isolation
findings may inform inspection; this proposal is no longer an implementation brief.

2026-10-03. Proposal for owner review; logging implementation is not part of this
write-up. This review inspected current checkout source. It does not establish
the cause or current state of any running learner process.

## Recommendation

Reuse the existing runtime JSONL logger, retain its code inside new immutable
learner releases, and add a small learner progress helper. Record operation and
phase boundaries immediately, with actual completed-work counters at most once
every ten seconds during loops. Use one rotating log per invocation.

This provides the last reached phase and evidence of advancing work without a
monitoring service, background thread, heartbeat file, database, or new dependency.
It does not detect deadlocks or guarantee an event every ten seconds while a
single call is blocked or doing expensive work.

## What exists today

| Component | Observed implementation | Applicable reuse |
| --- | --- | --- |
| Shared logger | [runtime_logging.py](../src/ck3chronicle/runtime_logging.py): standard-library logging, rotating UTF-8 JSONL, context fields, UTC timestamps, severity, component, PID, thread, and exception traceback. Defaults are INFO, 10 MiB, five backups. | Reuse the owner and its event conventions. |
| Watcher | [EventJournal](../src/ck3chronicle/watcher.py) configures that logger and emits lifecycle events. Heartbeats separately replace `watcher-heartbeat.json`; they are not appended to the event log. | Reuse entry-point configuration and lifecycle events. The watcher's heartbeat/lease machinery is unnecessary for a foreground learner operation. |
| Handler and ingestion | [database_handler.py](../src/ck3chronicle/pipeline/database_handler.py) supplies request context and start/completion/failure events. [ingestion.py](../src/ck3chronicle/pipeline/ingestion.py) records real wait transitions and monotonic elapsed times. | Use an invocation ID, phase context, and monotonic durations. No logging queue is needed. |
| Learner | [artifacts.py](../tools/template_learning/artifacts.py) prints after finishing a source family; [clustering.py](../tools/template_learning/clustering.py) prints every 100 region-group comparisons. [learn_error_templates.py](../tools/template_learning/learn_error_templates.py) prints its final JSON summary. | These are console messages, not a configured operational journal. Their spacing follows completed work, not elapsed time. |
| Execution receipt | [learner_loader.py](../tools/template_learning/learner_loader.py) writes the requested receipt in `finally` around operation execution. Earlier bootstrap failures and abrupt termination can bypass it. | Keep the receipt as execution provenance. It cannot serve as live progress. |

`records.collect_records` has no progress events around parsing inputs. Source
learning includes refinement/consolidation steps without durable phase events.
The [v46 delivery](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md) now batches identical
template groups and reports console progress; its cumulative re-inference loop
has been removed. Instrument the current stage and its `choose_medoid` and
`derive_pattern` calls without changing that algorithm. Logging gaps do not
establish the cause of an earlier delay.

## Smallest shared implementation

Keep [runtime_logging.py](../src/ck3chronicle/runtime_logging.py) the sole source
owner of handlers, formatting, rotation, and log-path conventions. Do not create
another learner JSON formatter or handler.

There is one necessary integration change: its top-level application-config
import is incompatible with frozen learner isolation. Move that import into the
configuration-reading function. Allow an explicit destination and explicit
settings, using defaults owned by this same module, without loading application
configuration. Preserve existing watcher/handler calls, destinations, and startup
error behavior.

During learner release creation, copy the exact shared-owner source bytes into a
private retained module, for example `template_learning/_runtime_logging.py`.
Include those bytes in the executable manifest and learner implementation
identity, and update closure/reference verification accordingly. This is a
generated release payload, not a second editable source implementation.

The frozen worker imports only this authenticated module. Keep the existing ban
on ambient `ck3chronicle` imports and checkout fallbacks. No import allowlist
relaxation, generic plugin mechanism, or new shared package is needed. Older
releases remain immutable and continue using their own launchers without new
logging arguments. Reject an explicit unsupported `--log-dir` clearly.

Add one small learner-owned adapter, tentatively `learner_logging.py`, for phase
context and throttled progress. It delegates emission to the retained logger;
it does not configure handlers itself. Prefer explicit existing phase boundaries
and loop counters to decorators on every function.

## Invocation and event contract

Add one optional launcher argument, `--log-dir`. For new releases, default it to
`<receipt-parent>/learner-logs` when `--receipt` is provided, otherwise
`<working-directory>/.ck3chronicle/wip/learner-logs`. Resolve the destination once
and pass it explicitly to the authenticated worker. The central logger owns the
filename convention: `learner-<invocation-id>.jsonl`, with the existing rotation
defaults. Separate invocation IDs prevent concurrent learners sharing a file.
The fallback is ignored in this checkout; external callers should select an
appropriate explicit directory. Do not add application configuration options.

Configure logging inside the authenticated worker, before executing the selected
operation. Print the absolute log path once to stderr. Preserve existing stdout
results and receipt behavior. Authentication/bootstrap failures before logger
initialization continue to use existing stderr diagnostics; do not load
unauthenticated logging code to cover that gap.

Every event carries `invocation_id`, `operation`, and `release_id`; normal common
fields come from the shared formatter. Record the manifest pin and parser identity
once in `learner_operation_started`. The ID describes an invocation, not a CK3
Run ID. Phase events add a phase name, relevant source family/input hash when
already available, and monotonic `elapsed_seconds`.

| Event | Meaning |
| --- | --- |
| `learner_operation_started` | Authenticated operation is about to execute. |
| `learner_phase_started` | Entered the named work stage, before its expensive call. |
| `learner_progress` | At an existing work boundary: `completed`, `unit`, and `total` only when already known. Optional current item identifies work about to be attempted. |
| `learner_phase_completed` | The stage returned successfully, with its final actual counts and duration. |
| `learner_operation_completed` | Existing operation success path completed; include output references already available. |
| `learner_operation_failed` | Existing error path, ERROR with traceback for an exception; preserve exception and exit status. |
| `learner_operation_interrupted` | A caught `KeyboardInterrupt`, WARNING; preserve interruption behavior. |

Use the existing success convention for `SystemExit(0)`; a nonzero exit must not
be reported as completion. Emit one operation terminal event, not repeated failure
events at every nested stage. Preserve the last active phase for failure context.
Do not claim that the execution receipt was saved unless its write succeeded.

Logging remains best effort after successful configuration, as it is for runtime
components. A log-file setup error should surface clearly before learning starts,
following the current shared logger's startup semantics. Do not silently announce
a persistent log that could not be opened. Closing/logging errors must not replace
the learner's original exception. Abrupt termination can leave no terminal event;
absence of completion means the outcome is unavailable, not a reconstructed failure.

## Instrumentation scope and cost

Instrument the shared paths used by both fresh `learn` and registry `sync`/`build`:

1. Inventory and input parsing: phase boundaries, each input's start/end, and
   completed-input counts. Use existing hashes; do not read or hash inputs again
   for logging. One parser call may remain silent until it returns.
2. Registry feature loading/combination: stage boundaries and existing entry
   counters, including cache reuse counts where already tracked.
3. Source learning: source start/end and the existing initial-grouping,
   literal/support refinement, same-wording consolidation, region regrouping, and
   duplicate-ID consolidation stages. Scope context so recursive/context learning
   cannot overwrite its caller's progress state.
4. Long loops: check elapsed time at existing boundaries; emit no more than one
   INFO progress event per ten seconds per active phase. Check before expensive
   work as well as after it where practical. For duplicate consolidation include
   current candidate ID and group size when available, using existing values.
5. Evaluation and artifact writing: stage start/end and already available counts
   or output paths. Record final phase counts even if no timed event was due.

Do not emit an INFO event per record, comparison, or merge. Do not evaluate lazy
IDs/patterns, traverse groups, serialize diagnostic bodies, or repeat inference
just to populate an event. Totals may be omitted. Counters describe completed
units in that specific phase, never a guessed global percentage or ETA.

A clock check and a few scalar counters should be the ordinary loop overhead;
JSON serialization and file writes happen only when an event is due. Keep current
console output for compatibility initially. The JSONL journal becomes the durable
operational reference.

## Verification and delivery

Use genuine protected CK3 evidence in a fresh candidate workspace, including an
input/source family that exercises consolidation. First verify a bounded corpus;
an all-logs rebuild is not a logging acceptance requirement. Exercise fresh
learning and registry sync/build through the selected retained launcher. Inspect
real JSONL for startup, phase ordering, advancing counts, durations, final output,
and isolation between invocation files. Record corpus scope and observed timing.
Do not manufacture a stalled process to claim hang detection.

Run `tools/check_runtime_logging.py` with the repository venv. Verify release
hashes and receipts include the retained logging module, and execution does not
import mutable application code. Check unchanged watcher/handler APIs and paths
without restarting services. Do not resurrect removed synthetic/fault-injection
logging tests; unobserved rotation or failure scenarios remain explicitly unverified.

Compare learned contracts and assignment outcomes against the same learner
implementation before logging changes, on the same genuine evidence. Preserve
the approved v46 changes; production v45 is not an equivalent baseline. The new executable closure legitimately changes
release identity and may affect provenance-bearing model hashes. Logging fields
must never enter inference inputs or semantic model content. Report actual
timings rather than inventing a performance threshold.

Deliver a new immutable candidate learner release under ignored research output,
its manifest pin, execution receipts and logs. Write
`docs/LEARNER_LOGGING_IMPLEMENTATION_HANDOFF.md` with usage, verification and
limitations, and update current status/handoff. Do not
edit existing distributions, reuse another release's registry state, register a
production release, pin a model, rebuild the full corpus by default, or restart
runtime processes. Follow [RELEASES.md](RELEASES.md) for subsequent owner-directed
delivery. Implementation instructions are in the
[agent prompt](LEARNER_LOGGING_IMPLEMENTATION_PROMPT.md).
