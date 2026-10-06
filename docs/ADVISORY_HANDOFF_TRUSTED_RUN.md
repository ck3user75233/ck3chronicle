# Transfer briefing — CK3Chronicle advisor: pathway to Trusted Run

Prepared 2026-10-03. Give this document to the new advisory conversation.
Relative links resolve from this repository's `docs/` directory.

## Your role and first assignment

Act as the owner's technical advisor and task-planning partner. Separate teams
implement the product. Help the owner understand choices, assess evidence, keep
scope coherent and prepare precise assignments. This briefing commissions advice
and document preparation, not implementation, operational changes or activation.

Your first assignment is to:

1. Review the intent and acceptance meaning of **Trusted Run** against current
   owner direction, delivered behavior and remaining evidence gaps.
2. Reassess the outgoing advisor's post-08B recommendations below. They are
   recommendations, not approved replacement tasks. Include the newly prepared
   09A canonical-logging planning prompt and decide its implementation sequencing.
3. Present a concrete pathway to Trusted Run completion: remaining deliverables,
   responsible teams, dependencies, acceptance evidence and material owner decisions.

Start with inspection, not a new task list inferred from historical task numbers.
Check whether 08B or other work has completed since this briefing. Do not equate
implemented, verified in disposable storage, activated, and milestone accepted.

## Working practice and authority

- Keep advice concise; expand where the owner must make a substantive choice.
- Distinguish owner requirements, implementation facts, proposals, reported checks
  and checks you personally ran. Existing code or tests do not define requirements.
- Carry assigned follow-ups to closure; completion of an original scope does not
  erase later obligations. Name a concrete receiving/repair owner.
- Reuse owning components. Do not introduce another engine, queue, scheduler or
  interpretation layer merely to finish a task number.
- Ask only for material unresolved decisions. Do not reopen settled requirements
  or require approval for ordinary work within an authorized assignment.
- Preserve the owner's wording when reviewing supplied prompts. Itemize proposed
  changes before implementing them when requested; do not quietly reduce scope.
- Keep review rationale outside executable prompts. Deliverables and acceptance
  bullets should be concrete. Handoffs must be durable and current pointers updated.

Existing ownership: Learner owns empirical learning and parser/matcher releases;
Pipeline owns ingest/contracts/storage/shared database access/retention APIs;
Watcher owns capture/playset production and automatic triggers; Reporting and
Analysis owns diagnostic queries, source search, reports and their CLI. Advisory
supports owner decisions and receiving review. Research is not automatically a
new permanent team.

[Agent working practices review](AGENT_WORKING_PRACTICES_REVIEW.md) recommends
shorter reusable task/handoff structures and clearer delivery/receiving ownership,
initially without new Skills. It is **a proposal**, not activated policy. Its
reference to 08B repairing source traversal is stale: that repair is now delivered.

## Checkout and reading discipline

Checkout: `C:/Users/nateb/Documents/ck3chronicle`.
Use `./.venv/Scripts/python.exe` for any justified checks.

Read `AGENTS.md`, applicable nested instructions,
[development environment](DEVELOPMENT_ENVIRONMENT.md), [banned ideas](BANNED_IDEAS.md),
and the opening current sections of [status](PROJECT_STATUS.md),
[plan](PROJECT_PLAN.md), and [current handoff](CURRENT_HANDOFF.md).
These contain substantial contradictory history; follow the latest applicable
owner decision, not whichever paragraph happens to support a conclusion.

For this assignment, read [owner intent](OWNER_PRODUCT_INTENT.md) and
[Trusted Run specification](TRUSTED_RUN_SPEC.md). Then use the focused deliveries
below and inspect owning source only as necessary. The
[Error Contract](ERROR_CONTRACT_SPECIFICATION.md) and
[architecture](ARCHITECTURE_AND_DATA_LINEAGE.md) govern their actual boundaries.

Do **not** read the rejected “shared database request handler — design,” copies,
or continuation instructions. Specifically avoid
`PIPELINE_QUEUED_INGESTION_DESIGN.md`,
`PIPELINE_QUEUED_INGESTION_FOLLOWUP_PROMPT.md`, and
`QUEUE_DESIGN_SHUTDOWN_HANDOFF.md`, even if another document links them.
Use the accepted 07D handoff instead.

The shared checkout has extensive unrelated uncommitted work. Preserve it.
This advisory assignment does not authorize process restarts, production ingestion,
database reset/mutation, retention expiry, model activation, installation, commit
or push. Recorded PIDs and prior activation reports are not proof of current state.

## Trusted Run: intent and reconciliation needed

