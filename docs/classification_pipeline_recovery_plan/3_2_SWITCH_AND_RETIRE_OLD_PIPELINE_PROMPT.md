# Mini-project 3.2 — Switch application callers and retire the old pipeline

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the Stage 3 coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_3_APPLICATION_SWITCH_ORCHESTRATOR_PROMPT.md).
This is the connected source activation and retirement handoff for owner review.

## Outcome and entry

Require completed 1.1–3.1 handoffs: direct interfaces/model, recovery/classifier,
complete Run/review storage, common processor/replay and new read/command handlers.
Connect those implementations to the application and delete the exact old
providers and tools below in the same mini-project.

Read WORKPLAN 6–8, [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and [CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md)
as the complete dependency closure. Read the current repository and nested
offline-tool AGENTS instructions before editing their files.

Require the separate verification task's concrete disposition for the evaluator,
tests and CI consumers named in WORKPLAN 8.1 before declaring the entire
implementation complete. They do not justify retaining old APIs and are not
silently deleted under this prompt.

## Exact mutation scope

Create: none.

Edit only the following existing files, within the stated changes. The new
pipeline files and direct artifact already belong to 1.1–3.1; corrections
return to the owning mini-project with its own baseline and scope proof.

| Mini-project | Exact existing file | Permitted change |
|---|---|---|
| 3.2 | [tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35) | Only the lexer/type/call reconnection and obsolete-tool removal edits enumerated in WORKPLAN 3.2 and the bounded offline-tool section below. |
| 3.2 | [tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:366) | Remove frozen-oracle build dependency/argument and associated evaluation output, as enumerated in WORKPLAN 3.2 and the bounded offline-tool section below. |
| 3.2 | [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md:1) | Update the tool inventory for the actual remaining files. |
| 3.2 | [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md:1) | Update obsolete tool ownership/reporting references; retain the existing learner location and candidate/promotion boundary. |
| 3.2 | [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:11) | Exact handler removals and new command/capture registrations in WORKPLAN 6.1 and the application-connection section below. |
| 3.2 | [src/ck3chronicle/watcher.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:17) | Capture-error import at 17–20. |
| 3.2 | [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:12) | Remove unreachable old-Python import fallback at 12–15. |
| 3.2 | [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) | Selected model package data at 29–34. |
| 3.2 | [models/README.md](C:/Users/nateb/Documents/ck3chronicle/models/README.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/DATA_COMPATIBILITY_AND_OPERATIONS.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATA_COMPATIBILITY_AND_OPERATIONS.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/MODEL_QUALITY_AND_PROMOTION.md](C:/Users/nateb/Documents/ck3chronicle/docs/MODEL_QUALITY_AND_PROMOTION.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/REPOSITORY_AND_BACKUP.md](C:/Users/nateb/Documents/ck3chronicle/docs/REPOSITORY_AND_BACKUP.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/WORKSPACE_ROUTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/WORKSPACE_ROUTING.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [README.md](C:/Users/nateb/Documents/ck3chronicle/README.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |

The next three lists are the complete deletion scope. They authorize deletion
of these source/artifact files, not recursive removal of a guessed directory.
Resolve the exact paths inside the checkout before deleting them and preserve
pre-existing owner changes in the recoverable source baseline.

### Delete obsolete offline tools

- [tools/template_learning/analyze_script_system_layers.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/analyze_script_system_layers.py:1) — entire file, 1–131.
- [tools/template_learning/blind_review/build_blind_stratified_sample.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:1) — entire file, 1–336.
- [tools/template_learning/blind_review/compare_blind_adjudication.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/compare_blind_adjudication.py:1) — entire file, 1–279.
- [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:1) — entire file, 1–376.
- [tools/template_learning/build_review_pack.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:1) — entire file, 1–446.
- [tools/template_learning/build_semantic_projection_catalog.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:1) — entire file, 1–1268.
- [tools/template_learning/evaluate_unseen_session.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:1) — entire file, 1–408.
- [tools/template_learning/mine_symbol_suffixes.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:1) — entire file, 1–273.

### Delete superseded product providers and converter

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

### Delete superseded active model files

- [models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1) — 1–1.
- [models/67303093ecda779d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/manifest.json:1) — 1–1.
- [models/67303093ecda779d/semantic_projection_catalog.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/semantic_projection_catalog.json:1) — 1–14082.
- [models/93196794a7e0115d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/93196794a7e0115d/empirical_template_model.json:1) — 1–1.
- [models/93196794a7e0115d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/93196794a7e0115d/manifest.json:1) — 1–1.

No runtime originals, review evidence, learner evidence/cache or databases are
included in these deletion lists. The old model content remains in existing Git
history; this task does not create a partial old revision or archive/export copy.

## Exact application connections

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



## Bounded offline-tool edits

These are dependency and obsolete-tool removal edits, not a learner rebuild.
The algorithm remains in
[tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:916) 916–1099 and
the evidence registry in
[tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:44).
A later learner relocation/reorganization under `src/` is separate work.

| ID | Exact existing file/function/call | Required edit and reason |
|---|---|---|
| L1 | [tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35): import 35; `block_message` type annotation at 719; `collect_records` 1102–1159, lexer call 1108 | Reconnect to new `pipeline.domain.Emission` / `pipeline.emissions.iter_emissions`, adapting the precise field accesses if N1 requires it. The old lexer module is retired in 3.2. This is an offline consumer of the lexer, not a production call to the learner. |
| L2 | Same file: `LayeredClusterMatch` 309–333; evaluator-only `template_fixed_semantics_are_ordered` 806–844; unused `constant_tokens` 912–913; evaluator helpers 1162–1323; `evaluate_frozen_oracle` 1326–1482 | Remove code belonging to the obsolete tools listed in WORKPLAN 6.2 and this prompt's deletion list. The learning call chain `cluster_source_records -> derive_template -> choose_medoid/matching_pairs/infer_slot` uses the separate helpers at 916–1099 and continues in its existing file. |
| L3 | Same file: `write_report` 1533–1571; `parse_args` 1574–1599; `main` 1602–1682, oracle call 1630 | Remove mandatory oracle execution/arguments and its report/model evaluation fields so deleting the old tool chain does not break ordinary offline authoring. |
| L4 | [tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:366): `build_revision` 366–473, oracle call 390/evaluation field 433; `parse_args` 500–526, option 520; `main` 529–540, forwarding 536 | Remove this same mandatory oracle dependency. Keep selected-evidence clustering/provenance and immutable candidate production. |
| L5 | [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md:1); [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md:1) | Update the concrete remaining tool inventory and commands, including the old instruction to produce evaluator-style assignment counts in AGENTS.md 15–16. |

Production uses an already approved artifact. The current structural candidate
format and a complete approved direct-contract artifact are different product
units (owner intent 97–98; architecture 206–211). This project supplies the
current direct artifact in WORKPLAN section 7; it does not rebuild automatic learner
promotion or claim that a future candidate can be loaded without review.

Future candidate promotion must reconcile normalization version, structure and
the approved direct-contract fields. That producer/consumer interface remains
explicit; a new learner algorithm, unified normalization rewrite, source-folder
relocation or training campaign is not a prerequisite for constructing the
production pipeline from the existing selected structures.



## Model and package activation

Use the actual direct model/manifest paths and hashes from 1.3. The new catalog
already pins that revision and shares the normalizer identity. Switch
`pyproject.toml` package data at 29–34 to those exact two files while the CLI
begins using the new package.

Remove all five old artifact files listed above and all projection loader/
service/generator files in the deletion scope. Source and installed-package
selection must agree on the same direct revision. No loader accepts the old
pair as a secondary format, and no runtime path converts old data.

## Ordered implementation

1. Read the actual completed source handoffs together and reconcile every
   required caller against WORKPLAN 6.1. A missing implementation returns to
   its named owner; this prompt's edit list is not permission to finish
   arbitrary files in the new package.
2. Make the bounded L1–L5 edits and the exact CLI/watcher/config/package changes.
   The old learner lexer call reconnects to the actual new emission interface.
   Keep its clustering/derivation algorithm and evidence registry in their
   existing files.
3. Delete each explicitly named obsolete tool, provider, converter and old
   artifact after its required behavior has the named destination. Delete the
   obsolete command/helper registrations and their bodies completely.
4. Reconcile the import, same-file caller, table and resource map against the
   resulting source. Required product callers point to the new package;
   unsupported chains have their explicit deletion. Historical source
   references in this plan are evidence, not reasons to retain providers.
5. Apply the exact documentation updates below using implemented facts only.
   Report the separate evaluator/tests/CI disposition under its own approved
   scope; do not silently classify those known consumers as finished.
6. Supply the entry-to-exit path comparison for all creations, edits and
   deletions, including untracked/ignored state. If another task changed a
   file during this work, identify that change separately rather than claiming
   it as this mini-project's permitted edit.

## Scoped documentation updates

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

The documentation table's authority/background rows are read inputs, not
additional mutation permissions. The explicit edit table above controls.

## Deliverable

Report the actual supported commands and their sole current service paths;
selected direct revision and package resources; all source/tool/artifact
deletions; precise offline changes; and the remaining separate verification
status. Account for each dependency-map finding and each allowed file.

The source switch does not itself run a capture, build a production generation,
replay retained logs, replace the active database, commit or publish changes.
Finish with the required file-scope proof. Declare the overall implementation
complete only when the commissioned source work and separately supplied
verification-consumer disposition are actually complete.
