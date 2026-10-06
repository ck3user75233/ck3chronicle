# 08A.1 / 08A.2 genuine multi-Run verification — 2026-10-02

## Scoped source traversal corrected — 2026-10-03

The owner's acceptance was for **unscoped searches defaulting to all mod roots**,
not for disregarding supplied restrictions. My broader acceptance statement below
was incorrect and is superseded by this delivery. No task prompt was changed.

`source_search.py` now applies member/root selection before availability probes;
an unrelated mod is no longer probed while selecting one member. Explicit
directory/recursion scopes apply before traversal. `_lookup_scope` derives
nonrecursive parent-directory inventories from exact files, exact relative paths
and stored relative references, intersected with explicit scope. Required files
are still checked for existence when no diagnostic references them; a genuine
zero-match Run must not be reported as a missing file. Candidate filtering/order,
case controls, excerpts and existing coverage errors are retained.

A filename-only or explicit basename search has no supplied parent directory;
it searches for that name within the selected root/directory scope. This does
not authorize ignoring member or directory restrictions. Cached inventory reuse
never broadens a traversal. `coverage.metrics.inventory_scopes` records actual
root/directory/recursion inventory construction for evidence and consumers.

Verification uses unchanged genuine SQL/playsets and installed source files:

| Actual query | Enumerated entries | Returned candidates |
|---|---:|---:|
| Filename anywhere in the recorded playset | 105,603 | 2 |
| Exact sea_minority file, no explicit directory workaround | 433 | 2 |
| Exact relative path or stored-reference path | 433 | 2 |
| Selected EB+EC724 member and exact file | 11 | 1 |
| Selected member, directory and filename | 11 | 1 |
| All genuine references, parent scopes only | 25,786 | 2,651 diagnostic associations |

All 41 scope/candidate comparisons passed. Four multi-Run source investigations
passed 93 comparisons; file queries deliberately omitted `directories` and still
returned correct zero/nonzero counts, candidates and recorded members for each
Run. Both disposable database hashes remained unchanged. Logging ownership,
isolated imports and pip check passed. No synthetic evidence, new dependency,
custom walker, schema change or production action was introduced.

Readable report: `.codex-tmp/task08a2/scope-repair/SOURCE_SCOPE_REPORT.md`.
Scope evidence/script: `.codex-tmp/task08a2/scope-repair/` and
`.codex-tmp/task08a2/verify_scope_repair.py`. Multi-Run evidence:
`.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/source-scope-review/`.
All nine retained genuine source tests also passed, with no failures or skips,
in 291.710 seconds; the exact log is
`.codex-tmp/task08a2/scope-repair-checks.txt`. Timing observations overlap that
suite and are not controlled benchmarks or new product thresholds.

08B receiving delta: the known-path traversal repair is now implemented and its
evidence is delivered; receive it rather than implementing another resolver.
Keep the existing whole-message/template-assignment/newness rules and display
explicit effective search scope. No receiving instruction was edited into the
08B prompt. One documentation patch initially failed due to a stray context
line, then applied successfully; no data-check failure or new requirement resulted.

## Owner accepts default root inventory — 2026-10-03

The owner clarified that enumeration of all selected playset roots is acceptable
as the default and requested documentation in code. `SourceSearch`, `_files`
and `resolve` now document the existing behavior precisely:

- Without explicit roots/member selectors, use every accessible member root in
  the selected Run's **recorded** playset, not today's active playset.
- Omitted `directories` means each selected root, recursively unless
  `recursive: false` is supplied. Exact filenames/files/references filter the
  inventory afterward; they do not implicitly narrow directory enumeration.
- Explicit roots, members and directory scopes are honored. Repeated physical
  root/scope inventories are reused within the session; member associations and
  recorded load order are preserved.
- Inventory construction retains paths, not every file's contents. Content
  searches and excerpts read their selected files separately.

This supersedes the default-traversal defect/open-repair classification in the
earlier reconciliation below. The default is accepted, not newly optimized or
repaired. **08B receiving change:** do not treat automatic narrowing from exact
references as a mandatory first repair; document the default and expose explicit
scope controls. The task prompts were not edited. Explicit narrower directory
scope must still be respected. This update changes docstrings/documentation only;
the previous genuine-data results remain the evidence, with no new test run.

