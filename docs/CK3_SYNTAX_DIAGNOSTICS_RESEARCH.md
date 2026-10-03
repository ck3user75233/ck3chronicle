# CK3 syntax diagnostics — research handoff for Reporting and Analysis

Research date: 2026-09-30; brace follow-up: 2026-10-01. **Verified findings and proposed report selectors;
no runtime or reporting policy is activated by this document.**

Prepared for the Reporting and Analysis team's 08A/08B work. The owner agreed
with the two persistent-reader punctuation entries and requested a handoff limited
to verifiable findings. Every proposed syntax selector below has both genuine
native evidence and a verified existing template definition. Unverified diagnostic
formulations are excluded. Implementation remains with the reporting assignment.

## Recommended initial list

Highlight these narrowly identified diagnostics as **syntax diagnostics**, with
their affected construct and uncertainty shown:

1. Persistent-reader punctuation rejection: `Unexpected token: =` and
   `Malformed token: {`. These establish a rejected syntactic token, not the
   particular source defect or a proven brace imbalance.
2. A trigger requiring simple assignment but receiving another operator: the
   exact reason `Trigger is simple assign, but used a symbol other than '=' in the middle`.
3. Localization-reader `Unexpected localization token` and `Missing quoted string value`.
4. Localization substitution `Unterminated '$'` and missing required quote escaping.
   Keep these visibly identified as localization syntax, with local impact.
5. Data-statement `Unexpected characters found at end of Statement`.

Keep ordinary `Unexpected token: <identifier>`, generic `Malformed token`,
failed key references, and GUI `Failed parsing ...` outside the syntax preset.
Their observed wording is retained below as **context-dependent research cases**,
not additional syntax selectors. Exclude unknown definitions, missing
resources, scope/type failures and generic `Script system error!` from automatic
syntax highlighting.

There is **no observed diagnostic explicitly saying unbalanced braces or premature
end-of-file** in this inspected corpus. Neither has a verified template selector
here, so neither is included in this handoff's recommended list. The verified
`Malformed token: {` entry retains its actual wording and limited meaning.

### Exact token wording and model check

Rechecked all 689 selected template displays and their relevant literal wrappers.
The persistent-reader templates say `Unexpected token: <KEY>` or the narrower
`Unexpected token: =`; **they do not put single quotes around the token**.
Their prefix is ` Error: "` and their suffix begins `" in file: "`, enclosing
the whole description in double quotes. E1 below is the genuine full example.
The localization-reader family does put single quotes around its token, as in
`Unexpected localization token 's'`; it is a separate family.

For this handoff, the unexpected-token selector is specifically the verified
literal `=` definition. Quote marks are presentation, not the test. An ordinary
identifier remains context-dependent, including an identifier containing
punctuation such as a dotted event ID. This evidence does not establish a general
rule for every punctuation character; no wildcard punctuation selector is proposed.

The selected model has four `Unexpected token` definitions: ordinary KEY
`dcc726d7285cda9a0a94e1f7`, expanded KEY variants
`2ec1bc21b344e9fe4e66b408` and `580538c57a6bff2c90abde24`, and literal equals
`ca6575c8898718edafb168ca`. No selected template display explicitly mentions
braces/brackets being unbalanced, unmatched or unclosed, or an end-of-file error.
A supplementary text inspection of all **12 retained
`empirical_template_model.json` files** under `models/` also found no
`unbalanced`, `unmatched brace`, `unclosed brace`, `brace mismatch` or
`mismatched brace` wording. Historical artifacts were inspected as text only;
none was activated or executed. This is not proof that CK3 cannot emit such a
diagnostic: the empirical models are not an exhaustive engine message catalogue.

In the eight stored Runs inspected on the research date, the narrow list finds **16 records /
16 occurrences**: eight unexpected localization tokens and eight assignment
operator errors. Other recommended families occur in retained historical logs
and have selected-package definitions, but have no records in this current database
snapshot. No historical captures were ingested to fill that gap.

## Concrete selector handoff

For 08A/08B review, the complete proposed initial selector set is the **OR of the
nine rows below**, applied within package `68f1ae5db205ab46afef9c4d` and model
revision `f5cde2616f35d563118d3d32`. Each row requires the exact
`definition.template_id` and `definition.source_family` shown. The final column
adds a condition where needed. These are predicates over stored records, not
instructions to parse or classify native messages again.

| Verified diagnostic | Template ID | Source family | Additional stored-value condition |
|---|---|---|---|
| Unexpected equals token | `ca6575c8898718edafb168ca` | `pdx_persistent_reader.cpp` | None; `=` is literal in this definition. |
| Malformed opening-brace token | `575c64f8a3b6e211b735c3ba` | `pdx_persistent_reader.cpp` | None; `{` is literal in this definition. |
| Wrong simple-assignment operator | `0b2804538785c71278ea37e7` | `jomini_script_system.cpp` | In the `body` region, binding `s1` has type `REASON`, `present = true`, and value exactly `Trigger is simple assign, but used a symbol other than '=' in the middle`. |
| Unexpected localization `s` | `d3e23fc8aad5883970f02964` | `localization_reader.cpp` | None; token and line/column wording are literal. |
| Unexpected localization comma | `3ee5943a9d6e695efc7f6f1c` | `localization_reader.cpp` | None; comma is literal. |
| Missing quoted localization value | `437a7f59c0736bb3b46b6e2f` | `localization_reader.cpp` | None; retain this definition's specific key and location wording. |
| Unterminated localization substitution | `7657bd29deb139cb27588ed9` | `pdx_data_localize.cpp` | None. |
| Required localization quote escaping missing | `14f626fdc756e7881168c8b0` | `pdx_data_localize.cpp` | None; preserve its specific substitution wording. |
| Trailing data-statement characters | `0d942a44097fd983668bacfd` | `pdx_data_statementparser.cpp` | None; retain the specific statement literal. |

