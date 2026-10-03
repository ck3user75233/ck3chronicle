# Retained learner and model releases

Selecting a release selects retained executable bytes. Author learner changes in
`tools/template_learning/`; never edit a distribution under `learners/releases/`
or `models/releases/`. Changing the closure creates a new learner release ID.
Changing a model's executable combination creates a new package ID, even when
the model revision is unchanged.

## Storage and authentication

| Family | Catalog | Retained distribution | Installed location |
|---|---|---|---|
| Learner | `learners/catalog.json` | `learners/releases/<release_id>/` | `<sys.prefix>/share/ck3chronicle/learners/` |
| Production model | `models/catalog.json` | `models/releases/<package_id>/` | `<sys.prefix>/share/ck3chronicle/models/` |

A learner distribution contains `manifest.json`, `launcher.py`, and its own
`template_learning/` code, JSON rules, parser/manifest and review assets. It has
no executable links to another release. Catalogs pin the manifest SHA-256; the
manifest authenticates each retained payload. Learner IDs are SHA-256 of the
canonical manifest excluding `release_id`. The existing learner fingerprint is
also retained, separately from this distribution ID. Model packages keep their
existing package/model identities and existing bootstrap authentication.

Catalogs record family, retained path, identity, manifest pin, availability,
publication status and explicit production publication order. `partial` learner
rows expose only the operations their manifest supports. Unavailable historical
models remain listed with their missing dependencies. A version/API label is
descriptive; exact release/package identity selects executable code.

The catalogs and external manifest pins are the local trust anchors. Hashes
detect disagreement with them; they are not publisher signatures. Python 3.11+
and its standard library are platform prerequisites. No third-party Python
runtime dependencies are required by the retained operations. Execution receipts
record actual Python implementation/version and Unicode version. Verification
does not establish bitwise reproducibility across interpreters or operating systems.

## Learner selection

