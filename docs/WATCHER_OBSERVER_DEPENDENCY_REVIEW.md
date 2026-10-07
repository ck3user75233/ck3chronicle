# Watcher dependency review before Observer deletion

2026-10-07. Owner-issued [boundary review](task09-deliverables/WATCHER_OBSERVER_BOUNDARY_REVIEW.md),
recorded on existing **TREK-3** for Pipeline's **TREK-6** receiving.
**Necessary Watcher functions do not depend on Observer code or output.**
The bounded deletion below needs no replacement capture, timestamp or playset
behavior. This is a source/evidence review; deletion and release changes have
not been performed or marked complete.

## Required path and file consumption

References are to the inspected working-tree source; line numbers precede deletion.

| Required behavior | Owning source and evidence |
|---|---|
| Identify the configured CK3 lifecycle and log | `watcher.find_process` (watcher.py:306) probes the OS for the exact process name; `WatchState.observe` (:168) tracks process identity. `cli.cmd_watch` (cli.py:87) uses configured `ROOT_LOGS` or `--logs`. `harvester.discover_logs` (harvester.py:84) selects regular, non-symlink `error.log`; `spool_logs` (:96) rejects missing/empty mandatory input. Newness is not derived from Observer measurements: ingestion deduplicates the complete protected log hash. |
| Capture after exit | `watcher.watch_sessions` (watcher.py:479) calls `attempt_capture("process_exit", previous)` only on `game_exited`. Initial absence/attachment and process replacement do not trigger capture. `cmd_watch.perform_capture` (cli.py:178) calls `_spool_once` (:9), then `harvester.spool_logs`, with restart guards, `include_debug=True` and the playset callback. Error bytes are copied first; optional debug/exception failures preserve useful error evidence. Completed `.copying-*` staging is published by directory rename (harvester.py:272). |
| Record the source log timestamp | `harvester._copy_stable_without_hash` (:347) validates source size/mtime before/after the copy and destination size, then returns the **source** stat. `spool_logs` (:166–171, :255) serializes `st_mtime_ns` as UTC `error_log_source_modified_at` with nine fractional digits into `capture-metadata.json`. It also returns `PendingFileStat.source_mtime_ns`. CLI observed start/end and capture time are separate facts. No Observer heartbeat, header timestamp or copied-file fallback supplies this value. |
| Produce active playset JSON | `cmd_watch.create_captured_playset` (cli.py:152) reads the **protected debug.log** through `playset.extract_playset` (playset.py:202). VFS `Mounted Data` emissions determine membership/order; configured game/Steam/local-mod roots and descriptors supply metadata. `harvester.write_playset_template` (:296) hashes both protected logs and atomically writes `playset.json` before directory publication. `PlaysetTemplate.to_dict` (playset.py:40) defines schema 1: both hashes, joined pair ID, capture time and ordered six-field members. Observer never reads debug.log or descriptors and never writes this JSON. |
| Submit and consume protected inputs | `cmd_watch` (cli.py:452–464) wires `WatcherProcessing.start/on_capture/tick`. `_startup` (watcher_processing.py:60) enumerates completed direct children of **pending**, skipping hidden/staging entries; `_ingest` (:91) submits the capture directory through `HandlerClient.submit('ingest', ...)` (request_handler.py:153). Results arrive through handler references, not log files. `database_handler._Handler._prepare` (:233) routes to `ingestion._ingest` (:151). |
| Persist timestamp/playset | `ingestion._ingest` reads `error.log` and `capture-metadata.json`, rejects already stored hashes, and calls `_read_playset` (:72). The latter validates `playset.json`, capture time and both log hashes using protected debug bytes and `playsets.stored_playset` (:16). Metadata becomes `facts=metadata` (:228); `repository.Database.write_run` (:246) stores lossless `facts_json` and normalized playset/member rows (:317). No Observer output is consumed. |

The existing `capture` / `watch --once` routes remain error-only; they are not
the continuous Watcher playset producer. Missing/invalid playsets remain an
explicit unavailable outcome with warnings where applicable, while useful error
evidence can still ingest. Deleting Observer neither changes nor repairs those
existing policies. Daily retention reads capture metadata under pending, not watch
journals (`pipeline.retention.retain_raw_logs`, :34).

## Observer boundary and exact removable code

