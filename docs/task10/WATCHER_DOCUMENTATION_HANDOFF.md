# Task 10D — Watcher documentation contribution

2026-10-08. **TREK-12**, Watcher → Launch & Distribution / Docs (TREK-11).
Authority: [component assignment](../task10-deliverables/COMPONENT_DOCUMENTATION_INPUT.md),
[10D](../task10-deliverables/10D_PRODUCT_REFERENCE.md),
[10E](../task10-deliverables/10E_USER_WORKFLOWS.md) and
[working agreement](../task10-deliverables/WORKING_AGREEMENT.md).
This is technical input for editorial integration, not a second final manual.
Task 09's completed TREK-3 stays closed. Docs records receipt on TREK-12;
final installed manual acceptance remains 10C.

## TREK-12 follow-up — 2026-10-12

Reference correction **watcher-reference-2026-10-12-r2** supersedes only r1's
retention recommendation below. The default 30-day raw-log retention is intentional
and independent of ingestion success; disabled ingestion with enabled retention is
supported. Repeated ingestion failures call for ingestion diagnosis. CMT-109 remains
the receipt of the original r1 contribution, not receipt of this correction.
Docs has already corrected the canonical manual (TREK-11 CMT-125/150/151).
Its frozen 10D-r2 edition and existing C9/C10 archives are unchanged by this edit.

Protected reads retrieved TREK-12 CMT-122, CMT-134 and later CMT-143, TREK-11's
Owner-clarification account CMT-125 and later delivery, TREK-9's application/cache
delivery and receipts, and TREK-3/10/16. The full 16-record inventory and 282-entry
native history were searched, along with current assignment documents and Watcher
handoffs. **The original Owner-issued stored-Run reconciliation assignment and any
implementation/delivery could not be located in these available records.** The
comments establish a reported Owner request, but none supplies its original scope
or a linked implementation handoff. TREK-3's completed logging/removal work is not
that assignment. No duplicate assignment is created.

The precise missing authority is the original Owner instruction (or its saved
assignment) commissioning a change to Watcher's unavailable-ingestion-result path:
consult persisted Run metadata through the public handler using the full error-log
hash, and handle the resulting stored-Run evidence. That scope must establish what
to do when a Run is found, absent, or cannot be determined, including any retry or
startup behavior it actually requests. These are unresolved scope boundaries, not
new requirements or a proposed recovery design. The existing documentation prompt
expressly excludes product repairs; it cannot supply that authority. The next
action is to recover/link the original instruction on **this TREK-12 follow-up**
and continue only its authorized work. This is not a request for a new assignment.

Read-only source/artifact findings:

- `WatcherProcessing._monitor_results` catches `LookupError`, clears pending,
  scheduled and retry references, and emits `ingestion_outcome_unavailable`.
  It does not call `find_run_by_log_hash` or reconstruct the request result.
  Startup can resubmit a retained error.log through ordinary deduplication.
- The public handler already exposes `find_run_by_log_hash` and `get_run`;
  persisted evidence is distinct from the temporary request outcome. The
  [Pipeline cache handoff](REQUEST_RESULT_CACHE_HANDOFF.md) documents genuine
  persisted hash lookup after cache eviction, not Watcher reconciliation.
- Current Watcher processing bytes match the Task 09 source baseline and the
  delivered **0.0.3** wheel `f03afb5b6abb5d7ee42522d832089d16d20a259374a987ae88dcb0f1a523ee38`.
  No changed Watcher implementation is present in that artifact. The original
  release pins and execution evidence below remain dated 0.0.2/C9 evidence.

Exact protected read snapshots, prior document bytes, source/wheel hashes and
static verification are in `.codex-tmp/task10-watcher-followup-20261012/`.
No runtime, capture, ingestion, retention, handler, production restart or synthetic
test was executed. Pipeline and Docs should retain the accurate unimplemented
reconciliation statement until an actual scoped source/artifact delivery exists.

## Release and integration boundary

Reference revision **watcher-reference-2026-10-08-r1** describes application **0.0.2**,
wheel SHA-256 `2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`,
received on TREK-9 CMT-83. Inspected C9 bundle manifest SHA-256:
`066ae6f7378372074c575cd9c5c8e75257c809ec65575526a0fee7979f9f4aa5`.
Source baseline is `709ea7842a0202c420b43355b18be91d8ca196a3` plus the identified
Task 10 changes; the tag alone does not identify application 0.0.2.

