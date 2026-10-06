# CK3Chronicle — Trekker consultant review packet

2026-10-03. This single document combines the advisor's reply, the full investigation, and the relevant supporting plugin documentation content. External documentation is summarized and cited, not reproduced verbatim. It is a review snapshot, not activated project instructions.

## Advisor reply

My recommendation is **Trekker plus a small CK3Chronicle helper, starting with a CLI pilot**. The consultant's proposal addresses the continuity problem better than additional Markdown ledgers.

The substantive findings are:

- The producer/receiver model can use one existing Trekker task, with tags, comments and dependencies; no fork is needed for that vocabulary.
- A helper is needed to reconstruct team-specific actionable state consistently.
- Shared access needs protection: static inspection found a possible concurrent ID-allocation race. It was not reproduced experimentally.
- The stock Codex plugin should be deferred until its Windows launch paths and access coordination are resolved.

The installation command and Python-venv distinction are in section A below. The owner's immediate choices are whether to approve a protected CLI pilot, which real tasks to enroll, and who maintains the tooling. No installation, activation or synthetic test was performed.

## Full investigation

2026-10-03. **Recommendation only.** The owner's attached assignment governs
this review; the earlier [working-practices review](AGENT_WORKING_PRACTICES_REVIEW.md)
remains a proposal. Nothing here activates instructions, team assignments or tooling.

## A. Recommendation

**Adopt Trekker plus a thin CK3Chronicle adapter, initially as a bounded CLI pilot.**
Its existing records can represent producer/receiver obligations without a fork.
The adapter should derive team views, make checkpoints easy, and serialize access.
Defer the stock Codex plugin and dashboard until their access paths can use that
same protection. Unrestricted concurrent use is not yet justified.

The consultant's central correction is sound: live obligations should be queried
from one record, rather than reconstructed from several Markdown summaries.
This revises my earlier recommendation to keep those obligations in the current
handoff. Retain Markdown for authorization, contracts and durable evidence.
Keep Learner, Pipeline, Watcher and Data Intelligence; research is a shared
workflow, and advisory review remains optional.

The qualifications are concrete: team views need a helper, source inspection
identifies a possible concurrent ID-allocation failure, and the Codex plugin
does not supply team-specific recovery. These are inspected capabilities and
limitations, **not locally reproduced runtime results**.

**Installation command, for the owner to run:** Trekker is a Bun/JavaScript
application, not a Python package. It cannot be installed with pip into our
Python `.venv`. Install it separately as development tooling. This PowerShell
command uses the npm executable confirmed on this machine and works from any
starting directory:

```powershell
& 'C:\Program Files\nodejs\npm.cmd' install --global bun '@obsfx/trekker@1.11.0'
```

