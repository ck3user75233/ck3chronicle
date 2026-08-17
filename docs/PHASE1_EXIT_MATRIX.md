# Phase 1 exit matrix

Current release candidate: **not yet frozen**.

Status: **Phase 1 not exited**.

This matrix records the latest valid public attempt and the work that must be
rerun against the next frozen successor. Candidate-bound passes never transfer
automatically after product, model, catalog, interface, or harness changes.
The rejected earlier fake/substituted-input cycle and the valid attempts that
followed it were Phase 1 evaluation work, not Phase 0 testing.

## Latest valid public attempt

Candidate `1f4d8c2f5a6e3ec1c5dc7a5324b0bbe4c4b233ac` was evaluated by the frozen
public v4 harness whose manifest SHA-256 was
`033a8e6ea0749386b7d157d98870308b44c047fe09261a1742b2442f6db1410c`.
The independent adjudication package manifest SHA-256 was
`05a69614fa3ae5dc3d160a36e7af1bdfa3f1547da638e4ad0a42df100d18bdbf`.

| Disposition on `1f4d8c2` | Gates |
|---|---:|
| Public PASS | 23 |
| Product FAIL | 5 |
| Infrastructure/unscored | 6 |
| Private holdout unrun | 1 |
| Total | 35 |

The five public product failures were repaired on the successor development
line, but those repairs currently have development regression/calibration
evidence only. The private holdout was correctly blocked and remains unseen.

## Capture

| Gate | `1f4d8c2` disposition | Successor requirement |
|---|---|---|
| `P1-CAP-01` | Infrastructure/unscored: stale-crash recipe failed before product execution | Fresh harness must exercise the published stale/unassociated crash interface and close a neutral result. |
| `P1-CAP-02` | PASS | Rerun unchanged gate. |
| `P1-CAP-03` | PASS | Rerun unchanged integrity gate. |
| `P1-CAP-04` | PASS | Rerun unchanged unstable-source/abort gate. |
| `P1-CAP-05` | Infrastructure/unscored: direct calls omitted the required CLI envelope/taxonomy observations | Exercise the public command and record exit, stage, retryability, recovery, and side effects. |
| `P1-CAP-06` | PASS | Rerun unchanged mandatory/optional/zero-byte gate. |

## Runtime context

| Gate | `1f4d8c2` disposition | Successor requirement |
|---|---|---|
| `P1-RUN-01` | PASS | Rerun exact complete runtime projection. |
| `P1-RUN-02` | PASS | Rerun Workshop/local mount forms. |
| `P1-RUN-03` | PASS | Rerun order-only metamorphism. |
| `P1-RUN-04` | **PRODUCT FAIL**: partial, malformed, and ambiguous inputs collapsed to `complete` | Successor structural repairs must distinguish all contract states under the fixed authentic mutations. |
| `P1-RUN-05` | Infrastructure/unscored: required resolver-root/source-instance observations were absent | Export every specified authority/enrichment observation without changing the product interface. |

## Parsing, classification, and persistence

| Gate | `1f4d8c2` disposition | Successor requirement |
|---|---|---|
| `P1-PAR-01` | PASS | Rerun exact lexical/cardinality/provenance gate. |
| `P1-PAR-02` | **PRODUCT FAIL**: 0/252 canonical semantic rows matched despite exact block linkage | Rerun the repaired contract-bound semantic projection against the same hash-bound authority. |
| `P1-PAR-03` | PASS | Rerun occurrence/content/signature relations. |
| `P1-PAR-04` | Infrastructure/unscored: mutation did not target an already-tokenized absolute-root locator span | Use the fixed authentic absolute-path unit and prove the mutation precondition. |
| `P1-PAR-05` | **PRODUCT FAIL**: case-variant semantic near miss remained a full contract | Rerun exact case-sensitive semantic-literal rejection. |
| `P1-PAR-06` | **PRODUCT FAIL**: the same case-variant near miss retained full assignment | Rerun authentic-positive/near-miss classification and assignment gate. |
| `P1-PAR-07` | PASS | Rerun all BOM/newline/encoding/truncation variants. |
| `P1-PAR-08` | PASS | Rerun reparse rollback. |
| `P1-PAR-09` | PASS | Rerun first-parse rollback. |
| `P1-PAR-10` | PASS | Rerun zero-byte explicit-success gate. |
| `P1-PAR-11` | PASS | Rerun standard/deep database reconciliation. |

## Reporting and public workflow

| Gate | `1f4d8c2` disposition | Successor requirement |
|---|---|---|
| `P1-REP-01` | PASS | Rerun processing envelope and side effects. |
| `P1-REP-02` | PASS | Rerun stored text/JSON equivalence. |
| `P1-REP-03` | PASS | Rerun archive-independent stored reporting. |
| `P1-REP-04` | Infrastructure/unscored: only aggregate DB hashes and no per-command evidence hashes were recorded | Record database and evidence identity around every required read command. |
| `P1-REP-05` | PASS | Rerun idempotence/order determinism. |
| `P1-REP-06` | Infrastructure/unscored: harness cleanup proof aborted the four-run chronology | Complete and close the exact normal/repeated/crash/unreportable chronology and run-bound reports. |
| `P1-REP-07` | PASS after independent adjudication of the retained corrupt-database transcript | Rerun all six taxonomy preparations with valid neutral envelopes. |

## Release gates

| Gate | `1f4d8c2` disposition | Successor requirement |
|---|---|---|
| `P1-HOLD-01` | Not selected or executed | Select a fresh private holdout only after all 34 public gates pass. |
| `P1-MUT-01` | **PRODUCT FAIL**: one valid malformed-runtime mutation was not detected; four other variants were invalid infrastructure | Run all eleven valid, precondition-proven variants; 11/11 required. |
| `P1-PERF-01` | PASS | Rerun frozen lexical/parse budgets. |
| `P1-PERF-02` | PASS | Rerun frozen runtime budget. |
| `P1-PERF-03` | PASS | Rerun frozen reporting/storage budgets. |
| `P1-PERF-04` | PASS | Rerun frozen pipeline wall/CPU/RSS budgets. |

## Required order of work

1. Finish implementation regression and public contract consistency review.
2. Commit and freeze one clean successor candidate and record complete
   tree/package/interface/model/catalog hashes.
3. Open a fresh user-owned evaluator task. The harness author may use only the
   fixed public contracts and input authority and must freeze a new harness.
4. Open a separate blind-runner task and execute all 34 public gates exactly as
   frozen. Seal the output package without scoring or substitutions.
5. Score in a separate read-only task and adjudicate every public gate.
6. Proceed only if all 34 public gates pass; then select and freeze a genuinely
   unseen private holdout under the hard-isolation policy.
7. Publish one candidate-bound Phase 1 exit report. Any product or contract
   change starts a new candidate and public attempt.
