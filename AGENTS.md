# ck3chronicle agent instructions

These instructions apply to the entire repository. A nested `AGENTS.md` may
add stricter rules for its subtree.

## Canonical repository boundary

- The Git root containing this file is the only source-of-truth repository for
  ck3chronicle.
- The canonical remote is `https://github.com/ck3user75233/ck3chronicle.git`.
- On Nate's current machine, the canonical checkout is
  `C:\Users\nateb\Documents\ck3chronicle`.
- Never implement, stage, commit, or generate ck3chronicle source under the
  sibling `ck3raven` repository, any `.ck3raven/wip` tree, or an old
  `ck3chronicle` WIP directory. Those locations may be read only when a task
  explicitly calls for historical research or external input.
- Before any write, confirm that `git rev-parse --show-toplevel` identifies
  this repository. If the task starts from another workspace folder, set the
  command working directory to this repository first.
- Do not make ck3chronicle depend on the `ck3raven` Git history, modules,
  worktrees, or untracked files. A clean clone of this repository must contain
  all reusable product and project-method source.

## Ownership map

- Product package and CLI: `src/ck3chronicle/`
- SQLite schema, migrations, and repositories: `src/ck3chronicle/db/`
- Approved runtime models and projection catalogs: `models/`
- Empirical learner, review, registry, and catalog-generation tools:
  `tools/template_learning/`
- Future requirement-derived regression checks: `tests/`
- Current plans, contracts, status, and operating guidance: `docs/`

Search these locations before creating a new implementation. Extend the
existing owned component instead of constructing a parallel copy elsewhere.

## Source versus local evidence

Commit reusable code, schemas, migrations, model/catalog artifacts, tests,
contracts, and operating documentation. Do not commit captured CK3 logs,
session archives, pending copies, SQLite runtime databases, parsed exports,
training/reference corpora, human-review workbooks, generated evaluator
results, or private holdouts. Pass external evidence through explicit CLI
paths; never hardcode a local WIP path into reusable source.

## Classification policy

The release requirement is complete occurrence accounting, not 100% L1/L2 or
full-contract attribution. Full, composed L1+L2, L1-only,
provisional/low-confidence, and unknown are legitimate durable outcomes.
Preserve confidence and disposition so unresolved patterns can be reviewed
periodically. Do not manufacture a confident template merely to improve a
coverage percentage.

## Workflow and handoff

1. Read `README.md`, `docs/CURRENT_HANDOFF.md`, `docs/PROJECT_STATUS.md`, and
   `docs/PROJECT_PLAN.md` before planning substantial work.
2. Treat dated restart handoffs and paths outside this repository as historical
   evidence, not current implementation authority.
3. Keep current routing, status, and operator documentation in the same commit
   as a material architecture or workflow change.
4. Run verification derived from the active requirement. Until the replacement
   test suite is established, run compilation, package/import/CLI checks, and
   read-only checks against representative real CK3 evidence. Do not port
   expectations from historical tests.
5. Run routine Python verification inside the agent with
   `.\.venv\Scripts\python.exe`. Do not delegate compilation, imports, CLI
   checks, or tests to the owner merely because the optional
   `.venv-owner-20260829` base interpreter is inaccessible to the sandbox. If
   `.venv` itself fails, diagnose or restore an agent-accessible project
   environment before declaring the work blocked.
6. Run `git diff --check` and inspect `git status --short` before committing.
7. Commit and push only from this repository. `main` on the canonical remote is
   the official recoverable copy; active `codex/*` branches are development
   checkpoints, not separate sources of truth.

## Verification authority

Tests, fixtures, and historical thresholds do not create product scope. Derive
every future check from an active owner-directed requirement and observed
supported CK3 behavior. Parser and learner proof uses representative real CK3
evidence outside Git. A holdout or independent evaluator exists only for a
separately commissioned empirical claim.

## Code review rules

- Treat `docs/BANNED_IDEAS.md` as the register of disproven design artifacts;
  do not reintroduce an entry without an explicit owner decision overturning it.
- Flag any ck3chronicle implementation or learner path outside this Git root.
- Flag hardcoded `.ck3raven/wip` dependencies in active source or guidance.
- Flag committed gameplay evidence, databases, corpora, workbooks, generated
  evaluation results, or private oracle material.
- Flag changes that turn unknown or low-confidence classifications into silent
  drops or claim 100% semantic coverage as a release requirement.
