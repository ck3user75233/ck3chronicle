# Phase 1 evaluation interface

Status: implementation-side handoff contract. This is not an executable test
harness and contains no expected answers.

The exact machine-readable schemas and mutation boundaries referenced here are
frozen in `PHASE1_OUTPUT_CONTRACTS.md`.

## Authority boundary

The implementation/orchestration authority may publish:

- the public product functions and CLI commands to invoke;
- required inputs, preconditions, side effects, return types, and output files;
- versioned output-field and error-envelope contracts;
- operational limits and permitted setup steps.

It must not author, edit, or run the Phase 1 exit harness, oracle fixtures,
mutation campaign, scoring code, or private-holdout selection. Those artifacts
belong to independent evaluation roles defined in `PHASE1_EXIT_PROTOCOL.md`.
Implementation-authored unit and regression tests remain development evidence
only.

## Product invocation map

These are the supported seams an independent harness author can use. The
harness author decides how to invoke them and how to capture results.

### Copy-first protection

Function:

```python
ck3chronicle.harvester.spool_logs(
    logs_root: pathlib.Path,
    dest_root: pathlib.Path,
    *,
    abort_if: Callable[[], bool] | None = None,
) -> PendingCapture
```

Purpose: copy approved CK3 logs into a protected pending directory without
hashing or SQLite work. `error.log` is mandatory. The returned
`PendingCapture` supplies the pending path, capture time, file count, names,
and copied-file statistics. A successful call creates one visible pending
directory; a restart signal raises `UnstableCapture` and must not publish a
completed pending directory.

The public watcher then records the independently durable run identity with:

```python
ck3chronicle.watcher.write_capture_receipt(
    dest_root: pathlib.Path,
    pending: PendingCapture,
    *,
    trigger: str,
    process: ProcessIdentity | None = None,
    observed_started_at: str | None = None,
    observed_ended_at: str | None = None,
    termination_kind: str = "unknown",
    crash: dict | None = None,
) -> pathlib.Path
```

The immutable receipt is separate from evidence bytes. Two receipts may point
to one content-addressed bundle; they must become two database run rows. Crash
inventory detection reads directory metadata only on the exit path. For a
newly associated crash folder, `write_capture_receipt` attempts to copy the
root-level `exception.txt` immediately to
`crash_evidence/<capture_id>/exception.txt`, hashes only that protected copy,
and records `captured`, `absent`, or `unavailable` in the receipt. Normal runs
record `not_applicable`. Deferred processing verifies that artifact, projects
its provenance into SQLite, hashes crash principal logs, and avoids copying an
exactly equal principal-log copy.

Public equivalents:

```text
ck3chronicle capture [--logs PATH]
ck3chronicle watch [--logs PATH] [--process-name NAME]
```

### Deferred end-to-end processing

Function:

```python
ck3chronicle.processing.process_pending(
    root: pathlib.Path,
    classifier: ck3chronicle.classification.Classifier,
) -> ProcessingResult
```

Purpose: finalize pending copies, reconcile immutable archives and the SQLite
index, parse runtime context, parse canonical error blocks, classify semantic
occurrences, and build the latest stored report. The watcher never calls this
function.

Returned fields:

```text
finalized_pending
registered_archives
registered_runs
context_sessions
parsed_sessions
classified_sessions
reconciliation_errors
latest_report
```

Public equivalent:

```text
ck3chronicle process-pending [--json]
```

The function returns `ProcessingResult` directly. The JSON CLI wraps its
`ck3chronicle.processing-result` v3 projection in exactly one
`ck3chronicle.command-result` v1 envelope:

```text
schema, schema_version, command, status, exit_code, result, error
```

`error`, when present, contains `code`, `message`, `stage`, and `retryable`.
The supported process exit codes are 0 success, 1 warning/pipeline failure,
3 archive integrity, 4 model integrity, and 5 database failure.

### Exact lexical blocks

Function:

```python
ck3chronicle.parser.log_blocks.iter_log_blocks(
    path: pathlib.Path,
    *,
    log_relpath: str | None = None,
    retain_preamble: bool = True,
) -> Iterator[TimestampedLogBlock]
```

