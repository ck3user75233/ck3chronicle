# Roadmap

## 1. Reboot foundation

Status: complete at commit `3ef8151`.

- replace inherited tests with independent takeover tests;
- revalidate lifecycle capture, archive finalization, and canonical parsing;
- repair any failures the new suite reveals;
- checkpoint the clean takeover baseline.

## 2. Empirical classification

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

## 3. First useful report

Status: complete.

- [x] implement `report`, `latest`, `latest --json`, and `errors`;
- [x] report only from stored records;
- [x] show model identity and classification coverage;
- [x] expose unresolved and L1-only review queues;
- [x] produce deterministic schema-versioned JSON.

## 4. Processing workflow

Status: foreground workflow complete.

- [x] add `process-pending` to finalize, reconcile, parse, classify, and report;
- [x] keep the watcher copy-only;
- evaluate safe login-start automation after the foreground workflow is proven.

## 5. Session intelligence

- [x] compare runs as new, fixed, worse, improved, or unchanged;
- [x] exclude keys, locators, timestamps, and lines from delta identity;
- [x] ensure both sides use a common classification model revision;
- [x] add observed-error-window rates and exact-100,000-block quality flags;
- [x] support named baselines and reasoned ignore rules;
- [x] add `report --since` as a convenience projection;
- add true gameplay-duration exposure when authoritative lifecycle timing is
  available;
- persist durable run chronology independently of archive deduplication.

## 6. Runtime DLC/mod context

Status: first production contract complete.

- [x] parse the same-run archived `debug.log` `Mounted Data:` sequence;
- [x] persist DLCs and active mods in exact order;
- [x] distinguish Workshop, local, and unknown mounted roots;
- [x] enrich from inventory only after authoritative membership is known;
- [x] exactly validate mounted membership against enabled inventory;
- [x] explicitly represent complete, partial, and absent runtime context.
- [x] include mounted identity/order changes in session comparisons.

## 7. Source resolution and triage

- [x] restrict exact-file resolution to recorded active runtime roots;
- [x] list current base/DLC/mod instances in mount order;
- [x] resolve exact-relative-path replacement as a distinct file layer;
- [x] persist immutable processing-time SHA-256 observations for the latest
  session's error-referenced file instances;
- [x] correlate stored source-instance changes with error deltas while retaining
  an explicit non-causality boundary;
- implement on-action container-merge evaluation over the common file chain;
- implement culture symbol-LIOS evaluation over the common file chain;
- preserve historical source bytes/diffs, not only content fingerprints;
- add broader mod/update fingerprints beyond referenced source files;
- [x] first action triage over new/worse patterns and current source candidates;
- rank investigation targets with richer explicit confidence and merge rules.
