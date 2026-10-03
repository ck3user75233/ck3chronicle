# Task 07C — self-contained release delivery

Implemented retained learner distributions, authenticated explicit execution,
candidate binding, package catalog/selection and installed-resource delivery.
The new learner closure supports fresh learning, same-release incremental work,
evaluation, publication and native review. Two existing production packages execute
through the current pipeline without learner resources. Historical availability
is incomplete and is listed below; this is not a claim that every past production
version is now executable.

**Task 07 can continue using its current selected package unchanged.** The default
remains package `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`, at
`models/candidates/68f1ae5db205ab46afef9c4d`, selected by the unchanged
`models/selection.json`. No new production model was built, activated or ingested.

## Layout, identity and execution

See [RELEASES.md](RELEASES.md) for executable commands/APIs and retention policy.

```text
learners/catalog.json
learners/releases/<64-character distribution ID>/
    manifest.json
    launcher.py
    template_learning/<retained code, rules, parser and review assets>
models/catalog.json
models/releases/<24-character package ID>/<existing runtime package bytes>
models/<historical-model-ID>/<unchanged original artifacts>
models/candidates/<original-package-ID>/<unchanged original artifacts>
```

Installed equivalents are under `<sys.prefix>/share/ck3chronicle/{learners,models}`.
Snapshots contain no external executable links. The authoring owner remains
`tools/template_learning/`. The complete learner identity includes 41 files,
including parser dispatch/implementation/manifest, rules, loader, evaluation,
publication and supported review helpers. The separately retained `launcher.py`
is also pinned by the release manifest. No application or third-party package is
required by explicit-path learner execution; Python 3.11+ and stdlib are platform
requirements. Actual Python and Unicode versions are recorded in execution receipts.

Catalog fields include `family`, `release_id`, `retained_path`,
`manifest_sha256`, `availability`, `publication_status`, `production_order`, and
publication evidence. Learner rows include original fingerprint, version and
supported operations. Model rows separately identify `model_revision_id`,
`package_id`, parser, matcher API and selector. Missing historical package IDs
remain null; old model IDs have not been repurposed as executable package IDs.

The external catalog manifest pin authenticates retained payloads before launch.
The child starts with `-I -S -B`, reauthenticates, and imports authenticated source
bytes in a fresh module namespace. Missing dependencies, incompatible selection,
wrong manifest pins and candidate/release disagreements raise errors. There is no
current-source or installed-module fallback. An audit hook records dynamically
compiled project code and rejects code outside the release/platform; publication
may load its generated runtime only where its bytes equal authenticated source.

New candidate `learner_release` contains distribution ID, manifest pin and learner
fingerprint. The candidate/model retains its parser identity. Registry provenance
requires the same selected release for continuation. Evaluation loads that release's
parser/matcher; publication copies runtime code from that authenticated release.
Published model evaluation goes through the retained runtime package, classifier
and public Error Contract preparation. Data-only evidence inspection remains separate.

`native_evidence_rows` now belongs to `evidence_serialization.py`; `all_patterns`
belongs to `artifacts.py`. Their callers use those owners. Publication no longer
imports review implementation for core serialization. Parser dispatch is retained
with each learner. Configuration defaults are resolved only by the outer launcher;
the registry core takes explicit paths. Shared matcher authoring remains in
`native_matching.py` and its existing dependencies.

## Learner inventory

The following are new immutable distribution envelopes. Original historical code
and historical learner fingerprints were preserved; adding an authenticated adapter
does not relabel it as the original executable closure.

