# Task 06 — v45 storage integration handoff

Completed 2026-09-28 after the owner directed Task 06 to proceed with the delivered
learner replacement. This advances the development selection to the delivered
v45 package. It does not activate the historical application providers, watcher,
production processing or a production database.

## Delivered baseline

| Boundary | Current value |
|---|---|
| Selected immutable package | `68f1ae5db205ab46afef9c4d` |
| Package manifest SHA-256 | `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f` |
| Published model | `f5cde2616f35d563118d3d32` |
| Learner / model schema / matcher API | v45 / schema 5 / `ck3-native-matcher-v2` |
| Parser | `ck3-lossless-v1.7`, unchanged |
| Selector / classifier | `complete-assignment-v2` / `ck3-native-message-classifier-v8` |
| Error Contract / SQLite schema / review manifest | `error-contract-v1` / 1 / 1 |

`models/selection.json` now points to this package and this handoff. The wheel's
`pyproject.toml` resource list ships this selected package; it no longer ships the
earlier API-v1 package as the selected runtime resources. Immutable earlier
packages remain unchanged in the checkout as historical artifacts.

## What Task 06 integrated

The existing product storage implementation already represents selected layouts
and definitions losslessly. The learner's prior literal-choice work in
`pipeline/contracts.py` was present at entry. Task 06 inspected and exercised it
through the complete storage path. **No pipeline or learner source edit and no
physical SQL schema change was necessary.** Selection and packaged resources were
the executable integration changes in this task.

The concrete flow is:

1. `catalog.load_selected_classifier` loads the selected authenticated package.
2. `Classifier.classify_raw` invokes the shared matcher and binds the selected
   regions. `SelectedRegion.layout` keeps `literal_choices` unchanged.
3. `contracts.materialize_definitions` retains literal alternatives in definitions;
   `prepare_record` retains selected indices in ordered region layouts.
4. `RecordAccumulator` compares `identity_data` including the full layout. Choice
   indices therefore participate in equality, alongside typed values, presence
   and component order. Digests remain indexes, not equality authority.
5. `Generation.write_run` stores definitions once in `definitions.definition_json`
   and layouts/values in `diagnostics.values_json`. Status, counts and representative
   provenance retain the existing physical columns and relationships.
6. `read_diagnostics` joins stored definitions and values. `render_regions` resolves
   literal choices from those stored facts; it never substitutes the canonical
   label or loads the selected model to infer what was originally written.

The existing shared model validator remains the package owner. No parser, matcher,
message-normalization pass, semantic stage, validator or compatibility adapter was
added. The matcher/recovery path and the SQL/review completion protocol remain
single implementations.

Database schema 1 already supports these JSON fields. A model/API/schema-of-model
change does not require matching SQLite version numbers. A **fresh database
generation** is still required because the stored Run processing lineage changes;
an existing generation refuses writes with different lineage. Prior accepted Runs
retain their stored definitions and render independently of current selection.

## APIs and persistence protocol

All signatures, tables, counter equations, date basis, duplicate handling,
publication/commit ordering and bounded cleanup APIs remain as specified in
[the original Task 06 storage handoff](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md).
Task 07 should use its runnable composition example with the normal selected
catalog; Task 08 should use its database-only read/render example.

Both final `template` and `provisional` results are eligible. Error type remains
`unknown`. Review receives genuine no-match evidence and writes exact original
emissions plus a finalized manifest, including both files for empty review. The
new package's literal alternatives change no review routing or occurrence-count
rules. SQLite publication requires both shard parts; duplicate/failure outcomes
never masquerade as successful `RunResult` values.

## Native storage verification

Verification orchestration is outside product source under
`.codex-tmp/task06-v45/`. Inputs were selected from the learner's delivered 73-log
inventory; all were read as complete unmodified native logs. The selected set is
seven logs: the original three Task 06 witnesses plus all four logs containing
the new package's remaining no-match outcomes. This is a storage integration
sample, not a replacement for the learner's broader model assessment or a new
unseen-accuracy claim.

The tests used the explicit proposed selection before changing active selection,
with new roots `.codex-tmp/task06-v45/verified/generation-a` and `generation-b`.
Generation IDs are `task06-v45-a` and `task06-v45-b`; both use SQLite schema 1.
The namespaces are `review/<generation_id>/<generated_run_id>/` under each root.
The first log is also written to generation B to verify independent namespaces.

