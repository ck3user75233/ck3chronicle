# What the remaining consolidation sweep does

2026-09-26. This describes `clustering.refine_region_groups`, using the corrected
v39 learner and an ablation on the same ten complete native logs. It is still a
form of regrouping. The deleted repeated loop and coverage-only absorption are
different operations; saying that all regrouping was removed was inaccurate.

## Actual mechanics

Initial grouping can separate messages before it knows which text is variable.
Each group then learns its own candidate template. The single sweep examines
whether two such groups provide evidence for a common formulation.

1. Order the original groups by distinct message count and stable template ID.
2. Consider only groups within the same source and construction/context scope.
   Rank neighbors by shared retained words and consider at most 12 neighbors,
   the current JSON setting. Accepted field values contribute no wording weight.
3. Require shared wording anchors. Pool the two groups' actual messages and run
   field inference against every member. Reject divided/unsupported results.
4. Check the proposed fields and preservation of already established wording.
   Compare the remaining case-sensitive diagnostic wording outside all accepted
   fields. Require nonempty shared wording and the existing comparison threshold.
5. If accepted, replace those two candidates with the joint candidate. Neither
   original group can merge again, and the resulting group is not reconsidered
   by this sweep. Continue once through the original list.

Other distinct operations still follow: identical executable patterns combine
their evidence, and exact fixed-KEY specializations may retire under v38 rules.
Those operations are retained in both sides of the ablation. Matching coverage
alone does not authorize pooling groups. This sweep is not winner selection.

This is a bounded repair of fragmentation from initial discovery, not a
necessary property of template learning in general. Better initial grouping
could remove the need for some of it.

## Controlled comparison

The ablation bypassed only `refine_region_groups` in the evaluation process;
production source was not given a disable flag. Both builds used the same raw
parser v1.6, owner JSON, field inference, retirement and selected-assignment code,
with the same ten complete logs and no imported templates.

| Measure | Sweep removed | Sweep enabled |
| --- | ---: | ---: |
| Active candidates | 357 | 292 |
| Supported / provisional candidates | 169 / 188 | 161 / 131 |
| Occurrences assigned to supported templates | 282,603 | 291,456 |
| Provisional occurrences | 69,714 | 60,861 |
| Unmatched occurrences | 0 | 0 |

The 8,853 outcome changes are provisional to supported. This measures the
learner's evidence status, not independently established accuracy. There are
64 changed selected-template pairs affecting 53,136 occurrences. Every selected
capture and complete body/wrapper reconstruction was checked on 7,864 contextual
rows; inference quality still requires the native examples below.

## 1. Two changing identifiers split into separate formulations

Emitter: `jomini_dynamicdescription.cpp`. Actual messages include:

```text
Unrecognized loc key canary_collective_noun. canary
Unrecognized loc key canary_name. canary
Unrecognized loc key rhomaios_collective_noun. rhomaios
Unrecognized loc key rhomaios_name. rhomaios
```

The actual two groups entering the pass each contain three distinct messages,
27 occurrences per group. Before:

```text
Unrecognized loc key <KEY>. canary
Unrecognized loc key <KEY>. rhomaios
```

After:

```text
Unrecognized loc key <KEY>. <KEY>
```

The second identifier was constant within each small group but varies across
the two. The diagnostic wording and punctuation remain identical. v39 compares
`Unrecognized | loc | key` on both sides; its score is 1.0. The previous code
included the identifiers and rejected at 0.64. Other original groups independently
converge to this same pattern; exact-duplicate consolidation then combines them.

## 2. An absent field and a populated field remained separate

Emitter: `pdx_persistent_reader.cpp`. Actual native messages:

```text
Failed to read key reference: : , near line: 10020357
Failed to read key reference: 999916_bgp_melissa: 999916_bgp_melissa, near line: 119
```

Before:

```text
Failed to read key reference: : , near line: <LOCATOR>
Failed to read key reference: <KEY>: <KEY>, near line: <LOCATOR>
```

After:

```text
Failed to read key reference: <OPTIONAL_KEY>: <OPTIONAL_KEY>, near line: <LOCATOR>
```

The empty group has 470 distinct full messages because line numbers differ;
that does not create 470 independent field examples. The populated group has
35 distinct messages. Pooling reveals absence and actual values in the same
positions. No PARAM is created. The malformed brace observation remains a
separate unresolved typing problem; this example does not claim to fix it.

## 3. A quoted field genuinely contains different raw token lengths

Emitter: `pdx_data_localize.cpp`. Actual native messages:

```text
Data error in loc string 'FERVOR_CHANGELOG_ENTRY'
Data error in loc string 'ck3ia easter_eggs_spawned host=[ROOT.GetUIName] jace=[scope:ck3ia_jace_desmond.GetUIName] aileann=[scope:ck3ia_aileann_desmond.GetUIName]'
```

Without the sweep, 24 distinct short values support `Data error in loc string
'<KEY>'`; the longer expression remains a separate literal candidate. Together:

```text
Data error in loc string '<PARAM>'
```

The quote boundaries and diagnostic wording remain outside the field. The long
expression supplies actual multi-token evidence; this is not a failed-KEY
fallback. Limitation: this ten-log corpus contains only one distinct long
expression in that union. The result is supported by observed structure, but it
does not establish every future permissible localization-expression grammar.

## 4. The same constructor was represented by singleton event messages

Emitter: `eventmanager.cpp`. The actual two initial candidates are:

```text
Event 'pregnancy.2102' expected scope 'character', but got 'none'
Event 'da_raid_social_events.0000' expected scope 'army', but got 'character'
```

There are three occurrences of the first and 314 of the second; each remains
one learning example. The sweep finds:

```text
Event '<KEY>' expected scope '<KEY>', but got '<KEY>'
```

All three quoted values vary; all diagnostic wording survives. The evidence is
two distinct native examples, not 317 independent observations.

## Limits and recommendation

The sweep does have demonstrated useful effects. Keeping it merely because it
reduces candidate count would be unjustified. The corrected comparison alone
also allowed `Unexpected token` / `Malformed token` to become `<KEY> token`.
The additional established-wording check rejects that loss, as well as the
`Unknown trigger` / `Unknown effect` generalization, in the corrected build.

UI-marked character-history fields remain poorly typed; the pass sometimes
reduces their literal fragmentation while still producing KEYs containing
formatting or separate KEYs for multi-word display content. Those are not proven
quality gains. Quote-bound PARAM changes and preservation of location fields
must be inspected separately from assignment counts.

Recommendation: retain this single evidence-checked sweep for these demonstrated
fragmentation cases, keep the repeated loop and coverage-only absorption absent,
and keep correcting initial grouping and field evidence. No result here supports
reinstating repeated broadening. Location-introduction wording still contributes
to the current comparison and remains an acknowledged limitation.

Artifacts (ignored):

- `diagnostic-wording-v39/guarded/sweep-review-10/REVIEW.html`: all 64 changes,
  original native text, old/new templates and actual captures.
- `diagnostic-wording-v39/sweep-actual-inputs.json`: the actual entering groups,
  every native member and the proposed replacement for the inspected sources.
- `diagnostic-wording-v39/ablate.py`: exact evaluation-only bypass.

All paths above are under `.codex-tmp/learner-refactor/`. No synthetic messages
or manually edited generated templates were used. All 81 displayed native
examples in this ablation report were additionally checked against their
original file hashes and exact byte spans (`ablation-byte-verification.json`).
