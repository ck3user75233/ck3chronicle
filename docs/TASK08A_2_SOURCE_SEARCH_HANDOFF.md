# Task 08A.2 — source search and diagnostic context

## Owner rule: last load order identifies the file/line error source — 2026-10-04

The owner now directs single-file/line analytics to identify the last matching
playset member in load order as the error source. This supersedes the earlier
blanket “winning file/ownership unresolved” presentation requirement for this case.
`file_line_sources(candidates)` is a pure public analysis helper, independent of
templates and disk reads. Resolver results add an identity-keyed `file_line_sources`
map; each group supplies relative path, line, candidate IDs, rule `last_load_order`,
an `error_source` file/member object and a reason when no assignment is possible.
Analysis forwards these groups into selected, historical/per-Run and partial records.

Groups use the effective source scope and resolved files before file-content
filtering, so excluding the last file's contents does not promote an earlier copy.
All original candidate associations and their order remain intact. No line or no
comparable load order means this file/line rule cannot assign a source; explicit
outside-playset roots retain their unavailable order. No parser, schema, stored
identity or current-path-resolution predicate changes. Reports display `resolved`
as **Resolved**, and completed zero-match `unresolved` as **File not found**.
See [08B](TASK08B_REPORTING_HANDOFF.md) for genuine CLI and browser checks.

## Owner clarification: game-relative paths across playset members — 2026-10-04

The ordinary path filter is relative to each playset member's root. Use
`scope.source.relative_path.exact`, for example
`["/common/scripted_effects/some_file.txt"]`. It matches the recorded relative path;
optional candidate lookup checks that same location across every recorded member
unless roots/members are explicitly restricted. All candidate associations remain
in recorded order. A matching basename in another folder is not a path match.
Exact paths continue to restrict inventories to their parent folders, nonrecursively.

`normalize_source` now accepts an optional single leading slash in the explicitly
relative fields `relative_path.exact` and `directories`, along with either separator.
It works on a copy; the request and stored references are unchanged. Standalone
`effective_selection` shows the normalized scope. Physical `roots`/`files`, UNC paths
and literal text predicates are not reinterpreted. Default stored-path investigation
remains SQL-only; reports opt into candidate context. See [08B](TASK08B_REPORTING_HANDOFF.md)
for genuine root-CLI, standalone and scoped-inventory verification.

## Owner correction: an emission without a path is complete — 2026-10-04

An emission need not supply a source-file path. Its absence is normal, not a
reference limitation or incomplete evidence. `source_references` now returns
`status: "present"` or `"no_path"` alongside `references`, replacing `limitation`.
The resolver returns an identity-keyed `reference_status` map. Neutral coverage
`records_without_source_path` replaces `reference_limitations`/`reference_complete`;
no-path records do not lower coverage completeness.

If no selected references need lookup, optional context does not read the playset
or probe roots: `searched` is false, file/folder counts are zero and source coverage
is complete. With mixed records, an actual source lookup problem concerns only
records carrying references. Existing source-path filters still exclude no-path
records normally. No diagnostic, parser classification or database schema changes.
See [08B](TASK08B_REPORTING_HANDOFF.md) for genuine CLI/archive verification.

## Owner-requested recursion measurements — 2026-10-04

Source search now returns per-search `coverage.search_counts`, separately from the
existing cumulative session `coverage.metrics`:

- `files_searched`: unique physical file names/paths considered in the effective
  inventory scopes, before file/path/content filters;
- `folders_searched`: unique enumerated folders, including the starting directories
  and empty folders;
- `candidate_files`: unique files selected before content filtering;
- `content_files_requested`: unique files selected for a content check, zero if
  none was requested; this is not a claim that every read succeeded;
- `matching_files`: unique files remaining after the source predicates.

`coverage.search_scopes` lists every selected root/member, actual lookup directories,
effective recursion, file/folder counts, completion/skipping and cache source
(`none`, `exact_scope`, `whole_root_subset`). Cached inventories preserve the
same applicable counts, including empty folders. Repeated/overlapping roots retain
their associations; global search counts deduplicate physical paths and per-root
rows are not additive. Incomplete coverage counts only the evaluated work and is
still labelled incomplete. SQL-only stored-path selection returns zero filesystem
counts. Existing construction metrics now also measure folders and attach counts
to `inventory_scopes`; they remain cumulative, not per-search totals.

