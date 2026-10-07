# Trekker CLI pilot — Pipeline delivery to Advisory

2026-10-06. **Delivered for resumption of 09B enrollment.** The pinned toolchain is
installed, one canonical store is initialized and protected empty-store reads
succeed. Mutation operations are implemented and reviewed against the installed
CLI, but await genuine enrolled work for execution evidence. Pipeline retains
actual receiving defects until received or explicitly dispositioned; no known
repair remains. Advisory is the usability receiver, not another approval gate.
The owner issued the saved assignment in the
current Pipeline conversation. Its design in [the unchanged assignment](TREKKER_CLI_PILOT_PROMPT.md)
and [O13–O15](TASK09_OWNER_DECISIONS.md#o13--pilot-commission) remains authoritative.

## Current result and exact paths

Delivered source and operating paths:

- Protected helper: `C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs`
- Pinned installer: `C:\Users\nateb\Documents\ck3chronicle\tools\work_state\install.ps1`
- Dependency manifest: `C:\Users\nateb\Documents\ck3chronicle\tools\work_state\package.json`
- Resolved dependency lock: `C:\Users\nateb\Documents\ck3chronicle\tools\work_state\package-lock.json`
- This handoff: `C:\Users\nateb\Documents\ck3chronicle\docs\TREKKER_CLI_PILOT_HANDOFF.md`

Canonical working directory:
`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state`.
Initialized native database:
`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state\.trekker\trekker.db`.
Local packages belong in its `toolchain\node_modules`; no global installation,
product dependency, Python environment or operational root is changed.

Placement is suitable for this checkout: the parent grants Modify to sandbox
users and FullControl to the owner; creation/writes succeeded, and `.ck3chronicle/`
is ignored by Git. It is separate from runtime/capture roots. No cleanup rule for
this tooling subtree was found in the inspected tooling/retention code.
`RETAIN-WORK-STATE.txt` expressly excludes the **whole directory** from disposable
`wip`/tooling, runtime, archive and verification cleanup. Preserve that exclusion
in any future cleanup. No fallback was needed or used. Each participating
session/worktree must have sandbox access to this same absolute directory and
helper; a narrower session must obtain that access, never initialize a copy.

## Installed versions and setup

| Component | Exact pin / observation |
|---|---|
| Trekker | `@obsfx/trekker@1.11.0` |
| Bun | `bun@1.3.10`; installed Windows x64 and x64-baseline platform packages also `1.3.10` |
| TOON decoder | `@toon-format/toon@2.1.0`, same pin as Trekker |
| Commander | `13.1.0` |
| Day.js | `1.11.19` |
| Drizzle ORM | `0.38.4` |
| Node | Existing `v24.19.0`, observed at `C:\Program Files\nodejs\node.exe` |
| npm | `11.17.0`, invoked through Node and `C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js` |

The installed package/bin/decoder and CLI command implementations were inspected;
real initialization and read operations demonstrate this installed combination.
Installation metadata is at
`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state\toolchain\installation.json`,
recorded `2026-10-06T08:23:44.4240642Z`. The full dependency graph, registry origins
and integrity values are in the lockfile, SHA-256
`D3A4A71781617DE1EDCAB28834C60BB86F8BA1E2EC96CDFFC053ED965AEC8D7F`.

The owner ran the installer after managed-session registry denial. Its Windows
PowerShell quoting problem and unjustified exact bootstrap npm version gate were
repaired. It requires Node 18+ and records actual Node/npm versions. The npm Bun
postinstall warning did not prevent the pinned executable from running Trekker;
no blanket script approval or policy change is needed for ordinary use.

From any starting directory, use:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot versions
& $pilotNode $pilot task-list
& $pilotNode $pilot epic-list
& $pilotNode $pilot history
& $pilotNode $pilot team-state pipeline
& $pilotNode $pilot team-state learner
& $pilotNode $pilot team-state watcher
& $pilotNode $pilot team-state data-intelligence
& $pilotNode $pilot team-state advisory
```

**The store is already initialized; do not rerun `init`.** Do not blindly retry
any possibly committed initialization or mutation. The dependency lock also
exists in `toolchain\package-lock.json`. If tooling reinstallation is needed,
stop clients and invoke the absolute `install.ps1` path above; it uses `npm ci`
with the lock. Reinstallation is unnecessary for ordinary use. Preserve package
licensing/notices and do not patch Trekker to match the helper.

## Protected invocation contract

Use the two absolute variables above from every session/worktree. Results are
JSON; errors exit nonzero and identify any pending recovery marker. These are
the supported operations; the verification section distinguishes exercised paths.

| Invocation after `& $pilotNode $pilot` | Meaning |
|---|---|
| `help` | Local syntax, no tracker access |
| `versions` | Verify installed pins under the canonical lock |
| `init` | One-time native initialization under the lock |
| `task-list`, `epic-list` | Complete paginated inventories |
| `task-show ID` | Record, all comments and dependency records |
| `epic-show ID` | Epic and all top-level member tasks |
| `task-create REQUEST.json`, `epic-create REQUEST.json` | Create authorized work/grouping |
| `task-update ID REQUEST.json`, `epic-update ID REQUEST.json` | Re-read, bounded patch, read back |
| `comment ID REQUEST.json`, `checkpoint ID REQUEST.json` | Append evidence/continuation |
| `comments ID` | All task comments |
| `dependency-add ID PREREQUISITE_ID` | ID depends on prerequisite; existing edge is reported |
| `dependencies ID` | Both edge directions plus current endpoint records |
| `history` or `history ID` | All pages of native history, optionally entity-filtered |
| `delivery ID REQUEST.json`, `receipt ID REQUEST.json` | Evidence comment then handoff tag update |
| `team-state TEAM` | Complete task inventory filtered by exact ownership/delivery tags |

Request files are UTF-8 JSON objects (BOM accepted), parsed as data. Use absolute
request paths outside the source tree in ignored local storage. Do not interpolate
assignment prose into shell commands. Required/optional request fields:

- **Task create:** required `title`, `description`, `tags` (array containing exactly
  one `team:TEAM`); optional `priority` (integer 0–5), `status`, `epic` (native ID).
  Description contains assignment, specification and governing decision links,
  receiving boundary, current next action and evidence limits.
- **Epic create:** required `title`, `description`; optional `priority`, `status`.
  Use description for responsible area and governing links (native epics have no
  tags). Team state is derived from top-level task records.
- **Task update:** any of `title`, `description`, `priority`, `status`, `epic`
  (`null` removes membership), `addTags` / `removeTags` (arrays). No blanket tags
  replacement. **Epic update:** title/description/priority/status only. Native
  cascade-complete is excluded; closing a group cannot hide unresolved children.
- **Comment:** required `author`, `content`.
- **Checkpoint:** required text fields `author`, `completed`, `stoppingPoint`,
  `nextAction`, `evidenceLimits`, `artifacts`, `ownerDecisions`. Use truthful
  “none recorded” where appropriate, never invented history. Stored as a normal
  Trekker comment prefixed `[checkpoint]`.
- **Delivery:** required `author`, `evidence`, `limits`, `nextAction`.
- **Receipt:** those same fields plus `outcome`: `received` or `changes`. Evidence
  describes satisfaction of the consuming requirement or required changes; an
  explicitly permitted evidence gap must include its authority and limits.

Unknown fields/operations are rejected. No arbitrary CLI arguments, SQL, schema
access, deletions, hooks, dashboard or plugins are exposed. All tracker access,
including native history/reads, stays inside the serialized helper. The helper
uses the package's public bin through the explicit local Bun executable, argument
arrays and no shell; only the pinned TOON package is imported for decoding.

## State conventions and 09B receiving

Use native statuses `todo`, `in_progress`, `completed`, `wont_fix`, `archived`
(epics omit `wont_fix`). **Prepared, awaiting owner dispatch = `todo`**, with the
description/checkpoint recording **“Next action: owner issues the assignment.”**
Do not add a dispatch status or infer dispatch from dependencies/readiness.

09B may group the six approved Canonical Logging deliverables in an epic and
create top-level tasks for Shared Backend/API, Learner Integration, Watcher
Integration, Pipeline Integration, Reporting Adoption and Final Packaging now
that the pilot is usable. Advisory owns that enrollment and explicit ID
amendments to the [index and prompts](CANONICAL_LOGGING_V1_DELIVERABLES.md).
Pipeline has created **no tasks, epics, IDs, checkpoints or synthetic sessions**.
Do not retroactively enroll 09A or the pilot, or enroll unassigned Task 10.

Each task has one `team:TEAM`. Meaningful cross-component deliveries also have
`producer:TEAM` and `receiver:TEAM` on that **same record**. `delivery` appends
evidence and sets `handoff:pending`; `receipt` sets `handoff:received` or
`handoff:changes`. Both preserve status and all unrelated tags. Producer work
remains open while receipt is pending; changes return action to the producer.
Receipt does not auto-close assigned follow-ups. Before explicit closure, append
their disposition and required decisions, linking independently assigned repair
work/dependencies where needed. Do not duplicate producer/receiver tasks.

Keep implemented, delivered, received, activated, verified and owner-accepted as
distinct recorded facts, not invented statuses. Comments/checkpoints carry owner
decisions and evidence links; the tracker cannot authorize scope or testing.

`team-state TEAM` includes owned open work, pending incoming deliveries,
unresolved outgoing deliveries, both dependency directions and blockers, full
descriptions/comments, latest checkpoint/action and state warnings. Missing
checkpoints and contradictory handoff/status evidence are surfaced. Pagination
metadata, counts and duplicate IDs are checked; a failed/incomplete page fails
the whole read. Timestamp ties in upstream ordering still require reading the
returned evidence rather than assuming a perfect event chronology.

On resume, read team state, the owner-assigned ID, its checkpoint and governing
links. At a meaningful pause append work done, stopping point, next action,
limits and useful artifacts. Do not create transcript/per-action noise.

## Lock, incomplete operations and stopped-client backup

All helper operations and installation use the canonical `.access-lock`
directory, created exclusively. Contention fails visibly; there is no automatic
expiry or retry. `owner.json` identifies host, PID, start timestamp and operation.
The lock spans read/modify/write, all pages and all steps of delivery/receipt.
It is cooperative protection, not an OS security boundary against direct access.
No client may run the raw CLI or database tools.

Before a mutating CLI call, `incomplete-operation.json` records intended arguments;
successful steps/results are retained until the operation and read-back finish.
Any possibly committed failure keeps that marker and blocks subsequent writes.
Protected reads remain available after ordinary process exit and show the marker.
Never blindly replay creates, comments or multi-command updates. Compare the
record, comments and native history to the intended operation; a successful
comment with a missing tag update must be reconciled as separate known work.

For an interrupted/abandoned lock: stop participating clients, inspect the owner
metadata **and actual process command lines/start times**, including Bun/npm
children. PID absence alone does not prove its child exited; PID reuse and
missing/truncated metadata demand manual inspection. Never expire a live writer
by age. After proving all relevant processes stopped, copy the lock and pending
marker as recovery evidence, then remove only the two known lock files/directory
(`owner.json`, `.access-lock`) without recursive deletion. If identity remains
uncertain, leave the lock and escalate to Pipeline.

Use protected reads to reconcile any pending operation. After its outcome and
remaining repair are documented, preserve the marker in a timestamped recovery
archive and remove the original **with all clients still coordinated/stopped**
before issuing the one needed repair. If the marker is unreadable, preserve it
before removing it to permit inspection; keep all other writers stopped until
reconciliation finishes. Do not use direct SQL or retry all recorded steps.
An upstream CLI error/output limit also requires inspection; no timeout-based
kill or automatic writer recovery is implemented.

For backup, stop all clients and verify no helper/Bun/npm process remains. Acquire
the same `.access-lock` exclusively with owner metadata identifying maintenance;
do not displace an existing lock. Copy the **complete work-state directory** to
an owner-selected retained backup destination, including `.trekker`, any SQLite
sidecars, retention marker, pending-operation evidence and the toolchain/version
records. Preserve the helper, dependency manifest and lockfile alongside it.
Verify copied file counts/sizes/hashes while clients remain stopped. Release only
your maintenance lock. Do not back up only the `.db` file or use a temporary
verification directory for retained backups.

For restore, stop/coordinate clients, acquire the lock and first preserve the
complete current directory as rollback evidence. Restore the complete snapshot
to the **same** canonical path while retaining the active maintenance lock; do
not activate a copied backup lock. Match the recorded helper and pinned tools.
Release your maintenance lock, then reconcile restored incomplete-operation
evidence and run protected inventories/team-state reads before reopening writes.
Do not initialize, merge databases, change product roots or guess missing outcomes.

## Verification, limitations and receiving responsibility

Genuine checks completed: installed package/bin/decoder inspection; protected
version checks; single real initialization through the helper; successful TOON
decoding of actual initialization/list/history output; task/epic/history inventories
and team-state for `pipeline`, `learner`, `watcher`, `data-intelligence`, `advisory`.
All inventories are empty with no pending recovery. Reads from outside the
checkout selected the same canonical store. Static syntax and `git diff --check`
passed. Exact ordinary read results are retained at
`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state\delivery-verification.json`.
That file records delivery evidence, not tracker history.
The saved assignment's SHA-256 remained
`73CC74DE358CFD68ECBCDE258F60CE09FBD688022B16A07306169014CAEFF3C3`.
Shared-document coordination was requested in the owner conversation; no overlap
was reported. Only pilot guidance was appended/updated after re-reading files.
Pre-existing Advisory edits and all product/Learner implementation were preserved.

**Unexercised:** populated task/epic create/show/update, dependencies,
comments/checkpoints, delivery/receipt and producer/receiver completion,
populated-team filtering, complete multi-page traversal, cross-session resumption,
interrupted updates, lock recovery, backup/restore and concurrent access. Native
init is a genuine write, not proof of those paths. Normal serialization does not
prove crash/concurrency safety. No orientation/resumption benefit or successful
cross-team receipt is claimed before genuine use.

No synthetic tests were created or run; each would need specific owner approval.
09B enrollment and subsequent real assignments can naturally exercise mutations;
an absent receipt case does not prevent this bounded delivery. **No known repair
remains, but actual receiving defects stay with Pipeline until received or
explicitly dispositioned.** Advisory's next action is real 09B enrollment, not
another approval request. Older index/status pointers saying “pilot undelivered”
are for Advisory to reconcile during resumption. No commits, pushes, product
installation, production activation or runtime restart occurred.
