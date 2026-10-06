# Canonical Logging v1 implementation plan — Task 09A

Revised 2026-10-06 under the owner's targeted 09A corrective. Learner-led planning only. This document proposes implementation and
verification; neither has been performed for canonical logging. The work for 09A
was read-only source/document inspection, local identity comparison, and writing
this file. No candidate, training campaign, publication, service action, production
change, tracker enrollment, commit or push is authorized by this plan.

Authority: [Canonical Logging System v1](CANONICAL_LOGGING_SYSTEM_V1.md), the
owner's [09A assignment](TASK09A_PROMPT.md), and
[team governance](team-governance/README.md). Component delivery, integrated
receiving, and owner-authorized activation remain separate. Subsequent owner
scope decisions govern any 09B implementation assignment. This complete corrected
revision supersedes the earlier plan; no implementation is claimed.

## A. Current-state findings

### Actual baseline and responsibilities

The checkout is `C:/Users/nateb/Documents/ck3chronicle`. It contains substantial
tracked modifications and untracked source/resources. HEAD is not its executable
baseline. Root and learner AGENTS, development guidance, opening plan/status/handoff,
current release and experiment guidance, 07C, 07E and the proposed Task 10 were read.
Rejected database-handler designs were not used. Historical test/build recipes do
not supersede current instructions.

The current [receiving receipt](learner-next-release/PIPELINE_RECEIVING.md), especially
“R3 packaging closed,” “Production activated,” and “Database replacement complete,”
supersedes older pending statements, including those in the learner tool README.
The original 2026-10-05 read-only comparison found that the two catalog pins equal
the actual manifest-file hashes. This is an identity observation, not a new execution or
complete installed-artifact authentication claim.

| Item | Current recorded identity |
|---|---|
| Learner/version | `0dc8130a0740d2209e1da8e2cc7241d7d735df2c0252342075b7624bfad0e3de` / `outer-diagnostic-consensus-v61` |
| Learner manifest | `d5dffa6f9202bf6d386f27a2738ca8d0274b42971272bc8cd2550cddbbe42041` |
| Learner implementation | `77a3935070c561c2de830f6577f31c189991dd93d0bce7bf0106c626a083ced7` |
| Parser | `ck3-lossless-v1.8`, `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Package/model | `4ac4e8ee92346e6d14eacfbf` / `789219fdbd81c8dab950bc93` |
| Package manifest | `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f` |
| Final R3 wheel | `.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl` |
| Wheel SHA-256 | `7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959` |
| Ingestion application lineage in current receipt | `application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d` |

The receipt records completed production activation, 31 new-model Runs, and the
natural lifecycle producing active Run `20261005-UYSOEO`. The current store is
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`. Do not
repeat the completed 73-log build, 30-capture rebuild, cutover or historical
ingestion to establish logging. R4 syntax remains Reporting-owned work outside
this plan. Process IDs and operational observations in that receipt are dated
evidence, not a fresh process-status assertion here.

The owner clarified during 09A: **the current production code being used is the
baseline; develop the logging plan against it.** Use the current checkout's actual
application and learner source, including current decoder code. The decoder has
no independent pin; changing it does not invalidate existing releases or selections.
An older retained decoder copy is not the baseline for this work and creates no
compatibility gate or prerequisite. Later logging verification compares this
baseline with the same code plus logging changes. Preserve concurrent work and
record the exact working bytes before implementation as specified in H.

Pipeline owns application composition, packaging and integrated receiving; Learner
owns retained learner/parser/matcher delivery. Watcher owns lifecycle/capture and
API triggers. Reporting owns query, source search and export behaviour. The existing
sole backend source remains `src/ck3chronicle/runtime_logging.py`; propose Pipeline
as implementer/receiver of that shared application module, with Learner receiving
its retained distribution interface. This assigns no component algorithm to another
team and does not create an Advisory approval gate.

### Source findings and gaps

Source links name actual files; symbols below are the primary anchors because
line numbers will move during concurrent work.

| Source / actual path | Finding and consequence |
|---|---|
| [runtime_logging.py](../src/ck3chronicle/runtime_logging.py), `logging_settings`, `configure_runtime_logging`, `event`, `watcher_event` | Sole formatter/rotation owner; INFO, 10 MiB, five backups; best effort after configuration. Eager `.config` import currently makes even explicit-settings import depend on mutable application configuration. No explicit file destination or canonical call/checkpoint API exists. |
| [learner_loader.py](../tools/template_learning/learner_loader.py), `main → launch → execute` | Outer `run` uses `argparse.REMAINDER`; worker runs `-I -S -B`, reauthenticates, installs `RetainedImports` and executable audit, then `runpy.run_module(..., run_name='__main__')`. Context `_ck3_learner_execution` already supplies manifest, pin and folder. There is no `--log-dir`. |
| Same file, `FILES`, `implementation_identity`, `create_release`, `authenticate` | 44 learner-local files are hashed/copied using `source/name` and authenticated under `template_learning/name`. The decoder is separately retained under `ck3chronicle/decoder.py` using explicit `application_source`; it affects release identity but is currently outside the learner implementation fingerprint. Shared logging cannot simply be appended as a nonexistent learner-local file. |
| Same file, `execute` finally block | Receipt writes happen after dispatch, even when dispatch raises; status currently only `failed/completed`. A receipt-write failure can mask the original exception. This is a necessary bounded terminal-handling repair, not permission to rewrite execution. |
| [records.py](../tools/template_learning/records.py), `collect_records(logs: Sequence[ProtectedLog], *, parser)` | Owns input processing. `evidence_stats[evidence.sha256] = stats` is after recovery processing. Add a local `enumerate(logs, 1)` index and emit it only after that input is completely processed, against `len(logs)`. This measures completed inputs, including repeated hashes; evidence-map cardinality measures something different. No extra traversal is needed. |
| [incremental_template_registry.py](../tools/template_learning/incremental_template_registry.py), `sync_registry` | `candidate_paths` returns a list. `summary['paths_seen']` increments before stat/hash/cache work. Reuse the single returned list for a total; emit after the path's cache validation/write and registry-entry update. Registry persistence occurs later; normal call return already observes its completion, so no routine bare checkpoint is needed. |
| Same file, `combine_training_records`, `build_revision` | Existing sequence is load features → merge records, then `artifacts.build_model` → `artifacts.write_bundle` → update registry. These real functions suffice; no invented stage vocabulary. `entries` is typed Iterable but the function already sorts it into a list. |
| [clustering.py](../tools/template_learning/clustering.py), `choose_medoid`, `refine_region_groups` | Medoid uses expensive `max(... sum(... generator ...))`; preserve it. `seen.add(key)` precedes remaining pair checks. `len(seen)` and `len(ordered)` have different meanings; neither supports the suggested completed/total pair. Preserve existing modulo-100 console output. |
| [patterns.py](../tools/template_learning/patterns.py), `derive_pattern(records, reference, *, hypotheses=None)` | Defined here, imported by clustering. `units` and outer mapping loop are materialized. Frequent calls from refinement would flood entry/return logs; no initial inner instrumentation is justified. |
| [artifacts.py](../tools/template_learning/artifacts.py), `build_model`, `write_bundle`, `learner_identity` | Source-family loop has a real completed boundary after `source_summary[source]` and existing `Learned ...` output. Identity currently calls `implementation_identity(Path(__file__).parent)`. Model work includes lazy/computed identities and inference: do not evaluate them for logging. |
| [publish_native_model.py](../tools/template_learning/publish_native_model.py), `verify_reference_implementation`, `publish_package` | Reference verification assumes every implementation hash is relative to the learner directory. Runtime copying uses `matcher_loader.RUNTIME_FILES`; journal imports must not leak into that matcher closure. Publication audit permits generated executable bytes only when identical to authenticated retained code. |
| [database_handler.py](../src/ck3chronicle/pipeline/database_handler.py), `_Handler`; [request_handler.py](../src/ck3chronicle/pipeline/request_handler.py), `HandlerClient` | Rich accepted/terminal/request/queue/wait/uncertain-write evidence already exists. `_prepare` copies context into the database queue. `_database_worker` currently uses explicit fields rather than installing that copied context around component calls. Status polls are intentionally silent. |
| [ingestion.py](../src/ck3chronicle/pipeline/ingestion.py), `_ingest` | Preparation timings bracket parsing/classification but do not identify progress within it. `classifier.classify_raw(raw)` is an iterator; `len(raw.emissions)` is not a total of classification units. Normal per-result completion follows `writer.observe` and any `accumulator.add`. |
| [repository.py](../src/ck3chronicle/pipeline/repository.py), `Database.write_run`; [retention.py](../src/ck3chronicle/pipeline/retention.py), `retain_raw_logs` | Database operations already have timings and terminal outcomes. Write validation/review staging precede transaction/commit; no journal event may imply commit early. Retention returns explicit eligible/removed/skipped/failure data consumed by Watcher; no need to log each deletion. |
| [watcher.py](../src/ck3chronicle/watcher.py), `EventJournal`, `watch_sessions`; [watcher_processing.py](../src/ck3chronicle/watcher_processing.py) | Shared backend already owns ordinary events. Heartbeat replaces JSON separately. Lease/startup paths, capture facts, submit/accepted/request-result correlation, warning severity, retention outcomes and unavailable-outcome handling must survive. |
| [harvester.py](../src/ck3chronicle/harvester.py), `spool_logs` | Protected-copy and publication owner; no logger of its own. Existing callback/Watcher events expose capture entry, completion and failure. Internal checkpoints remain available for targeted diagnosis; ordinary capture does not need duplicate hooks. |
| [analysis.py](../src/ck3chronicle/reporting/analysis.py), `DiagnosticAnalysis`; [source_search.py](../src/ck3chronicle/reporting/source_search.py), `SourceSearch`; [reporting/cli.py](../src/ck3chronicle/reporting/cli.py) | Existing investigation/source-completion/export/error events use shared loggers, but foreground CLI never configures a file. Handler logs do not observe client-side filtering, source search, rendering or output. `_content` already materializes ripgrep batches and records actual subprocess return codes. |
| [cli.py](../src/ck3chronicle/cli.py), `main`; [pipeline/catalog.py](../src/ck3chronicle/pipeline/catalog.py), `main` | Root CLI dispatches `args.func` and exits with its result. Three installed console entry points exist in `pyproject.toml`. Help must remain configuration-independent. Learner outer administration and model catalog operations also need a deliberate foreground disposition. |
| [logging_observer.py](../src/ck3chronicle/logging_observer.py), `observe_logging_progress` | Additional direct JSONL writer: `log-progress-<timestamp>-<pid>.jsonl`, plus a replaceable heartbeat. Its measurement is actual product behaviour; move ordinary JSONL emission to the shared owner without removing measurement or inventing another monitoring thread. |

