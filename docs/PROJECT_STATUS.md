# Project status

Date: 2026-08-17

Branch: `codex/ck3chronicle-reboot`

Takeover baseline: `99f98e3`

Project phase: **Phase 1 active; not exited**.

The numbered sections formerly published in `ROADMAP.md` were capability
areas, not project phases. Implemented checkpoints and the passing reboot fast
suite do not constitute Phase 1 acceptance. Phase authority now lives in
`PROJECT_PLAN.md`; the role-separated release process lives in
`PHASE1_EXIT_PROTOCOL.md`.

## Authority

The standalone repository at
`https://github.com/ck3user75233/ck3chronicle.git` is the source of truth.
`AGENTS.md`, `WORKSPACE_ROUTING.md`, and `CURRENT_HANDOFF.md` define the active
repository and workflow boundary. Old kickoff packets, prototypes,
architecture plans, dated handoffs, and WIP tests are not active project
inputs. No ck3chronicle implementation may be continued under `ck3raven` or a
`.ck3raven/wip` tree.

The following location contains historical takeover material only and is not a
source or restart authority:

`C:\Users\nateb\.ck3raven\wip\ck3chronicle\codex_reboot\takeover_archive_20260813`

## Implemented Phase 1 foundation

- exact CK3 lifecycle observation with an event journal and heartbeat;
- copy-first pending protection after an observed process exit;
- hashing only protected pending files during finalization;
- one content-addressed immutable archive per distinct evidence bundle;
- one immutable receipt and database run row per observed exit, even when
  several runs share the same evidence bundle;
- normal/crash/unknown termination provenance and per-run file origins;
- immediate default preservation of a newly associated crash folder's
  `exception.txt`, with receipt/database status and integrity provenance;
- deferred exact-hash comparison of crash-folder principal logs, with no
  duplicate copy when they equal the protected live logs;
- manifest verification and transactional SQLite registration;
- canonical parsing of archived `error.log` only;
- immutable source blocks plus one-row-per-occurrence provenance;
- atomic parse and reparse persistence.

The implemented foundation and production classifier seam are covered by the
new reboot-owned regression suite. Its current verified count is recorded in
`CURRENT_HANDOFF.md`; no inherited test contributes to that count.

These are fast regression tests. They do not constitute Phase 1 exit evidence.

The repository contains an implementation-side evaluation-interface handoff,
not implementation-authored executable exit tests. A later independent attempt
executed all 35 gates against `76fb2d5`, reporting 15 passes and 20 failures.
Forensic review found that only 10 passes and two product failures were
trustworthy; 22 gates used invalid inputs or harness assertions and one was
indeterminate because the taxonomy contract was ambiguous. The attempt is a
failed development artifact, not a valid Phase 1 exit measurement. Its private
holdout is permanently retired.

The two trustworthy product failures were repaired before candidate `bae136e`:
stored-report commands no longer rewrite a current SQLite database, and strict
processing rejects archive/run-integrity failures with the public
`archive_integrity` taxonomy. Its independent public run produced 23 passes,
one product failure, one infrastructure-unscored gate, four result/oracle
insufficiencies, and five contract-unscorable gates. The product failure was
the loss of the first valid error block when a UTF-8 BOM preceded its header.
The current successor preserves that BOM in exact raw evidence while excluding
it from semantic identity, and automatically reparses stored projections made
under the preceding parser contract. `errors --run` now also exposes the exact
selected run in its version-2 result.

The later frozen candidate `1f4d8c2` completed the repaired public v4 run. Final
independent adjudication was 23 pass, five product fail, and six infrastructure
unscored, so the private holdout remained blocked. The product failures were:
malformed/duplicated runtime-state handling; 0/252 exact canonical semantic
rows despite sound block linkage; two case-variant near misses incorrectly
accepted as full contracts; and the matching malformed-runtime mutation.

