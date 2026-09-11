# Database rebuild policy discussion

Date: 2026-09-09

Status: historical conversation record; not independent implementation
authority. The current proposed architecture and deletion decisions are recorded
in [Classification pipeline recovery review](CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md)
and [Banned ideas](BANNED_IDEAS.md).

This record preserves the sidebar exchange concerning database migrations,
historical reprocessing, Git sequencing, and where execution should continue.
Tool telemetry and intermediate progress messages are omitted.

## User

Nice work on the classification pipeline recovery review. The only question I'd
raise is, our previous discussions led me to believe that the current code-base
for ingesting logs into the database is doing some kind of
migration/re-processing steps to update past log entries in situ? I have never
called for the database to have a migration tool, and would prefer it we expunge
those parts of the process and simply re-start the database and re-ingest all
the error logs anytime the schema changes. This will help keep our code base
free of bugs and easy to understand.

Please look at the facts in detail before determining the implications of my
instruction. Should there be implications for the classification pipeline
recovery mini-project, please update the documentation accordingly.

We are looking at some Git operations in the main chat to bring local and remote
into better harmony. Are there implications for this work? Do we need to do
this first or after the Git operations? Does it matter? Please explain.

Lastly, once we are ready to begin the work outlined in the classification
review, do we do that in this sidebar or should I start a new task?

## Assistant

Yes—your recollection was correct, but two separate mechanisms had become
entangled.

### What the code currently does

| Mechanism | Current behavior |
|---|---|
| Database migration | Every writable `open_db()` automatically invokes `apply_migrations()`. This can add columns, copy data into replacement tables, drop old tables, rename replacements, update schema versions, and automatically run `VACUUM`. |
| Historical reprocessing | Processing compares stored parser/model/contract versions with current versions and may replace parsing, classification, and projection results for existing runs. The CLI also exposes `--reparse`, `--reclassify`, and `backfill-session`. |

The production database is still on capture schema 3 and storage schema 2,
while the working tree expects capture 4 and storage 6. Therefore, running
current writable processing against production would attempt an in-place
migration automatically.

The earlier apparent pending-process hang was a combination of these
mechanisms:

- Processing examined the historical sessions.
- Fifteen of the 38 sessions had parser contract `1.0.0`, while the current
  parser is `1.0.2`.
- Those 15 were selected for replacement parsing because of parser lineage—not
  because schema migration inherently required reparsing.
- Missing foreign-key indexes made deletion of their old derived rows extremely
  slow.

### Revised implication

Your rebuild-only direction is sound and materially simplifies the
classification recovery:

- SQLite becomes completely derived and disposable.
- A schema mismatch fails loudly; opening the database never upgrades it.
- A schema or selected parser/model/contract change creates a fresh database
  generation.
- Verified error-log archives are replayed through only the current
  implementation.
- The old database remains untouched until the replacement passes integrity and
  reconciliation checks.
- No old-schema readers, row translators, compatibility views, migration chain,
  backfill command, historical sweep, or in-place reparse/reclassification path
  survives.
- Normal SQLite transaction journaling/WAL remains—it is crash protection, not
  schema migration.

For classification recovery specifically, the new database schema will simply
omit semantic-projection and legacy issue structures. We will not translate
their existing rows.

There is one important consequence: the current one-week raw `error.log`
retention rule is incompatible with rebuild-only databases. Database history
cannot outlive the logs needed to reconstruct it. My recommendation is to
retain exact error logs for the same horizon as the desired database history,
with compression and a bounded retention policy if necessary.

The evidence needed for rebuilding remains available:

- 38 finalized production archives, all containing `error.log` and its SHA-256.
- 22 additional finalized version-3 archives in the readable rehearsal copy.
- Thirty-seven older production manifests lack newer structured capture
  metadata, but that legacy-only metadata is mostly low-value: 37/38 termination
  values are `unknown`, 35/38 triggers are legacy/unattributed, and only one has
  an observed start time. I recommend carrying none of that through special
  conversion code and retaining the old database temporarily for forensic
  reference.

Run IDs will also be local to each rebuilt database generation. The unique
`error.log`/evidence hash provides cross-generation correlation without
inventing another stable watcher identity.

The documentation was updated in:

- [Classification pipeline recovery review](CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md#database-lifecycle-finding-and-revised-direction)
- [Banned ideas — BAN-007](BANNED_IDEAS.md#ban-007--in-place-migration-or-historical-repair-of-derived-sqlite-state)

### Git sequencing

The Git reconciliation should finish before implementation begins.

The analysis and documentation were safe to do now, but the implementation
will delete and rewrite substantial parser, database, CLI, and test surfaces. A
committed and pushed recovery checkpoint gives us an unambiguous rollback
boundary first.

At the time of this exchange, the checked-out branch and its locally fetched
upstream both pointed to `a5925fad`, but the actual reboot state—including both
documents above—was still uncommitted, and those two documents were untracked.
The main Git work should preserve and include them. No destructive clean/reset
should be used.

Git operations do not inherently affect `.ck3chronicle` runtime evidence, but a
destructive `git clean -x` could, so that operation would be inappropriate.

### Where to execute the recovery

Use a new task after the Git checkpoint, rather than continuing implementation
in this sidebar. Reference the classification review and BAN-007 explicitly.
The execution task should initially operate only on a newly named candidate
database built from verified archives; production cutover should happen only
after reconciliation and owner review.
