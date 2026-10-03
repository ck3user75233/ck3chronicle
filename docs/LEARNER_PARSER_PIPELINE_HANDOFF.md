# Formal reply: published native model and shared parser

## Script location stack investigation — 2026-09-28

See [the investigation results](LEARNER_SCRIPT_LOCATION_STACK_INVESTIGATION_RESULTS.md)
for complete retained-log measurement, saved SQL sample 17, native short/long
examples, ordered location bindings, review-evidence checks and an assessed
variable-length design. Current selection is the Task 06-integrated v45 package
`68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`.
The recommendation is to retain the active representation; proposed repeat-node
model/API work and conditional pipeline dependencies are separate owner-review
items. No representation or activation change is part of the investigation, and
Task 07 need not wait for one. Earlier delivery-time selection statements below
retain their historical meaning.

Fresh replay of 73 complete native logs found **zero demonstrated length-caused
misses or lost location fields** across 1,174,361 Script location diagnostics
(1,807,351 file/line entries; observed lengths 1–30, 33, 41 and 55). All four
corpus-wide no-matches are unrelated travel diagnostics preserved byte-for-byte
in existing Task 06 review shards. The result is in-corpus coverage, not proof of
unseen-length generalization. The focused shared-primitive probe also shows why
simply dropping the ordered-structure gate would be unsafe: a one-frame body
pattern can absorb later locations into PARAM, while current complete matching
correctly rejects that assignment.

## Learner v45 release delivery for Task 06 integration — 2026-09-28

The owner separated learner release delivery from Task 06 integration, with a
shared target of **model schema 5 / `ck3-native-matcher-v2`**. The learner has
fixed the demonstrated additive applicability defect and built a replacement
from the agreed 73 complete native logs, using 20 + 20 + 20 + 13 cumulative
batches. This supersedes the two-log candidate as the proposed replacement.

| Identity | Delivered value |
|---|---|
| Runtime package | `68f1ae5db205ab46afef9c4d` |
| Published model | `f5cde2616f35d563118d3d32` |
| Source candidate | `c4f174d947fbc531aba35fb7` |
| Learner | `outer-diagnostic-consensus-v45` |
| Learner implementation SHA-256 | `025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088` |
| Parser | `ck3-lossless-v1.7` |
| Parser implementation SHA-256 | `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |
| Model schema / matcher API | `5` / `ck3-native-matcher-v2` |
| Package manifest / selection schemas | `1` / `2` |
| Selector | `complete-assignment-v2` |

Package directory:
[`models/candidates/68f1ae5db205ab46afef9c4d/`](../models/candidates/68f1ae5db205ab46afef9c4d/).
Externally pin this manifest SHA-256:
`2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
The [manifest](../models/candidates/68f1ae5db205ab46afef9c4d/manifest.json) contains
the exact hashes of the model, parser, shared matcher primitives/public API,
validator, selector, full-ID/continuation helpers, rules and bootstrap.
[Proposed selection metadata](../models/candidates/selection.v45.proposed.json)
is a separate file; active `models/selection.json` remains unchanged.

The complete [release assessment](LEARNER_RELEASE_V45_RESULTS.md) leads with
native before/after results, evolution, changed captures and remaining issues.
The final model assigns 2,439,711 occurrences as template and 154,873 as
provisional, leaving four unmatched. All original 122 review bodies / 9,153
occurrences have complete assignments through 28 definitions. There are two
lost matches versus the thirty-log baselines, no additional lost matches versus
the prior 73-log additive model, and documented capture/status regressions.
These limits are part of the delivery, not hidden behind a test-pass claim.

### Schema/API change and callable boundary

Authenticate the externally pinned manifest and its bootstrap before executing
the package. [matcher_example.py](../tools/template_learning/matcher_example.py)
demonstrates this without installed development packages. The callable interface
is unchanged in shape:

```python
package = authenticated_loader.load_package(folder, expected_manifest_sha256=pin)
raw = package.parse_file(complete_native_log)
for unit in package.iter_units(raw):
    result = package.match(unit, inspect=True)
```

Ordinary matching omits `inspect=True`; inspection adds alternatives without
changing selection. Complete `template` and `provisional` assignments are both
eligible records. `no_match` remains explicit. Byte spans are relative to each
original region in UTF-8/surrogateescape; provenance belongs to the caller.
See the [API-v2 contract](SHARED_MATCHER_API.md) for inputs, layouts and failures.

Schema 5 represents the owner-approved line-label equivalence as a literal part:

```json
{"kind":"literal","text":"line:","alternatives":["line:","near line:"],"location_label":"line-location"}
```

Validation requires the exact declared alternatives immediately before a
mandatory numeric LOCATOR, with only horizontal whitespace between them. These
are literals, not slots or preprocessing. Opaque fields and all other wording
retain their existing rules. A selected body/wrapper layout with choices adds
`literal_choices: [[part_index, alternative_index], ...]`. Persist those indices
with the layout and use them for exact rendering; do not substitute canonical
`text` or infer the spelling later. Choices participate in exact diagnostic
identity. Missing/invalid choice data fails explicitly.

The package is self-contained. It needs no learner registry, mutable rules,
training corpus or development imports. The API-v2 loader validates schema 5;
the old selected API-v1 package continues using its own immutable loader and
model. No cross-version training-state import or old-package rewrite occurred.

### Verification and integration disposition

[Immutable export validation](../models/candidates/68f1ae5db205ab46afef9c4d/native-validation.json)
replayed all 91,925 contextual inputs representing 2,594,588 occurrences and
found zero changed matches/outcomes/capture assignments after compaction. It
records the native evidence digest and 378,434 body/component capture-byte checks.
The independent `-I -S` [whole-log package replay](../.codex-tmp/learner-release-v45/delivery-replay.json)
completed all 73 genuine inputs: 2,439,711 template / 154,873 provisional / four
no-match occurrences, with zero discrepancies against the complete build
inspection results. It reparsed every original log and checked 2,882,529 selected
regions and 10,285,082 present captures against native bytes. Both declared
line-label spellings occurred. No development modules were imported, and active
selection remained unchanged. Coverage comparisons cache matching by distinct
complete input (91,925); native occurrence associations and bytes were checked
throughout, with additional fresh calls for the original review cases.

All original case/ordinal associations reconcile: 118 template / four provisional
cases, weighted 267 / 8,886 occurrences. The entire affected log gives 15,101
template / 9,011 provisional / zero no-match across 24,112 occurrences.
[Original-case public results](../.codex-tmp/learner-release-v45/original-122-public.json)
and [native layout/capture examples](../.codex-tmp/learner-release-v45/delivery-examples.json)
retain the exact values and provenance. The
[final artifact audit](../.codex-tmp/learner-release-v45/final-audit.json) verifies
all 12 runtime payload hashes and 28 frozen learner-source hashes. This proves
delivery parity; the assessment's semantic limitations remain.

Task 06 integration should exercise this explicit proposed selection in isolated
verification storage, preserve choice indices through preparation, aggregation,
SQLite and rendering, retain both final assignment statuses, and reconcile native
review associations. Existing records retain their own immutable definitions and
identities. The current contract remains `error-contract-v1`; no database migration,
production processing or active-selection change is part of this learner delivery.
The policy questions about word-run protection, grouping-sensitive captures and
tie-breaking remain for owner review. They were not broadened to fit this corpus.

## Earlier two-log Pipeline Team response — 2026-09-28

[Task 06 unmatched-review formal reply](LEARNER_TASK06_UNMATCHED_REVIEW_REPLY.md)
closes the original 122-case investigation and demonstrates complete candidate
assignments for all 9,153 emissions. It does not announce production deployment.
The then-current v44 additive candidate `39cb19ab0ea10a48ebb98a46` is isolated/unpublished,
uses model schema 5 / matcher API v2, and gives 114 template / 8 provisional cases.
The owner-highlighted date/full-ID and untyped-effect/Unknown examples have full
worked before/after traces; the complete case ledger retains original associations.

**Actual active selection:** Task 05 selected schema-2 package
`44a0401b8adf0a2953d26705`, model `76630685c4a341ca14bf9c7c` (schema 4 / API v1).
It remains selected and still produces the original unmatched shard. The delivery
text below describes the earlier pre-Task-05 state; its schema-1/not-activated
statements are historical, not current operating instructions. Current integration
authority is the [Task 05 handoff](TASK05_ERROR_CONTRACT_IMPLEMENTATION_HANDOFF.md)
and [Task 06 handoff](TASK06_RUN_STORAGE_AND_NATIVE_REVIEW_HANDOFF.md).

## Earlier delivery record — 2026-09-27

