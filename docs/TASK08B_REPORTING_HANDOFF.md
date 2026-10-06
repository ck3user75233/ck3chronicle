# Task 08B — reports and investigation experience

## Combined-release Reporting repairs — 2026-10-05

R1 repeat-template compatibility, R2 preserved-byte exports and R5 ordinary
missing-time Run eligibility are repaired. The new application artifact, genuine
before/after checks, exact commands and remaining owners are recorded in the
[Pipeline repair receipt](learner-next-release/PIPELINE_RECEIVING.md#reporting-repair-delivered--2026-10-05).
Pipeline receiving and owner activation remain separate. R2's prior nonblocking
disposition is unchanged; its repair is now delivered. R4 new-package syntax
selectors remain separately owned Reporting work, with explicit rejection intact.

Current interface corrections: `runs` includes missing-time Runs with an unavailable
date and labelled Run-ID ordering. Named reports work with and without optional
history; unplaceable history/newness is unavailable, never invented. All-Run
message search uses `DiagnosticAnalysis.search_runs`, independently of history
windows. The [query handoff](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md) records the fields.
These replace the older checklist's source-time listing restriction.

JSON serialization preserves native strings and identities with reversible
surrogate escapes, while retaining valid Unicode. HTML/text use the shared
`decoder.display_text` representation and label byte escapes; copyable identity
JSON remains reversible. Both main and appendix buffers are UTF-8 encoded before
either destination is opened. Native matching, storage, offsets and decoder
processing/header semantics are unchanged. Original evidence and receipts remain
intact; no synthetic acceptance data or failure injection was used.

## Earlier delivery status — 2026-10-04

**08B implementation is complete, including the owner's review corrections.
No known assigned feature or documentation work remains.** This is the reporting
delivery statement, not a claim of full live Trusted Run acceptance or execution
of every possible runtime fault. Commits and pushes remain deferred by instruction.

This section records the earlier checklist. Dated correction records
below retain the work history; their older counts and unfinished-work statements
are superseded by this section and the latest verification immediately below it.

Owner clarification on runtime faults: these mean failures to execute an
operation (for example a source-search process error or a database-worker
connection error). They belong at the caller's error boundary. They are not
diagnostic search results or outstanding analytical features. Stored diagnostic
content search does not invoke ripgrep; ripgrep searches current source contents.
Python checks source encoding and reads excerpts. An unreadable/unsupported file
is a per-file outcome with a reason, not evidence of a crashed search process.
Malformed CK3 syntax is still searchable text; reporting does not parse sources
to decide whether their CK3 syntax is valid. Busy database requests queue in the
existing handler; connection loss means runtime communication failed, not a
busy-queue rejection. No new admission or recovery policy is introduced.

### Deliverables

| Deliverable | Delivered behavior | Where to review |
|---|---|---|
| Root `runs` command | Configured/explicit database, explicit package, source-time ordering, timestamp exclusions, text/JSON and pagination after eligibility. | [CLI registration](../src/ck3chronicle/cli.py), [adapter](../src/ck3chronicle/reporting/cli.py), [Run example](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/runs-current.html#explanation) |
| Root `report` command | Named Run or `latest`, package validation, preset or explicit custom query, query files, display limits, history controls and verbose output. | [Commands and destinations](#commands-and-destinations), [README usage](../README.md) |
| Five presets | Script/file hotspots, frequent diagnostics, the nine researched syntax selectors, newly observed diagnostics, and symbol/template investigation. Refinements preserve the preset condition; valid opposing filters return an empty result. | [Preset definitions](#presets-and-refinements), [implementation](../src/ck3chronicle/reporting/presets.py) |
| Composable searches | Mod/member, relative file path, exact record, template reference/text, typed binding and grouped whole-message conditions. Ordinary content search includes literals and slot values; results show match origins and assigned templates. | [Query examples](../examples/reporting/README.md), [content-search report](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/message-unrecognized.html#explanation) |
| Text, JSON and offline HTML | Shared analytical results; effective query/scope, totals, stored messages, classification, typed values, review context, bounded detail and integrated plain-English explanation/navigation. | [Report index](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/examples.html), [presentation](../src/ck3chronicle/reporting/presentation.py) |
| History and worked five-Run investigation | Actual counts, fractions, window-relative newness, separate previously observed identities, per-Run contributors and file rankings. Requested -5…+5 positions explicitly show unavailable Runs. | [Five-Run investigation](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/worked-five-runs.html#explanation), [history positions](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/history-positions.html#explanation) |
| Source files and verbose appendix | All returned candidates, mod names, raw load order, paths and lines; last-load-order source per file/line; scoped file/folder counts; explicit resolution outcomes. Linked current-source excerpts ±10 lines, escaped HTML and local assets. | [Relative-path report](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/relative-path-all-members.html#explanation), [verbose report](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/worked.html#explanation) |
| Consumer verification | Actual root CLI against disposable copies of genuine stored data/current sources; authorized two-entry LOCATOR fixture separately labelled; format/limit checks, browser links/layout, recursion measurements, CLI/import/logging checks and stored-data I/O trace. | [Latest verification](#whole-message-search-and-concrete-outcome-corrections--2026-10-04), [outcome register](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/outcomes.html), [I/O result](../.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/investigations/stored-data-io.html#explanation) |
| Handoff and documentation | This handoff, README, query examples, owning-library handoffs, current status/handoff/plan and reporting ledger. Analysis remains reusable outside report templates; no new dependency. | [Project status](PROJECT_STATUS.md), [current handoff](CURRENT_HANDOFF.md), [reporting ledger](TASK08_SCOPE_REVIEW.md), [interfaces/dependencies](#interfaces-implementation-and-dependency-choice) |

### What is not verified or not part of this delivery

Two fault groups were not encountered and are **not claimed as executed checks**:

1. A database-handler operation/transport error while reading a report or comparison.
   Handling was inspected. The related Run-disappears/metadata-changes transition
   was also inspected but not manufactured. Empty results and missing window
   positions are already verified normal outcomes.
2. An actual ripgrep launch failure or abnormal/error exit. Handling was inspected.
   A file that cannot be read/decoded is instead a per-file source outcome:
   retain the file and reason, and disclose that its contents were not searched
   or could not supply an excerpt. Those outcomes were also source-inspected;
   they are not process-crash claims. Missing files, no-path emissions and genuine
   missing playsets have executed checks. SQL diagnostics are already decoded.

These are limits on observed verification, not remaining feature implementation
or requirements to fabricate failures. Full live Trusted Run acceptance belongs
to its separate milestone. Commits/pushes are intentionally not performed.
Syntax support remains bounded to the researched package/model. Reports do not
provide an atomic snapshot across separate database requests and current source
reads, and JSON can contain large analytical rollups despite a small display limit.

## Caller exception boundary — 2026-10-04

The owner's wrapper suggestion prompted inspection of the actual caller boundary.
Expected source/handler errors already reached the CLI's structured failure
response. An unexpected Python exception (for example malformed process output
or a programming error) could previously escape with only a raw traceback.
That bounded gap is now closed in `reporting.cli`: `runs` and `report` catch
ordinary `Exception` at their command boundary. Existing domain statuses/exit
codes remain; unclassified exceptions return `operation_failed`, exit 1, with
request, stage, exception class, message and traceback. Interrupts and `SystemExit`
are not swallowed. The libraries and database worker keep their existing contracts.

Text/HTML expose operation and exception details; HTML escapes the traceback.
The shared logging event receives `exc_info` without configuring any new logger.
If the error renderer or destination itself fails, the boundary writes the
original error envelope and the output exception to stderr as plain JSON and
returns exit 1. It does not retry rendering, invent an empty result or claim
recovery. Like any in-process exception boundary, it cannot run after the CLI
process itself is forcibly terminated or its interpreter terminates outside
Python exception handling.

Verification uses the existing genuine root-CLI selection/package/error-response
group and the 07E logging ownership/import checks. No process crash, mock response
or injected exception is manufactured. The unexpected-exception and double-error
branches are inspected, not claimed as executed failure tests. This is ordinary
caller error handling; the two unencountered fault groups above remain evidence
limits rather than feature work or a request for more game logs.

The genuine CLI group passed in 17.913 s with disposable exports under
`.codex-tmp/task08b/41163857495a44fc97da8c7c4fc7018a/`. Logging ownership, isolated
imports and whitespace checks pass. The execution-error reading guide explicitly
identifies a stopped operation and avoids describing a programming exception
during validation as invalid user input.

## Whole-message search and concrete outcome corrections — 2026-10-04

The normal content-search workflow is `refinement.message`: search the whole
stored diagnostic, including both template literals and populated slot values.
It already selected that content; the earlier explanation incorrectly pushed
users toward slot-specific or literal-pattern searches. Templates are assignments
attached to matching records. They do not produce errors. No new classification,
slot-only mode or special query for discovering templates has been introduced.

The existing contract renderer now exposes `render_segments`, using the same
selected layouts as `render`/`render_regions`. Analysis exports `message_matches`
with character spans, matched text, region and literal/slot origin, including
typed slot IDs. Positive terms from satisfied AND/OR branches are described;
negative clauses remain in the effective query. Casefold offsets map back to
original characters, and a phrase crossing literal/slot boundaries retains both
origins. Summaries in `rollups.message_matches` count exact records, occurrences
and assigned templates before display limits, separately for selected/per-Run/
window views. Origins can overlap; bucket totals are not a replacement for unique
diagnostic totals. HTML/text show these origins and an assigned-template column.
JSON carries the same reusable analysis data. No dependency was added.

Ordinary command and query:

```powershell
.\.venv\Scripts\python.exe -I -B -m ck3chronicle.cli report latest --database C:/evidence/run.sqlite3 --package-id 68f1ae5db205ab46afef9c4d --custom --query examples/reporting/message-search.json --format html --output C:/evidence/message-search.html
```

```json
{"refinement":{"message":{"contains":"unrecognized"}}}
```

Genuine latest Run `20261003-74G2EB` supplies two explained examples:

- `message-unrecognized`: 62 exact diagnostics / 62 occurrences; literal matches
  in records assigned to four templates.
- `message-context-switch`: 51 exact diagnostics / 245 occurrences; the phrase
  matches REASON values in records assigned to four templates.

Both use the same content filter. Eight diagnostics are displayed; a zero-display
repeat preserves every total and template association. The contrived
`bound-phrase-is-not-template` acceptance example is withdrawn. Its former link
now explains the withdrawal and leads directly to the ordinary content search;
original CLI evidence is retained unchanged.

The owner's earlier outcome corrections are also implemented:

- `history-positions` shows Run -5 through +5, with 0 selected and unavailable
  positions explicitly labelled. Seven genuine Runs supply three neighbors on
  each side and four unavailable positions. Existing full-side checks remain;
  eleven simultaneous Runs are not an acceptance prerequisite. JSON exports
  `window.positions`; missing positions do not enter counts/fractions.
- Run disappearance/metadata change between listing and reading is distinguished
  from a handler operation/transport error. Comparisons export `unavailable`
  and `coverage.comparison_unavailable`; actual handler errors retain `ReadError`
  and their operation/exception information. This rare transition was inspected,
  not manufactured or claimed exercised. Empty diagnostic reads remain success.
- `tools/check_reporting_io.py` traces a real root-CLI invocation and its cold
  disposable database worker. The successful trace observed 667 Python audit
  events, two SQLite opens (disposable file and handler memory database), no raw
  log/model artifact access, and only the normal handler child command. Non-code
  file opens were the query/output, disposable handler log, config and null
  device. This is Python I/O plus child-command observation, not a system-wide
  native trace. Inputs stayed present and unchanged.

Executed checks: genuine CLI groups 11 (content/provenance/formats/limits), 04
(grouped filters and template/binding selection), 02 (worked history/formats/
verbose links), and 12 (requested history positions) passed. A separate renderer
comparison preserved all 739 distinct messages from 123 earlier saved exports
(including the labelled LOCATOR fixture); no record was reclassified. Runtime
logging ownership and isolated CLI/reporting imports pass. Chrome checks inspect
the content searches, match details, history positions, I/O receipt links and
narrow layouts. The first browser assertion wrongly compared whitespace-normalized
`innerText` with original CRLF text; it now checks message `textContent` with HTML
newline normalization. The first I/O checker wrongly treated the handler's URI
and memory database as unexpected files; the corrected check explicitly accounts
for both. Neither attempt identified a reporting failure.

Evidence: `.codex-tmp/task08b/content-search/` contains the manifest, renderer and
browser receipts; CLI outputs are in `9a628541b00e4773967da22572cb72ef`,
`deda1a384b774b9cafd0e4262bbd9ba2`, `68f5cdbbea484fe8831a7480cb609519` and
`575614a5e6594b87b07f0753587db858` beneath `.codex-tmp/task08b/`. I/O receipt:
`.codex-tmp/task08b/io-trace/6f726df0935e4423bca7d5ccb9d8dbb5/`.

Five existing 08A.1 genuine SQL checks also passed in 14.525 s, with an added
assertion that a whole real diagnostic match spans both literals and slots;
the old contrived bound-value-versus-pattern case was removed. Receipt:
`.codex-tmp/task08a2/42f3ff1f95324a96bcdeb0f0924dd56a/`. Final bundle verification:
86 explained cases, 20,520 links, 16 named saved query outcomes and two explicit
unexercised fault groups. Five Chrome routes passed with eleven screenshots;
desktop match details and narrow summary layout were visually inspected.

Changed owners: contract rendering; reporting analysis, presentation, explanation
and CSS; genuine CLI checks; example/catalog/outcome builder and browser checker;
the I/O verification tool; README and current reporting documentation. The outcome
register now identifies two specific unexercised fault paths: database handler
operation/transport errors and source-search process launch/error exits.
SQL diagnostics are already decoded. Unavailable source roots concern current
file resolution/content/excerpts; a missing file or pathless emission is a normal
outcome. Ripgrep exit 1 means no match. These are verification limits, not invented
requirements to collect nonexistent data. `new-zero-count` is complete empty-set
verification. Full live Trusted Run acceptance remains separate. No production
inputs/processes/package selection, commits or pushes were changed.

## Earlier correction record: timestamp-duplicate requirement deleted — 2026-10-04

The owner directed deletion of this reporting requirement. Duplicate-ingestion
handling belongs to the pipeline. The 08A.1 chronology implementation no longer
groups equal timestamp strings, excludes their Runs, issues corruption guidance
or rejects explicit selection for that reason. Package selection, ordinary source-
time ordering and missing/unusable timestamp handling remain in the existing library.

The requirement is removed from the 08A.1/08B prompts, owning and receiving
handoffs, reporting ledger, README, current status and review metadata. It has
also been removed from cross-team reporting summaries so those references cannot
reintroduce it. The unverified list now has four groups. Removal is not recorded
as a passed check. `BANNED_IDEAS.md` records the ownership boundary. No fabricated
history, alternative duplicate rule or changes to pipeline ingestion/storage.

Verification: the existing genuine root-CLI selection/package and worked-window
format/history groups passed in 59.815 s using disposable storage under
`.codex-tmp/task08b/8dc7f9c73d8f4ba8b8a830b3f1ec4c00/`. These verify retained
reporting behavior, not the deleted requirement. Logging ownership, isolated
CLI/reporting imports and whitespace checks pass. No new acceptance test or
synthetic timestamp scenario was added.

The rebuilt review bundle has 81 explained cases, 19,361 checked links and four
remaining evidence-gap groups. All 17 named saved outcomes still agree with their
expected status/counts. Chrome verifies the removed item is absent and report →
outcome → result/return navigation works. Manifest and browser receipts are under
`.codex-tmp/task08b/pipeline-ownership/`. No production data/process/package change,
commit or push.

## Earlier failed queries and incomplete deliverables reconciled — 2026-10-04

Owner review correctly identified that the general status page did not make the
earlier list of problematic queries and incomplete deliverables easy to trace.
`outcomes.html` now explicitly reproduces the six review IDs (`08B-UX-01/02`,
`08B-QUERY-01`, `08B-QA-01`, `08B-EVID-01`, `08B-CLOSE-01`) with current dispositions.
The evidence item remains partly verified; documentation is not owner acceptance.

A separate named-case table covers 17 failed/empty-query examples. Each row shows
the question, expected behavior, actual saved CLI result/exit, work status and a
direct report link. It explicitly corrects the old rejection expectations for
opposing filters and the misleading `required-partial` filename. Expected selection
or input-validation errors are distinguished from unfinished acceptance work.
The four still-unverified groups remain visible with evidence needed to finish
them: the simultaneous eleven-Run window; naturally
failed reads/requests; unavailable roots/decoding/ripgrep failures; and unavailable
original logs/model packages. None has been relabelled as passing.

Every investigation's opening explanation now links directly to the named-case
table and remaining checks. The original saved CLI payloads are reused unchanged;
this is a reconciliation/navigation correction, not new execution of failure cases.
The bundle builder checks all 17 listed outcomes against saved status/exit/counts
and the symbol request's input-validation stage before publishing the page.
Maintained metadata: `examples/reporting/delivery-status.json`. Browser checks
cover the current report → query table → missing-selector result → status return.

Executed reconciliation checks: 81 reading copies, 19,361 local links, all six
review IDs and all 17 saved outcomes passed builder validation. Focused Chrome
navigation/status/narrow-layout checks passed; six screenshots and the receipt
are under `.codex-tmp/task08b/earlier-outcomes/browser/`. The named-case and original-
assessment screenshots were visually inspected. Logging ownership and presentation
import checks pass. No new database acceptance check was claimed or required for
this reading/navigation change.

## Owner direction: file status, columns and load-order source — 2026-10-04

The owner's latest direction supersedes the earlier blanket statement that a
winning file/source cannot be identified. For analytics on a single file/line,
the last matching playset member in load order is the **Error source**. Reports
keep all matching files visible and use the actual numeric load order without
the “recorded load order” prefix.

Resolution tables now say **Resolved** when one or more paths are found and
**File not found** when a completed lookup finds none. Their count is separate.
Matching-file tables have **Load order**, **Mod name**, **File path**, **Line** and
**Error source** columns; the source row says Yes. The redundant “Evidence / Current
file candidate” column is removed. The integrated explanation, detailed diagnostic,
file rankings, source-scope tables and verbose appendix use separate columns.
Base-game/DLC files have no mod name; explicit roots have no fabricated load order.

The source owner implements the rule as public `file_line_sources(candidates)`
and returns its identity-keyed groups from `SourceSearch.resolve`. Analysis forwards
those groups into selected, historical/per-Run and partial entries. Each group
contains relative path, line, candidate IDs, rule `last_load_order`, the chosen
`error_source` file/member object, and a reason if no line/comparable unique order
is available. It uses the effective source scope and is computed before any
file-content condition, so a content filter cannot promote an earlier copy.
JSON, text and HTML carry the same assignment. Stored classification, identities,
counts, history and the original candidate list/order are unchanged.

Executed genuine verification:

- Three CLI groups passed in 63.465 s under
  `.codex-tmp/task08b/bf417ac7f10840d7be776e15f11a15aa/`: worked-window formats,
  counts/limits/history and verbose links/line contents; resolved-path/content
  filtering; and relative paths across the full playset. Eighteen root-CLI exports
  use a disposable backup through `HandlerClient`.
- The genuine two-file example retains two diagnostics / 64 occurrences and both
  matching mods (114/115), assigning **EB+EC724 Compatibility Patch, load order 115**
  for both file/line groups. JSON asserts the same member/path. When a separate
  source-content predicate excludes all displayed files, the same source remains
  available and is shown separately; source selection uses pre-content matches.
- Focused Chrome checks pass for the new columns/raw numbers/Yes marker, the
  genuine “File not found” reading copy, content-independent attribution, offline
  navigation, return links and narrow layouts. Ten screenshots and the receipt
  are under `.codex-tmp/task08b/source-labels/browser/`; the main file-table
  screenshot was visually inspected. The missing-file case reuses retained
  genuine analytical output; it is not a new ingestion or query acceptance run.
- Logging ownership and isolated CLI/reporting imports pass. No executed check
  failed. The authorized fixture runner's label assertion was updated, without
  rerunning ingestion for this presentation correction.

The review bundle is regenerated from `source-labels/manifest/`. Reading copies
preserve their original analytical payloads. For prior exports without the new
field, the renderer can apply the same public rule to saved resolved associations;
it does not infer an assignment from a known content-filtered subset. Original
exports remain untouched. The updated relative-path example explains the rule
and shows the result on the same page.

Changed files: source search/public exports, analysis forwarding, shared report
presentation/explanation, genuine CLI checks, browser/fixture helpers, example
descriptions/status, README, owning handoffs and the current reporting ledger.
No new dependency, schema, production state, active-package, commit or push change.
Existing unrepresented-evidence gaps and live Trusted Run acceptance remain separate.

## Owner clarification: one relative path across the playset — 2026-10-04

The usual source-file filter is a game-relative path, shared by the base game
and mods' folder structures. Use `scope.source.relative_path.exact`; for example:

```json
{"scope":{"source":{"relative_path":{"exact":["/common/scripted_effects/some_file.txt"]}}}}
```

The optional leading `/` means the same relative location as `common/...` in
this explicit relative field. Both slash styles are supported. Stored references
determine diagnostic membership; a current disk file is optional context. By
default, lookup checks the location beneath every member of the Run's recorded
playset, retains all matching mod candidates, and inventories only the named
parent folder without recursion. A basename elsewhere is not a relative-path hit.

`source_query.normalize_source` normalizes copies of `relative_path.exact` and
`directories` for standalone search, optional context and diagnostic source scope.
Stored paths/identities and caller queries are unchanged. Physical `roots`/`files`,
UNC paths and literal text conditions keep their previous meanings. Standalone
`effective_selection` shows the normalized scope; diagnostic `effective_query`
retains the request spelling and its explanation states the interpretation.

The reusable [query example](../examples/reporting/relative-path.json) and README
document the command. `relative-path-all-members` integrates the plain-English
question, expected result, actual result and candidates on one report page.
Three accompanying cases show equivalent separator/leading-slash spellings and
a different-folder empty result. No unrelated template or message restriction is
applied. The query omits history to focus this check on the selected Run.

Executed verification with disposable backups and the public handler:

- `test_10_relative_path_across_playset`: passed in 36.236 s. Six actual root-CLI
  exports under `.codex-tmp/task08b/863281ad728c44d0bcc4b60d1837e055/`, including
  JSON, verbose text and verbose HTML. Genuine Run `20261003-74G2EB` returns two
  identities / 64 occurrences. All 133 recorded members remain in scope; all
  constructed inventories are `common/on_action`, nonrecursive. Lookup examines
  433 unique physical file names in 77 existing parent folders and finds two files:
  Early Bookmarks and the Legendary Super Compatch (recorded order 114), and
  EB+EC724 Compatibility Patch (115). These are current measured counts.
- Equivalent leading-slash/no-slash/backslash requests return identical records
  and candidates. The same basename under `common/scripted_effects` returns zero
  stored matches and performs no source lookup. SQL-only investigation returns the
  same totals without searching files. Standalone search, repeated cache reuse,
  relative directory scope and an explicit physical-file regression also pass.
- Existing genuine source composition/basename check: passed in 24.715 s under
  `.codex-tmp/task08a2/63c7fd2a33f04a748db4c26abdffdd72/`.
- The 07E logging ownership check, CLI/reporting imports and scoped whitespace
  checks pass. No executed check failed in this clarification.

The regenerated review bundle has 81 explained cases and 16,911 checked links,
using `.codex-tmp/task08b/relative-path/manifest/`. Chrome passed the two new
relative-path routes, integrated evidence/mod-name checks, status/return links and
narrow-layout checks. Nine screenshots and the browser receipt are retained under
`relative-path/browser/`; the main relative-path explanation/candidate screenshot
was visually inspected. Reading-copy generation preserves analytical payloads.

Changed implementation: source query/search, report explanation, focused genuine
CLI verification, query/check examples, review-bundle/browser helpers and the
current documentation/ledger. No dependency, schema, production state, active
package, commit or push changes. Earlier unrepresented evidence cases and the
separate live Trusted Run milestone remain as documented below.

## Owner correction: no path is normal emission content — 2026-10-04

The owner clarified that a pathless emission is complete by design. Reports now
say **“Source lookup: not applicable. This emission supplies no file path.”**
This is ordinary descriptive text, without warning styling or an incomplete-
evidence claim. In mixed reports, actual source lookup problems are attached only
to diagnostics that carry references. No-path emissions remain queryable through
`refinement.has_source_reference: false`; path/source filters exclude them normally.

The owning source library returns `source_references.status` (`present`/`no_path`)
and resolver `reference_status`. Analysis exports `source_path_status` on ordinary,
historical/per-Run and partial entries (`not_evaluated` when no resolver was used).
Misleading `limitation`, `reference_limitations` and `reference_complete` fields
are replaced by neutral presence status and `records_without_source_path` counts.
If no selected references need lookup, the source resolver skips playset/root
access, returns complete coverage and zero filesystem counts. This avoids a false
source-coverage problem even when a pathless archive has no recorded playset.

Also corrected the explanation helper: an empty source-filter object no longer
invents a “match recorded paths” condition in otherwise unfiltered reports.
Stored data, diagnostic identities, counts and classification are unchanged.

Executed genuine verification:

- Root-CLI no-path/mixed/member/file exclusions: passed in 37.467 s under
  `.codex-tmp/task08b/67c02b2d85324789bb0c21cffb682f65/`. The no-path localisation
  diagnostic retains 163 occurrences and shows not-applicable source context in
  JSON/text/HTML. No path condition is invented in its explanation. An earlier
  pass under `a7d6ec84194347d1b72807e13bc958d4` preceded that explanation fix.
- Genuine source-library exclusion regression: passed in 6.753 s under
  `.codex-tmp/task08a2/bd1537163eb7460286f92e4d7387af4c/`.
- Genuine archived Run `20261003-352QKU`, with no retained playset: five root-CLI
  exports passed under `.codex-tmp/task08b/no-path/archive/`. Its no-path emission
  remains complete with one occurrence, zero lookup work and no playset warning
  in all three formats. The mixed report keeps both diagnostics and attaches the
  real lookup problem only to the record with a file reference. Helper:
  `.codex-tmp/task08b/check_no_path_archive.py`; receipt: `verification.json`.
- The 07E runtime logging ownership check and whitespace checks pass.

The new examples integrate the explanation with the report: `pathless-emission`,
`pathless-archive` and `mixed-archive-source-context`. Prior original exports are
retained; their obsolete fields are not treated as the current public contract.
No production/process/package/schema change, commit or push. Actual required-
lookup failures and the previous verification gaps retain their separate meanings.

The regenerated bundle has 77 explained cases and 16,786 checked links, using
`.codex-tmp/task08b/no-path/manifest/`. Chrome passed all three new example routes,
status/return links and narrow-layout checks; ten screenshots are under
`no-path/browser/`. The no-path and mixed-report screenshots were visually
inspected. Original analytical payloads remain unchanged by the reading-copy
builder. No executed check failed in this correction.

## Owner addition: independently verify recursion and return search counts — 2026-10-04

Source search now exports per-search `coverage.search_counts` and per-root
`search_scopes`. Counts distinguish names/paths examined, folders enumerated,
candidate files, files selected for content checks and matching files. Folder
counts include starting directories and empty folders. Global physical-path
counts deduplicate overlapping/repeated roots while candidate associations remain
intact. Cached inventories retain the same scoped counts, and the report labels
cache use. SQL-only queries report zero filesystem work. Counts are observations;
incomplete coverage does not become complete merely because counts are available.

Exact-file lookups retain the delivered parent-directory optimization. The report
shows those actual directories, rather than claiming to search the whole root.
Text/HTML show the counts in the explanation/summary and a visible Source coverage
table, with expandable root/member/scope/cache detail. JSON exposes the same data.

Executed `tools/check_source_recursion.py` using genuine retained Run
`20261003-74G2EB`, a fresh disposable backup, HandlerClient and current sources.
Independent PowerShell `Get-ChildItem -LiteralPath -Force -Recurse` measured file
sets/folders; cold and cached SourceSearch results were compared with those sets
and counts. All **29 comparisons passed**:

| Scope | Files (independent = search) | Folders (independent = search) |
|---|---:|---:|
| Base-game root, recursive | 48,472 | 3,736 |
| Base-game root, recursion off | 30 | 1 |
| Base-game `common`, recursive | 2,677 | 212 |
| Base-game `common`, recursion off | 1 | 1 |
| Early Bookmarks and the Legendary Super Compatch, recursive | 17,875 | 385 |
| Same mod root, recursion off | 6 | 1 |
| Same mod `common`, recursive | 1,634 | 141 |
| Same mod `common`, recursion off | 0 | 1 |
| Root CLI: referenced file's `common/on_action` parent in that mod | 130 | 1 |

Also checked overlapping directory scopes, exact-file parent narrowing,
filename-only recursion, whole-root-cache subsets, exact-cache reuse and repeated
root associations. The root CLI exported JSON/text/HTML: two exact diagnostics /
64 occurrences, one candidate file after examining 130 names in one folder. The
stored-only library query returns the same identities with zero filesystem work.
The existing genuine path/basename regression passed in 17.313 s under
`.codex-tmp/task08a2/10100c33b9074cee8f9afbd14f170c7f/`. The 07E logging ownership
check passed. No recursion defect was found in these real trees; the change adds
counts and cache-aware folder inventories.

Passing evidence: `.codex-tmp/task08b/recursion/769ceb6ed0434981b2744aab42faff3e/`.
`recursion-verification.html` contains the question, expected behavior and all
comparisons together; `verification.json`, original independent file lists and
`commands.json` retain exact evidence. The ordinary `recursion-scoped-report`
example links this measurement. Reproduce with:

```powershell
.\.venv\Scripts\python.exe -I -B tools/check_source_recursion.py --source-database .codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/unchanged.sqlite3 --run-id 20261003-74G2EB --output-root .codex-tmp/task08b/recursion
```

The first verification attempt reached text-format checking, then failed because
the checker used `read_text`, normalizing CRLF before comparison with the stored
message. Raw exported bytes preserved the message correctly. The checker now
decodes bytes without newline conversion; the complete fresh rerun passed.
The failed attempt and explanation remain under
`recursion/20783f5f1fff4b26aecbfb01c108ca3f/`; it is not presented as passing evidence.

The genuine content-group/negative/no-match regression also passed (2.652 s),
`.codex-tmp/task08a2/e71abed019d94530bbe2b53cece441b4/`. Imports, verification-tool
help and whitespace checks pass. The refreshed bundle has 74 explained cases and
16,715 checked local links; analytical payloads remain unchanged. Its current
manifest is `.codex-tmp/task08b/recursion/manifest/`. Chrome passed the new report,
counts link, independent-measurement attachment and return navigation, with ten
screenshots under `recursion/browser/`. The counts and independent-comparison
screenshots were visually inspected. The new source counts appear only in newly
executed reports; earlier retained exports are not assigned invented measurements.

Runtime changes are confined to source-search metrics/folder inventories and
report presentation/explanation. The new verification tool uses genuine sources
and a disposable handler database; no source files, production data, package
selection or live processes changed. Reparse-point traversal, unavailable roots
and the previously listed evidence gaps remain unverified. Counts are measurements,
not acceptance thresholds. Commits/pushes and full live Trusted Run remain separate.

## Owner addition: explicitly seek unresolved recorded paths — 2026-10-04

The owner's latest request is implemented in the shared source/query services:

```json
{
  "scope": {"source": {"resolution": "unresolved"}},
  "analytics": {"history": false},
  "display": {"limit": 20}
}
```

Use `examples/reporting/unresolved-paths.json` with ordinary `report --preset
frequent --query ...` (or a compatible preset/custom investigation). `resolved`
is also supported. This is distinct from ordinary path selection: a `files`
predicate still returns recorded matches whether or not the file exists today.
`refinement.has_source_reference: false` separately selects no-path messages.

An unresolved match has at least one selected stored path with no current file
after a completed search within the effective roots. Root/member selections
choose where that resolution is tested; path/directory selections restrict the
references. With multiple references, one requested status suffices, and all
reference statuses remain visible. A separate content condition still requires
a current referenced file containing the requested text. File existence itself
is determined before content filtering, so nonmatching text cannot make an
existing file appear unresolved.

08A.2 returns per-reference `reference_resolution`; 08A.1 forwards it to ordinary,
historical, per-Run and known-match partial entries. Text/JSON/HTML expose the
same status: resolved, unresolved, unknown/incomplete, not searched, or outside
the required path scope. No-path records are ordinary nonmatches. The timestamp
is the existing report generation time. This current observation is not persisted
as a historical Run fact. Source roots may omit other valid locations: launcher-
relative `mod/` references, for example, are not proof of a globally missing file
when only recorded playset content roots were searched. No storage schema,
dependency, source-parser, active package or production change.

Executed verification for this addition:

- Genuine root-CLI resolution group: passed in 20.440 s, seven exports under
  `.codex-tmp/task08b/ffac74bcfbce42c383db2257bcc20c96/`. A known resolved path
  returns the culture diagnostic (32 occurrences) and both mod candidates at
  recorded orders 114/115. The unresolved query excludes that diagnostic and
  the pathless localisation diagnostic. Nonmatching optional content leaves
  the existing path resolved. Text/HTML show the resolution and original values.
- Broad genuine Run `20261003-74G2EB`: 60 identities / 386 occurrences, first 20
  displayed, checked independently from handler records and filesystem existence
  across 561 unique stored paths. JSON/text/HTML exported. Receipt and helper:
  `.codex-tmp/task08b/path-resolution/genuine/genuine-verification.json` and
  `.codex-tmp/task08b/check_path_resolution.py`.
- Authorized two-emission fixture: 14 checks / 30 root-CLI exports passed under
  `.codex-tmp/task08b/path-resolution/6270bcb83f8c4d65a9cd5bff59df7a39/`, Run
  `20261003-D1021Z`. Both fake paths match unresolved; neither matches resolved.
  Directory selection returns one, member-scoped absence returns two, and a
  required content condition returns zero. All earlier path/context checks pass.
  Original captures' hashes/mtimes and all 133 playset members are unchanged.
- Genuine archive without a retained playset: explicit resolution remains unknown
  (`source_filter_incomplete`, exit 3, no false missing-file matches) in all three
  formats. The same ordinary recorded-path query still returns four diagnostics.
  Five archive exports and its receipt are under `path-resolution/genuine/`.
- Genuine SQL-only path/basename/composition regression: passed, 25.710 s,
  `.codex-tmp/task08a2/1c8f0b8c041e4998aa30a48ed62aea97/`. No disk inventories
  for stored-only predicates. Genuine worked-window format/history/limit/link
  regression: passed, 76.252 s, `.codex-tmp/task08b/4b83c47b0e51422eb628fc3424d3dbfa/`.
- The 07E runtime logging ownership check and venv `pip check` passed.

Rebuild the existing reading bundle with `tools/build_reporting_examples.py
--evidence-dir .codex-tmp/task08b/path-resolution/manifest --output-dir
.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f`. The index starts with
`unresolved-genuine-paths` and `synthetic-unresolved-paths`, each integrating the
plain-English question, expected outcome, actual result and per-path evidence.
`outcomes.html` links the new checks and retains the four other evidence-gap
groups. This addition does not establish unavailable-root/decoding/ripgrep failures,
unavailable comparison reads or the full eleven-Run window.

The refreshed bundle passes 16,681 local-link checks across 73 explained cases,
with analytical payloads unchanged by the reading-copy builder. Chrome 154 passed
seven resolution/archive routes, delivery-status/return and fixture-input links,
plus narrow-layout checks. Fourteen final screenshots and the passing receipt are
under `path-resolution/browser-final/`; the synthetic unresolved and unknown-
archive pages were visually inspected, as were the genuine/resolved pages in the
first browser pass. The duplicate stored-path table was removed where the new
resolution table already presents that path. Isolated imports and `git diff
--check` also passed; existing CRLF-normalization notices concern working copies,
not failed checks. No new acceptance check failed in this addition.

Changed code: shared `source_query.py`, `query.py`, `source_search.py`, `analysis.py`;
report `explanation.py`/`presentation.py`; genuine CLI test, fixture/browser/example
tools; new query and check/status definitions; README and current plan/status/
handoff/reporting ledger plus both owning-library handoffs. Commits/pushes remain
deferred and full live Trusted Run acceptance remains separate.

## Owner correction: path queries return matching diagnostics — 2026-10-04

The owner rejected the earlier interpretation that missing/pathless records should
make a path filter fail. That behavior is corrected in the owning source library:
path-only predicates select recorded references. Nonmatching or unusable/missing
references are ordinary exclusions. A matching recorded path remains eligible
even when the current file is absent. No excluded record is surfaced as a warning
or `unidentified_records` partial. The earlier required-file and pathless-error
claims below are historical and superseded by this correction.

`scope.source.files`, `referenced_paths`, filename/relative-path predicates,
directory/recursion restrictions, extensions and globs compose over recorded paths.
Library path-only selection remains SQL-only by default; reports request optional
candidate context. Absolute/relative correspondence can use stored root metadata
without disk access. A mod/root or file-content predicate additionally requires a
current candidate. Missing individual files are still nonmatches; actual failures
reading required source evidence retain the existing incomplete-result contract.
An empty reference set does not trigger an unnecessary source search.

Ordinary query: `examples/reporting/file-path.json`. The new `file-path-all` report
asks for every diagnostic referencing `common/on_action/sea_minority_on_actions.txt`
in Run `20261003-74G2EB`, without message/template/identity restrictions. It returns
two exact diagnostics / 64 occurrences, independently checked against all stored
records through the public handler. Text, JSON and HTML agree. The historically
named `required-partial` example now returns the one matching culture diagnostic
(32 occurrences), excluding the pathless localisation record without a warning.

Checks executed for this correction:

- Genuine root-CLI member/file/exact/optional-context and exclusion groups:
  two passed, 70.665 s, `.codex-tmp/task08b/b64da3cd909542c2a1f6880e7eb071ce/`.
- Genuine source-library content grouping, composed member/file/excerpts,
  pathless exclusion and stored-reference/basename groups: four passed, 33.856 s,
  `.codex-tmp/task08a2/557bfaf0d8da47d0af3328353385e67f/`. The added combined
  recorded-path/glob/directory/extension/exclusion check passed in 17.691 s under
  `.codex-tmp/task08a2/886cb5d712cf4cb19e7d5d70b5437cf2/`.
- Authorized two-emission fixture: nine checks / nineteen actual CLI exports,
  `.codex-tmp/task08b/path-filter-correction/b58bf687410a4c44a2e81e6fc6af50e3/`.
  Exact/relative/absolute/directory filters match the recorded fake paths;
  unmentioned paths and missing current mod candidates return successful empty
  results. Original inputs and all 133 playset members are preserved.
- Genuine archive: seven CLI exports under `path-filter-correction/archive/`.
  A recorded-path query returns four matching diagnostics without a retained
  playset; an unmentioned path returns zero without looking up the playset.
  Required member evidence still correctly fails when that playset is unavailable.
- Broad genuine file query: three CLI formats under
  `path-filter-correction/all-path/`, with a raw-handler identity/count comparison.
- Shared logging ownership and isolated CLI/reporting imports pass.

The refreshed bundle has 63 explained investigations and 16,404 checked local
links; analytical payloads remain unchanged by the reading-copy builder. Chrome
154 passed eleven corrected report routes, status/return and fixture-input links,
with 18 screenshots under `path-filter-correction/browser/`. The broad path,
corrected mod-filter and empty-path screenshots were visually inspected. The
browser helper exited normally. A further genuine CLI check in
`path-filter-correction/optional-context/` verifies that selecting an outside root
for optional context cannot alter absolute recorded-path membership (two records /
64 occurrences, no disk candidates in that optional root).

Current evidence manifest: `.codex-tmp/task08b/path-filter-correction/manifest/`.
Rebuild with `tools/build_reporting_examples.py --evidence-dir` pointing there,
the existing bundle as `--output-dir`, and `--featured-commands` pointing to
`path-filter-correction/all-path/commands.json`. The example descriptions and
`outcomes.html` replace the previous required-file/pathless-failure interpretation.
No query/source schema, dependency, stored diagnostic or production state changed;
commits/pushes remain deferred. Four unrelated evidence-gap groups remain as listed
on the outcome page. No new acceptance case failed in this correction.

## Earlier verification follow-up and owner-authorized fixture — 2026-10-04

The owner asked for execution against the open evidence items, then explicitly
authorized a two-emission fixture whose only changes are nonexistent file LOCATOR
paths, with the same recorded playset. This supersedes the earlier blanket
synthetic-data prohibition for that fixture only. Genuine history remains separate.

The fresh unchanged production backup at
`.codex-tmp/task08b/gap-followup/3445c87f813243dc904ceccbcd08eee3/` has 21 Runs:
seven eligible and fourteen missing-timestamp exclusions. Public-handler reads of
all stored diagnostics/playsets/review metadata succeeded; all 133 members of each
eligible Run are currently accessible.
The backup SHA-256 remained unchanged after all checks.

Actual root-CLI reports under its `windows/` directory now verify a complete
trailing-five investigation (4,041 occurrences / 110 distinct identities), five
predecessors and five successors in separate default-window checks, and a middle
Run with three neighbors on each side. Counts, exact identity maps, fractions and
newness were compared with raw public-handler records. The worked report's
text/JSON/HTML all rendered the matching diagnostics and Run IDs. A simultaneous
five-before/five-after window still needs eleven eligible Runs.

`tools/check_reporting_locator_fixture.py` builds the owner-authorized fixture
through the normal capture/playset writer and HandlerClient ingestion. Only two
file-valued LOCATORs differ from their original full emissions; headers, reasons,
keys, lines and other values remain byte-identical. The fixture playset preserves
all 133 members and recorded orders, with correct synthetic-error and genuine-debug
hashes. Original retained files/hashes/mtimes were checked unchanged.

Historical fixture evidence (the explicit-file expectation below was rejected):
`.codex-tmp/task08b/locator-fixture/d9ca56e9b0ad4475ac8bd4562f4a3a23/`.
Eleven root-CLI exports originally exercised five checks, but their expectation
that an explicit file filter should fail when the file was absent was wrong.
Those historical results do not establish the current path-filter contract.
The corrected fixture returns both records when their stored fake LOCATOR paths
match the requested paths, and zero when no stored path matches. Disk existence
does not affect that selection. Current passing receipts are in the opening
sections above. The old exports remain retained as historical evidence.

The original test first expected zero solely because the files did not exist,
then was changed to expect an error. Neither expectation expressed the owner's
intended stored-path query. The later correction fixes the library and the checks.
The first inventory helper
also failed on a duplicate Python keyword before any record scan; its corrected
run produced the unchanged backup and inspection above. Both initial outputs are
retained. Historical closure/evidence counts below predate this follow-up.

### Genuine archive checks close syntax and missing-playset gaps

`tools/check_reporting_syntax_archives.py` receives five unchanged retained CK3
logs into separate disposable single-Run databases through normal capture and
handler ingestion. Seventeen actual root-CLI exports cover all nine researched
syntax selectors, 85 matching diagnostics, both stored statuses, and the precise
assignment-error body/slot/type/REASON condition. Each report's records, counts and
statuses agree with independently selected public-handler records. Original file
hashes and timestamps are unchanged. These fresh receipts do not extend the seven
production chronological Runs and establish no live lifecycle acceptance.

The archives have no retained playsets. All five optional-context reports succeed
in text, JSON and HTML and disclose that absence. Requiring a game-file association
returns `source_filter_incomplete`, exit 3, in JSON/HTML. No playset was removed.

Combined receipt: `.codex-tmp/task08b/syntax-archives/combined-verification.json`.
The first three cases and eleven exports are in `15a2e10406be4f079f00583729765bbd/`;
the remaining two cases and six exports are in `1587b339cf9b49b6a89ec83efbd63869/`.
The first attempt stopped with Windows access denied when renaming the next
temporary capture directory, before ingestion. A fresh disposable retry of those
two remaining cases passed. This preparation failure is disclosed, not counted as
acceptance evidence for a failed diagnostic read or request.

### Review and reproduction

The existing review bundle now has 54 explained investigations and 16,161 verified
local links, with analytical payloads unchanged. Its `outcomes.html` links the new
history, syntax, missing-playset and synthetic checks from their completed items.
The fixture report is `investigations/synthetic-missing-files.html`; it links the
two-entry error log, normal playset JSON, original emissions, precise modifications
and verification receipt. Its opening explanation shows complete/no-file evidence
beside both diagnostics. The new worked history is `worked-five-runs.html` in the
same directory; the earlier four-Run examples remain labelled as earlier evidence.

Chrome 154 passed fifteen new report routes, index/status/return navigation and
the fixture-input link, with 22 screenshots under
`.codex-tmp/task08b/browser-followup-final/`. The synthetic input and report,
archived equals-token report and remaining-gap page were visually inspected;
the five-Run report was also inspected in `browser-followup/`. The final genuine
CLI format/history/limit and partial-source regression groups passed (72.554 s),
with exports in `.codex-tmp/task08b/3c14e0bd42d54ce69ce5724603067335/`.
Logging ownership and isolated CLI/reporting imports passed. No dependency added.

The full browser walkthrough wrote its passing navigation receipt, then its
temporary Chrome/Node processes lingered during shutdown and were stopped by
their verified process IDs. The helper now bounds shutdown and closes only its
own child/pipes. A focused status-page run in `browser-shutdown-check/` passed and
exited normally (exit 0). This distinguishes passed report checks from the initial
verification-helper teardown defect.

Reproduce the new checks with the project venv (all outputs remain ignored):

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
& $python -I -B tools/check_reporting_locator_fixture.py --source-database .codex-tmp/task08b/gap-followup/3445c87f813243dc904ceccbcd08eee3/unchanged.sqlite3 --source-run 20261003-74G2EB --capture .ck3chronicle/wip/runtime/pending/20261003T050614.976714Z-_gldnNph --output-root .codex-tmp/task08b/locator-fixture
& $python -I -B tools/check_reporting_syntax_archives.py --inputs .codex-tmp/task08b/gap-followup/archive-inputs.json --output-root .codex-tmp/task08b/syntax-archives
```

The archive command supports repeatable `--case` selections for bounded retries.
The retained genuine-window helper is `.codex-tmp/task08b/verify_available_windows.py`;
its `windows/commands.json` records actual commands and `verification.json` records
independent comparisons. Rebuild the existing bundle using the earlier command
below plus `--featured-commands` for the new window, final fixture and both archive
`commands.json` files. Browser follow-up uses `tools/check_reporting_browser.mjs`
with `--followup-only` and an isolated output/profile directory.

Changed by this follow-up: the two verification tools, example builder/browser
check, report presentation, example descriptions/status/README, AGENTS.md's scoped
owner exception, README and current plan/status/handoff/reporting ledger, plus
08A.2's receiving evidence note. Library query/source semantics remain unchanged.
Four evidence-gap groups remain: simultaneous eleven-Run comparison,
naturally failed database reads/requests, unavailable roots
or decoder/ripgrep failures, and reporting with unavailable raw logs/model packages.
The two-entry fixture tests missing referenced files within readable roots.
Full live Trusted Run acceptance, production operations, commits and pushes remain
separate. No further product requirements are proposed by these checks.

## Earlier reporting delivery and explanation correction (2026-10-04)

The owner's latest review identified a remaining usability defect: opening an
outcome skipped its explanation, and readers still had to find the evidence in
the long report. Earlier closure statements did not establish a satisfactory
reading experience. The correction puts the question, expected behavior, actual
result and supporting evidence in one opening section, in ordinary CLI reports
as well as the generated example bundle. This records implementation and checks,
not owner acceptance or completion of the separate live Trusted Run milestone.
Production data/processes/configuration and active package selection are unchanged.
Commits and pushes remain deferred.

### Earlier incomplete items are now visible in the review bundle

The template report alone does not establish completion of the other deliverables.
`outcomes.html` beside `examples.html` now maps the earlier incomplete items to
their completed corrections and example reports. It separately lists six remaining
genuine-evidence gaps and what is needed to finish each check. Every investigation
reading copy links to this page. The maintained description is
`examples/reporting/delivery-status.json`; it is review metadata, not analytical
data or a claim that unavailable cases passed. The gaps listed at the end of this
handoff remain open. This reconciliation adds no database queries or new acceptance
evidence for those cases.

Rebuild verification passed for 38 examples and 12,136 local links, with analytical
payloads unchanged. A focused Chrome check clicked index → delivery status →
empty-result example → delivery status, checked every listed disposition and
completion condition, and checked narrow layout. Desktop completed/gap screenshots
were inspected. Evidence: `.codex-tmp/task08b/browser-delivery-status/`.
The shared runtime-logging ownership check also passed. These are presentation
checks, not new executions of the unverified cases.

### Integrated explanation correction

All 38 investigation links now land on `#explanation`. Its evidence includes the
stored template pattern where relevant, per-Run totals, diagnostic examples and
all candidates for those examples. The partial-source explanation includes both
the known match and the pathless diagnostic. Empty/error responses explain their
outcome in place. Examples are explicitly labelled; complete analytical totals
and bounded detailed lists remain unchanged. Long command/filter details are
expandable instead of separating the question from its answer.

Named links lead directly to the relevant template, diagnostic or Run window.
Verbose file links within the explanation open the exact numbered source excerpt
with its target line highlighted. Each diagnostic/template has a return link to
the explanation; the report also returns to its investigation-list entry.

Actual checks for this correction: genuine root-CLI format/history/limit/source
link group passed in 43.581 seconds (`2121691b550f41d0a5ce845a828e411f/`), and
partial-source group passed in 12.715 seconds (`31ab71bbcb184a77aaae3f30627f7edc/`),
both under `.codex-tmp/task08b/`. Shared runtime-logging ownership passed.
The rebuilt 38-example bundle passed 12,077 local-link checks and analytical
payload invariants. Chrome checks exercise 13 integrated explanation routes,
six direct evidence links, an excerpt link from the explanation and its return,
plus desktop/narrow layouts. Evidence and inspected screenshots are under
`.codex-tmp/task08b/browser-integrated/`. This uses existing genuine CLI exports
for the example rebuild; it does not claim a fresh query for every example.

### Closure of the review items

| Item | Outcome and evidence |
|---|---|
| 08B-UX-01: investigation → explanation and evidence → return | Corrected after further owner review. All 38 examples now open the explanation with its evidence inline; 12,077 local links checked. Actual Chrome clicks cover 13 representative reports and direct evidence/excerpt links. |
| 08B-UX-02: templates, Run counts and mod/file meaning | Closed. Templates show placeholder patterns and combined Run counts before separate diagnostics. Diagnostic Run counts and mod/path pairs are visible. Plain-English question, filters, expected and actual outcome appear together. Browser screenshots were inspected, including the original D2 concern. |
| 08B-QUERY-01: mutually exclusive preset filters | Closed. Owner feedback and the instruction to complete remaining work are applied: valid filters are ANDed and can return a successful empty set. Preset conditions remain visible and cannot be overwritten. Missing symbol input is rejected before any database request. |
| 08B-QA-01: browser inspection | Closed. Chrome 154 rendered the offline reports in an isolated disposable profile. Outcome/return clicks, source-excerpt navigation, marked lines, no remote assets, desktop layout and narrow-view overflow checks passed; representative PNGs were visually inspected. Earlier failed browser attempts are historical. |
| 08B-EVID-01: available genuine cases | Available-case work complete. A genuine DLC-path example now passes through the CLI and browser. Four-Run syntax output represents two of nine selectors; the seven absent selectors and genuine failure/full-window gaps remain explicitly unverified, as permitted by the assignment. They are not claimed as passing tests. |
| 08B-CLOSE-01: deliverable/evidence reconciliation | Closed by the matrix below, current README/status/handoff/ledger updates, and the recorded CLI/library/browser checks. |

### Current behavior and review outputs

The `new-contradiction`, `hotspots-contradiction`, `syntax-contradiction` and
`new-zero-count` examples now complete with zero matches and exit 0. The earlier
brief's rejection rule is superseded by the owner's empty-set feedback. Invalid
JSON/fields/types, missing required selectors, unsupported syntax packages and
incompatible execution controls remain errors. Disabling history while filtering
newness is an execution-control conflict, not an empty record predicate.

The owning query model now supports `refinement.all`: one additional list of
compound conditions ANDed with the ordinary refinement and scope. Presets append
their base condition without replacing the supplied filters. Each condition uses
the existing record/count/newness predicates and OR selectors. Effective query
exports retain both sides. Counts/history and source filtering stay in the owning
libraries; no empty-result fabrication or post-render filtering was introduced.

Stored source-reference presence means a file path recoverable from a path-valued
`<LOCATOR>` or literal stored text. A numeric line locator alone is insufficient.
The file need not exist today, so unresolved recorded paths still qualify for
hotspots. A required mod filter instead searches for current candidates under
the selected member's root from that Run's recorded playset; it establishes no
causal ownership.

`required-partial` now shows both kinds of evidence explicitly: the culture
failed-context-switch record at `common/on_action/sea_minority_on_actions.txt`
line 141 has a candidate in EB+EC724 Compatibility Patch (load order 115;
32 occurrences). The localisation message `Data error in loc string
'duke_male_holder_irish'` has only a PARAM and no path (163 occurrences). The
latter appears in a separate section and is named in the actual outcome. It is
not counted as a match or a proven nonmatch. The source library's incomplete
required-filter rule remains unchanged. JSON carries `unidentified_records` and
`unidentified_record_count`; text/HTML show the same information and respect
history being disabled.

`dlc-path` demonstrates a genuine six-occurrence diagnostic with two referenced
paths and three candidates: plain base-game/DLC paths, plus Unofficial Patch at
recorded order 28. `syntax-window` applies the nine selectors over all four
eligible Runs: two matching diagnostics/two occurrences in each Run. Only
`0b2804538785c71278ea37e7` and `d3e23fc8aad5883970f02964` are represented.

Current review entry point (generated evidence, outside Git):
`.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/examples.html`.
Reports and their explanation/outcome/return links are together under its
`investigations/` directory. Earlier raw CLI exports remain retained.

### Checks actually executed for closure

- Eight genuine root-CLI groups: passed, 161.987 seconds, outputs
  `.codex-tmp/task08b/1955129d312c4ae9bfa1f005c8f2b2a7/`.
- Six retained genuine query checks: passed, 13.926 seconds.
- Nine retained genuine source checks: passed, 260.071 seconds.
- Focused partial-source reruns verify the newly visible unidentified record,
  separate match totals and disabled-history presentation. Final focused pass:
  11.572 seconds, `.codex-tmp/task08b/5d008c39363b4211bcd550938f0be982/`. Outputs
  are linked from `.codex-tmp/task08b/closure-manifest/commands.json`.
- Additional actual CLI text/JSON/HTML: `dlc-path` and `syntax-window`, under
  `.codex-tmp/task08b/closure-extra/`, with commands and selector coverage recorded.
- Shared logging ownership, isolated imports, dependency consistency and Node
  verification-helper syntax checks passed. No runtime dependency was added.
- Chrome 154: 13 report routes plus excerpt/return navigation; 23 screenshots.
  `.codex-tmp/task08b/browser-closure/verified/` contains the retained first full
  walkthrough. The final refreshed walkthrough is in `browser-closure/final-review/`.
  Screenshots cover template pattern versus diagnostic, Run tables, mod and DLC
  paths, empty/error/partial outcomes, numbered highlighted excerpts and narrow
  layout; `visual-review.json` records the actual image inspection. Browser
  automation uses Node built-ins and DevTools pipes; it does not
  access the user's active browser/profile or require a local server.

No new acceptance check failed in this closure work. An initial early screenshot
was taken before fragment layout settled; the browser helper now waits for layout
before checking/capturing anchor positions. No product-navigation workaround was
needed. Earlier failed checks and restricted browser attempts remain documented
in the historical evidence below.

Rebuild the review bundle and check it with the installed browser:

```powershell
$bundle = '.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f'
.\.venv\Scripts\python.exe -I -B tools/build_reporting_examples.py --evidence-dir .codex-tmp/task08b/closure-manifest --output-dir $bundle --featured-commands "$bundle/template-example-commands.json" --featured-commands "$bundle/worked-full-json-command.json" --featured-commands .codex-tmp/task08b/closure-extra/commands.json
node tools/check_reporting_browser.mjs 'C:/Program Files/Google/Chrome/Application/chrome.exe' $bundle .codex-tmp/task08b/browser-closure/final-review
```

The bundle generator only adds reading/navigation metadata to saved CLI results;
its invariant check confirms that analytical fields remain unchanged.

### Earlier assigned-deliverable checklist (superseded)

| Deliverable | Implementation / actual evidence |
|---|---|
| Root runs/report; configured and explicit DB | Root registration; eligible pagination, named/latest package selection and the retained configured-disposable-DB check. CLI group 1 and command-help group 8. |
| Five presets and refinements | Shared validated queries; exact conditions documented below. CLI groups 4–6, syntax-window and browser routes. Opposing filters now yield empty sets. |
| Text, JSON, offline HTML | Shared analytical payload; CLI group 2 compares counts, identities, history and filters. Local CSS, escaped content and no browser network resources. |
| Template/message/typed/exact/mod/file selectors | CLI groups 3–4 and reusable example queries; exact record identity stays separate from template aggregates and candidate association. |
| Worked trailing-five investigation | Four available Runs disclosed; per-Run totals 392, 437, 0, 245; total 1,074 occurrences / 145 exact identities. Candidates and emitter/reference rankings remain separate. |
| History, newness, absences and display limits | Counts/fractions and included-window newness; CLI groups 2 and 6. Four available Runs, actual sizes, 14 timestamp exclusions; historical absences separate. |
| Source candidates and effective scope | All candidates in library order, recorded mod names/numbers, explicit roots, directories and coverage; CLI group 3, nine source tests and inspected mod/DLC output. |
| Verbose source appendix | Current excerpts ±10 lines, clipping and target emphasis; CLI group 2/source tests plus real browser reference and return clicks. |
| Empty, invalid, unavailable and partial states | Successful empty reports, pre-submission input validation, selection errors and genuine pathless-source partials; CLI groups 1, 4, 5, 7. Naturally failed reads remain unverified. |
| Documentation, packaging, logging, boundaries | README, this handoff, both owning-library handoffs, current status/plan/handoff and reporting ledger; packaged template/CSS verification retained; 07E check rerun. Disposable data only; no commits/pushes. |

The remaining evidence limitations below are preserved. No synthetic histories,
modified timestamps, removed roots, mock clients or injected failures were used
for acceptance. Full live Trusted Run remains a separate milestone.

## Earlier implementation and review evidence

Owner reading-experience correction: every report now starts with a plain-English
question, actual filter explanation, expected behavior, actual result and reading
guide. `reporting/explanation.py` derives this presentation data from the effective
query/result; it is returned as `explanation` in root-CLI JSON and rendered in
text/HTML, including empty/error results and `runs`. It does not assert that a test
passed. `examples/reporting/checks.json` supplies each consumer example's specific
question/expected outcome; the adjacent README explains which examples deliberately
repeat an analysis to verify formats or display limits.

Diagnostic headings no longer carry the confusing `matched template` phrase.
They explicitly identify a specific diagnostic; recognition status and template
ID remain under an explanatory classification section. A visible file table
pairs every current mod candidate path with its recorded name/load-order number.
Names come from 08A.2's existing candidate member metadata for the evidence Run,
not today's active playset or a guessed file owner. Repeated candidate associations
remain separate and in library order. `ROOT_GAME` members (base game/DLCs) use
plain paths. Stored message text is unchanged. File rankings, candidate details
and appendix links also carry the applicable mod name.

Actual verification: all eight genuine CLI groups passed in 276.954 seconds,
including explanations in every test export and visible, uncollapsed mod/path
pairs in representative HTML. Template-only exports were regenerated via the
actual root CLI; all displayed candidate names were compared with public
`read_playset` results, while counts/history and format agreement stayed intact.
That template dataset includes 14 base-game candidate files and no DLC candidate
files: the DLC prefix rule follows stored `ROOT_GAME` metadata by source inspection,
not a new genuine DLC-file check. Logging ownership, imports and dependency checks
passed. No new failed checks or production changes in this correction.

Latest consumer evidence is `.codex-tmp/task08b/cc41d9c32c7843d0bb98f857ee5f88ea/`;
the open `c9e83ce2125a45c78c8db4b4ab70d18f/template-only.html` and worked reports
were refreshed. `examples.html` in the latter folder indexes explained HTML
reading copies under the latest evidence folder's `explained/`. Those copies add
the check-specific explanation to saved root-CLI results; original CLI exports,
commands and analytical payloads remain unchanged. They are supplementary readable
views, not an additional CLI execution or a browser visual-inspection claim.
The generated guide covers 33 individual checks plus the two complete starting
examples; 3,550 links in the generated reading copies/index were checked. The
copy verification confirms analytical payloads are unchanged. See
`c9e83ce2125a45c78c8db4b4ab70d18f/example-guide-verification.json`.

Owner template/instance correction: template investigations now show the stored
placeholder pattern and combined selected/window/per-Run counts before individual
diagnostics. Headings explicitly say `Diagnostic D1` etc.; stored `template` status
is labelled `Match status: matched template`. For the genuine example, the template
has 396 selected occurrences / 202 diagnostics; D1 is one specific opinion/null-target
diagnostic with 48 selected occurrences. The summary uses new complete
`rollups.templates` data in the owning analysis library, grouped by full definition
reference before display limits and reused in JSON/text/HTML. All exact identities
remain separate. The same `template-only` exports were regenerated through the root
CLI and their pattern/count tables checked against raw genuine public-handler reads.
The focused template/refinement consumer group passed (14.960 seconds), including
zero-display-limit invariance; logging ownership and imports passed. An initial
test invocation could not import `tests` under isolated Python and executed no
checks; explicit unittest discovery corrected the invocation. Browser visual
inspection remains unverified as disclosed below.

Owner example correction: `examples/reporting/symbol-template.json` now filters
only by template ID. The earlier culture/context-switch restrictions reduced the
selected result to one identity and made it a misleading template-selection
example. Actual root-CLI JSON/text/HTML exports now show all 202 selected identities
/ 396 occurrences, 61 separate historical identities, and all per-Run contributors
within display limits 250/100. The four-Run window has 263 identities / 1,415
occurrences. Corrected exports are `template-only.{html,json,txt}` in the same
ignored `c9e83ce2125a45c78c8db4b4ab70d18f/` evidence directory; the worked
context-switch investigation remains a separate query/report. Commands, comparison
and verification are retained as `template-example-*.json`. Identities, counts,
history and visible HTML tables agree with public-handler analysis. The first
checking script used an XML parser, which rejected genuine CK3 U+0015 characters;
checking the unchanged export with HTMLParser passed while preserving stored text.
No product behavior changed for this correction.

Owner usability follow-up: per-diagnostic Run counts were hidden in a collapsed
history section. They now appear directly below each message in a visible
**Occurrences by Run** table, with observed/absent/unavailable labels and the
selected Run identified. Only the explanatory fractions/notes remain collapsed.
The existing `c9e83ce2125a45c78c8db4b4ab70d18f/worked-full.html` was regenerated
through the root CLI against its unchanged disposable database. Generated HTML
checks confirmed the history tables are outside the diagnostic's collapsed
sections and the displayed counts agree with the retained genuine result.
This changes presentation only; query, counts, identities and history are unchanged.

Initial implementation by Data Intelligence (Reporting and Analysis), 2026-10-03.
At that stage, review and closure work remained open. The current delivery checklist
at the top supersedes that historical status. Full live Trusted Run acceptance
remains separate. Production state was unchanged; commits/pushes remain deferred.

## Commands and destinations

Use the project venv and the existing root CLI:

```powershell
$python = (Resolve-Path '.\.venv\Scripts\python.exe').Path
$db = 'C:/evidence/genuine.sqlite3' # replace with an existing initialized database
$package = '68f1ae5db205ab46afef9c4d'
& $python -B -m ck3chronicle.cli runs --database $db --package-id $package --offset 0 --limit 10 --format text
& $python -B -m ck3chronicle.cli runs --database $db --package-id $package --format json
& $python -B -m ck3chronicle.cli report latest --database $db --package-id $package --preset frequent --limit 20
& $python -B -m ck3chronicle.cli report 20261003-74G2EB --database $db --preset hotspots --format html --verbose --output .codex-tmp/reports/hotspots.html
```

Omitting `--database` uses `config.watcher_settings().database`, the current
repository-root `config.toml` authority. No new bootstrap/discovery mechanism was
introduced. A named Run obtains its package through public `get_run`; a supplied
conflicting package fails. `latest` and `runs` require `--package-id`. Neither
reads active package selection nor loads a model. Eligibility and sorting use
08A.1's original source-log modification chronology before `runs` pagination.
All missing/unusable timestamp exclusions and original timestamp values
remain visible even on a small page. Directly selected excluded Runs fail.

Text/JSON default to stdout; `--output PATH` writes UTF-8. HTML requires an
explicit output. `--verbose` writes `NAME-sources.html` beside `NAME.html` and
links each candidate reference to its numbered appendix entry. Keep both files
together. CSS is packaged and embedded; there are no remote assets, JavaScript,
web server, or network requirements for reading reports. Normal reports show
candidate paths/member identities/reference locations without excerpts. Verbose
JSON includes the library's excerpts; verbose text appends the same source views
with `source-N` references. Stored multiline text is exported without Windows
newline translation. A destination cannot overwrite its database/query input.

`--limit` overrides the query's selected/per-Run display bound (default 50).
`--historical-limit` independently bounds preceding identities absent from the
selected Run (default 20). Zero is valid. Totals, identity counts and rollups are
computed first. Text/HTML also bound ranking tables to the current display limit,
show total bucket counts and indicate contributors outside the displayed set.
JSON preserves complete analytical rollups and identity maps, so broad JSON
exports can be large even with a small displayed-record limit.

Exit codes: 0 for success, including an empty result/list; 2 for invalid query,
unsupported preset package or unknown/ineligible/conflicting Run selection;
3 for incomplete required source evaluation; 1 for unavailable reads/output or
other operation failures. Errors print a concise stderr message and a structured
JSON or readable text/HTML result at the requested destination. Partial source
matches are labelled incomplete and never reported as a complete zero.

## Presets and refinements

Choose exactly one `--preset NAME` or `--custom`. Custom requires `--query PATH`.
A preset's optional query refines its base definition using the validated
`InvestigationQuery`; purpose prose does not change filters. The report returns
the actual effective query and a separate preset condition description.

| Name | Defining condition and presentation |
|---|---|
| `hotspots` | `has_source_reference=true` in the preset's AND clause: a stored identifiable script/file reference, through the existing source extractor. File existence is not required. Show occurrence/distinct-record concentrations separately for emitters, referenced paths and candidate associations. |
| `frequent` | Stored exact diagnostics in the effective scope, descending selected occurrence count, then the library's full equality key. No additional classifier or frequency threshold. |
| `syntax` | The research's nine OR selectors, each exact template ID + source family + model revision. Package `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32` only. Both stored statuses remain eligible unless explicitly refined. |
| `new` | `newly_observed=true` in the preset's AND clause: positive exact identities absent from every successfully read included predecessor. No predecessor means positive records are new within that window. |
| `symbol` | Requires a template reference, exact/partial template-text predicate and/or typed-binding selector. These can occur at top level or in every OR selector branch. Each exact identity remains separate. |

For syntax, the assignment-error branch preserves `body` / `s1` / `REASON` /
`present=true` and the exact value
`Trigger is simple assign, but used a symbol other than '=' in the middle`.
The other eight IDs and evidence descriptions are packaged in `presets.py`,
returned in report metadata, and documented in the
[research handoff](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff).
Generic trigger errors, failed context switches, context-dependent named tokens,
missing participant/value messages and unverified brace-balance claims are
excluded. This is the verified initial set, not an exhaustive taxonomy. Other
packages require their own researched selectors; this preset is unavailable there.

Preset conditions and user refinements are ANDed, including mutually exclusive
conditions; these complete with an empty set. The effective `refinement.all`
clauses preserve the preset definition. Scope and ordinary refinement still
apply to every clause. Within a clause, `selectors` are OR alternatives, template
references are OR alternatives and typed bindings are AND conditions. Symbol
selection may be supplied by an AND clause or by every branch of an OR group.
Missing required input and invalid execution controls fail before investigation.
No SQL, Python expression, regex or general-purpose predicate language was added.

## Query controls and composable examples

[member-file.json](../examples/reporting/member-file.json) demonstrates scope,
grouped literal AND/OR includes/excludes and trailing analytics:

```json
{
  "scope": {"source": {
    "members": [{"name": "EB+EC724 Compatibility Patch"}],
    "files": ["common/on_action/sea_minority_on_actions.txt"]
  }},
  "refinement": {"message": {"and": [
    {"contains": "failed context switch"},
    {"or": [{"contains": "culture"}, {"contains": "faith"}]},
    {"not_contains": "effect", "case_sensitive": false}
  ]}},
  "analytics": {"trailing_runs": 5}
}
```

Remove `members` to select only the candidate file, or remove `files` to select
only the member. Member selectors also accept stored `load_order`, `path`,
`root_ID`, `stable_id` and `descriptor_path`; fields inside one member object
are AND, objects are OR. Candidate scopes mean possible association, not blame.
`scope.source.referenced_paths` selects stored references independent of disk
existence. Reports additionally request optional context for that SQL-only query.

Record refinements compose independently with those source scopes:

```json
{"refinement":{"templates":[
  {"template_id":"ca6575c8898718edafb168ca"},
  {"template_id":"575c64f8a3b6e211b735c3ba"}
]}}
```

These stored matched-template references are OR, with optional exact
`model_revision` and `contract_version`. `template_exact: ["COPY RETURNED TEXT"]`
selects exact, case-sensitive stored body-template text. `template_text` uses
literal conditions on that template alone:

```json
{"refinement":{"template_text":{"and":[
  {"contains":"XYZ"},{"contains":"ABC"},{"not_contains":"obsolete"}
]}}}
```

For contains XYZ alone, use `{"contains":"XYZ"}`. Bound values do not satisfy
template-text conditions. `refinement.message` searches the entire rendered
stored record including all bound values. Text matching defaults to casefolded
literal search; individual leaves may set `case_sensitive=true`. Lists of
`source_families`, `match_status`, templates and identities are OR. Ordinary
fields are AND; `refinement.selectors` is OR of compound record predicates.
`occurrences.min/max` always refers to the selected Run, including historical
entries whose count is zero.

[symbol-template.json](../examples/reporting/symbol-template.json) now selects
the whole stored trigger-error template, with no binding, rendered-message or
exact-record restriction:

```json
{
  "refinement": {
    "templates": [{"template_id": "0b2804538785c71278ea37e7"}]
  },
  "analytics": {"trailing_runs": 5}
}
```

This demonstrates template selection: different keys, reasons and script locations
remain eligible, and their exact identities/counts/history stay separate. The
original example also required `KEY=culture` and message contains `failed context
switch`; that narrower query returned one selected identity / 32 occurrences.
It demonstrated combined refinement, not the breadth of this common template.
The corrected template-only query returns 202 selected identities / 396 occurrences
and 61 previously observed identities absent from the selected Run. Across the
four available eligible Runs it finds 263 distinct identities / 1,415 occurrences.

To deliberately narrow this template to that culture/context-switch case, add
both of these fields inside `refinement`:

```json
"bindings": [{"type": "KEY", "value": "culture"}],
"message": {"contains": "failed context switch"}
```

Binding lists are AND; optional `region`/`slot_id` constrain the same binding.
Exact diagnostic selection copies the full returned identity, not a digest,
template alone or Run-local ordinal:

```python
import json
from pathlib import Path
report = json.loads(Path('saved-report.json').read_bytes())
query = {'refinement': {'identities': [report['records'][0]['identity']]}}
# Add scope.source members/files or any other refinement independently.
Path('exact-query.json').write_text(json.dumps(query, indent=2), encoding='utf-8')
```

## Worked trailing-five investigation

```powershell
& $python -B -m ck3chronicle.cli report latest --database $db --package-id $package --custom --query examples/reporting/failed-context-switch.json --format html --verbose --output .codex-tmp/reports/failed-context-switch.html
& $python -B -m ck3chronicle.cli report latest --database $db --package-id $package --custom --query examples/reporting/failed-context-switch.json --format json --output .codex-tmp/reports/failed-context-switch.json
```

The query uses exact stored emitter `jomini_script_system.cpp`, message contains
`failed context switch`, and `analytics.trailing_runs=5`. Five includes the
selected Run and up to four predecessors. The genuine unchanged backup has four:

| Run | Filtered occurrences | Distinct exact records |
|---|---:|---:|
| `20261002-2PVVSE` | 392 | 95 |
| `20261003-IS3QON` | 437 | 80 |
| `20261003-D3N7ZQ` | 0 | 0 |
| `20261003-74G2EB` (selected) | 245 | 51 |

The selected timestamp is `2026-10-03T05:04:14.687380500+00:00`. The accompanying
historical view contains 94 preceding-window identities absent from the selected
Run. Fourteen older Runs lack a usable timestamp and remain outside the window.
The included-window occurrence sum is 1,074 across 145 distinct exact identities,
separate from the selected 245 occurrences / 51 identities.
The report shows per-Run contributors/all candidates and ranks candidate files
both per Run and across the included window. A candidate receives only counts
from Runs where that association exists; distinct full identities are counted
once per window bucket. Overlapping associations are disclosed separately from
unique diagnostic totals. Emitters never become referenced script paths.

The selected sea-minority candidate file refinement produces two exact records /
64 occurrences, with recorded members 114 and 115. Adding member 115 retains
those diagnostic counts with one candidate each. Member-only selection produces
15 exact records / 84 selected occurrences. All are candidate associations;
ownership remains unresolved.

For the alternative *templates containing that phrase*, move the literal from
`refinement.message` to `refinement.template_text`. The genuine context-switch
phrase occurs in bound REASON values, so the tested exact identity matches the
message query and yields a successful empty template-text result. That alternate
query is not equivalent to the worked message investigation.

## History, sources and incomplete evidence

Default history includes up to five preceding and five subsequent eligible Runs
within the same package. Counts, observation fractions, change from the preceding
included Run, newness and absence come directly from 08A.1. `--no-history` or
`analytics.history=false` omits recent commentary. `include_absent` controls the
separate historical view. No median, replacement baseline, notability threshold,
severity inference, causal ownership or confirmed fix is introduced.

Observation fraction = observed successful reads / all successful reads on that
side of the selected Run. Successful absence is zero; failed reads have null
counts, do not enter either fraction term, and are disclosed separately. With
no successful reads, the fraction is unavailable. Newness is relative to included
successfully read predecessors; an unavailable predecessor does not veto it.
Selected-only windows label positive identities new within that window.

Normal context uses each Run's recorded playset. `--source-context PATH` accepts
the source library's selection object. Repeat `--source-root PATH` for explicit
roots outside or inside the recorded playset; repeat `--source-directory RELATIVE`
and optionally add `--no-recursive`. Required filters belong in `scope.source`
and override optional defaults of the same name. All delivered source controls
remain available: roots, members, directories, recursion, files, filename/path
exact or grouped text conditions, extensions, include/exclude and filename/path
globs, file-level grouped content, reference paths/mode and case controls.
`--ripgrep PATH` selects the existing source library executable when needed.

The report displays effective selection, selected roots, recorded member identities
and numbers, coverage issues and actual inventory scopes. Root/member and directory
restrictions precede traversal; known relative paths narrow enumeration to parent
directories, while basename searches traverse the selected scope. All candidates
retain library order and repeated member associations. Explicit outside-playset
roots say recorded load order unavailable. Every displayed diagnostic remains
visible for complete no-file results, incomplete coverage, and unidentifiable
stored references, with distinct explanations.

Verbose source entries use 08A.2 excerpts, referenced line ±10 clipped to current
file boundaries. Lines are numbered; the target has both `>` and visual emphasis.
Missing/out-of-range excerpts explain the limitation. Repeated references may
share an appendix entry; separate recorded-member associations remain distinct.
Source timing is the report generation timestamp, not per-file timestamps or a
claim of historical contents. Review counts/references remain public stored
metadata and are not reconstructed from review files.

## Interfaces, implementation and dependency choice

Runtime path: `HandlerClient` → `DiagnosticAnalysis(client,
source_resolver=SourceSearch(client, context=..., excerpts=...,
candidate_context=True))` → `list_runs` / `investigate` →
`InvestigationResult.to_dict()` → text/HTML/JSON presentation. Analysis and source
search execute in the caller. The database worker and handler operations are
unchanged. The CLI uses public `get_run` only to obtain/check a named Run's package.
It catches `QueryError`, `RunSelectionError`, `ReadError` and
`SourceEvaluationError` separately. Shared `get_logger`/`event` helpers remain the
logging boundary; CLI clients do not configure handlers or log destinations.

Bounded receiving additions are documented in both updated upstream handoffs:
stored reference presence; per-Run/window contributors and association rollups;
candidate provenance in buckets; rendered known partial matches; and the opt-in
optional candidate context for otherwise SQL-only reference filters. No identity,
chronology, history rule, source recognizer, schema or storage path was replaced.

There was no suitable existing runtime HTML renderer. Jinja2 was preferred per
the prompt and its [official API guidance](https://jinja.palletsprojects.com/en/stable/api/),
but installation failed because the environment disallowed the package-index
socket connection. No dependency was partially installed. The delivered renderer
therefore uses standard-library `ElementTree` for automatic escaping, a packaged
`string.Template` HTML shell and packaged CSS. This is an explicit dependency
choice, not a silent runtime fallback or a custom template-expression language.
All data is placed in escaped element text/attributes; only library-generated
elements become markup. Diagnostic/template text, purpose, filenames and source
code never enter raw HTML. Links use encoded local filenames and generated IDs.

Changed source: root `cli.py`; new `reporting/cli.py`, `presets.py`,
`presentation.py`, `templates/report.html` and `report.css`; bounded additions to
`reporting/query.py`, `analysis.py`, `source_search.py`; package data in
`pyproject.toml`. Added three example queries and `test_reporting_cli_genuine.py`;
updated the source test's SQL/history invariance comparison for the added source
data. README, both upstream handoffs, current status/handoff/plan and the reporting
ledger point here. Pre-existing learner/advisory work is preserved.

## Verification and retained outputs

Acceptance uses the unchanged upstream backup at
`.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/unchanged.sqlite3`.
Each suite creates its own disposable SQLite backup; all runtime reads use the
actual public handler and all report checks invoke the actual root CLI. Current
installed source files remain read-only. No fabricated diagnostic histories,
mock clients, altered timestamps or injected failure responses are used.

Commands:

```powershell
$env:CK3_TASK08B_EVIDENCE = (Resolve-Path '.codex-tmp/task08b/evidence.json').Path
& $python -B -m unittest discover -s tests -p test_reporting_cli_genuine.py -v
& $python -B tools/check_runtime_logging.py
& $python -I -B -c "import ck3chronicle.cli; import ck3chronicle.reporting; import ck3chronicle.reporting.presentation"
& $python -I -B -m pip check
& $python -B -m pip wheel . --no-deps --no-build-isolation --wheel-dir .codex-tmp/task08b/dist
```

The evidence manifest names database, package, ignored output root and a genuine
outside-playset root. Retained logs/results are under `.codex-tmp/task08b/`.
`commands.json` inside each consumer exercise records exact commands, exit codes
and stderr. Worked HTML/text/JSON, a full bounded worked HTML with all available
contributors, verbose source appendices, scoped queries and partial-error reports
remain there. They are generated evidence and are excluded from Git.

The first eight-group consumer pass had three failures: two multiline-content
assertions exposed Windows newline translation plus newline-normalizing test
reads; an outside-playset check wrongly assumed the sea-minority file existed in
that root. Exports now avoid newline translation; verification reads their UTF-8
bytes and derives outside-root expectations from genuine files. The next pass
passed all eight groups in 191.639 seconds. The final pass additionally checks
included-window candidate rankings: **eight groups passed, no failures/skips,
179.454 seconds**, recorded in `verification-final.txt`. Final examples are in
`.codex-tmp/task08b/e5e61184ea4a41bcb077858ce49966f6/`: `worked.json`, `worked.txt`,
`worked.html`, `worked-sources.html`, `worked-full.html` and
`worked-full-sources.html`. The full worked view fits all available matching
contributors within its 200-record current/per-Run and historical limits.
After final presentation review, the source scope was made explicit in the
leading summary and partial failures were corrected to retain all fourteen
chronology exclusions rather than displaying an unsupplied empty exclusion list.
Both affected genuine CLI groups passed again (126.077 seconds), including
explicit escaped template/source-text assertions. `verification-presentation.txt`
records this focused pass. The latest worked HTML/text/JSON and complete appendix
are under `.codex-tmp/task08b/c9e83ce2125a45c78c8db4b4ab70d18f/`.
No extra product requirements were proposed by those corrections.

Rerun upstream evidence: six diagnostic-library checks passed in 17.654 seconds;
nine source-library checks passed in 199.944 seconds, including the real broad
content search, outside root, boundary excerpts and partial-reference failure.
These are actual 08B reruns. The previously reported 18 investigations / 359
comparisons, two single-Run checks, 41 scope comparisons and four source
investigations / 93 comparisons remain received upstream evidence, not reruns of
those older scripts. Timing is descriptive only.

Configured-database selection also passed through the root CLI from a disposable
configuration directory (`configured-cli/verification.json`), without changing
the project configuration or reading production SQL. The command omitted
`--database` and returned the four genuine eligible Runs from the disposable file.
Shared logging ownership, isolated imports and pip dependency checks passed.
The wheel was built with pip's existing build support, and both HTML/CSS resources
were inspected in the wheel. An earlier `python -I -m build` attempt failed because
that module is not installed; no build dependency was installed. Representative
text/HTML content, exact messages/identities/history, clipped source lines, escape
output and every main/appendix fragment link are checked from actual generated
files. A browser screenshot attempt did not complete: Chrome's GPU process failed
under the restricted environment and Edge did not produce an image. Browser visual
layout was unverified at that earlier stage; the current closure walkthrough
above now supplies actual browser and screenshot evidence. Only the disposable browser process was stopped.

## Current evidence limits and continuation

Use the [current delivery checklist](#current-delivery-status--2026-10-04) for the
authoritative status and two unexercised fault groups. Seven genuine eligible
Runs, the complete syntax-selector checks, explicit missing history positions,
genuine missing playsets, the authorized missing-file fixture and the CLI/worker
I/O trace are delivered evidence. Eleven simultaneous Runs and removal of
original logs/models are not acceptance prerequisites. No 08B implementation
continuation is known; a later genuine runtime fault should retain its result for
checking the corresponding inspected handling. Full live Trusted Run acceptance,
configuration-bootstrap replacement, commits and pushes remain outside this work.
