# Interface, data compatibility, and operations policy

Status: active operations-policy authority as of 2026-08-31.

## Support rule

Support status concerns documented operator meaning, compatibility, and
deprecation. It does not freeze internal parser, classifier, or database
implementation. Final command names marked "bounded UX decision" may change
before first public release without creating a public compatibility promise.

## Trusted Run operation matrix

| Operation | Planned support | Read/write | Required behavior | Command naming |
|---|---|---|---|---|
| Readiness diagnosis | Core | Read-only | Open the exact `--config` file or one fixed default; validate syntax, required roots/types/access, database/schema, model, and retention; base/watch readiness checks the live-logs root but does not require a current `error.log`; fail closed; never discover or repair. | `doctor` fixed semantically |
| Initialization/configuration | Core | Explicit write | Use explicit `--config` or the one fixed LocalAppData file; prompt for/write/validate required roots, derive only application-owned subdirectories, then initialize the database idempotently; report changes. | Bounded UX decision, e.g. `init`/`configure` |
| Foreground observation | Core | Source read; product-data write | Observe one configured CK3 start-to-exit lifecycle and publish one protected `error.log` copy after exit. | `watch` |
| Manual/recovery acquisition | Core | Source read; product-data write | Protect and validate one explicitly requested completed `error.log`; on successful processing create one Run ID, record manual/recovery mode and capture time, and leave unobserved lifecycle facts unknown. | `capture` |
| Process protected input | Core | Write | Recognize emissions, recover diagnostics, classify/aggregate or route review, commit operational database state. | `process` |
| List/select runs | Core | Read-only | Use public run IDs and chronology. | `runs` |
| Generate report | Core | Read-only | Query database on demand; create no mandatory snapshot row. | `report`, `latest`, `errors` |
| Review-debt status/inspection | Core | Read-only | Show counts, native-shard availability, provenance, bounded inspect/export. | `review-queue` or successor |
| Reconcile interrupted work | Core operations | Explicit write | Reconcile pending files, review shards, and database intents idempotently. | `reconcile` |
| Database audit | Core operations | Read-only | Standard integrity/counter/reference checks; optional explicit deep source audit. | `audit-db` or `audit` |
| Database migration/upgrade | Core operations | Explicit write | Preflight, backup, transactional/restart-safe migration, validation, rollback. | Bounded UX decision, e.g. `db migrate` |
| Database-retention status | Core operations | Read-only | Show configured time/size limits, current usage, eligibility, and reference constraints. | Bounded UX decision |
| Database-prune preview | Core operations | Read-only | Show whole runs, estimates, baselines/references affected, and expected post-state. | Bounded UX decision |
| Database-prune execution | Core operations | Explicit write | Delete oldest eligible complete whole runs transactionally, reconcile references, audit, optionally compact. | Bounded UX decision |
| Source-retention status/cleanup | Core operations | Status read; cleanup explicit write | Apply one-week/default duration and configured size limits only after safe processing; show unavailable operations. | Bounded UX decision |
| Native-review retention status/cleanup | Core operations | Status read; cleanup explicit write | Apply separate finite limits and update database availability/audit state. | Bounded UX decision |
| Backup | Core operations | Explicit artifact write | Consistent database plus retained source/review/attachments/config/manifest. | `backup` or grouped operation |
| Restore | Core operations | Explicit write | Restore to selected/empty root, verify hashes/schema/references/reports/audit; never silently overlay unrelated data. | `restore` or grouped operation |
| Direct parse/classify | Advanced/developer | Defined per command | Functional, tested direct-stage diagnostics with revisioned outputs; not ordinary-user orchestration. | `parse`, `classify` |
| Model/contract learner/review tools | Advanced/developer | Explicit | Never promote candidate output automatically. | Existing developer tools |

`doctor` remains read-only without exception. Any write it recommends is a
separate explicit operation.

## Explicit root-configuration policy

One supported user paths/configuration file is the sole authority for every
Trusted Run operational root, including the CK3 live-logs root, CK3 crashes
root, and ck3chronicle data root. A central configuration module or global
constants populated from that file supplies all commands. Application-owned
subdirectories may be derived only below the configured data root.

