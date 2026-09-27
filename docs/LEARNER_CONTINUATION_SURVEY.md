# Native continuation survey before message recovery

Date: 2026-09-20. This is evidence gathering for the shared parser, before the
learner refactor. No parser recovery or pipeline caller code changed in this
survey.

**Subsequent implementation:** recovery is now delivered and inspected against
these stable inputs. See the [pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md)
and [23 recovered outputs](../.codex-tmp/message-recovery-review/RECOVERED_EXAMPLES.md).
The findings below preserve the pre-implementation survey evidence. The owner
clarified that failure plus reason includes L1/L2 contracts and is one message;
those parts must never be split into sibling errors.

## Finding

The available logs contain more multi-message forms than the earlier inspection
found. **Individual messages must be recovered before learning or classification.**
The emission remains their lossless parent, not their substitute.

The strongest observed recovery structure is the persistent-reader wrapper:
`Error: "..." in file: "..." near line: ...`. Its enclosed messages occupy
separate physical lines, each with its own location suffix. Message introductions
vary and can differ within one emission. This supports recovery from the
wrapper/line/location structure rather than an enumeration of two error phrases.

Other observed multiline forms contain one failure plus a trace, structured
details, a multiline reason, or a quoted multiline value. Those require keeping
the content together. These findings establish an observed grammar to implement
and review; they do not establish every possible CK3 logging form.

## Corpus and method

- Discovered 117 readable error-log paths in the repository runtime/rehearsal
  data and configured CK3 log/crash directories. Content deduplication removed
  43 identical copies, leaving 74 distinct file contents at inventory time.
- Surveyed **73 stable distinct logs**, totaling 596,625,707 bytes and
  **2,517,940 emissions**. The live `logs/error.log` changed between inventory
  and parsing and was excluded. No archived input failed raw parsing.
- Directory discovery reported access denied for 22 protected pending
  directories. Readable rehearsal captures were included, but this survey does
  not certify that they replace every inaccessible input.
- Selected `ck3-lossless-v1` explicitly, using its existing implementation hash
  `0bca019faa9abdce55d063577d733bef9a864bb5453a103376bc2eab1c310e03`.
- Inspected every emission for nonblank continuation lines, regardless of source
  or error wording. Also collected quoted error wrappers and repeated-label
  leads on single lines. Counted blank-only continuations separately. Physical
  lines use LF boundaries; CK3 control characters were not treated as newlines.
- Retained 1,242,621 candidate occurrence references and 22,681 distinct native
  candidate bodies. Review indexing produced 4,243 shapes; those index labels
  are not parser rules or a claim of 4,243 different message formats.

There were 1,185,709 emissions spanning multiple physical lines: 1,185,017 with
nonblank continuation content and 692 with only blank trailing lines. No
timestamp-header-looking continuation was flagged. Counts describe these files;
different runs can share content even after identical-file deduplication.

The reusable discovery/collection tool is
[survey_continuations.py](../tools/template_learning/survey_continuations.py).
Generated evidence is ignored local data:

- [Scope, failures and counts](../.codex-tmp/continuation-survey/summary.json)
- [Input paths, hashes and discovery errors](../.codex-tmp/continuation-survey/inputs.json)
- [23 complete native examples](../.codex-tmp/continuation-survey/NATIVE_EXAMPLES.md)
- [Detailed wrapper/reason observations](../.codex-tmp/continuation-survey/review-observations.json)
- [Full selected example records](../.codex-tmp/continuation-survey/review-examples.json)

The same directory contains all candidate bodies (`bodies.jsonl`), all native
occurrence references (`occurrences.jsonl`), the review shape/line indexes and
the example-generation script (`review.py`). Native evidence stays outside Git.

## All observed sources of nonblank continuation content

| Engine source | Emissions | Observed structures / interpretation |
|---|---:|---|
| `pdx_persistent_reader.cpp` | 10,404 | Multiple separately located messages within one quoted wrapper. Recover individual messages and retain shared wrapper context. |
| `jomini_script_system.cpp` | 1,174,361 | One `Error:` field and one `Script location:` field per observed emission. Reasons and traces can each span additional lines. |
| `jomini_effect_impl.cpp` | 214 | 208 participant-detail emissions (`Cheater:`, `With:`); six emissions with an explicit `Stack trace:` and file frames. |
| `event.cpp` | 10 | Failure followed by a `From:` location. |
| `activity_type.cpp` | 9 | Failure followed by `Root:`, blank separators and `Saved event targets:`. |
| `faction.cpp` | 7 | Failed action followed by a formatted explanation. |
| `pdx_text_formatter.cpp` | 6 | Reported formatting tag itself contains newlines and a blank line inside quotes. |
| `character_commands.cpp` | 5 | Failed title grant followed by a doctrine explanation. |
| `pdx_data_localize.cpp` | 1 | Quoted localization value contains multiple paragraphs and nested quoted text. |

