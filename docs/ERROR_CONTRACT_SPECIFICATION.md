# Approved Error Contract specification

## Implementation interface note — 2026-09-27

2026-09-28 selected v45 integration: schema-5/API-v2 definitions can declare
finite line-label literals. Their selected body/wrapper layouts carry ordered
literal-choice indices, preserved through preparation, exact identity and rendering.
This uses the approved selected-layout rule below, not variable slot content or
normalization. Package `68f1ae5db205ab46afef9c4d` is now selected and verified
through SQLite/review persistence and independent rendering. See
[storage integration](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md) and the
[learner assessment](LEARNER_RELEASE_V45_RESULTS.md).

Implemented in [Task 05](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md). The
new public result preserves the shared matcher outcomes `template`,
`provisional`, `no_match` directly; the `full`/`unknown` names in the historical
acceptance table below describe the retired pipeline interface. Eligibility and
all approved contract rules are unchanged. Task 06 now supplies SQL, Run
aggregation and native review; application/provider cutover remains later.

Approved by the owner on 2026-09-27: “great, I approve of your proposed error
contract.” This approval includes the subsequent clarification that source/emitter
is stored with the SQL template definition and available through every diagnostic
record's template relationship. It need not be compared again during aggregation.

This is the complete approved Task 04 specification, recorded from the conversation.
It governs Task 05 over older prompts, layered-matching proposals and provisional-
only-to-review instructions. Implementation status is separate: see
[Task 04 handoff](TASK04_ERROR_CONTRACT_HANDOFF.md).

## Representation and authority

An Error Contract is an existing published template definition plus the common
storage rules below. Definitions stay embedded in `empirical_template_model.json`.
Use the verified selected model, parser, declarations and matching/selection package.
Task 05 integrates the independently verified shared matcher while preserving the
model definitions; the current pin and transition are in its executable prompt.
There is no new per-template contract
ID, diagnostic taxonomy or required `error_contracts.json` sidecar.

Version the common rules with the application as `error-contract-v1` and record
that version in Run metadata. The selected model manifest identifies the exact
template definitions; a separate model publication is unnecessary for these
common rules. A diagnostic record means the refined, unique error message stored
in SQL. Parser objects and classification results are transient processing data.

The owner-directed storage rules supply acceptance, identity and rendering.
Published definitions supply literals, slot definitions, applicability and declared
validation. The published selector supplies one complete assignment and its status.
Learning support does not become an additional pipeline approval gate.

## Fields and ownership

| Field or rule | Ownership / scope | Required meaning |
|---|---|---|
| `template_id` | Definition; every selected assignment | Existing template ID, interpreted under the Run's model revision. |
| Literal text and slot placements | Per-template definition | Ordered literal/slot parts, selected surrounding parts where present, and supporting-entry layouts where declared. |
| Slot identifier and type | Per-template definition | Existing positional identifier and published type. Semantic slot names are unnecessary. |
| Optionality and constraints | Per-template definition, when declared | Exactly the model's declarations; examples do not create additional restrictions. |
| Source/emitter applicability | Per-template definition | Enforced during assignment. Store with the SQL definition so every record can expose/filter it. |
| Selected layout choices | Occurrence, where alternatives exist | Which declared surrounding/entry layouts were used, preserving their order. |
| Ordered slot bindings | Occurrence; every assigned slot | Position/region, type and exact value. Absent optional content is distinct from present empty content. |
| `match_status` | Selected assignment; every stored record | `template` or `provisional`, derived from the final classifier outcome. |
| `occurrence_count` | Diagnostic record; universal | Number of identical assigned occurrences within one Run, initially one. |
| `error_type` | Universal initial rule; stored record | `unknown`. Later typing is an approved extension, not a current eligibility dependency. |
| Representative provenance | Record; one representative occurrence | Preserve original region/binding byte spans and contributing emission ordinals for traceability. Repetitions increment the count. |
| Processing lineage | Run metadata; universal | Model revision, selected package ID/manifest hash and matcher API, parser identity/hash, assignment-policy version, classifier/application revision, contract-rules version and database schema version. The package manifest pins the exact model bytes and executing matching dependencies. |

Slot placements locate values in the template's render layout. Original byte
spans locate evidence in the retained log; they are different data and are not
diagnostic-identity participants. Keep exact values, including punctuation,
whitespace, numeric spelling and opaque full identifiers.