## Completion-claim correction and requirement reconciliation — 2026-10-03

The owner requested confirmation that prompt edits had not been used to reduce
the delivery. The median/newness edits to the three task prompts were reversed;
their original requirements remain visible. Completion must be assessed against
those requirements plus the owner's subsequent instructions, not against an
agent-edited assignment. No task prompt was changed during this reconciliation.

**An unqualified claim that all original 08A.1/08A.2 deliverables are complete is
not accurate.** In particular, the known-path traversal correction is an
unfinished 08A.2 requirement. Recording it as an 08B receiving repair does not
fulfil or remove it. The successful source-filter tests supplied explicit parent
directories and therefore do not establish the missing automatic narrowing.

| Requirement group | Delivered implementation/evidence | Completion qualification |
|---|---|---|
| 08A.1 structured query, stored template-reference OR selection, whole-message/grouped literals, exact identity, typed bindings and count refinements | `query.py` and `analysis.py`; public signatures/examples in the 08A.1 handoff; genuine diagnostic and multi-Run checks | Implemented. Exact/partial template-text APIs from the original prompt remain present; they were not deleted or substituted for stored assignment selection. |
| 08A.1 handler-only reads and contract rendering/identity | HandlerClient reads; `contracts.render` and full `identity_data`; no repository/SQLite runtime access | Implemented and exercised on unchanged genuine backups. |
| 08A.1 package/source-timestamp chronology, windows, history, historical entries and exclusions | Four eligible genuine Runs and fourteen missing-timestamp exclusions; per-Run raw/filtered counts and default/trailing windows | Exercised for available history. Naturally failed reads were absent and remain unverified; no synthetic evidence was used. |
| 08A.1 original median/notability requirement | Was implemented and verified before the owner rejected median-based comparison; median and derived labels subsequently removed | A change following the owner's discussion, not fulfilment of the original formula requirement. No replacement notability capability has been delivered. |
| 08A.1 newness evidence rule | Updated to presence in selected Run and absence in included predecessors, without the prior unavailable-read veto | Owner-directed rule replaces the original gate. The implementation's selected-only-window behavior is explicitly disclosed below. |
| 08A.1 counts, rollups, display limits, review data and explicit record selectors | Returned through InvestigationResult; genuine tests cover totals/overlap and selector composition | Implemented; researched CLI presets remain 08B work, as originally split. |
| 08A.2 recorded playsets, independent roots, filters, all candidate associations, grouped ripgrep content and excerpts | `source_query.py`, `source_references.py`, `source_search.py`; original genuine source checks and integrated multi-Run evidence | Implemented for demonstrated cases. Recorded member/load order and independent-root behavior are retained. |
| 08A.2 use a supplied reference directory and avoid broader-than-requested traversal | `_files` still calls `_inventory` over selected roots before exact path/reference filtering when `directories` is omitted | **Open implementation defect against the source-scoping requirement.** Explicit-directory workarounds and passing result totals do not close it. Currently assigned to 08B as a bounded receiving repair, but still outstanding 08A.2 work. |
| 08A.2 performance/reuse/streaming and dependency documentation | Real 133-member playset timings, 105,603-entry inventory measurement, scoped/direct-path experiments, batched streamed ripgrep output; stdlib helpers and installed ripgrep | Measurements and implementation delivered. They do not prove the unresolved automatic narrowing or every encoding/case/error scenario. |
| 08A.2 unavailable-source/partial-result behavior | Explicit coverage/error paths and known partial matches retained | Genuine unavailable-reference cases exercised; missing-root/decoding/process-failure cases not manufactured and remain unverified. |
| Handoffs, current-status updates, human-readable results and required environment checks | Both 08A handoffs, this receiving delta, current reports, logging/import/pip checks | Delivered. Generated evidence is ignored; no production mutation, package change, commit or push. |

The latest 18-investigation/359-comparison pass establishes the stated genuine
cases, not universal completion of the original assignments. No replacement
threshold, reduced diagnostic filter set or new synthetic requirement was added.
This reconciliation read the restored prompts, owning query/history/source code,
and retained handoffs/evidence; it did not rerun acceptance checks or fix the
open traversal defect. One document-read command had a numeric-argument typo and
was rerun successfully; this was not a runtime/data-check failure.

