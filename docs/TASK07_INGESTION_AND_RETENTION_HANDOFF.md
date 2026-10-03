# Task 07 ingestion and retention — historical evidence

This records the original September 28 delivery. Runnable APIs, exact database
paths, versions, optional-playset policy and daily maintenance now live in the
[current Task 07D handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md). Obsolete directory/Generation examples and unresolved
receiving proposals have been removed. Preserve the original native evidence below
as historical results, not verification of the current handler/live installation.

## Historical verification, changed paths and limitations

Native requirement checks live in `tests/test_ingestion_retention_requirements.py`.
They require `CK3_TASK07_EVIDENCE` naming a JSON object with actual retained input
paths and a disposable output root. They skip rather than invent fixtures when
those inputs are unavailable. This task's input selection is in ignored
`.codex-tmp/task07/evidence.json`; no diagnostic messages or records are fabricated.

```powershell
$env:CK3_TASK07_EVIDENCE = (Resolve-Path .codex-tmp/task07/evidence.json).Path
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_ingestion_retention_requirements.py -v
```

The end-to-end campaign passed in 158.742 seconds; focused input/coordination checks
passed in 1.535 seconds. Evidence: ignored
`.codex-tmp/task07/6b60a845a9ed4733b62c8e37342e1908/results.json`, with its disposable
SQLite databases and review shards. These are measurements, not time budgets or
acceptance thresholds. The full campaign includes a second native classification
for independent source/render comparison and is not a single-call timing.

| Complete input SHA-256 prefix | Package | SQL records | Eligible occurrences | Review units | Playset |
|---|---|---:|---:|---:|---|
| `42d27e68` | `68f1ae5db205ab46afef9c4d` | 2,475 | 4,182 | 0 | 133 members |
| `01aeb0f1` | `44a0401b8adf0a2953d26705` | 970 | 2,151 | 0 | unavailable |
| `f5ca3538` | `68f1ae5db205ab46afef9c4d` | 1,661 | 22,660 | 1 | unavailable |

Verified API ingestion, CLI new/duplicate submissions, duplicate submission under
the other package without parsing/replacement, one protected manual copy, actual
per-Run lineage, source-region equality for stored renderings, every emission's
record/review accounting, exact native review bytes, ordered SQL/manifest playset
agreement and SQL-only rendering after raw expiry. All three Runs share one database.
The first input is the watcher team's isolated genuine pair; no live watcher was used.

Verified a post-publication injected IO failure rolls SQL back, preserves raw input,
and leaves cleanup to the existing guarded API. An actual copied schema-1 database
was refused with a reset message and byte-identical database preservation. Retention
checks covered preview, age boundary, configurable duration, busy capture exclusion,
real cross-process CLI lock contention, injected unlink failure, removal of unprocessed
copies and preservation of staging, metadata, playset JSON, SQL and review files.
Missing capture time was skipped. A simulated disagreement between the pre-parse hash
and an intact genuine parsed file failed before SQL. Pair mismatch validation used
the hash of another intact genuine log. No log bytes were mutated for these checks.

Imports and `pip check` pass. The existing release-selection suite reports nine passes
and one environment-gated native check skipped; Task 07's own campaign exercised both
packages through real contract preparation and storage. Source schema-1 and schema-2
storage are never opened through production paths for these checks.

Evidence limits: the selected logs contain no unresolved recovery or continuation
groups, and the captured playset does not establish every possible repeat/null field
combination. No synthetic cases were substituted. Malformed completed JSON disposition
is not accepted yet. Windows process-lock coordination was exercised; POSIX locking,
power-loss durability, simultaneous SQLite writers, an installed wheel build and live
watcher activation were not exercised by Task 07. Source CLI and isolated (`-I`)
environment imports were checked. The existing repository's OS/power-loss caveats remain.

Changed owning paths: `pipeline/schema.py`, `repository.py`, `review.py`; new
`pipeline/ingestion.py`, `playsets.py`, `capture_access.py`, `retention.py`; only the
new ingest handler/parser arguments in `cli.py`; the native requirement check above;
this handoff, README, status, plan, execution order, current handoff and scope ledger.
The large pre-existing dirty tree, including watcher/harvester/learner work, is preserved.

The completed [Script location-stack findings](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_RESULTS.md)
remain context: no demonstrated stack-length misses or lost location fields in the
surveyed corpus; retain the current representation. Historical release gaps are
separate learner-team work only if commissioned. Raw retention never prunes releases.

At the original delivery, malformed/mismatched-playset disposition and watcher
activation remained outstanding. Both were subsequently resolved in the linked
September 29 handoff. Task 07D subsequently delivered coordination and caller repairs; Run-result
replacement, Task 08 reports and Trusted Run acceptance remain separate.
