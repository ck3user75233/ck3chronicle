# Production-scope baseline candidate — Learner / TREK-2

2026-10-07. **Fresh 73-log model delivered for Pipeline receiving; no production switch.**
The Owner issued [this assignment](../task09-deliverables/RELEASE_BASELINE_LEARNER.md)
in the Learner chat. It supersedes the earlier two-input build limit for this work.
The existing logging-enabled, Observer-free Learner remains the correct closure:
all 48 payloads authenticate and equal current intended source bytes. No new
Learner release, algorithm change or v62 rename was needed.

This extends the [normal release handoff](HANDOFF.md). The earlier
[two-log acceptance](LOGGING_ACCEPTANCE.md), package `a6d9bfcde287f2f9f3961503`,
remains bounded evidence and is **not the production model**. This new package is
the **production-scope baseline candidate**, pending actual Pipeline receipt and
the Owner's separate adoption decision.

## Exact intake and retained locations

All relative artifact paths resolve under `C:/Users/nateb/Documents/ck3chronicle`.
**B** = `.codex-tmp/trek2-baseline-20261007`; **P** =
`.codex-tmp/combined-release-20261005`; **I** =
`.codex-tmp/trek6-removal-20261007/deployment`.

| Item | Exact identity / location |
|---|---|
| Learner release | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485` |
| External Learner manifest SHA-256 | `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e` |
| Learner fingerprint / algorithm | `67f881e22dfec7477ee2fe423a1c9789285acab6825c2b78fa3065996bcd52a9` / `outer-diagnostic-consensus-v61` |
| Retained executable | `I/share/ck3chronicle/learners/releases/2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485` |
| Existing installed host wheel SHA-256 | `1a325cd40eb29878e6c7c44a25615ea3eb3e47e4173eb6b72c3d6f8e596fb7ae` |
| Parser | `ck3-lossless-v1.8` / `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Candidate bundle | `B/registry/revisions/d729dea94d84323b8497e882` |
| Candidate manifest SHA-256 | `1b509590adfd56d1918d52dd94eaeab99e6f0d077dd83066a24a8499fd07a037` |
| **Model package** | **`2b12932103f3a3111a4e1880`** |
| **External package manifest SHA-256** | **`02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505`** |
| Immutable package directory | `B/packages/2b12932103f3a3111a4e1880` |
| Compact model revision | `3bc531d578074e6a430c161e` |
| Matcher / selector / schema | `ck3-native-matcher-v3` / `complete-assignment-v2` / 6 |
| Native matcher SHA-256 | `fe559adf9349d2fe83f50a0b000a14f00630a591684cdeeeead44d99efe52caa` |
| Package loader SHA-256 | `53168c6f84d17ca3a2d856e0b0248be3d78ab45e183937f5b2c9c50c441ce472` |
| Prior production package | `4ac4e8ee92346e6d14eacfbf` / manifest `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f` |

`B/intake.json`, `source-correspondence.json`, `package-authentication.json` and
`loaded-paths.json` retain full payload/module hashes. Normal `load_package`
authentication checks all 14 package payloads, its external pin, source-candidate
manifest link, parser/matcher/model identities and nine loaded package modules.
The application decoder is authenticated separately at
`19c4e46e5f4a6377f348901aecf5be87b69dabf2dc93e178168f864e70a2e227`. Runtime packages continue to use the
installed application decoder; no independent decoder distribution was invented.
`host-authentication.json` independently checks the existing wheel pin and all
49 installed retained members (manifest plus payloads) against that wheel. Actual
receipts record CPython 3.12.14 / Unicode 15.0.0. This scoped host check does not
replace Pipeline's final new-application resource/dependency receiving.

## Authenticated basis and exact commands

`P/build/build-basis.json` SHA-256
`fb1a3a35ebb8f26dd8a5fd6c36145b8b3aaac6e06308d498fed377e5a9864875` is the governing prior build basis.
Its retained delivery inventory also authenticates that file and comparison receipts.
`B/build-basis.json` carries the complete ordered inventory: **73 genuine inputs,
596,625,707 bytes**, original paths, retained snapshot paths, sizes and SHA-256s.
`B/intake.json` authenticates every snapshot and old staged copy, and records the
prior sync/build receipt arguments. No unavailable input was substituted.

The order is the original ascending input-hash order. Batches are exactly
**20 + 20 + 20 + 13**, cumulative **20/40/60/73**; strategy
`same-version-additive-v1`, threshold **0.72**, roles **training**. Fresh copies go
to `B/inputs/sessions/<input SHA-256>/error.log` at the corresponding batch boundary.
Fresh registry/cache/revisions live under `B/registry`. No prior candidate,
another-version registry or manual template seed enters this build.

