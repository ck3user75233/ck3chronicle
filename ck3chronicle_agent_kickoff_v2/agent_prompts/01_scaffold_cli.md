# Agent Prompt 01: Scaffold CLI

You are building the initial scaffold for ck3chronicle, a standalone Python CLI tool for preserving and analyzing Crusader Kings III runtime logs.

Product code must be created under:

```text
root:repo/ck3chronicle/
```

Scratch artifacts, generated reports, temporary logs, and parser spikes must go under:

```text
root:ck3raven_data/wip/ck3chronicle/
```

Create the package skeleton, `pyproject.toml`, CLI entrypoint, and empty command handlers for:

- `doctor`
- `ingest`
- `sessions`
- `report`
- `latest --json`

Use explicit CLI options for:

- `--logs-dir`
- `--crashes-dir`
- `--archive-dir`
- `--db`

so tests do not rely on real user paths.

Do not implement parsing yet.

Do not build:

- MCP server
- VS Code extension
- background daemon
- autonomous repair
- telemetry

Acceptance criteria:

- `python -m ck3chronicle.cli doctor` runs.
- CLI has help text for all commands.
- Tests can invoke the CLI.
- `pyproject.toml` defines package metadata and dependencies.
- No CK3-specific hardcoded absolute path is required for tests.
- No large log/copy artifacts are committed.
- Return a summary of files created and commands to run tests.
