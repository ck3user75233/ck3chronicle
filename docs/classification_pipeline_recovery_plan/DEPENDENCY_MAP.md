# Classification recovery: dependency map and proposed disposition

Status: completed source map, 2026-09-13. The owner has endorsed rebuilding the
production pipeline in a new source package and requested a workplan plus
expanded prompts. Learner reconstruction is outside this production project. [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md)
now owns the proposed steps, exact current function ranges and deliverables.
The detailed workplan and prompt scope remain under review; implementation is
not authorized by this map.

The map covers the current working tree, including its pre-existing edits.
No product code, existing documentation, tests, runtime evidence, or database
was changed in preparing it. No processing, watcher, evaluator, or test was run.
The companion [CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md)
records internal imports, imported call sites, all 21 current DDL tables and
their source references, and CLI registrations across all 66 Python files in
`src/`, `tools/`, and `tests/`. The analysis below adds same-module calls,
receiver calls, transaction boundaries, file formats, package resources, and
the distinction between live, unregistered, and provisional consumers.

## 1. Authority and settled scope

The current owner instructions, [OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md)
and [BANNED_IDEAS.md](C:/Users/nateb/Documents/ck3chronicle/docs/BANNED_IDEAS.md)
govern. The [recovery review](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md)
is technical input. Its historical approval language, code-preservation
arguments, and old verification prescriptions do not establish requirements.

The owner has settled removal of semantic projection, the regex taxonomy,
fallbacks, compatibility paths, migrations, and historical reclassification.
An existing caller is a dependency to resolve, not a reason to keep its old
provider. Required behavior moves into its canonical owner; an unsupported
consumer may be removed. No projection wrapper, alternate taxonomy,
old-schema reader, old-format fallback, dual write, or compatibility alias is
part of the recommendation.

“Classification meaning” is prose in the product intent, not an additional
field, taxonomy, model, or pipeline stage. Here its concrete contents are the
contract's hierarchical `error_type`, typed slots, permitted outcomes,
rendering, and diagnostic identity. No separate entity with that name is
proposed. There is one error-type hierarchy; the old `category` axis disappears.

Planning correction after the owner's question, 2026-09-13: existing approved definitions do not become
unapproved candidates because their storage or owning code changes. This map
has not identified a contract-approval backlog. Review of an actual addition,
unresolved field or changed classification rule is distinct from repackaging
existing definitions and selecting a new immutable artifact revision. The
earlier proposal for a general contract-candidate review was too broad.

This remains planning only under the [replan prompt](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md).
Verification design is a separate task. References to typed validation below
describe runtime classification behavior, not a proposed verification program.

## 2. Existing implementation inventory — removal evidence only

The target runtime pipeline and classification/shard definitions are in
[WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md) 1.1–1.5. The inventory below identifies
current providers and callers; it does not propose another pipeline.
The new production destination is `src/ck3chronicle/pipeline/`. The learner
remains in its current tools files, with the precise consumer/tool-removal edits
in WORKPLAN 3.2. The production processor does not invoke the learner.

The two previously compressed descriptions mean these exact existing operations:

| Existing operation | Exact source | Intended disposition |
|---|---|---|
| Production classifier computes a result in memory | [classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:84): `Classifier.classify` 84–208; current block wrapper 210–227 | Port the named runtime matching mechanics to `pipeline/classifier.py` under WORKPLAN R7. No learner or database write runs inside this classifier. |
| The old service stores that result in intermediate assignment/payload tables | [classification/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:197): runtime classifier call at 197–200, prepared assignments at 208 onward, `repository.replace_classification_run` call at 286–295; repository implementation 1763–2046 | Write `pipeline/processor.py` and `pipeline/repository.py` from scratch under N6/N7, then delete the old service/storage files. The classifier itself is not the writer of those tables. |
| The old projection service changes the selected session's stored issue rows | [semantic_projection_service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:432): repository call at 432–444; [db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:2598): `delete_previous` 2598–2606 deletes that session's projection lineage, `issue_occurrences` and `issues`; projection lineage/writes follow at 2615–2734 | Delete this service, repository transaction and old tables. “Replaced issues” described these deletes and inserts; it did not refer to the target pipeline, learner or a desired record format. |

Archive registration, parser storage, intermediate classifier storage and
projection currently commit separately. Manual ingest also invokes archive
reconciliation and stops after registration. These facts identify old
interfaces to remove, not target responsibilities to preserve.

### 2.1 Entry points, capture, and orchestration

