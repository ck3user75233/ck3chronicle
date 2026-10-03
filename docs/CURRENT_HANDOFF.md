# Current handoff

## Canonical logging planning handoff — 2026-10-03

The owner supplied an execution-journal design using actual code identities,
bare source-position checkpoints and optional caller-owned counts. Read
[CANONICAL_LOGGING_SYSTEM_V1.md](CANONICAL_LOGGING_SYSTEM_V1.md) and
[TASK09A_PROMPT.md](TASK09A_PROMPT.md). The latter commissions a plan only;
`CANONICAL_LOGGING_V1_IMPLEMENTATION_PLAN.md` is its future deliverable, not a
completed artifact. Earlier learner phase-logging prompts are superseded.

Advisor source inspection confirmed the shared logger's config import and existing
release-mapping seam. `derive_pattern` is defined in `patterns.py`; registry
`paths_seen` increments before processing, so placement must preserve honest
completed counts. No runtime code changed or campaign ran. Source-preservation,
immutable-candidate and bounded rollback guidance is in 09A. The
[incoming briefing](ADVISORY_HANDOFF_TRUSTED_RUN.md) proposes learner-first adoption
and separate consideration of runtime conversion; owner decisions remain open.
The agreed 08B prompt is untouched. Ongoing locator work below remains independent.

## Disposable combined locator experiment — 2026-10-03

The owner now explicitly authorizes implementing/testing BOTH marker/Unknown
recognition and count-independent trailing locators in a disposable candidate,
using genuine ingested data. This supersedes the review-only/design-paused
boundary below, but does not authorize production registration, pinning,
replacement of stored Runs or runtime restarts.

Completed disposable experiment: v48 adds a repeated location-entry part (schema 6 / matcher API
v3) inside the existing body. `location_sequences.py` recognizes complete trailing
Script location / Stack trace sections; actual entry layouts come from genuine
members. Marker literals remain outside the repeated part; all file/line LOCATORs
and trace PARAMs expand into individually named ordered captures. Selection,
rendering and exact identity retain per-occurrence layout choices and values.
The parser, source records, deduplication key and cross-emission recovery are
unchanged. `pipeline/contracts.py` renders the new declared layout without
performing recognition; existing production definitions still render normally.

Ignored experiment: `.codex-tmp/locator-marker-candidate/`. An unchanged database
backup was read through its own HandlerClient: 18 genuine Runs, 48,772 diagnostic
records / 766,476 occurrences. Seventeen logs match retained inventory hashes;
all 18 Runs can be tested from stored definitions and values. Build uses the
corrected 20-log set, including IS3QON and the rare house_head witness. Only
IS3QON among the stored Runs belongs to that training set.

The earlier marker-only build failed because model validation still demanded a
numeric LOCATOR for line-label alternatives; the failure log/release/receipt are
retained with `marker-only-` prefixes. The combined source removes that stale
condition. A second attempt was stopped to remove repeated deep copying of large
inference metadata; another failed on a stale fixed-field lookup for dynamic
trace captures. Their logs/releases are retained with `aborted-count-` and
`count-integration-failure-` prefixes. Both defects were corrected before the
successful immutable build. Do not describe the earlier attempts as successes.

Successful candidate `56d4dbeca2c0da99a25a0d85`, published model
`e36f6ce8aa9803738d5b6237`, disposable package `4c2069e688e0a62d82222838`;
manifest SHA-256 `60bf1616772fd49fbd83a7b383a8f1a75772fa515e1dbcebc033d3b2d3267fd3`.
Frozen learner release `77d04126bfa24d588ed49bc9a5c968a40dcd02115365958cab4e472d48cfb1dc`
has completed learn and publish execution receipts. Training/export replay covers
731,529 messages: 600,244 template, 131,285 provisional, zero unmatched. Export
checked 191,357 captures with zero changed assignments/outcomes. Runtime logging
ownership and scoped whitespace checks passed.

Stored-data comparison against the same-20-log v46 package: 766,476 occurrences,
1,376 no_match -> template, 171 provisional -> template, 4 template -> provisional,
56 still unmatched, and no complete match lost. All selected native regions
reconstruct exactly; existing locator captures and distinct message identities
are preserved. Thirty occurrences now capture explicit Unknown as LOCATOR.
The four status reductions use two one-example provisional effect definitions
instead of the old two-example generic KEY-effect definition; there are no
capture/selection ties. They are disclosed, not silently called an unqualified
improvement. Genuine wrappers and the hardcoded history continuation still
recover the same messages and captures.

Genuine 1/2/3-entry scope examples share template `0213bb363ad56f39d7e953a5`,
retain 2/4/6 individual LOCATOR captures, and have distinct identities. Full
original IS3QON capture replay yields 59,168 template + 145 provisional, zero
unmatched: scope mismatch now supported; both travel messages remain provisional
with literal bodies. Date equivalence / reusable short character identity are
not implemented by this locator experiment. Parser v1.7 remains unchanged,
including its numeric recovery predicates; no genuine nonnumeric near-line
example was available to verify that recovery path.

Owner requested a human-readable delta report: `CHANGES.html` includes 15 new
definitions, 15 removed definitions with observed replacements, 15 previously
unmatched stored-message examples and their new assignments, plus the three
original production no_match diagnostics. Inventory changes: 381 -> 283 total,
144 unchanged IDs, 139 new IDs, 237 removed IDs. These are definition identities,
not counts of wholly new/lost error families. `changes.json` retains observed
crosswalks; `RESULTS.html` / `verification.json` retain full verification and the
56 unmatched occurrences. Replacement observations cover stored Runs, not an
exhaustive semantic-equivalence proof for every removed definition.

Production selection/catalog hashes, all training logs and the read-only backup
are unchanged; no production package registration, activation or runtime restart.
Research drivers: `location_candidate_experiment.py`, `verify_location_candidate.py`,
`report_locator_candidate_changes.py`. Generated artifacts remain ignored.

Latest numeric-gate clarification: `line:` and `near line:` identify location
fields; numeric content is not a prerequisite for LOCATOR recognition. All
255,228 near-line mentions in the 104-log inventory have numeric values; no
nonnumeric counterexample was found. Do not present that observation as grounds
for retaining a numeric gate. Prior cautions below about not silently changing
recovery do not authorize treating the old numeric predicate as a requirement.
Preserve established message boundaries while correcting marker/value handling.
The actual locator contents continue to count toward exact message identity.

Latest owner identity clarification: exact locator contents and count DO count
toward error-message identity and deciding whether two instances are occurrences
of the same message. Only classification similarity ignores those values/counts.
Preserve all ordered values and do not use a locator-neutral comparison view as
a deduplication or occurrence-aggregation key. Different locations can share one
template while remaining distinct messages. Guidance and HTML review updated;
no executable behavior or stored identities changed.

Latest continuation double-check: Unknown normally remains literal; only its
immediate value position after a recognized location marker permits LOCATOR
typing (`line:` and `near line:` included). Do not change recovery boundaries
as a side effect. A complete 104-log audit using the recorded package's verified
parser is at `.codex-tmp/location-variability-review/continuation-overlap.json`;
the HTML review includes every existing structure and native examples. Current
parser bytes and continuation declarations equal the recorded package; the
corrected v46 candidate has the same parser/declaration too.

Only `history-colon-title-list-v1` joins separate timestamped emissions: 11 groups,
13 title entries, no inventoried location markers in any group. Existing local
recovery overlaps location-bearing messages: 1,837,757 script-error emissions
(including all 9,055 Script location: Unknown occurrences), 87,346 quoted reader
wrappers yielding 167,882 messages, 244 participant forms with file/line in the
opening and Cheater:/With: following it, ten From forms, and six Stack trace forms.
All except reader wrappers remain one message per emission. Other multiline
envelopes are scope context (15), formatted reason (13), and quoted multiline
value (7); no inventoried markers observed there. Single-line recovery and one
unresolved unit complete the inventory. Every one of 3,344,830 original emissions
was consumed exactly once, yielding 3,425,352 messages, matching the earlier census.

Current implementation: reader wrapper recovery requires numeric near-line values; file/line envelopes
also require a numeric line. Unknown is currently accepted specially only after
Script location in that envelope. These are implementation facts, not required
numeric recognition gates (superseded by the clarification above). No genuine
Unknown-after-line witness was found. Preserve shared wrapper context, ordered history title components,
and whole script-error bodies while designing repeated locator storage.
Research helper: `tools/template_learning/review_continuation_location_overlap.py`.
Only research tooling, guidance and ignored reports changed; no executable
parser/learner/matcher rules, model release or production state changed.

Latest owner clarification: retain location markers (e.g. `Script location:`) as
literals; following entry count contributes no dissimilarity or grouping veto.
Store all actual file/line LOCATORs and trace PARAMs in order. An explicit Unknown
in the location-value position is itself one present LOCATOR value, not literal
wording, an absent location section or SQL null. This supersedes the September 27
literal-Unknown rule. Current guidance/model-contract documentation records the
new requirement; executable rules and production packages still have the old
behavior. Continue the review before implementing the representation change.

The marker inventory is complete over the same 104 logs:
`.codex-tmp/location-variability-review/location-markers.json`. Among the probed
location labels and unavailable-value spellings, only `Script location: Unknown`
was observed as an explicit unavailable value (9,055 mentions). Other observed
section markers include `location:`, `From:`, `Stack trace:`, `New Location:` and
`Previous Location:`; file/line aliases and Database were also inventoried. These
are physical marker counts, not new recovered-message classifications or an
exhaustive grammar. Empty filenames are separate evidence, not Unknown values.
`unknown-current-behavior.json` confirms an actual recorded-package provisional
assignment with REASON only and no LOCATOR capture for Unknown. The HTML report
now distinguishes the new required typing from the older positive file/line-entry
census. Current implementation still requires correction; no model was released.

Follow-up: the owner emphasizes that fixed counts after an existing recovery split
do not establish fixed counts in original emissions. Continue using recovered
messages for the variability census, and reserve existing recovery forms for
manual comparison with the problem case. `recovery-examples.json` now retains
original and recovered examples: the 1/2/3-entry scope-mismatch witnesses each
remain one `script-error` message, with 2/4/6 body LOCATOR fields; a genuine reader
wrapper becomes two messages; a genuine history continuation combines three
emissions into one message with two attached title entries. The HTML review now
shows these distinctions. No additional full-corpus pass or model change was needed.

The owner paused the proposed repeated-location correction to first measure
variability within the **same diagnostic template wording/slot pattern**, allowing
slot values to vary. The final requested unit is **recovered error messages**,
not original emissions. Original emission provenance remains available for review.
Neither a repeated-entry representation nor splitting one message into several
has been approved by this investigation; do not implement either based on the
earlier proposal. Leading date-literal equivalence remains pending separately.

Read `.codex-tmp/location-variability-review/REVIEW.html` and `incidence.json`.
All 104 retained distinct logs were examined: 3,344,830 original emissions,
3,425,352 recovered message occurrences, one unresolved recovery unit. Comparing
exact existing literal/slot prefixes before complete trailing location lists
finds 66 overlapping variable-count patterns, all from
`jomini_script_system.cpp:303`. They cover 1,828,067 message occurrences counted
once, including 596,837 with multiple entries. They are measurement groups, not
66 independent error families or newly accepted complete templates. References
are the original recorded package and the isolated corrected v46 20-log candidate;
the latter supplies the general three-KEY scope-mismatch opening. The original
package's behavior is unchanged.

That scope-mismatch pattern has 77 occurrences across 29 logs: one with one
entry (story_owner), one with two (war), and 75 with three. A separate Stack trace
form from `jomini_effect_impl.cpp:495` occurs six times, always with two entries;
no count variability was demonstrated there. The reader supplement records
329 expanded-from annotations across Unexpected token / Unknown trigger /
Unknown effect, including 48 empty filenames. These add literal annotation wording
and are not silently equated with a freely repeating trailing list.

Research tools: `tools/template_learning/investigate_message_location_variability.py`
and `report_message_location_variability.py`. All output is ignored. Counting
agrees with the earlier 73-log detailed location inventory on 1,165,336 native
message occurrences / 1,807,351 entries, with zero differences. No learner/matcher
algorithm, parser, package selection, source log, stored Run or runtime process
was changed. The next step is owner review of the incidence and native examples,
before deciding whether or how to change message boundaries or representations.

## Corrected rare-case 20-log experiment — 2026-10-03

[Evidence-selection correction and results](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md).
The first v46 training set excluded the three original diagnostics and house_head;
IS3QON was only evaluated afterward. That was insufficient for the target question.
Execution receipts nevertheless confirm the changed v46 code ran.

Rebuilt frozen v45 and v46 on the same corrected 20 logs, explicitly including all
rare witnesses. Both yield complete provisional assignments for war and the two
travel errors, and a full shared assignment for house_head. All selected assignments
and captures agree on 731,529 messages. Travel identities/dates and war's scope text
remain singleton literals; these are not solved reusable formulations. Eight
alternative IDs differ. No additional learner implementation change was made.

Review artifacts: `.codex-tmp/learner-v46-targeted20/RESULTS.html`. The exported
candidate and read-only pipeline checks passed; production remains unchanged.
Continue from these corrected results, not the earlier missing-target experiment.
Keep the existing review boundary for further recognition/location-stack changes.

## Known-path source-scope repair delivered — 2026-10-03

[Latest receiving delta and evidence](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md):
unscoped default is all recorded-playset roots; supplied scope must narrow work.
SourceSearch now selects members before disk probes and derives nonrecursive
parent scopes for known paths. Explicit directory restrictions remain effective.
41 genuine scope comparisons and four multi-Run source investigations / 93
comparisons passed, preserving candidates and counts without a directory workaround.
08B receives this completed repair; do not repeat or replace it. Prior blanket
default-acceptance and open-repair notes below are historical. Prompts unchanged.

## Default inventory behavior accepted — 2026-10-03

Owner accepts default enumeration of all selected recorded-playset roots.
Code docstrings now explain that omitted directories mean whole roots; filenames
and references filter afterward; explicit roots/members/directories narrow scope;
inventories contain paths and are reused within the investigation. No runtime
change. [Receiving clarification](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md) supersedes
the automatic-narrowing defect/open-repair classification below. 08B should
document the accepted default and retain explicit controls. Prompts were not edited.

## Do not claim unconditional 08A completion — 2026-10-03

[Requirement-by-requirement reconciliation](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md)
separates delivered capabilities, owner-directed median/newness changes, genuine
verification limits and the open 08A.2 known-path traversal defect. Assigning that
defect to 08B does not fulfil the original source-scoping requirement. The latest
passing source queries explicitly supplied directory scope; automatic narrowing
is still outstanding. Prompt edits were restored and no prompt was changed by
this reconciliation. The prior blanket completion wording was too broad.

## Included-window newness correction complete — 2026-10-03

[API changes and checks](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md). Newness is
selected count positive and no observation in any included predecessor. Removed
the unavailable-read veto/`QueryEvidenceError`, median/baseline fields and derived
notability labels. Counts and fractions remain; no replacement formula was added.
Consumers must use `history.newly_observed` and actual `history.counts`.

Reverified the unchanged four-Run backup: 18 investigations, 359 comparisons,
zero mismatches, plus two genuine single-Run checks. Logging/imports/pip passed.
Current report: `.codex-tmp/task08-multirun/WINDOW_NEWNESS_REPORT.md`.
Evidence: `.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/presence-review/`.
No synthetic checks, runtime failure special cases, added dependency, production
write or new requirement. The verification handoff lists the required 08B
consumer changes. Median/newness edits to task prompts were restored per owner
direction; future receiving changes belong in the handoff. The separate
automatic traversal-scope correction remains open.

## Genuine timestamped history validated — 2026-10-03

[Verification results](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md) supersede the
earlier blocked outcome: four eligible Runs in package `68f1ae5db205ab46afef9c4d`,
17 completed investigations, 340 actual-data comparisons, zero mismatches.
Unchanged backup/evidence: `.codex-tmp/task08-multirun/2624478c0021411d861144eaff16e3c6/`.
Readable queries/results: `.codex-tmp/task08-multirun/TIMESTAMPED_MULTIRUN_REPORT.md`.

Latest `20261003-74G2EB` has three eligible predecessors. Whole-message
`failed context switch` returns 51 diagnostics / 245 occurrences; the exact
sea_minority file scope returns 2 / 64 and selected EB+EC724 mod returns 15 / 84.
Each Run's filtered identity/count maps and recorded members were verified.
Stored template references select ingestion assignments with OR; no template
wording search substitutes for whole-message content including slot values.

No runtime changes or new requirements. No synthetic data or failures.
One premature report-generation command failed, then succeeded after the final
integrity evidence was written; data comparisons all passed. Logging/imports/pip
checks passed. Failed-read/duplicate-timestamp/unavailable-source cases remain
unexercised. Continue 08B separately; its known traversal-scope repair is still open.

## Learner v46: approved changes and fresh 20-log candidate — 2026-10-03

[Results and continuation boundary](LEARNER_V46_QUOTED_DISCOVERY_RESULTS.md).
Implemented quoted-content-neutral discovery and one batch per identical-template
identity after the existing regrouping sweep. Threshold .72 and inference/matching
guards remain. Fresh 20-log build completed in 211.85 seconds; all 671,898 selected
assignments and capture bindings match the same-input v45 baseline. Seven unused
alternative definitions change; review details are in the ignored HTML report.

Candidate/package and authenticated learner release live only under
`.codex-tmp/learner-v46-20logs/`. Export validation checked 153,431 captures and all
35,362 contextual messages. Production catalogs/pin/processes/Runs/logs are unchanged.
All three original IS3QON diagnostics remain unmatched in this limited 20-log model.
No 104-log rerun or production activation was performed. Review this candidate
before deciding the next corpus/classification step; preserve the prior investigation.

## Genuine multi-Run verification — timestamp prerequisite absent — 2026-10-02

[Latest verification handoff](TASK08A_MULTIRUN_VERIFICATION_HANDOFF.md).
Configured current database: 14 genuine Runs / package `68f1ae5db205ab46afef9c4d`,
38,269 record rows / 683,608 occurrences, but **no Run has the required source
timestamp**. All 14 exclusions and explicit/latest selection failures were
verified on an unchanged disposable backup through `HandlerClient`.

The requested chronological acceptance is incomplete. Do not use Run IDs,
processing times or capture times as an alternate order; do not backfill facts.
An existing database with eligible timestamped history is needed. The owner was
asked whether another database was intended. Readable report and precise queries:
`.codex-tmp/task08-multirun/MULTIRUN_VERIFICATION_REPORT.md`; full evidence/backup:
`.codex-tmp/task08-multirun/049e5d1d395f4ad6b31008f177e9edab/`.

Real source/identity components were independently checked across all 14 Runs,
using each recorded playset. Their expected/actual filtered counts agree and
exclude out-of-scope identities; raw exact counts remain separate. 253 actual
data comparisons had no mismatches. No runtime changes were needed by those
checks. No synthetic evidence or new requirements were added. The ignored report
generator had one string-literal error, corrected before producing the report.
Logging ownership/imports/pip check passed. Only documentation and ignored
verification artifacts changed; no production writes or live restarts.

## Advisor receiving review — 08B ready with first repair — 2026-10-02

[Receiving review](TASK08B_RECEIVING_REVIEW.md): inspected both 08A deliveries and
reran all 15 retained genuine-data checks successfully. A public-handler syntax
selector probe returned the two actually present matches, including provisional
status. Static logging ownership, isolated imports and pip check passed.

