# Banned ideas

This list prevents disproven design artifacts from re-entering product scope.
It does not replace positive requirements in the owning specification.

## BAN-001 — Byte-identical error logs as distinct real CK3 sessions

CK3 timestamps are part of the `error.log` bytes. A matching full-file SHA-256
means the same captured file was submitted twice through operator or tool error.
Reject it loudly before parsing or inserting a new run.

Do not build forced-duplicate paths, duplicate overrides, receipt systems,
one-evidence/many-run identities, reporting scenarios, or acceptance machinery
for byte-identical logs. This ban does not apply to repeated diagnostics inside
one log, parser cases with separate headers sharing a timestamp value, CK3
messages about duplicate keys, or learner-side deduplication of training input.

Provenance audit:

- `14ed0dd` and `3ca2ae2` began with the legitimate content-hash guard, although
  the latter also introduced an override.
- `934cd6d` supplied the pivotal false premise: a test simulated two process
  exits around the same unchanged fixture and required one content bundle to
  represent two observations.
- `af1d583` promoted that fixture artifact into separate run/receipt/file-origin
  identities. `bc94c05`, `e5cee1a`, `76fb2d5`, and `bae136e` then reinforced it
  in evaluator, reporting, crash, and audit surfaces.

Those commits remain ordinary historical Git evidence; they are not current
authority. The reboot working tree deletes their receipt modules and provenance
tests/docs, removes the override, replaces the second observation-derived ID
with one `run_metadata` row keyed by the existing Run ID, and removes the
unused `run_file_origins` projection. Publishing the reboot commit will remove
those active artifacts from the remote branch tip without rewriting history.

## BAN-002 — Pre-reboot tests as product authority

The pre-reboot test and evaluator tree is deleted wholesale. Do not restore,
port, rename, or translate its cases into new checks. A new test must trace to
an active owner-directed requirement and, where CK3 behavior matters, to
representative real CK3 evidence.

## BAN-003 — A finite calibration sample as exhaustive runtime taxonomy

A selected calibration sample is evidence for the contracts it actually
reviews. Absence from that sample is not evidence that another learned template
is semantically unknown. Do not generate a total runtime catalog by assigning
`unclassified` / `unknown` to every model contract the sample did not touch.

The historical 252-row sample may contribute traceable reviewed decisions, but
it is not the complete CK3 error-type inventory and cannot downgrade a full or
partial structural match. Claim-specific calibration and evaluation remain
separate from runtime authority.

## BAN-004 — A separate semantic projection or mapping stage

An approved error contract contains its hierarchical error type, typed slots,
validation, rendering, and identity rules directly. Do not add a second
catalog or runtime stage that "projects" or "maps" a recognized contract into
category/type/tags, and do not retain `project_classification_run()` or a
projection-run database identity.

Contract authoring may review what a template means. That review changes the
approved contract; it is not a second runtime interpretation layer.

## BAN-005 — Unrequested legacy compatibility

Do not retain superseded parsers, extractors, schemas, commands, aliases,
adapters, dual reads/writes, or deprecated internal concepts merely because an
older implementation once exposed them. No current caller and no active
owner-directed requirement means removal, not a compatibility wrapper.

An explicitly approved, bounded one-time capture/archive evidence conversion
is permitted only with a named target, rollback boundary, and removal
condition. It does not authorize an in-place database migration, a permanent
alternate runtime, or an in-repo archive of retired source.

## BAN-006 — Silent fallback to a superseded or inapplicable path

Do not silently substitute an old taxonomy, parser, model, schema view, input
source, configuration root, or broad regex when the intended current path is
absent, unsupported, or fails. Fail loudly, or produce the explicit current
outcome required by the owning contract.

An explicit `unknown`, provisional result, native-review routing, transactional
rollback, or deliberately specified recovery action is not a banned fallback.
Those are named product outcomes. The banned behavior is an undeclared
alternate path that makes obsolete or weak behavior appear successful.

## BAN-007 — In-place migration or historical repair of derived SQLite state

SQLite is a disposable derived database. Do not retain a schema-migration
chain, old-schema reader, compatibility view, dual write, row translator,
backfill command, contract-mismatch sweep, or explicit reparse/reclassification
route that updates historical derived rows in an existing database generation.

An existing database must match the one current schema exactly or fail loudly.
When a schema, parser, splitter, model, or error-contract revision changes
persisted historical meaning, build a separately named fresh database from the
verified retained capture archives, validate it, and cut over explicitly. Keep
the previous database unchanged as rollback evidence until acceptance.

Fresh schema initialization, full archive replay, and a verified file-level
cutover are not migrations. Normal SQLite transaction journaling/WAL is also
not banned; it provides crash safety within one database generation and does
not translate an old schema.
