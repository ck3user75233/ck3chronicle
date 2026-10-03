# Learner investigation — why these native errors have no complete template match

Prepared for owner assignment, 2026-09-27.
Checkout: `C:/Users/nateb/Documents/ck3chronicle`.

## Objective

Systematically investigate the **122 unique message bodies representing 9,153
unmatched emissions** in the Task 06 review shard. Explain why each message has
no complete match under the selected model, whether the learner ever generated
a candidate for its formulation, whether that candidate was merged/subsumed,
retired, rejected or omitted, and whether distributing the evidence across
multiple logs would have changed discovery or the eventual matching outcome.

Identify common causes across messages and recommend targeted remedies. This is
an investigation and recommendation task, not authorization to change inference
rules, fix production code, publish a model, change selection or activate processing.
Do not assume that no runtime match means no candidate was ever discovered.

## Owner observations to investigate explicitly

Many examples contain valid opaque `CHARACTER_FULL_ID` values. In particular:

```text
Eberhard d'Orleans of d_west_franconia (Internal ID: 39530 - Historical ID 7953)
```

The owner identifies this as a perfectly formed `CHARACTER_FULL_ID`. Message 20
in the supplied list occurs twice and has the complete native body:

```text
 Date 1066.9.15. Title d_thuringia landed title holder Eberhard d'Orleans of d_west_franconia (Internal ID: 39530 - Historical ID 7953) is not alive. Hole in history discovered.
```

There are multiple instances of the readily recognizable formulation:

```text
Title <KEY> landed title holder <CHARACTER_FULL_ID> is not alive. Hole in history discovered.
```

Explain concretely why the learner/model did not handle this formulation. The
illustration above is not permission to omit the native `Date ...` prefix, change
the full-ID definition, decompose its internals or manually seed a template.
Trace recognition of the full ID, candidate grouping/inference, the date and title
regions, remaining literal wording and final complete matching separately. If
the implementation rejects this valid full ID, expose the exact faulty assumption;
do not dismiss the value as malformed because it contains an apostrophe, a compound
name or another native spelling variation. Successful field recognition alone
does not prove the entire message has a matching template.

Also investigate message 1 independently: the identical `untyped effect` error
with an invalid character scope and `Script location: Unknown` occurs **8,880
times**. Explain its complete-match failure and the influence, if any, of such
heavy repetition on learning. Do not let this one formulation obscure the other
121 distinct messages in either analysis or proposed remedies.

## Instructions and authority

Read `AGENTS.md`, `tools/template_learning/AGENTS.md`, and the opening current
sections of `docs/PROJECT_STATUS.md`, `PROJECT_PLAN.md`, `CURRENT_HANDOFF.md`.
Use `docs/DEVELOPMENT_ENVIRONMENT.md` and `BANNED_IDEAS.md`.

Read these focused boundaries:

- `docs/TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md`
- `docs/TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md`
- `docs/ERROR_CONTRACT_SPECIFICATION.md`
- `docs/LEARNER_NATIVE_MODEL_CONTRACT.md`
- `docs/LEARNER_PARSER_PIPELINE_HANDOFF.md`
- `docs/LEARNER_CONTINUATION_MODEL_STATUS.md`
- `docs/SHARED_MATCHER_API.md`

Current owner decisions and the approved contract govern over historical
L1/L2 classifications, old activation statements or retired APIs. Both final
`template` and `provisional` assignments are eligible diagnostic records.
Insufficient evidence for supported status does not by itself explain the absence
of a provisional match. Show the actual discovery/publication/selection rule.

## Evidence and baseline

Use these existing ignored files; preserve them:

| Evidence` | Checkout-relative path |
|---|---|
| Human-readable unique list | `.codex-tmp/task06/review-unique-messages/unique-messages.md` |
| Exact bodies, counts and original emission ordinals | `.codex-tmp/task06/review-unique-messages/unique-messages.json` |
| First native emission for each unique body | `.codex-tmp/task06/review-unique-messages/unique-first-occurrences.error.log` |
| Complete review payload | `.codex-tmp/task06/verified-final/generation-a/review/task06-a/20260927-4D8ATT/review.error.log` |
| Routing/provenance manifest | Same directory, `review-manifest.json` |
| Complete source-log paths and hashes | `.codex-tmp/task06/verified-final/inputs.json` |
| Predecessor 31-log inventory | `.codex-tmp/shared-matcher-pipeline-verification-20260927/inputs.json` |
| Storage verification facts | `.codex-tmp/task06/verified-final/verification.json` |

The source log SHA-256 is
`9d3622ab1b6c85cbab45d83767bb870b06c6fb9d6da50ee44f5eba3674d98cbc`.
Resolve its complete retained path from the inventory. The unique list excludes
native headers from equality, but retains exact values, continuations and body
line endings. Its 122 rows are not 122 inferred error templates. Markdown renders
control bytes as `\xNN`; use the JSON/native bytes for actual analysis, not those
display escapes as literal input. Preserve list indices as stable case references.

At Task 06 verification, the selected schema-2 package was
`44a0401b8adf0a2953d26705`, model `76630685c4a341ca14bf9c7c`, classifier v8,
contract `error-contract-v1`. Verify `models/selection.json` and actual loaded
resources rather than hardcoding this as the current selection. If selection has
changed, explain that and reproduce the recorded package separately; distinguish
its behavior from current behavior without altering either package.

This Run had 24,112 recovered occurrences: 14,959 matched and 9,153 no-match.
There were no input failures or mixed record/review emissions. Source counts for
review were: `jomini_script_system.cpp` 9,046; `landed_title_manager.cpp` 60;
`jomini_effect_impl.cpp` 29; `characterhistory.cpp` 12; other sources 6.

The continuation-model handoff says this affected log was **not trained on** by
the final thirty-log model. Treat that as a provenance lead to verify against
actual training manifests/registries, not a sufficient root-cause conclusion.
Some formulations or full-ID structures may already exist in training elsewhere.
Do not presume a separately commissioned holdout policy merely from its exclusion.

## 1. Establish what happened for every unique message

Start from the complete retained source log and the pinned parser/matcher path.
Use `load_selected_classifier()`/its package, `package.iter_units(raw)` and
`package.match(unit, inspect=True)` where applicable. Do not treat the deduplicated
extract as a new CK3 Run or substitute it for whole-log recovery context.
Recover each case's original associations using the manifest and JSON ordinals.

For each of the 122 cases, identify the earliest demonstrated cause of no-match,
any additional necessary causes, and the evidence supporting the explanation:

1. Did the exact message, or other instances of its formulation, enter the
   selected release's training evidence? Record inclusion/exclusion, actual
   occurrence counts, distinct bodies/values and independent source-log counts.
2. Was it collected and recovered as the intended complete message? Were declared
   fields recognized and kept opaque before grouping? Did any earlier filter,
   identity collapse, cache or collection choice remove or distort evidence?
3. Which candidate(s) were proposed? Show candidate IDs, definitions, native
   members and the actual inference/grouping decisions. If none was proposed,
   locate the stage/rule that prevented it. An unobserved training formulation
   must be distinguished from an observed formulation the learner failed to infer.
4. What happened during refinement, merge/subsumption, retirement, support/status
   assignment and publication? Show predecessor/successor IDs and the exact
   decision/reason. If merged into a broader template, demonstrate whether that
   surviving template retained the required structure and covers these examples.
   A related-looking template or a retirement record alone is not proof of coverage.
5. If a suitable definition reached the published model, what precisely fails at
   runtime: source/context applicability, literal layout, a field boundary/type,
   a constraint, wrapper/component completeness, or final assignment selection?
   Identify the first failing region/rule with native spans and actual symbols.
   Distinguish no structurally matching candidate from a candidate rejected later.

Follow actual call paths. Useful starting points include `full_ids.py`,
`parameter_structures.py`, `constructions.py`, `clustering.py`, `patterns.py`,
`selection_evidence.independent_support`, `selection_evidence.selection_evidence`,
`template_retirement.py`, `artifacts.py`, the publisher, and the package's shared
matching/validation/assignment code. Verify names and ownership in the current
checkout; do not infer a cause solely from a module name or historical line range.

Do not stop at generic labels such as “not enough data”, “unseen”, “too specific”,
“subsumed” or “no complete assignment”. Explain the responsible condition and show
how it produces this outcome. Missing retained research artifacts are an explicit
evidence gap, not proof that a candidate never existed. Group cases under a common
cause only after verifying that the explanation applies to every included case.

## 2. Determine whether the learner could discover these formulations

Inspect retained pre-publication candidates, merge/refinement traces and retirement
decisions where available. If required, run the existing learner unchanged with
fresh disposable state and explicit complete native training inputs. Distinguish
what the historical artifacts prove from what a present-day reconstruction shows.
Record exact learner/rules/parser identity and any reproducibility limitation.

For formulations absent from the release's training evidence, a bounded research
replay may include this complete original log alongside the established training
set to determine what is discovered. Keep that candidate isolated and unpromoted.
This answers discoverability after seeing the evidence; it is not unseen accuracy.
Do not merely add the examples and report a higher coverage number: trace the new
candidate's derivation and show whether it survives and completely matches.

For the landed-title-holder family, compare the related native members across
the existing corpus and the 30 distinct review bodies from that source. Show
whether the expected common formulation is discovered, fragmented into fixed
observations, merged into something unsuitable, lost during retirement, or present
but rejected. Demonstrate the exact full-ID span for the Eberhard case and explain
any difference between learning-time and runtime full-ID recognition.

## 3. Answer the multiple-log counterfactual precisely

For each causal family, answer the owner's question: **if these messages had been
spread across multiple logs, would their templates have been discovered?**

Separate these possibilities:

- The same exact messages and values, with only their distribution among genuinely
  distinct source logs changed.
- More distinct values/examples of the same formulation, regardless of log count.
- Inclusion of previously excluded evidence in the chosen training set.
- The same cumulative native evidence arriving in a different order or batches.

Trace which inputs actual rules use: occurrences, distinct message identities,
non-location diagnostic examples, value variation, source-log identities or other
evidence. Establish whether log count affects candidate discovery, supported versus
provisional status, retirement/publication, final selection, or none of these.
Do not equate repetition count, distinct values and independent-log support.
In particular, explain what the 8,880 identical occurrences do and do not establish.

Use existing genuine multi-log witnesses where available. Hold the mechanism and
relevant evidence constant when attributing a change to distribution rather than
to extra diversity or training inclusion. Do not manufacture CK3 logs, duplicate
one log under different identities, split a log into artificial Runs, or relabel
copies as independent evidence. Where native evidence cannot isolate this
counterfactual, give a code-derived conditional answer and state the limit.
A hypothetical calculation is not an observed native replay result.

State a supported answer for each family: distribution alone would help, would
not help, or cannot yet be determined; include the precise condition and stage.
If the algorithm has no dependence on log distribution, demonstrate that rather
than assuming multi-log evidence is necessary. If a threshold changes only status,
do not describe that as discovery of a previously nonexistent template.

## 4. Findings, themes and recommendations

Deliver a concise source-controlled report at
`docs/LEARNER_UNMATCHED_REVIEW_ROOT_CAUSE_RESULTS.md`, linking ignored detailed
evidence under a task-owned directory such as
`.codex-tmp/learner-unmatched-review-root-cause/`.

The report must include:

- A clear answer to all three questions: why no match; whether candidates existed
  or were subsumed; whether distribution across logs would change the outcome.
- A case ledger covering all 122 stable indices with occurrence counts, source,
  causal-family ID, training inclusion, candidate/retirement/published IDs where
  available, first demonstrated failure, evidence references and unresolved gaps.
- Full worked traces for the valid Eberhard full-ID/title-holder example and the
  8,880-repeat `untyped effect` example, plus representative cases for other causes.
- Common themes with counts of both unique messages and original occurrences.
  Reconcile the ledger to 122 unique bodies and 9,153 occurrences. Avoid counting
  overlapping contributing causes as disjoint totals. Separate frequency priority
  from breadth across formulations.
- A counterfactual table by causal family, distinguishing log distribution,
  evidence diversity, inclusion and arrival order, with observed versus analytical
  conclusions clearly identified.
- Targeted proposed fixes, owning component, expected affected formulations,
  potential overgeneralization or lost-coverage risks, and the native evidence
  needed to assess each proposal. Separate implementation defects from proposed
  learning-policy changes and from legitimate evidence limitations.
- Reproducible commands, exact input/candidate provenance and explicit coverage
  limits. Preserve useful unresolved cases rather than inventing certainty.

Use exact message content in ignored evidence, not large native dumps in Git.
Keep existing learner mechanisms authoritative during diagnosis: no parallel
matcher, semantic fallback, manually seeded template catalog or weakened field
rules to make examples pass. Do not target 100% classification as a requirement.
Retain current contract semantics, including opaque full IDs and provisional
record eligibility.

Run research with `.\.venv\Scripts\python.exe`. Keep registries, caches, candidates
and generated results in isolated ignored destinations; do not mutate existing
training state, immutable models, active selection, production databases or native
logs. Do not operate capture/watchers, commit or push. Preserve unrelated work.
Return the findings and recommendations for owner review before implementing
inference changes or publishing any candidate.
