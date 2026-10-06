# Consultant task — focused decoder receiving review

Prepared 2026-10-05. Review the accompanying `DECODER_REVIEW.zip`; begin with its
`START_HERE.md`. This is a bounded research/code/evidence review before combined
release integration, not a request to redesign the decoder or certify all encodings.

## Question

Is the delivered shared decoder a sound basis for the next learner/parser/matcher
release, and does its handoff accurately distinguish demonstrated behavior from
pending integration and evidence gaps?

The API is implemented, with disposable parser/source callers. Production callers
and dependencies have not switched. The documented v60 gains predate decoder
integration. Read current document openings before the dated historical ledger.

## Governing direction

- Support commonly readable text; CK3 encoding warnings do not define readability.
  Missing UTF-8 BOM alone must not reject readable UTF-8. Claims about CK3 refusing
  double BOMs or corrupted headers are observations with limited evidence, not a
  complete engine specification. The owner separately directed a double-BOM stop
  with an explicit failed read and preserved evidence; no automatic header repair.
- Use the known encoding when available; detect otherwise, through one small API.
  Do not reintroduce mandatory detection, detector voting or codec unanimity.
- Preserve original bytes and native processing text, including undecodable-byte
  escapes. Display escapes and normalized search text must not enter parsing,
  identity, byte-offset calculations or stored captures.
- Decoder is application code, with no independent release/version/pin. Frozen
  parser, learner and model artifacts still need their normal authenticated identities.
- Each synthetic test requires explicit owner approval for that specific test.
  No such tests are authorized here. Use supplied genuine bytes or code inspection;
  absent evidence stays unverified. Do not alter originals, install into the project,
  run production services or write the production database.

## Review priorities

1. Check current API/code against those requirements: known-codec behavior,
   automatic selection and confidence limits, BOM/header handling, whole-input
   decoding, failures and warnings. Inspect header checks at physical-file and
   parser-fragment boundaries; a readable fragment must not acquire an unintended
   file-admission rule. Assess whether the thin wrapper adds unnecessary policy.
2. Audit research adequacy: frozen random mod-only sample, hashes and denominator;
   detector comparison; the genuinely ambiguous Swedish file; the session-55
   rejection regression and its correction. Do not infer legacy-encoding accuracy
   from a sample containing 941 UTF-8 files and one unresolved file.
3. Check the actual parser substitution diff and four-log receipts: 186,704
   emissions / 190,701 native inputs reportedly unchanged. Determine what the
   comparisons prove and omit. Downstream classification and installed-release
   loading were not tested by that experiment. Verify receipt/code identities.
4. Review search/excerpt consistency, byte-safe display, failure coverage, and the
   separately reported stored-report export limitation. Do not mistake disposable
   source integration or display helpers for a delivered production export repair.
5. Review receiving completeness: remaining continuation decoder, shared dependency
   loading under `python -I -S -B`, authenticated parser-version changes, package
   comparison assumptions, and Pipeline failure/storage handling. Distinguish a
   decoder defect from work properly assigned to release/Pipeline integration.

Use the ZIP manifest and input map. Scripts are evidence of the original method,
not portable commands to run unchanged: some contain local paths, write receipts
or start disposable handlers. The ZIP omits the database and full 73-log release
corpus. Existing genuine evidence can support focused independent checks in a
disposable location; state exactly what you executed. Do not demand a broad new
test campaign merely because an encoding family is absent.

## Return

Provide one concise Markdown assessment containing:

1. Verdict: **ready for integration**, **ready with stated conditions**, or
   **repair required before integration**, with the principal reason.
2. Material findings only: file/line or receipt, observed behavior, consequence,
   smallest recommended action and responsible owner. Separate demonstrated defects,
   inspection concerns and unexercised cases.
3. A short evidence table: independently checked / producer-reported / unverified.
4. Necessary changes to the decoder or handoff, and the minimum checks that belong
   to the combined release and Pipeline receiving. Explicitly say if none are needed.

Do not provide generic best-practice lists, authorize production activation, or
make complete Task 08C delivery a prerequisite for this decoder release.