The file bootstrap is singular and non-searching. `--config <path>` opens only
that exact file. Without the option, ck3chronicle opens only
`ck3chronicle/paths.toml` below the Windows LocalApplicationData known-folder
location. Failure there is failure; no alternate filename/location is probed.

Initialization prompts for or accepts each required root, writes the file,
validates syntax/key/type/existence/access, and only then initializes the
database. A missing, malformed, damaged, inaccessible, or wrong-type
configuration/root causes operational commands to fail closed. `doctor`
reports the precise fault without writing.

Base/watch `doctor` readiness validates the configured live-logs directory and
its required access. It does not require `error.log` to exist before a CK3 run
has completed. An explicit manual capture or process request validates its own
requested file through the input-validation contract.

Filesystem search, registry or Steam probing, conventional Documents paths,
sibling-repository lookup, environment guesses, and default/fallback roots are
prohibited. The negative acceptance test instruments these sources and fails
if any is accessed for discovery.

## Aliases and pre-release compatibility

- `runs` is the public term.
- `sessions` must be an exact semantic alias of `runs`, or remain
  developer-only and disappear before alpha. It may not expose a different
  public object under a confusing name.
- `process-pending` and `ingest` may remain internal/developer migration aliases
  without a public transition promise unless evidence of an external contract
  is produced.
- No public compatibility debt is manufactured before the first public
  release.
- Comparison/baseline/annotation, context/source-resolution, triage, trend,
  and adapter surfaces remain later/provisional until their detailed specs and
  milestones are accepted.

## Structured-output policy

- UTF-8 JSON emits one object on stdout; diagnostics use stderr.
- Supported commands use a versioned command/result/error envelope.
- Domain objects have independent semantic schema names/versions.
- Ordering is deterministic where it conveys chronology, occurrence count,
  confidence, load order, priority, or provenance.
- Arrays have documented limits and expose returned/total counts.
- Unknown, unavailable, expired, pruned, ambiguous, and not-applicable remain
  distinct.
- Observed, derived, correlated, and recommended values are separate.
- Run ID—not an internal content object—is the public identity.
- Reports include application/database/output versions, represented
  model/contracts, generation time, selected runs/range, filters/order, and
  completeness limitations.
- The next run/report schemas remove obsolete crash equivalence, alternate
  crash-principal paths/origins, runtime-context fields from Trusted Run, and
  any mandatory report-snapshot identity.

## Report/query policy

The operational database is the durable reportable source of truth. Generate
ordinary reports on demand for:

- one run;
- selected run IDs;
- a date/time range;
- contract/category/severity filters;
- later comparison/trend queries after those milestones are accepted.

Routine generation creates no permanent report record. Report/query logic is
versioned in source control and tagged releases; old report scripts are not
stored in SQLite. A user-requested export may include a manifest, but future
application versions need not reproduce identical historical prose/layout.

A Trusted Run report shows review emission count, native-review availability, and
parser/model revision. It need not embed every unresolved native message.
Reports always query the database. They never open, parse, hash, or otherwise
access a retained or expired raw `error.log`; a trap raw path is therefore a
required negative regression.

## Compatibility policy

### Before the first public release

- Private databases/outputs receive a reasonable migration, one-time
  conversion, or documented export/rebuild path.
- Rejected crash/log/report concepts are not retained solely for unreleased
  compatibility.
- Table renames are not performed for cosmetic consistency.
- Migration preflight reports loss/conversion and verifies a backup.

### First public release

Test the supported update/migration mechanism from a frozen representative
pre-release installation/database fixture. Alternatively, with owner
ratification, mark immediate-predecessor-public-release update not applicable.
The first release must still define a supported update path.

### From the second public release onward

- Update from the immediate public predecessor is mandatory.
- Supported databases receive documented forward migration or safe
  export/rebuild.
- Breaking CLI/output meaning increments the relevant version and receives an
  explicit replacement/deprecation notice.
- A model/contract change creates new lineage; it does not silently rewrite
  retained diagnostic history.
- Internal Python APIs, evaluator artifacts, learner working files, private
  corpora, caches, and candidate models are not compatibility surfaces.

Application, database schema, parser/extractor/splitter, model, contract
registry, recommendation policy, and each output schema version independently.

## Database placement decision

