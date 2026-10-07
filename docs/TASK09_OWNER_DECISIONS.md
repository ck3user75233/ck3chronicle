# Task 09 — owner disposition and original decision brief

## Owner-run remote synchronization script — 2026-10-07

Owner asked Pipeline to review all changes needing staging/commit/push, provide a
PowerShell report script, then provide a complete script to bring the remote up
to date. The Owner ran that report and said "report ready". Pipeline received the
live remote-ref report and prepared a bounded owner-run script: exact reviewed
release and coordination files, local commit/annotated tag, atomic push of `main`
and that tag. This later request extends the earlier local-only Git preparation;
Pipeline does not execute the mutating script in the restricted agent session.
No force-push, tag movement, hosted upload, live switch/restart, reingestion or
Task 10 dispatch is included. Actual completion is recorded by tag and Trekker
receipt, never by script preparation alone. See [the baseline](TASK09_RELEASE_BASELINE.md).

## Local commit and annotated tag authorized — 2026-10-07

Owner issued [Publish and pin the received Task 09 baseline](task09-deliverables/RELEASE_PUBLICATION_PIPELINE.md)
in the Pipeline conversation. This explicitly authorizes the already executed
exact local catalog/default adoption plus a reviewed local commit with message
`Pin Task 09 logging baseline and production-scope model` and annotated tag
`task09-baseline-2026-10-07` on the new commit. Release label is **Task 09 baseline
— 2026-10-07**; 0.0.1/v61 labels remain and publication orders are not versions.
No additional generic approval is required. Session `.git` read-only policy
currently prevents the commit/tag; the baseline records exact continuation work.
Push, hosted upload, live switch/restart, reingestion and synthetic tests are
not authorized. External placement remains deferred to Task10; do not request it.

## Latest production publication authorized — 2026-10-07

Source: Owner's Pipeline conversation: "I want this published as per usual" and
"THIS IS THE NEW MOST RECENT PRODUCTION VERSION OF CK3CHRONICLE". The Owner also
expressed interest in external publication for Task 10. This authorizes adopting
and publishing the verified full-model combination as the newest production
release, superseding the earlier preparation-only limit for those actions.

