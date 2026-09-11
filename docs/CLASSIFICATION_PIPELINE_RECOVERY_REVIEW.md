# Classification pipeline recovery review

Status: owner-review draft; this document records proposed architecture and
deletion decisions but does not authorize implementation.

Updated: 2026-09-09

## Purpose

This review explains why structurally recognized CK3 errors are currently
reported as `unclassified` / `unknown`, identifies the obsolete layers that
caused it, and records the proposed clean target before an execution plan is
written.

The governing owner direction is:

- dismantle semantic projection/mapping rather than rename or preserve it;
- expunge the legacy regex extractor taxonomy rather than leave it as an
  alternate authority or fallback;
- expunge `project_classification_run()` and its runtime/storage surface;
- retain no legacy compatibility or fallback merely because old code or data
  once used it;
- retain only mechanisms justified by current product requirements and real CK3
  evidence; and
- if an obsolete source snapshot is deliberately archived, keep that archive
  outside the canonical workspace and package.

## Proposed decision summary

1. The empirical template matcher remains the structural foundation. Its full,
   L1+L2, L1-only, and unknown outcomes remain valid.
2. A reviewed error contract will contain its hierarchical error type and typed
   slot definitions directly. Runtime will not perform a second "semantic
   mapping" or "semantic projection" operation.
3. The June regex extractor taxonomy will be deleted. Its patterns may be read
   once as evidence while contracts are reviewed, but its modules, dispatch,
   confidence decisions, and fallback behavior will not survive as product
   code.
4. `project_classification_run()` and the entire semantic-projection catalog,
   runtime, database lineage, CLI, report, audit, packaging, and generator
   surface will be deleted after the replacement path is verified.
5. Template recognition and error-type approval will have explicit outcomes.
   Absence from a finite calibration sample can never change a recognized
   contract into `unclassified.unknown`.
6. Current exact-signature aggregation will be described as diagnostic-record
   aggregation, not an "issue cluster." Causal/file/concept grouping, if later
   implemented, will be called a related-error cluster and will be a separate
   analytical capability.
7. The replacement will be made as one bounded architecture transition. There
   is no product requirement for a permanent dual path, compatibility alias,
   legacy fallback, or parallel old/new taxonomy.
8. SQLite is a disposable derived database, not an independently migrated
   source of truth. The classification recovery transition will build a fresh
   current-schema database from retained capture archives and will not alter,
   translate, backfill, or reclassify the production database in place.
9. A database schema mismatch must fail loudly. Ordinary database open,
   ingestion, pending processing, and reporting must never run schema DDL or
   sweep historical runs as a side effect.

## What the 252-sample artifact actually is

The phrase "252-sample default-unclassified artifact" combines two related but
different things:

- The calibration evidence contained 252 selected rows from one reference log:
  232 human-classified rows and 20 deliberately preserved-unclassified rows.
- The generator then attempted to create a total runtime catalog for the much
  larger learned model. For every model contract not touched by the sample, it
  manufactured a row with:

  ```text
  accounting = preserved_unclassified
  category = unclassified
  error_type = unknown
  confidence(full) = low
  projection_authority = default_preserved_unclassified
  ```

The default is visible in
`tools/template_learning/build_semantic_projection_catalog.py` at the
`default_projections` construction. It was not a learned fact about those
templates and was not a human judgment that their meaning was unknown. It meant
only "this contract was absent from this finite sample."

The active catalog contains 892 rows:

| Catalog result | Contract rows |
|---|---:|
| `classified` | 100 |
| `preserved_unclassified` | 792 |
| Total | 892 |

The 792 rows combine genuinely reviewed unresolved cases with sample-absence
defaults. The compact published catalog no longer retains enough provenance to
cleanly distinguish every row in those two populations. All 892 rows also have
empty tags, which further demonstrates that this is not a complete diagnostic
contract system.

This behavior made sense only as a conservative calibration/evaluator rule: do
not invent labels outside reviewed sample evidence. It became a product defect
when commit `05afbe2` promoted that finite calibration catalog into mandatory
runtime authority and allowed it to overwrite the output of the more capable
template matcher.

The defect is measurable in real rehearsal data:

- Run 41 had 2,149 recovered occurrences.
- The empirical matcher assigned 2,123 at full-contract level, eight at L1, and
  only 18 as structurally unknown.
- The projection stage nevertheless emitted 670 `unclassified` occurrences.
- Therefore 652 structurally recognized occurrences were downgraded only by the
  projection layer.
- Across rehearsal Runs 39–60, 232,998 structurally recognized occurrences
  ended as final `unclassified` records.

The artifact to eliminate is therefore not the existence of 252 useful review
examples. It is the policy that a finite sample is an exhaustive runtime
taxonomy and the machinery that turns sample absence into a final unknown type.

## Why the legacy extractors exist

They exist because the pipeline grew additively instead of replacing a
superseded stage:

| Date / commit | Change |
|---|---|
| 2026-06-05, `c9a8580` | Added the original parser and per-family regex extractors. |
| 2026-06-19, `31c7d73` | Added log-type dispatch and the explicitly named "heritage taxonomy." |
| 2026-08-13, `0f1e314` | Promoted the empirical model/matcher runtime. |
| 2026-08-16, `05afbe2` | Added semantic projection as another stage instead of replacing the June taxonomy/storage path. |

The current parser still calls `extract_block()` for every log emission. That
legacy call produces an `IssueDraft`, assigns `category`, `error_type`, and
confidence through broad regexes, normalizes it through the old parser
normalizer, and writes preliminary `issues` / `issue_occurrences` rows. The
empirical classifier then independently analyzes the stored source block.
Finally, `project_classification_run()` deletes the preliminary issue rows and
replaces them with catalog-projected rows.

The present path is therefore:

```text
timestamp lexer
  -> June regex extractor taxonomy
  -> preliminary issue rows
  -> August empirical template matcher
  -> 252-sample semantic projection catalog
  -> delete and replace issue rows
  -> report
```

There is no current user-driven reason for two taxonomy authorities. The
extractors survived because later work kept the old parser's output contract
and layered around it. That is implementation history, not a product
requirement.

### Revised disposition

"Stop legacy extractors from acting as an independent taxonomy authority" is
too weak. The proposed decision is to expunge the extractor taxonomy and its
fallback completely.

The only sequencing qualification is technical: deleting it before the
replacement transaction exists would make the current parser fail because the
parser and schema still require `IssueDraft` rows. That is a reason to replace
the connected call/storage path atomically, not a reason to retain legacy
compatibility afterward.

Old regexes may be inspected while drafting contracts because a reviewed
pattern name can be useful evidence. No regex receives authority merely because
it existed, and no old module, dispatch order, default type, or confidence value
will be carried forward for compatibility.

## `project_classification_run()` versus classification lineage

The function `project_classification_run()` in
`src/ck3chronicle/semantic_projection_service.py` should be expunged. It is the
runtime bridge that reconstructs stored classifier output, consults the
projection catalog, creates old `NormalizedIssue` objects, and replaces the
canonical issue rows.

This decision also removes the idea of a separate "projection run." There
should be one approved classifier/contract result from which diagnostic records
are created directly.

This is distinct from classification lineage. Each generated database still
needs to identify the model/contract revision and assignment counts used to
interpret its records. That does not require a mutable `classification_runs`
history or an in-place reclassification operation. A selected new revision is
verified in a fresh database generation; on failure, the prior database file
remains the accepted state. This draft interprets the owner's phrase "project
classification run" as the function `project_classification_run()`, not as a
request to discard immutable generation lineage.

## Canonical vocabulary

The target vocabulary is:

| Canonical term | Meaning |
|---|---|
| Engine source | The CK3 engine source family from the log header; categorically observed, not inferred. |
| Log emission | One timestamp-header record plus continuation lines. |
| Recovered diagnostic | One diagnostic recovered from an emission; normally one, or several only under an approved source-specific splitter. |
| Error template | Empirically learned recurring structure with ordered typed slots. |
| Error contract | A reviewed runtime-assignable template, validation rule, hierarchical error type, slot roles, and identity rules. |
| Assignment level | `full`, `L1+L2`, `L1`, or `unknown`; this describes structural assignment strength. |
| Error type | The sole diagnostic taxonomy label, expressed hierarchically, for example `script_system.wrong_scope`. |
| Error family | Optional shorthand for the first segment of an error type; not a separate competing taxonomy field. |
| Slot role / slot value | The typed variable field defined by a contract and the value recovered for one occurrence. |
| Diagnostic record | One within-run aggregate for a complete approved meaning-bearing identity, with occurrence count. |
| Related-error cluster | A future analytical grouping by file, group of files, game concept, cascade, call relationship, or other evidence. It is not the current exact-signature aggregate. |

Terms to remove from this pipeline are:

- `category` as a second taxonomy axis;
- `issue type` as a synonym for error type;
- `semantic mapping` and `semantic projection` as runtime concepts;
- `issue cluster` for exact-signature aggregation; and
- `unclassified issue` as though it were an error type.

A contract-authoring review may decide that template X means error type Y. That
is a property of the approved error contract, not a separate runtime mapping
operation. If a structural candidate has not received an approved type, it is a
candidate template routed to review; it is not an approved full contract that a
second stage downgrades to `unknown`.

## Target pipeline

```text
validated error.log
  -> timestamp emission recognition
  -> approved source-specific diagnostic splitting
  -> empirical contract nomination
  -> exact typed contract validation
       -> approved full / approved L1+L2 / permitted approved L1
            -> aggregate compact diagnostic records
       -> provisional / low-confidence / unknown
            -> native per-run review shard
  -> database-only report
```

There is no legacy regex taxonomy stage and no semantic projection/mapping
stage. The error contract already contains the type, typed slots, rendering,
and identity rules needed to build the record.

## Database lifecycle finding and revised direction

### What the current code actually does

The repository contains two different historical-update mechanisms. They must
not be conflated:

1. **Automatic SQLite schema migration.**
   `src/ck3chronicle/db/repository.py::open_db()` always calls
   `apply_migrations()`. The processing pipeline calls that writable open before
   listing or processing runs. The migration module adds columns, copies legacy
   capture rows into `run_metadata`, rebuilds runtime-context tables, creates
   compact replacements for source/occurrence/classification tables, drops the
   old tables, renames the replacements, updates component versions, and may
   automatically run `VACUUM` during that ordinary writable open. This is
   genuine in-place database migration, not merely validation.
2. **Historical derived-state replacement.**
   Independently of schema migration, processing compares each stored parser,
   model, classification-contract, and projection-contract lineage to the
   current runtime. A mismatch can make it parse, classify, and project an
   already registered run again. The CLI also exposes `--reparse`,
   `--reclassify`, and `backfill-session` paths that replace historical state in
   the existing database.

The earlier pending-process investigation established that the 15 production
runs selected for historical parsing were selected by parser-contract lineage,
not by the storage migration itself: production contains 15 runs at parser
contract `1.0.0` and 23 at `1.0.2`. Missing foreign-key support indexes then
made replacement deletion appear hung. The schema migration and the historical
reparse happened in the same wide workflow, which made them look like one
operation.

The production database is currently behind the working-tree schema in at least
these components:

| Component | Production database | Working-tree schema |
|---|---:|---:|
| Capture | 3 | 4 |
| Storage | 2 | 6 |

Production still has 38 `capture_observations` rows and no `run_metadata`
table. Consequently, running a current writable command that reaches
`open_db()` against production would attempt to transform that database before
doing the requested work. Read-only open now refuses the mismatch, but writable
open does not.

### Evidence available for a clean rebuild

The classification inputs have not been lost:

- Production has 38 finalized, manifest-backed session archives. All 38
  manifests enumerate an `error.log` with its byte count and SHA-256.
- Thirty-seven production manifests are version 1 and one is version 3. The
  version-1 manifests retain `captured_at`, the evidence-bundle identity, and
  file hashes, but not the newer structured `capture_metadata` object.
- The readable pending rehearsal contains 22 finalized version-3 archives,
  each with `error.log` and structured capture metadata. These are the
  evidence sources currently represented as rehearsal Runs 39–60.
- The important Run-41 proof case can survive regenerated Run IDs by selecting
  evidence bundle
  `bc2a54cb8787f32ef6eecba45a5935aa2f9a4d62c6464150ca06e3b89ccc0ecc`.

Therefore the parser, classification, and diagnostic-record state can be
reconstructed from retained logs. Some legacy capture-lifecycle metadata is a
separate issue: the production database contains old capture IDs, triggers, and
observed times that 37 version-1 manifests cannot reproduce by themselves. It
is not needed to recover error classification, but before the old database is
discarded the owner must either accept omission of those legacy-only facts or
authorize one bounded evidence export. That does not justify a permanent
receipt subsystem, an old-schema runtime reader, or database migration code.

The legacy-only metadata is mostly low-information: 37 of 38 production rows
say termination is `unknown`; 35 of 38 use `legacy_import`,
`unattributed_pending`, or `legacy_pending` as the trigger; and only one retains
an observed start time. All 38 manifests already retain `captured_at`. The
recommended simplicity-preserving disposition is therefore to omit the
non-reconstructible legacy fields from the new generation, keep the unchanged
old database as temporary forensic/rollback evidence, and write no conversion
framework unless the owner identifies a concrete fact that must be carried
forward.

### Rebuild-only database-generation policy

The revised target is:

- The immutable capture archive is the reconstruction authority. SQLite is a
  generated query/index product.
- A fresh database is created only from the current schema. The product does
  not contain an ordered chain that understands or mutates prior schemas.
- Opening an existing database validates an exact supported schema and fails
  loudly on mismatch. It does not run DDL, copy rows, reclaim pages, or perform
  any other upgrade action.
- A schema revision creates a new database generation. Verified archives are
  replayed through the one current parser/classifier/contract implementation.
  The existing database remains closed and unchanged.
- For this classification recovery transition, the projection schema is
  omitted from the fresh schema; no production projection row or legacy issue
  row is translated into the replacement representation.
- The current `migrations.py` chain, implicit migration in `open_db()`, migration
  tests, old-schema adapters, `backfill-session`, historical contract-mismatch
  sweep, and explicit in-place `--reparse` / `--reclassify` routes are not part
  of the target implementation.
- An ordinary ingestion operation handles its selected new capture. It must
  never discover a version change and silently revisit all historical runs.
- A rebuild writes a separately named candidate database, replays the complete
  retained archive set in deterministic capture order, validates hashes,
  duplicate rejection, counts, lineage, `quick_check`, and foreign keys, then
  performs an explicit cutover. The prior database remains a rollback artifact
  until the new generation is accepted.

Building and validating a replacement file before an explicit cutover is not a
schema migration or a compatibility layer. It is the safe way to restart a
derived database without corrupting the last accepted generation. Normal
SQLite transaction journaling/WAL is likewise crash-safety machinery, not the
"migration tool" rejected here.

To keep one simple lifecycle rather than retain a second historical-update
subsystem, this review applies the same new-generation rule whenever a parser,
splitter, model, or error-contract revision would change persisted derived
meaning. A model or contract revision that is merely prepared but not selected
does nothing to the current database. Once selected for historical results, it
is applied by full archive replay into a new generation, not row replacement in
the existing generation.

### Consequences that must be resolved with this policy

1. **Raw-source retention changes.** The current Trusted Run documents say an
   exact `error.log` expires after one week while older derived database history
   remains reportable. That is incompatible with a database that must be fully
   reconstructible. Every run whose database history is meant to survive the
   next rebuild must retain its exact `error.log` for the same horizon. Archives
   may be compressed and both archive/database history may have an explicit
   bounded retention policy, but database history cannot outlive its rebuild
   source.
