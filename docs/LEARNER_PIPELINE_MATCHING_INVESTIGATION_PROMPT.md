# Fresh learner/runtime matching investigation

Investigate the **current** learner and classification-pipeline code that matches native CK3 error messages against template models. Establish the active execution paths independently, compare them through fresh execution on equivalent native inputs, assess correctness separately from agreement, and recommend a unified matching approach.

This is an **investigation and recommendation task only**. Do not change implementation code, templates, model rules, thresholds, assignment policy, parser behavior, model selection, or production configuration. Do not retrain, rebuild a model, publish, process pending captures, start a watcher, or run production ingestion. Investigation scripts, a short Markdown progress checklist, and generated evidence/report files may be written to a **new, uniquely named ignored directory**. Stop after delivering the findings and recommendation; implementation needs a subsequent instruction.

## 1. Start from current authority and isolate this investigation

Read repository and applicable nested `AGENTS.md` instructions, then the current project plan, status, handoff, development-environment instructions, and governing product/architecture documents. Follow relevant links from `README.md` and current handoffs. Distinguish current requirements from dated historical sections within the same document.

At prompt preparation on 2026-09-27, the checked-in selection and latest handoff identify:

- Learner **v41**, parser **ck3-lossless-v1.7**.
- Selected release **76630685c4a341ca14bf9c7c**, source candidate **007d011659a02de3c965a9cd**.
- Selected manifest SHA-256 **364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0**.
- Model schema **4**, learner feature format **v4**, assignment policy **complete-assignment-v2**, classifier **ck3-native-message-classifier-v7**.

These are navigation aids, **not assertions to preserve or a substitute for verification**. Verify the actual selection, artifact hashes, supported schemas, parser, learner implementation identity, and loaded code. If they have changed, report the change and investigate the actual current selection and compatible learner. Never silently fall back to a historical release. If current learner code cannot validly evaluate the selected release's source candidate, expose that incompatibility and the resulting comparison limits; do not bypass checks or rebuild to conceal it.

Use these currently relevant starting points, but discover actual callers and owning modules rather than treating this list as proof:

- `models/selection.json`, its selected release manifest, model and bundled executable artifacts.
- `docs/LEARNER_PARSER_PIPELINE_HANDOFF.md`.
- `docs/LEARNER_CONTINUATION_MODEL_STATUS.md`.
- `docs/LEARNER_NATIVE_MODEL_CONTRACT.md`.
- `docs/LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md`.
- `src/ck3chronicle/pipeline/MODEL_BUGS.md`, including P-04, as **dated issue leads**, not current findings.
- Learner: `tools/template_learning/evaluate_unseen_session.py`, `artifacts.py`, `records.py`, `research_matching.py`, `patterns.py`, `assignment.py`, `continuations.py`, `full_ids.py`, `owner_rules.py`, `owner_rules.json`, `publish_native_model.py`, and `parsers/`.
- Runtime: `src/ck3chronicle/pipeline/catalog.py`, `model.py`, `raw_input.py`, `classifier.py`, `matching.py`, result/binding types, and their actual application callers.

Prevent legacy contamination:

- Record Git HEAD, working-tree state, relevant source/artifact hashes, Python executable, and actual imported module paths. Use the repository Python environment and fresh interpreter processes with explicit import paths. Check for changes during the investigation that would invalidate results.
- Do not reuse previous investigation result rows, parsed records, registries, feature stores, matching caches, or verdicts as fresh evidence. In particular, prior matching-investigation reports and versioned learner research directories are not the baseline or expected answer.
- Write a fresh harness around existing entry points. Historical scripts may help locate raw inputs, but do not execute an old harness without first establishing every dependency and assumption against current interfaces. Prefer fresh minimal orchestration over carrying old adapters forward.
- Original, complete native logs remain valid inputs even if used in earlier research. Verify their provenance and hashes, then parse them afresh with the selected raw parser. Do not substitute saved recovered messages, debug projections, `native_evidence.json` message text, or hand-selected fragments for complete raw-log execution. Candidate metadata may establish provenance and model correspondence; it does not replace raw inputs.
- Do not import old template conclusions, expect old counts or outcomes, restore deprecated behavior, or use an earlier recommendation as the conclusion. Historical cases are leads to re-find in original native logs and reassess under the current contract; explicitly mark superseded or unavailable cases.

## 2. Establish both actual execution paths

