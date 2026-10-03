# Task 06B — deprecated code cleanup handoff

Completed 2026-09-28. Task 07 is next; Task 08 implements commands/reports.
No Task 07 implementation, new command activation, commit or push is included.

## Delivered scope and recovery package

The cleanup removes 53 obsolete source/tool/test files and 53 associated ignored
bytecode files, edits 13 existing files, and creates this handoff (120 file actions).
Current working bytes, including pre-existing uncommitted and untracked content,
are preserved by the PowerShell cleanup before any affected working file changes.

Portable package: `C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/task06b-archive-20260928T074827Z`.
It contains `README.md`, `cleanup.ps1`, `rollback.ps1`, `changes.json`, exact
repository-relative `before/` and `after/` payloads, and a copy of this handoff.
`entry.json`, `symbols.json` and final `scope.json` supply bounded scope evidence.
`changes.json` records every action, before/after SHA-256 or absence, actual result
and actual resulting hash. These hashes serve recovery, not runtime provenance.
The folder is ignored by `.gitignore` and outside package/import discovery.
Leave it intact for the owner to zip and move; the README has portable commands.

```powershell
$archive = 'C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/task06b-archive-20260928T074827Z'
$repo = 'C:/Users/nateb/Documents/ck3chronicle'
# Initial cleanup preview/execution (already completed; not rerunnable):
& "$archive/cleanup.ps1" -RepositoryRoot $repo -WhatIf
& "$archive/cleanup.ps1" -RepositoryRoot $repo
# Recovery preview/execution, only when the owner chooses to restore:
& "$archive/rollback.ps1" -RepositoryRoot $repo -WhatIf
& "$archive/rollback.ps1" -RepositoryRoot $repo
```

Cleanup refuses an existing `before/` archive and changed working baselines.
Both scripts constrain relative paths, reject reparse-point ancestors/traversal,
use literal file operations, and never recursively delete a source directory.
Only enumerated empty obsolete package directories are removed. Unexpected files
prevent directory removal. Rollback preflights all files before writing, recognizes
already-restored bytes, and refuses conflicts with subsequent work. There is no force
overwrite. The portable scripts require PowerShell 7+, no Python or Git.

## Commands and provider boundary

Retained: `watch`, `capture`, `doctor`, `observe-logging`, root/subcommand help,
the package version `0.0.1`, and `watch --once`. The entry baseline has no CLI
`--version` registration; its ordinary argparse rejection remains unchanged.
Watch defaults remain `ck3.exe`, 0.5-second polling and 30-second heartbeat;
observer defaults remain 2/30 seconds. No handlers were executed for verification.

Removed registrations and handlers: `ingest`, `reconcile`, `sessions`, `audit-db`,
`parse`, `classify`, `review-queue`, `report`, `latest`, `errors`, `process-pending`,
`backfill-session`, `compare`, `baseline`, `ignore`, `context`, `resolve-file`,
`triage`. All now return argparse exit 2 with invalid-choice errors, without aliases
or success stubs. `_cmd_process_pending_wide_legacy` and its exclusive result/format
helpers are gone. Deleting `processing.py` also deletes the unreachable guarded
broad-finalization/reconciliation bodies. `_capture_error` no longer imports SQLite
or the old repository; valid capture error exits (2, 3, generic 1) remain.

`watcher.py`, `playset.py`, config/path ownership and logging observation are
unchanged. Retained watcher/capture/doctor/observer handlers and spool helpers are
AST-identical to entry. There is still one lifecycle detector. Crash inventory,
root-exception handling, callback timing, paired-log publication and expected
template-failure behavior remain with their existing owners. No `pipeline/capture.py`,
legacy wrapper or fallback provider was created.

## Surviving harvester signatures and exact reasons

```python
def _make_inheriting_staging_directory(parent: Path, prefix: str) -> Path: ...
def discover_logs(root: Path) -> list[Path]: ...
def spool_logs(logs_root: Path, dest_root: Path, *, abort_if: Callable[[], bool] | None=None, capture_metadata: dict[str, Any] | None=None, crash_folder: Path | None=None, include_debug: bool=False, on_logs_copied: Callable[[Path, str, str], None] | None=None) -> PendingCapture: ...
def write_playset_template(directory: Path, *, captured_at: str, members: tuple[PlaysetMember, ...]) -> PlaysetTemplate: ...
def hash_file(path: Path) -> str: ...
def _stable_identity(path: Path) -> FileIdentity: ...
def _copy_exact(src: Path, dst: Path) -> None: ...
def _copy_stable_without_hash(src: Path, dst: Path) -> os.stat_result: ...
def read_capture_metadata(directory: Path) -> dict[str, Any] | None: ...
def _load_manifest(directory: Path) -> tuple[dict[str, Any], str]: ...
def selected_pending_path(dest_root: Path, pending_name: str) -> Path: ...
```

