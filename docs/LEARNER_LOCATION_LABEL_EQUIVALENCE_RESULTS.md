# Line-label equivalence — 2026-09-28

## Assessment after owner-requested before/after audit

**The two-log evidence demonstrates no native coverage gain from v43 to v44.**
Under the same learning procedure, all native assignments retain their status,
slot values, spans and supporting components. Definitions change only by the
declared line-label alternatives. This is evidence of preserving the observed
behavior while broadening the allowed label spelling, not proof of improved
discovery, reduced fragmentation or future classification quality.

The initial report was inadequate: it listed agent-chosen checks without a
version-matched baseline or a model-evolution audit. Those checks were not
owner-approved model-quality acceptance criteria. Passing them did not establish
that this implementation should be accepted or published.

The audit also distinguishes **fresh versus additive learning**. The retained v43
two-log candidate had 208 templates; the reported v44 candidate had 203. They
used different procedures. The corresponding v43 fresh build also has 203, and
the corresponding v44 additive build also has 208. The five-template difference
must not be attributed to the line-label change.

## Controlled before/after comparison

All comparisons use the same complete native inputs, parser hash, threshold and
recovery associations. The additive order is `9d3622…` then `10cbdc…`.
The old implementation is the retained, hash-verified v43 source snapshot; no
old model was imported into v44. The fresh v43 baseline was reconstructed during
this audit. The other five checkpoints were already retained.

| Procedure / evidence | v43 definitions (supported / provisional) | v44 definitions (supported / provisional) | Supported / provisional / unmatched occurrences, both versions |
|---|---:|---:|---:|
| First complete log | 183 (140 / 43) | 183 (140 / 43) | 15,078 / 9,034 / 0 |
| Both logs, fresh build | 203 (155 / 48) | 203 (155 / 48) | 91,462 / 9,159 / 0 |
| First log, then add second | 208 (159 / 49) | 208 (159 / 49) | 91,461 / 9,160 / 0 |

The two-log comparison covers **4,027 distinct bodies, 4,062 contextual records
and 100,621 original occurrences**. Contextual records preserve different native
wrappers for the same body. The audit compared exact bodies, parser pieces,
wrappers, continuations and every original occurrence association before comparing
assignments; all agree across the paired versions.

For both fresh and additive version pairs:

- No previously matched native occurrence becomes unmatched; none becomes newly
  matched. No supported/provisional assignment changes status.
- No selected slot type, value or byte span changes, including wrapper and
  continuation captures. No selected competing-template count changes.
- Every old definition has a corresponding new definition with the same remaining
  wording, fields, constraints, source/context applicability and supporting
  structure after projecting only the declared line-label equivalence.
- All corresponding definitions retain their native member sets, selection
  evidence and support statuses: 203/203 fresh and 208/208 additive.
- In the additive pair, 100 body-template IDs change because their literal
  definition now contains the alternatives. They account for 2,152 contextual
  records / 17,672 occurrences. This is a declaration/identity change, not a
  discovery of 100 additional error formulations.

The full [208-definition ledger](../.codex-tmp/learner-location-label-equivalence/comparison/v43_additive--v44_additive.json),
[fresh-build ledger](../.codex-tmp/learner-location-label-equivalence/comparison/v43_fresh--v44_fresh.json)
and [assignment comparison](../.codex-tmp/learner-location-label-equivalence/comparison/summary.json)
record the IDs, memberships, definitions, counts and differences. The definition
projection is an audit comparison, not a replacement matcher or text normalization.

## Concrete native examples

**Unknown trigger, `pdx_persistent_reader.cpp`.** Native recovered body:

```text
Unknown trigger: adulterer, near line: 414
```

| | Template body | Outcome |
|---|---|---|
| v43 `7e772a454a300b1d24e7f261` | `Unknown trigger: <KEY>, near line: <LOCATOR>` | Supported |
| v44 `01adbdfa8f9244dfd17710d6` | `Unknown trigger: <KEY>, {line:\|near line:} <LOCATOR>` | Supported |

The body still captures KEY `adulterer` at bytes `[17,26)` and LOCATOR `414`
at `[39,42)`. Its complete native wrapper still captures
`common/scripted_triggers/zzz_99_religious_triggers.txt` and line `415`.
The shown contextual example occurs 22 times; the family covers 284 contextual
records / 1,842 occurrences in both versions. The new definition admits the other
label spelling; this native example already matched before and shows no coverage
improvement. No assertion is made that this exact error was observed with `line:`.

**DLC descriptor, `dlc_descriptor.cpp`.** Native body (leading space and CRLF
are retained in the linked evidence):

