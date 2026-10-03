# Learner v45 release delivery

2026-09-28. Owner scope: deliver a replacement learner/model package for Task 06
integration, targeting model schema 5 and matcher API v2. Active selection and
production processing are separate work. The immutable replacement is package
`68f1ae5db205ab46afef9c4d`, model `f5cde2616f35d563118d3d32`.
All original 122 cases receive complete assignments. Across the broader corpus,
four occurrences remain unmatched; capture/status regressions are recorded below.
[Retained delivery evidence](../.codex-tmp/learner-release-v45/).

## Implementation boundary

The additive wording check previously compared a new proposal against retained
body patterns without applying the complete matcher's source/context/construction/
ordered-parameter gates. Four-frame comparison diagnostics could veto a one-frame
proposal: the body-only pattern swallowed the retained word `character`, even
though complete matching rejected that reference at the parameter-structure gate.
The historical rejected proposal was `3db1f37cb4f7356e76e701ba`; its incompatible
references included `8d93e1f93c13c1ad8f1fb7c0` and `ca7b575df254fc1c68d4dfd6`.

`Rules.applies_to_record` now owns the same existing gates for matching and
additive wording checks. Refinement partitions use complete retained matches.
The fix does not change protected wording, field definitions, support thresholds
or same-structure wording-loss policy. Retained native proposal replay shows the
one-frame proposal accepted while the travel/activity proposals keep their
wording-loss rejections. See the focused check in
[test_learner_applicability_requirements.py](../tests/test_learner_applicability_requirements.py)
and [historical native decisions](../.codex-tmp/learner-all-logs-v42/unmatched-73-derivation.json).
Those checks were chosen to verify the implementation; they are not owner
acceptance criteria or proof of model quality.

Earlier authorized changes remain: singleton dotted dates become KEY; full IDs
stay opaque; the two explicit untyped-effect/untyped-trigger bodies end in literal
`Script location: Unknown`; `line:` and `near line:` are finite literal choices
before numeric LOCATOR; supported complete unambiguous assignments remain settled
within one exact learner identity. Provisional evidence remains open for refinement,
promotion and proved retirement. There are no cross-version template imports.

## Native corpus and procedure

All 73 complete retained input hashes were verified: 596,625,707 bytes, in the
agreed SHA-256 inventory order, with cumulative checkpoints at 20, 40, 60 and 73
logs. The corpus is the agreed readable inventory, not every possible log on the
machine: the earlier inventory documents duplicate copies and inaccessible pending
files. No copies, artificial Runs or rewritten messages supply independent evidence.

The build reuses only the complete native recovery snapshot. Its input hashes,
parser identity, recovery-code identity and snapshot digest are checked in
[preflight.json](../.codex-tmp/learner-release-v45/preflight.json). No inferred
templates come from that snapshot. The package replay reparses every original log.
Learning starts from empty state under v45, then extends its own preceding
checkpoint. The frozen source, input paths, per-stage timings, complete native
members and decisions remain in ignored evidence.

Learner `outer-diagnostic-consensus-v45`, implementation SHA-256
`025c98f6ca84cab8b6ea3b81e76f9517d166ee2090a81ed4878313122ae6a088`.
Parser `ck3-lossless-v1.7`, SHA-256
`a8005254df58daf20e000e454c9e3e9b40304be4cd0962e1fa88e90cea86baab`.

Comparisons distinguish the selected thirty-log package, the retained fresh v42
thirty-log build, and the prior v43 73-log additive build. The latter uses the same
batch membership/order but predates the literal-choice representation and this
applicability fix. The smaller v44 matched-procedure comparison isolates the
literal-choice change on its two native logs; it is not a 73-log result.
There is no completed fresh all-at-once 73-log baseline: that earlier run was
stopped. Training-corpus replay measures observed behavior, not unseen accuracy.

## Delivery assessment

The replacement candidate is `c4f174d947fbc531aba35fb7`: **689 definitions
(492 supported, 197 provisional)** over 133 sources, 90,506 distinct message
identities and 91,925 complete contextual inputs. Its 2,594,588 recovered
occurrences come from 2,517,940 native emissions. There are no unresolved
recoveries. These are different counting units, not inferred-template counts.

