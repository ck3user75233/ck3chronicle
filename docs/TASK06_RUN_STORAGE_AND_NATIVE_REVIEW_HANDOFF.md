# Task 06 — Run storage and native review handoff

Current development selection advanced on 2026-09-28 to v45 / model schema 5 /
matcher API v2. See [the integration handoff](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md).
The SQL schema, public storage APIs and completion protocol below remain current;
the earlier package identities, selection status and verification totals describe
the original delivery.

Originally delivered 2026-09-27. This is the storage boundary consumed by Tasks 07 and 08.
The existing application providers remain connected. No processor, replay command,
capture service, report handler or application cutover is introduced here.

## Processing authority and implementation

Selection was inspected through `load_selected_classifier()`, not hardcoded into
storage: package `44a0401b8adf0a2953d26705`, model `76630685c4a341ca14bf9c7c`,
parser `ck3-lossless-v1.7`, matcher `ck3-native-matcher-v1`, selector
`complete-assignment-v2`, classifier v8 and `error-contract-v1` remain unchanged.
The [Task 05 handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md) continues
to own classification, binding, preparation, identity and rendering semantics.

New modules are all under `src/ck3chronicle/pipeline/`: `aggregation.py`,
`review.py`, `schema.py`, `repository.py`. `domain.py` adds storage result types.
There are **no additional predecessor corrections**, source deletions, old-provider
ports, model/selection edits or learner edits in this task.

## Aggregation and domain interfaces

`RecordAccumulator()` has `add(definition: dict, prepared: dict) -> None` and
`records() -> tuple[DiagnosticRecord, ...]`. Supply the definition used for
`prepare_record(definition, result)` and that preparation result. Each add represents
one eligible occurrence. Snapshots are independent copies in first-occurrence order.

Equality is exclusively `contracts.identity_data(values)`. SHA-256 indexes buckets;
full equality data is compared within a bucket. Layouts, components, ordered typed
values and presence participate. Final status, offsets, timestamps and another
emitter comparison do not. Contradictory definition or final status raises
`ResultIntegrityError`; it cannot split or reclassify an equal identity. Only the
first occurrence's provenance survives aggregation. Both statuses are eligible;
`error_type` remains `unknown`.

`DiagnosticRecord` fields:

| Field | Meaning |
|---|---|
| `definition: dict` | Materialized Task 05 definition; shared once in SQL |
| `values: dict` | Contract/template plus ordered regions, layout choices, component indices, slot IDs/types/values/presence |
| `match_status` | `template` or `provisional` |
| `occurrence_count: int` | Positive Run-local exact-identity count |
| `error_type` | `unknown` |
| `provenance: dict` | First complete prepared occurrence, including emission ordinals and region/binding spans |

`RunAccounting(counts: dict[str, int])` holds the reconciled counters below.
`ReviewMetadata` has `log_reference`, `manifest_reference`, `log_sha256`,
`log_bytes`, `emission_count`, `unit_count`, `availability`, `routing_counts`,
`source_counts`. `RunResult(run_id, generation_id, log_sha256, accounting, review)`
is returned **only after publication and SQLite commit**. Exceptions and the ID
carried by `DuplicateRunError` are not successful RunResults.

## Generation and physical SQLite layout

Choose an explicit, previously nonexistent generation directory. Its parent must
exist. `create_generation` exclusively creates that directory; it never clears,
adopts or overwrites an existing destination. Failed initialization can leave an
incomplete new directory: preserve/inspect it and choose a fresh name rather than
opening it as a current generation.

```text
<explicit-generation-root>/
  generation.sqlite3
  review/<generation_id>/
    .staging/<random-uuid-hex>/          # transient attempt, before a Run ID
    YYYYMMDD-XXXXXX/
      review.error.log
      review-manifest.json
```

Generation names accept `[A-Za-z0-9][A-Za-z0-9_-]{0,79}`. Schema version is **1**;
SQLite `application_id` is `0x434B3652`, `user_version` is 1. Opening checks both,
the physical table columns and singleton generation metadata. No migration,
adoption, backfill or model lookup occurs. The explicit generation pins the whole
Task 05 lineage, including the supplied application revision. A different lineage
requires a fresh generation; storage never mixes revisions in an existing one.
This deliberately includes application changes rather than guessing which are
meaning-changing. A future relaxation would require an explicit policy change.

