# Genuine build and Canonical Logging v1 acceptance — Learner / TREK-2

2026-10-07. **All five authorized installed operations and their complete result /
journal comparisons pass. Model package delivered for Pipeline receiving.**
Owner issuance of [the bounded acceptance assignment](../task09-deliverables/LOGGING_ACCEPTANCE_LEARNER.md)
explicitly resolves CMT-44 and authorizes this fresh learn, sync, build, evaluation
and local export. No candidate was relabelled and no identity check was weakened.
This completes Learner's bounded demonstration; Pipeline's pinned classification,
actual TREK-2 receipt, physical external placement and consolidated TREK-6 conclusion
remain separate under [its acceptance assignment](../task09-deliverables/LOGGING_ACCEPTANCE_PIPELINE.md).

## Exact executable, inputs and outputs

All paths below resolve beneath `C:/Users/nateb/Documents/ck3chronicle`:

- **A** = `.codex-tmp/trek2-acceptance-20261007` — fresh ignored output/state/evidence.
- **I** = `.codex-tmp/trek6-removal-20261007/deployment` — existing installed replacement.
- **B** = `.codex-tmp/trek2-learner-20261006/final` — unchanged genuine baseline.
- **L** = `I/share/ck3chronicle/learners/releases/2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`.

| Executable / artifact | Identity / external pin |
|---|---|
| Installed application wheel | `.codex-tmp/trek6-removal-20261007/application/ck3chronicle-0.0.1-py3-none-any.whl`; SHA-256 `1a325cd40eb29878e6c7c44a25615ea3eb3e47e4173eb6b72c3d6f8e596fb7ae` |
| Learner release | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`; manifest `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e` |
| Learner fingerprint / algorithm | `67f881e22dfec7477ee2fe423a1c9789285acab6825c2b78fa3065996bcd52a9`; `outer-diagnostic-consensus-v61` |
| Parser | `ck3-lossless-v1.8`; SHA-256 `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Learn candidate | `A/learn/f4c0448365c7fadff89f860b`; manifest `72d0056b742e53900483bca3022e87de1729fbce5e0b927c26cbc1d601953c89` |
| Registry candidate | `A/state/revisions/e838a9378056194e918d875d`; manifest `2bb73bda63363d86016b8985225f68d77fe6f470ecb581dd29127bc860b05cae` |
| Registry state | `A/state/registry.json`; final SHA-256 `c14157ca9484f8067b4b76ccbc0e189e0b7ec9edd483ab9563549934cf0d9f11`; exactly two training entries and one revision |
| **Delivered model package** | **`A/packages/a6d9bfcde287f2f9f3961503`** |
| **Package manifest pin** | **`bab7f890c55ca230e661b28ee3fde0526913461a67238b20cd8cfeba7b075720`** |
| Compact model revision / matcher | `6a26cfcda30616297fda9f6f`; model schema 6 / `ck3-native-matcher-v3` / `complete-assignment-v2` |

`A/intake.json` verifies the wheel pin, installed catalog selection, all 48 retained
payloads and manifest against wheel members, and exact administrative/retained
launcher correspondence. The cleaned backend remains
`aa22fb1b13b03c3661d6872298ef875fc9f6f08e21bf2c0fb5caadd81d49bf65`; journal adapter
remains `b48a1fde03f31e7e8d42e91a0f114fc15ed239afecbd265cabbd0412ecc2e8cc`.
No new Learner release or application rebuild was made. Pipeline's later CMT-47/50
and [replacement receiving](OBSERVER_FREE_PIPELINE_RECEIVING.md) identify this same
installed artifact; no superseding executable was found at intake.

Inputs are the existing `verification_copy` paths in `B/inputs.json`, authenticated
again without edits or recopying. **G1**, then **G2**:

