# Task 07B — Learner dependency and version-boundary audit

2026-09-28. Audit and repair proposal only. No implementation, publication,
activation, commit or push. The companion [handoff](TASK07B_LEARNER_DEPENDENCY_VERSIONING_HANDOFF.md)
contains the Task 07 receiving guidance.

## Confirmed gaps and practical consequences

1. **The learner fingerprint does not cover the complete execution boundary.**
   `artifacts.learner_identity()` hashes 28 files, including rules and shared
   matching code. It omits `parsers/__init__.py`, although `records.collect_records`
   executes that module's recovery dispatch. Changing dispatch can change the
   recovered training/evaluation stream without changing the learner fingerprint,
   feature version or selected parser artifact. Registry/cache identity checks
   therefore do not cover that change. The parser implementation itself **is**
   retained and hashed; this is an adapter omission, not an unpinned parser.

2. **Retained learner source exists, but selection is a manually assembled
   environment rather than a complete authenticated selection contract.**
   `.codex-tmp/learner-release-v45/source/template_learning/` contains all 28
   matching files and additional helpers. `source/identity.json` records the
   existing learner identity. The release instructions explicitly select that
   directory with `PYTHONPATH`. A bounded probe successfully loaded the final
   candidate and evaluated genuine evidence entirely through that source copy.
   Thus neither “no learner identity” nor “no retained learner code” is correct.
   However, the candidate does not reference this source directory/manifest;
   ordinary CLIs select imports, not a requested learner identity. The source
   identity authenticates only 28 files. There is no complete authenticated
   launcher contract for its omitted adapters, publication helpers, execution
   environment and external build recipe. Hashing a working checkout is not
   equivalent to executing a fully selected release.

3. **Candidate evaluation can use a different matcher while reporting only
   the candidate/model and parser identities.** `load_bundle` checks current
   constructions, owner rules and the clusterer label, but not the complete
   learner hash map. `research_matching.evaluate_records` imports the current
   `native_matching.Matcher`. `evaluate_unseen_session.evaluate` reports no
   identity for that executed matcher. A change to matching mechanics with the
   same schema/rules/clusterer label can pass these gates and produce different
   results under the same reported model revision. This is a confirmed missing
   guard by source trace; no altered-code experiment was performed. By contrast,
   incremental registry loading/additive continuation checks the whole recorded
   learner identity and rejects changes to any of its 28 files.

4. **Publication selects current source for important parts of the build.**
   Normal candidate publication verifies all recorded implementation hashes
   before replay, so changing a listed matcher file produces a clear rejection.
   But `publish_native_model.py` and its `native_evidence_rows` dependency in
   `inspect_incremental_learning.py` are outside that list. They control
   compaction, validation and serialization/packaging. Source-release repackaging
   does not perform the normal reference-hash/replay checks and takes its seven
   runtime files from the executing publisher's adjacent source. Changed bytes
   create a **new package identity**, or fail compatibility; they do not silently
   alter an existing authenticated package. What is missing is an explicit
   distinction between selecting a new implementation and reproducing a package
   with the same selected inputs and tooling. The copied `native-validation.json`
   on the repackaging path is historical validation, not proof of parity for a
   changed matcher.

5. **Publication and incremental commands have an unnecessary application
   configuration dependency.** The publisher imports a streaming reader from
   `inspect_incremental_learning.py`, whose module imports the registry, whose
   module imports `ck3chronicle.config`. Config loads and validates `config.toml`
   at import time. Even publication with explicit bundle/output paths therefore
   needs the application/config environment. An isolated frozen-source import
   actually failed with `No module named 'ck3chronicle'`. The registry uses config
   for default input/state roots, not inference or matching rules. This is a
   portability and evidence-selection dependency, not runtime inference leakage.

6. **Exact rebuilding also requires recipe and interpreter provenance.** The
   retained v45 runner controls cumulative 20/20/20/13 batches, uses an external
   recovery pickle and selects the parser manifest at a checkout path. These
   inputs are described in retained preflight/identity files, but the candidate
   build command does not hash/select the runner or bind that complete recipe.
   Python's standard library is an intentional external dependency: parser and
   matching/inference code use `unicodedata.category`, while the supported Python
   range is broad and the selected manifests do not identify the interpreter or
   Unicode database used. This limits claims of exact cross-environment
   reproduction. No observed cross-Python difference is claimed.

**Task 07 can continue against the current pinned package.** No dependency from
the selected runtime parser/matcher to mutable learner code was found. Package
identity plus its externally pinned manifest determines the retained local code
and rules. This conclusion covers the parser/matcher boundary, not every
application operation: the pipeline adapter, binding and contract code remain
application-owned and need the per-Run application/classifier provenance already
in Task 07's scope.

## Inspected identities and retained artifacts

Hereafter `T/` means `tools/template_learning/`, `P/` means
`src/ck3chronicle/pipeline/`, and `R/` means
`models/candidates/68f1ae5db205ab46afef9c4d/`. These are exact repository-relative
paths, not proposed directories. The selected source is `models/selection.json`.