## 08B receiving changes — handoff only

Owner direction: changes required by this delivery belong in the handoff, not
in another team's assignment prompt. My median/newness edits to the 08A.1,
08A.2 and 08B prompts have been reversed. The implementation and verification
below remain delivered. The following is the explicit receiving delta for 08B;
its team should reconcile older prompt wording against these owner clarifications.

| Receiving area | Required consumer change |
|---|---|
| Library responsibility | Receive actual counts, exact recurrence and window-relative newness; the median-based notability calculation has been removed. |
| Exception handling | Remove imports/catches of `QueryEvidenceError` and assumptions about its `.partial` result. The novelty-unavailable gate was removed. Continue handling `ReadError`, `RunSelectionError`, `QueryError` and `SourceEvaluationError`; source partial evidence remains distinct from successful empty results. |
| History fields/presentation | Use `history.counts`, `selected_count`, preceding/subsequent observed/read counts and fractions, and `newly_observed`. Removed fields: `preceding_median`, `baseline_available`, `notable`, `positive_above_zero_median_with_prior_observation`. |
| Newness | Present in selected Run and absent from every preceding Run actually included in the comparison window. Only included, successfully read predecessors determine the answer; unavailable comparisons do not veto it. The implementation reports positive records as new within a selected-only window. |
| Frequency labels | Remove median displays and old median-derived increase/decrease labels. No replacement baseline or threshold has been commissioned. Show actual counts, newness and absence. |
| Coverage | The obsolete `novelty_filter_unavailable_identities` list is removed. Ordinary comparison errors, source coverage and actual observation denominators remain separate evidence. |
| Template and message controls | Template selection means one or more stored ingestion-time template references, ORed across records. Diagnostic text search includes the entire rendered message and all slot values. Do not substitute template-wording search or rematching for these controls. |
| Verification evidence | Receive the unchanged four-Run results: 18 investigations / 359 comparisons plus two genuine single-Run checks, all passed. Current readable report and exact paths are below. |

For precise edit accountability, the five changes I had made to the 08B prompt
were: replacing “exact history and notability” with “exact history and newness”;
replacing its `QueryEvidenceError.partial` instruction with removal guidance;
replacing preceding-median presentation with window-relative newness; replacing
the median/no-history newness paragraph with the included-predecessor rule; and
replacing notable-rise/drop presentation with actual counts/newness/absence and
no replacement threshold. All five prompt edits are now reversed; the receiving
changes are listed above instead.

Outstanding implementation explicitly assigned to 08B remains: constrain source
traversal by known file/path scope before enumeration, then deliver the CLI and
reports. This follow-up completed the newness/median correction and genuine-data
verification; it did not complete that separately assigned source repair or 08B.

## Owner correction implemented: included-window newness — 2026-10-03

**Current delivery supersedes the median-based result below.** New means present
in the selected Run and absent from every preceding Run actually included in the
comparison window. The implementation uses successfully read preceding counts;
unavailable comparisons no longer veto the answer or the `newly_observed` filter.
With no included predecessors, positive records are new within that window.

Removed `preceding_median`, `baseline_available`, `notable`, and
`positive_above_zero_median_with_prior_observation` from observations, together
with the `statistics.median` import, novelty-unavailable gate/coverage list and
`QueryEvidenceError` class/export. Actual counts, fractions, full identity,
source filtering and ordinary read-error coverage remain. No replacement
baseline or increase/decrease threshold was added.

Reused the same unchanged four-Run backup named below, with all runtime reads
through HandlerClient. **18 complete genuine investigations and 359 comparisons
passed, zero mismatches.** Two updated genuine single-Run checks also passed:
`test_public_reads_exact_totals_review_and_short_history` and
`test_newness_uses_included_predecessors`. No synthetic or fault-injection check
was used. Logging ownership, isolated imports and venv `pip check` passed.
The backup SHA-256 still equals
`0826df9afdf0db26722134986007d44c3e92f8fd7339c35304f5b700172a9332`.