Purpose: partition the supplied file bytes into an optional preamble plus
timestamped blocks. It does not read an oracle, write SQLite, or classify
semantics.

Each yielded block exposes:

```text
timestamp
level
source_tag
source_family
header_line
continuation_lines
raw_block
log_relpath
line_number
end_line
raw_block_sha256
raw_byte_length
source_block_id
```

`raw_block_sha256` and `raw_byte_length` are computed from the exact source
bytes, including original line endings. `source_block_id` is the SHA-256 of
`log_relpath + NUL + start_line + NUL + raw_block_sha256` encoded as specified
by `source_block_id()` in the same module.

Independent lexical evaluation uses the default `retain_preamble=True` so the
yielded preamble is exact. The product parse service deliberately uses
`False`: it needs only the preamble cardinality and therefore avoids retaining
a potentially large malformed headerless prefix in Python memory.

### Canonical parse and persistence

Function:

```python
ck3chronicle.parser.service.parse_session(
    conn: sqlite3.Connection,
    evidence_root: pathlib.Path,
    session_id: int,
    *,
    reparse: bool = False,
) -> ParseResult
```

Precondition: the session is registered with finalized capture evidence and
contains exactly one archived `error.log` manifest row. The function validates
the archived byte length and SHA-256, then derives and persists one lexical
block at a time inside one replacement transaction. It reconciles persisted
totals, per-block issue counts, per-signature counts, and occurrence provenance
before marking success. Failure rolls back to the prior accepted projection.

Public equivalent:

```text
ck3chronicle parse --session SESSION_ID [--reparse]
```

### Runtime DLC and active-mod order

Function:

```python
ck3chronicle.runtime_context.parse_runtime_context(
    conn: sqlite3.Connection,
    evidence_root: pathlib.Path,
    session_id: int,
    *,
    reparse: bool = False,
) -> RuntimeContextResult
```

Purpose: derive and store the same-run ordered DLC and mounted-mod sequence
from the session's immutable archived `debug.log`. It does not use the
extension's currently active `session.mods` as historical evidence.

The result exposes `complete`, `partial`, `absent`, `malformed`, `truncated`,
or `ambiguous` plus the archived `session_file_id`, exact line and byte range,
raw block SHA-256, candidate/valid/malformed counts, termination evidence, and
absence reason. Authoritative DLC/mod identities and order are separate from
optional inventory names, descriptor paths, counts, and warnings.

Public equivalent:

```text
ck3chronicle context --session SESSION_ID [--reparse] [--json]
```

### Empirical classification

Function:

```python
ck3chronicle.classification.service.classify_session(
    conn: sqlite3.Connection,
    session_id: int,
    classifier: Classifier,
    *,
    reclassify: bool = False,
) -> ClassificationRunResult
```

Precondition: finalized evidence and a successful canonical parse. Contract v2
uses empirical similarity only to nominate a template, then PostValidates
ordered literals and typed slots. Locator typing precedes L1; locator tokens
cannot fill other slot roles. Invalid L2 falls back to L1 and invalid unlayered
shape to unknown. The return value identifies the model revision/hash and
supplies source-block, semantic occurrence, full, L1+L2, L1-only, and unknown
counts.

Public equivalent:

```text
ck3chronicle classify --session SESSION_ID [--reclassify] [--json]
```

### Stored report

Function:

```python
ck3chronicle.reporting.build_session_report(
    conn: sqlite3.Connection,
    session_id: int,
    *,
    model_sha256: str | None = None,
    observed_run_id: int | None = None,
    limit: int = 20,
) -> dict[str, object]
```

Purpose: build a schema-versioned report exclusively from stored records. It
must not reopen archived logs. Public report surfaces are:

```text
ck3chronicle report --session SESSION_ID [--json]
ck3chronicle report --run RUN_ID [--json]
ck3chronicle latest [--json]
ck3chronicle errors [--session SESSION_ID | --run RUN_ID] [--json]
```

The report is schema v6. `observed_run_id` selects an exact run; omitting it
selects the latest observed run for that evidence session. `latest` selects the
newest run whose evidence is finalized, parsed, and classified, with a
compatibility fallback only for direct development registrations that predate
run receipts.

