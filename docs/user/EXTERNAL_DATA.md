# Read stored data with SQLite

[Manual index](README.md) · [User workflows](WORKFLOWS.md) ·
[Configuration](CONFIGURATION_REFERENCE.md) · [Report interpretation](REPORT_QUERY_REFERENCE.md)

Application **0.0.3**, database schema **3**. SQLite holds diagnostic history
independently of the original error.log. Use a local SQLite tool to select stored
records, extract JSON fields and reshape the results for your analysis. Native
review evidence has its own files and viewing steps below.

## Identify the correct database

Use the same configuration as the product command whose result you want to check:

```powershell
$config = 'D:\Chronicle\settings\paths.toml' # Substitute your saved file.
.\ck3chronicle.cmd --config $config setup --format json
```

The preview's `database` is the exact configured file. It is also saved as
`[watcher] database` in TOML; a relative value resolves beside that TOML file.
Do not select a database by newest filename or current directory. Product reports
can use `--database` overrides; when comparing such a report, open that exact file.

Check both `PRAGMA user_version` and `database_info.schema_version` (3 here).
Model schema 6 and playset schema 1 describe different formats. Check these
identities before applying queries to a database.

## Connection and writer conditions

Use **SQLite URI `mode=ro` with a short read transaction** for live external
reads. The transaction gives related queries one consistent view once reading
begins; after it closes, later reads can see newer committed Runs.

Each application database has one request queue and one serial database worker.
Concurrent application clients submit requests to that worker, which owns the
application's single SQLite connection and writer. External read-only tools may
read while that writer is active. SQLite coordinates readers and writes; long
reads can delay writes. Finish promptly, close your connection, and retry later
if busy or locked.

Use a local tool that honors SQLite's URI/read-only settings. Do not open with
ordinary writable defaults, change schema/content or turn off locking. Do not
use `immutable=1` against a live database. A file copy made during writes is not
assumed consistent. Keep any required journal/WAL companions under SQLite's
management; do not delete them manually.

External tools connect directly to SQLite. These reads do not call the
application handler or create product journals. Normal application commands use
the public handler and may launch it and write execution logs even when querying
diagnostic history.

## Worked example: the bundled Python SQLite tool

The bundle includes Python's standard `sqlite3`, `tomllib` and JSON facilities.
Use its `runtime\python.exe` to read stored data directly. The script prints the
SQLite engine version used by your bundle.

First obtain a genuine Run ID from `runs --package-id <stored package ID>` or a
completed ingest. From the extracted bundle folder, paste this PowerShell block.
Replace the configuration and Run ID. It opens only the configured database and
closes the read transaction before returning:

```powershell
$config = 'D:\Chronicle\settings\paths.toml'
$run = '20261008-01PBM7' # Replace with a Run in your database.
@'
from pathlib import Path
import sqlite3, sys, tomllib

config = Path(sys.argv[1]).resolve()
settings = tomllib.loads(config.read_text(encoding='utf-8'))
database = Path(settings['watcher']['database'])
if not database.is_absolute():
    database = config.parent / database
database = database.resolve()
print('SQLite', sqlite3.sqlite_version)
print('Database', database)
connection = sqlite3.connect(database.as_uri() + '?mode=ro', uri=True, timeout=5)
try:
    connection.execute('BEGIN')
    print('Schema', connection.execute('PRAGMA user_version').fetchone()[0])
    print('Identity', connection.execute(
        'SELECT database_id, schema_version FROM database_info').fetchone())
    row = connection.execute('''
        SELECT r.run_id,
               json_extract(r.lineage_json, '$.package_id'),
               COUNT(d.ordinal), COALESCE(SUM(d.occurrence_count), 0),
               json_extract(r.counters_json, '$.aggregated_records'),
               json_extract(r.counters_json, '$.eligible_occurrences')
        FROM runs AS r LEFT JOIN diagnostics AS d ON d.run_id = r.run_id
        WHERE r.run_id = ? GROUP BY r.run_id
    ''', (sys.argv[2],)).fetchone()
    if row is None:
        raise SystemExit('Run not found in this database')
    print('Run, package, rows, occurrences, stored rows, stored occurrences')
    print(row)
    print('Assignment, records, occurrences')
    for status in connection.execute('''
        SELECT match_status, COUNT(*), SUM(occurrence_count)
        FROM diagnostics WHERE run_id = ?
        GROUP BY match_status ORDER BY match_status
    ''', (sys.argv[2],)):
        print(status)
finally:
    connection.rollback()
    connection.close()
'@ | .\runtime\python.exe -I -B - $config $run
```

Example output from a stored Run. Database/tool header lines are omitted; the
Run ID, package and counts are unchanged:

```text
Run, package, rows, occurrences, stored rows, stored occurrences
('20261008-01PBM7', '2b12932103f3a3111a4e1880', 1066, 1838, 1066, 1838)
Assignment, records, occurrences
('provisional', 9, 63)
('template', 1057, 1775)
```

