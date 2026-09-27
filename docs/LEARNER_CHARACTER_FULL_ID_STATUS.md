# CHARACTER_FULL_ID — construction inventory and status

Updated: 2026-09-26. **v33 implementation and complete native-log evaluation finished; candidate ready for owner review.**

Follow-up: v34 closes the missing-parent three-KEY defect described in these
v33 results. The same ten/thirty runs change only the 63 affected assignments;
all other outcomes and captures remain unchanged. The owner's complete
regrouping comparison is also finished. See
[the follow-up ledger](LEARNER_FULL_ID_FOLLOWUP.md) for current findings and the
recommendation to retain one sweep rather than repeated reopening.

Owner follow-up: the simplified `name of [zero or one key] (Internal ID…)`
structure has now been tested against all 7,414 character-form ID occurrences.
It holds in every case: 2,671 contain one raw token after the terminal `of`, and
4,743 contain none. The approved recognition is now implemented; the inventory
and implementation results are distinguished below.

The owner directed a complete, opaque character-reference field recognized from
declared native structures before ordinary template inference. This replaces the
suggested workaround of retaining inferred ID-parenthesis fields. It is not name
recognition, a new PARAM-discovery heuristic, or a restoration of default literals.

Final owner feedback integrated: say **name**, a variable-length field; lowercase
words inside it are irrelevant to recognition once the emitter and structure
establish the field. Add **HOUSE_FULL_ID** for the observed house emitter. Both
types preserve the complete name and ID parentheses, including empty internal
values. No internal name/title/ID slots or character-entity resolution are added.

## Status ledger

| Step | Status | Evidence / remaining work |
| --- | --- | --- |
| Inventory complete native inputs | Complete | 73 distinct complete logs; hashes verified; complete-file marker counts reconcile with the raw-parser census. |
| Inspect ID endings, context and exclusions | Complete for this corpus | Two character-form endings; title/house/province counterexamples; initial, embedded, final and multiple-reference examples. |
| Propose complete-field boundaries | Approved with final simplification and HOUSE_FULL_ID addition | Variable-length name; `of [zero/one token]` for characters; emitter-restricted ID suffix; contents opaque. |
| Declare reviewed rules in existing owner_rules.json | Implemented | Two full_id definitions in the existing declared-field registry; source/context starts and endings remain JSON data. Default literals remain disabled. |
| Implement shared recognition before ordinary inference | Implemented, v33 | full_ids.py consumes raw pieces/ranges. Both types enter inference as opaque declared units before grouping or KEY/PARAM discovery. No name recognition or shadow lexer. |
| Carry field through serialization, validation and both active matching routes | Implemented and verified | Slot types and structural constraints serialized. Both routes consume the same FullIdRules code with supplied owner/model JSON. Complete ten/thirty native replays agree on all outcomes, alternatives and capture bytes. |
| Compare complete-log models, templates and actual captures | Complete | Fresh same-ten/same-thirty builds and raw-field audits passed under full-ids-v33/. Remaining diagnostic-wording defect is reported below. |
| Update existing pipeline handoff | Complete | Development interface supplement added to the existing formal reply; no separate handoff. |
| Publish/pin model | Not performed | Production v29 and parser v1.6 unchanged; new candidates are for native review. |

Implementation before/after review: `.codex-tmp/learner-refactor/full-ids-v33/REVIEW.html`.
Initial inventory review: `.codex-tmp/learner-refactor/character-full-id-inventory/REVIEW.html`.
Supporting files: `inventory.json`, `native-witnesses.jsonl`,
`annotated-examples.json`, `contexts.txt`, `inventory.py`, `review.py` there.
Captured native evidence remains ignored, outside tracked documentation.

## Evidence and counting

The available complete-log census contains 2,517,940 emissions and 2,594,601
recovered messages in 73 distinct inputs. It was produced by the currently
selected parser, `ck3-lossless-v1.6`, SHA-256
`a9ed06a6c141a184939518c0b64292b1b48fda7f09fccc9067b3ecd944bd96d6`.

This inventory reused that exhaustive raw census, verified all 73 full-file
hashes, scanned the complete file bytes for case/spacing/underscore variants of
Internal ID, and verified every one of the 4,761 distinct source/message witnesses
against its original file byte range. Its exact token/gap sequence was checked
again using the selected parser's own lexer. No replacement tokenization,
synthetic messages, model inference, or training on 73 logs was used.

