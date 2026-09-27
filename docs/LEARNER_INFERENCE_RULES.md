# Learner inference rules and authority

Updated 2026-09-22. The current outer-diagnostic contract below supersedes the
independent L1/L2/tail descriptions in earlier dated development records.

## Contextual location labels — 2026-09-24, v29

`owner_rules.json.location_label_equivalences` declares the observed `Near file:` /
`near file:` / `file:` and `near line:` / `line:` location introducers. These are
complete, case-sensitive raw token sequences immediately before an independently
recognized LOCATOR, outside declared opaque fields. They are not default literal
words, a path-folder whitelist, or a rule changing native input.

Within an already proposed same-source complete-message group, corresponding
equivalent labels with different native spellings cause re-inference of each
observed exact formulation. The same check prevents later consolidation from
turning the labels into variable slots. The current model represents the result
as ordinary separate exact templates, not optional literals or match-time aliases.
Other surrounding wording and fields must still satisfy ordinary inference.

OPTIONAL_KEY remains a key or absence. One distinct present spelling does not
invalidate it. The rejected v28 minimum-present-variation experiment is reverted;
it was never published. No generated templates are manually overwritten.

## Current correction — 2026-09-23, v24

PARAM uses distinct candidate-local raw-span observations and separate boundary
validation. Punctuation tokens count; whitespace gaps do not. Whitespace, nesting,
alternating separators and unequal observed lengths are not requirements. Earlier
such restrictions were assistant heuristics, not owner authority. Qualified KEY
syntax retains precedence and its several raw pieces do not supply PARAM evidence
merely because an outlier fails KEY. No automatic KEY-failure/PARAM fallback.

A candidate with fewer than two distinct non-location examples remains provisional;
occurrences and locator-only variation do not increase this support. Such candidates
cannot yield full outcomes or be confirmed. Supported research candidates still
require review. See LEARNER_NATIVE_MODEL_CONTRACT.md and the implementation ledger
for the remaining quoted-expression regression and native checks.

## Current outer-diagnostic rules

- Owner follow-up: presumed-literal guidance is disabled globally through
  `default_literals.enabled=false`. The effective word/phrase list is empty in
  grouping, mandatory anchors, inference and new matching constraints. Retained
  vocabulary is inactive reference data. Case sensitivity, observed literal
  wording, trace declarations and location recognition remain active; they do
  not depend on the disabled vocabulary. This supersedes the earlier proposed
  contextual relaxation of individual guided identifier positions.
- Owner-declared trace structures now supply ordinary PARAM spans under
  `owner_rules.json.parameter_structures`. Complete Script location file/line
  chains are one span; inline file/line parenthetical interiors are separate
  spans with literal surrounding parentheses. The recognizer uses exact raw
  boundaries and balanced delimiter scanning, not alternate tokenization.
  Ordinary parentheses and arbitrary trailing text are not trace evidence.
- Declared PARAMs do not require observed variation, even for singleton messages.
  Their interiors are excluded before grouping/alignment, including recurring
  wording and default literals. Undeclared PARAMs retain empirical requirements.
  The ordinary PARAM matcher is unchanged: no TRACE slot, role, spelling list or
  definition-specific capture constraint. Definition IDs are inference provenance.
- Presence of recognized structures is an outer-message selection condition,
  alongside source and construction. Ordered declaration IDs are recorded in
  each candidate's `parameter_structures` and identity. Frame count and internal
  values do not enter the signature. This keeps Script location: Unknown from
  matching a trace-present formulation while leaving its bytes/literal intact.
- The complete recovered diagnostic is the learning/matching unit. Shared
  wrapper context remains attached; source families remain independent. No
  detached reason or tail pool can supply a candidate's field observations.
- The established script envelope is declared under `constructions` in
  `owner_rules.json`. Its exact bracketed reason is REASON content, not a
  separately learned template. Regex, source, named ranges, comparison regions,
  typed fields, authority and evidence are inspectable data. The generic
  consumer contains no CK3 sentence/source branches.
- The observed unbracketed variant of that same envelope has a declaration
  identifying its failure wording for comparison, with no prescribed fields.
  This follows the owner's permission to supply common structures through
  JSON. An explicit `excludes` reference keeps the bracketed REASON variant
  separate. Header and trace repetition cannot dominate either comparison.