## B. Minimal architecture

Use one editable backend and one small reusable adapter:

```text
runtime_logging.py (settings, paths, formatting, handlers, rotation, failure policy)
  → journal.py (new: actual call scopes, identity extraction, checkpoint throttling)
    → selected existing component functions

learner_loader authoritative source/payload map
  → immutable ck3chronicle/runtime_logging.py + ck3chronicle/journal.py
  → existing authenticated RetainedImports, alongside retained decoder
```

Both application and learner hooks import `ck3chronicle.journal`. Retaining the
same package paths avoids an import shim, editable learner copy, fallback import,
or special relocated relative import. Existing `RetainedImports` already owns
the `ck3chronicle` namespace and refuses missing modules. The adapter imports only
stdlib and `.runtime_logging`, never configuration, parser, model or learner code.

### Exact proposed edit set

Paths are relative to the checkout. No source file is edited by 09A. Preserve only
the files actually being changed in each delivery's rollback set (H).

| Delivery | Files and minimum edit |
|---|---|
| Shared owner/API — Pipeline, Learner receives retained seam | `src/ck3chronicle/runtime_logging.py`: lazy config import, validated config-free defaults, explicit destination, shared path helpers and central five-second interval. Preserve existing backend behaviour; ensure new setup/close use cannot mask substantive failure. New `src/ck3chronicle/journal.py`: local call timing, source identity and scalar checkpoint throttling. |
| Retained execution — Learner | `tools/template_learning/learner_loader.py`: payload mapping, shared implementation hashes, capability authentication, `run --log-dir`, transport, worker outcomes and bounded receipt repair. `artifacts.py`: authenticated identity lookup and selected hooks. `publish_native_model.py`: mapped reference verification without changing matching/export algorithms. |
| Initial learner hooks — Learner | `tools/template_learning/records.py`: `collect_records` scope and completed-input index / total inputs. `incremental_template_registry.py`: `sync_registry` scope and existing completed-path count. `artifacts.py`: `build_model` scope/existing source-summary count and `write_bundle` scope only. These are the four selected call scopes; no routine bare hooks. |
| Direct mapping consumers — Learner | `tools/template_learning/recover_large_candidate_export.py`: replace local-only byte assertion with mapping helper. `tools/template_learning/review_short_thresholds.py`: pass explicit application source when fingerprinting mutable source. Interface repairs only; do not run either experiment/recovery operation. |
| Pipeline — Pipeline | `src/ck3chronicle/pipeline/request_handler.py`: one accepted-request observation in the foreground client using the returned `RequestRef` and existing invocation context; no wire/poll change. `pipeline/catalog.py`: foreground invocation around command dispatch; no extra evaluator scope. Existing handler/preparation/storage events otherwise suffice. |
| Watcher — Watcher | `src/ck3chronicle/logging_observer.py`: delegate ordinary JSONL to shared backend/path helper, preserving measurements and heartbeat. No initial edits to `watcher.py`, `watcher_processing.py` or `harvester.py`; existing lifecycle/capture/triggers are covered. |
| Reporting — Data Intelligence / Reporting | `src/ck3chronicle/reporting/analysis.py`: `search_runs` call scope only. `reporting/source_search.py`: `_content` scope only. `reporting/cli.py`: `_emit` scope only. Existing events, counts, error ownership and console/export behaviour remain. |
| Application composition/enforcement — Pipeline, affected owners receive | `src/ck3chronicle/cli.py`: foreground setup/cleanup/outcomes around dispatch, leaving watch/observer destination ownership intact. `tools/check_runtime_logging.py`: cover adapter and declared learner-hook sources; authenticate retained copies separately. `learner_loader.py` also supplies administrative foreground setup in A. `pyproject.toml`: later authorized new distribution resource entries only. |
| Delivery documentation — respective owners | Update `docs/RELEASES.md`, `docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md`, `tools/template_learning/README.md` and affected component handoffs when implemented/received. This does not authorize 09A edits to them. |

Compared with the earlier first slice, `clustering.py` is removed from the edit set.
`refine_region_groups`, `combine_training_records` and `build_revision` lose their
proposed call scopes. `choose_medoid` and `derive_pattern` remain diagnosis-only
possibilities, not scheduled initial instrumentation. Remove routine end-of-write
and end-of-function checkpoints throughout. `learn_error_templates.py`, parser,
matcher, rules and decoder need no logging edits.

Later deliveries also remove the proposed edits to `ingestion.py`,
`database_handler.py`, `watcher.py` and `harvester.py`. A trivial local loop index
is allowed for useful completed-work progress; it does not justify additional
hooks solely to fill a coverage matrix. P/W/R/A remain explicit receiving
deliveries with the smaller required edits above; no-change coverage is explained
in E. No catalog/selection change belongs to this source edit set. Packaging later
adds only newly authorized immutable resources and pins.

### Task 10 logging/configuration interface only

Application configuration/Task 10 is the provider; shared logging is the consumer.
The provider supplies a **resolved writable logging destination** and validated
settings, or the shared defaults. The shared owner retains formatting, path
helpers, rotation and failure behaviour. Resolve the destination once before work.

Preserve existing Watcher/Handler path contracts, stdout/stderr/help behaviour and
INFO/10 MiB/five-backup defaults unless separately changed. The retained learner
receives an explicit destination and uses retained defaults; it never loads mutable
application configuration. Its config-free path selection is specified in D.

