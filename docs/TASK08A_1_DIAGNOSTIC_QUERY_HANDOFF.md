# Task 08A.1 — Diagnostic query and analysis delivery

Current genuine-history verification: [multi-Run receiving results](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md).
The October 3 owner correction removes the median-based comparison and novelty
unavailable-read veto. Newness uses actual included predecessors. The unchanged
backup has four eligible Runs and 14 excluded older Runs; 18 investigations / 359
real-data comparisons plus two single-Run checks passed. Template selections use
stored ingestion references; message searches include slot values. Naturally
unavailable reads and duplicate timestamps remain unexercised.

Delivered 2026-10-02 in `ck3chronicle.reporting`. This is the SQL-derived library
delivery, not reports/CLI, source search, or live Trusted Run acceptance.
08A.2 has now delivered the source boundary below; see
[its handoff](TASK08A_2_SOURCE_SEARCH_HANDOFF.md) for the combined 08B interface.

## Public interface

```python
from ck3chronicle.reporting import (
    InvestigationQuery, InvestigationResult, DiagnosticAnalysis,
    QueryError, ReadError, RunSelectionError,
    SourceEvaluationError, SourceResolver,
    chronology, exact_identity, identity_key, template_text,
    evaluate_text, frequency_observation, rollup,
)

InvestigationQuery(scope: dict = {}, refinement: dict = {},
                   analytics: dict = {}, display: dict = {}, purpose: str = '')
InvestigationQuery.from_dict(value: dict) -> InvestigationQuery
InvestigationQuery.to_dict() -> dict

DiagnosticAnalysis(client: HandlerClient, *, source_resolver: SourceResolver | None = None)
DiagnosticAnalysis.list_runs(package_id: str, *, offset: int = 0,
                             limit: int | None = None) -> dict
DiagnosticAnalysis.investigate(run: str, *, package_id: str,
                               query: InvestigationQuery | dict | None = None) -> InvestigationResult
InvestigationResult.to_dict() -> dict

chronology(runs: list[dict], package_id: str) -> dict
exact_identity(record: dict) -> dict
identity_key(record: dict) -> str
template_text(definition: dict) -> str
evaluate_text(text: str, expression: dict | None) -> bool
frequency_observation(selected: int, preceding: list[int | None],
                      subsequent: list[int | None] = ()) -> dict
rollup(entries: list[dict], associations: dict[str, list[str]]) -> dict
```

The constructor defaults shown above are explanatory; the implementation uses
dataclass default factories. `from_dict` and `to_dict` validate and copy inputs.
`evaluate_text` consumes an already validated predicate; validate it as part of
an `InvestigationQuery` (or use `reporting.query.validate_text`) before reuse.
The scalar chronology/statistics/rollup helpers do not perform reads.

Every runtime read uses `HandlerClient.submit`/`result`. The service submits
`list_runs` without limits, `get_run`, `read_diagnostics` and
`read_review_metadata`; it never opens SQLite, accesses a repository, reads raw
logs, imports an executable package, or changes worker operations. All rendering,
filtering, ordering and statistics run in the caller. Existing repository
processing-time APIs remain unchanged. No missing upstream operation was found.

The caller explicitly supplies `package_id`, including for named Runs. 08B may
infer that argument from a public `get_run` result before calling this API; it
must reject a conflicting supplied package. No package-selection file is consulted.

## Query rules and examples

Scope, refinement, analytics and display are distinct sections. Omitted filters
are unrestricted. Fields are ANDed. Lists of source families, matched-template
references, exact identities and `selectors` are ORed within their field.
Each `selectors` element is itself an AND of ordinary record predicates; this
supports the separately researched syntax selectors without a new catalog.
Binding predicates are ANDed: each must match at least one stored binding.
Different predicates may match different bindings.

```json
{
  "purpose": "Failed context switches in recent script-system diagnostics",
  "scope": {"source_families": ["jomini_script_system.cpp"]},
  "refinement": {
    "message": {
      "and": [
        {"contains": "failed context switch"},
        {"or": [{"contains": "trigger"}, {"contains": "effect"}]},
        {"not_contains": "this literal is excluded", "case_sensitive": true}
      ]
    },
    "occurrences": {"min": 1}
  },
  "analytics": {"trailing_runs": 5, "include_absent": true},
  "display": {"limit": 50, "historical_limit": 20}
}
```

The positive occurrence minimum in this example excludes historical zero-count
entries. Omit it to retain those entries. `purpose` is explanatory text only.
For templates containing the phrase, put the same expression under
`refinement.template_text` instead of `message`.

