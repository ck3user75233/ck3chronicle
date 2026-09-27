# Single-assignment selection: recommendation and native evidence

**Implementation update, 2026-09-26:** v38 now implements exact fixed-KEY
specialization retirement and a hash-covered standalone winner selector.
Complete native ten/thirty comparisons and remaining consumer work are recorded
in [LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md](LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md).
The proposal/status descriptions below are historical checkpoints.

## v36 follow-up: redundant formulations before winner selection

2026-09-26. This is a proposed correction, not an implemented retirement pass.
The older published-model replay below is still valid for that immutable model;
it does not describe the new v36 development candidate's overlaps.

The native `scope:recipient trigger` example has both a generic KEY formulation
and a formulation retaining that exact value. Both are currently labelled
supported. The narrow group's three native messages differ in location and
trace; the generic formulation has 67 observed KEY values. Thus the outstanding
correction is not limited to candidates labelled provisional. See the saved
no-coverage-v36/OVERLAP_MECHANICS.md for the original groups and code path.

Retire a narrower active formulation when it has the same source, construction,
surrounding diagnostic literals and corresponding field constraints, and its
only differences are fixed observations inside independently established KEY
fields. Every native member must retain one complete assignment under the
unchanged general template. Keep its evidence/provenance and a supersession
record, without retaining a competing template. Do not re-infer a broader union,
enlarge PARAMs, erase diagnostic wording, or use complete-match coverage alone
as justification. New contradictory observations can still reopen a field.

This preserves learned fields when a subgroup happens to have one value. It
does not discard uncovered provisional formulations, import conclusions across
learner versions, or implement the separate production winner policy below.
Trace-only variation must not be mistaken for identifier-field support.

2026-09-25. Investigation/proposal, not an implemented selection policy.
Selected model remains `0a61f6c93657948e0ca20b35`, learner v29, parser v1.6.
This addresses the selection investigation in LEARNER_SINGLE_ASSIGNMENT_PROMPT.md;
it does not complete that prompt's implementation/publication deliverables.

## Recommendation

Owner correction: **select exactly one winner when provisional candidates match**.
Competition or an evidence tie must not turn matching messages into unknowns.
Use an ordered, deterministic ranking of complete candidate assignments. The
winner remains provisional; selecting it is not confirmation or promotion.

Keep two decisions separate: **which complete assignment was selected**, and
**whether that template is supported or provisional**. This review concerns
competition between provisional candidates, not hypothetical supported-template
collisions or new reporting statuses. Unknown means no eligible complete match.

Recommend ordered comparisons rather than one weighted similarity score. Do not
introduce an uncalibrated percentage confidence or a blanket KEY-over-PARAM,
longest-literal, or most-occurrences rule. A stable ID-based tie-break is acceptable
only after the substantive comparisons: it guarantees one result, not superiority.

## Current native audit

Replayed all **91937 distinct contextual inputs**, representing **2594601 messages
from 73 complete logs**, through the current immutable model's runtime matching
mechanics. The inputs and wrapper contexts are those saved by the earlier full-log
learner/runtime comparison. Original message/context spans were checked against
their hash-verified files; hashes of all 73 complete input files were rechecked.
This replay uses saved pinned-parser pieces, not another lexer or invented input.

| Outcome | Distinct contextual inputs | Occurrences |
|---|---:|---:|
| Unique supported match | 64810 | 1359947 |
| Unique provisional match | 653 | 761401 |
| No matching template | 26474 | 473253 |
| Competing templates or ambiguous complete captures | 0 | 0 |

The broader corpus includes 63 logs outside the ten training logs. These are
previously inspected research logs, not a blind sample or accuracy benchmark.
Provisional does not mean competing in this corpus. Unknowns are coverage results,
not occasions to choose the closest nonmatching template.

Evidence: [current replay](../.codex-tmp/learner-refactor/single-assignment-review/current-replay.json),
[all input hashes](../.codex-tmp/learner-refactor/single-assignment-review/input-hashes.json).

## Practical selection mechanics to implement

1. **Enumerate complete eligible assignments.** Keep existing source, construction,
   wrapper, raw-boundary, literal and slot-constraint checks. Consider all complete
   capture alternatives. Similarity is useful during learning; it must not turn a
   partial template match into a complete assignment at runtime.