TREK-11 CMT-93 requests these final destinations: `CLI_REFERENCE.md` capture/watch,
`CONFIGURATION_REFERENCE.md` watcher controls and generated capture JSON, and a
10E start/stop cross-reference. Docs owns those files and the coverage/index edits;
Watcher supplies the ready-to-integrate text below without concurrent user-manual
edits. Preserve one canonical final reference. Shared configuration, handler and
logging ownership remain Pipeline's; bundle entry points remain 10B's.

## Reference text: capture and watch

Use a completed setup with readable CK3 logs and writable application storage.
Examples use the installed bundle's `ck3chronicle.cmd` in PowerShell; replace the
example paths with your own. An installed console entry point accepts the same
arguments. Global `--config` precedes the command. Omission selects only
`%LOCALAPPDATA%\ck3chronicle\paths.toml`; there is no current-folder fallback.
Relative TOML paths resolve beside that file. Relative command-line paths resolve
from the terminal's working directory. `--logs` overrides `[paths] root_logs` for
that invocation only; it does not change saved settings or other roots.

```text
ck3chronicle.cmd [--config PATH] capture [--logs PATH] [--log-dir PATH]
ck3chronicle.cmd [--config PATH] watch [--logs PATH] [--process-name NAME]
    [--poll-seconds N] [--heartbeat-seconds N] [--once]
```

Both commands support `-h`/`--help`, which exits 0 without loading configuration
or starting observation. These commands have no JSON-output or format selector.

| Argument | Type / default | Effect |
|---|---|---|
| `--logs PATH` | Directory; configured `paths.root_logs` | Source directory containing `error.log`; continuous watch also attempts `debug.log`. |
| `capture --log-dir PATH` | Directory; `<root_ck3chronicle>/logging` | Foreground invocation journal destination, not capture storage. `watch` has no such flag. |
| `watch --process-name NAME` | String; `ck3.exe` | Exact executable name, case-insensitive, not a path or substring. Also supplies the running-process guard for `--once`. `capture` always guards `ck3.exe`. |
| `watch --poll-seconds N` | Positive number of seconds; `0.5` | Process polling interval; a shorter interval cannot guarantee observing every transition. |
| `watch --heartbeat-seconds N` | Positive number of seconds; `30.0` | Latest-heartbeat update interval; not an ingestion or capture timer. |
| `watch --once` | Flag; off | Copy the current completed session's `error.log` once and exit. Does not enter the continuous watcher. |

### Protect a completed log once

Close CK3 before running `capture` or `watch --once`. Both protect a nonempty,
regular `error.log` and write `capture-metadata.json` beneath
`<root_ck3chronicle>/pending/<capture_id>/`. They do not copy debug.log, create a
playset, hash the log or submit ingestion in that invocation. They do not acquire
the continuous-watcher lease. A running watcher may discover the published input
on its next startup, but does not continuously scan the directory for manual additions.

An empty or missing error log is rejected; an empty log does not become an empty
successful Run. If the source changes during copying or CK3 is seen running again,
the copy is rejected. Partial `.copying-*` material can remain for inspection;
it is not a completed pending input. Originals are read-only.

Success prints two lines and exits 0:

```text
protected pending capture: <absolute pending directory>
copied 1 evidence file(s); hashing and SQLite deferred
```

This is an output-shape example with a substituted path, not a fresh transcript.
The capture ID identifies protected files; it is not a Run ID. Exit 2 means invalid
input (or root CLI/configuration error); exit 3 means a running process, unstable
copy or archive-integrity rejection; other handled capture failures exit 1.
Errors go to stderr. `capture` additionally writes its foreground invocation journal.

These two copyable command examples are **unexecuted on this release**; no genuine
end-to-end receipt for these exact one-shot commands is claimed here:

```powershell
.\ck3chronicle.cmd --config 'D:\CK3ChronicleSettings\paths.toml' capture --logs 'D:\CK3User\logs'
.\ck3chronicle.cmd --config 'D:\CK3ChronicleSettings\paths.toml' watch --once
```

For later processing, use the separately documented Pipeline `ingest` command
with the exact returned capture directory and initialized database. A one-shot
capture lacks captured playset context; do not create that history by editing JSON.

### Observe CK3 lifecycles

```powershell
.\ck3chronicle.cmd --config 'D:\CK3ChronicleSettings\paths.toml' watch
# Bundle shortcut; passes the remaining options to watch:
.\Start.cmd --config 'D:\CK3ChronicleSettings\paths.toml' --heartbeat-seconds 5
```

