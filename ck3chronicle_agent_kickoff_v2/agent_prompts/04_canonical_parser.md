# Agent Prompt 04: Canonical Parser

Implement a pure streaming parser for CK3-style logs.

The parser must be side-effect-free.

It should accept:

- a file path, or
- an iterable of lines

and return canonical issue records.

Each issue record must include:

- schema_version
- source_log
- raw_text or capped raw_sample
- raw_block_hash
- normalized_signature
- first_line_number
- last_line_number
- category
- severity
- confidence
- primary_file
- primary_line
- primary_symbol
- message
- call_stack
- extracted_file_paths

It should detect timestamp-prefixed CK3 log lines as new blocks and attach continuation lines to the current block.

Add tests for:

- single-line errors
- multi-line script-system errors
- repeated errors with different line numbers
- localization spam
- asset/graphics errors
- descriptor errors
- empty logs

Do not write to SQLite from the parser.
Do not inspect Git from the parser.
Do not copy files from the parser.
Do not resolve override chains from the parser.
Do not generate final reports directly from raw logs.

Acceptance criteria:

- All parser output conforms to `ck3chronicle.issue.v1`.
- Multi-line script-system call stacks are captured.
- Repeated runtime IDs can be normalized without losing useful identity.
- Tests prove output schema conformance.