2. **First comparison: structural fidelity.** Prefer fewer missed or absorbed
   independently recognized LOCATOR fields; then fewer violations of declared
   PARAM/REASON envelopes, such as literalizing their interiors or crossing their
   boundaries. These are structural comparisons, not extra similarity points
   for words inside a trace, filenames or reason text. Use existing model-backed
   recognizers, never example-specific branches or a second inline parser.
3. **Second comparison: field evidence.** Prefer fewer disputed slot assignments
   lacking positive candidate-local type/boundary evidence. The learner exports
   this evidence; runtime must not learn types anew. An identifier-shaped current
   value does not defeat a positively supported PARAM, and one present spelling
   plus absence remains valid OPTIONAL_KEY. A documented KEY-failure/PARAM fallback
   has weaker evidence than an independently justified identifier field. Missing
   evidence must be explicit, not assumed to mean zero defects.
4. **Third comparison: independent support.** Prefer the larger number of distinct
   complete diagnostic examples supporting that formulation, after removing
   repetitions and locator-only/declared-trace-only differences. Evidence must
   come from learning complete same-source messages, not from a counter that
   increments whenever runtime happens to choose the candidate. Raw occurrence
   counts and total literal characters receive no ranking weight. Greater log
   spread may be reported but is not an independent-observation guarantee.
5. **Final comparison: stable tie-break.** Among candidates tied on substantive
   evidence, select by stable template identity; within that template, select by
   a canonical ordering of complete binding assignments. The exact canonical
   key must be versioned and independent of enumeration/cache/input order.
   Record that the choice was tie-broken in research/debug provenance; return
   one ordinary provisional assignment to production. It is not a confidence
   claim, an unknown result or an additional match-status tier.

These comparisons form one total ordering: the first difference decides. A
candidate winning an earlier comparison is not displaced by many repeated
occurrences at a later comparison. If every eligible candidate has weaknesses,
select the best available by this ordering and keep the weaknesses visible to
the learner. Do not repair templates or alter captures inside the selector.

The ordering is a proposed engineering policy to evaluate, not a demonstrated
accuracy guarantee or an implemented production algorithm. Its structural and
field-evidence metrics should be explicit in the owner-rule JSON. The final
tie-break deliberately guarantees determinism where evidence cannot identify
which candidate is semantically better.

## Real multi-match examples

No current collisions were found. The examples below are **actual saved competing
provisional candidates from learner v16**, candidate `a5f3ace2fd908c6250ac7edd`.
We inspected saved outputs, verified original native bytes, and ran the current
model on those same messages. No old inference code was revived. Suggested choices
are policy illustrations, not a measured replay of an implemented new selector.

### A. Memorized expression versus variable expression

Native message, `pdx_data_factory.cpp`:

```text
Failed converting statement for 'GetTitleByKey('c_siracusa').GetHolder.GetFaith.HouseOfWorship'
```

The two real candidates were `Failed converting statement for '<PARAM>'` and the
entire native sentence as literal text. The PARAM candidate had 6 distinct native
members /39 occurrences; the memorized expression had 1 /12.

**Recommendation:** prefer the PARAM interpretation when its boundary/variation
evidence is validated across the comparable expressions. The six versus one
counts alone are not sufficient: the important distinction is variable content
in the same bounded expression position. A longest-literal rule chooses the
memorized exception. The current model now independently yields the PARAM form
as one supported match.

### B. KEY versus PARAM in the same two ranges

Native message, `pdx_persistent_reader.cpp`:

```text
Failed to read key reference: always_bce_cadet_branch: always_bce_cadet_branch, near line: 253
```

Real competitors:

```text
Failed to read key reference: <PARAM>: <PARAM>, near line: <LOCATOR>
Failed to read key reference: <KEY>: <KEY>, near line: <LOCATOR>
```

The PARAM candidate had **502 distinct messages /8317 occurrences**; the KEY
candidate had **4 /28**. Both captured the same ranges. The PARAM field evidence
contains only token counts 0 and 1, including the known closing-brace outlier:
this was the old KEY-failure/PARAM fallback defect. Equal lengths are not by
themselves proof against PARAM; there was no positive phrase evidence to justify
this fallback interpretation.

**Recommendation:** favor the justified identifier interpretation, after excluding
the unsupported fallback. A frequency rule chooses the defective candidate.
This is not a universal KEY-over-PARAM rule. Current output uses OPTIONAL_KEY for
both positions, accommodating actual absence, with one supported complete match.

