# Transfer prompt — CK3Chronicle advisor for Task 07 onward

Prepared 2026-09-28. Give this entire document to the new advisory task.

## Your assignment

Act as my technical advisor and task-planning partner for the remaining
CK3Chronicle work, starting with Task 07. I use separate implementation tasks and
teams. Help me understand decisions, review their deliveries, keep scope coherent,
and write precise prompts for the next work. Do not interpret this handover as an
instruction to execute Task 07 or the later drafts.

- Inspect code and handoffs before advising what is missing or needs rebuilding.
- Distinguish owner requirements, delivered behavior, proposals, verified results
  and unresolved choices. Existing code and old tests do not establish requirements.
- Revise prompts and planning documents when requested; explain material changes
  and rationale outside the executable prompt.
- Give exact deliverables and acceptance bullets. Prefer short answers; expand
  only when the decision needs it. Avoid repeated background and defensive prose.
- Keep the command set small. One operation should use arguments to vary inputs.
- Recommend sequencing, consolidation or removal of obsolete tasks. Do not preserve
  a task just because its number exists in the original sequence.
- Carry relevant learner findings forward even when they do not block the pipeline.
  Learner implementation belongs to the learner team; watcher integration belongs
  to the watcher team.
- Escalate concerns that proposed changes would break functionality still needed,
  naming the behavior and a concrete resolution. Do not silently add compatibility.

## Checkout and reading discipline

Checkout: `C:/Users/nateb/Documents/ck3chronicle`.
All relative links below resolve from this document's `docs/` directory.

1. Read [AGENTS.md](../AGENTS.md), [development environment](DEVELOPMENT_ENVIRONMENT.md)
   and [banned ideas](BANNED_IDEAS.md).
2. Read the opening current sections of [status](PROJECT_STATUS.md),
   [plan](PROJECT_PLAN.md) and [current handoff](CURRENT_HANDOFF.md). These files
   contain substantial historical material; later sections often contradict the
   latest decisions. They had not been updated by the 07C team at this transfer.
