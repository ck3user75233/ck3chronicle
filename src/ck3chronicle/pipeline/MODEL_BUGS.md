# Learner/model issues — current verification

## Selected release update — 2026-09-24

Selected model is now **0a61f6c93657948e0ca20b35**, learner v29, unchanged
parser v1.6. MODEL-004 is closed in this release. The learner's JSON-declared
contextual location-label recognition generates exact Near file:/file: forms;
OPTIONAL_KEY retains its existing meaning. New templates:
`959e7fc883d82201a278e344` (Near file) and `1edb00c1404c4dd6db2527dc` (file).
The old `1332e889d727946cb5b53eb4` template is absent. All other 295 templates
are unchanged. All ten logs /352317 messages pass separate pipeline replay;
only 25 contextual rows /217 occurrences change assignments, no outcome changes.
Evidence: [.codex-tmp native comparison](../../../.codex-tmp/learner-refactor/location-label-release/REVIEW.md)
and [formal delivery](../../../docs/LEARNER_PARSER_PIPELINE_HANDOFF.md).
The prior audit below remains evidence for the unchanged issues; its explicit
Near recommendations are superseded by this implemented correction.

## Prior full issue audit (v27 baseline)

Verified **2026-09-24** against selected model **a9fa27a85ccd066285b99fdb**,
learner v27, parser ck3-lossless-v1.6 and pipeline classifier v5. Manifest SHA-256:
`072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb`.

**The status table and findings below supersede the historical statuses later
in this file.** Stable issue IDs are retained. This audit changed documentation
only; no model edits, retraining, synthetic inputs, fabricated templates or
runtime workarounds were used.

## Current status by issue

| Issue | Current status | Evidence and remaining scope |
|---|---|---|
| MODEL-001 — namespace identifiers fixed as literals | **Closed on current model** | All 45 distinct native messages in the census match one template with the complete event ID in KEY, including every specifically cited counterexample. See W01–W04. |
| MODEL-002 — compound localization KEY becomes PARAM | **Closed on current model** | All 2048 distinct duplicate-localization messages match KEY + two LOCATORs; dotted/numeric key values stay intact. See W05–W07. |
| MODEL-003 — incompatible/native-incomplete representation | **Core defects closed; one cited coverage case remains open** | Model loads; native suffixes/tails survive; TYPE/ALT absent. Travel, capital_county, near-line and former TYPE examples fully match. The named artifact `holderplace` is still unknown; details below. |
| MODEL-004 — location wording Near inferred as OPTIONAL_KEY | **Closed in v29 selected release** | Learner-generated exact label forms replace 1332e889d727946cb5b53eb4. All 217 affected native occurrences use corrected forms; all other templates and OPTIONAL_KEY behavior unchanged. See selected-release evidence above. |
| P-01 — alleged independent-L2 defect | **Closed / withdrawn; architecture superseded** | No independent L2 lookup remains. Current complete-message templates capture intact REASON. The real stress_impact/proud pair now fully matches (W14). |
| P-02 — old routing and runtime cleanup | **Closed in selected pipeline; old routing superseded** | Outcomes are full/provisional/unknown, with complete-message matches and model-declared captures. No L1-only or independent-L2 result path. Application/SQL activation is a separate milestone. |
| P-03 — compound KEY rejection | **Closed in selected pipeline** | Actual namespace/localization dotted keys bind as one KEY without predicate bypasses or edited templates (W01–W07). |
| P-04 — learner/runtime interpretation drift | **Partly closed; duplication remains open** | Parser and declarations are shared/pinned, and current native replay agrees. Separate learner/runtime matching implementations still exist; this architectural risk is not eliminated. No current drift was reproduced. |
| P-05 — dotted key split before matching | **Closed in selected pipeline** | Complete `capital_county.kingdom` binds to one KEY with the location tail retained (W08). No `_Composer.key_path` in selected path. |
| P-06 — phrase masking changes KEY acceptance | **Closed in selected pipeline** | `enfp_test.0001` and the other dotted identifiers match directly from native pieces; no marker-equality or phrase-mask path (W01–W07, W11). |
| P-07 — rewritten literals / invented optional slots | **Closed in selected pipeline** | Ci Faj case preserves `of`, `Internal ID 296591` and all native text, with two model-declared PARAMs and no inserted OPTIONAL_KEY (W10). |
| P-08 — invalid expression loses namespace prefix | **Closed by removal of the offending selected-path code** | No `_Composer` or prefix-peeling rewrite remains. Actual `scope:overlord_scope.culture` survives intact (W17). The exact historical malformed branch had no native witness and is not claimed as a reproduced regression check. |

“Closed in selected pipeline” refers to `pipeline.catalog.load_selected_classifier`
and its parser/classifier/bindings. It does not certify application activation,
SQLite integration, or removal of all retired implementations elsewhere in the
checkout. This review did not execute those other paths or restore their rules.

## Verification evidence and method

