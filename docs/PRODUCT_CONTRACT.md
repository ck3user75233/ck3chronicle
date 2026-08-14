# Product contract

## Purpose

ck3chronicle answers four questions with reproducible evidence:

1. What errors occurred during this CK3 run?
2. Which repeatable error templates do those occurrences represent?
3. What became new, fixed, worse, or improved between runs?
4. Which active runtime sources are relevant to investigation?

## Evidence hierarchy

1. Protected copied bytes are primary evidence.
2. The finalized manifest binds retained paths, sizes, timestamps, and SHA-256
   hashes to one content-addressed archive.
3. An immutable run receipt records each observed CK3 lifecycle separately
   from the deduplicated archive, including normal/crash/unknown termination
   provenance.
4. Canonical source blocks and occurrence rows are immutable projections of
   archived `error.log`.
5. Template classifications, categories, reports, and deltas are derived,
   versioned, and reproducible.

Derived data may be replaced by a newer approved model. Captured bytes and raw
source-block provenance may not be rewritten.

SQLite normalization may store identical decoded raw blocks or identical full
classifier payloads once and reference them from many independently countable
rows. This is storage deduplication only: source blocks, canonical occurrences,
and semantic assignments retain separate ordered provenance. Compact integer
keys never replace the manifest SHA-256, raw-block SHA-256, line span, run
identity, or evidence-bundle identity used to verify evidence.

Compact storage is the default implementation and requires no user-directed
workflow. Migration of an older schema is automatic. Physical page reclamation
follows the committed migration and integrity checks on its first safe database
open; it is not a product capability or recurring operator obligation.

## Capture boundary

The watcher observes exact `ck3.exe` process identities. A normal capture
requires an observed absent -> running -> absent lifecycle. On exit it copies
the approved logs once to a private pending directory and publishes that
pending copy only after the complete file set is protected.

The exit path does not hash, parse, classify, or write SQLite.

The watcher may compare directory names and metadata in the sibling CK3
`crashes` directory to classify an observed termination as normal, crash, or
unknown. Crash-log hashes are calculated only during deferred processing.
Crash-folder `error.log`, `debug.log`, and `game.log` files that exactly match
the protected live copy are attributed but not copied again. A differing crash
version is preserved separately and linked to the run.

## Canonical issue stream

Only archived `error.log` is a canonical issue stream. Other logs remain
evidence with separate purposes.

Every timestamped `error.log` block is stored exactly once and produces at
least one explicit occurrence or unknown disposition. Silent drops are not
permitted.

## Template identity

Template identity is based on source family plus ordered semantic content.
Timestamps, keys, locators, paths, line numbers, and location chains never
create a new template.

Normalization recognizes strong locator grammar before template learning or
assignment. Explicit file/line forms, script-location chains, and equivalent
path/line structures are retained as typed `<LOCATOR>` evidence rather than
left as generic `<SLOT>` candidates that can be confused with keys. Ambiguous
text remains unresolved and the raw occurrence remains authoritative.

Classification may have two semantic template layers:

- L1: the stable outer error template;
- L2: an optional stable ordered reason/explanation subtemplate.

Assignments are explicit: full, independently composed L1+L2, L1-only, or
unknown. A known L1 does not authorize inventing an L2. Highly variable
bracketed detail may remain a structured reason slot on an L1 template rather
than becoming a large collection of low-value L2 templates.

A template contract is the machine-readable extraction and validation rule
attached to a template: slot order, `<KEY>`, `<OPTIONAL_KEY>`, `<LOCATOR>`,
structured relationships such as `<KEY>.<KEY>`, and optional/repeating shape.
It is not a synonym for the error template itself. A useful L1 template may
exist while some detailed slot typing remains unresolved.

Key and symbol shapes such as `*_effect` and `*_trigger` may validate a slot
after template assignment. They may not discover or choose the template.

## Runtime mod evidence

The same-run captured `debug.log` contiguous `Mounted Data:` block will be the
only primary source for historical DLC membership and ordered active mods.
Its exact archived file row, line range, byte range, raw-block SHA-256,
candidate count, and termination evidence are stored. Runtime context is
explicitly one of complete, partial, absent, malformed, truncated, or
ambiguous. Only complete context authorizes active-root source resolution.

The preceding DLC/Mod inventory is optional enrichment. Names, descriptor
paths, counts, and mismatch warnings are stored and reported separately; they
cannot add, remove, reorder, or rename an identity in the authoritative mount
projection.

Explicit exclusions:

- extension `session.mods`;
- save-game correlation on the normal path;
- Debug Enabled/Disabled inventory as a membership authority;
- searches across inactive mods when resolving a session.

## Reporting boundary

Product reports query stored canonical and classified records. They never
reopen and reparse raw logs. Reports distinguish evidence, inference, and
unknown state and do not claim that a referenced mod owns or caused an error
without later resolver evidence.

## Empirical logging observation

The optional logging-progress observer is separate from capture and reporting.
It may describe an exact-100,000 boundary only when `error.log` remains stable
at that timestamp-header count while the same observed CK3 process remains
alive and `game.log` advances. Process existence or a 100,000-count archived
file alone is insufficient. The observation does not prove that CK3 attempted
to emit additional errors; it establishes that the game session and another
log stream continued beyond the stable error boundary.

Per-poll progress and heartbeat journals are temporary diagnostics. They are
not canonical evidence or database records. After an observation closes, only
the bounded lifecycle/result summary is eligible for normal retention; verbose
diagnostics use bounded retention and may be discarded.

## Source-observation boundary

Source observations are derived at processing time, not captured at CK3 exit.
They are therefore timestamped observations of the current filesystem projected
through the session's authoritative recorded runtime roots; they are not
backdated claims about source bytes at game time.

Source observation is optional and is not invoked by the core
`process-pending` workflow. When explicitly performed, each referenced file
instance is read and SHA-256 hashed once for its first session/path observation,
then the stored observation is immutable. Inactive mod roots are never searched.
Exact-relative-path file replacement and domain-specific definition merging are
separate layers. Domain adapters remain deferred and cannot block database
ingestion, canonical parsing, classification, or reporting.

## Database-audit boundary

Database audit is read-only. The standard audit reconciles archive/session
membership, manifest aggregates, stored parser counters, canonical totals,
classification counters, runtime context, and relational provenance. It also
independently streams archived `error.log` bytes and counts timestamped block
headers without invoking the production parser. Deep audit
additionally reconciles every source-block and issue-signature distribution and
is explicitly opt-in because retained raw blocks make a full scan expensive.

An audit warning remains visible but does not make a structurally consistent
database unusable. An audit error means the affected evidence or derived state
must not be represented as fully accepted until repaired or regenerated.
