# Learner task: deterministic template assignment for pipeline storage

## Objective and ownership

Implementation checkpoint, 2026-09-26: learner v38 delivers retirement and one
selected body/wrapper assignment in review candidates, with native ten/thirty
verification. See LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md. Publication and
pipeline adaptation remain pending; the older selected-model audit below is
historical context, not a claim that development candidates lack competitors.

Deliver a model-backed assignment policy that lets the pipeline obtain **one
selected template and one complete set of bindings per matched error message**,
including provisional matches. Resolve how a #1 assignment is established when
several candidates or capture assignments are possible.

You own learner/model changes and publication. The pipeline team consumes the
published contract and owns pipeline adaptation, aggregation and SQL. This task
does not authorize changes to pipeline source or application/database processing.

## Owner decisions to preserve

- A **diagnostic record** is the refined, unique error message stored in SQL.
  Parsing supplies message pieces and spans; template assignment supplies literals,
  slot placements and values. SQL storage consumes that result without rematching.
- Identical matched content within a Run aggregates into one record with an
  occurrence count. Different slot values form different records. Emitting-source
  applicability belongs in template assignment, not a second aggregation check.
- Both template and provisional matches belong in SQL, distinguishable by a
  match-status field. Reports normally include both and can filter either.
- SQL needs the selected template's literals/slot placements and the corresponding
  bindings. It does not need competing-template lists or individual occurrence
  timestamps. Model/parser/processing lineage belongs in Run metadata.
- Messages with no template assignment go to the native review shard. Error type
  can remain `unknown`. Learning from provisional evidence remains learner-owned.

## Current integration evidence

Start with [the current learner handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) and
`models/selection.json`. Current selection is `a9fa27a85ccd066285b99fdb`, schema 3,
with pinned parser `ck3-lossless-v1.6`.

2026-09-25 update: current selection is now `0a61f6c93657948e0ca20b35` (v29).
The v27 reference above is the historical starting point. The read-only
[selection review](LEARNER_SINGLE_ASSIGNMENT_REVIEW.md) replays the saved native
inputs for all 73 logs with v29: no competing templates or ambiguous captures.
It provides verified historical multi-match examples and recommendations;
the selection implementation/publication outputs below remain outstanding.

The pipeline currently enumerates complete source-applicable template/capture
matches. It has no ranking policy. Its `provisional` result covers both a unique
match to a provisional template and competing templates/ambiguous captures.
Candidate order does not establish a #1 assignment. See
[classifier.py](../src/ck3chronicle/pipeline/classifier.py).

The latest six-log pipeline replay observed unique provisional matches and no
competing assignments. Thus this is an unresolved consumer-contract question,
not an established claim that the selected model has competing matches.
[Replay evidence](../.ck3chronicle/wip/reports/p1-spot-check-a9fa27-20260924/native-verification.json)
and the handoff's ten-log replay provide genuine starting material.

## Required outputs

1. **Native evidence audit.** Establish what provisional means in the current
   model and whether real retained messages have multiple eligible templates,
   multiple binding assignments, or ties between supported and provisional
   templates. Report actual examples with paths, hashes and spans, or state that
   none were observed and identify the inspected corpus.
2. **Deterministic selection contract.** Define how the selected assignment is
   obtained, including precedence, capture-boundary ambiguity and ties. Explain
   the evidence supporting any preference; arbitrary iteration order or an ID
   sort does not establish a better match. Identify proposed policy decisions
   requiring owner direction. A supported/provisional label describes the
   selected template's support status; explain separately whether selection
   itself was decided. Owner 2026-09-25 correction: competing provisional matches
   require exactly one production winner. Use evidence-based ranking and a
   deterministic final tie-break; report the tie-break honestly without claiming
   it establishes semantic superiority. Do not turn competition into unknown.
3. **Published consumer output.** For an assigned message, supply the selected
   template ID, template/provisional status, complete ordered slot bindings
   (types, values, native spans and placements), and all applicable literal
   layout references. Include existing enclosing file/line content in that
   layout/binding result where applicable. Define the exact interface and how
   support statuses map to the two reporting statuses. The pipeline must be
   able to reproduce selection using the immutable release and pinned parser,
   without mutable learner code or another pipeline-authored ranking policy.
4. **Delivery and verification.** If artifact changes are needed, publish a new
   immutable revision with hashes and selection-policy versioning; retain prior
   release bytes. Update the existing learner handoff with the policy, exact
   artifacts, interface changes and pipeline adaptations required. Compare old
   and new assignments on complete retained logs; account for every message and
   verify selected literals/bindings reconstruct the original content. Include
   human-readable changed examples and explicit coverage gaps.

Preserve the current six slot types (KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM,
REASON), complete native literals, pinned-parser boundaries and corrected trace
LOCATOR/PARAM bindings. Additional slot types require owner direction. Derive
requirements from owner instructions and evidence from genuine captured logs;
use no synthetic inputs, altered witness templates or test-file requirements.

**Completion:** the pipeline can persist the single returned assignment and its
status whenever an eligible complete candidate exists. Messages with no eligible
complete match go to review. No unresolved selection decision is delegated to SQL.
