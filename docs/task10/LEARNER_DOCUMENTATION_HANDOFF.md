# Task 10D — Learner documentation contribution

2026-10-08. Producer **Learner / TREK-14**, receiver **Launch & Distribution —
Docs / TREK-11**. Authority: the owner-issued
[component contribution](../task10-deliverables/COMPONENT_DOCUMENTATION_INPUT.md),
[10D](../task10-deliverables/10D_PRODUCT_REFERENCE.md),
[10E](../task10-deliverables/10E_USER_WORKFLOWS.md) and
[working agreement](../task10-deliverables/WORKING_AGREEMENT.md).
Task09 TREK-2 stays completed. This contribution commissions no product repair.

## Editorial boundary and exact release

Ready-to-integrate user text is between **Reference contribution begins/ends**
below. Proposed canonical destination is `docs/user/LEARNER_REFERENCE.md`, linked
from the CLI and configuration references. Placement/shared-row coordination was
requested on TREK-11 CMT-95; Docs owns final manual integration. This handoff is
technical input, not a second final manual. Record actual receipt on TREK-14;
10C owns final manual acceptance. Future interface changes need corresponding
reference/example corrections from Learner.

| Identity | Verified value |
|---|---|
| Application | 0.0.2, wheel SHA-256 `2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594` |
| Learner release | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485` |
| Learner manifest SHA-256 | `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e` |
| Algorithm / fingerprint | `outer-diagnostic-consensus-v61` / `67f881e22dfec7477ee2fe423a1c9789285acab6825c2b78fa3065996bcd52a9` |
| Parser / code SHA-256 | `ck3-lossless-v1.8` / `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Production model package | `2b12932103f3a3111a4e1880` |
| Model manifest SHA-256 | `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505` |
| Model revision / schema | `3bc531d578074e6a430c161e` / 6 |
| Matcher / selector | `ck3-native-matcher-v3` / `complete-assignment-v2` |

Pipeline's [0.0.2 handoff](PIPELINE_HANDOFF.md) and TREK-9 CMT-81/83 establish
the received application. The [10B handoff](DISTRIBUTION_HANDOFF.md) supplies
the outer Windows layout. Task09 TREK-2 CMT-58/60/64 and TREK-6 CMT-69 distinguish
build, receipt, production adoption and source publication. Production orders
10 (Learner) and 9 (model) are sequence numbers, not version numbers. The old
0.0.1 wheel's research catalog metadata was updated in 0.0.2; retained bytes did
not change. Do not repeat historical pending/adoption wording as current status.

## Reference contribution begins

### Learning and release administration

These are advanced tools for model maintainers. Ordinary capture, ingestion and
reporting use the installed model and need no training. A learning result is a
candidate; creating or exporting it does not select it for processing or change
stored Runs. Inputs are complete protected CK3 logs, read without modification.
Use separate writable locations for candidates, registry state, reviews and logs.
Keep those files outside immutable release folders.

Use `ck3chronicle-learner-release` from an application installation. Its equivalent
module entry point is `python -m template_learning.learner_loader` using that
installation's interpreter. In the Windows bundle, use the private interpreter;
the regular `ck3chronicle.cmd` entry point is not a Learner subcommand wrapper:

```powershell
# Run in your extracted bundle folder. These are user-chosen example paths.
$python = (Resolve-Path '.\runtime\python.exe').Path
$learner = '2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485'
& $python -I -B -m template_learning.learner_loader list --log-dir 'D:\CK3Work\journals'
```

The module and console command have identical arguments below. Standalone Python
installations require Python 3.11+ and the installed application dependencies;
the verified Windows combination uses CPython 3.12.14. The retained worker uses
isolated Python (`-I -S -B`) and authenticated retained imports, including its
decoder and journal backend. Missing retained modules do not fall back to an
installed or development copy. This is executable provenance isolation, not an
operating-system security sandbox or a cross-platform reproducibility guarantee.

### Select and run an exact Learner

```text
ck3chronicle-learner-release list [--root ROOT] [--log-dir DIR]
ck3chronicle-learner-release run [--root ROOT] --release ID
    [--receipt FILE] [--log-dir DIR] OPERATION -- OPERATION_ARGUMENTS
```

