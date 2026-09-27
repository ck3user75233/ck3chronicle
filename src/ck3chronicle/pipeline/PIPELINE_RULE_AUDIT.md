# Pipeline rule audit: supplied templates define slots

Date: 2026-09-17. Investigation only; no production source/model repairs in
this pass. The prior owner-authorized v2 routing change remains in place.

Subsequent owner direction now requires cleanup in the pipeline exercise.
[TASK03_CLASSIFICATION_HANDOFF.md](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md)
assigns it as an explicit implementation supplement to the paused Task 04 agent.
The owner's prohibition on phrase rules and restrictions beyond the supplied
template supersedes any narrower repair recommendation in this historical audit.
PARAM is a valid variable-phrase slot; it is not automatically missing typing.

## Owner boundary

The supplied template defines its literal content, slot count, slot order and
slot types. One KEY position binds one complete original key value, including
its punctuation and numeric components. Tokenization does not authorize
inventing multiple keys or substituting a Python-defined error grammar.

Scope: inspected the pipeline's emission recognition, diagnostic recovery,
normalization, alignment, acceptance, binding, model loading and selection.
This is a local source audit with focused genuine-log evidence. It does not
establish that every affected grammar has been exercised or that all templates
are semantically correct. No learner refactor or model repair was performed.

## Confirmed findings

### P-03 (extended): runtime KEY rules are an independent, restrictive definition

[classifier.py:32](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py:32)
accepts only a hard-coded subset of raw token spans as KEY. Every meaningful
token must match a letter/underscore-start identifier pattern. Additional
rules use a four-token cutoff and punctuation/digit/capitalization heuristics.
These constraints do not come from the supplied template's KEY position.

Conversely, the same predicate can accept several whitespace-separated words
as one KEY. Its input omits whitespace boundaries; punctuation is filtered
before type checking. This is not a consistent implementation of the owner's
one-complete-key-string concept. Original whitespace remains available in the
value map, so losing it from type decisions is not a loss of native evidence.

Prior full-path controls established that single-KEY templates reject genuine
eps_travel_event.01 and char_interaction.0170.t. Bypassing only KEY acceptance
allows both to align and bind their complete original values. See the compound
key report linked below. It was an isolated diagnostic control, not a fix.

### P-05: normalization decides multiple key positions before model matching

[normalization.py:661](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py:661)
`_Composer.key_path` splits a script expression on periods, masks every segment
as KEY, and inserts literal dots between the markers. It also treats scope,
var, cp and title prefixes as fixed namespace grammar. This operation receives
no candidate template. It runs from `_Composer.structured` before classification.

Real protected log B, native emission starting at line 4747:

```text
Script system error! Error: capital_county.kingdom trigger [ Failed context switch ]
```

Current normalized outer structure:

```text
Script system error ! Error : <KEY> . <KEY> trigger
```

With the selected model, runtime assigns the split template and binds
capital_county and kingdom separately. This does not prove that decomposition
is empirically justified: Python had already imposed it on the occurrence.
The artifact also contains split templates, so the audit is not claiming the
classifier silently edited their stored tokens.

More decisively, the model already contains entry `9b8215b4dc87ccfc`:

```text
L1: Script system error ! Error : <KEY> trigger
L2: Failed context switch
```

Using that unchanged entry as the sole candidate for the unchanged real
occurrence gives unknown. Bypassing only key_path masking in memory makes the
same template match and bind capital_county.kingdom as one original KEY.
The type predicate and template were unchanged in this control. Thus the
pre-match slot decomposition itself blocks a supplied single-KEY template,
independently of the numeric-fragment issue.

### P-06: phrase-specific masks give identical values different acceptance

[normalization.py:613](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py:613)
contains message-specific recipes for events, localization messages, shaders,
meshes, effects and other text. They designate KEY, OPTIONAL_KEY, TYPE and PARAM
positions before a model template has been selected.

[classifier.py:33](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/classifier.py:33)
unconditionally accepts a normalized marker identical to the template marker.
Consequently the same complete event identifier receives different treatment:

- Log B line 2477 is `Event enfp_test.0001 is orphaned`.
- A phrase-specific rule converts it to `Event <KEY> is orphaned`.
- The selected model matches and binds enfp_test.0001 correctly.
- Feeding that same original identifier through the raw KEY predicate fails
  because its separate 0001 token is not a letter-start identifier.

The value is not intrinsically unrepresentable. Its acceptance depends on
which hard-coded sentence recipe ran first. The model alone is not deciding
the applicable slot structure and type interpretation.

### P-07: normalization also removes literals and inserts optional slots

[normalization.py:680](C:/Users/nateb/Documents/ck3chronicle/src/ck3chronicle/pipeline/normalization.py:680)
contains structured rewriting recipes. In the real log B line 4904:

```text
Removing travel plan from the character Ci Faj of (Internal ID 296591) owner when the travel plan is not ending normally.
```

The normalized portion becomes:

```text
... character <KEY> ( <KEY> <OPTIONAL_KEY> ) owner ...
```

