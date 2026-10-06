# Combined learner / decoder release handoff

**Database replacement complete — 2026-10-05.** Production now has 31 freshly
ingested Runs under the new model: the 30 retained captures plus the session just
closed. The former database exists only in backup; no Run rows were migrated.
The natural live lifecycle and current reports are verified. See the
[replacement receipt](PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05)
and [current operational record](PIPELINE_CUTOVER.md). Older pending/held statements
below are historical.

**Production activated — 2026-10-05 09:57:58 UTC.** The owner-authorized cutover
uses the final R3 wheel and package `4ac4e8ee92346e6d14eacfbf`; no rollback.
See the [activation receipt](PIPELINE_RECEIVING.md#production-activated--2026-10-05)
and [cutover record](PIPELINE_CUTOVER.md). Existing database/Runs/evidence are
preserved. New-package live ingestion/lifecycle remains pending the next natural
unique capture; Pipeline retains the follow-up. R4 remains Reporting-owned.
Prior held/ready statements below are historical and superseded by this activation.

Updated 2026-10-05. Companion: [release README and change list](README.md).

## R3 closed; cutover held — 2026-10-05

**READY FOR OWNER ACTIVATION DECISION.** Pipeline's
[R3 receipt](PIPELINE_RECEIVING.md#r3-packaging-closed--2026-10-05) supersedes the
post-install override described in the earlier receipt below. The new wheel ships
the authenticated release default and clean-installed loading from `C:\Windows`
passes without replacement. Final wheel: `.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl`, SHA-256
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`.
Final installation: `.codex-tmp/pipeline-r3-packaging-20261005/deployment`.
Installed rollback authenticates; unchanged application/distribution bytes justify
reusing the completed independent Reporting and ingestion evidence. R3 is closed,
R4 remains Reporting-owned, and live configuration is unchanged. The
[cutover instructions](PIPELINE_CUTOVER.md) use this final artifact. The owner has
explicitly held activation; no live switch/restart or production processing occurred.

## Pipeline repair received; ready for owner decision — 2026-10-05

**READY FOR OWNER ACTIVATION DECISION.** The
[independent receipt](PIPELINE_RECEIVING.md#pipeline-repair-receiving-completed--2026-10-05)
authenticates the final Reporting wheel and closes R1/R2/R5 receiving with 35
genuine-data checks, 28 root CLI invocations and additional output-content checks.
The same learner v61/parser v1.8 package `4ac4e8ee92346e6d14eacfbf` is retained;
unchanged native processing justifies reusing original ingestion/full-corpus evidence.
No ingestion was repeated and the existing disposable database is unchanged.

Final application is the repair wheel below, hash `3b4b2088…68890`, installed at
`.codex-tmp/pipeline-reporting-receiving-20261005/deployment`. Pipeline owns and
verified the explicit new selection override and installed rollback; it retains
the exact delivered wheel with its disclosed standalone default-path limitation.
R4 new-model syntax remains separately owned Reporting work. R2's prior nonblocking
disposition stands; no further waiver was requested. The [updated runbook](PIPELINE_CUTOVER.md)
uses this final installation and refreshed read-only live observations. Keep the
production database. No live selection/configuration switch, restart, production
ingest/reset, backlog processing, commit or push. Owner activation and subsequent
natural lifecycle verification remain pending; earlier intake states are historical.

## Reporting repair application intake — 2026-10-05

**R1/R2/R5 are repaired and verified; ready for Pipeline receiving.** Use the
[new repair receipt](PIPELINE_RECEIVING.md#reporting-repair-delivered--2026-10-05)
for scope, source correspondence, genuine results, commands and remaining owners.
New wheel: `.codex-tmp/reporting-repair-20261005/final/application/ck3chronicle-0.0.1-py3-none-any.whl`,
SHA-256 `3b4b20881233174a1858b4fc960b0318555d0ef9387909ca4584c53772e68890`.
It changes only six application members; all retained learner/model/parser bytes,
pins and the dependency remain unchanged. This supersedes the original application's
Reporting defects, not its recorded identity or original receiving evidence below.

The separate final installation uses the authenticated proposed selection and
P's installed rollback selection. R3 is not fixed in the wheel; R4 new-package
syntax selectors remain unreceived Reporting work. R2's prior nonblocking status
stands. Pipeline must receive this artifact and update cutover; activation remains
the owner's decision. No production action or broader 08C completion is claimed.

## Original Pipeline receiving completed; activation held — 2026-10-05

[Receiving results](PIPELINE_RECEIVING.md) authenticate the exact final artifacts
and verify genuine handler/storage integration, native reconstruction, review
evidence, mixed-package lineage and current read-only live operations. The new
package's three receiving logs account for 172,130 units, including session 55's
44 preserved-byte occurrences. The previous-package control reports successfully.

End-to-end acceptance is held: Data Intelligence owns the demonstrated repeat-part
template-text failure (`KeyError: 'prefix'`) and surrogate export failure. New-model
syntax selectors also require Reporting receipt. The wheel's unshipped `candidates/`
default is recorded for packaging; Pipeline prepared a separate installed runtime
with the authenticated proposed selection and a valid installed rollback selection.
Default handler ingestion from that staged runtime passes on another retained
genuine log. The delivered wheel and Learner's installation are unchanged.

[Cutover instructions](PIPELINE_CUTOVER.md) retain the current database, specify
exact artifacts/processes/configuration, protect pending captures and describe
rollback/post-switch checks. No live pin switch, restart, reset or historical
processing occurred. The explicit owner restart prohibition still requires a
concrete decision. The publication section below records the original Learner
delivery; its pending-receiving statements are superseded by this receipt.

## Combined release delivered — 2026-10-05

**Learner release delivered; Pipeline receiving pending; activation pending.**
This section is the final publication evidence referenced by both catalogs.
The received planning/API sections below remain the history and owner boundary;
their future-tense integration checklist is fulfilled by these receipts.
No production ingestion/reset, service action, capture interruption, live selection
switch, commit, push or external upload occurred. Broader 08C work is not closed.

The production/v60 manifests, complete v60 learner source closure and corrected
decoder delivery were authenticated before edits. The later handoff-only change
matches the advisory receiving receipt. The owner confirmed the consultant's
findings were the delivered 08C correctives; no separate assessment was required.
Accepted source-search/excerpt edits preserve parallel work and match the reviewed
candidate text. No historical parser adapter's physical-file calls were copied.

All evidence paths in this section use repository-relative root
`.codex-tmp/combined-release-20261005` (abbreviated **OUT**). Start with
`receive.json`, `integration-review.json` and `delivery-hashes.json`.

### Final identities and Pipeline intake

| Item | Concrete intake / authenticated identity |
|---|---|
| Learner | `learners/releases/0dc8130a0740d2209e1da8e2cc7241d7d735df2c0252342075b7624bfad0e3de` |
| Learner manifest pin | `d5dffa6f9202bf6d386f27a2738ca8d0274b42971272bc8cd2550cddbbe42041` |
| Version / implementation fingerprint | `outer-diagnostic-consensus-v61` / `77a3935070c561c2de830f6577f31c189991dd93d0bce7bf0106c626a083ced7` |
| Parser | `ck3-lossless-v1.8`; SHA-256 `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Runtime package | `models/releases/4ac4e8ee92346e6d14eacfbf` |
| Package manifest pin | `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f` |
| Research revision / runtime model | `59d8130aaad3a305b9c1ba42` / `789219fdbd81c8dab950bc93` |
| Interfaces | Schema 6; matcher `ck3-native-matcher-v3`; selector `complete-assignment-v2`; classifier `ck3-native-message-classifier-v8`; contract `error-contract-v1` |
| Final application | `OUT/application-corrected/ck3chronicle-0.0.1-py3-none-any.whl`; SHA-256 `362b09b2d553f7610a1cf5e8b848000af610ef48f4c8c1b5bba739223586316b` |
| Dependency | `OUT/wheelhouse/chardet-7.6.0-cp312-cp312-win_amd64.whl`; SHA-256 `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64` |
| Source | HEAD `7b7208341469e0b5df8d739cb0fd6e805fc411ea` plus recorded dirty worktree. `OUT/application-source.json` maps actual application/resources bytes; aggregate `e47d8ed33c9301ad1b4a867d5862bf6ffdf9f7b4ac8832a08f2c352346a8020f`. |
| Installed application lineage | `sha256:34e0069e431a1c810265d655f7990e6c1c12d583f4d71f948111d59e1e477905`; this is the classifier's narrower lineage identity, not the whole-source digest. |
| Installed receipt | [OUT/installed-check-corrected/receipt.json](../../.codex-tmp/combined-release-20261005/installed-check-corrected/receipt.json); SHA-256 `a5ac3859af1746accfdddcf4dd0a43505c34bcc0a283edf10e06a91ef6205b86` |

Registration used `template_learning.learner_loader.register_release` (learner
production order **9**) then `ck3chronicle.pipeline.catalog.register_package`
(model order **8**), authenticated by the external pins above. The catalogs'
`production` publication status records availability/order, not live activation.
`OUT/publication.json` records before/after catalog hashes and exact selections;
`OUT/publish_verified.py` records the executed owner calls. Do not rerun that
registration script against populated catalogs. No retained release was edited.
All 62 files in the new retained distributions plus catalogs and the unchanged
selection were checked inside the final wheel (`application-artifact.json`).
Earlier wheels under `OUT/application/` and `OUT/wheelhouse/` are superseded
and are not intake. Final wheel/source correspondence checks all 556 included
code/resource files in both directions; no stale source files remain.

The exact proposed selection is `OUT/proposed-selection.json`:

```json
{
  "schema": "ck3chronicle.native-model-selection",
  "schema_version": 2,
  "revision_id": "789219fdbd81c8dab950bc93",
  "package_id": "4ac4e8ee92346e6d14eacfbf",
  "artifact_directory": "releases/4ac4e8ee92346e6d14eacfbf",
  "manifest_sha256": "839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f",
  "matcher_api_version": "ck3-native-matcher-v3"
}
```

The retained, still-active previous selection is `OUT/previous-selection.json`:

```json
{
  "schema": "ck3chronicle.native-model-selection",
  "schema_version": 2,
  "revision_id": "f5cde2616f35d563118d3d32",
  "package_id": "68f1ae5db205ab46afef9c4d",
  "artifact_directory": "candidates/68f1ae5db205ab46afef9c4d",
  "manifest_sha256": "2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f",
  "matcher_api_version": "ck3-native-matcher-v2",
  "integration_status": "integrated_verified",
  "handoff": "docs/TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md"
}
```

Its bytes still match `models/selection.json`, SHA-256
`d84ab9e9a1f455a7cb614b8ec9a988865df1ed36d1b68b4142da1706fdfe2e33`.
The `candidates/` path is intentional: it is the actual active selection. Previous
artifacts, including its registered release copy and earlier v58/v60 work, remain
retained. Do not activate the earlier v58 prepared selection. New records retain
their own lineage even after a later rollback.

### Decoder integration and dependency closure

Parser v1.8 uses only `decode_fragment(raw: bytes) -> str` at `Source.read_text`
and decoded header groups. The remaining native continuation conversion and
formatted-literal byte-tail conversion use the same API. It is plain
UTF-8/surrogateescape processing text: no physical-header admission, BOM removal,
detection or display/search normalization. Inverse encoding remains untouched.
Reversing only the substitutions, import and version/docstring changes reproduces
the v1.7 parser AST (`integration-review.json`, `parser.diff`). Framing, recovery,
spans and lexical behavior also pass the complete genuine-corpus comparison.

The single canonical `src/ck3chronicle/decoder.py` is retained as
`ck3chronicle/decoder.py` under the learner's ordinary authenticated manifest.
Creation requires explicit `--application-source`; `python -I -S -B` exposes only
that retained application dependency and rejects missing/ambient application or
learner imports. Old releases keep their original closures. Installed model
execution uses the installed application decoder. No separate decoder catalog,
version or selection pin was added; its file hash is ordinary artifact evidence.
Accepted decoder SHA-256:
`c31c8d6089850fb01d146b420e1c7364d86cb9287180f2e9f451861c21feb039`.

Automatic physical-source detection declares `chardet>=7.6,<8`; **7.6.0** was
verified in CPython **3.12.14**. Known-UTF-8 ingestion neither imports nor requires
the detector. The dependency download was blocked by socket policy and the pip
cache was unreadable. The supplied Windows CPython 3.12 wheel was locally repacked
from 65 installed files, each checked against its original RECORD hash
(`dependency-receipt.json`). It is not claimed to be the upstream wheel. Offline
installation and `pip check` pass; the final wheel declares the dependency.

Physical files keep `decode`/`read` and the existing header policy, including
corrected `bom_bytes`. Source-search and presentation match the accepted text;
unchanged genuine source campaigns were reused, authenticated in
`source-receiving.json`: 942 files, 941 readable, one low-confidence undetermined.
The corrective BOM receipt and installed genuine BOM/undetermined witnesses pass.
Missing genuine UTF-16/32, East Asian encoding and double-BOM positive examples
remain disclosed source-reading limits, not release gates. No extra encoding
research or synthetic cases were commissioned.

### Combined genuine verification

The new release built clean learner state from the original 73 hashes, with
20/20/20/13 stages. `OUT/build/build-basis.json`, `completion.json`,
`sync-{20,40,60,73}-execution.json`, `build-{20,40,60,73}-execution.json` and
`publish-execution.json` retain exact commands and isolated execution receipts.
No another-version registry or manual template seed was used. The final result
has **394 templates (296 supported, 98 provisional)**. Its compact templates and
summary equal v60 by measurement, while parser/learner/model/package IDs are new.

| Scope / receipt under OUT | Actual result |
|---|---|
| `parser-correspondence.json` | 73 genuine logs; 2,517,940 emissions; 2,594,588 native units. Original bytes, frames, decoded text, token spans, local/cross-emission recovery and matcher inputs agree, with each package's actual parser reference retained. The four corrective logs are within these 73. |
| Session 55 | SHA-256 `cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740`; 100,000 emissions / 100,003 native units pass parser/recovery correspondence. |
| Export `build/packages/4ac4e8ee92346e6d14eacfbf/native-validation.json` | 91,925 contextual messages / 2,594,588 occurrences / 371,403 captures; zero changed outcomes or matches. |
| `comparison.json`, `messages.json`, `stored-evidence.json` | Same retained 20 Runs: 52,899 records; 7,287 recovered contextual messages; 811,103 total occurrences including one unresolved. Candidate 798,160 template / 7,699 provisional / 5,243 no_match / 1 unresolved. Production 784,904 / 7,771 / 18,427 / 1. Gains 13,184 occurrences across 95 messages, plus 72 provisional-to-supported occurrences; no assignment losses or downgrades. |
| Stored fidelity | Zero production replay mismatches, native reconstruction failures, identity collisions or changed existing LOCATOR captures. The retained snapshot was received through the existing public-handler evidence; no production database campaign was repeated. |
| `training-corpus-comparison.json` | Same 73-log inputs and contextual IDs/counts: candidate 2,476,548 template / 118,038 provisional / 2 no_match / 0 unresolved. Transitions: 2,439,711 template-to-template; 118,038 provisional-to-provisional; 36,835 provisional-to-template; 2 no_match-to-template; 2 no_match-to-no_match. No losses/downgrades. |
| `gap-verification.json`, `literal-corrections-verification.json` | Original IS3QON three pass Classifier/prepare_record as supported. All 63 date/character cases, 16 history messages (33 occurrences), two localization messages (7 occurrences) and focused boundaries pass. No reviewed grammatical KEY captures, failed captures or template ties. |
| `formatted-verification.json` | All 71 marked-reference messages / 126 occurrences pass exact captures and reconstruction, including two enclosing-PARAM preservation cases. |
| `history-storage-verification.json`, `history-implementation-review.json` | 211 events including 43 child delta events with valid parent lineage. Streamed serialization and history owners retained. No new peak-memory claim. |
| `installed-check-corrected/receipt.json`, `installed-check-corrected/learner-execution.json` | Installed modules/resources and current contract renderer, original three and full session 55; 99,991 supported + 12 provisional, exact reconstruction and native JSON roundtrip. All 44 preserved-byte messages supported. Detector absent from known-UTF-8 ingestion. Actual isolated retained learner operation passes with the authenticated shared decoder. |
| `report-verification.json` | `CHANGES.html`: 15 added, 15 removed, 15 gained numbered examples. `FIXES.html`: 14 numbered examples. Shared patterns linked, local links/anchors valid. No new browser rendering campaign. |

Comparison tools re-lex retained real spans with each package's parser and prove
review-shard correspondence before matching. The full-corpus comparison requires
the exact package/pin and parser receipt, ties the research manifest to the runtime
package, authenticates the same training hashes and joins exact contextual IDs
and occurrence counts. It does not simply delete equality guards or relabel data.
The 20-Run and training scopes overlap; do not add counts or call them independent
accuracy estimates. Complete supported/provisional outcomes remain distinct from
unmatched and unresolved evidence. Runtime logging ownership check and development
and isolated `pip check` pass.

### Failed checks, bounded dispositions and remaining ownership

1. The first field run mistakenly consumed obsolete v55 preflight expectations
   that two history phrases should be PARAMs. Sixteen failures are preserved in
   `gap-verification-obsolete-preflight.{json,log}` and
   `focused-execution-initial.json`. The current v57 preflight correctly retains
   the literals. Rerunning only the failed field campaign passes; no product
   change or repeated completed 20-Run campaign was needed.
2. The first installed probe from `C:/Windows` stopped at the existing import-time
   configuration requirement (`installed-check-unconfigured.log`). The successful
   probe ran from `OUT/installation-context`, containing only `config.toml` and
   disposable runtime evidence. `installed-configuration.json` records the config
   hash and paths. It references genuine read-only game/source roots; it starts no
   services. Python `-I` module paths and recorded module origins exclude checkout
   source. This verifies installed loading without pretending the application is
   independent of its explicit working-directory configuration contract.
3. **Data Intelligence stored-report surrogate-display issue remains open.** The
   installed JSON, HTML and text export helpers raise `UnicodeEncodeError` on
   genuine session-55 surrogate-bearing text. The receipt labels these failed
   checks separately from passing ingestion/dependency checks. It is a focused
   real-text helper check, not a claim of complete stored-Run CLI acceptance.
   Native classifier/record preparation/reconstruction passes. Affected human
   exports require a bounded Data Intelligence repair or owner disposition during
   Pipeline receiving; decoder integration alone cannot close this issue.
4. Two activity messages remain unmatched; internally nested display formatting
   remains outside the implemented rule. Thirty-eight removed production
   alternatives have no selected witness across the two scopes. These reviewed
   limitations remain disclosed, not new commissioned fixes or independent loss
   findings. Source-reading coverage limits are as stated above.

5. Final wheel/source inventory found **54 obsolete files** carried over from an
   old setuptools build directory. The earlier runtime probe passed but did not
   detect these extra files. The rejected wheel and first receipt are retained;
   `application-stale-build-failure.json` lists every stale member. Rebuilding with
   explicit fresh build and wheel staging paths removed them. The corrected
   2,465,744-byte wheel above passes bidirectional correspondence for all 556
   included code/resource files. A new clean environment `OUT/installed-corrected`
   passes offline installation, `pip check` and the full installed genuine probe;
   final receipt is `OUT/installed-check-corrected/receipt.json`. This new artifact
   justified repeating the installed campaign. The learner/model bytes and
   completed 73-log/20-Run campaigns were unchanged and reused.

Pipeline owns final handler/storage/report receiving against these exact artifacts,
then a concrete cutover proposal. Existing live restart restrictions remain in
force until resolved with the owner in that assignment. This delivery does not
authorize activation, historical reclassification, reset or interruption of capture.

## Reproduction and intake commands

These are reproduction recipes, not a request to repeat valid campaigns. Execute
from the repository root with the repository venv; retain the completed receipts.
Use a fresh output directory for a new build or installed probe. The exact executed
stage commands are also embedded in the execution JSON files.

```powershell
$env:PYTHONPATH = 'tools;src'
$releaseOut = '.codex-tmp/combined-release-20261005'
$packagePath = 'models/releases/4ac4e8ee92346e6d14eacfbf'
$packagePin = '839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f'
$productionPin = '2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f'
$bundlePath = "$releaseOut/build/registry/revisions/59d8130aaad3a305b9c1ba42"

# Original freeze/build recipes; never overwrite retained releases.
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader create --source tools/template_learning --application-source src/ck3chronicle --output "$releaseOut/releases"
.\.venv\Scripts\python.exe -B -m template_learning.mirror_incremental_build --basis .codex-tmp/marked-references-v60-final/build/build-basis.json --release-file "$releaseOut/release.json" --output "$releaseOut/build"

# Genuine correspondence with separate authenticated parser identities.
.\.venv\Scripts\python.exe -B -m template_learning.verify_parser_correspondence --production models/releases/68f1ae5db205ab46afef9c4d --production-pin $productionPin --candidate $packagePath --candidate-pin $packagePin --basis "$releaseOut/build/build-basis.json" --additional-receipt .codex-tmp/task08c/decoder/parser-substitution-corrected/results.json --workers 3 --output "$releaseOut/parser-correspondence.json"

# Exact focused commands and successful receipt reuse are in this orchestrator.
.\.venv\Scripts\python.exe -B "$releaseOut/run_focused_checks.py"
.\.venv\Scripts\python.exe -B -m template_learning.compare_training_corpus compare --bundle $bundlePath --production-ledger .codex-tmp/production-73-v54-candidate/production-training-ledger.json --package $packagePath --pin $packagePin --parser-correspondence "$releaseOut/parser-correspondence.json" --output "$releaseOut/training-corpus-comparison.json"
.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py

# Final artifact build recipe after owner registration and packaging updates.
# The helper requires fresh build/staging paths; choose new paths on reproduction.
.\.venv\Scripts\python.exe -B "$releaseOut/build_application_clean.py"
```

Registration was performed through the two owning APIs, with the external pins,
publication orders and evidence anchor recorded above. Reproduction of registration
belongs in a disposable catalog root, not a second registration into the current
catalogs. `publish_verified.py` preserves the concrete executed calls.

For clean installed receiving, use absolute paths. The supplied dependency artifact
is specifically for Windows AMD64 / CPython 3.12. The following illustrates the
completed installation with the existing disposable context and a new probe output;
the final verified output is `OUT/installed-check-corrected`.

```powershell
$checkoutRoot = 'C:/Users/nateb/Documents/ck3chronicle'
$intakeRoot = "$checkoutRoot/.codex-tmp/combined-release-20261005"
& "$checkoutRoot/.venv/Scripts/python.exe" -B -m venv "$intakeRoot/installed-corrected"
& "$intakeRoot/installed-corrected/Scripts/python.exe" -I -m pip install --no-index --no-deps "$intakeRoot/wheelhouse/chardet-7.6.0-cp312-cp312-win_amd64.whl" "$intakeRoot/application-corrected/ck3chronicle-0.0.1-py3-none-any.whl"
& "$intakeRoot/installed-corrected/Scripts/python.exe" -I -m pip check
Push-Location "$intakeRoot/installation-context"
& "$intakeRoot/installed-corrected/Scripts/python.exe" -I -B -m template_learning.check_installed_combination --package 4ac4e8ee92346e6d14eacfbf --learner 0dc8130a0740d2209e1da8e2cc7241d7d735df2c0252342075b7624bfad0e3de --original-review "$checkoutRoot/.ck3chronicle/wip/runtime/review/ck3chronicle-schema3-20260928T211854Z/20261003-IS3QON/review.error.log" --session55-receipt "$checkoutRoot/.codex-tmp/task08c/decoder/parser-substitution-corrected/results.json" --source-survey "$checkoutRoot/.codex-tmp/task08c/random-mod-survey.json" --output "$intakeRoot/installed-check-reproduction"
Pop-Location
```

The context's existing `config.toml` is recorded by `installed-configuration.json`;
another host must supply its real read-only game/source paths and disposable
writable runtime roots under the existing configuration policy. No service startup
or production ingestion is part of this probe. Keep the old selection and artifacts
when preparing an actual cutover.

## Received baseline and original integration instructions

The remainder preserves the received baseline/API and original owner checklist.
Historical pending statements below describe preparation, not current release
status. The completed combination and remaining Pipeline boundary are above.

| Identity | Verified baseline |
|---|---|
| Active production package | `68f1ae5db205ab46afef9c4d` |
| Active production model | `f5cde2616f35d563118d3d32` |
| Active manifest pin | `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f` |
| v60 research package | `840957b2f8e16f1cf0f88ad2` |
| v60 runtime model | `8e6eed125bebfbc8b4ced145` |
| v60 package manifest pin | `1873f5b6f83c11fdd232817554343d154c9735f34398058d4057db6a0f43d288` |
| v60 research bundle | `5317ab79a799897585647fb9` |
| Frozen v60 learner | `a9cb7ae7704cfd7e6c5acf84def50dfe74440e9b913c0bf9240720dd985ebb6f` |
| Learner manifest pin | `66d6bcd105ea60fcabada86f90827a646fc00f5d102a7d6ee4f77ffe68920b01` |
| Baseline parser | `ck3-lossless-v1.7`; SHA-256 `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |
| Baseline interfaces | Native model schema 6; matcher API `ck3-native-matcher-v3`; selector `complete-assignment-v2` |

All relative paths below are from the repository root:

- Candidate package: `.codex-tmp/marked-references-v60-final/build/packages/840957b2f8e16f1cf0f88ad2`.
- Research bundle: `.codex-tmp/marked-references-v60-final/build/registry/revisions/5317ab79a799897585647fb9`.
- Frozen learner: `.codex-tmp/marked-references-v60-releases/a9cb7ae7704cfd7e6c5acf84def50dfe74440e9b913c0bf9240720dd985ebb6f`.
- Corpus/schedule: `.codex-tmp/marked-references-v60-final/build/build-basis.json`.
- Build/publication receipts: the same build directory's `completion.json`,
  `publish.log`, `publish-execution.json` and per-stage receipts.
- Retained 20-Run snapshot: `.codex-tmp/literal-v57-candidate`. Later evidence
  directories point there; they do not duplicate the actual Run documents.
- Saved production training outcomes:
  `.codex-tmp/production-73-v54-candidate/production-training-ledger.json`.

These are genuine retained inputs. Reuse the established hashes and schedule;
do not rediscover the corpus or compare a one-shot build with an incremental one
as a substitute for production-versus-candidate comparison.

## Decoder delivery: exact hookup instructions — 2026-10-05

**Corrective disposition: READY FOR LEARNER INTEGRATION.** Both receiving defects
are corrected and focused genuine checks pass. This is component readiness, not
combined-release or production activation. Use the corrected substitution below.

This is the receiving handoff for the learner team. The current implementation is
[src/ck3chronicle/decoder.py](../../src/ck3chronicle/decoder.py); the current
[design](../TASK08C_ENCODING_RECOMMENDATION.md) supersedes historical automatic-only
and candidate-voting proposals in the [08C ledger](../TASK08C_HANDOFF.md).
**The owner explicitly chose known encodings when available, detection otherwise.
The decoder has no separate release/version/pin.** The new parser, learner and
model distributions still acquire their normal new identities when code changes.

### Parser substitution

**Corrected before integration, 2026-10-05:** an internal parser span is not a
physical source file. The previously reviewed `decode(..., encoding='utf-8')`
adapter performed file-header admission and must not be copied unchanged.
Use the dedicated fragment operation below; physical-file checks remain intact.

The tested baseline implementation is
`tools/template_learning/parsers/v1_7/parser.py`, also retained inside the selected
model package. Develop the next parser through its owning source/release process;
do not rewrite a retained v1.7 artifact in place. The disposable experiment is
[parser_candidate.py](../../.codex-tmp/task08c/decoder/parser-substitution-corrected/parser_candidate.py),
with the exact [diff](../../.codex-tmp/task08c/decoder/parser-substitution-corrected/parser.diff).

Import the fragment-safe operation (the local alias is optional):

```python
from ck3chronicle.decoder import decode_fragment as _shared_text
```

Then replace only these existing decoding expressions:

| Existing location | Replacement |
|---|---|
| `Source.read_text`: `self.read_bytes(span).decode("utf-8", "surrogateescape")` | `_shared_text(self.read_bytes(span))` |
| `parse_bytes`: header groups decoded with `group.decode("utf-8", "surrogateescape")` | `_shared_text(group)` in the same generator expression |

`decode_fragment(raw: bytes) -> str` uses UTF-8/surrogateescape directly. It has
no physical-header/BOM admission, no signature consumption, no detector imports
and no normalization/substitution. It preserves leading BOM characters as span
content and round-trips all input bytes. The disposable helper adds only an
invocation counter around it; do not carry that counter into the release.

Continue passing original **bytes** to parse_bytes. Use the returned fragment str inside
the parser. Do not use display_text or working_text there, transcode the input,
rebind Source objects after parsing, or change framing, recovery, tokenization,
byte offsets or inverse `encode('utf-8', 'surrogateescape')` operations. These
are the approved narrow changes; parsing-mechanics changes need owner alignment.

### Result handling and remaining callers

- Parser fragments return a str directly, not DecodedText and not a file admission
  result. All following status/header/display metadata describes complete physical
  source-file operations (`decode`/`read`/`Decoder`), not arbitrary parser spans.
- Known codec: standard Python decoding with surrogateescape. Session 55's 44
  isolated bytes remain recoverable, while names such as Agmánd remain Unicode.
  The `preserved_bytes` warning carries a count; this is a successful read.
- `text is None`: stop this read with its supplied status/reason. Do not pass
  None downstream or reinterpret failure as an empty file or negative match.
- `display_text`: preserved bytes shown as `\xC3`/`\xC5`, suitable for UTF-8
  display. `working_text`: the same display plus CRLF/CR-to-LF normalization.
  Neither is byte-identical parser text. Keep original raw bytes separately.
- Unknown source encoding: `read(path)` without an encoding argument. BOM/strict
  UTF-8 first, then chardet's supported recommendation. Low-confidence detection
  fails explicitly. Double BOMs stop decoding; no header repair is implemented.
- `bom_bytes`: leading physical BOM bytes omitted from returned text, including
  explicit BOM-consuming Unicode codecs. UTF-8 BOM source: automatic and utf-8-sig
  report 3; plain utf-8 reports 0 and retains the BOM. No BOM or no returned text
  means 0. Endian-specific codecs retain their standard BOM-preserving semantics.
  The field is a prefix length, not an offset map; fragments have no such metadata.
- Search/excerpt candidate: [source_search.py](../../.codex-tmp/task08c/decoder/candidate/source_search.py).
  Search owns its session cache/change checks. Both consumers use working_text;
  ripgrep searches temporary UTF-8 files with `--encoding none`. Adapt these
  bounded changes to the then-current owning source service, rather than copying
  the entire older candidate over parallel work.
- `tools/template_learning/continuations.py` also contains a native UTF-8 decode
  lambda. Audit this remaining native-text caller during combined integration;
  use decode_fragment for native UTF-8 spans if consolidating it. This corrective
  does not integrate that caller. The four-log experiment replaces
  the two parser sites only; it does not claim this caller was switched.
- Existing stored-report exports have a separate surrogate-display issue recorded
  in `.codex-tmp/task08c/decoder/invalid-character-display-check.json`. Providing
  display_text does not automatically fix consumers rendering stored values.
  Do not change stored identities/captures to display escapes to work around it.

### Dependency and distribution boundary

The application module is the shared implementation, not a separately pinned
decoder product. Python provides known-codec decoding; chardet is lazily imported
only for automatic fallback. The staged dependency proposal is `chardet>=7.6,<8`
([candidate pyproject](../../.codex-tmp/task08c/decoder/candidate/pyproject.toml));
the installed version used for verification is 7.6.0. Production pyproject has
not been changed. Charset-normalizer is research evidence, not a second detector
needed by the new runtime API.

**Distribution loading remains receiving work.** The tested direct import works
in the application venv; it has not been proved inside the frozen learner's
`python -I -S -B` execution. That host currently prohibits application fallback
imports. Make the shared application dependency explicitly available through the
owning launcher/distribution mechanism, then test outside the checkout. Do not
silently reopen ambient checkout imports, copy an untracked decoder implementation
into each parser, or invent a decoder release/catalog/Run-lineage pin. If existing
isolation needs adjustment, record that bounded dependency change in this packet.

Parser bytes change, so regenerate the parser reference and new learner/model
manifests through their existing owners. Review version guards in
`parsers/__init__.py`, `learner_loader.py`, `matcher_loader.py` and native unit
projection for the chosen next parser version. Preserve each artifact's actual
digest: the disposable harness intentionally uses its candidate digest and does
not run the production matcher against falsely relabeled candidate units.

### Evidence and reproduction

For this bounded pre-integration corrective, run from any PowerShell starting
directory. These commands read retained evidence only; they do not ingest or
reclassify it, use a database, build a release or alter production selection.

```powershell
Set-Location 'C:\Users\nateb\Documents\ck3chronicle'
& '.\.venv\Scripts\python.exe' -B '.codex-tmp/task08c/decoder/check_disposable_parser.py'
& '.\.venv\Scripts\python.exe' -B 'tools/check_decoder_corrective.py' `
  --before-decoder '.codex-tmp/task08c/decoder/pre-integration-corrective/decoder_before.py' `
  --survey '.codex-tmp/task08c/random-mod-survey.json' `
  --log-receipt '.codex-tmp/task08c/decoder/parser-substitution-simplified/results.json' `
  --source-receipt '.codex-tmp/task08c/decoder/simplified-verification/sample-decoding.json' `
  --output '.codex-tmp/task08c/decoder/pre-integration-corrective/checks.json'
& '.\.venv\Scripts\python.exe' -B 'tools/check_runtime_logging.py'
```

These are workstation-local ignored evidence paths, not portable fixtures. The
one-off parser runner copies the currently selected baseline and exercises the
delivered decoder; it is a reproduction of the subteam comparison, **not** a test
of an arbitrary newly built combined package. Extend the owning release verifier
to exercise that package's actual authenticated parser and downstream classifier.

| Delivered check | Result and receipt |
|---|---|
| Actual corrected disposable parser substitution, four genuine logs | PASS: 186,704 emissions; 190,701 native matcher inputs; identical framing/text/token spans/recovery/bytes. Only candidate parser identity excluded from unit equality. [Corrective results](../../.codex-tmp/task08c/decoder/parser-substitution-corrected/results.json). |
| Session 55 regression | Included above: 100,000 emissions and 100,003 native units pass. First affected message: line 1618. Log SHA-256 `cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740`. |
| Physical source corrective | 884 genuine UTF-8 BOM files: explicit utf-8-sig bom_bytes corrected 0 -> 3, text unchanged; plain utf-8 retains BOM and reports 0. All 942 automatic text/metadata results match reviewed evidence, including one undetermined source. [Focused checks](../../.codex-tmp/task08c/decoder/pre-integration-corrective/checks.json). |
| Search/excerpts/public query (reused evidence) | 941 readable files and one low-confidence source; four equal search sets and stored-query equality. Caller bytes and sampled automatic decoder results are unchanged; no database checks rerun in this corrective. [Earlier results](../../.codex-tmp/task08c/decoder/simplified-verification/verification.json). |
| Preserved-byte display/search | All 44 Invalid character messages found, excerpt text agrees, display is UTF-8 and original processing bytes round-trip. [Results](../../.codex-tmp/task08c/decoder/simplified-display-search/results.json). |

Current corrected decoder SHA-256:
`c31c8d6089850fb01d146b420e1c7364d86cb9287180f2e9f451861c21feb039`.
Corrected disposable parser SHA-256:
`de55531bcdaa66ce7bdfbee06d489cfe45161b45c2ca9418b7bb9863493583f4`.
These are delivery/evidence identities, not a new decoder release or pin. The
[delivery hash manifest](../../.codex-tmp/task08c/decoder/pre-integration-corrective/delivery-hashes.json)
lists every corrected code/document/candidate file and verification receipt.

All four original log paths and complete SHA-256s are recorded in the corrective
results above. A genuine explicit-BOM witness is Workshop member `3655093103`,
`common/court_positions/tasks/bgp_court_positions_tasks.txt`, SHA-256
`3d93cf6154a309777d87fdb580430f69d125df54f42ae061b6cfe3cdfd0c58dc`.
The unchanged undetermined source is member `3630559851`,
`history/provinces/k_sweden.txt`, SHA-256
`89ef11bb8cb8a9ea70aab2fa022a1a5ad3622ae0c3790a08a09b0254c23341e7`.

No genuine internal double-BOM fragment was found in the supplied evidence.
The corrective verifies the fragment's direct standard-codec call graph and the
unchanged physical-header inspector by inspection; it does not manufacture a CK3
example. Explicit generic UTF-16/32 consumption uses the same signature-length
accounting, but has no genuine positive example here. These limits do not block
the known-UTF-8 fragment corrective; broader encoding work remains out of scope.

Full 73-log/20-Run classification, isolated learner distribution, installed-wheel
execution and live cutover remain unverified for the combined release. Genuine
double-BOM/header-positive, UTF-16/32 and East Asian examples were absent from the
source sample; do not label those branches tested. Follow the existing combined
verification/activation plan below. The decoder handoff does not authorize a
runtime restart, activation or parser-mechanics changes.

## Pipeline team: receiving and deployment — 2026-10-05

The decoder delivery is ready for both teams. Learner/release owns the new parser
artifact and combined package; pipeline owns consuming that package, application
dependencies, ingestion/storage verification and coordinated runtime deployment.
Use the [current 07D API handoff](../TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
for the handler contract. Do not create a second pipeline decoder or modify an
already retained parser to receive this work.

### Existing path and integration boundary

The current path is `HandlerClient.submit('ingest', ...)` -> dedicated handler
preparation -> `pipeline.ingestion._ingest` -> `Classifier.read_log` ->
selected package's `parse_file` -> pinned parser. The decisive call is
`raw = classifier.read_log(path)` in ingestion.py. Parsing/classification stay outside the database worker and SQL
transaction; only the complete prepared result reaches `write_run`.

Receive the newly built package with the shared-API decoding calls already in its
parser. Continue supplying the protected original log path/bytes. Do not preconvert
or normalize the log, change the complete-log hash used for deduplication, or pass
display_text/working_text into classification, byte-span binding, record identity,
review shards or storage. Keep the existing UTF-8/surrogateescape inverse encoding
where it reconstructs bytes or computes offsets.

Native source/log decoding is the scope. JSON transport, capture manifests and
other explicitly specified serialization codecs are not competing source decoders
and must not be changed wholesale. Capture remains byte-preserving in harvester.py.
Reports continue reading stored records rather than reopening the original log.

### Outcomes, warnings and storage

- Known UTF-8 with preserved bytes is successful processing. Session 55 and its
  44 Invalid character messages must not be rejected or downgraded merely for
  those bytes. Preserve selected/provisional/unmatched/unresolved outcomes through
  the existing classification and review rules.
- A physical-source decoder failure has no text; it must not be mistaken for
  empty input. The corrected parser fragment adapter returns a str directly and
  performs no physical-file admission. Retain existing preparation exceptions through the
  handler's `NOT_COMPLETED` result and protected-capture handling. Never convert
  it to empty input, successful partial ingestion or fabricated token errors.
  Verify this behavior at the receiving boundary; no new failure code/schema is
  required by this handoff.
- Physical-source decoder metadata includes header findings and preserved-byte
  notices; the corrected parser fragment operation returns text only and does
  not inspect headers. It does not aggregate notices
  into IngestResult.warnings or persist new warning records. Source-search warning
  propagation is a separate tested candidate. If pipeline notices are surfaced,
  use existing warning/event ownership; do not claim they already propagate.
- Keep ASCII-escaped JSON storage/transport behavior where it preserves internal
  surrogate escapes. Human-readable export needs display-safe text; it must not
  alter stored captures or identity. The separately recorded stored-report export
  limitation is not fixed merely by adopting the decoder in ingestion.

### Receiving checks and release coordination

1. Ship the shared application module with the combined application artifact and
   declare the staged `chardet>=7.6,<8` dependency for automatic source detection.
   Prove imports/package loading in the installed artifact outside the checkout.
   The decoder gets no independent version, manifest, catalog or Run-lineage pin.
2. Use the actual final authenticated package through Classifier, binding,
   contracts.prepare_record and the public handler against disposable storage with
   genuine evidence. Include session 55 and the established corpus/Run comparisons
   specified below. Verify captures, identities, occurrence accounting, review
   evidence and native reconstruction. Four passing parser comparisons alone do
   not establish ingestion/storage acceptance.
3. Verify per-Run lineage records the actual final package/parser/application
   combination. Do not relabel candidate units with the production parser digest
   to satisfy compatibility guards. Decoder adoption itself requires no historical
   reclassification or database migration.
4. Include the current contracts renderer and reporting integration in deployment
   coordination. Confirm what the running handler actually loaded; changing a
   selection file does not refresh imported application code. Runtime restarts
   remain subject to the existing owner restriction and coordinated activation plan.
5. Preserve the prior package and selection for rollback and historical records.
   Use the existing runtime logger/event helpers and run the ownership check;
   the decoder must not configure logging handlers.

The exact API adapter, genuine evidence paths, commands and limits are above.
Neither this handoff nor its documentation links claim that pipeline receiving,
end-to-end ingestion or production cutover has already happened.

## Receive and integrate the decoder

1. Read the delivered hookup section above and reconcile it with the current
   [08C handoff](../TASK08C_HANDOFF.md). Record API entry points, result/failure
   semantics, dependency versions, caller ownership and exact evidence paths.
   Its 2026-10-05 update uses known encodings when available and detection otherwise;
   `decode_fragment` is the header-free UTF-8/surrogateescape parser path;
   physical-source `decode`/`read` and Decoder retain file-header admission.
   The disposable dependency proposal is
   `chardet>=7.6,<8`. Receiving review must confirm the final delivered arrangement.
2. The latest subteam note reports four genuine disposable-parser checks passing:
   186,704 emissions and 190,701 native matcher inputs, including session 55's
   100,000 emissions / 100,003 native units. Matching/classification downstream
   was not rerun. Evidence is under
   `.codex-tmp/task08c/decoder/parser-substitution-corrected/results.json`.
   Earlier automatic-selection code failed on session 55's first `Invalid character`
   message (ordinal 1617 / line 1618); those receipts are historical, not the
   current result. Retain that regression case in combined verification. Distinguish
   processing text from `display_text` byte escapes and `working_text` newline
   normalization; display/search convenience output must not replace parser input.
3. Integrate the agreed decoding calls into the owning parser/callers without
   unrelated parsing-mechanics changes. Preserve original bytes, framing, spans,
   token boundaries, continuation recovery and reconstruction. Record any actual
   changed decoding/output explicitly and assess downstream effects.
4. Resolve dependency/distribution loading according to the decoder handoff.
   Existing frozen learner execution uses `python -I -S -B` and rejects application
   fallback imports. Merely importing a checkout module or installing a dependency
   in the development venv does not prove the retained learner/package works.
   Verify the agreed arrangement in both the isolated learner and installed
   application. The decoder itself must remain unversioned/unpinned as directed
   by the owner; normal application distribution identity still applies.
5. Freeze new executable bytes and parser reference metadata; never edit the
   existing production, v58 or v60 distributions. Rebuild fresh learner state
   with the same 73 logs and incremental schedule. New code must not inherit
   old registries or use production templates as cross-version seeds.

## Combined verification and comparison

The baseline commands/tools are reusable, but their parser assumptions need
receiving work before a decoder/parser change:

- `compare_production_candidate.py` currently asserts equal production/candidate
  parser references. Preserve each package's actual identity and compare its own
  parse/recovery output. Do not remove the assertion and relabel candidate inputs
  as production inputs without proving correspondence to native evidence.
- `compare_training_corpus.py` joins saved assignments by contextual message ID
  and occurrence count. Reuse the saved production ledger only where that join
  remains valid. Account explicitly for changed identities, recovery or decoded
  text; unchanged log hashes alone do not prove unchanged matcher inputs.
- Existing verification evidence must be regenerated for the new executable
  combination, not copied as its acceptance receipt.

| Check | Required evidence from the combined release |
|---|---|
| Decoder/parser | Genuine corpus, including session 55; exact bytes/spans/recovery comparisons and documented intentional differences. No fabricated diagnostic fixtures. |
| Learner/build | New immutable release; authenticated parser/dependencies; 20/20/20/13 receipts for the established 73 logs. |
| Classification | Production comparison on the same retained 20 Runs and all 73 training logs; supported, provisional, unmatched and unresolved outcomes reported separately. |
| Original failures | All three `20261003-IS3QON` diagnostics through public classification and record preparation. |
| Fields and identity | Date literals, short/full character forms, receiver/location fields, history wording, REASON/PARAM boundaries, exact control characters, repeated locator order/count and contextual Unknown. |
| Marked references | Repeat the 71-message focused check, including larger quoted PARAM preservation. Any added nested-formatting support gets its own genuine evidence. |
| Learning history / memory | Parent-linked deltas and streamed writer remain intact. Changed decoder packaging must not restore complete-model copying or producer reload. |
| Human report | 15 added samples, up to 15 removed templates grouped with their successors, and 15 newly classified examples; semantic changes and locator-layout-only changes distinguished. Number examples and link repeated patterns. |
| Installed resources | Final application artifact can load the authenticated package/learner and decoder dependencies outside checkout assumptions. Exercise actual classifier and contract renderer. |
| Runtime logging | Run `tools/check_runtime_logging.py` for runtime changes, following the existing logger ownership. |

Existing check owners include `verify_gap_candidate`, `verify_literal_corrections`,
`verify_formatted_references`, `compare_production_candidate`,
`compare_training_corpus`, `report_formatted_references` and
`report_production_comparison` under `tools/template_learning/`. Use the repository
venv and `PYTHONPATH=tools`; pass the new artifact paths explicitly. Keep generated
evidence outside Git and update the README with actual combined results.

## Publish, install and activate

Use the existing [release registration workflow](../RELEASES.md). The final
publication record needs the source/application artifact identity, learner and
parser identities, decoder arrangement/dependencies, model/package IDs, external
manifest pins, verification receipts and exact proposed/previous selections.
Determine production publication order from the catalogs at that time.

Register authenticated final distributions through the owning learner/model APIs.
Update packaged resource entries and build/verify the final application artifact;
registration alone does not update an existing wheel or the active selection.
The earlier v58 wheel is not the combined release.

Application `pipeline/contracts.py` must ship with the new package: it renders
repeated location layouts and exact date-literal choices. Pinning only a new model
does not replace code already imported by a running database handler. There is no
planned historical reclassification or database migration for the verified v60
changes; reassess only if the decoder handoff establishes a new requirement.

The owner intends a replacement after integration. Do all concrete preparation
and verification first. The earlier explicit runtime-restart prohibition has not
been lifted by this documentation request; resolve that operational point when
the final coordinated activation is ready. Do not request model-by-model or
template-by-template approvals. Record actual loaded package/application lineage
at activation rather than assuming a changed file refreshed a running process.

Retain the previous production selection and complete package for rollback, and
retain the renderer capable of reading records created with the new layouts.
Reverting a selection does not undo new Run records; preserve their lineage and
referenced packages. Do not rewrite source logs, existing Runs or review shards.

## Completion ledger — final disposition

| Deliverable | Status |
|---|---|
| Cumulative improvements and exact combined results | Delivered in README and final receipts above |
| Decoder corrective receipt / narrow integration | Authenticated and integrated; full genuine preservation checks pass |
| Integrated parser/dependency closure and new frozen learner | Delivered v1.8/v61, learner order 9 |
| Combined incremental build and production comparison | Completed 20/20/20/13, same 20 Runs and 73 logs; no observed losses/downgrades |
| Human report and immutable publication record | Delivered; model package order 8; concrete intake and external pins above |
| Final application artifact / installed-resource checks | Passed for installed ingestion, contract reconstruction and dependency closure; separate export failures disclosed |
| Data Intelligence surrogate export repair / disposition | Pending with Data Intelligence / owner; not closed by decoder integration |
| Pipeline handler/storage/report receiving | Pending on the final combination |
| Coordinated activation and active lineage | Pending; original selection and running services unchanged |

Known limitations remain release notes rather than newly commissioned requirements.
This README/HANDOFF pair remains the release record; no parallel release ledger
was created.
