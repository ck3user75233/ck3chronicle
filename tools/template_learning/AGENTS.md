# Template-learning tool instructions

This directory is the sole source-controlled home of ck3chronicle learner,
incremental-registry, review-pack, blind-review, symbol-mining, and projection-
catalog generation code.

- Modify or extend these tools here; never create the next learner generation
  under `.ck3raven/wip`, `ck3raven`, or another scratch tree.
- Treat corpora, raw logs, adjudication workbooks, registries, caches, and
  generated reports as external data. Accept them through CLI arguments and
  keep them ignored or outside the checkout.
- Preserve content-hash provenance and the separation between training,
  human-calibration, public-regression, private-holdout, and future-candidate
  evidence roles.
- Do not optimize for 100% attribution. Report full, L1+L2, L1-only,
  provisional/low-confidence, and unknown counts and examples.
- Learner output is a candidate artifact. Promotion into `models/` requires a
  reviewed immutable revision, manifest/hash validation, runtime selection,
  and regression coverage in the same repository.
- Add or update product-owned tests under `tests/` for reusable tool behavior.
  Release runner/scorer code remains independently authored.
