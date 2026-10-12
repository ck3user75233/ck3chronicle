# Learner storage and version map — 2026-10-09

**Later Owner-issued cleanup completed:** the 184 remaining research payloads
described below have now been removed, reclaiming **42,794,174,357 bytes**.
`learner-refactor` now totals **6.23 GB**, with its four historical release-copy
model files (**7.20 MB**) preserved. The historical registry-base and v41 research
replay questions are dispositioned by that explicit retirement. All other file
bytes in the subtree were preserved. See the updated
[cleanup receipt](LEARNER_RECLAMATION_RECEIPT_20261009.md).
**The following tables are the preserved pre-cleanup snapshot**, not current
remaining sizes or an outstanding clearance list. Other roots were not deleted.

This is an explanatory, read-only follow-up to the [cleanup receipt](LEARNER_RECLAMATION_RECEIPT_20261009.md).
No additional deletion or product operation was performed. Sizes below are fresh logical file bytes, expressed as decimal GB (1 GB = 1,000,000,000 bytes). No reparse traversal; inventory reported zero filesystem errors. This measures file sizes and reads model version metadata, not fresh authentication or dependency clearance of every payload.

## Reconciling the scale

The eleven largest Learner clusters in the main table below total **114.36 GB now**. Adding the completed **11.62 GB** cleanup gives approximately **125.98 GB before cleanup**, close to the recalled 127 GB. This reconstructs the scale; it does not establish which exact earlier category was quoted as 127 GB.

The saved Advisory JSON-only inventory records **133.11 GB (123.97 GiB)** across its measured scope. Its different coverage includes other JSON evidence, so it is not the same number as those eleven complete folders. Saved total `.codex-tmp` size was **159.33 GB**; the fresh total is **147.83 GB**, including non-Learner work. Concurrent files/accounting prevent attributing every total change to this cleanup. Do not add parent and child table rows.

## What pending clearance actually means

1. **Explicit protection:** the active October 5 installation, combined v61 evidence, Task09 baseline, Task10 evidence, published components and original inputs were excluded from deletion by the Owner. Their protection does not require guessing whether an old experiment is still used.
2. **Specific evidence dependency:** v57 holds shared original Run documents; the v54 production-training ledger is reused; v60 and v45 are named build/comparison lineage. Those facts protect the required files, not automatically every multi-gigabyte payload in their folder.
3. **Historical registry or evaluation question:** the old at-symbol registry still selects e6aee7..., while the v41 bundle is the source of historical published/evaluation evidence. Whether those full research bundles must remain loadable has not been dispositioned.
4. **Unreviewed or outside scope:** most other payloads have no established active dependency from this cleanup. They were not individually cleared. The optional removal authority covered only generated research payloads inside `learner-refactor`; it did not authorize deleting the large v42-v61 sibling folders. Feature-cache expiry was explicitly reserved for later scope.

There is no generic team-signoff queue behind these words. The remaining work is file-specific: identify the current consumer and what it actually reads; distinguish provenance citations from full-bundle loading; preserve original/shared evidence; and record retirement where a full historical replay is no longer required.

The packaged loaders for retained model `44a040...` and current `2b129...` read and authenticate their own listed package files. They do **not** load the old v41 research directory merely because their metadata records its source. Thus the v41 retention question is historical evaluation/evidence availability, not a demonstrated Watcher runtime dependency. Likewise the e6aee7... selection is in a September research registry, not the live model selection. Earlier clearance wording should be read with this distinction.

## Understanding the numbers and identifiers