The specification's core outcome is one explicitly configured CK3 start-to-exit
lifecycle, protected live-root error evidence, successful processing into the
operational SQLite database, a finalized native review shard, and human/structured
reports from stored records without depending on the original error log.

It states that acceptance concerns one identified candidate/revision combination,
not clean-machine installation or public-release readiness. Preserve that distinction.

Do not treat the old specification as an executable checklist without reconciling
it. It still contains historical provider references and potentially superseded
requirements for configuration bootstrap/setup, audit, database/review retention,
pruning, backup/restore, duplicates and verification methods. Some later
capabilities it excludes are already delivered or commissioned. Determine which
requirements are current, superseded, explicitly deferred, or genuinely unresolved.

In particular:

- The owner deferred audit/reconstruction work and directed that no further cycles
  be spent on it unless included explicitly. The owner reports that a separate
  investigation established reconstruction of the content they care about,
  discounting per-message timestamps and emission ordering. Do not reopen that
  investigation or infer a new occurrence-history requirement. Flag any remaining
  milestone-scope decision briefly instead of commissioning an audit.
- Raw-log expiry is separate from SQL history and native review. Do not revive
  old SQL/shard expiry, pruning or backup projects merely because the spec lists
  them; equally, do not silently certify their removal from milestone scope.
- Compare the old configuration/setup requirements with current behavior and later
  decisions before proposing changes. An old requirement is not proof of a current
  defect; implementation is not proof that an owner requirement was withdrawn.
- Existing live evidence includes attachment to already-running CK3 followed by
  capture/ingestion. That alone is not proof of an observed complete start-to-exit
  lifecycle. Inspect later genuine evidence before proposing another live exercise.
- Provisional and unresolved outcomes are legitimate. Trusted Run does not require
  100% classification, a new learner/model, or perfect attribution to mods.

## Delivered boundaries and focused references

| Boundary | Current receiving reference and qualification |
|---|---|
| Classification, exact aggregation, SQL and native review | [Task 06](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md), [v45 integration](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md). Consume the selected immutable parser/matcher assignment; no rematching or semantic taxonomy. |
| Deprecated providers | [06B cleanup](TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md). Old CLI/provider stack was removed. Preserve its portable recovery archive. Do not recreate a missing provider. |
| Learner/runtime releases | [07C](TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md), [Releases](RELEASES.md). Authenticated immutable executable distributions and explicit package selection are delivered. Historical recovery is not a pipeline prerequisite. |
| Ingest, database coordination and reads | [07D](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md). Runtime callers use `HandlerClient`; one database worker owns the connection. Preparation/presentation stay outside it. Three request states and an in-memory queue are delivered. |
| Watcher integration | [Wiring](WATCHER_INGESTION_WIRING_HANDOFF.md), [playset producer](WATCHER_ACTIVE_PLAYSET_HANDOFF.md), [source timestamp](WATCHER_SOURCE_MTIME_HANDOFF.md). Capture remains in `harvester.py`; root `playset.py` owns extraction. |
| Runtime logging and activation evidence | [07E](TASK07E_RUNTIME_LOGGING_HANDOFF.md). Shared JSONL logging and request tracing are delivered; activation and observed attached-session evidence are separate from full Trusted Run acceptance. |
| Diagnostic queries/history | [08A.1](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md), qualified by the latest [multi-Run handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md). |
| Source search/context | [08A.2](TASK08A_2_SOURCE_SEARCH_HANDOFF.md) and latest multi-Run handoff. Known-path scope-before-traversal repair is delivered; do not assign it again. |
| Reports/CLI | [Current 08B prompt](TASK08B_PROMPT.md). Prepared and re-issued; this advisory task has not received an 08B implementation handoff. Check for subsequent delivery. |

Last inspected default package: `68f1ae5db205ab46afef9c4d`, selected through
`models/selection.json`; schema 3. Recheck actual selection if it matters to your
assessment. Do not interpret an isolated learner candidate as production activation.

## Current 08B assignment and reporting decisions

The repository [TASK08B_PROMPT.md](TASK08B_PROMPT.md) is the owner's revised
Downloads draft, re-issued with **only three authorized corrections**:

1. `report` explicitly supports configured/explicit database selection.
2. A valid refinement returning no records is successful empty output, not a
   contradictory query.
3. No median-based notability or replacement statistical baseline/threshold is
   commissioned.

Preserve that version. The Downloads source remains unchanged. No further prompt
rewriting was commissioned. 08B delivers `runs`/`report`, five presets, text/JSON/
offline HTML, default unresolved source candidates and a linked verbose appendix.
Expected handoff: `docs/TASK08B_REPORTING_HANDOFF.md`; its existence alone will not
establish completion.

Settled receiving rules:

