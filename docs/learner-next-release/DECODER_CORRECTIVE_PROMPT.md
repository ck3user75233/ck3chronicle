# CK3Chronicle — decoder pre-integration corrective

For the existing Data Intelligence / 08C conversation: please complete this
corrective as a receiving repair to your decoder delivery. Keep it separate from
the remaining 08C scope. Update the shared release handoff so Learner receives the
corrected API, exact integration instructions, verification results and file hashes.
Finish with READY FOR LEARNER INTEGRATION or the specific unresolved defect.
Do not begin release integration or production activation.

This is a **small corrective to the reviewed decoder delivery before combined release integration**.

Do not begin the broader Learner release task, publish a new release, modify production selection, restart services, reprocess logs, or broaden this into a general encoding investigation.

The purpose is to remove two concrete defects identified in independent review so the decoder presents a sound boundary to the Learner team.

## Objective

CK3Chronicle's primary requirement is reliable ingestion and preservation of Paradox `error.log` evidence so Runs can be stored and compared longitudinally to understand which diagnostics are appearing, persisting and disappearing.

For this purpose:

- Paradox error logs are processed as **known UTF-8 with `surrogateescape` byte preservation**.
- Native bytes, byte spans and reconstruction must remain authoritative.
- A parser-internal byte fragment must not accidentally acquire physical-file admission semantics.
- The decoder does **not** need comprehensive automatic-encoding support for every possible game/mod source file before this release.
- Existing automatic source decoding remains useful to reporting, but improving its coverage is outside this corrective.

## Local checkout and inputs

Continue in the existing 08C checkout: `C:\Users\nateb\Documents\ck3chronicle`.
Every path below is relative to that checkout. Use these existing files directly;
the consultant review ZIP is not needed.

Read `AGENTS.md`, `docs/DEVELOPMENT_ENVIRONMENT.md`, the current API description
`docs/TASK08C_ENCODING_RECOMMENDATION.md`, and the opening current section of
`docs/TASK08C_HANDOFF.md`. The receiving instructions to correct are in
`docs/learner-next-release/HANDOFF.md`, under **Decoder delivery: exact hookup
instructions**, especially **Parser substitution**. Older dated checkpoints in
08C's handoff are historical where superseded.

| Purpose | Exact local files |
|---|---|
| Shared decoder implementation | `src/ck3chronicle/decoder.py` |
| Disposable parser substitution and comparison harness | `.codex-tmp/task08c/decoder/check_disposable_parser.py`; `.codex-tmp/task08c/decoder/parser-substitution-simplified/parser_candidate.py`; `.codex-tmp/task08c/decoder/parser-substitution-simplified/parser.diff` |
| Current four-log parser receipt and original input identities | `.codex-tmp/task08c/decoder/parser-substitution-simplified/results.json` |
| Source/search comparison harness and disposable callers | `tools/check_shared_decoder.py`; `.codex-tmp/task08c/decoder/source_search_before.py`; `.codex-tmp/task08c/decoder/candidate/source_search.py` |
| Current source comparison receipts | `.codex-tmp/task08c/decoder/simplified-verification/verification.json`; `.codex-tmp/task08c/decoder/simplified-verification/sample-decoding.json` |
| Preserved-byte and detector observations | `.codex-tmp/task08c/decoder/simplified-display-search/results.json`; `.codex-tmp/task08c/decoder/library-behavior-review.json` |
| Frozen genuine source sample, original paths and hashes | `.codex-tmp/task08c/random-mod-survey.json`; `.codex-tmp/task08c/random-mod-sample-manifest.json` |

These are the existing development implementation, disposable experiments and
retained evidence, not a production release to activate.

## Corrective 1 — separate physical-file header inspection from parser-fragment decoding

The reviewed disposable parser currently routes arbitrary parser spans through the shared decoder's ordinary `decode()` path.

The decoder's ordinary path performs physical-header inspection and can reject a `double_bom` before returning processing text.

Those are different concerns.

A byte span extracted from the middle of an `error.log` is **not a new physical file**. Its first bytes must not be interpreted as that fragment's file header.

Correct this boundary.

The resulting design must provide a shared decoder path suitable for the parser's known-UTF-8 byte fragments which:

- decodes using UTF-8 plus `surrogateescape`;
- preserves undecodable bytes exactly;
- does not perform physical-file BOM/header admission on an arbitrary internal span;
- does not normalize or substitute native processing text;
- continues to permit exact byte reconstruction using UTF-8 plus `surrogateescape`;
- does not alter parser framing, emission boundaries, byte spans, recovery or tokenization.

