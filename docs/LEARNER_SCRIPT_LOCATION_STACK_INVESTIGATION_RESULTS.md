# Script location stack investigation

2026-09-28. Investigation only; no representation, selection, parser, matcher,
pipeline, SQL or watcher change is authorized or implemented by this work.

## Decision and scope

**Zero demonstrated stack-length misses and zero lost location fields in the
73-log retained corpus.** All 1,174,361 Script location diagnostics received a
complete template or provisional assignment, including stacks up to 55 entries.

Retain the current representation for the active package. Its flat templates
constrain stack length, so an otherwise familiar diagnostic at a length without
an applicable complete definition can remain unmatched. That is a potential
generalization limitation, not evidence that the current parser truncates stacks
or that unmatched evidence is discarded. The measurements below distinguish
these claims.

An ordered repeated-frame representation is a reasonable future candidate for
reducing this constraint and definition duplication. It requires an explicit
model/API decision and native evaluation; it is not a Task 07 prerequisite.
Neither a whole-chain PARAM nor treating individual frames as separate errors
would satisfy the owner's requirement.

Actual selection was read from [selection.json](../models/selection.json):

| Identity | Value |
|---|---|
| Package | `68f1ae5db205ab46afef9c4d` |
| Model | `f5cde2616f35d563118d3d32` |
| Manifest SHA-256 | `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f` |
| Model / matcher | schema 5 / `ck3-native-matcher-v2` |
| Parser | `ck3-lossless-v1.7`, SHA-256 `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |

This is the Task 06 integration baseline, superseding the learner handoff's
historical delivery-time statements that v45 was not yet selected.

## Evidence and method

Read the saved [sample JSON](../.codex-tmp/task06-v45/sql-view/sample.json)
and [SQL viewer](../.codex-tmp/task06-v45/sql-view/sql-diagnostic-sample.html).
The random sample was not regenerated. Position 17 is SQL Run
`20260928-K2MKAF`, record ordinal 1291, definition 26, native emission 2978;
it is not native diagnostic ordinal 17.

The [Task 06 inventory](../.codex-tmp/task06-v45/verified/inputs.json) identifies
seven complete native logs. Contrary to the starting description,
[learner-date-key/inputs.json](../.codex-tmp/learner-date-key/inputs.json) currently
contains only two logs, both in that seven-log set. The expanded investigation
uses the retained [v45 73-log inventory](../.codex-tmp/learner-release-v45/inputs-all.json),
which includes both supplied inventories. This is the readable retained release
corpus, not a claim to have surveyed every capture on the machine or unseen CK3
output. It was used for v45 learning; these measurements are in-corpus coverage.

[Investigation tooling](../tools/template_learning/investigate_script_location_stacks.py)
authenticates the selected package, parses every complete native log afresh,
checks input SHA-256 before and after use, and verifies that recovery spans
partition all original bytes. It calls the packaged shared matcher for each
distinct complete contextual input within each log. The cache includes source,
parser, context, native body/pieces, wrappers and ordered continuations; it does
not match excerpts or rewrite messages. Outcomes are weighted by original
occurrences, not by SQL record counts or repeated files.

For measurement only, the tool inventories lines after native `Script location:`.
It counts the first file/line entry and each following file/line entry in order.
Literal `Unknown` is a separate category, not a zero-length known-location stack.
Unrecognized tail lines are explicit investigation problems. The measurement
expression never decides eligibility or supplies matching boundaries.
Other location-bearing formulations such as `Stack trace:` and `From:` are not
included in the Script location length denominator; all recovered diagnostics
still contribute to the corpus-wide outcome totals.

For selected Script location messages, the existing contract renderer checks the
entire body, including whitespace, line endings and literal choices, once per
distinct input. Each location file, numeric line and parenthetical interior is
compared with the selected capture's exact span and type. The existing pipeline
binder checks every selected capture against every occurrence's original bytes.
This distinguishes correct field boundaries from mere text reconstruction.

[Reporting tooling](../tools/template_learning/report_script_location_stacks.py)
also reconciles raw marker counts, compares the viewer's embedded data with the
saved sample, and reads the existing Task 06 review shards without writing them.
All generated evidence remains under the ignored
[investigation directory](../.codex-tmp/learner-script-location-stacks/verified/).

## Measured impact

All **73 inputs / 596,625,707 bytes** were available and hash-verified. Recovery
accounted for **2,517,940 original emissions / 2,594,588 diagnostic occurrences**,
with **zero unresolved recoveries**. The matcher was called for **193,107 distinct
complete inputs within logs**; duplicates between different logs remain separate
calls. Counts below weight all original occurrences.

| Population | Diagnostic occurrences | Template | Provisional | No match |
|---|---:|---:|---:|---:|
| All 73 complete logs | 2,594,588 | 2,439,711 | 154,873 | 4 |
| Script location, known file/line entries | 1,165,336 | 1,110,546 | 54,790 | 0 |
| Script location, literal Unknown | 9,025 | 0 | 9,025 | 0 |
| All Script location diagnostics | 1,174,361 | 1,110,546 | 63,815 | 0 |
| Task 06 seven-log subset, all diagnostics | 418,168 | 399,035 | 19,129 | 4 |
| Task 06 subset, Script location including Unknown | 146,662 | 137,270 | 9,392 | 0 |

The Script location population comprises **15,567 distinct complete inputs**
(15,563 with file/line frames, four with Unknown), appearing as 37,782 distinct
input-within-log rows. There are **1,807,351 ordered location entries**:
1,807,116 with parenthetical traces and **235 without a parenthetical**. All
**5,421,818 native location field instances** map exactly to their own LOCATOR /
LOCATOR / PARAM captures as applicable. None is swallowed into a larger capture,
retyped, omitted, or merely reconstructed from a literal. Complete Script bodies
render exactly; **7,498,776 selected bindings**, including opening fields, were
checked against original occurrence bytes. Raw `Script location:` marker counts
independently reconcile to 1,174,361.

Observed **33 stack lengths**, with outcomes per diagnostic (not per frame):

| Entries | Template | Provisional | No match |
|---:|---:|---:|---:|
| 1 | 733,652 | 12 | 0 |
| 2 | 293,279 | 445 | 0 |
| 3 | 47,216 | 54,185 | 0 |
| 4 | 14,023 | 8 | 0 |
| 5 | 18,850 | 6 | 0 |
| 6 | 1,803 | 1 | 0 |
| 7 | 434 | 1 | 0 |
| 8 | 539 | 41 | 0 |
| 9 | 85 | 2 | 0 |
| 10 | 75 | 0 | 0 |
| 11 | 33 | 0 | 0 |
| 12 | 58 | 0 | 0 |
| 13 | 67 | 2 | 0 |
| 14 | 42 | 2 | 0 |
| 15 | 48 | 62 | 0 |
| 16 | 51 | 0 | 0 |
| 17 | 22 | 0 | 0 |
| 18 | 82 | 0 | 0 |
| 19 | 65 | 1 | 0 |
| 20 | 19 | 3 | 0 |
| 21 | 14 | 0 | 0 |
| 22 | 22 | 3 | 0 |
| 23 | 19 | 2 | 0 |
| 24 | 2 | 3 | 0 |
| 25 | 17 | 1 | 0 |
| 26 | 8 | 0 | 0 |
| 27 | 17 | 1 | 0 |
| 28 | 0 | 5 | 0 |
| 29 | 2 | 0 | 0 |
| 30 | 2 | 1 | 0 |
| 33 | 0 | 1 | 0 |
| 41 | 0 | 1 | 0 |
| 55 | 0 | 1 | 0 |

Unknown has no native file/line entry and is reported separately above. The
seven-log per-length breakdown is retained in `summary.json`; that subset has
246,286 frames and 8,942 Unknown diagnostics. No other lengths were observed.

Provisional does not mean a location failed to match. For example, 54,180 of the
54,185 three-frame provisional occurrences use three complete singleton
definitions, each repeated 18,060 times (`d1ffad737de3154fbb3b4b34`,
`8a309877701d4def24be15d8`, `1e4925dd79ce5d80803191ea`). Repetition does not create
independent support. The appendix separately shows a fifteen-frame template tie.
Both cases preserve all frames and remain record eligible.

There are **251 published Script location definitions** out of 689, with 247
selected at least once in this replay. They have 91 distinct displayed openings
before the location marker. The generic `<KEY> trigger [ <REASON> ]` opening alone
has 19 definitions at lengths 1–9, 12, 15–19, 21, 23, 27 and 30. This measures
representation duplication; it is not a proven count of safely mergeable contracts.

**Causal finding:** zero length-caused misses out of 1,165,336 known-location
diagnostics, and zero out of all 1,174,361 Script location diagnostics. There are
zero observed missing-length variants, recovery failures, shared-matching failures
or location-field losses within that population. All four corpus-wide no-matches
lack a Script location tail. Their exact native emissions remain in the four
nonempty Task 06 review shards; fresh associations, native bytes and shard hashes
agree. The other three Task 06 shards are correctly empty.

**Limits:** this is the selected model's own 73-log learning corpus. It does not
prove coverage of a future length, changed wording, malformed/incomplete tail or
unseen frame layout. There was no genuine length-caused failure to use as a
counterexample, no unresolved Script recovery witness, and no evidence of loss
from an unrepresented length. Those are coverage gaps, not invented failures or
claims that the representation generalizes without limit.

## Where stack length is constrained

1. **Recovery does not impose a fixed frame count.** The pinned parser's
   [`_single_structure`](../models/candidates/68f1ae5db205ab46afef9c4d/parser.py)
   recognizes one Script error envelope, requires exactly one `Error:` and one
   `Script location:` introducer, accepts `Unknown` or a file/line first entry,
   then checks every remaining nonempty line as a file/line entry. It returns the
   complete emission body as one `script-error` message. There is no truncation
   after the first frame and no numeric maximum. Unsupported framing is unresolved
   evidence. Its syntax gate is real; a future unfamiliar spelling could fail
   recovery independently of stack length.
2. **Learning currently separates ordered parameter structures.**
   [`grouping_scope`](../tools/template_learning/clustering.py) includes the full
   ordered declaration tuple. The current `located-parenthetical` declaration
   recognizes each balanced trace interior following a file/line pair; it excludes
   that file and line from PARAM. [`_pattern`](../tools/template_learning/artifacts.py)
   publishes one declaration entry per recognized interior plus flat literal/slot
   parts. Thus one parenthetical-bearing frame yields one entry; four yield four.
   A genuine file/line entry without a parenthetical has no such parameter entry;
   its length is still constrained by the flat parts. The declaration sequence is
   not a universal frame counter or a count of tokens inside a PARAM.
3. **Shared applicability enforces that same sequence.**
   [`Rules.applies_to_record`](../models/candidates/68f1ae5db205ab46afef9c4d/matching_primitives.py)
   checks source, context, construction and exact ordered `parameter_structures`
   equality. `analyze_match_pattern` then requires every literal/slot part and
   complete input exhaustion. The one-frame trigger definition cannot match the
   four-frame trigger just by stretching its final PARAM: its applicability fails
   first, and its flat complete layout is different.
4. **Bindings preserve all selected entries.**
   [`Matcher._region`](../models/candidates/68f1ae5db205ab46afef9c4d/native_matching.py)
   checks slot order, exact capture byte spans, literal choices and whole-region
   reconstruction. [`bind_captures`](../src/ck3chronicle/pipeline/bindings.py)
   translates each selected region-relative span to original absolute bytes.
   [`contracts.py`](../src/ck3chronicle/pipeline/contracts.py) renders stored parts
   and ordered values; every frame's file, line and trace participates in identity.
5. **No assignment is different from lost evidence.**
   [`classifier.py`](../src/ck3chronicle/pipeline/classifier.py) preserves no-match
   explicitly. [`ReviewWriter`](../src/ck3chronicle/pipeline/review.py) retains the
   contributing original emissions and a routing manifest. Template and provisional
   assignments are both record eligible. Nothing in this path authorizes dropping
   the extra frames or salvaging only a matching prefix.

The older paragraph in `LEARNER_INFERENCE_RULES.md` saying whole file/line chains
are one PARAM and frame count is excluded from the signature describes the
superseded declaration. The dated 2026-09-24 correction in
[the model contract](LEARNER_NATIVE_MODEL_CONTRACT.md), the current published
rules, and executable gates agree on separate file/line/trace fields. That old
paragraph is not authority to restore the removed whole-chain behavior.

The [v45 applicability finding](LEARNER_RELEASE_V45_RESULTS.md#the-demonstrated-applicability-defect)
is an earlier learner admission defect: body-only wording checks let incompatible
four-frame references veto the needed one-frame comparison proposal. v45 corrected
the gate used by that check and published `b93cd68fb7b8374d173b423e`. It did not
introduce variable-length frames. Separate one/four-frame definitions are therefore
evidence of the current design, not proof of truncated or lost locations.
The release's separate wording, non-location capture and selection-tie limitations
remain open. This investigation audits location-entry accounting and observed
length coverage; it does not certify the entire model's semantic quality.

The focused native four-frame probe in
[supplement.json](../.codex-tmp/learner-script-location-stacks/verified/supplement.json)
confirmed recovery `script-error`, one complete body span `[1934609,1935110)`,
one-frame applicability **false**, four-frame applicability **true**, and no
complete match for the one-frame definition. Public matching selects the correct
four-frame definition. A deliberately isolated call to the shared **body-pattern
primitive only** does find one division for the one-frame parts: its final PARAM
would span body bytes `[186,497)`, swallowing the last three file/line entries.
That is **not an eligible assignment or an observed runtime loss**; the current
applicability gate rejects it. It demonstrates why removing the count-sensitive
gate alone, even while retaining whole-text reconstruction, is not a valid
variable-length implementation. No input, definition or matching code was changed
for this probe.

## Readable native examples

The [native appendix](../.codex-tmp/learner-script-location-stacks/verified/NATIVE_EXAMPLES.md)
shows complete native bodies, escaped exact text, selected parts with slot names,
ordered bindings and byte spans, disposition, every frame-to-slot mapping, and all
genuine no-match cases. Its [JSON companion](../.codex-tmp/learner-script-location-stacks/verified/chosen-examples.json)
retains exact machine-readable details. The complete measured stack population is
in [stack-ledger.jsonl](../.codex-tmp/learner-script-location-stacks/verified/stack-ledger.jsonl).

### Saved SQL sample 17: one entry

Native input hash `8c7eaa6319a5dd7851ed4c186a8564755b1c3eb7a9f4c90b792e2c1b5611efcf`,
emission 2978, body bytes `[527647,527840)`:

```text
 Script system error!
  Error: faith trigger [ Failed context switch ]
  Script location: file: common/decisions/RICE_khwarezm_decisions.txt line: 984 (RICE_khwarezm_worship_yazata:is_shown)