| Item | Existing value | Authoritative location |
|---|---|---|
| Package | `68f1ae5db205ab46afef9c4d` | Selection `package_id`; `R/manifest.json.package_id` |
| Package manifest SHA-256 | `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f` | Selection `manifest_sha256`; authenticated before code execution |
| Published model | `f5cde2616f35d563118d3d32` | Selection `revision_id`; package `model_revision_id`; model `revision_id` |
| Model bytes SHA-256 | `def3a676e7bef9f23bad5bc08e9023aedd54b4dae2ef9e46810dfe1bf1195f0c` | `R/manifest.json.hashes.empirical_template_model.json` |
| Source candidate | `c4f174d947fbc531aba35fb7` | Model `source_candidate_revision` |
| Source candidate manifest SHA-256 | `abcf350f5d0a8f6c2898ead0933dd986a5e1c73fb91efbcd4841aa16b1607c9b` | Package `source_manifest_sha256` |
| Learner | `outer-diagnostic-consensus-v45` | Model `algorithm.clusterer_version` and `algorithm.learner_identity.version` |
| Learner SHA-256 | `025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088` | Model `algorithm.learner_identity.sha256` |
| Learner file hashes | 28 entries | Model `algorithm.implementation_hashes`, repeated in `algorithm.learner_identity.implementation_hashes` |
| Feature revision | `ck3-native-message-features-v4` | Model `algorithm.feature_version`; `T/records.py:12` |
| Build strategy / threshold | `same-version-additive-v1` / `0.72` | Model `algorithm.build_strategy` / `cluster_threshold` |
| Parser | `ck3-lossless-v1.7` | Model, package and `R/parser-manifest.json` |
| Parser bytes SHA-256 | `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` | Those parser references and package `hashes.parser.py` |
| Matcher API | `ck3-native-matcher-v2` | Selection/package `matcher_api_version`; `R/native_matching.py:10` |
| Matcher implementation | Package manifest's complete executable hash set | API label alone is not an implementation identity |
| Selector | `complete-assignment-v2` | Package `selector_version`, model `assignment_policy.version` |
| Selector bytes SHA-256 | `29e3bc8f54ac678988a3dc3e0023ce7c1dc76403900a44805ef958fbd47be235` | Package `hashes.assignment.py` |
| Formats | model 5, package 1, selection 2, candidate bundle 1 | Respective `schema_version` fields |
| Application boundary | classifier `ck3-native-message-classifier-v8`; contract `error-contract-v1` | `P/classifier.py:12`; `P/contracts.py` |

`algorithm.learner_identity` is genuine historical training provenance already
protected by the model hash. The package does not need a newly invented learner
ID. `docs/TASK07_SCOPE_REVIEW.md`'s statement that an exact learner reference must
be requested is incomplete: the model already supplies it, even though the
package manifest has no top-level learner field. This audit leaves that shared
document unchanged.

### Direct answers to the five audit questions

| Question | Answer |
|---|---|
| Can runtime parser/matcher execute without learner checkout code? | **Yes.** Retained package closure, source tracing and the isolated native probe establish this boundary. Python/standard library and application adapters remain separate dependencies. |
| Can a learner revision execute independently of today's learner source? | **For retained v45, manually, yes; not as a complete authenticated identity selection.** Its source copy and documented import-path selection exist. The probe loaded/evaluated it. Ordinary entry points do not resolve a requested learner ID, and omitted adapters/recipe/environment limit reproduction. No full build was rerun. |
| Can the candidate load, evaluate and publish with those dependencies? | **Load/evaluate: demonstrated from the snapshot. Publish: requires the missing application/config environment today, and publisher dependencies are not fully pinned.** Normal listed-source drift rejects; explicit source-release repackaging instead takes the executing source and gives changed bytes a new package ID. Exact redistribution should use existing package bytes. |
| Are evaluation and released matching the same implementation/revision? | **Current core bytes match; selection guarantees differ.** Both use the shared Matcher/Rules/selector core. Runtime selects authenticated retained code; candidate evaluation uses imported source and has no complete identity gate/report. Input adapters and public output validation also differ. |
| What can Run metadata use; what is missing? | **Existing learner/model/parser/package/selector identities suffice.** Exact matcher identity is the package pin. Learner provenance is available in authenticated model data but not currently exposed by `run_lineage`; complete executable learner snapshot/recipe selection is a learner-side gap, not a missing ingestion service or new ID requirement. |

The retained final candidate is
`.codex-tmp/learner-release-v45/additive/logs-73/c4f174d947fbc531aba35fb7/`.
Its six hashed payloads are model, native evidence, parser, parser manifest,
assignment and continuations. Its `build_command` points to the retained
`run_additive.py`. The evidence JSON is 1,404,509,615 bytes; the load probe verified
its hash without executing the evidence as code. The source snapshot is a
separate sibling `source/` tree, not part of those six payloads.

## Dependency inventory and change consequences