Exact files/references still narrow lookup to parent directories within the
requested scope. Reports do not recursively scan a whole root merely to print
its total. `tools/check_source_recursion.py` independently measures full real roots
using PowerShell, compares returned file sets and counts for recursive/nonrecursive,
scoped and cached searches, and exercises root-CLI presentation from a disposable
database backup. See [08B](TASK08B_REPORTING_HANDOFF.md) for actual receipts.

## Owner-requested explicit path-resolution filter — 2026-10-04

The owner asked to seek messages whose recorded paths could not resolve. Use
`scope.source.resolution: "unresolved"` (or `"resolved"`) in diagnostic queries.
This explicitly requests current disk evaluation even in default library use.
It does not change SQL-only ordinary path predicates. `resolution` is not a
standalone file-search or optional-context option; validation directs callers to
the diagnostic query field.

For each original reference, `resolve` returns `reference_resolution[identity_key]`
entries with `reference`, `status` and ordered `candidate_ids`. Status is:

- `resolved`: at least one current file found in the effective scope;
- `unresolved`: a completed search found none for this reference;
- `incomplete`: no file found, but search coverage cannot establish absence;
- `not_searched`: disk context was not requested for a stored-path-only query;
- `outside_scope`: this reference does not satisfy the required path predicates.

No usable stored reference produces an empty reference list and a normal nonmatch.
Selection is existential per diagnostic: one selected reference with the requested
status suffices; a diagnostic can contain both resolved and unresolved paths.
Root/member predicates choose where resolution is tested, rather than requiring
a positive candidate when `resolution: "unresolved"` is present. Directory/path
filters still compose normally. File existence is evaluated before content filters:
an existing file with nonmatching content remains resolved. A separately required
content predicate needs a matching candidate, possibly from another reference.

Unresolved means absent within the disclosed scope; it is not a global filesystem
or historical fact. Incomplete required search retains `SourceEvaluationError`
and known matching partials. Current coverage is conservative across the selected
scope: unresolved references are unknown if the search could not complete.
`coverage.searched` distinguishes skipped lookup, and `resolution_filter` records
the requested status. Analysis exports the per-reference result and reports show
it beside each path. No persistent index, parser or database schema is added.

Genuine CLI checks, independent filesystem/count verification and the authorized
two-entry fixture pass; exact receipts are in [08B](TASK08B_REPORTING_HANDOFF.md).

## Owner correction: ordinary path filters — 2026-10-04

The owner's later clarification supersedes the missing-file and unidentified-
reference error rules below. In diagnostic investigations, path-only predicates
(`files`, `referenced_paths`, filename/relative-path conditions, directories and
globs/extensions) match recorded references. A matching file need not exist on
disk. No usable matching reference means exclusion, not incomplete evidence.
Source context remains optional for these predicates; default library use stays
SQL-only, while reports request candidate context. Absolute paths can be compared
with relative references through lexical recorded-root metadata without probing
disk. This establishes a possible path correspondence, not ownership.

Root/member/content predicates still use current candidate associations, after
excluding pathless and path-nonmatching records. Missing individual files return
ordinary nonmatches, including in standalone `search`. Actual selected-root,
traversal/read/decoding and search-process failures retain incomplete coverage.
No references left to evaluate means a complete empty result without disk probes.
Required-filter partials no longer contain an `unidentified_records` view.

Four focused genuine source groups passed (33.856 s); two genuine CLI groups
passed (70.665 s). The authorized two-entry fixture passes nine checks / nineteen
exports for recorded paths, missing files, directory/absolute paths and empty
mod candidates. See the current [08B handoff](TASK08B_REPORTING_HANDOFF.md) for
evidence and the report bundle. This is a bounded source/query-owner correction;
no storage, parser, matcher or architecture change.

## Earlier owner-authorized missing-file fixture — superseded filter semantics

The earlier fixture used two copied genuine emissions with fake file LOCATOR paths
and all 133 recorded playset members preserved. It exposed an incorrect distinction
between `files` and other stored-path selectors: `files` incorrectly failed when
the physical file was missing. Its original empty-result expectation and subsequent
error expectation were both superseded by the owner's clarification.

