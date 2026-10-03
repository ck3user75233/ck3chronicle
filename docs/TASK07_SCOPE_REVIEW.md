# Task 07 — agreed direction and remaining choices

## Task 07E live activation - 2026-09-30 08:28 Hong Kong

Following owner authorization, the updated watcher was started hidden at
00:27:53 UTC. The previous PID was absent, its heartbeat was stale, the runtime
lease was free, and no old handler was listening. The exact configured database
passed read-only schema-3 verification. CK3 was already running, so the new
watcher attached to that process without interrupting the game.

Watcher PID 34340 (launcher 9792) observed CK3 PID 44816; a fresh heartbeat at
00:28:23 UTC confirmed `running`. Handler PID 308 reported `handler_ready`, with
instance `71d783fe8dc34ea6b4b0f7140de130b2`. Startup ingestion found all five
readable retained captures already stored and returned ordinary duplicate
non-completion. Twenty-two older inaccessible captures remain unavailable;
permissions were not changed. No watcher/handler ERROR events were observed;
bootstrap stderr was empty. Configuration, model selection and database identity
were unchanged; no reset or forced expiry was performed.

Evidence: ignored `.codex-tmp/task07e/activation.json`. Logs now use the 07E
paths in [the handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md). The attached game's
exit was subsequently observed at 01:26:28 UTC and ingestion completed at
01:26:36 UTC as Run `20260930-BYVZUV`, request
`3f5002c984d94334b65205052b4916ed`. Its merged trace is retained under
`.codex-tmp/task07e/live-session-20260930-BYVZUV/`. Capture and ingestion took
7.657 seconds, with no warning/error/contention events for that request.
Attachment after game startup does not establish complete observed start-to-exit
Trusted Run acceptance. Task 08 and
Run-result replacement remain separate. The following implementation-delivery
checkpoint predates this separately authorized activation.

## Task 07E delivered — activation remains separate — 2026-09-30