There are **6,726 message occurrences with 7,768 ID-marker occurrences**:
5,725 messages contain one marker, 960 contain two, and 41 contain three.
The direct complete-file scan accounts for every marker in the recovered-message
inventory. All spellings found were `Internal ID`; no `Internal_ID`, `internalID`,
different capitalization, or broken ID-parenthesis ending was found in this
corpus. This does not establish that other game versions cannot produce them.

Counts below are field occurrences, not independent learning evidence. A message
may contribute multiple references, and multiple formats; distinct-message
columns therefore must not be added together.

| Observed ID ending | Field occurrences | Distinct source/messages | Distinct exact ID endings | Interpretation |
| --- | ---: | ---: | ---: | --- |
| `(Internal ID number)` | 4,875 | 3,392 | 3,184 | Character-form ending without historical ID. |
| `(Internal ID: number - Historical ID value)` | 2,539 | 1,465 | 1,410 | Character-form ending with historical ID; 1,516 numeric and 1,023 nonnumeric historical-ID .occurrences. One structure, not two types. |
| `(Internal ID: number - Internal Key: value)` | 337 | 100 | 77 | Title-like objects; exclude from CHARACTER_FULL_ID. |
| `(Internal ID: number - Internal Key: )` | 12 | 11 | 9 | House emitter; recognized as HOUSE_FULL_ID, including the empty internal value. |
| `(Internal ID: number)` | 5 | 3 | 2 | Provinces in the actual witnesses; exclude from the proposed character rules. |

The two character-form endings account for 7,414 field occurrences. That is an
inventory of endings, **not a claim that 7,414 complete starts are already proven
or recognized**. In particular, one malformed emitter context remains questionable.

### Sources

Includes non-character exclusions and mixed messages. Distinct means exact raw
message text within its source, not distinct character entities or templates.

| Source | Message occurrences | Distinct messages | ID occurrences |
| --- | ---: | ---: | ---: |
| activity_type.cpp | 9 | 9 | 9 |
| activity_utilities.cpp | 303 | 293 | 303 |
| character_commands.cpp | 5 | 2 | 5 |
| characterhistory.cpp | 641 | 349 | 1,076 |
| characterlocationdata.cpp | 1,335 | 1,230 | 1,335 |
| confederation.cpp | 19 | 18 | 19 |
| event_window_data.cpp | 1 | 1 | 1 |
| history.cpp | 70 | 34 | 71 |
| jomini_effect_impl.cpp | 105 | 105 | 105 |
| jomini_script_system.cpp | 3,635 | 2,379 | 4,164 |
| landed_title.cpp | 12 | 8 | 12 |
| landed_title_manager.cpp | 156 | 126 | 156 |
| neighboring_landed_title_script_lists.cpp | 79 | 69 | 79 |
| opinionmanager.cpp | 1 | 1 | 2 |
| pdx_assert.cpp | 4 | 4 | 6 |
| succession_order.cpp | 341 | 123 | 415 |
| travel_plan.cpp | 10 | 10 | 10 |

## Proposed recognition mechanics

Use **one shared outer formulation, with the observed colon/no-colon ID-label
variants and emitter-scoped starting boundaries**, declared in the existing
owner-approved JSON. The general code should interpret those declarations; no
source-specific sentence branches in Python. The earlier proposal over-specified
the contents of the ID parentheses. Historical-ID presence and the values inside
are not needed as independent recognition tests.

```text
<variable-length name> of [zero or one raw token] (Internal ID…)
```

The square brackets in that sketch mean optional presence in the recognition
structure, not native punctuation, an emitted OPTIONAL_KEY subslot, or an
optional-literal model feature. The entire reference becomes one slot.

1. Match the terminal `of`, zero or one following raw token, and the opening
   parenthesis containing the complete `Internal` / `ID` marker tokens. Both
   observed colon/no-colon label variants are valid. Use its actual matching
   closing parenthesis. The remaining contents stay opaque; do not validate ID
   values or split historical/internal values into fields.
