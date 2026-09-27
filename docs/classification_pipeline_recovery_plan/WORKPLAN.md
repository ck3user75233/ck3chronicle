# Classification pipeline recovery workplan

Status: expanded implementation handoff for owner review, 2026-09-13.
The owner endorsed three stages with seven mini-projects. This revision builds
out their prompts; product implementation and verification design are not
performed by preparing these documents.

## 1. Target pipeline, record fields and evidence

### 1.1 Governing definitions

| Source | Governing content |
|---|---|
| [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md:89) 89–105 | Run ID, emission, recovered diagnostic, compact diagnostic record, template, approved error contract and native review shard. |
| [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md:108) 108–146 | Classification/accounting policy, direct contract ownership, native review storage and retained original logs. |
| [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:118) 118–153 | Emission splitting, assignment, aggregation and component boundaries. |
| [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:176) 176–191 | Native shard content, Run association and review metadata. |
| [docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md:205) 205–254 | Current target vocabulary and flow; error type is the sole hierarchical diagnostic taxonomy label. Technical input, subordinate to the owner documents. |
| [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277 | Contract-defined identity, slots, rendering, occurrence counts, first/last observation and interpretation lineage. |

A **diagnostic record** is specifically the compact SQLite representation of
an approved diagnostic identity within a Run (owner intent 95).
A **recovered diagnostic** is a transient processing unit extracted from an
emission (94; architecture 166). Unclassified processing results do not become
“unclassified diagnostic records.” Their original emissions go to native review,
with the metadata specified by architecture 188–191.

### 1.2 Information sought for each error

This table assembles the fields specified in the sources above. Values are
populated when observed or authorized by the applicable contract. The taxonomy
is `error_type`; this field inventory is the record's information contract.

| Information | Definition and source | Present implementation/reference-data position |
|---|---|---|
| Run ID | Successful processed Run association; owner intent 89/95 | Present Run metadata exists; current-generation representation is rebuilt. |
| Engine source | Observed CK3 source family, not inferred error type; recovery review 211 | Model `source_family` and emission header. |
| Contract/template identity and revision | Approved template and its versioned assignment rules; owner intent 97–98, Trusted Run 255–270 | Structural model has `cluster_id`, `template_tokens`, model revision and optional layer contracts. |
| Assignment level | Current `full`, `l1_l2`, `l1`, `unknown`; recovery review 216 | Current runtime result; exact meanings and limits in 1.3. |
| Hierarchical error type | Sole diagnostic taxonomy label; recovery review 217–218 | **Absent from the selected structural model.** Old projection/extractor labels are not a complete approved direct-contract index. |
| Typed slot roles and concrete values | Applicable contract defines roles; matching extracts occurrence values; owner intent 98, recovery review 219 | Current templates contain typed placeholders; runtime returns `structured_slots`. Example slot values in model evidence are not a complete approved field dictionary. |
| Relevant file, symbol, line and other locator values | Include those required by the particular diagnostic identity; Trusted Run 255–258 | Useful extraction code is ported; applicable identity roles must be supplied by direct contracts. |
| Stable rendered text | Render stable text from the versioned contract; Trusted Run 268–270 | Selected structural template text exists; the selected model lacks a complete direct rendering specification. |
| Aggregate identity and repetition | All contract-defined identity fields agree; occurrence count and first/last observed timestamps; Trusted Run 255–262 | Old regex signatures and issue/occurrence tables implement a different representation. |
| Interpretation lineage | Application, parser/splitter/normalizer, model, contract and schema revisions; Trusted Run 276–277 | Current revisions are spread across stage-specific rows; new Run storage carries required current lineage. |
| Review evidence and metadata | Original emission plus Run/source/revisions/routing reason/count/integrity; architecture 176–191 | Target native review path is new. SQLite stores count/reference/availability/hash, not the unresolved native payload. |

There is no standalone complete canonical list of error-type values or exhaustive
per-contract field dictionary in the inspected governing documents and selected
model. The review defines the hierarchy and gives `script_system.wrong_scope`
as an example; it does not enumerate all approved types. The old category/error
type registries and projection catalog cannot serve as that authority.

The direct model revision must supply established contract definitions and
identify any exact missing/changed definition before dependent record writing.
The table above is the cited target field inventory, not a claim that all those
fields already exist in the current reference model.

### 1.3 Current structural matching: exact model and code evidence

The selected artifact is
[models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1).
Its immutable selection is at
[src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:13) 13–16.
Inspection of its 891 cluster entries found 240 with `layer_contracts` objects
and 651 with `layer_contracts: null`.

Concrete entries with null layer metadata:

| Cluster ID | Engine source | Exact structural template |
|---|---|---|
| `21b477c6e94b1681` | `pdx_persistent_reader.cpp` | `Unknown trigger : <KEY>` |
| `03e05f6617f59e8c` | `eventmanager.cpp` | `Event ' <KEY> . <VALUE> ' expected scope ' character ' , but got ' <KEY> '` |
| `63ae011e79992a5f` | `jomini_script_system.cpp` | `Script system error ! Error : Invalid activity object` |

These are structural-model entries, not projection rows or fallback issue
records. The proof of their production matching path is
[src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:91) 91–124:
candidate comparison, `validate_template_tokens` at 104, then a valid whole
template returns `full`; layer text is optional at 121–122.
This proves current structural matching, not that each entry already contains
every field of the target approved error contract.

The learner uses one clustering/derivation path:
[tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1024) 1024–1099.
Its `serializable_cluster` 1485–1530 adds optional layer metadata using
`script_system_layer_tokens` 744–783. That function recognizes a specific
script-system outer-envelope/bracketed-reason grammar. Other structures return
no layer metadata. There are not two separately invoked learner modes.

| Current result | Proven runtime meaning |
|---|---|
| `full` | Whole typed template validates. This includes model entries with and without optional L1/L2 metadata; inference 109–124. |
| `l1_l2` | Exact known outer envelope plus a validated reason contract; inference 126–183. |
| `l1` | L1 outer envelope matches successfully and L2 remains unclassified; inference 134–147 / 184–195. This is not a partial match to an error template. |
| `unknown` | No supported structural classification established; contract ID and L1/L2 template fields are null, score 0.0; inference 197–208. Extracted slots may still exist transiently. |

The current service persists these results, including unknown results and
extracted slots, in the intermediate classifier payload store:
[src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1852)
1852–1875 / 1912–1930. The projection later creates unknown IssueDrafts at
[src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:475)
475–496. These describe the old representation being removed. The canonical
target stores native unresolved emissions and review metadata, as stated in 1.1/1.5.

The plan ports these identified matching mechanics. “Complete non-layered
diagnostic classified” is not a separate proposed mode or an assertion that
all current structural entries already have complete direct contracts.

### 1.4 Provisional/low-confidence: policy versus implemented state

Current evidence is specific:

- The selected model's cluster fields have no `provisional`, `approved`,
  per-contract `status` or `confidence` field.
  [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:38) 38–52 / 86–138
  defines and loads the structural fields, including optional layers.
- `ClassificationResult.confidence` is a runtime number
  ([src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:28) 28–41).
  Whole matches use the candidate similarity score; L1-only returns 1.0;
  unknown returns 0.0. The classifier has four assignment-level branches,
  not distinct `provisional` or `low_confidence` branches.
- [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:244) 244–264 permits precisely
  `full`, `l1_l2`, `l1`, `unknown` in its classifier payloads.
- The old projection supplies separate categorical confidence labels:
  [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:475) 475–496 creates an
  unknown issue with `confidence="low"`; 513–529 reads projection confidence.
  This mechanism is a removal target.
- Owner intent 110–111 and architecture 133–138 explicitly name provisional
  and low-confidence outcomes and require review routing. They do not specify
  a per-contract field, threshold or current runtime trigger for those states.

Thus the preservation policy is canonical, while its proposed labels must not
be represented as existing model states. No extra threshold, provisional model
entry or post-match downgrade is introduced by this plan. A future explicit
operational definition must be settled before adding such a state. Existing
similarity scores are not calibrated probabilities or approval statuses.

The artifact's global `algorithm.status="wip_incremental_calibration_not_production"`
and `evaluation.status="calibration_only_not_holdout"` are authoring metadata;
they are not per-template provisional markers used by the production loader.

### 1.5 Target production flow and native review

Capture means **copying the completed Run's live log into protected pending
storage**. It precedes parsing/classification. Architecture 147 assigns that
boundary; [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:179) `spool_logs` 179–342
implements copy-only capture. The processor starts from the protected input.

| Target step | New owner | Required result |
|---|---|---|
| Protect completed Run evidence | `pipeline/capture.py:spool_logs` | Stable protected copy, supplied lifecycle facts and bounded crash attachment. |
| Prepare selected input | `pipeline/inputs.py:prepare_pending_input/prepare_manual_input/prepare_retained_input` | Explicit source, full-file hash and observed metadata. |
| Recognize emissions and recover diagnostics | `pipeline/emissions.py:iter_emissions`; `pipeline/diagnostics.py:recover_diagnostics` | Original spans/values and source-specific child boundaries. |
| Match approved contracts | `pipeline/model.py:load_model`; `pipeline/classifier.py:Classifier.classify` | Typed structural outcome carrying direct contract fields where authorized. |
| Aggregate and route review evidence | `pipeline/aggregation.py`; `pipeline/review.py` | Compact approved identities/counts; original emissions requiring review. |
| Complete the Run | `pipeline/processor.py:process_input`; `pipeline/repository.py:write_run` | Current-generation Run records and native-shard metadata. |
| Report the stored Run | `pipeline/reports.py`; `pipeline/audit.py` | Database-only views of current records and metadata. |

Full absolute file paths are enumerated in section 2.
The learner is not a step in this flow.

For review-routed results, store original emission bytes, including header and
continuations, in order and frequency. Keep the Run ID, routing provenance,
counts, availability and integrity metadata defined by architecture 176–191.
SQLite contains the shard reference/metadata; transient extracted slots do not
turn an unresolved result into a diagnostic record.

For a split emission with approved and unresolved children, the proposal is one
native emission in the shard plus child routing metadata, with separate emission
and diagnostic counts. This physical detail remains a proposal.

Every successful Run has one shard, including empty when review is unnecessary.
The full original protected log is separately retained indefinitely. Every
recognized emission is accounted for; 100% classification is not required.

## 2. Exact file scope by mini-project

The production package is constructed in Stages 1 and 2. Stage 3 constructs
application-facing consumers, then switches the application and removes the
old providers in mini-project 3.2. The seven scopes below are sequential.
Source reads do not grant mutation permission.

### 2.1 Files to create

| Mini-project | Exact new file |
|---|---|
| 1.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/__init__.py` |
| 1.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/domain.py` |
| 1.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py` |
| 1.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/emissions.py` |
| 1.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/diagnostics.py` |
| 1.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py` |
| 1.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py` |
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/model.py` |
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/catalog.py` |
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py` |
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/models/<new_revision>/empirical_template_model.json` |
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/models/<new_revision>/manifest.json` |
| 2.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/aggregation.py` |
| 2.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/review.py` |
| 2.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/schema.py` |
| 2.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/repository.py` |
| 2.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/capture.py` |
| 2.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py` |
| 2.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/processor.py` |
| 2.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/replay.py` |
| 2.2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/playset.py` |
| 3.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/reports.py` |
| 3.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/audit.py` |
| 3.1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/commands.py` |

`<new_revision>` is the content-derived identity specified in section 7.
Resolve and record the two concrete artifact paths before writing them.

### 2.2 Files to edit

Mini-project 1.3 may edit these files created by preceding mini-projects:

| Mini-project | Exact file | Permitted change |
|---|---|---|
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py` | Add R5 typed validation and its binding result to the direct interfaces from 1.1. |
| 1.3 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py` | Set the shared normalization identity for the direct artifact; grammar corrections require a specific handoff to 1.2. |

All other edits to existing files belong to mini-project 3.2:

| Mini-project | Exact existing file | Permitted change |
|---|---|---|
| 3.2 | [tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35) | Only the lexer/type/call reconnection and obsolete-tool removal edits enumerated in 3.2. |
| 3.2 | [tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:366) | Remove frozen-oracle build dependency/argument and associated evaluation output, as enumerated in 3.2. |
| 3.2 | [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md:1) | Update the tool inventory for the actual remaining files. |
| 3.2 | [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md:1) | Update obsolete tool ownership/reporting references; retain the existing learner location and candidate/promotion boundary. |
| 3.2 | [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:11) | Exact handler removals and new command/capture registrations in 6.1. |
| 3.2 | [src/ck3chronicle/watcher.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:17) | Capture-error import at 17–20. |
| 3.2 | [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:12) | Remove unreachable old-Python import fallback at 12–15. |
| 3.2 | [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) | Selected model package data at 29–34. |
| 3.2 | [models/README.md](C:/Users/nateb/Documents/ck3chronicle/models/README.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/DATA_COMPATIBILITY_AND_OPERATIONS.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATA_COMPATIBILITY_AND_OPERATIONS.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/MODEL_QUALITY_AND_PROMOTION.md](C:/Users/nateb/Documents/ck3chronicle/docs/MODEL_QUALITY_AND_PROMOTION.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/REPOSITORY_AND_BACKUP.md](C:/Users/nateb/Documents/ck3chronicle/docs/REPOSITORY_AND_BACKUP.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/WORKSPACE_ROUTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/WORKSPACE_ROUTING.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [README.md](C:/Users/nateb/Documents/ck3chronicle/README.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |
| 3.2 | [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md:1) | Only the implemented source/command/model/continuation facts enumerated in 8.3. |

### 2.3 Files to delete and package scope proof

Mini-project 3.2 owns all deletions: section 6.2, section 6.3 and the five
artifact files in section 7. Mini-projects 1.1–3.1 delete no existing files. Source-reading permissions do
not add files to these mutation lists.

At entry to each implementation package, record its starting source state and
resolved create/edit/delete list. At exit, supply a changed-path comparison
against that starting state and demonstrate that every creation, edit and
deletion is within the list. Account for pre-existing changes separately.
A path outside the list requires an amended instruction before mutation.

The comparison includes tracked, untracked and ignored files in the checkout,
and any explicitly authorized external output paths. Git diff alone cannot
prove the state of ignored or untracked files. This file-scope proof is the
owner's explicit package-exit requirement; product-test/evaluator design remains
the separate task described in 8.1.

Git can restore committed source snapshots. Uncommitted edits and untracked/
ignored files are not automatically protected. Record a recoverable source
baseline before implementation; preserve existing owner work. The planning
files in this directory are currently untracked, so HEAD alone would not
restore their present contents. This planning revision does not commit them.

Authority and operational context: [docs/BANNED_IDEAS.md](C:/Users/nateb/Documents/ck3chronicle/docs/BANNED_IDEAS.md:37) 37–87,
[docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md:1), [docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md:1) and
[docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md:1). The complete existing graph is recorded in
[docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md:1) and
[docs/classification_pipeline_recovery_plan/CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md:1).

## 3. Exact ports and integration edits

### 3.1 Production classification core — Stage 1

| ID | Existing source and exact scope | New destination and port treatment |
|---|---|---|
| R1 | [src/ck3chronicle/parser/log_blocks.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:26): `TimestampedLogBlock` 26–46; `source_block_id` 49–58; `_without_line_ending` 61–66; `_decode` 69–70; `_parse_header` 73–98; `_make_block` 101–139; `iter_log_blocks` 142–257; header/source/BOM definitions 16–23 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/emissions.py`: port lexer mechanics into `iter_emissions` and its private helpers; emission data moves to `pipeline/domain.py`. Supply real provenance explicitly. Omit the two-bracket fixture header at 19–21/86 and old constructor defaults. Decoded text is not the native review copy: preserve original byte spans. |
| R2 | [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:253): `block_message` 253–263; `split_location_evidence` 266–270; `extract_structured_slots` 273–422; `normalize_key_path` 425–437; `normalize_structured_slots` 440–501; `normalize_known_key_grammars` 504–592; `mask_locators` 626–631; `tokenize` 634–642; `script_system_layers` 645–670; `diagnostic_lead` 673–718; `reason_lead` 762–768; their constants/regex definitions 13–250 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py`: port these pure routines and their grammar definitions. Adapt block access to new emissions/diagnostics; remove the 384-token truncation at 638. Preserve a separate original-value binding view. Do not port `legacy_diagnostic_lead` 721–759. |
| R3 | Same [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:595): `_normalize_persistent_clause` 595–603 and `semantic_units` 606–623, specifically wrapper/clause recognition at 608–620 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/diagnostics.py`: port only the recognized persistent-reader splitting grammar into `recover_diagnostics`; write child spans/value ownership afresh (N2). Do not port lossy string normalization as the recovery result. Normalization follows recovery. |
| R4 | [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:135): `_path_from_match` 135–140; `_overlaps` 143–144; `_extract_locators` 147–181; supporting path patterns 39–77 and `_EVENT_URI_RE` 80; `LocatorEvidence` 97–102 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py`: port pure path/line extraction, adapted to preserve source spans and original spelling. Keep event URIs distinct from filesystem paths. Define the current locator value in `pipeline/domain.py`. Nothing else from the projection module is a port: typed values come from R2 and N2, not a post-classification mapping dispatcher. |
| R5 | [src/ck3chronicle/classification/contracts.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:22): `ValidatedSlot` 22–35; `TemplateValidation` 38–42; `_literal_equal` 45–50; `_closed_alternatives` 53–59; `validate_template_tokens` 62–146; imports/constants 1–19 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py`: port exact literal/typed-slot matching and ambiguity rejection. Extend the new direct contract/binding result under N1/N2. Similarity never substitutes for typed validation. |
| R6 | [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:24): schema/version constants 14–17; `ModelIntegrityError` 20–21; `LayerContracts` 24–35; `ModelCluster` 38–52; `EmpiricalModel` 55–64; validation helpers 67–138; `load_model` 141–191. [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:25): `_approved_revision_root` 25–45; `approved_model_path` 48–49; `load_approved_model` 56–57; `load_approved_classifier` 76–77 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/model.py` and `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/catalog.py`: port immutable hash/integrity checks, supported direct-contract structures and explicit source/install artifact lookup. Adapt to one current format. Keep one current normalization-version identity shared by the pure grammar and artifact readers/writers; do not preserve conflicting copies. Bind the new catalog to the prepared direct artifact in 1.3; application/package selection activates it in 3.2; omit projection pins/loaders and old-format support. |
| R7 | [src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:28): `ClassificationResult` 28–41; `_similarity` 44–55; `_ordered_anchor_overlap` 58–63; `_composed_id` 66–68; `Classifier.__init__` 74–82; `classify` 84–208; `_result` 229–255 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py`: port source partitioning, runtime candidate comparison, exact typed matching and layered result mechanics. Adapt to recovered diagnostics and N1 outcomes; remove dual lead lookup at 89. The old `classify_block` 210–227 is not ported: recovery is explicitly composed by the processor and learner evidence collector. |

New package initializers are inert. R1/R7 supply the source behavior for the
current domain interfaces in N1; the final deletion/import lists define their
application integration.

### 3.2 Concrete offline-tool edits within this project

These are dependency and obsolete-tool removal edits, not a learner rebuild.
The algorithm remains in
[tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:916) 916–1099 and
the evidence registry in
[tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:44).
A later learner relocation/reorganization under `src/` is separate work.

| ID | Exact existing file/function/call | Required edit and reason |
|---|---|---|
| L1 | [tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35): import 35; `block_message` type annotation at 719; `collect_records` 1102–1159, lexer call 1108 | Reconnect to new `pipeline.domain.Emission` / `pipeline.emissions.iter_emissions`, adapting the precise field accesses if N1 requires it. The old lexer module is retired in 3.2. This is an offline consumer of the lexer, not a production call to the learner. |
| L2 | Same file: `LayeredClusterMatch` 309–333; evaluator-only `template_fixed_semantics_are_ordered` 806–844; unused `constant_tokens` 912–913; evaluator helpers 1162–1323; `evaluate_frozen_oracle` 1326–1482 | Remove code belonging to the obsolete tools listed in 6.2. The learning call chain `cluster_source_records -> derive_template -> choose_medoid/matching_pairs/infer_slot` uses the separate helpers at 916–1099 and continues in its existing file. |
| L3 | Same file: `write_report` 1533–1571; `parse_args` 1574–1599; `main` 1602–1682, oracle call 1630 | Remove mandatory oracle execution/arguments and its report/model evaluation fields so deleting the old tool chain does not break ordinary offline authoring. |
| L4 | [tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:366): `build_revision` 366–473, oracle call 390/evaluation field 433; `parse_args` 500–526, option 520; `main` 529–540, forwarding 536 | Remove this same mandatory oracle dependency. Keep selected-evidence clustering/provenance and immutable candidate production. |
| L5 | [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md:1); [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md:1) | Update the concrete remaining tool inventory and commands, including the old instruction to produce evaluator-style assignment counts in AGENTS.md 15–16. |

Production uses an already approved artifact. The current structural candidate
format and a complete approved direct-contract artifact are different product
units (owner intent 97–98; architecture 206–211). This project supplies the
current direct artifact in section 7; it does not rebuild automatic learner
promotion or claim that a future candidate can be loaded without review.

Future candidate promotion must reconcile normalization version, structure and
the approved direct-contract fields. That producer/consumer interface remains
explicit; a new learner algorithm, unified normalization rewrite, source-folder
relocation or training campaign is not a prerequisite for constructing the
production pipeline from the existing selected structures.

### 3.3 Capture and fast-follow grammar — Mini-project 2.2

| ID | Existing source and exact scope | New destination and port treatment |
|---|---|---|
| C1 | [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:37): capture exceptions 37–50; `PendingFileStat` 112–118; `PendingCapture` 121–129; `_make_inheriting_staging_directory` 148–164; `discover_logs` 167–176; `spool_logs` 179–342; `_copy_exact` 475–481; `_copy_stable_without_hash` 484–496 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/capture.py`: port copy-only behavior and the exact helper/type closure. Keep current capture metadata and watcher abort callback; required error.log precedes optional associated crash evidence. No database/model/learner imports. Port the relevant constants for current error-log/capture metadata, not `LEGACY_LOG_NAMES`. |
| C2 | Same [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:364): `FileIdentity` 53–57; `hash_file` 364–370; `_stable_identity` 402–412; `read_capture_metadata` 552–556; `_manifest_bytes` 569–572; `_load_manifest` 602–611; `selected_pending_path` 920–937 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py`: port hashing, explicit path selection and JSON read/serialization primitives. Write current input inspection/protection interfaces under N3. Do not port `_inspect_pending` 940–1058, `finalize_pending` 1067–1150, `read_snapshot` 881–906 or their old-format/result machinery. |
| F1 | [src/ck3chronicle/runtime_context.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:25): `MountedDlc` 25–32; `MountedMod` 35–43; inventory/mount regex 73–91; path/key helpers 94–136; `_BlockCandidate` 139–181; `_ContextAnalysis` 184–202; `_typed_mounts` 205–271; `_analyze_debug_context` 274–453 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/playset.py`: port this pure extraction kernel as `analyze_debug_context`, with its types/constants. Do not port `parse_debug_context` 456–481: it is an old compatibility wrapper over the analyzer. No repository import, stored-result reconstruction or context reparse service. This preserves the approved same-Run playset fast-follow's working grammar; it is not added to `process_input` in this recovery. |

Current manifest/input validation rules are evidence for N3, not a reason to
copy old branches. In particular, no inferred `legacy_pending` metadata,
version-1/2 manifest reader, archive adoption, broad finalization, fallback
file set, deletion of a duplicate protected copy, or early session registration
is ported. Retained native logs can be selected explicitly for replay without
interpreting an old manifest or database.

## 4. New composition and changed storage responsibilities

Some required mechanics already work and have explicit ports in section 3.
The new function bodies below serve different input/output boundaries from the
old services. Their file names alone do not establish that all underlying
algorithms need rewriting.

| Existing implementation and exact evidence | Why the existing body is not the target composition | Destination |
|---|---|---|
| [src/ck3chronicle/parser/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:230): extractor call 230, unclassified fallback 239, old normalization 251, preliminary writer 264 | It assigns regex issue types and persists old source/issue rows before approved-contract classification. Lexer mechanics are ported separately as R1. | N2/N7 recover transient diagnostics and classify them before storage. |
| [src/ck3chronicle/classification/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:161): stored-block load 161–168, classifier call 197, assignment writer 286–295 | It reads database source rows and writes a second assignment/payload store; it does not consume the target transient diagnostic stream. Matching mechanics are R7. | N7 composes direct classification; N6 writes final Run records. |
| [src/ck3chronicle/processing.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:888): context 888, parser 903, classifier 929, projection 946 | Its flow composes the old stages and historical-currentness branches. | N7 composes the target flow and fresh-generation replay. |
| [src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1286): staged writers 1286–1543, 1763–2046 and 2531–2837; [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:244) | The old tables/writers encode intermediate raw blocks, classifier payloads, projection lineage and replacement issues. | N4/N6 implement compact contract-defined aggregates and successful-Run storage. |
| [src/ck3chronicle/reporting.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:99): projection required at 99–110, classifier payload query 124–133 | Required report behavior exists, but these queries require representations being removed. | N8 writes the queries for final compact records/stored rendering. |
| [src/ck3chronicle/database_audit.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:80): `audit_database` 80–861 | Checks the old schema/projection/issue/raw-log representation. | N8 implements the corresponding current-database facts. |
| Native review shard in architecture 176–191 | No current writer implements this target storage product. Old classifier payloads and unknown IssueDrafts are not native shards. | N5 is new functionality. |

The proposed interfaces below name the new composition and representation work.
Their source mechanics, where available, are the identified ports.

| ID | New file and proposed functions/types | Work to write; existing behavior reference |
|---|---|---|
| N1 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/domain.py`: `Emission`, `RecoveredDiagnostic`, `ClassificationOutcome`, `DiagnosticRecord`, `RunResult`; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py`: `ErrorContract`; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/model.py`: direct-format field reader | Define transient original spans/values, the structural outcomes established in 1.3, direct error type, rendering and contract-defined identity. Carry established definitions into one model artifact. Old `ModelCluster` 38–52 lacks these fields; old issue/category models are not port inputs. Missing or changed rules get focused review, not invented defaults or blanket reapproval. |
| N2 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/diagnostics.py`: `recover_diagnostics`; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py`: `bind_original_values`; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py`: `normalize_for_match` | Compose R2–R5 around original child spans. Extract values before masking; retain token-to-original binding sufficient for typed slots/rendering/identity. No second classifier or post-assignment rematch. R3's old strings and projection `_template_alignment` 287–343/`_reference_values` 384–472 do not implement this interface. |
| N3 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py`: `PreparedInput`, `prepare_pending_input`, `prepare_manual_input`, `prepare_retained_input`, `protect_input` | Explicit pending selection or explicit native-log selection; current input facts, stable complete hash, durable original protection and truthful unavailable metadata. Reuse C1/C2 primitives. Old `ingest` 35–121, harvester inspection/finalization and archive registration are not ported. Current-format checking has one supported representation and no failed-format fallback. |
| N4 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/aggregation.py`: `diagnostic_identity`, `add_classified_diagnostic`, `finish_records` | Aggregate exact contract-defined identity with original retained values/locators and occurrence counts. Keep emitted-diagnostic and source-emission counts distinct. No regex signature/category or grouping solely by contract ID. |
| N5 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/review.py`: `ReviewShardWriter`, `append_review_emission`, `finish_review_shard` | Write native bytes in original emission order/frequency, once per mixed emission, with child reasons/provenance in associated metadata. One Run shard, including empty, under the generation's review namespace. Produce hash/count/reference/availability metadata for SQLite; no duplicate unresolved payload table. |
| N6 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/schema.py`: current DDL; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/repository.py`: `create_generation`, `open_generation`, `open_generation_readonly`, `find_run_by_log_hash`, `write_run`, `get_run`, `latest_run`, `list_runs`, `read_diagnostics`, `read_review_metadata` | Build current-generation SQLite tables and strict opens; unique full-log hash, successful Run facts, compact records, stored rendering/contract lineage and native-review metadata. No code port from [src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:68) 68–2896 or [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:1) 1–550. Duplicate rejection behavior at repository 168–181 is a requirement reference, not old SQL to copy. |
| N7 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/processor.py`: `process_input`; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/replay.py`: `rebuild_generation` | Compose N3 -> duplicate guard -> R1/N2 -> R7 -> N4/N5 -> N6. Every recognized emission is accounted for; failures are explicit. Pending/manual/replay call this one processor. Replay takes an explicit retained-input set and a fresh generation, never old database rows or in-place reclassification. |
| N8 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/reports.py`: `build_run_report`, `list_errors`, `get_review_reference`; `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/audit.py`: `audit_database` | New read queries and presentation against N6 records/metadata. Old [src/ck3chronicle/reporting.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:81) `build_session_report` 81–411 and [src/ck3chronicle/database_audit.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:80) `audit_database` 80–861 are removal references; neither body is ported. Reports need neither original logs nor installed model files. |
| N9 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/commands.py`: `register_commands`, `cmd_ingest`, `cmd_process_pending`, `cmd_rebuild_db`, `cmd_runs`, `cmd_report`, `cmd_latest`, `cmd_errors`, `cmd_review_queue`, `cmd_audit_db`, `capture_error` | Implement current handlers/output against N3/N7/N8 and the neutral command envelope. Register supported commands in the existing application CLI. Registration and capture-error handling stay lightweight; they do not load a model or open SQLite. No old command-handler body is used as the new pipeline controller. Exact disconnections are in section 6.1. |

`process_input` is the only Run-composition function. It obtains a prospective
Run identity as part of processing, streams complete emissions through
diagnostic recovery/classification, aggregates classified diagnostics and routes
native review evidence, then completes the Run's records/metadata. No preliminary
regex issue writes, stored-source reread, separately persisted classifier
payloads/assignments or semantic projection stage exists in this call flow.

The connection between the native shard and SQLite completion must expose a
complete accepted Run or the prior accepted state. Use ordinary filesystem and
SQLite behavior. A processing journal, reservation/reuse scheme or publication
state machine is not prescribed or justified by the old implementation.
Mini-project 2.1 makes the concrete cross-resource behavior reviewable; Stage 2
presents it before application activation.

## 5. Three stages and seven ordered mini-projects

| Stage / coordinator | Mini-projects | Stage deliverable |
|---|---|---|
| [Stage 1 — Classification core](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md) | 1.1 -> 1.2 -> 1.3 | Direct contract interfaces, original-value recovery and artifact-backed runtime classification. |
| [Stage 2 — Run processing](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_2_RUN_PROCESSING_ORCHESTRATOR_PROMPT.md) | 2.1 -> 2.2 | One complete protected-input processor, compact storage, native review and fresh-generation replay. |
| [Stage 3 — Application switch](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_3_APPLICATION_SWITCH_ORCHESTRATOR_PROMPT.md) | 3.1 -> 3.2 | Stored reports/commands connected; superseded application paths, providers, tools and artifacts removed. |

| Mini-project prompt | Work assigned | Concrete deliverable |
|---|---|---|
| [1.1 — Define direct contracts and record interfaces](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_1_DEFINE_DIRECT_CONTRACTS_PROMPT.md) | N1 direct contract/record interfaces and cited definition gaps | Concrete types and a field-authority handoff; exact missing rules identified before they govern records. |
| [1.2 — Port emission recovery and original-value binding](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_2_PORT_EMISSION_RECOVERY_PROMPT.md) | R1–R4 / N2 emission recognition, splitting, normalization and bindings | Original-byte emissions and typed matching views with child/value provenance. |
| [1.3 — Build runtime classification and the direct model](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_3_BUILD_RUNTIME_CLASSIFIER_PROMPT.md) | R5–R7 / N1 direct model reader and classifier | One direct immutable artifact and runtime classifier; new package selection prepared. |
| [2.1 — Build aggregation, Run storage and native review](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/2_1_BUILD_RUN_STORAGE_AND_REVIEW_PROMPT.md) | N4–N6 aggregation, native review and current SQLite | Compact approved records, complete Run persistence and one native shard. |
| [2.2 — Compose protected inputs, processing and replay](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/2_2_COMPOSE_INPUT_PROCESSING_AND_REPLAY_PROMPT.md) | C1/C2/F1 / N3/N7 protected input and common processing | Pending/manual/replay reach one processor; pure playset grammar port remains separate from Run processing. |
| [3.1 — Build stored reports, audit and command handlers](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/3_1_BUILD_REPORTS_AND_COMMANDS_PROMPT.md) | N8/N9 stored reads and new handlers | Reports, audit and explicit commands ready for application integration. |
| [3.2 — Switch application callers and retire the old pipeline](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/3_2_SWITCH_AND_RETIRE_OLD_PIPELINE_PROMPT.md) | L1–L5, application/resource connections and complete retirement | One application path, bounded offline reconnection, obsolete source/artifact deletion and current documentation. |

These are construction handoffs within one replacement project. Application
activation and provider retirement occur together in 3.2; preceding mini-projects
do not claim a switched production application. No intermediate adapter or
parallel production command is required to make a construction handoff usable.

Each mini-project supplies the scope proof in 2.3. Coordinators sequence the
named prompts and compare their interfaces; they have no extra mutation scope.
A required correction returns to its named mini-project and file scope, with a
new entry baseline, before the dependent work continues.

Two focused implementation review points protect downstream decisions:

1. In 1.1, show the actual direct types and per-field source/definition inventory.
   Ask for a ruling only on a concrete missing or changed contract rule before
   it is used; established definitions retain their approval.
2. At Stage 2 completion, present the implemented record/shard layout, mixed
   emission accounting and SQLite/filesystem completion behavior, plus proposed
   explicit command inputs for 3.1. The owner reviews any still-open product
   choice before the final application switch. Already accepted choices are
   carried forward without repeated approval.

Product verification is separately specified under 8.1; these review points
do not introduce test/evaluator packages. Model/effort defaults and the launch
index are in the master prompt.

## 6. Final application connections and retirement

### 6.1 Exact application edges — Mini-project 3.2

The existing console remains [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:24) 24–25,
`ck3chronicle.cli:main`; `cli.main` is 2754–2757. New command implementations
live in `pipeline/commands.py`. The changes below switch the precise existing caller and registration sites
to the new handlers.

| Existing edge / exact range | Final connection or deletion |
|---|---|
| [src/ck3chronicle/watcher.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:17) import 17–20; `watch_sessions` 468–625 | Change only the `InvalidCaptureInput`/`UnstableCapture` import to `pipeline.capture`. Keep lifecycle observation and callback behavior. |
| [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:22) `_spool_once` 22–39, import 30, call 33; `cmd_capture` 142–165; `cmd_watch` 168–527 | Switch the capture import to the ported `pipeline.capture.spool_logs`. Existing callback argument/result shape is supported by the actual port, not an old-provider adapter. |
| Same CLI `_capture_error` 74–99; callers at 137, 163, 225, 526 and 543 | Remove the old DB/capture mixed error helper; connect those remaining capture callers to the new `pipeline.commands.capture_error`. The old ingest and reconcile callers disappear with their handlers. |
| Same CLI `build_parser` 2395–2751 | Call new `pipeline.commands.register_commands` for pipeline surfaces. Keep capture 2406–2411, watch 2423–2444, doctor 2458–2459 and observe-logging 2473–2481 registrations. |
| ingest registration 2413–2421; handlers `cmd_ingest` 132–139, `_capture_once` 11–19, `_print_capture_result` 50–71 | Delete old handlers/registration; new `cmd_ingest` accepts an explicit current manual/recovery input and calls the canonical processor. |
| sessions registration 2453–2455; `cmd_sessions` 555–585 | Delete; new `runs` registration/handler lists current Runs. No `sessions` compatibility alias. |
| audit-db 2461–2471; `cmd_audit_db` 595–640 | Replace the registration with the new handler; delete old output/old-table/deep-distribution options. |
| review-queue 2519–2538; `cmd_review_queue` 861–942 | New handler shows Run review metadata/native shard reference. Delete payload queue and model/session-stage arguments. |
| report 2540–2565; latest 2567–2579; errors 2581–2600; old helpers/handlers 945–1231 | Delete those old bodies, including `session_intelligence` import at 1052; register new N8/N9 consumers. Use Run identity; remove `--session`, `--since`, projection/category/payload coupling. |
| process-pending 2602–2623; `cmd_process_one_pending` 1499–1614; helpers 1420–1496 | Delete old plan/journal/projection wrappers; register new explicitly selected pending-input handler. |
| reconcile 2446–2450 / handler 530–552; parse 2484–2500 / handler 682–721; classify 2502–2517 / handler 724–858; backfill-session 2625–2641 / handler 1617–1723 | Delete historical registration, repair/reparse/reclassify/backfill routes completely. |
| compare 2643–2668; baseline and nested commands 2670–2692; ignore and nested commands 2694–2717; handlers/helpers 1726–2126 | Delete unsupported comparison/baseline/ignore chain completely. |
| context 2719–2730 / handler 2129–2243; resolve-file 2732–2739 / handler 2246–2297; triage 2741–2749 / handler 2300–2392 | Delete old context-reparse and provisional source/triage commands. F1's pure grammar has its explicit new destination; no replacement feature commands. |
| Unregistered `_cmd_process_pending_wide_legacy` 1234–1417; `_log_type_from_relpath` 668–679 | Delete; no destination. |
| Proposed `rebuild-db` (new registration) | Explicit retained inputs and named fresh generation -> `pipeline.replay.rebuild_generation` -> `pipeline.processor.process_input`. No old DB reader or implicit active-DB replacement. |
| [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:12) import branch 12–15 | Remove the unreachable old-Python import fallback; Python >=3.11 is already required. This is a specific final cleanup, not a configuration rewrite. |

Neutral configuration functions remain callable at
[src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:38): `default_config_path` 38–40,
`load_config` 43–59, `_configured_path` 62–77,
`require_strict_descendant` 80–102 and `validate_project_containment` 105–140.
Preserve [src/ck3chronicle/command_envelope.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/command_envelope.py:1) 1–51.
The required new input/generation arguments are explicit; do not hide an old
schema reader behind configuration defaults.

### 6.2 Obsolete offline tools retired in mini-project 3.2

- [tools/template_learning/analyze_script_system_layers.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/analyze_script_system_layers.py:1) — entire file, 1–131.
- [tools/template_learning/blind_review/build_blind_stratified_sample.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:1) — entire file, 1–336.
- [tools/template_learning/blind_review/compare_blind_adjudication.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/compare_blind_adjudication.py:1) — entire file, 1–279.
- [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:1) — entire file, 1–376.
- [tools/template_learning/build_review_pack.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:1) — entire file, 1–446.
- [tools/template_learning/build_semantic_projection_catalog.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:1) — entire file, 1–1268.
- [tools/template_learning/evaluate_unseen_session.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:1) — entire file, 1–408.
- [tools/template_learning/mine_symbol_suffixes.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:1) — entire file, 1–273.

The two existing learner/registry files and their guides receive only the edits
in 3.2. The separately scoped ordinary evaluator is listed in 8.1.

### 6.3 Old product implementation retired in Mini-project 3.2

The following entire files are deleted after their explicit ports, new
replacements and caller changes are connected. This includes old providers
from which useful functions were lifted; none is left as a partial legacy file.

- [src/ck3chronicle/classification/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/__init__.py:1) — entire file, 1–26.
- [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:1) — entire file, 1–82.
- [src/ck3chronicle/classification/contracts.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:1) — entire file, 1–146.
- [src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:1) — entire file, 1–255.
- [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:1) — entire file, 1–191.
- [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:1) — entire file, 1–768.
- [src/ck3chronicle/classification/projection_catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/projection_catalog.py:1) — entire file, 1–508.
- [src/ck3chronicle/classification/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:1) — entire file, 1–312.
- [src/ck3chronicle/db/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/__init__.py:1) — entire file, 1–1.
- [src/ck3chronicle/db/migrations.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:1) — entire file, 1–919.
- [src/ck3chronicle/db/payloads.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/payloads.py:1) — entire file, 1–35.
- [src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1) — entire file, 1–2896.
- [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:1) — entire file, 1–550.
- [src/ck3chronicle/models/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/__init__.py:1) — entire file, 1–1.
- [src/ck3chronicle/models/issue.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/issue.py:1) — entire file, 1–131.
- [src/ck3chronicle/models/parse.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/parse.py:1) — entire file, 1–65.
- [src/ck3chronicle/parser/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/__init__.py:1) — entire file, 1–1.
- [src/ck3chronicle/parser/extractors/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:1) — entire file, 1–121.
- [src/ck3chronicle/parser/extractors/asset_graphics.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/asset_graphics.py:1) — entire file, 1–35.
- [src/ck3chronicle/parser/extractors/culture_faith.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/culture_faith.py:1) — entire file, 1–34.
- [src/ck3chronicle/parser/extractors/database_reference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/database_reference.py:1) — entire file, 1–38.
- [src/ck3chronicle/parser/extractors/debug_log.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/debug_log.py:1) — entire file, 1–122.
- [src/ck3chronicle/parser/extractors/descriptor.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/descriptor.py:1) — entire file, 1–31.
- [src/ck3chronicle/parser/extractors/event_system.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/event_system.py:1) — entire file, 1–37.
- [src/ck3chronicle/parser/extractors/gui_interface.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/gui_interface.py:1) — entire file, 1–34.
- [src/ck3chronicle/parser/extractors/history_setup.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/history_setup.py:1) — entire file, 1–31.
- [src/ck3chronicle/parser/extractors/localization.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/localization.py:1) — entire file, 1–49.
- [src/ck3chronicle/parser/extractors/persistent_reader.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/persistent_reader.py:1) — entire file, 1–36.
- [src/ck3chronicle/parser/extractors/script_hygiene.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_hygiene.py:1) — entire file, 1–36.
- [src/ck3chronicle/parser/extractors/script_system.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_system.py:1) — entire file, 1–105.
- [src/ck3chronicle/parser/extractors/unclassified.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/unclassified.py:1) — entire file, 1–36.
- [src/ck3chronicle/parser/log_blocks.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:1) — entire file, 1–257.
- [src/ck3chronicle/parser/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/normalize.py:1) — entire file, 1–99.
- [src/ck3chronicle/parser/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:1) — entire file, 1–410.
- [src/ck3chronicle/archive_registry.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:1) — entire file, 1–307.
- [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:1) — entire file, 1–1389.
- [src/ck3chronicle/ingest.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:1) — entire file, 1–121.
- [src/ck3chronicle/processing.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:1) — entire file, 1–1086.
- [src/ck3chronicle/reporting.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:1) — entire file, 1–411.
- [src/ck3chronicle/database_audit.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:1) — entire file, 1–895.
- [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:1) — entire file, 1–620.
- [src/ck3chronicle/semantic_projection_service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:1) — entire file, 1–465.
- [src/ck3chronicle/runtime_context.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:1) — entire file, 1–668.
- [src/ck3chronicle/session_intelligence.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:1) — entire file, 1–937.
- [src/ck3chronicle/source_resolution.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:1) — entire file, 1–534.
- [src/ck3chronicle/triage.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:1) — entire file, 1–191.
- [tools/migrate_legacy_pending_metadata.ps1](C:/Users/nateb/Documents/ck3chronicle/tools/migrate_legacy_pending_metadata.ps1:1) — entire file, 1–236.

All 21 old DDL tables are replaced by N6's current representation or removed
with their unsupported features; the exact table/caller inventory is in
CALLER_INDEX.md. In particular, there are no permanent `raw_block_contents`,
`source_blocks`, classifier payload/assignment tables, projection lineage,
old issue/occurrence stores, migration chain, baseline/ignore/source-context
tables or placeholder playset tables. Needed Run/contract/record facts are
written into the new schema directly.

No code moves to an archive/legacy folder. No old data is migrated or rewritten.
No original log, review evidence, learner evidence/cache or database is deleted
by this source retirement.

## 7. Approved model artifact and selection

The reference index may still be called a **model**: it stores the supported
templates/contracts against which runtime classification operates. This
implementation project is construction of a new pipeline, not necessarily
learning a new set of error templates.

Existing learned structures and established approved definitions are inputs
to the current direct-contract revision. They keep their approval. The format
and selected revision change because the runtime no longer uses a
projection-bound pair of artifacts. That does not require blanket retraining
or general contract-candidate review.

Exact current artifact inputs and final active-tree removals:

- [models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1) — 1–1.
- [models/67303093ecda779d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/manifest.json:1) — 1–1.
- [models/67303093ecda779d/semantic_projection_catalog.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/semantic_projection_catalog.json:1) — 1–14082.
- [models/93196794a7e0115d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/93196794a7e0115d/empirical_template_model.json:1) — 1–1.
- [models/93196794a7e0115d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/93196794a7e0115d/manifest.json:1) — 1–1.

New paths are exactly
`C:/Users/nateb/Documents/ck3chronicle/models/<new_revision>/empirical_template_model.json` and
`C:/Users/nateb/Documents/ck3chronicle/models/<new_revision>/manifest.json`.
The revision is content-derived and cannot be named until that content exists.
No semantic-projection catalog is emitted.

Mini-project 1.3 prepares the direct content, loader, catalog pin and shared
normalizer identity. Mini-project 3.2 connects the application and switches
[pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) package data 29–34,
activating that prepared unit together. Remove the five superseded active
artifact files named above in the same change. Existing Git history is sufficient;
no old immutable artifact is edited in place or shipped as a partial revision.

Do not copy the projection catalog wholesale into “contracts.” Use only
independently established type/slot/identity/rendering definitions; projection
references, category mappings and sample-absence defaults are not runtime
contract authority. If a necessary definition is actually missing or changes,
identify its precise entry and proposed rule for focused owner review before
dependent implementation relies on it.

Runtime model normalization/index features may need regeneration for corrected tokenization
or splitting. Neither keeping exactly 891 clusters nor retraining everything
is required. Do not add a runtime old-model converter, automatic learner run,
approval-reset mechanism or preservation/export project.

## 8. Remaining scope and documentation

### 8.1 Known consumers deferred to the separate verification task

- [tools/evaluate_classifier.py](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:18): `evaluate` 18–62, runtime
  `classify_block` call at 30, `main` 65–89. This ordinary coverage utility
  is distinct from the removed frozen tools. Its current imports/API will be
  affected by the new kernel; its disposition belongs to verification design.
- [tests/test_processing_recovery_requirements.py](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:1) 1–390;
  [tests/test_watcher_capture_requirements.py](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:1) 1–207;
  [.github/workflows/ci.yml](C:/Users/nateb/Documents/ck3chronicle/.github/workflows/ci.yml:1): known import/schema/command consumers.
- [docs/REQUIREMENTS_AND_TESTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/REQUIREMENTS_AND_TESTING.md:20) 20–124;
  [docs/RELEASE_READINESS.md](C:/Users/nateb/Documents/ck3chronicle/docs/RELEASE_READINESS.md:17) 17–103; verification portions of
  Trusted Run beginning at 425 and the model-quality document.

Their disposition must be supplied by the separately commissioned verification
design after the complete workplan/master/package prompts are approved and
before implementation is treated as complete. This plan does not design,
run or prescribe tests/evaluators/acceptance/performance checks. It does not
authorize leaving broken consumers silently, nor preserving old APIs for them.
No verification claim is made for an implementation that does not yet exist.

### 8.2 Surrounding product boundaries

Keep [src/ck3chronicle/watcher.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:468) `watch_sessions` 468–625 and
[src/ck3chronicle/logging_observer.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/logging_observer.py:1) 1–187 behavior, with only the
watcher's import switch specified in 6.1.
[src/ck3chronicle/doctor.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/doctor.py:1) 1–61 has an independent write-probe gap;
its redesign is not commissioned here.

F1 ports working inventory/Mounted Data parsing for the approved same-Run
debug-log playset fast-follow. Capture/storage integration for that fast-follow
is later work. Comparison, source context, triage, pruning/retention features
and a general configuration/bootstrap redesign are also outside this recovery.
Original protected logs remain retained indefinitely.

### 8.3 Eventual documentation edits, not edits authorized now

| File / current locations | Treatment |
|---|---|
| [models/README.md](C:/Users/nateb/Documents/ck3chronicle/models/README.md:7), 7–54; [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29), 29–34 | Current selected artifact/packaging; remove projection and superseded active revision instructions. |
| [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253), 253–310, 332–382, 412–423 | Align implementation/identity/storage/retention descriptions with current owner intent and the new pipeline package and flow. Old one-week source expiry and migration prescriptions are superseded. Verification sections beginning at 425 remain assigned to the separate verification-design task. |
| [docs/DATA_COMPATIBILITY_AND_OPERATIONS.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATA_COMPATIBILITY_AND_OPERATIONS.md:12), 12–38, 69–82, 125–218, 220–334 | Reconcile supported command/storage/retention/operation descriptions; remove compatibility/migration prescriptions. Do not derive new release or verification conditions from old text. |
| [docs/MODEL_QUALITY_AND_PROMOTION.md](C:/Users/nateb/Documents/ck3chronicle/docs/MODEL_QUALITY_AND_PROMOTION.md:137), 137–147 | Replace historical in-place reclassification/source-expiry operational claims with fresh-generation behavior. Its measurement/promotion-verification design is outside this workplan. |
| [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md:48), active-exercise section 48–63; [docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md:71), runtime/gap sections starting at 71 | Record the actual implementation status when it exists. Do not propagate historical approval claims, measurements or deleted prompt routes as authority. |
| [docs/REPOSITORY_AND_BACKUP.md](C:/Users/nateb/Documents/ck3chronicle/docs/REPOSITORY_AND_BACKUP.md:17), ownership sections starting 17/29; [docs/WORKSPACE_ROUTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/WORKSPACE_ROUTING.md:1) | Update actual source ownership where it changes; no new archive/backup project. |
| [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md); [README.md](C:/Users/nateb/Documents/ck3chronicle/README.md); [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md); [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md) | These already direct the current architecture/planning. Change only actual implemented command/owner/continuation facts. Do not apply stale recovery-review line edits or mark implementation completed early. |
| [docs/BANNED_IDEAS.md](C:/Users/nateb/Documents/ck3chronicle/docs/BANNED_IDEAS.md); [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md) | Authority inputs; no policy rewrite required by this implementation. |
| [docs/DEVELOPMENT_RESTART_AUDIT_2026-09-08.md](C:/Users/nateb/Documents/ck3chronicle/docs/DEVELOPMENT_RESTART_AUDIT_2026-09-08.md); [docs/DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md) | Historical/background inputs; no implementation change required. The deleted operational recovery plan and rejected earlier prompts stay deleted/unread. |


In particular, the root AGENTS/README and workspace-routing source locations
must point to the new production pipeline package; the learner remains in its
existing separate tool files. The existing learner location remains accurate; its tool inventory is updated
as described in 3.2. Existing governing decisions and pre-existing
edits are preserved; actual implementation status is recorded only when true.

## 9. Expanded prompt index and delivery status

Start with [the master orchestrator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md).
It links all three stage coordinators and all seven complete mini-project
prompts, with a suggested model and effort for each.

The prompts now contain the steps, source functions/ranges, explicit mutation
lists, handoff requirements and deliverables for implementation. Any unresolved
direct-contract definition, mixed-emission storage detail or operator-facing
argument remains visible at its named review point; it is not treated as an
existing product capability.

Current work is confined to the planning files in this directory. Product
implementation, runtime operations and the separately commissioned verification
design have not been executed.
