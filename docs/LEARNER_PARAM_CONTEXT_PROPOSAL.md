# PARAM context and merge correction proposal — 2026-09-25

Status update: owner approved sequential work, pausing after each step. Step 1
is now in native validation; see LEARNER_PARAM_BOUNDARY_REVIEW.md. Owner further
directed removing unmarked-PARAM acceptance without attempting to preserve its
existing assignments. The unmarked-discovery proposals below are deferred, not
implemented. Items 2 onward remain pending.

Original proposal status: broader proposal for owner review. The subsequent owner-directed listed
diagnostic-wording loss blocker is now implemented in v31; see
`LEARNER_DIAGNOSTIC_WORDING_LOSS.md`. The remaining mechanics below have not been
implemented. v30 import removal/version isolation remains implemented; its 10/30
native comparison is the baseline, not proof of this proposal.
Persistent/revisable hypotheses are deferred.

Owner clarification: PARAM represents an independently identified variable-length
field, often explanatory/contextual content, not shared diagnostic wording. Words
repeating inside proposed values are neither positive PARAM evidence nor a reason
to preserve an existing PARAM assignment. Strong recurring internal structure may
instead expose diagnostic wording that the proposal wrongly absorbed. Evaluate
that possibility against the complete messages and external context. Once a field
is justified, matching uses its boundaries and admissible structure; its words do
not positively establish template similarity. Existing PARAM assignments are
subjects of the native review, not acceptance targets.

Owner clarification on discovery order: search clearly demarcated regions first.
An isolated adjacent colon does not propose an enclosing boundary. Unmarked PARAMs may be
discovered from concrete unexplained native variation within an independently
established formulation, but should not be routinely sought by broad alignment.
An isolated colon on one side supplies zero positive PARAM-identification evidence:
it is not a score bonus, weak endorsement, or relaxation of acceptance requirements.
It remains a raw structural token and may constrain a boundary established by
other evidence; its presence does not favor PARAM over another interpretation.
This also applies to sentence-ending punctuation. Such punctuation may be found
to mark the endpoint of an independently discovered field, but must not trigger a
PARAM hypothesis or add positive PARAM evidence merely by adjoining text.
Opening/closing candidates are specifically `(...)`, `[...]`, `{...}`, double
quotes and single quotes. Bracket pairs are substantially stronger discovery cues
than quotes. A colon pair is not an enclosing delimiter pair. Backslash remains
excluded as a PARAM proposal marker under the existing path-handling direction.

## Confirmed current mechanics

| Path | Current weakness | Proposed correction |
|---|---|---|
| `regions.field_evidence` | Variation plus punctuation on either side can suffice; no independent diagnostic context requirement. | Boundary/variation evidence and external diagnostic context must both pass. |
| `clustering.learning_tokens`, region-neighbor selection | Location values are hidden, but recognized location-label words remain; after inference only PARAM captures are explicitly excluded here, rather than every accepted variable field. Empty sequences can compare equal. | One role-aware comparison view excludes structural labels and all variable/proposed fields; empty diagnostic context cannot support discovery or merging. |
| `patterns.derive_pattern` | Balanced-region proposals, ordinary alignment and two field-coalescing passes can change what is literal. Assessment occurs per field without recording context dependencies. | Assess the complete proposed field set together, after every transformation, with context provenance. |
| `refine_literal_variants`, `refine_supported_wording` | Initial inference and partition/re-inference have no shared contextual acceptance contract. | Initial and revised groups use the same validator; failed proposals retain evidence in narrower formulations or explicit unresolved review. |
| `consolidate_same_wording` | Its wording shape treats different text-slot types alike; a successful re-inference can broaden fields. | Exact duplicate contracts may combine evidence without changing the contract. Any other union needs a concrete trigger and full contextual acceptance. |
| `reconsider_supported_groups` | Complete-match coverage can absorb another group; it preserves the broader candidate's wording shape, not both groups' independently established wording. Called twice. | Remove coverage-driven absorption and both unconditional invocations. Matching coverage remains a validation check, never a merge justification. |
| `refine_region_groups` | Unconditionally examines neighbors until no group-reducing union passes. Its protection is local to this path and its comparison can retain location-label words. | Process evidence-triggered proposals through the common validator; no repeated broadening merely because another pass can reduce group count. |
| `erased_supported_wording` | Only checks alphabetic runs of at least two words, and exempts paired-boundary PARAMs. It is not used by all union paths. | Preserve actual independently supported diagnostic literal spans, including single words and symbol-like wording; paired punctuation is not a waiver. No vocabulary list. |
| Final duplicate-ID consolidation | Re-infers the combined pool after identical IDs converge. | Aggregate identical executable patterns without broadening; changes require the same proposal mechanism. |
| `artifacts._context_patterns` | Wrapper inference constructs independent wrapper records. | Empirical wrapper-field validation must retain its owning complete diagnostic context; location-only wrapper wording cannot justify PARAM discovery. |

