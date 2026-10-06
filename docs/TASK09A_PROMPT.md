# Task 09A — Learner-led plan for project-wide canonical logging

**Lead: Learner. Deliverable: an implementation plan, not code.**

Plan logging implementation throughout CK3Chronicle.

Assess Learner, Pipeline, Watcher, Data Intelligence/Reporting and application entry points; a learner-first slice is a possible sequence, not the final scope. **“Cover” means assess current coverage and state the required disposition for each component. That disposition may be no logging change where existing coverage already satisfies Canonical Logging System v1.**

Each component retains its implementation/receiving owner under [team governance](team-governance/README.md). Pipeline owns application packaging and integrated receiving.

## Objective

Inspect the current checkout and produce a concrete, minimal plan for [Canonical Logging System v1](CANONICAL_LOGGING_SYSTEM_V1.md), the owner-approved architectural direction.

Logging observes real executable code and caller-owned counts; it must not invent phases, stages, semantic checkpoints or a workflow model.

The reference's snippets are labelled **illustrative**, with existing symbols and call signatures checked against source. `journal` and the checkpoint/call-lifecycle behaviours are proposed API concepts. Any token, context-manager or similar mechanism shown in the reference is illustrative; the plan should choose the smallest mechanism actually required by current call patterns. Final code must use actual CK3Chronicle symbol definitions and contracts; new API elements must be defined rather than assumed to exist.

The corrected source observations below are the starting point; inspect later changes before choosing implementation locations.

Do not implement, create a learner candidate, run a training campaign, publish, change production selection, restart services, commit or push.

Produce only:

```text
docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md
```

and a concise completion response.

Do not draft a document claiming that implementation or verification has occurred.

## Read and inspect

Checkout:

```text
C:/Users/nateb/Documents/ck3chronicle
```

Read root and learner `AGENTS.md`, the development environment, and opening current plan/status/handoff sections.

Read the canonical reference, `RELEASES.md`, `TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md`, `TASK07E_RUNTIME_LOGGING_HANDOFF.md` and the current learner delivery/experiment guidance.

Historical recipes do not override current instructions. Do not read rejected database-handler designs.

Inspect at least:

- `src/ck3chronicle/runtime_logging.py`
- `tools/template_learning/learner_loader.py`
- `tools/template_learning/learn_error_templates.py`
- `tools/template_learning/incremental_template_registry.py`
- `tools/template_learning/records.py`
- `tools/template_learning/clustering.py`
- `tools/template_learning/patterns.py`
- `tools/template_learning/artifacts.py`

Follow actual callers where needed, including release/reference verification and publication.

Inspect existing watcher/handler logger consumers enough to name the behaviour that must remain intact.

Also inspect Pipeline request/preparation/storage paths, Watcher capture/lifecycle/triggers, Reporting queries/source search/exports and CLI entry points for meaningful logging coverage.

Coordinate only the **logging/configuration interface boundary** with proposed [Task 10](TASK10_PROMPT.md): identify what Task 10 must consume, preserve or provide. Do not redesign or implement Task 10, and do not block the logging plan on work that can instead be expressed as a clear interface dependency.

Plan logging changes in existing components; no unrelated runtime rewrite.

The shared working tree includes unrelated and in-progress learner changes. Use current source, not an assumed v45/v46 baseline or a stale release label. Source inspection for this plan is read-only.

**As of preparation of this assignment**, the released baseline was learner v61 / parser v1.8 / package `4ac4e8ee92346e6d14eacfbf`. Reconfirm the current released identity from [learner-next-release/PIPELINE_RECEIVING.md](learner-next-release/PIPELINE_RECEIVING.md) and other current release evidence before relying on it. The identity stated here is orientation, not authority.

Use the current release receipt for exact application identity and completed production work.

Revalidate the October 3 observations below against actual working source. Do not alter retained releases or repeat the completed corpus build, cutover or historical ingestion to plan logging.

## Required design decisions

Show the minimum files and edits, concrete signatures/pseudocode and ownership:

1. **Shared logging owner.** Keep `runtime_logging.py` the sole editable backend/formatter/rotation/defaults owner. Determine the smallest explicit-destination/settings extension and config-import change needed for a retained learner without mutable application configuration. Preserve current watcher/handler callers and destinations.

