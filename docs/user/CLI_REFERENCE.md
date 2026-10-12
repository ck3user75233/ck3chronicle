# CLI reference

Application 0.0.3. Examples assume the extracted application folder and an existing
configuration created by [setup](INSTALLATION.md). These variables stand for your
chosen paths and a real completed capture:

```powershell
$config = 'D:\Chronicle\settings\paths.toml'
$database = 'D:\Chronicle\data\runtime\<database filename returned by setup>'
$capture = 'D:\Chronicle\data\runtime\pending\<completed capture ID>'
$package = '2b12932103f3a3111a4e1880'
```

Replace angle-bracket placeholders before running an example. `--config PATH`
is global and precedes the subcommand. It selects exactly that file; omission
uses only `%LOCALAPPDATA%\ck3chronicle\paths.toml`. A missing or invalid file
does not cause a search. Relative CLI paths use the invocation directory;
relative paths inside TOML use the file's parent. Each command accepts `--help`.
Installed Python entry point `ck3chronicle` has the same application syntax as
the bundle's `.\ck3chronicle.cmd`.

| Command | Audience and effects |
|---|---|
| `setup` | Users: inspect, initialize settings/storage, select a model |
| `doctor` | Users: diagnose configuration without writing state |
| `runtime-stop` | Operators: explicitly stop the configured database handler |
| `capture` | Operators: protect a completed `error.log`; defer processing |
| `watch` | Users/operators: observe CK3, capture and optionally ingest/retain |
| `ingest` | Operators: process captured or explicitly selected input into SQLite |
| `runs` | Users: list stored Runs for one explicit package |
| `report` | Users: investigate stored diagnostics; optionally read current sources |

`capture`, `ingest`, `runs` and `report` accept `--log-dir PATH`. It overrides the
invocation-journal directory for that command; default is `<runtime>/logging`.
Even read-only database queries can start the handler and write execution journals.
Only doctor and setup inspection/preview avoid those runtime side effects.
Configuration/argument errors normally exit 2; command-specific codes follow.

## Setup

```text
ck3chronicle [--config PATH] setup [--format text|json]
  [--suggest-paths | --list-models | --apply]
  [--data-root PATH] [--root-game PATH] [--root-steam PATH]
  [--root-local-mods PATH] [--root-logs PATH] [--root-crashes PATH]
  [--database PATH] [--package-id ID] [--ripgrep PATH]
  [--accept-path FIELD ...]
```

Format defaults to text. `--suggest-paths` returns editable bounded Windows
Known Folder/Steam suggestions without accepting them. `--list-models` reports
available authenticated packages and the shipped default. Both work without a
saved configuration. With neither flag nor `--apply`, the command validates a
preview and writes nothing. `--apply` validates then saves settings and initializes
storage when necessary; it starts neither watcher nor CK3.

