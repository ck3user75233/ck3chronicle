# Default literals and owner-rule reference

2026-09-21. Implements the owner's direction to use default words independently
of their original example phrases, include CK3 symbol type names, reject
embedded substring matches, and keep owner-directed declarations transparent.

## Implemented declarations

[owner_rules.json](../tools/template_learning/owner_rules.json) is the editable
reference. It contains 66 explicit words plus `due to`, grouped by rationale,
with authority and native evidence references. Examples include:

- `target`, `Target`, `Reason`, `reason`, `Event`, `event`, `link`, `Link`;
- `Failed`, `Could`, `Invalid`, `Undefined`, their listed lowercase forms, and
  the explicit words from the preceding failure/boundary wording survey;
- `trigger`, `effect`, `on_action`, `on_actions`, singular/plural scripted
  trigger/effect/modifier names, `culture`, `cultures`, `faith`, `faiths`.

This is an explicit initial vocabulary, not a claim to enumerate every CK3
symbol type. It does not import arbitrary symbols from base-game or mod files.
There is no stemming, implicit plural expansion, global case folding or
automatic titlecasing. Listed case variants remain distinct literal strings.
`Wrong`, `scope`, `for`, `trigger` and `effect` are individually default literals,
so the two Wrong-scope introductions stay distinct without hand-written templates.

The code consumes the reference directly. Editing Python generated from JSON
would introduce a second copy of the rules; no source-generation step is used.
The former `literal_guidance.json` declaration has been replaced rather than
kept as another authority. The existing L1/L2 source, regex and ordered regions
and the existing location/identifier position cues also come from this file.
Their behavior is unchanged. The file identifies the slot-position regexes
as implementation heuristics under owner requirements, not owner-authored syntax.

Architectural requirements are recorded with implementation locations. Those
entries document invariants, not mutable switches that can disable them. The
raw parser stays independently versioned and self-contained. Its implementation
was not altered or made dependent on the editable learner reference.

New models snapshot the entire reference in `owner_rules`, include its file
and loader hashes, and export the effective `literal_guidance`. Each slot saves
the default-literal list used to constrain its captures. Matching a saved slot
uses that list rather than whichever defaults are currently editable. No
example-specific slot-type override or optional literal representation was added.

## Boundary verification

Default wording must cover complete existing raw-parser pieces. The source
text is neither normalized nor split again. The owner's exact examples
`mod_effect` and `mod_scripted_trigger`, plus case/plural/prefix examples, were
passed through the selected raw lexing implementation as explicit interface
checks; they are not presented as native training evidence.

The native evidence inventory contains **1,700 distinct continuous strings**
that contain one of the default words but are not themselves declared defaults.
None is recognized through an internal substring. Native examples include:

```text
back_effect
front_effect
common/scripted_triggers/mxh_triggers.txt
death_reason
house_relation_reason_cuckoldry_desc
event/on_action
RICE_setup_on_actions
root.culture
host.faith
```

Fifteen original emissions containing selected examples were freshly reparsed;
their pieces match the saved native evidence exactly. All 15,646 inspected
source/region/context/text units retain the same L1/L2 segmentation after moving
the convention into the reference file. Colons and all other parser punctuation
retain their existing literal boundaries.

See [boundary evidence](../.codex-tmp/learner-refactor/default-literals-review/boundary-check.json).

## Why Event and link became slots

The actual supporting messages include:

```text
Script system error! (while building tooltip/description)
  Error: Event target link 'scope' returned an unset scope
  Script location: file: events/zz_lmfmod_spouse_events.txt line: 9945 (lmf_spouse.1240:option)

Script system error! (while building tooltip/description)
  Error: Undefined event target 'story'
  Script location: file: events/zz_lmfmod_spouse_events.txt line: 9945 (lmf_spouse.1240:option)
```

The learner compares complete ordinary messages here, not standalone extracted
`target` subphrases. These messages have 33 and 29 raw non-gap tokens, including
punctuation. Their shared wrapper, quote positions and identical location yield
similarity 0.835 against a grouping threshold of 0.72. This pair illustrates
why the group accepts different failure wording; it does not claim that this
exact pair was the group's first comparison.

The old group's error portion is:

```text
Error: <KEY> <OPTIONAL_KEY> target <OPTIONAL_KEY> '<KEY>' <PARAM>
```

