# Cross-header continuation recovery: parser v1.7

Updated: 2026-09-26. **Implemented, validated and published as a new selectable
immutable parser artifact.** This ledger supplements the existing
[formal pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md).

## Owner correction

The owner reviewed the initial proposal and directed: “please simplify the parser
and republish … that belongs in the learner where it was designed for.” This
supersedes the attachment's proposed character-recognizer dependency and the
initial proposal's full-ID packaging and fixed failure-sentence rule.

The parser now uses emitter/colon framing and opaque byte-prefix equality. It
does not import or embed character recognition, name rules, ID syntax, a model,
owner_rules.json or learner inference. Character and slot interpretation remain
learner responsibilities. The initial proposed schema 4 was not implemented.

## Status ledger

| Work | Status | Evidence / remaining work |
| --- | --- | --- |
| Native inspection | Complete | 73 complete logs; 11 blocks and 13 supporting entries. |
| Interface review | Complete | Simplified at owner's direction. |
| Shared recovery and consumer interfaces | Complete | One log-level stream; both consumers retain each group once. |
| Complete native replay | Passed | Exact reconstruction and unchanged unaffected recoveries across all 73 logs. |
| Existing parser checks | Passed | Nine checks with the complete annotated native input, including registry and independent replay. |
| Packaging and independent loading | Passed | Wheel bytes match; independent pipeline imports no character recognizer/learner. |
| Immutable parser publication | Complete | New v1.7 artifact; old parser/model artifacts unchanged. |
| Repeated-component inference/model classification | Separate learner work | Complete grouped evidence retained for review; no opener-only classification or title-line training. |

## Publication

Version: **ck3-lossless-v1.7**.
Manifest: `tools/template_learning/parsers/v1_7/manifest.json`.
Parser SHA-256:
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.

The standalone `parser.py` embeds the versioned recovery JSON, so the existing
three-field parser reference covers every runtime rule and implementation byte.
`recovery_rules.json` is an inspectable identical copy, verified at publication,
not a mutable runtime dependency. The wheel includes both and the manifest.
Publication means a selectable immutable repository/package artifact; it does
not mean pushing the unrelated dirty working tree to GitHub.

## Delivered rule

`history-colon-title-list-v1` records authority and native provenance in JSON:

1. A single physical-line message from `history.cpp`, level `E`, ending in `:`
   opens a continuation-bearing error. No failure sentence is hard-coded.
2. An adjacent entry has `<opaque prefix>'s title: <nonempty remainder>` framing.
   Its prefix must occur at the start of the opener followed by a space. Further
   entries repeat those exact prefix bytes. The parser does not interpret them.
3. Consume consecutive compatible entries only. A new colon opener, different
   prefix, different emitter/level, unrelated message or uncertain framing stops
   the group. No search ahead, timestamp equality or fixed C++ line numbers.
4. An opener without an established entry remains unresolved with a reason.
   Orphan entries also remain unresolved. Uncertain following content stays
   unconsumed; an already established list retains its recovery limitation.

The marker is native continuation framing. The displayed title is a complete
contiguous remainder, with its interior spaces and original order retained.
All original bytes, presentation spacing, repeated prefixes, headers and line
endings remain evidence. No missing content is manufactured.

## Shared API

Use `RawParse.iter_recoveries()` for v1.7. The loader's `iter_recoveries(raw)`
explicitly dispatches v1.6 to its original API and v1.7 to the complete-log stream.
Unsupported API versions fail; no parser substitution occurs. `Emission.recovery`
remains a local inspection primitive and cannot associate subsequent emissions.

`Recovery.parents` contains the ordered original emissions. For a grouped error,
`messages` contains one opening with an ordered `continuations` tuple. Each entry
holds its original `MessageSelection`, `prefix_span`, `label_span` and `value_span`.
These are structural ranges, not model slot assignments. `message.source_spans`
contains the component body ranges; `Recovery.ordered_spans` partitions all member
emission bytes once, including their headers. Consumed entries are never yielded
again as independent errors.

The opening's existing `span`, `text`, `pieces` and `native_bytes()` still describe
its own exact body. No compact display is assigned a false contiguous source span.
Debug format `ck3-raw-parse-v2` retains and validates both original emissions and
the authoritative log-level stream. The original source remains stored once.

