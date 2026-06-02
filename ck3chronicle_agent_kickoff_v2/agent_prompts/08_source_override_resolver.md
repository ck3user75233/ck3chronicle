# Agent Prompt 08: Source and Override-Chain Resolver

Implement source/override-chain resolution.

This is not a parser.

The resolver consumes file paths from canonical issue records and enriches them with source context.

Inputs:

- canonical issue records
- configured mod roots / playset roots
- base game root if configured
- load order metadata if available
- local submod name/path if configured

Outputs should include:

- referenced_file
- winning_source_name
- winning_source_type: base_game | workshop_mod | local_mod | unknown
- winning_source_path
- load_order_index
- our_submod_override: true/false
- override_chain
- recently_modified
- diff_vs_original_summary where available
- diff_vs_predecessor_summary where available
- confidence
- reason

Do not parse raw logs.
Do not generate final reports directly.
Do not modify files.

Acceptance criteria:

- Synthetic fixture mod tree can resolve a winning file.
- Our submod winner is detected.
- Upstream-only winner is detected.
- Base-game winner is detected.
- Override chain is ordered correctly.
- Output uses cautious language and confidence.
