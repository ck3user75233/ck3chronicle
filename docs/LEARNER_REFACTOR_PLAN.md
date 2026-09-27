# Learner refactor after shared message recovery

Date: 2026-09-20. Proposed implementation sequence; this document does not
record implementation or authorize model promotion/production processing.

## Implementation checkpoint

The owner subsequently authorized this plan and directed source-by-source
learning. The structural refactor is now implemented; see the
[delivery review](LEARNER_REFACTOR_REVIEW.md) for actual native evidence,
candidate output, remaining model-quality issues and pipeline responsibilities.
The native corpus confirms source-specific message/token sequences; no
cross-source template comparison is part of this work. The sections below
preserve the implementation sequence, not a claim that every candidate's
semantics have been accepted.

At the planning baseline, the parser was implemented and verified against native
evidence. The immediate problem was in the learner: its collector used whole emissions, while
the parser can return several individual messages from one emission. Learning
from the whole emission would combine unrelated sibling errors and give their
wrapper an accidental role in the template.

The [100-case comparison](../.codex-tmp/parser-100-review/INDEX.md) supplies the
current input review. It includes the exact serialized parser emission nodes,
previous pipeline outputs and separately identified former learner inputs.
The [parser specification](LEARNER_PARSER_SPEC.md) defines the raw boundary;
the [formal reply](LEARNER_PARSER_PIPELINE_HANDOFF.md) assigns runtime migration
to the pipeline team. This plan addresses the learner side of
[A1–A7](LEARNER_MODEL_DEPENDENCIES.md), followed by the identified model research.

## What is already connected, and what is not

- `evidence.read_evidence` loads an explicitly selected parser. The registry
  includes its reference in feature/build identity. These connections remain.
- `collect_records` groups emission tokens by source and records emission-level
  occurrences. The feature cache declares `record_scope: "emission"`. Both
  must change together; changing the iterator alone would leave misleading
  provenance and stale cache semantics.
- Clustering, alignment, medoid selection and slot/template inference already
  live in `learn_error_templates.py`. They are genuine learning work to retain
  and revise in learner modules. They are not functions to move out of the new
  parser. The historical `normalize_key_path` was also learner-local.
- Occurrence-weighted medoid scoring and frequency-based ordering still allow
  repeated bursts to affect learning despite record deduplication. Slot
  heuristics still admit `ALT`; complete native slot/layer export is unfinished.
- The current parser does not identify KEYs, PARAMs or L1/L2. Those are model
  responsibilities. The runtime inspector is outside this work.

## 1. Establish message records and the model boundary

Implement learner-owned records for recovered messages. Each occurrence carries
evidence identity, emission ordinal, message ordinal and exact message span.
Retain a reference to the parent emission/shared ranges; keep parser identity
once in dataset/model metadata. Preserve every occurrence for inspection, while
grouping distinct message forms for learning. Unknown recovery shapes retain
their native unresolved ranges and reason in research output; they do not become
invented single-message training records.

Read `emission.recovery` once per emission and iterate its messages. Obtain each
message's own pieces through its API. Do not filter whole-emission tokens by
containment: the reviewed expansion annotations include a punctuation token
that crosses a message boundary.

The proposed model contract has an ordered native message pattern and an
explicit associated-context description. The latter refers to the enclosing
wrapper when present, so its filename and location remain available to the
consumer without concatenating sibling messages. Header and separator bytes
remain parser framing. For wrapped messages, the learner must describe any
shared wrapper literals/slots needed by matching and capture; silently excluding
the filename because it is outside the child span is not acceptable. For an
ordinary multiline error, its trace and location tail remain inside its message
pattern. This is a framing/context distinction, not an invented universal L1/L2
format.

Owner clarification: these references serve raw evidence and model application;
they are not the proposed SQL layout. The consumer must assemble a complete
diagnostic, including its applicable wrapper context, before within-Run
deduplication. Store all content needed to understand that diagnostic with the
diagnostic. Verbatim repeats at different timestamps become occurrences against
one entry. Do not introduce a parent-emission lookup to recover required
diagnostic content, or use child text alone to merge errors whose relevant
context differs. Repeating common context across distinct diagnostics is
acceptable. Research range references may remain as provenance.

Deliver the record shape, a proposed model schema and genuine resolved examples
before rebuilding the corpus. Coordinate that concrete schema with the pipeline
handoff: message scope, context references, slot capture ranges, source
applicability, parser reference and trailing-content representation must agree.
The pipeline team implements its reader/matcher changes.

## 2. Separate the learning stages into their owning modules

Keep `learn_error_templates.py` as the direct CLI/orchestrator. Use small owning
modules under `tools/template_learning/` for:

| Stage | Responsibility |
|---|---|
| Native records/features | Message collection, deduplication, context/occurrence references and unresolved evidence |
| Clustering/alignment | Existing sequence comparison, clustering, medoid selection and alignment, with explicit evidence weighting |
| Template inference | Literal/slot decisions, source-applicable L1/L2 composition and complete native coverage |
| Candidate export/review | One model/manifest serializer and native-example review output shared by direct and registry builds |

Move useful algorithms without silently preserving their old transformations.
Remove unused masking, suffix rewriting, alternate tokenization and unsupported
slot-generation paths as their callers are replaced. Review imports of the
affected learner helpers and update or remove the research tools that actually
need them. Do not introduce compatibility shims. No separate parser copy or
model-aware parsing enters these modules.

## 3. Derive complete native patterns and the five slot types

Carry native ranges and gaps through alignment. Preserve literal order,
punctuation, repetition and suffixes. In particular, remove inference behavior
that collapses adjacent equal literals merely because they are equal. Any
variable region must be explicit in the model; no hidden downstream cleanup.

Use only KEY, OPTIONAL_KEY, PARAM, LOCATOR and VALUE. Learn whole continuous KEY
values, including dotted/numeric strings; lexical edge punctuation is not an
automatic key boundary. Span-based captures can include part of a lexical piece
or several pieces. PARAM boundaries come from surrounding native template
structure. Keep `, near line:` literal when only its location value varies.
Document optionality and actual constraints; do not invent constraints from a
restricted identifier alphabet.

Infer L1/L2 only for the applicable failure/reason constructions and retain them
within one error message. Support independent L1 assignment and reusable L2s
with their native relationship and trailing content represented. Do not treat
every bracket pair or multiline message as an L1/L2 contract. Ambiguous examples
remain visible research gaps rather than forced structures.

## 4. Remove repetition bias and inspect known inference defects

Use distinct native message variants as the evidence for generalization, with
occurrence totals retained separately. Revisit both medoid weighting and
cluster ordering; deduplicating the input list alone does not remove their
current occurrence weighting. Compare results when replaying the same native
occurrences again to expose burst sensitivity.

Inspect the specific examples identified in the dependency handoff: fixed
event-prefix overfitting, localization KEY-as-PARAM, the extra KEY before
`expected`, and travel/name phrase boundaries. A majority shared namespace
among distinct keys is still not proof that its prefix is literal. Use native
evidence to justify a generalization or leave the candidate unresolved; do not
optimize for complete attribution. Broader naming research follows the complete
native model connection rather than blocking its record/format work.

## 5. Rebuild feature storage and candidate artifacts coherently

Change feature scope/version and validation to the new message record contract.
Re-extract from native evidence for the selected parser; reject incompatible
caches without migration or fallback. Keep explicit parser version, retrievable
artifact and exact implementation digest in build identity and the model.

Make registry and direct builds use the same model serializer. Export one
immutable candidate revision with native patterns, five-slot definitions,
source applicability, template identifiers, context/L1/L2 structure, provenance,
hashes, reproduction command and a visible owner-override list (empty if none).
The artifact is a research candidate until reviewed and integrated; creating it
does not select or promote it into production.

## 6. Inspect real results and hand off the model

Use genuine logs, Python anomaly inspection and readable before/after examples.
Verify message counts against selected-parser recovery, provenance back to
native bytes, complete literal/capture coverage and retention of all unresolved
evidence. Inspect message variants, repeated bursts, long PARAMs, dotted/numeric
KEYs, present/absent OPTIONAL_KEYs, location suffixes, traces and L1/L2 reuse.
Do not manufacture expected classifications from old fixtures.

Supply the pipeline team a candidate bundle and actual examples with template
IDs, captures, native spans, context and unresolved outcomes. The pipeline team
owns loading/classification/SQL integration and its runtime checks; review its
results jointly against the native evidence. Include a wrapped multi-error
example demonstrating complete stored diagnostics, with their common filename
available on each diagnostic, and a repeated-error example demonstrating one
within-Run diagnostic plus occurrences at different timestamps. Neither report
should depend on an emission record or reopening the raw log.
Parser reconstruction is already
demonstrated and does not by itself establish model correctness.

After this structural delivery, continue the dependency handoff's separate
research on naming boundaries, deterministic error typing and incomplete
historical evidence. Error-type hierarchy and new slot types require the
owner's direction; this refactor does not invent either.

The first planned implementation deliverable was **message-based learner
records plus a concrete model/context contract**, followed by the stage
separation and inference work above. Preparing the original plan and 100-case
comparison performed no training or registry updates. The subsequently
authorized implementation and isolated candidate build are documented in the
delivery review linked at the top; production processing and promotion remain
outside this work.
