# Agent Task 06B — Remove the deprecated processing stack

Owner-directed cleanup before Task 07, 2026-09-28.
Repository: `C:/Users/nateb/Documents/ck3chronicle`.

## Outcome

Disable unused CLI processing/reporting paths and physically remove their obsolete
providers, research-only dependency chains and redundant pipeline code. Leave the
working watcher/capture/playset producer and selected Task 05/06 pipeline intact.
Deliver the cleanup, not merely another audit or a future deletion list.
Perform it through a PowerShell cleanup script that first preserves the affected
working files in a portable temporary archive, with a standalone rollback script
and README. The owner will zip that folder and move it outside the repository.

The owner has authorized disabling unused CLI callers so they need not hold the
deprecated stack in place. A reference from another retired component does not
justify retention: remove the obsolete group together. A current required consumer
does require preserving its behavior, with an exact dependency recorded.

Keep `harvester.py` as the capture owner. The older workplan's C1/C2 relocation to
`pipeline/capture.py` and eventual whole-file deletion are superseded. Remove dead
archive/ingest mechanics from that module in place. Task 07 reuses its live helpers.
This task does not implement Task 07 or activate new processing commands.

## Read and establish scope

Read repository instructions, [status](PROJECT_STATUS.md), [plan](PROJECT_PLAN.md),
[current handoff](CURRENT_HANDOFF.md), [banned designs](BANNED_IDEAS.md) and
[development environment](DEVELOPMENT_ENVIRONMENT.md). Inspect:

- [Watcher delivery](WATCHER_ACTIVE_PLAYSET_HANDOFF.md) and
  [approved producer plan](WATCHER_ACTIVE_PLAYSET_IMPLEMENTATION_PLAN.md).
