# Workspace and source routing

## One source of truth

All reusable ck3chronicle work belongs in the standalone Git repository whose
canonical remote is:

`https://github.com/ck3user75233/ck3chronicle.git`

On the current machine its primary checkout is:

`C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle`

The `ck3raven` repository and `.ck3raven/wip` directories are separate
projects/scratch areas. They are not alternate ck3chronicle source roots and
must not receive ck3chronicle implementation changes. Historical files there
may be supplied as read-only inputs, but anything reusable must be implemented,
tested, documented, and committed here.

## Where work belongs

| Work product | Canonical location | Git policy |
|---|---|---|
| Product/runtime code | `src/ck3chronicle/` | Track |
| Database schema and migrations | `src/ck3chronicle/db/` | Track |
| Approved model/catalog revisions | `models/` | Track with hashes/manifests |
| Learner and review tooling | `tools/template_learning/` | Track reusable source only |
| Product regression tests | `tests/` | Track |
| Contracts, plan, status, handoff | `docs/` | Track |
| Completed independent harness source | `evaluation/archive/<revision>/` | Track source-only immutable snapshot |
| Logs, crash evidence, archives, pending copies | Runtime/local data | Ignore |
| SQLite runtime databases | Runtime/local data | Ignore |
| Training/reference corpora and review workbooks | External/local data | Ignore |
| Private holdouts and expected answers | External protected data | Never commit |
| Generated runner/scorer/evaluation results | External/local data | Ignore |

## Preventing parallel construction

Before starting a feature or learner change:

1. Confirm this repository is the command working directory and Git root.
2. Search the ownership locations above for an existing component.
3. Extend that component and its tests rather than copying it into WIP.
4. If historical WIP contains a useful idea, port the reusable logic here and
   remove all runtime dependency on the historical path.
5. Update `docs/CURRENT_HANDOFF.md` and other current authority when ownership
   or workflow changes.

The repository test suite contains a boundary contract that fails if the old
WIP learner root is reintroduced into active source or current guidance.

## Classification improvement loop

Unknown and lower-confidence classification outcomes are expected review
queues, not evidence loss. The supported loop is:

1. preserve and process every occurrence;
2. query unknown, L1-only, provisional, or low-confidence assignments;
3. review representative evidence periodically;
4. improve the learner/contracts generically in `tools/template_learning/`;
5. publish a reviewed immutable model/catalog revision under `models/`;
6. reproject stored immutable source blocks while retaining lineage.

No step requires or promises 100% semantic attribution.
