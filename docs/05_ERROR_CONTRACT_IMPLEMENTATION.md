# Agent Task 05 — Integrate the shared matcher and implement Error Contracts

Revised 2026-09-27 for `C:/Users/nateb/Documents/ck3chronicle`.
This replaces earlier Task 05 prompts. The owner assigned shared-matcher
integration and duplicate-matcher retirement to this task following the Task 04(B)
review and independent candidate verification.

## Deliverable and authority

Deliver this processing path:

**Pinned parser and recovery → shared complete matching/selection → selected
assignment bound once → contract-compliant, serializable record-ready data.**

Implement the approved definition, acceptance, identity and rendering mechanics.
A diagnostic record remains the refined unique error stored in SQL; this task
prepares its data. Run aggregation, SQLite/review-shard persistence, report callers
and application cutover are subsequent assignments.

Read repository instructions, [status](PROJECT_STATUS.md), [plan](PROJECT_PLAN.md),
[current handoff](CURRENT_HANDOFF.md), [development environment](DEVELOPMENT_ENVIRONMENT.md)
and [banned designs](BANNED_IDEAS.md), then:

- [Approved Error Contract](ERROR_CONTRACT_SPECIFICATION.md): product requirements.
- [Learner delivery](LEARNER_PARSER_PIPELINE_HANDOFF.md) and
  [shared matcher API](SHARED_MATCHER_API.md): package and input/result/error contract.
- [Independent verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md): verified
  package, complete native input inventory, bindings and coverage limits.
- [Task 04 handoff](TASK04_ERROR_CONTRACT_HANDOFF.md) and
  [04(B) findings](04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md): predecessor evidence.

Current owner direction and this prompt supersede the earlier implementation hold,
local-matcher repair proposals and old interface descriptions. Audit recommendations
are not additional requirements. No fresh broad audit is required.

## Infrastructure to integrate

Candidate: `models/candidates/44a0401b8adf0a2953d26705/`.
Manifest SHA-256:
`2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1`.

The package contains unchanged model `76630685c4a341ca14bf9c7c` / schema 4,
parser `ck3-lossless-v1.7`, selector `complete-assignment-v2`, and matcher API
`ck3-native-matcher-v1`. Proposed selection schema 2 is in
`models/candidates/selection.proposed.json`; active selection is still schema 1.
Verify identities at entry. If delivery has advanced, establish its explicit
replacement handoff and differences before adapting.

The package exposes `load_package`, `parse_file`, `iter_units` and `match`.
It returns one complete assignment with final `template` or `provisional` status,
or explicit no-match. Captures supply exact values, presence and region-relative
byte spans; selected wrapper IDs, component indices and layout indices are supplied.
The package owns applicability, complete literals, all nine declared slot types,
constraints, wrapper/component matching and winner selection.

## Mutation boundary

Create `src/ck3chronicle/pipeline/contracts.py`. Adapt owning pipeline files
`catalog.py`, `model.py`, `raw_input.py`, `classifier.py`, `bindings.py` and
`domain.py` as necessary. Delete `pipeline/matching.py` after replacing its callers.
Remove superseded local matching/selection loops, duplicate model-semantic
validation, bound-candidate alternatives and types used solely by those paths.
Delegate model semantics to the package validator; retain application selection,
resource integrity and contract/result correspondence checks in their owners.

Update `models/selection.json`, selected-resource entries in `pyproject.toml`
and directly affected pipeline documentation. Candidate payloads and existing
model releases stay immutable. Learner implementation, inference, declarations,
ranking policy, application/CLI/database providers remain outside this task.

Historical `emissions.py`, `diagnostics.py`, `normalization.py` and their domain
types have a separate retirement dependency on the learner comparison tool.
Carry that named dependency into the handoff; keep them outside the new processing
path. Broad provider/model retirement belongs to the later cutover. Do not retain
the replaced matcher as a fallback or alias.

Record entry/exit hashes and Git state, including untracked source. Preserve
unrelated work and native logs. Keep verification artifacts ignored. No commit,
push, learner publication, production ingestion or watcher operation.

## Execute in this order

### 1. Load the pinned package

Adapt catalog/reader to selection schema 2, distinguishing model revision from
package identity. Resolve the selected directory within the models root; verify
the externally pinned manifest and bootstrap bytes before execution, then use
the package loader. Support source and installed resource locations.

Delegate model/parser/matcher validation to the verified package. Remove active
dependencies on mutable learner modules, including parser loaders and full-ID
helpers. Use explicit candidate selection for pre-activation verification.
Unsupported formats fail explicitly; no fallback to the old matcher.

### 2. Replace matching and bind the winner once