These are sanitized examples. Applicable genuine prior execution is reused for
the unchanged lifecycle path and installed Start/attachment; no fresh C9 complete
lifecycle was run for this contribution. Start the watcher before CK3 when possible.
It neither launches nor stops the game. If CK3 is already running, it attaches to
that observed process; its observed start time is the attachment time, not a claim
to have seen the original launch. If CK3 is absent, it waits without copying old
live logs. Startup processing of already protected pending captures is separate.

An observed transition from running to absent triggers capture. Switching directly
between process identities records replacement and does not copy a live session.
Windows selects the highest matching PID if several images have the same name;
this is not simultaneous multi-session tracking. Short sessions/restarts between
polls may be missed. Creation time supplements PID identity when obtainable.

After exit, the watcher protects error.log first, attempts debug.log, then extracts
mounted paths from the protected debug copy and hashes both protected logs for
playset.json. It publishes the completed directory before submitting processing.
Descriptor files supply metadata only; CK3 mount emissions determine member order.
No live game/mod/log content is modified.

Missing/failed debug copying preserves the protected error log with
`debug_capture_failure` metadata. A playset extraction/hash/write failure retains
raw evidence without claiming a completed playset. Missing descriptors retain
members with unknown metadata and warnings. Invalid/unstable primary captures are
journaled and observation continues, but there is no automatic retry of that same
missed exit; unexpected capture failures stop observation. These are implemented
branches, not newly executed fault cases.

Continuous watch normally remains silent in the terminal. Inspect
`<root_ck3chronicle>/watch/events-watcher.jsonl` and the latest
`watcher-heartbeat.json`. A heartbeat reports watcher state, not successful ingestion.
`capture_completed` establishes protection; `playset_template_created` establishes
template publication; handler-linked ingestion results establish processing.
`ingestion_accepted` alone does not establish a stored Run. An ordinary duplicate
can return `ingestion_not_completed`, `NOT_COMPLETED`, an existing Run ID and no
error; it does not create another Run. An unavailable outcome stays unavailable.

Press Ctrl+C in the watcher's terminal to request interruption. The implemented
KeyboardInterrupt path stops observation, waits for already submitted work,
removes the heartbeat and releases its OS lease; completion can take time while
requests are pending. It does not manufacture a final capture, stop CK3 or stop the
shared handler. Only one continuous watcher can hold a given runtime's lease.
The `watcher.lock` file can remain after release; file existence alone is not proof
of an active watcher. Forced termination may leave a stale heartbeat.

Handled interruption normally exits 0; startup/lease/probe/runtime failures normally
exit 1, while configuration/argument errors can exit 2. A later zero exit does not
mean every earlier capture or ingestion succeeded: inspect the journal. A second
watcher startup failure has its own `events-startup-<pid>.jsonl` when logging is
available and does not remove the active watcher's heartbeat.

Before changing an existing runtime's configuration or application, stop its watcher,
then use `ck3chronicle.cmd --config PATH runtime-stop` for the handler and restart
with the chosen settings. `runtime-stop` refuses while the watcher lease is held;
it is not a watcher-stop command. Fresh independent setup does not require stopping
an unrelated runtime. No automatic OS startup/service installation is supplied by
`watch`. The removed `observe-logging` command is not part of this interface.

**Evidence limit:** ordinary-console graceful Ctrl+C on the bundle remains
unverified. The existing managed-terminal checks did not deliver a working graceful
stop; their task-only cleanup is not proof of the user stop workflow.

## Reference text: watcher settings and automatic processing

The user-editable authority is TOML. Example values below illustrate the default
controls with a substituted database path; this edit was **not executed**:

```toml
[watcher]
database = 'D:\CK3ChronicleData\runtime\ck3chronicle-schema3-<created-time>.sqlite3'
ingest_enabled = true
retention_enabled = true
maintenance_hours = 24
retention_days = 30
```

| Field | Accepted value / default | Meaning and timing |
|---|---|---|
| `database` | Required nonempty path string; no filename default | Exact initialized current-schema database. Setup supplies its real filename. Required for continuous watch even with both switches false; do not replace the example placeholder literally. Pipeline owns initialization/admission. |
| `ingest_enabled` | TOML boolean, default `true` | Submit completed pending directories at startup and each newly published lifecycle capture. `false` leaves capture active and disables automatic ingestion/retries. |
| `retention_enabled` | TOML boolean, default `true` | Enable deletion of eligible raw error/debug logs during scheduled maintenance. Independent of ingestion. |
| `maintenance_hours` | Positive integer, default `24` | First maintenance is due this many hours after watcher construction, then at this interval while running, including while CK3 is absent. It is not immediate startup retention or a midnight job. Failed ingestion retries share this schedule. |
| `retention_days` | Positive integer, default `30` | Eligible raw-log age measured from capture metadata `captured_at`, not file mtime or source-log timestamp. |

