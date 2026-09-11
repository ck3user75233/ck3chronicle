# ck3chronicle

ck3chronicle is a standalone, local CK3 run-intelligence product. Its first
named capability is **Trusted Run**: observe one CK3 start-to-exit lifecycle,
protect the live `error.log`, associate root `exception.txt` only when a new
crash folder belongs to that lifecycle, process the run into SQLite, and report
from stored records.

## Current development boundary

- Operational roots come from the repository-local ignored `config.toml`.
- The watcher is lifecycle-triggered. Existing files, directory changes,
  watcher startup, retry, and reconciliation do not create sessions.
- Capture is copy-first. Hashing, SQLite work, parsing, classification, and
  reporting happen after pending publication.
- Trusted Run captures only live-root `error.log`. A new associated crash
  folder may add only its root `exception.txt`; crash-folder principal logs are
  ignored.
- Each successful session stores the `error.log` SHA-256 in `session_files`.
  Every ingest route rejects a matching hash before registration or parsing,
  with no override.
- CK3 and mod sources are read-only. Runtime evidence and the SQLite database
  stay outside Git.

## Local setup

Copy `config.example.toml` to ignored `config.toml` and set every path
explicitly. Codex and other repository automation must use the project-local
`.venv`; routine compilation, import, CLI, and test checks belong to the agent
performing the work and must not be delegated to the owner:

```powershell
Set-Location 'C:\Users\nateb\Documents\ck3chronicle'
$python = (Resolve-Path -LiteralPath '.\.venv\Scripts\python.exe').Path
& $python -B -m unittest discover -s tests -v
& $python -I -B -c "import ck3chronicle; import ck3chronicle.cli"
& $python -I -B -m pip check
```

On Nate's current machine, `.venv-owner-20260829` is an optional interpreter
for an interactive shell. Its base interpreter is outside the Codex sandbox's
executable boundary, so agents must use `.venv` instead of treating that
optional environment as the only Python path or reporting routine checks as
blocked.

The normal application commands are:

```powershell
& $python -B -m ck3chronicle.cli doctor
& $python -B -m ck3chronicle.cli watch
& $python -B -m ck3chronicle.cli latest --json
```

Read-only commands never migrate or vacuum the database. If the configured
database predates the working-tree schema, they fail loudly until an explicit
writable migration is separately approved and run.

`process-pending` is currently an exact-one-capture recovery/development
command, not a background watcher action. It prints a read-only plan and does
nothing unless `--execute` is supplied. `backfill-session` is the separate
exact-one-session historical-derived-state command with the same plan-first
contract. Both remain disabled against the production runtime until the
fresh-backup/review steps in `docs/CURRENT_HANDOFF.md` are complete and
production execution is separately approved. The disposable fault-isolation
and complete 22-item rehearsal have already passed.

Do not run `capture`, `watch --once`, or `process-pending` merely as a smoke
test against the live configured roots; those commands intentionally mutate
runtime evidence or the database.

## Project authority

- [Owner product intent](docs/OWNER_PRODUCT_INTENT.md)
- [Trusted Run specification](docs/TRUSTED_RUN_SPEC.md)
- [Architecture and data lineage](docs/ARCHITECTURE_AND_DATA_LINEAGE.md)
- [Named milestone plan](docs/PROJECT_PLAN.md)
- [Requirements and verification](docs/REQUIREMENTS_AND_TESTING.md)
- [Ingestion operational recovery plan](docs/INGESTION_OPERATIONAL_RECOVERY_PLAN.md)
- [Current status](docs/PROJECT_STATUS.md)
- [Current handoff](docs/CURRENT_HANDOFF.md)

The `tests/` tree contains only checks derived from current owner-directed
requirements. Historical test expectations never create product scope.
