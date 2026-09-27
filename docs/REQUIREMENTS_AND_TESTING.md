# Requirement, invariant, and test traceability

Status: active requirements and verification authority as of 2026-09-08.

## Identifier policy

- Requirements: `REQ-<DOMAIN>-<NUMBER>`.
- Invariants: `INV-<DOMAIN>-<NUMBER>`.
- Milestone acceptance: `<MILESTONE>-<DOMAIN>-<NUMBER>`.
- Public-release checks: `RELEASE-<DOMAIN>-<NUMBER>`.

Numbers order items only within a semantic domain; they do not encode roadmap
position, candidate, or release status.

Only Trusted Run currently has detailed requirements and acceptance IDs.
Later milestone names are high-level groups until their separately ratified
specifications define individual requirements/checks. No placeholder ID range
is authority.

## Trusted Run requirement catalog

The exact statements are in `TRUSTED_RUN_SPEC.md`.

| Domain | Individually defined requirement IDs | Subject |
|---|---|---|
| Configuration | `REQ-CONFIG-001` through `REQ-CONFIG-007` | Exact `--config` or one fixed LocalAppData bootstrap, one explicit user paths file, central root authority, initialization-before-DB order, mode-correct read-only diagnosis, fail-closed damage, and no discovery/fallback. |
| Database initialization | `REQ-DATABASE-001` | Initialize only after configured roots validate; idempotent empty-root setup. |
| Acquisition | `REQ-CAPTURE-001` through `REQ-CAPTURE-004` | Observed start-to-exit trigger, one post-exit copy attempt, and copy-first publication. |
| Content-hash guard | `REQ-CONTENT-HASH-001`, `REQ-CONTENT-HASH-002` | Every Run ID retains its `error.log` hash; every ingest route rejects an existing hash before registration/parsing, with no override. |
| Input boundary | `REQ-INPUT-001` through `REQ-INPUT-005` | Missing/unreadable/unstable/empty source fails; genuine nonempty zero-diagnostic CK3 input succeeds; the watcher is not an arbitrary fabricated-input queue; every valid log is processed completely as supplied regardless of size. |
| Crash | `REQ-CRASH-001`, `REQ-CRASH-002`, `REQ-CRASH-003`, `REQ-CRASH-004` | New-folder signal, root exception, principal-log exclusion, no inferred stage. |
| Exception retention | `REQ-EXCEPTION-RETENTION-001` | Configurable finite policy, no active numeric default before measurement/owner decision, preferred shard-or-run-prune relationship, and same-workflow removal when the run is pruned. |
| Run identity | `REQ-RUN-IDENTITY-001`, `REQ-RUN-IDENTITY-002` | One successful run per observed lifecycle or explicit manual/recovery capture; capture mode/time and honest lifecycle facts. |
| Recovery | `REQ-RECOVERY-001`, `REQ-RECOVERY-002` | Atomic/idempotent pipeline and per-run failure isolation. |
| Emission recognition | `REQ-LOG-EMISSION-001`, `REQ-LOG-EMISSION-002`, `REQ-LOG-EMISSION-003`, `REQ-LOG-EMISSION-004` | Header/continuation boundary, identical timestamps, no-silent-loss, counters. |
| Multi-error | `REQ-MULTI-ERROR-001`, `REQ-MULTI-ERROR-002`, `REQ-MULTI-ERROR-003` | Reviewed source-specific splitting and no permanent parent model requirement. |
| Diagnostic identity | `REQ-DIAGNOSTIC-IDENTITY-001`, `REQ-DIAGNOSTIC-IDENTITY-002` | Meaning-bearing identity and aggregation. |
| Classification | `REQ-CLASSIFICATION-001`, `REQ-CLASSIFICATION-002`, `REQ-CLASSIFICATION-003`, `REQ-CLASSIFICATION-004` | Approved contracts, compact records, review routing, lineage. |
| Database | `REQ-DATABASE-001`, `REQ-DATABASE-002`, `REQ-DATABASE-003`, `REQ-DATABASE-004`, `REQ-DATABASE-005` | Operational initialization/reopen/migration, compact data, review separation. |
| Native review shard | `REQ-REVIEW-SHARD-001` through `REQ-REVIEW-SHARD-003` | Exactly one native shard per successful run, native provenance, lightweight DB metadata, and transactional finalization. |
| Reporting | `REQ-REPORT-001` through `REQ-REPORT-004` | On-demand database-only reports, metadata, determinism, and review debt/availability. |
| Source-dependent operations | `REQ-SOURCE-DEPENDENCY-001` | Only explicitly raw-dependent operations care whether raw source remains. |
| Audit | `REQ-AUDIT-001` | Read-only integrity/counter/reference audit. |
| Source retention | `REQ-SOURCE-RETENTION-001` | Configurable one-week exact `error.log` default. |
| Database retention | `REQ-DATABASE-RETENTION-001`, `REQ-DATABASE-RETENTION-002`, `REQ-DATABASE-RETENTION-003` | Time/size limits, whole-run transactional pruning, compaction. |
| Review-shard retention | `REQ-REVIEW-SHARD-RETENTION-001`, `REQ-REVIEW-SHARD-RETENTION-002` | Independent finite time/size policy, FIFO deletion, truthful availability; 90-day/2-GiB measurement candidate only, pending evidence and later default decision. |
| Backup | `REQ-BACKUP-001` | Database and retained-file backup/verified restore. |

