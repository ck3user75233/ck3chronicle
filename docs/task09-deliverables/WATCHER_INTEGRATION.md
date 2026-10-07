# Watcher — Watcher Integration

**Historical assignment — superseded on 2026-10-07:** use [OBSERVER_REMOVAL_WATCHER.md](OBSERVER_REMOVAL_WATCHER.md)
for the current owner-issued continuation. The old Observer retention, lifecycle
and sole-stream requirements below are removed requirements, not passed tests.
All unrelated logging/receiving limits remain. This historical text does not
authorize running or restoring Observer.

Prepared 2026-10-06 from approved scope; **awaiting owner issuance**.
Owner/implementer: Watcher. Trekker ID: **TREK-3** — `todo`, prepared and awaiting owner dispatch.
Prerequisites: received Shared Backend/API and Learner Integration.
Early Pipeline Integration work may proceed independently.
Receiver: Pipeline for observer/application integration.

When issued, implement corrected [plan B, E/W, G and H](../CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md)
under the [owner disposition](../TASK09_OWNER_DECISIONS.md) and
[common boundaries](../CANONICAL_LOGGING_V1_DELIVERABLES.md#approved-implementation-limits).
Read current 07D/07E and Watcher handoffs with the current release receipt.

Edit only `src/ck3chronicle/logging_observer.py` and relevant Watcher/07E handoff
sections. Coordinate backend/path interface with Pipeline and owned-stream dispatch
with Pipeline Integration before edits. Save/verify exact edited bytes; do not modify the shared owner
or root CLI yourself.

Delegate existing ordinary JSONL events to `runtime_logging.py` and its shared
observer path helper/rotation. Preserve returned path and existing
`watch/log-progress-<timestamp>-<pid>.jsonl` naming from the actual timestamp/PID.
Use the standard shared formatter with existing event names/payloads. Preserve
measurement algorithm, actual facts, heartbeat content/replacement/removal and
old files. Add no call scope, routine bare checkpoint, measurement read, counter,
monitoring thread or alternate backend.

No initial edits to `watcher.py`, `watcher_processing.py`, `harvester.py`, lifecycle,
capture/playset/probe behavior or API triggers. Their existing evidence suffices.
Receive unchanged watcher/handler paths, lease/listener setup ordering, startup
PID destination, warnings, request/outcome correlation, silent polls and error
ownership. No duplicate canonical lifecycle pair or traceback redistribution.

Run source/ownership checks. Reuse valid genuine lifecycle/capture evidence only
for unchanged behavior. Changed observer execution requires bounded genuine
observation at a safe natural lifecycle, using the existing measurement inputs;
coordinate with Pipeline Integration to avoid a second root handler. Compare actual
measurements, returned path, heartbeat and ordinary shared JSONL/rotation behavior.
If a safe natural opportunity is unavailable, name exactly that execution gap and
leave receiving open pending appropriate authorization/opportunity. Source review
plus old evidence does not verify the changed observer. No live service restart,
fake process, injected failure, raw expiry or historical reingestion is authorized.

Deliver exact changed bytes/patch, genuine evidence or explicit limits, and
operator-visible formatter/rotation effects in the normal Watcher/07E handoff.
Pipeline records receipt against the application combination; component defects
remain Watcher-owned. Technical delivery cannot close a required unexercised
receiving obligation or imply owner acceptance/activation.

Read root instructions and current plan/status/handoff before implementation.
Coordinate shared files before editing; follow plan H for edited-byte preservation.
Runtime changes require `.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py`.
Every synthetic test requires explicit owner approval for that individual test.
No production activation/restart, publication, commit or push is authorized.

## Trekker startup and updates

Use only the delivered protected helper and canonical store from the
[pilot handoff](../TREKKER_CLI_PILOT_HANDOFF.md). On startup/resume:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state watcher
& $pilotNode $pilot task-show TREK-3
```

Use the results to retrieve incoming deliveries, upstream interfaces/artifacts and
limits, coordination requests in comments, and responses to your outgoing work.
Read later delivery/receipt comments as well as the checkpoint, then open the linked
technical handoffs. Follow the [reading guide](../DEVELOPMENT_ENVIRONMENT.md#what-to-retrieve-from-trekker).
Refresh affected records before integration or receipt; Trekker does not notify chats.
Proceed only within this owner-issued assignment. Ready lists do not dispatch work;
open dependencies can have usable interfaces with remaining receiving obligations.

For this assignment, retrieve the shared API on TREK-1 and relevant prerequisite
evidence on TREK-2. Read TREK-3's Pipeline responses and TREK-4's root CLI/stream
coordination, including compatibility requests that may not appear in your incoming list.

For actual changes use `task-update ID REQUEST.json`, `checkpoint ID REQUEST.json`,
`delivery ID REQUEST.json` and `receipt ID REQUEST.json` through the same helper,
with this record's ID and an absolute UTF-8 JSON request path in ignored storage.
The handoff documents exact fields. Re-read before updating; stop and reconcile
incomplete writes rather than replaying them. Delivery and receipt stay on the same
record; keep it open until required receiving/follow-up disposition. Final Packaging
records internal completion by checkpoint/update, without inventing a receiver.