Latest-Run message/file/mod totals remain 51/245, 2/64 and 15/84 respectively
(diagnostics/occurrences). The latest newness filter still returns 252 diagnostics
with 600 occurrences. Genuine counts `[0,45,0]` followed by `45` correctly yield
new=false because an included predecessor observed that identity. The oldest-Run
newness query returns its 3,308 diagnostics / 12,804 occurrences as new within
its window. Historical zero-count entries remain not new.

Current readable report: `.codex-tmp/task08-multirun/WINDOW_NEWNESS_REPORT.md`.
It supplies exact queries, per-Run counts, observation fractions/newness,
template assignment examples, source-binding distinctions, candidate files and
recorded load orders. Full evidence is in the earlier backup directory's
`presence-review/` child; original verification artifacts remain unchanged.
Reproduce with ignored `validate_presence.py` and `report_presence.py`.

Changed runtime files: `reporting/analysis.py`, `reporting/__init__.py`; updated
the two existing real-data checks in `tests/test_reporting_query_requirements.py`.
Updated the public handoff and current decision/status pointers. Task-prompt
edits were restored per owner direction; all required consumer changes are
listed in the receiving section above rather than applied to 08B's assignment.
No check failed in this follow-up. No new product requirement, dependency,
production action or replacement statistical rule was introduced.

All included reads succeeded; naturally unavailable reads remain unexercised,
as do unavailable source roots. No such case was
fabricated. 08B and its separately assigned traversal-scope repair remain open.

## Timestamped history verified — 2026-10-03

The earlier timestamp blocker is resolved for the four newly available eligible
Runs. **17 complete investigations and 340 genuine-data comparisons passed, with
zero mismatches.** The prior 14 Runs remain excluded; no history was backfilled.
This supersedes the blocked current outcome below, which is retained as history.

Fresh unchanged backup, taken at `2026-10-03T06:06:07.634175+00:00`:
`.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/unchanged.sqlite3`.
SHA-256 before/after all verification:
`0826df9afdf0db26722134986007d44c3e92f8fd7339c35304f5b700172a9332`.
The source is the same configured production database named below; SQLite was
used only for its read-only-source backup operation. All runtime reads used
`HandlerClient`. Package: `68f1ae5db205ab46afef9c4d`.

| Eligible Run in source chronology | Stored source-log timestamp | Default before / after |
|---|---|---|
| 20261002-2PVVSE | 2026-10-02T12:23:07.384133700+00:00 | 0 / 3 |
| 20261003-IS3QON | 2026-10-03T00:09:53.872195700+00:00 | 1 / 2 |
| 20261003-D3N7ZQ | 2026-10-03T02:34:42.700452600+00:00 | 2 / 1 |
| 20261003-74G2EB | 2026-10-03T05:04:14.687380500+00:00 | 3 / 0 |

Trailing five at latest obtained the selected Run plus three predecessors, no
successors. All comparison reads succeeded. All 14 missing-timestamp exclusions
were disclosed on paginated Run selection and every investigation.

The readable report is `.codex-tmp/task08-multirun/TIMESTAMPED_MULTIRUN_REPORT.md`.
It contains exact query forms, every Run/exclusion, expected/actual totals,
per-Run source-filtered counts, candidates with recorded member/load order,
different source bindings under one template, and genuine notability examples.
Full machine-readable evidence resides alongside the backup.

Owner clarification governs this verification: **template selection uses stored
ingestion-time template references with OR semantics**. Diagnostic substring
search uses the entire rendered message, including slot values. No template-text
search or rematching was substituted for these operations.

Latest-Run expected and actual results agreed:

| Investigation | Diagnostics | Occurrences | Historical entries |
|---|---:|---:|---:|
| Whole-message contains `failed context switch` | 51 | 245 | 94 |
| Same message, selected sea_minority file | 2 | 64 | 0 |
| Same message, EB+EC724 Compatibility Patch | 15 | 84 | 11 |
| One stored template reference | 202 | 396 | 61 |
| Two stored template references, OR | 244 | 1,158 | 112 |
| Selected count zero | 0 | 0 | 1,114 |
| Newly observed | 252 | 600 | 0 |

Source queries also passed against interior Run `20261003-IS3QON` with one
predecessor and two successors. Each Run used its own recorded 133-member
playset. The file candidates retain load orders 114 and 115. Expected identity
sets came from actual source references/direct file checks; actual per-Run
identity/count maps exclude out-of-scope records. Raw exact recurrence counts
remain distinct from these filtered totals. The file query explicitly supplied
`directories: ["common/on_action"]`, `recursive: false`, and the exact relative
file; this does not claim to finish the separate automatic traversal-scope repair.