| Input | Meaning and omitted behavior |
|---|---|
| Five `--root-*` external fields | Full machine-specific paths; existing values are reused, otherwise supply/confirm actual suggestions. See [fields](CONFIGURATION_REFERENCE.md#toml-fields). |
| `--accept-path FIELD` | Repeat for each new/changed external root: `root_game`, `root_steam`, `root_local_mods`, `root_logs`, `root_crashes`. Unchanged saved fields keep their acceptance. |
| `--data-root PATH` | Writable data parent; first-use default LocalAppData/ck3chronicle/data. Existing roots are preserved; this is not a data migration command. |
| `--database PATH` | Exact existing current-schema file; omission initializes only for a new empty runtime, then persists the returned filename. Never discovers existing databases. |
| `--package-id ID` | Authenticate and persist that available model pin. Repeat setup preserves the existing selection when omitted. |
| `--ripgrep PATH` | Persist source-content search executable; omission preserves existing value. |

Example first-use preview (replace all external paths):

```powershell
$setupArgs = @(
  '--data-root', 'D:\Chronicle\data',
  '--root-game', 'D:\SteamLibrary\steamapps\common\Crusader Kings III\game', '--accept-path', 'root_game',
  '--root-steam', 'D:\SteamLibrary\steamapps\workshop\content\1158310', '--accept-path', 'root_steam',
  '--root-local-mods', 'D:\CK3User\mod', '--accept-path', 'root_local_mods',
  '--root-logs', 'D:\CK3User\logs', '--accept-path', 'root_logs',
  '--root-crashes', 'D:\CK3User\crashes', '--accept-path', 'root_crashes',
  '--package-id', $package, '--format', 'json'
)
.\ck3chronicle.cmd --config $config setup @setupArgs
# After reviewing the preview:
.\ck3chronicle.cmd --config $config setup @setupArgs --apply
.\ck3chronicle.cmd setup --suggest-paths --format json
.\ck3chronicle.cmd setup --list-models --format json
```

JSON exposes `config`, `paths`, `database`, `model`, `findings`,
`acceptance_required`, `effects`, `applied` and `restart_required`. Findings give
severity, evidence, consequence and correction. Exit 0 is valid preview,
successful Apply or inventory; 2 is invalid input/precondition; 1 is operational
Apply failure. Missing optional mod/crash locations may produce warnings;
game/log directories must be readable. Missing current error.log alone is allowed.

Apply creates configuration/data parents, disjoint runtime/Learner trees,
database/review scaffolding, locks and a setup journal as required. It serializes
setup for that file and refuses an active watcher/handler. Repeat preserves
database, captures, review, model and unrelated settings. It rewrites comments.
On partial failure inspect `effects`; use the exact returned database with
`--database` if saving settings failed after initialization. An interrupted
`.setup-lock` requires inspecting effects and confirming its process exited
before removing that single lock. There is no automatic stale-lock takeover.

## Doctor

```powershell
.\ck3chronicle.cmd --config $config doctor --format json
```

Only option: `--format text|json`, default text. Checks configuration, CK3 layout,
paths, containment, database schema, model pin, controls and tools. It creates
no config, database, probe file or journal and starts no handler. Exit 0 means
all checks healthy; 2 includes warnings and unverified checks as well as errors.
Read-only write-access checks normally remain unverified. Tool existence does
not establish its executable version. Inspect individual findings.

## Runtime stop

```powershell
.\ck3chronicle.cmd --config $config runtime-stop
.\ck3chronicle.cmd --config $config setup --package-id $package --apply
```

No command-specific options. Stop the watcher first. This obtains the watcher
lease and asks the current database's existing handler to shut down, without
starting an absent one. Exit 0 prints `Handler stopped or absent: ...`; failures
exit 1, configuration errors 2. Shutdown stops admission and can reject unfinished
requests; it does not certify that all requests committed. Protected captures
remain. New requests can launch a handler again. Processes retain loaded settings,
so restart them after a settings/model change. Historical Runs are unchanged.

## Capture

```powershell
.\ck3chronicle.cmd --config $config capture --logs 'D:\CK3User\logs'
```

`--logs PATH` overrides `paths.root_logs`; `--log-dir PATH` sets the invocation
journal. Use a stable, nonempty completed `error.log` after `ck3.exe` has stopped.
The command protects an error-log copy and capture metadata beneath runtime
`pending/` and prints its directory and copied-file count as text. Hashing,
classification and SQLite storage happen during later ingestion.

Use continuous watch to capture paired debug-log/playset evidence and observed
lifecycle facts. `capture` and `watch --once` operate independently of the
continuous watcher lease. Submit their completed captures with `ingest`, or let
the continuous watcher discover them on its next startup scan. An already-running
watcher does not continuously scan for manual additions. Partial `.copying-*`
material is not a completed capture.

Exit 0 means protected capture, 2 invalid input, 3 running/restarted CK3,
unstable input or archive-integrity rejection, 1 other failure. A failed capture
can retain staging evidence. Do not treat a protected copy as an ingested Run.

## Watch

```text
ck3chronicle [--config PATH] watch [--logs PATH] [--process-name NAME]
  [--poll-seconds N] [--heartbeat-seconds N] [--once]
```

`--logs` overrides the configured logs folder; exact process name defaults to
`ck3.exe` (case-insensitive exact executable name, not a path/substring). Poll
interval defaults to **0.5 seconds**, heartbeat **30 seconds**;
both are positive floating-point values for continuous observation. Foreground
observation uses the configured runtime lease and journal. Starting may submit
existing completed pending captures and schedule retention according to
`[watcher]`. External CK3 and mod content stays read-only.

```powershell
.\ck3chronicle.cmd --config $config watch --poll-seconds 0.5 --heartbeat-seconds 30
# Alternative one-time, error-only protection after CK3 has stopped:
.\ck3chronicle.cmd --config $config watch --once
```

Continuous watch protects `error.log` and `debug.log` after observed exit, records
available lifecycle facts, and derives hashed playset evidence from the captured
pair. Processing is a separate outcome. Missing/uncertain observations remain
unavailable. Ctrl+C stops foreground observation; journal outcomes, including
capture/processing failures, must be inspected. Normal stop returns 0, startup
or runtime failure 1. `--once` uses manual error-only capture, without continuous
lifecycle/playset processing, and uses capture's 0/1/2/3 result codes. Poll and
heartbeat controls are not capture/ingestion timers.

Start before CK3 when possible. Attaching to an already-running game records
attachment time as observed start. When CK3 is absent, startup waits without
capturing old live logs. Direct process replacement is recorded without copying
a live session. Multiple matching images select the highest PID; this is not
multi-session tracking. Transitions between polls may be missed.

Failed/missing debug copying preserves the primary error log with
`debug_capture_failure` metadata. Playset extraction/hash/write failures retain
raw evidence without claiming a playset. Missing descriptors keep members with
unknown metadata and warnings. Invalid/unstable primary captures are journaled
and observation continues without automatic retry of that exit; unexpected
capture failures stop observation.

Continuous watch normally stays silent in the terminal. Read
`<runtime>/watch/events-watcher.jsonl` and `watcher-heartbeat.json`.
`capture_completed` proves protection; `playset_template_created` proves playset
publication; `ingestion_accepted` alone does not prove a stored Run. A duplicate
can report `ingestion_not_completed` with an existing Run and no error. A heartbeat
reports watcher state, not ingestion success.

Ctrl+C waits for submitted work, releases the OS lease and removes the heartbeat.
CK3 continues running, and this stop does not create a final capture. A remaining
`watcher.lock` file does not prove an active lease. Forced termination can leave
a stale heartbeat.

## Ingest

```text
ck3chronicle [--config PATH] ingest --database PATH
  (--capture-directory PATH | --error-log PATH)
  [--captures-root PATH] [--package-id ID] [--log-dir PATH]
```

The database must already exist; this command requires its explicit path.
`--capture-directory` selects one completed protected capture. `--error-log`
selects a manual complete log; `--captures-root` is required for an unprotected
manual input and names its protected pending
storage. A manual raw input lacks observed lifecycle/playset evidence unless
actually supplied through the capture mechanism. Do not point at a changing log.
`--package-id` overrides the saved default for this invocation; omission uses
the saved model pin in configuration. The shipped catalog default does not
replace that saved selection.

```powershell
.\ck3chronicle.cmd --config $config ingest --database $database --capture-directory $capture
.\ck3chronicle.cmd --config $config ingest --database $database `
  --error-log 'D:\ProtectedInputs\error.log' --captures-root 'D:\Chronicle\data\runtime\pending'
```

Validates/hashes input, deduplicates by full log SHA-256 within the database, classifies through
the selected retained package, writes compact SQLite records and preserves
unresolved evidence in a per-Run native review shard. A duplicate returns the
existing Run ID with `NOT_COMPLETED` and exit 1, even if another package was
requested; it does not reprocess stored history. JSON stdout includes
`status`, `run_id`, `log_sha256`, `capture_directory`, `warnings`, `error`,
`exception_class`, `details`. Exit 0 requires `COMPLETED`; other terminal outcomes
exit 1. Admission/retrieval exceptions write error JSON to stderr and exit 1;
they do not establish a terminal request outcome. Inspect the stored Run for
lineage/counts; a stdout success message alone is insufficient evidence.

### Request results and stored ingestion

A public ingestion request covers **one whole captured log**, including its
diagnostics and associated Run evidence. It is not a request per diagnostic row.
The handler's temporary completed-result cache also serves other public
operations. Outstanding requests are not evicted by its completed-result limit.
Evicting a completed result removes that request's cached response, not stored
Runs, diagnostic rows or review evidence. Request references belong to a handler
instance and are not durable ingestion records.

Persisted Run metadata and the log's full content SHA-256 establish whether that
protected log has been ingested into the selected database. The public handler
provides `find_run_by_log_hash`; stored Run details provide its identity and
lineage. An unavailable request result does not establish that ingestion failed
or that no Run exists. The temporary request list is not the only source of
ingestion information, and finding a stored Run does not recreate the original
request response. When an unchanged retained log is submitted again, normal
hash-based deduplication returns its existing Run instead of creating another.

**Application 0.0.3 retains 1,024 completed public request results** per handler
instance. Completion order controls eviction; reading a result does not extend
its lifetime in the cache.

In application 0.0.3, the watcher records an unavailable request outcome without
automatically reconciling it against stored Run metadata. On restart, its startup
scan can rediscover retained logs and normal ingestion deduplication applies.

This temporary cache and request recovery are separate from the configured
[raw-log retention period](CONFIGURATION_REFERENCE.md#automatic-processing-and-raw-log-retention).

## Runs

```powershell
.\ck3chronicle.cmd --config $config runs --package-id $package --format json --limit 50
```

Requires explicit `--package-id ID`. Optional `--database PATH` overrides the
configured database. `--offset` is a nonnegative integer (0 default), `--limit`
a nonnegative integer (50 default). `--format text|json` defaults to text;
`--output PATH` writes UTF-8 instead of stdout, creating parents. `--log-dir`
overrides the invocation journal. Lists stored package Runs, including entries
whose source dates are unavailable, with eligibility/chronology information.
It does not select the active model. Empty lists succeed. Exit 0 success, 2
invalid selection/query, 1 database/export/operation failure.

## Report

```text
ck3chronicle [--config PATH] report RUN_ID_OR_latest
  (--preset hotspots|frequent|syntax|new|symbol | --custom)
  [--query JSON] [--package-id ID] [--database PATH]
  [--format text|json|html] [--output PATH] [--limit N]
  [--historical-limit N] [--no-history] [--verbose]
  [--source-context JSON] [--source-root PATH ...]
  [--source-directory RELATIVE ...] [--no-recursive] [--ripgrep EXE]
  [--log-dir PATH]
```

| Argument | Meaning / default |
|---|---|
| Run operand | Named stored Run, or `latest` within explicit `--package-id`. Named Run supplies its stored package; a conflicting supplied package is rejected. |
| `--preset` / `--custom` | Exactly one. Custom requires `--query`; preset queries refine its base condition. |
| `--query PATH` | UTF-8 JSON object, BOM accepted; see [query reference](REPORT_QUERY_REFERENCE.md). |
| `--database PATH` | Existing database override; otherwise configured database. |
| `--format`, `--output` | text default, json or offline html. HTML requires output. Text/JSON default stdout. UTF-8 files overwrite the named target and create parents. |
| `--limit N` | Nonnegative selected/per-Run display bound, default 50; CLI overrides JSON. Totals are computed before truncation. |
| `--historical-limit N` | Separate previously observed display bound, default 20; CLI overrides JSON. |
| `--no-history` | Omit comparisons; conflicts with trailing/newness queries. |
| `--verbose` | Numbered current-source excerpts; HTML may write a sibling `-sources.html` appendix. Keep it with the main report. |
| `--source-context PATH` | Optional source-selection JSON, separate from required diagnostic filters. |
| Repeated `--source-root PATH` | Explicit absolute context roots in caller order; overrides context JSON roots. |
| Repeated `--source-directory RELATIVE` | Directories beneath every selected root; overrides context JSON directories. |
| `--no-recursive` | Set optional context recursion false; otherwise source default true. |
| `--ripgrep EXE` | Overrides configured source-content search executable for this report. |

Required `scope.source` query fields override same-named optional context fields.
Report destinations cannot overwrite the database or query/context inputs.
Writing a report does not change diagnostic history; journals/handler state and
explicit output files are side effects.

```powershell
.\ck3chronicle.cmd --config $config report latest --package-id $package --preset frequent --limit 5
.\ck3chronicle.cmd --config $config report latest --package-id $package --preset hotspots --format html --output 'D:\Reports\hotspots.html'
.\ck3chronicle.cmd --config $config report latest --package-id $package --preset new --format json
.\ck3chronicle.cmd --config $config report latest --package-id $package --custom --query 'D:\Queries\message.json' --format json
.\ck3chronicle.cmd --config $config report latest --package-id $package --preset symbol --query 'D:\Queries\symbol.json'
# Only for a Run stored under the syntax preset's supported package:
.\ck3chronicle.cmd --config $config report latest --package-id 68f1ae5db205ab46afef9c4d --preset syntax
```

The syntax preset is restricted to the shown older package/model; it is
unavailable for the shipped default model. It is not an exhaustive syntax checker.
The query reference provides the `message.json`/`symbol.json` content and explains
each preset, counts, history and source evidence.

Exit 0 includes empty results; 2 means invalid query, unsupported preset package
or unknown/ineligible/conflicting Run; 3 means a required source filter could not
be evaluated completely; 1 means read/export/operation failure. Structured failures
include `status`, `error`, `exception_class` and normally `failure_stage`; inspect
partial evidence rather than treating unknown as zero.

Example output from a stored Run, shortened to its totals (values unchanged).
Its five displayed records are a detail limit, not the total. Your counts depend
on your selected Run.

```json
{"status":"completed","totals":{"occurrences":1838,"distinct_records":1066,"historical_entries":0}}
```

## Other installed commands

[Installation](INSTALLATION.md) covers `Setup.cmd`, `Setup-Text.cmd`, `Start.cmd`
and `Verify.cmd`. [Release reference](RELEASE_REFERENCE.md) covers both advanced
installed entry points and all seven retained Learner operation names.
For task sequences, use [user workflows](WORKFLOWS.md).

[Manual contents](README.md)