Pipeline executed local model production order 9, Learner production order 10
and repository default adoption. The exact wheel, pins and actual publication
receipt are in [the baseline](TASK09_RELEASE_BASELINE.md#owner-adoption-proposal).
Physical external installation remains assigned to Task 10 under the explicit
disposition below. No live service switch, Git commit/tag/push or remote upload
is claimed. The session permits no `.git` writes or external staging writes.

Prepared and disposition recorded 2026-10-06. **Both recommendations accepted by
the owner in the current 09B assignment conversation.** Scope approval permits
Advisory preparation and later enrollment; implementation still requires the owner
to issue each team assignment. See the [assignment index](CANONICAL_LOGGING_V1_DELIVERABLES.md).

## External installation verification deferred to Task 10 — 2026-10-07

Source: the Owner's Advisory conversation reply about the outside-repository
installation check: "well I think we should start doing it but not for this one,
leave that to task 10".

Physical outside-checkout installation/execution verification is removed from
this Task 09 release's completion requirements and belongs to Task 10's installation
verification, with Pipeline as the proposed Task 10 lead. It remains unperformed;
this is an explicit scope disposition, not a passed check. It supersedes the
earlier requirement to complete placement before closing TREK-6/Task 09 and the
instruction not to transfer it to Task 10. No external staging access is needed
for this release. Publication/adoption remain outstanding; this decision does not
itself publish, activate, commit/tag or dispatch Task 10.

## Production-scope baseline direction — 2026-10-07

Source: the Owner's Advisory conversation request, "I think we need to create a
new model using this new production code, right? and formally pin everything so
it's clear going forward this is the base for this repo now...", followed by
"great, let's do this and once done, we can advance out of task 09 into task 10.
Give me the prompt/s."

Advisory has prepared [Learner's full-model build](task09-deliverables/RELEASE_BASELINE_LEARNER.md)
and [Pipeline's baseline receiving](task09-deliverables/RELEASE_BASELINE_PIPELINE.md)
on existing TREK-2/6. On owner issuance, these permit rebuilding the existing
73-log production basis with the authenticated logging-enabled Learner, preserving
its input order/settings and incremental schedule, then packaging and receiving
the exact pinned combination. That bounded full build supersedes the earlier
no-full-corpus/two-input limits for these assignments. It does not commission new
algorithms, additional training inputs or historical database reingestion.

The prompts prepare a concrete final baseline adoption decision, including exact
registration/default changes and a reviewed source commit/tag proposal. No live
activation, production selection, publication or Git action is inferred from
prompt preparation. Task 10 follows the received baseline and its own assignment;
its implementation has not been dispatched here.

## Observer deletion direction — 2026-10-07

Source: the Owner's instruction in the Advisory conversation to rewrite the
Watcher review prompt: "the owneer believes the \"Observer\" (refer to the .py's
related for more conrete understanding) to be a parallel construction and has
ordered its deletion." The same message requires checking whether necessary
Watcher functions depend on Observer before deletion. This supersedes earlier
Observer adoption and Observer lifecycle-verification requirements.

The Owner subsequently supplied the [completed Watcher review](WATCHER_OBSERVER_DEPENDENCY_REVIEW.md)
finding required functions independent, then requested: "give me prompts for each
then, and integrate the pipeline removal requiremetns with the replacement candidate
receiving/integration stuff above into one prompt". The [assignment index](CANONICAL_LOGGING_V1_DELIVERABLES.md#project-deliverables)
links the three prepared continuations. This records deletion scope and prompt
preparation, not dispatch or completed removal. No external-placement waiver or
production activation decision is inferred.

## Recorded owner direction — 2026-10-06

Source: the owner's message assigning “Task 09B — Organize logging implementation
and track delivery in Trekker,” followed in that same message by “And, please find
owner direction in response to the owner decision brief”. The numbered quotations
below preserve that supplied disposition, not an inferred or unavailable prior
conversation. Paragraph labels are reference anchors added by Advisory.

### O1 — Approval and revision

> I approve both recommendations in the Task 09 owner disposition.
>
> For Decision 1, I approve the corrected 2026-10-06 Canonical Logging v1 implementation scope for staged implementation through owner-issued team assignments, subject to and preserving the following owner decisions.

### O2 — Backend and lightweight scope

> Canonical Logging v1 remains a lightweight execution journal. `runtime_logging.py` remains the sole editable backend owner and the shared `journal.py` adapter remains small. Do not expand v1 into generalized tracing, monitoring, workflow modelling or an observability framework.

### O3 — Identity

> The approved call model does not include per-call UUIDs, parent-call IDs, call trees or cross-call correlation machinery. Invocation identity, actual code identity, source location, event ordering and existing application request identifiers are sufficient unless a concrete implementation case is later brought back to the owner showing otherwise.

### O4 — Checkpoints

> Bare `journal.checkpoint()` is primarily the local inside-the-call diagnostic mechanism for investigating an opaque or unexpectedly slow call. Do not add routine bare checkpoints merely to mark ordinary successful boundaries already represented by call completion or existing events. Counted checkpoints may be used in normal instrumentation where the executing code already owns truthful completed-work state.

### O5 — Completed-input counting

> For `collect_records`, use completed inputs / total inputs, overriding the current 09A proposal to use `len(evidence_stats)`. The implementation should use a trivial local completed-input counter or `enumerate(logs, 1)` and emit only after each input has completed processing, against the already available `len(logs)`. Do not use distinct accumulated evidence hashes as a surrogate progress count. This permits a trivial local loop counter for work the function is already performing; it does not authorize rescanning, recomputation or logging-owned application work.

Revision reconciliation: the corrected plan already specifies this in C and E.
The reference to a proposal using `len(evidence_stats)` describes a superseded
discrepancy; no current counting conflict needs another owner decision. The
recommendation is explicitly **completed inputs / total inputs**, now accepted.

### O6 — Learner destinations

> Do not use Codex- or agent-specific runtime paths or names as CK3Chronicle logging defaults. Retained learner logging should use the approved CK3Chronicle-owned config-free location, with receipt-relative `learner-logs` where applicable and otherwise the CK3Chronicle workspace location identified in the corrected plan. Explicit `--log-dir` may override it.

### O7 — Exception boundaries

> Do not use Canonical Logging v1 as a general cleanup of existing component exception or traceback ownership. Canonical nested call instrumentation must not add duplicate exception traces, and the canonical invocation boundary may record an escaping exception once. Otherwise preserve existing Pipeline, Watcher, Reporting and application error behaviour unless the newly introduced canonical logging itself creates a specific masking or duplication problem. The bounded learner receipt/terminal repair identified in the plan remains approved because it is directly required at that integration boundary.

### O8 — Preservation

> Preserve only the exact current bytes of files each delivery will actually edit, including prior absence for new files and directly coupled atomic edits, as that delivery's rollback baseline. Keep wider reproduction/authentication inputs separate. Do not turn logging implementation into a repository-scale archival or backup exercise. Retained releases remain immutable, and rollback must not overwrite intervening work.

### O9 — Task 10 interface

> Task 10 remains an interface dependency only. Canonical logging may consume a resolved writable logging destination and validated settings supplied by application configuration, while retained learner execution remains configuration-independent. Task 09 does not authorize redesign of Task 10's installer, path authority, discovery model, doctor, UI or broader configuration architecture.

### O10 — No-change dispositions

> Preserve the corrected plan's explicit no-change dispositions. In particular, do not add logging edits to parser, matcher, decoder, rules, clustering, ingestion, database-handler internals, Watcher lifecycle or harvester merely to populate a coverage matrix. Existing coverage may satisfy Canonical Logging v1 without another hook.

### O11 — Staged scope and ownership

> I approve the staged scope summarized in the decision brief: shared backend/API; authenticated Learner integration and bounded first Learner slice; the approved small Pipeline and Watcher changes; the approved Reporting and foreground composition work; and final application packaging/integrated receiving. Follow the corrected plan's dependency order and component ownership.

### O12 — Preparation is not dispatch

> Advisory should proceed with 09B to prepare the team-owned assignment prompts and assignment index from this approved scope. Preparing or enrolling those assignments does not itself dispatch implementation work; implementation begins only when I issue the relevant team assignment.

### O13 — Pilot commission

> For Decision 2, I commission the bounded Trekker CLI pilot under its existing saved prompt, with Pipeline as implementer of that bounded pilot. This does not assign Pipeline broader or permanent tooling ownership and does not authorize redesign of the approved pilot scope.

### O14 — Pilot prerequisite and enrollment

> Prepare the Trekker pilot assignment for me to issue to Pipeline. Once its protected helper and canonical store are delivered and usable, 09B may enroll the approved logging deliverables using the existing pilot state appropriate for prepared work awaiting owner dispatch.

### O15 — Authority and evidence

> The tracker records state, not authority. The owner-issued assignment remains the implementation authority, and technical evidence remains in the normal component handoff/delivery material.

### O16 — Exclusions

> This approval does not authorize 09B to implement logging or tooling, dispatch chats, activate production, restart services, publish releases, commit or push, create unapproved synthetic tests, or expand scope beyond the approved assignments.

## Current disposition

No material logging-scope or pilot-ownership decision remains outstanding.
The pilot is now delivered; 09B enrollment uses its protected route. The owner's
subsequent revised [deliverables](CANONICAL_LOGGING_V1_DELIVERABLES.md) consolidate
Learner administration into Learner Integration and Pipeline foreground work into
Pipeline Integration, with six logging outcomes and no extra assignments. This
owner-supplied consolidation governs the earlier advisory split and staging labels.
Next owner action: issue Shared Backend/API (`TREK-1`) to Pipeline.
The [pilot prompt](task09-deliverables/TREKKER_PILOT_PIPELINE.md) retains the saved
design unchanged. No approval is inferred for Task 10, production
activation, synthetic cases or a subsequent 09C. Advisory recommends no 09C on
the current decomposition; the index records the precise revisit trigger.

## Original advisory brief — historical proposal, now disposed above

The remainder preserves the recommendation and alternatives as prepared before
the owner's reply. Conditional/unapproved wording below describes that earlier
state; the recorded disposition above governs. The brief addresses the corrected 2026-10-06
[09A plan](CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md), particularly its edit set
in B, component dispositions in E and delivery sequence in H. Section I reports
no unresolved design question. Source changes and verification remain future work.

## Decisions needed

| Decision | Recommendation | Alternative and practical consequence |
|---|---|---|
| **1. Which logging scope should proceed to team assignments?** | Approve the corrected scope listed below for staged implementation through owner-issued team assignments. Advisory prepares those prompts under 09B; each component keeps its implementation/receiving owner. | Commission only the shared backend and Learner slice initially. Other required component deliveries remain deferred and visible; this does not complete project-wide adoption. |
| **2. Should the Trekker CLI pilot be commissioned now, and who owns it?** | Commission **Pipeline** as implementer of the bounded pilot under the existing saved CLI pilot prompt. Do not infer broader or permanent tooling ownership beyond the approved pilot arrangement. Prepare/issue that bounded assignment while Advisory prepares logging assignments. Enroll approved logging deliverables only when the delivered protected helper and canonical store are usable. | Defer the pilot. Advisory can still prepare logging assignments, but 09B's Trekker enrollment remains incomplete. No substitute tracker or helper is authorized. |

The owner has already selected the established Advisory role to lead 09B for
coordination only; this creates no approval gate or implementation/receiving
ownership. A new team, a separate
approval of routine API choices, Task 10 completion and an automatic 09C are not
needed. Evaluate 09C during 09B. Production activation remains a later decision
about an identified, received artifact; it is not an approval requested here.

## Recommended logging scope for decision 1

| Delivery / owner | Concrete outcome |
|---|---|
| Shared backend/API — **Pipeline**, Learner receives retained interface | Extend the existing logging owner for explicit destinations and configuration-independent use; add the small shared call/checkpoint adapter. Preserve existing callers and useful runtime evidence. |
| Authenticated integration and first Learner slice — **Learner** | Retain/authenticate the shared logging bytes; implement invocation configuration, outcome/receipt handling and direct mapping-consumer repairs. Add the four selected scopes: `collect_records`, `sync_registry`, `build_model`, `write_bundle`. Produce and verify a new immutable candidate through the existing release mechanism. |
| Bounded Pipeline adoption — **Pipeline** | Add the foreground accepted-request observation and catalog-command invocation. Existing ingestion, handler, preparation and storage logging otherwise remains sufficient. |
| Bounded Watcher adoption — **Watcher** | Move the logging observer's ordinary JSONL output to the shared backend while preserving measurements and heartbeat. Existing lifecycle, capture and automatic-trigger coverage needs no new hooks. |
| Reporting and foreground composition — **Data Intelligence / Reporting and Pipeline**, coordinated with Learner for its entry point | Reporting adds only `search_runs`, source `_content` and export `_emit` scopes. Pipeline owns root foreground setup/outcomes and enforcement; Learner owns its administrative entry-point changes. Preserve existing errors, console output and destination ownership. |
| Final packaging/integrated receiving — **Pipeline**, components repair their own defects | Build a fresh application artifact from received sources and authorized immutable resources. Authenticate installed correspondence and receive bounded genuine component evidence. Keep production activation separate. |

Use the plan's dependency order: shared backend → Learner first slice → bounded
Pipeline/Watcher changes → foreground/Reporting integration → final packaging and
receiving. Coordinate overlapping files; do not create competing owners or
duplicate delivery records.

**Counting recommendation within decision 1:** approve completed inputs / total
inputs for `collect_records`. The current 2026-10-06 plan already specifies
`enumerate(logs, 1)` after full input processing against `len(logs)` in sections C
and E. The consultant's reference to a planned `len(evidence_stats)` count is
superseded by that revision. Distinct hashes measure accumulated evidence, not
completed-input progress. No separate unresolved choice remains in the plan;
accepting the proposed implementation scope remains an owner decision.

Preserve the corrected plan's limits:

- `collect_records` uses a trivial local completed-input counter or
  `enumerate(logs, 1)`, emitted after each completed input against `len(logs)`.
  Do not substitute `len(evidence_stats)`, rescan or recompute application work.
- No logging edits to parser, matcher, decoder, rules, clustering, ingestion,
  database handler, Watcher lifecycle or harvester merely to populate a coverage
  matrix. Preserve the explicit no-change dispositions.
- Task 10 contributes only its logging/configuration interface dependency; its
  installer and setup design are outside this logging assignment.
- Use the current-source baseline and bounded genuine checks. Do not repeat the
  completed full-corpus build, historical ingestion or production cutover. Each
  synthetic test still requires its own explicit owner approval.
- Preserve only each delivery's edited files for rollback and reference wider
  reproduction inputs separately. Keep retained releases immutable.

## Recommended pilot scope for decision 2

Use [the saved pilot assignment](TREKKER_CLI_PILOT_PROMPT.md): reviewed Trekker
1.11.0, one canonical pilot store, serialized Windows-safe CLI helper access,
team ownership, optional producer/receiver delivery semantics, team-state views,
concise checkpoint/delivery/receipt operations and proportionate recovery guidance.
Its proposed location remains pilot placement subject to the specified suitability
check; no new storage architecture is being approved.

The recommendation assigns Pipeline the bounded pilot delivery; Advisory uses
the delivered interface in 09B. Any maintenance responsibility is limited to the
approved pilot arrangement; this does not assign broader or permanent tooling
ownership.
Do not install Trekker inside the product runtime or add MCP, a stock plugin,
dashboard, hooks, schema changes, arbitrary CLI proxy or historical migration.
Store assignment authority and technical evidence in Markdown; tracker records
hold current state and links. Newly prepared records await owner dispatch rather
than implying execution has started.

At this review, `tools/work_state/` is absent and the saved pilot prompt says
deferred. No delivered protected helper or pilot delivery reference was located.
These observations establish a setup prerequisite, not a reason to stop advisory
preparation or to invent a substitute implementation.

## Proposed owner reply — effective only if adopted

> I approve the corrected 2026-10-06 09A scope summarized in decision 1
> above, preserving its no-change dispositions, completed-input counting and stated
> limits. Advisory should proceed with 09B, preparing the team-owned assignment
> prompts and index. I commission the bounded Trekker CLI pilot under its saved
> prompt as proposed in decision 2, with Pipeline as implementer of that bounded
> pilot, without assigning broader or permanent tooling ownership; prepare that
> assignment for me to issue to Pipeline. Once its protected helper and canonical
> store are delivered, 09B may enroll the approved logging deliverables in the
> appropriate prepared/awaiting-dispatch state. Implementation starts through
> my team assignments. This does not authorize 09B to implement logging or
> tooling, dispatch chats, activate production, restart services or publish.

An owner may approve both recommendations together or amend either. Record each
actual decision and its scope with a precise source reference and, where useful
for disambiguation, a short exact quotation. Do not convert this proposed text
into an approval record automatically.