### Learner source, rules and candidate operations

All 28 recorded files matched both today's `T/` bytes and the retained v45 source
copy at inspection. “Hashed” below means the existing 28-file learner map unless
otherwise stated. Copies in a research workspace are retained bytes, but are not
automatically selected by loading a candidate. The owning implementation remains
in `T/`; copied releases must never become another source owner.

| Exact path(s) | Caller and actual role | Ownership, pin, selection and consequence |
|---|---|---|
| `T/learn_error_templates.py` | CLI selects logs/runtime root, exclusions, parser manifest, threshold; calls inventory, records and artifacts | Learner launcher; hashed. Imported source executes. Explicit settings and input stats enter model/bundle; no learner-selection option. Changed file creates a different learner fingerprint for a new build. |
| `T/incremental_template_registry.py` | `sync`, roles, cache validation, `build_revision`, additive parent selection | Learner state owner; hashed. `load_registry` (104), `feature_key` (145), `validate_feature` (168), `build_revision` (345) check current learner identity, parser and cached data. Foreign listed code is rejected, not selected. Registry is data, not an executable learner snapshot. |
| `T/inventory.py` | Fresh CLI and registry identify/deduplicate protected inputs; streaming SHA-256 | Learner evidence owner; hashed. Paths select evidence; actual bytes are checked by `records.collect_records`. File size/mtime is also an inventory shortcut in registry sync. No inference rules are read from configuration. |
| `T/evidence.py`, `T/records.py` | Read selected parser output; construct complete records, contexts, continuations, provenance and deduplication/features | Learner feature owner; both hashed, feature version explicit. Records imports unlisted `T/parsers/__init__.py` recovery dispatch. Changed listed source rejects old registry; changed unlisted dispatch does not alter its key. |
| `T/clustering.py`, `T/patterns.py`, `T/regions.py`, `T/diagnostic_wording.py`, `T/additive_learning.py` | Artifacts invokes clustering and additive discovery; pattern/region/wording inference delegates mechanical matching to shared primitives | Learner inference owners; all hashed, current imported code executes. Dynamic imports from `artifacts.build_model` to additive code and from `regions` to `records.identity` stay inside this set. Hash changes identify new learner source; they do not retain or select it. |
| `T/owner_rules.json`, `T/owner_rules.py` | Import-time rule parsing/validation; supplies constructions, inference policy, literal guidance, parameters, cues and location-label equivalences | Learner declaration owner; both hashed. JSON rules and derived declarations also retained in candidate/model. Changing effective rules explicitly fails old candidate load and incremental continuation. Formatting-only JSON changes alter learner hash even if loaded rules are equal. |
| `T/literal_guidance.py`, `T/constructions.py`, `T/parameter_structures.py`, `T/matching_defaults.py` | Inference-facing views around `Rules(OWNER_RULES)` and guidance | Learner adapters; all hashed. `matching_defaults` selects current rules explicitly and is not packaged. These are live callers, not competing matcher implementations to delete indiscriminately. |
| `T/selection_evidence.py`, `T/template_retirement.py` | Support/selection evidence and retirement, invoked by artifact builder; shared primitives used for mechanics | Learner model-building owners; both hashed. Their outputs affect definitions/status/selection evidence and therefore model identity. |
| `T/artifacts.py` | `learner_identity`, `build_model`, `write_bundle`, `load_bundle` | Learner artifact owner; hashed, including its own code. Lines 25–43 define the file boundary. Lines 134–142 reject foreign additive source/rules/parser/threshold. Lines 236–298 retain/validate candidates but consult current rules/version. No complete implementation-hash guard on candidate load. |
| `T/evidence_serialization.py` | Dynamically imported by `artifacts.write_bundle`; streams evidence and computes digest | Learner evidence-format owner; hashed. Appropriate existing home for the currently unlisted streaming reader. |
| `T/research_matching.py` | `build_model`, unseen evaluation and inspection tools call `evaluate_records` | Learner evaluation adapter; hashed. Imports current `Matcher`; reports full/provisional/unknown with native rows. Uses model-owned rules, but does not select/verify matcher implementation bytes against the model's recorded learner. |
| `T/native_matching.py`, `T/matching_primitives.py`, `T/matching_validation.py`, `T/full_ids.py`, `T/continuations.py`, `T/assignment.py`, `T/matcher_loader.py` | Shared mechanics/public API, declaration validator, typed fields, continuation matching, complete selector and package loader | Shared matcher source owners; all seven hashed. Evaluation imports these source modules. Runtime executes retained copies pinned by package hashes instead. `Matcher` uses defensive model data and `Rules(model.owner_rules)`, not `owner_rules.py`. |
| `T/evaluate_unseen_session.py` | Loads candidate, parses protected log and calls evaluation | Unlisted learner evaluation launcher; not in 28 hashes. Result at lines 21–23 identifies model/parser, not executed matcher. Changing this adapter can change input selection/reporting independently of candidate identity. |

