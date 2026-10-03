# Owner product intent and vocabulary

Status: active owner authority, updated 2026-09-12.

Contract/storage amendment approved 2026-09-27:
[Error Contract specification](ERROR_CONTRACT_SPECIFICATION.md). The vocabulary,
classification and storage rules below incorporate that approval; other product
decisions retain their existing scope.

## Product intent

ck3chronicle is a standalone, local CK3 run-intelligence product for human
modders and governed tools. It protects useful output from volatile runs, turns
completed-run `error.log` evidence into durable and reviewable diagnostic
history, relates retained history over time, adds bounded source context, and
eventually supports cautious action triage and governed repair workflows.

The first complete product capability is **Trusted Run**:

> A user explicitly configures operational roots; ck3chronicle observes one CK3
> start-to-exit lifecycle, protects and validates its live `error.log`, stores
> compact diagnostic history in SQLite, finalizes one native review shard, and
> generates reports from the database.

An explicit manual or recovery capture of the same supported files represents
the same kind of CK3 Run and receives the same file-derived processing. It may
lack watcher-only observations such as watcher-observed lifecycle-boundary
times, process name/PID/start identity, and proof that a crash folder appeared
during that lifecycle. Those fields remain unavailable unless independently
evidenced; the diagnostic content is not downgraded merely because capture was
manual.

The first required fast-follow after Trusted Run is same-Run `debug.log`
capture and effective-playset extraction. Once that capability begins, each new
Run ID must record the available active DLCs, enabled mods, mount/load order,
and paths needed to correlate diagnostics with the files that were active for
that Run. Earlier Run IDs, or manual/recovery Run IDs without a corresponding
`debug.log`, report playset context as unavailable.

The named capabilities, intended delivery order, and dependencies belong in
[`PROJECT_PLAN.md`](PROJECT_PLAN.md). Current implementation truth belongs in
[`PROJECT_STATUS.md`](PROJECT_STATUS.md).

## Product boundaries

- The standalone CLI, local database, approved model artifacts, and structured
  outputs are the product core. Integrations are optional consumers.
- Operation is local, with no telemetry by default.
- CK3 and mod source files are read-only. Automatic source edits and automatic
  operating-system startup or service installation are outside Trusted Run.
- Runtime logs, databases, review shards, corpora, workbooks, private holdouts,
  and generated evaluation results remain outside Git.
- All operational roots come from one explicit user-authored paths file and one
  central configuration module. An explicit `--config <path>` opens that exact
  file; otherwise only the fixed Windows LocalAppData
  `ck3chronicle/paths.toml` is used. Root search and fallback discovery are
  prohibited.
- Automatic capture requires one observed configured CK3 start-to-exit
  lifecycle. File presence, directory changes, retained files, retry, startup,
  or reconciliation do not create a run.
- The watcher protects the live `error.log` first. Hashing, parsing,
  classification, SQLite work, and reporting happen after pending publication.
- Every successful Run ID retains the full-file `error.log` hash. A matching
  hash means the same captured file was submitted again and is rejected before
  parsing or creation of another Run ID. There is no override.
- Missing, unreadable, unstable, or empty `error.log` input fails clearly. A
  zero-diagnostic success requires a genuine nonempty CK3 log.
- Every valid `error.log` is processed completely as supplied, regardless of
  size. No entry count creates special parsing, classification, storage,
  review, reporting, audit, testing, benchmarking, gating, or acceptance
  behavior.
- Trusted Run acquires and interprets diagnostic intelligence from `error.log`
  only. Its required fast-follow captures the same Run's live-root `debug.log`
  and extracts effective playset context from the DLC inventory, enabled-mod
  inventory, and `Mounted Data:` entries. This is required Source Context, not
  optional log research.
- Whether additional `debug.log` content, `game.log`, or other CK3 logs should
  be captured, parsed, or stored remains an explicit research and owner-decision
  question under Extended Log Intelligence.
- Only a newly created timestamped crash folder associated with the observed
  lifecycle is affirmative crash evidence. It may contribute root
  `exception.txt`. Crash-folder copies of principal logs are never opened,
  compared, copied, registered, exposed, parsed, or tested as product inputs.

## Product vocabulary

