# Learner canonical logging integration — TREK-2

2026-10-06. **Implemented and bounded genuine verification delivered; Pipeline
receipt and packaging pending.** Owner issuance is the attached assignment in
the Learner chat on this date. [Assignment](../task09-deliverables/LEARNER_INTEGRATION.md),
[owner disposition](../TASK09_OWNER_DECISIONS.md) and corrected plan D/E-L/G/H
govern. Production remains on the prior combined release; this candidate is not
registered or selected there. TREK-2 stays `in_progress` pending actual receipt
and the receiving follow-ups below. This is not project-wide logging completion.

## Authenticated intake

Evidence root **OUT**: `.codex-tmp/trek2-learner-20261006`; final verification is
**F = OUT/final**. All generated evidence stays ignored. Normal source remains
under `tools/template_learning/`; the shared backend/adapter were not edited.

| Item | Immutable identity / external pin |
|---|---|
| Fresh pre-logging release | `98cf3cb7cfdb1c0e6187a8e50887bde32b4c462c398f3eabde8b63a3ceae6657` |
| Pre-logging manifest SHA-256 | `377cd2499db03df4414a9f85c1c475742e9991201543706b3700a34d3ca1ea1d` |
| Pre-logging fingerprint | `77a3935070c561c2de830f6577f31c189991dd93d0bce7bf0106c626a083ced7` |
| Final logging release | `9c02a343c389aed3d6a4b679b10ac5df01d7dca76e8b1eb991f5138b09c1af12` |
| Final manifest SHA-256 | `0edc5b9e2149e0a64cd360502bbdfe74f3b9ff6753c76230e73dd93794cadfd3` |
| Final learner fingerprint | `20ee0661d0c1d758a2b649a7b6c7473ac1982ca5c2e520825f2f9b9e47b42e0d` |
| Algorithm / parser | `outer-diagnostic-consensus-v61` / `ck3-lossless-v1.8` |
| Parser SHA-256 | `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |

Final retained source: `F/post/releases/9c02a343c389aed3d6a4b679b10ac5df01d7dca76e8b1eb991f5138b09c1af12`.
The authenticated relocation is `F/post/catalog/releases/9c02a343c389aed3d6a4b679b10ac5df01d7dca76e8b1eb991f5138b09c1af12`.
The catalog contains a disposable **research** registration only. The original
pre-logging closure is `OUT/pre/releases/98cf3cb7cfdb1c0e6187a8e50887bde32b4c462c398f3eabde8b63a3ceae6657` and has its own
research registration in `F/pre/catalog`. `F/post-release.json`, `F/pre-release.json`
and `F/artifact-pins.json` contain absolute paths and full pins.

| Bounded artifact | ID | Manifest SHA-256 |
|---|---|---|
| pre learn_bundle | `4ce244d8d867258747bb5736` | `d940f317a3bb8e65e4fc0c262fbf0990253db122106d99998637ba662896c2b0` |
| pre registry_bundle | `cff722bc4723498282d554c6` | `0d7ba85685d02beb3710d821e1404cdd0a53427ef5f3f8882cd55c7b7125c344` |
| pre package | `160f46d2093b4e3c332d31cb` | `c0600ee9c4fe9d41a5d1475e091d6f303ca4a66c297c53ea53290e9a8b4062d5` |
| post learn_bundle | `698150a4220907b648aa47cf` | `c1ec04d4289a44d4eab21f531fd2b50aba8ab7fb06ea11be09bb5c2cb5feb1cd` |
| post registry_bundle | `26d739dca32b7f666f34cfab` | `e7b2713f92b1d8e3b5741043cbc40fd3ca98b547d7be7e3b2c630afcba619dc3` |
| post package | `aa741973c67542b55b9b6350` | `5cecc96693b23981a9a7b643f1442c3175ae2a036921b9c36fd74fd904de3d58` |

These exported packages are disposable reference-verification artifacts, not a
production model delivery. The two-log model cannot replace the 73-log production
model. No production publication, registration, selection, commit, push, activation,
service restart or historical ingestion occurred.

## Implementation and interface

Seven bounded source edits: `learner_loader.py`, `artifacts.py`,
`publish_native_model.py`, `records.py`, `incremental_template_registry.py`,
`recover_large_candidate_export.py`, and `review_short_thresholds.py`.
The latter two are interface repairs only; neither research/recovery operation ran.

`source_payloads(source, application_source=...)` owns the authoring map. `FILES`
and learner-local hash keys remain local. New identities add
`shared_implementation_hashes` for the exact two logging payloads and use the
three-element version/local/shared fingerprint; absent shared hashes retain the
old two-element formula. Decoder distribution treatment is unchanged. The final
48-payload closure adds only two shared files to the baseline's 46 payloads.
Authenticated capability `journal_api: 1` is required for the new private worker
transport; unknown versions, absent shared payload/identity, and launcher/local
loader disagreement are rejected. The final launcher and learner-loader bytes
are identical and authenticated together. Later edits require a fresh identity.

Shared hashes are unchanged from Pipeline's TREK-1 delivery:

- `ck3chronicle/runtime_logging.py`: `d18a6888713d374b0b7266b733d3fd11302372dd8ea94fa06538017a73a1d2b5`
- `ck3chronicle/journal.py`: `b48a1fde03f31e7e8d42e91a0f114fc15ed239afecbd265cabbd0412ecc2e8cc`

Retained `implementation_identity` returns a deep copy of authenticated manifest
identity. Registry/candidate equality stays strict. Publication checks that identity
and the mapped retained disk bytes; recovery's explicit context accompanies its
full source-map comparison. The parser pins, decoder bytes, compile/import audit,
publish-only identical-derived-code exception and matcher runtime closure remain
unchanged. No config payload, application initializer or ambient fallback is added.

Outer `run --log-dir` belongs before the operation; REMAINDER and optional separator
handling are preserved. The capable route resolves explicit destination, then
receipt-parent `learner-logs`, then `<cwd>/.ck3chronicle/wip/learner-logs`; it sends
an API-1 absolute destination and invocation ID through positional JSON. The child
imports/configures shared logging under its installed audit hook, announces the
opened file once on stderr and owns one terminal. Every retained event carries
invocation/release identity; full provenance appears once at start. Receipt fields
add the journal path, rotation and observed outcome without replacing existing
argv, parser, modules, compiled sources and derived executable evidence.

The bounded worker boundary preserves normal return, zero/string/nonzero SystemExit,
KeyboardInterrupt and other exceptions. An unwound call gets no normal finish or
traceback; the invocation boundary records an unexpected exception once. A receipt
failure propagates after success but cannot mask a pending execution exception.
Cleanup is best effort even with a pending boundary exception. A receipt's
`terminal_observation` describes the observed dispatch outcome, not proof that a
later best-effort terminal event reached disk. Missing terminals remain unavailable.
These exceptional paths were source-reviewed, not injected.

Administrative `create/list/register` use the same shared backend directly in the
loader's foreground dispatch. Explicit `--log-dir` wins; default is the CK3Chronicle
workspace location with `learner-admin-<id>.jsonl`. There is no alternate wrapper,
config discovery, fallback on open failure, metadata hash scan or change to catalog
authentication/publication semantics. Help parses before logging setup.

Exactly four call scopes were added. Real observed final counts/source hooks:

| Function | Source definition / hook line | Final genuine observation |
|---|---|---|
| `collect_records` | `records.py:77` / `132` | learn `2/2`; each sync subcall and evaluation `1/1` |
| `sync_registry` | `incremental_template_registry.py:209` / `307` | `2/2` paths after cache/entry work |
| `build_model` | `artifacts.py:119` / `159` | `51/51` completed source summaries |
| `write_bundle` | `artifacts.py:232` | normal call scope only |

Collection counts `enumerate(logs, 1)` after full input and stats assignment, not
distinct hashes. Sync binds its single existing path list and emits after completed
work. No rescan, field-only algorithm work, bare/end checkpoint or clustering,
parser, matcher, decoder or rules edit was introduced.

## Genuine execution and comparison

`F/inputs.json` references the first two existing entries from the combined release's
73-log inventory, with original paths, existing snapshots and SHA-256. Selected
hashes are `01aeb0f116da6fc3f20423ef0f75a0daa465c4242db304c6bf2fb00e33775c10`
and `05d71d156d3298e25568e4727d2fb15da111c2b74f8d18be29149e09e150ce95`
(303,696 and 633,966 bytes). Copies preserve exact bytes/timestamps; no LOCATOR,
emission, clock or input content was changed. Same ordering and schedule for both:
learn both; one sync of both as training; one fresh build; evaluate the second;
export/reference-verify the registry candidate. Registries/caches/outputs are separate
fresh state. The earlier same-task pass remains under OUT/pre and OUT/post; its
logging candidate `193389ef…b9ff5` is superseded, unmodified. Final verification was
repeated after the final loader cleanup/map correction; no check failed.

Both final candidates produce **5,137 emissions, 6,357 messages, 1,345 unique
messages, 51 source families and 97 templates: 66 supported, 31 provisional**.
Training: **5,268 full, 1,089 provisional, 0 unknown**, no unresolved emission or
candidate in these inputs. Evaluation: **3,197 full, 1,009 provisional, 0 unknown**
over 4,206 messages. Genuine absence of unknowns is not evidence of general coverage.

`F/review.json` records complete recursive semantic comparison: learn candidates,
registry candidates and exported compact models match after removing only the
explicit learner identity/release/revision metadata. Both corresponding native
evidence files match byte-for-byte. Evaluation's complete records, captures,
assignments, evidence and unresolved arrays match after only release/revision
removal. Export parity independently passes on both candidates; all nine derived
matcher executables match authenticated retained hashes. Matcher closure is unchanged.
Contract conversion, database persistence and review routing were not rerun; those
unchanged Pipeline boundaries retain their independent packaging/receiving obligation.

Sync/evaluate stdout is byte-identical. Learn/build progress text is identical;
result JSON differs only in bundle/model paths, revision and model hash. Export
results necessarily differ in package/path and authenticated source identity.
Full differing JSON paths, exact argv/stdout/stderr, receipts and return codes are
retained. Operation argv differs only in separate state paths and authenticated
parser/revision locations; private transport never enters operation argv.

All ten worker operations exit zero. Final admin checks include genuine production
catalog listing, candidate creation, research registration into two disposable
catalogs and listing the post catalog; all five exit zero with separate start/finish
journals and unchanged JSON stdout. No production catalog was written.

All launches run from **`C:/Windows`**, using isolated `-I -S -B` and the relocated
catalog's authenticated launcher. Receipts verify both shared module hashes, retained
paths, compiled bytes and absence of config imports. Parser/decoder identity and
all mapped source bytes authenticate. Payload placement itself is still inside the
writable checkout: **copying the new payload outside that filesystem boundary remains
unverified**. This session cannot write outside its permitted root; the result does
not claim that additional placement check. Pipeline should complete it in its
authorized packaging/staging environment.

Five event kinds occur naturally. Journals prove final counted observations,
normal completion, one terminal per worker, one stderr announcement and no canonical
traceback on success. Sync naturally nests collection calls; scope restoration and
separate invocation files pass. Build's 51-source loop emits first and final counts,
so suppression and final bypass are observed without invented workload. No >5-second
periodic interval or rotation was reached. Older protocol compatibility is genuine:
the fresh pre-logging candidate executes all five operations through the final outer
loader with its unmodified retained launcher and no journal capability.

## Measured cost and limits

Final pass, seconds; journal columns are post events / bytes (pre emits zero):

| Operation | Pre wall / CPU | Post wall / CPU | Post events / bytes |
|---|---:|---:|---:|
| learn | 4.166 / 3.328 | 4.364 / 3.609 | 12 / 7,959 |
| sync | 1.517 / 1.297 | 1.682 / 1.391 | 12 / 8,109 |
| build | 3.399 / 3.172 | 3.650 / 3.359 | 8 / 5,290 |
| evaluate | 1.889 / 1.719 | 2.236 / 2.156 | 5 / 3,278 |
| export | 1.686 / 1.469 | 1.839 / 1.562 | 2 / 1,277 |

`F/measurements.json` records exact commands, return codes and per-process final
Windows kernel/user CPU counters. Child handles were discovered every 50 ms and
retained until exit; extremely short unobserved descendants remain a measurement
limit. Each real worker was observed. Wall time includes launch/authentication/I/O
and polling. This is one sequential pre/post pass on a shared machine with warm
caches, not a statistical benchmark or an invented performance threshold. Journal
volume totals 39 worker events /
25,913 bytes plus the five administrative journals.

Unexercised: bare/count-only, empty/recursive inputs, repeated-hash input counting,
periodic >5s suppression, rotation and exceptional/receipt/open/flush/crash paths;
cwd default destinations without receipts/admin explicit path and negative capability
validation are source-reviewed. No synthetic or fault-injection tests, altered clock,
forced exit, fabricated event or full-corpus campaign was created or run. New
requirements were not introduced to fill unavailable evidence.

## Preservation, source checks and receiving

`OUT/before.json` and `OUT/before/` preserve exact edited working bytes and prior
absence of this handoff; `OUT/after.json` and `OUT/after/` preserve final bytes.
`OUT/source.patch` is the exact source delta; `OUT/delivery.patch` includes Learner
documentation. `OUT/delivery-receipt.json` hashes final source, launcher, manifests,
evidence and patches. Reproduction inputs are referenced separately in immutable
candidate manifests and `F/inputs.json`. Rollback must compare current hashes and
resolve intervening work, never overwrite it. No retained distribution was patched.

All seven sources parse; runtime ownership check passes. `OUT/source-review.json`
also runs the existing checker's AST ownership rule directly over the seven Learner
sources without editing the checker. ASTs of the four substantive functions match
their preserved baselines after removal of precisely the approved scope/checkpoint,
loop-counter and one-list binding edits. `git diff --check` passes for this delivery.

Shared coordination was recorded in TREK-1 comment CMT-9 before shared edits; no
Pipeline file was edited. Learner receives the unchanged backend/adapter's config-free
retained suitability with the above genuine evidence, while Watcher compatibility
and Pipeline-owned backend repairs remain on TREK-1. Do not close the producer solely
for Learner receipt.

Pipeline's TREK-2 receipt must authenticate the final distribution/package interface.
Pipeline Integration also receives two explicit coordination items: extend the owning
checker to cover the new Learner entry/hooks, and apply/reconcile
`OUT/RELEASES-proposed.patch` (source hash in `OUT/RELEASES-coordination.json`). This
is the prepared Learner section for `docs/RELEASES.md`; that shared file was not
edited without owner coordination. The proposal corrects its now-stale decoder-only
description and documents capability/destination/admin behavior. No requirement for
a new component or separate administrative wrapper is proposed.

Final Packaging independently verifies wheel/source/installed correspondence,
including retained `ck3chronicle/` resources and external payload placement. These
consumer obligations are not closed by Learner verification. Keep TREK-2 open until
actual receipt/follow-up disposition; owner acceptance and production activation
remain separate.