The declarations/settings already recorded are substantial: threshold, hard
source partition, feature/clusterer versions, build strategy, literal policy,
slot declarations, owner rules, assignment policy, parser hash, training inputs,
excluded evidence and additive parent revision. This is not a proposal to replace
those with a generic new configuration ID. Missing are the complete execution
closure and a bound recipe for reproducing a particular build. An additive
candidate's parent identity matters: final corpus membership alone does not
specify the sequence of same-version incremental updates.

### Parser artifact versus its learner adapter

| Exact path | Caller/role | Retention, identity and change consequence |
|---|---|---|
| `T/parsers/v1_7/parser.py` | `SelectedParser` dynamically executes it after hash/version checks; package executes its copied parser | Parser owner. Full executable retained under the versioned directory, candidate and package. Includes lexical rules and embedded `CROSS_EMISSION_RULES`; only standard-library imports. Different bytes fail an unchanged pin. |
| `T/parsers/v1_7/manifest.json` | Explicit CLI parser selector; `reference_from_manifest` resolves its relative artifact | Parser reference with version/artifact/SHA-256. A URI locates bytes; its hash authenticates them. No inference source selection implied. |
| `T/parsers/v1_7/recovery_rules.json` | Human-readable copy of embedded rules | Not dynamically read by parser or runtime. JSON equality with the embedded rules was verified. Editing this file alone changes documentation, not parser recovery. Prevent drift, but do not add a second runtime rule authority. |
| `T/parsers/__init__.py:18–30,48–101` | Loader, URI resolution, wrapper calls and v1.6/v1.7 recovery dispatch; records and fresh/candidate/registry paths import it | Parser adapter source; retained in v45 source copy but absent from learner fingerprint/candidate/runtime package. Parser SHA remains valid when this adapter changes. Loader executes verified bytes in `_ck3_raw_parser_<digest>`; dispatch is outside those bytes. |
| `T/parsers/v1/parser.py`, `T/parsers/v1/manifest.json` | Explicit historical parser choice, not an automatic fallback | Retained historical v1.6 path. Current matcher validates v1.7 and model schema 5; historical reader/experiment needs must be decided before removing this development path. Existing immutable packages retain their own parser. |

The isolated runtime does not call `T/parsers/__init__.py`. Its
`R/native_matching.py::iter_native_units` calls `raw.iter_recoveries()` and is
itself pinned. Thus the learner dispatch gap is not a Task 07 runtime leak.
Registry parser comparison/cache keys currently include the artifact URI as well
as version/hash: relocating identical parser bytes can reject/rekey state. That
is explicit path-sensitive behavior, not silent algorithm drift. A snapshot
launcher should keep byte identity separate from the resolver location and test
relocation without adding a fallback parser.

### Publication, review helpers and build environment

| Exact path | Caller/role | Pin/selection and consequence |
|---|---|---|
| `T/publish_native_model.py:28–57` | `compact_template` / `compact_model` choose retained fields and canonical model identity | Publisher owner, absent from learner hash list. Normal publisher executes whichever source Python imported. Changed compaction produces different model/package identities if outputs change; no exact publisher provenance is recorded. |
| `T/publish_native_model.py:59–115` | Hash-check reference implementation and compare compact matching, selected assignments, captures and totals to retained native evidence | Normal `publish` calls this before writing. Listed source drift rejects. Unlisted publisher/evidence-reader drift is not authenticated by that guard. Native validation is export parity, not unseen accuracy. |
| `T/publish_native_model.py:118–149,206–212` | Authenticate source release, then repackage | Source manifest and payload hashes checked; current schema/version contract checked. Does not call reference verification or replay. Current retained `models/` source releases have schema 3/4; this schema-5 reader rejects them. No successful current legacy repackaging is claimed. |
| `T/publish_native_model.py:166–204` | Copies seven `RUNTIME_FILES` from adjacent source; constructs matcher, package hashes/identity, immutable folder, proposed selection; reloads package | New explicit package identity for changed runtime bytes. Source model identity can remain the same. Supplied assignment/continuation payloads are overwritten by these source copies. Loader rejects conflicting existing content; publication does not activate selection. Direct callers of this function also bypass normal evidence replay. |
| `T/inspect_incremental_learning.py:30–101` | `native_evidence_rows`, imported by publisher and review/evolution tools | Unlisted streaming evidence reader: controls decoded records and occurrence counts used for publication acceptance. It is behavior relevant to validation, not merely UI. Full module also imports registry at line 17, pulling in application config even when only the reader is used. |
| `T/inspect_incremental_learning.py::inspect` | Optional experiment driver; subprocess launches registry using `sys.executable -m`, inherits Python import environment | Review/campaign orchestration, not runtime. Owns training order/checkpoints for that experiment. A claimed reproducible campaign must identify its driver/settings; no reason to package all review presentation code with runtime matching. |
| `src/ck3chronicle/config.py:24,43–60,143–160`, `config.toml` | Registry imports `ROOT_LEARNER_STATE` and `ROOT_CK3CHRONICLE` defaults at `T/incremental_template_registry.py:26,402–419` | Application path authority, not learner rules. Current import eagerly validates config even with explicit CLI roots. Changed defaults select other evidence/state or fail. Their resulting input hashes/roles are recorded, but the dependency prevents standalone publication/registry use. |
| `.codex-tmp/learner-release-v45/run_additive.py`, `inputs-all.json`, `additive/identity.json`, `preflight.json` | Delivered build's external runner, input order/batches and recovery-cache provenance | Retained evidence/recipe, not a source owner. Candidate stores command text; its manifest does not hash this runner or reference the complete preflight recipe. Runner reads a fixed external pickle and current checkout parser manifest; it checks the learner identity between batches, not the preflight snapshot digest itself. |
| `.codex-tmp/learner-all-logs-v42/batch-all-isolated/records.pickle` | Reused native recovery data in v45 runner | External derived evidence, not imported templates or runtime code. Preflight records digest `7d8ea234e1fc6594e36dd6875cee73e670e9615dd03c145c2189a82e342287d6` and claimed recovery checks. This audit did not unpickle or rerun the campaign; those historical checks were inspected, not independently reproduced. |
| `T/build_review_pack.py`, `T/build_visual_review.py`, `T/review_assignment_changes.py`, `T/inspect_candidate_revision.py`, `T/inspect_outer_diagnostics.py`, `T/inspect_symbol_locations.py`, `T/mine_symbol_suffixes.py` | Candidate readers, native-evidence viewers and comparisons; some import registry `all_patterns` or publisher compaction | Review consumers, not runtime dependencies. Candidate-load tightening/helper relocation must preserve their still-required inspection functions. Visual review additionally reads `T/template_review.html`; presentation is not matcher behavior. Migrate callers when moving helpers; do not retain a duplicate reader. |
| Python / standard library; `pyproject.toml` | All executable paths; regex, difflib, JSON, hashing, Unicode tables and serialization | External execution environment, not packaged learner code. Project declares Python `>=3.11`, no third-party runtime dependencies. Audit used CPython 3.12.14 / Unicode 15.0.0. Record these facts with verification/build receipts; do not claim arbitrary-Python bitwise equivalence. |

