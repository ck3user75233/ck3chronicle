# Learner research reclamation receipt — 2026-10-09

## Owner-issued remaining research cleanup — completed

Following the storage explanation, the Owner explicitly directed removal of the
remaining research payloads. **All 184 research files in 92 bundles were deleted:
42,794,174,357 bytes (42.79 GB). No deletion failed or was permission-blocked.**
Together with the two earlier batches below, this reclaims **54,418,943,219 bytes
(54.42 GB)** across **196 files / 98 retired research bundles**. October 4 savings
remain excluded.

All 184 files matched their original manifest hashes and measured sizes. Every
target was an explicitly inventoried `native-candidate-bundle` model/evidence
payload inside `learner-refactor`. Before each native PowerShell
`Remove-Item -LiteralPath`, checks revalidated the resolved path, ancestor reparse
attributes, manifest/hash, Windows file identity, single-link status, size and
payload hash. No directory deletion, payload copy, permission change or alternate
deletion route was used.

All **4,394 non-target files** in that subtree and **931 protected metadata files**
remained byte-identical. The four historical release-copy model files, totaling
**7,195,370 bytes**, remain intact, as do original logs, caches, reports, scripts,
parser/source files, compact exports, registries and original manifests. All
**73 original training inputs plus their 73 snapshots** independently match the
current build basis. `learner-refactor` now measures **6,226,538,913 bytes (6.23 GB)**,
including the new removal notices. Its only remaining model/native payload files
are those four release-copy models.

The five legacy model-manifest references found in the protected metadata are
`source_candidate_revision`/manifest provenance pins. The published artifacts
remain intact; those pins do not cause current runtime to load the retired research
directories. Current production and Task09/10 use separate v61 bundles/packages.
The Owner's instruction now retires the historical registry-base and v41 research
evaluation/replay availability discussed in the earlier assessment. No active
full-research-payload dependency was identified in refreshed task records or current
build bases. No additional approval was required.

Each affected directory has `REMOVED-PAYLOADS.json`, recording exact identities,
hashes, deletion scope and evidence limits. **All 92 additional research bundles
are deliberately incomplete and no longer available for authenticated loading,
evaluation or full replay.** Historical registry selections and manifests remain
unchanged provenance records, not claims that the retired bundles still load.
Original unresolved findings remain in retained reports; cleanup does not resolve
them or recreate unavailable outcomes.

Read-only observations confirm Watcher PID **29088** kept the same process start
and advanced its heartbeat/poll count. Repository model `2b129...` and installed
model `4ac4...` selections remain unchanged. No application operation, service
restart, source/configuration change or retention automation occurred. Protected
Trekker reads succeeded; its existing TREK-9 recovery marker remains untouched.

Exact additional evidence is in
[remaining-research/receipt.json](../.codex-tmp/learner-reclamation-20261009/remaining-research/receipt.json),
alongside `pre-deletion-inventory.json`, `dependency-clearance.json`,
`current-reference-hits.json`, `deletion-results.json`, `preserved-before.json`,
`protected-before.json`, `original-inputs-after.json`, `remaining-after.json` and
`watcher-before.json` / `watcher-after.json`. Measurements are logical file bytes,
not physical free-space attribution on a concurrently used drive.

## Earlier first and second batches — completed before the follow-up

**Deleted 12 explicitly checked payload files from six superseded experiments:
11,624,768,862 bytes (11.62 GB / 10.83 GiB).** Owner issuance in the Learner chat
authorized these bounded removals. The saved Advisory draft was not the authority.
These are new removals; the October 4 cleanup is not counted again.

| Batch | Experiment / revision | Files | Deleted bytes |
|---|---|---:|---:|
| 1 | default-literals-73-log-review / `9310e1af7379beb8f6cbcda4` | 2 | 2,350,592,261 |
| 1 | tighter-groups-review / `3764dc38e1339cf781cba857` | 2 | 2,333,339,121 |
| 1 | tighter-wording-review / `6d230eb73f03d4b738630eb4` | 2 | 2,323,585,231 |
| 1 | default-literals-review / `1fbe61bfc955c6773d6c6192` | 2 | 1,540,949,192 |
| 1 | explicit-literal-guidance-review / `87b4eed8261625c4ba9ff05c` | 2 | 1,539,727,469 |
| 2 | literal-context-review / `09b423a12a029f957c700512` | 2 | 1,536,575,588 |

Each row removes only `empirical_template_model.json` and `native_evidence.json`
from that experiment's `revisions/<revision>/` under `.codex-tmp/learner-refactor/`.
No directory was deleted. Every file was freshly SHA-256 verified against its
original manifest; batch 1 also matched Advisory's exact sizes and hashes. Resolved
paths, ancestor reparse attributes, single-link status and file identities were
checked before removal. Native PowerShell `Remove-Item -LiteralPath` performed
the deletions, without recursive deletion or another payload copy.

## Dependency clearance and preservation