2. **Run IDs are generation-local unless explicitly preserved.** The current
   schema assigns an autoincrement Run ID on ingestion. A replay is a new
   ingestion and may assign different IDs. Cross-generation proof and
   correlation should use the unique full-file/evidence hash; no watcher-side
   "stable identity" or receipt identity is required. If an externally durable
   Run ID is later required, that must be a separate owner decision rather than
   accidental reliance on insertion order.
3. **Observed facts cannot exist only in derived SQLite.** Future archive
   manifests must carry every non-derived fact expected to survive a rebuild.
   Derived classifications, counters, and report indexes belong in SQLite;
   source facts belong with the capture. The version-3 manifest is the current
   basis for that boundary.
4. **User-authored durable state needs a separate owner.** Any future
   acknowledgement, annotation, baseline, or preference that must survive a
   rebuild cannot have its only copy in the disposable database. Current
   provisional consumers do not justify preserving their tables or adding an
   export/import framework speculatively.
5. **Several current planning documents are superseded on this point.** In
   particular, migration requirements in `TRUSTED_RUN_SPEC.md`,
   `DATA_COMPATIBILITY_AND_OPERATIONS.md`, `RELEASE_READINESS.md`,
   `REQUIREMENTS_AND_TESTING.md`, `PROJECT_PLAN.md`, and `PROJECT_STATUS.md`,
   plus the one-week source-retention rule and the explicit-reclassification
   wording in `MODEL_QUALITY_AND_PROMOTION.md`, must be reconciled before this
   architecture is treated as implementation-ready. Until then, this reviewed
   owner direction governs the classification recovery transition and no
   production migration is authorized.

## Retain, refactor, and expunge inventory

### Retain as current foundations, with narrow refactoring

| Surface | Disposition | Reason |
|---|---|---|
| `src/ck3chronicle/parser/log_blocks.py` timestamp/continuation lexer | Retain the real-evidence emission recognizer. Remove fixture-only compatibility described below. | Current Trusted Run requirements explicitly own emission recognition. |
| `src/ck3chronicle/classification/model.py` | Retain strict hash-bound model loading. | The latest approved empirical model is present and intact. |
| `src/ck3chronicle/classification/inference.py` | Retain the full/L1+L2/L1/unknown matcher core; remove legacy-lead compatibility and return complete contract outcomes. | L1/L2 remains an owner-aligned mechanism for partial structural understanding. |
| `src/ck3chronicle/classification/contracts.py` | Retain typed exact validation and extend the approved contract definition to include error type and identity rules. | Similarity nominates; typed validation authorizes. |
| Useful portions of `src/ck3chronicle/classification/normalize.py` | Retain evidence-backed tokenization, locator separation, typed slot extraction, and approved persistent-reader splitting. | These are matcher/splitter mechanics, not the June taxonomy. |
| Empirical learner and incremental model registry core | Retain structural learning and reproducible model provenance after removing frozen-oracle/evaluator coupling. | The recovered latest learning model is valuable and current. |
| Classification lineage | Retain or replace with equivalent immutable generation metadata. | Required to interpret and verify the records in one rebuilt database; it does not authorize in-place reclassification. |

### Expunge from the active repository/package

| Surface | Required disposition |
|---|---|
| `src/ck3chronicle/parser/extractors/` | Delete the entire regex taxonomy, including `ERROR_EXTRACTORS`, debug/game/database dispatch lists, the `extract_block` legacy alias, and the terminal unclassified extractor. |
| `src/ck3chronicle/parser/normalize.py` | Delete the parallel old `IssueDraft` normalizer/signature path after diagnostic identity is implemented in the approved contract path. |
| Parser taxonomy logic in `src/ck3chronicle/parser/service.py` | Remove `extract_block()`, `IssueDraft`, unclassified fallback, and preliminary taxonomy rows. Keep only responsibilities justified by emission/splitter/storage design. |
| Old issue models in `src/ck3chronicle/models/issue.py` and dependent parse records | Replace `KNOWN_CATEGORIES`, `IssueDraft`, `NormalizedIssue`, and exact-signature "Issue cluster" types with the approved error-contract and diagnostic-record model. |
| `src/ck3chronicle/classification/projection_catalog.py` | Delete. |
| `src/ck3chronicle/semantic_projection.py` | Delete after any independently justified locator/slot routine has been moved into the contract implementation and verified. Do not retain the module as a wrapper. |
| `src/ck3chronicle/semantic_projection_service.py` | Delete, including `project_classification_run()`. |
| `models/67303093ecda779d/semantic_projection_catalog.json` | Delete from the active tree. The replacement approved revision must not bind to it. |
| Projection-bound model revision `models/67303093ecda779d/` | Use its verified structural model as an input to a deliberately published clean replacement revision, then remove the old projection-bound revision directory from the active tree. Do not leave a partial old revision or mutate a supposedly immutable artifact in place. |
| Projection fields in `models/README.md` and `pyproject.toml` | Remove when the clean model/contract revision is selected and packaged. |
| Projection loading in `src/ck3chronicle/classification/catalog.py` | Replace with loading of one approved model/error-contract authority. |
| Projection CLI arguments and output | Remove `--projection-catalog`, catalog hashes/revisions, "classified and projected" wording, and the separate projected result. |
| Projection processing stage | Remove `semantic_projection` timing/state and have approved classification produce diagnostic records directly. |
| Projection database surface | Omit `semantic_projection_runs`, projection foreign keys, indexes, triggers, repository replacement/validation functions, and counters from the fresh schema. Do not migrate or translate the existing production rows. No compatibility view or dual write remains. |
| Projection report/audit/query coupling | Remove from reporting, database audit, session intelligence, source resolution, and triage. A later feature must consume the new supported records or be deleted, not receive an adapter to the old projection schema. |
| `tools/template_learning/build_semantic_projection_catalog.py` | Delete. |
| `tools/template_learning/build_review_pack.py` | Delete the hard-coded frozen-252 review utility. Any future review export must be derived from the approved contract-review workflow, not this oracle. |
| `tools/template_learning/blind_review/` | Delete the uncommissioned historical blind evaluator utilities and hard-coded local evidence assumptions. |
| `tools/template_learning/evaluate_unseen_session.py` | Delete as a preserved historical evaluator. If a future empirical claim needs an evaluator, implement the exact commissioned claim then. |
| Projection-bound requirement tests | Replace only with checks derived from current Trusted Run requirements and real CK3 evidence. Do not translate the former projection expectations. |

Deleting a module does not mean blindly discarding an algorithm that current
requirements independently need. For example, exact locator parsing and typed
slot validation are needed. The rule is to place the smallest justified logic
inside the new contract path and then delete the old container and API; there
will be no forwarding wrapper or compatibility alias.

## Additional deprecated or superseded surfaces found

The audit found more than the three originally discussed surfaces.

### Definite cleanup in the classification/parse path

- `classification.normalize.legacy_diagnostic_lead()` explicitly exists only
  to keep the v4.6 model's historical index behavior working. A corrected new
  model revision must remove the need for it, after which the function and dual
  lookup must be deleted.
- `parser.log_blocks._HEADER_RE_TWO` is explicitly retained for legacy
  Chronicle fixtures. The rehearsal database contains 2,186,219 stored source
  blocks, all with level `E`, and zero null/empty levels; none used that
  two-bracket compatibility form. Remove it unless a separately reviewed real
  CK3 example proves it current.
- `TimestampedLogBlock` provenance defaults are documented as support for older
  unit fixtures. Update the small number of current learner-tool constructors
  to be explicit, then remove those compatibility defaults.
- `repository.replace_canonical_parse()` describes itself as a compatibility
  adapter for callers with complete prepared lists. It has no active caller and
  should be deleted rather than maintained beside the streaming path.
- `_log_type_from_relpath()` in the CLI and
  `extract_block_for_log_type()` in the extractor registry have no active
  callers. They belong to the unsupported multi-log extractor design and
  should disappear with that design.
