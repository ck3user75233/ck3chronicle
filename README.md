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
  one provenance row per semantic unit;

The watcher is deliberately copy-only. Hashing, SQLite work, parsing, and
classification do not occur in the process-exit path.

## Commands currently implemented

```powershell
.\.venv\Scripts\ck3chronicle.exe doctor
.\.venv\Scripts\ck3chronicle.exe audit-db
.\.venv\Scripts\ck3chronicle.exe audit-db --deep
.\.venv\Scripts\ck3chronicle.exe compact-db
.\.venv\Scripts\ck3chronicle.exe observe-logging
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

`audit-db` is a read-only reconciliation of finalized archives, session
manifests, parser counters, canonical occurrence totals, classification runs,
runtime context, and source-block provenance. The standard audit is intended
for routine use. `--deep` adds full per-block and per-signature distribution
checks and can take several minutes on a gigabyte-scale database.

`compact-db` losslessly normalizes repeated decoded raw blocks and complete
classification payloads, keeps one lightweight relationship row per actual
occurrence, runs SQLite integrity checks, and vacuums reclaimable pages. On the
15-session real-index oracle it reduced SQLite from 1.584 GB to 289.6 MB without
changing any executive report, comparison, or triage JSON hash.

`observe-logging` is an opt-in empirical diagnostic for one CK3 lifecycle. It
scans `error.log` and `game.log` once, then reads appended bytes only, writing a
30-second JSONL heartbeat. It records the suspected boundary only when
`error.log` remains at exactly 100,000 timestamp headers for the configured
stall interval while the same running CK3 process continues advancing
`game.log`. It does not copy, hash, parse, classify, or write SQLite.

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

1. [Project status](docs/PROJECT_STATUS.md)
2. [Product contract](docs/PRODUCT_CONTRACT.md)
3. [Testing authority](docs/TESTING.md)
4. [Roadmap](docs/ROADMAP.md)
5. [Resolver input audit](docs/RESOLVER_INPUT_AUDIT.md)

## Configuration

On first run, `ck3chronicle doctor` creates configuration at:

- Windows: `%LOCALAPPDATA%\ck3chronicle\config.toml`
- Linux/macOS: `~/.local/share/ck3chronicle/config.toml`