This seam does not decide Task 10's configuration authority, discovery strategy,
installer, package layout, doctor or UI. Those remain Task 10 decisions. Explicit
destinations permit logging implementation before Task 10 is delivered.

## C. API

All following journal APIs are **proposed**, not existing symbols. Existing
`get_logger`, `event`, `log_context`, `context_fields` and close semantics are
extended/reused. Pseudocode omits implementation detail, not application work.

### Backend extension

```python
# runtime_logging.py; preserve existing keyword callers and return handler.
CHECKPOINT_INTERVAL_SECONDS = 5.0

def default_logging_settings() -> dict:
    # Fresh dict: INFO, 10*1024*1024 bytes, 5 backups.
    ...

def configure_runtime_logging(*, database=None, runtime_root=None,
                              startup_pid=None, settings=None,
                              destination=None): ...

def invocation_log_path(log_dir, component, invocation_id) -> Path: ...

def observer_log_path(runtime_root, *, timestamp, pid) -> Path: ...
```

Move `ConfigurationError`/`load_config` imports inside `logging_settings()`.
Reject simultaneous destination and database/runtime-root/startup selectors.
Settings selection is explicit and centralized:

```python
if settings is not None:
    selected_settings = settings
elif destination is not None:
    selected_settings = default_logging_settings()
else:
    selected_settings = logging_settings()
# Validate selected_settings in the shared backend before configuring handlers.
```

Standalone callers can use `configure_runtime_logging(destination=path)` without
importing application config. Legacy calls without a destination continue to use
application settings when settings are omitted, or their supplied settings, and
the unchanged `runtime_log_path`. Invalid explicit values raise before work
without importing config. Retain the existing configuration-specific exception
at the application-config boundary.

Setup makes/opens the destination before substantive work; failure is visible.
After setup, formatter/write/rotation errors and close/remove-handler errors are
best effort. Preserve encoding, severity fields, UTC timestamp, PID/thread fields,
scoped context and scoped suppression of logging failures. Do not install a second
root handler in a watcher/observer that already owns its destination.
`observer_log_path` preserves `watch/log-progress-<timestamp>-<pid>.jsonl`;
its arguments are the observer's existing timestamp/PID, not newly inferred facts.

### Call/checkpoint adapter

```python
# journal.py; stdlib plus .runtime_logging only.
def get_journal(component: str) -> Journal: ...

class Journal:
    def call(self) -> CallScope: ...
    def checkpoint(self, completed: int | None = None,
                   total: int | None = None) -> None: ...

# Proposed insertion; the function owns completed-input progress.
def collect_records(logs, *, parser):
    with journal.call():
        records, evidence_stats = {}, {}
        total = len(logs)
        for completed, evidence in enumerate(logs, 1):
            # Existing read/hash/recovery/record code remains here.
            ...
            evidence_stats[evidence.sha256] = stats
            # This input has now been completely processed.
            journal.checkpoint(completed, total)
        return group_records(records.values()), evidence_stats
```

This count is **completed inputs / total inputs**. Two inputs with the same hash
still represent two processed inputs, so each advances progress. Caller-owned
means the work-owning code supplies a truthful local count at its natural
completed-work boundary; the counter need not predate instrumentation. A trivial
loop index or `enumerate()` is allowed. Here `len(logs)` uses the existing sized
sequence and enumeration adds no traversal or application processing. Scanning,
materializing or recomputing application state solely to obtain counts is forbidden.

Use an explicit context manager, not a caller-held token or generalized decorator.
Early returns/exceptions in `sync_registry` and source-content cache paths make it
useful: one scope records entry, normal return and elapsed time, then restores
local context on every exit without rewriting the algorithm.

`CallScope.__enter__` copies function identity, remembers monotonic start time and
installs a local active scope in a `ContextVar`. `__exit__` emits `call_finished`
only when `exc_type is None`, resets local context and returns false. Nested
canonical scopes log neither tracebacks nor exception terminals. `SystemExit(0)`
is not a normal call return; the invocation can still observe success. A normal
return carrying a failure result is not proof of operation success or SQL commit.

**No call IDs, parent IDs, call tree or cross-call relationships are part of v1.**
Invocation identity, actual function/source, timestamps/event order, PID/thread
and existing request IDs provide the needed observations in selected current
paths. No current execution case demonstrates a need for a call ID. If one is
later demonstrated, document that exact case as a blocking exception to this
design rather than retaining speculative correlation machinery.

Ordinary scope state is copied identity scalars, start time, one last counted-hook
line and one last-emission time, plus the token needed to restore local context.
There is no per-site dictionary or accumulated call history. Resetting local
throttling has a concrete use: registry feature creation repeatedly invokes
`collect_records`, whose next call must emit its first count independently.
Nested scopes restore the enclosing local state; recursive use would likewise
have local timing without emitting recursion relationships.

Do not transport scopes, tokens or call context across threads, processes or
queues. Leave existing Pipeline request fields/context transport unchanged.
`request_id` and handler identity remain authoritative. A foreground observation
may record the already returned `RequestRef` to help find the corresponding
request; it introduces no correlation protocol. Existing `log_context` supplies
foreground invocation metadata. No workflow or invocation state machine is added.

### Real source identity and helper handling

For a checkpoint inspect its immediate caller; for `CallScope.__enter__` inspect
the external `with` caller (a class avoids a generator-contextmanager helper
frame). Copy `co_qualname`, filename, `co_firstlineno`, `f_lineno` and module
identity strings, then delete the temporary frame in `finally`. Retain no frame,
locals, code object, bound method, arguments or return value. Adapter failure
after setup cannot prevent entry, suppress a return or mask a pending exception.

Prefer the caller's `__spec__.name`, otherwise `__name__`. `runpy` supplies the
operation module's spec despite `__main__`. For the retained launcher, existing
`_ck3_learner_execution.folder` and actual `co_filename` identify `launcher.py`;
record actual `__main__` identity rather than guessing an importable symbol.
A retained origin can supply its module path where available. Ordinary scripts
without a spec remain `__main__` with their actual source path.

Checkpoint line means the executed hook line. Call records identify the real
function and entry-hook line; normal-return records reuse that identity and add
monotonic elapsed time. Do not guess the next/return statement. An imported
`derive_pattern` would identify `template_learning.patterns.derive_pattern`.
Adapter helpers pass extracted identity internally; no arbitrary user-frame
skipping, symbol registry, AST or bytecode lookahead. A diagnostic checkpoint in
an actual helper names that helper, not its caller.

### Counts and suppression

Use one centrally owned **five-second interval**. No per-function settings,
modulo policies, unit taxonomy, percentages, ETA or global progress.

| Form | Meaning / emission |
|---|---|
| `checkpoint()` | Immediate deliberately inserted inside-call diagnostic location. No count keys; does not change counted throttling. Not routine entry/return punctuation. |
| `checkpoint(done)` | Truthful caller-owned completed count. First local counted observation emits; repeated loop observations emit after the interval. No inferred total. |
| `checkpoint(done, total)` | Same, with the locally owned compatible total. Explicit completed total always emits. |

The final guard is explicitly
`completed is not None and total is not None and completed == total`.
Omitted values are not completion. Explicit `(0, 0)` is valid only when the caller
knows those values. Counts must be nonnegative integers (not booleans); total
requires completed and `completed <= total`. Invalid hook arguments are coding
defects: discard the invalid observation without raising into application work,
and catch them during source review/genuine verification. Never clamp values.

Selected loops need one loop hook. If a later completed-only hook needs an explicit
final observation, the caller can supply it after the loop. A changed hook line
resets the one local throttle timestamp, making that final observation immediate. This is not independent
history for each site: only the last line/time is retained. Same-line loop
observations use the interval; completed-total equality bypasses it. A new call
starts fresh. Counted hooks outside a matching local scope emit without retained
throttle state; current selected counted hooks all have an owning scope.

There is no inferred final flush. On full completion, the final `collect_records`
iteration passes `completed == total`, bypassing suppression; an input that raises before
the hook contributes no completed-input observation. All selected known-total
loops use this equality guard. Do not append redundant final hooks after that
emission. An empty input sequence reaches normal call return without a loop
checkpoint. Repeated complete totals intentionally bypass suppression.

