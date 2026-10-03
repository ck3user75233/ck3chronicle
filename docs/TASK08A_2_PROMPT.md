# Task 08A.2 Prompt — Source File Search and Context

## Assignment

You are the Reporting and Analysis team. Implement the reusable library
capabilities for searching requested source roots, including a Run's recorded playset, identifying all
source candidates and providing excerpts. Integrate candidate-based member/file
filters with 08A.1's diagnostic investigations. Task 08B builds the reports and
CLI on both deliveries. Read all three prompts; execute 08A.2 here after 08A.1.

The intended journey is: select a Run and processing package, describe an
investigation with filters, retrieve matching diagnostics, show their recent
history, and find every candidate source file in the requested search scope. A later
HTML report or NiceGUI interface must consume the same analysis results.

## Orientation and boundaries

Checkout: `C:/Users/nateb/Documents/ck3chronicle`.
Read `AGENTS.md`, applicable nested instructions, `docs/DEVELOPMENT_ENVIRONMENT.md`,
`docs/BANNED_IDEAS.md`, and the opening current sections of `docs/PROJECT_PLAN.md`,
`docs/PROJECT_STATUS.md` and `docs/CURRENT_HANDOFF.md`. Then read:

- [Current reporting decisions](TASK08_SCOPE_REVIEW.md),
  [08A.1](TASK08A_1_PROMPT.md), [08A.2](TASK08A_2_PROMPT.md) and
  [08B](TASK08B_PROMPT.md).
  These prompts derive from the owner's updated 2026-10-02 drafts; where older
  planning text conflicts, these prompts govern.
- [Owner intent](OWNER_PRODUCT_INTENT.md) and the identity/rendering sections of
  [the Error Contract](ERROR_CONTRACT_SPECIFICATION.md).
