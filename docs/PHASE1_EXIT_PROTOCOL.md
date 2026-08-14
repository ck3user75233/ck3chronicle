# Phase 1 exit protocol

Status: required release process; no Phase 1 exit run has yet completed.

## 1. Purpose

The Phase 1 exit is an evaluation of one frozen release candidate, not a final
development test run. Expected answers must not influence implementation or
candidate execution.

## 2. Separation of duties

### Implementer

- may read public contracts, training evidence, and ordinary regression tests;
- may implement and run the fast suite;
- may not read private holdout inputs, private expected answers, or scorer
  output before the release candidate is frozen;
- supplies only a commit hash and documented public execution commands.

### Oracle custodian

- selects and protects the unseen holdout;
- holds expected lexical, semantic, runtime, and report answers;
- records hashes and provenance before execution;
- does not modify the candidate or runner outputs;
- does not disclose answer-level failures to the implementer during the same
  release attempt.

### Blind runner

- receives the frozen candidate, public runner instructions, and input package;
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

### Procedural isolation available in one Codex task

Separate subagents can be given non-overlapping instructions and context:

- the runner is not told expected answers or oracle paths;
- the scorer is instructed to remain read-only and not invoke the candidate;
- handoffs use hash-bound files rather than prose copied between agents.

This is useful separation of duties, but it is not a hard security boundary.
Codex subagents in one task share filesystem and tool authority.

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

1. Freeze public contracts and the gate inventory.
2. Freeze the candidate commit and require a clean worktree.
3. Record candidate source-tree and package hashes.
4. Freeze public calibration inputs and their independent manifests.
5. Select a holdout whose content hashes are absent from training,
   adjudication, debugging, and implementation evidence.
6. Freeze the private oracle before candidate execution.
7. Give the blind runner only the candidate, input package, and public command
   manifest.
8. Close and hash the runner result package.
9. Give the read-only scorer the closed result package and private oracle.
10. Give the adjudicator the gate scores, provenance, isolation statement, and
    exception log.

Any candidate change after step 2 starts a new release attempt. Any oracle
change after step 6 invalidates the run unless the adjudicator records an
oracle defect and restarts from a newly versioned oracle.

## 5. Artifact contract

Every release attempt has immutable files equivalent to:

```text
attempt.json
candidate.manifest.json
public-run-plan.json
input.manifest.json
runner-result.json
outputs/<gate-id>/...
timings.json
scorer-result.json
exit-report.md
```

`attempt.json` binds the candidate commit, public contract versions, input
manifest hash, runner-result hash, scorer-result hash, role identities, and
isolation level. Every JSON file has an explicit schema version and canonical
SHA-256.

The runner result records output bytes exactly. The scorer never consumes an
unhashed mutable working file.

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
