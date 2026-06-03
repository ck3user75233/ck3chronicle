# Phase 0 — Launch Packet

> **Phase:** 0 — Evidence Preservation and Session Registry  
> **Subagent shape:** implementer → reviewer (single implementer; reviewer mandatory)  
> **Source contract:** [01_implementation_plan.md §7 / Phase 0](../01_implementation_plan.md)  
> **Charter:** [00_project_charter.md](../00_project_charter.md)  
> **Branch:** `feature/ck3chronicle` (already created at launch commit `f0519b7`)  
> **Created:** 2026-06-03

This packet is what the implementer subagent receives. The reviewer subagent
receives this packet + the validation checklist in §3 of the implementation
plan + the boundary rules in charter §2.2 and §3.3.

---

## 1. Mission (in one sentence)

Stand up the `ck3chronicle` package skeleton, the `config.py` path registry,
and the harvester+ingest pipeline that snapshots a CK3 evidence bundle (logs
+ optional crash folder) into durable local storage and records session
metadata in SQLite — with `ingest`, `sessions`, and `doctor` CLI subcommands.

## 2. Hard Constraints (re-read before writing code)

- All product code under `root:repo/ck3chronicle/src/ck3chronicle/`.
  No exceptions.
- Tests under `root:repo/ck3chronicle/tests/`.
- **No live code may live in or import from
  `root:repo/ck3chronicle/error analysis refactor/`** (reference material
  only — plan §5.3.1).
- **No live code may live in or import from
  `root:repo/ck3chronicle/ck3chronicle_proto/`** (reference material only).
- All filesystem paths come from `ck3chronicle.config`. **No** inline
  `Path.home() / ...`, `os.environ[...]`, OS-default discovery, or
  hardcoded CK3 / Steam / launcher / mod / log paths outside `config.py`
  (plan §3 checklist + §4.3).
- Stdlib only. Permitted modules: `argparse, sqlite3, pathlib, dataclasses,
  json, re, hashlib, difflib, datetime, shutil, logging, tomllib` (Python
  3.11+ for `tomllib`). **No** click, rich, pydantic, requests, etc. unless
  explicitly approved.
- Python 3.11+ required.
- No log content is parsed yet. Parsing is Phase 1.
- No mod list / playset logic. That is Phase 3.
- No `ck3raven`, `mcp`, `ck3lens` imports anywhere.

## 3. Target Files (create / scaffold)

```
root:repo/ck3chronicle/
  pyproject.toml                                       (new)
  README.md                                            (new, stub)
  src/
    ck3chronicle/
      __init__.py                                      (new — version)
      cli.py                                           (new — argparse skeleton)
      config.py                                        (new — ROOT_* registry)
      doctor.py                                        (new)
      harvester.py                                     (new)
      ingest.py                                        (new)
      db/
        __init__.py                                    (new)
        schema.py                                      (new)
        migrations.py                                  (new)
        repository.py                                  (new)
  tests/
    __init__.py                                        (new)
    conftest.py                                        (new — tmp paths)
    test_cli.py                                        (new)
    test_config.py                                     (new)
    test_db.py                                         (new)
    test_doctor.py                                     (new)
    test_harvester.py                                  (new)
    test_ingest.py                                     (new)
    fixtures/
      logs/
        minimal/
          error.log                                    (new — see §7)
          game.log                                     (new — see §7)
        with_crash/
          error.log                                    (new)
          game.log                                     (new)
          crash/
            dump_metadata.txt                          (new)
```

Do not touch any file outside this list.

## 4. `pyproject.toml` Shape (minimal)

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "ck3chronicle"
version = "0.0.1"
description = "Preserve and triage Crusader Kings III runtime logs and crash evidence."
readme = "README.md"
requires-python = ">=3.11"
license = { text = "TBD" }
authors = [{ name = "ck3chronicle authors" }]
keywords = ["ck3", "crusader-kings", "modding", "logs", "diagnostics"]
classifiers = [
  "Development Status :: 3 - Alpha",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Operating System :: OS Independent",
]
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=7"]

[project.scripts]
ck3chronicle = "ck3chronicle.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## 5. `ck3chronicle.config` Spec

`config.py` is the **single source of truth** for filesystem locations.
All other modules import these names; no other module performs path
discovery or reads `config.toml`.

### Required public names

