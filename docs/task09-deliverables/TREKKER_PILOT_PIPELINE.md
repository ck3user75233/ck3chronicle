# Pipeline — Deliver the Commissioned Trekker CLI Pilot

Prepared for the owner to issue.

**Implementer: Pipeline.** This is the commissioned bounded Trekker pilot. It assigns no broader or permanent tooling ownership.

Delivery amendment, 2026-10-06: the [pilot is delivered](../TREKKER_CLI_PILOT_HANDOFF.md)
and 09B has used its protected route for real logging enrollment. No Trekker ID
was created retrospectively for the pilot. The owner-issued design below is unchanged.

## Objective

Execute the existing:

```text
TREKKER_CLI_PILOT_PROMPT.md
```

unchanged, under the recorded Task 09 owner direction.

That saved assignment remains the authority for the pilot design. This prompt identifies the implementer and Task 09 receiving boundary; it does not replace or expand the approved design.

Deliver:

- pinned Trekker 1.11.0 and its recorded compatible runtime/tool dependencies;
- one canonical pilot store;
- the serialized Windows-safe protected helper under `tools/work_state/`;
- bounded create/read/update/dependency/checkpoint/delivery/receipt/team-state operations;
- minimal enrolled-session navigation guidance; and
- a concise pilot handoff containing the exact delivered paths and invocation syntax.

Confirm the proposed canonical store location satisfies the saved assignment's access and retention requirements. Use only the permitted ignored-root fallback if it does not, and document the reason.

Do not expose arbitrary Trekker CLI access or direct SQL access.

## Scope boundaries

All Trekker reads and writes must use the protected serialized route.

Preserve unrelated tags and state. Re-read before updates where required by the saved design, surface incomplete reads or writes, and do not blindly retry an update that may already have committed.

Document proportionate lock/recovery and stopped-client backup/restore procedures.

Do not change CK3Chronicle product configuration or runtime roots.

Permitted edit surfaces are only those authorized by the saved pilot assignment, including as applicable:

- the protected helper/tooling installation;
- the ignored canonical pilot store;
- the concise Trekker section in `docs/DEVELOPMENT_ENVIRONMENT.md`;
- enrolled-session navigation in root `AGENTS.md`; and
- the pilot handoff.

Coordinate shared documents before editing and preserve unrelated current work.

Do not edit product or Learner implementation source.

Do not add:

- MCP or plugins;
- dashboard/UI;
- session hooks;
- Trekker schema changes;
- arbitrary CLI proxying;
- historical task migration; or
- a new permanent team or governance layer.

## Task 09 use

The delivered pilot must be usable by 09B to track the approved Canonical Logging deliverables:

- Shared Backend/API
- Learner Integration
- Watcher Integration
- Pipeline Integration
- Reporting Adoption
- Final Packaging

The pilot handoff must document the existing Trekker convention suitable for work that has been prepared but is awaiting owner dispatch, with owner issuance as its next action.

Do not invent a new status system for Task 09.

Tool delivery itself does not dispatch or begin any logging implementation.

Do not retroactively enroll 09A or fabricate historical tracker state.

Do not enroll unassigned Task 10 work.

The Trekker Pilot itself does not need to be retroactively enrolled after delivery merely to manufacture a tracker history from before the tracking capability existed.

## Verification

Use the real authorized pilot setup and ordinary real reads/updates needed to demonstrate that the protected interface is usable.

Do not invent tasks or sessions simply to exercise features.

Every synthetic test requires explicit owner approval for that individual test.

Verify and document the functionality that can naturally be exercised during delivery. State honestly what remains unexercised, including where applicable:

- cross-session resumption;
- producer/receiver completion;
- interrupted updates;
- lock recovery;
- backup/restore; and
- concurrent access.

Normal serialization does not by itself prove crash or concurrency safety.

Absence of a real cross-team receipt case does not prevent delivery of an otherwise usable bounded pilot.

## Handoff

Write the normal pilot handoff specified by the saved assignment.

It must state at minimum:

- exact Trekker and dependency versions;
- exact canonical store location;
- exact protected helper location;
- exact supported invocation syntax and operations;
- team-state usage;
- assignment/checkpoint/delivery/receipt conventions;
- backup/recovery guidance;
- limitations and naturally unverified behaviour; and
- any repair still required from Pipeline.

**Receiver: Advisory for resumption of Task 09B enrollment.** This is a usability receiving boundary, not an additional approval gate.

After receiving the handoff, 09B will use the delivered protected route to enroll the approved Canonical Logging deliverables. The assignment prompts remain execution authority and the tracker records state only.

Any actual defect in the delivered pilot remains with Pipeline until received or explicitly dispositioned.

No commit, push, product installation, production activation or runtime restart is authorized by this assignment.