All JSON is canonical ASCII-escaped JSON (`ensure_ascii=True`, sorted keys, compact
separators, no NaN). Opaque and surrogateescaped strings survive serialization.
Source family is also JSON-encoded in its indexed SQL column, avoiding SQLite's
UTF-8 encoding limitation for surrogate code points. Public queries return decoded
source-family strings and accept those same strings as filters.

| Table | Physical columns and relationships |
|---|---|
| `generation` | Singleton PK, unique `generation_id`, `schema_version`, `created_at`, `lineage_json` |
| `runs` | Integer `sequence` PK; unique `run_id`, unique `log_sha256`; `processed_at`, `processed_utc`, `identity_timestamp`, `identity_timezone`, `identity_basis`; `facts_json`, `counters_json`, `lineage_json` |
| `definitions` | Integer `definition_id` PK; `model_revision`, `contract_version`, `template_id` unique together; `source_family_json`, `definition_json` |
| `diagnostics` | PK `(run_id, ordinal)`; Run FK, definition FK; nonunique `identity_digest`; `values_json`, `match_status`, positive `occurrence_count`, `error_type`, `provenance_json` |
| `review` | `run_id` PK/FK; unique log/manifest references; `log_sha256`, `log_bytes`, `emission_count`, `unit_count`, `availability`, `routing_counts_json`, `source_counts_json` |

Text columns are NOT NULL; integer counts have appropriate nonnegative/positive
checks. Match status and error type are constrained. Indexes cover Run/digest,
Run/status, definition references and definition source. Digest is deliberately
not unique. There is no parent-emission table, occurrence table, cluster ID,
complete-message column, competing-candidate storage or second unresolved payload.

Definitions preserve Task 05's source family, body parts, wrapper alternatives,
slot declarations, continuation literals/types/layouts and lookup IDs without
reinterpretation. Used definitions are inserted once; conflicting data under an
existing model/contract/template identity fails. A rolled-back Run leaves no new
definitions or diagnostic records.

## Repository API

Module-level functions in `pipeline.repository`:

```python
create_generation(root: Path, *, generation_id: str, lineage: dict) -> Generation
open_generation(root: Path) -> Generation
open_generation_readonly(root: Path) -> Generation
```

`Generation` is a context manager and has `close()`. Its public read interface:

| Symbol | Result / ordering |
|---|---|
| `metadata` | Independent dict: generation ID, schema version, creation time, processing lineage |
| `root`, `review_root` | Explicit generation root and generation's review namespace |
| `connection` | SQLite connection, exposed for Task 08's database-only SQL audit |
| `find_run_by_log_hash(log_sha256: str)` | Run facts dict or `None`; use before parsing |
| `get_run(run_id: str)` | Run facts dict or `None` |
| `list_runs(*, limit: int \| None = None, offset: int = 0)` | List, newest `processed_utc` first, descending insertion `sequence` as tie-break; nonnegative pagination |
| `latest_run()` | First `list_runs` result or `None` for empty generation |
| `read_diagnostics(run_id: str, *, match_status: str \| None = None, source_family: str \| None = None)` | List of stored record dicts including definition and source, ascending Run-local record ordinal; both statuses by default |
| `read_review_metadata(run_id: str)` | Stored review dict or `None`; includes Run ID and decoded routing/source counts |
| `resolve_review_reference(reference: str) -> Path` | Lexical resolution from generation root with namespace/path-traversal validation; no external inspection |

Unknown Run diagnostic queries return `[]`; unknown Run/review lookup returns
`None`. The returned Run dict includes every `runs` column, with JSON columns
decoded as `facts`, `counters`, `lineage`. Diagnostic dicts include Run ID, ordinal,
definition ID, identity digest, values, definition, source family, match status,
count, error type and provenance. Filters combine with AND. Source filtering
joins the stored definition; it never revisits emitter matching.