Each JSON report command emits one `ck3chronicle.command-result` v1 envelope.
Its `result` is the session-report v6, report-with-comparison v2, or errors v1
projection. Readiness/input failures use exit 2 and report-stage error codes;
database failures use exit 5; unexpected report failures use exit 1. Human text
mode remains a concise executive projection of the same stored report object.

## Gate-to-interface invocation manifest

This table is the complete implementation-side handoff for the 35 Phase 1
gates. It identifies callable seams and observable product outputs, but does
not prescribe runner mechanics, mutations, expected values, scoring rules, or
private data. Those are independent-evaluator responsibilities.

| Gate | Product seam | Public inputs and observations |
|---|---|---|
| `P1-CAP-01` | `spool_logs`; `write_capture_receipt`; `finalize_pending_captures`; `capture`; `process-pending --json` | A logs directory, run-associated crash folder, and evidence root. Observe pending/archive paths, protected `exception.txt`, receipts, manifest, registry rows, processing envelope, and immutable evidence bytes. Exercise captured, absent, and stale/unassociated crash-folder cases. Copy/finalize/process mutate evidence and the index. |
| `P1-CAP-02` | Same capture/finalize/process seams | Re-submit independently selected identical evidence. Observe bundle identity, session rows, durable run receipts/rows, and returned registration counters. |
| `P1-CAP-03` | `spool_logs`; `read_snapshot`; `reconcile_archives`; `process-pending --json`; `audit_database` | The evaluator supplies its own source/evidence mutations, including a protected exception mutation. Observe manifest/file verification, run-artifact verification, bundle identity, command status, and archive/index state. |
| `P1-CAP-04` | `spool_logs(..., abort_if=...)`; `capture`; watcher receipt path | The evaluator controls restart/source-instability signals. Observe exception or command exit, pending/final archive presence, and receipts. |
| `P1-CAP-05` | `finalize_pending_captures`; `reconcile_archives`; `process-pending --json` | The evaluator supplies fault points. Observe durable archive recoverability plus the command-result status, exit code, stage, retryability, counters, and database state. |
| `P1-CAP-06` | `spool_logs`; `process-pending --json`; `build_session_report` | The evaluator supplies missing/zero-byte approved logs. Observe explicit rejection or accepted completeness, zero counters, and report fields. |
| `P1-RUN-01` | `parse_runtime_context`; `context --json`; stored report `runtime_context` | Finalized archived `debug.log`. Observe status, exact provenance, counts, ordered DLCs/mods, warnings, and persisted projection. |
| `P1-RUN-02` | Same runtime seams | Evaluator-selected Workshop and local mount forms. Observe `mod_key`, `mount_path`, `source_kind`, and load order. |
| `P1-RUN-03` | Same runtime seams | Evaluator authors an order mutation and compares only the returned/persisted authoritative sequence. |
| `P1-RUN-04` | Same runtime seams | Evaluator supplies complete/partial/absent/malformed/truncated/ambiguous shapes. Observe status, termination evidence, absence reason, counts, and warnings. |
| `P1-RUN-05` | `parse_runtime_context`; `context --json`; `resolve_file_instances` | Evaluator controls optional inventory metadata. Observe that authoritative membership, order, paths, and resolver roots remain separate from enrichment. |
| `P1-PAR-01` | `iter_log_blocks`; `parse_session`; repository source-block readers | Evaluator-selected archived `error.log`. Observe every lexical field, persisted source-block provenance, counters, and parse state. |
| `P1-PAR-02` | `extract_block`; `normalize`; `parse_session`; stored occurrences/issues | Evaluator supplies semantic inputs and oracle separately. Observe normalized issue fields, occurrence provenance, clusters, and counters. |
| `P1-PAR-03` | `parse_session`; stored `source_blocks`, `occurrences`, and `issues` | Evaluator selects duplicates. Observe separate source occurrences, shared signatures/clusters, and per-block/per-signature counts. |
| `P1-PAR-04` | `tokenize`; `Classifier.classify`; `classify_session` | Evaluator controls locator/path mutations. Observe typed normalized tokens, assignments, templates, and identities. |
| `P1-PAR-05` | Extractor/classifier seams above | Evaluator authors near-miss families. Observe conservative fallback (`l1` or `unknown`) and absence of a false full assignment. |
| `P1-PAR-06` | `Classifier.classify`; `classify_session`; `classify --json` | Evaluator supplies authentic positives and near misses. Observe assignment level, contract ID, L1/L2 templates, typed slots, model identity, and aggregate counts. |
| `P1-PAR-07` | `iter_log_blocks`; `parse_session` | Evaluator supplies encoding, newline, long-line, malformed, replacement-character, and truncation cases. Observe exact byte/line provenance, counters, and explicit failure state. |
| `P1-PAR-08` | `parse_session(..., reparse=True)` plus repository reads | Evaluator chooses a reparse failure injection. Compare prior and final canonical projections and parse state. |
| `P1-PAR-09` | `parse_session` plus repository reads | Evaluator chooses a first-parse failure. Observe exception/public exit and absence of a falsely successful or partial projection. |
| `P1-PAR-10` | `parse_session`; `classify_session`; `build_session_report` | A finalized zero-byte `error.log`. Observe returned counters, stored state, classification counts, and report projection. |
| `P1-PAR-11` | `audit_database`; `audit-db --deep --json`; repository aggregate reads | Evaluator-selected processed databases. Observe audit output and stored total/per-block/per-signature/provenance invariants. Audit is read-only. |
| `P1-REP-01` | `process_pending`; `process-pending --json` | Evidence root plus approved classifier. Observe processing-result v3 inside command-result v1 and all documented side effects. |
| `P1-REP-02` | `report`, `latest`, `errors` in text and `--json` modes | Same stored target and limit. Observe stdout bytes, JSON result, exit status, and stderr; field equivalence is independently scored. |
| `P1-REP-03` | `build_session_report`; `report`; `latest`; `errors` | Process once, then use stored records. The evaluator controls removal/unavailability of raw inputs and observes report stability. |
| `P1-REP-04` | Same report seams | Evaluator records database/evidence hashes before and after each read command. Product report functions and commands are read-only. |
| `P1-REP-05` | `process_pending`; report seams | Evaluator controls repeat calls and insertion order. Observe processing counters, stored projections, JSON bytes, and pattern ordering. |
| `P1-REP-06` | `latest_report_target`; `report --run`; `errors --run`; `latest` | Evaluator supplies run chronology including repeated evidence. Observe exact run/session selection, principal-file origin, crash provenance, and the exception status/path/hash/size/source-timestamp projection. |
| `P1-REP-07` | `process-pending --json`; `report --json`; `latest --json`; `errors --json` | Evaluator supplies success/readiness/integrity/model/database/pipeline conditions. Observe one command-result envelope, stdout/stderr, and process exit. |
| `P1-HOLD-01` | The same capture/runtime/parse/classify/report seams | Oracle custodian supplies a post-freeze unseen package. Runner records outputs only; scorer owns expected values. |
| `P1-MUT-01` | The same product seams | Independent harness author creates and hashes mutations. Runner records candidate outputs; independent scorer owns kill criteria. |
| `P1-PERF-01` | `iter_log_blocks`; `parse_session` | Independent runner owns warmup, repetitions, timing, peak RSS, cache policy, and environment capture. |
| `P1-PERF-02` | `parse_runtime_context` | Independent runner owns runtime extraction performance measurement and resource envelope. |
| `P1-PERF-03` | `build_session_report`; stored text/JSON commands | Independent runner measures stored reporting without reparsing raw evidence. |
| `P1-PERF-04` | `process_pending`; `process-pending --json` | Independent runner measures the complete deferred pipeline and captures its command envelope and resource use. |

The evaluator may call lower-level repository readers to observe persisted
state, but must not use production normalizers, classifiers, or report builders
to compute expected answers.

## Independent evaluator deliverables

Using only this interface plus the frozen product/gate contracts, the test
harness author supplies:

- executable runner code and environment setup;
- public calibration fixtures and mutations;
- exact result-envelope capture;
- resource measurement;
- cleanup and rerun behavior.

The oracle/scoring authority separately supplies expected answers and scorer
code. Neither deliverable is accepted merely because it resembles an
implementation-authored prototype.
