# Learner task — deliver the shared, model-pinned matcher

## Outcome and scope

Extract the learner's matching mechanics into one reusable implementation, use it
in the learner, and deliver an immutable package that the pipeline can load with
the model and parser. The pipeline will replace its separate matcher with this
component. This is an implementation and delivery task.

Own the learner extraction, caller changes, packaging and native verification.
Pipeline reader/classifier/binding integration and removal of the pipeline's
duplicate matcher belong to the pipeline team. Deliver a verified candidate
package and proposed selection metadata; keep the active model selection unchanged
until the pipeline reader supports the new package. Production ingestion,
application cutover and SQL implementation remain outside this task.

## Authority and starting point

Read repository and learner AGENTS.md instructions, current project status and
handoff, then:

- [Approved Error Contract](ERROR_CONTRACT_SPECIFICATION.md).
- [Current learner delivery](LEARNER_PARSER_PIPELINE_HANDOFF.md).
- [Native model contract](LEARNER_NATIVE_MODEL_CONTRACT.md).
- [Pipeline audit](04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md), as implementation
  evidence rather than authority for product requirements.

At prompt preparation, `models/selection.json` selects
`76630685c4a341ca14bf9c7c`, schema 4, parser `ck3-lossless-v1.7`, assignment policy
`complete-assignment-v2`. Verify the actual starting selection and hashes.
Later owner decisions govern over historical L1/L2 and provisional-to-review rules.

Inspect `research_matching.py`, `patterns.py`, construction/parameter/full-ID
helpers, `assignment.py`, `continuations.py` and `publish_native_model.py` under
`tools/template_learning/`. Compare the current pipeline interfaces read-only.

## Required implementation

1. **One matching implementation.** Extract complete literal/slot matching,
   source/structure applicability, declared constraints, wrapper matching and
   complete capture alternatives. Connect the existing continuation matcher and
   winner selector through the shared entry point. Learner evaluation, publication
   validation and inference callers that test a proposed pattern must use these
   same matching primitives. Keep template inference and evidence generation in
   their existing learner owners. Remove superseded learner matching bodies and
   update their callers; retain no independent fallback matcher.

2. **Explicit inputs and pinned dependencies.** Matching uses supplied templates,
   model declarations and selection evidence, plus native regions/pieces from the
   pinned parser. Extract matching dependencies from modules that also perform
   inference. The delivered runtime component must load independently of the
   learner checkout, its mutable rule files, registries and research state. Cover
   every executable matching dependency, including full-ID mechanics, with release
   hashes. Use the same implementation for unpublished candidates and published
   models through explicit inputs.

3. **Complete native matching.** Support exactly the currently owner-approved
   types: KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM, REASON, CHARACTER_FULL_ID,
   HOUSE_FULL_ID and TITLE_FULL_ID. Preserve complete literal text, punctuation,
   whitespace, optional absence versus present empty content, opaque full IDs,
   required surrounding regions and ordered supporting entries. Use declared slot
   boundaries and constraints without independent message rewriting or semantic
   classification. Error typing remains `unknown` downstream.

4. **One selected assignment.** The public operation accepts a loaded model and
   one complete recovered native unit: source/emitter, context kind, original body
   text/pieces, required wrapper regions and ordered continuation regions. It
   returns one complete selected assignment with final `template` or `provisional`
   status, or an explicit no-match result. Internal eligible alternatives feed the
   existing selector; retain its deterministic provisional tie handling. Research
   alternatives may be an explicit opt-in inspection output, separate from the
   ordinary result. The component does not create absolute occurrence bindings.

5. **Usable result contract.** Return selected template ID, selected wrapper and
   component layout references, ordered component indices, and ordered captures
   with slot identifier, type, exact value, presence and region-relative byte span.
   Define the offset origin for every region and absent/empty representation.
   Layout references must identify the actual selected literal layout so the
   pipeline can render without matching again. Preserve caller-owned provenance
   associations. Return explicit integrity/compatibility/declaration errors for
   invalid models or inconsistent results; ordinary no-match remains distinct.
   Document native recovery limitations separately.

6. **Immutable delivery.** Extend publication and loading to cover matcher API
   version, implementation hashes and parser/model/selector compatibility. Supply
   a candidate manifest and runnable minimal loading/invocation example. Existing
   releases stay immutable. Preserve current template definitions, IDs, support
   evidence and selection policy during this extraction; any discovered semantic
   defect or unavoidable change needs an explicit native-evidence explanation.
   Relearning or policy redesign is a separate task.

## Verification

Use the repository Python environment and complete, unmodified native CK3 logs.
Requirements come from owner direction: use no synthetic inputs, fabricated
templates, altered native witnesses or historical test expectations.

Establish a fresh baseline before edits. Replay all accessible complete logs
supporting the selected release, plus available additional logs used in the
current handoff, including continuation-bearing inputs. Record hashes, provenance
and unavailable evidence. Parse afresh with the pinned parser.

Compare the learner before/after extraction and the independently loaded candidate
package on equivalent models and native inputs. Read-only execution of the current
pipeline can identify integration differences; it is not the correctness oracle.
Check eligibility, complete captures, selected templates/layouts, final statuses,
wrapper/component completeness and exact correspondence to original bytes. Explain
every difference rather than treating increased coverage as success. Verify that
ordinary result production does not bind losing candidates or bind a winner twice.

Exercise package loading without learner source/rule imports. Report native
coverage gaps explicitly, including slot types, ambiguity/ties, empty fields or
failure paths without genuine witnesses. Keep generated evidence ignored.

## Handoff to the pipeline team

Update [LEARNER_PARSER_PIPELINE_HANDOFF.md](LEARNER_PARSER_PIPELINE_HANDOFF.md)
with a concise current delivery section containing:

- Exact candidate location, manifest hash, model/parser/matcher identities,
  dependency hashes and proposed selection metadata; distinguish delivery from
  activation.
- Callable loading and matching interfaces, input/result/error schemas, offset
  conventions, and a runnable example using an identified complete native log.
- Changed and retired learner paths, remaining matching callers, verification
  counts and human-readable native examples with templates, selected captures
  and statuses; include unmatched evidence where present.
- Explicit pipeline actions: load and verify the package, replace local matching
  with the shared entry point, bind only the selected assignment once, preserve
  final status, and retire the superseded pipeline matcher after native verification.
- Remaining limitations or dependencies, with evidence links.

The delivery is complete when the learner uses the shared mechanics and the
pipeline team can independently load the candidate package and obtain complete
selected assignments without importing learner development code or implementing
another matcher.