Include both `template` and `provisional` match statuses and display the stored
status. Do not infer syntax from `error_type = unknown`, frequency, emitter alone,
quote marks, generic keywords, or the broad trigger-error template alone. The
context-dependent rows in the evidence table are excluded from this selector set.
Other packages need verified selectors of their own; these IDs provide no claim
of coverage for them. An empty result for this supported package is a valid result.

Receiving verification can use the retained genuine examples E1–E9, the stored
research snapshot's 16-record result, and the exclusions as negative cases. The
same trigger-error ID must reject `Failed context switch` while accepting the
exact assignment reason; provisional localization matches must remain eligible.
The historical examples establish family coverage even where the current SQL
snapshot has no corresponding row. Preserve the existing handler, renderer and
storage boundaries; do not ingest production captures to populate a report test.

## Evidence and representation

The current selection is package `68f1ae5db205ab46afef9c4d`, model revision
`f5cde2616f35d563118d3d32`, manifest SHA-256
`2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
It contains 689 templates and parser `ck3-lossless-v1.7`. Selection and package
integrity were checked using the existing `load_selected_package` reader.
The manifest's historical delivery label is not the activation authority;
`models/selection.json` and each Run's stored lineage identify the selection.

Runtime reads used the existing `HandlerClient` against the exact configured
schema-3 database, `ck3chronicle-schema3-20260928T211854Z.sqlite3`. The client
startup hook was restricted, in this research process only, to an existing-host
`hello` probe, so it could not launch a service. The connected host reported PID
308, instance `71d783fe8dc34ea6b4b0f7140de130b2`. Only `list_runs`,
`read_diagnostics` and `read_review_metadata` were submitted. No direct SQLite
connection, arbitrary SQL, ingest, retention or shutdown operation was used.
Ordinary handler request logging may record those reads.

Stored text was reconstructed with `pipeline.contracts.render(definition, values)`.
Five historical files were also read through the authenticated package parser;
selected genuine representatives were checked with its existing matcher in
memory to confirm identifiers and match status. This was research inspection,
not generation replay, model training, ingestion or a new matching implementation.

The storage contract matters to the proposed selectors:

- `definition.template_id` and `definition.source_family` identify the definition;
  Run `lineage.package_id` and `lineage.model_revision` scope its interpretation.
- `values.regions[].bindings[]` preserves exact typed values, including `REASON`,
  with `slot_id`, presence and selected layout. The broad script-error template
  needs a reason predicate, not just a template-ID predicate.
- `match_status` is assignment confidence (`template` or `provisional`), not
  syntax confidence. Stored `error_type` is universally `unknown`; it is not a
  usable syntax selector and must remain unchanged.
- `occurrence_count` measures repetition, not severity. Representative provenance
  includes source tag, emission ordinals and original byte spans. It is not a
  timestamped history of every occurrence.

Owning references: [current handler boundary](TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md),
[Error Contract](ERROR_CONTRACT_SPECIFICATION.md),
[stored reader](../src/ck3chronicle/pipeline/repository.py),
[renderer](../src/ck3chronicle/pipeline/contracts.py), and
[schema](../src/ck3chronicle/pipeline/schema.py).

## Observed families and supporting evidence

“Confirmed” means the message explicitly reports a syntax/form requirement or
rejected syntactic punctuation. It does not mean the source defect was reproduced,
the entire file was discarded, or the session failed. Counts below describe
native wording occurrences across 81 distinct log hashes, not independent defects.
Examples E1–E13 and the source register below retain the distinction between
physical log lines and source-code lines printed by CK3.

| Family and actual diagnostic wording | Existing template identifier(s) | Assessment and seriousness | Recognition from stored fields; evidence |
|---|---|---|---|
| **Rejected assignment punctuation** — `Unexpected token: =, near line: ...` | `ca6575c8898718edafb168ca` | **Confirmed syntax diagnostic.** The reader rejects `=` at that position. Fourteen occurrences in one retained log; the surrounding event-file cluster suggests extensive misinterpretation, but does not establish the first defect or how much content was skipped. | Exact definition ID plus `pdx_persistent_reader.cpp`, package-scoped. Keep both inner and outer LOCATOR fields. E1 / H1. No current SQL records. |
| **Rejected opening brace** — `Malformed token: {, near line: ...` | `575c64f8a3b6e211b735c3ba` | **Confirmed syntax diagnostic at the token level.** Four occurrences in four logs. This is not a native assertion of unbalanced braces. The example has an empty filename and a very large source-line value; its source kind and affected extent remain unknown. | Exact ID and persistent-reader source. Preserve empty outer filename. E2 / H2; representative assignment is provisional. No current SQL records. |
| **Wrong operator for a simple-assignment trigger** — `Trigger is simple assign, but used a symbol other than '=' in the middle` | Observed selected ID `0b2804538785c71278ea37e7` | **Confirmed context-specific syntax/form diagnostic.** CK3 explicitly rejects the operator for this trigger. It identifies the trigger invocation, not a whole-file or session failure. 132 occurrences in 77 logs; eight records/occurrences in current SQL. | Require `jomini_script_system.cpp`, this ID, and the exact present body binding `s1` of type `REASON` equal to the quoted reason. Do not select the whole template. E3 / P1. |
| **Unexpected token in a localization entry** — `Unexpected localization token 's' at line 93 and column 28 in ...`; observed comma variant too | `d3e23fc8aad5883970f02964` (`s`, fixed line/column); `3ee5943a9d6e695efc7f6f1c` (comma, variable line/column) | **Confirmed localization syntax diagnostic.** Reports a token rejected while reading an entry. Current source corroborates the stray `s` after a closing quote. Entry/file remainder behavior is not established. 83 occurrences in 79 logs: 78 `s`, five commas. | Exact IDs and `localization_reader.cpp`; do not generalize the fixed literals into an imagined generic template. E4 / P1, E5 / H3. The eight current SQL records are all provisional. |
| **Missing quoted localization value** — `Missing quoted string value for key 'dynn_Abronius' at line 2117 and column 16 in ...` | `437a7f59c0736bb3b46b6e2f` | **Confirmed localization syntax diagnostic.** A required quoted value was not read for this key. One occurrence in one log. Does not distinguish a missing opening quote from an earlier disruption, or establish whole-file rejection. | Exact ID and localization-reader source. Key and line/column are literal in this definition; path is variable. E6 / H3, provisional representative. No current SQL records. |
| **Unterminated localization substitution** — `Unterminated '$' at position ... in $...$ localization replacement` | `7657bd29deb139cb27588ed9` | **Confirmed delimiter syntax diagnostic in localization replacement.** Four occurrences in one log. At least that substitution is malformed; no evidence the whole localization file is rejected. Logged positions are large negative values, so they are not reliable navigation offsets. | Exact ID and `pdx_data_localize.cpp`; keep key, position and file values verbatim. E7 / H4. No current SQL records. |
| **Required escaping missing in localization replacement** — `is missing required quote-escaping` (required form: `$...\|q$`) | `14f626fdc756e7881168c8b0` | **Confirmed quoting requirement violation**, suitable for a localization-syntax section. Fifty occurrences in one log. Wording establishes required escaping is absent, but does not say parsing stopped; rank separately from an explicitly failed parse. | Exact ID and data-localize source. The referenced `$DIARCHY_Dfp_regent$` is literal in this definition, not an arbitrary substitution slot. E8 / H4. No current SQL records. |
| **Trailing characters after a data statement** — `Unexpected characters found at end of Statement ...` | `0d942a44097fd983668bacfd` | **Confirmed expression syntax diagnostic.** The parser reports unconsumed trailing text, here `( GetPlayer )`. Two occurrences in two logs. Establishes incomplete acceptance of this expression, not which GUI file failed or whether a partial expression was used. | Exact ID and `pdx_data_statementparser.cpp`. This observed statement is literal in the model. E9 / H5; provisional representative. No source-file locator exists in this diagnostic. |
| **Unexpected named token / expanded token** — `Unexpected token: decision_has_second_step`; `Unexpected token: monthly_county_control_change_factor ... (expanded from file: ...)` | `dcc726d7285cda9a0a94e1f7`; `2ec1bc21b344e9fe4e66b408`; model also contains alternate expanded-layout ID `580538c57a6bff2c90abde24` | **Context-dependent candidate.** Can be an unsupported/contextually misplaced keyword, compatibility problem, or fallout from earlier structural corruption. Ordinary names are not proof of brace syntax failure. Current SQL: 192 ordinary and 31 expanded records, all one occurrence each. | IDs/source identify the candidates, with KEY and inner/outer/expanded LOCATOR bindings. No stored field identifies which cause applies. E10 / P1; cascade H1. |
| **Generic malformed token** — `Malformed token: @provisions_cost_infantry_cheap` (other retained examples contain numbers) | `e9c7a6cdb699dcb181672139` | **Context-dependent candidate.** Direct evidence that this reader could not accept the token, but not that the token is lexically malformed in all contexts. `@name` is a documented reader-variable syntax; missing/unavailable substitution or context remains possible. Eight current SQL records/occurrences. | Exact ID/source selects the candidate; KEY alone cannot distinguish missing substitution, invalid value or structural corruption. E11 / P1. The separate literal-brace ID above is narrower. |
| **Failed GUI/data-system parsing** — `Failed parsing data statement '...' for property '...'(...)`; `Failed parsing localized text: [...]` | Observed selected `6fd43d3e3e0e7ff80e876eb4`, `bd1e5f96bdefe7e06ebec219`, `9d9026e75908fcd2914918db`; model also contains `f7b0881b73fc54ce846c8053` | **Context-dependent candidate despite explicit parse failure.** Eighty-two messages across three logs establish a failed statement/localized-text operation. H3 has preceding missing-type/promotion/conversion errors for the same expression: a semantic binding failure is a serious alternative to grammar failure. Impact is the property/text expression; whole-window failure is not established. | IDs and sources `pdx_gui_factory.cpp` / `pdx_gui_localize.cpp` can select a “parse/conversion failure” view. Definition/value fields do not store a causal relation to adjacent emissions. E12 / H3 and cluster below. No current SQL records. |
| **Failed key reference, especially punctuation in the reference** — `Failed to read key reference: }: }, near line: ...` | Literal-brace ID `b62acdb1e71cd82b1c1ae00d`; generic `ba9391e538a1f5a1a68b54c6` | **Context-dependent candidate.** Four literal-brace occurrences in four logs strongly suggest structural misinterpretation. Generic messages also contain empty or ordinary named references. Do not turn the entire key-reference family into confirmed syntax. | Exact literal-brace ID/source supports a narrow warning. Generic OPTIONAL_KEY values preserve the actual references, but not why lookup/read failed. H2 log line 4127 and E2 context. No current SQL records. |

The model-only GUI variant `f7b...` was not the selected ID for the inspected
government-administration example: the existing matcher selected `6fd...`.
Model membership is not proof a definition was selected for a particular occurrence.
The IDs above are package-specific research recommendations, not a portable
unversioned taxonomy.

## Exclusions and unresolved near-misses

These messages can be serious and deserve their own reporting categories. Their
wording does not establish syntax, and recurrence does not change that conclusion.
All P1 ordinals below are zero-based stored diagnostic ordinals.

| Investigated message and genuine reference | Template ID(s) | Why unsuitable for automatic syntax inclusion |
|---|---|---|
| `Unknown trigger: has_graphical_celtic_culture_group_trigger` — P1 ordinal 274, native log line 278; `Unknown effect: rv_rescue_imprisoned_character_effect` — ordinal 375, line 382 | `01adbdfa8f9244dfd17710d6`; `8d107a58292c284eed607a4b` | Unknown callable/definition or wrong context; missing dependency or version mismatch is possible. The persistent-reader emitter alone is not a syntax classification. Current SQL has 7,376 unknown-trigger occurrences, which does not make them syntax. |
| `Unrecognized loc key mcr_revenge_war_invalidated_desc` — P1 ordinal 276, line 280 | `da538ceb80a2deb0905d6030`; other stored loc-key variants include `61f4da73cf00b35821b2a1b0`, `b1f01f162da0f074a3454a1a`, `783d4d8582f74f797ada703e` | Missing or mismatched localization identifier. Different from a localization reader rejecting the entry's grammar. |
| `Modifier 'ennobled_prestige_modifier' doesn't match expected type 'character', due to 'none'` — P1 ordinal 975, line 1753 | `5df7b728388cc7666bb652e9`, with typed `REASON` | Type/definition compatibility. Even a historical reason ending `due to '}'` is not itself an explicit brace-balance diagnostic. |
| `Wrong scope for trigger: none, expected character` — P1 ordinal 2460, line 4868 | `3139bef655a77313a897fb21` in this example; other script-error layouts also carry REASON | Scope mismatch. The word `expected` describes an object type, not a missing syntactic delimiter. |
| `Failed context switch` — same broad trigger-error ID used by E3 | `0b2804538785c71278ea37e7`, different `s1` REASON | 61,557 current SQL occurrences under this ID are this reason. Selecting the whole ID for syntax would be badly misleading. |
| `Compiling source for modify_allies_of_participants_fame_values failed for unknown arguments: LOSER, WINNER_FAME_SCALE, LOSER_FAME_SCALE` — P1 ordinal 532, line 637 | `9af302e5d6165f121a1bdeec` | Explicit compilation failure, but reported cause is an argument-interface mismatch. A serious failure is not automatically a grammar error. |
| `Failed to find pattern texture at path: gfx/coat_of_arms/patterns/pattern_chief_crenelated.dds` — P1 ordinal 822, line 1569 | `a3c0f7b704c8a4894a33e1b8` | Missing asset/path/dependency, not script grammar. |
| `Expected more data in the texture mipmaps than was actually present in file: gfx/interface/window_character/character_view_prowess_bg.dds` — P1 ordinal 157, line 158 | `5f9b2a5ab62409c7c686d325` | Texture payload/format problem. Not an unexpected ending of a CK3 script file. |
| `'}' is not a valid event ID, can't be 0`; `Namespace '}' used in event '}' ... is not defined in this file - it might not load properly.` — H1 lines 11365–11366 | `633b66f48955f99e4d4867cd`; `bec8986849a22c9979ba8896` | **Unresolved structural clues**, suitable as cluster context. The literal brace is suspicious, but the messages themselves are event-ID/namespace validation. Generic variants `039061d8abd1fe205574e64e`, `d787d9ed7b43dd8d7370ec64` also cover ordinary identifiers. |
| `create_character_memory effect [ Missing participant definition for tag '=' ]` and the same wording with tag `'{'` — P1 ordinals 984–985; source `common/character_interactions/lbr_ennoblement_interactions.txt:336` | `5df7b728388cc7666bb652e9`, with distinct exact `REASON` values | **Context-dependent structural clues.** Punctuation interpreted as participant names suggests an incorrect construct shape, but the stated failure is a missing participant definition. The same family also names `type` and `character`. Do not mark the whole effect-error template as syntax. The two punctuation reasons account for 32 records / 48 occurrences in current SQL, excluded from the confirmed total. |
| `Invalid left side during comparison 'global_var'`, unset scope and unset variable messages — Run `20260928-CHXRHV` review shard | No selected assignment for these particular retained units | Unavailable runtime values, not demonstrated token grammar failure. Review evidence must remain visible; “no match” does not mean syntax. |