Trace precisely what runs when the learner evaluates a candidate against an observed record, and when the pipeline applies the selected published model to native input. Include internal inference-time validation callers if they use different matching options or semantics from the learner evaluation entry point.

For each route identify:

- Entry points, imports, dispatch and transformations; selected parser loading; complete raw-byte input boundaries and diagnostic recovery.
- Opening bodies, wrapper contexts, ordered continuation groups, raw pieces and occurrence provenance. Establish the matching unit rather than assuming one parser emission equals one diagnostic.
- Candidate/published model loading, version/hash checks, rule sources and support statuses. Locate the selected release's exact source candidate without rebuilding it.
- Source and structural applicability, candidate indexing/filtering, and the distinction between inference-time retirement and evaluation-time eligibility.
- Literal matching, slot endpoints, constraints, declared fields and opaque full-ID captures; whole-message coverage and required wrapper/component coverage.
- Complete capture alternatives, ambiguity handling, continuation-reference checks and selection-policy inputs.
- Selection of one assignment, ranking and tie handling, selected versus alternative captures, supported/provisional/unknown outcomes, binding to original bytes, and unresolved evidence.
- Cache keys, lifetime and invalidation, including parser/model/rule/implementation identities.

Provide compact call maps with current file/function references. Separate the selected-model classifier from application/CLI/SQL callers, including callers awaiting migration. Determine what is actually active; naming a module `pipeline` does not prove the application uses it. Identify deprecated paths only to establish this boundary, not to mine them for behavior worth restoring.

The current handoff describes one selected complete supported/provisional assignment and repeatable continuation components. Verify this in code and execution. Do not impose an older rule that all competing templates necessarily remain unselected, that provisional results have no captures, or that supporting title entries are independent diagnostics. Equally, do not infer correctness merely because current documentation says integration passed.

## 3. Compare code at function level

Produce a comparison matrix covering shared functions, duplicated or substantially similar functions, learner-only behavior, runtime-only behavior, and similar-looking functions with different responsibilities or semantics. Include shared source imports versus separately loaded, hash-covered copies of executable helpers.

For each meaningful difference state:

1. What each function does and where it is called.
2. Whether it belongs to matching, learner inference, assignment policy, runtime orchestration, or result presentation.
3. Whether it can affect eligibility, captures, alternatives, ambiguity, selection, support status or final outcome.
4. Its likely benefit or harm and supporting evidence.
5. Whether that assessment is confirmed by execution, a code-review hypothesis, or a legitimate difference in responsibility.

Identify rules imposed independently of the supplied model. Determine whether observed values, inferred positions, selection evidence, member records, declaration registries or mutable global rules influence evaluation, and distinguish that from their use during inference. Do not assume additional validation improves correctness, simpler code is authoritative, or duplication proves behavioral divergence.

## 4. Execute a controlled comparison using current native evidence

Before looking at results, record the input-selection policy and inventory:

- First use **all available complete logs supporting the selected release**. The latest handoff currently describes thirty training logs; derive the actual set from verified provenance rather than hard-coding that count.
- Add available complete native logs outside that training set, identifying origins, overlap and selection rationale in advance. Include available continuation-bearing logs and other structural variety. Do not select only inputs known to agree or disagree. Separate training evidence from additional-log evidence and do not claim an untouched holdout unless established.
- Record missing/inaccessible inputs and access restrictions explicitly. Do not replace them with derived text or manufacture native variants. Continue comparisons that remain valid and bound conclusions accordingly.

Run existing processes without modifying their implementation. Establish input equivalence before attributing any difference to matching:

- Same raw bytes and selected parser implementation/hash, recovered diagnostics, pieces, wrappers and ordered components.
- Corresponding candidate/release templates: literal parts, constraints, source/structure declarations, continuation contracts, support statuses, selection policy and executable helpers.
- Separate inference-only metadata from executable matching/selection data. Explain compact-publication transformations and verify that apparent equivalence includes fields that influence outcomes.
- Expose mutable learner rules/code versus immutable published artifacts. Use normal loaders and version checks; do not patch globals, remove fields, manually construct a supposedly compatible runtime model, replace rules, or suppress compatibility failures to obtain parity.

