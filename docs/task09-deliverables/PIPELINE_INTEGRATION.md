# Pipeline — Pipeline Integration

**2026-10-07 amendment:** [Pipeline removal and receiving](OBSERVER_REMOVAL_AND_RECEIVING_PIPELINE.md)
supersedes Observer retention/execution and sole-stream checks. Required Watcher
compatibility is assessed from the dependency review and preserved code, not an
Observer check carried forward under another name.

Prepared from approved scope; **awaiting owner issuance**.
Owner/implementer: Pipeline. Trekker ID: **TREK-4** — `todo`, prepared and awaiting owner dispatch.
Prerequisite: received Learner Integration and Shared Backend/API. Early request/
catalog work can proceed independently of Watcher Integration; coordinate final
root foreground composition with the preserved required Watcher interface. Reporting
receives the configured foreground interface.

When issued, implement corrected [plan B, D outcomes, E/P, E/A, G and H](../CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md)
under the [owner decisions](../TASK09_OWNER_DECISIONS.md) and owner's consolidated
[deliverables and limits](../CANONICAL_LOGGING_V1_DELIVERABLES.md#approved-implementation-limits).
Read root instructions, current plan/status/handoff, current 07D/07E interfaces and
team governance. The consolidated assignment contains both the earlier Pipeline
adoption and application foreground work; there are no separate tickets for them.

Edit only `src/ck3chronicle/pipeline/request_handler.py`, `pipeline/catalog.py`,
root `src/ck3chronicle/cli.py` and `tools/check_runtime_logging.py`, plus relevant
07D/07E/application handoff sections. Preserve exact edited current bytes/prior
absence per plan H. Coordinate shared checker/CLI/document sections before editing.
Reporting owns `reporting/cli.py`, Watcher its capture/caller integration, and Learner its loader.
Shared backend repairs stay with the Shared Backend/API owner within issued scope.

Add one foreground `request_accepted` observation after successful submit RPC,
using the real returned `RequestRef` only when foreground invocation context is
active. Preserve request/handler identity, wire protocol, silent polls and Watcher's
existing acceptance evidence. No argument dump, extra call scope or context transport.

Wrap standalone model-catalog dispatch in shared foreground setup/outcome/cleanup.
Prefer explicit `--log-dir`; config-free default is
`<cwd>/.ck3chronicle/wip/model-release-logs`, filename `model-release-<id>.jsonl`.
Where application configuration is already used, consume its resolved destination;
open failure does not select a fallback. Preserve help/JSON stdout and original
errors/codes. No evaluator scope or routine post-write checkpoint.

Configure root capture/ingest/runs/report/doctor foreground invocation after parsing,
with explicit `--log-dir` override. Consume resolved destination/validated settings
from existing application configuration and shared naming under
`<ROOT_CK3CHRONICLE>/logging`. Keep help configuration-independent. Coordinate the
Task 10 seam if active, without installer, config authority, doctor or UI redesign.
Do not hash inputs/application/models or inspect lazy properties for event fields.

Preserve watch-owned destinations and lifecycle: no second handler,
call scope or terminal pair. Preserve caught-error return codes and existing
component traceback ownership. A canonical boundary records an escaping exception
once; nested scopes add no trace and cleanup cannot mask the substantive outcome.
Existing ingestion, handler internals, preparation, storage, transactions, retention,
classifier/schema and direct handler entry coverage require no edits or new hooks.

Extend the existing ownership checker for the shared adapter and declared Learner
hook sources, coordinating its Shared Backend/API changes. Authenticate retained
copies separately; static ownership does not prove isolated execution. Do not
restore the removed synthetic logging suite.

Run bounded source checks and
`.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py`. Use genuine
public-handler records, preferably the existing disposable receiving store, to
compare accepted references with real handler events. Verify real foreground
listing/report/source/export output with Reporting and genuine catalog reads/listing.
Preserve stdout/stderr, file destinations, help and normal outcomes. Reuse valid
unchanged evidence with explicit limits. No fake client/context harness, fault
injection, historical reingestion or production package registration/selection.
Do not run capture, retention or potentially destructive doctor operations for coverage.
Each synthetic test requires its own owner approval; missing cases stay unverified.

Deliver exact patches/hashes, configured interface, real commands/evidence and
limits in normal 07D/07E/application handoffs. Watcher confirms owned-stream/caller
compatibility; Reporting receives foreground journaling and request links. Keep
the canonical record open through actual consuming receipt, while usable interface
delivery allows authorized consumer integration to start. Final Packaging receives
the combined result. No production activation/restart, publication, commit or push.

## Trekker startup and updates

Use only the delivered protected helper and canonical store from the
[pilot handoff](../TREKKER_CLI_PILOT_HANDOFF.md). On startup/resume:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state pipeline
& $pilotNode $pilot task-show TREK-4
```

Use the results to retrieve incoming deliveries, upstream interfaces/artifacts and
limits, coordination requests in comments, and responses to your outgoing work.
Read later delivery/receipt comments as well as the checkpoint, then open the linked
technical handoffs. Follow the [reading guide](../DEVELOPMENT_ENVIRONMENT.md#what-to-retrieve-from-trekker).
Refresh affected records before integration or receipt; Trekker does not notify chats.
Proceed only within this owner-issued assignment. Ready lists do not dispatch work;
open dependencies can have usable interfaces with remaining receiving obligations.

For this assignment, read TREK-2 for Learner artifact identities/receipt limits,
TREK-3 for the removal delivery and dependency review, and TREK-4 comments for Learner's checker and
release-document coordination requests. Record actual consumption and later Reporting receipt.

For actual changes use `task-update ID REQUEST.json`, `checkpoint ID REQUEST.json`,
`delivery ID REQUEST.json` and `receipt ID REQUEST.json` through the same helper,
with this record's ID and an absolute UTF-8 JSON request path in ignored storage.
The handoff documents exact fields. Re-read before updating; stop and reconcile
incomplete writes rather than replaying them. Delivery and receipt stay on the same
record; keep it open until required receiving/follow-up disposition. Final Packaging
records internal completion by checkpoint/update, without inventing a receiver.
