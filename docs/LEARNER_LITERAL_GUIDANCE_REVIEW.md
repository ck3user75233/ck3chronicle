# Explicit literal guidance: correction and native comparison

2026-09-20. This supersedes the interpretation in the
[v4 experiment](LEARNER_LITERAL_CONTEXT_REVIEW.md).

Subsequent owner clarification removes the separate colons from the live
wording declaration: `target`, `Reason`, `due to`. See the
[native wording survey](LEARNER_LITERAL_WORDING_SURVEY.md). The immutable v5
comparison and counts below retain the declaration actually used for that run.

## Corrected authority and implementation

The owner did not authorize an example-specific relationship PARAM rule. The
rule, application function, exported slot rule ID and claimed authority are
removed from active code and documentation. The relationship value is inferred
normally; the actual native examples yield
`character (<KEY> (target character)) was null`. Most of the expression remains
literal. New models have an empty `owner_overrides` list.

The authorized feature is explicit supplied wording. Its editable declaration
now lives in [owner_rules.json](../tools/template_learning/owner_rules.json).
The declaration used for this historical comparison was:

```json
{"literals": ["target", "Reason:", "due to:"]}
```

This is wording guidance, not a catalog of special templates or slot types.
It applies inside the existing complete-message or L1/L2 learning unit and
does not construct additional subphrase templates or nested records.

The implementation:

1. Finds exact case-sensitive strings aligned with complete existing raw-parser
   pieces. It retains original gaps and never splits an identifier substring.
   `target_character` and `@target` are not the literal word `target`.
2. Uses the ordered guided pieces alongside punctuation as fixed anchors for
   candidate grouping and sequence alignment. Presence/absence or a different
   position relative to those anchors cannot be hidden in a variable slot.
3. Records the wording in the model's `literal_guidance` and in each inferred
   slot's `constraints.literal_guidance`. Matching uses that saved declaration
   and rejects a capture intersecting guided wording, even if that wording was
   absent from the candidate's own supporting messages.

Case-sensitive retrieval and separate case-only literal formulations remain.
Literal parts are mandatory exact text. There is no optional-literal node,
optional-literal syntax, or planned expansion in that direction. Existing
optional variable slots remain supported. Separate formulations for
`character was null` and a reason beginning with literal `target` are acceptable.

## Separate review of the blanket absence rule

The v4 rule treated every proposed variable with one distinct nonempty value
plus absence as a reason to split the candidate. That was broader than the
owner's wording guidance and is removed from active inference.

Presence/absence alone does not identify the value's role: the word may be
supplied literal wording, or the evidence may contain only one observed value
of an optional variable. A universal split also reduces the evidence available
for other variable positions in each resulting group. In the v4 comparison,
this contributed to ten lost special-building-slot L2 matches. Conversely,
removing it can leave nonguided words incorrectly proposed as variable slots;
that remains an empirical inference question, not permission for optional
literals or a restoration of the blanket rule.

The current mechanism protects a supplied word because it was supplied as
literal guidance. It does not infer that every singleton-plus-absence position
has the same meaning.

## Verification and scope

The selected raw parser remains `ck3-lossless-v1.1`; its implementation has not
changed. The native check reparsed 38 original captured emissions and verified
their exact saved pieces. All three supplied strings were observed, the
relationship capture remained KEY, and supplied wording was not captured by
matching inferred slots. This is a focused behavioral check, not the performance
sample for the comparison.

The full comparison uses the same 48 training-log hashes as v4 and all 25
additional cached logs with frozen candidates. The parser-version/digest and
feature-cache hashes are validated. All messages and occurrence counts enter
evaluation; no tiny selected sample determines the reported corpus outcomes.
Registry roles, confirmations, current revision, production models and SQL are
not changed by this comparison.

Detailed outputs are in
[the comparison directory](../.codex-tmp/learner-refactor/explicit-literal-guidance-review/summary.json)
and [the native wording check](../.codex-tmp/learner-refactor/explicit-literal-guidance-review/guidance-native-check.json).

## Completed comparison

Candidate `87b4eed8261625c4ba9ff05c` uses
`source-component-consensus-v5`. The baseline is v4 candidate
`09b423a12a029f957c700512`. The 48-log build includes 1,940,027 occurrences,
20,572 distinct complete messages and 110 source families. Matching remains
source-specific. The additional 25 logs contain 654,574 occurrences and were
evaluated against the frozen candidates, not added to this build.

| Outcome | 48 logs: before | 48 logs: after | Additional 25: before | Additional 25: after |
|---|---:|---:|---:|---:|
| Full ordinary match | 1,294,345 | 1,288,470 | 211,937 | 210,938 |
| L1+L2 match | 490,589 | 554,659 | 327,477 | 332,757 |
| L1-only | 0 | 0 | 1,952 | 1,942 |
| Partial | 0 | 0 | 239 | 239 |
| Provisional: competing matches | 155,093 | 96,898 | 9,581 | 5,314 |
| Unknown | 0 | 0 | 103,388 | 103,384 |

