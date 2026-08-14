# Phase 1 lexical calibration record — 2026-08-14

Result: **pass for `P1-PAR-01-LEXICAL` only**.

This record does not exit `P1-PAR-01` or Phase 1. The database persistence
portion of `P1-PAR-01` has not yet received the same separated evaluation.

## Evaluated candidate

- Product-code commit: `52a43254f847555a871833ef4a43bd97f3613bf6`
- Reference `error.log` SHA-256:
  `675216ebb2dbcd8b24bc0bb15474616826c923781be463ea22a9a5da1042b2bf`
- Reference `error.log` bytes: `7,684,888`
- Expected and observed timestamped blocks: `28,131`

The evaluator tooling and documentation were uncommitted during this
calibration. The product lexer under evaluation had no working-tree change
from the candidate commit.

This first calibration runner recorded the candidate commit but did not yet
fail closed if Python imported a package outside the declared checkout. The
matching code copies were manually checked, but this keeps the result at
calibration grade. The committed successor runner binds the imported module
path and hash to the declared Git root and requires a clean candidate by
default.

## Separation of duties

1. The blind runner received the candidate code and reference log, but no
   oracle path or expected block data.
2. The read-only scorer received the sealed runner result, its required hash,
   and the frozen oracle. It did not import or execute product code.
3. The scorer first verified the runner-result hash and failed closed when an
   initially supplied oracle path was wrong. It was then rerun with the exact
   frozen oracle.

This was **procedural isolation inside Codex**, not a hard security boundary:
agents in the same Codex task share host filesystem and tool capabilities.
Release-grade hidden holdouts require separate OS/CI identities or user-held
oracle custody, as specified in `PHASE1_EXIT_PROTOCOL.md`.

## Sealed artifacts

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| Blind runner result | 10,638,417 | `A066AE383F6D18C889A7FE5A53221B6FEC7BC6A66E08A83A3D1C2755778FD0A3` |
| Frozen lexical oracle | 10,791,458 | `AD1F2BBE91AC717FE5C1A21FEDB7ED30218A5C7CA59232BA3BD9700808EAFEC6` |
| Independent score result | 396 | `49864DF9BFE7613E73420A670096373197740261CE4ED6B769801925781B52C5` |

Large runner/scorer outputs remain under the ignored `.phase1-exit/` working
area. Their hashes, not mutable paths, are the durable identity in this record.

## Score

- Component: `P1-PAR-01-LEXICAL`
- Status: `pass`
- Blocks compared: `28,131`
- Field mismatches: `0`
- Discrepant records reported: `0`

The scorer compared input identity, block count, block boundaries, line count,
timestamp, level, source tag, source family, exact raw-block SHA-256, byte count,
derived source-block identity, and aggregate byte counts.