Current behavior: `files`, `relative_path.exact` and `referenced_paths` select
matching stored paths. Both fixture messages are returned when both recorded paths
are selected; an unmentioned path returns a successful empty result. No disk file
is required to answer that database question. Optional file lookup may find no
candidates without invalidating the diagnostic selection. See the current
[08B handoff](TASK08B_REPORTING_HANDOFF.md) for corrected checks and retained
historical receipts. The fixture is labelled synthetic and does not establish
unavailable-root or decoding-failure behavior.

## 08B source-presentation completion — 2026-10-04

The source evaluator's membership and incomplete-evidence rules are unchanged.
08A.1 now includes readable `unidentified_records` in required-source error
partials, derived from this resolver's existing `reference_limitations`.
Reports display these separately from known matches and name the diagnostic
whose mod/file condition cannot be evaluated. Stored reference presence remains
independent of current file existence; mod membership means a current candidate
under the root selected through that evidence Run's stored playset, not ownership.
The hotspots preset now expresses its stored-reference condition through an
AND refinement clause, using the same extractor.

All nine genuine source tests passed again (260.071 seconds). A genuine DLC-file
CLI example additionally confirms plain base-game/DLC paths alongside a named mod
candidate. Exact consumer evidence and browser inspection are in the current
[08B handoff](TASK08B_REPORTING_HANDOFF.md).

## 08B receiving additions — 2026-10-03

`SourceSearch(..., candidate_context=False)` has one opt-in constructor argument.
Reports pass `candidate_context=True`: stored-reference-only filters retain their
SQL membership while also looking up optional disk candidates. The default still
performs zero disk inventory for these queries. Optional disk gaps remain in
`coverage.complete`; they do not invalidate a complete stored-reference filter.
Other required-source predicates retain their existing evaluation/error behavior.

Resolver coverage now includes `effective_selection` and
`reference_only_filter`. Reports display those scopes and preserve all roots,
issues, inventory-scope metrics, candidates, member numbers and excerpts. The
hotspots query's new `scope.has_source_reference` calls this owner's existing
extractor from the query library; no new path-recognition logic was added.

The nine retained genuine source checks passed again during 08B (199.944 seconds).
The optional-source invariance assertion now compares window counts/history,
excluding the newly added candidate-bearing per-Run views/rollups. All data and
membership/count expectations remain unchanged. See [08B handoff](TASK08B_REPORTING_HANDOFF.md)
for CLI-specific evidence, newline repair and remaining unverified cases.

Current scope correction, 2026-10-03: **only unscoped searches default to all
recorded-playset roots**. Explicit roots/members are selected before disk probes;
explicit directories limit traversal. Exact files/relative references now narrow
enumeration to their actual parent directories, nonrecursively, intersected with
explicit directory scope. Filename-only/basename searches have no known parent
and traverse their selected root/directory scope. SourceSearch docstrings state
this distinction. The earlier broad interpretation of owner acceptance was wrong.

The known-path traversal defect is now fixed in `source_search.py`. Genuine scope
verification passed 41 comparisons, and four genuine multi-Run source investigations
passed 93 comparisons without a directory workaround. All candidate/member pairs
and per-Run identity/count maps agreed. All nine retained genuine source tests
also passed (291.710 seconds, no failures/skips); logging/imports/pip passed.
Current readable scope evidence:
`.codex-tmp/task08a2/scope-repair/SOURCE_SCOPE_REPORT.md`.

Current genuine-history verification: [multi-Run receiving results](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md).
The October 3 owner correction replaces median-based comparisons with actual
counts/fractions and newness over included predecessors. Reverification passed
18 genuine investigations / 359 comparisons; source totals/candidates are unchanged.
October 3 verification completed mod/file investigations across four eligible
timestamped Runs using each recorded playset, with expected/actual per-Run
identity/count maps and candidate/member provenance agreeing. The 14 older Runs
remain excluded. Source-filtered history is now exercised end-to-end; unavailable
source/read cases remain unexercised. The latest source rerun omitted explicit
parent directories for exact file queries and verified automatic narrowing.

