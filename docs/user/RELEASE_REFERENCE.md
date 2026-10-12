# Model and Learner administration

Application 0.0.3. These advanced interfaces are for model maintainers and
empirical Learner users. For ordinary runtime model selection, use
[setup](CLI_REFERENCE.md#setup).

Replace the example paths below with separate writable work locations.
Catalog registration, candidate construction and active runtime selection have
different effects. All path operands resolve from the invocation directory.
Explicit output/log/state roots keep operations independent of runtime settings.

```powershell
$package = '2b12932103f3a3111a4e1880'
$release = '2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485'
$logs = 'D:\LearnerWork\journals'
$candidate = 'D:\LearnerWork\candidates\<returned candidate directory>'
$inputLog = 'D:\ProtectedInputs\error.log'
```

## Model catalog commands

```text
ck3chronicle-model-release [--models-root PATH] [--log-dir PATH] COMMAND
```

Use `.\ck3chronicle-model-release.cmd` in the Windows bundle. Global options
precede the command. `--models-root` defaults to installed model resources;
`--log-dir` defaults to `<cwd>/.ck3chronicle/wip/model-release-logs`.
Commands write an invocation journal; help displays usage. Use setup to change the
active runtime model. Select this tool’s resource and journal paths with the
options above; application `--config` belongs to the main CLI.

| Command | Required inputs, output and side effects |
|---|---|
| `list` | JSON release inventory on stdout, including unavailable historical entries. Catalog presence alone does not authenticate every payload. |
| `selection --package ID` | Exact available package ID; prints schema-2 selection JSON, including manifest pin and retained path. Use setup to persist the active selection. |
| `evaluate --package ID --log PATH --output PATH` | Authenticated published package and genuine complete input. Writes full JSON evaluation with prepared records and unresolved/no-match outcomes; stdout omits full `records`. No ingestion or database write. |
| `register --source DIR --manifest-sha256 HASH` | Authenticate and retain an existing package, updating catalog JSON. Optional `--production-order N` requires N>=1 and `--publication-evidence TEXT`; omitting order registers it for research. Existing publication order and bytes remain immutable. |

```powershell
.\ck3chronicle-model-release.cmd --log-dir $logs list
.\ck3chronicle-model-release.cmd --log-dir $logs selection --package $package
.\ck3chronicle-model-release.cmd --log-dir $logs evaluate --package $package --log $inputLog --output 'D:\LearnerWork\model-evaluation.json'
.\ck3chronicle-model-release.cmd --models-root 'D:\ReleaseWork\models' --log-dir $logs register --source 'D:\ReleaseWork\built-package' --manifest-sha256 '<exact manifest SHA-256>'
```

Successful commands exit 0; parser errors exit 2; operational/authentication
exceptions return nonzero (normally 1). Inspect stderr and journal. Evaluation
records input hash, actual model/parser/package lineage, application source
fingerprint and environment. Registration needs a writable destination; select
an explicit authoring catalog, not the installed bundle, whose files are verified
as immutable distribution contents.

## Learning and release administration

These are advanced tools for model maintainers. Ordinary capture, ingestion and
reporting use the installed model. A learning result is a
candidate; creating or exporting it does not select it for processing or change
stored Runs. Inputs are complete protected CK3 logs, read without modification.
Use separate writable locations for candidates, registry state, reviews and logs.
Keep those files outside immutable release folders.

Use `ck3chronicle-learner-release` from an application installation. Its equivalent
module entry point is `python -m template_learning.learner_loader` using that
installation's interpreter. In the Windows bundle, use the private interpreter:

```powershell
# Run in your extracted bundle folder. These are user-chosen example paths.
$python = (Resolve-Path '.\runtime\python.exe').Path
$learner = '2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485'
& $python -I -B -m template_learning.learner_loader list --log-dir 'D:\CK3Work\journals'
```

The module and console command have identical arguments below. Standalone Python
installations require Python 3.11+ and the installed application dependencies;
the Windows bundle uses CPython 3.12.14. The retained worker uses
isolated Python (`-I -S -B`) and authenticated retained imports, including its
decoder and journal backend. Missing retained modules do not fall back to an
installed or development copy. This is executable provenance isolation, not an
operating-system security sandbox or a cross-platform reproducibility guarantee.

## Select and run an exact Learner

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
| `--release` | Required full release-ID string selecting the exact retained implementation. |
| `--receipt` | Optional JSON output filename, omitted by default. Parent directories are created; an existing file is overwritten. Records actual executable/parser/rule hashes, arguments, Python/Unicode versions and observed result. |
| `--log-dir` | Optional journal-directory path. For this `journal_api: 1` release: explicit directory, otherwise `<receipt parent>/learner-logs`, otherwise `<cwd>/.ck3chronicle/wip/learner-logs`. |
| `OPERATION` | One of the seven operation names above; availability is checked against the chosen release. |
| `--` | Separates operation arguments. All outer options must precede the operation; options after it belong to that operation. |

Use absolute input/output paths to make invocation independent of the working
directory. Relative filesystem arguments resolve from the invoking directory.
Rules belong to the selected release. The launcher supplies that release’s parser
manifest for `learn` and registry `sync`/`build`; if explicitly supplied,
`--parser-manifest PATH` must resolve to that same retained manifest.

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
parent uses `subprocess.run(check=True)`. Check the actual outer exit and receipt/journal. Receipts
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

## Build directly from protected logs

```text
learn -- (--log FILE [--log FILE ...] | --runtime-root ROOT)
    --output-dir DIR [--threshold FLOAT] [--exclude-sha256 HASH ...]
```

Use either repeated explicit logs or one protected-input root. A root is scanned
only for immediate `sessions/<name>/error.log` and `pending/<name>/error.log`
children; session `.staging` and pending `.copying-*` directories are skipped.
Use explicit `--log` arguments for protected files outside that layout. Identical content
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
# Example: build a candidate from a protected input log.
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\learn.json' learn -- --log 'D:\Protected\run-a\error.log' --output-dir 'D:\CK3Work\candidates'
```

## Maintain an incremental registry

```text
registry -- --state-root DIR sync --runtime-root ROOT
    [--default-role {candidate,training,holdout,ignored}]
registry -- --state-root DIR role SHA256 {candidate,training,holdout,ignored}
registry -- --state-root DIR build [--threshold FLOAT]
registry -- --state-root DIR status
```

`--state-root` goes before the registry subcommand. Use a separate state root per
Learner release. Existing state is checked against the selected release, learner
fingerprint and parser; incompatible state is rejected.

| Subcommand | Effect and output |
|---|---|
| `sync` | Scans the protected layout described above; records content identities, observed paths and parser-bound feature caches. Default role is **candidate** for newly discovered hashes only; prior roles stay unchanged. JSON reports paths seen/hashed, new/known evidence, caches and roles. Original logs remain read-only. Keep their protected copies separately from the registry. |
| `role SHA256 ROLE` | Updates one already-known content hash, case-insensitively. JSON reports hash, prior role and new role. |
| `build` | Uses only **training** evidence and validated caches; at least one is required. Writes a new immutable candidate in `revisions/<revision ID>`, updates registry `current_revision`/history and prints revision, bundle, model path/hash and summary. Default threshold is **0.72**; subsequent additive builds must keep the previous threshold. |
| `status` | Prints state root, learner identity, feature version, evidence/role totals, revision count/current revision and per-hash observations/cache counts. A missing registry gives an empty in-memory status while leaving disk state unchanged. |

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
# Example sync/build commands; replace the paths with your protected input and work folders.
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\sync.json' registry -- --state-root 'D:\CK3Work\registry' sync --runtime-root 'D:\Protected' --default-role training
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\build.json' registry -- --state-root 'D:\CK3Work\registry' build --threshold .72
# Illustrative inspection/role change; replace the hash with a status entry.
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' registry -- --state-root 'D:\CK3Work\registry' status
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' registry -- --state-root 'D:\CK3Work\registry' role '<input-sha256>' holdout
```

## Evaluate a candidate and export a model package

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
runtime package evaluation route, `ck3chronicle-model-release evaluate`. Candidate evaluation does not ingest a Run or alter SQLite.

`publish --bundle` validates compact export against the saved native candidate
evidence and writes `<output-dir>/<package ID>`. It prints package/revision IDs,
folder, manifest hash and a proposed selection. This is **local export**, not a
network upload, catalog registration or active selection. In particular the
printed `candidates/<ID>` selection path is a conventional suggestion, not proof
of the actual exported or installed location. Use the model catalog/selection
commands and setup for installation and active configuration.

The alternative `--source-release` route retains compatible published model
definitions with the chosen implementation and requires an external manifest
pin and at least one genuine validation log. It makes a new package with new
validation; it is not copying an old package or inheriting proof for changed
code. Unsupported historical formats are rejected. `--bundle` and
`--source-release` are mutually exclusive; pin/validation options apply only to
the source-release branch. Registration is the copy-existing-release route.

```powershell
# Example: evaluate and export a candidate using your protected input and work folders.
$candidate = 'D:\CK3Work\registry\revisions\d729dea94d84323b8497e882'
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\evaluate.json' evaluate -- --bundle $candidate --log 'D:\Protected\run-a\error.log' --output 'D:\CK3Work\evaluation.json'
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\export.json' publish -- --bundle $candidate --output-dir 'D:\CK3Work\packages'
# Alternative: substitute a compatible source and its exact pin.
& $python -I -B -m template_learning.learner_loader run --release $learner --receipt 'D:\CK3Work\repackage.json' publish -- --source-release 'D:\Releases\source-package' --expected-manifest-sha256 '<manifest-sha256>' --validation-log 'D:\Protected\run-a\error.log' --output-dir 'D:\CK3Work\packages'
```

## Inspect candidate evidence and specialized comparisons

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
authenticated candidate, not that sentence.

```powershell
# Examples: inspect candidate evidence using the paths prepared above.
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' review -- --bundle $candidate --output-dir 'D:\CK3Work\review'
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' visual-review -- --bundle $candidate --output 'D:\CK3Work\visual.json' --top 20 --examples 3
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' visual-review -- --bundle $candidate --output 'D:\CK3Work\diagnostics.json' --diagnostics --baseline 'D:\CK3Work\baseline' --previous-review 'D:\CK3Work\prior-review.json' --html 'D:\CK3Work\diagnostics.html'
& $python -I -B -m template_learning.learner_loader run --release $learner --log-dir 'D:\CK3Work\journals' compare -- --before 'D:\CK3Work\before' --after $candidate --output 'D:\CK3Work\comparison' --selection 'D:\CK3Work\selection.json'
```

## Create and register a Learner release

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
# Examples for a separate writable Learner catalog.
& $python -I -B -m template_learning.learner_loader create --source 'D:\Source\template_learning' --application-source 'D:\Source\ck3chronicle' --output 'D:\CK3Work\learner-releases' --log-dir 'D:\CK3Work\journals'
& $python -I -B -m template_learning.learner_loader register --root 'D:\CK3Work\learner-catalog' --source 'D:\CK3Work\learner-releases\<release-id>' --manifest-sha256 '<manifest-sha256>' --log-dir 'D:\CK3Work\journals'
```

Registration takes effect on the next catalog read or explicit invocation. It
does not change an already-running worker, build a new application wheel or select
a production model. Use a separate writable catalog for maintenance; installed
distribution resources remain immutable. Retention policy preserves at least the latest ten production Learner versions
and ten distinct production model revisions; this does not assert ten currently
available versions or authorize deleting older ones.

## Identities and JSON edit boundaries

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
configuration and reporting references. They cannot override Learner rules or
rewrite historical lineage. Use setup to select a model for future processing,
and public `run ... registry` for incremental Learner work.

## Additional installed inspection routes

Two existing module routes support advanced candidate inspection/evaluation.
Use the bundle's private interpreter from its extracted folder:

```powershell
.\runtime\python.exe -I -B -m template_learning.evidence_serialization --bundle 'D:\LearnerWork\candidate'
.\runtime\python.exe -I -B -m template_learning.evaluate_unseen_session --learner-release $learner --bundle 'D:\LearnerWork\candidate' --log 'D:\Protected\error.log' --output 'D:\LearnerWork\evaluation.json' --receipt 'D:\LearnerWork\execution.json'
```

`evidence_serialization` requires only `--bundle DIR`, authenticates saved data
hashes without executing that candidate's code, and prints manifest, model revision
and summary JSON. It changes no candidate/runtime state. Success exits 0, parser
errors 2, authentication/I/O failures nonzero.

`evaluate_unseen_session` requires `--learner-release ID`, `--bundle DIR`,
`--log PATH`, `--output PATH`; optional `--learner-root DIR` selects the installed
catalog alternative and `--receipt PATH` records execution. It delegates to the
same retained `evaluate` operation, including its outputs/identity constraints
and outer nonzero-exit behavior. Its name does not make a supplied training log
unseen evidence. It has no `--log-dir` flag; normal retained receipt/cwd journal
defaults apply.

Use the public retained-release entry points above for authenticated learning,
registry maintenance and publishing.

[Manual contents](README.md)