`list` prints catalog JSON. It inventories entries; it does not authenticate all
their payloads. `run` selects the unique exact release ID, checks availability,
the external manifest pin and retained payload hashes, then starts its worker.
Complete releases expose `learn`, `registry`, `evaluate`, `publish`, `review`,
`visual-review` and `compare`. Historical partial releases expose only their
manifest's operations, normally historical evaluation.

| Argument | Type, default and meaning |
|---|---|
| `--root` | Catalog-directory path. Default is an adjacent development `learners` directory when present, otherwise `<sys.prefix>/share/ck3chronicle/learners`. Explicit value wins; it is unrelated to runtime TOML model selection. |
| `--release` | Required full release-ID string. No implicit newest/production selection. |
| `--receipt` | Optional JSON output filename, omitted by default. Parent directories are created; an existing file is overwritten. Records actual executable/parser/rule hashes, arguments, Python/Unicode versions and observed result. |
| `--log-dir` | Optional journal-directory path. For this `journal_api: 1` release: explicit directory, otherwise `<receipt parent>/learner-logs`, otherwise `<cwd>/.ck3chronicle/wip/learner-logs`. |
| `OPERATION` | One of the seven operation names above; availability is checked against the chosen release. |
| `--` | Separates operation arguments. All outer options must precede the operation; options after it belong to that operation. |

Use absolute input/output paths to make invocation independent of the working
directory. Relative filesystem arguments are resolved from the invoking cwd,
not from the catalog or settings file. There is no per-operation rule override.
The launcher supplies the selected release's parser manifest for `learn` and
registry `sync`/`build`; if explicitly supplied, `--parser-manifest PATH` must
resolve to that same retained manifest.

Explicit paths make these operations independent of application configuration.
Registry is the exception when convenience arguments are omitted: the outer
application loader reads configured `ROOT_LEARNER_STATE/<release ID>` for missing
`--state-root` and configured `ROOT_CK3CHRONICLE` for missing sync `--runtime-root`.
Supply both to avoid that import. Calling the retained `launcher.py` directly
does not provide an application-config fallback; use all explicit paths there.
No Learner command accepts the root application's `--config` switch.

Successful operations return zero. Top-level argument errors return argparse's
code 2; authentication/I/O/worker failures return nonzero, commonly with a Python
traceback. A worker's own nonzero code is not a stable outer-command code: the
parent uses `subprocess.run(check=True)`. Check the actual outer exit and receipt/
journal rather than promising all nested usage errors propagate as 2. Receipts
can be absent when failure precedes worker execution; output existence alone
does not prove completion. An existing partial output is not automatically rolled
back after a failure.

For this release a successful journal open is announced once on stderr as
`Learner journal: PATH`; stdout remains operation output. Journals are
`learner-<invocation ID>.jsonl`, with 10 MiB rotation and five backups. Admin
commands use `learner-admin-<ID>.jsonl` and, without `--log-dir`, the cwd default
above. Help opens no admin journal. Operations, including read-only inspection,
still create their invocation journal and any requested receipt. Journal-open
failure has no fallback. Older releases without journal capability reject an
explicit `--log-dir`; omitting it preserves their older behavior.

### Build directly from protected logs

```text
learn -- (--log FILE [--log FILE ...] | --runtime-root ROOT)
    --output-dir DIR [--threshold FLOAT] [--exclude-sha256 HASH ...]
```

Use either repeated explicit logs or one protected-input root. A root is scanned
only for immediate `sessions/<name>/error.log` and `pending/<name>/error.log`
children; session `.staging` and pending `.copying-*` directories are skipped.
This is not recursive arbitrary-folder or live-log discovery. Identical content
hashes are deduplicated; repeated `--exclude-sha256` values exclude input content
case-insensitively. No remaining input is an error. Threshold is a float,
default **0.72**, used for clustering; it is not a promised accuracy score. The
argument parser supplies no numeric range check.

The command writes an immutable revision directory under `--output-dir`, including
candidate model, manifest, native evidence and retained dependencies. It prints
JSON with `bundle` and the model summary. An existing same-ID bundle must have
identical authenticated payloads; its recorded build-command metadata is preserved.
Preserve unknown and unresolved evidence; they are legitimate
outcomes, not an instruction to increase the threshold until they disappear.

```powershell
# Illustrative command; not executed in this documentation assignment.
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\learn.json' learn -- --log 'D:\Protected\run-a\error.log' --output-dir 'D:\CK3Work\candidates'
```

### Maintain an incremental registry

