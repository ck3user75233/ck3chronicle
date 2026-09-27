# Mini-project 1.3 — Build runtime classification and the direct model

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the stage coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md).
This prompt defines the implementation scope and deliverable; preparing it
does not authorize running it.

## Outcome and entry

Consume 1.1's direct contract rules and 1.2's original-value matching view.
Construct the selected direct model and runtime classifier. Production loads
the completed approved artifact; this task does not invoke the learner.

Read WORKPLAN 1.2–1.4 and section 7 before changing the artifact format.
A structural match does not by itself supply a missing direct error type,
identity or rendering rule.

## Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/model.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/catalog.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py`
- `C:/Users/nateb/Documents/ck3chronicle/models/<new_revision>/empirical_template_model.json`
- `C:/Users/nateb/Documents/ck3chronicle/models/<new_revision>/manifest.json`

Edit only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py` — add R5 typed validation and binding results to the 1.1 interfaces.
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py` — set the single shared normalization identity used by the new artifact; grammar changes return to 1.2.

Delete: none.

Record the entry state and perform the master's changed-file scope proof at
exit. Other new-package files belong to their named mini-projects; an interface
correction returns to that owner before dependent work continues.

Resolve the content-derived `<new_revision>` and record both actual artifact
paths before writing. It is the only variable component in this create list.

## Exact source ports

| ID | Existing source and scope | Destination and treatment |
|---|---|---|
| R5 | [src/ck3chronicle/classification/contracts.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:22): `ValidatedSlot` 22–35; `TemplateValidation` 38–42; `_literal_equal` 45–50; `_closed_alternatives` 53–59; `validate_template_tokens` 62–146; imports/constants 1–19 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py`: port exact literal/typed-slot matching and ambiguity rejection. Extend the new direct contract/binding result under N1/N2. Similarity never substitutes for typed validation. |
| R6 | [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:24): schema/version constants 14–17; `ModelIntegrityError` 20–21; `LayerContracts` 24–35; `ModelCluster` 38–52; `EmpiricalModel` 55–64; validation helpers 67–138; `load_model` 141–191. [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:25): `_approved_revision_root` 25–45; `approved_model_path` 48–49; `load_approved_model` 56–57; `load_approved_classifier` 76–77 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/model.py` and `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/catalog.py`: port immutable hash/integrity checks, supported direct-contract structures and explicit source/install artifact lookup. Adapt to one current format. Keep one current normalization-version identity shared by the pure grammar and artifact readers/writers; do not preserve conflicting copies. Bind the new catalog to the prepared direct artifact in 1.3; application/package selection activates it in 3.2; omit projection pins/loaders and old-format support. |
| R7 | [src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:28): `ClassificationResult` 28–41; `_similarity` 44–55; `_ordered_anchor_overlap` 58–63; `_composed_id` 66–68; `Classifier.__init__` 74–82; `classify` 84–208; `_result` 229–255 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py`: port source partitioning, runtime candidate comparison, exact typed matching and layered result mechanics. Adapt to recovered diagnostics and N1 outcomes; remove dual lead lookup at 89. The old `classify_block` 210–227 is not ported: recovery is explicitly composed by the processor and learner evidence collector. |

## Artifact inputs and current selection

- [models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1) and
  [models/67303093ecda779d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/manifest.json:1): existing selected structures
  and their provenance. Both are read-only inputs to this mini-project.
- [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:13) 13–16: current
  artifact selection; 25–45: source/install resource lookup to port.
- [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) 29–34: current packaging, changed only in 3.2.
- 1.1's per-field authority inventory: established direct rules and resolved
  decisions. The projection catalog is not an automatic contract conversion input.

## Implementation steps

1. Port `validate_template_tokens` and its exact literal/typed-slot/closed
   alternative mechanics into the new `contracts.py`. Connect successful
   typed slots to the original-value bindings supplied by 1.2. Ambiguity or
   failed validation cannot authorize a compact diagnostic record.
2. Implement `model.py:load_model` with one direct format and its integrity
   checks. Validate the structural and direct fields together, including the
   contract's identity and rendering requirements. Resolve model/contract
   revisions without importing the old loader or projection catalog.
3. Port `Classifier.__init__`, `Classifier.classify` and its named matching
   helpers into `classifier.py`. Preserve source partitioning, runtime
   candidate comparison and exact typed validation. Candidate similarity
   ranks structures; it never substitutes for a valid contract.
4. Preserve the supported whole-template and optional L1/L2 mechanics described
   in WORKPLAN 1.3. Remove old dual-lead lookup at inference.py 89. Consume
   recovered diagnostics rather than porting `classify_block`; the processor
   will explicitly compose recovery and classification.
5. Return the direct `ClassificationOutcome` from 1.1, including bound
   concrete fields where authorized and explicit unresolved routing where
   necessary. Do not add provisional flags or a confidence threshold absent
   an owner-defined operational rule. An L1-only outcome remains an exact L1
   classification with unresolved L2.
6. Prepare the direct model content from established structures and direct
   definitions. Retain their approval; identify a truly new/changed rule by
   exact entry before relying on it. Remove projection references and sample-
   absence defaults. Produce the one current model JSON and manifest with the
   content-derived identity and shared normalization identity.
7. Where changed tokenization/splitting invalidates an old normalized feature,
   state the affected entry and required regenerated structure. Do not silently
   relabel old features with a new normalizer version. No fixed cluster count,
   wholesale training campaign, or preservation of every old result is required.
   If needed evidence/approval is missing, hand off that concrete dependency
   rather than auto-running learning.
8. Implement `catalog.py` source/install lookup and approved model/classifier
   loading for the new artifact. Pin this new package's catalog now. The existing
   application and package-resource selection activate it only in 3.2, when
   both superseded active revisions are removed.

## Deliverable and following work

Deliver the new classifier, direct loader/catalog, typed validator, shared
normalization identity and two resolved artifact files. Record the exact
artifact hash/revision, source of direct rules, supported outcomes and the
entry-level treatment of any changed normalized structures.

Stage 2 must be able to consume approved fields for rendering/aggregation
without a projection or classifier payload reread. Report any unresolved
contract rule as incomplete work; do not manufacture an approval state to
finish the artifact. Finish with the required file-scope proof.
