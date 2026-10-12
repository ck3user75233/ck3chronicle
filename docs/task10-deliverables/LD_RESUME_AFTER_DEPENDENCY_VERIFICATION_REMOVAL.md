# Launch & Distribution — resume work after removal of dependency verification

Owner continuation, prepared 2026-10-12 for issuance to Launch & Distribution.
Checkout: `C:\Users\nateb\Documents\ck3chronicle`.

## Changed requirement

The Owner has already resumed 10B and 10C. This is a change notification and an
instruction to complete the work previously blocked by dependency verification,
not an instruction to redo those assignments from the beginning.

The Owner explicitly states: **"we do not need to verify python and ripgrep,
we know those are working"**. Use the existing working, identified local Python
and ripgrep payloads. Additional upstream verification, downloading comparison
archives and remote binary correspondence are **not Task 10 requirements**.
GitHub access is intentionally restricted. Do not run or ask the Owner to run
`Fetch-UpstreamInputs.ps1`, request network access for that comparison, or replace
the dependencies to satisfy the superseded check.

This direction supersedes conflicting waits in older 10B/10C descriptions,
handoffs, checklists, packaging notes and Advisory reports. Preserve the existing
payloads and included notices. Do not recreate the removed prerequisite as a
renamed provenance, licensing-evidence or dependency-reverification campaign.
Normal local bundle inventory/hashes and installed-product checks remain useful
and required; they identify the assembled product and its operation.

## Refresh current results before acting

Read root instructions, current plan/status/handoff, the updated
`docs/task10-deliverables/10B_DISTRIBUTION.md` and `10C_ACCEPTANCE.md`, and the
current distribution/documentation/acceptance handoffs. They may contain newer
results than Advisory last inspected. Retrieve the actual tracker records through
the protected helper, including all later deliveries and receipts:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state launch-distribution
& $pilotNode $pilot task-show TREK-10
& $pilotNode $pilot task-show TREK-16
& $pilotNode $pilot task-show TREK-11
& $pilotNode $pilot task-show TREK-9
& $pilotNode $pilot task-show TREK-12
& $pilotNode $pilot task-show TREK-15
```

Run these serially using the canonical store and syntax in the pilot handoff.
Continue **TREK-10** for packaging and **TREK-16** for acceptance; do not create
replacement records, replay receipts or rerun already satisfied checks without
a changed artifact or concrete reason. Record this Owner disposition on those
existing records and correct their current summaries. Preserve historical
comments and the exact scope of prior results.

## Complete the work that this decision unblocks

1. **Reconcile the actual remaining checklist.** Remove the upstream Python/
   ripgrep verification/download wait from current 10B/10C state and owned
   continuation documents. Do not infer that a failed historical acquisition
   attempt remains a current blocker. Identify which assembly or receiving
   actions were deferred solely because of it and resume those actions now.
2. **Finish 10B's local distribution work.** Consume the latest received
   application and agreed manual inputs. Preserve current component pins and
   existing working dependencies. If a suitable final archive already exists,
   authenticate and use it; otherwise complete the existing build recipe and
   produce a new identified archive, manifest and delivery receipt. Never patch
   an already received archive in place. Do not fetch or compare remote
   ck3chronicle source to determine what the local candidate should contain.
3. **Coordinate the newly requested manual revision accurately.** Refresh
   TREK-11 and the two `MANUAL_01_PRODUCT_INTRODUCTION_AND_ORIENTATION.md` /
   `MANUAL_02_STRUCTURE_AND_EDITORIAL_REVIEW.md` assignments. Use the latest
   actually delivered revision. Do not falsely label an older manual as satisfying
   the new Owner review. If that revision is still being edited, finish all
   independent bundle preparation/receiving now, coordinate directly on the
   existing record, and incorporate it when delivered. Avoid another candidate
   rebuild solely to demonstrate activity while the final manual is pending.
4. **Continue 10C with the actual combined delivery.** Authenticate the exact
   archive/manual and perform only outstanding or affected installed-user-journey
   checks, including external placement and ordinary-console Watcher Ctrl+C and
   explicit handler stopping within the existing authorized isolated scope.
   Preserve valid previous setup, ingestion, reporting and workflow evidence.
   Clean-environment acceptance remains a product installation check, not a
   renewed audit of upstream Python/ripgrep binaries.
5. **Close satisfied work and give a usable handoff.** Record delivery and receipt
   separately, name the tested artifact and real evidence limits, and close
   completed scope on the existing records. Give the Owner the package and manual
   links, what was unblocked and completed, and the exact remaining action if any.
   Distinguish readiness for Owner acceptance from the Owner's acceptance itself.

The separately discussed ingestion/hash-lookup/failed-Run/retry redesign remains
deferred until after Task 10. Do not wait on Watcher implementation or reopen
received Pipeline work without a concrete newly authorized change or defect.

## Handle actual access constraints explicitly

This continuation authorizes completion of already assigned packaging/acceptance
work without another generic permission request. It does not change tool access
restrictions. Inspect the current session's permitted environment before execution.
If an outstanding installation or interactive check cannot be performed there,
complete independent work and state the exact remaining observation, tested
artifact, required location/environment and bounded Owner-run command or steps.
Make that required intervention prominent in the final response; do not bury it
in an evidence file or simply say "acceptance pending". Do not bypass restrictions
or claim an in-checkout developer-host test proves clean external installation.

No production restart/configuration change, Git commit/push, hosted publication,
new implementation commission or dispatch of other teams is authorized here.
The requested outcome is completed work made possible by the scope correction,
not merely acknowledgement that the requirement changed.
