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

SQLite contains rebuildable derived state. When a schema, parser, splitter,
model, or contract change alters stored meaning, build and validate a fresh
database from retained captures and cut over explicitly.

Do not maintain schema-migration chains, old-schema readers, compatibility
views, dual writes, backfills, or historical row-repair paths. Ordinary SQLite
transaction recovery remains required.

## BAN-008 — Requiring 100% classification coverage

Unclassified, provisional, and low-confidence errors are expected product
outcomes. Trusted Run requires every recognized emission to be accounted for;
it does not require every emission to receive a confident classification.

Do not invent classifications, weaken validation, or make 100% classification
coverage a release requirement. The product may be useful and releasable below
100% when unresolved evidence is preserved and reviewable.