Normal publish and source-release repackage are materially different operations:

- **Normal publish:** candidate hash validation and current declaration/version
  checks → compact with current publisher → verify recorded 28 source hashes →
  native export parity → package adjacent shared code → package validation.
- **Source-release repackage:** authenticate old release and accepted schema →
  copy model/parser/rules/historical validation → overwrite runtime source files
  from current publisher environment → construct a new hashed package. There is
  no selected target runtime revision argument or new native replay receipt.
- **Use an existing package:** selection → authenticated package bootstrap →
  authenticated retained files. No publisher or learner is involved. For exact
  redistribution, preserve those package bytes rather than regenerate them with
  a new publisher.

The normal v45 source and seven packaged runtime files currently have equal
hashes. Packaged `owner_rules.json` has hash
`c020acb2e011b5ac5514423071667a0a491b4e87c3e01621471dda264abf8dd3`,
whereas the original learner rule file hash is
`0e03326ebc2c1a76f836b570a8b41ee2326d1f108286e7c041858856b80ce8d6`.
Publication serializes the rule object canonically; different formatting bytes
are not evidence of different effective rules. The runtime validates packaged
rules against the model's declarations.

### Delivered runtime and consumer boundary

`P/catalog.py::load_selected_package` selects the source models root or installed
`share/ck3chronicle/models`, validates selection format/path/IDs and calls
`P/model.py::load_package`. That adapter authenticates the manifest and bootstrap
before executing the **package's** `matcher_loader.py`. It does not import
`T/matcher_loader.py`.

The retained bootstrap verifies all 12 payload hashes, canonical package/model
identities, supported formats, parser pin, rules and executable API/selector
versions. It preloads `full_ids`, `continuations`, `assignment`,
`matching_primitives`, `matching_validation`, `native_matching` and `parser` into
`_ck3_matcher_<manifest_sha256>` with an empty package search path. Their imports
are standard library or relative imports of those retained modules. The
bootstrap itself is hashed and checked against the selected payload.

| Runtime payload / application path | Role and change consequence |
|---|---|
| `R/matcher_loader.py` | Retained bootstrap/parse/iteration adapter; changed bytes fail the external pin or identify a newly selected package. |
| `R/full_ids.py`, `R/continuations.py`, `R/assignment.py`, `R/matching_primitives.py`, `R/matching_validation.py`, `R/native_matching.py` | Executable shared matcher closure, including recovery-to-unit adapter; package hashes select bytes. No development-rule imports. |
| `R/parser.py`, `R/parser-manifest.json` | Retained parser executable and reference; pin agreement checked across manifest/model/parser. |
| `R/empirical_template_model.json`, `R/owner_rules.json` | Definitions, explicit policy/rules and historical learner provenance; authenticated package data supplies matcher behavior. |
| `R/native-validation.json` | Authenticated historical export-validation metadata; not matching rules or executable acceptance proof for a future repackaging. |
| `P/classifier.py`, `P/raw_input.py`, `P/bindings.py`, `P/contracts.py` | Application adapters, selected-only binding and Error Contract; outside the matcher package by design. Application/classifier revisions must describe them. No learner import found on this consumer path. |
| `pyproject.toml` data-file list | Delivers this exact package/selection to installed resources. Build configuration is an application distribution dependency, not a hidden matcher dependency. Historical installed whole-log proof is in `TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md`; not rerun here. |