Updated 2026-09-27. This is the formal reply to
[LEARNER_MODEL_DEPENDENCIES.md](LEARNER_MODEL_DEPENDENCIES.md), incorporating the
owner's subsequent decisions. It supersedes the dated development checkpoints
previously accumulated in this document. Historical research remains in the
[implementation ledger](LEARNER_OUTER_DIAGNOSTIC_IMPLEMENTATION.md).

## Historical delivery: shared model-pinned matcher candidate — 2026-09-27

**Delivered, not activated:** package `44a0401b8adf0a2953d26705` at
[`models/candidates/44a0401b8adf0a2953d26705/`](../models/candidates/44a0401b8adf0a2953d26705/).
Manifest SHA-256: `2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1`.
[Proposed selection metadata](../models/candidates/selection.proposed.json) uses
selection schema 2 and is **not** `models/selection.json`. The active schema-1
selection and original release remain byte-for-byte unchanged; the pipeline
reader must support the new package before activation.

Model **76630685c4a341ca14bf9c7c**, schema **4**, all **418 templates**, IDs,
definitions, support evidence and declarations are unchanged. Model JSON hash:
`897468f7b247c96ea29d7b28c944de1ff65c46e429ac6e06efebfbe93a6bf0db`.
Parser **ck3-lossless-v1.7** and selector **complete-assignment-v2** are unchanged.
Matcher API: **ck3-native-matcher-v1**. Package format:
**ck3chronicle.native-matcher-package v1**. All twelve payload hashes are in the
[manifest](../models/candidates/44a0401b8adf0a2953d26705/manifest.json).
Executable dependency hashes are:

| Artifact | SHA-256 |
|---|---|
| `matcher_loader.py` | `5af9fa3f0d7cfd36cd9133630a4183787be18c14b0a7e04d09786a0a7430f17c` |
| `native_matching.py` | `5262ed2944a85e8ffe34ce23ab6e11b3c5b47976cae157711532c87158d5ff4d` |
| `matching_primitives.py` | `b10fb86cac48c73c376a50da07379633f2f508d036a33bbbe4203a37a31693be` |
| `matching_validation.py` | `3d66d2e7ec9ff175d2bbdde778e97fd04bd080b4c4ad464fc27ae873bbcc57fc` |
| `full_ids.py` | `d91a646cde7887c5fe497e4c76a4bd4cd5ca59277c06c55995cdb5116d22dc28` |
| `assignment.py` | `29e3bc8f54ac678988a3dc3e0023ce7c1dc76403900a44805ef958fbd47be235` |
| `continuations.py` | `11e4d8b146367c6374508a29b802a143288b973760620babc02c8f9f9760d6ce` |
| `parser.py` | `a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab` |

The old model's learner implementation hashes remain training lineage. The new
manifest pins runtime matching code. `native-validation.json` is the unchanged
source-release record; the fresh extraction proof is linked below.

### Callable contract and runnable example

Authenticate the manifest and bootstrap, then call
`matcher_loader.load_package(folder, expected_manifest_sha256=pin)`.
`package.parse_file(path)` uses the pinned parser; `package.iter_units(raw)`
projects its complete regions. `package.match(unit, inspect=False)` returns one
`assignment` with final `match_status: template|provisional`, or
`status: no_match, assignment: null`. Inspection alternatives are opt-in.

Input supplies parser version/hash, source family/emitter, context kind, original
body text/pieces, complete prefix/suffix regions where required, ordered original
continuations and caller provenance. The selected result supplies template ID,
wrapper IDs, actual component `layout_index`, ordered `component_index`, and
ordered captures `{slot_id,type,value,present,span}` per named region. Provenance
associations pass through unchanged. No absolute occurrence binding is performed.

Every span is a half-open **UTF-8/surrogateescape byte interval relative to the
start of its own original region**, excluding the log header. Each wrapper and
continuation has its own origin. Absence is `false/null/null`; present empty is
`true/""/[p,p]`. Render directly from the selected layout references. Package
integrity/compatibility, matcher declarations/input and inconsistent-result
errors are explicit exceptions, distinct from no-match. Full input/result/error
schemas and layout lookups: [Shared matcher API](SHARED_MATCHER_API.md).

This command runs the standalone example over the **complete** identified
continuation-bearing native log. It needs only Python's standard library and the
package; it works with learner/site imports disabled:

```powershell
.\.venv\Scripts\python.exe -I -S -B tools/template_learning/matcher_example.py --package models/candidates/44a0401b8adf0a2953d26705 --manifest-sha256 2a768c9d9729025da2874671dfc5952b703019f57a36a68e8437e1242122aca1 --log .codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/sessions/10cbdcb23e34a5b571a16eb52d390e5e676663936f000fd43404af19d85027fb/error.log
```

Observed: 49,560 template and 26,949 provisional results, including complete
supporting groups. [Example source](../tools/template_learning/matcher_example.py)
and [saved output](../.codex-tmp/shared-matcher/example-result.json).

### Learner changes and native verification

Matching bodies were extracted from `patterns.py`, `research_matching.py`,
`constructions.py`, `parameter_structures.py`, `literal_guidance.py` and
`regions.py` into `matching_primitives.py`. `native_matching.py` connects those
primitives, the existing continuation helper and unchanged selector. The only
component-helper output extension is the selected literal `layout_index`.
`matching_defaults.py` supplies explicit current learner rules for inference;
it is not packaged. Full-ID mechanics are unchanged and now release-hashed.
No independent fallback matcher remains in learner code.

Remaining caller paths:

- Evaluation and publication validation use `Matcher.inspect_record`; the
  existing incremental/candidate/unseen-session tools reach that evaluator.
- Pattern derivation, clustering, wording checks, selection evidence and
  template retirement use shared primitives through explicit learner defaults.
- Native/outer/symbol-location inspection uses the same primitives.
  `review_assignment_changes.py` no longer invokes the pipeline matcher.
- `publish_native_model.py` now publishes matcher packages from an explicit
  reviewed release or a newly validated candidate; existing releases are never
  overwritten. No inference or template-policy redesign was performed.

Fresh baseline and learner after replay: **31 complete, unmodified logs**, all
30 selected-release evidence hashes plus the additional handoff log; none
unavailable. **78,869 distinct complete inputs within logs**, representing
**1,167,165 diagnostics**. Independently loaded final-package replay agrees on
eligibility, every complete capture alternative, selected templates/wrappers,
components and final status. Unpublished-candidate replay also agrees; compacting
it reproduces the selected model exactly.

Final counts: **712,271 template / 445,741 provisional / 9,153 no-match**.
**4,447,658 present captures and 59,054 absences** agree with original bytes;
all selected layouts reconstruct their native regions. All nine slot types,
**one present-empty REASON**, **55,268 wrappers**, **11 continuation groups /
13 entries**, and **1,086 evidence-ranked competing-template occurrences** are
covered. Instrumentation observed **102,371 selected-region materializations**
across distinct inputs, exactly once per selected region, with none for losing
candidates and zero absolute binding calls. Ordinary results omit alternatives.
The standalone example additionally invoked ordinary matching on all 76,509
occurrences of its complete log.

Human-readable examples (full original bodies, wrappers, templates, captures,
statuses and provenance in the [native appendix](../.codex-tmp/shared-matcher/NATIVE_EXAMPLES.md)):

- `Failed to read key reference: : , near line: 3` selects
  `b35f3708de13620311279395`, template. Its two OPTIONAL_KEY captures are absent;
  LOCATOR `"3"` is present at body bytes `[45,46]`. Required wrapper IDs and
  wrapper captures remain in the selected assignment.
- The native `equip_artifact_to_owner_replace effect [  ]` diagnostic selects
  `b40e4648e0d25bfd2b9857e0`, provisional. REASON is present `""` at `[73,73]`;
  the full file, line `1005` and PARAM `wedding_gift:effect` remain captured.
- `House 'Ashikaga (Internal ID: 33577602 - Internal Key: )' ...` selects
  `d93bb7bf10986cf39a125334`, template. HOUSE_FULL_ID retains the entire opaque
  ID, including its empty internal key; that is not an absent or empty slot.
- The two-entry native title group selects `0875e8c46afb0b47271a8341`, template,
  with both original components in order and layout index 0. Unmatched evidence
  remains: 9,153 occurrences / 122 distinct inputs in the additional log,
  including the original formatted already-has-trait diagnostic.

No semantic differences were found. The sole legacy-shaped result difference
is additive component layout metadata, explicitly accounted for in comparison.
New public presence/layout/provenance fields expose the same selected assignment.

