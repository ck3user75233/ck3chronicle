# Definition of Done

Every agent task must satisfy this checklist unless the user explicitly waives an item.

## Required

1. Code implemented.
2. Tests added or updated.
3. CLI behavior demonstrated where relevant.
4. README or docs updated if user-facing behavior changed.
5. No unrelated files changed.
6. No large raw logs committed.
7. All outputs are deterministic.
8. Parser code remains side-effect-free.
9. CLI code does not contain raw SQL.
10. Missing optional CK3 logs are warnings, not fatal errors.
11. Production code goes under `root:repo/ck3chronicle/`.
12. Scratch artifacts go under `root:ck3raven_data/wip/ck3chronicle/`.
13. Final reports are generated from canonical issue records, not raw logs.

## For database tasks

- Schema initialization is idempotent.
- Schema version is recorded.
- Tests use a temporary SQLite database.
- Repository functions are used rather than direct SQL in command handlers.

## For parser/extractor tasks

- Parser accepts a file path or iterable of lines.
- Parser does not write to SQLite.
- Parser does not inspect Git.
- Parser does not copy files.
- Parser does not resolve override chains.
- Parser preserves raw evidence through hashes and samples.
- Normalization is conservative.
- Parser/extractor emits canonical issue records.
- New extractor tests include representative fixtures.

## For source/override resolver tasks

- Resolver consumes canonical issue records or file paths from issue records.
- Resolver does not parse raw logs.
- Resolver distinguishes winning file, referenced file, and probable cause.
- Resolver uses cautious language.
- Resolver includes confidence and reason where possible.

## For reporting tasks

- Reports do not dump full raw logs by default.
- JSON output is compact and stable.
- Markdown output is readable.
- Crash status is included when available.
- Ignored issues are hidden by default once ignore support exists.
- Reports consume canonical issue records.
- Reports include source/override enrichment only through resolver output.

## For workspace/context tasks

- Blame language is cautious.
- Confidence and reason are explicit.
- Referenced file and probable cause are not treated as the same thing.
