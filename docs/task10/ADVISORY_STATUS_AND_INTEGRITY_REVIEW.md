# Advisory — Task 10 status, production health and release integrity

Reviewed 2026-10-08, under the Owner-issued [review assignment](../TASK10_ADVISORY_REVIEW_PROMPT.md).
This is an Advisory finding and proposed continuation document, not implementation,
acceptance, dispatch or activation authority.

## Subsequent Owner-authorized operation — October 9, 00:57 HKT

The Owner subsequently instructed this chat to stop any current Watcher and start
the October 5 Watcher. That instruction separately authorized the operation below;
the initial read-only review did not authorize it. This update supersedes the
stopped-state conclusion below for the time of this new observation.

**The October 5 Watcher was started successfully at October 8 16:57:51 UTC /
October 9 00:57:51 HKT.** Fresh pre-start process inventories contained no identified
ck3chronicle Watcher or CK3; no existing process was stopped. Other visible Python
processes belonged to CK3Raven / Python 3.13 and were left running.

All 556 installed application/resource members were freshly compared with R3 wheel
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`.
The installed loader authenticated model `4ac4e8ee92346e6d14eacfbf`, manifest
`839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
The exact launch used `.codex-tmp/pipeline-r3-packaging-20261005/deployment/Scripts/python.exe`
with `-I -B -m ck3chronicle.cli watch`, project-root working directory and hidden
window. No configuration, selection, artifact or startup registration was changed.

