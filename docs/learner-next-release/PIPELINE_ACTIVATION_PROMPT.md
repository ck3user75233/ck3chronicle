# Pipeline — execute the production cutover

Prepared for the owner to assign to the existing Pipeline chat. Saving this
document does not activate production or change the current hold. The following
authorization takes effect when the owner assigns this prompt for execution.

## Owner authorization

Execute the production cutover using [PIPELINE_CUTOVER.md](PIPELINE_CUTOVER.md)
and the [final R3 packaging receipt](PIPELINE_RECEIVING.md#r3-packaging-closed--2026-10-05).
This assignment supersedes the earlier activation hold and no-switch/no-restart
restrictions **for this specific cutover**. It authorizes the required backups,
selection changes, controlled watcher/handler stop and restart, normal automatic
ingestion of newly protected captures, and the documented package rollback if
needed. Proceed through the authorized operation without asking again merely
because older handoffs say activation is held.

Pipeline owns execution, verification and the operational handoff. Preserve the
existing database, stored Runs, capture evidence and immutable distributions.
Other project restrictions remain in force.

## Exact target

Checkout: `C:\Users\nateb\Documents\ck3chronicle`. Paths below are checkout-relative.
Read root/applicable `AGENTS.md`, development instructions and current status/
handoff openings. Use the final R3 artifact, not either earlier repaired wheel.

- Wheel: `.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl`.
  SHA-256: `7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`.
- Verified staged interpreter:
  `.codex-tmp/pipeline-r3-packaging-20261005/deployment/Scripts/python.exe`.
- New package: `4ac4e8ee92346e6d14eacfbf`, learner v61 / parser v1.8.
  Manifest pin: `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
- Existing production database:
  `.ck3chronicle/wip/runtime/ck3chronicle-schema3-20260928T211854Z.sqlite3`.
  Configuration remains checkout `config.toml`.
- Correct packaged selection: `packaging/models/selection.json`.
  The staged installed default already matches it; no corrective replacement is
  needed. Rollback uses the authenticated previous installed selection identified
  in the runbook, not the checkout's old `candidates/` path.

## Execute and verify

1. Reauthenticate the final artifact, staged installation, default and rollback
   inputs. Refresh game state, process identities, heartbeat/handler observations
   and pending-capture accounting. Runbook PIDs/times are historical: reconcile
   the concrete targets before executing commands. Resolve changed facts rather
   than blindly executing stale process references.
2. If CK3 is running, wait for its natural exit; do not stop the game. Let capture
   publication and in-flight ingestion finish. Preserve all protected inputs and
   confirm the runbook's safe boundary before stopping the verified watcher and
   handler. Do not start a competing watcher/handler or stop unrelated processes.
3. Make and verify the documented backup of the closed database, review material,
   configuration, selections and accessible protected captures. Leave previously
   inaccessible capture directories untouched. Execute the documented selection
   switch and hidden watcher start using the verified installed interpreter and
   checkout working directory. Preserve existing retention settings; perform no
   manual expiry or separate bulk ingestion. Normal startup duplicate handling
   does not authorize reprocessing old hashes.
4. Confirm the new process identities, heartbeat, handler instance, installed
   module origins, selected package/pin and unchanged database identity. Check
   runtime/bootstrap logs and genuine existing-Run reporting through the public
   handler. Reuse valid receiving evidence; do not repeat the learner build or
   full ingestion/reporting campaigns.
5. On the next naturally completed new unique capture, verify actual stored
   lineage, capture facts, counts, playset/review availability and reports. Missing
   timestamps must not exclude Runs from ordinary listing, search or reporting;
   only chronological placement is unavailable. If no new capture is available,
   report activation separately from the pending live ingestion/lifecycle check;
   Pipeline retains that follow-up and its concrete next action. Do not generate
   a fake log or claim a completed live lifecycle from process startup alone.
6. If the switch fails, use the documented package rollback at the same safe
   boundary and verify restored operation. Preserve all new captures and Runs.
   Do not restore a database backup over newer records; destructive recovery or
   a materially different deployment requires a separate owner decision. If safe
   rollback cannot proceed, preserve evidence and report the precise obstruction.

## Completion

Update [PIPELINE_CUTOVER.md](PIPELINE_CUTOVER.md), append the activation result to
[PIPELINE_RECEIVING.md](PIPELINE_RECEIVING.md), and update the current status/
handoff pointers. Record actual times, artifact/package identities, processes,
database, backup location, checks and any rollback. Keep historical receipts intact.

State whether production is on the new package, has rolled back, or remains
unchanged; separately state whether new-package live ingestion/lifecycle has been
verified or is still pending. Keep R4's unavailable new-model syntax preset visible
as separately owned Reporting work. R1/R2/R3/R5 receiving is already closed; do not
reopen accepted evidence limits as new activation gates.

No database reset, historical replacement/reprocessing, model rebuild, unrelated
repairs, commit or push. Each synthetic test still requires specific owner
approval; none is authorized here.