| Complete input SHA-256 prefix | Recovered occurrences | SQL records | Review emissions |
|---|---:|---:|---:|
| `9d3622ab` | 24,112 | 2,501 | 0 |
| `10cbdcb2` | 76,509 | 3,423 | 0 |
| `48f3aca3` | 98,924 | 3,594 | 0 |
| `8c7eaa63` | 103,360 | 3,786 | 1 |
| `ba6ea800` | 60,963 | 3,330 | 1 |
| `eb2f32b8` | 31,639 | 1,617 | 1 |
| `f5ca3538` | 22,661 | 1,661 | 1 |
| Total (seven distinct inputs) | 418,168 | 19,912 | 4 |

The seven Runs contain **418,164 eligible occurrences**:
399,035 template and 19,129
provisional. Both literal-choice values occurred natively: index 0 appeared
269,487 times and index 1 appeared
36,056 times in selected regions. These are choice
references, not record or occurrence totals. Native coverage includes
11 groups / 13 supporting entries,
24,634 absent fields and 1 present-empty
fields. No replacement-decoding or value normalization was used.

All original 122 cases / 9,153 review occurrences are now stored as records:
267 template and
8,886 provisional occurrences.
The original affected log yields 2,501 records and an empty finalized review shard.
The isolated SQL-only reader verifies 22,413 records
across eight Runs, including the namespace-isolation repeat in generation B.
The installed whole-log write produces another 2,501 records in its separate
generation. Source integration elapsed 488.359 seconds; this is
an observation, not a performance threshold.


Checks performed:

- Every prepared occurrence rendered each body/wrapper/component exactly as the
  native parser region, including the selected `line:` or `near line:` literal.
  No synthetic message, spelling swap or fabricated prepared record was used.
- Compact records were compared to full prepared identity data, counts, final
  status and first-occurrence provenance; readback matched definitions/values
  exactly. Source/status filters remained correct and both statuses were included.
- Every original review-case ordinal was record-eligible. Reconciliation covered
  all emissions, eligible occurrences, unique records and native review units.
- All four remaining no-match emissions were preserved byte-for-byte in order
  from their complete input logs. Manifest identity, lineage, original/shard
  spans, routing associations, counters and integrity agreed with SQLite.
  Empty-review Runs had both completed files and zero payload bytes.
- Same-generation duplicate writes rejected without new Runs or shard changes.
  Cross-generation writes used distinct IDs and namespace paths. Run timestamp
  metadata truthfully used processing time because original creation facts were
  unavailable. Capture/lifecycle/crash facts remained null where unavailable.
- Actual read-only SQLite connections rejected genuine prepared writes, both
  before any accepted Run and with an accepted Run already present. Staging was
  cleaned, prior accepted state survived, and no false availability was recorded.
- Database `quick_check` and `foreign_key_check` passed. No unused definition rows
  or missing review rows remained. Exact input hashes were unchanged.
- A separate `-I -S -B` process opened the new generations read-only and rendered
  every record with model/parser/classifier/binding/learner imports and external
  log/model/manifest reads blocked. Rendered hashes agreed and DB bytes were
  unchanged. The same isolated reader also rendered the prior Task 06 generation
  after the development selection changed, without external model lookup.

Evidence: `verified/inputs.json`, `application-source.json`, `lineage.json`,
`verification.json`, `expected-reads.json`, `render-only.json`, and the two
disposable generation directories. The application revision is a digest of the
exact pipeline source snapshot, including the pre-existing literal-choice changes.

Reproduction from the repository root, choosing a new output directory:

```powershell
.\.venv\Scripts\python.exe -I -B -u .codex-tmp/task06-v45/verify.py .codex-tmp/task06-v45/new-verification
.\.venv\Scripts\python.exe -I -S -B .codex-tmp/task06-v45/render_only.py .codex-tmp/task06-v45/new-verification
```

## Installed package verification

An offline wheel was built from fresh ignored source staging, preventing stale
build-tree files from defining the result. Its selection file, selected package
payloads and pipeline modules were compared to checkout bytes. Old API-v1 runtime
resources and the removed duplicate pipeline matcher are absent from the wheel.