```text
registry -- --state-root DIR sync --runtime-root ROOT
    [--default-role {candidate,training,holdout,ignored}]
registry -- --state-root DIR role SHA256 {candidate,training,holdout,ignored}
registry -- --state-root DIR build [--threshold FLOAT]
registry -- --state-root DIR status
```

`--state-root` goes before the registry subcommand. Use a separate state root per
Learner release. Existing state is checked against the selected release, learner
fingerprint and parser; incompatible state is rejected, not migrated or replayed.

| Subcommand | Effect and output |
|---|---|
| `sync` | Scans the protected layout described above; records content identities, observed paths and parser-bound feature caches. Default role is **candidate** for newly discovered hashes only; prior roles stay unchanged. JSON reports paths seen/hashed, new/known evidence, caches and roles. Original logs remain read-only; this is not a raw-log backup. |
| `role SHA256 ROLE` | Updates one already-known content hash, case-insensitively. JSON reports hash, prior role and new role. |
| `build` | Uses only **training** evidence and validated caches; at least one is required. Writes a new immutable candidate in `revisions/<revision ID>`, updates registry `current_revision`/history and prints revision, bundle, model path/hash and summary. Default threshold is **0.72**; subsequent additive builds must keep the previous threshold. |
| `status` | Prints state root, learner identity, feature version, evidence/role totals, revision count/current revision and per-hash observations/cache counts. Missing registry gives an empty in-memory status; it does not create a persisted registry. |

Candidate, holdout and ignored evidence are excluded from training. Assigning
`holdout` does not execute evaluation or establish an independent accuracy claim.
Role changes affect subsequent builds, not existing candidate revisions. Builds
are additive; removing a hash from training does not promise to unlearn prior
templates. Keep protected input bytes immutable: sync can reuse the known hash
when path, size and modification time are unchanged. Mutations use an exclusive
`.registry.lock`; concurrent use fails rather than merging, and no automatic
stale-lock recovery is promised. Generated registry/cache JSON is not a user-edit
configuration surface; change roles through the command.

```powershell
# Sync/build structure reuses genuine prior execution; paths are substituted.
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\sync.json' registry -- --state-root 'D:\CK3Work\registry' sync --runtime-root 'D:\Protected' --default-role training
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\build.json' registry -- --state-root 'D:\CK3Work\registry' build --threshold .72
# Illustrative inspection/role change; replace the hash with a status entry.
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' registry -- --state-root 'D:\CK3Work\registry' status
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' registry -- --state-root 'D:\CK3Work\registry' role '<input-sha256>' holdout
```

### Evaluate a candidate and export a model package

```text
evaluate -- --bundle CANDIDATE_DIR --log FILE --output JSON_FILE
publish -- --bundle CANDIDATE_DIR --output-dir DIR
publish -- --source-release DIR --expected-manifest-sha256 HASH
    --validation-log FILE [--validation-log FILE ...] --output-dir DIR
```

All shown paths are required for their respective form. `evaluate` checks
candidate hashes, revision and matching Learner/parser identity. It writes JSON
containing model/input identities, evidence, summary, complete records and
unresolved evidence; stdout contains the summary. Published models require their
runtime package evaluation route, `ck3chronicle-model-release evaluate`, owned by
Pipeline. Candidate evaluation does not ingest a Run or alter SQLite.

`publish --bundle` validates compact export against the saved native candidate
evidence and writes `<output-dir>/<package ID>`. It prints package/revision IDs,
folder, manifest hash and a proposed selection. This is **local export**, not a
network upload, catalog registration or active selection. In particular the
printed `candidates/<ID>` selection path is a conventional suggestion, not proof
of the actual exported or installed location. Use Pipeline's catalog/selection
interfaces and setup for installation and active configuration.

The alternative `--source-release` route retains compatible published model
definitions with the chosen implementation and requires an external manifest
pin and at least one genuine validation log. It makes a new package with new
validation; it is not copying an old package or inheriting proof for changed
code. Unsupported historical formats are rejected. `--bundle` and
`--source-release` are mutually exclusive; pin/validation options apply only to
the source-release branch. Registration is the copy-existing-release route.

