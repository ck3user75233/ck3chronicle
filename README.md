# ck3chronicle

ck3chronicle is a standalone, local CK3 run-intelligence product for modders.
It protects the useful output of completed runs, turns `error.log` into durable
and reviewable diagnostic history, and provides libraries for comparison and
bounded source context. Cautious action guidance remains planned.

The first product milestone is **Trusted Run**: observe one CK3 start-to-exit
lifecycle, protect its live `error.log`, process it into SQLite, preserve
unresolved evidence for review, and generate reports from stored records.

## Target flow

1. The watcher observes the configured CK3 process and copies the live
   `error.log` and full `debug.log` after that process exits. It extracts the
   ordered active playset and writes `playset.json` with both content hashes.
2. Deferred processing validates and deduplicates the protected copy, recognizes
   log emissions, and classifies recovered diagnostics against approved error
   contracts.
3. Selected template and provisional assignments become compact SQLite records,
   distinguished by match status. Unassigned/unresolved evidence goes to one
   native review shard for the resulting Run ID.
4. Reports query SQLite and do not depend on the retained source log.

CK3 and mod sources are read-only. A newly associated crash folder may provide
only its root `exception.txt`; its copies of principal logs are ignored.

The watcher playset producer is delivered. Its template includes the base game,
DLCs and mods in emitted mount order, with descriptor names and paths. Run-owned
SQL persistence and review-manifest ingestion are implemented by Task 07.
See the [watcher handoff](docs/WATCHER_ACTIVE_PLAYSET_HANDOFF.md) for the format,
verified example, failure behavior and pipeline receiving requirements.

## Current development state

