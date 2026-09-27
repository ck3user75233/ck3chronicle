# Plan the classification-pipeline recovery

Create a proposed work plan and package structure for simplifying
ck3chronicle's classification pipeline. This task is planning only. Produce the
plan and implementation prompts for owner review; do not implement the
refactor or design its tests and checks yet.

## The job

The current `error.log` path works end to end, but classification meaning is
spread across three competing layers: a legacy regex extractor taxonomy and
fallback, the empirical classifier, and a later semantic-projection layer that
rewrites classifier output.

Use `docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md` as the technical analysis
of that problem. Inspect the live code it identifies, verify its file and caller
map against the current tree, and design the smallest coherent sequence of
changes that replaces the competing layers with one direct path:

```text
error.log
-> timestamped emission recognition
-> source-specific splitting when one emission contains multiple diagnostics
-> empirical error-template/error-contract nomination
-> typed validation and an explicit classification outcome
-> compact database records or native review evidence
-> database reporting
```

The plan should leave a usable end-to-end path after each coherent package and
make legacy components removable as soon as their required behavior has moved
to the target path.

## Product outcomes to preserve

- Process every valid `error.log` completely under the same behavior regardless
  of size.
- Account for every recognized emission through one or more recovered
  diagnostics, preserved review evidence, or an explicit parser failure.
- Treat fully classified, provisional, low-confidence, L1-only, and unknown
  results as valid explicit outcomes.
- Let an approved error contract directly own classification meaning, typed
  slots, validation, rendering, and aggregation identity.
- Store compact diagnostic records and one native review shard per successful
  Run ID, then report from stored records.
- Use fresh database generations when stored meaning changes. The product has
  not launched, so no legacy-schema compatibility or historical-row migration
  is needed.

## Sources and authority

Read repository-root `AGENTS.md`, then use these sources:

1. `docs/OWNER_PRODUCT_INTENT.md` for product requirements;
2. `docs/BANNED_IDEAS.md` for rejected designs;
3. `docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md` for the technical findings,
   current pipeline analysis, and proposed retain/refactor/delete outcomes;
4. `docs/ARCHITECTURE_AND_DATA_LINEAGE.md` for the surrounding architecture;
5. `docs/CURRENT_HANDOFF.md`, `docs/PROJECT_PLAN.md`, and
   `docs/PROJECT_STATUS.md` for current repository and operational state; and
6. `docs/DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md` for background on
   fresh database generations.

Current owner instructions, `OWNER_PRODUCT_INTENT.md`, and `BANNED_IDEAS.md`
govern if a technical document conflicts with them. For each package, identify
the owner-defined outcome it serves. List any materially unresolved product or
design choice for the owner instead of settling it inside the plan.

Do not plan tests, checks, fixtures, evaluators, validation procedures,
acceptance conditions, or performance thresholds in this task. Verification
design is a separate step after the owner has reviewed and approved the
workplan, master prompt, and package prompts.

## In-flight owner reviews

Use two short owner reviews while developing the plan:

1. After reading the governing documents and recovery review and locating the
   primary live entry points—but before doing the exhaustive code map—report the
   understood problem, target outcome, intended deliverables, material
   assumptions, and questions that genuinely need owner direction. Pause for
   the owner's response.
2. After completing the code map and drafting the package sequence and shared
   structure—but before writing the final workplan and package prompts—report
   the provisional retain/refactor/delete map, proposed package names and order,
   product outcome served by each, expected kinds of behavioral change, and
   remaining assumptions. Pause for the owner's response.

Keep each review concise and directed at catching a mistaken interpretation or
unnecessary expansion early. These reviews do not create new requirements or
separate validation work.

## Workplan content

Create an exact map of the live implementation, including:

- emission parsing and source-specific splitting;
- legacy regex extraction and fallback behavior;
- empirical normalization, model loading, nomination, and typed validation;
- semantic projection and its catalogs;
- database schema, repositories, transactions, and classification lineage;
- native review handling;
- reporting and audit consumers;
- CLI registrations and every affected live caller;
- model-generation and learner tools.

Reconcile that map with every retain, refactor, and delete finding in the
classification recovery review. Assign each finding to one implementation
package or record a concise reason that no change is needed.

Then define the smallest practical package sequence. For each package, state:

- the product outcome and technical objective;
- dependencies on earlier packages;
- exact files, symbols, callers, and artifacts to change or remove;
- the intended behavior after the change;
- expected interactions with the preceding and following packages; and
- the point at which the resulting design should return to the owner for
  review.

Identify a small number of similar owner-review points for the later
implementation, placed only where an incorrect interpretation could compound
across subsequent packages. State what concrete code change or observed output
the owner would review at each point and what decision it protects.

## Deliverables

Create a new `docs/classification_pipeline_recovery_plan/` directory containing:

- `WORKPLAN.md`: the current and target pipelines, exact code map, package
  sequence, review-finding coverage, dependencies, boundary rationale,
  in-flight owner reviews, and open owner decisions;
- `MASTER_ORCHESTRATOR_PROMPT.md`: a concise implementation handoff containing
  the shared objective, package order, operational boundaries, and the proposed
  owner-review points; and
- numbered package prompts named for their concrete technical objectives.

Keep shared instructions in the master prompt. Package prompts should contain
only the information specific to that package.

Use one primary agent for this planning task; do not use subagents or validation
agents. Preserve unrelated work. Do not change product source, tests, existing
project documents, production evidence, or the production database. Return the
new plan to the owner as a proposal, explicitly identify open decisions, and
stop before implementation.