Trusted Run establishes the production database and must initialize, close,
reopen, migrate, audit, prune, back up, restore, and report from it. Run
Comparison later relates retained diagnostic history. Trend Intelligence may
add measured longitudinal optimizations.

| Named milestone | Conceptual ownership |
|---|---|
| Trusted Run | runs/chronology and capture mode/time; durable per-Run-ID `error.log` content hash; crash-attachment facts; compact diagnostic records and counts; contract/model/parser lineage; processing counters; review emission count/reference/availability/hash; schema/migrations; audit/retention/pruning/backup state; on-demand reportable inputs |
| Run Comparison | named baselines; acknowledged-noise annotations; compatibility metadata; measured optional caches |
| Source Context | approved `Mounted Data:` projection; source observations; resolved instances/merge outcomes; user overrides; temporal/availability state |
| Action Triage | versioned recommendation-policy executions or rebuildable results; never run truth |
| Extended Log Intelligence | only owner-approved source-specific compact fields/contracts for selected other-log sections/message families |
| Trend Intelligence | measured issue/file-history indexes, recurrence windows, cached aggregates, or materialized summaries |
| Integrations and Guided Repair | adapter configuration, capability grants, proposal/approval/audit state for ratified profiles |

### Existing implementation evidence

| Existing element | Current value | Required treatment |
|---|---|---|
| `sessions`, `session_files` | Captured-set identity/manifests/bytes | Preserve useful data; distinguish run chronology and narrow Trusted Run to required `error.log`. |
| Run capture metadata | Capture time/mode plus observed process and crash/exception facts when available | Preserve honest facts with one metadata record per accepted Run ID; do not create a separate receipt identity. |
| `schema_versions`, migrations | Production schema/migration seam | Preserve; harden explicit invocation/restart/rollback. |
| `raw_block_contents`, `source_blocks` | Full raw per-emission content/provenance under current model | Audit for migration; target does not require permanent per-emission rows or raw duplication. |
| `issues`, `issue_occurrences` | Aggregated and per-occurrence semantic state with overlapping parser/projection ownership | Preserve counts/meaning; migrate only after diagnostic identity approval. |
| Classification/projection tables | Model/contract/payload/assignment lineage and derived meaning | Preserve approved provenance; align with compact records and conservative review routing. |
| Current review queries | Uncertain DB rows and bounded samples | Preserve useful operator behavior; move native unresolved payload to separate shards. |
| Current reporting queries | On-demand views from stored rows | Preserve direction; remove unaccepted context/crash fields and add required query metadata. |
| Baseline/ignore tables | Comparison groundwork | Later/provisional; migrate only after Run Comparison detailed gate. |
| Runtime-context/source-observation tables | Source Context groundwork | Later/provisional; not Trusted Run acceptance. |

## Required diagnostic-record identity design

Before schema work, specify contract/revision, typed slot, relevant
file/line/symbol/locator, category/severity, normalization, and collision rules.
Only equal meaning-bearing identities within one run aggregate. Volatile
repetition metadata does not split records. Exact schema/table names follow
query and migration analysis.

## Native review-shard physical design

Use exactly one immutable, losslessly compressible native `error.log` review
shard per successfully processed run plus a small JSON sidecar, including a
valid empty shard when nothing routes to review. Preserve each routed emission,
continuation lines, order/frequency, run ID, source family, application/parser/
extractor/model revisions, routing reason, counts, and hashes. SQLite stores
only `review_emission_count`, reference, availability, and hash. Developer
inspect/export is read-only.

Shard publication and database metadata commit form one recoverable
finalization boundary. The shard has independent configurable duration/storage
limits and a finite ratified default before Trusted Run acceptance. It is not
moved into the diagnostic schema merely because SQLite exists.

Owner-accepted measurement candidate, not an active default:
**90 days and 2 GiB, whichever requires FIFO deletion first**. Measure
per-run/per-day routed bytes before and after compression, median and tail
percentiles, unknown-heavy workloads, review turnaround, and simulated
occupancy. Adjust to preserve materially more review time than the one-week raw
source while remaining finite; return the evidence for a later default decision.

## Retention layers

### Exact source and attachment data

