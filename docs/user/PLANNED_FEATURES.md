# Planned Features

The following describes future direction beyond application **0.0.3**. Use the
current manual's workflows for today's operations. Planning status here expresses
intent; detailed designs and delivery schedules remain to be decided.

## Planned direction

- **Snapshot export:** create a consistent portable copy of stored evidence
  for inspection and sharing at a known point in time.
- **Guided application-data backup and restore:** help preserve the related
  settings, database and separate evidence files, then recover them together.
- **Interactive investigation:** explore Runs, diagnostics and source context
  through an interactive interface. The interface framework remains a design choice.

Until snapshot and backup procedures are available, preserve the separate
evidence files you need and follow the existing
[SQLite connection and live-copy precautions](EXTERNAL_DATA.md#connection-and-writer-conditions).
Raw-log retention continues to apply independently of stored diagnostic history.

## Under exploration

**Near-match assistance for keys and tokens** could compare a missing key or
undefined token with known names to help spot typos, misspellings and nonexistent
identifiers, including in AI-generated code. It would provide leads to check
against the intended source and context. Its analytical approach remains exploratory.

Current [source lookup, content search and excerpts](ORIENTATION.md#how-source-context-fits)
already support investigations using captured playset references and present-day
files. These capabilities are described in [report queries and results](REPORT_QUERY_REFERENCE.md).

[Manual contents](README.md)