Ordinary reads report **stored availability** (`available` for successful Task 06
writes). They do not stat or open either shard, source log or selected model.
External deletion does not silently change this stored fact; future explicitly
commissioned retention/audit operations must own availability transitions. Those
operations and pruning are not implemented in Task 06. The connection enables
SQL relationship/count audits without reading external files; use readonly opening
for those audits. No generation-selection or operator command policy is introduced.

### Write arguments, Run dates and facts

```python
Generation.write_run(
    *, log_sha256: str, facts: dict, lineage: dict,
    records: tuple[DiagnosticRecord, ...], review_writer: ReviewWriter,
    processed_at: datetime | None = None,
    reliable_original_log_created_at: datetime | None = None,
) -> RunResult
```

`log_sha256` is the truthful complete validated input hash, lowercase 64 hex.
Storage validates its form and enforces uniqueness; Task 07 owns stable-input
validation and hashing. It need not invent a PreparedInput adapter to use this API.
`facts` is lossless explicit JSON for capture mode/time, lifecycle observations,
crash/exception associations, retained input provenance and other supplied facts.
Unavailable facts should be null. Storage adds no inferred process events, crash
stage, capture time or copied-file creation claim. Precise capture/lifecycle times
belong in this supplied object, not diagnostic identity.

`processed_at` defaults to current UTC, or accepts a timezone-aware datetime.
`reliable_original_log_created_at` is an explicit caller assertion of reliable
**original** creation time. When supplied, it determines the date prefix and
`identity_basis='original_log_creation'`; otherwise the processing timestamp is
used and basis is `processing`. Copied file ctime is insufficient. Naive timestamps
are refused. The precise timestamp (microseconds), timezone name/key and offset
in the ISO timestamp are retained. Run query ordering uses processing chronology;
original/capture/lifecycle chronology remains unavailable unless supplied.

IDs are `YYYYMMDD-` plus six cryptographically random characters from `A-Z0-9`.
They are independent of the internal SQL insertion sequence. While holding the
SQLite write transaction, storage checks the Run ID and its shard destination,
then inserts under SQLite UNIQUE enforcement. Collisions retry before publication
(bounded at 100 candidates). Existing shard destinations are preserved, including
unaccepted leftovers. A retry after failure generates a fresh ID. Full-log hashes
remain the duplicate and cross-generation correlation authority.

Write validates compact identity uniqueness, definition/lineage correspondence,
serialized layout completeness and count reconciliation. This is structural
storage validation, with no matching, recovery, binding or semantic interpretation.
Lineage consumes all Task 05 fields and adds `database_schema_version` and
`generation_id` on each Run/manifest. No splitter or normalizer revision is invented.

## Review API, native format and manifest

`ReviewWriter(raw)` receives the pinned parser's original `RawParse`.
`observe(result: NativeClassification | NativeReview) -> None` must receive every
result from one complete `classify_raw(raw)` stream exactly once, including records.
It verifies original association and rejects repeated child references. This
collects accounting/routing only; it does not prepare or aggregate records.
`accounting(records) -> RunAccounting` reconciles counts and complete emission
coverage. Consume the complete stream: a coverage check is not a substitute for
exhausting the classifier iterator.

The repository calls `ReviewWriter.stage(directory) -> dict` in its exclusive
staging directory, then `review.finalize(directory, staged, *, run_id, lineage,
log_sha256, accounting) -> dict`. These are protocol implementation APIs; callers
normally call only `observe`, then `write_run`. `review.verify_published(directory,
expected)` reopens both parts before commit, outside ordinary reporting.

`review.error.log` is uncompressed bytes: concatenate original emission spans in
ascending original ordinal. The unit of deduplication is the original ordinal,
never text equality. Any review child retains the entire original parent once.
Groups retain all contributing emission ordinals, including supporting emissions.
Native headers, continuation lines, punctuation, line endings and undecodable
bytes are copied without decoding or rendering. Identical bytes at distinct
ordinals remain distinct occurrences. No metadata is inserted into this payload.
Zero review produces an existing zero-byte log with SHA-256 of empty bytes.

`review-manifest.json` is ASCII-escaped JSON plus a trailing newline:

| Field | Meaning |
|---|---|
| `schema`, `schema_version` | `ck3chronicle.native-review`, 1 |
| `run_id`, `lineage`, `input_log_sha256` | Successful identity candidate, full processing/storage lineage and source correlation |
| `finalization` | `complete`: both staged parts finished; SQL commit determines acceptance |
| `log_file`, `log_sha256`, `log_bytes` | Native payload name and integrity |
| `counts` | Complete Run accounting, identical to SQL |
| `source_counts` | Distinct review emissions by their original emission source family |
| `routing_counts`, `reason_counts` | Review units by kind and exact reason, respectively |
| `emissions[]` | Original ordinal, original emission/header spans, shard span, source family |
| `routes[]` | Unit index, kind, reason, source family, original provenance, affected child/group regions |

Route kinds are `no_match`, `unresolved_recovery`, `native_input_failure`. Provenance
retains message ordinal when available, all parent ordinals, ordered spans and
recovery limitation. Recovered routes include body/context/continuation provenance;
unresolved routes include unresolved spans. Explicit native-input failures also
retain exception class name. Original parser recovery objects/text are not copied
into JSON. Route-to-emission references are ordinals; emission-to-shard references
are byte offsets `[start,end)`. Multiple child routes can point to one emitted
parent, and every group contributor is retained. SQL keeps counts/references/hash
and source/kind summaries; detailed child routes and reasons stay in the manifest.

## Accounting and reconciliation

All counters are explicit, including zero:

| Counter | Meaning |
|---|---|
| `recognized_emissions` | Number of original parser emissions |
| `single_unit_emissions`, `multi_unit_emissions` | Emissions referenced by one, or more than one, final unit respectively; group supporting emissions count as referenced emissions, not extra occurrences |
| `observed_units` | Every final stream result, including unresolved/failure units |
| `recovered_occurrences` | Complete recovered messages/groups, including complete unassigned/input-failure units |
| `recovered_groups`, `supporting_entries` | Recovered units having continuations and total continuation entries |
| `template_occurrences`, `provisional_occurrences`, `no_match_occurrences` | Final classification outcomes; unresolved and explicit input failures are separate |
| `unresolved_recovery_units`, `input_failures` | Distinct explicit native recovery/input outcomes |
| `eligible_occurrences` | Template plus provisional occurrences |
| `aggregated_records` | Number of unique SQL records |
| `review_units`, `review_emissions` | Routed child/group units versus distinct original emissions written |
| `record_emissions`, `mixed_emissions` | Emissions contributing to records; those also routed to review |

With `T`, `P`, `N`, `F`, `U` denoting template, provisional, no-match, explicit
input failure, unresolved-recovery unit counts:

```text
eligible_occurrences = T + P = sum(diagnostics.occurrence_count)
recovered_occurrences = T + P + N + F
observed_units = recovered_occurrences + U
review_units = N + F + U
recognized_emissions = single_unit_emissions + multi_unit_emissions
recognized_emissions = record_emissions + review_emissions - mixed_emissions
review.emission_count = len(manifest.emissions) = counts.review_emissions
review.unit_count = len(manifest.routes) = counts.review_units
sum(manifest.source_counts.values()) = review_emissions
sum(manifest.routing_counts.values()) = review_units
```

Aggregation verifies separate T/P occurrence totals as well as the combined count.
The set of referenced original ordinals must equal the parser's emission set.
Mixed emissions contribute to both record and review counts; these are not disjoint
categories. Supporting entries never increase the complete-error occurrence count.
There is no general equality between recovered occurrences and original emissions.

## Completion, failure and cleanup ownership

SQLite and the filesystem are **not one atomic transaction**. The implemented
ordinary order is:

1. Reject a known duplicate before staging or Run-ID generation. Validate finished
   record/accounting data. Stage and flush exact native review bytes in a uniquely
   created `.staging/<uuid>` directory.
2. `BEGIN IMMEDIATE` serializes writers. Repeat the hash lookup to handle another
   writer's success since the precheck. Generate/check an ID and insert the Run,
   definitions and records inside this uncommitted transaction.