| Distribution ID | Original/complete learner fingerprint | Production order | Availability |
|---|---|---|---|
| `cdbd72475baf238d5a44a7ef37c2a266a71179d780dbaf71aa35d5a91b3d5a0f` | `d412f3e0368b0fe3a34fd161b236f98cfa5b8dd7051638fb1e0e5467e1b5475b` | 7 | Complete new closure; algorithm label remains v45 |
| `bac89011106e2fcd8e48ebc5a14f9c3dd4304e68d35d79ac3401a7c749c76f0b` | `6621d644feab8c343b76354e83900f4c82d3ae91fef03f01643d93e1f7f9909b` | 5 | Original v41; evaluation only |
| `cff09dcdc1ef6ea063c589850ad37d1d2711a52e7bc766877422ffda96e1452e` | `025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088` | 6 | Original v45; evaluation only |
| `9f25e4221f50320960db70ecbc6c2a04f0727d160469c19dd2ca65a1a44df032` | `0150da52b03a3dfd1c75e4fad3485e7f75e2c18a47d8a7a81f59a0674fe0ecd0` | None | Research v42; evaluation-only envelope, not exercised |
| `5067e83e293ae70fdd0a449a378b116ad9cbd8e74688601aaaf2cfce7328d8c7` | `8a1d1b067008a3d776b4496209e4b36c6bb7523923b28a7081be8deae216cbcc` | None | Research v43; evaluation-only envelope, not exercised |

Manifest pins in the same order:

```text
3d10ccc9a1a41acd6fb734b514dbb0a64a27e7ab4858d5e60e1a397c061f4a2d
cce56b334da8fd1896fac560c9b98646b1c080b4860b87e3618248b43d5801f4
d405b1f2b6532fe2ef4c9a5245b9b7742430aa141b12552608676a9113a9fa2a
37720e142f115f79cef9b3b1bf6b8a91ebfd4aea59d0a7cd4ada9c4841913045
53ddbb00583fb6cc7869ecc36b9d001bb11f7258e6bfb8de5c7fe0cc693670bc
```

Genuine sources found and authenticated:

- v41: `.codex-tmp/learner-refactor/continuations-v41/wheel-unpacked/template_learning/`;
  all 21 original implementation hashes match.
- v45: `.codex-tmp/learner-release-v45/source/template_learning/`; all 28 original
  implementation hashes match. Learner identity and retained source were present.
- Research v42/v43: `.codex-tmp/learner-all-logs-v42/baseline-source/template_learning/`
  and `additive-source/template_learning/`. The latter identifies itself as v43;
  its directory name is not a production-version claim.

Durable release copies are now the executable authority; those scratch paths are
provenance evidence only. Every original retained source payload is byte-identical.
Historical envelopes add only a new authenticated launcher and evaluation adapter,
which validates candidate fingerprints and executes original records/matcher/parser
code. They do not expose historical creation, incremental-registry or publication
commands: the originals lack release-bound candidate provenance and retain old
application/configuration dependencies. **Owner decision:** if those historical
producer operations are still needed, commission their closure separately with
genuine dependency recovery and explicit new distribution identity. Do not rewrite
old files or route old candidates through the new learner. Current additive learning,
publication and native review are supported by the new complete release.

Historical source search found these recorded original bytes missing across the
inspected retained source roots (not a claim about all possible external backups):

| Historical learner/model | Missing recorded implementation bytes |
|---|---|
| v25 / `b1965fa4408ca1bcf36763c9` | `clustering.py`, `owner_rules.json` |
| v26 / `1d1d6e0389f7235f565b2504` | `clustering.py`, `owner_rules.json`, `patterns.py` |
| v27 / `a9fa27a85ccd066285b99fdb` | `artifacts.py`, `clustering.py`, `owner_rules.json`, `patterns.py` |
| v29 / `0a61f6c93657948e0ca20b35` | `artifacts.py`, `clustering.py`, `owner_rules.json`, `owner_rules.py`, `patterns.py` |

These original models record implementation-file hashes but no aggregate learner
fingerprint. Partial byte matches cannot establish a complete historical closure.
They remain named `historical_unavailable` catalog entries. Genuine matching
backups could close individual missing-file gaps; none found establishes an entire
executable release. No historical campaign or evidence reconstruction was attempted.

## Production model inventory

| Package | Model | Manifest SHA-256 | Order/API |
|---|---|---|---|
| `44a0401b8adf0a2953d26705` | `76630685c4a341ca14bf9c7c` | `2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1` | 5 / `ck3-native-matcher-v1` |
| `68f1ae5db205ab46afef9c4d` | `f5cde2616f35d563118d3d32` | `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f` | 6 / `ck3-native-matcher-v2` |