- Matching enforces the same declared-construction identity as learning.
  Ordinary candidates cannot compete across that boundary and absorb an
  established REASON field into a whole-message PARAM.
- Construction identity supplies the envelope evidence. Its declared failure
  wording supplies similarity; the complete outer message still participates
  in alignment, field assessment, matching and provenance. Repeated header
  wording and arbitrary reason values do not boost a grouping score.
- The JSON `inference_policy` admits short candidates when one of two aligned
  wording positions agrees (fraction .49). It is an investigation gate, not
  template acceptance. Longer comparisons retain the existing threshold;
  full native evidence still determines slots and retained wording.
- PARAM needs candidate-local nonblank variation and punctuation boundary
  evidence. Adjacent variable text fields may be re-inferred across an isolated
  recurring word in favor of an outer punctuation boundary. Longer literal
  runs and LOCATOR/VALUE/REASON fields are not absorbed by this operation.
  A punctuation-free PARAM is flagged for review and additionally requires four
  distinct nonblank values and two nonzero token lengths.
  These are engineering heuristics, not learned certainty or extra approved
  CK3 formats. Insufficient fields split into observed literal formulations.
- Field-local empirical evidence remains required for undeclared PARAMs.
  Presumed-literal protection is disabled both inside and outside fields.
  Only the explicitly declared trace structures bypass empirical variation;
  ordinary parenthesized content does not automatically become PARAM.
- Candidate consolidation re-infers all member messages and refreshes each
  slot's `field_support` record IDs and exact ranges. Confirmed review decisions
  remain fixed; competing matches are not suppressed.
- Matching counts all complete capture assignments using memoized suffix states;
  it never accepts the first/shortest/longest success. Exactly one assignment
  is needed for an ordinary match. Multiple assignments retain their exact count
  and two concrete witnesses, without enumerating an exponential output list.
  Capture ambiguity and competing templates are distinct review outcomes.
- Complete matching must reproduce each candidate member's inferred field
  spans. Reconstructing the same bytes with different field assignments is
  insufficient. Failed unions are rejected. Partially failing initial groups
  re-infer both successful and failing native subsets; no member is dropped.
  Wholly failing groups remain explicit. Saved member offsets never become positional rules for
  matching new messages.
- A marker directly beside the same aligned wording in every member remains
  a literal boundary even when its later repetition count varies. The JSON
  records this generic adjacency heuristic; it adds no sentence-specific rule
  or automatic slot type.
- Stable separator rank from either end of aligned wording also supports an
  outer boundary despite additional interior occurrences. The raw punctuation
  and whitespace are always retained. These mechanics do not assign PARAM to
  constant content merely because it is enclosed in punctuation.
- Performance caches store immutable native comparison views and byte offsets
  on in-memory records. They neither normalize messages nor persist a second
  parser interpretation.
- Region regrouping investigates at most 12 nearest later candidates per group
  per iteration, ranked by retained wording. This engineering search bound is
  recorded in `inference_policy`; it does not subsample candidate members.
  Accepted unions restart consideration. The search is not exhaustive, so a
  remaining separate candidate is not proof that no valid union exists.

See [implementation status](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md) and
[schema 3 contract](LEARNER_NATIVE_MODEL_CONTRACT.md). No other CK3 message
families or sentence-specific templates are declared by this change.

## Earlier reference and development record

The following 2026-09-21 text describes the preceding learner, not current
preprocessing. New message-specific rules require owner approval and an evidence
reference here. No sentence masks, reason categories or semantic projection
have been introduced by the boundary correction.

The machine-readable reference is
[owner_rules.json](../tools/template_learning/owner_rules.json). Code consumes
the declarations directly; no Python source is generated or rewritten. The
file replaces the narrower literal-guidance declaration. It is the editable
home for exact spellings and the existing known composition/slot-label cues.
Each entry records authority and evidence. Architectural requirements also
have entries pointing to their owning implementation; these are documentation,
not switches that can disable source partitioning or other invariants.