Every returned observation was compared with independent calculations on actual
stored counts, including genuine absence, fractions, medians, novelty and the
specified notability formulas. Examples include a fractional baseline `0.5`,
an exact increase boundary `B=2, C=20`, and counts `[0,45,0]` before `C=45`:
the latter has median zero but is neither new nor notably increased. The oldest
Run has no baseline/novelty; its three successors do not supply a baseline.
Display limits, nested message conditions, exact/template composition, historical
origins, emitter rollups and overlapping candidate buckets also passed.

No runtime defect was demonstrated and no runtime code or product requirement
was changed. No synthetic tests, fabricated history, mock clients or injected
failures were used. Logging ownership, isolated reporting/source/handler imports
and venv `pip check` passed; no dependencies were installed.

One report-generation command failed because it preceded completion of the
verifier's final integrity JSON. It was rerun successfully after verification
exited; no data comparison failed and no runtime branch was added in response.

Still unexercised: naturally failed/unavailable reads and denominator exclusion,
unavailable-source cases, full five-before/five-after
capacity and exhaustive threshold boundaries. These are evidence limits, not
new requirements or blockers for the genuine short-history checks delivered here.
Scripts: `check_current_availability.py`, `validate_timestamped.py` and
`report_timestamped.py` in the ignored `.codex-tmp/task08-multirun/` directory.

## Outcome: chronological verification blocked

The configured current database has 14 genuine Runs in package
`68f1ae5db205ab46afef9c4d`, with 38,269 diagnostic rows / 683,608 occurrences.
**Every Run lacks `facts.error_log_source_modified_at`. Eligible Runs: zero.**
This differs from the earlier single-Run disposable timestamp-delivery dataset.
The requested chronological multi-Run acceptance is not complete.

Source database:
`C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/ck3chronicle-schema3-20260928T211854Z.sqlite3`.
An unchanged, consistent backup was created at
`.codex-tmp/task08-multirun/049e5d1d395f4ad6b31008f177e9edab/unchanged.sqlite3`.
SQLite access was limited to the backup operation using a read-only source
connection; every runtime database read used `HandlerClient`. The backup remained
byte-identical before and after the exercise, SHA-256
`efa4cde8e65f7bd0a379841a4b01048830316e34fe1b9006d926440fe817d577`.

The readable report, with every Run ID/timestamp exclusion, actual queries,
expected/actual counts, exact-identity matrices and candidate/member details, is
`.codex-tmp/task08-multirun/MULTIRUN_VERIFICATION_REPORT.md`.
Full raw public reads and verification results remain beneath the backup directory.

## Genuine checks completed

- `DiagnosticAnalysis.list_runs(package_id, limit=1)` returned zero eligible
  Runs and all 14 exclusions. Eligibility was applied before pagination.
- Explicit selection of each actual Run raised `RunSelectionError` with the
  missing-timestamp explanation. `latest` with default history and trailing-five
  likewise rejected selection. Five actual structured template/message/file/mod
  queries were also rejected for that reason. These are successful exclusion
  checks, not successful empty investigations.
- All 14 Runs' diagnostics, metadata, review metadata and 133-member captured
  playsets were readable through public operations. Read failures were not
  fabricated. All saved records remained unchanged on repeated public reads.
- The shared literal evaluator was exercised on actual stored template and
  rendered diagnostic text. `failed context switch` occurs in bound REASON values
  and rendered messages, but matched zero template texts across all 14 Runs.
  Template substring `trigger` had genuine matches.
- The public `SourceSearch.resolve` component was exercised for every Run using
  that Run's recorded playset, with a mod scope (`EB+EC724 Compatibility Patch`)
  and a file scope (`common/on_action/sea_minority_on_actions.txt`). File lookup
  explicitly supplied its parent directory/nonrecursive scope; no automatic
  traversal repair was smuggled into this verification.
- Expected membership/candidate pairs came from real stored references and
  direct checks under selected recorded roots. Actual resolver matches agreed,
  as did summed original occurrence counts. Excluded identities contributed
  nothing to the filtered counts. Source coverage was complete in these cases.