Supported record predicates (also accepted inside each `selectors` branch):

| Field | Meaning |
|---|---|
| `source_families: [str, ...]` | Exact stored emitter/source family, no inferred taxonomy. Also supported in scope. |
| `match_status: [str, ...]` | `template` and/or `provisional`; both included when omitted. |
| `templates: [{template_id, model_revision?, contract_version?}, ...]` | Any selected stored matched-template reference. No template AND operator or rematching. Omitted revision fields remain scoped by the selected package. |
| `identities: [exact_identity(record), ...]` | Any full definition-scoped contract equality selector. Digests and Run-local ordinals are not accepted selectors. |
| `bindings: [{type, value, present?, region?, slot_id?}, ...]` | Exact typed value/presence; default `present=true`. An absent binding requires `present=false, value=null`. Optional region/slot constrain that same binding. |
| `message` | Nested literal predicate over `contracts.render(definition, values)`. |
| `template_text` | Same predicate over `template_text(definition)` only. |
| `template_exact: [str, ...]` | OR of exact, case-sensitive template-text strings. |

Additional top-level refinement fields are `occurrences: {min?, max?}` and
`newly_observed: bool`. Occurrence boundaries are inclusive nonnegative integers
and **always refer to the selected Run**, including during per-Run summaries.
Newly observed means the complete preceding window, not first-ever occurrence.

Examples that compose with any scope or other refinement:

```python
# OR between stored matched-template references.
refinement = {'templates': [
    {'template_id': 'ca6575c8898718edafb168ca'},
    {'template_id': '575c64f8a3b6e211b735c3ba'},
]}
# Both literals in the template itself, independent of bindings.
refinement = {'template_text': {'and': [
    {'contains': 'XYZ'}, {'contains': 'ABC'}, {'not_contains': 'obsolete'},
]}}
# Exact diagnostic selected from a previous result, optionally combined with KEY.
refinement = {'identities': [result.records[0]['identity']],
              'bindings': [{'type': 'KEY', 'value': 'has_focus'}]}
```

Text leaves contain exactly one `contains` or `not_contains`, with optional
boolean `case_sensitive` (default false). `str.casefold()` supplies case-insensitive
matching. Groups contain exactly one nonempty `and` or `or` list. Empty literals,
empty selector lists, empty branches, ambiguous groups, unknown fields, bad types,
negative counts/limits and contradictory min/max are rejected with `QueryError`,
a `ValueError`. The unrequested 32-level nesting cap was removed during owner
review. No SQL, regex, Python
expression or `eval` is accepted. `display.limit=0` is valid; totals still exist.

Stored definitions have parts rather than a separate display string.
`template_text` concatenates the **body** definition's literal parts and `<TYPE>`
slot placeholders, preserving declared prefix/suffix. Finite literal choices
are represented as `{a|b}` in their stored order. All choices are definition text,
independent of an individual record's selected choice. Optional wrapper/support
definitions are returned as part of `stored_record.definition`, but are not the
body template searched by this field. Use the returned `template_text` for exact
text selectors. This needs no model file, matching pass, or new stored schema.

The syntax research handoff **is available**. Its nine OR branches can use
`selectors`, exact `templates` and `source_families`. Its assignment-error branch
additionally uses:

```python
{'templates': [{'template_id': '0b2804538785c71278ea37e7'}],
 'source_families': ['jomini_script_system.cpp'],
 'bindings': [{'region': 'body', 'slot_id': 's1', 'type': 'REASON',
               'value': "Trigger is simple assign, but used a symbol other than '=' in the middle"}]}
```

08B owns implementing the named preset and enforcing the research's package/model
boundary. This delivery supplies the selector interface, not a syntax catalog or
new findings. See `CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff`.

## Chronology and evidence

Eligibility is determined across **all** stored Runs in the explicit package,
before pagination or diagnostic filters. Only
`facts.error_log_source_modified_at` orders Runs. Missing, invalid or offsetless
timestamps are excluded with Run IDs and the stored value. No backfill, process
time, capture time or Run-ID fallback is used.

All members of each duplicate **stored timestamp string** group are excluded;
the exclusion includes the shared timestamp and guidance to inspect duplicated
session data or overwritten/corrupted timestamps. An explicitly selected member
raises `RunSelectionError` with `.exclusions`. `latest` chooses the latest remaining
eligible Run, or raises a clear no-eligible-Run error. `list_runs` returns newest
first, total eligible count and all package exclusions even on a one-item page.