## Observed clusters and limits on cascade inference

**H1: event-file cluster.** At 14:38:18, log lines 11360–11386 report ordinary
tokens such as `name`, `add_trait`, `if` and `ai_chance`, then `Theme missing in
event 'option'`, brace-valued namespace/ID failures, the rejected `=` at source
line 194, and further named-event and `=` errors at later source lines. The
printed inner/outer source lines for the first `=` are 194 and 515; those are
reported locations, not a proven skipped interval. Subsequent named-event errors
reach source lines in the thousands. This is consistent with a disrupted parse
context affecting multiple constructs. The first highlighted `=` is already
preceded by suspicious messages: it cannot be declared the root cause.

**H2: empty-filename cluster.** Log line 4127 rejects a `}` key reference;
4128–4134 contain seven malformed tokens in one native emission, including the
opening brace at line 4133. Subsequent emissions reject a number and names such
as `target`, `leader` and `discontent`. The reader prints `in file: ""` and source
lines around 23,876,612. No evidence here licenses assigning a mod file, interpreting
this as a normal source file, or asserting a corrupt save. The native wrapper
applies to the component messages; seven components are not seven original headers.

**H3: semantic failure followed by “parsing” failure.** At 18:16:20, lines
2158–2164 successively report failure to find type `GuiFaithDoctrineItem`, failure
to find its promote, failure to convert argument 0 of `GetName`, failure to convert
the expression, failed localized-text parsing, and failed conversion of GUI
property `text`. The shared expression gives stronger evidence of a related
failure sequence than mere timestamp proximity. It still does not prove engine
control flow, and specifically argues against assuming malformed braces.

