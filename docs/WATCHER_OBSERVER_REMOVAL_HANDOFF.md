# Watcher Observer removal delivery

2026-10-07. Owner issued [Watcher removal](task09-deliverables/OBSERVER_REMOVAL_WATCHER.md)
in the Watcher chat, superseding the earlier Observer integration/verification
requirements. **The independent Observer module is deleted from current source.**
Required Watcher behavior is unchanged. TREK-3 remains open for Pipeline's actual
replacement-candidate receipt under [TREK-6's combined assignment](task09-deliverables/OBSERVER_REMOVAL_AND_RECEIVING_PIPELINE.md).
This is component delivery, not complete application removal or installed receipt.

## Exact deletion and preservation

Deleted only `src/ck3chronicle/logging_observer.py`: **6,849 bytes / 194 lines**,
SHA-256 `8d178a65800d13b9b4f0ea2cd1cc7185192742c2562f6a78692b32c09d29553e`.
This removes `_replace_json`, `LogProgress`, `IncrementalTimestampLog`,
`observe_logging_progress`, private timestamp-header/schema constants and all
Observer measurement/heartbeat machinery. Nothing was transferred to Watcher.

Evidence root **D**: `.codex-tmp/watcher-observer-removal-20261007/` (ignored).

- `before.json` and `before/` preserve exact current bytes of the deleted module
  and edited `docs/WATCHER_ACTIVE_PLAYSET_HANDOFF.md`; the new handoff's prior
  absence is recorded explicitly. They preserve the dirty working-tree version,
  not merely the older Git version.
- `source.patch` is the exact deletion against those saved bytes; SHA-256
  `72758a08797069690b3fc22ecc2ddb7f2b660b1c7a0650c4d2461a21e0b02244`.
- `preservation-before.json` separately records 64 unchanged source/test/guidance
  guards, rather than treating unedited files as rollback payloads.
  `verification.json` records each comparison and the existing evidence identity.
- `delivery.patch`, `after.json` and `delivery-manifest.json` identify the complete
  deletion/documentation delivery, including this handoff's hash. New files are
  represented as additions; there is no replacement Observer implementation.

Any future restoration must reconcile intervening work and the Owner's deletion
decision; these saved bytes preserve evidence, not permission to revive Observer.
Historical logs, old wheels/installations and immutable retained artifacts were
not edited or deleted.

## Required Watcher path remains intact

All 64 guards compare byte-identically. In particular:

| Preserved source | Preserved responsibility |
|---|---|
| `watcher.py` | Exact process helpers, `WatchState`, exit trigger, `EventJournal`, OS lease and Watcher heartbeat. |
| `harvester.py` | Error/debug stable copying, validated original source mtime, `capture-metadata.json`, playset writer and pending publication. |
| `playset.py` | Protected debug VFS extraction, ordered members, descriptor metadata and schema-1 serialization. |
| `cli.py` | `cmd_watch`, `perform_capture`, `create_captured_playset`, `_spool_once`, direct Watcher dispatch and ingestion/tick callbacks. |
| `watcher_processing.py` | Startup discovery, publication submission, public handler references/outcomes and automatic retention triggers. |
| `pipeline/ingestion.py`, `playsets.py`, `repository.py`, `request_handler.py`, `database_handler.py`, `retention.py` | Protected-file consumption, hashes/deduplication, source facts, ordered playset storage and handler/retention interfaces. |
| `runtime_logging.py` | Shared logging configuration/helpers and Watcher paths, unchanged by Watcher. |

The twelve required-path files above also match the source hashes from the
[dependency review](WATCHER_OBSERVER_DEPENDENCY_REVIEW.md). Its explicit call/file
trace remains the dependency evidence. Current-source AST parsing and
`.venv/Scripts/python.exe -B tools/check_runtime_logging.py` passed.
Searches found no exclusively Observer test in Watcher-owned checks to remove.
The Reporting command-list check is Pipeline's assigned edit.

Existing genuine evidence is reused within its original scope:
[2026-10-05 natural lifecycle receipt](learner-next-release/PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05),
with `.codex-tmp/pipeline-refresh-20261005/switch-verification.json` (SHA-256
`010f1133d6c2270c08929d0ca3ffe13d6674f759f2bcb330f17c9fca757ee974`). It records
capture `20261005T120614.334116Z-ZxGo208o`, active Run `20261005-UYSOEO`, source time
`2026-10-05T12:04:29.731991200+00:00` and successful facts/playset receiving.
This review neither reruns that lifecycle nor certifies a newly installed candidate.

## Pipeline coordination and remaining receiving

Protected startup/resumption reads covered Watcher team state and TREK-3/4/6,
including CMT-27/28/31 and dependency-review CMT-32/33. **CMT-34 on TREK-3** records
the pre-deletion scope/transition notice for Pipeline. No other team source or
shared 07E/Task 09/release guidance was edited by Watcher.

At this delivery, Pipeline's remaining source edits are `cmd_observe_logging` and
its parser block in `cli.py`, `observer_log_path` in `runtime_logging.py`, README's
command entry and `tests/test_reporting_cli_genuine.py`'s command-list entry.
The CLI import is temporarily dangling after this module deletion: **do not run
`observe-logging` during this transition**. Pipeline must remove it before claiming
application removal. Refresh actual source and records when receiving.

Observer-only natural lifecycle, replacement, measurements, heartbeat/rotation,
cleanup and Observer sole-stream checks are **removed requirements**, not passed
tests, under the newly issued removal prompt. Earlier pending statements are
historical. No fresh CK3 exercise is required to replace them. Any separate actual
Watcher compatibility is supported here by unchanged source and existing genuine
evidence, not by carrying forward an Observer check under a Watcher name.

Pipeline receives this deletion on **the same TREK-3** against its fresh TREK-6
candidate, reconciles shared guidance and application fingerprints, and verifies
that no Observer implementation/command/helper/embedded retained copy ships.
Learner supplies a newly authenticated distribution; old immutable distributions
stay historical. Pipeline retains external-placement and other unrelated receiving
obligations. No generic Watcher confirmation is requested in place of that concrete
candidate receipt, and this component delivery does not close TREK-3 or TREK-6.

No new CK3 run, synthetic test, ingestion, production change, service restart,
packaging, publication, commit or push occurred. Source preservation is verified;
post-removal installed behavior and final packaging remain unverified here.