- [Readable native messages, current templates and actual captures — W01–W17](../../../.codex-tmp/learner-refactor/model-bugs-audit/REVIEW.md)
- [Full replay results, parser pieces, original log hashes and byte spans](../../../.codex-tmp/learner-refactor/model-bugs-audit/native-replay.json)
- [Source hashes, current slot vocabulary and prior replay consistency](../../../.codex-tmp/learner-refactor/model-bugs-audit/source-and-model-checks.json)
- [Named-artifact coverage against the ten training-log hashes](../../../.codex-tmp/learner-refactor/model-bugs-audit/named-artifact-coverage.json)
- [Previously completed full ten-log pipeline replay](../../../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/pipeline-replay.json)

The 73-log census supplies the family inventory. This audit freshly parsed
**37 original hash-verified logs** and classified **2314 distinct native
text/source witnesses** through the selected pipeline. Original parser pieces,
complete native messages, recovered wrapper context and every returned capture
were verified against source bytes. One actual occurrence of each distinct
text/source was replayed. Occurrence totals below are census weights, not a claim
that this audit reclassified every occurrence in all 73 logs. Families overlap
(for example stress_impact/proud); do not add their counts as distinct messages.

The prior complete ten-log replay covers 352317 occurrences. Every pipeline
source hash and every pinned learner implementation hash still agrees with that
run, so its full-corpus parity evidence remains applicable. That evidence checks
matching/capture agreement, not universal semantic correctness.

## MODEL-001 — verified closed

Current template `45733db2c420017df63b5164`, source `jomini_eventmanager.cpp`:

```text
'<KEY>' does not have a valid namespace
```

All **45 distinct messages / 334 census occurrences** fully match. Complete
KEY captures include `eps_travel_event.01`, `esp_misc.0012`,
`darkages_less_warfare_women.01` and the `holy_stuff_go_on_relic_pilgrimage_event`
identifiers. The latter prefix is not fixed template wording. The current
learner's candidate consensus uses all distinct member messages, not the old
80-percent position vote; see [artifacts.py](../../../tools/template_learning/artifacts.py:109)
and [derive_pattern](../../../tools/template_learning/patterns.py:348).
Native evidence: **W01–W04** in the readable review.

## MODEL-002 and P-03 — verified closed

Current template `6629fd0b8027f2471e6770da`, source `pdx_localize.cpp`:

```text
Duplicate localization key. Key '<KEY>' is defined in both '<LOCATOR>' and '<LOCATOR>'.
```

All **2048 distinct messages / 7860 census occurrences** fully match. `black`,
`char_interaction.0170.t` and `char_interaction.0170.desc_burned` are each one
complete KEY capture. No per-occurrence PARAM-to-KEY conversion occurs. The raw
parser preserves these dotted spellings, and the pipeline consumes its pieces.
The matcher applies the supplied constraints; it no longer requires every numeric
fragment to have a letter/underscore start. Native evidence: **W05–W07**.

The positive original-byte captures also close the reported runtime limitation:
these are published templates through the actual pipeline, not the historical
in-memory predicate-bypass controls.

## MODEL-003 — repaired representation, remaining coverage

The selected schema-3 model passes `load_selected_classifier()` and artifact/hash
validation. Its complete template tree has only KEY, OPTIONAL_KEY, VALUE, LOCATOR,
PARAM and REASON; **zero TYPE or ALT parts**. The obsolete structural-normalizer
compatibility failure is no longer present.

| Cited native case | Current result and evidence |
|---|---|
| Ci Faj travel message | **Full**, `2f8897f000d8e9aaa8c32cfb`; PARAM `Ci Faj`, literal ` of  (`, PARAM `Internal ID 296591`, literal closing text. No missing native wording or invented historical-ID slot. W10. |
| capital_county.kingdom / Failed context switch | **Full**, `8aea72c0a077d1370746193f`; one KEY, intact REASON, LOCATOR path, LOCATOR `872`, PARAM script trace. One distinct message / 72 census occurrences. W08. |
| Unknown trigger … near line: 261 | **Full**, `7e772a454a300b1d24e7f261`; KEY plus LOCATOR `261`, with `, near line:` literal. Recovered wrapper path and line also remain bound. One distinct child / 67 census occurrences. W09. |
| Former TYPE-bearing cheated-on-partner family | **Full**, `8227e052fb9a203c34edfd29`, for all 208 distinct native messages / 208 occurrences. The varying root/target position is KEY, and complete locations/rich text remain represented. W12. |
| Empty artifact name, ID 83886255 | **Full**, `d43c3a332821b9b600654706`; literal empty quotes, VALUE `83886255`, KEY `generic_material_wood`. No requirement to invent an absent optional field. W15. |
| Named artifact holderplace, ID 100667378 | **Unknown**, no candidate, no declaration error. W16. This cited case remains uncovered. |

The remaining native message is:

```text
Artifact 'holderplace' (100667378) has no feature in group saint_name
```