The current successor checkpoint repairs those failures. Runtime candidates
are structurally separated and absolute mount paths are validated. Semantic
literals compare exactly and case-sensitively. Most importantly, the empirical
classifier now feeds a separately hash-bound semantic projection catalog rather
than the old source-substring canonical parser. Development calibration against
the now-public 252-row authority is 252/252 exact over all scored fields. This
is a regression/calibration result, not independent exit or private-holdout
evidence.

Successor input authority is a public nine-unit, 42-file corpus, immutably
gate-bound by manifest SHA-256
`407e47d12bc17f30e2abd453dc69c4dda0b4e3fab705e2e361e6d26a8e6a6147`.
It adds the hash-bound 252-sample semantic authority, authentic absolute-path
evidence, and crash evidence required by the repaired gate rules. An
independent harness may exercise only the prescribed mutations; it may not
replace, truncate, synthesize, or reassign the locked base inputs.

Semantic authority is reconciled in `PHASE1_SEMANTIC_AUTHORITY.md`: canonical
issue fields, structural template identity, and explicit human slot decisions
are separate hash-bound authorities over the same immutable evidence. Historical
development artifacts called `holdout` are excluded from the future private
release holdout because they have already influenced implementation.

## Implemented classifier runtime

- exact reviewed model artifact promoted under `models/67303093ecda779d`;
- whole-file SHA-256 and internal cluster-contract validation before use;
- source family is a hard classification boundary;
- ordered-token matching with conservative semantic-lead gating;
- classification contract v2 typed PostValidate after empirical candidate
  selection; invalid L2 becomes L1 and invalid unlayered shape becomes unknown;
- exact case-sensitive semantic-literal validation;
- locator grammar runs before L1 assignment and a typed locator cannot satisfy
  a key, value, parameter, or type slot;
- grammar-preserving `scope:<KEY>.<KEY>` normalization;
- optional historical identity retained as `<OPTIONAL_KEY>` extraction data;
- full, independently composed L1+L2, L1-only, and unknown outcomes;
- location chains retained separately and excluded from template identity.
- versioned model registry and per-session classification runs in SQLite;
- one assignment row per semantic unit with source-block and ordinal identity;
- database-only classification after canonical parse;
- lossless raw-block and complete-classifier-payload dictionaries, with compact
  integer relationships for every independently countable occurrence;
- atomic same-model reclassification with prior-run rollback on failure.
- hash-bound semantic projection catalog schema v2 with total contract
  disposition and contract-specific symbol/object/locator selectors;
- database-only canonical reprojection from persisted classifications, with
  exact model/catalog lineage and atomic per-block/per-signature validation;
- schema-versioned `classify --json` with same-model idempotence;
- bounded stored-record `review-queue` for L1-only and unknown patterns.
- database-only executive `report`, chronological `latest`, and bounded
  `errors` projections;
- stable command-result v1 envelopes across `process-pending`, `report`,
  `latest`, and `errors` JSON surfaces, including success, reconciliation
  warning, input/readiness, archive integrity, model integrity, database, and
  generic pipeline failures;
- newest-reportable-run `latest` selection plus exact `report --run` and
  `errors --run` selection when content-addressed evidence is reused;
- compact 891-row model-contract catalog for readable templates without
  duplicating template text per occurrence;
- idempotent `process-pending` finalization → registration → parse → classify
  → latest-report workflow.
- chronological `compare` with stable model-bound pattern identities and
  observed new/fixed/worse/improved/unchanged occurrence deltas.
- first-to-last error-window rates plus an explicit exact-100,000-block
  possible-censoring warning.
- immutable named session/model baselines and reason-required, non-suppressing
  pattern-ignore annotations.
- `report --since` and `latest --since` combined report/comparison projections.
- archived-debug `Mounted Data:` parsing with ordered DLCs and active mods,
  exact source-file/line/byte/block-hash provenance, and explicit complete,
  partial, absent, malformed, truncated, and ambiguous states;
- inventory names/descriptors and mismatch warnings separated from the
  authoritative mounted membership/order projection;
- runtime context integrated into `process-pending`, `context` v2, and report v5.
- session comparisons include mounted DLC/mod additions, removals, and
  load-order moves while explicitly deferring content-update fingerprints.
