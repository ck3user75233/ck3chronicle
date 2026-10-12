# Advisory local source-and-package checkpoint review — 2026-10-13

**Recommendation: preserve all 91 initial main-checkout changes, the four prepared
C11 package files, this review, and two proposed Git policy edits in one coherent
98-path source-and-package checkpoint.** Include the actual ZIP as a normal Git
blob. No main-checkout change needs exclusion or a separate inclusion decision.
The root README needs the small current-version correction shown below.

**Execution state: prepared only. Nothing staged, committed, fetched, pulled or
pushed.** `.gitignore`, `.gitattributes` and the existing README are unchanged;
their exact proposed patch is saved for later execution. Task 10 acceptance is
still open. The Owner's [issued assignment](task10-deliverables/ADVISORY_LOCAL_CHECKPOINT_AND_INSTALL_PACKAGE_REVIEW_20261013.md)
explicitly reserves staging/commit/publication decisions until this review exists.

## Local observations and scope

- Checkout: `C:\Users\nateb\Documents\ck3chronicle`; branch `main`.
- HEAD and cached `origin/main`: `709ea7842a0202c420b43355b18be91d8ca196a3`.
  Local comparison is **0 ahead / 0 behind**, not a live remote observation.
  `git log --branches --not --remotes` is empty: neither local branch has a
  commit absent from cached remote history. The Task09 tag object is
  `31dcb4428470331d453f71ccc1fad0c6e5d10001`.
- Configured origin: `https://github.com/ck3user75233/ck3chronicle.git`;
  no separate push URL. No remote operation was needed or performed.
- Initial inventory: **22 modified tracked + 69 untracked = 91 files**, totaling
  **1,782,504 working-tree bytes**. Staged inventory empty; no main-checkout
  deletions, renames, conflict entries, gitlinks or `.gitmodules`.
  Initial tracked diff: 851 additions / 157 removals. The PNG is the only
  binary among these initial changed paths. All were read/scanned as content,
  with detailed source/diff review, document authority/version review and image inspection.
  This is a checkpoint inclusion review, not new whole-product acceptance.
- One additional linked worktree exists under ignored `.codex-tmp/`, discussed
  separately below. Its branch is an ancestor in cached main history; its dirty
  contents are not the current application. App-owned `refs/codex/turn-diffs/*`
  are local snapshots, not publication targets.
- Protected `team-state advisory` and `task-list` succeeded against the canonical
  store: 16 records, no active/incoming/outgoing Advisory record and no recovery
  marker. No Advisory ID was assigned, so this report is the checkpoint; no
  duplicate producer record or unrelated tracker write was created.
  Actual TREK-9/10/11/12/15/16 records, including later comments, were retrieved.
  TREK-10 CMT-193/194/197 and TREK-11 CMT-195/198 confirm C11/r4 delivery and
  local receipt. TREK-16 CMT-196/199 retains actual environment/console work.
  TREK-12 CMT-168 defers ingestion redesign; this is not a missing Task 10 feature.

The initial inventory, full staged/unstaged inspection, sizes, SHA-256 hashes,
configuration origins, refs and subsequent evidence are saved under
[the ignored review directory](../.codex-tmp/advisory-checkpoint-20261013/).
No runtime/experimental archive was swept or hashed. Existing source, model and
Learner bytes were not regenerated, restored or normalized.

Protocol disclosure: the very first `git status --short`, issued alongside the
assignment read, omitted `--no-optional-locks`. It could refresh index stat-cache
metadata; no earlier index hash exists to disprove that. All subsequent Git
inspection used `--no-optional-locks` and disabled external diff/textconv helpers.
The saved post-read index hash is checked unchanged at finalization. No Git write
was used to test access. An initial inventory printer failed with a Windows
`UnicodeEncodeError`; its JSON encoding was corrected before saving evidence.
Neither event staged content or changed product files. No inspection command
was denied.

## Complete main-checkout disposition inventory

Every initial changed path appears once below. “Include” means include its current
unfinished-but-legitimate source/documentation state; it does not certify release
acceptance. Historical requests, received contributions and cleanup proposals
remain useful source history. Current Task 10 receiving and later Owner decisions
supersede their dated progress prose. Local path references in technical handoffs
are context, not a reason to export their private evidence targets.

### Application, catalog metadata and requirement checks

| State | Exact path | Bytes | Disposition and reason |
|---|---|---:|---|
| Modified | `packaging/learners/catalog.json` | 10,276 | Include. Order-10 production adoption metadata; retained IDs, pins and bytes unchanged. |
| Modified | `packaging/models/catalog.json` | 11,450 | Include. Order-9 production adoption metadata; retained IDs, pins and bytes unchanged. |
| Modified | `pyproject.toml` | 60,148 | Include. Application version 0.0.3; other packaging declarations unchanged. |
| Modified | `src/ck3chronicle/__init__.py` | 62 | Include. Application version 0.0.3. |
| Modified | `src/ck3chronicle/cli.py` | 32,070 | Include. Setup/doctor/configuration, explicit runtime stop and saved-model help. |
| Modified | `src/ck3chronicle/config.py` | 7,505 | Include. Explicit configuration authority and validated lazy roots for installed use. |
| Modified | `src/ck3chronicle/doctor.py` | 720 | Include. Read-only diagnosis through the central setup owner. |
| Modified | `src/ck3chronicle/pipeline/catalog.py` | 13,902 | Include. Runtime classifier honors authenticated configured model pin. |
| Modified | `src/ck3chronicle/pipeline/database_handler.py` | 19,341 | Include. Received runtime/config identity admission and 1,024-result cache. |
| Modified | `src/ck3chronicle/pipeline/repository.py` | 22,167 | Include. Discloses exact partial database-creation path for setup recovery. |
| Modified | `src/ck3chronicle/pipeline/request_handler.py` | 9,050 | Include. Configuration propagation, existing-handler probe and identity agreement. |
| Modified | `tests/test_database_handler_hardening_requirements.py` | 9,128 | Include. Existing expectations updated to 1,024/1,026; not run as reporting acceptance. |
| Untracked | `src/ck3chronicle/pipeline/runtime_identity.py` | 1,019 | Include. Required application/configuration identity implementation. |
| Untracked | `src/ck3chronicle/setup.py` | 22,188 | Include. Central setup validation, preview/apply, model selection and state preservation. |

