# Agent Prompt 10: Fixability Ranking

Implement fixability/actionability ranking.

The ranking should consider:

```text
severity weight
+ new/regression weight
+ crash-adjacent weight
+ our-submod-winner weight
+ recently-modified weight
+ small-diff-from-predecessor weight
- upstream-only/no-override penalty
- known-noise penalty
```

Inputs:

- canonical issue records
- session deltas
- ignore state
- crash status
- source/override resolver output
- workspace/Git context where available

Outputs:

- fixability score
- recommendation
- confidence
- reason
- top files by actionability
- top issues by actionability

Acceptance criteria:

- Direct submod regressions rank highly.
- Known localization/asset noise ranks lower by default.
- Upstream-only issues do not outrank direct submod regressions unless severity demands it.
- Recommendation language is cautious.
- Tests cover ranking examples.
