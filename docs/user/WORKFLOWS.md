# Everyday workflows

[Manual index](README.md) · [Commands](CLI_REFERENCE.md) ·
[Settings](CONFIGURATION_REFERENCE.md) · [External data](EXTERNAL_DATA.md)

For **ck3chronicle 0.0.3 for Windows x64**. Examples use PowerShell in the extracted
application folder. Replace the illustrative paths with your saved settings and
returned database. Sample output illustrates genuine stored evidence; your IDs
and totals will differ.

```powershell
$config = 'D:\Chronicle\settings\paths.toml'
$database = 'D:\Chronicle\data\runtime\<filename returned by setup>.sqlite3'
$runtime = Split-Path -Parent $database
$package = '2b12932103f3a3111a4e1880'
```

Keep using the same `--config` before each subcommand. Omitting it selects only
`%LOCALAPPDATA%\ck3chronicle\paths.toml`; it does not remember a different file
chosen in setup. Relative TOML paths resolve beside that file; relative command
arguments resolve from the terminal's working directory.

## Set up, or revisit your settings

Complete [Installation and launch](INSTALLATION.md) before using these workflows.
Keep the returned configuration and database paths. To revisit settings, stop
that setup's watcher and handler, then follow
[repeat setup](INSTALLATION.md#revisit-settings-move-the-application-or-recover-a-save).

## Observe a game session and stop observation

Use a completed setup. Start before launching CK3 when possible:

```powershell
.\Start.cmd --config $config
```

Leave the terminal open, launch CK3 normally, play, and exit the game. The watcher
is normally quiet and waits for the configured CK3 process. If CK3 is already
running, its observed start is the attachment time. Transitions between polls
can be missed. For observation at sign-in, use the optional Windows startup route
in [Installation](INSTALLATION.md).

After an observed exit, expect a protected directory under `$runtime\pending`,
capture metadata, and attempted debug-log/playset capture. With ingestion enabled,
the watcher submits the protected input for processing. Missing debug/playset
evidence remains explicitly unavailable. Startup can also submit existing
protected captures. Configured retention is separately scheduled and can remove
eligible raw logs while preserving stored diagnostic history.

Check `$runtime\watch\events-watcher.jsonl` and `watcher-heartbeat.json`:
`capture_completed` establishes protection, not a stored Run. Follow the handler
result and use `runs`/`report` below to establish processing. A heartbeat only
establishes observer state. See [execution logs](#find-and-read-execution-logs).

To stop, press **Ctrl+C in the watcher's terminal** and wait for the command to
return. Pending work can take time. This does not stop CK3, manufacture a final
capture or stop the database handler. Then, before changing settings/model or
application files:

```powershell
.\ck3chronicle.cmd --config $config runtime-stop
```

Expected output, with a substituted path:

```text
Handler stopped or absent: D:\Chronicle\data\runtime\<database>.sqlite3. New requests may start it again.
```

`runtime-stop` refuses while the watcher holds its lease. It is not a watcher-stop
command. Shutdown can reject unfinished requests; inspect outcomes before assuming
everything committed. A later report can start a handler again. An existing lock
file by itself does not prove a watcher is running; do not delete files to bypass
an active lease.

If Ctrl+C fails to return, retain the logs and avoid changing that runtime's settings. Seek help with the command, configuration path and relevant logs.

## Process an already captured log

You need the initialized database and a completed protected capture directory
containing `error.log` and whatever metadata/playset was actually captured.
Use the directory reported by capture, not partial `.copying-*` material.
Keep its original metadata/playset; do not edit hashes or supply invented facts.

```powershell
$capture = 'D:\Chronicle\data\runtime\pending\<completed capture directory>'
.\ck3chronicle.cmd --config $config ingest --database $database --capture-directory $capture
```

Expected: JSON `status: COMPLETED`, a Run ID and exit 0. Save the returned ID and
verify it with a report. Example output, shortened to returned fields:

```json
{"status":"COMPLETED","run_id":"20261008-01PBM7","log_sha256":"5a7b93d8ee374c60f767593631713eaf8719004ba4f9cf33e7eb5d812dbec629"}
```

The example capture produced **1,066 records / 1,838 occurrences** with its
original observed times and 133 playset members. IDs and totals will differ for
your log. The capture-directory name and metadata Capture ID identify the input;
the returned Run ID identifies its stored processing result.

Ingest reads the saved model pin unless `--package-id` explicitly overrides it.
Duplicate full log content in the same database returns the existing Run ID,
`NOT_COMPLETED` and exit 1, even with a different requested model. It does not
create a second Run or reclassify history. Other failures also use exit 1; inspect
`error`, `warnings`, `details` and journals rather than interpreting the code alone.

For a standalone complete, stable log, the supported alternative is:

```powershell
.\ck3chronicle.cmd --config $config ingest --database $database `
  --error-log 'D:\ProtectedInputs\error.log' --captures-root "$runtime\pending"
```

Standalone ingestion records the evidence supplied by the log. Observed lifecycle
and paired playset facts come from continuous watcher capture. To protect the
current log once after CK3 exits, `capture` or `watch --once` copies `error.log`
and defers ingestion. See [capture](CLI_REFERENCE.md#capture).

## Find a Run and investigate diagnostics

List Runs for the processing package you want to investigate. Choose the report's
historical package scope explicitly, using the package recorded for those Runs.

```powershell
.\ck3chronicle.cmd --config $config runs --package-id $package --format json
$run = '20261008-01PBM7' # Replace with your returned Run ID.
.\ck3chronicle.cmd --config $config report $run --preset frequent --limit 5
```

Example text output:

```text
Run 20261008-01PBM7: 1066 different diagnostics, occurring 1838 times. 5 diagnostics are displayed; counts include every match.
```

Start with the report's question, actual result, totals and coverage. Frequency is
not severity. A record represents an exact stored diagnostic identity; one record
can occur repeatedly. `template` and `provisional` are assignment statuses, not
severity or numeric confidence. Unresolved review evidence is separate.

Use `hotspots` for stored source references and `new` for newness within the
available comparison window. For an exact investigation save a query as UTF-8 JSON
in a user folder, for example `D:\Queries\message.json`:

```json
{"refinement":{"message":{"contains":"failed context switch"}},"analytics":{"history":false}}
```

```powershell
.\ck3chronicle.cmd --config $config report $run --custom --query 'D:\Queries\message.json' --format json
```

The example query has zero matches in the illustrated Run. Successful empty
output is a valid finding. Change the literal phrase to investigate your own
stored messages. [Report queries](REPORT_QUERY_REFERENCE.md) explains typed
bindings, source filters and combinations. Use `frequent`, `hotspots`, `new` or
a custom query with the supplied package; `syntax` requires its older named model.

Current source lookup uses captured playset references or explicitly supplied roots.
Missing paths/descriptors stay missing; installed mods may have changed since the
Run. Engine emitters such as `.cpp` names are not script-file paths. A present-day
excerpt is not a historical snapshot or proof that a mod caused the diagnostic.

## Compare Runs

Keep one package scope and select a real Run. A normal report includes its
available comparison window; named Runs can be inspected even if their source
timestamp is absent. `latest` needs usable source chronology and an explicit package:

```powershell
.\ck3chronicle.cmd --config $config report latest --package-id $package --preset frequent --limit 5
```

Read **All matches by Run**, the selected position, previous/next positions and
the previously observed entries absent now. Chronology uses the original
error-log modification timestamp, not processing date or the Run ID. Missing
positions/failed reads are unavailable, not zero. A successful read that lacks an
identity can establish zero within that Run. Newness is relative to the included
predecessors; it does not establish a globally first occurrence, fix or regression.

The first illustrated database contains one Run, so other comparison positions
are unavailable. The following example uses genuine history under retained package
`4ac4e8ee92346e6d14eacfbf`. History queries stay within one package. For window
controls and identity meaning use [history rules](REPORT_QUERY_REFERENCE.md#history-and-display).

Example comparison for Run `20261005-BND9AS`:

| Position | Run | Diagnostic records | Occurrences |
|---|---|---:|---:|
| Previous available Run | `20261005-OSPK8G` | 3,315 | 12,811 |
| Selected Run | `20261005-BND9AS` | 3,211 | 59,313 |

Its report also identified 541 earlier identities absent from the selected Run.
These figures describe that evidence; they do not establish cause or a regression.
The other requested positions were unavailable, and an additional same-package
Run without source time could be listed but not placed chronologically.

## Save reports for later or for another tool

Use new output filenames; existing named targets are overwritten. These commands
create parent folders when needed:

```powershell
.\ck3chronicle.cmd --config $config report $run --preset frequent --limit 5 --format text --output 'D:\Reports\frequent.txt'
.\ck3chronicle.cmd --config $config report $run --preset frequent --limit 5 --format json --output 'D:\Reports\frequent.json'
.\ck3chronicle.cmd --config $config report $run --preset frequent --limit 5 --format html --output 'D:\Reports\frequent.html'
```

JSON retains structured query/results; arrays can be display limited even when
totals include every match. Keep the query separately if you want to rerun it.
HTML requires `--output`; open it in a browser and read the explanation/evidence
before following diagnostic and source links. A verbose report can create a
sibling `-sources.html` appendix; keep it with the report. Text and JSON can also
print to stdout. A report is a dated result, not a full database backup. For SQL
and modest JSON extraction see [external data](EXTERNAL_DATA.md).

## Inspect or change the selected model

Read the saved `[model]` values using setup preview. Use `--list-models` to
inventory the available installed releases and shipped default:

```powershell
.\ck3chronicle.cmd --config $config setup --format json
.\ck3chronicle.cmd --config $config setup --list-models --format json
```

After stopping observation and running `runtime-stop`, choose an authenticated
available package ID, preview it, then apply the intended change:

```powershell
$chosenPackage = '<available package ID from the inventory>'
.\ck3chronicle.cmd --config $config setup --package-id $chosenPackage --format json
.\ck3chronicle.cmd --config $config setup --package-id $chosenPackage --apply --format json
```

Check returned `model.package_id` and `manifest_sha256`, then restart observation
when wanted. New processing uses that pin; old Run lineage and diagnostics do not
change. Reverting uses the same procedure with the prior available package ID.
Do not edit immutable model/rule files or treat catalog publication order as a version.

## Find and read execution logs

The live CK3 `error.log` is input evidence. CK3Chronicle's JSONL files record its
own operations. Find `paths.root_ck3chronicle` in saved settings to locate your
runtime logs.

| Location below the configured runtime | What to inspect |
|---|---|
| `logging/<command>-<invocation_id>.jsonl` | Foreground setup, capture, ingest, runs and report invocations. A command's `--log-dir` can override its destination where supported. |
| `logging/<database filename>/handler.jsonl` | Handler request acceptance, terminal results and shutdown. |
| `watch/events-watcher.jsonl` | Lifecycle, capture, playset, ingestion and maintenance events. |
| `watch/watcher-heartbeat.json` | Latest watcher state; not a history of completed processing. |

Read doctor findings from its command output. Logs for other operations rotate
according to `[logging]`; older events may be in adjacent numbered backups.
Use the events actually retained when investigating an outcome. Use PowerShell
to inspect one recent report invocation:

```powershell
$journal = Get-ChildItem -LiteralPath "$runtime\logging" -Filter 'report-*.jsonl' |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1
Get-Content -LiteralPath $journal.FullName | ForEach-Object { $_ | ConvertFrom-Json } |
  Select-Object timestamp_utc,severity,event,operation,invocation_id,request_id,handler_instance
```

Read the first and terminal events, plus warnings/errors. Correlate a foreground
`request_id` **and** `handler_instance` with the handler journal. Acceptance means
queued work; a terminal result and the stored Run/report establish outcome.
Record Run ID, command, settings path and relevant journal when seeking help;
remove private paths/content before sharing.

## Preserve data and recover after an interrupted setup

If setup initialized a database but failed to save configuration, retain the exact
returned path and effects. After ensuring setup is no longer running, retry with
that file and the same roots through `.\Setup.cmd --config $config --database $database`.
Do not reset storage or guess another database.

The [read-only SQLite route](EXTERNAL_DATA.md#connection-and-writer-conditions)
is live access, not a backup. A complete evidence set also includes protected
captures, native review files, settings, retained resources and other external
evidence. An arbitrary copy during writes is not a consistent export. Retention
can remove raw logs; stored diagnostics cannot reconstruct the original `error.log`.
See [Planned Features](PLANNED_FEATURES.md) for guided backup and restore.

[Manual contents](README.md)
