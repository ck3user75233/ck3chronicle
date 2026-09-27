# CK3 symbol wording loss across slot types — v40

Owner authorized extending the existing CK3 symbol-type loss check to KEY and
OPTIONAL_KEY, retaining PARAM coverage and complete raw-token matching.

## Status ledger

- [x] Replace the hard-coded PARAM-only filter with `target_slot_types` in the
  existing owner JSON: KEY, OPTIONAL_KEY and PARAM. Validate the declaration.
- [x] Preserve complete raw-token/phrase boundaries, first-letter case variants,
  and exclusion of all existing captures, including locators and opaque fields.
- [x] Record the actual proposed slot name and type in every wording-loss event.
  No PARAM-only report label remains in the live check.
- [x] Bump the learner to v40; do not import old model templates or change parser.
- [x] Preserve positively demonstrated enclosed KEY fields: require at least
  two distinct nonempty native values and the same enclosing pair across every
  candidate member. Record this evidence when it outweighs symbol-list loss.
  This is a general evidence exception for new KEY/OPTIONAL_KEY protection;
  existing PARAM loss behavior remains unchanged.
- [x] Build from the same ten/thirty complete native logs with parser v1.6.
- [x] Inspect native blocked proposals and before/after assignments, including
  restrictions that may retain overly specific formulations.
- [x] Verify export/capture consistency and report remaining decisions.

The reference does not establish initial literals. Only wording previously
outside the old candidate's fields is checked against a proposed replacement.
It does not scan known KEY/PARAM/REASON/LOCATOR contents and then force those
contents into diagnostic literals. No adjective vocabulary is restored here.

## Status of the two preceding discussions

| Item | Disposition |
| --- | --- |
| Exclude accepted KEY values from diagnostic comparison | Implemented in v39; remains active. |
| Award one word-equivalent match for corresponding populated KEYs | Native ten-log experiment completed, zero template/capture/outcome changes. Not enabled in production; no demonstrated benefit at the final comparison stage. OPTIONAL_KEY absence was neutral in the precise trial. |
| Negative-adjective resistance outside bounded fields | Investigated using the saved scoped NLTK survey and complete thirty-log evidence. Not implemented in production. It flags the 4,160 unguarded Unexpected/Malformed losses already prevented by v39's broader wording check. No numeric penalty has been selected or validated. |
| CK3 symbol-type protection against loss into KEY/OPTIONAL_KEY | Implemented in v40 through the existing JSON-driven mechanism; ten/thirty-log native validation completed below. |

Native experimental output is ignored under
`.codex-tmp/learner-refactor/symbol-slot-loss-v40/`. The existing model pin is
unchanged. This task does not publish a model or modify pipeline/SQL code.

## First native result and correction

The direct extension catches `trigger` and `effect` becoming KEY in the actual
`Unknown trigger` / `Unknown effect` proposals. It also blocks the previously
correct `Event '<KEY>' expected scope '<KEY>', but got '<KEY>'` formulation,
because quoted values `army` and `character` were still literal in the initial
groups. Ten logs consequently lose 317 supported assignments; the two native
event formulations remain matched provisionally. No other selected assignments
change in that direct-extension ten-log build.

Treating these quoted values as mandatory literal wording would misuse the
reference. The correction uses the existing paired-boundary mechanism and
actual distinct field values to distinguish them, not exceptions for specific
symbols or emitter sentences. The condition is declared in the same owner JSON
and reported as evidence-based allowance. Enclosure alone does not suffice.
This is an engineering response to native validation under the contextual loss
check's implementation authorization, not an owner-prescribed numeric threshold.

## Final native results

The corrected v40 builds use the exact same complete native inputs as v39.
No synthetic messages were introduced.

| Corpus | Occurrences | Templates (supported / provisional) | Supported assignments | Provisional assignments | Unknown |
| --- | ---: | ---: | ---: | ---: | ---: |
| Ten logs | 352,317 | 292 (161 / 131) | 291,456 | 60,861 | 0 |
| Thirty logs | 1,143,064 | 424 (236 / 188) | 697,680 | 445,384 | 0 |

Every selected template, capture and outcome is unchanged from v39 in both
corpora, including the original ten and added twenty separately. This closes a
specific guard gap; it does not demonstrate extra classification gains on these
inputs, because the existing general wording guard already prevented the bad
proposals. No regression remains from the first direct-extension experiment.

Actual proposals in each corpus record six symbol-loss rejections and one
allowance based on native field evidence. Readable examples:

| Existing formulations | Proposed replacement | Decision |
| --- | --- | --- |
| `Unknown trigger: <KEY>, near line: <LOCATOR>` and `Unknown effect: <KEY>, near line: <LOCATOR>` | `Unknown <KEY>: <KEY>, near line: <LOCATOR>` | Reject: loses the established words `trigger` and `effect` into KEY. Native witnesses include `Unknown trigger: adulterer, near line: 414` and `Unknown effect: hidden, near line: 9029`. |
| `Event target '<KEY>' is used but is never set. ...` and `List target '<KEY>' is used but is never set. ...` | `<KEY> target '<KEY>' is used but is never set. ...` | Reject: loses `Event` from established diagnostic wording. Native witness: `Event target 'cultureforeffect' is used but is never set. Setting it in an unused scripted trigger or effect does not count`. Ellipses in this table abbreviate the shared suffix, not parsed content. |
| `Event 'pregnancy.2102' expected scope 'character', but got 'none'` and `Event 'da_raid_social_events.0000' expected scope 'army', but got 'character'` | `Event '<KEY>' expected scope '<KEY>', but got '<KEY>'` | Allow: corresponding quoted fields have distinct native values; `army` and `character` are demonstrated contents there. |

The full native comparison checks every selected body/context capture against
the raw message. Both native-evidence exports are byte-identical to their v39
counterparts. Ten-log compact export replay additionally checked all 7,864
contextual rows and 38,007 captures with zero changed matches/outcomes.
The thirty-log bundle's parser/learner provenance validates, and its complete
424-template ID set agrees with v39. These checks establish consistency and
absence of changed results; they do not establish correctness of every retained
template.

Native scope inspection confirms `activity` does not match inside
`activity_types`; `common/scripted_effects/RICE_khwarezm_effects.txt` remains a
LOCATOR, and listed words already inside KEY, PARAM or REASON captures remain
excluded. First-letter case handling is unchanged. No optional-field inference
rule was changed: two nonempty values are required only for this particular
positive-evidence exception to the new loss check.

Research candidate revisions:

- Ten: `0fee46ee8d04f9a7d3ef9386`.
- Thirty: `56a5ae97d60f780bad24c28e`.

Evidence is under `symbol-slot-loss-v40/bounded/`: `review-10/`, `review-30/`,
`loss-decisions-10.json`, `loss-decisions-30.json` and `verification-10.json`.
The production model pin remains unchanged. Adjective-specific resistance and
the KEY agreement bonus remain unimplemented for the reasons in the status
table; neither is silently enabled by this change.