These are code-review findings. The v30 saved native evidence already demonstrates
the broad `<PARAM>: <PARAM>, near line: <LOCATOR>` and texture-LOCATOR regressions.
No result below is claimed to have been demonstrated by a revised implementation.

## Revised proposal triggers

New, distinct observations can propose an initial formulation when there is no
existing explanation. A working formulation may be reopened only with a recorded
native witness for one of these deficiencies:

1. **Unexplained variant:** it shares independent external diagnostic wording and
   compatible structure, but the current fields/literals cannot explain it.
2. **Contradictory field evidence:** new corresponding region content challenges a
   current type, boundary or previously inferred literal. A malformed observation
   triggers investigation; it does not automatically justify broadening.
3. **Capture inconsistency:** inferred member ranges and complete matching disagree,
   or the current formulation admits incompatible capture divisions.
4. **Competing interpretations:** eligible explanations conflict on an actual native
   message and expose an identifiable field or grouping deficiency. An independently
   unsupported broad candidate cannot create its own reopening authority.

Store the witness record IDs, affected field/context spans and the exact deficiency.
More occurrences, more input files, a larger support count, or a broader candidate
matching another group's members are not triggers. A new valid value of an already
supported field can add evidence without replacing diagnostic literals.

This is within-build bookkeeping for the mechanical correction, not a persistent
hypothesis architecture. The same batch run can discover a genuine deficiency
while processing distinct messages. Model import remains prohibited.

## Acceptance mechanics

### 1. Separate structural facts from diagnostic evidence

Use the selected parser's actual pieces and original ranges. From those, record
source, construction, recognized locations and their introductions, declared
fields and delimiter relationships. This is an evidence view, not rewritten text.

For diagnostic comparison, remove from the evidence calculation:

- recognized location values and complete location-label spans;
- punctuation and whitespace;
- accepted KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM and REASON contents;
- every region provisionally proposed as variable in this candidate, including
  nested/coalesced spans, before assessing whether that proposal can be accepted.

Exclude construction boilerplate according to the existing declared comparison
regions. Do not introduce default literals, word blacklists or word normalization.
Use case-sensitive shared literal wording in the remaining diagnostic region.
Exclusion from a comparison never removes bytes from the record or template.

A nonempty common external context is necessary. It is not sufficient by itself:
corresponding region boundaries, field evidence and previously established wording
must also pass. Similarity scores can retrieve possible neighbors; they cannot
override a failed context or preservation check. No new numerical cutoff is proposed.

### 2. Prioritize demarcated regions, then validate fields together

The current implementation only partly follows boundary-first discovery:
`candidate_envelopes` proposes balanced outer interiors before interior alignment,
but `field_evidence` defines `punctuation_bounded` as punctuation on either side.
It records paired boundaries without requiring or prioritizing them in acceptance.
The weak-connector coalescing pass likewise accepts punctuation on either edge as
grounds to propose a larger field. These later routes undermine the intended
priority; adding another early balanced-region pass would not fix them.
The existing exclusions already include a period, equals sign and backslash;
the generic punctuation test still admits other sentence endings such as `!` and
`?`. The correction is explicit enclosure recognition, not a growing list of
punctuation exceptions. The configured `marker_pairs` already lists parentheses,
square brackets, braces and both quote types; the permissive later checks are
not restricted to those pairs.

Proposed discovery order and restrictions:

1. Honor existing owner-declared structures and recognized locations. Then inspect
   corresponding, explicitly demarcated regions in comparable native messages,
   starting with matched `(...)`, `[...]` and `{...}` envelopes. Paired double and
   single quotes are weaker, secondary candidates, not equally strong enclosure
   evidence; their opening/closing use must be established in the native context.
   Keep surrounding markers as structure and assess the interior as a region before
   decomposing it. Delimitation proposes a field; it does not establish PARAM type.
   Do not extend enclosure discovery to arbitrary punctuation pairs such as colons.
2. Isolated adjacent punctuation, including colons and sentence endings, must not
   trigger a PARAM proposal or increase its support. First discover a variable
   field through independent native evidence; only then can such punctuation be
   established as its endpoint. This differs from proposing an actual paired
   envelope. Two punctuation marks somewhere around a span are not automatically
   an envelope.
3. Do not run a general search for unmarked PARAMs. Consider one only when a
   concrete unexplained native variant or capture contradiction in an otherwise
   independently supported formulation exposes a corresponding variable region.
   Record how the unchanged surrounding message structure locates both endpoints,
   and inspect competing divisions. More different values or multi-token content
   alone cannot substitute for this boundary evidence. If the endpoints remain
   uncertain, retain that uncertainty rather than accepting a broad PARAM.

Every inference and coalescing path must retain the region's proposal origin and
boundary evidence and pass this policy. Merge selection is driven by matching
diagnostic wording, as specified below, not by punctuation or a boundary score.
If a justified merge proposes changed fields, those changes still need their own
field evidence. This is a discovery priority and evidence requirement, not a ban on unmarked
or message-initial PARAMs. No new numeric threshold or example-specific exception
is proposed. Runtime matching does not prefer one candidate merely because it has
parentheses; this policy governs learning justified regions.

The observed `<PARAM>: <PARAM>, near line: <LOCATOR>` has no positive boundary
evidence from its adjacent punctuation, and removing both proposed fields leaves
no independent diagnostic wording. It must not become viable merely because its
captures consume the native messages.

First propose boundaries without assigning their correctness. Then evaluate raw
region values, token-length variation and type evidence within the independently
comparable complete messages. A boundary or a failed KEY/LOCATOR check does not
establish PARAM. Equal observed lengths do not veto a supported variable span.

For every empirical PARAM, save the exact outside literal spans and native member
comparisons supporting its context. Assess all proposed variable spans simultaneously:
the contents of field B cannot support field A while B itself is a variable proposal.
If their removal leaves no shared diagnostic wording, reject the combined proposal.

Whenever alignment, field coalescing, a merge or a split changes a supporting
literal span, invalidate dependent field assessments and revalidate the complete
candidate. Do not reuse old `supported=True` flags. Accept the revision atomically
only when all affected fields still have independent context. Otherwise preserve
the earlier justified formulation or split the evidence; retain the failed witness.

This permits a PARAM at the beginning of a message when diagnostic wording later
in that same message supplies context. It does not require wording on both sides,
whitespace inside PARAMs, or fixed token ordinals.

### 3. Preserve diagnostic wording without freezing PARAM interiors

Track which literal spans were stable across distinct corresponding variable
values in independently comparable messages. A proposal covering those spans
must provide native counterevidence showing a variable region in the same outer
diagnostic context. Broader matching and union-pool variation are not that evidence.

Words repeated *inside* an independently justified PARAM may remain in its values,
but repetition supplies no positive evidence for that field. Substantial stable
wording must prompt examination of whether the proposed region has swallowed
diagnostic text; retain or narrow the region according to the complete-message
evidence, not according to its previous PARAM assignment.
Conversely, enclosing diagnostic wording in parentheses does not make it freely
erasable. Ownership of a span must follow its demonstrated context and field
boundaries, not a vocabulary or punctuation-only exemption.

Existing owner-declared traces/reasons retain their explicit structural authority.
Their interiors never support discovery of other fields. Do not relabel a weak
empirical candidate as a declared field to bypass these checks.

### 4. Merge on matching diagnostic wording

Within the same source and compatible construction, require corresponding
diagnostic words to match before proposing a union. Prefer formulations of the
same message that retain more independently supported matching diagnostic wording
over those that explain less wording by replacing it with fields. Compare wording
in its message context and order, not an unordered bag of recurring words.
Locations, their labels, punctuation and variable-field contents add no positive
weight. Literalized names or values do not become diagnostic evidence merely
because they increase a candidate's word count.