- Search diagnostic records, including all rendered bound values. Select one or
  more stored matched template references using OR; no rematching. Separate
  stored-template-text filtering is available and must be distinguished from
  whole-record search.
- Exact identity includes all meaning-bearing literal/layout/binding values,
  including actual locations and their order/count. Shared template does not
  imply identical messages.
- Reporting chronology uses `run["facts"]["error_log_source_modified_at"]`, accepted
  by the owner as session-end ordering. Missing facts are excluded, without
  fallback/backfill. Same-package only; duplicate-ingestion handling stays in the pipeline.
- Default history is up to five predecessors and five successors. Trailing five
  includes the selected Run and at most four predecessors.
- New means positive in the selected Run and absent from all successfully read
  predecessors included in the window. With no included predecessors, positive
  records are new within that window. Disclose coverage; failed reads are not zero
  and do not enter observation fractions. No reads means an unavailable fraction.
- Median/notability fields, `QueryEvidenceError` and its unavailable-read novelty
  veto were removed by owner direction. Do not restore them.
- Source searches may use explicit roots outside a recorded playset. Default
  roots come from that Run's recorded playset. Preserve every candidate, repeated
  member association and recorded load-order number. No winning-file/mod-blame
  inference or full game-state resolution.
- Optional missing context does not suppress SQL diagnostics. Unavailable evidence
  required by a source filter is an explicit evaluation error with partial evidence,
  not an exact zero. Verbose snippets show the referenced line and ten on each side.
- [Syntax research](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md) supplies nine scoped selectors
  for 08B, not a new universal severity taxonomy or automatic cascade diagnosis.

Latest upstream evidence reports four eligible genuine Runs: 18 investigations /
359 comparisons plus two single-Run checks; subsequent scope repair reports 41
scope comparisons, four source investigations / 93 comparisons and nine source
tests. Fourteen older Runs lack timestamps and remain excluded. Failed-read
and other absent genuine cases remain unverified. See
[receiving review](TASK08B_RECEIVING_REVIEW.md) for the distinction between the
advisor's earlier checks and later source/document inspection. Do not claim you
reran this evidence.

## Other settled decisions and separate work

- Ordinary full-log duplicates return the existing Run ID without overwriting it;
  request status is `NOT_COMPLETED` with an ordinary duplicate explanation.
