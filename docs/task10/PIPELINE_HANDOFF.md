# Task 10A.1 — Pipeline interface and application delivery

## Current replacement for 10B — 2026-10-11

**TREK-9: CMT-106 help/reference correction implemented; replacement delivered
for Launch & Distribution receipt.** Application **0.0.3** carries the received
1,024-result cache from CMT-126/132. Original application receipt CMT-83 and cache
receipt CMT-132 remain valid for their exact artifacts; CMT-133 resolved the tracker
recovery. This delivery does not claim a replacement Windows bundle or activation.

Wheel: `.codex-tmp/pipeline-help-20261011/application/ck3chronicle-0.0.3-py3-none-any.whl`.
SHA-256 **`f03afb5b6abb5d7ee42522d832089d16d20a259374a987ae88dcb0f1a523ee38`**;
**2,805,027 bytes**, 627 ZIP members. Version metadata and `__version__` agree.
Exact source/wheel/installed inventory: `.codex-tmp/pipeline-help-20261011/artifact.json`.
Build recipe/log, isolated installation log, commands and output are in that same
directory. Earlier wheels and prior edited files (`before/`) are preserved.

Changes and affected reference text:

- `ingest --package-id` help now says it overrides the package for this invocation;
  omission uses the saved model pin in configuration. Actual selection behavior is
  unchanged: `[model] package_id` and `manifest_sha256` are required and authenticated.