Settings are loaded for the running process and have no live reload. Stop the
watcher/handler before editing an existing runtime and restart to apply changes.
No CLI flags override these four processing/retention controls. Manual `capture`
and `watch --once` do not instantiate automatic processing/maintenance.

Ingestion uses the public shared handler, off the lifecycle polling thread.
Startup scans direct nonhidden, nonsymlink pending directories containing error.log
in name order. In-process submission/result failures may be retried at maintenance;
lost outcomes are recorded without inventing success. Restart can rediscover retained
inputs; Pipeline validation/deduplication decides whether a new Run is created.
The saved model pin applies to new processing through the handler, not retroactively
to stored Runs. Shared model/configuration controls belong in the Pipeline reference.

Retention deletes only expired raw error.log/debug.log from completed pending
directories, under capture locks. It preserves capture/playset JSON, crash attachments,
SQLite history and review shards. **It does not require successful ingestion** and
can expire an unprocessed log even when `ingest_enabled = false`. Keeping
`ingest_enabled = false` with `retention_enabled = true` is a supported
configuration for independent capture and raw-log expiry. The
default 30-day period is intentional. Diagnose repeated ingestion failures through
their results and journals; unsuccessful ingestion does not suspend raw-log expiry.
Hidden staging, busy captures, linked inputs and unusable capture timestamps are
skipped; filesystem dates are not substituted. Disabling retention does not restore
previously removed logs. Pipeline owns the retention implementation and its detailed
eligibility/results contract.

Relevant `[paths]` fields are `root_logs` (live inputs), `root_crashes` (termination
inference/optional exception), `root_game`, `root_steam`, `root_local_mods` (playset
root classification/descriptors), and `root_ck3chronicle` (pending/watch storage).
The shared reference owns all required roots and containment validation. Shared
`[logging]` controls default to `level = 'INFO'`, `max_bytes = 10485760`,
`backup_count = 5`; raising the level can hide ordinary progress events. Watcher
does not supply separate handler/rotation/path settings.

## Reference text: generated capture and playset facts

`capture-metadata.json`, `playset.json`, heartbeat/journal files and stored Run
facts are **generated evidence, not editable behavior controls**. Keep published
capture contents intact. Model/Learner manifests and release-bound rules are also
not runtime configuration. Capture IDs and Run IDs are different identities.

| Capture metadata field | Type / meaning |
|---|---|
| `schema_version`, `capture_id` | Integer `1`; generated capture directory identifier string. |
| `captured_at` | UTC ISO timestamp for this protection operation; also retention's clock. |
| `error_log_source_modified_at` | Original error.log modification time from the stat validated during stable copying, UTC ISO with nine fractional digits and `+00:00`. Not the copied file's date, game exit time or Run processing time. Historical absence is unknown; no backfill. |
| `trigger`, `termination_kind` | `process_exit` or one-shot `manual_capture`; inferred `normal`, `crash` or `unknown`. One-shot termination is unknown. |
| `process` | Lifecycle process object (`pid`, `image_name`, nullable `started_ns`); not supplied by one-shot capture. |
| `observed_started_at`, `observed_ended_at` | Lifecycle observation timestamps, not exact game execution boundaries; absent in one-shot metadata. |
| `crash` | Lifecycle crash association object or null. New matching crash folders between observations support inference; several candidates are labelled ambiguous and newest is selected. Missing/unreadable inventory leaves termination unknown. No new folder yields inferred normal, not proof of a clean game exit. |
| `crash_exception` | Object: status `not_applicable`, `absent`, `unavailable` or `captured`; source/retained relative paths and error details when applicable. Only associated exception.txt is attached. |
| `debug_capture_failure` | Present on failed debug copy, with error and optional partial-file location. Primary error evidence remains useful. |

Pipeline stores received metadata as Run facts. It does not derive an absent
source timestamp from Run identity, processing time or copied-file mtime.
For example, one genuine lifecycle recorded source modification
`2026-10-05T12:04:29.731991200+00:00` and capture
`2026-10-05T12:06:14.334116+00:00`; these describe different facts.

Playset JSON schema 1 contains `error_log_sha256`, `debug_log_sha256` (lowercase
SHA-256 strings of entire protected files), `log_pair_id`
(`sha256:<error hash>:<debug hash>`), `captured_at` and ordered `members`.
It contains no Run ID. The pair ID is not a replacement for Pipeline's error-log
deduplication key.