A demonstrated cascade would need the exact contemporaneous source files and
effective load order, a located initial defect, and a naturally available
before/after repair comparison under otherwise comparable game/mod versions.
Engine tracing or authoritative recovery documentation could establish which
constructs are skipped. No mod file was broken or repaired for this research.
Do not automatically suppress later messages, infer a root cause, or derive a
damage radius from these clusters. Stored representative ordinals can help show
nearby first occurrences, but cannot reconstruct every repeated sequence.

## Brace-token follow-up — 2026-10-01

At the owner's request, searched for opening and closing braces after `token:`,
with and without single/double quotes, and inspected the grouped brace-bearing
native lines. The follow-up covers **82 distinct log contents, 673,596,198 bytes**:
the original 81 plus one newly readable retained pending capture. Twenty-two
pending directories remained inaccessible. This extends the native search only;
the eight-Run SQL snapshot and its counts above were not refreshed.

The opening-brace rejection remains **four `Malformed token: {` occurrences in
four logs**. There was **no `token: '}'`, `token: "}"`, or unquoted `token: }`
occurrence** in this search. There were nine lines containing quoted `'}'` across
three logs, in the following other diagnostic contexts:

| Actual wording / context | Native count and example | Verified template ID / representative status | Assessment for reporting |
|---|---|---|---|
| `Namespace '}' used in event '}' ... is not defined in this file - it might not load properly.` | Two in H1; line 11365, emission 8029 | `bec8986849a22c9979ba8896` / `template`; `jomini_eventmanager.cpp` | Context-dependent structural clue. The engine is treating the brace as a namespace/event name; the message states namespace validation failure. |
| `'}' is not a valid event ID, can't be 0` | Two in H1; line 11366, emission 8030 | `633b66f48955f99e4d4867cd` / `provisional`; `jomini_eventmanager.cpp` | Context-dependent structural clue. Confirms rejection of this event ID, without locating a missing or extra delimiter. |
| `Theme missing in event '}'` | Two in H1; line 11400, emission 8064 | `a42a088596f3afe33008ce41` / `provisional`; `event.cpp` | Context-dependent cluster evidence. Confirms a missing theme for the brace-valued event, not a grammar diagnosis. |
| `Duplicated event ID '}' found. New Location: ... Previous Location: ...` | One in H1; line 14020, emission 10605 | `ef9bf9a0e957c9cb026803d9` / `provisional`; `jomini_eventmanager.cpp` | Context-dependent cluster evidence. Both printed locations identify source line 194; duplicate registration alone does not establish the underlying source defect. |

