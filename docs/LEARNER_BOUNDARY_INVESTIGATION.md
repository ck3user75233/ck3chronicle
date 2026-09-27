# Learner boundary investigation

The subsequent [reason-composition investigation](LEARNER_REASON_COMPOSITION_INVESTIGATION.md)
traces null-word captures to their actual supporting messages and documents
additional native failure/reason structures. Training remains stopped.

## Stopped at 48 logs; trace alignment corrected

The owner stopped the exercise after 48 complete logs: 1,940,027 message
occurrences, 20,572 distinct messages and 110 sources. The 73-log build was
interrupted. The registry already contains 73 training inputs, but its last
completed candidate is the 48-log revision; a plain future build would use all
73 unless its evidence selection is explicitly restricted. No restart is running.

The owner suspected LOCATOR sometimes included location labels. Inspection of
1,071 LOCATOR positions with 16,634 observed values in the 48-log model found
no captured `file:`/`line:` labels. Paths and line values are separate LOCATOR
slots; labels remain literals. Continuous range text can occupy a line locator;
there is no claim here about unobserved range formats.

The demonstrated trace defect was in alignment. Whole-sequence matching jumped
between repeated `file:`/`line:` entries and proposed PARAM spanning several
trace frames. Boundary validation rejected these patterns, preserving the
native evidence but leaving the composition incomplete.

Correction: corresponding punctuation pieces are mandatory ordered anchors;
sequence alignment runs only between those anchors. Every native trace entry
therefore keeps its own file, line and context boundaries. This is generic
boundary enforcement, not a hardcoded trace length or reason-word rule.

The correction was exercised over all 2,507 stored native failure regions from
29 rejected candidates. All now match their rederived patterns. Regrouping those
actual failure regions also passed complete membership/matching checks. Separate
discovery groups can converge to identical structural patterns, so the learner
now merges those candidates and their evidence rather than counting duplicate
IDs as competing alternatives. This does not suppress distinct overlapping
patterns. The research evaluator now uses `partial` when L1 and L2 are both
recognized but framing is incomplete; `L1-only` is reserved for a missing L2.

A targeted replay replaced only the 29 failed patterns using their complete
saved supporting variants and matched the two complete comparison logs. The
first log's 367 partial matches fell to zero; the second remained at zero. This
was a diagnostic replay, not a new trained/published corpus checkpoint. Native
trace content and each path/line capture are in
[the corrected trace example](../.codex-tmp/learner-refactor/trace-boundary-fix/TRACE_EXAMPLE.md).
Machine-readable replay and regrouping evidence is beside it.

### Remaining L2 inference issue requiring a separate correction

The real-log results still expose overgeneralized reason words. These are
source-local L2 candidates, not a return of whole-message inference:

- `<OPTIONAL_KEY> character was null` has only one observed nonempty first
  value, `target`, plus absence. The owner now supplies `target` as literal
  wording; formulations with and without it remain separate. This does not
  authorize an optional-literal architecture.
- `target <OPTIONAL_KEY> was null` has observed values `faith`, `slot`, `title`
  and absence. Its wildcard also accepts `character`, which was not a
  supporting value in that discovery group.
- `<KEY> <KEY> was null` has first-position values `Target`/`target` and
  second-position values `culture`/`faith`. It likewise accepts unseen word
  combinations because KEY presently validates lexical boundaries alone.

The next inference correction must distinguish evidence of a variable symbol
from differing literal formulations. The blanket one-value-plus-absence split
was broader than the requested guidance and has been removed for separate
review. Explicitly supplied wording stays literal. Multiple reason words also do
not establish that arbitrary symbols belong in those positions. Preserve the
observed alternatives and explicit insufficient evidence while designing that
criterion; do not invent additional word lists beyond the owner's supplied wording,
restore the old two-word heuristic, or select one match merely to hide overlap.
No new reason-word categorization rule has been introduced in this correction.

## Superseding full-log exercise

The owner corrected the @ treatment using native CK3 definition evidence and
resumed complete-log learning. Parser v1.1 retains adjoining @ in the string:
`[@name]` becomes `[`, `@name`, `]`. The two-log checkpoint now infers
`Cannot read [<KEY>] as a script value` and captures
`@cultural_maa_extra_ai_score` in full, with brackets literal.

This supersedes statements below that the parser is unchanged or training is
paused. Those describe the prior bounded regression stage. Results are in
[the full-log checkpoint report](../.codex-tmp/learner-refactor/at-symbol-incremental-review/REVIEW.md).
The earlier 64-case result is not representative corpus performance evidence.

