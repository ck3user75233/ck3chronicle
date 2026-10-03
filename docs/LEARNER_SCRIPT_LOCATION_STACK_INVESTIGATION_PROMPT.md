# Learner task — Investigate Script location stack matching

## Question

Does variation in the number of Script location entries cause avoidable unmatched
messages or loss of information? Assess an ordered variable-length representation.
Investigate first; no representation change has been approved.

## Starting evidence

- Read repository/learner instructions and the current learner handoff.
- [Task 06's recorded owner question](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md#limits-and-model-findings-carried-forward): sampled SQL record 17 used template `0b2804538785c71278ea37e7`, which has one Script location entry. Sibling templates cover longer stacks.
- Inspect `.codex-tmp/task06-v45/sql-view/sample.json` and `sql-diagnostic-sample.html`. Read these saved artifacts; do not regenerate the random sample.
- Resolve complete native logs through `.codex-tmp/task06-v45/verified/inputs.json`. The broader retained inventory is `.codex-tmp/learner-date-key/inputs.json`.
- Read [the v45 applicability finding](LEARNER_RELEASE_V45_RESULTS.md#the-demonstrated-applicability-defect): one-frame and four-frame structures required different definitions. This does not itself establish information loss.
- Establish the actual selected package from `models/selection.json`. The Task 06 baseline was package `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`.

## Deliverables

1. **Current behavior:** trace genuine examples through parser recovery, published templates, shared matching and bindings. Identify where stack length is constrained. Distinguish missing variants, recovery/matching defects and correctly preserved review evidence.
2. **Measured impact:** count observed stack lengths, template/provisional/no-match outcomes and misses demonstrably caused by stack length. State the input coverage and denominator; report zero demonstrated misses if supported by the evidence.
3. **Readable examples:** show native text, matched template/parts, ordered bindings and disposition for short/longer stacks and any genuine failures. Account for every location entry. Distinguish coverage gaps from demonstrated loss.
4. **Recommendation:** retain the current representation or propose an ordered variable-length representation. Explain effects on model format, matcher API, complete-message matching, binding order, exact rendering and diagnostic identity. Preserve frame order and values; do not make the whole chain an opaque PARAM merely to match it.
5. **Handoff:** write `docs/LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_RESULTS.md` with evidence links, proposed learner/parser/matcher work and pipeline dependencies separately. Link it from the learner handoff.

## Boundaries

- Use complete genuine retained logs and the shared matcher. No synthetic or modified messages; tests and old output do not define requirements.
- Bounded investigation tooling and reports are in scope. Preserve selected artifacts, model selection, pipeline code, SQL databases and watcher behavior.
- Work independently of Task 07. Present proposed model/API changes and their compatibility impact for owner review; do not implement or activate them during this investigation.