[Task 07E's handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md) documents the shared
standard-library logging owner, bounded UTF-8 JSONL files, watcher/request-ID
correlation, preparation/database timing, compact contention episodes, tracebacks
and durable bootstrap stderr. EventJournal preserves lifecycle vocabulary and
the replaceable heartbeat. Runtime logging failures do not change Run outcomes.
Future runtime code uses `runtime_logging.py`; run `tools/check_runtime_logging.py`.

Fresh verification passed **66 checks, no failures, errors or skips**, in 86.156
seconds: the 59 receiving checks were rerun alongside seven focused logging
checks, using genuine retained CK3 inputs and disposable storage. Static ownership,
isolated imports and `pip check` passed. This is distinct from the inherited
September 30 07D handoff's 59-check result. Evidence is ignored under
`.codex-tmp/task07e/`; the handoff records coverage and limitations.

The [07D API contract](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) is preserved:
one dedicated handler, one preparation thread, one database worker, exactly three
public states, all unfinished requests plus the latest 256 terminal outcomes,
`LookupError` for unavailable results, `exception_class`, and internal-only
`cleanup_unaccepted`. Watcher `ingestion_outcome_unavailable` still creates no
outcome or eviction retry. SQL/review/playset formats and ingestion/retention
semantics are unchanged. Logging does not recover outcomes after abrupt termination.

No production configuration, selection, storage, captures or live processes were
changed; nothing was committed or pushed. The unrelated dirty tree is preserved.
Next operational step: follow the 07E handoff's separate procedure to stop the
watcher at a quiet boundary, shut down the old handler for the configured file,
verify that file read-only, and start the updated watcher. Startup ingestion and
daily retention keep their existing behavior. Task 08 SQL reports, Run-result
replacement and complete Trusted Run acceptance remain separate assignments.

## Historical scope decisions (not current executable instructions)

## Live activation and database naming completed — 2026-09-29

The [operational handoff](WATCHER_LIVE_ACTIVATION_HANDOFF.md) supersedes earlier
not-activated/naming-pending entries. The updated watcher is running and five
readable retained captures are accepted into SQL. Current APIs use database
terminology and explicit schema/timestamp-named SQLite file paths; SQL/review
version is 3. The subsequent database-handler design was rejected and deleted;
replacement implementation instructions will be issued separately.

## Watcher caller delivery — 2026-09-29

The [post-publication caller](WATCHER_INGESTION_WIRING_HANDOFF.md) is implemented,
along with daily maintenance, startup submission, error-only publication after
debug failure and optional-playset receiving warnings. It is native-verified
against real SQL in disposable storage; the live watcher has not been restarted.
The owner approved the schema/UTC-initialization filename convention in the
pipeline follow-up prompt. Its implementation and the shared request queue remain
separate work. Earlier wording that these receiving decisions await approval is
superseded; no generation replay, production reset or deletion was introduced.

## Owner decisions — 2026-09-29

Superseding the earlier proposals below: missing, malformed or mismatched playset
JSON must not block otherwise valid new error-log ingestion. Report unavailable
playset details and preserve supplied JSON. The watcher must also publish a
successfully copied error log if debug copying fails. All completed captures
enter ingestion; identify and attempt outstanding unaccepted captures at startup.

Retention cadence is daily, with the approved 30 elapsed days and eligibility of
failed/unprocessed captures unchanged. Config.toml settings need sensible defaults.
Contention is waiting work, not ingestion failure. The subsequent handler design
and [former follow-up prompt](PIPELINE_QUEUED_INGESTION_FOLLOWUP_PROMPT.md) have been
retired; their queue mechanics are not current direction or awaiting implementation.
Replacement instructions will be issued separately. Database naming was delivered
as recorded above. No generation replay or production reset/deletion is authorized.

## Implementation checkpoint — 2026-09-28

The [Task 07 ingestion/retention handoff](TASK07_INGESTION_AND_RETENTION_HANDOFF.md)
supersedes the pre-implementation state descriptions below: APIs/manual command,
schema 2, manifest 2, playset storage and per-Run lineage are implemented and verified
with genuine inputs. The malformed/mismatched-playset question was put to the owner
and remains pending; the reviewable implementation proposes rejection with input
preservation. Missing playsets are accepted. Watcher wiring/live activation and
Task 08 remain separate; explicit replacement remains unimplemented follow-up work.

Updated 2026-09-28 after the owner's scope correction and the Task 07C delivery
review. This is a planning update; no runtime implementation or database deletion
has occurred. Source inspection still finds schema 1, the database-wide lineage
restriction and no product ingest command; no Task 07 completion handoff was found.

## Ingestion is one operation

The error-log-to-SQL path is implemented and exercised. Task 06 provides
`store_validated_log` as a composition example; its v45 verification script calls
the existing product APIs end to end. There is currently no product ingest
entry point or CLI command. Task 07 exposes that existing sequence, adds playset
storage, corrects per-Run version handling and supplies the retention API.

“Callable processing” was the Python function implementing ingest, not a separate
product capability. Use one ingestion implementation, called automatically after
the watcher publishes a completed capture and by one manual `ingest` command.
Use arguments to select the input and database. Capture comes first; successful
ingestion creates the SQL Run and its two-part native review shard.

Task 07 delivers ingest and retention APIs, a manual ingest command, playset
persistence and a watcher-team integration handoff. The watcher team wires ingest
after capture publication and periodic retention checks, including idle periods.
Existing classification, binding, contract, aggregation and review APIs are reused.

The owner confirmed that playset storage requires a new SQL schema version.
Playset data remains optional: watcher and manual ingestion must accept otherwise
valid logs without it, recording `playset_captured=false` and no member rows.
Unknown playset does not mean an unmodded game.

## Database policy

Store new Runs processed with new pinned components
in the same database, recording the exact component combination on each Run.
Remove the existing database-wide lineage equality restriction. Model/parser/
matcher changes do not themselves require a SQL schema change.

A SQL schema change means explicitly discard the old database and initialize the
current schema. Re-ingest retained captures through ordinary ingest if wanted.
No migrations, legacy fallbacks or backward compatibility. Opening an incompatible
schema reports the required reset without deleting the database automatically.
Escalate concerns that a change will break still-required functionality, explaining
the affected behavior and proposed resolution before making the breaking change.

Owner clarification: provide an explicit option to re-ingest the same log with a
different package, replacing its stored processing result while preserving its
Run ID. Keep only one current result. Ordinary duplicate ingestion still returns
the existing Run ID unchanged, including when another package is supplied without
the explicit replacement option.

Replacement must completely remove the old Run-owned diagnostics and install the
new set, including occurrence/accounting counts, processing lineage and both native
review files (log and manifest). Updating matching rows alone is insufficient:
a smaller replacement must leave no stale diagnostics or review evidence. Preserve
the original capture/playset facts and other Runs' data, including shared definitions
they still use. Perform SQL deletion and insertion in one transaction; coordinate
review-file replacement so failure preserves the previously accepted result.

This is production reprocessing. Comparative model evaluation remains learner-team
work and does not require database storage. The capability is an owner requirement;
implementation is not delivered or assigned, and it is not added to Task 07's
executable prompt.

**Timing recommendation:** commission a bounded pipeline/storage follow-up after
Task 07's ingest, per-Run lineage and playset interfaces are delivered, before using
production replacement. Current `Database.write_run` rejects duplicate hashes,
allocates a new Run ID and publishes into a new review directory; its failure
cleanup deliberately preserves accepted shards. Replacement therefore needs a
specific extension of the accepted-result publication/failure behavior, beyond
Task 07's ingest composition. The follow-up should prove smaller-result replacement,
preserved capture/playset and other-Run data, unchanged ordinary duplicates, and
preservation of the old accepted result on failure. It need not block watcher
wiring or SQL reports. Timing and implementation assignment remain for owner review.

## Versioned parts and current evidence

| Part | Current representation | Task 07 treatment |
|---|---|---|
| Learner | 07C retains executable distributions and new-publication learner provenance; not a runtime ingestion service. | No new ingestion-side learner ID/import or historical recovery assignment. Offline provenance remains with the learner team. |
| Model | Revision `f5cde2616f35d563118d3d32`, format/schema 5, artifact hash in package manifest. | Per-Run model identity; model format version is distinct from SQL schema version. |
| Parser | `ck3-lossless-v1.7` and exact parser hash. | Per-Run parser identity. |
| Matcher | API `ck3-native-matcher-v2`; implementation and dependencies pinned by package file hashes. | Record exact package identity/hash as well as API version; API version alone does not identify code. |
| Assignment selector | `complete-assignment-v2`, implemented in the pinned package. | Record the policy version; this is part of the matcher package, not a separate service to build. |
| Published package | `68f1ae5db205ab46afef9c4d` plus manifest hash. | Identifies the complete delivered dependency combination, including continuation handling. |
| Pipeline and Error Contract | Application revision, classifier revision, `error-contract-v1`. | Record actual runtime revisions per Run. |
| SQLite schema | `SCHEMA_VERSION = 1`, checked through SQLite `user_version` and schema metadata. | Already versioned. Advance when changing the physical storage contract, including playset tables and database metadata. |
| Playset JSON and review manifest | Both currently format version 1. | Carry producer format; advance review format when its stored structure changes. Capture application revision identifies the producer code. |

These are components and data formats, not a proposal for more services.
A new template or parser algorithm usually changes values, not SQL columns.
New stored entities, columns, relationships or constraints can require a schema
change. Task 07's playset table is a concrete example.

07C adds explicit `package_id` selection to the existing catalog loaders; omission
keeps the current default, and `selection_path` is an alternative, mutually
exclusive selector. Use `contracts.run_lineage` on the actual loaded package.
The same model can have different executable packages, so model ID alone cannot
select execution. Both retained production packages are available for the
same-database check using distinct genuine logs; ordinary ingestion of an
already-ingested hash remains a duplicate even when another package is requested.
The explicit replacement capability above is separate, not yet delivered. The 07C source/installed
verification is reported evidence, not independently rerun by this advisory review.

## Retention and preparation

Keep original error/debug logs at the watcher capture location, with a configurable
initial one-month retention period; ingestion creates no extra archives. SQL
history, stored playsets and review shards are separate from raw-log expiry.
SQL can render diagnostics and counts, but cannot restore every original timestamp
and position after aggregation.

Owner decisions in this advisory review: raw logs from all completed captures
expire by age, including failed/unprocessed captures. Initial retention is 30
elapsed days from capture time. This supersedes the earlier processed-only
recommendation. Incomplete capture staging is outside this policy. The watcher
owns automatic triggers; current maintenance cadence is daily.

## Historical recommendations — subsequently resolved

- Skip and report captures without a usable capture time rather than inventing
  their age; include this edge case in the implementation's retention proposal.
- Reject a present malformed/mismatched completed playset, preserve the capture and
  report the reason. Missing JSON remains allowed. This keeps a retry possible
  without commissioning later playset replacement on an already accepted Run.
- Propose hourly retention maintenance to the watcher team, independent of new
  captures. This is a proposed cadence, not an approved configuration default.
- Keep startup/backlog/retry handling within the watcher and the idempotent ingest
  API. The watcher team should present a concrete policy with its wiring assignment;
  no persistent queue or new resident scheduler is commissioned.

These historical proposals are superseded: invalid playsets warn and proceed,
maintenance is daily, and the dedicated handler owns ingestion coordination.

## Current task ledger

| Work | State and owner |
|---|---|
| 07C release boundary | Delivered; source/API and documentation inspected, verification campaign not rerun. No production selection change. |
| Task 07 | Delivered ingest composition, playset SQL/manifest/read API, per-Run lineage and retention. Five receiving checks passed; review findings are assigned to 07D rather than reopening this team's scope. |
| Task 07D | Delivered: owner's simplified in-memory, three-state shared handler/sole database worker; complete runtime routing, outcome reconciliation, and current handoff repair. Implemented and hardened with the 256-terminal cache, unavailable-result LookupError, internal-only cleanup and scoped exception_class field; 59 checks passed. See TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md. Live activation remains separate. |
| Task 07E | Delivered shared rotating JSONL logging, watcher/handler/preparation/worker request correlation and timing, compact contention events, tracebacks, bootstrap capture, static enforcement and operator guide. Fresh combined verification: 66 checks passed with no skips; inherited 07D evidence remains separate. See TASK07E_RUNTIME_LOGGING_HANDOFF.md. Activated 2026-09-30 at 00:27 UTC; attached to the existing CK3 process, with fresh heartbeat and handler readiness verified. Attached-session capture/ingestion verified as Run 20260930-BYVZUV; full observed-start Trusted Run acceptance remains separate. |
| Explicit Run-result replacement | Owner requirement recorded; not implemented or assigned. Recommend a bounded pipeline/storage follow-up after Task 07, preserving Run ID and original capture/playset facts, with complete result replacement and failure preservation. Task 07's executable prompt is unchanged by this clarification. |
| Watcher wiring | Existing caller and activation delivered per handoffs; current live state not rechecked. 07D integrated the shared handler client and preserved lifecycle/daily maintenance; activation on updated code is separate. |
| Tasks 08A.1 / 08A.2 | Reporting and Analysis: [08A.1 diagnostic queries/history](TASK08A_1_PROMPT.md), then [08A.2 source search/context and filter integration](TASK08A_2_PROMPT.md). Prompts split from owner-updated drafts; implementation not claimed. |
| Task 08B | Reporting and Analysis: presets, CLI, HTML/text/JSON and source appendix, consuming both 08A.1 and 08A.2 handoffs. [Owner-updated prompt](TASK08B_PROMPT.md); implementation not claimed. Syntax research is available. Audit excluded; see [split review](TASK08_SPLIT_REVIEW.md). |
| Original Task 09 | Recommend retiring its obsolete offline reconnection/deletion draft. It references removed interfaces and would delete current 07C release tools. No replacement learner task is commissioned; see TASK08_TASK09_SCOPE_PROPOSAL.md. |
| Learner follow-up | Location-stack investigation is complete; retain current representation. Historical release recovery and specialized operations require a separate owner need. |
| Trusted Run acceptance | Still outstanding after wiring and reports; library checks alone do not establish the live lifecycle capability. |

## Historical Task 07 execution order (completed)

1. Correct storage to accept per-Run component combinations; extend playset SQL,
   manifest and read APIs, with an explicit current schema version.
2. Implement one ingest operation and its manual command using completed APIs.
3. Implement the retention API under the approved eligibility/duration; verify both
   APIs with disposable copies of genuine native evidence.
4. Deliver the exact APIs, configuration, call examples, coordination and failure
   behavior to the watcher team in the Task 07 handoff.
5. The watcher team wires both triggers, with live activation separately authorized.
   Task 08 concentrates on
   SQL reports/read operations. Task 07 itself does not modify the watcher.

The implementation prompt must replace obsolete instructions in its required
reading. Historical delivery handoffs remain useful for API evidence, but their
database-wide lineage requirements are superseded by per-Run processing versions.