2. **Small adapter API.** Specify a small adapter API for call entry/return and checkpoints. Illustrative checkpoint forms are:

   ```python
   journal.checkpoint()
   journal.checkpoint(done)
   journal.checkpoint(done, total)
   ```

   Derive actual module/qualified function/source/line from frames or functions. Resolve helper frames and `runpy`/`__main__` identity using existing execution context, without a symbol registry, AST/bytecode lookahead or retained frame/local references.

   Do not assume a separate call token is required. If entry/return timing or correlation requires a token, context manager or other small mechanism, justify and define the minimum mechanism from actual call patterns.

3. **Checkpoint and throttling semantics.** Define immediate bare checkpoints, counted first/periodic/final emission, monotonic elapsed time and the smallest throttling state. Recommend one simple centrally owned interval.

   Address nested/repeated/recursive calls and distinct invocations using actual needs, not a generalized tracing design.

   Guard the completed-total case explicitly; omitted counts are not a completed total.

4. **Immutable distribution.** Show one source-to-release-payload mapping for shared-owner and adapter bytes. Inspect all `FILES`/hash/copy assumptions. Cover authentication, implementation/release identity, executable audit, publication/reference checks and receipts.

   No editable duplicate owner or ambient import fallback.

5. **Invocation configuration.** Trace `run --log-dir` from outer argument parsing through `launch` and retained `execute`: path resolution, invocation ID, filename, retained configuration, stderr path announcement and unsupported-old-release handling.

   Preserve stdout and operation arguments.

   Recommend an explicit default without application config in the worker.

   Explain how provenance remains usable with rotation.

6. **Invocation lifecycle.** Locate invocation start/finish relative to authentication, retained imports, operation dispatch, receipt write and cleanup.

   Preserve actual success, nonzero `SystemExit`, `KeyboardInterrupt`, exceptions and subprocess results.

   Do not claim a normal call return on exception, double-log exceptions, mask an original error with cleanup, or infer outcomes after abrupt termination.

7. **Initial instrumentation.** Select only significant actual functions worth instrumenting now.

   Counts originate in local application state at a completed-work boundary.

   No scans, extra hashes, inference, model inspection, lazy properties or diagnostic-body serialization for journal fields.

   No algorithm rewrite to expose progress.

8. **Project-wide disposition.** Name current hooks/events/console outputs to retain, replace or leave alone.

   Preserve useful runtime evidence, request correlation and operator behaviour through deliberate conversion.

   Account for every component in the project-wide plan with one of:

   - required logging edits;
   - already-sufficient coverage / no logging change;
   - a concrete dependency before a decision can be made; or
   - an explicitly deferred delivery justified by implementation order.

   Staging the implementation must not silently defer all non-Learner work.

   Project-wide coverage does not mean tracing every function or changing algorithms.

## Source observations to revalidate

These observations were checked on 2026-10-03. Use current code to confirm or correct them when selecting implementation locations.

- `collect_records` owns a sequence of logs. A completed-input checkpoint belongs after processing an input, not before `read_evidence`. Do not rewrite the parser to expose internal progress.

- `sync_registry` has `paths_seen`, `paths_hashed` and other existing counters. In the inspected code, `paths_seen` increments at loop entry; it is not evidence of completed processing at that location. A checkpoint using it belongs after that path's processing succeeds.

  `candidate_paths` returns a list, not a generator; the earlier addendum's generator description was incorrect. Do not call it again to obtain a logging total.

- `combine_training_records` loads existing entries; `build_revision` calls it, `artifacts.build_model` and `artifacts.write_bundle`. Prefer these real owners to invented stage labels, with the fewest useful hooks.

- `choose_medoid` uses an expensive `max`/generator expression. Entry/return may be sufficient; do not expand it into nested loops for logging counts.

- `derive_pattern` is defined in **`patterns.py`**, imported by clustering. It has materialized `units` and an outer mapping loop. Log the defining symbol/source, not a guessed `clustering.derive_pattern` location. Assess whether hooks here would flood journals across many calls; do not instrument every inner block.

- In `refine_region_groups`, `len(seen)` counts encountered pair identities and `len(ordered)` counts groups. They are not a completed/total pair.

  `seen.add(key)` precedes the pair's remaining checks/inference, so that location cannot report completed pair processing either.

  Preserve console behaviour unless separately commissioned to change it; journal throttling need not inherit its modulo-100 cadence.

- Recent learner experiments may change this inventory during planning. Document discrepancies and use actual current source. Do not undo another team's changes to make an illustrative example fit.

## Safe refactor plan required for subsequent implementation

Propose small, reversible edits, not replacement of source trees.

