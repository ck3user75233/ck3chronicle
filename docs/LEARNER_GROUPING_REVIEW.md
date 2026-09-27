# Native candidate grouping review — 2026-09-21

The owner rejected the mixed formulations in the cumulative 73-log candidate.
This follow-up changes learner inference and matching. The selected raw parser,
default-literal reference, source boundaries and independent L1/L2 pools stay
the same.

## Corrections

The portrait source had a candidate erasing `gene template` versus `gene
accessory group`. Independent native groups already retained those phrases.
Inference now uses such evidence to split a mixed group: each alternative
needs at least two distinct native supporting messages, and every member of
the mixed group must select exactly one alternative. All members survive and
each resulting group is inferred again. The implementation has no gene-specific
word list and creates no subphrase templates.

The localization source also inferred adjacent variable fields separated only
by whitespace, such as `<OPTIONAL_KEY> <PARAM>`. When a PARAM participates and
no learned wording or punctuation establishes separate fields, inference now
uses the complete native region as one field. Numeric and locator slots are
excluded. Exact whitespace is retained in the pattern or capture.

Candidates retaining the same fixed wording and field positions are then
re-inferred from joint native support. The comparison ignores whitespace only
beside text fields; it preserves internal literal spacing and all punctuation
and default-word anchors. A merge must reproduce all its native supports and
retain the same wording. Thus different slot padding or optionality does not
automatically create another candidate for the same formulation. Different
failure wording remains distinct. Nothing is normalized in stored native text.

Finally, capture selection now searches parser boundaries directly. Native
`Mts'khet'` consists of the token `Mts'khet` and a trailing apostrophe. The
previous regex selected the internal apostrophe and then failed boundary
validation. The matcher now finds the valid capture ending before the trailing
apostrophe. It neither reparses nor modifies the token.

These are recorded generic inference heuristics and a matcher correction,
not additional owner-approved hardcoded vocabulary. All matching candidates
remain visible; no preferred-candidate suppression is introduced.

## Native comparison

The comparison rebuilds exactly the previous 73 logs, using their selected-parser
feature caches and hash-verified saved outcomes. It preserves the registry and
does not promote a model. This is an in-corpus comparison, not an unseen-log
accuracy claim.

Baseline: `9310e1af7379beb8f6cbcda4`, 2,594,601 occurrences, 90,518 distinct
messages, 133 sources. Output and full native evidence are under
`.codex-tmp/learner-refactor/tighter-wording-review/`.

The preceding intermediate run, saved under `tighter-groups-review`, split the
gene formulations and recovered all 171 unknown occurrences. It reduced
ambiguity by 414 occurrences without regressions, but still left 97,063
ambiguous localization occurrences. That finding prompted joint-support
re-inference of candidates with identical fixed wording. Its immutable revision
is `3764dc38e1339cf781cba857`; it is not the final result of this follow-up.

Final revision: `6d230eb73f03d4b738630eb4` (`source-component-consensus-v7`).

| Outcome | Baseline | Corrected |
|---|---:|---:|
| Full ordinary | 1,514,455 | 1,610,797 |
| L1+L2 | 978,148 | 978,148 |
| Ambiguous | 101,827 | 5,656 |
| Unknown | 171 | 0 |
| L1-only / partial | 0 / 0 | 0 / 0 |

96,171 ambiguous occurrences become full matches; all 171 unknown occurrences
become full matches. Every previously full or L1+L2 occurrence retains that
outcome. There are no new ambiguities or unresolved candidates in this corpus.
The final model has 895 ordinary and 1,041 component candidates.

## Inspectable changes and limits

- **Portrait source:** the mixed `Unknown <KEY> gene <KEY> <PARAM> ...`
  candidate is gone. `gene template` and `gene accessory group` retain their
  different wording. The mixed group's twelve native supports partition into
  eleven accessory-group messages and one template message; the latter remains
  literal where that support alone does not establish variation. Independent
  generic gene-template candidates remain available. Portrait ambiguities fall
  from 4,030 to 3,616.
- **Localization source:** native ` Key is missing localization: 0\r\n`
  previously matched four candidate layouts. It now matches one:
  ` Key is missing localization:<PARAM>`. Its exact PARAM capture is
  ` 0\r\n`, including its native whitespace; the JSON does not trim it to `0`.
  This is a structural match, not semantic approval of every field boundary.
  Localization ambiguities fall from 97,063 to 1,306.
- **Apostrophe:** native `Mts'khet'` now captures `Mts'khet` and retains the
  trailing apostrophe as a literal. `Qal'at al-Nisā'` similarly captures the
  complete `Qal'at al-Nisā` phrase. Neither internal apostrophe becomes a
  capture boundary.

The remaining 5,656 ambiguous occurrences are: portrait 3,616; localization
1,306; script system 667; effect implementation 48; character history 11;
artifact feature 8. For example, `Unknown cloaks gene accessory group ...`
still matches both a candidate fixing `cloaks` and one treating that position
as KEY. Localization `Aach im Gau` matches the general PARAM candidate, a
three-KEY candidate, and a candidate fixing `im`. These still need evidence-led
candidate reconciliation; they were not suppressed to improve the counts.

## Verification and artifacts

Every emitted nonempty message/component capture in the final native export
(339,119 captures over distinct evidence rows and all candidate matches) was
checked against exact UTF-8 byte spans and raw-piece boundaries. Every row's
pieces reconstruct its text; every match remains in its source family.

Two original logs were freshly parsed and evaluated: 8,723 and 3,694 messages,
with 5 and 2 ambiguities respectively, no unknowns or unresolved emissions.
Their 1,724 distinct combined message/context cases reproduce the cached
candidate matches and captures exactly. These logs belong to the accumulated
corpus; this is fresh-parser verification, not a held-out claim. Saved bundle
hashes and all current inference implementation hashes were verified.

- [Counts and all outcome transitions](../.codex-tmp/learner-refactor/tighter-wording-review/summary.json)
- [Native examples, actual pieces, captures and grouping refinements](../.codex-tmp/learner-refactor/tighter-wording-review/native-grouping-checks.json)
- [Remaining native ambiguities and competing patterns](../.codex-tmp/learner-refactor/tighter-wording-review/training-review.json)
- [Fresh original-log checks](../.codex-tmp/learner-refactor/tighter-wording-review/fresh-parse-checks.json)

Registry selections and confirmations remain unchanged. No production model
was promoted. The remaining semantic grouping questions are visible for review.