| Name | Type | Notes |
|---|---|---|
| `ROOT_GAME` | `Path` | CK3 install dir |
| `ROOT_STEAM` | `Path` | Workshop content (`.../workshop/content/1158310`) |
| `ROOT_LOCAL_MODS` | `Path` | Paradox local mods folder |
| `ROOT_LOGS` | `Path` | CK3 runtime logs folder |
| `ROOT_WIP` | `Path` | User scratch / dev artifacts root |
| `ROOT_CK3CHRONICLE` | `Path` | ck3chronicle's own data root |
| `CONFIG_FILE_PATH` | `Path` | Resolved `config.toml` location |
| `load_config(path: Path \| None = None) -> dict` | function | Loads (and creates with defaults if absent) the user config file |
| `default_config_path() -> Path` | function | Computes the OS-default `config.toml` location |
| `default_root(name: str) -> Path` | function | Computes the OS-default for a single ROOT name |

### OS-default discovery (Windows-first; Linux/Mac stubs acceptable)

| Constant | Windows default | Linux/Mac default |
|---|---|---|
| `ROOT_GAME` | `C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game` | `~/.steam/steam/steamapps/common/Crusader Kings III/game` |
| `ROOT_STEAM` | `C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310` | `~/.steam/steam/steamapps/workshop/content/1158310` |
| `ROOT_LOCAL_MODS` | `%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings III\mod` | `~/.local/share/Paradox Interactive/Crusader Kings III/mod` |
| `ROOT_LOGS` | `%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings III\logs` | `~/.local/share/Paradox Interactive/Crusader Kings III/logs` |
| `ROOT_CK3CHRONICLE` | `%LOCALAPPDATA%\ck3chronicle` | `~/.local/share/ck3chronicle` |
| `ROOT_WIP` | `<ROOT_CK3CHRONICLE>/wip` | `<ROOT_CK3CHRONICLE>/wip` |
| `CONFIG_FILE_PATH` | `<ROOT_CK3CHRONICLE>/config.toml` | `<ROOT_CK3CHRONICLE>/config.toml` |

### `config.toml` shape (auto-written if missing)

```toml
# ck3chronicle user configuration
# Edit any path below to override its OS default.
# Leave a value as the empty string "" to fall back to the OS default.

[paths]
root_game        = ""
root_steam       = ""
root_local_mods  = ""
root_logs        = ""
root_wip         = ""
root_ck3chronicle = ""
```

### Test points (mandatory)

- For every `ROOT_*`: unit test for OS-default discovery (mock home/env).
- For every `ROOT_*`: unit test for override via `config.toml`.
- Test that `load_config()` creates the file with defaults when missing.
- Test that `load_config()` is idempotent on an existing file.
- Test that an empty string in `config.toml` falls back to the OS default.

## 6. Harvester + Ingest Spec

### Evidence bundle identity (Phase 0 dedupe semantics — plan)

```python
evidence_bundle_hash = sha256(
    sorted(log_files_by_relpath_with_their_sha256)
    + sorted(crash_artifact_files_by_relpath_with_their_sha256)
)
```

### `harvester.py`

- Function `discover_logs(root: Path) -> list[Path]`:
  read the fixed log list from the plan / config:
  `error.log, game.log, debug.log, database_conflicts.log, setup.log, text.log`.
  Returns only files that exist. No directory walking.
- Function `discover_crash_folder(root: Path) -> Path | None`:
  conservative stub — returns the most recent crash folder under
  `<ROOT_LOGS>/crashes/` if one exists; otherwise `None`. Configurable
  cap on age is not required in Phase 0.
- Function `hash_file(path: Path) -> str`: streaming SHA256.
- Function `snapshot(bundle: EvidenceBundle, dest_root: Path) -> SnapshotResult`:
  copies each file to `<dest_root>/sessions/<evidence_bundle_hash>/...`
  preserving relative paths. Idempotent — re-snapshotting the same bundle
  to the same dest is a no-op.

### `ingest.py`

- Function `ingest(logs_root: Path | None = None, force: bool = False) -> IngestResult`:
  1. Resolve sources via `config` (defaults to `ROOT_LOGS`).
  2. Build the evidence bundle.
  3. Compute `evidence_bundle_hash`.
  4. Check DB for an existing session with that hash.
     - If found and not `force`: return existing session ID; mark
       `IngestResult.was_duplicate = True`.
     - If `force`: create a new session row with a `forced_duplicate_of`
       column pointing at the original.
  5. Snapshot files to durable storage under `ROOT_CK3CHRONICLE/sessions/`.
  6. Write session row(s) and per-file rows.

