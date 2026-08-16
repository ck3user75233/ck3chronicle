# ck3chronicle

ck3chronicle preserves CK3 runtime evidence and turns `error.log` into
versioned, reviewable error intelligence.

This repository was taken over and reset to a controlled reboot on
2026-08-13. It is the canonical, standalone source repository. Historical WIP
outside this tree is not required to install, run, test, or continue the
product; reusable learner and catalog-generation source is retained under
`tools/`, while captured logs, local databases, training corpora, private
holdouts, and generated evaluation results remain local data.

Agents and workflows must follow the repository-loaded rules in `AGENTS.md`.
The exact source/data routing map is in `docs/WORKSPACE_ROUTING.md`; the current
restart-safe project state is in `docs/CURRENT_HANDOFF.md`. In particular,
neither `ck3raven` nor `.ck3raven/wip` is an alternate implementation root.

## Working capabilities

- copy CK3 logs immediately after an observed `ck3.exe` exit;
- journal process starts, exits, heartbeats, copy attempts, and failures;
- retain one immutable run receipt per observed exit independently of
  content-addressed evidence deduplication;
- record normal/crash/unknown termination and exact crash-log source
  equivalence without duplicating identical crash-folder logs;
- capture `exception.txt` by default from the newly associated crash folder,
  with explicit captured/absent/unavailable provenance bound to the run;
- finalize protected copies into content-addressed archives;
- verify archive manifests and reconcile finalized archives with SQLite;
- split archived `error.log` into immutable source blocks;
- stream canonical occurrence and cluster rows in one rollback-safe
  transaction, with persisted cardinality/provenance validation before success;
- load the exact approved empirical model after whole-file SHA-256 validation;
- classify diagnostics as full, independently composed L1+L2, L1-only, or
  unknown while retaining key, locator, and structured-slot evidence;
- require typed template PostValidate after empirical candidate selection, so
  a recognized locator can never satisfy a key/value/parameter slot;
- atomically persist versioned model registrations, classification runs, and
  one provenance row per semantic unit;

Classification coverage is not required to reach 100%. Every occurrence must
be accounted for, but L1-only, provisional/low-confidence, and unknown results
are legitimate stored outcomes that can be reviewed and improved over time.

## Install from a clean clone

```powershell
git clone https://github.com/ck3user75233/ck3chronicle.git
Set-Location ck3chronicle
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
```

The approved model and semantic catalog are source-controlled and are also
included as installed package data. Runtime captures, databases, and training
corpora are intentionally not downloaded with the source.

The watcher never hashes the live principal logs and performs no SQLite,
parsing, or classification work in the process-exit path. It copies the small
crash `exception.txt` artifact, when present, and hashes only that protected
copy so the immutable run receipt can bind it immediately.

## Commands currently implemented

