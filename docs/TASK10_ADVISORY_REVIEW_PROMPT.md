# Advisory — Establish Task 10 status, production health and release integrity

Prepared for Owner issuance in a new Advisory chat, **2026-10-08**.
Checkout: `C:\Users\nateb\Documents\ck3chronicle`.
Read root instructions and current evidence; do not assume access to the previous
Advisory conversation. This prompt supplies the relevant Owner context.

## Assignment and authority

The Owner needs a clear Task 10 status and next steps, confirmation of what is
actually running in production and whether its logging is working, and verification
that Windows distribution work preserved pinned components and the normal
source-to-release process. Establish these independently from current evidence;
do not presume either damage or successful deployment.

Advisory owns review, scope clarification and concrete next assignments.
This assignment authorizes read-only investigation and Advisory review/prompt
documents. It does not authorize component implementation, configuration/selection
changes, service start/stop/restart, activation, database repair/reingestion,
retention changes, model builds, synthetic/fault-injection tests or Git/publication
actions. Do not fix or restart production before establishing its actual state.
No team dispatch or new implementation commission is implied.

Continue independent investigation if one path is inaccessible. Identify an exact
missing observation and a bounded owner-run command/access request when necessary;
do not repeatedly probe denied paths, bypass permissions or return only a gate
message. No generic new approval is needed for this authorized read-only review.

## Read and obtain current state

Read `AGENTS.md`, `docs/PROJECT_PLAN.md`, `PROJECT_STATUS.md`, `CURRENT_HANDOFF.md`,
[team governance](team-governance/README.md), [Task 10 index](TASK10_DELIVERABLES.md),
the relevant owner-issued prompts in `docs/task10-deliverables/`, and
[Trekker working instructions](task10-deliverables/WORKING_AGREEMENT.md).
Use focused handoffs; do not reconstruct the entire repository history.

