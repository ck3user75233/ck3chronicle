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
3. Complete selected template and provisional assignments become compact SQLite
   records with a filterable match status. Unassigned/unresolved evidence goes to
   one native review shard for the resulting Run ID.
4. Reports query SQLite and do not depend on the original CK3 log.

Configuration is explicit, CK3 and mod sources are read-only, and runtime
evidence remains outside Git. See
[`docs/ARCHITECTURE_AND_DATA_LINEAGE.md`](docs/ARCHITECTURE_AND_DATA_LINEAGE.md).
The approved contract and current Task 05 boundary are in
[`docs/ERROR_CONTRACT_SPECIFICATION.md`](docs/ERROR_CONTRACT_SPECIFICATION.md) and
[`docs/05_ERROR_CONTRACT_IMPLEMENTATION.md`](docs/05_ERROR_CONTRACT_IMPLEMENTATION.md).

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

Task 06B removed the old CLI/provider stack; see
[`docs/TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md`](docs/TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md).
Capture stays in `harvester.py`; Task 07 delivered ingest/retention APIs, manual
ingest, per-Run lineage and playset storage; watcher integration is also delivered.
Task 07D delivers the dedicated shared database handler and bounded receiving
repairs: use `docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md` for current APIs,
verification and the separate live-activation step. Runtime clients use
`pipeline.request_handler.HandlerClient`. Do not read or reuse the
rejected shared-database-handler design or its copies/continuation instructions.
Tasks 08A.1/08A.2/08B belong to Reporting and Analysis: 08A.1 implements
reusable diagnostic queries/history; 08A.2 implements playset source search/context
and its query integration; 08B implements reports and CLI. Use
`docs/TASK08A_1_PROMPT.md`, `docs/TASK08A_2_PROMPT.md`, `docs/TASK08B_PROMPT.md`
and the current pointer in `docs/TASK08_SCOPE_REVIEW.md`. The owner's 2026-10-02
revisions supersede conflicting older planning text. Audit is excluded.
Generation replay is banned; current direction is
in `docs/TASK07_SCOPE_REVIEW.md`. Do not restore removed providers.

Task 07E runtime logging belongs to `src/ck3chronicle/runtime_logging.py`.
Runtime components use its logger/event helpers; only that owner configures
handlers, formatting, rotation and log paths. Run
`.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py` for runtime changes.
The synthetic/fault-injection logging test module was removed by owner direction;
do not restore it from historical handoffs or runners.
See `docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md` for fields, operator queries and
the separate activation procedure. Logs never reconstruct unavailable outcomes.

## Working in this repository

The checkout is `C:\Users\nateb\Documents\ck3chronicle`; its source repository
is `https://github.com/ck3user75233/ck3chronicle.git`.

- Product and CLI code: `src/ck3chronicle/`
- Current Run storage: `src/ck3chronicle/pipeline/schema.py` and `repository.py`
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

Owner clarification for reporting verification (2026-10-02): use genuine stored
CK3 records through the public handler. Do not introduce synthetic histories,
invented diagnostic/count scenarios, mock clients or injected failures as reporting
acceptance tests. A case not represented by real evidence remains unverified;
tests must not create additional product requirements. Report failed checks and
any proposed requirements beyond the assigned task explicitly to the owner.