```powershell
# Genuine prior evaluate/export structure; paths substituted, not rerun here.
$candidate = 'D:\CK3Work\registry\revisions\d729dea94d84323b8497e882'
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\evaluate.json' evaluate -- --bundle $candidate --log 'D:\Protected\run-a\error.log' --output 'D:\CK3Work\evaluation.json'
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\export.json' publish -- --bundle $candidate --output-dir 'D:\CK3Work\packages'
# Unexecuted alternative; substitute a compatible source and its exact pin.
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\repackage.json' publish -- --source-release 'D:\Releases\source-package' --expected-manifest-sha256 '<manifest-sha256>' --validation-log 'D:\Protected\run-a\error.log' --output-dir 'D:\CK3Work\packages'
```

### Inspect candidate evidence and specialized comparisons

| Operation syntax after `run ... OPERATION --` | Output and limits |
|---|---|
| `review --bundle DIR --output-dir DIR` | Writes `INDEX.md`, per-example Markdown, template JSON definitions, `refinement-history.json` and `unresolved.json`. Preserves all occurrence references; no ordinary stdout summary. |
| `visual-review --bundle DIR --output FILE [--top INT] [--examples INT]` | Writes review JSON and prints JSON summary. Defaults: top **20**, examples **3**; both must be positive. Examples are selected supports, not a random sample. |
| `visual-review --bundle DIR --output FILE --diagnostics --previous-review JSON --baseline DIR [--html FILE]` | Specialist all-template metrics/prior-case export; baseline and previous review are required together. Optional HTML is generated only in this branch; inline HTML must stay below 1 MB. Uses compatible prior review schema, stable native cases and matching parser; not an arbitrary before/after comparison. `--top`/`--examples` do not control this branch's fixed sample selection. |
| `compare --before DIR --after DIR --output DIR --selection JSON` | Specialized single-assignment comparison; writes `comparison.json`, `examples.json`, `all-change-groups.json` and `REVIEW.html`, and prints comparison JSON. Requires identical example sets/occurrence counts, preserved selected bindings and 25 selected examples; reads referenced protected logs to verify displayed bytes. Not a general model/version comparator. |

These operations write review outputs, without updating model definitions or
registry state. Choose new output locations: ordinary review files can overwrite
existing files. For `compare`, selection JSON supplies `logs`, an array of
objects with string `sha256` and original protected-log `path`. An adjacent
`same-30-results.jsonl`, if present, supplies legacy per-example cohort weights.
Do not fabricate those generated weights. The retained comparison HTML contains
a historical parser-v1.6 description; obtain actual parser identity from the
authenticated candidate, not that sentence. Current-release functional evidence
for these specialist review variants has not been established by this reference.

```powershell
# All four review examples are illustrative/unexecuted for this release.
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' review -- --bundle $candidate --output-dir 'D:\CK3Work\review'
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' visual-review -- --bundle $candidate --output 'D:\CK3Work\visual.json' --top 20 --examples 3
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' visual-review -- --bundle $candidate --output 'D:\CK3Work\diagnostics.json' --diagnostics --baseline 'D:\CK3Work\baseline' --previous-review 'D:\CK3Work\prior-review.json' --html 'D:\CK3Work\diagnostics.html'
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' compare -- --before 'D:\CK3Work\before' --after $candidate --output 'D:\CK3Work\comparison' --selection 'D:\CK3Work\selection.json'
```

### Create and register a Learner release

```text
ck3chronicle-learner-release create --source DIR --output DIR
    [--application-source DIR] [--historical-identity JSON] [--log-dir DIR]
ck3chronicle-learner-release register [--root DIR] --source DIR
    --manifest-sha256 HASH [--production-order INT --publication-evidence TEXT]
    [--log-dir DIR]
```

These are release-maintainer operations. `create` needs a complete supported
source tree; it copies source/rules/assets into a content-addressed directory
and authenticates it. It does not train a model. Normal complete creation also
requires `--application-source` pointing to the source directory supplying decoder,
runtime logging and journal modules, although argparse labels this option optional.
`--historical-identity` instead accepts an authenticated historical fingerprint
JSON and matching historical source, creating an evaluation-only envelope; it
is a legacy maintenance route, not a way to relabel current code. Output JSON
includes release ID, manifest SHA-256, folder, learner fingerprint and completeness.

`register` authenticates an existing distribution against the required pin,
copies it under `<root>/releases/<ID>` and records its catalog row. Omitted
production order means research. Production metadata requires a positive integer
order and nonempty evidence reference; an established order/row cannot be changed
by re-registering. An identical existing registration is accepted. Conflicting
immutable bytes or metadata are errors. Catalog replacement uses a temporary
file; this does not make a whole multi-file operation transactional.