Current source `artifact_feature.cpp` has the empty-name template
`Artifact '' (<VALUE>) has no feature in group <KEY>`. Its literal empty quotes
cannot match a nonempty name. The exact named witness occurs once in the census
and **zero times in the current ten training logs**; two other holderplace IDs
also occur outside those training logs. This is a model coverage gap, not a
runtime KEY rejection, TYPE/ALT issue or failure to load the model. Original
evidence is retained, and no name slot is fabricated during classification.
Proposed next work is learning from actual named/unnamed variants with the usual
support requirements, not manually editing this template. No new slot-type
decision is required merely to investigate that coverage.

The current travel formulation deliberately treats the ID description as PARAM.
Its content is preserved, not stripped. More consistent name/ID decomposition
remains a separate quality topic accepted as-is by the owner for now.

## Historical effect/proud non-bug; P-01 and P-02

The old claim about absence from eight earlier training logs is historical;
this review does not reinterpret it as absence from today's larger census.
We now have an actual native **stress_impact effect / Cannot find proud in trait
database** message: **full**, template `214eb68c37037a8fbdffad06`, KEY
`stress_impact`, intact REASON `Cannot find proud in trait database`, and its
file/line/trace captures. There are **17 census occurrences** of this native
message; see **W14**. All five observed stress_impact formulations (26 occurrences)
fully match (**W13** provides another reason).

Current source [classifier.py](classifier.py:42) selects complete templates and
retains all alternatives. REASON is a declared bounded field, not an independent
L2-template lookup with allowed-L1 pairings. The old L1-first/independent-L2 routing
requirement is superseded by subsequent owner direction. Current outcomes and
bindings are defined in [domain.py](domain.py:286). The prior full-log replay
checks all three outcome semantics where evidenced; it contains full and
provisional results, and fresh W16 supplies an actual unknown case.

## P-04 — partially resolved, implementation duplication remains

Resolved: learner [evidence.py](../../../tools/template_learning/evidence.py:14)
and pipeline [classifier.py](classifier.py:27) call the selected raw parser.
[raw_input.py](raw_input.py:20) exposes its unchanged pieces and ranges. Runtime
rules come from the selected immutable release, not a mutable learner registry.
Current source/hash checks plus full-log and focused native replay show agreement.

Remaining: KEY/path grammar and full capture matching are implemented separately
in [learner patterns.py](../../../tools/template_learning/patterns.py:54) and
[runtime matching.py](matching.py:26). Pinning the parser and JSON declarations
does not make these executable implementations one shared primitive. The original
drift risk therefore remains open, although **no present divergence was found**.
This audit does not recommend sharing banned historical preprocessing or moving
learner inference into ingestion.

## P-05 through P-08 — selected-path verification

- **P-05:** W08 binds `capital_county.kingdom` intact. The selected parser does
  not split its dots into identifier fragments; the runtime does not insert KEY
  markers. The whole native location tail participates in matching.
- **P-06:** W11 binds `enfp_test.0001` directly using published template
  `30d520985b553a06ec80ff85`, full for its 55 census occurrences. W01–W07 verify
  the same dotted/numeric grammar in other formulations. No fabricated cross-
  context occurrence was used to claim testing the same spelling everywhere.
- **P-07:** W10 demonstrates both preserved content and absence of invented
  slots. `Internal ID 296591` is visible in the actual PARAM capture, not removed
  from matching input. All literal/slot parts reconstruct the original message.
- **P-08:** current classifier imports raw_input/bindings/matching and consumes
  native pieces; it contains no `_Composer`/prefix-peeling stage. W17 captures
  `scope:overlord_scope.culture` including its namespace. That is corroborating
  native evidence; closure of the previously unobserved malformed branch rests
  on source removal, not a synthetic malformed-key probe.

See [classifier.py](classifier.py:42), [raw_input.py](raw_input.py:20),
[matching.py](matching.py:317) and [bindings.py](bindings.py:5). No selected-path
import calls the old normalization view. Old code in other namespaces is not
evidence that the selected classifier still runs those branches.

## MODEL-004 — Near file wording inferred as OPTIONAL_KEY

Owner correction 2026-09-24 supersedes the general OPTIONAL_KEY evidence
recommendation below: a key may be present or absent even when only one present
spelling has been observed. The attempted minimum-present-variation restriction
was reverted and its unpublished candidate marked rejected. The bug remains open.
Investigate contextual location-label equivalence for Near file:/file: through
the learner's JSON declarations, preserving original labels and existing
OPTIONAL_KEY semantics. No label-equivalence rule is implemented yet.

Owner requested this follow-up after the matching-route investigation. Current
model a9fa27a85ccd066285b99fdb, template 1332e889d727946cb5b53eb4:

```text
Unrecognized loc key <KEY>. <OPTIONAL_KEY> file: <LOCATOR> line: <LOCATOR> (<PARAM>)
```

Training evidence: nine complete messages / 90 occurrences with `Near file:`
(every recorded source tag jomini_dynamicdescription.cpp:57), and sixteen /
127 with plain `file:` (all cpp:66). OPTIONAL_KEY s1 has only `Near` plus absence.
Across the 73-log census, Near form has 616 messages / 1255 occurrences and plain
form 928 / 2737. Their 588 and 817 distinct localization keys do not overlap.
Source-line association is evidence of distinct emitted formulations, not a rule
to hard-code cpp line numbers.

