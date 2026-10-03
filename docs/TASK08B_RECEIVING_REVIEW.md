# 08A.1 / 08A.2 receiving review for 08B

## Updated receiving decision — 2026-10-03

[08B's prompt](TASK08B_PROMPT.md) now receives the latest
[multi-Run handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md). It can launch:
the known-path traversal repair is delivered, so its former mandatory repair
assignment has been removed. The earlier review below remains historical evidence.

The prompt now uses actual counts, observation fractions and included-window
newness. It removes median/notability requirements and the deleted
`QueryEvidenceError` contract without commissioning a replacement statistic.
Positive records are new within a selected-only window; unavailable predecessors
do not veto newness, and actual comparison coverage must be disclosed.

Four eligible genuine Runs are now available. Upstream reports 18 investigations /
359 comparisons plus two single-Run checks, followed by 41 scope comparisons,
four source investigations / 93 comparisons and nine source tests. Those are
reported upstream results, not reruns by this advisor. The remaining absent
failure/duplicate-timestamp/full-window cases remain explicitly unverified.

This review read the handoff, current query/source implementations and readable
newness/scope reports. It confirmed removed exports/history fields and the
scope-before-inventory path by source inspection. Only documentation changed;
links and whitespace were checked. No runtime or production action occurred.
Template/message controls, report presets and other task scope were preserved.

## Earlier receiving review — 2026-10-02

2026-10-02. Advisor review of delivered source, handoffs and genuine-data checks.

## Recommendation

Launch [08B with the updated prompt](TASK08B_PROMPT.md). The diagnostic and source
libraries are integrated and usable. One owner-directed 08A.2 traversal-scope
correction remains; the updated prompt assigns it as 08B's first bounded receiving
repair in the existing source library. This is within the Reporting and Analysis
team's existing responsibility for bounded consumer gaps. It is not a claim that
the repair was completed by this review.

No new architecture, schema, queue, worker, model operation or live activation
is needed. Report/CLI implementation itself remains outstanding.

## Findings and prompt changes

1. **Complete the known scope-before-traversal correction.** In
   `src/ck3chronicle/reporting/source_search.py`, `_files` calls `_inventory` with
   `directories=['.']` when none were explicitly supplied, before applying exact
   file/reference constraints. `resolve` supplies known relative references to
   that path. Thus precise automatic lookup can enumerate whole roots first.
   This confirms the outstanding item already disclosed in the current handoff
   and 08A.2 memory review. 08B now explicitly owns finishing this bounded repair:
   deduplicate exact references, use direct checks or their parent scopes, preserve
   all candidates and evidence behavior, and update 08A.2's handoff. Broad queries
   remain supported. No measured count/time/memory becomes a new threshold.

2. **Receive the actual interfaces.** 08B now names `DiagnosticAnalysis`,
   `SourceSearch`, the delivered query fields, optional context versus required
   source filters, verbose excerpts, and the different partial-result shapes of
   `QueryEvidenceError` and `SourceEvaluationError`. A reference-only query
   deliberately performs no disk search; the report still needs optional context
   through the source library, as already required by its report behavior. Keep
   that SQL-only library capability intact.

3. **Apply current verification instructions.** Removed the obsolete instruction
   to reuse mathematical checks. The owner removed synthetic/scalar reporting
   and injected-failure checks, along with the synthetic logging module. 08B must
   use real stored records through the public handler and genuine source files;
   unavailable cases remain unverified, not fabricated into acceptance evidence.

4. **Receive delivered syntax research.** Replaced the stale missing-handoff
   conditional with implementation of the nine researched selectors through the
   existing query interface. The exact REASON binding and package/model scope are
   retained, as are both template/provisional outcomes. The research is available;
   the named report preset is still 08B's implementation responsibility.

Existing load-order-number presentation, independent source roots, file-level
content predicates, template OR selection, timestamps, recurrence policy and
exclusion of audit remain unchanged.

## Checks actually run in this review

Reviewed both delivery handoffs; the reporting query/analysis, source validation,
reference extraction and search implementation; the retained genuine test modules;
and the current 08B prompt. Did not read rejected database-handler design material.

- Reran all **six** genuine diagnostic checks: **passed**, no failures/skips,
  14.923 seconds. New unchanged disposable backup/results are under
  `.codex-tmp/task08a1/1a1f118e49dc468e83dde6f02833a77f/`.
- Reran all **nine** genuine source checks: **passed**, no failures/skips,
  216.948 seconds. Evidence is under
  `.codex-tmp/task08a2/c59ba41756ac47a6b8ea663056ef3e69/`.
- Applied the research's nine OR branches through `DiagnosticAnalysis` and the
  public handler on the new disposable SQL backup. The actual Run returned two
  records/two occurrences: one assignment-reason record with `template` status
  and one localization-token record with `provisional` status. Saved result:
  `.codex-tmp/task08b-review/syntax-receiving.json`. This checks receiving fit on
  available records, not all nine families or the future report preset.
- Runtime logging ownership check, isolated reporting/source/CLI imports and
  `pip check` passed. Document links and whitespace were checked separately.

The real source checks cover composition, independent roots, whole-file Boolean
content conditions, no-match results, excerpts and boundaries, visible stored
member order, unchanged SQL totals despite candidate overlap, and known partial
matches when real reference evidence is unavailable.

The new broad content pass searched 11,914 associations in 66 ripgrep batches,
with complete coverage/no issues, in **181.405 seconds**. Initial filename lookup
took 8.302 seconds and reused lookup 0.478 seconds. The earlier delivery recorded
13.181 and 62.297 seconds for content search on different passes. These timings
are variable observations, not controlled performance comparisons or guarantees;
the diagnostic suite briefly overlapped the source suite. Broad content searches
must not be presented as instantaneous on the strength of the fastest run.

## Evidence limits and work not done

The unchanged SQL dataset has one eligible Run. It cannot verify genuine
multi-Run recurrence/disappearance, duplicate-time groups or notability boundaries.
It does verify absent prior history and preservation of the actual counts. Missing
root/decoding/ripgrep-process failure cases were not manufactured; their full
runtime behavior remains unverified. The source handoff discloses further limits,
including Unicode case-fold equivalence and UTF-16/multiline cases not exercised.

The earlier memory measurements and candidate-equivalence experiments were read
as reported evidence, not rerun here. No reporting runtime code was changed, no
dependencies were installed, and no production database or live process was
modified. Only disposable verification handlers were started/stopped. No commits
or pushes. 08B's first repair and final report delivery still require execution.