- Four recurring full identities were compared across all 14 successfully read
  Runs using definition-scoped contract equality and actual stored counts.
  Genuine absent identities contributed zero to this **unordered count matrix**.
  No preceding/subsequent labels, medians, novelty or disappearance claims were
  attached to excluded Runs.
- Genuine records sharing template `433855ecb17db0d8beeacd6a` and non-LOCATOR
  bindings retained distinct identities for health_events source lines 12528
  and 12537. Equal occurrence counts did not collapse their identities.

For named Run `20261002-B3CK5G`, the source component expectations and actuals were:

| Scope within rendered-message `failed context switch` | Expected records / occurrences | Actual records / occurrences |
|---|---:|---:|
| No source restriction | 94 / 24,478 | 94 / 24,478 |
| Selected sea_minority file | 2 / 64 | 2 / 64 |
| Selected EB+EC724 mod | 19 / 118 | 19 / 118 |

The file result has candidates in recorded load orders **114** (Early Bookmarks
and the Legendary Super Compatch) and **115** (EB+EC724 Compatibility Patch).
Culture and faith exact identities contribute 32 occurrences each. The two
health_events exact identities have 25 occurrences each in the same Run, but
are excluded from this file scope. Their stored counts are not rewritten to zero.

These source totals are component results, **not** an end-to-end
`DiagnosticAnalysis` comparison window. Its chronology correctly prevents
that investigation. Raw exact-identity counts and source-filtered counts remain
separate in the report and JSON evidence.

## Failures, limits and receiving prerequisite

There were no unexpected source/count/equality mismatches: 253 real-data
comparisons passed, plus eligibility/query rejection checks. This is a count of
comparisons over actual Runs, not 253 invented test scenarios or requirements.
One report-generation command initially failed from an unterminated Python
string; the ignored generator was corrected and rerun. No runtime defect was
demonstrated by the exercised checks and no runtime code was changed.

Not verified: eligible multi-Run chronological ordering, actual default/trailing
window sizes, source-filtered totals through a successful history investigation,
observation fractions/denominators, medians, novelty/notability and threshold
boundaries. No failed reads or unavailable
source roots occurred. No such evidence was fabricated. A missing timestamp is
an eligibility exclusion, not a failed diagnostic read.

An existing database with multiple eligible timestamped Runs is needed to finish
the requested historical acceptance; the owner was asked whether a different
database was intended. Do not substitute processing/capture/process-start times
or backfill these Runs. The source-mtime handoff now documents a separate
owner-authorized live activation at 10:49:49 UTC on October 2. A fresh unchanged
backup under `.codex-tmp/task08-multirun/22a2b73650db4db9b0ea4d0bbabb5baa/`
was subsequently checked through HandlerClient: still the same 14 excluded Runs,
zero eligible Runs. No live process was restarted by this verification.
Producer/operations receiving should confirm that a future
genuine capture's original source timestamp appears unchanged in public
`get_run` / `list_runs` facts. No missing handler operation was identified.

## Verification tools and changes

Ignored reproducing scripts: `collect.py`, `read_existing.py`, `components.py`,
`probe_queries.py`, `build_report.py` under `.codex-tmp/task08-multirun/`.
They use the project venv and the real backup. No new dependency was needed.

Runtime logging ownership, isolated reporting/source/handler imports and
`pip check` passed; output is `environment-checks.txt` in that directory.
No synthetic, scalar-only or fault-injection acceptance tests were added or run.
The follow-up readable report puts whole-message investigations first and makes
explicit that all slot values are searched. Template-reference checks are separate
optional filters, not a substitute for searching diagnostic content. A search for
other local database paths encountered access-denied pending folders; this is not
a failed diagnostic read and no claim of a comprehensive machine-wide search is made.
The existing source-scope receiving improvement remains assigned separately in
the 08B prompt; this exercise did not redesign its contract or complete 08B.

Changed tracked-intent material is documentation only: this verification handoff,
the two 08A handoff pointers, and current status/handoff/reporting ledger.
No production writes, ingestion, process restarts, schema/model selection changes,
commits or pushes occurred. Only disposable handlers were started/stopped.
