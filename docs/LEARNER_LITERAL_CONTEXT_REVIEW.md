# Literal-context corrections and native-log rerun

**Superseded v4 experiment.** The owner corrected the implementation's claimed
authority: the example-specific PARAM override was not authorized and is now
removed. Current inference uses explicit supplied literal wording instead.
The blanket one-spelling-plus-absence split is removed for separate review.
No optional-literal architecture is supported or planned. The counts below
remain the historical comparison for this rejected interpretation.

2026-09-20. Owner authorized the ready corrections and a new learner test.
Candidate `09b423a12a029f957c700512` uses `source-component-consensus-v4` and
the unchanged raw parser `ck3-lossless-v1.1`. It is not promoted.

## Changes implemented

- Candidate retrieval is case-sensitive. Following alignment, a proposed slot
  whose values differ only by case is partitioned into separate literal forms.
  `Target` and `target` are preserved exactly rather than becoming a KEY.
- One fixed spelling plus absence no longer establishes a variable slot.
  Those formulations are retained separately. Optional slots supported by
  several different nonempty values remain eligible. This is deliberately
  conservative; a real optional literal can result in extra templates.
- This experiment incorrectly installed an example-specific PARAM override
  and attributed it to the owner. That attribution was wrong. The override
  is removed from current code; this historical candidate is not a source of
  authority for restoring it.

The [rule ledger](LEARNER_INFERENCE_RULES.md) records these decisions.
L2 learning stays independent of L1 within each source. There is no additional
nested-message investigation, preprocessing or parser change.

The comparison also includes the earlier trace-alignment correction and merge
of identical structural candidates, which had not been rebuilt into the saved
48-log baseline. Its trace improvements must not be attributed solely to the
new literal refinements.

## Complete 48-log comparison

Exactly the baseline's 48 evidence hashes were selected from validated caches
created by the selected raw parser. The corpus contains 1,940,027 occurrences,
20,572 distinct complete messages and 110 sources. Registry roles, confirmations
and current revision were not changed. The additional 25 ingested logs did not
enter this build. There are no confirmed templates in this research registry.

| Structural outcome, occurrences | Previous candidate | Revised candidate |
|---|---:|---:|
| One complete ordinary-message match | 1,290,172 | 1,294,345 |
| One complete L1/L2 composition | 446,217 | 490,589 |
| Both L1/L2 known, framing incomplete (`partial`) | 42,515 | 0 |
| L1 known, L2 missing | 7 | 0 |
| Multiple matching candidates | 160,857 | 155,093 |
| Unknown | 259 | 0 |

The previous saved exercise combined partial framing and actual missing L2
under `L1-only`. This table evaluates both candidates with the current outcome
definitions. Every occurrence remains accounted for.

Ambiguity decreased by 5,764 occurrences (3.6% of the previous ambiguous count).
It remains in about 8% of training occurrences. This is a modest reduction,
not evidence that the candidate-formation problem is solved. Ordinary candidates
increased from 492 to 568; component candidates from 957 to 961. Unsupported
candidates fell from 29 to zero. All current candidates match their supporting
native evidence; semantic correctness is a separate question.

10,308 previously ambiguous occurrences now have one complete match. Conversely,
4,478 previously single-match occurrences now have multiple matches, and 66
previously partial occurrences are now ambiguous. Exact per-message/context
transitions were checked against both saved native evidence exports.

## Actual-file replay

The original two comparison logs were also read and parsed afresh with the
candidate's bundled raw parser. Their current SHA-256 values matched the
recorded corpus hashes. They are part of training, not held-out evidence.

| Log | Messages | Ambiguous before / after | Partial before / after | Unknown before / after |
|---|---:|---:|---:|---:|
| First comparison log | 8,723 | 122 / 82 | 367 / 0 | 1 / 0 |
| Second comparison log | 3,694 | 9 / 0 | 0 / 0 | 0 / 0 |

## What remains outstanding

### Additional 25-log frozen comparison

Both candidates were matched against all 654,574 occurrences in the other 25
accumulated logs. These logs were not included in either 48-log build. This is
a development comparison, not a separately commissioned holdout claim. Across
both sets, 73 complete native logs / 2,594,601 occurrences were evaluated.

| Structural outcome, occurrences | Previous candidate | Revised candidate |
|---|---:|---:|
| One complete ordinary-message match | 210,840 | 211,937 |
| One complete L1/L2 composition | 313,881 | 327,477 |
| Partial framing | 13,978 | 239 |
| L1 known, L2 missing | 1,944 | 1,952 |
| Multiple matching candidates | 10,320 | 9,581 |
| Unknown | 103,611 | 103,388 |