| ID | Current owner and exact surface | Dependencies and effect |
|---|---|---|
| C01 | [cli.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:11) `_capture_once`; `cmd_ingest:132` | Calls `ingest()` and returns archive/registration results. This is the older manual route, despite the helper name. |
| C02 | [cli.py:22](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:22) `_spool_once`; `cmd_capture:142`, `cmd_watch:168` | Calls `harvester.spool_logs`; watcher callback protects evidence without opening SQLite or importing the classifier. |
| C03 | [watcher.py:468](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:468) `watch_sessions` | Owns lifecycle observation and invokes the capture callback. No projection, issue-model, or classification-storage dependency. Its existing operating controls do not automatically justify processor controls. |
| C04 | [harvester.py:179](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:179) `spool_logs`; `inspect_pending:1061`, `finalize_pending:1067` | Owns pending bytes, source metadata and archive publication. The public selected processor uses these functions. Actual copy mechanics are independently useful. |
| C05 | [harvester.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:15) legacy file lists and manifest versions; `_manifest_payload:499`, `_principal_names:546`, `_manifest_identity:663`, `_inspect_pending:940` | Supports manifest versions 1, 2 and 3. Manual snapshot writes version 1; current capture writes version 3. Missing pending metadata produces synthetic `legacy_pending` metadata. Pending inspection accepts the old multi-log list. These are additional compatibility dependencies, not semantic-projection code. |
| C06 | [harvester.py:443](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:443) `build_bundle`; `snapshot:1272`; `adopt_legacy_archive:1174`, `_adopt_legacy_snapshot:1249`, `_publish_manifest_atomic:575` | Manual bundle construction invokes `discover_crash_folder:345`; snapshot may add a manifest to an old archive. Reconciliation calls `adopt_legacy_archive`. `finalize_pending_captures:1153` serves the rejected wide processing branch. |
| C07 | [ingest.py:35](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:35) `ingest` | Calls `reconcile_archives:51` before selecting/building its input; opens writable DB for deduplication, snapshots, registers an already-finalized session and commits metadata separately. Its “compatibility API” description is not authority; explicit manual/recovery input is an owner requirement. |
| C08 | [archive_registry.py:85](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:85) `register_archive`; `reconcile_archives:184` | Registration calls writable repository open and session registration. Reconciliation scans archives and sessions, validates existing representations, adopts legacy archives, repairs/registers old rows and metadata. `snapshot_manifest_projection` means an archive representation, not the banned semantic projection. |
| C09 | [processing.py:414](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:414) `plan_pending_capture`; `process_planned_pending_capture:499` | Selected plan uses a direct read-only SQLite connection, current old table queries and model/projection identity. Processing finalizes capture, commits archive registration, then calls `process_selected_sessions`. |
| C10 | [processing.py:698](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:698) `process_pending`; `process_selected_sessions:1064` | The selected wrapper disables broad finalization/reconciliation and latest reporting. The implementation still enumerates sessions before filtering and retains rejected wide branches. Calls runtime context at 888, parser at 903, classifier at 929, projection at 946; optional latest/report at 978/988. |
| C11 | [processing.py:593](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:593) `plan_selected_sessions`; plan/result dataclasses at 241–404 | Historical plans compare parser/classifier/projection currentness. Results carry separate parsed, classified, projected and runtime-context counts. The historical backfill command consumes this path. |
| C12 | [processing.py:46](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:46) `ProcessorLease`; `ProcessingJournal:96` | Current exact-pending and backfill CLI wrappers use these operational mechanisms. Their presence does not establish a new recovery or publication requirement; BAN-013 applies to preservation as well as expansion. |
| C13 | [config.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:12), [command_envelope.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/command_envelope.py:12) | Python `<3.11` import fallback is unreachable under package requirements. Several callers derive a fixed `ck3chronicle.db` path independently. A separately named candidate generation needs one explicit destination passed through retained entry points. Error/JSON envelope behavior is independent of projection. |

### 2.2 Emission, classification, and representation

| ID | Current owner and exact surface | Dependencies and effect |
|---|---|---|
| E01 | [parser/log_blocks.py:142](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:142) `iter_log_blocks`; `_parse_header:73`; `TimestampedLogBlock:27` | Recognizes three-bracket headers and continuations, tracks provenance and hashes. Also accepts fixture-only two-bracket headers through `_HEADER_RE_TWO:19` and supplies old-fixture field defaults. `raw_block` is decoded with replacement, so it is not an exact native-byte store. |
| E02 | [parser/service.py:83](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:83) `parse_session` | Reads archived `error.log`, supports reparse/currentness, starts parser replacement at 194, calls lexer at 205, extractor at 230, old normalizer at 251 and appends preliminary rows at 264; counts and commits at 331/345. Handles `IssueDraft` versus lists and terminal unclassified drafts. |
| E03 | [parser/extractors/__init__.py:43](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:43) registries; `extract_block:98`; `extract_block_for_log_type:111` | `extract_block` has one product caller, parser service. Registry invokes leaf `match`/`extract` functions in order. Debug/game/database dispatch and multi-log function are unsupported; the latter has no direct caller. |
| E04 | All extractor leaves: `asset_graphics`, `culture_faith`, `database_reference`, `debug_log`, `descriptor`, `event_system`, `gui_interface`, `history_setup`, `localization`, `persistent_reader`, `script_hygiene`, `script_system`, `unclassified` | All live under the preceding directory. `script_system._classify_error_type:57` defaults broad matches to `syntax_error`, and `extract:69` gives high confidence. `persistent_reader.extract:14` emits one unknown draft, not the required splitter. `unclassified.match:15` always succeeds. No leaf owns the new error-type hierarchy. |
| E05 | [parser/normalize.py:60](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/normalize.py:60) `normalize` | Creates old signatures from category/type/tags/source/masked text. It removes concrete keys/locators instead of applying reviewed identity roles. Both parser service and projection use it; keeping it would preserve a second identity authority. |
| E06 | [models/issue.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/issue.py:14); [models/parse.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/parse.py:10) | `KNOWN_CATEGORIES`, `IssueDraft`, `NormalizedIssue`, `Issue`, occurrences, source-block records and parse counters connect extractors, parser, repository and projection. “Issue cluster” is an exact-signature aggregate, not a related-error discovery capability. |
| E07 | [classification/normalize.py:253](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:253) `block_message`, `split_location_evidence:266`, structured-slot helpers at 273–504 | Contains useful grammar, locator separation and typed normalization. These mechanics must bind original values and provenance before creating a masked matching view. They are not an alternative taxonomy. |
| E08 | [classification/normalize.py:595](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:595) `_normalize_persistent_clause`; `semantic_units:606` | Splits persistent-reader clauses but masks keys and strips near-line information before returning plain strings. Does not return per-diagnostic source spans. A later whole-emission first-match lookup cannot reliably recover each child's values. |
| E09 | [classification/normalize.py:634](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:634) `tokenize`; `diagnostic_lead:673`, `legacy_diagnostic_lead:721`, `reason_lead:762` | Tokenization slices to 384 tokens. Current inference uses both current and old diagnostic leads. The learner has its own normalization/index generation, so removal must align the selected artifact and runtime; no second lead lookup should survive. |
| E10 | [classification/contracts.py:23](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:23) `ValidatedSlot`, `TemplateValidation`; `validate_template_tokens:62` | Exact literal sequence and typed-slot validation already exist. They do not yet define the complete approved error type, rendering and aggregation identity. Bindings should be produced here without later projection rematching. |
| E11 | [classification/inference.py:29](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:29) `ClassificationResult`; `Classifier.classify` 84–208, `classify_block` 210–227 | Production runtime compares a diagnostic against loaded model contracts and applies exact typed matching. For layered diagnostics L1-only means exact L1 classification with L2 unclassified; no approximate template match is authorized. Existing `full` also covers complete non-layered contracts. Current result lacks direct `error_type`/rendering/identity definition; similarity is not an approval state. See WORKPLAN.md 1.4 for the outcome definitions. |
| E12 | [classification/model.py:39](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:39) `ModelCluster`; `load_model:141` | Strict hash/schema/normalizer-bound structural model. Clusters contain structural templates and layers, not direct error types. The loader itself does not require projection. The selected artifact has no per-entry pending-approval status; absence of such a field does not revoke its existing approved selection. |
| E13 | [classification/catalog.py:13](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:13) model/projection pins; `load_approved_classifier:76`, `load_approved_semantic_runtime:80` | Model-only loading is possible. Product processing/classify entry points load the paired semantic runtime. Source-tree and installed package resource lookup must both select the new approved artifact; neither may fall back to an older revision. |
| E14 | [classification/service.py:100](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:100) `classify_session` | Loads stored raw source blocks, prepares assignments and replaces a separately committed classification run. Reclassify/version checks permit historical mutation. Its `run_id` is a classification-run identity, distinct from the product Run ID. |
| E15 | [classification/__init__.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/__init__.py:9) exports | Importing the classification package also imports its old service and database dependencies. Removing files without updating this initializer breaks otherwise model-only callers. Other package initializers have no equivalent service export. |

