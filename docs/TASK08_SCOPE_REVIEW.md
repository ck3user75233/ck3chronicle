# Tasks 08A.1 / 08A.2 / 08B — current scope decisions

## 08B delivery disposition — 2026-10-04

Unreadable/unsupported current files are per-file source results, with a reason
and disclosure that their contents/excerpts could not be read. They are distinct
from a crashed/failed source-search process. Busy database requests queue through
the existing handler; runtime connection loss is not a busy-queue rejection.
These owner clarifications require no new pipeline policy.

The owner clarified that source-process/database faults are ordinary execution
errors to surface at the caller boundary. A bounded reporting CLI repair now
handles unexpected Python exceptions consistently and preserves the error on
stderr if error rendering also fails. No broader recovery system or new analytical
requirement is commissioned. Unencountered crash paths remain verification limits.

Implementation and owner-requested corrections are complete. The authoritative
[handoff checklist](TASK08B_REPORTING_HANDOFF.md) lists the delivered CLI, five
presets, composable queries, report formats, history/source experience, verification
and documentation. No known assigned feature/documentation work remains. Two
unencountered runtime fault groups are disclosed as verification limits, not
executed tests or new requirements. Full live Trusted Run acceptance is separate;
commits and pushes remain deferred. Historical review entries below retain their
original evidence and do not override this disposition.

## Owner clarification: content search and concrete availability — 2026-10-04

Default phrase/token investigation searches the whole diagnostic, including
template literals and populated slots. Match origins and assigned templates are
result data; templates do not produce errors. No special template-discovery query
or slot-only flags are commissioned. The contrived template-phrase acceptance
example is withdrawn. Bounded shared-renderer provenance, analytical match
annotations/rollups and report columns implement this through existing services.

Requested Run positions must display unavailable neighbors. Eleven simultaneous
Runs are not required for acceptance; existing full-side and new seven-Run
position checks cover this. Raw-log/model independence is verified through I/O
observation, with no input removal. Empty results, no-path emissions and missing
Run positions are normal outcomes. Handler operation/transport errors and current
source-search process launch/error exits are separately named execution faults;
these two fault paths were not encountered in retained checks. Exact results and
limits are in [08B](TASK08B_REPORTING_HANDOFF.md). Live Trusted Run remains separate.

## Owner deletion: reporting duplicate-detection requirement — 2026-10-04

The owner directed removal of timestamp-based duplicate Run exclusion/rejection
from Data Intelligence. Duplicate-ingestion handling belongs to the pipeline.
The rule and its verification obligation are deleted from reporting code, prompts,
handoffs and open-item tracking. It is not an unverified case. No replacement
duplicate policy, new timestamp test or pipeline modification is commissioned.
Ordinary package/source-time history remains in 08A.1; [08B](TASK08B_REPORTING_HANDOFF.md)
records the regression checks.

## Earlier failed-query and incomplete-item traceability — 2026-10-04

The owner requires the earlier incomplete-deliverable assessment to be visible,
not implied by individual improved reports. The review bundle now maps its six
review IDs and 17 named query outcomes explicitly. Four evidence-gap groups remain
unverified. This is a bounded reporting/documentation correction using saved CLI
outputs, with direct links from each report; it claims no additional failure-case
acceptance. See [08B](TASK08B_REPORTING_HANDOFF.md).

## Owner direction: file status, columns and error source — 2026-10-04

The owner now directs single-file/line analytics to use the last matching playset
member in load order as the error source. This supersedes earlier blanket limits
on identifying a winning source for that case. Implementation stays in the source
and analysis libraries; reports show the same JSON decision. Status labels are
Resolved / File not found; raw load order, mod name, file path and line have their
own columns. All matching copies remain visible. Genuine CLI and browser evidence
is recorded in [08B](TASK08B_REPORTING_HANDOFF.md). No separate broader causal
analysis or schema change is commissioned.

## Owner clarification: game-relative path selection — 2026-10-04