- [Watcher review, Section B: Legacy / Duplicate Watcher Assessment](../.codex-tmp/watcher-playset-review/REPORT.md#b-legacy--duplicate-watcher-assessment).
  Its early runtime snapshot and proposal sections predate the delivered producer
  and later live activation; use its retirement leads with current code.
- [Task 06 storage handoff](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md) and
  [v45 integration handoff](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md).
- [Task 07 prompt](TASK07_PROMPT.md) for required input helpers.
- [Earlier path audit](04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md) for leads only.

Inspect actual references, including imports inside functions, command registration,
packaging, tools and tests. Historical deletion lists and filenames alone are not
proof. Record a bounded entry baseline and exact file/symbol dispositions, then
execute the authorized cleanup without a second blanket approval checkpoint.

The watcher review found one lifecycle detector, not duplicate production watchers.
Its obsolete-code findings are incorporated below. Its earlier recommendation to
wait for processor cutover is superseded by the owner's authorization to disable
unused CLI paths and clean up before Task 07.

## Retained boundaries

Preserve these functioning components and their required dependencies:

- CLI `watch`, `capture`, `doctor`, `observe-logging`, ordinary help/version behavior,
  and `watch --once`. Keep the watcher's current defaults, events and exit behavior.
- `watcher.py`, `playset.py`, configuration/path ownership and logging observation.
- `harvester.spool_logs`, `write_playset_template`, pending types, capture exceptions,
  stable-copy helpers, inherited-directory-access helper and their exact closure.
  Preserve `include_debug`, `on_logs_copied`, crash attachment handling and callback
  publication/failure behavior. The watcher remains owner of extraction.
- Neutral input helpers used by Task 07: `FileIdentity`, `hash_file`,
  `_stable_identity`, `read_capture_metadata`, `selected_pending_path` and their
  dependencies. Keep these in `harvester.py`; document the surviving signatures.
- Selected `pipeline` catalog/model/classifier/raw-input/bindings/contracts,
  aggregation/review/schema/repository and their live domain types.
- The selected package/resources, current learner/parser/matcher/publication paths,
  and neutral command helpers still required by retained or planned consumers.

The live watcher is separately owner-authorized and may be running. Do not stop,
restart, reconfigure or use it for verification. Runtime evidence, pending captures,
logs, descriptors, databases and generated learner/review evidence are outside this
source-cleanup scope. Preserve immutable model packages and selection.

## Portable archive, scripted cleanup and rollback

Before the first cleanup edit or deletion, create a new task-owned ignored folder
such as `.codex-tmp/task06b-archive-<UTC timestamp>/`. Deliver this self-contained
layout, preserving repository-relative paths beneath the payload directory:

```text
task06b-archive-<timestamp>/
  README.md
  cleanup.ps1
  rollback.ps1
  changes.json
  before/<repository-relative paths>
  after/<repository-relative paths for edited/created files>
  TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md
```

`before/` must contain the exact current working bytes of **every file edited or
deleted**, including affected tests, tools and documentation, with uncommitted and
untracked content preserved. Git HEAD is not a substitute. Record created files
as having no prior file. Limit the archive to this cleanup's affected files;
exclude runtime evidence, credentials, databases and unrelated workspace contents.

Create and run `cleanup.ps1` using native PowerShell file operations. It must copy
and verify the complete pre-change payload before modifying any affected working
file, then apply the concrete reviewed replacements from `after/` and delete only
the enumerated retired files. Accept an explicit `-RepositoryRoot` and support
`-WhatIf` without changing files. Prepare replacement content outside the live source
tree. If another file enters the scope, archive its original before changing it.
The script must refuse to overwrite an existing archive or silently overwrite a
working file that changed since its captured baseline. On failure, stop and report
what was applied; the complete pre-change payload remains available for rollback.

`changes.json` records repository-relative paths, create/edit/delete actions,
pre-change and expected post-change SHA-256 values (or absence), and the actual
applied result. These hashes support correct backup/restore only. Keep all paths
inside the explicit repository/archive roots, reject traversal and reparse-point
escapes, and use `-LiteralPath`. Use an exact file list rather than recursive
deletion of a parent that might contain unrelated files. Keep the archive ignored
and outside package discovery/import paths; it is a backup, not a fallback provider.

`rollback.ps1` must work after the folder has been zipped, moved and extracted
elsewhere. Resolve its payload through `$PSScriptRoot`, accept an explicit
`-RepositoryRoot`, and require no original archive location, Git history, Python
environment or other local helper. Restore deleted files and pre-edit versions;
remove task-created files only when they still match the recorded cleanup version.
Recognize already-restored files. Preview changes with `-WhatIf`, preflight all
targets before applying them, and report conflicts with subsequent work instead
of overwriting or deleting it. Do not implement an automatic force overwrite.

The README must give exact copy/paste commands for cleanup preview/execution,
zipping or copying the whole archive folder, extracting it elsewhere, rollback
preview/execution against an explicitly selected checkout, and handling conflicts.
Explain that this restores the cleanup's affected files, not an entire repository,
environment or runtime dataset. Document PowerShell requirements and distinguish
restoring code from restarting services or enabling old commands. Include the final
cleanup handoff in the archive. Leave the completed folder in place for the owner
to back up; do not delete it during temporary-output cleanup or relocate it yourself.

## Disable retired CLI callers and remove their providers

Remove the old command registrations and handlers for:

`ingest`, `reconcile`, `sessions`, `audit-db`, `parse`, `classify`, `review-queue`,
`report`, `latest`, `errors`, `process-pending`, `backfill-session`, `compare`,
`baseline`, `ignore`, `context`, `resolve-file`, `triage`.

Remove helper functions/imports used only by those handlers. Their command names
may be reintroduced by the later new implementation. For now invocation must fail
clearly/nonzero through ordinary argument handling; no success stubs, old aliases
or fallback providers. Do not wire unfinished replacement commands.

Explicitly remove the unregistered `cli._cmd_process_pending_wide_legacy`, as named
by the watcher review, along with its exclusive formatting/result helpers. Retire
`processing.process_pending` and its guarded broad-finalization/reconciliation
branches with the old processor; leaving unreachable bodies retains the unwanted
implementation even after disabling its command.

Inspect shared error handlers: `_capture_error` currently imports
`db.repository.ExistingErrorLogHashError` even for retained capture failures.
Remove obsolete database-specific branches/imports while preserving valid capture
errors. Removing registrations alone would leave this hidden dependency broken.

With those callers removed, retire the following old product groups after checking
their actual dependency closure:

| Source path under `src/ck3chronicle/` | Disposition |
|---|---|
| `classification/`, `parser/`, `models/` | Delete old classification, extraction and issue/parse representations. This `models/` is the Python package, not repository model artifacts. |
| `db/` | Delete old schema, repository, migrations and payload handling. Retain the new `pipeline/schema.py` and `pipeline/repository.py`. |
| `semantic_projection.py`, `semantic_projection_service.py` | Delete obsolete interpretation stages. |
| `archive_registry.py`, `ingest.py`, `processing.py` | Delete old registration, ingest, journal and staged processing. |
| `reporting.py`, `database_audit.py` | Delete old-schema reporting/audit providers. |
| `runtime_context.py` | Delete historical extraction/reparse service after its retired callers are removed; the current watcher uses `playset.py`. |
| `session_intelligence.py`, `source_resolution.py`, `triage.py` | Delete old-schema downstream consumers with their disabled commands. |
| `pipeline/emissions.py`, `diagnostics.py`, `normalization.py` | Delete superseded recovery/normalization implementation with its obsolete research consumers. |
| `pipeline/domain.py` | Remove types/helpers used exclusively by deleted modules; preserve shared/live types such as `ByteSpan` and current storage results. |
| `harvester.py` | Retain and simplify in place; remove old bundle/archive/adoption/inspection/finalization machinery and unused types/constants. |

For harvester cleanup, trace `_inspect_pending`, `inspect_pending`,
`finalize_pending`, `finalize_pending_captures`, `read_snapshot`, `snapshot`,
archive-adoption/validation, bundle hashing and their exclusive helper/type closure.
Their rejection of `playset.json` is not a behavior to port. Preserve the capture
and Task 07 helper list above. No parallel capture module, relocation wrapper or
legacy folder is needed.

Apply the remaining watcher-review findings as follows:

- Remove `runtime_context.parse_debug_context`, `_analyze_debug_context`,
  `_typed_mounts` and `parse_runtime_context` with the retired module. The delivered
  `playset.py` is already the owner of current extraction; no port is required.
- Remove `source_resolution._recorded_roots` with its old consumer. It reconstructs
  a second root list from old DLC/mod tables; Task 07 receives the watcher list.
- Remove `parser/extractors/debug_log.py` and `DEBUG_EXTRACTORS` with the retired
  parser registry. These are old diagnostic extractors, not watcher functions.
- Remove the legacy importer-only `harvester.discover_crash_folder` if its current
  callers are all retired. Preserve watcher's lifecycle-associated crash inventory
  and root-exception capture.
- Check the report's unused `[migration].legacy_runtime_root` and
  `[evaluation].locked_public_corpus_root` against current consumers. Remove dead
  declarations from tracked examples/documentation when confirmed; do not modify
  local operational configuration or invent a replacement root.
- Historical six-log captures, receipts, `last_capture.json` and `crash_evidence`
  are retained data, not duplicate watcher source. Do not delete them. Unseen OS
  scheduler entries, external wrappers and inaccessible old runtimes are outside
  this repository cleanup; do not infer their obsolescence.

## Close research, test and packaging dependencies

Handle obsolete consumers as part of the deletion, not as reasons to keep obsolete
production behavior:

- Inspect `tools/evaluate_classifier.py`,
  `tools/template_learning/build_semantic_projection_catalog.py` and
  `build_parser_comparison.py`. Retire code exclusively evaluating/generating the
  removed stack. Preserve ignored historical output; do not build a new evaluator.
- Retire obsolete consumer-check sections in `inspect_cross_emission_recovery.py`
  and `tests/test_raw_parser_requirements.py` that call removed pipeline APIs.
  Preserve any independent current package checks.
- Inspect other affected tools/tests by actual imports and invocation. Delete tests
  exclusively asserting removed behavior; remove obsolete portions of mixed files.
  Maintain current required checks without adding compatibility aliases or taking
  test assertions as product requirements.
- Active learner implementation remains outside scope. Only retirement of obsolete
  research consumers/imports is authorized in its directory. Preserve current
  learner behavior, including `evaluate_unseen_session.py` where it uses the current
  shared matcher. If a live learner function truly needs redesign to release a
  dependency, name that precise blocker for its team and continue independent cleanup.
- Remove obsolete packaging/configuration references to deleted source only.
  Preserve the selected package and its shipped resources. Do not remove historical
  model artifacts or data merely because source consumers are retired.

Check `tools/migrate_legacy_pending_metadata.ps1` for retirement with the old archive
path; never execute it. Update affected ownership/usage documentation, including
AGENTS/README references where their named source boundaries are now removed.

## Verification

Use `.venv/Scripts/python.exe -I -B`. Verify retained imports, CLI help/registration
and clean rejection of removed commands. These checks must not start a watcher,
capture live logs, run `doctor` write probes or touch production storage.

On complete retained native evidence, exercise the surviving capture/playset path
against disposable copied sources and the selected classification/storage path in
a fresh disposable generation. Confirm the two-part review shard and database-only
rendering remain usable. Focus checks on changed boundaries; no full learner replay
campaign is required. Check current offline entry-point imports/help without
training or publishing models.

Use the watcher's documented native pair/template and Task 06 native inventory.
No synthetic logs, fabricated prepared data, mocks, artifact mutations or tests
used to determine requirements. Record gaps explicitly. Keep generated verification
under a task-owned ignored `.codex-tmp/` directory.

Verify no retained executable consumer imports a deleted module, including delayed
imports and packaged entry points. Inspect non-source artifacts separately; stale
build output must not masquerade as working source. Never recursively delete a
computed path before verifying its absolute target stays in task-owned scope.

Rehearse cleanup and rollback with copies of the actual affected files in a
disposable directory, never against the live checkout for the rollback exercise.
Copy/extract the archive to a different disposable location and run its rollback
there against the rehearsal checkout, proving it has no dependency on the original
archive path. Verify restoration of exact pre-change bytes and removal of recorded
task-created files. Use no fabricated log content. Record any unexercised conflict
or interruption branches without inventing a failure-injection campaign.

## Completion and Task 07 handoff

Create `docs/TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md` with exact deleted/edited
paths, disabled/retained commands, surviving harvester APIs, any genuine remaining
dependency with its owner, verification results/limits and entry/exit scope proof.
Include the exact archive directory, inventory, script commands and relocated
rollback rehearsal results so the owner can zip the complete recovery package.
Every retained candidate needs a concrete current consumer or named upcoming need;
historical references alone do not count. Do not invent completion if a real
dependency still blocks part of the deletion.

Update current status, plan, handoff, execution order, README and the Task 07 prompt
to reflect actual results. Carry forward completed Task 06 and watcher contracts.
Record which later retirement tasks are now discharged so they are not repeated.
Task 07 then implements protected inputs, playset receiving/storage and processing;
Task 08 implements reports/commands. Leave new application activation to its assigned
task. No commit, push, production processing or runtime-data deletion.