[Verification and limitations](../.codex-tmp/shared-matcher/VERIFICATION.md),
[fresh baseline and input provenance](../.codex-tmp/shared-matcher/baseline/baseline.json),
[final independent replay](../.codex-tmp/shared-matcher/independent-final.json),
[learner after replay](../.codex-tmp/shared-matcher/baseline/after.json),
[unpublished parity](../.codex-tmp/shared-matcher/unpublished.json).
Generated native evidence remains ignored. No native capture ambiguity, template
or capture tie, alternative component layout, >2-entry group, declaration error,
corrupt-package input or unresolved recovery was available. Those branches are
not claimed empirically verified. Deterministic provisional tie handling remains
in the byte-unchanged selector. Parser recovery limitations are unchanged and
separate from matcher no-match; see the API contract.

### Pipeline actions

1. Add support for the proposed selection/package schema; load and verify the
   package and its parser/model/matcher/selector pins.
2. Replace local matching with `package.match` on each complete recovered unit.
3. Bind only its selected assignment **once**, preserving final match status,
   exact values, presence, layout references, order and caller provenance.
4. Verify against complete native logs, then retire the superseded pipeline
   matcher. Keep error typing `unknown`.
5. Activate the candidate only after reader integration. SQL, production
   ingestion, application cutover and watcher operation remain separate work.

## Active older release: learner v41, parser v1.7, complete continuation groups

Published and pinned revision **76630685c4a341ca14bf9c7c** in
`models/selection.json`. Manifest SHA-256:
`364215904d0b167b94365cb6b666818db15cc1947778acf6511772b9e12943c0`.
Model schema **4**, assignment policy **complete-assignment-v2**, classifier
**ck3-native-message-classifier-v7**, learner feature format **v4**. The parser
is the previously delivered immutable **ck3-lossless-v1.7**, unchanged hash
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.
This section supersedes the earlier candidate/integration-gap notes below.

The release contains seven hash-covered artifacts plus manifest.json: model,
parser, parser manifest, owner rules, native validation, **assignment.py** and
**continuations.py**. The runtime reader verifies and loads the two standalone
helpers from the selected release. No caller should implement its own ranking
or continuation matcher, concatenate component bodies for matching, or classify
a supporting title entry as an independent diagnostic.

### Complete-error representation and use

Ordinary templates have `continuation: null`. A grouped template has one opening
pattern plus a repeatable component contract: rule ID, opening reference slot,
reference/value types, minimum entry count and exact native literal layouts.
For the delivered declaration, each entry has a repeated CHARACTER_FULL_ID,
the literal `'s title: ` and a displayed-title PARAM. The opening diagnostic
wording is learned; the declared entry field is opaque. One/two/more entries
use the same template. Every entry must validate and repeat the selected opening
reference. Matching only the opener is insufficient.

`NativeDiagnostic.continuations` retains ordered original bodies and parser
prefix/label/value spans. Group `context_kind` is
`continuation:history-colon-title-list-v1`; normal body/wrapper kinds are unchanged.
The learner record key includes the whole ordered entry list, so equal openings
with different lists do not collapse. Occurrence provenance includes all member
emission ordinals, complete group span and component spans.

`Classifier.classify_raw()` / `classify()` now invoke the published selector.
`NativeClassification.selected` is one complete CandidateMatch, or None for an
unknown. `template_id` and `bindings` expose that selected result for **both full
and provisional outcomes**; callers must retain `outcome` rather than treating a
nonempty template ID as confirmation. `candidates` remains research alternatives;
use `selected` for production assignment. `selection` records ranking/tie details.
The selected result contains opening, wrapper and ordered `components` matches.
Each binding carries its region: `message`, wrapper name, or `continuation:N`
(zero-based entry index), with its own **absolute native byte span**.

For direct selector consumers, supply all complete opening/wrapper witnesses as
before, plus `component_witnesses`, aligned one-for-one with body witnesses.
Each component match is `{index, captures}`; captures retain
`{name,type,value,span}` with spans **relative to that entry's original body**.
The result now includes `component_matches`. Ordinary candidates supply one empty
component list per body witness. The hash-covered continuations.py validates
component layouts and opening-reference equality; it performs no tokenization.
The runtime analyzer no longer truncates alternatives to two witnesses.

### Native validation and remaining application work

Fresh inference on the same thirty complete logs produces **418 templates**:
232 supported and 186 provisional. All 1,143,044 unaffected occurrences retain
their v40 selected templates, statuses and captures. Twenty formerly separate
messages become nine complete errors with eleven supporting entries; seven old
opening/title formulations become one complete-error template. The resulting
1,143,053 diagnostics comprise 697,671 full and 445,382 provisional assignments,
zero unknown. Compact export and independent runtime replay agree on every
assignment; **4,429,930 bindings** match original bytes.

Both affected complete logs were also exercised: all eleven groups/thirteen
entries, including repeated occurrences and both list lengths. The second log
is outside the thirty-log training set; its two groups match the same supported
template. It still has 9,153 unrelated unknown occurrences (8,880 are one
`untyped effect` / `Script location: Unknown` formulation). Those are an existing
coverage limitation, not new continuation regressions; the v40 comparison had
9,155 unknowns, including two now-associated title entries. No unseen-accuracy
claim follows from training coverage.

Reader, matcher, selector and binding integration are implemented and exercised.
Application ingestion/storage/report callers still need to consume the selected
result and retain necessary component content in the same diagnostic record.
No separate SQL emission parent is required. This publication starts no watcher
and performs no production ingestion. Rebuild features/registry state for the
new learner/parser identity; do not migrate previous template conclusions.

See [status and evidence](LEARNER_CONTINUATION_MODEL_STATUS.md) and the
[readable native group review](../.codex-tmp/learner-refactor/continuations-v41/REVIEW.html).
Native artifacts remain ignored. Missing/malformed title-list variants have no
native witness in this census and remain unvalidated. All other accumulated
changes remove deprecated/incorrect architecture.

## Historical candidate single-assignment delivery — learner v38, 2026-09-26

Owner authorized template retirement/winner selection and a native comparison.
This delivery is a **review candidate**, not a replacement production pin.
Thirty-log candidate `8c188491a07bba594efa4159` is under
`.codex-tmp/learner-refactor/single-assignment-v38/policy-driven/logs-30/`; ten-log candidate is
`71adca09f2d7551287987976`. Both use parser v1.6 to isolate the comparison.
The independently delivered v1.7/grouped-component work below remains separate.

The model now carries `assignment_policy` version `complete-assignment-v1` and
candidate-local `selection_evidence` on body and wrapper templates. The bundle
includes hash-covered standalone **assignment.py**, using only the standard
library. No mutable learner rules or second pipeline ranking policy are needed.

After existing source/construction/body/wrapper eligibility matching, call:

```python
selected = assignment_module.select_assignment(model_data, candidates)
```

`candidates` is a list of:

```python
{
    "template_id": template_id,
    "body": {"count": complete_count, "witnesses": complete_capture_lists},
    "contexts": {
        # prefix/suffix only where the diagnostic has an enclosing wrapper
        region_name: [
            {"template_id": wrapper_template_id,
             "count": complete_count, "witnesses": complete_capture_lists}
        ]
    }
}
```

Supply **every complete capture alternative**, not just ambiguity witnesses.
The selector rejects truncated witness lists. The learner's analyzer now exposes
`witness_limit=None`; the runtime analyzer currently retains only two witnesses
and needs corresponding adaptation for cases with more than two assignments.
None of the current thirty-log native cases has capture ambiguity. Multiple
templates are nevertheless exercised. Each capture remains `{name,type,value,span}`
with native region-relative byte offsets. Do not flatten wrappers into the body.

The returned assignment contains one `template_id`, `template_status`,
`match_status` (`template` or `provisional`), ordered `captures`, and one selected
wrapper pattern/capture list per region in `context_matches`. Literal layouts
remain in each selected model pattern's `parts`. `None` means no eligible
complete candidate. `selection` records evidence ranks/ties for research/debug;
SQL does not need the competing-candidate audit.

Selection prefers fewer native structural losses, fewer fields without positive
local evidence and greater independent support; final identity/capture ordering
breaks evidence ties and keeps reporting status provisional. Metrics are exported
from each candidate's native learning evidence, not inferred anew at runtime.
No adjective lookup, raw occurrence weighting, longest-literal rule or global
KEY-over-PARAM rule. The learner first retires exact fixed-KEY specializations
with proven identical surrounding structure, retaining an audit and native
provenance. It does not re-infer a coverage-driven union.

Native evidence: all 38,621 contextual rows / 1,143,064 occurrences replayed
through existing runtime matching mechanics plus the independently loaded frozen
selector; selected bodies/wrappers reconstruct exactly. Active templates 600 →
500; 106,869 previously competing occurrences receive one supported assignment;
1,119 become provisional after excluding trace-only support. Unknown remains zero.
The ten-log build exercises four occurrences requiring the deterministic tie-break.
These counts do not establish semantic correctness of every retained template.