`B/run_build.py` records the exact sequential command orchestration. Every retained
operation uses the supported launcher from `C:/Windows`:

```text
I/Scripts/python.exe -I -S -B <retained executable>/launcher.py run
  --root I/share/ck3chronicle/learners --release <Learner ID above>
  --receipt B/<operation>-execution.json --log-dir B/journals
  <operation> -- <arguments>
```

For each cumulative checkpoint N, the arguments are:

```text
registry -- --state-root B/registry sync --runtime-root B/inputs --default-role training
registry -- --state-root B/registry build --threshold .72
```

Then the final candidate is evaluated on genuine G2, hash
`05d71d156d3298e25568e4727d2fb15da111c2b74f8d18be29149e09e150ce95`, and exported:

```text
evaluate -- --bundle <final candidate> --log B/inputs/sessions/<G2 hash>/error.log --output B/evaluation.json
publish -- --bundle <final candidate> --output-dir B/packages
```

These are abbreviations, not literal runnable paths. `B/*-command.json` and
`commands.json` contain full argv/cwd; `*-execution.json` contains actual worker
arguments including the retained parser manifest. `*.stdout` / `*.stderr` preserve
ordinary output. All ten processes exit 0 with authenticated completed receipts.
The `publish` operation is the normal **local export**, not external publication
or production catalog registration.

The historical `mirror_incremental_build.py:execute` invokes private `_execute`,
which does not provide the required journal transport for this release. Learner
owns that legacy orchestration limitation. Bounded disposition: this build uses
the supported public `run` route for the identical schedule and operations.
The legacy helper was not run or modified; no unsupported worker call, source repair,
new release or inference implementation was needed. No other defect was found.

## Complete model and semantic comparison

| Cumulative inputs | New research revision | Templates (supported / provisional) | Full / provisional / unknown occurrences | Complete comparison with prior checkpoint |
|---|---|---|---|---|
| 20 | `456fb06bf05bb9ff669f983a` | 272 (198 / 74) | 545,862 / 126,036 / 0 | 36 provenance/path leaves; native bytes identical |
| 40 | `f12564571d808026d58fd3a9` | 318 (231 / 87) | 1,204,019 / 287,311 / 0 | 57 provenance/path leaves; native bytes identical |
| 60 | `12f73a8d2b60462fe1b3def3` | 391 (292 / 99) | 1,705,528 / 442,915 / 0 | 77 provenance/path leaves; native bytes identical |
| 73 | `d729dea94d84323b8497e882` | 394 (296 / 98) | 2,476,548 / 118,038 / 2 | 90 provenance/path leaves; native bytes identical |

Each checkpoint's **entire native evidence file is byte-identical** to its prior
counterpart. This includes every native message/piece, context, continuation,
capture presence/value/span, match alternative/ambiguity, complete selected assignment,
status, unmatched evidence and occurrence reference. This is not an aggregate-only
comparison. `comparison-{20,40,60,73}.json` enumerates every differing model leaf.

Differences are expected provenance only: five logging/invocation-related source
hashes in each of two identity maps; Learner fingerprint and added shared logging
hash map; three release-reference fields; candidate revision; staged input paths;
and the corresponding parent revision after the first checkpoint. No template,
policy, status, learning history content, source summary or assignment differs.
`semantic-review.json` validates those exact fields/values and records **zero
unexpected or behavioral differences**. Nothing was retuned.

The compact model differs only in the 16 executable/provenance leaves and its
source-candidate revision. All runtime executable, parser and rule payloads are
byte-identical to production. Only the compact model JSON and validation JSON
payload hashes change. `package-comparison.json` enumerates package, manifest,
model and validation differences; the validation differs only by source-candidate ID.

Normal authenticated export replays **91,925 contextual
messages / 2,594,588 occurrences**, checks **371,403
captures**, and finds **zero changed matches or outcomes**. Training remains
**2,476,548 full / 118,038 provisional /
2 unknown**, with zero unresolved training emissions.
The two unknown occurrences remain preserved; zero unresolved in this corpus is
not a claim about every possible CK3 log. Native evidence SHA-256:
`7442710719cbbd27b7aad3a9066dcb7f75699a37ff0026085f061a816164572f`.

`evaluation.json` is fresh genuine G2 evaluation using the final candidate and new
authenticated identity. Its complete records, captures, evidence and unresolved
array are retained: **4,141 full /
65 provisional /
0 unknown**, 4,206 recovered
messages and zero unresolved emissions. G2 is already training evidence, not a
holdout. The former two-input acceptance model has different breadth and is not
the production comparator.

