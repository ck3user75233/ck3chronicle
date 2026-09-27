# Master orchestrator — classification pipeline replacement

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: coordinate the three stages below, maintain the complete dependency view,
and require each mini-project's concrete handoff and file-scope proof.

Status: expanded prompt for owner review, 2026-09-13. Preparing this prompt set
does not execute it. When the owner commissions implementation, use this master
with the relevant stage and mini-project prompts.

## Governing objective and required reading

Build the production pipeline in
`C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/`, using the exact working-function ports and new
composition specified in [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md). Connect the application to that
package and delete the superseded providers in mini-project 3.2.

Read these definitions before deciding classification or storage behavior:

| Source | Required content |
|---|---|
| [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md:89) 89–105 / 108–146 | Product units, direct contracts, emission accounting, review evidence and original-log retention. |
| [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:118) 118–153 / 176–211 / 227–244 | Component ownership, native shards, fresh generations, offline authoring boundary and completion/retention. |
| [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277 | Contract-defined identity, typed fields, rendering, counts and interpretation lineage. |
| [docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md:205) 205–254 | Target vocabulary; `error_type` is the sole hierarchical diagnostic taxonomy. Technical analysis is subordinate to owner decisions. |
| [docs/BANNED_IDEAS.md](C:/Users/nateb/Documents/ck3chronicle/docs/BANNED_IDEAS.md:37) 37–87 | Removed designs and prohibited substitutes. |

Also read [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md), [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md),
[docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md) and [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md).
Current owner instructions take precedence over earlier technical proposals.
The dependency evidence is [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and [CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md).
Their existing-source ranges are locators; if lines move, use the named symbol
and reported diff to identify the same code. Scope does not expand with a search.

## Product definitions and flow

A Run is the successful processing result for one protected error log.
An emission is the timestamped native engine output including its continuations.
A recovered diagnostic is a transient child processing unit. A diagnostic record
is an approved compact SQLite identity within a Run.

The target flow is:

1. Copy completed-run evidence into protected pending storage.
2. Prepare an explicitly selected protected input and reject duplicate full-log hashes.
3. Recognize emissions and recover source-specific child diagnostics with original spans.
4. Compare each diagnostic to the selected approved model, validate typed contracts
   and bind concrete values once.
5. Aggregate approved identities; preserve review-routed original emissions.
6. Complete the Run's compact records and native-shard metadata.
7. Report stored records without reopening the original log or loading a model.

Use WORKPLAN 1.2 for the cited complete target field inventory. There is no
separate “classification meaning” entity. The current structural outcomes are
`full`, `l1_l2`, `l1` and `unknown` (WORKPLAN 1.3). L1-only is an exact
successful L1 assignment with unresolved L2. Optional layer metadata does not
prove that a structural model entry already has all direct-contract fields.

WORKPLAN 1.4 distinguishes canonical preservation policy from current model
state: no per-entry provisional/confidence status or calibrated threshold exists
in the selected structural artifact. Do not invent one from similarity scores.
Unresolved evidence is native emission content and metadata, not an unclassified
diagnostic record. Every recognized emission is accounted for; classification
coverage is not required to reach 100%.

One native shard belongs to each successful Run, including an empty shard.
The protected full original remains retained indefinitely. Production consumes
an approved artifact; it never runs the offline learner.

## Launch index and model defaults

Start each coordinating task with this master and the named stage prompt.
Each mini-project starts with this master, its stage prompt, its own prompt and
the preceding completion handoff. The master and stages do not execute the same
work twice: the active coordinator chooses the next incomplete child.

| Coordinating prompt | Model | Effort |
|---|---|---|
| This master | GPT-6 Astra | xhigh |
| [Stage 1 — Construct classification core](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md) | GPT-6 Astra | xhigh |
| [Stage 2 — Construct complete Run processing](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_2_RUN_PROCESSING_ORCHESTRATOR_PROMPT.md) | GPT-6 Astra | xhigh |
| [Stage 3 — Connect application and retire old pipeline](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_3_APPLICATION_SWITCH_ORCHESTRATOR_PROMPT.md) | GPT-6 Astra | xhigh |

| Mini-project prompt | Model | Effort |
|---|---|---|
| [1.1 — Define direct contracts and record interfaces](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_1_DEFINE_DIRECT_CONTRACTS_PROMPT.md) | GPT-6 Astra | xhigh |
| [1.2 — Port emission recovery and original-value binding](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_2_PORT_EMISSION_RECOVERY_PROMPT.md) | GPT-6 Astra | high |
| [1.3 — Build runtime classification and the direct model](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/1_3_BUILD_RUNTIME_CLASSIFIER_PROMPT.md) | GPT-6 Astra | xhigh |
| [2.1 — Build aggregation, Run storage and native review](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/2_1_BUILD_RUN_STORAGE_AND_REVIEW_PROMPT.md) | GPT-6 Astra | xhigh |
| [2.2 — Compose protected inputs, processing and replay](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/2_2_COMPOSE_INPUT_PROCESSING_AND_REPLAY_PROMPT.md) | GPT-6 Astra | high |
| [3.1 — Build stored reports, audit and command handlers](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/3_1_BUILD_REPORTS_AND_COMMANDS_PROMPT.md) | GPT-6 Astra | high |
| [3.2 — Switch application callers and retire the old pipeline](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/3_2_SWITCH_AND_RETIRE_OLD_PIPELINE_PROMPT.md) | GPT-6 Astra | xhigh |

These are task-specific recommendations, not measured quality guarantees.
The [official GPT-6 Astra documentation](https://developers.openai.com/api/docs/models/gpt-6-astra)
describes its reasoning/coding use and supported `high`/`xhigh` efforts.
Select the model and effort in the task's actual settings; writing a model name
inside a prompt does not change the active model. No global configuration change
is part of this project.

## Sequence and coordination

Stage 1 runs 1.1 -> 1.2 -> 1.3. Stage 2 runs 2.1 -> 2.2.
Stage 3 runs 3.1 -> 3.2. Keep each stage's required predecessor outputs explicit.

Treat stages as construction boundaries. Mini-project 3.2 is the connected
application activation and deletion change; no transitional public pipeline,
fallback, wrapper, old-schema reader or compatibility alias is commissioned.
Required behavior has a destination in the new package. Obsolete behavior and
its callers are deleted. The offline changes are precisely L1–L5 in WORKPLAN;
learner relocation, algorithm redesign and candidate-promotion redesign are
separate projects.

A coordinator has no additional file-writing scope. If it implements a child
itself, it works under that child's exact list and entry baseline. Cross-package
corrections return to the owning prompt with a new scope comparison. An out-of-list
change needs an amended instruction before mutation. Coordination does not
itself authorize creating tasks, spawning agents or parallel implementation.

## Mini-project entry, exit and source protection

At entry, read the predecessor's handoff and record the exact resolved create,
edit and delete lists and starting source state. Preserve pre-existing edits.
Source references are read inputs, not edit permissions. Resolve the two
content-derived model paths before creating them.

At exit, report each created, edited or deleted path and the scope entry that
authorized it. Compare against the entry state, including tracked, untracked
and ignored files and any explicitly authorized external output roots. An empty
`git diff` alone cannot establish this proof. Use read-only inventories and
content comparisons; do not build a new journal or status infrastructure.

Git history protects committed source. Uncommitted and untracked work requires
a recoverable baseline too. Do not reset owner changes or assume HEAD restores
the present planning files. No commit, push, runtime-evidence deletion or
production database operation is implied by implementation scope.

Each handoff includes: concrete interfaces and callers; ports versus new bodies;
source/contract decisions with evidence; completed file-scope proof; and the
specific input required by the next child. Report any unresolved question with
its exact field, caller or proposed behavior. Keep the handoff in the task
completion message; no extra receipt/status artifact is authorized.

## Focused owner reviews and separate verification

In 1.1, present the implemented types and per-field authority inventory. Only
a necessary missing or changed contract rule requires a decision before dependent
work uses it. Moving an established definition does not require blanket review
of existing approved contracts.

At Stage 2 completion, present the concrete record/shard layout, mixed-emission
routing, ordinary SQLite/filesystem completion behavior and proposed explicit
operator inputs. Resolve remaining product choices before the final application
switch. Prior owner decisions persist; do not ask for them again.

Product tests, fixtures, evaluators, acceptance/performance design and operational
replay are outside this prompt set. WORKPLAN 8.1 names the known evaluator,
test and CI consumers whose disposition must be supplied by the separate
verification task before implementation is declared complete. Do not keep old
APIs to satisfy old checks or silently leave that dependency unresolved.
The owner-requested changed-file scope proof remains required for every child.

## Final delivery

Report the new package and sole production flow, selected direct artifact,
supported commands, retired providers/artifacts and bounded offline edits.
Account for every dependency-map finding, every child's file-scope proof and
the separate verification disposition. Distinguish completed source work from
authorized operational replay or activation of a real database generation.