```

Native ending is `\n\r\n`; display blocks here do not encode line-ending bytes.
Selected template `0b2804538785c71278ea37e7`, status **template**, record eligible:

```text
 Script system error!
  Error: <KEY:s0> trigger [ <REASON:s1> ]
  Script location: file: <LOCATOR:s2> {line:|near line:} <LOCATOR:s3> (<PARAM:s4>)
```

| Ordered slot | Exact value | Absolute native byte span |
|---|---|---|
| s0 KEY | `faith` | `[527678,527683)` |
| s1 REASON | `Failed context switch` | `[527694,527715)` |
| s2 LOCATOR | `common/decisions/RICE_khwarezm_decisions.txt` | `[527743,527787)` |
| s3 LOCATOR | `984` | `[527794,527797)` |
| s4 PARAM | `RICE_khwarezm_worship_yazata:is_shown` | `[527799,527836)` |

The sole frame is s2/s3/s4, in that order. Layout choice `[[7,0]]` retains native
`line:`. There is no additional native location entry missing from the SQL record.

### Four-entry sibling

Native input hash `06a042029054e7f4d52f69a398d8e20126ba63b823072c469efed3923aff7249`,
emission 8147, body bytes `[1934609,1935110)`:

```text
 Script system error!
  Error: is_primary_heir_of trigger [ character (is_primary_heir_of) was null ]
  Script location: file: common/script_values/04_ep2_accolade_values.txt line: 819 (squires_bonus_martial)
    file: common/scripted_effects/00_accolades_scripted_effects.txt line: 10295 (accolade_create_squire_effect)
    file: common/on_action/accolade_on_actions.txt line: 152 (on_accolade_create_squire)
    file: common/on_action/accolade_on_actions.txt line: 142 (on_accolade_create_squire)