```text
 Invalid supported_version in file: mod/ugc_2218867072.mod line: 7
```

v43 `b5c4e63e487a7c744dbf22c1` ends `file: <LOCATOR> line: <LOCATOR>`;
v44 `18ab0aa08d6b4985bc8ac6c4` ends
`file: <LOCATOR> {line:|near line:} <LOCATOR>`. Both select supported assignments,
with the same path and line captures. The example occurs twice; the family covers
51 contextual records / 102 occurrences in both versions. Again, the observable
change is the accepted declaration, not a newly classified native message.

**Unchanged diagnostic wording.** The complete `untyped effect` / literal
`Script location: Unknown` template remains `d9f8268f8306c6c4b5ca77a7` in both
versions. Its one body / 8,880 occurrences remain provisional, with the same opaque
REASON capture. Neither repetition nor the line-label rule promotes it.

Exact bodies, complete wrappers, old/new captures, original ordinals and source
spans are retained in the
[native example ledger](../.codex-tmp/learner-location-label-equivalence/comparison/v43_additive--v44_additive-examples.json).

## Evolution as the second log arrives

This evolution is identical in v43 and v44, after mapping IDs changed by the label
declaration. All 35 recorded lifecycle events agree; see
[lifecycle comparison](../.codex-tmp/learner-location-label-equivalence/comparison/lifecycle-equivalence.json).

- All 140 previously supported definitions survive.
- Four provisional definitions become supported: history title-holder evidence
  grows from 1 to 10 distinct examples; duplicate-event, title-holder assertion
  and GUI-layout evidence each grow from 1 to 2.
- Three provisional fixed observations retire into supported KEY formulations.
- Twenty-eight definitions are discovered from the cumulative open evidence:
  15 supported and 13 provisional. Thus `183 + 28 - 3 = 208`.
- On the first log alone, 11 formerly provisional occurrences become supported;
  9,023 remain provisional and all 15,078 supported occurrences stay supported.

For a concrete retirement, v44 `872fb81ed7e7d31f50bd58bd` fixes the malformed
token as `@provisions_cost_infantry_cheap`. After additional native token values
arrive, supported successor `e9c7a6cdb699dcb181672139` is
`Malformed token: <KEY>, {line:|near line:} <LOCATOR>`.
The retained evidence includes `+10` at lines 10 and 11, alongside the earlier
`@provisions_cost_infantry_cheap` observation. The retirement reason is
fixed observation inside an independently established KEY field. The same
retirement happens under v43's exact-label definitions; it is not a benefit
introduced by v44. Full predecessor/successor wording, support and native witnesses
are in [evolution.json](../.codex-tmp/learner-location-label-equivalence/comparison/evolution.json).

## Degradation and limitations exposed by the audit

There is **no observed version-induced native regression in this two-log sample**.
That does not prove the broader accepted language is correct on future messages.
The sample has not demonstrated a previously rejected native spelling becoming a
complete match. Earlier in-memory spelling swaps are implementation controls,
not native evidence of improvement or owner-approved acceptance criteria.

There is an actual **procedure-dependent loss of generalization** that the initial
report omitted. Fresh versus additive builds differ in selected definitions and
captures for 104 contextual records / 116 occurrences across four families:

| Family | Contextual records / occurrences | Fresh build | Additive build |
|---|---:|---|---|
| Culture innovation history | 86 / 90 | Innovation is KEY | Retains separate `innovation_armilary_sphere` and `innovation_baliffs` literals |
| Religious-head succession | 8 / 12 | Faith/title/expected-faith are KEYs | Retains observed constant combinations |
| Character-history trait | 6 / 9 | Character markup IDs are KEYs | Retains separate character-ID literals |
| Character holding after history | 4 / 5 | Character and holding are KEYs | Retains a numeric-character/b_canterbury formulation and a fixed provisional observation |

Concrete native example:

```text
 Character 'nidaros_bishop_1' holds 'b_eynafylki' after history, but has higher titles and doesn't hold the de jure county
```

The fresh build selects supported `c79e97f29c3899f3d8ea2009`, with both values as
KEYs. The additive build selects provisional `f45e3539f1adc5f2227474bb`, fixing
both values as literals. That is one native occurrence with a worse support
outcome relative to fresh learning. It is already present in v43, and persists
unchanged in v44. It is not a supported-to-provisional regression within the
additive timeline: this example arrives in the second log.