3. Complete/flush the manifest with that ID, lineage, counts and hash. Exclusively
   create its destination directory; move the two staged parts into it. Flush
   directories where supported, remove the now-empty staging directory, and reopen
   both published files to check manifest equality and payload integrity.
4. Insert SQL review metadata as available, construct the success result, commit
   SQLite, then return it. No fallible filesystem operation follows commit.

Duplicate races roll back and remove their own stage. `DuplicateRunError` contains
`existing_run_id`; the caller reports rejection and keeps protected input. Ordinary
write/publication failures roll back and remove only their known stage files.
`RunWriteError` preserves the cause and exposes `published_run_id` (possibly null)
and `staging_reference`. Validation/integrity/argument errors before staging
propagate directly. Interrupt/SystemExit is re-raised after attempted rollback and
stage cleanup. None of these returns a successful RunResult.

Published files are deliberately retained on a write/commit exception because a
commit error can have an uncertain outcome. Reopen the generation through normal
SQLite recovery, check the full-log hash, and report its actual state. If the hash
exists, the accepted Run owns its shard and retry must reject the duplicate. If
absent, retry can use a new ID; it never overwrites the old destination.

`cleanup_unaccepted(run_id: str) -> bool` removes a specifically identified orphan
under the same SQLite write lock, refuses any accepted Run, checks manifest Run/
generation identity when present, and unlinks only the two known filenames. It
also handles partial publication. Unknown contents or paths escaping ownership
are refused. It never deletes a retained input. `cleanup_staging(stage_name: str)`
removes one explicit 32-hex interrupted stage **only after all writers are stopped**:
staging precedes the SQL lock, so that lock cannot prove a stage is abandoned.
No automatic age sweep, reservation, Run-ID reuse, journal or recovery framework
is involved. Callers must not add another publication protocol.

Interruption can leave a partial stage, a partial published directory, or complete
but unaccepted files. These are bounded to the exact generation's `.staging/<uuid>`
or Run-ID directory and identifiable against SQLite. Finalized manifest state
alone does not mean accepted. Abrupt interruption after commit can leave a caller
without a returned result even though the database accepted the Run; the hash
lookup resolves that uncertainty. Normal rollback preserves prior records.

File contents use flush/fsync and SQLite uses FULL synchronous writes. POSIX also
flushes directories. Windows's ordinary Python filesystem API does not expose a
directory fsync here; sudden power-loss durability still depends on Windows and
the storage/filesystem. Process interruption and ordinary IO errors are not a claim
of an exercised power-loss guarantee. An external actor deleting accepted files
also lies outside this completion protocol.

## Task 07 composition example

This is a callable composition example, not a new processor. The caller supplies
an explicitly validated retained log path, truthful full hash, facts and exact
application revision. It owns validation and exhaustion of the result stream;
`write_run` owns all stage/finalize/publish/abort actions.

```python
from pathlib import Path
from ck3chronicle.pipeline.catalog import load_selected_classifier
from ck3chronicle.pipeline.contracts import materialize_definitions, prepare_record, run_lineage
from ck3chronicle.pipeline.aggregation import RecordAccumulator
from ck3chronicle.pipeline.review import ReviewWriter
from ck3chronicle.pipeline.repository import (
    open_generation, DuplicateRunError, RunWriteError,
)

def store_validated_log(root: Path, log: Path, sha256: str,
                        facts: dict, application_revision: str):
    with open_generation(root) as db:
        existing = db.find_run_by_log_hash(sha256)  # BEFORE parser/model loading
        if existing is not None:
            raise DuplicateRunError(existing['run_id'])
        classifier = load_selected_classifier()
        lineage = run_lineage(classifier.package,
                              application_revision=application_revision)
        definitions = materialize_definitions(classifier.package)
        raw = classifier.read_log(log)
        review = ReviewWriter(raw)
        aggregate = RecordAccumulator()
        for result in classifier.classify_raw(raw):
            review.observe(result)
            if result.disposition == 'record':
                definition = definitions[result.selected.template_id]
                aggregate.add(definition, prepare_record(definition, result))
        try:
            return db.write_run(log_sha256=sha256, facts=facts, lineage=lineage,
                records=aggregate.records(), review_writer=review)
        except RunWriteError as failure:
            # No success result. write_run already aborted its stage/transaction.
            # Close/reopen first: a commit failure may have an uncertain outcome.
            db.close()
            with open_generation(root) as recovered:
                if recovered.find_run_by_log_hash(sha256) is None:
                    if failure.published_run_id is not None:
                        recovered.cleanup_unaccepted(failure.published_run_id)
                    # If stage cleanup was blocked, stop writers, then call
                    # cleanup_staging on the basename of staging_reference.
            raise  # report failure; retain input; a later retry rechecks its hash
```

