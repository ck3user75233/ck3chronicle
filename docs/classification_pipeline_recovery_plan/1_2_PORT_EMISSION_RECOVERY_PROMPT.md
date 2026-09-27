# Mini-project 1.2 — Port emission recovery and original-value binding

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`high`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the stage coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_1_CLASSIFICATION_CORE_ORCHESTRATOR_PROMPT.md).
This prompt defines the implementation scope and deliverable; preparing it
does not authorize running it.

## Outcome and entry

Consume 1.1's concrete emission, child-span and binding interfaces. Build the
stream from original error-log bytes to source-specific recovered diagnostics
and typed matching views. WORKPLAN 1.1/1.5 defines the emission/review units;
WORKPLAN R1–R4 and N2 define the source ports.

## Exact mutation scope

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

## Exact source ports

| ID | Existing source and scope | Destination and treatment |
|---|---|---|
| R1 | [src/ck3chronicle/parser/log_blocks.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/parser/log_blocks.py:26): `TimestampedLogBlock` 26–46; `source_block_id` 49–58; `_without_line_ending` 61–66; `_decode` 69–70; `_parse_header` 73–98; `_make_block` 101–139; `iter_log_blocks` 142–257; header/source/BOM definitions 16–23 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/emissions.py`: port lexer mechanics into `iter_emissions` and its private helpers; emission data moves to `pipeline/domain.py`. Supply real provenance explicitly. Omit the two-bracket fixture header at 19–21/86 and old constructor defaults. Decoded text is not the native review copy: preserve original byte spans. |
| R2 | [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:253): `block_message` 253–263; `split_location_evidence` 266–270; `extract_structured_slots` 273–422; `normalize_key_path` 425–437; `normalize_structured_slots` 440–501; `normalize_known_key_grammars` 504–592; `mask_locators` 626–631; `tokenize` 634–642; `script_system_layers` 645–670; `diagnostic_lead` 673–718; `reason_lead` 762–768; their constants/regex definitions 13–250 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py`: port these pure routines and their grammar definitions. Adapt block access to new emissions/diagnostics; remove the 384-token truncation at 638. Preserve a separate original-value binding view. Do not port `legacy_diagnostic_lead` 721–759. |
| R3 | Same [src/ck3chronicle/classification/normalize.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/classification/normalize.py:595): `_normalize_persistent_clause` 595–603 and `semantic_units` 606–623, specifically wrapper/clause recognition at 608–620 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/diagnostics.py`: port only the recognized persistent-reader splitting grammar into `recover_diagnostics`; write child spans/value ownership afresh (N2). Do not port lossy string normalization as the recovery result. Normalization follows recovery. |
| R4 | [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:135): `_path_from_match` 135–140; `_overlaps` 143–144; `_extract_locators` 147–181; supporting path patterns 39–77 and `_EVENT_URI_RE` 80; `LocatorEvidence` 97–102 | `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py`: port pure path/line extraction, adapted to preserve source spans and original spelling. Keep event URIs distinct from filesystem paths. Define the current locator value in `pipeline/domain.py`. Nothing else from the projection module is a port: typed values come from R2 and N2, not a post-classification mapping dispatcher. |

## Implementation steps

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

## Port boundaries

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

## Deliverable and following work

Deliver `iter_emissions`, `recover_diagnostics`, `normalize_for_match` and
`bind_original_values` in the four scoped files. Explain the actual data
path from original bytes to a child diagnostic's normalized tokens and original
values, with source/function references from the implementation.

Pass those interfaces and the normalization identity to 1.3. Pass native-byte
access and parent/child identity requirements to 2.1/2.2. The future offline
lexer caller changes belong to 3.2, where the old lexer is retired. Finish with
the required file-scope proof.