### 2.3 Semantic projection: the complete removal surface

| ID | Current owner and exact surface | Dependencies and effect |
|---|---|---|
| P01 | [classification/projection_catalog.py:59](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/projection_catalog.py:59), loader at 421 | Separate slot/reference/type/accounting definitions, old category validation and contract-ID helpers. Requires catalog coverage for every structural model contract. |
| P02 | [semantic_projection.py:99](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:99) evidence classes; locator/slot extraction at 147/184; complete-message analysis at 217/234 | Some real locator parsing is independently useful, including separating file locators from event URIs. Whole-emission extraction is coupled to a later reconstruction path. Only justified grammar/binding logic has a destination in the canonical contract implementation. |
| P03 | [semantic_projection.py:287](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:287) alignment, span/reference extraction; default/resolution at 475–529; `project_issue:532`, `project_normalized_issue:605` | Rematches templates, interprets reference specifications, assigns category/type/accounting, creates old issue drafts, then runs the old signature normalizer. This is the competing runtime authority; moving or renaming the whole dispatcher would preserve the banned design. |
| P04 | [semantic_projection_service.py:145](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:145) `_reconstruct`; `project_classification_run:225` | Recreates lexer/classifier objects from stored payloads and raw blocks, projects occurrences, then calls `replace_semantic_projection:432`. Product calls are exactly CLI 799 and processing 946. |
| P05 | [db/repository.py:2058](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:2058) projection getters/input reconstruction/counting/validation through 2528; replacement at 2531 | Deletes/replaces issues and occurrences, stores projection lineage, updates old counters and commits. No independent product capability requires these APIs or their transaction representation. |
| P06 | [models/67303093ecda779d/semantic_projection_catalog.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/semantic_projection_catalog.json); model and manifest in same directory | Structural artifact has 891 clusters, including 240 with layers; catalog has 892 entries. The manifest binds projection. The catalog includes both reviewed and manufactured unknown dispositions; its export stripped the provenance needed to distinguish all individual defaults. It is not a source of automatically approved replacement labels. |

### 2.4 Storage, review and read consumers