- `spool_logs` is called by `cli._spool_once`, serving watch/capture/once. It owns
  `PendingCapture`, `PendingFileStat`, `discover_logs`, `LOG_NAMES`,
  `CAPTURE_METADATA_NAME`, `_make_inheriting_staging_directory`,
  `_copy_stable_without_hash` and `_copy_exact`. `CaptureError`,
  `InvalidCaptureInput`, `UnstableCapture` support this closure and watcher errors.
- `cli.cmd_watch` calls `write_playset_template`; it calls `hash_file` and uses
  `playset.PlaysetMember`, `PlaysetTemplate`, `PLAYSET_FILENAME`. `include_debug`
  and `on_logs_copied` signatures and bodies are unchanged.
- Task 07 explicitly needs `FileIdentity(bytes, mtime_ns, sha256)`, `hash_file`,
  `_stable_identity`, `read_capture_metadata` and `selected_pending_path`.
  `read_capture_metadata` still reads `manifest.json` via `_load_manifest`, returning
  its `capture_metadata` dict or None. Thus `_load_manifest`, `MANIFEST_NAME` and
  `ArchiveIntegrityError` are an exact retained dependency, not the removed archive
  inspection/adoption/finalization service. It does **not** read the watcher's
  `capture-metadata.json`; Task 07 implements current input JSON receiving.
  `selected_pending_path` also raises `ArchiveIntegrityError`. Its existing checks
  reject hidden/traversing names, missing directories and direct symlinks; additional
  receiver containment policy belongs to Task 07.
- `command_envelope.command_envelope` is retained as the neutral response builder
  for upcoming Task 08 command handlers; `_emit_command_json` was CLI-only retired
  formatting and is removed. Config's existing path helpers serve retained commands
  and the explicit Task 07 path-ownership requirement.

The selected `pipeline` catalog/model/classifier/raw-input/bindings/contracts,
aggregation/review/schema/repository remain. `domain.ByteSpan`, `OriginalAccess`,
`ResultIntegrityError`, native assignment/review types and all Task 06 storage
results remain with their actual current consumers. Historical framing/view types
and their only old comparison consumer are removed together.

## Exact source dispositions

Deleted files (all contained symbols retire with each file):

- `src/ck3chronicle/archive_registry.py`
- `src/ck3chronicle/classification/__init__.py`
- `src/ck3chronicle/classification/catalog.py`
- `src/ck3chronicle/classification/contracts.py`
- `src/ck3chronicle/classification/inference.py`
- `src/ck3chronicle/classification/model.py`
- `src/ck3chronicle/classification/normalize.py`
- `src/ck3chronicle/classification/projection_catalog.py`
- `src/ck3chronicle/classification/service.py`
- `src/ck3chronicle/database_audit.py`
- `src/ck3chronicle/db/__init__.py`
- `src/ck3chronicle/db/migrations.py`
- `src/ck3chronicle/db/payloads.py`
- `src/ck3chronicle/db/repository.py`
- `src/ck3chronicle/db/schema.py`
- `src/ck3chronicle/ingest.py`
- `src/ck3chronicle/models/__init__.py`
- `src/ck3chronicle/models/issue.py`
- `src/ck3chronicle/models/parse.py`
- `src/ck3chronicle/parser/__init__.py`
- `src/ck3chronicle/parser/extractors/__init__.py`
- `src/ck3chronicle/parser/extractors/asset_graphics.py`
- `src/ck3chronicle/parser/extractors/culture_faith.py`
- `src/ck3chronicle/parser/extractors/database_reference.py`
- `src/ck3chronicle/parser/extractors/debug_log.py`
- `src/ck3chronicle/parser/extractors/descriptor.py`
- `src/ck3chronicle/parser/extractors/event_system.py`
- `src/ck3chronicle/parser/extractors/gui_interface.py`
- `src/ck3chronicle/parser/extractors/history_setup.py`
- `src/ck3chronicle/parser/extractors/localization.py`
- `src/ck3chronicle/parser/extractors/persistent_reader.py`
- `src/ck3chronicle/parser/extractors/script_hygiene.py`
- `src/ck3chronicle/parser/extractors/script_system.py`
- `src/ck3chronicle/parser/extractors/unclassified.py`
- `src/ck3chronicle/parser/log_blocks.py`
- `src/ck3chronicle/parser/normalize.py`
- `src/ck3chronicle/parser/service.py`
- `src/ck3chronicle/pipeline/diagnostics.py`
- `src/ck3chronicle/pipeline/emissions.py`
- `src/ck3chronicle/pipeline/normalization.py`
- `src/ck3chronicle/processing.py`
- `src/ck3chronicle/reporting.py`
- `src/ck3chronicle/runtime_context.py`
- `src/ck3chronicle/semantic_projection.py`
- `src/ck3chronicle/semantic_projection_service.py`
- `src/ck3chronicle/session_intelligence.py`
- `src/ck3chronicle/source_resolution.py`
- `src/ck3chronicle/triage.py`
- `tests/test_processing_recovery_requirements.py`
- `tools/evaluate_classifier.py`
- `tools/migrate_legacy_pending_metadata.ps1`
- `tools/template_learning/build_parser_comparison.py`
- `tools/template_learning/build_semantic_projection_catalog.py`