Suppression does only identity/scalar/clock checks. Serialize/write only emitted
events. Never compute hashes, evaluate lazy model properties, run inference,
inspect a model or serialize diagnostic bodies for fields. Bare diagnostic
capability remains available, but **no routine bare checkpoint is selected in E**.

## D. Release integration

### One source-to-payload mapping

Keep `FILES` as the learner-local inventory; do not append virtual shared names
that break its existing `source/name` consumers. Define one authoritative mapping
in `learner_loader.py` and have creation, fingerprinting and reference comparison
consume it:

| Authoring root / file | Retained payload |
|---|---|
| Explicit `source`, each existing `FILES` member | `template_learning/<member>` |
| Current loader source (existing launcher copy rule) | `launcher.py` |
| Explicit `application_source/decoder.py` | `ck3chronicle/decoder.py` |
| Explicit `application_source/runtime_logging.py` | `ck3chronicle/runtime_logging.py` |
| Explicit `application_source/journal.py` | `ck3chronicle/journal.py` |

No `config.py`, application `__init__.py`, mutable configuration or installed-module
fallback is retained. The existing retained namespace package is enough. The
shared files are exact bytes from their application owners; generated copies are
immutable payload, never another editable source. The decoder remains the same
dependency, not a new logging implementation.

Proposed helpers/signatures, all owned by the loader:

```python
def source_payloads(source, *, application_source) -> dict[str, bytes]: ...
def implementation_identity(source, *, application_source=None) -> dict: ...
def verify_implementation_reference(identity, *, execution_context) -> None: ...
```

`source_payloads` applies the mapping once and rejects absent inputs. In authoring
mode `implementation_identity` requires explicit application source; in retained
mode it uses the already authenticated execution context. `artifacts.learner_identity`
returns a copy of that authenticated manifest identity, rather than trying to
discover a checkout application directory. Publication reference verification
still checks retained disk bytes against the identity; context lookup does not
remove that integrity check.

Preserve learner-local `implementation_hashes` keys. Add
`shared_implementation_hashes` keyed only by the two new logging payload paths,
`ck3chronicle/runtime_logging.py` and `ck3chronicle/journal.py`.
For new identities compute the fingerprint from the canonical tuple
`(version, implementation_hashes, shared_implementation_hashes)`; absence of the
new field uses the existing two-element formula for genuinely older manifests.
Manifest authentication validates both sets against their mapped payload bytes.
This makes shared owner/adapter explicit implementation dependencies for new
releases while preserving old identities exactly. The decoder keeps its current
distribution treatment; do not add it to the learner implementation fingerprint
or create an independent decoder pin. The complete manifest's
existing hash map and release-ID formula also cover these files, the launcher and
new capability. No parser-version or algorithm-label increment is implied by a
logging-only edit; changed fingerprints/releases are mandatory regardless of label.

Add authenticated manifest capability `journal_api: 1` for the complete new
distribution. Reject unknown journal API versions and a capability missing either
shared logging payload; do not infer support from a file name or version nickname.
Keep historical envelopes on their existing execution, without claiming journal
support. Adding optional authenticated fields does not require changing the
existing schema-1 envelope; the new loader validates the capability explicitly.

Inspect/repair every present assumption:

- `implementation_identity` and `create_release`: one mapping and identity formula.
- `authenticate`: old local hashes plus explicit new shared hashes; external pin,
  release-ID, parser identity and operation checks remain mandatory.
- `artifacts.learner_identity`, candidate algorithm metadata and registry checks:
  carry the complete new identity. Never continue a previous-release registry by
  weakening equality checks.
- `publish_native_model.verify_reference_implementation`: use the helper for local
  and shared retained bytes; no unchecked `../` names or ambient application lookup.
- `recover_large_candidate_export`: use the same map for its byte comparison,
  including shared bytes. `review_short_thresholds`: supply explicit source root.
  `evaluate_unseen_session` and `location_candidate_experiment.build` already call
  `launch`; defaulted new keyword parameters preserve these calls.
- `RetainedImports.get_code`, compile audit, `finder.loaded`, `compiled_sources`:
  preserve all restrictions and include the two new shared imports in receipts.
  Do not broaden audit's “publish” exception beyond identical authenticated bytes.
- `matcher_loader.RUNTIME_FILES` and `publish_package`: leave matcher closure
  unchanged. Selected initial hooks are learner/application functions, not modules
  copied into the production matcher. Publishing a candidate must still pass its
  genuine reference checks; journaling does not weaken `require_candidate`.
- `register_release` already copies authenticated manifest payloads; reuse it.
  `pyproject.toml` has explicit retained-resource entries: later packaging must
  include the new learner's `ck3chronicle` directory, not merely `template_learning`.
  Verify wheel/source/installed correspondence in both directions and preserve
  `.gitattributes` release-byte rules. No release is generated during 09A.

### `run --log-dir` transport and provenance

Proposed signatures:

```python
def launch(folder, pin, operation, arguments, *, receipt=None, log_dir=None): ...
def execute(folder, pin, operation, arguments, receipt, *, journal_options=None): ...
```

1. Add `--log-dir PATH` on outer `run`, **before** its positional operation.
   Keep `REMAINDER` and the existing optional separator removal. Arguments after
   the operation belong to the operation; never strip similarly named arguments
   from that vector. Preserve the existing parser-manifest injection unchanged.
2. Authenticate selected release and operation first. `launch` checks `journal_api`.
   Explicit `log_dir` with an old/unsupported release raises `ReleaseError` before
   spawning. Omitted `log_dir` with an old release invokes its original launcher
   protocol unchanged, with no claim of journaling. Never patch an old worker.
3. For a capable release, `launch` resolves an explicit `--log-dir` first. When
   omitted, use `<receipt-parent>/learner-logs` if a receipt was supplied; otherwise
   use `<cwd>/.ck3chronicle/wip/learner-logs`. The current `launch` already receives
   the optional receipt, and its child keeps the outer cwd, so this uses an
   existing explicit input without worker configuration. Expand `~` and resolve
   paths once in `launch`; pass the resolved receipt path and destination to the
   worker. A bare relative receipt filename uses the outer cwd as its parent.
   Failure to open the chosen location is an error, never a fallback to another
   directory. Generate one UUID **invocation** ID; backend helper names
   `learner-<invocation-id>.jsonl` within that directory.
4. Transport one small JSON object (API 1, absolute destination, invocation ID)
   as a private positional header to a new `_execute_journal_v1` worker route.
   Retain the old `_execute` shape for old retained launchers. Pass subprocess argv
   as a list, not shell text or environment configuration; operation arguments
   follow the private header intact. No user logging flags enter `sys.argv` of the
   operation. Worker validates absolute path/component filename and API version.
5. After reauthentication and audit setup, call the retained backend with the
   explicit destination and omitted settings; it uses its own shared defaults
   and opens the file. Settings are code-pinned to that release;
   they are not silently inherited from the installed application. Announce the
   resolved journal path to **stderr**, once, only after successful setup.
6. Every event has invocation ID; retained events additionally carry compact
   `release_id`. The start event supplies manifest pin, learner fingerprint,
   already-known parser identity, operation and journal location. Do not read a
   model to manufacture matcher/package provenance; include it only if the owning
   operation already has it. Receipt adds invocation ID, journal path, rotation
   settings and observed terminal detail while preserving current module/audit,
   parser, argument, environment and identity fields.

Rotation uses existing `.1` through `.5`, in the invocation's own filename
namespace. A surviving event's invocation ID plus release ID identifies the
retained source even when the start record has rotated away; the release ID
authenticates its canonical manifest contents and the catalog/receipt provides
the external pin. Full provenance is written once at start, not at every
checkpoint; no new sidecar/provenance database or repeated fake start event is
needed. Existing optional receipts remain optional and independent. If all old
segments and the receipt are absent, do not claim their observations survived.
For application journals, attach already-known artifact identity when available;
otherwise state source path/version and the limit that mutable source cannot be
identified as an immutable installed artifact. Never hash the application solely
to enrich an event.

