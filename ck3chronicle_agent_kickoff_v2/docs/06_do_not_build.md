# Do Not Build Yet

The following features are explicitly out of scope for MVP agent packets unless the user assigns them later.

Do not build:

- VS Code extension
- ck3lens sidebar integration
- MCP server
- background daemon
- autonomous repair
- direct mod file editing
- telemetry
- full crash dump parser
- CK3 static validator
- CWTools replacement
- CK3 Tiger replacement
- community web service
- cloud sync
- GUI application

## Also do not build

Do not create:

```text
raw error.log → one-off parser → custom final report
```

Do not let a parser:

- write final reports
- inspect Git
- resolve override chains
- decide patch recommendations
- mutate files

## Rationale

The initial goal is to create a reliable standalone CLI that preserves logs, detects crash evidence, parses issues into canonical issue records, and reports deltas.

Override-chain analysis, source context, and fixability ranking are important, but they must be layered on top of canonical issue records.
