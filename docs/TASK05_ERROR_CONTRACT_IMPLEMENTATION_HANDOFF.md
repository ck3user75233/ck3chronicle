# Task 05 implementation handoff — 2026-09-27

## Delivered boundary

Pinned parser/recovery → shared complete assignment → selected regions bound once
→ serializable Error Contract record preparation. `error-contract-v1` accepts
both final `template` and `provisional` assignments, with `error_type=unknown`
and `occurrence_count=1`. This creates record-ready data, not SQL records.

The package is `44a0401b8adf0a2953d26705`; model revision remains
`76630685c4a341ca14bf9c7c` / schema 4. Parser is `ck3-lossless-v1.7`, matcher API
`ck3-native-matcher-v1`, selector `complete-assignment-v2`, classifier
`ck3-native-message-classifier-v8`. Manifest SHA-256:
`2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1`.
Parser SHA-256:
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.
Bootstrap SHA-256:
`5af9fa3f0d7cfd36cd9133630a4183787be18c14b0a7e04d09786a0a7430f17c`.

## Public API and stage ownership

All symbols below are under `ck3chronicle.pipeline`.

| Owner | Public signature / result |
|---|---|
| `catalog` | `selected_models_root() -> Path`; `load_selected_package(*, models_root: Path \| None = None, selection_path: Path \| None = None)`; `load_selected_classifier(*, models_root: Path \| None = None, selection_path: Path \| None = None, cache_size: int = 4096) -> Classifier` |
| `model` | `load_package(folder: Path, *, expected_manifest_sha256: str)` authenticates manifest and bootstrap, executes those verified bytes and calls the package loader. `read_json(payload)` rejects duplicate keys. No application model-semantic validator remains. |
| `classifier` | `Classifier(package, *, cache_size: int = 4096)`; `read_log(path)`; `classify_raw(raw)`; `classify(diagnostic)`. Public `package` exposes its verified loader/API. |
| `raw_input` | `iter_diagnostics(package, raw)` consumes package `iter_units` once; `native_regions(unit)` gives body, prefix, suffix, components in API order; `matching_content(unit)` removes only occurrence provenance for relative caching. |
| `bindings` | `bind_captures(original, region: dict, captures: list) -> tuple[NativeBinding, ...]` checks the selected original region and each present capture, producing absolute byte spans exactly once. |
| `contracts` | `materialize_definitions(package) -> dict[str, dict]`; `prepare_record(definition: dict, result: NativeClassification) -> dict`; `identity_data(values: dict) -> dict`; `identity_digest(values: dict) -> str`; `render_regions(definition: dict, values: dict) -> list[tuple[str, str]]`; `render(definition: dict, values: dict) -> str`; `run_lineage(package, *, application_revision: str) -> dict` |

`NativeDiagnostic(original, unit)` retains the original package input, pieces,
regions, supporting-entry framing and original access. Its `source_family`,
`source_tag` and `provenance` properties expose native facts directly.
`NativeClassification(diagnostic, model_revision, classifier_revision, selected,
review_reason=None)` has final `outcome` (`template`, `provisional`, `no_match`)
and `disposition` (`record` or `native_review`). These use the package status,
without the predecessor full/unknown translation or independent hierarchy.

`SelectedAssignment(template_id, template_status, match_status, regions, selection)`
contains exactly one assignment. `template_status` retains support metadata;
`match_status` is the final eligible status, including provisional tie-breaks.
`selection` contains selector facts without research alternatives.
`SelectedRegion(name, layout, bindings, span, component_index=None)` retains each
selected wrapper ID/component layout index and original region span.
`NativeBinding(slot_id, type, value, present, span)` contains exact opaque values
and absolute original-byte spans. No bound-candidate alternatives survive.

Cache: bounded instance-local LRU, default 4096, disabled by `cache_size=0`.
The key contains package-scoped parser metadata, source family/tag, recovery status,
context kind, exact body/wrapper text and ordered pieces, and every ordered
continuation text/piece/framing span. Only caller provenance is removed. Cached
results have relative spans and no occurrence association. Each current occurrence
receives fresh bindings and provenance; contract preparation does not read bytes,
recover, rematch, select, bind, infer semantics or regroup.