Create the separately named generation once with `create_generation(root,
generation_id=..., lineage=run_lineage(package, application_revision=...))` before
this example; preserve prior generations. Parser/model/preparation exceptions occur
before staging and require no shard abort. Operator commands, generation selection,
batch failure presentation and production execution remain Task 07 owner decisions.

## Task 08 database-only read/render example

```python
from pathlib import Path
from ck3chronicle.pipeline.repository import open_generation_readonly
from ck3chronicle.pipeline.contracts import render

def read_latest(root: Path):
    with open_generation_readonly(root) as db:
        metadata = db.metadata
        run = db.latest_run()
        if run is None:
            return {'generation': metadata, 'run': None, 'diagnostics': []}
        rows = db.read_diagnostics(run['run_id'])  # both statuses
        return {
            'generation': metadata, 'run': run,
            'review': db.read_review_metadata(run['run_id']),
            'diagnostics': [dict(source=r['source_family'], status=r['match_status'],
                count=r['occurrence_count'], text=render(r['definition'], r['values']))
                for r in rows],
        }
```

Use `match_status='provisional'`, `source_family='pdx_persistent_reader.cpp'`, or
both for filters. The generation schema, Run counters/lineage, definition FK and
review FK are available for DB-only audit, including SQL SUMs, missing relationships,
`PRAGMA quick_check` and `foreign_key_check`. Ordinary reports do not need the
native payload, manifest or selected model. Explicit shard inspection may resolve
the stored references against `db.root`, or use the Run-ID suffix under the
explicit `db.review_root`; this is a separate source-dependent operation.

## Verification evidence and limits

Verification orchestration is ignored, outside product source, at
`.codex-tmp/task06/verify.py` and `render_only.py`. Fresh evidence is in
`.codex-tmp/task06/verified-final/`. Inputs are complete unmodified files from Task 05's
31-log inventory, selected for these native features:

| Input SHA-256 prefix | Purpose |
|---|---|
| `9d3622ab` | Nonzero review, template/provisional records, genuine repeated groups and differing values |
| `10cbdcb2` | Zero review, wrappers and one/two supporting-entry groups |
| `48f3aca3` | Zero review, absent fields and the inventory's genuine present-empty field |

Fresh final-source results (three distinct native inputs; the namespace check
also writes the first input to generation B):

| Input | Recognized emissions | Recovered occurrences | Eligible occurrences | SQL records | Review emissions |
|---|---:|---:|---:|---:|---:|
| `9d3622ab` | 23,503 | 24,112 | 14,959 | 2,379 | 9,153 |
| `10cbdcb2` | 74,858 | 76,509 | 76,509 | 3,423 | 0 |
| `48f3aca3` | 98,314 | 98,924 | 98,924 | 3,594 | 0 |
| Total | 196,675 | 199,545 | 190,392 | 9,396 | 9,153 |

The review payload is 2,030,291 bytes. Native features include 11 groups with 13
supporting entries, 5,466 wrappers, 5,764 absent fields and one present-empty field.
Standalone rendering verifies 11,775 stored records across four accepted Runs in
two generations (including the deliberate cross-generation repeat). Both
`quick_check` and foreign-key checks pass. Read-only write rejection is exercised
both before the first acceptance and with a prior accepted Run; prior state is
preserved and no second availability claim appears.