| Input | Actual path | Bytes / SHA-256 |
|---|---|---|
| G1 | `B/inputs/sessions/01aeb0f116da6fc3f20423ef0f75a0daa465c4242db304c6bf2fb00e33775c10/error.log` | 303,696 / `01aeb0f116da6fc3f20423ef0f75a0daa465c4242db304c6bf2fb00e33775c10` |
| G2 | `B/inputs/sessions/05d71d156d3298e25568e4727d2fb15da111c2b74f8d18be29149e09e150ce95/error.log` | 633,966 / `05d71d156d3298e25568e4727d2fb15da111c2b74f8d18be29149e09e150ce95` |

`B/inputs` contains exactly these two logs. Both are training inputs. This is
functional/regression evidence, **not holdout quality or production-model selection**.

## Execution and complete comparisons

Every command used this supported outer launcher from `C:/Windows`:

```text
I/Scripts/python.exe -I -S -B L/launcher.py run
  --root I/share/ck3chronicle/learners --release <Learner ID above>
  --receipt A/<operation>-receipt.json --log-dir A/journals
  <release operation> -- <arguments below>
```

Symbols above are path abbreviations, not literal shell commands. Exact expanded
argv/cwd are in `A/<operation>-command.json` and `A/commands.json`; each operation
also has `<operation>.stdout`, `.stderr` and `-receipt.json`. Parser arguments for
learn/sync/build are inserted by the supported worker from **L**, recorded in receipts.
All outputs are outside installation/release directories.

| Operation / command arguments | Inputs → outputs | Result comparison | Receipt / journal under A |
|---|---|---|---|
| `learn --log G1 --log G2 --output-dir A/learn` | G1+G2 → learn candidate above | Complete model differs only in six enumerated identity fields; native evidence byte-identical. Progress stdout identical; final `bundle` path changes. Exit 0. | `learn-receipt.json`; `journals/learner-43ab1772d6b74090a148a372c4e1fe12.jsonl` |
| `registry --state-root A/state sync --runtime-root B/inputs --default-role training` | G1+G2 → fresh registry and two caches | Two paths seen/hashed, two new training entries/caches, no duplicates. Complete stdout byte-identical. Exit 0. | `sync-receipt.json`; `journals/learner-9539f44b270b4c20bb388ac3e91a8448.jsonl` |
| `registry --state-root A/state build` | Fresh training registry → registry candidate above | Complete model differs only in six identity fields; native evidence byte-identical. Progress stdout identical; final bundle/model paths, revision and model hash change. Exit 0. | `build-receipt.json`; `journals/learner-5a298eeb036d4ea590eca1c26b4c44f9.jsonl` |
| `evaluate --bundle A/state/revisions/e838a9378056194e918d875d --log G2 --output A/evaluation.json` | Registry candidate + G2 → evaluation | Complete records, captures, assignments, evidence and unresolved arrays equal. Only release provenance/model revision differ; stdout byte-identical. Exit 0. | `evaluate-receipt.json`; `journals/learner-f020f78b5bc5417a848624b220729b7c.jsonl` |
| `publish --bundle A/state/revisions/e838a9378056194e918d875d --output-dir A/packages` | Registry candidate → pinned package above | Complete compact model/parity match except identities. Reference verification and normal package load pass. Local export only. Exit 0. | `export-receipt.json`; `journals/learner-5086eca75564415db4576a6d6e038bc0.jsonl` |

The baseline is `B/post`: learn `698150a4220907b648aa47cf`, registry candidate
`26d739dca32b7f666f34cfab`, package `aa741973c67542b55b9b6350`, and `evaluation.json`.
`A/comparisons.json` recursively compares the complete corresponding objects and
records every differing leaf with old/new values, not just counts or broad field
removal. The six candidate differences are exactly:

- `algorithm.learner_identity.sha256` and
  `algorithm.learner_identity.shared_implementation_hashes.ck3chronicle/runtime_logging.py`;
- `learner_release.learner_identity`, `learner_release.manifest_sha256`,
  `learner_release.release_id`, and `revision_id`.

