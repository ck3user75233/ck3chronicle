# Single-assignment implementation ledger — 2026-09-26

Owner requested adjective removal, then clarified the purported unmatched count
was from another file and authorized template retirement/winner changes and a
native before/after report. This ledger distinguishes implementation from results.
Pipeline adaptation and SQL remain pipeline-owned.

| Step | Status | Scope / evidence |
|---|---|---|
| Remove adjective experiment | Implemented and validated as v37 | Deleted active error-word reference loading and its JSON selection, removed retired diagnostic-word defaults, removed NLTK optional dependency. Survey/ablation tools archived outside the production package. Same ten/thirty native builds have exactly the same templates and assignments as v36; 7,864 / 38,621 contextual rows compared. No adjective disable switch remains. CK3 symbol-type loss protection remains. |
| Correct misleading unmatched flag | Implemented and validated as v37 | `unmatched_complete_message` now means unknown, not every non-full result. No consumer read the old flag. Actual v36 thirty-log pool: zero unknown, 445,729 single provisional matches, 106,869 competing-template occurrences, zero ambiguous captures. |
| Retire redundant fixed-value formulations | Implemented and validated in v38 | Same source/construction/wrapper grammar; exact symbolic specialization into established KEY/OPTIONAL_KEY fields; at least two values or value-plus-absence; every narrower native member must match uniquely. Retain retired template/evidence in audit, remove from active set. No union re-inference, coverage-only absorption or PARAM expansion. Retired 37 / 100 formulations in the ten/thirty builds. |
| Correct independent support | Implemented and validated | Remove locator and declared-trace-only differences from supporting-example count. Keep actual varying identifier/character/reference observations. Occurrences never provide independent support. 166 / 1,119 previously full occurrences become provisional without losing their templates or captures. |
| Select one complete assignment | Implemented and validated | Standalone stdlib `assignment.py`, hash-covered in candidate bundle. Lexicographic candidate-local evidence: observed structural losses, unsupported fields, independent examples, then stable identity/capture ordering. Field evidence is exported, not learned by the consumer. All complete capture alternatives must be supplied; truncated witness lists raise an error. Evidence/capture ties remain provisional. Four occurrences in the ten-log build require an honest tie-break; none in the thirty-log build. |
| Inspect native before/after | Complete | Same complete ten/thirty logs and parser v1.6 isolate this change from separately delivered parser v1.7. All 7,864 / 38,621 contextual rows replayed through existing runtime matching mechanics plus the frozen selector. Every selected body/wrapper reconstructs exactly. Twenty-five exact distinct native messages in each readable review, with before templates, after winner, actual captures, evidence and provenance. |
| Consumer contract | Implemented export; adaptation pending | Selector accepts complete body/wrapper assessments and returns one template ID, ordered captures, wrapper selections and status. Literal layouts remain in model parts. Production pipeline code and model selection have not changed. Existing formal handoff will record exact delivery. |

The selector does not repair a defective candidate or claim that a deterministic
choice proves semantic correctness. Native structural-loss evidence is measured
on a template's own learning members; it is not fresh structural inference on a
new runtime message. Complete source, construction, field and wrapper eligibility
must already have been checked by the matcher.

The executable metric order/directions, wrapper contribution and retirement
field types/diversity threshold are consumed from owner_rules.json, not merely
described there. Final policy packaging reproduces every ten/thirty assignment
and retirement. Compact-export replay also passes every contextual input. The
bundled standalone selector reproduces 25 native samples from each corpus in an
isolated interpreter with no learner or pipeline imports. Evidence:
policy-packaging-verification.json, compact-validation-10/30.json and
isolated-validation-10/30.json under the review root.

The malformed brace remains a separate issue: no anomalous-identifier binding
was implemented as part of adjective removal or ordinary winner selection.

## Demonstrated results

| Complete corpus | Templates before → after | Full before → after | Provisional before → after | Unknown |
|---|---:|---:|---:|---:|
| Ten logs | 392 → 355 | 271,028 → 290,694 | 81,289 → 61,623 | 0 → 0 |
| Thirty logs | 600 → 500 | 590,466 → 696,216 | 552,598 → 446,848 | 0 → 0 |

Thirty-log changes: 106,869 provisional occurrences receive one supported
assignment; 1,119 move from full to provisional after correcting support.
563 occurrences retain genuine active competitors and use the evidence ranking;
all others have one complete candidate after retirement. These are assignment
and support results, not a measured semantic accuracy percentage.

Original-ten cohort within the thirty-log build: 19,850 provisional → full,
168 full → provisional. Added-twenty cohort: 87,019 provisional → full,
951 full → provisional. No native messages were dropped.

Representative inspected changes:

- `scope:recipient trigger` retains the established KEY; the fixed-value copy
  retires. No KEY-to-literal reversal or new template inference occurs.
- `Missing loc for name 'Abd al-Aziz' for character '1235023'` chooses the full
  name PARAM / character KEY formulation (571 independent examples) over the
  numeric VALUE alternative (12). This is candidate evidence, not a universal
  KEY-over-VALUE ordering.
- `Could not find data system function 'GetUIName' in 'ROOT.GetUIName'` selects
  the existing KEY/PARAM formulation. Its PARAM evidence includes an actual
  seven-token expression and a one-token expression; the current one-token
  capture does not invalidate an established variable-length field.
- `Fetched null province from capital_province link` keeps the same complete
  diagnostic and location/trace captures but becomes provisional: location and
  trace variants alone no longer supply extra independent diagnostic examples.

Quality limits remain visible: CK3 UI formatting/name fragments still appear in
some KEY captures. Choosing that existing template resolves competition, not
those underlying typing questions. Four ten-log cases tie on evidence between
whole qualified identifiers and literal `scope:` plus KEY; stable identity
selects a winner and its reporting status stays provisional. More data removes
those ties in the thirty-log build, without proving every template correct.

Native reviews: `.codex-tmp/learner-refactor/single-assignment-v38/review-30/REVIEW.html`
and `review-10/REVIEW.html`; machine-readable transitions, selected captures and
all change groups accompany them. Candidate revisions:
`71adca09f2d7551287987976` (ten), `8c188491a07bba594efa4159` (thirty).
No production publication or pin change; pipeline adaptation remains separate.
