# Owner product intent and vocabulary

## Authority status

Active as of 2026-08-31. This is the concise repository authority for the
owner's governing product decisions and latest clarifications.

## Product intent

ck3chronicle is a standalone-first, local CK3 run-intelligence product for
human modders and governed tools. It protects the useful output of volatile
runs, turns one completed run's `error.log` into durable reviewable diagnostic
history, relates retained history over time, adds bounded source context, and
eventually supports cautious action triage and governed repair workflows.

The first complete product capability is Trusted Run:

> A user explicitly configures the operational roots; ck3chronicle observes
> one CK3 start-to-exit lifecycle, captures and validates its live-root
> `error.log`, stores compact diagnostic history in the production database,
> finalizes one native review shard, and generates reports from the database.

## Product boundaries

- The CLI, local database, approved model artifacts, and structured outputs
  are independently usable product core.
- CK3 and mod source files are read-only.
- Integrations are optional consumers, never core runtime dependencies.
- Runtime logs, databases, native review shards, workbooks, private holdouts, and
  generated evaluation results remain outside Git.
- Operation is local-only with no telemetry by default.
- All operational roots come only from one user-configured paths file and a
  central configuration module. Root search/autodiscovery is prohibited.
- The paths file itself is opened only from explicit `--config <path>` or the
  single fixed Windows LocalAppData application path
  `ck3chronicle/paths.toml`; no alternate-file discovery is permitted.
- Automatic capture requires one observed configured CK3 start-to-exit
  lifecycle. File presence, directory change, old retained files, retry, or
  reconciliation do not create a run.
- Every successful Run ID retains its `error.log` content hash as metadata.
  Any ingest route rejects a matching hash loudly before parsing or creating
  another Run ID. There is no override.
- Missing, unreadable, unstable, or empty `error.log` input fails loudly. A
  zero-diagnostic success requires a genuine nonempty CK3 log. The automatic
  watcher trusts the configured Paradox-managed source and is not an arbitrary
  file-validation queue.
- CK3/Paradox caps `error.log` at 100,000 timestamped entries. Reaching that
  exact boundary is expected producer behavior, not parser truncation or
  corruption. Stored/report totals must identify that they are
  producer-censored beyond the cap.
- Trusted Run acquires, parses, classifies, and stores diagnostic intelligence
  from `error.log` only.
- Existing capture or parsing of `debug.log` and `game.log` is provisional
  later-milestone groundwork and does not enlarge Trusted Run.
- Targeted `debug.log` `Mounted Data:` interpretation belongs to Source
  Context. Broader other-log research belongs to Extended Log Intelligence.
- Automatic source edits and automatic operating-system startup/service
  installation are outside Trusted Run.

## Named capability milestones

| Stable semantic ID | Name | Operator outcome |
|---|---|---|
| `MILESTONE-TRUSTED-RUN` | Trusted Run | One completed run becomes durable, classified, inspectable `error.log` intelligence in the production database. |
| `MILESTONE-RUN-COMPARISON` | Run Comparison | Stored runs and baselines yield auditable change states and visible noise annotations. |
| `MILESTONE-SOURCE-CONTEXT` | Source Context | Supported references resolve within approved active-runtime and override semantics. |
| `MILESTONE-ACTION-TRIAGE` | Action Triage | Trusted reports, changes, and source context become cautious priorities or an explicit no-recommendation result. |
| `MILESTONE-EXTENDED-LOG-INTELLIGENCE` | Extended Log Intelligence | Separately justified stable sections or message families from other logs answer approved operator questions. |
| `MILESTONE-TREND-INTELLIGENCE` | Trend Intelligence | Durable run history yields recurrence, stability, regression, and longer-run analysis. |
| `MILESTONE-INTEGRATIONS-GUIDED-REPAIR` | Integrations and Guided Repair | Accepted core capabilities support bounded adapters and separately governed repair workflows. |

Reboot Foundation names completed repository takeover, audit, evidence control,
and design recovery. It is historical foundation work, not product acceptance.

## Corrected product vocabulary

