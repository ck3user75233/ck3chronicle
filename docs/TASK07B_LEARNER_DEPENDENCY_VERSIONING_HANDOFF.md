# Task 07B — Version-boundary audit handoff

2026-09-28. Audit complete; repairs proposed only. See the
[audit](TASK07B_LEARNER_DEPENDENCY_VERSIONING_AUDIT.md) for dependency inventory,
source anchors, ordered acceptance outcomes and limitations.

## Task 07 disposition

**Continue against the current pinned runtime package.** No unpinned learner
dependency was found in its parser/matcher execution. `pipeline/model.py`
authenticates and executes the package's retained bootstrap. That bootstrap
verifies all payload hashes and loads its own parser/matcher closure in an
isolated namespace. A new isolated probe processed a complete genuine 51-emission
log with learner/application imports blocked: 51 template matches, no development
imports. Application binding/contracts remain covered by application/classifier
provenance; this is not proof that the whole application is inside the package.

Task 07's per-Run metadata can already use these identities. It need not await a
learner release or invent new learner/matcher IDs:

| Component | Exact existing identity and location |
|---|---|
| Package | `68f1ae5db205ab46afef9c4d`; `models/selection.json.package_id` and selected `manifest.json` |
| Manifest hash | `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`; selection `manifest_sha256` |
| Published model | `f5cde2616f35d563118d3d32`; selection `revision_id`, manifest `model_revision_id` |
| Model bytes hash | `def3a676e7bef9f23bad5bc08e9023aedd54b4dae2ef9e46810dfe1bf1195f0c`; manifest `hashes.empirical_template_model.json` |
| Source candidate | `c4f174d947fbc531aba35fb7`; model `source_candidate_revision` |
| Source manifest hash | `abcf350f5d0a8f6c2898ead0933dd986a5e1c73fb91efbcd4841aa16b1607c9b`; package `source_manifest_sha256` |
| Learner | `outer-diagnostic-consensus-v45`; model `algorithm.learner_identity.version` / `clusterer_version` |
| Learner hash | `025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088`; model `algorithm.learner_identity.sha256`, with 28 implementation hashes |
| Features / build | `ck3-native-message-features-v4`, `same-version-additive-v1`, threshold `0.72`; model `algorithm` |
| Parser | `ck3-lossless-v1.7`, SHA-256 `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`; model/manifest/parser-manifest references |
| Matcher | `ck3-native-matcher-v2` API; exact implementation is the package ID/manifest hash and payload hashes, not the API label alone |
| Selector | `complete-assignment-v2`; manifest `selector_version`; `assignment.py` hash `29e3bc8f54ac678988a3dc3e0023ce7c1dc76403900a44805ef958fbd47be235` |
| Formats/application | model 5, package 1, selection 2; classifier `ck3-native-message-classifier-v8`, contract `error-contract-v1`; record actual executed application revision separately |

Selected files live under `models/candidates/68f1ae5db205ab46afef9c4d/`.
`src/ck3chronicle/pipeline/contracts.py::run_lineage` already exposes runtime
package/model/parser/matcher API/selector/classifier/application/contract fields.
It does not expose learner provenance yet. If that provenance must survive in
SQL/review metadata independently of package availability, Task 07 can copy the
existing authenticated `package.data['algorithm']['learner_identity']` and feature
version/source candidate. **Do not import learner code or recompute learner hashes
at ingestion.** Package/model hashes already bind those fields. Future snapshot
references describe training history, not an ingestion dependency.

The “learner provenance missing” premise in `TASK07_SCOPE_REVIEW.md` is incomplete;
the fields exist in the model. Shared scope/status/handoff documents were not
edited here. Per-Run combinations, removing database-wide lineage equality and
physical schema/reset policy remain Task 07's existing work.

## Confirmed repair targets

- The 28-file fingerprint omits `tools/template_learning/parsers/__init__.py`,
  which dispatches recovery during feature collection. Parser bytes are pinned;
  this learner adapter is not part of that pin or the learner fingerprint.
- A retained v45 learner source snapshot **does exist** at
  `.codex-tmp/learner-release-v45/source/`; all 28 hashes match. Documented
  `PYTHONPATH` selection works: this audit loaded the final candidate and evaluated
  native evidence using only snapshot learner modules. Candidate selection itself
  does not authenticate/select that complete source closure.
- Candidate loading checks current rules/clusterer but not the complete learner
  fingerprint. Evaluation imports current matcher code and reports no executed
  matcher identity. Same-label source changes can therefore go unreported by
  evaluation metadata. Registry/additive identity checks are stronger and reject
  listed source changes.
