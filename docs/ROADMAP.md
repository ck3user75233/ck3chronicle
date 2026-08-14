# Capability inventory

This is an implementation/backlog inventory, not the project phase plan. Its
sections are deliberately unnumbered so they cannot be cited as completed
phases. See `PROJECT_PLAN.md` for phase authority and exit status.

## Reboot foundation capabilities

Status: complete at commit `3ef8151`.

- replace inherited tests with independent takeover tests;
- revalidate lifecycle capture, archive finalization, and canonical parsing;
- repair any failures the new suite reveals;
- checkpoint the clean takeover baseline.

## Empirical classification capabilities

Status: production runtime, persistence, and CLI complete.

- [x] register and hash-verify approved model artifacts;
- [x] implement full, L1+L2, L1-only, and unknown inference;
- [x] pass key/locator/source/semantic-order contract tests;
- [x] persist versioned classification runs;
- [x] store semantic-unit occurrences linked to raw source blocks;
- [x] store full, L1+L2, L1-only, and unknown assignments;
- [x] expose `classify` and `review-queue` commands;
- [x] pass protected holdout and untouched-candidate compatibility gates;
- add semantic adjudication samples as new source families are approved.

## Stored-report capabilities

Status: complete.

- [x] implement `report`, `latest`, `latest --json`, and `errors`;
- [x] report only from stored records;
- [x] show model identity and classification coverage;
- [x] expose unresolved and L1-only review queues;
- [x] produce deterministic schema-versioned JSON.

## Processing-workflow capabilities

Status: foreground workflow complete.

- [x] add `process-pending` to finalize, reconcile, parse, classify, and report;
- [x] keep the watcher copy-only;
- evaluate safe login-start automation after the foreground workflow is proven.

## Session-intelligence capabilities

- [x] compare runs as new, fixed, worse, improved, or unchanged;
- [x] exclude keys, locators, timestamps, and lines from delta identity;
- [x] ensure both sides use a common classification model revision;
- [x] add observed-error-window rates and exact-100,000-block quality flags;
- [x] support named baselines and reasoned ignore rules;
- [x] add `report --since` as a convenience projection;
- add true gameplay-duration exposure when authoritative lifecycle timing is
  available;
- [x] persist durable run chronology independently of archive deduplication;
- add explicit run selection to report/compare commands where several runs
  share one evidence bundle.

## Runtime DLC/mod-context capabilities

Status: first production contract complete.

- [x] parse the same-run archived `debug.log` `Mounted Data:` sequence;
- [x] persist DLCs and active mods in exact order;
- [x] distinguish Workshop, local, and unknown mounted roots;
- [x] enrich from inventory only after authoritative membership is known;
- [x] exactly validate mounted membership against enabled inventory;
- [x] explicitly represent complete, partial, and absent runtime context.
- [x] include mounted identity/order changes in session comparisons.

## Database hardening capabilities

Status: active.

- [x] reconcile every finalized archive with exactly one session and manifest
  rows;
- [x] independently count real archived `error.log` blocks and reconcile them with
  source blocks, occurrences, issues, and classification assignments;
- [x] prove that every stored occurrence and assignment retains source-block
  provenance;
- test idempotence, failed transactions, and corruption handling on copies of
  large real archives and the real database shape;
- [x] expose a read-only database audit command with bounded human and
  deterministic JSON
  output;
- [x] classify each audit failure as evidence, canonical parse, classification,
  runtime-context, or index-integrity failure.
- [x] normalize repeated raw blocks and complete classification payloads without
  collapsing occurrences or changing report/comparison/triage output;
- [x] replace repeated textual source relationships with compact integer foreign
  keys, migrate automatically, and verify internal page reclamation;
- [x] add a separate `observe-logging` diagnostic with an append-only
  lifecycle/result journal, a replaceable heartbeat, and a requirement for
  stable 100,000 error headers plus independently advancing `game.log` evidence;

Current real-index compaction oracle: 15 sessions, 858,732 independently
recounted raw headers/canonical blocks/occurrences, and 887,892 classification
assignments. A disposable real-index migration reduced SQLite from 1.584 GB to
289.6 MB while preserving every report, comparison, and triage hash. Remaining
work is a controlled live-session observation of the exact-100,000 boundary,
deep-distribution performance, and chronology repair policy for imported
sessions.

## Source-resolution and triage capabilities

Status: groundwork present; further development deferred until Phase 1 is
exited.

- [x] restrict exact-file resolution to recorded active runtime roots;
- [x] list current base/DLC/mod instances in mount order;
- [x] resolve exact-relative-path replacement as a distinct file layer;
- [x] implement optional immutable processing-time SHA-256 observations;
- [x] correlate stored source-instance changes with error deltas while retaining
  an explicit non-causality boundary;
- defer on-action container-merge evaluation over the common file chain;
- defer culture symbol-LIOS evaluation over the common file chain;
- preserve historical source bytes/diffs, not only content fingerprints;
- add broader mod/update fingerprints beyond referenced source files;
- [x] first action triage over new/worse patterns and current source candidates;
- rank investigation targets with richer explicit confidence and merge rules.
