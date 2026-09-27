# Source-specific native learner refactor: delivery review

Date: 2026-09-20. Implementation of the owner-authorized
[learner refactor plan](LEARNER_REFACTOR_PLAN.md).

## Source-specific learning

The native audit replayed 73 unchanged captured logs: 2,517,940 emissions,
2,594,601 recovered messages and 133 emission source families. It found 90,518
distinct exact message strings and 90,494 distinct token sequences. Neither
an exact message nor a token sequence occurred across source families. This
supports source-specific learning. No cross-source derived-template comparison
was performed or retained in the implementation.

The earlier learner already called its clusterer separately per source. The
refactor retains that boundary throughout collection, alignment, inference,
context patterns, L1/L2 components and template identity. An anchor index reduces
candidate comparisons within each source. The source-code line suffix is not
a separate template family; original source tags remain in native occurrences.

[Source audit data](../.codex-tmp/learner-refactor/source-audit.json) records
every inspected input and its hash. The original survey's inaccessible/changing
input exclusions remain unchanged.

## Implemented changes

| Owning component | Result |
|---|---|
| `inventory.py`, `records.py` | Protected evidence inventory; recovered messages, complete parser pieces/gaps, wrapper context, every native occurrence and explicit unresolved emissions |
| `clustering.py` | Source-specific anchor indexing and ordered similarity; deterministic medoid selection independent of repetition counts |
| `patterns.py` | All-member consensus literals; complete native patterns; only KEY, OPTIONAL_KEY, PARAM, LOCATOR and VALUE; exact byte capture inspection |
| `layers.py` | Learner-owned source-applicable failure/reason interpretation, with separately learned L1/L2 components and native region boundaries |
| `artifacts.py` | One immutable candidate serializer/loader used by direct and registry builds; bundled exact parser; hashes, provenance and visible empty override list |
| `incremental_template_registry.py` | Registry/features schema 3, message scope and provenance/accounting validation; incompatible caches rejected without conversion |
| Research callers | Native bundle-based review, inference inspection and symbol-suffix research; obsolete fixed blind-exercise callers removed |

The monolithic learner CLI no longer contains masking, suffix removal, alternate
tokenization or the earlier slot vocabulary. The raw parser implementation and
its hash are unchanged. It performs no deduplication. SQL diagnostic assembly
and within-Run deduplication remain downstream, with complete diagnostic content
and no required emission-record join.

## Native verification and candidate

The candidate is built from the complete previously annotated log, SHA-256
`16d3ab935f938e63ae3dd460dfeffeee6f32c2a31d95782fd787356f1afce196`.
This is an implementation inspection build, not a claim of full-corpus training
or release quality.

Revision: `7fe7cfd73ae5faf324389ed8`.
[Candidate manifest](../.codex-tmp/learner-refactor/final-review/candidates/7fe7cfd73ae5faf324389ed8/manifest.json).
[Model contract](LEARNER_NATIVE_MODEL_CONTRACT.md).
[Focused native examples and captures](../.codex-tmp/learner-refactor/FOCUSED_REVIEW.md).
[All 1,536 supporting message variants](../.codex-tmp/learner-refactor/examples/INDEX.md).

- 8,111 emissions yielded 8,723 messages and 1,536 distinct native message
  variants, processed within 65 sources into 176 candidate templates.
- Every recovered occurrence was accounted for. No unresolved parser structure
  occurred in this input; the unresolved evidence path remains explicit.
- Literal text plus captured values reconstructed every supporting message
  exactly. Captures covered all five types, including present/absent
  OPTIONAL_KEYs; original native ranges and wrapper text were checked.
- Tripling the actual occurrence lists left template identities unchanged for
  every source. Occurrence weighting no longer determines alignment literals
  or medoid selection.
- Registry cache/build and direct construction produced byte-identical models.
  Incompatible feature scopes/versions were rejected. A separate interpreter
  loaded the bundle and replayed its bundled selected parser successfully.
- The nine native parser/consumer checks passed. Current research review and
  suffix-mining commands executed successfully against the candidate.

[Inspection results](../.codex-tmp/learner-refactor/final-review/inspection.json)
and the reusable [inspection tool](../tools/template_learning/inspect_native_learner.py)
record the concrete checks. No synthetic CK3 messages or old expected
classifications establish these findings.

The namespace example now learns the complete dotted/numeric event identifier
as one KEY, without fixing a majority event prefix into the template.
Localization keys remain complete KEY captures; the inspected varying file
paths are LOCATOR captures. The full evidence for broader naming and historical
model issues still needs semantic review; this refactor does not declare every
reported model defect closed.

## Review debt and pipeline handoff

Self-inspection found 7,959 occurrences with one full candidate match and 764
with multiple matches (762 script-system, two persistent-reader). They remain
provisional. Complete training-member fit is not evidence that all learned
generalizations or slot semantics are correct. Types are explicit learner
proposals with their rationale and observed values.

An additional complete native log containing the 915-message continuation
produced 3,694 messages: 3,532 full structural matches, 67 provisional and 95
unknown. No L1-only or L1+L2 partial outcome occurred in these two inspections;
those counts are reported as zero. Neither inspection silently chooses the
closest candidate. Full text, context and provenance remain in
[the additional-log report](../.codex-tmp/learner-refactor/additional-log-inspection.json).

The next model-quality work is review of overlapping candidates and slot
semantics, then broader owner-directed corpus learning/research. The separate
error-type hierarchy is not invented by this refactor. The pipeline team owns
adapting its reader/matcher and SQL path to the delivered native contract,
including complete diagnostics assembled before occurrence deduplication.
The existing application model reader is not claimed compatible with this new
candidate schema. No runtime model promotion, production registry/database
mutation, watcher startup or runtime-inspector change was performed. All
candidate state and review material are in ignored `.codex-tmp/learner-refactor/`.