## Serializable schemas and usage

Definitions are copied once from the verified package and keyed by existing
`template_id`. Each is a JSON object containing:

- `contract_version`, `model_revision`, `template_id`, `source_family`,
  `context_kind`, `construction_id`, `parameter_structures`;
- `parts`: unchanged ordered literal/slot parts, including positional `name`,
  `type`, `optional`, `prefix`, `suffix` and declared `constraints`;
- `context_patterns`: prefix/suffix alternatives with existing `template_id` and
  exact ordered `parts`;
- `continuation`: null or unchanged declared rule, opening slot, reference/value
  types, minimum entries and ordered leading/label/trailing literal layouts.

The definition's `source_family` is emitter applicability without a changing C++
line number; the representative `source_tag` retains the original emitter tag.
Full-ID contents are never decomposed.

`prepare_record` returns:

```text
{
  values: {
    contract_version, template_id,
    regions: [{name, layout, component_index,
               bindings: [{slot_id, type, value, present}, ...]}, ...]
  },
  match_status: template | provisional,
  error_type: unknown,
  occurrence_count: 1,
  provenance: {
    source_tag, emission_ordinals, ordered_spans, recovery_limitation,
    message_ordinal,
    regions: [{name, span: [start,end], binding_spans: [[start,end] | null, ...]}, ...]
  }
}
```

`layout` is the exact shared API layout reference: body; prefix/suffix with
`wrapper_template_id`; or continuation with `layout_index`. Components also
carry their zero-based `component_index`. Regions remain in API order
(body, prefix, suffix, continuations); rendering walks framing order
(prefix, body, suffix, then ordered components). It adds no separators and no
log-header timestamps. All stored text and line endings retain native spelling.
Absent means `present=false,value=null,span=null`; present empty means
`present=true,value="",span=[p,p]`. Rendered optional prefix/value/suffix is omitted
only for absence. No duplicate complete-message field is stored.

```python
from ck3chronicle.pipeline.catalog import load_selected_classifier
from ck3chronicle.pipeline.contracts import (
    materialize_definitions, prepare_record, identity_data, identity_digest,
    render, run_lineage,
)
from ck3chronicle.pipeline.domain import NativeReview

classifier = load_selected_classifier()
definitions = materialize_definitions(classifier.package)
lineage = run_lineage(classifier.package, application_revision=exact_build_revision)
for result in classifier.classify_raw(classifier.read_log(complete_native_log)):
    if isinstance(result, NativeReview) or result.disposition == 'native_review':
        # Later storage owns native-review publication; retain this evidence.
        continue
    definition = definitions[result.selected.template_id]
    record = prepare_record(definition, result)
    equality = identity_data(record['values'])
    index_digest = identity_digest(record['values'])
    display = render(definition, record['values'])
```

For explicit pre-activation verification pass
`selection_path=Path('models/candidates/selection.proposed.json')` to the catalog.
The default follows active selection only; schema 1 and unsupported formats fail.

Use JSON `ensure_ascii=True` (the default) to retain surrogateescape values safely.
After JSON serialization/deserialization, rendering needs definitions and values
alone. `contracts` imports only standard-library facilities and the domain types;
its optional lineage function imports the classifier revision when called.

Identity retains full equality data, including template, every selected layout,
wrapper choice, component count/order/content and every ordered slot ID/type/value/
presence flag. The SHA-256 digest indexes that data; downstream aggregation must
compare full equality data. Status, timestamps, absolute offsets and a redundant
emitter comparison do not participate. Identity is scoped to the Run's definition
revision; grouping/counting across occurrences is not implemented here.

## Error and review dispositions

- `model.ResourceIntegrityError`: application selection/manifest/bootstrap
  correspondence or integrity failure, before unverified execution.