`logging_observer.observe_logging_progress` (:107) independently probes CK3 and
incrementally reads live **error.log and game.log** for size/mtime/header progress.
It writes only `watch/log-progress-<timestamp>-<pid>.jsonl` (plus rotations) and
replaceable `watch/log-progress-heartbeat-<pid>.json`; the heartbeat is removed on
exit. It does not capture, hash/publish pending evidence, produce playsets, submit
ingestion or record Run facts. Repository-wide symbol/path searches and inspection
of pending enumeration, ingestion and retention found no consumer of those outputs
in the required path. Dependency direction is **Observer -> Watcher** for
`ProcessIdentity` / `find_process`, not Watcher -> Observer.

The later deletion can remove exactly:

1. All of `src/ck3chronicle/logging_observer.py`, including its private JSON writer,
   progress classes, schema/header constants and observation loop.
2. `cli.cmd_observe_logging`, cli.py:502–524, including its local imports and
   result/error printing; and `build_parser`'s entire `p_observe_logging` block,
   :662–675. No shared top-level CLI import needs removal for this deletion.
3. Only `runtime_logging.observer_log_path`, runtime_logging.py:36–37, from the
   active shared backend. Its only active caller is the removed Observer.
4. The `observe-logging` command-list entry in README.md:56 and the matching
   command string in `tests/test_reporting_cli_genuine.py:401`
   (`test_08_existing_commands_and_html_destination`). Preserve the rest of that
   genuine-evidence test; no new test is needed to supply a dependency finding.

**Preserve** Watcher process helpers, `EventJournal`, its lease, and the shared
runtime logging module's configuration/event/path/rotation facilities.
Watcher uses `events-watcher.jsonl`, `events-startup-<pid>.jsonl` and
`watcher-heartbeat.json`; sharing the `watch` directory does not create an
Observer-output dependency. `cli.main` (:720) directly dispatches both owned-stream
commands; `watch` is excluded from `_foreground` and needs no rewiring.
TREK-4's conditional foreground request event does not alter Watcher's caller or
outcome path. This confirms source compatibility, not new installed execution.

## Pipeline receiving and evidence limits

Protected retrieval covered `team-state watcher`, TREK-3/4/6 descriptions,
dependencies and comments, especially later Pipeline CMT-27/CMT-28 and TREK-6
CMT-31. The linked 07D/07E and packaging handoffs were read alongside the Watcher
playset, timestamp and ingestion handoffs. Prior checkpoints remain historical
evidence; this review does not turn pending Observer checks into passed checks.

The retained [2026-10-05 natural lifecycle receipt](learner-next-release/PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05)
and `.codex-tmp/pipeline-refresh-20261005/switch-verification.json` record capture
`20261005T120614.334116Z-ZxGo208o`, subsequent Run `20261005-UYSOEO`, and original
source time `2026-10-05T12:04:29.731991200+00:00`. This is existing genuine evidence
for the unchanged capture path, not a newly executed test or proof of deletion.

Two nonfunctional couplings require ordinary deletion/release accounting:

- `ingestion.application_revision` (:42) fingerprints **all** application Python
  files. Deletion therefore changes future application lineage, wheel membership
  and exact source pins. It does not alter stored facts or require reingestion.
  Pipeline must produce/receive the changed artifact; the existing TREK-6 wheel
  still contains Observer and cannot certify its removal.
- Immutable retained Learner release
  `9c02a343c389aed3d6a4b679b10ac5df01d7dca76e8b1eb991f5138b09c1af12`
  has its own authenticated `ck3chronicle/runtime_logging.py` copy containing the
  unused helper. Do not edit that retained payload in place. Removing the active
  helper changes active/retained backend byte equality; Pipeline/Learner must
  account for this in receiving rather than reuse the old equality assertion.
  No retained consumer of that helper was found.

When deletion is implemented, current command/API and receiving guidance in
07E, RELEASES, the canonical logging deliverables/plan and their Watcher/Pipeline/
Final Packaging prompts must be reconciled with the Owner's deletion decision.
Preserve historical evidence, old Observer files and immutable releases. Record
the disposition of obsolete Observer-only follow-ups on existing TREK-3/4/6;
do not silently mark them verified or close unrelated receiving obligations.

No uncertainty blocks the **inspected-source dependency conclusion**. Arbitrary
external callers and currently loaded processes were not surveyed, and no deletion,
fresh build, installed post-deletion execution, CK3 run, synthetic test, runtime
restart or database operation occurred. Actual deletion/packaging receipt remains
Pipeline's next consuming step. This review introduces no requirement for a new
CK3 run. The source inventory is retained in ignored
`.codex-tmp/watcher-observer-review-20261007/source-before.json`.