The four assignments were verified by passing genuine H1 emissions through
the selected package's existing reader and matcher, in memory. Their exact
template IDs and source families can identify them in stored records for an
optional contextual view; no new matching pass is needed. They remain outside
the nine confirmed selectors. Existing records do not establish whether these
messages share one cause or which opening/closing brace would need correction.

The remaining two quoted-brace lines report
`has_house_modifier trigger [ Modifier 'trad_authority' doesn't match expected type 'character' due to '}' ]`
in two logs, including H4 line 2479. The reported failure is modifier type
compatibility; the brace in its explanation remains unresolved and does not
qualify it for the syntax preset.

E13 below shows the brace-valued namespace/ID messages immediately before the
verified unexpected-equals rejection. The later duplicate-ID message points back
to the same printed source line 194. This strengthens the interpretation of a
disrupted event parse context, but does not demonstrate an unbalanced brace or
prove that `Malformed token: {` is CK3's brace-imbalance diagnostic. The latter
comes from the separate empty-filename H2 cluster, not this event-file sequence.

Other brace occurrences reinforce the need for narrow reporting: the unquoted
`Failed to read key reference: }: }` occurs four times in four logs (E2), while
`Missing participant definition for tag '{'` occurs 146 times across 73 logs.
Neither states a brace-balance failure. Native `{}` formatting placeholders,
GUI container messages and building-list dumps also contain braces without
establishing delimiter errors. No explicit brace-balance wording was found.

The additional pending log is
`.ck3chronicle/wip/runtime/pending/20260930T143407.348249Z-VCaXNrgO/error.log`,
SHA-256 `d48fd874051504f5f2f1b35eba819e712d4d0954ce620548f5cd234fd496b607`,
6,685,782 bytes. The dated hash inventory, search counts and representative
assignments are retained in ignored research scratch as
`.codex-tmp/syntax-research/brace-followup-20261001.json`.

## CK3-specific external and source documentation

Sources were consulted on 2026-09-30. None provides an exhaustive native CK3
syntax-diagnostic catalogue or a universal recovery/whole-file-abort guarantee.

- **Primary, CK3 developer:** Matthew's [Dev Diary #37 — Making Mods](https://forum.paradoxplaza.com/forum/developer-diary/ck3-dev-diary-37-making-mods.1410656/)
  identifies Jomini as CK3's scripting layer and explicitly links the Jomini
  manuscript. It also distinguishes GUI scripting from normal database/event
  script. This supports keeping the language contexts separate, not treating all
  emitters as one grammar.
