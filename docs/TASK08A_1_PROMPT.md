# Task 08A.1 Prompt — Diagnostic Record Search and Analysis

## Assignment

You are the Reporting and Analysis team. Implement the reusable library
capabilities for diagnostic-record searching/filtering, Run selection, exact
recurrence and notability. Task 08A.2 adds playset/source-file search and Task
08B builds the reports and CLI on both deliveries. Read all three prompts before
choosing the public interfaces; execute 08A.1 here.

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

08A.1 owns the structured investigation query and SQL-derived result, including
filters, exact identity, template-text matching, rollups, chronology and history.
08A.2 owns stored source-reference extraction, optional playset member selection,
explicit source-root selection, disk
search, candidate associations and excerpts, including the integration needed
for member/source-candidate filters in the shared investigation query.

Define that small query/result boundary in this task. Deliver the SQL-only
capabilities without waiting for disk search; document which source-dependent
filters require 08A.2. Do not implement a temporary search engine or treat a
not-yet-implemented candidate filter as a successful empty result. 08A.2 will
complete and verify composition with the query engine before 08B consumes it.

## 1. Structured investigations

Provide plain, documented query and result objects independent of CLI/HTML/UI.
Support these composable filters without a general query language:

- Scope: all stored diagnostics, emitter/source family, referenced file/path,
  or candidate association with selected source roots/files or playset members
  (including source mods). Playset membership is not a mandatory search limit.
  Support investigation of selected mods, selected source files, and specific
  diagnostic records; these selectors can be used independently or composed.
- Refinement: match status, one or more error templates, exact diagnostic identity using the
  existing contract, typed binding such as a particular `KEY`,
  occurrence count, and newly observed exact diagnostics.
- Search diagnostic records with multiple literal `contains`/`not_contains` conditions, combined in
  explicit nested AND/OR groups. Ignore case by default, with an explicit
  case-sensitive option. Search diagnostic content rendered from stored definitions/values.

Filter diagnostic records by the matched template reference already stored with
each record. Allow selection of one or more template references with OR semantics:
a record qualifies if its matched template is any of those selected. Each record
matches exactly one template; do not offer AND between template references.
This does not require searching model files or performing another matching pass.

Error-template selection supports exact stored template references, exact
template-text matching, and partial template-text matching. Support multiple
literal template `contains`/`not_contains` conditions using the same explicit
AND/OR grouping and case controls as diagnostic-record content filters. For example, a caller can
request diagnostic records whose error templates contain `XYZ`, or contain both
`XYZ` and `ABC`. Match the stored template text, including its literal and
placeholder text, independently of the rendered diagnostic message and binding
values. A token present only in a bound value does not satisfy a template-text
condition. Literal partial matching does not require fuzzy matching or a new
expression language. Records sharing a template remain distinct under the
existing full diagnostic identity.

Occurrence-count refinements apply to the count for the selected Run ID unless
a particular analytical operation explicitly states otherwise. Historical
comparison entries absent from that Run have a selected-Run count of zero.

Return the effective filters and enough information to describe their meaning,
including search coverage. Keep scope, refinement, optional analytics and display
limits distinguishable. Define how empty/invalid groups are handled; reject
invalid queries clearly. Do not use Python `eval` or accept arbitrary SQL.
Use a small evaluator unless an existing dependency materially simplifies it.