- `model.SelectionCompatibilityError`: unsupported selection format.
- Verified bootstrap `PackageIntegrityError` / `PackageCompatibilityError` and API
  `MatcherCompatibilityError`, `MatcherDeclarationError`, `MatcherIntegrityError`
  propagate distinctly. Package-specific exception types are exposed by the
  executing bootstrap/API; no exception is relabeled ordinary no-match.
- `domain.ResultIntegrityError`: selected-result, absolute binding or contract
  correspondence failure; propagates as an implementation/integrity error.
- Valid complete no-match: `NativeClassification` with `selected=None`,
  `outcome=no_match`, `disposition=native_review`, reason and intact diagnostic.
- Unresolved recovery: `NativeReview(original, unit, reason, error=None)`;
  `unit['recovery']` and original provenance remain intact. Public `source_family`,
  `source_tag` and `provenance` properties expose the unresolved evidence. Matcher
  is not called.
- Package `NativeInputError`: `NativeReview(original, unit, reason, error=exc)`.
  It is an explicit input failure with evidence, distinct from no-match. Other
  implementation exceptions are not swallowed. File/parser failures propagate;
  callers retain the named original input as evidence.

Run lineage includes `contract_version`, `model_revision`, `package_id`,
`package_manifest_sha256`, exact `parser` reference (version/hash/artifact),
`matcher_api_version`, `selector_version`, `classifier_revision` and explicit
`application_revision`. Supply an exact application build/source revision,
including working-tree differences when applicable. Historical training hashes
cannot stand in for package lineage. Database schema version belongs to storage.

## Verification and selected resources

Fresh verification used the repository `.venv` and all complete unmodified logs
from the [independent input inventory](../.codex-tmp/shared-matcher-pipeline-verification-20260927/inputs.json).
Every integrated occurrence was compared with a fresh separate package instance
and independent parse. No saved classifications, synthetic inputs, altered
witnesses or corrupt packages were used.

| Check | Observed |
|---|---:|
| Complete native logs | 31 |
| Recovered occurrences | 1,167,165 |
| Template / provisional / no-match | 712,271 / 445,741 / 9,153 |
| Selected regions bound once | 1,268,561 |
| Present original-byte captures | 4,447,658 |
| Absent captures / present empty fields | 59,054 / 1 |
| Wrapped occurrences | 55,268 |
| Groups / supporting entries | 11 / 13 |
| Selected-result differences | 0 |
| Fresh direct distinct inputs within logs | 78,882 |
| Integrated matcher / selector calls | 78,886 / 78,886 |
| Integrated selected materializations | 102,388 |
| Separate-process serialized unique values | 39,008 |
| Separate-process rendered regions | 42,460 |

Every original byte was retained by the parser and all emission ordinals were
accounted for. Selected IDs, final statuses, layouts, component indices, selection
facts, ordered captures and absolute bindings agreed. All nine slot types were
observed: KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM, REASON, CHARACTER_FULL_ID,
HOUSE_FULL_ID and TITLE_FULL_ID. Every occurrence independently checked original region bytes and each
present/absent binding. No unexplained differences remain.

Integrated replay used the documented 4096-entry instance LRU, cleared between
logs; fresh direct execution used an independent per-log complete-input cache.
Both cached only relative assignments. The bounded cache required four more
matching calls than the per-log direct cache; all selected results still agreed.
Instrumentation observed one parser call
and one recovery stream per log, one selector call per matcher call, and one
binding call per selected occurrence region. Preparation and rendering invoked
none of those stages. Genuine repeated groups have equal full identity data at
different offsets. A genuine pair with identical template/layout choices and
differing native values has distinct equality data and digests.

Every distinct definition/value combination encountered was JSON-serialized.
A separate `-I -S -B` process rendered those values with parser/model/loader/
classifier imports and native-log/model reads explicitly blocked. Region and
complete-render hashes match the original selected regions. Repeated occurrences
also passed rendering checks during the full replay.

Native coverage gaps: substantive/capture ties (including supported-template
provisional tie-breaks), alternative component layouts, groups beyond two entries,
unresolved recovery, malformed input, declaration conflicts, corrupt packages and
inconsistent-result errors. No fabricated cases are claimed as coverage. Previous
counts are observations; fresh direct-package execution supplied the comparison.