`reused-evidence.json` authenticates the previous `comparison.json`, `messages.json`,
`stored-evidence.json`, parser correspondence and full-corpus comparison against
their original delivery hashes. Exact runtime payloads and behavior-bearing model
content still apply, so the genuine 20-Run comparison is reused, not re-executed or
relabelled: **7,287 recovered contextual messages**, **798,160 template / 7,699
provisional / 5,243 no-match / 1 unresolved-recovery occurrence** under what is now
production package `4ac4...`. The complete retained per-message statuses, bindings,
native renderings and review references remain evidence, including the original
unresolved route. Its former comparison with package `68f1...` is historical;
the reported gains from that earlier change are not gains in this build.
No new database read, ingestion or unresolved-path execution is claimed. Training
and stored scopes overlap; their totals must not be added or called unseen accuracy.

## Actual Canonical Logging v1 journals

`journal-review.json`, `journal-excerpts.txt`, `source-hooks.json` and
`loaded-paths.json` review actual files against the
[canonical design](../CANONICAL_LOGGING_SYSTEM_V1.md) and Owner O5.
All event invocation/release IDs agree with their receipts; each starts with the
exact release/manifest/Learner/parser identity. Loaded/compiled sources authenticate,
application config is absent, and export's derived executable hashes equal their
retained sources. Each stderr contains exactly one journal-path announcement.

| Operation | Observed wall seconds | Events / completed call pairs | Actual journal under B/journals | Receipt / outcome |
|---|---:|---:|---|---|
| sync-20 | 69.453 | 73 / 21 | `learner-05a94956c7964fe39bb5c2f362995bdb.jsonl` L1–73 | `sync-20-execution.json`; exit 0, completed, successful terminal and written receipt |
| build-20 | 136.797 | 11 / 2 | `learner-e990096cbc554c608e39637f83286dc1.jsonl` L1–11 | `build-20-execution.json`; exit 0, completed, successful terminal and written receipt |
| sync-40 | 95.516 | 76 / 21 | `learner-c54f10a7f7a743e5a74a9ac21e0c3bdd.jsonl` L1–76 | `sync-40-execution.json`; exit 0, completed, successful terminal and written receipt |
| build-40 | 175.078 | 11 / 2 | `learner-b2a0fd415789453fbb30491fade2db76.jsonl` L1–11 | `build-40-execution.json`; exit 0, completed, successful terminal and written receipt |
| sync-60 | 87.437 | 75 / 21 | `learner-c5a572b721eb4da2bb2d8ce2c0a97015.jsonl` L1–75 | `sync-60-execution.json`; exit 0, completed, successful terminal and written receipt |
| build-60 | 293.468 | 13 / 2 | `learner-12e8bc0b3a1944628e34965e42433c56.jsonl` L1–13 | `build-60-execution.json`; exit 0, completed, successful terminal and written receipt |
| sync-73 | 75.453 | 53 / 14 | `learner-8948ef93902a4390b42bbfd4f771883a.jsonl` L1–53 | `sync-73-execution.json`; exit 0, completed, successful terminal and written receipt |
| build-73 | 263.343 | 13 / 2 | `learner-4489a1ff917b4f4ab0693c26feb0329d.jsonl` L1–13 | `build-73-execution.json`; exit 0, completed, successful terminal and written receipt |
| evaluate | 4.516 | 5 / 1 | `learner-d83614e7d36a4cda9a5a724727e85c61.jsonl` L1–5 | `evaluate-execution.json`; exit 0, completed, successful terminal and written receipt |
| publish | 119.718 | 2 / 0 | `learner-d6e909307798477e8ae51e4922ce5c95.jsonl` L1–2 | `publish-execution.json`; exit 0, completed, successful terminal and written receipt |

Total: **332 events,
86 completed call pairs,
229,450 journal bytes**. Wall times describe
one execution including launch/authentication/I/O, not a performance guarantee.

Selected fields copied from actual `learner-05a94956c7964fe39bb5c2f362995bdb.jsonl` (full original lines in
`journal-excerpts.txt`; omitted fields are not changed):

```text
L1 {"event":"invocation_started","invocation_id":"05a94956c7964fe39bb5c2f362995bdb","release_id":"2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485","manifest_sha256":"9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e"}
L3 {"event":"call_started","invocation_id":"05a94956c7964fe39bb5c2f362995bdb","release_id":"2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485","module":"template_learning.records","function":"collect_records","function_line":77,"source_line":78}
L4 {"event":"checkpoint","invocation_id":"05a94956c7964fe39bb5c2f362995bdb","release_id":"2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485","module":"template_learning.records","function":"collect_records","function_line":77,"source_line":132,"completed":1,"total":1}
L5 {"event":"call_finished","invocation_id":"05a94956c7964fe39bb5c2f362995bdb","release_id":"2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485","module":"template_learning.records","function":"collect_records","function_line":77,"source_line":78,"elapsed_seconds":0.14099999994505197}
L73 {"event":"invocation_finished","invocation_id":"05a94956c7964fe39bb5c2f362995bdb","release_id":"2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485","outcome":"success","dispatch_outcome":"success","receipt_requested":true,"receipt_written":true,"receipt_error":null}
```

