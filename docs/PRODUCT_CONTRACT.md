# Product contract

## Purpose

ck3chronicle answers four questions with reproducible evidence:

1. What errors occurred during this CK3 run?
2. Which repeatable semantic contracts do those occurrences represent?
3. What became new, fixed, worse, or improved between runs?
4. Which active runtime sources are relevant to investigation?

## Evidence hierarchy

1. Protected copied bytes are primary evidence.
2. The finalized manifest binds retained paths, sizes, timestamps, and SHA-256
   hashes to one content-addressed archive.
3. Canonical source blocks and occurrence rows are immutable projections of
   archived `error.log`.
4. Template classifications, categories, reports, and deltas are derived,
   versioned, and reproducible.

Derived data may be replaced by a newer approved model. Captured bytes and raw
source-block provenance may not be rewritten.

## Capture boundary

The watcher observes exact `ck3.exe` process identities. A normal capture
requires an observed absent -> running -> absent lifecycle. On exit it copies
the approved logs once to a private pending directory and publishes that
pending copy only after the complete file set is protected.

The exit path does not hash, parse, classify, or write SQLite.

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

Classification has two layers where applicable:

- L1: the stable outer semantic contract;
- L2: the ordered reason or explanation contract.

Assignments are explicit: full, independently composed L1+L2, L1-only, or
unknown. A known L1 does not authorize inventing an L2.

Key and symbol shapes such as `*_effect` and `*_trigger` may validate a slot
after contract assignment. They may not discover or choose the contract.

## Runtime mod evidence

The same-run captured `debug.log` contiguous `Mounted Data:` block will be the
only primary source for historical DLC membership and ordered active mods.

Explicit exclusions:

- extension `session.mods`;
- save-game correlation on the normal path;
- Debug Enabled/Disabled inventory;
- searches across inactive mods when resolving a session.

## Reporting boundary

Product reports query stored canonical and classified records. They never
reopen and reparse raw logs. Reports distinguish evidence, inference, and
unknown state and do not claim that a referenced mod owns or caused an error
without later resolver evidence.

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
