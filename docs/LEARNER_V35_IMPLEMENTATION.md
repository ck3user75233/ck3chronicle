# Learner v35–v36 implementation and native validation

**Superseded implementation checkpoint:** after this evaluation, the owner asked
why coverage merging remained. Re-reading LEARNER_PARAM_CONTEXT_PROPOSAL.md
confirmed the plan explicitly removes that function and both calls. They are now
deleted in v36 development. The results below describe v35 before that deletion.
The owner also requested expunging regrouping; clarification is pending about
whether this includes the demonstrated one-sweep stage or repeated reopening only.

Two shared-workspace source files (`records.py` and
`incremental_template_registry.py`) changed after these builds, adding deferred
continuation-group bookkeeping. Those edits were not made or reverted in this
task. The recorded v35 build identity remains the evidence for these measurements;
a fresh build is required to describe the current implementation.

Owner instruction: implement the approved removal of repeated regrouping in a
new learner version, include discussed improvements, and explicitly account for
anything remaining. This ledger supplements the existing formal pipeline
handoff; it does not replace it.

## Current v36 step

`reconsider_supported_groups` and both callers are deleted. There is no dormant
function or configuration switch. The JSON records removal as policy history.
The approved single original-group sweep is retained while the latest wording
about expunging “regrouping” is clarified. Initial grouping and exact-wording
consolidation also remain; they are not the deleted repeated loop.

Fresh same-ten/thirty native evaluation isolates coverage removal from v35's
single-sweep/title changes. Early ten-log results expose overlapping generic and
identifier-specific templates; the general templates still match. This is an
outstanding inference/assignment issue, not justification to silently restore
the deleted absorption mechanism. The completed results are:

| Same corpus | v35 templates | v36 templates | v35 full / provisional | v36 full / provisional |
|---|---:|---:|---|---|
| Ten logs, 352,317 messages | 311 | 392 | 290,864 / 61,453 | 271,028 / 81,289 |
| Thirty logs, 1,143,064 messages | 457 | 600 | 697,335 / 445,729 | 590,466 / 552,598 |

v36 candidates: ten `703ea71fcd35b1fa23af6db5`, thirty
`e63bc6c6f15f79d36ae234a1`. Thirty-log templates: 296 supported and 304
provisional. Unknown counts remain zero; no message was dropped. Both builds
use fresh native evidence and the recorded v36 implementation identity, including
the concurrent continuation-bookkeeping edits. Parser v1.6 is unchanged.

Removal changes 938 thirty-log contextual rows / 106,869 occurrences. Every one
retains all its previous matching templates and acquires additional competitors.
This is an outcome regression caused by unresolved overlaps, not disappearance
of the general formulation. Sources: jomini_script_system.cpp 106,253;
characterhistory.cpp 581; jomini_effect_impl.cpp 34; pdx_data_factory.cpp 1.
The original-ten cohort has 19,850 full-to-provisional changes under the
thirty-log models, and the added twenty have 87,019. The independent ten-log
build has 19,836 changes. Counts are not independent learning examples.

Actual most-frequent case (66,389 occurrences): the existing
`Error: <KEY> trigger [ <REASON> ]` formulation survives, while
`Error: scope:recipient trigger [ <REASON> ]` also matches. Both retain the same
file/line LOCATORs and trace PARAM. Character-history messages additionally show
KEY versus VALUE alternatives for character IDs. No winner was fabricated and
no diagnostic word was made a default literal to hide these overlaps.

The next mechanical correction must address these competing specializations
through independent diagnostic agreement and corresponding field evidence. The
coverage-only function is not being restored. General proposal/context and joint
PARAM validation remain required; no new numeric shortcut or example-specific
merge was added in this removal step. This candidate is not ready for publication.

Validation: all 187,295 captures in the thirty-log evidence retain exact native
bytes. The active runtime candidate-selection route, including source/construction/
field-structure gates, agrees with the learner on all 938 changed rows and 76
parent/title witnesses: 1,014 rows / 106,945 occurrences. All 63 missing-parent
cases keep one supported match with intact diagnostic phrases, and all thirteen
title-reference matches survive. Strict bundle/declaration/compact-template
validation passes. This is not a new complete runtime replay of every source.

Native review: `.codex-tmp/learner-refactor/no-coverage-v36/REVIEW.html`.
That directory contains all changed groups, exact source snapshot and identity,
input hashes, build commands, candidate bundles, cohort comparison and validation.
The v35 review below remains available for the separate title/one-sweep change.

## Historical v35 steps

