# Public-release readiness specification

Status: active release-policy authority as of 2026-08-31.

## Purpose

Milestone acceptance proves a capability. Public-release readiness proves that
people can obtain, install, update, operate, recover, and understand a
supported build. A public release requires both. Development tests, historical
evaluator results, and model-quality scores cannot alone qualify a release.

Trusted Run qualification uses an isolated functional setup whose required
roots are explicitly configured and validated. That is distinct from the
public-release clean-machine installation, packaging, upgrade, and support
claim in this document. Neither phrase substitutes for the other.

## Release profiles

| Profile | Capability prerequisite | Meaning |
|---|---|---|
| Alpha/preview | Trusted Run accepted | A limited supported Windows preview under the stated pre-1.0 policy. |
| Capability preview/beta | The advertised later milestone is accepted after its detailed-specification gate | Wider feedback on a precisely bounded capability/interface set. |
| Stable | Owner-selected stable boundary accepted; Action Triage remains the recommendation | Stable compatibility, documentation, migration, operational, and support promises. |

## Release identity

Every candidate records source commit, application/package version, database
schema/migration range, parser/extractor/splitter versions, model and contract
revisions/hashes, structured-output schemas, supported-command matrix,
dependency/build lock, accepted milestones/profiles, artifact hashes, and
release-readiness result.

## Required readiness checks

| Readiness ID | Alpha | Stable | Exact check |
|---|:---:|:---:|---|
| `RELEASE-INSTALL-01` | Yes | Yes | One documented Windows install path succeeds cleanly without ck3raven, WIP, private corpora, source-checkout state, or runtime network service. |
| `RELEASE-INSTALL-02` | Yes | Yes | Installed commands, model/contract package data, exact `--config` handling, the one fixed LocalAppData configuration-file location, explicit operational-root configuration, and version reporting work outside the checkout; no alternate-file or root autodiscovery/fallback is introduced. |
| `RELEASE-UPDATE-FIRST-01` | Yes | Yes | For the first public release, the supported migration/update mechanism succeeds from a frozen representative pre-release installation/database fixture, or immediate-predecessor-public-release update is explicitly marked not applicable with owner ratification. |
| `RELEASE-UPDATE-PREDECESSOR-01` | N/A for first public release | Yes from second public release | From the second public release onward, update from the immediate public predecessor preserves or safely converts supported configuration, database, retained files, and interfaces. |
| `RELEASE-UPDATE-MATRIX-01` | No | Yes | Every still-supported stable release has a documented forward path or safe export/rebuild route. |
| `RELEASE-UNINSTALL-01` | Yes | Yes | Uninstall removes application files without silently deleting user history; data removal is separately explicit. |
| `RELEASE-LOCATION-01` | Yes | Yes | Documentation and `doctor` identify configuration, database, exact-source, crash-attachment, native-review, backup, cache, and application-log locations. |
| `RELEASE-VERSION-01` | Yes | Yes | Application, database, parser/extractor/splitter, model/contract, and output versions are queryable and appear where meaning requires them. |
| `RELEASE-MIGRATION-01` | Yes | Yes | Clean initialization and supported forward migrations pass transactional interruption/rollback tests. |
| `RELEASE-MIGRATION-02` | Yes | Yes | A verified pre-migration backup or safe export/rebuild path recovers the prior accepted state. |
| `RELEASE-RETENTION-01` | Yes | Yes | Ratified finite exact-source, native-review, crash-attachment, and database defaults/overrides; both-limit behavior; run-owned-file removal; previews; pruning; compaction; and unavailable operations are documented/tested. Measurement candidates are not advertised as defaults. |
| `RELEASE-BACKUP-01` | Yes | Yes | Database plus retained source/review/attachment backup and restore succeed on a clean machine and pass hash/reference/audit checks; ordinary reports regenerate from the restored database rather than being restored snapshots. |
| `RELEASE-SMOKE-01` | Yes | Yes | Clean-machine smoke covers config-file bootstrap, explicit root entry, read-only `doctor` readiness without a current `error.log`, explicit initialization, watcher and manual/recovery capture modes, representative real normal/crash evidence, missing/unreadable/unstable/empty failure, existing-hash rejection, database reopen/reporting without raw access, one native review shard, retention previews, audit, and restore. |
| `RELEASE-RECOVERY-01` | Yes | Yes | The documented recovery path handles credible interrupted capture/commit without publishing a duplicate or contradictory successful run. |
| `RELEASE-INDEPENDENCE-01` | Yes | Yes | Static/runtime checks prove no dependency on another project, WIP tree, private evidence, or untracked model. |
| `RELEASE-COMMANDS-01` | Yes | Yes | Documentation, help, and generated inventory agree on core, advanced/developer, internal aliases, and later/provisional surfaces. |
| `RELEASE-OUTPUT-01` | Yes | Yes | Supported JSON schemas, exit codes, ordering, bounds, query metadata, and compatibility notes are published/validated. |
| `RELEASE-DOCS-01` | Yes | Yes | Quick start, explicit paths-file configuration, data management, native review shards, backup/restore, troubleshooting, limitations, privacy, and unsupported-capability pages pass link/example checks. |
| `RELEASE-LICENCE-01` | Yes | Yes | A recognized open-source licence exists and package/bundled notices agree. |
| `RELEASE-BUILD-01` | Yes | Yes | A tagged build is reproducible from the canonical repository; artifacts, tag, checksums, and notes agree. |
| `RELEASE-PRIVACY-01` | Yes | Yes | Operation is local-only/no telemetry by default and documents all local storage. |
| `RELEASE-SAFETY-01` | Yes | Yes | Clean-machine hashes prove no CK3 or mod source mutation across supported journeys. |
| `RELEASE-MODEL-01` | Yes | Yes | Bundled model/contracts have an approved promotion record under the complete candidate-independent method. |
| `RELEASE-PERFORMANCE-01` | Yes | Yes | Owner-ratified workloads for accepted capabilities pass on documented hardware with variance recorded. |
| `RELEASE-SUPPORT-01` | Yes | Yes | Platform/package matrix, deprecation policy, issue path, privacy-safe diagnostics, and data required for support are documented. |
| `RELEASE-ROLLBACK-01` | No | Yes | Failed update/migration has a tested rollback or safe restore path preserving the last supported state. |
| `RELEASE-COMPATIBILITY-01` | No | Yes | Stable command/database/output promises and deprecation windows are published and enforced. |