The ordinary path filter names the same relative location under all recorded
playset members, for example `/common/scripted_effects/some_file.txt`. The explicit
`relative_path.exact` selector accepts the optional leading slash; lookup inventories
only the parent directory and retains every matching mod candidate. A different
relative directory is not a basename match. This bounded source/consumer clarification
is implemented and verified with genuine stored data; see [08B](TASK08B_REPORTING_HANDOFF.md).

## Owner correction: no path is normal emission content — 2026-10-04

The owner rejects calling an emission incomplete because it supplies no path.
No path means source lookup is not applicable, not unavailable evidence. The
source/query owners now export neutral path presence, skip unnecessary source
lookup, and preserve ordinary nonmatching filter behavior. Reports remove warning
styling and do not attach another record's lookup failure to a pathless emission.
The [08B handoff](TASK08B_REPORTING_HANDOFF.md) records genuine verification.

## Owner addition: measure recursion and expose search counts — 2026-10-04

The owner requested independent counts under search roots and returned file/folder
counts to verify recursion. 08A.2 now supplies per-search unique physical-path
counts plus actual root/directory/recursion/cache details; 08B presents them.
Twenty-nine comparisons pass against genuine trees independently enumerated with
PowerShell, including full roots, recursion off, directory and exact-file scopes,
cache reuse and repeated roots. Counts remain measurements, not thresholds.
The ordinary root CLI also verifies scoped counts in all formats. An initial
checker newline failure and successful fresh rerun are disclosed in the
[08B handoff](TASK08B_REPORTING_HANDOFF.md). No new storage or search architecture,
synthetic source trees, production change or broader acceptance claim.

## Owner addition: explicitly seek unresolved paths — 2026-10-04

The owner requested a way to find messages whose recorded paths could not resolve.
The source/query owners now provide `scope.source.resolution` (`unresolved` or
`resolved`), and reporting displays/exports the per-reference current result.
Stored paths stay authoritative recorded evidence; current resolution is measured
at report generation within the disclosed scope, not written into historical
diagnostics. Missing paths and incomplete searches remain distinct. Ordinary path
filtering keeps its corrected semantics below. Genuine and authorized fixture
checks are recorded in the [08B handoff](TASK08B_REPORTING_HANDOFF.md); no new
architecture, production activation or expanded synthetic-history permission.

## Owner correction: path selection is ordinary filtering — 2026-10-04

The owner rejects errors/partials caused by records without a usable matching
path. This supersedes earlier source requirements treating unidentified references
or explicitly missing files as failed evidence. Path-only investigations match
recorded paths independently of disk existence; nonmatches are excluded normally.
Root/member/content predicates still use current candidate evidence. Missing
individual files are ordinary nonmatches; actual required-source read failures
remain failures. No additional filter language or storage architecture is added.

The bounded correction is in the owning source/query library, with obsolete
unidentified-record error presentation removed. Updated root-CLI examples include
an unrestricted path query, successful empty results, the authorized fake-LOCATOR
fixture and a genuine archive with no playset. Relevant genuine CLI/source checks,
fixture and archive exports pass. See [08B handoff](TASK08B_REPORTING_HANDOFF.md).
Prior test expectations do not override this owner correction. Production and
unrelated work remain unchanged; no commits or pushes.

## Earlier 08B verification follow-up and bounded synthetic permission — 2026-10-04

The owner explicitly authorized two copied genuine emissions with only fake file
LOCATOR paths, paired with the normal captured playset JSON. This bounded exception
supersedes the blanket synthetic-data prohibition for that fixture; it does not
authorize fabricated history or unrelated injected failures. Five checks across
eleven actual CLI exports pass with all 133 original playset members preserved.
Source API semantics are unchanged; missing paths in readable roots are distinct
from unavailable roots. The fixture report links inputs and verification evidence.

Available genuine cases were also pursued: a fresh unchanged backup supplies seven
eligible Runs, now verifying a full trailing-five and each five-neighbor side.
Five unchanged archived logs in separate single-Run storage cover all nine syntax
selectors and missing-playset behavior. Seventeen exports cover 85 syntax records;
original logs and production chronology are unchanged. No simultaneous eleven-Run
claim is made. The failed temporary-capture rename/retry is disclosed in
[the handoff](TASK08B_REPORTING_HANDOFF.md).