| ID | Current owner and exact surface | Dependencies and effect |
|---|---|---|
| D01 | [db/schema.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:4), `ALL_DDL:509`, versions at 541 | Tables comprise `sessions`, `session_files`, `run_metadata`, `schema_versions`, `issues`, `issue_occurrences`, `classification_models`, `classification_runs`, `classification_contracts`, `classification_payloads`, `classification_assignments`, `semantic_projection_runs`, `session_baselines`, `ignored_patterns`, `session_runtime_contexts`, `session_mounted_dlcs`, `session_mounted_mods`, `source_resolution_observations`, `source_file_instances`, `raw_block_contents`, `source_blocks`. The appendix lists every referencing file. |
| D02 | [db/repository.py:68](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:68) `open_db`; `open_db_readonly:116`; [db/migrations.py:40](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:40) | Writable open applies migrations and may compact/VACUUM. Read-only open uses migration detection and reports migration required. Some planner/audit connections bypass this opener. Changing only the writable opener therefore leaves additional schema assumptions to remove. |
| D03 | [db/repository.py:168](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:168) error-log hash lookup; registration at 259; metadata at 442/604/624; run queries at 728–847 | Contains independently required deduplication and run facts alongside legacy registration repair. Run listing synthesizes `legacy-session-` labels; latest-run joins projection/classification. Archive registration currently assigns a session identity before classification succeeds. |
| D04 | [db/repository.py:1065](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1065) parse result; row writers at 1104–1217; replacement at 1286–1543; adapter at 1546 | Stores raw source blocks, old aggregates and per-occurrence rows. Historical replacement deletes prior classification/parser state. `replace_canonical_parse` has no direct caller; its prepared-list adapter is unnecessary. |
| D05 | [db/repository.py:1577](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1577) classification reads; model registration at 1644/1752; replacement at 1763 | Separately persists models, contract templates, payloads and per-source assignments. [db/payloads.py:24](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/payloads.py:24) hashes the old payload representation for this writer and migrations. Model/contract lineage is needed; this payload schema and replace-history lifecycle are not. |
| D06 | [db/schema.py:292](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:292) projection table/index/trigger; repository P05 | The deletion trigger resets old session counters. Reports also depend on projection foreign keys attached to issue rows. All disappear with the fresh schema, not by converting old rows. |
| D07 | [db/repository.py:2840](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:2840) `list_classification_review_items`; [cli.py:869](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:869) review command region | DB-backed unresolved review groups classifier payloads. There is no native per-Run review writer in the current product. Replacing the store requires reconnecting review navigation and counts; keeping the old queue would duplicate unresolved content. |
| D08 | [reporting.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:15) `latest_report_target`; `latest_session_id:43`; `build_session_report:81` | Requires projection at 99 and validates it at 108. Reads classifier payloads for source/pattern/review summaries, issues for category summaries, occurrences for files, and old context/metadata. Top patterns group primarily by contract/template, not every meaning-bearing value. Latest fallback serves old run metadata. |
| D09 | [database_audit.py:80](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:80) `audit_database` | Has independent read-only open and an old required-table list. Even ordinary audit reopens archived logs and reconstructs header facts, scans filesystem state, and checks projection/raw/issue/context tables. Its deep flag adds old distributions. Ordinary audit cannot retain these raw-log dependencies under the target architecture. |
| D10 | [session_intelligence.py:22](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:22) classification lookup; baselines at 61–127; previous at 141; identity at 213–250; patterns at 391; comparison at 647/889/908 | Baselines/ignore state and comparisons depend on old assignments, projection selection and metadata fallbacks. Pattern identity can be contract ID alone or stripped normalized text. `report --since` imports/calls this module; removing standalone commands alone does not detach it. |
| D11 | [source_resolution.py:27](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:27) location parser; context roots at 82; resolution at 151/269/321; observations at 335/454; references at 409 | Reads old runtime context; referenced-file discovery reads classifier/raw payloads and projection. `observe_session_sources` has no direct product caller. The registered resolve command and triage are callers of resolution. `_live_projection` and `_stored_projection` concern filesystem resolution, not the semantic catalog; disposition follows ownership, not a word match. |
| D12 | [triage.py:25](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:25) compatibility locator wrapper; latest at 30; pattern files at 46; `build_triage:81` | Re-parses raw/payload location data, uses projection-backed latest selection, comparisons, reporting, source resolution and observations. It is an entire provisional consumer chain, not a reason to retain raw DB rows. |
| D13 | [runtime_context.py:274](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:274) `_analyze_debug_context`; `parse_debug_context:456`; stored service at 545 | Inventory/`Mounted Data:` grammar serves the explicitly required same-Run debug-log fast-follow. WORKPLAN F1 ports the underlying analyzer to the new playset file. `parse_debug_context` is an old compatibility wrapper and is not ported. The stored service depends on old session manifests/context tables and reparse/currentness; processing calls it at 888 and CLI at 2139. |

### 2.5 CLI registration closure

All registrations below are in [cli.py:2395](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2395).
Exact callback registration expressions also appear in the caller index.

| Current surface / registration line | Current dependency | Required disposition proposed after the full map |
|---|---|---|
| `capture` 2406; `watch` 2423 | C02–C05 | Retain capture/lifecycle behavior; adjust only shared capture-format dependencies affected by removal. |
| `ingest` 2413 | C01, C06–C08 | Make explicit manual/recovery input use canonical capture/processing; remove archive adoption, implicit whole-store reconciliation and registration-only success semantics. |
| `reconcile` 2446 | C08 | Remove historical archive/row repair command. Explicit fresh replay uses the canonical input path. |
| `sessions` 2453 | D03 | Preserve run listing from canonical records; use Run vocabulary (`runs`), without a compatibility alias. |
| `doctor` 2458 | Config/environment | No projection dependency. Existing write probes are a separate read-only-doctor gap, not a reason to add work to the classification change. |
| `audit-db` 2461 | D09 | Recalibrate to current-generation stored facts; remove old projection/raw-log/distribution assumptions and corresponding options. |
| `observe-logging` 2473 | `logging_observer`, watcher process identity | No classifier/schema dependency requiring change. Preserve unrelated in-flight source edits. |
| `parse` 2484; `classify` 2502 | E02/E14/P04 | Remove standalone historical-stage commands, `--reparse`, `--reclassify`, projection catalog/hash options and projected results. Supported manual processing executes the whole canonical path. |
| `review-queue` 2519 | D07 | Replace its DB-payload implementation with navigation to native Run review evidence and DB metadata. Do not retain a second queue store. |
| `report` 2540; `latest` 2567; `errors` 2581 | D08 and optional D10 | Reconnect to direct records, stored rendering/lineage and review metadata. Remove `--session` aliases, projection output and provisional comparison (`--since`) coupling. Canonical selection is `--run`. |
| `process-pending` 2602 | C09/C10; handler at 1499 | Retain exact selected-capture operation. Remove semantic-runtime load, projected counts, historical currentness and old operational machinery without an independent requirement. |
| `backfill-session` 2625 | C11; handler at 1617 | Remove historical rewrite route. |
| `compare` 2643; `baseline` 2670 with create/list/delete; `ignore` 2694 with add/list/remove | D10 | Remove this provisional feature chain from the active product; do not adapt its old identity or tables. |
| `context` 2719 | D13 stored service | Remove old reparse/storage command; preserve required pure playset-extraction logic for the approved fast-follow. |
| `resolve-file` 2732; `triage` 2741 | D11/D12 | Remove provisional commands and their unsupported old-data modules. Future source context consumes accepted diagnostics under its own requirements. |
| `_cmd_process_pending_wide_legacy:1234`; `_log_type_from_relpath:668` | Dead/rejected helpers | Neither has a CLI registration; no direct call was found. Delete. |