| Step | Status | Scope and evidence |
|---|---|---|
| 1. One original-group consolidation sweep | Implemented and validated | `refine_region_groups` considers each original group once. Accepted unions are not reopened. The two separate coverage-absorption calls remain unchanged; their independent value has not been established. v34's complete thirty-log ablation supported this specific change. v35 reproduces that one-sweep result exactly outside the 13 new title-reference assignments. |
| 2. Preserve the missing-parent wording correction | Retained and verified | All 63 missing-parent native messages retain one supported match with their complete diagnostic phrase; both active matching routes agree. v34's established literal-sequence loss guard remains. This is not a default-literal list or a ban on initial adjacent KEY slots. |
| 3. Add the discussed title reference structure | Implemented; inventory validated | `TITLE_FULL_ID` uses the existing shared `full_id` recognizer. Owner JSON declares three source/context boundaries; no title-rank or identifier-value whitelist. Native populated Internal Key format occurs across county, barony, duchy and kingdom references, so COUNTY_FULL_ID would be too narrow. |
| 4. Clarify the earlier review's labels | Complete | “No region regrouping” replaces “Disabled” in the rendered v34 review. Every message was still processed; coverage merging stayed enabled in every experimental arm. Historical results remain unchanged. |
| 5. Repeat native ten/thirty comparison | Complete | Same complete log selections and verified input hashes; fresh inference, no imported templates, no synthetic messages. Compare v34 repeated-loop results and the saved one-sweep experiment separately. |
| 6. Inspect captures and consumer support | Complete | Learner and runtime use the same declarations. Native inventory captures preserve exact byte ranges and do not cross two references. Both candidate bundles and all compact template constraints validate. All 183,570 captures in the thirty-log evidence match original native bytes. Both matchers agree on the 76 affected title/parent rows. Production release still loads. This is not a new complete runtime replay of every source. |
| 7. Reconcile docs and existing handoff | Complete | Production model and parser pins remain unchanged pending candidate review. No parser code changed. |

## Title construction evidence

The complete 73-log inventory contains 337 populated Internal Key title markers.
252 occur inside an existing opaque REASON; those remain there. The other 85
are recognized as TITLE_FULL_ID in these explicit contexts:

| Source | Outside wording before / after the field | Occurrences |
|---|---|---:|
| `pdx_assert.cpp` | `Assertion failed: Trying to remove holder of the on-map title '` / `' currently held by '` | 2 |
| `succession_order.cpp` | `Title '` / `' is in the succession that we are currently building for character '` | 74 |
| `jomini_script_system.cpp` | `Error: Trying to check state faith on ` / `, which shouldn't have one`, within Script system error | 9 |

The field includes the variable-length title name and complete balanced
`(Internal ID …)` suffix. Names, rank, internal IDs and Internal Key contents
are opaque. Quotes and surrounding diagnostic wording remain outside.
Character and house recognition remains unchanged: 3,666 and 12 captured
occurrences respectively. Another 4,002 ID markers remain inside already opaque
constructions. Three truncated markers remain outside declared complete fields.
No competing full-ID boundaries were found. These are finite-corpus findings,
not a guarantee about every future CK3 emission.

## Previously discussed work: disposition

The next mechanical work is items 2–5 of LEARNER_OUTSTANDING_WORK.md, with the
coverage-absorption passes evaluated explicitly. Those changes require their own
native comparison; the approved one-sweep experiment does not validate them.

| Work | Decision / next action |
|---|---|
| “In history for” and “Lowborn of” | No additional change needed. The owner clarified that In history for stays diagnostic wording; Lowborn of is already inside the character field. Verify retention in this build. |
| Diagnostic-only comparison; joint PARAM evidence; controlled reopening | Still required, not dropped. Implement together as a separately inspectable mechanical step: accepted fields/location labels provide no positive diagnostic evidence; proposed fields cannot justify one another. Do not claim the one-sweep change solves these. |
| Coverage-only absorption and Event/List wording loss | Investigate the remaining merge decisions against native formulations, then correct diagnostic agreement generally. Do not add Event/List exceptions or restore default literals. |
| Negative-adjective additions | Keep the completed log-derived survey for review. Proposed additions have not been approved as active vocabulary; current loss-check lists remain active only in their scoped role. No global literal behavior. |
| LOCATOR lost through empty/malformed observations | Still open. Correct field evidence/outlier handling; no folder whitelist and no manual generated-template edits. |
| Malformed identifier braces | Current containment remains; general outlier handling still open. Do not turn a brace into KEY or infer PARAM from failed KEY checks. |
| Broad/narrow competitors and one production assignment | Still open. Audit current competing candidates first; ranking must not conceal invalid inference. Then implement evidence-based selection and transparent ties with the pipeline. |
| Location-label equivalence | Exact observed variants already prevent Near-as-OPTIONAL_KEY. General declared equivalence still needs a lossless matching representation; no optional-literal or text-normalization workaround. |
| Matching unification | Shared full-ID recognition is implemented. The remaining learner/runtime matching duplication still needs the separate architectural consolidation already requested. |
| Rich-text character references without Internal ID | Not covered by CHARACTER_FULL_ID. A separate native structural inventory is necessary before declaring recognition; no name dictionary or arbitrary capture of preceding words. |
| Revisable incremental hypotheses | Remains explicitly deferred until the mechanical inference corrections are validated. Evidence accumulates and inference rebuilds within a learner identity today; templates are not imported across versions. |
| Production publication | Candidate review comes first. Keep selected v29 model and raw parser v1.6 pins. A learner-only change is not grounds for a parser version bump. |

