# Task 09B — Organize logging implementation and track delivery in Trekker

Prepared for assignment only after 09A **and an explicit owner disposition of the 09A plan**.

**Lead: Learner**, continuing its planning role; implementation and receiving stay with the owning teams.

Saving this prompt does not start work.

Evaluate the need for **09C during this task**.

## Entry gate

**Do not start 09B merely because 09A is complete.**

Before beginning this assignment, the owner must have reviewed `docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` and identified the implementation scope authorized for assignment.

Recommendations, sequencing and proposed changes in 09A are not commissioned work merely because they appear in the plan.

If no owner disposition is available:

- identify the specific decisions needed;
- do not create implementation assignments from unapproved recommendations;
- do not enroll proposed logging implementation work in Trekker; and
- stop.

## Objective and inputs

Turn the completed `docs/CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` **and the owner's explicit scope decisions** into concise, independently assignable deliverables for project-wide logging implementation.

Begin using Trekker to track their execution so responsible teams, next actions, dependencies and unresolved deliveries remain visible across chats.

This task does not add a task tracker to the product.

Read:

- root instructions;
- current plan/status/handoff;
- the 09A plan;
- [canonical logging design](CANONICAL_LOGGING_SYSTEM_V1.md);
- the owner's disposition of the 09A plan;
- [team ownership](team-governance/README.md); and
- the saved [Trekker CLI pilot assignment](TREKKER_CLI_PILOT_PROMPT.md).

Use current release evidence and the relevant component handoffs; do not reconstruct all task history.

If the owner's disposition leaves particular issues unresolved, identify the affected deliverables and continue with independent authorized work.

Proposed scope is not approved merely by being written into the plan or tracker.

## 1. Produce the implementation assignments

Break the **owner-approved scope** into substantive outcomes that can be implemented, verified and received independently.

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

Inspect whether the saved CLI pilot has already been delivered.

If it has, identify and use the **exact protected helper, canonical store and documented invocation path delivered by that approved pilot**.

Do not construct an alternate helper, alternate store, wrapper or substitute interface during 09B.

If the pilot has not been delivered, make its setup the first prerequisite deliverable, with Pipeline as the proposed tooling owner, and prepare its assignment from the saved prompt.

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

Use:

- One team owner on every item, including internal work without a receiver.
- Optional grouping for the initiative, with independently useful deliverables as tasks and actual prerequisites as dependencies.
- Producer/receiver semantics only for meaningful component deliveries.
- One canonical record visible to both producer and receiver, remaining open until receiving disposition.
- An actionable next step, material evidence limits and concise checkpoints at meaningful pauses.

Do not invent historical sessions, delivery or receipt.

Give each assigned team its record ID and startup/resume directions:

1. query its team state;
2. inspect the assigned record and latest checkpoint;
3. open the linked authoritative assignment; and
4. proceed only within that authorization.

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

- the assignment index and prompts;
- actual Trekker IDs and dependencies for work that was genuinely enrolled;
- usable team startup/update directions; and
- a short 09C recommendation in the index.

Demonstrate that the relevant team-state views expose the real enrolled work and its current next actions.

Identify any pilot behaviour not yet naturally exercised.

09B establishes actionable assignments and tracking; it does not itself certify the logging implementation complete.

Leave component work and receiving repairs open in Trekker until their real completion.

If pilot setup prevents enrollment, report 09B as partial with the accountable owner and next action. Do not invent Trekker IDs or substitute another tracker/helper.

No production switch, restart, publication, commit or push is authorized by this coordination assignment; those actions require their own applicable owner authorization.