| Term | Meaning |
|---|---|
| Capability milestone | A named user outcome accepted as one coherent capability. |
| Acceptance check | A requirement-derived check proving part of a capability milestone. |
| Milestone accepted | Every ratified check passes together against one identified candidate and revision set. |
| Implemented | Code or behavior exists; this alone does not mean accepted, supported, or released. |
| Run | One CK3 gaming session whose evidence is captured automatically after its observed lifecycle or supplied explicitly through manual/recovery capture. The Run has already happened when processing begins. |
| Run ID | The identity assigned to one successfully ingested Run. Capture-route metadata records only what that route actually observed. |
| Paths configuration | The single user-authored authority for operational roots, with no search or fallback discovery. |
| Exact source log | The original `error.log` at the protected capture location, subject to configurable retention initially set to one month; expiry eligibility is still being settled. |
| Content-hash guard | Rejection of an `error.log` whose full-file hash already belongs to a Run ID. |
| Log emission | One recognized timestamp-prefixed `error.log` header and its continuation lines up to the next recognized header. |
| Recovered message/group | Transient native message pieces/spans recovered by the pinned parser; this is not a finalized diagnostic record. Existing code may call this a recovered diagnostic. |
| Diagnostic record | The refined, unique error message stored in SQLite within one Run, with template/provisional status and occurrence count. |
| Occurrence count | The number of equivalent diagnostics aggregated under the approved identity rule. |
| Error template | An empirically learned recurring message structure. |
| Error contract | A published template definition plus approved common acceptance, identity and rendering rules; error type initially remains unknown. |
| Native review shard | One per-Run-ID native-format file containing unassigned/unresolved evidence and provenance. Selected provisional assignments are record-eligible. |
| Effective playset | The ordered active DLC and mod context reconstructed for a Run from its captured `debug.log` inventory and `Mounted Data:` evidence. |
| Report | An on-demand human or structured database view for selected runs and query parameters. |

Most log emissions are one physical line, but some have continuation lines.
Separate timestamp-prefixed rows remain separate emissions even when their
timestamp values match. Internal implementation names do not redefine this
product vocabulary.

## Classification and completeness

- Full, provisional and unknown are current complete-message assignment outcomes.
  The published selector returns one complete assignment for both full and
  provisional outcomes, including deterministic provisional tie-breaks.
- A finite sample establishes only the templates it contains. It cannot define
  the complete set of templates CK3 may emit, and later evidence may make a
  previously unknown template classifiable.
- Complete occurrence accounting is required; 100% classification coverage is
  neither expected nor required for usefulness or release.
- Every recognized emission contributes to recovered messages/groups, is written
  to the run's native review shard, or causes an explicit parser failure. A group
  may include several emissions. No recognized emission silently disappears.
- Complete literal/slot validation and the published selector authorize an
  assignment; storage consumes the selected result without rematching.
- An approved error contract directly owns classification meaning. There is no
  separate semantic-projection or runtime mapping layer.
- Equal selected templates/literal layouts and all ordered typed binding values
  aggregate within a Run. Supporting-entry count/order/content participates;
  timestamps and original byte offsets do not. Source applicability is resolved
  during assignment, not compared again during aggregation.
- Approved classification models and contracts are immutable, versioned
  revisions selected only after deliberate review. Prior approved revisions
  remain available for rollback unless a separate retention decision changes
  that policy.

## Storage and trust

- Both selected template and provisional assignments become diagnostic records,
  with a filterable match status and occurrence count. Individual occurrence and
  diagnostic first/last timestamps are unnecessary; Run lifecycle times remain.
- Store template literals/slot placements and source/emitter once per definition,
  with ordered values and selected layout choices on each record. Reports expose
  source/emitter through that relationship and render entirely from SQL.
- Processing lineage belongs in Run metadata. Record error type may remain
  unknown. SQL does not need competing-template lists or ranking evidence.
- Every successfully processed Run ID finalizes one two-part native review shard:
  a native review log and metadata manifest, including when there are zero review emissions.
- Unresolved native payload is not duplicated in SQLite. The database stores
  only its review count, shard reference, availability, and integrity hash.
- SQLite has one explicitly versioned current schema. Compatible processing
  revisions add new Runs to the same database with their own component versions
  in Run metadata. A schema change requires an explicit database reset, without
  migration, legacy compatibility or fallback. Generation replay is banned.
  Reprocessing retained logs after an owner-chosen reset uses ordinary ingest.
- Reports query SQLite and never reopen or parse raw CK3 logs.
- Captured error/debug logs stay where the watcher put them. Use configurable
  retention, initially one month; ingestion creates no additional archive.
  Expiry eligibility for unprocessed/failed captures and automation cadence
  remain open. This raw-log policy does not expire SQL history or review shards.
- If a future authorized operation prunes a Run ID and its database record, it
  also removes that Run ID's native review shard and review metadata. It does
  not automatically delete the retained source capture or alter an approved
  classification-model revision whose development used evidence from that Run.
  Source-archive and training-evidence retention are separate policy decisions.
- The database can render diagnostic reports but is not an archive from which
  the original `error.log` can be reconstructed. Exact re-ingestion or
  source export uses the retained captured log.
- Observed facts, derived interpretations, correlations, and recommendations
  remain visibly distinct. A referenced or winning file is evidence, not proof
  of causal ownership.

## Trusted Run database requirement

The production database is an implemented part of Trusted Run, not a later
optimization. Trusted Run cannot be accepted until ck3chronicle can initialize
and reopen the current database, process a completed `error.log`
into it, and produce supported reports from stored records without requiring
the original log.