- **Primary, shared-engine developer documentation:** the [Grand Jomini Modding
  Information Manuscript](https://forum.paradoxplaza.com/forum/threads/grand-jomini-modding-information-manuscript.1170261/)
  describes comparison operators, generated scope/effect/trigger documentation,
  and the GUI/localization Data System's types, promotes, functions and callbacks.
  CK3's diary establishes relevance, but the 2019 manuscript is shared-engine
  documentation, not proof that every current CK3 behavior is identical. It
  supports the semantic alternative in H3 and the need for trigger-specific
  operator rules.
- **Primary, installed CK3 documentation:**
  `C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/reader_export/_reader_export.info`,
  especially lines 7–27, documents reader-variable declaration/loading with
  `@name` and token-stream substitutions. Thus the `@` in E11 is not enough to
  diagnose a spelling/lexical error. The installed
  `common/decisions/_decisions.info` also describes nested constructs and their
  contexts. These are current local documents, not archived documentation for
  every historical run.
- **Community-authored CK3 documentation:** the [Scripting page](https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Scripting.md)
  documents assignment/block forms and separates triggers, effects and GUI use;
  [Localization](https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Localization.md)
  documents quoted values and `$...$` substitutions;
  [Mod troubleshooting](https://github.com/jesec/ck3-modding-wiki/blob/master/wiki_pages/Mod_troubleshooting.md)
  distinguishes missing localization keys and scope problems. These are readable
  mirrors of community wiki pages; the direct Paradox-wiki pages were inaccessible
  through the browser. The localization page labels itself last verified for 1.4.
  Use these as contextual explanations, not current authoritative error wording.
- **Community tool, author's own documentation:** [Tiger's README](https://github.com/amtep/tiger)
  distinguishes syntax validation, missing items/localizations and scope checks,
  and acknowledges false positives and update lag. Its diagnostics are not CK3
  native emissions. No Tiger/tool-generated message was added to the proposed list.

### Limit of the documentation evidence

The external documentation explains syntax forms but does not verify additional
native diagnostic wording for this handoff. It contributes no extra selectors.
In particular, the verified brace and equals examples establish token rejection
only; the verified `Unterminated '$'` message concerns localization substitution,
not file EOF. Unverified brace-balance and premature-ending formulations are
excluded from the recommended list rather than reserved as hypothetical entries.

## Coverage and limitations

- The native corpus is the union of the retained v45 input inventory's 73 hashes
  and eight readable current pending captures: **81 distinct SHA-256 contents,
  666,910,416 bytes**. Thirty-eight runtime session copies duplicate hashes in
  the 73-file inventory and are counted once. Directory names in the old session
  store are not assumed to equal file content hashes.
- The current SQL snapshot contains eight Runs, **20,281 records**, **266,381
  eligible occurrences**, and 210 used definitions. All eight Runs use the selected
  package above. Runs are `20260928-GW43YB`, `20260928-M7HR5W`, `20260928-YU0JAK`,
  `20260928-30BUN6`, `20260928-CHXRHV`, `20260930-BYVZUV`, `20260930-RPNL9U`,
  `20260930-88WBO5`. Counts are a bounded read snapshot, not a promise the live
  database will stay at eight Runs.
- All eight review shards were included in evidence inspection/search. Six are
  nonempty; stored metadata accounts for **17,421 no-match units**, zero unresolved
  recovery units and zero input failures. Review content includes recurring
  unset-variable/scope errors and character evidence. No matched row was invented
  for it. Review bytes overlap the original logs and are not extra independent logs.
- Discovery searched template displays, all reconstructed stored messages, and
  genuine bytes for token/parse/syntax/delimiter/quotation/assignment/ending leads.
  Targeted exact-wording counts and surrounding native excerpts were then checked.
  This is not exhaustive manual review of every emission. Search normalization in
  ignored scratch summaries is only an exploration aid, never classification data.
- Twenty-two older pending directories were inaccessible during inventory discovery;
  permissions were not changed. The configured locked public corpus directory was
  absent. Arbitrary benchmark/rehearsal copies, the legacy database, live game logs,
  and crash dumps were not treated as extra independent corpus coverage.
- The retained logs are strongly correlated modded runs. Repetition across hashes
  does not provide independent experiments. Historical CK3 versions and the exact
  effective historical source files were not established. Logs can contain large
  repetitive sections; no frequency is presented as a measure of damage.
- Current source readback corroborates E3 and E4: workshop item `2753934263`,
  `common/character_interactions/xx_baie_education_interactions.txt:715` contains
  `has_focus != education_learning`; item `3076887545`,
  `localization/english/music_l_english.yml:93` contains
  `ahrimans_wrath: "Achaemenes"s`. Item `3595441040` places the E10 keywords inside
  a `widget` block. One current local `paighan_fix.txt` contains the E11 `@name`
  reference at line 28. These are read-only present-day candidates, not proof of
  historical effective-file ownership, missing dependencies, or the exact repair.
- Ignored research read snapshots, hash inventory, search counts and representative
  matcher evidence are under `.codex-tmp/syntax-research/`. No raw capture,
  database, review shard, model artifact, selection, runtime code or mod source
  was changed by this work. No service was restarted and no capture was ingested.

## Bounded recommendation for future reporting

Reporting and Analysis should review the concrete selector handoff above when
implementing the syntax preset under 08A/08B. It is limited to the verified
families and the exact `REASON` predicate for E3. Include both match statuses by
default and display provisional status
explicitly. For this database snapshot, the result is the 16 records stated above;
do not silently broaden it to fill a sparse report.

Render the stored message with the owning renderer and show Run ID, family
explanation, occurrence count, source/emitter and the supplied locators. Keep
context-dependent reader/parse failures outside this preset; they remain available
through ordinary report filters. State
the supported extent, such as a rejected token, trigger invocation or localized
expression; use “extent unknown” when appropriate. No stored severity, syntax
boolean or `error_type` migration is needed to express this proposal.

Real gaps remain: there is no stored causal linkage, exact affected-file extent,
per-occurrence timeline, historical source snapshot, or guarantee that unresolved
review evidence will be searchable as SQL diagnostics. Some messages lack a file
locator; negative localization positions are not navigable offsets. Some clear
historical families are absent from current SQL. Package changes require renewed
definition/selector review. Report these limits; do not solve them with raw-message
rematching, production ingestion, generated examples, model changes or automatic
root-cause assertions as part of this assignment.

## Source register and readable genuine examples

The following excerpts are actual messages, not demonstrations manufactured to
look like CK3 output. SQL renderings omit native timestamp headers as designed.
Line-ending style is normalized for this Markdown display only. Native source
hashes identify the exact inspected bytes; physical log lines are one-based.

| Reference | Genuine source and content SHA-256 |
|---|---|
| P1 | [Retained native log](C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/pending/20260930T074832.800991Z-ga9O9i6j/error.log); SHA-256 `42b946899cc94194d5d9baccc2dc119e2de34528cc7d2d77c1a8c0a934324794`. Stored Run `20260930-88WBO5`. |
| H1 | [Retained native log](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/99532085d7e7e1e4cde5192bb698738b6eb7d2e4024155f3044f44e2fd5a9dff/error.log); SHA-256 `99532085d7e7e1e4cde5192bb698738b6eb7d2e4024155f3044f44e2fd5a9dff`. Historical native log; no current Run association asserted. |
| H2 | [Retained native log](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/137715f59da017220e158899b52d8652e168ddb0b3fc242c37967d993c64df6b/error.log); SHA-256 `137715f59da017220e158899b52d8652e168ddb0b3fc242c37967d993c64df6b`. Historical native log; no current Run association asserted. |
| H3 | [Retained native log](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740/error.log); SHA-256 `cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740`. Historical native log; no current Run association asserted. |
| H4 | [Retained native log](C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/sessions/dd9d51a224c72ae1be8e89b4e74e0cb1c57d3ae6b3f07b042229e402949c5d40/error.log); SHA-256 `6a558de2cc355bf05eb085214bfd0bb1c6167c9c8e36e17885a62a7fc0901d28`. Historical native log; no current Run association asserted. |
| H5 | [Retained native log](C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/sessions/2245666ad17d89b44fdaef0d3ab69d4566775df755b2fea1b6e6ac7851197e78/error.log); SHA-256 `3ccf41d39129f60ae9175271bfe536e4ae54c7ac40bff50d2de8e62a079ee0c5`. Historical native log; no current Run association asserted. |

### E1 — Rejected equals token

H1, physical log lines 11367–11367, byte interval `[1948610, 1948790)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/99532085d7e7e1e4cde5192bb698738b6eb7d2e4024155f3044f44e2fd5a9dff/error.log:11367).

```text
[14:38:18][E][pdx_persistent_reader.cpp:216]: Error: "Unexpected token: =, near line: 194" in file: "events/education_and_childhood/child_personality_events_2.txt" near line: 515
```

### E2 — Rejected opening brace inside a multi-message emission

H2, physical log lines 4127–4134, byte interval `[551518, 552048)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/137715f59da017220e158899b52d8652e168ddb0b3fc242c37967d993c64df6b/error.log:4127).

```text
[10:31:27][E][pdx_persistent_reader.cpp:216]: Error: "Failed to read key reference: }: }, near line: 23876606" in file: "" near line: 23876606
[10:31:27][E][pdx_persistent_reader.cpp:216]: Error: "Malformed token: 161456, near line: 23876606
Malformed token: 33605552, near line: 23876607
Malformed token: 8, near line: 23876608
Malformed token: 62.234, near line: 23876609
Malformed token: 80, near line: 23876610
Malformed token: {, near line: 23876612
Malformed token: 3, near line: 23876617" in file: "" near line: 23876619
```

### E3 — Simple-assignment trigger operator

P1, Run `20260930-88WBO5`, stored ordinal `366`, template `0b2804538785c71278ea37e7`, `template`, count `1`; representative emission(s) `[365]` (zero-based).

```text
 Script system error!
  Error: has_focus trigger [ Trigger is simple assign, but used a symbol other than '=' in the middle ]
  Script location: file: common/character_interactions/xx_baie_education_interactions.txt line: 715 (educate_child_interaction:ai_will_do)
```

### E4 — Unexpected localization token

P1, Run `20260930-88WBO5`, stored ordinal `95`, template `d3e23fc8aad5883970f02964`, `provisional`, count `1`; representative emission(s) `[95]` (zero-based).

```text
 Unexpected localization token 's' at line 93 and column 28 in localization/english/music_l_english.yml
```

### E5 — Unexpected comma in localization

H3, physical log lines 749–749, byte interval `[158562, 158723)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740/error.log:749).

```text
[18:15:35][E][localization_reader.cpp:581]: Unexpected localization token ',' at line 143 and column 62 in localization/english/events/tfe_events_l_english.yml
```

### E6 — Missing quoted value

H3, physical log lines 158–158, byte interval `[29674, 29855)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740/error.log:158).

