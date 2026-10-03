# Shared native matcher API v2

2026-09-28 Task 06 integration: package `68f1ae5db205ab46afef9c4d` is now
selected for source and installed runtime resources. API-v2 choices have passed
preparation, aggregation, SQLite/native-review completion and SQL-only rendering.
See [integration details](TASK06_V45_STORAGE_INTEGRATION_HANDOFF.md).
Earlier non-activation statements below describe delivery-time history;
application/provider cutover and production processing remain separate.

## Schema-5 delivery interface — 2026-09-28

The checkout's learner v45 builds schema-5 models with `ck3-native-matcher-v2`.
The selected immutable schema-4/API-v1 package documented below is unchanged.
The new loader accepts schema 5/API v2 explicitly; no legacy package is rewritten.

A literal part may declare `location_label: "line-location"` and
`alternatives: ["line:", "near line:"]`, with canonical `text: "line:"`.
Validation requires the exact owner-declared, nonempty, prefix-free alternatives
immediately before a mandatory numeric LOCATOR (only horizontal whitespace may
intervene). Such parts are literals, not captures. Every remaining complete-match
condition and the assignment policy remain in force.

For each selected body or wrapper with alternatives, its existing `layout`
additionally contains `literal_choices: [[part_index, alternative_index], ...]`
in part order. The matcher verifies these choices against the native region and
checks exact reconstruction with the selected captures. Contract rendering uses
only those declared indices and stored definitions/values; missing/invalid choices
fail explicitly. Choices participate in exact diagnostic identity. No normalization,
new slot type or matcher fallback is introduced. See the
[73-log release assessment](LEARNER_RELEASE_V45_RESULTS.md),
[exact package delivery](LEARNER_PARSER_PIPELINE_HANDOFF.md) and earlier
[literal-choice verification](LEARNER_LOCATION_LABEL_EQUIVALENCE_RESULTS.md).

## Earlier API-v1 pipeline integration checkpoint — 2026-09-27

Task 05 selects the earlier immutable API-v1 package. See
[the implementation handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md) for
the new public pipeline/contract interfaces, native replay and installed proof.
The candidate/non-activation statements below describe the original learner
delivery. Application/provider cutover remains later.

This is a candidate delivery, not an application cutover. The active model
selection remains unchanged. The current package identity and verification are
in [the pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md).

## Loading and compatibility

`matcher_loader.load_package(folder, expected_manifest_sha256=...)` accepts an
explicit local directory and an externally pinned manifest digest. It checks
the complete artifact set and hashes, canonical package/model identities,
model/parser/declaration agreement, matcher API, selector policy and template
declarations before exposing a matcher. It executes the verified payload bytes
in a private Python namespace whose import search path is empty.

The bootstrap is itself hashed. Consumers must authenticate its bytes before
executing it; [matcher_example.py](../tools/template_learning/matcher_example.py)
does this. No `template_learning`, `ck3chronicle`, installed application,
mutable owner-rule file, registry or inference state is required. Python 3.11+
and its standard library are required. The supported tuple is:

- package schema `ck3chronicle.native-matcher-package`, version 1;
- matcher API `ck3-native-matcher-v2`;
- native model schema 5;
- parser `ck3-lossless-v1.7`, with the model's exact implementation digest;
- selector `complete-assignment-v2`, with the packaged implementation digest.

Package identity is separate from model identity. The manifest hashes every
payload, including the bootstrap, matching primitives, model validator, public
API/recovery adapter, full-ID helper, continuation helper, selector and parser.
The original model's `algorithm.implementation_hashes` remain historical
training lineage. They do not describe the newly extracted executable matcher;
the package manifest does. `native-validation.json` records replay of the compact
export against the complete candidate evidence; independent package replay is
linked from the handoff. The old selected package retains its own API-v1 loader
and model schema. Neither package is adapted or rewritten to load as the other.

`LoadedPackage` exposes:

