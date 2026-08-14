# Testing authority

## Rule

Only tests authored for the 2026-08-13 takeover contract count toward product
acceptance. The inherited test tree was archived and removed.

Every acceptance test must state or document:

- the requirement it covers;
- its observable output;
- the independent source of the expected result;
- relevant mutations that must change the result;
- irrelevant mutations that must not change it;
- whether its evidence was excluded from learner training.

The fast suite is checkpoint regression coverage. Phase exit requires the
separate role-bound process in `PHASE1_EXIT_PROTOCOL.md` and a gate-by-gate exit
record against one frozen candidate.

## Exit-test separation of duties

- The implementation/orchestration authority documents callable functions,
  CLI commands, inputs, outputs, side effects, and schemas. It does not write
  or run executable exit harnesses, exit fixtures, mutation campaigns, or
  scorers.
- An independent test-harness author turns that public interface contract into
  runner code without receiving expected answers or modifying product code.
- The implementer freezes the candidate before private holdout designation and
  cannot access private inputs, expected answers, or answer-level scorer output.
- The blind runner receives the candidate, input package, and public command
  manifest, but no expected answers.
- The oracle custodian freezes expected answers independently of production
  output.
- The read-only scorer receives immutable runner outputs and the private oracle
  but cannot execute or import the candidate or modify its outputs.
- A release adjudicator verifies artifact hashes, role separation, every named
  gate, and the final decision.

Subagents inside one Codex task share filesystem and tool authority, so prompt
separation alone is procedural, not a hard security boundary. A release-grade
blind holdout requires user custody, separate OS identities/ACLs, or external
CI jobs with isolated secrets. The exit report must state the actual isolation
level.

Implementation-authored unit and regression tests remain valuable fast-suite
controls. They are not exit tests, even when they call the same product seam or
use the same public calibration input.

## Permitted oracles

- literal expected records derived from the approved product contract;
- human semantic adjudications;
- independently calculated byte counts and cryptographic hashes;
- manually specified filesystem and database states;
- protected external evidence with frozen, independently reviewed manifests.

## Forbidden oracles

- serializing production output and treating it as expected output;
- copying production SQL, tokenization, normalization, or aggregation into a
  test;
- using learner output as human truth;
- letting a crafted positive example stand in for full-corpus behavior;
- measuring acceptance on evidence used to train the model.

## Current suite

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider tests
```

The suite currently covers:

- lifecycle state transitions and heartbeat behavior;
- copy-first exact-byte protection and rapid-relaunch rejection;
- six-file independent SHA-256/bundle oracle;
- single-pass finalization hashing;
- deduplicated archive identity;
- transactional session/manifest registration;
- archived-byte corruption detection;
- exact lexical block spans, hashes, and identities;
- `error.log`-only canonical storage;
- explicit empty-log success and missing-evidence failure;
- block-at-a-time canonical persistence without the legacy whole-session batch
  boundary;
- failed reparse rollback after partial replacement work and persisted
  per-block distribution validation before success;
- exact approved-model hash and contract validation;
- source-family isolation and semantic-change rejection;
- key and locator invariance;
- locator-before-L1 typing and rejection of a locator in a key slot;
- typed template PostValidate with conservative L2-to-L1 fallback;
- grammar-preserving two-key scope normalization;
- optional-key extraction;
- full, L1+L2, L1-only, and unknown classification behavior;
- one-row-per-semantic-unit database provenance;
- two identical raw blocks retaining two source/occurrence rows but one exact
  raw-content dictionary row;
- repeated complete classifier results retaining independent assignments but
  one lossless payload row;
- legacy-schema migration preserving every relationship with clean foreign
  keys, followed by automatic verified physical page reclamation;
- forged raw-hash/content disagreement rolling the entire migration back;
- incremental timestamp counting that reads appended bytes once and resets on
  truncation;
- exact-boundary detection requiring stable 100,000 error headers plus
  independently advancing `game.log` evidence;
- classification from stored source blocks without reopening archives;
- same-model idempotence and atomic reclassification rollback;
- rejection of unparsed sessions;
- deterministic classify JSON and stored-record review-queue output;
- explicit empty filtered review queues;
- database-only executive report structure and readable contract templates;
- capture-time latest ordering independent of session registration ID;
- bounded report/error JSON projections;
- end-to-end and second-run idempotence for `process-pending`;
- cross-session semantic deltas despite changed keys, locators, and line
  numbers;
- chronological CLI selection and bounded deterministic comparison JSON;
- observed error-window rates and quality metadata;
- immutable, case-insensitive named baselines pinned to a model revision;
- mandatory-reason ignore annotations that remain visible in comparisons;
- compatible report-plus-comparison envelopes for `report --since`;
- Mounted Data authority over inventory membership and order;
- disabled-mod exclusion, Workshop/local identity, mismatch visibility,
  missing-debug state, reparse rollback, and context CLI JSON;
- mounted mod addition/removal/load-order movement in session deltas;
- active-root-only file resolution with ordered base/DLC/mod instances;
- explicit inactive-root exclusion, path-traversal rejection, and CLI JSON;
- immutable one-pass source fingerprints despite later live-file changes;
- exact-relative-path file winners separated from on-action/culture domain
  policies;
- stored source-instance change correlation across compared sessions;
- read-only database audit success over a complete archive/index shape;
- explicit parser-counter corruption and orphan-archive detection;
- bounded schema-versioned database-audit CLI JSON;
- new/worse action triage, stored raw-block locator fallback, malformed locator
  rejection, active-source links, bounded CLI JSON, and review separation.

The current suite does **not** constitute Phase 1 exit testing. Its foundation
oracles are intentionally small (including a three-block lexical fixture and a
two-DLC/two-mod runtime fixture), it does not contain a complete independently
frozen report result, and it has not executed the full protected-real-evidence,
mutation, private-holdout, or five-run performance gates against one frozen
candidate.

## Protected-corpus compatibility gate

`tools/evaluate_classifier.py` is a read-only coverage utility. It was run
against the three reviewed holdouts and two untouched candidates excluded from
training. The production runtime exactly reproduced the frozen release
evaluator's assignment counts across 194,022 semantic occurrences:

| Evidence | Full | L1+L2 | L1-only | Unknown |
|---|---:|---:|---:|---:|
| 3 reviewed holdouts | 67,115 | 6 | 49 | 275 |
| 2 untouched candidates | 126,505 | 48 | 15 | 9 |

This proves compatibility with the reviewed model/evaluator pair. It does not
turn the old evaluator into a semantic oracle or satisfy `P1-HOLD-01`;
human-authored normalization and assignment tests provide development
authority, while the release holdout must remain private until candidate
freeze.