- `_cmd_process_pending_wide_legacy()` has no CLI registration; the supported
  command is the exact-one-capture operation. Delete the dead wide processor
  rather than keep a rejected implementation in source.
- CLI `--session` aliases for `--run` are explicitly labeled compatibility
  aliases. Current vocabulary has one Run ID, so the aliases should be removed
  unless the owner identifies a current external caller and expressly directs
  a short removal transition.
- The current DB-backed `review-queue` is superseded by the approved native
  per-run review shard. It must not be preserved as a second unresolved-payload
  store when the shard is implemented.

### WIP/evaluator code imported as preservation

Commit `090d8c8` imported roughly 7,000 lines of learner, 252-sample,
blind-review, holdout, evaluator, and projection-generator source. Its stated
reason was to preserve WIP project method against machine loss. The current
`tools/template_learning/README.md` repeats that several WIP calibration
utilities are preserved, and `tools/template_learning/AGENTS.md` currently
declares blind-review and projection-catalog generation as owned work.

That preservation rationale is not a user requirement and is a direct source
of obsolete terminology and policy. The tool guidance must be rewritten along
with the code cleanup.

The useful structural learner should not be deleted, but it is mixed with
obsolete evaluator assumptions:

- `learn_error_templates.py` requires `--oracle-root`, embeds a
  `evaluate_frozen_oracle()` pass against the 252 artifacts, performs synthetic
  mutation checks, and reports category/type purity. Remove that coupling from
  the learner. Training should create structural candidates; contract review
  and any commissioned evaluation are separate.
- `incremental_template_registry.py` requires the same oracle for every build
  and embeds a universal candidate/training/holdout/ignored role system. Retain
  only provenance and deliberately selected training inputs needed by the
  current learner. A holdout/evaluator exists only for a separately
  commissioned empirical claim.
- `mine_symbol_suffixes.py` imports the old unseen-session evaluator for model
  reconstruction. Decouple any genuinely needed slot-QC logic from that
  evaluator; absent a current owner requirement, delete the miner rather than
  preserve it speculatively.
- `analyze_script_system_layers.py` is not projection code and may provide
  useful evidence for L1/L2 review. Retain it only if the forthcoming contract
  review actually uses it; otherwise it also has no reason to remain as an
  unowned historical utility.

### Other compatibility surfaces requiring bounded review

- The Python `<3.11` `tomllib` import fallback in `config.py` is unreachable
  under the package's declared `requires-python >=3.11` contract and should be
  removed.
- `reporting.latest_report_target()` contains a fallback for databases awaiting
  run-metadata backfill, and session-intelligence contains a fallback for old
  direct/development registrations. The replacement database must use only the
  current representation, so these paths should be deleted rather than carried
  into a fresh generation.
- `ingest()` calls itself a compatibility API, but explicit manual/recovery
  capture is a current owner requirement. It must be reviewed on function, not
  name: either make one deliberately supported manual/recovery route with a
  current contract or replace it. It does not survive merely as a compatibility
  route.
- The 22 legacy pending captures still need bounded evidence normalization and
  finalization from their readable copies. That is a one-time capture/archive
  recovery task, not authority for a database migration framework. The
  production database will not be migrated; it remains a rollback artifact
  while a fresh generation is built. The temporary pending-metadata conversion
  utility must be deleted after the captures are finalized and verified.

Later-milestone modules such as `session_intelligence.py`,
`source_resolution.py`, and `triage.py` are provisional under the active
project plan and currently query projection storage. Their existence must not
force compatibility adapters. If no ratified current milestone requires a
surface when projection is removed, the default is deletion; future work can
be rebuilt from accepted diagnostic records after its own requirements gate.

## Model and contract recovery direction

The current empirical model is not missing. Revision `67303093ecda779d` is the
latest recovered incremental revision and its model bytes match the preserved
registry. The structural matcher and L1/L2 implementation are also present.

The recovery task is therefore not to restore an older parser wholesale. It is
to publish a clean approved model/error-contract revision that:

- retains or retrains the verified structural templates;
- removes the legacy diagnostic-lead compatibility shim;
- places the hierarchical error type and typed slot/identity rules directly in
  each approved contract;
- distinguishes approved full, permitted approved partial/L1, provisional, and
  structurally unknown outcomes;
- uses the 252 examples only as review evidence where still valid;
- incorporates other traceable human-reviewed decisions and representative
  real CK3 evidence;
- contains no sample-absence default that downgrades a recognized template;
  and
- contains no semantic projection catalog or projection runtime binding.

The old regex parser is not the restoration target. A direct in-memory pass of
that parser over Run 41 produced 465 unclassified occurrences and relied on
broad high-confidence matches. It contains useful historical clues, but it is
not the best-in-class matcher the product should run.

## Non-negotiable proof for the later execution plan

This is not the ordered execution plan, but the eventual plan must prove at
least the following before cutover:

- Runs 39–60 retain exact recognized-emission and recovered-diagnostic
  accounting unless an explicitly reviewed splitter correction explains a
  difference.
- Run 41 retains 1,541 source emissions and 2,149 recovered occurrences; the
  2,131 full/L1 assignments cannot become unknown merely because the 252 sample
  omitted their contracts.
- Full, L1+L2, L1, provisional, and unknown outcomes remain visible and
  reconcile with the native review shard and diagnostic records.
- Every approved record has one hierarchical `error_type`, contract identity,
  typed slots, and required source/locator identity fields.
- No active import, CLI option, schema field, report field, package-data entry,
  documentation authority, or processing stage uses semantic projection or
  semantic mapping.
- No active parser/extractor taxonomy or terminal regex fallback remains.
- Taxonomy/contract refresh does not masquerade as a parser-contract change.
  If the selected revision changes persisted historical meaning, it produces a
  complete new database generation rather than replacing rows in situ.
- The existing production database remains byte-unchanged during rebuild. The
  fresh current-schema database is reconstructed only from verified archives;
  cutover requires `quick_check=ok`, zero foreign-key violations, unique source
  hashes, archive/database reconciliation, and reconciled diagnostic counts.
- Repository searches prove there is no active schema-migration chain,
  old-schema adapter, historical contract-mismatch sweep, `backfill-session`,
  or in-place reparse/reclassification command.
- Representative obvious patterns, including persistent-reader failed-key
  references, script-system wrong-scope errors, and never-set variables, show
  the expected reviewed error types.
- Repository searches and package/import checks prove the superseded modules
  and compatibility aliases are gone rather than merely unused.

## Archive and Git-history rule

No `archive/`, `legacy/`, disabled copy, forwarding wrapper, or commented-out
version of the removed implementation should remain in the canonical workspace
or package. If the owner elects to retain a standalone source snapshot, it must
be exported outside the workspace and must not be an active dependency.

A normal deletion commit removes these files from the branch tip and from the
future package/clone while ordinary Git history still records the old commits.
Rewriting remote history to erase those commits is a separate destructive
decision and is not implied by this review.

## Owner-review checkpoints before execution planning

The next review should confirm:

1. `project_classification_run()` is the intended meaning of "project
   classification run"; immutable per-generation classification lineage itself
   remains required.
2. The definite-expunge inventory above is accepted, including the 252 review
   pack, blind-review, and unseen-session evaluator utilities imported in
   `090d8c8`.
3. The structural learner and L1/L2 mechanism remain, but all frozen-oracle and
   universal-holdout coupling is removed.
4. Later provisional consumers receive no compatibility adapter and are deleted
   if they have no ratified requirement at transition time.
5. Any optional archive is external only; the canonical tree contains the
   current implementation and current evidence-derived method, not retired
   source.
6. SQLite is accepted as a fully derived, rebuild-only database; schema and
   persisted-meaning changes create a fresh generation rather than migrating or
   replacing historical rows in situ.
7. Exact `error.log` retention is extended to the desired database-history
   horizon, or the owner explicitly accepts that a rebuild drops history whose
   source has expired.
