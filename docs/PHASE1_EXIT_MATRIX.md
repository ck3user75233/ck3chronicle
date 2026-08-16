# Phase 1 exit matrix

Release candidate: **successor to public candidate `bae136e` not yet frozen**.

Status: **Phase 1 not exited**.

This matrix separates historical candidate-bound evidence from the current
unfrozen implementation. A pass on `bae136e` is useful regression evidence but
does not transfer automatically after source or contract changes.

## Latest public-attempt accounting

The frozen public score for candidate
`bae136e491f75863b34f689d5c9474793fd52437` is preserved under result SHA-256
`a62e5cfe5fbb5bcb072040e11c13e80c1f51bad25d65680fb1333c93046aa11a`.
It scored 34 public gates as follows; the private gate was not selected.

| Disposition on `bae136e` | Gates |
|---|---:|
| Public PASS | 23 |
| Product FAIL | 1 |
| Infrastructure/unscored | 1 |
| Result/oracle insufficiency | 4 |
| Contract-unscorable | 5 |
| Private holdout unrun | 1 |
| Total | 35 |

The one product failure was the byte-zero UTF-8 BOM first-block loss in
`P1-PAR-07`; the current development tree repairs it and passes real-corpus
counts of 10,785/10,785 and 100,000/100,000 with zero preamble blocks. The ten
unscored/insufficient gates were evaluator-input or frozen-rule deficiencies,
not product failures. Locked public corpus v2 and
`PHASE1_PUBLIC_GATE_RULES.md` now close those upstream gaps. The current tree
also adds observable run identity to `errors` v2, which `P1-REP-06` requires.

The earlier `76fb2d5` attempt remains rejected after its input/harness
postmortem, and its exposed private holdout is retired permanently.

## Capture

| Gate | Latest public evidence | Successor requirement |
|---|---|---|
| `P1-CAP-01` | PASS on `bae136e` | Rerun unchanged gate. |
| `P1-CAP-02` | PASS on `bae136e` | Rerun unchanged gate. |
| `P1-CAP-03` | Infrastructure/unscored: archive mutation applied zero changes | Use the fixed exact-target mutation rule; a precondition failure remains unscored. |
| `P1-CAP-04` | PASS on `bae136e` | Rerun unchanged gate. |
| `P1-CAP-05` | PASS on `bae136e` | Rerun unchanged gate. |
| `P1-CAP-06` | PASS on `bae136e` | Rerun unchanged gate. |

## Runtime context

| Gate | Latest public evidence | Successor requirement |
|---|---|---|
| `P1-RUN-01` | PASS: exact 27-DLC/104-mod complete projection | Rerun unchanged gate. |
| `P1-RUN-02` | PASS: Workshop/local and non-complete forms | Rerun unchanged gate. |
| `P1-RUN-03` | PASS: order-only metamorphism | Rerun unchanged gate. |
| `P1-RUN-04` | PASS: six distinct runtime states | Rerun unchanged gate. |
| `P1-RUN-05` | PASS: enrichment cannot change authority | Rerun unchanged gate. |

## Parsing and persistence

| Gate | Latest public evidence | Successor requirement |
|---|---|---|
| `P1-PAR-01` | PASS: 28,131 exact blocks reconcile | Rerun on parser contract 1.0.1. |
| `P1-PAR-02` | Unscored: 252-item oracle omitted from authorized inputs | Corpus v2 now includes the exact sample/oracle pair; run the frozen row-level rule. |
| `P1-PAR-03` | PASS: occurrence/content/signature relations | Rerun unchanged gate. |
| `P1-PAR-04` | Unscored: invalid mutation changed `event:` rather than an absolute root | Corpus v2 adds an authentic absolute-path unit; use the exact locator-root rule. |
| `P1-PAR-05` | PASS: conservative near-miss rejection | Rerun unchanged gate. |
| `P1-PAR-06` | PASS: authentic positives and near misses | Rerun unchanged gate. |
| `P1-PAR-07` | FAIL: BOM first block became preamble | Repair is implemented and development-tested; rerun the complete gate. |
| `P1-PAR-08` | PASS: reparse rollback | Rerun on parser contract 1.0.1. |
| `P1-PAR-09` | PASS: first-parse rollback | Rerun on parser contract 1.0.1. |
| `P1-PAR-10` | PASS: zero-byte explicit success | Rerun on parser contract 1.0.1. |
| `P1-PAR-11` | PASS: standard/deep database invariants | Rerun on parser contract 1.0.1. |

## Reporting and public workflow

| Gate | Latest public evidence | Successor requirement |
|---|---|---|
| `P1-REP-01` | PASS: processing envelope and side effects | Rerun unchanged gate. |
| `P1-REP-02` | PASS: text/JSON equivalence | Include `errors` v2 run projection. |
| `P1-REP-03` | PASS: stored reporting without raw archive | Rerun unchanged gate. |
| `P1-REP-04` | PASS: eight read commands did not mutate storage | Rerun with `errors` v2. |
| `P1-REP-05` | PASS: repeat/order determinism | Rerun unchanged gate. |
| `P1-REP-06` | Unscored: no crash provenance case, and `errors` lacked run identity | Use the fixed four-run chronology and three assigned units; score `errors` v2 exact binding. |
| `P1-REP-07` | Unscored: readiness used no DB; pipeline fault was installed too late | Use the six exact preparations and validity rules in the public gate contract. |

## Release gates

| Gate | Latest public evidence | Successor requirement |
|---|---|---|
| `P1-HOLD-01` | Not selected or executed | Select a fresh private holdout only after all public gates pass. |
| `P1-MUT-01` | Contract-unscorable | Run all eleven frozen valid mutations; 11/11 required. |
| `P1-PERF-01` | Measurements captured; no prior budget | Apply frozen lexical/parse budgets. |
| `P1-PERF-02` | Measurements captured; no prior budget | Apply frozen runtime budget. |
| `P1-PERF-03` | Measurements captured; no prior budget | Apply frozen report/storage budget. |
| `P1-PERF-04` | Measurements captured; no prior budget | Apply frozen pipeline wall/CPU/RSS budget. |

## Required order of work

1. Keep locked corpus v1 immutable and use verified locked corpus v2 for the
   successor attempt.
2. Finish implementation regression, independent code/test review, and public
   contract consistency review.
3. Commit and freeze one clean successor candidate and record its complete
   tree/interface hashes.
4. Have an independent harness authority author and freeze a new bounded
   harness against the fixed corpus v2 mapping and public gate rules.
5. Run and score all 34 public gates. Infrastructure cases are repaired and
   rerun only under the unchanged candidate/input/oracle rule.
6. Proceed only if all 34 public gates pass; then select and freeze a new
   private holdout.
7. Run the private gate through the separated runner/scorer/adjudicator process
   and publish one candidate-bound Phase 1 exit report.
