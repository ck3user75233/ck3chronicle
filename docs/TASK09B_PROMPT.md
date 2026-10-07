# Task 09B — Organize logging implementation and track delivery in Trekker

Prepared for assignment after 09A. Advisory prepares any missing owner decisions before proceeding to approved assignments and enrollment.

**Lead: Advisory for coordination only; this creates no approval gate or implementation ownership.** Advisory is an established role under [team governance](team-governance/README.md). Learner supplies technical clarification of the 09A plan; implementation and receiving remain with the owning teams, and approval remains with the owner.

Saving this prompt does not start work.

Evaluate the need for **09C during this task**.

## Start with the available owner direction

**09A completion does not authorize implementation. It does provide the input for useful advisory preparation.**

Read `docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` and identify which owner decisions are already established in the supplied assignment, conversation or linked documents. Do not ask the owner to repeat settled direction merely because it is not in a separate disposition file.

Record each actual owner decision in the assignment index with a precise source reference and, where useful for disambiguation, a short exact quotation. Identify the plan revision and scope it covers. Do not infer approval from the plan, a consultant recommendation or an unavailable prior conversation.

Specifically surface any unresolved owner correction to the 09A plan before producing the affected implementation assignment. Check the current revision rather than carrying forward a superseded discrepancy. At preparation time, the corrected 2026-10-06 plan already uses a trivial local completed-input counter (`enumerate(logs, 1)`) against `len(logs)` in `collect_records`, emitted after each input completes; see sections C and E. It does not use `len(evidence_stats)`, which counts distinct hashes rather than completed inputs. Make that counting recommendation explicit in the owner decision brief and preserve it in the proposed scope. Its presence in the plan is not implementation authorization. If an actual conflict with owner direction remains, surface it for disposition rather than silently choosing between instructions.

Recommendations, sequencing and proposed changes in 09A are not commissioned work merely because they appear in the plan.

If a material scope or pilot decision is missing:

- prepare or update [the owner decision brief](TASK09_OWNER_DECISIONS.md), with each question, recommendation, alternative and practical consequence;
- present concrete proposed scope and ownership, including a short disposition the owner can adopt or amend;
- prepare clearly labelled provisional decomposition and draft prompts where the missing decision does not prevent useful preparation;
- keep proposed work distinct from approved, owner-issued assignments and do not enroll unapproved work; and
- return the concrete decisions and recommendations, not an empty-handed gate message. Continue independent authorized preparation where available.

The decision brief is advisory until the owner accepts it. Do not mark recommendations approved merely by saving that file. Approval is required before treating its scope as commissioned or enrolling it; it is not required to prepare a reviewable proposal.

## Objective and inputs

Prepare any missing owner scope decisions, then turn the completed `docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` **and the owner's explicit scope decisions** into concise, independently assignable deliverables for project-wide logging implementation.

Begin using Trekker to track their execution so responsible teams, next actions, dependencies and unresolved deliveries remain visible across chats.

This task does not add a task tracker to the product.

09B may write decision, draft-assignment and index documents and, when the approved pilot is available, create/update authorized Trekker records. It must not edit CK3Chronicle application/Learner source, implement logging, create candidate releases, perform component verification or execute the Trekker pilot installation itself.

Package the approved plan and dependency order into assignments. Do not reopen its architecture; identify any concrete conflict with current evidence or owner direction for disposition without silently redesigning the work.

Read:

- root instructions;
- current plan/status/handoff;
- the 09A plan;
- [canonical logging design](CANONICAL_LOGGING_SYSTEM_V1.md);
- any available owner disposition and [the decision brief](TASK09_OWNER_DECISIONS.md), distinguishing actual decisions from recommendations;
- [team ownership](team-governance/README.md); and
- the saved [Trekker CLI pilot assignment](TREKKER_CLI_PILOT_PROMPT.md).

Use current release evidence and the relevant component handoffs; do not reconstruct all task history.

If the owner's disposition leaves particular issues unresolved, identify the affected deliverables and continue with independent authorized work.

Proposed scope is not approved merely by being written into the plan or tracker.

## 1. Produce the implementation assignments

Break the **owner-approved scope** into substantive outcomes that can be implemented, verified and received independently.

Before approval, the same decomposition may be prepared only as a clearly labelled proposal for the owner. It must not be presented as an issued assignment or used to enroll implementation work.

Where the approved disposition is already-sufficient/no-code-change, do not create an implementation deliverable merely to give that component a ticket. Create a receiving/compatibility check only if the owner-approved scope requires it.

Split where ownership, dependencies or receiving decisions differ; keep minor coding steps inside a deliverable.

Do not prescribe a ticket count or automatically create one task per team, module or function.

For each deliverable, specify:

- the required outcome, owning team and bounded files/interfaces it may change;
- prerequisites and any shared-file coordination before editing;
- genuine verification, evidence limits, completion conditions and receiving owner where another component consumes the result; and
- a concise owner-assignable prompt linked to the governing plan and owner decisions.

Cover the shared backend/API, authenticated Learner release integration, required component logging adoption, and final application packaging/integrated receiving **only to the extent commissioned by the owner**, according to the actual plan.

Preserve existing team boundaries.

Assign one implementer to each shared change; do not give several teams competing backend implementations.

Coordinate the configuration seam with Task 10 if it is active.

Put the prompts under:

```text
docs/task09-deliverables/
```

and a compact assignment index in:

```text
docs/CANONICAL_LOGGING_V1_DELIVERABLES.md
```

The index holds scope, prompt links and Trekker IDs.

Live progress belongs in Trekker.

