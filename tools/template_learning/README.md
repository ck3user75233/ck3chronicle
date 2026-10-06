# Current delivered learner: v61

The combined decoder/parser/learner release is locally registered and verified.
Learner `0dc8130a0740d2209e1da8e2cc7241d7d735df2c0252342075b7624bfad0e3de`
(publication order 9) and runtime package `4ac4e8ee92346e6d14eacfbf` (order 8)
use parser v1.8 and the authenticated shared application decoder. The fresh
73-log build followed 20/20/20/13. See the [release README](../../docs/learner-next-release/README.md)
and [final handoff](../../docs/learner-next-release/HANDOFF.md) for external pins,
installed artifact, comparisons, reproduction and the separate Data Intelligence
export limitation. Pipeline receiving and activation remain pending.
Production still selects `68f1ae5db205ab46afef9c4d`.

The authenticated v60 research package `840957b2f8e16f1cf0f88ad2` remains the
received baseline; it does not contain the decoder integration. Earlier notes
below are retained history, not the proposed cutover.

## Retained v58 research baseline

The complete frozen release is
`2951fe80c0dd31a83cd639562a427d2658daaeab30279dcd15d32069ea1f2d8a`, retained in
`learners/releases/` and registered at publication order 8. Its verified 73-log
incremental model package is `f23424ed8aa4d910bf4d3223`. That earlier candidate
was retained but never activated; its exact manifest pins are
in [the pipeline handoff](../../docs/LEARNER_PARSER_PIPELINE_HANDOFF.md).

Use the retained release for reproducible learning and the package's own parser,
matcher and owner rules for classification. Current inference guidance is in
[LEARNER_INFERENCE_RULES](../../docs/LEARNER_INFERENCE_RULES.md). Historical notes
below do not supersede that guidance or the current handoff.

## Historical learner v41: complete continuation groups

The published/pinned schema-4 release is **76630685c4a341ca14bf9c7c**, using
parser v1.7 and fresh feature-v4 evidence. One complete learning record retains
an opening plus ordered supporting title entries. Entry PARAM values and repeated
CHARACTER_FULL_ID contents do not contribute diagnostic wording. The owner JSON
holds the component declaration; continuations.py is the shared, hash-covered
component matcher. assignment.py policy v2 supplies one complete selected result.

Native thirty-log comparison, runtime replay, publication details and remaining
limits are in [the delivery ledger](../../docs/LEARNER_CONTINUATION_MODEL_STATUS.md).
Use [the existing formal handoff](../../docs/LEARNER_PARSER_PIPELINE_HANDOFF.md)
for the current interface. No template conclusions are imported between learner
versions. Default literals, repeated regrouping and coverage absorption remain
removed/disabled as previously directed. The sections below record prior changes.

## Historical v36: coverage absorption deleted


v36 deletes coverage-driven absorption and both unconditional calls. The
implementation is removed, with no enable/disable switch. v35 already removed
repeated region regrouping. Each
original group receives one sweep; newly merged groups are not reopened. The
coverage-absorption function no longer exists. v34's missing-parent wording
loss guard is retained; default literals remain disabled.

`TITLE_FULL_ID` extends the shared JSON-driven full-ID mechanism to the native
title formatter, with explicit emitter/outer boundaries. It does not classify
internal title names, rank or ID values. Runtime model validation and the shared
recognizer accept the new type; parser v1.6 remains unchanged.

Implementation, complete-log evaluation and explicit remaining work are tracked
in [the v35 ledger](../../docs/LEARNER_V35_IMPLEMENTATION.md). These are development
candidates, not a change to `models/selection.json`.

## Opaque character and house references retained from v33

Owner-approved `CHARACTER_FULL_ID` and `HOUSE_FULL_ID` capture complete
variable-length names and ID parentheses using emitter-scoped declarations in
`owner_rules.json.parameter_structures`. Lowercase words and empty internal values
are opaque content. `full_ids.py` supplies the same raw-piece recognition to the
learner and active pipeline matcher. No name dictionary, capitalization veto or
internal entity/ID interpretation is used. Existing REASON regions remain opaque.