- active-runtime-only `resolve-file` projection with base/DLC/mod order,
  inactive-root exclusion, and cautious last-mounted candidate wording.
- action `triage` for new/worse contracts, dominant stored file evidence,
  active-source candidates, and separate classifier-review items.
- optional immutable processing-time source observations, limited to recorded
  active runtime roots;
- one-pass SHA-256 fingerprints per observed file instance, exact-relpath file
  winners, and explicit unevaluated on-action/culture domain policies;
- triage source-observation deltas when both compared sessions contain stored
  observations, with correlation kept distinct from causation.

The current learner revision uses eight distinct training logs containing
432,847 timestamped blocks and produces 891 source-qualified contracts.
Development calibration assigns all 252 public semantic samples with 100%
category/type purity and stable locator/key mutation checks. The downstream
contract-bound projection independently reproduces all 252 canonical rows
exactly. These are implementation measurements over known development
authority, not independent semantic, performance, or private-holdout evidence.

## Not yet released

- candidate-bound independent acceptance of the published Phase 1 evaluation
  interface/output contract, plus any non-core envelopes the independent
  all-command gate demonstrates are still required;
- independently frozen complete report output;
- the Phase 1 mutation, private-holdout, and performance exit runs;
- on-action container-merge and culture symbol-LIOS adapters;
- historical source-byte snapshots/diffs, broad mod/update fingerprints, and
  richer confidence/merge-aware triage;
- automatic watcher startup on user login.
- a controlled live-session logging-progress observation proving or rejecting
  the suspected exact-100,000 error-record boundary.

Source observation is deliberately not part of `process-pending`. Resolver
failures or source-file hashing must not block capture, canonical parsing,
classification, or database reporting.

## Database hardening checkpoint

The read-only `audit-db` command checks archive/session membership,
manifest aggregates, stored parser counters, canonical totals, classification
counters, runtime-context rows, and source-block provenance. Its first run over
the live index found:

- 15 registered sessions;
- 858,732 canonical source blocks and occurrence rows;
- 858,732 independently recounted timestamped headers in archived `error.log`
  files, exactly matching the database for every session;
- 887,892 classification assignments;
- no structural errors or orphaned provenance;
- multiple archived source logs themselves end at exactly 100,000 blocks, so
  ck3chronicle did not truncate them; the repeated boundary is recorded as an
  observation whose cause remains unverified;
- historical imports lacked durable process chronology; capture-schema v3
  preserves one explicit `unknown` legacy run per otherwise unobserved bundle,
  without inventing unrecoverable start/exit facts, and marks historical crash
  exception evidence `unavailable` rather than claiming it was captured;
- one protected pending capture not yet processed, reported separately.

The compact-storage migration was exercised on a consistent disposable copy of
the 1,583,861,760-byte live database. After `VACUUM` it was 289,566,720 bytes,
an 81.7% reduction. All 15 report JSON hashes, the current comparison hash, and
the current triage hash were byte-identical before and after; canonical row
counts, `foreign_key_check`, and `quick_check` also reconciled exactly.

Full per-block/per-signature distribution reconciliation remains available
through `audit-db --deep`. Compact storage is the default and older schemas
migrate automatically. The first post-migration database open verifies
integrity and reclaims the freed pages automatically; this is not a recurring
user workflow.

## Approved production semantic runtime

- revision: `67303093ecda779d`;
- model SHA-256: `0a508eb8056f37d586921bb4441099dcb71fcf89e4a9d1c0e764b1b86d4c1b89`;
- projection catalog SHA-256: `c287849b16447e7b154f067c918afb3e0d30563ce56a9c578b06c006f20032b4`;
- projection revision: `public-semantic-252-contract-evidence-v3`;
- normalizer: `ck3-empirical-template-normalizer-v4.11`;
- clusterer: `ordered-token-clusterer-v4-bounded-script-layers`.

Both artifacts are hash-pinned and their exact lineage is used by production
persistence, reporting, audit, and triage. They are not authority to discard
raw evidence or perform automatic mod edits.
