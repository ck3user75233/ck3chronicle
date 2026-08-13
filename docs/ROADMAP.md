# Roadmap

## 1. Reboot foundation

Status: complete at commit `3ef8151`.

- replace inherited tests with independent takeover tests;
- revalidate lifecycle capture, archive finalization, and canonical parsing;
- repair any failures the new suite reveals;
- checkpoint the clean takeover baseline.

## 2. Empirical classification

Status: runtime inference complete; persistence and CLI in progress.

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
- add `report --since` as a convenience projection;
- add true gameplay-duration exposure when authoritative lifecycle timing is
  available;
- persist durable run chronology independently of archive deduplication.

## 6. Runtime DLC/mod context

- parse the same-run `debug.log` `Mounted Data:` sequence;
- persist DLCs and active mods in exact order;
- distinguish Workshop and local descriptors;
- explicitly represent absent or malformed runtime context.

## 7. Source resolution and triage

- restrict source searches to the recorded active runtime mod list;
- identify winning files and override chains;
- correlate mod/patch changes with error deltas;
- rank investigation targets with explicit confidence.