### Protected coordination tooling and regression fixture

| State | Exact path | Bytes | Disposition and reason |
|---|---|---:|---|
| Modified | `tools/work_state/pilot.mjs` | 22,762 | Include. Protected helper imports the received strict decoder adapter. |
| Untracked | `tests/work_state/fixtures/cmt-132.json` | 20,811 | Include. Bounded genuine decoder regression fixture, including prose/history; no live DB or credentials. |
| Untracked | `tests/work_state/toon_output.test.mjs` | 1,264 | Include. Four offline genuine-record decoder regressions; local pinned dependency required. |
| Untracked | `tools/work_state/toon_output.mjs` | 656 | Include. Required strict TOON decoder repair; not generated store state. |

### Windows distribution sources

| State | Exact path | Bytes | Disposition and reason |
|---|---|---:|---|
| Untracked | `packaging/windows/Fetch-UpstreamInputs.ps1` | 5,083 | Include. Retain historical acquisition source; do not run or revive removed download gate. |
| Untracked | `packaging/windows/INSTALL.md` | 1,571 | Include. Included r4 installation entry. |
| Untracked | `packaging/windows/Place-And-Verify.ps1` | 8,120 | Include. Source for separately invoked external placement/acceptance helper; needs TRANSFER.json. |
| Untracked | `packaging/windows/README.md` | 3,389 | Include. Build/maintainer instructions and explicit removal of upstream comparison gate. |
| Untracked | `packaging/windows/RELEASE_NOTES.md` | 1,723 | Include. Included r4 application/manual release notes. |
| Untracked | `packaging/windows/Setup.ps1` | 24,925 | Include. Native Windows Forms setup presentation, checks and final save. |
| Untracked | `packaging/windows/THIRD_PARTY_NOTICES.md` | 864 | Include. Included C11 notice index; existing notice bytes preserved. |
| Untracked | `packaging/windows/build.py` | 8,397 | Include. Offline distribution recipe; original plan and wheel files remain ignored inputs. |
| Untracked | `packaging/windows/external_check.py` | 7,638 | Include. Explicit installed acceptance helper; starts handler and may ingest if supplied a capture. Not run here. |
| Untracked | `packaging/windows/launcher.py` | 14,133 | Include. Bundle entry points and text setup presentation. |
| Untracked | `packaging/windows/ripgrep-LICENSE-MIT.txt` | 1,079 | Include. Required retained tool license text. |
| Untracked | `packaging/windows/setup_gui_backend.py` | 2,278 | Include. JSON bridge to Pipeline-owned setup APIs. |
| Untracked | `packaging/windows/upstream-inputs.json` | 1,739 | Include. Retain matching historical acquisition pins; no current download requirement. |

### Canonical user manual and image

| State | Exact path | Bytes | Disposition and reason |
|---|---|---:|---|
| Untracked | `docs/user/CLI_REFERENCE.md` | 20,387 | Include. Canonical r4 manual: CLI reference; exact C11 bytes authenticated. |
| Untracked | `docs/user/CONFIGURATION_REFERENCE.md` | 12,550 | Include. Canonical r4 manual: Configuration reference; exact C11 bytes authenticated. |
| Untracked | `docs/user/DISTRIBUTION_REFERENCE.md` | 2,211 | Include. Canonical r4 manual: Windows launcher reference; exact C11 bytes authenticated. |
| Untracked | `docs/user/EXTERNAL_DATA.md` | 16,710 | Include. Canonical r4 manual: Read stored data with SQLite; exact C11 bytes authenticated. |
| Untracked | `docs/user/INSTALLATION.md` | 8,358 | Include. Canonical r4 manual: Installation and launch; exact C11 bytes authenticated. |
| Untracked | `docs/user/INTRODUCTION.md` | 8,871 | Include. Canonical r4 manual: Introduction; exact C11 bytes authenticated. |
| Untracked | `docs/user/ORIENTATION.md` | 14,023 | Include. Canonical r4 manual: Orientation to ck3chronicle; exact C11 bytes authenticated. |
| Untracked | `docs/user/PIPELINE_REFERENCE.md` | 3,588 | Include. Canonical r4 manual: Python application interfaces; exact C11 bytes authenticated. |
| Untracked | `docs/user/PLANNED_FEATURES.md` | 1,706 | Include. Canonical r4 manual: Planned Features; exact C11 bytes authenticated. |
| Untracked | `docs/user/PRODUCT_VERSION.md` | 3,659 | Include. Canonical r4 manual: Product Version; exact C11 bytes authenticated. |
| Untracked | `docs/user/README.md` | 4,202 | Include. Canonical r4 manual: ck3chronicle user manual; exact C11 bytes authenticated. |
| Untracked | `docs/user/RELEASE_REFERENCE.md` | 26,514 | Include. Canonical r4 manual: Model and Learner administration; exact C11 bytes authenticated. |
| Untracked | `docs/user/REPORT_QUERY_REFERENCE.md` | 14,458 | Include. Canonical r4 manual: Report queries and results; exact C11 bytes authenticated. |
| Untracked | `docs/user/TROUBLESHOOTING.md` | 5,005 | Include. Canonical r4 manual: Troubleshooting; exact C11 bytes authenticated. |
| Untracked | `docs/user/WORKFLOWS.md` | 14,563 | Include. Canonical r4 manual: Everyday workflows; exact C11 bytes authenticated. |
| Untracked | `docs/user/images/setup-folders-c9-crop.png` | 19,514 | Include. 19,514-byte genuine cropped UI illustration; visually inspected, no private username/path visible. |

### Assignments and issued continuations

