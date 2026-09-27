## 2026-09-24: correct trace PARAM boundaries (v27)

- [x] Remove the incorrect whole Script location chain PARAM declaration. The existing general file/line + balanced script-chain declaration keeps paths/lines outside PARAMs.
- [x] Withdraw the proposed nested location extraction approach; no extraction artifact, nested fields, schema change or caller change is part of this correction.
- [x] Audit native trace formats across the 73-log census: 15563 distinct changed messages / 1165336 occurrences, 3614702 formerly hidden location ranges. Zero recognized location/trace-PARAM overlaps. Native witnesses cover zero through 55 parenthetical traces; only actual log messages were used.
- [x] Rebuild on the same ten complete native logs: candidate 762e1b8d5772b08ca08f1440. 296 patterns (164 supported / 132 provisional), 290888 full / 61429 provisional / zero unknown or ambiguous. 553 occurrences across 36 templates become provisional because their variation is now correctly recognized as location-only under the unchanged support policy. 38336 inferred member ranges agree with captures; no export discrepancies in 37456 capture checks.
- [x] Independent pipeline replay of all ten complete logs: 352317 outcomes and all captures agree, including 821250 LOCATOR captures; exact original-byte reconstruction. Owner's native example from an additional log is a full match with four LOCATORs and two trace PARAMs. Publish/select a9fa27a85ccd066285b99fdb; retain parser v1.6 and schema 3. Update the existing formal handoff. No caller change or production ingestion.

## 2026-09-24: declared reason boundary correction (v26)

- [x] Reproduce the native empty-reason failure; establish that raw parser v1.6 correctly preserves the original gap.
- [x] Declare REASON allow_empty in owner_rules.json; capture complete whitespace runs outside the reason, including newlines. No example-specific rule or changed raw parser.
- [x] Emit zero-length declared fields once during inference, then continue at the same raw boundary. Keep empty capture value and zero-length span distinct from absent OPTIONAL_KEY.
- [x] Audit declared field boundaries across the 73-log native census: 15558 distinct declared messages / 1174352 occurrences, five changed messages, zero remaining boundary errors. Verify changed witnesses against original file hashes/bytes and literal-plus-capture reconstruction.
- [x] Complete unchanged ten-log comparison: all 229 template records, captures and outcomes are identical.
- [x] Finish the previously blocked twenty-log comparison: candidate 9b7b9c106a99cc32129e6e53, 196 supported / 126 provisional. Twenty previously provisional families now fully supported; original-ten outcomes improve for 299 occurrences, none regress in status. Capture assignments change on 199 contextual rows / 926 original occurrences and still require semantic review. Candidate remains unpublished. See empty-reason-review/twenty-log-comparison.json.
- [x] Publish/pin 1d1d6e0389f7235f565b2504 with the same parser artifact; previous release unchanged. Wheel artifact bytes and explicit selection verified.
- [x] Add Task 4 supplement to the existing formal pipeline handoff, including empty capture semantics, hashes and outcomes. Current pipeline reader/matcher returns ordinary unknown for all five affected native cases without exceptions.

## 2026-09-23: publication completed

- [x] Record settled expression-PARAM and malformed-reference KEY policy in the owner JSON; reject the proposed colon-count/game-validity gate.
- [x] Replace the obsolete short-expression KEY assertion with native field-member, raw-boundary and capture verification. No synthetic messages or inference exceptions.
- [x] Build v25 from the same ten complete logs; compare every contextual row against v24. Zero template/capture/outcome changes.
- [x] Validate compact export against all 7864 native contextual results and 20832 captures; retain provisional statuses.
- [x] Replay the packaged parser on all ten complete native logs, verifying exact reconstruction and individual-message recovery.
- [x] Publish immutable b1965fa4408ca1bcf36763c9 with parser/rules/hashes; pin models/selection.json and package the release files.
- [x] Update the existing formal pipeline handoff in place, replying to the original dependency request. Shared repository is the owner-selected delivery channel.

133 supported + 96 provisional hypotheses; 291441 full + 60876 provisional
occurrences. No individually confirmed templates, unknown or ambiguous outcomes
in these ten training logs. Wider semantic quality and pipeline integration
remain explicit limits in LEARNER_PARSER_PIPELINE_HANDOFF.md.

The quoted-expression question below is now settled by the owner: its supported
variable span remains PARAM, including one-token values. The dated v24 failure
is retained as history, not an open restriction or an authority to alter inference.

## 2026-09-23: raw-span evidence and provisional support correction

- [x] Remove whitespace, nested-content and alternating-separator requirements from PARAM evidence; these were assistant heuristics, not owner requirements.
- [x] Use raw token counts (punctuation included, whitespace gaps excluded), distinct member values and separately validated boundaries. Equal observed lengths do not veto PARAM.
- [x] Keep singleton and location-only repetition provisional; block full classification and confirmation from those candidates.
- [x] Rerun the same ten complete native logs; inspect mesh and character/ID regions and all four changed formulation transitions.
- [x] Run native requirements, document regressions, update consumer contract and handoff.
- [x] Owner resolved quoted-expression typing: a supported variable expression field remains PARAM, including one-token members. Native verification now checks field evidence and exact boundaries; no expression-specific inference rule was added.

