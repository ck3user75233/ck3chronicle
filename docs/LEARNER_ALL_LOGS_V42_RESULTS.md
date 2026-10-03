# Learner v42 baseline and v43 cumulative learning

Owner-directed research, 2026-09-27. Candidates are isolated and unpromoted.
Selected package `44a0401b8adf0a2953d26705`, model `76630685c4a341ca14bf9c7c`,
remains unchanged. [Ignored evidence and scripts](../.codex-tmp/learner-all-logs-v42/)
retain native examples, manifests, timing records and failed/stopped attempts.

## Experiment and authority

The owner superseded the all-at-once comparison with batches of 10–20 logs:
establish supported templates, retain them, and focus later discovery on
cumulative unmatched and provisional evidence. The run uses **20 + 20 + 20 + 13
complete original logs**, in the inventory's SHA-256 order. Each checkpoint is
one cumulative model. No final log count must be chosen before starting.

The 73 unique retained logs include all thirty actual training inputs of the
selected model and the Task 06 review log. Membership comes from the model's
evidence map, not old inventory role labels. The 38 readable runtime session
copies duplicate retained contents. Twenty access-denied pending paths were
recorded but not inspected or counted. No log was split, manufactured or modified.

The v43 implementation was frozen before this experiment at SHA-256
`8a1d1b067008a3d776b4496209e4b36c6bb7523923b28a7081be8deae216cbcc`.
`additive-source/` and `additive/identity.json` retain code, hashes, complete paths
and batch membership. Parser v1.7, feature v4, model schema 4 and assignment v2
are unchanged. No inference rule is tuned from the 73-log experiment's results.

## Completed cumulative results

Final isolated candidate: **`28cac50bf1249077100d12d5`**, containing all 73 logs,
90,506 distinct bodies and 2,594,588 recovered occurrences. Its parent chain is
`2ce48af93bb9371e74c45ba1` (20), `6c68c8f708f381d7bc36b953` (40),
`3cb70df35de2f6f89334a438` (60), then the final 73-log revision.

| Cumulative logs | Supported/provisional definitions | Supported occurrences | Provisional occurrences | Unmatched occurrences |
|---:|---:|---:|---:|---:|
| 20 | 247 / 115 | 545,688 | 126,210 | 0 |
| 40 | 345 / 168 | 1,203,786 | 287,544 | 0 |
| 60 | 482 / 203 | 1,686,764 | 461,677 | 2 |
| 73 | 492 / 199 | 2,396,084 | 154,876 | 43,628 |

Every earlier supported definition survived. Across updates, **30 provisional
definitions became supported** and **53 fixed observations retired with explicit
supported successors**. No previously matched training evidence became unmatched
within this same-version chain: each later unmatched body was also checked
against its preceding model. The final 43,628 unmatched occurrences represent
only eight distinct bodies, explained below. These are coverage outcomes, not
semantic accuracy measurements.

| Update | Settled distinct bodies set aside | Distinct bodies open to discovery | Inference seconds | Build + write seconds |
|---|---:|---:|---:|---:|
| First 20 | 0 | 35,327 | 79.57 | 120.46 |
| Add 20, total 40 | 41,583 | 1,149 | 21.21 | 173.14 |
| Add 20, total 60 | 84,385 | 4,104 | 25.78 | 347.20 |
| Add 13, total 73 | 87,910 | 2,596 | 11.01 | 392.73 |

The four builds/writes took 1,033.53 seconds in total, with 137.57 seconds in
inference. They reused complete native recovery (746.55 seconds in the retained
73-log collection); no templates crossed learner identities. Recovery-code hashes
agree between snapshots. Settled matching, wording guards and final cumulative
evaluation now dominate update cost. At 60 logs, the localization source set aside
17,808 of 19,288 bodies; discovery handled 1,480, producing 47 retained templates
in 12.33 seconds of source processing. No source-specific rule was added.

### Comparison on the same complete 73-log evidence

| Model | Supported occurrences | Provisional occurrences | No complete match |
|---|---:|---:|---:|
| Selected v41, original 30 logs | 1,472,966 | 1,002,506 | 119,116 |
| Fresh v42, same 30 logs | 1,473,026 | 1,002,506 | 119,056 |
| Cumulative v43, 73 logs | 2,396,084 | 154,876 | 43,628 |