| Model, evaluated on the same 73 logs | Supported assignments | Provisional assignments | No complete match |
|---|---:|---:|---:|
| Selected v41, trained on 30 logs | 1,472,966 | 1,002,506 | 119,116 |
| Fresh v42, same 30-log membership | 1,473,026 | 1,002,506 | 119,056 |
| Earlier v43, 20 + 20 + 20 + 13 | 2,396,084 | 154,876 | 43,628 |
| Replacement v45, 20 + 20 + 20 + 13 | 2,439,711 | 154,873 | 4 |

Relative to the selected package, 119,114 formerly unmatched occurrences gain a
complete assignment and **two formerly matched occurrences are lost**: net gain
119,112. Another 911,957 provisional occurrences become supported, while 72 go
from supported to provisional. Status changes are not newly discovered
formulations or new coverage: both statuses were already eligible records.
All original thirty-log training occurrences still have complete assignments.

Relative to the earlier 73-log additive model, 43,624 occurrences gain complete
supported assignments, with **no additional lost matches**. Five occurrences
move from provisional to supported and two move the other way. The four remaining
misses are the same four as before. The comparison is not a uniformly improving
capture/wording result; the changes below matter for review.

The [comparison summary](../.codex-tmp/learner-release-v45/assessment/summary.json)
separates original30/added43 cohorts and every status transition.
[Changed assignments](../.codex-tmp/learner-release-v45/assessment/changed-assignments.jsonl)
and [grouped examples](../.codex-tmp/learner-release-v45/assessment/changes.json)
retain native text, IDs, old/new fields and byte spans. Before-results come from
the retained authoritative matcher runs; their assignment-file digest is recorded.
New results come from the v45 build and are checked again during immutable export.

### The demonstrated applicability defect

New supported definition `b93cd68fb7b8374d173b423e` is derived from four genuine
comparison bodies and covers all **43,624** affected occurrences. Its complete
form includes the Script system error opening, comparison wording, a bounded
PARAM for the type comparison, and the entire one-frame Script location tail.
It retains exactly one `located-parenthetical` structure. The two earlier
four-frame references cannot pass that same structural gate. The new definition
does not absorb their incompatible structure or retire their definitions.
See [definition and native member IDs](../.codex-tmp/learner-release-v45/comparison-family-definitions.json)
and the no-match-to-template entries in the comparison ledger.

### Capture improvements and regressions

Compared with the selected thirty-log model, **936 contextual inputs / 518,946
occurrences** change captures among mutually matched messages. This combines
training exposure, the earlier support policy, additive learning, date handling
and literal-choice changes; it is not an isolated effect of the applicability fix.
For example, `Key poet not found at Database: common/traits` now captures `poet`
as KEY instead of fixing it as wording (334,197 occurrences). The analogous
localization diagnostic now captures its leading trigger identifier, including
`house_equal`, while retaining the explanatory sentence. Two contextual inputs
in that family account for 180,396 occurrences. These few formulations dominate
the weighted capture difference; the full ledger preserves the remaining breadth.

Against v43's identical batch procedure, **28 contextual inputs / 63 occurrences**
change captures:

- Nineteen inputs / 54 occurrences have a fifteen-frame trigger error. Both
  versions already have two equally ranked complete candidates. The selector's
  unchanged ID tie-break previously chose fixed `house.house_head`; schema-5 IDs
  choose the candidate capturing it as KEY. Status remains provisional. Old
  IDs `a10fdff423dd408777a5c404` / `a21aee9371859c2086672d35` become
  `24caa282ff8270fe165149d0` / `0b34413cf6d714d7293ef7e4`. Both ranks are
  `[0,0,0,-5]`. This is a representation-sensitive tie-break, not new evidence
  of greater confidence. [Exact example](../.codex-tmp/learner-release-v45/tie-change-example.json).
- Seven travel-debug inputs / seven occurrences regroup names and textual dates.
  Some fixed years become VALUE; two earlier fixed observations gain variable
  name/location fields. In the Farida example, `Jun` becomes literal and two
  supported candidates tie, changing the final assignment to provisional. The
  `1178.10.1` date rule does not cover textual month formats, and no broader date
  rule was silently added.
