# Agent Task 07B — Audit learner, matcher and parser version boundaries

## Outcome

Determine whether selecting a learner/model/matcher/parser revision actually
selects all code and rules needed to reproduce its behavior, or whether execution
still depends on mutable code outside the selected version or snapshot. Produce
a concrete, ordered repair plan with exact files, ownership and deliverables.

This is a dedicated learner-team review. Audit and propose repairs; do not implement
them in this task. Task 07 can proceed in parallel against the current pinned
runtime package. Escalate any confirmed dependency that would make its ingestion
results depend on unpinned learner code, or any proposed repair that could break
functionality the owner still needs.

## Scope and parallel-work boundary

Read repository instructions, `tools/template_learning/AGENTS.md`, current sections
of status/plan/handoff, and the focused references below. Historical tasks and
tests are evidence of implementation, not requirements.

Inspect learner building, incremental updates, candidate loading, evaluation,
publication/repackaging, parser selection and the delivered runtime package.
Inspect pipeline callers only to establish the consumer boundary.

Write only:

- `docs/TASK07B_LEARNER_DEPENDENCY_VERSIONING_AUDIT.md` — findings and repair plan.
- `docs/TASK07B_LEARNER_DEPENDENCY_VERSIONING_HANDOFF.md` — concise actionable
  handoff, including any implications for Task 07's per-Run processing metadata.

Keep any generated inspection output in a task-owned ignored directory. Leave
source code, existing artifacts, active selection, configuration, databases,
watcher and shared planning/handoff files unchanged. Other agents may be changing
the checkout: distinguish their changes from yours. Do not publish or activate
a new model/package. No commits or pushes.

## Starting evidence — confirm and extend

The review that commissioned this task inspected source; it did not execute a
learner campaign or independently prove complete dependency isolation.

1. **Published runtime package:** `models/selection.json` selects package
   `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`.
   `pipeline/model.py` executes the package's pinned bootstrap. The package
   contains matcher dependencies and parser code, with file hashes and an isolated
   module namespace. This appears self-contained; do not assume runtime leakage
   just because matching source also exists in `tools/template_learning/`.
2. **Learner identity already exists:** the selected model's `algorithm` includes
   `learner_identity`, 28 implementation-file hashes, clusterer version
   `outer-diagnostic-consensus-v45`, and feature version
   `ck3-native-message-features-v4`. An earlier claim that learner provenance was
   missing overlooked these fields. Determine whether the identity is complete
   and the referenced executable bytes are retained and selectable.
3. **Candidate snapshots:** `artifacts.write_bundle` stores the model, evidence,
   parser and parser manifest, `assignment.py` and `continuations.py`. It does not
   itself copy the entire learner implementation named by its hash list.
   `load_bundle` consults current imported `CONSTRUCTIONS`, `OWNER_RULES` and
   `CLUSTERER_VERSION`. Establish which uses require a matching working checkout
   and whether an independently selectable learner snapshot exists elsewhere.
4. **Publication:** `publish_native_model.publish_package` fills `RUNTIME_FILES`
   by reading adjacent working-tree source files. The normal publish path checks
   recorded reference implementation hashes; the source-release repackaging path
   also needs tracing. Explain whether changing working source explicitly creates
   a newly identified package, fails, or can unexpectedly affect a requested build.
5. **Parser boundary:** `parsers/v1_7/parser.py` is versioned and hashed; recovery
   rules are embedded, with a readable JSON copy. `parsers/__init__.py` supplies
   loading and recovery dispatch outside that parser artifact and outside the
   learner's 28-file list. Check whether this affects reproducibility, without
   presuming the parser itself is unpinned.
6. **Other helpers:** `publish_native_model.py` and
   `inspect_incremental_learning.py` participate in publication but are not in
   that learner file list. `incremental_template_registry.py` imports application
   configuration for path defaults. Classify these dependencies by their actual
   effect; path selection is different from inference or matching behavior.