`_cmd_report:1048` imports session intelligence even when `--since` is absent.
`latest_session_id` also has callers in CLI comparison, session intelligence
and triage. These imports/helpers leave with the provisional chain; a new
Run selector belongs in the canonical repository, without a forwarding alias.

### 2.6 Model authoring, package resources and other consumers

| ID | Current owner and exact surface | Dependencies and effect |
|---|---|---|
| L01 | [learn_error_templates.py:344](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:344) evidence discovery; normalization at 398–910; clustering at 956–1102; serialization at 1485 | Useful selected-evidence learning and provenance. Duplicates runtime normalization, including older lead behavior and token truncation. `collect_records:1102` uses the real lexer at 1108. It should produce candidate structures, not runtime approval. |
| L02 | [learn_error_templates.py:1162](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1162) `best_cluster`, `best_layered_cluster`, mutation helpers and `evaluate_frozen_oracle:1326`; arguments/main at 1574/1602 | Training is coupled to the frozen 252 rows, synthetic mutation and category/type purity. Report writing also expects these results. Duplicated evaluator matchers have callers in tools slated for removal, not the runtime. |
| L03 | [incremental_template_registry.py:121](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:121) candidate/feature paths, sync at 189, roles at 293, build at 366, CLI at 500 | Useful deliberately selected training inputs, caches and revision provenance. `candidate`/`training` roles describe evidence logs, not contracts waiting for approval. Every build invokes the old oracle at 390 and CLI forwards `--oracle-root`. Universal holdout roles are not a required learner capability. Current-format feature generation must agree with the selected normalizer. |
| L04 | [build_semantic_projection_catalog.py:742](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:742) main; defaults at 972; compatible export at 1156; calibration at 1207 | Uses finite reviewed rows to manufacture unknown defaults for other model contracts. Export strips `projection_authority`. Imports runtime projection and model-only loading. Entire generator and its policy have no destination in the target. |
| L05 | [build_review_pack.py:388](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:388); [evaluate_unseen_session.py:27](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:27); three files under `tools/template_learning/blind_review/` | Frozen review pack and uncommissioned historical evaluation chain. The three files are `build_blind_stratified_sample.py`, `compare_blind_adjudication.py`, `evaluate_postfix_blind_sample.py`. They depend on learner-side matchers/reconstruction, the lexer, fixed evidence assumptions and/or old output schemas. |
| L06 | [mine_symbol_suffixes.py:18](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:18); [analyze_script_system_layers.py:23](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/analyze_script_system_layers.py:23) | Miner imports the unseen evaluator and duplicate matcher. Layer analyzer reads registry features and is not projection code. Neither has an established current use in this recovery. Default recommendation is removal, not speculative replacement tooling. |
| L07 | [tools/evaluate_classifier.py:18](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:18) `evaluate` | Additional caller absent from the review inventory: uses runtime lexer/classifier to produce coverage summaries. It is not the frozen oracle or a product stage. Its output/result API will change; deciding any future evaluator belongs to the separately commissioned verification task. No automatic port or replacement is proposed. |
| L08 | [models/67303093ecda779d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/manifest.json); older `models/93196794a7e0115d/`; [pyproject.toml:29](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) | Package ships current structural model, manifest and projection catalog. Older structural revision remains in the active tree but is not selected. New direct-contract artifact selection, loader/normalizer and package data must change together; superseded active revisions must not remain as runtime fallbacks. |
| L09 | [tests/test_processing_recovery_requirements.py](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py); [tests/test_watcher_capture_requirements.py](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py); [.github/workflows/ci.yml](C:/Users/nateb/Documents/ck3chronicle/.github/workflows/ci.yml) | Downstream import/schema/behavior consumers, not preservation authority. Source index records their imports/table references. Requirement-derived verification design and resulting changes are deliberately deferred by this task; old projection assertions must not dictate the implementation. |
| L10 | [tools/migrate_legacy_pending_metadata.ps1](C:/Users/nateb/Documents/ck3chronicle/tools/migrate_legacy_pending_metadata.ps1) | One-time conversion utility, not a required permanent facility. Current status records that all 22 rehearsal copies completed processing; original evidence remains unchanged. Remove the utility without repeating the operation or making production conversion a precondition. |

Lexer constructor dependencies deserve a specific correction to the review:
the projection bridge, frozen oracle, frozen review pack and projection
generator construct `TimestampedLogBlock` directly. Those callers are being
removed. The retained learner uses the real lexer. The lexer's own normal and
preamble constructors must supply explicit fields. There is no retained
fixture-compatibility requirement.

### 2.7 Documentation dependencies and dated findings