- Two rich-text relationship inputs / two occurrences change name-field layouts.
  One trades captured `de` for captured `root`; the other falls back to a singleton
  definition with fixed rich-text names/IDs and becomes provisional. These are
  capture/generalization regressions requiring review, even though exact native
  matching remains possible. They are not changes to opaque CHARACTER_FULL_ID.

The last two bullets reflect different grouping/refinement outcomes under the
combined authorized changes. There is no full-corpus v44 intermediate run to
separate their causes experimentally. The retained
[40-log membership differences](../.codex-tmp/learner-release-v45/checkpoint-40-member-changes.json)
and per-checkpoint template-evolution files expose the actual definitions and
members. They must not be described as cosmetic ID changes.

The wording audit also retains the earlier concerns about an activity PARAM
containing `Grand Tour` and a quoted KEY containing `trait`. The new audit flags
`Cill Chainnigh` moving inside a bounded PARAM in one travel-debug observation.
These are review findings, not proof that all PARAM/KEY captures are wrong.
[Wording evidence](../.codex-tmp/learner-release-v45/assessment/wording-review.jsonl)
and [earlier field-boundary assessment](../.codex-tmp/learner-all-logs-v42/wording-review-detail.json)
retain the native values and surrounding wording.

### Four remaining unmatched occurrences

| Family | Distinct bodies / occurrences | Complete proposed definition | Actual stopping rule |
|---|---:|---|---|
| Starting travel with incorrect receiver | 2 / 2 | `a95fc969f6fded7e3d2a6918` | Existing word-run protection prevents old Caliph/Jophé wording becoming KEY values. |
| Aborting travel while participating in activity | 2 / 2 | `960123704cb4d27bf3e915fc` | The same policy protects fixed Grand Tournament against the new Grand Wedding/Hunt values. |

Both proposals have supported evidence and completely match their two respective
native bodies. Both are rejected before retention/publication, and each proposed
refinement has only one group with no matching predecessor IDs, so no smaller
groups are re-inferred. Consequently no suitable published definition reaches
runtime. This is not insufficient repetition, rejection of a valid full ID, or a
runtime prohibition on provisional records. The travel-debug pair are the two
matches lost relative to the thirty-log baselines; the activity pair were already
unmatched there. [Native proposals, captures and exact rejection events](../.codex-tmp/learner-release-v45/remaining-unmatched-traces.json).

Concretely, retained reference `cdc83d0ad425f8f57ea2fc65` contains literal runs
`receiver is Caliph` and `default location is Jophé`. The proposal preserves
`receiver is` and `default location is`, but the rule rejects even the individual
value words moving into KEY because they belong to those established multiword
runs. Activity reference `3b4494600bba2071fef6de54` similarly protects
`Grand Tournament`. This is the policy assumption needing review, not a claim
that these values are inherently constant or malformed.

### Original Task 06 cases

All **122 bodies / 9,153 occurrences** have complete assignments using **28
definitions**: 118 bodies / 267 occurrences supported, four bodies / 8,886
occurrences provisional (indices 1, 8, 52, 88). This is the broad-corpus result;
the earlier two-log candidate's supported/provisional split was different.
[Stable-index comparison ledger](../.codex-tmp/learner-release-v45/assessment/review-122.json).

Case 20 selects `4f26298c4e632cfe02b9b548`. The complete `Date ...` prefix stays
present: date KEY `[6,15)`, title KEY `[23,34)`, opaque CHARACTER_FULL_ID `[55,135)`.
Eberhard's apostrophe and compound native spelling remain inside that one field.
Case 1 selects `d9f8268f8306c6c4b5ca77a7`, capturing only REASON `[48,129)`;
`untyped effect` and `Script location: Unknown` remain literal. Its 8,880 exact
repetitions remain one distinct example, hence provisional. The paired trigger
declaration is still the separately confirmed complete Unknown-ending body,
not a general effect/trigger declaration. Historical causes and every original
case remain in the [root-cause report](LEARNER_UNMATCHED_REVIEW_ROOT_CAUSE_RESULTS.md).

