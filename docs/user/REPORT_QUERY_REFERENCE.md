# Report queries and results

Start with the report's question, selected Run, totals and coverage. Occurrences
measure repetition; records distinguish complete diagnostic identities. Use the
[everyday investigation workflow](WORKFLOWS.md#find-a-run-and-investigate-diagnostics)
for a first report. This reference helps you narrow that investigation with
structured filters and interpret the resulting history and source context.

Application 0.0.3. Supply UTF-8 JSON using `report --query PATH`; a BOM is accepted.
Unknown fields and wrong types are rejected. These are structured filters,
not SQL or expressions. A query is read on each invocation. Relative query-file
arguments resolve from the invocation directory, not the settings directory.

## Sections and combination rules

| Top-level field | Meaning / omitted behavior |
|---|---|
| `scope` | Object of starting source/emitter restrictions; omitted unrestricted. |
| `refinement` | Object of record conditions inside that scope; omitted unrestricted. |
| `analytics` | History controls below; history and previously observed entries enabled by default. |
| `display` | Detail bounds; CLI defaults 50 current/per-Run and 20 historical. Does not limit total computation. |
| `purpose` | String describing the investigation. Empty/omitted receives preset/custom description. |

Fields in an object combine with AND. Lists of emitters, statuses, templates,
identities and compound selectors combine with OR within that field. Binding
predicates combine with AND, each matching some binding. `refinement.all` is
one additional list of conditions ANDed with ordinary refinement; its entries
have the same refinement fields except another `all`. Nonempty selector lists
are required when supplied. Omit a field to leave it unrestricted.

Presets add their own conditions; a refinement never erases them. Valid opposing
filters can yield a successful empty report. `hotspots` requires a stored source
reference; `frequent` ranks exact records by occurrences; `new` requires newness
within the comparison window; `symbol` requires template, template-text or typed
binding input; `syntax` uses nine verified selectors restricted to package
`68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`.

## Literal text conditions

```json
{"and": [
  {"contains": "failed context switch"},
  {"or": [{"contains": "culture"}, {"contains": "faith"}]},
  {"not_contains": "effect", "case_sensitive": false}
]}
```

A leaf has exactly one nonempty `contains` or `not_contains` string plus optional
boolean `case_sensitive` (false default). Matching is literal, casefolded by
default, not regex or word-token syntax. A group has exactly `and` or `or` and a
nonempty list of child expressions. Source-content absence requires complete
coverage; an unreadable scope does not establish a negative match.

## Scope and record refinements

`scope` accepts `source_families` (nonempty string list of exact stored emitter
families), `has_source_reference` (boolean), and `source` (selection object below).

| Refinement field | Value and interpretation |
|---|---|
| `source_families` | Nonempty exact emitter-name string list. |
| `match_status` | Nonempty list containing `template` and/or `provisional`; unresolved review data is separate. |
| `message` | Text condition over the whole rendered stored diagnostic, including bound values. |
| `template_text` | Text condition over stored body-template text alone; bound values do not satisfy it. |
| `template_exact` | Nonempty list of exact case-sensitive body-template strings. |
| `templates` | Nonempty list of objects: required string `template_id`, optional exact string `model_revision`, `contract_version`. |
| `identities` | Nonempty list of complete returned identities, including `definition` and full contract `equality`. Copy from report JSON; a digest alone is insufficient. |
| `bindings` | Nonempty list of predicates with required string `type` and exact `value`; optional `region`, `slot_id`, boolean `present` (true default). Present value is a string; absent uses `present:false,value:null`. |
| `selectors` | Nonempty OR list of compound objects containing any fields above. Other refinement fields still AND with this result. |
| `occurrences` | Object with optional nonnegative integer `min`, `max` for the selected Run count. Historical-only entries have zero selected count. |
| `newly_observed` | Boolean; requires history. New means absent from successfully read included predecessors, not globally first-ever. |
| `has_source_reference` | Boolean testing stored identifiable references, not current disk existence. |
| `all` | Nonempty list of additional refinement conditions, one level only. |

Complete identity structure is `definition:{template_id,model_revision,contract_version}`
and `equality:{template_id,regions}`. Each region supplies `name`, nonempty
`layout`, `component_index` (nonnegative integer or null), and `bindings`.
Identity bindings contain `slot_id`, `type`, `value`, `present`; absent values
are null. Preserve this returned contract structure exactly rather than
manufacturing identities from displayed messages.

Save as `D:\Queries\message.json`:

```json
{
  "purpose": "Find failed context switches in this Run",
  "refinement": {"message": {"contains": "failed context switch"}},
  "analytics": {"history": false}
}
```

Use `--custom --query 'D:\Queries\message.json'`. For `--preset symbol`, save
this genuine stored-template selector as `D:\Queries\symbol.json`; template
availability depends on the Run's package, so a nonmatching Run can return empty:

```json
{"refinement":{"templates":[{"template_id":"0b2804538785c71278ea37e7"}]}}
```

## History and display

| Field | Type / default / effect |
|---|---|
| `analytics.history` | Boolean, true default. Default window includes up to five preceding and five subsequent eligible same-package Runs. |
| `analytics.trailing_runs` | Integer >=1. Total requested trailing window size, including selected Run and up to N-1 predecessors; requested positions and missing coverage remain visible. |
| `analytics.include_absent` | Boolean, default follows history; show separately previously observed records absent in the selected Run. |
| `display.limit` | Nonnegative integer or null. Null/omitted becomes 50 in CLI; `--limit` overrides. |
| `display.historical_limit` | Nonnegative integer or null. Null/omitted becomes 20 in CLI; `--historical-limit` overrides. |

`history:false` conflicts with trailing window, newness, or explicitly enabled
`include_absent`. `--no-history` disables history and absent entries but rejects
trailing/newness requests. Missing or failed Run reads are disclosed; successful
absence is zero, unavailable counts are null. Observation fractions use successful
reads on that side of the selected Run. A selected-only window can label positive
identities new in that window. It does not establish a fix, cause or regression.

Chronology uses the recorded source error-log modification timestamp. Ordinary
Run listing includes same-package Runs without that timestamp, in labelled Run-ID
order. A named Run can be reported without time placement; history/novelty then
remain unavailable. `latest` requires usable source chronology. Processing time
is never substituted for missing source time.

## Source selection JSON

These fields can be used inside required `scope.source` or, except `resolution`,
in the optional object read by `--source-context`. The selection cannot be empty
when explicitly supplied as `scope.source`. Lists must be nonempty. Fields AND;
alternatives within a list OR. Optional context enriches the report; required
source predicates determine which records qualify. Required fields override
same-named context fields. CLI context roots/directories/recursion override the
optional context file before required filters are composed.

| Field | Value, default and meaning |
|---|---|
| `roots` | List of absolute physical directory strings. Otherwise use each Run's recorded playset roots. Preserve supplied order; outside-playset roots have no recorded load order. |
| `members` | List of objects selecting recorded members. Optional exact `name`, `path`, `root_ID`, `stable_id`, `descriptor_path` string/null and nonnegative `load_order`; at least one field. Fields AND, objects OR. |
| `directories` | Relative directory strings beneath each root; default root itself. No `..`, drive prefix or absolute escape. Optional single leading slash means game-relative. |
| `recursive` | Boolean, true default; false enumerates only selected directories. |
| `files` | Exact physical absolute paths or game-relative paths across selected roots. |
| `referenced_paths` | Stored reference strings; path filtering does not require the referenced file to exist today. |
| `reference_mode` | `relative` default or `basename`; basename broadens association and can find multiple files. |
| `filename` | Object with `exact` string list and/or `text` condition, applied to basename. |
| `relative_path` | Object with `exact` string list and/or `text` condition. Explicit exact game-relative paths allow a single leading slash and normalize separators. |
| `extensions` | String list such as `["txt",".yml"]`; suffix filter. |
| `filename_globs` | String list of filename wildcard patterns. |
| `path_globs`, `include` | String lists of relative-path wildcard patterns; each supplied field must match. |
| `exclude` | String list of relative-path wildcard patterns; any match excludes. |
| `case_sensitive` | Boolean, false default for path/exact/glob comparisons. Text leaves have their own case setting. |
| `content` | File-level grouped text condition; requires current file reads and configured/explicit ripgrep. |
| `resolution` | Required diagnostic filter only: `resolved` or `unresolved` in `scope.source`. Tests current resolution; pathless records excluded, incomplete coverage remains unknown. |

Example stored-path investigation:

```json
{
  "scope": {"source": {"relative_path": {
    "exact": ["common/on_action/sea_minority_on_actions.txt"]
  }}},
  "analytics": {"history": false}
}
```

Path-only filters select stored references without requiring current existence.
Records with no path are complete emissions for which source context is not
applicable. Required unresolved/resolved filtering is different from ordinary
stored-path selection. Search narrows roots/directories before traversal; known
relative paths narrow parent-directory enumeration. Unscoped searches inventory
whole selected roots. File counts describe paths examined, not errors found.

## Reading report JSON

| Result field | Interpretation |
|---|---|
| `status` | `completed` for success, including empty output; failure states are described in [CLI exit behavior](CLI_REFERENCE.md#report). |
| `run`, `package_id` | Actual selected stored Run and lineage; capture/processing times have separate meanings. |
| `effective_query`, `filter_meaning` | Applied validated predicates and their meaning after preset/CLI composition. |
| `totals` | Occurrences, distinct records and historical entries before display truncation. |
| `records`, `historical` | Selected and previously observed record views, exact identities, native messages, classification, bound values, template/literal provenance and per-Run counts. |
| `window`, `chronology_exclusions` | Included/requested positions and unavailable or ineligible chronology; do not fill gaps with invented Runs. |
| `rollups` | Separate emitter, reference and candidate associations; association is not general causal blame. |
| `review` | Stored review counts/references/availability; no raw review payload reconstruction. |
| `coverage` | Completed versus unavailable reads/source work and disclosure of partial evidence. |
| `presentation` | Format context, generation time, preset and optional source selection. Generation time is not historical file time. |
| `explanation` | Plain-language question, result interpretation and limitations shared by output formats. |

For single-file/line references, the last matching recorded member in load order
identifies the file/line source under this product's rule. Keep other candidates
and coverage visible. Current text is not proof of historical content. Verbose
excerpts are referenced line ±10, clipped to current file bounds; missing or
out-of-range text remains explained.

JSON preserves native text with reversible surrogate escapes for undecodable
bytes. Consumers must preserve those escapes if they need exact text fidelity.
Text/HTML are presentation views of the same analytical result. Frequency is not
severity, and an empty result is not proof that CK3 produced no unresolved evidence.

JSON keeps complete rollups and identity maps even with a low detail limit, so
large JSON output is expected. Text/HTML also bound ranking tables. Offline HTML
needs no server, JavaScript or remote assets; main/appendix writes are not atomic
as a pair. Source content search can create temporary decoding files.

`totals` describes the selected Run; `window.totals` aggregates successful included
reads and distinct full identities across them. Historical entries come from
predecessors, not successors. Reference/candidate buckets can overlap; inspect
`bucket_totals_are_additive` before summing. Provisional/template statuses are
assignments, not severity or numeric confidence. Successful status does not prove
complete optional history/source coverage: inspect `window.complete`,
`coverage.comparison_errors` and `coverage.comparison_unavailable`.

Source resolution statuses distinguish resolved, unresolved, outside_scope,
not_searched and incomplete. Required resolution means at least one selected
reference has that result. Content predicates evaluate a whole file, so AND
terms may occur on different lines. Member/root/content/resolution restrictions
need current-source evaluation; incomplete required work returns exit 3.
Optional context failures leave stored membership intact. For source attribution,
missing lines, unavailable load order or ties leave it unassigned with a reason;
content filtering never promotes an earlier copy to the assigned last member.

[Manual contents](README.md)