Updated 2026-09-20 after owner authorization to fix the current code.
Corpus training remains paused. The changes below were checked on 64 distinct
native examples, not a resumed checkpoint or a promoted model.

## Current corrections

- Recognized script errors learn L1 and L2 independently within
  `jomini_script_system.cpp`. Every L2 observation in that source enters the
  same L2 pool regardless of its L1. There is no L1/L2 eligibility table.
  Recognized constructions do not enter competing whole-message inference.
- The learner treats the raw parser's punctuation pieces as literal syntax.
  Candidate grouping preserves their ordered signature; inference cannot put
  them in KEY or PARAM. Matching checks raw-piece boundaries, and KEY requires
  one complete non-punctuation parser token. Internal string punctuation is
  unchanged. The parser implementation is unchanged, including its `[@` piece.
- LOCATOR holds the variable path/file/number, with labels and delimiters in
  literals. Numeric location values have a numeric constraint; captures must
  respect parser boundaries. The short line pattern rejects expanded clauses.
- Exact message aggregation already existed within and across logs. Distinct
  native messages (source + context kind + exact text) each enter inference
  once; occurrence lists preserve repetition without weighting learning.
  Components likewise deduplicate their own exact text within source and role.
- Registry builds now carry explicitly confirmed templates forward unchanged,
  match them first, and infer candidates only from uncovered records. Multiple
  confirmed matches remain visible as ambiguity. Provisional candidates are
  not silently confirmed. The registry `confirm` command requires template IDs,
  revision and a review note. No owner confirmations were made in the paused
  registry. The confirmation exercise is isolated verification state only.
- Native model schema 2 represents compositions through independent region
  patterns and message-level observed matches. All native framing/location/trace
  content remains in the evidence record. Pipeline integration is separate.

The [rule ledger](LEARNER_INFERENCE_RULES.md) states the owner-authorized
conventions and remaining generic inference heuristics. No historical code
restoration or further search for value in expunged architecture is planned.
Recovering the symbol survey is not a prerequisite for these boundary fixes.

## Verification

[Corrected native examples](../.codex-tmp/learner-refactor/boundary-fix-verification-v2/EXAMPLES.md)
and [machine-readable inspection](../.codex-tmp/learner-refactor/boundary-fix-verification-v2/inspection.json)
cover 64 distinct examples from four sources, including all six previously
reviewed cases reparsed from their original captured emissions. All 64 have one
complete ordinary match or one complete component composition in this bounded
inspection. 160 captures were checked against native byte ranges. One literal
`Failed context switch` L2 is reused across eight observed L1 texts. Numeric
line templates reject the expanded location clause. Exact duplicate aggregation
and explicit-confirmation carry-forward were exercised. The sample is not a
claim about correctness or ambiguity counts across the paused corpus.

## Historical checkpoint evidence (before these corrections)

## Evidence available for review

Incremental checkpoints completed at 1, 2, 4, 8 and 16 logs. The 32-log build
was stopped after ingestion and before candidate publication. Its parsed
features remain available. No training process remains running.

[Six native comparisons](../.codex-tmp/learner-refactor/boundary-investigation/EXAMPLES.md)
show script values with and without an `@` prefix, two distinct script reasons,
an expanded location, and a game-rule modifier error. Each JSON includes an
unchanged emission node from the raw parser's debug serializer, the recovered
message API's exact token/gap pieces and byte spans, proposed templates,
captures, and matching L1/L2 components at every completed checkpoint.
Historical normalization/tokenization and diagnostic-lead results are explicitly
separate: these are function comparisons on the same message, not a replay or
acceptance of the old parser or old model.

[Checkpoint outcomes](../.codex-tmp/learner-refactor/incremental-review/REVIEW.md)
are structural matching counts on the two previously discussed logs. Both enter
training. The one-log baseline reproduced 764 ambiguous occurrences on the first
log, and 67 ambiguous/95 unknown on the second. After 16 logs these are 828
ambiguous on the first and 76 ambiguous/zero unknown on the second. These
counts alone do not establish correct template semantics or slot boundaries.

## Findings before these corrections

