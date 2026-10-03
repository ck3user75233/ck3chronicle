# Task 08 Prompt — SQL reports and read-only database audit

Status: superseded scope proposal; do not issue for implementation. The owner
has expanded reporting/source-context/history requirements and split delivery
into 08A and 08B. See [current scope decisions](TASK08_SCOPE_REVIEW.md).
Use [Task 08A](TASK08A_PROMPT.md) followed by [Task 08B](TASK08B_PROMPT.md).
The historical body below is retained for reference, not execution. Its audit
assignment is excluded from the replacement tasks.

## Objective

Make accepted Runs useful from the ordinary CLI: list Runs, inspect one Run and
its stored diagnostics/playset/review metadata, and check database consistency.
Reports remain usable after raw captures expire and without model packages.
Complete implementation, CLI registration, verification and durable handoff.

## Orientation and receiving baseline

Checkout: `C:/Users/nateb/Documents/ck3chronicle`.
Read `AGENTS.md`, applicable nested instructions, `docs/DEVELOPMENT_ENVIRONMENT.md`,
`docs/BANNED_IDEAS.md`, and the opening current sections of `PROJECT_STATUS.md`,
`PROJECT_PLAN.md` and `CURRENT_HANDOFF.md` under `docs/`.
Read these focused current references:

- `docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md`;
- `docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md`;
- `docs/OWNER_PRODUCT_INTENT.md` and `docs/ERROR_CONTRACT_SPECIFICATION.md`,
  focusing on stored diagnostics, rendering and reports.

07D and 07E are delivered. Later 07E documentation records separately authorized
live activation. Historical PIDs are not current process identities. Source
inspection and disposable checks do not require operating that live runtime.
Do not read the rejected shared-database-handler design, copies or continuations.
This prompt supersedes the old Task 08 draft in the WIP prompt collection.

Inspect current `pipeline/repository.py`, `schema.py`, `contracts.py`,
`request_handler.py`, `database_handler.py`, `runtime_logging.py` and `cli.py`.
Reuse `list_runs`, `latest_run`, `get_run`, `read_diagnostics`, `read_playset`,
`read_review_metadata` and `contracts.render`; these already exist.
Historical tests and output counts do not create requirements.

## Command surface

Register exactly three new logical commands in the existing root CLI:

```text
runs --database FILE [--limit N] [--offset N] [--format text|json]
report --database FILE --run ID|latest [--view summary|diagnostics|playset|review|all]
       [--match-status template|provisional] [--source-family VALUE] [--format text|json]
audit-db --database FILE [--run ID] [--format text|json]
```

Use text output by default; `report` defaults to `summary`. An omitted audit Run
selects the whole database. Database selection is an explicit existing SQLite
file, with no discovery, initialization, migration or fallback.
Run listing uses the repository's existing newest-processing-first order.
`latest` uses that same order and resolves once to a Run ID for the entire report.
Return all matching records unless an explicit supported pagination argument
limits them; never silently truncate. Diagnostic filters apply only to
`diagnostics` or `all`; reject irrelevant filter/view combinations clearly.

Do not add separate latest/errors/review commands. Existing ingestion, capture,
watch, doctor and observe-logging commands retain their contracts.

## Report contents

- Run listing: Run ID, processing time, available capture time/route and stored
  diagnostic/review totals. Distinguish processing time from game/capture facts.
- Summary: stored Run identity/hash, available capture/lifecycle facts, per-Run
  processing lineage, unique diagnostic count, occurrence counts by match status,
  playset availability and stored review counts/references.
- Diagnostics: render each record using its SQL definition and values. Show
  occurrence count, template/provisional status, stored source/emitter and
  template identifier. Include both statuses by default. Preserve multiline
  text, binding values and existing record order; do not expand repeated copies.
- Playset: ordered stored members and pair provenance, preserving nulls and
  repeats. `playset_captured=false` means unavailable, not unmodded.
- Review: stored native-log and manifest references, availability, counts and
  recorded hash. Label availability as stored metadata, not a filesystem check.
  Zero review emissions still have the Run's two-part shard metadata.