```powershell
# Illustrative maintainer commands; not executed in this assignment.
& $python -I -B -m template_learning.learner_loader create --source 'D:\Source\template_learning' --application-source 'D:\Source\ck3chronicle' --output 'D:\CK3Work\learner-releases' --log-dir 'D:\CK3Work\journals'
& $python -I -B -m template_learning.learner_loader register --root 'D:\CK3Work\learner-catalog' --source 'D:\CK3Work\learner-releases\<release-id>' --manifest-sha256 '<manifest-sha256>' --log-dir 'D:\CK3Work\journals'
```

Registration takes effect on the next catalog read or explicit invocation. It
does not change an already-running worker, build a new application wheel or select
a production model. Use a separate writable catalog for maintenance; installed
distribution resources remain immutable. There is no pruning/deletion command.
Retention policy preserves at least the latest ten production Learner versions
and ten distinct production model revisions; this does not assert ten currently
available versions or authorize deleting older ones.

### Identities and JSON edit boundaries

| File/identity | Meaning and supported changes |
|---|---|
| Application version/wheel hash | Identifies the host application; independent of Learner algorithm and release IDs. |
| Learner `release_id` | Full SHA-256 of canonical manifest excluding the ID field. Selects one retained executable closure; changed bytes require a new distribution. |
| `learner_identity.sha256` | Algorithm implementation fingerprint, separate from distribution ID and descriptive algorithm label. |
| Candidate/model revision | Identity of candidate/model content. Compact exported model revision can differ from research candidate revision. |
| Model `package_id` | 24-hex identity of executable package combination; unchanged model revision can have a new package identity after implementation changes. |
| Manifest pin and `hashes` | External manifest SHA-256 plus per-payload hashes authenticate exact bytes. Catalogs/pins are local trust anchors, not publisher signatures. |
| `owner_rules.json` | Release-bound literal, construction, inference and parameter declarations. No supported user override or hot reload; edit only in a separately commissioned source change, then build a new release. |
| Parser manifests / `recovery_rules.json` | Release-bound parser/recovery behavior, authenticated with the executable. Not runtime configuration. |
| Candidate model, native evidence, package JSON | Generated authenticated data; do not hand-edit templates, captures, status, hashes or manifests to promote/reclassify evidence. |
| Catalog JSON | Generated/maintained release inventory: identity, retained path, manifest pin, availability, operations, publication status/order/evidence. Use registration; metadata is not active selection. |
| Registry/cache JSON | Generated mutable state under its owning commands. Role CLI changes next-build inputs; manual edits are unsupported. |
| Execution receipt/journal/evaluation/review JSON | Generated evidence. Preserve originals; interpretation or annotations belong in separate files. No edits change the executed operation. |
| `compare` selection JSON | Explicit specialized input: `logs` array of hash/path references to real evidence. Paths may be prepared for the actual files; hashes must describe those files. Other review inputs are generated prior results, not arbitrary query JSON. |

Runtime settings and Reporting query JSON have their own editable schemas in the
configuration/reporting references. They cannot override Learner rules or rewrite
historical lineage. Model selection for future processing is Pipeline-owned.
The private `_execute`/`_execute_journal_v1` protocols and empirical one-off
investigation/report scripts are implementation/developer utilities, not supported
user entry points. In particular the legacy `mirror_incremental_build.py` helper
does not supply this release's journal transport; use public `run ... registry`
for supported incremental work.

## Reference contribution ends

## Evidence, limitations and receiving

Fresh read-only verification is retained outside Git at
`.codex-tmp/task10d-learner/verification.json` with exact commands, stdout/stderr,
exit statuses and hashes. `verify.py` is the small evidence reader, not a product
test or fabricated acceptance case. It reauthenticated **120 files** against the
actual baseline delivery inventory, **49 retained members** across source/wheel/
0.0.2 staged installation, the wheel pin and current installed outer loader.
Five installed invocations from `C:/Windows` passed: top-level/create/register/run
help and catalog list. List returned the expected release/pin, production order
10 and wrote only its isolated admin journal. Help proves syntax, not build effects.
The original list output is retained; public example paths are substitutions.
The copyable private-interpreter module route was also freshly exercised for help
and list from the **local staged C9 bundle**, outside its cwd: both exit 0.
`bundle-commands.json` retains argv/output/exits; `bundle-correspondence.json`
checks all 49 retained members, outer loader equality, identical catalog output
and the one actual successful admin terminal. This verifies the local bundle
syntax, not the inaccessible external installed copy.

