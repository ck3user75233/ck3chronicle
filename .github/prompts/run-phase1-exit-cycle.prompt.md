# Run the ck3chronicle Phase 1 public exit cycle

You are the independent Phase 1 evaluation coordinator and harness authority
for ck3chronicle. This is a fresh user-owned Codex task, separate from the
implementation task. Complete the public evaluation cycle without requiring
the user to relay messages between roles.

## Frozen candidate

- Repository: `https://github.com/ck3user75233/ck3chronicle.git`
- Candidate commit:
  `23a2534db3923dc83e7fa84c69a628b1932fd1f6`
- Product repository on this PC is the standalone `ck3chronicle` checkout.
- `ck3raven` is not an implementation or output root. Do not edit, stage,
  commit, or generate any file inside `ck3raven`. Read-only access to the
  already locked corpus is permitted if that is where its exact manifest is
  found.

Before doing anything else, verify the candidate commit exists, its tree is
clean and complete, and the canonical remote is exact. Never modify the
candidate. Put all evaluator harnesses, scratch trees, outputs, and result
packages in a new attempt directory under the user-level external WIP root
`%USERPROFILE%\.ck3raven\wip\ck3chronicle-phase1\`, never inside either source
repository.

## Phase truth

This is **Phase 1 exit testing**. The reboot foundation was unnumbered
planning/audit work, not a product test phase. Do not resurrect or execute the
pre-reboot Phase 0 launch packet. The earlier rejected fake/substituted-input
run was also a Phase 1 attempt.

No Phase 1 gate is inherited. Run all 34 public gates against this one
candidate. `P1-HOLD-01` remains unselected and unexecuted unless and until all
34 public gates pass and a separately protected unseen holdout is authorized.

## Required public authorities

Read completely, in this order:

1. `AGENTS.md`
2. `docs/WORKSPACE_ROUTING.md`
3. `docs/PROJECT_PLAN.md`
4. `docs/PROJECT_STATUS.md`
5. `docs/PHASE1_EXIT_MATRIX.md`
6. `docs/PHASE1_EXIT_PROTOCOL.md`
7. `docs/PHASE1_EVALUATION_INTERFACE.md`
8. `docs/PHASE1_PUBLIC_GATE_RULES.md`
9. `docs/PHASE1_OUTPUT_CONTRACTS.md`
10. `docs/PHASE1_SEMANTIC_AUTHORITY.md`
11. `docs/PRODUCT_CONTRACT.md`
12. `docs/TESTING.md`

The public base-input authority is locked corpus v2:

- schema version: 2
- units/files: 9 units / 42 files
- manifest SHA-256:
  `407e47d12bc17f30e2abd453dc69c4dda0b4e3fab705e2e361e6d26a8e6a6147`
- source-set SHA-256:
  `f4b95276058f5b4f379de6e443e585b6fe8040ed3202b8f886e91c44a4f60c51`

Locate the already locked `locked-corpus-v2-public/corpus.manifest.json`
read-only and verify the exact manifest, source set, file set, sizes, hashes,
and symlink/reparse constraints before reading normative content. Stop on any
mismatch. Do not regenerate, normalize, truncate, resample, substitute, or
reassign a base input. Synthetic data is permitted only for harness self-tests
and can never score an authentic-evidence gate.

The `DEV-SEMANTIC-252` answer artifact belongs only to the read-only scorer.
The harness author may bind its declared identity without opening its answer
contents. The blind runner must not receive it.

### Fail-closed designated-input enforcement

The `gate_inputs` object inside the exact corpus manifest is normative, not a
menu or example. Preserve its complete 35-gate mapping verbatim in the harness
plan. The evaluator has no discretion to choose a different unit, a smaller
sample, another real log, or synthetic data for a scored case.

Before harness authorship, publish a neutral input-authority preflight that
records, for every gate, the exact assigned unit names and their declared file
paths, sizes, hashes, and source-set identities. It must prove:

- all 35 gate keys occur exactly once, including the disabled private
  placeholder;
- every public case uses only units assigned to its gate by `gate_inputs`;
- every assigned unit and file matches the locked manifest exactly;
- no prefix, first-N-line subset, truncation, reconstructed sample, or
  evaluator-created replacement is used as base evidence;
- any derived mutation retains the immutable base identity, records the exact
  derived identity and byte delta, and satisfies the prescribed precondition
  and application count.

Any mismatch aborts before candidate execution and is reported as
`INFRASTRUCTURE_INVALID_INPUT`; it cannot be repaired by substituting a
different input within the attempt. The harness reviewer must compare the
machine plan back to `gate_inputs`, not merely confirm that all nine corpus
units exist.

Be efficient: verify the locked source corpus once at runner preflight. During
case staging, compute the staged or derived file hash as part of that copy or
derivation and compare it with the declared identity. Do not repeatedly hash
the same immutable source file merely to prove the same authority again.

## Role and execution boundaries

1. Independently author a new harness from the current public contracts and
   fixed gate-to-input authority. Do not copy, patch, import, or execute an old
   harness from `evaluation/archive/` or a prior WIP attempt.
2. The harness must contain all 35 named gates, with 34 executable public gates
   and one hard-disabled private placeholder. It must use finite process-tree
   safety ceilings, no retries, per-case atomic closure, exact result hashes,
   bounded retained artifacts, and explicit infrastructure/unscored outcomes.
3. Use prescribed hash-bound mutations only. A failed mutation precondition or
   missing required observation is infrastructure/unscored, never a product
   pass or failure.
4. You may use a read-only reviewer subagent to audit the harness, but do not
   start the public run until the harness is frozen, read-only, hash-manifested,
   and independently reviewed GO.
5. Create a **separate user-owned blind-runner task** with the Codex task tool.
   Give it only the frozen candidate, harness, public inputs, and invocation
   manifest. It must execute each public case exactly once, never score, never
   read expected answers, and seal the neutral output package.
6. After runner closure, create a **separate user-owned read-only scorer task**.
   It receives sealed outputs plus the public scoring/oracle authority, does
   not execute or import the candidate, and emits gate dispositions with exact
   artifact citations.
7. Create or commission a separate adjudication role to verify identities,
   role separation, all gate dispositions, exceptions, and the final public
   recommendation. Missing or invalid cases cannot be converted to passes.
8. If the product fails, preserve bounded evidence and report the exact public
   defect classes. Do not modify the candidate or start a second attempt.
9. If infrastructure fails, preserve the failed package, repair only the
   independently owned harness in a new version, obtain a new reviewer GO, and
   follow the frozen rerun policy. Never silently replace an input or result.
10. If all 34 public gates pass, report `PUBLIC READY FOR PRIVATE HOLDOUT` and
    stop before selecting or opening private material. Phase 1 is not exited
    until `P1-HOLD-01` later passes under the hard-isolation protocol.

If the Codex task-creation tools needed for separate user-owned runner/scorer
tasks are unavailable, freeze the current role's artifact and produce the
exact next-role prompt and hashes; do not collapse roles into this task.

## Required completion report

Return:

- candidate commit/tree/package/model/catalog identities;
- locked-corpus manifest/source-set verification;
- harness manifest, source-set, plan, and reviewer verdict;
- runner package identities and complete case/action counts;
- scorer/adjudicator package identities;
- all 35 gate dispositions, with `P1-HOLD-01` explicitly unrun unless public
  readiness was achieved and a later authorized private cycle completed;
- counts of PASS, PRODUCT FAIL, INFRASTRUCTURE/UNSCORED, and private-unrun;
- confirmation that no candidate, corpus, `ck3raven`, or prior result package
  was modified.

Do not claim Phase 1 exit from development tests, calibration accuracy, a
partial public run, or a public-only pass.