2. Require a declared source and surrounding construction that identifies the
   complete reference's start. An ID ending alone, a nearby `for`, `of`, `:`, or
   quote does not supply that start. Confirm corresponding surrounding wording
   after the ending where the declaration uses it.
3. End immediately after the matched ID closing `)`. Preserve any outer quote,
   outer parentheses, diagnostic suffix, newline, location, and trace outside.
   Do not stop at an apostrophe within a name. Do not consume later parentheses.
4. Capture all intervening raw content, without assigning internal name,
   dynasty, title, ID or PARAM subfields. Match future references by the same
   declared structure, not by their observed spelling or capitalization.
5. If two boundary interpretations remain possible, retain uncertainty. Missing
   internal values do not invalidate a structurally recognized complete field.
   `(no character)` lacks the outer formulation and is not this slot.

The two observed ending forms are both valid examples of that shared formulation.
The source/context restrictions apply to starts. They should not be an enumeration
of effect keys, character names or title values. Reuse emitter structures rather
than introducing a rule per diagnostic sentence in the inventory table.

### Native test of the owner's simplified structure

`simplified-structure-check.json` and `structure_check.py` in the ignored inventory
directory preserve the counts and raw evidence. All 5,421 distinct character-form
field positions (7,414 occurrences) have the terminal `of` followed by zero or one
raw token before `(Internal ID…)`; there are no tail-shape exceptions. This uses
the existing parser pieces, not whitespace re-tokenization. Names can themselves
contain `of`, e.g. `Beorhtric of Gloucester of x_d_laamp_1168`; the relevant `of`
is the one immediately preceding the optional key and ID parentheses.

The emitter evidence is indeed narrower than the initial inventory emphasized:
the retained witnesses for all 1,230 distinct travel-plan-removal messages have
`characterlocationdata.cpp:151`; all 105 setup-test messages have
`jomini_effect_impl.cpp:450`. The seven distinct confederation character messages
have `confederation.cpp:590`, while the eleven house messages have
`confederation.cpp:686`. These are verified source tags on retained witnesses,
not an exhaustive per-occurrence source-line census. Source family plus its
emission structure belongs in recognition declarations; observed line numbers
are provenance, not assumed stable across game releases.

Capitalization is useful evidence but not a sufficient or universally valid
boundary rule. In the 405 parent-reference occurrences whose opening boundary is
independently visible after `Parent (`, 401 start with a capitalized raw token;
four start with `_name`:

```text
Parent (_name Tián of  (Internal ID: 23 - Historical ID qiguo_tian_020)) of An_name Lowborn of  (Internal ID: 25 - Historical ID qiguo_tian_021) is hasn't been born …
```

This is an actual `characterhistory.cpp:850` message; the complete text, raw
pieces and native provenance are retained in the check JSON. It is not a proposed
name-specific exception. Also, `Denise de la Châtre`, `Dirk van Gerulfing` and
`Beorhtric of Gloucester` have lowercase words within the name. Therefore do not
use a consecutive-capitalized-word run to determine the field start. A known
emitter position plus the shared ending delimits the variable-length name without
validating names. Capitalization may corroborate that start, not veto it.

The earlier phrase **“houses with an empty key; exclude” was misleading**. The
empty value is not the reason. The native example is:

```text
House 'Ashikaga (Internal ID: 33577602 - Internal Key: )' is not allowed to join confederation 'Tachibana Bloc (Id: 150994946)'.
```

It lacks the `name of [key]` formulation and comes from the house emitter.
No inspection of its empty internal value is needed to distinguish it. Likewise,
the observed province/title examples do not satisfy the proposed character outer
structure and emitter context; no separate object-classification subsystem is
proposed.

### Starts supported by the observed surrounding constructions

All ends in this table are the character's own ID closing parenthesis. Literal
leads/suffixes describe declared recognition context; ordinary inference still
learns the error wording around the opaque field. Counts for each actual context,
including the script-system variants, are in the HTML appendix with native text
and raw pieces. Rare one-occurrence structures are explicitly reviewable rules,
not grounds to promote a learned template from a single example.