Standard Python aware ISO `datetime` ordering is used. Original timestamp strings
are retained in every result and are used directly for duplicate grouping; they
are never rounded into duplicate groups. No special nanosecond chronology is
introduced. The producer's canonical UTC timestamp format is the receiving
contract; sub-microsecond distinctions between distinct sessions are not claimed.

Default history is up to five preceding and five subsequent eligible Runs,
regardless of playset differences. `analytics.trailing_runs=N` instead selects
the selected Run plus up to N-1 predecessors and no successors. `history=false`
reads only the selected Run; trailing/novelty options conflict with that setting.
`include_absent` defaults to the history setting.

Before reading diagnostics, the service checks that the listed Run still exists
with the same metadata because `read_diagnostics` alone returns an empty list for
unknown Runs. A required selected read/review failure raises `ReadError`.
Comparison failures are retained as unavailable evidence, with null counts and
error details. They contribute neither observations nor denominators. Newness
uses only successfully read predecessors included in the window, without an
unavailable-read veto. Admission errors and evicted results are failures. There is
no cross-request transactional snapshot; clients should rerun after a concurrent
Run change. No automatic retries, resubmissions or replacement machinery were added.

Exact recurrence uses `contracts.identity_data(values)`, scoped by
`model_revision`, `contract_version`, and `template_id` from the stored definition.
`identity_key` is the canonical JSON encoding of that full data, **not a hash**.
Full ordered bindings, presence, layouts, literal choices and supporting entries
participate. Provenance, timestamps, support status and Run-local row IDs do not.
The stored definition ID and ordinal remain origin references only.

Successfully read Runs contribute actual counts or zero when the identity is
absent. Following the owner's October 3 correction, newness means selected count
positive and no occurrence in any successfully read predecessor in this window.
It is a boolean relative to the included window, including a window with no
preceding observations. Earlier observations outside that window do not affect it.
`newly_observed` filtering uses this rule directly.

The median-based comparison was removed. History returns selected/window counts,
preceding/subsequent observed/read counts and fractions, `newly_observed`, and
comparison completeness. `preceding_median`, `baseline_available`, `notable`,
`positive_above_zero_median_with_prior_observation`, the obsolete novelty-unavailable
coverage list, and `QueryEvidenceError` were removed. No replacement notability
formula has been commissioned. Separate read-error/coverage evidence is retained;
it does not override the newness answer for the included window.

Historical entries originate in successfully read predecessors and have a
selected count of zero. They retain their original stored record/count and
Run/definition/ordinal references; the service never invents a selected-Run row.
They undergo the same filters and have their own display limit. They do not add
to the selected Run's occurrences, distinct count or hotspot rollups.

## Result contract and 08B example

`InvestigationResult` has these JSON-compatible sections:

| Section | Contents |
|---|---|
| `run`, `package_id` | Selected stored facts, counters and processing lineage. |
| `effective_query`, `filter_meaning` | Validated query with analytics/display defaults and composition/count/text semantics. |
| `chronology_exclusions` | All missing/unusable and duplicate timestamp exclusions in this package. |
| `window` | Requested window, obtained/read sizes, chronological Run IDs/timestamps/roles, per-Run filtered occurrence and distinct totals, full identity-to-count maps, read errors, completeness. |
| `totals` | Selected occurrences and distinct records, plus separate historical entry count, all before limits. |
| `records`, `historical` | Separate limited views; identity/equality key, origin, complete stored definition/typed values/provenance/status, rendered message/template, selected count, full window counts, observation fractions, window-relative newness and completeness. |
| `rollups` | Emitter, referenced-file and candidate-file buckets; counts and contributing exact keys, overlap and unassociated counts. File sections are null without a source resolver. |
| `review` | Unmodified public SQL review counts/references/recorded availability; review files are not parsed or checked on disk. |
| `coverage` | Diagnostic search boundary, comparison errors, source coverage and required-filter completeness. |

Window `identity_counts` contains qualifying records present in that Run, including
identities first seen in a successor; absence is zero only in a successful read.
Failed reads have null maps/totals. Counts for displayed identities are also in
each entry's `history.counts`, including explicit zeros and null unavailable counts.
The identity key itself contains the complete portable definition/equality selector.