## Evolution within this learner version

| Logs | Candidate revision | Supported / provisional definitions | Supported / provisional / unmatched occurrences |
|---:|---|---:|---:|
| 20 | `78878bcc7909a6270594404e` | 247 / 115 | 545,688 / 126,210 / 0 |
| 40 | `4341892dd830c73b0b39e63a` | 346 / 164 | 1,203,790 / 287,540 / 0 |
| 60 | `a42328154f2888e92d9e74b5` | 481 / 201 | 1,686,767 / 461,674 / 2 |
| 73 | `c4f174d947fbc531aba35fb7` | 492 / 197 | 2,439,711 / 154,873 / 4 |

All earlier supported definitions survive; **30 definitions promote and 50 retire
with explicit successor/reason records**. No previously matched native input
becomes unmatched within this chain. At 40, 60 and 73 logs respectively,
41,583 / 84,391 / 87,914 distinct messages remain settled, while
1,149 / 4,098 / 2,592 return to discovery.

Retaining definitions does not freeze the final selection when new competing
definitions appear. At 60 logs, 21 previously supported occurrences become
provisional across seven contextual inputs; all 21 transitions are deterministic
ties between complete assignments, not deletion of the earlier definitions.
[Exact status transitions](../.codex-tmp/learner-release-v45/within-chain-status-downgrades.json).
Capture layouts change for 32, 44 and six previously seen contextual
inputs across the three extensions. The
[evolution ledger](../.codex-tmp/learner-release-v45/evolution.json) preserves these
transitions, old/new captures, promotions, retirements and complete-contract
extensions; per-checkpoint `template-evolution-*.json` files compare definitions
and native memberships with v43. Batch/order dependence remains a limitation:
this is one agreed sequence, not proof that every batch partition gives the same
model or that distribution among logs alone causes discovery.

## Immutable runtime delivery and reproduction

The [runtime manifest](../models/candidates/68f1ae5db205ab46afef9c4d/manifest.json)
pins the model, parser, shared matcher, validator, selector and rules. Its external
SHA-256 is `2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
The published model is derived from candidate `c4f174d947fbc531aba35fb7`;
publication compacts research evidence without changing native matching.
The [export validation](../models/candidates/68f1ae5db205ab46afef9c4d/native-validation.json)
covers 91,925 contextual inputs / 2,594,588 occurrences, with zero changed
matches, outcomes or capture assignments and 378,434 capture-byte checks.

The independent [whole-log replay](../.codex-tmp/learner-release-v45/delivery-replay.json)
then reparsed all 73 original files with the delivered package. All 91,925
distinct complete inputs reproduce the full build inspection results, including
alternatives and selected captures. Occurrence totals are exactly 2,439,711
template / 154,873 provisional / four no-match. It verifies 2,882,529 selected
regions and 10,285,082 present captures against native bytes, observes both
declared line-label alternatives, and imports no development modules.
The complete original Task 06 log gives 15,101 template / 9,011 provisional /
zero no-match over 24,112 occurrences. Every supplied original case ordinal
reconciles; see [public case results](../.codex-tmp/learner-release-v45/original-122-public.json)
and [native runtime examples](../.codex-tmp/learner-release-v45/delivery-examples.json).
These demonstrate package parity, not resolution of the semantic regressions above.

[Proposed selection](../models/candidates/selection.v45.proposed.json) is delivered
separately. Read-only application catalog loading resolves the new package as
API v2 and still resolves the active package as `44a0401b8adf0a2953d26705`.
[Catalog evidence](../.codex-tmp/learner-release-v45/catalog-load.json) also verifies
the learner identity and unchanged active-selection digest. This does not exercise
Task 06 storage integration. The [pipeline handoff](LEARNER_PARSER_PIPELINE_HANDOFF.md)
specifies literal-choice persistence, callable interfaces and integration work.

Same-version learning can continue from the retained full candidate and cumulative
native evidence. The compact immutable runtime package is an inference artifact,
not a replacement for that research state. A successor runtime package is a new
immutable revision; the already delivered package is never edited in place.

Reproduction runs from the checkout with `.\.venv\Scripts\python.exe`.
The retained [runner](../.codex-tmp/learner-release-v45/run_additive.py) calls the
owning learner with cumulative complete-native evidence and the preceding v45
model. Its build-command provenance is recorded in each candidate manifest.
For a new build, copy that runner and `inputs-all.json` to a **new** ignored
sibling directory: the runner deliberately refuses an existing `additive/`
destination. Use the frozen source on `PYTHONPATH`, preserving the verified
parser and recovery-snapshot paths:

```powershell
$env:PYTHONPATH = (Resolve-Path .codex-tmp/learner-release-v45/source).Path
.\.venv\Scripts\python.exe -B .codex-tmp/NEW-REPLAY/run_additive.py
```

`NEW-REPLAY` denotes that fresh directory, not an existing evidence destination.
The exact original input inventory, source identity and recovery-snapshot hash
are in `preflight.json`, `inputs-all.json` and `source/identity.json` under the
delivery evidence directory. The current source still has the frozen identity.
No historical model is imported to bootstrap learning. The native comparison
scripts `assess.py`, `evolution.py`, `trace_remaining.py` and
`trace_status_changes.py` preserve their joins, before-results and derivations
there; rerun them only in fresh output destinations because their SQLite and
report outputs are retained evidence.

The actual publication and independent replay commands were:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.publish_native_model --bundle .codex-tmp/learner-release-v45/additive/logs-73/c4f174d947fbc531aba35fb7 --output-dir models/candidates
.\.venv\Scripts\python.exe -I -S -B .codex-tmp/learner-release-v45/verify_delivery.py
```

