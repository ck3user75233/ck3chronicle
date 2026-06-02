# Agent Prompt 06: Reports from Canonical Issue Records

Implement latest-session reporting for ck3chronicle.

Commands:

- `ck3chronicle report`
- `ck3chronicle report --format markdown`
- `ck3chronicle latest --json`

Reports must consume canonical issue records from the database or parser output.

Reports must not parse raw `error.log` directly.

Reports should include:

- session id
- captured logs
- crash detected yes/no
- crash folder linked yes/no
- unique issue count
- top issues by severity
- top issues by occurrence count
- unclassified count
- referenced files

Reports should not dump full raw logs by default.

Acceptance criteria:

- Terminal report is readable.
- JSON report is compact and stable.
- Markdown report can be saved to file.
- Reports include crash status when available.
- Tests use fixture sessions and canonical issue records.
- Tests prove report generation does not depend on raw log parsing.