### Worker lifecycle, receipts and terminal semantics

Order for a capable retained worker:

```text
authenticate manifest/payloads → verify worker bytes and operation
→ reject preloaded learner modules → install execution context/finder/audit
→ import retained logging owner/adapter → configure destination
→ invocation_started → parser-argument checks / operation imports / runpy dispatch
→ attempt receipt → invocation_finished (if terminal outcome observed)
→ detach/close logging → preserve original return/raise
```

Authentication, retained-logging import and file-setup failures occur before a
configured authenticated invocation exists: stderr/nonzero subprocess result
remains evidence; do not fabricate a start or finish. Operation import failure
after setup is an observed failed invocation. Start is before `runpy`, so imports
and argument failures are covered. The retained launcher itself is authenticated
by the existing byte check; importing logging must happen under the audit hook.

Use an outer `try/except BaseException/finally` around dispatch and receipt,
without swallowing the pending exception. Snapshot terminal scalars and the
exception for boundary handling only; do not put exception objects/tracebacks
into long-lived adapter state. Emit one invocation terminal with useful traceback
for an unexpected exception. Nested call scopes emit no traceback and no false
return. Free boundary exception references at exit.

| Observed result | Required treatment |
|---|---|
| Normal runpy return / `SystemExit(None or 0)` | Existing successful execution/receipt `status='completed'`; terminal outcome `success`. `SystemExit(0)` handling stays at existing dispatch boundary. |
| Nonzero integer `SystemExit`, or string code | Terminal `nonzero_exit`, original code/detail; re-raise the original. Preserve Python's string-exit stderr behaviour, do not coerce it into success or an invented integer. |
| `KeyboardInterrupt` | Terminal `interrupted`; re-raise. Do not emit normal call finishes for unwound calls. |
| Other exception | Terminal `failed`, exception class and traceback once in journal; re-raise. Ordinary interpreter stderr traceback remains intact. |
| Receipt write fails after successful dispatch | Dispatch remains observed as successful, `receipt_written=false`, receipt error recorded. Invocation fails because the required requested receipt could not be written; propagate that error as today. Never claim receipt success. |
| Receipt write fails while another exception is pending | Preserve/re-raise the original exception, record receipt failure as secondary detail without replacing the original traceback. Old receipt `failed` status remains compatible; new terminal fields distinguish the actual outcome. |
| Close/flush fails after setup | Best effort; never replaces dispatch/receipt outcome. |
| Kill/crash/power loss | Missing terminal/receipt is unavailable outcome, not inferred failure, hang or success. No restart/recovery mechanism. |

`launch` retains `subprocess.run(..., check=True)` and its returned CompletedProcess
or CalledProcessError behaviour. The child owns journal outcomes; the parent must
not append a second terminal based on its own interpretation. If the parent is
interrupted while the child continues, it cannot claim the child finished. A
successful local call and the worker exit must not overwrite an actual subprocess
failure produced by an operation. Reporting's ripgrep code 1 remains normal “no
matches”; codes outside its existing accepted set remain its current incomplete
search outcome, not a new logging interpretation.

For application CLI commands that catch errors and return a code, preserve those
codes and stdout/stderr payloads. Preserve existing caught-error events and
traceback behaviour, including Reporting's `report_failed` and
`report_error_output_failed`. Root dispatch emits `invocation_finished` with the
returned code and no added traceback. If an exception escapes the new canonical
invocation boundary, that boundary records it once; nested canonical scopes do
not record it. Do not redesign existing component error ownership or mark
exceptions as already observed. Independently imperfect historical behaviour is
outside this task. Only a concrete duplicate/masking problem caused by the new
journal warrants a narrow integration fix.

The learner's existing receipt-finally issue is the specific exception: retain
the bounded worker repair above so receipt/logging cleanup cannot replace its
original execution failure. It does not commission general exception cleanup.

## E. Project-wide instrumentation map

The corrected map selects scopes only where real function entry/normal return and
elapsed time add useful visibility. Counts come from truthful local completed-work
state, including trivial loop indices added for instrumentation. Existing counters
can be reused when their meaning matches; a sized collection's length costs no
traversal. **No bare checkpoint is selected for ordinary initial operation.**
That diagnostic primitive remains available when a specific opaque/slow call
needs internal observations (F). No scan, hash, inference, diagnostic serialization
or algorithm rewrite is added for fields.

### Learner — delivery L

| File/function | Why / entry-return | Existing completed count / total | Bare checkpoint disposition | Required change / extra computation |
|---|---|---|---|---|
| `learner_loader.execute` | Authenticated operation invocation; invocation events only | None | None initially; dispatch start already locates work | Required L: setup, transport and bounded terminal/receipt handling in D. Covers learn/registry/evaluate/publish/review/visual-review/compare. |
| `learn_error_templates.main` | Real `collect_records → build_model → write_bundle` calls provide boundaries | None needed | None | No edit. Preserve operation JSON and progress console output. |
| `records.collect_records` | Parsing/collection can take substantial time; scope shows entry and normal completion | Local `completed` from `enumerate(logs, 1)` after full input processing and stats assignment / `len(logs)` | Only future diagnosis around `read_evidence` if warranted | Required L: one call scope and counted-total loop hook; final successful input bypasses suppression. A trivial index adds no traversal, read or hash; no after-loop hook. |
| `incremental_template_registry.sync_registry` | Input/cache synchronization can involve long file work; scope supplies elapsed time | Existing `summary['paths_seen']` after path cache/entry processing succeeds / `len(paths)` | No after-registry-write hook; normal return suffices | Required L. Name the list from the existing single `candidate_paths` call; no repeated inventory. Do not emit at its loop-entry increment or treat `paths_hashed` as completed paths. |
| `combine_training_records` | Existing feature loading is inside registry build invocation; no demonstrated need for a separate initial pair | No checkpoint selected; input iterable need not be counted | Available for later specific load/merge diagnosis | Removed from initial hooks because distinct initial visibility is not needed, not because a local index would be prohibited. |
| `build_revision` | Invocation and selected `build_model`/`write_bundle` scopes cover its substantive work | None needed | Remove after-registry-write checkpoint | Removed from initial scopes; lock/registry semantics unchanged. |
| `artifacts.build_model` | Substantial model construction; function entry/return and existing source-family completion useful | `len(source_summary)` after existing source summary assignment / `len(sources)` | No routine hook after `evaluate_records` | Required L: scope plus counted source loop. Use existing collection lengths; no lazy property access. Preserve `Learned ...` console output. |
| `artifacts.write_bundle` | Large serialization/publication can be opaque; function entry and return isolate this cost | None selected | Remove after-bundle-write/manifest hooks; normal return suffices | Required L: scope only. No extra file hashes or serialization. |
| `clustering.refine_region_groups` | Existing console progress plus enclosing build scope supply initial visibility | `seen` pairs and `ordered` groups are not a valid pair; no count selected | Diagnosis-only if a real need arises | Removed from initial scopes. `clustering.py` leaves the edit set. Preserve modulo-100 console output and branching. |
| `clustering.choose_medoid` | Repeated expensive expression; extra entry/return volume not justified initially | None without unnecessary restructuring | Diagnosis-only | No initial hook; never expand `max`/generator for logging. |
| `patterns.derive_pattern` | Frequent inner inference, correctly defined in `patterns.py` | `maps`/`units` could support a later completed mapping observation, but none selected | Diagnosis-only | No initial hook; do not instrument each inner block. |
| Publication/reference and evaluation/review helpers | Existing authenticated invocation and reference checks cover selected operation | Existing validation/result counts stay result data | Diagnosis-only | Mapping repair remains required; no extra function tracing. Preserve reference verification, console and receipts. |

This reduces the initial learner scopes from seven to four. The new shared
adapter and authentication/loader work remain necessary; the reduction is in
application instrumentation, not release integrity. Optional deeper diagnosis is
not a scheduled delivery obligation without a demonstrated need.

### Pipeline — delivery P