For example, the existing native `Unknown trigger` and `Unexpected token`
formulations retain diagnostic wording; the broad two-PARAM candidate retains
none. Consuming both groups cannot outweigh this loss. This is a learner grouping
and merge preference, not a new runtime tie-break that legitimizes a bad candidate.

Before joining member pools, establish a valid trigger and independent diagnostic
correspondence outside the proposed fields. Then propose a joint pattern. Finally
validate all members, dependencies, preserved wording, types and actual captures.
Re-inference on a combined pool is the last validation stage, not permission to
combine unrelated evidence in the first place.

Keep evidence aggregation for exactly identical executable patterns. All other
unions—including same-wording/different-slot patterns and merges exposed by a
previous merge—use the same acceptance path. Reprocess only decisions affected
by changed members or context; do not run unconditional whole-pool absorption
twice. A failed union does not discard messages or force a winner in matching.

## Location introductions: explicit matching change

Current `owner_rules.json.location_label_equivalences` recognizes introductions
before independently recognized LOCATORs. The learner currently emits separate
exact literal formulations; the ordinary matcher still compares literal text
exactly. That does **not** implement general runtime equivalence of the labels.

Proposed behavior: retain recognized label spans and their declared family as
structural metadata. `near line:` and `line:` satisfy the same required introduction
at that position; original token pieces, spacing and byte ranges remain attached
to the actual record. Missing or incompatible introductions remain structural
discrepancies. Neither introduction contributes diagnostic similarity. Recognition
is scoped to actual location fields outside opaque PARAM/REASON contents.

For runtime acceptance of either approved spelling, the model/matcher contract
must explicitly support this required structural-label alternative at that span.
It must not silently rewrite input, make `near` an OPTIONAL_KEY, or introduce a
general optional-literal feature. Matching returns the actual label span so exact
reconstruction uses its native spelling. The proposal includes auditing both
learner and pipeline matching consumers before selecting the representation and
versioning its interface. Do not claim runtime equivalence by changing only the
learner's grouping or by silently emitting unseen native examples.

## Native validation plan

Use the exact v30 ten/thirty selections and original complete logs. New learner
identity, fresh registries, no imported templates; keep the production pin unchanged
during evaluation. Compare v30 and revised inference, plus ten versus thirty under
the revised learner, on identical native messages.

Report actual source/message, raw pieces, templates, captures, outside supporting
wording, rejected proposal reason and occurrence versus independent-example counts.
Choose examples by changed formulation, not repeated timestamps/locations.

- `Unknown trigger` and `Unexpected token`: verify stable diagnostic wording and
  correctly typed values survive; inspect the union rejection, not only output names.
- Key-reference empty/present cases: preserve real OPTIONAL_KEY behavior; a brace
  must not provide evidence for the broad PARAM formulation. Its separate anomaly
  treatment remains explicit rather than manufacturing a valid KEY.
- Character descriptions, names and mesh spans: reassess boundaries, corresponding
  values and raw token lengths. Check whether each PARAM is genuinely justified
  or has absorbed diagnostic wording. Repeated internal words are not an acceptance
  target or positive similarity evidence; punctuation-separated values remain
  eligible for evidence-based assessment.
- Texture paths: retain recognized location structure despite the blank-path outlier;
  report whether field-outlier handling still requires a separate correction.
- Location introductions: inspect actual existing native label variants and missing
  introductions. If no native case exercises a proposed discrepancy, say so; do not
  fabricate one. Check native spelling/ranges and complete reconstruction.
- Every changed formulation: report both gains and regressions, ambiguity and
  unsupported decisions in each cohort (original ten and additional twenty). Full-match
  totals do not establish semantic correctness. Preserve adverse results for review.

Remaining uncertainties: exact structural-label serialization and consumer impact;
ambiguous attribution of an unmarked repeated phrase to diagnostic context versus
a field interior; separating genuine field changes from malformed outliers; and
how conservative acceptance affects short/rare formulations. These require native
evidence, not another list of presumed literals. This proposal does not claim to
resolve them before execution.
