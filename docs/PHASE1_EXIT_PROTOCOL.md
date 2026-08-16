# Phase 1 exit protocol

Status: required release process; no valid Phase 1 exit has been accepted. The
latest candidate-bound public disposition is recorded in
`PHASE1_EXIT_MATRIX.md`.

## 1. Purpose

The Phase 1 exit is an evaluation of one frozen release candidate, not a final
development test run. Expected answers must not influence implementation or
candidate execution.

## 2. Separation of duties

### Implementer

- may read public contracts, training evidence, and ordinary regression tests;
- may implement and run the fast suite;
- publishes only the callable product interface, input/output contract, and
  operational instructions needed by independent evaluators;
- may not author, edit, or run executable exit-test harnesses, exit fixtures,
  mutation campaigns, private-holdout selectors, or scorer code;
- may not read private holdout inputs, private expected answers, or scorer
  output before the release candidate is frozen;
- supplies only a commit hash and documented public execution commands.

Implementation-authored unit and regression tests are permitted development
controls. They can never be promoted into exit evidence by renaming them.

### Independent test-harness author

- receives the frozen public evaluation interface and gate contract, but no
  private expected answers;
- receives an immutable public gate-to-input manifest and may not replace,
  truncate, synthesize, or reassign its base evidence;
- independently writes the execution harness, result-envelope capture,
  mutations, resource measurements, and cleanup behavior;
- cannot modify product code or ask the implementer to provide executable
  test logic;
- freezes and hashes the harness before the release candidate receives its
  private holdout run;
- hands only the frozen harness and public invocation manifest to the runner.

### Oracle custodian

- selects and protects the unseen holdout;
- holds expected lexical, semantic, runtime, and report answers;
- records hashes and provenance before execution;
- does not modify the candidate or runner outputs;
- does not accept implementation-authored runner or scorer logic as exit
  authority;
- does not disclose answer-level failures to the implementer during the same
  release attempt.

### Blind runner

- receives the frozen candidate, evaluator-authored harness, public invocation
  manifest, and input package;
- does not receive expected answers, scorer rules containing answer values, or
  prior answer-level failure reports;
- executes only the declared commands in a clean environment;
- writes stdout, stderr, exit status, timing, peak RSS, environment identity,
  input hashes, candidate hash, and output hashes to an append-only result
  envelope;
- never edits or normalizes candidate output after execution.

### Read-only scorer

- receives immutable runner outputs plus the private oracle only after the run
  closes;
- performs no candidate execution and makes no source or result changes;
- compares with an independently implemented scorer or manual adjudication;
- emits gate-level pass/fail and bounded discrepancy classes;
- cannot silently bless missing fields through aggregate accuracy.

### Release adjudicator

- verifies role separation, artifact hashes, gate completeness, and exception
  records;
- accepts or rejects the exit report;
- does not convert an unexecuted or partially scored gate into a pass.

## 3. Isolation levels

### Required public procedural task separation

The implementation task stops after freezing the candidate and its public
handoff. The remaining public roles use fresh user-owned tasks:

- a fresh evaluator task authors and freezes the harness without private
  expected answers;
- a separate blind-runner task receives only the frozen candidate, harness,
  public inputs, and invocation manifest;
- a separate read-only scorer task receives sealed outputs and must not invoke
  or import the candidate;
- an adjudicator task verifies identities, dispositions, and exceptions.

The harness author and runner may not be subagents of the implementation task.
Handoffs use hash-bound files rather than prose copied between agents. Separate
tasks provide context and role separation but still are not a hard security
boundary when they share the same OS account and filesystem.

### Hard isolation required for a release-grade blind holdout

At least one of the following must hold:

- the user retains the private oracle and provides only the final score;
- runner and scorer use separate OS accounts with filesystem ACLs;
- an external CI system exposes holdout inputs only to the runner job and
  expected answers only to a non-executing scorer job;
- encrypted oracle material is decrypted only inside the scorer environment
  using a secret unavailable to implementer and runner.