The first public release still must define and test a supported update
mechanism. It simply cannot update from a public predecessor that does not
exist.

## Alpha decision rule

A public 0.1 alpha may be published only when:

1. Trusted Run is accepted for the exact candidate;
2. every Alpha readiness check passes for the same application, database,
   parser/extractor, model/contract, and output revisions;
3. limitations explicitly exclude unaccepted later milestones and general
   `debug.log`/`game.log` intelligence;
4. pre-1.0 compatibility and the first-release update path are published;
5. no known defect contradicts the advertised operational database/reporting,
   review routing, retention, or crash-exclusion behavior.

## Stable recommendation

Recommend stable 1.0 after Action Triage and its exact consumed dependencies
are accepted. Selecting an earlier boundary
requires advertising the smaller outcome without implying unsupported source
or action intelligence.

## Deterministic checks versus empirical evaluation

Install, update, migration, output, transaction, retention, backup, docs,
licensing, and builds use ordinary deterministic checks. Held-out real logs
measure model coverage and false-confident assignments only. A model failure
may block that model and a release bundling it; it cannot redefine database or
report correctness.

## Current known gaps

Currently the repository has versioned packaging and substantial
implementation, but no accepted clean-machine install/update record, ratified
finite retention defaults/operations, native review subsystem, complete
backup/restore path, final command support taxonomy, corrected crash/output
migration, licence selection, or public release-readiness record.

These are planning facts, not authorization to implement or release.

## Release record

Every required check is pass, fail, owner-ratified not-applicable, or
unexecuted. Unexecuted is never pass. The record links to—not copies or
redefines—milestone acceptance and model promotion.