Both complete packages were copied byte-for-byte from existing retained packages.
They share parser `ck3-lossless-v1.7`, SHA-256
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`, and selector
`complete-assignment-v2`. Model format 4/API v1 and format 5/API v2 both reach
the existing pipeline/contract boundary successfully. Each contains its own
matcher/bootstrap, matching primitives/validation, assignment/continuations, IDs,
parser, model, rules and validation artifact. Neither requires learner snapshots,
registry, training corpus or authoring source.

All other retained original model directories remain listed and distributed:

| Model | Status and specific missing runtime boundary |
|---|---|
| `b1965fa4408ca1bcf36763c9` | Production v25, order 1; no standalone authenticated matcher/bootstrap closure |
| `1d1d6e0389f7235f565b2504` | Production v26, order 2; same gap |
| `a9fa27a85ccd066285b99fdb` | Production v27, order 3; same gap |
| `0a61f6c93657948e0ca20b35` | Production v29, order 4; same gap |
| `67303093ecda779d` | Earlier selected empirical model; production order unknown; no versioned raw parser, complete matcher/bootstrap or native Error Contract declarations |
| `43634d23e619ecb4` | Historical empirical artifact; production status/order unverified; same empirical-format gaps |
| `93196794a7e0115d` | Historical empirical artifact; production status/order unverified; same empirical-format gaps |

For the four native historical models, missing package dependencies are
`matcher_loader.py`, `native_matching.py`, `matching_primitives.py`,
`matching_validation.py`, `full_ids.py`, `assignment.py`, `continuations.py`.
This lists the current receiving package boundary, not an invented historical
hash set. Existing parser/model/validation files do not establish the missing
executable combination. All seven fail the real `pipeline.model.load_package`
boundary with missing `matcher_loader.py`; no fallback is used.

**Bounded receiving work:** learner release inventory owns finding genuine complete
packages or original executable dependencies for these named versions. Pipeline
owners of `catalog.py`, `model.py`, `classifier.py` and `contracts.py` then assess
the recovered package/API. The smallest current action is their explicit unavailable
catalog status, already implemented. If genuine old dependencies can only be
delivered through a new package contract, supply that concrete contract and native
validation before proposing a receiving change. In particular, raw 16-character
empirical model IDs do not satisfy schema-2 package selection or Error Contracts.
No compatibility adapter or applying today's matcher is authorized as a substitute.
There is no demonstrated substantive pipeline change needed for either usable package.

## Verification performed

All generated inspection/evaluation data is in ignored
`.codex-tmp/task07c-releases/`. No synthetic native messages, fabricated models,
mutated CK3 logs or mocked matching behavior were used for parity. Disposable
corrupt copies were used only for integrity-failure tests.

Environment: repository `.venv/Scripts/python.exe`, CPython 3.12.14, Windows AMD64,
Unicode 15.0.0. The installed check used a separate Python environment and wheel
`ck3chronicle-0.0.1-py3-none-any.whl`, SHA-256
`9c0abb0b0eeb1d9b5d418dce02d1b353205a42df0069e32d8a124d02e6a4b32c`.

Native verification inputs were unmodified complete retained logs:

| Input SHA-256 | Recovered message occurrences used |
|---|---|
| `6e394b3f33fbfdacf0f40e40b2a1ab8fd4aec82a857c3732c35a27848e8e1562` | 51 |
| `dcdacdeb02c01101d88fc21af8fd1cdd96c2cf805239d8ada74156593900848a` | 543 |

1. Relocated the complete snapshot to task-owned storage. Fresh learning, first
   registry sync/build, additive second sync/build, candidate evaluation and
   publication all executed through its retained launcher with working-tree learner
   and application imports unavailable. Receipts identify loaded/compiled source
   hashes and retained JSON rules. The resulting two-log exercise covers 26 source
   families, 593 raw emissions, 594 recovered occurrences, 45 templates
   (27 supported, 18 provisional).
2. Compared snapshot evaluation with its delivered runtime on both native logs:
   51 template assignments in the first; 472 template and 71 provisional in the
   second; **1,440 captures checked, zero assignment/status/capture differences**.
   Comparison normalizes only the context dictionary identifier (`native` versus
   its exported hash), not captures or statuses.
3. A fresh one-source candidate evaluated against the multi-source log retained
   49 full and 494 unknown outcomes. No silent promotion or dropping of unknowns.
4. Explicit historical v41 and v45 selections on the same 51-emission log executed
   different retained matcher code: v41 returned 51 provisional, v45 returned 51
   full. Today's evaluator was deliberately already imported in the parent; each
   selection still executed in a fresh child with its own recorded module hashes.
5. Both production packages passed real classifier and Error Contract preparation,
   in source and from the installed wheel:

   | Package | 51-message log | 543-message log |
   |---|---|---|
   | `44a0401b8adf0a2953d26705` | 51 provisional | 337 template, 206 provisional |
   | `68f1ae5db205ab46afef9c4d` | 51 template | 485 template, 58 provisional |

   Installed verification blocked learner imports and checkout resource access
   outside the isolated task evidence area. Packages loaded only from installed
   `share/ck3chronicle/models`. All five installed learner distributions also
   authenticated against their catalog pins. The installed learner launcher then
   evaluated the fresh candidate successfully: 51 full outcomes, with selected
   code paths recorded under installed `share/ck3chronicle/learners`.
6. Native Markdown review through the complete snapshot produced 53 review files
   from the fresh candidate, including unresolved-data output. Cross-selecting a
   new candidate with v41, or a v41 candidate with the new release, failed before
   evaluation and produced no evaluation output. Bounded visual-review JSON export
   also succeeded (one template, two examples, support counts checked); the
   data-only bundle-inspection command succeeded without learner execution.
7. Ten requirement tests passed, including genuine native pipeline preparation,
   missing dependency, mutated rule, manifest mismatch, incompatible manifest,
   absent release, conflicting selectors and absent package. No deletion-policy
   tests were introduced. The active selection bytes remained unchanged.

Evidence locations:

- `verify_native.py`, `final-native/result.json`, `final-native/*execution.json`,
  `fresh.json`, `sync-*.json`, `build-*.json`, `publish.json` within `final-native/`.
- `final-native/evaluation-*.json`, `unknown-evaluation.json`, `v41-evaluation.json`,
  `v45-evaluation.json`, `pipeline-*.json` within the same directory.
- `verify_installed.py`, `installed-proof.json`, `historical-source-inventory.json`,
  `historical-runtime-gaps.json`, `final-checks.json`,
  `installed-learner-execution.json`, `installed-learner-evaluation.json`,
  `distribution-check.json`.
- `tests/test_release_selection_requirements.py`; set
  `CK3CHRONICLE_RELEASE_TEST_LOG` to a genuine retained log for the native test.

Verification-only candidate `d7f72dadf10738a01f5811ed`, compact model
`2e27ad2f001452a9b73eaeab`, package `65dd0e41a2f1197e70f00085`, manifest
`beade2b10edb8bef734b7c3935c0fa26ecdef8237522c8a96e79598cf558d59a`
remain solely in ignored output. They are not production releases or default selections.

Limits: no full campaign, no historical retraining/reconstruction, and no
cross-interpreter/OS reproducibility claim. These logs do not exercise unresolved
recovery or all continuation/ambiguity branches. Their preservation is traced in
code and receipts, not proved by absent cases. Research v42/v43 payloads authenticated
but their evaluation branches were not run. Specialized HTML/assignment-comparison
reviews and explicit different-matcher source-release repackaging were source-traced
but not functionally exercised. Such repackaging now requires fresh native validation
of the selected target; old validation cannot certify a changed matcher.

Historical campaign/research entry points such as `inspect_candidate_revision.py`,
`inspect_accumulated_corpus.py`, `inspect_incremental_learning.py`,
`inspect_native_learner.py`, `inspect_symbol_locations.py` and `mine_symbol_suffixes.py`
are not declared release operations. Calls from them into executable bundle loading
now fail without selected-release context. They have not been removed or granted a
current-code exception. Their historical exercises are evidence, not requirements
for this delivery. If owners still need those specialized rebuild/mining workflows,
identify the required command and extend the authenticated operation/closure in a
new release; do not bypass candidate binding. Current native Markdown review,
visual-review export and data-only evidence inspection have supported routes above.

## Task 07 receiving contract

Use `catalog.load_selected_classifier(package_id=...)` or
`load_selected_package(package_id=...)` for an explicit catalog selection; the
existing `selection_path` remains mutually exclusive. Omitting both preserves the
current default. `catalog.package_selection(package_id)` emits the existing schema-2
selection and never modifies the default. Do not select by model revision alone.

Persist the actual package's existing `contracts.run_lineage` fields:
`contract_version`, `model_revision`, `package_id`, `package_manifest_sha256`,
`parser` (version/hash/artifact), `matcher_api_version`, `selector_version`,
`classifier_revision`, and Task 07's actual `application_revision`. Existing package
identity identifies executable behavior; no new ingestion-side learner ID is
required. New candidate/package publication records additionally retain
`learner_release` / `publication_learner_release` for offline provenance. Ingestion
must not import learner code or reconstruct that provenance from the checkout.
SQL/playset/retention/watcher owners need no implementation changes from this task.

## Retention, changed files and preservation

Policy is at least the latest ten production learner versions and ten distinct
production model revisions with complete runtime packages. Production publication
order is explicit: native sequence v25, v26, v27, v29, v41, v45 is supported by the
delivery handoffs; the new complete learner distribution is order 7. Research
snapshots have no order. Early empirical publication order remains unknown. No
candidate time, directory timestamp, hash order or repeated activation determines
retention. No pruning, deletion commands, previews or locks were implemented;
older releases remain. Captured-log retention belongs to Task 07 independently.

Changed owning files:

- New `tools/template_learning/learner_loader.py`, `release_evaluation.py`.
- `artifacts.py`, `incremental_template_registry.py`, `evidence_serialization.py`,
  `research_matching.py`, `evaluate_unseen_session.py`, `publish_native_model.py`.
- Helper import/selected-code callers: `build_review_pack.py`, `build_visual_review.py`,
  `review_assignment_changes.py`, `inspect_incremental_learning.py`,
  `inspect_candidate_revision.py`, `inspect_outer_diagnostics.py`,
  `inspect_symbol_locations.py`, `report_script_location_stacks.py`.
- `src/ck3chronicle/pipeline/catalog.py` only within the pipeline; no changes to
  `model.py`, `classifier.py`, contracts, ingestion or storage implementation.
- `learners/catalog.json`, five `learners/releases/` distributions,
  `models/catalog.json`, two `models/releases/` byte-for-byte copies.
- `pyproject.toml` console entry points/data files; `.gitattributes` prevents
  newline normalization of authenticated release bytes.
- `tests/test_release_selection_requirements.py`, this handoff, `docs/RELEASES.md`.

The checkout already contained parallel/uncommitted work. Task-owned before hashes
in `.codex-tmp/task07c-releases/before.json` distinguish these edits from that work.
Shared distribution edits were limited to adding release entry points and resource
entries; existing default-resource entries were preserved. Shared plan/status/
CURRENT_HANDOFF files were not edited.

Final baseline checks confirm active selection, original immutable model artifacts,
application configuration and unrelated pipeline files remained byte-identical.
All 68 baseline model/selection files, 26 copied package files and 182 retained
historical source payloads were checked byte-for-byte. The wheel contains no logs,
databases, learner state or native evidence. Original historical learner source
copies were preserved. No production data or
existing Runs were modified; no production ingestion, watcher operation/configuration,
activation, release deletion, commit or push was performed. Stop here for review.
