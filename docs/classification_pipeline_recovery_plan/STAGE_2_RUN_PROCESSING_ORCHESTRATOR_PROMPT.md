# Stage 2 — Construct complete Run processing

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: sequence this stage's mini-projects and reconcile their interfaces.
Use with [the master orchestrator prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md); its authority, scope
proof and operational boundaries apply in full. This is an implementation
handoff prepared for owner review.

## Entry and exact child prompts

Require the Stage 1 handoff: direct contract interfaces and rules, original-byte emission recovery, bound values, runtime classifier and resolved artifact identity. Any missing field decision returns to 1.1; it is not supplied by a storage default.

Read [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and
[CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md) for this stage's mapped source responsibilities.

1. [2_1_BUILD_RUN_STORAGE_AND_REVIEW_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/2_1_BUILD_RUN_STORAGE_AND_REVIEW_PROMPT.md).
2. [2_2_COMPOSE_INPUT_PROCESSING_AND_REPLAY_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/2_2_COMPOSE_INPUT_PROCESSING_AND_REPLAY_PROMPT.md).

## Ordered work and handoffs

| Mini-project | Work to coordinate | Handoff dependency |
|---|---|---|
| 2.1 | Construct aggregation, the native shard writer and current-generation repository as one connected storage boundary. | 2.2 receives exact write_run inputs, duplicate-hash behavior, shard completion metadata and read interfaces. |
| 2.2 | Port capture/input primitives and compose pending/manual/replay through process_input. | Stage 3 receives complete processing/replay functions and explicit argument/result shapes. |

Run the named children in order. Reuse completed output rather than recreating
it when starting a new task. Inspect each child's actual file changes and
handoff against its exact scope; a coordinator has no independent create/edit/
delete list and cannot authorize additional files.

Aggregation, native review and SQLite are owned together by 2.1. Reprocessing uses a separately named fresh generation and explicit original-log inputs. This stage does not switch the existing application or read old database rows.

## Decisions to protect

Before Stage 3 activation, show the actual diagnostic identity fields, shard bytes/metadata separation, mixed-child accounting and the code path that makes a Run complete. Include explicit input/generation arguments proposed for commands. Ask only for a remaining product choice; accepted scope and established requirements do not need reconfirmation.

Apply WORKPLAN 1.1–1.5 before interpreting classification states, record fields
or review content. Implementation defaults cannot supply missing approved rules.

## Stage deliverable

The stage handoff shows prepare_* -> process_input -> classification -> aggregation/review -> write_run, plus rebuild_generation -> the same process_input. It names duplicate/failure results and their effect on protected evidence. It supplies the proposed command input/output contract for 3.1. The pure playset analyzer port is listed as a future feature dependency with no current processor call.

Collect each child's changed-file proof against its own starting state.
State any incomplete dependency by file/function and responsible mini-project.
Use the completion message as the handoff; do not create an extra tracking
file. Product verification remains the separate scope named in WORKPLAN 8.1.
