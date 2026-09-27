# Mini-project 3.1 — Build stored reports, audit and command handlers

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`high`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the stage coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_3_APPLICATION_SWITCH_ORCHESTRATOR_PROMPT.md).
This is an implementation handoff prepared for owner review.

## Outcome and entry

Build reports and audit from stored current-generation facts, then implement
the explicit command handlers that 3.2 connects to the existing application.
Require Stage 2's repository, processor and input/result handoff and its
resolved owner-facing choices.

## Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/reports.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/audit.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/commands.py`

Edit: none. Delete: none.

Record the entry baseline and finish with the master's changed-file scope
proof. A needed change to a preceding file returns to its owning mini-project
before dependent work continues. Runtime evidence output is implemented here;
writing actual evidence or databases is a separate operational action.

## Exact behavior references

| Existing source | New destination and reason |
|---|---|
| [src/ck3chronicle/reporting.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:81) `build_session_report` 81–411; projection precondition 99–110; classifier payload query 124–133 | New `reports.py` reads final compact records and stored rendering. The old body requires removed representations and is not ported. |
| [src/ck3chronicle/database_audit.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:80) `audit_database` 80–861 | New `audit.py` describes current database facts without old projection/raw-block/schema assumptions or required log reopening. |
| [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:74) `_capture_error` 74–99 and calls 137/163/225/526/543 | New lightweight `commands.capture_error` handles the remaining copy-only capture callers after 3.2 disconnects old ingest/reconcile. |
| [src/ck3chronicle/command_envelope.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/command_envelope.py:1) 1–51 | Use the existing neutral command envelope. |
| [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:38) 38–140 | Use explicit configured path ownership; this task does not redesign configuration. |
| WORKPLAN 6.1 and CALLER_INDEX CLI registration sites | Exact old registrations and the destination handler for each retained command. Existing CLI edits belong to 3.2. |

## Functions and implementation steps

1. In `reports.py`, implement `build_run_report`, `list_errors` and
   `get_review_reference` using 2.1's repository reads. Use Run identity,
   contract-defined fields, counts and stored rendering. Report native-review
   metadata separately from compact approved diagnostic records.
2. Make reports independent of the original log and installed model files.
   Missing external review evidence does not erase the stored Run; present
   stored availability/reference metadata accurately. Ordinary reports do not
   recreate diagnostics from a shard or perform classification.
3. In `audit.py`, implement `audit_database` over the current schema,
   Run/record/lineage and review metadata relationships. This is the ordinary
   product audit command, not a new evaluation framework or a source-log
   reconciliation tool. It must not mutate or upgrade a database.
4. In `commands.py`, implement the handlers and registration below against
   `inputs`, `processor`, `replay`, `reports`, `audit` and `repository`.
   Import heavier processing/model dependencies inside the appropriate handlers
   so command registration and copy-only capture remain lightweight.
5. Implement `capture_error` for the current capture exceptions and operation
   failures. It must not import a removed database/provider module merely to
   reproduce the old mixed exception handler.
6. Implement `register_commands` to add the supported pipeline commands to
   the existing parser's subparsers. The root CLI continues to own capture,
   watch, doctor and observe-logging; their behavior is outside this new module.

## Proposed command contract for the Stage 2 review

The selectors below are the concrete proposal for the new handlers. Carry
forward any owner change recorded at Stage 2; do not preserve old aliases.
Resolve paths under existing configured authority. The generation's review
namespace comes from 2.1, not an independently guessed fallback path.

| Command / function | Explicit selector(s) and result |
|---|---|
| `ingest` / `cmd_ingest` | `--error-log PATH --db PATH`: protect the supplied native input and process it into the chosen current generation. |
| `process-pending` / `cmd_process_pending` | `--pending PATH --db PATH`: process exactly the selected current capture. |
| `rebuild-db` / `cmd_rebuild_db` | Repeated `--error-log PATH` plus `--destination-db PATH`: create a named fresh generation from that explicit retained-input set. |
| `runs` / `cmd_runs` | `--db PATH`: list successful current Runs. |
| `report` / `cmd_report` | `--db PATH --run RUN_ID`: report the stored Run. |
| `latest` / `cmd_latest` | `--db PATH`: report the latest stored Run, or explicitly report no Runs. |
| `errors` / `cmd_errors` | `--db PATH --run RUN_ID`: list the Run's approved compact diagnostic records. |
| `review-queue` / `cmd_review_queue` | `--db PATH --run RUN_ID`: return the Run's native shard reference and review metadata. |
| `audit-db` / `cmd_audit_db` | `--db PATH`: read-only audit of current database facts. |

A missing/incompatible database produces an explicit result rather than a
migration or guessed alternative. `rebuild-db` creates the fresh generation;
normal read commands never create one. Processing uses the selected direct
artifact through the new catalog; individual commands do not select separate
projection/classifier revisions.

Present successful Run identity/counts/review reference, duplicate results and
processing failures using the actual 2.2 result contract. Do not retain old
payload counts, category/projection fields or session-stage status as output
compatibility obligations.

## Deliverable and following work

Deliver the three new modules, the actual registered command/argument list and
handler-to-service call table. Give 3.2 the exact `register_commands` and
`capture_error` entry points. Existing `cli.py`, watcher imports and package
resources remain scoped to 3.2. Finish with the required file-scope proof.