The learner compares complete same-source-family messages here, not an independent
global sub-phrase pool. [patterns._slot](../../../tools/template_learning/patterns.py:267)
types a present single non-punctuation token plus absence as OPTIONAL_KEY.
[refine_literal_variants](../../../tools/template_learning/clustering.py:193)
has a one-spelling-plus-absence check for PARAM, not OPTIONAL_KEY. Lexical KEY
eligibility is being mistaken for variable-identifier evidence. Both matchers
faithfully execute the resulting wrong type; this is not evidence of runtime drift.

Recommendation: retain separate fixed `. Near file:` and `. file:` formulations.
No new LOCATOR boundary rule is needed and no optional-literal feature is proposed.
An investigative partition of the actual 25 members, using unchanged inference,
produced both expected templates with all members matching uniquely. This is not
an implemented automatic split. A general OPTIONAL_KEY evidence refinement needs
impact review; the owner previously required separate review of a blanket fixed-
spelling-plus-absence split. No global Near literal, source-line whitelist or
new rule was added. The two other OPTIONAL_KEY positions in the selected model
each have 31 distinct present identifier values, unlike this field.

[Readable findings, native examples and recommendations](../../../.codex-tmp/learner-refactor/near-literal-review/REVIEW.md)
and [complete field support, all members and provenance](../../../.codex-tmp/learner-refactor/near-literal-review/evidence.json).
No code/model changes or publication in this review.

## Historical investigation — superseded status and implementation references

Everything below describes the 2026-09-17–19 investigation of older artifacts.
Its “selected”, “current”, “open” and line-number references apply to that dated
state, not the selected release verified above. It is retained as evidence of
the original reports; do not restore its abandoned model architecture or controls.

Started: 2026-09-17. Updated after the owner's layered-matching clarification.
Stable MODEL issue IDs are retained to avoid losing previous references.
They identify learning/process defects visible in the artifact, not separate
runtime model-repair responsibilities. No retraining or model edit was performed.
The later owner-authorized pipeline routing/outcome change is recorded below;
it does not repair these learning issues.

## Current owner direction

Runtime processing-rule repairs are required now in the Task 04 supplement,
not deferred to a separate learner project. Learner algorithm changes/retraining
remain separate. PARAM is a valid variable-phrase slot; its presence alone is
not a bug or incomplete result. One supplied KEY slot is one complete key value,
not several inferred identifier fragments.

## Mandatory instructions for learner enhancement requests

Owner directive: runtime must impose no restrictions additional to the supplied
error template. Phrase-specific processing, advance semantic slot identification,
literal rewriting and name-to-KEY conversion are banned. The ban applies before
and after matching; relocating a rule is not a fix.

When a developer believes a case needs custom handling beyond its template,
add an explicit learner/model enhancement request here instead of implementing
runtime handling. Preserve the unresolved occurrence and evidence for review.
Do not silently alter the supplied template, retype KEY to PARAM, invent a new
slot type, or add a sentence recognizer to rescue coverage.

Each request must include:

1. Stable issue ID, status and owning component (learner/model generation or
   pipeline implementation). Separate observed facts from hypotheses.
2. Genuine emission text/source, exact local evidence path and location, model
   revision, template ID and actual stored structure where applicable.
3. What the template cannot express or what learner decision is wrong, with
   the actual runtime result. Distinguish an absent template from a pipeline
   rule rejecting or rewriting a template-declared slot.
4. The needed learned structure/type/optionality/constraint as a request,
   clearly labelled proposed. Do not present a hand-created model entry as
   learned or owner-approved.
5. Training coverage evidence where available. Record unknown coverage instead
   of guessing whether the learner had an opportunity to observe the variation.
6. What remains unresolved, how original evidence is retained, and confirmation
   that no compensating phrase rule or extra slot restriction was added. State
   any genuinely necessary owner type/schema decision precisely.

These reports request template/model improvements, not permission for a second
runtime learner. Literal text such as Internal ID stays literal where declared.
CHAR_NAME is a suggested future type only; do not create it or a name-recognition
rule without a model decision.

## Selected model and investigation evidence

Selected model: `43634d23e619ecb4`, SHA-256
`791b37be8fd3de65b613d7d34d5dadcdb7acb275cdac5c25d0fa5e50ba25a5b7`.
Source model: `67303093ecda779d`, learner normalizer v4.11, eight training logs.
Task 03 converted its format; it did not relearn structures.

This review reopened both artifacts, inspected learner and pipeline source,
replayed selected genuine occurrences, and commissioned a read-only learner
investigation. All eight original training logs were located in relocated
runtime sessions and matched against their recorded SHA-256 identities. The
sub-agent read the logs completely for the specified message families; it did
not execute training, change the learner, or adopt deprecated evaluation goals.
Historical v4.6 model observations remain historical context, not a fallback.

## MODEL-001 - Namespace event identifiers incorrectly retained as literals

