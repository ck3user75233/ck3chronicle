# Phase 1 output contracts

Status: implementation-side schema freeze for independent evaluation. No
expected values, oracle answers, scorer rules, mutations, or runner code are
defined here.

## Authority and serialization

JSON is the authoritative machine-readable public projection. Public CLI JSON
is UTF-8, one JSON object on stdout, with deterministic key sorting. Diagnostic
text belongs on stderr. Human text is a concise projection of the same stored
result but is not a substitute for the JSON schema.

Schema changes require a schema-version increment. Adding, removing, renaming,
or changing the type or meaning of a field is a schema change. Array ordering
is meaningful wherever the fields below describe load order, rank, occurrence
order, or provenance.

## Command-result v1

`process-pending --json`, `report --json`, `latest --json`, and
`errors --json` emit exactly one envelope:

```text
schema             "ck3chronicle.command-result"
schema_version     1
command            string
status             "succeeded" | "warning" | "failed"
exit_code          non-negative integer equal to the process exit code
result             object | null
error              object | null
```

On success, `exit_code` is `0`, `result` is present, and `error` is `null`.
On warning/failure, `exit_code` is nonzero and `error` is:

```text
code               stable machine-readable string
message            operator-readable string
stage              stable pipeline stage string
retryable          boolean
```

The stable Phase 1 exit taxonomy is:

| Exit | Meaning | Representative code/stage |
|---:|---|---|
| 0 | Complete success | no error |
| 1 | Reconciliation warning or untyped pipeline/report failure | `reconciliation_incomplete/reconcile`, `processing_failed/pipeline`, `report_failed/report`, `errors_failed/report` |
| 2 | Target, readiness, or input is unavailable | `report_unavailable/report`, `errors_unavailable/report` |
| 3 | Archived evidence is corrupt or inconsistent | `archive_integrity/archive` |
| 4 | Approved classification model fails integrity validation | `model_invalid/classifier` |
| 5 | SQLite open, migration, query, or transaction failure | `database_failed/database` |

A warning may carry a non-null partial `result`; a failed envelope does not.

## Processing-result v3

The `result` of `process-pending --json` is:

```text
schema                  "ck3chronicle.processing-result"
schema_version          3
finalized_pending       integer
registered_archives     integer
registered_runs         integer
context_sessions        integer
parsed_sessions         integer
classified_sessions     integer
reconciliation_errors   array[string]
latest_report           session-report v6 | null
```

The counters describe mutations performed by that invocation, not lifetime
totals. A repeated call may therefore return zero mutation counters while
returning the same latest report. Reconciliation errors are retained in the
result and cause a warning envelope with exit `1`.

This operation mutates pending/archive state and the SQLite index. It may
finalize pending evidence, recover finalized orphan archives, register durable
run receipts, and transactionally derive runtime, parse, and classification
records. The watcher never invokes it.

## Session-report v6

`build_session_report`, successful `report --json`, successful `latest
--json`, and `processing-result.latest_report` use:

```text
schema             "ck3chronicle.session-report"
schema_version     6
run                run | null
session            session
parse              parse
classification     classification
runtime_context    runtime-context projection | null
category_summary   array[summary row]
source_summary     array[summary row]
file_summary       array[summary row]
top_patterns       array[pattern]
review_queue       array[review item]
```

`run` contains:

```text
run_id, capture_id, observed_started_at, observed_ended_at,
trigger, process_name, process_pid, termination_kind,
crash, file_origins
```

`crash` is `null` unless `termination_kind == "crash"`; otherwise it contains
`folder_name`, `detected_at`, `association_method`, `confidence`, and
`exception`.

`crash.exception` contains:

```text
status             "captured" | "absent" | "unavailable"
source_rel_path    "exception.txt"
retained_path      string | null
sha256             64-character lowercase SHA-256 | null
bytes              non-negative integer | null
source_mtime_ns    integer | null
```

Only `captured` carries retained path/hash/size/source-timestamp fields. The
protected path is `crash_evidence/<capture_id>/exception.txt`. Historical v1
run receipts may project `unavailable`; they must not be relabeled captured.
Each file-origin item contains `rel_path`, `origin_kind`,
`crash_equivalence`, and `preserved_crash_rel_path`. These fields identify
whether a run's authoritative log came from the live log set or a preserved
crash copy. They do not assert error causation.

`session` contains:

```text
session_id, captured_at, evidence_bundle_hash, log_count,
legacy_crash_artifact_present, total_bytes, evidence_completeness
```

`legacy_crash_artifact_present` describes old content bundles that embedded a
crash-folder copy. It is not run termination evidence. Normal/crash/unknown is
defined only by `run.termination_kind` and its crash projection.

`parse` contains:

```text
contract_version, source_blocks, preamble_blocks,
canonical_occurrences, issue_clusters, unclassified_occurrences,
multi_issue_blocks
```

`classification` contains:

```text
run_id, contract_version, model_revision_id, model_sha256,
semantic_occurrences, counts, full_rate, l1_or_better_rate,
review_required
```

`counts` contains the integer fields `full`, `l1_l2`, `l1`, and `unknown`.
The rates are numbers in `[0, 1]`; an empty semantic population has rate `1.0`.

`runtime_context`, when present, contains:

