# Task 04 completion handoff — 2026-09-27

## Outcome

Task 04 is complete: P1 repair and bounded P2 verification are delivered; the
owner approved the full [Error Contract specification](ERROR_CONTRACT_SPECIFICATION.md),
including source/emitter through the stored definition. Supported and provisional
selected assignments are record-eligible; unmatched evidence goes to review.
Error type remains unknown. Contract identity/rendering helpers and SQL persistence
are not implemented by this specification handoff. The subsequent
[Task 04(B) audit](04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md) and
[shared-matcher verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md) are complete.
The owner assigned shared-matcher integration and duplicate-matcher retirement
to [Task 05](05_ERROR_CONTRACT_IMPLEMENTATION.md), alongside contract implementation.
The selected infrastructure and interfaces below describe the predecessor that
Task 05 replaces; the revised prompt and learner handoff identify the new package.

## Active predecessor infrastructure

| Item | Exact value |
|---|---|
| Model revision | `76630685c4a341ca14bf9c7c` |
| Manifest SHA-256 | `364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0` |
| Model schema | `ck3chronicle.native-message-model`, version 4 |
| Parser | `ck3-lossless-v1.7` |
| Parser SHA-256 | `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |
| Selector / classifier | `complete-assignment-v2` / `ck3-native-message-classifier-v7` |

Resolve through [selection.json](../models/selection.json) and catalog; the
[learner handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) documents the published helpers.

## Predecessor interfaces to adapt in Task 05

[catalog.load_selected_classifier(*, models_root=None)](../src/ck3chronicle/pipeline/catalog.py)
returns the classifier. Use `read_log(path)` and `classify_raw(raw)`.
[NativeClassification](../src/ck3chronicle/pipeline/domain.py) exposes `selected`,
`outcome`, `template_id`, `bindings`, `error_type` and original evidence.
`selected` contains message, selected surrounding parts and ordered `components`.
Bindings expose region, positional name, type, value and absolute native span.
Both full and provisional outcomes expose selected bindings. Consume `selected`,
not the research `candidates` or ranking audit. Model `parts`/continuation layouts
supply literals. Unknowns and `UnresolvedEmission` retain original evidence.

## Checks and native examples

Fresh read-only replay using `.venv/Scripts/python.exe -I -B -u -` covered two
complete hash-verified native logs: 100,621 results; 64,160 full, 27,308 provisional,
9,153 unknown. All bytes accounted for; 173,247 present bindings matched source
bytes; 4,350 absences retained. All selected layouts reconstructed their content,
including 11 groups/13 entries. No synthetic inputs or test-derived requirements.

Exact inputs under `.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/`:

| SHA-256 directory / `error.log` | Representative evidence |
|---|---|
| `10cbdcb23e34a5b571a16eb52d390e5e676663936f000fd43404af19d85027fb` | Emission 0: provisional file/line LOCATORs; 51: duplicate-localization KEY/two LOCATORs; 292: selected surrounding file/line parts; 47026: two supporting entries. |
| `9d3622ab1b6c85cbab45d83767bb870b06c6fb9d6da50ee44f5eba3674d98cbc` | Two identical character/title groups yield one identity with count 2; also genuine unknown content. |

The learner's separate 30-log replay is corroborating evidence, not a Task 04
rerun: [continuation status/evidence](LEARNER_CONTINUATION_MODEL_STATUS.md).
Native ties/capture ambiguity, accepted empty REASON, HOUSE_FULL_ID and malformed
continuations were not exercised by the fresh two-log check. SQL/render-from-SQL
proof remains downstream. These were limits of the two-log check. Subsequent
[31-log verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md) exercises all nine
slot types and present-empty REASON; its report gives current native coverage.

## Original closeout changes and scope

Paths relative to `C:/Users/nateb/Documents/ck3chronicle/`:

| Action | Exact paths |
|---|---|
| Created | `docs/ERROR_CONTRACT_SPECIFICATION.md`; `docs/TASK04_ERROR_CONTRACT_HANDOFF.md`; `docs/05_ERROR_CONTRACT_IMPLEMENTATION.md` |
| Edited: entry guidance | `AGENTS.md`; `README.md` |
| Edited: approved product rules | `docs/OWNER_PRODUCT_INTENT.md`; `docs/ARCHITECTURE_AND_DATA_LINEAGE.md`; `docs/TRUSTED_RUN_SPEC.md` |
| Edited: continuation/history | `docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md`; `docs/CURRENT_HANDOFF.md`; `docs/PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md`; `docs/PROJECT_PLAN.md`; `docs/PROJECT_STATUS.md` |
| Deleted / predecessor source corrections | None |

This closeout records approval, reconciles active documentation and revises the
Task 05 prompt. The owner approved its improvements and required cleanup obligations
to remain accounted for, then commissioned a separate read-only Task 04(B) audit.
The subsequent review assigned shared-matcher integration, selected-only binding
and local matcher retirement to Task 05. Historical recovery/view retirement still
depends on retiring the learner parser-comparison tool's old path; broad application
cutover remains later. The revised prompt defines the current implementation scope.
No source/model/learner/runtime files changed; no database, production operation,
commit or push. Prior verification matched all 294 entry file hashes. This
documentation pass compares its 261-file entry baseline, verifies local links and
whitespace, and preserves the pre-existing
`docs/LEARNER_PIPELINE_MATCHING_INVESTIGATION_PROMPT.md`.

P1 source work and subsequent learner-delivered v41 integration already exist in
the checkout; they are not new changes in this closeout. Remaining specification
blockers: none. The 04(B) review hold is superseded by the owner-approved revised
Task 05 scope; shared-matcher verification is complete. Implementation is next.