| Label | Meaning |
|---|---|
| Algorithm v41, v45, v54, v61 | Learner inference implementation generation, read here from `algorithm.clusterer_version`; not an application version or number of logs |
| SC / SM / OD below | Full prefixes `source-component-consensus`, `source-message-consensus`, `outer-diagnostic-consensus`; preserve these namespaces when identifying old experiments |
| `logs-20`, `logs-40`, `logs-60`, `logs-73` | Corpus size at a cumulative checkpoint; several checkpoints can share one algorithm version |
| 24-character research revision | Exact research bundle/model identity, such as `d729dea94d84323b8497e882`; not a sequential version |
| Model package ID | Immutable exported runtime model identity: live `4ac4e8ee92346e6d14eacfbf`; repository/Task09/Task10 `2b12932103f3a3111a4e1880` |
| 64-character Learner release ID | Exact retained executable distribution; logging/packaging changes can change this while the algorithm remains v61 |
| Parser v1.7/v1.8; matcher v3; schema 6 | Separate parser/interface/data-format versions, not Learner generations |
| Application 0.0.1/0.0.2 | ck3chronicle application package versions; distinct from Learner algorithm and model IDs |
| Publication orders 9/10; Windows C9 | Catalog sequence numbers and distribution candidate number; neither is Learner v9/v10 |
| `final`, `candidate`, `production` in a directory name | Historical purpose/name; current selections and received manifests establish authority |

Both current model authorities use **v61**. The October 7 build changes authenticated provenance/logging identities relative to October 5, while the documented comparison preserves native evidence and behavior-bearing model content. Different package IDs do not by themselves mean a new inference algorithm.

## Largest Learner clusters

All paths in this table are relative to `.codex-tmp/`. “Payload” means the exact basenames `empirical_template_model.json` and `native_evidence.json`; a few folders also contain compact packaged models with that same model basename. It is not a deletion allowance. Logs, reports, native snapshots, environments and compact releases account for the remaining folder bytes.

| Folder | Total GB | Model/native payload GB | Feature-cache GB | Observed algorithm versions | Role / clearance |
|---|---:|---:|---:|---|---|
| `learner-refactor` | 49.02 | 42.80 | 1.94 | SM v1; SC v2/v7-v12; OD v14-v41 (multiple experiments) | Within prior cleanup scope for individually cleared generated payloads only. Contains canonical inputs and a selected historical registry; remaining 188 payload files were not all reviewed. |
| `learner-all-logs-v42` | 7.94 | 6.70 | 0.20 | OD v42, OD v43, OD v44 | Historical v42-v44 campaigns; outside prior deletion scope. Preserve original inputs, frozen-source provenance and evaluation records; review each research checkpoint separately. |
| `production-incremental-v54-candidate` | 6.63 | 4.24 | 1.31 | OD v54 | Superseded same-schedule v54 experiment and review evidence. Outside prior deletion scope; full-payload need not yet individually assessed. |
| `learner-release-v45` | 6.63 | 4.50 | 0.00 | OD v45 | Published v45 lineage and 20/40/60/73 historical bundles named in current build-basis schedules. Outside prior deletion scope; distinguish historical comparison bundles from originals, source and compact published artifacts. |
| `literal-v57-candidate` | 6.58 | 4.22 | 1.31 | OD v57 | Superseded algorithm but contains actual retained 20-Run documents referenced by later evidence. Protect those shared documents; do not equate them with every research payload. Outside prior deletion scope. |
| `owner-gaps-v56-candidate` | 6.56 | 4.22 | 1.31 | OD v56 | Superseded owner-gap experiment; review reports/outstanding historical evidence separately from payloads. Outside prior deletion scope. |
| `combined-release-20261005` | 6.28 | 4.24 | 1.31 | OD v41, OD v45, OD v58, OD v61 | Explicitly protected. Current live v61 delivery evidence; later Task09 comparison reuses this build and its native outcomes. Contains small packaged copies of older model versions too. |
| `coupled-words-v58-candidate` | 6.21 | 4.22 | 1.31 | OD v58 | v58 research and published/prepared replacement lineage; never activated as final combined release. Preserve published components; research payloads not individually cleared. Outside prior deletion scope. |
| `marked-references-v60-final` | 6.19 | 4.22 | 1.31 | OD v60 | v60 baseline explicitly named by combined v61 handoff: bundle, schedule, package, receipts. Outside prior deletion scope; assess retained comparison use separately from runtime use. |
| `marked-references-v59-final` | 6.18 | 4.22 | 1.31 | OD v59 | Superseded v59 final research campaign; final means final for that experiment, not currently active. Outside prior deletion scope. |
| `trek2-baseline-20261007` | 6.14 | 4.22 | 1.31 | OD v61 | Explicitly protected. Adopted v61 Task09 full 73-log model, four cumulative checkpoints, original inputs and logging/receiving evidence. |

