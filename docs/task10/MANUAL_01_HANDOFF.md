# Manual Part 1 — product introduction and orientation

2026-10-12. Launch & Distribution / Docs, existing **TREK-11**.

## Current revision r2 — restored assignment consumed

The Owner restored [MANUAL_01](../task10-deliverables/MANUAL_01_PRODUCT_INTRODUCTION_AND_ORIENTATION.md)
after CMT-173. The restored requirements are now incorporated; the missing-prompt
limit in CMT-173/176 is resolved. CMT-177 records temporary return of these three
pages to Part 1. The r2 delivery releases them to Part 2 again. The first input
snapshot and all prior receipts remain intact; the older sections below are
historical evidence for that first delivery, not the current coverage statement.

Current evidence root: `.codex-tmp/manual01-20261012/r2/`. It contains prior bytes,
the restored prompt, `verification.json`, `example-provenance.json`, `headings.json`
and the new three-page `manual01-snapshot/` / `manual01-edition.json`. This remains
an intermediate Part 1 input, not a final bundled manual or combined freeze.

R2 verification passed: **44 local links/anchors**, **20 headings inventoried**,
genuine example bindings/count/native-input correspondence, exact application
and manifest fields, all **11 existing manual files unchanged**, all **13 prior
frozen inputs** and the first Part 1 snapshot preserved. Mermaid labels/edges
were reviewed as a seven-node flow. No runtime commands were used.

R2 input manifest SHA-256:
`d425a0ee7ca1cb830a61991f5dc4a57a85a8b6e98f0edb4ce7a69752cf4f78ee`.

| Page | Current SHA-256 |
|---|---|
| `PRODUCT_VERSION.md` | `153b7e2c2217a430e30841f47b839d50d11b9f9ccf2edd9520705f0a5cb7e031` |
| `INTRODUCTION.md` | `cb9120f1f81fa7e7975d9abe215ec91084ef8edcf7ca4040070c78b86b17d54d` |
| `ORIENTATION.md` | `ce5e295b45ce2141e2beaf9a70b24d834225782e016a27da2c3cd9792a500795` |

### Restored requirement coverage

| Requirement | Current explanation / evidence |
|---|---|
| Product/platform, manual and model versions | Product Version distinguishes application 0.0.3, opening revision, classification model/package, bundle and formats. Instructions identify `application.version` and `manual_revision` in the actual manifest. Compact IDs follow their purpose. |
| Purpose, audience and use cases | Introduction starts with volatile logs; covers post-play review, recurring issues, mod/playset changes, locating sources and supplying structured evidence to AI assistants for investigation/patch proposals. |
| Empirical templates and example | Emitting-code analogy is explicitly bounded. Genuine unknown-trigger excerpt demonstrates literal wording, KEY/LOCATOR values and wrapper context; simplified notation is labelled. Other names/references/variable-length REASON values depend on published declarations. |
| Template family versus diagnostic/count | Different values/context remain separate records; repetitions increment occurrences. Selected layout and supporting entries contribute to identity. Human investigation and machine-readable grouping/comparison are both explained. |
| AI and near-match help | JSON supplies explicit wording/values/references/coverage; reasoning and proposed patches require judgment. Planned features marks typo/missing-key/AI-identifier assistance exploratory and links current source context. |
| Journey and component purposes | Orientation begins with a labelled Mermaid flow and connected prose. Separate rows explain parser, templates/model, matcher, selector, handler/database, review, reports/queries, source context and retained Learner. |
| Three Run groups and retained input | Metadata/context/lineage including playset; diagnostic definitions/values/counts; unresolved native review. Protected raw logs are separate input with independent 30-day retention. |
| Capture/lifecycle/crash facts | Capture ID precedes successful Run ID; duplicate hashes refer to the existing Run. Live error/debug logs, reconstructed playset and associated root exception.txt are distinguished; absent facts remain unavailable. |
| Launch options | Manual Start launcher versus separately user-configured Windows sign-in automation, using the same launcher/config. Installation supplies existing launch contract; setup is not described as registering startup. No unverified OS recipe supplied. |
| Source attribution | Recorded playset, candidate files and last applicable load-order member. Current files can differ; missing/ambiguous attribution stays explicit and source association does not establish fault. |
| Single writer and external readers | One handler, one queue and one serial database worker per database. Concurrent clients differ from writers; external readers can overlap the single writer, with short-transaction/busy/locking precautions. |
| Packages and reproducibility | Purpose precedes ID/pin. Registration adds an authenticated package to a catalog; setup separately selects an available pin for future processing. Recorded lineage and retained components support traceability/reproducibility; old Runs keep their identities. |

