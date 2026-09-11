# Ingestion operational recovery plan

Updated: 2026-09-08

Status: active recovery plan. Production processing is disabled.

This plan restores bounded, observable CK3 ingestion without replacing the
working parser, classifier, projection catalog, or learner. It is subordinate
to the current owner decisions in `OWNER_PRODUCT_INTENT.md`,
`TRUSTED_RUN_SPEC.md`, and `CURRENT_HANDOFF.md`.

## Provenance and correction

The overlooked 2026-08-29 recovery report was recovered from dangling Git blob
`e6084af5a604281ad68fe6da158de1369632ac13`. Its useful operating method was:
one processor, durable stage telemetry, a read-only plan, explicit bounds, a
100,000-block disposable benchmark, and one-at-a-time production resumption.

The recovered draft also referred to a receipt subsystem, Phase 1 evaluator
artifacts, pre-reboot tests, and stale inventory counts. Those directions are
superseded and deliberately removed here. Legacy JSON files are one-time
metadata input for the retained pending set, not a product receipt subsystem.
No pre-reboot test or evaluator artifact is an authority or recovery target.

## Boundary: inside the checkout, outside Git

| Material | Location | Git treatment |
|---|---|---|
| Reusable product/learner source, schemas, current tests, and operating contracts | `src/`, `tools/`, `tests/`, `docs/` | Track |
| Production captures, archives, databases, journals, local learner state, benchmarks, and generated outputs | `.ck3chronicle/wip/` | Ignore completely |

The canonical local runtime remains below:

```text
.ck3chronicle/
  wip/
    runtime/
      ck3chronicle.db
      pending/
      sessions/
      crash_evidence/
      watch/
      processing/        # processor lease, JSONL journal, current status
      migration/
      backups/
    learner/
    benchmarks/
      ingestion/         # disposable scale/recovery roots
```

Any old `runtime/run_receipts/` directory is retained evidence input only until
the 22 legacy records are converted. New source must not depend on that path or
recreate a receipt lifecycle.

## Current operational checkpoint

- Canonical production database: 725,381,120 bytes, SHA-256
  `D5D4DB51D86CE7EA784B90A924EB80199CE8B3E5AE8994FD3D36596DB6C246E3`.
- Database integrity: `quick_check=ok`; no foreign-key errors; no active
  rollback journal or WAL.
- Registered sessions: 38 finalized sessions.
- Historical derived-state debt: 15 sessions lack a current semantic
  projection.
- Six retained sessions reached CK3/Paradox's known 100,000-entry `error.log`
  cap. They are valid source files with producer-censored totals, not evidence
  of parser truncation.
- Protected backlog: 22 unmodified legacy pending directories, with 22/22
  matching metadata records and seven verified exception attachments.
- Readable rehearsal copy: 22/22 pending directory names, 132 files, and
  728,770,249 bytes under
  `.ck3chronicle/wip/benchmarks/ingestion/legacy-pending-rehearsal-20260908-01/`.
  All files are readable. The watcher-record name/size/mtime inventory matches,
  the 22 metadata and seven exception hashes match, and the copy's content-set
  SHA-256 baseline is
  `5f8652229595606ba14d224488e27d64db9cad02910f1b60227d7ba4f3429387`.
- Legacy conversion on the rehearsal copy: 22/22 complete; repeat preview
  proposes zero changes.
- Exact pending outcomes: all 22 succeeded as session/Run IDs 39–60; zero
  copied captures remain pending.
- Watcher: stopped pending final handoff review and a separate startup decision.
- Production processor: stopped and disabled.
- Current Python authority: repository `.venv`; the optional owner environment
  is not a verification dependency.

