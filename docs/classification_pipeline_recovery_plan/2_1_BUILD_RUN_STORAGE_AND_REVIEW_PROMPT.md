# Mini-project 2.1 — Build aggregation, Run storage and native review

Suggested model: **GPT-6 Astra (`gpt-6-astra`)**. Reasoning effort: **`xhigh`**.
Use with [the master prompt](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/MASTER_ORCHESTRATOR_PROMPT.md) and [the stage coordinator](C:/Users/nateb/Documents/ck3chronicle/docs/classification_pipeline_recovery_plan/STAGE_2_RUN_PROCESSING_ORCHESTRATOR_PROMPT.md).
This is an implementation handoff prepared for owner review.

## Outcome and entry

Construct aggregation, current SQLite storage and native review as one
connected boundary. Consume the Stage 1 direct contract/record interfaces,
original-byte emission access and approved classification outcomes.

Read WORKPLAN 1.1–1.5 / N4–N6, plus
[docs/TRUSTED_RUN_SPEC.md](C:/Users/nateb/Documents/ck3chronicle/docs/TRUSTED_RUN_SPEC.md:253) 253–277 and
[docs/ARCHITECTURE_AND_DATA_LINEAGE.md](C:/Users/nateb/Documents/ck3chronicle/docs/ARCHITECTURE_AND_DATA_LINEAGE.md:176) 176–204 / 227–244.
Those specify compact identity, native review and complete Run storage.

## Exact mutation scope

Create only:

- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/aggregation.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/review.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/schema.py`
- `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/repository.py`

Edit: none. Delete: none.

Record the entry baseline and finish with the master's changed-file scope
proof. A needed change to a preceding file returns to its owning mini-project
before dependent work continues. Runtime evidence output is implemented here;
writing actual evidence or databases is a separate operational action.

## Existing code references and why these bodies are new

| Existing file and exact scope | Reason for new composition |
|---|---|
| [src/ck3chronicle/db/repository.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/repository.py:168) `get_session_by_error_log_hash` 168–181 | Full-log duplicate rejection is useful behavior; the new repository writes current Runs, so its SQL is written against the new schema. |
| Same repository, staged writes 1286–1543 / 1763–2046 / 2531–2837 | Old source, assignment/payload and projected issue representations are replaced; these writers are not ported. |
| [src/ck3chronicle/db/schema.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/db/schema.py:1) 1–550; 21-table inventory in CALLER_INDEX | Existing DDL includes obsolete stages and features. Build only the current Run/record/review representation. |
| [src/ck3chronicle/semantic_projection.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/semantic_projection.py:475) `_unclassified_draft` 475–496 | An old unknown issue is not the target native review evidence. No current native-shard writer implements the target. |

## Functions and implementation steps

1. In `aggregation.py`, implement `diagnostic_identity`,
   `add_classified_diagnostic` and `finish_records`. Use all identity roles
   defined by the approved contract, including concrete values and locators
   where required. Aggregate occurrence count and first/last observed timestamps.
   Grouping solely by contract ID or old regex signature is insufficient.
2. Make assignment eligibility explicit using Stage 1's approved outcome.
   Render stable text from that versioned contract and store the needed concrete
   values/rendering. Unknown emissions do not acquire a diagnostic identity
   merely because some slots were extracted.
3. In `review.py`, implement `ReviewShardWriter`,
   `append_review_emission` and `finish_review_shard`. Stream original native
   bytes with headers and continuations in original order and frequency.
   Use the original byte view; do not encode replacement-decoded text.
4. Implement the proposed mixed-emission representation: write an emission once
   when one or more children require review, with child routing/provenance in
   associated metadata. Preserve occurrence frequency across distinct emissions.
   Keep recognized-emission counts, recovered-diagnostic counts, classified
   counts and review-emission counts distinct. Record this physical choice for
   the Stage 2 owner review.
5. Produce one native shard per successful Run, including an empty shard.
   Its namespace is tied to the destination generation and Run ID so equal
   Run IDs in different generations cannot collide. SQLite holds the reference,
   counts, availability, integrity and routing metadata required by architecture
   176–191, not a duplicate unresolved text payload.
6. In `schema.py`, define current-generation DDL for successful Run facts,
   required model/contract/application/parser/splitter/normalizer/schema lineage,
   compact approved records and review metadata. Enforce duplicate full-log hash
   rejection within the generation. Store enough record interpretation/rendering
   for reads to remain independent of the installed model and original log.
7. In `repository.py`, implement the following concrete API:

| Function | Responsibility |
|---|---|
| `create_generation` | Create a separately named current schema and generation identity. |
| `open_generation` | Open only the supported current generation for writing. |
| `open_generation_readonly` | Open stored current-generation facts without mutations. |
| `find_run_by_log_hash` | Resolve/reject an already processed full-log hash. |
| `write_run` | Complete one Run's records and native-review metadata. |
| `get_run`, `latest_run`, `list_runs` | Read current Run facts. |
| `read_diagnostics`, `read_review_metadata` | Supply the stored report/audit/review interfaces. |

8. Define the concrete SQLite/filesystem order by which shard completion and
   Run acceptance remain consistent. Report the ordinary transaction/file
   behavior on success and failure, including any unaccepted temporary file.
   A failed write cannot leave a successful Run pointing at an incomplete shard.
   Do not port the old processing journal, invent a reservation/reuse scheme,
   or add a publication state machine without a requirement.
9. Keep originals independently retained. Neither duplicate rejection nor a
   failed Run gives this code authority to delete a protected original log.
   Use one supported schema; incompatible generations require an explicit fresh
   rebuild through 2.2 rather than migration on open.

## Deliverable and following work

Deliver the four scoped modules, their actual data/schema shapes, repository
API and shard completion contract. Give 2.2 exact inputs/results for
`write_run`, hash rejection and shard completion. Give 3.1 the read API and
stored fields required by reports/audit.

Present the concrete identity/routing/layout and cross-resource behavior in
the Stage 2 review. Do not claim those physical choices were already specified
by the old implementation. Finish with the required file-scope proof.
