# ck3chronicle

ck3chronicle is a standalone, local CK3 run-intelligence product for modders.
It protects the useful output of completed runs, turns `error.log` into durable
and reviewable diagnostic history, and will support comparison, bounded source
context, and cautious action guidance.

The first product milestone is **Trusted Run**: observe one CK3 start-to-exit
lifecycle, protect its live `error.log`, process it into SQLite, preserve
unresolved evidence for review, and generate reports from stored records.

## Target flow

1. The watcher observes the configured CK3 process and copies the live
   `error.log` only after that process exits.
2. Deferred processing validates and deduplicates the protected copy, recognizes
   log emissions, and classifies recovered diagnostics against approved error
   contracts.
3. Approved diagnostics become compact SQLite records. Unresolved,
   provisional, and low-confidence emissions go to one native review shard for
   the resulting Run ID.
4. Reports query SQLite and do not depend on the retained source log.

CK3 and mod sources are read-only. A newly associated crash folder may provide
only its root `exception.txt`; its copies of principal logs are ignored.

The required fast-follow after Trusted Run captures the same Run's `debug.log`
and extracts its effective playset—active DLCs and mods, mount/load order, and
paths needed to correlate diagnostics with the files that were active.

## Current development state

Trusted Run is partly implemented but not accepted. Classification-pipeline
recovery is the active exercise. Consult
[`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) for current gaps,
operational restrictions, and the exact continuation point.

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
& $python -B -m ck3chronicle.cli doctor
& $python -B -m ck3chronicle.cli latest --json
```

Before starting the watcher, capturing evidence, processing pending captures,
or writing to the production database, read the current status and handoff.
Never use a runtime-mutating command merely as a smoke test.

## Project documentation

- [Owner product intent](docs/OWNER_PRODUCT_INTENT.md) — governing product
  purpose, boundaries, vocabulary, and trust rules.
- [Architecture and data lineage](docs/ARCHITECTURE_AND_DATA_LINEAGE.md) — target
  components, data ownership, and transaction boundaries.
- [Project plan](docs/PROJECT_PLAN.md) — milestones and dependencies; explicit
  delivery-order clarification remains pending.
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