| Documents | Current interpretation and eventual disposition |
|---|---|
| [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md), [README.md](C:/Users/nateb/Documents/ck3chronicle/README.md), [ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md), [CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md) | Several appendix allegations refer to earlier text: these now route toward direct contracts and replanning. Do not blindly apply old line-number edits. Update only eventual code/CLI/status facts that actually change. Never read or revive the rejected earlier prompt directory named by the handoff. |
| [PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md), [PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md) | Contain historical operational results and stale approval/debt claims. Eventual implementation should distinguish observed history from the newly reviewed plan. Existing measurements and counts create no preservation target. |
| [TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md), [MODEL_QUALITY_AND_PROMOTION.md](C:/Users/nateb/Documents/ck3chronicle/docs/MODEL_QUALITY_AND_PROMOTION.md), [DATA_COMPATIBILITY_AND_OPERATIONS.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATA_COMPATIBILITY_AND_OPERATIONS.md) | Reconcile old migration/reparse/alias/identity/retention prescriptions with current intent. Current source archives have no automatic age or size expiry; the older one-week policy is superseded. Do not create replacement compatibility policy. |
| [REQUIREMENTS_AND_TESTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/REQUIREMENTS_AND_TESTING.md), [RELEASE_READINESS.md](C:/Users/nateb/Documents/ck3chronicle/docs/RELEASE_READINESS.md) | Obsolete projection/migration expectations cannot govern the new implementation. Actual verification and release-condition redesign remains outside this planning task. |
| [REPOSITORY_AND_BACKUP.md](C:/Users/nateb/Documents/ck3chronicle/docs/REPOSITORY_AND_BACKUP.md), [WORKSPACE_ROUTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/WORKSPACE_ROUTING.md), [models/README.md](C:/Users/nateb/Documents/ck3chronicle/models/README.md) | Align eventual active ownership, model packaging and supported operations; remove instructions directing work to projection/migration facilities. |
| [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md), [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md) | Remove WIP-preservation, frozen review, blind-evaluator and projection-generator ownership. Update the existing guides' obsolete tool/reporting inventory. The learner stays in its current separate files; WORKPLAN 3.2 lists the bounded edits. |
| [DEVELOPMENT_RESTART_AUDIT_2026-09-08.md](C:/Users/nateb/Documents/ck3chronicle/docs/DEVELOPMENT_RESTART_AUDIT_2026-09-08.md), [DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md) | Historical/background material. Do not turn past incidents or suggestions into new protocols, packages, or owner requirements. The deleted ingestion operational plan stays deleted. |

This map does not re-establish the old pre-reboot Git chronology, inspect
external 252-row artifacts, or inventory production evidence. Those are not
necessary to trace the current code and are not authorized operational work.

## 3. Conclusions from the complete dependency graph

### 3.1 The replacement boundary is the stored representation

Projection is removable. What connects its callers is the current old issue /
raw-block / classifier-payload representation. The coherent replacement must
change the producing services, database writer, result objects, queries and
operator entry points together. There is no need for a separate compatibility
phase and no product requirement to preserve the old intermediate rows.

The target owning path is:

```text
explicit protected input
  -> complete emission recognition
  -> approved source-specific diagnostic splitting with original provenance
  -> runtime Classifier.classify selects matches from the loaded model (inference.py 84–108)
  -> validate_template_tokens authorizes the outcome (contracts.py 62–146)
  -> approved diagnostic aggregation + native review routing
  -> successful Run in one current SQLite generation
  -> database reports and ordinary audit
```

An emission and a recovered diagnostic are transient processing objects.
Their existence does not require permanent source-block or occurrence tables.
Compact records retain the contract's meaning-bearing values and the context
needed for reporting. The database retains the approved rendering definition
and immutable lineage needed to interpret those records without reopening a
log or loading a later model revision.

### 3.2 Binding original values is a prerequisite for compact storage

Removing projection's post-hoc extraction reveals a defect in the current
classifier input: some keys and per-clause locators have already disappeared
into placeholders. Fix splitting and typed binding before finalizing the
direct-record writer. The canonical path should carry original child values
and spans, with a separate normalized view used by the runtime classifier to
select matches from the loaded model. Reusing the
old masked signature or grouping only by contract ID would collapse distinct
diagnostics. No later reconstruction/mapping service should recover discarded
information.

The 384-token slice must not allow a full assignment to be authorized from a
truncated prefix. Whole-log completeness and complete diagnostic handling
apply to every input size. This does not introduce a special size branch,
fixture, benchmark or quota.

### 3.3 Native review replaces the intermediate unresolved store

Interpret classification first using WORKPLAN.md section 1 and its exact
references to OWNER_PRODUCT_INTENT.md 89–146 and
ARCHITECTURE_AND_DATA_LINEAGE.md 118–153 / 176–191. L1-only means L1 classified
successfully while L2 remains unclassified; it is not a partial template match.
Approved complete classifications and reportable L1 classifications become
compact records. Unknown, provisional and low-confidence diagnostics retain
their original emission headers and continuation lines in the Run ID
review shard, in original order/frequency. Every successful Run has one shard,
including an empty shard when nothing needs review. SQLite stores navigation
and integrity metadata, not duplicate native payload. Complete emission
accounting is required; 100% classification is not.

For a split emission with both approved and unresolved children, retain the
native emission once in its original position, preserve why it was routed and
which children were unresolved, and keep diagnostic counts distinct from
emission counts. This is a proposed representation choice serving the existing
accounting requirement; it must not silently count the whole emission again
as an additional diagnostic. Native bytes cannot be reconstructed by encoding
the lexer's replacement-decoded text.

