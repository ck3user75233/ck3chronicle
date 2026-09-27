# Learner version isolation and cumulative evidence — 2026-09-25

Owner direction: no template imports. Each learner version rediscovers templates
from native evidence; its registry must be isolated from other learner versions.

## Work status

- Complete: remove confirmed-template import, confirmation command and frozen-template discovery bypass.
- Complete: bind registries and caches to learner implementation identity; reject foreign state.
- Complete: inspect cache contents and selection; execute native cache/direct-record equivalence,
  occurrence accounting and an isolated registry build (4,179 messages, no unresolved emissions).
- Complete: run v30 on the original ten complete native logs (297 templates: 165 supported,
  132 provisional; zero imports). All 7,864 contextual assignments and captures match v29.
- Complete: run the same learner on those ten plus twenty additional native logs;
  compare both models on the same complete evidence and inspect changed inference.
- Complete: research incremental template learning and confidence revision; recommend
  a mechanism without implementing a new inference architecture in this change.

The 10/30 experiment is expanding-corpus batch retraining, not a demonstration of
incremental hypothesis updates. Production model selection remains unchanged
until a new candidate is reviewed. Generated logs, candidates and measurements
stay under `.codex-tmp/learner-refactor/version-isolation-v30/`.

## Native experiment result

**More data improves coverage but also exposes serious overgeneralization. The
30-log candidate is not suitable for promotion.** Removing imports itself caused
no inference regression on the original ten logs: every executable template,
status, support summary, candidate assignment and capture is identical to v29.

Both fresh runs use learner v30, parser v1.6 and unchanged inference rules. The
thirty inputs are the original publication ten plus the first twenty additional
SHA-sorted logs from the retained corpus, selected before outcomes. Neither build
reads previous models or feature caches. Native input hashes were verified.

| Build | Native messages | Distinct messages | Templates | Supported | Provisional |
|---|---:|---:|---:|---:|---:|
| 10 logs | 352,317 | 7,827 | 297 | 165 | 132 |
| 30 logs | 1,143,064 | 38,584 | 406 | 243 | 163 |

Both have zero unresolved emissions and zero imported/confirmed templates. Build
times were 194.4 and 415.6 seconds; these are observations on this machine, not a
controlled speed benchmark. Candidates are `7885c36206ddaf31a7ec9a3b` (10) and
`7278879bde9161fd798abc6d` (30). The shared source fingerprint is
`5215661b7ab41b3b91129ea2e9f16a0aa11523e2520f54808bf6df383624f5b4`.

Both models were evaluated on exactly the same thirty-log evidence:

| Outcome on the same 1,143,064 occurrences | Model learned from 10 | Model learned from 30 |
|---|---:|---:|
| One supported, unambiguous match | 620,385 | 679,252 |
| Provisional result | 283,545 | 463,812 |
| No match | 239,134 | 0 |

These are structural outcomes, not correctness scores. On the **original ten**,
8,343 formerly full occurrences become provisional; 759 go the other way. On the
added twenty, 14,231 full occurrences become provisional. The total newly
ambiguous count is 22,574, all key-reference diagnostics. Meanwhile 72,540 formerly
unknown occurrences become full and 166,594 become provisional. Training on these
inputs does not establish unseen-log accuracy. Across the common corpus, 24,362
contextual rows /303,954 occurrences change assignment or capture information.

### Inspectable improvements

Actual native message: `New data types does not contain a 'Character' data context`.
The ten-log model retains that literal wording as provisional. With new `Culture`
and other observations, the thirty-log model learns the supported formulation
`New data types does not contain a '<KEY>' data context`. This is useful evidence
generalization rather than repeating one observed spelling (2,729 previously
provisional occurrences of the Character form; 2,018 previously unknown Culture
occurrences in this corpus).

The tooltip/description construction containing `Error: culture trigger [...]`
previously had no matching template for its complete native layout. Thirty logs
produce `Error: <KEY> trigger [ <REASON> ]`, with file and line LOCATORs and a trace
PARAM retained separately. This change group covers 37,320 occurrences. The full
native text, raw pieces and captures are in the readable review.

### Confirmed regressions and mechanism

The thirty-log model creates supported template `0a7ae5626ebf4b4291dac439`:

```text
<PARAM>: <PARAM>, near line: <LOCATOR>
```

It absorbs `Unknown trigger: <KEY>, near line: <LOCATOR>` (26,721 occurrences)
and `Unexpected token: <KEY>, near line: <LOCATOR>` (4,097 occurrences), turning
their diagnostic wording into captured data. Both still count as full matches,
demonstrating why the full-match total is insufficient. The first PARAM has nine
observed phrases, including `Unknown effect`, `Malformed token`, `Unexpected token`
and `Failed to read key reference`; its saved assessment says punctuation on the
right, no surrounding wording, yet supported. Variation among those different
diagnostic formulations is not sufficient proof of one variable field.

