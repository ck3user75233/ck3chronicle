# Mini-project 1.1 — Define direct contracts and record interfaces

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the stage coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md).
This prompt defines the implementation scope and deliverable; preparing it
does not authorize running it.

## Outcome and entry

Define the direct contract and record interfaces consumed by all following
mini-projects. Start with the definitions and field inventory in WORKPLAN
1.1–1.5; do not derive product units from existing database tables.

Read the cited sources directly:

- [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md:89) 89–105 / 108–146.
- [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277.
- [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:118) 118–153 / 166 / 176–211.
- [docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md:205) 205–254;
  `error_type` is defined at 217–218 and slot roles at 219.

## Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/__init__.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/domain.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py`

Edit: none.

Delete: none.

Record the entry state and perform the master's changed-file scope proof at
exit. Other new-package files belong to their named mini-projects; an interface
correction returns to that owner before dependent work continues.

## Existing representation evidence to inspect

| Exact source | What it establishes |
|---|---|
| [src/ck3chronicle/parser/log_blocks.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:26) `TimestampedLogBlock` 26–46; `_make_block` 101–139 | Existing emission fields/provenance; raw decoded text alone is insufficient for native-byte preservation. |
| [src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:28) `ClassificationResult` 28–41; `Classifier.classify` 84–208 | Existing structural outcome and slot result shapes. |
| [src/ck3chronicle/classification/contracts.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:22) `ValidatedSlot` 22–35; `TemplateValidation` 38–42 | Typed match results; the matcher body is ported in 1.3. |
| [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:24) `LayerContracts` 24–35; `ModelCluster` 38–52; `_load_cluster` 86–138 | Current supported structural fields and optional layers. |
| [models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1) | Concrete current entries and their actual fields. WORKPLAN 1.3 lists three exact null-layer cluster IDs. |

The selected artifact has 891 clusters: 240 with layer metadata and 651 without.
It has no complete direct `error_type`, identity and rendering definition, and
no per-cluster provisional/status/confidence field. These absences are definition
gaps to resolve precisely, not authorization to manufacture values.

## Implementation steps

1. Keep the package initializer inert. In `domain.py`, define `Emission`,
   `RecoveredDiagnostic`, `ClassificationOutcome`, `DiagnosticRecord` and
   `RunResult`, plus the concrete span/locator/binding values they need.
   Define actual data interfaces used by the following prompts, not placeholder
   service functions.
2. Specify an emission's original-byte span, source/header facts, order and
   original content access. A recovered diagnostic carries its parent emission,
   child boundaries and original-value ownership. A normalized match view
   retains enough token-to-original correspondence for typed slot binding.
3. Specify structural assignment separately from eligibility for an approved
   compact record. Preserve the proven `full/l1_l2/l1/unknown` distinctions.
   L1-only can form a record only as permitted by its approved L1 contract;
   retain unresolved native evidence according to the applicable routing rule.
   Similarity is not an approval or probability field.
4. In `contracts.py`, define `ErrorContract`: source/template identity and
   revision, supported layer structure, typed roles, direct error type,
   identity fields and rendering definition. Make requirements explicit enough
   that 1.3 can reject a malformed direct artifact and 2.1 can aggregate/render
   without another mapping layer.
5. Define `DiagnosticRecord` around WORKPLAN 1.2 / Trusted Run 255–277:
   Run association, contract/revision, assignment, direct type, concrete
   identity/slot/locator fields, stored stable rendering, count and first/last
   observations. Define the processing/Run result fields required to account
   for recognized emissions, recovered diagnostics and review metadata without
   calling unresolved native emissions diagnostic records.
6. Produce a field-authority inventory in the handoff. For every required
   direct-contract rule, cite its established source by exact artifact entry or
   document lines. List specific missing/changed definitions separately, with
   the affected entry/field and proposed decision. The inspected sources do not
   contain an exhaustive approved error-type index; do not claim one exists.
7. Make the implemented types and exact definition choices reviewable before
   downstream code depends on an unresolved rule. Existing approved definitions
   retain their approval. Projection rows and extractor categories have no
   blanket authority to fill missing fields.

## Deliverable and following work

Deliver the three scoped files and the cited field-authority inventory in the
completion message. Record agreed signatures/data shapes and each exact open
rule. Mini-project 1.2 consumes original-byte/child-span interfaces; 1.3 adds
the matcher and direct loader. Mini-project 2.1 consumes the complete record,
identity and review-result contract.

A missing necessary rule is a focused owner decision, not a general request
to review all contract candidates. Continue independent interface work while
that decision is pending. Finish with the required file-scope proof. This
mini-project does not create a new runtime model artifact.
