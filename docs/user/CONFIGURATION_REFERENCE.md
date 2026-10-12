# Configuration reference

Application 0.0.3. Use [setup](CLI_REFERENCE.md#setup) to initialize paths,
database and model selection. This reference also covers editable
[report-query JSON](REPORT_QUERY_REFERENCE.md); those files are separate from
installation settings.

## Authority, paths and changes

`ck3chronicle --config PATH ...` uses exactly that TOML file. Without the option,
only `%LOCALAPPDATA%\ck3chronicle\paths.toml` is used. LocalAppData must be an
absolute available location; otherwise supply `--config`. There is no cwd search,
environment-variable override per field, or fallback to another settings file.

CLI paths resolve from the invocation directory. Relative TOML paths resolve
from the configuration file's parent. Setup writes absolute owned path values.
Use literal single-quoted TOML strings for Windows backslashes, or forward slashes;
do not write JSON-style paths into TOML accidentally. `%VARIABLE%` inside a TOML
string is not an environment-expansion mechanism.

Stop the affected watcher and handler before changing saved settings. Application
processes cache their loaded configuration; edits take effect for fresh processes.
The handler receives the exact config authority and rejects incompatible application/
configuration identities. Reports and ingest may launch it again. Editing a query
file affects the next report invocation without restarting the watcher.

Command overrides (`--logs`, ingest `--package-id`, report `--database`/`--ripgrep`,
invocation `--log-dir`) affect only that invocation. Setup `--apply` persists its
inputs. Report package selection always follows explicit reporting scope or named
Run lineage, never the current model default.

## TOML fields

All eight `[paths]` fields are required nonempty strings in a complete runtime
configuration. Defaults below describe what first setup writes, not implicit
runtime fallback for missing fields.

| Field | Accepted value, meaning and default |
|---|---|
| `paths.root_game` | Readable CK3 `game` directory. Shared diagnosis checks game content and adjacent `binaries/ck3.exe`; an unfamiliar layout remains a warning. User-specific, no silent fallback. |
| `paths.root_steam` | CK3 workshop content directory, usually `steamapps/workshop/content/1158310`. Missing optional content is reported. |
| `paths.root_local_mods` | Local CK3 mod directory; optional missing content is reported. |
| `paths.root_logs` | Existing readable live logs directory. Current `error.log` may be absent at setup. |
| `paths.root_crashes` | Configured crash directory. Its absence does not establish a crash and need not block setup. |
| `paths.root_wip` | Writable application data parent, first setup default LocalAppData/ck3chronicle/data. |
| `paths.root_ck3chronicle` | Strict descendant of data parent for runtime state, default `<data>/runtime`. |
| `paths.root_learner_state` | Separate strict descendant, default `<data>/learner`; cannot overlap runtime. |
| `watcher.database` | Required nonempty string naming exact initialized schema-3 SQLite file beneath runtime. Setup saves the returned filename; never guess it or supply a directory. |
| `watcher.ingest_enabled` | Boolean, default `true`; enable automatic pending-capture processing in continuous watcher. |
| `watcher.retention_enabled` | Boolean, default `true`; enable automatic raw-evidence retention maintenance. |
| `watcher.maintenance_hours` | Positive integer, default `24`; first maintenance this many hours after watcher construction, then at that interval. Failed ingestion retries share this schedule; not immediate startup retention. |
| `watcher.retention_days` | Positive integer, default `30`; age from capture metadata `captured_at`, not file mtime. Does not erase stored diagnostic history. |
| `model.package_id` | Nonempty exact available model package ID; required for default processing. Setup persists an authenticated choice. |
| `model.manifest_sha256` | Matching SHA-256 manifest pin required with the package ID. Set through setup rather than independently editing it. |
| `tools.ripgrep` | Optional executable-path string for source-content search. Report `--ripgrep` wins. Without either, content search is unavailable; no ambient PATH lookup. |
| `logging.level` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`; default `INFO`. |
| `logging.max_bytes` | Positive integer, default `10485760`; per-log rotation size in bytes. |
| `logging.backup_count` | Positive integer, default `5`; rotated backups. |

Booleans are TOML `true`/`false`, not strings. Positive integer fields reject
booleans and zero. External directories may be missing only where diagnosis
permits optional evidence. Writable roots and settings destinations must not
overlap protected application/resources or external game/mod/log/crash trees.
External contents stay read-only; setup does not manufacture missing CK3 folders.

Example of optional controls to edit in an already generated file:

```toml
[watcher]
database = 'D:\Chronicle\data\runtime\<exact returned filename>.sqlite3'
ingest_enabled = true
retention_enabled = true
maintenance_hours = 24
retention_days = 30

[logging]
level = 'INFO'
max_bytes = 10485760
backup_count = 5
```

This is a section example, not a complete configuration; preserve generated
`[paths]` and `[model]`. Run doctor afterward. Doctor distinguishes invalid,
warning and unverified findings and cannot prove write access. Setup Apply
performs bounded write checks. Repeat setup preserves unrelated values and
existing controls but rewrites comments/formatting. Neither operation migrates
existing data to another root.

## Automatic processing and raw-log retention

Continuous watch requires the configured database even with both processing
switches false. Ingestion runs through the public handler off the polling thread;
startup scans direct nonhidden, nonsymlink pending directories containing error.log
in name order. Newly published lifecycle captures are submitted individually.
Request-result availability is separate from the stored ingestion record; see
[request-result recovery](CLI_REFERENCE.md#request-results-and-stored-ingestion).

Raw logs are intentionally retained for a configured period, **30 days by
default**, independently of ingestion success. At scheduled maintenance,
retention deletes eligible `error.log` and `debug.log` files from completed
pending capture directories under capture locks. A log becomes eligible when
its age reaches `watcher.retention_days`, measured from capture metadata
`captured_at` to the maintenance time. File modification time and the original
source-log timestamp do not determine this age.

`watcher.retention_enabled` enables maintenance, `watcher.retention_days` sets
the age threshold, and `watcher.maintenance_hours` sets the check interval.
Expiration before successful ingestion follows the configured policy. Keeping
retention enabled while setting `watcher.ingest_enabled = false` is a valid
configuration choice. If ingestion repeatedly fails, diagnose ingestion using
its results and journals. Older CK3 error logs also become less useful as mod
content changes.

Retention preserves capture/playset JSON, crash attachments, stored Runs and
diagnostic history in SQLite, and native review shards. Hidden staging, busy
captures, linked inputs and unusable capture timestamps are skipped; filesystem
dates are not substituted. Changing retention settings does not restore deleted
raw logs. One-shot commands do not instantiate this maintenance schedule.

## User files, generated state and immutable resources

| Surface | How to use/change it |
|---|---|
| Selected TOML | Editable settings. Prefer setup for paths/database/model; stop affected processes first. |
| Report `--query` JSON | Editable validated investigation definition. [All fields](REPORT_QUERY_REFERENCE.md). |
| Report `--source-context` JSON | Editable optional source-selection object; required `scope.source` filters override matching fields. |
| Model catalog `catalog.json` | Release inventory and publication metadata, not runtime settings. Use authenticated admin registration for new packages. |
| Installed model `selection.json` | Shipped schema-2 selection resource. Admin `selection` prints such a document; it does not activate it. Setup persists the user's active pin in TOML. |
| Learner catalog `catalog.json` | Retained release availability/identities/operation capabilities. Use Learner registration; `run --release` makes an explicit invocation choice. |
| Model/Learner/parser manifests, owner rules, recovery rules, matcher/model JSON | Authenticated immutable release resources. Editing bytes invalidates pins; changes require a release procedure and a new identity. |
| Learner registry/state, candidate bundle/manifest, review JSON | Generated working artifacts with retained-release identity. Use registry/learning/review operations; not general settings or interchangeable across releases. |
| Capture metadata, `playset.json`, joined/log hashes | Generated capture evidence. Preserve the original members, order and identities. Do not hand-edit to change a historical Run. |
| SQLite, native review log/manifest, journals, heartbeat, lock/endpoint files | Generated runtime evidence/control state. Use product operations. Do not edit rows, reconstruct unavailable outcomes or use lock removal as normal operation. |
| Release manifest, `runtime`, `tools` and launcher internals | Installed implementation resources verified as one distribution; not editable configuration. |

Native review evidence is separate from SQLite. Resolve its stored references
relative to the database's parent and verify hashes before claiming integrity.
Moving only SQLite omits that evidence. Read `.log` with a text viewer and the
manifest with a JSON reader. Database schema **3** and model schema **6** describe
different formats.

External tools may open SQLite using `mode=ro` and short read transactions.
Do not use `immutable=1` against the live database, change schema/content or copy
only the database while writes are occurring. `COUNT(*)` of diagnostic rows is
distinct-record count; `SUM(occurrence_count)` is occurrences. Useful tables are
`runs`, `diagnostics`, `definitions`, `playsets`, `playset_members`, `review` and
`database_info`. JSON columns retain structured lineage/facts/values. Query and
reshape those fields in your chosen tool. Keep native review payloads and their
counts separate from diagnostic rows.

For the actual SQLite and separate native-shard walkthroughs, follow
[external data access](EXTERNAL_DATA.md).

## Captured facts

Capture metadata schema 1 records `capture_id`, UTC `captured_at`, and the original
validated `error_log_source_modified_at` (UTC with nine fractional digits).
These differ from Run processing time and from each other; missing historical
source times are never backfilled. Lifecycle captures add `process` (`pid`,
`image_name`, nullable `started_ns`), `observed_started_at`, `observed_ended_at`,
`trigger: process_exit` and inferred `termination_kind`. One-shot capture uses
`manual_capture` and unknown termination, with no observed lifecycle pair.

Crash association is inferred from new folders between observations. Ambiguous
candidates remain labelled; no new folder implies inferred normal, not proof of
clean exit. Unavailable inventory leaves termination unknown. `crash_exception`
records not_applicable/absent/unavailable/captured and applicable paths/errors;
only associated exception.txt is attached. `debug_capture_failure` records a
failed secondary copy without invalidating protected primary evidence.

Playset schema 1 contains both full-file hashes, `captured_at`, ordered `members`
and `log_pair_id` (`sha256:<error hash>:<debug hash>`), with no Run ID. The pair
identity does not replace error-log deduplication. Each member has integer
`load_order` (base at 0), `name`, `path`, nullable `root_ID`, `stable_id` and
`descriptor_path`. Root IDs are ROOT_GAME/ROOT_STEAM/ROOT_LOCAL_MODS; unknown
outside-root mounts keep null identity. Base is CK3 Game Files; unavailable names
are UNKNOWN. Mount emissions determine order; descriptors supply metadata.
No mounts yields base plus warning, not invented mod membership. Paths describe
captured references, not archived mod contents or guaranteed present-day files.

[Manual contents](README.md)
