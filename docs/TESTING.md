# Testing authority

## Rule

Only tests authored for the 2026-08-13 takeover contract count toward product
acceptance. The inherited test tree was archived and removed.

Every acceptance test must state or document:

- the requirement it covers;
- its observable output;
- the independent source of the expected result;
- relevant mutations that must change the result;
- irrelevant mutations that must not change it;
- whether its evidence was excluded from learner training.

## Permitted oracles

- literal expected records derived from the approved product contract;
- human semantic adjudications;
- independently calculated byte counts and cryptographic hashes;
- manually specified filesystem and database states;
- protected external evidence with frozen, independently reviewed manifests.

## Forbidden oracles

- serializing production output and treating it as expected output;
- copying production SQL, tokenization, normalization, or aggregation into a
  test;
- using learner output as human truth;
- letting a crafted positive example stand in for full-corpus behavior;
- measuring acceptance on evidence used to train the model.

## Current suite

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider tests
```

The suite currently covers:

- lifecycle state transitions and heartbeat behavior;
- copy-first exact-byte protection and rapid-relaunch rejection;
- six-file independent SHA-256/bundle oracle;
- single-pass finalization hashing;
- deduplicated archive identity;
- transactional session/manifest registration;
- archived-byte corruption detection;
- exact lexical block spans, hashes, and identities;
- `error.log`-only canonical storage;
- explicit empty-log success and missing-evidence failure;
- exact approved-model hash and contract validation;
- source-family isolation and semantic-change rejection;
- key and locator invariance;
- grammar-preserving two-key scope normalization;
- optional-key extraction;
- full, L1+L2, L1-only, and unknown classification behavior;
- one-row-per-semantic-unit database provenance;
- classification from stored source blocks without reopening archives;
- same-model idempotence and atomic reclassification rollback;
- rejection of unparsed sessions;
- deterministic classify JSON and stored-record review-queue output;
- explicit empty filtered review queues;
- database-only executive report structure and readable contract templates;
- capture-time latest ordering independent of session registration ID;
- bounded report/error JSON projections;
- end-to-end and second-run idempotence for `process-pending`;
- cross-session semantic deltas despite changed keys, locators, and line
  numbers;
- chronological CLI selection and bounded deterministic comparison JSON;
- observed error-window rates and quality metadata;
- immutable, case-insensitive named baselines pinned to a model revision;
- mandatory-reason ignore annotations that remain visible in comparisons;
- compatible report-plus-comparison envelopes for `report --since`;
- Mounted Data authority over inventory membership and order;
- disabled-mod exclusion, Workshop/local identity, mismatch visibility,
  missing-debug state, reparse rollback, and context CLI JSON;
- mounted mod addition/removal/load-order movement in session deltas;
- active-root-only file resolution with ordered base/DLC/mod instances;
- explicit inactive-root exclusion, path-traversal rejection, and CLI JSON;
- immutable one-pass source fingerprints despite later live-file changes;
- exact-relative-path file winners separated from on-action/culture domain
  policies;
- stored source-instance change correlation across compared sessions;
- read-only database audit success over a complete archive/index shape;
- explicit parser-counter corruption and orphan-archive detection;
- bounded schema-versioned database-audit CLI JSON;
- new/worse action triage, stored raw-block locator fallback, malformed locator
  rejection, active-source links, bounded CLI JSON, and review separation.

## Protected-corpus compatibility gate

`tools/evaluate_classifier.py` is a read-only coverage utility. It was run
against the three reviewed holdouts and two untouched candidates excluded from
training. The production runtime exactly reproduced the frozen release
evaluator's assignment counts across 194,022 semantic occurrences:

| Evidence | Full | L1+L2 | L1-only | Unknown |
|---|---:|---:|---:|---:|
| 3 reviewed holdouts | 67,115 | 6 | 49 | 275 |
| 2 untouched candidates | 126,505 | 48 | 15 | 9 |

This proves compatibility with the reviewed model/evaluator pair. It does not
turn the old evaluator into a semantic oracle; human-authored normalization
and assignment tests provide that authority.