All tracker reads/writes use the delivered protected helper and canonical store:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state advisory
& $pilotNode $pilot task-list
& $pilotNode $pilot task-show TREK-6
# Repeat task-show for the real relevant IDs below, including later comments.
```

Canonical store: `C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state`.
Use [the pilot handoff](TREKKER_CLI_PILOT_HANDOFF.md) for syntax and recovery.
No raw CLI/SQL, alternate helper/store or invented IDs. Query `pipeline`,
`launch-distribution`, `watcher`, `data-intelligence` and `learner` team views as
needed, but do not mistake a filtered/empty team view for the project overview.

Preparation-time navigation, **not a final status judgment**:

| Work | Record / evidence to refresh |
|---|---|
| Task 09 baseline | TREK-6 completed; CMT-69, [baseline](TASK09_RELEASE_BASELINE.md). Commit `709ea7842a0202c420b43355b18be91d8ca196a3`, tag `task09-baseline-2026-10-07`; completion explicitly excludes live activation. |
| 10A design | TREK-7; TREK-8 is an archived duplicate, not another obligation. [Design](task10/FIRST_USE_DESIGN.md). |
| 10A.1 Pipeline | TREK-9; CMT-81 delivery, CMT-83 receipt, CMT-106 separate help/reference follow-up, CMT-126 new application-wheel delivery. [Pipeline handoff](task10/PIPELINE_HANDOFF.md). |
| 10B distribution | TREK-10; [distribution handoff](task10/DISTRIBUTION_HANDOFF.md). Recorded C9 external setup/isolated installed checks are not evidence of production cutover. Refresh provenance/notices, final manual bundle and exact current candidate. |
| 10D reference | TREK-11; [documentation handoff](task10/DOCUMENTATION_HANDOFF.md), [interface inventory](task10/INTERFACE_INVENTORY.md), canonical `docs/user/` manual. |
| Component documentation | TREK-12 Watcher, TREK-13 Reporting, TREK-14 Learner; receipts CMT-109/110/111 are recorded despite descriptions still saying pending. Read later comments before deciding whether these should close. |
| 10E workflows | TREK-15; [workflow handoff](task10/WORKFLOWS_HANDOFF.md). Delivery recorded; final 10C receipt remains distinct. |
| 10C acceptance | No record found in the preparation-time list through TREK-15. Check current list/actual issuance; absence of enrollment alone does not prove no work occurred. |

Several records remain `in_progress` while carrying `handoff:received` and stale
pending-receipt descriptions. Determine actual remaining obligations individually.
Do not assume all are incomplete or close all merely from the tag. Do not reissue
already delivered work or revive the duplicate 10A chat.

## 1. Establish production identity and health first

Separate **editable source, source publication, built wheel, isolated installed
candidate, configured production installation, and actually running process**.
The application version string alone is insufficient; identify paths and exact
artifact/executable/configuration/model identities where evidence permits.

Start with [the October 5 cutover record](learner-next-release/PIPELINE_CUTOVER.md)
as historical evidence only. Do not reuse its old PIDs as current identity. Trace
any later explicit activation, launch/stop action or changed configuration and
determine whether Task 09 logging was ever deployed to the operational installation.
Do not silently identify the new Task 10 C9 test installation as production.

Obtain timestamped read-only observations, recording UTC and Hong Kong time:

- Configured operational installation, config/database/log paths and actual loaded
  executable/process identity when accessible. Check process start time as well as
  PID; distinguish launcher, Watcher and handler and any deliberate shutdown.
- Latest authentic lifecycle/capture/request/ingestion evidence, heartbeat and
  journal activity. Relate each to its process/artifact and expected activity.
  Distinguish event time from file modification/rotation times and capture source
  timestamps from processing times. Date alone does not prove inactivity.
- Whether CK3 has actually run/exited since the last verified lifecycle; use real
  evidence or one focused Owner question when this cannot be established locally.
  Do not infer a missed run solely from the calendar advancing.
- Accessible logs for the identified production route and older/rotated locations.
  State exactly which roots/date range were examined and which were inaccessible.
  Assess ordinary execution events against the activity that actually occurred.
- Existing persisted Run/hash/capture evidence, where safely readable, to assess
  whether an observed lifecycle has a captured/processed result. Do not turn this
  into historical reingestion or a new acceptance campaign.

Inspect command behavior before using any product probe: a nominal read/doctor or
HandlerClient operation may create logs or auto-start a host. Do not auto-start
services or configure a new runtime during diagnosis. Use existing evidence and
genuinely read-only access; if a necessary probe has side effects, present that
specific observation plan instead of executing it under this review authority.

Conclude with the strongest supported state: operating; stopped and why if known;
wrong/old version active; logging path/coverage problem; or unknown due to stated
missing evidence. A failed or unperformed activation is distinct from a logger
defect. Preserve evidence before proposing any operational change.

## 2. Audit pinned component integrity and the distribution repair path

Trace Task 09's received baseline through each materially changed Task 10 application
wheel, Windows bundle/candidate and installed/external copy. Use actual manifests,
build recipes, patches, delivery receipts, Git/worktree evidence and package member
bytes. Read L&D/Pipeline handoffs and repair comments, including owner-run scripts.
Start with the current received bundle and any subsequent application deliveries;
expand to earlier candidates only where needed to explain a changed file or fix.
At preparation, C9 contained wheel
`2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`,
while TREK-9 CMT-126 delivered a newer wheel
`94987fb06eeac685eb5b57a87edc41e58da1df9730ff8bf15ba7a023750ab489`.
Refresh later integration/receiving evidence before deciding which is current.
A source or wheel delivery alone does not establish installation or activation.

Establish for model, parser, matcher, selector, retained Learner and its retained
shared backend/adapter:

- The authoritative ID, external manifest pin and payload hashes; validate identity
  rules as well as file hashes. Check against the received baseline/delivery, not
  only a manifest that may have been regenerated beside edited files.
- Whether editable source, application wheel, bundle and installed copy contain
  the expected corresponding bytes/resources, and whether the actual loader selects
  those copies. Identify stale duplicates, shadowed imports, unexpected lookup roots
  or selection/catalog differences; record unreadable payloads as unverified.
- Whether any immutable release directory or already received artifact was edited
  in place, or whether a displayed ID/pin/version now describes different bytes.
  Also distinguish intact pins from wrong component selection or runtime dependency
  problems: valid payload hashes alone do not prove correct execution.

For each substantive fix during Windows distribution work, produce a compact trace:
reported issue and authority; owning team; exact file/copy edited; authoritative
source incorporation; new release/artifact identity if required; rebuilt bundle;
verification and receiving; actual activation if any. Establish whether a copy-only
fix was exploratory and later incorporated, remained only in an installed candidate,
or was represented as a completed product repair despite lacking a reproducible
source change. Do not infer this sequence from file timestamps alone.

Apply the normal ownership/release process accurately:

- Application code fixes belong in owning editable source and yield a fresh
  authenticated application artifact before rebuilding the Windows candidate.
- Changed retained executable/model closure requires the corresponding new
  immutable release identity/pin under the existing release procedure; never
  patch an old retained release in place.
- Outer installer/launcher, notices or manual fixes belong in the distribution's
  source/build recipe and yield a new identified bundle. They do not automatically
  require a new trained model or changed matcher identity.
- Keep product-version labels, content identities, local production registration,
  source commit/tag, hosted publication and live deployment distinct. An unchanged
  `0.0.2` filename does not establish identical wheels or automatically establish
  corrupted pins; compare exact hashes and the documented release contract.

Conclude which pins remain intact, which relationships are verified, whether any
direct-copy repair bypass occurred, and the exact evidence limits. If the normal
process was bypassed, identify the minimal source/release/bundle reconciliation
and its owner as a proposed assignment. Do not repair, rebuild, re-pin, overwrite,
delete or activate anything during this audit. Preserve suspect originals and
their evidence. Do not trigger another model build solely because packaging changed.

## 3. Give the Owner an actionable Task 10 picture

Reconcile the actual issued scope, deliveries, receipts and follow-ups across the
records above. Show each work package's owner, meaningful completed outcome,
actual remaining obligation, dependency, next actor/action and exact artifact.
Distinguish the outer C9 bundle, its documentation revision and any newer unreceived
application wheel. Determine what must reach the final bundle before 10C, what
is already received, and which remaining requirements are supported by issued scope.

Preserve settled scope: Launch & Distribution leads setup/distribution/manual and
acceptance; Pipeline owns application/configuration/storage APIs; component teams
own their code and technical reference contributions. Basic external SQLite access
may require users to reshape data. No unified review-shard/diagnostic view, mandatory
flattened exports or NiceGUI implementation. Physical external installation belongs
to Task 10, but credit actual later evidence rather than carrying forward an old gap.

Keep technical receiving, source publication, Owner acceptance and live activation
separate. Do not manufacture a new task number, duplicate producer records, require
the Owner to relay existing technical evidence or use Advisory as an approval gate.

## Deliverables and stopping point

Write `docs/task10/ADVISORY_STATUS_AND_INTEGRITY_REVIEW.md` with:

1. A short answer on production/logging health and the exact confidence/limits.
2. The compact Task 10 status/next-action table and recommended issuance order.
3. The pinned-component integrity findings and fix-to-source-to-release-to-bundle
   trace, including whether copy-only edits occurred and any reconciliation needed.
4. Only necessary bounded owner-assignable continuation prompts or diagnostic
   commands, ready to use. Identify whether each is a read-only observation,
   documentation correction, defect repair or activation.

Do not overwrite component-authored evidence or stale tracker descriptions during
this initial audit. Preserve historical comments. Propose precise current-text
corrections/closure changes with citations and named owners; factual conclusions
belong in this Advisory report first. If this review is enrolled when issued,
use `team:advisory`, link this prompt and append concise checkpoints through the
protected helper. Enrollment of the review does not dispatch implementation.

Return useful findings even if live observation is blocked. Lead with what the
Owner can conclude and do next, not a dump of tracker history. Never claim the
log search, production inspection, test, receiving or repair was performed
by you unless you actually performed it and can cite its evidence.
