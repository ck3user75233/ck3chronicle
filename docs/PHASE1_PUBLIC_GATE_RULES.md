# Phase 1 public gate rules

Status: normative successor-attempt authority. These rules and the immutable
gate-to-input manifest freeze before independent harness authorship. A harness
author implements them but cannot change the input assignment, case validity,
expected product outcome, mutation kill, or performance budget.

## Case validity and scoring

A case whose base input hash, declared precondition, exact mutation application
count, derived-input hash, required observation, or runner result envelope does
not verify is infrastructure/unscored. It is neither a product pass nor a
product failure, and the harness may not silently substitute another input or
operation. All row-level rules prevail over aggregate totals.

## `P1-PAR-02` canonical semantics

The frozen input authority supplies `DEV-REF-63E97B` plus
`DEV-SEMANTIC-252`. Before scoring, independently verify the semantic oracle's
hash, normative schema/status, linked error-log hash, 252 unique sample IDs,
and 252 unique manifest block indices. Candidate results must cover exactly
those 252 blocks with no missing, extra, or duplicate sample. Join by
independently recomputed block index and raw-block hash, never by a product
signature.

Every sample must exactly match:

- accounting disposition and issue cardinality;
- category, error type, severity, and confidence;
- primary file and primary line;
- referenced symbols and referenced objects, using the oracle's canonical
  array order;
- stored occurrence-to-source-block linkage.

`proposed_error_type`, rationale, uncertainty, and adjudication metadata are
not production fields and are not scored. The required totals are 232
classified and 20 preserved unclassified, but totals cannot compensate for a
row mismatch. An absent or invalid oracle is infrastructure/unscored.

## `P1-PAR-04` locator-root metamorphism

Use an authentic absolute path in the assigned `PUB-LONG-20260429` evidence.
A valid mutation starts at a token boundary, matches exactly one drive letter
followed by `:/` or `:\\` inside an already-tokenized `<LOCATOR>`, excludes URI
schemes such as `event:/`, changes only that root prefix, and preserves the
locator suffix plus every non-locator byte. Record original/replacement spans,
byte offsets, before/after hashes, and application count.

Pass requires the value/raw evidence hash to change while the locator remains
typed `<LOCATOR>`. Non-locator normalized tokens, category, error type,
severity, issue signature, assignment level, contract ID, L1, and L2 remain
identical. Only locator-valued provenance may change.

## `P1-REP-06` run selection

Use this fixed chronology:

1. normal run A over `PUB-RUNTIME-COMPLETE-20260816`;
2. later normal run B over the same evidence;
3. later crash run C over `PUB-CRASH-20260428`, including `exception.txt`;
4. newest run D over `PUB-NOMINAL-20260510`, registered but deliberately not
   parsed or classified.

Pass requires A/B to be distinct run/capture IDs linked to one evidence
session; report/errors `--run` to expose and return the exact requested run;
`report --session` to select B; C to project exact crash, file-origin, and
exception path/hash/size/source-time provenance; and `latest` to skip
unreportable D and select C. Ordering is `observed_ended_at DESC, run_id DESC`.
Evidence-bundle timestamps cannot substitute for run chronology.

## `P1-REP-07` command taxonomy

Every JSON case emits exactly one command-result object on stdout, with no
diagnostic contamination, matching process/envelope exit codes, and documented
status/result/error nullability.

| Case | Required preparation | Required result |
|---|---|---|
| success | Valid processable pending evidence | exit 0, succeeded |
| readiness | Integrity-valid current DB with a known finalized but unparsed/unclassified target | exit 2, `report_unavailable` or `errors_unavailable`, stage `report` |
| archive | Registered archive corrupted after registration | exit 3, `archive_integrity`, stage `archive` |
| model | Approved model bytes fail integrity | exit 4, `model_invalid`, stage `classifier` |
| database | Existing unopenable, unsupported, or corrupt SQLite target | exit 5, `database_failed`, stage `database` |
| pipeline | Non-domain `RuntimeError` installed before the first processing invocation and reached exactly once | exit 1, `processing_failed`, stage `pipeline` |

An absent database does not exercise readiness. A pipeline injection installed
after work, or not reached exactly once, is invalid infrastructure.

## `P1-MUT-01` mutation kills

This is an eleven-variant input-fault/metamorphic campaign, not source-code
mutation testing. Every variant derives from its assigned hash-bound base.

| Variant | Required primary delta and protected invariants |
|---|---|
| `remove_error_log` | Capture rejects the missing mandatory file and publishes no pending completion, archive, session, or run. |
| `zero_error_log` | Capture/process succeeds with zero parse, classification, and report populations. |
| `archive_integrity_fault` | Strict processing returns exit 3 / `archive_integrity` with no false successful derived update. |
| `newline_variant` | Byte identity changes; block/semantic accounting remains equivalent with zero silent drops. |
| `locator_path` | Locator value changes; typed locator and semantic/template identity remain stable. |
| `semantic_literal` | The sample cannot retain the same full contract assignment. |
| `truncated_tail` | Tail receives an explicit occurrence/unknown disposition with zero silent drops, or processing fails transactionally. |
| `swap_mount_order` | Only authoritative order and its provenance hash change. |
| `runtime_absent` | Status is `absent`; authoritative mount arrays are empty. |
| `runtime_malformed` | Status is `malformed`; no fabricated valid mounts appear. |
| `inventory_metadata` | Only enrichment changes; authoritative identity/order and resolver roots remain identical. |

The gate passes only when all eleven valid variants satisfy their primary delta
and protected invariants. No percentage threshold applies.

## Performance budgets

Use `PUB-STRESS-20260806`: a 39,719,864-byte/100,000-block `error.log`, a
60,804,434-byte `debug.log`, and a 139,932,278-byte complete locked unit. Run one unscored
warmup followed by five successful measured repetitions. The median is the
third sorted value; the fourth value is the fourth-smallest, equivalently at
least four of five results meet that wall ceiling. Peak RSS is the maximum
sampled resident set across the five measurements.

Input preparation is outside the timed region except `P1-PERF-04`; its complete
wall measurement begins with the evidence copy and ends when
`process-pending --json` exits.

| Gate/seam | Median wall | Fourth wall | Peak RSS | Additional rule |
|---|---:|---:|---:|---|
| `P1-PERF-01` lexical | <= 2 s | <= 3 s | <= 64 MiB | Exactly 100,000 lexical blocks each run |
| `P1-PERF-01` canonical parse | <= 15 s | <= 20 s | <= 128 MiB | Identical counters and stored projection |
| `P1-PERF-02` runtime context | <= 1.5 s | <= 2 s | <= 64 MiB | Identical runtime projection |
| `P1-PERF-03` each function/text/JSON report | <= 1.5 s | <= 2 s | <= 96 MiB | Storage hash unchanged |
| `P1-PERF-04` complete pipeline | <= 180 s | <= 240 s | <= 512 MiB | Median child CPU <= 180 s; identical successful results |

All five repetitions must succeed and remain logically equivalent. Timing
tolerance never excuses a crash, timeout, or inconsistent counter. A result
whose wall time exceeds four times its child CPU may be rerun once only when
hash-bound host-suspension evidence overlaps it; otherwise it remains in the
five-value set.