The 22 original legacy directories are inaccessible to the current task
because the old watcher created staging directories with Python
`tempfile.mkdtemp()`. A
controlled Windows probe reproduced a protected owner-only DACL, and rename
preserved it. This was a code defect, not an owner instruction and not a failed
runtime relocation. Future captures now use an ordinary collision-resistant
directory that inherits the pending root's ACL. Nate recovered their contents
by copying them into the ordinary, inheriting rehearsal directory. The
originals remain retained and unchanged; no broad ACL rewrite is needed for
the rehearsal.

## Controls required before any processor run

1. Acquire a kernel-held exclusive lease before opening SQLite. The kernel
   handle is authority; a status filename or PID is diagnostic only.
2. Create an append-only JSONL journal under `runtime/processing/` and print its
   path before work starts.
3. Flush and `fsync` a record before and after every session and major stage,
   and emit bounded progress within large loops.
4. Maintain a replaceable `processor-status.json` snapshot for quick operator
   inspection; failure to replace it must not invalidate the append-only log.
5. Record PID, root/database paths, selected IDs, scope switches, input bytes,
   row/cardinality counts, elapsed time, throughput, commit, rollback, and
   exception context where available.
6. Generate the exact plan with a strict SQLite `mode=ro`, `query_only`
   connection before any writable command.
7. Require an explicit capture/session selection or an explicit positive bound.
   An omitted bound must never silently mean every pending capture plus every
   historical session.
8. Keep pending capture finalization and historical derived-state backfill as
   separate operator actions.
9. Never connect watcher exit handling to parsing or backfill.

## Completed diagnostic: historical-session stall

The first blind rehearsal was stopped. After stage telemetry was added, a fresh
byte-verified database/archive copy localized the stall to:

```sql
DELETE FROM source_blocks WHERE session_id = ?
```

`classification_assignments.source_block_pk` and
`issue_occurrences.source_block_pk` are foreign keys to
`source_blocks(source_block_pk)`. Neither child table had an index beginning
with that column. SQLite's foreign-key check therefore planned a full child
index scan for every parent row deleted: about 1.53 million classification rows
and 1.50 million occurrence rows scanned repeatedly while replacing a
100,000-block session.

Storage schema v3 adds:

- `idx_classification_assignments_source_block(source_block_pk)`; and
- `idx_issue_occurrences_source_block(source_block_pk)`.

Migration validation now treats either missing index as schema work, and index
creation occurs after any older compact-storage table conversion. The real
query plans changed from `SCAN` to `SEARCH` using those exact indexes.

## Completed benchmark: Run ID 14

Rehearsal root:
`.ck3chronicle/wip/benchmarks/ingestion/session-14-current-code-20260908-03/`

Scope was frozen by a read-only plan to Run ID 14 only. Pending finalization,
filesystem reconciliation, other sessions, and report generation were disabled.
The copied database and four archived files matched production by length and
SHA-256 before execution.

Result: 100,000 source blocks became 101,037 classified/projected occurrences
and 381 issue clusters. The pipeline completed in 159.663 seconds with no
failure. Post-run `quick_check=ok` and `foreign_key_check` returned no rows.
This capped CK3 log is also the producer-defined maximum-size ingestion case.

| Stage | Duration |
|---|---:|
| Classification preparation | 115.783 s |
| Semantic-projection preparation | 23.352 s |
| Complete parse | 11.756 s |
| Parse block loop | 10.148 s |
| Projection transaction | 4.404 s |
| Projection SQL write loop | 2.456 s |
| Classification transaction | 1.651 s |
| Database open and storage-v3 migration | 1.145 s |
| Formerly stalled source-block delete | 0.217 s |

The draft report's projection-write hypothesis is falsified for this workload:
the 101,037-item write loop used 1.140 seconds for cluster statements and 1.229
seconds for occurrence statements. Do not build a bulk-write redesign from
that hypothesis. Classification preparation is the measured dominant cost;
optimization there is a separate decision after reliability recovery and an
owner-approved performance threshold.

The durable journal is:
`.ck3chronicle/wip/benchmarks/ingestion/session-14-current-code-20260908-03/processing/events-20260908T054429.031330Z-3832.jsonl`.