8. Rebuilt Run IDs are allowed to be generation-local, with full content/evidence
   hashes used for cross-generation correlation.
9. The disposition of legacy capture metadata present only in the old database
   is chosen before that database's rollback copy is deleted.

After those decisions are ratified, a separate execution plan can order the
new contract artifact, code replacement, fresh-database replay, real-evidence
verification, explicit cutover, and final deletion without creating a
compatibility period as a product feature.

## Locator appendix: removal provenance and live call graph (2026-09-09)

This appendix is the deletion/refactor search map requested before execution.
The locators refer to the working tree inspected on 2026-09-09, atop Git commit
`a5925fad8c209c206d8da10986d81c3183aa27c7`. That working tree already contains
uncommitted reboot/recovery changes, so all ranges must be revalidated
immediately before an implementation commit. A range identifies the connected
surface to replace or review; it is not permission to delete retained logic
blindly.

Disposition labels used below are:

- **Expunge**: remove the implementation and all active callers; do not leave a
  wrapper, fallback, alias, or disabled copy.
- **Replace/refactor**: retain only the independently required responsibility in
  the new direct error-contract path.
- **Conditional review**: no current requirement was established by this audit;
  delete if owner/routing review confirms there is no separately ratified use.
- **Historical evidence only**: useful for provenance, but outside the canonical
  repository and never an implementation authority or dependency.

### Exact provenance of the 252 rows

The two raw 252-row JSON artifacts are **not present anywhere in the current
canonical repository or its reachable Git path history** under their filenames.
The generator nevertheless defaults to nonexistent canonical paths at
`tools/template_learning/build_semantic_projection_catalog.py:23-28` and later
overwrites them from required CLI arguments at
`tools/template_learning/build_semantic_projection_catalog.py:734-750`.

Exact historical copies were located outside the canonical repository. These
are evidence locators only and must not become runtime dependencies:

| Historical artifact | Exact content ranges | Identity |
|---|---|---|
| `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase0\SEMANTIC_CALIBRATION_SAMPLE_CANDIDATE.json` | Metadata/selection summary `:1-372`; `samples` array `:373-6792`; closing document `:6793`. The explicit `sample_count: 252` is at `:52-80`. | 348,923 bytes; 6,793 lines; SHA-256 `f19a7aa858a14ee62371fa3721fc3c95288b9473c54d487c1608a55fe0480061`. |
| `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase0\SEMANTIC_LABELS_ADJUDICATED.json` | Metadata/review/accounting `:1-167`; `annotations` array `:168-10349`; closing document `:10350`. The `232 classified / 20 preserved_unclassified` accounting is at `:52-58`. | 341,708 bytes; 10,350 lines; SHA-256 `db8a58a9a7f7f7fb0b84d1e39c1b2e724eae8058a00d07bb578367b795723e3d`. |
| `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase1\locked-corpus-v2-public\units\DEV-SEMANTIC-252\SEMANTIC_CALIBRATION_SAMPLE_CANDIDATE.json` | Same ranges as the phase-0 candidate above. | Byte-identical to the phase-0 candidate; same SHA-256. |
| `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase1\locked-corpus-v2-public\units\DEV-SEMANTIC-252\SEMANTIC_LABELS_ADJUDICATED.json` | Same ranges as the phase-0 adjudication above. | Byte-identical to the phase-0 adjudication; same SHA-256. |

The historical selector that created the candidate sample is
`C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3raven\.ck3raven\wip\ck3chronicle-phase0\select_semantic_calibration_sample.py`:

| Range | Role | Disposition |
|---|---|---|
| `:146-276` | `select_candidates()` sampling policy. | Historical evidence only. |
| `:279-425` | `build_output()` candidate-document construction. | Historical evidence only. |
| `:428-445` | CLI arguments and `main()` execution. | Historical evidence only. |

The finite sample becomes the default-unclassified runtime policy in the
current canonical generator here:

| Canonical locator | Exact role | Disposition |
|---|---|---|
| `tools/template_learning/build_semantic_projection_catalog.py:742-763` | Loads all candidate rows and adjudications and classifies each row with the approved empirical matcher. | Expunge with the projection generator. |
| `tools/template_learning/build_semantic_projection_catalog.py:967-991` | Computes model contracts absent from the audited set and manufactures `accounting=preserved_unclassified`, `category=unclassified`, `error_type=unknown`, low confidence, empty tags/slots/references, and `projection_authority=default_preserved_unclassified`. This is the exact policy source. | Expunge. |
| `tools/template_learning/build_semantic_projection_catalog.py:992-1028` | Combines audited and manufactured projections and records their counts. | Expunge. |
| `tools/template_learning/build_semantic_projection_catalog.py:1156-1185` | Creates the runtime-compatible catalog. Critically, `compatible_fields` omits `projection_authority`, so the compiled runtime artifact no longer records which individual rows were manufactured by the default. | Expunge. |
| `tools/template_learning/build_semantic_projection_catalog.py:1187-1264` | Reloads that catalog, projects the same 252 rows, and emits the 252/252 calibration result. | Expunge. |

The compiled result is
`models/67303093ecda779d/semantic_projection_catalog.json:1-14082`.
Its projection array is `:7-14081`; the first preserved-unclassified record is
`:8-22` and the last is `:14066-14080`. The 792 preserved-unclassified records
are interspersed rather than one contiguous line range. A JSON parse of the
current file gives 892 total projections: 100 `classified` and 792
`preserved_unclassified`. Because the compatible export stripped
`projection_authority`, the generator range above—not a field in this compiled
file—is the authoritative provenance of the default policy.

Related active artifact/documentation bindings are:

| Locator | Role | Disposition |
|---|---|---|
| `models/67303093ecda779d/manifest.json:1` | Pins the semantic projection revision and SHA-256 in a minified manifest. | Publish a clean projection-free model/error-contract revision, then remove the old projection-bound revision. |
| `models/README.md:7-32` | Declares the 892-row catalog, 792 unclassified projections, and 252/252 calibration. | Rewrite for the replacement revision. |
| `pyproject.toml:29-34` | Packages the semantic projection catalog. | Remove the catalog package-data entry. |

### Where the 252-derived policy enters ingestion and parsing

There is no direct runtime read of either raw 252 JSON file. The current
`ingest()` operation explicitly stops after archive/Run registration and says
parsing is outside that operation at `src/ck3chronicle/ingest.py:35-121`
(especially `:41-45` and `:80-103`). The compiled catalog enters the later
processing path instead:

```text
src/ck3chronicle/cli.py:1507-1622  cmd_process_one_pending()
  :1523                         load approved classifier + compiled catalog
  :1524-1529                    make the one-capture plan
  :1555-1560                    execute process_planned_pending_capture()

src/ck3chronicle/processing.py:499-590
  :575-579                      process only the newly registered Run
    -> :1064-1086               process_selected_sessions()
      -> :698-1061              process_pending()
        :817-822                writable database open
        :897-917                parse_session()
        :927-943                classify_session()
        :944-960                project_classification_run() with catalog
```

`process_pending()` can also load the catalog itself when none was supplied at
`src/ck3chronicle/processing.py:756-764`. The direct `classify` command loads a
default or caller-supplied projection catalog, classifies, and immediately
projects at `src/ck3chronicle/cli.py:732-866` (catalog selection `:746-797`, DB
open/classify/project `:798-809`, projection output `:829-865`). The historical
`backfill-session` route repeats the same approved-runtime load and selected-Run
processing at `src/ck3chronicle/cli.py:1625-1731` (especially `:1641-1646` and
`:1673-1688`).

That proves the present order precisely:

1. `src/ck3chronicle/parser/service.py:204-289` applies the old regex taxonomy
   and stores preliminary issue rows.
2. `src/ck3chronicle/classification/service.py:161-210` runs the empirical
   matcher, and `:275-303` stores its assignments.
