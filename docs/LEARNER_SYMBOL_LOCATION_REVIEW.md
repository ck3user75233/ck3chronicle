# Symbol defaults and location fields — 2026-09-21

## Owner correction implemented

A CK3 symbol type can occur in the path holding its definitions. Its occurrence
in a path does not establish that it is a symbol type. The previous expansion
incorrectly used directory categories as a proxy for type identity.

Removed from the active reference: the folder-derived expansion, directory/path
inventory, and the all/restricted vocabulary selector. Removed the comparison
runner tied to that expansion. The native slash survey no longer reads or
classifies by installed directory names.

The active symbol group contains 18 explicitly owner-supplied spellings: the
original trigger/effect/on_action/scripted type/culture/faith examples and their
listed plurals, plus event and trait. This is a bounded initial vocabulary, not
an exhaustive type inventory. Additional types need evidence identifying their
type role in definitions or documentation. Directory names are insufficient.
The requested broader-type comparison remains outstanding on that basis.

Symbol defaults accept either case of the first letter on complete parser tokens
only. Native casing stays intact. A word embedded in mod_effect, root.faith,
common/traits, or common/scripted_effects does not become a default literal.

## Generic locator recognition

Location inference does not read the symbol vocabulary to identify paths. It
uses explicit file/line/Database labels, slash-bearing values after
a colon or a complete in/file introducer, and slash-delimited filename syntax with an extension. There is no
folder or extension allowlist. Numeric ratios alone do not establish a path.

Current parser v1.2 emits every slash separately. A path is an adjacent range
of segment and slash tokens, not one raw token.

Recognized values become LOCATOR even if their spelling is shared by every
observed support. That repetition is not evidence that the path is template
wording. Complete existing parser-range boundaries determine the field; labels,
whitespace, delimiters and subsequent trace text stay outside it. Separately
labelled file and line values remain two fields; path.txt:6 remains the final segment token of
a path, with any preceding slash tokens represented separately. These are generic lexical heuristics subject to native
review, not a claim to recognize every possible path presentation.

Before the slash-boundary correction, a read-only scan covered all 352,317 message
occurrences in the same ten selected logs (7,864 exported source/context evidence
rows), finding 17,029 location positions across those rows. Four actual native
examples were re-inferred independently to verify exact LOCATOR capture bounds:

| Native presentation | LOCATOR value |
|---|---|
| Database: common/traits | common/traits |
| in file common/dynasties/00_bgp_dynasties.txt:6 | common/dynasties/00_bgp_dynasties.txt:6 |
| file: common/scripted_effects/RICE_khwarezm_effects.txt line: 166 | path and 166 as separate fields |
| in localization/english/mcr_rescue_vengeance_l_english.yml | localization/english/mcr_rescue_vengeance_l_english.yml |

Full native text, actual parser pieces, inferred parts and captures are saved in
`.codex-tmp/learner-refactor/symbol-location-review/folder-removal-checks.json`.
Those checks established field typing under v1.1 only. The current v1.2 native
verification and model results are in [the slash-boundary review](LEARNER_SLASH_BOUNDARY_REVIEW.md).

## Historical v1.1 path suffix and introducer verification

The native dynasty message is exactly:

```text
 Missing name for dynasty 999992 in file common/dynasties/00_bgp_dynasties.txt:6
```

The then-selected v1.1 parser returned the entire path as one token. That
segmentation has been replaced by v1.2: common / dynasties / 00_bgp_dynasties.txt:6
are separate adjacent tokens. The presence of the numeric suffix is a
statement about this example, not every path. Other native messages have a plain
filename followed by a separate line: field. No suffix is appended, required, or
assumed for all paths. The attached numeric suffix remains in the final segment token. LOCATOR spans
the complete path sequence, including its separate slash tokens.

The owner clarified that file <path> and in <path> themselves supply context.
The generic path cue now accepts those complete introducers without requiring
an extension or numeric suffix. Re-inference of all 99 matching native evidence
rows (963 occurrences) from the same ten logs preserved exact path values and
LOCATOR byte boundaries with no failures. Evidence is in
`.codex-tmp/learner-refactor/symbol-location-review/path-formulation-checks.json`.
These selected logs contain no extensionless paths after those introducers;
that allowed presentation has not received native-example validation here.
The separate extensionless Database: common/traits case is verified above.

## Phrase corrections retained

Internal ID, Historical ID, event ID, Event ID and due to are phrase guides.
Standalone Internal/Historical/ID/to/for are not guides. Event belongs to symbol
types. The complete saved 73-log evidence contains Internal ID in 6,726 message
occurrences, Historical ID in 2,001 and event ID in 210. The proposed underscore
and camel-case ID forms were not observed and remain inactive, recorded for
review. No native PARAM regression caused by to/for was demonstrated in the
previous ten-log experiment; removing those standalone guides restores their
eligibility without forcing them to vary.

## Experiment status

The earlier two-arm run finished on the same ten logs before this correction.
Both arms had 352,278 fully recognized or L1+L2 occurrences, 39 ambiguous
occurrences and no unknowns. The expanded arm used the rejected folder-derived
vocabulary. Its results therefore do not answer which genuine symbol-type list
is better, and are not a basis to restore that vocabulary. Saved bundles remain
historical experiment evidence only; none was promoted.

The full 73-log follow-up was stopped. No registry or production model selection
changed. The existing visualization still shows candidate
6d230eb73f03d4b738630eb4, not the current edited rules. A valid expanded type
vocabulary and renewed controlled comparison remain outstanding.
