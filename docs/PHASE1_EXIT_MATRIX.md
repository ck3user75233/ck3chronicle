# Phase 1 exit matrix

Release candidate: **not frozen; no candidate hash assigned**.

Status: **Phase 1 not exited**.

This matrix distinguishes implemented behavior, fast regression coverage, and
formal candidate-bound release evidence. `Partially covered` is not a pass.

## Summary

| Status | Gates |
|---|---:|
| Historical proof on an older candidate | 1 |
| Partially covered | 23 |
| Untested | 11 |
| Missing or contract-incompatible public surface | 0 |
| Total | 35 |

The older `52a43254f847555a871833ef4a43bd97f3613bf6` candidate has one separated
real-evidence lexical calibration and one zero-byte proof. Neither transfers
automatically to the future frozen candidate. The remaining frozen Phase 0
real-evidence oracles are not yet executed by an independent current harness.
The fast reboot suite remains implementation regression coverage only.

## Capture

| Gate | Current status | Evidence and gap |
|---|---|---|
| `P1-CAP-01` | Partially covered | Tiny independent six-file fixture verifies finalization; the frozen real capture oracle has not run for the audited candidate. |
| `P1-CAP-02` | Partially covered | Duplicate archive/session reuse is tested; no formal gate record. |
| `P1-CAP-03` | Untested | Archive corruption is detected, but each single-byte source mutation has not been recaptured and compared. |
| `P1-CAP-04` | Partially covered | Rapid relaunch rejection is tested; the exact source-mutation command result/envelope is not. |
| `P1-CAP-05` | Partially covered / contract reconciled | The stable public command envelope distinguishes archive, model, database, reconciliation, and pipeline failures. A finalized content-addressed archive may deliberately survive database registration failure and is recovered by reconciliation; this is the frozen recoverability rule, not a partial-success ambiguity. The independent fault matrix has not run. |
| `P1-CAP-06` | Partially covered | Missing debug and zero-byte error paths are tested separately; complete public-command outcomes are not. |

## Runtime context

| Gate | Current status | Evidence and gap |
|---|---|---|
| `P1-RUN-01` | Partially covered | Production now exposes archived file identity, line/byte range, block SHA-256, counts, and termination evidence. A read-only real-shape probe found one complete 27-DLC/104-mod block at lines 537–667, but the distinct frozen 27-DLC/94-mod oracle has not run independently. |
| `P1-RUN-02` | Partially covered | One Workshop and one local mount are tested, not the complete frozen sequence. |
| `P1-RUN-03` | Untested | No independent swap-order metamorphic gate. |
| `P1-RUN-04` | Partially covered | Production explicitly implements complete, partial, absent, malformed, truncated, and ambiguous states with focused implementation regressions. The independent frozen state oracle has not run. |
| `P1-RUN-05` | Partially covered | Inventory names/descriptors/warnings are now a separate enrichment projection and cannot change authoritative membership/order or source-resolution identities. The independent inventory-mutation gate has not run. |

## Parsing and persistence

| Gate | Current status | Evidence and gap |
|---|---|---|
| `P1-PAR-01` | Partially covered | `P1-PAR-01-LEXICAL` passed a separated blind-runner/read-only-scorer comparison of all 28,131 frozen blocks with zero field mismatches. Persistence against the compact current schema is not yet independently scored. See `PHASE1_LEXICAL_CALIBRATION_2026-08-14.md`. |
| `P1-PAR-02` | Untested | No audited-candidate exact comparison with the independently approved semantic records. The later human-reviewed empirical contracts must first be reconciled with the older 252-item oracle. |
| `P1-PAR-03` | Partially covered | Duplicate blocks retain separate occurrences and shared raw content; the complete cluster/signature relation is not asserted. |
| `P1-PAR-04` | Partially covered | Locator grammar now precedes L1 and typed PostValidate rejects a locator in a key slot; the complete independent provenance/absolute-root mutation matrix has not run. |
| `P1-PAR-05` | Partially covered | Conservative semantic rejection examples exist, not every required independent family mutation. |
| `P1-PAR-06` | Partially covered | Typed PostValidate and conservative fallback have focused development tests and read-only real-session probes. No independent authentic positive/near-miss gate for every extractor or frozen 33-versus-20,156 gate has run. |
| `P1-PAR-07` | Partially covered | Mixed line endings and final-newline behavior are tested; the full malformed/BOM/long-line/replacement/truncation matrix is not. |
| `P1-PAR-08` | Partially covered | A development regression injects failure after one streamed replacement block and proves the prior canonical projection is identical; the independent exit gate has not run. |
| `P1-PAR-09` | Partially covered | Missing evidence leaves `not_started`; generic injected first-parse failure and public exit behavior remain untested. |
| `P1-PAR-10` | **Historical proof on older candidate** | Present zero-byte `error.log` committed succeeded state with every required counter exactly zero on `52a...`; rerun is required after candidate freeze. |
| `P1-PAR-11` | Partially covered | Repository/audit invariants and real-session totals reconcile; the frozen reference and future holdout executions are absent. |

## Reporting and public workflow

| Gate | Current status | Evidence and gap |
|---|---|---|
| `P1-REP-01` | Partially covered / contract reconciled | `process-pending` is now the documented canonical vertical slice with one command-result envelope; the obsolete `analyze --logs` expectation is explicitly retired. No complete independent report oracle has run. |
| `P1-REP-02` | Untested | Text and JSON share data in implementation, but no independent field-equivalence gate exists. |
| `P1-REP-03` | Partially covered | Stored report works after `error.log` removal; `latest` and `errors` have not been proven unchanged in the same gate. |
| `P1-REP-04` | Untested | No before/after database and evidence hashes for every report command. |
| `P1-REP-05` | Partially covered | Repeat processing is deterministic; randomized insertion-order equivalence is absent. |
| `P1-REP-06` | Partially covered | `latest` selects the newest reportable run and `report --run` distinguishes repeated observations of identical evidence. The independent eligibility/order gate has not run. |
| `P1-REP-07` | Partially covered | `process-pending`, `report`, `latest`, and `errors` share a stable success/warning/failure envelope and exit taxonomy. The independent all-command black-box gate has not run. |

## Release gates

| Gate | Current status | Evidence and gap |
|---|---|---|
| `P1-HOLD-01` | Untested | The 194,022-occurrence run proves evaluator/runtime compatibility only. No post-freeze private holdout has run. |
| `P1-MUT-01` | Untested | No mutation campaign or mutant-kill ledger. |
| `P1-PERF-01` | Untested | No prescribed parser warmup + five-run timing/RSS record. |
| `P1-PERF-02` | Untested | No prescribed runtime-extraction performance record. |
| `P1-PERF-03` | Untested | No prescribed stored text/JSON reporting performance record. |
| `P1-PERF-04` | Untested | No prescribed end-to-end performance record. |

## Required order of work

1. Freeze the updated public Phase 1 contract, gate-to-interface handoff,
   complete output schemas, and exact error taxonomy. Implementation agents
   stop writing execution logic at that boundary.
2. Reconcile and freeze semantic authority from the later human reviews.
3. Freeze a clean candidate commit and record its complete tree/interface
   hashes.
4. Have the independent harness authority write the real
   capture/runtime/lexical runners from the published interface, without
   importing production expectation logic.
5. Independent evaluator roles run calibration, failure, rollback, mutation,
   and performance gates.
6. Select a new private holdout and use the separated runner/scorer process in
   `PHASE1_EXIT_PROTOCOL.md`.
7. Publish a single candidate-bound exit report.