3. Read [owner intent](OWNER_PRODUCT_INTENT.md), the
   [Error Contract](ERROR_CONTRACT_SPECIFICATION.md), and the architecture's
   [review-shard definition](ARCHITECTURE_AND_DATA_LINEAGE.md#native-review-shard).
   Use current owner direction below when historical wording conflicts.
4. Read the focused delivery references in the following sections. Consult older
   task prompts only when evaluating their actual remaining scope.

The checkout contains extensive unrelated uncommitted work from several teams.
Preserve it. The watcher was separately activated by the owner; its recorded PID
is historical, not proof of its present state. Advisory work does not authorize
restarting it, changing selection, processing production captures, resetting a
database, expiring retained files, committing or pushing. Ordinary read-only
inspection and document preparation are appropriate.

## What already works

| Boundary | Delivered behavior and reference |
|---|---|
| Shared runtime matching | The selected immutable package contains parser, matcher and dependencies. Pipeline consumes selected assignments and original bindings. [Task 05](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md), [matcher API](SHARED_MATCHER_API.md). |
| Error-log-to-SQL path | Classification, contract preparation, exact aggregation, SQL writes, native review and SQL-only rendering were exercised end to end. [Task 06 storage APIs](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md), [v45 integration](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md). |
| Reusable orchestration | Task 06 provides `store_validated_log`; `.codex-tmp/task06-v45/verify.py` exercised the product APIs. At this inspection there is no normal product ingest entry point or main CLI ingest command. Expose the existing sequence; do not build another engine or copy verification assertions as requirements. |
| Watcher capture/playset | The watcher protects paired error/debug logs and produces ordered `playset.json`. [Producer handoff](WATCHER_ACTIVE_PLAYSET_HANDOFF.md). Capture remains owned by `harvester.py`; extraction by root `playset.py`. |
| Deprecated-code cleanup | 06B removed the old processing/semantic/provider stack and unused CLI paths. [Cleanup handoff](TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md). Its portable archive contains originals, PowerShell cleanup/rollback scripts and a README. Preserve it. |
| Versioned releases | 07C delivered retained executable learner releases, model-package catalogs, explicit selection and installed resources. See the next section. |

Task 06/v45 reports seven complete logs, 418,168 recovered occurrences, 19,912
unique SQL records and four review emissions. These are reported verification
results, not targets for future output or proof of live product acceptance.

The root CLI retained `watch`, `capture`, `doctor`, `observe-logging`, including
`watch --once`, after 06B. The deleted `process-pending` command is not an existing
ingest facility. 07C adds separate release-management entry points; do not confuse
those with product ingestion. Recheck the checkout before claiming current command
availability or end-to-end operation.

## New delivery: Task 07C

Read both in full:

- [TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md](TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md)
- [RELEASES.md](RELEASES.md)

For motivation/history only, use the [07B version-boundary audit handoff](TASK07B_LEARNER_DEPENDENCY_VERSIONING_HANDOFF.md).

Carry these facts into advice and Task 07 revisions:

- Default selection remains package `68f1ae5db205ab46afef9c4d`, model
  `f5cde2616f35d563118d3d32`, selected by `models/selection.json` from its existing
  `models/candidates/` path. 07C did not publish or activate a new production model.
- The selected package manifest pin is
  `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
  Model format 5, matcher API v2, parser `ck3-lossless-v1.7`, selector
  `complete-assignment-v2`; Error Contract v1 and SQL schema 1 at this inspection.
- `learners/catalog.json` and `learners/releases/<release_id>/` retain learner
  execution distributions. `models/catalog.json` and `models/releases/<package_id>/`
  retain runtime packages. Authoring remains in `tools/template_learning/`.
- Complete new learner distribution:
  `cdbd72475baf238d5a44a7ef37c2a266a71179d780dbaf71aa35d5a91b3d5a0f`.
  Its algorithm label is still v45; a label is not an exact executable identity.
- `catalog.load_selected_classifier(package_id=...)` and
  `load_selected_package(package_id=...)` now accept explicit package selection.
  `selection_path` is an alternative, mutually exclusive argument. Omitting both
  preserves the default. `package_selection(package_id)` does not activate it.
- Select by package ID, not model ID alone: the same model can be packaged with
  different executable components. Obtain actual Run lineage through
  `contracts.run_lineage(package, application_revision=...)`.
- Existing Run lineage already names package/manifest, model, parser, matcher API,
  selector, classifier, application and contract. Ingest requires no new learner
  imports or ingestion-side learner ID. New publications retain learner-release
  provenance for offline use. Earlier advisory text calling missing learner ID an
  ingestion dependency must be reconciled with this delivered boundary.
- Two production packages are usable: `44a0401b8adf0a2953d26705` and the current
  `68f1ae5db205ab46afef9c4d`. 07C reports source/installed classifier and contract
  checks on two genuine logs. It did not verify every historical version or all
  native branches; consult its stated limits.
- Some historical learners support evaluation only; others/packages are explicitly
  unavailable. Their recovery is not a Task 07 dependency. Do not supply today's
  code as a substitute or commission recovery merely because a catalog lists a gap.
- Release policy retains at least the latest ten production learner versions and
  ten distinct production models with executable packages. No release pruning was
  implemented or authorized by 07C. This is separate from raw-log retention.

This advisory transfer inspected the documentation, selection and catalog source;
it did not independently rerun the 07C verification campaign. Treat its test claims
as reported evidence until any specifically needed receiving check is performed.

## Owner decisions to preserve

### Diagnostic records and matching

- Pipeline uses the pinned parser/model/matcher and its winning assignment. No
  additional semantic taxonomy, reinterpretation, classification or regrouping.
  Exact aggregation under the approved Error Contract is already authorized.
- A diagnostic record is the refined stored unique message, not a raw parser unit.
- Equal message content under the approved template/literal/binding identity
  becomes one record with an occurrence count. Variable values create distinct
  records. Do not restore per-repeat timestamps or occurrence history tables.
- Store source/emitter, literals/layouts, typed bindings and placements. Template
  versus provisional is a filterable SQL field; both are accepted record outcomes.
- Unassigned/unresolved evidence belongs in native review. Error type may remain
  `unknown`; typing/taxonomy is not an ingestion dependency. Do not store losing
  candidates in SQL or invent another matching pass.
- Each successful Run has one two-part shard: native review log plus manifest.
  Zero review emissions still have metadata. Avoid the misleading term “empty shard.”
- Reports use stored SQL definitions and values. SQL renders diagnostics and counts;
  it cannot reconstruct every original log timestamp and ordering after aggregation.

### Database policy

- Compatible processing revisions add new Runs to the same database. Each Run
  records its exact component combination. Remove the existing database-wide
  lineage equality restriction; preserve per-Run definition correctness.
- Playset tables require a new, explicitly versioned SQL schema. Schema changes
  use explicit reset. No migrations, legacy fallbacks or backward compatibility.
  An incompatible open must not silently delete the database.
- The owner rejected generation replay. Do not include a discussion or deletion
  assignment for nonexistent replay code. Re-ingesting after an owner-chosen reset
  uses ordinary ingest, not another command/workflow.
- Per-Run replacement by matching source hash was floated, not commissioned.
  Ordinary duplicates return the existing Run ID without overwriting it.
- Run IDs are automatically generated; exact full-log hashes identify duplicate
  inputs. Task 06 already owns ID allocation; do not redesign it casually.

### Playset, capture and retention

- Missing playset data must never block otherwise valid ingestion. Store unavailable
  state (`playset_captured=false`), not an assertion that the game was unmodded.
- Consume the watcher's ordered artifact; do not repeat extraction or look up
  today's descriptors. Preserve delivered fields, nulls, repeats and pair provenance.
- Original error/debug logs stay where the watcher put them. Processing creates
  no additional archive copies. Initial raw-log retention is configurable, one month.
- Raw expiry is separate from SQL history, playset rows and native review shards.
  Retain small capture metadata/playset JSON under the current Task 07 proposal.
- Watcher is the ongoing process. The watcher team triggers ingest after completed
  capture publication and periodic retention checks even when no ingestion occurs.
  Task 07 supplies APIs and the handoff; it does not modify or activate the watcher.

### Scope and verification

- Learner work is separate from pipeline implementation; there is no separate
  parser team. Pinned parser/matcher artifacts are delivered by the learner team.
- Use real complete native logs for pipeline verification. No synthetic messages,
  fabricated records, modified artifacts or tests used as requirement sources.
  A delivery's historical test methodology does not grant fresh authorization.
- Reuse owning components. Do not expand ordinary checks into provenance ceremonies,
  new queues, recovery frameworks or hypothetical safety gates.
- Every implementation task needs a durable handoff and current status updates.
  Keep owner-review rationale outside the executable prompt.

## Remaining work and sequencing

| Work | Advisor's next responsibility |
|---|---|
| Task 07 | Review the [current prompt](TASK07_PROMPT.md) against 07C. Its substantive additions are playset storage/new schema, per-Run version correction and retention; expose the already tested ingest sequence with minimal API/CLI glue. Keep the prompt brief. |
| Watcher integration | After Task 07 delivers signatures/configuration, prepare or review the watcher-team assignment for ingest and periodic retention triggers. No second resident scheduler. Confirm which team proves the automatic end-to-end path. |
| Task 08 | Revise toward SQL-only reports/read operations and bounded audit using delivered APIs. Use the fewest logical commands and arguments. Do not rebuild ingestion or require raw logs/model imports for ordinary reports. |
| Task 09 | Reassess entirely after 06B and 07C. Old learner-reconnection and deletion assumptions are unreliable. Any remaining learner operation must have an owner need and the learner team as owner. |
| Tasks 10–11 | Reassess remaining application wiring/retirement. Much cleanup already happened in 06B. Inventory actual remaining work; do not repeat removal lists or recreate missing providers. |
| Task 12 | Reconcile documentation to delivered behavior. Earlier tasks still update their own handoffs. Keep current guidance short and move obsolete history out of mandatory reading without losing useful evidence. |
| Final acceptance | Identify the remaining end-to-end acceptance assignment after wiring. Separate disposable native-log verification from owner-authorized live activation. Do not claim completed Trusted Run from library checks alone. |

Original draft prompts 08–12 are in:

`C:/Users/nateb/Documents/WIP/CK3Chronicle_Classification_Replacement_Prompts_2026-09-14 (1)/AGENT_PROMPTS/`

- `08_REPORTS_AUDIT_AND_COMMAND_HANDLERS.md`
- `09_OFFLINE_LEARNER_RECONNECTION.md`
- `10_CUTOVER_AND_RETIREMENT_MANIFEST.md`
- `11_APPLICATION_CUTOVER_AND_RETIREMENT.md`
- `12_CURRENT_DOCUMENTATION_RECONCILIATION.md`

That folder also contains the original ZIP. The repository Task 07 supersedes its
old Task 07. [Remaining-task review](REMAINING_TASK_PROMPTS_REVIEW.md) is useful
historical context, but predates 06B, the database-policy correction and 07C.
Its replay, old-provider and offline-tool recommendations are not current authority.
No later draft is ready to execute just because it exists.

## Resolved investigation and genuinely open choices

**Script location stack investigation is complete**, not awaiting assignment:

- [Results](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_RESULTS.md),
  [original investigation prompt](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_PROMPT.md).
- It reports zero demonstrated stack-length misses and zero lost location fields
  across 1,174,361 Script location diagnostics in 73 retained logs, with stacks up
  to 55 entries. This is in-corpus evidence, not proof about all future logs.
- Recommendation: retain current representation. Repeated-frame representation is
  a possible future model/API change; it is not approved or a Task 07 prerequisite.
- The investigation corrected the starting inventory description: the 73-log list
  is `.codex-tmp/learner-release-v45/inputs-all.json`; the date-key list has two logs.

Open choices, unless the owner or newer work has since settled them:

- Do raw logs from unprocessed/failed captures expire too? Previous advisor proposed
  processed/duplicate-only expiry initially; the owner has not selected that rule.
- Is one month 30 days? That is a proposal, not a confirmed convention.
- Retention check interval: watcher ownership is decided; exact cadence is not.
- Malformed/mismatched completed playset disposition: distinguish this from missing
  playset, which is already expressly allowed. Obtain a concrete recommendation.
- Startup/backlog/retry behavior at the watcher/API boundary needs a minimal,
  explicit handoff; do not invent a framework before establishing actual need.
- Historical release recovery and specialized offline operations listed by 07C
  are conditional future work, not pipeline blockers.

## Your first response and continuing practice

1. Read the focused current references and check whether new implementation/handoffs
   appeared after this transfer. Do not infer Task 07 completion from planning text.
2. Give me a concise assessment of what 07C changes for Task 07, what is already
   delivered, and the remaining work/decisions with team ownership.
3. Flag necessary Task 07 prompt corrections, especially its older learner-provenance
   wording. Make bounded document corrections when justified; no runtime work.
4. Recommend the next executable task and sequencing. Ask only for material unresolved
   decisions, rather than reopening settled requirements.
5. As I bring completion reports, review evidence proportionately, update a compact
   current decision/task ledger and prepare the next prompt. Clearly distinguish
   documentation review, source inspection and checks you actually ran.

I need continuity of advice and steering, not another implementation effort or a
retelling of every historical change. Keep the decisions and deliverables concrete.