```text
contract_version, status, debug_log_sha256, provenance,
mounted_entry_count, dlc_count, mod_count, unknown_mount_count,
warnings, dlcs, active_mods, inventory_enrichment
```

Its `provenance` contains `source_session_file_id`, `start_line`, `end_line`,
`start_byte`, `end_byte`, `block_sha256`, `candidate_count`,
`valid_mount_count`, `malformed_mount_count`, `termination_evidence`, and
`absence_reason`. `dlcs` are ordered objects with `dlc_order`, `dlc_key`, and
`mount_path`. `active_mods` are ordered objects with `load_order`, `mod_key`,
`mount_path`, and `source_kind`. Inventory enrichment supplies optional display
names and descriptor paths but cannot alter authoritative membership or order.

Summary rows are ordered by descending occurrence count with deterministic
tie-breaking. Category rows contain `category` and `occurrences`; source rows
contain `source_family` and `occurrences`; file rows contain `file` and
`occurrences`.

Each top-pattern item contains:

```text
assignment_level, contract_id, source_family, occurrences,
first_line, template, sample
```

Each review item contains:

```text
assignment_level, source_family, occurrences, first_line,
l1_template, l2_template, sample
```

Report construction is read-only and queries stored records only. It does not
reopen archived logs, reparse, or reclassify.

## Report wrappers

`report --since ... --json` nests these objects in the command result:

```text
schema          "ck3chronicle.report-with-comparison"
schema_version  2
report          session-report v6
comparison      session-comparison v2
```

The comparison identifies the exact previous/current sessions and observed
runs, model hash, evidence-quality caveats, runtime-context delta, aggregate
movement, changed/unchanged patterns, and returned/total counts. Comparisons
describe observed association and chronology; they do not claim a patch caused
an error change.

`errors --json` returns:

```text
schema               "ck3chronicle.errors"
schema_version       1
session_id           integer
captured_at          string
model_revision_id    string
total_occurrences    integer
patterns             session-report top-pattern array
```

## Runtime-context v2

`context --session ID --json` emits a direct JSON object, not a command-result
envelope:

```text
schema                 "ck3chronicle.runtime-context"
schema_version         2
session_id             integer
contract_version       string
status                 complete | partial | absent | malformed | truncated | ambiguous
debug_log_sha256       string | null
provenance             object
mutated                boolean
unknown_mount_count    integer
warnings               array[string]
dlcs                   ordered array
active_mods            ordered array
inventory_enrichment   object
```

The provenance and mount fields have the same meanings as the session report;
the direct DLC/mod items additionally include `mount_ordinal`, and direct DLC
items include `dlc_order` while mod items include `load_order` and
`source_kind`. `mutated` reports whether that call replaced stored context.
Runtime parsing mutates only derived SQLite rows and validates archived
`debug.log` identity before replacement.

## Classification-run v1

`classify --session ID --json` emits a direct object:

```text
schema                              "ck3chronicle.classification-run"
schema_version                      1
session_id                          integer
run_id                              integer
model_revision_id                   string
model_sha256                        lowercase SHA-256
classification_contract_version     string
counts                              object
mutated                             boolean
```

`counts` contains `source_blocks`, `semantic_occurrences`, `full`, `l1_l2`,
`l1`, and `unknown`. Classification mutates derived SQLite rows in one
replacement transaction. A repeated compatible call returns the accepted run
with `mutated=false`.

## Direct parse and lexical results

`parse_session` returns `ParseResult(session_id, parser_contract_version,
counters, mutated)`. Counters are `source_blocks`, `preamble_blocks`,
`issue_occurrences`, `issue_clusters`, `unclassified_occurrences`,
`multi_issue_blocks`, and `silently_dropped_blocks`. Successful Phase 1 parses
must retain `silently_dropped_blocks == 0`. Parse persistence is transactional;
failure cannot expose a partial replacement.

Each `iter_log_blocks` item exposes `timestamp`, `level`, `source_tag`,
`source_family`, `header_line`, `continuation_lines`, `raw_block`,
`log_relpath`, `line_number`, `end_line`, `raw_block_sha256`,
`raw_byte_length`, and `source_block_id`. Its hashes and byte lengths cover the
exact original bytes, including line endings. The iterator is read-only.

## Human text projection

Text `report`/`latest` prints, in order: session identity, exact run identity
when available, evidence summary, parse summary, classification summary,
runtime summary, ranked top patterns, and ranked review-required examples.
Text `errors` prints the selected session/total followed by the same ranked
top-pattern identity and counts. Exact spacing is presentation, but every
printed value must originate from the corresponding JSON result object.

## Mutation boundary summary

| Operation | Evidence writes | SQLite writes | Reads archived logs |
|---|---:|---:|---:|
| `spool_logs` / watcher capture | yes, pending copy/receipt and optional protected exception | no | live approved logs plus only the associated crash exception; no archive reads |
| `process_pending` | yes, finalization/reconciliation | yes | yes |
| `parse_session` | no | yes, derived transaction | `error.log` only |
| `parse_runtime_context` | no | yes, derived transaction | `debug.log` only |
| `classify_session` | no | yes, derived transaction | no |
| `build_session_report`, `report`, `latest`, `errors` | no | no | no |
| `iter_log_blocks` | no | no | supplied file only |

The independent runner records these side effects; it does not infer expected
answers from them.
