# Source repository and backup boundary

Status: active repository policy, updated 2026-09-12.

The ck3chronicle source repository is:

`https://github.com/ck3user75233/ck3chronicle.git`

The checkout on this machine is:

`C:\Users\nateb\Documents\ck3chronicle`

The repository contains every reusable part of the product and project method.
A clean clone must not depend on another checkout, historical worktree, or
untracked local implementation.

## Tracked source

Git contains:

- product and CLI source, including watcher, capture, parsing, direct error-
  contract classification, current database schema, reporting, and audit code;
- approved model and contract revisions with their integrity metadata;
- reusable learner, review, and model-publication tools;
- current requirement-derived tests and CI configuration; and
- product specifications, architecture, plans, status, handoff, and operator
  documentation.

## Local operational data

Git does not contain:

- captured CK3 logs, crash folders, exception attachments, pending captures,
  or retained run archives;
- SQLite databases, journals, native review shards, or processing journals;
- machine-specific paths configuration;
- training or reference corpora, review workbooks, private holdouts, or
  generated evaluator results; or
- virtual environments, caches, editor settings, and build products.

These exclusions protect private gameplay evidence and keep the source clone
reproducible. Local data may live under configured ignored paths inside the
managed workspace, but its location does not make it source code.

## Backup responsibilities

The Git remote is the recoverable copy of reusable software and project method.
It is not a backup of operational evidence.

Operational backup must separately preserve the paths configuration, current
database generation, retained source logs, crash attachments, native review
shards and manifests, and the hashes and provenance needed to verify them. The
supported backup and restore contract belongs in
[`DATA_COMPATIBILITY_AND_OPERATIONS.md`](DATA_COMPATIBILITY_AND_OPERATIONS.md).

A clean-clone check must install the project, load the approved model and
contracts, initialize the current database schema, and pass current
requirement-derived verification without consulting local runtime data.
