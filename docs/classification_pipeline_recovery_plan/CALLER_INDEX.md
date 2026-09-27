# Current source dependency index

Implementation routing: Stage 1 (1.1–1.3) constructs the classification core;
Stage 2 (2.1–2.2) constructs complete Run processing; Stage 3 (3.1–3.2) connects
reads/commands and retires the old graph. Exact prompts are indexed in
[MASTER_ORCHESTRATOR_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md).
This index records the inspected existing source; its old imports/calls are
removal evidence, not instructions to retain those APIs. L1–L5 offline edits
and all provider/tool deletions occur in mini-project 3.2.

Planning evidence captured on 2026-09-13 from the working tree, including pre-existing edits. This is a source map, not execution evidence or a proposed verification procedure. No product module was imported or executed to produce it.

Coverage: all 66 Python files under `src/`, `tools/`, and `tests/`; SQL references below are taken from those files. The companion dependency map covers package resources, command registrations, filesystem formats, owning documentation, and the required disposition of these edges.

Imported call expressions are resolved from source aliases. Local receiver calls such as `classifier.classify_block`, callbacks, SQL dependencies, and same-module helper chains need the accompanying manual map. A missing call here establishes only that no matching direct imported call expression was found; it does not establish that a symbol is unreachable.

## Internal imports

### src/ck3chronicle/archive_registry.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/archive_registry.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:10) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/archive_registry.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:11) | `ck3chronicle.harvester` | `ArchiveIntegrityError, MANIFEST_NAME, adopt_legacy_archive, read_capture_metadata, read_snapshot, snapshot_file_metadata_matches_manifest, snapshot_manifest_projection` |

### src/ck3chronicle/classification/__init__.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/__init__.py:7](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/__init__.py:7) | `ck3chronicle.classification.inference` | `ClassificationResult, Classifier` |
| [src/ck3chronicle/classification/__init__.py:8](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/__init__.py:8) | `ck3chronicle.classification.model` | `EmpiricalModel, ModelIntegrityError, load_model` |
| [src/ck3chronicle/classification/__init__.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/__init__.py:9) | `ck3chronicle.classification.service` | `ClassificationError, ClassificationPreconditionError, ClassificationRunResult, classify_session` |

### src/ck3chronicle/classification/catalog.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/catalog.py:8](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:8) | `ck3chronicle.classification.inference` | `Classifier` |
| [src/ck3chronicle/classification/catalog.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:9) | `ck3chronicle.classification.model` | `EmpiricalModel, load_model` |
| [src/ck3chronicle/classification/catalog.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:10) | `ck3chronicle.classification.projection_catalog` | `ProjectionCatalog, load_projection_catalog` |

### src/ck3chronicle/classification/contracts.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/contracts.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:14) | `ck3chronicle.classification.normalize` | `KEY, LOCATOR, OPTIONAL_KEY, TYPE` |

### src/ck3chronicle/classification/inference.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/inference.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:10) | `ck3chronicle.classification.contracts` | `TemplateValidation, validate_template_tokens` |
| [src/ck3chronicle/classification/inference.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:11) | `ck3chronicle.classification.model` | `EmpiricalModel, ModelCluster` |
| [src/ck3chronicle/classification/inference.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:12) | `ck3chronicle.classification.normalize` | `LOCATOR, PUNCTUATION, TRUNCATED_REASON, diagnostic_lead, block_message, extract_structured_slots, legacy_diagnostic_lead, reason_lead, semantic_units, script_system_layers, split_location_evidence, tokenize` |

### src/ck3chronicle/classification/model.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/model.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:11) | `ck3chronicle.classification.normalize` | `tokenize` |

### src/ck3chronicle/classification/projection_catalog.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/projection_catalog.py:20](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/projection_catalog.py:20) | `ck3chronicle.models.issue` | `ConfidenceValue, KNOWN_CATEGORIES` |
| [src/ck3chronicle/classification/projection_catalog.py:22](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/projection_catalog.py:22) | `ck3chronicle.classification.model` | `EmpiricalModel, ModelCluster` |

### src/ck3chronicle/classification/service.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/classification/service.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:11) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/classification/service.py:13](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:13) | `ck3chronicle.classification.inference` | `ClassificationResult, Classifier` |

### src/ck3chronicle/cli.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/cli.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:12) | `ck3chronicle.ingest` | `ingest` |
| [src/ck3chronicle/cli.py:29](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:29) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:30](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:30) | `ck3chronicle.harvester` | `spool_logs` |
| [src/ck3chronicle/cli.py:76](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:76) | `ck3chronicle.harvester` | `ArchiveIntegrityError, InvalidCaptureInput, UnstableCapture` |
| [src/ck3chronicle/cli.py:81](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:81) | `ck3chronicle.db.repository` | `ExistingErrorLogHashError` |
| [src/ck3chronicle/cli.py:113](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:113) | `ck3chronicle.command_envelope` | `command_envelope` |
| [src/ck3chronicle/cli.py:144](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:144) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:145](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:145) | `ck3chronicle.watcher` | `is_process_running` |
| [src/ck3chronicle/cli.py:172](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:172) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:173](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:173) | `ck3chronicle.watcher` | `EventJournal, WatcherLease, find_process, infer_termination_from_crashes, is_process_running, scan_crash_inventory, watch_sessions` |
| [src/ck3chronicle/cli.py:532](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:532) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:533](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:533) | `ck3chronicle.archive_registry` | `reconcile_archives` |
| [src/ck3chronicle/cli.py:556](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:556) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:557](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:557) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:589](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:589) | `ck3chronicle.doctor` | `run_doctor` |
| [src/ck3chronicle/cli.py:599](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:599) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:600](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:600) | `ck3chronicle.database_audit` | `DatabaseAuditError, audit_database` |
| [src/ck3chronicle/cli.py:645](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:645) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:646](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:646) | `ck3chronicle.logging_observer` | `observe_logging_progress` |
| [src/ck3chronicle/cli.py:647](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:647) | `ck3chronicle.watcher` | `ProcessProbeError, find_process` |
| [src/ck3chronicle/cli.py:684](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:684) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:685](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:685) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:686](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:686) | `ck3chronicle.parser.service` | `CanonicalParseError, parse_session` |
| [src/ck3chronicle/cli.py:728](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:728) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:729](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:729) | `ck3chronicle.classification` | `ClassificationError, Classifier, ModelIntegrityError, classify_session, load_model` |
| [src/ck3chronicle/cli.py:736](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:736) | `ck3chronicle.classification.catalog` | `APPROVED_MODEL_SHA256, load_approved_semantic_runtime, approved_model_path` |
| [src/ck3chronicle/cli.py:741](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:741) | `ck3chronicle.classification.projection_catalog` | `ProjectionCatalogIntegrityError, load_projection_catalog` |
| [src/ck3chronicle/cli.py:745](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:745) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:746](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:746) | `ck3chronicle.semantic_projection_service` | `SemanticProjectionServiceError, project_classification_run` |
| [src/ck3chronicle/cli.py:865](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:865) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:866](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:866) | `ck3chronicle.classification.catalog` | `APPROVED_MODEL_SHA256` |
| [src/ck3chronicle/cli.py:867](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:867) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:948](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:948) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:949](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:949) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:950](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:950) | `ck3chronicle.reporting` | `ReportError, build_session_report, latest_report_target` |
| [src/ck3chronicle/cli.py:1051](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1051) | `ck3chronicle.reporting` | `ReportError` |
| [src/ck3chronicle/cli.py:1052](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1052) | `ck3chronicle.session_intelligence` | `ComparisonError, compare_sessions` |
| [src/ck3chronicle/cli.py:1059](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1059) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1060](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1060) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:1150](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1150) | `ck3chronicle.reporting` | `ReportError` |
| [src/ck3chronicle/cli.py:1239](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1239) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1240](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1240) | `ck3chronicle.classification.catalog` | `load_approved_semantic_runtime` |
| [src/ck3chronicle/cli.py:1241](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1241) | `ck3chronicle.classification.model` | `ModelIntegrityError` |
| [src/ck3chronicle/cli.py:1242](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1242) | `ck3chronicle.harvester` | `ArchiveIntegrityError` |
| [src/ck3chronicle/cli.py:1243](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1243) | `ck3chronicle.processing` | `ProcessingJournal, ProcessorAlreadyRunning, ProcessorLease, process_pending` |
| [src/ck3chronicle/cli.py:1421](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1421) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1422](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1422) | `ck3chronicle.config` | `ConfigurationError` |
| [src/ck3chronicle/cli.py:1457](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1457) | `ck3chronicle.classification.model` | `ModelIntegrityError` |
| [src/ck3chronicle/cli.py:1458](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1458) | `ck3chronicle.db.repository` | `ExistingErrorLogHashError` |
| [src/ck3chronicle/cli.py:1459](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1459) | `ck3chronicle.harvester` | `ArchiveIntegrityError` |
| [src/ck3chronicle/cli.py:1460](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1460) | `ck3chronicle.processing` | `ProcessorAlreadyRunning` |
| [src/ck3chronicle/cli.py:1501](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1501) | `ck3chronicle.classification.catalog` | `load_approved_semantic_runtime` |
| [src/ck3chronicle/cli.py:1502](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1502) | `ck3chronicle.processing` | `ProcessingJournal, ProcessorLease, plan_pending_capture, process_planned_pending_capture` |
| [src/ck3chronicle/cli.py:1619](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1619) | `ck3chronicle.classification.catalog` | `load_approved_semantic_runtime` |
| [src/ck3chronicle/cli.py:1620](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1620) | `ck3chronicle.processing` | `ProcessingJournal, ProcessorLease, plan_selected_sessions, process_selected_sessions` |
| [src/ck3chronicle/cli.py:1805](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1805) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1806](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1806) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:1807](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1807) | `ck3chronicle.session_intelligence` | `ComparisonError, compare_against_baseline, compare_latest, compare_sessions` |
| [src/ck3chronicle/cli.py:1862](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1862) | `ck3chronicle.reporting` | `latest_session_id` |
| [src/ck3chronicle/cli.py:1885](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1885) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1886](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1886) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:1887](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1887) | `ck3chronicle.session_intelligence` | `PolicyError, create_baseline` |
| [src/ck3chronicle/cli.py:1931](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1931) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1932](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1932) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:1933](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1933) | `ck3chronicle.session_intelligence` | `list_baselines` |
| [src/ck3chronicle/cli.py:1971](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1971) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:1972](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1972) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:1973](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1973) | `ck3chronicle.session_intelligence` | `delete_baseline` |
| [src/ck3chronicle/cli.py:2017](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2017) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:2018](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2018) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:2019](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2019) | `ck3chronicle.session_intelligence` | `PolicyError, ignore_pattern` |
| [src/ck3chronicle/cli.py:2054](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2054) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:2055](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2055) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:2056](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2056) | `ck3chronicle.session_intelligence` | `list_ignored_patterns` |
| [src/ck3chronicle/cli.py:2090](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2090) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:2091](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2091) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:2092](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2092) | `ck3chronicle.session_intelligence` | `unignore_pattern` |
| [src/ck3chronicle/cli.py:2132](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2132) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:2133](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2133) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:2134](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2134) | `ck3chronicle.runtime_context` | `RuntimeContextError, parse_runtime_context` |
| [src/ck3chronicle/cli.py:2249](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2249) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:2250](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2250) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:2251](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2251) | `ck3chronicle.source_resolution` | `SourceResolutionError, resolve_file_instances` |
| [src/ck3chronicle/cli.py:2303](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2303) | `ck3chronicle` | `config` |
| [src/ck3chronicle/cli.py:2304](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2304) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/cli.py:2305](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2305) | `ck3chronicle.triage` | `TriageError, build_triage` |