Reporting owns the new `SourceSearch` library and its integration with
`DiagnosticAnalysis`. It uses stored definitions and values through the existing
public handler and searches current files read-only. No pipeline, watcher,
learner, schema, live process or selected package is changed. 08B owns the report
and CLI presentation. Generated demonstrations remain under ignored
`.codex-tmp/task08a2/`.

## Public API

```python
from ck3chronicle.reporting import SourceSearch, source_references

SourceSearch(client=None, *, ripgrep='rg', context=None, excerpts=False,
             scratch_directory=None, candidate_context=False)
SourceSearch.read_playset(run_id) -> dict
SourceSearch.search(selection: dict, *, run_id: str | None = None) -> dict
SourceSearch.resolve(run, records, scope) -> dict
SourceSearch.excerpts_for(paths_and_lines: dict[str, set[int]]) -> dict
SourceSearch.clear()
SourceSearch.begin_investigation()
source_references(record: dict) -> dict
```

The optional client is a `HandlerClient`, never a repository. Explicit-root
searches need neither a client nor a Run. `read_playset` checks the stored Run,
then returns `available`, `stored`, and ordered `members`, each containing its
unchanged member object plus current `available`/`reason`. Null fields, repeats,
load order and all stored identifiers remain intact. No descriptor/debug-log
reconstruction occurs. Missing recorded playsets remain unavailable.

`context` supplies optional source-selection defaults. With no explicit roots or
member selection, a resolver uses that Run's recorded playset. `scope.source` in
an investigation supplies **required** source predicates and overrides defaults
of the same name. A required incomplete association raises
`SourceEvaluationError`; `.partial` retains the resolver's known matches,
candidates, references and coverage. It is not a complete filtered result.
Optional unavailable context leaves the SQL investigation usable. Handler read
failures remain `ReadError`, not successful empty playsets.

## Source selection

`search(selection, run_id=...)` and `InvestigationQuery.scope.source` use the
same validated JSON-compatible fields. Fields compose with AND; alternatives
within a list compose with OR. Omit an unrestricted field. Empty selections,
lists and Boolean groups, unknown fields and invalid types raise `QueryError`.

| Field | Meaning |
|---|---|
| `roots` | Ordered absolute directory strings, independent of playset membership. |
| `members` | OR list of objects selecting stored `load_order`, `name`, `path`, `root_ID`, `stable_id`, or `descriptor_path`; fields inside an object use exact AND, including nulls. |
| `directories` | Relative directory scopes under each root; default `['.']`. Absolute paths and parent traversal are rejected. |
| `recursive` | Default true; false uses a single-directory inventory. |
| `files` | Exact recorded paths in path-only investigations; no disk existence requirement. With root/member/content predicates, select current candidate files. Standalone search selects disk files. Missing/out-of-scope files are ordinary nonmatches. |
| `extensions` | OR list, with or without leading dot. |
| `filename`, `relative_path` | Objects with `exact` string alternatives and/or a `text` literal condition tree. Both, if supplied, must match. |
| `filename_globs`, `path_globs`, `include`, `exclude` | `fnmatch.fnmatchcase` patterns; slash is an ordinary character, so `common/*` includes descendants. Exclusion wins. No custom glob engine or shell expansion. |
| `case_sensitive` | Exact path/name/glob/reference comparisons; default false. Each text leaf has its own case option. |
| `content` | Nested `and`/`or` groups of literal `contains`/`not_contains` leaves with optional `case_sensitive`. Evaluated over the whole file. |
| `referenced_paths` | Select stored references in investigations, or relative inventory paths in standalone search. Like other path-only filters, this does not need disk access. |
| `reference_mode` | `relative` by default, preserving supplied directories; `basename` explicitly broadens lookup. |

With both `members` and `roots`, only selected recorded members whose root is
also explicitly listed remain. To search outside the playset, supply `roots`
without a member restriction. No implicit parent/root discovery occurs.

Examples:

```python
# Default recorded-playset lookup, all matching candidates.
files = sources.search({'filename': {'exact': ['sea_minority_on_actions.txt']}},
                       run_id='20260930-CWO6LH')

# Explicit roots, independent of stored playset data.
files = SourceSearch().search({
    'roots': [r'C:\my-mod'], 'directories': ['common'], 'extensions': ['txt'],
    'content': {'and': [
        {'contains': 'culture'}, {'contains': 'faith'},
        {'not_contains': 'obsolete', 'case_sensitive': True},
    ]},
})
```

`search` returns `effective_selection`, `files`, and `coverage`. Each file has
`candidate_id`, `root`, `root_order`, unchanged `member` (null for explicit roots),
`relative_path`, `physical_path`, and numbered `matching_lines`. Positive terms
on different lines can satisfy AND. Negative predicates inspect the entire file;
an exclusion-only match has an empty positive-line list. All matches are returned
in member/caller-root order, then stable relative-path order, without a display
cap. `coverage` distinguishes matching associations from unique physical files,
includes roots/issues, explicit search settings and cumulative timing/work metrics.

## References, candidates and excerpts

Reference extraction uses `contracts.render_regions` and stored ordered bindings.
Path-valued LOCATORs retain their slot identifier; paths in stored literal/support
text are also located. Adjacent `line`, `near line`, and `line … and column … in`
wording supplies line numbers. Script-stack locations retain supporting roles and
region references. Numeric locators and C++ emitter names are not script paths.
An emission without a file reference has status `no_path`; source lookup is not
applicable. This is normal emission content, not a limitation. No location is guessed.
This is reference lookup, not another matcher, syntax catalog or semantic classifier.

Every matching physical/member association is retained, including repeated
members. A candidate ID identifies the root-order/root/relative-path association;
it is not diagnostic identity, a content fingerprint or proof of ownership.
Full definition-scoped contract equality remains the sole diagnostic identity.
Candidate rollups disclose overlap and never inflate the investigation's unique
record or occurrence totals. SQL selectors and selected-Run count refinements
are applied before source association. Chronology/history rules are unchanged.

Returned diagnostic entries add `reference_details` and `candidates` to the
existing `references` list. Candidates carry their originating references and,
when requested, `excerpts`. Excerpts have `available`, `line`, `total_lines`, and
numbered `lines` with a Boolean `target`; they include +/-10 lines clipped to the
file. Missing line numbers, unreadable text and out-of-range lines have explicit
unavailable reasons. No replacement line is guessed. `excerpts_for` returns a
mapping keyed by `(physical_path, line)` for Python callers; composed investigation
results remain JSON-compatible lists/objects.

These are **current possible locations and contents**. Neither the winning mod,
error owner, historical content nor a repair is inferred. Individual file
observation times are not recorded. 08B supplies report generation time.

## Search implementation and reuse

### Owner-requested memory and scope review — 2026-10-02

Original acceptance measured time/counts, not memory. The follow-up uses real
stored references and the same installed playset; details/raw measurements are
in ignored `.codex-tmp/task08a2/memory/MEMORY_REVIEW.md`. No runtime strategy was
changed during this review. Python `tracemalloc`/object sizing and Windows process
counters were already available; no package was installed.

The 105,603-entry full inventory retains 12,101,079 bytes (11.54 MiB) of Python
objects. For the single known sea_minority path, nonrecursive inventory of only
`common/on_action/` retains 98,321 bytes (96 KiB), covering 433 entries and finding
the same two candidates. Across all diagnostics, 1,786 references reduce to 454
distinct paths in 120 parent directories. Inventories limited to those parents
retain 2,811,521 bytes (2.68 MiB), covering 25,786 entries, with exactly the same
495 distinct root/file pairs as the full inventory. These are inventory sizes,
not whole-application peaks or bounds for content results/excerpts.

A separate direct `os.stat` experiment reaches those same files without an
inventory, using 60,382 root/path checks for all references. One literal path
comparison differed (`CCU_on_actions.txt` on disk versus `ccu_on_actions.txt` in
stored evidence); `Path.samefile` confirmed the same Windows file. It is a small
I/O experiment, not a replacement for production coverage/case/provenance rules.