Runtime binds KEY values `Ci Faj of` and `296591`, plus an empty OPTIONAL_KEY.
The words Internal ID have disappeared from matching text and an absent
historical-ID marker has been inserted. Native bytes are retained, but Python
has imposed slot/type choices and changed the matchable literal structure.
The current model expects this normalized form; that dependency is precisely
why simply changing a learner template cannot always repair runtime behavior.

Another real example, log B line 7995, contains comparison categories flag and
boolean. `_Composer.structured` labels both KEY through a message regex rather
than consulting a candidate template. This audit does not prescribe replacement
types for character displays, IDs or categories; it identifies where those
decisions currently come from.

### P-08: invalid namespaced expression can lose its prefix

Source-level finding, not reproduced in the three inspected real logs:
`_Composer.key_path` peels a recognized namespace prefix at lines 665-669;
if the remaining segments fail its predicate, line 672 returns only the peeled
remainder. The namespace is then absent from matching text. The original
diagnostic still retains it. This branch should not alter literal content merely
because the key grammar did not accept an expression. No synthetic occurrence
was introduced to claim this is an observed production failure.

## Other active rules and their boundary

| Component | Rule and assessment |
|---|---|
| classifier.py:56, `_align` | Full ordered literal matching and multi-token variable spans. This mechanism already supports one slot spanning punctuation. It does not itself split a model slot into multiple bindings. Keep complete coverage and explicit ambiguity handling. |
| classifier.py:145 candidate selection | Rejects competing templates or multiple alignments. This preserves uncertainty; do not replace it with arbitrary template selection when broader KEY matching reveals overlap. |
| classifier.py:164 routing | L1 gates L2, independent L2 reuse follows, no L2-only result. This is the recently implemented owner direction. |
| classifier.py:35-53, other slot predicates | TYPE/OPTIONAL_KEY require normalized markers; VALUE uses a digit/simple-decimal test after punctuation filtering; LOCATOR requires masks; PARAM accepts any nonempty token span; ALT enforces a stored closed set. These are implementation-defined type rules. ALT is already rejected by the owner as a slot type; its replacement remains deferred. |
| normalization.py:735, locators | Broad path/filename/line patterns mask text before matching. Adjacent locator markers collapse at lines 825-827. Evidence extraction can be useful, but extraction does not authorize overriding the type or boundaries declared by a candidate template. No new erroneous locator assignment was demonstrated here. |
| normalization.py:812, script-location tail | Removes recognized trailing location text from matching while retaining its original value. This is a representation rule requiring an explicit shared contract, not learned per-template slot discovery. |
| normalization.py:740, persistent clauses | Removes near-line text and maps selected clause grammars to one or two KEY markers independently of a model. Include this in the template-authority repair scope. |
| emissions.py / diagnostics.py | Recognize native headers, preserve spans, recover known persistent-reader child boundaries and collapse whitespace in the matching view. These operations concern evidence/diagnostic boundaries. The audit did not establish that they should be removed with semantic slot rewriting. |
| bindings.py:174 | Constructs one preserved original value per matcher-supplied slot span. It preserves punctuation and interior whitespace and does not invent additional model slots. Genuine one-slot compound-key controls succeeded through this code. |
| model.py / catalog.py | Validate and pin stored artifacts, supported schema and marker vocabulary. Do not learn or rewrite templates during load. The artifact's versioned representation can still encode an unsuitable type system; integrity checks are not semantic approval. |

`diagnostic_lead`, `reason_lead` and the standalone `normalize_key_path` helper
exist in normalization.py, but the active classifier does not use the lead
functions. The operative key-splitting method is `_Composer.key_path`.
Do not attribute runtime classification to unused copied helpers.

## Repair boundary recommended by this audit

1. Match the supplied literal/slot structure against evidence that has not
   already been assigned competing semantic slots by Python message recipes.
2. Bind each model slot to its complete original span. Punctuation inside a
   KEY remains part of that KEY unless the template itself declares it literal.
3. Treat type checks as the agreed interpretation of declared model types,
   not heuristics copied from learner inference or a second slot-discovery system.
4. Preserve diagnostics, source partitions, literal equality, L1/L2 routing,
   explicit ambiguity and exact original-value binding.
5. Reconcile current artifact assumptions with any normalization change rather
   than silently rewriting a supplied template or choosing a convenient model.

This is a pipeline correctness issue, even where rules were copied from learner
code. Sharing those rules would only make their assumptions consistent; it
would not establish that the model controls slots. Comments calling a port
authorized do not establish owner approval of these semantic rules.

The current model includes structures built around these recipes. Their safe
replacement therefore needs explicit handling of that representation dependency;
this audit does not claim that deleting every normalizer regex is a complete fix.

## Evidence and scope of changes

Real log B is the retained rehearsal copy under session
`1fc0ecb983d7c3726d880384a38581e6c6daa6c58870f0cbc01e6e1857e7c7d2`.
No captured log, model artifact or Python product source changed in this audit.
The experimental bypasses affected only the local investigation process.

- [Rule effects and existing-template control](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/check_model_authority.json)
- [Reproduction script](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/check_model_authority.py)
- [Normalization examples from genuine logs](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/normalization-rule-audit.json)
- [Earlier compound numeric KEY control](C:/Users/nateb/Documents/ck3chronicle/.codex-tmp/pipeline-review/check_compound_key_rejection.json)
