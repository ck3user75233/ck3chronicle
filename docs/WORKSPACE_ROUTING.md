# Workspace and source routing

## One source of truth

All reusable ck3chronicle work belongs in the standalone Git repository whose
canonical remote is:

`https://github.com/ck3user75233/ck3chronicle.git`

On the current machine its primary checkout is:

`C:\Users\nateb\Documents\ck3chronicle`

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
| Requirement-derived verification | `tests/` | Track only current owner-directed checks |
| Contracts, plan, status, handoff | `docs/` | Track |
| Operational path authority | repository-root `config.toml` | Ignore machine-local values; track `config.example.toml` |
| Logs, crash evidence, archives, pending copies | `.ck3chronicle/wip/runtime/` | Ignore |
| SQLite runtime databases and pending metadata | `.ck3chronicle/wip/runtime/` | Ignore |
| Learner state and candidate artifacts | `.ck3chronicle/wip/learner/` | Ignore |
| Retired local recovery records | `.ck3chronicle/wip/tooling/archive/` | Ignore; never treat as supported tooling |
| Training/reference corpora and review workbooks | Configured local data | Ignore |
| Private holdouts and expected answers | External protected data | Never commit |
| Generated runner/scorer/evaluation results | `.ck3chronicle/wip/evaluation/` | Ignore |

## Preventing parallel construction

Before starting a feature or learner change:

1. Confirm this repository is the command working directory and Git root.
2. Search the ownership locations above for an existing component.
3. Extend that component and its tests rather than copying it into WIP.
4. If historical WIP contains a useful idea, port the reusable logic here and
   remove all runtime dependency on the historical path.
5. Update `docs/CURRENT_HANDOFF.md` and other current authority when ownership
   or workflow changes.

Review and CI must reject any reintroduced dependency on the old WIP learner
root.

## Operational runtime

The repository-root `config.toml` is the explicit authority for configured
machine and writable roots. The relocated watcher, runtime, and learner entry
points do not search the OS for fallback Steam, Paradox,
user-profile, AppData, crash, WIP, runtime, or learner roots. On the current
machine, the configured runtime is `.ck3chronicle/wip/runtime/` under this
checkout and the learner state root is `.ck3chronicle/wip/learner/`. Both
remain local and untracked, but they are inside the managed workspace so the
watcher and deferred processor can run under the repository sandbox.

The current tree still contains bounded path inference outside that relocated
root selection: repository-root config bootstrapping from the required working
directory, approved-model source/install probing, a legacy direct-ingest crash
fixture convention, base-game reconstruction in active source resolution, and
some historical learner/blind-review tool defaults. These are tracked closure
debt, not alternate path authority, and must be removed or replaced by explicit
configured/package/evidence contracts before a repository-wide no-discovery
claim is made.

The approved, hash-bound model revision also retains eight historical absolute
paths under its `evidence.*.path` metadata. They are descriptive strings, not
runtime inputs: the approved model loader consumes revision, algorithm, and
cluster contracts only, and no active path resolution uses those values. Do
not rewrite them in place, because any byte change creates a different model
hash and invalidates the approved catalog relationship. Remove or relativize
them only as part of a deliberately reviewed new model revision.

The runtime tree remains one unit: SQLite, `pending/`, `sessions/`, `watch/`,
and historical migration records must not be split between roots. Retired
runtime subdirectories are inert compatibility residue and are not active
authorities. The one-time legacy relocation is
complete; there is no active importer command or dependency on the legacy
root.

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
