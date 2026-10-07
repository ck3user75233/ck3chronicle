# Development environment

The ck3chronicle checkout on this machine is:

`C:\Users\nateb\Documents\ck3chronicle`

The source repository is:

`https://github.com/ck3user75233/ck3chronicle.git`

The managed workspace permits work in this checkout. Local runtime evidence is
kept in ignored application directories and is not source code. Captured CK3
logs, SQLite databases, pending copies, review material, workbooks, and
generated evaluation results must remain outside Git.

## Python

Use the repository environment for agent-run development and verification:

```powershell
Set-Location 'C:\Users\nateb\Documents\ck3chronicle'
$python = (Resolve-Path -LiteralPath '.\.venv\Scripts\python.exe').Path

& $python -B -m unittest discover -s tests -v
& $python -I -B -c "import ck3chronicle; import ck3chronicle.cli"
& $python -I -B -m pip check
```

If `.venv` fails, diagnose or restore it as part of the task. Optional
owner-created environments are not required for routine verification.

## Runtime safety

Consult `docs/PROJECT_STATUS.md` before running commands that capture evidence,
write to the production database, process pending captures, start the watcher,
or change configured runtime roots. Ordinary compilation, imports, unit tests,
and read-only inspection should be performed by the agent doing the work.

## Trekker CLI pilot

Pipeline's bounded pilot is installed and its canonical store initialized.
Source is under `tools/work_state/`. Exact setup, invocation/request fields,
verification limits and Pipeline's receiving responsibility are in the
[pilot handoff](TREKKER_CLI_PILOT_HANDOFF.md).

The manifest pins Trekker 1.11.0, Bun 1.3.10, TOON 2.1.0, Commander 13.1.0,
Day.js 1.11.19 and Drizzle ORM 0.38.4, with Bun Windows x64/baseline packages
1.3.10. Installation used Node 24.19.0/npm 11.17.0; the full dependency graph and
integrities are in `tools/work_state/package-lock.json`. Protected initialization,
TOON decoding and empty task/epic/history/team-state reads succeeded. Mutation
and populated-state behavior await genuine enrolled work; no synthetic tests ran.
The canonical store is
`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state`,
with native `.trekker\trekker.db` beneath it. This whole
ignored directory is retained work state, **excluded from disposable cleanup**.
All sessions/worktrees require access to that same location; never create copies.

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot help
& $pilotNode $pilot team-state pipeline
```

Use only that protected route for every read/write. Its bounded operations cover
tasks, minimal epics, comments/checkpoints, dependencies, history and
delivery/receipt. Prepared work awaiting owner issuance uses native `todo`, with
owner issuance as its recorded next action. Meaningful deliveries share one
producer/receiver record; receipt tags do not erase follow-ups or authorize work.

The shared lock has no automatic expiry. An incomplete operation blocks writes;
inspect actual state/history before retrying anything that may have committed.
Recover a lock only after verifying all relevant clients/children are stopped.
Back up/restore the complete canonical directory with clients stopped and the
same lock held, preserving versions and recovery evidence. Use the handoff's
procedure; crash recovery, concurrent access and backup/restore are unexercised.
Product configuration, runtime roots and Python dependencies are separate.

### What to retrieve from Trekker

Use Trekker to answer: **What has another team delivered or asked of me that
affects my assigned work?** It should let you recover the handoff without asking
the owner to relay another chat. Query it when starting/resuming, before consuming
another team's output, and before recording receipt or closing a delivery.
It provides information when queried; it does not notify or wake chats.

| Where to look | What to retrieve and do with it |
|---|---|
| `team-state TEAM` → `active` | Your owned open work, stopping points and follow-ups. Select the owner's assigned record, not a replacement task from this list. |
| `incoming` | Another team's delivered output awaiting your receipt. Read its evidence, interface/artifact references, limits and requested receiving action. |
| `outgoing` | Your delivered work still awaiting a receiver or returned for changes. Read the receiver's response and identify what remains yours to do. |
| Assigned record → comments | Coordination requests from other teams, shared-file ownership, prepared patches and later decisions—not just your own checkpoint. |
| Dependencies → `task-show ID` | Upstream delivery details and limitations you must account for before integration. An open predecessor may already have a usable interface with later receiving still pending. |
| Linked handoff/delivery material | Exact artifacts/pins, API changes and technical verification. Trekker points to this evidence; it does not replace it. |

Read the sequence of relevant comments. `latestContinuation` is the latest
checkpoint, while `latestRecordedAction` may be a later delivery or receipt.
For example, Learner's TREK-2 checkpoint preceded Pipeline's interface receipt:
both are valid, and the later receipt identifies what was received and what remains.
Do not rewrite an accurate earlier checkpoint or treat an old “awaiting receipt”
statement as overruling the subsequent receipt. If facts genuinely conflict,
identify the exact conflict rather than inferring an outcome.

Team lists are filtered views, not an exhaustive inbox for every mention of your
team. A received item can disappear from `incoming`; compatibility follow-ups may
be recorded in prose on another team's record. Open IDs named by your assignment,
dependencies and latest comments even when they are absent from your team's list.

For Task 09, Reporting should retrieve TREK-4's foreground-interface delivery and
receiving limits before integrating TREK-5. Pipeline should retrieve Learner's
coordination requests and artifact references on TREK-2/TREK-4, plus Watcher's
observer delivery on TREK-3. Use the existing protected invocation variables:

```powershell
& $pilotNode $pilot task-show TREK-4
& $pilotNode $pilot dependencies TREK-5
```

Apply retrieved information within the owner-issued assignment. Record which
delivery/request you consumed, the result and remaining action in the next
meaningful checkpoint or receipt; no per-read acknowledgment is needed. Reading a
request does not authorize new scope, and “implemented” does not mean “received.”