```python
package = loader.load_package(folder, expected_manifest_sha256=pin)
raw = package.parse_file(complete_native_log)
for unit in package.iter_units(raw):
    if unit['recovery_status'] == 'unresolved':
        # Retain the supplied recovery/provenance for native review.
        continue
    result = package.match(unit)  # one selected assignment or explicit no_match
definitions = package.data  # defensive snapshot of the supplied model
```

`iter_units` is an optional projection of the pinned parser's existing ranges.
It neither recognizes new boundaries nor joins or rewrites messages. Pipeline
readers can construct the same input directly from their pinned parser objects.

## Input

`package.match(unit, inspect=False)` takes one complete recovered unit:

```python
{
    'parser': {'version': 'ck3-lossless-v1.7', 'sha256': parser_digest},
    'recovery_status': 'recovered',
    'source_family': source_without_terminal_cpp_line_number,
    'source_tag': original_emitter_tag,  # optional; passed through
    'context_kind': 'body',  # or located-message-wrapper / continuation:<rule>
    'body': {'text': original_body, 'pieces': [(kind, exact_text), ...],
             'provenance': caller_owned_body_association},
    'contexts': {},  # wrapped units require both prefix and suffix regions
    'continuations': [],  # ordered original supporting regions
    'provenance': caller_owned_unit_association,
}
```

A wrapper region has the same text/pieces/provenance shape as `body`.
Each continuation additionally has `prefix_span`, `label_span`, `value_span`,
the parser's half-open byte spans relative to that continuation's original
body. These framing spans must coincide with native piece boundaries. They
are not inferred by the matcher. A continuation kind requires entries, and
ordinary/wrapped kinds cannot silently omit or ignore supporting entries.

`kind` is `token` or `gap`. Concatenating the supplied pieces must reproduce
the region text exactly. Matching uses complete literal/slot layouts, supplied
source and structure declarations, declared constraints and all complete
capture alternatives. No ordinary KEY-to-PARAM fallback, semantic typing,
message cleanup or second tokenization occurs.

The complete matcher accepts all nine approved types: KEY, OPTIONAL_KEY, VALUE,
LOCATOR, PARAM, REASON, CHARACTER_FULL_ID, HOUSE_FULL_ID and TITLE_FULL_ID.
The full-ID types remain opaque, including internal empty values. Error typing
remains `unknown` in the downstream contract; the matcher does not assign types
to errors.

## Result and layout references

Ordinary result:

```python
{
    'api_version': 'ck3-native-matcher-v2',
    'status': 'matched',  # or no_match, with assignment=None
    'source_family': source,
    'source_tag': original_emitter_tag,
    'provenance': caller_owned_unit_association,
    'assignment': {
        'template_id': selected_template_id,
        'template_status': original_support_status,
        'match_status': 'template',  # or provisional, from final selector outcome
        'regions': [
            {
                'name': 'body',
                'layout': {'template_id': selected_template_id, 'region': 'body'},
                'captures': [
                    {'slot_id': slot_name, 'type': declared_type,
                     'value': exact_value, 'present': True, 'span': [a, b]},
                ],
                'provenance': caller_owned_body_association,
            },
        ],
        'selection': selector_facts_without_alternative_list,
    },
}
```

Regions are ordered body, prefix, suffix (when present), then continuation:0,
continuation:1, etc. This is API region order, not a joined text offset space.
To render a wrapped message, use its prefix/body/suffix layouts in framing order.
Each capture list follows slot order in that region's selected layout.
For a body or wrapper containing declared literal alternatives, `layout` also
contains `literal_choices`. Each pair identifies a part index and the chosen
alternative index; persist it with the layout for exact rendering. An ordinary
literal-only layout has no such addition. Canonical `text` is not a substitute
for the selected native spelling.

| Region | Exact layout lookup under the loaded model |
|---|---|
| Body | `templates[template_id].parts` |
| Prefix/suffix | The layout also contains `wrapper_template_id`; find that pattern in `templates[template_id].context_patterns[region]` and use its `parts`. |
| Continuation | The layout contains `region: continuation` and `layout_index`; use `templates[template_id].continuation.layouts[layout_index]`. The result also carries the zero-based `component_index`. |

