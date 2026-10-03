# Task 04(B) — Pipeline processing audit results

**Subsequent disposition:** owner review and shared-matcher delivery/verification
are complete. [Revised Task 05](05_ERROR_CONTRACT_IMPLEMENTATION.md) now owns
package integration, selected-only binding, duplicate matcher retirement and
Error Contract helpers. The findings and proposed dispositions below preserve the
original read-only audit; its closing review hold is historical, not a current
execution gate.

2026-09-27. Read-only investigation of the current checkout, under
[the audit commission](04B_PIPELINE_PROCESSING_AUDIT.md). No repairs or Task 05
implementation were performed.

**Finding:** the selected classifier applies the pinned parser, published
declarations and published selector directly. Source tracing and native replay
found no additional phrase rewriting, slot masking, learner inference,
reclassification or learner-style regrouping on that path. It does, however,
bind candidates and then bind the selected captures again. Historical framing
code remains callable by a research comparison tool, and application commands
still use the older parser/classification/projection stack. These are separate
cleanup and cutover concerns; the selected API is not yet the application pipeline.

## 1. Actual selection and call map

The selection is unchanged from the handoff: **76630685c4a341ca14bf9c7c**, model
schema **4**, parser **ck3-lossless-v1.7**, selector **complete-assignment-v2**,
classifier **ck3-native-message-classifier-v7**. Loading through
`pipeline.catalog.load_selected_classifier()` verified the manifest and all seven
release artifacts. The model contains 418 templates: 405 ordinary, 12 wrapped,
and one continuation template.