| State | Exact path | Bytes | Disposition and reason |
|---|---|---:|---|
| Untracked | `docs/task10-deliverables/10A1_PIPELINE_INTERFACES.md` | 7,165 | Include. Owner assignment/coordination source: Task 10A.1 — Application interfaces and artifact; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/10A_FIRST_USE_DESIGN.md` | 4,363 | Include. Owner assignment/coordination source: Task 10A — First-use design; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/10B_DISTRIBUTION.md` | 6,404 | Include. Owner assignment/coordination source: Task 10B — Standalone Windows distribution; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/10C_ACCEPTANCE.md` | 7,528 | Include. Owner assignment/coordination source: Task 10C — Integrated installation acceptance; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/10D_PRODUCT_REFERENCE.md` | 8,144 | Include. Owner assignment/coordination source: Task 10D — Product reference; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/10E_USER_WORKFLOWS.md` | 5,470 | Include. Owner assignment/coordination source: Task 10E — User workflows and external data access; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/ADVISORY_LOCAL_CHECKPOINT_AND_INSTALL_PACKAGE_REVIEW_20261013.md` | 10,490 | Include. Current Owner assignment, including Git-tracked ZIP and initial-review limits. |
| Untracked | `docs/task10-deliverables/COMPONENT_DOCUMENTATION_INPUT.md` | 4,334 | Include. Owner assignment/coordination source: Task 10D — Component documentation contribution; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/LD_RESUME_AFTER_DEPENDENCY_VERIFICATION_REMOVAL.md` | 6,541 | Include. Owner assignment/coordination source: Launch & Distribution — resume work after removal of dependency verification; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/MANUAL_01_PRODUCT_INTRODUCTION_AND_ORIENTATION.md` | 11,182 | Include. Owner assignment/coordination source: Launch & Distribution — manual introduction and product orientation; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/MANUAL_02_STRUCTURE_AND_EDITORIAL_REVIEW.md` | 18,981 | Include. Owner assignment/coordination source: Launch & Distribution — complete manual structure and editorial review; execution requires its actual issuance. |
| Untracked | `docs/task10-deliverables/SOURCE_CHECKPOINT_PUBLICATION_20261011.md` | 10,465 | Include. Historical prompt with explicit supersession banner; not present publication authority. |
| Untracked | `docs/task10-deliverables/WORKING_AGREEMENT.md` | 7,864 | Include. Owner assignment/coordination source: Task 10 — Common execution and Trekker instructions; execution requires its actual issuance. |

### Project, component, Advisory and cleanup records

| State | Exact path | Bytes | Disposition and reason |
|---|---|---:|---|
| Modified | `README.md` | 24,155 | Include. Product entry, commands and config transition; apply the proposed C11 pointer correction before checkpoint. |
| Modified | `docs/CURRENT_HANDOFF.md` | 397,272 | Include. Task 10 continuation, original delivery history, decoder recovery and completed Learner reclamation. |
| Modified | `docs/PROJECT_PLAN.md` | 60,843 | Include. Milestone/dependency history and current C11 receiving boundary. |
| Modified | `docs/PROJECT_STATUS.md` | 95,005 | Include. Current C11 status, historical evidence and operational restrictions. |
| Modified | `docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md` | 24,528 | Include. Public 1,024-completed-operation cache contract and historical verification boundaries. |
| Modified | `docs/TASK07_SCOPE_REVIEW.md` | 20,113 | Include. Aligns the active handler contract to the approved 1,024 bound. |
| Modified | `docs/TASK10_PROMPT.md` | 9,190 | Include. Marks older Task 10 proposal subordinate to issued split and corrected setup requirements. |
| Modified | `docs/TREKKER_CLI_PILOT_HANDOFF.md` | 17,465 | Include. Required decoder module, recovery receipt and protected-store continuity. |
| Modified | `docs/team-governance/README.md` | 8,548 | Include. Owner-approved application/distribution/manual responsibilities. |
| Untracked | `docs/LEARNER_RECLAMATION_RECEIPT_20261009.md` | 11,013 | Include. Completed authorized cleanup record; does not include retired research payloads. |
| Untracked | `docs/LEARNER_RESEARCH_RETENTION_PROPOSAL.md` | 5,668 | Include. Explicitly unadopted policy proposal; preserve without activating it. |
| Untracked | `docs/LEARNER_STORAGE_MAP_20261009.md` | 45,822 | Include. Documented historical storage/version map, explicitly marked pre-cleanup. |
| Untracked | `docs/LEARNER_URGENT_SPACE_RECLAMATION_PROMPT.md` | 6,686 | Include. Original bounded cleanup assignment; receipt establishes subsequent execution. |
| Untracked | `docs/TASK10_ADVISORY_REVIEW_PROMPT.md` | 14,492 | Include. Project documentation: Advisory — Establish Task 10 status, production health and release integrity; dated claims retain their original scope. |
| Untracked | `docs/TASK10_DELIVERABLES.md` | 14,081 | Include. Project documentation: Task 10 — Setup, distribution and product documentation; dated claims retain their original scope. |
| Untracked | `docs/TASK10_HANDOFF.md` | 37,145 | Include. Project documentation: Current Task 10 receiving: combined C11 / manual r4 — 2026-10-12; dated claims retain their original scope. |
| Untracked | `docs/TREKKER_CMT132_RECOVERY.md` | 5,512 | Include. Technical recovery/decoder diagnosis; source continuity without exporting canonical store. |
| Untracked | `docs/task10/ADVISORY_COMPLETION_BLOCKERS_20261012.md` | 11,239 | Include. Project documentation: Task 10: why completion is stalled; dated claims retain their original scope. |
| Untracked | `docs/task10/ADVISORY_STATUS_AND_INTEGRITY_REVIEW.md` | 45,589 | Include. Project documentation: Advisory — Task 10 status, production health and release integrity; dated claims retain their original scope. |
| Untracked | `docs/task10/DATA_INTELLIGENCE_CONTRIBUTION.md` | 30,115 | Include. Project documentation: Task 10D — Data Intelligence documentation contribution; dated claims retain their original scope. |
| Untracked | `docs/task10/DISTRIBUTION_HANDOFF.md` | 50,947 | Include. Project documentation: Current distribution: C11 assembled and locally received — 2026-10-12; dated claims retain their original scope. |
| Untracked | `docs/task10/DOCUMENTATION_HANDOFF.md` | 44,150 | Include. Project documentation: Manual r4 included and locally received in C11 — 2026-10-12; dated claims retain their original scope. |
| Untracked | `docs/task10/FIRST_USE_DESIGN.md` | 31,579 | Include. Project documentation: Task 10A — First-use design; dated claims retain their original scope. |
| Untracked | `docs/task10/INTERFACE_INVENTORY.md` | 17,144 | Include. Project documentation: Entry-point classification inventory; dated claims retain their original scope. |
| Untracked | `docs/task10/LEARNER_DOCUMENTATION_HANDOFF.md` | 30,520 | Include. Project documentation: Task 10D — Learner documentation contribution; dated claims retain their original scope. |
| Untracked | `docs/task10/MANUAL_01_HANDOFF.md` | 15,631 | Include. Project documentation: Manual Part 1 — product introduction and orientation; dated claims retain their original scope. |
| Untracked | `docs/task10/OWNER_STATUS_AND_TESTING_20261011.md` | 13,060 | Include. Project documentation: Task 10: remaining work and testing the available package; dated claims retain their original scope. |
| Untracked | `docs/task10/PIPELINE_HANDOFF.md` | 18,095 | Include. Project documentation: Task 10A.1 — Pipeline interface and application delivery; dated claims retain their original scope. |
| Untracked | `docs/task10/REQUEST_RESULT_CACHE_HANDOFF.md` | 5,808 | Include. Project documentation: Pipeline completed-result cache — next application candidate; dated claims retain their original scope. |
| Untracked | `docs/task10/WATCHER_DOCUMENTATION_HANDOFF.md` | 24,575 | Include. Project documentation: Task 10D — Watcher documentation contribution; dated claims retain their original scope. |
| Untracked | `docs/task10/WORKFLOWS_HANDOFF.md` | 15,806 | Include. Project documentation: Task 10E — Workflow and external-data delivery; dated claims retain their original scope. |


### Prepared additions and proposed policy changes

| Exact path | State / disposition |
|---|---|
| `release-candidates/task10/candidate11/ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip` | Prepared, still ignored by current `*.zip`; include after exact exception. 20,980,042 bytes. |
| `release-candidates/task10/candidate11/release-manifest.json` | Prepared unchanged copy; include with exact `-text` attribute. 469,387 bytes. |
| `release-candidates/task10/candidate11/SHA256SUMS` | Prepared; include ZIP and original-manifest checksums. |
| `release-candidates/task10/candidate11/README.md` | Prepared; include identity, setup/start instructions and acceptance/privacy limits. |
| `docs/ADVISORY_LOCAL_CHECKPOINT_REVIEW_20261013.md` | Prepared; include this complete disposition and execution plan. |
| `.gitignore` | Proposed only; include one selected-archive exception. |
| `.gitattributes` | Proposed only; include two exact byte-preservation entries. Existing immutable rules unchanged. |

### Separate old worktree: retain, do not merge into this checkpoint

`codex/pipeline-inspection` at `1af79a4e29b673f2b93eb250b71179c4639af435`
is rooted at `.codex-tmp/pipeline-inspection`. It has four modified tracked and
three untracked files (111,593 bytes). A read-only status/diff/hash snapshot is
saved in `legacy-worktree.json`. Its partial Task03 inspection code predates the
current pipeline; copying it onto main would overwrite newer owning behavior.
These are ignored-area development remnants, not needed C11 transfer inputs.
Preserve them locally, without cleanup or implicit integration. If that abandoned
inspection is wanted on the next machine, first perform a separately bounded
worktree/source review; a main-branch clone will not carry these uncommitted bytes.

| Exact path | Bytes | Disposition |
|---|---:|---|
| `.codex-tmp/pipeline-inspection/AGENTS.md` | 1,916 | Hold outside main checkpoint; preserve old-worktree bytes. |
| `.codex-tmp/pipeline-inspection/src/ck3chronicle/pipeline/bindings.py` | 10,104 | Hold outside main checkpoint; preserve old-worktree bytes. |
| `.codex-tmp/pipeline-inspection/src/ck3chronicle/pipeline/classifier.py` | 10,499 | Hold outside main checkpoint; preserve old-worktree bytes. |
| `.codex-tmp/pipeline-inspection/src/ck3chronicle/pipeline/normalization.py` | 39,525 | Hold outside main checkpoint; preserve old-worktree bytes. |
| `.codex-tmp/pipeline-inspection/docs/PIPELINE_INSPECTION_PLAN.md` | 16,415 | Hold outside main checkpoint; preserve old-worktree bytes. |
| `.codex-tmp/pipeline-inspection/tests/test_pipeline_inspection.py` | 18,028 | Hold outside main checkpoint; preserve old-worktree bytes. |
| `.codex-tmp/pipeline-inspection/tools/inspect_pipeline.py` | 15,106 | Hold outside main checkpoint; preserve old-worktree bytes. |

## Ignore and byte-preservation proposal

The only effective project exclusions are the repository `.gitignore` rules.
`.git/info/exclude` contains comments only. Git configuration sets no
`core.excludesFile`; `XDG_CONFIG_HOME` is absent and the default
`C:\Users\nateb\.config\git\ignore` does not exist. System Git has LFS filter
definitions, but no path under this proposal has a `filter=lfs` attribute.
No LFS installation, pointer conversion, global configuration or hosting change
is recommended. The selected ZIP is about 20.01 MiB, and one explicit retained
binary is suitable for the requested ordinary-Git checkpoint; this is not a
claim about unqueried server-side limits.

Observed `git check-ignore -v --no-index` results:

| Paths / class | Actual rule | Recommendation |
|---|---|---|
| Selected controlled C11 ZIP | `.gitignore:67:*.zip` | Add the single anchored exception below. |
| Original C11 ZIP, build plans, wheels, private receipts, review directory, old worktree | `.gitignore:24:.codex-tmp/` | Keep ignored. Copy only the selected ZIP/manifest into the controlled folder. |
| Canonical Trekker DB/toolchain and application local evidence | `.gitignore:35:.ck3chronicle/` | Keep ignored; preserve locally, including complete canonical work-state directory. |
| Root `config.toml` | `.gitignore:34:config.toml` | Keep ignored; machine-specific roots/database/model selection. |
| `.venv/pyvenv.cfg` and environment | `.gitignore:5:.venv/` | Keep ignored; prepare a workstation-local development environment. |
| Five already tracked `models/releases/*/empirical_template_model.json` files | `.gitignore:71:/models/**/empirical_template_model.json` | Keep tracked and byte-preserved; ignore matching does not remove index entries. |

Those five retained model IDs are `2b12932103f3a3111a4e1880`,
`44a0401b8adf0a2953d26705`, `4ac4e8ee92346e6d14eacfbf`,
`68f1ae5db205ab46afef9c4d` and `f23424ed8aa4d910bf4d3223`.
They are unchanged. No `git rm --cached` or other index removal is proposed.
Existing `/models/** -text` and `/learners/releases/** -text` remain intact.
Unrelated ZIPs, logs, SQLite files, pending/review evidence and caches retain
their current exclusions. No newly visible generated/private main-checkout file
needs another ignore rule. The tiny genuine Trekker fixture is deliberate test
source, not an export of the canonical store.

Exact proposed patch, including the stale root README correction (not applied):

```diff
--- a/.gitignore
+++ b/.gitignore
@@ -65,6 +65,8 @@

 # Local archives
 *.zip
+# One Owner-selected complete install candidate for source/workstation transfer
+!/release-candidates/task10/candidate11/ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip

 # Generated learned-model data stays local until selected for publication.
 # Keep versioned processing code, resources, manifests and pins visible.
--- a/.gitattributes
+++ b/.gitattributes
@@ -3,3 +3,7 @@
 # Immutable distributions are authenticated as bytes, including original newlines.
 /learners/releases/** -text
 /models/** -text
+
+# Preserve the received candidate archive and its authenticated manifest bytes.
+/release-candidates/task10/candidate11/ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip -text
+/release-candidates/task10/candidate11/release-manifest.json -text
--- a/README.md
+++ b/README.md
@@ -8,7 +8,9 @@
 For the installed Windows candidate, start with the [user manual](docs/user/README.md),
 [practical workflows](docs/user/WORKFLOWS.md) and
 [external SQLite access](docs/user/EXTERNAL_DATA.md). These describe application
-0.0.2/candidate 9; final distribution acceptance remains pending.
+0.0.3/candidate 11; final distribution acceptance remains pending.
+The complete proposed install ZIP is preserved in
+[the candidate checkpoint](release-candidates/task10/candidate11/README.md).

 The first product milestone is **Trusted Run**: observe one CK3 start-to-exit
 lifecycle, protect its live `error.log`, process it into SQLite, preserve
@@ -85,7 +87,7 @@
 separate. Consult
 [project status](docs/PROJECT_STATUS.md) before operational work.

-Application 0.0.2 uses an exact global `--config <path>` or the fixed
+Application 0.0.3 uses an exact global `--config <path>` or the fixed
 LocalAppData `ck3chronicle/paths.toml` bootstrap. Existing checkout users must
 pass their repository configuration explicitly; there is no current-directory
 fallback. See the [configuration reference](docs/user/CONFIGURATION_REFERENCE.md).
```

The received standalone manifest has **4,331 CRLF line endings**. Current
`* text=auto eol=lf` would normalize it, breaking its authenticated hash.
The exact `-text` entry prevents that. ZIP bytes are already binary-detected;
the second explicit rule makes that intended preservation durable. Other source
text will keep normal LF Git behavior; raw source hashes in older private
receipts can differ after a fresh checkout. The immutable ZIP and retained
resources remain the exact historical identities, not regenerated source pins.

## Selected package, private-state inspection and acceptance

Prepared location: [candidate11](../release-candidates/task10/candidate11/README.md).
Source receipt and current delivery records agree on the following identities:

| Artifact | SHA-256 / identity |
|---|---|
| ZIP, 20,980,042 bytes | `97f52263beca3387390d220d33ea461d6e60edaca7e70314096f473566750771` |
| Original release manifest, 469,387 bytes | `7d820a624be69a96a182cf609b73cc6ef7fcbde3c110c78ab2be823807bf4af7` |
| Application 0.0.3 wheel | `f03afb5b6abb5d7ee42522d832089d16d20a259374a987ae88dcb0f1a523ee38` |
| Manual r4 input manifest, 18 documents/assets | `b58a48f4159368b01a2e742a0e2f33b7740c74a850273a602b5ac24fa3a240d2` |
| Default model | `2b12932103f3a3111a4e1880`; manifest `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505` |
| Retained Learner | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`; manifest `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e` |

The ZIP and manifest were copied into a newly created folder using exclusive file
creation. Original and destination hashes match; neither received source was
moved or overwritten. No bulk extraction or duplicate installed tree was added.
The manifest is copied unchanged, including its truthful build-time “uncommitted”
source baseline. The new README is a separate publication summary. C9/C10 and
the standalone wheel are not substituted for C11.

Fresh Advisory checks found exactly **1,507 unique safe ZIP member paths**:
1,506 payloads plus the manifest, with no missing/unlisted members or hash
mismatches. There are 1,475 runtime files, 16 manual files/assets, one ripgrep
executable, one separate notice file and 14 root files including the manifest.
The root supplies seven CMD launchers, GUI/backend/launcher code, INSTALL,
RELEASE_NOTES, notice index and the manifest. Existing Python/chardet/ripgrep
license payloads remain present. No upstream comparison/download was performed.

No runtime SQLite files, captured logs, `config.toml`/`paths.toml`, Trekker store,
Git metadata or bytecode/cache files appear in the archive inventory. Credential
pattern scans of changed text and archive text found no matching private keys
or token patterns; this is a bounded inspection, not a security certification.
**22 archive text members retain local-path references**: five model payloads,
five model owner-rule files, eight retained Learner owner-rule files, the active
Learner owner-rule file, two Learner inspection utilities and application METADATA. These correspond to existing
retained provenance/tooling or the packaged developer README, not captured user
state. They are disclosed rather than silently sanitized. The assignment
explicitly preserves retained immutable bytes. The source docs and genuine
decoder fixture also contain historical local paths/record identifiers. The PNG
is a cropped setup illustration showing only ordinary Steam installation paths.

Original C11 receiving checked 157 manual links, application/dependency wheel
members and installed help/private imports/resources, preserving prior genuine
C9 workflow evidence where bytes correspond. This Advisory review reuses that
component evidence and independently verified source/archive correspondence for
**64 files**: every current `src/ck3chronicle/*.py` recursively, all 16 manual
files/assets, and six root packaging/notice files. No differences were found.
Catalog semantic comparison found only the already-approved production status,
order and evidence fields (model order 9, Learner order 10), plus Learner catalog
pretty-printing. No retained model hash or selection changed.

**Remaining acceptance is precisely TREK-16:** actual C11 external placement,
clean-Windows operation, ordinary-console Watcher Ctrl+C and explicit handler
stop. The optional sign-in shortcut is unexercised. Same-chat authorship limits
of prior receiving remain disclosed. These do not prevent a proposed candidate
checkpoint. No acceptance, deployment, current live process state or production
activation is inferred from this review.

## Verification performed and limits

- Runtime logging ownership checker passed using the repository `.venv`.
- Fifteen changed/new Python files parsed successfully; all three packaging
  PowerShell sources parsed without syntax errors. The staged/unstaged whitespace
  review passed (Git emitted expected CRLF-to-LF notices for source text).
- The four existing offline genuine-record TOON regressions passed. They use
  the already-installed pinned decoder and do not access/write the tracker.
- Source/archive and selected wheel-input hashes passed. ZIP payload/member
  completeness, copied archive/manifest identity and JSON syntax passed.
- No new tests or fabricated reporting histories were introduced. The existing
  hardening tests' changed bounds were statically reviewed, not executed: their
  forced-failure/contention cases are not current reporting acceptance authority.
  The genuine 1,027-operation producer cache receipt is reused within its
  documented limits; simultaneous waiter/eviction behavior remains unexercised.
- No setup, external-check helper, handler/watch operation, ingest, retention,
  model build, dependency install, download or full test campaign ran. Those
  actions are not hidden inside this checkpoint's verification commands.

The only review finding requiring a proposed text correction is the root README's
stale C9/application-0.0.2 pointer. No new product requirement is proposed.
Other dated handoffs are included with their historical scope; their original
receipt hashes are not rewritten to erase subsequent decisions.

## What the next workstation will and will not receive

After a later commit and push (or an explicitly arranged local Git transfer), a
clone supplies application/Learner source, retained immutable resources,
packaging catalogs and recipes, tests, the protected Trekker helper and dependency
lockfile, full manual/task history, this plan and **the actual complete C11 ZIP**.
The ZIP is runnable after extraction and machine-specific setup; it is neither
a download placeholder nor an LFS pointer. An unpushed local commit is not yet
fetchable from origin.

For ordinary C11 use, follow the candidate README and included installation guide:
Windows x64 plus PS5.1/.NET desktop components, real CK3 folders, an explicit
configuration and separate writable settings/data. Setup can create fresh local
history; it does not migrate this workstation's database. It does not require a
development Python or the source build. Start the watcher only when ready for
its documented pending-ingest/retention effects. Acceptance on a clean machine
still needs actual recorded observations.

For development, prepare a fresh local Python environment satisfying
`pyproject.toml` (Python >=3.11; the delivered Windows runtime is 3.12.14), install
the source's declared dependencies/editable package as described by
[development guidance](DEVELOPMENT_ENVIRONMENT.md), and use explicit `--config`
when exercising configured runtime commands. Do not copy this machine's `.venv`
or assume its drive paths. Current setup/config reference supersedes old
repository-config fallback instructions. Environment preparation is a separate
workstation action, not performed by this review.

The original absolute build plan, exact application wheel (2,805,027 bytes),
chardet wheel (1,160,778 bytes), frozen document snapshots and original receipts
remain under ignored `.codex-tmp/`. The two wheel hashes were freshly checked.
Their installed payloads, runtime/tool files and complete inventories are inside
the proposed ZIP. Those raw input archives are **not required to install C11**.
The source recipe accepts a pinned input plan; a clone alone does not yet provide
an executable portable plan plus those exact wheel files for a byte-identical
rebuild. A later rebuild needs a newly prepared plan and corresponding inputs;
do not treat `Fetch-UpstreamInputs.ps1` as an outstanding prerequisite. Keep the
working originals locally; exact rebuild-input transfer can be separately scoped
if needed. No whole experimental archive or redundant extracted tree is proposed.
Likewise, `Place-And-Verify.ps1` is source requiring its staged `TRANSFER.json`
and tree; it cannot run standalone from `packaging/windows`. The self-contained
ZIP installation instructions work without that private acceptance staging.

Machine-local and absent from a clone: current configuration, CK3/mod installations,
raw captures, SQL/review/history, journals, private acceptance evidence, caches,
venvs, old dirty worktree and the canonical Trekker store/toolchain. Links into
ignored receipts remain historical local references, not promised clone contents.
No current production configuration/selection was changed.

**Trekker continuity needs explicit separate coordination.** The protected helper
hard-codes the canonical store on this workstation. Do not run `init` or let a
second machine create an independent store to compensate for its absence in Git.
Continue using the canonical store from its authorized host. If ownership is
later moved, stop/coordinate clients and follow the complete-directory,
hash-verified backup/restore procedure in [the pilot handoff](TREKKER_CLI_PILOT_HANDOFF.md),
including sidecars, retention marker, toolchain/version and recovery evidence.
Resolve the authorized canonical path/access before using the helper on another
machine. The offline decoder test also depends on the pinned local toolchain;
do not initialize a database merely to make that import available.

## Exact proposed local execution

Recommend **one atomic checkpoint commit**, grouping the received application,
distribution/manual, catalog metadata, coordination repair and cleanup history
with its actual candidate. This avoids a commit whose CLI imports absent setup
or decoder modules, or whose guides lack the referenced ZIP.

Suggested message:
`Checkpoint Task 10 application, documentation and Windows candidate 11`

The prepared local execution script is
[execute-local-checkpoint.ps1](../.codex-tmp/advisory-checkpoint-20261013/execute-local-checkpoint.ps1).
It is **not executed**. It checks HEAD, empty staged state, the complete visible
status set and every reviewed file hash before applying the three-file proposed
patch. It aborts on concurrent edits; do not reset/restore to defeat that guard.
It then stages only the explicit paths below, checks the exact staged set and
ZIP/manifest blob hashes, checks whitespace, and commits once. It never pushes.
The index is currently empty and remains preserved. If it becomes nonempty,
stop to review the user's staged work instead of resetting it.

Exact staged path list (no `git add .`, wildcard inclusion or force-add):

```powershell
$paths = @(
    '.gitattributes'
    '.gitignore'
    'README.md'
    'docs/ADVISORY_LOCAL_CHECKPOINT_REVIEW_20261013.md'
    'docs/CURRENT_HANDOFF.md'
    'docs/LEARNER_RECLAMATION_RECEIPT_20261009.md'
    'docs/LEARNER_RESEARCH_RETENTION_PROPOSAL.md'
    'docs/LEARNER_STORAGE_MAP_20261009.md'
    'docs/LEARNER_URGENT_SPACE_RECLAMATION_PROMPT.md'
    'docs/PROJECT_PLAN.md'
    'docs/PROJECT_STATUS.md'
    'docs/TASK07D_DATABASE_REQUEST_HANDLER_HANDOFF.md'
    'docs/TASK07_SCOPE_REVIEW.md'
    'docs/TASK10_ADVISORY_REVIEW_PROMPT.md'
    'docs/TASK10_DELIVERABLES.md'
    'docs/TASK10_HANDOFF.md'
    'docs/TASK10_PROMPT.md'
    'docs/TREKKER_CLI_PILOT_HANDOFF.md'
    'docs/TREKKER_CMT132_RECOVERY.md'
    'docs/task10-deliverables/10A1_PIPELINE_INTERFACES.md'
    'docs/task10-deliverables/10A_FIRST_USE_DESIGN.md'
    'docs/task10-deliverables/10B_DISTRIBUTION.md'
    'docs/task10-deliverables/10C_ACCEPTANCE.md'
    'docs/task10-deliverables/10D_PRODUCT_REFERENCE.md'
    'docs/task10-deliverables/10E_USER_WORKFLOWS.md'
    'docs/task10-deliverables/ADVISORY_LOCAL_CHECKPOINT_AND_INSTALL_PACKAGE_REVIEW_20261013.md'
    'docs/task10-deliverables/COMPONENT_DOCUMENTATION_INPUT.md'
    'docs/task10-deliverables/LD_RESUME_AFTER_DEPENDENCY_VERIFICATION_REMOVAL.md'
    'docs/task10-deliverables/MANUAL_01_PRODUCT_INTRODUCTION_AND_ORIENTATION.md'
    'docs/task10-deliverables/MANUAL_02_STRUCTURE_AND_EDITORIAL_REVIEW.md'
    'docs/task10-deliverables/SOURCE_CHECKPOINT_PUBLICATION_20261011.md'
    'docs/task10-deliverables/WORKING_AGREEMENT.md'
    'docs/task10/ADVISORY_COMPLETION_BLOCKERS_20261012.md'
    'docs/task10/ADVISORY_STATUS_AND_INTEGRITY_REVIEW.md'
    'docs/task10/DATA_INTELLIGENCE_CONTRIBUTION.md'
    'docs/task10/DISTRIBUTION_HANDOFF.md'
    'docs/task10/DOCUMENTATION_HANDOFF.md'
    'docs/task10/FIRST_USE_DESIGN.md'
    'docs/task10/INTERFACE_INVENTORY.md'
    'docs/task10/LEARNER_DOCUMENTATION_HANDOFF.md'
    'docs/task10/MANUAL_01_HANDOFF.md'
    'docs/task10/OWNER_STATUS_AND_TESTING_20261011.md'
    'docs/task10/PIPELINE_HANDOFF.md'
    'docs/task10/REQUEST_RESULT_CACHE_HANDOFF.md'
    'docs/task10/WATCHER_DOCUMENTATION_HANDOFF.md'
    'docs/task10/WORKFLOWS_HANDOFF.md'
    'docs/team-governance/README.md'
    'docs/user/CLI_REFERENCE.md'
    'docs/user/CONFIGURATION_REFERENCE.md'
    'docs/user/DISTRIBUTION_REFERENCE.md'
    'docs/user/EXTERNAL_DATA.md'
    'docs/user/INSTALLATION.md'
    'docs/user/INTRODUCTION.md'
    'docs/user/ORIENTATION.md'
    'docs/user/PIPELINE_REFERENCE.md'
    'docs/user/PLANNED_FEATURES.md'
    'docs/user/PRODUCT_VERSION.md'
    'docs/user/README.md'
    'docs/user/RELEASE_REFERENCE.md'
    'docs/user/REPORT_QUERY_REFERENCE.md'
    'docs/user/TROUBLESHOOTING.md'
    'docs/user/WORKFLOWS.md'
    'docs/user/images/setup-folders-c9-crop.png'
    'packaging/learners/catalog.json'
    'packaging/models/catalog.json'
    'packaging/windows/Fetch-UpstreamInputs.ps1'
    'packaging/windows/INSTALL.md'
    'packaging/windows/Place-And-Verify.ps1'
    'packaging/windows/README.md'
    'packaging/windows/RELEASE_NOTES.md'
    'packaging/windows/Setup.ps1'
    'packaging/windows/THIRD_PARTY_NOTICES.md'
    'packaging/windows/build.py'
    'packaging/windows/external_check.py'
    'packaging/windows/launcher.py'
    'packaging/windows/ripgrep-LICENSE-MIT.txt'
    'packaging/windows/setup_gui_backend.py'
    'packaging/windows/upstream-inputs.json'
    'pyproject.toml'
    'release-candidates/task10/candidate11/README.md'
    'release-candidates/task10/candidate11/SHA256SUMS'
    'release-candidates/task10/candidate11/ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip'
    'release-candidates/task10/candidate11/release-manifest.json'
    'src/ck3chronicle/__init__.py'
    'src/ck3chronicle/cli.py'
    'src/ck3chronicle/config.py'
    'src/ck3chronicle/doctor.py'
    'src/ck3chronicle/pipeline/catalog.py'
    'src/ck3chronicle/pipeline/database_handler.py'
    'src/ck3chronicle/pipeline/repository.py'
    'src/ck3chronicle/pipeline/request_handler.py'
    'src/ck3chronicle/pipeline/runtime_identity.py'
    'src/ck3chronicle/setup.py'
    'tests/test_database_handler_hardening_requirements.py'
    'tests/work_state/fixtures/cmt-132.json'
    'tests/work_state/toon_output.test.mjs'
    'tools/work_state/pilot.mjs'
    'tools/work_state/toon_output.mjs'
)
```

After the Owner authorizes this concrete local checkpoint in a Git-writable
session, the next local command is:

```powershell
Set-Location 'C:\Users\nateb\Documents\ck3chronicle'
& '.\.codex-tmp\advisory-checkpoint-20261013\execute-local-checkpoint.ps1'
```

Its mutation core is exactly:

```powershell
# Preflight, content hashes and staged-state checks are in the prepared script.
git --no-optional-locks apply --check -- '.codex-tmp/advisory-checkpoint-20261013/proposed-policy-and-pointer.patch'
git --no-optional-locks apply -- '.codex-tmp/advisory-checkpoint-20261013/proposed-policy-and-pointer.patch'
git --no-optional-locks add -- $paths
git --no-optional-locks diff --cached --no-ext-diff --no-textconv --check
# The script also checks staged names and raw ZIP/manifest blob hashes here.
git --no-optional-locks commit -m 'Checkpoint Task 10 application, documentation and Windows candidate 11'
```

Each native command's exit code is checked by the script. Any failure preserves
the resulting state and stops; inspect before continuing rather than replaying
blindly. This session's policy makes `.git` read-only and offers no escalation;
the initial assignment also expressly forbids these mutations. No write probe
was attempted. The review and package preparation are complete independently
of that later Git execution.

### Optional separate push, only after later Owner authorization

In the same repository, first establish the actual configured destination and
live remote ref. The example deliberately expects the reviewed cached baseline;
an unexpected result stops for explanation, without pull/merge/reset/force-push.

```powershell
$repo = 'C:\Users\nateb\Documents\ck3chronicle'
$expectedRemote = 'https://github.com/ck3user75233/ck3chronicle.git'
$actualRemote = git --no-optional-locks -C $repo remote get-url --push origin
if ($LASTEXITCODE -ne 0 -or $actualRemote -ne $expectedRemote) { throw 'Unexpected push destination; stop.' }
$remoteLine = git --no-optional-locks -C $repo ls-remote --exit-code origin refs/heads/main
if ($LASTEXITCODE -ne 0) { throw 'Live remote inspection failed; stop.' }
if (($remoteLine -split '\s+')[0] -ne '709ea7842a0202c420b43355b18be91d8ca196a3') {
    throw 'Remote ref differs from the reviewed baseline; inspect without reconciling automatically.'
}
# Inspect the actual new local commit and its 98-path diff before publication.
git --no-optional-locks -C $repo show --no-ext-diff --no-textconv --stat --oneline main
if ($LASTEXITCODE -ne 0) { throw 'Local inspection failed.' }
git --no-optional-locks -C $repo push origin refs/heads/main:refs/heads/main
if ($LASTEXITCODE -ne 0) { throw 'Push failed; do not pull or force-push.' }
$published = git --no-optional-locks -C $repo ls-remote --exit-code origin refs/heads/main
if ($LASTEXITCODE -ne 0) { throw 'Push verification unavailable; preserve output and inspect.' }
$localMain = git --no-optional-locks -C $repo rev-parse refs/heads/main
if ($LASTEXITCODE -ne 0 -or ($published -split '\s+')[0] -ne $localMain) { throw 'Publication identity needs review.' }
```

No tags, other branches/projects, global settings or security/network policy
changes are part of that optional step. No current server divergence is assumed.

## Final refresh and stopping point

Final main-checkout status is **22 modified tracked + 73 visible untracked = 95
visible changed paths**, plus the explicitly selected **one still-ignored ZIP**.
All 91 initial changed-file hashes remained unchanged during this review.
The five prepared files account for the difference. Applying the proposed
`.gitignore`/`.gitattributes` changes later brings the exact checkpoint to 98 paths;
README is already one of the original 91. The complete refreshed status/hashes
are saved in `final-inventory.json`; index SHA-256 remains
`e065cd3cb42ae07c3fc4f355f7c5fc65630f73b71b4ccd5df849064320aac2fb`.
HEAD and cached origin/main remain the observed baseline. Staged diff is empty.

No main-checkout inclusion decision remains unresolved. The old ignored dirty
worktree and any future exact build-input/canonical-Trekker transfer are explicitly
separate from the requested source plus runnable-package checkpoint. The next
decision is execution of the concrete local patch/stage/commit plan; optional
publication is separate. Until that occurs these files remain local preparation,
not a source checkpoint another workstation can fetch from origin.

## Owner execution follow-up — 2026-10-13

The original review above records the pre-execution snapshot. Owner execution
subsequently staged the exact 98 reviewed paths, but stopped before commit at
`git diff --cached --check`. Four whitespace-only context lines in this report's
illustrated patch and the unchanged manifest's 4,331 CRLF lines triggered it.
The report's whitespace-only lines are corrected in the working tree for restaging.
The ZIP and manifest staged blob hashes match the received originals; their bytes
remain unchanged. The continuation checks ordinary files normally and checks only
the manifest with command-local `core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol`.
This recognizes its intentional CRLF without disabling other whitespace checks
or altering repository/global configuration.

Windows PowerShell 5.1 also required direct assignment of the decoded JSON path
array; the earlier wrapper treated all 98 entries as one item. That repair and
read-only preflight passed in Windows PowerShell 5.1.26100.9549. These were review
script defects, not product failures.

The Owner now requests bringing the remote up to date. The prepared
[continuation script](../.codex-tmp/advisory-checkpoint-20261013/finish-and-push.ps1)
verifies the captured staged tree, restages only this corrected review, checks
all 98 paths and the artifact hashes, commits once, checks the verified origin's
actual main ref, then performs a normal push of main and confirms the resulting
remote identity. Unexpected state stops without pull, reset or force-push. The
original execution script must not be restarted over this staged work. At this
follow-up's preparation, commit and push remain unexecuted; this note is not a
publication receipt.
