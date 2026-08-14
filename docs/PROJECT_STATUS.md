# Project status

Date: 2026-08-15

Branch: `codex/ck3chronicle-reboot`

Takeover baseline: `99f98e3`

Project phase: **Phase 1 active; not exited**.

The numbered sections formerly published in `ROADMAP.md` were capability
areas, not project phases. Implemented checkpoints and the passing reboot fast
suite do not constitute Phase 1 acceptance. Phase authority now lives in
`PROJECT_PLAN.md`; the role-separated release process lives in
`PHASE1_EXIT_PROTOCOL.md`.

## Authority

Source behavior and the documents in this directory are authoritative. Old
kickoff packets, prototypes, architecture plans, and tests are not active
project inputs.

Historical material is recoverable from:

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
new reboot-owned suite: 115 tests at the current successor checkpoint. No
inherited test contributes to that count.

These are fast regression tests. The complete protected-real-evidence,
holdout, mutation, command-envelope, and performance exit gates have not run
against one frozen current-tip candidate.

The repository contains an implementation-side evaluation-interface handoff,
not implementation-authored executable exit tests. An independent harness was
frozen for `d07b19e`, but no private holdout was selected or executed. The
candidate and harness were superseded by the crash-exception requirement and
remain baseline artifacts only. Independent evaluator roles must rebind and
extend their own harness for the successor candidate.

Semantic authority is reconciled in `PHASE1_SEMANTIC_AUTHORITY.md`: canonical
issue fields, structural template identity, and explicit human slot decisions
are separate hash-bound authorities over the same immutable evidence. Historical
development artifacts called `holdout` are excluded from the future private
release holdout because they have already influenced implementation.

## Implemented classifier runtime

- exact reviewed model artifact promoted under `models/93196794a7e0115d`;
- whole-file SHA-256 and internal cluster-contract validation before use;
- source family is a hard classification boundary;
- ordered-token matching with conservative semantic-lead gating;
- classification contract v2 typed PostValidate after empirical candidate
  selection; invalid L2 becomes L1 and invalid unlayered shape becomes unknown;
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
- compact 822-row model-contract catalog for readable templates without
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

The pre-PostValidate classification contract v1 was compared with the frozen
release evaluator across all five training-excluded logs: 194,022 semantic
occurrences reconciled by assignment count. Contract v2 deliberately changes
that behavior by rejecting typed-slot violations. Read-only development probes
over current stored evidence retained 98.72% L1-or-better coverage on the
largest session (100,000 blocks / 103,358 semantic occurrences) while
downgrading 1,055 formerly overconfident assignments; its read-only inference
probe took 45.7 seconds and the latest 2,124-unit probe took 0.34 seconds. These
are implementation measurements, not independent semantic or performance exit
evidence.

This compatibility result is not Phase 1 semantic exit evidence. At least one
current full-assignment template has failed subsequent human plausibility
review, and the private holdout must be selected and scored only after the
release candidate is frozen.

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

## Approved production model

- revision: `93196794a7e0115d`;
- SHA-256: `3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3`;
- normalizer: `ck3-empirical-template-normalizer-v4.6`;
- clusterer: `ordered-token-clusterer-v4-bounded-script-layers`.

The artifact is hash-pinned and used by production persistence, reporting, and
triage. It is not authority to discard raw evidence or perform automatic mod
edits.
