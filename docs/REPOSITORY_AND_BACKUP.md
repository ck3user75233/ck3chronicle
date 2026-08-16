# Canonical repository and backup boundary

The canonical repository is:

`https://github.com/ck3user75233/ck3chronicle.git`

The checkout at `ck3chronicle` owns its own `.git` directory. It is not a
worktree of, submodule of, or otherwise dependent on the `ck3raven` Git
repository. Auxiliary historical worktrees may physically live elsewhere, but
the canonical branch and object database are owned by `ck3chronicle/.git`.

## Included in Git

- product source and CLI;
- watcher, capture, archive, run-receipt, and reconciliation logic;
- SQLite schema, migrations, repositories, and audits;
- parser, empirical classifier, semantic projection, reporting, and triage;
- approved hash-bound model/catalog revisions and their manifests;
- reusable learner, review, and catalog-generation source under `tools/`;
- source-only archives of independently authored public evaluator harnesses
  under `evaluation/archive/`, without their corpora or generated results;
- product contracts, plans, operator documentation, and automated tests.

## Intentionally excluded

- CK3 `error.log`, `debug.log`, `game.log`, crash folders, and exceptions;
- content-addressed session archives and pending copies;
- local SQLite databases and journals;
- parsed exports, training/reference corpora, private holdouts, human review
  workbooks, and generated evaluator/scorer result packages;
- virtual environments, caches, editor settings, and build products.

Those exclusions protect privacy and keep the source repository reproducible.
They also mean Git is a complete backup of the software and project method,
not a backup of a user's captured gameplay evidence. A clean-clone verification
must install the project, load the approved model/catalog, and pass the tracked
test suite without consulting ck3raven or WIP paths.