The Phase 1 exit report must state which isolation level was actually used. A
procedural Codex-only run must not be described as cryptographically blind.

## 4. Freeze and handoff order

1. Freeze public contracts, the gate inventory, the implementation-authored
   callable-interface handoff, exact public gate/scoring rules, performance
   budgets, and the public gate-to-input manifest.
2. Freeze the candidate commit, require a clean worktree, and record its
   source-tree, package, interface, model, and catalog hashes.
3. In a fresh evaluator task, the independent harness author writes, validates,
   and freezes execution code from the handoff and fixed input set without
   receiving expected answers. Prescribed mutations must derive from and remain
   hash-bound to the assigned base unit.
4. In a separate blind-runner task, execute all public gates exactly once and
   close/hash the result package.
5. In a separate read-only scorer task, score the sealed public results without
   executing or importing the candidate; then adjudicate every gate.
6. Proceed only if every public gate passes for the same candidate. Then select
   a holdout whose content hashes are absent from training,
   adjudication, debugging, and implementation evidence.
7. Freeze the private oracle before candidate execution.
8. Execute the private gate under one of the hard-isolation methods in
   section 3, then close and hash its result package.
9. Give the read-only private scorer the closed result package and private
   oracle.
10. Give the adjudicator all gate scores, provenance, isolation statement, and
   exception log.

Any candidate change after step 2 starts a new release attempt. Any oracle
change after step 7 invalidates the run unless the adjudicator records an
oracle defect and restarts from a newly versioned oracle.

The harness author cannot alter a frozen input assignment, product expectation,
mutation validity rule/kill criterion, or performance budget. A case whose
required input, mutation precondition/application count, observation, or
result-envelope closure fails is infrastructure/unscored; it cannot be called a
product pass or failure and cannot be replaced silently.

## 5. Artifact contract

Every release attempt has immutable files equivalent to:

```text
attempt.json
candidate.manifest.json
evaluation-interface.json
public-run-plan.json
evaluator-harness.manifest.json
input.manifest.json
runner-result.json
outputs/<gate-id>/...
timings.json
scorer-result.json
exit-report.md
```

`attempt.json` binds the candidate commit, public contract versions, input
manifest hash, evaluation-interface hash, evaluator-harness hash, runner-result
hash, scorer-result hash, role identities, and isolation level. Every JSON file
has an explicit schema version and canonical SHA-256.

The runner result records output bytes exactly. The scorer never consumes an
unhashed mutable working file.

Retained result packages are bounded evidence packages, not copies of every
scratch workspace. After each case is closed and its declared observations,
stdout/stderr, database projections, timings, mutation descriptors, and hashes
are sealed, the runner removes disposable copied inputs and runtime trees.
Immutable base evidence remains in the locked corpus. A failed case may retain
only the smallest hash-bound artifact needed to reproduce the discrepancy;
keeping complete repeated 100+ MiB workspaces is not an exit requirement.

## 6. Failure disclosure and reruns

- Development/calibration gates may return detailed discrepancies.
- A private holdout failure returns only gate ID, discrepancy class, and
  bounded counts during the failed attempt.
- Expected values and raw private examples remain sealed until the release is
  abandoned or accepted under the custodian's disclosure policy.
- Fixing a failure requires a new candidate hash and a new attempt.
- The same exposed holdout cannot remain "unseen" for the next candidate.
- Infrastructure failures are recorded separately and may be rerun only when
  candidate, input, oracle, and public command hashes are unchanged.

## 7. Learner-data separation

Each evidence file is assigned exactly one role by content hash:

- training;
- human calibration/adjudication;
- public regression;
- private holdout;
- untouched future candidate.

Aliases, copied files, and content-addressed duplicates retain the same role.
No holdout failure may be promoted into training while still being cited as
holdout evidence for a later candidate.

## 8. Phase 1 decision rule

Phase 1 passes only when every named gate passes for the same candidate and
attempt lineage. Aggregate classifier coverage, a green fast suite, a clean
database audit, or a successful manual demonstration cannot substitute for an
unexecuted gate.