Retaining already supported narrow definitions and discovering from open evidence
can preserve incidental constants instead of learning the generalization a fresh
joint build finds. These results warrant review of that policy; they do not
authorize a fix here. No previously matched occurrence is lost in this sample,
but equal match counts conceal these differences in representational breadth.
See the [procedure comparison](../.codex-tmp/learner-location-label-equivalence/comparison/v44_fresh--v44_additive.json)
and its [native examples](../.codex-tmp/learner-location-label-equivalence/comparison/v44_fresh--v44_additive-examples.json).

No inference or matcher code was changed during this audit. No package was
published or selected. The implementation remains subject to owner review.

## Implementation scope

Owner authorized `line:` and `near line:` as interchangeable introductions to
the same line LOCATOR. Learner v44 now discovers one template with finite literal
choices, even when training supplies only one spelling. It neither captures
`near` as KEY/OPTIONAL_KEY nor rewrites the input. This supersedes the earlier
line-label policy that deliberately produced separate exact templates.

The active package/model/selection remain unchanged. No candidate was published,
no production processing ran, and no 73-log retraining was performed. The separate
v43 additive applicability defect remains unresolved.

- `owner_rules.json` explicitly declares `["line:", "near line:"]` for the
  line-location group. File-label behavior is unchanged.
- `patterns.py` recognizes complete label token ranges immediately before an
  independently recognized numeric LOCATOR, outside opaque fields. Alignment and
  similarity use a common label position. Native pieces and bodies stay exact.
- A literal part retains `kind: literal`, canonical `text: line:`, the declared
  `alternatives`, and `location_label: line-location`. It is never a slot.
  Retirement/consolidation retain this distinction from ordinary fixed literals.
- The shared validator checks the exact declared choices, unique nonempty
  prefix-free spellings, and adjacency to a required numeric LOCATOR. The shared
  matcher accepts either literal and still checks every other literal, field,
  source, construction, structure, wrapper and supporting component.
- The selected body/wrapper layout carries ordered
  `literal_choices: [[part_index, alternative_index], ...]`. Matching verifies
  exact native reconstruction. Contract preparation preserves the choices;
  stored rendering resolves them without matching or reading the log again.
  Choices participate in exact diagnostic identity, so different native spellings
  share a template but remain distinct stored messages.
- One observed spelling does not count as two examples. Support and provisional
  eligibility are unchanged; declared alternatives supply no invented evidence.

The new representation is explicitly **model schema 5 / matcher API v2**.
The parser remains `ck3-lossless-v1.7`, and the selector remains
`complete-assignment-v2`. Existing `error-contract-v1` selected-layout semantics
carry the new choices. The active package still executes its own pinned schema-4 /
API-v1 code. New learner state cannot import v43 templates; an existing selected
package is not edited to acquire this behavior.

## Evidence and verification

Research results, exact native evidence and the isolated unpromoted candidate are
under [the task evidence directory](../.codex-tmp/learner-location-label-equivalence/).
[verification.json](../.codex-tmp/learner-location-label-equivalence/verification.json)
records the exact learner identity, model revision, inputs and candidate path.
Candidate revision is `6afef6948c1535e6d96126f5`; learner SHA-256 is
`2988d6fb02b51f4226fd6e025a21496062a518227f81607c4f45cc72fa1313cf`.
The two-log build contains 203 definitions (155 supported / 48 provisional) and
4,027 distinct native messages. Its 100,621 recovered occurrences reconcile to
91,462 supported assignments, 9,159 provisional assignments and zero unmatched.
This is training replay, not an unseen-accuracy result or a promotion recommendation.

The seven agent-chosen implementation checks pass
([log](../.codex-tmp/learner-location-label-equivalence/verified-tests.log));
they include native label positions in 2,117 distinct bodies and explicit
spelling-swap controls across 100 selected template definitions. Four existing
date checks also pass
([log](../.codex-tmp/learner-location-label-equivalence/date-regression.log)).
All eight existing additive checks pass, including cumulative registry learning,
settled-template retention, provisional promotion/retirement, field support and
the two exact untyped/Unknown constructions
([log](../.codex-tmp/learner-location-label-equivalence/additive-regression.log)).
That is 19 passing implementation checks across the three suites, not a model-quality
acceptance decision. The before/after findings above govern the assessment. Scoped whitespace checks
also pass. No general legacy test suite or full-corpus performance comparison was
run; concurrent test wall times are not a learner performance benchmark.
The review JSON export preserves literal alternatives and verifies counts for
its 20 selected definitions / 58 native examples
([log](../.codex-tmp/learner-location-label-equivalence/visual-review-verified.log)).
That viewer also needed a small pre-existing assertion corrected: an unambiguous
provisional template is not a competing-template conflict. No inference or status
rule was changed by that viewer correction.