The wheel was installed into the task-owned ignored `installed-env`. With checkout
`src`, `tools`, and `models` reads blocked and learner/historical-provider imports
blocked, its normal catalog loaded API v2 from its own installed resources. The
complete original affected log was classified, aggregated, written to another
fresh generation and read/rendered from SQL. Counts and rendered output matched
the source integration; both empty-review parts were reopened and checked.
Evidence is `wheel.json`, `installed.json` and `installed-generation/`.

## Limits and model findings carried forward

The [learner v45 assessment](LEARNER_RELEASE_V45_RESULTS.md) remains the authority
for its evidence and limitations. It reports four remaining unmatched occurrences,
including two lost matches relative to the selected thirty-log predecessor,
capture/generalization regressions, representation-sensitive ties and remaining
word-run policy questions. Task 06 preserves those outcomes, including provisional
status; it does not change inference, promote support or fix policy by storage.
Selecting this development package does not assert universal model correctness,
resolve those policy questions, or accept Trusted Run as a completed product.

The Script location-stack investigation raised during owner review of sampled
SQL record 17 is complete. See the
[results](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_RESULTS.md) and the historical
[assignment](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_PROMPT.md).
On the same selected v45 package/model/parser used by Task 06, all 1,174,361 Script
location diagnostics across 73 retained logs received complete template or
provisional assignments, including stacks up to 55 entries. There were zero
demonstrated stack-length misses or lost location fields. All four no-match
occurrences lack a Script location tail; the seven-log outcomes agree exactly
with Task 06. The saved SQL sample and its displayed data were also verified.

Template `0b2804538785c71278ea37e7` has one location entry; sibling definitions
cover other observed structures. An unrepresented future length remains a
potential generalization limitation, not an observed defect. Task 06's earlier
explanation of that possibility must not be read as evidence of truncation or
matching failure. No additional Script-specific parsing, matching or processing
layer was introduced. Retain the current representation for Task 07; no fix or
new prerequisite follows from this investigation. A repeated-frame design would
require a separate owner decision and compatibility assessment.

The original Task 06 unexercised failure windows and native gaps remain explicit:
mixed record/review children, unresolved recovery/input-failure witnesses,
undecodable native values, reliable original-log creation dates, random Run-ID
collisions, sudden process interruption and power-loss/commit-IO failures were
not manufactured. Existing ordinary transaction/file ordering and cleanup continue
to apply. Verification here exercises actual read-only SQLite rejection.

## Scope and continuation

Exact changed repository paths for this integration:

- `models/selection.json`: selects the verified immutable v45 package.
- `pyproject.toml`: ships that same package in installed resources.
- `docs/TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md`: this new integration handoff.
- `docs/TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md`: retains the storage
  interfaces and adds the current selection checkpoint.
- `docs/CURRENT_HANDOFF.md`, `docs/PROJECT_STATUS.md`, `docs/PROJECT_PLAN.md`,
  `docs/PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md`: current completion and next task.
- `docs/ERROR_CONTRACT_SPECIFICATION.md`, `docs/SHARED_MATCHER_API.md`,
  `README.md`: current integration status and links.

Entry/exit hashes and exact changes are in `.codex-tmp/task06-v45/entry.json`,
`exit.json`, `scope.json`. HEAD is unchanged. Pipeline source, learner source,
immutable model packages, existing generation evidence and protected logs are
preserved. No source deletion, production DB write, watcher/capture operation,
Git staging, commit or push occurred.

The unrelated `docs/LEARNER_UNMATCHED_REVIEW_ROOT_CAUSE_PROMPT.md` changed during
this integration. Task 06 did not edit it; the scope ledger records its entry/exit
hashes separately and preserves the current file. All other non-task repository
files retain their entry hashes.

The development package and installed resources now share the v45 baseline.
**Task 07 is next:** protected-input validation, processing/replay composition and
operator command behavior. **Task 08** consumes SQL-only reporting/audit APIs.
Application/provider cutover remains separately commissioned.

Task 05's historical retirement dependencies remain: the old-baseline path in
`tools/template_learning/build_parser_comparison.py`; removed-API consumers in
`inspect_cross_emission_recovery.py`; and opt-in
`test_raw_parser_requirements.py::test_independent_pipeline_replay`. Do not revive
compatibility aliases or route current processing through the historical modules.
