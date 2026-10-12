# Task 10A — First-use design

2026-10-08. Owner: Launch & Distribution. **TREK-7: design proposal delivered
for Pipeline review; technical receipt pending.** Authority: [10A assignment](../task10-deliverables/10A_FIRST_USE_DESIGN.md)
and [Task 10 scope/sequence](../TASK10_DELIVERABLES.md). The Owner halted an
erroneous parallel 10A chat and confirmed this Launch & Distribution chat as owner.
TREK-8 is an archived duplicate, not a second assignment.

**Owner correction, 2026-10-08:** setup suggests and validates this user's paths,
requires individual acceptance, and saves editable configuration. External game/mod
files remain read-only. A config doctor must diagnose missing and suspicious setup
with practical consequences. The logs directory is an expected installation input;
only a current `error.log` may be absent during setup. These corrections supersede
the initial design's ambiguous path wording and limited doctor description.

This is an implementable proposal, not the installed manual. All setup, launcher,
global `--config` and `runtime-stop` commands below are **proposed**, awaiting
[Pipeline 10A.1](../task10-deliverables/10A1_PIPELINE_INTERFACES.md) agreement and
[10B](../task10-deliverables/10B_DISTRIBUTION.md) delivery. Existing report/watch
syntax is identified separately. No application or installer code changes in 10A.

## Baseline and concrete gaps

TREK-6 CMT-69 records completed Task 09 publication. Local HEAD and annotated tag
`task09-baseline-2026-10-07` independently resolve to
`709ea7842a0202c420b43355b18be91d8ca196a3`. Remote publication is the producer's
recorded receipt, not a fresh remote check by 10A. The [baseline](../TASK09_RELEASE_BASELINE.md)
supplies the exact wheel/dependency/Learner pins and genuine evidence:

- Application 0.0.1, wheel SHA-256
  `2dbb613de4fbac058a1ae2f429eea8adf2f85a1c861c859b89eaa0d5d62f1b1e`.
- Model package `2b12932103f3a3111a4e1880`, manifest SHA-256
  `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505`.
- Verified runtime combination: Windows x64 CPython 3.12.14, chardet 7.6.0.
  Production orders 9/10 are catalog sequence numbers, not application versions.

Current-source inspection and six actual help executions establish these gaps:

| Current interface | Consequence for first use | Implementation owner |
|---|---|---|
| `config.py` imports cwd/config.toml and evaluates module globals; no root `--config` | Select configuration before runtime imports; preserve config-free help | Pipeline |
| Writable roots must descend from the config directory | Deliberately revise containment for a data drive separate from LocalAppData and installed files | Pipeline |
| `repository.create_database` returns a schema/timestamp-named path; no setup command | Wrap validation/creation/persistence in one supported operation | Pipeline |
| Model catalog `selection --package` prints JSON; does not activate it | Persist an authenticated user choice outside immutable installed resources | Pipeline |
| Handler child receives only database path; shared identity is database-based | Propagate configuration and establish safe application/config change behavior | Pipeline |
| `runs` needs package ID; `report latest` does not consult active selection | Show copyable commands with explicit package or actual Run ID | 10B/Docs; Reporting retains semantics |
| `doctor` reports path existence and a writable probe, but does not establish CK3 identity or diagnose invalid setup comprehensively | Upgrade the existing command into a substantive config doctor sharing setup validators | Pipeline |

Help proves command inventory only. Evidence and source hashes are in ignored
`.codex-tmp/task10a-design-20261008/interface-evidence.json`, `help-0.txt` through
`help-5.txt`, and `interface-review.md`. No setup/ingestion/lifecycle was executed.

## Download and installation recommendation

Deliver a versioned **Windows x64 ZIP** with bundled runtime, application and
dependencies, `Setup.cmd`, `Start.cmd`, `ck3chronicle.cmd`, offline manual,
release manifest and notices. Extraction selects the installation directory;
recommend a user-writable programs folder. Routine execution treats installed
files as read-only. No Git, preinstalled Python, pip download or machine PATH
change is part of normal use. Setup does not register services or start observation.

