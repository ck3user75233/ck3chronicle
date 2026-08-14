# Phase 1 evaluation interface

Status: implementation-side handoff contract. This is not an executable test
harness and contains no expected answers.

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
inventory detection reads directory metadata only on the exit path. Deferred
processing hashes crash logs and avoids copying an exactly equal crash copy.

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
`ck3chronicle.processing-result` v2 projection in exactly one
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

The report is schema v5. `observed_run_id` selects an exact run; omitting it
selects the latest observed run for that evidence session. `latest` selects the
newest run whose evidence is finalized, parsed, and classified, with a
compatibility fallback only for direct development registrations that predate
run receipts.

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