Status: **Open. Training coverage and majority-stability failure established.**

Source family: `jomini_eventmanager.cpp`.
Source cluster: `3c600d76a0206aba`.
Selected cluster: `45442966e4e35fa0`.

Selected template:

```text
' <PARAM> holy_stuff_go_on_relic_pilgrimage_event <KEY> . <VALUE> ' does not have a valid namespace
```

The learning process incorrectly fixed an event-name prefix into template
content. These event identifiers are keys; they are not localization keys:

```text
'eps_travel_event.01' does not have a valid namespace
'esp_misc.0012' does not have a valid namespace
'darkages_less_warfare_women.01' does not have a valid namespace
```

Training investigation found exactly 66 occurrences and 21 distinct event
identifiers, agreeing with source-cluster support. Eighteen identifiers share
`holy_stuff_go_on_relic_pilgrimage_event` with suffixes .0007 through .0024.
The remaining three are precisely the examples above. Lack of training
opportunity does not explain this defect: all three counterexamples were seen.

[derive_template:1024](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:1024)
retains positions occurring in at least ceil(0.80 * distinct-sequence count)
alignments. Here the threshold is 17; the repeated prefix appears in 18 of 21.
This promotes a variable prefix to a literal despite contradictory observations.
The malformed adjacent PARAM/KEY arrangement additionally involves gap
construction at lines 1039-1059; this review did not replay derivation to prove
the origin of every extra marker.

Recent replay: protected rehearsal session `a3022dc...`, lines 417, 450 and 464,
still returns unknown. That follows the artifact's literal mismatch; it is
not a missing-slot-type outcome. The runtime must not invent missing slots.

Expected direction: the recurring phrase remains fixed and event identity is
represented as variable KEY content, not a specific event name. A single
compound KEY also requires correction of the pipeline limitation P-03 below.
Historical KEY-dot-VALUE structure is comparison evidence, not authority to
reclassify a numeric identifier suffix as a semantic quantity.

Repair belongs in learning/model generation, with contradictory training
examples considered when deriving fixed content. No particular learner patch
or new model has been implemented or certified by this review.

## MODEL-002 - Generic KEY position falls back to PARAM for compound keys

Status: **Open. Concrete corpus and type-grammar evidence established.**

Source family: `pdx_localize.cpp`.
Source cluster: `514c7f0349cf61eb`.
Selected cluster: `f0565bd0fc1252a8`.

```text
Duplicate localization key . Key ' <PARAM> ' is defined in both <LOCATOR> and <LOCATOR> .
```

`black` is an occurrence value in this message, not a literal template token.
The expected slot type is generic KEY. There is no distinct localization-key
slot type in the model; localization is the message's subject.

Across eight verified training logs: 655 occurrences / 84 distinct keys,
matching source-cluster support. Thirteen keys have dotted numeric segments,
including `char_interaction.0170.t`, `char_interaction.0170.desc_burned`, and
`holy_stuff_go_on_relic_pilgrimage_event.0007.desc.opening`.

[Tokenizer and identifier grammar:63](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:63)
split `char_interaction.0170.t` into `char_interaction`, `.`, `0170`, `.`, `t`.
[infer_slot:979](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:979)
removes punctuation, then requires every KEY token to have a letter/underscore
start. The `0170` token fails. Mixed identifier/numeric content also fails
VALUE inference, so the span falls back to PARAM. These real compound values
explain generic typing across the cluster, including its simple `black` key.
Follow-up verification executed the actual pure `infer_slot` function on the
tokenized 84 distinct keys read from all eight hash-verified training inputs:
the function returned PARAM, and 13 keys failed its identifier predicate.
No clustering, template derivation or training run was executed.

Concrete training evidence: runtime session
`990504db5f3cf0cdc219629a3f88b49dd56156f1d78c001783515f32a8a95b5c/error.log`,
line 52 (`black`) and line 60 (`char_interaction.0170.t`).

Expected direction: recognize the complete key position and accommodate the
actual key grammar. The explicit `Key '...'` context is relevant learning
information; no global rule that all quoted text is a key is commissioned.
A model marker change alone is insufficient until P-03 is addressed.

The learned artifact records a KEY marker, not an empirically learned grammar
of allowed key characters. `infer_slot` uses hard-coded type heuristics. It
therefore cannot adapt that grammar simply by seeing more compound-key examples.
Hyphens, underscores and digits after an initial letter/underscore are allowed
by the identifier regex. Dots become separate punctuation tokens; the numeric
segments left after punctuation filtering fail the letter/underscore-start
rule. This is not a blanket ban on compound keys or a key-character-length
limit; it is a restrictive per-token predicate applied to a multi-token span.

PARAM remains a declared broad category in the present artifact. The previous
proposal to automatically mark this occurrence incomplete is withdrawn.
Do not retype it per occurrence during ingestion.

## Investigated non-bug - No complete effect/proud pair in training

The generic effect L1 is present. The reason template
`Cannot find <KEY> in <ALT:law|trait> database` is also present, originally under
a trigger whole template. No template requires the literal keys stress_impact
or proud for this assignment.