Final technical evidence belongs in each component's normal handoff/delivery material. Trekker links to that evidence and records where work stands and what happens next.

Implementation teams execute their owner-issued assignments.

Preparing prompts does not dispatch chats, authorize cross-component repairs or commission every proposed change.

### Assignment authority

**The owner-issued assignment prompt remains the execution authority.**

A Trekker record is a concise state and handoff record. It should contain, as applicable:

- record ID;
- team owner;
- concise required outcome;
- current state;
- next action;
- dependencies;
- producer/receiver relationship;
- evidence references; and
- path/link to the authoritative assignment.

Do not duplicate full implementation instructions into Trekker.

If a Trekker summary and the owner-issued assignment ever appear to conflict, the assignment and subsequent explicit owner direction govern.

## 2. Make the bounded Trekker pilot usable

Inspect the saved CLI pilot's owner authorization and delivery state.

If the approved pilot **has been delivered**, identify and use the **exact protected helper, canonical store and documented invocation path delivered by it**.

Do not construct an alternate helper, alternate store, wrapper or substitute interface during 09B.

If the saved pilot assignment is already owner-approved but undelivered, prepare its prerequisite assignment using that existing ownership and scope. Do not modify its design, select a different owner or infer broader tooling authority. Enroll the prerequisite only when the approved protected helper is available.

If pilot authorization or ownership is not established, recommend an owner and scope in the decision brief. The current recommendation is Pipeline as implementer of the bounded pilot. Do not infer broader or permanent tooling ownership beyond the approved pilot arrangement. This is a proposal, not permission for 09B to install tooling or choose an alternate design.

You may still prepare the logging decomposition and assignment files while Trekker setup remains unavailable.

Do **not** enroll records, fabricate IDs or claim tracker adoption until the separately authorized pilot deliverable is actually available and its protected helper can be used.

The saved prompt governs pinned Trekker 1.11.0, the canonical pilot store, serialized Windows-safe CLI access, bounded helper operations, team-state queries, backup/recovery and minimal enrolled-session instructions.

Do not replace that scope with:

- a fork;
- schema change;
- custom tracker;
- arbitrary CLI proxy;
- MCP/plugin;
- dashboard;
- session hooks; or
- historical migration.

No new permanent team is needed.

## 3. Enroll the real deliverables and begin tracking

Once the approved Trekker pilot is actually available, use **only its delivered protected helper and canonical store** to create records for the owner-enrolled implementation scope.

Link every record to its authoritative assignment and relevant plan section.

Make pending owner decisions and assignment state explicit.

Enrollment does not mean dispatch or execution. Until the owner actually issues the linked assignment, use the pilot-supported state equivalent to prepared/ready/awaiting dispatch, with owner dispatch as the explicit next action. Do not mark work assigned or in progress merely because 09B created a record. Use existing pilot conventions; do not add statuses, schema or another state system for this purpose.

Use:

- One team owner on every item, including internal work without a receiver.
- Optional grouping for the initiative, with independently useful deliverables as tasks and actual prerequisites as dependencies.
- Producer/receiver semantics only for meaningful component deliveries.
- One canonical record visible to both producer and receiver, remaining open until receiving disposition.
- An actionable next step, material evidence limits and concise checkpoints at meaningful pauses.

Do not invent historical sessions, delivery or receipt.

Put the actual Trekker record ID and these startup/resume directions into each owner-assignable prompt and the index, so the team receives them when the owner dispatches the assignment:

1. query its team state;
2. inspect the assigned record and latest checkpoint;
3. open the linked authoritative assignment; and
4. proceed only within that authorization.

Do not contact or dispatch implementation teams as part of preparing these materials.

Record delivery and receiving outcomes as they actually happen.

Finishing one deliverable must leave sibling work and assigned follow-ups visible.

Do not let an available/ready query override an owner's specific assignment.

The tracker records state, not authority.

It cannot authorize:

- new scope;
- repairs outside an assignment;
- production activation;
- product acceptance; or
- synthetic testing.

Creation or execution of each synthetic test requires explicit owner approval for that specific test.

Use real work to assess whether state recovery and handoffs improve; no invented cases, mandatory cycle counts or process KPIs.

## 4. Determine whether 09C is needed

During 09B, assess whether the deliverables already provide complete implementation and receiving ownership.

If they do, recommend **no 09C**.

If a distinct remaining outcome needs a subsequent assignment, name:

- its scope;
- owner;
- prerequisites; and
- reason.

Do not use a new task number to hide unfinished work or duplicate records.

If the decision depends on results not yet available, identify the exact trigger and owner for revisiting it.

Do not pre-authorize or manufacture 09C.

## Completion

Deliver:

- any outstanding owner decisions with concrete recommendations, clearly separated from recorded approvals;
- the assignment index and prompts;
- actual Trekker IDs and dependencies for work that was genuinely enrolled;
- usable team startup/update directions; and
- a short 09C recommendation in the index.

Demonstrate that the relevant team-state views expose the real enrolled work and its current next actions.

Identify any pilot behaviour not yet naturally exercised.

09B establishes actionable assignments and tracking; it does not itself certify the logging implementation complete.

Leave component work and receiving repairs open in Trekker until their real completion.

If pilot setup prevents enrollment, report 09B as partial with the accountable owner and next action. Do not invent Trekker IDs or substitute another tracker/helper.

Missing scope approval likewise limits enrollment and commissioned assignments, not the advisory decision brief or clearly labelled drafts. State exactly what is prepared, which decision remains, and the recommended next action.

No production switch, restart, publication, commit or push is authorized by this coordination assignment; those actions require their own applicable owner authorization.