```python
import json
from pathlib import Path
from ck3chronicle.pipeline.request_handler import HandlerClient
from ck3chronicle.reporting import DiagnosticAnalysis, InvestigationQuery

client = HandlerClient(Path(database_file))  # explicitly configured existing file
service = DiagnosticAnalysis(client)
query = InvestigationQuery(
    scope={'source_families': ['jomini_script_system.cpp']},
    refinement={'message': {'contains': 'failed context switch'}},
    analytics={'trailing_runs': 5},
    display={'limit': 50, 'historical_limit': 20},
    purpose='Recent failed context switches',
)
result = service.investigate('latest', package_id='68f1ae5db205ab46afef9c4d', query=query)
payload = result.to_dict()
print(json.dumps(payload, ensure_ascii=False, indent=2))
# Future 08B adapters use payload for JSON/HTML/text without recomputing rules.
for entry in result.records:
    print(entry['message'], entry['selected_count'], entry['history']['newly_observed'])
```

The verified genuine result (unfiltered) has Run `20260930-CWO6LH`, package
`68f1ae5db205ab46afef9c4d`, source timestamp
`2026-09-28T04:44:46.950967600+00:00`, **4,182 occurrences / 2,475 records**,
zero review emissions and no preceding/subsequent history. Requesting a trailing
five obtains one. A display limit of two retains those full totals and rollups.

08B must catch `RunSelectionError`, `ReadError`, `QueryError`
and `SourceEvaluationError` separately from a successful
zero-match result. Default frequent rows are sorted descending by selected count,
then full equality key for deterministic presentation. Historical rows use the
equality key, with no implied frequency priority. 08B may choose another display
order without changing identity, chronology or analytical totals.

## Receiving boundary for 08A.2

