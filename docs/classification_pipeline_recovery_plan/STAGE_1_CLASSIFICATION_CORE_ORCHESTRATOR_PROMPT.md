# Stage 1 — Construct classification core

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: sequence this stage's mini-projects and reconcile their interfaces.
Use with [the master orchestrator prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md); its authority, scope
proof and operational boundaries apply in full. This is an implementation
handoff prepared for owner review.

## Entry and exact child prompts

Start from the cited target fields and existing-source map. The new package is not yet present at the planning snapshot; preserve all existing application callers during this construction stage.

Read [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and
[CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md) for this stage's mapped source responsibilities.

1. [1_1_DEFINE_DIRECT_CONTRACTS_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_1_DEFINE_DIRECT_CONTRACTS_PROMPT.md).
2. [1_2_PORT_EMISSION_RECOVERY_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_2_PORT_EMISSION_RECOVERY_PROMPT.md).
3. [1_3_BUILD_RUNTIME_CLASSIFIER_PROMPT.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_3_BUILD_RUNTIME_CLASSIFIER_PROMPT.md).

## Ordered work and handoffs

| Mini-project | Work to coordinate | Handoff dependency |
|---|---|---|
| 1.1 | Define ErrorContract and the transient/record interfaces; produce the exact field-authority inventory. | 1.2 receives original-byte/child-span and matching-view interfaces. 1.3 receives the direct artifact shape and established rules. |
| 1.2 | Port R1–R4 and compose original-value recovery; supply one normalization identity. | 1.3 receives typed token bindings, original-value ownership and source-specific diagnostic boundaries. |
| 1.3 | Port R5–R7, implement direct artifact loading and build the current revision. | Stage 2 receives approved direct outcomes and immutable model/contract lineage. |

Run the named children in order. Reuse completed output rather than recreating
it when starting a new task. Inspect each child's actual file changes and
handoff against its exact scope; a coordinator has no independent create/edit/
delete list and cannot authorize additional files.

All three children complete their own scope proof. Stage 1 does not edit the learner or delete its tools; the precise dependency edits and deletions are coordinated with provider retirement in 3.2.

## Decisions to protect

Read the actual domain/contract definitions together with the field inventory. If a direct error type, slot role, identity rule or rendering rule has no established source, return that exact issue to the owner before it becomes runtime authority. Do not convert the projection catalog wholesale or relabel all existing templates as candidates.

Apply WORKPLAN 1.1–1.5 before interpreting classification states, record fields
or review content. Implementation defaults cannot supply missing approved rules.

## Stage deliverable

The stage handoff names all ten new core Python files, the two resolved artifact paths, normalization/model identities and the classification interfaces consumed by aggregation. It identifies structural support separately from direct-record eligibility and records any owner decisions. Existing command selection remains unchanged until 3.2.

Collect each child's changed-file proof against its own starting state.
State any incomplete dependency by file/function and responsible mini-project.
Use the completion message as the handoff; do not create an extra tracking
file. Product verification remains the separate scope named in WORKPLAN 8.1.