- Normal publish verifies 28 reference hashes; publisher code and streaming
  evidence reader are outside that list. Repackaging uses adjacent runtime source
  without normal replay/reference checks. Changed payloads create a new package
  ID or fail compatibility; existing selected packages do not change silently.
- Publisher imports review tooling → registry → application config just to read
  evidence. Isolated publication import failed without `ck3chronicle`. Config
  controls path defaults/availability, not matching rules.
- Build order/parents/cache provenance and Python/Unicode environment must be
  retained with the recipe for an exact rebuild. Current v45 recipe/source are
  retained separately but not completely bound by the candidate selection.

## Follow-up deliverables, in order

Paths below are relative to `tools/template_learning/` unless otherwise stated.

1. **Learner evidence/artifact owner:** move `native_evidence_rows` from
   `inspect_incremental_learning.py` into `evidence_serialization.py`; move
   `all_patterns` from registry to `artifacts.py`; update publication/review
   callers and remove old definitions. Resolve config defaults lazily at registry
   CLI boundaries. Deliver standalone explicit-path imports/operations and native
   reader parity, preserving existing default-root behavior.
2. **Learner artifact/launcher owner:** extend `artifacts.py`'s existing identity
   to include required adapters/publication/evaluation code; retain an immutable
   manifest and selected source closure. Add one `learner_loader.py` authenticator
   for explicit snapshot selection before imports. Update fresh/registry launchers
   and parser selection. Deliver relocation/import-isolation verification on
   genuine evidence; preserve old v45 releases without rewriting their identity.
3. **Learner evaluation/shared matcher owner:** update `artifacts.py`,
   `research_matching.py`, `evaluate_unseen_session.py` and review callers to
   authenticate/select dependencies and report actual executed identity. New
   candidate manifests reference the snapshot/parser. Published evaluations use
   selected package bytes. Deliver complete assignment/status/capture and unresolved
   accounting checks; preserve historical native evidence inspection.
4. **Publication/shared matcher owner:** update `publish_native_model.py` and
   package verification tools so publication uses selected source, exact
   redistribution preserves package bytes, and deliberate repackaging names its
   target implementation with fresh scoped native validation. Deliver deterministic
   same-input packaging and explicitly identified changed-target results.
5. **Learner build/evidence owner:** bind retained input order/roles, batch
   boundaries, threshold, parents, parser/source and reused-cache digests to build
   receipts. Record Python and Unicode versions. Deliver a bounded reproducible
   native fresh/additive sequence; distinguish semantic parity from byte-identical
   candidate identity when evidence paths differ.
6. **Pipeline receiving owner, coordinated with/after 07:** use existing runtime
   IDs and expose authenticated learner provenance if required in per-Run records.
   Owning paths are `src/ck3chronicle/pipeline/contracts.py`, `schema.py`,
   `repository.py`, `review.py` and the Task 07 ingest entry point. No learner
   execution, selection change or new ID is required for current ingestion.

Owner decisions before breaking changes: confirm whether model-preserving
`--source-release` repackaging and development v1.6 research dispatch remain
required; if needed, explicitly select retained tools or replace the operation
with the current explicit target contract. Do not add compatibility fallbacks.
Preserve additive continuation and native candidate review. The small
construction/parameter/defaults adapters have live inference callers and should
not be mistaken for redundant matchers. Existing immutable packages/bundles stay
intact; only new candidate formats should retire redundant code copies.

## Verification and change boundary

Source/import/dynamic-load tracing, package/model/candidate metadata and retained
source hashes were inspected. New probes used CPython 3.12.14 / Unicode 15.0.0,
isolated `-I -S -B`, and one complete unchanged 5,368-byte native log. Runtime gave
51 template matches; frozen-source candidate evaluation gave 51 full and zero
provisional/unknown/unresolved. Candidate load verified its six payload hashes.
No full learner build, publication/repackaging, full-corpus replay, wheel rebuild,
SQL, watcher or production processing ran. A final comparison of 150 inspected
source/artifact/configuration files found no changes from the read-only baseline.
Changed-source and cross-environment
claims are limited to the demonstrated source boundaries, not experimental proof
of changed outcomes. Probe/results are ignored under
`.codex-tmp/task07b-version-audit/`.

This task changed only the two requested `TASK07B_...` documents and task-owned
ignored inspection material. The extensively dirty source/selection/artifact and
shared planning state predated this task or belongs to parallel work; it was not
reverted or edited. Active source, selection, configuration, existing artifacts,
databases and watcher were left unchanged. No commits or pushes. Stop here for
review of the proposal.