Saved refinements explicitly show `reconsider_supported_groups` absorbing narrower
groups because the broader candidate matches all their members and joint inference
retains **the broad candidate's** wording shape. That path does not call the existing
`erased_supported_wording` check used during other region regrouping. The review
therefore identifies an inference/merge defect, not a reason to treat the broad
candidate as an equally credible competitor. No new special case has been added.

The correct OPTIONAL_KEY key-reference template survives but now overlaps this
broad template. For absent keys both candidates have complete captures (22,061
occurrences); for present keys the broad candidate can place the colon boundary
in more than one way (513 occurrences). Together these explain the 22,574 new
provisional results. The old KEY-failure fallback was not restored or imported.

The brace message `Failed to read key reference: }: }, near line: 23876606`
also regresses: it was a provisional singleton; the larger corpus merges it into
the broad template, capturing `Failed to read key reference` and `}: }` as PARAMs.
It is reported full despite remaining malformed evidence (three occurrences in
the thirty logs, including the original two). Initial isolation is undone by
later regrouping; this is not a successful brace repair.

A second regression occurs for the native texture lookup:

```text
Could not find texture due to 'VFSOpen Error: gfx/coat_of_arms/colored_emblems/ce_african_cross_NU.dds not found'
```

Before: `Could not find texture due to 'VFSOpen Error: <LOCATOR> not found'`.
After: `Could not find texture due to 'VFSOpen Error:<PARAM>not found'`.
The new field's evidence includes a two-space value alongside sixteen path values.
An empty token sequence makes the all-values location check fail; multi-token
variation then supports PARAM, including surrounding spaces. This loses attribution
information. That 4,307-occurrence transition from provisional to full is therefore
a regression, not a quality improvement. The general remedy must handle missing
or malformed field values without erasing independently established path structure.

Other inspected limitations persist: succession names still use several KEYs;
character-history explanations still include `is <KEY> <KEY> <KEY>`. These were
not repaired by more logs. Expression PARAM recognition and the inspected mesh
formulations remain available. The HTML retains ten focus cases plus all 216
changed assignment groups; only the examples discussed here have semantic judgments.

### Verification and next correction

The existing native requirement checks on the ten-log candidate report 32 passes
and one unexercised ambiguity check. The previous assertion that every corpus must
contain ambiguity was replaced by an explicit skip; no artificial messages were
introduced. The obsolete seed-import check was removed with that API, retaining
its actual native singleton-status check. These structural checks do not claim
the thirty-log inference is correct.

An isolated fresh registry was exercised on a complete 4,179-message native log.
Sync, repeated sync, cache reload, direct-record comparison and model build passed;
the old registry was rejected and its bytes were unchanged. JSON turns tuple pairs
into arrays; comparison of canonical serialized records confirms identical content.

Before implementing the proposed persistent hypothesis updates, correct the
general merge acceptance and field-outlier handling identified above, then repeat
this exact 10/30 comparison. Reuse established field/literal evidence across every
merge path; do not fix the symptoms with diagnostic-word lists or manual template
edits. Incremental state must not make an unsupported generalization harder to
challenge. These inference corrections are identified, not implemented in v30.

## What the cache actually does

`collect_records` reads the selected lossless parser. It retains complete message
text, raw pieces, wrapper regions and every occurrence's source spans. Identical
source/context/text observations share one learning record; occurrences remain
attached. No template, token mask, normalization or semantic projection is cached.

If the parser cannot recover individual messages within an emission, that emission
is explicitly saved under `evidence_stats.unresolved_emissions`, including its
text, source, byte ranges and reason. It does not enter template inference. The
registry validates that recovered and unresolved emissions together account for
every framed emission, with no overlap. A parser exception aborts the operation;
it is not an instruction to skip a log. These checks concern framed emissions;
the original complete file remains the byte-level authority.

The registry chooses whole input logs by their recorded role. Only `training`
logs enter a build. Sync defaults to `candidate`, unless the caller explicitly
chooses training. That is evidence selection, not text preprocessing. Stale or
incompatible caches fail explicitly; they do not cause messages to disappear.

v30 state records version plus implementation hashes. Default roots include this
identity. Explicit roots reject different identities or old registry schemas;
there is no migration, importing or reading another version's conclusions. A
fresh registry can be populated from the same explicitly selected original logs.
The registry also pins the parser on first sync. Builds remain batch rediscovery
over accumulated selected evidence, not online hypothesis updating.

## External research and recommendation