Sources: [product intent](../OWNER_PRODUCT_INTENT.md),
[architecture](../ARCHITECTURE_AND_DATA_LINEAGE.md),
[approved contract](../ERROR_CONTRACT_SPECIFICATION.md), current component
contributions and the complete current manual. Version/schema/launcher facts
were checked read-only against the received wheel and bundle manifest/builder.
Current CMT-168/169 deferral supersedes historical ingestion-design waits.

### Genuine diagnostic correspondence

Reuses saved public-handler/report evidence for **Run 20261008-01PBM7**,
diagnostic ordinal **614**, template `886a8eb94e4218403e4dd015`, **11 occurrences**,
from `.codex-tmp/task10d/evidence/report.json`. Model revision
`3bc531d578074e6a430c161e` and package `2b12932103f3a3111a4e1880` are unchanged
in 0.0.3. Execution remains original C9/0.0.2 evidence, not a newly executed Run.

Shown excerpt: `Unknown trigger: adulterer, near line: 414`. Its wrapper records
`common/scripted_triggers/zzz_99_religious_triggers.txt`, near line 415. The four
bindings and published line-label alternatives are from that saved result.
Input log SHA-256:
`5a7b93d8ee374c60f767593631713eaf8719004ba4f9cf33e7eb5d812dbec629`.
The saved export and actual protected log are authenticated and the excerpt
checked read-only. REASON explanations come from the contract; this example is
not claimed to contain that slot. No fabricated CK3 text, count or history.

### Heading inventory

| Page | Headings in reading order |
|---|---|
| Product Version | Which version means what?; Check your copy; Supplied classification reference. |
| Introduction | Who it is for; Questions it helps you answer; Why templates help; Working with an AI assistant → Planned features; From a test session to useful history; Where to start. |
| Orientation to ck3chronicle | From CK3 exit to a report → Starting observation; The parts you work with; What a stored Run contains; Templates and packages; How source context fits; Terms at a glance. |

Exact heading levels/anchors are in `r2/headings.json`. Reader review checks
purpose, journey, Run contents, templates/values and package purpose before
requiring the CLI reference; detailed syntax stays in existing reference pages.

### Part 2 integration actions

- Use r2 instead of the CMT-173 input; include all three pages in Part 2's
  systematic negative-construction inventory, contextual classification and
  lead-reviewed recommendations before broader review. Part 1 does not claim
  that whole-manual pass.
- Build the numbered TOC beginning with these pages. Replace the opening-revision
  label with the actual combined manual edition on finalization.
- Consolidate `INTRODUCTION.md#planned-features` into the final dedicated Planned
  Features section/page and retarget its link. This current local subsection
  supplies a working destination until Part 2 chooses that location. Keep the
  current source-context capability distinct from exploratory near-match help.
- Installation already supplies the launch/configuration contract. Check any
  exact Windows startup instructions before including them; Part 1 describes
  the user-configured choice only, not an exercised startup procedure.
- Correct the unchanged external-data page's “concurrent-writer timing” wording
  as a factual erratum. The new orientation correctly explains the single writer;
  the erroneous phrase must not become a new multiple-writer test requirement.
- Create the combined freeze and deliver it on existing TREK-10/16. Preserve
  CMT-159/131 and old archives. README, other canonical pages and packaging remain
  unchanged by Part 1. No product/service/publication action was performed.

No missing assignment authority or unresolved technical fact remains for these
three pages. Final TOC/roadmap placement and edition naming are the explicit
Part 2 integration actions above. Verification details and hashes accompany the
r2 delivery; the earlier checks below retain their original scope.

## Historical first delivery — CMT-173

## Delivered pages and editorial transfer

The three opening pages are written for application **0.0.3**, in reading order:

1. [Product Version](../user/PRODUCT_VERSION.md)
2. [Introduction](../user/INTRODUCTION.md)
3. [Orientation to ck3chronicle](../user/ORIENTATION.md)

They are actual user prose, with a linked reading sequence, definitions and
links into the existing manual. No task identifiers, receipt commentary,
acceptance status or development-machine paths appear in these pages.

The Part 1 editor releases all three pages to the Owner-issued Part 2 editor at
the delivery comment on TREK-11. Part 2 can revise and integrate them into the
full manual and its numbered table of contents. Part 1 deliberately leaves
`docs/user/README.md`, `DOCUMENTATION_HANDOFF.md`, the other canonical pages,
bundle-facing text and packaging sources to their existing editors. This
handoff is internal evidence, not a fourth user page or replacement manual.

## Authority and the damaged assignment

The Owner explicitly requested these three pages and continuation of TREK-11.
On intake, the named
[MANUAL_01 assignment](../task10-deliverables/MANUAL_01_PRODUCT_INTRODUCTION_AND_ORIENTATION.md)
contained only one unrelated sentence about running a PowerShell download script
(114 bytes). Its observed bytes are preserved in the evidence directory. The
Owner was informed during work; the assignment file was left untouched.

