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
- full, L1+L2, L1-only, and unknown classification behavior.
