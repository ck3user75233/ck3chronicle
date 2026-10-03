# Template-learning tool instructions

This directory is the sole source-controlled home of ck3chronicle learner,
incremental-registry, review-pack, blind-review and symbol-mining code.
Task 06B retired the old parser comparison and semantic projection catalog
generators; current learner/parser/matcher/publication code remains the owner.

- Modify or extend these tools here; never create the next learner generation
  under `.ck3raven/wip`, `ck3raven`, or another scratch tree.
- Treat corpora, raw logs, adjudication workbooks, registries, caches, and
  generated reports as external data. Accept them through CLI arguments and
  keep them ignored or outside the checkout.
- Preserve input/model hashes and review provenance. A holdout or rigid
  evidence-role split exists only for a separately commissioned empirical
  claim.
- Do not optimize for 100% attribution. Report full, L1+L2, L1-only,
  provisional/low-confidence, and unknown counts and examples.
- Learner output is a candidate artifact. Promotion into `models/` requires a
  reviewed immutable revision, manifest/hash validation, runtime selection,
  and regression coverage in the same repository.
- Derive verification from the active model-quality requirements, using real
  CK3 evidence outside Git. Do not port expectations from historical tests
  or the retired runner/scorer.