```

Selected `f0cd72fd7357b2cfc5c275ad`, **template**, record eligible. It has the same
trigger/REASON opening, followed by four explicit file/line/PARAM groups. Opening
bindings are s0 KEY `is_primary_heir_of`, s1 REASON
`character (is_primary_heir_of) was null`. Every subsequent binding is listed here:

| Native frame | Ordered LOCATOR / LOCATOR / PARAM slots | Exact file | Exact line | Exact trace |
|---|---|---|---|---|
| 0 | s2 / s3 / s4 | `common/script_values/04_ep2_accolade_values.txt` | `819` | `squires_bonus_martial` |
| 1 | s5 / s6 / s7 | `common/scripted_effects/00_accolades_scripted_effects.txt` | `10295` | `accolade_create_squire_effect` |
| 2 | s8 / s9 / s10 | `common/on_action/accolade_on_actions.txt` | `152` | `on_accolade_create_squire` |
| 3 | s11 / s12 / s13 | `common/on_action/accolade_on_actions.txt` | `142` | `on_accolade_create_squire` |

All four location labels choose index 0 at parts 7, 15, 23 and 31. The repeated
last filename and trace remain two entries with different lines; neither is
deduplicated. The appendix shows the full published parts and all relative spans.

### Other complete and unmatched examples

The appendix accounts for every frame in each of these additional genuine cases:

| Example | Selected definition / disposition | What it establishes |
|---|---|---|
| One-frame type comparison, log `f1b2195a…`, emission 2793 | `b93cd68fb7b8374d173b423e`, template | Native `left was 'culture_tradition', right was 'flag'`; `common/culture/traditions/roman_traditions.txt`, line `220`, trace `tradition_roman_succession:prestige`. Ordered s0 PARAM comparison, s1/s2 LOCATOR file/line, s3 PARAM trace. This definition matches 43,624 occurrences in the fresh replay. |
| Four-frame type comparison, log `10f99290…`, emission 14787 | `bd05cdbc8471ae8529ae1bc0`, template | Complete longer comparison, with all four file/line/trace triples s0–s11 retained. The one-frame applicability correction did not replace or absorb this structure. |
| File/line without parenthetical, log `05d71d15…`, emission 1693 | `4050eda5d98e351bc4121c36`, template | `remove_trait effect [ target: Not found in database class CTraitDatabase ]`, `history/characters/japanese2.txt`, line `483`. Frame is s2/s3 LOCATOR; the native text has no trace to capture. |
| Fifteen-frame insufficient-support example, log `06a04202…`, emission 18052 | `05f9f043b69ba615a1247b04`, provisional | `Could not fetch title or province from scope 'county'`; one complete candidate, all 15 frames retained. |
| Fifteen-frame `house.house_head` trigger tie | `0b34413cf6d714d7293ef7e4`, provisional | Two complete templates, deterministic tie-break, rank `[0,0,0,-5]`. Every frame is retained despite the provisional status. |
| Fifty-five-frame effect, log `8c7eaa63…`, emission 48899 | `ba83735f93b25db3565c2d73`, provisional | `appoint_court_position effect [ Employee has already hired max amount ]`. One complete candidate; all 55 ordered frames and 165 location fields are individually present. Full text and all 55 frame mappings are in the appendix. |
| Literal Unknown, log `05d71d15…`, emission 2949 | `02b0fa94768ae3ba600940d4`, provisional | Untyped trigger with intact REASON and literal `Script location: Unknown`. There is no lost file/line chain to reconstruct. |

The **four genuine failures** all have `assignment = null`, no selected parts or
bindings, and native-review disposition. Full native bodies and empty inspection
alternatives appear in the linked JSON/appendix:

| Native input / emission | Native formulation | Retained review Run |
|---|---|---|
| `8c7eaa63…` / 66048 | `Starting travel with incorrect receiver` for Anantadevi Dayal; inline file/line/trace before the debug sentence | `20260928-K2MKAF` |
| `ba6ea800…` / 33550 | Same travel-debug formulation for Ceyda Alaeddin | `20260928-35WAFX` |
| `eb2f32b8…` / 23939 | Activity participant Chaka Tzachas aborting travel during a Hunt | `20260928-WPOVDT` |
| `f5ca3538…` / 11848 | Activity participant Beorhtric aborting travel during a Grand Wedding | `20260928-RA3MJP` |

These are missing published formulations, not Script stack-length variants.
The [earlier v45 causal trace](LEARNER_RELEASE_V45_RESULTS.md#four-remaining-unmatched-occurrences)
documents rejected complete travel/activity proposals under the retained word-run
policy; this investigation did not rerun inference or change that policy. The
fresh replay independently establishes no complete selected match and exact
preservation of their 336, 308, 333 and 346 native emission bytes, respectively.

## Ordered variable-length option for owner review

This is a design proposal, not an implemented schema or a request to activate it.
Retaining v45 now avoids an unmeasured compatibility change when the measured
corpus supplies no stack-length failure to repair. A later experiment can test
whether explicit repetition generalizes to genuinely retained lengths absent from
its training set and reduces redundant definitions without changing field quality.

| Boundary | Proposed behavior and compatibility effect |
|---|---|
| Model | Add an explicit ordered repeated-frame node to the complete body's render layout. Each frame layout contains literal file/line labels and separate LOCATOR file and line slots. Native parenthetical-bearing frames additionally retain the declared PARAM interior and literal parentheses; evidenced frames without a parenthetical require their own explicit layout, not an invented empty trace. First-entry prefix, following-entry indentation, separators and final suffix remain explicit literals/layout choices. This needs a new model schema and new definition/model/package IDs; it is not a schema-5 optional literal or whole-chain PARAM. |
| Applicability and learning | Compare the declared frame grammar instead of requiring one `located-parenthetical` declaration per observed frame. Preserve source, construction, outer wording and unrelated ordered-parameter gates. Support, ambiguity and selection still need complete native evidence; repeated frames or repeated occurrences do not manufacture independent support. Review consolidation against actual fields, not just common display headings. |
| Recovery/parser | Keep one complete native diagnostic and its byte partition. No fixed length limit is needed in current recovery. Prefer recognizing repeat boundaries in shared matching over existing raw pieces. If the API instead exposes parser-owned frame ranges, that is a separately versioned/pinned parser API change requiring whole-log recovery verification. Do not reinterpret existing cross-emission title continuations as inline Script frames. |
| Matcher API | Return an ordered frame collection with repeat-node ID, zero-based frame index, selected frame layout/literal choices, and ordered typed captures. An address such as `(body, repeat-node, frame-index, slot-id)` disambiguates reused local slot names. Spans must have an explicit origin in the unchanged native body or frame; callers must not infer the origin. This requires a new matcher API, not an undocumented API-v2 result extension. |
| Complete matching | A recognized nonempty file/line chain must be consumed through the final suffix. No arbitrary finite frame cap, greedy prefix acceptance, ignored trailing frame, reordering, deduplication or capture of multiple file/line pairs in one PARAM. Ambiguity remains explicit/provisional under the selector. `Unknown` remains its own literal formulation, not an inferred empty stack. Other variants require genuine evidence and declarations. |
| Exact rendering | Walk the outer parts and repeated frame parts in stored order. Preserve every filename, numeric spelling, trace interior, delimiter, whitespace/line ending and literal-choice index. Rendering must require only stored definition and ordered bindings. Missing entries/layout data is an integrity failure. |
| Diagnostic identity | Include the repeated-node layout, entry count and order, every typed value and presence flag, and all selected literal choices. Different lengths or reordered/changed/repeated frames remain different diagnostic records. Absolute native offsets and emission timestamps remain provenance. A shared template across lengths must not collapse distinct stacks into one diagnostic. |

Changing definition structure changes IDs and can change ID-based tie outcomes.
The existing v45 fifteen-frame trigger tie is a concrete reason to measure this,
not to assume fewer templates automatically improve confidence. There is no
measured compression ratio or unseen-accuracy gain for the proposal in this task.
Grouping current templates by the text before `Script location:` is descriptive;
it does not prove they are safe to merge.

## Proposed work and dependencies

**Learner/parser/matcher owner, only after a separate decision:** specify the
repeat grammar and byte-span origin; correct superseded guidance; implement
inference, serialization, validation, applicability and complete matching together;
retain exact typed fields; publish a separately hashed candidate. Compare native
short/long stacks, literal Unknown, longest observed stacks, repeated frames,
singleton and competing definitions, ordered field values, exact rendering and
selection status. Use complete genuine logs. Any deliberately withheld-length
evaluation must state its training/evaluation membership and support assumptions.
Missing malformed/novel-length witnesses remain coverage gaps, not manufactured
requirements. Do not carry forward templates across learner identities as a
shortcut or restore the removed whole-chain declaration.

**Pipeline owner, conditional on that candidate:** review loader compatibility,
selected-only binding addresses, serializable definition/value validation,
rendering, identity and aggregation. Review SQL storage capacity and database-only
report consumption for repeated regions; do not assume JSON storage alone makes
the existing flat contract reader compatible. Version the contract if its accepted
layout changes. Determine whether physical SQL schema changes are actually needed;
if they are, follow the explicit reset rule, not migration/dual readers. Record
exact processing versions per Run under Task 07's current direction. Unsupported
contracts must fail clearly; no flattening fallback or silent reinterpretation of
old records. Existing immutable artifacts are not edited in place.

**Task 07:** continue against selected v45/API v2 and the current Error Contract.
This investigation adds no ingest stage, retention dependency, schema change,
database write or watcher integration requirement. A later repeat representation
requires its own owner-reviewed package and pipeline compatibility work.

## Verification and changed paths

Commands used (run from the repository root; choose a new ignored output directory
for a later replay because the investigation refuses to overwrite an existing one):

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.investigate_script_location_stacks --selection models/selection.json --inventory .codex-tmp/learner-release-v45/inputs-all.json --task06-inventory .codex-tmp/task06-v45/verified/inputs.json --date-inventory .codex-tmp/learner-date-key/inputs.json --sample .codex-tmp/task06-v45/sql-view/sample.json --sample-html .codex-tmp/task06-v45/sql-view/sql-diagnostic-sample.html --output .codex-tmp/learner-script-location-stacks/verified
.\.venv\Scripts\python.exe -B -m template_learning.report_script_location_stacks --results .codex-tmp/learner-script-location-stacks/verified --selection models/selection.json --task06 .codex-tmp/task06-v45/verified --sample .codex-tmp/task06-v45/sql-view/sample.json --sample-html .codex-tmp/task06-v45/sql-view/sql-diagnostic-sample.html
```

Evidence: [summary](../.codex-tmp/learner-script-location-stacks/verified/summary.json),
[supplement](../.codex-tmp/learner-script-location-stacks/verified/supplement.json),
[no-match results](../.codex-tmp/learner-script-location-stacks/verified/no-match.json),
[unparsed/recovery problems](../.codex-tmp/learner-script-location-stacks/verified/problems.json).
The summary includes per-input hashes/counts, selected resource and saved-artifact
entry/exit hashes, and the executed investigation tool hash. Native replay and
byte/field reconciliation are the requirement-derived checks; historical tests or
old outcome totals did not define expected classifications.

Source changes are this report, its link in the learner handoff, and the two
bounded investigation/reporting tools. The first reporting attempt stopped on a
tool-only duplicate `bytes` keyword while assembling its first log summary; the
corrected full run writes to `verified/`. The partial root ledger is not evidence
for the final counts. No selected artifacts, selection, pipeline code, databases,
watcher behavior, retained inputs, Git staging, commit or push were changed.