Edited files:

- `AGENTS.md`
- `README.md`
- `docs/TASK07_PROMPT.md`
- `docs/CURRENT_HANDOFF.md`
- `docs/PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md`
- `docs/PROJECT_PLAN.md`
- `docs/PROJECT_STATUS.md`
- `src/ck3chronicle/cli.py`
- `src/ck3chronicle/harvester.py`
- `src/ck3chronicle/pipeline/domain.py`
- `tests/test_raw_parser_requirements.py`
- `tools/template_learning/AGENTS.md`
- `tools/template_learning/inspect_cross_emission_recovery.py`

Created: `docs/TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md`. No prior file existed.
The three code-file symbol inventories below are exhaustive for removed top-level
functions/types/constants; all their retained signatures/bodies are in `after/`.

### `src/ck3chronicle/cli.py`

Removed: `_capture_once`, `_print_capture_result`, `_emit_command_json`, `cmd_ingest`, `cmd_reconcile`, `cmd_sessions`, `cmd_audit_db`, `_log_type_from_relpath`, `cmd_parse`, `cmd_classify`, `cmd_review_queue`, `_report_for_args`, `_print_executive_report`, `_cmd_report`, `cmd_report`, `cmd_latest`, `cmd_errors`, `_cmd_process_pending_wide_legacy`, `_selected_processing_root`, `_show_read_only_plan`, `_processing_failure`, `cmd_process_one_pending`, `cmd_backfill_session`, `_print_session_comparison`, `cmd_compare`, `_latest_session_and_model`, `cmd_baseline_create`, `cmd_baseline_list`, `cmd_baseline_delete`, `_policy_model`, `cmd_ignore_add`, `cmd_ignore_list`, `cmd_ignore_remove`, `cmd_context`, `cmd_resolve_file`, `cmd_triage`.

### `src/ck3chronicle/harvester.py`

Removed: `LEGACY_LOG_NAMES`, `LEGACY_PRINCIPAL_LOG_NAMES`, `PRINCIPAL_LOG_NAMES`, `LEGACY_MANIFEST_VERSION`, `PREVIOUS_LIVE_MANIFEST_VERSION`, `MANIFEST_VERSION`, `SUPPORTED_MANIFEST_VERSIONS`, `BUNDLE_HASH_ALGORITHM`, `LIVE_SESSION_HASH_ALGORITHM`, `EvidenceSource`, `CapturedFile`, `EvidenceBundle`, `SnapshotResult`, `PendingInspection`, `discover_crash_folder`, `_source_entries`, `_identity_key`, `_bundle_hash`, `_live_session_hash`, `_compute_bundle_hash`, `build_bundle`, `_manifest_payload`, `_principal_names`, `_write_manifest`, `_manifest_bytes`, `_publish_manifest_atomic`, `_files_from_manifest`, `_manifest_identity`, `validate_snapshot`, `snapshot_file_metadata_matches_manifest`, `snapshot_manifest_projection`, `_evidence_descriptor`, `_existing_snapshot_result`, `read_snapshot`, `_pending_captured_at`, `_inspect_pending`, `inspect_pending`, `finalize_pending`, `finalize_pending_captures`, `adopt_legacy_archive`, `_adopt_legacy_snapshot`, `snapshot`.