Cross-cutting ratified authorities must also define standalone operation,
source read-only safety, local privacy/no telemetry, model promotion, public
release separation, and requirements-first test authority.

## Invariant catalog

| Invariant ID | Normative statement |
|---|---|
| `INV-STANDALONE-001` | Core acquisition, processing, reporting, recovery, retention, and backup depend on no other project, integration, private corpus, or untracked file. |
| `INV-CONFIG-001` | The paths file is opened only by exact `--config` or one fixed LocalAppData location; every operational root then comes only from that file through one central authority. Alternate-file/root search, inference, and fallback are forbidden. |
| `INV-LIFECYCLE-001` | Only one observed configured CK3 start-to-exit lifecycle may trigger one automatic capture and one processing attempt. |
| `INV-CAPTURE-001` | Live root `error.log` is protected before hashing, database work, interpretation, or enrichment. |
| `INV-PUBLICATION-001` | Acquisition is complete or explicitly failed/incomplete; partial bytes are never success. |
| `INV-CONTENT-HASH-001` | Every ingest route rejects a full-file `error.log` hash already attached to a Run ID before registration or parsing and provides no override. |
| `INV-INPUT-VALIDITY-001` | Automatic acquisition reads the configured Paradox-managed live `error.log`; missing, unreadable, unstable, or empty capture cannot be success. Arbitrary fabricated-input robustness is outside the watcher contract. |
| `INV-RUN-IDENTITY-001` | Each successful observed lifecycle or explicit manual/recovery capture has one run identity and chronology; manual mode/time are recorded and unobserved lifecycle facts remain unknown. |
| `INV-CRASH-001` | Only a new associated timestamped crash folder is affirmative crash-folder evidence; pre-existing folders and crash artifacts alone do not create or alter a run. |
| `INV-CRASH-002` | Crash-folder principal logs are never opened or used as input, authority, alternate storage, schema/report meaning, or positive test expectation. |
| `INV-CRASH-003` | No inferred lifecycle stage is persisted/emitted as observed fact. |
| `INV-EMISSION-COMPLETENESS-001` | Every recognized emission yields recovered diagnostic(s), routes to the run's native review shard, or produces explicit parser failure; silent disappearance is zero. |
| `INV-MULTI-ERROR-001` | Multiple diagnostics require an approved source-specific grammar; a long message is never generically guessed apart. |
| `INV-RECONSTRUCTION-001` | For an accepted structural parse, template plus ordered slot values reconstructs the originating emission exactly or under one explicitly enumerated narrow normalization contract. |
| `INV-STRUCTURE-001` | Approved templates represent recurring structure and must not rely on degenerate per-message templates or unjustified broad merges. |
| `INV-DIAGNOSTIC-IDENTITY-001` | Aggregation occurs only when every approved meaning-bearing identity field agrees. |
| `INV-CLASSIFICATION-001` | Similarity nominates, reviewed typed validation authorizes, and unsupported input routes conservatively. |
| `INV-REVIEW-SEPARATION-001` | Low-confidence/provisional/unresolved native payload resides in the bounded file-based review subsystem, not the diagnostic-record payload. |
| `INV-LINEAGE-001` | Stored/reported meaning names the application, schema, parser/extractor, model, and contract revisions needed to interpret it. |
| `INV-TRANSACTION-001` | Mutation exposes prior accepted or complete new truth, never contradictory partial truth. |
| `INV-REPORTING-001` | Reports query the database on demand, never access raw logs, and do not require routine snapshot persistence. |
| `INV-OUTPUT-001` | Supported output is versioned, deterministic, bounded, and semantically consistent across human/structured views. |
| `INV-READ-ONLY-001` | `doctor`, query, preview, and audit do not mutate; no product journey mutates CK3/mod source. |
| `INV-RETENTION-001` | Source, review, and database stores have finite configurable policies; pruning is truthful, audited, and reference-safe, and deleting a database run recoverably removes every solely owned source/attachment/shard unless separately exported/promoted. |
| `INV-OBSERVATION-001` | Observation, derived interpretation, correlation, confidence, and recommendation remain distinguishable. |

