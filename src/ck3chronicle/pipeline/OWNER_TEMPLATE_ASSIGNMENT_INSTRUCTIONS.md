# Owner instructions: templates control pipeline interpretation

Updated: 2026-09-17, after the owner's final direction on processing rules.
This is the current instruction record. It supersedes earlier recommendations
to retain runtime slot heuristics or defer their removal to a learner project.

## Current work and authority

Classification routing and outcome labels were implemented in classifier.py
and domain.py, revision `ck3-exact-empirical-classifier-v2`. Broader rule cleanup
is not yet implemented. The owner requires that cleanup within this pipeline
exercise and authorized either implementation here or a supplement to the
paused Task 04 agent. The selected route is the explicit Task 04 implementation
supplement in
[TASK03_CLASSIFICATION_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md).
It extends Task 04's originally specification-only mutation scope for this work.
The original Error Contract specification remains proposed for owner approval.

Learner retraining is not commissioned. The inspector remains a separate side
project. No production ingestion, database operation, watcher action, application
cutover, commit or push is included in this supplement.

## Template authority and banned architecture

An error template is an empirically learned recurring structure with ordered,
typed slots. The supplied template defines applicable literals, slot locations,
types and declared constraints. Pipeline processing must take it as given.

Matching against the applicable source templates determines the template and
capture spans. Successful spans then supply concrete original values for binding
and subsequent template/contract-directed diagnostic processing. The pipeline
must not identify semantic slots in advance, or reinterpret their count/types
through a separate message-rule system before or after matching.

Owner directives:

- No restrictions additional to the supplied template may be imposed by runtime.
- No phrase-specific processing rules belong in the pipeline.
- Recognizing a name or other value through Python rules and converting it into
  KEY markers before matching is a banned architecture.
- A model KEY position binds one complete original key, including punctuation
  and numeric components. It does not authorize KEY-dot-KEY decomposition or
  rejection of numeric fragments as though they were separate identifiers.
- Do not convert a value in a KEY position to PARAM due to capitalization,
  punctuation, length or any other arbitrary characteristic.
- PARAM is the intended slot for variable phrases, including multi-token text
  of varying length inside brackets or quotes. It is a valid declared type,
  not automatically missing typing or an incomplete result.
- If extra custom handling seems necessary, request an enhancement to the
  learner/model in MODEL_BUGS.md. Preserve unresolved evidence; do not implement
  a phrase exception, parallel interpreter or hidden fallback.

These requirements do not ban evidence-preserving native framing, source
identification, literal/order matching, original-span integrity or reporting
ambiguous candidates/captures. Those are matching mechanics, not permission to
invent semantic boundaries. Preprocessing must not alter matchable meaning.

## Example and type boundary

For `Ci Faj of (Internal ID 296591)`, the owner proposed:

```text
<PARAM> of (Internal ID <KEY>)
```

`Internal ID` is literal template text, not a key. `296591` is the captured ID
value in the example. CHAR_NAME was suggested as a possible alternative type;
it is not an approved new slot or a reason to add a runtime name recognizer.
The pipeline must use an actually supplied template, not install this example
as a new handwritten sentence rule.

There is one generic KEY type for the discussed event IDs and keys occurring in
localization messages. There is no distinct localization-key slot type. ALT is
not an owner-approved type. Existing artifact encodings do not establish approval
of their type systems or justify semantic workarounds during ingestion.

## Layered matching and implemented outcomes

For a layered occurrence, match L1 first on its complete outer structure. If no
L1 matches, return unknown without an L2 search. Given L1, consider L2 templates
independently of the L1 under which they were initially stored, within applicable
source scope. Never inherit L1 or trigger/effect characteristics from an L2.

| Outcome | Meaning and assigned references |
|---|---|
| `matched to template` | A non-layered whole template matches, or L1 and L2 match independently. Non-layered results have whole only; layered results have l1/l2 and whole=None. |
| `L1` | L1 matched; L2 did not. Only l1 is assigned. |
| `unknown` | No applicable assignment, including no L1 for a layered occurrence. No assigned references. |

The owner previously proposed incomplete for structurally fitting templates with
missing/mismatched slot typing. It is not implemented. Do not manufacture it
from PARAM, punctuation, an unmatched reason or a runtime-imposed type rule.
Task 04 must identify any remaining representation decision consistently with
these latest prohibitions, rather than pretending the old type validators are
owner requirements. Literal mismatch and ambiguity are not typing failures.

## Current model use and repair consequence

The audited pipeline currently applies phrase-specific masks and rewriting,
then matches the resulting tokens. Some supplied templates therefore depend on
Python-rewritten text rather than describe native text as the owner intends.
Those templates cannot all be used as native-message templates without revising
the learning/model representation. Do not claim that removing a regex can
recover literal words or correct slots absent from the artifact.

Repair runtime processing now. Where a supplied template is defective or cannot
represent native evidence under the permitted contract, preserve the unresolved
result and file a learner enhancement request. Do not invent a replacement
structure or retain a banned preprocessing rule just to keep match coverage.
Version/format dependencies must be reported truthfully, not hidden by altered
hashes, false compatibility claims or model-loading errors disguised as unknowns.

The selected artifact is revision 43634d23e619ecb4, a conversion of source
67303093ecda779d, not retraining. It retained 889 templates after excluding two
explicitly truncated source structures. No artifact repair was performed in
this dialogue. Some learned structures are defective, as documented below.

## Evidence and implementation status

The effect/proud occurrence matches the actual effect L1
`Script system error! Error: <KEY> effect`, with stress_impact bound to KEY, and
an independently eligible L2 with proud bound to KEY. The earlier claim that
independent L2 reuse was a defect was withdrawn. The model's 238 stored pairs
contain 14 distinct L1s and 222 distinct L2s; observed reuse disproves exclusive
pairing. No trigger L1 adoption was reproduced in that occurrence.

The current v2 routing passed focused checks on genuine logs. Those checks do
not establish correctness of the still-present preprocessing and type rules.

- [Pipeline rule audit](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/PIPELINE_RULE_AUDIT.md)
- [Bug list and mandatory learner-request instructions](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/MODEL_BUGS.md)
- [Supplemental implementation task and exact files](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md)

The rule audit is evidence of current behavior. Historical recommendations in
that audit do not override the owner requirements here. The pipeline cleanup
is assigned and required; it must not be represented as already completed.
