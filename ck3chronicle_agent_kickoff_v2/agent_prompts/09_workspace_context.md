# Agent Prompt 09: Workspace Context

Implement workspace and Git context capture.

Commands:

- `ck3chronicle workspace configure <path>`
- `ck3chronicle context`
- `ck3chronicle errors --changed-files`
- `ck3chronicle errors --file <path>`
- `ck3chronicle suspects`
- `ck3chronicle report --with-context`

Capture:

- workspace roots
- Git branch
- Git commit
- dirty yes/no
- modified files
- added files
- deleted files

Use cautious likely-cause language.

Output fields should distinguish:

- referenced_file
- emitting_file
- recently_modified_candidate
- load_order_candidate
- probable_cause
- confidence
- reason

Acceptance criteria:

- Errors can be queried by file.
- New errors can be correlated to changed files.
- Reports explain why a file is suggested.
- Confidence is explicit.
- The tool does not claim certainty when evidence is only circumstantial.
