# Revised implementation assignment — Trekker CLI pilot

Saved 2026-10-04 for later resumption. **Commissioned 2026-10-06 with Pipeline as
bounded pilot implementer; awaiting the owner's issuance to Pipeline.** See
[the actual owner disposition](TASK09_OWNER_DECISIONS.md#o13--pilot-commission)
and [prepared dispatch prompt](task09-deliverables/TREKKER_PILOT_PIPELINE.md).
The design below is unchanged. This does not give Advisory installation authority
or Pipeline broader/permanent tooling ownership. This consolidates the revised assignment,
the owner's corrections and the subsequent deliverable-breakdown clarification.
It supersedes the draft implementation section in the earlier
[investigation](TREKKER_WORK_STATE_REVIEW.md) and
[consultant packet](TREKKER_CONSULTANT_REVIEW_PACKET.md). No tooling or instructions
were activated by saving it.

## Objective and enrollment

Implement a bounded Trekker CLI pilot that makes specialist work and meaningful
cross-component obligations recoverable across conversations. Use reviewed Trekker
**1.11.0**, unchanged, with a thin CK3Chronicle helper. Preserve product assignments
and unrelated checkout work. Trekker is Bun/JavaScript tooling, separate from the
project's Python environment; retain its required runtime and tooling dependency
versions in the installation record.

Owner clarification, 2026-10-05: Trekker may track deliverables across all teams.
Logging is an independent product initiative. [09B](TASK09B_PROMPT.md) is the
proposed starting point for tracking its team-owned implementation deliverables.
No logging integration or logging-specific tracker is requested. Runtime
checkpoints and agent continuation checkpoints are separate.

Enroll only owner-named real tasks with their governing authorization. 09A
produces the technical plan; 09B breaks it into team-owned deliverables and begins
tracking their execution here. Do not retroactively enroll or invent checkpoints
for 09A. Enroll [Task 10](TASK10_PROMPT.md) or other work only when assigned.
The earlier proposed 08B-to-09 handoff is withdrawn: do not reopen completed 08B,
resurrect obsolete Task 09 instructions or invent a receiver. Use the next real
commissioned delivery for producer/receiver evidence; if none is available, leave
that behavior unexercised. Pilot enrollment does not authorize its product tasks.

Use a real specialist task that naturally pauses and resumes for continuation
assessment; the receiving task can also serve this purpose. Do not fabricate
retrospective checkpoints or new work merely to exercise the tracker.

## Granularity: assignments, epics and deliverables

- The owner prompt defines authorized scope; it remains in Markdown.
- An optional Trekker epic groups a large assignment.
- Top-level Trekker tasks represent independently deliverable or independently
  resumable substantive work. Split when outcomes, dependencies, responsibility
  or receiving decisions can progress independently.
- Minor implementation steps belong in checkpoints, not separate tickets.
- One canonical record means **one record per cross-component delivery**, visible
  to both sides. It does not mean one giant record for all of 08B or 09.
- Completion of one deliverable leaves siblings and assigned follow-ups open.
  Closing a grouping must not conceal unresolved authorized work.

Use epics plus top-level tasks for the initial pilot; nested-subtask traversal is
not required. Add only the upstream epic/grouping operations actually needed by
the enrolled assignment. No prescribed number or size of tasks applies.

## Ownership and delivery facts

Use existing Trekker tags, descriptions, comments, statuses and dependencies.
Every work item has one responsible specialist area, for example `team:learner`,
`team:pipeline`, `team:watcher` or `team:data-intelligence`.

Add `producer:<team>` and `receiver:<team>` only for meaningful deliveries.
Ordinary investigations, repairs and maintenance need no receiver. Link the owner
assignment, specification and evidence in the description. Use existing statuses
plus a small delivery convention such as `handoff:pending`, `handoff:changes` and
`handoff:received`.

Producer implementation completion leaves a delivery open pending receipt.
Preserve later assigned follow-ups. Link independently assigned repair work when
needed without creating separate producer and receiver copies. Record implemented,
delivered, received, activated, verified and owner-accepted as distinct facts where
relevant; they need not become separate statuses.

The tracker records state; it never authorizes scope, reassignment, cross-component
repair, activation, testing or acceptance. A discovering receiver may repair
upstream only within existing explicit scope or a subsequent owner assignment.

## One canonical pilot store

Prior inspection found the ignored `.ck3chronicle/wip/tooling` directory, containing
runtime/archive tooling. Proposed working directory:

`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state`

Trekker's native `.trekker/trekker.db` would live beneath it. Confirm accessibility
and retention suitability before initialization; expressly exclude work state from
disposable cleanup. This is **pilot placement subject to later confirmation**.
If unsuitable, use the permitted ignored checkout-root `.trekker` fallback and
record why. Do not silently change location or build a new storage hierarchy.

All participating sessions/worktrees use the same explicitly configured absolute
location, with applicable sandbox access. Never initialize per-worktree copies.
Keep it outside Git and separate from CK3 runtime databases/captures and temporary
verification artifacts. Do not change product configuration or operational roots.

## Bounded helper

Place the helper under `tools/work_state/`, separate from product runtime code.
Use documented Trekker CLI operations and a pinned compatible TOON decoder;
do not import internal services or directly read/change the database/schema.

Expose only operations required by enrolled work:

| Operation | Purpose |
|---|---|
| Create/show/update task | Maintain enrolled work using required upstream fields |
| Minimal epic/grouping operations, if used | Group the authorized deliverables |
| Append comment/checkpoint | Preserve continuation, decisions and evidence links |
| Add/read dependencies | Link actual prerequisites and separately assigned work |
| Inspect history | Read relevant recorded changes |
| `team-state TEAM` | Derive actionable specialist state |
| Record delivery/receipt | Append evidence and consistently update delivery tags |

No arbitrary `trekker <arguments>` proxy, scheduling, generic workflow enforcement
or project policy engine. Share invocation/serialization/decoding internally.
If implementation evidence materially favors a different interface, present the
specific tradeoff before expanding the public surface.

The helper selects the canonical store, serializes all approved access including
reads and multi-command updates, and safely invokes the CLI on Windows using
explicit executables and arguments. Reread records before updates and preserve
unrelated tags. Surface failed/incomplete reads and interrupted updates. Do not
blindly retry possibly committed creates/comments. Document conservative lock
recovery; never expire a live writer's lock based only on elapsed time.

All pilot access uses this protected route. No MCP or background service is needed.
The helper remains disposable infrastructure around Trekker.

## Team state and session practice

`team-state TEAM` returns active work owned through `team:TEAM`, incoming deliveries
requiring that team's action, unresolved outgoing deliveries, blockers/dependencies,
and latest relevant continuation/next actions. Include governing links, material
evidence limits and recorded owner decisions. Use exact tag matching and complete
pagination; surface absent checkpoints or contradictory state.

- **Startup/resume:** identify the assigned task ID, query team state, and read
  that item's checkpoint and governing links. `ready` cannot choose a replacement
  for an owner-assigned task.
- **Meaningful pause:** append completed work, stopping point, next action,
  evidence limits and useful artifact references. No transcript or per-action noise.
- **Delivery:** record actual output/evidence/limits and leave receipt pending.
- **Receipt:** record satisfaction of the consuming requirement, changes required,
  or an explicitly permitted evidence gap. Implementation is not receipt.
- **Closure:** disclose disposition of assigned follow-ups and required decisions.

## Minimal documentation and recovery

Add a concise pilot section to `docs/DEVELOPMENT_ENVIRONMENT.md` for version/setup,
location, commands, conventions and recovery. Add only enrolled-session navigation
and update rules to root `AGENTS.md`. Name a tooling maintainer in the commissioning
assignment; no new permanent team or mandatory advisor is required.

Add IDs to enrolled assignments through an explicit amendment. Markdown preserves
authorization/specifications/technical evidence; Trekker owns enrolled live
obligations. Preserve `CURRENT_HANDOFF.md` for shared-checkout hazards and pointers.
No duplicate live ledgers or historical migration.

Document ordinary backup/restore with clients stopped, the complete state directory
preserved, and the tool version recorded. No new backup service.

## Practical pilot evaluation and exclusions

Continue only long enough for naturally available work to exercise useful resumption
and receipt. No mandatory resumption counts, process KPIs or numerical success gates.
Report qualitatively whether orientation improved, next actions were recoverable
without owner reconstruction, both teams saw the same unresolved obligation,
updates were omitted, or bookkeeping/maintenance became disproportionate. State
what remained unexercised. Do not infer crash/concurrency resilience from normal
serialized operation.

**Creation or execution of each synthetic test requires explicit owner approval
for that specific test.** General implementation/debugging/verification permission
does not authorize synthetic cases. A specific reporting fixture exception does
not authorize synthetic tracker tests.

Exclude forks/schema changes, a custom tracker/database, MCP, stock plugin,
dashboard, session hooks, broad migration, mass documentation cleanup and unrelated
runtime/product changes. Do not commit, push or activate production services.
Deliver the helper, minimal guidance and one concise pilot handoff when the owner
issues this commissioned assignment to Pipeline.
