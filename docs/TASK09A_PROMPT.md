# Task 09A — Plan Canonical Logging System v1 implementation

Provisional task number, 2026-10-03. This is an **implementation-planning assignment**.
It ends with an implementation plan, not code. The incoming advisor may recommend
a different grouping or sequence; final implementation scope remains for owner
decision. This new 09A does not revive the obsolete Task 09 learner-reconnection
or deletion instructions.

## Objective

Inspect the current checkout and produce a concrete, minimal plan for
[Canonical Logging System v1](CANONICAL_LOGGING_SYSTEM_V1.md), the owner-approved
architectural direction. Logging observes real executable code and caller-owned
counts; it must not invent phases, stages, semantic checkpoints or a workflow model.

The reference's snippets are labelled **illustrative**, with existing symbols and
call signatures checked against source. `journal`, its methods and `call_token`
are explicitly proposed API elements. Final code must use actual CK3Chronicle
symbol/token definitions and contracts; new API elements must be defined rather
than assumed to exist. The corrected source observations below are the starting
point; inspect later changes before choosing implementation locations.

Do not implement, create a learner candidate, run a training campaign, publish,
change production selection, restart services, commit or push. Produce only
`docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` and a concise completion response.
Do not draft a document claiming that implementation or verification has occurred.

## Read and inspect

Checkout: `C:/Users/nateb/Documents/ck3chronicle`.
Read root and learner `AGENTS.md`, the development environment, and opening current
plan/status/handoff sections. Read the canonical reference, `RELEASES.md`,
`TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md`, `TASK07E_RUNTIME_LOGGING_HANDOFF.md`
and the current learner delivery/experiment guidance. Historical recipes do not
override current instructions. Do not read rejected database-handler designs.

Inspect at least:

- `src/ck3chronicle/runtime_logging.py`
- `tools/template_learning/learner_loader.py`
- `tools/template_learning/learn_error_templates.py`
- `tools/template_learning/incremental_template_registry.py`
- `tools/template_learning/records.py`
- `tools/template_learning/clustering.py`
- `tools/template_learning/patterns.py`
- `tools/template_learning/artifacts.py`

Follow actual callers where needed, including release/reference verification and
publication. Inspect existing watcher/handler logger consumers enough to name
the behavior that must remain intact. Do not broaden into a runtime rewrite.

The shared working tree includes unrelated and in-progress learner changes.
Use current source, not an assumed v45/v46 baseline or a stale release label.
Source inspection for this plan is read-only.

## Required design decisions

Show the minimum files and edits, concrete signatures/pseudocode and ownership:

1. Keep `runtime_logging.py` the sole editable backend/formatter/rotation/defaults
   owner. Determine the smallest explicit-destination/settings extension and
   config-import change needed for a retained learner without mutable application
   configuration. Preserve current watcher/handler callers and destinations.
2. Specify a small adapter API for call entry/return. Illustrative forms are `checkpoint()`,
   `checkpoint(done)`, `checkpoint(done, total)`. Derive actual module/qualified
   function/source/line from frames or functions. Resolve helper frames and
   `runpy`/`__main__` identity using existing execution context, without a symbol
   registry, AST/bytecode lookahead or retained frame/local references.
3. Define immediate bare checkpoints, counted first/periodic/final emission,
   monotonic elapsed time and the smallest throttling state. Recommend one simple
   centrally owned interval. Address nested/repeated/recursive calls and distinct
   invocations using actual needs, not a generalized tracing design. Guard the
   completed-total case explicitly; omitted counts are not a completed total.
4. Show one source-to-release-payload mapping for shared-owner and adapter bytes.
   Inspect all `FILES`/hash/copy assumptions. Cover authentication, implementation/
   release identity, executable audit, publication/reference checks and receipts.
   No editable duplicate owner or ambient import fallback.
5. Trace `run --log-dir` from outer argument parsing through `launch` and retained
   `execute`: path resolution, invocation ID, filename, retained configuration,
   stderr path announcement and unsupported-old-release handling. Preserve stdout
   and operation arguments. Recommend an explicit default without application
   config in the worker. Explain how provenance remains usable with rotation.
6. Locate invocation start/finish relative to authentication, retained imports,
   operation dispatch, receipt write and cleanup. Preserve actual success,
   nonzero `SystemExit`, `KeyboardInterrupt`, exceptions and subprocess results.
   Do not claim a normal call return on exception, double-log exceptions, mask an
   original error with cleanup, or infer outcomes after abrupt termination.
7. Select only significant actual functions worth instrumenting now. Counts
   originate in local application state at a completed-work boundary. No scans,
   extra hashes, inference, model inspection, lazy properties or diagnostic-body
   serialization for journal fields. No algorithm rewrite to expose progress.
8. Name current hooks/events/console outputs to retain, replace or leave alone.
   Existing runtime consumers must not lose useful behavior silently. Any broader
   conversion is a separate recommendation, not implicit implementation scope.

## Source-specific corrections checked against the checkout — 2026-10-03

- `collect_records` owns a sequence of logs. A completed-input checkpoint belongs
  after processing an input, not before `read_evidence`. Do not rewrite the parser
  to expose internal progress.
