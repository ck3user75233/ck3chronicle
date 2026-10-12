# Task 10B — Standalone Windows distribution

**Owner: Launch & Distribution.** Prepared for owner issuance.
**Trekker ID: TREK-10.** Owner-issued 2026-10-08. Follow the [common instructions](WORKING_AGREEMENT.md)
and [scope/index](../TASK10_DELIVERABLES.md).

## Outcome and inputs

### Owner clarification — Python/ripgrep verification, 2026-10-12

The Owner explicitly states: "we do not need to verify python and ripgrep, we
know those are working". Use the existing working, identified runtime/tool
payloads. Additional upstream correspondence verification and acquisition of
Python/ripgrep archives are **not Task 10 completion requirements**. This
supersedes earlier handoff/checkpoint instructions that made those downloads
and comparisons a prerequisite to final assembly. Do not request or attempt
GitHub access for this purpose; the Owner intentionally restricts that access.

Preserve the existing bytes and included notices. Continue normal bundle
inventory/hash recording and final installed-product acceptance; those establish
which local candidate was assembled and how it operates, not correspondence to
a remote copy. Do not replace dependencies or add another provenance campaign
to reintroduce the removed requirement. Incorporate the Owner-requested revised
manual and deliver the final identified bundle to 10C. Historical acquisition
failures remain evidence of those attempts, not current blockers.

Produce the runnable Windows distribution and guided setup/launch entry points
specified in [10A](10A_FIRST_USE_DESIGN.md), using the authenticated application
delivered by [10A.1](10A1_PIPELINE_INTERFACES.md). An ordinary user must not need
the developer checkout, Git, an existing Python environment or hand-edited model
selection JSON. A text-based guided setup is sufficient; no NiceGUI dashboard.

Refresh those producer records, latest handoffs and TREK-6 baseline before use.
Record actual receipt of Pipeline's interface/artifact on 10A.1, with exact pins
and limits. Preparation may use a received interface before Pipeline's whole
assignment closes. Do not demand completed status before consuming a usable delivery.

## Implement and verify

Own the outer distribution recipe, runtime/dependency bundling, setup and launch
scripts, versioned archive contents, licenses/notices and short installation guide.
Use a dedicated outer-distribution directory agreed with Pipeline; do not compete
for its wheel recipe, `pyproject.toml`, configuration validation or database owner.
The launcher collects user inputs and calls the technical interfaces; it must not
duplicate initialization, selection, validation or analysis logic.

Owner correction, 2026-10-08: use Pipeline's bounded Steam/Windows Known Folder
suggestions and meaningful validation. Display editable full paths and findings;
require a separate Yes/Accept for every external root, including automatically
found paths. Save the user's locations, with no assumed relationship to the bundle
or developer machine. Final Apply does not replace per-field acceptance. External
game/mod/log contents stay read-only; their configuration values are editable.
Expose the improved config doctor and explain its missing/suspicious findings.

Include or explicitly provision the required runtime and external dependencies
such as ripgrep. Use received immutable model resources/defaults. Record runtime,
application, model and dependency versions/hashes and meaningful human-readable
release labels. A wheel's unchanged version string alone is not an exact identity.
Include or link the corresponding 10D/10E manual; keep its version aligned.

Install/extract the actual distribution **physically outside the checkout** into
an authorized location with separate writable user state. Preflight that access
at assignment start. Verify setup/help, first and repeat setup, selected model,
launch/report commands, correct installed imports/resources and logs. Changing
cwd alone does not demonstrate relocation. Preserve existing user data and do not
silently register OS startup, restart production or change the owner's live config.

If permissions prevent external placement, report the exact required environment
early, retain it as an open 10B/10C obligation and continue build/docs work. Do not
report an in-checkout environment as equivalent. A developer-machine test must
state which preinstalled dependencies it could still rely on; 10C establishes the
stronger clean-environment claim where evidence is available.

## Delivery

As setup/distribution implementer, supply the technical reference drafts for the
entry points you own: installation requirements, setup inputs/defaults, launch/stop
commands, configuration selection, repeat-setup effects, outputs and error behavior.
Include real command/output examples from your authorized checks and useful actual
setup screenshots when applicable. Deliver these with the artifact for the Docs
role in 10D/10E to edit, verify and integrate. Keep them updated when your launcher
or bundle changes; do not make Docs rediscover your interface by experimentation.

Write `docs/task10/DISTRIBUTION_HANDOFF.md` with artifact location/hash, build recipe,
supported platform/dependencies, setup/start/stop commands, actual external-location
evidence, limitations and component repair requests. Deliver on this record to
[10C](10C_ACCEPTANCE.md); 10D/10E retrieve exact commands and layout from here.

Do not use a shared editor race to update bundled docs. Coordinate a final content
revision with 10D/10E, record their hashes, then deliver the final artifact.
Documentation verification uses an earlier usable installed candidate with settled
commands/layout; supply it before requiring the finished manual, avoiding a circular
wait. Authenticate the final bundle again after including the agreed documentation.
Code repairs return to Pipeline/component owners; outer-bundle repairs stay here.
10C records actual internal receipt on this same record and closes it once this
delivery's requirements are met. Subsequent acceptance-only work stays on 10C.

Before integrated acceptance, give the Owner a concise convergence brief: received
artifact/interfaces/docs, actual external-placement result, strongest evidence and
limits, remaining owner/action and any decision. No automatic publication, source
commit/tag/push, live switch or general installer/auto-updater expansion.