| Source / construction | Proposed complete-reference start | Content that must remain outside |
| --- | --- | --- |
| history: reference followed by `has no faith` or `should hold at least one landed title…` | Message-body start, with those observed suffixes | The entire failure suffix, including `(barony or county)`. |
| history: `Couldn't set … as capital for … it's held by …` | First after the full capital-setting lead; second after `it's held by` following the first complete reference | Capital key and the wording joining the two fields. No global `for` rule. |
| history: `Barony … does not have a holding, but is held by …` | After that full lead | `after running history…` and subsequent explanation. |
| characterhistory: `Parent (…) of … is …` | Inside the parent's outer `(`; then after its paired outer `)` and `of` | Parent's outer pair and the whole diagnostic after the child's ID. Missing-parent `(no character)` is separate. |
| characterhistory: Spouse/Concubine `Character: … . In history for …` | After the declared Character label; separately after `In history for` | The failure explanation between them and trailing file/line. |
| characterhistory: `Character born after death or bookmark date (age …): …` | After the complete age-bearing lead | Age parentheses and trailing file/line. |
| jomini_effect_impl: existing `file: … line: … (trace):` wrapper | Diagnostic-body start after that established wrapper, with the observed character-first diagnostic suffix | Filename, line, trace and `is married…` / `is a landed herder…` / `is a herder or nomad tributary…`. No fixed filename or trace value. |
| characterlocationdata: `Removing travel plan from the character …` | After the complete lead | `owner when the travel plan…`. |
| succession_order: `Failed build succession for '…'` | After the lead and opening quote | Quotes and `due to unhandled succession order…`. |
| succession_order: `Title '…' is in the succession … for character '…'` | After the character introduction and opening quote | The preceding title reference, even though it also has Internal ID. |
| landed_title_manager: `Date … Title … landed title holder …` | After `landed title holder` in that construction | Date/title values and `is not alive. Hole in history discovered.` |
| activity_utilities: `Trying to trigger activity event '…' for character …` | After the full event/character lead | Event key and invalid-activity diagnostic. |
| travel_plan: `Activity participant …` | After that lead, with the observed aborting-travel suffix | Activity description, formatting codes and later instructions. |
| character_commands: grant-title failure with `current holder:` | After that label within this grant-title construction | Following newline and warning explanation. |
| activity_type: scope dump introduced by failed activity-option diagnostic | After line-start `Root:` | Following rich-text `(Character - …)` decoration and Saved event targets section. |
| landed_title: quoted reference followed by wrong-faith diagnostic | After message-initial quote within this source/suffix construction | Quotes, faith names and religious-head title wording. |
| confederation: `Character '…' is not allowed to join…` | After Character and opening quote | House messages and confederation `(Id: …)` are excluded. |
| neighboring_landed_title_script_lists: `… used on character '…'` | After that declaration's character introduction and opening quote | The county-level diagnostic and near-file/trace tail. |
| event_window_data: orphaned-options diagnostic `… has no valid options for '…'` | After this complete context and opening quote | Event identifier and remaining diagnostic. |
| opinionmanager: `Trying to add an obedient opinion to the character '…' targeting '…'` | Two explicit starts, after the first lead and after targeting | Opinion wording and joining quotes/label. |
| pdx_assert: employer diagnostic / title-holder diagnostic | After the complete employer lead or `currently held by` in the reviewed title-holder assertion | Assertion wording, source-function suffix, and non-character title reference. |
| jomini_script_system: outer `Error: Character '…' has no capital` | After Character and opening quote within that outer structure | has-no-capital diagnostic, Script location and trace. |

### References within script-system REASON fields

The inventory also records references **inside existing opaque REASON content**:
quoted character introductions, reason-initial references, `Scope:`, `Actor:` /
`Recipient:` / secondary labels, `with owner`, and two/three-reference sentences.
They share the two ID endings. Their native surrounding wording and counts are
visible in all script-system context buckets in the HTML, rather than hidden in
an inferred name rule.

Examples include `Trying to put character ('…') in court of someone ('…')`,
`… is not allowed to marry …`, and `Tried to make '…' a Tributary contract with
Suzerain '…', but they are already a vassal of …`.

**Recommended overlap behavior:** preserve the already declared enclosing REASON
as opaque for template comparison. Do not split it into character slots or start
learning its interior to accommodate this feature. Recognized inner boundaries
may be inspected in the inventory, but a nested capture/export interface has not
been designed or implemented here. Decide that separately if required; the full
REASON text is already preserved. The immediate model benefit is character
references in diagnostic wording outside existing opaque fields.