- `sync_registry` has `paths_seen`, `paths_hashed` and other existing counters.
  In the inspected code, `paths_seen` increments at loop entry; it is not evidence
  of completed processing at that location. A checkpoint using it belongs after
  that path's processing succeeds. `candidate_paths` returns a list, not a generator;
  the earlier addendum's generator description was incorrect. Do not call it again
  to obtain a logging total.
- `combine_training_records` loads existing entries; `build_revision` calls it,
  `artifacts.build_model` and `artifacts.write_bundle`. Prefer these real owners
  to invented stage labels, with the fewest useful hooks.
- `choose_medoid` uses an expensive `max`/generator expression. Entry/return may
  be sufficient; do not expand it into nested loops for logging counts.
- `derive_pattern` is defined in **`patterns.py`**, imported by clustering. It has
  materialized `units` and an outer mapping loop. Log the defining symbol/source,
  not a guessed `clustering.derive_pattern` location. Assess whether hooks here
  would flood journals across many calls; do not instrument every inner block.
- In `refine_region_groups`, `len(seen)` counts encountered pair identities and
  `len(ordered)` counts groups. They are not a completed/total pair. `seen.add(key)`
  precedes the pair's remaining checks/inference, so that location cannot report
  completed pair processing either. Preserve console behavior unless separately
  commissioned to change it; journal throttling need not inherit its modulo-100
  cadence.
- Recent learner experiments may change this inventory during planning. Document
  discrepancies and use actual current source. Do not undo another team's changes
  to make an illustrative example fit.

## Safe refactor plan required for subsequent implementation

Propose small, reversible edits, not replacement of source trees. Include:

- A bounded baseline of exact affected working files and their dependency closure,
  including tracked, untracked and relevant ignored source/resources. Git HEAD,
  a clean-looking diff or the Markdown source export alone is insufficient.
- A verified recoverable copy of those actual working bytes before edits, in a
  new task-owned ignored location, with relative paths/hashes and relevant prior
  absence recorded for new files. These are refactor safeguards, not extra runtime
  journal hashing or a new backup framework. Preserve the existing 06B archive.
- Coordinate ownership of overlapping learner/shared-logger files before editing.
  An isolated checkout must contain the required current uncommitted source;
  branching from HEAD does not automatically provide it. Do not move another
  team's workspace or interrupt its process to achieve isolation.
- No `git reset --hard`, `git clean`, blanket checkout/restore, recursive source
  deletion or in-place modification of immutable releases. Review exact file
  diffs. Roll back only this task's edits; do not overwrite intervening work with
  the saved baseline. Resolve any overlap against the current bytes.
- First extend the shared owner without changing existing callers, then add
  authenticated distribution support, then a few learner hooks. Verify each
  boundary before broadening instrumentation. Remove a hook only by a deliberate
  source edit/new candidate, never by patching a running or retained release.
- Keep candidate output/state isolated. Compare against equivalent pre-logging
  source and inputs, not a different learner algorithm. Do not mix logging and
  concurrent inference experiments into one unexplained semantic comparison.

This assignment plans these safeguards; it does not execute the refactor or
create candidate distributions. Propose any concrete prerequisite, not a blanket
freeze on other teams' work.

## Plan document structure

Use these sections in `docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md`:

**A. Current-state findings:** actual owners, call paths and discrepancies from
the supplied orientation, with source references.

**B. Minimal architecture:** shared owner → learner adapter → application hooks;
loader/release distribution boundary. Identify the exact proposed edit set.

**C. API:** concrete signatures/pseudocode, real-code identity, call correlation,
optional count semantics and throttling. No registry/taxonomy/general tracing.

**D. Release integration:** source mapping, identity/authentication, invocation
configuration transport, old-release handling, receipts and terminal semantics.

**E. Initial instrumentation map:** for each file/function, why useful, entry/
return hooks, existing completed count, existing total, bare-checkpoint suitability,
and additional computation (normally none). Explicitly list opportunities left alone.

**F. Diagnostics extension:** show how a developer adds local bare checkpoints
and builds a new immutable candidate without global tracing configuration changes.

**G. Verification:** bounded genuine learner execution showing all event kinds,
optional counted forms, truthful final counts, retained source identity, separate
files, suppression, authentic release closure and unchanged contracts/assignments.
Check watcher/handler logging behavior without live restarts. Measure realistic
overhead on equivalent genuine inputs; no invented performance threshold or
full-corpus rebuild. State how removing optional checkpoints leaves semantics
unchanged. Respect the owner's ban on resurrecting synthetic/fault-injection
logging suites; unavailable genuine cases stay unverified. The existing static
logging checker alone does not prove retained learner integration.

**H. Implementation sequence and preservation:** short dependency order, exact
source-preservation/rollback approach, proposed implementer and receiving owner,
candidate verification boundary and separately authorized activation.

**I. Blocking questions:** only concrete unresolved issues preventing safe
implementation. Resolve ordinary API preferences from this design/source; do not
present speculative features or optional preferences as blockers.

## Completion

Deliver the plan, summarize the proposed minimal change and genuine blockers,
then stop. Do not begin implementation, update another team's executable prompt
or silently turn proposed sequencing into an approved task assignment.