The eight verified training inputs contain neither `Cannot find proud in trait
database` nor `effect [ Cannot find ... database ]`, including a whitespace-
flexible multiline search. They contain three stress_impact effect occurrences,
all with `Wrong scope for effect: none, expected character`:

- session `990504db5f3cf0cdc219629a3f88b49dd56156f1d78c001783515f32a8a95b5c`, line 50810;
- session `e994c844d678ef0003a9873ae39805b08b300f17da5c68990b9d9fd9186b95ed`, lines 41040 and 164957.

Thus no failure to learn an observed complete target pair is established.
The owner's current rule permits L1-then-L2 composition regardless of original
pairing, so the absent whole combination does not block a complete layered match.

## Pipeline findings, separate from learner repair

### P-01 - Previous independent-L2 defect claim withdrawn

Cross-L1 reuse is expressly permitted after matching L1. The existing classifier
already gates its independent L2 lookup on L1 success. The real stress_impact
occurrence assigned an effect L1, not a trigger L1. The earlier restriction to
whole-template pairings was an incorrect recommendation and must not be applied.

### P-02 - Routing implemented; runtime rule cleanup assigned to Task 04

Classifier revision v2 now uses `matched to template`, `L1` and `unknown`.
Recognized layered occurrences match L1 before considering independent L2s.
Layered matches carry separate L1/L2 references and no whole-template reference.
Focused real-log routing and binding checks passed. No incomplete result is
implemented. The owner's latest direction requires removal of extra runtime
restrictions and pre-matching slot decisions in the Task 04 supplement. Learner
retraining remains separate. Do not equate valid PARAM phrase slots with missing
metadata automatically.

### P-03 - Compound KEY grammar incompatible with genuine identifiers

Confirmed with current `_accepts('<KEY>', tokenize(actual_value))`:

| Actual value | Accepted as one KEY |
|---|---|
| black | yes |
| proud | yes |
| stress_impact | yes |
| eps_travel_event.01 | no |
| char_interaction.0170.t | no |

[classifier.py:44](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py:44)
requires every meaningful token to satisfy the same letter-start identifier
shape. A corrected model with one KEY at these positions would still reject
the dotted numeric keys. This is a pipeline limitation that must be addressed
alongside compatible learner typing, not concealed by a new runtime template.

Full-path follow-up confirmed this with native emission parsing, recovery,
normalization and classification on unchanged captured messages. In isolated
in-memory model candidates, the namespace identifier was represented as one
KEY; the duplicate-key template's PARAM was replaced with KEY. These proposed
templates were diagnostic controls, not learned/published model revisions.

| Genuine occurrence value | Proposed KEY template, existing predicate | Same template, only KEY predicate bypassed |
|---|---|---|
| black | matched to template | matched to template |
| eps_travel_event.01 | unknown | matched to template |
| char_interaction.0170.t | unknown | matched to template |

The bypassed control bound each complete original key correctly. This isolates
the runtime rejection to KEY acceptance, rather than a lost value, failed
literal match or inability to align a multi-token slot. The bypass was scoped
to the investigation process; it is not a proposed blanket removal of checking.
The result is specifically about unmasked key spans: normalized KEY markers
from existing contextual grammars take another acceptance path.

[Investigation report](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/check_compound_key_rejection.json)

Do not tighten every KEY to a simple identifier: existing contextual rules
also use KEY for some numeric character IDs and display names. Marker equality
alone is not independent semantic proof, but no observed misbinding caused by
that shortcut was established here. No universal semantic validator is proposed.

### P-04 - Separate learner/runtime interpretation can drift

Status: runtime correction is included in Task 04's supplement; integration
with future learner work remains separate. The learner has its own tokenizer,
normalization and infer_slot plus the
older log-block parser. The replacement pipeline has separate native emission
and diagnostic processing, normalization, and slot acceptance. Some rules were
ported rather than shared. Both presently reject the compound-key spans in
P-03; changing one side alone would cause a learner/runtime disagreement.

Sharing emission lexing alone does not resolve type acceptance. A multi-token
identifier can occupy one KEY slot, so learning and ingestion need a common
slot grammar and interpretation contract as well as consistent normalization.
Recommended direction: reusable runtime-safe processing/type primitives consumed
by both paths, with learning/clustering remaining outside runtime. Revision
checks are useful but do not prove duplicated rules are behaviorally identical.
See the Task 03 handover's shared-contract note. No refactor was performed.

### P-05 through P-08 - Runtime interpretation before model matching

The owner's follow-up audit established broader pipeline defects, documented
with exact locations and real-occurrence controls in
[PIPELINE_RULE_AUDIT.md](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/PIPELINE_RULE_AUDIT.md).

- P-05: `_Composer.key_path` splits dotted expressions into multiple KEY markers
  before matching. Existing single-KEY template 9b8215b4dc87ccfc fails on the
  real capital_county.kingdom occurrence with this normalization, but succeeds
  and binds the complete value when only that rule is bypassed in memory.