## Concrete native examples

The HTML has 25 selected cards, complete original messages, proposed spans and
layouts, individual captured values, source/log provenance, and expandable exact
raw token/gap ranges. It also has one full native witness with raw pieces for
each of the 86 report contexts. There are no synthetic examples. Proposed layouts
are expressly **not** new model output.

**Initial:** `Eudes Lowborn of d_knights_templar (Internal ID: 81171 - Historical ID 144612)`
is followed by `should hold at least one landed title (barony or county) but doesn't has any:`.
The proposed field ends before `should`; the later parentheses stay diagnostic.

Its actual raw pieces, with `gap` denoting an original whitespace piece, are:

```text
"Eudes" | gap(" ") | "Lowborn" | gap(" ") | "of" | gap(" ") |
"d_knights_templar" | gap(" ") | "(" | "Internal" | gap(" ") |
"ID" | ":" | gap(" ") | "81171" | gap(" ") | "-" | gap(" ") |
"Historical" | gap(" ") | "ID" | gap(" ") | "144612" | ")"
```

**Embedded:** `Denise de la Châtre of  (Internal ID: 91375 - Historical ID 3034322)`
would become one field. The two spaces after `of` remain inside it. Both the
preceding trace and following `is married but not an adult!` remain outside.

**Multiple:** The owner's exact Barcelona example was verified in a native log
from `history.cpp` (one occurrence). Proposed layout:

```text
Couldn't set c_barcelona as capital for <CHARACTER_FULL_ID> it's held by <CHARACTER_FULL_ID>
```

The first capture is the complete Alfons reference; the second is the complete
Berenguer reference. The unchanged `c_barcelona` is shown literally here to
isolate the proposed character fields; ordinary inference determines its slot.

**No historical ID:** `A_Ha Ssy Hxa of  (Internal ID 16894909)` appears in the
travel-plan-removal diagnostic. Raw ID-ending pieces are:
`"(" | "Internal" | gap(" ") | "ID" | gap(" ") | "16894909" | ")"`.

**Must remain outside:** In one assertion, `Athlone (Internal ID: 662 - Internal Key: c_athlone)`
is the title and `MA_el-Sechnaill Úa Máoilsheáchlainn of k_ireland (Internal ID: 47002 - Historical ID 131505)`
is its holder. Only the second is proposed as CHARACTER_FULL_ID.

## Remaining uncertainties and review decisions

- `remove_confederation_member` has eight occurrences with unfilled `{}`
  placeholders and wording `because it's a house-based '…'` before a
  character-form description. Recommend leaving this context unsupported
  initially rather than using its nearest quote as authority.
- Names can be empty: native text includes `Parent ( Lowborn of …)` and
  message-initial ` Lowborn of …`. Leading whitespace can combine presentation
  spacing with an empty-name position in one raw gap. No name-validity check
  should reject it, and no code should split/trim that gap to invent a cleaner
  name boundary. The implementation keeps the entire introductory gap outside the field and
  starts at the first name token. It retains every gap byte, and internal gaps
  stay in the capture. No whitespace run is split or normalized.
- Scope descriptions sometimes append control bytes and `(Character - number)`
  after the ID parentheses. Recommend ending this field at the requested ID `)`;
  the decoration is separate. Rich-text references without Internal ID are not
  covered by these two constructions.
- `(no character)` and numeric-only travel-debug `(302829, Rüyan)` are not
  CHARACTER_FULL_ID under this proposal. This does not resolve every earlier
  enclosed-field regression.
- The quoted apostrophe example `Ari_ie Ari'ie-ryū …` shows why quote searching
  alone is insufficient. Declared opening context plus the ID ending is needed.
- The inventory itself changed no model. The authorized v33 implementation and
  fresh-run results are recorded in the status ledger and validation section.

The approved structures and boundary conventions are now encoded in the existing
owner JSON and consumed by one shared implementation. Publication remains a
separate step; the existing production selection is unchanged.

## v33 native implementation results