3. `src/ck3chronicle/processing.py:944-960` calls the projection stage, which
   turns those assignments into final issue rows using the compiled
   252-derived catalog.

### Old regex taxonomy: complete implementation and call locators

The active parser imports the legacy draft model, registry, terminal fallback,
and old normalizer at `src/ck3chronicle/parser/service.py:10-21`. For every
recognized emission it calls `extract_block()`, applies the unconditional
fallback if needed, normalizes the draft, and writes preliminary issue rows at
`src/ck3chronicle/parser/service.py:204-289` (the taxonomy call itself is
`:230-251`). The parser later counts exact-signature aggregates at `:329-365`.

The complete extractor-taxonomy directory is:

| Locator | Role | Disposition |
|---|---|---|
| `src/ck3chronicle/parser/extractors/__init__.py:1-121` | Log-type registries and dispatch. `ERROR_EXTRACTORS` is `:43-55`; aliases/maps are `:57-93`; live `extract_block()` is `:98-108`; unused multi-log `extract_block_for_log_type()` is `:111-121`. | Expunge entire file/directory with connected parser calls. |
| `src/ck3chronicle/parser/extractors/asset_graphics.py:1-35` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/culture_faith.py:1-34` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/database_reference.py:1-38` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/debug_log.py:1-122` | Deprecated debug/game multi-log taxonomy. | Expunge. |
| `src/ck3chronicle/parser/extractors/descriptor.py:1-31` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/event_system.py:1-37` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/gui_interface.py:1-34` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/history_setup.py:1-31` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/localization.py:1-49` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/persistent_reader.py:1-36` | Regex category extractor. | Expunge after reviewed persistent-reader contracts cover the real patterns. |
| `src/ck3chronicle/parser/extractors/script_hygiene.py:1-36` | Regex category extractor. | Expunge. |
| `src/ck3chronicle/parser/extractors/script_system.py:1-105` | Explicit “heritage taxonomy” provenance `:1-15`, broad pattern/type selection `:27-62`, and high-confidence draft creation `:65-105`. | Expunge; inspect patterns once as non-authoritative evidence if useful. |
| `src/ck3chronicle/parser/extractors/unclassified.py:1-36` | Terminal always-true match at `:12-16` and `unclassified/unknown` draft at `:19-36`. | Expunge. |

Its connected old normalization/storage representation is:

| Locator | Role | Disposition |
|---|---|---|
| `src/ck3chronicle/parser/normalize.py:1-99` | Parallel draft masking, template, and signature algorithm; `normalize()` is `:60-99`. | Expunge after required diagnostic identity is implemented in approved contracts. |
| `src/ck3chronicle/models/issue.py:1-30` | Category/error-type registries. | Replace with one hierarchical `error_type` contract vocabulary. |
| `src/ck3chronicle/models/issue.py:42-65` | `IssueDraft`. | Expunge. |
| `src/ck3chronicle/models/issue.py:69-93` | Old `NormalizedIssue`. | Expunge. |
| `src/ck3chronicle/models/issue.py:97-131` | Exact-signature `Issue` aggregate and `IssueOccurrence`. | Replace with diagnostic-record and exact-template-occurrence models. |
| `src/ck3chronicle/models/parse.py:33-57` | `ClusterRecord`/`ParseCounters` “issue cluster” vocabulary. | Rename/refactor; retain only exact-template aggregation accounting. |
| `src/ck3chronicle/db/repository.py:1104-1217` | Preliminary source-block, aggregate, and occurrence inserts. | Refactor to the one direct contract-derived record path. |
| `src/ck3chronicle/db/repository.py:1286-1365` | Deletes prior parse/classification state and appends replacement parser rows. | Remove historical replacement behavior; retain only fresh-generation/new-Run writes justified by the new schema. |

A repository-wide Python call search found exactly one live caller of
`extract_block()`: `src/ck3chronicle/parser/service.py:230`. It found no caller
of `extract_block_for_log_type()` outside its definition.

### Semantic projection/mapping: complete active surface

The projection system is not one function; it is a catalog authority, runtime
transformation, persistence lineage, replacement transaction, CLI/processing
stage, and a set of downstream query assumptions. All of the following must be
removed or rewritten together so no partial compatibility path remains.

#### Catalog pinning and validation

| Locator | Exact role | Disposition |
|---|---|---|
| `src/ck3chronicle/classification/catalog.py:10-22` | Imports projection loader and pins projection revision/SHA. | Remove projection binding. |
| `src/ck3chronicle/classification/catalog.py:52-73` | Finds and hash-validates the approved projection catalog. | Expunge. |
| `src/ck3chronicle/classification/catalog.py:76-82` | Returns either classifier alone or the combined semantic runtime. | Replace with one approved classifier/error-contract loader. |
| `src/ck3chronicle/classification/projection_catalog.py:1-508` | Complete catalog schema/model/loader. Contract-ID helpers are `:123-142`; entry validation is `:145-418`; total model-coverage loading is `:421-508`, including the every-contract requirement at `:471-495`. | Expunge entire module. |
| `models/67303093ecda779d/semantic_projection_catalog.json:1-14082` | Active compiled projection authority. | Expunge after clean replacement revision is published and verified. |

#### Runtime transformation and `project_classification_run()`

| Locator | Exact role | Disposition |
|---|---|---|
| `src/ck3chronicle/semantic_projection.py:1-620` | Complete pure projection module. Evidence/locator/slot parsing is `:94-251`; template/reference extraction is `:254-472`; unclassified default/resolution is `:475-529`; final projection is `:532-620`. | Expunge module. Move only independently justified, tested locator/typed-slot routines into the direct contract implementation. |
| `src/ck3chronicle/semantic_projection_service.py:1-465` | Complete stored-classification bridge. Reconstruction is `:103-222`; `project_classification_run()` is exactly `:225-465`. | Expunge entire module and function. |
| `src/ck3chronicle/semantic_projection_service.py:318-430` | Reconstructs stored assignments and creates projected occurrences. | Expunge. |
| `src/ck3chronicle/semantic_projection_service.py:432-465` | Calls the repository replacement transaction and returns projection lineage/counts. | Expunge. |
| `src/ck3chronicle/processing.py:18,32-34` | Projection type/service imports. | Remove. |
| `src/ck3chronicle/processing.py:593-695` | Treats projection currentness as a historical-Run planning state. | Remove projection state and the historical contract-mismatch sweep. |
| `src/ck3chronicle/processing.py:698-1061` | Runtime accepts/loads catalog and invokes projection; focused ranges are `:756-764` and `:944-960`. | Replace with bounded new-Run direct record production. |
| `src/ck3chronicle/cli.py:732-866` | Direct classify command loads and invokes projection. | Rewrite or remove according to the replacement operator workflow. |
| `src/ck3chronicle/cli.py:2516-2531` | `--projection-catalog`, hash, and `--reclassify` CLI options. | Remove. |
| `src/ck3chronicle/cli.py:1507-1622` | Exact pending command loads the semantic runtime and reports projected counts. | Retain one-capture command, remove projection dependency/output. |
| `src/ck3chronicle/cli.py:1625-1731` | Historical `backfill-session` command loads and runs projection. | Expunge command. |

A repository-wide call search found only two product-code calls to
`project_classification_run()`: `src/ck3chronicle/cli.py:807-809` and
`src/ck3chronicle/processing.py:944-960`. Its pure helper
`project_normalized_issue()` is called by the service at
`src/ck3chronicle/semantic_projection_service.py:358`; `project_issue()` is also
called by the obsolete generator at
`tools/template_learning/build_semantic_projection_catalog.py:1207`.

#### Projection database schema and repository transaction