Each member contains integer `load_order` (base at 0, then consecutive mount order),
string `name` (`CK3 Game Files` for base, `UNKNOWN` if unavailable), string `path`,
nullable `root_ID` (`ROOT_GAME`, `ROOT_STEAM`, `ROOT_LOCAL_MODS`), nullable `stable_id`
(`ck3:1158310`, `pops:<id>`, `steam_workshop:<id>`) and nullable `descriptor_path`.
Outside-root mounts remain with null root identity. No mounts yields base plus a
warning, not inferred mod membership. Names/IDs come from descriptors or applicable
Workshop path IDs; directory names are not fabricated display names. These paths
are captured historical references, not snapshots of mod content or promises that
the source still exists. Reporting's current source lookup has its own limits.

## Evidence, correspondence and outstanding discrepancies

Fresh inspection only: `.codex-tmp/task10d-watcher/inspection.json` records hashes,
commands/stdout/stderr/exits and comparisons; `inspect.py` is its read-only recorder.
The wheel and eight relevant source/C9-installed modules match byte-for-byte.
Four Watcher modules match the 2026-10-05 deployed installation; five CLI capture/
watch functions match its AST. Shared config/entry-point/logging changes are checked
against 0.0.2 itself, not claimed byte-identical to the older release.

| Example / claim | Applicable evidence and limit |
|---|---|
| `capture --help`, `watch --help` | Fresh staged C9 private-Python execution from `C:/Windows`, both exit 0, stderr empty. Syntax only; does not prove command effects. |
| Full lifecycle, capture/source facts, stored result | Reused `.codex-tmp/pipeline-refresh-20261005/switch-verification.json`, SHA-256 `010f1133d6c2270c08929d0ca3ffe13d6674f759f2bcb330f17c9fca757ee974`. Real CK3 PID 53004 start/exit, capture `20261005T120614.334116Z-ZxGo208o`, two protected files, active Run `20261005-UYSOEO`. Older package/receiving context; establishes unchanged Watcher behavior, not fresh C9 end-to-end acceptance. |
| Installed start/attachment, startup duplicate and runtime-stop refusal | Reused `.codex-tmp/task10b/verification-candidate3-final/watcher-check.json`, SHA-256 `3e89301bc435af25b26f72f1cc4fe112bc66c182327e89a052e1d71e185cd0c3`, and [10B handoff](DISTRIBUTION_HANDOFF.md). Genuine Start.cmd attachment, duplicate existing Run `20261008-W4UVWM`, same application wheel. Managed-terminal graceful stop unsuccessful; task-only forced cleanup and subsequent handler stop recorded. |
| Captured playset and preserved stored facts on 0.0.2 | TREK-9 CMT-81/83; [Pipeline handoff](PIPELINE_HANDOFF.md), `.codex-tmp/task10a1/release/{artifact.json,stored.json,verification.json}`. Genuine captured input `20261003-D3N7ZQ`, public-handler receiving. Ingestion of retained input, not a new capture. |
| Example playset membership | Reused `.codex-tmp/watcher-playset-implementation/native-verification.json`, SHA-256 `f862b796cd8c6169ebc475fddcf4605106a8db4b7c38d3604ceb205b832a0592`: 133 members, zero unknown names/warnings on genuine protected log pair. Historical native-input demonstration, not current source availability or a new lifecycle. |
| One-shot capture/once, edited controls, timed retention, failure branches | Source/installed contract inspection only for this contribution; no fresh execution, mock/fault fixtures or deletion. Older synthetic checks are not promoted to genuine user-workflow evidence. |

No newly established product defect is identified. Documentation drift to avoid:
the older [playset handoff](../WATCHER_ACTIVE_PLAYSET_HANDOFF.md) says either copy
failure prevents publication and cites `events-*.jsonl`; current implementation
publishes error-only evidence on expected debug failure and uses the shared
`events-watcher.jsonl` path. Its old pending receiving statements are superseded
by TREK-3's receipt and the current application receipts, not grounds to reopen it.
`watch --once` help says completed-session logs but the actual operation is error-only;
this contribution explicitly documents that boundary rather than changing code.

Docs should preserve the ordinary-console stop and fresh-C9-lifecycle limits in
its coverage inventory and coordinate genuine workflow evidence under 10D/10E/10C.
Watcher owns factual corrections to this input; product repairs require their
own issued scope. No source/runtime edit, capture, ingestion, retention execution,
service restart, build, publication or synthetic test was performed here.