- P-06: phrase-specific masks plus marker-equality acceptance make identical
  values subject to different KEY criteria. Real enfp_test.0001 is accepted in
  an orphan-event message but fails raw KEY acceptance.
- P-07: message recipes remove matching literals and insert typed/optional
  slots before consulting the model. A real travel message binds Ci Faj of,
  numeric 296591, and an inserted absent historical-ID marker as coded types.
- P-08: a source-level invalid-key-path branch can drop a recognized namespace
  prefix from matching text. No occurrence of that branch was found in the
  three logs inspected; do not claim an observed failure.

These are pipeline findings, not issues to attribute solely to learner quality.
Source fixes are now required in the Task 04 supplement; the investigation
itself changed documentation and ignored review artifacts only. Sharing existing rules would not
resolve their conflict with the supplied-template authority boundary.

## Evidence artifacts

- [All 238 pairs and shared L2 structures](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/layered-template-pairs.md)
- [Real occurrence traces](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/real-occurrence-traces.json)
- [KEY acceptance probes using actual observed values](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/key-grammar-checks.json)
- [Current owner directions](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/OWNER_TEMPLATE_ASSIGNMENT_INSTRUCTIONS.md)

Generated review evidence stays in ignored local storage; original logs and
models were read only. MODEL-001, MODEL-002 and pipeline P-03 remain unresolved.

## MODEL-003 - Native template representation after P1 cleanup

Status: open, 2026-09-19. Owner: separate learner/model-generation team for
artifact changes; pipeline compatibility enforcement is implemented in P1.
This extends the representation dependency behind P-04 through P-07. It does
not replace MODEL-001/002 or the previously recorded truncated-template gap.

The selected model remains revision `43634d23e619ecb4`, with the SHA-256
recorded above. Its manifest and model require
`ck3-native-structural-normalizer-v1`. P1 removes that revision's sentence
rewrites, masks and extra slot restrictions. The runtime now requires
`ck3-native-literal-view-v2`, with classifier revision
`ck3-exact-empirical-classifier-v4` after the owner's slot-support correction
(initial P1 used v3). Catalog/model loading raises
`ModelCompatibilityError` for the unchanged selected artifact. This is a
loading failure, not an `unknown` classification, and prevents using the old
artifact as though it described native text. Relabelling its revision is not
a valid conversion.

The initial P1 restriction to KEY/PARAM was an implementation mistake, corrected
after owner review. Supported slots are KEY, PARAM, LOCATOR, VALUE and
OPTIONAL_KEY. The current structural matcher captures nonempty template-delimited
text for LOCATOR/VALUE and preserves their declared labels; it does not certify
path validity or numeric validity. Detailed validation remains a shared-contract
decision. OPTIONAL_KEY permits one continuous key or absence only at its supplied
template position. An absent capture has empty text and a zero-width native
boundary; no placeholder token, historical-ID slot or surrounding literal is
invented.

ALT remains unsupported and the owner will have it removed by the learner team.
TYPE remains unsupported pending clarification. Its actual origin is a
sentence-specific learner rewrite: `SCRIPTED_EFFECT_KEY_RE` captures
`root|target` before `cheated on a partner that they wouldn't have`, then
`normalize_known_key_grammars` replaces that word with TYPE. The selected model
contains one TYPE-bearing template, `4d2438c6013a2390`, in
`jomini_effect_impl.cpp`:

`<LOCATOR> <KEY> : <TYPE> cheated on a partner that they wouldn ' t have Cheater : <KEY> With : <KEY>`

This is neither the diagnostic error_type nor a general type definition.
The separate learner team needs to remove/replace or explicitly define that
encoding; no TYPE recognizer or runtime retyping has been introduced.
Source: `tools/template_learning/learn_error_templates.py`,
`SCRIPTED_EFFECT_KEY_RE` and `normalize_known_key_grammars`.

The immediate selected-model loading failure still precedes any slot inspection:
the catalog checks the old normalization revision in the pinned manifest first.
The pipeline owns this explicit check and the eventual catalog revision/hash
selection; the learner/model team owns supplying compatible native templates,
not merely relabelling old content. No rollback to the old preprocessing is
authorized or implemented.

### Genuine evidence and observed results

Protected log B:

`C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/benchmarks/ingestion/legacy-pending-rehearsal-20260908-01/sessions/1fc0ecb983d7c3726d880384a38581e6c6daa6c58870f0cbc01e6e1857e7c7d2/error.log`

SHA-256: `16d3ab935f938e63ae3dd460dfeffeee6f32c2a31d95782fd787356f1afce196`.

The results below use explicitly labelled in-memory native-template controls.
Where stated, token sequences are copied unchanged from the selected artifact.
They are not a converted/published model or a successful selected-model replay.