### src/ck3chronicle/db/migrations.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/db/migrations.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:11) | `ck3chronicle.db.payloads` | `payload_sha256` |
| [src/ck3chronicle/db/migrations.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:12) | `ck3chronicle.db.schema` | `ALL_DDL, CANONICAL_ISSUES_VERSION, CAPTURE_VERSION, CLASSIFICATION_ASSIGNMENTS_IDX_DDL, CLASSIFICATION_ASSIGNMENTS_SOURCE_BLOCK_IDX_DDL, CLASSIFICATION_VERSION, CURRENT_VERSION, ISSUE_OCCURRENCES_IDX_DDL, ISSUE_OCCURRENCES_PROJECTION_RUN_IDX_DDL, ISSUE_OCCURRENCES_PROJECTION_SIGNATURE_IDX_DDL, ISSUE_OCCURRENCES_PROJECTION_SOURCE_IDX_DDL, ISSUE_OCCURRENCES_SOURCE_BLOCK_IDX_DDL, ISSUES_PROJECTION_RUN_IDX_DDL, RUNTIME_CONTEXT_VERSION, SEMANTIC_PROJECTION_VERSION, SESSION_RUNTIME_CONTEXTS_DDL, SESSION_CONTEXT_VERSION, SESSION_INTELLIGENCE_VERSION, SOURCE_BLOCKS_IDX_DDL, SOURCE_RESOLUTION_VERSION, STORAGE_VERSION` |

### src/ck3chronicle/db/repository.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/db/repository.py:13](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:13) | `ck3chronicle.db.migrations` | `apply_migrations, migrations_required` |
| [src/ck3chronicle/db/repository.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:14) | `ck3chronicle.db.payloads` | `payload_sha256` |
| [src/ck3chronicle/db/repository.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:15) | `ck3chronicle.models.issue` | `NormalizedIssue` |
| [src/ck3chronicle/db/repository.py:16](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:16) | `ck3chronicle.models.parse` | `ClusterRecord, OccurrenceRecord, ParseCounters, ParseResult, SourceBlockRecord` |

### src/ck3chronicle/doctor.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/doctor.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/doctor.py:9) | `ck3chronicle` | `__version__` |
| [src/ck3chronicle/doctor.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/doctor.py:10) | `ck3chronicle` | `config` |

### src/ck3chronicle/ingest.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/ingest.py:7](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:7) | `ck3chronicle` | `config` |
| [src/ck3chronicle/ingest.py:8](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:8) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/ingest.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:9) | `ck3chronicle.harvester` | `ArchiveIntegrityError, build_bundle, snapshot` |
| [src/ck3chronicle/ingest.py:47](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:47) | `ck3chronicle.archive_registry` | `reconcile_archives` |

### src/ck3chronicle/logging_observer.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/logging_observer.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/logging_observer.py:14) | `ck3chronicle.watcher` | `ProcessIdentity` |

### src/ck3chronicle/models/parse.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/models/parse.py:6](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/parse.py:6) | `ck3chronicle.models.issue` | `NormalizedIssue` |

### src/ck3chronicle/parser/extractors/__init__.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/__init__.py:21](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:21) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |
| [src/ck3chronicle/parser/extractors/__init__.py:22](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:22) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/__init__.py:24](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:24) | `ck3chronicle.parser.extractors` | `debug_log, script_system, localization, descriptor, persistent_reader, asset_graphics, gui_interface, event_system, database_reference, history_setup, culture_faith, script_hygiene, unclassified` |

### src/ck3chronicle/parser/extractors/asset_graphics.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/asset_graphics.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/asset_graphics.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/asset_graphics.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/asset_graphics.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/culture_faith.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/culture_faith.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/culture_faith.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/culture_faith.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/culture_faith.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/database_reference.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/database_reference.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/database_reference.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/database_reference.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/database_reference.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/debug_log.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/debug_log.py:26](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/debug_log.py:26) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/debug_log.py:27](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/debug_log.py:27) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/descriptor.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/descriptor.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/descriptor.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/descriptor.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/descriptor.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/event_system.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/event_system.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/event_system.py:10) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/event_system.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/event_system.py:11) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/gui_interface.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/gui_interface.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/gui_interface.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/gui_interface.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/gui_interface.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/history_setup.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/history_setup.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/history_setup.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/history_setup.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/history_setup.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/localization.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/localization.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/localization.py:12) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/localization.py:13](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/localization.py:13) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/persistent_reader.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/persistent_reader.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/persistent_reader.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/persistent_reader.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/persistent_reader.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/script_hygiene.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/script_hygiene.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_hygiene.py:4) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/script_hygiene.py:5](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_hygiene.py:5) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/script_system.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/script_system.py:20](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_system.py:20) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/script_system.py:21](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_system.py:21) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/extractors/unclassified.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/extractors/unclassified.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/unclassified.py:9) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/extractors/unclassified.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/unclassified.py:10) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### src/ck3chronicle/parser/normalize.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/normalize.py:25](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/normalize.py:25) | `ck3chronicle.models.issue` | `IssueDraft, NormalizedIssue` |

### src/ck3chronicle/parser/service.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/parser/service.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:10) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/parser/service.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:11) | `ck3chronicle.models.parse` | `OccurrenceRecord, ParseCounters, ParseResult, SourceBlockRecord` |
| [src/ck3chronicle/parser/service.py:17](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:17) | `ck3chronicle.models.issue` | `IssueDraft` |
| [src/ck3chronicle/parser/service.py:18](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:18) | `ck3chronicle.parser.extractors` | `extract_block` |
| [src/ck3chronicle/parser/service.py:19](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:19) | `ck3chronicle.parser.extractors` | `unclassified` |
| [src/ck3chronicle/parser/service.py:20](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:20) | `ck3chronicle.parser.log_blocks` | `iter_log_blocks` |
| [src/ck3chronicle/parser/service.py:21](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:21) | `ck3chronicle.parser.normalize` | `normalize` |

### src/ck3chronicle/processing.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/processing.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:15) | `ck3chronicle.archive_registry` | `reconcile_archives, register_archive` |
| [src/ck3chronicle/processing.py:16](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:16) | `ck3chronicle.classification` | `Classifier, classify_session` |
| [src/ck3chronicle/processing.py:17](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:17) | `ck3chronicle.classification.service` | `CLASSIFICATION_CONTRACT_VERSION` |
| [src/ck3chronicle/processing.py:18](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:18) | `ck3chronicle.classification.projection_catalog` | `ProjectionCatalog` |
| [src/ck3chronicle/processing.py:19](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:19) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/processing.py:20](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:20) | `ck3chronicle.harvester` | `ArchiveIntegrityError, CapturedFile, finalize_pending, finalize_pending_captures, inspect_pending, read_snapshot, selected_pending_path` |
| [src/ck3chronicle/processing.py:29](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:29) | `ck3chronicle.parser.service` | `PARSER_CONTRACT_VERSION, parse_session` |
| [src/ck3chronicle/processing.py:30](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:30) | `ck3chronicle.reporting` | `build_session_report, latest_report_target` |
| [src/ck3chronicle/processing.py:31](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:31) | `ck3chronicle.runtime_context` | `parse_runtime_context` |
| [src/ck3chronicle/processing.py:32](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:32) | `ck3chronicle.semantic_projection_service` | `SEMANTIC_PROJECTION_CONTRACT_VERSION, project_classification_run` |
| [src/ck3chronicle/processing.py:757](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:757) | `ck3chronicle.classification.catalog` | `load_approved_projection_catalog` |

### src/ck3chronicle/reporting.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/reporting.py:8](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:8) | `ck3chronicle.db` | `repository` |

### src/ck3chronicle/runtime_context.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/runtime_context.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:15) | `ck3chronicle.db` | `repository` |

### src/ck3chronicle/semantic_projection.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/semantic_projection.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:14) | `ck3chronicle.classification.inference` | `ClassificationResult` |
| [src/ck3chronicle/semantic_projection.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:15) | `ck3chronicle.classification.normalize` | `KEY, LOCATOR, OPTIONAL_KEY, PARAM, PERSISTENT_UNEXPECTED_TOKEN_RE, SCRIPT_SYSTEM_ROLE_RE, TOKEN_RE, TYPE, VALUE, block_message, mask_locators, normalize_structured_slots` |
| [src/ck3chronicle/semantic_projection.py:29](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:29) | `ck3chronicle.classification.projection_catalog` | `ProjectionCatalog, ReferenceProjection, SemanticProjection` |
| [src/ck3chronicle/semantic_projection.py:34](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:34) | `ck3chronicle.models.issue` | `IssueDraft, NormalizedIssue` |
| [src/ck3chronicle/semantic_projection.py:35](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:35) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |
| [src/ck3chronicle/semantic_projection.py:36](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:36) | `ck3chronicle.parser.normalize` | `normalize` |