Eudes formerly produced two messages; now one error with one continuation.
Its complete block is `[4566781,4567121)`, opening body `[4566812,4566971)`,
entry body `[4567002,4567121)`, and title `Duchy of the Knights Templar`
`[4567091,4567119)`.

Yasutsune formerly produced three messages; now one error referencing emissions
`[47037,47038,47039]`, covering `[4567121,4567630)`. Its opening body is
`[4567152,4567324)`. The ordered title ranges are `[4567457,4567473)` for
`Duchy of Nushiro` and `[4567608,4567628)` for `The Takashina Family`.

## Consumers and model pin

Both `records.collect_records` and pipeline `raw_input.iter_diagnostics` consume
the shared stream, with no independent grouping heuristic.

Pipeline `NativeDiagnostic.continuations` retains each contiguous original body,
framing/value ranges and emission/source provenance. Captures bind relative to
their own body and are verified against original file bytes. The diagnostic
also carries all member ordinals and the complete grouped extent. No SQL emission
record is required. Classifier v6 returns one `unknown` result with the complete
group and an explicit model-support limitation, rather than classifying only its
opening using an ordinary template.

Learner feature version is `ck3-native-message-features-v3`. Current inference
cannot represent the repeated supporting component. The collector preserves each
complete group, its exact native block, component texts/ranges and member ordinals
in the existing unresolved-evidence channel with `recovery_status="recovered"`
and an explicit consumer limitation. `deferred_recovered_messages` counts these
groups; `recovered_messages` remains the number of inference-eligible messages.
Registry validation accounts for every grouped emission. Neither the opener nor
supporting entries become independent training records. This is visible model
deferral, not dropped evidence or a parser recovery failure.

The learner handoff is one opening plus an ordered repeated supporting component:
CHARACTER_FULL_ID for the opening reference and one PARAM for each displayed title.
The list must not become an independent error template per supporting line or per
list length. This task changes the necessary interfaces, not learner inference.

**Pin action:** parser consumers may select the new v1.7 manifest. Full model
classification requires a newly built immutable model with that parser pin and
the learner's repeated-component contract plus matching reader/runtime support.
Regenerate parser/feature-dependent caches; do not edit an existing model's pin.
Selected model `0a61f6c93657948e0ca20b35` remains on v1.6 and rejects mismatched raw
input. No model training/promotion, production processing, SQL or watcher changes.

## Native validation and limitations

All 73 supplied complete logs passed; 2,517,940 original emissions survive.
Messages change from **2,594,601 to 2,594,588**: exactly the 13 supporting lines
now belong to 11 complete errors. There are nine one-entry lists and two two-entry
lists, no new unresolved parser results, and **2,517,916 unaffected local
recoveries** compare exactly with v1.6. All inputs reconstruct byte-for-byte.
Distinct native body lexical sequences also compare exactly.

The first affected log has nine consecutive blocks at lines 48279–48298, bounded
by a `has no faith` message and the Barcelona capital-setting failure. The second
has repeated Henan blocks at lines 3478 and 9841, each surrounded by `has no faith`.
Both occurrences survive. Original native hashes, neighbors, all body/value ranges
and individual results are in the evidence below.

Both affected logs were replayed completely through both consumer adapters.
They retain 11 groups and emit no supporting entry independently. All 13 title
capture bindings reproduce the original bytes. Learner feature validation and a
complete affected-log debug reload passed. Independent pipeline loading verified
there is no character-recognizer or learner import. Existing model-pin rejection
passed. An explicitly in-memory ordinary-model probe confirmed grouped diagnostics
remain unknown; this is not a newly published model or a claim of learned matches.

- [Native census and original ranges](../.codex-tmp/character-title-continuation-review/evidence.json)
- [Former pipeline output: 24 separate messages](../.codex-tmp/character-title-continuation-review/pipeline-before.json)
- [Complete replay results](../.codex-tmp/character-title-continuation-review/v1_7/verification.json)
- [Package and independent-consumer verification](../.codex-tmp/character-title-continuation-review/v1_7/package-verification.json)

The reusable check is `tools/template_learning/inspect_cross_emission_recovery.py`.
It takes the complete input root, prior native census, both manifests and an ignored
output directory. Native inputs and generated evidence remain outside Git.

No missing, malformed or mismatched title-list case occurs in these logs; no native
negative-case coverage is claimed for those branches. No synthetic log messages
were used. Grouped inference remains explicitly deferred, so parser publication
does not establish full model classification support or diagnostic quality.