The date change alone gains 60 complete matches in the added-log cohort. Against
v42, v43 gains 75,430 matches and loses two (the travel-debug examples below),
for a net gain of 75,428. Seventy-four formerly supported occurrences become
provisional. All original thirty-log training occurrences still completely match.
Support-policy and training-scope changes contribute to the large status shift;
it is not evidence of an equivalent increase in discovered formulations.

All **122 Task 06 review cases / 9,153 occurrences** now match 28 selected
definitions: 118 cases / 267 occurrences supported, four cases / 8,886 occurrences
provisional (indices 1, 8, 52, 88). Eberhard case 20 captures date bytes `[6,15)`,
title `[23,34)` and the entire opaque CHARACTER_FULL_ID `[55,135)`. Case 1 retains
one REASON and literal effect/Unknown, with provisional status despite 8,880 repeats.

`comparison/summary.json` separates original30/added43 counts and status changes;
`comparison/review-122.json` preserves every stable case. All selected body and
wrapper capture values were checked against their native bytes (390,401 captures
for v43). The comparison took 241.45 seconds. `checkpoint-audit.json` records
retention, promotions, retirements, parents and exact input reconciliation.

## Additive behavior and provisional lifecycle

Previously the registry cached native recovery but rebuilt templates from all
admitted evidence at each revision. A single batch already learned each source
once; the repeated work arose when successive builds revisited cumulative inputs.
The additive path now retains definitions and passes cumulative open evidence to
the ordinary learner.

A record is settled only when every native wrapper has exactly one complete
assignment to the same supported template. Provisional, ambiguous and unmatched
records remain open. Supported contracts remain available; wrapper extensions
must cover earlier native members too. The registry continues its current
same-implementation candidate by default. Changed learner/rules/parser/threshold
require fresh learning, as does removing cumulative training evidence. There is
no special unchanged-evidence shortcut.

Batch boundaries and arrival order can affect which supported definitions settle
first; equivalence to fresh all-at-once inference is not claimed. This does not
prevent combining the evidence into one model. Log count itself is not a support
threshold, and repeated bodies in different genuine logs still count once.

Provisional definitions can become supported as distinct evidence accumulates.
Existing symbolic retirement can replace fixed KEY observations with a supported
general definition that demonstrably covers their members. Each retirement names
its predecessor, successor and reason; unexplained disappearance is rejected.
This is not a general semantic wrongness detector. Low frequency alone does not
justify deleting a provisional definition.

| Decision | Treatment of fields |
|---|---|
| Empirical support/status | Different native slot values count as distinct examples; identical repetitions do not. No independent-log threshold. |
| Learner similarity | Each recognized present field contributes one typed position, like one token. Its internal words contribute nothing individually. Unaccepted regions receive no field credit. |
| Complete runtime assignment | The shared matcher validates literals, field types/boundaries, wrappers and continuations, without the learner's similarity score. Complete provisional assignments are eligible. |

The older support counter masked LOCATOR and declared trace PARAM variation but
counted KEY, REASON, full-ID and inferred PARAM variation. This was a support
policy, not an omission of those other fields from opacity. The owner's
clarification removes that masking. The older similarity code excluded accepted
fields entirely; v43 restores their one-position contribution without admitting
their internal words.

## Protected wording and Unknown constructions

`effect` and `trigger` were already in the active wording-loss reference, which
already covered KEY, OPTIONAL_KEY and PARAM. The first additive implementation
checked new proposals against supported predecessors only. Open-pool inference
could therefore combine the prior provisional `untyped effect` with a new
`untyped trigger` into `untyped <KEY>`. Its apparent supported-coverage increase
was not an acceptable improvement.

The guard now includes provisional predecessors. Rejected unions are re-inferred
in smaller groups of complete native members, partitioned by their matches to
retained formulations, using the existing matcher, inference and loss check.
Before adding owner declarations, seven native checks passed, including separate
complete effect/trigger matches (`additive-wording-tests.log`). This demonstrates
the general correction independently of special declarations.

The owner subsequently confirmed two complete constructions in `owner_rules.json`:
literal `untyped effect` or `untyped trigger`, literal `Script location: Unknown`,
exact native leading spaces/endings and one opaque bracketed REASON. Explicit
exclusions give them precedence over the generic script envelope. The general
locator cue currently covers file/line/lines/Database, not every `location:`
value. Native verification confirms the Unknown forms capture REASON only;
other script-system formulations retain ordinary location fields.

Two-log candidate `aaae9d23a9a2fd3b85c10775` completely matches both:

| Formulation | Template ID | Empirical status/examples |
|---|---|---|
| untyped effect; location Unknown | `d9f8268f8306c6c4b5ca77a7` | provisional / 1 |
| untyped trigger; location Unknown | `02b0fa94768ae3ba600940d4` | provisional / 1 |

The effect's 8,880 occurrences in the affected log still supply one example.
Owner approval of wording does not manufacture empirical diversity. Definitions
and support facts are in `owner-rule-checks.json`. The historical 122-case
diagnosis remains in [the root-cause report](LEARNER_UNMATCHED_REVIEW_ROOT_CAUSE_RESULTS.md).

## Baseline and stopped attempt

Completed fresh v42 thirty-log candidate `88391d2199fc00464bb091e3` contains
38,573 distinct bodies / 1,143,053 occurrences and 418 templates (232 supported,
186 provisional). Training outcomes: 697,671 supported, 445,382 provisional,
0 unknown. These use the earlier support/similarity policies and are not unseen
accuracy. Model building took 425.26 seconds, including 118.31 seconds evaluation;
bundle writing took 233.51 seconds. Original collection took 239.98 seconds in
the preceding attempt; only its native recovery snapshot was reused.

That first attempt failed because date `inference_rule` metadata leaked into
executable field identity. Excluding learner-only metadata and representing
balanced delimiter pairs as the validator-required lists fixed the build without
weakening field acceptance. The failed attempt remains retained.

The fresh 73-log attempt recovered 90,506 distinct bodies but was stopped at the
owner's batch-direction change. **It produced no completed model or coverage
result.** Partial timings showed expensive regrouping of about 19,000 initial
`pdx_locstring.cpp` groups: a single-build scaling cost, separate from repeated
registry relearning. No inference change was made from that observation.
`batch-all-isolated/stopped.json` identifies this attempt. Its complete native
recovery snapshot supplies the batched experiment; no templates are imported.

## Verification and reproduction

Eight native additive checks passed in 99.24 seconds: registry continuation,
supported retention, provisional maturation, serialization, continuation counts,
version isolation, field contributions, distinct location-value support and
Unknown constructions. Four date checks passed in 38.24 seconds, including full
model construction and title-holder matches with opaque full IDs. These checks
do not establish semantic correctness of every learned template.

Native evidence is now written as compact JSON, bounded to one record during
encoding. The owning inspection reader was updated to consume JSON independently
of indentation. Reading all 60-log compact records reconciled 2,148,443
occurrences; reading the earlier indented thirty-log export reconciled 1,143,053.
This serialization correction changes no inference or matching rule.

## Unresolved evidence requiring review

Final unmatched evidence is **8 bodies / 43,628 occurrences**. All eight have
proposed supported definitions that completely match their native members, but
the additive wording guard rejects them before retention. None matched the
preceding sixty-log candidate. Details and complete-match proofs are in
`unmatched-73.json` and `unmatched-73-derivation.json`.

| Family | Bodies / occurrences | Rejected candidate | First demonstrated cause |
|---|---:|---|---|
| Script comparison, one trace frame | 4 / 43,624 | `3db1f37cb4f7356e76e701ba` | Additive guard uses incompatible four-frame reference structures |
| Travel-debug receiver/location | 2 / 2 | `9399c0e45227296406c1264f` | Existing word-run rule protects fixed Caliph/Jophé |
| Aborting activity travel | 2 / 2 | `960123704cb4d27bf3e915fc` | Existing word-run rule protects fixed Grand Tournament |

The first family exposes an **implementation defect in the new additive guard**.
It compares previous source definitions without respecting their complete
structural applicability. Previous definitions `8d93e1f93c13c1ad8f1fb7c0` and
`ca7b575df254fc1c68d4dfd6` have four `located-parenthetical` structures; the new
candidate has one. The body-only pattern can span the older messages and appears
to swallow literal `character` into PARAM, but the shared complete matcher rejects
that candidate on both reference messages at the parameter-structure gate.
The prior definitions themselves completely match those reference messages.
`wording-scope-check.log` records this contrast. This is not insufficient evidence,
a provisional-publication filter, or a reason to weaken PARAM/wording protection.
The frozen experiment was not repaired or rerun to improve this count.

At the sixty-log checkpoint, two `jomini_effect_impl.cpp` travel-debug bodies
remain unmatched. Candidate `9399c0e45227296406c1264f` was proposed as supported,
and the shared matcher demonstrates complete matches for both. It was rejected
before retention by `established-wording-to-key-run-loss`: older definition
`55453df539af3f71d887943d` retains fixed `Caliph` and `Jophé` inside the runs
`receiver is Caliph` and `default location is Jophé`. The new candidate would
capture those spellings in KEYs. This is the broader established-word-run rule,
not the explicit effect/trigger symbol-word list.