Execute the public learner evaluation and selected runtime routes where available. Read-only calls to existing lower-level functions may supplement them to expose candidate decisions that public results omit; label these diagnostic probes and do not substitute their output for the actual route's outcome. Do not reimplement either matcher in the harness. If a route does not expose rejection reasons or all alternatives, state that limitation and identify what the supplemental calls establish.

Compare and preserve:

- Recovered messages, contexts, complete-group membership and unmatched/unresolved raw evidence.
- Applicable/filtered candidates, complete matches and rejections; all exposed capture alternatives and candidate competition.
- Inputs to the selector, selected assignment, ranking/tie evidence, wrapper/component matches and outcome.
- Slot names/types/values, original raw pieces, region-relative boundaries and absolute byte spans for **each occurrence**, including `continuation:N` regions and empty/absent fields.
- Exceptions, unsupported structures and evidence retained for unresolved review. Inspect preservation without invoking production ingestion or SQL.

Keep parser-emission counts, complete-diagnostic occurrence counts, distinct native message counts and distinct contextual/grouped-record counts separate. Define every deduplication key. If matching runs once per identical complete record, disclose that optimization, establish that the key includes all matching inputs, and verify occurrence-specific absolute bindings against each original log. Do not describe weighted counts as independently executed calls.

Store source log hashes, native spans, environment/artifact identities, commands, scripts and machine-readable results in the new ignored directory. Make the report reproducible without including captured logs or generated evidence in Git.

## 5. Assess correctness independently of agreement

Inspect every distinct disagreement category, representative agreements, frequent results, rare structural outliers and previously documented cases that still have identifiable native witnesses. Include ordinary bodies, wrappers, relevant slot types, unknown/provisional outcomes, and complete continuation groups where present. If a requested behavior such as malformed continuation handling or capture ambiguity has no native witness, say so; do not invent one.

For each important example show together:

- Source, original native message and complete relevant wrapper/continuation content; log hash and original spans.
- Readable current template with `<KEY>`, `<PARAM>`, `<LOCATOR>`, `<CHARACTER_FULL_ID>`, etc., plus relevant constraints/status. Keep explanatory repeat notation separate from native text.
- Learner and runtime alternatives, selected results, outcomes and captures.
- Relevant raw pieces and exact byte boundaries, including per-component regions.
- Which interpretation the native wording and current model contract support, or why evidence is insufficient. Distinguish correct application of a questionable template from a matching implementation defect.
- Exact code responsible for a difference, or the model/parser/data difference that prevents attributing it to matching.

Higher coverage, repeated occurrences and agreement do not establish correctness. Unknown and provisional are legitimate results. Distinguish model quality, parser recovery, matching semantics, selection policy, and caller/presentation errors. Reassess historical issue statuses; do not presume old defects persist or old closure claims remain valid.

## 6. Recommend a unified approach and staged verification

Use current code review and fresh evidence to recommend:

- Which mechanics should have one implementation, including complete literal/slot matching, applicability, wrapper/component completeness, alternatives and selection where appropriate.
- Which inference, evidence generation, model publication, runtime orchestration, binding and presentation responsibilities should remain separate.
- The owning module and concrete callable interface, including inputs, outputs, ambiguity/selection semantics, provenance and errors.
- How unpublished candidates and published models use it without importing learner inference into runtime or invoking SQL/ingestion during learning.
- How parser identity, model-declared rules, support/selection evidence, frozen executable helpers, caches and compatibility/version checks work together.
- Useful behavior to retain, defects to correct, and unjustified behavior to remove, distinguishing demonstrated defects from unresolved hypotheses.

Do not automatically designate either existing matcher or an earlier proposal as authoritative. Explain why the recommendation follows from the current evidence. Provide a staged migration and native-log verification plan with explicit success criteria for eligibility, complete coverage, alternatives, selection, status, exact captures, byte preservation and caller integration. Require independently justified differences rather than blanket parity or higher-match-rate targets. No migration is authorized in this task.

## Deliverables

Maintain a short Markdown progress checklist. Deliver a report that leads with findings and their limits, followed by the verified version/input ledger, compact call maps, function-level comparison matrix, execution results, inspectable native examples, recommendation, staged success criteria and unresolved questions. Link the report, scripts and evidence artifacts in the final response.

Clearly separate fresh observations, code-derived conclusions, historical claims and untested hypotheses. State any comparison prevented by missing inputs or compatibility checks. Do not let an unavailable artifact justify silently using a legacy route. End with findings and recommendations only; do not implement changes.