1. **Line 4904, characterlocationdata.cpp:151.** Native message:

   `Removing travel plan from the character Ci Faj of  (Internal ID 296591) owner when the travel plan is not ending normally.`

   Stored template `991ba68d50653950`:

   `Removing travel plan from the character <KEY> ( <KEY> <OPTIONAL_KEY> ) owner when the travel plan is not ending normally .`

   The repaired view keeps `Internal ID`, `of` and every other literal.
   It neither invents an optional value nor assigns the name to KEY.
   Restoring OPTIONAL_KEY support does not repair this template's deleted
   literals or its multi-word name assigned to KEY. A **proposed,
   unpublished control**, using `<PARAM> of ( Internal ID <KEY> )` within the
   unchanged surrounding sentence, captures `Ci Faj` and `296591` with their
   original spans. This verifies the mechanism, not a learned contract.
   Request: derive native structures covering the actual display variants;
   do not add a name recognizer. The selected artifact reports 292 supporting
   occurrences across seven evidence hashes. This particular log's hash is
   not one of them; variant coverage in the training logs was not rechecked.

2. **Line 4747, jomini_script_system.cpp:303.** The complete recovered text is:

   `Script system error! Error: capital_county.kingdom trigger [ Failed context switch ] Script location: file: common/activities/guest_invite_rules/activity_invite_rules.txt line: 872 (activity_invite_rule_local_exam_entrants)`

   Stored template `9b8215b4dc87ccfc` supplies
   `Script system error ! Error : <KEY> trigger [ Failed context switch ]`.
   Its unchanged tokens in a native-format control now bind
   `capital_county.kingdom` as one KEY and yield `L1`. The location tail
   remains present; the current layered representation requires a terminal
   `]`, so it cannot represent this complete native occurrence. The earlier
   audit's abbreviated message omitted this tail. Request: represent native
   trailing evidence explicitly in the shared template/layer format; do not
   restore a runtime rule that strips it. This requires a producer/consumer
   representation decision. The model reports 20,164 supporting occurrences;
   complete native tail coverage in training was not established in P1.

3. **Line 301, pdx_persistent_reader.cpp:216.** Recovered child:

   `Unknown trigger: has_graphical_celtic_culture_group_trigger, near line: 261`

   Stored template `a7451146877a3211` is `Unknown trigger : <KEY>`.
   Its unchanged tokens in a native-format control yield `unknown`: the
   native near-line clause is no longer removed before matching. A proposed
   control with `, near line : <KEY>` appended captures the key and `261`.
   Request: derive a structure that accounts for the native clause, rather
   than silently dropping its suffix. This is not approval of that proposed
   structure or of locator semantics. The model reports 7,434 supporting
   occurrences; native suffix variation was not re-evaluated in training.
   The cause is now confirmed directly in learner source:
   `normalize_persistent_clause` removes `PERSISTENT_NEAR_LINE_RE` before
   template derivation; the earlier pipeline repeated that removal. Thus the
   model was derived from suffix-stripped text. The model did not instruct
   the pipeline to strip it during matching. Repair belongs in native model
   generation, not restoration of the runtime rewrite.

All three originals remain in protected storage. Results retain their parent,
child/shared boundaries and native byte access. No compensating phrase rule,
template edit, retyping or learner change was introduced. The recovery splitter
still only establishes known child boundaries and preserves shared evidence.

### P1 verification limits and continuation

Sixteen bounded implementation checks passed, using seven genuine occurrences
from two retained logs plus clearly separate in-memory controls. Genuine
occurrences establish literal preservation, complete numeric/punctuated KEY
binding and variable PARAM capture. Ambiguity, source restrictions, all result
shapes, L1-first routing and independent L2 reuse also passed controls.
The independent-L2 control does not establish full-native-log L2 coverage:
the inspected real layered examples carry the unresolved location-tail
dependency above. No selected-model compatibility or complete P2 verification
is claimed. Temporary reader-check artifacts were removed.

Pipeline findings P-03 and P-05 through P-08 have their prohibited rules removed
in P1; P-08 remains a source-level finding, not a newly observed real occurrence.
P-04's cross-team representation dependency remains open. The earlier issue
descriptions and evidence are retained as historical investigation records.

Owner-review correction checks: 21 bounded checks passed using eleven genuine
occurrences across the same two retained logs plus separate in-memory controls.
Additional real evidence: log B line 6009 (`Artifact '' (83886255) has no feature
in group generic_material_wood`) and line 8889 (`Artifact 'holderplace'
(100667378) has no feature in group saint_name`) use the unchanged tokens of
template `7828dde850e31fd7` in native-format controls. Both capture the
declared OPTIONAL_KEY correctly, absent and present respectively.
Log A (the previously linked retained session
`a3022dc1381f74f842ad02581d57576a1d4be257592b5d92afd970de304d6a69`) lines 1
and 52 exercise native LOCATOR spans using unchanged template tokens
`cc1ebecbb4106ed7` and `f0565bd0fc1252a8`. The line-301 child also passes a
proposed control using VALUE for its native line number. These checks establish
structural capture/binding, not new approved per-template semantics or full
selected-model compatibility. Empty optional boundaries, literal coverage,
ambiguity and the previous P1 checks pass; temporary reader-check files were
removed. Learner code and supplied artifacts remain unchanged.
