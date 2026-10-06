# Banned ideas

These are designs the owner has explicitly rejected. They prevent known errors
from re-entering the product; positive requirements remain in their owning
specifications.

## BAN-001 — Treating one error log as multiple runs

Two genuine nonempty `error.log` files from different CK3 runs cannot be
byte-identical: their timestamped entries belong to different run times.

A matching full-file SHA-256 therefore means that the same captured file was
submitted or copied again. Reject it before parsing or creating another Run ID.
Do not add duplicate overrides, one-log/many-run identities, or receipt systems
to support this impossible case.

Duplicate-ingestion handling belongs to the pipeline. Reporting must not add
timestamp-based duplicate detection, Run exclusion or rejection. The owner
removed that reporting requirement on 2026-10-04; it is not a verification gap.

## BAN-002 — Historical tests defining product scope

Deleted or superseded tests do not create requirements. Every new test must
trace to a current owner-directed requirement and, where CK3 behavior matters,
representative real CK3 evidence.

## BAN-003 — Treating a finite sample as the complete template set

A finite sample establishes only the templates represented in that sample. It
cannot establish the complete set of templates CK3 may emit.

A template absent from a sample is unknown relative to that sample. It is not
thereby unclassifiable or permanently unknown; later evidence may support a
reviewed contract for it.

Do not use one sample to create an exhaustive global taxonomy, downgrade
existing supported contracts, or claim complete coverage of present or future
CK3 output. CK3 evolves, so the complete possible template set is neither known
nor expected to remain fixed.

## BAN-004 — A separate semantic-projection stage

Approved error contracts directly own their error type, typed slots,
validation, rendering, and identity rules. Do not add a second runtime catalog
or mapping stage that reinterprets classified contracts.

## BAN-005 — Unrequested legacy compatibility

Do not retain an obsolete schema, parser, handler, command, alias, adapter,
dual read/write path, or compatibility wrapper without an explicit current
owner-approved requirement.

Before removing legacy code, identify any owner-required behavior that still
depends on it. Refactor that behavior onto the current architecture as part of
the change when possible. If the required refactor cannot be completed safely
within the task, surface the dependency, its effect, and the recommended
refactor to the user.

Do not recommend retaining legacy compatibility as the solution. Existing
callers and runtime failures reveal dependencies; they do not create or
preserve product requirements.

## BAN-006 — Silent fallback

Do not silently substitute an old parser, model, schema, taxonomy,
configuration source, or broad heuristic when the intended path is absent or
fails. Fail clearly or return the explicit current outcome required by the
owning specification.

Unknown, provisional, and review-routed results are valid outcomes, not
fallbacks.

## BAN-007 — In-place migration of derived databases

SQLite has one explicitly versioned current schema. A schema change requires
explicitly discarding the old database and initializing the current schema.
Opening an incompatible database must not silently reset it.

New compatible models, parsers and matchers can process new logs into the same
database. Record their exact versions per Run; do not require a database-wide
processing-version match or a reset just because processing components changed.

Do not maintain schema-migration chains, old-schema readers, compatibility
views, dual writes, backfills, or historical row-repair paths. Ordinary SQLite
transaction recovery remains required.

## BAN-014 — Database generation replay

Do not implement named processing generations, parallel-generation rebuilds,
replay/cutover workflows or dedicated replay/rebuild commands. After an owner-chosen
whole-database reset, reprocess retained logs through the same ingest operation.
Keep schema versioning and per-Run processing provenance.

The owner requires an explicit option to re-ingest the same log with a different
package and replace its processing result while preserving its Run ID. Keep one
current result; ordinary duplicate ingestion still returns the existing Run ID
unchanged. Replace all old Run-owned diagnostics, counts, processing lineage and
native review log/manifest; preserve original capture/playset facts and other Runs.
SQL deletion/insertion must share one transaction, with review-file replacement
coordinated so failure preserves the previously accepted result. This bounded
production reprocessing is permitted; generation replay remains banned. Delivery
is unassigned and outside the current Task 07 prompt; see the
[database policy and task ledger](TASK07_SCOPE_REVIEW.md#database-policy).
Comparative model evaluation remains learner-team work without database storage.

## BAN-008 — Requiring 100% classification coverage

Unclassified, provisional, and low-confidence errors are expected product
outcomes. Trusted Run requires every recognized emission to be accounted for;
it does not require every emission to receive a confident classification.

Do not invent classifications, weaken validation, or make 100% classification
coverage a release requirement. The product may be useful and releasable below
100% when unresolved evidence is preserved and reviewable.

## BAN-009 — Treating 100,000-entry logs as a special test category

CK3 itself stops writing additional timestamped `error.log` entries when its
100,000-entry producer limit is reached. That fact corrects the false inference
that ck3chronicle truncated or corrupted such a file; it does not create a
special ck3chronicle input class or user requirement.

Do not create or require a 100,000-entry-specific test, fixture, stress case,
benchmark, performance threshold, acceptance gate, evidence-set member, or work-
package precondition. Do not treat that count as having special testing or
requirements significance. Parsing, classification, storage, review routing,
reporting, and audit must not branch solely because a log has that exact entry
count. Every valid `error.log` must instead be processed completely as supplied,
regardless of size. Every recognized emission must be accounted for through
recovered diagnostics, preserved review evidence, or an explicit parser
failure.

## BAN-010 — Unrequested chain-of-custody and marker-validation work

Do not initiate chain-of-custody systems, tamper audits, evidence manifests,
signed receipts, recurring rehash procedures, identity checkpoints, or similar
evidence ceremony unless the owner has explicitly requested that capability.

Do not create tests, validation activities, gates, or acceptance conditions
around content hashes, IDs, counts, timestamps, manifests, schema fingerprints,
or other markers merely because those markers exist. A marker named by an
owner requirement may be used and checked only for the purpose that requirement
defines. Its presence does not authorize a broader integrity regime.

## BAN-011 — Turning agent conclusions into requirements

Historical facts, existing code, existing tests, prior plans, validator
suggestions, retained evidence, measured timings, archive counts, and ordinary
engineering preferences do not create product requirements.

Do not turn any of them into a mandatory test, threshold, gate, precondition,
protocol, artifact, or architecture. Every such obligation must serve an
owner-defined outcome. When the owner has not chosen among materially different
designs, present the choice instead of silently promoting one to a requirement.

## BAN-012 — Treating old pipeline output as the correctness oracle

Do not require a replacement pipeline to reproduce the old pipeline's
classifications, coverage, counts, or dispositions mechanically. The old
pipeline contains deprecated and incorrect stages, so a difference—including
lower classification coverage—may be a correction.

Evaluate substantive differences against the source emissions and the current
owner-defined behavior. Block only an unexplained loss or regression against
that behavior, not a failure to preserve superseded output.

## BAN-013 — Unrequested recovery and publication machinery

Do not introduce processing journals, hash chains, active-attempt pointers,
Run-ID reservation or reuse protocols, publication state machines, signed
receipts, exhaustive crash-injection matrices, or similar recovery machinery
without an explicit owner requirement that needs it.

Existing or historical machinery does not justify preserving or expanding it.
Use ordinary filesystem and SQLite guarantees where they satisfy the stated
product behavior; return a genuinely unresolved design choice to the owner.