Shared source and identical released implementation are separate claims. Today
the hashes establish equality of the seven shared files; source tracing shows
`evaluate_records → Matcher.inspect_record` and
`Matcher.match → inspect_record → Rules.match_record/select_assignment` use the
same mechanical core. Research evaluation projects records through `records.py`
and parser dispatch; public matching additionally validates complete units and
materializes selected regions. One is not a blanket proof of the other's input
adapter or public-output behavior. Future source changes are not automatically
selected released code, even if the API label remains unchanged.

## Ordered repair plan

These are proposed follow-up deliverables, not authorization to implement them in
this audit. All authoring stays with the existing learner/parser/matcher owners.
Retained releases and active selection remain unchanged. No compatibility layer,
automatic legacy fallback, new algorithm or pipeline redesign is proposed.

### 1. Remove incidental application/review dependencies from core operations

**Owner:** learner evidence/artifact team. **Paths:**
`T/evidence_serialization.py`, `T/inspect_incremental_learning.py`,
`T/publish_native_model.py`, `T/incremental_template_registry.py`,
`T/artifacts.py`, and their named review callers above.

Move `native_evidence_rows` to its existing evidence-format owner
`evidence_serialization.py`; update all imports and remove the old definition.
Move `all_patterns` to the model artifact owner and update review imports.
Resolve application config only in the registry CLI when omitted roots actually
need existing defaults. Explicit roots should permit use without application
imports. Preserve current default-root behavior at the launcher boundary; do not
invent an alternate config file or fallback directories.

**Deliverable/acceptance:** publication/evidence-reader imports and registry
operations with explicit disposable roots work in a clean selected-source process
without `ck3chronicle` or `config.toml`. Streaming retained native evidence yields
the same records/counts, including `retain_occurrences=True`; required visual and
comparison readers still work. No inference change. These source changes create
a new learner fingerprint; do not make old registries accept it as v45.

### 2. Turn the existing source-copy practice into an authenticated selection

**Owner:** learner artifact/launcher team, with parser adapter ownership retained.
**Paths:** `T/artifacts.py`, `T/learn_error_templates.py`,
`T/incremental_template_registry.py`, `T/parsers/__init__.py`,
`T/publish_native_model.py`, `T/evaluate_unseen_session.py`; proposed new
`T/learner_loader.py` as the single small snapshot authenticator/launcher.

Extend the existing learner identity's file map to the required execution closure:
the present 28 files, parser loader/dispatch, publication code and the evaluation
launcher. After step 1, the streaming reader is already in a hashed owner. Include
any future executable package initializer explicitly; `T/` is currently a
namespace package with no `__init__.py`. Review-only HTML and comparison reports
need not enter inference identity. Their launchers need provenance only when
their outputs are claimed as a reproducible evaluation/build.

Use `artifacts.py` to serialize an immutable learner source snapshot and manifest,
referenced by the existing `learner_identity.sha256` plus a manifest digest/location.
The manifest lists entry points, allowed files and explicit parser references;
retain the parser bytes or an authenticated retained parser artifact reference.
Use the new lightweight loader to authenticate before importing selected code,
in a fresh process with a closed import source. Never fall through to today's
learner or installed namespace-package portions. Path location locates content;
content hash determines identity. Pin the launcher code as part of the delivery.

**Deliverable/acceptance:** from a relocated snapshot, select learner identity,
parser reference and explicit evidence/roots; run a bounded fresh and incremental
build without checkout learner modules. Missing/different selected source rejects
before inference. Genuine existing snapshots with different revisions must stay
isolated. Expand the existing identity rather than create a competing learner ID.
New snapshot metadata is justified because the present identity does not resolve
the complete retained closure. Preserve v45 source/identity/package as historical
artifacts; never retrofit them to claim the new closure.

### 3. Bind candidate loading and evaluation to the selected implementation

**Owner:** learner artifacts/evaluation and shared matcher owners. **Paths:**
`T/artifacts.py`, `T/research_matching.py`, `T/evaluate_unseen_session.py`,
`T/records.py`, `T/parsers/__init__.py`, review callers, `T/learner_loader.py`.

New candidate manifests reference the selected learner snapshot and parser.
Validate recorded identity against executed snapshot before evaluating or
continuing learning. Candidate loads must not infer their source selection from
ambient rules. Separate data inspection from executing evaluation so that native
evidence remains reviewable without importing a current inference revision.
For a published-model evaluation, select the existing runtime package/bootstrap;
for an unpublished candidate, use matching modules from its selected learner
snapshot. Both continue to use the single shared implementation owners.