### `src/ck3chronicle/pipeline/domain.py`

Removed: `TokenSpan`, `SourceProvenance`, `Emission`, `EvidenceScope`, `EvidenceSpan`, `OccurrenceValue`, `RecoveredDiagnostic`, `MatchingToken`, `NormalizedValue`, `NormalizedView`.

The CLI retains `build_parser` and `main` but edits registrations/error mapping;
other retained handlers are unchanged. The raw-parser test loses only
`test_independent_pipeline_replay` and its unused imports (the removed read_raw_log
API); all independent parser/learner checks remain. `inspect_cross_emission_recovery`
loses only the obsolete pipeline iter_diagnostics/bind_captures/Capture consumer
section and its output claims; independent parser and learner feature checks remain.
`evaluate_unseen_session` and all current learner/parser/matcher/publication behavior
are unchanged. No learner redesign blocker was found.

The migration utility was inspected and deleted without execution. Searches found
no tracked declaration or executable consumer of `[migration].legacy_runtime_root`
or `[evaluation].locked_public_corpus_root`; there was nothing tracked to remove.
Local operational configuration was not edited. `pyproject.toml` has no removed
module-specific dependency; its console entry and selected package resource list
remain correct and unchanged. Historical model artifacts remain untouched.

### Exact obsolete bytecode deletions

- `src/ck3chronicle/__pycache__/archive_registry.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/database_audit.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/ingest.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/processing.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/reporting.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/runtime_context.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/semantic_projection.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/semantic_projection_service.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/session_intelligence.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/source_resolution.cpython-312.pyc`
- `src/ck3chronicle/__pycache__/triage.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/__init__.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/catalog.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/contracts.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/inference.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/model.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/normalize.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/projection_catalog.cpython-312.pyc`
- `src/ck3chronicle/classification/__pycache__/service.cpython-312.pyc`
- `src/ck3chronicle/db/__pycache__/__init__.cpython-312.pyc`
- `src/ck3chronicle/db/__pycache__/migrations.cpython-312.pyc`
- `src/ck3chronicle/db/__pycache__/payloads.cpython-312.pyc`
- `src/ck3chronicle/db/__pycache__/repository.cpython-312.pyc`
- `src/ck3chronicle/db/__pycache__/schema.cpython-312.pyc`
- `src/ck3chronicle/models/__pycache__/__init__.cpython-312.pyc`
- `src/ck3chronicle/models/__pycache__/issue.cpython-312.pyc`
- `src/ck3chronicle/models/__pycache__/parse.cpython-312.pyc`
- `src/ck3chronicle/parser/__pycache__/__init__.cpython-312.pyc`
- `src/ck3chronicle/parser/__pycache__/log_blocks.cpython-312.pyc`
- `src/ck3chronicle/parser/__pycache__/normalize.cpython-312.pyc`
- `src/ck3chronicle/parser/__pycache__/service.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/__init__.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/asset_graphics.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/culture_faith.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/database_reference.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/debug_log.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/descriptor.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/event_system.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/gui_interface.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/history_setup.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/localization.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/persistent_reader.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/script_hygiene.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/script_system.cpython-312.pyc`
- `src/ck3chronicle/parser/extractors/__pycache__/unclassified.cpython-312.pyc`
- `src/ck3chronicle/pipeline/__pycache__/diagnostics.cpython-312.pyc`
- `src/ck3chronicle/pipeline/__pycache__/emissions.cpython-312.pyc`
- `src/ck3chronicle/pipeline/__pycache__/normalization.cpython-312.pyc`
- `tests/__pycache__/test_processing_recovery_requirements.cpython-312-pytest-9.1.0.pyc`
- `tests/__pycache__/test_processing_recovery_requirements.cpython-312.pyc`
- `tools/__pycache__/evaluate_classifier.cpython-312.pyc`
- `tools/template_learning/__pycache__/build_parser_comparison.cpython-312.pyc`
- `tools/template_learning/__pycache__/build_semantic_projection_catalog.cpython-312.pyc`

These ignored non-source artifacts are individually archived and deleted so old
cache directories do not survive as namespace packages. Existing `build/`, egg-info,
other old verification installations and ignored reports are historical artifacts,
not source/import evidence. They were not deleted. The verified wheel was built
offline from a fresh source staging tree; it contains no retired product packages
or deleted research generators and keeps selected resources.

## Verification and limits