[08B's prompt](TASK08B_PROMPT.md) now receives the actual APIs, available syntax
research and owner-directed real-evidence verification policy. It explicitly
assigns the remaining source-scope correction as its first bounded receiving
repair: apply known exact path/directory constraints before enumeration, without
widening scope to populate a cache. The correction is not yet implemented.
Multi-Run and absent real failure scenarios remain unverified. The fresh broad
content search took 181.405 seconds; no fixed performance threshold is inferred.
See the review for evidence paths and limits. Runtime code and production state
were unchanged; only disposable verification handlers were used.

## Task 08A.2 implementation delivery — 2026-10-02

Latest owner review concerns inventory memory and actual traversal scope.
Measurements/recommendations are in the 08A.2 handoff and ignored
`.codex-tmp/task08a2/memory/MEMORY_REVIEW.md`: full path inventory 11.54 MiB;
single-reference parent scope 96 KiB; all-reference parent scopes 2.68 MiB.
Full and parent-scoped inventories find exactly the same real candidate pairs.
Direct file checks reach the same files with one recorded/on-disk case-spelling
difference, verified with `Path.samefile`. No runtime strategy changed, packages
installed or synthetic checks added. Automatic lookup still needs its directory
constraints pushed ahead of traversal; preserve the owner's prohibition on
widening a narrower requested scope to fill a cache. 08B itself remains unimplemented.

Owner follow-up: the readable report now shows all 133 stored members in a
load-order table and includes explicit load-order numbers beside candidate names
and excerpt headings. Outside-playset roots show recorded order unavailable.
The 08A.2 handoff, 08B prompt and reporting ledger preserve this display requirement.
Regenerated from saved genuine evidence; no runtime code or new tests needed.

Delivered [source search/context and its 08A.1 integration](TASK08A_2_SOURCE_SEARCH_HANDOFF.md).
Public API: `SourceSearch(client=None, ripgrep=..., context=..., excerpts=...)`
(options keyword-only), `read_playset`, `search`, `resolve`, `excerpts_for`,
`clear`, and `source_references(record)`. Pass it as `DiagnosticAnalysis`'s
`source_resolver`. Required source predicates now work; optional source context
leaves SQL totals usable. 08B receives both deliveries and owns presentation.

Added reporting `source_query.py`, `source_references.py`, `source_search.py`;
extended `query.py`, `analysis.py`, `__init__.py`; added only genuine-data checks
in `tests/test_source_search_genuine.py`; updated both handoffs and current docs.
No handler/watcher/learner/schema changes. Unrelated dirty work is preserved.

Nine new checks passed twice; final run 64.248 seconds. Six existing genuine
diagnostic checks passed in 31.454 seconds. No failures/skips, synthetic scenarios
or injected errors. Full evidence and disposable SQL backup:
`.codex-tmp/task08a2/7db8b47229564e748a47221366512b0b/`.
Readable filters/results/excerpts:
`.codex-tmp/task08a2/SOURCE_SEARCH_REAL_DATA_REPORT.md`.
The handoff names each precise check, measured scope/timings and genuine cases
not exercised. Initial inspection encountered a console Unicode print error and
found a reference-slot provenance overlap; both are documented. No requirements
beyond the task were introduced.

The 133-member playset supplied 105,603 inventory entries; large content search
covered 11,914 text files in 66 Windows ripgrep batches. The 2,475 diagnostics /
4,182 occurrences remain unchanged despite 2,651 candidate associations. No
dependency installation was needed: ripgrep 15.2.0 already exists on PATH.
Logging ownership, isolated imports and pip check passed. No live processes were
restarted or production state modified. Do not restore removed synthetic tests;
missing real evidence stays explicitly unverified. Earlier checkpoints follow.

## Task 08A.1 implementation continuation — 2026-10-02

Delivered [diagnostic query/analysis library and handoff](TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md).
New files are `src/ck3chronicle/reporting/{__init__,query,analysis}.py`,
`tests/test_reporting_query_requirements.py` and that handoff. This task also
updates the opening status/plan/reporting-ledger sections; all unrelated dirty
changes remain. No existing pipeline/handler/watcher/learner code was changed.

Public entry point is `DiagnosticAnalysis(HandlerClient(database_file))` with
`investigate(run, package_id=..., query=...)` and eligibility-first `list_runs`.
Results include effective filters, exact totals/rollups, stored rendering,
historical zero-count entries, requested/obtained windows, unavailable evidence,
review metadata and chronology exclusions. A required source filter fails
explicitly until 08A.2 supplies `SourceResolver`; no temporary search engine exists.

Owner review removed all 12 synthetic/scalar reporting checks plus the injected
request-failure and file/import-guard checks. Six genuine-data checks remain and
passed with no failures or skips. No invented metadata, counts, mock clients or
failure injection remains in this reporting test file. Its misleading syntax-test
name is now `test_record_selector_and_positive_occurrence_filter`; it does not
claim to verify the syntax preset. Do not restore the removed checks or turn their
scenarios into owner requirements. Report failures and proposed scope additions.

Current evidence is `.codex-tmp/task08a1/verification-after-synthetic-removal.txt`
and `35906eab57f24c338148dddc4803eadc/baseline.json` beneath that directory. All six
checks passed again in 9.732 seconds, with no failures or skips; logging ownership,
isolated imports and dependency checks passed again too. The unchanged
SQL exercise contains one eligible Run, 2,475 records and 4,182 occurrences.
Multi-Run behavior, threshold boundaries and failed-read behavior remain unverified
by genuine data. Earlier synthetic passes are not acceptance evidence. The owner
subsequently directed removal of the pre-existing synthetic logging suite too:
`tests/test_runtime_logging_requirements.py` and all seven checks are deleted.
Do not restore it from older handoffs or ignored runners. The arbitrary 32-level
query nesting cap was removed. Source inspection found no reporting branches
keyed to mock clients or fabricated messages; handling of documented handler
errors and unavailable comparisons follows the original task. No logging, handler
or watcher runtime code was changed. Earlier execution logs remain historical.

Continue with 08A.2's prompt and this delivered source/query boundary. Implement
and verify reference extraction, explicit roots/optional members, all-candidate
search, incomplete-coverage errors, file rollups and excerpts before 08B. The syntax
research handoff is available; the shared OR-selector interface can express its
exact conditions. CLI/presets remain 08B's task. Production operation restrictions
remain in force; nothing was committed or pushed.

## Source-search and 08B receiving corrections — 2026-10-02

Updated [08A.1](TASK08A_1_PROMPT.md), [08A.2](TASK08A_2_PROMPT.md) and
[08B](TASK08B_PROMPT.md): source roots need not belong to a playset; content
conditions evaluate across a file; unavailable required source associations
produce explicit errors with partial coverage/results retained. Optional context
remains distinct from a required filter. Added ripgrep configuration isolation,
structured output, match/no-match/error handling, missing-executable guidance
and actual Windows invocation verification to 08A.2's assignment.

08B names both split prompts and `TASK08A_1_DIAGNOSTIC_QUERY_HANDOFF.md` /
`TASK08A_2_SOURCE_SEARCH_HANDOFF.md`. It starts after both deliveries and their
query/source integration are complete. Removed rejected timestamp and mandatory
playset recommendations from the separate review; the owner's session-end
wording is unchanged. Documentation edits only; checked ripgrep help/documentation
and document links, not runtime implementation or production behavior.


## 08A.1 / 08A.2 prompts finalized — 2026-10-02

[08A.1](TASK08A_1_PROMPT.md) now explicitly supports OR selection of multiple
stored matched-template references and uses diagnostic-record search terminology.
[08A.2](TASK08A_2_PROMPT.md) requires efficient disk search from the start:
ripgrep bulk search, reused in-memory filename/path inventory, batching, early
filters, bounded streaming, explicit coverage settings and representative large
real-playset timings. The remaining prompt policies were preserved. The template
representation recommendation is withdrawn; unrelated recommendations remain
unapplied in [the separate review](TASK08_SPLIT_REVIEW.md). No implementation,
installations or runtime actions were performed; 08B was unchanged in this pass.

## Owner-updated reporting split — 2026-10-02

The current sequence is [08A.1 diagnostic queries/analysis](TASK08A_1_PROMPT.md),
[08A.2 playset source search/context](TASK08A_2_PROMPT.md), then
[08B reports/CLI](TASK08B_PROMPT.md). The owner's supplied revisions are the
baseline; changes are limited to task division, receiving boundaries and requested
search-library guidance. They supersede conflicting older planning text below.
Prompts are prepared, not implemented. See [the split review](TASK08_SPLIT_REVIEW.md)
for the scope mapping and separate unapplied recommendations. Documentation only;
no runtime actions or installations.


## Syntax research ready for Reporting and Analysis — 2026-09-30

[CK3 syntax diagnostics research](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#concrete-selector-handoff)
supplies nine explicit selectors over existing stored definitions/values for
package `68f1ae5db205ab46afef9c4d`, including the exact REASON condition needed
to distinguish assignment errors from semantic errors sharing a template.
It includes genuine excerpts, source hashes, citations, exclusions and limited
extent/cascade findings. Both stored match statuses remain eligible.

The owner requested verified findings only. Unverified brace-balance formulations
have been removed from the proposed list; the observed `Unexpected token: =`
and `Malformed token: {` remain with their precise meanings. Context-dependent
messages are research evidence, not syntax-preset selectors. The recorded
eight-Run research snapshot yields 16 records; this is not a new live query.

The [2026-10-01 brace follow-up](CK3_SYNTAX_DIAGNOSTICS_RESEARCH.md#brace-token-follow-up--2026-10-01)
searched 82 distinct retained logs. It verifies quoted `'}'` in event-ID,
namespace and missing-theme messages, but finds no `token: '}'` spelling.
Exact template IDs and native excerpts are recorded as contextual clues;
brace imbalance remains unproved and the nine proposed selectors are unchanged.

Research delivery only: Reporting and Analysis reviews this handoff when building
08A/08B. Updated the report and receiving-document links; no runtime code,
classification, ingestion, storage, model selection or reporting implementation
was changed. No production ingestion or service restart was performed.

## Reporting and Analysis prompt handoff — 2026-09-30

Prepared [08A](TASK08A_PROMPT.md) and [08B](TASK08B_PROMPT.md) together. Execute
08A's reusable investigation/history/search services first; 08B consumes its
actual handoff to deliver presets, CLI and HTML/text/JSON with linked excerpts.
The [reporting ledger](TASK08_SCOPE_REVIEW.md) records ownership, dependencies
and drafting rationale. Old Task 08 audit instructions are superseded.

The timestamp field is already confirmed by the receiving check below. Exact
recurrence stays within a selected package; missing timestamps exclude Runs,
and short history is valid. Disappearance analysis includes historical identities
with selected count zero without creating stored records. The syntax research
delivery above now supplies that preset's selectors for receiving review.

Updated the two prompts and planning pointers only. Inspected focused source and
handoffs; did not rerun runtime checks, open the live database, change processes,
ingest captures, alter selection, reset/expire data, commit or push. Rejected
handler design documents were not read. Implementation is not claimed.

## Pipeline source modification timestamp receiving check — 2026-09-30

The existing capture-metadata → handler-owned write → `runs.facts_json` →
public Run facts path preserves `error_log_source_modified_at` exactly.
Read it as `run["facts"]["error_log_source_modified_at"]` when present;
historical/manual absence remains unavailable. See the
[current pipeline handoff](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md#source-modification-timestamp-receiving-check--2026-09-30)
for the exact path and evidence distinction.

Reviewed the inherited watcher source-mtime suite's 43-check result; did not
rerun it. Ran two additional focused checks on disposable copies: all public
Run reads preserved the nine-digit string, and a duplicate with conflicting
capture metadata preserved the entire stored Run. Both passed without skips.
Evidence and reproducer are ignored under
`.codex-tmp/pipeline-source-mtime-receiving/`. No preservation gap or implementation
change was needed. This follow-up changes only that pipeline handoff and this
ledger, plus ignored verification artifacts. Existing unrelated work is preserved.
No production ingestion, live restart, historical mutation, commit or push.

## Watcher source modification time — 2026-09-30

`spool_logs` now records `error_log_source_modified_at` from the validated
original source stat in the existing capture metadata. The existing ingestion
path preserves it in SQL Run facts without a schema change. See the
[focused handoff](WATCHER_SOURCE_MTIME_HANDOFF.md) for the field, genuine-input
checks and ignored disposable evidence. Changed files for this follow-up are
`harvester.py`, the new `test_capture_source_mtime_requirements.py`, that handoff
and this ledger. Existing unrelated changes are preserved. No historical
captures/Runs, production configuration or live processes were modified;
activation remains separate. Nothing was committed or pushed.

## Task 07E live activation - 2026-09-30 08:28 Hong Kong

Following owner authorization, the updated watcher was started hidden at
00:27:53 UTC. The previous PID was absent, its heartbeat was stale, the runtime
lease was free, and no old handler was listening. The exact configured database
passed read-only schema-3 verification. CK3 was already running, so the new
watcher attached to that process without interrupting the game.

Watcher PID 34340 (launcher 9792) observed CK3 PID 44816; a fresh heartbeat at
00:28:23 UTC confirmed `running`. Handler PID 308 reported `handler_ready`, with
instance `71d783fe8dc34ea6b4b0f7140de130b2`. Startup ingestion found all five
readable retained captures already stored and returned ordinary duplicate
non-completion. Twenty-two older inaccessible captures remain unavailable;
permissions were not changed. No watcher/handler ERROR events were observed;
bootstrap stderr was empty. Configuration, model selection and database identity
were unchanged; no reset or forced expiry was performed.

Evidence: ignored `.codex-tmp/task07e/activation.json`. Logs now use the 07E
paths in [the handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md). The attached game's
exit was subsequently observed at 01:26:28 UTC and ingestion completed at
01:26:36 UTC as Run `20260930-BYVZUV`, request
`3f5002c984d94334b65205052b4916ed`. Its merged trace is retained under
`.codex-tmp/task07e/live-session-20260930-BYVZUV/`. Capture and ingestion took
7.657 seconds, with no warning/error/contention events for that request.
Attachment after game startup does not establish complete observed start-to-exit
Trusted Run acceptance. Task 08 and
Run-result replacement remain separate. The following implementation-delivery
checkpoint predates this separately authorized activation.

## Task 07E delivered — activation remains separate — 2026-09-30

[Task 07E's handoff](TASK07E_RUNTIME_LOGGING_HANDOFF.md) documents the shared
standard-library logging owner, bounded UTF-8 JSONL files, watcher/request-ID
correlation, preparation/database timing, compact contention episodes, tracebacks
and durable bootstrap stderr. EventJournal preserves lifecycle vocabulary and
the replaceable heartbeat. Runtime logging failures do not change Run outcomes.
Future runtime code uses `runtime_logging.py`; run `tools/check_runtime_logging.py`.

Fresh verification passed **66 checks, no failures, errors or skips**, in 86.156
seconds: the 59 receiving checks were rerun alongside seven focused logging
checks, using genuine retained CK3 inputs and disposable storage. Static ownership,
isolated imports and `pip check` passed. This is distinct from the inherited
September 30 07D handoff's 59-check result. Evidence is ignored under
`.codex-tmp/task07e/`; the handoff records coverage and limitations.

The [07D API contract](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md) is preserved:
one dedicated handler, one preparation thread, one database worker, exactly three
public states, all unfinished requests plus the latest 256 terminal outcomes,
`LookupError` for unavailable results, `exception_class`, and internal-only
`cleanup_unaccepted`. Watcher `ingestion_outcome_unavailable` still creates no
outcome or eviction retry. SQL/review/playset formats and ingestion/retention
semantics are unchanged. Logging does not recover outcomes after abrupt termination.

No production configuration, selection, storage, captures or live processes were
changed; nothing was committed or pushed. The unrelated dirty tree is preserved.
Next operational step: follow the 07E handoff's separate procedure to stop the
watcher at a quiet boundary, shut down the old handler for the configured file,
verify that file read-only, and start the updated watcher. Startup ingestion and
daily retention keep their existing behavior. Task 08 SQL reports, Run-result
replacement and complete Trusted Run acceptance remain separate assignments.

## Historical checkpoints and separately scoped proposals

## Task 08/09 look-ahead proposal — 2026-09-29

[TASK08_TASK09_SCOPE_PROPOSAL.md](TASK08_TASK09_SCOPE_PROPOSAL.md) recommends
rewriting 08 as complete SQL reports/bounded audit over delivered 07D APIs and
retiring the old 09 offline reconnection/deletion draft. The proposed command
surface and sequencing are recommendations, not owner-approved implementation
instructions. Existing storage read/render APIs and 07C learner operations were
source-inspected; no runtime/learner campaign was rerun. The rejected database
handler design was not opened. 07D remains the active implementation assignment;
Run-result replacement and final Trusted Run acceptance remain separate.

## Task 07 receiving review and separate 07D assignment — 2026-09-29

Use [TASK07D_PROMPT.md](TASK07D_PROMPT.md) for the new team's implementation
assignment and [TASK07_QUALITY_REVIEW_FOR_07D.md](TASK07_QUALITY_REVIEW_FOR_07D.md)
for independent source/verification findings. The rejected design/copies were not
opened for this receiving review and are prohibited reading for 07D. The owner's
new in-memory, three-state direction supersedes the old design-review/stop gates.

Five receiving checks passed with no skips in 102.916 seconds, including three
complete genuine inputs, both packages in one database, SQL/review/playset
agreement, native rendering and disposable retention/initialization. Evidence is
ignored under `.codex-tmp/task07d-advisory-review/`. No core ingest/storage rewrite
was identified. Assignments 07D-01 through 03 cover shared runtime routing,
caller outcome reconciliation and current API/handoff repairs.

07D code/integration/verification remain to be delivered; this pass prepared
instructions and reviewed existing code. No product code, production data,
configuration, selected package or live process was changed. Historical activation
does not establish current live status. Task 08 and Run-result replacement remain
separate. Older rejected-design continuation text below is historical only.

## Rejected database-handler design retired

The owner rejected the shared-database-request-handler design as materially
over-scoped. `PIPELINE_QUEUED_INGESTION_DESIGN.md` has been deleted. Its review,
continuation and implementation instructions are withdrawn; no replacement design
or implementation is authorized by this cleanup. A replacement instruction will
be issued separately. Earlier queue follow-up references below do not authorize
implementation of the deleted design.

Repository inspection found no implementation derived from it: no request handler,
named-pipe transport, owner-election/request-recovery machinery, expanded request
states, or related schema/runtime integration. Ingest still opens the repository
directly; the watcher uses its existing local executor. SQL/review version 3 and
existing capture locks predate the rejected design and remain unchanged.

Only documentation was changed. No production data, configuration, runtime code or
live process was changed; current live-process status was not checked. Cleanup is
complete; stop here pending the separate replacement instruction.

## Watcher live ingestion activated; database naming implemented — 2026-09-29

The owner directed completion rather than leaving operational setup outstanding.
See [WATCHER_LIVE_ACTIVATION_HANDOFF.md](WATCHER_LIVE_ACTIVATION_HANDOFF.md).
The watcher was restarted at 21:19:39 UTC with worker PID 5032 and launcher PID
51116. It now ingests completed captures into the explicitly configured database
`ck3chronicle-schema3-20260928T211854Z.sqlite3` in the existing runtime directory.
Startup ingestion accepted all five readable captures (12,449 diagnostic records);
SQL/playset/review agreement and the new heartbeat are verified. Daily retention is enabled, first due one
day after startup. Twenty-two inaccessible older capture directories were
reported and skipped; permissions and the old legacy DB were not changed.

The approved storage naming is implemented in its owning APIs: `create_database`,
`open_database`, `open_database_readonly`, `Database`, `database_info` and
`database_id`. Open/ingest/config now take an exact SQLite file path. Schema and
review manifest are version 3; playset format stays 1. No compatibility alias,
migration, replay or newest-file discovery was introduced. Forty-five checks
passed before activation. Shared pipeline queuing remains the separate pipeline
follow-up; the actual watcher caller and operational activation are delivered.

## Watcher-to-ingest caller implemented — 2026-09-29

See [WATCHER_INGESTION_WIRING_HANDOFF.md](WATCHER_INGESTION_WIRING_HANDOFF.md).
The actual `cmd_watch` -> published capture -> completion callback now invokes
the existing ingest API on a serial worker outside lifecycle polling. Startup
submission, daily maintenance/retention, journaled outcomes and config defaults
are implemented. Protected error logs publish even when debug capture or playset
extraction fails. A narrow pipeline correction accepts malformed/mismatched
playsets as unavailable, with explicit `IngestResult.warnings`; supplied JSON is
preserved. These changes were verified through the actual watcher caller using
genuine inputs and disposable SQL storage. The pipeline's shared request queue
remains separate work and no longer blocks the watcher caller's implementation.

The owner approved `ck3chronicle-schema<N>-YYYYMMDDTHHMMSSZ.sqlite3` naming;
the pipeline filename/API terminology change is not yet implemented. No existing
database was deleted or renamed. The ignored config now contains explicit watcher
defaults, but current-schema production storage has not been initialized. The
live watcher started earlier still runs the previously loaded capture-only code;
this delivery has not restarted it or activated production ingestion/retention.

## Owner ingestion/retention decisions and pipeline queue request — 2026-09-29

The owner approved processing otherwise valid new error logs with missing,
malformed or mismatched playsets: report the problem, preserve source JSON and
store the existing unavailable-playset representation. A debug-copy failure must
also not block publication/ingestion of an already protected error log; that
capture change belongs to the watcher. Extract playsets only from copied pairs.
All completed captures enter ingestion, with startup identification and another
attempt for captures not accepted into SQL. Retention cadence is DAILY, with
the already-approved 30-day expiry policy unchanged. Configuration must have
sensible defaults and require no routine interactive setup.

This checkpoint's queue follow-up was later covered by the now-rejected handler
design. The [former prompt](PIPELINE_QUEUED_INGESTION_FOLLOWUP_PROMPT.md) is retired;
its queue/durability review and implementation instructions no longer apply.
Replacement instructions will be issued separately. The existing watcher caller
and its contention handling are unchanged.

The owner also questions legacy generation terminology and wants a consistent
database filename incorporating schema and initialization date/hour. A precise
UTC naming convention is proposed in the prompt, pending confirmation. No database
deletion, reset, rename or migration is authorized by that naming discussion.
This checkpoint and the prompt are documentation only; no live watcher, pipeline
code, operational config or production data was changed. Earlier malformed-playset
rejection and hourly-retention proposals below are superseded by these decisions.

## Task 07 implementation and verification checkpoint — 2026-09-28

Continue from [TASK07_INGESTION_AND_RETENTION_HANDOFF.md](TASK07_INGESTION_AND_RETENTION_HANDOFF.md).
Working ingest/retention APIs and the manual command are implemented. SQL schema 2
and review manifest 2 store ordered playsets and per-Run processing lineage. Three
genuine complete inputs passed API/CLI ingestion, cross-package duplicates, both
packages in one DB, native rendering/review accounting, playset agreement, explicit
schema-reset refusal, failure cleanup and disposable retention. Two native requirement
checks passed; evidence and limitations are in the handoff.

Exact continuation: obtain the already-requested owner disposition for malformed or
mismatched completed playset JSON. The current reviewable proposal raises PlaysetError
and preserves the capture; missing JSON is allowed. Do not claim Task 07 fully closed
before that decision. After closure the watcher team wires both automatic triggers;
Task 08 reports and separate live activation remain outstanding. No watcher trigger
or production change was made. Explicit Run replacement is separate follow-up work.

Task 07 changed `pipeline/schema.py`, `repository.py`, `review.py`, added
`ingestion.py`, `playsets.py`, `capture_access.py`, `retention.py`, added the ingest
handler/arguments in `cli.py`, native requirement checks, and the handoff/status/plan/
execution-order/scope/README documentation. Preserve the substantial pre-existing
dirty tree. Harvester, watcher, models, learners, selection and live configuration
remain untouched by this task. Scratch evidence is under `.codex-tmp/task07/`.
The completed Script location-stack findings remain context, not a pending task.
This checkpoint supersedes earlier implementation-pending continuation points below.

## Task 07 advisory review after 07C — 2026-09-28

Reviewed current source and delivery documents; Task 07 remains unimplemented.
The [prompt](TASK07_PROMPT.md) now uses 07C package selection
and existing `contracts.run_lineage`, removes ingestion-side learner-provenance
follow-up and recognizes the completed location-stack investigation. The
[scope review](TASK07_SCOPE_REVIEW.md#current-task-ledger) holds the compact task
ledger: the owner chose expiry of all completed captures, including failed/unprocessed
ones, after 30 elapsed days from capture time; malformed-playset disposition remains
pending. Current selection remains unchanged. Next: settle that choice, execute Task 07, then watcher-team
wiring and Task 08 SQL reports. This pass changed documentation only; no runtime
checks, production operations or independent rerun of delivery verification.

## Advisory transfer — 2026-09-28

Use the [Task 07 onward advisory transfer prompt](ADVISORY_HANDOFF_TASK07_ONWARD.md)
for the new planning/advisory task. It incorporates the delivered 07C release
handoff and completed Script location-stack investigation, distinguishes them
from older open-item wording below, and records current owner decisions and
remaining team boundaries. This transfer is documentation work, not Task 07
implementation or independent re-execution of 07C verification.

## Task 06B cleanup completed — 2026-09-28

The deprecated CLI/provider stack and its exclusive research/test consumers have
been removed. See [the cleanup handoff](TASK06B_DEPRECATED_CODE_CLEANUP_HANDOFF.md)
for the exact inventory, portable rollback archive, verification and limits.
`watch`, `capture`, `doctor` and `observe-logging` remain; `watch --once` remains
error-only. `harvester.py` remains the capture owner. No processing command is
active. Task 07 delivers ingest and retention APIs, one manual `ingest` command,
playset SQL storage and a watcher-team integration handoff. The watcher team owns
automatic ingest after capture and periodic retention checks, including idle periods.
See the [current scope](TASK07_SCOPE_REVIEW.md)
and [revised draft](TASK07_PROMPT.md).
Task 07 must remove the current database-wide lineage
lock and record processing versions per Run; compatible selections share one
database. Schema changes require an explicit reset, without migration or fallback.
These are instructions for implementation, not completed code. Retention eligibility
and cadence remain open. Task 08 focuses on SQL reports/read operations.
The old provider retirement, C1/C2 capture relocation/deletion proposal, parser
comparison retirement and removed-API research checks are discharged/superseded;
do not repeat them or restore compatibility providers. Task 06/v45 storage and
the watcher producer contracts remain intact, as do learner policy limitations
and the separate Script location-stack investigation. The separately authorized
live watcher was not stopped, restarted, reconfigured or used for verification.
Older dated provider-retention and cleanup-pending statements below are historical.

## Next: Task 06B cleanup, then Task 07 — 2026-09-28

The owner authorized disabling unused old CLI paths and removing their deprecated
providers before Task 07. Execute [Task 06B](06B_DEPRECATED_CODE_CLEANUP.md), then
[Task 07](TASK07_PROMPT.md) against its completion handoff.
Keep the working watcher/playset producer and capture owner `harvester.py` in place;
the earlier plan to relocate capture into `pipeline/capture.py` is superseded.
The watcher review's Section B supplies specific retirement targets. This checkpoint
records the assignment and revised prompts, not completed deletion. The live
watcher's separate operating authorization and Task 06's selected baseline remain.
Older instructions to retain unused CLI providers until cutover are superseded for
the explicit 06B scope.

The owner additionally requires 06B to archive every pre-edit/deleted file through
PowerShell before cleanup, delivering a portable archive with `cleanup.ps1`,
standalone `rollback.ps1`, inventory and restore README. Keep the archive available
for the owner to zip and move outside the repo; rehearse rollback on disposable
copies from a relocated archive. The Task 06B prompt contains the full requirements.

## Live watcher started at owner request — 2026-09-28

Started the updated continuous watcher in a hidden background process at
06:55:46 UTC using `.venv/Scripts/python.exe -B -m ck3chronicle.cli watch`
from the repository root. Worker PID: 46516; virtual-environment launcher PID:
61708. The worker holds the runtime lease and its journal reports
`watcher_ready` / `awaiting_game_start`; CK3 was absent at startup.
The worker's heartbeat was verified at 06:56:17 UTC.
Journal: `.ck3chronicle/wip/runtime/watch/events-20260928T065546.589644Z-46516.jsonl`.
New observed exits will publish paired logs and playset templates to the
configured pending directory. Pipeline processing remains a separate task.
This operating checkpoint supersedes the earlier statements that the live
watcher had not yet been started; no autostart or scheduled task was installed.

## Watcher active-playset producer delivered — 2026-09-28

The owner approved implementation of the watcher plan. Continuous `cmd_watch`
now copies the full error/debug pair, extracts the emitted active playset,
resolves descriptor names, hashes both protected files and writes `playset.json`
before existing pending publication. The joined identifier is
`sha256:<error_log_sha256>:<debug_log_sha256>`. Outcomes and metadata problems
go to the watcher journal without continuous-watcher terminal messages.

Production changes are confined to new `src/ck3chronicle/playset.py`, capture
support in `harvester.py`, actual watcher wiring in `cli.py`, and a small
`EventJournal` option in `watcher.py` for safe startup-failure logging. No root
configuration changes were required. Manual commands keep their existing behavior.
Tests were added/extended in the two watcher/playset capture requirement files.

39 focused checks passed, including existing processing-recovery coverage.
An isolated demonstration on recent real log copies produced 133 members,
zero UNKNOWN names and zero resolution warnings; both copied files and their
serialized hashes verified. Generated evidence is ignored under
`.codex-tmp/watcher-playset-implementation/`.

See [WATCHER_ACTIVE_PLAYSET_HANDOFF.md](WATCHER_ACTIVE_PLAYSET_HANDOFF.md) for the
complete producer format, generated example and precise Task 07 receiving work.
Task 07 was held for this delivery and has not been started here. Its receiving
path must consume the watcher template and preserve pair provenance in Run-owned
SQL and the review manifest; the old pending inspector currently rejects the new
JSON artifact. No pipeline/schema implementation, live watcher startup, production
capture processing, production DB write, commit or push was performed. Existing
unrelated working-tree changes were preserved.

## Task 06 v45 integration complete; Task 07 next — 2026-09-28

Task 06 has integrated and selected learner v45 package
`68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`:
model schema 5 / matcher API v2, `error-contract-v1`, SQLite schema 1.
The normal source catalog and installed wheel now use the same package.
The existing SQL design stores the new literal choices correctly; no pipeline
source edit, extra processing stage or physical database migration was needed.

Seven complete native logs passed preparation, aggregation, SQLite write/readback,
review completion and separate-process database-only rendering:
418,168 recovered occurrences,
19,912 unique records and four native review emissions.
All original 122 cases / 9,153 emissions are record-eligible. Both line-label
choices retain their exact native spelling. Duplicate rejection, generation
isolation and actual read-only SQLite failure preserve accepted state.
The installed whole-log storage path also passed with checkout resources blocked.
See [the v45 integration handoff](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md)
for exact evidence, storage mappings, changed paths and remaining limits.

The learner assessment's remaining word-run policy issues, two lost matches
against the thirty-log predecessor, capture regressions and tie behavior remain
documented; storage does not reinterpret those outcomes. Development selection
is updated, while production processing and existing application providers remain
unchanged. Next is Task 07 protected-input/processing/replay composition, followed
by Task 08 SQL-only reporting/audit. The historical learner/research retirement
dependencies in the Task 05/06 handoffs remain. No production database writes,
watcher/capture operation, retained-input deletion, commit or push occurred.

The dated selection and "integration pending" statements below retain their
historical context and are superseded by this checkpoint.


## Learner v45 release delivered; Task 06 integration separate — 2026-09-28

The owner authorized the demonstrated additive applicability fix, a replacement
over the complete retained 73-log corpus in cumulative 20 + 20 + 20 + 13 batches,
native before/after assessment and immutable schema-5 / matcher-API-v2 delivery.
That replacement is package `68f1ae5db205ab46afef9c4d`, published model
`f5cde2616f35d563118d3d32`, from candidate `c4f174d947fbc531aba35fb7`.
Manifest SHA-256:
`2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
Task 06 integration and active selection remain separate. Earlier no-publication
statements describe earlier scope, not this delivery assignment.

Learner v45 extracts the existing source/context/construction/parameter applicability
gates into the shared matcher and uses them before additive wording protection.
Refinement partitions use complete retained matches. The same-structure wording
rules are unchanged. Native retained decisions demonstrate that the one-frame
comparison proposal survives while the travel/activity policy conflicts remain.
Fresh state and exact provenance are under
`.codex-tmp/learner-release-v45/`; this is a new build, not an import of v43/v44
learned definitions. Learner SHA-256:
`025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088`.

The final model has 689 definitions (492 supported / 197 provisional), assigning
2,439,711 occurrences as template and 154,873 as provisional, with four unmatched.
It gains 43,624 complete assignments versus the prior 73-log additive build with
no additional lost matches. Versus the selected thirty-log model it gains 119,114
and loses two. All original 122 cases / 9,153 occurrences match through 28
definitions: 118 bodies / 267 occurrences template; four / 8,886 provisional.

The [release assessment](LEARNER_RELEASE_V45_RESULTS.md) records native examples,
28 contextual inputs / 63 occurrences with changed captures versus the prior
73-log build, four remaining wording-policy conflicts, grouping regressions and
representation-sensitive ties. Within v45, all earlier supported definitions
survive, 30 promote and 50 retire with recorded successors/reasons. No prior
match becomes unmatched, but competing complete assignments make 21 previously
supported occurrences provisional at the 60-log checkpoint. Coverage gains do
not establish uniform semantic improvement or model acceptance.

The [pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) supplies exact parser,
matcher/validator/selector identities, callable interfaces, native export evidence
and schema-5 literal-choice requirements. Proposed selection is
`models/candidates/selection.v45.proposed.json`; read-only catalog loading resolves
it successfully. Active package `44a0401b8adf0a2953d26705` remains unchanged.
Next: Task 06 isolated integration of this explicit package, including choice
indices in storage/rendering, both statuses and native review associations, before
separate selection/cutover. Production processing remains disabled. No commit/push.

The independent immutable-package replay completed all 73 original logs without
development imports: zero discrepancies against 91,925 complete build inspection
results, 10,285,082 capture-byte checks and every original 122-case ordinal
reconciled. Exact results are in
`.codex-tmp/learner-release-v45/delivery-replay.json`; native examples and public
case results are alongside it. Active selection and all frozen source/package
hashes were reverified. This delivery makes no universal accuracy or performance
improvement claim; remaining policy/capture issues stay explicit in the assessment.

## Formal Pipeline Team reply: original unmatched shard — 2026-09-28

The owner requested closure against the original 122-case / 9,153-emission task.
[Formal reply](LEARNER_TASK06_UNMATCHED_REVIEW_REPLY.md): investigation and
candidate-level coverage are resolved; production deployment is not performed.
Fresh whole-original-log replay of current v44 additive candidate
`39cb19ab0ea10a48ebb98a46` and fresh candidate `6afef6948c1535e6d96126f5`
gives 114 template / 8 provisional cases, weighted 263 / 8,890 emissions, zero
no-match, using 28 definitions. Every original case/ordinal association reconciles.
The actually selected package remains `44a0401b8adf0a2953d26705` and still gives
the original 9,153 no-matches. Do not describe this reply as a deployed fix.
The reply links the historical causes, current before/after ledger, two worked
cases, multi-log answer and remaining out-of-scope learner limitations.
No publication, selection change, production processing, commit or push.

## Line-label equivalence implementation — 2026-09-28

Owner challenged the initial report's reliance on agent-chosen checks. The report
now leads with a procedure-matched v43/v44 audit, native examples, complete template
ledgers and additive evolution. There is no observed native coverage gain or loss:
fresh builds both have 203 templates; additive builds both have 208. All paired
definitions preserve memberships, support and capture behavior apart from the
declared label alternatives. Fresh-versus-additive differences affect 116 native
occurrences in four families, including one supported-versus-provisional difference;
these predate v44. Passing implementation checks is not owner acceptance. No
learner/runtime code was changed during this report audit. See the report for
concrete evidence/limits.

Owner authorized interchangeability of `line:` and `near line:` before LOCATOR.
Learner v44 represents these as declared literal alternatives in one template,
including from one native observation. Model schema 5 / matcher API v2 carry the
selected literal choice through exact rendering and identity; opaque fields,
source/context checks, complete assignment and support thresholds remain in force.
File-label policy is unchanged. Fresh same-version learning state is required.
See [implementation and verification](LEARNER_LOCATION_LABEL_EQUIVALENCE_RESULTS.md).
All 19 focused/native regression checks pass. The isolated two-log candidate
`6afef6948c1535e6d96126f5` accounts for 100,621 recovered occurrences; explicit
spelling-swap controls preserve template identity across 100 selected definitions.
Learner SHA-256: `2988d6fb02b51f4226fd6e025a21496062a518227f81607c4f45cc72fa1313cf`.
This does not fix the separate additive applicability defect recorded below.
No package publication, active selection change or production processing.

## Learner same-version additive exercise — 2026-09-27

Owner directs batches of 10–20 complete logs, retaining supported templates with
complete unambiguous assignments and refining cumulative provisional/unmatched
evidence. Do not tune inference from the 73-log run's behavior. The all-at-once
v42 attempt was stopped with its partial timing/recovery evidence retained;
the fresh thirty-log baseline completed. The v43 experiment completed
20 + 20 + 20 + 13 native logs and one cumulative successor model per checkpoint.
See [the experiment report](LEARNER_ALL_LOGS_V42_RESULTS.md), ignored
`.codex-tmp/learner-all-logs-v42/additive/` and `additive.log` for results.

v43 adds same-identity continuation, explicit provisional promotion/retirement
history, protection of provisional literal wording, and streamed native-evidence
serialization. The owner confirmed separate complete untyped effect/trigger
Unknown-location constructions, with opaque REASON and literal Unknown. Different
slot values count as distinct examples; repeated bodies do not. Each recognized
field contributes one typed similarity position, never its internal words.
No unchanged-evidence shortcut remains. Eight native additive and four date checks
pass. Frozen learner SHA-256 is
`8a1d1b067008a3d776b4496209e4b36c6bb7523923b28a7081be8deae216cbcc`.

The prior date-build issues are resolved: balanced-pair metadata uses lists, and
learner-only inference_rule metadata is excluded from executable field identity.
Final candidate `28cac50bf1249077100d12d5` has 492 supported / 199 provisional
definitions and matches all original 122 review cases. Its overall 73-log outcomes
are 2,396,084 supported, 154,876 provisional and 43,628 unmatched occurrences.
Those unmatched occurrences are eight bodies; the largest family demonstrates an
additive-guard applicability defect (one-frame proposals judged against four-frame
reference structures despite complete-matcher incompatibility). The other two
families expose incidental-value wording protection. Do not promote this candidate
or tune rules to its coverage. The report records targeted follow-up recommendations
and native proof; no inference changes were made during the frozen experiment.

All previous supported definitions survived; 30 provisional definitions promoted
and 53 fixed observations retired with successors. No previously matched training
evidence became unmatched within the same-version chain. The final comparison,
checkpoint audit and rejection traces are complete in the ignored directory.
The native-evidence inspector now reads ordinary JSON independently of indentation,
verified against both compact and indented complete exports; learner identity is
unchanged by this viewer correction.

No selected package, production state or existing research evidence was changed;
no commit, push, watcher or publication. Earlier dated sections remain historical.

## Learner date-token inference — 2026-09-27

Owner requires native dates such as `1178.10.1` to be KEYs, never diagnostic
wording, without waiting for variation in sampled values. Learner v42 adds the
declaration in `owner_rules.json`, recognizes the existing complete parser token
before grouping/alignment, and preserves it as KEY during field coalescing.
Selection evidence recognizes that declared field even with one observed value;
template support rules are unchanged. Opaque fields remain intact. The owner's
possible long evaluation interval is an explanation to consider, not an established
game behavior or a rule prerequisite.

Verification and native inputs are under `.codex-tmp/learner-date-key/`; the
requirement checks are `tests/test_learner_date_requirements.py`. No package,
active selection, parser, production state or existing research artifact was
changed. The previously reported in-memory balance-pair validation defect is
separate and remains unresolved; no full model build/publication was attempted.

## Task 06 completed; Task 07 is next — 2026-09-27

Task 06 delivers exact-identity aggregation, current-generation SQLite Run storage,
and the native review log plus manifest for every successful Run, including zero
review. Template and provisional records remain filterable and render from stored
definitions/values. `write_run` owns staging, finalization, publication, rollback and
commit; Tasks 07/08 consume its [public APIs and detailed handoff](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md).

Three complete unmodified Task 05 inventory logs were verified in fresh ignored
generations: 199,545 recovered occurrences, 190,392 eligible occurrences, 9,396
aggregated records and 9,153 native review emissions. Verification covers exact
bytes/order/frequency, both empty-shard files, duplicate rejection, namespaces,
Run IDs/date basis, count reconciliation, real read-only SQLite rejection and
separate-process database-only rendering. The detailed handoff distinguishes
observed failures from unexercised crash/native branches and records scope proof.

Next: Task 07 protected-input preparation and processing/replay composition;
Task 08 database-only reporting/audit. Operator command choices remain for Task 07
owner review. Existing application providers remain connected until separately
commissioned cutover. Production processing remains disabled. No watcher operation,
live capture, production database write, retained-input deletion, commit or push.

Task 05's named retirement dependencies remain: the historical baseline in
`tools/template_learning/build_parser_comparison.py`, the removed-API consumer
in `inspect_cross_emission_recovery.py`, and opt-in
`test_raw_parser_requirements.py::test_independent_pipeline_replay`. Learner/model
coverage limitations remain unchanged; storage does not repair unmatched or
malformed native patterns. The current selection/package is unchanged.

All dated instructions and task orders below are historical where superseded by
this checkpoint, the approved Error Contract and the Task 06 handoff.


## Task 05 completed; storage is next — 2026-09-27

Task 05 is complete: the selected schema-2 package is
`44a0401b8adf0a2953d26705` (unchanged model `76630685c4a341ca14bf9c7c`).
The pipeline now executes pinned recovery and shared complete selection, binds
only selected regions once, and prepares serializable `error-contract-v1` data
with exact identity and standalone rendering. The duplicate pipeline matcher and
its bound-candidate alternatives are removed. All 31 native inventory logs and
the disposable installed path passed; see
[the implementation handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md)
for APIs, resources, evidence, coverage limits and exact changes.

Next: Run aggregation, SQL/native-review persistence and stored reporting;
application/provider cutover remains separately commissioned. Historical
recovery/view retirement still depends on the learner comparison tool's old
baseline. Two additional research/test consumers of removed APIs are named in
the handoff. Production processing remains disabled; no watcher operation,
learner publication, commit or push occurred. Earlier sections below describe
historical checkpoints and do not supersede this completion.

## Next implementation: revised Task 05 — 2026-09-27

The owner assigned the verified shared matcher integration to
[Task 05](05_ERROR_CONTRACT_IMPLEMENTATION.md). Execute its ordered steps:
load the pinned package; replace local matching and bind only the selected result
once; implement Error Contract preparation/identity/rendering; verify complete
native inputs; then select the package and verify installed resources.
Delete the superseded pipeline matcher and its unused result machinery.
The earlier Task 05 review hold is superseded for this defined scope.

[Independent pipeline verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md)
passed across 31 logs / 1,167,165 occurrences, including every selected capture's
original-byte check. Candidate `44a0401b8adf0a2953d26705` is ready for integration;
selection remains unchanged in this prompt-revision pass. No source, package or
model implementation was changed. SQL/review persistence and application cutover
remain later. Historical recovery/view retirement still requires retiring the
learner comparison tool's old-baseline path; carry that dependency forward.

The delivery and earlier checkpoints below retain their dated evidence. Use this
section and the revised prompt for current execution scope and order.

## Shared matcher candidate delivered — 2026-09-27

Owner-directed learner extraction is complete. Candidate package
`models/candidates/44a0401b8adf0a2953d26705/`, manifest
`2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1`, supplies
`ck3-native-matcher-v1` with the unchanged schema-4 model
`76630685c4a341ca14bf9c7c`, parser v1.7 and assignment policy v2. The old release
and active `models/selection.json` remain byte-identical. Proposed metadata is
`models/candidates/selection.proposed.json`; it is not activation.

Fresh before/after learner and independent package replay agree on all 31
complete logs: 1,167,165 diagnostics, 78,869 distinct complete inputs within logs,
712,271 template / 445,741 provisional / 9,153 no-match. All nine slot types,
present empty versus absent, wrappers and 11 groups/13 entries are exercised.
4,447,658 present captures and 59,054 absences retain exact original bytes.
Unpublished-model parity also passes. New layout indices are the sole additive
legacy-result difference; no definitions, IDs, support or policy were changed.

Matching bodies are extracted into `matching_primitives.py`; learner callers,
evaluation and publication use the shared mechanics. `native_matching.py`,
`matching_validation.py` and `matcher_loader.py` provide the standalone contract.
Publication now creates immutable packages. Full-ID dependencies are hashed.
Research assignment review no longer imports the pipeline matcher. Generated
evidence is ignored under `.codex-tmp/shared-matcher/`.

Next owner: pipeline team. Implement package/selection reading, call the shared
entry point, bind only the selected assignment once, preserve final status and
layout references, verify on native logs, then retire its duplicate matcher.
Pipeline source, active/wheel selection, SQL and production operation were not
changed. Pre-existing product/pipeline documentation edits are preserved; no
commit/push was requested. See the [formal delivery and exact invocation](LEARNER_PARSER_PIPELINE_HANDOFF.md)
and [API/error/offset contract](SHARED_MATCHER_API.md). Ties, capture ambiguity,
alternative component layouts, >2 entries and malformed/failure paths have no
genuine witnesses in this corpus and remain explicit verification limits.

## Historical Task 04 closeout before audit/shared-matcher review — 2026-09-27

Owner approved the [full Error Contract](ERROR_CONTRACT_SPECIFICATION.md), including
source/emitter stored with the template definition and exposed through each record.
[Task 04 completion handoff](TASK04_ERROR_CONTRACT_HANDOFF.md) supplies the current
pin/interfaces, native checks, coverage limits and exact continuation point.
At this checkpoint the owner commissioned [Task 04(B)](04B_PIPELINE_PROCESSING_AUDIT.md)
before deciding repairs or Task 05 amendments. That audit, subsequent review and
shared-matcher delivery are now complete. The current scope at the top of this
document supersedes the original hold and bounded-local-matcher repair proposal.
The historical recovery/view retirement dependency remains separate.

The learner assignment dependency is resolved in selected model
76630685c4a341ca14bf9c7c, schema 4 / parser v1.7 / assignment-v2 / classifier-v7.
Both full and provisional outcomes expose one selected complete assignment.
Fresh Task 04 replay: 100,621 results on two complete logs, 173,247 present bindings
checked against source bytes, 4,350 absences, 11 groups / 13 supporting entries.
No SQL persistence or application cutover was performed.

This closeout adds the approved specification, completion handoff and revised
prompt, and reconciles active guidance. Code, models, learner files and protected
evidence remain unchanged. Pre-existing LEARNER_PIPELINE_MATCHING_INVESTIGATION_PROMPT.md
is preserved. Task 04(B) was the next step at that checkpoint. Run aggregation,
SQL/review publication and stored reporting
remain later implementation work. No commit or push is part of this closeout.

## Published: continuation-aware learner v41 and parser v1.7

2026-09-26. Owner authorized completing continuation support then publishing.
Selected release **76630685c4a341ca14bf9c7c**, manifest
`364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0`.
Model schema4 / featurev4 / assignment-v2 / classifier-v7. Parser v1.7 bytes
unchanged. models/selection.json and wheel data paths reference this release.

One complete learning record contains an opening and its ordered supporting title
entries. Owner JSON declares the component reference/value types; opening wording
is inferred. CHARACTER_FULL_ID remains opaque and each displayed title is PARAM.
Hash-covered continuations.py validates every entry against the selected opening;
assignment.py selects one complete supported/provisional result. Runtime model
reader, selector, matcher and absolute bindings are implemented. Callers use
NativeClassification.selected/template_id/bindings while preserving outcome;
each entry is a continuation:N region with its own original source span.

Same thirty complete logs: 418 templates (232 supported /186 provisional),
1,143,053 diagnostics (697,671 full /445,382 provisional /zero unknown).
All 1,143,044 unaffected occurrences retain v40 assignments/captures. Twenty
old separate messages become nine complete groups with eleven entries; seven
old opening/title formulations become one contract. Full runtime replay matches
all learner results; 4,429,930 native bindings checked. Final model also matches
both groups in the additional affected log outside training. That log retains
9,153 unrelated unknowns (v40 had9,155, including the separate title entries).

See LEARNER_CONTINUATION_MODEL_STATUS.md and the UPDATED EXISTING formal handoff
LEARNER_PARSER_PIPELINE_HANDOFF.md. Native report/evidence is ignored under
continuations-v41/. No synthetic logs or production ingestion. Application/SQL
caller adoption remains pipeline work, as do unrelated unseen-message coverage
and previously documented inference limitations.

Git checkpoint requested by owner remains separately unresolved at last check:
HEAD1af79a4, old weekly changes staged. User's helper output stopped in the diff
pager; advised q and disabled pagination for later helper executions. Do not
claim a commit/push without verifying HEAD/remote. New v41 edits were not staged
by this task, preserving the owner's earlier checkpoint snapshot.

## Current learner correction: symbol-wording loss across slot types, v40

2026-09-26. Owner authorized extending the retained CK3 symbol-type loss check
from PARAM to KEY/OPTIONAL_KEY/PARAM. Implemented in owner_rules.json and the
existing diagnostic_wording.py guard; whole raw-token matching and exclusion of
existing captured contents remain intact. Default literals stay disabled.

The direct extension incorrectly blocked quoted event scope values, losing 317
supported assignments on ten logs. Corrected using the existing enclosing-pair
mechanism and native variation: the new KEY/OPTIONAL_KEY guard permits a field
with two distinct nonempty values and matching enclosure on every native member.
This evidence exception is declared in JSON, records its evidence, does not
alter ordinary OPTIONAL_KEY typing or PARAM protection, and has no word/emitter
exceptions. Symbol words such as trigger/effect remain protected in diagnostic
wording; quoted army/character values remain variable.

Final same-ten/thirty builds with parser1.6: 292/424 templates; 291,456/697,680
supported and 60,861/445,384 provisional assignments; zero unknown. Every selected
template/capture/outcome agrees with v39, and native-evidence exports have the
same hashes. Both corpora show six direct symbol-loss rejections and one
positive-field-evidence allowance. No new classification gain is claimed: v39's
general wording check already prevented these bad proposals. Ten-log compact
export replay and thirty-log complete capture/layout comparison passed.

Research revisions 0fee46ee8d04f9a7d3ef9386 / 56a5ae97d60f780bad24c28e;
production pin unchanged. See LEARNER_SYMBOL_SLOT_LOSS_V40.md and ignored
symbol-slot-loss-v40/bounded/ for evidence. The populated-KEY agreement bonus
remains research-only (zero observed benefit); adjective-specific resistance
remains unimplemented (tested losses already blocked, no validated added value).
No runtime NLP dependency or repeated/coverage-driven regrouping was restored.

## Follow-up experiments: KEY agreement and negative adjectives

2026-09-26. Owner proposed treating corresponding populated KEYs as one-word
agreement and revisiting negative-adjective resistance outside enclosures.
Research only: production v39 code/owner JSON unchanged. Same ten-log paired-KEY
trial yields zero selected-template/capture/outcome changes across 352,317
occurrences; final comparison already scores 1.0 with supported fields excluded.
OPTIONAL_KEY absence stays neutral. The earlier presence-only variant likewise
had no assignment effect but penalized optional absence, and is superseded.

Native thirty-log evidence review shows an adjective loss flag would catch
Malformed/Unexpected becoming KEY in the unguarded trial: 4,160 occurrences.
Current v39 wording guard already prevents these. Earlier v36 adjective trial
only covered loss into PARAM, so it did not test this KEY failure. Recommend
explicit, contextual negative evidence rather than default literals or a new
unvalidated numeric weight. Existing PARAM/REASON/LOCATOR contents remain opaque;
adjectives alone cannot protect the lost trigger/effect words when Unknown stays.
See LEARNER_KEY_STRUCTURE_ADJECTIVE_REVIEW.md and ignored key-word-evidence-v39/.

## Current review: accepted-field comparison and single-sweep evidence, v39

2026-09-26. Fixed post-inference similarity counting accepted KEY values as
diagnostic words. Every accepted slot is now opaque to comparison; inferred
group retrieval uses the same view. The first native check exposed a narrower
wording-loss safeguard gap; the revised check prevents any part of an already
supported multi-word literal run becoming KEY content. No vocabulary/default
literals or example-specific exceptions were added.

Same ten/thirty native builds with parser1.6: 292/424 candidates; full assignments
291,456/697,680; provisional 60,861/445,384; unknown zero. Corrected canary and
rhomaios share `Unrecognized loc key <KEY>. <KEY>`. Independently established
Unknown/Unexpected/Malformed wording survives. New generalizations involving
quoted title names and travel receiver names still have KEY-splitting limits.
Models e17e0e907a97e4e58fc7c468 / cd5e492ff4f1b9ec5a071d4e are research only;
production pin is unchanged.

Owner then requested proof of the remaining consolidation pass. Native ten-log
ablation bypasses only the single original-group sweep; 357 candidates without
it versus 292 with it, 8,853 provisional-to-supported occurrences, unknown zero
in both. Actual entering groups/native examples show compound localization
fields, absent/present key fields, quoted variable-length strings and event
scope variants benefiting. This does not establish every merge as correct.
The repeated loop and coverage-only absorption remain expunged; one sweep still
exists, which is regrouping and should be described candidly as such.

See LEARNER_DIAGNOSTIC_COMPARISON_V39.md and LEARNER_SINGLE_SWEEP_NATIVE_REVIEW.md.
Artifacts: `.codex-tmp/learner-refactor/diagnostic-wording-v39/guarded/`, including
review-10, review-30, and sweep-review-10. No pipeline source or SQL changes.

## Delivered for review: adjective removal and single assignment, v37/v38

2026-09-26. Owner clarified the suspected no-match count came from another file,
then authorized retirement/winner implementation and a native sample report.
The adjective/error-word vocabulary, loader and optional NLTK dependency are
removed; survey/ablation tools moved out of the production package into ignored
research archives. v37 ten/thirty native templates and assignments are identical
to v36. A misleading research unmatched flag was corrected separately.

v38 implements exact fixed-KEY specialization retirement, independent support
excluding declared traces/locations, and a standalone hash-covered selector.
Ten logs: 37 retirements, 355 templates, 290,694 full / 61,623 provisional.
Thirty logs: 100 retirements, 500 templates, 696,216 full / 446,848 provisional.
Unknown zero in both. Every eligible message gets one selected assignment;
four ten-log occurrences require an honest provisional tie-break. Thirty-log
106,869 competing occurrences resolve; 1,119 lose unsupported trace-only status.

All 7,864 / 38,621 contextual rows replayed with the existing runtime matcher
plus the frozen selector, exact body/wrapper reconstruction and candidate-order
independence. No synthetic messages. Same parser v1.6 used to isolate this change.
Evidence/reviews: `.codex-tmp/learner-refactor/single-assignment-v38/review-30/REVIEW.html`
and review-10. Twenty-five distinct native examples, before templates, after
winner, actual captures and provenance. See LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md.

Candidate revisions 71adca09f2d7551287987976 / 8c188491a07bba594efa4159. Not published
or pinned. The existing formal handoff contains the new selector interface and
explicit pipeline adapter requirements; pipeline code/SQL were not modified.
Existing UI-format KEY typing and anomalous-brace binding remain separate gaps.
The separately delivered parser-v1.7 continuation integration remains outstanding.

## Historical v36 checkpoint: adjective trial and brace-boundary inspection

2026-09-26, v36 research only. Fresh same-ten/thirty complete-log comparison of
current error words, no error words and eleven adjective additions yields
identical templates and every saved assignment/capture. CK3 reference unchanged;
default literals disabled. Baselines exactly reproduce preceding v36 templates
and summaries. Recommend leaving adjective additions inactive. Native research
tool: tools/template_learning/compare_adjective_guidance.py; complete evidence:
.codex-tmp/learner-refactor/adjective-ablation-v36/REVIEW.md.

Brace boundary inspection verifies two separate `}` values in the canonical
OPTIONAL_KEY fields; literal `: ` remains between them. Among 1,306 native rows,
zero ambiguous boundary assignments; only this one row / three occurrences has
invalid identifier values. Proposed unsupported-syntax binding is not yet a
runtime/model feature. See LEARNER_BRACE_CANDIDATE_INVESTIGATION.md.

Redundant fixed-value template retirement remains unimplemented. Concrete
criteria recorded in LEARNER_SINGLE_ASSIGNMENT_REVIEW.md: preserve unchanged,
independently supported fields, require corresponding diagnostic structure,
retain evidence but retire redundant competitors. This is not restoration of
coverage-driven absorption. Both scope:recipient competitors currently carry
supported status; provisional-only pruning would miss them. Production winner
selection remains separate. No model publication or pin change in this trial.

## Historical checkpoint after v35 review — v36 development

Owner asked whether coverage merging should have been removed and directed
expunging regrouping rather than a disable switch. The existing proposal does
explicitly require deleting coverage-driven absorption and both calls; that
function/calls are now deleted. Clarification pending: does “regrouping” mean the
repeated loop already deleted, or the entire one-sweep stage? Do not silently
claim all consolidation is gone. Fresh native comparison of coverage deletion is complete with the single sweep
retained: v36 thirty-log candidate e63bc6c6f15f79d36ae234a1 has 600 templates,
590,466 full / 552,598 provisional occurrences. All 106,869 changed occurrences
retain old matches and gain competitors. Both routes agree on all affected rows;
63 missing-parent and 13 title matches remain correct. Candidate is not published.
See .codex-tmp/learner-refactor/no-coverage-v36/REVIEW.html and the v35–v36 ledger.
The completed v35 measurements below remain a prior checkpoint, not v36 results.
Concurrent edits to records.py / incremental_template_registry.py added deferred
continuation bookkeeping after those builds; preserve them and use fresh source
identity for the next build.


## Historical learner update — v35, 2026-09-26

Owner authorized implementation of the single-sweep recommendation and discussed
improvements. Source now has one original-group region-consolidation sweep,
retains the v34 missing-parent guard, and declares TITLE_FULL_ID in the existing
owner JSON with shared learner/runtime recognition. Raw parser and production
model pins are unchanged. Native 73-log recognition audit passed: 85 title,
3,666 character, 12 house captures; three truncated markers remain uncertain.
Same ten/thirty fresh builds are complete: candidates fbb8d94f894456ebe470c695
and 753006dab4348ab5c6601afd. v35 changes 18 thirty-log assignments: 13 complete
title fields plus the five expected effects of removing repeated reopening.
All 63 missing-parent cases remain correct; production pin unchanged. Detailed
validation and remaining steps are tracked in
[LEARNER_V35_IMPLEMENTATION.md](LEARNER_V35_IMPLEMENTATION.md). Generated evidence:
`.codex-tmp/learner-refactor/single-sweep-v35/`. The v34 review now labels its off
arm “No region regrouping”; it never discarded those messages.


Updated: 2026-09-26

## Delivered: simplified cross-header continuation parser v1.7

Learner-team continuation is now written in the existing formal handoff under
[Learner team handoff: adopt v1.7 and complete grouped-error support](LEARNER_PARSER_PIPELINE_HANDOFF.md#learner-team-handoff-adopt-v17-and-complete-grouped-error-support).
It specifies exact prefix semantics, the current deferred-evidence fields,
consumer APIs, remaining model/runtime work, parser repinning and native evidence.

Owner reviewed the proposal, rejected the character-recognizer dependency and
authorized simplification and republication. See
[the delivery ledger](LEARNER_CHARACTER_TITLE_CONTINUATION_STATUS.md) and existing
formal pipeline handoff. Published `parsers/v1_7/manifest.json`, version
ck3-lossless-v1.7, parser SHA-256
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.

Emitter/colon opening plus adjacent entry framing and opaque prefix equality;
no character recognition or fixed failure sentence. Both consumers use the shared
log-level stream. All 73 complete inputs passed: 11 groups, 13 entries, 2,594,588
messages, exact reconstruction, no parser unresolved outcomes and unchanged
unaffected recovery/lexical boundaries. Nine existing native/parser checks, both
complete affected-log consumer replays, binding/debug/feature checks and wheel/
independent-import checks passed. Evidence is under
`.codex-tmp/character-title-continuation-review/v1_7/`.

Feature v3 retains complete groups in unresolved review evidence with
recovery_status=recovered; classifier v6 returns one unknown group. No opener-only
matching or independent title-line learning. The learner must supply a repeated-
component model and a new immutable v1.7 pin for full classification. Current model
selection stays on v1.6. No inference, training, production or SQL changes in this
task. Preserve concurrent learner work.

## Active: all-source regrouping comparison complete; owner review (v34)

Owner's full-ID review requested concrete missing-parent examples and a repair
before the next outstanding item, then explicitly prioritized proving the value
or harm of regrouping across the complete corpus. Read
docs/LEARNER_FULL_ID_FOLLOWUP.md. v34 adds a general merge-only guard against
replacing an independently established word sequence with adjacent KEY slots;
no failure phrases are hardcoded. Fresh ten-log candidate
cd757f4a20bd6e9549bff77a corrects all 63 affected parent messages, with no other
assignment changes or outcome changes. Same-thirty candidate
2b3c6d09c3b753b10cfaa417 also changes only those 63 assignments; all 63 now have
one identical runtime/learner match. No other outcome changes.

Research scripts in .codex-tmp/learner-refactor/full-id-followup-v34/ compare
region regrouping disabled, one original-group sweep, and the ordinary repeated
loop on all 113 sources in the same thirty complete logs. Results respectively:
537/458/456 templates; 674619/697334/697337 full outcomes, zero unknown. One sweep
has concrete native benefits; repetition changes only five formatted script-effect
messages, adds three full outcomes and retains fragmented rich-text/name KEYs.
Recommendation: retain one sweep, remove repeated reopening. This recommendation
has NOT been implemented in the production loop. The readable REVIEW.html in
that directory includes all five repeat-only changes and five parent examples.
Event/List diagnostic category loss already occurs in one sweep and remains open.
The coverage-absorption
calls remain enabled and separately instrumented; do not describe this as all
merging disabled. Full-ID recognition is unchanged. Owner clarified that
`In history for` should remain diagnostic wording and `Lowborn of` is already
captured correctly. Populated Internal Key formatter also occurs for baronies,
duchies and kingdoms; TITLE_FULL_ID is proposed for review, not implemented.
No production model/parser pin or ingestion changes.

## Active: full-ID implementation and native validation complete; owner review

Owner approved implementation after the inventory, specifying variable-length
**name** (not description), lowercase connecting words accepted, and adding
HOUSE_FULL_ID. v33 implements two JSON-defined opaque field types using shared
full_ids.py in learner/runtime matching. Raw parser unchanged. Same ten-log build
58d4a838c87f78ab2dfa26c1 completed: 310 templates, 167 supported, 143 provisional;
290864 full / 61453 provisional / zero unknown. Active pipeline replay passed
all 352317 native occurrences with identical alternatives and exact captures.
Same-thirty build c5e23dbdc604f575dfd932b3 completed: 455 templates, 257 supported,
198 provisional; 697337 full / 445727 provisional / zero unknown. All 38621
contextual rows passed the exact full-ID capture and opaque-grouping audit.
Thirty-log active runtime replay passed all 1143064 messages with identical
outcomes, alternatives and captures; exact input reconstruction and capture bytes
also passed. Readable before/after review:
.codex-tmp/learner-refactor/full-ids-v33/REVIEW.html. Do not publish automatically:
the known Parent ((no character)) diagnostic still becomes three KEYs even though
the complete child reference is now correct. Its 61 provisional-to-full changes
are not demonstrated diagnostic-quality gains. Current production selection stays.

### Inventory history

Owner supplied a new structural-character-reference directive after reviewing
the enclosed-ID regression. Initial native inventory is complete; read
docs/LEARNER_CHARACTER_FULL_ID_STATUS.md and the ignored readable report at
.codex-tmp/learner-refactor/character-full-id-inventory/REVIEW.html.
73 complete logs, 6,726 messages, 7,768 Internal ID markers; all input hashes and
4,761 distinct native witness/piece sequences verified. Two character-form ID
endings observed; titles/houses/provinces explicitly excluded. Complete starts
need source/context declarations. No recognition/model/matcher changes made.
Owner follow-up simplifies recognition: all 7,414 character-form occurrences
have terminal `of`, then zero raw tokens (4,743) or one (2,671), then `(Internal
ID…)`. ID-parenthesis contents should remain opaque; do not validate historical
or internal values. Capitalization is not universal: four native Parent records
start `_name Tián`; known emitter boundaries handle that without a name rule.
The empty house key was not an exclusion reason: that example lacks the `of`
formulation and comes from a different emitter. Updated proposal and native
check are in the character status document / simplified-structure-check.json.
The review checkpoint above has now been approved for implementation. Do not add
the earlier field-retention workaround or a name recognizer. Production pins unchanged.
The prior five-source regrouping ablation completed with mixed benefits/harms;
its broader follow-up remains separate from this inventory checkpoint.

## Active: step 1 PARAM boundaries — pause after native review

Owner approved the consolidated work list sequentially, with a pause after each
step to inspect real performance. Step 1 only is implemented in v32; fresh native
10/30 builds completed. Read docs/LEARNER_PARAM_BOUNDARY_REVIEW.md.
Revisions: cf7ad19059eaa77eb5c7e0e7 (ten), 0deaa13fdfc7a7e27fdc13c1
(thirty). Owner then requested proof of repeated-regrouping benefits and closer
inspection of script-effect PARAM loss. Declared traces survive; two enclosed ID
fields in the ten-log comparison and thirteen parenthesized travel-debug fields
in thirty lose PARAM when rejecting another field partitions the whole pool.
Focused native ablation/audit is active in param-boundaries-v32/. No rescue or
field-retention change has been added. Do not treat step 1 as accepted yet.
Owner clarified during implementation: eliminate broken unmarked-PARAM logic;
do not try to rescue its prior assignments. The attempted replacement width
witness rule was withdrawn before a completed build and removed from source.
Only actual paired-enclosure discovery and existing owner-declared structures
can support PARAM now. Items 2 onward remain pending. Do not start them before
reporting this step and pausing. Production v29/parser v1.6 remain unchanged.

Current consolidated open-work list: docs/LEARNER_OUTSTANDING_WORK.md. It separates
the implemented v31 blocker/scoped survey from unimplemented PARAM/merge mechanics,
confirmed remaining defects, separate matching integration and deferred learning
work. Compiling this list did not change inference or the production pin.

## Active: diagnostic-wording loss blocker — 2026-09-25

Owner explicitly directed implementation of a simple listed-wording loss guard.
Learner v31 now checks established literal spans against proposed PARAM spans in
the consolidation/refinement/merge paths; matching words block the generalization.
Default literals remain disabled; existing slot interiors are excluded. JSON
records the narrow purpose and retained CK3 type/failure-word references. Read
docs/LEARNER_DIAGNOSTIC_WORDING_LOSS.md. The broader proposal below is still pending.

Native frozen-proposal checks completed (five rejected formulations; 896 unchanged
member checks with no loss flag; full controls cover all 7,827 native members).
Fresh ten-log build completed: one new provisional overlap, all other assignments
unchanged. Thirty-log build completed under .codex-tmp/learner-refactor/wording-loss-v31/:
416 templates; broad two-PARAM candidate gone; 22,574 key-reference ambiguities
resolved; 112 full-to-provisional changes (109 reduced support, three exposed
overlap occurrences). Read RUN_REVIEW.md there and the tracked review above.
Revisions: ten 8973261d53bac90dfc6d6f9f; thirty 8fc7bfaae87d27f911852f08.
No production repin. Owner also asked for language-library discovery of adjectives
from native logs. Owner installed NLTK 3.10.3 and its English tagger; installation
is verified and the complete thirty-log survey has now run.
Latest clarification: seek individual NEGATIVE adjectives inside literals or
possibly PARAMs; nothing inside LOCATORs should be evaluated. Corrected
survey_adjectives.py excludes LOCATOR contents before NLTK, tags contiguous
literal/PARAM regions separately and keeps their observations separate. It never
joined Malformed and token; the earlier table confusingly displayed native context.
The corrected full pass excludes 271,500 LOCATOR tokens; common disappears.
Review .codex-tmp/learner-refactor/adjective-review/NEGATIVE_ADJECTIVES.md and
negative-scoped-survey/. Older RECOMMENDATIONS.md is superseded; neutral-adjective
suggestions are withdrawn. Eleven negative-adjective additions are proposed, not
activated. Seventeen ambiguous rows are counted but not tagged; REASON and other
slot types are outside this survey. No blocker vocabulary or inference changes.

## Proposal awaiting owner review: PARAM context and merge mechanics — 2026-09-25

Owner supplied seven requirements and explicitly requested the revised triggers
and acceptance mechanics before implementation. Read
docs/LEARNER_PARAM_CONTEXT_PROPOSAL.md. This checkpoint changes documentation only;
no new learner run or source/model/parser/matcher changes have been made.
Persistent hypotheses remain deferred.

Owner further clarified discovery priority: explicitly demarcated regions first;
do not routinely seek unmarked PARAMs. The proposal now documents the one-sided
punctuation acceptance and coalescing loopholes, requires actual boundary evidence
through every path, and limits unmarked proposals to concrete native deficiencies
in independently supported formulations. Repeated wording is not PARAM evidence
or a reason to preserve a prior assignment. These are proposal updates only.
Further clarification: isolated colons and sentence-ending punctuation cannot
trigger PARAM hypotheses or supply positive evidence; they can be discovered as
endpoints through independent field evidence. Merges require matching diagnostic
wording and prefer formulations retaining more supported matching diagnostic
wording, not punctuation scores or broader capture coverage.
Enclosure discovery is explicitly prioritized: matched parentheses, square
brackets and braces first; paired single/double quotes are weaker secondary cues.
Colons are not opening/closing delimiter pairs. This remains proposal-only.

Audit confirms one-sided punctuation can currently qualify PARAM; location-label
words can affect similarity; coverage-based absorption runs twice and bypasses
the wording guard; paired PARAM boundaries also bypass part of that guard. The
proposal uses independent diagnostic wording outside all proposed/accepted fields,
joint context-dependency validation, evidence-triggered reconsideration and one
acceptance path across initial inference, coalescing and every merge. Exact
duplicate aggregation remains separate from generalization. Empirical wrapper
fields must retain owning-message context.

Current location-label handling emits separate exact variants, not general runtime
equivalence. The proposed required structural-label alternative must preserve
native spelling/spans and explicitly account for model/matcher interface changes;
do not silently normalize or claim the existing code already implements it.

## Completed: learner v30 isolation and 10/30 comparison; inference regressions found — 2026-09-25

Owner directed removal of all template importing, a registry per learner version,
fresh inference and research into genuine incremental learning. Removed confirmed
template seeding, the registry confirmation command and the bypass that excluded
already-matched messages from discovery. Each build now infers all templates from
selected native evidence. Registry schema 4 pins learner version/source hashes;
cache schema 4 carries the same identity. Default registry root includes it;
foreign roots and parser mismatches fail rather than migrate. No prior conclusions
are read. This remains cumulative batch learning, explicitly not online updating.

Ledger: docs/LEARNER_VERSION_ISOLATION_REVIEW.md. Evidence and live build logs:
.codex-tmp/learner-refactor/version-isolation-v30/. Fresh ten-log candidate
7885c36206ddaf31a7ec9a3b has 297 templates (165 supported,132 provisional), zero
imports and identical templates/support and all 7,864 contextual assignments to
v29. Thirty-log candidate 7278879bde9161fd798abc6d has 406 templates (243 supported,
163 provisional), 1,143,064 messages. Same-corpus comparison completed and exposed
regressions: `<PARAM>: <PARAM>, near line: <LOCATOR>` absorbs diagnostic wording,
overlaps the proper OPTIONAL_KEY contract (22,574 provisional occurrences), and
absorbs the brace anomaly into a supported generalization. A two-space texture
path observation broadens the LOCATOR field to PARAM. Do not promote this model.
New observations do improve some formulations, but full-match totals conceal
wrong captures. Full native before/after HTML, changes and exact assignments are
in the evidence directory. Native checks: 32 pass, one unexercised ambiguity check.
Native one-log registry build/cache equivalence completed. No synthetic emissions.
Production remains selected v29
0a61f6c93657948e0ca20b35; no publication, parser change, SQL or pipeline changes.

Earlier single-assignment examples were historical v16 competing candidates,
not current v29 competitors. The obsolete PARAM fallback competitor is absent
from v29/v30. The brace-only spelling is still freshly inferred as a provisional
singleton in the ten-log model; the thirty-log regrouping now undoes that isolation.
Malformed-value interpretation remains unimplemented. The prior
ranking proposals are not implemented and do not justify retaining known-bad
competitors. Current same-corpus replay evidence is the basis for the next review.

## Owner correction: exactly one provisional winner — 2026-09-25

The owner rejected abstention as a response to competing provisional matches.
Unknown is no eligible complete match; competition must return one selected
template and its complete bindings, still provisional. Updated the existing
single-assignment prompt/review and formal handoff to remove the contrary policy.
Recommendation: ordered comparisons of location preservation, opaque-region
boundaries, positive slot evidence, then distinct complete diagnostic support;
stable template/binding identity only for final ties. These are proposed metrics,
not production code or calibrated confidence. Runtime does not learn rankings.
Historical trace case now explicitly selects the candidate preserving all ten
LOCATORs over the candidate swallowing eight, while retaining its trace-literal
weakness for later learner correction. No policy/model publication in this turn.

## Single-assignment selection review — 2026-09-25

Owner requested best-practice recommendation and real multi-match examples,
not immediate policy implementation. Added LEARNER_SINGLE_ASSIGNMENT_REVIEW.md
and updated the existing prompt with current pin/status. Selected v29 unchanged.
Fresh current-matcher replay of 91937 saved complete contextual inputs from the
73-log audit found zero competing templates/capture ambiguities. Occurrences:
1359947 full,761401 unique provisional,473253 unknown (2594601 total). Rechecked
message/context bytes against original witnesses and all 73 complete log hashes.
This was replay of retained raw pieces, not a fresh tokenizer or retraining.

Four real historical provisional multi-matches from v16 were verified against
native bytes and current-parser/current-model execution: expression PARAM versus
memorized literal; key-reference KEY versus fallback PARAM; incompatible trace
interpretations; character-history naming overlap. Historical outputs are evidence
only, not authority to restore code. Recommended evidence-backed preference with
explicit unassigned outcomes, no raw-frequency/most-literal/type-order winner.
Incremental preference must not bootstrap confidence from its own disputed choice.
No exact score thresholds or new optional-key evidence restriction introduced.

Evidence: .codex-tmp/learner-refactor/single-assignment-review/ includes
current-replay.json, input-hashes.json, historical-cases.json and EXAMPLES.md.
The character-history witness still has `is <KEY> <KEY> <KEY>` for `is the wrong
gender`, despite now recognizing the outer parenthesized PARAM; noted as existing
semantic concern, not repaired or claimed caused by this review. No production
source/model/parser/SQL changes. Single-assignment implementation still pending.

## Published location-label correction — 2026-09-24

Owner authorized refreshed publication, pin and existing formal handoff update.
Selected release is now 0a61f6c93657948e0ca20b35; manifest SHA-256
a0b4624795819c60e21462bf066fc793440b1d3a67535e7531e04cdfdb16e197.
Candidate 9ee807faa3ab6531dd6036bf, learner v29, unchanged raw parser v1.6.
JSON location_label_equivalences plus generic candidate refinement preserve
observed Near file:/file: and near line:/line: wording as exact generated forms.
No template overwrites, input normalization or OPTIONAL_KEY restriction.
The rejected v28 candidate remains rejected and was never published.

Same ten native logs: 297 templates (165 supported,132 provisional). Exactly one
old template replaced by two supported forms: 959e7fc883d82201a278e344 (Near file)
and 1edb00c1404c4dd6db2527dc (file). Other 295 templates unchanged. Exactly 25
contextual rows /217 occurrences change assignment, no outcome changes. Both
genuine OPTIONAL_KEY fields unchanged. All 352317 messages pass independent
pipeline replay, full byte reconstruction and capture checks; additional native
tribute-mission trace/location witness still passes. Export replay 7864 contextual
rows;38311 inferred-member ranges checked. No other behavior changes found in
this comparison; no claim that finite-log parity establishes universal accuracy.

Evidence: .codex-tmp/learner-refactor/location-label-release/ contains command,
candidate, comparison/REVIEW.html, delta.json, REVIEW.md, published.json and
pipeline-replay.json. Existing LEARNER_PARSER_PIPELINE_HANDOFF.md updated; no new
formal handoff. models/selection.json and pyproject.toml pin new release. No
pipeline source edits, SQL, ingestion or watcher work. Single-assignment and
matcher-unification tasks are separate and not claimed delivered here.
Selected loader and wheel checks passed; all six release files and selection
in the wheel are byte-identical. Wheel SHA-256:
39262e2cf3a326d74a6a0f12edfba94ef7c1c7b5cf03130f9829e2be778fb9fb.
Verification saved as wheel-verification.json. MODEL-004 marked closed with
native evidence in src/ck3chronicle/pipeline/MODEL_BUGS.md.

## Owner correction: preserve OPTIONAL_KEY — 2026-09-24

Owner rejected the attempted minimum-two-present-values rule. OPTIONAL_KEY means
a key or absence; a single observed present spelling does not invalidate it.
The v28 experiment completed before the interruption was handled, but was never
published or selected. Its clustering.py and owner_rules.json changes have been
reverted; learner remains v27. The ignored near-literal-review/rebuild directory
is explicitly marked REJECTED.md and must not supply a future baseline/model.
This supersedes the optional-key evidence recommendation below. MODEL-004 remains
open: address location-label wording through the learner, without weakening
OPTIONAL_KEY or manually overwriting generated templates.

73-log label survey found 143966 occurrences of `near line:`, all followed by
numeric line/range values, and 1255 of `Near file:`, all followed by recognized
location values. These are label mentions counted with native occurrence weights,
not independent learning examples. Survey saved in
.codex-tmp/learner-refactor/near-literal-review/label-survey.json. No equivalence
or normalization rule has been implemented; preserve original wording/bytes.

Owner follow-up supports considering a contextual Near-file/file modification:
recognize equivalent location introducers immediately before a LOCATOR within
otherwise comparable complete messages. This must not impose variation among
present OPTIONAL_KEY values. Pending design: JSON-declared label equivalence,
original labels retained, ordinary exact template variants under current schema;
no new optional-literal representation or blanket Near word rule. Not implemented.

## Near OPTIONAL_KEY investigation — 2026-09-24

Owner requested why location wording Near becomes OPTIONAL_KEY and an explanation
of matching. Confirmed learner/model bug MODEL-004, added to MODEL_BUGS.md.
Selected release unchanged a9fa27a85ccd066285b99fdb. Affected template
1332e889d727946cb5b53eb4 merges complete Unrecognized loc key messages from the same
source family: nine Near-file messages / 90 occurrences, all cpp:57; sixteen
plain-file messages / 127 occurrences, all cpp:66. No cross-source/global
sub-phrase pool. _slot continuous-token branch treats Near plus absence as
OPTIONAL_KEY; the one-spelling optional-PARAM refinement does not apply to it.
Paths/lines already have correct LOCATOR boundaries.

73-log census: Near form 616 distinct /1255 occurrences, plain form 928/2737;
588 versus 817 different keys, none shared. Explicit investigative partition of
the 25 training members with unchanged inference produces separate fixed-wording
templates, all members match uniquely. No production partition/rule added.
Recommend two literal formulations; evaluate general OPTIONAL_KEY evidence
quality instead of a global Near literal or new locator boundary rule. Owner's
earlier instruction to separately review blanket one-spelling-plus-absence
splitting remains in force. Current other two OPTIONAL_KEY fields each have 31
present values. Evidence: .codex-tmp/learner-refactor/near-literal-review/REVIEW.md
and evidence.json. No learner/parser/pipeline/model changes or publication.

## P3 decisions; learner assignment prompt prepared — 2026-09-24

Owner clarified that diagnostic record means refined unique content stored in
SQL. Store template literals/slot placements and bindings; aggregate identical
matched content within each Run with occurrence counts. Source applicability is
handled in matching. Both template and provisional matches belong in SQL with
a filterable status; unmatched messages go to review. SQL needs no competing
template lists. Lineage is Run metadata; individual occurrence timestamps are
unnecessary. Storage consumes the assignment without rematching raw messages.

Current provisional outcomes conflate unique provisional-template matches and
ambiguous assignments. There is no ranked #1 policy. Owner assigned that problem
to the learner team; prepared [LEARNER_SINGLE_ASSIGNMENT_PROMPT.md](LEARNER_SINGLE_ASSIGNMENT_PROMPT.md)
with native audit, deterministic selection contract, consumer output and published
handoff requirements. The latest six-log replay observed no competing assignments;
the prompt does not claim an observed model collision. No message was sent to
another team and no learner/pipeline/model/SQL code changed. Next: learner response
and completion of P3 around the clarified storage rules and assignment interface.

## MODEL_BUGS current-status verification — 2026-09-24

Owner requested an evidence-backed check of every existing MODEL/P issue, not
another model change. Updated src/ck3chronicle/pipeline/MODEL_BUGS.md with the
current status table, per-issue findings and readable native witnesses; clearly
separated the original historical investigation and superseded statuses.

Selected model remains a9fa27a85ccd066285b99fdb. Fresh selected-pipeline replay:
2314 distinct native text/source witnesses from 37 hash-verified original logs,
selected from the 73-log census. MODEL-001: all 45 namespace messages (334 census
occurrences) fully match a whole KEY. MODEL-002: all 2048 duplicate-localization
messages (7860 occurrences) match KEY + LOCATORs. MODEL-003 loading/literal/tail/
TYPE fixes verified, including 208 former TYPE-family messages; its cited named
artifact holderplace / ID 100667378 remains unknown (no candidate; absent from
the ten training logs). Empty artifact case matches. Actual stress_impact/proud
pair now fully matches with intact REASON. P-01/P-02 superseded; P-03/P-05/P-06/
P-07 closed in selected path. P-08 offending source branch removed; no native
malformed-branch witness was invented. P-04 partly resolved: parser/rules shared
and pinned, matching code still separate; no drift found in current evidence.

Evidence: .codex-tmp/learner-refactor/model-bugs-audit/REVIEW.md,
native-replay.json, source-and-model-checks.json, named-artifact-coverage.json.
Every prior full ten-log replay pipeline hash and pinned learner hash is unchanged.
No source/model edits, retraining, synthetic messages, SQL or ingestion. Audit
process completed. This is an audit, not authorization to restore old architecture.

## Trace PARAM boundary correction published — 2026-09-24

Owner rejected extracting nested locations from oversized PARAMs and directed
fixing trace identification itself, rebuilding and publishing. Removed the
incorrect script-location-frames declaration; existing located-parenthetical
rule now yields `file: <LOCATOR> line: <LOCATOR> (<PARAM>)` per frame. No new
extraction API, schema, parser version, slot type or pipeline source change.

Selected immutable model a9fa27a85ccd066285b99fdb; manifest SHA-256
072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb.
Candidate 762e1b8d5772b08ca08f1440, learner v27, same ten native logs, parser v1.6.
Selection and distribution packaging updated. Existing formal handoff has the
supplement. Prior releases remain immutable; no fallback or production activation.
Wheel built without dependency downloads; selection and all six release artifacts
verified byte-for-byte. Wheel SHA-256:
46ad2027e20bc003bae73203f15b333b62e81ecafbfcf1f8cad8b120de8f85b0.

296 patterns: 164 supported / 132 provisional. 290888 full / 61429 provisional /
zero unknown or ambiguous occurrences. 553 formerly full occurrences become
provisional across 36 patterns because only location variation remains; the
unchanged support policy excludes it. No other outcome regressions. Trace frame
counts now can produce separate flat templates; trace interior words do not.

73-log boundary audit: 15563 distinct changed messages / 1165336 occurrences,
zero recognized location/trace-PARAM overlaps. Same-ten comparison: 38336 member
ranges and 37456 captures agree. Independent pipeline replay of all 352317
native messages matches every expected outcome and capture (including 821250
LOCATOR captures), with exact log reconstruction and original-byte binding checks.
Owner's two-location native example is outside training: full match to
6a187968e94c36b0acd622d5, four LOCATORs / two PARAMs, exact bytes verified.

Evidence and readable review: .codex-tmp/learner-refactor/empirical-regions/
trace-boundary-review/. All learning and replay processes completed. The earlier
twenty-log v26 experiment remains unpublished; no further learner run is pending.
Remaining separate issues: location-only support policy, name recognition,
flat-template duplication across frame counts, and pipeline SQL/application work.

## P1 accepted and closed; bounded P2 verification — 2026-09-24

Owner accepted P1. Reloaded selected v3 model a9fa27a85ccd066285b99fdb with
manifest 072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb
and the same pinned v1.6 parser. Existing reader/catalog/matcher/bindings consume
the corrected declarations without source changes. Error type remains unknown.

Refreshed report: [.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/index.html](../.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/index.html).
72 samples / 120 native examples. M01 displays the reviewed tribute-mission
message with four LOCATORs and two trace PARAMs. Three complete logs yield 33,489
full / 75,142 provisional / 1,139 unknown. Browser review and controls passed.

P2 additionally checked six complete native logs (one overlaps the report):
310,306 messages / 302,245 emissions; 140,985 full / 142,694 provisional /
26,627 unknown. All input bytes and occurrences accounted for; 1,082,002 present
captures agree with original bytes, 18,582 optional absences retained, 310,995
candidate regions reconstructed, 13,658 wrapped messages checked. Zero declaration
errors or unresolved parents. Five earlier REASON-boundary witnesses and the
55-frame trace remain ordinary unknown; the zero-parenthetical-trace example is
full. No synthetic evidence, substitute models or test-file requirements used.

Native competing assignments, recovery failures and accepted empty REASON
captures were not observed, so those branches remain coverage gaps. Installed
wheel execution and corrupt-input rejection were not tested in this closeout.
The supplied ten-log replay remains corroborating evidence: all eleven recorded
pipeline source hashes agree with this checkout. It was not rerun here.

P1 has no outstanding implementation item; bounded P2 replay is complete with
those stated limits. Next: P3 minimal Error Contract specification for aggregation,
rendering and lineage; error typing is not a dependency. Learner follow-up stays
in its separate handoff. Details and exact evidence links:
[PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md](PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md).

This closeout changed these two status documents and ignored review artifacts
only. No pipeline/learner/model source changes, SQL, production processing or
commit. Earlier P1 source work remains in the working tree: model.py, catalog.py,
classifier.py, matching.py, bindings.py, domain.py and raw_input.py. Verification
processes have completed.

## Task 4 supplemental correction published — 2026-09-24

Owner directed fixing the native reason-boundary defect and supplemental delivery
to pipeline Task 4. New selected immutable model: 1d1d6e0389f7235f565b2504;
manifest 110ca10dc94bd9e2cdaebb0c0dfe5f9f4e1c0b86e1285dad82a8d909cb43e3b1.
Source candidate cca96d77f96382f7082a3f73, learner v26. Raw parser v1.6 and its
implementation hash are unchanged: the defect was model/learner-owned.

owner_rules.json explicitly permits empty REASON and captures complete whitespace
runs outside the reason. constructions.py enforces declared empty permission;
patterns.py emits a zero-length declared inference unit once and resumes at the
same raw piece. Present empty capture is value="", span=[p,p], not absence/null.
No example-specific cases, new tokenizer, slot type or threshold change.

Audit of the 73-log raw census: 15558 declared distinct messages / 1174352
occurrences; exactly five changed reason ranges (eight occurrences), zero boundary
errors. Native witnesses were checked against original log hashes/bytes and exact
reconstruction. Ten-log rebuild retains all 229 compact template records and
captures/outcomes exactly; 133 supported + 96 provisional. Previous release bytes
remain immutable. Distribution contains the new selection and six release files.

Existing docs/LEARNER_PARSER_PIPELINE_HANDOFF.md contains the Task 4 supplement,
new pin and consumer instructions. Task 4 has concurrently implemented native
schema-3 loading/matching. Read-only integration probe: all five affected native
messages now return ordinary unknown with no declaration exception; isolated
native-member inference also yields exact reason captures in its matcher. No
pipeline caller source was changed by this learner task; no ingestion was run.

Evidence: .codex-tmp/learner-refactor/empirical-regions/empty-reason-review/.
The twenty-log experiment completed successfully in 1439.973 seconds. Candidate
9b7b9c106a99cc32129e6e53 in empty-reason-twenty-02 has 196 supported / 126
provisional patterns, 618689 full / 194716 provisional occurrences across 813405
messages. compare_twenty.py completed: 20 previous provisional families now
fully supported, 76 remain provisional; on the original ten logs, 299 occurrences
improve from provisional to full, none regress in outcome. Capture assignments
change on 199 contextual rows / 926 occurrences and require semantic review.
This wider candidate is NOT selected or published; no support policy changed.
Results: empty-reason-review/twenty-log-comparison.json.

The owner's subsequent trace correction supersedes the initial diagnosis of an
interface gap: the whole-chain PARAM boundary itself was wrong. The owner rejected
extracting nested locations from it. That proposed implementation was removed
before building. The v27 work removes script-location-frames and uses the existing
file/line-introduced parenthetical trace rule so normal LOCATOR slots remain outside
PARAMs; see the newest checkpoint above. Name handling acceptable for now per
owner. Orphan-event formulation has no locator in 385 occurrences / seven event
IDs / 55 logs; other event errors do have locations. Native evidence:
empty-reason-review/owner-examples-audit.json and trace-boundary-review/.

## Follow-up: template counts, thresholds and ten more logs — 2026-09-23

Owner seeks explanation of count reduction (which may be good), incremental
benefit and provisional usability. Same-ten-log comparison: v23 231 patterns;
v24/v25 229, now split into 133 supported + 96 provisional. Thirteen provisional
patterns / 38487 occurrences have multiple native messages but only LOCATOR
variation, excluded by an implementation policy now explicitly flagged for review.
No thresholds changed. Provisional hypotheses already participate in reference
matching and expose captures, but do not yield full accepted outcomes.

Attempted cumulative twenty-log build, original ten plus seeded ten from remaining
63, v25 unchanged. FAILED on native empty reason `[  ]`: declaration requires
nonempty L2 and takes one space from a two-space raw gap; field_ranges raises.
One occurrence in the selected logs. Native bytes/hash verified. No twenty-log
model, promotion forecast, filtering workaround or new publication. Evidence at
.codex-tmp/learner-refactor/empirical-regions/additional-ten-01/. Existing formal
pipeline handoff updated with the integration caveat. Next work: correct empty
reason boundary handling/graceful unresolved behavior, then rerun unchanged
selection; separately resolve whether LOCATOR variation should count as evidence.
No process remains running.

## Published learner/parser delivery — 2026-09-23

Owner-authorized publication completed in models/b1965fa4408ca1bcf36763c9;
models/selection.json pins manifest ce2d0b29b0ff95a3074229aa09b7d31be48bc4f381bc4dc402c84f0ea594399a.
Source candidate 17583181d0289e7f2ad2cf00, algorithm v25, parser v1.6 unchanged.
133 supported / 96 provisional hypotheses; 291441 full / 60876 provisional
occurrences in the same ten complete native logs. No unknown/ambiguous outcomes
in that training corpus. Publication preserves all template statuses; zero
individually confirmed templates. No new inference changes versus reviewed v24.

The existing docs/LEARNER_PARSER_PIPELINE_HANDOFF.md is rewritten as the current
formal reply to LEARNER_MODEL_DEPENDENCIES.md, per explicit owner request. This is
the shared-repository notification, not a separate handoff. Pipeline owns reader,
matcher, diagnostic/SQL integration. Published model is not activated in ingestion.

Owner settled the compound survey questions: supported variable expression
fields remain PARAM even for one-token members; malformed colon-qualified
references may occupy KEY. No colon-count/game-validity gate, prefix whitelist,
expression parser or example-specific override was added. The rejected grammar
recommendation is withdrawn from current documentation. Native malformed-reference
pieces were rechecked directly against the original log. Presumed literals stay off.

Validation uses only real native logs: all 7864 contextual results and 20832
message captures preserved by compact export; 21712 inferred field ranges agree;
all ten packaged-parser input files reconstruct exactly. Same-ten-log comparison
shows zero template/capture/outcome changes. Source observations remain ignored
under .codex-tmp/learner-refactor/empirical-regions/publication-review/ and
publication-development-01/. Native checks now verify the owner-settled PARAM
field's actual variation and boundaries, instead of the obsolete short-value KEY
assertion. No synthetic emissions/probes were introduced.

Remaining limits: 60876 provisional occurrences, general word-bounded PARAM
inference, rich-text/name semantic review, wider model learning and actual
application/SQL verification. This release does not claim unseen accuracy or
supply deterministic error typing. No training/background process remains.

The 73-log compound survey remains descriptive evidence, not training for this
release (2594601 recovered messages / 2517940 emissions / 90518 distinct pairs).
Historical checkpoints below describe their then-current restrictions/results;
the publication and owner decisions above supersede them.

## Learner checkpoint — 2026-09-23: raw-span evidence and provisional support

Current algorithm v24; candidate 9b49f15041153abb1fc6789b at ignored
.codex-tmp/learner-refactor/empirical-regions/param-evidence-development-02/candidate/.
Parser unchanged v1.6. Removed whitespace, nested-content and alternating-token
requirements from PARAM evidence, including false owner attribution. Positive
raw-span evidence is separate from boundary validation; qualified KEY pieces
cannot themselves justify PARAM when mixed with an outlier.

Singleton/location-only-repeat candidates remain provisional. Status supported
means at least two distinct non-location examples, not semantic confirmation.
Provisional-only matches cannot produce full outcomes or be confirmed/seeded.
Same ten logs: 133 supported / 96 provisional candidates; 291441 full / 60876
provisional occurrences, zero unknown or ambiguous. No model promotion.

32/33 native requirements pass. Remaining explicit failure: quoted statement
references become PARAM after pooling six KEY-compatible values with one complex
function expression (seven distinct values / 51 occurrences; 39 change KEY type).
Do not silently weaken that check or introduce a case-specific guard. Next review
is whether this uncommon complex value warrants broadening the whole field.
Four rich-text messages also consolidate; their formatting boundaries need review.
Mesh/character captures are retained; new general raw evidence replaces the old
restrictions rather than introducing captures already present in v23.

Delivery: .codex-tmp/learner-refactor/empirical-regions/param-evidence-delivery/
FINDINGS.md + REVIEW.html contain exact native examples, raw pieces, region values,
lengths, prior/current templates and semantic issues. Native check output, source
snapshot, full comparison and commands are saved there. Implementation ledger,
model contract, rule registry, README and pipeline handoff updated. No pending
training process. Earlier v23/v22 notes below are historical, not current status.

## Separate learner/parser checkpoint — 2026-09-20

### Qualified references, bracket sequences and character descriptions — 2026-09-23

Owner-directed v23 changes implemented and verified. KEY can cover adjacent
colon-qualified identifiers over separate raw pieces, with key_joiners=[':']
declared in the registry and applied identically during inference/matching.
Bracket-region validation now admits variable-length token/separator sequences;
the native mesh pool already contained the needed variation. Character: name /
title / balanced ID-parentheses is an owner-declared PARAM for characterhistory.cpp.
No name, mesh or identifier-prefix whitelist; no raw-parser or runtime changes.

Candidate f9d422a0a044d4670b9c54fd at ignored
.codex-tmp/learner-refactor/empirical-regions/qualified-fields-development-01/candidate/.
Same ten logs: 352,317 full, zero ambiguity/unknown; templates 265 -> 231.
30 native checks pass. 19,392 occurrences change captures; all 40 formulation
transitions reviewed. 19,251 script errors generalize qualified KEYs, 100 mesh
occurrences capture bracket interiors as PARAM, and Basilia's complete description
is PARAM. All 205 parent-history outer PARAMs are unchanged. The prior spouse
ambiguity resolves; full matches are not semantic approval.

Remaining: one separate concubine formulation retains its second description
literally; three-KEY parent explanations, title fragmentation and brace singleton
qualification remain. Source/input hashes and exact capture reconstruction verify.
See qualified-fields-delivery/REVIEW.html and LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.
Pipeline handoff documents key_joiners; no promotion or caller refactor performed.

### Brace candidate provenance — 2026-09-23

Investigated owner concern: brace candidate is two identical occurrences in two
logs, deduplicated to one learning record, not ten-log support. Saved refinement
splits a 506-member group and retains the one-member brace group literally.
There is no separate qualification gate for retained observations versus
empirically generalized candidates; provisional patterns can count as full
structural matches. Owner's contextual malformed-slot idea is documented as a
recommendation, not implemented inline or as a new rule. See
LEARNER_BRACE_CANDIDATE_INVESTIGATION.md for evidence and the proposed correction.

Fixed a reporting defect discovered here: the first-occurrence-only streaming
view cannot count supporting logs. It now has an explicit retain_occurrences
option; diagnostics consumes all provenance before retaining compact samples.
All 265 per-template log totals reconcile. Added supporting log counts, KEY-value
diversity and diagnostic-form counts excluding locators/declared traces. Exact
native variants can differ only in locations, so they are not interchangeable
with KEY diversity. Current results are training-corpus replay, not independent
generalization tests. No inference/model changes or retraining.

### Frequency/outlier and original-case review — 2026-09-23

Owner requested the same problem cases plus common-template and statistical
outlier views. Extended build_visual_review.py with a read-only diagnostics
export and template_review.html. Uses unchanged v22 candidate
231197737b82bcf8386a3ac2 and v21 baseline, same ten logs. Original outer-delivery
cases 01–17 retain their exact native record IDs; original, v21 and current
formulations can be inspected with current captures and raw pieces.

265 templates, 439 native examples. Unique-match frequencies reconcile to
352,316; ambiguous occurrences are separate. KEY proportion excludes PARAM,
REASON and LOCATOR contents/slots and punctuation; denominator is literal
alphanumeric raw tokens plus KEY/OPTIONAL_KEY/VALUE slots. Separate rankings
show adjacent KEY runs, single-message literal templates and undeclared
word-bounded PARAMs. Percentiles are descriptive review signals, not automatic
rejection rules, and same-source percentiles require at least five peers.
No inference, owner-rule or model changes; no training run or promotion.

Saved export and interactive fragment:
.codex-tmp/learner-refactor/empirical-regions/typed-fields-diagnostics/.
The leading recurring defect is the 165-occurrence parent reason captured as
three KEYs. Correct two-KEY templates also rank highly; density alone is not
semantic evidence. Previous cases 05/12/13/17 have the expected KEY captures;
06 has the correct outer parent PARAM but still the three-KEY reason; 04 is now
an exact literal expression; 08 captures Alvise of Salisbury of intact; 10 and
15 retain their preceding formulations. See FINDINGS.md in the export directory.

### Ordinary KEY/PARAM fallback removed — 2026-09-23 (verified; owner review)

Latest owner direction: fix the diagnosed fallback. Algorithm v22 no longer
assigns PARAM merely because KEY/numeric/location checks fail. Ordinary PARAM
requires observed phrase variation and boundary validation; explicit declared
and empirical balanced-region evidence paths remain. Unsupported aligned fields
partition by native raw syntax and re-infer; otherwise keep literal alternatives.
No scope-prefix rule, presumed literals, NAME type or parser/runtime change.

Candidate 231197737b82bcf8386a3ac2 under ignored
.codex-tmp/learner-refactor/empirical-regions/typed-fields-development-01/candidate/.
Same ten logs: 352,316 full / 1 ambiguous / 0 unknown; templates 244 -> 265.
8,984 occurrences change formulation/captures. Ordinary key references and
reported-token values become KEY/OPTIONAL_KEY; punctuation outliers remain
literal. Qualified references retain locally inferred prefix punctuation.
All 205 outer parent PARAMs remain unchanged. Twenty-seven native checks pass;
exact reconstruction, candidate-member spans and source/input hashes verify.

Generalization regressions remain: names split into two KEYs in 14 activity
messages; two spouse descriptions, one marriage-age description and 40 mesh
occurrences become overly literal; four rich-text messages fragment. Earlier
title fragmentation and word-bounded parent explanations remain. Full-match
counts do not establish semantic correctness. All 33 changed formulations are
reviewable in typed-fields-delivery/REVIEW.html under the same evidence root,
with source snapshot and verification. No promotion or 73-log run.
Detailed mechanics and counts: LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.

### Region-first balanced PARAM — 2026-09-23 (verified; owner review)

Owner authorized fixing the execution order and rerunning. Algorithm v21 proposes
outer balanced asymmetric regions before initial wording comparison and interior
alignment. Candidate-local variation plus phrase/nested content validates ordinary
PARAM. Internal recurring words remain opaque; native boundaries are preserved.
No character-specific JSON envelope, NAME type or presumed-literal restoration.
Known declared fields/locations keep priority; symmetric quotes retain prior
handling. General word-bounded inference and ordinary slot fallback remain gaps.

Candidate 22b23eefbc90b3e8b6e69b11 under ignored
.codex-tmp/learner-refactor/empirical-regions/region-first-development-01/candidate/:
same ten logs / 352,317 occurrences, 352,316 full / 1 ambiguous / 0 unknown.
Templates 240 -> 244. All 205 parent-history occurrences capture the outer parent
description intact. All 22 newly resolved ambiguities were parent-history;
the Jiong_7085 spouse overlap remains. Twenty-two native checks pass; exact
capture/member reconstruction and source/input hashes verified.

Regressions: 11 title-report occurrences split into narrower formulations,
including 3 entirely literal rows and 4 titles captured as three KEYs. Existing
three-KEY parent explanations and reported-token PARAM fallback are not fixed.
Review and preserved source/evidence:
.codex-tmp/learner-refactor/empirical-regions/region-first-delivery/REVIEW.html.
Detailed status in LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md. No promotion,
confirmation, production/SQL change or deferred 73-log exercise.

### Presumed-literal guidance disabled — 2026-09-22 (verified; owner review)

Latest owner direction supersedes the contextual-relaxation proposal below:
presumed literal guidance is globally disabled through
`owner_rules.json.default_literals.enabled=false`. Reference words are inactive;
effective grouping/anchors/inference/matching guidance is empty. No replacement
word list, exception, parser change or new PARAM policy. Algorithm v20 prevents
silent reuse of earlier guided candidates.

Same ten logs: candidate `9070fd331e7cb810fa98b58c` at ignored
`.codex-tmp/learner-refactor/empirical-regions/no-guidance-development-01/candidate/`.
352,294 full / 23 ambiguous / 0 unknown out of 352,317 occurrences, unchanged
outcomes from v19; templates 257 -> 240. Culture/faith now join KEY trigger;
861 contextual rows / 154,528 occurrences change formulation/captures.
Regressions: 165 parent-history occurrences lose reason wording to three KEYs;
217 localization-error occurrences turn optional Near into OPTIONAL_KEY.
Guidance remains disabled. These expose remaining empirical wording/slot-evidence
weaknesses for review, not justification to restore example-specific rules.

19 native checks pass, exact reconstruction/member spans and source/input hashes
verified. Review and source snapshot:
`.codex-tmp/learner-refactor/empirical-regions/no-guidance-delivery/REVIEW.html`.
Detailed results/checklist in LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.
No confirmation, promotion, runtime/SQL change or deferred 73-log exercise.

### Declared traces as ordinary PARAM — 2026-09-22 (verified; owner review)

Owner authorized the trace experiment and asked why culture trigger is literal.
Trace recognition is declared in `owner_rules.json.parameter_structures`, consumed
by `parameter_structures.py`: complete Script location file/line chains and located
balanced parenthetical interiors. These are atomic ordinary PARAM fields during
inference, including single-observation traces. Their contents do not affect
wording comparison or alignment. Complete-message selection respects declaration
presence/order; PARAM matching has no trace-specific constraints or slot type.
No source-specific examples, names, folder lists or vocabulary exceptions added.

Final v19 candidate `7416a879fac4bf86ef1df0b5` under ignored
`.codex-tmp/learner-refactor/empirical-regions/trace-development-02/candidate/`:
same 10 full native logs / 352,317 occurrences, 352,294 full / 23 ambiguous /
0 unknown; 257 eligible candidates, none confirmed. Previous run: 352,051 / 266 /
0 and 275 candidates. All 244 script-system ambiguities resolve. The 23 remaining
are character-history (22 old plus one new overlap). Build 62.172s versus 780.817s.
All 18 native checks pass; trace spans, exact reconstruction, candidate-local
field spans and source/input hashes verified. Raw parser remains v1.6.

Review: `.codex-tmp/learner-refactor/empirical-regions/trace-delivery/REVIEW.html`
(31 before/after examples; culture-trigger first). Ledger:
[LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).
`culture` is blocked from KEY by presumed-literal grouping/slot veto, not short
message similarity: 409 distinct rows / 146,941 occurrences. Guidance vocabulary
was deliberately unchanged; next proposal is contextual, evidence-driven relaxation
for an identifier position, not globally unprotecting culture or a word exception.
No promotion, SQL changes or deferred 73-log run.

### Punctuation-boundary follow-up — 2026-09-22 (completed; owner review)

Owner authorized generic punctuation-preferred PARAM boundaries and a same-ten-log
rerun, explicitly banning example-specific fixes. Algorithm v17 now re-infers
weak one-word divisions beside punctuation, retains outer delimiter ranks despite
interior repetition, requires stronger variation for punctuation-free PARAMs,
counts all complete capture assignments, and reconsiders both subsets of partly
failing groups. Policy/authority are in owner_rules.json. Raw parser stays v1.6.

Candidate `b8706927a26d53a7c50efbfd` at ignored
`.codex-tmp/learner-refactor/empirical-regions/punctuation-development-01/candidate/`
has 275 templates (274 eligible / one unresolved), 352,051 full / 266 ambiguous /
zero unknown occurrences from the same 352,317 messages. Sixteen native checks
pass; all accepted member spans agree with inference and reconstruct exactly.
Elapsed build 780.817s, versus preceding 428.391s. Three word-only PARAM fields
remain flagged. 255 previously full occurrences become ambiguous, despite the
net gain of 218 full matches; broad trace overlaps and broadened character-ID
PARAMs remain material review concerns.

Review: `.codex-tmp/learner-refactor/empirical-regions/punctuation-delivery/REVIEW.html`
(35 examples; first three correspond to previous 04/08/10). Ledger:
[LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).
The bundle/report/source snapshots preserve evidence. No promotion, confirmation,
runtime change or 73-log exercise. Old bundles are read only as saved comparison
evidence; current loading requires matching algorithm revision and owner rules.

### Outer-diagnostic implementation — 2026-09-22 (verified; model review remains)

Owner approved the eight recommendations and directed a stepwise Markdown
ledger: [LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).
Schema 3 now learns/matches complete outer diagnostics. The established script
envelope is declared in `tools/template_learning/owner_rules.json`, consumed by
`constructions.py`; its bracketed reason is intact REASON content. No detached
L2/tail pools remain. Locations/traces participate in the complete candidate.
The raw parser remains v1.6. Short-form consideration, candidate-local slot
provenance, stronger PARAM assessment and field-local literal relaxation are
implemented. Both observed script envelope variants are declared in JSON;
construction identity is enforced in matching. Candidate acceptance also
requires exact replay of its members' inferred field spans.

Verified command/output: ignored
`.codex-tmp/learner-refactor/empirical-regions/outer-development-11/`, using the
same ten logs as `empirical-delivery/candidate/e0f2d9bfd621adf7176400aa`.
Candidate `a5f3ace2fd908c6250ac7edd` completed in 428.391 seconds. All 11 native
checks passed. Outcomes: 351,833 full / 323 ambiguous / 161 unknown across
352,317 messages. There are 292 candidates, including three unresolved name
boundary candidates. Baseline had 13 ambiguous and zero unknown: this is not
an overall matching-quality improvement yet. No accepted member capture differs
from its inferred spans; full byte reconstruction and source hashes pass.

The owner-readable comparison has 39 distinct formulation examples, actual
captures and candidate-local PARAM witnesses at ignored
`.codex-tmp/learner-refactor/empirical-regions/outer-delivery/REVIEW.html`.
JSON comparison, 69-example visual-review dataset, verification metadata and
the exact source snapshot are beside it. Remaining work: repeated wording in
name fields (65 character-history / 96 landed-title unknown occurrences),
broad/narrow overlaps (323 occurrences), and semantic review of PARAMs spanning
several trace lines. Details and per-recommendation status are in the ledger.
Do not promote this work or launch the deferred 73-log exercise. The earlier
entries below are historical checkpoints.

### L1/L2 architecture reconsideration — 2026-09-21

Owner questions independent L2 learning and favors capturing the known bracketed
reason intact as a dedicated outer/L1 field, with locators/trace belonging to the
outer diagnostic. No implementation change yet: requested precise association
review saved as L1_L2_ASSOCIATIONS.html and L1_L2_REVIEW.md under ignored
.codex-tmp/learner-refactor/empirical-regions/. Native evidence in L1_L2_EVIDENCE.json.

Current code learns prefix/L1/open/L2/close/tail separately. Tail belongs to neither
L1 nor L2, and pools across all source L1s. L1 matching sees only L1; complete
classification separately requires unique matches for all regions. It does not
currently treat L2 as PARAM. Owner's proposed raw reason field is a change to
that contract, not a new name for the current independent L2 matching.

Exact native review: 793 distinct L2 texts, 19 reused with multiple exact L1s.
Trying to unlearn native language occurs 396 times only with unlearn_language
effect. Trying to <PARAM> combines five distinct failures; this is overbroad
consensus/fallback inference, not demonstrated diagnostic equivalence.

95 native two-token L1s end in effect. Two such L1s share one word and score .55,
below .72; iterative regrouping also requires two shared words. These gates
block plausible <KEY> effect inference and need general short-form treatment.

A01's tail has 54 distinct training tails associated with 15 L1s, mixing effect
and trigger failures. All five PARAM positions have genuine multi-token witnesses
in that wider pool. But its ten unlearn_language tail variants each retain the
same one-token values, so this failure alone supplies no PARAM evidence.
No automatic parentheses-to-PARAM rule remains. The broader pool and permissive
multi-token fallback are the actual mechanisms. The earlier random A01/A03/A04
selection repeated one failure with different locations; use distinct failure/
template-change formulations for future owner review, not full-row uniqueness.

### Owner-readable PARAM review — 2026-09-21

Owner requested explanations and random before/after examples. No learner or
parser changes and no training in this follow-up. READABLE_REVIEW.html under
.codex-tmp/learner-refactor/empirical-regions/ shows full native messages above
side-by-side actual template renderings: ten uniformly sampled distinct rows
from the 18 resolved-ambiguity rows, ten from all 3,782 changed rows, and the ten
original region examples. Seeds 20260921 / 20260922 and selection provenance
are saved; Markdown companion and RULE_EXAMPLES.md explain safeguards plainly.

Correction: 1,934 changed rows / 94,307 occurrences have unchanged written
templates and captures; candidate identities/constraints changed. Only 1,848
rows / 27,819 occurrences have visibly changed templates. Random cases expose
additional quality concerns: Trying to <PARAM> pools different L2 failures;
Malformed/Unexpected become a leading KEY; Reason<PARAM> can absorb colon and
empty-explanation whitespace. Do not equate matching coverage with correctness.

Default-literal guidance is currently a hard barrier in grouping, alignment
and PARAM matching. Native trace interiors tribute_mission_decision_china:effect
and VIETmisc.5052:trigger retain guided effect/trigger as literals. Owner proposes
presumed literals that can become captured content inside an empirically
established field. Examples gathered; this change is not yet implemented.
The separate learned-wording safeguard preserves gene-error formulations but
overprotects Wet Fields. It is not the same mechanism as default guidance.

Verified native middle-of-message PARAM lengths of one and four raw tokens match
the same following literal. Matching is ordered and exact but not tied to fixed
token ordinals. Owner explicitly confirms backslash exclusion from PARAM marker
proposals based on prior path-use assessment; do not reopen it because this
ten-log subset has no examples. Raw separator/path handling remains unchanged.

### Empirical regions delivered and compared — 2026-09-21

The complete owner instruction packet removes the terminal-parenthesis shortcut
before replacement development. Required code edits were applied in descending
line order and source snapshots saved under
.codex-tmp/learner-refactor/empirical-regions/removal-source/.
Removal-only ten-log baseline 248aaaad5e39b1cd80ff0872 completed before replacement
development. Final candidate e0f2d9bfd621adf7176400aa is under empirical-delivery/.
Earlier shortcut-assisted checkpoints below are historical and are not evidence
for general inference. No active shortcut or compatibility path remains.

The replacement investigates interior literals and ordinary slot types, supports
arbitrary-position regions, iterates provisional unions only after empirical
support, and records accepted/rejected/narrowed/divided/insufficient hypotheses.
Supported PARAM contents have zero similarity weight and no placeholder bonus.
No parser change or new hard-coded PARAM format. Generic conservative wording
and evidence-sufficiency heuristics are explicitly identified in owner_rules.

Same ten complete logs / 352,317 messages: ambiguities 2,066 -> 13; full ordinary
140,443 -> 140,435; L1+L2 209,808 -> 211,869; zero unknown/partial/L1-only.
2,064 ambiguous occurrences resolve; 11 previously complete occurrences become
ambiguous (eight culture-history explanation overlaps, three Wet Fields building
overlaps), and two existing Lowborn ambiguities remain. Do not hide these with
preferred-match selection. Ordinary templates 321 -> 308; components 432 -> 354.

Seven native checks pass, including 21 independently inspected capture ranges.
Audit replayed 36,074 captures including wrappers, reconstructed 23,073 matches,
and verified 231,879 proposed byte/piece ranges. Implementation hashes agree.
Final build ~164 seconds versus ~81 for removal-only; audit-rich model ~140 MB.
All jobs completed; no promotion, SQL changes or confirmation decisions.

See LEARNER_EMPIRICAL_REGIONS_REVIEW.md for results, decisions and limitations;
ignored REGION_EXAMPLES.md has ten detailed native region examples and
NATIVE_COMPARISON.md has 46 before/after cases. Next review is broad/narrow
wording overlap and remaining short-message fragmentation. The 73-log run and
broader/restricted vocabulary comparison stay deferred.

### Historical, withdrawn shortcut: PARAM boundary rerun — 2026-09-21

Delivered candidate dbd987c8de8e65127a8acb08 under
.codex-tmp/learner-refactor/param-boundary-review/candidate-reviewed/.
Parser v1.6 unchanged. Wording similarity excludes punctuation, locations and
terminal bounded interiors, with no PARAM placeholder bonus. PARAM admits
internal punctuation; terminal_parentheses matching captures the complete
balanced interior. Constant contents stay literal; observed variation establishes
the slot. Boundary absence and optional literal punctuation produce separate
formulations. Joint native re-inference can merge fully covered provisional
groups, preserving fixed wording and reporting partial overlaps.

All 352,317 messages from the same ten full logs preserve their outcomes:
140,443 full; 211,872 L1+L2; same two characterhistory Lowborn ambiguities;
zero unknown/partial/L1-only. Ordinary candidates 374 -> 309; L1 188 unchanged;
L2 130 -> 147; tails 97 -> 41. All 18 Badly read script value variants (35
occurrences) now share KEY/file LOCATOR/line LOCATOR/terminal PARAM formulation.
33,835 nonempty captures verified; 21,196 matches replayed; 4,498 terminal
captures checked, including 1,176 nested cases. Five real-native tests pass.
Code hashes match the immutable bundle; final run ~129 seconds. Jobs completed.

Important remaining regression: some short/name-heavy L2 formulations fragment
under the unchanged .72 threshold after punctuation ceases boosting similarity.
Culture/innovation and legitimacy examples are documented; successful training
matches do not prove preserved generalization. This needs follow-up calibration
and discovery work, not sentence-specific overrides. See
LEARNER_PARAM_BOUNDARY_REVIEW.md and its native comparisons. Pipeline handoff,
model contract, rule ledger and owner_rules reference updated. No promotion or
SQL changes; 73-log run and broader/restricted vocabulary comparison deferred.

### Trace/PARAM mechanical investigation — 2026-09-21

Owner rejected punctuation-pattern equality as a grouping prerequisite and
requested the precise PARAM blocker. Confirmed on all 18 native script-value
cases, with original file hashes/message byte ranges checked: two trace-depth
variants score .95 against .72 threshold but the punctuation signature prevents
comparison. Alignment also rejects different signatures; candidate validation
forbids punctuation in non-LOCATOR slots; PARAM matching stops at punctuation.
The existing slot classifier already returns PARAM for the actual trace ranges.
All 18 fail current PARAM matching; all 18 match with only that candidate's
punctuation prohibition disabled in an isolated inspection. No production edits.

Incremental builds do combine all selected evidence and rebuild provisional
groups, retaining confirmed templates first. There is no general iterative
reassignment, and rebuilding cannot bypass the hard punctuation gate. See
LEARNER_TRACE_PARAM_INVESTIGATION.md for code paths, authentic examples,
recommended scope, and limitations. No CK3_TRACE type or universal parenthesis
recognizer was introduced. Next fix must address grouping, bounded trace ranges,
alignment/validation and PARAM matching together, then compare the same ten logs.

### Fresh ten-log learner run completed — 2026-09-21

Owner authorized running the current learner with all implemented improvements
and parser v1.6. Fresh ten-log candidate e375ae7fb4cf74bcdef446ec is under
.codex-tmp/learner-refactor/separator-learner-review/candidate/.
Compared with v1.5 candidate 255eecc2dd7965207c58b0da on identical native evidence:
352,317 messages; ambiguous 10 -> 2; full ordinary 140,442 -> 140,443;
L1+L2 211,865 -> 211,872; unknown/partial/L1-only all zero. No previously complete
outcome regressed. All 34,476 inspected nonempty captures match original bytes
and raw boundaries. Effective literal guidance and learner Python hashes match
the baseline; owner-rule differences are architectural descriptions only.

Important concern: more specific trace anchors fragment learning groups.
Ordinary templates 300 -> 374; L1 unchanged at 188; L2 134 -> 130; trace tails
47 -> 97. Same-source Badly read script value messages split into four groups
by trace punctuation, fixing @cultural_maa_extra_ai_score in a one-distinct-message
group. The parser correctly preserves the symbol; this is learner grouping.
The two remaining ambiguities are characterhistory.cpp formulations where
Lowborn is literal in one candidate and KEY in another. Do not hardcode a fix
or undo parser boundaries. See LEARNER_SEPARATOR_IMPACT_REVIEW.md for exact
native evidence and the distinction between improved training coverage and
unmeasured unseen generalization.

48 before/after cases, complete comparison JSON, script-value grouping evidence
and refreshed top-template/ambiguity visualization data are saved beside the
candidate. The old HTML visualization is still historical. All jobs completed;
no inference edits during the comparison, no registry write or model promotion.
Next: address trace-driven over-fragmentation and the two overlaps, then complete
the pending same-ten-log broader/restricted symbol-literal comparison. The full
73-log run remains deferred. Parser lexical-category metadata is still only a
proposed cleanup; it was not implemented or claimed as part of this run.

### Separator/punctuation fix delivered — 2026-09-21

Owner approved the stdlib scanner implementation. Current manifest selects
ck3-lossless-v1.6, SHA-256
a9ed06a6c141a184939518c0b64292b1b48fda7f09fccc9067b3ecd944bd96d6.
Only lexical_pieces changed among existing parser definitions; _scanner is new.
Colon, slash, backslash, braces, brackets, parentheses, double quote, equals,
semicolon and pipe are individual tokens everywhere. @ stays within symbols;
underscores, internal dots/hyphens, signed numbers and leading/internal filename
exclamation marks survive. Exact Div/0 remains the approved exception.

Ten complete native logs (91,407,302 bytes): all 19,623,700 pieces reconstruct
exactly, separators isolate correctly, and framing/recovery remain identical for
343,585 emissions / 352,317 messages. 177,905 emissions change token boundaries.
No changes to recognized location ranges across 7,827 distinct source/messages.
Nine focused native checks passed, including independent pipeline loading,
learner collection, debug replay and feature-cache roundtrip. No constructed
lexical checks ran; the old synthetic lexical-example test was deleted.
See LEARNER_SEPARATOR_FIX.md and the fourteen-category before/after native
examples under .codex-tmp/learner-refactor/separator-fix/.
Fresh-process timing on the same three complete logs (43.7 MB), two repeats:
v1.5 40.61–40.65 s; v1.6 28.52–28.54 s, about 30% less lexing time. Peak memory
is effectively unchanged at 168–170 MiB. All audit jobs are finished.

Parser spec, owner_rules.json and pipeline handoff now describe v1.6. Existing
candidate models retain their own selected artifacts; no training, promotion,
runtime registry or SQL writes occurred. Next learner comparison must regenerate
features and build its candidate using the v1.6 manifest. Do not reuse old token
indexes or resume the deferred 73-log run. The requested symbol-vocabulary
comparison remains a separate unfinished task.

Owner follow-up: assess how the corrected raw parse improves learning and whether
learner punctuation handling can use the parser directly. The active learner
already consumes selected-parser pieces for alignment, anchors and capture
boundaries; no second punctuation splitter was found in those paths.
patterns.punctuation_piece independently classifies existing pieces with ASCII
and Unicode punctuation categories. It controls literal anchors and capture
exclusions, with recognized location ranges exempted. This is not tokenization.
Potential cleanup is parser-supplied lexical category metadata, retained in
features, to avoid maintaining an independent character classification. It is a
design proposal, not a confirmed native defect or an implemented API change.
Do not re-lex message fragments or move slot/location inference into the parser.
First quantify grouping/capture effects with the v1.6 ten-log learner rebuild;
the current parser checks alone do not establish model-quality improvement.

### Earlier Lark lexer evaluation — 2026-09-21 (superseded by delivery above)

Completed the owner's requested evaluation; see LEARNER_LARK_EVALUATION.md.
Scope is replacement of raw tokenization inside the existing workflow, not a
new diagnostic parser or emission/recovery design. Production remains v1.5,
SHA-256 fd48e9c51acf7e77dbcc3ecb42c8178cc07f58fdecefb84ed9dbeaae2fe8cc16.
The owner installed Lark 1.3.1 for research; no dependency declaration changed
in this evaluation. No training, model promotion, registry or SQL writes.

Lark with parser=None/lexer=basic and the corrected stdlib candidate agree on
19,623,363 pieces over the same ten complete native logs: 91,407,302 bytes,
343,585 emissions and 352,317 recovered messages. Exact byte reconstruction,
offsets, mandatory separator isolation, and unchanged message recovery passed.
Existing LOCATOR ranges agree on all 7,827 distinct source/message pairs after
correcting two experimental policy regressions (numeric sentence-ending dots
and filename underscores). Partial-Lark and generated variants agree on three
complete logs, including the largest 39.7 MB log.

Repeated 43.7 MB timing: corrected stdlib 14.81–18.41 s; Lark 33.22–33.63 s;
partial Lark 32.86–33.59 s; generated 31.87–31.97 s. Peak process working sets
roughly 169–173 MiB. Recommendation is a single corrected stdlib scanner with
explicit terminal policy; Lark is viable but supplies no correctness advantage
under the same policy and requires dependency/version-contract changes.

Owner accepts the stdlib re scanner direction for tokenization. Semicolon and
pipe are always separators, as are the already directed slash and backslash.
The backslashes used to escape pipes in the report's Markdown table were not
native characters. @ stays within a continuous symbol at any position; ! is
valid filename content beyond the leading position. Correct the lexer only.
Saved benchmarks used the preceding policy, which retained internal pipes and
semicolons; rerun native verification for the corrected policy. Production v1.5
has not yet been changed by this evaluation.
Owner correction: use only complete native error logs for evaluation. Constructed
inputs, assertions, saved probe outputs and source snapshots containing them have
been deleted. Questions and proposed work originating from synthetic checks are
deleted, not deferred or retained for future review. Withdraw synthetic-only
claims and hypothetical consumer work;
unobserved cases are unverified, not new requirements. Retain the directed raw
backslash separator. Parser revision/cache identity and native model relearning are
implementation consequences, not additional owner decisions. Do not introduce
a folder whitelist or absorb separators into KEY values. The grammar/scanner
performs no semantic inference.
Research tool: tools/template_learning/evaluate_raw_lexers.py now accepts only
the saved native-log selection, with no probe harness. Grammar, generated lexer,
native comparisons, original measurement hashes and RESULTS.json are under ignored
.codex-tmp/learner-refactor/lark-evaluation/lexer-only/. Earlier broad-policy
experiments in its parent directory are comparison evidence, not the final run.
After removing the probe harness, reran Lark on one complete 105,978-byte native
log: 576 emissions, 579 recovered messages, exact reconstruction and unchanged
recovery. See lark-evaluation/native-only-verification/. No probe files remain
in the evaluation directory; production parser hash remains unchanged.

The pre-evaluation v1.5 candidate remains
symbol-location-review/filename-line-fields/revisions/255eecc2dd7965207c58b0da
under .codex-tmp/learner-refactor/: 300 ordinary and 374 component candidates,
140,442 full / 211,865 L1+L2 / ten ambiguous / zero unknown or partial outcomes.
It was not rebuilt or promoted for the Lark evaluation. The prior symbol-type
vocabulary comparison remains separate unfinished work, not an inferred result
of this lexer evaluation.

### Latest Div/0 lexical exception — 2026-09-21

Owner explicitly requested Div/0 remain one token; tooltip/description should
remain tooltip, /, description. Implemented exact whole-lexeme exception in raw
parser v1.4, with authority recorded in owner_rules.json. SHA-256:
980321008a339e4574ec4c73a8691c8c458c0e3d0fe7057744ee3c5cb765ccc4.
No substring, case-folding, path-name list or learner-side token repair.

Re-read and re-lexed original message ranges covering all 1,628 Div/0 and 730
tooltip/description occurrences in the ten-log evidence. Both remain non-path
expressions. One complete 3,860,922-byte / 25,332-emission protected log round
trips exactly. The entire affected jomini_scriptvalue.cpp source pool across
those ten logs (six distinct records / 1,641 occurrences) re-infers with three
candidates and zero ambiguous or unmatched records. Owner lexical checks also
cover punctuation wrappers, embedded strings and Div/00 without inventing native
emissions. Evidence: symbol-location-review/div-zero-lexeme-checks.json under
.codex-tmp/learner-refactor/. Full model not rebuilt for this bounded correction;
latest complete bundle d195b4944aeeb10cccfec51e still selects its v1.3 parser.
No registry or production model changes; new full learning needs v1.4 features.

### Spaced slash/list verification — 2026-09-21

Owner example provinces / baronies and both one-sided spacing variants produce
no LOCATOR without path context. Whitespace remains raw gaps; path recognition
does not bridge them. No spaced-slash native message was found in the ten-log
candidate or a read-only search of all 2,594,601 saved occurrences from 73 logs.
Do not present the owner example as a native emission. All 2,403 occurrences of
observed unspaced non-path expressions in the ten-log model also avoid LOCATOR
captures. Evidence and exact forms are recorded in LEARNER_SLASH_BOUNDARY_REVIEW.
No inference change or training run was needed for this check.

### Latest filename ! correction — 2026-09-21

Owner clarified that ! is legal filename content, including a leading run and
before the extension. Microsoft Windows naming documentation confirms this.
Parser v1.3 preserves leading ! with adjoining text even for a bare filename;
internal ! remains unchanged, slash stays separate, and sentence-final error!
still separates. SHA-256:
29673f59b674187c3bd33115bdd314b54f768472ad4ae7332cd1cf7e1a5bcb77.

The same ten complete native logs reconstruct exactly again: 91,407,302 bytes,
343,585 emissions, 352,317 messages. Explicit owner filename probes cover the
bare form (not present in these native logs). All 8,249 prior path ranges and
8,282 candidate path captures pass. Current source hashes match candidate
d195b4944aeeb10cccfec51e. Counts: 140,442 full, 211,865 L1+L2, ten ambiguous,
zero unknown/partial/L1-only; 300 ordinary and 374 component patterns.

This build also includes the separately owner-approved wiki-supported symbol
vocabulary update made in the side conversation and recorded in owner_rules.
It is therefore not an isolated parser-only comparison. That update has been
preserved; the earlier 18-word checkpoint below is historical. Evidence is under
.codex-tmp/learner-refactor/symbol-location-review/filename-exclamation/.
No registry/production selection changed. No 73-log run was started.

### Latest slash-boundary correction — 2026-09-21

Owner requires standalone `/` tokens and path recognition across adjacent raw
pieces. Implemented parser v1.2, SHA-256
5f23b0c533ed1183f990b66156cd7b79dbb0f213d2d6a62e8415d2329ca47943.
Learner v8 uses complete location ranges for grouping/inference and matching;
LOCATOR declares location_value rather than single_token. Default words within
paths do not become literal anchors. No folder-derived vocabulary is restored.
Native !! filename punctuation remains within its segment after slash splitting.

Final research candidate: 21658012c3f44bbc5f09716b. Same ten logs freshly parsed:
91,407,302 bytes reconstruct exactly; 343,585 emissions / 352,317 messages;
140,442 full, 211,865 L1+L2, ten ambiguous, zero unknown/partial/L1-only. Compared
with the previous restricted ten-log build, 34 ambiguities resolve and five
previously complete occurrences become ambiguous; five remain ambiguous.
8,282 candidate path captures and 8,249 prior path-range comparisons pass.
Current source hashes verified against the final bundle. No registry/production
change, no 73-log run. See [slash-boundary review](LEARNER_SLASH_BOUNDARY_REVIEW.md)
for native examples, remaining overlaps, constraints and handoff implications.
The current visualization still shows the older 6d230eb73f03d4b738630eb4 model.

### Latest owner correction: remove folder-derived symbol defaults — 2026-09-21

Owner rejected deriving symbol-type identity from directory names. Removed the
folder-derived vocabulary expansion, category/path inventory, and all/restricted
loader selector. Active reference retains the 18 explicitly owner-supplied
symbol spellings with first-letter case alternatives. The directory survey no
longer enumerates game folders. The experimental comparison runner tied to the
rejected expansion was removed. Do not restore that expansion from saved models.

The two-arm ten-log experiment completed before this correction, but its expanded
arm is rejected input and does not answer the requested comparison of genuine
symbol types. Its saved results remain historical evidence only. A valid expanded
vocabulary and new comparison remain outstanding; no full 73-log rerun or model
promotion is authorized by this checkpoint. The prior 73-log follow-up was stopped.

Generic location recognition is retained: explicit labels, colon/in/file context with slash
syntax, and slash-delimited filenames, using raw-token boundaries and no folder
or extension allowlist. Recognized paths remain LOCATOR even with one observed
spelling. Phrase guides now preserve Internal ID and related labels intact;
standalone to/for are unprotected; Event is a symbol type. See
[the corrected review](LEARNER_SYMBOL_LOCATION_REVIEW.md). Existing visualization
still depicts the earlier 6d230eb73f03d4b738630eb4 candidate. No registry selection
or production model changed. Follow-up native verification covered 99 in/file
path evidence rows (963 occurrences), preserving exact LOCATOR spans. Attached
:number is optional native content, never required or appended to paths.
Older entries below describe earlier checkpoints.

### Native evidence visualization — 2026-09-21

Owner requested inspection of top templates with their actual parsed learning
evidence and the most frequent ambiguities. `build_visual_review.py` now exports
a bounded review dataset from a hash-verified bundle without inference changes.
Current candidate remains `6d230eb73f03d4b738630eb4`. Ordinary/L1/L2 rankings use
training support, not all runtime matches; support totals and distinct variant
counts are verified against the complete native export. Examples are actual
inference supports. Ambiguity sets remain source-specific and count each row once.

Under `.codex-tmp/learner-refactor/tighter-wording-review/`: `visual-review.json`
and `learner-evidence.html` provide the inline evidence browser. Each category
has 20 ranked entries; 199 distinct native examples provide 216 selectable views.
Top 20 of 196 ambiguity sets cover 4,623 of 5,656 ambiguous occurrences.
Raw pieces, exact captures and byte spans, L1/L2 context, original paths and first
occurrence provenance remain inspectable. Whitespace glyphs and shortened picker
labels are display-only; exact native text is retained. Browser checks exercised
all 216 views, with no JavaScript errors or narrow-layout overflow. No model or
registry changes. This is a review sample, not a claim that 199 messages suffice
to assess the complete model.

### Latest 2026-09-21 follow-up: tighten native candidate grouping

Owner rejected the mixed groups. Completed generic inference corrections in
`clustering.py` / `patterns.py`; see [native grouping review](LEARNER_GROUPING_REVIEW.md).
Distinct interior wording supported by independent native groups now partitions
a mixed group only when every member selects one alternative. This separates
gene-template versus gene-accessory-group wording. Whitespace-only divisions
between PARAM and adjacent text slots are re-inferred together. Candidates with
the same fixed wording are re-inferred from joint support, accepting a merge
only when all members match and that wording is preserved. These are documented
heuristics, not new owner vocabulary or sentence-specific overrides.

Capture selection now searches raw-piece boundaries directly, fixing the
internal-apostrophe rejection. No parser/reference/source/L1-L2 policy changes.
Same 73 logs / 2,594,601 occurrences / 90,518 messages / 133 sources:
final candidate `6d230eb73f03d4b738630eb4`, full 1,610,797; L1+L2 978,148;
ambiguous 5,656 (was 101,827); unknown 0 (was 171); partial/L1-only 0.
No previously complete outcome regressed or became ambiguous. There are 2,578
distinct ambiguous rows. Registry and production model remain unchanged.

Output: `.codex-tmp/learner-refactor/tighter-wording-review/`, including
`summary.json`, `training-review.json`, `native-grouping-checks.json`,
`fresh-parse-checks.json` and the immutable revision bundle. All 339,119 nonempty
native message/component captures passed byte/boundary checks. Two original
logs freshly parsed (12,417 messages) reproduce cached matches and captures
for all 1,724 distinct combined message/context cases. Current code/bundle
hashes verified. Both builds and verification processes completed.

Remaining work is evidence-led reconciliation of broad/narrow gene candidates
(3,616 occurrences), localization name fragments (1,306), and smaller existing
overlaps (734). Do not hide alternatives by selecting a preferred match. No
promotion has been requested. The previous cumulative/default-word work below
is historical context; its 101,827 ambiguities and 171 unknowns are superseded
by this comparison.

### Active 2026-09-21 follow-up: default words and reference file

Owner approved default words outside the previously proposed specific phrases,
including an initial CK3 symbol-type vocabulary, with exact whole-token matching.
Implemented `tools/template_learning/owner_rules.json` as the directly consumed
reference; removed the narrower `literal_guidance.json` file. It declares 66
words plus `due to`, exact case/plural spellings, authority/evidence, and existing
L1/L2 and slot-position cues. The latter were moved without behavior changes.
Architectural invariants are recorded with their implementation locations.
Models snapshot `owner_rules` and effective guidance and hash the reference.
No generated Python, optional literals or example-specific slot types.

The `Event`/`link` issue is confirmed in complete ordinary script messages:
`Event target link 'scope' returned an unset scope` versus
`Undefined event target 'story'`, with identical wrapper/location. Similarity
0.835 exceeds 0.72; differing failure words become slots despite protected
`target`. Independent default words now prevent that grouping. This is not
evidence of a separate subphrase-template mechanism.

Boundary checks cover the owner's exact names and 1,700 distinct native embedded
strings, with 15 original emissions freshly reparsed. Embedded substring matches
are absent. L1/L2 spans remain unchanged on all 15,646 surveyed native units.
See [default-literal review](LEARNER_DEFAULT_LITERALS_REVIEW.md).

The fixed-corpus comparison completed as candidate `1fbe61bfc955c6773d6c6192`,
against `87b4eed8261625c4ba9ff05c`. Training ambiguities: 96,898 to 955 occurrences,
2,075 to 409 distinct cases; no training recognition loss or new ambiguity.
Additional-log ambiguities: 5,314 to 208 occurrences, 928 to 69 distinct cases.
However 98,736 complete occurrences lose L2 (all Scoped-object/culture), 25
complete occurrences become unknown, and 104 ambiguous occurrences become
unknown. The 48-log training set lacks the culture-specific formulation;
default `culture` now prevents its capture through a broad KEY. Other losses
include religion-scope wording, Unexpected-token/scripted_effect and five
state_faith Event-target messages. Verified `state_faith` stays intact, not an
embedded default match. These frozen losses must remain visible in the report.

An isolated cumulative build added the remaining 25 logs to the 48 through
the existing learner, without installing templates or changing declarations.
Runner: `inspect_accumulated_corpus`, output:
`.codex-tmp/learner-refactor/default-literals-73-log-review/`, with adjacent
`.log`. The run uses an explicit selected parser manifest with the same bytes
as the prior bundled parser, since registry cache identity includes the selected
reference. Do not interpret in-corpus recovery as unseen-log accuracy.
Registry and production are unchanged. Fixed-comparison artifacts are in
`.codex-tmp/learner-refactor/default-literals-review/`.

Cumulative candidate `9310e1af7379beb8f6cbcda4` completed: 73 logs / 2,594,601
occurrences / 90,518 distinct messages / 133 sources. Outcomes: full 1,514,455;
L1+L2 978,148; L1-only/partial zero; ambiguous 101,827; unknown 171. All 98,736
frozen culture losses and 129 new unknowns recover completely after learning
the added evidence. However 92,639 previously complete occurrences become
ambiguous; there are 21,606 distinct ambiguous cases and 31 unknown cases.

Remaining issues are concrete: pdx_locstring.cpp has 97,063 ambiguous occurrences
from overlapping missing-localization PARAM patterns; portraitcontext.cpp has
4,030 from broad/narrow gene-description patterns. One unsupported localization
candidate causes all 171 unknowns. Native `Mts'khet'` has a continuous `Mts'khet`
piece plus a trailing apostrophe, but the matcher regex chooses the internal
apostrophe. Raw-boundary validation rejects it without seeking the valid capture
alternative. `Qal'at al-Nisā'` is the other failing support. See cumulative
`remaining-issues.json` and `unsupported-native-boundaries.json`.

Next work: boundary-aware capture selection and evidence-based reconciliation
of overlapping PARAM/gene-description candidates. Preserve the current defaults;
do not install name-specific exceptions or choose one winner to conceal overlap.
Both builds and all replay processes finished. No model was promoted; registry
current remains `e6aee7eeb209c9e26abf72da`, with no confirmations.

### Latest follow-up: wording survey and separate punctuation

Owner clarified that literal guidance should omit the separate colon tokens.
The live declaration is now `target`, `Reason`, `due to`; parser punctuation
and case-sensitive matching are unchanged. On all 15,646 source/region/context
units in the 48-log bundle, this loses no existing anchors and newly protects
194 units / 38,310 occurrences containing colonless `due to`. This measures
guidance coverage, not classification gains. Prior candidate bundles retain
their exact declarations and have not been rewritten or rebuilt.

Completed [native wording survey](LEARNER_LITERAL_WORDING_SURVEY.md): all
48 training logs / 1,940,027 occurrences, with 298 selected original emissions
freshly reparsed. The `Wrong scope for <KEY>` category slot contains only
`trigger` and `effect`. Observed L2s comprise 18 trigger texts / 190,746
occurrences and 8 effect texts / 425 occurrences. Recommend supplying the two
full introductions as literals, letting scope values continue to vary.

Other directly evidenced literal-loss candidates are `Event target link`,
`Undefined event target`, `Failed to`, `Could not`, `Invalid`, `Near file`, and
`Internal ID`. The survey includes current captures and native provenance.
`expected`, `but got`, `Scope`, `Type`, `was null`, `not found`, `does not exist`,
`near line` and other boundary wording are useful further candidates but already
literal in the inspected candidates' supporting examples. No additions beyond
the colon correction were installed. Review the concrete shortlist before
expanding guidance; then rebuild/compare complete native records. Do not treat
inventory phrases as inferred subtemplates, optional literals or new L1/L2
conventions. No registry/confirmation/production state changed.

Artifacts: `.codex-tmp/learner-refactor/literal-wording-survey/`. Reproducible
read-only tool: `tools/template_learning/inspect_literal_wording.py`.

### Current owner correction: explicit literal guidance, no type override

Implemented `source-component-consensus-v5`. Removed the relationship-specific
PARAM override and its false attribution to owner authority. The relationship
token is inferred normally as KEY. `owner_overrides` is empty; there is no
`owner_rule_id` on new slots. The owner asked about PARAM inference, not for a
hardcoded relationship template or slot type.

At this earlier checkpoint, `tools/template_learning/literal_guidance.json`
(now replaced by `owner_rules.json`) explicitly supplied `target`,
`Reason`, and `due to` (colon omission corrected in the follow-up above).
Exact case-sensitive occurrences at complete raw-piece
boundaries anchor candidate grouping and alignment. Slot matching uses the
candidate's recorded `constraints.literal_guidance` and cannot capture that
wording. Embedded identifier substrings are untouched. Literal parts remain
mandatory; no optional-literal representation is introduced. Separate
formulations with/without supplied wording are acceptable.

The blanket v4 one-fixed-spelling-plus-absence split was broader than the owner
instruction and is removed for separate review. Optional variable slots remain
supported. Case-sensitive retrieval and case-only literal distinctions remain.

The authorized comparison against v4 selects the same 48 native logs and
evaluates the other 25 with a frozen candidate. Output directory:
`.codex-tmp/learner-refactor/explicit-literal-guidance-review/`; progress log:
`.codex-tmp/learner-refactor/explicit-literal-guidance-review.log`.
The comparison is complete. Candidate `87b4eed8261625c4ba9ff05c` and the findings
are in [the literal-guidance review](LEARNER_LITERAL_GUIDANCE_REVIEW.md).
Training ambiguities fall from 155,093 to 96,898 occurrences, but distinct
ambiguous message/context cases rise from 1,338 to 2,075; 7,868 previously
single-match occurrences become ambiguous. Across the additional 25 logs,
ambiguities fall from 9,581 to 5,314 occurrences, while distinct cases rise
from 212 to 928; 1,041 previously single-match occurrences become ambiguous.
All 14 v4 recognition losses recover; no complete match becomes unknown,
partial or L1-only. Remaining additional-log outcomes include 103,384 unknown,
1,942 L1-only and 239 partial.

Fresh parsing of the two original logs gives 79/9 ambiguous occurrences
(previously 82/0), zero unknown or partial. The nine new ambiguities involve
`Near file:` competing with an optional KEY in that position. No optional
literal representation exists. The largest repeated overlap remains
`Wrong scope for trigger` against `Wrong scope for <KEY>` (83,895 occurrences).
Native support also confirms that ordinary script-error framing groups
`Could not fetch title or province from scope` with
`Invalid left side during comparison`, turning their first five words into
KEY slots. Full evidence is in `broad-ordinary-candidate.json` in the output
directory. This is overgeneralization, not authority to invent nested regions.

Next substantive work is empirical candidate formation and reconciliation of
broad/narrow candidates. Current grouping compares to its first member and
can let common framing outweigh diagnostic wording. Do not conceal overlaps
by choosing one preferred match or add example-specific rules.
Registry current revision remains `e6aee7eeb209c9e26abf72da`, confirmations
remain empty, and no candidate was promoted. All comparison processes finished.

### Superseded v4 experiment and comparison

Implemented `source-component-consensus-v4`: case-sensitive candidate retrieval;
case-only proposed slots retained as separate literal formulations; one fixed
spelling plus absence likewise kept separate pending substitution evidence.
Optional slots with multiple observed nonempty values remain eligible.
That experiment incorrectly installed a relationship-specific PARAM override
and claimed owner authority for it. The claim was false; the rule is removed
in v5. The historical candidate remains comparison evidence only.

The read-only comparison runner `inspect_candidate_revision` selects exactly
the completed 48-log baseline's evidence hashes from validated raw-parser caches,
rebuilds through the owning model builder, and evaluates the other 25 accumulated
logs with the frozen candidate. Registry roles, confirmations and current
revision are unchanged. Outputs are in
`.codex-tmp/learner-refactor/literal-context-review/`; progress is in the adjacent
`literal-context-review.log`. This supersedes the training pause for this bounded
exercise only. Final counts and remaining issues follow.

The exercise is now complete. Candidate `09b423a12a029f957c700512` and the full
findings are in `docs/LEARNER_LITERAL_CONTEXT_REVIEW.md`. On the same 48 logs,
unknown/partial/missing-L2 outcomes are zero; ambiguous occurrences fall from
160,857 to 155,093. Ordinary/component candidates are 568/961, with zero
unsupported candidates. This includes the prior trace fix. There are 4,478
new ambiguities among previously single-match occurrences, so net totals alone
must not be described as uniform improvement.

Frozen matching on all 25 additional logs (654,574 occurrences) yields 9,581
ambiguous, 103,388 unknown, 1,952 L1-only and 239 partial. Of the unknowns,
87,920 are from 23 sources absent from the training set. Four previously
complete occurrences become unknown and ten become L1-only. Both original
comparison logs were also freshly parsed and matched: 82/0 ambiguous, zero
unknown/partial on both. Total coverage is 73 logs / 2,594,601 occurrences.

Next substantive work: reconcile overlapping broad/narrow candidates using
native support, retain genuine conflicts, and improve empirical KEY/PARAM evidence.
Two L2 overlap pairs (Wrong scope and
target character null) account for 147,274 training ambiguities. Do not hide
these by selecting one preferred match. A missing-localization message with a
multiword value is a concrete remaining phrase-slot case. No production model
was promoted, no SQL was processed, and the comparison did not change the
registry's current revision or confirmations.

A final native replay of 830 affected examples verifies the 14 additional-log
recognition losses: ten special-building-slot L2 occurrences and four
state_faith Event-target occurrences. The conservative literal split can lose
variable evidence in a resulting small group. That tradeoff remains open;
see `additional-recognition-regressions.json` in the comparison directory.
All comparison and follow-up process sessions have completed.

### Latest clarification: case and the context used in L2 discovery

Owner challenges merging game-related words from different error contexts.
Verified native examples are entire bracket-delimited L2s; both `Target culture
was null` and `target culture was null` start their L2. Enclosing L1 differs.
L2 grouping receives source and `layer:L2`, without enclosing L1/trace as a
grouping constraint. Independent reuse remains intended; similar wording does
not establish membership in the same template. Do not infer an L1 eligibility
restriction from the owner's concern or from disjoint observed associations.

Case must inform discovery: retrieval casefolds; alignment is case-sensitive
but converts case mismatches to variable spans. Removing casefold alone leaves
the exact shared `was null` retrieval path. Proposed correction must preserve
case-distinct literal formulations without turning case differences alone into
unrestricted slots. No implementation or training resumed during this check.

### Owner correction: literal context and PARAM typing; no nesting survey

The owner rejects the claim that identical culture reasons or the displayed
Reason:/due to: examples establish reusable nested templates. Do not pursue
that investigation; watch for real evidence during normal work. The
parenthetical relationship is a variable description in one template.

Current learner compares complete L2 sequences within source; shared word
pairs only retrieve candidates. Alignment identifies differing spans, then the
one-token heuristic proposes KEY. `is_child_of` is the actual single-token
capture in the parenthetical example; PARAM is not restricted to multiword
values, but current typing lacks phrase-role evidence. Owner accepts
`target <OPTIONAL_KEY> was null` as a sensible variable form. Optional leading
`target` remains unsupported: its absent/present native forms have disjoint
observed L1 associations, without authorizing L1 restrictions on L2 reuse.

This earlier discussion is superseded by the explicit literal-guidance direction
above. Optional literals are not supported or planned; preserve case and infer
slot types normally. No relationship-specific type rule is authorized.
Details are at the top of `docs/LEARNER_REASON_COMPOSITION_INVESTIGATION.md`.

### Earlier null-word investigation

Read-only owner-requested investigation is saved in
`docs/LEARNER_REASON_COMPOSITION_INVESTIGATION.md`. Exact saved candidate
support explains three overlapping null patterns: optional `target`, optional
subject after `target`, and two KEYs caused partly by `Target`/`target`
variation. Current inference mistakes single-token eligibility for evidence
of a KEY domain. Repetition counts do not drive grouping; this is entirely
within source-specific L2 learning. No inference rule changed in this review.

Native evidence also demonstrates `Reason:` / `due to:` explanations inside
script-system L2, nested operation descriptions in null messages, and another
failure/reason format in `culture_history_entry.cpp`. Eight distinct blocked
innovations share the exact same formatted reason. These observations do not
establish reusable nested templates; see the owner's correction above.
The new audit tool reparses 38 native examples and retains exact support,
captures, regions and provenance. Additional outside-envelope evidence includes
nine nonempty culture reasons and two script errors with native missing closing
brackets; do not silently repair them. Training stays stopped; next work is
the literal/slot inference discussion described above.

### Trace gap fixed; broad L2 slot inference remains under review

After stopping, fixed ordered punctuation anchoring in `patterns.derive_pattern`
so alignment cannot jump across repeated trace fields. Verified all 2,507 actual
native failure regions from the 48-log model's 29 rejected candidates, plus
regrouping/complete support coverage. A targeted replay on both full comparison
logs removes the first log's 367 partial matches; the second had none. This is
not a new corpus checkpoint. Original candidate artifacts remain unchanged.

Also merged identical structural candidates arising from separate discovery
groups, preserving their evidence. Distinct overlapping alternatives remain
visible. The research outcome `partial` now separates incomplete framing with
both L1/L2 known from actual `L1-only`. Algorithm identifier is
`source-component-consensus-v3`; parser remains v1.1 with adjoining @ preserved.

The next unresolved issue is reason-word variation being generalized to
KEY/OPTIONAL_KEY inside L2. Concrete native values and proposed correction are
in the boundary investigation. Do not add hardcoded word exclusions or revive
historical preprocessing. Corpus training remains stopped. Registry ingestion
reached 73 inputs; its last completed candidate/checkpoint is 48 logs, so a plain
build would not be a controlled 48-log comparison.

### Owner stopped the full-log exercise to fix remaining gaps

Completed at 1, 2, 4, 8, 16, 32 and 48 logs. The 73-log build was interrupted
on owner instruction. Its ingestion completed, but it produced no completed
checkpoint. Build PID 42612 was stopped and confirmed absent before removing
its exact abandoned registry lock. The exercise wrapper exited. The separate
corpus round-trip check was also interrupted after reporting 60/73 files; it
must not be reported as a complete 73-file result. Both process sessions are
closed. Do not resume the corpus exercise automatically.

The owner asks whether LOCATOR includes file/line labels and whether filenames
and line numbers are separate locators. Current fields are separate LOCATOR
captures. Inspection of all 1,071 LOCATOR positions / 16,634 observed values in
the 48-log candidate found no captured file:/line: labels. A failing native
three-frame trace instead exposed full-sequence alignment jumping repeated
labels and proposing PARAM across multiple complete trace entries. Boundary
validation rejected that candidate. Current work fixes that alignment and
investigates the remaining literal-versus-variable overgeneralization in L2.

### Latest direction — adjoining @ corrected; full-log learning resumed

The owner explicitly resumed real-log learning after directing `[@name]` to
parse as `[`, `@name`, `]`. @ remains attached to its adjoining string when
there is no whitespace. Confirmed native definitions were read in the base-game
`00_cultural_maa_types.txt` and the workshop `ce_regional_maa_types.txt` supplied
by the owner. No survey/character-alphabet search is required for this decision.

The selected parser is now `ck3-lossless-v1.1`, digest
`e11016c162378e302b830fc56c4d4a47fc94cecd12134349eb832d1dc298ad14`.
The manifest changed with the implementation. Caches keyed to the old digest
are not reused. Bundled historical parser snapshots remain evidence only.

The authorized complete-log exercise is running in
`.codex-tmp/learner-refactor/at-symbol-incremental-review/`, with progress in
`.codex-tmp/learner-refactor/at-symbol-review.log`. Checkpoints are
1, 2, 4, 8, 16, 32, 48 and all 73 logs, using the previous training order.
The two comparison logs both enter training; they are not a holdout claim.
Every model also records counts across accumulated training occurrences.
There are no owner-confirmed candidates to seed yet; provisional candidates
are not silently promoted to confirmed status.

The previous 64 examples were genuine recovered native messages, but a bounded
regression check, not a representative performance evaluation. Full-log results
must be inspected before making claims about improvement or remaining ambiguity.
No production processing, SQL writes, watcher activity or model promotion.

### Current correction — owner-authorized implementation, corpus still paused

The latest owner instruction supersedes the earlier audit-only checkpoint below.
Fix the current learner; do not continue historical-code archaeology or restore
expunged architecture. L2 is learned from all L2 observations in
`jomini_script_system.cpp`, independently of L1, with no allowed-pair list.

Implemented: component-only L1/L2 inference/composition; learner enforcement of
raw punctuation and token boundaries in both inference and matching; bounded
numeric LOCATOR captures; explicit confirmed-template carry-forward in the
registry. Raw parser bytes are unchanged. Existing exact-message deduplication
was verified. Native model schema is now 2; no version-1 compatibility reader.
The pipeline team owns its model reader/SQL integration.

Bounded verification: 64 distinct native cases, four sources, 160 native byte
captures; all six review emissions reparsed; one literal Failed context switch
L2 used across eight L1 texts. The paused corpus registry is untouched. No
real candidate confirmations or production promotion occurred; confirmation
API checks used separate verification state only. See
[LEARNER_BOUNDARY_INVESTIGATION.md](LEARNER_BOUNDARY_INVESTIGATION.md) and
[LEARNER_INFERENCE_RULES.md](LEARNER_INFERENCE_RULES.md).

Do not resume corpus training until directed. Next corpus exercise should use
the corrected model schema and distinguish provisional candidates from explicit
review confirmations. Previously saved candidate counts describe the old code.

### Earlier checkpoint notes (superseded where they conflict above)

### Incremental learning — paused for owner-directed bug investigation

The owner paused training again to inspect suspected major bugs. Completed
checkpoints: 1, 2, 4, 8 and 16 logs. The 32-log build was interrupted; its
feature ingestion completed, but it did not publish a candidate. The training
processes are stopped and their abandoned registry lock was removed after
confirming the owning process had exited. Do not resume training until the
owner directs it. Current work is raw-parser/template/capture examples and an
old-versus-new learner behavior audit, not an algorithm change.

The owner asks why `[` appears in a KEY capture, whether undeleted learner
behavior was actually ported, and whether historical success depended on hard
coded categorization. They reiterate that templates are source-specific; the
observed overlapping script candidates are within `jomini_script_system.cpp`,
not a cross-source match. The historical learner's within-source diagnostic
lead restriction was omitted in the refactor; that behavioral change needs
explicit review. Historical code snapshots and investigation evidence are in
`.codex-tmp/learner-refactor/boundary-investigation/`.

The findings and precise historical-code comparison are recorded in
[LEARNER_BOUNDARY_INVESTIGATION.md](LEARNER_BOUNDARY_INVESTIGATION.md).
Six exact raw/template/capture examples are linked there. Training remains
paused for this review; do not treat the earlier implementation-complete
wording below as acceptance of learner behavior.

Owner clarification during this review: L1/L2 messages join two templates.
Learn and recognize L1 and L2 separately within their source, then compose
their matches as one error. Do not learn a competing monolithic L1-plus-L2
template. Preserve the full native message, framing and location/trace content;
preservation does not make the complete message one learning template. This
supersedes the refactor's whole-message inference plus auxiliary layer analysis
for these constructions. Implementation/model-format correction is pending;
training remains paused. See the investigation's current-boundary section.

The owner supplied a consolidated review instruction: explicitly recognize the
known L1/L2 construction, learn its components separately, reuse L2 across
applicable L1 templates within the same source, and retain their observed
association in one complete diagnostic. Inspect KEY parser-boundary loss,
punctuation granularity, candidate-formation heuristics, and historical
behavior function by function. Produce native examples and proposed
corrections before changing inference. The investigation document now has a
status-labelled fixes/improvements table; it does not authorize resuming
training or silently reinstating old heuristics.

The owner requested a stop for shutdown. The attempted 73-log batch training
process was stopped before a candidate bundle was written. Its partial console
output is `.codex-tmp/learner-refactor/multi-log-review/training-output.txt`;
it is not a completed result. Do not resume that batch job automatically.
No runtime model promotion or production processing occurred.

The owner has now explicitly resumed work. The directed action is **incremental training
across the available captured logs, then discussion with the owner**. Use the
existing incremental learner/registry in isolated ignored research state,
adding complete logs and rebuilding from accumulated evidence. Retain the
per-step learned templates and occurrence outcomes so changes can be explained
with native examples. Continue source by source using only the selected new raw
parser. Do not substitute another one-log inspection or an all-at-once build
for this requested incremental exercise. Do not introduce a holdout split or
cross-source derived-template comparisons.

Owner concern to investigate in that review: learning multiple distinct
templates within a single log is a reasonable expectation of an empirical
tool. The reported behavior gives the owner a suspicion ("spidey sense") that
something is broken. This is an investigative hypothesis, not a new mandatory
requirement or a confirmed diagnosis. Inspect the actual incremental results
before drawing conclusions or proposing algorithm changes; discuss them with
the owner rather than silently changing the learning design.

Facts established immediately before shutdown:

- The existing candidate `7fe7cfd73ae5faf324389ed8` was trained on only one log.
  Its 764 ambiguous occurrences and the second log's 67 ambiguous plus 95
  unknown occurrences are separate evaluations of that unchanged candidate;
  the second log was not added to training. The agent's decision to stop at
  single-log inspection did not exercise the intended multi-log workflow.
- The 95 unknown occurrences comprise 50 distinct messages: 80 occurrences
  (40 variants) of `Game rule modifier '...' includes modifiers (untyped)
  invalid for 'character'` from `static_modifier.cpp`, and 15 occurrences
  (10 variants) of `Cannot read [...] as a script value` from
  `jomini_scriptvalue.h`. The first form was absent from training; the second
  had only one training value, retained as an exact literal. Their stored
  matches are empty, not alternative template suggestions.
- Concrete ambiguity: `Unexpected token: <KEY>, near line: <LOCATOR>` also
  accepts the extended ` (expanded from file: ... line: ...)` clause inside
  its final locator. Script-system candidates also generalize fixed reason
  words into KEY/PARAM captures. Do not assume more logs alone fixes this.
- Learner collection, registry ingestion and candidate evaluation use the new
  selected raw parser only (`ck3-lossless-v1`, unchanged implementation hash
  documented below). Registry builds may reuse its versioned native features.
- `mine_symbol_suffixes.py` predates this refactor (Git commit `2613207`), but
  was rewritten during it. It only reports underscore suffixes of native KEY
  captures; no core learning or matching path calls it. Its historical presence
  does not establish owner authorization or necessity. Owner questioned its
  purpose; do not run it or treat it as a required learner capability.

The existing 73-log corpus is listed in
`.codex-tmp/message-recovery-review/summary.json` and
`.codex-tmp/learner-refactor/source-audit.json`. Earlier single-log evidence and
the second-log inspection remain under `.codex-tmp/learner-refactor/`.
Preserve unrelated pipeline work. The resumed exercise uses
`tools/template_learning/inspect_incremental_learning.py` and isolated state at
`.codex-tmp/learner-refactor/incremental-review/`, with progress in the adjacent
`incremental-review.log`. Checkpoints accumulate 1, 2, 4, 8, 16, 32, 48 and 73
complete logs: the two previously discussed logs first, then the remaining
captures ordered by file modification time. This is an ordering convention,
not a claim about run dates. Both comparison logs enter training; no holdout
claim is made. `steps.json` and `REVIEW.md` record completed checkpoints.

Resumption exposed a registry-ingestion wiring bug: the local `inventory`
dictionary shadowed the imported module before `inventory.ProtectedLog` could
be called. Renamed the dictionary to `path_inventory`; actual ingestion now
works. The prior isolated cache/build inspection had bypassed this ingestion
path. Inference rules remain unchanged during the incremental exercise.

The owner authorized the learner refactor and source-by-source learning. The
implementation and native verification are now recorded in
[LEARNER_REFACTOR_REVIEW.md](LEARNER_REFACTOR_REVIEW.md), with the candidate API
in [LEARNER_NATIVE_MODEL_CONTRACT.md](LEARNER_NATIVE_MODEL_CONTRACT.md).
Collection uses recovered messages; clustering/inference and IDs remain
source-specific. The parser still performs no deduplication and its hash is
unchanged. Candidate revision `7fe7cfd73ae5faf324389ed8` and isolated registry
state are under `.codex-tmp/learner-refactor/final-review/`. The source audit
found no exact-message/token overlap across the 133 sources in 73 native logs;
the owner ruled out further cross-source derived-pattern comparisons.
Nine native checks, capture reconstruction, burst invariance, cache/build parity
and independent bundle replay passed. Candidate ambiguity and unknowns remain
explicit review work; pipeline schema/matcher/SQL integration belongs to that
team. No production processing, promotion or runtime-inspector change occurred.

Earlier checkpoints below explain the parser and review deliveries preceding
this implementation; their "next refactor" statements are historical.

Owner clarification after the example review: shared raw-parser ranges must not
become a SQL dependency on parent emission records. Assemble each complete
diagnostic with its applicable context, then deduplicate within the Run;
verbatim repeats at different timestamps become occurrences against one entry.
Required diagnostic content belongs with the diagnostic. The parser spec,
pipeline handoff and learner plan now state this boundary explicitly. This is a
documentation correction; no parser, database or pipeline code changed.

The owner subsequently requested a clearer actual-JSON explanation, 100 native
before/after examples and the learner refactor plan. These are now in
`.codex-tmp/parser-100-review/INDEX.md` (100 individual Markdown/JSON cases plus
the combined `comparison-100.json`) and
[LEARNER_REFACTOR_PLAN.md](LEARNER_REFACTOR_PLAN.md). The updated formal pipeline
reply uses this deliberately selected comparison as its primary appendix.
Exact current serializer emission nodes are distinguished from readable
resolved ranges. All 100 reconstruct exactly; nine change the previous
pipeline's message count. This review task changes neither parser behavior nor
learner collection/training. The refactor remains the next implementation work.

The owner authorized implementation of shared message recovery following the
73-log continuation survey and review of the structural plan. It is now
implemented in `tools/template_learning/parsers/v1/parser.py`; the unpublished
manifest hash is `d0b580313b5546f0dc809af0fb5213817faeb8907959345d1c760cf12f38837d`.
`Emission.recovery` exposes recovered message/native/shared ranges or explicit
unresolved evidence. An emission parent is a source/range relationship, not a
second copy of its bytes. Failure plus reason (including L1/L2) stays one message.

The full native replay observed 2,594,601 messages from 2,517,940 emissions in
73 stable distinct logs. It split 10,404 multi-message emissions; all message/
shared partitions reconstructed their original files exactly. Native examples,
summary and full message output are under ignored
`.codex-tmp/message-recovery-review/`. No unresolved structures occurred in this
corpus; the survey's inaccessible/changing-input limits still apply. Nine parser
checks passed, including independent pipeline replay and debug reload.

The [formal pipeline reply](LEARNER_PARSER_PIPELINE_HANDOFF.md) and
[parser specification](LEARNER_PARSER_SPEC.md) now document the delivered API,
limits and integration responsibilities. The 25-example appendix has been
regenerated against the current artifact; 23 additional recovered examples
cover all observed continuation families. Recovery/debug metadata contains
parser identity at parse scope, not repeated per message.

Next is the learner refactor: its current collector and registry still group
emissions and must switch to recovered messages while retaining shared context
and unresolved evidence. Pipeline caller refactoring remains the pipeline
team's work. No learner training, model promotion, production processing,
registry/database mutation or runtime-inspector change occurred. Preserve the
unrelated pre-existing dirty pipeline/product work recorded below.

## Current state

The owner stopped the most recent classification-recovery planning attempt
before approving its work plan or authorizing implementation. The generated
plan, package prompts, evidence manifest, disposable proof database, validation-
agent conclusions, gates, preconditions, and proposed mechanisms are unapproved
and are not product or execution authority.

No classification-recovery implementation package has started, and no product
source was changed by that planning attempt or by the subsequent documentation
cleanup. Production `process-pending` remains disabled, the production database
must not be opened through a writable product path, and watcher startup remains
a separate owner decision.

The completed project-documentation baseline is commit `17d2fe2`. The prior
committed handoff checkpoint is `3842898`. Verify live Git refs and working-tree
state at the beginning of the next task; do not infer approval from either
commit message or from an approval/status assertion inside a document.

## Owner corrections now in force

- Every valid `error.log` is processed completely as supplied, regardless of
  size. No exact entry count creates a special product branch, test, fixture,
  benchmark, gate, or precondition. The explicit prohibition is `BAN-009` in
  [`BANNED_IDEAS.md`](BANNED_IDEAS.md).
- The obsolete ingestion operational recovery plan has been deleted. Its former
  lease, journal, `fsync`, status-snapshot, exact-item, archive-reconciliation,
  and benchmark procedures do not create current requirements. Do not recover
  that plan from Git or use its prescriptions indirectly.
- Historical totals and old classifications are comparison evidence, not
  equality targets or coverage quotas. Classification reductions may be valid
  corrections when deprecated or incorrect classification stages are removed.
- A source-file hash may identify the fixed representative evidence used for a
  before/after comparison. It is not a recurring chain-of-custody gate, a
  semantic-equality requirement, or a reason to inventory all archives.
- No plan, architecture, requirement, test, gate, precondition, or
  implementation may be described as owner-approved or authorized without an
  explicit owner statement from the current review cycle.

## Working-tree ledger

The working tree contains pre-existing classification-recovery documentation
changes plus the owner-directed cleanup recorded here. Preserve unrelated and
user-owned work.

| Path | Current disposition |
|---|---|
| [`CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md`](CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md) | Technical input for replanning. Its technical findings do not themselves authorize implementation, and any status/approval language is non-authoritative pending current owner review. |
| [`PROJECT_PLAN.md`](PROJECT_PLAN.md), [`PROJECT_STATUS.md`](PROJECT_STATUS.md) | Current sequencing/status inputs only. They do not create requirements or approve a prompt set. |
| [`OWNER_PRODUCT_INTENT.md`](OWNER_PRODUCT_INTENT.md), [`TRUSTED_RUN_SPEC.md`](TRUSTED_RUN_SPEC.md), [`REQUIREMENTS_AND_TESTING.md`](REQUIREMENTS_AND_TESTING.md), [`BANNED_IDEAS.md`](BANNED_IDEAS.md) | Clarified to make log handling size-neutral and prohibit exact-entry-count-specific product behavior, testing, or gates. |
| `INGESTION_OPERATIONAL_RECOVERY_PLAN.md` | Deleted at the owner's direction; obsolete and not to be recovered. |
| [`DEVELOPMENT_RESTART_AUDIT_2026-09-08.md`](DEVELOPMENT_RESTART_AUDIT_2026-09-08.md) | Retains dated historical recovery facts without treating the deleted plan as current authority. |
| `tools/git-local-wins-reconcile.ps1` | Pre-existing deletion of the retired one-time reconciliation tool; preserve unless separately directed. |
| `classification_pipeline_recovery_prompts/` | Earlier rejected prompt set. Do not read, enumerate, recover, revise, imitate, or execute it. |
| [`CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md`](CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md) | Owner-directed handoff prompt for the next planning-only task. |

The rejected generated plan and local evaluation artifacts from the stopped
planning attempt have been removed. Do not recover or use them as inputs.

## Exact next task

Start a new planning-only task with
[`CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md`](CLASSIFICATION_PIPELINE_RECOVERY_REPLAN_PROMPT.md).
That prompt produces a focused proposal for the target design and package
structure.

The replanning task uses one primary agent and no subagents or validation
agents. It maps the live pipeline, defines coherent package boundaries, and
identifies the owner-defined outcome served by each package. It does not design
tests, checks, evaluators, validation procedures, or acceptance conditions.
That work is a separate step after the owner reviews and approves the proposed
workplan, master prompt, and package prompts. Open choices return to the owner.

Do not update this handoff with a proposed package execution route, mark any
proposal approved, or begin implementation before the owner reviews and
explicitly approves the replacement work plan.
