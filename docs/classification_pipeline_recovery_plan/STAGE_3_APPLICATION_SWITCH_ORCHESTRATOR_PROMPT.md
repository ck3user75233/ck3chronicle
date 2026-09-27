# Stage 3 — Connect application and retire old pipeline

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: sequence this stage's mini-projects and reconcile their interfaces.
Use with [the master orchestrator prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md); its authority, scope
proof and operational boundaries apply in full. This is an implementation
handoff prepared for owner review.

## Entry and exact child prompts

Require Stage 1 and Stage 2 handoffs, including concrete model paths, repository/read interfaces, complete processing inputs/results and resolution of the Stage 2 product choices. Obtain the separate verification task's explicit disposition for the known evaluator/tests/CI before declaring the whole implementation complete.

Read [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and
[CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md) for this stage's mapped source responsibilities.

1. [3_1_BUILD_REPORTS_AND_COMMANDS_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/3_1_BUILD_REPORTS_AND_COMMANDS_PROMPT.md).
2. [3_2_SWITCH_AND_RETIRE_OLD_PIPELINE_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/3_2_SWITCH_AND_RETIRE_OLD_PIPELINE_PROMPT.md).

## Ordered work and handoffs

| Mini-project | Work to coordinate | Handoff dependency |
|---|---|---|
| 3.1 | Build stored reports, current database audit and new command handlers. | 3.2 receives one register_commands entry and the lightweight capture_error handler. |
| 3.2 | Switch existing application/model resources, reconnect bounded offline consumers and delete all named obsolete providers/artifacts. | The application has one current pipeline and current documentation; no residual adapter keeps the retired provider graph callable. |

Run the named children in order. Reuse completed output rather than recreating
it when starting a new task. Inspect each child's actual file changes and
handoff against its exact scope; a coordinator has no independent create/edit/
delete list and cannot authorize additional files.

Mini-project 3.2 owns activation and retirement together. Recheck the complete caller/index disposition before concluding; any needed preceding implementation correction returns to its exact owning mini-project instead of authorizing a broad edit to the new package.

## Decisions to protect

Use the approved Stage 2 command contract and concrete 3.1 handlers. A new product behavior or additional mutation path returns as a precise amendment before it is implemented. Do not use general cleanup as authorization to expand the final switch.

Apply WORKPLAN 1.1–1.5 before interpreting classification states, record fields
or review content. Implementation defaults cannot supply missing approved rules.

## Stage deliverable

The final handoff accounts for WORKPLAN 6.1 caller changes, 6.2/6.3 deletions, section 7 artifact selection/removal, L1–L5 offline edits and section 8 documentation/deferred consumers. Describe source completion and separate verification status truthfully; do not claim a production replay, database cutover or working retained test suite that was not commissioned and evidenced.

Collect each child's changed-file proof against its own starting state.
State any incomplete dependency by file/function and responsible mini-project.
Use the completion message as the handoff; do not create an extra tracking
file. Product verification remains the separate scope named in WORKPLAN 8.1.