- [Pipeline reference](../user/PIPELINE_REFERENCE.md) now describes C9's healthy
  default GUI checkboxes and final **Save settings**, per the later Owner direction
  documented in [10B's handoff](DISTRIBUTION_HANDOFF.md). The CLI/API still requires
  acceptance flags for new/changed external paths; the text launcher retains its
  individual questions. No GUI or setup implementation changed here.
- Pipeline reference identifies 0.0.3's 1,024 completed public results while retaining
  C9's 256 limit. The [cache handoff](REQUEST_RESULT_CACHE_HANDOFF.md) records exact
  semantics and genuine verification; 0.0.3's handler bytes match that candidate.

Fresh checks passed: 622 source/wheel/installed payload comparisons, wheel RECORD
hashes/sizes, all 453 unchanged shared-resource members, installed console and module
ingest help from `C:/Windows`, root help, model inventory, and actual default classifier
selection using the existing isolated 10A.1 configuration without modifying it.
The installed model root is inside the new installation. Runtime logging ownership
and dependency checks passed. Compared with cache wheel `94987fb0...`, after normalizing
the versioned ZIP paths, only `cli.py`, `__init__.py`, `METADATA` and `RECORD` differ.
AST comparison proves the CLI delta is the help string; metadata differs only by
version. Prior genuine setup/ingestion/report/history and 1,027-operation cache
evidence is reused by this correspondence; none was rerun or manufactured.

Dependency remains `chardet>=7.6,<8`, tested with 7.6.0 on Windows x64 CPython
3.12.14. Exact dependency wheel SHA-256:
`99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64`.
Model `2b12932103f3a3111a4e1880` / manifest
`02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505` and retained
Learner `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485` /
manifest `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e`
remain unchanged. No retained bytes or models were rebuilt.

Receiving: 10B consumes this exact wheel instead of `94987fb0...` or `2de516e0...`
for its next bundle. 10D updates its final edition's application identity, replaces
the `CLI_REFERENCE.md` ingest stale-help note with the corrected wording, and links
the delivered cache rather than saying delivery is pending. Keep C9-specific claims
until a replacement bundle is identified. Existing setup/model/SQLite command
examples retain their syntax. TREK-10 CMT-127/129, TREK-11 CMT-128/130 and TREK-15
CMT-131 were consumed; canonical manual files and outer packaging remain L&D-owned.
Receive the replacement on TREK-9, then close Pipeline's producer work if no defect
remains. Final bundle/manual/provenance and external/clean-machine receiving stay
on TREK-10/11/16; no sibling work is dispatched by this delivery.

Limits and rollback: fresh install is inside the checkout on a developer host.
No fresh GUI, successful ingestion, cache-boundary, lifecycle, concurrency or
production check is claimed. The initial verification recorder misdecoded Windows
root-help output as UTF-8; an explicit subprocess UTF-8 mode fixed recording and
the check passed without product changes (`recorder-correction.txt`). Application
identity changes in 0.0.3, so stop affected observation/handler before replacing
files; do not reuse a running older handler. Prior evidence remains historical,
not proof of a newly installed outer bundle. Roll back deliberately to a retained
exact wheel with affected processes stopped, preserving configuration/data; older
C9 has its original 256-result cache and stale help. No production, source-publication
or hosted-upload action occurred.

## Original 0.0.2 delivery and dated evidence

2026-10-08 follow-up: the [1,024-result cache delivery](REQUEST_RESULT_CACHE_HANDOFF.md)
updates repository source and supplies a fresh wheel for the next candidate.
The artifact and receiving evidence below continue to identify the original
0.0.2/C9 input; they do not establish activation or receipt of the cache update.

2026-10-08. **TREK-9**, Pipeline → Launch & Distribution. Implementation and
isolated application verification delivered; receiver disposition belongs on
TREK-9. This does not claim outer bundle acceptance, Owner acceptance, publication
or production activation. Design receipts are TREK-7 CMT-77/CMT-80, including the
owner's later path-confirmation and substantive-doctor corrections.

## Interface agreement and ownership

The callable interface and user-facing examples are in
[PIPELINE_REFERENCE.md](../user/PIPELINE_REFERENCE.md). This is Pipeline's technical
reference contribution for 10D/10E, not a substitute for their complete manual.
10B's launcher should call the application CLI/library operations, never duplicate
configuration writing, model authentication or initialization.

Delivered surfaces:

- Global `--config PATH` before the subcommand; otherwise only fixed Windows
  LocalAppData/ck3chronicle/paths.toml. No cwd-config fallback. Help/setup inventory
  are config-free; doctor diagnoses absent configuration without import failure.
- `setup --suggest-paths`, `setup --list-models`, setup preview and `--apply`, with
  text/JSON results. External roots require individual `--accept-path FIELD` when
  first selected/changed. Windows Known Folders supply editable suggestions only.
- Shared setup/doctor checks: CK3 layout evidence, readable required game/log
  directories, optional current log/mod/crash evidence, writable-root containment,
  current database, model authentication, controls and tool settings. Setup owns
  bounded write probes; doctor performs read-only diagnosis and labels uncertainty.
- Initialization saves `create_database().path`; repeat preserves history and user
  settings. Nonempty runtime without an explicit database is rejected. Partial
  creation/save effects are reported; no reset, relocation or database discovery.
- `[model] package_id/manifest_sha256` saves the explicit processing default.
  Installed resources remain immutable; historical lineage stays per Run.
- Explicit child config and application/config identity on handler admission.
  `HandlerClient.probe()` observes without starting; `runtime-stop` uses existing
  shutdown, guarded by the Watcher lease. No automatic restart or OS startup.
- `setup --ripgrep EXE` saves optional `[tools] ripgrep`; report's explicit override
  wins. Missing configuration leaves content search unavailable rather than finding
  an ambient tool. 10B supplies its pinned executable; this task adds no binary.

All TOML-relative paths use the selected file's parent; command-line operands use
invocation cwd. Setup writes absolute owned path values. Runtime processes retain
their loaded configuration; stop observation/handler before changes. The old
implicit cwd/config.toml route requires explicit transition, not a compatibility
search. Setup preserves unrelated TOML values but rewrites comments/formatting.

Routine agreement refinements: read-only doctor returns 2 for any warning/error/
unverified finding; inability to establish write access is normally unverified,
not a new Ready gate. No new snapshot command was needed: SQLite mode=ro with a
short read transaction meets the accepted external-access boundary. Database schema
3 is distinct from model schema 6. See the reference for tables, JSON/count semantics,
writer conditions and separate native-shard access. Reference resolution is lexical,
not an integrity check; the receiving example separately verified the shard hash.

Pipeline owns the edited shared CLI/config/catalog/handler/setup/doctor and wheel
manifest. Watcher lifecycle/harvester/playset, Reporting query/rendering and Learner
code/retained distributions are unchanged. Launch & Distribution owns the outer
`packaging/windows/` recipe, runtime archive, ripgrep binary, launcher interaction
and manual integration. It selects a real available runtime archive and verifies
that combination; the tested venv is not a portable runtime distribution.

## Identified artifact

The final delivery manifest is ignored runtime evidence at
`.codex-tmp/task10a1/release/artifact.json`; its full source/wheel/installed inventory
is the authority for exact correspondence. The wheel is
`.codex-tmp/task10a1/release/application/ck3chronicle-0.0.2-py3-none-any.whl`.
SHA-256 **`2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`**,
2,804,832 bytes. `release/artifact.json` authenticates 622 members in both directions;
`release/final-checks.json` confirms 592 unchanged component/retained payloads.

| Input | Pin / scope |
|---|---|
| Baseline source | Task09 tag `task09-baseline-2026-10-07`, commit `709ea7842a0202c420b43355b18be91d8ca196a3`, TREK-6 CMT-69; Task10 source changes remain uncommitted |
| Prior received wheel | `2dbb613de4fbac058a1ae2f429eea8adf2f85a1c861c859b89eaa0d5d62f1b1e` (0.0.1) |
| New application | 0.0.2; unchanged dependency constraint `chardet>=7.6,<8`, Python >=3.11 |
| Tested runtime | Windows x64 CPython 3.12.14; chardet 7.6.0; pip 25.0.1; no claim for untested Python versions |
| Build tools | Repository setuptools 84.0.0 / wheel 0.48.0; build recipe retained in release/build.py |
| Dependency wheel | Existing chardet cp312 win_amd64 wheel, SHA-256 `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64` |
| Default model | `2b12932103f3a3111a4e1880`, manifest `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505`; adopted production order 9 |
| Retained Learner | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`, manifest `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e`; adopted order 10 |

Packaging catalogs now reflect those already-adopted production statuses/orders
and their existing publication evidence. Their Task09 wheel copies still said
research; only those three fields in each latest row were aligned with the canonical
catalogs. Retained model/Learner payloads, manifest pins, prior rows and installed
selection bytes remain unchanged. This is metadata correspondence in a fresh wheel,
not a new model publication. The production installation and canonical catalogs
were not modified.

## Verification and evidence limits

All evidence is under ignored `.codex-tmp/task10a1/`; originals remain outside Git.
`before/` preserves edited prior files, including the coupled repository exception
annotation and packaging catalogs. Newly introduced setup/runtime-identity/reference/
handoff files had no prior version. Earlier candidates and their receipts are kept;
the release directory identifies the final candidate, not a moving alias.

Executed normal operations use genuine paths from the user's existing explicit
config and task-owned isolated storage. CLI subprocesses run from `C:/Windows`;
installed imports/resources come from the isolated application prefix.

| Check | Evidence and practical limit |
|---|---|
| Source/wheel/installation | Full bidirectional 622-member authentication, every available retained Learner release, exact shipped default and dependency check. Entry-point metadata retained. |
| First/repeat setup | Config-free help/inventory, mutation-free preview, exact returned database persisted, repeat empty/populated setup. Database/capture/review hashes unchanged by repeat. |
| Real data | Genuine capture `20261003-D3N7ZQ`, log SHA-256 `5a7b93d8ee374c60f767593631713eaf8719004ba4f9cf33e7eb5d812dbec629`; normal public-handler ingestion. Playset members and source capture metadata preserved. |
| Reports/external read | Text/JSON/HTML report; 1,066 diagnostic records and 1,838 occurrences match a SQLite mode=ro read transaction. Native review reference resolves and actual log hash agrees. |
| Configuration/children | Explicit absolute and relative config paths from unrelated cwd; handler reports matching canonical authority, installed source/resource root and executable. Actual LocalAppData path resolution checked; default-location writes are outside this session's scope. |
| Model timing | Deliberately select retained prior package, ingest genuine G2 `05d71d...` through normal API, observe that package in new Run lineage; restore full-model default and verify prior Run rows unchanged. |
| Doctor/journals | Doctor leaves all data files unchanged. Findings explicitly mark write access unverified. Actual setup events and foreground request references match handler completions. |
| Unchanged behavior | Byte correspondence to Task09 establishes unchanged Watcher/Reporting/retained payloads; prior lifecycle/Learner evaluation receipts retain their original scope. No fresh live lifecycle is claimed. |

Commands/stdout/stderr/exits, stored results, before/after hashes and handler identity
are retained in `commands.json`, `verification.json`, `stored.json`,
`supplement-commands.json`, `supplement.json` and the referenced output files.
The runtime logging ownership checker and source parsing checks passed. No mock
clients, invented logs/history, injected failures or full-corpus campaign ran.

Final-wheel genuine Run IDs: `20261008-VZP1CG` for the captured playset example;
the prior-package selection example's ID is in `release/supplement.json`. The
supplement matches **21 foreground request references** to handler completions
across **12 journals**, verifies preserved source facts/playset members and review
hash, and records the restored production selection. Task-started handlers were
explicitly shut down. The fixed bootstrap path was resolved read-only; its file
was not created or changed. Final CLI help, model inventory, doctor, retained
Learner/model admin help and dependency checks are recorded with actual exit codes.

Verification corrections: the initial source-inspection invocation used unsupported
`python -m ck3chronicle`; the existing executable/module route is `ck3chronicle` or
`python -m ck3chronicle.cli`, and that route passed. An authentication recorder first
compared Windows backslash paths with baseline slash paths and incorrectly listed
unchanged members as changed; the original receipt is retained, normalization was
corrected and the exact source/wheel/installed comparison passed. A read-only Windows
process inventory was denied by this environment; no process was killed or runtime
state inferred from that failure. Handler shutdown/identity evidence uses its public
API. No failed product acceptance check remains concealed by those corrections.

Unverified cases remain explicit: setup with genuinely absent current error.log
(the current real logs directory contains it), unfamiliar/invalid installations,
invalid TOML/permissions/schema and partial-save failures, active-watcher refusal,
incompatible live-handler rejection and interruption/concurrency races. Implemented
guards were inspected; absent genuine cases were not manufactured. Doctor does not
prove executable tool version or write access. The actual fixed LocalAppData file,
physical outside-checkout install and clean-machine/runtime-archive proof remain
10B/10C work in a suitably authorized environment. No synthetic permission is inferred.

## Receiving, continuation and rollback

10B receives the wheel and CLI contract on TREK-9, supplies the runtime/ripgrep and
guided per-field confirmation, and verifies its actual installation layout. 10D/10E
receive `PIPELINE_REFERENCE.md`, use exact returned paths/IDs and preserve the explicit
evidence limits. At final refresh those assignments had no enrolled record or incoming
question; their prepared prompts were read. They are not silently dispatched here.

Pipeline retains real implementation/receiving defects until resolved; outer-bundle
or Docs-only work stays on its receiving assignment after technical receipt. Record
the consumer's actual `receipt` on TREK-9 before closing it. Launch & Distribution
can reconcile 10A's stale pre-receipt prose using CMT-80; Pipeline does not edit its
owned design. No further material Owner scope choice was identified.

Rollback is deliberate: stop observation and explicitly shut down the task's
handler before replacing application files or selection. Prior immutable application
artifacts remain retained. Application 0.0.1 still has its old configuration route;
do not imply it understands this setup contract. Do not switch the production copy
or overwrite its config to demonstrate rollback. Compatible model rollback uses
setup's explicit available package selection and preserves stored history. Do not
copy a live SQLite file as a full backup or use rollback to reset/reprocess Runs.

Implemented, locally packaged and verified within stated limits; receiving pending.
No source commit/tag/push, hosted upload, production configuration/database change,
live-service restart or Owner acceptance is claimed.
