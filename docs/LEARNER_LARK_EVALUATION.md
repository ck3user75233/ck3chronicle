# Lark as the existing raw workflow's lexer

Evaluation date: 2026-09-21. Owner accepts the stdlib scanner direction;
separator corrections below are recorded for implementation.

**Implementation follow-up:** the accepted stdlib approach is now implemented
in `ck3-lossless-v1.6`. Current rules and native validation are in
[LEARNER_SEPARATOR_FIX.md](LEARNER_SEPARATOR_FIX.md). The measurements below
describe the earlier evaluation policy and are not v1.6 performance results.

The evaluated replacement calls **Lark's basic lexer with `parser=None`**.
The evaluation concerns tokenization inside `lexical_pieces`.
The production control at evaluation time was `ck3-lossless-v1.5`, SHA-256
`fd48e9c51acf7e77dbcc3ecb42c8178cc07f58fdecefb84ed9dbeaae2fe8cc16`.
No production code, model, registry, or dependency declaration was changed
during that evaluation; the implementation follow-up above supersedes it.

Owner correction: evaluate only complete native error logs. Constructed inputs,
their assertions, saved outputs and probe-bearing research source snapshots
have been deleted. Conclusions supported only by those checks are withdrawn.
Questions and proposed work originating from those checks are deleted, not
deferred. They must not be carried forward as review items or requirements.
The native measurements below are retained; absent native cases remain unverified.