Native artifacts: `.codex-tmp/learner-refactor/single-sweep-v35/`.

## Demonstrated complete-log results

| Corpus | v34 templates / supported / provisional | v35 templates / supported / provisional | v34 full / provisional occurrences | v35 full / provisional occurrences |
|---|---|---|---|---|
| Same ten logs, 352,317 messages | 311 / 168 / 143 | 311 / 168 / 143 | 290,864 / 61,453 | 290,864 / 61,453 |
| Same thirty logs, 1,143,064 messages | 456 / 258 / 198 | 457 / 257 / 200 | 697,337 / 445,727 | 697,335 / 445,729 |

Both have zero unknown outcomes; that is coverage, not proof of correct inference.
Ten-log candidate: `fbb8d94f894456ebe470c695` (62.25 seconds).
Thirty-log candidate: `753006dab4348ab5c6601afd` (189.51 seconds).
Fresh builds used original logs and the v35 implementation identity; neither
loaded earlier templates. Timings are elapsed measurements, not a controlled
speed comparison.

Only one assignment changes in the ten-log build: Athlone's complete title
reference replaces its former literal spelling. It remains provisional.

Eighteen assignments change in the thirty-log build:

- Thirteen title references become complete TITLE_FULL_ID captures: the Athlone
  assertion and twelve succession messages. South Kazanskaya's two-word title
  joins the same supported succession template as the eleven previously
  supported one-token title names. It changes provisional to full.
- Five rich-text character messages reproduce the earlier one-sweep arm. Three
  revert from full to provisional; two remain full but retain literal `target`
  instead of KEY in the diagnostic clause. Fragmented rich-text names remain a
  limitation. Their lack of Internal ID means the declared full-ID construction
  does not apply; no example-specific name rule was introduced.

The three full-to-provisional changes and the one provisional-to-full change
are all in the added twenty logs. There are no outcome changes on the original
10-log cohort evaluated with the thirty-log models. On that cohort both models
have 291,558 full and 60,759 provisional outcomes. Assignment changes and outcome
changes are distinct; the original Athlone capture changes without promotion.

Compared directly with the saved v34 one-sweep experiment, every assignment and
capture outside the thirteen title rows is identical, across all 38,621 contextual
rows / 1,143,064 occurrences. This verifies the production implementation of the
approved loop change independently of the title extension.

The 73-log inventory retains all 2,595 distinct character/house captures with
identical raw-piece boundaries, byte ranges, text and occurrence weights. All 85
title captures agree between learner and runtime recognition. The thirty-log
candidate contains thirteen of those title occurrences; the other contexts are
recognition evidence, not invented training examples.

Readable native before/after examples and all three title contexts:
`.codex-tmp/learner-refactor/single-sweep-v35/REVIEW.html`.
Machine evidence: `comparison.json`, `changes.json`, `native-validation.json`,
`implementation-audit.json`, `single-sweep-changes.json`, and both build bundles.
No generated model templates were manually edited. No model has been promoted.

## Follow-up: exact origin of the scope:recipient competitor

Read-only native trace established a concrete earlier grouping defect. Initial
comparison sees `scope:recipient trigger` as three words and ordinary trigger
identifiers as two. Candidate retrieval uses word pairs for the former and
individual-word keys for the latter, so there is no shared lookup key despite
shared diagnostic `trigger`. Direct seed similarity is 0.425 versus 0.72. The
remaining region sweep repeats the shared-anchor prerequisite. Meanwhile KEY
matching accepts the complete colon-qualified expression, so both general and
narrow templates match. No parser defect is implicated.

The narrow candidate has only three distinct native texts with identical failure
wording/reason. Its support calculation excludes LOCATOR values but still counts
the second trace PARAM spelling, so it is marked supported (two nonlocation
forms). The **classification**, not this template, becomes provisional because
both candidates match. See the actual native member locations, template IDs,
and mechanical trace in
`.codex-tmp/learner-refactor/no-coverage-v36/OVERLAP_MECHANICS.md`.
No source or model change was made during this explanatory investigation.