## Inside learner-refactor

The folder now contains **49.02 GB**: 37.42 GB of native evidence, 5.38 GB of model JSON, 1.94 GB of feature caches, 1.53 GB of log files (including inputs/journals), and 2.75 GB of other files. Original inputs and feature caches remain outside the payload deletion scope. Algorithm labels here describe surviving models; removed pairs are recorded separately below.

| Subfolder | Total GB | Model/native payload GB | Observed algorithm versions | Disposition |
|---|---:|---:|---|---|
| `empirical-regions` | 8.713 | 8.575 | SC v11-shortcut-removed, SC v12-empirical-regions, OD v14, OD v15, OD v16, OD v17, OD v18, OD v19, OD v20, OD v21, OD v22, OD v23, OD v24, OD v25, OD v26, OD v27 | Not individually dependency-cleared; size/version inventory only. |
| `at-symbol-incremental-review` | 5.684 | 3.644 | SC v2 | Protect original 73-log input tree; historical registry selects e6aee7...; review selected-base retirement separately. |
| `diagnostic-wording-v39` | 3.613 | 3.610 | OD v39 | Not individually dependency-cleared; size/version inventory only. |
| `single-assignment-v38` | 3.281 | 3.268 | OD v38 | Not individually dependency-cleared; size/version inventory only. |
| `symbol-slot-loss-v40` | 3.257 | 3.256 | OD v40 | Not individually dependency-cleared; size/version inventory only. |
| `symbol-location-review` | 2.783 | 2.769 | SC v7, SC v8, SC v9 | Not individually dependency-cleared; size/version inventory only. |
| `full-id-followup-v34` | 2.027 | 1.547 | OD v34 | Not individually dependency-cleared; size/version inventory only. |
| `incremental-review` | 1.992 | 0.926 | SM v1 | Not individually dependency-cleared; size/version inventory only. |
| `version-isolation-v30` | 1.695 | 1.633 | OD v30 | Not individually dependency-cleared; size/version inventory only. |
| `param-boundaries-v32` | 1.664 | 1.626 | OD v32 | Not individually dependency-cleared; size/version inventory only. |
| `wording-loss-v31` | 1.615 | 1.615 | OD v31 | Not individually dependency-cleared; size/version inventory only. |
| `no-coverage-v36` | 1.550 | 1.546 | OD v36 | Not individually dependency-cleared; size/version inventory only. |
| `full-ids-v33` | 1.550 | 1.548 | OD v33 | Not individually dependency-cleared; size/version inventory only. |
| `single-sweep-v35` | 1.548 | 1.540 | OD v35 | Not individually dependency-cleared; size/version inventory only. |
| `no-adjectives-v37` | 1.546 | 1.546 | OD v37 | Not individually dependency-cleared; size/version inventory only. |
| `continuations-v41` | 1.417 | 1.415 | OD v41 | Historical published/evaluation source; no demonstrated runtime load of this research directory. |
| `param-boundary-review` | 1.225 | 0.922 | SC v10 | Not individually dependency-cleared; size/version inventory only. |
| `adjective-ablation-v36` | 0.997 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `key-word-evidence-v39` | 0.715 | 0.715 | OD v39 | Not individually dependency-cleared; size/version inventory only. |
| `location-label-release` | 0.361 | 0.357 | OD v29 | Not individually dependency-cleared; size/version inventory only. |
| `separator-learner-review` | 0.360 | 0.309 | SC v9 | Not individually dependency-cleared; size/version inventory only. |
| `near-literal-review` | 0.358 | 0.357 | OD v28 | Not individually dependency-cleared; size/version inventory only. |
| `compound-identifiers-survey` | 0.161 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `adjective-review` | 0.122 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `literal-wording-survey` | 0.121 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `default-literals-review` | 0.097 | 0.000 | default-literal generation; exact algorithm label unverified in this follow-up (removed payloads) | Payload pair retired; retained reports/manifest remain. Do not delete folder. |
| `explicit-literal-guidance-review` | 0.095 | 0.000 | SC v5 (removed payloads) | Payload pair retired; retained reports/manifest remain. Do not delete folder. |
| `character-full-id-inventory` | 0.069 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `literal-context-review` | 0.068 | 0.000 | SC v4 (removed payloads) | Payload pair retired; retained reports/manifest remain. Do not delete folder. |
| `tighter-groups-review` | 0.064 | 0.000 | intermediate grouping revision; exact algorithm label unverified in this follow-up (removed payloads) | Payload pair retired; retained reports/manifest remain. Do not delete folder. |
| `final-review` | 0.055 | 0.039 | SM v1 | Not individually dependency-cleared; size/version inventory only. |
| `tighter-wording-review` | 0.044 | 0.000 | SC v7 (removed payloads) | Payload pair retired; retained reports/manifest remain. Do not delete folder. |
| `verified` | 0.036 | 0.019 | SM v1 | Not individually dependency-cleared; size/version inventory only. |
| `default-literals-73-log-review` | 0.034 | 0.000 | cumulative default-literal generation; exact algorithm label unverified in this follow-up (removed payloads) | Payload pair retired; retained reports/manifest remain. Do not delete folder. |
| `examples` | 0.025 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `reason-composition-investigation` | 0.024 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `model-bugs-audit` | 0.012 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `direct-cli-final` | 0.010 | 0.010 | SM v1 | Not individually dependency-cleared; size/version inventory only. |
| `candidates` | 0.010 | 0.010 | SM v1 | Not individually dependency-cleared; size/version inventory only. |
| `lark-evaluation` | 0.007 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `single-assignment-review` | 0.003 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `boundary-fix-verification-v2` | 0.002 | 0.000 | SC v2 | Not individually dependency-cleared; size/version inventory only. |
| `separator-fix` | 0.001 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `boundary-investigation` | 0.001 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `boundary-fix-verification` | 0.001 | 0.000 | SC v2 | Not individually dependency-cleared; size/version inventory only. |
| `trace-boundary-fix` | 0.001 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |
| `multi-log-review` | 0.000 | 0.000 | No surviving model version read; see role/name | Reports/surveys or other material; no model version inferred solely from folder name. |

