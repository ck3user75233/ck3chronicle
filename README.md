# ck3chronicle

ck3chronicle is a standalone, local CK3 run-intelligence product for modders.
It protects the useful output of completed runs, turns `error.log` into durable
and reviewable diagnostic history, and provides libraries for comparison and
bounded source context. Cautious action guidance remains planned.

The first product milestone is **Trusted Run**: observe one CK3 start-to-exit
lifecycle, protect its live `error.log`, process it into SQLite, preserve
unresolved evidence for review, and generate reports from stored records.

## Target flow

1. The watcher observes the configured CK3 process and copies the live
   `error.log` and full `debug.log` after that process exits. It extracts the
   ordered active playset and writes `playset.json` with both content hashes.
2. Deferred processing validates and deduplicates the protected copy, recognizes
   log emissions, and classifies recovered diagnostics against approved error
   contracts.
3. Selected template and provisional assignments become compact SQLite records,
   distinguished by match status. Unassigned/unresolved evidence goes to one
   native review shard for the resulting Run ID.
4. Reports query SQLite and do not depend on the retained source log.

CK3 and mod sources are read-only. A newly associated crash folder may provide
only its root `exception.txt`; its copies of principal logs are ignored.

The watcher playset producer is delivered. Its template includes the base game,
DLCs and mods in emitted mount order, with descriptor names and paths. Run-owned
SQL persistence and review-manifest ingestion are implemented by Task 07.
See the [watcher handoff](docs/WATCHER_ACTIVE_PLAYSET_HANDOFF.md) for the format,
verified example, failure behavior and pipeline receiving requirements.

## Current development state

