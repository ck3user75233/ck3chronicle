# Project phase plan

This document is the authoritative phase plan for the ck3chronicle reboot.
`CAPABILITY_INVENTORY.md` is a backlog inventory and must not be used to infer phase
completion.

## Status vocabulary

- **implemented**: production code exists and a focused development test may
  exercise it;
- **checkpoint accepted**: the checkpoint's independent prerequisites and
  named gates passed at a recorded commit;
- **phase exited**: every phase exit gate passed together against one frozen
  release candidate and a formal exit record was accepted;
- **prototype/groundwork**: useful code exists but has no phase-completion
  authority.

Later functionality does not make an earlier gate pass. A green fast suite is
regression evidence, not a phase exit by itself.

## Reboot foundation: audit and Phase 1 definition

Status: **complete**.

This was unnumbered planning and evidence-control work completed before the
active reboot phase. It:

- audited and archived inherited source, tests, plans, and prototypes;
- established the reboot test-authority rule;
- froze capture, runtime, lexical, and initial semantic evidence artifacts;
- defined the Phase 1 product and acceptance contracts;
- established checkpoint and commit boundaries.

The reboot's numbered plan begins at Phase 1; there is no preceding numbered
phase. Evidence preservation, session/run registration, crash provenance, and
operator-readiness requirements are part of the Phase 1 capture and reporting
gates. Superseded pre-reboot plans remain recoverable from Git history but are
not active project inputs.

The evaluation cycle that used substituted or synthetic-scale evidence and was
later rejected was a **Phase 1 exit attempt**, not a reboot Phase 0 cycle. Its
invalid results do not remove, satisfy, or rename any Phase 1 gate.

## Phase 1: first useful vertical slice

Status: **active; not exited**.

### Outcome

Given one completed CK3 run, ck3chronicle must preserve the evidence, record
the same-run ordered DLC/mod context, account for every canonical `error.log`
block, classify semantic occurrences conservatively, persist the results, and
produce deterministic stored-record reports through one supported operator
workflow.

### Current implementation inventory

The repository contains substantial Phase 1 implementation:

- auditable CK3 lifecycle observation and copy-first pending protection;
- content-addressed archive finalization and transactional registration;
- durable per-run receipts and run rows independent of deduplicated evidence,
  including crash termination, principal-log origin provenance, and default
  capture of the associated crash `exception.txt` artifact;
- canonical `error.log` block/occurrence storage;
- versioned empirical classification and review queues;
- durable assignment-level/confidence telemetry so L1-only, provisional,
  low-confidence, and unknown patterns can be reviewed and improved over time;
- memory-bounded block-at-a-time canonical persistence with transactional
  replacement and persisted distribution/provenance validation;
- typed template PostValidate after candidate assignment, including locator
  recognition before L1 and conservative L2-to-L1 fallback;
- same-run Mounted Data runtime context;
- exact Mounted Data source-file/line/byte/hash provenance, six-state parsing,
  and inventory-independent authoritative membership/order;
- stored reporting and deferred `process-pending` processing;
- database reconciliation and compact default storage.

These are implementation facts, not a Phase 1 exit claim.

Semantic coverage is intentionally revisable. Phase 1 requires explicit
accounting for every occurrence, not 100% full/L2 attribution on arbitrary
future logs. Unknown and lower-confidence outcomes remain visible review debt,
not release-blocking data loss.

### Exit authority

Phase 1 exits only when all 35 named gates in the frozen Phase 1 acceptance
specification pass against one release-candidate commit:

- `P1-CAP-01..06`;
- `P1-RUN-01..05`;
- `P1-PAR-01..11`;
- `P1-REP-01..07`;
- `P1-HOLD-01`;
- `P1-MUT-01`;
- `P1-PERF-01..04`.

The gate run must include role-separated execution/scoring, immutable artifact
hashes, the protected real evidence oracles, a genuinely unseen holdout, and a
formal exit report. No current commit has such an exit record.

### Immediate work

The latest valid public attempt evaluated candidate `1f4d8c2` and ended at 23
public passes, five product failures, and six infrastructure-unscored gates.
The private holdout was correctly blocked. The current successor development
line repairs the five product failures, but development tests and public
calibration do not transfer the prior gate results or exit Phase 1.

The public evidence corpus, gate mapping, and bytes are fixed input authority,
not evaluator discretion. Implementation agents publish function/output
contracts and the immutable input manifest but do not edit evaluator runner or
scorer code. The 252-item canonical issue-field oracle and human-reviewed
template/slot authority have separate hash-bound roles, with locator
recognition preceding L1 assignment.

Remaining work proceeds in this order:

1. Freeze a clean successor release-candidate commit and record its tree,
   package, interface, model, and contract hashes.
2. Open a fresh user-owned evaluator task, separate from the implementation
   task. In that task, have the independent harness authority write and freeze
   a new harness against the fixed public gate-to-input manifest. It may create
   only prescribed, hash-bound mutations and may not substitute base inputs.
3. Have the independent oracle authority freeze the complete report and
   command-envelope expected artifacts.
4. Run the public harness from a separate blind-runner task and score its sealed
   results without executing the candidate. Proceed only when all public gates
   pass for the same candidate.
5. Select and freeze a new unseen private holdout, then execute it under the
   hard-isolation requirements in `PHASE1_EXIT_PROTOCOL.md`.
6. Publish and review the single candidate-bound Phase 1 exit report.

## Phase 2: deltas, baselines, and noise management

Status: **not entered; partial implementation exists**.

`compare`, named baselines, ignore annotations, and `report --since` are useful
groundwork. They have not passed the original Phase 2 exit criteria together.
Crash-state deltas and the final ignore/suppression policy remain unresolved.
No Phase 2 completion claim is permitted before Phase 1 exits.

## Phase 3: source and override-chain resolution

Status: **not entered; groundwork only**.

Active-runtime exact-relative-path resolution and immutable processing-time
fingerprints exist. Full override chains, historical source bytes, predecessor
diffs, and domain-specific merge semantics do not. The current `resolve-file`
surface is not a Phase 3 exit.

## Phase 4: workspace context and likely-cause analysis

Status: **not entered**.

Runtime Mounted Data is not workspace context. Git branch/commit/dirty state,
changed-file correlation, reasoned confidence, and the original Phase 4 exit
criteria have not been implemented and accepted.

## Phase 5: fixability ranking and recommendations

Status: **not entered; triage is preliminary groundwork**.

Current triage does not implement or validate the defined evidence-weighted
fixability score and recommendation policy.

## Phase 6: agentic query layer

Status: **not entered; partial JSON surfaces exist**.

Some commands emit bounded JSON, but the stable agent-facing schema, public
query contract, and phase exit tests do not exist. MCP integration is not a
prerequisite for the core product and must not be used to bypass Phase 1.

## Later phases

Cross-run trend intelligence, IDE integration, static reference enrichment,
and guided repair remain future work. They are not active phases merely
because a prototype or capability-backlog entry exists.
