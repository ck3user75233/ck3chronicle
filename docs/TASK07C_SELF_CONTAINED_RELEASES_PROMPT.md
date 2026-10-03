# Agent Task 07C — Complete, Selectable Learner and Model Releases

## Objective

Implement complete, immutable production releases that can be selected and
executed directly. Selecting a version must execute its retained code and rules,
never today's working-tree implementation applied to historical artifacts.

Maintain two independent release families:

- **Learner releases:** learner code, rules, parser, matcher, adapters,
  evaluation/publication helpers and all dependencies required for supported
  learner operations.
- **Production model releases:** already-built models with the parser, matcher,
  rules and runtime dependencies required to use them through the pipeline.

Include dependencies inside each release directory. Duplication between releases
is intentional. Do not introduce shared executable dependency stores,
cross-release executable links or dependencies on the mutable learner checkout.
Keep one authoring implementation under `tools/template_learning/`; releases are
immutable distributions, not separate authoring codebases.

This task does not commission production-model rebuilding, historical training
evidence retention, campaign reconstruction or changes to learning behavior.

## Scope and required reading

Treat this as one learner-team implementation. Own release creation, inventory,
authentication, selection, candidate evaluation, publication and distribution.
Reuse existing runtime packages and pipeline loading contracts.

Read root/nested `AGENTS.md`, current plan/status/handoff sections,
`docs/DEVELOPMENT_ENVIRONMENT.md`, and:

- `docs/TASK07B_LEARNER_DEPENDENCY_VERSIONING_AUDIT.md`
- `docs/TASK07B_LEARNER_DEPENDENCY_VERSIONING_HANDOFF.md`
- `docs/LEARNER_PARSER_PIPELINE_HANDOFF.md`
- `docs/SHARED_MATCHER_API.md`
- `docs/TASK07_SCOPE_REVIEW.md`
- `docs/BANNED_IDEAS.md`

This prompt narrows the audit's repair proposals to release retention and
execution. Its exact-rebuild recipe/evidence proposals are not commissioned.

Task 07 can continue using the current package. Leave its ingestion, SQL,
playset, raw-log retention and watcher work unchanged. Coordinate shared
distribution edits, including `pyproject.toml`, and preserve parallel changes.

## Retention policy — no deletion implementation

Document a policy of keeping the latest **ten production learner versions** and
**ten distinct production model revisions**, including their complete runtime
packages. Distinguish production releases from research candidates and record
production order explicitly.

Do not implement automatic pruning, retirement commands, deletion previews,
release-use locks or deletion tests in this task. Do not delete existing releases.
Older versions remain available until separately directed; ten is not a maximum
to enforce now.

**Automatic one-month retention of captured `error.log` and `debug.log` belongs
to Task 07 and watcher integration. It is unrelated to learner/model retention.**

## Implementation

### 1. Inventory and retain complete releases

Inventory actual production releases and genuine retained source/package copies.
Create durable repository/application-owned release directories and a small
catalog mapping existing identities to paths, pinned manifest hashes, production
order and availability. Keep learner snapshots separate from model runtime
packages. Task scratch directories must not be their permanent authority.

Preserve existing immutable artifacts byte-for-byte. Verified artifacts may be
registered or copied without rebuilding them or changing their identities.
Keep logs, databases, learner state and generated evaluation material outside
executable release directories and Git.

The audit found a retained v45 learner source copy at
`.codex-tmp/learner-release-v45/source/`, including the 28 hashed implementation
files. The current runtime package already contains its parser/matcher closure.
Confirm current evidence; do not claim learner identity or retained source is
absent.

Identify historical releases with missing bytes or incompatible interfaces.
Report exactly what is missing and whether genuine retained artifacts can resolve
it. Do not guess dependencies, retrain models, silently exclude releases or claim
ten usable historical versions exist without evidence.

### 2. Authenticate and execute complete learner snapshots

Extend the existing artifact/identity mechanism to cover the full execution
dependency set: imports, dynamic loads, parser dispatch, rule files, evaluation
and publication helpers. Retain the selected parser implementation and manifest
inside the release. Do not stop at the existing 28-file list.

Relevant owners include `artifacts.py`, `parsers/__init__.py`,
`learn_error_templates.py`, `incremental_template_registry.py`,
`evidence_serialization.py`, `inspect_incremental_learning.py` and
`publish_native_model.py`, under `tools/template_learning/`.

Remove incidental application/review dependencies from core operations. Move
needed helpers into their existing format/artifact owners and update callers,
without duplicate definitions or compatibility aliases. Explicit-path execution
must not require application configuration merely to import learner code.
Resolve convenience path defaults at the outer command boundary.

