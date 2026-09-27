# Diagnostic-wording loss check

## Current implementation: v40

The retained CK3 symbol-type reference now checks literal loss into **KEY,
OPTIONAL_KEY and PARAM**, selected by `diagnostic_wording_loss.target_slot_types`
in the owner-approved JSON. This closes the PARAM-only implementation gap under
the owner's 2026-09-26 direction. Whole raw-token/phrase matching and exclusion
of all previous captures remain unchanged; presumed/default literals remain
disabled. Rejection evidence names `proposed_slot` and `proposed_slot_type`.

For KEY/OPTIONAL_KEY proposals only, corresponding native fields with at least
two distinct nonempty values and the same enclosing pair across every member
can outweigh symbol-list loss. Both the loss and positive evidence are recorded.
Enclosure alone is insufficient; PARAM loss protection is unchanged. This avoids
forcing demonstrated quoted scope values such as `army` into literal wording.

See LEARNER_SYMBOL_SLOT_LOSS_V40.md for current native validation and the status
of the separate, still unimplemented adjective-resistance proposal. The account
below records historical stages; its references to coverage-merging paths and
adjective dependencies do not describe the current code.

## Historical v31 implementation and subsequent studies

Owner directive: 2026-09-25. Implemented in learner v31; default-literal guidance
remains disabled. This implements the requested reference-wording blocker, not
the entire earlier PARAM-context/merge proposal. No production model is repinned.

## Behavior

For an existing inferred template, find listed words and complete phrases in its
actual literal spans on native members. Compare those spans with a proposed
replacement's PARAM ranges. Reject the generalization if a listed literal would
be swallowed, including enlargement of an existing PARAM. Preserve the rejected
proposal, previous patterns, wording, source, native witness and byte spans in
the discovery review. Increased coverage cannot override the rejection.

All pre-existing captured fields are excluded. A listed word already inside a
KEY, LOCATOR, trace, REASON or PARAM is not lost literal wording. Matching uses
complete selected-parser pieces and declared phrase boundaries, never identifier
substrings. A partly swallowed complete phrase also counts; moving only whitespace
does not. Bracket enclosure does not exempt a proposed generalization.

The shared guard covers region regrouping, coverage-driven absorption (both calls),
same-wording consolidation and established-wording refinement. Duplicate-ID
re-inference is also checked; an unexpected loss there aborts the build rather
than publishing altered contracts under an identical-contract consolidation.

The implementation is in `tools/template_learning/diagnostic_wording.py`; the
declaration is `owner_rules.json.diagnostic_wording_loss`. The learner identity
includes that source file. Runtime matching does not consult this vocabulary.

## Reference vocabulary and language-tool work

The retained reference contains 45 CK3 symbol-type word spellings and complete
multiword type phrases. The check reuses that list, including its declared
first-letter case variants. It does not derive type names from path folders.
Only the explicitly selected failure-word subset is active from the former
diagnostic-word list; incidental words such as `of`, `line` and `was` are not
activated as independent blockers. The retained list is not claimed exhaustive.

Owner subsequently clarified that negative-adjective discovery is the exploration
target. `survey_adjectives.py` uses NLTK's English POS tagger on existing raw tokens
within eligible literal/PARAM regions from the complete native message corpus. It
records tags, counts, sources and actual native examples. It does not call another
tokenizer or install POS tagging in the inference/matching path. The main report
selects adjective tags JJ/JJR/JJS; participial readings VBN/VBG are shown separately
for contextual review, not silently treated as adjectives. Tags do not prove
diagnostic meaning or automatically activate blockers. NLTK is an optional
development dependency.

The owner installed NLTK 3.10.3 and the English tagger data, then clarified the
scope: individual negative adjectives in literals or possibly PARAMs, excluding
all LOCATOR contents before language evaluation. The earlier broad adjective
survey and neutral-adjective recommendations are superseded. Malformed and token
were always separate raw tokens; the earlier presentation confusingly showed the
surrounding native phrase.

The corrected pass scans 38,621 contextual rows representing all 1,143,064
occurrences. It excludes 271,500 LOCATOR tokens before tagging; common disappears.
Only contiguous literal and PARAM regions enter NLTK, separately. Seventeen
ambiguous-assignment rows are counted but not tagged; other slot types including
REASON are excluded. Current model captures supply survey regions, not grammatical
truth. Negative meaning is assessed from native contexts, not inferred from a
POS label alone.

Current recommendations and eleven proposed additions are in
`.codex-tmp/learner-refactor/adjective-review/NEGATIVE_ADJECTIVES.md`; raw pieces,
tagger inputs' scope, witnesses, tags and hashes are under `negative-scoped-survey/`.
No active vocabulary, inference, matcher or model change was made. PARAM content
remains inspection evidence, not a reason to activate the literal-loss blocker
on words already inside that PARAM.

## Native verification

Evidence is under `.codex-tmp/learner-refactor/wording-loss-v31/` (ignored).
`NATIVE_EXAMPLES.md` shows actual native messages, old and proposed templates,
swallowed wording, raw pieces and decisions. Frozen v30 models are comparison
evidence only; fresh v31 builds import no templates.

The saved native broad proposal `<PARAM>: <PARAM>, near line: <LOCATOR>` is rejected
against these actual earlier formulations:

| Existing formulation | Listed wording lost | Decision |
|---|---|---|
| `Unknown trigger: <KEY>, near line: <LOCATOR>` | `Unknown`, `trigger` | Reject |
| `Unknown effect: <KEY>, near line: <LOCATOR>` | `Unknown`, `effect` | Reject |
| `Unknown holy site '<KEY>': holy_site, near line: <LOCATOR>` | `Unknown`, `holy site` | Reject |
| `Failed to read key reference: <OPTIONAL_KEY>: <OPTIONAL_KEY>, near line: <LOCATOR>` | `Failed` | Reject |
| `Failed to read key reference: }: }, near line: <LOCATOR>` | `Failed` | Reject; does not validate the malformed value |