The query counts diagnostic rows and sums their occurrences independently, then
shows the Run's stored accounting fields alongside them. In this example,
`report 20261008-01PBM7 --preset frequent --limit 5` reports **1,066 different
diagnostics occurring 1,838 times**, with five records displayed. Compare SQL
with a report using the same filters, scope and package. Diagnostic counts and
native review counts describe separate evidence; inspect each in its own context.

For more queries, replace the SELECT inside the same read-transaction pattern.
Keep values as bound parameters (`?`) when taking user input. The SQL below
inspects stored facts; it does not recreate the product's semantic comparisons.

## Tables, keys and JSON

| Table | Important keys and stored content |
|---|---|
| `database_info` | Single row (`singleton=1`), `database_id`, `schema_version`, `created_at`. Identifies this database, not the entire installation. |
| `runs` | Unique `run_id`, local `sequence`, unique full-input `log_sha256`; processing/identity timestamps and three JSON fields below. Deduplication is by full log hash within this database. |
| `diagnostics` | Primary key `(run_id, ordinal)`; `run_id` references `runs`, `definition_id` references `definitions`. Stores `match_status`, positive `occurrence_count`, `identity_digest`, `values_json`, `provenance_json`. |
| `definitions` | Primary key `definition_id`; unique `(model_revision, contract_version, template_id)`. `definition_json` stores the contract/template structure; `source_family_json` is JSON (the observed examples are JSON strings, not unquoted SQL text). |
| `playsets` | Primary key `run_id` referencing `runs`; captured flag, playset schema, paired log hashes/ID and capture time. |
| `playset_members` | Primary key `(run_id, load_order)`; `run_id` references `playsets`. Historical `name`, `path`, `root_ID`, `stable_id`, `descriptor_path`; nullable metadata stays unknown. |
| `review` | One Run-linked row with relative native-log/manifest references, log hash/size, emission/unit counts, publication availability and routing/source JSON. External payload; see the separate workflow below. |

`COUNT(*)` on diagnostics counts compact records, while `SUM(occurrence_count)`
counts repeated occurrences. Joining diagnostics to several playset members
multiplies rows and corrupts those totals. Aggregate each subject separately.
A diagnostic ordinal is local to its Run; a definition ID is local to this
database. Neither is a cross-Run error ID. Use the product's full identity/history
outputs for semantic comparison; a digest or template alone is insufficient
to redefine equality.

`match_status` is `template` or `provisional`; both are stored diagnostics.
Provisional does not mean unresolved review data, and neither status establishes
severity or a numeric confidence. `error_type` is currently the literal `unknown`;
it is not a usable severity classification.

| JSON field | Meaning and missing-data limits |
|---|---|
| `runs.facts_json` | Received capture facts, including capture ID/time, observed start/end, process/termination/crash evidence when available, and `error_log_source_modified_at`. Missing observations stay absent/null. |
| `runs.counters_json` | Processing accounting, including `aggregated_records`, `eligible_occurrences`, template/provisional occurrences and separate review/emission/unit accounting. Do not add these differently measured fields indiscriminately. |
| `runs.lineage_json` | Processing package ID/manifest hash, model revision/schema, contract, parser identity, matcher/selector/classifier/application revisions and database identity/schema. Historical, independent of today's selected model. |
| `diagnostics.values_json` | Contract values: regions, typed bindings (`slot_id`, `type`, `value`, `present`) and layout choices. KEY/LOCATOR/etc. are binding roles, not new error categories. |
| `diagnostics.provenance_json` | Native source tag, emission/message ordinals, spans and recovery metadata. Byte offsets refer to original evidence; offsets alone cannot reconstruct missing bytes. |
| `definitions.definition_json` | Literal/slot/repeat/context structure interpreted by the matching contract version. Use product reports for rendered diagnostic text. |
| `review.routing_counts_json`, `source_counts_json` | Why/by which native emitter evidence was routed to review. Separate from compact diagnostic counts. |

Run `processed_at`/`processed_utc` record processing, not CK3 launch/exit.
`identity_timestamp`, `identity_timezone` and `identity_basis` explain the Run ID's
date basis (`original_log_creation` or fallback `processing`). For reporting
chronology, use the recorded source log modification fact; never fill missing
source dates with processing dates or sort Run IDs as a substitute for history.

Small inspection query (replace the bound Run parameter in your script):

```sql
SELECT run_id, processed_utc, identity_basis,
       json_extract(facts_json, '$.observed_started_at') AS observed_start,
       json_extract(facts_json, '$.error_log_source_modified_at') AS source_modified,
       json_extract(lineage_json, '$.package_id') AS package
FROM runs WHERE run_id = ?;
```

The worked Run was processed on 2026-10-08, but its source modification fact is
`2026-10-03T02:34:42.700452600+00:00`. These are different events, not inconsistent
timestamps. SQLite `json_extract` returns SQL NULL for an absent path and JSON
null; use `json_type` if that distinction matters. Neither is an observed zero.

