# Compound-identifier investigation — 2026-09-23

The survey below was read-only. Owner review subsequently settled the typing
decisions: supported variable expression fields remain PARAM (including their
one-token members); malformed colon-qualified references may occupy KEY fields.
The proposed one-colon-per-dotted-step restriction was rejected and is not
implemented. v25 records these decisions without changing v24 inference results.
See the existing [formal handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md) for publication.

## Evidence

All 73 distinct protected logs in the existing corpus were read with raw parser
ck3-lossless-v1.6: 2,517,940 emissions, 2,594,601 recovered message occurrences,
90,518 distinct source/message pairs, zero unresolved emissions. Counts describe
recovered messages, not independent learning examples or unique emissions.

Ignored delivery:
`.codex-tmp/learner-refactor/compound-identifiers-survey/`

- `REVIEW.html`: readable findings, 23 complete native witnesses, actual raw
  pieces, source counts, syntax discussion and expandable exact value inventories.
- `FINDINGS.md`: the same main findings in Markdown.
- `census.json`: all input identities/hashes and parser provenance.
- `native-messages.jsonl`: all distinct native messages, raw pieces and per-log
  occurrence counts.
- `colon-inventory.json`, `run-shapes.json`, `selected-formulations.json`:
  descriptive search inventories, not recognition dictionaries.
- `review-witnesses.json`, `verification.json`: displayed examples verified
  directly against original byte ranges in 13 protected logs; inference hashes
  unchanged. `source/` pins the read-only survey tools.

## Findings

| Observed formulation | Message occurrences | Distinct exact values |
|---|---:|---:|
| title-qualified | 14,703 | 4 |
| scope-qualified, including one explicitly invalid double-colon link | 188,776 | 107 |
| cp-qualified | 521 | 5 |
| var-qualified | 198 | 4 |
| religion-qualified attempted tags | 55 | 2 |
| character-qualified script link | 4 | 1 |
| root.war.var-qualified | 2 | 1 |
| liege.court_position-qualified | 2 | 1 |
| Gene attribute composite labels | 238 | 238 |
| Colon-bearing trace frames | 773,097 | 2,327 |
| Decorated trace frames | 246,359 | 630 |
| Quoted data-call expressions in the two investigated data/GUI diagnostic sources | 394 | 39 |
| Pipe-delimited mesh names | 280 | 4 |

Rows can overlap. Counts are messages containing a formulation, once per row;
the expanded value inventories separately count span instances. Exact values
retain whitespace and spelling differences. Full per-source counts accompany
each family in the readable delivery.

The ordinary reference examples suggest this structural grammar:

```text
reference := step ("." step)*
step      := name [":" name]
```

This describes punctuation structure, not the full allowed character set for a
CK3 name. Dots remain inside existing raw tokens; a span validator need not
replace tokenization. Established symbol spellings, including attached `@`,
remain intact. Prefix/property/value spellings are evidence, not an allowlist.

Important native distinctions:

- `scope:attacker.var:val_beneficiary` occurs 47 times. It contains two qualified
  steps separated by a dot; its actual raw pieces are `scope`, `:`,
  `attacker.var`, `:`, `val_beneficiary`.
- `scope:title:e_western_roman_empire` occurs once, and the emitter explicitly
  reports more than one colon in the event target link. The present generic
  colon-join implementation accepts its shape; it is not demonstrated valid
  link syntax.
- `most recent:file: ...` occurs 718 times. The adjacent `recent:file` is prose
  followed by a location label, despite having an atom-colon-atom shape.
- `filename.gui:925` remains filename/line structure, not a qualified symbol.
- Gene `name:variant:demographic` triples have two colons but a different
  construction: 28 observed first components, 60 second components, four third
  components. The semantic names of those components are inferred, not an engine
  schema claim. No list of their observed values is proposed as a rule.
- Trace names can contain `[args#digits]`, `[hash#digits]`, both decorations,
  and colon-labelled steps. All 630 decorated values and 305,393 span instances
  are accounted for in file/line trace frames. Keep those internals within the
  existing trace PARAM treatment.
- Data calls have arguments, internal whitespace, nesting and member chaining.
  They require a richer expression grammar, not a colon/parenthesis joining
  rule. One native statement explicitly rejects the trailing `( GetPlayer )`
  after `GetTravelOption('tutor_child_option').GetName`; balanced parentheses
  alone are not sufficient evidence of a valid compound value.

## Effect on the earlier expression question

In the **same** `pdx_data_factory.cpp` formulation, `Failed converting statement
for ...`, all 73 logs contain 76 distinct values / 914 occurrences. Of these,
35 distinct values / 150 occurrences contain calls. `GetTitleByKey(...)` is
therefore not an isolated call-shaped observation in this error context.

Owner decision: a supported variable expression field remains PARAM. Its short
members do not acquire a different slot type. The outdated KEY expectation is
replaced by verification of actual same-candidate native values, raw boundaries,
token counts and captures. The separate native reference context remains KEY.

## Owner disposition after investigation

Do not impose a one-colon-per-dotted-step restriction or require a reference to
resolve successfully in CK3. An error may report malformed input in a KEY field.
The syntax description above is an observation, not a learner acceptance gate.
Syntax alone cannot distinguish `recent:file` from a reference: field context
and surrounding native wording govern inference. Existing LOCATOR and declared
PARAM/REASON ownership take precedence. Trace interiors remain opaque.

Keep the raw expression pieces intact. No call-expression parser, function-name
whitelist, or punctuation-wide KEY extension is needed. Positive variable-span
evidence and validated boundaries govern PARAM; brackets alone do not prove it.

The report distinguishes attempted references from proven valid syntax:
`religion:...` values are reported as invalid religion tags, rare court-position
and character forms have only one distinct value, and function lookup/arity
failures do not establish that each submitted expression is semantically valid.

No extra recognition branch was required by these decisions. The JSON registry
now makes the accepted policy explicit; publication uses the fresh ten-log build.
