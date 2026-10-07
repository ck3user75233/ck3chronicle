# Pipeline — Shared Backend/API

**2026-10-07 amendment:** the Owner's [removal continuation](OBSERVER_REMOVAL_AND_RECEIVING_PIPELINE.md)
removes `observer_log_path` only. Remaining backend/adapter semantics and receiving
obligations are preserved. Earlier Observer-specific compatibility requirements
are superseded by deletion and preserved required Watcher-path correspondence.

Prepared 2026-10-06 from approved scope; **awaiting owner issuance**.
Owner/implementer: Pipeline. Trekker ID: **TREK-1** — `todo`, prepared and awaiting owner dispatch.

When issued, deliver the shared backend/API in corrected
[plan B/C and H stage 1](../CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md), subject to
[owner disposition O1–O10](../TASK09_OWNER_DECISIONS.md#o1--approval-and-revision)
and the [index's common boundaries](../CANONICAL_LOGGING_V1_DELIVERABLES.md#approved-implementation-limits).
There is no product prerequisite; The pilot supplies tracking only.

Edit only `src/ck3chronicle/runtime_logging.py` and new
`src/ck3chronicle/journal.py`, plus the directly coupled ownership-checker update in
`tools/check_runtime_logging.py` for this new adapter. Pipeline is their sole
implementer. Update the shared 07E handoff with the interface and evidence after
coordinating its section; retain component implementation ownership elsewhere.
Save exact edited-byte baselines/prior absence per plan H before editing.

Extend the existing owner without breaking current keyword callers: lazy config
import; validated fresh config-free INFO/10 MiB/five-backup defaults; explicit
destination; shared foreground path helper; central five-second interval.
Setup failure surfaces before work; post-setup writes/rotation/close remain best
effort and cannot replace the substantive outcome. Preserve legacy paths, formatter,
fields, severity, rotation and context. Avoid extra root handlers in owned streams.
Task 10 supplies only a resolved writable destination/settings when available;
coordinate that seam if newly active, without changing its architecture.

Implement the small stdlib/backend-only `get_journal`, `Journal.call()` context
manager and checkpoint API from C. Extract real function/module/source/hook line,
release temporary frames, keep minimal scalar local context and restore it on
exit. Emit normal `call_finished` only on normal return; nested scopes add no
exception terminal/traceback. No call IDs, parent IDs, transport or generalized
tracing. Bare checkpoints are immediate diagnostic observations, not routine hooks.
Counted hooks emit first/periodic and explicit completed-total observations under
C's exact guard; never discover work, clamp invalid counts or infer a final flush.
No component hooks belong to this assignment.

Verify exact patch/source boundaries and run the ownership checker with the repo
Python. Review lazy import, frame/context cleanup, throttling/guard, preserved
destinations/settings and non-masking behavior. Use available genuine current
caller evidence where applicable; do not fabricate API harnesses, recursion,
timing or failures. Dynamic counted/bare/rotation/error cases not naturally exercised
remain explicitly unverified; Learner Integration and later receiving supply real consumer evidence.
Do not require synthetic execution to declare this interface ready for consumers.

Deliver API signatures, exact source hashes/patch and limits in
`docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md`. Learner receives config-free retained
import/payload suitability; Watcher and Pipeline confirm existing destination,
settings and field compatibility. Implementation readiness releases Learner Integration to perform
its genuine integration; it is not proof of that later execution. This record
remains open for actual required receiving dispositions, without making all of Learner Integration
a prerequisite for shared backend implementation. No production restart or candidate generation
belongs to this prompt.

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
& $pilotNode $pilot team-state pipeline
& $pilotNode $pilot task-show TREK-1
```

Use the results to retrieve incoming deliveries, upstream interfaces/artifacts and
limits, coordination requests in comments, and responses to your outgoing work.
Read later delivery/receipt comments as well as the checkpoint, then open the linked
technical handoffs. Follow the [reading guide](../DEVELOPMENT_ENVIRONMENT.md#what-to-retrieve-from-trekker).
Refresh affected records before integration or receipt; Trekker does not notify chats.
Proceed only within this owner-issued assignment. Ready lists do not dispatch work;
open dependencies can have usable interfaces with remaining receiving obligations.

For this assignment, look on TREK-1 for Learner's retained-interface receipt and
remaining compatibility requests; inspect TREK-3/TREK-4 when their linked follow-ups
affect backend compatibility. Do not assume an earlier checkpoint is the latest disposition.

For actual changes use `task-update ID REQUEST.json`, `checkpoint ID REQUEST.json`,
`delivery ID REQUEST.json` and `receipt ID REQUEST.json` through the same helper,
with this record's ID and an absolute UTF-8 JSON request path in ignored storage.
The handoff documents exact fields. Re-read before updating; stop and reconcile
incomplete writes rather than replaying them. Delivery and receipt stay on the same
record; keep it open until required receiving/follow-up disposition. Final Packaging
records internal completion by checkpoint/update, without inventing a receiver.