### `db/schema.py`

Minimum tables (others added in later phases):

```sql
CREATE TABLE sessions (
    session_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    evidence_bundle_hash TEXT NOT NULL UNIQUE,
    created_at           TEXT NOT NULL,           -- ISO 8601 UTC
    log_count            INTEGER NOT NULL,
    crash_present        INTEGER NOT NULL,       -- 0/1
    total_bytes          INTEGER NOT NULL,
    forced_duplicate_of  INTEGER REFERENCES sessions(session_id)
);

CREATE TABLE session_files (
    session_file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL REFERENCES sessions(session_id),
    rel_path        TEXT NOT NULL,
    sha256          TEXT NOT NULL,
    bytes           INTEGER NOT NULL,
    kind            TEXT NOT NULL                -- 'log' | 'crash_artifact'
);

CREATE TABLE schema_versions (
    component   TEXT PRIMARY KEY,
    version     INTEGER NOT NULL,
    migrated_at TEXT NOT NULL
);
```

`schema_versions` is the only thing `migrations.py` needs to track for now;
real migrations land when later phases extend the schema.

### `db/repository.py`

A thin function-style module (no ORM) wrapping the SQL above:
`open_db(path: Path)`, `get_session_by_hash(...)`, `create_session(...)`,
`add_session_file(...)`, `list_sessions(...)`.

## 7. Test Fixtures (synthetic — do NOT use real logs)

### `tests/fixtures/logs/minimal/`

`error.log` (5–10 lines, multiple categories, no real names):

```
[14:01:02] [data_loader.cpp:511]: Trait 'made_up_trait_a' references unknown trait 'missing_trait_b' at common/traits/00_synth.txt line 12
[14:01:02] [data_loader.cpp:511]: Variable not defined: 'synth_var_x' in common/scripted_effects/00_synth.txt
[14:01:03] [localization.cpp:121]: Missing localization key 'synth_loc_key_001' in 00_synth_l_english.yml
[14:01:03] [localization.cpp:121]: Missing localization key 'synth_loc_key_002' in 00_synth_l_english.yml
[14:01:03] [localization.cpp:121]: Missing localization key 'synth_loc_key_003' in 00_synth_l_english.yml
```

`game.log` (3 lines, harmless):

```
[14:00:50] Game starting
[14:01:00] Mods loaded
[14:05:00] Save autoflushed
```

### `tests/fixtures/logs/with_crash/`

Same files as `minimal/` plus a `crash/` subfolder with a single
`dump_metadata.txt`:

```
crash_type=synthetic
timestamp=2026-06-03T14:05:42Z
note=Synthetic fixture for ck3chronicle Phase 0 test.
```

## 8. CLI Subcommands

```
ck3chronicle ingest [--logs PATH] [--force]
ck3chronicle sessions [--limit N]
ck3chronicle doctor
```

- `ingest`: defaults to `config.ROOT_LOGS`. Prints the resolved
  `evidence_bundle_hash` and the resulting session ID. If a duplicate is
  detected without `--force`, says so explicitly and returns the existing
  session ID.
- `sessions`: prints a table with `session_id`, `created_at`, `log_count`,
  `crash_present`, `total_bytes`.
- `doctor`:
  - Prints Python version, SQLite version, ck3chronicle version.
  - Prints resolved value of every `ROOT_*` and whether each exists.
  - Prints `CONFIG_FILE_PATH`; creates it with defaults if missing and
    reports that it did so.
  - Prints durable-storage status (writable? on the same drive as
    `ROOT_LOGS`?).

## 9. Acceptance Tests (must all pass)

- [ ] `pip install -e .` from `root:repo/ck3chronicle/` succeeds with
      stdlib-only deps.
- [ ] `ck3chronicle doctor` runs end-to-end and lists every `ROOT_*` value.
- [ ] First run of `ck3chronicle doctor` against a fresh
      `ROOT_CK3CHRONICLE` creates `config.toml` and reports the creation.
- [ ] `ck3chronicle ingest --logs tests/fixtures/logs/with_crash/` creates
      one new session, copies files to durable storage, records the
      crash artifact.