Fresh ten/thirty-log evaluations and the implementation status are recorded in
[the full-ID ledger](../../docs/LEARNER_CHARACTER_FULL_ID_STATUS.md). These are
development candidates; `models/selection.json` remains the publication authority.
Parser v1.6 is unchanged. The historical checkpoints below are not current pins.

## Version isolation retained from v30

Every build rediscovers templates from all selected native evidence. Template
seeding, the registry `confirm` command, and the confirmed-template discovery
bypass have been removed. Registries and caches are pinned to learner version
and implementation hashes. Default state paths include that identity; explicit
paths reject another implementation's state. A registry pins its parser too.
New learner versions require fresh registries populated from original logs.

This is cumulative batch retraining, not incremental hypothesis updating.
Caches retain exact message text, raw pieces, wrappers and provenance.
Unrecovered emissions remain separately recorded with text, ranges and reasons;
they do not participate in template inference. Stale caches fail explicitly.
See [the v30 work ledger](../../docs/LEARNER_VERSION_ISOLATION_REVIEW.md).
The historical checkpoints below do not describe the current publication pin;
`models/selection.json` is authoritative.

v26 (2026-09-24) fixes declared reason boundaries: explicitly empty fields emit
one zero-length unit; bracket-adjacent whitespace including newlines stays whole
and literal. Raw parser v1.6 and the learning thresholds are unchanged. See the
Task 4 supplement in the existing docs/LEARNER_PARSER_PIPELINE_HANDOFF.md.

Published model: models/1d1d6e0389f7235f565b2504, explicitly selected by
models/selection.json. Use publish_native_model.load_release with the selected
manifest hash. verify_reference_implementation guards replay with the existing
research matcher. Application caller migration is described in the existing
docs/LEARNER_PARSER_PIPELINE_HANDOFF.md; publication does not activate ingestion.

Owner clarification recorded in v25: supported expression fields remain PARAM
for both short and long values; malformed colon-qualified references can be KEY.
No colon-count/game-validity gate or expression-specific rule. The fresh ten-log
run is unchanged from v24. Build commands and native reviews remain ignored.

# Current learner: v26 and published model

Raw-span PARAM evidence no longer requires whitespace, nesting or alternating
separator shapes. Always use the selected raw parser pieces. Qualified KEY spans
are not themselves evidence for PARAM; exact region/member boundaries still need
validation. Equal observed lengths do not veto otherwise supported regions.

A single distinct non-location learning example remains a provisional hypothesis,
regardless of occurrence count. Supported hypotheses need two such examples;
provisional ones cannot produce full outcomes or be confirmed. Published revision 1d1d6e0389f7235f565b2504 retains these statuses. See
docs/LEARNER_NATIVE_MODEL_CONTRACT.md for status fields.

The earlier phrase/nesting restrictions below were assistant engineering
heuristics, not owner requirements; v24 supersedes them. Earlier deliveries and
counts are historical checkpoints, not the current result.

# Empirical template-learning tools

Algorithm v23 recognizes adjacent colon-qualified KEY spans using the registry's
key_syntax declaration and serialized key_joiners constraint. The raw parser is
unchanged. Balanced variable-length token/separator sequences can support PARAM
empirically; the owner-approved Character: description uses an explicit
characterhistory.cpp parameter declaration. Current native comparison and limits
are recorded in docs/LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md.

Read-only frequency/outlier review: `build_visual_review --diagnostics --bundle
<candidate> --baseline <previous-bundle> --previous-review <comparison.json>
--output <review.json> --html <fragment.html>`. This verifies saved bundles and
support counts, exports all-template unique-match frequency, KEY proportions,
adjacent KEY runs, sparse literal formulations and undeclared word-bounded PARAMs.
The previous review's first 17 native cases retain their original numbering.
Metrics are review tools only and do not change inference or model selection.
`template_review.html` owns the interactive view; large raw artifacts stay ignored.