### src/ck3chronicle/semantic_projection_service.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/semantic_projection_service.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:11) | `ck3chronicle.classification.inference` | `ClassificationResult` |
| [src/ck3chronicle/semantic_projection_service.py:12](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:12) | `ck3chronicle.classification.projection_catalog` | `ProjectionCatalog` |
| [src/ck3chronicle/semantic_projection_service.py:13](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:13) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/semantic_projection_service.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:14) | `ck3chronicle.models.issue` | `NormalizedIssue` |
| [src/ck3chronicle/semantic_projection_service.py:15](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:15) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock, source_block_id` |
| [src/ck3chronicle/semantic_projection_service.py:16](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:16) | `ck3chronicle.semantic_projection` | `CompleteBlockEvidence, analyze_complete_block, project_normalized_issue` |

### src/ck3chronicle/session_intelligence.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/session_intelligence.py:10](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:10) | `ck3chronicle.db` | `repository` |
| [src/ck3chronicle/session_intelligence.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:11) | `ck3chronicle.reporting` | `latest_session_id` |

### src/ck3chronicle/source_resolution.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/source_resolution.py:11](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:11) | `ck3chronicle.db` | `repository` |

### src/ck3chronicle/triage.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/triage.py:8](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:8) | `ck3chronicle.reporting` | `build_session_report, latest_session_id` |
| [src/ck3chronicle/triage.py:9](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:9) | `ck3chronicle.session_intelligence` | `ComparisonError, assignment_pattern_id, compare_sessions` |
| [src/ck3chronicle/triage.py:14](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:14) | `ck3chronicle.source_resolution` | `compare_file_observations, extract_file_from_location, resolve_file_instances` |

### src/ck3chronicle/watcher.py

| Import site | Imported module | Symbols |
|---|---|---|
| [src/ck3chronicle/watcher.py:17](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:17) | `ck3chronicle.harvester` | `InvalidCaptureInput, UnstableCapture` |

### tests/test_processing_recovery_requirements.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tests/test_processing_recovery_requirements.py:12](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:12) | `ck3chronicle.archive_registry` | `register_archive` |
| [tests/test_processing_recovery_requirements.py:13](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:13) | `ck3chronicle.classification.catalog` | `load_approved_semantic_runtime` |
| [tests/test_processing_recovery_requirements.py:14](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:14) | `ck3chronicle.db` | `repository` |
| [tests/test_processing_recovery_requirements.py:15](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:15) | `ck3chronicle.harvester` | `MANIFEST_NAME, ArchiveIntegrityError, finalize_pending, spool_logs` |
| [tests/test_processing_recovery_requirements.py:21](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:21) | `ck3chronicle.processing` | `ProcessingJournal, ProcessorAlreadyRunning, ProcessorLease, plan_pending_capture, plan_selected_sessions, process_pending` |

### tests/test_watcher_capture_requirements.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tests/test_watcher_capture_requirements.py:14](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:14) | `ck3chronicle` | `harvester` |
| [tests/test_watcher_capture_requirements.py:15](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:15) | `ck3chronicle.harvester` | `CAPTURE_METADATA_NAME, UnstableCapture, spool_logs` |
| [tests/test_watcher_capture_requirements.py:20](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:20) | `ck3chronicle.watcher` | `CrashInventory, ProcessIdentity, scan_crash_inventory, watch_sessions` |

### tools/evaluate_classifier.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/evaluate_classifier.py:14](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:14) | `ck3chronicle.classification` | `Classifier, load_model` |
| [tools/evaluate_classifier.py:15](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:15) | `ck3chronicle.parser.log_blocks` | `iter_log_blocks` |

### tools/template_learning/blind_review/build_blind_stratified_sample.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/blind_review/build_blind_stratified_sample.py:12](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:12) | `tools.template_learning.evaluate_unseen_session` | `module as unseen` |
| [tools/template_learning/blind_review/build_blind_stratified_sample.py:13](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:13) | `tools.template_learning.learn_error_templates` | `module as learner` |

### tools/template_learning/blind_review/evaluate_postfix_blind_sample.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:12](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:12) | `tools.template_learning.evaluate_unseen_session` | `module as unseen` |
| [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:13](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:13) | `tools.template_learning.learn_error_templates` | `module as learner` |
| [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:14](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:14) | `ck3chronicle.parser.log_blocks` | `iter_log_blocks` |

### tools/template_learning/build_review_pack.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/build_review_pack.py:17](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:17) | `tools.template_learning.learn_error_templates` | `module as learner` |
| [tools/template_learning/build_review_pack.py:18](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:18) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |

### tools/template_learning/build_semantic_projection_catalog.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/build_semantic_projection_catalog.py:32](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:32) | `ck3chronicle.classification.catalog` | `APPROVED_MODEL_REVISION, APPROVED_MODEL_SHA256, load_approved_classifier` |
| [tools/template_learning/build_semantic_projection_catalog.py:37](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:37) | `ck3chronicle.classification.normalize` | `KEY, LOCATOR, OPTIONAL_KEY, PUNCTUATION, TOKEN_RE, TYPE` |
| [tools/template_learning/build_semantic_projection_catalog.py:45](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:45) | `ck3chronicle.classification.projection_catalog` | `load_projection_catalog` |
| [tools/template_learning/build_semantic_projection_catalog.py:48](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:48) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock` |
| [tools/template_learning/build_semantic_projection_catalog.py:49](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:49) | `ck3chronicle.semantic_projection` | `analyze_complete_message, project_issue` |

### tools/template_learning/evaluate_unseen_session.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/evaluate_unseen_session.py:15](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:15) | `tools.template_learning.learn_error_templates` | `module as learner` |
| [tools/template_learning/evaluate_unseen_session.py:16](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:16) | `ck3chronicle.parser.log_blocks` | `iter_log_blocks` |

### tools/template_learning/incremental_template_registry.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/incremental_template_registry.py:29](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:29) | `ck3chronicle` | `config as project_config` |
| [tools/template_learning/incremental_template_registry.py:32](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:32) | `tools.template_learning.learn_error_templates` | `module as learner` |

### tools/template_learning/learn_error_templates.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/learn_error_templates.py:34](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:34) | `ck3chronicle` | `config as project_config` |
| [tools/template_learning/learn_error_templates.py:35](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35) | `ck3chronicle.parser.log_blocks` | `TimestampedLogBlock, iter_log_blocks` |

### tools/template_learning/mine_symbol_suffixes.py

| Import site | Imported module | Symbols |
|---|---|---|
| [tools/template_learning/mine_symbol_suffixes.py:18](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:18) | `tools.template_learning.evaluate_unseen_session` | `module as unseen` |
| [tools/template_learning/mine_symbol_suffixes.py:19](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:19) | `tools.template_learning.learn_error_templates` | `module as learner` |

## Imported call sites

Grouped by the module that defines the imported target. Each entry records the caller function and exact source line. This includes calls inside obsolete or currently unregistered functions; reachability is distinguished in the companion map.

### ck3chronicle.archive_registry