The 54-example review bundle links these completed checks from `outcomes.html`,
with four remaining genuine-evidence gap groups clearly separate. Browser checks,
two focused genuine CLI groups and logging/imports pass. No new dependency,
architecture, live activation, commit or push. Full Trusted Run remains separate.

## Earlier 08B explanation integrated with report evidence — 2026-10-04

The owner's later request to see earlier incomplete deliverables is addressed by
a visible `outcomes.html` reconciliation in the review bundle, linked from each
example. Completed fixes and unverified genuine-data cases remain distinct; the
page gives the evidence needed for the latter. No scope or acceptance rule changes.

Further owner review requires the explanation and the evidence it discusses to
be together. An outcome anchor alone did not resolve the reading problem. The
report renderer now includes template patterns, Run counts and example diagnostic
evidence in the opening explanation, with direct links to exact detail entries
and verbose source excerpts. The 38-example bundle, genuine CLI format/partial
groups and actual Chrome navigation were checked; precise evidence is in
[the reporting handoff](TASK08B_REPORTING_HANDOFF.md). This presentation correction
does not change analytical results or evidence limitations.

### Earlier 08B reporting closure record — 2026-10-04

The owner required completion of the remaining implementation, clarity and browser
work before finishing 08B. That work is now complete, with the evidence matrix in
[the reporting handoff](TASK08B_REPORTING_HANDOFF.md). The owner's empty-set feedback
supersedes the older prompt's rejection of contradictory preset refinements:
well-formed filters are ANDed and can produce zero matches. Preset definitions
remain explicit in the reusable query model's additional `refinement.all` clauses.
Missing required selectors and invalid execution controls still fail validation.
This is a bounded correction in the owning query library, not a new architecture.

Required-source evaluation semantics are unchanged. Partial reports now show the
pathless diagnostic separately so the incomplete result can be understood. The
existing source resolver supplies the evidence. Mod names, Run counts, templates
and a genuine DLC-file example have been visually inspected. Chrome navigation,
all eight CLI groups, six query and nine source checks passed; a later focused
partial-report check covers the final presentation change. Earlier unavailable
browser verification is superseded by the current actual walkthrough.

Unrepresented genuine failure/duplicate/full-window cases and seven absent syntax
selectors remain disclosed, consistent with the assignment's evidence rules.
No synthetic acceptance data, production changes, commits or pushes were added.
Full live Trusted Run acceptance remains separate.

### Earlier implementation evidence — 2026-10-03

Owner usability refinement: every report explains its query, expected behavior,
actual results and how to read diagnostics; each genuine consumer example has a
specific plain-English check description. Visible file tables add recorded mod
names/load-order numbers beside mod paths using existing source-service provenance.
Base-game/DLC paths remain simple. No analytical selection or identity rule changed.
All eight root-CLI groups passed; precise evidence is in the 08B handoff.

Owner presentation correction: template investigations show the stored pattern
and combined per-Run counts first; diagnostic instances and their match statuses
are labelled explicitly. Template aggregates are reusable 08A.1 data, computed
before display limits with separate full diagnostic identities. Genuine root-CLI
and raw-handler checks passed. See the 08B handoff for precise evidence.

Owner review correction: the checked-in template example now selects only its
template ID. The earlier additional culture/message filters demonstrated a narrow
refinement, not template breadth. Corrected genuine CLI exports show 202 selected
identities / 396 occurrences, retaining separate messages and visible Run counts.
The handoff records output agreement and the corrected verification-parser issue.

[Working handoff](TASK08B_REPORTING_HANDOFF.md) records the implemented root CLI,
five preset definitions, structured refinements, text/JSON/offline HTML and linked
verbose appendix. Both 08A services and completed traversal-scope repair were
received. Bounded gaps were resolved in their owners: stored reference presence,
per-Run/window association ranking data, candidate provenance, readable partial
matches and an opt-in optional context mode for SQL-reference queries. No new
storage path, worker, source recognizer or statistical baseline was introduced.