This directory is the source-controlled home of the empirical learner,
incremental evidence registry, native review tools and shared versioned raw
parser used by ck3chronicle development.

Only reusable source belongs here. Captured `error.log` files, parsed exports,
training/reference corpora, human workbooks, private holdouts, incremental
state, and generated evaluation results are deliberately excluded from Git.
Supply those inputs through command-line paths and keep them under one of the
ignored local-data directories or outside the checkout.

The approved runtime artifacts are versioned under `models/` and verified by
SHA-256 at load time. These development tools may produce a candidate model or
catalog, but do not silently promote one. Promotion requires review, a new
immutable revision directory, manifest hashes, regression testing, and a code
change selecting the approved revision.

Semantic quality is tracked, not forced to perfection. Current reports preserve
the counts and examples for full, provisional (insufficient distinct learning support, competing complete candidates or capture assignments),
and unknown outcomes. The invariant is that every occurrence is accounted for;
unknowns and lower-confidence assignments are review debt rather than dropped
evidence.

Fixed historical blind-exercise callers were removed with their obsolete
learner dependencies. The current research evaluator uses the native bundle;
it is distinct from the pipeline progress inspector. No frozen oracle or
historical classification quota controls the build.

## Source-specific native learner

In v22, failing KEY/LOCATOR/VALUE inference no longer implies PARAM. Ordinary
PARAM needs distinct raw-span variation and separate boundary evidence. Unsupported field
pools are re-inferred by native syntax shape, keeping ordinary identifiers apart
from punctuation-only observations and qualified forms. If shape supplies no
distinction, unsupported alternatives retain their literal spellings. No prefix
or diagnostic vocabulary is prescribed by this mechanism; see the native review.

Building on the v21 experiment, current balanced-region inference proposes outer parentheses/brackets/braces
before initial wording comparison and interior alignment. It validates variation
and multi-token raw content from each candidate's actual members, then treats the
supported interior as opaque PARAM, retaining the outer markers. Repeated words
inside that PARAM do not split it. Fixed interiors remain literal; locations and
declared fields keep priority. No presumed literals, NAME type or message-specific
character envelope was added. See the implementation ledger for the native run
and the outstanding ordinary slot-type and word-boundary issues.

For a compact interactive-review dataset from an existing candidate:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.build_visual_review `
  --bundle <completed-candidate-bundle> `
  --output <ignored-review-directory/visual-review.json> --top 20 --examples 3
```

This verifies the immutable bundle, ranks complete diagnostic templates
by training-support occurrences, and verifies supporting distinct variants and
occurrence totals against native evidence. Examples must belong to the actual
inference-support IDs. Ambiguities are ranked by source-specific competing
candidate sets; each ambiguous row contributes to one set. Selected examples
retain exact pieces, captures, declared construction boundaries, framing and log provenance.
Counts and rankings cover the complete bundle; displayed examples are bounded
selections, with distinct learning-unit text preferred. It performs no learning,
confirmation or registry writes.

For a before/after comparison of complete outer-diagnostic runs:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.inspect_outer_diagnostics `
  --baseline <previous-bundle> --bundle <new-bundle> --output <ignored-review-directory> `
  --focus-review <previous-comparison.json> --focus-cases 4 8 10
```

The optional focus list preserves owner-selected review cases at the beginning
of the report; it does not affect training, grouping, or matching. Both bundles
must contain the same input hashes and parser revision. The previous result is
read as saved evidence, while the new result is checked against the current
implementation. Capture ambiguities and punctuation-free PARAM proposals are
visible separately from competing templates.

Owner-directed declarations live in [owner_rules.json](owner_rules.json).
The code reads this file directly; it never injects generated Python into the
source tree. The file lists exact default words and phrases, authority, evidence,
the known script envelope and intact REASON field, existing slot-position cues, and implementation
references for architectural requirements. See the
[rule ledger](../../docs/LEARNER_INFERENCE_RULES.md) for how it is maintained.