The final compact export reproduces all ten/thirty contextual assignments. An
isolated interpreter reproduces 25 native samples per corpus using only the
bundled assignment.py and model/candidate data, with no learner/pipeline imports.
Ranking metrics and retirement thresholds are executable owner-JSON declarations.

**Pipeline work remains:** verify/load the extra hash-covered artifact, carry
the policy/evidence fields through model validation, expose all complete capture
alternatives, invoke this selector, and bind/store its single body/wrapper result.
The existing `Classifier.classify()` has not been changed to call it. Read-only
mechanical replay is not completion of that adapter. Existing model readers also
require updating their exact release artifact set before a new release is pinned.
No production ingestion/SQL, model publication or selection change occurred here.
All other changes are removal of deprecated/incorrect architecture.

Readable comparison with 25 native examples:
`.codex-tmp/learner-refactor/single-assignment-v38/review-30/REVIEW.html`.
Implementation/results ledger: [LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md](LEARNER_SINGLE_ASSIGNMENT_IMPLEMENTATION.md).

## Published parser v1.7: simplified emitter continuation recovery — 2026-09-26

New immutable artifact: `tools/template_learning/parsers/v1_7/manifest.json`,
**ck3-lossless-v1.7**, parser SHA-256
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.
See the [delivery ledger](LEARNER_CHARACTER_TITLE_CONTINUATION_STATUS.md).

The owner rejected the character-recognizer dependency and directed the simpler
rule. A history.cpp/E message ending in a colon opens the group; adjacent title
entries associate by opaque prefix-byte equality. No character/name/ID recognition,
fixed failure wording, C++ source-line rule, model dependency or learner import.
Versioned recovery JSON is embedded in the standalone hash-covered artifact.

Both consumers use shared `iter_recoveries(raw)` / v1.7 `RawParse.iter_recoveries()`.
A recovery exposes ordered `parents` and one opening with ordered `continuations`,
each preserving original body/prefix/label/value ranges. The opening's own text/span
remains native. Complete byte partitions and debug v2 retain every header and
repeated reference. Captures bind to individual native bodies. Supporting entries
never become separate pipeline diagnostics or learner records.

All 73 complete logs passed: 11 groups, 13 entries, exact reconstruction,
2,517,916 unchanged unaffected local recoveries and 83,417 unchanged distinct native
body lexical sequences. Messages change from 2,594,601 to 2,594,588; zero new parser
unresolved outcomes. Complete affected-log consumer replay, all 13 capture ranges,
feature/debug round-trip, nine existing native/parser checks, independent loading
without the learner/recognizer and wheel byte/hash verification passed.

**Model action:** current inference cannot express repeated supporting components.
Feature v3 preserves each whole group in unresolved review evidence with
`recovery_status="recovered"`; classifier v6 returns one unknown group, never an
opener-only match. Repeated-component inference/model publication remain learner
work; schema 4 was not implemented. Publish a new immutable model referencing
v1.7 and its agreed component contract, with reader/matcher support, for full
classification. Regenerate caches; do not edit an existing model's parser pin.
Current model `0a61f6c93657948e0ca20b35` remains pinned to v1.6 and rejects mismatched
raw input. No production ingestion, SQL or watcher action occurred.

### Learner team handoff: adopt v1.7 and complete grouped-error support

**Starting point:** parser recovery is delivered. The next learner integration
must learn and match one complete error with an ordered list of supporting titles.
Do not reimplement the grouping rule or introduce character recognition into the
parser. This handoff describes the remaining integration; it does not claim that
a compatible model has already been trained or published.

**Select the new artifact explicitly.** Use
`tools/template_learning/parsers/v1_7/manifest.json`, with the version/hash above.
The old `v1/manifest.json` still selects v1.6, including its old recovery behavior.
Published models are immutable; switching a CLI parser argument does not repin
an existing model. Start fresh features/registry state for the new parser and
current learner implementation. Feature identity is now
`ck3-native-message-features-v3`; reuse neither old assignments nor cached pieces.

**What “prefix” means:** all message-body bytes before the literal `'s title: `
in an entry, excluding the log header and leading presentation spacing. It is
variable length, not the first X characters. The opener must start with those
exact bytes followed by a space, and subsequent entries must repeat them exactly.
This is byte association, not proof that the prefix is a valid CHARACTER_FULL_ID.
The learner owns that interpretation and the appropriate slot declaration.

Consume the shared stream rather than looping over `emission.recovery`:

```python
from template_learning.parsers import (
    iter_recoveries, load_parser, reference_from_manifest,
)

parser = load_parser(reference_from_manifest(
    "tools/template_learning/parsers/v1_7/manifest.json"))
raw = parser.parse_file(protected_log)
for recovery in iter_recoveries(raw):
    if recovery.status != "recovered":
        # Retain recovery.reason and unresolved_spans in the review channel.
        continue
    for opening in recovery.messages:
        # opening.text / span / pieces refer only to its original body.
        for entry in opening.continuations:
            original_entry = entry.message.text
            repeated_prefix = raw.read_text(entry.prefix_span)
            displayed_title = raw.read_text(entry.value_span)
        # Feed opening plus its ordered entries as ONE complete learning unit.
```

The snippet demonstrates access only; the existing collector already retains
unresolved outcomes. Preserve `recovery.reason` even on a recovered group, since
it can report an uncertain following continuation. `recovery.parents` supplies
all original emission provenance; `ordered_spans` reconstructs the complete
group. Do not use opening.text alone as the complete diagnostic.

**Current consumer behavior is deliberately explicit.** In `records.py`, complete
groups are retained in `evidence_stats[sha]["unresolved_emissions"]`, with
`recovery_status="recovered"`, `structure`, `recovery_limitation`, the complete
native block `text`/`span`, member `emission_ordinals`, and ordered `components`.
Component zero is the opener; subsequent components retain original body text/span
and prefix/label/value spans. `deferred_recovered_messages` counts these groups;
`recovered_messages` counts only inference-eligible records. No group member enters
the ordinary `SequenceRecord` pool independently. Preserve this distinction when
reporting coverage: these are parser successes awaiting model support, not lost
input or unsupported raw boundaries.

Pipeline `NativeDiagnostic.continuations` already carries ordered component
bodies and source ranges. Classifier v6 presently returns one `unknown` result
for a group, with its complete evidence and an explanatory limitation. Do not
remove that guard until matching validates the complete error, including entries.

**Remaining work for the learner/runtime integration:**

1. Define and version the repeated supporting-component model contract jointly
   with the runtime reader/matcher. The earlier suggested schema 4 was not
   implemented; do not assume it exists. Represent one opening and one repeatable
   title-entry component, with one or more entries in native order. Do not create
   an independent error template per title line or per observed list length.
2. Move complete groups from explicit deferral into structured learning records
   only when inference, serialization, evaluation and matching support them.
   Include all entries and their order in complete-record identity. Identical
   openings with different lists must not collapse; repeated complete errors
   remain occurrences. Preserve unresolved recovery outcomes separately.
3. Apply the learner's CHARACTER_FULL_ID rules to the opening reference, and
   capture each whole displayed title as PARAM, including interior spaces. The
   parser's opaque prefix association supplies neither slot type nor confidence.
   Keep repeated prefixes and headers retrievable as original evidence; compact
   display may show the opening once and indented title entries.
4. Bind every capture to its own original component region. Runtime offsets are
   relative to that region before binding to absolute byte offsets. Never add an
   offset in compact joined display text to the opening's start. Existing
   `bind_captures` can retain its contiguous-region contract.
5. Publish a new immutable model referencing v1.7 after the complete-error contract
   works in both routes. Update model selection only as part of that model's
   publication, not by rewriting an old release. No SQL parent-emission record is
   needed to understand one diagnostic; store its necessary content with it.

**Native evidence to reuse:**

- Input root: `.codex-tmp/learner-refactor/at-symbol-incremental-review/inputs/`.
- `sessions/10cbdcb23e34a5b571a16eb52d390e5e676663936f000fd43404af19d85027fb/error.log`,
  lines 48279–48298: nine adjacent blocks, including both two-entry examples.
- `sessions/9d3622ab1b6c85cbab45d83767bb870b06c6fb9d6da50ee44f5eba3674d98cbc/error.log`,
  blocks at lines 3478 and 9841: two occurrences of the same complete error.
- [Independent native census, neighbors and exact ranges](../.codex-tmp/character-title-continuation-review/evidence.json).
- [v1.7 complete-log and consumer results](../.codex-tmp/character-title-continuation-review/v1_7/verification.json).
- [Artifact/package and independent-loader verification](../.codex-tmp/character-title-continuation-review/v1_7/package-verification.json).

