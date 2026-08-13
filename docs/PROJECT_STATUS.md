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

The accepted foundation and production classifier seam are covered by the new
reboot-owned suite: 29 tests as of this status record. No inherited test
contributes to that number.

## Accepted classifier runtime

- exact reviewed model artifact promoted under `models/93196794a7e0115d`;
- whole-file SHA-256 and internal cluster-contract validation before use;
- source family is a hard classification boundary;
- ordered-token matching with conservative semantic-lead gating;
- grammar-preserving `scope:<KEY>.<KEY>` normalization;
- optional historical identity retained as `<OPTIONAL_KEY>` extraction data;
- full, independently composed L1+L2, L1-only, and unknown outcomes;
- location chains retained separately and excluded from template identity.

The production runtime has also been compared with the frozen release
evaluator across all five training-excluded logs: 194,022 semantic
occurrences. Every file reconciles exactly by full, L1+L2, L1-only, and
unknown assignment count. This is an implementation-equivalence gate; the
separate human-authored contract tests remain the semantic authority.

## Not yet released

- empirical L1/L2 classifications in the product database;
- unknown/L1-only review queue;
- `report`, `latest`, and `errors` commands;
- pending-to-report processing command;
- session deltas, baselines, and ignore rules;
- same-run DLC and ordered active-mod persistence;
- source/override resolution and action triage;
- automatic watcher startup on user login.

## Approved production model

- revision: `93196794a7e0115d`;
- SHA-256: `3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3`;
- normalizer: `ck3-empirical-template-normalizer-v4.6`;
- clusterer: `ordered-token-clusterer-v4-bounded-script-layers`.

The artifact is now hash-pinned and loadable by production inference. Database
persistence and CLI processing remain the next checkpoint. The model is not
authority to discard raw evidence or perform automatic mod edits.