Use `packaging/windows/` for 10B's outer recipe/launchers. Pipeline retains the
wheel, resource manifests, dependency closure and central runtime APIs. Recommend
evaluating a private CPython runtime with isolated module paths first. Python's
[embeddable distribution guidance](https://docs.python.org/3/using/windows.html#the-embeddable-package)
supports application-local runtimes and bundled third-party packages; it does not
prove this application's compatibility. 10B/Pipeline choose and pin the concrete
runtime archive after checking native dependency, SQLite and child-process support.
Prefer the verified 3.12 family where a supported redistributable is available;
do not assume a downloadable 3.12.14 embedding package exists or silently use a
different runtime. A changed runtime needs bounded compatibility verification.

The bundle must contain the received wheel's installed resources, retained
Learner entry point, model-administration entry point and an identified ripgrep
executable. Resolve runtime, modules, assets and tools from the bundle's absolute
location, including handler children; disable installation-tree bytecode writes.
Wire bundled ripgrep through the existing source-search interface. No developer
PATH/resource fallback. 10B owns archive/runtime/tool hashes and notices; Pipeline
owns application/model correspondence. `pyproject.toml` currently says license
`TBD`: a public distribution needs an Owner licensing disposition before upload;
local design/build can proceed. No public upload is part of 10A.

An extracted folder on the development machine is not clean-machine evidence.
10B/10C must test physically outside the checkout and disclose ambient dependencies.
This session's permitted writes are checkout-only: later external placement needs
an appropriately authorized environment; no such check is claimed here.

## User journey and representative prompts

The following is proposed interface text with illustrative paths/placeholders,
not a transcript of successful execution.

1. **Extract** the identified archive into a new versioned directory; open its
   short README and `Setup.cmd`. Choose the configuration destination, defaulting
   to `%LOCALAPPDATA%\ck3chronicle\paths.toml`, and a writable data directory,
   defaulting to `%LOCALAPPDATA%\ck3chronicle\data`. Show both expanded paths.
2. **Choose and confirm each path.** Offer the bounded Steam and Windows Documents
   suggestions below for the CK3 `game`, workshop, local-mod, logs and crash
   directories. Let the user browse or type any actual location. Validate the
   candidate's purpose, show the full path and findings, then require a separate
   Yes/Accept for that field even when automatically found. An existing directory
   alone is not proof of a CK3 installation. No selected root is inherited from
   the developer's machine or silently accepted from a suggestion.
3. **Confirm the model.** Show application release/build identity, shipped model
   package/manifest identity and available compatible installed packages. Recommend
   the authenticated shipped default; advanced users can choose another available
   approved package. No training or editing selection JSON.
4. **Review and apply.** Display resolved paths, planned directory/database creation,
   model choice, automatic-ingestion and retention settings. The user chooses Apply.
   Pipeline validates all inputs first, initializes only when appropriate and
   persists the exact returned database filename. Display the resulting config,
   database, review/pending/log locations and model identity. Do not print Ready
   until creation and configuration persistence have succeeded.
5. **Observe.** Open `Start.cmd` (fixed bootstrap) or use the explicit command below.
   Keep its foreground window open, start CK3 and later exit CK3 normally. Explain
   that starting observation may process existing protected pending captures when
   ingestion is enabled; maintenance uses the displayed retention settings.
   Missing `error.log` during setup is normal. Capture requires a genuine completed
   log; a failed capture/ingest must remain visible rather than become an empty Run.
6. **Stop observation** with Ctrl+C in that window. Existing watcher shutdown waits
   for its dispatched work/outcomes before releasing its lease; do not promise an
   immediate return. Stopping observation does not end CK3 or stop the independent
   database handler. Do not claim a completed lifecycle if observation was interrupted.
7. **Read results.** List the selected package's stored Runs, choose an actual Run ID,
   then render a report. An empty history is a normal result until ingestion succeeds.
   Reports read stored diagnostics; optional source context uses current read-only
   sources and can be unavailable. Explain unresolved evidence as a separate native
   review shard linked to the Run, not a missing diagnostic row.

Representative review screen:

```text
Configuration: C:\Users\Example\AppData\Local\ck3chronicle\paths.toml
Writable data: D:\CK3ChronicleData
Model package: 2b12932103f3a3111a4e1880 (manifest authenticated)
Database: create once; show and save the returned filename
Automatic ingestion: on   Raw retention: 30 elapsed days, checked every 24 hours
No current error.log: observation can be configured before the first run
Apply setup? [Yes/Cancel]
```

Each external path has its own preceding confirmation, for example:

```text
CK3 game directory (suggested from the Windows Steam location):
C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game
Check: game content and adjacent CK3 executable found.
Use this location? [Y] Yes / [E] Edit / [B] Browse / [C] Cancel
```

The final Apply confirms the changes as a whole; it does not replace these individual
acceptances. On repeat setup show saved values first; check and confirm the displayed
external paths again in the guided flow. Routine runtime commands do not reprompt.

## Path suggestions and meaningful configuration diagnosis

Every external root is a user-editable configuration value. Only paths **inside
the application bundle** have a product-defined layout. Game, workshop and personal
folders may be on different drives and need not be related to the installation,
configuration file, data directory or one another. Setup saves the user's accepted
locations; it never creates, moves or edits the external game/mod/log contents.

Use these initial candidates, not mandatory layouts:

| Field | Candidate to offer/check |
|---|---|
| `root_game` | `<Program Files (x86)>\Steam\steamapps\common\Crusader Kings III\game` |
| `root_steam` | `<Program Files (x86)>\Steam\steamapps\workshop\content\1158310` |
| `root_local_mods` | `<this user's Documents>\Paradox Interactive\Crusader Kings III\mod` |
| `root_logs` | `<this user's Documents>\Paradox Interactive\Crusader Kings III\logs` |
| `root_crashes` | `<this user's Documents>\Paradox Interactive\Crusader Kings III\crashes` |

Resolve the user's actual Documents folder through Windows
[`SHGetKnownFolderPath`](https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/nf-shlobj_core-shgetknownfolderpath)
with `FOLDERID_Documents`; obtain `FOLDERID_ProgramFilesX86` through the same
[Known Folder facility](https://learn.microsoft.com/en-us/windows/win32/shell/knownfolderid).
Use the current folder location, including redirection, without creating it.
Do not construct Documents by concatenating a username or assume the system drive.
If resolution fails, ask the user for the location. A user-supplied alternative
drive, Steam/library directory or full path gives additional bounded candidates;
game and workshop locations are confirmed independently. No recursive disk scan.

Suggestion lookup is confined to setup and has no authority until accepted. Normal
operation and doctor inspect the saved paths; they never search for replacements
or silently repair them. This Owner-approved setup assistance qualifies older
blanket no-root-discovery wording; exact configuration-file selection is unchanged.

**Config doctor:** retain and improve `ck3chronicle --config PATH doctor`, sharing
the same semantic checks used by setup. It should answer what is missing, what
looks wrong, how the finding affects use, and how to correct it. A parseable TOML
file or an existing folder is insufficient for a healthy finding. Missing/invalid
configuration must produce useful diagnostics rather than fail during import;
run independent checks where possible and label dependent checks unavailable.

| Check | Expected diagnostic behavior |
|---|---|
| Config file and fields | Identify exact missing/unreadable file, invalid TOML or absent/malformed field; suggest setup/editing that exact configuration |
| CK3 game identity | Check readability and CK3-specific evidence, such as adjacent `binaries/ck3.exe` together with expected game content; show observations. An arbitrary folder or another Paradox game must not pass just because it exists |
| Workshop and local mods | Check saved paths/readability and applicable content; explain unavailable mod context. No installed/subscribed mods is not itself an error |
| Logs directory | Expect an existing readable CK3 logs directory. If missing or implausible, identify the path and explain that capture cannot read logs there; check the installation/user-data location. Do not present it as a normal ready first-use state |
| Current `error.log` | Distinguish missing file from missing directory. Absence alone does not block setup; capture needs an actual completed log |
| Crash directory | Report absence without asserting a crash or blocking ordinary operation |
| Data/database/model/tool settings | Report containment/access concerns, missing or incompatible configured database, model authentication/availability and required tool availability; explain which operation is affected |

Pipeline must ground game-identity checks in genuine supported layouts. In the
current actual installation, `game/common`, `game/events`, `game/map_data` and
adjacent `binaries/ck3.exe` were observed read-only; this is evidence for checks,
not proof that every distribution has identical internals. An unrecognized layout
gets an explicit warning/unknown result and corrective guidance, not a confident
claim that CK3 is absent. Confirmed invalid required paths prevent Ready status;
suspicious or optional findings stay visible and are not hidden by Yes/Accept.

Doctor displays per-check healthy/warning/error/unverified findings with evidence,
impact and next action, plus a summary. It does not change settings, create external
directories, initialize a database or start a handler. If a property cannot be
established read-only, report it unverified; a directory-exists check must not claim
write access. Setup may perform its bounded application-data write checks when
applying changes. Doctor is diagnosis, not a new automatic repair system.

Illustrative diagnostic (not an executed test):

```text
WARNING root_game: D:\Games\OtherGame exists, but CK3 could not be identified.
Expected CK3 game content / adjacent binaries\ck3.exe were not found.
Impact: CK3 source context may be unavailable or use the wrong files.
Action: choose the Crusader Kings III game directory in Setup and confirm it.
```

After setup, proposed wrapper/global-config syntax combined with **existing**
watch/runs/report options (replace paths and Run ID with actual setup/output):

```powershell
$app = 'C:\Apps\CK3Chronicle-<release>\ck3chronicle.cmd'
$cfg = 'D:\CK3ChronicleSettings\paths.toml'
$package = '2b12932103f3a3111a4e1880'
& $app --config $cfg watch
# Ctrl+C in the watcher window after the desired observation.
& $app --config $cfg runs --package-id $package
& $app --config $cfg report '<actual Run ID>' --preset frequent
& $app --config $cfg report latest --package-id $package --preset frequent --format html --output 'D:\CK3ChronicleData\reports\frequent.html'
```

`latest` needs its explicit package ID and uses Reporting's current eligible Run
selection; active model choice never silently supplies its scope. Named Run IDs
infer stored lineage. A completed manual-capture ingest remains a separate 10E
workflow; `watch --once` does not demonstrate an observed lifecycle or playset.

## One configuration authority and path contract

Pipeline resolves root `--config <path>` once before loading configuration-dependent
modules. An explicit relative config filename resolves from invocation cwd. With
no argument, use only the fixed LocalAppData file above. A missing/invalid explicit
file never falls back; if LocalAppData is unavailable, request an explicit path.
Normal operational commands require an existing valid file; help and first setup
do not. Doctor reports absent/invalid configuration as a diagnostic finding.

Paths **inside TOML**, including relative database paths, resolve from that file's
parent. CLI file operands/overrides retain documented invocation-cwd semantics and
are normalized before transport. Setup stores normalized absolute paths to make
the review unambiguous. No hidden environment/cwd source search or second config
file. Transition existing checkout users with explicit `--config <old config.toml>`;
keep supported keys and preserve their chosen paths, without retaining implicit
cwd/config.toml fallback. This task does not edit the owner's live configuration.

All path values below can be created/edited in configuration by setup or deliberate
user edits. The final column describes **filesystem contents**, not permission to
change the configured path.

| Setting/input | Required meaning and validation | Filesystem contents: who creates/changes them |
|---|---|---|
| `paths.root_game` | User-confirmed existing readable location, checked for CK3 identity | Game installation contents stay read-only to CK3Chronicle |
| `paths.root_steam`, `root_local_mods` | Independently confirmed workshop/local-mod locations; unused mod locations are disclosed, not fabricated | Steam/user-owned mod contents stay read-only to CK3Chronicle |
| `paths.root_logs` | User-confirmed expected existing readable CK3 logs directory; missing directory needs correction, current error.log need not exist | CK3 owns logs; CK3Chronicle reads/copies them and never fabricates them |
| `paths.root_crashes` | User-confirmed crash location; absence is not affirmative crash evidence | CK3-owned crash contents stay read-only to CK3Chronicle |
| `paths.root_wip` | Chosen writable data root, independent of configuration/installation location | Setup may create |
| `paths.root_ck3chronicle` | Runtime subtree, normally `<data>/runtime` | Setup/runtime |
| `paths.root_learner_state` | Separate subtree, normally `<data>/learner`; does not gate retained config-free Learner help/execution | Create only as required by setup/learner operation |
| `watcher.database` | Exact existing initialized database after setup | Pipeline creates once and saves returned path |
| `[watcher]` controls | Preserve ingest/retention booleans and positive maintenance-hours/retention-days; first-use defaults true/true/24/30 | Setup shows/preserves values |
| `[logging]` | Preserve shared backend fields/defaults | Only runtime_logging configures logs |
| Proposed `[model] package_id`, `manifest_sha256` | Persist authenticated explicit user selection; catalog maps ID to retained resources | Pipeline setup, in the same TOML authority |

Pipeline may refine the proposed model field representation during receipt, retaining
one explicit authority and immutable installed payloads. Installed shipped default
is the initial setup suggestion only; subsequent upgrades do not overwrite user choice.
An unavailable selected package is an actionable error, not a reason to substitute one.

Writable runtime/learner trees remain disjoint beneath the data root. Do not place
writable roots within or above installed files or configured CK3/mod/log/crash trees.
Resolve containment centrally, including paths that already exist; a launcher must
not bypass it. Separate data/config locations must be allowed. Validate external
readability where needed without turning absent optional evidence into a hard gate.

Every application child receives the canonical absolute config path explicitly.
The handler must use the same application resources and authority as its caller;
database identity alone does not establish compatibility. Pipeline defines the
small compatibility check/rejection needed for an existing handler with a different
configuration or application. No silent reuse or automatic restart. Retained Learner
execution remains configuration-independent, with explicit output/log destinations.

## Proposed technical surface for Pipeline receipt

Keep the launcher thin: it collects values, shows the Pipeline validation result,
and invokes the same operation available to agents. It does not write TOML/selection
JSON, initialize SQL, authenticate models or configure log handlers itself.

| Proposed surface | Contract |
|---|---|
| `ck3chronicle setup --suggest-paths --format json` | Config-free bounded candidates and validation observations; nothing accepted or saved |
| `ck3chronicle --config PATH setup --list-models --format json` | Config-free installed catalog/default inspection and available compatible choices; no config/database creation |
| `ck3chronicle --config PATH setup [inputs] --format json` | Read/merge existing settings with explicit inputs, validate and describe intended actions; no data/config mutation |
| Same command with `--apply` | Revalidate, apply supported changes, initialize if first setup and save exact resulting paths/selection; report effects |
| `ck3chronicle --config PATH doctor [--format json]` | Diagnose configured setup with per-check evidence/impact/action, including missing or invalid config; no automatic fixes |
| `ck3chronicle --config PATH runtime-stop` | Explicit maintenance stop using existing HandlerClient shutdown, after stopping observation; never start an absent handler just to stop it |

Proposed setup inputs: `--data-root`, `--root-game`, `--root-steam`,
`--root-local-mods`, `--root-logs`, `--root-crashes`, `--database` (explicit existing
file, including recovery), and `--package-id`. Omitted values preserve an existing
configuration; only first setup uses the defaults described here. The guided setup
can repeat these calls without maintaining a second settings file. For noninteractive
setup, propose repeatable `--accept-path FIELD` for each newly selected or changed
external root, alongside its explicit path input. No blanket `--apply` may accept
automatically found paths. The launcher supplies individual acceptances only after
the user's Yes/Accept for those fields. Pipeline can refine syntax without weakening
per-field confirmation. Retain existing
per-command `--database`, `--logs`, `--package-id` and output overrides as documented
operation scope; they do not implicitly rewrite persistent configuration.

Structured setup result: resolved config/data/runtime/database paths, model identity,
available choices when requested, validation errors/warnings, proposed/performed
actions and whether a process restart is required. On apply distinguish created,
preserved and failed effects. Return 0 for valid inspection/success, 2 for invalid
input/configuration and 1 for operational failure; existing command-specific exit
codes remain unchanged. For the improved doctor, propose 0 when there are no
warnings/errors/unverified checks, 2 when findings need attention and 1 if diagnosis
itself fails; JSON retains every finding's severity and meaning. This deliberately
changes the current doctor's always-success behavior and must be documented by
Pipeline. These are proposed semantics, not observed output.

Model/config changes apply to newly started affected processes. Before applying a
change that an active watcher/handler would retain, return an actionable in-use
result: stop observation, let its outstanding work finish, explicitly stop the
shared handler, then apply/restart. The maintenance shutdown stops admission and
may reject unfinished requests; it is not a guarantee every queued request commits.
No loss of protected evidence or historical Run lineage is permitted. New normal
requests start a handler through the existing mechanism; no OS service installer.

Repeat setup preserves database identity/content, captures, review shards, selected
model and user controls. It never resets, migrates, imports or reprocesses history.
Changing data root does not move existing state: show the existing paths and require
an explicit supported choice, or reject relocation as outside setup scope. On a
partial setup failure, report every created path and preserve prior configuration;
an explicit `--database <returned file>` can recover an initialized file after
configuration-save failure. Never search for a plausible database or claim success
after a failed save. Persistence/atomic-write mechanics belong to Pipeline.

## Useful errors and recovery

| Situation | User-facing action |
|---|---|
| No config | Name the exact attempted path; offer Setup.cmd or explicit --config |
| Invalid/unreadable or suspicious game path | Explain failed CK3 identity/readability checks and consequences; edit/reconfirm the field |
| Missing or suspect logs directory | Explain that capture cannot use that path; correct/reconfirm the location before claiming ready |
| No current error.log | Allow setup; explain that capture requires a genuine completed log |
| Absent unused mod/crash directory | Explain operation-specific unavailable context; do not invent installed mods or crash evidence |
| Data/config destination not writable | Name the failed destination and preserved/created effects; choose writable storage |
| Incompatible existing database | Leave it intact; explain schema mismatch and separate explicit reset decision; never auto-upgrade |
| Invalid/unavailable package or manifest | Preserve prior selection; choose an authenticated available package or correct distribution |
| Active runtime retains previous settings | Stop observation and use the explicit maintenance stop before applying |
| No stored Runs for requested package | Explain that capture/ingestion has not produced a matching Run; show correct package scope |
| Capture/ingest does not complete | Link actual journal/pending path and returned outcome; do not infer rollback/success from missing output |
| Missing bundled search tool | Report distribution defect; database-only reporting does not become fabricated source context |

## Acceptance and documentation mapping

These are required observable outcomes for the later issued assignments, **not
passed checks**. Use isolated configuration/storage, genuine evidence and normal
public-handler routes. Reuse valid unchanged evidence with exact correspondence.

| Journey | Concrete observation/evidence | Owner and manual input |
|---|---|---|
| Cold extraction/help | Actual bundle runs outside checkout without developer imports/runtime/PATH; help before config | 10B then 10C; 10D prerequisites/commands |
| Suggested external roots | Windows-derived/user-supplied candidates stay editable; each shows validation and requires individual acceptance; runtime uses only saved values | Pipeline validators and 10B interaction; 10C follows guide |
| Config doctor | Actual setup findings name check/evidence/impact/correction; CK3 identity exceeds directory existence; config/log-directory/log-file states are distinguished | 10A.1, then 10D/10E/10C; absent genuine cases remain unverified |
| First setup before live log exists | Exact path resolution, authenticated model, created database/schema and saved returned filename; no CK3/source writes | 10A.1 then 10B/10C; 10D config and 10E setup |
| Repeat setup | Same configured database and genuine stored contents, captures/review and choices preserved; no additional database | 10A.1/10C; 10E repeat/recovery |
| Explicit/default config and children | Fixed bootstrap or exact explicit file; same resolved authority/resources in foreground and handler from unrelated cwd | 10A.1/10B/10C; 10D precedence |
| Model inspection/change | Installed authenticated identities, persisted choice and effective next-runtime identity; historical lineage preserved | 10A.1/10C; 10D selection/10E workflow |
| Observe/stop | Received unchanged lifecycle evidence plus any necessary safe natural-session check for changed paths; actual journal/outcomes and stop boundary | Watcher evidence received by 10B/10C; Watcher contribution/10E |
| Genuine capture ingest/report | Capture hash and playset provenance, handler result, actual stored Run/record/count/shard facts and meaningful text/HTML report agree | 10A.1 evidence, 10B candidate, 10E/10C exercise; Reporting contribution |
| External data/review | Exact database/schema and supported read-only or consistent-snapshot procedure; meaningful SQL result; separate real shard viewing | Pipeline 10A.1 access contract; 10E then 10C |

Available baseline genuine G2 classification, retained Learner evaluation,
Reporting comparisons and Watcher capture/playset receipts are catalogued in the
[Task 09 baseline](../TASK09_RELEASE_BASELINE.md#build-basis-and-acceptance).
They do not prove new setup or cold installation. Preserve their original artifact
identities when reused. Choose actual captured logs/playsets through their owning
handoffs; do not invent new histories, timestamps or faults. Cases absent from
genuine evidence remain unverified. No synthetic acceptance is authorized by 10A.

10D receives component-authored references; 10E assembles/exercises workflows.
Record exact artifact/manual revision, command/input, expected/actual result and
relevant stored/file effects. Prefer copyable snippets, using genuine screenshots
for visual navigation. Help/screenshots alone cannot prove initialization or ingest.
10B supplies a usable candidate before Docs verification, then bundles the agreed
manual; 10C follows that exact final bundle. No circular manual/build dependency.

## Delivery, review questions and remaining owners

Pipeline's issued 10A.1 should record receipt/corrections on **TREK-7**, confirming:
(1) setup/model field and CLI shapes; (2) bootstrap/containment and child authority;
(3) initialization/repeat/partial-failure contract; (4) active-handler compatibility,
selection timing and maintenance stop; (5) wheel/resources/runtime boundary and
external SQLite access. Routine corrections can be agreed directly. These proposed
surfaces are not a demand to change Watcher/Reporting semantics. A needed component
change outside shared wiring gets an exact owner-issued continuation.

Launch & Distribution owns incorporation of that review and 10B preparation once
issued. Pipeline has not yet received this proposal; 10A remains in progress until
its required technical receipt. 10A.1 and sibling assignments were not enrolled or
dispatched by this work. No material first-use scope decision currently requires
Owner disposition; the public-license choice belongs before eventual publication.
Physical external placement and clean-machine claims remain later 10B/10C work.
