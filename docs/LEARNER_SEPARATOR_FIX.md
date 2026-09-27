# Separator and punctuation correction

2026-09-21. Implementation: `ck3-lossless-v1.6`.

The subsequent fresh learner run is complete; see
[learner impact review](LEARNER_SEPARATOR_IMPACT_REVIEW.md) for measured template,
capture and ambiguity changes. The results below concern the parser delivery.

The shared parser now tokenizes with one ordered stdlib regex scanner.
Colon, slash, backslash, braces, brackets, parentheses, double quote, equals,
semicolon and pipe become individual tokens wherever they occur, including
inside text without whitespace. This replaces the old edge-peeling and special
filename/line splitting. The scanner retains every character and whitespace run
and constructs exact absolute byte spans.

`@` stays inside a continuous symbol at any position. Underscores, internal dots
and hyphens, numeric signs and leading/internal filename exclamation marks stay
intact. Word-ending commas and sentence punctuation separate. Non-ASCII edge
punctuation uses the standard-library Unicode categories. `Div/0` remains the
explicit exact-token exception; slash-separated prose remains separate pieces.

Only `lexical_pieces` changed among the existing parser functions/classes;
`_scanner` is the new compiled-regex helper. Emission framing, source facts,
continuation recovery and the raw output interface are unchanged. The parser
artifact remains self-contained and adds no dependency.

## Native evidence

The input is the same fixed selection of ten complete native logs used for the
lexer evaluation, totaling 91,407,302 bytes. No constructed strings or synthetic
emissions are used. The old constructed lexical-example unit test was removed.

Independent comparison of v1.5 and v1.6 confirms identical framing and recovery
for all 343,585 emissions and 352,317 messages, with no unresolved emissions.
Recognized location ranges are unchanged across all 7,827 distinct
source/message pairs. This verifies the existing location consumer; it does not
claim a retrained model or classification-quality improvement.

Nine focused checks passed using the separately annotated complete native log.
They cover exact byte reconstruction, individual separators, known source/range
retrieval, continuation recovery, debug save/reload, independent pipeline loading,
learner collection and feature-cache serialization/selection.

The full token audit passed on all ten logs: 19,623,700 token/gap pieces,
contiguous absolute byte offsets, exact emission and whole-file reconstruction,
and every directed separator isolated wherever present. Boundaries changed in
177,905 emissions. This is a tokenization-change count, not an accuracy score.
All 157 semicolons and 90 pipes are preserved as separate tokens.

Fresh-process timing on the same three complete native logs (43,686,764 bytes),
two repetitions with reversed version order:

| Version | Lexing seconds | Peak process working set |
| --- | ---: | ---: |
| v1.5 | 40.61–40.65 | 168.2–169.7 MiB |
| v1.6 | 28.52–28.54 | 168.6 MiB |

The corrected scanner used about 30% less lexing time in this local comparison.
Timing includes creation of the same Piece/Span objects, excluding reading and
framing. Peak memory covers the whole process, not just the scanner. These are
local measurements with the final implementation, separate from the earlier
Lark evaluation. Raw measurements are in `separator-fix/timing.json`.

The review includes fourteen categories of actual emissions, with complete
original messages and before/after tokens:
[native examples](../.codex-tmp/learner-refactor/separator-fix/NATIVE_EXAMPLES.md).
Its accompanying `native-consumer-review.json` preserves token/gap arrays,
absolute byte offsets, source families, log hashes and emission ordinals.
The first 100 distinct changed emission bodies from the audit are recorded
separately in `audit/native-comparisons.json`; this is not a random sample.

Native examples confirm separation of scope colons, brackets embedded in effect
text, equals, pipes in mesh text and display-control semicolons. They also confirm
preservation of `@cultural_maa_extra_ai_score`, `capital_county.kingdom`,
`!!0_TFE_chars.txt`, `_default_28_shadow.dds`, `Div/0`, and filename/line fields.
Backslash is a directed separator but does not occur in these selected emission
bodies. No new requirement is inferred from absent input cases.

## Integration

Select `tools/template_learning/parsers/v1/manifest.json` explicitly. Its version
is `ck3-lossless-v1.6`, with SHA-256
`a9ed06a6c141a184939518c0b64292b1b48fda7f09fccc9067b3ecd944bd96d6`.
Both the learner and `ck3chronicle.pipeline.raw_input.read_raw_log` already use
that version/hash selection mechanism. Feature-cache identity includes the
parser reference; features from earlier tokenization must be regenerated.
Existing candidate bundles keep their own exact parser reference and are not
silently rewritten. A new candidate must be built with v1.6 before evaluating
its template effects. No model was trained or promoted as part of this fix.

Owner authority is recorded in `tools/template_learning/owner_rules.json`.
The pipeline team's handoff is updated with the new version and changed tokens.
No application caller refactor, runtime registry write or SQL operation was
performed. The v1.5 copy in the ignored review directory is comparison evidence,
not a runtime fallback.