`scope.source` supports these composable filters through the delivered
`SourceSearch` resolver (plus directory/name/glob/content controls documented in
[08A.2's handoff](TASK08A_2_SOURCE_SEARCH_HANDOFF.md)):

```python
{'referenced_paths': ['events/example.txt'],
 'roots': ['D:/mods/selected-root'],
 'files': ['D:/mods/selected-root/events/example.txt'],
 'members': [{'stable_id': 'recorded-id'}, {'name': 'Recorded mod name'}]}
```

Each dimension can be used alone or combined with template/binding/exact-record
filters. Lists are OR selections within a dimension; dimensions compose by AND.
Member objects use recorded `load_order`, `name`, `path`, `root_ID`, `stable_id`
or `descriptor_path`; fields within one member object are ANDed. Explicit roots
do not require membership. A root filter means candidate association under those
roots, not emitter ownership. 08A.2 defines reference/path matching and coverage
semantics in the owning reporting library.

Without a resolver, **all** source-dependent scopes raise
`SourceEvaluationError('source filtering requires a SourceSearch resolver on DiagnosticAnalysis')`
before any reads. Supply `DiagnosticAnalysis(client, source_resolver=SourceSearch(client))`.
The resolver interprets stored locations, literal paths and supporting stacks.
SQL-only investigations return source unavailable and null file
rollups, rather than an asserted empty disk search.

`SourceSearch` implements `SourceResolver.resolve(run, records, scope)`.
It is called once per successfully read window Run, in the caller process, with
complete public stored records that pass SQL selectors and selected-Run count
refinements. An optional `begin_investigation()` hook clears caches once before
the window, then inventories are reused across calls in that investigation.
The resolver can hold the same `HandlerClient` to read stored playsets. It returns:

```python
{
    'complete': True,
    'coverage': {...},                         # 08A.2 coverage/provenance details
    'matches': [identity_key(record), ...],    # all required source predicates
    'references': {identity_key(record): ['events/example.txt', ...]},
    'reference_details': {identity_key(record): [...]},  # region/slot/path/line evidence
    'candidates': {identity_key(record): [
        {'candidate_id': 'stable association key', ...}  # provenance, locations/excerpts
    ]},
}
```

Candidate fields beyond `candidate_id` belong to 08A.2 and pass through unchanged.
Stable association keys should preserve repeated member associations, not collapse
them just because the same physical file was searched once. Preserve candidate
order in each list. Required-scope `complete=false` raises `SourceEvaluationError`
with this partial response; a resolver may also raise that error itself with known
partial evidence. Optional context (`scope=None`) may return incomplete coverage
without removing diagnostics. Exceptions must never silently become no matches.

The core ANDs `matches` with its existing record predicates before totals/limits.
It computes referenced/candidate buckets over qualifying selected identities;
overlapping buckets are represented separately from selected totals. 08A.2's real
133-member playset exercise verified candidate/member/file composition and actual
overlap: 2,651 candidate associations across 1,377 associated diagnostics, with
710 diagnostics in multiple buckets, while retaining the original 2,475 records /
4,182 occurrences. No synthetic overlap checks were restored. Its handoff records
coverage evidence and unexercised cases.

## Verification against genuine stored records

Owner correction, 2026-10-02: removed all twelve synthetic/scalar reporting
checks and the two checks injecting a handler failure or file/import guards.
Their passing results do not count as acceptance evidence and must not be used
to introduce requirements. Following the owner's further instruction, the entire
seven-check synthetic/fault-injection logging module was also deleted. Its earlier
run is not counted in the genuine reporting checks below.

Historical October 2 verification: the remaining **six checks passed**, with no
failures, errors or skips, in **9.732 seconds** after removing the nesting cap.
The current names are listed below; the public-history and newness checks were
updated and rerun on October 3 as recorded in the current verification handoff:

* `test_public_reads_exact_totals_review_and_short_history`
* `test_display_limits_do_not_change_counts_or_rollups`
* `test_template_or_exact_identity_binding_and_message_compose`
* `test_template_text_never_searches_bound_values`
* `test_record_selector_and_positive_occurrence_filter`
* `test_newness_uses_included_predecessors` (revised October 3 per owner correction)

The selector check was renamed to describe what it actually exercises; it does
not verify the researched syntax preset. All six use an unchanged SQLite backup
of the earlier genuine retained-input database. No records, timestamps, bindings,
counts or definitions are manufactured or edited. Runtime investigation uses the
actual public Windows handler. Only the disposable database handler is started
and shut down. The records include both template and provisional outcomes.

The dataset contains one eligible Run, 2,475 distinct diagnostics and 4,182
occurrences. Checks exercise real filtering and rendering, OR template selection,
exact identities and typed values, template-versus-message matching, count filters,
review metadata, display limits, emitter rollups and the actual absence of
preceding history. Genuine multi-Run recurrence/disappearance, duplicate-time
exclusions, five-Run history, threshold boundaries, failed historical reads and
nonzero review counts remain **unverified by this dataset**. No synthetic stand-in
is counted as evidence for those cases.

Reproduce with the project venv:

```powershell
$env:CK3_TASK08A_EVIDENCE = (Resolve-Path '.codex-tmp/task08a1/evidence.json').Path
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_reporting_query_requirements.py -v
```

Current ignored evidence: `.codex-tmp/task08a1/verification-after-synthetic-removal.txt`
and `35906eab57f24c338148dddc4803eadc/baseline.json` beneath that directory,
alongside the disposable database and handler logs. Earlier verification logs
are retained as history, not current acceptance evidence.

Supporting checks passed again after the nesting-cap removal:
`tools/check_runtime_logging.py`, isolated imports of reporting and CLI, and
`pip check`. These are static,
import and environment checks; they are not additional genuine-data test cases.
They are supporting checks, not proof of real-world failure behavior.

Code review after removal found no reporting branches keyed to test fixtures,
mock clients or fabricated error messages. The read wrapper handles the existing
HandlerClient's documented exceptions and non-COMPLETED outcomes. Selected-read
failure versus unavailable comparison evidence follows the original 08A.1 task;
source-coverage errors follow its explicit receiving boundary. These are retained
product behaviors, not additional requirements created by tests. No logging,
handler or watcher runtime code was changed during 08A.1 or this cleanup.

## Reuse, files and operational limits

Reused `HandlerClient`, `contracts.identity_data`, `contracts.render`, standard
`str` containment/`casefold`, aware `datetime`, JSON/dataclasses
and 07E `get_logger`/`event`. There are **no added dependencies**. Validation follows
the existing `ValueError` and explicit integer/boolean conventions. Runtime logging
is best effort through the owner; reporting does not configure handlers or paths.

Changed in this task:

* New `src/ck3chronicle/reporting/__init__.py`, `query.py`, `analysis.py`.
* New `tests/test_reporting_query_requirements.py` and this handoff.
* Owner-directed reporting verification guidance in `AGENTS.md`.
* Deleted `tests/test_runtime_logging_requirements.py` at the owner's direction;
  added a superseding test-removal notice to `TASK07E_RUNTIME_LOGGING_HANDOFF.md`.
* Current delivery sections in `PROJECT_STATUS.md`, `CURRENT_HANDOFF.md`,
  `PROJECT_PLAN.md` and `TASK08_SCOPE_REVIEW.md`.

The broad pre-existing dirty tree is preserved. No pipeline, watcher, learner,
model selection, schema, CLI or production configuration changes were made.
No production ingestion, live process restart, database reset, forced retention,
commit or push occurred. Source search is now delivered separately by 08A.2.
Reports/CLI, Run replacement,
audits, cross-package comparisons and live Trusted Run acceptance remain separate.