Current owner direction disables presumed literals via `default_literals.enabled=false`.
No configured spelling affects grouping, anchors, slot inference or newly built
matching constraints. The retained vocabulary/provenance below is inactive reference
data for the comparison; trace structures and location cues remain operational.

`parameter_structures` declares recognized traces as ordinary PARAMs before
wording comparison and alignment. The generic recognizer supplies raw ranges;
it does not introduce a TRACE type, different tokenizer or trace-specific slot
matcher. Outer-message structural presence/order is checked before matching.
Ordinary unrecognized PARAMs continue to require empirical evidence.

The disabled reference lists words outside the phrases that first exposed the bug: for example
`Event`, `event`, `link`, `trigger`, `effect`, `culture`, and `faith` are explicit
entries. Singular/plural spellings are explicitly declared. Symbol-type defaults
accept either case of the first letter only; diagnostic words keep their listed
spellings. Native casing is preserved in learned literals. Matching uses complete
raw-parser pieces, so `mod_effect`,
`mod_scripted_trigger`, `death_reason`, and `root.faith` remain intact and do not
match these defaults. Colons remain separate literal punctuation. The declaration
does not supply complete templates, example-specific slot types or optional
literals. Models snapshot the reference and hash the file; each slot saves its
literal constraint for matching. Candidate-local evidence may make presumed
literal words content inside a supported PARAM; protection elsewhere is unchanged.

Symbol defaults contain explicitly owner-supplied type names. The folder-derived
expansion and directory inventory were removed: a path does not establish type
identity. Expansion requires evidence identifying actual CK3 symbol types.
`Internal ID` and related labels are phrase guides; standalone `to`/`for` are
not defaults. Event belongs to symbol types.

Location recognition uses labels, colon/in/file context with slash syntax, and slash-bearing
filename syntax, without a folder or extension allowlist. Recognized locations
become LOCATOR even without observed variation. A path spans the original
segment and standalone slash tokens with no intervening gaps. Default words
inside that range are excluded from literal anchors. Labels and following content
remain literal; no rule captures arbitrary text through the line ending.

To rebuild exactly a previous candidate's corpus using the current learner,
without changing its registry, and optionally evaluate additional cached logs:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.inspect_candidate_revision `
  --registry <existing-feature-registry> `
  --baseline-bundle <completed-candidate-bundle> `
  --parser-manifest tools/template_learning/parsers/v1/manifest.json `
  --output <ignored-comparison-directory> --evaluate-remaining
```

This uses validated caches from the baseline's exact parser version/hash and
selects evidence by the baseline bundle's hashes, not the registry's current
training count. It reports all old/new outcomes, transitions and unresolved
native examples. Additional logs are matched with the frozen rebuilt candidate.
`--saved-baseline-outcomes` explicitly reuses the baseline bundle's hash-verified
native training results when repeating an inspection; its occurrence counts
must agree with the saved model. It does not skip evaluation of the new model
or the additional logs.

After a completed comparison, add its additional logs to the cumulative corpus
in an isolated build without changing the registry:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.inspect_accumulated_corpus `
  --registry <existing-feature-registry> `
  --comparison <completed-comparison-directory> `
  --parser-manifest tools/template_learning/parsers/v1/manifest.json `
  --output <ignored-cumulative-directory>
```

This uses the owning builder with native evidence only. It reports
transitions from the previous candidate's saved outcomes on the same accumulated
logs. Those results measure learning from added evidence, not unseen accuracy.

The [model contract](../../docs/LEARNER_NATIVE_MODEL_CONTRACT.md) and
[delivery review](../../docs/LEARNER_REFACTOR_REVIEW.md) describe the implemented
refactor and native verification. Source grouping uses the engine source family
without its terminal code line number. Collection, clustering, inference and
IDs remain source-specific. No cross-source template comparison runs.