Both new members fell into the same group with no match to a retained formulation,
so the additive correction could not subdivide that rejected group and retained
no new definition for it. There is no runtime provisional-status veto or shortage
of candidate examples: the definition was explicitly rejected. Full native bodies,
candidate definition, captures and decisions are in `unmatched-60-derivation.json`.
This reveals a review question about freezing incidental observed values as
wording. Do not add Caliph/Jophé exceptions or change a rule to improve this run's
coverage. A separate general proposal would need native witnesses distinguishing
true diagnostic wording from variable values in these positions, and checks
against renewed effect/trigger or other wording loss.

The two `travel_plan.cpp` bodies likewise have valid opaque CHARACTER_FULL_ID
captures in the rejected candidate. Rejection concerns old activity wording
`Grand Tournament`, not malformed IDs. Their Grand Wedding/Hunt evidence exposes
the same incidental-value review question, with a different native formulation.

Distribution among more logs would not remove any of these rejections: the
candidates already exist, already have sufficient distinct examples, and already
completely match. Inclusion is also already established. Additional diversity or
different batch arrival order could change inference or the retained references;
no controlled native experiment isolates that counterfactual here. Do not confuse
43,624 repetitions with 43,624 independent formulations.

## Recommendations for owner review

1. **Correct additive guard applicability** in `additive_learning.py`, using the
   existing source/context/construction/parameter-structure boundaries before
   treating prior wording as a rejection witness. Preserve protection for both
   supported and provisional definitions. Verify the one-/four-frame native
   counterexample and same-formulation effect/trigger protection in a focused
   check, then start fresh state under the changed implementation identity and
   repeat the fixed batch order. This is an implementation correction, not a
   special exemption for character, culture types or this corpus.
2. **Review incidental values versus protected wording** in the existing word-run
   policy and refinement. Caliph/Jophé and Grand Tournament show how earlier
   fixed observations can block a later variable-field proposal. Any general
   change needs native field-boundary and variation evidence, including cases
   where literal diagnostic words really must survive. Do not add value-name
   exceptions, force all unmatched evidence into templates, or treat a retirement
   record as sufficient proof of coverage.
3. **Optimize remaining matching/guard work only with parity evidence.** Discovery
   is now a small part of later updates. Exact applicability indexes or reuse of
   unchanged capture calculations could reduce cost without changing inference.
   Keep the existing complete matcher authoritative and require identical
   assignments, ambiguity reporting and capture bytes before adopting an
   optimization. The 73-log run is evidence for profiling, not policy tuning.

The cross-version wording audit flags two additional contexts, not two proven
errors: one activity display becomes an empirically supported outer PARAM with
two native values and matching parentheses; `trait` becomes a quoted KEY alongside
observed `geographical_region`. These follow existing field-evidence mechanisms.
`wording-review-detail.json` preserves values and boundary assessments for review.
The activity examples both contain Grand Tour, so they do not independently
establish variation in that suffix. No broad semantic-quality claim is made.

From this checkout:

```powershell
$env:PYTHONPATH = (Resolve-Path tools).Path
$env:CK3_ADDITIVE_NATIVE_INPUTS = (Resolve-Path .codex-tmp/learner-date-key/inputs.json).Path
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_learner_additive_requirements.py -v
$env:CK3_DATE_NATIVE_INPUTS = $env:CK3_ADDITIVE_NATIVE_INPUTS
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_learner_date_requirements.py -v
$env:PYTHONPATH = (Resolve-Path .codex-tmp/learner-all-logs-v42/additive-source).Path
.\.venv\Scripts\python.exe -B .codex-tmp/learner-all-logs-v42/run_additive.py
.\.venv\Scripts\python.exe -B .codex-tmp/learner-all-logs-v42/compare.py
```

Scripts require fresh output destinations; preserve existing results on reruns.
They call the owning builder/matcher and retain all occurrence associations,
parents and transitions. Comparison separates the original thirty inputs from
the added 43 and retains the 122 stable review cases. Comparing v42 with v43
changes both training scope and owner-directed policy; it cannot isolate either.
Timings are single-run observations, not controlled benchmarks. Native checks
overlapped some initial collection/inference periods.

No production processing, watcher, production database write, publication, selection change,
commit or push occurred. The final candidate remains unselected for owner review.
