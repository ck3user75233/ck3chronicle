# Task 08B — Reports and Investigation Experience

## Current owner clarifications — 2026-10-04

Ordinary phrase/token search encompasses complete diagnostic messages: template
literals and populated slot values together. Show the stored origin of matches
and the template already assigned to each diagnostic. Templates do not produce
errors. No special template-discovery query or slot-only search options are needed.
The contrived bound-phrase-versus-template empty-set example is withdrawn.

Display requested Run -5…+5 positions with unavailable positions labelled, rather
than requiring eleven simultaneous genuine Runs for verification. Empty diagnostic
results and missing Run positions are normal outcomes. Distinguish actual handler
operation/transport errors from those outcomes. Source decoding/search errors
refer to current files or the search process, not already-decoded SQL records.
Verify independence from logs/models through observed I/O without deleting inputs.
These clarifications supersede conflicting earlier example or acceptance wording;
the current delivery/evidence is in [08B's handoff](TASK08B_REPORTING_HANDOFF.md).

## Assignment and deliverables

You are the Reporting and Analysis team. Deliver the CLI and report experience
using the completed 08A.1 diagnostic-query/history and 08A.2 source-search services.
Their integration, known-path source-scope repair and current multi-Run receiving
changes are delivered. Receive those interfaces, then implement:

- **Root CLI:** `runs` and `report`, using arguments for presets and query controls.
- **Five presets:** script/file hotspots, frequent diagnostics, syntax-related
  diagnostics, newly observed diagnostics, and symbol/template investigation.
- **Report formats:** readable text, structured JSON and offline HTML, with source
  candidates for every displayed diagnostic and a linked verbose source appendix.
- **Queries and examples:** composable mod/member, file, exact-record, template,
  message and typed-binding selection, plus the worked five-Run investigation below.
- **Consumer verification:** genuine stored CK3 records and current source files,
  exercised through the actual root CLI with disposable storage.
- **Handoff and documentation:** `docs/TASK08B_REPORTING_HANDOFF.md`, README usage,
  and the existing current status, handoff and reporting ledger.

The delivery consists of ordinary CLI operations and exported report files.
Keep analytical data independent of presentation templates so later adapters can
reuse the same services.

## Read and receive

Checkout: `C:/Users/nateb/Documents/ck3chronicle`.

Read `AGENTS.md`, applicable nested instructions, `docs/DEVELOPMENT_ENVIRONMENT.md`,
`docs/BANNED_IDEAS.md`, and the opening current sections of `docs/PROJECT_PLAN.md`,
`docs/PROJECT_STATUS.md` and `docs/CURRENT_HANDOFF.md`. Then receive:

- [Reporting decisions](TASK08_SCOPE_REVIEW.md), [08A.1 scope](TASK08A_1_PROMPT.md)
  and [08A.2 scope](TASK08A_2_PROMPT.md).
- [08A.1 diagnostic-query delivery](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md),
  [08A.2 source-search delivery](TASK08A_2_SOURCE_SEARCH_HANDOFF.md), and their
  actual public implementations.
- [Latest multi-Run and scoped-traversal delivery](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md)
  and the current decision in [08B receiving review](TASK08B_RECEIVING_REVIEW.md).
  Use their current receiving sections; earlier review sections are historical.
- [Syntax selectors](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff):
  package scope, nine selectors, exact REASON condition, genuine examples and exclusions.
- [07D handler APIs](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md),
  [07E logging](TASK07E_RUNTIME_LOGGING_HANDOFF.md), and
  [source timestamp delivery](WATCHER_SOURCE_MTIME_HANDOFF.md).

The current history contract is actual counts, observation fractions and
included-window newness, as specified below. This owner correction supersedes
conflicting analytics requirements in earlier Task 08 documents.

## Ownership and working boundaries

- **08A.1 owns** Run selection, query/filter evaluation, stored diagnostic rendering,
  exact identity, history and newness.
- **08A.2 owns** source-reference extraction, search, candidate-filter integration,
  excerpts, ordering and coverage.
- **08B owns** CLI registration, preset definitions, report presentation, consumer
  verification and handoff. Resolve bounded consumer gaps in the owning library
  and update its handoff; report material scope changes before expanding them.
- **Database access:** use `HandlerClient` for all runtime database access. Analysis
  and presentation execute outside the database worker.
- **Operations:** preserve unrelated work. Use disposable verification storage and
  keep live processes, production captures/databases, retained evidence and active
  package selection unchanged. Commits and pushes remain deferred for this task.
- **Architecture:** reuse the delivered query, source, handler and logging services.
  Changes beyond these consumer responsibilities require a separate commission.

## Public interfaces to use

- Construct `DiagnosticAnalysis(client, source_resolver=SourceSearch(client, ...))`
  from `ck3chronicle.reporting`, with `HandlerClient` as the client.
- Use public `list_runs` and `investigate(..., package_id=..., query=...)`;
  `InvestigationResult.to_dict()` supplies presentation data. The adapter may obtain
  a named Run's package through public `get_run` before calling `investigate`.
- Follow the delivered `InvestigationQuery` fields: `refinement.templates` (OR),
  `refinement.selectors` (OR of compound predicates), `refinement.message`
  (diagnostic-record content), `scope.source`, `analytics.trailing_runs`, and
  separate current/historical display limits.
- Use 08A.2's `context` for optional candidate context, `scope.source` for
  required source predicates, and `excerpts=True` for verbose data. Keep the
  library's stored-reference-only query capability SQL-only; reports request
  optional candidate context for displayed records through the source library.
- Handle the current `QueryError`, `ReadError`, `RunSelectionError` and
  `SourceEvaluationError` contracts. Present `SourceEvaluationError.partial` as
  incomplete source evidence and an inability to evaluate the required filter.

The delivered source repair selects roots/members before availability probes.
Directory and recursion scopes constrain traversal; exact files and stored
relative references narrow inventories to their parent directories within that
scope. Basename-only searches use the selected scope. Recorded-playset roots are
the default; explicitly selected outside-playset roots remain supported. Cache
reuse preserves this scope. Retain all candidates, repeated associations, ordering
and coverage errors. Display the effective scope; inventory construction is
available in `coverage.metrics.inventory_scopes`. Verify integration with genuine
scoped queries. Upstream counts, memory and timings are measurements, not acceptance
thresholds.

## CLI and query deliverables

Follow the existing root CLI argument and output conventions. Document the final
syntax and support:

- **`runs`:** configured/explicit database, explicit processing package, eligible
  Run listing in source-modification chronology, text/JSON, and pagination applied
  after eligibility and ordering. Disclose missing/unusable timestamps with
  their Run IDs and stored values.
- **`report`:** configured/explicit database, named Run or `latest`, named preset or explicit custom query path,
  structured query file, text/JSON/HTML, display limit and `--verbose` excerpts.
  HTML requires an explicit destination. Text/JSON default to stdout unless the
  root CLI has another established convention.
- **Package selection:** `--package-id`. A named Run's stored lineage may supply
  it; reject a conflicting supplied package. `latest` requires an explicit package
  and selects its latest eligible Run using 08A.1 chronology. Selection uses stored
  metadata, without loading a model.
- **Timestamp eligibility:** use 08A.1's original source-log modification chronology
  and missing/unusable timestamp exclusions. Explain when no eligible Run remains; excluded
  Runs remain outside chronological windows and neighbor lists.
- **Queries:** provide a concise JSON example with scope, refinement, grouped
  literal include/exclude clauses using AND/OR, and optional analytics. Use the
  existing validated structured-query model; arbitrary SQL/Python expressions
  remain unsupported. Report the actual effective filters alongside any prose purpose.
- **Selectors:** document mod/playset-member, source-file and exact diagnostic-record
  selection, independently and combined. Include exact template references, partial
  template text such as “contains XYZ” and “contains both XYZ and ABC,” typed bindings
  such as a specified `KEY`, and separate rendered-message filtering. Evaluate template
  text against the template and message text against rendered record content; bound
  values belong to the latter. Use the existing exact-identity selector.
- **Preset refinement:** the preset supplies the base investigation definition.
  A query may refine it with ordinary 08A.1 filters and analytics while retaining
  its defining condition. Document each condition and reject contradictory
  refinements clearly. A valid refinement that finds no matching records is a
  successful empty result, not a contradictory query. Custom investigations use
  the explicit non-preset path.
- **Result states:** give distinct messages for unknown/ineligible Runs, unavailable
  reads and successful empty results. Optional missing source context leaves a valid
  stored-data report readable. Unavailable evidence required by a source filter
  produces the library's evaluation error and clearly labelled partial matches.

### Worked investigation

Include a working query and report for script-system diagnostics whose rendered
messages contain “failed context switch” across a trailing window of five eligible
Runs ending at the selected Run or `latest`:

- Select script-system scope using stored emitter/source-family evidence.
- Show per-Run filtered totals, contributing exact diagnostics and all source candidates.
- Rank candidate files by matching occurrence and distinct-record counts. Keep
  emitter groupings distinct from referenced script paths and count overlapping
  associations separately from unique diagnostic totals.
- Explain the alternative query for templates containing that phrase.
- Describe file rankings as candidate associations, with ownership remaining unresolved.

## Report presets

Implement these over the same composable library services. Every preset supports
first-stage scope, further refinement and explicit analytics selection.

| Preset | Required investigation and presentation |
|---|---|
| Script/file hotspots | Occurrence and distinct-record concentration for script-referenced diagnostics, followed by contributing exact diagnostics and all candidate files; separate emitter groupings from referenced paths. |
| Frequent diagnostics | Exact records ranked by occurrence count within the chosen scope. |
| Syntax-related diagnostics | The syntax handoff's nine verified selectors, evidence description, package/model boundary and exclusions. Preserve the exact body/slot/type/REASON condition on the assignment-error branch and include both stored match statuses. An unsupported package makes this preset unavailable. |
| Newly observed diagnostics | Positive exact identities in the selected Run that are absent from every successfully read included predecessor. With no included predecessors, positive records are new within that window. Disclose the window and coverage. |
| Symbol/template investigation | Exact template references, exact/partial template text and grouped literal token conditions, and/or typed bindings, with optional message/source refinement. Preserve separate exact diagnostic identities. |

For every displayed record, attempt 08A.2 candidate lookup and show all applicable
candidates in library order. Distinguish:

- Complete search with no matching file on disk.
- Incomplete coverage from unavailable, unreadable, unsupported or out-of-coverage roots/files.
- Stored evidence that cannot identify a source reference.

Keep the diagnostic visible in all three cases. Mod/member and path scopes express
possible candidate association. Frequency rollups preserve exact identity.

Include recent-Run commentary by default, with an option to omit it. History-enabled
reports also show a bounded accompanying view of matching preceding-window identities
absent from the selected Run, using the library's historical entries. Label them
“previously observed,” keep their totals separate from selected-Run totals, and explain
the effect of an explicit positive occurrence filter on this view.

## Report content, history and layout

Lead with:

- Purpose and effective filters.
- Selected Run/package and original source-log modification timestamp.
- Report generation time and effective source scope.
- Filtered occurrence and distinct-diagnostic totals.
- Review-routed counts/references as coverage context, using existing stored information.

For each displayed diagnostic, show rendered stored text, relevant typed values,
template/provisional status, occurrence count, source references/candidates and a
compact history comment or panel.

Use the following history contract:

- Default comparison: up to five preceding and five subsequent eligible Runs,
  with actual counts, observation fractions and window-relative newness.
- Expose the library's recent-window control through the structured query. A
  trailing window of five contains the selected Run and up to four eligible predecessors.
- Use `history.counts`, `selected_count`, preceding/subsequent observed/read counts
  and fractions, and `newly_observed`, with 08A.1's same-package eligibility and chronology.
- Disclose missing/unusable timestamp exclusions and the actual available window size.
- Newness uses successfully read included predecessors. Unavailable comparisons
  remain disclosed coverage gaps; they do not veto window-relative newness.
  A selected-only window labels positive records new within that window and has
  an unavailable observation fraction. “New” is relative to the disclosed window.
- For each preceding/subsequent window, the observation fraction is observed
  successful reads divided by all successful reads in that window. A successfully
  read Run with the identity absent contributes zero. Failed/unavailable reads enter
  neither numerator nor denominator and appear separately. With no successful reads,
  the fraction is unavailable.
- Present observed counts, changes, newness and absence. Counts describe frequency;
  “not observed in this Run” describes absence. Severity, confirmed fixes and causal
  ownership remain unresolved by these data. No median-based notability or
  replacement statistical baseline/threshold is commissioned. Explain session-length and unassigned
  evidence limitations briefly, once where useful.

Use summary-to-detail navigation, clear headings, readable tables and restrained
visual emphasis, with labels that work independently of color. Bound the displayed
diagnostic set and disclose total matches and the display limit. Compute statistics
before limiting display. Count diagnostics independently of candidate associations;
show every candidate for displayed records, using expandable sections when helpful.
Choose visualizations for their investigative value.

## Source context and verbose appendix

- Use current readable source contents. Default roots come from the selected Run's
  recorded playset when available; expose 08A.2 explicit root/directory selection,
  including roots outside that playset.
- Show all candidates in recorded load order with member identity, recorded
  load-order number beside the mod name, and relative/physical paths. Preserve stored
  numbers. Outside-playset roots display recorded load order as unavailable.
- Record current-source timing once, as the report generation timestamp.
- Report unavailable roots and incomplete coverage. Treat matches and load order as
  current candidate evidence; historical contents and winning-file/ownership conclusions
  remain unresolved.
- Normal output shows candidates and available reference locations. `--verbose`
  adds a separate linked HTML appendix using 08A.2 excerpts: referenced line plus
  ten lines above/below, clipped to file boundaries, numbered and emphasized.
- Link each main-report reference to its appendix entry; repeated references may
  share entries. Explain unavailable and out-of-range excerpts.
- Generate offline HTML with packaged/local assets and working relative appendix
  links. Escape diagnostic text, filenames and source code as untrusted content.
- Text/JSON expose the same substantive results. Verbose JSON includes excerpts;
  verbose text may present the appendix sequentially with clear references.

Reuse existing CLI/rendering helpers and 08A.1/08A.2 capabilities. If a suitable HTML
renderer is absent, prefer [Jinja2](https://jinja.palletsprojects.com/en/stable/api/)
with HTML autoescaping and packaged templates. Declare/package any dependency
normally and document actual reuse and dependency choices in the handoff. Later
separately commissioned adapters or enhancements should consume these same services.

## Verification and acceptance evidence

Use genuine retained CK3 inputs, stored records through the public handler, current
source contents and disposable storage. Extend retained genuine-data checks with
focused real-data consumer checks. Report absent cases as unverified; synthetic
histories, mock clients and injected failures are outside reporting acceptance.
Distinguish source inspection, upstream evidence and checks actually executed by 08B.

Exercise representative reports through the root CLI and demonstrate:

- **Selection:** package restriction, source-timestamp order, `runs`/`latest`,
  missing/unusable timestamp exclusions and honest short/absent history.
- **Queries:** preset definitions and refinements, contradiction rejection, grouped
  message filters, mod/member and file scopes, exact-record selection, and exact/partial
  template selection distinct from bound-value matches.
- **Format agreement:** HTML/text/JSON agree on identities, counts, history and
  effective query. Display limits preserve totals and recurrence; historical absences
  retain their separate presentation.
- **Source presentation:** default context, all candidates, recorded order numbers,
  verbose links, line ranges and correctly escaped content.
- **Evidence states:** unavailable comparison reads remain outside fractions;
  required-source evaluation errors retain partial evidence; genuine request failures
  are reported as failures. Optional missing sources/playsets permit stored diagnostics
  to render, including when raw logs or model packages are unavailable.
- **Integration:** existing CLI operations and shared logging continue to work.
  Inspect representative rendered output and links; run relevant CLI/import checks
  and the 07E logging check with the project venv.

The current upstream handoff reports four eligible genuine Runs: 18 investigations /
359 comparisons and two single-Run checks under the current newness rule. The later
scope delivery reports 41 scope/candidate comparisons, four multi-Run source
investigations / 93 comparisons and nine genuine source tests. Receive these as
upstream evidence. Use its unchanged backup and linked reports for consumer checks.

Fourteen older missing-timestamp Runs remain excluded. Naturally failed reads,
unavailable roots, decoding/ripgrep failures and a full
five-before/five-after window remain unexercised. Preserve these evidence gaps unless
genuine cases are available. Available genuine windows suffice for delivery; report
their actual sizes. Report failed checks and proposed requirements beyond this assignment.

## Handoff checklist

Deliver `docs/TASK08B_REPORTING_HANDOFF.md` with:

- Final commands, presets, defining conditions and worked query examples.
- Supported filters and actual 08A.1/08A.2 interfaces reused.
- Generated-output examples, effective query/scope and verbose appendix behavior.
- Changed files, dependency choices and checks actually run.
- Concrete remaining limitations, receiving dependencies and unverified cases.

Update README usage and the existing current status/handoff/reporting ledger. Keep
generated evidence outside Git. Describe this as reporting delivery; full live
Trusted Run acceptance remains a separate milestone.