## Empirical-regions subexperiments

These rows are already included in the 8.71 GB empirical-regions row above. All remain individually unreviewed for removal.

| Subexperiment | GB | Observed algorithms |
|---|---:|---|
| `empty-reason-twenty-02` | 0.789 | OD v26 |
| `outer-development-8` | 0.513 | OD v14 |
| `punctuation-development-01` | 0.507 | OD v17 |
| `outer-development-10` | 0.492 | OD v15 |
| `outer-development-11` | 0.492 | OD v16 |
| `empirical-delivery` | 0.442 | SC v12-empirical-regions |
| `empirical-final` | 0.441 | SC v12-empirical-regions |
| `empirical-reviewed` | 0.440 | SC v12-empirical-regions |
| `empirical-discovery` | 0.438 | SC v12-empirical-regions |
| `trace-boundary-review` | 0.362 | OD v27 |
| `trace-development-02` | 0.349 | OD v19 |
| `trace-development-01` | 0.349 | OD v18 |
| `no-guidance-development-01` | 0.339 | OD v20 |
| `typed-fields-development-01` | 0.335 | OD v22 |
| `region-first-development-01` | 0.334 | OD v21 |
| `publication-development-01` | 0.332 | OD v25 |
| `param-evidence-development-01` | 0.331 | OD v24 |
| `param-evidence-development-02` | 0.331 | OD v24 |
| `empty-reason-ten-02` | 0.331 | OD v26 |
| `qualified-fields-development-01` | 0.330 | OD v23 |
| `removal-baseline` | 0.309 | SC v11-shortcut-removed |
| `typed-fields-diagnostics` | 0.032 | No surviving model version read; see role/name |
| `trace-delivery` | 0.006 | No surviving model version read; see role/name |
| `param-evidence-delivery` | 0.003 | No surviving model version read; see role/name |
| `no-guidance-delivery` | 0.003 | No surviving model version read; see role/name |
| `punctuation-delivery` | 0.003 | No surviving model version read; see role/name |
| `outer-delivery` | 0.002 | No surviving model version read; see role/name |
| `empty-reason-review` | 0.002 | No surviving model version read; see role/name |
| `publication-review` | 0.001 | No surviving model version read; see role/name |
| `typed-fields-delivery` | 0.001 | No surviving model version read; see role/name |
| `qualified-fields-delivery` | 0.000 | No surviving model version read; see role/name |
| `region-first-delivery` | 0.000 | No surviving model version read; see role/name |
| `delivery-source` | 0.000 | No surviving model version read; see role/name |
| `replacement-source` | 0.000 | No surviving model version read; see role/name |
| `removal-source` | 0.000 | No surviving model version read; see role/name |
| `outer-development-7` | 0.000 | No surviving model version read; see role/name |
| `outer-development-6` | 0.000 | No surviving model version read; see role/name |
| `outer-development-5` | 0.000 | No surviving model version read; see role/name |
| `outer-development-4` | 0.000 | No surviving model version read; see role/name |
| `outer-development-9` | 0.000 | No surviving model version read; see role/name |
| `retired-component-investigations` | 0.000 | No surviving model version read; see role/name |
| `outer-development-3` | 0.000 | No surviving model version read; see role/name |
| `outer-development-2` | 0.000 | No surviving model version read; see role/name |
| `outer-development` | 0.000 | No surviving model version read; see role/name |
| `additional-ten-01` | 0.000 | No surviving model version read; see role/name |
| `empty-reason-twenty-01` | 0.000 | No surviving model version read; see role/name |
| `empty-reason-ten-01` | 0.000 | No surviving model version read; see role/name |

