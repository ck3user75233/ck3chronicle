# Classification pipeline replacement — complete prompt review copy

Prepared: 2026-09-13.

This document combines the master orchestrator, all three stage coordinators
and all seven mini-project prompts for external review. The instructions below
are review material; this compilation does not execute or approve implementation.

The prompt text and model/effort recommendations are preserved. Heading levels
and links between included prompts are adjusted for navigation within this file.
Original checkout paths and source line references remain as supplied in the
individual prompts. The supporting workplan, dependency maps, governing documents
and product source are referenced but are not reproduced in this compilation.

## Contents

1. [Master orchestrator — classification pipeline replacement](#master)
2. [Stage 1 — Construct classification core](#stage-1)
3. [Mini-project 1.1 — Define direct contracts and record interfaces](#mini-1-1)
4. [Mini-project 1.2 — Port emission recovery and original-value binding](#mini-1-2)
5. [Mini-project 1.3 — Build runtime classification and the direct model](#mini-1-3)
6. [Stage 2 — Construct complete Run processing](#stage-2)
7. [Mini-project 2.1 — Build aggregation, Run storage and native review](#mini-2-1)
8. [Mini-project 2.2 — Compose protected inputs, processing and replay](#mini-2-2)
9. [Stage 3 — Connect application and retire old pipeline](#stage-3)
10. [Mini-project 3.1 — Build stored reports, audit and command handlers](#mini-3-1)
11. [Mini-project 3.2 — Switch application callers and retire the old pipeline](#mini-3-2)

---

<a id="master"></a>

## Master orchestrator — classification pipeline replacement

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: coordinate the three stages below, maintain the complete dependency view,
and require each mini-project's concrete handoff and file-scope proof.

Status: expanded prompt for owner review, 2026-09-13. Preparing this prompt set
does not execute it. When the owner commissions implementation, use this master
with the relevant stage and mini-project prompts.

### Governing objective and required reading

Build the production pipeline in
`C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/`, using the exact working-function ports and new
composition specified in [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md). Connect the application to that
package and delete the superseded providers in mini-project 3.2.

Read these definitions before deciding classification or storage behavior:

| Source | Required content |
|---|---|
| [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md:89) 89–105 / 108–146 | Product units, direct contracts, emission accounting, review evidence and original-log retention. |
| [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:118) 118–153 / 176–211 / 227–244 | Component ownership, native shards, fresh generations, offline authoring boundary and completion/retention. |
| [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277 | Contract-defined identity, typed fields, rendering, counts and interpretation lineage. |
| [docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md:205) 205–254 | Target vocabulary; `error_type` is the sole hierarchical diagnostic taxonomy. Technical analysis is subordinate to owner decisions. |
| [docs/BANNED_IDEAS.md](C:/Users/nateb/Documents/ck3chronicle/docs/BANNED_IDEAS.md:37) 37–87 | Removed designs and prohibited substitutes. |

Also read [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md), [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md),
[docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md) and [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md).
Current owner instructions take precedence over earlier technical proposals.
The dependency evidence is [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and [CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md).
Their existing-source ranges are locators; if lines move, use the named symbol
and reported diff to identify the same code. Scope does not expand with a search.

### Product definitions and flow

A Run is the successful processing result for one protected error log.
An emission is the timestamped native engine output including its continuations.
A recovered diagnostic is a transient child processing unit. A diagnostic record
is an approved compact SQLite identity within a Run.

The target flow is:

1. Copy completed-run evidence into protected pending storage.
2. Prepare an explicitly selected protected input and reject duplicate full-log hashes.
3. Recognize emissions and recover source-specific child diagnostics with original spans.
4. Compare each diagnostic to the selected approved model, validate typed contracts
   and bind concrete values once.
5. Aggregate approved identities; preserve review-routed original emissions.
6. Complete the Run's compact records and native-shard metadata.
7. Report stored records without reopening the original log or loading a model.

Use WORKPLAN 1.2 for the cited complete target field inventory. There is no
separate “classification meaning” entity. The current structural outcomes are
`full`, `l1_l2`, `l1` and `unknown` (WORKPLAN 1.3). L1-only is an exact
successful L1 assignment with unresolved L2. Optional layer metadata does not
prove that a structural model entry already has all direct-contract fields.

WORKPLAN 1.4 distinguishes canonical preservation policy from current model
state: no per-entry provisional/confidence status or calibrated threshold exists
in the selected structural artifact. Do not invent one from similarity scores.
Unresolved evidence is native emission content and metadata, not an unclassified
diagnostic record. Every recognized emission is accounted for; classification
coverage is not required to reach 100%.

One native shard belongs to each successful Run, including an empty shard.
The protected full original remains retained indefinitely. Production consumes
an approved artifact; it never runs the offline learner.

### Launch index and model defaults

Start each coordinating task with this master and the named stage prompt.
Each mini-project starts with this master, its stage prompt, its own prompt and
the preceding completion handoff. The master and stages do not execute the same
work twice: the active coordinator chooses the next incomplete child.

| Coordinating prompt | Model | Effort |
|---|---|---|
| This master | GPT-6 Astra | xhigh |
| [Stage 1 — Construct classification core](#stage-1) | GPT-6 Astra | xhigh |
| [Stage 2 — Construct complete Run processing](#stage-2) | GPT-6 Astra | xhigh |
| [Stage 3 — Connect application and retire old pipeline](#stage-3) | GPT-6 Astra | xhigh |

| Mini-project prompt | Model | Effort |
|---|---|---|
| [1.1 — Define direct contracts and record interfaces](#mini-1-1) | GPT-6 Astra | xhigh |
| [1.2 — Port emission recovery and original-value binding](#mini-1-2) | GPT-6 Astra | high |
| [1.3 — Build runtime classification and the direct model](#mini-1-3) | GPT-6 Astra | xhigh |
| [2.1 — Build aggregation, Run storage and native review](#mini-2-1) | GPT-6 Astra | xhigh |
| [2.2 — Compose protected inputs, processing and replay](#mini-2-2) | GPT-6 Astra | high |
| [3.1 — Build stored reports, audit and command handlers](#mini-3-1) | GPT-6 Astra | high |
| [3.2 — Switch application callers and retire the old pipeline](#mini-3-2) | GPT-6 Astra | xhigh |

These are task-specific recommendations, not measured quality guarantees.
The [official GPT-6 Astra documentation](https://developers.openai.com/api/docs/models/gpt-6-astra)
describes its reasoning/coding use and supported `high`/`xhigh` efforts.
Select the model and effort in the task's actual settings; writing a model name
inside a prompt does not change the active model. No global configuration change
is part of this project.

### Sequence and coordination

Stage 1 runs 1.1 -> 1.2 -> 1.3. Stage 2 runs 2.1 -> 2.2.
Stage 3 runs 3.1 -> 3.2. Keep each stage's required predecessor outputs explicit.

Treat stages as construction boundaries. Mini-project 3.2 is the connected
application activation and deletion change; no transitional public pipeline,
fallback, wrapper, old-schema reader or compatibility alias is commissioned.
Required behavior has a destination in the new package. Obsolete behavior and
its callers are deleted. The offline changes are precisely L1–L5 in WORKPLAN;
learner relocation, algorithm redesign and candidate-promotion redesign are
separate projects.

A coordinator has no additional file-writing scope. If it implements a child
itself, it works under that child's exact list and entry baseline. Cross-package
corrections return to the owning prompt with a new scope comparison. An out-of-list
change needs an amended instruction before mutation. Coordination does not
itself authorize creating tasks, spawning agents or parallel implementation.

### Mini-project entry, exit and source protection

At entry, read the predecessor's handoff and record the exact resolved create,
edit and delete lists and starting source state. Preserve pre-existing edits.
Source references are read inputs, not edit permissions. Resolve the two
content-derived model paths before creating them.

At exit, report each created, edited or deleted path and the scope entry that
authorized it. Compare against the entry state, including tracked, untracked
and ignored files and any explicitly authorized external output roots. An empty
`git diff` alone cannot establish this proof. Use read-only inventories and
content comparisons; do not build a new journal or status infrastructure.

Git history protects committed source. Uncommitted and untracked work requires
a recoverable baseline too. Do not reset owner changes or assume HEAD restores
the present planning files. No commit, push, runtime-evidence deletion or
production database operation is implied by implementation scope.

Each handoff includes: concrete interfaces and callers; ports versus new bodies;
source/contract decisions with evidence; completed file-scope proof; and the
specific input required by the next child. Report any unresolved question with
its exact field, caller or proposed behavior. Keep the handoff in the task
completion message; no extra receipt/status artifact is authorized.

### Focused owner reviews and separate verification

In 1.1, present the implemented types and per-field authority inventory. Only
a necessary missing or changed contract rule requires a decision before dependent
work uses it. Moving an established definition does not require blanket review
of existing approved contracts.

At Stage 2 completion, present the concrete record/shard layout, mixed-emission
routing, ordinary SQLite/filesystem completion behavior and proposed explicit
operator inputs. Resolve remaining product choices before the final application
switch. Prior owner decisions persist; do not ask for them again.

Product tests, fixtures, evaluators, acceptance/performance design and operational
replay are outside this prompt set. WORKPLAN 8.1 names the known evaluator,
test and CI consumers whose disposition must be supplied by the separate
verification task before implementation is declared complete. Do not keep old
APIs to satisfy old checks or silently leave that dependency unresolved.
The owner-requested changed-file scope proof remains required for every child.

### Final delivery

Report the new package and sole production flow, selected direct artifact,
supported commands, retired providers/artifacts and bounded offline edits.
Account for every dependency-map finding, every child's file-scope proof and
the separate verification disposition. Distinguish completed source work from
authorized operational replay or activation of a real database generation.

---

<a id="stage-1"></a>

## Stage 1 — Construct classification core

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: sequence this stage's mini-projects and reconcile their interfaces.
Use with [the master orchestrator prompt](#master); its authority, scope
proof and operational boundaries apply in full. This is an implementation
handoff prepared for owner review.

### Entry and exact child prompts

Start from the cited target fields and existing-source map. The new package is not yet present at the planning snapshot; preserve all existing application callers during this construction stage.

Read [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and
[CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md) for this stage's mapped source responsibilities.

1. [1_1_DEFINE_DIRECT_CONTRACTS_PROMPT.md](#mini-1-1).
2. [1_2_PORT_EMISSION_RECOVERY_PROMPT.md](#mini-1-2).
3. [1_3_BUILD_RUNTIME_CLASSIFIER_PROMPT.md](#mini-1-3).

### Ordered work and handoffs

| Mini-project | Work to coordinate | Handoff dependency |
|---|---|---|
| 1.1 | Define ErrorContract and the transient/record interfaces; produce the exact field-authority inventory. | 1.2 receives original-byte/child-span and matching-view interfaces. 1.3 receives the direct artifact shape and established rules. |
| 1.2 | Port R1–R4 and compose original-value recovery; supply one normalization identity. | 1.3 receives typed token bindings, original-value ownership and source-specific diagnostic boundaries. |
| 1.3 | Port R5–R7, implement direct artifact loading and build the current revision. | Stage 2 receives approved direct outcomes and immutable model/contract lineage. |

Run the named children in order. Reuse completed output rather than recreating
it when starting a new task. Inspect each child's actual file changes and
handoff against its exact scope; a coordinator has no independent create/edit/
delete list and cannot authorize additional files.

All three children complete their own scope proof. Stage 1 does not edit the learner or delete its tools; the precise dependency edits and deletions are coordinated with provider retirement in 3.2.

### Decisions to protect

Read the actual domain/contract definitions together with the field inventory. If a direct error type, slot role, identity rule or rendering rule has no established source, return that exact issue to the owner before it becomes runtime authority. Do not convert the projection catalog wholesale or relabel all existing templates as candidates.

Apply WORKPLAN 1.1–1.5 before interpreting classification states, record fields
or review content. Implementation defaults cannot supply missing approved rules.

### Stage deliverable

The stage handoff names all ten new core Python files, the two resolved artifact paths, normalization/model identities and the classification interfaces consumed by aggregation. It identifies structural support separately from direct-record eligibility and records any owner decisions. Existing command selection remains unchanged until 3.2.

Collect each child's changed-file proof against its own starting state.
State any incomplete dependency by file/function and responsible mini-project.
Use the completion message as the handoff; do not create an extra tracking
file. Product verification remains the separate scope named in WORKPLAN 8.1.

---

<a id="mini-1-1"></a>

## Mini-project 1.1 — Define direct contracts and record interfaces

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](#master) and [the stage coordinator](#stage-1).
This prompt defines the implementation scope and deliverable; preparing it
does not authorize running it.

### Outcome and entry

Define the direct contract and record interfaces consumed by all following
mini-projects. Start with the definitions and field inventory in WORKPLAN
1.1–1.5; do not derive product units from existing database tables.

Read the cited sources directly:

- [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md:89) 89–105 / 108–146.
- [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277.
- [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:118) 118–153 / 166 / 176–211.
- [docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md](C:/Users/nateb/Documents/ck3chronicle/docs/CLASSIFICATION_PIPELINE_RECOVERY_REVIEW.md:205) 205–254;
  `error_type` is defined at 217–218 and slot roles at 219.

### Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/__init__.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/domain.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py`

Edit: none.

Delete: none.

Record the entry state and perform the master's changed-file scope proof at
exit. Other new-package files belong to their named mini-projects; an interface
correction returns to that owner before dependent work continues.

### Existing representation evidence to inspect

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

### Implementation steps

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

### Deliverable and following work

Deliver the three scoped files and the cited field-authority inventory in the
completion message. Record agreed signatures/data shapes and each exact open
rule. Mini-project 1.2 consumes original-byte/child-span interfaces; 1.3 adds
the matcher and direct loader. Mini-project 2.1 consumes the complete record,
identity and review-result contract.

A missing necessary rule is a focused owner decision, not a general request
to review all contract candidates. Continue independent interface work while
that decision is pending. Finish with the required file-scope proof. This
mini-project does not create a new runtime model artifact.

---

<a id="mini-1-2"></a>

## Mini-project 1.2 — Port emission recovery and original-value binding

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`high`**.
Use with [the master prompt](#master) and [the stage coordinator](#stage-1).
This prompt defines the implementation scope and deliverable; preparing it
does not authorize running it.

### Outcome and entry

Consume 1.1's concrete emission, child-span and binding interfaces. Build the
stream from original error-log bytes to source-specific recovered diagnostics
and typed matching views. WORKPLAN 1.1/1.5 defines the emission/review units;
WORKPLAN R1–R4 and N2 define the source ports.

### Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/emissions.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/diagnostics.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py`

Edit: none.

Delete: none.

Record the entry state and perform the master's changed-file scope proof at
exit. Other new-package files belong to their named mini-projects; an interface
correction returns to that owner before dependent work continues.

### Exact source ports

| ID | Existing source and scope | Destination and treatment |
|---|---|---|
| R1 | [src/ck3chronicle/parser/log_blocks.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:26): `TimestampedLogBlock` 26–46; `source_block_id` 49–58; `_without_line_ending` 61–66; `_decode` 69–70; `_parse_header` 73–98; `_make_block` 101–139; `iter_log_blocks` 142–257; header/source/BOM definitions 16–23 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/emissions.py`: port lexer mechanics into `iter_emissions` and its private helpers; emission data moves to `pipeline/domain.py`. Supply real provenance explicitly. Omit the two-bracket fixture header at 19–21/86 and old constructor defaults. Decoded text is not the native review copy: preserve original byte spans. |
| R2 | [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:253): `block_message` 253–263; `split_location_evidence` 266–270; `extract_structured_slots` 273–422; `normalize_key_path` 425–437; `normalize_structured_slots` 440–501; `normalize_known_key_grammars` 504–592; `mask_locators` 626–631; `tokenize` 634–642; `script_system_layers` 645–670; `diagnostic_lead` 673–718; `reason_lead` 762–768; their constants/regex definitions 13–250 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py`: port these pure routines and their grammar definitions. Adapt block access to new emissions/diagnostics; remove the 384-token truncation at 638. Preserve a separate original-value binding view. Do not port `legacy_diagnostic_lead` 721–759. |
| R3 | Same [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:595): `_normalize_persistent_clause` 595–603 and `semantic_units` 606–623, specifically wrapper/clause recognition at 608–620 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/diagnostics.py`: port only the recognized persistent-reader splitting grammar into `recover_diagnostics`; write child spans/value ownership afresh (N2). Do not port lossy string normalization as the recovery result. Normalization follows recovery. |
| R4 | [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:135): `_path_from_match` 135–140; `_overlaps` 143–144; `_extract_locators` 147–181; supporting path patterns 39–77 and `_EVENT_URI_RE` 80; `LocatorEvidence` 97–102 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py`: port pure path/line extraction, adapted to preserve source spans and original spelling. Keep event URIs distinct from filesystem paths. Define the current locator value in `pipeline/domain.py`. Nothing else from the projection module is a port: typed values come from R2 and N2, not a post-classification mapping dispatcher. |

### Implementation steps

1. Port the real lexer into `emissions.py:iter_emissions`. Keep header,
   continuation, source and original ordering behavior. Supply provenance
   explicitly from the actual input. Keep native byte access independent of
   replacement-decoded matching text.
2. Define `diagnostics.py:recover_diagnostics` over each emission. Use the
   identified persistent-reader wrapper/clause grammar to split supported
   multi-diagnostic emissions. Recover child spans and ownership before any
   masking or value normalization. A single diagnostic uses the corresponding
   original emission span. A recognition/recovery failure remains explicit and
   cannot make the input appear successfully fully processed.
3. Port the named grammar routines into `normalization.py` and compose
   `normalize_for_match` over recovered diagnostics. Extract concrete values
   before replacing them with typed tokens. Preserve the full token sequence;
   the old 384-token cap at normalize.py 638 is removed.
4. Build `bindings.py:bind_original_values` so token/typed-slot results resolve
   to their original child values and locators. Port only R4's locator grammar
   from the old projection file. Keep event URIs distinct from paths and
   maintain original spelling and positions.
5. Make shared-envelope versus child-local fields explicit where splitting
   requires it. Do not extract a value from one child and assign it to a
   neighboring child just because both came from one emission. Carry the
   provenance required by the approved contract and later native review routing.
6. Expose the normalization identity in `normalization.py`. Document in the
   handoff the exact grammar changes from the selected artifact's normalization
   so 1.3 can prepare a matching current artifact. The offline learner's own
   normalization and algorithm are outside this mini-project.

### Port boundaries

R3's old `semantic_units` returns normalized strings; its grammar is useful,
but that output cannot serve as original diagnostic recovery. The new N2
composition supplies original spans and value binding.

R4 is the complete authorized port from the projection module. Its
`_template_alignment` 287–343, `_reference_values` 384–472 and issue/projection
dispatchers are not dependencies of the new binder. The typed match in 1.3
consumes this original-value map once; it does not rematch the whole message.

The new modules depend on the new domain types and pure standard/library
utilities as needed. They do not import the old providers merely to delegate
their behavior. Their exact source ports are listed above.

### Deliverable and following work

Deliver `iter_emissions`, `recover_diagnostics`, `normalize_for_match` and
`bind_original_values` in the four scoped files. Explain the actual data
path from original bytes to a child diagnostic's normalized tokens and original
values, with source/function references from the implementation.

Pass those interfaces and the normalization identity to 1.3. Pass native-byte
access and parent/child identity requirements to 2.1/2.2. The future offline
lexer caller changes belong to 3.2, where the old lexer is retired. Finish with
the required file-scope proof.

---

<a id="mini-1-3"></a>

## Mini-project 1.3 — Build runtime classification and the direct model

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](#master) and [the stage coordinator](#stage-1).
This prompt defines the implementation scope and deliverable; preparing it
does not authorize running it.

### Outcome and entry

Consume 1.1's direct contract rules and 1.2's original-value matching view.
Construct the selected direct model and runtime classifier. Production loads
the completed approved artifact; this task does not invoke the learner.

Read WORKPLAN 1.2–1.4 and section 7 before changing the artifact format.
A structural match does not by itself supply a missing direct error type,
identity or rendering rule.

### Exact mutation scope

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

### Exact source ports

| ID | Existing source and scope | Destination and treatment |
|---|---|---|
| R5 | [src/ck3chronicle/classification/contracts.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:22): `ValidatedSlot` 22–35; `TemplateValidation` 38–42; `_literal_equal` 45–50; `_closed_alternatives` 53–59; `validate_template_tokens` 62–146; imports/constants 1–19 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/contracts.py`: port exact literal/typed-slot matching and ambiguity rejection. Extend the new direct contract/binding result under N1/N2. Similarity never substitutes for typed validation. |
| R6 | [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:24): schema/version constants 14–17; `ModelIntegrityError` 20–21; `LayerContracts` 24–35; `ModelCluster` 38–52; `EmpiricalModel` 55–64; validation helpers 67–138; `load_model` 141–191. [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:25): `_approved_revision_root` 25–45; `approved_model_path` 48–49; `load_approved_model` 56–57; `load_approved_classifier` 76–77 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/model.py` and `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/catalog.py`: port immutable hash/integrity checks, supported direct-contract structures and explicit source/install artifact lookup. Adapt to one current format. Keep one current normalization-version identity shared by the pure grammar and artifact readers/writers; do not preserve conflicting copies. Bind the new catalog to the prepared direct artifact in 1.3; application/package selection activates it in 3.2; omit projection pins/loaders and old-format support. |
| R7 | [src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:28): `ClassificationResult` 28–41; `_similarity` 44–55; `_ordered_anchor_overlap` 58–63; `_composed_id` 66–68; `Classifier.__init__` 74–82; `classify` 84–208; `_result` 229–255 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py`: port source partitioning, runtime candidate comparison, exact typed matching and layered result mechanics. Adapt to recovered diagnostics and N1 outcomes; remove dual lead lookup at 89. The old `classify_block` 210–227 is not ported: recovery is explicitly composed by the processor and learner evidence collector. |

### Artifact inputs and current selection

- [models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1) and
  [models/67303093ecda779d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/manifest.json:1): existing selected structures
  and their provenance. Both are read-only inputs to this mini-project.
- [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:13) 13–16: current
  artifact selection; 25–45: source/install resource lookup to port.
- [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) 29–34: current packaging, changed only in 3.2.
- 1.1's per-field authority inventory: established direct rules and resolved
  decisions. The projection catalog is not an automatic contract conversion input.

### Implementation steps

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

### Deliverable and following work

Deliver the new classifier, direct loader/catalog, typed validator, shared
normalization identity and two resolved artifact files. Record the exact
artifact hash/revision, source of direct rules, supported outcomes and the
entry-level treatment of any changed normalized structures.

Stage 2 must be able to consume approved fields for rendering/aggregation
without a projection or classifier payload reread. Report any unresolved
contract rule as incomplete work; do not manufacture an approval state to
finish the artifact. Finish with the required file-scope proof.

---

<a id="stage-2"></a>

## Stage 2 — Construct complete Run processing

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: sequence this stage's mini-projects and reconcile their interfaces.
Use with [the master orchestrator prompt](#master); its authority, scope
proof and operational boundaries apply in full. This is an implementation
handoff prepared for owner review.

### Entry and exact child prompts

Require the Stage 1 handoff: direct contract interfaces and rules, original-byte emission recovery, bound values, runtime classifier and resolved artifact identity. Any missing field decision returns to 1.1; it is not supplied by a storage default.

Read [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and
[CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md) for this stage's mapped source responsibilities.

1. [2_1_BUILD_RUN_STORAGE_AND_REVIEW_PROMPT.md](#mini-2-1).
2. [2_2_COMPOSE_INPUT_PROCESSING_AND_REPLAY_PROMPT.md](#mini-2-2).

### Ordered work and handoffs

| Mini-project | Work to coordinate | Handoff dependency |
|---|---|---|
| 2.1 | Construct aggregation, the native shard writer and current-generation repository as one connected storage boundary. | 2.2 receives exact write_run inputs, duplicate-hash behavior, shard completion metadata and read interfaces. |
| 2.2 | Port capture/input primitives and compose pending/manual/replay through process_input. | Stage 3 receives complete processing/replay functions and explicit argument/result shapes. |

Run the named children in order. Reuse completed output rather than recreating
it when starting a new task. Inspect each child's actual file changes and
handoff against its exact scope; a coordinator has no independent create/edit/
delete list and cannot authorize additional files.

Aggregation, native review and SQLite are owned together by 2.1. Reprocessing uses a separately named fresh generation and explicit original-log inputs. This stage does not switch the existing application or read old database rows.

### Decisions to protect

Before Stage 3 activation, show the actual diagnostic identity fields, shard bytes/metadata separation, mixed-child accounting and the code path that makes a Run complete. Include explicit input/generation arguments proposed for commands. Ask only for a remaining product choice; accepted scope and established requirements do not need reconfirmation.

Apply WORKPLAN 1.1–1.5 before interpreting classification states, record fields
or review content. Implementation defaults cannot supply missing approved rules.

### Stage deliverable

The stage handoff shows prepare_* -> process_input -> classification -> aggregation/review -> write_run, plus rebuild_generation -> the same process_input. It names duplicate/failure results and their effect on protected evidence. It supplies the proposed command input/output contract for 3.1. The pure playset analyzer port is listed as a future feature dependency with no current processor call.

Collect each child's changed-file proof against its own starting state.
State any incomplete dependency by file/function and responsible mini-project.
Use the completion message as the handoff; do not create an extra tracking
file. Product verification remains the separate scope named in WORKPLAN 8.1.

---

<a id="mini-2-1"></a>

## Mini-project 2.1 — Build aggregation, Run storage and native review

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](#master) and [the stage coordinator](#stage-2).
This is an implementation handoff prepared for owner review.

### Outcome and entry

Construct aggregation, current SQLite storage and native review as one
connected boundary. Consume the Stage 1 direct contract/record interfaces,
original-byte emission access and approved classification outcomes.

Read WORKPLAN 1.1–1.5 / N4–N6, plus
[docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277 and
[docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:176) 176–204 / 227–244.
Those specify compact identity, native review and complete Run storage.

### Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/aggregation.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/review.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/schema.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/repository.py`

Edit: none. Delete: none.

Record the entry baseline and finish with the master's changed-file scope
proof. A needed change to a preceding file returns to its owning mini-project
before dependent work continues. Runtime evidence output is implemented here;
writing actual evidence or databases is a separate operational action.

### Existing code references and why these bodies are new

| Existing file and exact scope | Reason for new composition |
|---|---|
| [src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:168) `get_session_by_error_log_hash` 168–181 | Full-log duplicate rejection is useful behavior; the new repository writes current Runs, so its SQL is written against the new schema. |
| Same repository, staged writes 1286–1543 / 1763–2046 / 2531–2837 | Old source, assignment/payload and projected issue representations are replaced; these writers are not ported. |
| [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:1) 1–550; 21-table inventory in CALLER_INDEX | Existing DDL includes obsolete stages and features. Build only the current Run/record/review representation. |
| [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:475) `_unclassified_draft` 475–496 | An old unknown issue is not the target native review evidence. No current native-shard writer implements the target. |

### Functions and implementation steps

1. In `aggregation.py`, implement `diagnostic_identity`,
   `add_classified_diagnostic` and `finish_records`. Use all identity roles
   defined by the approved contract, including concrete values and locators
   where required. Aggregate occurrence count and first/last observed timestamps.
   Grouping solely by contract ID or old regex signature is insufficient.
2. Make assignment eligibility explicit using Stage 1's approved outcome.
   Render stable text from that versioned contract and store the needed concrete
   values/rendering. Unknown emissions do not acquire a diagnostic identity
   merely because some slots were extracted.
3. In `review.py`, implement `ReviewShardWriter`,
   `append_review_emission` and `finish_review_shard`. Stream original native
   bytes with headers and continuations in original order and frequency.
   Use the original byte view; do not encode replacement-decoded text.
4. Implement the proposed mixed-emission representation: write an emission once
   when one or more children require review, with child routing/provenance in
   associated metadata. Preserve occurrence frequency across distinct emissions.
   Keep recognized-emission counts, recovered-diagnostic counts, classified
   counts and review-emission counts distinct. Record this physical choice for
   the Stage 2 owner review.
5. Produce one native shard per successful Run, including an empty shard.
   Its namespace is tied to the destination generation and Run ID so equal
   Run IDs in different generations cannot collide. SQLite holds the reference,
   counts, availability, integrity and routing metadata required by architecture
   176–191, not a duplicate unresolved text payload.
6. In `schema.py`, define current-generation DDL for successful Run facts,
   required model/contract/application/parser/splitter/normalizer/schema lineage,
   compact approved records and review metadata. Enforce duplicate full-log hash
   rejection within the generation. Store enough record interpretation/rendering
   for reads to remain independent of the installed model and original log.
7. In `repository.py`, implement the following concrete API:

| Function | Responsibility |
|---|---|
| `create_generation` | Create a separately named current schema and generation identity. |
| `open_generation` | Open only the supported current generation for writing. |
| `open_generation_readonly` | Open stored current-generation facts without mutations. |
| `find_run_by_log_hash` | Resolve/reject an already processed full-log hash. |
| `write_run` | Complete one Run's records and native-review metadata. |
| `get_run`, `latest_run`, `list_runs` | Read current Run facts. |
| `read_diagnostics`, `read_review_metadata` | Supply the stored report/audit/review interfaces. |

8. Define the concrete SQLite/filesystem order by which shard completion and
   Run acceptance remain consistent. Report the ordinary transaction/file
   behavior on success and failure, including any unaccepted temporary file.
   A failed write cannot leave a successful Run pointing at an incomplete shard.
   Do not port the old processing journal, invent a reservation/reuse scheme,
   or add a publication state machine without a requirement.
9. Keep originals independently retained. Neither duplicate rejection nor a
   failed Run gives this code authority to delete a protected original log.
   Use one supported schema; incompatible generations require an explicit fresh
   rebuild through 2.2 rather than migration on open.

### Deliverable and following work

Deliver the four scoped modules, their actual data/schema shapes, repository
API and shard completion contract. Give 2.2 exact inputs/results for
`write_run`, hash rejection and shard completion. Give 3.1 the read API and
stored fields required by reports/audit.

Present the concrete identity/routing/layout and cross-resource behavior in
the Stage 2 review. Do not claim those physical choices were already specified
by the old implementation. Finish with the required file-scope proof.

---

<a id="mini-2-2"></a>

## Mini-project 2.2 — Compose protected inputs, processing and replay

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`high`**.
Use with [the master prompt](#master) and [the stage coordinator](#stage-2).
This is an implementation handoff prepared for owner review.

### Outcome and entry

Compose protected pending input, explicit manual input and fresh-generation
replay through one `process_input`. Consume Stage 1's recovery/classifier and
2.1's aggregation, review and repository handoff.

Capture means a stable protected copy before classification or database
processing. WORKPLAN 1.5, C1/C2, N3/N7 and the canonical source definitions govern
this boundary.

### Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/capture.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/processor.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/replay.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/playset.py`

Edit: none. Delete: none.

Record the entry baseline and finish with the master's changed-file scope
proof. A needed change to a preceding file returns to its owning mini-project
before dependent work continues. Runtime evidence output is implemented here;
writing actual evidence or databases is a separate operational action.

### Exact source ports

| ID | Existing source and scope | Destination and treatment |
|---|---|---|
| C1 | [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:37): capture exceptions 37–50; `PendingFileStat` 112–118; `PendingCapture` 121–129; `_make_inheriting_staging_directory` 148–164; `discover_logs` 167–176; `spool_logs` 179–342; `_copy_exact` 475–481; `_copy_stable_without_hash` 484–496 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/capture.py`: port copy-only behavior and the exact helper/type closure. Keep current capture metadata and watcher abort callback; required error.log precedes optional associated crash evidence. No database/model/learner imports. Port the relevant constants for current error-log/capture metadata, not `LEGACY_LOG_NAMES`. |
| C2 | Same [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:364): `FileIdentity` 53–57; `hash_file` 364–370; `_stable_identity` 402–412; `read_capture_metadata` 552–556; `_manifest_bytes` 569–572; `_load_manifest` 602–611; `selected_pending_path` 920–937 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/inputs.py`: port hashing, explicit path selection and JSON read/serialization primitives. Write current input inspection/protection interfaces under N3. Do not port `_inspect_pending` 940–1058, `finalize_pending` 1067–1150, `read_snapshot` 881–906 or their old-format/result machinery. |
| F1 | [src/ck3chronicle/runtime_context.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:25): `MountedDlc` 25–32; `MountedMod` 35–43; inventory/mount regex 73–91; path/key helpers 94–136; `_BlockCandidate` 139–181; `_ContextAnalysis` 184–202; `_typed_mounts` 205–271; `_analyze_debug_context` 274–453 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/playset.py`: port this pure extraction kernel as `analyze_debug_context`, with its types/constants. Do not port `parse_debug_context` 456–481: it is an old compatibility wrapper over the analyzer. No repository import, stored-result reconstruction or context reparse service. This preserves the approved same-Run playset fast-follow's working grammar; it is not added to `process_input` in this recovery. |

### New interfaces and old-body boundaries

| New function/type | Required behavior |
|---|---|
| `inputs.PreparedInput` | Explicit protected source, complete hash, supported capture facts and truthful unavailable metadata. |
| `prepare_pending_input` | Inspect exactly one selected current pending capture. |
| `prepare_manual_input` | Accept an explicitly supplied native error log and protect it for processing. |
| `prepare_retained_input` | Accept an explicitly selected already retained original for a fresh replay. |
| `protect_input` | Preserve the full original independently of records/review and within configured writable ownership. |
| `processor.process_input` | Sole Run composition from prepared input to complete records/native review. |
| `replay.rebuild_generation` | Process an explicit retained-input set into a named fresh generation via the same processor. |

Existing bodies explain the changed boundary:

- [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:940) `_inspect_pending` 940–1058,
  `finalize_pending` 1067–1150, `read_snapshot` 881–906 and `snapshot`
  1272–1389 contain old-format/adoption/result behavior outside C1/C2.
- [src/ck3chronicle/ingest.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:35) `ingest` 35–121 registers old
  storage before classification; it is not the new manual-input processor.
- [src/ck3chronicle/processing.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:888) context 888, parser 903,
  classifier 929 and projection 946 compose the old stages. Its lease/journal
  46–190 is not a port.
- [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:38) `load_config` 43–59,
  `require_strict_descendant` 80–102 and `validate_project_containment`
  105–140 supply existing explicit path authority.

### Implementation steps

1. Port C1's copy-only `spool_logs` and its exact helper/type closure into
   `capture.py`. Preserve the actual watcher callback/abort and result shape.
   Protect the required error log before optional associated crash evidence.
   Urgent capture does not hash the full log, open SQLite or load a classifier.
2. Port C2 primitives into `inputs.py`, then implement the explicit preparation
   and protection interfaces above. Compute a stable complete-file hash in the
   deferred path. Accept one current capture representation; manual native-log
   selection is an explicit input route, not a failed-format fallback.
3. Use supplied observed lifecycle facts only. If manual/replay input has no
   such facts, preserve their unavailability. Do not infer them from directory
   names, filesystem times or old database rows. Protect originals indefinitely.
4. Implement `process_input` with this single call order:

   `PreparedInput -> duplicate guard -> iter_emissions -> recover_diagnostics`
   `-> normalize_for_match / typed classify / original bindings`
   `-> aggregation + native review -> write_run`.

   Follow the actual 1.2/1.3 binding API without applying normalization or typed
   matching twice. The input stream is complete at every file size; every
   recognized emission yields accounted diagnostics/review or an explicit
   failure. Do not silently skip a malformed child.
5. Obtain a prospective Run identity within the ordinary 2.1 completion design.
   Coordinate the shard and compact records once. Report duplicate input as
   the defined duplicate result without creating a second successful Run or
   deleting protected evidence. Expose failures truthfully; no success-shaped
   result may hide incomplete storage.
6. Implement `rebuild_generation` with an explicit set of retained native
   inputs and separately named destination generation. Require the destination
   to be fresh; use the same preparation/classification/storage behavior as
   ordinary processing. Do not read/translate old database rows or replace the
   active generation implicitly.
7. Port F1 to `playset.py:analyze_debug_context` and its named pure type/helper
   closure. It preserves working grammar for the approved same-Run debug-log
   fast-follow when `runtime_context.py` is deleted. The current processor
   does not call it; capture/context persistence integration is later work.
8. Write down the concrete processing arguments/results for 3.1: selected
   input, configured protection ownership, chosen generation, Run/duplicate/
   failure result and stored review reference. Present the proposed explicit
   CLI selectors at the Stage 2 review, using 3.1's command table.

### Deliverable and following work

Deliver the five files and an exact call-chain handoff to Stage 3. Explain how
pending/manual/replay share `process_input`, how the protected original survives,
and what happens on duplicate/failure. Include the two Stage 2 data/layout
decisions from 2.1 and the proposed operator arguments for review.

Existing application calls change in 3.2. No actual capture, processing,
production database creation or replay is performed merely to prepare this
source handoff. Finish with the required file-scope proof.

---

<a id="stage-3"></a>

## Stage 3 — Connect application and retire old pipeline

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Role: sequence this stage's mini-projects and reconcile their interfaces.
Use with [the master orchestrator prompt](#master); its authority, scope
proof and operational boundaries apply in full. This is an implementation
handoff prepared for owner review.

### Entry and exact child prompts

Require Stage 1 and Stage 2 handoffs, including concrete model paths, repository/read interfaces, complete processing inputs/results and resolution of the Stage 2 product choices. Obtain the separate verification task's explicit disposition for the known evaluator/tests/CI before declaring the whole implementation complete.

Read [WORKPLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/WORKPLAN.md), [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and
[CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md) for this stage's mapped source responsibilities.

1. [3_1_BUILD_REPORTS_AND_COMMANDS_PROMPT.md](#mini-3-1).
2. [3_2_SWITCH_AND_RETIRE_OLD_PIPELINE_PROMPT.md](#mini-3-2).

### Ordered work and handoffs

| Mini-project | Work to coordinate | Handoff dependency |
|---|---|---|
| 3.1 | Build stored reports, current database audit and new command handlers. | 3.2 receives one register_commands entry and the lightweight capture_error handler. |
| 3.2 | Switch existing application/model resources, reconnect bounded offline consumers and delete all named obsolete providers/artifacts. | The application has one current pipeline and current documentation; no residual adapter keeps the retired provider graph callable. |

Run the named children in order. Reuse completed output rather than recreating
it when starting a new task. Inspect each child's actual file changes and
handoff against its exact scope; a coordinator has no independent create/edit/
delete list and cannot authorize additional files.

Mini-project 3.2 owns activation and retirement together. Recheck the complete caller/index disposition before concluding; any needed preceding implementation correction returns to its exact owning mini-project instead of authorizing a broad edit to the new package.

### Decisions to protect

Use the approved Stage 2 command contract and concrete 3.1 handlers. A new product behavior or additional mutation path returns as a precise amendment before it is implemented. Do not use general cleanup as authorization to expand the final switch.

Apply WORKPLAN 1.1–1.5 before interpreting classification states, record fields
or review content. Implementation defaults cannot supply missing approved rules.

### Stage deliverable

The final handoff accounts for WORKPLAN 6.1 caller changes, 6.2/6.3 deletions, section 7 artifact selection/removal, L1–L5 offline edits and section 8 documentation/deferred consumers. Describe source completion and separate verification status truthfully; do not claim a production replay, database cutover or working retained test suite that was not commissioned and evidenced.

Collect each child's changed-file proof against its own starting state.
State any incomplete dependency by file/function and responsible mini-project.
Use the completion message as the handoff; do not create an extra tracking
file. Product verification remains the separate scope named in WORKPLAN 8.1.

---

<a id="mini-3-1"></a>

## Mini-project 3.1 — Build stored reports, audit and command handlers

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`high`**.
Use with [the master prompt](#master) and [the stage coordinator](#stage-3).
This is an implementation handoff prepared for owner review.

### Outcome and entry

Build reports and audit from stored current-generation facts, then implement
the explicit command handlers that 3.2 connects to the existing application.
Require Stage 2's repository, processor and input/result handoff and its
resolved owner-facing choices.

### Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/reports.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/audit.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/commands.py`

Edit: none. Delete: none.

Record the entry baseline and finish with the master's changed-file scope
proof. A needed change to a preceding file returns to its owning mini-project
before dependent work continues. Runtime evidence output is implemented here;
writing actual evidence or databases is a separate operational action.

### Exact behavior references

| Existing source | New destination and reason |
|---|---|
| [src/ck3chronicle/reporting.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:81) `build_session_report` 81–411; projection precondition 99–110; classifier payload query 124–133 | New `reports.py` reads final compact records and stored rendering. The old body requires removed representations and is not ported. |
| [src/ck3chronicle/database_audit.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:80) `audit_database` 80–861 | New `audit.py` describes current database facts without old projection/raw-block/schema assumptions or required log reopening. |
| [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:74) `_capture_error` 74–99 and calls 137/163/225/526/543 | New lightweight `commands.capture_error` handles the remaining copy-only capture callers after 3.2 disconnects old ingest/reconcile. |
| [src/ck3chronicle/command_envelope.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/command_envelope.py:1) 1–51 | Use the existing neutral command envelope. |
| [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:38) 38–140 | Use explicit configured path ownership; this task does not redesign configuration. |
| WORKPLAN 6.1 and CALLER_INDEX CLI registration sites | Exact old registrations and the destination handler for each retained command. Existing CLI edits belong to 3.2. |

### Functions and implementation steps

1. In `reports.py`, implement `build_run_report`, `list_errors` and
   `get_review_reference` using 2.1's repository reads. Use Run identity,
   contract-defined fields, counts and stored rendering. Report native-review
   metadata separately from compact approved diagnostic records.
2. Make reports independent of the original log and installed model files.
   Missing external review evidence does not erase the stored Run; present
   stored availability/reference metadata accurately. Ordinary reports do not
   recreate diagnostics from a shard or perform classification.
3. In `audit.py`, implement `audit_database` over the current schema,
   Run/record/lineage and review metadata relationships. This is the ordinary
   product audit command, not a new evaluation framework or a source-log
   reconciliation tool. It must not mutate or upgrade a database.
4. In `commands.py`, implement the handlers and registration below against
   `inputs`, `processor`, `replay`, `reports`, `audit` and `repository`.
   Import heavier processing/model dependencies inside the appropriate handlers
   so command registration and copy-only capture remain lightweight.
5. Implement `capture_error` for the current capture exceptions and operation
   failures. It must not import a removed database/provider module merely to
   reproduce the old mixed exception handler.
6. Implement `register_commands` to add the supported pipeline commands to
   the existing parser's subparsers. The root CLI continues to own capture,
   watch, doctor and observe-logging; their behavior is outside this new module.

### Proposed command contract for the Stage 2 review

The selectors below are the concrete proposal for the new handlers. Carry
forward any owner change recorded at Stage 2; do not preserve old aliases.
Resolve paths under existing configured authority. The generation's review
namespace comes from 2.1, not an independently guessed fallback path.

| Command / function | Explicit selector(s) and result |
|---|---|
| `ingest` / `cmd_ingest` | `--error-log PATH --db PATH`: protect the supplied native input and process it into the chosen current generation. |
| `process-pending` / `cmd_process_pending` | `--pending PATH --db PATH`: process exactly the selected current capture. |
| `rebuild-db` / `cmd_rebuild_db` | Repeated `--error-log PATH` plus `--destination-db PATH`: create a named fresh generation from that explicit retained-input set. |
| `runs` / `cmd_runs` | `--db PATH`: list successful current Runs. |
| `report` / `cmd_report` | `--db PATH --run RUN_ID`: report the stored Run. |
| `latest` / `cmd_latest` | `--db PATH`: report the latest stored Run, or explicitly report no Runs. |
| `errors` / `cmd_errors` | `--db PATH --run RUN_ID`: list the Run's approved compact diagnostic records. |
| `review-queue` / `cmd_review_queue` | `--db PATH --run RUN_ID`: return the Run's native shard reference and review metadata. |
| `audit-db` / `cmd_audit_db` | `--db PATH`: read-only audit of current database facts. |

A missing/incompatible database produces an explicit result rather than a
migration or guessed alternative. `rebuild-db` creates the fresh generation;
normal read commands never create one. Processing uses the selected direct
artifact through the new catalog; individual commands do not select separate
projection/classifier revisions.

Present successful Run identity/counts/review reference, duplicate results and
processing failures using the actual 2.2 result contract. Do not retain old
payload counts, category/projection fields or session-stage status as output
compatibility obligations.

### Deliverable and following work

Deliver the three new modules, the actual registered command/argument list and
handler-to-service call table. Give 3.2 the exact `register_commands` and
`capture_error` entry points. Existing `cli.py`, watcher imports and package
resources remain scoped to 3.2. Finish with the required file-scope proof.

---

<a id="mini-3-2"></a>

## Mini-project 3.2 — Switch application callers and retire the old pipeline

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](#master) and [the Stage 3 coordinator](#stage-3).
This is the connected source activation and retirement handoff for owner review.

### Outcome and entry

Require completed 1.1–3.1 handoffs: direct interfaces/model, recovery/classifier,
complete Run/review storage, common processor/replay and new read/command handlers.
Connect those implementations to the application and delete the exact old
providers and tools below in the same mini-project.

Read WORKPLAN 6–8, [DEPENDENCY_MAP.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/DEPENDENCY_MAP.md) and [CALLER_INDEX.md](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/CALLER_INDEX.md)
as the complete dependency closure. Read the current repository and nested
offline-tool AGENTS instructions before editing their files.

Require the separate verification task's concrete disposition for the evaluator,
tests and CI consumers named in WORKPLAN 8.1 before declaring the entire
implementation complete. They do not justify retaining old APIs and are not
silently deleted under this prompt.

### Exact mutation scope

Create: none.

Edit only the following existing files, within the stated changes. The new
pipeline files and direct artifact already belong to 1.1–3.1; corrections
return to the owning mini-project with its own baseline and scope proof.

| Mini-project | Exact existing file | Permitted change |
|---|---|---|
| 3.2 | [tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35) | Only the lexer/type/call reconnection and obsolete-tool removal edits enumerated in WORKPLAN 3.2 and the bounded offline-tool section below. |
| 3.2 | [tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:366) | Remove frozen-oracle build dependency/argument and associated evaluation output, as enumerated in WORKPLAN 3.2 and the bounded offline-tool section below. |
| 3.2 | [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md:1) | Update the tool inventory for the actual remaining files. |
| 3.2 | [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md:1) | Update obsolete tool ownership/reporting references; retain the existing learner location and candidate/promotion boundary. |
| 3.2 | [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:11) | Exact handler removals and new command/capture registrations in WORKPLAN 6.1 and the application-connection section below. |
| 3.2 | [src/ck3chronicle/watcher.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:17) | Capture-error import at 17–20. |
| 3.2 | [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:12) | Remove unreachable old-Python import fallback at 12–15. |
| 3.2 | [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29) | Selected model package data at 29–34. |
| 3.2 | [models/README.md](C:/Users/nateb/Documents/ck3chronicle/models/README.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/DATA_COMPATIBILITY_AND_OPERATIONS.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATA_COMPATIBILITY_AND_OPERATIONS.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/MODEL_QUALITY_AND_PROMOTION.md](C:/Users/nateb/Documents/ck3chronicle/docs/MODEL_QUALITY_AND_PROMOTION.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/REPOSITORY_AND_BACKUP.md](C:/Users/nateb/Documents/ck3chronicle/docs/REPOSITORY_AND_BACKUP.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/WORKSPACE_ROUTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/WORKSPACE_ROUTING.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [README.md](C:/Users/nateb/Documents/ck3chronicle/README.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |
| 3.2 | [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md:1) | Only the implemented source/command/model/continuation facts enumerated in WORKPLAN 8.3 and the scoped-documentation section below. |

The next three lists are the complete deletion scope. They authorize deletion
of these source/artifact files, not recursive removal of a guessed directory.
Resolve the exact paths inside the checkout before deleting them and preserve
pre-existing owner changes in the recoverable source baseline.

#### Delete obsolete offline tools

- [tools/template_learning/analyze_script_system_layers.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/analyze_script_system_layers.py:1) — entire file, 1–131.
- [tools/template_learning/blind_review/build_blind_stratified_sample.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/build_blind_stratified_sample.py:1) — entire file, 1–336.
- [tools/template_learning/blind_review/compare_blind_adjudication.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/compare_blind_adjudication.py:1) — entire file, 1–279.
- [tools/template_learning/blind_review/evaluate_postfix_blind_sample.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/blind_review/evaluate_postfix_blind_sample.py:1) — entire file, 1–376.
- [tools/template_learning/build_review_pack.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_review_pack.py:1) — entire file, 1–446.
- [tools/template_learning/build_semantic_projection_catalog.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/build_semantic_projection_catalog.py:1) — entire file, 1–1268.
- [tools/template_learning/evaluate_unseen_session.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/evaluate_unseen_session.py:1) — entire file, 1–408.
- [tools/template_learning/mine_symbol_suffixes.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/mine_symbol_suffixes.py:1) — entire file, 1–273.

#### Delete superseded product providers and converter

- [src/ck3chronicle/classification/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/__init__.py:1) — entire file, 1–26.
- [src/ck3chronicle/classification/catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/catalog.py:1) — entire file, 1–82.
- [src/ck3chronicle/classification/contracts.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/contracts.py:1) — entire file, 1–146.
- [src/ck3chronicle/classification/inference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/inference.py:1) — entire file, 1–255.
- [src/ck3chronicle/classification/model.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/model.py:1) — entire file, 1–191.
- [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:1) — entire file, 1–768.
- [src/ck3chronicle/classification/projection_catalog.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/projection_catalog.py:1) — entire file, 1–508.
- [src/ck3chronicle/classification/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/service.py:1) — entire file, 1–312.
- [src/ck3chronicle/db/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/__init__.py:1) — entire file, 1–1.
- [src/ck3chronicle/db/migrations.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/migrations.py:1) — entire file, 1–919.
- [src/ck3chronicle/db/payloads.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/payloads.py:1) — entire file, 1–35.
- [src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:1) — entire file, 1–2896.
- [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:1) — entire file, 1–550.
- [src/ck3chronicle/models/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/__init__.py:1) — entire file, 1–1.
- [src/ck3chronicle/models/issue.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/issue.py:1) — entire file, 1–131.
- [src/ck3chronicle/models/parse.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/models/parse.py:1) — entire file, 1–65.
- [src/ck3chronicle/parser/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/__init__.py:1) — entire file, 1–1.
- [src/ck3chronicle/parser/extractors/__init__.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/__init__.py:1) — entire file, 1–121.
- [src/ck3chronicle/parser/extractors/asset_graphics.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/asset_graphics.py:1) — entire file, 1–35.
- [src/ck3chronicle/parser/extractors/culture_faith.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/culture_faith.py:1) — entire file, 1–34.
- [src/ck3chronicle/parser/extractors/database_reference.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/database_reference.py:1) — entire file, 1–38.
- [src/ck3chronicle/parser/extractors/debug_log.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/debug_log.py:1) — entire file, 1–122.
- [src/ck3chronicle/parser/extractors/descriptor.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/descriptor.py:1) — entire file, 1–31.
- [src/ck3chronicle/parser/extractors/event_system.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/event_system.py:1) — entire file, 1–37.
- [src/ck3chronicle/parser/extractors/gui_interface.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/gui_interface.py:1) — entire file, 1–34.
- [src/ck3chronicle/parser/extractors/history_setup.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/history_setup.py:1) — entire file, 1–31.
- [src/ck3chronicle/parser/extractors/localization.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/localization.py:1) — entire file, 1–49.
- [src/ck3chronicle/parser/extractors/persistent_reader.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/persistent_reader.py:1) — entire file, 1–36.
- [src/ck3chronicle/parser/extractors/script_hygiene.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_hygiene.py:1) — entire file, 1–36.
- [src/ck3chronicle/parser/extractors/script_system.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/script_system.py:1) — entire file, 1–105.
- [src/ck3chronicle/parser/extractors/unclassified.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/extractors/unclassified.py:1) — entire file, 1–36.
- [src/ck3chronicle/parser/log_blocks.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:1) — entire file, 1–257.
- [src/ck3chronicle/parser/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/normalize.py:1) — entire file, 1–99.
- [src/ck3chronicle/parser/service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/service.py:1) — entire file, 1–410.
- [src/ck3chronicle/archive_registry.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/archive_registry.py:1) — entire file, 1–307.
- [src/ck3chronicle/harvester.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/harvester.py:1) — entire file, 1–1389.
- [src/ck3chronicle/ingest.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/ingest.py:1) — entire file, 1–121.
- [src/ck3chronicle/processing.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/processing.py:1) — entire file, 1–1086.
- [src/ck3chronicle/reporting.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/reporting.py:1) — entire file, 1–411.
- [src/ck3chronicle/database_audit.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/database_audit.py:1) — entire file, 1–895.
- [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:1) — entire file, 1–620.
- [src/ck3chronicle/semantic_projection_service.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection_service.py:1) — entire file, 1–465.
- [src/ck3chronicle/runtime_context.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/runtime_context.py:1) — entire file, 1–668.
- [src/ck3chronicle/session_intelligence.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/session_intelligence.py:1) — entire file, 1–937.
- [src/ck3chronicle/source_resolution.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/source_resolution.py:1) — entire file, 1–534.
- [src/ck3chronicle/triage.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/triage.py:1) — entire file, 1–191.
- [tools/migrate_legacy_pending_metadata.ps1](C:/Users/nateb/Documents/ck3chronicle/tools/migrate_legacy_pending_metadata.ps1:1) — entire file, 1–236.

#### Delete superseded active model files

- [models/67303093ecda779d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/empirical_template_model.json:1) — 1–1.
- [models/67303093ecda779d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/manifest.json:1) — 1–1.
- [models/67303093ecda779d/semantic_projection_catalog.json](C:/Users/nateb/Documents/ck3chronicle/models/67303093ecda779d/semantic_projection_catalog.json:1) — 1–14082.
- [models/93196794a7e0115d/empirical_template_model.json](C:/Users/nateb/Documents/ck3chronicle/models/93196794a7e0115d/empirical_template_model.json:1) — 1–1.
- [models/93196794a7e0115d/manifest.json](C:/Users/nateb/Documents/ck3chronicle/models/93196794a7e0115d/manifest.json:1) — 1–1.

No runtime originals, review evidence, learner evidence/cache or databases are
included in these deletion lists. The old model content remains in existing Git
history; this task does not create a partial old revision or archive/export copy.

### Exact application connections

The existing console remains [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:24) 24–25,
`ck3chronicle.cli:main`; `cli.main` is 2754–2757. New command implementations
live in `pipeline/commands.py`. The changes below switch the precise existing caller and registration sites
to the new handlers.

| Existing edge / exact range | Final connection or deletion |
|---|---|
| [src/ck3chronicle/watcher.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/watcher.py:17) import 17–20; `watch_sessions` 468–625 | Change only the `InvalidCaptureInput`/`UnstableCapture` import to `pipeline.capture`. Keep lifecycle observation and callback behavior. |
| [src/ck3chronicle/cli.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/cli.py:22) `_spool_once` 22–39, import 30, call 33; `cmd_capture` 142–165; `cmd_watch` 168–527 | Switch the capture import to the ported `pipeline.capture.spool_logs`. Existing callback argument/result shape is supported by the actual port, not an old-provider adapter. |
| Same CLI `_capture_error` 74–99; callers at 137, 163, 225, 526 and 543 | Remove the old DB/capture mixed error helper; connect those remaining capture callers to the new `pipeline.commands.capture_error`. The old ingest and reconcile callers disappear with their handlers. |
| Same CLI `build_parser` 2395–2751 | Call new `pipeline.commands.register_commands` for pipeline surfaces. Keep capture 2406–2411, watch 2423–2444, doctor 2458–2459 and observe-logging 2473–2481 registrations. |
| ingest registration 2413–2421; handlers `cmd_ingest` 132–139, `_capture_once` 11–19, `_print_capture_result` 50–71 | Delete old handlers/registration; new `cmd_ingest` accepts an explicit current manual/recovery input and calls the canonical processor. |
| sessions registration 2453–2455; `cmd_sessions` 555–585 | Delete; new `runs` registration/handler lists current Runs. No `sessions` compatibility alias. |
| audit-db 2461–2471; `cmd_audit_db` 595–640 | Replace the registration with the new handler; delete old output/old-table/deep-distribution options. |
| review-queue 2519–2538; `cmd_review_queue` 861–942 | New handler shows Run review metadata/native shard reference. Delete payload queue and model/session-stage arguments. |
| report 2540–2565; latest 2567–2579; errors 2581–2600; old helpers/handlers 945–1231 | Delete those old bodies, including `session_intelligence` import at 1052; register new N8/N9 consumers. Use Run identity; remove `--session`, `--since`, projection/category/payload coupling. |
| process-pending 2602–2623; `cmd_process_one_pending` 1499–1614; helpers 1420–1496 | Delete old plan/journal/projection wrappers; register new explicitly selected pending-input handler. |
| reconcile 2446–2450 / handler 530–552; parse 2484–2500 / handler 682–721; classify 2502–2517 / handler 724–858; backfill-session 2625–2641 / handler 1617–1723 | Delete historical registration, repair/reparse/reclassify/backfill routes completely. |
| compare 2643–2668; baseline and nested commands 2670–2692; ignore and nested commands 2694–2717; handlers/helpers 1726–2126 | Delete unsupported comparison/baseline/ignore chain completely. |
| context 2719–2730 / handler 2129–2243; resolve-file 2732–2739 / handler 2246–2297; triage 2741–2749 / handler 2300–2392 | Delete old context-reparse and provisional source/triage commands. F1's pure grammar has its explicit new destination; no replacement feature commands. |
| Unregistered `_cmd_process_pending_wide_legacy` 1234–1417; `_log_type_from_relpath` 668–679 | Delete; no destination. |
| Proposed `rebuild-db` (new registration) | Explicit retained inputs and named fresh generation -> `pipeline.replay.rebuild_generation` -> `pipeline.processor.process_input`. No old DB reader or implicit active-DB replacement. |
| [src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:12) import branch 12–15 | Remove the unreachable old-Python import fallback; Python >=3.11 is already required. This is a specific final cleanup, not a configuration rewrite. |

Neutral configuration functions remain callable at
[src/ck3chronicle/config.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/config.py:38): `default_config_path` 38–40,
`load_config` 43–59, `_configured_path` 62–77,
`require_strict_descendant` 80–102 and `validate_project_containment` 105–140.
Preserve [src/ck3chronicle/command_envelope.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/command_envelope.py:1) 1–51.
The required new input/generation arguments are explicit; do not hide an old
schema reader behind configuration defaults.



### Bounded offline-tool edits

These are dependency and obsolete-tool removal edits, not a learner rebuild.
The algorithm remains in
[tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:916) 916–1099 and
the evidence registry in
[tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:44).
A later learner relocation/reorganization under `src/` is separate work.

| ID | Exact existing file/function/call | Required edit and reason |
|---|---|---|
| L1 | [tools/template_learning/learn_error_templates.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/learn_error_templates.py:35): import 35; `block_message` type annotation at 719; `collect_records` 1102–1159, lexer call 1108 | Reconnect to new `pipeline.domain.Emission` / `pipeline.emissions.iter_emissions`, adapting the precise field accesses if N1 requires it. The old lexer module is retired in 3.2. This is an offline consumer of the lexer, not a production call to the learner. |
| L2 | Same file: `LayeredClusterMatch` 309–333; evaluator-only `template_fixed_semantics_are_ordered` 806–844; unused `constant_tokens` 912–913; evaluator helpers 1162–1323; `evaluate_frozen_oracle` 1326–1482 | Remove code belonging to the obsolete tools listed in WORKPLAN 6.2 and this prompt's deletion list. The learning call chain `cluster_source_records -> derive_template -> choose_medoid/matching_pairs/infer_slot` uses the separate helpers at 916–1099 and continues in its existing file. |
| L3 | Same file: `write_report` 1533–1571; `parse_args` 1574–1599; `main` 1602–1682, oracle call 1630 | Remove mandatory oracle execution/arguments and its report/model evaluation fields so deleting the old tool chain does not break ordinary offline authoring. |
| L4 | [tools/template_learning/incremental_template_registry.py](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/incremental_template_registry.py:366): `build_revision` 366–473, oracle call 390/evaluation field 433; `parse_args` 500–526, option 520; `main` 529–540, forwarding 536 | Remove this same mandatory oracle dependency. Keep selected-evidence clustering/provenance and immutable candidate production. |
| L5 | [tools/template_learning/README.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/README.md:1); [tools/template_learning/AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/tools/template_learning/AGENTS.md:1) | Update the concrete remaining tool inventory and commands, including the old instruction to produce evaluator-style assignment counts in AGENTS.md 15–16. |

Production uses an already approved artifact. The current structural candidate
format and a complete approved direct-contract artifact are different product
units (owner intent 97–98; architecture 206–211). This project supplies the
current direct artifact in WORKPLAN section 7; it does not rebuild automatic learner
promotion or claim that a future candidate can be loaded without review.

Future candidate promotion must reconcile normalization version, structure and
the approved direct-contract fields. That producer/consumer interface remains
explicit; a new learner algorithm, unified normalization rewrite, source-folder
relocation or training campaign is not a prerequisite for constructing the
production pipeline from the existing selected structures.



### Model and package activation

Use the actual direct model/manifest paths and hashes from 1.3. The new catalog
already pins that revision and shares the normalizer identity. Switch
`pyproject.toml` package data at 29–34 to those exact two files while the CLI
begins using the new package.

Remove all five old artifact files listed above and all projection loader/
service/generator files in the deletion scope. Source and installed-package
selection must agree on the same direct revision. No loader accepts the old
pair as a secondary format, and no runtime path converts old data.

### Ordered implementation

1. Read the actual completed source handoffs together and reconcile every
   required caller against WORKPLAN 6.1. A missing implementation returns to
   its named owner; this prompt's edit list is not permission to finish
   arbitrary files in the new package.
2. Make the bounded L1–L5 edits and the exact CLI/watcher/config/package changes.
   The old learner lexer call reconnects to the actual new emission interface.
   Keep its clustering/derivation algorithm and evidence registry in their
   existing files.
3. Delete each explicitly named obsolete tool, provider, converter and old
   artifact after its required behavior has the named destination. Delete the
   obsolete command/helper registrations and their bodies completely.
4. Reconcile the import, same-file caller, table and resource map against the
   resulting source. Required product callers point to the new package;
   unsupported chains have their explicit deletion. Historical source
   references in this plan are evidence, not reasons to retain providers.
5. Apply the exact documentation updates below using implemented facts only.
   Report the separate evaluator/tests/CI disposition under its own approved
   scope; do not silently classify those known consumers as finished.
6. Supply the entry-to-exit path comparison for all creations, edits and
   deletions, including untracked/ignored state. If another task changed a
   file during this work, identify that change separately rather than claiming
   it as this mini-project's permitted edit.

### Scoped documentation updates

| File / current locations | Treatment |
|---|---|
| [models/README.md](C:/Users/nateb/Documents/ck3chronicle/models/README.md:7), 7–54; [pyproject.toml](C:/Users/nateb/Documents/ck3chronicle/pyproject.toml:29), 29–34 | Current selected artifact/packaging; remove projection and superseded active revision instructions. |
| [docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253), 253–310, 332–382, 412–423 | Align implementation/identity/storage/retention descriptions with current owner intent and the new pipeline package and flow. Old one-week source expiry and migration prescriptions are superseded. Verification sections beginning at 425 remain assigned to the separate verification-design task. |
| [docs/DATA_COMPATIBILITY_AND_OPERATIONS.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATA_COMPATIBILITY_AND_OPERATIONS.md:12), 12–38, 69–82, 125–218, 220–334 | Reconcile supported command/storage/retention/operation descriptions; remove compatibility/migration prescriptions. Do not derive new release or verification conditions from old text. |
| [docs/MODEL_QUALITY_AND_PROMOTION.md](C:/Users/nateb/Documents/ck3chronicle/docs/MODEL_QUALITY_AND_PROMOTION.md:137), 137–147 | Replace historical in-place reclassification/source-expiry operational claims with fresh-generation behavior. Its measurement/promotion-verification design is outside this workplan. |
| [docs/PROJECT_PLAN.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_PLAN.md:48), active-exercise section 48–63; [docs/PROJECT_STATUS.md](C:/Users/nateb/Documents/ck3chronicle/docs/PROJECT_STATUS.md:71), runtime/gap sections starting at 71 | Record the actual implementation status when it exists. Do not propagate historical approval claims, measurements or deleted prompt routes as authority. |
| [docs/REPOSITORY_AND_BACKUP.md](C:/Users/nateb/Documents/ck3chronicle/docs/REPOSITORY_AND_BACKUP.md:17), ownership sections starting 17/29; [docs/WORKSPACE_ROUTING.md](C:/Users/nateb/Documents/ck3chronicle/docs/WORKSPACE_ROUTING.md:1) | Update actual source ownership where it changes; no new archive/backup project. |
| [AGENTS.md](C:/Users/nateb/Documents/ck3chronicle/AGENTS.md); [README.md](C:/Users/nateb/Documents/ck3chronicle/README.md); [docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md); [docs/CURRENT_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/docs/CURRENT_HANDOFF.md) | These already direct the current architecture/planning. Change only actual implemented command/owner/continuation facts. Do not apply stale recovery-review line edits or mark implementation completed early. |
| [docs/BANNED_IDEAS.md](C:/Users/nateb/Documents/ck3chronicle/docs/BANNED_IDEAS.md); [docs/OWNER_PRODUCT_INTENT.md](C:/Users/nateb/Documents/ck3chronicle/docs/OWNER_PRODUCT_INTENT.md) | Authority inputs; no policy rewrite required by this implementation. |
| [docs/DEVELOPMENT_RESTART_AUDIT_2026-09-08.md](C:/Users/nateb/Documents/ck3chronicle/docs/DEVELOPMENT_RESTART_AUDIT_2026-09-08.md); [docs/DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md](C:/Users/nateb/Documents/ck3chronicle/docs/DATABASE_REBUILD_POLICY_DISCUSSION_2026-09-09.md) | Historical/background inputs; no implementation change required. The deleted operational recovery plan and rejected earlier prompts stay deleted/unread. |

The documentation table's authority/background rows are read inputs, not
additional mutation permissions. The explicit edit table above controls.

### Deliverable

Report the actual supported commands and their sole current service paths;
selected direct revision and package resources; all source/tool/artifact
deletions; precise offline changes; and the remaining separate verification
status. Account for each dependency-map finding and each allowed file.

The source switch does not itself run a capture, build a production generation,
replay retained logs, replace the active database, commit or publish changes.
Finish with the required file-scope proof. Declare the overall implementation
complete only when the commissioned source work and separately supplied
verification-consumer disposition are actually complete.
