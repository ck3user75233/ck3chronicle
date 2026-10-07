# Watcher — Remove the independent Observer implementation

Prepared for owner issuance. Continue **TREK-3**; Pipeline receives on the same
record for **TREK-6** integration.

The Owner has ordered Observer deletion. The completed
[Watcher dependency review](../WATCHER_OBSERVER_DEPENDENCY_REVIEW.md), delivered
as CMT-33, establishes that necessary Watcher functions are independent of it.
No behavior needs transferring before deletion. This assignment replaces the
Observer implementation/verification requirements in the earlier Watcher prompt.

Delete `src/ck3chronicle/logging_observer.py`, including its private measurements,
timestamp-header reader and heartbeat machinery. Remove exclusively Observer
checks from Watcher-owned material if present. Update the normal Watcher handoff
with exact deleted bytes and preservation evidence.

Preserve `watcher.py`, `harvester.py`, `watcher_processing.py`, process helpers,
`EventJournal`, lease and Watcher heartbeat. Preserve CK3 exit capture, validated
source-log timestamp recording, protected debug.log/playset JSON production,
publication and ingestion triggers. Do not delete shared helpers because Observer
used them. Do not remove historical logs or immutable artifacts.

Pipeline owns the CLI/backend removal, README and Reporting command-list check,
shared Task 09/07E/release guidance, and replacement packaging under its
[combined assignment](OBSERVER_REMOVAL_AND_RECEIVING_PIPELINE.md).
Coordinate the deletion with Pipeline so it can remove the temporary dangling CLI
reference. Do not run that command during the transition. Keep shared 07E edits
with Pipeline; reference your normal Watcher handoff from the delivery.

Preserve exact current bytes of files actually edited/deleted and prior absence
for new delivery files. Verify the removal and unchanged required Watcher path by
source comparison and existing genuine evidence. Source review is not a new
installed-execution claim. No additional CK3 exercise or synthetic test is needed.

Deliver the exact deletion/patch, preserved-path comparison, evidence limits and
next receiving action on TREK-3. Pipeline records actual removal receipt against
the replacement candidate. Dispose of Observer-only lifecycle checks as removed
requirements, not passed tests; preserve unrelated obligations.

Read root instructions and current handoffs. Use only the protected pilot route:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state watcher
& $pilotNode $pilot task-show TREK-3
& $pilotNode $pilot task-show TREK-6
```

Read later comments and linked evidence; refresh before delivery. Use the
[pilot handoff](../TREKKER_CLI_PILOT_HANDOFF.md) for checkpoint/delivery operations,
preserving unrelated state. The issued prompt is authority; readiness is not
dispatch. No production changes, restart, publication, commit or push.
