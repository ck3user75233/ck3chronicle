# Canonical repository and backup boundary

The canonical repository is:

`https://github.com/ck3user75233/ck3chronicle.git`

The checkout at `ck3chronicle` owns its own `.git` directory. It is not a
worktree of, submodule of, or otherwise dependent on the `ck3raven` Git
repository. Auxiliary historical worktrees may physically live elsewhere, but
the canonical branch and object database are owned by `ck3chronicle/.git`.

Current repair note (2026-09-08): the local `origin` fetchspec names only
`codex/ck3chronicle-reboot`, so this checkout has no `origin/main` tracking ref.
In a task with `.git` write access and GitHub connectivity, restore the normal
all-heads fetchspec, fetch/prune, inspect `origin/main`, and only then commit and
promote the reboot. This is local remote-configuration debt, not object-store
corruption.

```powershell
git config --replace-all remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
git fetch --prune origin
git branch -a -vv
```

Repository-loaded agent instructions live in `AGENTS.md`; the detailed
ownership map lives in `WORKSPACE_ROUTING.md`; and restart-safe current context
lives in `CURRENT_HANDOFF.md`. These files must be updated when source
ownership changes so new agents do not reconstruct moved tooling in WIP.

## Included in Git

- product source and CLI;
- watcher, capture, archive, pending-metadata, and reconciliation logic;
- SQLite schema, migrations, repositories, and audits;
- parser, empirical classifier, semantic projection, reporting, and triage;
- approved hash-bound model/catalog revisions and their manifests;
- reusable learner, review, and catalog-generation source under `tools/`;
- product contracts, plans, and operator documentation;
- future requirement-derived verification source, when added.

## Intentionally excluded

- CK3 `error.log`, `debug.log`, `game.log`, crash folders, and exceptions;
- uniquely identified live-session archives and pending copies;
- local SQLite databases and journals;
- parsed exports, training/reference corpora, private holdouts, human review
  workbooks, and generated evaluator/scorer result packages;
- virtual environments, caches, editor settings, and build products.

These local artifacts live under the ignored `.ck3chronicle/wip/` tree inside
the canonical checkout so the managed repository sandbox can own capture,
processing, database audit, and learner review without writing outside its
boundary. They remain excluded from Git and require their own backup.

Those exclusions protect privacy and keep the source repository reproducible.
They also mean Git is a complete backup of the software and project method,
not a backup of a user's captured gameplay evidence. A clean-clone verification
must install the project, load the approved model/catalog, and pass package,
import, and current requirement-derived checks without consulting ck3raven or
WIP paths.
