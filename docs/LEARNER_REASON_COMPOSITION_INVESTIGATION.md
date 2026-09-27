# Reason composition and overly broad KEY inference

Subsequent implementation and complete native-log results are in
[Explicit literal guidance and native comparison](LEARNER_LITERAL_GUIDANCE_REVIEW.md).
The investigation below records the evidence and corrections preceding that
owner-authorized implementation.

2026-09-20. Read-only investigation requested by the owner. Corpus training
remains stopped; no parser, inference or matching rule changed in this review.

## Owner correction and current interpretation

Further context check: these examples are complete bracket-delimited L2s,
not `was null` phrases extracted from longer sentences. The native forms include
`cultural_acceptance trigger [ Target culture was null ]` and
`get_all_innovations_from effect [ target culture was null ]`. Both variants
start their L2; sentence-initial versus embedded position has not been shown
for these examples. Their enclosing L1s differ. `component_records` pools the
L2s and grouping sees source plus `layer:L2`, not the enclosing L1 or trace.
That implements independent L2 reuse but provides no further template-context
guard against overgeneralizing distinct L2 formulations.

The owner requires case distinctions to inform discovery. Retrieval currently
casefolds word pairs; similarity and alignment compare exact case, but a case
mismatch is then eligible to become a variable span. Removing retrieval's
casefold alone will not solve this: shared exact `was null` still retrieves
the candidates. Case variation at an otherwise literal position must not by
itself justify an unrestricted slot. Preserve literal formulations while their
common template is unestablished. Different L1 associations neither establish
nor disprove a shared L2 template, and are not an authorized eligibility rule.

The owner rejected the inference that the observations below establish reusable
nested templates. Repeating an identical reason for different innovations does
not establish independently varying, reusable reason templates. `Reason:` and
`due to:` alone do not establish this either. Additional composition is only
something to watch for during normal work; do not pursue a dedicated survey.
The parenthetical relationship example is a variable description within an
error template, not evidence of another L1/L2 structure.

The second candidate, `target <OPTIONAL_KEY> was null`, is acceptable to the
owner as an optional variable position. Matching an unobserved value does not
alone invalidate a learned variable slot. The first candidate's optional
`target` is not established: `character was null` appears with
`add_activity_log_entry effect`, whereas the other form's 23 observed L1 texts
exclude that L1. The grouping inferred optionality rather than demonstrating
it within an independently established common template. These associations
are evidence for review, not permission to partition L2 by L1.

Current grouping compares complete L2 token sequences within source and role;
it does not mine isolated `was null` subphrases as separate learning inputs.
Shared word pairs retrieve candidates, then full-sequence similarity groups
them. Differing aligned spans establish proposed variable positions; parser
boundaries subsequently influence the proposed slot type. The previous account
overstated the role of parser boundaries in discovering variability itself.

For `character (<KEY> (target character)) was null`, the actual capture is
`is_child_of` (or another complete operation token), not the whole parenthetical
phrase. The present heuristic chooses KEY because that differing span has one
token. The owner clarified that KEY is acceptable here: most of the expression
is literal and only the relationship value varies. The question about PARAM
did not authorize a relationship-specific slot rule. The subsequently installed
override was an agent error and has been removed.

Owner-supplied literal guidance is the authorized improvement. Current code
records `target`, `Reason`, and `due to` as explicit wording, matched exactly
at raw-piece boundaries, and preserves it as literal content. It does not
declare templates or slot types. No optional literals are supported. The blanket
one-spelling-plus-absence split rule has been removed for separate review.

## Evidence and scope

The completed 48-log candidate contains 1,940,027 message occurrences and
20,572 distinct complete messages across 110 sources. This investigation
examined its 2,834 distinct recognized L2 texts / 639,471 occurrences in
`jomini_script_system.cpp`. Candidate membership comes from saved
`evidence_record_ids`, not from everything a broad candidate can match.

The [audit](../.codex-tmp/learner-refactor/reason-composition-investigation/audit.json)
and [native examples](../.codex-tmp/learner-refactor/reason-composition-investigation/EXAMPLES.md)
include exact pieces, gaps, component regions, captures, source tags, protected
log paths and byte spans. All 38 selected complete native messages were
recovered again from original emission bytes using the bundled selected raw
parser. Counts cover the source's complete saved L2 evidence; the examples are
selected explanations of findings, not a representative performance sample.

The reproducible inspection tool is
[`inspect_reason_composition.py`](../tools/template_learning/inspect_reason_composition.py),
invoked with `--bundle` and `--output`. It does not train or mutate the registry.

## Why words become KEY captures

Three saved candidates all match the actual L2 `target character was null`:

| Proposed candidate | Actual distinct supporting L2 texts | Capture on `target character was null` |
|---|---|---|
| `<OPTIONAL_KEY> character was null` | `character was null`; `target character was null` | `target` |
| `target <OPTIONAL_KEY> was null` | `target faith was null`; `target slot was null`; `target title was null`; `target was null` | `character`, absent from this candidate's supporting values |
| `<KEY> <KEY> was null` | `Target culture was null`; `Target faith was null`; `target culture was null` | `target`, `character`; `character` absent from this candidate's supporting values |

In the first candidate, **`character was null` remains literal**. The observed
variation is the presence or absence of `target`. The two supporting texts
occur 4 and 63,379 times respectively; repeated occurrences do not weight
grouping. Exact text is deduplicated within source and component role.

The current code path is:

1. `layers.component_records` supplies a source-wide L2 pool independently of
   L1. Observed L1 associations do not limit L2 reuse.
2. `clustering.anchors` retrieves candidates through shared adjacent word
   pairs. It casefolds retrieval keys only; native tokens remain unchanged.
3. `cluster_source_records` compares exact token sequences against each group's
   first member. Its default threshold is 0.72. It updates the representative
   only after grouping finishes. The examples above share `was null` and
   meet the threshold: 0.775 or 0.8375 for non-seed members.
4. `patterns.derive_pattern` retains consensus literals and turns differing
   positions into variable spans.
5. `patterns._slot` proposes KEY for a single non-punctuation parser token,
   or OPTIONAL_KEY when absence was observed. Token eligibility is being used
   as sufficient evidence of a symbol slot.
6. `patterns.match_pattern` accepts any token satisfying that structural
   constraint. It does not constrain KEY to observed values. That permits the
   unsupported `character` substitutions above.

The third group additionally turns `Target` versus `target` into a variable
position. This does not establish that the subject word is an identifier.
Native capitalization should not be normalized away to conceal the issue.

The cause is now demonstrated in current source-specific L2 inference. It is
not a parser punctuation error, cross-source comparison, duplicate-frequency
bias, or a surviving competing whole-L1+L2 template. Separating L1/L2 removed
the earlier whole-message problem but does not resolve this within-L2 issue.

Whether these phrases should be separate literal templates or a composition
with a constrained subject-description component remains a modeling decision.
The evidence establishes wording variation; it does not establish unrestricted
KEY substitutions.

## Observed formatting; reusable nested templates not established

The following counts are source-specific observational queries, not installed
recognition rules. Query groups can overlap.

| Observed structure inside script-system L2 | Distinct L2 texts | Occurrences |
|---|---:|---:|
| Explicit `Reason:` clause | 24 | 30 |
| Explicit `due to:` cause | 40 | 42 |
| `character (<operation> (target character)) was null` | 6 | 346 |
| Actor/recipient field block beginning `Actor:` | 10 | 11 |
| Failure followed by `Current Buildings =` state | 5 | 9 |

A native `run_interaction effect` has L2 containing
`Interaction cannot be sent. Reason:` followed by native formatting controls
and `No target selected`. This is a failure/reason construction **inside the
already recognized L2**. Other native L2s report inability to join an activity
followed by `due to:` and a formatted condition explanation, including nested
`All of these:` / `Any of these:` lists.

The null family also contains the exact text
`character (is_child_of (target character)) was null` and five related forms.
Its current candidate is `character (<KEY> (target character)) was null`, with
observed operation names `is_child_of`, `is_close_relative`, `is_consort_of`,
`is_parent_of`, `is_sibling_of`, `is_spouse_of`. These are nested operand or
operation descriptions. Parentheses alone do not prove another error template.
Likewise, actor fields and building dumps are structured context, not
automatically additional failures. None should split a diagnostic record.

An additional inventory outside the known script envelope kept each source
separate. In `culture_history_entry.cpp`, 57 messages have `Reason:`: 48 have
an empty suffix and 9 have content. Eight different blocked innovations share
the exact same formatted explanation beginning `Discover at least` and ending
in a missing-innovation count. The ninth explains prerequisites for
`innovation_repeating_crossbow`. This is concrete evidence of another
failure/reason arrangement, with repeated reason text across different outer
messages in the same source. It does not establish reusable nested templates
or authorize cross-source template reuse. The owner has directed no further
dedicated investigation of this hypothesis.

The [outside-envelope evidence](../.codex-tmp/learner-refactor/reason-composition-investigation/outside-known-envelope.json)
retains all nine nonempty culture examples and their raw pieces/provenance;
each was checked against the native emission and reparsed. It also records two
actual script-system messages whose error text ends abruptly before the script
location and has no closing `]`. The protected log bytes confirm this is not
loss introduced by the parser. Their composition is not recognized by the
current complete-envelope rule. The engine-side cause of the abrupt ending is
unknown. Preserve these as incomplete evidence; do not invent closing bytes.

## Proposed direction, not installed changes

- Separate candidate grouping from the decision that a varying word is a KEY.
  Complete-token boundaries are necessary but do not establish slot semantics.
  Preserve literal alternatives or an explicitly unresolved component proposal
  when the evidence supports wording variation without a symbol domain.
- Keep additional reusable message composition as an observation to watch for,
  not an active investigation. Treat the parenthetical relationship as a slot
  within a template. KEY is acceptable; there is no special-case typing rule.
- Keep exact case, punctuation, control codes, whitespace and observed
  composition boundaries. Use only explicitly supplied literal wording; do not
  invent extra lists, first-two-word rules, or formatting normalization.
- Continue to learn within each source. Keep the owner's known L1/L2 convention
  and unrestricted source-wide L2 reuse. Additional reusable components must
  not introduce hardcoded L1/L2 compatibility lists or extra diagnostic records.
- Apply explicit literal guidance and review KEY/PARAM evidence against these
  native cases. PARAM can represent a variable phrase, including a one-token
  instance; relabeling an overly broad KEY as PARAM does not repair a wrongly
  variable literal. Optional literals are not supported. Evaluate corrections on complete logs, reporting
  overlaps and unknowns explicitly.

The saved candidate and registry are unchanged. The registry has 73 ingested
inputs but only a completed 48-log checkpoint; a plain build would not repeat
this 48-log investigation.