This installs tooling only. Node v24.19.0 is present; Bun was not found on PATH.
The manifest requires Node >=18 and Bun >=1.0.0; both projects document npm
installation. The command was **not executed**, and the registry package contents
were not independently verified.
[Trekker installation](https://github.com/obsfx/trekker),
[package manifest](https://raw.githubusercontent.com/obsfx/trekker/main/package.json),
[Bun installation](https://bun.com/docs/installation).

## B. Existing capability map

“Supported” below means documented and/or inspected in source, not locally exercised.

| Need | Finding | Fit for CK3Chronicle |
|---|---|---|
| Persistent records, IDs, priorities, epics/subtasks | Directly supported in local SQLite | Reuse; no new schema |
| Active/closed work | Native task statuses: `todo`, `in_progress`, `completed`, `wont_fix`, `archived` | Convention needed: implementation completion does not close a delivery |
| Producer, receiver, component | Comma-separated tags; no dedicated identity/assignee fields | Exact tag conventions, interpreted by adapter |
| Dependencies/blockers | Dependency links, cycle checks and ready query | Reuse links; expose unresolved prerequisites in team view |
| Continuation and evidence links | Task descriptions and authored, timestamped comments | Append concise checkpoints; link existing artifacts |
| Change history/search | Change events with snapshots/diffs; full-text search | Useful recovery; history is not authenticated approval or immutable audit |
| Incoming/outgoing team views | No native team/tag list filter; tags are not in the full-text index | Thin adapter required for dependable exact filtering |
| CLI/structured output | CLI and `--toon` output; ordinary task output is formatted text | Decode TOON; do not assume an undocumented JSON flag |
| Agent/Codex access | Separate plugin: 26 MCP tools, ten Skills, one startup hook | Available, but requires Windows/access-path work before adoption |
| Session resume | Hook queries in-progress/ready work, displays one branch, and includes recent history | Insufficient for team identity, pagination and per-item continuation |
| Human UI | Separate optional dashboard, sharing the database and permitting edits | Defer; writes would bypass pilot serialization |
| Receipt enforcement, authorization, perfect crash capture | Genuinely absent | Conventions and visible limits; no autonomous coordinator |

Primary evidence: [schema](https://raw.githubusercontent.com/obsfx/trekker/main/src/db/schema.ts),
[task commands](https://raw.githubusercontent.com/obsfx/trekker/main/src/commands/task.ts),
[dependencies](https://raw.githubusercontent.com/obsfx/trekker/main/src/services/dependency.ts),
[history](https://raw.githubusercontent.com/obsfx/trekker/main/src/commands/history.ts),
[search](https://raw.githubusercontent.com/obsfx/trekker/main/src/services/search.ts),
[output handling](https://raw.githubusercontent.com/obsfx/trekker/main/src/utils/output.ts),
[Codex plugin](https://github.com/obsfx/trekker-codex),
[startup script](https://raw.githubusercontent.com/obsfx/trekker-codex/main/scripts/session-start.sh),
[dashboard](https://github.com/obsfx/trekker-dashboard).

**Secondary comparison:** Todolist MCP has SQLite/SQLModel, a Python MCP server,
an explicit project directory, tag filtering, dependencies/ready queries and an
optional FastAPI/HTMX board. Its statuses are `open`, `in_progress`, `done`,
`cancelled`. These are attractive simplifications, particularly the project path.
However, I found no documented chronological comment/change-history facility,
Codex startup hook, or task-management CLI independent of its server entry point.
That leaves more continuation machinery to build. Retrieved source/documentation
snapshots differ in age, so newer implementation remains possible. It is not a
materially better fit here. [Todolist MCP documentation](https://github.com/wdm0006/todolist-mcp),
[Python packaging](https://raw.githubusercontent.com/wdm0006/todolist-mcp/main/pyproject.toml).

Conventions alone leave repetitive state reconstruction. A fork adds release
maintenance; a custom tracker duplicates storage/history/dependencies. Neither
is justified by missing domain vocabulary. If protected CLI access is unacceptable,
defer adoption pending a satisfactory concurrency fix.

## C. Producer/receiver mapping

**Proposed workflow example only; no record or CK3 evidence was created.**
Use one top-level task for “Deliver retained learner package to Pipeline.”

| Element | Proposed representation |
|---|---|
| Identity | One Trekker-generated task ID, used by both teams |
| Stable participants | `producer:learner,receiver:pipeline` tags |
| Authorization | Description links the owner assignment and relevant release/API contract; identifies authorized repair scope |
| Work being produced | `in_progress`; no handoff tag yet |
| Implementation/delivery | Learner appends `Delivery:` with artifact identity, actual evidence, limits and next receiver action; adds `handoff:pending` |
| Receiving failure | Pipeline appends `Receipt: changes required` with observed defect, responsible component and repair authorization; replaces tag with `handoff:changes` |
| Continuation | `Checkpoint:` comment: completed / stopped at / next / evidence limits / files or artifacts |
| Receipt | Pipeline records usable consumer behavior or explicit evidence gap; replaces tag with `handoff:received` |
| Closure | `completed` only when authorized scope and assigned follow-ups are dispositioned and required receipt/owner acceptance is recorded |

The task remains open awaiting receipt: Learner's outgoing and Pipeline's incoming
views show the **same ID**. Changes required retain the original obligation.
A repair assigned to another team gets a linked task with that team as producer;
the delivery depends on its disposition and subsequent receipt. Discovery alone
never authorizes the receiver to repair upstream.

Record activation, verification and owner acceptance as dated facts/evidence links.
Receipt with a gap does not assert verification; required unfinished work remains
open unless explicitly dispositioned. `wont_fix`/`archived` require a reason and
do not mean receipt. Tags and comment authors do not confer authority.

## D. Team session-state reconstruction

Proposed startup: read normal project guidance and the assigned prompt, then run
one `team-state learner` command and inspect the selected task's linked contract
and latest checkpoint. Establish the assigned task ID from the owner prompt;
do not guess it from whichever item happens to be “ready.”

The helper retrieves every page of top-level tasks, selects exact tag tokens,
and fetches comments/dependencies for relevant records. Keep all pilot obligations
top-level: Trekker's `task list` explicitly excludes subtasks. A later decision
to use subtasks must add their public enumeration path, not silently omit them.
[Task listing implementation](https://raw.githubusercontent.com/obsfx/trekker/main/src/commands/task.ts).

| View | Derivation for team T |
|---|---|
| Owned work | Open tasks with `producer:T`, including work awaiting assignment decisions |
| Incoming action | `receiver:T` and `handoff:pending` |
| Outgoing unresolved | `producer:T` and `handoff:pending` or `handoff:changes` |
| Blockers | Dependencies of relevant open tasks, with prerequisite disposition and next responsible actor |
| Continuation | Latest `Checkpoint:`, delivery/receipt notes and evidence links; missing notes explicitly shown |
| Owner decisions | Relevant records tagged `needs-owner`, with the exact decision in a comment |
| Closed work | Bounded recent closed records, retaining closure reason and evidence limits; older history on demand |

The same query takes `pipeline`, `watcher` or `data-intelligence`. Owned work
includes received items awaiting acceptance/activation. Surface malformed records;
“no work” is valid only after complete successful pagination.

Do not rely solely on `ready`: it selects top-level `todo` tasks and treats
`completed`, `wont_fix` and `archived` dependencies as resolved. It therefore
misses active receiving work and cannot establish whether a cancelled prerequisite
actually satisfies the consumer. [Ready query](https://raw.githubusercontent.com/obsfx/trekker/main/src/services/ready.ts).

## E. Minimal CK3Chronicle-specific layer

Propose one small Node module at `tools/work_state/cli.mjs`, its tooling-only
`package.json` and lockfile. Reuse the TOON decoder rather than inventing a parser;
pin a compatible version with the selected Trekker version. No Python runtime
dependency, database reader, schema change, persistent view cache or MCP server.
[TOON API](https://toonformat.dev/reference/api).

Three interfaces are sufficient:

1. **`team-state TEAM`**: the derived view above, including timestamps and incomplete-read warnings.
2. **`record ID --kind checkpoint|delivery|receipt --note-file PATH`**, with optional
   receiving disposition: append the note and adjust handoff tags while preserving
   other tags; reread the task under the access lock before changing it.
3. **`trekker <arguments>`**: protected access to ordinary create/show/update,
   comments, dependencies and history, using upstream CLI semantics. Routine use
   excludes destructive wipe/delete operations; these are not needed for the pilot.

Implement a single shared access lock around the complete helper operation,
including child completion. A conservative exclusive lock directory is sufficient
for the local pilot if abandoned locks fail visibly and are cleared only after
confirming every writer has stopped. Do not auto-expire a live writer's lock.
Launch the published CLI entry with an explicit executable/argument array on
Windows; avoid composing shell commands from task descriptions. Decode `--toon`
and return compact JSON/text to Codex. Resolve the installation entry from the
package's declared `bin`, not imported Trekker service internals.

Scope is one module and three commands; launching, pagination, decoding and locking
still require implementation and verification. Codex can use CLI directly; later
MCP access must call this helper. Name a tooling maintainer for conventions/upgrades;
Data Intelligence is a plausible assignment, not assigned here.

The CLI needs no long-running daemon. MCP adds a server process while connected;
CLI and MCP can reach the same backend when configured with the same working
directory, but that alone does not coordinate concurrent access.
[CLI and integration model](https://github.com/obsfx/trekker).

## F. Repository/instruction changes

Reuse existing authoritative orientation: Learner's
[nested guide](../tools/template_learning/AGENTS.md), [release contract](RELEASES.md)
and [matcher API](SHARED_MATCHER_API.md); Pipeline's [07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md);
Watcher's [playset](WATCHER_ACTIVE_PLAYSET_HANDOFF.md) and
[ingestion wiring](WATCHER_INGESTION_WIRING_HANDOFF.md) references; Data Intelligence's
[08 scope pointer](TASK08_SCOPE_REVIEW.md) and current reporting handoffs.
No four new team-guide files are needed. Data Intelligence does not acquire
Pipeline persistence ownership.

If adopted, add a short work-state section to `docs/DEVELOPMENT_ENVIRONMENT.md`
covering commands, canonical location, tag/note meanings and recovery. Add only
navigation and execution rules to root `AGENTS.md`: load state at startup/resume;
record delivery, receipt and meaningful pause/closure; preserve authorization;
use the shared helper. Preserve the owner's rule exactly:
**Each synthetic test requires explicit owner approval before creation or execution.**

Future prompts carry team, task ID, authorized outcome and receiver. Handoffs retain
technical evidence; plan retains milestones; status retains readiness/restrictions;
current handoff retains checkout hazards and continuation pointers. Only enrolled
pilot tasks move their live state to Trekker. Do not rewrite historical authorization
or maintain duplicate live inventories.

This addresses a concrete observed problem: the [08B receiving review](TASK08B_RECEIVING_REVIEW.md)
now records the traversal repair as delivered and removes its earlier repair
assignment, while preserving older findings. A fresh session needs the current
disposition, its authorization and evidence link, not the obsolete conclusion.
These results are reported project evidence; this investigation did not rerun them.

## G. Operational and durability concerns

**Concurrency is the main qualification.** ID allocation increments a counter
then reads it separately, without a surrounding transaction. Concurrent processes
can obtain the same ID and encounter insert failures. SQLite statement locking
does not make the sequence atomic. This is static reasoning, not a reproduced
failure or a claim of corruption.
[ID generator](https://raw.githubusercontent.com/obsfx/trekker/main/src/utils/id-generator.ts),
[task service](https://raw.githubusercontent.com/obsfx/trekker/main/src/services/task.ts).

Initialization has no explicit WAL setup, busy timeout or application retry queue;
even reads can initialize tables/config. Serialize **all** access. Raw CLI and
separate MCP processes otherwise bypass the protection. Also avoid simultaneous
editing of one record and reread before updates: serialization does not resolve
conflicting intent. [Database client](https://raw.githubusercontent.com/obsfx/trekker/main/src/db/client.ts).

**Location:** `.trekker/trekker.db` is relative to process working directory.
Use one ignored directory in the canonical checkout, selected explicitly by the
helper. All worktrees use that store, with sandbox permission where necessary;
never silently initialize per-worktree copies. An adjacent directory adds sandbox
configuration. [Location implementation](https://raw.githubusercontent.com/obsfx/trekker/main/src/db/client.ts).

**Backup/recovery:** after delivery sessions and before upgrades, stop clients and
copy the complete state directory to the owner's backup location, recording the
tool version. Restore with clients stopped. Git does not protect ignored state;
copying only the main SQLite file during writes is not the proposed backup method.

**Codex suitability:** the hook invokes `.sh`; MCP uses `execFile('trekker', ...)`
and process working directory. Node says Windows `.cmd` launchers cannot run that
way. This is an npm/Windows compatibility concern, not a reproduced failure.
Executable paths, working directory and hook commands need validation.
[Plugin runner](https://raw.githubusercontent.com/obsfx/trekker-codex/main/mcp-server/src/cli-runner.js),
[hook configuration](https://raw.githubusercontent.com/obsfx/trekker-codex/main/hooks.json),
[Node Windows behavior](https://nodejs.org/api/child_process.html#spawning-bat-and-cmd-files-on-windows).

Official hooks support session events and Windows overrides. A later hook could
surface `team-state` with explicit session/team binding; the stock plugin supplies
neither that binding nor a stop checkpoint hook. Start with guided queries and
transition checkpoints; add automation if the pilot shows omissions.
[Codex hooks](https://learn.chatgpt.com/docs/hooks),
[plugin documentation](https://github.com/obsfx/trekker-codex).

**Interrupted updates:** append the transition note before updating tags; these
are separate calls, so surface mismatches. After a crash, reconcile saved notes,
history and actual files/Git changes. Do not infer acceptance or blindly repeat a
possibly committed create/append. Unrecorded work remains unknown. Comments are
editable/deletable; append-only use is a convention.
[Comment operations](https://raw.githubusercontent.com/obsfx/trekker/main/src/commands/comment.ts).

**Maintenance:** retrieved pages show core v1.11.0 at `3f2ac99` and the separately
maintained Codex integration at `e156488`, both April 10, 2026. These snapshots
cannot exclude newer activity. Pin the pilot version and reassess upgrades.
[Core history](https://github.com/obsfx/trekker/commits/main/),
[integration history](https://github.com/obsfx/trekker-codex/commits/main/).

## H. Licensing

| Project | Focused finding |
|---|---|
| `obsfx/trekker` | MIT; [license text inspected](https://raw.githubusercontent.com/obsfx/trekker/main/LICENSE) |
| `obsfx/trekker-codex` | Independently MIT; [license text inspected](https://raw.githubusercontent.com/obsfx/trekker-codex/main/LICENSE) |
| `obsfx/trekker-dashboard` | README declares MIT; standalone license file could not be retrieved, so distribution review remains incomplete. [Project](https://github.com/obsfx/trekker-dashboard) |
| `wdm0006/todolist-mcp` | MIT; [license text inspected](https://github.com/wdm0006/todolist-mcp/blob/main/LICENSE) |

These are open-source offerings. The inspected MIT terms permit internal use and
modification without requiring publication of modifications; retain copyright and
permission notices in copies/substantial portions. This is a reading of the stated
terms, not an assurance about every dependency or redistribution scenario.

Trekker's direct dependencies include TOON, Commander, Day.js and Drizzle. Drizzle
is Apache-2.0; Bun's own code is MIT but its binary incorporates JavaScriptCore and
other components with additional terms, including LGPL. Do not describe the entire
runtime bundle as MIT-only. Separate internal tooling use is the proposed scope;
redistributing a modified/bundled runtime merits a specific review. No full
transitive dependency or registry-artifact audit was performed.
[Dependencies](https://raw.githubusercontent.com/obsfx/trekker/main/package.json),
[Drizzle license](https://raw.githubusercontent.com/drizzle-team/drizzle-orm/main/LICENSE),
[Bun component licenses](https://raw.githubusercontent.com/oven-sh/bun/main/LICENSE.md).

## I. Proposed next implementation assignment

**Draft only; requires a separate owner assignment:**

> Implement the bounded Trekker CLI pilot described here using the reviewed core,
> one canonical ignored store, and the three helper interfaces in section E.
> Keep all enrolled obligations top-level. Use public CLI operations and a pinned
> compatible TOON decoder; serialize every access, disclose interrupted transitions,
> and document Windows launch/backup/recovery. Do not fork Trekker, change its schema,
> add MCP/dashboard/hooks, or change CK3Chronicle runtime code.
>
> Enroll only the owner's named real tasks, including one actual producer/receiver
> delivery. Preserve assignment and evidence links. Make the minimal approved
> instruction changes in section F. Demonstrate a fresh specialist session recovering
> current work, incoming/outgoing obligations and the next action from those records.
> Observe real delivery and receipt; do not manufacture a defect or runtime history.
> Each synthetic test requires explicit owner approval before creation or execution.
> General permission to test is insufficient. Report unexercised behavior explicitly.
>
> After two real session resumptions and one receiving cycle, report owner corrections,
> omitted follow-ups, startup effort and bookkeeping effort in the pilot handoff.
> The pilot succeeds if both teams see the same unresolved delivery until receipt,
> fresh sessions recover the next action without owner reconstruction, and updates
> replace duplicate narrative maintenance. Stop expansion if maintaining the adapter
> or access discipline costs more than it saves. Do not claim concurrency resilience
> from source inspection or serialize-only observations.

The owner decisions are therefore narrow: approve this CLI pilot or defer it;
name its tooling maintainer and real tasks; and accept the single protected access
path while broader concurrency and Windows plugin behavior remain unverified.
No implementation, installation, synthetic test or production action occurred in
this investigation. Only this report was added.

## Supporting plugin documentation and source detail

The following is a cited digest of the content relevant to this recommendation. **Documented behavior**, **source inspection**, and **advisor interpretation** are distinguished. These external instructions do not authorize installation, workflow changes or tests in CK3Chronicle.

### 1. Upstream plugin workflow and installation model

**Documented behavior:** The integration assumes persistent Trekker state. Its workflow calls for searching and reading the existing record before changes, marking active work, leaving a checkpoint when pausing, and recording a summary before completion. It requires Bun, a global Trekker CLI, Node 18+ and Codex local-plugin support. Installation is described as cloning or linking a home-local plugin and registering it in a local marketplace. The Node server runs from source without a separate build. Updates require restarting Codex. The README also proposes a scratch-task verification exercise; it was not executed here. [Upstream README](https://github.com/obsfx/trekker-codex).

**Advisor interpretation:** The checkpoint workflow is useful, but its completion convention must preserve CK3Chronicle's receiving obligations. The README's Unix-oriented installation examples are not a verified Windows installation procedure. Its sample verification exercise does not override the owner's requirement for specific approval before creating or executing any synthetic test.

### 2. Package boundaries

**Source inspection:** The plugin manifest separately points to its Skills directory, hooks configuration and MCP configuration. It is an integration package around the Trekker CLI, rather than a replacement tracker or CK3Chronicle runtime component. [Plugin manifest](https://raw.githubusercontent.com/obsfx/trekker-codex/main/.codex-plugin/plugin.json).

**Advisor interpretation:** Installing the Trekker CLI with the command in section A does not also install or enable this Codex package. The proposed pilot deliberately uses the CLI through a project helper; plugin adoption would be a subsequent decision.

### 3. Exact startup behavior

**Source inspection:** The hook matches startup, resume, clear and compaction events and invokes a relative shell-script path. No Windows-specific override or stop/session-end handler is present in that configuration. [Hook configuration](https://raw.githubusercontent.com/obsfx/trekker-codex/main/hooks.json).

The script checks for the CLI and a `.trekker` directory in its working directory. It queries active tasks, ready work and five recent history entries. It displays active-task output when nonempty, otherwise ready output, then history. Query errors are suppressed. It does not supply team filtering, per-task checkpoints or pagination traversal. [Startup script](https://raw.githubusercontent.com/obsfx/trekker-codex/main/scripts/session-start.sh).

**Clarification of the original reply:** The hook does not display both work lists together. It queries both and displays one branch. The capability table in this packet uses this more precise wording.

**Advisor interpretation:** Checking whether formatted command output is nonempty does not establish that its task collection is nonempty. This branch condition needs verification before relying on the fallback. A failed query must not be interpreted as proof that a team has no outstanding work. Neither concern was reproduced locally.

### 4. MCP launch and backend selection

**Source inspection:** MCP configuration launches Node with a relative server-entry path and does not specify a working directory. The runner delegates to the Trekker executable, requests TOON by default, uses the process working directory unless overridden, and applies a 30-second timeout. It returns command output or an error result; the runner does not introduce a shared project lock. [MCP configuration](https://raw.githubusercontent.com/obsfx/trekker-codex/main/.mcp.json), [CLI runner](https://raw.githubusercontent.com/obsfx/trekker-codex/main/mcp-server/src/cli-runner.js).

**Advisor interpretation:** CLI and MCP reach the same store only when their effective project directory is aligned. Adding MCP does not repair a race inside concurrent CLI invocations. Any later integration must preserve the helper's canonical location and serialization boundary.

### 5. Task-query surface

**Source inspection:** Task tools expose standard task operations. Creation and updates accept tags, while listing offers task-status/epic filtering and pagination rather than producer, receiver or team parameters. [Task-tool definitions](https://raw.githubusercontent.com/obsfx/trekker-codex/main/mcp-server/src/tools/task.js).

**Advisor interpretation:** A team view can be derived from public task data, without adding producer/receiver columns to Trekker. Exact tag parsing and complete pagination remain the helper's responsibility. Natural-language search should not be assumed to supply a complete team inventory.

### 6. Windows process-launch issue

**Documented platform behavior:** Node's direct process-execution API cannot launch Windows batch/command scripts as ordinary executable files; an appropriate command interpreter or executable entry point is needed. [Node child-process documentation](https://nodejs.org/api/child_process.html#spawning-bat-and-cmd-files-on-windows).

**Advisor interpretation:** The plugin's direct Trekker launch is a compatibility concern where npm supplies a Windows command shim. This does not prove every Windows installation fails. The actual installed entry point, Bun executable, PATH and working directory must be checked during an authorized pilot. The recommendation is to use explicit executable/argument handling, not to interpolate arbitrary task content into a shell command.

### 7. What official Codex documentation supports

**Documented Codex capability:** Hooks support session lifecycle events, including startup/resume and session-end events. Command hooks support a Windows override and execute with the session's working directory. These capabilities could support a project-specific state loader, but do not establish that Trekker's current plugin implements one. [Official hooks documentation](https://learn.chatgpt.com/docs/hooks).

Plugin hooks must be reviewed and trusted; enabling a plugin alone does not establish that its hooks will execute. Official packaging guidance documents plugin-root variables for locating bundled scripts and supports the compatibility manifest used by this plugin. [Official plugin packaging documentation](https://developers.openai.com/plugins/build/plugins).

**Advisor interpretation:** A later hook could load an explicitly selected team's state through the same helper. It still needs reliable team/task binding, bounded output and an explicit failure result. Automatic context loading cannot recover work that was never recorded.

### 8. License and evidence limits

The Codex integration has its own MIT license. Its terms permit use and modification while retaining the required notices; it does not require publication of internal modifications. Dependency/runtime licensing is discussed in section H. [Plugin license](https://raw.githubusercontent.com/obsfx/trekker-codex/main/LICENSE).

This packet combines repository review, retrieved primary documentation and static source reasoning. It does not claim successful installation, exercised hooks, live MCP behavior, concurrent-access verification, or proof of crash recovery. The original standalone investigation remains unchanged; this packet incorporates the startup-display wording clarification described above.

## Questions for the consultant

1. Does the proposed helper remain proportionate once Windows launching, complete pagination and serialized access are included?
2. Is a protected CLI pilot a reasonable adoption condition, or should adoption wait for an upstream concurrency fix?
3. Does one record with producer/receiver tags and receiving notes preserve accountability without excessive bookkeeping?
4. Is instruction-driven startup/checkpointing sufficient for the first pilot, before adding a session hook?
5. Are there specific source findings that change this conclusion, especially an existing supported team-query, transactional allocation or Windows integration path?

These are review questions, not implementation authorization.