**Accepted direction: a scanner built with Python's stdlib `re`, using explicit
token rules and one scan.** This is not a ready-made filename-aware lexer.
Python's `tokenize` module targets Python source; `re` matches the patterns we
supply. [Python re](https://docs.python.org/3/library/re.html),
[Python tokenize](https://docs.python.org/3/library/tokenize.html).
The standard library does supply reusable character classifications:
`string.punctuation` for ASCII punctuation, `unicodedata.category` for Unicode
categories, and `re` character classes for whitespace, digits and word characters.
The current v1.5 lexer already uses the first two. Its problem is applying
punctuation separation mainly at string edges, rather than consistently emitting
the directed always-separators wherever they occur. Classification is useful,
but cannot itself mean split everywhere: ASCII punctuation includes @, underscore
and dot, which must remain within the relevant continuous symbols and filenames.
`shlex` also supplies configurable shell-style tokenization, but its shell quoting,
escaping and whitespace handling are not this log's lossless token contract.
[String constants](https://docs.python.org/3/library/string.html#string.punctuation),
[Unicode categories](https://docs.python.org/3/library/unicodedata.html#unicodedata.category),
[shlex](https://docs.python.org/3/library/shlex.html).
Lark works as a direct
lexer replacement, but the tested stdlib scanner produces identical boundaries,
takes about half the lexing time, and preserves the self-contained artifact
contract. Lark's main additional benefit here is its grammar/terminal API; it
does not remove the policy work or the byte adapter. I would not add a hybrid
or generated-code stage for this boundary.

**Comparison.** Lark is technically suitable. Both engines still need an explicit
CK3 lexical policy: adopting Lark cannot establish which characters belong in a
symbol, filename, or diagnostic formulation.

| Option | Practical benefit | Cost / limitation |
| --- | --- | --- |
| Lark replaces tokenization | Named terminals, explicit priorities, character positions; our adapter only produces existing pieces and byte spans | Adds a pinned runtime dependency; grammar and byte adapter remain our responsibility |
| Lark handles selected runs | Can retain a stdlib scanner for ordinary text | Two scanner paths and policy-consistency obligations; no observed correctness advantage |
| Corrected stdlib lexer | One ordered terminal table and one regex scan; keeps the existing self-contained parser artifact | We maintain terminal ordering, coverage checks, and byte-span construction |
| Generated Lark lexer | Runs without an installed Lark package | Generated artifact/build provenance, additional code, and different license notice; lexer initialization needs care |

All measured replacements used the same token rules. Both Lark and the stdlib
candidate match a designated separator as one character and emit it as its own
token during scanning. They preserve the punctuation and whitespace. The rules
also specify which characters stay within a continuous string. Lark terminal
priorities control which rule matches first.
[Lark grammar reference](https://lark-parser.readthedocs.io/en/stable/grammar.html)

**Token policy, including the latest owner corrections.** Counts are occurrences
in emission bodies across the fixed ten complete native logs, excluding headers.

| Characters | Native evidence | Proposed treatment |
| --- | --- | --- |
| `:` | 1,532,516 | Always one separator token, including inside scope expressions and filename/line presentations |
| `/` | 1,092,019 | Always separate except the exact approved `Div/0` atom |
| `\` | None in these bodies | Always separate under the owner requirement; not validated by this native corpus |
| `{ } [ ] ( )` | Respectively 30, 14, 218,456, 218,455, 431,325, 431,325 | Each character is a separate token; no balance requirement |
| `"` | 34,428 | Always separate; retain the quote itself |
| `=` | 57, including `host=[ROOT.GetUIName]` | Always separate |
| `< >` | None | No native finding or adoption decision raised by this evaluation |
| `;` | 157, including display-control text ending `L;` | Always separate, as directed by the owner |
| Pipe (U+007C) | 90, including mesh names | Always separate, as directed by the owner |

The previous table escaped pipes for Markdown rendering. Those formatting
backslashes were not native characters. If an actual backslash and pipe occur
together, each is a separate token, retaining its original character.

`@` can occur anywhere within a continuous symbol, including internally; it is
not a separator. Retain underscores, dotted names and filename extensions.
`!` is valid filename content beyond the leading position. Windows filename
rules do not restrict it to the beginning. The existing rule also retains it
internally, including before a filename extension; sentence-final punctuation
is a separate lexical use. [Windows filename rules](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file).
Preserve signed/decimal numbers; a sentence-ending dot is separate.
`tooltip/description` and `yes/no` remain words separated by `/`.
Folder names are not consulted.

The saved measurements below used the earlier experimental policy, which kept
internal pipes and semicolons. They are not validation of the newly directed
separator policy. Recheck complete native logs after implementing that policy.

**Inspectable native examples.** These are excerpts from actual emissions,
not invented training records. Complete bodies, source families, log hashes,
emission ordinals, and old/new byte spans are saved in the linked evidence.

| Source / native excerpt | Current pieces | Candidate pieces |
| --- | --- | --- |
| `localization_reader.cpp`: `(:)` | `"(:)"` | `"("`, `":"`, `")"` |
| `jomini_effect.cpp`: `launch_hungarian_migration_scripted_effect[args#3668957614])` | `"launch_hungarian_migration_scripted_effect[args#3668957614"`, `"])"` | `"launch_hungarian_migration_scripted_effect"`, `"["`, `"args#3668957614"`, `"]"`, `")"` |
| `pdx_data_localize.cpp`: `host=[ROOT.GetUIName` | One piece | `"host"`, `"="`, `"["`, `"ROOT.GetUIName"` |
| `pdx_data_factory.cpp`: `scope:ck3ia_jace_desmond` | One piece | `"scope"`, `":"`, `"ck3ia_jace_desmond"` |
| `jomini_script_system.cpp`: `'{'` | One punctuation run | `"'"`, `"{"`, `"'"` |
| `jomini_scriptvalue.h`: `[@cultural_maa_extra_ai_score` | `"["`, `"@cultural_maa_extra_ai_score"` | Same; this behavior is already correct in v1.5 |
| `dynasty_template.cpp`: `00_bgp_dynasties.txt:6` | Filename, colon, number | Same, now obtained from the general colon rule |
| `characterhistory.cpp`: `!!0_TFE_chars.txt` | One piece | Same |
| `jomini_scriptvalue.cpp`: `Div/0` | One piece | Same |

**Losslessness and validation.** Lark and the corrected stdlib scanner agree on
all **19,623,363 pieces** across ten complete native logs: **91,407,302 bytes,
343,585 emissions and 352,317 recovered messages**. Every emission reconstructs
exactly, including its unchanged header. Piece text, kinds and absolute byte
spans agree; the designated always-separators are individual tokens. Recovery
status, message ranges, shared ranges and emission framing remain unchanged.
There are 177,868 emissions with different token boundaries from current v1.5;
that is a boundary-change count, not a model-accuracy improvement.

The hybrid and generated variants also agree on three complete logs totaling
43,686,764 bytes, including the largest selected log (39,719,864 bytes).

Performance: two fresh-process repetitions per variant, reversed variant order
on the second round, on the same three complete logs totaling 43,686,764 bytes.
These are wall-clock lexing times, including creation of the same raw Piece/Span
objects. File reading, framing, initialization and validation are excluded from
the timed region. Peak memory is whole-process Windows peak working set,
including native bytes and emission framing, with pieces materialized one
emission at a time; it is not a lexer-only allocation measurement.

| Implementation | Lexing seconds, observed range | Peak working set, MiB |
| --- | ---: | ---: |
| Current v1.5 control | 19.49–20.62 | 169.2 |
| Corrected stdlib scanner | 14.81–18.41 | 169.2–169.9 |
| Lark lexer only | 33.22–33.63 | 172.3–172.7 |
| Lark for selected runs | 32.86–33.59 | 172.5–172.7 |
| Generated Lark lexer | 31.87–31.97 | 171.4–172.1 |

Mean initialization was 0.37 ms for the stdlib scanner, 41.69 ms for Lark,
44.88 ms for partial use, and 35.90 ms for generated code. Environment: Windows
11, Python 3.12.14, Lark 1.3.1. These local observations are not a cross-platform
performance guarantee. The control has different, coarser token output; the four
replacement variants have identical output on their equivalence corpus.

Lark text positions are character indexes, not UTF-8 byte offsets. The adapter
accumulates each token's `encode('utf-8', 'surrogateescape')` length from the
original absolute span. Whitespace is an explicit terminal; no `%ignore`, quote
removal, transformations, or reconstruct-from-tree operation is used. The native
corpus contains 343,585 CRLF endings, 802,803 additional LF endings and 433
non-ASCII characters. These results establish reconstruction for the observed
corpus, not unobserved encoding cases. [Lark API](https://lark-parser.readthedocs.io/en/stable/classes.html)

**Regressions and remaining limits.** A first experimental policy absorbed the
dot in `line: 2858.` and detached `_` from the native filename
`_default_28_shadow.dds`. These were policy defects shared by both backends,
not Lark failures. Removing the edge-stripping pass corrected them. The revised
candidate preserves the current LOCATOR ranges on all **7,827 distinct
source/message pairs** in the selected ten-log candidate.

The corrected separator policy needs a fresh native comparison of token text,
boundaries, exact reconstruction, timing and existing consumers.

**Dependency and version handling.** The owner installed Lark **1.3.1** for this
evaluation. Its default installation requires no other packages. A production
runtime adoption would need an exact dependency pin and an explicit version
check, with the grammar, adapter and required Lark version covered by the parser
artifact identity. Currently only a self-contained stdlib artifact is promised;
that contract must be updated openly if a runtime dependency is selected.

Standalone generation produced a 129,210-byte module and was exercised on
the three complete native logs described above.
The generated code uses MPL-2.0, whereas the Lark package uses MIT. Keep its
notice and generator provenance if choosing this route. The generated 1.3.1
object otherwise rebuilds its lexer on repeated `.lex()` calls; the experimental
wrapper constructs that lexer once using a generated-code internal method.
The regular lexer-only candidate uses the public `parser=None` configuration.
[Standalone generator](https://lark-parser.readthedocs.io/en/stable/tools.html),
[generator license notice](https://github.com/lark-parser/lark/blob/master/lark/tools/standalone.py),
[package license](https://github.com/lark-parser/lark/blob/1.3.1/LICENSE)

Any adopted boundary change needs a new parser revision/hash. Existing feature
cache keys already include the selected parser reference; rebuild features and
candidate models rather than mixing tokenizations. Parser/dependency provenance
belongs in run/build metadata, not every emission or diagnostic. The pipeline
continues to call `read_raw_log` with its model's selected parser reference.
No framing, message recovery, deduplication, SQL, or source-specific learning
architecture change is warranted by this evaluation.

**Implementation scope:** replace tokenization in `lexical_pieces` with the
stdlib scanner, incorporating the directed separator policy. Verify on complete
native logs, publish a new parser revision and invalidate affected feature
caches. Provide actual changed-boundary examples to the pipeline team.
No training or model promotion was performed in this evaluation.

The reproducible research entry point is
[`evaluate_raw_lexers.py`](../tools/template_learning/evaluate_raw_lexers.py).
Generated native evidence is intentionally outside Git under
`.codex-tmp/learner-refactor/lark-evaluation/lexer-only/`.
The key files are `RESULTS.json`, `selected-native-examples.json`,
`audit-handwritten-0/native-comparisons.json` (first 100 distinct changed bodies
in saved log order, not a random sample), `consumer-location-comparison.json`,
and `native-encoding-stats.json` in the parent evaluation directory. Piece arrays
are `[kind, exact text, absolute start byte, absolute end byte]`. The generated
lexer and grammar remain available. Native results retain their original source
hashes; the probe-bearing source snapshots were deleted at the owner's direction.
The current research entry point has had the probe harness removed. The fixed
input hashes are in the prior ten-log selection file.

After removal, the Lark audit was rerun on the complete 105,978-byte native log
with hash `85b96d996eff3d9479079f4f3341ecfd8eaa1e910c17b0dabadb1346b0f46a9b`:
576 emissions, 579 recovered messages, 20,548 pieces, exact reconstruction and
unchanged recovery. Results are in the parent directory's
`native-only-verification/`; no constructed inputs were run or saved.