## Why historical sessions were selected

The old wide pipeline revisited earlier data because parser lineage changed,
not because a storage migration intrinsically required every log to be parsed
again. Commit `1f4d8c2` advanced parser contract `1.0.0` to `1.0.1`, made a
contract mismatch force replacement, and left the wide command iterating every
session. Commit `05afbe2` advanced the contract to current version `1.0.2` and
added semantic projection to that pipeline. Production contains 15 sessions at
`1.0.0` and 23 at `1.0.2`, so the first 15 were legitimately selected for
current parser output. Missing foreign-key support indexes then made their
replacement deletion appear hung.

## Completed work package 1: expose safe operator scopes

`process-pending --capture NAME` and `backfill-session --session ID` are now
separate. Each command:

1. requires one exact direct-child capture name or session ID;
2. uses a strict read-only SQLite plan before acquiring the processor lease;
3. makes plan-only the default and requires `--execute` for mutation;
4. records explicit pending/historical bounds and names untouched scopes;
5. verifies the selected pending files or finalized archive against its
   manifest and database projection;
6. prints and durably records the processing journal; and
7. preserves an idempotent derived-state skip only when parser, model,
   classifier, projection catalog, and projection contract lineage is current.

The former internal wide defaults now reject pending finalization or archive
reconciliation before mutation. Eleven current requirement-derived tests cover
these scope controls, the database indexes, journal visibility/I/O accounting,
processor exclusivity, and watcher behavior.

## Completed work package 2: readable copy and all 22 captures

The copy, metadata conversion, and all 22 exact-item runs are complete.
The production database and all 22 original pending directories remain
unchanged. The rehearsal root began with a byte-identical production database;
only the rehearsal copy has since migrated to storage schema v6 and gained
session/Run IDs 39–60.

| Capture | Result | Blocks | Occurrences | Clusters | Wall time |
|---|---:|---:|---:|---:|---:|
| `20260903T045043.873506Z-dxpfzis7` | normal, session/Run 39 | 51 | 51 | 1 | 5.99 s |
| `20260903T050025.994078Z-olz9p33v` | crash, session/Run 40 | 1,512 | 2,121 | 90 | 24.55 s |
| `20260902T164429.635723Z-l9gtkwz1` | crash, session/Run 41 | 1,541 | 2,149 | 97 | 5.78 s |

Session 40 localized 11.996 seconds of projection preparation to 452 semantic
units originating in the same 21,287-character persistent-reader source block.
The old loop repeated complete-block normalization and six locator scans for
every unit. Reusing immutable block evidence improved the real 2,121-item
preparation benchmark from 11.712 seconds to 0.489 seconds (23.97x), with zero
semantic mismatches. A corrected complete rebuild retained the same 90 issues,
2,121 occurrences, and fingerprint
`7272e3e0a800408bea7a5acae8b9dd5a92742dd92e835d2ef758754a29bc4c1f`.

The rebuild exposed the same foreign-key indexing class on
`issues.semantic_projection_run_id` and
`issue_occurrences.semantic_projection_run_id`. Storage schema v4 adds both
leading-column indexes. Rehearsal projection deletion improved from 1.618
seconds to 32.934 milliseconds, with both query plans changing to indexed
`SEARCH`.

Later detailed timing isolated two projection post-validation joins. Storage
schema v5 adds the projection/signature access path needed for cluster
reconciliation; storage v6 adds the complementary projection/source-block path
so that index cannot make block reconciliation regress. On session 52, complete
post-validation then took 119.156 milliseconds: 22.255 milliseconds for block
reconciliation and 2.083 milliseconds for cluster reconciliation.