The active symbol vocabulary contains 18 explicitly owner-supplied spellings:
the original trigger/effect/on_action/scripted type/culture/faith words and
plurals, plus event and trait. The folder-derived expansion and its directory
inventory have been removed. Being a directory name or appearing in a path is
not evidence that a word is a CK3 symbol type. A broader list remains pending
independent type evidence from definitions or documentation.

Symbol-type recognition accepts either case of the first letter only, on a
complete parser token. Native template casing is unchanged. Diagnostic words
retain their explicit spellings. Embedded strings such as mod_effect, root.faith,
and common/scripted_effects do not match contained defaults.

`Internal ID`, `Historical ID`, `event ID`, `Event ID`, and `due to` are phrase
guides. Standalone Internal/Historical/ID/to/for are not guides. Event is a symbol
type, not diagnostic wording. Unobserved underscore/camel ID forms remain under
review, not active rules.

Locations are recognized from explicit location labels, slash syntax after
a colon or a complete in/file introducer, or slash-delimited filename syntax with an extension. Recognition
uses ordered existing parser pieces and no folder or extension allowlist.
Parser v1.2 emits every slash separately; a path spans adjacent segments and
slashes, without gaps. Complete location ranges are inference fields; raw
tokens are never replaced, reordered or joined into a new parser token.
Numeric ratios alone do not establish a path. Recognized fields remain LOCATOR
even if every observed support shares their spelling. Labels, punctuation,
whitespace and subsequent trace content stay outside the field. Symbol words
inside those values cannot turn them into literals. File and separately labelled
line fields remain separate locators; path.txt:6 is filename/path, colon, line: two LOCATOR fields and a literal colon.
Parser v1.5 separates the suffix. Bare .txt/.yml/.md/.py suffixes are explicit
filename cues; other shapes use path/file or filename:line context. In an
explicit file field, spaces can remain inside the filename range. A dot alone
does not make a CK3 identifier a filename.
These lexical heuristics remain subject to native review for other presentations.

Changing a declaration requires updating its authority/evidence and running
the relevant native comparison. Candidate models snapshot `owner_rules`, export
the effective `literal_guidance`, and hash both the reference and its loader.
Slot matching uses each slot's saved guidance, not the current editable word
list. The selected raw parser remains independently versioned; changing this
reference does not mutate an archived parser or candidate.

| Rule | Authority / justification | Current implementation |
|---|---|---|
| Keep exact Div/0 as one lexical token | Explicit owner approval; native jomini_scriptvalue.cpp messages | Parser v1.4 ATOMIC_LEXEMES, whole case-sensitive match only; tooltip/description stays three tokens; not a path or template rule |
| Retain leading ! in adjoining strings, including bare filenames | Owner clarification; Windows permits ! within names; native !!0_TFE_chars.txt and explicit bare-name probes | Raw parser v1.3 keeps !!0_TFE_chars.txt, fi!le.txt and file!.txt intact; sentence-final error! remains separate |
| Retain adjoining @ in symbol tokens | Owner correction backed by base-game and workshop variable definitions; e.g. `@cultural_maa_extra_ai_score = 80` | Raw parser v1.1 returns `[`, `@name`, `]`; learner KEY captures retain @ |
| Partition every pool and match by emission source | Owner instruction; corpus source audit | `records`, `clustering`, `artifacts`, `research_matching` |
| Recognize `Script system error! … Error: L1 [ L2 ] … Script location: …` in `jomini_script_system.cpp` | Owner explicitly permits this known convention; captured Failed context switch and Unknown loc key examples | `layers.layer_regions`; exact native spans, no replacement or normalization |
| Learn all L2 observations in that source together, independently of L1 | Owner correction: no restriction to particular L1 templates | `component_records`; source/role/text pool, no allowed-pair table |
| KEY is a whole non-punctuation parser token; PARAM may contain variable punctuation between its literal boundaries | Owner bracket-capture correction and subsequent variable-length PARAM direction | `derive_pattern`, `match_pattern`; punctuation cannot veto wording similarity. Raw pieces remain intact; no identifier splitting or new lexer |
| Location labels remain literal; locator slots hold only the variable field | Owner boundary review and explicit `Key <KEY> not found at Database: <LOCATOR>` direction | `_slot` retains `file:`, `line:`, `lines:`, `Database:`; location slot has complete parser-range bounds and a numeric constraint when observations are numeric. Database directory values need no extension |
| Preserve exact repeated-message evidence without repeat weighting | Owner empirical workflow; verified collection and merge | Key is source/context-kind/exact text; repeated occurrences retained separately. Component text is deduplicated within source/role |
| Confirmed templates run before residual inference | Owner incremental-learning direction | Registry `confirm` records revision/template IDs/note/time. Confirmed patterns persist unchanged. Zero-match evidence enters inference; ambiguous matches are reported, not silently selected |
| Case differences alone do not establish slots | Owner case/context correction; native `Target culture was null` / `target culture was null` | Case-sensitive retrieval; `refine_literal_variants` partitions a proposed slot whose distinct values differ only by case. Literal text is not normalized |
| Default words are literals outside their original example phrases | Owner 2026-09-21 endorsed default words and CK3 symbol type names, complete tokens only, with first-letter case alternatives for type recognition | `owner_rules.json` declares words/phrases and the per-group casing policy. Native casing and gaps remain exact; guidance applies outside recognized locations. Slots record the guidance applicable to their range |
| No optional literals | Owner correction: the architecture does not support them and must not be expanded | Literal parts remain mandatory exact text. Presence/absence of guided wording yields separate formulations. OPTIONAL_KEY remains a variable slot, not an optional-literal representation |

