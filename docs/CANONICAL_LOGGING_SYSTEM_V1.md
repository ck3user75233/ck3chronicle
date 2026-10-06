# Canonical Logging System v1

2026-10-03. Owner-supplied architectural direction, recorded for implementation
planning. This reference does not authorize implementation or production activation.
[Task 09A](TASK09A_PROMPT.md) commissions the plan; final implementation assignment
and sequencing remain with the owner and incoming advisor.

Owner clarification, 2026-10-05: Learner leads planning for implementation
throughout CK3Chronicle, with component implementation and receiving ownership
preserved. A learner-first slice does not limit the overall scope.

The examples below are individually labelled **illustrative**. Existing function
names and call signatures were checked against the checkout on 2026-10-03.
`journal` and its methods describe a proposed API, not existing CK3Chronicle code.
Final implementation uses the actual owning modules, symbols, parameter/token
definitions and return contracts, with any new journal API explicitly defined.

## Purpose and governing principle

Provide lightweight operational visibility into long-running CK3Chronicle work:
which invocation is running, what actual code is executing or most recently
completed, where execution last reached, any caller-reported completed work,
and how the invocation terminated if that outcome was observed.

This is an **execution journal, not an application workflow model**. Identify
actual functions such as `choose_medoid` and `collect_records`. Do not translate
them into `medoid_selection`, `parsing_phase`, `matching_stage` or another logging
taxonomy. The executable implementation is the authority.

Derive module, qualified function, source file and appropriate source line from
the actual function/frame where practical. Do not maintain a parallel mapping
between code and semantic logging names. An imported alias does not change the
function's defining source.

## One logging owner

[`src/ck3chronicle/runtime_logging.py`](../src/ck3chronicle/runtime_logging.py)
remains the sole editable source owner for JSONL formatting, handlers, rotation,
encoding, severity, timestamps, common context, defaults, path conventions and
logging failure behavior.

Small component adapters may expose journal calls through that owner. They must
not introduce their own formatter, handler, backend, file management or logging
framework. An immutable release may retain the exact shared-owner bytes as
authenticated distribution payload; that is not a second editable implementation.

## Journal events

| Event | Meaning |
|---|---|
| `invocation_started` | An authenticated/configured invocation is beginning. Record invocation ID, operation and already-known executable/release provenance. |
| `call_started` | A selected significant actual function was entered. |
| `checkpoint` | Execution reached this actual source location, optionally with caller-owned counts. |
| `call_finished` | A selected call completed, with monotonic elapsed time where useful. Do not imply successful return from a call that raised. |
| `invocation_finished` | An observed terminal outcome, such as success, failed, interrupted or nonzero exit. |

Component prefixes are permissible without changing these meanings. No phase,
stage, pipeline-step or workflow-state event family is needed. Select useful
call boundaries; do not instrument every function or build function-level tracing.

Record stable release/manifest/parser/matcher provenance once at invocation start
when already available. An independent invocation ID and its journal identify
subsequent events without repeating all provenance at every checkpoint. The
implementation plan must keep that association understandable across rotation.

An absent terminal event means **no terminal outcome was observed**. It does not
establish failure, success, a hang, or the process's current state. Silence after
a checkpoint establishes only the last recorded observation.

## Checkpoints and caller-owned counts

**Illustrative proposed API — three alternative calls, not a sequence to emit
three times at one work boundary.** `completed` and `total` stand for scalar
values available in the instrumented function.

```python
journal.checkpoint()                  # Position only.
journal.checkpoint(completed)         # Position and caller-owned completed count.
journal.checkpoint(completed, total)  # Position and caller-owned completed/total.
```

These mean, respectively:

- Execution reached this location.
- Execution reached this location; the application reports this completed count.
- Execution reached this location; the application reports this completed count
  and this locally known total.

The journal derives the enclosing function and exact checkpoint source location.
It does not require a checkpoint name, registry, unit taxonomy, configuration
file, or manually maintained mapping. It never examines the next statement, AST
or bytecode to predict what will execute next.

The code that performs work owns its counts. Pass only scalar values already
available at the observation boundary. Constant-time use of an already-sized
collection and a natural loop counter is appropriate; do not materialize a
generator, traverse collections, rescan inputs or restructure algorithms to
manufacture progress. A count recorded before work starts is not completed work.
Use compatible local units for completed/total; unrelated collection lengths do
not become a meaningful pair merely because both are available.

The journal does not discover work, count batches/records, calculate totals,
percentages, global progress or ETA, or infer what the unit represents. Counts
are optional; a unit label is not required.

## Throttling and overhead

Counted checkpoints support lightweight time-based suppression within the
adapter, with a simple centrally owned default interval. Application loops need
not contain logging-only modulo conditions. Define the first counted emission,
periodic emissions and final emission in the implementation plan. A supplied
completed total (`completed == total`, with both values present) is not suppressed.

A bare `checkpoint()` is a deliberately inserted position observation and
normally emits immediately, regardless of counted-checkpoint throttling. No
count must be inferred when only one or neither value is supplied.

Use a monotonic clock and the smallest scalar state the actual instrumented calls
require. Keep nested calls, recursion and separate invocations from misleading
each other. No general phase/task state machine is warranted. Avoid retaining
Python frames or their application locals after extracting the necessary identity.