Use complete native logs for integration checks. Demonstrate both list lengths,
one learner/runtime outcome per group, no independent title classification, exact
CHARACTER_FULL_ID/PARAM source bytes, and preservation of unrelated neighboring
messages and repeated occurrences. The existing 73-log parser replay is a boundary
baseline, not proof of a future model's classifications. Missing/malformed/mismatched
title-list branches have no native witness in this corpus; report that limit.

The parser/adapter changes are separate from current v36 inference experiments,
template retirement and winner-selection work. Preserve that work and record the
actual learner implementation identity used for any new build. This handoff does
not start training, select a new production model, process pending logs or start
the watcher.

## Development correction — v36 coverage absorption removal

The owner-approved correction plan explicitly required deleting coverage-driven
absorption and its two unconditional calls. v36 implements that deletion; it
is not a runtime toggle. The repeated region-regrouping loop was already removed
in v35. The previously approved one original-group sweep remains.

The v35 evidence below predates this correction. Fresh native ten/thirty
comparison is recorded in [the implementation ledger](LEARNER_V35_IMPLEMENTATION.md).
Removing absorption exposes competing narrower/general templates; do not interpret
additional provisional outcomes as dropped raw messages or automatically valid
alternatives. v36 candidate e63bc6c6f15f79d36ae234a1 has 600 templates (296 supported,
304 provisional). In the thirty-log comparison all 106,869 changed occurrences
retain their prior matching template and gain additional competitors, so their
outcomes become provisional. Runtime/learner candidate selection and captures
agree on every changed row plus the full-ID witnesses; native capture bytes and
compact-template validation pass. This demonstrates the overlap defect rather
than resolving it. No v36 model is published and no production pin has changed.

## Development supplement — v35 one sweep and TITLE_FULL_ID

v35 implements the approved single original-group consolidation sweep, retaining
v34's missing-parent wording guard. Repeated region reopening is removed; the
separate coverage-absorption passes have not changed.

`TITLE_FULL_ID` joins CHARACTER_FULL_ID and HOUSE_FULL_ID in the existing
`parameter_structures` declaration registry and uses the same `full_id:
{definition, source}` slot constraint. The active model validator and shared
raw-piece recognizer support it. Consumers must preserve the complete captured
name/ID value and its byte ranges. Do not decompose it or treat its content as
positive diagnostic wording. No parser, framing, capture API or SQL changes.

Across the complete 73-log inventory, both routes agree on 85 title-reference
captures in three declared emitter contexts. Existing CHARACTER_FULL_ID and
HOUSE_FULL_ID boundaries are unchanged. The fresh same-ten/thirty candidate
comparison and remaining work are in [the v35 ledger](LEARNER_V35_IMPLEMENTATION.md).
Thirty-log candidate **753006dab4348ab5c6601afd** contains 457 templates (257
supported, 200 provisional). Strict compact-template validation passes; all
183,570 candidate captures preserve native bytes, and both matchers agree on all
76 affected title/parent rows. Outside thirteen title rows, the complete native
assignment comparison exactly reproduces the earlier one-sweep experiment.
This is targeted runtime verification plus complete learner comparison, not a
new complete runtime replay. The remaining inference work is explicit in the ledger.

Production still selects **0a61f6c93657948e0ca20b35** with parser v1.6; this
supplement is preparation for the candidate interface, not a publication.

## Development interface supplement — full-ID fields, 2026-09-26

Owner authorized CHARACTER_FULL_ID and HOUSE_FULL_ID. Learner v33 and the active
pipeline model validator/matcher now support both, using the same generic
`template_learning.full_ids.FullIdRules` implementation and the model's owner JSON.
The existing declared-field registry (`parameter_structures`) carries
`mechanic: full_id`, `slot_type`, raw ID markers and emitter-scoped boundaries.
Serialized slot constraints include `full_id: {definition, source}`. Consumers
must keep each complete value intact; no name/ID decomposition or entity identity
across runs is implied. Both fields are nonoptional whole captures; empty values
inside their ID parentheses are ordinary preserved content.

Raw parser v1.6, message framing, capture names/values/byte-range representation
and existing opaque REASON behavior are unchanged. Both fields supply no positive
diagnostic wording during learning. Full-ID matching verifies the declared whole
span rather than accepting an arbitrary PARAM-sized substring.

This is a development candidate supplement, **not a new published pin**. Existing
selection 0a61f6c93657948e0ca20b35 still validates and remains selected. Complete
native-log evaluation and outstanding diagnostic-wording issues are recorded in
[the full-ID ledger](LEARNER_CHARACTER_FULL_ID_STATUS.md). No SQL, ingestion,
watcher, or production selection changes have been made.

Candidate c5e23dbdc604f575dfd932b3 passed active-pipeline replay of all 1,143,064
messages in the same thirty native logs, agreeing with the learner on outcomes,
all alternatives and exact capture bytes. This establishes interface parity,
not correctness of every inferred diagnostic formulation; the ledger identifies
the surviving missing-parent wording defect.

Development follow-up, v34: candidate 2b3c6d09c3b753b10cfaa417 closes that
missing-parent wording defect, changing only the 63 affected assignments in the
same thirty logs. All 63 have identical single learner/runtime matches. This
adds no interface or parser change and is not a publication. The complete
regrouping experiment and remaining concerns are recorded in
[the follow-up ledger](LEARNER_FULL_ID_FOLLOWUP.md).

## Location-label refresh to pipeline Task 4 — 2026-09-24

Learner development note, 2026-09-25: v30 removes all template imports and pins
each evidence registry to one learner implementation. The fresh ten-log candidate
reproduces v29 templates and captures. The thirty-log candidate exposes newly
inferred overbroad PARAMs and is not approved for publication. This is not a release
or a pipeline interface change. The published revision below remains selected. See
[the work ledger](LEARNER_VERSION_ISOLATION_REVIEW.md).

New immutable release: **0a61f6c93657948e0ca20b35**. Manifest SHA-256:
`a0b4624795819c60e21462bf066fc793440b1d3a67535e7531e04cdfdb16e197`.
Source candidate `9ee807faa3ab6531dd6036bf`, learner v29. Supersedes the v27
pin below and retains its trace-boundary and empty-reason corrections. Parser
**ck3-lossless-v1.6**, parser bytes/hash, model schema 3 and capture interface
are unchanged. Rejected v28 was never published and is not included.

The learner consumes `owner_rules.json.location_label_equivalences`. It recognizes
declared complete location-label token sequences immediately before LOCATORs and
automatically re-infers each observed exact wording form. No manual template
overwrites, input normalization, optional literals or changed OPTIONAL_KEY rules.
The declarations do not equate arbitrary messages sharing a location label.

Replaced template `1332e889d727946cb5b53eb4`:

```text
Unrecognized loc key <KEY>. <OPTIONAL_KEY> file: <LOCATOR> line: <LOCATOR> (<PARAM>)
```

New supported templates:

| ID | Exact wording and slots (surrounding native whitespace also preserved) |
|---|---|
| `959e7fc883d82201a278e344` | `Unrecognized loc key <KEY>. Near file: <LOCATOR> line: <LOCATOR> (<PARAM>)` |
| `1edb00c1404c4dd6db2527dc` | `Unrecognized loc key <KEY>. file: <LOCATOR> line: <LOCATOR> (<PARAM>)` |

Same ten complete native logs: **297 templates: 165 supported, 132 provisional**.
Only 25 contextual rows / 217 occurrences change assignments; all other 295
templates are unchanged. Both genuine OPTIONAL_KEY fields retain their original
present/absent behavior. No outcome regressions: 290888 full, 61429 provisional,
zero unknown or ambiguous occurrences. Complete capture and inferred-member
checks passed; compact export reproduces all 7864 contextual rows / 37447 captures.
Independent pipeline replay also passed every message in all ten logs, with
identical outcomes, templates and captures. All logs reconstructed exactly and
every captured range reproduced its original file bytes, including 821250
LOCATOR captures. The additional native tribute-mission witness still exposes
four LOCATORs outside its two trace PARAMs. Selection and wheel packaging pin
this release; the selected-loader and wheel artifact/hash checks are recorded
with the native review.

**Consumer action:** reload the selection and invalidate model-dependent caches.
Do not reuse assignments or slot ordinals from the removed template: its optional
slot is gone, so following slot names shift. Runtime consumes ordinary exact
templates; it must not implement label stripping or its own alias rule. No parser
repin, schema migration, caller code change or new capture API is required.
This publication does not start ingestion or modify SQL. Separate matching
unification/single-assignment work remains outside this correction.

2026-09-25: the [single-assignment selection review](LEARNER_SINGLE_ASSIGNMENT_REVIEW.md)
now includes a current-model replay of the retained 73-log inputs and verified
historical competing provisional matches. No current collisions were found. It
The owner subsequently clarified that provisional competition must yield one
winner. The revised review recommends ordered evidence comparisons followed by
a stable final tie-break. No selection-policy implementation or replacement
publication has occurred; the earlier abstention recommendation is withdrawn.

