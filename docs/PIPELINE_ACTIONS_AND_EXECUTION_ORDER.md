**Pipeline actions and proposed execution order**

## Shared decoder receiving handoff — 2026-10-05

Decoder delivery is ready for pipeline and learner/release receiving. Follow the
[pipeline section of the combined release handoff](learner-next-release/HANDOFF.md#pipeline-team-receiving-and-deployment--2026-10-05)
for exact ownership, ingestion/failure/storage boundaries and deployment checks.
The [current 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) remains the
runtime API authority. Production integration and activation remain pending.

## Task 07D implemented — activation remains separate — 2026-09-29

Use the [current Task 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) for APIs, handler startup/shutdown,
three-state outcomes, verification and limitations. One dedicated host and sole
database worker now serve watcher, manual and API clients through Windows named
pipes. Preparation stays outside the database worker; contention waits internally;
duplicates are `NOT_COMPLETED`. SQL/review formats remain 3, playset format 1,
and database arguments are exact SQLite files. Daily maintenance and configurable
30-day raw expiry are preserved. Receiving repairs 07D-01 through 03 are delivered.
The final focused suite passed 53 checks with no skips; isolated imports and
`pip check` passed. Evidence and limitations are in the current handoff.

No production data, configuration, selection or live process was changed.
Historical activation is reported evidence, not a fresh runtime-status check.
Next operational work: verify the configured schema-3 file and restart the watcher
on updated code at a safe boundary, shutting down any older handler for that file.
Task 08 reports use HandlerClient; Run-result replacement and complete Trusted Run
acceptance remain separate. Preserve unrelated uncommitted work.

## Historical checkpoints (superseded where they conflict above)

## Rejected database-handler design retired

Do not continue the former shared-handler review/implementation sequence. The
design has been rejected and deleted; its continuation checklist is withdrawn.
Stop after this documentation cleanup. Replacement implementation instructions
will be issued separately. Existing ingestion, playset handling and daily retention
remain unchanged; older queue follow-up references do not authorize the deleted
design. See [CURRENT_HANDOFF.md](CURRENT_HANDOFF.md).

## Task 07 implementation checkpoint — 2026-09-28

Ingest, raw retention, manual command, schema 2/playset SQL reads, manifest 2 and
per-Run processing lineage are implemented and verified against genuine retained
inputs. [Exact interfaces and evidence](TASK07_INGESTION_AND_RETENTION_HANDOFF.md).
One closure decision remains: malformed/mismatched completed-playset disposition.
Rejecting ingestion and preserving the capture is the pending proposal.

1. Settle that owner decision and close Task 07.
2. Watcher team wires completed-capture ingest and periodic idle-capable retention;
   hourly checks are proposed. Task 07 made no watcher changes or live activation.
3. Task 08 builds SQL-only reports against the delivered storage/read boundary.
4. Perform separately authorized live activation and Trusted Run acceptance.

Explicit same-Run result replacement remains a separately commissioned follow-up.
The Script location-stack investigation is complete and its representation remains.
Earlier dated implementation-pending entries below are historical.

## Task 06B cleanup completed — 2026-09-28

The deprecated CLI/provider stack and its exclusive research/test consumers have
been removed. See [the cleanup handoff](TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md)
for the exact inventory, portable rollback archive, verification and limits.
`watch`, `capture`, `doctor` and `observe-logging` remain; `watch --once` remains
error-only. `harvester.py` remains the capture owner. No processing command is
active. Task 07 delivers ingest and retention APIs, one manual `ingest` command,
playset SQL storage and a watcher-team integration handoff. The watcher team owns
automatic ingest after capture and periodic retention checks, including idle periods.
See the [current scope](TASK07_SCOPE_REVIEW.md)
and [revised draft](TASK07_PROMPT.md).
Task 07 must remove the current database-wide lineage
lock and record processing versions per Run; compatible selections share one
database. Schema changes require an explicit reset, without migration or fallback.
These are instructions for implementation, not completed code. Retention eligibility
and cadence remain open. Task 08 focuses on SQL reports/read operations.
The old provider retirement, C1/C2 capture relocation/deletion proposal, parser
comparison retirement and removed-API research checks are discharged/superseded;
do not repeat them or restore compatibility providers. Task 06/v45 storage and
the watcher producer contracts remain intact, as do learner policy limitations
and the separate Script location-stack investigation. The separately authorized
live watcher was not stopped, restarted, reconfigured or used for verification.
Older dated provider-retention and cleanup-pending statements below are historical.

## Next: Task 06B cleanup, then Task 07 — 2026-09-28

The owner authorized disabling unused old CLI paths and removing their deprecated
providers before Task 07. Execute [Task 06B](06B_DEPRECATED_CODE_CLEANUP.md), then
[Task 07](TASK07_PROMPT.md) against its completion handoff.
Keep the working watcher/playset producer and capture owner `harvester.py` in place;
the earlier plan to relocate capture into `pipeline/capture.py` is superseded.
The watcher review's Section B supplies specific retirement targets. This checkpoint
records the assignment and revised prompts, not completed deletion. The live
watcher's separate operating authorization and Task 06's selected baseline remain.
Older instructions to retain unused CLI providers until cutover are superseded for
the explicit 06B scope.

## Task 06 v45 integration complete; Task 07 next — 2026-09-28

Task 06 has integrated and selected learner v45 package
`68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`:
model schema 5 / matcher API v2, `error-contract-v1`, SQLite schema 1.
The normal source catalog and installed wheel now use the same package.
The existing SQL design stores the new literal choices correctly; no pipeline
source edit, extra processing stage or physical database migration was needed.

Seven complete native logs passed preparation, aggregation, SQLite write/readback,
review completion and separate-process database-only rendering:
418,168 recovered occurrences,
19,912 unique records and four native review emissions.
All original 122 cases / 9,153 emissions are record-eligible. Both line-label
choices retain their exact native spelling. Duplicate rejection, generation
isolation and actual read-only SQLite failure preserve accepted state.
The installed whole-log storage path also passed with checkout resources blocked.
See [the v45 integration handoff](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md)
for exact evidence, storage mappings, changed paths and remaining limits.

The learner assessment's remaining word-run policy issues, two lost matches
against the thirty-log predecessor, capture regressions and tie behavior remain
documented; storage does not reinterpret those outcomes. Development selection
is updated, while production processing and existing application providers remain
unchanged. Next is Task 07 protected-input/processing/replay composition, followed
by Task 08 SQL-only reporting/audit. The historical learner/research retirement
dependencies in the Task 05/06 handoffs remain. No production database writes,
watcher/capture operation, retained-input deletion, commit or push occurred.

The dated selection and "integration pending" statements below retain their
historical context and are superseded by this checkpoint.


## Task 06 completed; Task 07 is next — 2026-09-27

Task 06 delivers exact-identity aggregation, current-generation SQLite Run storage,
and the native review log plus manifest for every successful Run, including zero
review. Template and provisional records remain filterable and render from stored
definitions/values. `write_run` owns staging, finalization, publication, rollback and
commit; Tasks 07/08 consume its [public APIs and detailed handoff](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md).

Three complete unmodified Task 05 inventory logs were verified in fresh ignored
generations: 199,545 recovered occurrences, 190,392 eligible occurrences, 9,396
aggregated records and 9,153 native review emissions. Verification covers exact
bytes/order/frequency, both empty-shard files, duplicate rejection, namespaces,
Run IDs/date basis, count reconciliation, real read-only SQLite rejection and
separate-process database-only rendering. The detailed handoff distinguishes
observed failures from unexercised crash/native branches and records scope proof.

Next: Task 07 protected-input preparation and processing/replay composition;
Task 08 database-only reporting/audit. Operator command choices remain for Task 07
owner review. Existing application providers remain connected until separately
commissioned cutover. Production processing remains disabled. No watcher operation,
live capture, production database write, retained-input deletion, commit or push.

Task 05's named retirement dependencies remain: the historical baseline in
`tools/template_learning/build_parser_comparison.py`, the removed-API consumer
in `inspect_cross_emission_recovery.py`, and opt-in
`test_raw_parser_requirements.py::test_independent_pipeline_replay`. Learner/model
coverage limitations remain unchanged; storage does not repair unmatched or
malformed native patterns. The current selection/package is unchanged.

All dated instructions and task orders below are historical where superseded by
this checkpoint, the approved Error Contract and the Task 06 handoff.


## Task 05 implementation delivered — 2026-09-27

Task 05 is complete: the selected schema-2 package is
`44a0401b8adf0a2953d26705` (unchanged model `76630685c4a341ca14bf9c7c`).
The pipeline now executes pinned recovery and shared complete selection, binds
only selected regions once, and prepares serializable `error-contract-v1` data
with exact identity and standalone rendering. The duplicate pipeline matcher and
its bound-candidate alternatives are removed. All 31 native inventory logs and
the disposable installed path passed; see
[the implementation handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md)
for APIs, resources, evidence, coverage limits and exact changes.

Next: Run aggregation, SQL/native-review persistence and stored reporting;
application/provider cutover remains separately commissioned. Historical
recovery/view retirement still depends on the learner comparison tool's old
baseline. Two additional research/test consumers of removed APIs are named in
the handoff. Production processing remains disabled; no watcher operation,
learner publication, commit or push occurred. Earlier sections below describe
historical checkpoints and do not supersede this completion.

**Task 04 complete; current execution order — 2026-09-27**

The owner approved [the complete Error Contract](ERROR_CONTRACT_SPECIFICATION.md),
including source/emitter through the stored template definition. The learner
selection dependency is resolved by schema-4 release `76630685c4a341ca14bf9c7c`:
`selected` supplies one complete assignment for full and provisional outcomes.
The [Task 04 handoff](TASK04_ERROR_CONTRACT_HANDOFF.md) records interfaces, hashes,
fresh native verification and remaining coverage limits.

1. Completed: [Task 04(B) audit](04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md), owner
   review, learner shared-matcher delivery and
   [independent verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md).
2. [Revised Task 05](05_ERROR_CONTRACT_IMPLEMENTATION.md): integrate the pinned
   shared matcher, bind the selected assignment once, retire the duplicate pipeline
   matcher, and implement contract/result, identity and rendering helpers. Select
   the package after integration verification and verify installed resources.
3. Subsequent tasks: Run aggregation/counting, SQL definitions/records, native-review
   publication and stored-report integration.
4. Separately commissioned application cutover and retirement of old providers.

P1/P2 and the P3 specification are complete. Error typing remains optional future
work; `unknown` is valid. Provisional assignments are SQL-eligible. The original
Task 05 prompt's mandatory new model, L1/L2 gates and semantic-typing dependency
are superseded by the approved contract. The verified matcher package preserves
existing model definitions; no relearning or contract sidecar is required.
Historical recovery/view deletion retains its comparison-tool retirement dependency;
it is not permission to keep those modules in the active processing path.

**Historical record below — superseded where it conflicts with the current
specification and handoff. Earlier pins, unresolved dependencies and remaining
orders describe their dated checkpoints, not today's work.**

**P3 owner decisions and learner assignment dependency — 2026-09-24**

A diagnostic record is the refined, unique error message stored in SQL. Parsing
supplies pieces/spans; assignment supplies template literals, slot placements and
bindings; storage consumes that result without rematching. Identical matched
content within a Run aggregates with an occurrence count; differing slot values
form separate records. Source applicability belongs in template assignment.
Individual occurrence timestamps are unnecessary; lineage belongs in Run metadata.
Template and provisional matches both belong in SQL with a filterable status;
unmatched messages go to the review shard. SQL does not store competing templates.

The current `provisional` result also includes competing assignments, and there
is no #1-selection policy. The owner assigned resolution to the learner team:
[deterministic assignment prompt](LEARNER_SINGLE_ASSIGNMENT_PROMPT.md).
P3 must consume its single-assignment contract. These storage decisions supersede
the older provisional-only-to-shard proposal; the P1 implementation table below
describes current interfaces, not the newly required persistence behavior.

**P1 closed; bounded P2 native verification completed — 2026-09-24**

The owner accepted the P1 implementation. The latest learner correction is now
verified against selected v3 release `a9fa27a85ccd066285b99fdb`, manifest SHA-256
`072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb`, and the
same hash-pinned `ck3-lossless-v1.6` parser. A fresh classifier loads the corrected
trace declarations and additional ordinary LOCATOR captures through existing
interfaces. No further pipeline source adaptation was needed. Error type remains
`unknown`, as authorized.

| Component | Delivered |
|---|---|
| Reader (`pipeline/model.py`) | Release/manifest/artifact integrity, v3 parts and constraints, declaration references, support statuses, immutable model data, and verified parser loading. Unsupported schemas/types/constraints fail explicitly. |
| Catalog (`pipeline/catalog.py`) | Reads `models/selection.json`, checks the selected revision, and resolves source or installed release resources. Existing package configuration includes the complete release. |
| Matcher (`pipeline/classifier.py`, `pipeline/matching.py`) | Exact complete-message literals; KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM and intact REASON; all declared constraints; construction/exclusion and parameter-structure selection; required wrapper context. Counts every complete capture assignment across all applicable candidates. |
| Results (`pipeline/domain.py`) | `full`, `provisional`, `unknown`; template IDs; candidate alternatives, exact assignment counts and up to two witnesses per region; explicit provisional/unresolved reasons. Only a unique supported/confirmed assignment supplies accepted bindings. |
| Bindings (`pipeline/bindings.py`) | Exact original byte spans and values, including wrapper-relative conversion and surrogateescape. Declared absence has `value=None`, `span=None`, including optional PARAM/LOCATOR fields actually supplied in this release. |
| Input (`pipeline/raw_input.py`) | Uses the selected parser's messages/pieces, recovers each emission once, retains wrapper spans and unresolved parent evidence. No normalization stage in the selected path. |

Runtime declarations come from the selected release. The neutral parser loader
is the only learner-package dependency. The old framing/recovery/view code is
retained for `tools/template_learning/build_parser_comparison.py`; the selected
runtime path does not import it. The old layered result interfaces were removed.
The release's complete outer message with REASON supersedes separate L1/L2 matching.

**Reviewable interface**

```python
from ck3chronicle.pipeline.catalog import load_selected_classifier

classifier = load_selected_classifier()
raw = classifier.read_log(native_log_path)
for result in classifier.classify_raw(raw):
    # NativeClassification or UnresolvedEmission; no database writes.
    ...
```

`NativeClassification.diagnostic` retains original evidence and context.
`candidates` retains provisional/ambiguous alternatives; `template_id` and
`bindings` are populated only for `full`. Parser identity remains on the raw
input/model, rather than being duplicated in each result.

**Current native verification and review**

[Refreshed spot-check report](../.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/index.html):
72 samples / 120 native examples, with complete templates, captured values,
original spans and provenance. Sample M01 is the reviewed tribute-mission case:
four LOCATORs and two trace PARAMs. Browser checks passed for navigation, search,
bindings, unmatched evidence, whitespace display and narrow-screen layout.

The report replays three complete retained logs:

| Log SHA-256 | Full | Provisional | Unknown |
|---|---:|---:|---:|
| `152f6ba75c1dfe9fea2e8dcfac35ce61258da1d2c49d634ffac7a304a088e370` | 1,856 | 267 | 0 |
| `16d3ab935f938e63ae3dd460dfeffeee6f32c2a31d95782fd787356f1afce196` | 3,458 | 5,191 | 74 |
| `48f3aca380e7e0c44945becc7f3e60392b0288ed95f41d2a1c5c042d9718874c` | 28,175 | 69,684 | 1,065 |

109,770 messages; no unresolved parents. Outcome totals are observations of the
corrected model, not targets inherited from the previous release.

P2 independently replays six complete native logs selected for the five earlier
REASON-boundary witnesses and the trace-boundary audit's zero/55-frame examples.
One log also appears in the report above; these totals must not be added together.

| Log SHA-256 | Full | Provisional | Unknown |
|---|---:|---:|---:|
| `0e3c3ce0270bfda5dce5b45c845886c16353abde90aceda41a8a76111e2fc008` | 6,343 | 16,533 | 11,681 |
| `2e62dfc0c104491e7beac39d911b84075d4abd51c08fb51b083367a927cfb66a` | 19,874 | 4,978 | 19 |
| `bc2de94bfc6992dd928a6cc15e8eb3845085b0390f89816e8cb10c358257ba78` | 15,744 | 8,424 | 312 |
| `48f3aca380e7e0c44945becc7f3e60392b0288ed95f41d2a1c5c042d9718874c` | 28,175 | 69,684 | 1,065 |
| `8c7eaa6319a5dd7851ed4c186a8564755b1c3eb7a9f4c90b792e2c1b5611efcf` | 56,393 | 42,627 | 4,340 |
| `9d3622ab1b6c85cbab45d83767bb870b06c6fb9d6da50ee44f5eba3674d98cbc` | 14,456 | 448 | 9,210 |

All 310,306 messages from 302,245 emissions were accounted for. Checks passed for:

- Complete original-file and recovered-emission byte-span coverage, input hashes
  and retention of native evidence for every outcome.
- 1,082,002 present captures across all six types, checked against original bytes;
  18,582 absent optional captures kept distinct from present values.
- 310,995 candidate regions reconstructed from exact literals and captures,
  including required contexts for 13,658 wrapped messages.
- Unique supported assignments for every full result; provisional/unknown results
  expose no accepted template or bindings.
- All five previous REASON witnesses and the 55-frame trace return ordinary
  unknown with no declaration error. The zero-parenthetical-trace example is full.

[Native verification evidence](../.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/native-verification.json)
records exact paths, hashes, counts and witness occurrences.

Separately, the learner's supplied ten-log pipeline replay covers 352,317 messages
and reports agreement on all outcomes/captures. All eleven recorded pipeline
source hashes were checked against this checkout and agree. This is supplied
corroborating evidence, not another replay performed during this closeout.

**Verification limits and follow-up**

The six-log replay found no competing templates, ambiguous capture assignments,
recovery failures or accepted empty REASON captures. Those branches remain
unverified by native cases. The real empty-REASON witness is retained as unknown;
its successful processing does not establish accepted empty-field binding or
storage. Installed-wheel execution and corrupt-input rejection were not tested
here. No synthetic input, substitute template or test-file requirement was used.
These checks establish implementation behavior on the stated evidence, not
universal model coverage or semantic accuracy.

Earlier v26 checks remain historical evidence: 21,446 original-byte captures,
10,537 exact comparisons with pinned saved native records, old-schema rejection,
syntax/import checks and packaging inspection. The v27 figures above supersede
its outcome totals. The earlier allow_empty validation/enforcement remains in P1.

**Remaining order**

1. P3: propose the minimal Error Contract specification for aggregation,
   rendering and lineage, with error type allowed to remain unknown.
2. Implement the agreed contract specification. Retain the native coverage gaps
   above for genuine future examples; do not manufacture verification cases.
3. Separately commissioned application/SQL integration and stored-report proof.

Learner-owned follow-up remains in the learner handoff: location-only support
policy, name recognition and flat-template duplication across trace-frame counts.
P1 has no outstanding implementation item. P2's bounded replay is complete with
the explicit coverage limits above. This closeout changed status documentation
and ignored review artifacts only; source, models, learner code and application
processing were unchanged. No database writes or commit occurred.

**Historical pre-v3 proposal follows**

The current delivery above supersedes the following dated state, layered-matching
rules and typing dependencies. The older discussion is retained as decision history.

Updated: 2026-09-18. This document consolidates the Task 04 discussion and the
owner's corrections. It separates existing implementation, required behavior,
open decisions and proposed sequencing. It does not approve unresolved design
choices or claim that the implementation work is complete.

The companion [learner/model handoff for the separate development team](LEARNER_MODEL_DEPENDENCIES.md)
preserves all supplied learner/model findings, questions, corrections and
evidence, including those with no Task 04 dependency. Pipeline impact is
recorded separately and does not determine whether knowledge is retained.
The Task 04 agent owns preparing that handoff; the separate team owns learner
implementation. Creating these documents does not commission learner changes,
training, model publication, production processing or application cutover.

**Corrections to the earlier proposal**

- Use **template ID** for the identifier of a supplied template. There is no
  separate “cluster ID” or “template reference” concept in this design. The
  existing code/artifact field named `cluster_id` currently stores the template
  ID; that spelling is discussed below only to explain the present files.
- `error_type` remains the sole hierarchical diagnostic taxonomy.
- “Semantic typing failure” was assistant wording with no owner-directed
  deliverable behind it. It is withdrawn: no field, outcome or subsystem is
  commissioned under that name.
- Do not require semantic slot names, authored prose roles, a generic
  `conditions` language, a `nonidentity_fields` registry or “complete field
  disposition.” Preserve captures through positional references instead.
- Enforce only the supplied template's declared slot types, optionality and
  constraints. Observed examples do not authorize additional restrictions.
- L1-only matching is permitted for layered templates. Independent L2 reuse
  within applicable source scope is permitted after L1 matches. Neither an
  L1-only prohibition nor approval of individual L1/L2 pairs belongs here.
- The proposed one-off event-theme mapping is not the population strategy.
  Deterministic error typing remains an open dependency.

**Verified terminology and owner direction**

The current field `cluster_id` is the template ID. For example,
`a7451146877a3211` identifies the supplied `Unknown trigger : <KEY>` template
from `pdx_persistent_reader.cpp` in the selected model. It is a truncated
SHA-256 of canonical source-family/template-token content. It does not name
a group of related diagnostics or explain what those diagnostics mean.
The field `source_cluster_id` is the predecessor artifact's template ID,
retained as provenance; it is not another live diagnostic identity.

The future analytical grouping called “related-error cluster” in the recovery
vocabulary is a different, unimplemented concept. It has no role in this
pipeline proposal. The earlier explanation unnecessarily conflated terminology
around that future concept and the present template ID.

Use template ID consistently in the design and the next agreed interface/
artifact format. Do not add another ID alongside it or preserve the duplicate
design terms. The current serialized spelling must be changed through
coordinated producer/reader format work; the repair supplement explicitly keeps
the supplied model artifacts unchanged. This documentation update therefore
does not rewrite their bytes or install a compatibility alias. A matched layer
is identified by its template ID and whole/L1/L2 part within the model revision;
the current model stores no independent layer IDs.

See [model identity](../src/ck3chronicle/pipeline/model.py),
[template IDs in matching results](../src/ck3chronicle/pipeline/domain.py), and the
[recovery vocabulary](CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md).

**Current state**

| Item | State | Consequence |
|---|---|---|
| Native occurrence/value/span interfaces | Present | Extend the owning components; preserve complete original values. |
| Selected empirical artifact | Present: `43634d23e619ecb4`, 889 entries, 238 with layers | Supplied input to runtime; not a complete Error Contract artifact. |
| L1-first routing and revised outcome labels | Present in classifier revision `ck3-exact-empirical-classifier-v2` | Preserve this behavior during cleanup. Prior bounded checks do not validate all preprocessing. |
| Phrase-specific preprocessing and extra slot restrictions | Still present; cleanup outstanding | Existing classification results are not proof that these rules comply with owner direction. |
| Deterministic error-type derivation | Unresolved; absent from selected artifact | Required input before finalizing type consumption in the contract implementation. |
| Aggregation identity, rendering details and final contract format | Proposed/incomplete | Settle the actual record requirements before implementing persistence-facing behavior. |
| Model defects | Open in `MODEL_BUGS.md` | Report unsupported structures; do not hide them with runtime exceptions. |
| Application cutover and production operations | Outside this work | Existing providers remain connected until the separately commissioned cutover. |

**Pipeline behavior to retain or implement**

The processing flow is protected native emission, recovered occurrence,
evidence-preserving matching view, source-applicable template matching,
original-value binding, and contract-directed diagnostic processing.

Matching determines capture boundaries. The pipeline must not pre-identify
semantic slots, mask recognized sentences into typed markers, rewrite literal
words, invent absent optional slots, or move those rules after matching.
Native framing, approved occurrence recovery, source identification, ordered
literal matching, ambiguity handling and original-span integrity remain
necessary mechanics. Recovery/extraction calls must be checked against the
same boundary; a splitter is not permission to interpret arbitrary messages.

One supplied KEY slot captures one complete key, including punctuation and
numeric components. PARAM captures variable phrases and is a valid type.
No occurrence is retyped from KEY to PARAM to satisfy an extra runtime rule.
The current artifact's other markers require an explicit shared-format
decision; their mere presence does not approve their semantics.

Slots need a structural part, template position, declared type and captured
value/correspondence. Human semantic names are not required for storage or
rendering. Constraints and optionality apply only when actually supplied;
the pipeline does not derive limits from observed examples.

| Matching situation | Outcome | Assigned references |
|---|---|---|
| Non-layered whole template matches | `matched to template` | Whole only |
| L1 matches and an applicable L2 matches | `matched to template` | Independent L1 and L2; no whole reference |
| L1 matches and L2 does not | `L1` | L1 only |
| No applicable assignment, including no L1 for a layered occurrence | `unknown` | None |

L2 is searched only after L1 succeeds. Its original stored pairing cannot
restrict reuse or supply a different L1/trigger/effect characteristic.
L1 is eligible for the corresponding diagnostic record; unresolved L2
evidence remains preserved. The eventual type/identity specification must
represent L1 rather than silently require L2. No new failure taxonomy is
proposed. A distinct `incomplete` outcome is not implemented or newly
commissioned here; add one only if the owner supplies a concrete definition.

**Contract and record responsibilities still to settle**

| Responsibility | Pipeline requirement | Remaining decision/input |
|---|---|---|
| Definition identity and lineage | Reference the exact supplied whole/layer definition and revisions used | Minimal contract identity/revision representation; avoid redundant identities without purpose |
| Error type | Consume model/contract-defined type through the same classification path | Offline derivation, hierarchy, L1/L2 composition and behavior for an untyped structure |
| Aggregation | Count equivalent occurrences within a Run; retain meaning-bearing differences | Participating slot/locator values, equality rules, and L1 aggregation when unresolved L2 reasons differ |
| Rendering | Render deterministically from supplied literals and captured values; store reportable text | Whitespace/punctuation/optionality rules and stable L1 rendering |
| Evidence | Preserve exact original values/spans; native unresolved content remains outside SQLite | Minimal stored representative provenance without implying full-log reconstruction |
| Packaging | Load one integrity-checked selected definition set | Embedded definitions versus one jointly selected sidecar; exact fields and revision relationship |

Timestamps and emission positions are repetition metadata, not automatic
diagnostic identity participants. A template ID alone also does not
determine equality of occurrences with different captured values. This is an
aggregation question, not another taxonomy.

The sidecar remains a recommendation, not an approved schema. If chosen, one
bundle contains a manifest, empirical model and `error_contracts.json`; the
manifest binds both files, and the catalog selects them together. The old
proposal's withdrawn fields must not reappear in it. Model generation stays
offline under either representation.

Every successful Run finalizes one native review shard, including an empty
one. Approved occurrences are counted once; reviewing a parent emission must
not count an already assigned child twice. Protected originals remain retained.
Reports use stored facts and rendered text without reopening logs or models.
Meaning-changing generations follow the fresh-database-generation policy.

**Proposed pipeline execution order**

P1/P2 are the repair and verification assigned by the Task 04 supplement;
P3 is the Error Contract specification that follows them. They are outstanding
assigned work, not merely optional recommendations. P4/P5 describe later
dependencies and do not commission additional implementation or cutover.

| Order | Work | Dependencies | Concrete result |
|---|---|---|---|
| P1 | Remove prohibited preprocessing and extra acceptance rules; make matching/binding use supplied structures and original values end to end | Existing owner rules; any genuinely unsupported format/type must be reported explicitly | Coherent template-driven matching path, with required revision updates and no false compatibility claim |
| P2 | Verify P1 on genuine retained occurrences; record remaining template defects against existing model issue IDs | P1 | Evidence for whole KEY capture, variable PARAM capture, preserved literals/spans, L1-first routing and independent L2; honest unresolved results |
| P3 | Finalize the pipeline-facing Error Contract specification | P1/P2 findings; offline type decision and shared slot-format decisions from the companion document | Exact minimal identity, aggregation, rendering, lineage and artifact-consumption rules |
| P4 | Implement the approved contract-consumption behavior in the same processing path | P3 and a compatible supplied contract/model artifact; separately agreed implementation scope | Deterministic diagnostic assignments and aggregation inputs, without learning or a projection service in runtime |
| P5 | Hand the verified interfaces and remaining limitations to the later Run-storage/report/application work | P4 | Concrete continuation point; no premature cutover or production processing |

**Task 04 supplement mapped to executable work**

The [supplement](../src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md)
has been read in full. Its source-repair assignment is included here, not
deferred into learner work. P1 is one coordinated processing-path repair:

| Component/action | Required change | Step |
|---|---|---|
| `normalization.py` | Remove semantic rewriting from `_Composer.key_path`, `known`, `structured`, `persistent` and their active callers. Preserve an evidence-bearing matching view without preassigned typed markers, invented optionals or altered literals. | P1 |
| `classifier.py` | Remove independently imposed `_accepts` restrictions. Match the supplied literals and ordered slots; let the template determine capture boundaries and any declared constraints. Preserve explicit ambiguity handling. | P1 |
| `bindings.py` and necessary adjacent pipeline interfaces | Bind each matched slot to its complete original value and exact spans, including punctuated/numeric KEY values and multi-word PARAM values. Keep one processing path. | P1 |
| Recovery and extraction calls | Inspect their active path for the same banned pre/post-match interpretation. Retain necessary native framing, source and occurrence evidence. Do not introduce a name recognizer or a new slot type. | P1 |
| Model loading and revision dependencies | Report unsupported formats/revisions explicitly. Do not alter supplied templates, falsify hashes/compatibility, or disguise a loading failure as an unmatched occurrence. | P1 |
| Existing routing | Keep `matched to template`, `L1`, `unknown`; L1 before L2; independent L2 reuse within source scope; no L1/trigger/effect inheritance from L2; no fabricated `incomplete` outcome. | P1/P2 |
| Genuine-log verification | Exercise complete punctuated KEY capture, variable-length PARAM, preserved literals and original spans, L1-first matching, independent L2 reuse and retained unresolved evidence. Confirm prohibited phrase rules and extra restrictions are no longer active. Old match counts are not correctness targets. | P2 |
| Learner enhancement requests | For remaining template deficiencies, follow `MODEL_BUGS.md`: native evidence/path/location, model and template IDs, actual structure/result, proposed improvement, known/unknown training coverage, retained evidence and no compensating runtime rule. | P2 |
| Completion deliverable | Deliver implemented cleanup, changed interfaces, verification results and remaining template limitations, followed by the proposed Error Contract specification. | P2/P3 |

The [rule audit](../src/ck3chronicle/pipeline/PIPELINE_RULE_AUDIT.md) supplies
the exact locations, genuine evidence and reproductions for this work. The
supplement's requirements govern the changes. Neither the two documents nor
the pre-existing routing changes constitute completion of this repair.

P1/P2 do not require an exhaustive error taxonomy or 100% repaired-template
coverage. They can proceed while the owner arranges the separate learner/model
work. Particular unsupported type/format cases may still require a specific
decision; they must not be silently coerced or reported as ordinary nonmatches
when the model cannot be loaded. P3 can resolve rendering and identity questions
while typing is investigated, but cannot be declared complete without its
remaining inputs. Independent work here means separate workstreams, not an
instruction to spawn agents.

**Scope and next action**

The next assigned executable pipeline action is P1, followed immediately by
P2 and then the P3 specification deliverable. This documentation review
performs none of those implementation steps and does not mark them complete.

The original Task 04 assignment was specification-only. The later
[pipeline repair supplement](../src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md)
records source-repair scope confined to `src/ck3chronicle/pipeline/`, with
learner code/model artifacts unchanged. It does not commission training,
model publication, databases, watcher activity, production replay, commits,
pushes or application cutover. The inspector remains separate.

The [current template instructions](../src/ck3chronicle/pipeline/OWNER_TEMPLATE_ASSIGNMENT_INSTRUCTIONS.md)
and [rule audit](../src/ck3chronicle/pipeline/PIPELINE_RULE_AUDIT.md) supply the
focused continuation evidence. Existing project-wide status documents contain
older statements; they do not supersede the current owner discussion.
