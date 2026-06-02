# Agent Prompt 11: Agent JSON Contracts

Implement stable JSON output contracts for agentic use.

Commands:

- `ck3chronicle latest --json`
- `ck3chronicle diff --json`
- `ck3chronicle errors --json`
- `ck3chronicle suspects --json`
- `ck3chronicle crash-status --json`

JSON outputs should be:

- compact
- deterministic
- schema-versioned
- explicit about confidence
- free of giant raw log dumps by default

Optional raw evidence retrieval should be capped.

Potential future MCP wrappers:

- `ck3_logs.latest_report()`
- `ck3_logs.new_errors()`
- `ck3_logs.fixed_errors()`
- `ck3_logs.errors_for_file(path)`
- `ck3_logs.session_diff(from_session, to_session)`
- `ck3_logs.top_fatal(limit)`
- `ck3_logs.crash_status()`
- `ck3_logs.baseline_diff(name)`
- `ck3_logs.suspects()`

Acceptance criteria:

- JSON schema version is included.
- Latest session summary is available.
- Diffs are available.
- Crash status is available.
- Suspects are available with confidence and reason.
- Output is suitable for agent context.
- Output is based on canonical issue records and enrichment tables, not raw logs.
