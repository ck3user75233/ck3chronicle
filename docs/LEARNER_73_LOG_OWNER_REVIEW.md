# Owner review of the 73-log candidate — 2026-10-04

Subsequent owner clarification: these judgments assess learner behavior and
inform code improvements; they are not approvals required for individual
templates. The learner assigns supported/provisional status. Production release
approval remains separate. Do not turn an example review into a template queue.

Production: package `68f1ae5db205ab46afef9c4d`, model
`f5cde2616f35d563118d3d32`. Fresh v54 candidate: package
`c506869af1b6c97d0bafb11e`, model `31488ccd43652c5bcd8f05cf`.

The owner directs a same-schedule incremental build **before** investigating or
correcting the detailed differences. Production used cumulative checkpoints of
20, 40, 60 and 73 logs, in retained SHA-256 inventory order. Use the unchanged
frozen v54 learner and fresh same-version state. Do not import production's
cross-version templates. The owner's subsequent explicit correction limits the
active comparison to **production versus the incremental candidate**. The
purpose of mirroring the schedule was to control build method, not commission a
fresh-versus-incremental investigation. Retain native evidence and separate
coverage from semantic quality. Earlier three-way reports are historical only.
No production activation, Run mutation or source-log changes are authorized.

The owner subsequently clarified that corpus equality is already established by
the retained content hashes. Reuse the saved input inventory and build order;
do not inspect the old model to rediscover them or conduct another input audit.

## Reviewed comparisons

| Example | Owner assessment | Required interpretation |
|---|---|---|
| 1. Different comparison types | Correct | The complete parenthetical `left was …, right was …` interior may become PARAM. |
| 2. Invalid comparison side | Correct | `left`/`right` may occupy KEY; consolidation is accepted. |
| 3. Trigger failures | Correct | Trigger names become KEY; `trigger` remains literal. |
| 4. Unset event targets | Correct | The quoted target becomes KEY. |
| 5. Untyped trigger | Possibly correct, not fully approved | Dedicated `untyped-trigger` and generic constructions have different applicability. On the inspected example, the generic template is inapplicable; this was not a preference for more literal wording. Explain coexistence and retain pending assessment. |
| 6. Invalid province | Location-layout consolidation | One versus two location entries is not a reduction of distinct diagnostic formulations. Report location-layout changes separately. |
| 7. Character history | Incorrect typing | `after death` / `from before` should be one PARAM in `has history <PARAM> birth, won't execute.`, not two KEYs. Find a reusable basis, then correct and verify. |
| 8. Emblem category | Accepted, borderline | `colored`/`textured` may share KEY; explain precisely why inference became more willing to generalize. Do not revert just because it was flagged for review. |
| 9. Flag/Variable | Accepted, borderline | Grouping is acceptable here, although these may be separate fixed engine formulations. Explain the sensitivity change. |
| 10. Unknown effect/trigger | Serious regression | `effect`/`trigger` should not have become KEY this easily. Trace the actual safeguard branch. Leading `Unknown` becoming KEY is only a hypothesis; these examples show no variation establishing it as a slot. |
| 11. Scope mismatch | Improvement | Target, expected scope and actual scope become KEYs while the diagnostic frame stays literal. |
| 12. Compare-trigger expected scope | Improvement | Trigger and expected scope become KEYs. |
| 13. Previous holders | Improvement | The complete quoted title display becomes PARAM. |
| 14. Formatting tag | Improvement | The complete quoted formatting tag becomes PARAM; preserve control characters and line endings exactly. |

Example 7 candidate: `796ad48a3e5e8f97332f4427`; example 8:
`766cfec88e63687b63c5123d`; example 9: `f7a161abe24ee04e2cd78b76`;
example 10: `afac2b20cf8aab9ca59f9a09`.

## Investigation after the incremental comparison

Trace examples 7–10 from native pieces and similarity inputs/scores through first
slot inference, regrouping/merging, applicable guards and final selection. Locate
the first step that turns disputed wording into KEY. For example 10 establish
whether the wording-loss check ran, whether the words were already slots, whether
established wording existed and whether an exception applied. Do not infer the
branch from the final template.

Default literal guidance was disabled in both compared learners. That is not
a newly established cause of their difference. Both enable the separate
diagnostic-wording-loss guard covering KEY, OPTIONAL_KEY and PARAM, with `effect`
and `trigger` in its protected vocabulary. It protects established literals
during revisions; it does not determine initial types. The location-position
Unknown rule must not be confused with leading `Unknown effect:` wording.

Audit KEY bindings across all 73 logs for prepositions and other function words,
including `after`, `before` and `from`. Provide template/slot IDs, distinct-message
and occurrence counts, and genuine contextual examples. The earlier 7,287-message
20-Run scan found `all` (1 message / 20 occurrences), `if` (15 / 23), and `this`
(7 / 90); it was not the full-corpus audit. Distinguish grammatical phrases from
valid script identifiers and offending tokens. Do not introduce an English
stop-word ban; `death` is a noun and the disputed phrase is not exclusively
function words.

After supported corrections, evaluate another disposable candidate on the same
evidence. Preserve the accepted examples, resolve examples 7 and 10, explain
sensitivity changes and retain pending example 5. Report literal/slot transfers,
semantic consolidations, location-layout-only changes, coverage and regressions
separately. The owner's assessment is mostly positive among reviewed examples,
with unresolved semantic regressions in 7 and 10; counts and coverage alone do
not authorize promotion.