The companion [Part 2 assignment](../task10-deliverables/MANUAL_02_STRUCTURE_AND_EDITORIAL_REVIEW.md)
establishes the expected filenames, opening reading order and conceptual topics.
Those instructions and the explicit user request supplied enough scope to
write the pages. No absent Part 1 requirements are claimed to have been checked.
This does not execute the separately assigned whole-manual editorial review.

## Technical and editorial review

| Page | Explanation delivered | Facts checked against existing evidence |
|---|---|---|
| Product Version | Separates application, bundle, model, Learner and format identities; explains how to identify/check a copy. | Received 0.0.3 wheel and metadata; default model selection/manifest; schema versions; bundle builder and Verify launcher. |
| Introduction | Explains modder audience, practical investigation questions and first-use reading path. | Owner product intent; current query/report, workflow and installation references; local processing and read-only source boundary. |
| Orientation | Explains components, capture-to-report journey, Run contents, templates/bindings/counts, packages, source context and a glossary. | Current architecture/contract vocabulary; Pipeline, Watcher, Reporting and Learner contributions and their canonical references; schema/lineage; genuine previously received workflows. |

Specific semantic checks: Capture ID is distinct from Run ID; duplicate file
hashes do not create another Run; unresolved evidence stays outside diagnostic
rows in one native review shard; provisional assignments can be stored; occurrence
and record counts differ; current source excerpts are not historical snapshots;
source association does not prove causality; one queue/serial database worker
serves each database; stopping the watcher does not stop the handler; raw-log
retention is independent of successful ingestion and preserves stored history.

The pages introduce no new command procedure or transcript. The template example
is explicitly conceptual, not fabricated CK3 evidence. `Verify.cmd`, `--config`
and the stop explanation reuse existing launcher/configuration semantics.
No runtime command, handler startup, capture, ingestion, report generation,
retention, source edit or acceptance campaign was performed for these prose
changes. Existing execution evidence keeps its original C9/producer identity.

## Snapshot and verification

Evidence root: `.codex-tmp/manual01-20261012/`.

- `before.json` records that all four new document paths were absent before work.
- `existing-user-pages.json` pins the pre-existing manual files.
- `TREK-*-before.json` preserves protected reads of the six named work records.
- `verification.json` records local links/anchors, editorial checks, wheel/model
  authentication, and preservation checks for the existing manual/frozen edition.
- `manual01-snapshot/` and `manual01-edition.json` preserve the exact three-page
  delivery with destination paths and SHA-256 hashes for integration.

Verification passed: **30 local links/anchors**, all **11 pre-existing manual
files unchanged**, all **13 prior frozen document inputs authenticated**, and
the received wheel/version/default-model identity authenticated. New documents
have no trailing whitespace or internal status/path leakage; `git diff --check`
passed. The initial verifier used an LF-only metadata assertion and stopped on
the wheel's CRLF line endings; correcting the verifier to read logical lines
resolved it. This was a verification-script error, not a product/version failure.

Part 1 manifest SHA-256:
`3caaec101c819e971da7b3e2849df5df9452408f43249b45b1c832a55fe420d5`.

| Page | SHA-256 |
|---|---|
| `PRODUCT_VERSION.md` | `c25e0bc00be6c1b1df072957c8194ed3b0bf701a6b7f6e942cd2bd4228c3e241` |
| `INTRODUCTION.md` | `4cdb73229bcbba2236e6d662d1463997c936ac957a0d0b65b452d9d35748e611` |
| `ORIENTATION.md` | `4770e91e21a70f4ae6015ec579ff65ece93829deee7cb33515bfd5aad4208664` |

This is a **Part 1 input snapshot**, not a new complete manual freeze or an
already-packaged distribution. The full-manual editor must include these pages
in the replacement edition, recheck links after reorganization, and publish
the combined document identities for 10B and 10C.

## Prior receipts and next action

Retrieved current team state and TREK-9/10/11/12/15/16 before editing. Prior
10D-r2 receipt **CMT-159**, 10E receipt **CMT-131**, C9/C10 and all original
snapshots remain intact. TREK-11 is continued for the new manual revision;
TREK-15's completed execution scope is unchanged. Owner deferral CMT-168/169
governs the separate ingestion/hash-lookup/retry discussion; no such feature is
advertised here or required to finish this documentation.

Next: Part 2 integrates these opening pages and completes its whole-manual
review, TOC and combined freeze on this same TREK-11 record. 10B/TREK-10 uses
the resulting replacement manual in a new archive; 10C/TREK-16 receives the
final installed guide. Their packaging/environment obligations remain separate.
The only missing assignment evidence is the damaged Part 1 prompt; no unresolved
user-facing technical fact was identified in the three authored pages.
