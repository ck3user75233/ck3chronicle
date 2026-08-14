# Project phase plan

This document is the authoritative phase plan for the ck3chronicle reboot.
`ROADMAP.md` is a capability inventory and must not be used to infer phase
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

## Reboot Phase 0: audit and Phase 1 definition

Status: **complete**.

This was a planning and evidence-control phase, not the product's original
"Evidence Preservation" phase. It:

- audited and archived inherited source, tests, plans, and prototypes;
- established the reboot test-authority rule;
- froze capture, runtime, lexical, and initial semantic evidence artifacts;
- defined the Phase 1 product and acceptance contracts;
- established checkpoint and commit boundaries.

The semantic acceptance oracle still requires reconciliation with the later
human-reviewed empirical-template work before Phase 1 release testing. The
original Phase 0 artifact is historical evidence until that reconciliation is
recorded.

### Historical product Phase 0

The older multiphase packet separately called evidence preservation and the
session registry "Product Phase 0." It was never formally reviewer-exited, and
its crash-folder, `show-session`, and full `doctor` criteria are not all met by
current HEAD. The reboot subsumes retained capture requirements into its Phase
1 vertical slice; completion of the planning Phase 0 must not be cited as
completion of that historical product phase.

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
  including crash termination and principal-log origin provenance;
- canonical `error.log` block/occurrence storage;
- versioned empirical classification and review queues;
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

1. Freeze the implemented process/report command envelopes, complete text/JSON
   projections, and exact failure taxonomy for independent scoring.
2. Reconcile the Phase 1 semantic oracle with the PostValidate-protected,
   user-approved empirical
   template model, including locator recognition before L1 assignment.
3. Publish the callable evaluation interface for every gate; an independent
   harness author maps it to runner code, while a separate oracle authority
   owns expected artifacts and scorer rules.
4. Have the independent evaluation authority adapt protected real-evidence
   harnesses to the current compact schema.
5. Independently freeze the complete report and command-envelope oracle.
6. Provide the supported public vertical-slice command and exact failure
   envelopes.
7. Freeze the release candidate before the private holdout is scored.
8. Execute correctness, rollback, mutation, holdout, and performance gates.
9. Publish and review the Phase 1 exit report.

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
