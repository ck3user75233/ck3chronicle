# ck3chronicle

ck3chronicle preserves CK3 runtime evidence and turns `error.log` into
versioned, reviewable error intelligence.

This repository was taken over and reset to a controlled reboot on
2026-08-13. Historical plans, prototypes, and tests were archived outside the
active source tree because they described a different or failed design.

## Working capabilities

- copy CK3 logs immediately after an observed `ck3.exe` exit;
- journal process starts, exits, heartbeats, copy attempts, and failures;
- finalize protected copies into content-addressed archives;
- verify archive manifests and reconcile finalized archives with SQLite;
- split archived `error.log` into immutable source blocks;
- persist canonical occurrence and cluster rows transactionally;
- load the exact approved empirical model after whole-file SHA-256 validation;
- classify diagnostics as full, independently composed L1+L2, L1-only, or
  unknown while retaining key, locator, and structured-slot evidence;
- atomically persist versioned model registrations, classification runs, and
  one provenance row per semantic unit.

The watcher is deliberately copy-only. Hashing, SQLite work, parsing, and
classification do not occur in the process-exit path.

## Commands currently implemented

```powershell
.\.venv\Scripts\ck3chronicle.exe doctor
.\.venv\Scripts\ck3chronicle.exe watch
.\.venv\Scripts\ck3chronicle.exe capture
.\.venv\Scripts\ck3chronicle.exe reconcile
.\.venv\Scripts\ck3chronicle.exe sessions
.\.venv\Scripts\ck3chronicle.exe parse --session <ID>
.\.venv\Scripts\ck3chronicle.exe classify --session <ID>
.\.venv\Scripts\ck3chronicle.exe review-queue --session <ID>
.\.venv\Scripts\ck3chronicle.exe report --session <ID>
.\.venv\Scripts\ck3chronicle.exe report --session <ID> --since <EARLIER_ID>
.\.venv\Scripts\ck3chronicle.exe latest
.\.venv\Scripts\ck3chronicle.exe errors --session <ID>
.\.venv\Scripts\ck3chronicle.exe process-pending
.\.venv\Scripts\ck3chronicle.exe compare
.\.venv\Scripts\ck3chronicle.exe baseline create <NAME>
.\.venv\Scripts\ck3chronicle.exe baseline list
.\.venv\Scripts\ck3chronicle.exe ignore add <PATTERN_ID> --reason <TEXT>
.\.venv\Scripts\ck3chronicle.exe ignore list
.\.venv\Scripts\ck3chronicle.exe context --session <ID>
.\.venv\Scripts\ck3chronicle.exe resolve-file --session <ID> --path <RELATIVE_PATH>
.\.venv\Scripts\ck3chronicle.exe triage
```

`watch` is a foreground process and must currently be started again after a PC
restart. Automatic login startup has not yet been released.

## Current development checkpoint

`process-pending` is the normal deferred workflow after the copy-only watcher:
it finalizes protected pending copies, reconciles archives, parses canonical
blocks, classifies them with the approved model, and prints the latest report.
It is idempotent and never rewrites captured evidence.

`compare` selects the latest and preceding compatible captures by capture time.
It reports observed new, fixed, worse, improved, and unchanged semantic
patterns. Known patterns use stable contract IDs; residuals use normalized slot
structure, so keys, locators, timestamps, and line numbers do not create false
changes. Use `--session` and `--against` to choose an explicit pair.
Raw counts are accompanied by rates over the stored first-to-last error window
and evidence-quality warnings; these are observational diagnostics, not causal
claims about a patch or mod.

Baselines pin both a session and the exact classification model used to
interpret it. Ignore rules are model-bound annotations with mandatory reasons;
ignored patterns remain visible in comparisons and retain their counts.
`report --since` returns a versioned report-plus-comparison JSON envelope (or
both human-readable sections) under the same exact model revision.

`context` reads only the session's archived `debug.log`. The contiguous
`Mounted Data:` sequence is authoritative for DLC/mod membership and order;
the earlier DLC/Mod inventory only supplies names and descriptor paths and is
used for exact-set validation. Disabled inventory entries are never promoted
into the active mod list.
Session comparisons report mounted DLC/mod additions, removals, and load-order
moves. They deliberately do not infer that mod contents are unchanged when a
Workshop/local mount identity remains the same.

`resolve-file` projects one session's recorded active roots onto the current
filesystem. It checks base game, mounted DLCs, and active mods in order, never
searches inactive mod roots, and reports a cautiously worded last-mounted
candidate. It does not yet claim historical contents or full CK3 merge rules.

`triage` keeps classification review separate from game-error priority. It
ranks observed new/worse contracts, links their stored file evidence to the
current active-root projection when possible, and retains explicit evidence
quality and non-causality caveats.

Read these documents in order:

1. [Project status](docs/PROJECT_STATUS.md)
2. [Product contract](docs/PRODUCT_CONTRACT.md)
3. [Testing authority](docs/TESTING.md)
4. [Roadmap](docs/ROADMAP.md)

## Configuration

On first run, `ck3chronicle doctor` creates configuration at:

- Windows: `%LOCALAPPDATA%\ck3chronicle\config.toml`
- Linux/macOS: `~/.local/share/ck3chronicle/config.toml`
