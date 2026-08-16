# Current development handoff

Date: 2026-08-17

## Repository authority

- Canonical remote: `https://github.com/ck3user75233/ck3chronicle.git`
- Official branch: `main`
- Active development branch: `codex/ck3chronicle-reboot`
- Primary checkout on this machine:
  `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle`
- `ck3raven` and `.ck3raven/wip` are not ck3chronicle implementation roots.

The repository is standalone and owns its own `.git`. A machine-loss recovery
of product source, tests, schema, approved models/catalogs, learner tooling,
project contracts, and archived evaluator source requires only a clone of the
canonical remote. Gameplay evidence and local databases are intentionally a
separate backup concern.

The full standalone regression suite was verified at **233 passed** on
2026-08-17 after the repository-routing guard was added. GitHub CI runs the
same suite on pushes to `main` and `codex/*` branches and on pull requests.

## Current product state

Phase 1 of the reboot plan is active and has not exited. Capture, run receipts,
immutable archives, SQLite registration, canonical parsing, empirical
classification, semantic projection, review queues, reporting, and audit are
implemented.
The latest independent public attempt found product and evaluator-infrastructure
issues; the product repairs and semantic-projection integration are now in the
current successor line, but no private holdout should run until a new public
attempt is clean.

Classification does not need 100% full/L2 coverage. Every occurrence must be
stored with its disposition and confidence. Unknown, L1-only, composed L1+L2,
and provisional/low-confidence populations remain queryable so later logs and
human review can improve the empirical model over time.

## Canonical development locations

- runtime/package: `src/ck3chronicle/`
- learner/review/catalog tools: `tools/template_learning/`
- approved model and semantic projection catalog: `models/`
- implementation regression tests: `tests/`
- release contracts and plan: `docs/`
- completed independent harness source snapshots: `evaluation/archive/`

Do not resume from an old WIP learner directory. Read `AGENTS.md` and
`docs/WORKSPACE_ROUTING.md` before assigning work to another agent or workflow.

## Next work sequence

1. Keep the lower-confidence/unknown review path operational and visible; do
   not block Phase 1 on perfect semantic coverage.
2. Freeze one clean successor commit, then open a fresh user-owned evaluator
   task. The evaluator must not be a subagent of the implementation task.
3. Run the frozen harness from a separate blind-runner task using the fixed
   input authority; score only the sealed outputs without executing the
   candidate.
4. Repair only evidence-backed product defects or evaluator defects in their
   respective ownership boundaries.
5. Run the new unseen private holdout only after every public gate is valid and
   passing, then publish the candidate-bound Phase 1 exit decision.

## Verification command

From the repository root:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
git diff --check
git status --short
```