Watcher launcher PID **35924**, start **16:57:51.4387612 UTC**; actual Watcher PID
**29088**, start **16:57:51.5357706 UTC**. Handler launcher PID **14540**, start
**16:57:51.9604613 UTC**; actual handler PID **2384**, start **16:57:51.9957369 UTC**,
instance **2c875ccbbe15493daf3d4aa420cf249b**. These are dated observations, not
permanent process identifiers. The existing configured database remains
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`.

At **16:58:24 UTC / 00:58:24 HKT**, both processes remained present; heartbeat
**16:58:21.976038 UTC** identified Watcher 29088, `state: absent`, 59 polls.
New logs contain Watcher started/ready and handler started/ready events. Normal
startup submitted 34 readable protected captures; all 34 returned existing Run IDs
and explicit duplicate warnings, with no ingestion errors. The 22 previously
inaccessible older inputs remained unavailable. No new CK3 lifecycle/capture has
yet been verified after this start. Ingestion and 30-day / 24-hour retention remain
enabled under the unchanged existing configuration.

Execution evidence: [preflight](../../.codex-tmp/watcher-start-20261009/preflight.json),
[launch](../../.codex-tmp/watcher-start-20261009/launch.json),
[verification and heartbeat](../../.codex-tmp/watcher-start-20261009/verification.json),
[process identities](../../.codex-tmp/watcher-start-20261009/processes-after.json).
That evidence directory also preserves the old heartbeat, pre-start process lists,
new Watcher/handler event excerpts and redirected stdout/stderr. The original
October 8 audit findings below remain historical evidence.

## 1. What the Owner can conclude

**The known operational installation is stopped in the observed process inventory,
and still contains the October 5 application, not Task 09 logging or Task 10.**
Its last heartbeat is October 5 23:52 UTC / October 6 07:52 Hong Kong time (HKT).
The reason and exact stopping time are unknown. There is no evidence here that
distribution work stopped it, or that an attempted Task 09 activation failed.
The accessible older logging route successfully recorded capture, requests and
ingestion. Missing Task 09 foreground journals in this installation are consistent
with its authenticated old executable bytes; they do not establish a logger defect.

**Task 09 logging was installed and successfully exercised.** This finding does
not dispute its received tests or production-release adoption. The installed
Task 09 baseline is `.codex-tmp/trek6-baseline-20261007/deployment`. Its retained
Learner journal records successful completion on October 7 at 08:03:44 UTC /
16:03:44 HKT. The same installation's `pipeline/catalog.py` executed the actual
production model registration successfully at 09:02:26 UTC / 17:02:26 HKT.
The distinction is that this installed release and its successful command
executions did not replace the bytes in the October 5 continuous-Watcher
installation identified above. A later continuous-Watcher cutover to Task 09
has not been established by the examined evidence.

Clarification checked October 9 against the actual journals:
[installed Learner execution](../../.codex-tmp/trek6-baseline-20261007/journals/learner-bfd079b9969c4f7cbec278ee371ff533.jsonl)
and [production registration](../../.codex-tmp/trek6-production-20261007/journals/model-release-27e8ea9cac6c4263b4934fc26d3d9848.jsonl).
The [Task 09 baseline](../TASK09_RELEASE_BASELINE.md#build-basis-and-acceptance)
also records received Reporting/public-handler logging evidence, including 65 real
request links. These are successful logging observations, not a missing test.

**CK3 activity occurred after that heartbeat.** A retained genuine October 8
distribution check observed CK3 already running. Current CK3 logs contain newer
evidence, and their current error-log hash has no Run in the configured operational
database. The operational Watcher has no corresponding later capture in its
accessible pending storage. This is a concrete coverage gap, with the unreadable
roots and unknown shutdown cause qualified below; it is not a count of all missed
sessions or authorization to reingest history.

**The pinned component bytes are intact in the examined release chain.** All 499
tracked retained model/Learner files equal the Task 09 commit byte-for-byte. Both
Task 10 wheels preserve all 450 retained members shipped in the Task 09 wheel.
All nine Windows candidate archives contain the original received 627-member
application wheel unchanged. No delivered application/retained-resource copy-only
repair bypass was found. External C9's current payload is unreadable here; its
successful owner-run authentication and installation receipts remain valid dated
evidence, not an independent fresh payload check by Advisory.

**Task 10 has useful, received components but is not ready for final acceptance.**
C9's external GUI installation is established. The corrected reference and 10E
guides are delivered but absent from that archive. The newer 1,024-result wheel is
delivered separately and has no Windows receiving receipt. Resume existing owners
for the bounded follow-ups below, finish the identified bundle, then issue 10C.
Do not reissue 10A, repeat C9 setup merely to record its existing success, or rebuild
the model because the outer packaging changed.

### Observation basis and limits

Advisory performed process/file inspection, full accessible log parsing, a short
SQLite `mode=ro` / `query_only` transaction, hashes, ZIP-member comparisons and
read-only Git comparisons. No product CLI, doctor, HandlerClient, retained worker,
build, runtime test, service operation or publication was executed. In particular,
`HandlerClient.submit()` calls `_ensure_started()`; ordinary public Run queries can
start a host. Source inspection established this before choosing direct read-only
SQLite for this operational audit, not a reporting acceptance campaign.

Evidence root **E** is
`C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/advisory-status-integrity-20261008/`.
It is ignored, local evidence. References to E below identify files there:

| Evidence | What Advisory actually inspected or recorded |
|---|---|
| `process-observation.json` | Timestamped `Get-Process` paths/start times; denied CIM command-line inventory recorded separately |
| `production-observation.json`, `observe.py` | Full accessible JSONL ranges/events, heartbeat, config hash, all 34 Run records, 56 pending-directory dispositions and current CK3 file hashes |
| `legacy-text-logs.json` | Existing root/watch stdout/stderr and both handler bootstrap logs, including excerpts and hashes |
| `integrity.json`, `integrity.py` | Four wheel identities, installed comparisons, retained identities, Git baseline, C1–C9 archives and C9 staged/source/transfer correspondence |
| `learner-source-map-correction.json` | Corrects an audit recorder's initially guessed nonexistent launcher-source path; actual `tools/template_learning/learner_loader.py` matches. No product failure or repair |
| `supplement.json`, `repair-path-supplement.json` | Catalog-field differences, current manual hashes, external receipt hashes, historical genuine CK3 observation and exploratory-copy inspection |
| `TREK-6.json` through `TREK-15.json` | Protected-helper snapshots, including all later comments and dependencies; archived TREK-8 preserved |

Initial process observation was **2026-10-08 15:37:06 UTC / 23:37:06 HKT**;
database/log observation began **15:39:34 UTC / 23:39:34 HKT**; artifact observation
began **15:41:26 UTC / 23:41:26 HKT**. Supplement times are in their evidence files.
These are dated observations, not a continuous monitor. The database's full SHA-256,
size and modification time were identical before and after the read.

The protected `team-state advisory` and complete `task-list` returned 15 records,
no enrolled Advisory review, and no 10C record. No tracker record was created or
edited. Absence of enrollment alone does not prove no private work occurred;
the prepared 10C prompt, index and refreshed comments also contain no delivery or
acceptance evidence. Component-authored documents and historical comments remain
untouched. No new team was dispatched.

## 2. Production identity and logging

### Distinct installations and identities

All relative paths in this report are relative to
`C:/Users/nateb/Documents/ck3chronicle`, unless an explicit external path is given.

| Layer | Established identity and disposition |
|---|---|
| Editable source | HEAD and annotated Task 09 tag resolve to `709ea7842a0202c420b43355b18be91d8ca196a3`; Task 10 application, catalogs, packaging and docs are uncommitted changes. The tag alone does not describe them. |
| Published source baseline | TREK-6 CMT-69 records verified atomic main/tag publication. Advisory verified local refs and retained blobs; no fresh remote query or hosted-asset inspection was performed. |
| Configured historical operational route | October 5 R3 environment `.codex-tmp/pipeline-r3-packaging-20261005/deployment`; launcher `Scripts/python.exe`; config `config.toml`, SHA-256 `d8fc8c5b36a7deae4b2e5217aed0d349b6d9a7899f3cebf4dc9577e21dbfb106`. All 556 installed code/resource members still equal R3 wheel `7239a0c5…` below. |
| Operational database/state | `.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3`; pending, review, watch and handler logging are beneath the same runtime root. Config keeps ingestion and retention enabled, 30 days / 24-hour maintenance. No settings were changed. |
| Operational selected model | Installed `deployment/share/ck3chronicle/models/selection.json` selects `4ac4e8ee92346e6d14eacfbf`, pin `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`. All stored Runs use that package. It is separate from the checkout/default Task 09 selection. |
| Task 09 isolated installation | `.codex-tmp/trek6-baseline-20261007/deployment`; all 620 code/resource members equal received wheel `2dbb613d…`. Published locally as the newest production release, but not thereby operationally deployed. |
| Task 10 application installation | `.codex-tmp/task10a1/release/deployment`; all 622 code/resource members equal wheel `2de516e0…`. Separate setup/processing evidence. |
| External C9 candidate | `C:/Users/nateb/AppData/Local/Programs/ck3chronicle-task10-c9`; separate `C:/Users/nateb/AppData/Local/ck3chronicle-task10-acceptance-c9/settings/paths.toml` and `data/runtime/ck3chronicle-schema3-20261008T120240Z.sqlite3`. Owner-run receipts identify private executable/import/resource paths. This is an acceptance installation, not a production cutover. |
| Actually running | The observed process inventory contains neither CK3 nor an executable under the operational environment, its CPython 3.12 base runtime, or C9. Visible Python processes are CK3Raven venv / Python 3.13 processes starting October 8 around 11:54–11:55 UTC. No present loaded Watcher/handler identity can be reported. CIM command lines/parentage were denied. |

The R3 venv uses CPython 3.12.14 from the Codex runtime, with system site packages
disabled. Its launcher SHA-256 is
`81bac8328c3df7c80a0915ea0baf01996355ebcc00ab6f8dbfefb4e60935e2bc`.
Its `runtime_logging.py` hashes to
`540e74f460c5ebf689ac76bff348e918c788893e139e621d499d59d7e899b844`;
it lacks Task 09's added `journal.py`. The received Task 09 executable closure
changes the logging backend, root/request/catalog and Reporting journal callers.
Current operational bytes and stored application lineage still identify R3
`application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d`.
No later operational activation receipt was found in the focused Task 09/10
handoffs and refreshed records. This supports **Task 09 not deployed to the known
operational installation**, not an assertion about every inaccessible installation.

### Last verified lifecycle and later game activity

The old [cutover record](../learner-next-release/PIPELINE_CUTOVER.md) describes the
initial 31-Run replacement. Fresh SQLite inspection finds **34 Runs**, not 31:
the subsequent October 5 Runs are `JW7JBR`, `Y1UHZL`, and `FJ0PS4` (each prefixed
`20261005-`). Latest facts are independently consistent across capture metadata,
Watcher log, handler log, file hash and stored Run:

| Event | UTC | HKT |
|---|---|---|
| Latest observed game start, CK3 PID 65512 | Oct 5 13:35:44.620 | Oct 5 21:35:44.620 |
| Source error.log modified | Oct 5 13:43:26.942 | Oct 5 21:43:26.942 |
| Observed exit, classified as crash with new crash folder | Oct 5 13:43:35.676 | Oct 5 21:43:35.676 |
| Capture metadata `captured_at` | Oct 5 13:43:35.701 | Oct 5 21:43:35.701 |
| Protected capture published | Oct 5 13:43:37.615 | Oct 5 21:43:37.615 |
| Stored processing timestamp | Oct 5 13:43:39.910 | Oct 5 21:43:39.910 |
| Handler / Watcher successful completion | Oct 5 13:43:40.034 / .113 | Oct 5 21:43:40.034 / .113 |
| Last persisted heartbeat, state `absent` | Oct 5 23:52:11.332 | Oct 6 07:52:11.332 |

Capture `20261005T134335.700594Z-91gNvhbq` has hash
`ca871b17e958193a70f7a873042fff3f0d62df3e0f8dd7d0faab6da7a2d00ecd`, Run
`20261005-FJ0PS4`. Request `a23d27ca9604453181f7d90bbb97c15e`, historical handler
instance `f474dbf7100a44399e2ae4a6a05f6375`, and historical Watcher 51024 / handler
54908 correlate. These are event identities, **not current process targets**.
Thirty-four readable captures all have matching stored hashes. Twenty-two older
pending directories (August 30–September 6) were access-denied and not retried.

The later genuine C3 check at **October 8 00:41:10 UTC / 08:41:10 HKT** observed
CK3 PID 36632, start time **October 7 23:24:42.812 UTC / October 8 07:24:42.812 HKT**.
Advisory read this existing receipt, not a newly executed game observation:
`.codex-tmp/task10b/verification-candidate3-final/watcher-check.json`.
That task Watcher was later explicitly stopped; it was not the operational Watcher.
The current process snapshot has no CK3. Thus there is real later-run and subsequent
absence evidence; its exact exit time/manner is not established.

Current live `error.log` is 7,534,322 bytes, hash
`226008bea0ae0246cef1b1d96b7633ff21a51fcaaaabbe02f9dc009d2c015d67`, modified
**October 8 00:55:58.933 UTC / 08:55:58.933 HKT**. It has no stored match and no
match among readable operational captures. `debug.log` begins with genuine log
initialization at 07:24:43 and ends with emissions at 08:55:38; those time-of-day
lines alone do not supply a calendar date or exit event. File modification,
source emission, capture and processing times have deliberately not been conflated.

The Owner was asked once whether the Watcher was deliberately stopped/rebooted and
whether CK3 ran afterward. Pending that reply and the bounded OS observation below,
do not attribute the stop to a defect, intentional shutdown or distribution activity.
Preserve the currently unmatched evidence before any separately authorized
operational change; this review has neither captured nor ingested it.

### Log search coverage and health conclusion

Advisory parsed every accessible `.jsonl*` in the configured runtime `watch/`
and `logging/` trees, including existing older names; no rotated siblings were
present in those trees. All parsed lines were valid JSON. The inventory records
each exact path, hash, event range and file modification time.

| Examined root / evidence | Actual coverage and interpretation |
|---|---|
| `.ck3chronicle/wip/runtime/watch/` | Ten JSONL files, event coverage Aug 11–Oct 5. Current `events-watcher.jsonl`: Sep 30 00:27:53.668–Oct 5 13:43:40.113 UTC, 773 events. Later heartbeat is a separate snapshot, not another journal event. |
| `runtime/logging/ck3chronicle-schema3-20260928T211854Z.sqlite3/` | 1,044 handler events, Sep 30–Oct 5 12:07:32.504 UTC; explicit shutdown belongs to the old-database cutover. Bootstrap log empty. |
| `runtime/logging/ck3chronicle-schema3-20261005T112504Z.sqlite3/` | 1,683 handler events, Oct 5 11:25:04.940–13:43:40.034 UTC; includes staged preparation and later operational instance, distinguished by instance/PID. No later shutdown event; empty bootstrap log. |
| Runtime root and `watch/` text logs | Existing Aug 10–Sep 28 stdout/stderr read. Historical invocation failure is August evidence, not an October failure. Old migrated paths in their text do not change current config authority. |
| Configured CK3 `logs/` | Listed current files, hashed error/debug/system/game; inspected debug endpoints/system contents. No game files edited. |
| C9 task evidence under `.codex-tmp/task10b/resume-20261008/` | Read actual setup and handler journals. C9 deliberately closes DB/stops handler at Oct 8 12:02:54.761 UTC / 20:02:54.761 HKT; receipt completes at 12:02:56 UTC. No C9 Watcher started in that check. |
| `C:/Users/nateb/AppData/Local/ck3chronicle` | Root enumeration denied; fixed bootstrap and older logs here remain unknown. No retry or alternate-access bypass. |
| External C9 Programs-directory manifest/payload | Direct manifest read denied; no descendant probing. Dated owner-run verification is credited, present external bytes remain unverified by Advisory. |

No whole-disk log search or inspection of every historic backup was performed.
The configured operational roots and existing earlier/rotated locations were the
bounded search. A quiet event journal while the heartbeat remains fresh and CK3 is
absent is not itself a failure. The stale heartbeat plus missing known-route
processes now supports a stopped route. **Observed historical logging worked;
present operational health is stopped, cause unknown; Task 09 deployment is absent
from the known installation.** A claim that all production logging is currently
healthy, or that its logger is broken, would exceed this evidence.

## 3. Task 10 status and next actions

The [issued index](../TASK10_DELIVERABLES.md), [working agreement](../task10-deliverables/WORKING_AGREEMENT.md)
and later comments govern; `handoff:received` does not erase follow-ups.

| Work / owner | Meaningful completed outcome and exact evidence | Actual remaining obligation; next actor |
|---|---|---|
| Task 09 / Pipeline, TREK-6 | Baseline received and source-published; CMT-69, [baseline](../TASK09_RELEASE_BASELINE.md), wheel `2dbb613d…`. Local tag independently verified. | Remains completed. Neither live activation nor a hosted wheel upload was included. Do not reopen for Task 10. |
| 10A / L&D, TREK-7 | Corrected design received by Pipeline, CMT-80; [design](FIRST_USE_DESIGN.md). | L&D can record closure and correct pending-receipt current prose. Later C9 healthy-default GUI choice supersedes old separate-click wording. TREK-8 stays archived. |
| 10A.1 / Pipeline, TREK-9 | Original wheel `2de516e0…` received CMT-83; [handoff](PIPELINE_HANDOFF.md). Cache follow-up source/wheel `94987fb0…` delivered CMT-126, [cache handoff](REQUEST_RESULT_CACHE_HANDOFF.md). | Pipeline disposes of CMT-106 stale ingest-help and GUI-reference wording. L&D must receive the newer application in the next candidate; CMT-83 does not receive it. Keep open for these specific obligations, not old generic receipt/placement wording. |
| 10B / L&D, TREK-10 | C9 GUI/external setup and 1,492-payload checks received CMT-91. C4 genuine Run/report/repeat evidence read back; [distribution handoff](DISTRIBUTION_HANDOFF.md). | Finish upstream runtime/tool correspondence and matching notices; consume final application and corrected 10D/10E freeze; build a newly identified bundle. Then actual 10C receipt on this record. Existing C9 need not be reinstalled. |
| 10D / L&D Docs, TREK-11 | Six canonical reference pages, inventory, three component receipts; genuine installed example 1,066 records / 1,838 occurrences. CMT-114/116/125; [handoff](DOCUMENTATION_HANDOFF.md). | Refresh CMT-126 delivery status; settle CMT-106/122 facts, freeze against exact next bundle, obtain 10C manual receipt. C9's 256 statement remains accurate. |
| Watcher contribution / Watcher, TREK-12 | CMT-96 received CMT-109 into canonical CLI/config pages; [contribution](WATCHER_DOCUMENTATION_HANDOFF.md). | Later CMT-122 requests correction of disable-retention advice and identification of separately Owner-requested unavailable-result reconciliation. Correct technical prose and resolve that delivery/assignment pointer before closing; do not silently commission code under the documentation task. |
| Reporting contribution / Data Intelligence, TREK-13 | CMT-101 received CMT-110 with no producer correction; [contribution](DATA_INTELLIGENCE_CONTRIBUTION.md). | Producer may close received documentation scope and correct current description. Final manual acceptance is TREK-11/10C, not another Reporting obligation. |
| Learner contribution / Learner, TREK-14 | CMT-104 received CMT-111 with no producer correction; [contribution](LEARNER_DOCUMENTATION_HANDOFF.md). | Producer may close received documentation scope and correct current description. No training/release repair required by this audit. |
| 10E / L&D Docs, TREK-15 | `10E-r1` guides and image delivered CMT-117/118; combined-freeze agreement CMT-119/120; [handoff](WORKFLOWS_HANDOFF.md). Real SQL and separate nonempty shard evidence available. | Consume later corrected reference, preserve guide identity, include in new bundle and obtain 10C receipt. No duplicate ingestion to recreate the existing example. |
| 10C / L&D | [Prepared acceptance assignment](../task10-deliverables/10C_ACCEPTANCE.md); no enrollment/delivery found. | Owner issues when final candidate/manual are usable. Follow exact installed guides; record receipts on TREK-10/11/15 and changed Pipeline delivery on TREK-9. |

### Exact convergence inputs

C9 is ZIP `db1ed81f…`, manifest `066ae6f7…`, application `2de516e0…`, reference
`10B-reference-2026-10-08-r7`. Its archive contains only
`docs/user/DISTRIBUTION_REFERENCE.md`, `docs/user/PIPELINE_REFERENCE.md` and the
Pipeline handoff, plus `INSTALL.md`. It does **not** contain the subsequently
authored canonical manual or 10E guides. C9 manifest's pre-installation limits are
dated artifact text; later successful CMT-91 receipts supersede their operational
status without authorizing an in-place archive edit.

Current 10D content is pinned by `.codex-tmp/task10d/evidence/manual-hashes.json`,
SHA-256 `e140384be10aa680eefb1fd0f776f1ff0c091a447f1b1d86f95c9a6f4c2bd64f`.
All ten listed files match. 10E-r1 delivery manifest hashes to
`b1b346abf92ff294ea1cae9edb952b2b86ba5560f36b830aed0300368e1d3154`; all six
authored-file hashes match. Its evidence reference to the earlier 10D hash manifest
is historical: CMT-124/125 deliberately corrected that reference after the freeze
offer. Consume the new reference hashes, not the earlier combined-freeze snapshot.

Before the final bundle: include the Owner-selected 1,024-result application change
and any CMT-106 source correction in an authenticated wheel; settle the separately
requested Watcher recovery's actual assignment/delivery/release disposition; finish
provenance/notices; freeze the corrected canonical manual plus guides/image; then
authenticate a new bundle. No automatic Watcher reconciliation was found in current
`watcher_processing.py`: `LookupError` records `ingestion_outcome_unavailable` and
removes tracking; it does not call stored hash lookup. CMT-122/125 identify separate
Owner-requested work, but supply no implementation record/artifact. This is an
unresolved pointer/delivery, not permission for Advisory to create an implementation
commission. If intended for this release, receive it before freeze; otherwise record
the Owner's actual separate-release disposition rather than quietly dropping it.

Recommended order: **(1)** finish the bounded operational observation independently;
**(2)** resume Pipeline's specific TREK-9 follow-ups and Watcher's CMT-122 disposition,
while L&D finishes provenance and Docs correct current text; **(3)** L&D/Docs agree
the final application/manual and build a fresh bundle; **(4)** issue 10C; **(5)**
separately decide Owner acceptance, source publication/hosting and live activation.
No Advisory approval gate or relay of existing technical evidence is needed.

10C must credit completed physical external placement; the remaining stronger
clean-Windows/no-preinstalled-dependency claim is still unverified. Ordinary-console
graceful Watcher stop is also unverified; the managed-terminal failure is not yet
a diagnosed product defect. Handoffs call for a fresh lifecycle, but the issued
10C prompt expressly permits unchanged lifecycle evidence reuse. The receiver must
assess changed paths and exact correspondence, identifying any necessary natural
session and safe timing, rather than adding an unconditional repeated lifecycle
campaign. A competing production Watcher, forced game exit, synthetic history or
unseen error case is not an acceptance requirement.

### Proposed current-text corrections (not applied)

| Owner | Precise correction / closure basis |
|---|---|
| L&D, TREK-7 | Replace “Pipeline receipt pending / Owner issues 10A.1” with “Received CMT-80; design complete”; close 10A, leave duplicate TREK-8 archived. |
| Pipeline, TREK-9 | Replace original pending-receipt description with original CMT-83 receipt plus CMT-106 obligation and CMT-126 newer-wheel awaiting consuming receipt. Do not erase CMT-82 history. |
| L&D, TREK-10 and current pointers | Remove present-tense claims that 10D/10E are unissued and physical external installation unperformed. Cite CMT-91, TREK-11/15 and CMT-124; retain provenance/final-bundle/10C gaps. Correct owned r7 input's stale external-check statement only in a new document/bundle revision. |
| Docs, TREK-11 | Change “Pipeline source only/no artifact yet” to “CMT-126 wheel delivered, not installed/received into C9.” Keep C9 256 versus next candidate 1,024 distinct. |
| Watcher, TREK-12 | Record CMT-109 receipt, then resolve later CMT-122. Remove the unsolicited disable-retention recommendation; intentional independent 30-day retention remains. |
| Reporting / Learner, TREK-13/14 | Record CMT-110/111 receipt and close their completed contribution scope; keep later concrete correction responsibility without retaining generic pending status. |
| L&D coordination, project plan/status/handoff/index | Current Task 10 pointers should acknowledge deliveries, actual external placement and fresh 34-Run operational observation; preserve dated older statements. No component evidence overwrite is proposed. |

## 4. Pinned-component and release-process findings

### Independent authentication

| Component | Authoritative identity and result |
|---|---|
| Full model package | `2b12932103f3a3111a4e1880`; external manifest `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505`; all 14 payloads match. Recomputed package identity equals SHA-256 of canonical manifest excluding `package_id`, truncated to 24 hex digits. Baseline manifest itself is unchanged. |
| Compact model | Revision `3bc531d578074e6a430c161e`; payload SHA-256 `3afde7def3a056f16e3699e814ee217d71e46aced0ce2cb19eb395a8fc6a685b`. Recomputed revision equals canonical model without `revision_id`; parser and owner-rules declarations agree. |
| Parser | `ck3-lossless-v1.8`; `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135`. Editable parser, retained copies and wheel/bundle members correspond; parser manifest/model/package references agree. |
| Matcher / selector | `ck3-native-matcher-v3` / `complete-assignment-v2`; native matcher `fe559adf9349d2fe83f50a0b000a14f00630a591684cdeeeead44d99efe52caa`; assignment `29e3bc8f54ac678988a3dc3e0023ce7c1dc76403900a44805ef958fbd47be235`; authenticated bootstrap `53168c6f84d17ca3a2d856e0b0248be3d78ab45e183937f5b2c9c50c441ce472`. Corresponding owning editable sources match. No independent invented selector pin. |
| Retained Learner | Release `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`; external manifest `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e`; all 48 payloads match. Recomputed canonical manifest identity excluding `release_id` agrees. |
| Learner algorithm identity | `outer-diagnostic-consensus-v61`; recomputed fingerprint `67f881e22dfec7477ee2fe423a1c9789285acab6825c2b78fa3065996bcd52a9` includes implementation and shared implementation hashes. Owning editable closure matches, including launcher after the documented recorder mapping correction. |
| Retained shared backend / adapter | `ck3chronicle/runtime_logging.py`: `aa22fb1b13b03c3661d6872298ef875fc9f6f08e21bf2c0fb5caadd81d49bf65`; `journal.py`: `b48a1fde03f31e7e8d42e91a0f114fc15ed239afecbd265cabbd0412ecc2e8cc`. Both equal editable application source, retained payloads and received wheel/bundle copies. Decoder closure also matches `19c4e46e5f4a6377f348901aecf5be87b69dabf2dc93e178168f864e70a2e227`. |

These checks compare against the received Task 09 wheel **and** Git retained blobs,
not merely a regenerated adjacent manifest. All 499 retained Git files match;
450 retained wheel members match across Task 09, original Task 10 and cache wheel.
All 622 original Task 10 source inventory paths match the latest wheel; the only
current source change since original delivery is `pipeline/database_handler.py`.
This is byte/identity verification, not fresh model evaluation or functional testing.

Selection/catalog differences are intentional and bounded. The Task 10 packaged
catalogs change only `publication_status`, `production_order` and
`publication_evidence` on the already-adopted latest model/Learner rows (orders 9/10).
Model and Learner row counts remain 12 and 8. Retained paths, identity pins, prior
rows and packaged selection bytes are unchanged. The known operational default
remains the older package; intact pins do not imply the newest component is active.

Static loader inspection shows model bootstrap/payload authentication before
execution and retained Learner imports restricted to its authenticated closure.
C9 `python312._pth` names only its private runtime/Lib/DLLs/site-packages.
The inspected installed `Lib/models` and `Lib/learners` shadow roots are absent;
normal model lookup therefore reaches installed `share/ck3chronicle/models`.
External C9's actual prior handler receipt names that installed root and selected
pin. This review did not execute a new loader, so it does not replace those dated
runtime receipts or establish in-memory identity of an inaccessible alternate route.

### Artifact identities

| Artifact | Full SHA-256 / location |
|---|---|
| October 5 operational R3 wheel | `7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`; `.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl` |
| Received Task 09 wheel | `2dbb613de4fbac058a1ae2f429eea8adf2f85a1c861c859b89eaa0d5d62f1b1e`; `.codex-tmp/trek6-baseline-20261007/application/ck3chronicle-0.0.1-py3-none-any.whl` |
| Original Task 10 / C1–C9 wheel | `2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`; `.codex-tmp/task10a1/release/application/ck3chronicle-0.0.2-py3-none-any.whl` |
| New cache wheel | `94987fb06eeac685eb5b57a87edc41e58da1df9730ff8bf15ba7a023750ab489`; `.codex-tmp/pipeline-cache-1024/application/ck3chronicle-0.0.2-py3-none-any.whl` |
| C9 archive | `db1ed81f050e13c93652681e829c18ef282a92965c116aee0fc59cea49eedfc1`; `.codex-tmp/task10b/build/ck3chronicle-0.0.2-task10b-candidate9-win-x64.zip`, 20,909,122 bytes |
| C9 manifest | `066ae6f7378372074c575cd9c5c8e75257c809ec65575526a0fee7979f9f4aa5`; staged at `.codex-tmp/task10b/READY_TO_MOVE_C9/ck3chronicle/release-manifest.json` |

All nine archive hashes equal their separate saved receipts; every manifest-listed
payload in each archive matches. Each contains all 627 original application ZIP
members, including metadata, unchanged. The staged C9 has all 1,492 listed payloads
plus its manifest, with no extra files. Its build recipe and input-plan hashes
match current `packaging/windows/build.py` and `inputs/plan-candidate9.json`.
Launcher, Windows Forms script, GUI adapter, placement/check helpers and their
transfer pins correspond to owning source. No source-to-wheel or wheel-to-bundle
discrepancy was found in that closure.

### Issue → source → artifact → receiving trace

All candidate paths below use `.codex-tmp/task10b/`; full hashes and changed member
lists are in E/`integrity.json`. Later source incorporates the delivered outer
fixes. None of these deliveries establishes live activation.

| Issue / authority / owner | Exact changed source or copy; new identity | Evidence, receipt and disposition |
|---|---|---|
| New configuration/setup/handler authority, issued 10A.1 / Pipeline | Owning `src/ck3chronicle/{cli,config,doctor,setup}.py`, `pipeline/{catalog,database_handler,repository,request_handler,runtime_identity}.py`, version and packaging catalogs. Fresh original 0.0.2 wheel `2de516e0…`. | `task10a1/release/artifact.json` maps source/wheel/install; CMT-81 delivery, CMT-83 L&D receipt. 592 unchanged components/resources reported by producer; Advisory independently compared complete closure. No production deployment. |
| Redirected encoding / 10B / L&D | `packaging/windows/launcher.py`, builder-generated CMD `-X utf8`, installation guide. C1 `30e3e42e…` → C2 `86f70955…`. | `verification-candidate2/`; genuine setup/ingest/report/stop receipt CMT-83. Application wheel unchanged. |
| Editable data-root suggestion / 10B / L&D | `packaging/windows/launcher.py`, `docs/user/DISTRIBUTION_REFERENCE.md`; C3 `ac7672a0…`. | `prepare3.py`, `inputs/plan-candidate3.json`, `verification-candidate3-final/`, CMT-84/85. Genuine local checks; later external C3 receipt establishes copy/entry only. |
| PS5.1 execution-policy and unavailable Get-FileHash / owner-run helper repair / L&D | `packaging/windows/Place-And-Verify.ps1` uses .NET SHA-256; process-only invocation documented. Transfer helper copies/hash control refreshed by `verify3.py`/`finalize.py`. | Failed original transcripts retained in `verification-candidate3/` and `verification-candidate3-retry/`; later helper inspection and actual owner-run receipts. This is source-incorporated helper repair, outside the immutable application/archive payload. |
| Installation location, fresh/existing-state wording, Watcher terminology / Owner feedback / L&D | `packaging/windows/{launcher.py,Place-And-Verify.ps1,INSTALL.md}` and distribution reference; C4 `79478764…`. | `ux-correction/before/`, commands/verification, CMT-86; external result later CMT-89 and `single-setup/`: Run `20261008-P8KHM4`, reports, repeat preservation. |
| Avoid asking user to name TOML file / Owner feedback / L&D | `packaging/windows/launcher.py`, reference; C5 `337c783f…`. | `simple-setup/{before,commands.json,verification.json}`; first/repeat preservation. No separate C5 external execution claimed. |
| Show actual folder findings; hide technical acceptance flag / Owner feedback / L&D | Same owning launcher/reference and `INSTALL.md`; C6 `1cc412d3…`. | `path-findings/{before,commands.json,verification.json}`, CMT-88; no application-validator replacement. |
| Explain/remove mandatory second setup / Owner feedback / L&D | `packaging/windows/{Place-And-Verify.ps1,external_check.py}` adds explicit `-VerifyRepeatSetup`, receipt distinction; staged single-setup helper. | `single-setup/before/`; C9 external receipt confirms once-only path, C4's actual repeat remains separate. Current C9 transfer helper hashes equal owning source and pins. |
| Native Windows GUI / Owner request / L&D | `packaging/windows/{Setup.ps1,setup_gui_backend.py,launcher.py,build.py}`; C7 `41345076…`, C8 `8579e888…` changes only generated `Setup.cmd` for visible help. | `gui-setup/final-checks/verification.json`, screenshots, `candidate8-correspondence.json`, CMT-89. Discarded Tk prototype under `gui-setup/working-bundle/setup_gui.py` equals retained `tk-draft.py`, absent from C9. All 627 application members in that exploratory copy also remain intact. C8 external check cancelled, not passed. |
| Numbered steps, plain fixed paths, healthy folders selected / later Owner instruction / L&D | `packaging/windows/Setup.ps1`, `INSTALL.md`, reference r7; C9 `db1ed81f…`. | `wizard-flow/{before,checks}`, CMT-90; actual external C9 receipt CMT-91, read back by Advisory. No new application/model identity required. |
| 256 → 1,024 completed results / explicit Owner follow-up / Pipeline | Authoritative `src/ck3chronicle/pipeline/database_handler.py`; fresh wheel `94987fb0…`. Only handler, METADATA and RECORD differ from original 0.0.2. | CMT-126; `pipeline-cache-1024/{artifact.json,verification.json,build.py}`. Producer reports 1,027 genuine operations; Advisory authenticated bytes, did not rerun them. No new installed/bundle receipt or activation. |
| Help/default and GUI reference discrepancy / Docs CMT-106 / Pipeline | `cli.py` ingest `--package-id` help still says catalog default while configured model governs; contribution has obsolete GUI confirmation description. | Concrete follow-up remains open. Correct owning source/reference; if wheel code changes, deliver another authenticated wheel before final bundle. No repair performed here. |
| Retention correction and final user manual / Owner correction, 10D/10E / Docs | Canonical `docs/user/` pages and image; CMT-124/125 supersede older reference hashes. | Current authored hashes verified. Still outside C9; new outer bundle required. This does not require a new model/Learner release. |

**Copy-only finding:** exploratory GUI copies and mutable transfer-helper refresh
scripts exist. They are not evidence of a patched retained release. The prototype
was not shipped; the delivered helper and all substantive delivered outer changes
have owning source correspondence. Current C1–C9 archives, received wheels and
retained releases show no in-place payload drift against independent pins.
The helper scripts explicitly copy source into existing transfer staging and update
`TRANSFER.json`; those transfer documents are distinct from the pinned application
and archive. Existing files establish the route and final correspondence, not a
complete transcript of every exploratory edit. No source/release reconciliation
repair is justified on present evidence. Preserve prior artifacts; if the bounded
external read finds a divergence, reconcile that exact copy through its owner.

Provenance remains a real 10B obligation. CPython 3.12.14 and ripgrep 15.2.0 are
identified local snapshots; hashes alone do not establish upstream origin or
complete native/PCRE2/Rust notices. The prepared download-only acquisition route
has not produced `.codex-tmp/task10b/upstream/` in this observation. Its absence and
the current receipt leave upstream comparison unverified; no download was attempted
by Advisory. Dependency replacement would require a new bundle and affected checks,
not automatically a new trained model. The application license remains `TBD` for
separate public-publication disposition; this review supplies no legal conclusion.

## 5. Bounded continuations ready for Owner use

These are proposals to resume existing scope or obtain missing observations.
Saving them has not issued work or authorized activation.

**Read-only observation — Owner session, then Pipeline/Watcher interpretation.**
The only presently inaccessible observations needed to tighten this review are
current process command lines/parent/start identities, the fixed bootstrap/legacy
log root, and fresh external C9 payload correspondence. The prepared helper reads
only those locations and emits JSON. It imports no product, opens no DB and starts
no service. PowerShell syntax was parsed successfully; execution is unperformed.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\nateb\Documents\ck3chronicle\.codex-tmp\advisory-status-integrity-20261008\Owner-ReadOnly-Observation.ps1'
```

