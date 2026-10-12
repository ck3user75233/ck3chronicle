# Pipeline completed-result cache — next application candidate

2026-10-08. Owner-issued Pipeline follow-up; coordination on TREK-9, including
Docs CMT-121. Delivered in repository source and a fresh application wheel for
the next production candidate. This does not update the externalized Windows C9
installation or activate production.

## Exact change and contract

`src/ck3chronicle/pipeline/database_handler.py::_Handler._finish` changes the
completed-result eviction threshold from 256 to **1,024** and adds a scope comment.
An AST comparison against the saved pre-change source confirms that this numeric
bound is the only executable change made by this follow-up. Pre-existing Task 10
identity/configuration work in the same file is preserved.

Each entry represents one whole public operation, including ingestion and queries.
One ingestion's internal hash lookups/write do not create extra entries; a query's
diagnostic rows do not create extra entries. Both `COMPLETED` and `NOT_COMPLETED`
terminal outcomes count. Completion order controls eviction; lookup does not
refresh it. Outstanding requests remain in `requests` outside `terminals`, and
only an ID removed from `terminals` is evicted from `requests`.

The cache is temporary execution state. Persisted SQLite Run metadata, including
the full log content hash, is authoritative evidence of ingestion. Eviction changes
neither Run records nor hash deduplication. An unavailable result alone proves
neither that ingestion failed nor that no Run exists; use the existing public
`find_run_by_log_hash` lookup to inspect persisted evidence. It does not reconstruct
the old request outcome. Raw-log retention is independent and unchanged.

## Candidate artifact

Wheel: `.codex-tmp/pipeline-cache-1024/application/ck3chronicle-0.0.2-py3-none-any.whl`

- SHA-256: `94987fb06eeac685eb5b57a87edc41e58da1df9730ff8bf15ba7a023750ab489`
- Size: 2,804,999 bytes; 627 ZIP members.
- Compared with the received 10A.1 wheel `2de516e0...`, only the handler Python
  member, `METADATA` and `RECORD` differ. Handler bytes equal repository source.
  Metadata includes pre-existing README manual/configuration corrections.
- All 453 packaged shared-resource members, including retained model/Learner
  payloads, are byte-identical. No models were rebuilt or reselected.
- Existing 0.0.2 version is retained; the exact wheel hash identifies this
  candidate. Earlier artifacts and their receipts remain intact.

Build recipe/output and artifact comparison are in ignored
`.codex-tmp/pipeline-cache-1024/{build.py,build.log,artifact.json}`. This wheel has
not been installed or received as a new Windows distribution. Future source
builds inherit the repository source change; C9 continues to describe its own
256-result artifact until an actual replacement is installed.

## Verification

Executed using `.venv/Scripts/python.exe -B` and the real public `HandlerClient`
against the existing isolated 10A.1 database
`.codex-tmp/task10a1/release/data/runtime/ck3chronicle-schema3-20261008T001346Z.sqlite3`.
Its two genuine stored Runs were reused; no history, diagnostic scenario, mock
client, failure or contention was manufactured.

- **1,027 public operations passed.** Genuine duplicate ingestion was result 1;
  a two-Run query was result 2; the genuine 1,066-diagnostic-row query was result 3.
  Another 1,021 genuine Run reads filled the completed cache to 1,024.
- Result 1 remained available at 1,024 completions. The next public content-hash
  lookup evicted result 1; `status`, `wait` and `result` all raised the existing
  `LookupError`. Result 2 remained available. Reading result 1 before eviction
  did not refresh its completion order.
- Duplicate ingestion after eviction still returned `NOT_COMPLETED`, the same
  Run `20261008-VZP1CG` and hash
  `5a7b93d8ee374c60f767593631713eaf8719004ba4f9cf33e7eb5d812dbec629`.
  Final `list_runs` exactly matched the original two stored Run records.
- All 13 database/capture/review evidence-file hashes remained unchanged.
  The task started its own handler against this isolated database and verified
  shutdown afterward. Production services were untouched.
- Runtime logging ownership check, source/test syntax and scoped diff checks pass.
  The existing hardening tests' 256/258 expectations were corrected to 1024/1026;
  their synthetic/forced-failure scenarios were not executed or expanded.

Exact recorder/results: `.codex-tmp/pipeline-cache-1024/{verify.py,verification.json}`.
Original genuine ingestion, successful storage, playset and model-selection
evidence is reused from `.codex-tmp/task10a1/release/supplement.json` and the
[10A.1 handoff](PIPELINE_HANDOFF.md); unchanged executable-byte correspondence
supports that reuse, not a claim of fresh successful ingestion.

**Limits:** normal completed-result eviction is exercised. Outstanding-request
exclusion is verified by source inspection and the exact AST comparison retaining
the admission/completion/eviction algorithm. Simultaneous eviction while a request
is outstanding, an existing waiter returning after lookup eviction, and a new
successful ingestion across the cache boundary remain unexercised. No fault
injection, synthetic history, full lifecycle, installation or production activation
is claimed. No failed product check occurred.

## Continuation

Pipeline source delivery is complete. Launch & Distribution can consume this
exact wheel for the next candidate and update release-specific documentation only
after identifying that replacement. C9 documentation's 256 limit remains accurate
for C9; its statement that Pipeline delivery is pending can now link here.
The separate CMT-106 CLI-help/GUI-reference correction remains outside this bounded
cache change. No source commit or production publication was performed.