Ambiguous occurrence counts improve, but this is not uniform improvement:

- On the training logs, distinct ambiguous message/context cases increase from
  1,338 to 2,075. Previously single-match occurrences becoming ambiguous total
  7,868. There are 64,070 transitions from ambiguous to L1+L2 and 1,993 to full.
- On the additional logs, distinct ambiguous cases increase from 212 to 928.
  Previously single-match occurrences becoming ambiguous total 1,041. There
  are 5,270 transitions from ambiguous to L1+L2 and 38 to full.
- All 14 recognition losses from the v4 experiment recover: ten
  special-building-slot occurrences regain L2 and four state_faith Event-target
  occurrences regain full matching. No previously complete match becomes
  unknown, partial or L1-only in this comparison.

The frequency improvement is concentrated in repeated families. More distinct
ambiguous cases is a real regression; lower occurrence totals alone do not
establish better semantic accuracy. Current output has 530 ordinary and 954
component templates, no unsupported candidates, and no confirmed templates.
Unknown and incomplete outcomes in the additional logs remain unresolved.

The two original comparison logs were also freshly parsed from their actual
files with the candidate's bundled parser, with input hashes verified. Their
8,723 and 3,694 messages have zero unknown, partial or L1-only outcomes.
Ambiguities change from 82 to 79 on the first and **0 to 9 on the second**.
All nine regressions on the second concern `Unrecognized loc key` messages
with `Near file:` tails; the competing candidates are shown below.
See [fresh replay results](../.codex-tmp/learner-refactor/explicit-literal-guidance-review/fresh-parse-summary.json).

## What improved and what remains wrong

Supplied `target` is now literal. The separate unprefixed `character was null`
formulation is retained. In the target-prefixed family, evidence supports
`target <OPTIONAL_KEY> was null`, with descriptors including character, culture,
faith, slot and title, as well as absence. This removes the previous overlap
with the target-character formulation. It does not force every descriptor to
be literal. The relationship expression is learned normally as
`character (<KEY> (target character)) was null`; no PARAM override remains.

The largest remaining repeated overlap accounts for 83,895 training occurrences:

```text
Wrong scope for trigger: <KEY>, expected <KEY>
Wrong scope for <KEY>: <KEY>, expected <KEY>
```

A separate confirmed problem affects ordinary script-system messages outside
the recognized bracketed L1/L2 convention. Candidate grouping sees complete
messages, including common `Script system error!`, `Error:` and trace framing.
For example, actual native support for one broad candidate contains:

```text
Could not fetch title or province from scope 'county'
Invalid left side during comparison 'holder'
```

The resulting error portion is:

```text
Error: <KEY> <KEY> <KEY> <KEY> <KEY> <PARAM> '<KEY>'
```

The first five positions turn `Could / Invalid`, `not / left`, `fetch / side`,
`title / during`, and `or / comparison` into variables. Similarity of the
surrounding message is insufficient evidence for these substitutions. This
candidate also accepts native `Character with no location in link 'location'`
messages and competes with a more literal candidate. Complete support,
raw pieces and candidate parts are saved in
[the native broad-candidate evidence](../.codex-tmp/learner-refactor/explicit-literal-guidance-review/broad-ordinary-candidate.json).
This is evidence of overgeneralization, not evidence authorizing another
nested-template convention.

Removing the blanket absence rule also exposes nonguided literal words:

```text
Unrecognized loc key <KEY>. <OPTIONAL_KEY> file: ...
Unrecognized loc key <KEY>. Near file: ...
```

The first candidate can capture `Near` as a variable. These are the nine fresh
second-log regressions and a 448-occurrence training overlap. No optional
literal was introduced: the defect is proposing a variable where literal
wording belongs. Guidance for the three supplied strings cannot establish
the role of every other word.

The remaining substantive work is candidate formation and competing-candidate
reconciliation. Current grouping compares with its first member; common framing
can outweigh different diagnostic wording, and broad and narrow candidates
survive together unless their complete patterns are identical. Corrections
must use native support and the current candidate's supported structure,
retain case and source boundaries, and expose insufficient evidence. Selecting
one preferred match would merely conceal these overlaps. No additional
sentence-specific rules, literal words or slot-type overrides were installed
to make the comparison pass.

## Completion state

The full comparison and fresh replays completed. One initial comparison attempt
exposed a list-versus-tuple cache-key error in the new guidance helper; it was
fixed by canonicalizing containers without changing parser pieces, then the
full comparison completed successfully. Guidance checks cover both forms.
Final checks verified all bundle hashes, the reported counts against review
rows, compilation of the changed modules, and packaging of the guidance file.
All 3,433 exported slots carry the saved guidance; all 4,912 literal parts are
mandatory, and no exported owner rule ID remains.

Registry current revision remains `e6aee7eeb209c9e26abf72da`, with no
confirmations. Neither comparison candidate was promoted. Generated native
evidence stays outside Git; the current model contract, inference-rule record,
pipeline handoff and session handoff describe the corrected implementation.