| File/function | Useful existing coverage / entry-return decision | Counts / totals | Bare checkpoint disposition | Component disposition |
|---|---|---|---|---|
| `database_handler.serve`, `_Handler` admission/finish | Existing handler lifecycle and accepted/terminal request events already identify process work | Existing results and queue fields suffice | None | Already sufficient; no new process invocation pair or source edit. Preserve exclusive listener bind before logging. |
| `_prepare`, `_database_worker`, `database_call` | Existing preparation/database operation pairs, request identity, queue waits and elapsed times cover boundaries | No count needed | None | Already sufficient; no new scope/context transport or exception-ownership edit. |
| `ingestion._ingest` | Existing preparation start/completion/failure and database submission events identify work; extra scope duplicates this boundary | No count selected because existing coverage suffices. A trivial completed-result index is allowed if later warranted; emissions are not a unit total. Do not read private ReviewWriter counters | Future diagnosis only if parsing/classification needs specific internal locations | No logging change. Removed proposed scope, iterator enumeration and ordinary bare hooks. Preserve duplicate paths and actual outcomes. |
| `request_handler.HandlerClient.submit` | Foreground invocation currently lacks the accepted request reference visible in handler logs | Returned `RequestRef` only; no counts | None | Required P: one `request_accepted` client observation after successful `_rpc` only when foreground invocation context is active, carrying actual request/handler identity. No duplicate of Watcher's existing acceptance, scope, argument dump, protocol or poll change. |
| `repository.Database.write_run`, `_insert_records`, review/accounting | Existing worker operation events/waits and return locate storage work | Existing accounting remains storage evidence; no recomputation | None initially | Already sufficient. No transaction, commit, uncertain-write or cleanup changes. |
| `retention.retain_raw_logs` | Watcher records exact returned eligible/removed/skipped/problem information | Existing returned results suffice | None | Already sufficient for current runtime use. No per-file journal or deletion campaign. |
| `pipeline.catalog.main`, `evaluate_package` | Standalone operation needs foreground invocation; evaluator scope would duplicate its dominant operation | Existing evaluation counts remain output data | Remove after-output-write hook | Required P/A: invocation setup/terminal only in `main`; leave evaluator algorithm/hooks alone. |
| Parser/classifier/bindings/contracts/model/accumulator/schema | Existing owning preparation/evaluation and authenticated APIs enclose work | None added | Diagnosis-only | No logging change, package regeneration or second implementation. |

Retain `handler_started/ready/shutdown_started/stopped/failed`,
`request_accepted/completed/not_completed`, preparation/capture-wait/ingestion-warning
and database open/close/operation/wait/uncertain-write events. Existing
`request_id`, `handler_instance`, database/capture/run references and queue/elapsed
semantics remain authoritative. Status polls stay silent. Bootstrap stderr stays
`<database-parent>/logging/<database-name>/handler-bootstrap.log`.

Leave historical traceback behaviour and error ownership unchanged. Canonical
nested instrumentation adds no traceback; no exception marking or redistribution
between worker and preparation is proposed. Existing events are not renamed just
to make their vocabulary resemble canonical event names.

### Watcher — delivery W

| File/function | Useful existing coverage / entry-return decision | Counts / totals | Bare checkpoint disposition | Component disposition |
|---|---|---|---|---|
| `EventJournal`, `cli.cmd_watch`, `watch_sessions` | Existing watcher/process/capture lifecycle and failures identify observed work | Existing polls/captures are observed facts, not work-to-total | None; no per-poll journal | Already sufficient/no logging edits. Preserve lease-owned setup/close and failed-startup PID destination. No duplicate canonical lifecycle pair. |
| `harvester.spool_logs` | Caller capture start/completion/failure and manual foreground invocation suffice | No count selected; optional debug/crash attachments make a naive fraction misleading | Remove copy/metadata/callback/rename punctuation | No logging edit or scope. Preserve protected-copy/publication ordering and optional degradation. |
| `watcher_processing.start/_startup/_ingest/_monitor_results/_maintain/close` | Existing submit/accepted/outcome/warning/unavailable/retention events provide useful facts | Existing actual results/references suffice | None | Already sufficient. Preserve retries, unavailable-result clearing, silent polls and closing workers before journal/lease. |
| `logging_observer.observe_logging_progress` | Existing observation events are useful but ordinary JSONL bypasses sole backend owner | Existing measurements remain heartbeat data; no new counters | None | Required W: delegate existing ordinary events and path to shared owner/rotation. Preserve returned path, timestamp/PID naming, heartbeat content/replacement/removal and measurement algorithm. No new scope/thread/read. |
| Playset/crash inventory/process probe | Caller warning/failure/fact events cover operations | None added | Diagnosis-only | No changes or extra scans/inferred facts. |

Watcher JSONL stays `<runtime-root>/watch/events-watcher.jsonl`; failed startup
stays `events-startup-<pid>.jsonl`. Preserve `schema_version`, `watcher_pid`, capture
facts, warnings, existing error fields/tracebacks and operator queries. Do not add
`exc_info` overrides or redistribute capture/probe exceptions. `observe-logging`
uses the shared standard formatter for ordinary existing event names/payloads;
its replaceable measurement heartbeat remains a separate existing state artifact,
not another backend. Preserve old files and all existing observation behaviour.

### Data Intelligence / Reporting — delivery R

| File/function | Useful visibility / entry-return decision | Existing counts / totals | Bare checkpoint disposition | Component disposition |
|---|---|---|---|---|
| `DiagnosticAnalysis.list_runs` | Handler reads plus foreground invocation already cover the short local selection | None needed | None | No local hook. Preserve missing-time Run eligibility. |
| `DiagnosticAnalysis.search_runs` | Cross-Run iteration has no encompassing useful existing event pair; scope distinguishes entire search from individual investigations | `len(matched)` counts matching Runs, not searched Runs. A trivial completed-search index would be allowed; no checkpoint selected initially | Remove loop-end bare hook | Required R: call scope only; additional progress hooks need a demonstrated visibility need. |
| `DiagnosticAnalysis.investigate` | Existing `investigation_started/completed` identifies run/package and summary, with comparison availability events | Preserve existing result counts; `len(data)/len(chosen)` is not successful work total | Remove post-read/post-source-loop hooks | Already sufficient once A configures foreground logging. No additional scope; retain warnings and error behaviour. |
| `SourceSearch._search`, `resolve`, `search` | Existing source-search completion/coverage and containing investigation provide ordinary context | Preserve existing result counts; no new set/comprehension for fields | Remove after-`_files`/resolution hooks | No added scopes; existing coverage sufficient initially. |
| `SourceSearch._content` | Substantial decoding/ripgrep execution is otherwise opaque until source search finishes; real scope adds distinct entry/elapsed visibility | Batch/return-code metrics already exist but no appropriate local completed-success counter. No checkpoint selected | Remove routine post-batch hooks | Required R: scope only, including cache/early return. Keep code 0/1, incomplete-search semantics, subprocess cleanup and existing metrics. |
| `reporting.cli._emit` | Rendering/encoding/output work occurs after analysis and can be substantial; scope locates its start and duration | None selected | Remove post-encoding/write/stdout hooks | Required R: scope only. Preserve render-before-write, UTF-8/surrogate and appendix behaviour. |
| `cmd_report/cmd_runs/_failure` | Existing export/failure events and console payloads are useful | Existing output data unchanged | None | Preserve `report_exported`, `report_failed`, `report_error_output_failed` and existing traceback ownership. New invocation finish records returned code without adding another trace. |
| Query/source-query/reference/preset/explanation/presentation helpers | Covered by existing operation events and selected substantive scopes | None | Diagnosis-only | No local hooks or predicate/render-node tracing. |

Existing `failure_stage` stays an existing error payload field; it does not become
a journal workflow. Library functions still raise original exceptions and do not
configure files. Application entry provides the configured foreground destination.

### Application entry points — delivery A