The test-authority rule is project governance, not a product invariant: tests,
evaluators, fixtures, historical ceilings, and candidate results do not create
scope. Claim-specific held-out work must keep its discovery/evaluation evidence
separate by content hash, but a universal immutable-role registry is not a
product invariant.

## Four verification lanes

| Lane | Purpose | Blocking role |
|---|---|---|
| Deterministic product regression | Fast proof of boundaries, identities, splitting, aggregation, schemas, transactions, review routing, retention, and fixed reviewed contracts | Blocks implementation merge on regression; cannot accept a milestone alone. |
| Empirical template review | Real-corpus coverage, reconstruction, compactness, split/merge review, discovery/saturation, stability, and direct human inspection | Informs model review/promotion; a held-out subset blocks only when the owner commissioned a specific blocking claim. |
| Milestone acceptance | Full operator outcome plus every ratified requirement-derived check for one candidate | Accepts only that named milestone. |
| Public-release readiness | Installation/update/docs/migration/retention/backup/build/support/privacy on clean systems | Allows publication of already accepted capabilities. |

Independent review may audit any lane. Blind/private custody is relevant to
empirical generalization, not exact filesystem/database/output behavior.

## Verification execution responsibility

Routine compilation, imports, CLI checks, and tests are agent work. On Nate's
current machine, agents run them through the repository's
`.\.venv\Scripts\python.exe`, which is agent-accessible and imports the current
editable source. The optional `.venv-owner-20260829` delegates to a base
interpreter outside the Codex sandbox's executable boundary; that optional
environment must not be treated as the only Python path or used to hand normal
verification back to the owner. Privileged production-runtime operations
remain separately controlled by their safety and authorization requirements.

## Trusted Run traceability

