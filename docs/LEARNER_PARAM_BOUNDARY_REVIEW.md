# Step 1: PARAM boundary correction — 2026-09-25

Status: v32 source correction and complete native ten/thirty comparison finished.
Owner requested closer investigation of script-effect collateral losses and
empirical proof of any benefit from repeated regrouping; those follow-ups are in
progress. Pause after this step's results, before work-list item 2. No model
publication, production selection change, parser change or runtime matcher change.

## Implemented scope

- Removed acceptance of PARAM based on punctuation on either side. A colon,
  sentence ending or any arbitrary adjacent punctuation supplies no support.
- Removed the unmarked-PARAM acceptance route outright. The owner explicitly
  corrected the attempt to preserve assignments from this suspect pool. A
  replacement token-width witness rule was withdrawn before any completed model;
  it is absent from the implementation. Recognition needs for genuine unmarked
  fields will be investigated separately after reviewing this correction.
- Existing outer balanced `()`, `[]` and `{}` discovery still runs before
  interior wording alignment. Every empirical PARAM must have corresponding
  complete raw-token enclosing pairs in all native members. Asymmetric markers
  must actually pair in the raw sequence, not merely touch the field's strings.
- Quotes remain secondary aligned candidates, subject to complete capture replay;
  they are not masked before initial word comparison as brackets are.
- Coalescing across an intervening word now requires a complete enclosing pair,
  not punctuation on one side. Final boundary validation applies after all
  coalescing. Adjacent-marker review no longer proposes arbitrary colon-to-colon
  or sentence-ending envelopes.
- Existing explicit owner-declared structures retain their authority. No
  example-specific rescue rules, default literals, PARAM-to-KEY fallback or
  imported templates were introduced.

An enclosing pair only proposes a region. Existing content variation/type checks
and unique complete capture replay remain required. This correction does not
prove every retained paired PARAM is semantically justified. Diagnostic-only
comparison, joint support validation and merge control remain items 2–5.

Rules and their current authority are recorded in
`tools/template_learning/owner_rules.json`, `inference_policy.param_boundary_preference`.
Implementation is in `regions.py` and `patterns.py`; learner version is v32.

## Native evaluation

Fresh builds use the same ten logs and the same thirty logs as v31, after checking
their SHA-256 values against the saved selection. v31 is only a frozen comparison
artifact. No inference conclusions are loaded from it. Logs, model bundles,
complete native evidence and readable comparisons are under
`.codex-tmp/learner-refactor/param-boundaries-v32/`.

| Corpus | Templates v31 → v32 | Full v31 → v32 | Provisional v31 → v32 | Unknown | Observed runtime v31 → v32 |
|---|---:|---:|---:|---:|---:|
| Same ten logs, 352,317 messages | 298 → 331 | 290,887 → 290,789 | 61,430 → 61,528 | 0 → 0 | 69 → 250 seconds |
| Same thirty logs, 1,143,064 messages | 416 → 479 | 701,714 → 697,258 | 441,350 → 445,806 | 0 → 0 | 303 → 647 seconds |

These are training-corpus outcomes, not accuracy or unseen-log generalization.
Timing is observed wall time in the shared environment, not an isolated benchmark.
The ten-log build changes 546 contextual rows / 1,090 occurrences. Of 98
full-to-provisional occurrences, 62 have competing matches and 36 retain one
narrower candidate with insufficient support. The thirty-log build changes 980
rows / 7,609 occurrences; 149 original-ten and 4,307 added-twenty occurrences move
from full to provisional. The latter are texture errors whose path is now LOCATOR;
their support status needs explanation separately from their improved typing.

Revisions: ten `cf7ad19059eaa77eb5c7e0e7`; thirty
`0deaa13fdfc7a7e27fdc13c1`. Both builds completed their bundle/hash validation.
Every native evidence row reconstructs its original message from raw pieces.
Every empirical PARAM capture checked has the recorded complete raw enclosing
pair; no unmarked empirical PARAM remains. That check does not prove the retained
fields' semantic correctness. Mesh bracket fields remain PARAM. `Unknown trigger`
and `Unexpected token` retain their diagnostic wording. The malformed-brace
formulation remains a provisional literal; no broad PARAM rescue was added.

## Confirmed collateral loss in script-effect messages

The explicit trace PARAMs are retained. The narrower audit compares actual capture
spans, not just a source's aggregate outcome. Across these three sources
(`jomini_effect_impl.cpp`, `jomini_effect.cpp`, `jomini_script_system.cpp`), it finds
zero lost declared PARAM captures: 351,588 retained capture-occurrences in ten
logs and 788,329 in thirty logs. These are field-occurrences, not message counts.

However, two previously enclosed ID descriptions lose PARAM in the ten-log
comparison. Denise de la Châtre's `(Internal ID: 91375 - Historical ID 3034322)`
is one native witness. The preceding `(run_setup_tests_effect)` trace is still
PARAM. In the thirty-log comparison, thirteen parenthesized ID/location spans in
the travel-debug messages become literal. See `script-param-audit-10.json` and
`script-param-audit-30.json` in the ignored review directory for actual native
text, raw pieces, old captures, resulting templates and provenance.

The code path is `clustering.refine_literal_variants`: a rejected unmarked field
partitions the entire native pool by that field's exact spelling and starts
inference again in each child. Variation evidence for a different enclosed field
can disappear in that smaller pool. This is collateral loss, not evidence that
the trace was unmarked and not a justification to restore unmarked acceptance.
No new field-retention or rescue rule has been implemented. The owner requested
closer investigation before accepting the result.

## Repeated regrouping: five-source ablation complete

The printed regrouping loop restarts after each accepted union; it is not simply
several full passes over an unchanged pool. There are also two invocations of a
separate complete-match absorption loop. Reduced group counts and broader match
coverage alone do not establish a benefit.

An isolated native-only ablation compares no region regrouping and one sweep of
original groups with the completed v32 output, on every native message from five
selected affected/control sources across the same thirty logs. A single sweep
can merge disjoint original groups but does not reopen merged groups. The two
absorption calls are instrumented separately. This changes research-process
functions only; production learner files are unchanged.

Completed evidence is in `regrouping-ablation.json`. Some consolidation has real
value: data-system failures that were literal singletons acquire the retained
diagnostic `Could not find data system function '<KEY>' in '<PARAM>'.` One
original-group sweep already achieves that result; repetition adds nothing there.
Beyond one sweep, two history messages gain variable character fields while
retaining their wrong-sex diagnostic. However, 61 parent-history messages lose
`hasn't been born` / `the wrong gender` from one competing formulation, replaced
by three KEYs; provisional outcome counts conceal that wording loss. Region
regrouping also generalizes Event/List target to `<KEY> target`, already in the
single-sweep variant. Complete-match absorption remains enabled in both variants,
so this is specifically a region-regrouping ablation, not an all-merges-off run.

This establishes mixed benefit/harm on the five named sources, not a complete
all-source comparison. The latest owner directive instead requires a structural
CHARACTER_FULL_ID inventory and a pause before implementation; that checkpoint
is documented in LEARNER_CHARACTER_FULL_ID_STATUS.md. No field-retention rescue,
name recognizer, or further merge correction has been added.
