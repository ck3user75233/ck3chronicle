# Team governance

## Current team responsibilities

Updated 2026-10-05 following owner direction. This is the authoritative record of
the team boundaries below, including the agreed addition of application packaging
to Pipeline. Teams are owner-directed specialist tasks/chats; a role can have
several bounded assignments. The roles do not require a new agent platform.

| Team / role | Core responsibilities | Delivery, receiving and repair accountability |
|---|---|---|
| **Pipeline** | **Production processing and classification; ingestion and deduplication; Error Contract implementation and native reconstruction; SQLite schema, persistence and per-Run lineage; unresolved review storage; shared database handler and public APIs; retention APIs.** Also owns application packaging, dependencies/resources, installed defaults, deployment preparation and rollback. | Receive and execute the approved Learner parser/matcher/model package on protected logs, preserve capture facts and evidence, and expose durable results to consumers. Own runtime composition, database and application packaging defects. Verify the final installed combination and coordinate integrated receiving/cutover while each component retains its repair owner. |
| **Learner** | Empirical learning, parser/matcher/selection behavior, model construction, comparative evaluation and immutable learner/parser/matcher/model distributions with authenticated identities and pins. | Own the algorithms, model meaning and executable component delivery that Pipeline consumes. Supply interfaces and genuine evaluation evidence; repair defects in those components. Changed retained artifacts require new identities. Pipeline packages these distributions into the application without rewriting them. |
| **Watcher** | **Separate from Pipeline:** CK3 lifecycle observation; protected log capture/publication; observed capture facts; active-playset extraction/publication; automatic ingestion and retention triggers, including startup handling and request-outcome consumption. | Own the capture boundary and the caller integration that invokes Pipeline's APIs. Deliver protected inputs and metadata to Pipeline. Pipeline owns processing/storage and retention implementation; Watcher owns triggering those operations and handling their outcomes. Neither team substitutes inferred facts for unavailable observations. |
| **Data Intelligence / Reporting** | Diagnostic queries and cross-Run searches, history analysis, source search/context, report presentation and exports; compatibility with delivered model/contract structures. | Consume stored results through the public handler, implement analytical/report behavior and repair consumer incompatibilities. Supply genuine verification and source/artifact correspondence for integrated receiving. A task producing a repair wheel does not transfer application packaging ownership from Pipeline. |
| **Advisory** | Owner-facing planning; evidence-based options and recommendations; requirements clarification; concise task prompts; dependency/sequence assessment; delivery and receiving review; decision and handoff continuity. | Own the accuracy of advice, summaries and prompts, including corrections when evidence or owner direction changes. Distinguish requirements, proposals, delivered behavior, reported checks and independently performed checks. Identify unresolved work and its accountable owner. Recommendations do not authorize scope, implementation or activation; Advisory is not a compulsory approval step between teams. |
| **Product owner** | Product intent, priorities, scope and assignment decisions, final acceptance and operational activation authorization. | Resolve material product/scope conflicts and accept outcomes with visible limits. Teams make routine implementation choices within assigned scope. Technical readiness or a completed component delivery alone does not authorize a live switch/restart. |

## Important boundaries

**Classification spans two responsibilities.** Learner owns the parser/matcher/
model behavior and its released implementation. Pipeline owns production execution
and integration of that behavior, conversion into approved contracts, accounting
and persistence. A recognition/model defect goes to Learner; an ingestion,
contract-conversion or storage defect goes to Pipeline. Identify the actual failing
boundary before assigning a repair; Pipeline does not create a competing matcher.

**Watcher remains separate.** Packaging the watcher in the application and
coordinating a release does not transfer its lifecycle/capture implementation to
Pipeline. Watcher publishes and submits; Pipeline processes and persists. Watcher
schedules automatic retention calls; Pipeline owns the retention API and behavior.
See [current Pipeline APIs and caller integration](../TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
and [Watcher capture/playset ownership](../WATCHER_ACTIVE_PLAYSET_HANDOFF.md).
The older Watcher handoff's API details are superseded by the current Pipeline
handoff where applicable.

**Keep application packaging with Pipeline.** It is part of delivering a usable
production runtime. The present work does not establish a need for another team.
Use bounded Pipeline assignments when concurrent packaging and ingestion work
need separate focus. Reconsider a team split only if practical delivery experience
shows a persistent capacity or ownership problem; do not split merely because the
responsibility list is long.

## Working and receiving

Each implementing team owns relevant verification and documentation of its
changes. The consumer verifies its use of the delivered interface. Pipeline owns
consolidating the integrated application result; that does not require it to
implement every component repair. Teams proceed independently within assignments;
ownership does not expand scope into unrelated repairs or production operations.

An unfinished follow-up or receiving repair remains an explicit obligation with
an owner and next action, even after the original delivery is complete. Separate
component delivery, integrated receiving, accepted limitations and activation.
Reuse valid evidence; repeat checks when changes or failures warrant them.

Advisory helps the owner prepare assignments and assess results without adding a
mandatory review gate. Owner decisions govern; advice and historical code/tests
must not silently become new requirements. Advisory must keep a correction visible
in the current prompt/decision record rather than relying on conversation memory.
See the [Advisory working handoff](../ADVISORY_HANDOFF_TRUSTED_RUN.md).

## Where decisions and work live

Update enduring responsibilities here when the owner agrees changes. Task prompts
link here and specify concrete scope, artifacts and evidence. Current work and
operational restrictions remain in [PROJECT_STATUS.md](../PROJECT_STATUS.md) and
[CURRENT_HANDOFF.md](../CURRENT_HANDOFF.md).

The [Pipeline continuation](../learner-next-release/PIPELINE_INTEGRATION_PROMPT.md)
applies these boundaries to the combined release; its artifact identities and
results remain in the [receiving record](../learner-next-release/PIPELINE_RECEIVING.md).

The earlier [working-practices review](../AGENT_WORKING_PRACTICES_REVIEW.md) remains
background/proposals except where separately adopted. Recording these roles does
not adopt that review's remaining workflow, tooling or Skill proposals.