Ordinary SQLite transactions and filesystem publication should satisfy the
stated complete-Run behavior. Do not port the processor journal, invent a
Run-ID reservation protocol, or introduce a publication state machine merely
because the old pipeline has multiple commits. A concrete unresolved design
choice would return to the owner at implementation review.

### 3.4 Required consumers have canonical destinations

| Retained behavior | Destination after removal | What deliberately disappears |
|---|---|---|
| Complete error-log processing | New `src/ck3chronicle/pipeline/` package; exact ports R1–R7 and new composition N1–N9 in WORKPLAN | Preliminary regex issues, raw-text DB staging, re-reading stored classifier assignments and semantic projection |
| Error type, slots, rendering, identity | Approved error contract and its typed binding result | Separate category taxonomy, catalog mappings, signature normalizer and “classification meaning” abstraction |
| Run listing, latest, errors, reports | Current-generation Run/diagnostic repository reads | Projection-backed selection, historical metadata fallback, old dictionary/output fields and `--session` aliases |
| Review navigation | Native shard reference plus stored review metadata | DB-backed unresolved payload queue |
| Ordinary audit | Current-generation database facts | Required source-log reopening, filesystem reconciliation and projection consistency queries |
| Manual/recovery input | Explicit current input contract and the same processing service | Legacy bundle importer, fabricated observation facts, archive adoption and whole-store reconciliation |
| Fresh generation replay | Explicit retained `error.log` inputs and the same service, writing a separately named destination | Old DB reading, row translation, automatic migration, historical reparse/backfill and in-place cutover |
| Classification lineage | Immutable generation/model/contract/parser/splitter identities associated with new Runs | Mutable per-stage classification/projection histories |
| Structural learning | Existing tools/template_learning/learn_error_templates.py and incremental_template_registry.py, with only WORKPLAN L1–L5 dependency/tool-removal edits | Frozen-252 approval policy, universal holdout framework, duplicated evaluator inference and automatic promotion |
| Required playset fast-follow foundation | Pure inventory and `Mounted Data:` extraction ported to new `pipeline/playset.py` under F1; old runtime_context.py is deleted | Mandatory error-log processing dependency on old context tables/reparse service |

The default disposition of provisional comparison/baseline/ignore/source
resolution/triage is deletion, including their CLI/report imports, tables and
repository helpers. Their current presence does not commission reimplementation.
This does not delete the independently required playset extraction foundation.

### 3.5 Explicit inputs and fresh replay share one processor

The old manual input route is not a usable canonical replay path: it creates
legacy manifests, adopts archives and commits registration independently.
Both selected pending processing and explicit manual/replay input must reach
the same new diagnostic writer. Candidate-generation destination and review
storage must be explicit and isolated from the active generation; generation-
local Run IDs must not cause shard-path collisions.

Retained native `error.log` files are still valid inputs after old manifest
readers are deleted. Explicitly selecting such a file through the supported
manual/replay input contract does not require interpreting its old database or
archive format. It must not be an automatic “try the old format, then raw file”
fallback. Capture facts may be supplied only through the supported current
input contract; absent observed lifecycle/playset facts remain unavailable.
Do not infer them from an archive directory, file timestamp or older database.
No rewriting or normalization of original evidence is proposed.

Fresh replay and the canonical writer therefore belong in the same connected
runtime change. A later replay package would leave the removal of old input
and database paths unresolved or encourage a temporary adapter.

### 3.6 A new artifact revision is needed; wholesale relearning is not implied

The current structural model is already selected as approved and is loadable
without projection. Its package is nevertheless bound to the old catalog, and
its schema does not directly contain all the required contract fields. Publish
a clean immutable direct-contract revision carrying forward established
structures and definitions. Moving an established rule into its canonical
owner does not require reapproving it as a new candidate.

Identify any concrete field or behavior that cannot be supplied from an
established definition, or that must change under current requirements. Only
those additions, unresolved decisions and behavioral changes need substantive
contract review. Review of the new artifact revision is separate from blanket
review of every existing entry. Do not mechanically promote all projection
rows into unquestioned contracts or treat sample-absence defaults as an
approval ledger. Conversely, deleting the projection mechanism does not itself
invalidate an independently established type or slot rule stored there.

Regenerating normalization/index features or relearning particular structures
may be necessary where the corrected splitter/normalizer changes them. Neither
retaining exactly 891 clusters nor retraining everything is a requirement.
A structure without an approved direct rule remains outside approved record
eligibility and preserves native review evidence. This does not imply a
per-entry provisional state in the current model (see WORKPLAN 1.4). A move to the new format does not establish that an existing
structure is unapproved. Coverage and labels may change, including decreasing,
when an identified old misclassification is removed.

Switch model format, normalizer, loader, catalog selection and package resources
together. Remove the old projection-bound directory and superseded active
revision; leave existing Git history alone. Do not create an archive/export
project, partial old revision, dual-schema loader or runtime rollback fallback
to justify keeping banned code.

### 3.7 Construction strategy and bounded offline dependencies

The new production implementation is built under
`C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/`.
WORKPLAN sections 2, 6 and 7 provide exact per-package create/edit/delete lists.
Every implementation package must supply the owner's changed-path scope proof
against its starting state, including tracked/untracked/ignored files.

R1–R7 and C1/C2/F1 in WORKPLAN 3.1/3.3 specify exact source-to-destination
ports. N1–N9 in section 4 specify new interfaces/composition and the precise
old-stage/table dependencies that explain why those bodies change.

The earlier proposal to move/split the entire learner into a new source package
is withdrawn from this production project. Its working clustering algorithm and
evidence registry already run offline. The concrete cross-boundary source edge
is learner import at learn_error_templates.py:35, type use at 719 and real-lexer
call at 1108. Those reconnect to the new emission module; they do not establish
a runtime call into learning.

