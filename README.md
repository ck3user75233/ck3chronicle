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
- persist canonical occurrence and cluster rows transactionally.

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
```

`watch` is a foreground process and must currently be started again after a PC
restart. Automatic login startup has not yet been released.

## Current development checkpoint

The next checkpoint integrates the approved empirical L1/L2 template learner
as a versioned derived classification layer over stored source blocks. It will
not rewrite captured evidence.

Read these documents in order:

1. [Project status](docs/PROJECT_STATUS.md)
2. [Product contract](docs/PRODUCT_CONTRACT.md)
3. [Testing authority](docs/TESTING.md)
4. [Roadmap](docs/ROADMAP.md)

## Configuration

On first run, `ck3chronicle doctor` creates configuration at:

- Windows: `%LOCALAPPDATA%\ck3chronicle\config.toml`
- Linux/macOS: `~/.local/share/ck3chronicle/config.toml`