Candidate **9b49f15041153abb1fc6789b**, algorithm v24, unchanged parser v1.6.
Same ten logs / 352,317 occurrences: **133 supported + 96 provisional** candidates;
291,441 full, 60,876 provisional, zero unknown/ambiguous. Provisional-only outcomes
are insufficient-support evidence, not lost messages. Exact repeats and changes
only to LOCATOR values do not increase independent learning support. Registry
confirmation and confirmed seeding both enforce this gate.

32/33 native checks pass; test_native_dotted_statement_reference_is_key fails
because one multi-token function expression joins six simple/qualified references
under Failed converting statement for '<PARAM>'. Six formerly KEY forms / 39
occurrences change type; the broader seven-value family has 51 occurrences.
No assertion was weakened to accept this result. That generalization remains a
review issue; no new negative/example-specific rule was added to suppress it.

Mesh/character captures are unchanged from v23, with evidence now derived from
actual raw spans instead of the removed restrictions. Mesh counts 1/5/7; Parent
outer-region counts 4/12/13, ID interiors all eight tokens. Four rich-text messages
also consolidate, with wider name PARAMs; retained formatting boundaries need
review. A development regression merging Unexpected/Malformed was corrected by
excluding qualified KEY raw-piece multiplicity from positive PARAM evidence.

11 contextual rows / 55 occurrences change captures, four distinct formulation
transitions. 7,864 reconstructed alternatives, 20,832 captures, 21,712 member spans,
zero discrepancies. Reconstruction is bookkeeping evidence, not semantic approval.
45.06 seconds. Review at ignored
.codex-tmp/learner-refactor/empirical-regions/param-evidence-delivery/FINDINGS.md
and REVIEW.html; source/ contains the matching implementation snapshot. No runtime
or SQL changes, no promotion. Current model contract and pipeline handoff updated.

Historical checkpoints follow; their prior heuristics/counts are superseded.

# Outer diagnostic learner implementation status

## Qualified KEY, sequence-region and character-description corrections — 2026-09-23

- [x] Confirm native evidence: twelve distinct mesh messages / 120 occurrences;
  their interiors include three LOD spellings, a longer tree chain and plain
  identifiers. Existing region discovery finds the brackets but rejects the
  non-space-separated chains. No additional logs needed to demonstrate variation.
- [x] Implement registry-declared colon-qualified KEY spans with matching over
  the original separate parser pieces; no prefix whitelist or raw-parser change.
- [x] Extend positive balanced-region evidence to variable-length alternating
  token/separator sequences. Keep whole KEY-compatible interiors typed as KEY;
  no mesh-name, pipe-specific or bracket-implies-PARAM shortcut.
- [x] Add owner-approved characterhistory.cpp Character: description declaration
  through balanced ID parentheses, including no-character form. Prefix and
  subsequent error wording stay literal; no name or ID values are hard coded.
- [x] Run the same ten logs, native checks and before/after capture comparison.
- [x] Review regressions; publish results and update parser/learner handoff.

Focused complete-source replay passes: qualified Unexpected token and promote
references join KEY formulations; nonempty shader mesh group uses [<PARAM>],
while the two blank-shader messages have only single-token mesh evidence and
retain [<KEY>]. Character declaration recognizes Basilia's whole description.
Algorithm v23. No promotion or runtime/SQL changes.

Candidate f9d422a0a044d4670b9c54fd under ignored qualified-fields-development-01:
same ten logs, 352,317 full / 0 ambiguous / 0 unknown, versus 352,316 / 1 / 0.
Templates 265 -> 231. All 30 native checks pass. 128 contextual rows / 19,392
occurrences change captures; 40 distinct formulation transitions were inspected.
19,251 script-system occurrences now use qualified KEYs in the generic trigger
template, rather than literal scope/title references. 100 mesh occurrences use
the supported bracket PARAM; the 20 blank-shader occurrences retain single-token
mesh KEYs. Basilia's description is one declared PARAM; all 205 parent-history
outer PARAMs are unchanged. The spouse ambiguity resolves.

Remaining limitation: the now-separate concubine error retains its second person
description literally (one occurrence); the first description is PARAM and the
actual failure wording is preserved. The new declaration intentionally covers
Character: descriptions, not arbitrary names or In history for tails. Existing
three-KEY parent explanations and title-report fragmentation remain; the brace
singleton qualification issue from the previous investigation is unchanged.

7,864 complete matches reconstruct exactly; 20,824 captures and 21,704 member
ranges verify without discrepancy. Source/input hashes and unchanged parser
verified. Build 40.754 seconds (single observation). Readable comparison, all
changed formulations, raw source snapshot and test output: qualified-fields-delivery
in the same ignored evidence root. Full matches remain research replay outcomes,
not semantic approval. The delivery explains the new KEY constraint to consumers.

## Positive ordinary PARAM typing — 2026-09-23 (implemented and verified)

- [x] Remove PARAM as the residual type when other slot checks fail. Ordinary
  PARAM needs observed phrase variation plus the existing boundary validation;
  declared fields and accepted empirical regions keep their explicit evidence.
- [x] Reject unsupported unions; partition initial native groups by actual raw
  syntax and re-infer, retaining literal variants if syntax does not distinguish
  them. No prefix whitelist, default literals, punctuation exception or new type.
- [x] Focused native-source replay: normal key references remain KEYs, } stays
  literal in its own formulation, qualified-reference prefixes emerge as literal
  structure, and Unexpected/Malformed token formulations separate in this evidence.