It compares external C9 to the already received manifest pin and hashes all 1,492
payloads, without invoking its CLI/Verify. Access failure remains an explicit
result; no permission repair is attempted. This command is requested because
Windows denied those exact reads in the managed session, not because authorized
read-only review needs another generic approval. Answer the pending stop/reboot
question to distinguish deliberate inactivity from an unexplained stop. Existing
Trekker receipts need not be recopied or relayed by the Owner.

**Documentation correction / bounded application defect — resume Pipeline TREK-9.**
“Read this review, CMT-83, CMT-106 and CMT-126. Preserve the received C9 wheel and
cache-wheel originals. Disposition the exact ingest-help/configured-default and
GUI-reference discrepancies in your owning source/reference. If application bytes
change, deliver a fresh authenticated wheel incorporating the already delivered
1,024-result change, with source/resource correspondence and affected evidence.
Coordinate directly with TREK-10/11 and obtain actual consuming receipt. Do not
rebuild/re-pin unchanged models, change production or reopen Task 09.”

**Documentation correction / assignment-status clarification — resume Watcher TREK-12.**
“Consume CMT-109 and later CMT-122. Correct your contribution's disable-retention
recommendation to the Owner's intentional independent 30-day behavior. Identify
the actual separately Owner-issued unavailable-result reconciliation assignment,
its current state and delivery/artifact, if any; current source/C9 do not implement
it. Return the exact record/handoff or explicit missing-assignment fact directly
to Docs/Pipeline. Do not implement code under this documentation continuation or
invent a producer record. Resolve this follow-up, then close received contribution
scope; final manual acceptance stays with 10C.”

