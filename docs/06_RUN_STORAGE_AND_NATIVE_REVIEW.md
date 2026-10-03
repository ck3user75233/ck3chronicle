# Agent Task 06 — Build aggregation, Run storage and native review

Revised proposal, 2026-09-27, for `C:/Users/nateb/Documents/ck3chronicle`.
When assigned, this replaces the earlier Task 06 prompt. Implement storage for
the completed Task 05 interfaces and approved Error Contract.

## Outcome and boundaries

Deliver exact-identity aggregation, one native review shard per successful Run,
current-generation SQLite persistence and database-only read interfaces.
The [two-part shard](ARCHITECTURE_AND_DATA_LINEAGE.md#native-review-shard)—native
review log and manifest—must be implemented, integrated with Run persistence and
verified by the end of Task 06. Later tasks consume this working capability.
Consume completed classification/binding and contract preparation. A diagnostic
record is the refined unique error stored in SQL; unresolved evidence remains
native review evidence. Both selected template and provisional matches are
record-eligible. Error typing remains `unknown`.

Protected-input preparation, capture, the production processing/replay orchestrator
and command/report handlers are later tasks. Keep existing application providers
connected until their separately commissioned cutover. Verification may compose
current APIs over explicit retained logs and a disposable generation.

Read repository instructions, [current status](PROJECT_STATUS.md),
[plan](PROJECT_PLAN.md), [current handoff](CURRENT_HANDOFF.md),
[development environment](DEVELOPMENT_ENVIRONMENT.md) and [banned designs](BANNED_IDEAS.md).
Required boundary specifications:

- [Task 05 implementation handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md).
- [Approved Error Contract](ERROR_CONTRACT_SPECIFICATION.md).
- [Owner intent](OWNER_PRODUCT_INTENT.md): diagnostic identity, Run and retention.
- [Architecture](ARCHITECTURE_AND_DATA_LINEAGE.md): native review, generations,
  source reconstruction and transaction invariants.
- [Trusted Run](TRUSTED_RUN_SPEC.md): content-hash guard, accounting, storage and
  database-only reporting requirements.

Current owner decisions and the approved contract supersede historical timestamps,
semantic gates, normalization stages and migration instructions in older material.
Use named sections and actual symbols, not stale source line ranges or test files,
to establish requirements.

## Predecessor interfaces to consume

Inspect the actual `catalog.py`, `classifier.py`, `raw_input.py`, `domain.py`,
`contracts.py` and `bindings.py` under `src/ck3chronicle/pipeline/`.
The active schema-2 package is `44a0401b8adf0a2953d26705`, model
`76630685c4a341ca14bf9c7c`, classifier v8 and `error-contract-v1`.
Verify the current selection and handoff rather than hardcoding this snapshot.

- `load_selected_classifier()` supplies the selected parser/matcher path.
- `classify_raw(raw)` yields `NativeClassification` or `NativeReview`.
  Final outcomes are `template`, `provisional`, `no_match`; disposition is
  `record` or `native_review`.
- `materialize_definitions(package)` supplies serializable model definitions.
- `prepare_record(definition, result)` supplies `values`, final `match_status`,
  `error_type`, initial `occurrence_count=1` and representative provenance.
- `identity_data(values)` is the equality authority; `identity_digest(values)`
  is an index. `render`/`render_regions` consume serialized definitions and values.
- `run_lineage(package, application_revision=...)` supplies processing lineage;
  storage adds schema/generation metadata.

The pinned raw parse retains original bytes and emission ordinals/spans. Use that
evidence for review writing. Historical `pipeline/emissions.py`, normalization
and recovery implementations are not dependencies of this task. Matching,
selection, binding and semantic interpretation are not repeated in storage.

## Mutation scope

Create `pipeline/aggregation.py`, `review.py`, `schema.py` and `repository.py`.
Edit `pipeline/domain.py` for actual `DiagnosticRecord`, successful `RunResult`
and required storage/review accounting interfaces. Necessary non-semantic
predecessor corrections may touch at most two additional pipeline files; identify
the requirement and each correction separately. Preserve existing contract rules.

No source-file deletions, old database/provider ports, model/selection changes,
learner changes or application cutover. Standard-library SQLite/filesystem tools
are sufficient. Do not import old repository writers, projections or journals.
Record entry/exit hashes and preserve unrelated work. Use a task-owned ignored
directory inside this checkout for disposable databases, shards and evidence.
No production database writes, live capture, watcher operation, retained-input
deletion, commit or push.

## 1. Aggregate prepared occurrences

Expose an accumulator that accepts `prepare_record` results and produces compact
records. Delegate equality to `contracts.identity_data`; use digests only as
lookup indexes and compare the full equality data.

Within one Run, equal template/layout choices and every ordered typed value and
presence flag aggregate by increasing occurrence count. Component count, order
and content participate. Preserve one representative occurrence's provenance.
Neither status, timestamps, absolute offsets nor another emitter comparison
create an additional identity. Contradictory status/definition data for the same
identity under the same Run lineage is an explicit inconsistency, not permission
to reclassify or silently split records.

Keep `template` and `provisional` filterable; both belong in ordinary diagnostic
queries. Preserve `error_type=unknown`. Store occurrence counts without individual
occurrence or diagnostic first/last timestamps. Retain available Run lifecycle
and capture times as separate supplied facts; unavailable facts remain unavailable.

## 2. Preserve native review evidence

Implement a writer/finalizer consuming review-routed results and their original
emission associations. Copy exact original bytes, including native headers,
continuations, punctuation, line endings and undecodable bytes. Do not reconstruct
review text by rendering or replacement decoding.

If any child of an emission requires review, write that original emission once
and retain the child routing reasons/provenance. If an unassigned group spans
several emissions, retain every contributing emission. Deduplicate only repeated
references to the same original emission ordinal within the Run, never identical
content at different ordinals. Preserve original order and occurrence frequency.
Use existing parser spans without a second recovery pass. Unresolved recovery
and explicit native-input failures retain their distinct reasons and evidence.

Implement the [native review shard definition](ARCHITECTURE_AND_DATA_LINEAGE.md#native-review-shard).
Finalize both parts for every successful Run:

- `review.error.log[.gz]`: exact native emissions routed to review.
- `review-manifest.json`: Run ID, processing lineage, review/source counts,
  routing reasons, original spans/ordinals, shard offsets, affected children/groups,
  finalization state and native-review-log integrity hash.

When no emissions require review, the native review log contains zero emissions and the
manifest still records the Run, lineage, completion and zero review count.
Namespace the shard by generation and Run identity. Keep metadata in the manifest
and the required SQLite fields, outside the native payload bytes.
No permanent parent-emission table or second unresolved-text payload is required.

Keep recognized emissions, recovered complete occurrences, supporting entries,
assignment outcomes, eligible occurrences, aggregated records, review units,
distinct review emissions and explicit input failures distinguishable. Document
the reconciliation equations. Mixed emissions contribute to both records and
review; these are not disjoint emission categories. Sum of record occurrence
counts must equal eligible occurrences. Shard counts reflect original emissions
written, not the number of review-routed children.

## 3. Persist the current generation

Store successful Run facts, complete-log SHA-256, supplied capture/lifecycle/crash
metadata, counters, processing lineage, definitions, diagnostic records and review
metadata. The generation has an explicit identity and supported schema version.
Fresh generations replace incompatible schemas or meaning-changing processing
revisions; opening a database performs no migration, adoption or backfill.

Generate Run IDs automatically as `YYYYMMDD-XXXXXX`, for example
`20260927-K7M4P2`: a full year/date and six random uppercase alphanumeric
characters. Use the original log creation date when reliably supplied; otherwise
use the processing date. Store the precise timestamp, timezone and its basis in
Run metadata. A copied file's creation time does not establish the original
log creation time. Enforce Run-ID uniqueness in SQLite and retry a collision
before shard publication. IDs are independent of generation counters; full-log
hashes remain the authority for duplicate detection and cross-generation correlation.

Store each used definition once under its model/contract/template identity.
Definitions retain source/emitter, literals, slot placements/types and selected
layout lookup data. Records reference definitions and retain ordered values,
presence, layout choices, final status, count, error type and representative
provenance. Source must be queryable through the definition relationship.
Preserve opaque and surrogateescaped strings through a lossless representation
such as ASCII-escaped JSON. Add no cluster IDs, separate contract taxonomy,
semantic slot roles, competing candidates or duplicate complete-message column.

Run lineage consumes Task 05's model/package/parser/matcher/selector/application/
contract fields and adds database schema/generation identity. Introduce no fictional
splitter/normalizer revision. SQL stores review reference, counts, integrity hash,
availability and lightweight routing metadata; native unresolved payload remains
in the shard. Ordinary record rendering reads only stored definitions and values.

Expose the following repository capabilities and document exact arguments/results:

| API | Responsibility |
|---|---|
| `create_generation` | Explicitly create a separately named current generation; preserve existing destinations. |
| `open_generation`, `open_generation_readonly` | Validate the supported generation; read-only opening performs no mutation or implicit creation. |
| `find_run_by_log_hash` | Let the later processor reject duplicates before parsing. |
| `write_run` | Persist one complete successful Run with its finalized shard metadata. |
| `get_run`, `latest_run`, `list_runs` | Return Run facts with documented ordering and available/unavailable chronology. |
| `read_diagnostics`, `read_review_metadata` | Return database facts usable by later reporting, including status/source filters and renderable definitions/values. |

Also expose read-only generation/schema/lineage metadata and the stored
relationships/counters needed by Task 08's database audit. Document diagnostic
query ordering and how shard references resolve from the explicit generation or
review root. Ordinary reads report stored availability; they do not silently
inspect external evidence or require the currently selected model.

Enforce full-log hash uniqueness within the generation at the write boundary as
well as exposing the pre-parse lookup. Duplicate rejection creates no second
successful Run and never deletes protected input. Run IDs and duplicate/failure
results must not be confused with successful `RunResult` values.

## 4. Complete SQLite and filesystem work honestly

Specify and implement the ordinary transaction/file order: stage the native review log,
obtain Run identity within the chosen storage design, complete its manifest,
safely publish both parts, and commit only a complete Run.
Define generation and Run ownership of
shard paths, using the generated Run ID and preserving existing destinations.

A successful database record requires both shard parts to be complete and
published, with manifest identity/counts/integrity consistent with SQLite.
Database or shard failure returns no success. Rollback preserves prior accepted
records. Document complete-but-unaccepted files that can survive interruption,
their bounded identification/cleanup, and retry behavior without overwriting an
accepted shard or touching unrelated files. Acknowledge that SQLite and filesystem
operations are not one atomic transaction. Use ordinary transactions and the
smallest sufficient file protocol, without the old processing journal, durable
reservation system or parallel publication framework.

Task 06 owns this completion protocol. Its public API and handoff must specify
who stages, finalizes, aborts and cleans up, when a Run ID becomes successful,
and what the caller does after duplicate rejection or failure. Task 07 composes
these operations; it must not invent another publication or reservation protocol.
Accept truthful input hash, capture facts and lineage through explicit arguments
without requiring Task 07's not-yet-created `PreparedInput` class.

## Verification with genuine inputs

Use complete unmodified native logs from the Task 05 inventory and a fresh ignored
disposable generation. Select a small documented set covering template and
provisional records, genuine repeats/differing values, wrappers/components,
optional absence/present-empty values and Runs with zero and nonzero review emissions.
Use existing native mixed-emission witnesses if available. No synthetic CK3
inputs, fabricated prepared records, corrupted artifacts or test-derived rules.

Demonstrate create/open, successful writes/readback, duplicate rejection, count
reconciliation, exact native shard bytes/order/frequency, namespace isolation
between two fresh generations, and unchanged protected originals. Check generated
Run-ID format, distinct IDs for successful writes, and timestamp/basis metadata.
Reopen both shard files and verify manifest identity, lineage, counts, routing
references and native-review-log integrity against the written evidence and SQLite.
For a Run with zero review emissions, verify both files exist and its manifest
records successful completion with a zero review count.
Reopen read-only and render database records in a separate process with model/parser/log access
unavailable. Verify source and status remain reportable and no repeated matching
or binding occurs. Keep verification orchestration outside product source.

Exercise a bounded ordinary SQLite/filesystem write rejection using genuine
prepared input, such as an actual read-only database connection, and show that
it produces no successful Run or false shard availability. Inspect publication/
commit failure ordering; distinguish exercised failures from unexercised crash
windows. Use no mocks or failure-injection framework. Record unavailable native
branches as gaps rather than fabricating evidence.

## Completion and next-task handoff

Create `docs/TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md`. Include actual
symbols/signatures, record and Run fields, physical SQL/definition layout,
generation/shard namespace, manifest schema and both file formats,
Run-ID generation and timestamp basis, collision and
duplicate behavior, count meanings, transaction/file
ordering, failure/retry behavior, commands/evidence and coverage limits.
Give Task 07 a short runnable composition example using the real APIs; do not
implement its processor, capture or replay module here.
The example must show pre-parse duplicate lookup, preparation/aggregation/review,
completion, and failure cleanup. Give Task 08 a database-only read/render example
and document empty-generation/latest behavior, generation metadata, source/status
filtering, counts and shard-reference resolution. Physical storage choices are
made here and carried forward; remaining operator command choices belong to
Task 07's owner review.

Update the opening current sections of `docs/CURRENT_HANDOFF.md`,
`docs/PROJECT_STATUS.md`, `docs/PROJECT_PLAN.md` and
`docs/PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md`, plus README links as needed.
Link the detailed handoff, state what actually completed and identify the next
task. Mark superseded instructions as historical. Carry forward Task 05's named
learner/research retirement dependencies and model limitations.

Finish with a concise outcome, exact changed paths, interface summary, decisions
or blockers, verification results and entry/exit scope proof. Stop at this storage
boundary; later tasks own input processing/replay, report handlers and cutover.