Use one pinned parser/recovery route. Consume `iter_units` or adapt its original
ranges once into the documented input. Preserve source/emitter, complete bodies,
wrapper regions, ordered supporting entries and original provenance.

Call the shared matcher once per complete matching input. Consume its selected
template, final status, layouts and captures. If caching is retained, scope it to
the package/parser and all matching inputs; cache relative assignments, never
absolute spans or occurrence provenance. Bind each selected region once against
the current original bytes. Preserve absence separately from present empty values.

Remove eager binding of losing candidates and subsequent rebinding of the winner.
Keep research alternatives out of the ordinary pipeline result. Internal candidate
comparison stays inside the shared selector. Retire `matching.py` and obsolete
integration code once caller checks pass.

Preserve unmatched and unresolved native evidence with explicit review disposition.
Propagate integrity, compatibility, declaration and inconsistent-result errors
distinctly. Preserve native-input/recovery failures with their evidence; do not
convert implementation failures into ordinary no-match results.

### 3. Implement the approved Error Contract

- **Definitions and values:** use existing template IDs and ordered literal/slot
  layouts. Materialize serializable definitions with source/emitter and slot
  placements/types; record-ready values carry selected layouts, ordered bindings,
  presence and components. Keep full IDs opaque. Supporting entries belong to
  one complete error.
- **Acceptance:** both selected `template` and `provisional` results are eligible,
  including provisional tie-breaks. Preserve final status rather than deriving it
  from template support. Set `error_type = unknown` and initial
  `occurrence_count = 1`.
- **Preparation:** check internal correspondence and required data using completed
  matching/binding results. Preserve one representative occurrence's original
  spans and contributing emission ordinals. Add no second recovery, matching,
  selection, binding, semantic interpretation or regrouping stage.
- **Identity:** retain deterministic equality data comprising selected template
  and literal-layout choices plus every ordered typed value and presence flag.
  Include wrapper choices and component count/order/content. Exclude timestamps,
  absolute offsets and a second emitter comparison. A digest may index the full
  equality data; Run aggregation itself is later work.
- **Rendering:** render exact literals, optional prefix/value/suffix and every
  selected component from serialized definitions/values alone. Respect framing
  order, native spelling and absence versus empty. Require no parser/model/classifier
  objects or source log, and no duplicate complete-message field.
- **Lineage:** expose `error-contract-v1` and approved Run metadata, including
  model revision, package ID/manifest hash, parser identity/hash, matcher API,
  selector and application/classifier revisions. Package lineage identifies the
  executing matcher; historical model training hashes do not substitute for it.
  Database schema version belongs to subsequent storage implementation.

Keep selected assignment, final outcome, source/emitter and unresolved provenance
available through concrete public interfaces. Retain no obsolete compatibility
aliases or independent classification hierarchy.

### 4. Verify the integrated candidate path

Use the repository Python environment and complete unmodified native logs from
the independent verification inventory. Requirements come from owner direction,
not test files. Use no synthetic inputs, altered witness templates, fabricated
negative cases or generated corrupt packages.

Replay all 31 available inventory logs through the new integration. Compare with
fresh direct-package execution: selected IDs, final statuses, layouts, ordered
captures and original-byte bindings. Account for all occurrences, including
unmatched evidence. Explain differences using native evidence; previous counts
are observations rather than optimization targets. Disclose matching caches and
verify occurrence-specific bindings independently.

Observe that recovery, matching/selection and binding occur only in their owning
stages. Exercise all nine witnessed slot types, empty/absent fields, wrappers
and continuation groups. Use actual repeated groups to prove identity equality
despite different offsets, and genuine differing values to prove distinct
identities. Serialize definitions/values and render in a separate process without
model/log access; compare with the original selected regions.

Prepare wheel resource entries for selection and every selected package artifact.
Report unwitnessed branches, including ties and malformed-input paths, as coverage
gaps.

### 5. Select, verify installation and hand off

After integrated candidate verification succeeds, update active selection to the
verified schema-2 package and align installed resources. Verify the final source
selection loads the exact package through the normal catalog. Build/install in
a disposable environment and exercise the installed catalog and pipeline on
complete native input with source-checkout and learner imports unavailable.
Verify installed selection resolves the identical package. Leave development and
production environments intact.
This selects infrastructure for the new pipeline; it does not switch legacy
application providers or enable production processing.

Deliver `docs/TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md` with actual public
symbols/signatures, definition/value schemas, identity/rendering usage, error and
review dispositions, lineage, exact selected resources, native checks and limits.
Include created/edited/deleted paths and scope proof. Identify remaining work:
Run aggregation, SQL, native-review persistence, stored reporting, the historical
comparison-tool retirement dependency and later application cutover. Carry
forward known learner/model limitations by reference; do not lose them or
implement them inside the pipeline.