The compact model additionally changes `source_candidate_revision`. Evaluation
changes only the three `learner_release` leaves and `model_revision`.
`native-validation.json` changes only `source_candidate_revision`. Export stdout
changes only folder/package/model/pin and their proposed-selection counterparts.
Manifest hashes and build-command paths consequently change as recorded in
`artifacts.json`; input paths/content, algorithm implementation hashes, parser,
matcher, rules, model templates and all native results remain identical.

Both new candidates contain **97 templates (66 supported, 31 provisional), 51
source families, 1,345 unique messages, 5,137 emissions and 6,357 messages**.
Training outcomes remain **5,268 full / 1,089 provisional / 0 unknown**.
Evaluation on G2 remains **3,197 full / 1,009 provisional / 0 unknown**, 4,206
recovered messages, no unresolved emissions. Zero unknowns here imply no general
coverage claim. Both complete native evidence files are byte-identical to baseline.

Export's existing reference verification replays all 1,345 contextual messages /
6,357 occurrences, checks **3,220 captures**, and reports **zero changed matches
or outcomes**. Native evidence pin is
`ef3328622d4fd06836b1c1e97bcaf2ac2349c8125a74e1d4a46481ed7f1735c1`.
`package-authentication.json` records normal `load_package` authentication at the
external pin, all 14 payloads, parser/matcher/selector/model identities and nine
actually loaded package module paths. The export receipt independently authenticates
the same nine derived executables against retained source. The package requires
the exact installed application decoder; it is not a standalone decoder distribution.

## What the actual journals demonstrate

`A/journal-review.json`, `loaded-paths.json` and `source-hooks.json` inspect every
event and actual retained source. `journal-excerpts.txt` preserves all **39 original
JSONL lines**, labelled with their per-journal line numbers. There are **nine normal
call pairs** across the five invocations. All event invocation/release IDs match
their receipt; all loaded/compiled hashes authenticate; no config module was loaded.
Each stderr consists of one journal-path announcement. Each receipt says completed /
success / written, agrees with process exit 0, and has one observed successful
terminal on disk. Export has the intended invocation boundary only, no invented
function hooks.

These short excerpts select actual fields from the linked journal lines; repeated
invocation/release/source fields are omitted here only for readability:

| Journal lines | Actual excerpt | What it establishes |
|---|---|---|
| Learn L1 | `"operation": "learn", "invocation_id": "43ab1772d6b74090a148a372c4e1fe12", "manifest_sha256": "9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e"` | Start provenance also includes Learner fingerprint, parser pin, journal path, PID and timestamp; later lines carry the same invocation/release. |
| Learn L2 | `"event": "call_started", "module": "template_learning.records", "function": "collect_records", "function_line": 77, "source_line": 78` | Actual source is `L/template_learning/records.py`; the entry hook identifies the defining function, not a logging helper or phase. |
| Learn L3–4 | `"source_line": 132, "completed": 1, "total": 2` then `"source_line": 132, "completed": 2, "total": 2` | One then two completed inputs. Source line 131 assigns the completed input's stats after full recovery/record processing; line 132 emits. It does not count distinct evidence hashes or work about to begin. |
| Learn L5 | `"event": "call_finished", "function": "collect_records", "elapsed_seconds": 0.5` | Normal function return was observed, with monotonic elapsed time. |
| Sync L2–11 | `sync_registry` starts at `incremental_template_registry.py:210`; collection completes at L5/L9; outer checkpoints at L6/L10 are `1/2`, `2/2` from source line 307 | Two real nested collection calls each independently emit `1/1`; the outer scope is restored. Sync counts processed paths after cache/entry work, not a database commit. |
| Build L2–5 | `"function": "build_model"`; L3 `"source_line": 159, "completed": 1, "total": 51`; L4 `51/51`; L5 `"elapsed_seconds": 1.952999999979511` | First/final source summaries; source lines 157–158 assign the completed summary before the hook. Intermediate 2–50 observations are naturally suppressed during this sub-five-second loop; final equality bypasses suppression. |
| Build L6–7 | `"function": "write_bundle", "function_line": 232, "source_line": 233`; finish `"elapsed_seconds": 0.39099999994505197` | Actual bundle writer entry and normal completion. No redundant bare checkpoint. Learn L10–11 observes the same function separately. |
| Evaluate L2–4 | `collect_records`; L3 `"completed": 1, "total": 1`; L4 `"elapsed_seconds": 0.29599999997299165` | The one supplied complete evaluation input has finished collection. Full evaluation success is separately recorded at L5. |
| Export L2 | `"event": "invocation_finished", "outcome": "success", "dispatch_outcome": "success", "receipt_requested": true, "receipt_written": true, "receipt_error": null` | Observed invocation outcome agrees with the actual receipt and exit result. This is not inferred from silence or the existence of an output file. |

