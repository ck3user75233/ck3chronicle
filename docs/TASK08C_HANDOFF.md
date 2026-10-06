# Task 08C — receiving and encoding decision checkpoint

## Pre-integration corrective complete — 2026-10-05

**READY FOR LEARNER INTEGRATION.** This bounded receiving repair is separate from
remaining 08C work and from combined-release integration. No production parser,
selection, service, database, release or dependency declaration was changed.

The earlier disposable substitution sent arbitrary parser spans to physical-file
header admission. It is superseded: use `decode_fragment(raw: bytes) -> str`, a
direct UTF-8/surrogateescape decode with no header inspection, BOM consumption,
detector import, normalization or substitution. Original BOM characters and
undecodable bytes remain content. `decode`/`read`/`Decoder` retain physical-source
header admission and the double-BOM stop. Parser framing/recovery/offset/token
mechanics are unchanged; only the two disposable decoding sites were replaced.

`bom_bytes` now means the leading physical BOM bytes omitted from returned text,
including bytes consumed by explicit Unicode codecs. On a UTF-8 BOM source,
automatic/utf-8-sig = 3; plain utf-8 = 0, with the BOM retained. No BOM or no
returned text = 0. Explicit endian codecs preserve their native semantics;
generic utf-16/utf-32 account for the actual consumed signature length. Existing
uses in tools/check_shared_decoder.py are omitted-prefix comparisons; no production
consumer was found. This is not a byte/character-offset map.

Focused checks, all passing:

- Four supplied logs, original SHA-256s verified: exact fragment round trips,
  with no detector imported. Session 55 retains all 44 isolated undecodable bytes.
- Actual corrected disposable parser: 186,704 emissions and 190,701 native matcher
  inputs agree with the pinned baseline; all framing, body/decoded text, token
  spans, local/cross-emission recovery and native reconstruction compare equal.
- 884 genuine BOM-bearing source files reproduce the old explicit utf-8-sig
  metadata defect and verify 0 -> 3 with unchanged text. Plain utf-8 reports 0;
  the fragment function preserves the genuine leading BOM bytes exactly.
- All 942 frozen mod-source automatic text/metadata results equal the reviewed
  receipt; 941 readable, one undetermined. This reuses the sample, not a new draw.
  Source-search caller bytes remain unchanged, so prior search/query receipts are
  reused rather than rerunning pipeline/database work.
- Header inspector source is unchanged. Fragment call-graph inspection confirms
  no header/detection/normalization calls. Runtime logging ownership check passes.

Current evidence: `.codex-tmp/task08c/decoder/pre-integration-corrective/checks.json`
and `parser-substitution-corrected/results.json` under the same decoder evidence
root. Both record original full paths/hashes. The supplied session-55 log hash is
`cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740`.
The supplied `parser-substitution-simplified` directory is preserved as historical
review/input provenance; its physical-file adapter must not be copied.

Exact corrected files: src/ck3chronicle/decoder.py;
tools/check_decoder_corrective.py; .codex-tmp/task08c/decoder/check_disposable_parser.py;
the generated parser-substitution-corrected/parser_candidate.py and parser.diff;
docs/TASK08C_ENCODING_RECOMMENDATION.md; this handoff; and
docs/learner-next-release/HANDOFF.md. Generated receipts and the before-image are
ignored evidence, not product artifacts. The complete delivery/evidence hash list
is `.codex-tmp/task08c/decoder/pre-integration-corrective/delivery-hashes.json`.
Decoder SHA-256: `c31c8d6089850fb01d146b420e1c7364d86cb9287180f2e9f451861c21feb039`.
Candidate parser SHA-256: `de55531bcdaa66ce7bdfbee06d489cfe45161b45c2ca9418b7bb9863493583f4`.
These hashes identify the delivery; they do not create a decoder version or pin.

Limits: no genuine internal double-BOM fragment or physical double-BOM positive
case was supplied; the boundary is verified by inspection, not fabricated CK3
evidence. Generic UTF-16/32 consumption has no genuine positive example here.
Those do not block the known-UTF-8 corrective. Detector coverage, distribution
closure, continuation callers, combined classification, pipeline integration and
activation remain with their existing tasks and were not undertaken.

