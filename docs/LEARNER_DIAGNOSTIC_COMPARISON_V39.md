# Diagnostic wording comparison correction — v39

Owner direction: accepted identifier values must not drive template similarity.
We infer the game's diagnostic wording and variable fields from native evidence.

## Status

- [x] Confirm current defect: `learning_tokens(record, parts)` excluded PARAM
  captures but still compared KEY values, after joint inference accepted them.
- [x] Clarify removal scope: the repeated regrouping loop and coverage-driven
  absorption are gone. One sweep over original groups remains. Accepted unions
  are not reopened by that sweep. Earlier descriptions of removal were too broad.
- [x] Make every accepted slot capture opaque to diagnostic-wording comparison.
  This includes KEY, OPTIONAL_KEY and numeric fields, not just PARAM.
- [x] Use the same field-excluding view when retrieving/ranking already inferred
  groups. Retain source/construction restrictions, native field validation and
  established-wording loss checks. Empty diagnostic agreement cannot accept a union.
- [x] Record the actual remaining diagnostic tokens in each evaluated proposal.
  Remove an obsolete comment suggesting deleted coverage merging still happens.
- [x] Rebuild from the same ten and thirty complete logs with parser v1.6;
  compare against v38 without changing parser, thresholds, rules or source corpus.
- [x] Inspect native templates and captures, including the localization-key case,
  new generalizations and diagnostic-wording regressions. Report limits honestly.

This is not a repeated-loop restoration or a coverage merge. No generated model
is edited, no template is imported, and no example-specific rule is introduced.
Raw parsing and runtime matching implementations are unchanged.

## Scope limits

Initial grouping still operates before fields have been inferred. This correction
addresses comparisons where inferred fields are available; it does not claim a
complete redesign of initial discovery. Recognized location introductions still
need the broader structural-only comparison work described in
`LEARNER_PARAM_CONTEXT_PROPOSAL.md`. Variable numbers of location/trace entries
also remain a separate model-structure issue.

Native build and comparison artifacts are kept outside Git under
`.codex-tmp/learner-refactor/diagnostic-wording-v39/`.

## First native check: correction alone is insufficient

The ten-log build accepts `Unrecognized loc key <KEY>. <KEY>`, including both
canary and rhomaios. But it also exposes the existing field-evidence weakness:
`Unknown trigger` / `Unknown effect` become `Unknown <KEY>`, and `Unexpected
token` / `Malformed token` become `<KEY> token`. Successful KEY syntax is not
enough to justify deleting an already established diagnostic word.

The existing loss check only rejects replacement of multiple stable words by
multiple adjacent KEY slots. The correction being evaluated extends that check
to loss of any word within a previously stable multi-word run, where independent
non-location field variation already supported the old wording. This uses raw
word runs and observed previous fields, not adjective lists or default literals.
It is a conservative engineering acceptance rule, not an owner-supplied linguistic
definition. A constant isolated spelling such as the final `canary` is not such
a run. Its proposed variation can still be learned from the corresponding native
messages. Quotes, punctuation and existing slots interrupt the raw word run.

This can retain narrower templates when a genuine identifier is embedded in an
unquoted stable phrase. Native comparison must report that tradeoff; the check
does not claim to recognize diagnostic meaning in arbitrary English.

## Completed native results

The initial thirty-log attempt finished before the stop request took effect.
It and the ten-log correction-only build are retained as rejected research
evidence. The corrected builds are under `guarded/`, with no publication/pin change.

| Same corpus | v38 candidates | v39 candidates | v38 full / provisional | v39 full / provisional |
| --- | ---: | ---: | --- | --- |
| Ten logs | 355 | 292 | 290,694 / 61,623 | 291,456 / 60,861 |
| Thirty logs | 500 | 424 | 696,216 / 446,848 | 697,680 / 445,384 |

Unknown remains zero. In the thirty-log comparison, 445 occurrences in the
original ten and 1,019 in the added twenty move from provisional to full; none
move the other way. These are support-status changes, not an accuracy metric.
All 7,864 / 38,621 contextual rows retain exact complete body/wrapper capture
reconstruction, covering 37,261 / 183,706 body captures respectively.

The six canary/rhomaios messages now share one two-KEY template, with identical
remaining comparison words and score 1.0. Thirty logs contain 174 occurrences
of those six texts. `Unknown trigger`, `Unknown effect`, `Unexpected token` and
`Malformed token` retain their literal wording; the trial's regressions are
rejected. Event scope alternatives and missing-localization values also combine
without deleting their surrounding diagnostic wording.

Remaining quality concerns are visible in the reports: a four-location
`No previous holders` formulation changes to three KEY fields within quotes
(three native occurrences), rather than an opaque variable-length title field.
Travel receiver/name descriptions also still split into KEY fields. These are
not claimed as typing improvements. The changed guard conservatively retains
`Event target` and `List target` as separate diagnostic formulations instead of
generalizing their first word. Location/trace-count fragmentation and malformed
brace binding remain open.

Final research candidates: ten `e17e0e907a97e4e58fc7c468`, thirty
`cd5e492ff4f1b9ec5a071d4e`. The report lists every changed selected-template pair
(32 / 48 pairs) with actual captures and native provenance. The single-sweep
ablation and its demonstrated benefits/limitations are explained in
`LEARNER_SINGLE_SWEEP_NATIVE_REVIEW.md`.

Compact-export validation replays every contextual row with zero changed
matches/outcomes. The 43 / 65 displayed native examples in these two comparisons
also match their original log byte spans and file hashes. See `verification.json`.
