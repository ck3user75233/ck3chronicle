# Native outer-diagnostic model contract

Current development: learner v41 / schema 4 adds a repeated supporting-component
contract for parser v1.7 groups. See [the continuation ledger](LEARNER_CONTINUATION_MODEL_STATUS.md).
The body remains the opening's original region; `continuation` defines ordered
entries with a reference to its CHARACTER_FULL_ID capture and a displayed-title
PARAM. Selection returns `component_matches` with entry indices and captures
relative to each entry's original body. No joined-display offsets or standalone
entry diagnostics. Hash-covered assignment.py (policy v2) and continuations.py
ship with the model. Runtime classifier v7 loads these from the selected release
and exposes one selected supported/provisional assignment. Publication/pin status
is recorded in the ledger and models/selection.json; historical sections below
describe earlier deliveries.

Development extension v35: `TITLE_FULL_ID` uses the same `full_id` declarations
and constraints as CHARACTER_FULL_ID/HOUSE_FULL_ID. All three are opaque complete
captures. The three declared title contexts retain surrounding diagnostic wording
outside the field. Existing published models need no migration. See
[the v35 ledger](LEARNER_V35_IMPLEMENTATION.md); this is not a new release pin.

Owner-authorized development extension, v33 (2026-09-26): add CHARACTER_FULL_ID
and HOUSE_FULL_ID. Their complete name/ID contents are opaque before grouping
and at matching. Definitions are in the existing owner JSON declared-field
registry with `mechanic: full_id`; slot constraints carry
`full_id: {definition, source}`. Both active routes consume `full_ids.py` rather
than maintaining separate recognition logic. Recognition preserves exact raw
pieces and byte ranges; the parser and capture API are unchanged. This candidate
extension is not a publication or ingestion activation.

Learner v30 development update (2026-09-25): no templates are imported or retained
as frozen seeds. All candidates are rediscovered from selected native evidence.
Registries and caches are private to one learner version/implementation identity;
new versions require fresh state populated from explicitly selected original logs.
This is cumulative batch learning, not incremental hypothesis updating. See
[the current investigation](LEARNER_VERSION_ISOLATION_REVIEW.md). Publication is
separate; `models/selection.json` remains authoritative for the selected release.

Published 2026-09-24: **a9fa27a85ccd066285b99fdb**, selected explicitly in
models/selection.json. The [existing formal handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md)
is the current integration entry point. Application caller migration remains
pipeline-owned. Publication preserves supported/provisional/confirmed statuses;
it does not confirm all patterns or activate ingestion.

The compact release manifest is ck3chronicle.native-model-release v1; its model
remains schema 3. It omits observed values, member ranges and research hypotheses
while retaining all executable parts, constraints, declarations, context patterns,
source applicability and support summaries. Full native evidence stays outside Git.
Use publish_native_model.load_release with an externally selected manifest hash.
Raw parser artifacts are immutable within each release.

Current contract: schema 3, owner-authorized 2026-09-22. The raw parser stays
v1.6. [Implementation status](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md) records
progress, native verification and remaining issues.

## Learning and matching unit

A candidate describes a complete recovered diagnostic message in one source
family. Locations and traces belong to this candidate. There are no independent
L1, L2, prefix or tail learning pools and no component-candidate acceptance gate.
All supporting field observations come from that candidate's member records.
Existing recovered-message wrapper context is retained and evaluated with the
candidate; the parser's emission recovery is unchanged.

`owner_rules.json` contains `constructions`: explicit owner-approved envelope
regexes, source scope, named ranges, fields, and the ranges carrying diagnostic
wording for comparison. `constructions.py` is a generic consumer. Adding a CK3
construction requires a declaration and owner authority, not a source-name or
sentence branch in the inference code.

For the established script-system envelope, the bracket interior is an intact
REASON field. Prefix, failure wording, brackets, whitespace, locations and trace
content all remain in the outer pattern. The declared failure region supplies
wording similarity so repeated boilerplate and arbitrary reason contents do not
inflate it. Complete native messages still participate in alignment, field
assessment and matching. This is a comparison view, not a separate learned head.

The same observed envelope without a bracketed reason is declared separately,
with its failure wording as the comparison region and no prescribed slot types.
Its `excludes` reference keeps bracketed messages under the REASON declaration.
This prevents common headers and traces from grouping unrelated unbracketed
failures into an `Error: <PARAM>` template.

## Slot types

Declared-field correction (v26, 2026-09-24): a field whose registry declaration
sets `allow_empty: true` may capture an empty string with a zero-length, non-null
span `[p,p]` at an actual raw-piece boundary. This is present empty content, not
absent OPTIONAL_KEY. Script REASON now permits this. Complete whitespace runs
between the brackets and reason, including line endings, remain literal; the
raw parser never splits a gap for the field. Inference emits an empty declared
unit once and then continues at the same piece boundary. Ordinary PARAM, KEY
and other field evidence requirements are unchanged.