All eight real-data CLI groups passed in the final run; six diagnostic and nine
source checks were actually rerun. Four-Run source chronology, all-candidate
composition, exact/template/message distinctions, both syntax statuses, newness,
historical absence, error partials, display limits and format/appendix agreement
are exercised. The first three failed checks and corrections are disclosed in the
handoff. Naturally unavailable reads/roots and full windows
remain unverified. Browser visual layout could not be checked in this environment.

Jinja2 installation was blocked by the environment. The explicit delivered
alternative is standard-library escaped elements with packaged HTML/CSS; no new
dependency or silent runtime renderer fallback. Ordinary reports remain reusable
library consumers. Prompts were not rewritten; no new product requirement,
production operation, commit or push was added. Trusted Run acceptance is separate.

## Advisor reconciled 08B receiving instructions — 2026-10-03

Following owner-requested review of the multi-Run handoff,
[08B's prompt](TASK08B_PROMPT.md) now receives the completed source-scope repair,
actual counts/fractions and included-window newness. Deleted median/notability
fields and `QueryEvidenceError` are no longer consumer requirements. No replacement
statistical rule was added. Verification guidance now identifies the four-Run
upstream evidence and its remaining limits. Other task scope is unchanged.
[Review](TASK08B_RECEIVING_REVIEW.md): source/document inspection only this turn;
upstream checks were not rerun. Earlier statements that prompts were unchanged
describe the delivering team's handoff, before this advisor reconciliation.

## Scope clarification and repair delivered — 2026-10-03

The owner accepts all-root defaults for **unscoped** searches only. My previous
broader acceptance statement was incorrect. Member/root filters apply before
disk probes, directories constrain traversal, and exact files/references now
derive nonrecursive parent scopes before enumeration. Filename-only/basename
searches traverse the selected scope to find that name; no member/directory
restriction is ignored. Genuine 41-comparison scope and 93-comparison four-Run
integration verification passed. The handoff delivers the completed repair to
08B; no prompt was edited and no new requirement was introduced.

## Default root inventory accepted — 2026-10-03

Owner accepts enumeration of all selected roots as the default and requests code
documentation. Without root/member filters these are the selected Run's recorded
playset roots; without directories traversal covers the roots. File/reference
filters apply afterward. Explicit scopes remain effective. SourceSearch docstrings
now state this behavior and path-inventory reuse. No runtime change or prompt edit.
This supersedes earlier default-traversal defect/mandatory-repair classifications;
the 08B receiving handoff records the change.

## Completion accountability — 2026-10-03

The restored prompts remain the assignment baseline, qualified by subsequent
owner instructions. [Requirement reconciliation](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md)
records the delivered code/evidence and the original median/notability requirement
changed after owner review. The known-path traversal correction remains an open
08A.2 source-scoping obligation; assigning it to 08B does not remove or complete
that obligation. Do not infer full acceptance from the passing explicit-directory
queries or the older “delivered” headings. No prompt was edited in this review.

## Owner correction: actual counts and included-window newness — 2026-10-03

New means present in the selected Run and absent from every preceding Run
actually included in the comparison window. Successfully read predecessor
counts decide the answer; unavailable reads do not veto it. No included
predecessors means positive records are new within that window.

The owner rejected the median-based comparison. Removed median/baseline result
fields, derived notability labels and the novelty-unavailable exception/gate.
No replacement statistic or threshold was commissioned. Counts, observation
fractions and exact identity remain the consumer evidence. The public handoff
records the correction and required 08B consumer changes. Median/newness edits
to the task prompts were restored per owner direction; do not silently rewrite
another team's assignment. The owner correction supersedes earlier formulas below.
[Verification](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md): 18 genuine investigations,
359 data comparisons and two genuine single-Run checks passed without changing
the evidence. No failed check or new requirement in this follow-up.

## Genuine short-history acceptance and template clarification — 2026-10-03

[Verified results](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md): four eligible Runs
now exercise default/trailing history, exact recurrence and notability, and
source filtering against each recorded playset. Seventeen investigations and
340 genuine-data comparisons passed without changing the backup or runtime code.
The earlier chronology blocker below is historical; unavailable real cases remain
explicit evidence limits. Five eligible Runs are not a prerequisite.

Owner clarification: selecting templates means selecting one or more stored
ingestion-time template references, ORed across diagnostic records. Message
search examines whole rendered content including every slot value. Verification
and consumer examples must use these operations; template wording is not a
substitute for either. Source-filtered totals exclude nonmatching identities;
exact-identity recurrence retains original counts. No new requirements were added.

## Genuine existing-history receiving check — 2026-10-02

[Verification handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md): the configured
database's 14 real Runs all lack the required source timestamp. Zero are eligible;
default/trailing windows and temporal analytics cannot be verified from this
unchanged history. No substitute clock, fabricated history or backfill is allowed.
The owner was asked for another existing database if that was intended.

Real component checks over all 14 public-handler reads passed: definition-scoped
exact counts, differing source bindings, template/message filters, and mod/file
candidate memberships using recorded playsets. Source-filtered totals deliberately
differ from unfiltered totals; excluded identities contribute nothing. These do
not claim a successful chronological investigation. The backup stayed byte-identical.
No runtime redesign or new test-derived requirement was introduced.

## 08B receiving decision — 2026-10-02

Launch [08B](TASK08B_PROMPT.md) with the known 08A.2 traversal-scope correction
as its first bounded repair in the owning source library. The libraries and their
integration are delivered; the correction remains open. Receive actual query,
resolver and partial-result APIs, implement the delivered syntax selectors, and
use only genuine acceptance evidence under the current owner policy. The advisor
reran all 15 genuine checks successfully; no multi-Run or missing failure evidence
was invented. See [the receiving review](TASK08B_RECEIVING_REVIEW.md).

## 08A.2 implementation decisions and delivery — 2026-10-02

Owner memory/scope review: narrower user requests must not trigger broader
enumeration to populate a cache. Measured full inventory: 105,603 entries /
11.54 MiB; the known path's parent-directory inventory: 433 entries / 96 KiB.
For all real references, only 454 distinct paths / 120 parent directories are
needed; parent-only inventories retain 2.68 MiB and the same 495 root/file pairs.
Direct path checks are another measured option, with no inventory but 60,382
filesystem checks across all roots/references. See the 08A.2 handoff's memory
review and ignored `memory/MEMORY_REVIEW.md` beneath `.codex-tmp/task08a2/`.
No runtime change was made by this review. Directory constraints must be applied
before traversal when completing this receiving improvement; a cache is not a
reason to widen scope. No persistent/growing cross-query index is recommended.

Owner follow-up: every mod displayed in a report must visibly include its stored
load-order number, including source-excerpt headings. Preserve stored numbers;
sorting alone is insufficient. For roots outside the recorded playset, label
recorded load order unavailable. The readable evidence report, 08A.2 handoff and
08B prompt now carry this presentation requirement.

[Delivered handoff](TASK08A_2_SOURCE_SEARCH_HANDOFF.md): `SourceSearch` implements
the 08A.1 batch resolver, independent-root search, recorded-member provenance and
excerpts. Source predicates compose with existing SQL/template/exact selectors.
08B receives the combined library; no report/CLI was added in this delivery.

- Ripgrep 15.2.0 was already available. It supplies isolated-config, structured,
  streamed literal content searches in Windows-sized batches. No installation
  or Python dependency was needed. Standard-library traversal, pathlib/fnmatch,
  existing validators and one shared Boolean evaluator supply supporting work.
- Path globs explicitly use fnmatch's ordinary-slash semantics. No custom glob
  engine, persistent index, resident service or new worker was introduced.
- Inventory reuse preserves member/caller-root order and every candidate.
  Stored references retain region/slot/line evidence. Supplied relative paths
  are honored; basename expansion requires an explicit option.
- Optional source context does not change SQL totals. Required incomplete
  source filters retain known partial matches and fail explicitly. Candidates
  remain possible current locations, without ownership or historical claims.
- Nine new real-data checks and six existing real-data checks passed, no
  failures/skips or synthetic/fault-injection checks. The representative playset
  has 133 roots / 105,603 entries; content search covered 11,914 text files.
  2,651 candidate associations preserve 2,475 diagnostics / 4,182 occurrences.
- Unreadable-root, decoding, process-error and multi-Run cases were not present
  and were not fabricated. The handoff lists these limits and the early console
  inspection error/provenance correction. No extra product requirements arose.

Human-readable filters/returns/excerpts remain outside Git at
`.codex-tmp/task08a2/SOURCE_SEARCH_REAL_DATA_REPORT.md`. Current 08A.2 delivery
supersedes the older pending-source statements below; production state is unchanged.

## 08A.1 implementation decisions and delivery — 2026-10-02

[Delivered handoff](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md): `ck3chronicle.reporting`
owns the structured query, handler-only reads, stored rendering, chronology,
exact recurrence/notability and totals. Following owner review, verification is
limited to six passing genuine-data checks; 12 synthetic/scalar and two injected
reporting checks were removed. 08A.2 and 08B remain next.

* Record/template predicates share one literal AND/OR evaluator. Matched-template
  references are OR lists. Template text is derived from stored body parts with
  literal/placeholder text, independent of bound values; no model import occurs.
* Full contract equality data plus the stored definition revision scopes exact
  identity. Historical entries preserve their originating record references and
  have selected count zero; occurrence refinements remain selected-Run based.
* Eligibility precedes pagination. Missing/unusable timestamps are excluded and
  disclosed. Standard datetime supplies
  chronological ordering, with original strings retained and no nanosecond system.
* Source extraction belongs to 08A.2, including referenced-path interpretation.
  The shared query reserves explicit roots/files, optional members and referenced
  paths. These filters fail clearly until its batch resolver is supplied. Generic
  file/candidate rollups already preserve unique diagnostic totals and disclose
  overlapping buckets; actual source integration must be verified by 08A.2.
* Incomplete required source filters retain partial evidence in an exception.
  Unavailable novelty filters likewise cannot become successful empty queries.
  Ordinary read failures remain errors or disclosed unavailable comparisons.

No dependency was added; the library reuses contracts, HandlerClient, built-in
literal/casefold operations, `statistics.median`, dataclasses and 07E logging.
The genuine SQL exercise contains one eligible Run. Multi-Run recurrence,
disappearance and threshold boundaries remain unverified by genuine data.
The owner rejected synthetic reporting checks as acceptance evidence: do not
reintroduce them or promote their scenarios into requirements. The owner also
directed deletion of the seven-check synthetic logging suite. The arbitrary
32-level nesting cap is removed; no test-specific error branches were found in
reporting. Documented handler-error handling remains part of the assigned task.
No production changes or live acceptance are claimed. This section
supersedes earlier entries that describe all split tasks as only prompts.

## Current source-search and receiving clarification — 2026-10-02

Source searches are not restricted to playset membership: callers may supply
explicit source roots. A Run's recorded playset remains available for member
selection and default report context. Source-content AND/OR predicates apply
at file level, and unreadable evidence required by a source-association filter
produces an explicit evaluation error with any known partial matches marked
incomplete. It never becomes a silent non-match or exact zero.

08A.2 requires ripgrep configuration isolation, structured output, distinct
matches/no-match/error handling, actionable missing-executable errors and actual
Windows invocation verification. 08B receives both split prompts and handoffs
and starts after both deliveries and query/source integration are complete.
The owner's session-end timestamp wording remains unchanged. The timestamp and
mandatory-playset recommendations have been removed from the separate review.


## Current owner revision — 2026-10-02

Use [08A.1](TASK08A_1_PROMPT.md), then [08A.2](TASK08A_2_PROMPT.md), then
[08B](TASK08B_PROMPT.md). All belong to Reporting and Analysis. Their baseline is
the owner's updated Downloads prompts. The split adds responsibility/receiving
boundaries and requested search-library guidance only. The older chronology
precision/tiebreak and source-observation wording below is superseded by those
updated prompts; it must not override them. See [the split review](TASK08_SPLIT_REVIEW.md)
for the change account and recommendations left unapplied. Implementation is not
claimed. The earlier ledger below is retained as historical context.


2026-09-30. Advisory decision ledger, not an implementation prompt.
The former TASK08_PROMPT.md is superseded as a scope proposal; do not issue it.

## Current assignments

Both tasks belong to the **Reporting and Analysis team**. Executable prompts are
prepared, not implementation deliveries:

| Task | Assignment | Status |
|---|---|---|
| [08A](TASK08A_PROMPT.md) | Reusable investigation queries, exact history/notability, recorded-playset search and excerpt data | Prompt prepared; execute first |
| [08B](TASK08B_PROMPT.md) | Report presets, root CLI, HTML/text/JSON and linked source appendix | Prompt prepared; execute against 08A's delivered handoff |

Pipeline retains ownership of database/handler contracts; watcher retains capture
and playset production; learner retains parser/matcher/model work. Reporting
consumes those boundaries. The [syntax research handoff](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff)
now supplies nine explicit package-scoped selectors, genuine examples and
exclusions for review when building that preset. It excludes unverified
brace-balance formulations and context-dependent messages from the initial syntax
set. This is research delivery, not reporting implementation.

### Drafting rationale — outside the executable assignments

Writing 08B exposed the need for 08A to include previously observed identities
whose selected-Run count is zero. Otherwise an analysis starting only from the
selected Run's rows could never show disappearance. These remain comparison
entries with their original Run references; no SQL records are manufactured.

The prompts also make filtering independent of presentation limits and candidate
counts: a diagnostic matching several files must not multiply report totals.
Source excerpts are library data before they become appendix links. This keeps
a future NiceGUI adapter from having to rebuild analysis/search behavior.

Routine interface choices in these drafts include a structured query file for
grouped filters, two CLI operations (`runs`/`report`), and a disclosed stable
Run-ID tiebreak for identical source timestamps. They are implementation direction,
not claims about previously delivered behavior or additional temporal evidence.

This advisory pass inspected current handoffs and focused contract/repository,
request-handler and playset source. It prepared documentation only; it did not
rerun delivery checks or inspect the live database/process state.

## Owner direction

- Split work into 08A (reusable investigation capabilities) and 08B (reporting,
  presentation and integration). Define report journeys before finalizing 08A APIs.
- Use generated HTML reports, linked source appendices and CLI/JSON initially.
  Keep query, analysis and result objects independent of presentation so a later
  NiceGUI interface can call the same services. No GUI installation is commissioned.
- Recurrence means the same exact diagnostic content and template matching,
  following existing exact aggregation semantics. No fuzzy recurrence or alternative
  pattern-group recurrence has been approved. Report rollups do not redefine identity.
- Order reporting Runs by `run["facts"]["error_log_source_modified_at"]`, the
  original input error.log modification time validated during stable capture.
  The delivered format is UTC ISO with nine fractional digits and `+00:00`.
  Preserve that precision when ordering. Exclude Runs without that data; no
  capture-time, process-start or processing-time substitution and no backfill.
- Reports and recurrence windows stay within the selected processing package.
  Select up to five preceding eligible Runs using the agreed timestamp. Fewer
  than five does not block a report: show the actual history count, use available
  observations for the median, and show no baseline when none exist. Cross-package
  comparison is not commissioned; no equivalence machinery is required.
- Initial presets: script/file hotspots, frequent diagnostics, syntax-related
  diagnostics, newly observed diagnostics, selected symbol/template investigation.
- Add multiple free-text message include/exclude conditions with AND/OR grouping.
  Use literal matching with explicit groups, case-insensitive by default and an
  explicit case-sensitive option. No arbitrary expression evaluator is needed.
- Source context is sought by default using the selected Run's recorded playset.
  Return all source candidates in recorded order, including base game/DLC entries
  where accessible. Support member/directory/extension filters and recursive,
  exact/partial filename and content searches. Never stop after the first candidate.
- Verbose reports link to an appendix with the referenced line and ten lines
  above/below for each candidate. Source contents are current observations, not
  claimed historical contents. No winner, blame or effective-state resolution.
- Include up to five preceding and five subsequent Runs. Do not exclude Runs
  because playsets changed. Correlating playset additions/removals is later work.
- Use an in-memory search inventory/reused reads first; persistent indexing is
  conditional future work based on actual need.
- The separately commissioned [syntax-diagnostic research](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md)
  is available. Reports consume its concrete verified selectors;
  cascade/root-cause inference is excluded.
- Repair-commitment verification and mod-file change correlation remain separate
  follow-ups, potentially within the MVP. Audit is excluded from 08A/08B unless
  the owner explicitly reintroduces it.
- The owner reports separate reconstruction verification succeeded after excluding
  unwanted timestamps/ordinality. No further reconstruction investigation is assigned.

## Owner's notability thresholds

| Reference occurrence count (preceding-window median) | Notable increase | Notable decrease |
|---|---|---|
| Greater than zero, below 10 | At least tenfold | Reaches zero |
| At least 10, below 200 | At least 100 additional occurrences | Reaches zero |
| 200 or more | At least 60 percent | At least 60 percent |

The owner selected the selected Run's count versus the median of the preceding
five Runs. Interpret 200 as belonging to the high band; medians may be fractional
when fewer observations are available. These are reporting thresholds, not
severity or proof of cause/fix.

Use up to five available eligible preceding observations and show the denominator;
count verified absence as zero,
but not unavailable/incomparable observations. No observations means no baseline.
A zero median does not establish that every preceding count was zero. Label a
diagnostic newly observed in the window only when it is absent in every comparable
preceding Run; otherwise describe an increase above a zero median without an
infinite percentage. Subsequent five-Run counts remain part of historical-Run
reports; a separate future-window notability formula has not been selected.

## Source-inspected receiving facts

Three retained error-log starts and one paired debug-log start were inspected.
Their native headers contain HH:MM:SS without calendar date/timezone. The selected
parser's header pattern likewise reads time-of-day. The first error is not a
session-start declaration. This is inspected evidence, not a claim about every log.

`watcher.ProcessIdentity.started_ns` captures Windows process creation as Unix
nanoseconds where available. CLI capture metadata preserves it under `process`;
ingestion passes that metadata into SQL Run `facts`. Thus process-start facts
already have a storage route. `observed_started_at` can be watcher attachment time
and must not be presented as actual process start. Manual inputs may lack both.
These process-start observations do not supply the owner's chosen reporting
timestamp and must not be used as a substitute. Repository `list_runs`/`latest_run`
currently order by processing time. No live database was opened for this assessment.

A processing package is the pinned parser/matcher/model combination, not a game
mod. The owner has now chosen selected-package reporting. Earlier proposals for
cross-package comparison or definition-equivalence checks are superseded.

## Confirmed receiving contract

The owner returned watcher and pipeline confirmation on 2026-09-30. Read
`docs/WATCHER_SOURCE_MTIME_HANDOFF.md` and the source-modification-timestamp
section of `docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md`.

The source fact travels through capture-metadata.json to SQL runs.facts_json and
is returned unchanged by HandlerClient get_run/list_runs/latest_run/
find_run_by_log_hash as `run["facts"]["error_log_source_modified_at"]`.
Example: `2026-09-28T04:44:46.950967600+00:00`. Fixed-format UTC strings preserve
chronological ordering directly; do not round to microseconds or floating point.
Existing Run listing still orders by processing time, so report chronology must
explicitly use this fact. It does not change Run IDs or raw-retention clocks.

Pipeline reports two passing focused disposable checks for public read precision
and conflicting duplicate metadata preserving the accepted Run. Watcher reports
43 checks. This advisory pass read their handoffs, not reran their tests. The
watcher handoff leaves live activation separate; source delivery alone does not
establish which code a live process has loaded.

The timestamp prerequisite is resolved for task specification. New eligible
history accumulates going forward; neither task execution nor ordinary reporting
requires five existing eligible Runs. Older Runs lacking the field stay excluded.

## Interface direction for 08A / 08B

08A owns structured filters, playset/file search, excerpt data, exact recurrence
and analytic results. 08B owns report presets, presentation and appendix links.
UI adapters must call those services rather than implement their own analysis.
This makes adding NiceGUI later additive, although the interactive UI itself
would still require implementation and verification.

General query-builder libraries exist, but simple contains/not-contains rules
combined in AND/OR groups need only a small explicit evaluator. A visual builder
can later emit the same structured rules. No SQL-string or Python-eval interface.