`target` was protected, but `Event` versus `Undefined`, the presence of `event`,
and the presence of `link` became variables. Short diagnostic text makes the
shared framing relatively influential. The defect is still overgeneralization
during grouping and alignment, not a requirement that short templates contain
slots. Default words now preserve those distinctions before grouping.

## Native comparison

The comparison rebuilds from the same 48 native logs as candidate
`87b4eed8261625c4ba9ff05c` and evaluates all 25 additional logs against the frozen
new candidate. It includes every occurrence, preserves source partitions, and
uses the unchanged parser version and digest. This isolates the effect of the
new declarations; it is not a holdout accuracy claim or an incremental addition
of the other 25 logs. Results and transitions are recorded in
[the comparison output](../.codex-tmp/learner-refactor/default-literals-review/summary.json).

No registry selections, confirmations, SQL records or production model are
changed by this research comparison.

### Fixed 48-log build and frozen additional logs

Candidate `1fbe61bfc955c6773d6c6192`, compared with
`87b4eed8261625c4ba9ff05c`:

| Outcome | 48 logs before | 48 logs after | Additional 25 before | Additional 25 after |
|---|---:|---:|---:|---:|
| Full ordinary | 1,288,470 | 1,300,504 | 210,938 | 212,102 |
| L1+L2 | 554,659 | 638,568 | 332,757 | 237,834 |
| L1-only | 0 | 0 | 1,942 | 100,678 |
| Partial | 0 | 0 | 239 | 239 |
| Ambiguous | 96,898 | 955 | 5,314 | 208 |
| Unknown | 0 | 0 | 103,384 | 103,513 |

Training ambiguities decrease from 2,075 to 409 distinct message/context cases.
No complete training match regresses to ambiguity or nonrecognition. There are
612 ordinary and 974 component candidates, versus 530 and 954 previously.
There are no unsupported candidates or unresolved parser emissions.

On the 25 additional logs, distinct ambiguous cases decrease from 928 to 69,
and no complete match becomes ambiguous. However, **98,736 previously complete
occurrences lose L2**, 25 previously full occurrences become unknown, and 104
previously ambiguous occurrences become unknown. Lower ambiguity is therefore
not sufficient to call the frozen comparison a success.

All 98,736 L2 losses are instances of:

```text
Scoped object of type 'culture' is not valid ( [native formatting] (Culture - [number])[native formatting])
```

The original strings, control characters, raw pieces and captures are retained
in [native regression examples](../.codex-tmp/learner-refactor/default-literals-review/native-regression-examples.json).
The 48-log evidence did not contain this culture-specific L2 formulation. The
old candidate generalized the type name through KEY; the new candidate correctly
refuses to capture the declared literal `culture` but has not yet learned its
separate formulation. This is a concrete coverage cost of default type literals.

Other losses include eight `Failed to scope to religion` occurrences, twelve
`Unexpected token: scripted_effect` occurrences and five Event-target messages
with `state_faith`. The 104 formerly ambiguous cases are ordinary Wrong-scope
messages. `state_faith` remains a single variable token: its loss is not an
embedded-word match. Separating previously broad groups can leave location/trace
variants under-supported too. No new rule was installed to force these to match.

### Inspected improvements and remaining overlaps

All 26 native Wrong-scope L2 variants now have exactly one match. `trigger` and
`effect` are literal; declared `culture` and `faith` scope values also become
literal, while other observed values remain inferred slots. This yields nine
supported patterns across these examples, rather than one forced generalized
template. `Event` and `link`, `Undefined event target`, and `Near file` remain
literal. The relationship formulation remains
`character (<KEY> (target character)) was null`.

Some newly separated groups contain only one distinct example and therefore
retain its entire text literally. That is not evidence of successful inference
of its future variable values. Inspectable before/after native examples are in
[selected comparisons](../.codex-tmp/learner-refactor/default-literals-review/selected-native-comparisons.json).

Of the 955 remaining training ambiguities, 697 are in script location tails,
206 are in L2, and 52 are ordinary messages. The largest single overlap affects
414 occurrences: a five-frame trace pattern with variable file paths competes
with another pattern fixing one file path. Other overlaps concern rendered
names and formatted error text. Defaults do not resolve competing broad/narrow
patterns whose differences contain no default word.

Fresh parsing of the two original comparison logs reduces ambiguities from
79 to 2 and from 9 to 0, with zero unknown, partial or L1-only results. Input
hashes are unchanged. These two logs do not replace the 25-log regression evidence.

### Adding the remaining evidence

