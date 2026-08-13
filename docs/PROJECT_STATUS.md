# Project status

Date: 2026-08-13

Branch: `codex/ck3chronicle-reboot`

Takeover baseline: `99f98e3`

## Authority

Source behavior and the documents in this directory are authoritative. Old
kickoff packets, prototypes, architecture plans, and tests are not active
project inputs.

Historical material is recoverable from:

`C:\Users\nateb\.ck3raven\wip\ck3chronicle\codex_reboot\takeover_archive_20260813`

## Accepted foundation

- exact CK3 lifecycle observation with an event journal and heartbeat;
- copy-first pending protection after an observed process exit;
- hashing only protected pending files during finalization;
- one content-addressed immutable archive per distinct evidence bundle;
- manifest verification and transactional SQLite registration;
- canonical parsing of archived `error.log` only;
- immutable source blocks plus one-row-per-occurrence provenance;
- atomic parse and reparse persistence.

The accepted foundation is covered by the new reboot-owned suite: 13 tests as
of this status record. No inherited test contributes to that number.

## Not yet released

- empirical L1/L2 classifications in the product database;
- unknown/L1-only review queue;
- `report`, `latest`, and `errors` commands;
- pending-to-report processing command;
- session deltas, baselines, and ignore rules;
- same-run DLC and ordered active-mod persistence;
- source/override resolution and action triage;
- automatic watcher startup on user login.

## Approved learner candidate

- revision: `93196794a7e0115d`;
- SHA-256: `3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3`;
- normalizer: `ck3-empirical-template-normalizer-v4.6`;
- clusterer: `ordered-token-clusterer-v4-bounded-script-layers`.

The model is approved for versioned, revisable classification. It is not
authority to discard raw evidence or perform automatic mod edits.
