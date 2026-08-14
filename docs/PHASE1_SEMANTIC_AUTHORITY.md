# Phase 1 semantic authority reconciliation

Status: implementation authority reconciled; independent `P1-PAR-02` execution
has not run.

## Result

Phase 1 has two related but non-interchangeable semantic projections over each
immutable source block:

1. the canonical issue projection describes accounting, category, error type,
   severity, primary location, and referenced symbols/objects;
2. the empirical classification projection describes repeatable error-template
   identity, L1/L2 structure, typed slots, and assignment confidence.

Neither projection may silently rewrite the other. A category does not choose
an error template, and a learned template does not invent a canonical category
or referenced symbol. Both remain derived and reproducible from retained raw
evidence.

This resolves the apparent conflict between the older 252-item semantic oracle
and the later template-learning reviews: they answer different questions.

## Hash-bound public calibration artifacts

| Artifact | Role | SHA-256 |
|---|---|---|
| `SEMANTIC_LABELS_ADJUDICATED.json` | Canonical issue-field calibration: 252 ordered blocks, 232 classified, 20 preserved unclassified | `db8a58a9a7f7f7fb0b84d1e39c1b2e724eae8058a00d07bb578367b795723e3d` |
| approved model `models/93196794a7e0115d/empirical_template_model.json` | Frozen structural-template inference input | `3bd189b4c93ad260e925d1a1ac3ece7c79cc63217480b79a939f6f7f5d034db3` |
| learner `release_candidate_v2/FINAL_REVIEW.md` | Model provenance and bounded-development decision | `8ac04b3a73edd34d8805ff9815c41a8fba229dfb19c2473775dab0d73ee300b4` |
| `human-template-review-queue-v4-human comments.xlsx` | Early explicit user comments on templates and slot roles | `a44313c57fb1dc5b2b440f9664cd4218bc2d318ed7b0474847f81f176a285d6b` |
| `ck3chronicle-new-candidate-adjudication-20260813.xlsx` | Explicit user comments on scope paths, semantic role words, and residuals | `d84b76ebe0ed7d53ae4eddaa5f2e956e60f6125b2b937443b2eed2e31619b631` |
| `ck3chronicle-template-review-v44-20260813.xlsx` | Review-preserving disposition of the preceding comments | `04a5fdc57f33d42fc73279048e4ae79a92d24da985ae0db8324dd58037507a9e` |
| `ck3chronicle-holdout-semantic-review-gen2-20260813.PARTIAL-REVIEW-20260813T152042.xlsx` | Later partial user review of L1/L2 residuals | `4fa2a2beb311ceec5009ec5e8aa9440c8403ecb786423ce356b6dc6a638240f3` |

These files are public development/calibration evidence because their content
has already been inspected or used while refining the implementation. A file
or folder named `holdout` or `unseen` in this historical material is therefore
not eligible for the future private `P1-HOLD-01` release gate.

Only explicit user-entered decisions and reviewer notes are human authority.
Prefilled candidate contracts, preliminary findings, default `Pending` values,
blank decision cells, and machine dispositions are proposals. In particular,
the partially reviewed generation-two workbook does not approve every
prepopulated corrected contract.

## Authority precedence

When projections disagree, apply this order without changing raw evidence:

1. exact retained source bytes and provenance;
2. the frozen canonical issue-field oracle for its declared fields;
3. explicit human template/slot decisions for the examples they address;
4. the hash-approved empirical model and its PostValidate contract;
5. conservative L1-only or unknown disposition when no reviewed rule applies.

An implementation mismatch does not authorize editing an oracle. A proposed
oracle change needs a new artifact version, rationale, review, and hash.

## Reconciled template rules

- Source family and ordered semantic literals define template identity.
- Timestamp, locator value, line/range value, key value, and repetition count
  never create a different base template.
- Strong locator grammar runs before L1 assignment. A typed `<LOCATOR>` can
  satisfy only a locator slot and can never be absorbed by `<KEY>`, `<VALUE>`,
  `<PARAM>`, or `<TYPE>`.
- L1 is the stable outer contract. For script-system diagnostics it includes
  `Script system error! Error:`, the leading key expression, and the literal
  semantic role `effect` or `trigger`.
- L2 is the optional ordered reason/explanation inside brackets. A stable
  reason phrase may have its own typed slots. A novel or uncertain reason does
  not erase a proven L1 and must not be forced into a known L2.
- `scope:` is grammar outside the changing slot. A path such as
  `scope:actor.target` is represented as `scope:<KEY>.<KEY>` so the period's CK3
  relationship remains explicit.
- Character/display identity may use `<KEY> (<KEY> <OPTIONAL_KEY>)`; optional
  internal/historical metadata does not split the template.
- Repeated identical embedded clauses create multiple semantic occurrences of
  one base template; repetition cardinality is not template identity.
- Symbol-shape hints such as `*_effect` and `*_trigger` may quality-check a slot
  only after a template is nominated. They cannot discover the contract.

## Key, parameter, and locator meaning

Slot role is positional and contract-specific; it is not inferred from a
global trigger-word list.

- `<KEY>` is a CK3 symbol, identity, object label, or other contract-defined
  identifier occupying a reviewed key position.
- `<OPTIONAL_KEY>` is a key-position member that can be absent without changing
  the contract.
- `<LOCATOR>` is source/evidence position: path, filename in a source-position
  construction, line/column/range, or a complete script-location chain.
- `<PARAM>`, `<VALUE>`, and `<TYPE>` remain available only where a reviewed
  contract needs those distinctions. An arbitrary unfamiliar token is not a
  parameter merely because the learner cannot identify it.

The historical suggestion that a title such as `x_nf_1449` might be a locator
is not adopted. In `Failed to find any valid flavorization for title x_nf_1449`,
the title is a CK3 symbol key; it is not a source location. Conversely, a
texture or script path in a source-position phrase is a locator even when it
contains symbol-looking segments.

## Storage mapping

| Authority | Production records |
|---|---|
| Exact source evidence | `source_blocks`, immutable archived logs, source/run provenance |
| Canonical issue fields | `occurrences`, `issues`, parse counters and signatures |
| Structural templates | classification model registry, runs, payloads, contracts, assignments |
| Human review debt | L1-only/unknown review queue and retained unresolved reason text |

Issue signature and template contract ID are intentionally different keys. An
issue signature clusters normalized canonical issues; a template ID clusters
source-qualified ordered semantic structure. Reports may present both but must
not imply that equality or causation follows from their co-occurrence.

## Implemented reviewed decisions

The approved model and classification contract v2 already contain the reviewed
high-priority structure:

- separate `scope:<KEY>.<KEY> trigger` and plain `<KEY> trigger` L1 forms;
- literal `effect`/`trigger` semantic roles;
- optional historical identity slots;
- repeated-clause expansion;
- complete location-chain separation;
- script-system L1/L2 classification with conservative fallback;
- locator-first typed PostValidate.

The generation-two reviewed residuals are handled conservatively: the paired
illustration diagnostic receives no invented locator; the new illustration key
shape remains a source-qualified review item; reviewed script-system shapes
retain a sound L1 while novel reasons remain unresolved L2; the supported
travel-plan reason has a structured full contract.

## Remaining release work

This reconciliation closes the implementation-authority prerequisite. It does
not pass `P1-PAR-02`, promote old development holdouts to release evidence, or
prove every low-volume model slot. The independent evaluator must still compare
all 252 canonical issue judgments and separately score structural template and
slot behavior against a frozen release candidate.