```text
[18:15:33][E][localization_reader.cpp:535]: Missing quoted string value for key 'dynn_Abronius' at line 2117 and column 16 in localization/english/dynasties/TFE_dynn_l_english.yml
```

### E7 — Unterminated localization substitution

H4, physical log lines 180–180, byte interval `[35025, 35253)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/sessions/dd9d51a224c72ae1be8e89b4e74e0cb1c57d3ae6b3f07b042229e402949c5d40/error.log:180).

```text
[15:49:38][E][pdx_data_localize.cpp:349]: Loc key `dfp_regency_stability_MIN_LABEL`: Unterminated '$' at position -2501362365707 in $...$ localization replacement - file `localization/english/LOC_Situations_COPF_l_english.yml`
```

### E8 — Required quote escaping

H4, physical log lines 153–153, byte interval `[28027, 28289)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/sessions/dd9d51a224c72ae1be8e89b4e74e0cb1c57d3ae6b3f07b042229e402949c5d40/error.log:153).

```text
[15:49:38][E][pdx_data_localize.cpp:279]: Loc key `DECISION_Normalize_dfp_regent_power.DESC`: `$DIARCHY_Dfp_regent$` at position 166 is missing required quote-escaping (`$...|q$`) - file `localization/english/LOC_Decisions_Feudal_dfp_regent_COPF_l_english.yml`
```

