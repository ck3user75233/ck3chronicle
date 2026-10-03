# Task 08 and Task 09 — scope proposal

2026-09-30 current direction: 07D hardening and 07E logging are delivered.
Reporting is now split into [08A capabilities](TASK08A_PROMPT.md) and
[08B reports/CLI](TASK08B_PROMPT.md), both owned by Reporting and Analysis.
Audit is excluded. See [current decisions](TASK08_SCOPE_REVIEW.md).
The recommendation to retire the original Task 09 draft remains; the Task 08
scope/sequencing below is historical and must not override the new prompts.

2026-09-29. Advisory proposal, not executable instructions or owner approval of
new commands. Reviewed the original 08/09 drafts in the owner's WIP prompt folder,
current repository/CLI and learner release entry points, and 06B/07C handoffs.
No rejected handler design was opened. No runtime checks or mutations were needed.

## Recommendation

Keep Task 08, rewritten as complete SQL-only reports and bounded database audit
over the implemented 07D request interface. Retire the original Task 09 offline
reconnection/deletion assignment. It is neither a pipeline prerequisite nor safe
to execute against the current release boundary.

Recommended order: finish 07D and receive its actual APIs; implement and wire
Task 08; then review remaining Trusted Run acceptance/wiring work. Run-result
replacement remains desired but separately unassigned. It can receive its own
new prompt after the request/storage boundary is stable; do not inherit old Task
09 scope merely to reuse its number.

## Task 08 proposed deliverables

1. Run listing and a selected-Run report, including available capture/lifecycle
   facts, actual processing lineage, occurrence and unique-record counts, ordered
   playset or explicit unavailable state, and stored review references/counts.
2. Diagnostic output rendered from stored definitions/bindings with occurrence
   count, template/provisional status and source/emitter. Both statuses by default;
   filters use current supported fields. No new error taxonomy or classification.
3. A bounded SQL audit of stored Run/diagnostic/definition/playset/review-metadata
   relationships and counts that can be reconciled from those stored facts. It
   reports findings; it does not repair, migrate, rehash raw logs, inspect model
   packages, sweep external shards or prove every original emission from SQL.
4. Human-readable and JSON output, integrated into the existing root CLI and
   usable immediately through the delivered 07D handler. A durable handoff and
   current documentation updates belong to this task.

Proposed small command surface, subject to owner review:

```text
runs --database FILE [pagination]
report --database FILE --run ID|latest [--view summary|errors|playset|review] [filters] [--format text|json]
audit-db --database FILE [--run ID]
```

Use arguments for views/selectors rather than separate latest/errors/review-queue
commands. The examples are a command proposal, not exact approved argument syntax.
No process-pending, rebuild-db, replacement or additional ingest command. Retain
the existing spelling `--database` and exact SQLite file selection.

## Task 08 implementation and acceptance boundary

Existing repository methods already provide `list_runs`, `latest_run`, `get_run`,
`read_diagnostics`, `read_playset` and `read_review_metadata`; `contracts.render`
already renders from SQL definitions/values. Reuse them through 07D's supported
requests. Add any demonstrably needed fixed audit/read operation in the owning
repository and handler; no caller SQLite connection or arbitrary SQL interface.
Formatting runs outside the database worker. Do not guess 07D signatures or create
a temporary bypass while its implementation is unfinished.

Verify against disposable databases populated from complete genuine native logs:
reported counts/filters and rendered values agree with stored facts; both statuses
and optional playset are represented; report operations do not mutate Run data;
raw logs and model resources are unnecessary for ordinary reads. Use genuinely
empty storage for the no-Runs case. Distinguish an empty successful query from
an unknown explicitly requested Run and from an actual failure. Report shard
availability as stored metadata, not a fresh filesystem check. Preparation may
proceed concurrently, but all report reads use 07D's runtime access boundary.

Remove old draft requirements to inspect nonexistent inputs/processor/replay/capture
modules, select a classifier for reports, recreate capture error handling, preserve
providers removed by 06B, or leave completed command handlers unregistered until a
later cutover. Do not impose a new artifact format, occurrence-history table or
database schema merely for presentation. Ordinary reports need no learner imports.

## Why retire the original Task 09

- Its L1 reconnection targets `pipeline.emissions.iter_emissions`; that owning
  module has been removed. The current learner/release path does not need it
  restored. Parser/matcher bytes belong to selected immutable releases.
- Its deletion list includes `build_review_pack.py` and
  `evaluate_unseen_session.py`. Current `learner_loader.FILES` retains both;
  `OPERATIONS['review']` uses `build_review_pack`, and candidate evaluation's
  entry point delegates to explicit retained-release execution. Deleting these
  authoring files would break the declared closure for new learner snapshots and
  remove current commands. Existing immutable snapshots must also stay untouched.
- Other deletion candidates are already absent, including
  `build_semantic_projection_catalog.py` and two named blind-review tools.
  Neither their absence nor survival of other research scripts creates work.
- 07C already delivered supported learning, registry, evaluation, publication
  and review routes. Historical releases with unavailable operations remain
  explicit limitations; recovering them is not a reporting/ingestion dependency.

Keep any remaining offline follow-up with the learner team, commissioned for a
specific owner-needed operation. Before proposing it, name the operation, its
current supported route or concrete gap, and the effect of the change. Do not
commission a general cleanup/reconnection audit or historical recovery campaign.

This review source-traced the relevant current callers; it did not rerun 07C's
learner/native/installed verification. Historical claims remain reported evidence.
