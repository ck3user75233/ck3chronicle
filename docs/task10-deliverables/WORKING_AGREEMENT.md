# Task 10 — Common execution and Trekker instructions

Read this with the specific owner-issued prompt and [assignment index](../TASK10_DELIVERABLES.md).
Root instructions, current plan/status/handoff and owning technical specifications
apply. Implementation begins on owner issuance; a tracker record is state, not authority.

## Start or resume the actual assignment

Use only the delivered absolute protected route and its canonical store:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state launch-distribution
# Pipeline assignments use: team-state pipeline
# Component contributions use their actual team: watcher, data-intelligence or learner.
& $pilotNode $pilot task-list
# Once the real ID is known:
# & $pilotNode $pilot task-show TREK-N
```

Canonical store: `C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state`.
The existing free-form team tag `launch-distribution` needs no schema/helper change.
Never use raw Trekker/SQL, initialize another store, or add a wrapper.

1. Find this prompt's exact title/path in `task-list` and inspect the actual record.
   If the owner has issued this assignment and none exists, use `task-create` with
   a UTF-8 JSON request in ignored local storage. Fields: `title` (exact prompt
   title), `description` (outcome, owner, authoritative prompt, state and next action),
   `tags` (exactly one owning `team:` tag named in the prompt), `status: "todo"`.
   For **10A** add `producer:launch-distribution, receiver:pipeline` as two array
   entries; for **10A.1** use `producer:pipeline, receiver:launch-distribution`.
   Component documentation contributions use their actual `producer:` team and
   `receiver:launch-distribution`. These are meaningful cross-team deliveries.
   Other assignments need only their team tag; do not invent producer/receiver
   teams for internal work. The Docs role uses `team:launch-distribution`.
2. Read back the result. Record the returned native ID in the prompt and index,
   coordinating those small edits. Do not enroll sibling work not yet issued.
   If another chat already created this exact record, resume it instead.
3. Read the latest checkpoint **and later comments/deliveries/receipts**, then the
   linked authoritative prompt and technical handoffs. Read named dependencies
   directly even if your team view does not list them. Preserve truthful history.
4. When actually starting owner-issued work, set `in_progress`. Readiness never
   chooses another assignment. Add named dependencies through `dependency-add`
   once their real records exist; preserve partial-work allowances in the index.

Exact JSON fields/commands and uncertain-write recovery are in the
[pilot handoff](../TREKKER_CLI_PILOT_HANDOFF.md#protected-invocation-contract).
Use its `task-update`, `checkpoint`, `delivery`, `receipt`, `comment` and
`dependency-add` operations; do not improvise syntax. Re-read before mutations,
preserve unrelated tags and stop/reconcile incomplete writes before retrying.

## Retrieve information as well as recording it

Before declaring an input missing, editing a shared file, integrating a delivery
or resuming dependent work, refresh the named producer record. Retrieve exact
artifact/version, interface agreement, evidence limits, open questions, later
receipts and responses to your requests. Open the linked handoff before consuming.
Available information should not require the Owner to paste it between chats.

Post a concrete question on the relevant canonical record with the named team,
needed answer and effect on your assigned work. Continue independent work. Trekker
does not wake idle chats: if a response requires a dormant assigned team, tell the
Owner only which chat/ID needs resuming and why. A short "Resume ID; see CMT-X"
is sufficient for existing scope; a new technical prompt is not needed each time.
Do not dispatch chats or treat a coordination comment as new implementation authority.

## Record pauses, delivery and receipt

Keep the mutable description short: current outcome/state, responsible team,
next actor/action, prompt and latest handoff/checkpoint links. Do not paste prior
descriptions or full evidence into it. At meaningful pauses append a checkpoint:
what changed; stopping point; next action; limitations; evidence; owner decisions.
No per-read acknowledgments, mandatory cycles or parallel spreadsheet.

The producer records a usable delivery with exact interface/artifact and limitations.
The consumer records what it actually used and whether it meets its requirement.
For cross-team deliveries use `delivery` and `receipt` on the same record; receipt
does not itself close remaining assigned work. For internal 10B/10D/10E deliveries,
10C records receiving disposition on those same records by comment and links its
evidence. Use existing native statuses, not another receiving status system.

Close a producer record when its own scope and required receipt are satisfied.
Keep receiver-only integration/environment work on the receiver's record, linked
back, rather than leaving a completed producer falsely active. Genuine producer
defects stay with that producer until received; identify the exact repair. A usable
partial interface can be consumed before all producer work closes. No circular
"awaiting confirmation" or duplicate tickets for the same obligation.

## Scope, evidence and shared changes

Documentation is part of each feature team's delivery: author the technical
reference/example changes with the interface, and maintain them when behavior
changes. Docs (within Launch & Distribution) owns editorial coherence and user
verification, not the discovery of missing technical contracts. Use the
[bounded contribution prompt](COMPONENT_DOCUMENTATION_INPUT.md) for the explicitly
planned initial Watcher/Reporting/Learner contributions and later specific
owner-issued gaps. Pipeline/setup contributions stay on their existing assignments.
Deliver content/evidence on the canonical producer record, then Docs records
receipt there. Keep final guide acceptance on 10C rather than holding a received
technical producer open for Docs-only work. A substantive later technical error
returns to its producer with the exact correction required.

Launch & Distribution owns user experience/distribution/docs; Pipeline owns the
application and internal configuration/storage interfaces. Preserve Watcher,
Reporting and Learner component ownership. Source edits, shared CLI wiring,
packaging manifests and documentation each need one named editor at a time.
Record the file/section and handoff point; a posted request is not a reply.

Use genuine CK3 inputs and isolated task storage for authorized execution. Creating
or executing each synthetic/fault-injection test requires specific owner approval.
Do not fabricate histories or mock clients to complete acceptance. Inspect actual
results and logs, not merely return codes. Reuse valid evidence with exact source/
artifact correspondence; rerun when changed behavior or failures warrant it.
For runtime changes run the existing runtime logging ownership checker.

Preserve exact prior bytes/absence of edited files and directly coupled atomic
changes; keep wider reproduction inputs separate. Retained releases stay immutable.
No production configuration/database edits, live restart/activation, historical
reingestion, source commit/tag/push or hosted publication is authorized by these
implementation prompts. Fresh isolated configuration/storage and package builds
within the assigned scope are authorized on issuance. Report actual environment
permissions early; never bypass them or postpone a known access blocker until final
delivery. Stop only affected work and continue independent authorized preparation.
