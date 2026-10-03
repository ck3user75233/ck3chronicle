# Agent Task 04(B) — Audit the complete pipeline processing path

Repository: `C:/Users/nateb/Documents/ck3chronicle`.
This is a read-only investigation with a written report. The owner will review
the findings with the Task 04 agent before deciding repairs or changes to Task 05.

## Objective

Establish whether the pipeline applies the pinned parser/model directly, or
whether additional interpretation, reprocessing, reclassification or regrouping
still changes or obstructs the result. Trace the complete selected execution path
and distinguish active behavior from inactive remnants and callers awaiting cutover.

Preserve the positive mechanics: lossless pinned recovery into message pieces/groups,
complete template matching, declared constraints, published single assignment,
original-value binding and the approved contract's record representation. The
pipeline must retain those mechanics while eliminating additional interpretation.
Exact-identity occurrence counting is approved downstream aggregation; it is not
learner-style regrouping or a new structural classification.

## Authority and starting evidence

Read [AGENTS.md](../AGENTS.md), [project status](PROJECT_STATUS.md),
[project plan](PROJECT_PLAN.md), [current handoff](CURRENT_HANDOFF.md),
[development environment](DEVELOPMENT_ENVIRONMENT.md) and [banned ideas](BANNED_IDEAS.md).
Then read:

- [Approved Error Contract](ERROR_CONTRACT_SPECIFICATION.md): current owner rules.
- [Task 04 handoff](TASK04_ERROR_CONTRACT_HANDOFF.md): interfaces, pins and native logs.
- [Learner delivery](LEARNER_PARSER_PIPELINE_HANDOFF.md): current model/parser/helpers.
- [Task 04 repair supplement](../src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md)
  and [historical rule audit](../src/ck3chronicle/pipeline/PIPELINE_RULE_AUDIT.md):
  cleanup obligations and investigation leads. Their L1/L2 rules are superseded.
- [Task 05 prompt](05_ERROR_CONTRACT_IMPLEMENTATION.md): the separate contract-
  implementation boundary. Do not execute or rewrite it during this audit.

At preparation, selection is `76630685c4a341ca14bf9c7c`, schema 4, parser v1.7,
assignment-v2, classifier-v7. Resolve through `pipeline.catalog` and verify the
actual selection/manifest. If changed, record the new evidence and interface
differences. Historical pins, counts and prior conclusions are not correctness targets.

## Investigation scope and method

1. **Map the path.** Trace catalog/model loading, executable-helper loading, raw
   recovery, candidate applicability, literal/slot matching, selection, binding
   and returned results. Include caches and all pre/post-selection transformations.
   Identify which parser/model declarations govern each behavior. Follow direct
   dependencies, including neutral helpers under learner-package paths; distinguish
   hash-covered release artifacts from application code and mutable policy inputs.
2. **Check for additional interpretation.** Look for phrase rewriting, literal
   removal, slot masking, invented optionality, extra lexical/type/semantic gates,
   inference, fallback classifiers, duplicated recovery/matching/binding, and
   selection overrides. Establish actual callers and effects. Validation explicitly
   required by the supplied definitions is not an extra gate. Considering multiple
   candidates inside the published selector is not reclassification.
3. **Account for retained code.** Identify obsolete pipeline modules/types and
   every relevant caller. Separate the selected pipeline from current application
   providers and historical research tools. Inspect application call edges only to
   establish reachability/cutover boundaries; do not derive requirements from their
   old semantics or execute production processing.
4. **Check contract readiness.** Confirm that complete selected assignments expose
   exact literals/layout choices, bindings, source/emitter, status and provenance.
   Include surrounding parts and ordered supporting entries. A parser result is
   not a finalized SQL diagnostic record. Contract implementation and SQL storage
   are still future work; identify their current absence without calling it an
   unauthorized semantic stage.
5. **Verify important findings on native evidence.** Use bounded replay of the
   complete retained logs in the handoff, adding a specific genuine log only when
   it resolves an identified gap. Verify hashes, original-byte correspondence,
   result accounting and preservation of selected assignments. Read-only tracing
   may observe calls on real inputs; do not mock behavior or alter policy/candidates.
   Report observed behavior separately from source-level hypotheses and unexercised
   branches. More matching coverage alone does not prove the path is clean.

Initial leads to verify, not presumed defects:

- `classifier.py` binds candidate captures and binds selected captures again:
  establish repetition, purpose and effect, distinguishing redundant work from
  changes to classification meaning.
- `pipeline/emissions.py`, `diagnostics.py`, `normalization.py` and historical
  domain types remain; `tools/template_learning/build_parser_comparison.py`
  imports them. Establish reachability and retirement dependencies.
- `matching.py` implements constraint mechanics and imports
  `template_learning.full_ids` with supplied declarations. Audit actual inputs
  and responsibilities; package location or similar source alone proves neither
  semantic drift nor unnecessary duplication.

Use no synthetic messages, mutated witness templates, generated corrupt artifacts
or test-file-derived requirements. A naturally unavailable case is a coverage gap.
Use `.venv/Scripts/python.exe -I -B`; preserve all captured logs.

## Allowed outputs and restrictions

Create only `docs/04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md` as the review report.
If it already exists, preserve it and identify the conflict. Optional task-owned
native evidence/traces may be written under ignored
`.ck3chronicle/wip/task04b-audit/`; reference exact paths and input hashes.

Do not edit code, model artifacts/selection, parser/learner files, prompts or other
documentation. Do not fix findings during the audit. No retraining, publication,
database writes, application cutover, watcher action, commit, push or evidence
deletion. Record entry/exit hashes and relevant Git state, preserving unrelated work.

## Required report and stop

Deliver a concise report containing:

1. The actual call map with current file/function references and selected identities.
2. A findings table: behavior and location; required mechanic, unauthorized active
   behavior, redundant non-semantic work, inactive remnant or later cutover concern;
   evidence; consequence; exact proposed repair/retirement and affected callers.
3. Explicit reconciliation of the Task 04 cleanup obligations: satisfied, violated
   or unverified, with evidence. Do not infer satisfaction merely from a module name
   or prior completion claim.
4. Task 05 impact for each finding: prerequisite repair, possible bounded contract
   integration correction, independent cleanup, or no effect. Propose the smallest
   scope and owning team; do not silently assign broader repair to Task 05.
5. Native checks, hashes/counts, coverage limits and unchanged-source scope proof.

Stop and return the report link with a short findings summary. The owner and Task
04 agent will review it together. This report does not authorize repairs, change
the approved Error Contract, or release Task 05 for execution.
