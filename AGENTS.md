# ck3chronicle agent guide

These instructions apply to the whole repository. A nested `AGENTS.md` may add
instructions for its own subtree.

## Project

ck3chronicle is a standalone, local run-intelligence tool for Crusader Kings III
modders. It protects the useful output of completed CK3 runs, turns `error.log`
into durable and reviewable diagnostic history, compares evidence over time,
and will later add source context and cautious action guidance.

The first product milestone is **Trusted Run**: observe one CK3 start-to-exit
lifecycle, protect its live `error.log`, process it into SQLite, preserve
unresolved evidence for review, and report from stored records.

The governing product decisions are in
[`docs/OWNER_PRODUCT_INTENT.md`](docs/OWNER_PRODUCT_INTENT.md).

## Architecture

The target flow is:

1. A lifecycle watcher observes the configured CK3 process and, after exit,
   copies the live `error.log` into protected pending storage.
2. Deferred processing validates and deduplicates that copy, recognizes log
   emissions, and classifies them against approved error contracts.
3. Approved diagnostics become compact SQLite records. Unresolved,
   provisional, or low-confidence emissions go to one native review shard for
   the resulting Run ID.
4. Reports query SQLite and do not depend on the original CK3 log.

Configuration is explicit, CK3 and mod sources are read-only, and runtime
evidence remains outside Git. See
[`docs/ARCHITECTURE_AND_DATA_LINEAGE.md`](docs/ARCHITECTURE_AND_DATA_LINEAGE.md).

## Current direction

Before substantial work, read:

- [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) for milestones and dependencies;
- [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) for the active exercise,
  completed work, gaps, and operational restrictions.

If the working tree is not clean or work continues across tasks, also read
[`docs/CURRENT_HANDOFF.md`](docs/CURRENT_HANDOFF.md) for the live change ledger
and exact continuation point.

Use the focused specifications linked from [`README.md`](README.md) when
changing a particular product boundary. Before reviving a deliberately removed
design, check [`docs/BANNED_IDEAS.md`](docs/BANNED_IDEAS.md).

## Working in this repository

The checkout is `C:\Users\nateb\Documents\ck3chronicle`; its source repository
is `https://github.com/ck3user75233/ck3chronicle.git`.

- Product and CLI code: `src/ck3chronicle/`
- Database code: `src/ck3chronicle/db/`
- Approved runtime models: `models/`
- Empirical learner and review tools: `tools/template_learning/`
- Requirement-derived checks: `tests/`
- Product and operating documentation: `docs/`

Extend the owning component rather than creating a parallel implementation.
Keep captured logs, databases, review material, workbooks, and generated
evaluation results out of Git.

Unknown and low-confidence classifications are legitimate durable outcomes.
Preserve them for review; never drop them silently or manufacture confidence.

Sandbox, local runtime, and Python environment instructions are in
[`docs/DEVELOPMENT_ENVIRONMENT.md`](docs/DEVELOPMENT_ENVIRONMENT.md). Run
routine Python checks with `.\.venv\Scripts\python.exe` and derive verification
from current owner-directed requirements.