The other offline edits remove mandatory frozen-oracle calls/options/report
fields and now-unused helpers after the obsolete tool files are deleted.
WORKPLAN L1–L5 enumerates them. Future source-folder relocation, algorithm work,
normalization unification and candidate-promotion redesign remain separate
projects. Future promotion still has to satisfy the current direct artifact
format and normalized-contract requirements.

## 4. Review-finding coverage and new construction ownership

| Existing finding / source-map IDs | Implementation assignment |
|---|---|
| E01: lexer and fixture-only header/defaults | 1.2 R1 -> new emissions/domain interfaces; old source retirement in 3.2. |
| E09–E15: current matching, typed validation, optional layer model/loaders | 1.1/1.3 R5–R7/N1 -> new contracts/model/catalog/classifier. Current structural entries are evidenced in WORKPLAN 1.3, not assumed to be complete target error contracts. |
| E07–E09, P02/P03: normalization, original values, persistent splitting, locator grammar | 1.2 R2–R4/N2 -> new normalization/diagnostics/bindings; whole-message projection rematching is omitted. |
| L01–L03: learner/registry and lexer dependency | 3.2 L1–L5 edit the exact existing offline files; no learner rebuild/relocation. |
| E02–E06: extractor taxonomy, aliases, fallback, old issue models/normalizer | Whole-file retirement in 3.2 after the new kernel/records are connected. |
| P01–P06, L04/L08: projection tools/catalog/runtime/service/package bindings | Tool/runtime/artifact deletion and application switch together in 3.2. |
| C09–C12, D02–D09: staged storage/processing/read dependencies | N3–N9 in 2.1/2.2/3.1; exact caller switch in 3.2. |
| D10–D13: provisional comparison/baseline/ignore/source/triage | Delete the old chain and registrations in 3.2; F1 ports the independently required playset analyzer in 2.2. |
| C08–C11: migrating opens and historical reparse/reclassify/backfill | New N6 current-generation storage and N7 replay; old route retirement in 3.2. |
| E03/D04: no-caller parser/repository/multi-log helpers and wide CLI | Delete with the named providers/handlers in 3.2. |
| D04/D07/D08/E06: old review queue/issue-cluster identity | N4/N5/N8 -> compact approved diagnostic identities and native-emission review. |
| C13/D03/D08/D10: Python import fallback, metadata fallback and command aliases | Specific config/CLI edits in WORKPLAN 6.1; old provider retirement. |
| C05–C08/L10: manual/recovery input and legacy converters | C1/C2/N3 in 2.2; old input/conversion code deletion in 3.2, preserving original evidence. |
| L02–L06: frozen review/blind/unseen tools, miner/layer analyzer and oracle coupling | Eight tool deletions in WORKPLAN 6.2 plus bounded L2–L5 edits in existing learner files. |
| L07/L09: ordinary evaluator and tests/CI | Separate verification design, explicitly enumerated in WORKPLAN 8.1. |
| Documentation dependencies in 2.7 | Exact allowed documentation edits in WORKPLAN 2.2/8.3. Existing canonical decisions are inputs. |
| Old sample-count/proof/archive prescriptions | Background only. The owner-requested file-scope proof is explicit; product verification remains separately scoped. |

## 5. Three construction stages and seven mini-projects

| Stage | Concrete construction | Coordinating prompt |
|---|---|---|
| 1 | 1.1 direct definitions/interfaces; 1.2 original-byte recovery/binding; 1.3 runtime classifier and direct artifact | [STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md) |
| 2 | 2.1 aggregation/native review/current storage; 2.2 explicit inputs/common processor/fresh replay | [STAGE_2_RUN_PROCESSING_ORCHESTRATOR_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_2_RUN_PROCESSING_ORCHESTRATOR_PROMPT.md) |
| 3 | 3.1 stored reports/audit/commands; 3.2 application/model switch, bounded offline edits and complete provider/tool retirement | [STAGE_3_APPLICATION_SWITCH_ORCHESTRATOR_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_3_APPLICATION_SWITCH_ORCHESTRATOR_PROMPT.md) |

The exact per-mini-project file scopes and handoffs are in [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md)
and the expanded prompts indexed by [MASTER_ORCHESTRATOR_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md). The source IDs in this map
remain stable. Every source finding has a named destination or deletion.

Stages 1 and 2 construct the new package without activating a second production
path. Mini-project 3.2 owns application activation and retirement together.
The stage boundaries do not authorize compatibility adapters or partial old
provider retention.

## 6. Evidence limits that constrain the plan

WORKPLAN 1.2–1.4 records the direct field inventory, concrete model entries,
current branch behavior and absent status fields:

- The selected structural model has 240 layered entries and 651 with null
  layer metadata. Learner serialization at 1485–1530 deliberately supports
  both; production whole-template matching at inference 109–124 supports both.
  This is not proof of complete direct error-type/identity/rendering fields.
- No per-cluster provisional/status/confidence field exists in that model.
  Runtime numeric similarity and projection categorical confidence are separate.
  Canonical provisional/low-confidence preservation policy does not by itself
  define current model states or operational thresholds.
- Diagnostic records mean approved compact SQLite identities. Current unknown
  classifier results can carry transient slots; target persistence is the
  original native emission plus review metadata. The old unknown IssueDraft
  at semantic_projection.py 475–496 is a removal example, not target authority.
- The inspected canonical sources define the error-type hierarchy and required
  information but do not supply a complete enumerated direct-contract taxonomy.

These are source/model/document inspections. No classifier run, learner build,
production query, evaluator or product test was used to manufacture proof.
The work remains planning only.