```powershell
.\.venv\Scripts\python.exe -m template_learning.learn_error_templates `
  --log <protected-error.log> `
  --parser-manifest tools/template_learning/parsers/v1/manifest.json `
  --output-dir <ignored-candidate-directory>
```

Repeat `--log` for several complete inputs, or use `--runtime-root` to inventory
protected session/pending copies. Candidate bundles contain complete native
patterns, six-slot declarations including REASON, attached wrapper context, exact parser bytes,
hashes, all supporting native evidence and an explicit override list.

For the incremental learning review, `inspect_incremental_learning` accepts
`--corpus <native-survey-summary.json>`, two ordered `--first-log` paths,
repeated `--checkpoint` log counts, `--parser-manifest`, and a fresh `--output`
directory. It adds complete captured logs to an isolated registry and builds
at each checkpoint, always including the complete corpus as the final step.
The registry caches raw-parser features. Templates are rediscovered from all
accumulated training evidence. The two comparison logs also enter training, so their
reported outcomes are not a holdout claim. Each checkpoint retains its native
candidate, comparison messages/captures and outcome counts in the output
directory. This inspection does not alter inference rules or promote models.

```powershell
.\.venv\Scripts\python.exe -m template_learning.inspect_native_learner `
  --log <protected-error.log> `
  --parser-manifest tools/template_learning/parsers/v1/manifest.json `
  --output <ignored-isolated-inspection-directory>
.\.venv\Scripts\python.exe -m template_learning.evaluate_unseen_session `
  --log <protected-error.log> --bundle <candidate-revision-directory> `
  --output <ignored-inspection.json>
.\.venv\Scripts\python.exe -m template_learning.build_review_pack `
  --bundle <candidate-revision-directory> --output-dir <ignored-examples-directory>
.\.venv\Scripts\python.exe -m template_learning.mine_symbol_suffixes `
  --bundle <candidate-revision-directory> --output <ignored-suffixes.json>
```

The inspection command creates a candidate and fresh registry state under its
explicit output directory. It checks native occurrence/capture reconstruction,
burst invariance, cache/build parity and separate-process bundle replay.
Research outcomes preserve full, provisional (insufficient evidence or ambiguous) and unknown counts;
these are candidate structural matches, not production acceptance.

## Outer diagnostic boundaries

Native model schema 3 learns complete outer diagnostics, including locations
and traces. The established script-system envelope is declared in
`owner_rules.json`; its bracket interior is captured intact as REASON. There
are no independent L1/L2/tail pools or component matching gates. The declaration
supplies comparison wording without removing other content from inference or
matching. All field support comes from the candidate's own complete messages.
The observed unbracketed variant is declared too, prescribing comparison
wording but no fields. Its explicit exclusion keeps bracketed reasons with
their own declaration. Matching enforces these construction identities.

`inference_policy` records the transparent short-form admission and field
evidence heuristics. Presumed literals may become captured PARAM content only
within supported fields; parentheses do not force PARAM. Case distinctions,
source scope and raw boundaries remain.
See [status and verification](../../docs/LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md)
and [the current model contract](../../docs/LEARNER_NATIVE_MODEL_CONTRACT.md).

The native comparison tool renders meaningful distinct formulation changes and
validates candidate-local evidence against raw bytes:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.inspect_outer_diagnostics `
  --baseline <historical-schema-2-bundle> --bundle <current-schema-3-bundle> `
  --output <ignored-review-directory>
```

The historical baseline is read explicitly for comparison, never loaded as a
fallback model. Component-only investigation entrypoints were retired; their
source and generated evidence remain in the ignored research snapshots.

There is no template-import or frozen-confirmation path in v30. Native
requirement checks use `CK3_LEARNER_NATIVE_BUNDLE` with the actual schema 3
candidate and `tests/test_learner_parameter_requirements.py`; no synthetic
emissions or recombined fixtures are used.