```powershell
.\.venv\Scripts\ck3chronicle.exe doctor
.\.venv\Scripts\ck3chronicle.exe audit-db
.\.venv\Scripts\ck3chronicle.exe audit-db --deep
.\.venv\Scripts\ck3chronicle.exe observe-logging
.\.venv\Scripts\ck3chronicle.exe watch
.\.venv\Scripts\ck3chronicle.exe capture
.\.venv\Scripts\ck3chronicle.exe reconcile
.\.venv\Scripts\ck3chronicle.exe sessions
.\.venv\Scripts\ck3chronicle.exe parse --session <ID>
.\.venv\Scripts\ck3chronicle.exe classify --session <ID>
.\.venv\Scripts\ck3chronicle.exe review-queue --session <ID>
.\.venv\Scripts\ck3chronicle.exe report --session <ID>
.\.venv\Scripts\ck3chronicle.exe report --run <RUN_ID>
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

The project is in **Phase 1: first useful vertical slice**. Substantial
capabilities work, but Phase 1 has not passed its complete exit gate. A green
fast suite or an implemented capability is not a phase-completion claim. See
`docs/PROJECT_PLAN.md` and `docs/PHASE1_EXIT_PROTOCOL.md`.

`process-pending` is the normal deferred workflow after the copy-only watcher:
it finalizes protected pending copies, reconciles archives and run receipts,
extracts runtime context, streams canonical blocks, classifies them with the
approved model, and prints the latest report. It is idempotent and never
rewrites captured evidence.

With `--json`, `process-pending` always emits one
`ck3chronicle.command-result` v1 object. Success, warning, archive-integrity,
model, database, and generic pipeline failures have stable status, exit code,
result, and error fields. The JSON `report`, `latest`, and `errors` surfaces use
the same envelope. `report --run` selects an exact observed CK3 run even when
its evidence bytes are shared with an earlier or later run.

`audit-db` is a read-only reconciliation of finalized archives, session
manifests, parser counters, canonical occurrence totals, classification runs,
runtime context, and source-block provenance. The standard audit is intended
for routine use. `--deep` adds full per-block and per-signature distribution
checks and can take several minutes on a gigabyte-scale database.

Compact storage is the default schema and requires no normal user action. An
older database is migrated, integrity-checked, and physically reclaimed once
when it is first opened. A consistent disposable copy of the live 15-session
index was reclaimed from 1.584 GB to 289.6 MB without changing any executive
report, comparison, or triage JSON hash.

`observe-logging` is an opt-in empirical diagnostic for one CK3 lifecycle. It
scans `error.log` and `game.log` once, then reads appended bytes only, writing a
replaceable 30-second current-health heartbeat and retaining only lifecycle or
decisive-result events. It records the suspected boundary only when
`error.log` remains at exactly 100,000 timestamp headers for the configured
stall interval while the same running CK3 process continues advancing
`game.log`. It does not copy, hash, parse, classify, or write SQLite.

`compare` selects the latest and preceding compatible runs by observed run time,
even when several runs reuse one content-addressed evidence bundle.
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
its exact file, line/byte range, block hash, candidate count, and termination
evidence are stored. Complete, partial, absent, malformed, truncated, and
ambiguous states are distinct. The earlier DLC/Mod inventory supplies a
separate enrichment projection of names, descriptor paths, and mismatch
warnings; it cannot change authoritative membership/order. Disabled inventory
entries are never promoted into the active mod list. Source resolution refuses
non-complete runtime context.
Session comparisons report mounted DLC/mod additions, removals, and load-order
moves. They deliberately do not infer that mod contents are unchanged when a
Workshop/local mount identity remains the same.

`resolve-file` prefers an immutable processing-time observation when one has
been stored for the requested session/path; otherwise it projects the recorded
active roots onto the current filesystem. It checks base game, mounted DLCs,
and active mods in order and never searches inactive roots. Exact-relative-path
replacement is resolved separately from directory-specific semantics. The
resolver groundwork is optional and is not invoked by `process-pending`.
On-action and culture semantic adapters are explicitly deferred until the
database and real-corpus acceptance work is complete.

`triage` keeps classification review separate from game-error priority. It
ranks observed new/worse contracts, links their stored file evidence to the
active-root resolution when requested, and retains explicit evidence-quality
and non-causality caveats. Resolver enrichment is downstream of the core
database workflow.

Read these documents in order:

1. [Workspace and source routing](docs/WORKSPACE_ROUTING.md)
2. [Current development handoff](docs/CURRENT_HANDOFF.md)
3. [Project phase plan](docs/PROJECT_PLAN.md)
4. [Phase 1 exit matrix](docs/PHASE1_EXIT_MATRIX.md)
5. [Phase 1 evaluation interface](docs/PHASE1_EVALUATION_INTERFACE.md)
6. [Phase 1 public gate rules](docs/PHASE1_PUBLIC_GATE_RULES.md)
7. [Phase 1 output contracts](docs/PHASE1_OUTPUT_CONTRACTS.md)
8. [Phase 1 semantic authority](docs/PHASE1_SEMANTIC_AUTHORITY.md)
9. [Phase 1 exit protocol](docs/PHASE1_EXIT_PROTOCOL.md)
10. [Project status](docs/PROJECT_STATUS.md)
11. [Product contract](docs/PRODUCT_CONTRACT.md)
12. [Testing authority](docs/TESTING.md)

The optional [capability inventory](docs/CAPABILITY_INVENTORY.md) is a backlog
reference, not phase or startup authority.

## Configuration

On first run, `ck3chronicle doctor` creates configuration at:

- Windows: `%LOCALAPPDATA%\ck3chronicle\config.toml`
- Linux/macOS: `~/.local/share/ck3chronicle/config.toml`