Relevant entry points:

- `tools/template_learning/learn_error_templates.py`
- `tools/template_learning/incremental_template_registry.py`
- `tools/template_learning/artifacts.py`
- `tools/template_learning/research_matching.py`
- `tools/template_learning/publish_native_model.py`
- `tools/template_learning/matcher_loader.py`
- `tools/template_learning/native_matching.py` and its imports
- `tools/template_learning/parsers/__init__.py` and versioned parser manifests
- `src/ck3chronicle/pipeline/model.py`, `catalog.py`, `classifier.py`

Read `docs/LEARNER_PARSER_PIPELINE_HANDOFF.md` and `docs/SHARED_MATCHER_API.md`
for delivered formats/APIs; verify current code rather than assuming historical
handoff statements still describe it exactly.

## Audit questions

Trace the local dependency chain for each active entry point, including dynamic
imports, loaded Python files, JSON rules, configuration and publication helpers.
Separate development source, immutable delivered code, launchers/adapters,
external evidence and review-only tooling.

For each dependency relevant to behavior or publication, record:

- Exact path and caller; whether it executes, supplies rules or only metadata.
- Owning component and where its version/hash is recorded.
- Whether the referenced bytes are retained, merely hashed, or taken from the
  current checkout; how the consumer selects them.
- Consequence of a change: new explicit identity, clear rejection, missing
  reproducibility, or silently different behavior. Supply source evidence.

Answer these concrete questions:

1. Can the selected runtime parser/matcher run without learner checkout code?
2. Can a learner revision be selected and executed independently of today's
   working learner source? Are all behavior-affecting rules/settings included?
3. Can its candidate be loaded, evaluated and published using those same selected
   dependencies? Distinguish intended new-package publication from reproducing
   an existing package.
4. Do learner evaluation and published matching use the same implementation and
   explicitly identified revisions? Shared source and selected released code are
   different claims; explain which is currently true.
5. Which existing identities can pipeline Run metadata use, and is anything
   genuinely missing? Do not create new IDs where existing ones suffice.

Location outside a version-named directory is not by itself a defect. A dependency
is adequately pinned if the selected identity determines its retained bytes and
the intended operation uses them. Conversely, listing a hash alone does not
preserve executable code or make it selectable. Identify the actual gaps.

## Repair proposal

For each confirmed gap, propose the smallest concrete correction: owning files,
versioned artifact or snapshot contents, selection/reference mechanism, consumer
changes and observable acceptance outcome. Recommend an execution order and
separate learner-local repairs from any consumer coordination needed after 07.

Use one source owner per implementation. Preserve existing immutable releases.
Identify duplicated or obsolete code worth retiring only after tracing its callers
and still-required behavior. No legacy fallbacks or backward-compatibility layers.
If a repair would break something still needed, identify the concern and options
for owner review rather than silently retaining or removing that behavior.

Keep this focused on version/dependency ownership. Do not introduce a new learning
algorithm, error taxonomy, broad model-quality campaign or pipeline redesign.
Carry unrelated learner issues as references, not additional work in this audit.

## Evidence and completion

Prefer source/import tracing and existing release metadata. If execution is needed
to resolve a specific uncertainty, use the repository Python environment and a
bounded selection of genuine retained native evidence in disposable storage.
Use no synthetic messages, mutated logs/artifacts, fabricated records or mocks.
Explain what was inspected versus executed and leave unsupported claims open.

The report must lead with confirmed gaps and their practical consequences, followed
by the dependency inventory and ordered repair plan. The handoff must state:

- Whether Task 07 can continue unchanged and the evidence for that conclusion.
- Exact existing learner/model/parser/matcher/package identities and metadata
  locations; proposed additions only where a confirmed need exists.
- Concrete follow-up deliverables, affected paths and any owner decisions needed.
- Verification limits and confirmation that active source/selection were not changed.

Stop after delivering the audit and repair proposal for review.