- [Readable native before/after](../.codex-tmp/learner-refactor/location-label-release/REVIEW.md)
- [Complete comparison with raw pieces](../.codex-tmp/learner-refactor/location-label-release/comparison/REVIEW.html)
- [All changed assignments and preserved optional keys](../.codex-tmp/learner-refactor/location-label-release/delta.json)
- [Published export validation](../models/0a61f6c93657948e0ca20b35/native-validation.json)
- [Independent full-log pipeline replay](../.codex-tmp/learner-refactor/location-label-release/pipeline-replay.json)

## Previous trace boundary delivery (superseded pin) — 2026-09-24

New immutable release: **a9fa27a85ccd066285b99fdb**, manifest SHA-256
`072e4af61179d8f853ddbd4f2a169e34c2f28ed26e0286a03941c3ce2755fbdb`.
Source candidate `762e1b8d5772b08ca08f1440`, learner v27. This supersedes the
v26 delivery below and retains its empty-reason correction. Parser v1.6,
model schema 3, release schema 1 and the ordinary capture interface are unchanged.

The defect was **incorrect identification of a trace PARAM**: the removed
`script-location-frames` declaration swallowed the message's actual file/line
locations. The correction uses the existing general file/line-introduced
parenthetical trace rule, yielding ordinary LOCATOR captures and opaque trace
PARAMs. It does not extract nested locations from an oversized PARAM.

```text
Script system error!
  Error: <KEY> trigger [ <REASON> ]
  Script location: file: <LOCATOR> line: <LOCATOR> (<PARAM>)
    file: <LOCATOR> line: <LOCATOR> (<PARAM>)
```

For the reported tribute-mission message, both file captures are
`events/dlc/tgp/tgp_tribute_mission_events.txt`; the line captures are `1433`
and `319`. Only `tribute_mission.1000:immediate` and
`tribute_mission.0001:immediate` enter the PARAMs. Labels, punctuation,
whitespace and frame order remain intact. Its new template ID is
`6a187968e94c36b0acd622d5`.

Task 4: reload the selected release and invalidate model-dependent caches.
Consume the additional ordinary LOCATOR captures through existing binding
interfaces. Template IDs and slot ordinals can change; do not reuse bindings
from the previous model. No parser repin or nested-location API is needed.
The existing independent pipeline reader/matcher passed replay of all ten complete
native logs: every outcome and capture agrees, including 821250 LOCATOR captures.
Every capture was checked against original file bytes, and every complete log
reconstructed exactly. The owner's example is from an additional native log;
it is a full supported match with the four expected LOCATORs and two PARAMs.
Selection and packaging now pin this release. No caller source change was needed;
production ingestion and SQL were not run.

Same ten-log rebuild: 296 patterns (164 supported / 132 provisional), 290888
full / 61429 provisional / zero unknown or ambiguous occurrences. 553 previously
full occurrences become provisional under the unchanged location-only support
policy: their apparent independent evidence had been file/line variation hidden
inside PARAM. All 36 affected patterns have only one non-location learning form.
This support restriction remains a separate review item, not silently relaxed.
Different numbers of explicit file/line frames can create separate flat templates;
trace interior length and wording remain opaque.

The 73-log boundary audit covers 15563 changed distinct messages / 1165336
occurrences, with zero recognized LOCATOR/trace-PARAM overlaps. Native witnesses
include messages with no parenthetical trace and chains up to 55 trace interiors.
The complete ten-log comparison verifies 38336 inferred member ranges and 37456
captures, without discrepancies. Export replay reproduces all 7864 contextual
rows. This establishes boundary/capture correctness for the checked evidence,
not universal semantic accuracy.

- [Native before/after review](../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/comparison/REVIEW.html)
- [Trace boundary audit](../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/boundary-audit.json)
- [All 36 support regressions and native examples](../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/regression-summary.json)
- [Independent pipeline replay and owner example captures](../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/pipeline-replay.json)
- [Concise readable before/after](../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/REVIEW.md)

## Previous supplemental delivery: empty reason (superseded pin) — 2026-09-24

**Prior model pin: `1d1d6e0389f7235f565b2504`.** Manifest SHA-256:
`110ca10dc94bd9e2cdaebb0c0dfe5f9f4e1c0b86e1285dad82a8d909cb43e3b1`.
This delivery preceded the trace correction above. Its immutable artifacts and
previous release `b1965fa4408ca1bcf36763c9` are unchanged on disk.
Model schema remains 3; source learner candidate is `cca96d77f96382f7082a3f73`,
algorithm v26. This is the corrected ten-log release, not promotion of the wider
learning experiment.

**The raw parser does not need a new version.** v1.6 already returned `[`, the
complete two-space gap, and `]`. Its exact implementation hash remains
`a9ed06a6c141a184939518c0b64292b1b48fda7f09fccc9067b3ecd944bd96d6`.
The defect was in the learner/model construction declaration, which required a
nonempty reason and split that raw gap. A 73-log declaration audit also found
four nonempty reasons whose trailing newline/space gap was split the same way.

The correction is in owner_rules.json, constructions.py and patterns.py:

1. The script reason declaration explicitly sets `allow_empty: true` and permits
   zero content. Complete whitespace runs adjoining the brackets, including line
   endings, stay in the surrounding literal regions.
2. An empty but present REASON is `value=""`, `span=[p,p]`, `optional=false`.
   It is distinct from absent OPTIONAL_KEY (`value=null`, `span=null`). Both ends
   are real raw-piece boundaries. In the reported native message, the reason is
   at message-relative bytes `[73,73]`, immediately before `]`; the two spaces
   remain literal.
3. Inference emits an empty declared field exactly once, then resumes at the
   same raw boundary. No repeated loop, gap splitting, normalization or invented
   reason content. Other slot types and support thresholds are unchanged.

Task 4 should load the newly selected release/rules, retain zero-length capture
ranges and empty strings through matching/binding/storage, and invalidate
model-dependent caches using the new model/manifest identity. Honor explicit
`allow_empty` declarations; do not make every PARAM or KEY nullable. Keep the
ordinary unresolved safeguard for unsupported input, but these five native cases
must no longer enter it because of a declaration-boundary exception. A message
without a supported template can still be genuinely unknown/provisional.

The current Task 4 working tree now has a native schema-3 reader and independent
matcher, so the initial handoff's reader incompatibility is no longer the current
code state. Application integration and SQL verification remain Task 4's work;
this task changes no pipeline caller implementation.

Validation: all 15,558 declared distinct messages / 1,174,352 occurrences in the
73-log raw census have valid field boundaries. Only the five affected messages
(eight occurrences) changed reason ranges. Their original bytes/hashes and
literal-plus-capture reconstruction were verified. The complete ten-log rebuild
retains all 229 patterns (133 supported / 96 provisional), every template ID and
every original capture/outcome; all 21,712 member field ranges still agree.
No synthetic emissions or example-specific rules were introduced.

The Task 4 working-tree reader/matcher was exercised read-only on all five
complete native witnesses using the new release: all return ordinary `unknown`,
with `unresolved_reason=None`, rather than a declaration exception. The ten-log
model has no complete template for these exact formulations; this is not a claim
of successful full classification. Native singleton-derived patterns also verify
the corrected reason captures through the independent pipeline matcher, without
promoting those singleton hypotheses. Source hashes/results are saved in the
[pipeline native probe](../.codex-tmp/learner-refactor/empirical-regions/empty-reason-review/pipeline-native-probe.json).

- [Five complete native cases, before/after](../.codex-tmp/learner-refactor/empirical-regions/empty-reason-review/FINDINGS.md)
- [Native boundary audit and actual raw pieces](../.codex-tmp/learner-refactor/empirical-regions/empty-reason-review/native-field-audit.json)
- [Ten-log regression comparison](../.codex-tmp/learner-refactor/empirical-regions/empty-reason-review/ten-log-comparison/comparison.json)

The separate LOCATOR-only support restriction remains under review; it has not
been changed as part of this boundary correction. Production ingestion has not
been launched.

## Owner review: locations inside trace PARAMs — 2026-09-24

**Corrected in v27: this was an incorrect PARAM boundary, not a missing
nested-location interface.** Owner clarified that the actual file/line locations
must not enter the trace PARAM. The earlier proposal to extract locations out of
that PARAM is withdrawn, and its initial code was removed before any build or
publication. No nested-location schema or consumer API is being introduced.

Native witness: `scope:overlord_scope.culture trigger [ Failed context switch ]`
has two frames in `events/dlc/tgp/tgp_tribute_mission_events.txt`, at lines
1433 and 319. Both learner and pipeline location recognizers already return
the two paths and two line values, with matching raw-piece ranges.