Evaluation receipts record the existing candidate/model identity, parser pin,
selected learner/snapshot reference or published package ID/manifest digest, and
evidence hashes. Preserve native alternatives, ambiguity, unknown and provisional
outcomes. Stop copying apparently selectable standalone assignment/continuation
files into new candidate formats once their selected snapshot owns those bytes;
current evaluation does not execute the copies. Keep historical bundles intact.

**Deliverable/acceptance:** evaluate genuine retained evidence from a selected
snapshot with checkout imports unavailable; compare complete selected assignments,
statuses/captures and unresolved accounting to that snapshot's native evidence.
Evaluation under a deliberately selected new matcher is explicitly identified as
such, never labeled merely with the old candidate ID. New format readers reject
unsupported old formats clearly; historical bundles are reviewed through their
retained historical tools, not a compatibility branch in the new implementation.

### 4. Make publication inputs and operation explicit

**Owner:** learner publication/shared matcher team. **Paths:**
`T/publish_native_model.py`, `T/matcher_loader.py`, `T/learner_loader.py`,
`T/evidence_serialization.py`, `T/verify_matcher_package.py`,
`T/verify_shared_matcher.py`, publication documentation.

Publisher consumes authenticated selected snapshot bytes, not arbitrary adjacent
source. Normal publication validates that snapshot's matcher against candidate
evidence. Keep package identity/model identity distinct and retain immutable output.
For exact redistribution, authenticate/copy an existing package byte-for-byte.
For a new matcher around retained model definitions, require an explicit target
source/package selection and a new native validation receipt for that exact
combination; historical source validation must not masquerade as validation of
the target matcher. Preserve old validation with its historical scope if useful.
Pin publisher code through the selected snapshot, not another independent
publisher version service.

**Deliverable/acceptance:** the same selected source/model/parser/recipe produces
the same canonical payload hashes and package identity; changed target source
either rejects the old selection or produces an explicitly identified new
package, validated through its own bootstrap on genuine evidence. This remains
publication, not activation. Native checks compare public matching as well as
record-level inspection; compaction parity alone is insufficient.

**Owner decision before retiring `--source-release`:** the current path provides
deliberate model-preserving repackaging but no target source pin/replay. Determine
whether that capability is still needed. If yes, replace it with the explicit
target operation above. If no, retire its reader/CLI only after confirming no
required delivery workflow depends on it. Current on-disk schema-3/4 source
releases are already rejected by the schema-5 reader; do not add a compatibility
layer to revive them. Immutable packages remain loadable through their own
authenticated bootstraps.

### 5. Bind build recipe and external environment; retain enough to reproduce

**Owner:** learner build/evidence team. **Paths:** `T/artifacts.py`,
`T/learn_error_templates.py`, `T/incremental_template_registry.py`,
`T/inspect_incremental_learning.py` when used as a campaign driver,
`T/learner_loader.py`; future task-owned build receipts.

Record exact ordered input hashes/roles, threshold, cumulative batch boundaries,
parent candidate references, selected parser/snapshot, and any reused feature or
recovery cache digest in a retained recipe referenced by the candidate manifest.
External runners that affect builds must be retained and hashed or replaced by
the owning selected entry point; timing instrumentation is metadata, whereas
batch selection and cached-record filtering affect the result. Require caches to
validate their recorded producer/input identities before reuse. Keep raw evidence
and large caches outside Git; code ownership stays under `T/`.

Record Python implementation/version and Unicode database version in build and
verification receipts. Define a supported reproduction environment rather than
claiming all Python `>=3.11` versions produce identical behavior. Reuse ordinary
version strings; no new invented environment algorithm ID is needed.

**Deliverable/acceptance:** a bounded genuine-evidence fresh/additive sequence
repeats in disposable storage from its selected source and recipe, with matching
definitions, statuses, captures and input/parent accounting. State separately
whether byte-identical candidate reproduction requires original provenance paths:
current model evidence embeds paths and those participate in candidate identity.
Do not silently normalize historical evidence paths or rewrite old revisions.
An old incomplete recipe is reported incomplete, not reconstructed by assumption.

### 6. Consumer coordination after Task 07; no learner dependency at ingestion

**Owner:** pipeline team for receiving metadata only. **Paths:**
`P/contracts.py::run_lineage`, `P/schema.py`, `P/repository.py`, `P/review.py`,
the Task 07 ingest entry point and handoff. Learner team supplies artifact fields.

Use the existing package/model/parser/API/selector identities per Run. If learner
provenance must be visible without opening the package later, copy the existing
`package.data['algorithm']['learner_identity']` (or version/SHA plus a retained
provenance object), feature version and source candidate from the authenticated
model into Run processing metadata. Do not compute learner hashes from `T/` at
ingestion. The package/model hash already transitively binds that data; this is
an exposure/storage choice, not a new identity.

