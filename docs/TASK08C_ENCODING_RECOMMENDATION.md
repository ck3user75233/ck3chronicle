# Task 08C — thin shared decoding API

**Status: implemented in development, with passing disposable-caller checks;
production integration and combined-release acceptance are pending.** This file
now describes the delivered API and agreed approach, not an unexecuted prompt.

Current owner direction, 2026-10-05. Use a known encoding when available and a
public detection library otherwise. This explicitly supersedes the earlier
fully automatic requirement and the incorrect all-candidates-must-agree rule.
The decoder remains unversioned and unpinned. Production callers stay unchanged
until the coordinated parser/learner/matcher upgrade. Experiments use disposable
caller copies; parser mechanics must not change without owner alignment.

Read commonly readable text independently of CK3's warnings about encoding.
In particular, a missing UTF-8 BOM is not grounds to reject readable UTF-8. The
owner's observations about CK3 parsing do not establish a complete engine encoding
specification. The specifically directed double-BOM stop below remains in force;
do not generalize it into rejecting all files with encoding/header warnings.

## Small shared boundary

**Pre-integration corrective, 2026-10-05:** physical files and internal parser
fragments now have explicit separate entry points. Do not copy the earlier
`Decoder(encoding='utf-8').decode(span)` parser substitution.

`ck3chronicle.decoder.decode(raw, encoding=None)` and `read(path, encoding=None)`
decode **complete physical source files**, including header inspection/admission.
`decode_fragment(raw: bytes) -> str` is the parser path: exactly Python UTF-8 with
surrogateescape, without header inspection, BOM consumption, detector use or
normalization. Even BOM bytes at the start of a span remain content. Its text
round-trips with `text.encode('utf-8', 'surrogateescape') == raw`.
`Decoder(encoding=None)` is a small optional physical-file convenience object.
There are no caller-name policies, source/log/snippet
APIs, path-based encoding overrides, detector voting, release metadata or decoder
cache. SourceSearch owns its request cache and file-change checks.

The shared layer retains only codec selection, the existing header validation,
byte-preservation warnings, and consistent display/newline views. Callers continue
to own file scope, parsing, searching and reporting.

```python
from ck3chronicle.decoder import decode_fragment, read

# A parser-internal span, with no physical-file header semantics:
processing_text = decode_fragment(raw_span)
# Unknown source encoding:
source_input = read(source_path)
```

The physical-file operations return `DecodedText`: original bytes, processing text or failure, selected
encoding, method, reason, warnings, header findings and newline information.
`text` retains native newlines and any byte-preserving surrogate escapes.
`display_text` renders those escapes as visible byte notation such as `\xC3`.
`working_text` additionally normalizes physical CRLF/CR to LF for search/snippets.
Display text is not fed back into parsing or used to reconstruct original bytes.
The fragment operation returns a plain str, with no file-admission metadata.

`DecodedText.bom_bytes` is the number of leading physical BOM bytes omitted from
the returned processing text, whether skipped by automatic BOM selection or
consumed by an explicit codec. On genuine UTF-8 BOM bytes: automatic decoding and
explicit utf-8-sig report 3; explicit utf-8 reports 0 and preserves U+FEFF. With
no BOM, or no returned text, it is 0. Generic utf-16/utf-32 codecs report the actual
signature length when they consume it; explicit endian codecs that preserve it
report 0. This is not a character/byte-offset map. The existing verification
consumers use it as the omitted-prefix length; no production consumer was found.

## Library behavior

For a known encoding, use the standard codec with `errors="surrogateescape"`.
This is the existing parser's behavior: isolated undecodable bytes survive without
changing surrounding Unicode text or original byte positions. Some codecs still
cannot recover particular errors; those remain explicit decoding failures.
Explicit codecs retain their standard BOM semantics: utf-8 preserves a BOM,
utf-8-sig consumes it. Conflicting encoding/signature choices fail.

