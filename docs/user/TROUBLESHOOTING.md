# Troubleshooting

Start with the command's findings, exit code and selected configuration. Keep
the exact database path returned by setup. The checks below help distinguish
configuration problems from incomplete evidence or valid empty results.

## Setup and launch

| Symptom | What to check |
|---|---|
| Doctor exits 2 after setup | Read each finding. Read-only write-access checks normally remain unverified; errors about required paths or models need their stated correction. |
| A CK3 folder needs attention | Check its full path and purpose. Game and logs directories must exist; optional mod/crash locations can produce warnings. Recheck edited paths before saving. |
| A command uses different settings | Pass the same `--config PATH` before the application subcommand. Omission selects `%LOCALAPPDATA%\ck3chronicle\paths.toml`. |
| Setup reports an active runtime | Stop that setup's watcher with Ctrl+C, wait, then use `runtime-stop`. Reports and ingest can start the handler again. |
| The watcher is quiet | It normally waits quietly for the configured CK3 process. Inspect its heartbeat and execution log; start CK3 in the usual way. |
| Ctrl+C fails to return | Keep the logs and avoid changing that runtime's settings. Seek help with the command, configuration path and relevant events. |

If saving settings failed after database initialization, retain the returned
database path and reported effects. Once the setup process has exited, retry with
the same roots and `.\Setup.cmd --config 'FULL PATH' --database 'EXACT RETURNED FILE'`.
Do not reset storage, delete the data directory or guess a different database.
An interrupted `.setup-lock` requires inspection of effects and confirmation that
its process exited before removing that single lock. A watcher lock file alone
does not establish an active lease; do not remove files to bypass a live lease.

## Find an expected Run

Capture protects input; successful ingestion assigns its Run ID. A
`capture_completed` event or watcher heartbeat alone does not establish ingestion.
Check the handler's terminal outcome and list Runs under the processing package.

If ingest returns `NOT_COMPLETED` and an existing Run ID, inspect its details:
the same full log content may already be stored. Deduplication preserves that
Run even when another model was requested. An unavailable temporary request
result also does not prove ingestion failed. Use
[request results and stored ingestion](CLI_REFERENCE.md#request-results-and-stored-ingestion)
and [execution logs](WORKFLOWS.md#find-and-read-execution-logs) to follow the evidence.

Raw captured logs expire according to the configured retention period, default
30 days from capture, independently of ingestion success. Stored history and
native review shards survive that cleanup. Preserve exact raw logs separately
when you need them beyond that period; stored diagnostics cannot reconstruct
the original file.

## Interpret reports and source context

| Symptom | What to check |
|---|---|
| An empty report succeeds | Check selected Run, package, preset and filters. Empty diagnostic results can coexist with unresolved native review evidence. |
| SQL and report counts differ | Compare the same scope and committed data. Display limits differ from totals; count records and occurrences separately, and avoid joins that multiply rows. |
| `latest` cannot select a Run | It requires source chronology and an explicit package. List Runs and use an exact Run ID to inspect stored evidence with unavailable source time. |
| History contains gaps | Missing/failed reads are unavailable, not zero. Processing time and Run-ID order do not replace missing source timestamps. |
| A source is unassigned | Inspect coverage, captured playset order and current file/line availability. A stored reference is a lead, not proof of causal responsibility. |
| Source filtering returns exit 3 | Required source work was incomplete. Read the structured failure and coverage; correct inaccessible roots/files or search-tool settings. |
| SQLite is busy or locked | Close long external read transactions, then retry. Keep locking enabled and leave journal/WAL files under SQLite management. |

For details, use [report interpretation](REPORT_QUERY_REFERENCE.md#reading-report-json)
and [external-read troubleshooting](EXTERNAL_DATA.md#troubleshooting-external-reads).

## Ask for help with useful evidence

Record the application version, exact command and exit code, settings path,
database and Run ID when available. Retain the relevant invocation journal and
handler events, including both `request_id` and `handler_instance`.
[Find execution logs](WORKFLOWS.md#find-and-read-execution-logs) for locations and
a PowerShell viewing example. Remove private paths or content before sharing.
Preserve original evidence; put your notes in a separate file.

[Continue to Planned Features](PLANNED_FEATURES.md) · [Manual contents](README.md)