- `all`: combine these views for the same resolved Run. Identify filtered
  diagnostic totals separately from the unfiltered Run totals.

Provide reusable report functions and human/JSON presentation over the same
data. Keep fields unambiguous and document the actual API/output shape. Do not
invent missing lifecycle observations, error taxonomy or occurrence timestamps.
These reports do not reconstruct the original log's complete timestamp/order.

## Shared runtime boundary

All runtime database reads go through `HandlerClient`. No reporting caller opens
SQLite, receives a repository/connection, or sends arbitrary SQL. Add only fixed
read/audit operations demonstrably needed in the owning repository and handler.
Perform display formatting outside the database worker. Use one coherent
database read operation for audit totals that must agree during concurrent ingest.

Use 07E's shared logging helpers and inherited operation/request instrumentation;
do not configure another logger output or log every diagnostic. Preserve CLI
stdout for the requested report. Preserve all 07D request/duplicate/cache/lookup
semantics, including `exception_class` and `LookupError` for unavailable results.
Missing result retrieval is not evidence of a new request outcome or permission
to resubmit automatically.

Successful empty queries are valid: no Runs, no matching diagnostics and zero
review emissions are distinguishable from failures. `latest` on an empty database
reports no Runs successfully. An explicit unknown Run ID is a clear command error;
check Run existence rather than presenting an empty diagnostic list as proof.
Use exit 0 for successful reports and audits with no findings, exit 1 for command
failures or audit findings, and argparse's normal usage-error behavior. Preserve
handler request semantics: a completed audit can return findings. Put successful
reports/audit findings on stdout and ordinary operational errors on stderr.

## Bounded audit

Audit stored relationships and consistency only:

- Run-owned diagnostics refer to existing stored definitions with the applicable
  Run model/contract lineage; different compatible Runs may use different packages.
- Diagnostic row counts and summed occurrences, including each match status,
  agree with the corresponding stored Run counters.
- Each accepted Run has its playset and review metadata; member ownership/order,
  captured/unavailable state and review emission/unit totals agree with stored facts.
- Stored definitions/values render through the existing contract renderer.

Reuse current contract meanings and shared checks where appropriate. Identify
findings by Run and record/reference when available, with plain explanations.
Document which checks were performed and their limits. Do not claim complete
original-emission coverage from aggregated SQL alone. If the database cannot be
opened or audited, report that failure rather than a clean result.

Do not inspect or hash raw logs, load parser/matcher/model artifacts, read native
shard bodies, or consult today's mod descriptors. Do not repair, delete, backfill,
reset or migrate data. No schema or review-format change is commissioned.

## Verification and delivery

Use `.venv/Scripts/python.exe`, disposable storage and genuine complete retained
CK3 inputs. Reuse suitable existing native evidence; do not fabricate diagnostic
records or modify artifacts to manufacture cases. Demonstrate:

- registered CLI commands and reusable APIs produce matching text/JSON facts;
- rendered diagnostics, counts, supported filters, ordered playset/unavailable
  state and review metadata agree with the stored genuine-input results;
- SQL reports and audit work without opening raw logs, model resources or shards;
- empty storage, unknown Run, no filter matches and incompatible database behave
  as specified, without creating/resetting storage;
- audit checks applicable stored relationships without modifying application
  tables or review artifacts; runtime reads use the shared handler;
- 07E logging ownership enforcement passes and report stdout remains usable.

Run relevant regression checks for affected boundaries. Do not rerun learner
campaigns or create a general audit/test framework. Preserve the unrelated dirty
tree. No commit/push, production ingestion, live restart, reset or raw expiry.

Deliver code wired into the CLI, focused checks, operator examples and
`docs/TASK08_REPORTS_AND_AUDIT_HANDOFF.md`. Record actual commands/API signatures,
output/exit behavior, changed files, verification performed and concrete limits.
Update current README guidance and opening status/plan/handoff/task-ledger entries.
Distinguish inherited verification from checks actually run.

Run-result replacement, cross-Run comparison, learner work and complete live
Trusted Run acceptance remain separate. No later wiring task is needed merely
to expose the commands delivered here.
