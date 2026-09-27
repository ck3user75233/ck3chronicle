# Populated KEY agreement and adjective resistance

2026-09-26. Research only, following owner suggestions. Production inference,
the owner-approved JSON, current candidate bundles and production pin are unchanged.

## 1. Count corresponding populated KEY fields as one word match

The controlled experiment uses the same ten complete native logs, parser v1.6
and corrected v39 rules. At the final proposal comparison, each KEY or
OPTIONAL_KEY populated on both sides contributes one ordered matching marker.
Marker identity denotes the corresponding field in the same proposed template,
not its value. Permitted absence contributes neither a bonus nor a penalty.
Independent shared diagnostic wording is still required; initial discovery and
neighbor ranking are unchanged in this precise trial.

Actual native comparison:

```text
Unrecognized loc key canary_collective_noun. canary
Unrecognized loc key rhomaios_collective_noun. rhomaios
```

The proposed comparison views are both:

```text
Unrecognized | loc | key | <KEY s0 present> | <KEY s1 present>
```

Result: corrected wording-only score 1.0; score with two matching KEY markers
1.0. Across 352,317 occurrences / 7,864 contextual rows, there are zero changes
to selected templates, outcomes or captures. Both runs have 292 candidates,
291,456 full and 60,861 provisional assignments, unknown zero. Every selected
body/wrapper still reconstructs exactly.

All measured comparisons at this final stage already score 1.0 on remaining
wording. Once the same complete proposed template explains both messages, its
remaining literals agree. Adding matching fields cannot improve that score or
prove the proposal's inferred fields correct. This is a limitation of what this
final similarity check can establish, not evidence that structure is unimportant.

A preliminary variant inserted markers whenever a field was present, including
one-sided OPTIONAL_KEY presence, and let them enter neighbor ranking. It also
changed no assignments, but reduced two optional-field comparison scores. That
variant was superseded: allowed absence must remain neutral under the owner's
specific suggestion that the corresponding fields be populated on both sides.

Recommendation: regard corresponding populated fields as structural agreement,
separate from lexical diagnostic evidence. Do not activate a new final score
term without demonstrated value. A future earlier-stage comparison of already
inferred formulations could use it, but must establish field correspondence and
avoid letting newly guessed slots manufacture their own supporting evidence.

## 2. Negative adjectives as resistance to slot generalization

The old NLTK study nominated individual words from actual literal/PARAM regions,
excluding locators. POS tags alone do not establish negative meaning. This review
reuses that saved scoped survey and its native-context recommendations; it does
not run a new tokenizer, reintroduce old default literals or rerun NLTK in the
production inference path.

The earlier v36 adjective trial guarded established literals becoming PARAM.
It did not guard literal-to-KEY changes. Its zero-effect result therefore did
not test the failure now under discussion.

An advisory check over the complete thirty-log before/after evidence finds:

| Existing template | Unguarded proposal | Listed word lost | Contextual rows | Occurrences |
| --- | --- | --- | ---: | ---: |
| `Malformed token: <KEY>, near line: <LOCATOR>` | `<KEY> token: <KEY>, near line: <LOCATOR>` | Malformed | 11 | 63 |
| `Unexpected token: <KEY>, near line: <LOCATOR>` | `<KEY> token: <KEY>, near line: <LOCATOR>` | Unexpected | 63 | 4,097 |

Actual native witnesses, checked against the original file bytes:

```text
Malformed token: +10, near line: 10
Unexpected token: 100663301, near line: 23876712
```

The proposed resistance flags these 4,160 occurrences. With the current v39
established-wording safeguard active, neither loss occurs, so the adjective
check currently adds no further correction to these assignments. This was a
native evidence review, not a new adjective-enabled model build or a calibrated
soft-penalty experiment.

Existing captured content is excluded. For example, native
`audio2_fmod_sound.cpp` emits:

```text
PdxAudio2: couldn't check isPlaying channel (An invalid object handle was used.).
```

Its PARAM value `An invalid object handle was used.` stays opaque. The word
`invalid` does not challenge an independently supported field. Existing PARAM
and REASON content accounted for 265 and 164,979 excluded word-occurrence hits
respectively; these are token hits, not counts of independent learning examples.

## Recommended scope

- Flag an exact listed raw word changing from established literal wording into
  a new/enlarged KEY, OPTIONAL_KEY or PARAM outside a balanced enclosure.
- Treat the flag as evidence for retaining the existing diagnostic wording.
  More match coverage or matching slot markers do not rebut it. Concrete native
  evidence may justify a field; no arbitrary numeric resistance weight is
  recommended from this experiment.
- Exempt existing opaque fields and reduce/exempt this adjective-specific
  resistance inside a genuinely bounded region. Enclosure still does not prove
  that region is PARAM; ordinary field evidence remains necessary.
- Keep any eventual word list and policy explicit in the owner JSON. Use NLTK
  offline to nominate additions for native review, not to supply automatic
  semantic truth or unconditional default literals.

Adjectives are not a complete diagnostic-wording safeguard. `Unknown trigger`
becoming `Unknown <KEY>` retains the adjective Unknown and loses trigger; this
check alone would not flag that loss. It should not replace the existing
broader checks. No production adjective vocabulary or dependency was restored.

Artifacts are under `.codex-tmp/learner-refactor/key-word-evidence-v39/`:
`paired/` contains the exact corresponding-field trial and comparison;
`adjective-results.json` contains native wording-loss evidence; and
`research-reference.json` records the reviewed spellings, purpose and scope.
The preliminary presence-only trial is retained at the root for transparency.