The replacement removes the overbroad `script-location-frames` declaration.
The existing general `located-parenthetical` recognition applies independently
at each file/line introducer. Correct form: `file: <LOCATOR> line: <LOCATOR>
(<PARAM>)`, repeated in native order as present. Parentheses and labels remain
literal; only script-chain interiors are opaque PARAMs. File/line values use the
existing LOCATOR type and byte bindings. See the new delivery above for native
verification and the replacement release.

The same audit verifies the exact orphan-event formulation genuinely contains
no mod-file locator: seven event IDs, 385 occurrences, 55 of the 73 native logs,
all from jomini_eventmanager.cpp. Original-byte witnesses show the next header
immediately after the message, with no hidden location continuation. Engine
header `jomini_eventmanager.cpp:372` identifies the emitter, not a mod-file
location. Other event-source formulations do carry file/line locations.

The owner's succession/travel name examples remain a known contextual typing
inconsistency: the former uses separate KEY slots, the latter a name/title PARAM.
No dedicated name recognition or default literal rules were added; the owner
accepts the current treatment for now.

Evidence, original-byte witnesses, raw pieces and both recognizers' agreeing
location ranges: [owner examples audit](../.codex-tmp/learner-refactor/empirical-regions/empty-reason-review/owner-examples-audit.json).
Parser and pipeline source are unchanged; this correction belongs to the learner
rule registry and regenerated model.

## Delivery and selection

Published revision: **0a61f6c93657948e0ca20b35** under
[models/0a61f6c93657948e0ca20b35](../models/0a61f6c93657948e0ca20b35/manifest.json).
Select it explicitly using [models/selection.json](../models/selection.json).
Model schema: `ck3chronicle.native-message-model`, version **3**.
Release manifest schema: `ck3chronicle.native-model-release`, version **1**.
Source learner revision: `9ee807faa3ab6531dd6036bf`, algorithm v29.

The release packages the model, exact self-contained parser, relative parser
manifest, owner-rule registry and aggregate native replay validation. Artifact
hashes are in its manifest; the selection pins the manifest hash. Raw logs,
observed field values and per-occurrence research records are not in the release.
Template IDs, source applicability, constraints and support summaries are retained.

**Published for pipeline integration; not yet activated in ingestion.** Task 4 has begun native schema-3 reader and matcher integration. Caller migration,
SQL validation and deployment remain with the pipeline team. This delivery does not run `process-pending`.

## Response to the dependency request

| Request | Delivered; remaining pipeline responsibility |
|---|---|
| A1 immutable loadable model | Published compact release, pinned hashes, provenance and explicit loader. Replaying the exported model preserves all native classifications and captures. Application reader/catalog integration remains. |
| A2 selectable raw parser | Packaged `ck3-lossless-v1.6`, with exact bytes/hash and a stdlib-only interface. Learner and reference evaluation use this parser; pipeline input adapter exists. Wire it into application processing. |
| A3 complete native templates | Ordered literal/slot parts preserve whitespace, punctuation, location labels and tails. No normalization step. Complete-member reconstruction and capture evidence agree on the ten logs. |
| A4 slot definitions | KEY, OPTIONAL_KEY, VALUE, LOCATOR, PARAM, plus the subsequently owner-approved REASON. Implement the serialized constraints, including multi-piece KEY and LOCATOR. |
| A5 L1/L2 and tails | Subsequent owner decision supersedes separate L2 template matching: one complete outer diagnostic with intact REASON content. Locations remain outside that reason; recognized traces are PARAM. No permitted-L1/L2-pair list. |
| A6 transparent guidance | Packaged owner_rules.json declares structures and inference policies. Presumed-literal guidance is disabled. No example-specific template or ordinary slot-type override. |
| A7 genuine examples and integration evidence | Complete native training/replay, readable templates/captures and parser comparisons linked below. Real application classifications and stored SQL records still require pipeline verification. |
| B1/B2 inference improvements | Source-specific distinct-message learning; bounded PARAMs precede interior alignment; typed fields have positive evidence. General word-boundary discovery and uncommon formulations remain limited. |
| B3 deterministic error typing | Not delivered by this model. Template IDs and source are not an error-type hierarchy. Requires separate owner-approved work. |
| B4 old incomplete evidence | Current release is regenerated from identified complete native logs. No reconstruction or revival of incomplete old templates. |
| B5 canonical parser | Shared v1.6 selected and frozen in this release; observed recovery/tokenization differences documented. Pipeline must verify its connected path, not retain a second tokenizer. |

## Native results and practical limits

Fresh build on the same **ten complete native logs**, not synthetic or recombined
messages: **343,585 emissions**, **352,317 recovered occurrences**, **7,827 distinct
messages** across **93 source families**. With wrapper context there are 7,864
comparison rows. The 73-log compound-identifier survey was additional read-only
evidence; it was not a 73-log training run for this release.

| Outcome | Count |
|---|---:|
| Supported templates | 165 |
| Provisional hypotheses | 132 |
| Individually confirmed templates | 0 |
| Unique supported-template matches, with unique complete captures | 290,888 occurrences |
| Provisional-only matches | 61,429 occurrences |
| Unknown / competing-template or capture-ambiguous occurrences | 0 in this corpus |

Publication authorizes this revision; it does not silently mark all its templates
`confirmed`. Supported means sufficient distinct evidence under the declared
policy, not an independently measured accuracy claim. One distinct formulation,
including repeated occurrences or location-only changes, stays provisional.

Most provisional occurrences come from two fixed formulations: texture mipmap
size errors (36,319) and `Key poet not found at Database: <LOCATOR>` (18,805).
Their frequency does not create independent non-location learning examples.
Preserve these as provisional diagnostics/review evidence; never discard them
or present them as accepted template matches.

Relative to v27, the v29 correction changes assignments for 25 contextual rows /
217 occurrences, with no outcome changes. The compact published model reproduces
all 7864 contextual results and 37447 message captures, with no export regressions.
All 38311 inferred member field ranges agree with matched ranges. The earlier
trace correction's support changes remain as documented in its dated section.

Remaining quality limits: learning coverage is ten logs, general word-bounded
PARAM discovery is incomplete, and the earlier rich-text/name boundary
formulations still warrant semantic review. Full matching and reconstruction
alone do not establish correct generalization or unseen-log accuracy.

## Loading and raw interface

```python
import json
from pathlib import Path
from template_learning.publish_native_model import load_release

root = Path("models")
selection = json.loads((root / "selection.json").read_text(encoding="utf-8"))
model, parser = load_release(
    root / selection["artifact_directory"],
    expected_manifest_sha256=selection["manifest_sha256"],
)
raw = parser.parse_file(native_log_path)
```

`load_release` validates all artifacts, model identity and parser/rule agreement.
It then verifies and executes the exact packaged parser. If using the existing
research matcher, call `verify_reference_implementation(model)` first: its source
hash guard prevents silently applying changed learner rules to this release.
A pipeline implementation must consume the release's declarations/constraints,
not whichever mutable rule registry happens to be current in the checkout.

Parser version: **ck3-lossless-v1.6**. SHA-256:
`a9ed06a6c141a184939518c0b64292b1b48fda7f09fccc9067b3ecd944bd96d6`.
Its implementation is `parser.py` relative to the release directory.
`pipeline/raw_input.read_raw_log(path, parser_reference=parser.reference.to_dict())`
is also available; it performs no second lexing or SQL work.

| Interface | Meaning |
|---|---|
| raw.source, raw.emissions, raw.parser_reference | Original bytes, ordered emissions, selected parser metadata. |
| emission.span / header_span / body_span | Absolute half-open byte ranges; header ends after the native header prefix, not after the physical line. |
| source_family / source_tag / timestamp / level / ordinal | Native framing facts; family omits the terminal source-code line suffix, while source_tag retains it. |
| emission.recovery | Recovered individual messages, structure, shared ranges and explicit unresolved ranges/reason. Save this result locally rather than recomputing it. |
| recovery.messages | Each message has span, ordinal, text, pieces, tokens and native_bytes(). A multiline failure/reason/trace is one message; supported repeated-error wrappers yield multiple messages. |
| message.pieces | Ordered token/gap pieces with exact text and original absolute byte spans. Spaces, tabs and line endings remain present. |
| recovery.ordered_spans | Shared/message/unresolved ranges in native order, accounting for every emission byte. |
| raw.read_bytes / read_text / bytes_between / text_between | Exact original-source retrieval. Text uses UTF-8 with surrogateescape. |
| raw.save_debug / parser.load_debug | Optional lossless raw snapshots, with replay validation; not an SQL schema. |