The replay uses the package's authenticated bootstrap, parser, `iter_units` and
`match(..., inspect=True)` on complete original logs, with development imports
explicitly blocked. Repeated identical complete inputs share one matcher result;
every original occurrence still has its native region/capture bytes and frequency
checked. All original case emission ordinals are reconciled separately. This is
not inference on the deduplicated review extract or unseen-accuracy measurement.

## Performance and remaining work

Build plus bundle writing took 388.30, 495.21, 1,226.22 and 993.92 seconds
(about 51.7 minutes total). New inference took 260.53, 37.65, 130.62 and 82.67
seconds. Later source-processing totals include inference, settled matching and
wording checks; they must not be added to inference again. The final cumulative
evaluations took 87.79, 207.25, 502.51 and 340.87 seconds.
[Per-phase timings](../.codex-tmp/learner-release-v45/additive/timings.jsonl).
These runs do **not** demonstrate a speed improvement over the earlier v43 run.
They demonstrate reduced discovery scope and continuing cumulative matching cost;
cross-run timings were not controlled benchmarks.

| Proposed follow-up | Owner/component | Evidence needed and risk |
|---|---|---|
| Review proper-name/activity-value handling against generic word-run protection | Learner policy: `diagnostic_wording`, refinement | The four retained misses and additional genuine variations. Preserve effect/trigger and true diagnostic phrases; no spelling exceptions or automatic catalog seeding. |
| Review grouping sensitivity and capture regressions | Learner clustering/refinement | The travel-debug and rich-text old/new member sets, native field boundaries and counterexamples. Do not treat better coverage or fewer definitions as semantic correctness. |
| Decide whether representation-sensitive tie-breaking should change | Selector policy, separately approved | The 19-input/54-occurrence tie family and existing ambiguity behavior. Changing rank/tie semantics can change stored captures and must retain provisional uncertainty. |
| Profile cumulative matching and evidence handling | Shared matcher / learner orchestration | Exact assignment, ambiguity and capture parity on genuine inputs. Indexing existing applicability gates is a possible mechanical optimization; this delivery changes no scoring rule for speed. |
| Integrate schema 5 / API v2 with Task 06 storage and rendering | Pipeline Team | Immutable package replay, literal choices in persisted layouts/identity, both assignment statuses, original native review associations and existing-record compatibility. Selection/cutover is a separate action. |

The scoped applicability defect is fixed. The policy questions and capture
regressions above are explicitly not repaired by broadening inference to fit this
73-log run. Unknown outcomes remain legitimate, and no 100% classification target
was used.