| Locator | Exact role | Disposition |
|---|---|---|
| `src/ck3chronicle/db/schema.py:102-192` | Old issue columns plus projection foreign keys and indexes; projection FK fields are `:122-124` and `:160-162`, projection indexes `:139-142` and `:177-192`. | Replace issue schema; omit projection fields/indexes from fresh schema. |
| `src/ck3chronicle/db/schema.py:291-332` | `semantic_projection_runs`, index, and invalidation trigger. | Expunge. |
| `src/ck3chronicle/db/schema.py:509-539` | Adds projection DDL to schema initialization. | Remove entries. |
| `src/ck3chronicle/db/schema.py:541-550` | Component-version constants, including `SEMANTIC_PROJECTION_VERSION` at `:546`. | Remove projection version; retain only an exact current-schema identity mechanism. |
| `src/ck3chronicle/db/repository.py:2058-2124` | Loads projection lineage and stored classifier inputs. | Expunge projection-specific functions. |
| `src/ck3chronicle/db/repository.py:2127-2210` | Computes and validates prepared projection counts. | Expunge. |
| `src/ck3chronicle/db/repository.py:2213-2286` | Upserts projected aggregates and occurrences. | Replace with direct approved diagnostic-record inserts, not an adapter. |
| `src/ck3chronicle/db/repository.py:2289-2528` | Postvalidates and revalidates projection lineage/rows. | Expunge projection-specific validation. |
| `src/ck3chronicle/db/repository.py:2531-2837` | `replace_semantic_projection()`: deletes prior projection/issues at `:2595-2614`, inserts lineage at `:2615-2649`, writes rows at `:2651-2735`, updates counters/validates/commits at `:2737-2798`. | Expunge whole replacement transaction. |

#### Downstream projection consumers

| Locator | Dependency | Disposition |
|---|---|---|
| `src/ck3chronicle/reporting.py:15-40` | Latest-report target requires a projection join, with old-metadata fallback. | Rewrite against direct records and remove backfill fallback. |
| `src/ck3chronicle/reporting.py:81-411` | Main report requires/validates projection (`:99-110`), filters projected occurrences (`:150-157`), and emits projection metadata (`:254-266`, `:404`). | Rewrite; no projection compatibility adapter. |
| `src/ck3chronicle/database_audit.py:80-875` | Projection table inventory and consistency audit, especially `:370-580` and summary `:856-860`. | Rewrite for fresh direct schema. |
| `src/ck3chronicle/session_intelligence.py:22-49` | Classification selection requires projection join. | Rewrite if feature remains commissioned. |
| `src/ck3chronicle/session_intelligence.py:141-210` | Previous-Run selection requires projection joins (`:161`, `:192`). | Conditional review, then rewrite or delete. |
| `src/ck3chronicle/session_intelligence.py:484-516` | Previous-run metadata requires projection join (`:495`). | Conditional review, then rewrite or delete. |
| `src/ck3chronicle/source_resolution.py:409-451` | Referenced-file query requires projection join at `:417`. | Conditional review, then rewrite or delete. |
| `src/ck3chronicle/triage.py:30-43` and `:81-191` | Triage chooses only projection-backed classification runs. | Conditional review, then rewrite or delete. |
| `tests/test_processing_recovery_requirements.py:13,145-150,314-320` | Current recovery test loads/passes the semantic runtime. | Rewrite from the final direct-contract requirement. |
| `tests/test_processing_recovery_requirements.py:168-284` | Current recovery test asserts projection foreign-key/index behavior. | Delete these projection expectations; replace only with new-schema invariants. |

### In-place database migration and historical rewriting locators

These are separate from semantic projection but conflict with the accepted
rebuild-only database policy.

| Locator | Exact role | Disposition |
|---|---|---|
| `src/ck3chronicle/db/migrations.py:1-919` | Complete migration implementation. Detection is `:40-158`; transaction wrapper `:161-174`; schema/data conversions `:177-618`; compact table rebuild/copy/drop/rename `:621-919`. | Expunge migration chain. Do not replace it with old-schema adapters. |
| `src/ck3chronicle/db/repository.py:13` | Imports migration machinery. | Remove. |
| `src/ck3chronicle/db/repository.py:68-109` | Every writable `open_db()` applies migrations and may run `VACUUM`. | Replace with create-current-or-open-exact-current behavior; mismatch fails loudly. |
| `src/ck3chronicle/db/repository.py:112-144` | Read-only open reports “migration required.” | Retain read-only protection but replace migration terminology/decision with exact-schema mismatch failure. |
| `src/ck3chronicle/archive_registry.py:85-181` and `:184-307` | Archive registration/reconciliation both call writable `open_db()` (`:121-126`, `:203`). | Retain required archive functions only after their DB open cannot migrate. |
| `src/ck3chronicle/ingest.py:57-64,80-103` | Manual ingest opens DB twice through the migrating opener. | Use strict current-generation DB open. |
| `src/ck3chronicle/processing.py:817-822` | Pending processing opens DB through the migrating opener. | Use strict current-generation DB open. |
| `src/ck3chronicle/cli.py:690-713` | Direct parse opens writable DB and can replace historical parse. | Remove in-place route or constrain replacement implementation to fresh/new Run processing. |
| `src/ck3chronicle/cli.py:732-866` | Direct classify opens writable DB and can replace historical classification/projection. | Remove in-place route. |
| `src/ck3chronicle/cli.py:1890-1933`, `:1976-2012`, `:2022-2056`, `:2095-2134`, `:2137-2251` | Baseline/ignore/context mutable commands also use the auto-migrating opener. | If retained after requirement review, all must use strict current-schema open; no migration side effect. |

Historical derived-state replacement is implemented independently of schema
migration:

| Locator | Replacement behavior | Disposition |
|---|---|---|
| `src/ck3chronicle/parser/service.py:83-126` | `reparse` flag and parser-contract mismatch permit an existing parse to be revisited. | Remove historical in-place semantics. |
| `src/ck3chronicle/parser/service.py:182-203` plus `src/ck3chronicle/db/repository.py:1286-1339` | Begins destructive canonical replacement. | Not part of ordinary processing in rebuild-only design. |
| `src/ck3chronicle/classification/service.py:100-159` | `reclassify` and contract-version checks permit an existing classification to be revisited. | Remove historical in-place semantics. |
| `src/ck3chronicle/classification/service.py:275-303` plus `src/ck3chronicle/db/repository.py:1763-2046` | Replaces the stored classification run. | Refactor for one write in a fresh generation/new Run; no historical replacement command. |
| `src/ck3chronicle/processing.py:593-695` | Plans parse/classification/projection currentness for existing Runs. | Remove historical mismatch sweep. |
| `src/ck3chronicle/processing.py:824-960` | Lists selected/historical sessions and reparses when parser lineage differs (`:897-917`), then classifies/projects. | Ordinary pending processing must handle only the selected new Run. |
| `src/ck3chronicle/cli.py:2497-2514` | Exposes `parse --reparse`. | Remove `--reparse`. |
| `src/ck3chronicle/cli.py:2516-2531` | Exposes `classify --reclassify`. | Remove `--reclassify`. |
| `src/ck3chronicle/cli.py:2639-2655` and command body `:1625-1731` | Exposes `backfill-session`. | Expunge. |
| `src/ck3chronicle/cli.py:2733-2744` and command body `:2137-2251` | Exposes runtime-context `--reparse`. | Review separately; if context is derived, refresh it only in a fresh database generation rather than in-place. |
| `tests/test_processing_recovery_requirements.py:80-94` | Asserts automatic schema migration. | Replace with exact-schema failure/current-generation initialization checks. |
| `tests/test_processing_recovery_requirements.py:286-346` | Exercises selected historical-session planning/backfill. | Remove or rewrite for explicit fresh-database replay. |
| `tools/migrate_legacy_pending_metadata.ps1:1-236` | One-time conversion of the 22 recovered pending captures. | Delete after the captures are finalized and verified; it is not a database migration facility. |

`schema_versions` or an equivalent single schema identity may remain solely to
recognize the exact current format. The banned behavior is translating an old
database or revisiting old derived rows during ordinary open/processing. Normal
SQLite transaction rollback, journaling, and WAL remain crash-safety mechanisms
and are not implicated.