The September progression is recorded in [default-literal review](LEARNER_DEFAULT_LITERALS_REVIEW.md),
[grouping review](LEARNER_GROUPING_REVIEW.md) and [literal-guidance review](LEARNER_LITERAL_GUIDANCE_REVIEW.md).
[Literal-context review](LEARNER_LITERAL_CONTEXT_REVIEW.md) explicitly marks v4
superseded. Current [production build authority](learner-next-release/PRODUCTION_SCOPE_BASELINE.md),
[Task 09 baseline](TASK09_RELEASE_BASELINE.md), Task 10 handoffs and protected
Trekker records use later retained artifacts. Current catalogs, selections,
build bases and input inventories showed no full-bundle dependency on these six.

Historical seeded `selection.json` files cite `6d230...` as a comparison baseline;
they are log-sample inventories, not current production selections. Historical
grouping/fresh-parse/slash-list scripts do load that bundle: those scripts and
their saved reports remain, but their full replay is now deliberately unavailable.
The original remaining ambiguities/regressions are not claimed resolved by cleanup.

After both batches, **931 protected metadata files and 83 retained sibling files**
matched their pre-deletion hashes, including original manifests, reports, reviews,
parser files and other experiment artifacts. Every original log and snapshot in
the current 73-input build basis also matched its recorded size/hash: **146 paths,
596,625,707 bytes per set**. All other original inputs were outside the explicit
deletion targets. No original input, feature cache, compact export, script,
published model/Learner, Task 09/10 bundle, source or configuration was removed.

Repository selection remains `2b12932103f3a3111a4e1880`; the October 5 live
installation selection remains `4ac4e8ee92346e6d14eacfbf`. Neither was switched.
Read-only heartbeat/process observations show Watcher PID **29088** running,
with unchanged process start and advancing timestamps/poll counts. No service
probe, start, restart, capture, ingestion or replay was invoked.

Each of the six revision directories now has `REMOVED-PAYLOADS.json`, carrying
exact paths, sizes, hashes and receipt links. Original manifests are unchanged
historical records. **These research bundles are incomplete and cannot be fully
authenticated or replayed.** Saved reports retain their original evidence limits.

## Retained candidates and limits

- `at-symbol-incremental-review/registry/revisions/e6aee7eeb209c9e26abf72da`
  remains selected by its preserved research registry. Its historical registry
  loading/build use was not retired in these batches. This is not a production
  dependency claim. Its original log-input tree is independently protected.
- `continuations-v41/logs-30/007d011659a02de3c965a9cd` remains a source of published
  `76630685...` and retained `44a040...` validation provenance. Full-evidence
  retirement relative to published lineage/root-cause evidence was not cleared.
- Other payloads were not individually cleared. The final measured inventory
  contains 188 remaining model/native-evidence files, 42,801,369,727 bytes; this
  excludes caches and other folder contents and is not a deletion promise.

No deletion failed or was permission-blocked. An initial guard used an unsupported
PowerShell `Split-Path` parameter combination and stopped before any mutation;
the error receipt is retained. It was corrected to `System.IO.Path`, all checks
were repeated, and removal succeeded. The locked Watcher lockfile could not be
read; heartbeat and live process evidence supplied the running check. An initial
process lookup used `pid` instead of heartbeat field `watcher_pid`; the corrected
lookup succeeded. Logical deleted bytes are measured, not a physical free-space
delta attributable on a concurrently used drive.

The final handoff-preservation check initially used Windows' default text decoding
and failed on UTF-8 text; explicit UTF-8 verification passed without any content
repair. `documentation-check.json` records the correction and confirms that the
entire prior handoff remains beneath the new cleanup entry. Documentation whitespace
checking passed. No product acceptance tests or invented evidence were introduced.

Protected Trekker reads consumed team-state, the task list and TREK-2/6/14/11/16,
including later delivery/receipt comments. Task 09 remains completed and TREK-14
was not repurposed. No enrollment was requested. The existing TREK-9 incomplete
operation still requires Pipeline recovery; no tracker mutation/retry was made.

## Exact local evidence

All generated evidence remains ignored under
[`.codex-tmp/learner-reclamation-20261009/`](../.codex-tmp/learner-reclamation-20261009/):

- [Consolidated receipt](../.codex-tmp/learner-reclamation-20261009/cleanup-receipt.json)
- `first-batch-inventory.json`, `first-batch-deletion-results.json`, `first-batch-receipt.json`
- `second-batch-inventory.json`, `second-batch-receipt.json`
- `dependency-clearance.json`, `second-batch-clearance.json`, saved reference searches and protected Trekker responses
- `protected-before.json`, both sibling inventories and `original-inputs-authenticated.json`
- `watcher-before.json`, `watcher-after-first-batch.json`, `watcher-final.json`
- `remaining-payload-inventory-final.json`, `attempt1-preflight-parameter-error.json`

[Separate retention proposal](LEARNER_RESEARCH_RETENTION_PROPOSAL.md) is advice
for future research output management; no automatic retention was implemented.

The [storage and version map](LEARNER_STORAGE_MAP_20261009.md) expands the Owner's
follow-up about the roughly 127 GB total and distinguishes actual evidence
dependencies, historical registry/evaluation questions, unreviewed files and
folders outside the original deletion scope. It records no further deletions.