87,920 of the remaining unknown occurrences are from 23 sources absent from
the 48-log training set. These are corpus-coverage gaps, not evidence that the
case changes broke inference. One exact `gene_util.cpp` message accounts for
66,311 occurrences: `Could not find template at index '1' in gene 'gene_height'`.
Another 19,001 unknown occurrences are from the previously absent `ethnicity.cpp`.
The remaining 15,468 unknown occurrences are from represented sources; these
include new formulations as well as inadequate generalization.

For example, `pdx_locstring.cpp` has the native message
`Key is missing localization: Zengibar Kalesi`. The candidate has a single-token
KEY pattern and a separate literal `Black Turbans Rebellion` formulation, not a
general phrase capture. This is a concrete remaining KEY/PARAM investigation.
Most missing-L2 occurrences are a previously unseen
`province (scope province/barony/county) was null` formulation. Remaining partial
matches have known L1/L2 but unmatched location/trace tail shapes.

The conservative corrections also lose complete recognition on 14 occurrences
that previously had one complete match: 10 now have only L1, and 4 are unknown.
These must remain visible alongside the improvements; a net reduction in
unknowns does not mean there were no regressions.

A follow-up reparsed 830 actual native messages from the affected outcome/source
groups and matched each against both candidates. It confirmed all 14 losses:
ten occurrences of `Province '<name>' already has a special building slot`
lose their L2 match; four occurrences of an Event-target `state_faith` error
become unknown. The former pattern had generalized
`Province '<KEY>' already has a <KEY> building <OPTIONAL_KEY>`. Separating the
fixed optional `slot` wording reduces the evidence in each resulting group and
can leave a province name literal. This is an observed cost of the conservative
refinement, not a resolved generalization problem. The exact messages, old
patterns, protected paths and native spans are saved in the linked regression
audit.

### Candidate reconciliation and remaining typing work

The biggest remaining issue is coexistence of broad and narrower candidates
within the same source and component. Two L2 pairs account for 147,274
ambiguous occurrences:

| Competing candidates | Occurrences |
|---|---:|
| `Wrong scope for trigger: <KEY>, expected <KEY>` and `Wrong scope for <KEY>: <KEY>, expected <KEY>` | 83,895 |
| `target character was null` and `target <OPTIONAL_KEY> was null` | 63,379 |

The broader Wrong-scope candidate has observed `effect` and `trigger` in its
first slot. The narrower candidate has additional native support with fixed
`trigger`. This is evidence to review for candidate consolidation, not proof
that all such overlaps should be resolved by choosing the broadest template.
The same problem also affects ordinary messages and trace patterns.

The new ambiguities include 3,927 occurrences matching both a specific
`Event target link 'scope' returned an unset scope` formulation and a candidate
with a KEY in the quoted position. The specific candidate came from refining
this old, much broader formulation:

```text
Error: <PARAM> target <OPTIONAL_KEY> '<KEY>' <PARAM>
```

The optional `link` position had one fixed nonempty value. Separating its
presence/absence restored literal wording, but the resulting candidate now
overlaps an independently learned Event-target candidate. This explains why
an increase in ambiguous matches need not mean the former single match had a
better understanding of the error.

Remaining work is to reconcile candidate families using their supporting native
messages, distinguishing safe consolidation from genuinely competing
interpretations. Selecting one preferred match at evaluation time would hide
the problem. General KEY/PARAM typing remains heuristic. The owner rejected
the relationship-specific override and any optional-literal expansion. The
blanket absence-based splitting experiment must be reviewed independently of
the requested explicit literal guidance.

## Evidence and reproduction

- [Comparison summary](../.codex-tmp/learner-refactor/literal-context-review/summary.json)
- [Remaining training ambiguities and actual candidates/captures](../.codex-tmp/learner-refactor/literal-context-review/training-review.json)
- [Context-sensitive transition audit](../.codex-tmp/learner-refactor/literal-context-review/transition-audit.json)
- [Fresh raw-parse comparison](../.codex-tmp/learner-refactor/literal-context-review/fresh-parse-summary.json)
- [Additional-log unknowns, partials and ambiguities](../.codex-tmp/learner-refactor/literal-context-review/additional-review.json)
- [Fresh native verification of lost recognition](../.codex-tmp/learner-refactor/literal-context-review/additional-recognition-regressions.json)
- [Immutable candidate bundle](../.codex-tmp/learner-refactor/literal-context-review/revisions/09b423a12a029f957c700512/REVIEW.md)

The reusable `template_learning.inspect_candidate_revision` command takes
`--registry`, `--baseline-bundle`, `--parser-manifest`, `--output` and optional
`--evaluate-remaining`. It calls the owning learner and evaluator, verifies
selected-parser cache hashes, and writes comparison artifacts outside Git.
