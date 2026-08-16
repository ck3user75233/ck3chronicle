# ck3chronicle agent instructions

These instructions apply to the entire repository. A nested `AGENTS.md` may
add stricter rules for its subtree.

## Canonical repository boundary

- The Git root containing this file is the only source-of-truth repository for
  ck3chronicle.
- The canonical remote is `https://github.com/ck3user75233/ck3chronicle.git`.
- On Nate's current machine, the canonical checkout is
  `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle`.
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
- Product-owned regression tests: `tests/`
- Current plans, contracts, status, and operating guidance: `docs/`
- Source-only archives of completed independent evaluator harnesses:
  `evaluation/archive/`

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
4. Run the focused tests for changed behavior, then the full suite:
   `.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider`.
5. Run `git diff --check` and inspect `git status --short` before committing.
6. Commit and push only from this repository. `main` on the canonical remote is
   the official recoverable copy; active `codex/*` branches are development
   checkpoints, not separate sources of truth.

## Evaluation separation

Implementation agents may maintain public interfaces, contracts, schemas,
fixed input manifests, and ordinary regression tests. They must not author or
edit the executable Phase 1 exit runner, scorer, private holdout, or expected
answers. The next evaluator harness must be authored in a fresh user-owned
task, not by a subagent of the implementation task; its blind runner must use a
separate task. An independently authored completed harness may later be
preserved as a source-only archive under `evaluation/archive/`; its generated
results and corpora remain outside Git.

## Code review rules

- Flag any ck3chronicle implementation or learner path outside this Git root.
- Flag hardcoded `.ck3raven/wip` dependencies in active source or guidance.
- Flag committed gameplay evidence, databases, corpora, workbooks, generated
  evaluation results, or private oracle material.
- Flag changes that turn unknown or low-confidence classifications into silent
  drops or claim 100% semantic coverage as a release requirement.