Active schema-2 selection was changed only after candidate replay and isolated
rendering succeeded. The normal source catalog then loaded the exact package.
The wheel was built offline from fresh ignored source staging, avoiding a stale
`build/lib` copy of the deleted matcher. Its selected resources and every pipeline module match source bytes;
it contains `contracts.py` and no `pipeline/matching.py`. Installation used only
`.codex-tmp/task05/installed-env`. Installed execution used an independent working
directory, `-I -B`, blocked learner/historical-provider imports, and blocked source
checkout code/model reads. The normal catalog resolved identical package bytes
from its own `sys.prefix/share/ck3chronicle/models`.

Installed **uncached** replay: 24,112 occurrences; 14,600 template, 359 provisional, 9,153 no-match. There were 24,112 selections, 17,781 selected-region bindings/materializations, and one recovery stream. Every prepared region rendered exactly, and the installed path also proved equal
identity for repeated groups at different offsets in that same log.

Exact selected wheel resources (under `share/ck3chronicle/`):

| Resource | SHA-256 |
|---|---|
| `models/selection.json` | `24d5c466de01577fd86bab4ccdc6bfa4ce79b0f4c0bf82ce6a8bde8103a76592` |
| `models/candidates/44a0401b8adf0a2953d26705/manifest.json` | `2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1` |
| `models/candidates/44a0401b8adf0a2953d26705/assignment.py` | `29e3bc8f54ac678988a3dc3e0023ce7c1dc76403900a44805ef958fbd47be235` |
| `models/candidates/44a0401b8adf0a2953d26705/continuations.py` | `11e4d8b146367c6374508a29b802a143288b973760620babc02c8f9f9760d6ce` |
| `models/candidates/44a0401b8adf0a2953d26705/empirical_template_model.json` | `897468f7b247c96ea29d7b28c944de1ff65c46e429ac6e06efebfbe93a6bf0db` |
| `models/candidates/44a0401b8adf0a2953d26705/full_ids.py` | `d91a646cde7887c5fe497e4c76a4bd4cd5ca59277c06c55995cdb5116d22dc28` |
| `models/candidates/44a0401b8adf0a2953d26705/matcher_loader.py` | `5af9fa3f0d7cfd36cd9133630a4183787be18c14b0a7e04d09786a0a7430f17c` |
| `models/candidates/44a0401b8adf0a2953d26705/matching_primitives.py` | `b10fb86cac48c73c376a50da07379633f2f508d036a33bbbe4203a37a31693be` |
| `models/candidates/44a0401b8adf0a2953d26705/matching_validation.py` | `3d66d2e7ec9ff175d2bbdde778e97fd04bd080b4c4ad464fc27ae873bbcc57fc` |
| `models/candidates/44a0401b8adf0a2953d26705/native-validation.json` | `076be4069855f8cabd2b0c96fcb4a31f0c3d65046a54e0ccceed0c0375d5a8b4` |
| `models/candidates/44a0401b8adf0a2953d26705/native_matching.py` | `5262ed2944a85e8ffe34ce23ab6e11b3c5b47976cae157711532c87158d5ff4d` |
| `models/candidates/44a0401b8adf0a2953d26705/owner_rules.json` | `3d7e3da60625554f67f9ebf258514172c12a6c5315acb30fe7309f2db340fc77` |
| `models/candidates/44a0401b8adf0a2953d26705/parser-manifest.json` | `8ecc55cbdfb4d5601e4cc2c2f11b278b4b0962f9f6e9c62c739f6fd5248f79bb` |
| `models/candidates/44a0401b8adf0a2953d26705/parser.py` | `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |

Wheel SHA-256: `b3e75953bf81ec73566ff3bd8ecd70e5df1181e6bc3e27dae5bb2db8b927b940`.

Ignored [verification directory](../.codex-tmp/task05/) contains `verify.py`,
`verification.json` (per-log counts, instrumentation, caches, timing and repeated
group provenance), `render_only.py`, `render-only.json`, `definitions.json`,
`render-input.jsonl`, `identity_check.py`, `differing-native-values.json`,
`build_wheel.py`, `wheel.json`, `installed_check.py`, `installed.json`,
`lineage.json`, `entry.json`, `exit.json` and `scope.json`.

Reproduce native and isolated rendering checks from the repository root:

```powershell
.\.venv\Scripts\python.exe -I -B -u .codex-tmp/task05/verify.py
.\.venv\Scripts\python.exe -I -S -B .codex-tmp/task05/render_only.py
.\.venv\Scripts\python.exe -I -B .codex-tmp/task05/identity_check.py
```

The build script requires fresh build-source/wheels directories; use a new
disposable output directory for another build. Source compilation and focused
whitespace/link checks passed. No synthetic regression suite or legacy-provider
processing command was run.


## Scope, Git state and remaining work

Entry and exit HEAD are unchanged:
`2993144e061681c5651e3e18be1290c957d4892d`. Entry captured **291** tracked and
untracked non-ignored file hashes plus full Git status. The ignored
[entry](../.codex-tmp/task05/entry.json), [exit](../.codex-tmp/task05/exit.json) and
[scope comparison](../.codex-tmp/task05/scope.json) record exact SHA-256 hashes and
Git state, including pre-existing untracked learner and candidate source.
All other entry hashes and all 31 native input hashes remain unchanged.

| Action | Paths |
|---|---|
| Created | `src/ck3chronicle/pipeline/contracts.py`; `docs/TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md` |
| Edited: pipeline | `src/ck3chronicle/pipeline/catalog.py`, `model.py`, `raw_input.py`, `classifier.py`, `bindings.py`, `domain.py` |
| Deleted | `src/ck3chronicle/pipeline/matching.py` |
| Edited: resources | `models/selection.json`; `pyproject.toml` |
| Edited: documentation | `README.md`; `docs/PROJECT_STATUS.md`; `docs/PROJECT_PLAN.md`; `docs/CURRENT_HANDOFF.md`; `docs/PIPELINE_ACTIONS_AND_EXECUTION_ORDER.md`; `docs/SHARED_MATCHER_API.md`; `docs/SHARED_MATCHER_PIPELINE_VERIFICATION.md`; `docs/ERROR_CONTRACT_SPECIFICATION.md`; `src/ck3chronicle/pipeline/TASK03_CLASSIFICATION_HANDOFF.md` |


No commits, Git staging, push, learner publication, production ingestion, database
access or watcher operation. Native logs, immutable candidate payloads, existing
model releases, learner source, application/CLI/database providers and unrelated
entry work remain unchanged. Development and production environments remain intact.

Remaining implementation: Run aggregation/counting; SQL definitions and records;
native-review persistence; reports reading stored definitions/values; and the
separately commissioned application/provider cutover and broad model retirement.

Named historical dependency: retire the live old-baseline path in
`tools/template_learning/build_parser_comparison.py` before deleting
`pipeline/emissions.py`, `diagnostics.py`, `normalization.py` and their historical
domain types. They remain outside this processing path.

Additional removed-API consumers found during caller inspection, left untouched
under the learner mutation boundary: the historical consumer-check section in
`tools/template_learning/inspect_cross_emission_recovery.py` imports old `Capture`
and calls old `iter_diagnostics`/binding signatures; the opt-in
`tests/test_raw_parser_requirements.py::test_independent_pipeline_replay` imports
removed `read_raw_log`. Their owners should update those research checks to the
selected package API, without resurrecting compatibility aliases. Current Task 05
native and installed checks exercise the replacement APIs directly.

Known learner/model limits remain as recorded in
[the learner handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md),
[the API/recovery limits](SHARED_MATCHER_API.md),
[the independent verification](SHARED_MATCHER_PIPELINE_VERIFICATION.md), and
[continuation model status](LEARNER_CONTINUATION_MODEL_STATUS.md).
Training coverage does not establish unseen accuracy. Unseen/malformed/interrupted
title-list recovery variants and existing unrelated unmatched formulations are
not repaired or reinterpreted in this pipeline task.