| Representative actual call | Journal lines (entry / normal finish) | Source and observed progress |
|---|---|---|
| sync-20: `collect_records` | `learner-05a94956c7964fe39bb5c2f362995bdb.jsonl` L3 / L5 | `records.py:77`; entry hook 78; elapsed 0.141s. L4 `1/1` |
| sync-40: `sync_registry` | `learner-c54f10a7f7a743e5a74a9ac21e0c3bdd.jsonl` L2 / L75 | `incremental_template_registry.py:209`; entry hook 217; elapsed 94.985s. L3 `1/40`, L4 `19/40`, L74 `40/40` |
| build-73: `build_model` | `learner-4489a1ff917b4f4ab0693c26feb0329d.jsonl` L2 / L10 | `artifacts.py:119`; entry hook 121; elapsed 204.671s. L3 `1/133`, L4 `35/133`, L9 `133/133` |
| build-73: `write_bundle` | `learner-4489a1ff917b4f4ab0693c26feb0329d.jsonl` L11 / L12 | `artifacts.py:232`; entry hook 233; elapsed 24.516s. No routine checkpoint; entry and normal completion only. |

`collect_records` is entered at retained `records.py:77`, scope at 78; line 80
enumerates supplied inputs starting at one. All recovery/record processing and
the evidence-stat assignment at 131 precede `journal.checkpoint(completed,
len(logs))` at **132**. The actual build observes 73 singleton collection calls
during sync plus the one G2 evaluation call, each **1/1**, followed by normal
completion. It does not count distinct accumulated hashes. This build does not
exercise duplicate hashes within one multi-input call; the exact-release earlier
two-log acceptance separately observed 1/2 and 2/2.

Outer sync progress at `incremental_template_registry.py:307` counts processed
paths after cache/entry work; later cumulative syncs include the existing cached
paths. Build progress at `artifacts.py:159` follows assignment of completed source
summaries. Nested collection does not consume the outer call's count state.
Real periodic observations occur in this full build; first/final observations
and naturally suppressed intermediate counts are visible without artificial delays.
Call finish identifies the original entry hook and normal return, not a guessed
return-statement location. Export has the approved invocation boundary only.

Every journal has exactly one actual successful terminal, with dispatch success,
`receipt_requested=true`, `receipt_written=true`, `receipt_error=null`, matching
its on-disk receipt and process exit 0. No terminal is inferred from output existence.
Rotation defaults remain 10 MiB/five backups; no rotation occurs. Bare/count-only,
empty/recursive/repeated-hash input and exceptional/setup/receipt/flush/crash cases
remain unobserved. No synthetic or fault-injection test was used.

## Preservation, delivery and next actor

One task-owned verification helper initially assumed the prior delivery inventory
listed every intermediate candidate manifest; it raised `KeyError` before completing
verification. `verify-delivery-attempt-1.py` and `verification-correction.json`
preserve that error and disposition. The corrected check authenticates the actual
inventoried result/execution receipts and recomputes each historical model revision
against its inventoried revision. The pinned production package additionally binds
its final source-candidate manifest. The corrected helper passes. No product check
failed, no input/output was retuned and no build/evaluation/export was rerun.

`before.json` and `before/HANDOFF.md` preserve the exact prior bytes of the only
existing document edited; this document's prior absence is recorded. Authentication
guards are separate from that rollback baseline. Inputs, prior production model,
selected Learner distribution, source closure, catalogs and selection files remain
unchanged. New state, model, journal and evaluation material remain ignored by Git.
No product-source, shared catalog/resource, live default, database, configuration,
service, commit, tag, push or external publication change occurred.

Pipeline receives this exact production-scope package on **TREK-2**, under
[baseline receiving](../task09-deliverables/RELEASE_BASELINE_PIPELINE.md), and owns
application packaging/resources/default preparation and integrated installed
classification. Its new wheel must use this package/pin, not the two-log acceptance
package. The normal proposed selection is in `B/completion.json` / `publish.stdout`.
Its `candidates/<package_id>` path is the exporter's conventional suggestion, not
the actual package location above or an installed default. Pipeline should obtain
the selection for its isolated registered package through the normal catalog API.
No Learner-side model registration was needed; any receiving registration belongs
in isolated roots. Existing installed evidence here is not final new-application
receiving, physical external placement or production activation.

Record actual receipt separately from delivery on TREK-2, then close the received
Learner component. Pipeline's external-placement obligation belongs on **TREK-6**;
it does not create further Learner work after receipt. Rollback of this documentation
must preserve intervening edits; retain all immutable build artifacts and pins.