For unknown encoding, recognize Unicode BOMs first, then try strict UTF-8 when
there are no NUL bytes. Only remaining input needs chardet. Use its top result,
requiring confidence above its published `MINIMUM_THRESHOLD` (0.20), then strictly
decode the entire file. Chardet may return low-confidence fallback guesses; these
are not accepted. No custom detector, candidate-unanimity requirement or numerical
accuracy claim is added. The threshold is a library heuristic, not a guarantee of
correct author intent. Successful inferred readings have an explicit warning.

Double BOM remains a failed read before text is supplied; no header repair is
implemented. Existing critical header findings remain visible. A failed read
supplies no processing text and cannot become a negative content-search match.

## Why the known-encoding route matters

The genuine session-55 log is processable and already has successful stored
processing. Python UTF-8/surrogateescape reproduces its processing text and all
original bytes, including 44 isolated byte anomalies in Invalid character
messages. Display can show `Invalid character '\xC3' in key name 'Agmánd'` while
keeping the original byte internally. This is readable evidence, not a reason to
reject the log.

Neither detector reliably infers this whole log: installed chardet recommends
ISO-8859-14 at about 0.091 confidence; charset-normalizer prefers HP Roman-8.
Guessing again for each parser fragment also produces wrong results. Therefore
known UTF-8 must remain known when replacing the parser's embedded decoder calls.
The fragment API now directly embodies that known UTF-8 contract, without
subjecting arbitrary parser spans to physical-file admission.

## Staging and verification

The corrected disposable parser changes only its two decoding expressions to
decode_fragment, plus a test invocation counter. It retains its own candidate digest. Emission framing,
recovery, tokenization and byte-offset calculations are unchanged. Checks compare
actual parser outputs and native matcher inputs, excluding only candidate parser
identity metadata. They do not claim database-ingestion or release acceptance.

Disposable source search and excerpts share cached DecodedText results. Ripgrep
searches temporary UTF-8 copies of working_text with `--encoding none`; it does
not select another interpretation. Preserved-byte display is identical in search
and excerpts. Production source-search and presentation code are unchanged.

The uniform random mod-only sample remains 942 of 18,837 files (5.0008%), excluding
all official game/DLC members. 941 have unchanged readable UTF-8 text; the remaining
k_sweden.txt is undetermined because chardet's confidence is about 0.032. Explicit
Windows-1252 reading works consistently, but its original codec is unconfirmed.

Current receipts under `.codex-tmp/task08c/decoder/`:

- `parser-substitution-corrected/`: corrected fragment-safe parser, diff and renewed four-log comparison.
- `pre-integration-corrective/checks.json`: genuine byte round trips, explicit BOM metadata, unchanged automatic source results and boundary inspection.
- `pre-integration-corrective/delivery-hashes.json`: exact corrected delivery/evidence hashes, not a release pin.
- `library-behavior-review.json`: actual detector results and standard-codec round trips.
- `parser-substitution-simplified/`: historical reviewed candidate; its physical-file decoder calls are superseded. Retained for input identities/provenance only.
- `simplified-verification/verification.json`: random source text/search/excerpt and stored-query comparisons.
- `simplified-display-search/results.json`: all 44 Invalid character messages searchable and displayable, with exact processing-byte recovery.

Double-BOM/header anomaly positive cases, UTF-16/32 and East Asian examples are
not represented in this genuine sample; no passing acceptance claim is made for
those branches. The absence of fragment header admission is established by
inspection of its direct standard-codec call; no synthetic double-BOM example
is presented as genuine evidence. Broader Task 08C scope/filter/beta work is separate.

## Dependencies

The owner-installed chardet 7.6.0 provides fallback detection. The disposable
packaging proposal is `chardet>=7.6,<8`; production pyproject is unchanged.
charset-normalizer remains research evidence, not a second runtime detector.
Python's standard library provides all codecs and byte-preserving error handling.

References: [Python codecs](https://docs.python.org/3/library/codecs.html#error-handlers),
[chardet usage](https://chardet.readthedocs.io/en/latest/usage.html). Installed source
was checked: detect_all can return an unfiltered fallback when every candidate is
below its minimum, so accepting that list blindly would not establish confidence.