Task 07 ingestion, per-Run lineage, ordered playsets and raw retention are
implemented. [Task 07D's current handoff](docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
documents the dedicated shared database handler used by watcher, manual CLI and
application clients. Windows named pipes connect callers to one host and one
SQLite worker per exact database file. Hashing/parsing/classification stay outside
that worker. Request states are `ENQUEUED`, `COMPLETED` and `NOT_COMPLETED`;
duplicates return the existing Run ID as non-completion, and contention waits.

[Task 07E](docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md) adds shared rotating JSONL logs,
request-ID correlation through watcher/preparation/database execution, traceback
evidence and bootstrap diagnostics. Its handoff records the owner-authorized
September 30 activation and includes operator queries. Future runtime changes use
the shared logging owner and run `tools/check_runtime_logging.py`.

SQL schema and native-review manifest are version **3**; playset format is **1**.
Missing playsets are unavailable; invalid supplied playsets warn and permit the
valid error log to proceed. Daily watcher maintenance preserves configurable
30-elapsed-day raw expiry. Selection and the existing Run writer are unchanged.
Removed providers and generation replay remain excluded.

Commands are `runs`, `report`, `ingest`, `watch`, `capture`, `doctor` and `observe-logging`;
`watch --once` retains manual error-only copying. The [earlier watcher activation](docs/WATCHER_LIVE_ACTIVATION_HANDOFF.md)
and [September 30 handler/logging activation](docs/TASK07E_RUNTIME_LOGGING_HANDOFF.md)
are historical records, not evidence of current live status.

[Task 08A.1](docs/TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md) delivered reusable stored
diagnostic queries and history analysis. [Task 08A.2](docs/TASK08A_2_SOURCE_SEARCH_HANDOFF.md)
delivered playset source search and context integrated with those queries.
[Task 08B reports and CLI](docs/TASK08B_REPORTING_HANDOFF.md) implement five presets,
text/JSON/offline HTML and a linked verbose source appendix. The source-path
traversal repair is delivered; report queries reuse both libraries.
The query, clarity, navigation and browser corrections are recorded in the handoff.
The follow-up adds a full genuine trailing-five investigation, all nine syntax
selectors from unchanged archives and an owner-authorized missing-file fixture.
Live Trusted Run milestone acceptance remains separate.

Delivery does not establish complete verification. The [08B follow-up](docs/TASK08B_REPORTING_HANDOFF.md)
uses a fresh unchanged backup with seven eligible genuine Runs and fourteen older
timestamp exclusions. Five genuine archived logs separately verify syntax and
missing-playset behavior. The labelled two-entry fixture changes only LOCATOR
paths and preserves genuine recorded playset membership. Absent failure
and simultaneous eleven-Run cases remain unverified. Duplicate-ingestion handling
belongs to the pipeline; reporting adds no second duplicate-detection policy.
Explicit Run-result replacement and full Trusted Run milestone acceptance remain
separate. Consult
[project status](docs/PROJECT_STATUS.md) before operational work.

The current implementation still reads the ignored repository-root
`config.toml`, created from `config.example.toml`. The approved target is an
exact `--config <path>` or one fixed LocalAppData `ck3chronicle/paths.toml`
bootstrap with no path discovery. Until that transition is implemented, do not
mistake the current bootstrap for the target contract.

Use the repository `.venv`. Tested PowerShell commands and sandbox guidance are
in [`docs/DEVELOPMENT_ENVIRONMENT.md`](docs/DEVELOPMENT_ENVIRONMENT.md).

Read-only development commands include:

```powershell
$python = (Resolve-Path -LiteralPath '.\.venv\Scripts\python.exe').Path
& $python -I -B -m ck3chronicle.cli --help
& $python -I -B -m ck3chronicle.cli watch --help
& $python -I -B -m ck3chronicle.cli ingest --help
```

Before starting the watcher, capturing evidence, processing pending captures,
or writing to the production database, read the current status and handoff.
Never use a runtime-mutating command merely as a smoke test.

## Run investigations and exported reports

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
$package = '68f1ae5db205ab46afef9c4d'
# Omit --database to use the existing watcher.database configuration.
& $python -B -m ck3chronicle.cli runs --database C:/evidence/run.sqlite3 --package-id $package --limit 10
& $python -B -m ck3chronicle.cli report latest --database C:/evidence/run.sqlite3 --package-id $package --preset frequent
& $python -B -m ck3chronicle.cli report latest --database C:/evidence/run.sqlite3 --package-id $package --custom --query examples/reporting/file-path.json
& $python -B -m ck3chronicle.cli report latest --database C:/evidence/run.sqlite3 --package-id $package --custom --query examples/reporting/failed-context-switch.json --format html --verbose --output .codex-tmp/reports/context-switch.html
& $python -B -m ck3chronicle.cli report 20261003-74G2EB --database C:/evidence/run.sqlite3 --preset symbol --query examples/reporting/symbol-template.json --format json
```

Replace the example database with an existing initialized file. Named Runs infer
their package from stored lineage and reject conflicts; `latest` requires an
explicit package. No model is loaded. `runs` orders by original source-log
modification time and discloses excluded Runs before pagination.

The `symbol-template.json` example selects the whole stored trigger-error
template: every matching key, reason and script location remains eligible.
It demonstrates template selection and separate per-diagnostic Run history.
Template investigations lead with the stored placeholder pattern and combined
per-Run counts, followed by explicitly labelled individual diagnostics. A record's
`template` match status means it matched a template; the record is still a specific
diagnostic with bound values.
For ordinary phrase or token search, use [message-search.json](examples/reporting/message-search.json)
with `report latest --package-id ID --custom --query examples/reporting/message-search.json`.
`refinement.message` searches the complete diagnostic, including template literals
and populated slot values. Results show where each term matched, the assigned
template for each diagnostic, and counts across matching templates before display
limits. No slot-specific query is needed. Templates are stored classifications of
records; the search does not classify them again.
The context-switch example uses this same content search. Additional binding/message conditions narrow a template query and are
optional; the template example has neither. Display limits affect only how many
matching records are shown, not the totals.

Every report opens with its question, expected behavior, actual result and relevant
evidence together. Template patterns, Run counts and diagnostic examples appear
inside that explanation; named links jump directly to full entries and verbose
source excerpts. Query details and the reading guide are expandable.
[Reading the examples](examples/reporting/README.md)
distinguishes the broad template example, message search and deliberately narrow
checks. [Each consumer check](examples/reporting/checks.json) has its own question
and expected outcome, including intentional empty results and rejections.
Visible file tables pair mod paths with names and load-order numbers from the
evidence Run's recorded playset. Base-game/DLC paths have no mod-name prefix;
multiple candidate mods remain separate. Original diagnostic text is preserved.

Presets are `hotspots`, `frequent`, `syntax`, `new`, and `symbol`. `--query`
refines a preset while retaining its defining condition; `--custom --query PATH`
is the explicit independent path. `symbol` needs a template/text/binding selector.
`syntax` is available only for its researched package/model. Valid no-match
queries succeed; unavailable required evidence fails with labelled partial matches.

Text and JSON default to stdout. `--output PATH` writes UTF-8; HTML requires it.
An execution error returns an error response and a nonzero exit code. Unexpected
Python exceptions include the operation/stage, exception type, message and
traceback. If the error report itself cannot be written, its details go to stderr.
Zero matching diagnostics is a successful result. Ripgrep is used for current
source-content searches; ordinary stored-message searches do not invoke it.
`--verbose` adds numbered source excerpts and writes `NAME-sources.html` beside
an HTML report. Keep both files together; all styling is local and links are
relative. `--limit` defaults to 50; `--historical-limit` defaults to 20. Full
totals and rankings are computed before display limits. JSON retains complete
analytical rollups; text/HTML disclose the bounded ranking and diagnostic views.

History defaults to up to five preceding/five subsequent eligible Runs. Use
the displayed Run -5…+5 positions to see which Runs exist; missing positions say
**Not available** and contribute neither zeros nor failed reads. JSON exposes
the same positions through `window.positions`. Use
`analytics.trailing_runs` for a trailing window, or `--no-history` to omit recent
commentary. Newness is relative to successfully read included predecessors.
Previously observed entries absent from the selected Run have separate totals.
An explicit positive occurrence minimum removes those zero-count entries.

Sources default to each Run's recorded playset. For optional context, repeat
`--source-root C:/my-mod` or `--source-directory common/on_action`; add
`--no-recursive` or supply a full selection with `--source-context PATH`.
Required member/file/content filters belong in the query's `scope.source`.
Matching files show separate load order, mod name, path and line columns, using
the playset's raw order numbers. **Resolved** means one or more matching paths;
**File not found** means none after a completed lookup. For each file/line,
the last matching playset member in load order is labelled **Error source**, under
the owner's reporting rule. All matching copies remain visible. JSON exports the
same decision in each diagnostic's `file_line_sources`. This uses the effective
source scope and is evaluated before separate file-content filtering. Files outside
the playset have no load order, so this rule cannot assign them an order-based source.

Displayed source files also receive a bounded encoding-header validation. Known
double-BOM, BOM-mojibake, displaced/conflicting signature, replacement-character
and BOM/byte-mismatch findings appear as **Critical Encoding issues (reason)**.
A found path can show **Resolved / Critical Encoding issues (double BOM)**;
resolution, diagnostic counts and source attribution remain separate. JSON keeps
the issue codes, severity, byte offsets and affected candidates in
`encoding_validation`. Header checks inspect the first 4,096 bytes, with scope
and unavailable/undetermined outcomes disclosed; a successful decode alone does
not establish a clean file. Sources are never rewritten. Library callers can
use `SourceSearch.validate_sources(selection, run_id=...)` to validate every file
in a requested selection, independently of a report's display bounds.

A shared `ck3chronicle.decoder.Decoder` development API is under evaluation.
Caller integrations are kept in disposable candidates; production search,
excerpts and ingestion retain their existing decoding until a coordinated
release cutover. The API uses a known encoding when supplied and detects only
unknown encodings. Standard Python codecs preserve undecodable bytes, with visible
escapes for display; low-confidence detection fails with a reason. Original bytes
are preserved, and double BOMs block content reading without header repair.
See [the decoder design](docs/TASK08C_ENCODING_RECOMMENDATION.md) for current
scope and genuine disposable-parser/source-search comparisons.

`scope.has_source_reference` checks whether a file path can be recovered from the
stored diagnostic, including path-valued `<LOCATOR>` bindings or literal paths.
It does not require that file to exist today. `scope.source.members` instead
requires a referenced file to be found under the selected member's current root,
using the Run's recorded playset. A record with no usable matching path is excluded
normally, with no warning or partial-result entry. Optional unfiltered context
keeps such a diagnostic visible.

The `synthetic-missing-files` example demonstrates that an identifiable stored path
can have no disk candidate while its diagnostic remains readable. It links the
two-entry log and playset JSON. Path-only predicates, including `scope.source.files`,
`relative_path`, `filename`, directory scopes and `referenced_paths`, select stored
references independently of disk existence. A query for an unmentioned path
completes with zero matches. Adding member/root/content predicates requires the
corresponding current candidate evidence; missing individual files are still
ordinary nonmatches. The generated `outcomes.html` page tracks
the new checks and remaining gaps with links to their explained reports.

Use a **game-relative path** for the usual path filter, for example
`"scope": {"source": {"relative_path": {"exact": ["/common/scripted_effects/some_file.txt"]}}}`.
The optional leading `/` is accepted by `relative_path.exact` and `directories`;
`common/...` and `/common/...` mean the same location beneath each selected source
root. Forward slashes and backslashes are accepted. The filter matches recorded
paths; candidate lookup checks that location in every member of the Run's recorded
playset by default. It inventories only the named parent folder, without recursion,
and shows all matching copies with their mod names and recorded order numbers.
The same filename in a different directory does not match. Explicit physical
`roots`/`files` and literal text conditions keep their separate meanings.
Try the [relative-path example](examples/reporting/relative-path.json):

```powershell
& $python -I -B -m ck3chronicle.cli report latest --database C:\path\runs.sqlite3 --package-id PACKAGE_ID --custom --query examples/reporting/relative-path.json --verbose --format html --output C:\path\relative-path.html
```

To find messages whose recorded paths have no current file in the chosen source
scope, use the separate [unresolved-path query](examples/reporting/unresolved-paths.json):

```powershell
& $python -I -B -m ck3chronicle.cli report latest --database C:\path\runs.sqlite3 --package-id PACKAGE_ID --preset frequent --query examples/reporting/unresolved-paths.json --format html --output C:\path\unresolved.html
```

Its condition is `"scope": {"source": {"resolution": "unresolved"}}`. Use
`"resolved"` for messages with at least one current file candidate. These filters
exclude messages with no usable recorded path; to select those, use
`"refinement": {"has_source_reference": false}` instead. Each recorded reference
has a current resolution in exported `reference_resolution`, also shown in text
and HTML. Incomplete searches are unknown, not evidence of a missing file.
Resolution is measured at report generation, not permanently stored as a fact
about the original Run. Roots/members restrict where resolution is tested;
directory/path predicates restrict the references. An unresolved path may exist
elsewhere. Ordinary path matching still does not require a file to exist.

An emission with no file path is a complete diagnostic. Reports label its source
lookup **not applicable**, without a warning or incomplete-evidence claim. JSON
records expose `source_path_status: "no_path"`. If none of the selected emissions
supplies a path, no playset/root lookup is performed; source counts are zero.
Actual lookup failures for other records do not attach to pathless emissions.

Reports disclose the number of file names/paths and folders checked by each
source lookup. **Source coverage** gives the actual directories, recursion setting,
cache use, candidate count and files selected for a content check. Folder counts
include the starting directories and empty folders. These are per-search counts
of unique physical paths, not cumulative session counters. Known file paths can
narrow lookup to their parent folders, so those counts need not equal the entire
root tree. Incomplete coverage remains labelled; stored-only selection does no
filesystem search. The independent real-tree verification is reproducible with
`tools/check_source_recursion.py --help`.

The symbol preset's required template/typed-value input is validated before any
database request. Preset conditions and additional filters are ANDed: valid
mutually exclusive filters complete successfully with zero matches. The exported
`refinement.all` clauses retain the preset definition alongside user refinements.
Missing inputs and incompatible execution controls still fail validation.

See the [08B handoff](docs/TASK08B_REPORTING_HANDOFF.md) for defining conditions,
all filters, exact-identity selection, the worked investigation, output examples
and verification limits. Reusable queries are in [examples/reporting](examples/reporting).

## Project documentation

- [Current Task 07D database and ingestion handoff](docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md)
  — APIs, handler lifetime, three states, watcher integration, schema/review 3,
  playset 1, daily maintenance and verification.
- [Historical Task 07 evidence](docs/TASK07_INGESTION_AND_RETENTION_HANDOFF.md)
  — original native verification and limitations.

- [Task 06 implementation handoff](docs/TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md)
  — storage/review APIs, physical generation/shard layout, completion and cleanup,
  historical native evidence and predecessor examples; use the current 07D
  handoff for runtime APIs.

- [Approved Error Contract](docs/ERROR_CONTRACT_SPECIFICATION.md) — owner-approved
  assignment, identity, rendering, source/emitter and lineage rules.
- [Task 04 handoff](docs/TASK04_ERROR_CONTRACT_HANDOFF.md) and
  [revised Task 05 prompt](docs/05_ERROR_CONTRACT_IMPLEMENTATION.md) — historical
  predecessor scope. [Task 05 implementation handoff](docs/TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md)
  records the delivered shared matcher integration, selected-only binding,
  serializable contracts, native verification and installed-resource proof.
- [Shared matcher delivery](docs/LEARNER_PARSER_PIPELINE_HANDOFF.md),
  [API](docs/SHARED_MATCHER_API.md) and
  [independent verification](docs/SHARED_MATCHER_PIPELINE_VERIFICATION.md) —
  immutable package delivery and predecessor verification. Task 06 integrated
  and selected v45; the later Task 07 handoffs record runtime integration.
- [Unmatched learner investigation](docs/LEARNER_UNMATCHED_REVIEW_ROOT_CAUSE_RESULTS.md)
  and [cumulative learning experiment](docs/LEARNER_ALL_LOGS_V42_RESULTS.md) —
  native case evidence, same-version additive learning and isolated candidates;
  neither changes the selected runtime package. The
  [formal Pipeline Team reply](docs/LEARNER_TASK06_UNMATCHED_REVIEW_REPLY.md)
  records the original 122-case investigation with complete candidate assignments,
  before the subsequent v45 integration.
- [Next learner / decoder release](docs/learner-next-release/README.md) and
  [integration handoff](docs/learner-next-release/HANDOFF.md) — running improvement
  list, verified v60 baseline, pending decoder integration and final pinning.
- [Learner v45 release delivery](docs/LEARNER_RELEASE_V45_RESULTS.md) —
  the 73-log replacement build, native model evolution and schema-5 / API-v2
  package assessment preceding the [completed Task 06 integration](docs/TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md).
- [Owner product intent](docs/OWNER_PRODUCT_INTENT.md) — governing product
  purpose, boundaries, vocabulary, and trust rules.
- [Architecture and data lineage](docs/ARCHITECTURE_AND_DATA_LINEAGE.md) — target
  components, data ownership, and transaction boundaries.
- [Project plan](docs/PROJECT_PLAN.md) — milestones, dependencies and current sequencing.
- [Team governance](docs/team-governance/README.md) — core team responsibilities,
  component boundaries, integration ownership and Advisory's role.
- [Project status](docs/PROJECT_STATUS.md) — current implementation truth.
- [Current handoff](docs/CURRENT_HANDOFF.md) — live uncommitted work and the
  continuation point.
- [Banned ideas](docs/BANNED_IDEAS.md) — explicitly rejected designs.

### Detailed policies pending reconciliation

The following detailed specifications and policies retain useful requirements,
but their retention, projection, migration, compatibility, and historical-
reprocessing sections require reconciliation during classification recovery.
Where they conflict, current owner intent, architecture, and banned-design
decisions govern.

- [Trusted Run specification](docs/TRUSTED_RUN_SPEC.md) — detailed first-
  milestone requirements; it requires reconciliation after classification
  recovery before serving as the next implementation plan.
- [Requirements and verification](docs/REQUIREMENTS_AND_TESTING.md)
- [Data compatibility and operations](docs/DATA_COMPATIBILITY_AND_OPERATIONS.md)
- [Model quality and promotion](docs/MODEL_QUALITY_AND_PROMOTION.md)
- [Release readiness](docs/RELEASE_READINESS.md)

Runtime logs, databases, review shards, corpora, workbooks, and generated
evaluation results remain outside Git. Tests derive from current owner-directed
requirements; historical tests do not create product scope.