The selected classifier was loaded and exercised separately against the complete
affected log; one selected line-bearing message passed original-byte binding,
record preparation and exact rendering. The loaded package is still
`44a0401b8adf0a2953d26705`, model `76630685c4a341ca14bf9c7c`, API v1
([check](../.codex-tmp/learner-location-label-equivalence/selected-package-check.json)).

Native recovery starts from two complete retained logs with SHA-256:

- `9d3622ab1b6c85cbab45d83767bb870b06c6fb9d6da50ee44f5eba3674d98cbc`
- `10cbdcb23e34a5b571a16eb52d390e5e676663936f000fd43404af19d85027fb`

The requirement checks cover both observed spellings, complete native replay,
exact JSON-only rendering, actual classifier binding/preparation, single-example
provisional status, opaque REASON/full-ID/PARAM boundaries, literal Unknown,
invalid declarations/layout choices, and unchanged source/wording restrictions.
Explicit in-memory spelling-swap controls check that the same template and field
values survive either spelling. These controls are **not observed CK3 emissions**,
are never written as logs, and do not enter training or native occurrence counts.
They do not establish that one genuine native formulation was emitted both ways.

Commands from the checkout (all Python uses the repository environment):

The six exact checkpoint paths, input hashes, procedures and learner identities
are in [comparison/provenance.json](../.codex-tmp/learner-location-label-equivalence/comparison/provenance.json).
The v43 fresh baseline is `99cc1cf8c926992006abc5bc`; the corresponding v44 fresh
baseline is `6afef6948c1535e6d96126f5`. The additive pair is
`aaae9d23a9a2fd3b85c10775` → `39cb19ab0ea10a48ebb98a46`.
Their first-log parents are `e8c7ffbee2d74f07d696c590` and
`0a75fda0b9e203af2d3a4baf`, respectively.

Reproduce the v43 fresh baseline using the preserved implementation (choose a
fresh ignored output directory). Its bundle manifest retains the complete input
paths and build arguments. The source identity must equal
`8a1d1b067008a3d776b4496209e4b36c6bb7523923b28a7081be8deae216cbcc`:

```powershell
$learnerArgs = @('--parser-manifest', 'tools/template_learning/parsers/v1_7/manifest.json',
  '--output-dir', '.codex-tmp/learner-location-label-equivalence/comparison/v43-fresh-reproduction')
foreach ($entry in (Get-Content .codex-tmp/learner-date-key/inputs.json | ConvertFrom-Json)) {
  $learnerArgs += @('--log', $entry.path)
}
.\.venv\Scripts\python.exe -B -c 'import sys,json; from pathlib import Path; sys.path.insert(0,str(Path(".codex-tmp/learner-all-logs-v42/additive-source").resolve())); from template_learning.artifacts import learner_identity; assert learner_identity()==json.loads(Path(".codex-tmp/learner-all-logs-v42/additive-source/identity.json").read_text()); from template_learning.learn_error_templates import main; main()' @learnerArgs
.\.venv\Scripts\python.exe -B .codex-tmp/learner-location-label-equivalence/comparison/compare.py
.\.venv\Scripts\python.exe -B .codex-tmp/learner-location-label-equivalence/comparison/evolution.py
```

The last two commands read the retained paths in their scripts and reproduce the
evidence comparison, not new inference. The comparison authenticates bundle file
hashes and checks identical native associations. It uses retained complete matcher
results; it does not introduce a second matcher. No controlled spelling mutations
enter this native before/after comparison.

Earlier implementation-check commands, retained for reproducibility rather than
as an acceptance policy:

```powershell
$env:CK3_LOCATION_NATIVE_INPUTS = '.codex-tmp/learner-date-key/inputs.json'
$env:CK3_LOCATION_OUTPUT = '.codex-tmp/learner-location-label-equivalence'
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_learner_location_label_requirements.py -v
$env:CK3_ADDITIVE_NATIVE_INPUTS = $env:CK3_LOCATION_NATIVE_INPUTS
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_learner_additive_requirements.py -v
$env:CK3_DATE_NATIVE_INPUTS = $env:CK3_LOCATION_NATIVE_INPUTS
.\.venv\Scripts\python.exe -B -m unittest discover -s tests -p test_learner_date_requirements.py -v
```

The scope is these exact, case-sensitive labels before line numbers/ranges.
Internal label whitespace variants, file-label interchangeability and different
surrounding error wording have not been newly authorized as aliases. Native
spacing outside the labels remains part of the template. This work does not
establish future coverage or authorize promotion of its research candidate.