Exact input paths/hashes are in `verified-final/inputs.json`. Expected preparation and
identity are recomputed from the active APIs; historical counts are not acceptance
targets. Each record is compared against its genuine prepared occurrences and
first provenance. Shard bytes equal concatenated original parser emission spans;
all manifest identity, lineage, counters, routing references, offsets and hashes
are reopened and reconciled against SQLite. Both zero-review files are verified.

Commands from the checkout (use a new output directory for a fresh replay):

```powershell
.\.venv\Scripts\python.exe -I -B -u .codex-tmp/task06/verify.py .codex-tmp/task06/verified-final
.\.venv\Scripts\python.exe -I -S -B .codex-tmp/task06/render_only.py .codex-tmp/task06/verified-final
```

`verified-final/application-source.json` records the exact pipeline source hashes whose
canonical digest is supplied as application revision. The standalone read/render
process blocks catalog/classifier/model/raw-input/binding/learner imports and
model/native-log/review-manifest reads. It verifies identical rendered hashes,
source/status visibility and unchanged database bytes. No rematching or binding
can occur in that process. Two fresh generations accept the same original hash
under isolated shard paths and distinct Run IDs; same-generation duplicates reject.

An actual SQLite `mode=ro` connection exercises write rejection with genuine
prepared input: no success or false availability is returned and its stage is
removed. Initial native verification also exposed a SQL placeholder bug after
publication; it was corrected before the fresh replay. The resulting ordinary
rollback left zero accepted rows and one complete unaccepted shard. Its payload
hash was checked and `cleanup_unaccepted` removed it. This observed failure is
recorded in `ordinary-publication-failure.json`; it was not manufactured by artifact
corruption, mocks or failure injection.

Remaining genuine coverage gaps: mixed assigned/review children in one emission,
unassigned multi-emission groups, unresolved recovery, explicit native-input
failures and surrogateescaped/undecodable native witnesses were not observed in
the selected logs. The only Task 05 inventory log with no-match results is included;
no mixed-emission witness was found there. No native branch was fabricated.
Reliable original-log creation facts were unavailable, so date verification uses
the truthful processing basis; supplied original-date selection is code-inspected.
Random ID collision, abrupt process termination, partial file-move failure, commit
IO failure and power-loss windows are inspected, not claimed as exercised tests.

## Scope and next task

Task 07 next composes protected-input preparation, pre-parse duplicate rejection,
these preparation/aggregation/review APIs, and processing/replay command behavior.
Task 08 consumes database-only query/render/audit interfaces. Existing application
providers remain connected until their separately commissioned cutover. Trusted Run
is not accepted merely because this storage boundary is delivered.

Task 05 retirement dependencies remain named and unchanged:

- Retire `tools/template_learning/build_parser_comparison.py`'s historical baseline
  before deleting `pipeline/emissions.py`, `diagnostics.py`, `normalization.py` or
  their historical domain types.
- Update the historical consumer check in
  `tools/template_learning/inspect_cross_emission_recovery.py` for removed `Capture`
  and old iteration/binding signatures.
- Update opt-in `tests/test_raw_parser_requirements.py::test_independent_pipeline_replay`
  for the removed `read_raw_log` API. Do not resurrect compatibility aliases.

Learner/model limitations from Task 05 remain: unseen/malformed/interrupted title
list variants and unrelated unmatched formulations are not repaired by storage.
Training coverage does not establish unseen accuracy. Unsupported assignment ties,
alternative component layouts and larger groups have no new witnesses here.

Entry/exit source scope proof is recorded in `.codex-tmp/task06/entry.json`,
`exit.json` and `scope.json`. Entry captured 294 tracked/untracked non-ignored file
hashes. HEAD remains `2993144e061681c5651e3e18be1290c957d4892d`. The allowed delta is
the four new pipeline modules, `domain.py`, this handoff, README and the opening
current sections of CURRENT_HANDOFF, PROJECT_STATUS, PROJECT_PLAN and
PIPELINE_ACTIONS_AND_EXECUTION_ORDER. The pre-existing deletion of `matching.py`
and all other unrelated dirty/untracked work are preserved. No retained input
deletion, production database writes, live capture, watcher operation, Git staging,
commit or push is part of this task.