Task 07 ingestion, per-Run lineage, ordered playsets and raw retention are
implemented. [Task 07D's current handoff](docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
documents the dedicated shared database handler used by watcher, manual CLI and
application clients. Windows named pipes connect callers to one host and one
SQLite worker per exact database file. Hashing/parsing/classification stay outside
that worker. Request states are `ENQUEUED`, `COMPLETED` and `NOT_COMPLETED`;
duplicates return the existing Run ID as non-completion, and contention waits.

[Task 07E](docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md) adds shared rotating JSONL logs,
request-ID correlation through watcher/preparation/database execution, traceback
evidence and bootstrap diagnostics. Its handoff records the owner-authorized
September 30 activation and includes operator queries. Future runtime changes use
the shared logging owner and run `tools/check_runtime_logging.py`.

SQL schema and native-review manifest are version **3**; playset format is **1**.
Missing playsets are unavailable; invalid supplied playsets warn and permit the
valid error log to proceed. Daily watcher maintenance preserves configurable
30-elapsed-day raw expiry. Selection and the existing Run writer are unchanged.
Removed providers and generation replay remain excluded.

Commands are `ingest`, `watch`, `capture`, `doctor` and `observe-logging`;
`watch --once` retains manual error-only copying. The [earlier watcher activation](docs/WATCHER_LIVE_ACTIVATION_HANDOFF.md)
and [September 30 handler/logging activation](docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md)
are historical records, not evidence of current live status.

[Task 08A.1](docs/TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md) delivered reusable stored
diagnostic queries and history analysis. [Task 08A.2](docs/TASK08A_2_SOURCE_SEARCH_HANDOFF.md)
delivered playset source search and context integrated with those queries.
[Task 08B reports and CLI](docs/TASK08B_PROMPT.md) remain outstanding, including
the assigned correction to apply known source-path constraints before traversal.

Delivery does not establish complete verification. The earlier genuine-data checks
covered one eligible Run; the [later multi-Run exercise](docs/TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md)
found 14 stored Runs without the required source timestamp, leaving chronological
multi-Run analysis unverified. Cases without genuine evidence also remain
unverified. Explicit Run-result replacement and full observed start-to-exit
Trusted Run acceptance remain outstanding. Consult
[project status](docs/PROJECT_STATUS.md) before operational work.

The current implementation still reads the ignored repository-root
`config.toml`, created from `config.example.toml`. The approved target is an
exact `--config <path>` or one fixed LocalAppData `ck3chronicle/paths.toml`
bootstrap with no path discovery. Until that transition is implemented, do not
mistake the current bootstrap for the target contract.

Use the repository `.venv`. Tested PowerShell commands and sandbox guidance are
in [`docs/DEVELOPMENT_ENVIRONMENT.md`](docs/DEVELOPMENT_ENVIRONMENT.md).

Read-only development commands include:

```powershell
$python = (Resolve-Path -LiteralPath '.\.venv\Scripts\python.exe').Path
& $python -I -B -m ck3chronicle.cli --help
& $python -I -B -m ck3chronicle.cli watch --help
& $python -I -B -m ck3chronicle.cli ingest --help
```

Before starting the watcher, capturing evidence, processing pending captures,
or writing to the production database, read the current status and handoff.
Never use a runtime-mutating command merely as a smoke test.

## Project documentation

- [Current Task 07D database and ingestion handoff](docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
  — APIs, handler lifetime, three states, watcher integration, schema/review 3,
  playset 1, daily maintenance and verification.
- [Historical Task 07 evidence](docs/TASK07_INGESTION_AND_RETENTION_HANDOFF.md)
  — original native verification and limitations.

- [Task 06 implementation handoff](docs/TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md)
  — storage/review APIs, physical generation/shard layout, completion and cleanup,
  historical native evidence and predecessor examples; use the current 07D
  handoff for runtime APIs.

- [Approved Error Contract](docs/ERROR_CONTRACT_SPECIFICATION.md) — owner-approved
  assignment, identity, rendering, source/emitter and lineage rules.
- [Task 04 handoff](docs/TASK04_ERROR_CONTRACT_HANDOFF.md) and
  [revised Task 05 prompt](docs/05_ERROR_CONTRACT_IMPLEMENTATION.md) — historical
  predecessor scope. [Task 05 implementation handoff](docs/TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md)
  records the delivered shared matcher integration, selected-only binding,
  serializable contracts, native verification and installed-resource proof.
- [Shared matcher delivery](docs/LEARNER_PARSER_PIPELINE_HANDOFF.md),
  [API](docs/SHARED_MATCHER_API.md) and
  [independent verification](docs/SHARED_MATCHER_PIPELINE_VERIFICATION.md) —
  immutable package delivery and predecessor verification. Task 06 integrated
  and selected v45; the later Task 07 handoffs record runtime integration.
- [Unmatched learner investigation](docs/LEARNER_UNMATCHED_REVIEW_ROOT_CAUSE_RESULTS.md)
  and [cumulative learning experiment](docs/LEARNER_ALL_LOGS_V42_RESULTS.md) —
  native case evidence, same-version additive learning and isolated candidates;
  neither changes the selected runtime package. The
  [formal Pipeline Team reply](docs/LEARNER_TASK06_UNMATCHED_REVIEW_REPLY.md)
  records the original 122-case investigation with complete candidate assignments,
  before the subsequent v45 integration.
- [Learner v45 release delivery](docs/LEARNER_RELEASE_V45_RESULTS.md) —
  the 73-log replacement build, native model evolution and schema-5 / API-v2
  package assessment preceding the [completed Task 06 integration](docs/TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md).
- [Owner product intent](docs/OWNER_PRODUCT_INTENT.md) — governing product
  purpose, boundaries, vocabulary, and trust rules.
- [Architecture and data lineage](docs/ARCHITECTURE_AND_DATA_LINEAGE.md) — target
  components, data ownership, and transaction boundaries.
- [Project plan](docs/PROJECT_PLAN.md) — milestones, dependencies and current sequencing.
- [Project status](docs/PROJECT_STATUS.md) — current implementation truth.
- [Current handoff](docs/CURRENT_HANDOFF.md) — live uncommitted work and the
  continuation point.
- [Banned ideas](docs/BANNED_IDEAS.md) — explicitly rejected designs.

### Detailed policies pending reconciliation

The following detailed specifications and policies retain useful requirements,
but their retention, projection, migration, compatibility, and historical-
reprocessing sections require reconciliation during classification recovery.
Where they conflict, current owner intent, architecture, and banned-design
decisions govern.

- [Trusted Run specification](docs/TRUSTED_RUN_SPEC.md) — detailed first-
  milestone requirements; it requires reconciliation after classification
  recovery before serving as the next implementation plan.
- [Requirements and verification](docs/REQUIREMENTS_AND_TESTING.md)
- [Data compatibility and operations](docs/DATA_COMPATIBILITY_AND_OPERATIONS.md)
- [Model quality and promotion](docs/MODEL_QUALITY_AND_PROMOTION.md)
- [Release readiness](docs/RELEASE_READINESS.md)

Runtime logs, databases, review shards, corpora, workbooks, and generated
evaluation results remain outside Git. Tests derive from current owner-directed
requirements; historical tests do not create product scope.