| Layer | Candidate target default | Configuration and consequence |
|---|---|---|
| Original `error.log` | One week | Duration, storage allocation, or both. Eligible only after database and the run's review shard safely commit. |
| Root `exception.txt` attachment | No accepted numeric default; measure actual size/use | Preferred candidate relationship is retention with the associated native review shard or until its database run is pruned, whichever occurs first. Expiry retains crash/exception state/hash metadata but removes byte inspection. |

The former run-count-based source default is withdrawn. Source expiry does not
remove ordinary database reports or require a routine report warning. Reparse,
whole-log byte audit, or an operation requiring the original file reports
unavailability when invoked. When duration and allocation are both configured,
expire the oldest eligible exact sources until both limits are satisfied.

### Native review shards

Review shards use an independent finite duration and maximum allocation. The
measurement candidate is 90 days and 2 GiB pending evidence and a later owner
default decision. When both limits apply, expire oldest eligible finalized
shards FIFO until both pass. Database review emission counts remain; reference
availability becomes false and audit remains clean.

### Database history

Database history is durable relative to ephemeral source, but never unlimited.
Support a retention period, maximum database/storage allocation, or both.
Choose safe defaults only after measuring compact-record growth across
representative runs; the ratified default must be finite before acceptance.

When both are configured:

1. runs older than the period are eligible;
2. calculate oldest additional complete runs needed to meet the size limit;
3. preview the union, including estimates and affected references;
4. prune oldest eligible whole runs transactionally until both limits pass;
5. reconcile/tombstone later baseline/reference state under its ratified
   contract—never leave dangling references or silently pin data forever;
6. run audit and report actual reclaimed space;
7. offer explicit compaction with preflight, interruption behavior, and backup.

No per-emission raw-sample quota is the database sizing model. Holds/pins are
not part of the default design; add them only if a later approved operator
journey justifies their lifecycle and storage impact.

## Retention examples

### Exact source expiry

Run R-100 finishes on 1 September. After successful database/review commit, its
original `error.log` is eligible on 8 September under the one-week default.
After cleanup, R-100 still produces ordinary reports from diagnostic records;
reparse reports original source unavailable.

### Database time pruning

With a 180-day ratified period, preview selects oldest complete runs beyond 180
days. Execution deletes each selected run as a whole transaction and audits
afterward.

### Database size pruning

With a 2-GiB illustrative configured allocation (not a proposed default),
preview selects the oldest additional complete runs until estimated
post-compaction usage fits. Actual selection and reclaimed space are reported;
the example does not ratify 2 GiB.

## Pruning workflows

### Exact source/review cleanup

1. Compute eligibility and verify processing/finalization state.
2. Preview files, bytes, runs, and unavailable operations.
3. Require explicit cleanup.
4. Record intent, stage recoverably, verify removal, update availability, and
   audit.
5. On interruption, reconcile staging and database truth.

### Database pruning

1. Compute time/size eligibility over complete runs.
2. Preview exact run IDs, dependencies, estimates, and expected limits.
3. Require explicit prune execution.
4. Stage every still-retained exact source, crash attachment, and native review
   shard owned solely by the chosen run for recoverable removal.
5. Delete each chosen run and all owned database rows transactionally; finalize
   file removal and reconcile the filesystem/database intent.
6. Reconcile later references per contract.
7. Audit; then optionally run explicit compaction.

A run-owned shard may expire before its database run. It may not silently
outlive deletion of that run. Only an explicit export/promotion into a
separately governed learner corpus creates an independently retained artifact.

## Backup and restore

A software-independent history backup contains a consistent SQLite backup,
retained exact source, crash attachments, native review shards/sidecars,
configuration, and a relative-path/hash/version manifest. It excludes product
source, caches, learner corpora, private holdouts, and evaluator results.

Restore targets an empty or explicitly selected root, verifies the manifest
and database compatibility before mutation, restores files, reconciles
availability, generates representative reports from the database, and runs
audit. It never silently overlays an unrelated root.

## Operations and rollback summary

- `doctor` diagnoses only.
- Every write previews or reports changes and leaves auditable state.
- Failed migration preserves the prior database and verified backup.
- Failed source/review cleanup or database prune preserves/reconciles truthful
  availability and has no dangling references.
- Failed derived work preserves prior accepted records.
- Read operations never migrate, reclaim, reclassify, or persist a report.