The earlier log table gives exact filenames; e.g. Learn L3 refers to line 3 of
`A/journals/learner-43ab1772d6b74090a148a372c4e1fe12.jsonl`. Source identity was
checked against each retained file hash and actual function/hook line. Call finish
reuses its entry-hook location; it does not claim to identify a return statement.
Learn also observes `build_model` first/final `1/51`, `51/51`, elapsed
`2.14000000001397` seconds. All scopes complete naturally; no timing was altered.

| Operation | Observed wall seconds | Events / bytes |
|---|---:|---:|
| Learn | 4.016 | 12 / 8,137 |
| Sync | 1.140 | 12 / 8,317 |
| Build | 3.219 | 8 / 5,403 |
| Evaluate | 1.781 | 5 / 3,327 |
| Export | 1.703 | 2 / 1,263 |

Total journal volume is **26,447 bytes**. Wall values are one sequential observed
pass, rounded here; full values are in `commands.json`. They include launch,
authentication and I/O. Timestamps, invocation/PID IDs, source paths, elapsed times
and journal bytes differ naturally from the earlier run; no controlled overhead or
performance threshold claim is made. Defaults remain 10 MiB / five backups.

No counted loop reached a periodic five-second emission. Rotation, bare/count-only
checkpoints, empty/recursive/repeated-hash input cases and exceptional/setup/receipt/
flush/crash paths remain unexercised. No delays, faults, workload or hooks were
manufactured. Logs never infer an unobserved outcome.

## Verification correction, preservation and receiving

One additional authentication helper initially invoked the application package
loader with `-S` outside the retained worker's import finder. It failed to import
the package's required `ck3chronicle.decoder`. This helper error is preserved in
`package-authentication-attempt-1.json`; normal installed `-I -B` application loading
then passes, with the installed decoder path/hash explicitly authenticated.
All five required retained operations already passed with **`-I -S -B`** and were
not rerun or relaxed. No product failure, source repair or outcome discrepancy was
found. No proposed requirements were added.

`A/before.json` and `before/` preserve exactly the prior Learner delivery document
and this new document's prior absence. `guards.json` is a separate read-only
authentication inventory, not a broad rollback baseline. Final preservation checks
retain inputs, prior models/distributions, installed release and wheel. This work
edits no product source, shared catalog, installed resource, default, production
registry or runtime service. Generated evidence remains ignored.

Pipeline receives **the exact package/pin above** and this installed candidate
evaluation on TREK-2, then performs its authorized task-local pinned classification
without rebuilding the unchanged wheel or changing production defaults. The normal
proposed-selection object is retained in `A/artifacts.json` / `export.stdout`;
Pipeline owns its research registration and actual selected execution. No local
model catalog registration was needed on the Learner side.

Physical external placement remains Pipeline's separate item: this installed
release and all outputs are within the checkout, while `C:/Windows` is only cwd.
This work does not claim relocation outside checkout, new database persistence,
a fresh Watcher lifecycle, general model quality, final application acceptance or
production activation. No synthetic test, full-corpus campaign, production
registration/selection, restart, external publication, commit or push occurred.