For one modest JSON extraction, inspect stored body bindings without classifying
them or changing the data:

```sql
SELECT d.ordinal,
       json_extract(region.value, '$.name') AS region_name,
       json_extract(binding.value, '$.type') AS binding_type,
       json_extract(binding.value, '$.present') AS present,
       json_extract(binding.value, '$.value') AS bound_value
FROM diagnostics AS d,
     json_each(d.values_json, '$.regions') AS region,
     json_each(region.value, '$.bindings') AS binding
WHERE d.run_id = ? AND d.ordinal = 0;
```

For the example Run, this query returns LOCATOR values `mod/ugc_2218867072.mod`
and `7`. Inspect each record's stored contract shape when selecting JSON fields:
other templates can require a different traversal.

`playset_captured=0` means unavailable capture context, not a known empty mod
list. A captured member path records historical mounting; it does not preserve
source file content or prove the current file exists. One SQLite file covers its
stored Runs/definitions/playsets and references, not all application installations
or external evidence. Settings, immutable releases, raw captures, review payloads,
source trees and execution journals are separate.

## Locate and view a native review shard separately

Review shards preserve native unresolved evidence that did not become complete
selected diagnostic assignments. They are **not diagnostic rows** and are not
joined into a diagnostic total. Whole native emissions can contain several units
or both assigned and review material; emission counts, review-unit counts and
diagnostic occurrences are different measures.

1. In the same read-only connection, select the Run's review metadata:

   ```sql
   SELECT run_id, log_reference, manifest_reference, log_sha256,
          log_bytes, emission_count, unit_count, availability
   FROM review WHERE run_id = ?;
   ```

2. Resolve the returned references relative to the **database's parent directory**,
   not the config or installation directory. The expected shape is
   `review/<database_id>/<run_id>/review.error.log` and `review-manifest.json`.
   Use only references from the selected database and retain that directory
   relationship. Application clients can use public handler operation
   `resolve_review_reference` for bounded namespace resolution; that operation
   checks neither file existence nor integrity.
3. Read `review.error.log` in a text viewer without saving over it. It contains
   concatenated **original native bytes**, including their original framing and
   line endings; it is not JSON/JSONL or a normalized CSV. Choose an appropriate
   encoding for text display and keep original bytes unchanged.
4. Read `review-manifest.json` separately as JSON. Native-review schema 3 identifies
   Run, input hash, lineage, byte size/hash, original/shard emission spans and
   routing reasons, with accounting/playset metadata. The manifest describes
   this shard; it does not reconstruct the complete input log.

PowerShell example, after substituting the two relative references returned by
your query and the actual database path:

```powershell
$database = 'D:\Chronicle\data\runtime\<actual database>.sqlite3'
$logReference = 'review/<database_id>/<run_id>/review.error.log'
$manifestReference = 'review/<database_id>/<run_id>/review-manifest.json'
$shard = Join-Path (Split-Path -Parent $database) $logReference
$manifest = Join-Path (Split-Path -Parent $database) $manifestReference
Get-Item -LiteralPath $shard | Format-List Length
.\runtime\python.exe -I -B -c "import hashlib,sys; from pathlib import Path; print(hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest())" $shard
Get-Content -LiteralPath $shard -Encoding UTF8 -TotalCount 20
Get-Content -LiteralPath $manifest -Raw | ConvertFrom-Json |
  Format-List schema,schema_version,run_id,log_bytes,routing_counts
```

For example, historical Run `20261005-OSPK8G`, stored under
package `4ac4e8ee92346e6d14eacfbf`, has **418 bytes, 3 emissions and 3 review units**:
two unmatched units and one unresolved-recovery unit. These are native review
counts, separate from diagnostic totals.

`availability='available'` records publication, not a current filesystem probe.
If a file is missing, preserve its reference and report the missing evidence;
SQLite cannot recreate it. Compare actual size/SHA-256 with stored values when
checking integrity.
Copying only SQLite does not carry these native files with it.

## Troubleshooting external reads

| Symptom | Next step |
|---|---|
| Unable to open database | Check the exact selected config and resolved file, plus read permissions. Keep `mode=ro`; removing it could create an empty database at a mistaken path. |
| Busy or locked | End other long external reads, close this connection, then retry. Do not delete journal/WAL/lock files. |
| No Run found | Verify database and Run ID from the same product output; a capture ID is not a Run ID. |
| SQL counts disagree with a report | Check filters, package/Run, display limits, and whether new commits arrived between reads; avoid joins that multiply diagnostic rows. |
| Missing JSON functions in another tool | Use the bundled interpreter, or decode JSON text with that tool's own JSON facilities. |
| Missing source time, member metadata or file | Keep it unavailable. Do not substitute processing time, infer a mod name or turn unknown into zero. |
| Different schema | Check the matching release reference. Do not apply this edition's SQL as a schema migration. |

[Manual contents](README.md)
