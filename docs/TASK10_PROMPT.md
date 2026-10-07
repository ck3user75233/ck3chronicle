# Proposed Task 10 — Installable production copy and first-run setup

Prepared 2026-10-05 for owner review and assignment. **Not commissioned by saving
this draft.** Replaces the original cutover/retirement-manifest proposal and the
subsequent readiness-only recommendation; neither old deletion nor cutover scope
carries forward.

The owner requires configuration/package-selection setup and the ability for a
user to download CK3Chronicle cold and start using it. An installer is a possible
means. A separate doctor command is undecided. Recommended lead: **Pipeline**,
using its application-packaging/runtime-integration ownership. Watcher and Data
Intelligence receive affected startup/capture and reporting behavior; Learner
owns the supplied immutable parser/matcher/model packages.

## Outcome

A new user obtains an identified production distribution from the project,
installs or extracts it into a chosen supported location, supplies their paths,
accepts or chooses an available approved package, initializes storage, and can
start observation and obtain reports. No agent must reconstruct Nate's checkout,
edit selection JSON by hand, copy a development environment or train a model.

**Proposed initial delivery:** Windows, with an application-local runtime and
required dependencies, usable without separately installing Git or Python. Prefer
a versioned downloadable bundle with a setup launcher unless a conventional
installer materially improves that journey. Pipeline should recommend the exact
format and explain material limitations before committing to a packaging tool.
This is not a claim of arbitrary-OS support or unrestricted write access anywhere.

## Read and establish the baseline

Read root instructions, development guidance, current plan/status/handoff,
[team ownership](team-governance/README.md), and the configuration/storage parts
of [Owner Product Intent](OWNER_PRODUCT_INTENT.md) and
[Trusted Run specification](TRUSTED_RUN_SPEC.md). Current owner directions govern
conflicts, including the undecided separate doctor surface and synthetic-test rule.
Use the [release receipt](learner-next-release/PIPELINE_RECEIVING.md) and
[operational record](learner-next-release/PIPELINE_CUTOVER.md) for actual delivered
packaging and production identities. Do not read rejected handler designs.

Inspect `config.py`, `cli.py`, `doctor.py`, `runtime_logging.py`, the model catalog,
database initialization/public handler, watcher startup, reporting entry points,
`pyproject.toml` and `packaging/`. Reuse their owners and interfaces. Coordinate
logging/configuration seams with [09A](TASK09A_PROMPT.md); use the shared logging
owner and avoid a competing backend. Neither task depends on Trekker.

## Required deliverables

1. **Reproducible distribution.** Package the approved application, compatible
   runtime/dependencies, report assets and pinned executable model resources.
   Include or explicitly provision actual external dependencies such as ripgrep
   for source-content search. Record exact versions, hashes and required notices.
   Launch independently of the checkout, current directory and developer PATH.
   Account for read-only application files and separately writable user state.
   Inventory required uncommitted/untracked files: local delivery does not prove
   that a GitHub download contains them. Prepare a release artifact and exact
   publication inputs; do not assume the moving Git branch is a tested release.

2. **First-run configuration.** Provide a concise guided setup and repeatable
   explicit arguments/configuration for agent use. Implement the established
   exact `--config <path>` or fixed LocalAppData `ck3chronicle/paths.toml` entry;
   all consumers use the same central authority. Help/setup must work before a
   configuration exists. Accept explicit game, source, log and writable-data
   locations; explain required existing paths versus application-owned paths
   setup may create. No disk-wide root discovery or fallback. Resolve relative
   values consistently from the chosen configuration, not the caller's directory.
   Validate before creating the database. Persist its exact returned path. Rerun
   setup without replacing an existing database, captures, review or user choices.
   Watching must be configurable before a current error.log exists. Update
   configuration containment deliberately to support the installation layout.

3. **Usable package selection.** Show the selected package/version and available
   compatible approved choices; supply a working reviewed default. Reuse catalog
   authentication and compatibility checks, persist an explicit selection and
   explain when it takes effect. Preserve immutable artifacts, existing Run
   lineage and available rollback. Reuse coordinated process boundaries if a
   running installation needs a restart; changing a file is not proof that a
   process loaded it. Package selection does not reset or reprocess history.

4. **Start/use and validation.** Give the user a straightforward launcher or
   command for observation, stopping and reports after setup, with actionable
   errors for incomplete configuration or dependencies. Setup performs necessary
   validation. Decide whether a separate doctor adds useful ongoing diagnosis;
   it is not required merely because an older checklist named it. If retained,
   diagnosis is read-only and reuses validation rather than duplicating setup.
   Installation must not silently activate OS startup/services or touch CK3/mod
   sources. Document normal subsequent launch and preservation of user data when
   replacing application files; no automatic updater is required.

## Verification and handoff

**Owner direction, 2026-10-07:** physical outside-checkout installation and
execution verification deferred from Task 09 belongs here. See the
[recorded disposition](TASK09_OWNER_DECISIONS.md#external-installation-verification-deferred-to-task-10--2026-10-07).
Verify the actual Task 10 distribution in an authorized location physically outside
the repository, with isolated writable state and no checkout imports/resources.
Changing only the working directory is insufficient. This check was not performed
for the [Task 09 baseline](TASK09_RELEASE_BASELINE.md); do not report it as inherited
acceptance evidence. This direction adds no immediate Task 10 dispatch.

Exercise the actual produced artifact and setup in a fresh permitted location,
without ambient checkout modules or dependence on the development environment.
Use genuine CK3 inputs and explicit paths in isolated application storage. Check
setup, repeat setup, the selected package, ordinary ingestion through the public
handler and meaningful report contents; preserve evidence and missing-time Run
behavior. Receive affected Watcher/Reporting interfaces and reuse valid existing
classification/storage evidence. No new learning or full-corpus campaign.

Report the actual environment tested. A fresh directory on a developer machine
does not alone prove cold-machine installation. Identify remaining prerequisite,
platform or clean-machine evidence gaps. Creation or execution of **each synthetic
test** needs explicit owner approval for that specific test; do not fabricate
logs, timestamps, histories, failures or mock clients to complete verification.

Deliver the distribution/build recipe, brief user setup instructions and
`docs/TASK10_HANDOFF.md`: exact identities, commands, evidence, limitations and
outstanding owners. Separate locally prepared, received and published states.
No commit/push/publication, live service restart, production configuration or
database change, historical rebuild or deletion of unrelated work is authorized
by this draft. Public release and this owner's production upgrade remain explicit
subsequent actions.

## Advisory basis for the proposed download format

GitHub supports uploaded release assets alongside automatically generated source
archives; that permits a tested runnable bundle to be the ordinary user download.
See [GitHub releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).
Python documents an embeddable Windows distribution for application use, one
possible runtime-packaging route; its fit and third-party dependency distribution
must be established rather than copying the repository venv. See
[Python on Windows](https://docs.python.org/3/using/windows.html#the-embeddable-package).
Neither reference selects an installer technology or establishes CK3Chronicle
delivery/verification.