| Type | Meaning |
|---|---|
| KEY | Complete native identifier, including adjacent colon-qualified segments across separate raw tokens at an empirically varying position |
| OPTIONAL_KEY | KEY or observed absence, including explicitly represented surrounding whitespace |
| VALUE | Native numeric text, without implicit conversion |
| LOCATOR | Recognized complete path/file or line field; labels and separating punctuation remain literal |
| PARAM | Empirically supported variable-length raw span, including punctuation; candidate-local field evidence is required |
| REASON | Exact content of an owner-declared reason field; no independent reason template or categorization required |
| CHARACTER_FULL_ID | Complete variable-length character name, terminal `of`, optional single raw-token key, and ID parentheses; exact opaque content with JSON-declared emitter boundaries |
| HOUSE_FULL_ID | Complete variable-length house name and ID parentheses in a declared house emitter; internal values, including empty values, remain opaque |

No optional literal parts exist. Parentheses do not assign PARAM. Presumed
literal guidance is now disabled under owner direction. All newly built slot
`literal_guidance` constraints are empty. Declared traces and empirically
supported variable fields supply PARAM evidence; the former bypass variation
requirements, while the latter do not.

Algorithm v23 extends KEY through `constraints.key_joiners`, currently `[":"]`,
as declared in owner_rules.json. Segments must be complete non-punctuation raw
tokens with no intervening whitespace; only the declared separator may join
them. Inference and matching use the same syntax. This supersedes the earlier
single-token-only KEY description, without merging parser pieces. LOCATOR
recognition retains precedence. Pipeline consumers must honor this constraint
when integrating the published release. Application activation remains separate.

Algorithm v24 proposes balanced outer interiors before aligning interior wording.
PARAM evidence uses distinct values and actual raw token counts: punctuation
counts, whitespace gaps do not. Neither whitespace, nested content, an alternating
word/separator shape, nor unequal observed lengths is required. Repeated interior
wording remains opaque in a supported region. Fixed contents remain literal.
Simpler KEY/LOCATOR syntax retains precedence; a colon-qualified KEY cannot
supply PARAM evidence merely because another member fails KEY. Failure of simpler
type checks alone is still insufficient. Boundary validation and complete member
capture agreement remain separate checks. Equal observed lengths impose no
fixed-length matching restriction.

The earlier phrase/whitespace and nested-content requirements were assistant
heuristics, not owner requirements. They are removed, including the special
alternating-sequence evidence path. Optional empirical_region provenance now
records raw_token_counts, distinct_nonempty, multi_token_content and
observed_length_variation; it does not affect matching identity. General
word-bounded discovery remains limited; its four-value review threshold is an
engineering hypothesis recorded in the registry, not owner authority.

The existing owner-approved character-history declaration captures the description
following Character: through its balanced ID parentheses as ordinary PARAM.
Its source, prefix, required marker and mechanics remain explicit registry data.
That declaration is distinct from empirical PARAM discovery; the native Parent
outer region is empirically inferred. No new CK3-specific declaration was added.
Unsupported discovery fields retain separate formulations; PARAM is not a fallback.

## Candidate artifacts

The immutable bundle retains `empirical_template_model.json`,
`native_evidence.json`, `parser.py`, `parser-manifest.json` and a manifest of
hashes. Model schema is `ck3chronicle.native-message-model`, version 3;
`record_scope` is `message`. Schema 2 candidates are historical evidence, not a
runtime or learner fallback. The dedicated comparison report reads the previous
saved results without running their contracts through the new matcher.

The model has `templates`, `constructions`, `owner_rules`, `slot_definitions`,
`algorithm`, `diagnostic_policy`, `region_discovery`, input evidence identities
and summary counts. It has no `layers_by_source` or component template IDs.
The implementation hash includes the declaration consumer and JSON reference.
Loading validates construction declarations, the full rule registry and the
inference algorithm revision against the selected learner;
a changed declaration requires an explicit rebuild/review rather than silent
reinterpretation of a saved model.

Each template retains source family, context kind, optional construction ID,
ordered `parameter_structures` for outer-message structure selection,
ordered literal/slot parts, candidate member record IDs, support occurrence and
unique-message counts, inference refinements, hypotheses and unresolved members.

Each outer candidate has learning_support: distinct_messages,
distinct_nonlocation_examples, minimum_distinct_examples (2), and eligible.
Exact repeats and LOCATOR-only variation do not increase independent support.
Different examples within one log can suffice; multiple logs are not required.
All hypotheses remain in templates for inspection, with explicit status:
provisional (insufficient support), supported (enough empirical examples),
confirmed (explicit review), or unresolved (failed inference validation).
Supported does not mean semantically correct or promoted. Summary counts separate
supported_templates and provisional_templates from total hypotheses.