1. **The new raw parser is used, but punctuation boundaries are mishandled.**
   `lexical_pieces` in `parsers/v1/parser.py` detaches a leading punctuation
   run as one token. Thus `[` is a separate piece before an ordinary script
   value, while `[@` is one piece before an `@`-prefixed value. All non-gap
   pieces have kind `token`. `patterns.derive_pattern` aligns complete piece
   texts, so these two opening pieces do not match. It joins the unmatched
   pieces into a variable span. `_slot` accepts any continuous non-whitespace
   span as a KEY, including the bracket. The result retains the original bytes
   but fails to retain the common opening bracket as a literal. The historical
   tokenizer separated `[` and `@`; the same raw-piece difference is real.

   More precisely, the learner's `continuous` predicate means only that the
   reconstructed string contains no whitespace (`patterns.py:35`). It does not
   mean one raw-parser token. `derive_pattern` concatenates unmatched parser
   pieces before calling `_slot` (`patterns.py:84`). Thus the parser already
   separated the leading punctuation from the identifier, but KEY inference
   ignores that boundary after joining the pieces. This is not a second lexer;
   it is a slot-inference decision made without the relevant parsed boundaries.
   The parser's grouping of adjacent punctuation and the learner's loss of
   boundary information are distinct issues. Refining punctuation granularity
   alone does not make the KEY inference boundary-aware.

2. **The source partition is intact; distinctions within that source are not.**
   The overlapping script candidates are all from `jomini_script_system.cpp`.
   In all 32 already-parsed logs, the exact phrase `Failed context switch`
   occurs only inside the recognized L2 region of that source: 242,763
   occurrences across 2,004 distinct complete messages. No outside-L2 example
   was found in those logs. See the [scope inspection](../.codex-tmp/learner-refactor/boundary-investigation/failed-context-scope.json).
   This is not a claim about uninspected CK3 messages.

3. **Whole-message inference does not use the learned L1/L2 distinctions.**
   `artifacts.build_model` first groups and derives patterns for complete
   messages, then calls `learn_layers` separately. Complete-message grouping
   uses similarity and shared word pairs, without a diagnostic/reason lead
   restriction. Shared framing can therefore group distinct reason forms.
   Consensus then replaces their differing reason words with slots. The
   evaluator computes layer matches separately; they do not constrain a
   complete candidate match. A literal L2 reason can coexist with an overbroad
   complete-message candidate matching it. This is not a search for that reason
   across other sources or an inference that it also exists as a standalone
   error.

4. **A relevant historical grouping restriction was omitted.**
   Historical `diagnostic_lead` extracted within-source distinctions including
   script role/shape and the first two reason words. Historical
   `cluster_source_records` required equal leads before a similarity comparison;
   `best_cluster` applied the same restriction. Those functions distinguished
   the observed reason leads `failed/context` and `unknown/loc`. Current
   `clustering.py` has no equivalent restriction. This behavioral change was
   not properly accounted for when removing the old normalization. The exact
   two-word heuristic is not thereby a requirement to restore; preserving
   useful distinctions on native evidence needs explicit review.

5. **The old learner combined empirical inference and hand-written rules.**
   It performed real ordered sequence comparison, alignment and template
   derivation. It also applied many sentence-specific replacements to KEY,
   OPTIONAL_KEY, TYPE, PARAM and LOCATOR before learning. Therefore its apparent
   success cannot be attributed entirely to empirical discovery. Its matching
   path chose one highest-scoring candidate instead of reporting all complete
   matches, so old single-result outputs do not establish absence of overlap.
   These facts support neither a blanket claim that the learner was fake nor
   blanket acceptance of its historical behavior.

6. **Location constraints are too broad in the inspected candidate.**
   `_slot` identifies numeric line values as LOCATOR but emits empty constraints
   for that type. Matching then permits arbitrary text, including the full
   expanded-file clause after the number. The native example matches both a
   short location template and the template explicitly representing that clause.

The historical source inspected is commit
`1af79a4e29b673f2b93eb250b71179c4639af435`,
`tools/template_learning/learn_error_templates.py`: tokenizer at lines 732–741,
diagnostic lead at 847–909, grouping at 1066–1099, matching at 1162–1260, and
sentence-specific normalization at 556–670. A read-only comparison copy is in
the ignored investigation directory. It is not installed as a learner fallback.

## Scope of historical observations

The historical observations above explain terminology from the earlier review;
they are not a worklist to restore old preprocessing. “Historical candidate
selection” meant returning one preferred matching candidate rather than all
alternatives. It did not mean treating each input log as an independent corpus.
Before this correction, current incremental builds retained all accumulated raw
features but rebuilt provisional templates, without confirmed-template reuse.
The current registry now has explicit confirmation carry-forward.

No claim is made that the old workflow already satisfied that requirement.
No further historical-code audit is required for these fixes. The current code,
owner-approved conventions and native evidence are the implementation basis.