Historical scope review (the correction is now delivered above): a user-scoped
search must not enumerate a broader scope
merely to populate a cache. The current automatic reference resolver retains
relative-path matching but still inventories entire selected roots first unless
directories are supplied. Narrowing that traversal remains a receiving change,
not something demonstrated by the original filename benchmark. Recommended
direction: deduplicate exact references, use direct path checks or inventories
of their actual parent directories, and reserve broader traversal for explicitly
broader queries. Reuse applies only to the same scope or a proven covered subset;
there is no demonstrated need for a growing cross-query or persistent index.

### Delivered implementation

Python 3.12.14 and the already-installed ripgrep 15.2.0 were used. No `.venv`
dependency or executable was installed. Ripgrep is MIT/Unlicense dual-licensed;
it is a Windows executable invoked by Python, not a Python import. Consumers
need `rg` on PATH or `SourceSearch(ripgrep=r'C:\tools\rg.exe')`. Windows installation
is available with `winget install BurntSushi.ripgrep.MSVC`, subject to the owner's
approval. Missing executable errors identify both configuration and installation
options. See the [official guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md).

`os.walk(onerror=...)` / `os.scandir`, `pathlib`, and
[`fnmatch.fnmatchcase`](https://docs.python.org/3/library/fnmatch.html) provide
inventory and path filtering. The documented ordinary-slash glob semantics do
not need wcmatch; no substitute glob engine was written. Existing query validators
and a shared Boolean evaluator are reused. Standard-library subprocess, tempfile,
codecs and JSON handle ripgrep transport, strict decoding and streaming output.
Existing `HandlerClient`, contract identity/rendering and 07E event/logger helpers
retain ownership. The subsequent owner-directed 08A.1 correction removed the
median calculation; current history uses counts, fractions and included-window
newness, as recorded in the diagnostic-query handoff.

Inventories are cached per physical root/scope; narrower scopes can reuse a
complete root inventory. Repeated members retain associations without repeating
an identical traversal. Diagnostic references are indexed against candidate
relative paths/basenames in a batch, with path filtering before content reads.
Encoding validation and content/excerpt results are cached during the session.
`begin_investigation` clears caches before each investigation; standalone callers
use `clear()` before refreshing a changed installation. No persistent index,
queue, resident service, additional worker or alternative backend was added.

Ripgrep receives `--no-config --json --fixed-strings --text --hidden --no-ignore
--encoding auto --no-mmap --color never --line-number --with-filename` plus explicit
case control. Literal patterns use a temporary pattern file; multiline literals
use `--multiline` and separate `-e` arguments. Windows command-line-sized batches
contain all selected files; this is transport sizing, not a result limit. Output
is consumed one JSON event at a time. Only inventory strings and returned matches/
requested excerpt lines are retained, never an accumulated copy of all file data
or subprocess stdout. Source text must decode strictly as UTF-8 (optional BOM) or
BOM-marked UTF-16; other encodings are coverage failures. Ignore files, hidden
files and binary heuristics cannot silently prune the requested inventory.
Source-content candidate detection uses ripgrep's Unicode case-insensitive
matching; diagnostic/template text retains Python `str.casefold()` semantics.
Full Unicode multi-character folding equivalence between those engines is not
claimed. The genuine content queries exercised ASCII script identifiers.

Exit 0 means matches; exit 1 means a completed no-match search; other exits or
stderr diagnostics mark incomplete coverage. Known positive matches may survive
an errored batch; absence requires completed evidence. A missing/unreadable root,
archive/file mount or traversal/read/decoding failure can prevent completion of a
filter requiring that disk evidence. Pathless records and missing individual files
are ordinary nonmatches. Optional context still preserves SQL data; path-only
membership remains independent of disk coverage.

## Concrete 08B consumer

Owner clarification (2026-10-02): visibly show each mod's stored
`candidate['member']['load_order']` beside its name in the report and source
appendix, preserving the number without renumbering. Ordering the list alone
does not satisfy this display requirement. Explicit roots outside the recorded
playset have no recorded load order; label it unavailable. The readable real-data
report now includes the full 133-member load-order table and explicit numbers
on candidate and excerpt headings. This presentation update reuses saved genuine
handler results; it requires no runtime library changes or new tests.

```python
from ck3chronicle.pipeline.request_handler import HandlerClient
from ck3chronicle.reporting import DiagnosticAnalysis, SourceSearch, SourceEvaluationError

client = HandlerClient(database_file)
sources = SourceSearch(client, excerpts=True)
analysis = DiagnosticAnalysis(client, source_resolver=sources)
query = {
    'scope': {'source': {
        'members': [{'load_order': 114}, {'load_order': 115}],
        'files': ['common/on_action/sea_minority_on_actions.txt'],
    }},
    'refinement': {
        'templates': [{'template_id': '0b2804538785c71278ea37e7'}],
        'bindings': [{'type': 'KEY', 'value': 'culture'}],
        'message': {'contains': 'Failed context switch'},
    },
    'display': {'limit': 20},
}
try:
    result = analysis.investigate('latest', package_id=package_id, query=query)
except SourceEvaluationError as exc:
    # Render an incomplete-filter explanation and known partial candidates.
    # Do not label their count an exact filtered total.
    incomplete_source_data = exc.partial
else:
    report_data = result.to_dict()
    # Render stored messages, pre-limit totals, coverage, candidate provenance
    # and candidate['excerpts']; no additional file lookup belongs in the UI.
```

Normal consumers follow the existing application's handler lifecycle; they do
not shut down a shared live handler after each report. SQL-only use remains
`DiagnosticAnalysis(client)` with no resolver. Review metadata and unavailable
historical evidence remain the original 08A.1 contract.

## Verification and remaining evidence limits

Acceptance uses only unchanged genuine CK3 SQL and installed sources. No
synthetic/scalar checks, generated diagnostic/source fixtures, mock clients,
injected errors, rewritten timestamps or invented history are included.

Input: unchanged disposable SQL evidence for Run `20260930-CWO6LH`, package
`68f1ae5db205ab46afef9c4d`; 2,475 records / 4,182 occurrences, one eligible Run.
All 133 recorded member roots were present. Each check suite made a fresh offline
backup and then used only the public handler for its runtime reads. Installed
game/mod sources were read in place without changes. The explicit outside-playset
case searched installed More Bookmarks+ (`steam_workshop:2216670956`) without a
client or Run. This is genuine source data, not a generated directory fixture.

Final evidence is in ignored
`.codex-tmp/task08a2/7db8b47229564e748a47221366512b0b/`.
The readable report is `.codex-tmp/task08a2/SOURCE_SEARCH_REAL_DATA_REPORT.md`.
It shows effective filters, actual returned excerpts, candidate paths, query
errors for unavailable real reference evidence and precise checks. Full result
JSON is saved beside the disposable database; no evidence is added to Git.

| Measured operation | Scope | Final seconds |
|---|---|---:|
| First exact filename lookup | 133 roots; 105,603 inventory file entries; two candidates | 8.652 |
| Inventory construction within that lookup | 133 root inventories | 7.933 |
| Reused-inventory filename lookup | Same candidates, no new inventory | 0.640 |
| File-level content AND | 11,914 common/*.txt associations; two matches; 66 Windows batches | 13.181 |
| Full diagnostic investigation with optional candidates | 2,475 diagnostics, 1,786 extracted references | 10.144 |
| Inventory construction within investigation | 105,603 entries | 8.364 |
| Batched reference association after inventory | 495 candidate file associations available to references | 0.021 |

The earlier successful run took 62.297 seconds for the same content scope versus
13.181 on the later pass; filesystem cache state was not controlled. These are
observed timings, not a new acceptance threshold. Candidate associations totaled
2,651 across 1,377 diagnostics; 710 diagnostics had overlap. There were 1,429
diagnostics with identifiable references and 1,046 without. Both statuses remain
in the original SQL totals. All naturally searched roots/text were readable;
the broad content pass reported no coverage failures.

Nine checks in `tests/test_source_search_genuine.py` passed in the initial run
(110.998 seconds) and the final run (64.248 seconds), with no failures or skips:

1. `test_01_recorded_playset_and_full_inventory_reuse`: compare stored members
   with public handler data; preserve metadata/nulls/order; locate both real
   sea_minority files at member orders 114/115; reuse the full inventory.
2. `test_02_large_playset_batched_content`: search all selected common text
   files; verify both literals and numbered result lines against actual contents.
3. `test_03_file_level_groups_negatives_and_windows_no_match`: terms on different
   lines, nested AND/OR, whole-file exclusion, exclusion-only empty line lists,
   case-sensitive no-match and ripgrep exit 1. Normal matches exercise exit 0.
4. `test_04_explicit_unrecorded_root_and_path_filters`: no-client explicit root,
   non-recursion, extension/include/exclude, partial filename, exact relative
   path and filename/path globs on the real outside-playset descriptor.
5. `test_05_many_diagnostic_references_preserve_sql_totals`: full reference
   investigation, real overlap and unchanged SQL totals/window evidence.
6. `test_06_member_file_template_exact_identity_composition_and_excerpts`:
   composed member/file/template/full-identity/KEY/message/template-text query;
   five occurrences remain one diagnostic despite two candidates; line 141 +/-10
   matches current file contents, retaining binding slot `s2`.
7. `test_07_script_stack_and_real_boundary_excerpt`: eight real diagnostics /
   sixteen occurrences, supporting stack references, and clipping the actual
   health_on_actions.txt line-4 excerpt to lines 1–14.
8. `test_08_real_unlocated_diagnostics_are_unavailable_required_evidence`: one
   genuine unlocated diagnostic plus the known culture diagnostic under member
   115; explicit incomplete-filter error retains the known partial candidate.
9. `test_09_stored_reference_filter_and_explicit_basename_mode`: two diagnostics /
   ten occurrences selected from stored paths without inventory construction;
   explicit broader basename search returns the actual candidates.

The six existing genuine-data checks in `test_reporting_query_requirements.py`
also passed (31.454 seconds, no failures/skips): display-limit totals/rollups;
unavailable no-history novelty; public reads/totals/review/short history; explicit
record selector with positive occurrence count; template OR/exact identity/typed
binding/message composition; template text independent of bound values.

Commands actually run with the project venv:

```powershell
$env:CK3_TASK08A2_EVIDENCE=(Resolve-Path .codex-tmp/task08a2/evidence.json).Path
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_source_search_genuine.py -v
$env:CK3_TASK08A_EVIDENCE=(Resolve-Path .codex-tmp/task08a1/evidence.json).Path
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_reporting_query_requirements.py -v
.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py
.\.venv\Scripts\python.exe -I -B -c "import ck3chronicle.reporting; import ck3chronicle.reporting.source_search; import ck3chronicle.pipeline.request_handler"
.\.venv\Scripts\python.exe -I -B -m pip check
```

Logging ownership, isolated imports and dependency consistency passed. The
removed synthetic logging suite was not restored or run. Logs are
`verification-first.txt`, `verification-final.txt`, `diagnostic-regression.txt`
and `environment-checks.txt` under `.codex-tmp/task08a2/`.

No acceptance assertion failed. An early inspection print failed with
`UnicodeEncodeError` on a Unicode mod name in the Windows console; the saved JSON
was unaffected and inspection output was escaped. Inspection found and corrected
overlap between a binding-path match and a stored-text match that obscured its
slot provenance. No test-specific branches or additional product requirements
were introduced. Error/partial-evidence handling implements the assigned contract.

Not naturally exercised: missing/unreadable roots or playsets, archive mounts,
decoding failures, ripgrep process errors/missing executable, repeated identical
member roots, UTF-16/multiline literals, out-of-range stored line numbers, and
multi-Run history. No fake errors, files, members or Runs were created to claim
those cases. Genuine missing-reference evidence exercised required-filter
unavailability and known partial matches, not an unreadable-root or process-error
claim. No missing upstream operation blocks the delivered interface.

## Changed files

- `src/ck3chronicle/reporting/source_query.py`, `source_references.py`,
  `source_search.py`: source validation, extraction and search/context service.
- `src/ck3chronicle/reporting/query.py`, `analysis.py`, `__init__.py`: shared
  evaluator, source-query receiving integration, resolver session and exports.
- `tests/test_source_search_genuine.py`: real SQL/source acceptance only.
- This handoff, 08A.1's handoff and current status/plan/handoff/decision ledger.

All unrelated dirty work is preserved. Generated reports, returned evidence,
verification logs and disposable databases are ignored and excluded from Git.