Include:

- A bounded baseline of exact affected working files and their dependency closure, including tracked, untracked and relevant ignored source/resources. Git HEAD, a clean-looking diff or the Markdown source export alone is insufficient.

- A verified recoverable copy of those actual working bytes before edits, in a new task-owned ignored location, with relative paths/hashes and relevant prior absence recorded for new files.

  These are refactor safeguards, not extra runtime journal hashing or a new backup framework.

  Preserve the existing 06B archive.

- Coordinate ownership of overlapping learner/shared-logger files before editing.

  An isolated checkout must contain the required current uncommitted source; branching from HEAD does not automatically provide it.

  Do not move another team's workspace or interrupt its process to achieve isolation.

- No `git reset --hard`, `git clean`, blanket checkout/restore, recursive source deletion or in-place modification of immutable releases.

  Review exact file diffs.

  Roll back only this task's edits; do not overwrite intervening work with the saved baseline.

  Resolve any overlap against the current bytes.

- First extend the shared owner without changing existing callers, then add authenticated distribution support and useful component hooks in the proposed dependency order.

  Keep subsequent component deliveries explicit until received.

  Verify each boundary before broadening instrumentation.

  Remove a hook only by a deliberate source edit/new candidate, never by patching a running or retained release.

- Keep candidate output/state isolated.

  Compare against equivalent pre-logging source and inputs, not a different learner algorithm.

  Do not mix logging and concurrent inference experiments into one unexplained semantic comparison.

This assignment plans these safeguards; it does not execute the refactor or create candidate distributions.

Propose any concrete prerequisite, not a blanket freeze on other teams' work.

## Plan document structure

Use these sections in:

```text
docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md
```

### A. Current-state findings

Actual owners, call paths and discrepancies from the supplied orientation, with source references.

### B. Minimal architecture

Shared owner → necessary component adapters → application hooks; loader/release distribution boundary.

Identify the exact proposed edit set.

Identify the specific logging/configuration seam Task 10 must consume or preserve without redesigning Task 10.

### C. API

Concrete signatures/pseudocode, real-code identity, call correlation, optional count semantics and throttling.

No registry/taxonomy/general tracing.

Choose the smallest actual mechanism for call timing/correlation; do not assume a call token is required.

### D. Release integration

Source mapping, identity/authentication, invocation configuration transport, old-release handling, receipts and terminal semantics.

### E. Project-wide instrumentation map

For each component and selected file/function, state:

- why it is useful;
- whether entry/return hooks are needed;
- whether an existing completed count exists;
- whether an existing total exists;
- whether bare-checkpoint suitability exists;
- additional computation required for logging, normally none; and
- the component disposition: change, already sufficient/no change, concrete dependency, or explicit sequenced delivery.

Identify the first implementation slice and remaining deliveries.

Explicitly justify existing coverage left alone.

### F. Diagnostics extension

Show how a developer adds local bare checkpoints and builds a new immutable candidate without global tracing configuration changes.

### G. Verification

Plan bounded genuine execution by each affected component, reusing applicable evidence.

Include learner execution showing all event kinds, optional counted forms, truthful final counts, retained source identity, separate files, suppression, authentic release closure and unchanged contracts/assignments.

Check watcher/handler logging behaviour without live restarts.

Measure realistic overhead on equivalent genuine inputs; no invented performance threshold or full-corpus rebuild.

State how removing optional checkpoints leaves semantics unchanged.

Respect the owner's ban on resurrecting synthetic/fault-injection logging suites; creation or execution of each synthetic test requires explicit owner approval for that specific test.

Unavailable genuine cases stay unverified.

The existing static logging checker alone does not prove retained learner integration.

### H. Implementation sequence and preservation

Short dependency order, exact source-preservation/rollback approach, implementer and receiving owner for each component delivery, candidate verification boundary and separately authorized activation.

Distinguish a completed first slice from completed project-wide adoption.

### I. Blocking questions

Only concrete unresolved issues preventing safe implementation.

Resolve ordinary API preferences from this design/source; do not present speculative features or optional preferences as blockers.

## Completion

Deliver the plan, summarize the proposed minimal change and genuine blockers, then stop.

The following 09B assignment may turn the plan **and subsequent owner scope decisions** into team-owned implementation deliverables.

Completion of 09A does not authorize 09B, implementation, tracker enrollment or any proposed work from the plan.

Do not begin implementation, update another team's executable prompt or treat proposed sequencing as authorization.