**Learner-team hookup:** the delivered instructions are in the combined release
[HANDOFF.md](learner-next-release/HANDOFF.md#decoder-delivery-exact-hookup-instructions--2026-10-05).
It gives the exact two decoding replacements, result/failure handling, dependency
and isolation boundary, evidence and reproduction commands. Decoder delivery is
complete; receiving review, combined-package verification and activation remain
with the learner/release team.

## Simplification complete in development; disposable checks pass — 2026-10-05

The owner explicitly selected "Use the known encoding when available; detect
otherwise". This supersedes the earlier mandatory automatic selection and
candidate-unanimity requirements. The shared API exposes decode/read functions
and a small optional Decoder convenience object. Standard Python codecs perform
all conversion; known encodings use surrogateescape. Unknown encodings use Unicode
signatures/strict UTF-8, then one chardet recommendation above the library's own
minimum threshold, followed by full-input strict decoding. Low-confidence guesses
remain failed reads. No custom detector or confidence-accuracy claim is introduced.

Removed: candidate-text voting, directory override routing, decoder-owned cache.
The disposable source caller retains its own snapshot/change checks. Processing
text and bytes stay exact; display_text renders byte escapes as \\xHH and
working_text adds newline normalization. Double BOMs still stop content reading;
header repair remains excluded. Production dependencies and callers are unchanged;
the disposable dependency proposal now uses chardet>=7.6,<8.

The actual disposable parser calls this API with its existing known UTF-8 codec.
All four genuine logs PASS, including session 55: 186,704 emissions and 190,701
native matcher inputs compare exactly, excluding only the candidate parser digest.
Framing, text, token spans, local/cross-emission recovery and byte reconstruction
match. Session 55 alone compares 100,000 emissions and 100,003 native units.
There are no parser-mechanics edits, production artifact changes, new Run writes
or package publication. Matching/classification downstream was not rerun.

Source validation uses the existing 942/18,837 uniform random mod-only sample:
941 exact readable text/excerpt comparisons, four equal search result sets
(260/32/104/267 matching files), one low-confidence undetermined source whose
content is not searched. Genuine stored-query parity remains 64 occurrences and
two distinct records. Separate actual-log search finds all 44 Invalid character
messages, matches snippet text, emits valid UTF-8 display and proves exact original
bytes through the processing text. Runtime logging ownership passed.

Current evidence under `.codex-tmp/task08c/decoder/`:
`parser-substitution-simplified/results.json` with candidate/diff,
`simplified-verification/verification.json`,
`simplified-display-search/results.json`, and `library-behavior-review.json`.
The one-off parser runner is `check_disposable_parser.py` in that directory;
source/public comparisons remain in tools/check_shared_decoder.py. Full design:
TASK08C_ENCODING_RECOMMENDATION.md. Double-BOM/header positive cases and absent
encoding families remain unverified against genuine evidence. All earlier failure
receipts are retained as historical evidence, not current acceptance results.

## Actual disposable parser substitution tested — 2026-10-04

Owner clarified that staged integration must be exercised in a disposable parser
copy now, not deferred until release. The one-off experiment under
`.codex-tmp/task08c/decoder/parser-substitution/` replaces the two embedded
UTF-8/surrogateescape decoding expressions with the shared Decoder API. The only
other addition is a small call/failure wrapper and invocation counter. Exact
reverse reconstruction verifies no parsing-mechanics changes. The candidate has
its own parser-reference digest; production package files and selection hashes
are verified unchanged. No package was published and no database was ingested.

The three previously compared genuine logs now run through the actual modified
parser: all 86,704 emissions and 90,698 native matcher inputs match the baseline,
including framing, decoded text, token spans, local/cross-emission recovery and
original-byte reconstruction. Candidate parser-reference metadata is the sole
excluded field in matcher-input comparison; downstream matching/classification
was not rerun. The fourth log, legacy session 55, frames all 100,000 emissions and
reconstructs its bytes exactly, but fails on reading emission ordinal 1617, line
1618: the first Invalid character message produces 12 detector interpretations
for that fragment and is rejected. Only 1,617 preceding emissions completed the
text/token/local-recovery comparisons; downstream recovery/unit comparisons for
this file did not run. Overall result is FAILED, exit code 1. This is an actual
decoder substitution regression; correcting the decoder remains outstanding.

Reproduce with `.venv/Scripts/python.exe -B
.codex-tmp/task08c/decoder/check_disposable_parser.py`. The directory contains
`parser_candidate.py`, `parser.diff`, and `results.json`. This four-log exercise
does not establish whole-corpus or release acceptance. Earlier statements that
only standalone decoder/native-parser text comparisons exist are superseded.

**Current acceptance correction:** rejecting the successfully processed legacy
session 55 log is a decoder regression. The comparison tool now fails on this
difference. See "Owner correction: readable processing, not codec unanimity"
below; earlier passing-check language does not establish parser compatibility.

2026-10-04. **Task is in progress, not fully delivered.** Shared automatic decoding
and critical header warnings are implemented. Broader playset-scope/beta work and
the coordinated parser/learner/matcher upgrade remain separate. Earlier requests
for an encoding choice below are superseded by the owner's direction here.

## Double BOM stops content reading — 2026-10-04

Owner clarified that CK3's token-error cascade from attempting to process a double
BOM must not be reproduced by this tool. The development decoder now returns
`invalid_header`, no decoded text and one failed file-read reason when its header
inspector detects a double BOM. The critical finding and original bytes remain
available. The failure occurs before full content decoding and before any return
of text to search or parsing; an encoding override cannot bypass it. No header
repair is attempted.

The disposable source candidate already excludes every failed decoder result
from ripgrep and marks excerpts unavailable. File discovery/resolution remains
independent, and a failed content read cannot become a negative content match.
Future parser call replacement must honor the same failed-read result without
entering parser mechanics. Production callers, pinned artifacts and dependencies
are unchanged. Genuine double-BOM positive evidence remains absent; no fabricated
fixtures were created. The existing genuine sample and real ambiguous-file
failure path provide regression evidence, not positive double-BOM acceptance.

## Cutover deferred; confidence and scope corrected — 2026-10-04

**Current authority, superseding earlier delivery descriptions below:** the owner
requires caller cutover only with a new coordinated pinned parser/learner/matcher
release. Development comparisons must use disposable copies. The shared decoder
itself remains unpinned. No changes to parser internals are authorized.

Correction performed: preserved the candidate source-search/presentation files
and dependency proposal in ignored `.codex-tmp/task08c/decoder/candidate/`.
Restored `reporting/source_search.py` byte-for-byte from the pre-decoder snapshot
(after checking the whole intervening diff contained only this decoder work).
Removed only this work's decoding-warning additions from `presentation.py`, and
restored the original dependency declaration in `pyproject.toml`. Parallel work
in those files and elsewhere was preserved. No service restart or pinned release
change occurred. The development `decoder.py` remains in the repo with no
production imports/callers; integration experiments are disposable only.

The owner also clarified that an inconclusive/ambiguous guess must not be
presented as readable content. Development API now uses strict Unicode first,
then charset-normalizer with last-resort fallback disabled. Candidate codecs
must decode the entire input and produce one identical text; different texts
return `ambiguous` with a reason and no selected text. No candidate returns
`undetermined`. A successful result must also encode as valid UTF-8 for rendering.
Optional explicit codecs remain instructions from the caller, not automatic
confidence. Single-result heuristic detection is disclosed and never described
as proof of the original author's intended characters.

Header repair is not requested. Double BOM/mojibake and related findings retain
critical warnings without repair, where the content is otherwise readable.
Original bytes remain intact. This replaces the temporary best-guess-plus-warning
policy described in older checkpoints; the real ambiguous Swedish mod file and
malformed-byte log now fail automatic decoding explicitly rather than returning
cp1250/HP Roman-8 guesses.

The comparison tool now requires `--candidate-source` as well as the saved
baseline source; it loads disposable modules without changing production callers.
Current command adds:

```powershell
--candidate-source .codex-tmp/task08c/decoder/candidate/source_search.py
```

Current receipts are under `decoder/staged-verification/`; older receipts remain
historical and must not be read as current activation evidence. Parser decoding
replacement is still pending; the source-reference rebinding prototype was
removed, not transferred to a production parser. The report-export defect
identified in the next section remains a separate unimplemented correction.

## Parser integration boundary clarified — 2026-10-04

Owner expects replacement of the parser's embedded decoding calls with the
shared decoder API, upstream of parsing. No changes to framing, recovery,
tokenization, offsets or parser result structure are authorized without prior
alignment. The opt-in `decoder_integration.py` prototype rebound source references
in parsed results; it has been removed, along with `DecodedText.text_at_bytes`.
No pinned parser artifact or parsing algorithm was edited during this work.
The unrelated dirty `pipeline/contracts.py` is parallel work and was untouched.

`tools/check_shared_decoder.py` now compares automatic decoder text with the
unchanged parser's native text. It does not inject objects or change parse results.
Actual decoder-call integration is pending the coordinated upgrade. The earlier
adapter comparison receipts below remain historical evidence of that removed
prototype, not a current delivered hookup. Source search/excerpt integration
through `Decoder` remains implemented. The malformed-byte interpretation and
separate report-export defect remain relevant findings.

## Invalid-character log follow-up — 2026-10-04

Owner asked whether the malformed character caused current processing failures.
A focused check found 44 invalid single-byte sequences (C3/C5), each in CK3's
`localization_reader.cpp:445` `Invalid character` diagnostic. The complete key
names contain valid UTF-8; the quoted offending byte is incomplete by itself.
All 44 emissions recover, classify as template matches, bind their original
capture byte ranges and prepare contract records successfully with the selected
package. All 44 native emissions round-trip exactly; storage's ASCII-escaped JSON
serialization round-trips through strict UTF-8 without errors. No new ingestion
or production write was performed.

A separate **report export defect** was reproduced at the output boundary using
one of those genuine recovered messages. The current JSON (`ensure_ascii=False`),
HTML and plain-text rendering paths retain the internal U+DCC3 byte-preservation
marker. Strict UTF-8 encoding then raises `UnicodeEncodeError: surrogates not
allowed`. This is a rendering/serialization defect, not parser failure or evidence
loss. The selected log is absent from the existing disposable Run database, so
this is an actual-message output-boundary check, not a full stored-Run CLI export.
Recommended correction: escape preserved undecodable bytes visibly in display
text and use safe JSON escaping, leaving stored values and original bytes intact.
No rendering repair was made during this question-only investigation.

Evidence: ignored `decoder/invalid-character-processing.json` and
`decoder/invalid-character-display-check.json` beneath `.codex-tmp/task08c/`.

## Shared automatic decoder and staged parser comparison — 2026-10-04

Owner direction: build one reusable decoder/API, without separate versioning or
pinning. Do not require callers to select source/log/snippet-specific functions
or policy profiles. Read what the library can read; warn about inferred/ambiguous
interpretations rather than making ambiguity an override gate. Keep the full
pinned-package/ingestion switch for the coordinated upgrade already in progress.

Delivered:

- `src/ck3chronicle/decoder.py`: `Decoder().decode(bytes)` / `.read(path)` return
  `DecodedText` with original bytes, text, codec/method, warnings, alternatives,
  BOM and original newline metadata. Unicode fast paths precede the detector's
  default best-effort behavior. Overrides are optional. No decoder release,
  manifest, version field, package pin or database-lineage addition.
- `SourceSearch(decoder=...)` defaults to that same automatic reader. Retired the
  separate `_encoding` probe, excerpt-side decoding and ripgrep auto-decoding.
  Search/excerpts share captured text and an LF working view; rg receives strict
  UTF-8 temporary inputs with `--encoding none`. Snapshots are in memory until
  clear/new investigation, with observed-change errors instead of mixed reads.
- The same decoder owns the existing bounded header inspector. Inferred/ambiguous
  encodings are ordinary warnings in query results and HTML/text coverage and
  candidate details; critical header anomalies retain their previous labels.
- `src/ck3chronicle/decoder_integration.py`: opt-in `parse_file(path,
  parse_bytes=selected_parser.parse_bytes)` automatically decodes the file and
  attaches an original-byte source to the unchanged parser result. It supplies
  decoder-backed span reads during recovery/lexing. It does not choose a log
  profile, mutate the parser module, or change its version/hash. Frozen embedded
  header-field decoding remains for the planned package upgrade.
- Normal dependency `charset-normalizer>=3.5,<4`; installed 3.5.2 exercised.
  Read-only inspection CLI: `python -m ck3chronicle.decoder PATH`.

Verification on genuine inputs, with no generated fixtures or mock clients:

- Frozen uniform mod-only sample: all 942 source hashes unchanged; 941 Unicode
  texts equal their former decoding. The remaining real `k_sweden.txt` now reads
  automatically as the library's best usable cp1250 result, with inferred and
  ambiguous warnings (eight distinct interpretations). This is not ground truth.
  Optional cp1252 interpretation separately verified, including non-ASCII search
  and excerpt agreement.
- Four actual rg comparisons across all 941 formerly readable files: identical
  matches and displayed lines (260, 32, 104 and 267 matching files respectively).
  First-line excerpts agree for all 941; matched-line excerpts agree; genuine
  adjacent-line literals expressed as LF/CRLF give the same results. Normal
  temporary transport cleanup verified. No universal performance claim.
- Public `SourceSearch` plus `DiagnosticAnalysis` on genuine stored Run
  `20261003-74G2EB`, through the handler on the existing disposable database:
  two file associations and unchanged 64 occurrences / two distinct diagnostics.
  Inferred/ambiguous warning coverage rendered in JSON, HTML and text from the
  genuine mod selection. Root CLI JSON/HTML/text reports exported successfully.
- Three genuine UTF-8 logs (451,160 / 4,603,120 / 11,613,432 bytes): 86,704
  emissions and 90,698 matcher input units. Original bytes, framing, recovery,
  lexical pieces/offsets and complete matcher inputs agree with the selected
  package. No decoder hints/profiles supplied.
- Existing five genuine replacement-character header cases still pass the public
  validation API, critical labels and original byte-offset checks.
- Isolated imports, runtime logging ownership and `pip check` pass.

**Concrete integration mismatch, not a passing ingestion acceptance:** an
unchanged genuine 7,972,048-byte log has invalid UTF-8 at byte 347,993: CK3 emitted
an isolated C3 byte in an `Invalid character` message while other nearby text
contains valid UTF-8. The detector selects HP Roman-8 with 35 distinct candidate
texts. The original parser preserves the bytes; the staged hookup reports that
its detected codec is outside the current parser's UTF-8 byte-framing contract.
This must be addressed before activating automatic decoder-backed ingestion.
It is not solved by retaining raw bytes alone. No live ingestion was switched.

A fresh check of 74 historical distinct-log paths found 59 unchanged strict UTF-8
logs, that one unchanged non-UTF-8 log, 13 now-missing paths and one changed live
log. Missing/changed files were excluded, not represented as passing evidence.
Mixed CRLF/LF occurs in the malformed-byte log. UTF-16/32, East Asian sources,
lone-CR input, double/conflicting/displaced BOM and BOM-mojibake positives remain
unrepresented; no synthetic cases were created to fill these gaps.

Reusable comparison: `tools/check_shared_decoder.py`. Evidence under ignored
`.codex-tmp/task08c/decoder/`: `verification/verification.json`,
`verification/sample-decoding.json`, `log-encoding-inventory.json`,
`warning-coverage.{json,html,txt}`, and `report.{json,html,txt}`. The saved
`source_search_before.py` is the pre-change comparison implementation, not a
runtime fallback. The command is:

```powershell
.\.venv\Scripts\python.exe -B tools/check_shared_decoder.py `
  --sample-survey .codex-tmp/task08c/random-mod-survey.json `
  --baseline-source .codex-tmp/task08c/decoder/source_search_before.py `
  --logs-manifest .codex-tmp/continuation-survey/inputs.json `
  --database .codex-tmp/task08c/genuine.sqlite3 --run 20261003-74G2EB `
  --output .codex-tmp/task08c/decoder/verification
```

Failed/interrupted development checks disclosed: two early comparisons were
interrupted to receive the owner's API/policy corrections. One retry's cleanup
assertion encountered their leftover scratch directory; a scoped PowerShell
cleanup was rejected as blocked by policy, so it remains ignored at
`decoder/ck3-source-nzyedmdx`. Verification moved to a fresh directory and normal
cleanup passes there. A harness call omitted required `package_id`; corrected
before the complete passing run. A warning-render probe initially searched for
an absent literal; corrected to a literal actually present in that genuine file.
These are not product successes or new requirements. No production state,
pinned artifacts, catalogs or release selections changed; no commit/push.

Design/API details: [shared decoder recommendation](TASK08C_ENCODING_RECOMMENDATION.md).


## Delivered critical encoding-header warnings — 2026-10-04

Owner explicitly requested warnings such as `Resolved / Critical Encoding issues
(mojibake, double BOM)` and the standalone critical label. Implemented in the
existing source/analysis/presentation owners:

- `source_search.inspect_source_header` is a module-level byte inspector;
  the session's candidate validation enforces
  recorded-member membership/resolved containment before a read. Checks cover
  the first 4,096 bytes: double BOM, displaced/conflicting signatures, three known
  BOM-mojibake re-encoding forms, literal U+FFFD and BOM/byte mismatch. No detector
  choice or source repair is made; unmarked non-UTF-8 headers are undetermined.
- `SourceSearch.validate_sources(selection, run_id=...)` validates all matching
  files through existing search methods. `validate_details` attaches the same
  results after report ranking/display limits. Cache keys include file-change
  metadata and caches clear for a new investigation. No-path records cause no
  header read; unavailable/uninspected coverage is distinct from checked headers.
- `encoding_validation` contains critical severity, issue code/label, byte offset,
  affected file/member, bounded scope and readable header evidence. Per-reference
  warnings preserve `status: resolved`; they do not alter stored counts or the
  last-load-order source decision. Source rows get an Encoding validation column;
  resolution rows combine the owner's labels when warnings exist. Text and HTML
  use the same renderer; JSON retains the structured warnings. No whole-file
  encoding certificate or general mojibake detector is claimed.

Genuine verification:

- Inspected all 18,837 paths in the previously enumerated mod-only text population,
  at most the first 4 KiB each. 18,821 had no targeted pattern; 11 were undetermined;
  five had 45 literal U+FFFD occurrences. No I/O errors. No double-BOM or BOM-mojibake
  positive appeared in that inspected region. Full scan receipt is
  `.codex-tmp/task08c/source-header-validation-scan.json` (187.970 seconds).
- The public source-validation API, with playset provenance read through
  `HandlerClient` on disposable genuine storage, returned all five critical files.
  Independently checked each byte offset against original UTF-8 `EF BF BD` bytes
  and checked the standalone critical label. Receipt:
  `source-validation-verification.json`; full results: `source-validation-positive.json`.
  No selected-Run stored diagnostic referenced those five paths, so a positive
  combined Resolved/Critical report row remains code-inspected rather than claimed
  as a genuine rendered example. No synthetic diagnostic was manufactured.
- Genuine root CLI exports for `common/on_action/sea_minority_on_actions.txt`
  passed JSON/text/HTML: 64 occurrences, two diagnostics, two physical files with
  checked headers. A limit-zero export preserved totals and requested no header
  validation. Chrome desktop/narrow checks passed; both screenshots were inspected.
  Evidence: `header-report.*`, `header-report-zero-detail.json`, `browser/`.
- Imports and the required runtime logging ownership check passed. These warnings
  are source result data; no separate logger configuration was introduced.

Failed/limited attempts: the first all-mod scan used a slow byte-at-a-time signature
loop and was interrupted; replaced with byte-string searches and reran the full
scan successfully. A process diagnostic using `Get-CimInstance` was denied by the
environment; it was not needed for validation. Neither is a passing product check.
No fabricated files, injected failures, service restarts, production writes,
commits or pushes. The disposable verification handler was shut down afterwards.

Remaining 08C work includes the proposed shared decoder, broader enumeration and
exclusion policy, existing whole-history candidate enrichment correction and beta
report. New header reads are bounded to displayed detail; this does not claim the
pre-existing candidate lookup/excerpt work has already been bounded.

## Header-anomaly follow-up — 2026-10-04

Owner asked about duplicate BOMs and mojibake before a BOM. The recommendation
now specifies consuming only one initial signature; preserving/reporting extra
U+FEFF, suspected literal BOM mojibake, displaced/conflicting signature sequences
and literal replacement characters. Readable anomalous text remains searchable;
undecodable text retains honest coverage. No automatic header stripping/repair
or inference that CK3 rejects the file. Escaped header display is separate from
literal search text. Unicode/W3C primary references are linked there.

Inspected first 256 bytes/decoded characters of the unchanged 942-file sample.
No targeted anomaly was found; this does not rule out other forms or unsampled
files. Ignored `header-survey.json` / `inspect_sample_headers.py` record exact
scope and observations. No fabricated header tests or runtime implementation.

## Concrete encoding design recommendation — 2026-10-04

Owner requested a complete recommended design rather than another decision menu.
Rewrote `TASK08C_ENCODING_RECOMMENDATION.md` around one proposed implementation:
strict Unicode first; charset-normalizer as the sole fallback candidate provider;
explicit ambiguity and scoped overrides; one decoded working text shared by
search and excerpts. It now specifies CRLF/LF/CR normalization only in temporary
working text and source-content query literals, preserving original newline
metadata and leaving source files untouched. It also addresses unmarked NUL-bearing
input, which cannot safely be identified as UTF-8 solely because byte decoding
succeeds. These are recommendations, not implemented or newly verified cases.

The original research narrative is preserved outside Git at
`.codex-tmp/task08c/encoding-recommendation-research-history.md`; the frozen sample
and detector receipts are unchanged. The dependency comparison explicitly credits
chardet's better stand-alone result while explaining the proposed narrower
charset-normalizer role. Owner direction on implementation remains pending.

## Installed detectors evaluated — 2026-10-04

Owner completed venv installation. Verified charset-normalizer 3.5.2 and chardet
7.6.0; `pip check` passed. Evaluated both on the frozen random 942-file mod sample.
All source hashes were unchanged; no read errors or observed changes during
reading. The original survey and draw remain intact.

Chardet's preferred result agrees with all 941 strict Unicode decodings.
Charset-normalizer with proposed fallback guesses disabled agrees with 933;
seven return no result and one prefers a legacy codec despite a valid UTF-8 BOM.
A follow-up on exceptional cases shows default fallback restores those seven
UTF-8 results, but not the eighth. Unicode-first decoding bypasses all eight.
Observed total detector-call times: 1.295 s versus 0.584 s, respectively; these
are one-pass measurements, not a general performance claim.

The single non-UTF-8 file yields eight distinct charset-normalizer interpretations
headed by CP1250, whereas chardet gives Windows-1252 at confidence 0.03233.
Two interpretations produce visibly different Swedish-name comments on eight
lines. No originating-codec ground truth is established. Recommendation remains
strict Unicode first, then explicit ambiguity/override handling; automatic policy
still requires owner direction. The sample is not proof of legacy-encoding
accuracy or universal support. Library selection rationale and evidence are in
`TASK08C_ENCODING_RECOMMENDATION.md`.

Ignored evidence: `compare_detectors.py`, `detector-comparison.json`,
`detector-followup.json` under `.codex-tmp/task08c/`. Product dependencies,
encoding implementation, runtime services and production state were not changed.

## Owner correction — random mod-only encoding research

The owner rejected the small non-random sample as a representative basis and
directed a 5% uniform random sample excluding CK3 game/DLC files. That research
is complete: 942 unique `.txt`/`.yml` paths drawn without replacement from 18,837
eligible files in 105 recorded mod members (5.0008%); all 28 official members
excluded. No relative-path, member, size or language quotas. Population, OS-random
seed and sample were frozen before reading contents. 75 mod members appear in
the draw; no duplicate sample paths, missing reads, inventory issues or observed
changes during reading.

941 files strictly decode as UTF-8 (884 BOM / 57 unmarked); one unmarked file in
member 114 does not. Line endings: 580 CRLF, 359 LF, three without line breaks;
no lone CR/mixed cases observed. One CRLF result uses raw-byte counts because
encoding remains unresolved. Full details and limits are in the recommendation.
The earlier survey below is historical, superseded for representative sampling.

Ignored files: `random_mod_survey.py`, `random-mod-sample-manifest.json` and
`random-mod-survey.json` under `.codex-tmp/task08c/`. No synthetic fixtures.
The owner requested explicit venv installation instructions; absolute-path
PowerShell commands for `charset-normalizer` and `chardet`, followed by `pip check`,
were supplied. Neither library was present during that initial survey; the
installed-detector evaluation above now completes this follow-up. A blocked
download was not treated as a completed detector investigation. Product encoding
policy remains awaiting direction.

## Completed work

- Read the supplied Task 08C brief, repository instructions, current
  plan/status/handoff openings, development environment, 08B and 08A.2 handoffs,
  reporting decisions and owning query/source/analysis/preset/presentation/CLI
  code. The current 08B handoff is the received correction baseline; older open
  lists are historical. Existing unrelated dirty work remains intact.
- Prepared [encoding recommendation](TASK08C_ENCODING_RECOMMENDATION.md), with
  primary library/ripgrep references, genuine source-file observations, explicit
  uncertainty treatment, dependency limits and a concrete shared-text transport
  to the existing search backend. **Not owner-approved or implemented.**
- Surveyed 949 unchanged `.txt`/`.yml` files, 91,683,459 bytes, across 117 of 133
  recorded members in 35.415 seconds. 947 strictly decode as UTF-8; two do not.
  One has a UTF-8 BOM inconsistent with later bytes. Full receipt and selection
  method are in the recommendation and ignored evidence.
- Owner-requested sample denominator: 949 member/file associations are 946 unique
  files out of 33,682 unique `.txt`/`.yml` files (**2.81%**), or **0.90%** of
  105,382 files of all types. Same-scope enumeration completed without errors;
  `sample-coverage.json` records counts and `count_sample_scope.py` reproduces
  them. The sample does not establish playset-wide prevalence/reliability.
- Established a genuine stored-data beta baseline through `HandlerClient`,
  without resolving candidates or reparsing logs. Run `20261003-74G2EB`, package
  `68f1ae5db205ab46afef9c4d`: script-system 4,992 occurrences / 718 distinct
  diagnostics; non-script 3,924 / 2,203; existing syntax query 2 / 2. One script
  diagnostic is pathless (two occurrences); 347 script diagnostics have multiple
  paths, producing overlapping buckets over 160 referenced paths. One of the
  two syntax diagnostics is also script-system. These are observed values, not
  acceptance thresholds or a new classification rule.

Evidence lives outside Git in `.codex-tmp/task08c/`: `survey.py`,
`encoding-survey.json`, `playset.json`, `beta_baseline.py`, `beta-baseline.json`,
and a disposable `genuine.sqlite3`. The source backup was opened SQLite read-only
only to prepare that disposable copy; all Run/diagnostic/playset reads used the
public handler. Both research scripts shut down only their disposable handler.
These JSON receipts are research evidence, **not delivered beta exports**.

## Pending owner direction

1. Any 08B corrections newer than the current handoff, before changing shared
   reporting files. The brief expressly says to receive ongoing corrections.
2. Confirm or correct the proposed first beta section: rank referenced files and
   show contributing diagnostics beneath each. The brief calls this an assumption
   and asks for owner correction before implementation.
3. Encoding policy: conservative ambiguous/unsearched outcome with explicit codec
   override (recommended), or search the highest-ranked candidate as explicitly
   tentative. The brief explicitly requires direction before implementation.

The two asynchronous questions in the chat cover these three points. No response
has been received at this checkpoint. Do not treat elapsed time as a disposition.

## Implementation receiving notes

These map the requested work onto existing owners; they are not new requirements.

- `SourceSearch._roots` currently permits outside-playset explicit roots, and
  `_physical` is lexical. Extend the existing member association/enumeration path
  to intersect explicit paths with each Run's stored members and enforce resolved
  containment at access. Preserve member-relative paths, overlapping/repeated
  member associations and raw load orders. Validate the public excerpt entry
  point too; it currently takes arbitrary physical paths without a Run scope.
- `_inventory`, `_lookup_scope`, `_files`, `_reference_matches` and `resolve`
  must share effective policy. Put the seven folder defaults in declarative rules
  evaluated generically, prune excluded trees before walking, and key inventory
  reuse on policy/scope. `map_data` excludes directly contained files only.
  Distinguish caller narrowing from internally derived LOCATOR parent scopes.
  A whole-root inventory cannot be reused across incompatible policies.
- Keep stored-reference predicates separate from current source validation.
  Per-reference results must distinguish configuration exclusion, not requested,
  completed not-found, and unavailable/error. Excluded candidates must not create
  false unresolved findings, and unknown required predicates cannot become false.
- `DiagnosticAnalysis.investigate` currently resolves every qualifying row in
  each selected/comparison Run before applying display bounds. Extract references
  from stored data for all ranking/count work; perform optional candidate/excerpt
  work on the requested displayed detail set. Required source filtering and
  explicitly requested source-association analytics still need complete scope.
  Existing query analytics has no explicit source-association switch; expose that
  intent if needed rather than treating ordinary report construction as a request
  for full association work. Disclose selection work versus detail enrichment.
- `source_rollups` already deduplicates records within each referenced-path
  bucket. Reuse it/the existing rollup services for the beta. Do not sum overlapping
  buckets as a unique script total. Use actual `jomini_script_system.cpp` values,
  retain pathless totals, and preserve every contributing diagnostic under selected
  file buckets. Reuse existing report/history services, with the three section
  limits applied after each section's totals.
- `presets.py` scopes the nine syntax selectors to package
  `68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`. It does not
  establish selectors for pending replacement package `f23424ed8aa4d910bf4d3223`.
  Display unsupported lineage honestly; do not reuse old IDs or invent zeroes.
- Add informational same-parent/same-extension stem-substring candidates through
  the same enumerator. Keep them separate from exact resolution, counts and the
  existing `file_line_sources` last-load-order attribution. Preserve literal
  content substring matches without changing exact-token predicate meaning.
- Update current examples/tests that permit arbitrary roots only with the actual
  scope change; keep old 08B receipts historical. Existing genuine source tests
  contain old external-root expectations and cannot be blindly run as 08C
  acceptance. No mock clients, fabricated encodings/folders/history or injected
  failures are authorized. The two-emission LOCATOR exception remains narrow.

## Failed attempts and verification limits

Research-only `pip install --target .codex-tmp/task08c/research-libs
charset-normalizer chardet` failed because network sockets were denied
(WinError 10013). That attempt installed/executed no detector; the owner's later
installation and genuine evaluation are recorded above. Product packaging and
unrepresented encodings remain unverified. The final pip distribution error was
not evidence of incompatible versions.

The repository-wide whitespace check returned exit 2 on pre-existing changes in
`models/catalog.json` and `models/README.md`; those unrelated files were not
changed. A separate check of the two new documents initially used Windows'
default codec and failed; rerunning with explicit UTF-8 passed with no trailing
whitespace. Research files/database were confirmed Git-ignored.

The survey and stored baseline completed. No product change, root-CLI beta,
browser acceptance or new runtime logging check is claimed. Inherited 08B
evidence was read, not rerun. Retain its two unencountered fault groups separately:
database-handler operation/transport errors and ripgrep launch/error exits. Also
retain inspection limits for changing/disappearing Runs, unexpected/double-error
caller paths and unreadable source files.

Remaining delivery: owning-component implementation; encoding disposition and
dependency verification; configuration/CLI guidance; genuine complete-scope and
bounded-enrichment checks; HTML/text/JSON beta exports and browser review;
affected current pointers and final handoff. No production mutation, runtime
restart, model selection, synthetic test, commit or push occurred.
# Owner correction: readable processing, not codec unanimity — 2026-10-04

The owner rejects treating a successfully processed CK3 log as an acceptable
decoder failure merely because strict UTF-8 decoding fails or detector candidates
disagree. The current candidate's rejection of log SHA-256
`cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740`
is a compatibility regression, not a passing ambiguity test. The decoder's
candidate-unanimity rule is not a demonstrated measure of readable processing.
No production caller or parser mechanics were changed for this correction.

Read-only inspection found this exact hash in legacy rehearsal database
`.ck3chronicle/wip/benchmarks/ingestion/legacy-pending-rehearsal-20260908-01/ck3chronicle.db`,
session 55: parse status succeeded, 100,000 source blocks/issue occurrences,
zero silently dropped blocks. All 44 localization_reader.cpp:445 Invalid
character messages have stored blocks, occurrence rows and classification
assignments. The stored quoted invalid byte is U+FFFD; surrounding names such as
Agmánd are preserved. This proves processing, not byte-exact preservation in
those legacy text fields. A public-handler lookup by hash in the current schema-3
database returned no Run. Receipt:
`.codex-tmp/task08c/decoder/stored-log-processing-review.json`.

`tools/check_shared_decoder.py` now records parser-text compatibility and fails
when a checked genuine log differs from the existing parser. Earlier successful
script completion did not enforce this acceptance criterion and is superseded.
The decoder itself still needs correction; actual decoder-call integration remains
pending the coordinated release using disposable caller copies.

