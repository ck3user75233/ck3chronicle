# Pipeline — Receive and pin the Task 09 release baseline

**Receiving is delivered.** For the subsequent owner-issued publication step use
[Publish and pin the received baseline](RELEASE_PUBLICATION_PIPELINE.md). That
continuation specifies local adoption/commit/tag authority; this earlier prompt
records the build/receiving assignment and its original prepare-only boundary.

Prepared for owner issuance, 2026-10-07. Continue **TREK-6**, receiving Learner's
production-scope model on **TREK-2**. This assignment takes effect when issued by
the owner. Preparation may proceed while Learner builds.

**Owner amendment, 2026-10-07:** physical external installation verification is
deferred to Task 10 and no longer blocks this release. The
[recorded disposition](../TASK09_OWNER_DECISIONS.md#external-installation-verification-deferred-to-task-10--2026-10-07)
supersedes earlier placement prerequisites. Publication/adoption boundaries below
remain unchanged.

Deliver one verified application/Learner/model combination suitable for adoption
as the repository's baseline and input to Task 10. Build a fresh application
candidate containing the new full model, complete integrated receiving, and make
the exact remaining owner actions concrete. Do not declare Task 09 complete merely
because a wheel built or a command returned success.

## Receive and package

Read root instructions, [owner decisions](../TASK09_OWNER_DECISIONS.md),
[release procedures](../RELEASES.md), [current receiving evidence](../learner-next-release/OBSERVER_FREE_PIPELINE_RECEIVING.md)
and [Learner's baseline assignment](RELEASE_BASELINE_LEARNER.md).

Receive the exact new 73-log model: authenticate its manifest, executable closure,
input basis/order, build receipts, semantic comparison with current production and
actual journal review. Confirm this is the full production-scope delivery, not the
two-log acceptance package. Record the real TREK-2 receipt or the specific Learner
repair still required.

Reconcile current application source and resources with the received component
deliveries. Record a bounded source inventory including required untracked files;
a Git HEAD alone does not identify this dirty working tree. Account for unrelated
concurrent changes rather than silently incorporating them. Component defects
remain with their owners; Pipeline owns packaging and runtime composition.

Through the existing release process, create a fresh immutable application artifact
and isolated installation containing the exact authenticated Learner and new model.
Prepare the packaged default selection with the actual package and manifest pins.
Pipeline owns packaging resources and `packaging/models/selection.json`; coordinate
shared files before editing. Use isolated catalogs/selection for receiving. Prepare
the corresponding repository catalog/default changes for final adoption, but do not
change active `models/selection.json` or production catalog metadata yet.

Verify source/resource correspondence, dependencies and installed payload integrity.
No Observer command, module, helper or embedded retained Observer copy may reappear.
Preserve previous immutable artifacts for history/rollback. The existing tested
wheel is evidence for unchanged components, not the identity of this new artifact.

## Verify the installed combination and logging

Use bounded genuine inputs from the existing receiving evidence to execute installed
classification with the new pinned model. Compare meaningful results with Learner's
delivery, including statuses, captures and native diagnostic representation. Verify
actual loaded identities and ordinary output behavior. Authenticate and exercise
the installed retained Learner through a bounded genuine evaluation; do not repeat
its full build just to demonstrate packaging.

Receive Reporting/public-handler and Watcher capture/timestamp/playset evidence
against the final source/resource closure. Reuse valid unchanged evidence explicitly;
refresh only what the changed model, package or actual failures invalidate. Any
needed genuine persistence/report checks use isolated task storage and the public
handler, not production history. No full historical reingestion or manufactured
cases. A new live CK3 session or production restart is not a prerequisite invented
by this assignment.

Inspect the resulting journals, not just exit codes. Consolidate actual excerpts
and receipt references against the [canonical design](../CANONICAL_LOGGING_SYSTEM_V1.md):
executing identities, source locations, ordering, substantive call outcomes,
truthful completed-work counts where applicable, and terminal/receipt consistency.
Distinguish newly observed, valid reused and unobserved behavior. Preserve normal
stdout/error ownership; do not demand extra logging hooks or synthetic tests.

Do not perform physical outside-checkout placement for this release or request
external staging access as a Task 09 prerequisite. Record the check as unperformed
and explicitly deferred by the Owner to Task 10's installation verification.

## Pin the baseline and close the handoff

Write one concise `docs/TASK09_RELEASE_BASELINE.md`, linking detailed evidence in
the normal Pipeline/Learner handoffs. Record:

- Exact source inventory/fingerprint, application artifact/hash, Learner ID/pin,
  model ID/pin, parser/matcher identities and dependency versions.
- Ordered training-input basis and settings, received comparison and installed
  behavior/logging evidence, placement result and material evidence limits.
- Intended packaged/repository selections, separately from currently active
  production selections. Do not claim activation based on a staged default.
- Prior baseline and bounded rollback instructions that preserve immutable
  artifacts, existing Run lineage and intervening work.
- A concrete final adoption proposal: exact local production registrations with
  the next valid production orders and publication-evidence references; exact
  repository selection changes; reviewed Git include/exclude list and proposed
  commit/tag. Do not tag an older HEAD and call it the tested source baseline.

Use existing registration/selection formats; do not invent another pin system.
Prepare all receiving and exact proposed changes before returning the final owner
decision. State clearly which actions remain unexecuted. Live switch/restart,
production registration/selection, external publication and Git commit/tag/push
remain separate owner-authorized actions; none is implied by this prompt.

Task 09 is ready for owner closure when the full model and final artifact are
received, placement is dispositioned to Task 10 as directed above, and no
Task 09 implementation/receiving defect remains. Record baseline adoption and
source/live activation status honestly when the owner decides; pending activation
does not mean the implementation is unfinished. Reconcile the assignment index,
project status/plan and current handoff with actual results, without erasing history.

Give Task 10 the exact received baseline and its locations, supported installation/
configuration interfaces and remaining first-run setup work. [Task 10](../TASK10_PROMPT.md)
remains a separate owner-issued assignment; do not implement its installer or
configuration redesign here. No new Task 09C is needed for this existing receiving
work. Independently owned unrelated follow-ups remain visible.

## Coordination

Use only the [protected pilot](../TREKKER_CLI_PILOT_HANDOFF.md):

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state pipeline
& $pilotNode $pilot task-show TREK-6
& $pilotNode $pilot task-show TREK-2
```

Refresh affected component records before receiving; read later receipts and
technical handoffs alongside checkpoints. Link this owner-issued prompt and keep
current summaries short, with evidence links and explicit next actor/action.
Record delivery and receipt separately. Close TREK-2 when its component is received;
keep remaining Pipeline packaging obligations on TREK-6. Complete TREK-6 only
when its required receiving is resolved, with operational decisions separately
identified. Tracker state never substitutes for owner acceptance or dispatch.