The earlier example-specific relationship PARAM override was an agent error,
not an owner-authorized rule. It and its claimed authority have been removed.
The varying relationship token in `character (is_child_of (target character))
was null` is inferred normally; KEY is acceptable. `owner_overrides` is empty.

The blanket v4 rule splitting every one-spelling-plus-absence slot is removed
from active inference. It was broader than the requested literal guidance.
Its benefits/regressions remain separate review evidence; it is not a current
requirement or an authorization to introduce optional literals.

The script envelope is the message-specific segmentation convention. Its
benefit is a correct learning unit: `Failed context switch` remains an L2
literal even when its associated L1 changes. The declaration applies to native
messages matching that convention, not arbitrary brackets in other sources.
The closing delimiter is followed by the known location tail; that tail and
all framing remain in the complete record.

## Generic inference heuristics still subject to empirical review

These are existing generic candidate proposals, not owner-approved semantic
truths or sentence categories:

- Candidate retrieval uses case-sensitive adjacent word pairs, or individual words for fewer
  than three words. Alignment similarity has a configurable default of 0.72.
- The similarity score combines matched/longest, matched/shortest and length
  ratio with weights 0.55/0.35/0.10. Reference selection samples up to 40
  candidates against 100 distinct variants; every variant enters alignment.
- Punctuation is not a mandatory grouping signature or a similarity weight.
  Ordered alignment retains supported punctuation as exact literals. No
  delimiter arrangement automatically excludes its contents from comparison or
  forces PARAM. General region proposals must investigate native interior
  literals, variation and type evidence before reconsidering similarity.
  Identical structural candidates are merged with their native evidence;
  differing overlapping candidates remain visible.
- Consensus anchors require every distinct member. An inconsistent boundary
  leaves a candidate unresolved; there is no normalization repair.
  Similarity groups are then refined when their proposed slots have only
  case variation. Each resulting group is
  aligned again against all of its native members. Refinements are exported
  for review; distinct overlapping patterns are still reported.
- Recognized locations contribute one range-backed unit to alignment and no
  weight to wording similarity; path spelling and number of slash-separated segments must not
  drive formulation grouping. This is an inference view over original pieces,
  not a replacement parser or rewritten message.
- Numeric variable text proposes VALUE unless its observed position is a
  location or an ID/key-labelled position. Complete adjacent path sequences propose
  LOCATOR. Otherwise one non-punctuation parser token proposes KEY; multi-token
  text proposes PARAM. Optionality records observed absence. There is no
  example-specific slot typing and no blanket minimum-substitution rule.
- Matching retains every qualifying candidate. Similarity-based choice during
  candidate formation does not establish that only one template can match.