- [07D's current API handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md),
  [07E logging](TASK07E_RUNTIME_LOGGING_HANDOFF.md), and
  [source timestamp delivery](WATCHER_SOURCE_MTIME_HANDOFF.md).

Inspect the owning source before extending it. In particular, use
`pipeline.request_handler.HandlerClient` for all runtime database access and
`pipeline.contracts` for stored identity/rendering. Existing public reads include
`get_run`, `list_runs`, `read_diagnostics`, `read_playset` and
`read_review_metadata`. Callers never open SQLite or receive repository objects.
Perform searching, analysis and presentation outside the database worker.

Reporting owns these new library services. Pipeline owns repository/handler
operations; watcher owns capture/playset production; learner owns parser,
matcher and model changes. If an actual missing upstream operation prevents a
required result, specify that operation and its receiving check for its owning
team. Continue independent work; do not create a parallel access path.

Preserve unrelated changes. Verification uses disposable storage; do not restart
live processes, ingest production captures, reset databases, expire files,
change package selection, commit or push. Do not read the rejected shared
database handler design, copies or continuation instructions. Current 07D APIs
are the receiving boundary.

## Split boundary and receiving interface

Read `docs/TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md` and its actual implementation
before integrating. Reuse its structured query, diagnostic filtering, identity,
Run selection, recurrence, notability and rollups; do not reimplement them.

This task owns source-reference extraction, recorded-playset lookup, member/root
and file selection, all-candidate disk search, excerpts and their integration
with the shared investigation query. Complete the mod/member and candidate-file
filter composition left to this task by 08A.1. Associate candidates with the
existing exact diagnostic identities; keep diagnostic totals independent of the
number of candidate associations. Resolve bounded receiving-interface gaps in
the owning library and update its handoff. 08B receives the combined capability.

## 1. Source roots, recorded playset and all-candidate search

Searches are not limited to a playset. Callers can select source directories
directly, including directories outside the selected Run's playset. Playset
membership is an optional selection/provenance aid, not a mandatory search
boundary. Explicit-directory searches do not require captured playset data.
Diagnostic searches and history selection likewise do not require matching
playsets; retain 08A.1's package and chronology rules.

Provide reusable functions to address a Run's stored playset and search its
accessible member roots, including recorded base-game and DLC entries. Preserve
load order, null fields, repeats and member identity. Use recorded paths; do not
re-extract debug logs or consult today's descriptors to reconstruct the playset.
Missing playset data remains unavailable, not evidence of an unmodded game.

Search must support:

- Selecting members by their available identifiers/names/paths.
- Selecting explicit source directories independently of playset membership.
- Directory scopes, optional recursion, extension and include/exclude glob filters
  (for example all `common/` descendants, or only `*.yml`).
- Exact and partial filename/relative-path matching, plus filename/path globs.
- Literal content search within the selected files, returning matching files and
  numbered matching lines. Reuse case controls and diagnostic-record filter grouping where
  useful; do not add a general expression engine.
- Every matching candidate across all selected members, in recorded member order
  and stable relative-path order within a member. For explicitly supplied roots
  outside the playset, retain the caller's root order. Never stop at the first match.

Evaluate grouped source-content conditions at file level. If `XYZ` occurs on
line 10 and `ABC` on line 40, `contains XYZ AND contains ABC` matches that file.
`not_contains` is true only when the forbidden text is absent throughout the
file; combine these predicates using the requested AND/OR groups. Return the
numbered lines satisfying positive conditions in qualifying files. An
exclusion-only search may return qualifying files without positive matching lines.

Use a path reference's supplied relative directory when present. Basename search
is an explicit broader mode, not a silent fallback. Reuse an in-memory inventory
and file reads within an investigation; preserve repeated member associations
even when the same physical root is scanned once. Do not add a persistent index,
queue or resident indexing process without demonstrating an actual unmet need.

Locate references using stored definitions, bindings, literals and placements;
inspect genuine examples to distinguish script references, supporting stack
locations and engine emitters. A numeric `LOCATOR` is not automatically a file,
and an emitter such as a C++ filename is not automatically a mod script. This
is reference lookup, not another parser/classifier or a semantic taxonomy.
If the stored evidence cannot identify a source, return that limitation.

A search operates within the caller-selected source roots and the requested
directory scope beneath it. If recursion is requested, recurse through
directories within that scope. Do not search filesystem
locations outside the selected search scope. This task does not commission
searches that follow or resolve filesystem links, or a special symlink, junction,
link-resolution or cross-root traversal policy. Retain only handling already
required by the existing implementation for ordinary path access.

Treat missing/unreadable roots, unsupported archive mounts and decoding failures
as explicit coverage limits. Do not call incomplete search proof of no match.
When source association is itself a filter, an unavailable required association
must not become "this diagnostic does not match." A filter naming a mod whose
root is unreadable returns an explicit inability-to-evaluate error. Retain known
partial matches where available, with incomplete filter coverage; do not present
them as a complete filtered result, silently remove the filter, or report an
exact zero. Apply the same rule to required explicit source roots/files.
This differs from optional source context, whose absence leaves the stored-data
report usable. Member lookup should expose readable-path availability so a future
GUI can disable unavailable choices and show, for example, `MOD XXX (Not present
on disk)`; CLI/API callers still receive the explicit filter error.
Do not expand into archive mounting or full game-state resolution. Search and
context remain read-only. The report records its generation time; do not record
individual source-file observation times. Candidate matches identify possible
source locations, never the winning mod or error owner, and current file contents
are not proof of their contents when the Run occurred.

## 2. Search-library and performance guidance

High-performance disk search is an initial requirement: the actual playset
contents are already known to be huge. Do not defer an efficient approach until
a basic implementation proves slow. Reuse existing project helpers and suitable
public libraries/tools rather than building a custom search engine.

- Prefer [`ripgrep`](https://github.com/BurntSushi/ripgrep) as the default bulk
  content-search engine, invoked from Python. Its
  [literal-search mode](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
  is `--fixed-strings`. Preserve the query's case and AND/OR semantics when
  batching and evaluate source-content groups at file level; reuse 08A.1's shared
  evaluator where applicable.
- Disable ambient ripgrep configuration with `--no-config` so user configuration
  cannot change query behavior. Consume structured output, preferably `--json`,
  rather than parsing formatted terminal output. Distinguish successful matches,
  successful no-match and search errors using the process outcome and diagnostics;
  retain partial matches together with coverage failures when a search errors.
  A missing executable must produce an actionable message identifying ripgrep
  and how to install it or configure its executable location.
- Build and reuse an in-memory filename/path inventory within an investigation.
  Resolve multiple diagnostic references against that inventory without
  repeatedly traversing the same directories. Preserve repeated playset-member
  associations even when a physical directory is inventoried once.
- Batch searches where possible. Avoid one subprocess, directory traversal or
  full content scan per diagnostic. Apply playset-member, directory, filename
  and extension filters before reading file contents.
  Playset-member filters are optional; explicit source-root searches use the same
  inventory, batching and filtering path without a membership restriction.
- Stream results and keep memory bounded. Keep the reusable inventory compact;
  do not accumulate unbounded file contents or subprocess output in memory.
  Preserve all matches, repeated member associations, recorded playset ordering
  and explicit coverage failures; bounded memory must not become a hidden
  result limit.
- Configure ripgrep's ignore rules, hidden-file handling and binary/encoding
  behavior explicitly so its defaults do not silently omit files required by
  the requested search scope. Preserve coverage errors from traversal and search
  rather than treating them as successful no-match results.
- Use standard-library helpers for supporting path/filter operations:
  [`os.walk`](https://docs.python.org/3.11/library/os.html#os.walk) with `onerror`
  for recursive inventory, `os.scandir` for a single directory, `pathlib` for
  path handling, and
  [`fnmatch.fnmatchcase`](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatchcase)
  or literal string operations with explicit case handling for filename filters.
  Where relative-path globs and exclusions need richer matching, use
  [`wcmatch.glob.globmatch`](https://facelessuser.github.io/wcmatch/glob/#globglobmatch)
  on the inventory rather than writing a glob engine. `fnmatch` does not treat
  `/` specially; choose the appropriate helper for filename versus path patterns.

Verify performance on a representative large real playset, covering filename
lookup, content search and an investigation with many diagnostic references.
Report timings and scope, including the playset/files searched and reference
count, and distinguish inventory construction from reused-inventory lookup.
Do not invent an arbitrary performance threshold.
Verify the actual Python-to-ripgrep invocation on Windows, including paths with
spaces, structured-output consumption and handling of matches, no-match and
errors. Installation instructions alone do not establish that invocation works.

Document the selected dependency/version, license and Windows installation or
distribution requirements in the handoff. Ripgrep supports Windows and is
MIT/Unlicense dual-licensed; it is an executable invoked by Python, not a Python
import. `wcmatch` is [MIT-licensed](https://facelessuser.github.io/wcmatch/about/license/);
if used, select a release supported by the project's Python version and declare
it as a normal dependency. Preserve the search-scope, ordinary path-access and
read-only requirements above. This does not commission persistent indexing,
a resident service, additional workers or multiple interchangeable search backends.

## 3. Excerpts and consumer contract

Provide excerpt data for each candidate with a usable referenced line: that
line plus ten lines above and below, clipped to file boundaries, with line
numbers and the target identified. Missing/out-of-range line information is
explicit; do not guess a replacement location. Return data that 08B can reuse
and link in an appendix without reimplementing lookup or excerpt extraction.

The combined analysis result uses 08A.1 for Run/package metadata; effective query; counts
and rollups; stored diagnostic text/typed values; review counts/references;
comparison evidence/notability; and chronology exclusions. This task adds candidate
provenance/coverage and optional excerpts. SQL-derived results remain usable when source context
is unavailable and after raw captures or model packages are unavailable.

## Verification and delivery

Derive checks from this prompt. Use genuine retained CK3 inputs and disposable
storage for integration; do not fabricate diagnostic records, modify evidence
to manufacture a history, or require five eligible production Runs. Pure scalar
checks are appropriate for filter logic, chronology/exclusions and threshold math;
distinguish those from genuine-data integration evidence.

Demonstrate:

- Public handler reads drive investigations; analysis/search do not occupy the
  database worker. SQL rendering requires neither raw logs nor executable models.
- Scoped search returns all available matching candidates in recorded order;
  coverage gaps and excerpt boundaries are explicit. Use real source contents.
- Explicit source roots outside a playset are searchable. File-level grouped
  conditions match positive terms on different lines; negative conditions apply
  across the file and exclusion-only queries can return files without match lines.
- Unavailable required source associations produce an explicit filter-evaluation
  error with any known partial matches and coverage failures, not false non-matches
  or an exact zero. Optional unavailable context leaves stored analysis usable.
- The Windows ripgrep invocation disables ambient configuration, consumes
  structured output, distinguishes matches/no-match/errors, preserves partial
  results on error and reports a missing executable actionably.
- The representative large-playset performance check covers filename lookup,
  content search and many diagnostic references, with timings/scope reported.
  Inventory reuse, batched searches and bounded streaming preserve all matches
  and coverage failures without per-diagnostic traversals or full scans.
- Missing sources/playset leave stored analysis usable; ordinary request errors
  are not converted into empty successful reads.

- Mod/member, source-file, template and exact-record selectors compose correctly
  through 08A.1's query engine; candidate associations do not inflate occurrence
  or distinct-record totals or change its history/notability rules.

Implement in the owning library components, use 07E logging helpers, and run
focused checks plus `tools/check_runtime_logging.py`, isolated imports and
`pip check` with the project venv. Report any genuine-data case not exercised.
Do not expand into audits, reconstruction, Run replacement, source-change history,
repair tracking, cross-package comparisons, GUI work or new storage schemas.

Deliver `docs/TASK08A_2_SOURCE_SEARCH_HANDOFF.md` with actual public
signatures, query/result examples, search/candidate/excerpt semantics, the
integration with 08A.1, a concrete 08B consumer example, changed files, checks
actually run and remaining limitations.
Update current status/handoff and the reporting decision ledger. Keep generated
reports, databases and verification artifacts outside Git. Finish implementation
and the handoff; do not stop at a design proposal.