From the repository Python environment:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader list
```

Select the exact `release_id` from that catalog. For example, the Task 07C complete
release is `cdbd72475baf238d5a44a7ef37c2a266a71179d780dbaf71aa35d5a91b3d5a0f`.
The following examples use concrete user-supplied paths; output, state and
evaluation data must be outside release directories and outside Git.

```powershell
$releaseId = 'cdbd72475baf238d5a44a7ef37c2a266a71179d780dbaf71aa35d5a91b3d5a0f'
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader run --release $releaseId --receipt <execution.json> learn -- --log <error.log> --output-dir <candidate-output>
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader run --release $releaseId --receipt <sync.json> registry -- --state-root <state> sync --runtime-root <protected-input-root> --default-role training
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader run --release $releaseId --receipt <build.json> registry -- --state-root <state> build
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader run --release $releaseId --receipt <evaluation-execution.json> evaluate -- --bundle <candidate> --log <error.log> --output <evaluation.json>
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader run --release $releaseId --receipt <publication-execution.json> publish -- --bundle <candidate> --output-dir <package-output>
.\.venv\Scripts\python.exe -B -m template_learning.learner_loader run --release $releaseId --receipt <review-execution.json> review -- --bundle <candidate> --output-dir <review-output>
```

Replace angle-bracket placeholders; quote paths containing spaces. `run --root`
selects an alternate learner catalog. Installed applications expose the same
commands as `ck3chronicle-learner-release`. Use `--receipt` to retain execution
provenance alongside evaluation/publication results.

The launcher authenticates the selection, then starts its retained launcher with
`python -I -S -B`. Authenticated in-memory source supplies learner imports in the
child. Application imports and missing learner modules fail; neither installed
learner code nor the working checkout supplies a fallback. A candidate and
incremental registry must belong to the selected release. The parser must come
from that release. Explicit state/input paths avoid application configuration;
only the outer command resolves convenience defaults when those paths are omitted.

`evaluate_unseen_session` also requires `--learner-release` and delegates to this
launcher. Published models must instead use package evaluation below. Read-only
inspection of retained candidate data requires no executable learner selection:

```powershell
.\.venv\Scripts\python.exe -B -m template_learning.evidence_serialization --bundle <candidate>
```

The complete release also exposes `visual-review` and `compare`; pass `-- --help`
after the operation for its arguments. These are the existing specialized review
workflows, not arbitrary cross-version replay. Historical distributions currently
expose evaluation only. Do not run old creation/registry/publication code through
today's implementation or reinterpret an old candidate as belonging to a new release.

## Production package selection

```powershell
.\.venv\Scripts\python.exe -B -m ck3chronicle.pipeline.catalog list
.\.venv\Scripts\python.exe -B -m ck3chronicle.pipeline.catalog selection --package 44a0401b8adf0a2953d26705
.\.venv\Scripts\python.exe -B -m ck3chronicle.pipeline.catalog evaluate --package 44a0401b8adf0a2953d26705 --log <error.log> --output <evaluation.json>
.\.venv\Scripts\python.exe -B -m ck3chronicle.pipeline.catalog evaluate --package 68f1ae5db205ab46afef9c4d --log <error.log> --output <evaluation.json>
```

Installed command: `ck3chronicle-model-release`. Optional `--models-root` precedes
the subcommand. `selection` prints a schema-2 selection; it never edits the active
default. `evaluate` uses the real classifier and Error Contract preparation without
ingestion or database writes. Receipts include actual package/model/parser lineage,
input hash, application source fingerprint, environment, statuses and prepared records.

Pipeline callers use:

```python
from ck3chronicle.pipeline.catalog import load_selected_classifier
classifier = load_selected_classifier(package_id="44a0401b8adf0a2953d26705")
```

`load_selected_package` accepts the same `package_id`. Existing `selection_path`
is an alternative and cannot be combined with `package_id`. Omitting both retains
the current default. Model revision alone never implicitly chooses among multiple
packages. Run lineage must come from the loaded package through
`contracts.run_lineage(package, application_revision=...)`.

## Creating and registering releases

Use `learner_loader create --source tools/template_learning --output <release-root>`
to snapshot the declared closure, then `register --source <snapshot-directory>
--manifest-sha256 <pin> --root <learner-root>`. `pipeline.catalog register --source
<package-directory> --manifest-sha256 <pin>` authenticates and copies an already
built package. Neither registration requires learning or activation. Registration
without production metadata is research; production registration requires both
`--production-order <integer>` and `--publication-evidence <reference>`. Existing
publication order cannot be changed by activation or registration. Catalog review
annotations and historical incomplete entries are inventory maintained by the owner.

Update `pyproject.toml` data-file entries when adding retained distributions, then
verify the installed resources. Registration alone does not add a new distribution
to an already-built wheel. Keep `.gitattributes` byte-preserving release rules.

Repackaging existing schema-5 model definitions against another implementation
requires an explicit learner release and `publish -- --source-release <source>
--expected-manifest-sha256 <pin> --validation-log <native-log> --output-dir <output>`.
Repeat `--validation-log` as needed. This creates a new package and fresh validation
of the target combination; inherited validation is not proof for new code. Copying
an existing package uses registration instead. Older incompatible model formats
are rejected rather than adapted with today's matcher.

## Retention policy

Retain at least the latest **10 production learner versions** and latest **10
distinct production model revisions**, with complete executable distributions.
Track production publication order explicitly. Multiple runtime packages of one
model do not count as multiple model revisions. Research candidates, creation
timestamps, filesystem order, hashes and repeated activation do not define order.

Ten is a future minimum, not a maximum or a claim about current availability.
Keep older releases until separately directed. This change implements no pruning,
retirement, deletion command, preview or release-use lock. Historical publication
order that is not established remains unknown. Logs, databases, learner state and
generated evaluations stay outside executable release storage and Git. Task 07's
one-month captured-log policy is independent of release retention.

See [Task 07C handoff](TASK07C_SELF_CONTAINED_RELEASES_HANDOFF.md) for exact inventory,
verification evidence and named historical gaps.