Drain3 demonstrates actual incremental template mining: a persisted search index
and learned groups are updated when each new message arrives. Its API distinguishes
creating a group, changing its template, and adding a member without a template
change. This supports retaining learned hypotheses within a learner version.
It does not provide a calibrated probability that a template is semantically
correct. Its group size is a message count, not our independent learning support.
See [Drain3's implementation and persistence documentation](https://github.com/logpai/Drain3).

Drain's template update replaces differing token positions with wildcards and
requires equal token counts. That is unsuitable as a drop-in replacement for our
variable-length PARAMs and raw boundaries. The useful precedent is persisted,
updatable knowledge, not its positional wildcard inference or text masking.
See [the owning algorithm](https://github.com/logpai/Drain3/blob/master/drain3/drain.py).

Spell is another directly relevant online miner: it maintains message types and
updates them using longest common subsequences as new messages arrive. It is
evidence that online template discovery need not rebuild the whole corpus.
For CK3, shared subsequences alone would still need our raw-region/slot validation
to avoid preserving incidental words inside PARAMs. This is a design comparison,
not a proposal to replace our lexer or install another parser.
See [the authors' Spell paper](https://users.cs.utah.edu/~lifeifei/papers/spell.pdf).

River's Hoeffding Adaptive Tree maintains alternatives and replaces a subtree
when an alternative has sufficient evidence of better performance. That supplies
a useful design precedent: supported conclusions can be challenged and replaced.
However, this is supervised learning; CK3 logs do not supply true template labels.
Its statistical thresholds cannot be transplanted as template-correctness guarantees.
See [the adaptive-tree API](https://riverml.xyz/latest/api/tree/HoeffdingAdaptiveTreeClassifier/).

ADWIN detects changes in an observed numeric stream using adaptive windows. A
source's rising mismatch rate could trigger investigation, but changes in mod
mix or CK3 version are not themselves proof that a template is wrong. I recommend
deferring automatic forgetting or drift-triggered replacement until the basic
evidence update mechanism works. See [ADWIN](https://riverml.xyz/latest/api/drift/ADWIN/).

Online evaluation normally records a prediction before learning from the new
example. For us, a match before updating is measurable; semantic correctness
still needs inspected native examples or owner adjudication. Feeding a selected
match back as unquestioned truth would amplify mistakes. See
[River's batch-to-online explanation](https://riverml.xyz/latest/examples/batch-to-online/).

### Proposed next implementation, not part of v30

1. **Persist hypotheses and their evidence inside one version's registry.** Keep
   each source's learned formulations, supporting distinct native records,
   candidate-local field observations and revision history. Do not import model
   artifacts. The learner resumes its own evolving state; a new version starts
   from explicitly selected native logs again.
2. **Assess new evidence before updating.** Exact duplicate observations update
   occurrence provenance only. New distinct messages are checked against current
   hypotheses, recording current matches, mismatches and competing interpretations.
   A successful match is compatibility evidence, not a correct-label assertion.
3. **Update the affected hypotheses, not the whole corpus.** Reuse earlier member
   evidence and field boundaries. Consider new messages alongside comparable
   same-source evidence. For a proposed split, merge or generalization, re-evaluate
   the affected members and competing neighboring hypotheses; do not discard
   earlier support or freeze a supported template. Removing a provisional
   hypothesis requires an evidence-backed replacement, with history retained.
4. **Track evidence strength explicitly.** Record independent diagnostic forms,
   slot-value diversity, boundary support, malformed outliers, contradictory
   observations and overlap with other hypotheses. Repetitions, extra locator
   spellings and trace interiors must not masquerade as more diagnostic support.
   Support belongs to the particular hypothesis/field, not pooled unrelated errors.
   Preserve provisional/supported statuses; no third template tier is proposed.
   A scalar probability should wait for measured calibration against inspected
   native cases. Counts or match rates alone cannot supply that probability.
5. **Allow both increasing and decreasing confidence.** New valid variants may
   support a literal-to-slot refinement. Counterexamples can narrow or split an
   overbroad hypothesis, or reduce support for a field boundary. Broadening is not
   the only legal update. A production winner is an assignment decision, not new
   training truth. Record why each learner revision changed a conclusion.
6. **Publish immutable snapshots separately.** The learner's same-version state
   can evolve; ingestion uses an explicitly pinned snapshot. Validate incremental
   updates against full rediscovery on the same native corpus, several log arrival
   orders and restart/resume. Compare slot captures and wording, not merely counts.
   Batch rediscovery remains a reference computation during development, not the
   normal implementation disguised as incremental learning.

This is a proposed engineering design informed by the external mechanisms above,
not a claim that any cited library supplies CK3 grammar or confidence labels.
No external dependency, new score, slot rule, template selection policy or online
inference mechanism has been installed or implemented in v30.