| Requirement group | Primary invariants | Deterministic regression focus | Empirical role | Milestone acceptance | Release checks |
|---|---|---|---|---|---|
| Configuration/standalone/privacy | `INV-STANDALONE-001`, `INV-CONFIG-001`, `INV-READ-ONLY-001` | Exact config bootstrap, explicit paths file, central root access, init ordering, base/watch doctor without current log, manual requested-file validation, damaged config/root, no discovery | None | `TRUSTED-RUN-CONFIG-01` through `06`, `TRUSTED-RUN-SAFETY-01` | Install, independence, privacy, location |
| Lifecycle/acquisition/content-hash guard | `INV-LIFECYCLE-001`, `INV-CAPTURE-001`, `INV-PUBLICATION-001`, `INV-CONTENT-HASH-001`, `INV-RUN-IDENTITY-001` | Start/exit correlation, one exact `error.log` copy, manual mode/time/unknown lifecycle, and existing-hash rejection before Run-ID creation | None | `TRUSTED-RUN-CAPTURE-01`, `TRUSTED-RUN-CAPTURE-IDENTITY-01`, `TRUSTED-RUN-MANUAL-CAPTURE-01`, `TRUSTED-RUN-RECOVERY-01` | Smoke, recovery, performance |
| Input boundary | `INV-INPUT-VALIDITY-001`, `INV-PUBLICATION-001`, `INV-EMISSION-COMPLETENESS-001` | Missing/unreadable/unstable/empty failures; genuine nonempty CK3 zero-diagnostic success; no arbitrary watcher-input queue; every valid log is processed completely as supplied regardless of size | None | `TRUSTED-RUN-INPUT-01` through `03` | Smoke, output, performance |
| Crash/exception | `INV-CRASH-001` through `INV-CRASH-003` | Normal session, crashed session/new folder/exception, historical folders, sequential sessions, artifacts-not-runs, no inferred stage | None | `TRUSTED-RUN-CRASH-01` through `TRUSTED-RUN-CRASH-03` | Smoke, migration |
| Emissions/multi-error | `INV-EMISSION-COMPLETENESS-001`, `INV-MULTI-ERROR-001` | Representative real one-line/multiline and identical-timestamp headers, approved persistent-reader clauses, counter reconciliation | Splitter version fixes denominator; no quality score excuses loss | `TRUSTED-RUN-EMISSION-01`, `TRUSTED-RUN-MULTI-ERROR-01`, `TRUSTED-RUN-NO-SILENT-LOSS-01` | Smoke, performance |
| Diagnostic aggregation | `INV-DIAGNOSTIC-IDENTITY-001`, `INV-TRANSACTION-001` | Real repeated diagnostics, meaning-bearing identity differences, first/last/count, rollback | Measurement counts recovered diagnostics, not DB rows | `TRUSTED-RUN-AGGREGATION-01`, `TRUSTED-RUN-DATABASE-01` | Migration, smoke |
| Classification/contracts | `INV-CLASSIFICATION-001`, `INV-LINEAGE-001`, `INV-RECONSTRUCTION-001`, `INV-STRUCTURE-001` | Reconstruction, reviewed recurring structure, typed slots, conservative fallback, lineage | Real-corpus coverage, compactness, split/merge review, discovery/saturation, stability, and optional claim-specific holdout | `TRUSTED-RUN-CLASSIFICATION-01`, `TRUSTED-RUN-MODEL-01` | Model readiness |
| Native review shard | `INV-REVIEW-SEPARATION-001`, `INV-TRANSACTION-001`, `INV-RETENTION-001` | Exactly one shard per success including empty, native bytes, sidecar/hash, DB emission-count/ref/availability/hash, publish/prune recovery | Review-debt distribution | `TRUSTED-RUN-REVIEW-01`, `TRUSTED-RUN-REVIEW-RETENTION-01` | Retention, docs, backup |
| Database/report | `INV-LINEAGE-001`, `INV-REPORTING-001`, `INV-OUTPUT-001` | Init/reopen/migrate, database-only human/JSON query, raw-path trap, no snapshot mutation | None | `TRUSTED-RUN-DATABASE-01`, `TRUSTED-RUN-DATABASE-02`, `TRUSTED-RUN-REPORT-01`, `TRUSTED-RUN-READ-01` | Migration, output, update |
| Retention/backup/audit | `INV-RETENTION-001`, `INV-TRANSACTION-001` | One-week raw/hash, review 90-day/2-GiB measurement candidate, pending measured exception policy, DB time/size/both, FIFO/whole-run prune with solely owned files, no orphan shard, references, compaction, restore/report regeneration | None | `TRUSTED-RUN-SOURCE-RETENTION-01`, `TRUSTED-RUN-DATABASE-RETENTION-01`, `TRUSTED-RUN-REVIEW-RETENTION-01`, `TRUSTED-RUN-EXCEPTION-RETENTION-01`, `TRUSTED-RUN-BACKUP-01` | Retention, backup, rollback |

## Later milestone traceability status

| Milestone | Current test value | Authority status before detailed gate |
|---|---|---|
| Run Comparison | Existing implementation is factual groundwork only. | No active detailed requirements or acceptance IDs. |
| Source Context | Existing `Mounted Data:`, traversal, exact-path, fingerprint, and file-instance code is factual groundwork only. | No active detailed requirements or acceptance IDs; targeted `debug.log` acquisition/copy timing, retention, and grammar must be specified first. |
| Action Triage | Existing ranking, locator, source-link, and review-separation code is factual groundwork only. | No active recommendation requirements or acceptance IDs. |
| Extended Log Intelligence | Preserve only factual existing capture/parser groundwork. | Research and owner approval precede requirements/development. |
| Trend Intelligence | Existing chronology/comparison query code is factual groundwork only. | No trend acceptance authority or speculative schema. |
| Integrations and Guided Repair | Existing bounded core JSON is an implementation observation only. | No adapter/repair acceptance authority; profiles/dependencies must be specified. |

## Test-tree policy

The test tree was reset on 2026-09-08. It contains only checks written after the
reboot from active owner-directed requirements. New checks must identify their
owning requirement and use representative real CK3 evidence whenever behavior
depends on CK3 output.

## Acceptance authorship

Requirement-derived acceptance may be implemented after ratification as
ordinary product-owned tests/records. It is not a universal blind evaluator.
A future claim-specific held-out comparison receives only its ratified
empirical question and method and may not redefine product requirements,
retention, or release engineering.