Fresh builds used exactly the same ten and thirty complete inputs as v32, with
verified hashes and no template imports. Candidate revisions:
ten `58d4a838c87f78ab2dfa26c1`; thirty `c5e23dbdc604f575dfd932b3`.
Readable actual templates/captures are in
`.codex-tmp/learner-refactor/full-ids-v33/REVIEW.html`; all changed assignment
groups are expandable there. JSON evidence and complete build/replay scripts
remain in that ignored directory.

| Corpus | Templates v32 → v33 | Supported templates | Full outcomes | Provisional outcomes | Unknown |
| --- | ---: | ---: | ---: | ---: | ---: |
| Same ten, 352,317 messages | 331 → 310 | 174 → 167 | 290,789 → 290,864 | 61,528 → 61,453 | 0 → 0 |
| Same thirty, 1,143,064 messages | 479 → 455 | 265 → 257 | 697,258 → 697,337 | 445,806 → 445,727 | 0 → 0 |

No full-to-provisional or full-to-unknown transitions occurred. In the thirty-log
comparison, the original-ten cohort has 76 provisional-to-full transitions; the
added-twenty cohort has three. These are comparisons of v32 and v33 trained on
the same thirty logs, not a claim that adding twenty logs improves every template.

The ten-log comparison changes 520 contextual rows / 541 occurrences; thirty
changes 907 / 1,033. All changed rows contain a newly recognized full-ID field.
The declared field positions in the complete thirty-log evidence are 1,188
CHARACTER_FULL_ID occurrences and two HOUSE_FULL_ID occurrences. Every accepted
match captures the exact recognized spans. The 38,621 contextual-row audit also
confirms that these interiors are excluded before diagnostic grouping, rather
than merely hidden in a display. Ten-log counts are 696 and one respectively.

Concrete improvements:

- Denise and Teresa now share `file: <LOCATOR> line: <LOCATOR> (<PARAM>):
  <CHARACTER_FULL_ID> is married but not an adult!`. The full name and ID
  parentheses are captured together; the trace and failure wording stay outside.
- `Removing travel plan from the character <CHARACTER_FULL_ID> owner when the
  travel plan is not ending normally.` replaces fragmented name/key/ID variants.
- `House '<HOUSE_FULL_ID>' is not allowed to join confederation '<KEY> Bloc
  (<PARAM>)'.` captures the complete house name and ID parentheses, preserving
  empty Internal Key contents. Confederation details remain outside the field.
- The Barcelona witness captures two distinct complete references and preserves
  `it's held by`. It remains provisional because the known field structure does
  not manufacture a second independent diagnostic learning example.
- Ordinary parent-history messages retain `hasn't been born`, `the wrong gender`
  and the age-based wording around their complete character fields.

Important remaining defect: **61 formerly competing parent-history occurrences
now produce one full match whose diagnostic still says `is <KEY> <KEY> <KEY>`.**
The previous broad missing-parent formulation survives; the alternative whose
first PARAM accepted `(no character)` no longer overlaps it once the actual
parent-reference structure is explicit. The child capture is corrected, but
the surviving diagnostic formulation remains wrong. Thus 61 of the 79
provisional-to-full changes in thirty logs are not demonstrated diagnostic-quality
gains. This work neither fixes nor conceals the outstanding merge/wording issue.

Other limitations remain visible: title/place names and formatted activity names
outside the new fields still undergo ordinary inference; numeric-only travel
debug IDs are not these structures. In the wider 73-log recognition inventory,
3,666 character fields and all twelve house fields are recognized outside
REASON. Another 4,002 Internal ID markers are already inside opaque REASON
content and stay there. The 88 remaining markers comprise 85 non-character
title/province markers and three character markers in two truncated script
messages without an applicable complete declared context. No new truncation or
fallback rule was added.

Both active pipeline replays completed over every message with identical
outcomes, competing candidates, captures and exact original file bytes: 352,317
messages in ten logs and 1,143,064 in thirty. Exact emission reconstruction also
passed for every input. Replay durations were 119.1 and 667.3 seconds respectively.
Evidence is in `pipeline-replay-10.json` and `pipeline-replay-30.json` beside the
readable review. Candidate serialization and strict model/rule validation pass,
and the existing published v29 selection still loads unchanged.
The shared raw parser, production model pin, SQL and ingestion remain unchanged.