The current release declares KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM, REASON,
CHARACTER_FULL_ID, HOUSE_FULL_ID and TITLE_FULL_ID. The last three were delivered
through the learner team's owner-directed full-ID work. The current
[native model contract](LEARNER_NATIVE_MODEL_CONTRACT.md) defines their boundaries.
The pipeline consumes these declarations without decomposing their contents.

## Acceptance and validation

Owner clarification on 2026-09-27: implementing this contract must preserve the
mini-project's cleanup obligations. The pipeline executes pinned recovery,
model-directed complete matching/selection and binding, then prepares compliant
record data. Additional semantic interpretation, reclassification, raw-message
reprocessing and regrouping are removed. Required declared validation remains in
its owning matching stage. Exact-identity occurrence counting remains the approved
downstream aggregation. Removal of an old port instruction does not waive cleanup.
The owner subsequently separated the complete-path audit into
[Task 04(B)](04B_PIPELINE_PROCESSING_AUDIT_RESULTS.md). Following review and
shared-matcher verification, the owner assigned package integration, selected-only
binding and duplicate pipeline matcher retirement to Task 05. The contract rules
remain unchanged; general application cutover remains a later assignment.

Consume the classifier's single `selected` assignment:

| Classifier result | Contract/storage disposition |
|---|---|
| `full`, with selected assignment | Eligible; SQL `match_status = template`. |
| `provisional`, with selected assignment | Eligible; SQL `match_status = provisional`. |
| `unknown`, no selected assignment | Native review shard. |
| Unresolved parser/recovery evidence | Native review shard or explicit parser failure under the existing recovery policy. |

The published selector resolves competing complete assignments and capture ties.
A deterministic tie-break remains provisional and eligible. SQL does not store
competing-template lists, ranks or research alternatives. Use final outcome rather
than the selected template's support label: a supported template can win a tie
whose final outcome is provisional.

Matching already validates source applicability, complete literals, declared slot
boundaries/constraints and supporting-entry requirements. Binding already checks
values against original bytes. Contract preparation checks completeness and
internal correspondence of that result; it does not tokenize, match or bind the
message again, introduce semantic conditions, or independently rank candidates.
Inconsistent results are explicit implementation/integrity errors, not ordinary
no-match evidence. Separate L1/L2 assignment is superseded by complete templates
with intact REASON and, where supplied, complete supporting components.

## Diagnostic identity and counts

Within one Run, equal records have the same selected template and literal layout,
with the same ordered typed binding values. All slots participate, including
LOCATOR, PARAM, REASON and full-ID values. Include declared absence/presence,
selected layout alternatives, and supporting-entry number/order/content.

Different slot values create different records even under the same template.
Absolute byte offsets and timestamps do not split records. Source applicability
has already been resolved by the template assignment. Run lineage scopes the
definition revision; no additional source comparison or semantic field registry
is required. Each repeated complete error adds one occurrence. Supporting entries
belong to that complete error and do not receive independent record counts.

Store occurrence counts, not individual occurrence timestamps or diagnostic
first/last timestamps. Existing Run capture and lifecycle times remain Run facts.

## SQL representation and rendering

Store each used template definition once in SQL, retaining literal text, ordered
slot placements/types and source/emitter. Each diagnostic record references that
definition and contains selected layout choices, ordered bindings, match status,
occurrence count, error type and representative provenance. Lineage belongs to
the Run. Physical table/column organization belongs to later storage implementation.

Render by walking stored literal/slot parts and substituting exact binding values.
An absent optional slot omits its declared prefix/value/suffix; a present empty
value remains present. Preserve literal punctuation, spacing and line endings.
Retain every selected surrounding part and ordered supporting entry. Render an
opening followed by its entries as one complete error, without log-header times.

Reports use these stored definitions and values alone. A second complete-message
string is unnecessary. Default reporting includes template and provisional records;
`match_status` provides an easy filter. Source/emitter is available through the
definition relationship. Rendering requires neither raw logs nor model files.

## Population and implementation boundary

These common rules apply mechanically to every complete selected assignment from
the approved release, including provisional selections. No per-template manual
authoring or additional error-type approval is required. Unassigned evidence
remains reviewable; complete accounting does not require complete model coverage.

Task 05 integrates the shared matcher, retires the duplicate pipeline matcher and
implements contract/result preparation, deterministic identity and rendering
helpers. Later work implements aggregation, SQL definitions/records, native review
publication and stored-report integration. Application cutover is separately
commissioned. The representative native cases and verified interfaces are in the
[handoff](TASK04_ERROR_CONTRACT_HANDOFF.md); the executable assignment is
[the revised Task 05 prompt](05_ERROR_CONTRACT_IMPLEMENTATION.md).
