# Pipeline — Remove Observer interfaces and receive the replacement candidate

Prepared for owner issuance. Continue **TREK-6** through removal, integration and
final receiving in this one assignment. Read TREK-1 through TREK-6 and their latest
receipts; use TREK-3 for Watcher's removal delivery and TREK-2 for Learner's fresh
authenticated distribution. No new task or 09C is needed for this work.

The Owner has ordered Observer deletion. The completed
[Watcher dependency review](../WATCHER_OBSERVER_DEPENDENCY_REVIEW.md), CMT-32/33,
establishes that required Watcher functions are independent and need no transfer.
This assignment supersedes requirements to retain or exercise Observer in the old
Task 09 plan/prompts. All unrelated approved logging and receiving limits remain.

## Remove Pipeline-owned interfaces and unblock Learner

Remove `cmd_observe_logging` and its parser block from `src/ck3chronicle/cli.py`,
and only `observer_log_path` from `src/ck3chronicle/runtime_logging.py`. Remove
Observer command entries from README and `tests/test_reporting_cli_genuine.py`,
preserving the remaining genuine-evidence check. Coordinate that small test edit
with any current Reporting work. Remove other exclusively Observer references
required by these deletions without broad cleanup.

Watcher owns deletion of `logging_observer.py` under its
[removal prompt](OBSERVER_REMOVAL_WATCHER.md). Preserve the actual Watcher CLI route,
process helpers, EventJournal/lease/heartbeat, exit capture, source timestamp,
playset JSON and ingestion wiring. Preserve the shared logging backend and adapter,
execution journals, existing defaults and component error behavior.

Reconcile current command/API and acceptance guidance in README, 07E, RELEASES,
the Task 09 plan/index and affected prompts with the deletion. Preserve historical
delivery evidence with explicit supersession. Remove the Observer lifecycle and
Observer sole-stream confirmations as completion requirements; do not record them
as passed tests. Assess any separate actual Watcher compatibility obligation against
the dependency review and preserved code, rather than carrying an Observer check
forward under a Watcher label.

Publish the cleaned backend's exact path/hash and scope in normal Pipeline handoff
material and a TREK-6 checkpoint for Learner. Do this before waiting for Learner's
[replacement distribution](OBSERVER_REMOVAL_LEARNER.md). Learner consumes these
bytes and owns distribution authentication; you own packaging them. This partial
delivery breaks the sequence into usable steps without another assignment.

## Build the replacement and receive the integrated result

After receiving Watcher's deletion and Learner's new distribution, build a fresh
wheel and clean staged installation. Do not patch the old wheel, staged candidate
or any immutable retained distribution. Preserve them as history and rollback.

Update required resource entries and candidate catalog/references through the
existing release mechanism. Exclude Observer-bearing retained distributions from
the replacement package, including the superseded logging distribution; adding a
clean copy alongside a contaminated copy is insufficient. Keep their historical
checkout artifacts intact. Account for shipped catalog references so the replacement
does not advertise missing bundled payloads. Preserve production model defaults
and unrelated supported resources. If an actual required model/reference binds to
an excluded distribution, report that concrete conflict rather than altering pins
or rewriting retained bytes to conceal it.

**Acceptance: no Observer command, implementation, helper or embedded retained
copy remains in the replacement candidate; CK3Chronicle execution logging and the
required Watcher capture/timestamp/playset/processing behavior remain intact.**

Verify against the exact replacement artifact:

- Source/wheel/installed correspondence in both directions, including every bundled
  retained payload, absence of stale Observer modules and command registration,
  and updated application fingerprint/release identities.
- New Learner manifest/payload authentication, exact shared backend/adapter bytes,
  retained isolated config-free execution and bounded genuine result/logging checks.
- Installed root/help/catalog and genuine public-handler/Reporting behavior relevant
  to the changed CLI/backend combination. Reuse unchanged semantic evidence and
  compare actual outputs, not only command success.
- Unchanged required Watcher route and preserved capture facts/playset wiring,
  using Watcher's review, source correspondence and existing genuine lifecycle
  evidence. No new CK3 run is required merely to prove removal of the independent
  Observer. If a required path actually changed unexpectedly, report the defect.
- Logging ownership checker and appropriate packaging/dependency checks. Do not
  run broad historical synthetic suites or invent events/failures for coverage.

Retain the existing external-placement issue explicitly. Check environment access
early: if an authorized writable staging location outside checkout is available,
perform the bounded physical relocation/isolated execution check. If unavailable,
finish all independent work, state the precise remaining check and required access
or owner disposition. Do not bypass sandbox restrictions, treat outside-cwd execution
as physical relocation, or infer that the Owner accepted Advisory's earlier proposed
disposition. Unrepresented rotation/exception cases remain disclosed under plan G;
they do not become new mandatory test campaigns.

## Delivery and closure

Preserve exact edited/deleted bytes and prior absence, including coupled packaging
changes; keep broader build inputs separate. Identify the prior immutable rollback
artifact without overwriting intervening work. Coordinate shared documents and
catalog edits with the component deliveries before editing.

Write one consolidated Pipeline handoff with replacement path/hash, immutable
Learner ID/pin, removed contents, actual verification, limits, rollback and per-record
receiving dispositions. Record receipt on TREK-3 and TREK-2 for the new deliveries.
Reconcile Observer-only follow-ups on TREK-1/3/4/6 as superseded by removal, retaining
unrelated work and historical comments. Close only obligations actually satisfied
or explicitly dispositioned; name the owner and next action for any remainder.
Do not leave a generic awaiting-confirmation item where no specific obligation remains.

Read root instructions and current handoffs. Use only the protected helper:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state pipeline
& $pilotNode $pilot task-show TREK-6
```

Also read TREK-1 through TREK-5 directly, later comments and linked technical evidence;
refresh before integration or receipt. Use the
[pilot handoff](../TREKKER_CLI_PILOT_HANDOFF.md) for updates/delivery/receipt and
incomplete-write reconciliation. No new records, invented receipt or automatic team
dispatch. Runtime changes require `.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py`.
No production activation/selection change, service restart, historical reingestion,
full-corpus campaign, synthetic test, publication, commit or push is authorized.