The source counts exhaust the nonblank-continuation inventory for this corpus.
Interpretations are based on native content review; they are not output of an
implemented message-recovery classifier. All seven smaller source families
were inspected directly, alongside the wrapper and script-shape analyses.

## Repeated-message wrappers

Across single-message and multi-message cases, 67,305 persistent-reader emissions
contained 143,966 enclosed message lines. Of these emissions, 10,404 contained
multiple messages. Observed batch lengths range from two to **915**. The earlier
449-message example was not the largest available case.

The multi-message examples include:

| Message introduction | Enclosed messages in multi-message emissions |
|---|---:|
| `Failed to read key reference:` | 65,132 |
| `Unknown trigger:` | 21,610 |
| `Unknown effect:` | 147 |
| `Unexpected token:` | 144 |
| `Malformed token:` | 28 |
| `Terrain type dry_hills not defined.:` | 2 |
| `Terrain type high_boreal not defined.:` | 2 |

These are observed introductions, not a proposed whitelist. In particular:

1. One wrapper contains `Unknown effect:` followed by `Unknown trigger:`.
   Repetition does not mean identical wording or identical error type.
2. Terrain names occur inside the introduction itself. A fixed introduction
   list would confuse variable content with framing.
3. Empty wrapper filenames occur, including in the longest batch. Retain the
   empty value and its punctuation; it does not invalidate the child boundaries.
4. Every inspected enclosed line has `, near line: <digits>`, optionally followed
   by an `(expanded from file: ... line: ...)` annotation. There are 219 observed
   expansion annotations, all in single-message wrappers in this corpus.
   The annotation is retained message content, not discarded after the digits.
5. No inspected wrapper had an embedded double quote inside its enclosed text,
   multiple such location suffixes on one physical line, or a child spanning
   multiple physical lines. These are coverage limits, not declarations that
   CK3 cannot emit them.

The wrapper/line/location query accounted for every collected persistent-reader
body with no unmatched form after including expansion annotations. That is
evidence for this grammar on these inputs, not authorization to force unfamiliar
future content through the same split.

## Script errors and genuinely multiline message content

The script-system emissions had two first-line forms:

- `Script system error!` — 1,043,388 occurrences.
- `Script system error! (while building tooltip/description)` — 130,973 occurrences.

Each observed emission had one native `Error:` field and one native
`Script location:` field. The longest trace contained 55 file frames; 9,025
emissions had `Script location: Unknown`. Neither trace length nor a missing
specific location changes the message count.

Seventy-seven distinct script bodies (92 occurrences) additionally contained
reason lines beyond the simple first-line-reason-plus-trace shape. They include:

- Several formatted conditions after `due to:` / `All of these:`.
- Actor, recipient and secondary participant fields.
- `Current Buildings = ...` dumps with nested braces and repeated `Slot` text.
- Reasons ending with a newline before the closing bracket.
- A reported quoted value containing a literal newline.

These are within one native `Error:` field. Recovering that message does not
require assigning semantic L1/L2 structure or treating its constituent reasons
as independent messages. Preserve all of it for subsequent learning.

The other source families show that multiline values and explanations are not
exclusive to script-system errors. In particular, the localization paragraph
and formatting-tag examples rule out treating either a newline or a blank line
as a universal message boundary.

## Single-line leads and remaining uncertainty

The survey also inspected 703 single-line repeated-label candidates outside the
quoted wrapper cases. Their 12 source/label combinations describe paired file
locations, repeated internal IDs, CK3 formatting directives, repeated scopes,
or embedded error text inside a localization value. Review found no demonstrated
independent sibling messages in those candidates. No same-line multi-message
persistent wrapper was observed.

This broader search reduces dependence on an existing phrase list, but it does
not prove that arbitrary single-line concatenation is absent. Likewise,
inaccessible pending directories and the changing live log remain explicit
coverage limits. The whole scan covered the available stable files; it did not
infer missing content or extrapolate a universal CK3 grammar.

## Consequences for the parser work

1. Keep emission framing and lossless original ranges as the parent structure.
2. Implement shared individual-message recovery for the evidenced wrapper
   grammar. Preserve each message's location literal/value/annotation and
   reference the original shared wrapper rather than inventing repeated text.
3. Preserve the observed multiline reason, context and quoted-value forms as
   message content. Recognition cannot mean splitting every non-header line.
4. Return message boundaries before learning or matching. The learner's current
   emission-scoped connection is an unfinished intermediate state and must not
   be treated as the completed input contract.
5. Make unsupported/ambiguous framing visible with its intact evidence. Do not
   turn failure to establish a split into a claim of one recovered message, or
   require an already trained model to recover this observed structural grammar.
6. Inspect recovered outputs against these native patterns and their outliers,
   and reconstruct the original bytes. Then update the pipeline handoff with
   the implemented interface and actual recovery evidence.

This survey completes the requested first investigation. Message recovery
implementation remains the next parser step; learner refactoring follows it.