Provide one lightweight authenticated launcher, adding `learner_loader.py` if
appropriate. It must select and verify the requested snapshot before importing
its implementation, then execute in a clean process or equivalently isolated
namespace. Ambient `PYTHONPATH`, installed learner modules and previously imported
versions must not determine execution.

Missing, corrupt or incompatible selections fail explicitly. No fallback to
current source or another release. The launcher contains no inference or matching
logic.

Treat Python and its standard library as explicit platform prerequisites; record
supported requirements and the execution version. Include required non-platform
dependencies. Do not expand this into operating-system bundling or claims of
cross-interpreter bitwise reproduction.

Closing the dependency set creates a newly identified learner release. Preserve
historical identities and do not make old registries accept changed code as their
original learner.

### 3. Bind candidate operations and publication to releases

New candidates must identify the exact learner snapshot and parser they require.
Evaluation and same-version incremental continuation must authenticate and execute
that selection, rather than consult current imported rules or version labels.
Preserve data-only inspection of retained evidence.

Update `research_matching.py`, `evaluate_unseen_session.py` and affected review
callers. Evaluation receipts must identify the candidate/model, input, parser and
actual executed learner snapshot or runtime package. Published-model evaluation
uses its retained runtime package; unpublished-candidate evaluation uses its
selected learner snapshot. Maintain one shared matcher source owner.

Publication must copy runtime code from the selected authenticated release.
Registering, copying or selecting an existing package requires no learning.
If packaging existing model definitions with a different matcher remains supported,
require an explicit target implementation, a new package identity and validation
of that actual combination. Old validation does not establish parity for changed
code.

Preserve required additive-learning, publication and native-review workflows.
Identify any owner decision before breaking required behavior; do not add legacy
fallbacks.

### 4. Make retained models usable through the pipeline

Every available production model package must parse and match without its
training corpus, learner registry, learner snapshot or working checkout.

Reuse existing model/package identities, parser hashes, matcher API and selector
versions, and manifest hashes. Package identity determines the executable
combination; an API label alone does not. If a model has multiple packages,
selection must resolve an explicitly recorded package rather than guess.

Expose release listing and explicit selection through the owning interface.
Verify through `src/ck3chronicle/pipeline/catalog.py`, `model.py`,
`classifier.py` and the public contract-preparation boundary. Deliver retained
releases in installed resources as well as source-checkout storage.

Use alternate selections for verification without changing the active default
or existing Runs. Supply Task 07 with exact identity fields and the supported
selection entry point. Run metadata must describe the package actually executed;
ingestion must not import learner code or recompute training provenance.

If a historical release needs a substantive pipeline/API change, identify the
release, failing boundary, owning files and smallest receiving change. Deliver a
bounded pipeline follow-up and continue independent learner work. Do not redesign
the pipeline, add compatibility layers or hide the unresolved availability gap.

## Verification

Use the repository Python environment, bounded genuine retained CK3 evidence and
task-owned ignored output. A small learner exercise verifies executable releases;
it does not authorize rebuilding production models or running a quality campaign.

Demonstrate:

1. A relocated learner snapshot can perform bounded fresh learning, same-version
   continuation, evaluation and publication without working-tree learner or
   application imports. Verify every project-local executable/rule source.
2. Explicit selection isolates distinct genuine retained learner versions where
   available, including protection from already-imported modules.
3. Every inventoried usable production package works through the pipeline on
   bounded native evidence. Switch packages without editing them or the default.
4. Retained models run without learner/training resources and are available from
   installed application resources.
5. Snapshot evaluation and delivered matching agree on selected assignments,
   statuses and captures for the verified evidence; provisional, unknown and
   unresolved outcomes remain explicit.
6. Missing dependencies, integrity disagreements and incompatible selections
   fail without fallback, and metadata identifies the implementation executed.

Use no fabricated models, synthetic CK3 messages, mutated native logs or mocked
matching behavior to establish functional parity. Integrity checks may use
isolated copies; they are not matching-parity evidence. Report unexercised branches
and historical availability limits. No release-deletion verification is required.

## Deliverables and completion

Deliver the implementation, complete releases, catalog/listing/selection
interfaces, distribution integration, focused verification and documented
last-ten policy.

Write `docs/TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md` with:

- Exact layout, commands/APIs, catalog and identity fields.
- Usable production releases and named historical availability gaps.
- Verification evidence, execution environments and limits.
- Instructions for selecting retained versions without modifying them.
- Retention policy, changed files and precise pipeline receiving work.
- Confirmation that active selection, existing immutable artifacts, production
  data and watcher operation remain unchanged.

Update focused documentation; coordinate shared planning/handoff edits.
Do not activate a new model, run production ingestion, alter configuration roots,
modify the watcher, delete releases, commit or push.

Stop after delivering the implementation and reviewable handoff. Do not claim
complete version availability while quietly excluding a retained production
version that still cannot execute.