| Imported target | Caller sites |
|---|---|
| `reconcile_archives` | [src/ck3chronicle/cli.py:536 (cmd_reconcile)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:536); [src/ck3chronicle/ingest.py:51 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:51); [src/ck3chronicle/processing.py:792 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:792) |
| `register_archive` | [src/ck3chronicle/processing.py:555 (process_planned_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:555); [tests/test_processing_recovery_requirements.py:52 (ProcessingRecoveryRequirements.test_one_database_identity_is_the_run_id)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:52); [tests/test_processing_recovery_requirements.py:309 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:309) |

### ck3chronicle.classification

| Imported target | Caller sites |
|---|---|
| `Classifier` | [src/ck3chronicle/cli.py:773 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:773); [src/ck3chronicle/cli.py:777 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:777); [tools/evaluate_classifier.py:73 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:73) |
| `classify_session` | [src/ck3chronicle/cli.py:793 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:793); [src/ck3chronicle/processing.py:929 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:929) |
| `load_model` | [src/ck3chronicle/cli.py:774 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:774); [src/ck3chronicle/cli.py:778 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:778); [tools/evaluate_classifier.py:73 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:73) |

### ck3chronicle.classification.catalog

| Imported target | Caller sites |
|---|---|
| `approved_model_path` | [src/ck3chronicle/cli.py:779 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:779) |
| `load_approved_classifier` | [tools/template_learning/build_semantic_projection_catalog.py:752 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:752) |
| `load_approved_projection_catalog` | [src/ck3chronicle/processing.py:761 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:761) |
| `load_approved_semantic_runtime` | [src/ck3chronicle/cli.py:783 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:783); [src/ck3chronicle/cli.py:1302 (_cmd_process_pending_wide_legacy)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1302); [src/ck3chronicle/cli.py:1515 (cmd_process_one_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1515); [src/ck3chronicle/cli.py:1633 (cmd_backfill_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1633); [tests/test_processing_recovery_requirements.py:145 (ProcessingRecoveryRequirements.test_pending_plan_is_read_only_and_names_exactly_one_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:145); [tests/test_processing_recovery_requirements.py:314 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:314) |

### ck3chronicle.classification.contracts

| Imported target | Caller sites |
|---|---|
| `validate_template_tokens` | [src/ck3chronicle/classification/inference.py:104 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:104); [src/ck3chronicle/classification/inference.py:156 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:156) |

### ck3chronicle.classification.inference

| Imported target | Caller sites |
|---|---|
| `ClassificationResult` | [src/ck3chronicle/semantic_projection_service.py:179 (_reconstruct)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:179) |
| `Classifier` | [src/ck3chronicle/classification/catalog.py:77 (load_approved_classifier)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:77); [src/ck3chronicle/classification/catalog.py:82 (load_approved_semantic_runtime)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:82) |

### ck3chronicle.classification.model

| Imported target | Caller sites |
|---|---|
| `load_model` | [src/ck3chronicle/classification/catalog.py:57 (load_approved_model)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:57) |

### ck3chronicle.classification.normalize

| Imported target | Caller sites |
|---|---|
| `PERSISTENT_UNEXPECTED_TOKEN_RE.match` | [src/ck3chronicle/semantic_projection.py:453 (_reference_values)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:453) |
| `SCRIPT_SYSTEM_ROLE_RE.match` | [src/ck3chronicle/semantic_projection.py:444 (_reference_values)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:444) |
| `TOKEN_RE.findall` | [tools/template_learning/build_semantic_projection_catalog.py:242 (exact_template_capture_specs)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:242) |
| `TOKEN_RE.finditer` | [src/ck3chronicle/semantic_projection.py:354 (_template_span_value)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:354) |
| `block_message` | [src/ck3chronicle/classification/inference.py:214 (Classifier.classify_block)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:214); [src/ck3chronicle/semantic_projection.py:220 (analyze_complete_block)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:220) |
| `diagnostic_lead` | [src/ck3chronicle/classification/inference.py:89 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:89) |
| `extract_structured_slots` | [src/ck3chronicle/classification/inference.py:86 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:86) |
| `legacy_diagnostic_lead` | [src/ck3chronicle/classification/inference.py:89 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:89) |
| `mask_locators` | [src/ck3chronicle/semantic_projection.py:353 (_template_span_value)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:353) |
| `normalize_structured_slots` | [src/ck3chronicle/semantic_projection.py:353 (_template_span_value)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:353) |
| `reason_lead` | [src/ck3chronicle/classification/inference.py:152 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:152) |
| `script_system_layers` | [src/ck3chronicle/classification/inference.py:126 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:126) |
| `semantic_units` | [src/ck3chronicle/classification/inference.py:215 (Classifier.classify_block)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:215) |
| `split_location_evidence` | [src/ck3chronicle/classification/inference.py:85 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:85) |
| `tokenize` | [src/ck3chronicle/classification/inference.py:87 (Classifier.classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:87); [src/ck3chronicle/classification/model.py:132 (_load_cluster)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:132) |

### ck3chronicle.classification.projection_catalog

| Imported target | Caller sites |
|---|---|
| `load_projection_catalog` | [src/ck3chronicle/classification/catalog.py:64 (load_approved_projection_catalog)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:64); [src/ck3chronicle/cli.py:785 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:785); [tools/template_learning/build_semantic_projection_catalog.py:1187 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:1187) |

### ck3chronicle.command_envelope

| Imported target | Caller sites |
|---|---|
| `command_envelope` | [src/ck3chronicle/cli.py:117 (_emit_command_json)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:117) |

### ck3chronicle.config

| Imported target | Caller sites |
|---|---|
| `CONFIG_FILE_PATH.is_file` | [src/ck3chronicle/cli.py:323 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:323) |
| `ConfigurationError` | [src/ck3chronicle/cli.py:1434 (_selected_processing_root)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1434) |
| `ROOT_CK3CHRONICLE.resolve` | [src/ck3chronicle/cli.py:185 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:185); [src/ck3chronicle/cli.py:1291 (_cmd_process_pending_wide_legacy)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1291); [src/ck3chronicle/cli.py:1426 (_selected_processing_root)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1426) |
| `ROOT_CRASHES.resolve` | [src/ck3chronicle/cli.py:184 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:184) |
| `ROOT_LOGS.drive.lower` | [src/ck3chronicle/doctor.py:56 (run_doctor)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/doctor.py:56) |
| `require_strict_descendant` | [src/ck3chronicle/cli.py:1427 (_selected_processing_root)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1427) |

### ck3chronicle.database_audit

| Imported target | Caller sites |
|---|---|
| `audit_database` | [src/ck3chronicle/cli.py:603 (cmd_audit_db)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:603) |

### ck3chronicle.db.migrations

| Imported target | Caller sites |
|---|---|
| `apply_migrations` | [src/ck3chronicle/db/repository.py:75 (open_db)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:75) |
| `migrations_required` | [src/ck3chronicle/db/repository.py:136 (open_db_readonly)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:136) |

### ck3chronicle.db.payloads

| Imported target | Caller sites |
|---|---|
| `payload_sha256` | [src/ck3chronicle/db/migrations.py:801 (_migrate_compact_storage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:801); [src/ck3chronicle/db/migrations.py:832 (_migrate_compact_storage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:832); [src/ck3chronicle/db/repository.py:1875 (replace_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1875) |

### ck3chronicle.db.repository

| Imported target | Caller sites |
|---|---|
| `ExistingErrorLogHashError` | [src/ck3chronicle/ingest.py:75 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:75); [src/ck3chronicle/processing.py:474 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:474) |
| `append_canonical_block` | [src/ck3chronicle/parser/service.py:264 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:264) |
| `begin_canonical_replacement` | [src/ck3chronicle/parser/service.py:194 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:194) |
| `count_canonical_clusters` | [src/ck3chronicle/parser/service.py:331 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:331) |
| `ensure_classification_model` | [src/ck3chronicle/classification/service.py:128 (classify_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:128) |
| `finish_canonical_replacement` | [src/ck3chronicle/parser/service.py:345 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:345) |
| `get_classification_model` | [src/ck3chronicle/cli.py:882 (cmd_review_queue)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:882); [src/ck3chronicle/reporting.py:111 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:111); [src/ck3chronicle/semantic_projection_service.py:264 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:264); [src/ck3chronicle/session_intelligence.py:304 (ignore_pattern)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:304) |
| `get_classification_run` | [src/ck3chronicle/classification/service.py:136 (classify_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:136); [src/ck3chronicle/cli.py:879 (cmd_review_queue)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:879); [src/ck3chronicle/processing.py:646 (plan_selected_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:646); [src/ck3chronicle/reporting.py:52 (_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:52); [src/ck3chronicle/semantic_projection_service.py:251 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:251) |
| `get_classification_source_blocks` | [src/ck3chronicle/classification/service.py:163 (classify_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:163) |
| `get_error_log_manifest_row` | [src/ck3chronicle/parser/service.py:130 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:130) |
| `get_log_manifest_row` | [src/ck3chronicle/runtime_context.py:558 (parse_runtime_context)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:558) |
| `get_mounted_dlcs` | [src/ck3chronicle/reporting.py:306 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:306); [src/ck3chronicle/reporting.py:331 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:331); [src/ck3chronicle/runtime_context.py:502 (_result_from_store)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:502); [src/ck3chronicle/session_intelligence.py:625 (_runtime_context_delta)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:625); [src/ck3chronicle/session_intelligence.py:626 (_runtime_context_delta)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:626); [src/ck3chronicle/source_resolution.py:98 (_recorded_roots)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:98) |
| `get_mounted_mods` | [src/ck3chronicle/reporting.py:315 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:315); [src/ck3chronicle/reporting.py:341 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:341); [src/ck3chronicle/runtime_context.py:514 (_result_from_store)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:514); [src/ck3chronicle/session_intelligence.py:631 (_runtime_context_delta)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:631); [src/ck3chronicle/session_intelligence.py:632 (_runtime_context_delta)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:632); [src/ck3chronicle/source_resolution.py:99 (_recorded_roots)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:99) |
| `get_run` | [src/ck3chronicle/cli.py:963 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:963); [tests/test_processing_recovery_requirements.py:66 (ProcessingRecoveryRequirements.test_one_database_identity_is_the_run_id)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:66) |
| `get_run_for_session` | [src/ck3chronicle/reporting.py:347 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:347); [src/ck3chronicle/session_intelligence.py:151 (previous_session_id)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:151); [src/ck3chronicle/session_intelligence.py:667 (compare_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:667); [src/ck3chronicle/session_intelligence.py:687 (compare_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:687) |
| `get_runtime_context` | [src/ck3chronicle/reporting.py:273 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:273); [src/ck3chronicle/runtime_context.py:490 (_result_from_store)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:490); [src/ck3chronicle/runtime_context.py:559 (parse_runtime_context)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:559); [src/ck3chronicle/session_intelligence.py:571 (_runtime_context_delta)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:571); [src/ck3chronicle/session_intelligence.py:572 (_runtime_context_delta)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:572); [src/ck3chronicle/source_resolution.py:88 (_recorded_roots)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:88) |
| `get_semantic_projection_inputs` | [src/ck3chronicle/semantic_projection_service.py:320 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:320) |
| `get_semantic_projection_run` | [src/ck3chronicle/processing.py:657 (plan_selected_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:657); [src/ck3chronicle/reporting.py:99 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:99); [src/ck3chronicle/semantic_projection_service.py:281 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:281); [src/ck3chronicle/semantic_projection_service.py:447 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:447) |
| `get_session` | [src/ck3chronicle/classification/service.py:112 (classify_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:112); [src/ck3chronicle/parser/service.py:102 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:102); [src/ck3chronicle/processing.py:619 (plan_selected_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:619); [src/ck3chronicle/reporting.py:91 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:91); [src/ck3chronicle/runtime_context.py:553 (parse_runtime_context)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:553); [src/ck3chronicle/semantic_projection_service.py:238 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:238); [src/ck3chronicle/session_intelligence.py:72 (create_baseline)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:72); [src/ck3chronicle/session_intelligence.py:148 (previous_session_id)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:148); [src/ck3chronicle/session_intelligence.py:658 (compare_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:658); [src/ck3chronicle/session_intelligence.py:692 (compare_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:692); [src/ck3chronicle/source_resolution.py:85 (_recorded_roots)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:85) |
| `get_session_by_error_log_hash` | [src/ck3chronicle/ingest.py:60 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:60); [src/ck3chronicle/processing.py:467 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:467) |
| `get_session_by_hash` | [src/ck3chronicle/archive_registry.py:220 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:220) |
| `get_successful_parse_result` | [src/ck3chronicle/parser/service.py:116 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:116) |
| `latest_run` | [src/ck3chronicle/reporting.py:19 (latest_report_target)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:19) |
| `list_classification_review_items` | [src/ck3chronicle/cli.py:889 (cmd_review_queue)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:889); [src/ck3chronicle/reporting.py:206 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:206) |
| `list_sessions` | [src/ck3chronicle/archive_registry.py:211 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:211); [src/ck3chronicle/cli.py:565 (cmd_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:565); [src/ck3chronicle/processing.py:826 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:826) |
| `open_db` | [src/ck3chronicle/archive_registry.py:123 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:123); [src/ck3chronicle/archive_registry.py:203 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:203); [src/ck3chronicle/cli.py:690 (cmd_parse)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:690); [src/ck3chronicle/cli.py:790 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:790); [src/ck3chronicle/cli.py:1891 (cmd_baseline_create)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1891); [src/ck3chronicle/cli.py:1977 (cmd_baseline_delete)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1977); [src/ck3chronicle/cli.py:2023 (cmd_ignore_add)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2023); [src/ck3chronicle/cli.py:2096 (cmd_ignore_remove)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2096); [src/ck3chronicle/cli.py:2138 (cmd_context)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2138); [src/ck3chronicle/ingest.py:58 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:58); [src/ck3chronicle/ingest.py:82 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:82); [src/ck3chronicle/processing.py:819 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:819); [tests/test_processing_recovery_requirements.py:118 (ProcessingRecoveryRequirements.test_pending_plan_is_read_only_and_names_exactly_one_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:118); [tests/test_processing_recovery_requirements.py:171 (ProcessingRecoveryRequirements.test_replacement_foreign_keys_have_leading_column_indexes)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:171); [tests/test_processing_recovery_requirements.py:294 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:294) |
| `open_db_readonly` | [src/ck3chronicle/cli.py:564 (cmd_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:564); [src/ck3chronicle/cli.py:876 (cmd_review_queue)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:876); [src/ck3chronicle/cli.py:954 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:954); [src/ck3chronicle/cli.py:1062 (_cmd_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1062); [src/ck3chronicle/cli.py:1820 (cmd_compare)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1820); [src/ck3chronicle/cli.py:1937 (cmd_baseline_list)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1937); [src/ck3chronicle/cli.py:2060 (cmd_ignore_list)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2060); [src/ck3chronicle/cli.py:2255 (cmd_resolve_file)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2255); [src/ck3chronicle/cli.py:2309 (cmd_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2309); [tests/test_processing_recovery_requirements.py:58 (ProcessingRecoveryRequirements.test_one_database_identity_is_the_run_id)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:58); [tests/test_processing_recovery_requirements.py:92 (ProcessingRecoveryRequirements.test_readonly_open_never_performs_an_implicit_migration)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:92) |
| `record_run_metadata` | [src/ck3chronicle/ingest.py:96 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:96) |
| `register_capture_metadata` | [src/ck3chronicle/archive_registry.py:160 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:160); [src/ck3chronicle/archive_registry.py:248 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:248); [src/ck3chronicle/archive_registry.py:275 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:275) |
| `register_finalized_session` | [src/ck3chronicle/archive_registry.py:130 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:130); [src/ck3chronicle/archive_registry.py:262 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:262); [src/ck3chronicle/ingest.py:84 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:84) |
| `replace_classification_run` | [src/ck3chronicle/classification/service.py:286 (classify_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:286) |
| `replace_runtime_context` | [src/ck3chronicle/runtime_context.py:641 (parse_runtime_context)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:641) |
| `replace_semantic_projection` | [src/ck3chronicle/semantic_projection_service.py:432 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:432) |
| `validate_finalized_session_projection` | [src/ck3chronicle/archive_registry.py:238 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:238); [src/ck3chronicle/processing.py:632 (plan_selected_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:632) |
| `validate_semantic_projection` | [src/ck3chronicle/reporting.py:108 (build_session_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:108) |

### ck3chronicle.doctor

| Imported target | Caller sites |
|---|---|
| `run_doctor` | [src/ck3chronicle/cli.py:591 (cmd_doctor)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:591) |

### ck3chronicle.harvester

| Imported target | Caller sites |
|---|---|
| `ArchiveIntegrityError` | [src/ck3chronicle/archive_registry.py:99 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:99); [src/ck3chronicle/archive_registry.py:102 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:102); [src/ck3chronicle/archive_registry.py:106 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:106); [src/ck3chronicle/archive_registry.py:216 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:216); [src/ck3chronicle/archive_registry.py:292 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:292); [src/ck3chronicle/ingest.py:72 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:72); [src/ck3chronicle/processing.py:430 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:430); [src/ck3chronicle/processing.py:443 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:443); [src/ck3chronicle/processing.py:458 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:458); [src/ck3chronicle/processing.py:530 (process_planned_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:530); [src/ck3chronicle/processing.py:627 (plan_selected_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:627) |
| `adopt_legacy_archive` | [src/ck3chronicle/archive_registry.py:260 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:260) |
| `build_bundle` | [src/ck3chronicle/ingest.py:52 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:52) |
| `finalize_pending` | [src/ck3chronicle/processing.py:536 (process_planned_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:536); [tests/test_processing_recovery_requirements.py:51 (ProcessingRecoveryRequirements.test_one_database_identity_is_the_run_id)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:51); [tests/test_processing_recovery_requirements.py:308 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:308) |
| `finalize_pending_captures` | [src/ck3chronicle/processing.py:769 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:769) |
| `inspect_pending` | [src/ck3chronicle/processing.py:428 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:428) |
| `read_capture_metadata` | [src/ck3chronicle/archive_registry.py:152 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:152); [src/ck3chronicle/archive_registry.py:246 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:246); [src/ck3chronicle/archive_registry.py:273 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:273) |
| `read_snapshot` | [src/ck3chronicle/archive_registry.py:112 (register_archive)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:112); [src/ck3chronicle/archive_registry.py:258 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:258); [src/ck3chronicle/processing.py:448 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:448); [src/ck3chronicle/processing.py:631 (plan_selected_sessions)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:631) |
| `selected_pending_path` | [src/ck3chronicle/processing.py:427 (plan_pending_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:427) |
| `snapshot` | [src/ck3chronicle/ingest.py:80 (ingest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:80) |
| `snapshot_file_metadata_matches_manifest` | [src/ck3chronicle/archive_registry.py:234 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:234) |
| `snapshot_manifest_projection` | [src/ck3chronicle/archive_registry.py:229 (reconcile_archives)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:229) |
| `spool_logs` | [src/ck3chronicle/cli.py:33 (_spool_once)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:33); [tests/test_processing_recovery_requirements.py:43 (ProcessingRecoveryRequirements.test_one_database_identity_is_the_run_id)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:43); [tests/test_processing_recovery_requirements.py:124 (ProcessingRecoveryRequirements.test_pending_plan_is_read_only_and_names_exactly_one_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:124); [tests/test_processing_recovery_requirements.py:136 (ProcessingRecoveryRequirements.test_pending_plan_is_read_only_and_names_exactly_one_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:136); [tests/test_processing_recovery_requirements.py:300 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:300); [tests/test_watcher_capture_requirements.py:41 (CaptureBoundaryTests.test_pending_capture_contains_error_log_only)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:41); [tests/test_watcher_capture_requirements.py:71 (CaptureBoundaryTests.test_published_capture_inherits_pending_directory_acl)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:71); [tests/test_watcher_capture_requirements.py:116 (CaptureBoundaryTests.test_unavailable_exception_does_not_discard_error_log)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:116); [tests/test_watcher_capture_requirements.py:150 (CaptureBoundaryTests.test_error_log_change_during_copy_is_not_published)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:150) |

### ck3chronicle.ingest

| Imported target | Caller sites |
|---|---|
| `ingest` | [src/ck3chronicle/cli.py:15 (_capture_once)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:15) |

### ck3chronicle.logging_observer

| Imported target | Caller sites |
|---|---|
| `observe_logging_progress` | [src/ck3chronicle/cli.py:651 (cmd_observe_logging)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:651) |

### ck3chronicle.models.issue

| Imported target | Caller sites |
|---|---|
| `IssueDraft` | [src/ck3chronicle/parser/extractors/asset_graphics.py:19 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/asset_graphics.py:19); [src/ck3chronicle/parser/extractors/culture_faith.py:18 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/culture_faith.py:18); [src/ck3chronicle/parser/extractors/database_reference.py:22 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/database_reference.py:22); [src/ck3chronicle/parser/extractors/debug_log.py:69 (_extract_pdx_localize)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/debug_log.py:69); [src/ck3chronicle/parser/extractors/debug_log.py:106 (_extract_gamedatabase)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/debug_log.py:106); [src/ck3chronicle/parser/extractors/descriptor.py:15 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/descriptor.py:15); [src/ck3chronicle/parser/extractors/event_system.py:21 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/event_system.py:21); [src/ck3chronicle/parser/extractors/gui_interface.py:18 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/gui_interface.py:18); [src/ck3chronicle/parser/extractors/history_setup.py:15 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/history_setup.py:15); [src/ck3chronicle/parser/extractors/localization.py:33 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/localization.py:33); [src/ck3chronicle/parser/extractors/persistent_reader.py:20 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/persistent_reader.py:20); [src/ck3chronicle/parser/extractors/script_hygiene.py:20 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_hygiene.py:20); [src/ck3chronicle/parser/extractors/script_system.py:89 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_system.py:89); [src/ck3chronicle/parser/extractors/unclassified.py:20 (extract)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/unclassified.py:20); [src/ck3chronicle/semantic_projection.py:480 (_unclassified_draft)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:480); [src/ck3chronicle/semantic_projection.py:586 (project_issue)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:586) |
| `NormalizedIssue` | [src/ck3chronicle/parser/normalize.py:81 (normalize)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/normalize.py:81) |

### ck3chronicle.models.parse

| Imported target | Caller sites |
|---|---|
| `OccurrenceRecord` | [src/ck3chronicle/parser/service.py:255 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:255) |
| `ParseCounters` | [src/ck3chronicle/db/repository.py:1090 (get_successful_parse_result)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1090); [src/ck3chronicle/parser/service.py:336 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:336) |
| `ParseResult` | [src/ck3chronicle/db/repository.py:1087 (get_successful_parse_result)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1087); [src/ck3chronicle/parser/service.py:405 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:405) |
| `SourceBlockRecord` | [src/ck3chronicle/parser/service.py:267 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:267) |

### ck3chronicle.parser.extractors

| Imported target | Caller sites |
|---|---|
| `extract_block` | [src/ck3chronicle/parser/service.py:230 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:230) |

### ck3chronicle.parser.extractors.unclassified

| Imported target | Caller sites |
|---|---|
| `extract` | [src/ck3chronicle/parser/extractors/__init__.py:108 (extract_block)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:108); [src/ck3chronicle/parser/extractors/__init__.py:121 (extract_block_for_log_type)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:121); [src/ck3chronicle/parser/service.py:239 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:239) |

### ck3chronicle.parser.log_blocks

| Imported target | Caller sites |
|---|---|
| `TimestampedLogBlock` | [src/ck3chronicle/semantic_projection_service.py:164 (_reconstruct)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:164); [tools/template_learning/build_review_pack.py:75 (sample_message)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:75); [tools/template_learning/build_semantic_projection_catalog.py:88 (make_block)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:88); [tools/template_learning/learn_error_templates.py:1349 (evaluate_frozen_oracle)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1349) |
| `iter_log_blocks` | [src/ck3chronicle/parser/service.py:205 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:205); [tools/evaluate_classifier.py:26 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:26); [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:77 (source_messages)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:77); [tools/template_learning/evaluate_unseen_session.py:58 (inference_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:58); [tools/template_learning/learn_error_templates.py:1108 (collect_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1108) |
| `source_block_id` | [src/ck3chronicle/semantic_projection_service.py:177 (_reconstruct)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:177) |

### ck3chronicle.parser.normalize

| Imported target | Caller sites |
|---|---|
| `normalize` | [src/ck3chronicle/parser/service.py:251 (parse_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:251); [src/ck3chronicle/semantic_projection.py:613 (project_normalized_issue)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:613) |

### ck3chronicle.parser.service

| Imported target | Caller sites |
|---|---|
| `parse_session` | [src/ck3chronicle/cli.py:692 (cmd_parse)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:692); [src/ck3chronicle/processing.py:903 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:903) |

### ck3chronicle.processing

| Imported target | Caller sites |
|---|---|
| `ProcessingJournal` | [src/ck3chronicle/cli.py:1284 (_cmd_process_pending_wide_legacy)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1284); [src/ck3chronicle/cli.py:1529 (cmd_process_one_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1529); [src/ck3chronicle/cli.py:1647 (cmd_backfill_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1647); [tests/test_processing_recovery_requirements.py:352 (ProcessingRecoveryRequirements.test_processing_journal_is_visible_before_pipeline_completion)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:352) |
| `ProcessorLease` | [src/ck3chronicle/cli.py:1283 (_cmd_process_pending_wide_legacy)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1283); [src/ck3chronicle/cli.py:1528 (cmd_process_one_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1528); [src/ck3chronicle/cli.py:1646 (cmd_backfill_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1646); [tests/test_processing_recovery_requirements.py:383 (ProcessingRecoveryRequirements.test_second_processor_cannot_acquire_the_same_runtime)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:383); [tests/test_processing_recovery_requirements.py:385 (ProcessingRecoveryRequirements.test_second_processor_cannot_acquire_the_same_runtime)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:385) |
| `plan_pending_capture` | [src/ck3chronicle/cli.py:1516 (cmd_process_one_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1516); [tests/test_processing_recovery_requirements.py:147 (ProcessingRecoveryRequirements.test_pending_plan_is_read_only_and_names_exactly_one_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:147) |
| `plan_selected_sessions` | [src/ck3chronicle/cli.py:1634 (cmd_backfill_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1634); [tests/test_processing_recovery_requirements.py:317 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:317); [tests/test_processing_recovery_requirements.py:341 (ProcessingRecoveryRequirements.test_backfill_plan_verifies_one_selected_archive_and_excludes_pending)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:341) |
| `process_pending` | [src/ck3chronicle/cli.py:1321 (_cmd_process_pending_wide_legacy)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1321); [tests/test_processing_recovery_requirements.py:105 (ProcessingRecoveryRequirements.test_wide_pending_pipeline_is_disabled_before_runtime_mutation)](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:105) |
| `process_planned_pending_capture` | [src/ck3chronicle/cli.py:1547 (cmd_process_one_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1547) |
| `process_selected_sessions` | [src/ck3chronicle/cli.py:1665 (cmd_backfill_session)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1665) |

### ck3chronicle.reporting

| Imported target | Caller sites |
|---|---|
| `ReportError` | [src/ck3chronicle/cli.py:960 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:960); [src/ck3chronicle/cli.py:965 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:965); [src/ck3chronicle/cli.py:970 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:970) |
| `build_session_report` | [src/ck3chronicle/cli.py:971 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:971); [src/ck3chronicle/processing.py:988 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:988); [src/ck3chronicle/triage.py:106 (build_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:106) |
| `latest_report_target` | [src/ck3chronicle/cli.py:958 (_report_for_args)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:958); [src/ck3chronicle/processing.py:978 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:978) |
| `latest_session_id` | [src/ck3chronicle/cli.py:1864 (_latest_session_and_model)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1864); [src/ck3chronicle/session_intelligence.py:896 (compare_latest)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:896); [src/ck3chronicle/session_intelligence.py:920 (compare_against_baseline)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:920); [src/ck3chronicle/triage.py:91 (build_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:91) |

### ck3chronicle.runtime_context

| Imported target | Caller sites |
|---|---|
| `parse_runtime_context` | [src/ck3chronicle/cli.py:2139 (cmd_context)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2139); [src/ck3chronicle/processing.py:888 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:888) |

### ck3chronicle.semantic_projection

| Imported target | Caller sites |
|---|---|
| `analyze_complete_block` | [src/ck3chronicle/semantic_projection_service.py:354 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:354) |
| `analyze_complete_message` | [tools/template_learning/build_semantic_projection_catalog.py:789 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:789) |
| `project_issue` | [tools/template_learning/build_semantic_projection_catalog.py:1207 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:1207) |
| `project_normalized_issue` | [src/ck3chronicle/semantic_projection_service.py:358 (project_classification_run)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:358) |

### ck3chronicle.semantic_projection_service

| Imported target | Caller sites |
|---|---|
| `project_classification_run` | [src/ck3chronicle/cli.py:799 (cmd_classify)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:799); [src/ck3chronicle/processing.py:946 (process_pending)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:946) |

### ck3chronicle.session_intelligence

| Imported target | Caller sites |
|---|---|
| `ComparisonError` | [src/ck3chronicle/cli.py:1817 (cmd_compare)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1817) |
| `assignment_pattern_id` | [src/ck3chronicle/triage.py:72 (_pattern_files)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:72) |
| `compare_against_baseline` | [src/ck3chronicle/cli.py:1824 (cmd_compare)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1824) |
| `compare_latest` | [src/ck3chronicle/cli.py:1831 (cmd_compare)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1831) |
| `compare_sessions` | [src/ck3chronicle/cli.py:1066 (_cmd_report)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1066); [src/ck3chronicle/cli.py:1838 (cmd_compare)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1838); [src/ck3chronicle/triage.py:95 (build_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:95) |
| `create_baseline` | [src/ck3chronicle/cli.py:1897 (cmd_baseline_create)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1897) |
| `delete_baseline` | [src/ck3chronicle/cli.py:1980 (cmd_baseline_delete)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1980) |
| `ignore_pattern` | [src/ck3chronicle/cli.py:2024 (cmd_ignore_add)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2024) |
| `list_baselines` | [src/ck3chronicle/cli.py:1940 (cmd_baseline_list)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1940) |
| `list_ignored_patterns` | [src/ck3chronicle/cli.py:2063 (cmd_ignore_list)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2063) |
| `unignore_pattern` | [src/ck3chronicle/cli.py:2098 (cmd_ignore_remove)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2098) |

### ck3chronicle.source_resolution

| Imported target | Caller sites |
|---|---|
| `compare_file_observations` | [src/ck3chronicle/triage.py:127 (build_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:127) |
| `extract_file_from_location` | [src/ck3chronicle/triage.py:27 (_file_from_location)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:27) |
| `resolve_file_instances` | [src/ck3chronicle/cli.py:2258 (cmd_resolve_file)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2258); [src/ck3chronicle/triage.py:126 (build_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:126) |

### ck3chronicle.triage

| Imported target | Caller sites |
|---|---|
| `build_triage` | [src/ck3chronicle/cli.py:2312 (cmd_triage)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2312) |

### ck3chronicle.watcher

| Imported target | Caller sites |
|---|---|
| `EventJournal` | [src/ck3chronicle/cli.py:371 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:371) |
| `ProcessIdentity` | [tests/test_watcher_capture_requirements.py:162 (WatcherLifecycleTests.test_only_an_observed_exit_triggers_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:162) |
| `WatcherLease` | [src/ck3chronicle/cli.py:371 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:371) |
| `find_process` | [src/ck3chronicle/cli.py:254 (cmd_watch.perform_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:254); [src/ck3chronicle/cli.py:496 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:496); [src/ck3chronicle/cli.py:654 (cmd_observe_logging)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:654) |
| `infer_termination_from_crashes` | [src/ck3chronicle/cli.py:456 (cmd_watch.lifecycle_event)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:456) |
| `is_process_running` | [src/ck3chronicle/cli.py:148 (cmd_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:148); [src/ck3chronicle/cli.py:156 (cmd_capture)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:156); [src/ck3chronicle/cli.py:210 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:210); [src/ck3chronicle/cli.py:218 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:218) |
| `scan_crash_inventory` | [src/ck3chronicle/cli.py:404 (cmd_watch.record_crash_inventory)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:404); [tests/test_watcher_capture_requirements.py:197 (WatcherLifecycleTests.test_crash_inventory_ignores_unrelated_directories)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:197) |
| `watch_sessions` | [src/ck3chronicle/cli.py:493 (cmd_watch)](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:493); [tests/test_watcher_capture_requirements.py:176 (WatcherLifecycleTests.test_only_an_observed_exit_triggers_capture)](C:/Users/nateb/Documents/ck3chronicle/tests/test_watcher_capture_requirements.py:176) |

### tools.template_learning.evaluate_unseen_session

| Imported target | Caller sites |
|---|---|
| `inference_records` | [tools/template_learning/blind_review/build_blind_stratified_sample.py:84 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:84) |
| `reconstruct_model` | [tools/template_learning/blind_review/build_blind_stratified_sample.py:83 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:83); [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:116 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:116); [tools/template_learning/mine_symbol_suffixes.py:64 (mine)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:64) |
| `sha256_file` | [tools/template_learning/blind_review/build_blind_stratified_sample.py:80 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:80); [tools/template_learning/blind_review/build_blind_stratified_sample.py:272 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:272); [tools/template_learning/blind_review/build_blind_stratified_sample.py:320 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:320); [tools/template_learning/blind_review/build_blind_stratified_sample.py:321 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:321); [tools/template_learning/blind_review/build_blind_stratified_sample.py:322 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:322); [tools/template_learning/blind_review/build_blind_stratified_sample.py:323 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:323); [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:287 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:287); [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:288 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:288) |

### tools.template_learning.learn_error_templates

| Imported target | Caller sites |
|---|---|
| `NORMALIZER_VERSION.encode` | [tools/template_learning/incremental_template_registry.py:143 (feature_cache_path)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:143) |
| `ProtectedLog` | [tools/template_learning/incremental_template_registry.py:262 (sync_registry)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:262) |
| `SequenceRecord` | [tools/template_learning/build_review_pack.py:47 (reconstruct_clusters)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:47); [tools/template_learning/evaluate_unseen_session.py:31 (reconstruct_model)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:31); [tools/template_learning/incremental_template_registry.py:341 (combine_training_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:341) |
| `TemplateCluster` | [tools/template_learning/build_review_pack.py:55 (reconstruct_clusters)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:55); [tools/template_learning/evaluate_unseen_session.py:39 (reconstruct_model)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:39) |
| `best_cluster` | [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:135 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:135); [tools/template_learning/build_review_pack.py:104 (map_samples)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:104); [tools/template_learning/mine_symbol_suffixes.py:79 (mine)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:79) |
| `best_layered_cluster` | [tools/template_learning/evaluate_unseen_session.py:97 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:97); [tools/template_learning/evaluate_unseen_session.py:204 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:204) |
| `block_message` | [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:80 (source_messages)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:80); [tools/template_learning/build_review_pack.py:86 (sample_message)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:86); [tools/template_learning/evaluate_unseen_session.py:62 (inference_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:62) |
| `cluster_source_records` | [tools/template_learning/incremental_template_registry.py:381 (build_revision)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:381) |
| `collect_records` | [tools/template_learning/incremental_template_registry.py:148 (feature_from_log)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:148) |
| `diagnostic_lead` | [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:139 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:139); [tools/template_learning/build_review_pack.py:108 (map_samples)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:108); [tools/template_learning/evaluate_unseen_session.py:73 (inference_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:73); [tools/template_learning/evaluate_unseen_session.py:208 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:208) |
| `evaluate_frozen_oracle` | [tools/template_learning/incremental_template_registry.py:390 (build_revision)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:390) |
| `has_ordered_anchor_overlap` | [tools/template_learning/blind_review/build_blind_stratified_sample.py:50 (ranked_matches)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:50) |
| `layered_contract_id` | [tools/template_learning/evaluate_unseen_session.py:146 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:146) |
| `mutate_locators` | [tools/template_learning/evaluate_unseen_session.py:203 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:203) |
| `script_system_layer_tokens` | [tools/template_learning/evaluate_unseen_session.py:105 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:105); [tools/template_learning/evaluate_unseen_session.py:131 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:131) |
| `semantic_units` | [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:132 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:132); [tools/template_learning/build_review_pack.py:102 (map_samples)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:102); [tools/template_learning/evaluate_unseen_session.py:63 (inference_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:63) |
| `sequence_similarity` | [tools/template_learning/blind_review/build_blind_stratified_sample.py:52 (ranked_matches)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:52); [tools/template_learning/blind_review/build_blind_stratified_sample.py:163 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:163) |
| `serializable_cluster` | [tools/template_learning/incremental_template_registry.py:434 (build_revision)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:434) |
| `sha256_file` | [tools/template_learning/incremental_template_registry.py:443 (build_revision)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:443) |
| `tokenize` | [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:138 (main)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:138); [tools/template_learning/build_review_pack.py:49 (reconstruct_clusters)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:49); [tools/template_learning/build_review_pack.py:107 (map_samples)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:107); [tools/template_learning/evaluate_unseen_session.py:33 (reconstruct_model)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:33); [tools/template_learning/evaluate_unseen_session.py:64 (inference_records)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:64); [tools/template_learning/evaluate_unseen_session.py:207 (evaluate)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:207) |
| `write_report` | [tools/template_learning/incremental_template_registry.py:442 (build_revision)](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:442) |

## Current table-name references

Every current DDL table name is listed. References include SQL, required-table lists, and test expectations. They identify consumers to remove or rewrite; they do not prescribe preserving a table. Occurrences in migrations and DDL are listed alongside live consumers so those dependencies are visible.

| Table | Files and line numbers |
|---|---|
| `classification_assignments` | [src/ck3chronicle/cli.py:624](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:624) (all lines: 624); [src/ck3chronicle/database_audit.py:24](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:24) (all lines: 24, 222, 386, 396, 578, 716, 736, 845, 846); [src/ck3chronicle/db/migrations.py:91](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:91) (all lines: 91, 118, 640, 665, 795, 861, 880, 891, 912); [src/ck3chronicle/db/repository.py:1964](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1964) (all lines: 1964, 2111, 2160, 2445, 2467, 2873); [src/ck3chronicle/db/schema.py:268](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:268) (all lines: 268, 283, 288); [src/ck3chronicle/reporting.py:125](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:125) (all lines: 125, 170); [src/ck3chronicle/session_intelligence.py:267](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:267) (all lines: 267, 281, 406); [src/ck3chronicle/source_resolution.py:431](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:431) (all lines: 431); [src/ck3chronicle/triage.py:55](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:55) (all lines: 55); [tests/test_processing_recovery_requirements.py:174](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:174) (all lines: 174) |
| `classification_contracts` | [src/ck3chronicle/db/repository.py:1685](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1685) (all lines: 1685, 1696, 1721); [src/ck3chronicle/db/schema.py:230](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:230) (all lines: 230); [src/ck3chronicle/reporting.py:175](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:175) (all lines: 175); [src/ck3chronicle/session_intelligence.py:408](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:408) (all lines: 408) |
| `classification_models` | [src/ck3chronicle/db/repository.py:1647](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1647) (all lines: 1647, 1661, 2053, 2109); [src/ck3chronicle/db/schema.py:195](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:195) (all lines: 195, 211, 231, 247, 296, 343, 353) |
| `classification_payloads` | [src/ck3chronicle/database_audit.py:23](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:23) (all lines: 23, 387, 737); [src/ck3chronicle/db/migrations.py:804](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:804) (all lines: 804, 819, 845, 869); [src/ck3chronicle/db/repository.py:1912](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1912) (all lines: 1912, 1936, 2113, 2875); [src/ck3chronicle/db/schema.py:244](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:244) (all lines: 244, 274, 336); [src/ck3chronicle/reporting.py:126](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:126) (all lines: 126, 171); [src/ck3chronicle/session_intelligence.py:269](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:269) (all lines: 269, 283, 407); [src/ck3chronicle/source_resolution.py:432](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:432) (all lines: 432); [src/ck3chronicle/triage.py:56](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:56) (all lines: 56) |
| `classification_runs` | [src/ck3chronicle/cli.py:1870](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:1870) (all lines: 1870); [src/ck3chronicle/database_audit.py:22](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:22) (all lines: 22, 221, 367, 395, 739, 843); [src/ck3chronicle/db/migrations.py:796](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:796) (all lines: 796, 847, 862); [src/ck3chronicle/db/repository.py:751](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:751) (all lines: 751, 1307, 1583, 1812, 1824, 2108, 2569, 2874); [src/ck3chronicle/db/schema.py:208](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:208) (all lines: 208, 276, 309); [src/ck3chronicle/reporting.py:31](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:31) (all lines: 31, 56); [src/ck3chronicle/session_intelligence.py:37](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:37) (all lines: 37, 160, 191, 268, 282, 494); [src/ck3chronicle/source_resolution.py:416](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:416) (all lines: 416); [src/ck3chronicle/triage.py:34](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:34) (all lines: 34) |
| `ignored_patterns` | [src/ck3chronicle/cli.py:2076](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2076) (all lines: 2076); [src/ck3chronicle/db/schema.py:352](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:352) (all lines: 352); [src/ck3chronicle/session_intelligence.py:315](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:315) (all lines: 315, 344, 351, 369, 720) |
| `issue_occurrences` | [src/ck3chronicle/cli.py:718](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:718) (all lines: 718); [src/ck3chronicle/database_audit.py:21](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:21) (all lines: 21, 195, 326, 349, 463, 470, 481, 550, 706); [src/ck3chronicle/db/migrations.py:85](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:85) (all lines: 85, 111, 400, 404, 408, 410, 413, 430, 460, 475, 487, 491, 492, 497, 498, 503, 504, 635, 662, 777, 882, 886, 903, 910); [src/ck3chronicle/db/repository.py:1075](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1075) (all lines: 1075, 1201, 1230, 1316, 1390, 1399, 1409, 1411, 1412, 1428, 1447, 1461, 1522, 2264, 2310, 2322, 2367, 2393, 2416, 2444, 2468, 2604); [src/ck3chronicle/db/schema.py:145](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:145) (all lines: 145, 169, 174, 179, 184, 189); [src/ck3chronicle/models/parse.py:42](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/parse.py:42) (all lines: 42, 52); [src/ck3chronicle/parser/service.py:177](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:177) (all lines: 177, 285, 298, 318, 339, 363); [src/ck3chronicle/reporting.py:150](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:150) (all lines: 150); [tests/test_processing_recovery_requirements.py:178](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:178) (all lines: 178, 188, 238, 265) |
| `issues` | [src/ck3chronicle/cli.py:2486](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2486) (all lines: 2486); [src/ck3chronicle/database_audit.py:20](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:20) (all lines: 20, 196, 197, 210, 220, 287, 348, 466, 471, 547, 842); [src/ck3chronicle/db/migrations.py:90](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:90) (all lines: 90, 117, 413, 449, 453, 490, 496, 502); [src/ck3chronicle/db/repository.py:1162](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1162) (all lines: 1162, 1170, 1334, 1372, 1391, 1395, 1400, 1446, 1465, 2222, 2231, 2312, 2316, 2323, 2392, 2420, 2545, 2595, 2606); [src/ck3chronicle/db/schema.py:98](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:98) (all lines: 98, 103, 131, 136, 141); [src/ck3chronicle/models/issue.py:1](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/issue.py:1) (all lines: 1); [src/ck3chronicle/reporting.py:138](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:138) (all lines: 138); [src/ck3chronicle/semantic_projection_service.py:235](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:235) (all lines: 235); [tests/test_processing_recovery_requirements.py:182](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:182) (all lines: 182, 237); [tools/template_learning/build_review_pack.py:111](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:111) (all lines: 111); [tools/template_learning/build_semantic_projection_catalog.py:376](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:376) (all lines: 376, 764, 787, 1200); [tools/template_learning/learn_error_templates.py:1388](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1388) (all lines: 1388) |
| `raw_block_contents` | [src/ck3chronicle/database_audit.py:18](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:18) (all lines: 18, 727); [src/ck3chronicle/db/migrations.py:689](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:689) (all lines: 689, 701, 725, 741); [src/ck3chronicle/db/repository.py:1111](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1111) (all lines: 1111, 1120, 1598, 2118); [src/ck3chronicle/db/schema.py:479](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:479) (all lines: 479, 498); [src/ck3chronicle/source_resolution.py:436](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:436) (all lines: 436); [src/ck3chronicle/triage.py:60](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:60) (all lines: 60) |
| `run_metadata` | [src/ck3chronicle/cli.py:963](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:963) (all lines: 963, 964, 966, 983, 988, 990, 991, 993, 995, 996, 998); [src/ck3chronicle/database_audit.py:29](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:29) (all lines: 29, 758, 769); [src/ck3chronicle/db/migrations.py:82](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:82) (all lines: 82, 295, 297, 304, 330, 347, 359); [src/ck3chronicle/db/repository.py:532](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:532) (all lines: 532, 571, 581, 732, 738, 760, 777, 794, 795); [src/ck3chronicle/db/schema.py:52](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:52) (all lines: 52); [src/ck3chronicle/reporting.py:347](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:347) (all lines: 347, 349, 352, 353, 354, 355, 356, 357, 358, 359, 362, 363, 364, 367, 371, 372, 375, 378, 379, 380, 385); [src/ck3chronicle/session_intelligence.py:151](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:151) (all lines: 151, 152, 154, 159, 460, 465, 466, 471, 475, 476, 477, 478, 493); [tests/test_processing_recovery_requirements.py:76](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:76) (all lines: 76) |
| `schema_versions` | [src/ck3chronicle/db/migrations.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:4) (all lines: 4, 48, 53, 549, 556, 563, 570, 577, 584, 591, 598, 605, 613); [src/ck3chronicle/db/repository.py:77](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:77) (all lines: 77, 95); [src/ck3chronicle/db/schema.py:90](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:90) (all lines: 90) |
| `semantic_projection_runs` | [src/ck3chronicle/database_audit.py:25](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:25) (all lines: 25, 223, 370, 402, 451, 844); [src/ck3chronicle/db/migrations.py:92](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:92) (all lines: 92, 454, 467); [src/ck3chronicle/db/repository.py:750](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:750) (all lines: 750, 2066, 2297, 2600, 2619); [src/ck3chronicle/db/schema.py:123](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:123) (all lines: 123, 161, 292, 318, 323); [src/ck3chronicle/reporting.py:30](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:30) (all lines: 30); [src/ck3chronicle/session_intelligence.py:38](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:38) (all lines: 38, 161, 192, 495); [src/ck3chronicle/source_resolution.py:417](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:417) (all lines: 417); [src/ck3chronicle/triage.py:35](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:35) (all lines: 35) |
| `session_baselines` | [src/ck3chronicle/db/schema.py:340](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:340) (all lines: 340); [src/ck3chronicle/session_intelligence.py:83](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:83) (all lines: 83, 107, 119, 131) |
| `session_files` | [src/ck3chronicle/database_audit.py:17](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:17) (all lines: 17, 193, 263, 282, 652); [src/ck3chronicle/db/migrations.py:213](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:213) (all lines: 213); [src/ck3chronicle/db/repository.py:175](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:175) (all lines: 175, 194, 234, 289, 349, 354, 426, 836, 856); [src/ck3chronicle/db/schema.py:40](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:40) (all lines: 40, 375) |
| `session_mounted_dlcs` | [src/ck3chronicle/database_audit.py:27](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:27) (all lines: 27, 200); [src/ck3chronicle/db/repository.py:881](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:881) (all lines: 881, 966, 1020); [src/ck3chronicle/db/schema.py:409](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:409) (all lines: 409) |
| `session_mounted_mods` | [src/ck3chronicle/database_audit.py:28](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:28) (all lines: 28, 201); [src/ck3chronicle/db/repository.py:895](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:895) (all lines: 895, 970, 1040); [src/ck3chronicle/db/schema.py:424](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:424) (all lines: 424) |
| `session_runtime_contexts` | [src/ck3chronicle/database_audit.py:26](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:26) (all lines: 26, 199, 586); [src/ck3chronicle/db/migrations.py:83](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:83) (all lines: 83, 371, 376, 382); [src/ck3chronicle/db/repository.py:870](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:870) (all lines: 870, 974, 979); [src/ck3chronicle/db/schema.py:364](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:364) (all lines: 364) |
| `sessions` | [src/ck3chronicle/archive_registry.py:100](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:100) (all lines: 100, 196); [src/ck3chronicle/cli.py:561](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:561) (all lines: 561, 569, 616, 631, 632, 638, 970, 1866, 2452, 2453, 2493, 2645); [src/ck3chronicle/database_audit.py:16](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:16) (all lines: 16, 89, 135, 154, 169, 770, 868, 891); [src/ck3chronicle/db/migrations.py:81](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:81) (all lines: 81, 183, 186, 205, 218, 357, 716, 750); [src/ck3chronicle/db/repository.py:151](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:151) (all lines: 151, 174, 367, 405, 659, 761, 790, 795, 797, 799, 810, 1506, 2490, 2741); [src/ck3chronicle/db/schema.py:4](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:4) (all lines: 4, 42, 54, 105, 147, 210, 325, 342, 365, 410, 425, 442, 490); [src/ck3chronicle/harvester.py:1101](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:1101) (all lines: 1101, 1277); [src/ck3chronicle/ingest.py:68](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:68) (all lines: 68); [src/ck3chronicle/parser/service.py:143](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:143) (all lines: 143); [src/ck3chronicle/processing.py:294](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:294) (all lines: 294, 305, 307, 308, 445, 625, 711, 824, 833, 860, 1073); [src/ck3chronicle/reporting.py:26](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:26) (all lines: 26); [src/ck3chronicle/runtime_context.py:594](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:594) (all lines: 594); [src/ck3chronicle/session_intelligence.py:1](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:1) (all lines: 1, 120, 190, 577, 898, 922); [src/ck3chronicle/source_resolution.py:277](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:277) (all lines: 277); [src/ck3chronicle/triage.py:93](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:93) (all lines: 93); [tests/test_processing_recovery_requirements.py:330](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:330) (all lines: 330); [tools/template_learning/build_review_pack.py:255](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:255) (all lines: 255, 343, 377); [tools/template_learning/incremental_template_registry.py:123](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:123) (all lines: 123, 124, 125); [tools/template_learning/learn_error_templates.py:347](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:347) (all lines: 347, 348, 349) |
| `source_blocks` | [src/ck3chronicle/classification/service.py:91](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:91) (all lines: 91, 277); [src/ck3chronicle/cli.py:621](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:621) (all lines: 621, 717, 853, 1015); [src/ck3chronicle/database_audit.py:19](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:19) (all lines: 19, 194, 198, 217, 241, 245, 325, 461, 462, 500, 511, 707, 717, 726, 839); [src/ck3chronicle/db/migrations.py:84](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:84) (all lines: 84, 631, 660, 676, 693, 700, 740, 778, 863, 883, 884, 909); [src/ck3chronicle/db/repository.py:1073](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1073) (all lines: 1073, 1132, 1228, 1325, 1389, 1393, 1396, 1408, 1427, 1462, 1520, 1597, 1611, 1637, 1835, 2115, 2140, 2179, 2192, 2309, 2314, 2319, 2366, 2417, 2637, 2655, 2756, 2876); [src/ck3chronicle/db/schema.py:149](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:149) (all lines: 149, 272, 488, 506); [src/ck3chronicle/models/parse.py:40](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/parse.py:40) (all lines: 40, 50); [src/ck3chronicle/parser/service.py:176](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:176) (all lines: 176, 284, 290, 297, 306, 317, 337, 362, 384, 397); [src/ck3chronicle/processing.py:262](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:262) (all lines: 262, 280, 682); [src/ck3chronicle/reporting.py:172](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:172) (all lines: 172, 227, 264); [src/ck3chronicle/semantic_projection_service.py:105](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:105) (all lines: 105, 389, 409, 426); [src/ck3chronicle/session_intelligence.py:536](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:536) (all lines: 536, 539, 544, 558); [src/ck3chronicle/source_resolution.py:433](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:433) (all lines: 433); [src/ck3chronicle/triage.py:57](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:57) (all lines: 57); [tests/test_processing_recovery_requirements.py:264](C:/Users/nateb/Documents/ck3chronicle/tests/test_processing_recovery_requirements.py:264) (all lines: 264); [tools/evaluate_classifier.py:23](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:23) (all lines: 23, 29, 54, 80) |
| `source_file_instances` | [src/ck3chronicle/db/schema.py:457](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:457) (all lines: 457); [src/ck3chronicle/source_resolution.py:286](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:286) (all lines: 286, 370) |
| `source_resolution_observations` | [src/ck3chronicle/db/schema.py:441](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:441) (all lines: 441, 473); [src/ck3chronicle/source_resolution.py:276](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:276) (all lines: 276, 350) |

## CLI registration sites

| Source site | Registration expression |
|---|---|
| [src/ck3chronicle/cli.py:2406](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2406) | `sub.add_parser('capture')` |
| [src/ck3chronicle/cli.py:2411](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2411) | `p_capture.set_defaults(func=cmd_capture)` |
| [src/ck3chronicle/cli.py:2413](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2413) | `sub.add_parser('ingest')` |
| [src/ck3chronicle/cli.py:2421](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2421) | `p_ingest.set_defaults(func=cmd_ingest)` |
| [src/ck3chronicle/cli.py:2423](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2423) | `sub.add_parser('watch')` |
| [src/ck3chronicle/cli.py:2444](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2444) | `p_watch.set_defaults(func=cmd_watch)` |
| [src/ck3chronicle/cli.py:2446](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2446) | `sub.add_parser('reconcile')` |
| [src/ck3chronicle/cli.py:2450](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2450) | `p_reconcile.set_defaults(func=cmd_reconcile)` |
| [src/ck3chronicle/cli.py:2453](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2453) | `sub.add_parser('sessions')` |
| [src/ck3chronicle/cli.py:2455](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2455) | `p_sessions.set_defaults(func=cmd_sessions)` |
| [src/ck3chronicle/cli.py:2458](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2458) | `sub.add_parser('doctor')` |
| [src/ck3chronicle/cli.py:2459](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2459) | `p_doctor.set_defaults(func=cmd_doctor)` |
| [src/ck3chronicle/cli.py:2461](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2461) | `sub.add_parser('audit-db')` |
| [src/ck3chronicle/cli.py:2471](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2471) | `p_audit_db.set_defaults(func=cmd_audit_db)` |
| [src/ck3chronicle/cli.py:2473](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2473) | `sub.add_parser('observe-logging')` |
| [src/ck3chronicle/cli.py:2481](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2481) | `p_observe_logging.set_defaults(func=cmd_observe_logging)` |
| [src/ck3chronicle/cli.py:2484](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2484) | `sub.add_parser('parse')` |
| [src/ck3chronicle/cli.py:2500](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2500) | `p_parse.set_defaults(func=cmd_parse)` |
| [src/ck3chronicle/cli.py:2502](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2502) | `sub.add_parser('classify')` |
| [src/ck3chronicle/cli.py:2517](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2517) | `p_classify.set_defaults(func=cmd_classify)` |
| [src/ck3chronicle/cli.py:2519](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2519) | `sub.add_parser('review-queue')` |
| [src/ck3chronicle/cli.py:2538](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2538) | `p_review.set_defaults(func=cmd_review_queue)` |
| [src/ck3chronicle/cli.py:2540](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2540) | `sub.add_parser('report')` |
| [src/ck3chronicle/cli.py:2565](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2565) | `p_report.set_defaults(func=cmd_report)` |
| [src/ck3chronicle/cli.py:2567](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2567) | `sub.add_parser('latest')` |
| [src/ck3chronicle/cli.py:2579](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2579) | `p_latest.set_defaults(func=cmd_latest)` |
| [src/ck3chronicle/cli.py:2581](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2581) | `sub.add_parser('errors')` |
| [src/ck3chronicle/cli.py:2600](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2600) | `p_errors.set_defaults(func=cmd_errors)` |
| [src/ck3chronicle/cli.py:2602](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2602) | `sub.add_parser('process-pending')` |
| [src/ck3chronicle/cli.py:2623](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2623) | `p_process.set_defaults(func=cmd_process_one_pending)` |
| [src/ck3chronicle/cli.py:2625](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2625) | `sub.add_parser('backfill-session')` |
| [src/ck3chronicle/cli.py:2641](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2641) | `p_backfill.set_defaults(func=cmd_backfill_session)` |
| [src/ck3chronicle/cli.py:2643](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2643) | `sub.add_parser('compare')` |
| [src/ck3chronicle/cli.py:2668](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2668) | `p_compare.set_defaults(func=cmd_compare)` |
| [src/ck3chronicle/cli.py:2670](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2670) | `sub.add_parser('baseline')` |
| [src/ck3chronicle/cli.py:2675](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2675) | `baseline_sub.add_parser('create')` |
| [src/ck3chronicle/cli.py:2683](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2683) | `p_baseline_create.set_defaults(func=cmd_baseline_create)` |
| [src/ck3chronicle/cli.py:2684](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2684) | `baseline_sub.add_parser('list')` |
| [src/ck3chronicle/cli.py:2686](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2686) | `p_baseline_list.set_defaults(func=cmd_baseline_list)` |
| [src/ck3chronicle/cli.py:2687](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2687) | `baseline_sub.add_parser('delete')` |
| [src/ck3chronicle/cli.py:2692](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2692) | `p_baseline_delete.set_defaults(func=cmd_baseline_delete)` |
| [src/ck3chronicle/cli.py:2694](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2694) | `sub.add_parser('ignore')` |
| [src/ck3chronicle/cli.py:2699](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2699) | `ignore_sub.add_parser('add')` |
| [src/ck3chronicle/cli.py:2706](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2706) | `p_ignore_add.set_defaults(func=cmd_ignore_add)` |
| [src/ck3chronicle/cli.py:2707](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2707) | `ignore_sub.add_parser('list')` |
| [src/ck3chronicle/cli.py:2710](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2710) | `p_ignore_list.set_defaults(func=cmd_ignore_list)` |
| [src/ck3chronicle/cli.py:2711](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2711) | `ignore_sub.add_parser('remove')` |
| [src/ck3chronicle/cli.py:2717](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2717) | `p_ignore_remove.set_defaults(func=cmd_ignore_remove)` |
| [src/ck3chronicle/cli.py:2719](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2719) | `sub.add_parser('context')` |
| [src/ck3chronicle/cli.py:2730](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2730) | `p_context.set_defaults(func=cmd_context)` |
| [src/ck3chronicle/cli.py:2732](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2732) | `sub.add_parser('resolve-file')` |
| [src/ck3chronicle/cli.py:2739](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2739) | `p_resolve.set_defaults(func=cmd_resolve_file)` |
| [src/ck3chronicle/cli.py:2741](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2741) | `sub.add_parser('triage')` |
| [src/ck3chronicle/cli.py:2749](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:2749) | `p_triage.set_defaults(func=cmd_triage)` |

## Package resources and non-Python entry points

- [pyproject.toml:24](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:24): the console script imports `ck3chronicle.cli:main`; package data selects revision `67303093ecda779d`, including its projection catalog.
- [.github/workflows/ci.yml](C:/Users/nateb/Documents/ck3chronicle/.github/workflows/ci.yml): installation and existing source/test commands are downstream consumers of the package and imports. Their verification design is outside this planning task.
- [tools/migrate_legacy_pending_metadata.ps1](C:/Users/nateb/Documents/ck3chronicle/tools/migrate_legacy_pending_metadata.ps1): separate one-time pending-capture conversion tool; no role in canonical classification or fresh database generations.
- Model directories and documentation authority are inventoried in `DEPENDENCY_MAP.md`; historical evidence paths are not runtime code dependencies.

## Current same-file call chains and bounded integration

This supplements the imported-call index with exact current same-file calls.
Runtime matching moves under WORKPLAN R1–R7. Learning remains in its current
files; WORKPLAN L1–L5 enumerates only the offline lexer/dependency/tool-removal
edits. No learner, classifier or evaluator was
executed. Target outcome/shard definitions are in
[WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), sections 1.1–1.5.

| Current caller | Callee and current call lines | Responsibility / destination |
|---|---|---|
| [incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:147) `feature_from_log` 147–172 | `learn_error_templates.collect_records` at 148 | Offline evidence feature collection in the current learner file; only the lexer edge is reconnected under L1. |
| Same file `build_revision` 366–473 | `learn_error_templates.cluster_source_records` at 381 | Offline model building in the current registry; oracle dependency is removed under L4. |
| [learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1066) `cluster_source_records` 1066–1099 | `has_ordered_anchor_overlap` at 1079, `sequence_similarity` at 1081, `derive_template` at 1097 | Current offline learning algorithm; no relocation/rewrite. |
| Same file `derive_template` 1024–1063 | `choose_medoid` at 1026, `matching_pairs` at 1029, `infer_slot` at 1051 | Current offline template derivation. |
| Same file `choose_medoid` 956–972 | `sequence_similarity` at 965 | Current offline medoid selection. |
| Same file `infer_slot` 979–1021 | `_meaningful` at 987 | Current offline slot inference. |
| Same file `main` 1602–1682 | `collect_records` at 1610, `cluster_source_records` at 1613 | Current offline entry point; obsolete oracle call/report dependency removed under L3. |
| [classification/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:197) `classify_session` 100–312 | Runtime `classifier.classify_block` at 197 | Old production service is deleted; new pipeline/processor.py composes recovery and classification under N7. |
| [tools/evaluate_classifier.py](C:/Users/nateb/Documents/ck3chronicle/tools/evaluate_classifier.py:30) `evaluate` | Runtime `classifier.classify_block` at 30 | Separate coverage utility; disposition belongs to the deferred verification scope. |
| [build_semantic_projection_catalog.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:759) `main` | Runtime `classifier.classify_block` at 759 and 1201 | Obsolete caller deleted with the generator. Its runtime matching provider is ported under R7; the old provider file is then deleted. This is not the learner's model-build chain. |
| [classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:210) `Classifier.classify_block` 210–227 | `self.classify` at 226–227; `Classifier.classify` calls `validate_template_tokens` at 104 and 156 | R7 ports classify mechanics to pipeline/classifier.py. The old classify_block wrapper is not ported; explicit recovery/classification composition is new. No learning or model build occurs here. |

The named obsolete learner-file helpers `best_cluster` 1162–1181 and
`best_layered_cluster` 1184–1261 are called by the frozen oracle/review/unseen/
blind/miner utilities and by each other, not by the retained model-build call
chain above. Their shared similarity/anchor primitives at 916–1099 remain in the current
learner file because its clustering/derivation chain uses them. “Remove matching code” is not a valid deletion scope.