An emission extends from one recognized native header to the next, including
continuations. Equal timestamps do not merge emissions. Unsupported framing or
recovery is explicit; no silent byte discard. Parser identity belongs to the Run
(or top-level research context before a Run exists), not every record.

Always-separator punctuation is `: / \ { } [ ] ( ) " = ; |`, individually emitted
even without whitespace. Other edge-punctuation rules preserve dotted symbols,
@ spellings and filename punctuation; Div/0 is the approved whole-token exception.
The parser assigns **no slot types or diagnostic meaning**. Do not put a shadow
lexer, punctuation stripping, quote removal or path normalization after it.

## Model and capture contract

Each `templates` entry carries template_id, source_family, context_kind,
construction_id, parameter_structures, status, learning_support, ordered parts,
and context_patterns. Literal parts contain exact text; slot parts contain their
name/type, optional/prefix/suffix representation and constraints. `display` is a
readable rendering, not the executable matching format.

| Slot | Consumer meaning |
|---|---|
| KEY | Complete identifier field, optionally spanning adjacent raw tokens joined by declared colon tokens. No engine-validity gate; a malformed attempted reference can occupy it. |
| OPTIONAL_KEY | KEY or observed absence; honor explicit optional whitespace/prefix/suffix, without inventing optional literals. |
| VALUE | Exact numeric text satisfying its numeric constraint; do not coerce or normalize it during matching. |
| LOCATOR | A complete recognized path/file or line/range value. Can span many raw tokens. Labels stay literal; filename and separately represented line are separate captures. |
| PARAM | Variable span bounded by this complete candidate. Internal words, punctuation and token count do not contribute to template similarity. A one-token value can fill an established PARAM field. |
| REASON | Intact content of the owner-declared script error reason field. Do not classify its interior or match a second reason template. |

Supported constraints are parser_boundaries, literal_punctuation,
literal_guidance, single_token, key_joiners, location_value, numeric_text,
line_reference, balanced_pairs and declared_field. Reject unknown constraints;
do not ignore them. Presumed-literal constraints are empty in this release.
`owner_rules.json` is transparent data consumed by generic code, not code injected
into source files. Rule updates require a new model release and hash selection.

Matching is case-sensitive and uses complete native messages within their source
family. Construction identity and recognized parameter-structure presence/order
must agree. Complete-message literals delimit slots; their ordinal positions may
shift with variable-length content. No fixed field offsets from training are
used to match a future message. Paths and supported PARAM/REASON interiors are
opaque to wording comparison.

The existing reference is `research_matching.match_record`, backed by
`patterns.analyze_match_pattern`. Evaluate every applicable template and every
complete capture assignment. A first complete or partial match is insufficient.
`full` requires exactly one supported/confirmed candidate and one complete capture
assignment; alternatives are provisional, and no candidate is unknown.
Preserve `insufficient_distinct_learning_examples`, `competing_templates` and
`ambiguous_capture_boundaries` reasons where applicable.

Captures have name, type, value and span. Capture spans are half-open UTF-8 byte
ranges **relative to the message**, while raw parser spans are **absolute in the
source file**. Add message.span.start to convert body capture coordinates.
For wrapper prefix/suffix captures use that context range's own start instead.
An absent OPTIONAL_KEY has no value range. Preserve native bytes when materializing
records; never convert these offsets into Python string indexes.

For located-message wrappers, use `records.context_for(emission, recovery)` to
obtain context_kind, exact prefix/suffix pieces and their absolute ranges.
Reference matching uses SequenceRecord with these contexts keyed by their content
identity. A child cannot be classified without its applicable wrapper context.

## Concrete effects for callers

These are excerpts of observed native messages, not constructed test emissions.
Complete messages, actual pieces and captures are in the linked native reviews.

| Native content | New representation / caller consequence |
|---|---|
| `Unexpected token: title:h_china.holder, near line: ...` | Raw title, colon, h_china.holder remain separate pieces; the candidate captures title:h_china.holder as one KEY and the line as LOCATOR. |
| `Failed converting statement for 'war_goal_title.GetName'` | The whole quoted interior is PARAM in this candidate, supported by other actual expressions in this same formulation. A shorter value does not change its field type. |
| `[LOD_0&#124;decal_world&#124;decal_worldShape]` in a mesh error | Interior has five raw tokens; a supported region is one PARAM. No whitespace or nesting prerequisite and no pipe-specific rule. |
| `most recent:file: common/on_action/ccu_on_actions.txt line: 14 (ccu_culture_created)` | recent:file stays native template wording; path and line are LOCATORs, trace interior PARAM. Colon adjacency does not independently create a KEY field. |
| `Script system error! ... Error: culture trigger [ ... ] ... Script location: ...` | Outer template uses KEY trigger, intact REASON, and `file: <LOCATOR> line: <LOCATOR> (<PARAM>)` for each frame. Trace interiors stay opaque. Different frame counts can require distinct flat templates; a complete location chain must not become PARAM. |
| `scope:title:e_western_roman_empire` in the multiple-colon error | Its raw pieces are scope, colon, title, colon, e_western_roman_empire. KEY syntax permits the attempted reference; the single survey occurrence does not itself establish a supported template. |

## Responsibilities outside the parser

| Functionality | Owner |
|---|---|
| Distinct-message aggregation, occurrences, source-specific grouping and template inference | Learner. Repeated observations do not add independent support; raw parser never deduplicates. |
| KEY/PARAM/LOCATOR/VALUE/REASON recognition and constraints | Learner/model defines fields; classifier applies the model to raw pieces. |
| Location labels, path value interpretation, trace/reason meaning | Model and classifier; all original wording survives parsing. |
| Evidence IDs, Run identity, persistence and diagnostic deduplication | Pipeline. Keep parser/model identities at Run scope. |
| Individual-message recovery from native continuations | Shared versioned parser. No separate caller recovery heuristic. |

These are the functional responsibilities retained outside raw parsing, rather
than features to delete. All other changes were removal of deprecated / incorrect
architecture.

A diagnostic stored in SQL must contain all content/context needed to understand
it, including locations from a shared wrapper. Materialize that context before
within-Run deduplication. Do not make reports join an emission record or reopen a
log to recover missing diagnostic meaning. Verbatim repeats become occurrences;
the parser itself does not perform that deduplication.

## Pipeline integration order

1. Implement the explicit v3 model/release reader and selection. Package the pinned
   artifacts with the application; validate the selected manifest and file hashes.
2. Connect the selected parser to input processing. Consume recovery.messages and
   unresolved outcomes; retain message and wrapper ranges. Remove duplicate
   tokenization assumptions from the connected path.
3. Implement complete-message source-specific matching, six slot types and all
   constraints, construction/parameter declarations and exhaustive ambiguity handling.
4. Materialize complete diagnostics and context, then deduplicate and persist.
   Supported unique matches and provisional/unknown evidence remain distinguishable.
   Keep the native review shard self-contained for unresolved material.
5. Replay the same complete native logs through the application. Compare recovered
   messages, exact captures, wrapper context, provisional reasons and SQL/report
   records with the delivered reference results. Cache keys must include evidence
   digest, parser version/hash, model revision/hash and feature/matcher version.
   Rebuild caches when these change; no old-format fallback.

## Evidence, reproduction and review

- [Fresh native comparison, including actual PARAM values and raw pieces](../.codex-tmp/learner-refactor/empirical-regions/publication-review/REVIEW.html)
- [All comparison counts and member-range checks](../.codex-tmp/learner-refactor/empirical-regions/publication-review/comparison.json)
- [Complete ten-log packaged-parser replay](../.codex-tmp/learner-refactor/empirical-regions/publication-review/parser-replay/summary.json)
- [Fresh build command and exact input paths](../.codex-tmp/learner-refactor/empirical-regions/empty-reason-ten-02/command.json)
- [Source candidate and full research evidence](../.codex-tmp/learner-refactor/empirical-regions/trace-boundary-review/candidate/762e1b8d5772b08ca08f1440/manifest.json)
- [Native 100-case framing/recovery before/after appendix](../.codex-tmp/parser-100-review/INDEX.md): historical lexical version; use v1.6 for current token boundaries.
- [v1.6 punctuation correction and native comparisons](LEARNER_SEPARATOR_FIX.md)
- [Model details](LEARNER_NATIVE_MODEL_CONTRACT.md) and [parser specification](LEARNER_PARSER_SPEC.md)

The release records the training input hashes and source candidate manifest hash.
Rebuild with the saved learner command, then invoke
`python -B -m template_learning.publish_native_model --bundle <candidate> --output-dir models`.
Existing revision contents cannot be overwritten with different artifacts.
Generated reviews/raw evidence stay ignored; transfer them separately when another
checkout needs the native examples. The published model and this formal reply
are the shared-repository delivery requested by the owner.