- [x] Run the same ten logs, native requirements and saved-result comparison.
- [x] Inspect all formulation changes/regressions, preserve source/input hashes,
  update handoff and deliver a readable review. Parser and runtime unchanged.

Candidate 231197737b82bcf8386a3ac2, algorithm v22, under ignored
.codex-tmp/learner-refactor/empirical-regions/typed-fields-development-01/candidate/.
Same ten complete logs / 352,317 occurrences: 352,316 full, one ambiguous,
zero unknown, unchanged from v21. Templates 244 -> 265; none confirmed.
794 contextual rows / 8,984 occurrences change formulation and captures,
covering 33 distinct before/after formulations across eight source families.

8,343 key-reference occurrences now use OPTIONAL_KEY (the native pool includes
empty references); the two } outliers retain literal braces separately. Ordinary
Unexpected token and Malformed token values become KEYs in 251 occurrences;
their diagnostic words remain literal. Plain/dotted references and scope-prefixed
references re-infer separately with local literal prefixes. No prefix, word or
example-specific exception was added. All 205 outer parent PARAMs are unchanged.

Remaining generalization regressions are explicit: 14 activity-event descriptions
split names into two KEYs, two spouse-history descriptions become literal apart
from locations, and one marriage-age description becomes literal apart from the
declared trace/locations. Four rich-text messages fragment; 40 mesh occurrences
retain pipe-separated identifiers as literals. These are not semantic successes
merely because they still match. A single complex GetTitleByKey spelling (12
occurrences) also remains literal; repetition does not establish field variation.
Earlier title-report fragmentation, 165 three-KEY parent explanations, and the
one spouse-history ambiguity remain. No NAME type or new declarations added.

All 27 native requirements pass. All 7,865 complete matching alternatives
reconstruct exactly; 20,756 captures and 21,646 candidate-member ranges verify.
No inferred-versus-matched field discrepancy. Source/input hashes verified;
parser v1.6, declared fields and disabled presumed literals remain unchanged.
Build 230.500s versus 144.925s before (single observations, not a benchmark).
Readable review, all 33 transitions, source snapshot and verification are under
typed-fields-delivery/ in the same ignored evidence directory. No promotion.

## Region-first balanced PARAM experiment — 2026-09-23 (implemented and verified)

- [x] Propose outer balanced regions before initial wording comparison and
  interior alignment. Locations and declared fields retain priority. Symmetric
  quotes keep their existing handling; this step addresses nested asymmetric
  punctuation envelopes without source/phrase-specific rules.
- [x] Historical assistant heuristic (removed in v24, never an owner requirement): validate variation plus phrase/nested content within candidate members;
  preserve a supported outer region as opaque PARAM despite repeated interior
  words. Fixed interiors remain literal; mere parentheses do not force PARAM.
- [x] Keep raw parser, presumed-literal disablement and declared trace/reason
  behavior unchanged; record generic engineering mechanics in owner_rules.json.
- [x] Verify the native parent/ID examples and run the same ten complete logs.
- [x] Check complete captures, nesting, regressions and changed formulations;
  deliver a readable comparison. General word-boundary discovery and the
  previously diagnosed ordinary slot-type fallback remain explicit separate gaps.

Candidate 22b23eefbc90b3e8b6e69b11 (algorithm v21), under ignored
.codex-tmp/learner-refactor/empirical-regions/region-first-development-01/candidate/.
Same ten complete logs / 352,317 occurrences: 352,316 full / one ambiguous /
zero unknown, versus 352,294 / 23 / zero. All 22 resolved ambiguities are the
parent-history overlap; the Jiong_7085 spouse overlap remains. Templates 240 ->
244, all eligible, none confirmed. Captures change for 521 contextual rows /
625 occurrences. All 205 parent-history occurrences capture the outer description
as one PARAM; the native (no character) variant keeps its inner parentheses.
The model has 25 empirical balanced-region fields across 11 source families,
used in 618 occurrences. No NAME type or character-specific declaration added.

Semantic regression: eleven history.cpp title-report occurrences fragment into
narrower candidates; three become entirely literal and four title values become
three KEYs. These retain full-match status, which does not establish correctness.
The 165 parent explanations after is still have three KEYs; they have no enclosing
balanced punctuation and this experiment does not fix word-bounded inference.
Previously diagnosed ordinary KEY/PARAM fallback and leading diagnostic-word
generalizations remain unchanged. No claim of general PARAM discovery is made.

All 22 native checks pass (16.255s with comparison running concurrently).
7,865 complete matching alternatives reconstruct exactly; 20,855 captures and
21,732 candidate-local field ranges verify without discrepancy. Source hashes,
input hashes, parser v1.6 and declared trace/reason behavior verified unchanged
where required. Build 144.925s versus preceding 95.916s, single observations.
Review: region-first-delivery/REVIEW.html in the same ignored evidence directory;
24 side-by-side examples plus highlighted title regressions, source snapshot,
verification.json and test output. No promotion, runtime/SQL change or 73-log run.

## Required sequencing correction — 2026-09-23 (investigation preceding v21)

Owner challenged the renewed region-first proposal because this was already an
instruction. Current code confirms that the general requirement is NOT fulfilled:
cluster_source_records first groups by learning_tokens; derive_pattern performs
SequenceMatcher alignment and assigns slots before calling envelope_review.
That function appends diagnostic hypotheses; it does not select outer regions
or alter the inferred parts. Only known constructions, declared traces and
LOCATORs are atomic before alignment. Existing anchor/balance/coalescing and
regrouping mechanics are real but do not constitute general region-first PARAM
discovery. Earlier completion language must not be read as satisfying that
requirement.