| Selected item | SHA-256 |
|---|---|
| `models/selection.json` | `8d304c2cc178909347b21367f0f746467e37a70cda32e1c6af5e0e1d21656fb4` |
| Release manifest | `364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0` |
| Model JSON | `897468f7b247c96ea29d7b28c944de1ff65c46e429ac6e06efebfbe93a6bf0db` |
| Parser | `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |
| `assignment.py` | `29e3bc8f54ac678988a3dc3e0023ce7c1dc76403900a44805ef958fbd47be235` |
| `continuations.py` | `76148141951682ca47542776b34a65d2fac3142089de7560338d688646222053` |
| Released owner rules | `3d7e3da60625554f67f9ebf258514172c12a6c5315acb30fe7309f2db340fc77` |

References below use current file line numbers, not the historical audit's lines.
`pipeline/` means `src/ck3chronicle/pipeline/`; release files are under
`models/76630685c4a341ca14bf9c7c/`.

1. **Load:** [catalog.py](../src/ck3chronicle/pipeline/catalog.py),
   `load_selected_model` (17), resolves selection and calls
   [model.py](../src/ck3chronicle/pipeline/model.py), `load_model` (212).
   The loader checks hashes, canonical model identity, schema, parser agreement,
   owner-rule agreement, constraints and complete component declarations. It
   executes hash-verified assignment/component helper bytes (256–259), freezes
   model data, partitions templates by source, and loads the pinned parser (284).
   Source-checkout versus installed-resource lookup changes location, not revision.
   No historical model is substituted when this load fails.
2. **Frame and recover:** [classifier.py](../src/ck3chronicle/pipeline/classifier.py),
   `read_log` (27), calls `SelectedParser.parse_file/parse_bytes`
   ([parser loader](../tools/template_learning/parsers/__init__.py), 63/67).
   Release `parser.parse_bytes` (524) frames original bytes; `recover_log` (410)
   calls local `recover_messages` (342) or the embedded cross-emission rule.
   `raw_input.iter_diagnostics` (20) dispatches this stream through
   `template_learning.parsers.iter_recoveries` (18), preserving complete groups.
   `_region` (15) requests the parser's token/gap pieces. Wrapper prefix/suffix
   ranges are selected from parser-established boundaries, not recovered again.
   Source-family removal of the terminal C++ line number is parser framing;
   the original `source_tag` remains available.
3. **Applicability:** `Classifier.classify_raw` (36) and `classify` (88) check the
   parser pin and complete context. `_match_content` (42) calls
   [matching.py](../src/ck3chronicle/pipeline/matching.py), `Rules.structure` (274).
   Candidates must agree on source, context kind, construction and ordered
   parameter structures; unresolved templates are ineligible. The controlling
   declarations are the release's `owner_rules.constructions`,
   `parameter_structures` and each template's corresponding references.
4. **Complete matching:** `Rules.analyze` (319) walks unchanged literal/slot
   `parts`, requires complete text consumption, and retains all capture witnesses.
   Optional branches come only from `part.optional`; prefix/suffix and native
   spacing remain exact. Parser boundaries, KEY joiners, numeric/line grammar,
   location syntax, literal guidance/punctuation, balance, declared REASON and
   full-ID checks implement the supplied constraints. `slot_position_cues` supplies
   the location declarations. There is no ordinary KEY-to-PARAM fallback or
   independently imposed old `_accepts` predicate.
5. **Components, selection and binding:** `classify` (104–127) calls released
   `continuations.match_components` (32) for every opening witness: all entries,
   their literal layouts, minimum count and exact opening-reference equality must
   pass. It builds relative eligible assignments and separately binds all candidate
   witnesses through `_bind` (78) and `bindings.bind_captures` (5). At line 128 it
   invokes released `assignment.select_assignment` (32). That helper ranks exported
   `selection_evidence` using `assignment_policy.metrics`, resolves all complete
   body/wrapper alternatives, and returns one assignment. It does no inference.
   Lines 132–138 bind the selected captures again. Lines 139–145 translate the
   selector's final status and return `NativeClassification`; no subsequent
   classifier, normalizer, projection or aggregator runs.

The parser's embedded recovery JSON, lexical exceptions and framing expressions
are hash-covered parser behavior. They are not an additional application policy.
Likewise, the full-ID emitter patterns are explicit released declarations, not a
new name recognizer invented by the pipeline.

Two active dependencies live in the learner package but are ordinary application
code, **outside the release artifact hashes**:

| Dependency | Responsibility and application-source SHA-256 |
|---|---|
| `tools/template_learning/parsers/__init__.py` | Local hash-verifying parser loader and explicit recovery API dispatch. `29fbaa2236b700570439f99ccb0186b051577ae595e5740c7cbc2164e964e6e7` |
| `tools/template_learning/full_ids.py` | `FullIdRules` consumes only the supplied `parameter_structures`; checks whole opaque spans without ID resolution, dictionaries or capitalization rules. `d91a646cde7887c5fe497e4c76a4bd4cd5ca59277c06c55995cdb5116d22dc28` |

`matching.py` is also application code, hash
`8470781bdfe1dafee3719964a93e15249456ed6ac1f68b9cc822c37079de4b22`.
Neither runtime helper imports mutable learner owner rules, inference, registries
or research matching. Released inference-policy/wording-loss/label-equivalence
metadata is not run as another classification stage. Application revision remains
necessary lineage alongside the model manifest.

**Caches:** `_match` is a 4,096-entry, classifier-instance LRU over source, kind,
exact body text/pieces and complete wrapper content. It stores relative assessments,
not absolute bindings or final groups. Components are checked on every occurrence,
so entries omitted from that opening-cache key are not silently reused.
`Rules.analyze.visit` memoizes only within one match. `FullIdRules.inspect` and
`capture_ends` use 16,384-entry caches including the rules instance and exact
pieces/source/definition as applicable. The parser caches scanner expressions
(64 entries) and its module by verified digest. No persistent assignment cache,
cross-model reuse or post-selection transformation was found.

## 2. Findings and proposed disposition

All repairs below are proposals for joint owner/Task 04 review, not authorization.

| ID; behavior/location | Classification; evidence and consequence | Smallest proposed action; affected callers; Task 05 impact |
|---|---|---|
| F1. Direct declared matching, shared full-ID mechanics and released selection | **Required mechanic.** The call map and replay preserve exact parts, source applicability and every chosen capture. Multiple candidates are considered within the published selector; 1,032 native results exercised evidence ranking. No extra active semantic stage was established. | Keep these mechanics. No matcher unification, learner-code port, policy rewrite or model republish is justified by package location or similar code alone. **No effect** on Task 05 beyond consuming the existing result. |
| F2. Candidate binding followed by selected binding, `classifier.py:121–138` | **Redundant non-semantic work, observed.** 101,024 candidate-region binding calls plus 99,567 selected-region calls. Every selected region was already present among bound candidates; the second pass repeated span/value validation and object construction without changing selection. Bound candidate objects are not the selector's input. | Task 04: select the exact already-bound witness using the published choice, including wrapper alternatives and components. Do not choose the first candidate or bind again in contracts. This affects `classify`/`classify_raw`; no tracked source/research reader of `.candidates` was found. Removing research alternatives would be a separate API decision. **Proposed prerequisite repair** to the no-duplicate-pass objective, owned by Task 04; moving it into Task 05 needs explicit agreed scope. |
| F3. Repeated construction recognition, `matching.py:199,217,274` | **Redundant non-semantic computation.** `structure` calls `recognize`, then `field_ranges` calls it again; declared captures resolve the same declaration during matching. Observed 4,850 structure calls and 10,335 recognitions. These are checks of the same definitions, not new typing or a second raw parser. | Optional Task 04 mechanical reuse of a recognition result within one assessment, preserving native-piece checks. No correctness repair demonstrated. **Independent cleanup**, not a Task 05 prerequisite. |
| F4. Historical emission/recovery/view modules and types | **Inactive remnant relative to selected execution; callable research dependency.** `emissions.py:36,168`, `diagnostics.py:39`, `normalization.py:25` remain. The old recovery still recognizes specific persistent-reader phrases and collapses whitespace. `build_parser_comparison.py:23–26,189,204,207` directly uses all three. None loaded or ran in native selected replay. | Task 04 plus learner/review-tool owner: retire the comparison tool's live old-baseline path (preserve existing ignored historical evidence), then delete obsolete modules and historical types together. Do not copy their recipes into the selected path or keep a compatibility wrapper. **Independent cleanup**, outside current Task 05 deletion scope. |
| F5. Application providers still use the old stack | **Later cutover concern, source-confirmed.** CLI parse/classify/process/backfill commands reach `parser.service`, `classification.catalog`/`service`, and `semantic_projection_service`, not `pipeline.catalog`. The old catalog hardcodes model `67303093ecda779d`; reports read semantic-projection records. These paths would use old interpretation if invoked, but were not executed here. | Application/storage team: explicitly replace provider, storage and report edges after contract/storage delivery, then retire old classifier/parser/projection paths and their old model dependency. Never insert semantic projection after the new selected result. **No change to Task 05 scope**; later application cutover. |
| F6. `DeclarationBoundaryError` becomes unknown, `classifier.py:71–75` | **Unverified error-disposition concern in reachable code.** The catch handles unsupported native declared ranges, but also `matching.py:191`'s overlapping declarations. The latter is a definition conflict, unlike ordinary unmatched input. No declaration exception occurred; the selected two construction declarations explicitly exclude overlap. This is not an observed dropped assignment or fallback classifier. | Task 04/contract integration owner: distinguish definition/programming conflicts from reviewable native boundary limitations; propagate the former explicitly while retaining evidence for the latter. Do not remove all boundary-review handling. **Possible bounded contract integration correction**, only if joint review assigns it; no demonstrated prerequisite failure for this pin. |
| F7. Contract-ready serialization, identity and SQL records absent | **Later implementation concern, expected boundary.** Selected results plus model definitions contain the necessary native data, but no `pipeline/contracts.py` or finalized new SQL record exists. | Task 05 owns contract/result preparation, identity and standalone rendering. Later teams own within-Run exact-identity counting, SQL, review shards and stored reports. **Task 05's existing scope**, not an unauthorized semantic stage or general audit repair. |

**Retirement/caller inventory.** Historical `domain.py` types are `TokenSpan`,
`SourceProvenance`, `Emission`, `EvidenceScope`, `EvidenceSpan`, `OccurrenceValue`,
`RecoveredDiagnostic`, `MatchingToken`, `NormalizedValue` and `NormalizedView`
(lines 30–204). Their in-repository consumers are the historical three-module
chain and `build_parser_comparison`; retain `ByteSpan`, `OriginalAccess` and the
native types. `normalization.tokenize` has no source/research caller found.
`raw_input.read_raw_log` (10) is a documented convenience loader with no Python
caller found; it invokes the same pinned parser, not a parallel implementation.

Other research callers are `review_assignment_changes.py:14–15,59,78`, which
constructs the current classifier around an explicitly supplied research bundle
and calls `_match_content`, and `inspect_cross_emission_recovery.py:111–138`, which
uses `iter_diagnostics` and `bind_captures` for parser-range inspection. Their
research orchestration is not reachable from selected classification. The shared
parser dispatcher's explicit v1.6 branch serves other explicit parser selections;
v1.7 does not fall back to it. No research tool was executed in this audit.

Application call edges inspected: `cli.cmd_parse:682`, `cmd_classify:724`,
`cmd_process_one_pending:1499`, `cmd_backfill_session:1617`; registered command
handlers at 2500, 2517, 2623 and 2641. The unregistered
`_cmd_process_pending_wide_legacy:1234` is a separate retained remnant.
`processing.py:16–34,899–960` reaches parse/classify/project services;
`classification/catalog.py:13,80` supplies the old runtime;
`reporting.py:99–108` requires old projection storage. Caller reachability does
not authorize production processing or establish old semantics as requirements.
The import inventory records 47 relevant edges across 112 source/research Python
files; it excludes tests as requirement sources.

## 3. Reconciliation of Task 04 cleanup obligations

| Obligation | Status and current evidence |
|---|---|
| Preserve native framing, source and original correspondence | **Satisfied on selected path and replay.** Every input byte and emission accounted for; exact bindings, wrapper regions and grouped entry provenance retained. |
| Remove `_Composer` phrase recipes, preassigned markers, literal removal, optional-slot invention and prefix peeling | **Satisfied on selected path.** Those Python symbols/recipes are absent from current pipeline code; no old normalizer import/call. Native reconstruction checks all selected regions. F4 means historical recovery/view retirement is not complete repository-wide. |
| Remove old `_accepts` lexical restrictions; model owns complete KEY/PARAM boundaries | **Satisfied on selected path.** Current checks are serialized constraints and published grammar. Native `char_interaction.0170.t` binds as one KEY; multiword PARAM and opaque full-ID examples retain their original values. |
| Match complete literals/order and preserve surrounding locations/reasons | **Satisfied for exercised assignments.** 99,567 selected regions reconstruct exactly. REASON is not independently classified; LOCATORs and wrapper layouts remain explicit. |
| One processing path; no duplicate raw recovery/matching/binding | **Violated for binding** (F2). **Satisfied for observed raw recovery/lexing and selected execution:** no second lexer or recovery path ran. Candidate search and required declaration validation are not reclassification; F3 records repeated computation precisely. |
| Remove additional interpretation/reclassification/regrouping | **Satisfied within selected path examined.** No learner inference or union/regrouping calls. Pinned cross-header recovery and exact-identity downstream occurrence counting are approved mechanics. **Application-wide cutover remains outstanding** (F5); do not label the whole product cleaned. |
| Retire obsolete implementations and affected callers | **Violated/incomplete repository-wide:** F4 and F5. Actual callers are identified above; merely bypassing them does not establish removal. |
| Preserve unresolved evidence; failures explicit | **Satisfied for 9,153 native unknowns and ordinary explicit integrity checks by inspection. Unverified** for naturally unavailable parser-unresolved/declaration-failure branches; F6 identifies a specific exception-disposition question. No corrupt-artifact or synthetic rejection proof claimed. |
| Historical L1-first / independent L2 behavior | **Superseded, not a repair target.** Current owner contract requires one complete assignment with intact REASON and components. No L1/L2 compatibility stage should be restored. |

## 4. Contract readiness

`NativeClassification.selected` supplies one complete `CandidateMatch` for full
and provisional outcomes. Opening/template and selected wrapper IDs identify exact
model `parts`; native bindings carry region, positional name, type, original value
and absolute span. `None/None` is absence; present empty values can retain non-null
zero-width spans. `NativeDiagnostic` preserves source family/tag, body/context
ranges, group emission ordinals and each supporting entry's original range/tag.
The final outcome, not merely template support, controls reporting status.

Ordered components retain the repeated reference and title PARAM. The current
continuation definition has exactly one literal layout, so it is unambiguous;
`RegionMatch` does not independently export a component-layout index. Task 05 can
materialize that existing layout without another native match. Multiple declared
component-layout alternatives were not exercised and must not be claimed as
verified representation coverage.

Thus the current definition/result pair can supply the approved representation.
It is not already a serializable standalone SQL diagnostic: common-rules lineage,
definition/value serialization, selected-layout representation, deterministic
identity and model/log-independent rendering remain Task 05 work. Counts,
publication and SQL/report integration remain later work. This audit's literal
reconstruction checks are verification only, not delivered contract helpers.

## 5. Native evidence and limits

Complete inputs are below; each filename is `error.log` inside its SHA-256
directory under
`.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/`.
Both entry and exit hashes matched these exact values:

- A: `10cbdcb23e34a5b571a16eb52d390e5e676663936f000fd43404af19d85027fb`
- B: `9d3622ab1b6c85cbab45d83767bb870b06c6fb9d6da50ee44f5eba3674d98cbc`

| Fresh observation | A | B | Total |
|---|---:|---:|---:|
| Input bytes | 10,369,025 | 6,233,007 | 16,602,032 |
| Native emissions | 74,858 | 23,503 | 98,361 |
| Results | 76,509 | 24,112 | 100,621 |
| Full | 49,560 | 14,600 | 64,160 |
| Provisional | 26,949 | 359 | 27,308 |
| Unknown | 0 | 9,153 | 9,153 |
| Parser-unresolved results | 0 | 0 | 0 |
| Present selected bindings checked | 97,815 | 75,432 | 173,247 |
| Absent bindings | 3,000 | 1,350 | 4,350 |
| Selected regions reconstructed | 81,786 | 17,781 | 99,567 |
| Complete groups / supporting entries | 9 / 11 | 2 / 2 | 11 / 13 |

Command: `.\.venv\Scripts\python.exe -I -B -u .ck3chronicle/wip/task04b-audit/replay.py`.
The observer uses `sys.setprofile` on genuine calls/returns; it replaces no
function, policy or candidate. Each release selector return was compared directly
with the classifier's selected template, status, layouts, values and converted
absolute spans: **91,468 unchanged complete assignments**. All 100,621 classified
messages invoked the selector once, including unknowns. Both logs were parsed
once in this replay. Recovery partitions covered original bytes contiguously and
every emission ordinal exactly once. Wrapped children explain multiple results
per emission; supporting entries stay within their one group.

There were 104,174 lexical calls and **zero repeated lexical ranges per input**.
The opening match cache finished with 96,559 hits and 4,062 misses; each miss used
the same frozen model/rules. Native module traces contain only the selected pipeline,
pinned helpers/parser and neutral `parsers`/`full_ids` modules, with no historical
normalizer, learner inference or application projection execution. The measured
200,591 binding calls split into 101,024 candidate calls and 99,567 repeated
selected-region calls. Every latter result equaled an already-bound candidate
witness. These observations distinguish duplicated work from altered meaning.

Additional bounded native witness inspection used the same complete A input and
unchanged classifier (601 selected native-message inspections; separate from the
table). It verified KEY `char_interaction.0170.t`, emission 59, bytes `[7178,7201)`;
multiword PARAM `(no character)`, emission 46270, bytes `[4432300,4432314)`; and an
intact character full ID containing `Internal ID`, emission 45953, bytes
`[4358672,4358733)`. The exact historical `capital_county.kingdom` witness was not
established by that bounded inspection; its earlier audit result is not treated
as a fresh check. A's emission 216 also preserves the complete pipe-containing
PARAM `LOD_0|decal_world|decal_worldShape`. All selected literal layouts, including
native spacing and line endings, reconstructed without rewriting.

Groups use template `0875e8c46afb0b47271a8341`; A includes two-entry groups at
emissions 47026 and 47037. B's two repeated groups start at 2652 and 4794, with
different source offsets. No group entry was emitted as an independent result.
No aggregation or SQL database was created.

Limits: eight of nine declared slot types were exercised; HOUSE_FULL_ID was not.
No accepted present-empty REASON, capture ambiguity, selector evidence tie,
malformed/unassociated continuation, parser-unresolved outcome or declaration
exception occurred. Competing candidates did occur (1,032 results), resolved by
published evidence ranks without a tie. Installed-wheel execution, external
callers, corrupt artifacts and unsupported schemas were not exercised. No new
log was added solely to increase coverage. Exact reconstruction demonstrates
execution fidelity, not semantic correctness of every learned template or
accuracy on unseen CK3 formulations.

Audit evidence, all ignored and task-owned under
`.ck3chronicle/wip/task04b-audit/`:

- [replay.py](../.ck3chronicle/wip/task04b-audit/replay.py): complete native observer.
- [replay.json](../.ck3chronicle/wip/task04b-audit/replay.json): exact input paths,
  hashes, counts, recovery accounting, call sites, module paths, cache observations,
  group content, binding examples and result digests.
- [witnesses.json](../.ck3chronicle/wip/task04b-audit/witnesses.json): additional
  original-byte witnesses above.
- [import-edges.json](../.ck3chronicle/wip/task04b-audit/import-edges.json): current
  pipeline source/research import edges.
- [entry.json](../.ck3chronicle/wip/task04b-audit/entry.json) and
  [exit.json](../.ck3chronicle/wip/task04b-audit/exit.json): scope comparison.

## 6. Unchanged scope and stop

Entry: branch `main`, HEAD `2993144e061681c5651e3e18be1290c957d4892d`.
The pre-existing worktree had ten modified files and five untracked documents,
recorded verbatim in `entry.json`. The baseline was captured after read-only
orientation and before replay; it hashes all 265 tracked/nonignored existing
files, including untracked documents and all source/model files.

Exit comparison preserves all 265 baseline file hashes: 68 under `src/`, 57
under `tools/`, 41 under `models/`, and all other baseline files. HEAD and the
pre-existing Git status entries are unchanged. The sole new nonignored file is
this report. Task-owned observer/evidence files are ignored; both captured logs
retain their entry hashes. No code, parser, learner, model, selection, prompt,
other documentation, database or captured log was changed; no watcher, production
processing, commit, push or deletion was performed.

Stop for joint owner/Task 04 review. F2 is the concrete proposed small repair;
F4/F5 require separately scoped retirement/cutover, and F6 needs an explicit
error-disposition decision if assigned. This report neither approves repairs nor
releases Task 05.