Only supported/confirmed candidates can produce full outcomes. Provisional matches
retain captures in matches, but the row has no accepted template_id/captures.
provisional_reasons distinguishes insufficient_distinct_learning_examples from
competing_templates and ambiguous_capture_boundaries. v30 has no confirmation
command or template-seed loading. Context-wrapper patterns
remain structural components, not separately accepted diagnostics.

Each slot retains observed values, ordinary inference basis and `field_support`:
member record identities, raw-piece ranges, UTF-8 byte ranges, token-count and
punctuation variation. PARAM support additionally records its field assessment
and any local relaxation of presumed literals. Evidence metadata does not change
structural template identity; capture constraints do.

Trace declarations supply ordinary PARAM fields without empirical variation.
Their `parameter_definition` identifies inference provenance, not a slot subtype
or a capture constraint. Declared spans are excluded from wording comparison and
ordinary alignment. Before ordinary matching, the candidate's complete-message
structure must agree with the recognized declaration presence/order.

Owner correction 2026-09-24: a file/line location is not part of its following
trace PARAM. Remove the former whole-chain `script-location-frames` declaration;
use the general file/line-introduced balanced parenthetical interior. This yields
`file: <LOCATOR> line: <LOCATOR> (<PARAM>)` for each native frame. Labels and
parentheses are literal. Actual trace words, punctuation and token count remain
opaque; the file and line are ordinary, directly bound LOCATOR slots. No nested
extraction interface is used. Under the existing flat template representation,
different numbers of file/line frames can require separate templates; this is
distinct from varying token counts inside a single trace PARAM.

Current constraints include complete parser boundaries, single token or approved
KEY join syntax, numeric
text, line reference, location syntax, literal guidance, supported delimiter
balance, and a declared field reference (`construction`, `field`). The generic
REASON matcher resolves that declaration against each actual complete message;
it never reuses an earlier message's numeric offsets.
Matching also requires the candidate's construction identity to agree with
the actual message. An ordinary candidate cannot bypass a declared REASON
field by absorbing the same message into a broader PARAM.

## Outcomes and persistence boundary

Research matching records `full` (one sufficiently supported candidate with one
complete capture assignment), `provisional` (insufficient learning evidence,
competing templates or capture assignments) and
`unknown`. A memoized search counts every complete assignment. It does not stop
at the first successful division of a PARAM. `capture_ambiguities` holds the
exact assignment count and two complete witnesses; `matches` holds uniquely
captured candidate alternatives. Context-wrapper ambiguities are also retained.
The bounded witness display does not truncate the search or its count.
There is no preferred-match suppression or separate L1-only outcome. Each
native evidence row retains raw pieces, native occurrences, contexts,
construction ranges, complete matches, capture ambiguities and actual captures.

Field captures and literal content must reconstruct the original diagnostic
exactly. Variable-length fields shift subsequent literal positions without
requiring fixed token ordinals. Candidate-local provenance must remain correct
after membership changes and candidate consolidation.
For its own native members, a candidate must also reproduce the exact field
spans used in inference. Byte reconstruction alone cannot establish correct
assignment when wording repeats. A failed proposed union is rejected; a failing
initial candidate remains unresolved. These member spans are verification
evidence, not fixed offsets imposed on new messages: matching still follows
literals and variable-length raw spans in each actual message.

Owner correction (v30): remove confirmed-template retention and its discovery
bypass completely. No previous template or review decision exempts native evidence
from rediscovery. A candidate matching its training messages does not establish
semantic correctness. The current published release has no individually confirmed
templates. New learner candidates require separate publication review.

The pipeline team owns application loading, matching integration and SQL
acceptance. A stored diagnostic must contain the content needed to understand
it, including the complete reason and location/trace captures; reports must not
need an emission-record join or source-log reread. Occurrence deduplication is
downstream of parsing and matching.

## Filename and line fields (v1.5)

A path/file.txt:6 formulation has separate path and line LOCATOR captures with
a literal colon between them. The parser returns file.txt, :, 6 at its tail.
Line ranges such as 6-9 stay native text; LOCATOR's line_reference constraint
requires decimal digits with an optional hyphenated decimal endpoint.

The owner-supplied .txt/.yml/.md/.py suffix cues identify bare filenames without
requiring a slash. Generic filename shape is also sufficient in explicit file
context, a slash-delimited path, or filename:line notation. A dot alone does
not establish a filename: scope.culture and event.0001 remain identifiers absent
location evidence. These suffix cues are explicit in owner_rules.json and do
not enumerate directory names or claim exhaustive filename-extension coverage.

In an explicit file field, filename content may span space gaps up to its
filename ending. The native history/characters/00_NEW CHARACTERS.txt is one
path capture containing those spaces and existing segment/slash tokens. A
following line label remains literal. Slash-separated lists without a file
context do not acquire a location merely because they contain spaces/slashes.

Matching now requires a complete range recognized by the same location syntax
and context used during inference. A single arbitrary word cannot satisfy a
bare filename LOCATOR. Current consumers must apply the selected declarations;
no model/text normalization or token reconstruction is permitted.
