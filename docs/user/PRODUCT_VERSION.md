# Product Version

[Manual contents](README.md) · [Next: Introduction](INTRODUCTION.md)

This manual covers **ck3chronicle 0.0.3 for Windows x64**.

Manual revised **12 October 2026**.

The Windows bundle includes the application, its Python runtime, search tools
and classification resources. Start with [Introduction](INTRODUCTION.md) to
understand what it does, or go to [Installation and launch](INSTALLATION.md) to
set it up.

## Which version means what?

| Identity | What it identifies |
|---|---|
| Application **0.0.3** | The program and its commands described by this manual. |
| Manual edition | A revision of the documentation, identified by the bundle manifest. Explanations and examples can improve while the application and classification model stay the same. |
| Windows bundle manifest | The exact application, tools and document files in your extracted bundle. Keep the manifest with those files. |
| Classification model and package | The model describes recurring message structures; its package includes the compatible components that recognize them in an incoming log. Each has its own exact identity, recorded with the stored result. |
| Learner release | The retained software used by maintainers to build and evaluate classification models. Ordinary Run capture and reporting use the supplied resources. |
| Data format | The structure understood by a reader of that data: SQLite and native review manifests use schema **3**, model data uses schema **6**, and captured playset JSON uses schema **1**. |

A catalog's publication order is a sequence within that catalog. The application
version identifies the program release. A package ID names a particular package;
its manifest hash checks the exact bytes. See
[templates and packages](ORIENTATION.md#templates-and-packages) for why this
matters when comparing Runs or changing models.

## Check your copy

Open `release-manifest.json` in the extracted application folder with a text
viewer. The `version` value inside `application` gives the installed application
version; for this manual it is `0.0.3`. The `manual_revision` field identifies
the documentation included in that bundle. Read `application.version` rather
than the separate runtime's version when identifying ck3chronicle.

`Verify.cmd`, run from the extracted folder, checks the bundled files against
`release-manifest.json`. For the download itself, compare its SHA-256 hash with
the separately supplied release hash before extracting it. The manifest check
establishes file correspondence; the source of the release hash establishes
which download you intended to obtain.

Each stored Run records the model and processing identities actually used for
it. Those identities remain attached to the Run when you install a newer
application or select another model for future processing.

## Supplied classification reference

The supplied model is ready for ordinary capture and reporting. These compact
identifiers are useful when checking a report's processing lineage or discussing
a particular result:

| Resource | Identity |
|---|---|
| Default model revision | `3bc531d578074e6a430c161e` |
| Default classification package | `2b12932103f3a3111a4e1880` |

For the manifest hash and available retained releases, use the documented
[model inspection workflow](WORKFLOWS.md#inspect-or-change-the-selected-model).
The [advanced reference](RELEASE_REFERENCE.md#identities-and-json-edit-boundaries)
explains the full set of identifiers and which files to preserve unchanged.

[Continue to Introduction](INTRODUCTION.md) · [Manual contents](README.md)