- Provisional groups are reconsidered when a candidate covers every native member
  of another group in the same context and with the same guided wording. Their
  union must infer one supported candidate retaining the covering pattern's fixed
  wording; otherwise the groups stay separate. Accepted unions reduce the group
  count and are revisited until none remain. This is joint inference, not
  match-time suppression or a rewrite of confirmed templates. Partial overlaps
  remain explicit. Generic optional punctuation-only captures split by presence
  to preserve the no-optional-literals requirement. The terminal-pair and whole-
  parenthesized-capture rules were removed; no blanket fixed-word-plus-absence
  rule is installed. Internal PARAM punctuation and token counts may vary.
- Empirical region search proposes unions within source/component and guided
  wording. All raw interiors participate in alignment first. Stable wording,
  marker occurrence/rank and observed nesting can support boundaries at any
  position; differing interiors do not themselves force PARAM. Period, equals
  and backslash do not seed marker-envelope proposals, while remaining raw
  evidence and possible fixed literals. Interior literals divide/narrow a
  proposal; ordinary slot assessment chooses KEY, VALUE, LOCATOR or PARAM.
- Only supported PARAM captures are removed from the comparison token view,
  contributing neither a penalty nor a placeholder bonus. At least two common
  wording tokens must remain to support a union at the unchanged threshold.
  Every accepted union is re-inferred and reduces group count; changed pools
  are reconsidered until no further union qualifies. Rejections and their
  native boundary evidence are retained in the candidate's discovery ledger.
- A proposed PARAM cannot erase independently supported alphabetic literal
  phrases from a pool with observed non-location variation without being
  flagged/divided. This conservative heuristic is based on raw word runs and
  native support, not a sentence dictionary. It can overprotect repeated field
  values; the resulting overlaps remain visible in the report.
- One nonempty spelling plus absence is insufficient evidence for a varying
  multi-token PARAM. The hypothesis is recorded and the observed literal
  formulations remain separate. This does not change OPTIONAL_KEY or the
  general case of one fixed word plus absence.
- Balanced delimiter pairs are saved only when every observed PARAM value
  supports them; the matcher applies that learned constraint to raw pieces.
  No region gets a type, loses guidance or gets excluded solely because a
  particular delimiter surrounds it.
- A mixed group can be split by interior wording retained in independently
  learned groups from the same source and component. Each alternative needs
  at least two distinct native supports; every member of the mixed group must
  select exactly one alternative. The resulting groups are inferred again.
  This is a generic, reviewable heuristic, not an owner-supplied vocabulary or
  authority to discard overlapping candidates at match time.
- Adjacent KEY/OPTIONAL_KEY/PARAM fields separated only by whitespace are
  inferred as one region when at least one field is a PARAM. There is no learned
  wording or delimiter establishing those as independent fields. Numeric and
  locator fields are excluded from this coalescing. Native gaps remain exact.
- Independently proposed candidates with the same fixed wording and field
  positions are re-inferred from their joint native evidence. Only whitespace
  next to text fields is ignored for that grouping comparison; internal literal
  spacing, punctuation/default anchors, source/component and typed numeric or
  locator fields remain distinct. The merge is accepted only if all native
  supports match and the resulting fixed wording is unchanged. No message is
  normalized, and there is no match-time preference for one candidate.
- Capture search visits raw-parser boundaries directly and tries another valid
  partition when needed. An internal apostrophe cannot terminate a capture
  inside a parser token merely because a later template literal is an apostrophe.

These heuristics remain subject to the owner-authorized same-corpus rerun.
Default words such as `Failed` and `Unknown` now have explicit owner authority
as literals. They do not authorize hardcoding `Failed context switch` or
`Unknown loc key` as whole templates or reason categories; their remaining
structure is inferred from native observations.

## Confirmation is separate from inference

A provisional candidate is not confirmed merely because it matches its own
evidence. Confirmation is an explicit review input and is not runtime promotion.
Confirmed patterns, review provenance and current native captures remain in the
next candidate. Uncovered evidence proposes additional templates; it cannot
silently rewrite a confirmed contract. Multiple matching confirmed patterns
remain a review outcome. Additional evidence may expose a confirmed contract
as too broad; this still requires a new review decision.

No production confirmations were made during the correction. The confirmation
API verification uses an isolated, explicitly labelled test registry.