Classification preparation was also repeating deterministic work for identical
stored raw blocks. The classifier now reuses immutable results only when both
`raw_block_pk` and source family match. A direct real-data comparison of 22,645
ordered blocks and 23,254 semantic units was exactly equal to uncached output,
with fingerprint
`0e5a15b64d2f5be1e41b3a2a56cd123edd70f576d8a5dcb3370899b8ef7fbdd5`;
preparation improved from 23.411 seconds to 0.641 seconds (36.52x).

Session 41 then exercised both changes end to end. Its journal measured 0.866
seconds for parse, 1.151 seconds for classification, and 1.670 seconds for
semantic projection. The newly instrumented journal accounting reported 140
events and 1.074 seconds of durability cost: 0.283 seconds in append/fsync and
0.786 seconds in atomic status replacement/fsync. Post-run `quick_check=ok` and
`foreign_key_check` was empty.

The three journals are respectively:

- `processing/events-20260908T062620.570029Z-23876.jsonl`;
- `processing/events-20260908T062905.635714Z-25164.jsonl`; and
- `processing/events-20260908T064751.685167Z-22472.jsonl`

under the rehearsal root.

The completed set comprises 15 normal and seven crash runs, 702,113 source
blocks, 720,090 semantic occurrences, and 16,271 issue clusters. Three captures
reached the 100,000-entry CK3 cap. Final verification rehashed 22 archives and
139 files (728,780,581 bytes) and reconciled every selected archive, capture
run metadata, parser lineage, classification run, projection run, source count,
occurrence count, and cluster count. It found zero duplicate `error.log`
hashes. `quick_check=ok` in 2.202 seconds and `foreign_key_check` returned zero
rows in 1.936 seconds.

Checkpoint: all 22 copied captures have an explicit success/failure outcome,
no lifecycle/crash fact is lost, and no matching `error.log` hash creates a
second Run ID or reaches parsing.

## Completed work package 3: interruption and recovery proof

Session 52 was intentionally interrupted after the v5 query plan stopped
advancing inside `projection_postvalidate_blocks`. Before recovery, the exact
882,556,928-byte database and 5,033,680-byte hot rollback journal were copied
to `backups/interrupted-session52-v5-plan-20260908-01/`; their SHA-256 values
are `7C7F37BC9AAF74E0F4A2356F774CB17BE4B80F0CAA0440DCA46C199B29AE2247`
and `1467B9217FDF5AFD69783428E6A126652B1B716D665FFCF2F0B8BE554BC631AA`.

Ordinary SQLite open recovered the database and removed the journal. Session
52 retained its complete finalized/parsed/classified prior state and had zero
projection lineage; the interrupted replacement exposed no partial projection.
The OS processor lease was immediately acquirable. An exact read-only
`backfill-session --session 52` plan reverified the six-file archive, skipped
current parse/classification, and selected only semantic projection. After the
v6 index correction, that retry succeeded in 7.682 seconds with no pending
capture or unrelated historical session in scope.

Checkpoint: interruption cannot expose a partially accepted session and never
requires production evidence for diagnosis.

## Remaining work package 4: iterative production resumption

Production requires a separate owner-approved execution decision after the
preceding checkpoints.

1. Create and verify a fresh production backup; record database hash, size,
   integrity, and inventory.
2. Run the read-only plan for one exact pending capture or one exact historical
   session—never both.
3. Execute that one item, inspect the journal, and run integrity and
   reconciliation checks.
4. Compare the resulting counts/lineage to the disposable rehearsal.
5. Review before selecting the next item. Permit a larger bounded batch only
   after repeated stable one-item runs.
6. Do not claim or optimize for 100% full/L2 classification; durable L1-only,
   provisional, and unknown outcomes are valid review work.

## Separate decisions

- Starting the capture-only watcher is separate from processor recovery.
- Automatic watcher-to-processor triggering remains out of scope.
- Git is not a backup for `.ck3chronicle/wip/`; runtime backup/retention needs
  its own supported procedure.
- The reboot source and current documents must be reviewed, committed, and
  pushed from the canonical repository before the remote reflects this state.