**Existing distribution and documentation completion — resume L&D TREK-10 and Docs
TREK-11/15.** “Consume CMT-126, CMT-124/125 and 10E-r1 directly. Credit the actual C4/C9
external receipts. Finish the existing upstream payload/notices work using the
prepared acquisition route when available; preserve old binaries. Resolve the
application/recovery delivery disposition, agree exact corrected manual hashes,
and produce a new identified archive from owning source/build inputs. Authenticate
source → wheel → installed resources → archive and repeat only affected checks.
Keep C9 intact. Deliver the exact bundle/manual and limits for 10C; no publication
or production cutover.” Reporting and Learner may separately close TREK-13/14 on
their existing receipts without another content commission.

**Acceptance — issue the existing [10C prompt](../task10-deliverables/10C_ACCEPTANCE.md)
after convergence.** Add: “Use this review's received evidence and scope distinctions.
Follow the final installed manual, credit physical external placement, record
actual environment/ordinary-console stop evidence and any justified natural
lifecycle observation or permitted reuse. Record exact receipts on TREK-10/11/15
and changed Pipeline input on TREK-9. Return concrete defects to their owners.
No new unified shard view, mandatory flattened export, NiceGUI, synthetic campaign,
model build or production activation.”

**Activation — separate future Owner decision, not a command to run now.** Once the
operational observation is settled, Pipeline/Watcher can prepare a concrete
preservation and activation plan for an explicitly selected installation/wheel,
config, database and model. Account for the unmatched current log, 34 existing
Runs and old-versus-new configuration authority; identify expected logging paths,
rollback and actual process/heartbeat verification. Do not treat C9 installation,
Task 09 local production registration, or completed source publication as that
authorization. No activation, preservation capture, restart or historical
reingestion has been performed by this review.