### C. Choose the trace candidate that preserves the locations

Native failure wording, `jomini_script_system.cpp`:

```text
Script system error!
  Error: Event target link 'scope' returned an unset scope
```

The complete message has five file/line/parenthetical frames, printed in full in
the linked examples. One candidate froze all five trace interiors as literals
(2 distinct members /2 occurrences). Its competitor captured one PARAM from
inside the first parenthesis through four subsequent file/line frames
(155 members /3198 occurrences).

**Recommended winner:** the first candidate, preserving all ten LOCATORs, beats
the second, which preserves only two and absorbs eight inside PARAM. This follows
the first structural comparison before frequency or trace-word matching. Its
literalized trace interiors remain a documented inference weakness; the selection
does not claim the template is perfect or promote it. The newer model fixes both
weaknesses: ten LOCATORs and five separate opaque PARAM interiors. Ranking chooses
among available candidates; inference can subsequently produce a better one.

### D. A weaker evidence-based choice and an existing quality limit

The verified character-history message beginning `Parent (Arnaldo Lowborn of ...`
also had two provisional candidates: one fixed `Lowborn` with an OPTIONAL_KEY
before it; another captured both name components as KEYs. If the structural and
type-evidence comparisons tie, the 23-example candidate wins over the four-example
candidate after independent-example deduplication. This is the best available
provisional choice, not proof that either formulation is correct. The single
present optional name plus absence is legitimate OPTIONAL_KEY evidence; it is
not grounds for reinstating the rejected minimum-present-variation rule.

Current output recognizes the outer parenthesized description as PARAM, but
still captures `the`, `wrong`, `gender` as three KEYs after `is`. This is a separate
existing semantic-inference concern. The absence of competing matches does not
establish correct inference. No fix to that template was attempted in this review.

**Full native text, actual alternatives, raw pieces, current outputs, source tags,
hashes and file spans:** [readable examples](../.codex-tmp/learner-refactor/single-assignment-review/EXAMPLES.md).

## How the best candidate emerges across logs

Keep inference and evidence accumulation in the learner. The runtime should make
the same decision for the same input and immutable release; it should not learn
or change ranking while ingesting a Run.

For each new log, record assignments using the previous model before using that
log to revise candidate definitions. Inspect how unchanged boundaries and types
handle genuinely new values. Retain both confirming observations and contrary
evidence. Deduplicate repeated complete formulations; locator-only changes and
bursts do not establish new template distinctions. Spread across logs is useful
provenance, not proof that logs or observations are statistically independent.

Do not count a disputed message's provisional winner as ground truth supporting
that same winner. A new independent formulation, native contradiction, or owner
adjudication can settle a disputed interpretation; repetition of the selection
cannot. Reconsider competing candidates when new evidence challenges the earlier
boundary/type interpretation, and publish changed preferences in a new revision.

This predict-before-learning discipline is standard in incremental evaluation;
River documents this ordering in its [official explanation](https://riverml.xyz/0.14.0/examples/the-art-of-using-pipelines/).
Here it would measure future candidate stability, not provide correctness labels
automatically. No new training sequence or fixed holdout was imposed by this audit.

## Best-practice comparison and delivery scope

Drain3 illustrates why copying a generic log-miner ranking rule is insufficient:
its matching and mining code uses token similarity and parameter counts, with
different behavior depending on the search path. CK3's typed variable-length
regions and existing evidence defects require a more specific contract. See the
[primary implementation](https://github.com/logpai/Drain3/blob/master/drain3/drain.py).
No new parsing library or Drain dependency is proposed.

The earlier recommendation imported selective-classification abstention into a
requirement that explicitly needs a winner. That recommendation is withdrawn.
No calibrated probability or statistical accuracy guarantee is claimed here.

Next implementation should publish one versioned selection policy with the model,
evidence summaries sufficient to reproduce each preference, and an assignment
result containing selected ID/status/complete ordered bindings and literal
layout references whenever at least one eligible complete candidate exists;
otherwise return no match. Preserve the six slot types. Both learner
evaluation and pipeline runtime must execute the same published decision contract;
SQL receives the result without ranking. Do not ship the research evidence logs
or an identifier-value whitelist as runtime selection logic.

Owner review is still needed for the exact preference predicates. No selection
policy, production source, model pin, ingestion or SQL was changed by this review.