Reuse existing project helpers and suitable public libraries before writing
equivalents. Literal template/diagnostic-record filtering can use Python's built-in string
containment and [`str.casefold()`](https://docs.python.org/3/library/stdtypes.html#str.casefold),
with one shared evaluator for the structured AND/OR groups. Template-text matching
belongs in 08A.1 and its 08B consumer; it does not require a separate 08C task.
Use [`statistics.median`](https://docs.python.org/3/library/statistics.html#statistics.median)
for the existing baseline calculation. Reuse existing query validation conventions.
Choose APIs supported by the project's Python version. Document actual reuse and
justify any added dependency in the handoff; library choices must preserve the
handler, identity and evidence contracts rather than introduce another data path.

Return exact occurrence totals and distinct-record counts before display limits.
Support file/emitter rollups for hotspots without redefining diagnostic identity.
A diagnostic with several candidate files remains one diagnostic: expose the
overlap, and never sum overlapping candidate buckets into a supposedly unique
total. Include both template and provisional records unless explicitly filtered.

## 2. Run selection and exact history

Select reporting Runs within one explicit processing `package_id` from stored
lineage. This identifies a parser/matcher/model package, not a game mod. Package
files and learner imports are unnecessary for reads and rendering.

Order eligible Runs only by `run["facts"]["error_log_source_modified_at"]`.
This is the timestamp when CK3 wrote the original source `error.log` to disk at
the end of the gaming session. Use the stored timestamp normally. Distinct CK3
sessions are not expected to finish within fractions of a second of one another;
exact nanosecond preservation is not a product requirement. Do not introduce
special nanosecond-ordering machinery solely for reporting.
Do not substitute capture, processing or process-start time or backfill old Runs.
Missing/unusable timestamps exclude Runs from this chronology and are reported
as exclusions. A directly selected ineligible Run gets a clear explanation.

Within the selected processing package, distinct Run IDs sharing the same stored
source timestamp are suspicious data, not ordinary chronological ties. Before
selecting chronological neighbors or applying pagination, exclude every Run in
each such group from time-series/ordinal reporting. Report the excluded Run IDs,
shared timestamps and reason; suggest inspecting duplicated session data or
overwritten/corrupted timestamps. Do not force ordinality with Run IDs, capture
time, ingestion time or another fallback. Do not deliberately round timestamps
to create duplicate groups. If the explicitly selected Run belongs to such a
group, fail report generation and explain the failure to the caller. Diagnostic
filters and display limits must not hide a duplicate or restore its eligibility.

`latest` means the latest eligible Run in the explicitly selected processing
package under this chronology, after missing/unusable and duplicate-timestamp
exclusions. If none remains, report that no eligible Run is available.

Repository `list_runs`/`latest_run` currently use processing time. Build the
reporting order explicitly; do not take their first five results or silently
change those existing APIs. Determine eligibility/order before pagination.

For a selected eligible Run, obtain up to five preceding and five subsequent
eligible Runs in the same package. Ignore playset differences for selection.
Show actual window sizes and the Run IDs/timestamps used. Fewer than five is
normal; no history means no baseline, not a zero baseline.

Expose an optional recent-window control for investigations such as "how has
this evolved over the last five Runs?" A trailing window of five means the
selected Run plus up to four preceding eligible Runs in the same package, with
no subsequent Runs. For `latest`, this is the latest five eligible Runs. Keep the
existing five-before/five-after default when no override is requested. Return
per-Run occurrence totals and distinct-record counts for the effective filters,
alongside exact-identity counts, and disclose the window requested and obtained.
Any preceding baseline uses only successfully read predecessors in the chosen
window; keep the existing novelty/notability formulas and evidence rules.

Recurrence follows full existing template/literal/layout/binding identity,
scoped to its stored definition. Reuse contract equality data; a digest alone
is not proof of equality. Do not use Run-local row IDs, fuzzy matching, normalized
messages or template-only equality. Different binding values remain distinct.

For each investigated identity, provide its selected count, window counts,
number of preceding/subsequent Runs where observed, and preceding-count median.
Count an absent record as zero only after successfully reading that eligible
Run. Missing/failed reads are unavailable evidence, not absence; expose an
incomplete comparison rather than claiming disappearance or novelty.

Allow comparisons to include identities observed in the preceding window but
absent in the selected Run. These are historical comparison entries with a
selected count of zero, not invented stored records. Preserve their originating
Run/definition references. Apply the investigation's filters consistently to
these entries; occurrence refinements use the selected count unless explicitly
described otherwise. Do not filter out zero counts before disappearance analysis.

## 3. Notability

Compare selected count `C` with median `B` of the available preceding window:

| Baseline | Notable increase | Notable decrease |
|---|---|---|
| `0 < B < 10` | `C >= 10 * B` | `C == 0` |
| `10 <= B < 200` | `C - B >= 100` | `C == 0` |
| `B >= 200` | `C >= 1.6 * B` | `C <= 0.4 * B` |

Use inclusive boundaries and retain fractional medians. With preceding history,
label an identity newly observed in this window only if every preceding count
is zero and its selected count is positive. A zero median alone is insufficient.
For a positive count above a zero median with earlier observations, describe
that fact without an infinite percentage or an invented notability threshold.
Without history, novelty/notability are unavailable. Subsequent counts show
trajectory; no separate future-window notability formula is commissioned.

These are frequency observations, not severity, causation, or proof of repair.

## 4. Consumer contract

The SQL-derived analysis result must supply Run/package metadata; effective
query; counts and rollups; stored diagnostic text/typed values; review
counts/references; comparison evidence/notability; and chronology exclusions.
08A.2 adds candidate provenance/coverage and optional excerpts. SQL-derived
results remain usable when source context is unavailable and after raw captures
or model packages are unavailable.

Support explicit diagnostic selectors supplied by the separate syntax-identification
task, using the same template/binding/diagnostic-record content filters. Do not invent a syntax
catalog or cascade inference. If its handoff is not yet available, deliver and
document this selector interface; 08B will state the missing preset dependency.

## Verification and delivery

Derive checks from this prompt. Use genuine retained CK3 inputs and disposable
storage for integration; do not fabricate diagnostic records, modify evidence
to manufacture a history, or require five eligible production Runs. Pure scalar
checks are appropriate for filter logic, chronology/exclusions and threshold math;
distinguish those from genuine-data integration evidence.

Demonstrate:

- Public handler reads drive investigations; analysis/search do not occupy the
  database worker. SQL rendering requires neither raw logs nor executable models.
- Package/timestamp selection, exclusions and short/absent history follow the
  contract; existing repository processing-time order cannot leak into reports.
  Duplicate-timestamp groups are wholly excluded from chronology and disclosed;
  an explicitly selected member fails clearly, and `latest` uses eligible Runs.
- Exact identity preserves value differences; zero median, disappearance and
  boundary/fractional counts follow the stated rules without false novelty.
- Combined include/exclude filters, rollups and display limits preserve totals.
  One or more template references selected with OR filter by each record's stored
  matched template; template and exact-record selectors compose correctly. 08A.2 completes
  verification of mod/member and source-candidate filter composition;
  partial template matching searches template text rather than bound values.
  A trailing five-Run investigation includes the selected Run and up to four
  eligible predecessors, with per-Run filtered totals and honest missing evidence.
- Ordinary request errors are not converted into empty successful reads.

Implement in the owning library components, use 07E logging helpers, and run
focused checks plus `tools/check_runtime_logging.py`, isolated imports and
`pip check` with the project venv. Report any genuine-data case not exercised.
Do not expand into audits, reconstruction, Run replacement, source-change history,
repair tracking, cross-package comparisons, GUI work or new storage schemas.

Deliver `docs/TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md` with actual public
signatures, query/result examples, identity semantics, the receiving boundary
for 08A.2, a concrete 08B consumer example, changed files, checks actually run
and remaining limitations.
Update current status/handoff and the reporting decision ledger. Keep generated
reports, databases and verification artifacts outside Git. Finish implementation
and the handoff; do not stop at a design proposal.
