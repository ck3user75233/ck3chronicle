# Python application interfaces

Application **0.0.3**. This advanced reference is for callers integrating with
the installed Python application. For terminal use, start with the
[command reference](CLI_REFERENCE.md); for direct external inspection, use the
[read-only SQLite guide](EXTERNAL_DATA.md).

## Configuration and setup

Configure once at application entry with `ck3chronicle.config.configure(path)`
before accessing runtime roots. Use the same explicit configuration authority
throughout the process. Root globals are lazy module attributes; application
processes retain loaded settings. [Configuration rules](CONFIGURATION_REFERENCE.md#authority-paths-and-changes)
explain selection, path resolution and restarts.

The `ck3chronicle.setup` module provides:

| Operation | Purpose and effects |
|---|---|
| `suggest_paths()` | Return editable bounded Windows Known Folder/Steam suggestions. |
| `model_choices()` | List authenticated available model choices and catalog information. |
| `prepare(path, inputs, accepted=())` | Merge and validate a preview, returning findings and proposed settings without creating state. |
| `apply_setup(path, inputs, accepted=())` | Validate, initialize storage as needed and save the selected configuration. Inspect returned effects on failure. |
| `diagnose(document, path)` | Read-only checks of a configuration document and its referenced resources. |

Input keys use the underscore names of CLI destinations. `accepted` identifies
the changed external roots the caller has reviewed, such as `root_game` or
`root_logs`. Applying alone does not accept newly selected paths. See
[setup options and results](CLI_REFERENCE.md#setup) for required paths, findings,
partial-save handling and immutable model selection. Setup refuses an active
watcher/handler and preserves existing history on repeat.

## Public database requests

Runtime clients use `ck3chronicle.pipeline.request_handler.HandlerClient`.
One database has one request queue and one serial database worker. Concurrent
clients submit work to the application's single writer.

| Interface | Purpose and effects |
|---|---|
| `HandlerClient(database).probe()` | Inspect an existing handler and its identity without starting one. |
| `submit(operation, arguments)` | Submit one supported public operation; ordinary requests can start the handler. |
| `result(ref, timeout=None)` | Retrieve the outcome for the request reference and handler instance. |
| `shutdown()` | Explicitly stop admission and shut down the existing handler; unfinished requests can be rejected. Stop the watcher before runtime maintenance. |

Use public operations and their returned data; the handler exposes no SQL
connection. A submitted ingestion request covers a whole log. Completed results
are temporarily cached; stored Run evidence remains durable. Public
`find_run_by_log_hash` locates an existing Run by full log content hash. See
[request results and stored ingestion](CLI_REFERENCE.md#request-results-and-stored-ingestion)
for the 1,024-result cache, request-instance lifetime and unavailable outcomes.

Public `resolve_review_reference` resolves stored review references within the
database's review namespace. It does not check current existence or integrity;
inspect the resolved files and compare stored size/hashes when needed. Native
review evidence stays separate from diagnostic rows. Follow the
[review-shard viewing instructions](EXTERNAL_DATA.md#locate-and-view-a-native-review-shard-separately).

[Manual contents](README.md)