Repeated Internal ID / Historical ID wording is visible to the algorithm. It is
retained as internal literal anchors, and envelope_review consequently marks
the surrounding region divided. This is an implemented preference/order issue,
not evidence that empirical recognition of repeated structure is impossible.
PARAM remains the fallback after simpler type checks fail, a separate defect.

Withdraw the suggestion that scope:<KEY> is generically valid across messages.
It was an observed local formulation, not an approved global prefix rule. No
new default literal or scope-prefix declaration has been added. General inferred
regions here mean candidate PARAM spans, to validate before interior alignment;
the added generic field-typing abstraction obscured that requirement.

Recommended next decision: a focused demonstration of actual generic region-first
discovery on native character descriptions and other boundary forms, before new
NAME machinery or more structural declarations. A locator-plus-exact-raw-message
product path is independently viable for evidence retention/navigation, but
location extraction and mod ownership need their own validation; extracted paths
alone do not establish a mod conflict. This investigation does not authorize or
implement a pipeline/SQL redesign.

## Slot typing investigation — 2026-09-23 (findings; not implemented)

Follow-up cases 13/15/17 from the same outer-delivery report, verified against
latest v20; evidence saved under no-guidance-delivery/owner-cases-13-15-17.json:

- Case 13: war_goal_title.GetName is one raw token, but shares its candidate
  with scope-qualified references and a nested GetTitleByKey expression. All
  seven observed values are whitespace-free; raw-piece count causes PARAM via
  the same residual-type fallback. The earlier reviewed candidate contained
  the scope-qualified values but kept the nested expression separate; v20
  combines them. Preserving the outer quotes improved boundaries without fixing
  the semantic field type.
- Case 15: the old trailing PARAM was optional and absent in this native row.
  Its compact display hid optionality. The outer-diagnostic run rejected that
  combined optional-tail proposal as insufficient field evidence, then retained
  the absent subgroup as a template without a tail. A separate template handles
  parenthetical-present messages. Latest trace-presence grouping retains that
  distinction. This is structural separation, not deletion of captured content.
- Case 17: 59 native rows / 254 occurrences combine Unexpected (222) and
  Malformed (32) into a leading KEY. Similarity/union plus differing single-token
  values supplies the inference; no positive evidence establishes an identifier
  field at the leading diagnostic word. The reported-token field has 51 distinct
  values, none containing whitespace. Two occurrences report { and one reports
  title:h_china.holder; these fail the one-nonpunctuation-token KEY criterion and
  trigger PARAM for the whole candidate. Boundary acceptance does not establish
  phrase-valued content. This is both excessive formulation merging and the
  residual PARAM typing defect, already present before guidance was disabled.

No code or rule change during inspection. Positive region/type identification
must distinguish candidate-boundary evidence from type evidence. Neither
restoring a word list nor banning these individual observed values is the fix.

Owner reviewed cases 05/06/12 from outer-delivery and proposed NAME recognition.
These case numbers differ from the later ten-example boundary report. Exact
latest native evidence is saved in ignored
.codex-tmp/learner-refactor/empirical-regions/no-guidance-delivery/owner-cases-05-06-12.json.
No inference, lexer, slot-schema or registry changes during this investigation.

- Case 05, Failed to read key reference: latest candidate covers 8,345 occurrences.
  Of these, 8,343 contain ordinary identifier values; two contain the literal
  punctuation token } in both fields. All values are one raw token; none is a
  multi-word phrase. The all-member single-nonpunctuation-token KEY test fails on
  }, and the else branch assigns PARAM to both entire fields. Colon boundaries
  then satisfy PARAM's boundary check. There is no special colon-to-colon rule.
- Case 12, Could not find promote: four native messages / 24 occurrences.
  Values holder and war_goal_title are single raw tokens; two scope-qualified
  references each occupy token/colon/token pieces with no whitespace. The same
  fallback converts both fields to PARAM. Raw token count is being used as a
  proxy for semantic field type. Lexer separation is correct; the learner needs
  positive reference/field recognition rather than PARAM as the residual type.
- Case 06, Agrippina: latest model now matches, but subdivides the parent
  description into an optional name-like PARAM and an inner-ID PARAM. The name
  after the outer parenthesis is another PARAM; the explanation is three KEYs.
  Recognition of the approved outer character-description structure should
  precede alignment of its recurring ID labels. A NAME would describe a name
  subspan, not the complete parenthetical description including IDs or the
  native (no character) alternative.