- Owner-desired explicit reprocessing with a different package must preserve Run
  ID, replace the entire processing result including review files, preserve capture/
  playset facts and other Runs, and preserve the previous accepted result on failure.
  It is recorded under [Database policy](TASK07_SCOPE_REVIEW.md#database-policy),
  but implementation/assignment remains separate. Do not make it a Trusted Run
  prerequisite without an owner decision. Generation replay remains banned.
- Raw error/debug logs stay at the watcher location. All completed captures,
  including failed/unprocessed ones, are eligible after the configured initial
  30 elapsed days; daily checks belong to the watcher. Preserve small metadata/
  playset JSON, SQL history and native review. No extra ingestion archive copies.
- Missing playset is an unavailable state, never an assertion of an unmodded game,
  and cannot block otherwise valid ingestion.
- Compatible processing revisions share a database with exact per-Run lineage.
  Schema changes require explicit reset, without migrations or silent deletion.
- Verification uses genuine retained CK3 evidence and disposable storage. Do not
  restore removed synthetic histories, mock clients or fault-injection logging/
  reporting tests. Unrepresented cases stay unverified, not fabricated.

Learner work proceeds separately. [v46 results](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md)
were corrected after the initial corpus omitted target witnesses; consult the
latest findings rather than attributing gains to an algorithm without evidence.
[Canonical Logging System v1](CANONICAL_LOGGING_SYSTEM_V1.md) now supersedes the
earlier phase-based learner logging prompt/proposal. [Task 09A](TASK09A_PROMPT.md)
commissions planning only; see the sequencing recommendation below. No canonical
journal implementation or candidate was created by this advisor.
Current location-variability work has progressed to an owner-authorized disposable
combined locator experiment; inspect the latest CURRENT_HANDOFF.md before advising.
That experiment does not itself activate a production parser/model/API change or
justify altering exact aggregation. Carry these findings forward without making
every learner investigation a pipeline/reporting blocker.

## Outgoing advisor's recommendations after 08B — review, do not execute

Original draft folder:
`C:/Users/nateb/Documents/WIP/CK3Chronicle_Classification_Replacement_Prompts_2026-09-14 (1)/AGENT_PROMPTS/`

**Task 09 — `09_OFFLINE_LEARNER_RECONNECTION.md`: recommend retiring the original
assignment as superseded.** It reconnects to absent `pipeline.emissions` and would
delete currently retained `build_review_pack.py` and `evaluate_unseen_session.py`.
07C already provides learning/registry/evaluation/publication/review routes.
See [earlier 09 assessment](TASK08_TASK09_SCOPE_PROPOSAL.md); its old Task 08 audit
proposal is historical, not current scope. Commission learner follow-ups only for
a named owner-needed operation, not to reuse a number.

**New Task 09A — canonical logging planning, provisional numbering.** This is
separate from the retired original Task 09. Read the owner architecture and
[planning prompt](TASK09A_PROMPT.md); the requested plan output is
`docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md`. It does not yet exist as a
delivery from this advisory task. The prompt stops before source edits, candidate
creation or activation. Final implementation assignment/numbering is unsettled.

Recommended handling for the incoming advisor to assess:

- Plan 09A alongside 08B; do not add canonical-logging implementation to 08B's
  now-agreed three-correction prompt.
- Prefer a bounded learner-first implementation after plan review: shared logger
  extension, immutable distribution, selected actual-function hooks/checkpoints.
  Learner is the proposed delivery lead, with the shared runtime logger's maintainer
  receiving any common change and checking existing watcher/handler behavior.
- Decide separately whether wider watcher/handler/reporting journal conversion is
  needed. Current event names, request correlations, operator instructions and
  destinations have consumers; identify concrete replacements before removing them.
  Do not silently drop needed visibility, create aliases or commission a broad rewrite.
- If logging implementation is approved before the acceptance candidate is chosen,
  include its common-owner changes in Task 10 readiness checks. If it is not a
  prerequisite, keep it independent of Trusted Run completion. Do not move the
  acceptance target continuously to include every observability improvement.
- Use 09A's preservation plan: verified exact working-source copies including
  uncommitted files, coordinated overlapping edits, small diffs, immutable candidate
  releases and rollback limited to this task's changes. Neither Git HEAD nor the
  Markdown exports alone protect current source. No cleanup/reset/release overwrite.

Alternatives are to keep both plan and later implementation under 09A as separately
authorized steps, or split implementation into learner/common-owner delivery and
a later runtime-consumer conversion. Recommend the smallest justified arrangement
to the owner; no alternative is approved merely by appearing here.

**Task 10 — `10_CUTOVER_AND_RETIREMENT_MANIFEST.md`: recommend replacing the old
cutover exercise with a bounded integration and acceptance-readiness review after
08B.** The original assumes providers removed by 06B, relocates capture away from
its current owner, and includes banned generation replay. Existing watcher/ingest/
handler wiring is delivered; 08B registers its own commands.

Proposed replacement deliverables:

- Verify actual watcher publication → ingestion → SQL/review → Run selection →
  report CLI boundaries, using delivered APIs and existing evidence.
- Check packaging of reporting code/templates/dependencies proportionately, without
  turning Trusted Run into clean-machine/public-release certification.
- Identify only concrete remaining defects with responsible team and bounded repair.
- Assess existing complete-lifecycle evidence and specify what acceptance remains.
- Deliver a short readiness handoff and acceptance procedure; live execution remains
  separately authorized.

Recommended product sequence: **08B → bounded integration/readiness review →
concrete repairs if needed → final Trusted Run acceptance and documentation
reconciliation.** New 09A planning may proceed alongside 08B; logging implementation
enters that sequence only by an explicit scope/timing decision as described above.
Reassess old Task 11 cutover together with 10; do not preserve duplicate work.
Task 12-style documentation reconciliation should reflect actual delivery; each
preceding task still maintains its own handoff. These are not yet approved new
executable prompts. The new advisor should challenge or refine this sequence.

## Your first deliverable to the owner

Prepare `docs/TRUSTED_RUN_COMPLETION_PATHWAY.md` and summarize it in chat:

1. A short statement of the milestone's intended user outcome and acceptance meaning.
2. A compact table: requirement/outcome, current authority, delivered behavior,
   evidence and limit, remaining action, responsible/receiving team.
3. Decisions genuinely needed to reconcile old specifications with later direction.
   Recommend an answer for each; distinguish a missing decision from missing code.
4. A minimal sequenced pathway, with concrete deliverables and acceptance bullets.
   Separate disposable verification, already-authorized live evidence, and any
   new live action that would need authorization.
5. Your disposition of original Tasks 09–12, new 09A planning/implementation
   sequencing, and the next executable assignment.

Review available later handoffs before treating the snapshot here as current.
Do not rerun large verification campaigns just to restate reported evidence.
Do not silently shrink Trusted Run to whatever currently passes or expand it to
every capability mentioned in old plans. Present the reconciled pathway before
implementing it or rewriting owning product specifications.