| Example / operation | Evidence status and exact scope |
|---|---|
| `list`, admin/run help | Fresh installed 0.0.2 commands, exit 0. `help.stdout`, `create-help.stdout`, `register-help.stdout`, `run-help.stdout`, `list.stdout` and matching stderr. Local C9 `bundle-help`/`bundle-list` additionally verify the private-interpreter example route. |
| `registry sync`, `registry build` | Reused authenticated baseline `sync-{20,40,60,73}` / `build-{20,40,60,73}` command, receipt, stdout/stderr and journals. All exit 0; explicit state/input/parser paths; 73 genuine logs, batches 20+20+20+13, threshold .72. |
| `evaluate` | Reused `evaluate-command.json`, `evaluate-execution.json`, `evaluation.json`, stdout/stderr and journal; exact selected release, genuine G2 input hash `05d71d156d3298e25568e4727d2fb15da111c2b74f8d18be29149e09e150ce95`. 4,141 full / 65 provisional / 0 unknown, zero unresolved. G2 is training evidence, not unseen quality. |
| `publish --bundle` | Reused `publish-command.json`, receipt/stdout/stderr/journal, exact package manifest and native validation. 91,925 contextual messages / 2,594,588 occurrences / 371,403 captures validated; no changed matches/outcomes. Local export only. |
| `learn`; registry `role`/`status`; `review`; both `visual-review` forms; `compare`; `publish --source-release` | Illustrative examples; not freshly executed or claimed functionally verified here. Exact retained parsers/implementation inspected. Some earlier component receipts cover learning, but this contribution does not promote them into fresh current-release verification. |
| `create`, `register`, historical creation and production metadata variants | Syntax/implementation inspected; examples unexecuted here. Existing genuine creation/registration/adoption is recorded in the Observer-free delivery and TREK-2 CMT-64; the illustrative commands are not those exact receipt commands. No fresh publication or catalog mutation commissioned. |

Baseline evidence root is `.codex-tmp/trek2-baseline-20261007/`; all ten execution
receipts/journals were checked for exact release/pin, completed status, successful
terminal and absence of imported application configuration. This is reuse of the
actual [73-log delivery](../learner-next-release/PRODUCTION_SCOPE_BASELINE.md),
received by Pipeline in TREK-2 CMT-60; no build/evaluation/export was rerun. Full
training results preserve **2 unknown occurrences**, with **2,476,548 full /
118,038 provisional** and zero unresolved for that corpus. Those are different
scopes from G2 and must not be summed or called holdout accuracy.

The external C9 runtime directory read was denied by the session's filesystem
policy. No bypass or external command execution followed. Fresh checks used the
received staged 0.0.2 installation. 10B's C9 external installation receipt remains
producer evidence with its stated scope; no new clean-machine or external Learner
execution claim is made. Rotation, exceptional receipt/journal failure, partial
write recovery and specialist review branches remain unexercised.

### Concrete discrepancies and disposition

1. `compare` retains a parser-v1.6 HTML sentence although this release uses v1.8,
   plus corpus-specific equal-evidence/25-example assumptions. Source-inspected
   limitation, not an observed failure in a newly run comparison. Learner owns
   any separately issued correction; no immutable bytes or requirements changed.
2. `create --application-source` is optional in help but required by normal
   complete-release creation. Documented as effective requirement; no source fix.
3. Registry omitted-path convenience depends on outer application configuration;
   direct retained execution with missing paths cannot be called configuration-free.
   Explicit paths are the supported independent route verified in genuine receipts.
4. The legacy private mirror helper lacks required journal transport; already
   dispositioned in the baseline handoff/TREK-2 CMT-60. Public registry invocation
   remains usable. This does not reopen Task09.

No failed product acceptance check occurred in this assignment. The denied external
directory read is an evidence-access limit. Final Docs editing and user-side
workflow verification remain on TREK-11/10E; final installed manual acceptance is
10C. Docs should preserve these limits, use one canonical final section, record
the TREK-14 ID/link in the coverage handoff and assignment contribution table, and
record technical receipt or exact correction on TREK-14.