- NAME research: local game files contain culture name lists, dynasty name
  references/prefixes and localized displayed names. Verified Hovhannes/Alvise
  mappings and lowercase dynasty prefix de. Capitalization is evidence, not a
  complete boundary/type test. Recommend a source-derived phrase index over raw
  token ranges, with name-list/localization/mod provenance plus message context.
  Unknown spellings must remain possible; uncalibrated evidence scores must not
  be presented as probabilities. Do not turn this into another literal word list.
  Dictionary phrase matching is an established method (spaCy PhraseMatcher:
  https://spacy.io/api/phrasematcher); adoption of spaCy or new tokenization is
  not required or proposed as part of this investigation.

Next implementation must positively identify regions and field kinds, not add
negative exceptions for reviewed examples or restore presumed literals. The
owner-authorized character envelope can be declared transparently in JSON;
ordinary KEY/reference versus PARAM typing still requires a general correction.

## Presumed-literal guidance disabled — 2026-09-22 (implemented and verified)

Owner directed disabling presumed literals and rerunning after PARAM boundary
and trace corrections. No substitute word lists or example-specific exceptions.

- [x] Set `default_literals.enabled=false` in owner_rules.json with owner authority.
  Effective guidance is empty in grouping, literal anchors, inference and every
  newly built slot constraint. The old spellings remain inactive reference data.
- [x] Increment the algorithm revision to v20; old enabled-guidance candidates
  cannot be silently reused by the current loader.
- [x] Build from the same ten complete logs, with unchanged parser, trace
  declarations, location recognition, similarity threshold and PARAM policy.
- [x] Verify disabled guidance and native captures; inspect culture/faith/holder
  trigger generalization and possible overbroad wording; publish comparison.

Candidate `9070fd331e7cb810fa98b58c` (v20) under ignored
`.codex-tmp/learner-refactor/empirical-regions/no-guidance-development-01/candidate/`:
same ten logs / 352,317 occurrences, **352,294 full / 23 ambiguous / zero unknown**,
unchanged from v19. Templates decrease **257 -> 240**, all eligible, none confirmed.
861 contextual rows / 154,528 occurrences have changed formulations/captures.
All 146,941 culture-trigger occurrences and 493 faith-trigger occurrences now use
`Error: <KEY> trigger [ <REASON> ]`; the 2,018 holder-trigger occurrences still do.
Quoted event targets and inconsistent-trigger scope names also generalize.

Removing the word list exposes overgeneralization elsewhere: 165 parent-history
occurrences (117 `hasn't been born`, 48 `the wrong gender`) now have three KEY
fields instead of the reason wording. Each field contains only the corresponding
word pair: `hasn't/the`, `been/wrong`, `born/gender`. These move together as phrases;
the current learner nevertheless treats the positions independently. Separately,
217 localization-error occurrences merge optional `Near` into OPTIONAL_KEY, whose
only nonempty observed value is `Near`. These are formulation regressions despite
unchanged full-match counts. The same 23 character-history ambiguities remain.
No guidance list or example-specific exception has been restored. Next review
should address empirical correlated wording and evidence for optional KEY fields.

Nineteen native checks pass; 7,887 complete alternatives reconstruct exactly,
21,707 captures and 22,462 candidate-local field spans verify without discrepancy.
Parser v1.6, input hashes, trace/location recognition and PARAM policies are
unchanged; the only changed rule section is `default_literals`. Build 95.916s
(preceding run 62.172s); this is one timing observation, not a benchmark claim.
The readable comparison has 23 examples and preserved source/verification data:
`.codex-tmp/learner-refactor/empirical-regions/no-guidance-delivery/REVIEW.html`.
Nothing promoted; the deferred 73-log exercise remains unrun.

## Declared trace PARAM follow-up — 2026-09-22 (implemented and verified)

Owner approved recognizing supported trace structures as ordinary PARAM every
time, without a TRACE slot or special matching role. Other PARAMs remain empirical.

- [x] Survey complete native records and identify supported boundaries. Two JSON
  declarations: a complete Script location file/line chain, and the balanced
  parenthetical interior immediately following a file/line introducer.
- [x] Expose these spans as atomic PARAM inference units; exclude their interiors
  from wording comparison and ordinary alignment. Leave original pieces intact.
- [x] Use ordinary PARAM matching; per-slot declaration IDs are inference provenance,
  excluded from slot matching identity/constraints. Preserve declarations and source hashes.
- [x] Keep declared-field presence as grouping structure, without grouping by trace
  words or frame count. Never classify arbitrary trailing text as a trace.
- [x] Enforce that same structural presence/order before complete-message matching.
  The initial v18 run showed 19 Unknown-location occurrences accepted by an ordinary
  PARAM in a trace-present candidate. v19 adds the missing outer-message selection
  check; the PARAM matcher itself has no trace-specific path.
- [x] Diagnose culture-trigger specificity. `culture` is presumed literal and
  participates in the hard grouping signature and slot veto. It occurs in 409
  distinct native rows / 146,941 occurrences. No vocabulary alteration is included
  in the trace experiment; source-specific KEY generalization needs a separate
  correction to contextual literal guidance, not a culture-specific exception.
- [x] Same-ten-log build, native boundary/matching checks, comparison and handoff.

Initial native recognition audit: 221,299 Script location chains; 2,214 located
parenthetical captures across the remaining supported messages (20 sources total).
One distinct Script location: Unknown formulation, occurring 19 times, is explicitly
not treated as a trace. ID parentheses and unrelated explanatory parentheses are
not matched by either declaration. Recognition evidence is in ignored
`.codex-tmp/learner-refactor/empirical-regions/trace-recognition.json`.

Final candidate `7416a879fac4bf86ef1df0b5`, algorithm v19, is at ignored
`.codex-tmp/learner-refactor/empirical-regions/trace-development-02/candidate/`.
Same 10 full logs / 352,317 occurrences: **352,294 full, 23 ambiguous, 0 unknown**;
257 templates, all eligible, none confirmed. The preceding run had 352,051 full,
266 ambiguous, zero unknown and 275 templates. 244 ambiguities become full;
22 remain ambiguous; one formerly full character-history occurrence becomes
ambiguous. All remaining ambiguity is in characterhistory.cpp. The new overlap
is the native Jiong_7085 marriage-after-death message and a broader competing
`<KEY> Character ... cannot <PARAM>` candidate. Existing broad ID PARAMs and
literal/KEY errors in that family remain review work, not fixed by trace handling.

Build time 62.172 seconds versus 780.817 seconds. Eighteen native checks passed
in 8.088 seconds. The report verifies 7,887 complete matching alternatives,
20,452 captures and 21,257 candidate-member field ranges, with no span/reconstruction
discrepancies. Recognized trace ranges match actual PARAM captures exactly.
Declared single-observation traces are PARAM; ordinary parentheses do not force
PARAM. The Unknown-location formulation remains a unique non-trace match.

Owner review: ignored `.codex-tmp/learner-refactor/empirical-regions/trace-delivery/REVIEW.html`
has 31 distinct formulation comparisons, beginning with culture-trigger and the
script-value trace. Source snapshot, recognition evidence, verification metadata
and the culture-trigger diagnosis accompany it. The raw parser remains v1.6;
there is no TRACE slot, trace-specific PARAM matcher, promotion or runtime change.

Culture-trigger finding: both `culture trigger` and `holder trigger` pass the
two-token similarity gate. Their default-literal grouping signatures differ:
`culture, trigger` versus `trigger`. A proposed KEY also rejects guided `culture`.
The learner already produces `<KEY> trigger` for unguided names, so message length
is not the blocker. Default vocabulary is byte-for-byte unchanged in the new
model's JSON values. Recommended next correction: presumed literals may yield
to candidate-local evidence of an identifier position while surrounding `trigger`
remains literal; do not remove culture globally or add a culture-specific exception.
This guidance correction was diagnosed, not bundled into the trace experiment.

## Punctuation boundary follow-up — 2026-09-22 (implemented and compared)

Owner authorized general mechanics and a fresh same-ten-log run; no rules for
the discussed example words, people, sources or templates.

- [x] Record punctuation preference and complete capture search in owner_rules.json.
- [x] Preserve an aligned outer separator when its rank from either end is stable,
  even if the field contains more copies of that punctuation.
- [x] Re-infer adjacent variable text fields across a weak one-word connector when
  a punctuation boundary is available. Preserve longer wording and typed fields.
  The one-word limit is an explicit engineering heuristic, not CK3 grammar.
- [x] Flag punctuation-free PARAMs; require four distinct nonempty values and two
  nonzero token lengths before accepting their weaker boundaries. These are
  reviewable engineering thresholds, not claims of owner-specified numbers.
- [x] Count all complete capture assignments through memoization. Require exactly
  one for ordinary matching; retain two ambiguity witnesses with the exact count.
- [x] Re-infer successful/failed member subsets when a candidate partially fails;
  keep all native evidence, and leave wholly ambiguous groups unresolved.
- [x] Validate requirements on native records and run the same ten complete logs.
- [x] Review changes beyond the motivating cases; publish readable before/after,
  counts, regressions, limitations, source hashes and updated handoff.

Focused development check: the seven actual statement-conversion variants now
jointly retain their outer quotes. All nine spouse and 96 title-holder members
have unique captures after removing the unsupported interior word boundary.
The initial focused 56-member parent-history candidate remained ambiguous.
The complete run re-formed these groups; some resulting ID fields are broader
PARAMs and still require semantic review. Coverage is not proof of correct granularity.
No raw-parser change, model promotion, or production processing is authorized.

### Completed run and owner review

Candidate `b8706927a26d53a7c50efbfd`, algorithm `outer-diagnostic-consensus-v17`,
is under ignored `.codex-tmp/learner-refactor/empirical-regions/punctuation-development-01/candidate/`.
The same ten complete native logs and unchanged parser v1.6 produced 352,317
occurrences / 7,827 distinct messages / 7,864 contextual rows from 93 sources.
Build time: 780.817 seconds, versus 428.391 seconds for the preceding run.
Counting all capture alternatives and the changed grouping cost more; no speed
improvement is claimed.

| Measure | Previous | New |
|---|---:|---:|
| Unique complete matches | 351,833 | 352,051 |
| Ambiguous occurrences | 323 | 266 |
| Unknown occurrences | 161 | 0 |
| Candidate templates | 292 | 275 |
| Unresolved candidates | 3 | 1 |
| Candidates supported by one distinct message | 113 | 104 |

312 formerly ambiguous and 161 formerly unknown occurrences become full matches.
255 former full matches become ambiguous (234 script-system, 21 character-history).
11 remain ambiguous. Two of the 266 ambiguous occurrences have competing capture
assignments; the other 264 have competing templates. This is a net coverage gain,
not a declaration that all new formulations are better.

The 35-example report is at ignored
`.codex-tmp/learner-refactor/empirical-regions/punctuation-delivery/REVIEW.html`.
Its first three entries preserve previous review cases 04, 08 and 10. It includes
before/after templates and captures, remaining conflicts and three PARAM fields
without adjacent punctuation. Machine evidence and an exact source snapshot are
beside it. No example word, person, source or template was added to production
inference rules. In this corpus the generic weak-word operation absorbed nine
interior boundaries whose spelling happened to be `of`; the implementation does
not test for that spelling.

All 16 native requirement checks pass (43.762 seconds). Exact reconstruction
verified 8,095 matching alternatives / 24,234 captures, plus 24,144 candidate-local
member field ranges, with zero inferred/captured span discrepancies. Full input,
parser, bundle and implementation hashes are checked. Test selectors were corrected
to distinguish the actual statement-conversion formulation from another native
message containing the same expression, and to verify zero PARAM weight across
current native groups rather than requiring one historical group membership.

Remaining review concerns:

- Trace templates still overlap: the largest group is 124 occurrences matching
  both a whole-trace PARAM and a detailed file/line formulation; another 65 match
  different trace lengths. Some PARAMs still span several parenthesized trace rows.
- ID labels/content inside some character-history parentheses became a broader
  PARAM during joint inference. Case 08 fixes the name split but exposes this
  loss of field detail. Punctuation preference must not be mistaken for evidence
  that every interior should be opaque.
- Three accepted word-only PARAM fields meet the stronger variation thresholds
  but are explicitly flagged as suspect for review.
- One 52-member Undefined-event-target candidate remains unresolved because its
  capture assignments are ambiguous; other eligible candidates cover those rows.

No candidate is confirmed or promoted. Do not start the deferred 73-log exercise.

Owner authorized all eight recommendations on 2026-09-22, with common
constructions declared in the owner-approved JSON rather than sentence-specific
branches. This checklist is the active execution record.

The established script-system envelope will be supplied explicitly. Its bracketed
reason is an intact REASON field; the remaining diagnostic is learned from native
evidence. The observed unbracketed variant of that same envelope is also
declared, to keep its header and trace from dominating wording comparison.
It prescribes no template or slot type. Generic inference
heuristics are recorded separately from owner-supplied semantic declarations.

| # | Recommendation | Status | Verification / remaining work |
|---|---|---|---|
| 1 | Learn complete outer diagnostics; remove detached tail learning | Complete | Schema 3 has complete candidates and no detached component pools. All 352,317 native messages are accounted for. |
| 2 | JSON-declared construction and intact REASON capture | Complete | Both observed script envelope variants are data in owner_rules.json. Native tests verify intact reasons and matching construction identity. |
| 3 | Length-aware short-message candidate consideration | Complete | One shared position in two-token heads is admitted for investigation. Four complete `<KEY> effect` formulations were learned; the unlearn-language example uses one. |
| 4 | Whole-message structure without boilerplate dominance | Complete | Full-message inference/matching; both declared envelope variants compare failure wording. Native unbracketed comparison excludes the repeated header and trace. |
| 5 | Slot evidence belongs to the candidate's actual members | Complete | 27,761 member field ranges verified; zero discrepancies between accepted member captures and inferred spans. All unions re-infer their full membership. |
| 6 | Stronger evidence for PARAM and retained interior wording | Complete; semantic limits below | Variation/boundary checks, retained adjacent separators and exact member capture replay are enforced. Three initial candidates remain unresolved instead of emitting inconsistent fields. |
| 7 | Presumed literals may become content inside supported fields | Complete; semantic review remains | Native `effect` wording occurs inside a supported trace PARAM. Relaxation is field-local; the report also exposes wide captures spanning several trace lines. |
| 8 | Same-log comparison and readable semantic review | Complete | Same ten logs; 11 native checks passed. 39 distinct formulation comparisons, actual captures and candidate-local PARAM witnesses are available below. |

Baseline: `e0f2d9bfd621adf7176400aa`, ten logs / 352,317 messages. Historical
baseline contains independently learned L1/L2/tails. It is comparison evidence,
not a compatibility target. New candidate contract must explicitly identify the
outer-diagnostic representation; no runtime promotion or SQL changes are in scope.

## Verified result and remaining work

Candidate: `a5f3ace2fd908c6250ac7edd`, parser v1.6 unchanged. Build completed
in 428.391 seconds. The corpus contains 93 source families, 343,585 emissions,
352,317 messages, 7,827 distinct source/message records and 7,864 contextual rows.
There are 292 complete candidates, including three explicitly unresolved ones.

| Outcome | Earlier baseline | Current candidate |
|---|---:|---:|
| Single complete result (earlier full plus L1+L2) | 352,304 | 351,833 |
| Ambiguous occurrences | 13 | 323 |
| Unknown occurrences | 0 | 161 |

This is an architectural correction with verified capture consistency, **not
an overall matching-quality improvement yet**. Twelve earlier ambiguous
occurrences became single matches, but 322 formerly single results became
ambiguous and 161 became unknown. Of the 211,869 earlier L1+L2 results, 211,866
now match one complete outer candidate and three are ambiguous.

Verified: all 11 native requirement checks passed; 26,297 captures and 7,775
complete matching alternatives reconstruct exactly; all 27,761 candidate
member field ranges agree with native bytes; zero accepted member capture
discrepancies; selected-parser and implementation hashes agree. These checks
establish mechanics and provenance, not semantic approval of every template.

Inspect the [readable native comparison](../.codex-tmp/learner-refactor/empirical-regions/outer-delivery/REVIEW.html).
It shows actual messages above before/after templates, expandable actual
captures, and shortest/longest PARAM witnesses from each candidate's own
members. Selection covers distinct formulations, all 12 competing-candidate
sets, and each unresolved candidate; it does not repeat location variants as
if they were different learning outcomes. Full comparison data, a 69-example
visual-review dataset, verification metadata and the matching source snapshot
are beside that HTML under the ignored `outer-delivery/` directory.

Useful review points:

- Example 26: the effect name now varies in `<KEY> effect [ <REASON> ]`.
  The reason stays intact. The applicable complete candidate has 506 distinct
  member messages; its PARAM evidence comes from those members, not detached
  tails belonging to other candidates.
- Example 9: the colon after `Reason` remains literal. Examples 20 and 29
  show trace content containing a presumed literal and the retained `@` key.
- Examples 6, 8 and 10: unknowns expose repeated-word boundary failures in
  names. The three rejected candidates cover 65 character-history occurrences
  and 96 landed-title occurrences. Even when only some members replayed
  incorrectly, the entire affected candidate remains unresolved.
- Ambiguity remains: 286 occurrences in `pdx_persistent_reader.cpp`, 24 in
  `jomini_script_system.cpp`, 12 in `pdx_data_factory.cpp`, and one in
  `characterhistory.cpp`. Broad PARAM candidates overlap more specific
  KEY/literal/trace formulations. All alternatives remain visible.
- Some supported PARAMs extend across several trace lines, including file/line
  labels. Their complete captures are exposed for review. Candidate-local
  evidence and byte consistency alone do not settle whether these boundaries
  are the most useful diagnostic representation.
- `Malformed`/`Unexpected` still generalize to a leading KEY in some reader
  templates. No sentence-specific fix or unapproved vocabulary was added.

Next model-quality work: resolve repeated-word field boundaries without
preferring a convenient match; reconsider overlapping broad/narrow candidates;
review the actual wide trace captures. The bounded 12-neighbor proposal search
can leave valid unions undiscovered. No model was confirmed/promoted, no runtime
or SQL integration was changed, and the deferred 73-log exercise was not run.

## Execution record

- Planning: read the current handoff and owning learner interfaces. Confirmed
  detached pools are built in artifacts/layers, and matching independently
  requires all components. Current short-form gates and PARAM fallback are
  separate correction points. Native parser v1.6 remains unchanged.
- Steps 1–2: replaced separate composition learning/matching with complete outer
  candidates and a generic declarative REASON field. Native A01 reconstruction
  passes with its reason intact and constant trace values literal when inferred
  from that one message. This is a mechanical check, not the corpus evaluation.
- Steps 3–7: implemented candidate admission, candidate-local field provenance,
  ordinary field evidence and field-local literal guidance. No added CK3
  sentence formats. The JSON distinguishes owner-approved semantics from
  tunable engineering heuristics.
- Native development: repaired two interface errors during integration. Stopped
  a slow development build and removed an overbroad attempted opening-word
  safeguard; it fragmented ordinary character names. No special vocabulary was
  added to force Malformed/Unexpected apart. The resumed complete-log pass has
  progressed beyond character history into script-system evidence.
- Performance: cache repeated immutable comparison views and byte offsets;
  bound region-union proposals to 12 nearest later candidates per group per
  iteration. Every proposed candidate still uses all of its native members.
  The JSON records this engineering bound and its non-exhaustive limitation.
- Stopped development 7 after 727.5 seconds: duplicate failed-proposal evidence
  and repeated comparison/identity calculations made regrouping expensive.
  Development 8 caches unchanged marker/nesting/similarity facts and current
  group identities. Failed-proposal records retain complete member IDs and
  decision summaries; accepted candidates retain exact field-support spans.
  Nearest-candidate ranking now uses actual literal raw pieces, avoiding a
  substring test in that ranking. This is not a new literal-recognition rule.
- Development 8 completed its candidate build but exposed a real matching
  defect: ordinary candidates could match messages belonging to the declared
  script construction. Seven native checks passed; the intact-REASON check
  failed. Its 217,608 ambiguous occurrences are a rejected development result,
  not a successful coverage claim. Matching now enforces the same construction
  identity as learning; native verification explicitly covers this distinction.
- Development 9 also revisits candidate containment after region unions, with
  joint inference rather than preferred-match suppression. Rejected union
  proposals no longer recursively rebuild the subgroups they would discard.
  The full ten-log run is underway again. Profiling was removed from its runner.
- Stopped development 9 after the saved native comparison exposed a second
  cause: unbracketed script-system failures were grouped mainly by their shared
  header/location wording, yielding an overbroad `Error: <PARAM>` candidate.
  Under the owner's permission for explicit common structures, the JSON now
  declares this observed variant of the same envelope, with failure wording
  as its comparison region and no prescribed fields. `excludes` explicitly
  keeps bracketed messages with the REASON declaration. No sentence-specific
  templates, trace types or lexical rules were added. Development 10 is the
  complete ten-log verification run for this correction.
- Development 10 completed in 350.625 seconds: 351,934 full / 383 ambiguous /
  zero unknown occurrences. Its audit found nine candidate-member capture-value
  discrepancies in character/name fields despite perfect byte reconstruction.
  The matcher could choose another occurrence of repeated wording such as `of`.
  Candidate acceptance now requires every member's matched spans to agree with
  its inferred field spans; failing unions are rejected, unresolved initial
  candidates remain explicit. The final audit checks exact spans as well as
  values. A generic JSON-recorded adjacency rule also keeps `Reason:`'s colon
  literal when extra colons occur farther inside the variable explanation.
  Development 11 verifies these corrections on the same ten complete logs.

## Completion criteria

Each row must include its actual implementation and native verification before
being marked complete. Do not infer success from matching coverage alone. Keep
competing candidates visible and document unresolved grouping/type concerns.
Generated native evidence and snapshots remain outside Git.