Permitted work is approximately: inspect the caller frame/code object, read the
clock, compare a timestamp, retain tiny throttling state, accept supplied scalar
values, serialize a small event and emit through the existing logger. Serialization
and file writes occur only when an event is emitted.

Logging must not hash inputs, invoke inference/parser/matcher/classifier work,
inspect models, evaluate lazy IDs/properties/patterns, serialize diagnostic bodies
or large structures, or repeat application computations for visibility.

## Minimal API and progressive diagnosis

**Illustrative proposed call-boundary API — normal-return path only.**
`call_token` is the proposed return value of `call_started()`, supplied back to
`call_finished()`; it is not an existing parser token or an application data type.

```python
call_token = journal.call_started()
# Existing work executes here; its body is omitted from this API illustration.
journal.call_finished(call_token)
```

A small context-manager/helper equivalent is acceptable. Select signatures after
inspecting actual return/exception patterns; avoid generalized instrumentation
decorators across the codebase. Identify the work's function, not the helper's
frame. Entry/finish correlation must remain clear for nested/repeated calls
without becoming a distributed tracing system.

For a suspected slow call, add local bare checkpoints to the owning function,
create a new immutable candidate and inspect which locations were recorded.
Instrument deeper only where genuine operational evidence warrants it.

**Illustrative insertion inside `template_learning.records.collect_records`.**
The middle line is its existing call to `read_evidence`; `evidence` and `parser`
are existing locals/parameters. Only the surrounding proposed journal calls are
new. They locate observations in `records.collect_records`, not inside the callee.

```python
journal.checkpoint()
raw = read_evidence(evidence.path, parser=parser)
journal.checkpoint()
```

The retained source shows the region between observations. No tracing configuration,
source lookahead, profiler integration or automatic hang diagnosis is needed.
Do not edit an already-retained release to add checkpoints.

## Invocation files, outcomes and receipts

Prefer one rotating JSONL journal per foreground invocation, for example
`learner-<invocation-id>.jsonl`. Separate invocations must not share a writable
narrative. Resolve destination/identity explicitly and pass them into the
authenticated worker; never forward launcher logging flags as operation arguments.

Log-file setup failures surface before substantive work. After successful setup,
logging remains best effort and cannot replace the application's real outcome.
Preserve success, nonzero `SystemExit`, `KeyboardInterrupt`, exception, subprocess
exit and receipt semantics. Record an exception once at the invocation boundary,
with useful traceback/code context; do not log it again at every nested call.
Cleanup must not mask the original exception or claim an unwritten receipt.

An execution receipt records provenance and observed final execution information.
A journal records observations during execution. Neither replaces the other;
do not merge them into a status/provenance database. Abrupt termination may leave
neither a receipt nor a terminal journal event.

The learner's existing `run` surface may gain `--log-dir` for logging-capable
releases. The exact default, resolution/transport seam and support detection belong
in the plan. Older immutable releases keep their own execution; explicit unsupported
logging requests must fail clearly rather than be silently ignored or forwarded.

## Immutable execution

The worker imports only authenticated retained logging/instrumentation bytes.
Use one authoritative source-to-payload mapping so the shared owner can become,
for example, `template_learning/_runtime_logging.py` in a release. Include the
adapter and shared-owner bytes in manifest authentication, executable closure/
reference checks, implementation identity and release identity as appropriate.

Preserve isolated Python execution, retained imports, parser pinning, executable
auditing, ambient-import restrictions and receipts. Release identity plus actual
source location identifies the observed immutable code. Source edits do not change
already-created releases or code already loaded in running processes.

## Non-goals and acceptance

No OpenTelemetry, metrics subsystem, dashboard, task/status database, workflow
orchestration, monitoring/heartbeat threads, watchdog, deadlock detection,
automatic restart/timeout, generalized tracing or automatic profiler integration.
Existing watcher lifecycle/heartbeat responsibilities are not deleted by this
prohibition on adding journal machinery.

Success means a reader can identify the actual code entered/completed, the last
recorded source location, and any counts reported by that code, without translating
a separate operational ontology. Verify on bounded genuine execution, authentic
release bytes and unchanged learner outcomes. Missing genuine cases stay unverified.

## Adoption scope and sequencing

The owner's 2026-10-05 direction requires project-wide implementation planning
led by Learner. Cover Learner, Pipeline, Watcher, Data Intelligence/Reporting and
application entry points. Plan small deliveries through their existing owners,
with Pipeline receiving application packaging and integrated runtime effects.
Useful current logging, request correlation, operator commands and destinations
must be preserved or deliberately converted, not lost as collateral cleanup.

The planner must identify required changes and already-sufficient coverage across
those consumers, which events change, and how operators receive the result. A
learner-first delivery remains a sequencing option; other required component work
stays explicit. This planning direction does not execute the implementation or
authorize activation. No permanent compatibility shims, duplicate backends or
indiscriminate function tracing are commissioned. Canonical journals retain v1.

This direction supersedes the phase-based design in
[the earlier learner proposal](LEARNER_LOGGING_PROPOSAL.md) and
[implementation prompt](LEARNER_LOGGING_IMPLEMENTATION_PROMPT.md). Their release
isolation and operational evidence may remain useful, but they are not active
implementation assignments for this design.