| Term | Meaning |
|---|---|
| Capability milestone | A named, user-meaningful outcome accepted as a coherent whole. |
| Acceptance check | A requirement-derived check proving one part of a capability milestone. |
| Milestone accepted | Every ratified check for the milestone passes together against one identified candidate. |
| Public-release readiness | Packaging, installation, update, documentation, migration, support, and operational checks needed to publish a supported build. |
| Model promotion | The separate decision that makes a reviewed model/contract revision approved runtime authority. |
| Implemented | Code or a capability exists, regardless of acceptance or release status. |
| Run | One successfully processed watcher-observed lifecycle capture or explicit manual/recovery capture. |
| Run ID | Stable database identity for one successful run. A manual/recovery run records capture mode/time and leaves unobserved lifecycle facts unknown. |
| Paths configuration | The single explicit user-authored configuration authority for operational roots. No search or fallback discovery supplements it. |
| Exact source log | The retained original `error.log` acquired for a run while source-retention policy keeps it. |
| Content-hash guard | Reject an `error.log` whose full-file hash is already attached to a Run ID before registration or parsing; no override is permitted. |
| Crash attachment | Root `exception.txt` associated with a newly created crash folder when captured. |
| Log emission | One parser input unit beginning at a recognized timestamp-prefixed `error.log` header and including its continuation lines until the next recognized timestamp-prefixed header. |
| Recovered diagnostic | One semantic diagnostic extracted from a log emission. The normal mapping is one-to-one; an approved source-specific splitter may recover several. |
| Diagnostic record | The compact structured database representation of one distinct recovered diagnostic identity within one run. |
| Occurrence count | Repetition metadata on a diagnostic record for equivalent diagnostics aggregated under the approved identity rule. |
| Error template | An empirically learned recurring structure. |
| Error contract | A reviewed template and validation rule approved for runtime assignment. |
| Native review shard | The single bounded per-run native-format file containing unresolved, provisional, or low-confidence emissions with provenance. It is separate from the raw log and diagnostic database. |
| Report | An on-demand human or structured view generated from stored database records for selected runs and query parameters. A user export may carry a manifest; routine generation creates no permanent snapshot. |

Most log emissions are one physical line. Some have continuation lines.
Separately timestamp-prefixed rows remain separate emissions even when their
timestamp values match. A log emission is a parser/completeness-control unit,
not normally a permanent first-class database entity.

Current internal names such as `TimestampedLogBlock`, `source_blocks`, or
`issue_occurrences` may remain temporarily where a rename would be cosmetic.
They do not define target product vocabulary or target data ownership.

## Trust rules

- Every recognized `error.log` emission produces one or more recovered
  diagnostics, is written to that run's native review shard, or produces an
  explicit parser failure. No recognized emission silently disappears.
- The normal path is one log emission to one recovered diagnostic. Multiple
  diagnostics require a reviewed source-specific splitter, representative
  fixtures, and deterministic boundaries.
- Approved full and explicitly permitted approved partial/L1 results become
  compact diagnostic records with typed slots and contract identity.
- Repeated equivalent diagnostics aggregate only when all meaning-bearing
  identity fields agree.
- Every successfully processed run finalizes one native review shard, including
  an empty shard when no item routes to review.
- Low-confidence, provisional, and unresolved native payload is not duplicated
  into the main database. The database retains review count, shard reference,
  availability, and integrity hash.
- Semantic coverage is separate from no-silent-loss completeness.
- Similarity may nominate a template; reviewed typed validation authorizes an
  assignment.
- Reports always query the operational database and never open, parse, or
  depend on raw CK3 logs.
- Pruning a database run removes every raw source, crash attachment, and native
  review shard owned solely by that run in the same recoverable workflow. A
  shard may expire earlier but cannot silently outlive its deleted run unless
  explicitly exported/promoted under separate learner-corpus governance.
- Observed facts, derived interpretations, correlations, and recommendations
  remain visibly distinct.
- A referenced or winning file is evidence, not proof of causal ownership.

## Crash rule

Only a newly created timestamped crash folder associated with the observed run
is affirmative crash-folder evidence. It may provide root `exception.txt`.
Crash-folder copies of `error.log`, `debug.log`, and `game.log` are ignored:
the product does not open, compare, hash, copy, register, expose, parse, or
test them. No inferred lifecycle stage is persisted.

## Database placement decision

The production database is established in Trusted Run.

> **The production database is a required implemented capability of Trusted
> Run. Trusted Run cannot be accepted until ck3chronicle can initialize and
> reopen the database, process a completed `error.log` run into it, and
> generate the supported Trusted Run reports from the stored records without
> requiring the original `error.log`.**

Trusted Run establishes durable run and diagnostic history. Run Comparison
relates that history. Trend Intelligence may later add measured longitudinal
optimizations. The database is neither an evaluator artifact, a raw-log
archive, nor an unlimited history store.

## Authority model after ratification

1. ratified owner intent and vocabulary;
2. focused product, interface, data, retention, model-quality, testing, and
   release contracts;
3. the named milestone plan and ratified detailed milestone specifications;
4. current status and handoff;
5. generated implementation inventories;
6. ordinary development tests and candidate-bound acceptance records;
7. model-evaluation and release records;
8. Git history.

Each stable fact has one normative home. Status and tests report truth but do
not create product scope.