The next isolated build adds the 25 logs to the existing 48-log evidence through
the owning cumulative learner. It preserves confirmed-first behavior (the
registry currently has no confirmations), source partitions and exact distinct
message aggregation. It does not install templates or change the literal rules.
The runner is [inspect_accumulated_corpus.py](../tools/template_learning/inspect_accumulated_corpus.py).
It validates parser/cache hashes, reconciles prior outcomes across the combined
corpus, and leaves registry selections and confirmations unchanged.

The comparison above remains the evidence for behavior before learning from
the added logs. A successful cumulative match is in-corpus coverage, not proof
that the frozen recognition losses could not recur on a new formulation.

The cumulative build completed as `9310e1af7379beb8f6cbcda4`: **73 logs,
2,594,601 occurrences, 90,518 distinct messages and 133 sources**. It produces
901 ordinary and 1,042 component candidates, with one unsupported candidate.

| Outcome on all 73 logs | Before adding the 25 to learning | After cumulative learning |
|---|---:|---:|
| Full ordinary | 1,512,606 | 1,514,455 |
| L1+L2 | 876,402 | 978,148 |
| L1-only | 100,678 | 0 |
| Partial | 239 | 0 |
| Ambiguous | 1,163 | 101,827 |
| Unknown | 103,513 | 171 |

All 98,736 culture-related losses and all 129 new unknowns from the frozen
comparison now have complete matches. This happened through native evidence,
without additional declarations. However, 92,639 previously complete
occurrences become ambiguous during the cumulative rebuild. There are now
21,606 distinct ambiguous message/context cases and 31 unknown cases.

The dominant new issues are:

1. **Missing-localization overlap:** `pdx_locstring.cpp` accounts for 97,063
   ambiguous occurrences. For example, the native message
   `Key is missing localization: 0` matches four candidates with differing
   PARAM placement and optional variable slots. They share the same introduction
   and accept the same content. One overlap combination accounts for 92,160
   occurrences. The display string omits PARAM optionality; actual `parts`
   explicitly records it. This is not optional literal support.
2. **Gene-description overlap:** `portraitcontext.cpp` accounts for 4,030.
   `Unknown gene_height gene template dwarf_height at file: ...` matches broad
   `Unknown <KEY> gene <KEY> <PARAM> ...`, more specific gene-template patterns,
   and a pattern fixing `gene_height`. These are competing candidates within
   one source, not source-crossing comparisons.
3. **A concrete matcher boundary defect:** one localization candidate with 31
   supporting messages / 171 occurrences is unresolved because two supports
   fail validation. For native `Mts'khet'`, the parser correctly returns the
   continuous token `Mts'khet` followed by a separate apostrophe. The regex
   chooses the internal apostrophe instead, yielding `Mts` and `khet'` captures.
   `match_pattern` rejects those invalid raw-piece boundaries but does not
   search for the valid alternative using the final apostrophe. `Qal'at
   al-Nisā'` has the same defect. The entire unsupported candidate is excluded
   from matching, leaving all 31 cases unknown. The parser and default-literal
   substring checks are not responsible for this failure.

The [subsequent grouping correction](LEARNER_GROUPING_REVIEW.md) addresses
native-boundary capture selection, separates the mixed gene formulations,
and reconciles candidates retaining the same fixed wording. Its final
73-log comparison reduces ambiguities to 5,656 and unknowns to zero, without
recognition regressions. Remaining alternatives stay visible; no name-specific
rules or preferred-template selection were added. Neither candidate is promoted.

Detailed cumulative evidence:

- [Counts and transitions](../.codex-tmp/learner-refactor/default-literals-73-log-review/summary.json)
- [Remaining competing patterns and native examples](../.codex-tmp/learner-refactor/default-literals-73-log-review/remaining-issues.json)
- [Native apostrophe pieces and rejected captures](../.codex-tmp/learner-refactor/default-literals-73-log-review/unsupported-native-boundaries.json)
- [Recovered regression examples](../.codex-tmp/learner-refactor/default-literals-73-log-review/regression-recovery-examples.json)

Both builds and all replay processes completed. Registry bytes, current revision
and confirmations are unchanged. The new reference is packaged as data and
its saved contents/hashes are verified against the models. The initial cumulative
runner attempt rejected the bundle's different parser artifact location as a
registry cache identity mismatch; the runner now requires the explicit selected
manifest and verifies that its version and bytes equal the bundled parser.
No cache fallback or parser substitution was introduced.