Checking 896 native members against their unchanged templates produces zero loss
flags. A subsequent complete ten-log control covers all 297 original templates
and 7,827 distinct native members, also with zero loss flags. It includes 631
listed-word hits already inside PARAMs, 473 inside KEYs, 4,430 inside LOCATORs and
5,314 inside REASONs. These are listed-phrase hits, not independent error counts.
No synthetic messages were used.

Fresh ten-log run: 352,317 messages; 298 templates (165 supported, 133 provisional).
Compared with v30, one occurrence changes: `Assertion failed: Invalid faction
update day, updating it to avoid more problems`. The check preserves its literal
candidate instead of allowing a broader PARAM candidate to absorb it. Both still
match, so the outcome changes from full to provisional. This exposes a remaining
overlap; the blocker alone does not remove an already-existing broad candidate.
All other ten-log contextual assignments/captures are unchanged. The fresh build
records 19 rejection events: 18 in region regrouping and one in coverage-driven
absorption. Rejection events can include repeated proposals; they are not counts
of independently corrected error types.

The complete thirty-log run finished: 1,143,064 messages, 416 templates (246
supported, 170 provisional), no parser-unresolved emissions. It records 31 blocked
proposal events (29 region-regrouping, two coverage-absorption). The broad
`<PARAM>: <PARAM>, near line: <LOCATOR>` no longer exists in the new model.

`RUN_REVIEW.md` shows each changed formulation and actual rejected proposals in
ordinary template notation. `changes.json` retains actual captures and competing
capture-ambiguous candidates as well. Inspectable improvements include:

- 26,721 `Unknown trigger` occurrences regain that wording and a KEY capture.
- 4,097 `Unexpected token` occurrences regain that wording and a KEY capture.
- 178 `Unknown effect` and 87 `Unknown holy site` occurrences regain their wording.
- All 22,574 key-reference occurrences made provisional by the old broad PARAM
  candidate now have one supported match. This includes 513 cases where the broad
  candidate had multiple capture divisions, not a unique ordinary match.

There are 112 full-to-provisional changes. Of these, 109 retain one literal
formulation with insufficient independent variation: 99 `Character with no
location` messages, three `Invalid army found` messages, three malformed-brace
key references, three malformed-token brace messages and one `ai_check_interval`
message. These are reduced claims of support, not additional matching ambiguity.
Three occurrences have newly exposed overlapping candidates: two assertion
messages described above and one `Unop: destination_2 is undefined` message in
`jomini_effect_impl.cpp`. The existing broad PARAM candidate remains beside a
preserved literal candidate in each of those two formulations. No winner rule
was introduced to conceal those overlaps.

| Same thirty-log evidence | Original ten cohort | Added twenty cohort |
|---|---:|---:|
| Provisional to one supported match | 8,343 | 14,231 |
| Full to provisional | 16 | 96 |

Totals move from 679,252 full / 463,812 provisional to 701,714 full / 441,350
provisional; unknown remains zero. These are matching outcomes, not accuracy.
There are 1,708 changed contextual rows representing 53,862 occurrences, including
wording/capture improvements that remain classified full before and after.

Fresh review revisions: ten-log `8973261d53bac90dfc6d6f9f`, thirty-log
`8fc7bfaae87d27f911852f08`. The production selection remains unchanged. The
LOCATOR-to-PARAM texture-path issue and the broader context/boundary mechanics
remain outside this targeted correction. Successful loss detection does not
establish that retained templates are otherwise correct.

## Current-v36 adjective ablation — 2026-09-26

Subsequent owner disposition: v37 removes the error-word reference from active
learner code, its JSON selection and loader, the NLTK optional dependency, and
the packaged research tools. Their historical source/evidence is archived under
adjective-ablation-v36/archived-tools, outside the production package. The CK3
symbol-type loss check remains. Fresh ten/thirty builds reproduce all v36
templates and captures exactly. The recommendation below is historical; this
idea is now removed from production, not merely deactivated.

The owner requested an actual trial of the negative-adjective proposals. Fresh
inference on the same complete native ten/thirty logs compares the current list,
no error words, and the current list plus the eleven scoped survey additions.
CK3 symbol-type checks stay identical; default literals stay disabled. The
selected parser remains v1.6 for this controlled comparison. No production rules
or model pin changed. The separate parser-v1.7 release is outside this study.

Additions tested: Malformed, Unexpected, Missing, Illegal, Unrecognized,
Inconsistent, unset, unused, unhandled, negative, null. This is a list of proposed
negative descriptors; membership is not a grammatical guarantee in all contexts.

All three arms produce identical templates and native assignments/captures:
ten logs: 352,317 messages, 392 templates (188 supported, 204 provisional);
thirty logs: 1,143,064 messages, 600 templates (296 supported, 304 provisional).
Zero changes in either cohort; zero literal-to-PARAM rejection events. The
separate established-word-sequence-to-KEY-run guard records eight rejections in
every arm. Exact byte checks cover 38,882 / 187,295 captures per arm respectively.

Recommendation: leave the adjective additions inactive; no current improvement
is demonstrated. Earlier v31 combined-list benefits above are historical and
do not prove marginal adjective benefit under today's proposal/merge mechanics.
This finite ablation is not a claim that diagnostic adjectives can never help.

Research harness: tools/template_learning/compare_adjective_guidance.py.
Inputs, process-local declarations, immutable-source identity, per-arm models,
native rows and readable findings: .codex-tmp/learner-refactor/adjective-ablation-v36/.