All Python execution uses `.venv/Scripts/python.exe -I -B`. Verification lives in
`.codex-tmp/task06b-verification/`; orchestration scripts are adjacent task-owned
`.codex-tmp/task06b-*.py` files. No production paths were used as destinations.

- Retained source and learner module imports, syntax compilation, delayed import
  AST scan, command registration/help and all 18 retired-command rejections pass.
  Root/subcommand help does not call watch, capture, doctor or observer handlers.
  Retained handler/helper AST comparisons prove unchanged bodies, including
  `cmd_watch` callback failure/event handling. Capture-error mappings pass.
- Copied the complete documented watcher pair from
  `.codex-tmp/watcher-playset-implementation/runtime/pending/20260928T044454.938004Z-OLveBBJL/`.
  Disposable paired capture copied exact bytes; callback saw both logs and metadata
  before publication. Current extraction and writing reproduce the original 133
  ordered members, zero warnings, both hashes and joined ID. Default capture is
  error-only. A genuinely absent source fails without creating a destination.
- Two complete Task 06 v45 inventory logs (hash prefixes `9d3622ab` and `f5ca3538`)
  were copied to `native2/storage-sources/` and processed in a fresh `task06b`
  generation: 46,773 recovered occurrences, 4,162 records, and one review emission.
  Both statuses occur. SQL values/definitions/counts match prepared records; review
  bytes equal original emissions in order. Both completed shard files exist for
  empty and nonempty review. This is a bounded cleanup check, not a learner replay.
- A separate process reopened SQL read-only and rendered all 4,162 records using
  stored definitions/values, with parser/model/learner imports and log/model/template/
  manifest reads blocked. Database bytes stayed unchanged.
- Fresh offline wheel build/install passes installed CLI help, selected package
  loading using its explicitly supplied installed resource root, and eight offline
  entry-point help checks: evaluate_unseen_session, incremental_template_registry,
  publish_native_model, inspect_raw_parse, inspect_native_learner,
  verify_shared_matcher, verify_matcher_package, inspect_cross_emission_recovery.
  No training or model publication ran.
- Final cleanup/rollback rehearsal uses actual affected working files, including
  ignored caches and the newly created handoff. Cleanup preview leaves files
  untouched. The completed recovery folder is copied to a different disposable
  location; rollback there preflights and restores the rehearsal checkout exactly,
  removes the created handoff, then recognizes an already-restored checkout.
  Preview leaves it unchanged. Exact hashes/absence reconcile for every action.

Initial verification orchestration corrections were confined to ignored scripts:
UTF-8 reading for the Unicode template, JSON tuple/list normalization for comparison,
and explicit models_root for a pip --target installation. They required no product
changes. The first staged parser filtering pass exposed dependent argument-group
statements; these were removed before final rehearsal or live cleanup.

No fabricated logs/prepared records, mocks, artifact mutation, broad learner campaign
or historical test expectations defined verification. Existing synthetic watcher
unit tests remain but were not executed for this assignment. Crash attachment error,
actual live lifecycle, sudden interruption/power loss, script conflict/reparse refusal
branches and concurrent file-change races were inspected, not failure-injected.
The initial abandoned rehearsal archive remains separate from the final archive;
only the final relocated rehearsal is the recovery proof. Previously documented
Task 06 native/model limitations remain unchanged. No universal model claim is made.

## Entry/exit proof and next owner

`entry.json` records HEAD and hashes of Git-visible files (tracked and untracked,
excluding runtime/ignored data), including entry-absent tracked paths. The action
inventory additionally captures only the affected ignored bytecode. `scope.json`
records the final path/hash comparison and action outcomes. No unrelated source,
selected immutable package, selection, runtime data, descriptor, database, capture
receipt or pending evidence was changed. The working watcher was not stopped,
restarted, reconfigured or used for verification. No Git stage/commit/push occurred.

Task 06B discharges old provider retirement, old archive inspector/finalizer removal,
obsolete parser comparison/projection/evaluation consumers, obsolete raw-input/binding
consumer checks, debug extractors and legacy metadata migration utility retirement.
C1/C2 capture relocation/whole-file deletion is superseded; keep `harvester.py`.
Task 07 consumes these surviving APIs and the completed watcher/Task 06 contracts;
it implements protected-input/playset receiving, Run-owned storage and replay APIs.
Task 08 implements command/report handlers. New application activation remains its
assigned task. Learner policy and Script location-stack investigation remain separate.