`P/contracts.py:202–213` currently returns contract/model/package/manifest/parser/
matcher API/selector/classifier/application fields. `P/schema.py::LINEAGE_FIELDS`
does not yet expose learner provenance. Task 07 owns removing database-wide
lineage equality and storing component combinations per Run. Do not broaden this
audit into schema implementation. Keep application revision truthful for the
executed dirty checkout/build; an API label or stale Git HEAD alone is not exact
source provenance. Interpreter facts may accompany execution provenance after
coordination, without blocking the present pinned-package integration.

**Deliverable/acceptance:** a stored Run names the package actually used and its
existing learner provenance without importing learner code. Multiple compatible
component combinations coexist according to Task 07's approved scope. Future
learner snapshot references describe training history; ingestion never needs to
load or run a learner snapshot.

## Required-behavior and retirement decisions

- Preserve same-version additive continuation, current native review tools and
  deliberate model/package delivery. Tightening selection without an explicit
  historical-tool route could strand their retained candidates. New code should
  fail clearly; users select the retained old tool explicitly where required.
- `constructions.py`, `parameter_structures.py` and `matching_defaults.py` have
  live inference callers. They are adapters over one mechanics owner, not
  redundant matchers. No wholesale deletion is justified by this audit.
- Consolidate `native_evidence_rows` and the registry-only placement of
  `all_patterns`; remove old definitions/import paths after updating live callers.
  Do not leave compatibility aliases.
- Retire candidate assignment/continuation duplicates only in the new artifact
  contract; they are authenticated historical payloads in existing bundles.
- Resolve need for development v1.6 dispatch and `--source-release` with the owner
  before removing them. No new fallback or automatic historical format support.
- Word-run policy, capture regressions, two lost matches and Script location-stack
  investigation remain in `LEARNER_RELEASE_V45_RESULTS.md` and the current status.
  They are not repairs commissioned by this version-boundary review.

## Verification and limits

Read root/nested agent instructions, current plan/status/handoff, environment and
owner/banned-design references, delivered parser/API handoffs, source imports and
dynamic file loads, selection/package/model/candidate metadata, retained v45
source identity, recipe and release documentation. Historical evidence was used
as implementation evidence, not as a replacement for current requirements.

New execution used `.venv/Scripts/python.exe -I -S -B` and the task-owned ignored
directory `.codex-tmp/task07b-version-audit/`. [probe.py](../.codex-tmp/task07b-version-audit/probe.py),
[runtime.json](../.codex-tmp/task07b-version-audit/runtime.json) and
[snapshot.json](../.codex-tmp/task07b-version-audit/snapshot.json) retain the exact
probe and results. The complete 5,368-byte retained native input was copied
unchanged; its SHA-256 is
`6e394b3f33fbfdacf0f40e40b2a1ab8fd4aec82a857c3732c35a27848e8e1562`.

1. Runtime: executed the current pipeline authentication adapter and selected
   pinned bootstrap, verified 12 payload hashes, parsed all 51 emissions and
   matched all 51 as template. Both `template_learning` and `ck3chronicle` imports
   were explicitly blocked; no development modules loaded. This proves that
   bounded runtime path does not require the learner checkout.
2. Frozen source: selected only the retained v45 source directory under isolated
   Python; matched the 28-file learner identity, authenticated/loaded the original
   final candidate and its parser, then recovered/evaluated the same native log:
   51 full, zero provisional/unknown/unresolved, 51 contextual rows. Every loaded
   `template_learning.*` module came from that snapshot. This is not a build or
   campaign reproduction, nor a complete capture-by-capture parity claim.
3. Publication portability: importing publisher in that isolated environment
   failed at its transitive `ck3chronicle` dependency. No publish function ran.
4. Static/hash checks: selected shared source equals the seven retained runtime
   files; all 28 learner files match working source and snapshot; readable parser
   recovery rules equal embedded JSON. Candidate load verified all six payloads.

No altered source, synthetic messages, fabricated records, mutated artifacts or
mocked application were used. The import block constrained the environment; it
did not substitute matcher/parser behavior. No learner build, incremental write,
publication/repackaging, full corpus replay, wheel rebuild, SQL write, capture,
watcher action or production processing occurred. Existing historical verification
receipts were not rerun. Branches absent from the 51-emission sample, all-version
reproducibility and changed-source behavior remain source-derived conclusions or
explicit future acceptance work.

An end-of-audit hash comparison covered 150 source/artifact/configuration files
under `tools/template_learning/`, `src/ck3chronicle/`, `models/`, plus
`config.toml` and `pyproject.toml`: none changed after the read-only inspection
baseline. This supplements the task's write inventory; it does not attribute
older working-tree edits or claim to monitor all concurrent activity.

The checkout was already extensively dirty, including active selection, learner,
pipeline and shared documentation changes. Those are pre-existing/parallel work,
not this audit's changes. This task authors only the two `TASK07B_...` documents
plus ignored inspection material. It leaves source, existing artifacts, selection,
configuration, databases, watcher and shared planning/handoff files unchanged.