### Remaining deprecated, superseded, or conditional surfaces

| Locator | Finding | Disposition |
|---|---|---|
| `src/ck3chronicle/classification/normalize.py:721-759` | `legacy_diagnostic_lead()` explicitly recreates v4.6 lookup behavior. | Remove when clean model revision is published. |
| `src/ck3chronicle/classification/inference.py:12-25,84-105` | Imports and performs dual current/legacy lead lookup (call at `:89`). | Retain matcher; remove legacy lookup. |
| `src/ck3chronicle/parser/log_blocks.py:19-21,73-98` | `_HEADER_RE_TWO` fallback exists for old Chronicle fixtures (use at `:86-97`). | Remove unless reviewed real CK3 evidence proves it current. |
| `src/ck3chronicle/parser/log_blocks.py:27-46` | `TimestampedLogBlock` contains old-fixture provenance defaults. | Make real lexer fields explicit, then remove defaults. |
| `src/ck3chronicle/db/repository.py:1546-1574` | No-caller `replace_canonical_parse()` compatibility adapter. | Expunge. |
| `src/ck3chronicle/cli.py:676-687` | No-caller `_log_type_from_relpath()` from unsupported multi-log parsing. | Expunge. |
| `src/ck3chronicle/parser/extractors/__init__.py:111-121` | No-caller multi-log extractor dispatch. | Expunge with extractor directory. |
| `src/ck3chronicle/cli.py:1242-1425` | `_cmd_process_pending_wide_legacy()` is not registered with the CLI. | Expunge dead implementation. |
| `src/ck3chronicle/cli.py:2557-2569,2598-2610` | `--session` is explicitly a compatibility alias for `--run` in report/errors. | Remove aliases; retain canonical Run ID spelling. |
| `src/ck3chronicle/cli.py:869-950`, registration `:2533-2552`, and `src/ck3chronicle/db/repository.py:2840-2896` | Database-backed review queue. | Replace with the native per-Run review shard; do not keep both stores. |
| `src/ck3chronicle/config.py:12-15` | Python `<3.11` `tomllib` fallback despite `pyproject.toml:10` requiring Python `>=3.11`. | Expunge unreachable compatibility dependency. |
| `src/ck3chronicle/reporting.py:15-40` | Old-database/run-metadata backfill fallback. | Remove in fresh-generation reporting path. |
| `src/ck3chronicle/ingest.py:35-121` | Calls itself a compatibility API, although manual/recovery capture is a real current need. | Replace/rename as one deliberate current API; do not preserve merely for compatibility. |
| `src/ck3chronicle/models/issue.py:97-116`, `src/ck3chronicle/models/parse.py:33-57`, `src/ck3chronicle/parser/service.py:329-365`, `src/ck3chronicle/db/repository.py:1154-1189,1368-1374`, and `src/ck3chronicle/cli.py:715-729` | “Issue cluster” currently means exact-signature aggregate, not related errors. | Rename/refactor to exact-template aggregate. Do not delete useful counting; reserve “related-error cluster” for a future causal/file/concept analysis feature. |

Obsolete imported learner/evaluator coupling is located here:

| Locator | Finding | Disposition |
|---|---|---|
| `tools/template_learning/build_review_pack.py:1-446` | Frozen-252 review-pack utility; args/main are `:388-442`. | Expunge. |
| `tools/template_learning/blind_review/build_blind_stratified_sample.py:1-336` | Historical blind sample builder. | Expunge. |
| `tools/template_learning/blind_review/compare_blind_adjudication.py:1-279` | Historical blind adjudication comparator. | Expunge. |
| `tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:1-376` | Historical postfix evaluator. | Expunge. |
| `tools/template_learning/evaluate_unseen_session.py:1-408` | Uncommissioned preserved evaluator. | Expunge. |
| `tools/template_learning/mine_symbol_suffixes.py:18` | Imports the unseen-session evaluator. | Remove coupling; retain the miner only if a current contract-learning requirement justifies it. |
| `tools/template_learning/analyze_script_system_layers.py:1-131` | Standalone exploratory analyzer. | Conditional review; it has no runtime authority. |
| `tools/template_learning/learn_error_templates.py:1326-1482` | `evaluate_frozen_oracle()` hard-binds learning to the 252 candidate/adjudication. | Remove frozen-oracle pass while retaining structural learner. |
| `tools/template_learning/learn_error_templates.py:1574-1634` | Requires `--oracle-root` and invokes that evaluation. | Remove argument/call. |
| `tools/template_learning/incremental_template_registry.py:366-390` | Every revision build invokes the same frozen oracle. | Remove oracle/evaluator coupling. |
| `tools/template_learning/incremental_template_registry.py:500-536` | Requires and forwards `--oracle-root`. | Remove argument/call while retaining justified incremental registry behavior. |
| `tools/template_learning/README.md:3-5,13-17,25-28` | Declares preserved WIP evaluator/projection tooling as owned method. | Rewrite to current structural-learning/contract-review method. |
| `tools/template_learning/AGENTS.md:3-5` | Names blind review and projection catalog generation as owned work. | Rewrite with the architecture transition. |

The old projection/evaluator contract tests already appear as deletions in the
current working tree, so they have no live working-tree line ranges to preserve.
They must not be restored or translated merely to maintain historical coverage.
The active recovery test locators that still encode projection/migration were
listed above and must be rewritten from the final owner-approved requirements.

### Documentation authority that must be reconciled in the transition commit

Not every sentence below should be erased: dated operational findings may
remain as explicitly historical evidence. Current guidance, ownership maps, and
future requirements must stop authorizing projection, migration, backfill, or
in-place reclassification.

| Document locator | Conflicting current text |
|---|---|
| `AGENTS.md:27-39` | Ownership/commit map still names migrations and projection catalogs. |
| `README.md:54-62` | Describes separately approved migration and `backfill-session`. |
| `docs/TRUSTED_RUN_SPEC.md:254-281,327,420,453-464` | Requires supported migration/reparse and migration gates. |
| `docs/MODEL_QUALITY_AND_PROMOTION.md:145-146` | Defines reclassification as an explicit historical operation. |
| `docs/REQUIREMENTS_AND_TESTING.md:39,96,119-124` | Requires migration test classes and migrate/reopen behavior. |
| `docs/PROJECT_STATUS.md:78,108-135,194-204` | Treats projection/migration/backfill as current state or debt. Historical measurements may remain only when clearly marked superseded. |
| `docs/PROJECT_PLAN.md:106,147-165` | Treats schema migration and compatibility as planned product capability. |
| `docs/RELEASE_READINESS.md:23-62,91-103` | Makes supported forward migration a public-release gate. |
| `docs/DATA_COMPATIBILITY_AND_OPERATIONS.md:26,75,129-146,167-196,230-334` | Defines an explicit migration framework and compatibility aliases. |
| `docs/ARCHITECTURE_AND_DATA_LINEAGE.md:118,179,189-205` | Contains a staged migration proposal. |
| `docs/INGESTION_OPERATIONAL_RECOVERY_PLAN.md:8,140-206,260-300` | Records projection/migration/backfill operational work. Keep facts historical; supersede prescriptions. |
| `docs/CURRENT_HANDOFF.md:43-50,82-109,148-198,263-269` | Current handoff still routes migration/backfill/projection work. |
| `docs/REPOSITORY_AND_BACKUP.md:34-35` | Lists migrations and semantic projection as active repository assets. |
| `docs/WORKSPACE_ROUTING.md:25,83` | Routes database migrations as current owned source. |

This locator appendix converts the recovery review into a checkable removal
boundary. Execution is complete only when repository searches show no active
raw-252 authority, sample-absence default, semantic projection/mapping stage,
old regex taxonomy/fallback, in-place schema migration, historical backfill or
reparse/reclassification route, compatibility alias, or obsolete evaluator
coupling—and the replacement direct error-contract path has passed the
real-evidence proof defined above.
