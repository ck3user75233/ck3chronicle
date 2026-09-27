# Task 04 supplement: repair template matching

Repair the pipeline so it uses the supplied error templates directly, then
complete the Task 04 Error Contract specification. Pipeline source edits needed
for this repair are authorized.

Scope: `C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/`.
Keep learner code and model artifacts unchanged. Preserve unrelated work.

## Required behavior

1. Preserve the native emission, source and original-value correspondence.
2. Match the supplied source-applicable template's literals and ordered slots.
   Matching determines the capture boundaries; preprocessing must not decide
   slot positions or types.
3. Bind each matched slot to its complete original value.
4. Apply only processing required by the matched template/contract.

Remove phrase-specific rules, preassigned slot markers, literal rewriting,
invented optional slots and runtime restrictions additional to the template.
These rules are banned before and after matching; moving them elsewhere is
not a repair. Retain evidence-preserving framing, exact literal/order matching
and explicit handling of ambiguous matches.

- `<KEY>` captures one complete key, including punctuation and numeric components.
  Do not split it into multiple keys or reject its lexical fragments separately.
- `<PARAM>` captures a variable-length phrase, including multiple words. It is
  valid typing, not a fallback for rejected KEY values or an incomplete result.
- Preserve literal words. In `<PARAM> of (Internal ID <KEY>)`, `Internal ID`
  remains literal and the two slots capture their respective original values.
  Use this structure only if supplied by a template; do not add a name recognizer
  or introduce a new slot type.

## Implementation focus

- [normalization.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py):
  remove semantic rewriting from `_Composer.key_path`, `known`, `structured`,
  `persistent` and their active callers. Keep an evidence-preserving matching view.
- [classifier.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py):
  remove independently imposed slot restrictions in `_accepts`. Let the supplied
  template determine slot boundaries and any declared constraints.
- [bindings.py](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/bindings.py):
  preserve one complete original value per matched slot. Update adjacent pipeline
  interfaces where required; keep one processing path.

Review recovery and extraction calls for the same prohibited behavior. Do not
silently change a supplied template to fit an occurrence. If its structure cannot
represent native evidence, preserve the unresolved result. Record required
learner enhancements in
[MODEL_BUGS.md](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/MODEL_BUGS.md)
using its reporting instructions, instead of adding custom runtime handling.
Report format/revision incompatibilities explicitly rather than claiming
compatibility or disguising loading failures as unmatched diagnostics.

## Preserve implemented classification behavior

| Situation | Outcome | Assigned references |
|---|---|---|
| Non-layered template matched | `matched to template` | whole only |
| L1 and L2 matched | `matched to template` | l1 and l2; whole=None |
| L1 matched, L2 unmatched | `L1` | l1 only |
| No template match, including no L1 match | `unknown` | none |

Match L1 before attempting L2. Given L1, consider every applicable L2 template
in the source partition regardless of its original L1. Never inherit an L1
or trigger/effect characteristic from an L2 reference.

`incomplete` is not currently implemented. Do not manufacture that outcome from
PARAM, key spelling or additional runtime type restrictions.

## Verify and deliver

Use genuine captured logs. Verify complete punctuated KEY capture, variable-length
PARAM capture, preserved literals and original spans, L1-first matching, independent
L2 reuse, and retention of unresolved evidence. Confirm that phrase-specific rules
and additional slot restrictions are no longer active. Do not use old match counts
as correctness targets.

[PIPELINE_RULE_AUDIT.md](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/PIPELINE_RULE_AUDIT.md)
contains exact offending locations, real-log examples, evidence paths and
reproductions. Use it as investigation evidence; the requirements above govern
the repair.

Deliver the implemented cleanup, changed interfaces, verification results and
remaining template limitations, followed by the proposed Task 04 Error Contract
specification. The classification routing is already implemented; this processing-
rule cleanup remains to be done.
