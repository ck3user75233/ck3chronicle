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
- expose `classify` and `review-queue` commands;
- [x] pass protected holdout and untouched-candidate compatibility gates;
- add semantic adjudication samples as new source families are approved.

## 3. First useful report

- implement `report`, `latest`, `latest --json`, and `errors`;
- report only from stored records;
- show model identity and classification coverage;
- expose unresolved and L1-only review queues;
- produce deterministic schema-versioned JSON.

## 4. Processing workflow

- add `process-pending` to finalize, reconcile, parse, classify, and report;
- keep the watcher copy-only;
- evaluate safe login-start automation after the foreground workflow is proven.

## 5. Session intelligence

- compare runs as new, fixed, worse, improved, or unchanged;
- support named baselines and reasoned ignore rules;
- ensure both sides use a common classification model revision;
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