| Entry | Disposition |
|---|---|
| `ck3chronicle.cli.main`: capture/ingest/runs/report/doctor | Required A: foreground invocation setup/terminal after parsing, with explicit `--log-dir` override. When configuration is used, obtain resolved writable destination/settings through its existing path authority; use shared path naming under `<ROOT_CK3CHRONICLE>/logging` for the current application. Preserve stdout/stderr/help and return/exception semantics. No doctor or caught-error redesign. |
| Root `watch` and `observe-logging` | Existing component owns destination/lifecycle. Do not wrap it in another handler, call scope or canonical terminal pair. W converts only observer JSONL backend. |
| Learner `run` | L child owns canonical invocation. Parent authenticates, resolves/transports logging options and preserves subprocess semantics; no parent terminal in child's journal. |
| Learner `create/list/register`; `pipeline.catalog.main` | Required A: foreground invocation around actual dispatch, no individual helper tracing. Prefer explicit `--log-dir`; standalone config-free default is `<cwd>/.ck3chronicle/wip/learner-logs` for learner administration, or `<cwd>/.ck3chronicle/wip/model-release-logs` for model catalog. When already using application configuration, consume its resolved destination instead. No fallback on open failure. Component filenames remain `learner-admin-<id>.jsonl` / `model-release-<id>.jsonl`. Preserve JSON stdout and existing authentication/registration. |
| Direct handler module entry | Existing exclusive-listener/bootstrap/file/close behaviour is sufficient; no new hooks. |
| Historical research/support scripts | No general tracing rollout. Repair only directly affected mapping consumers identified in B/D; no new operation registry or campaign. |

The first executable slice is shared owner/API plus **L**. **P, W, R and A remain
explicit subsequent deliveries**, including their no-change receiving checks.
P adds foreground request references; W removes the observer's duplicate backend;
R adds three substantial client-side scopes; A makes foreground evidence durable.
A is needed to receive R's CLI journaling. Completing L alone is not project-wide
adoption; integrated packaging/receiving remains Pipeline-owned.

## F. Diagnostics extension

For a genuinely observed slow function, edit its authoring source only. Add bare
`journal.checkpoint()` immediately before/after the actual suspected call, or add
one local `with journal.call()` if function entry/normal-return timing is needed. Example: surrounding
the existing `read_evidence(evidence.path, parser=parser)` in `records.collect_records`
records positions in **collect_records**, not fictitious progress inside a parser.
The source between those observations is the diagnostic evidence.

Use the same source/payload map to build a new task-owned immutable candidate
release, with a new fingerprint/ID and separate state/output/journal. Authenticate
and execute that candidate explicitly. No global tracing config, symbol registry,
profiler, hang detector or live-patch mechanism is introduced. A missing later
checkpoint identifies only the last recorded location. Remove optional hooks by
a deliberate authoring edit and another candidate, never by changing a retained
release or running process. Verification compares application results as in G;
the removed observations need not leave their own replacement events.

## G. Verification

Everything in this section is a **future verification plan**. Read-only inspection
for 09A does not establish runtime correctness. Execute only the bounded delivery
authorized next; reuse applicable existing evidence and name unverified cases.

1. **Source/API boundary.** Review exact patches against preserved working bytes.
   Parse/compile changed source using `.venv/Scripts/python.exe -B` without launching
   operations; run `tools/check_runtime_logging.py` for runtime changes. Inspect
   lazy config import, context cleanup, first/periodic/final guard, source-frame
   release, no count-generating scans, stdout preservation and the new journal's
   non-masking/no-added-traceback behaviour. Existing component error ownership
   is not a cleanup target.
   Extend ownership coverage to adapter/learner hooks. The static checker alone
   cannot prove retained execution, rotation, outcomes or performance.
2. **Equivalent bounded learner execution.** Select a small existing genuine
   protected-log inventory from valid retained evidence, sufficient to exercise
   collect/build/registry paths. Preserve the same current-source algorithm,
   rules, parser, decoder, input ordering and build schedule in pre-logging and
   logging candidates. Use separate fresh same-version registry/cache/output
   directories; never continue production or another-release state. No 73-log
   campaign. Exercise learn, bounded sync/build, evaluate and permitted disposable
   export/reference verification only as included in the implementation assignment.
   Publishing a production release remains separately authorized.
3. **Journal observations.** On bounded genuine invocations inspect all five
   event kinds, actual source/qualified function/line, runpy identity, local scope
   restoration and separate invocation files. Counted-total coverage uses completed
   inputs / `len(logs)` in `collect_records`, successful path processing in
   `sync_registry` and source summaries in `build_model`. Compare final values
   with their actual input sequences/owning counters, not distinct evidence hashes
   or invented counts. Check that `collect_records` emits after full input processing
   and that its last completed input bypasses suppression. Counted-only remains an
   API capability: verify it on an authorized genuine use if one arises; otherwise
   leave its execution unverified rather than adding hooks to fill a matrix.
   A naturally longer-than-five-second loop can show suppression and final emission;
   if none fits the authorized work, periodic suppression stays dynamically
   unverified. Do not monkeypatch clocks or sleep to fabricate work. Bare checkpoints
   remain a source-reviewed diagnostic capability until a concrete diagnosis warrants
   a local hook on genuine execution; do not insert routine ones just to fill a test
   matrix. Unrepresented empty/nested/recursive cases remain unverified; no artificial
   recursion harness. No call-ID/call-tree acceptance criteria remain.
4. **Closure and transport.** Relocate the candidate and launch explicit paths with
   `-I -S -B` from outside the checkout. Authenticate manifest, all mapped payloads,
   both implementation hash sets, parser pin, loaded modules and compiled-source
   receipt. Verify shared logging paths resolve under that retained folder and
   `.config` is not imported. Inspect reference verification and derived publication
   executable records on a genuine bounded candidate. Check old-release ordinary
   execution against available genuine evidence and document unsupported explicit
   `--log-dir` rejection by source review unless a specific dynamic negative test
   is authorized. Do not corrupt release copies as an unapproved test.
5. **Outcomes and output.** Verify normal genuine completion, receipt-written truth,
   stderr path announcement, unchanged operation argv and stdout. Preserve each
   naturally encountered nonzero result/error; record it as failed verification
   where appropriate. Nonzero SystemExit, KeyboardInterrupt, receipt failure,
   cleanup failure, disk failure and abrupt termination are source-reviewed unless
   actually encountered or separately authorized for a specific test. Do not kill
   processes or inject these failures to fill a coverage table. Check journal
   absence of newly duplicated canonical tracebacks separately from normal
   interpreter stderr; do not impose new requirements on historical component logs.
6. **Pipeline/Watcher.** Reuse existing genuine lifecycle, capture, startup
   duplicate, playset, review and handler evidence for unchanged code. Check the
   new foreground client's accepted `RequestRef` against its genuine public-handler
   read and corresponding handler event. Use existing disposable receiving stores
   where available; do not ingest again merely to test a client observation.
   Confirm existing watcher/handler paths, setup ordering, request/queue fields,
   warnings and traceback behaviour remain unchanged by the shared extension.
   Do not restart live services. Observer backend conversion needs bounded genuine
   observation at a safe natural lifecycle; if unavailable, leave it unverified
   pending separate authorization. No fake process, forced failure, raw expiry or
   repeated historical ingestion is justified by logging. Old evidence plus source
   review is not fresh verification of changed observer execution.
7. **Reporting.** Reuse existing genuine stored receiving Runs through public
   `HandlerClient`, preferably the retained disposable receiving store. Verify
   listing, cross-Run search, history, source search/content, and JSON/HTML/text
   exports against unchanged query/results/paths. Use genuinely stored missing-time
   and preserved-byte witnesses already documented. Verify foreground file output,
   accepted request links, actual ripgrep results and source/encoding coverage
   without mock clients, invented histories or new fake paths. The prior two-emission
   source-path fixture exception authorizes no new logging fixture.
8. **Rotation and overhead.** Measure wall/CPU time, emitted journal bytes/events
   and observed workload sizes for equivalent pre/post candidates on the same
   bounded genuine inputs. Report raw measurements, cache/warmup conditions and
   limitations, not an invented overhead threshold. Use a naturally large genuine
   journal or an explicitly permitted smaller positive rotation setting during a
   genuine invocation; inspect `.1` ordering and surviving invocation/release
   association. Do not flood the backend with fabricated events. If rotation cannot
   be observed within authorized work, retain that limit. Do not rerun a full corpus
   to manufacture volume.