Continuation rendering uses layout `leading`, captured `reference`, layout
`label`, captured `value`, layout `trailing`, in that order. The actual selected
layout index is retained during matching, never rediscovered by rendering.

All capture spans are **half-open byte intervals** in UTF-8 with
`surrogateescape`, relative to byte zero of that region's **original text**.
The body origin is the opening/message body, excluding its log header. Wrapper
origins are their own prefix/suffix ranges. Each continuation starts again at
zero. There is no offset into a synthetic joined diagnostic.

- Absence: `present: false`, `value: null`, `span: null`. The slot must be
  optional; its declared prefix/suffix are absent too.
- Present empty: `present: true`, `value: ""`, `span: [p,p]`. This requires the
  existing declared empty-field permission and a native boundary.
- Present nonempty: `present: true`, exact text and `[start,end]`.

Caller provenance objects on the unit and regions pass through unchanged by
identity. The convenience parser adapter populates them from existing parser
ranges, tags and emission ordinals. The matcher never creates absolute
occurrence bindings. Only the selected regions are materialized/validated as
public results, once each. Losing candidates are never bound.

`inspect=True` adds `inspection` with `matches`, `capture_ambiguities` and the
complete legacy-shaped `selected_assignment`. This opt-in research view retains
all eligible complete alternatives; it does not change the ordinary assignment.
The unchanged selector resolves substantive/capture ties deterministically and
keeps their final status provisional. Consumers must preserve `match_status`,
not derive it from `template_status` or a non-null template ID.

## Errors and recovery limits

| Error | Meaning |
|---|---|
| Bootstrap `PackageIntegrityError` | Missing/corrupt payload, hash, canonical identity or mutually pinned data disagreement. |
| Bootstrap `PackageCompatibilityError` | Unsupported package contract, executable version, bootstrap or raw-parser pin. |
| `MatcherCompatibilityError` | Unsupported model/parser/selector or unit parser mismatch. |
| `MatcherDeclarationError` | Invalid, unsupported, missing or conflicting model declarations, including overlapping constructions. |
| `NativeInputError` | Incomplete unit, inconsistent pieces/components, or a declared field boundary unavailable in the native pieces. Preserve evidence and report the failure explicitly. |
| `MatcherIntegrityError` | Inconsistent selected result, captures, component count or literal reconstruction. |

These are exceptions, not `no_match`. Ordinary no-match means that a valid
complete unit has no eligible complete assignment. Parser failures remain parser
failures. Unresolved recovery is yielded separately with its original recovery
object and provenance; it must not be passed off as a complete matching unit.

The parser is unchanged. Its existing emitter/colon/adjacency/prefix-equality
continuation recovery remains the only group-recovery mechanism. Missing,
malformed, interrupted or unseen title-list variants are not newly recognized.
Unmatched complete diagnostics remain evidence for review. Native coverage gaps
for ties and error branches are reported separately from implemented
API behavior; no fabricated witnesses establish those branches.

## Learner ownership and pipeline integration

`matching_primitives.Rules(declarations)` is the sole implementation of the
extracted literal, slot, construction, parameter, wrapper and complete-capture
mechanics. `Matcher(model)` uses it plus the existing standalone continuation
matcher and selector for both unpublished and published models.
`matching_defaults.py` explicitly constructs those same primitives from current
learner rules for inference-time proposed patterns. It is never packaged.

The former matching bodies in `patterns.py`, `research_matching.py`,
`constructions.py`, `parameter_structures.py`, `literal_guidance.py` and
`regions.py` are removed. Inference, evidence generation and review presentation
stay in their current owners. Evaluation and publication validation call the
shared Matcher; clustering, wording checks, support evidence and retirement use
its primitives. `review_assignment_changes.py` no longer invokes the pipeline's
separate matcher. No independent learner fallback is retained.

Pipeline work remains: support the new package/selection format, authenticate
and load it, construct the complete input, call `match` once, bind only the
selected assignment once, retain final status and exact layouts/provenance,
then retire its local matcher after native verification. SQL, application
cutover, production processing and active model selection are outside this
delivery. The current active reader accepts the old release format; pointing
it at this package before reader integration will fail explicitly.