Retain physical-file header inspection for the places where the input genuinely represents a complete source file and that inspection is intended.

Do **not** solve this by weakening or deleting source-file header checks globally.

Choose the smallest clear API separation that makes the distinction explicit. Do not introduce a routing framework or generalized decoding architecture.

Update the API comments in `src/ck3chronicle/decoder.py`, `docs/TASK08C_ENCODING_RECOMMENDATION.md`, `docs/TASK08C_HANDOFF.md`, and the decoder hookup section of `docs/learner-next-release/HANDOFF.md` so the receiving Learner team is not instructed to copy the reviewed disposable parser substitution unchanged.

## Corrective 2 — make `bom_bytes` truthful

Independent review reproduced a metadata error on genuine supplied BOM-bearing source bytes:

an explicit BOM-consuming codec such as `utf-8-sig` can consume the physical BOM while the returned `DecodedText.bom_bytes` remains `0`.

Correct this field so its documented meaning and returned value agree.

If `bom_bytes` represents bytes removed from the native byte sequence by BOM handling before the returned processing text, it must report those bytes for explicit BOM-consuming Unicode codec paths as well as automatically selected BOM paths.

Do not use this corrective to redesign BOM policy or add speculative encoding heuristics.

Inspect current consumers before changing the contract. Preserve compatibility where the existing meaning is already relied upon; if no consumer exists, make the field's meaning explicit now rather than preserving demonstrably false metadata.

## Focused verification

Use the genuine retained evidence at the local paths above. The four original
log paths and SHA-256s are in `logs[]` of
`.codex-tmp/task08c/decoder/parser-substitution-simplified/results.json`.
Session 55 is the entry with log SHA-256
`cf3214a8186859223a9d3e5c36fafcd1d3d01c8ca715bcabcac986e3a2750740`.
For genuine BOM-bearing source bytes and the unresolved source, use the original
`files[].path` and `files[].sha256` entries in
`.codex-tmp/task08c/random-mod-survey.json`, alongside the current source receipts
listed above. These identify existing originals; no ZIP extraction or new sample
is required.

At minimum verify that:

1. the known-UTF-8/surrogateescape path still round-trips the session-55 error log exactly;
2. the parser's genuine comparison inputs retain the same framing, emission counts, body/decoded text, recovery and native reconstruction after the API correction;
3. parser byte fragments now use the fragment-safe known-codec path rather than physical-file header admission;
4. genuine BOM-bearing source evidence demonstrates truthful `bom_bytes` behavior for the affected explicit codec path;
5. the automatic unknown-encoding path and its existing conservative `undetermined` behavior have not been unintentionally changed.

Reuse valid existing comparison evidence where the relevant bytes and behavior are unchanged. Run only the focused comparisons necessary to establish the effects of these edits.

Do not manufacture CK3 histories or claim genuine-game evidence from constructed examples. If an edge condition lacks a genuine positive example, verify the implementation boundary by inspection and state that limitation plainly.

## Explicitly out of scope

Do **not** undertake any of the following in this corrective:

- broader UTF-16/UTF-32 research;
- East Asian encoding research;
- further detector benchmarking or threshold tuning;
- another mod-corpus sampling campaign;
- attempts to make automatic decoding universally correct;
- broad source-search/reporting redesign;
- stored-report surrogate display/export repair;
- 08C folder, scope or beta work;
- final `chardet` dependency/distribution closure;
- isolated learner/package loading work;
- continuation-caller integration;
- release freezing, model rebuilding or package publication;
- Pipeline/database integration;
- production selection, ingestion, restart, reset or cutover.

Those remain with their existing receiving tasks.

In particular, the known-UTF-8 Paradox error-log path must not be made dependent upon automatic detector availability merely to complete this corrective.

## Deliverable

Return the corrected decoder delivery in place, with:

1. the exact files changed;
2. a short explanation of the new **physical source file vs parser fragment** boundary;
3. the exact `bom_bytes` semantics after correction;
4. genuine verification results and identities used;
5. any evidence limitation that remains;
6. updated HANDOFF instructions for the Learner receiving task;
7. final hashes/identities for the corrected decoder delivery.

Finish with a concise disposition:

- **READY FOR LEARNER INTEGRATION**, if both corrections are complete and focused genuine verification passes; or
- **NOT READY**, naming the concrete unresolved defect.

Do not convert unrelated limitations into blockers. The criterion is whether the shared decoder is now a reliable component for CK3Chronicle's known-UTF-8 Paradox error-log ingestion path while retaining its already-reviewed bounded source-file capability.