9. **Semantic comparison / removable hooks.** Compare native templates, supported/
   provisional/unknown outcomes, complete assignments, captures, contract records,
   review routing and application return values on equivalent inputs. Provenance
   identities necessarily change; list exactly which identity/timing/output-path
   fields differ rather than expecting byte-identical model packages. A follow-up
   candidate removing optional checkpoints must preserve the same semantics on
   that bounded input. Do not confuse concurrent inference/decoder edits with
   logging changes or weaken release/registry binding to force a comparison.
10. **Installed receiving.** Pipeline builds a fresh artifact/staging directory,
    verifies all changed source and required resources in both directions, installs
    outside checkout assumptions, and checks no ambient application/learner fallback.
    Receive P/W/R/A evidence against the exact combination. Preserve existing
    defaults and operator queries; no production activation is part of receiving.

The removed synthetic/fault-injection logging suite must not be restored.
**Creation or execution of each synthetic test requires explicit owner approval
for that specific test.** Historical 07C corrupt-copy and 07E fault recipes are not
authorization. Do not run broad historical test discovery merely because it exists.
Failed genuine checks and proposed requirements beyond this scope must be reported
explicitly. Unrepresented genuine cases remain unverified, not silently “passed.”

## H. Implementation sequence and preservation

### Edit rollback baseline

Before **each** later delivery edits source, save only:

- the exact current bytes of files that delivery will modify;
- prior absence for files it will create;
- relative paths, byte counts and hashes sufficient to verify the saved bytes; and
- directly coupled source files that must be changed atomically with those edits.

Use B's exact file list to select that delivery's rollback set; it is not a request
to archive every component at once. For example, the shared-owner delivery needs
`runtime_logging.py` and prior absence for `journal.py`, plus the checker only if
it is edited in that delivery. L saves its modified loader/reference/identity
consumers and three hook files. A dependency that is merely imported does not
belong in the rollback archive. Include tracked, uncommitted, untracked and relevant
ignored **edited files** equally; HEAD and a Markdown export do not preserve their
actual working bytes.

Save them in a new ignored task-owned directory, such as
`.codex-tmp/task09-logging-<unique-id>/before/<delivery>/`. Read/hash the saved
copies and compare them with the source snapshot; detect changes during copying
and refresh only the affected entries with their owner. Keep a small before/after
manifest and exact patch. No repository-scale inventory, restore rehearsal or
backup framework is required. This plan does not create that archive.

Before editing a shared file, coordinate with its active owner. Do not pause
another team's process, move its workspace or request a blanket freeze. If an
isolated checkout is needed, ensure it has the current uncommitted/untracked bytes
needed for that implementation; a branch from HEAD alone is insufficient. That
working checkout is not an obligation to duplicate its whole source into rollback
storage. Preserve the existing 06B archive
`.codex-tmp/task06b-archive-20260928T074827Z` unchanged; do not reuse its rollback
script for this work.

### Reproduction and verification inputs — separate from rollback

Identify/reference only the wider inputs actually used for a candidate or check:

| Input | Evidence to retain/reference |
|---|---|
| Current source used to create a new learner candidate | The normal source-to-payload mapping, implementation hashes and generated immutable manifest in D. Creation authenticates the declared executable closure; it does not enlarge the edit rollback set. |
| Selected retained learner/parser/model/package | Exact existing IDs, paths and external manifest pins; authenticate their declared payloads. The v61/current-package references in A are existing evidence, not an instruction to rebuild them. |
| Genuine input inventory and comparison inputs | Existing content-hash inventory, selected ordering and applicable same-baseline receipts. Keep raw evidence outside Git. |
| Selection/catalog/configuration | Actual identity/path and applicable configuration evidence needed to interpret that execution. Do not routinely copy all configuration, catalogs or package defaults into the source rollback archive. |
| Receiving artifact/store/resources | Reference the exact installed artifact and genuine public-handler evidence used. Use an existing consistent disposable store or an authorized backup if necessary; never present a loose copy of a live SQLite file as consistent. |

Existing immutable distributions normally remain in place and are referenced and
authenticated. Copy one only for a specific availability/recovery need, stated for
that input. Templates, decoder, all 44 learner closure files, all application
source, model JSON and receiving artifacts are **not automatically rollback
archive contents**. Required untracked/ignored reproduction inputs still must be
available/authenticated when used; a missing input is reported by name rather than
silently omitted. This separation preserves reproducibility without turning a
small logging edit into a preservation project.

### Dependency order and receiving ownership

| Order | Implementer / concrete delivery | Receiving owner and completion boundary |
|---|---|---|
| 0 | Each delivery owner: coordinate overlapping edits, save/verify only its rollback set and identify needed reproduction inputs separately | Pipeline coordinates shared files/packaging; Learner authenticates actual candidate closure. No blanket freeze or complete-source archive. |
| 1 | Pipeline: extend shared backend **without changing current callers**; add adapter | Learner receives config-free/authenticated-import suitability; Watcher/Pipeline confirm existing destinations/settings/fields unchanged. No new hooks yet. |
| 2 — first slice L | Learner: mapping/capability/identity/authentication/transport/terminal repairs, then selected learner hooks | Learner authenticates and genuinely checks isolated candidate; Pipeline receives distribution/package interface. “L complete” means this slice only. No model activation or full-corpus build. |
| 3 — P and W | Pipeline: foreground accepted-request reference and catalog invocation; Watcher: observer backend conversion | Watcher/Pipeline confirm existing request/capture/lifecycle coverage unchanged. Pipeline receives observer integration. No ingestion/handler/capture instrumentation rewrite or live restart. |
| 4 — A and R | Pipeline: foreground setup/entry composition; Reporting: only `search_runs`, `_content` and `_emit` scopes | Reporting receives configured CLI seam; Pipeline receives genuine public-handler/source/export results with existing error behaviour unchanged. Coordinate shared CLI sections. |
| 5 | Pipeline: integrate exact received sources and immutable resources into a fresh application artifact | Each component repairs its defects; Pipeline records integrated receiving and remaining limits. New source/resource hashes and installed correspondence, not a mutable label, identify delivery. |
| Separate | Owner decides whether/when to activate the concrete received artifact | Pipeline coordinates activation; Watcher owns observation/caller effects. No release registration as production, switch, restart or historical ingestion is implied by technical readiness. |

After each boundary, review exact file diffs and perform its bounded checks before
broadening hooks. Deliveries P/W/R/A remain explicit obligations until received;
completing L alone must not be reported as project-wide canonical logging adoption.
Task 10 can consume these seams independently and is not a prerequisite for L.

Rollback is an inverse of **this task's reviewed edits against current bytes**.
Keep per-delivery before/after hashes and patches. If a file changed since the
task's edit, resolve the overlap with its owner; never overwrite intervening work
with the saved baseline. Remove a newly created task file only if its current bytes
still match this task's owned version and no later work depends on it. Prohibit
`git reset --hard`, `git clean`, blanket checkout/restore, recursive source deletion,
tree replacement and in-place immutable release changes. Candidate logs, state,
receipts and outputs stay in a new ignored task namespace, separate from production
and concurrent learner experiments. Removing a hook always creates new candidate
bytes/identity; it never changes already-loaded code.

## I. Blocking questions

No unresolved design question blocks this plan. Ordinary choices are resolved:
one shared adapter, local call context manager without call IDs, five-second throttling,
config-free learner default, capability-gated transport and explicit remaining
component deliveries.

Before a later implementation edits overlapping source, its concrete prerequisite
is a verified copy of that delivery's edited current bytes and coordination with
active file owners. Reproduction inputs are referenced separately. This requires
neither a repository archive nor a Task 10 design decision. If an actual required
input is unavailable or an edit overlap cannot be resolved, report the exact
file/interface and affected delivery; do not substitute a HEAD baseline.

Simplification exposes no new blocking question. The corrected plan is ready for
owner disposition and subsequent Task 09B scope assignment. 09B, tracker enrollment,
implementation, candidate generation, publication and activation require their subsequent assigned
scope; none begins by completing this document.