## Other top-level clusters

These rows complete the `.codex-tmp` directory-level map. “Not assessed” means exactly that; it does not assert a necessary dependency. No additional deletion is authorized by this inventory. Current task evidence, retained components and original inputs keep their explicit protection.

| Folder | GB | Observed model versions | Role / boundary |
|---|---:|---|---|
| `task08b` | 6.347 | No surviving model version read; see role/name | Reporting/CLI verification data and environments, not a Learner version. Outside prior cleanup scope. |
| `production-73-v54-candidate` | 2.093 | OD v54 | Historical v54 one-shot candidate plus production-training-ledger.json explicitly reused by later combined-release work. Preserve that ledger/reports; full payloads need separate assessment. Outside prior deletion scope. |
| `pipeline-inspection` | 2.027 | ordered-token-clusterer-v4-bounded-script-layers, unresolved from 128KiB prefix | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-unmatched-review-root-cause` | 1.846 | No surviving model version read; see role/name | Historical diagnostic investigation/evidence, including v41. Not a new Learner algorithm release; outside prior cleanup scope. |
| `pipeline-refresh-20261005` | 1.813 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10b` | 1.737 | OD v41, OD v45, OD v58, OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases. Current Task10 distribution/installation evidence, explicitly protected by assignment. |
| `owner-gaps-v55-candidate` | 1.521 | OD v55 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `reporting-repair-20261005` | 1.507 | OD v41, OD v45, OD v58, OD v61 | Reporting application repair/installed-package evidence; multiple retained Learner models are packaged. Not a new Learner algorithm number; outside cleanup scope. |
| `pipeline-activation-20261005` | 1.316 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `marked-references-v59-candidate` | 1.233 | OD v59 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task07d` | 1.137 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-all-logs-20261003` | 0.818 | No surviving model version read; see role/name | Canonical retained input snapshots referenced by both current 73-log build bases. Protect original inputs; no algorithm version of its own. |
| `continuation-survey` | 0.683 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek4-pipeline-20261006` | 0.494 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `marked-references-v60-candidate` | 0.488 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `production-v53-comparison` | 0.440 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task08-multirun` | 0.394 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task07e` | 0.385 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `locator-marker-candidate` | 0.369 | OD v48 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task08a1` | 0.318 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `production-73-v53-candidate` | 0.306 | OD v53 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10a1` | 0.297 | OD v41, OD v45, OD v58, OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `character-location-candidate` | 0.285 | OD v51 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `super-short-character-candidate` | 0.282 | OD v53 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `receiver-location-boundaries-candidate` | 0.282 | OD v52 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `character-date-candidate` | 0.282 | OD v50 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `locator-presence-candidate` | 0.282 | OD v49 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task07` | 0.273 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-script-location-stacks` | 0.260 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `short-threshold-review` | 0.252 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek5-reporting-20261006` | 0.249 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `pipeline-receiving-20261005` | 0.249 | OD v41, OD v45, OD v58, OD v61 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `git-cleanup-review-20261002` | 0.244 | ordered-token-clusterer-v4-bounded-script-layers, OD v25, OD v26, OD v27, OD v29, OD v41, OD v45, unresolved from 128KiB prefix | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-location-label-equivalence` | 0.237 | OD v43, OD v44 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-packaging-20261006` | 0.189 | OD v41, OD v45, OD v58, OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `trek6-removal-20261007` | 0.176 | OD v41, OD v45, OD v58, OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `trek2-learner-20261006` | 0.164 | OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `task06b-verification` | 0.151 | ordered-token-clusterer-v4-bounded-script-layers, OD v25, OD v26, OD v27, OD v29, OD v41, OD v45, unresolved from 128KiB prefix | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task08a2` | 0.143 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-baseline-20261007` | 0.134 | OD v41, OD v45, OD v58, OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `task08c` | 0.132 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `watcher-source-mtime` | 0.128 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10c` | 0.121 | OD v41, OD v45, OD v58, OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `task07d-hardening` | 0.105 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `matching-investigation` | 0.104 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task07d-advisory-review` | 0.096 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task06-v45` | 0.094 | ordered-token-clusterer-v4-bounded-script-layers, OD v25, OD v26, OD v27, OD v29, OD v41, OD v45, unresolved from 128KiB prefix | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task07c-releases` | 0.087 | ordered-token-clusterer-v4-bounded-script-layers, OD v25, OD v26, OD v27, OD v29, OD v41, OD v45, unresolved from 128KiB prefix | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10d` | 0.080 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `learner-parser-review` | 0.078 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `parser-100-review` | 0.074 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task05` | 0.072 | ordered-token-clusterer-v4-bounded-script-layers, OD v25, OD v26, OD v27, OD v29, OD v41, unresolved from 128KiB prefix | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task06` | 0.070 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `syntax-research` | 0.060 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `pipeline-r3-packaging-20261005` | 0.046 | OD v41, OD v45, OD v58, OD v61 | Explicitly protected active installation; model 4ac4.../v61. Research model versions alone do not identify an installation. |
| `watcher-playset-implementation` | 0.045 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-parser-v1` | 0.043 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `pipeline-reporting-receiving-20261005` | 0.041 | OD v41, OD v45, OD v58, OD v61 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-acceptance-20261007` | 0.040 | OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `trek2-acceptance-20261007` | 0.040 | OD v61 | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `shared-matcher` | 0.033 | OD v41 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `pipeline-source-mtime-receiving` | 0.026 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `git-checkpoint-simple-20261003` | 0.019 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `v58-production-promotion` | 0.019 | OD v41, OD v45, OD v58 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `run-content-reconstruction-20260930` | 0.018 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `git-cleanup-runner-20261003` | 0.010 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `decoder-consultant-review-20261005` | 0.008 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `nltk_data` | 0.007 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `shared-matcher-pipeline-verification-20260927` | 0.006 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `tmp83oo10jm` | 0.005 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `pipeline-cache-1024` | 0.005 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task09-git-reports` | 0.005 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-remote-20261007` | 0.004 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `learner-v46-20logs` | 0.004 | OD v46 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-v46-targeted20` | 0.004 | OD v46 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `tmpgml1y30y` | 0.004 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `location-variability-review` | 0.003 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `run-IS3QON-investigation` | 0.003 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-parser-handoff` | 0.003 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `(root files)` | 0.003 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task06b-archive-20260928T074827Z` | 0.002 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `refinement-lineage-control` | 0.002 | OD v54 | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek2-removal-20261007` | 0.001 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `learner-reclamation-20261009` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-pin-20261007` | 0.001 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `trekker-usefulness-review-20261007` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `message-recovery-review` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-production-20261007` | 0.001 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `marked-references-v60-releases` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `marked-references-v59-releases` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10a-design-20261008` | 0.001 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `advisory-status-integrity-20261008` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `character-title-continuation-review` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `git-review` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `coupled-words-v58-releases` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `literal-v57-releases` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `owner-gaps-v56-releases` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `owner-gaps-v55-releases` | 0.001 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `pipeline-review` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `watcher-observer-review-20261007` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `history-inference-review` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `watcher-start-20261009` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek3-watcher-20261006` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10e` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `task10d-learner` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `watcher-playset-review` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task09b-enrollment-20261006-advisory` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task09-shared-backend-20261006` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-parser-audit` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `codex-sandbox-factory` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10d-data-intelligence` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `watcher-observer-removal-20261007` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `effect-regression-review` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10d-watcher` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `task05-reference-reconciliation-20260927` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task05-prompt-revision-20260927` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-resume-20261007` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `task08b-review` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task07b-version-audit` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `codex-multiproject-policy` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `decoder-integration-review-20261005` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `git-weekly-checkpoint` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `learner-date-key` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `watcher-live-activation` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trek6-owner-placement-disposition-20261007` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |
| `refinement-writer-memory` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `trekker-npm-cache` | 0.000 | No surviving model version read; see role/name | Outside prior learner-refactor deletion scope; individual dependency/retention not assessed. |
| `task10a` | 0.000 | No surviving model version read; see role/name | Preserve current Task09/10 evidence; directory versions can include packaged historical releases.  |

## Evidence and limits

Fresh machine-readable [storage map](../.codex-tmp/learner-reclamation-20261009/storage-map.json) records every measured top-level cluster, each learner-refactor/empirical-regions subcluster, every research-model path and extracted version, categories, timestamp and errors. Version extraction reads the first 128 KiB for the actual `clusterer_version` field; unresolved entries are labelled rather than guessed. Installed folders can include compact archived models from several versions; listing those versions does not mean each controls the installation.

Dependency interpretation uses [production-scope baseline](learner-next-release/PRODUCTION_SCOPE_BASELINE.md), [combined handoff](learner-next-release/HANDOFF.md), [historical Learner handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md), [self-contained release handoff](TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md), the two current build-basis inventories, actual historical registry pointer and retained package-loader source. Refreshed protected Learner team-state still reports the existing TREK-9 recovery marker; no tracker writes occurred.

The 127 GB figure is not an individually verified reclaimable-space total. The largest remaining in-scope review opportunity is **42.80 GB of model/native payloads in learner-refactor**, of which some carry the specific historical-registry/evaluation questions described above. Most of the large v42-v60 sibling clusters need expanded deletion scope as well as file-specific evidence review; their age alone neither protects nor clears every file.
