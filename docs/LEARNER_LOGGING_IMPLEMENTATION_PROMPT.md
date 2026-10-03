# Learner operational logging â€” implementation prompt

## Objective and boundaries

**Superseded 2026-10-03; do not launch this phase-based implementation prompt.**
The owner supplied [Canonical Logging System v1](CANONICAL_LOGGING_SYSTEM_V1.md).
[Task 09A](TASK09A_PROMPT.md) now prepares its implementation plan and stops before
code changes. The text below is retained as historical context, not current
implementation authority. Final implementation assignment remains for owner review.

Implement lightweight learner logging as specified in
[LEARNER_LOGGING_PROPOSAL.md](LEARNER_LOGGING_PROPOSAL.md). Operators must be able
to see the selected release, current/last phase, completed work, elapsed time,
and observed completion or failure in a rotating JSONL log per invocation.

Reuse the existing logging owner. Do not change learning/matching behavior or
build monitoring, heartbeat threads, watchdogs, status storage, automatic
restarts/timeouts, or hang detection. Production publication and activation
are outside this assignment.

## Orientation

Read the root and learner `AGENTS.md`, the development environment, and the
opening current sections of the plan, status and handoff. Then read:

- [Logging proposal](LEARNER_LOGGING_PROPOSAL.md) for event names, fields and instrumentation scope.
- [Runtime logging handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md) for the shared owner.
- [Releases](RELEASES.md) for immutable execution and provenance.
- [Learner rules](LEARNER_INFERENCE_RULES.md) and [native contract](LEARNER_NATIVE_MODEL_CONTRACT.md).
- [Current v46 delivery](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md): preserve its approved discovery and batched consolidation changes.

Inspect current source before editing. Preserve unrelated work, source logs,
production data, catalogs/selection, retained releases and running processes.
Current owner requirements supersede historical verification recipes.

## Implementation

1. **Shared owner.** Extend `src/ck3chronicle/runtime_logging.py` to accept an
   explicit learner destination and settings without application configuration.
   Move the config import into the config-reading function. Keep defaults,
   paths, formatting, handlers and rotation owned here; preserve watcher/handler
   calls and destinations. Do not copy an editable logging implementation into
   the learner tree.

2. **Immutable distribution.** Update `learner_loader.py` to retain the exact
   shared-owner bytes as a private module, such as
   `template_learning/_runtime_logging.py`, alongside a learner progress adapter.
   Use one source-to-payload mapping for release creation and implementation
   identity. Update affected closure/reference checks, including publication.
   Keep authenticated execution and rejection of ambient application imports or
   checkout fallbacks. Older releases continue using their own launchers without
   new logging arguments; an explicit unsupported `--log-dir` must be rejected
   clearly, not ignored or passed to the learner operation.

3. **Invocation setup.** Add optional `run --log-dir`. Default to
   `<receipt-parent>/learner-logs`, or without a receipt to
   `<cwd>/.ck3chronicle/wip/learner-logs`. Resolve the directory before launch.
   Configure once inside the authenticated worker, before dispatch, with an
   independent invocation ID, `learner-<invocation-id>.jsonl` and existing rotation
   defaults. Print the absolute path once to stderr; preserve stdout and receipt
   interfaces. Bootstrap failures retain existing stderr diagnostics. Surface
   log-file setup failures before work; subsequent logging is best effort.

4. **Progress.** Add a small learner-owned adapter that delegates to the shared
   logger. Implement the proposal's event/field contract, monotonic durations
   and nested phase-context restoration. Emit boundaries immediately and
   intermediate INFO progress at most every ten seconds per active phase, at
   existing loop boundaries. Record completed units and already-known totals.
   Do not add scans, hashing, inference, lazy pattern/ID evaluation or diagnostic
   bodies for logging. No per-record/per-pair INFO events or guessed ETA. A long
   individual call may remain silent until it returns.

5. **Instrumentation.** Cover inventory/parsing, registry feature loading and
   combination, source learning/refinement/consolidation, evaluation and artifact
   writing. Inspect `records.py`, `learn_error_templates.py`,
   `incremental_template_registry.py`, `artifacts.py`, `clustering.py` and the
   actual evaluation/serialization owners. Place shared hooks where fresh
   learning and registry builds both use them. Instrument the current batched
   duplicate-ID consolidation and its expensive calls without changing their
   algorithm. Preserve existing console output.

6. **Outcomes.** Emit one operation terminal event on an observed outcome.
   Preserve `SystemExit` success/nonzero semantics and `KeyboardInterrupt`
   behavior. Log an actual exception once at the operation boundary with its
   traceback and failing phase, then preserve it. Cleanup/logging errors must
   not replace the original exception. Preserve receipt provenance and report
   receipt-writing failures honestly. Abrupt termination may leave no terminal
   event or receipt; do not infer an outcome from that absence.

## Verification

Use the repository venv with `-B`, genuine CK3 evidence, fresh state and an
immutable candidate release under ignored research output. Do not restore
removed synthetic or fault-injection logging tests.

- Verify manifest hashes, learner identity and receipt evidence for the retained
  logger/adapter; confirm execution uses authenticated code rather than mutable
  application imports.
- Exercise retained fresh learning and registry sync/build on a bounded genuine
  corpus, including consolidation. Inspect JSONL validity, release/invocation
  context, phase boundaries, completed-work counts, durations, terminal events
  and separate invocation files.
- Compare learned contracts and selected assignments against the same learner
  implementation before logging changes, on the same inputs. Preserve the new
  v46 behavior; the production v45 package is not an equivalent baseline.
  Explain legitimate release/provenance hash differences. Logging fields must
  not affect inference or semantic model content.
- Run `tools/check_runtime_logging.py` and inspect learner integration separately:
  the checker currently covers product source only. Confirm no duplicate
  formatter/handler and unchanged watcher/handler calls and destinations without
  restarting services. Run relevant existing release checks consistent with
  current owner rules.

Report corpus scope, timings and unverified cases. Do not manufacture missing
rotation/failure/progress evidence or expand into an all-logs build to obtain it.
Keep generated releases, logs, receipts and results ignored. Do not publish a
production release or model.

## Delivery

Write `docs/LEARNER_LOGGING_IMPLEMENTATION_HANDOFF.md` and update the current
status/handoff. Include changed files, instrumented phases, logging usage, a
working candidate-release command and manifest pin, verification results and
limitations. Show how to inspect recent events and interpret an unfinished log.

State clearly that source edits do not add logging to existing retained releases
or running learners. Production activation remains a separate assignment.