### E9 — Unconsumed expression suffix

H5, physical log lines 21286–21286, byte interval `[1798121, 1798299)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.ck3chronicle/wip/runtime/sessions/2245666ad17d89b44fdaef0d3ab69d4566775df755b2fea1b6e6ac7851197e78/error.log:21286).

```text
[15:51:51][E][pdx_data_statementparser.cpp:237]: Unexpected characters found at end of Statement 'GetTravelOption('tutor_child_option').GetName ( GetPlayer )': '( GetPlayer )' 
```

### E10 — Unexpected named token: context-dependent

P1, Run `20260930-88WBO5`, stored ordinal `291`, template `dcc726d7285cda9a0a94e1f7`, `template`, count `1`; representative emission(s) `[291]` (zero-based).

```text
 Error: "Unexpected token: decision_has_second_step, near line: 56" in file: "common/decisions/vata_varangian_decisions.txt" near line: 62
```

### E10b — Expanded unexpected named token: context-dependent

P1, Run `20260930-88WBO5`, stored ordinal `476`, template `2ec1bc21b344e9fe4e66b408`, `template`, count `1`; representative emission(s) `[529]` (zero-based).

```text
 Error: "Unexpected token: monthly_county_control_change_factor, near line: 40 (expanded from file: common/buildings/holy_stuff_common_buildings.txt line: 41)" in file: "common/buildings/holy_stuff_common_buildings.txt" near line: 40
```

### E11 — Malformed named token: context-dependent

P1, Run `20260930-88WBO5`, stored ordinal `362`, template `e9c7a6cdb699dcb181672139`, `template`, count `1`; representative emission(s) `[361]` (zero-based).

```text
 Error: "Malformed token: @provisions_cost_infantry_cheap, near line: 28" in file: "common/men_at_arms_types/paighan_fix.txt" near line: 28
```

### E12 — Type/conversion failures accompanying localized-text parse failure

H3, physical log lines 2158–2164, byte interval `[463305, 464168)`. [Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740/error.log:2158).

```text
[18:16:20][E][pdx_data_factory.cpp:1364]: Failed to find type 'GuiFaithDoctrineItem' in 'GuiFaithDoctrineItem.GetFaith '.
[18:16:20][E][pdx_data_factory.cpp:1371]: Could not find promote for 'GuiFaithDoctrineItem' in 'GuiFaithDoctrineItem.GetFaith '.
[18:16:20][E][pdx_data_factory.cpp:1072]: Failed to convert statement for argument '0' for call 'GetName' in 'FaithDoctrine.GetGroup.GetName( GuiFaithDoctrineItem.GetFaith )'
[18:16:20][E][pdx_data_factory.cpp:1052]: Failed converting statement for 'FaithDoctrine.GetGroup.GetName( GuiFaithDoctrineItem.GetFaith )'
[18:16:20][E][pdx_gui_localize.cpp:358]: gui/window_faith_creation.gui:1298 - Failed parsing localized text: [FaithDoctrine.GetGroup.GetName( GuiFaithDoctrineItem.GetFaith )]

[18:16:20][E][pdx_gui_factory.cpp:939]: gui/window_faith_creation.gui:1298 - Failed converting property 'text'(143)
```

### E13 — Quoted closing braces in event diagnostics

H1, physical log lines 11365–11367, byte interval `[1948320, 1948790)`.
[Open excerpt](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/99532085d7e7e1e4cde5192bb698738b6eb7d2e4024155f3044f44e2fd5a9dff/error.log:11365).

```text
[14:38:18][E][jomini_eventmanager.cpp:574]: Namespace '}' used in event '}' (file: events/education_and_childhood/child_personality_events_2.txt) is not defined in this file - it might not load properly.
[14:38:18][E][jomini_eventmanager.cpp:137]: '}' is not a valid event ID, can't be 0
[14:38:18][E][pdx_persistent_reader.cpp:216]: Error: "Unexpected token: =, near line: 194" in file: "events/education_and_childhood/child_personality_events_2.txt" near line: 515
```

Later in H1, physical log line 11400, byte interval `[1955198, 1955256)`:

```text
[14:38:18][E][event.cpp:368]: Theme missing in event '}'
```

Later still, H1 physical log line 14020, byte interval `[2413036, 2413314)`:

```text
[14:38:20][E][jomini_eventmanager.cpp:428]: Duplicated event ID '}' found. New Location: 'file: events/education_and_childhood/child_personality_events_2.txt line: 194 (})', Previous Location: 'file: events/education_and_childhood/child_personality_events_2.txt line: 194 (})'
```

These are separate excerpts, not an uninterrupted sequence. The first two lines
precede the `=` rejection; the later two do not establish a causal chain.
