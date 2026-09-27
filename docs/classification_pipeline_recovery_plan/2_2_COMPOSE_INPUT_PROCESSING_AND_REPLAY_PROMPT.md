# Mini-project 2.2 — Compose protected inputs, processing and replay

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`high`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the stage coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_2_RUN_PROCESSING_ORCHESTRATOR_PROMPT.md).
This is an implementation handoff prepared for owner review.

## Outcome and entry

Compose protected pending input, explicit manual input and fresh-generation
replay through one `process_input`. Consume Stage 1's recovery/classifier and
2.1's aggregation, review and repository handoff.

Capture means a stable protected copy before classification or database
processing. WORKPLAN 1.5, C1/C2, N3/N7 and the canonical source definitions govern
this boundary.

## Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/capture.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/processor.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/replay.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/playset.py`

Edit: none. Delete: none.

Record the entry baseline and finish with the master's changed-file scope
proof. A needed change to a preceding file returns to its owning mini-project
before dependent work continues. Runtime evidence output is implemented here;
writing actual evidence or databases is a separate operational action.

## Exact source ports

| ID | Existing source and scope | Destination and treatment |
|---|---|---|
| C1 | [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:37): capture exceptions 37–50; `PendingFileStat` 112–118; `PendingCapture` 121–129; `_make_inheriting_staging_directory` 148–164; `discover_logs` 167–176; `spool_logs` 179–342; `_copy_exact` 475–481; `_copy_stable_without_hash` 484–496 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/capture.py`: port copy-only behavior and the exact helper/type closure. Keep current capture metadata and watcher abort callback; required error.log precedes optional associated crash evidence. No database/model/learner imports. Port the relevant constants for current error-log/capture metadata, not `LEGACY_LOG_NAMES`. |
| C2 | Same [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:364): `FileIdentity` 53–57; `hash_file` 364–370; `_stable_identity` 402–412; `read_capture_metadata` 552–556; `_manifest_bytes` 569–572; `_load_manifest` 602–611; `selected_pending_path` 920–937 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py`: port hashing, explicit path selection and JSON read/serialization primitives. Write current input inspection/protection interfaces under N3. Do not port `_inspect_pending` 940–1058, `finalize_pending` 1067–1150, `read_snapshot` 881–906 or their old-format/result machinery. |
| F1 | [src/ck3chronicle/runtime_context.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:25): `MountedDlc` 25–32; `MountedMod` 35–43; inventory/mount regex 73–91; path/key helpers 94–136; `_BlockCandidate` 139–181; `_ContextAnalysis` 184–202; `_typed_mounts` 205–271; `_analyze_debug_context` 274–453 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/playset.py`: port this pure extraction kernel as `analyze_debug_context`, with its types/constants. Do not port `parse_debug_context` 456–481: it is an old compatibility wrapper over the analyzer. No repository import, stored-result reconstruction or context reparse service. This preserves the approved same-Run playset fast-follow's working grammar; it is not added to `process_input` in this recovery. |

## New interfaces and old-body boundaries

| New function/type | Required behavior |
|---|---|
| `inputs.PreparedInput` | Explicit protected source, complete hash, supported capture facts and truthful unavailable metadata. |
| `prepare_pending_input` | Inspect exactly one selected current pending capture. |
| `prepare_manual_input` | Accept an explicitly supplied native error log and protect it for processing. |
| `prepare_retained_input` | Accept an explicitly selected already retained original for a fresh replay. |
| `protect_input` | Preserve the full original independently of records/review and within configured writable ownership. |
| `processor.process_input` | Sole Run composition from prepared input to complete records/native review. |
| `replay.rebuild_generation` | Process an explicit retained-input set into a named fresh generation via the same processor. |

Existing bodies explain the changed boundary:

- [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:940) `_inspect_pending` 940–1058,
  `finalize_pending` 1067–1150, `read_snapshot` 881–906 and `snapshot`
  1272–1389 contain old-format/adoption/result behavior outside C1/C2.
- [src/ck3chronicle/ingest.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:35) `ingest` 35–121 registers old
  storage before classification; it is not the new manual-input processor.
- [src/ck3chronicle/processing.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:888) context 888, parser 903,
  classifier 929 and projection 946 compose the old stages. Its lease/journal
  46–190 is not a port.
- [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:38) `load_config` 43–59,
  `require_strict_descendant` 80–102 and `validate_project_containment`
  105–140 supply existing explicit path authority.

## Implementation steps

1. Port C1's copy-only `spool_logs` and its exact helper/type closure into
   `capture.py`. Preserve the actual watcher callback/abort and result shape.
   Protect the required error log before optional associated crash evidence.
   Urgent capture does not hash the full log, open SQLite or load a classifier.
2. Port C2 primitives into `inputs.py`, then implement the explicit preparation
   and protection interfaces above. Compute a stable complete-file hash in the
   deferred path. Accept one current capture representation; manual native-log
   selection is an explicit input route, not a failed-format fallback.
3. Use supplied observed lifecycle facts only. If manual/replay input has no
   such facts, preserve their unavailability. Do not infer them from directory
   names, filesystem times or old database rows. Protect originals indefinitely.
4. Implement `process_input` with this single call order:

   `PreparedInput -> duplicate guard -> iter_emissions -> recover_diagnostics`
   `-> normalize_for_match / typed classify / original bindings`
   `-> aggregation + native review -> write_run`.

   Follow the actual 1.2/1.3 binding API without applying normalization or typed
   matching twice. The input stream is complete at every file size; every
   recognized emission yields accounted diagnostics/review or an explicit
   failure. Do not silently skip a malformed child.
5. Obtain a prospective Run identity within the ordinary 2.1 completion design.
   Coordinate the shard and compact records once. Report duplicate input as
   the defined duplicate result without creating a second successful Run or
   deleting protected evidence. Expose failures truthfully; no success-shaped
   result may hide incomplete storage.
6. Implement `rebuild_generation` with an explicit set of retained native
   inputs and separately named destination generation. Require the destination
   to be fresh; use the same preparation/classification/storage behavior as
   ordinary processing. Do not read/translate old database rows or replace the
   active generation implicitly.
7. Port F1 to `playset.py:analyze_debug_context` and its named pure type/helper
   closure. It preserves working grammar for the approved same-Run debug-log
   fast-follow when `runtime_context.py` is deleted. The current processor
   does not call it; capture/context persistence integration is later work.
8. Write down the concrete processing arguments/results for 3.1: selected
   input, configured protection ownership, chosen generation, Run/duplicate/
   failure result and stored review reference. Present the proposed explicit
   CLI selectors at the Stage 2 review, using 3.1's command table.

## Deliverable and following work

Deliver the five files and an exact call-chain handoff to Stage 3. Explain how
pending/manual/replay share `process_input`, how the protected original survives,
and what happens on duplicate/failure. Include the two Stage 2 data/layout
decisions from 2.1 and the proposed operator arguments for review.

Existing application calls change in 3.2. No actual capture, processing,
production database creation or replay is performed merely to prepare this
source handoff. Finish with the required file-scope proof.