- [ ] Re-running the same `ingest` command returns the **existing**
      session ID with a clear "already ingested" notice.
- [ ] `ck3chronicle ingest --logs tests/fixtures/logs/with_crash/ --force`
      creates a second session whose `forced_duplicate_of` points to the
      first.
- [ ] `ck3chronicle sessions` lists all sessions with correct columns.
- [ ] `pytest` is green (every Phase 0 test, no regressions — there are
      none yet).
- [ ] grep across `src/ck3chronicle/` and `tests/` shows **zero** imports
      from `error analysis refactor` or `ck3chronicle_proto`.
- [ ] grep across `src/ck3chronicle/` (excluding `config.py`) shows
      **zero** uses of `Path.home`, `os.environ`, `expanduser`, or any
      hardcoded `Steam`, `Paradox Interactive`, or `Crusader Kings III`
      path literal.

## 10. End-to-End CLI Demo Transcript (paste in PR body)

The implementer must run and paste this transcript into the PR body:

```
$ python -m pip install -e .
... (success)

$ ck3chronicle doctor
ck3chronicle 0.0.1
Python 3.11.x   SQLite 3.x
config.toml: <ROOT_CK3CHRONICLE>/config.toml  (created with defaults)
ROOT_GAME           : <resolved>   (exists / missing)
ROOT_STEAM          : <resolved>   (exists / missing)
ROOT_LOCAL_MODS     : <resolved>   (exists / missing)
ROOT_LOGS           : <resolved>   (exists / missing)
ROOT_WIP            : <resolved>   (exists / missing)
ROOT_CK3CHRONICLE   : <resolved>   (exists / missing)
durable storage     : writable

$ ck3chronicle ingest --logs tests/fixtures/logs/with_crash/
evidence_bundle_hash: <sha256>
session_id: 1
copied 3 files (2 logs, 1 crash artifact) to durable storage

$ ck3chronicle ingest --logs tests/fixtures/logs/with_crash/
already ingested; existing session_id: 1

$ ck3chronicle ingest --logs tests/fixtures/logs/with_crash/ --force
forced duplicate of session_id: 1
session_id: 2

$ ck3chronicle sessions
id  created_at            logs  crash  bytes
2   2026-06-03T14:..Z     2     1      ...
1   2026-06-03T14:..Z     2     1      ...

$ pytest
... N passed
```

## 11. Reviewer Hand-off Note

When the implementer reports done, the reviewer subagent must:

1. Run the §3 validation checklist on the diff.
2. Confirm §2 hard constraints are intact (grep checks in §9).
3. Confirm acceptance tests pass and the demo transcript is in the PR.
4. Return exactly one verdict: `APPROVE` / `REQUEST_CHANGES` / `REJECT`.

## 12. Out-of-Scope (Phase 0 must NOT do)

- Parse log contents into issues. (Phase 1.)
- Compare sessions / build deltas. (Phase 2.)
- Introduce `Playset`. (Phase 3.)
- Resolve overrides. (Phase 4.)
- Touch `git`. (Phase 5.)
- Score fixability or generate recommendations. (Phase 6.)
- Stable agent JSON contracts. (Phase 7.)
- Cross-run analytics. (Phase 8.)
- Any IDE / ck3lens / MCP integration. (Phase 9.)
- Edit, import from, or move anything inside
  `error analysis refactor/` or `ck3chronicle_proto/`.

---

## §13 Orchestrator Tier Signal (per §9 of implementation plan)

Every reply from this phase's implementer and reviewer MUST end with:

```
Orchestrator tier signal: [A | B]
Reason: <one short sentence>
```

For Phase 0 specifically:
- **Implementer success** → `Tier B` (next action: orchestrator invokes reviewer; mechanical).
- **Reviewer `APPROVE`** → `Tier A` (next action: orchestrator drafts Phase 1 launch packet — first three-agent pipeline phase, new shape).
- **Reviewer `REQUEST_CHANGES`** → `Tier B` (next action: orchestrator re-dispatches implementer with the itemized fix list).
- **Reviewer `REJECT`** → `Tier A` (next action: orchestrator diagnoses boundary-rule or heritage-rule violation).

This applies even when the orchestrator is a human; the signal documents
recommended tier without forcing it.
