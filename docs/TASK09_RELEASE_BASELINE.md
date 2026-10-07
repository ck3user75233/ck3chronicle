# Task 09 baseline — 2026-10-07

## Reviewed remote publication

Owner requested the full Git review and an owner-run PowerShell script to bring
the remote up to date. The supplied report
`.codex-tmp/task09-git-reports/20261007T123507118Z/` shows local/remote `main` both
at `450b1f71fcd69d08f75de1002fc03950b436db2a`, no staged files or remote tags, and
no received-build/review drift. The exact script is
`.codex-tmp/Publish-Task09Baseline.ps1`, with frozen plan and stdlib Python helper
under `.codex-tmp/trek6-remote-20261007/`. It runs from any starting directory.

The reviewed update includes 195 existing changed/new paths: the prior 193-path
release scope plus the two Advisory usefulness-review documents, retained as
dated historical findings. Only the five previously named required ignored
model JSONs may be force-added. All 622 received build inputs and all prior
retained payloads are preserved; ordinary text Git newline normalization is
explicitly mapped in the frozen plan. No runtime evidence, local config or
generated wheel is committed. The historical Observer-bearing retained release
is Git history/catalog inventory only; it remains excluded from this wheel.

The script checks the exact local/remote base, file hashes, full staged/committed
tree, unchanged exclusions, model/Learner/catalog pins and successful tag target.
It creates commit `Pin Task 09 logging baseline and production-scope model`,
then annotated tag **`task09-baseline-2026-10-07`** on that new commit and pushes
only `main` plus that tag atomically. It never force-pushes, moves a tag, resets,
fetches, rewrites a release or changes services. A conflicting remote/staged edit
stops execution. A recorded partial execution can be safely resumed only after
its state/tree/ref checks pass; no unrecorded commit is adopted automatically.

**Actual publication receipt:** `.codex-tmp/trek6-remote-20261007/execution/state.json`
and `PUBLICATION.md` after execution; the tag annotation and TREK-6 checkpoint
record the actual commit and pins. These execution files do not exist at plan
preparation. Confirm the tag with `git rev-parse task09-baseline-2026-10-07^{commit}`;
this avoids embedding the new commit's hash in its own source. Script preparation
is not publication; TREK-6 stays open until actual commit/tag verification.

Release label **Task 09 baseline — 2026-10-07**, application **0.0.1**, Learner
algorithm **v61**, model package **2b12932103f3a3111a4e1880**. Production orders
9/10 are publication sequence numbers. The immutable wheel keeps its tested
research-at-build catalogs; repository catalogs record production adoption.
The exact full pins and genuine functional/logging results below remain valid.
No fresh campaign is needed. Live activation is unchanged; physical external
installation is deferred/unperformed for separately owner-issued Task 10.
Hosted release assets are not queried by the report and wheel upload is outside
this Git operation; the tested wheel remains at its exact local location below.

Earlier sections record the preceding local-publication and session-access states.

## Issued publication continuation — current result

The Owner issued [RELEASE_PUBLICATION_PIPELINE](task09-deliverables/RELEASE_PUBLICATION_PIPELINE.md).
Exact release label: **Task 09 baseline — 2026-10-07**. Package version **0.0.1**;
Learner algorithm **v61**. Production orders **9/10** are sequence numbers, not
product versions. Local model/Learner publication and repository adoption already
equal the authorized proposal; no registration/selection write was replayed.

Fresh evidence: `.codex-tmp/trek6-pin-20261007/reconciliation.json` authenticates
the exact wheel, all 620 installed members, all 622 original build inputs, both
model defaults and retained Learner manifest/payloads. All three prepared
preconditions match the preserved pre-publication metadata; current bytes match
the proposal and actual publication after hashes. No conflicting order or pin.
Build/classification/journal results below remain valid and are reused.

Operational `.codex-tmp/pipeline-r3-packaging-20261005/deployment/share/ck3chronicle/models/selection.json`
is a different file from repository `models/selection.json`, resolves under the
operational installation and still selects/authenticates `4ac4e8ee92346e6d14eacfbf`
at `839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
The normal loader in that installation independently confirms its default from
`C:/Windows`. No coupling was found; this does not inspect already running
in-memory services or claim their activation. Config remains unchanged.

**Git commit: none. Annotated tag: not created.** Owner authorization is present;
the remaining constraint is environment policy: `.git` is explicitly read-only
and this session has no permission-escalation route. No write was attempted or
restriction bypassed. TREK-6 is continued for this required publication step;
it must not be reported complete under the expanded assignment until the new
commit/tag exist and verify. No component receiving defect remains.

The refreshed exact review is `.codex-tmp/trek6-pin-20261007/git-review.json`,
with `git-include.txt`, `git-exclude.txt` and `git-force-include.txt`: **193 paths**,
including the issued publication prompt and Task10 deferral update; two independent
Advisory usefulness-review documents are now excluded and preserved. Only five
explicitly named required ignored model JSONs permit force-add. No staged paths
exist. Prospective path/content review includes no runtime files and detects no
private-key/token credential signatures; no actual staged-diff review is claimed.

All 622 raw received build inputs remain byte-identical. Existing `.gitattributes`
normalizes ordinary text CRLF to LF in Git; the review records raw hashes and
expected filtered Git blob IDs and identifies paths with only this newline
conversion. Immutable retained releases and models remain byte-exact. Before
committing in a writable session, refresh the review for intervening edits,
verify the actual staged tree and exclude runtime evidence/local secrets. Verify
the new commit against the received input inventory, expected Git newline
normalization and three approved publication metadata changes. No committed tree
correspondence or byte-reproducible rebuild is claimed before that verification.

Commit message: `Pin Task 09 logging baseline and production-scope model`.
Annotated tag: `task09-baseline-2026-10-07`, currently absent; never move it.
After creating the new commit, put its actual ID, label, wheel/model/Learner pins,
catalog orders and deferred/live limits in the tag annotation and Trekker/final
handoff. Do not edit the commit to insert its own hash. No push/upload is authorized.
Task 09 awaits only this publication step before final owner-closure readiness.
Task 10 receives this exact verified wheel/installation and the deferred,
unperformed physical outside-checkout check; it is not dispatched here.

Earlier local-publication receipt and proposal history follow. CMT-63 closed its
then-assigned receiving/local-adoption scope; the new Git assignment continues TREK-6.

**Published locally and adopted by the Owner as the newest production release.**
Model production order **9**, Learner production order **10**, repository default
and the verified wheel default select the exact full model below. Task 09 receiving
is complete: TREK-2 receipt CMT-60 and TREK-6 closure CMT-63. The Owner explicitly
deferred physical outside-checkout verification to Task 10; it remains unperformed.
Live service activation, Git commit/tag/push and remote upload are unexecuted.

This is the owner-issued [Pipeline baseline assignment](task09-deliverables/RELEASE_BASELINE_PIPELINE.md)
receiving [Learner's full delivery](learner-next-release/PRODUCTION_SCOPE_BASELINE.md).
The earlier CMT-61 placement hold is superseded by the
[owner disposition](TASK09_OWNER_DECISIONS.md#external-installation-verification-deferred-to-task-10--2026-10-07).
This is the full 73-log production model, not the two-log demonstration package.
The application distribution version remains **0.0.1**, algorithm **v61**; exact
wheel/package/manifest identities below identify this newly published combination.

## Exact tested combination

All aliases are beneath `C:/Users/nateb/Documents/ck3chronicle`:
**P** = `.codex-tmp/trek6-baseline-20261007`; **B** =
`.codex-tmp/trek2-baseline-20261007`; **I** = `P/deployment`.

| Item | Exact identity / location |
|---|---|
| Source/build inventory | `P/source-inventory.json`; 622 hashed build inputs, including 71 required untracked inputs at build; fingerprint `sha256:06cd89694ceaf392bb8c2e5fc524cc53f4eb3e20f46e46ef45d56027e36952f9` |
| Git base only | `450b1f71fcd69d08f75de1002fc03950b436db2a`; dirty working tree, **not** the tested source identity |
| Application wheel | `P/application/ck3chronicle-0.0.1-py3-none-any.whl`; 2,796,464 bytes; SHA-256 `2dbb613de4fbac058a1ae2f429eea8adf2f85a1c861c859b89eaa0d5d62f1b1e` |
| Installed application source | `application-source-sha256:eb41a2f7aee62c55004e642e35deccb6f89c2233042f8be1af76b5246602924b`; unchanged executable source, new wheel/resources |
| Learner | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`; manifest `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e` |
| Learner identity | `67f881e22dfec7477ee2fe423a1c9789285acab6825c2b78fa3065996bcd52a9`; `outer-diagnostic-consensus-v61` |
| Full model package / pin | `2b12932103f3a3111a4e1880` / `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505` |
| Compact model / candidate | `3bc531d578074e6a430c161e` / `B/registry/revisions/d729dea94d84323b8497e882`, candidate manifest `1b509590adfd56d1918d52dd94eaeab99e6f0d077dd83066a24a8499fd07a037` |
| Parser | `ck3-lossless-v1.8`; `0357b8d1c342c546452ed8f294405bfe41c86c7116eca51eddf8bc5b67984135` |
| Matcher / selector / schema | `ck3-native-matcher-v3` / `complete-assignment-v2` / 6; native matcher `fe559adf9349d2fe83f50a0b000a14f00630a591684cdeeeead44d99efe52caa` |
| Runtime/build dependencies | CPython 3.12.14, Unicode 15.0.0, chardet 7.6.0; install pip 25.0.1; build setuptools 84.0.0 / wheel 0.48.0. Project requires Python >=3.11 and chardet >=7.6,<8; only this Windows CPython combination is verified. |
| Offline dependency wheel | `.codex-tmp/combined-release-20261005/wheelhouse/chardet-7.6.0-cp312-cp312-win_amd64.whl`; `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64` |

`P/artifact.json` and `installed-receipt.json` verify all **620** members in both
directions, eight retained Learner releases / 371 payloads, dependency consistency,
and installed-only module locations. Relative to the prior received wheel, only
the model catalog/default and 15 new immutable model files differ. All executable
bytes are unchanged; all wheel names/content are free of Observer. Concurrent
Learner/Advisory documentation is explicitly accounted for in `P/git-review.json`,
not silently treated as application source. The source fingerprint is an evidence
inventory; runtime selection uses the existing catalog/manifest formats.

## Build basis and acceptance

The **73 original logs / 596,625,707 bytes** preserve ascending input-hash order,
training role, threshold **0.72**, `same-version-additive-v1`, batches **20+20+20+13**
and checkpoints **20/40/60/73**. Exact ordered paths/hashes/settings:
`B/build-basis.json`, SHA-256 `665f5bc680b1df27b40ed4ff24881807f4f4f431baa3b508c5d97c7617ccf7ad`;
governing prior basis `.codex-tmp/combined-release-20261005/build/build-basis.json`,
`fb1a3a35ebb8f26dd8a5fd6c36145b8b3aaac6e06308d498fed377e5a9864875`.
Pipeline authenticated all 73 new staged inputs and ten successful retained build/
evaluation/export executions; full build was not repeated.

| Evidence | Result and scope |
|---|---|
| Received full model | 394 templates (296 supported/98 provisional); 2,476,548 full / 118,038 provisional / **2 unknown**, zero unresolved training emissions. All four native-evidence checkpoints byte-identical to prior build; only enumerated provenance/path changes in model objects. Export parity: 91,925 contextual messages, 2,594,588 occurrences, 371,403 captures; zero changed matches/outcomes. |
| New installed classification | Genuine G2, 633,966 bytes, SHA-256 `05d71d156d3298e25568e4727d2fb15da111c2b74f8d18be29149e09e150ce95`: **4,141 template / 65 provisional**, 4,206 prepared Error Contracts. Entire prepared record arrays equal prior production package on this installation. All 12,947 present captures and 7,298 native regions agree with Learner; optional absence and source spans checked. |
| New retained evaluation | Installed `-I -S -B` Learner evaluates final candidate on G2; full JSON and stdout equal producer output, authenticated receipt/terminal agreement. No repeated training. |
| Logging | New: 13 events / one completed call pair; received full build: 332 events / 86 completed call pairs, including **natural periodic** observations. Actual code/source positions, nested ordering, completed counts and terminals inspected. [Detailed receiving](learner-next-release/OBSERVER_FREE_PIPELINE_RECEIVING.md#full-model-baseline-receiving--2026-10-07) supplies commands, actual excerpts and receipt paths. |
| Reused component evidence | Unchanged Reporting/public handler: 13 comparisons, 15 call pairs, 65 real request links, 44 native-byte occurrences. Unchanged Watcher: genuine 2026-10-05 capture/source-time/playset receipt and installed correspondence. All 394 model contract definitions equal prior production except model revision. No new database persistence/report or live CK3 lifecycle was necessary or claimed. |

G2 is training evidence, not unseen accuracy. Unknown/unresolved handling retains
the prior genuine 20-Run evidence with its original identities, including one
unresolved recovery outcome. Rotation, bare/count-only checkpoints, unusual input
and exceptional/setup/flush/crash cases remain unobserved; no artificial cases or
extra hooks were added. Normal stdout and error ownership remain intact.

## Placement and selection state

**Placement deferred to Task 10 by the Owner, 2026-10-07.** Physical external
installation/execution remains unverified for this artifact and is no longer a
Task 09 receiving blocker. The earlier proposed sibling staging directory and
request for access are not required for this release. `P/placement-preflight.json`
retains the original checkout-only policy evidence; changing cwd did not establish
physical relocation. [Task 10](TASK10_PROMPT.md#verification-and-handoff) will verify
its actual distribution outside the repository without checkout imports/resources.

Packaged `packaging/models/selection.json`, I's default and repository
`models/selection.json` now select **2b12932103f3a3111a4e1880** at manifest pin
**02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505**.
The repository catalogs mark model order **9** and Learner order **10** production.
Packaged catalogs retain their immutable research-at-build metadata; publication
does not rewrite the tested wheel. Config and running services were not changed.
Learner has no implicit selection file; callers select its exact release ID.

## Owner adoption proposal

**Owner authorized publication in the Pipeline conversation on 2026-10-07:
“I want this published as per usual” and “THIS IS THE NEW MOST RECENT PRODUCTION
VERSION OF CK3CHRONICLE”. Steps 1–3 below are now executed; step 4 remains unexecuted.**
Original prepared files/diffs and preconditions remain in `P/adoption/` as history.
Actual receipt is `.codex-tmp/trek6-production-20261007/publication.json` (**PUB**).
All three precondition hashes matched; current model/Learner orders were confirmed
as next valid orders 9/10. Exact before metadata is retained alongside PUB in
`before/`; after hashes, argv, return code, stdout and journal are recorded.
The installed registration command returned 0, preserving normal JSON stdout;
the exact reviewed Learner metadata promotion and schema-2 selection then applied.
All 620 installed members and both manifests were freshly authenticated. Repository
and installed defaults load the same intended model. Existing classification and
Learner execution evidence remains valid; no redundant training or ingestion ran.

Publication journal `model-release-27e8ea9cac6c4263b4934fc26d3d9848.jsonl`
has line 1 `invocation_started`, `operation: register`, installed `pipeline/catalog.py`
source; line 2 `invocation_finished`, `outcome: success`, same invocation ID.
Actual path is `.codex-tmp/trek6-production-20261007/journals/` plus that filename.
`registration-command.json` records elapsed time/argv/return code; `register.stdout`
agrees with the resulting order-9 catalog row. These two events demonstrate
registration invocation/terminal consistency, not another classification run.

Git source publication remains pending because this session's `.git` access is
read-only. No commit/tag/push or remote release was created; the older HEAD must
not be labelled as this tested baseline. The exact source proposal below remains
available for execution in a Git-writable session. Local production publication
uses the same catalogs/immutable wheel mechanism as the prior v61 release.

Original concrete adoption operations (status as above):

1. Register model **2b129... / pin 02c706...** locally in `models/` as production
   **order 9**, publication evidence `docs/TASK09_RELEASE_BASELINE.md#owner-adoption-proposal`.
   The complete existing `ck3chronicle-model-release register` argv is in
   `P/adoption/proposal.json`; it names `models/releases/2b12932103f3a3111a4e1880`
   as source, the full pin, `--production-order 9` and that evidence reference.
2. Publish Learner **2ec4... / pin 9ba2...** at production **order 10**, same evidence
   reference, by the **explicitly reviewed catalog-row metadata change** in
   `P/adoption/learners/catalog.json`. All other rows/payloads remain unchanged.
   Current `register_release` refuses promotion of an existing research row
   (`existing learner publication order cannot change`); do not issue a knowingly
   failing register command or remove a live row to circumvent that guard. The
   Owner approved publication; that exact metadata edit has now been applied
   without changing retained executable bytes.
3. Adopt `P/adoption/models/selection.json` as repository `models/selection.json`
   after those registrations. It is the same schema-2 package/manifest selection
   already tested in I. The frozen packaged catalogs/default stay at their tested
   bytes; repository publication metadata does not rewrite the immutable wheel.
4. Review **193 exact include paths** in `P/git-include.txt` / `git-review.json`,
   then commit the tested dirty source/resources plus approved metadata using
   **`Pin Task 09 logging baseline and production-scope model`**. Proposed annotated
   tag: **`task09-baseline-2026-10-07`**, targeting that **new commit**, never the
   old HEAD. Five specifically pinned model JSONs in `git-force-include.txt` are
   required by the wheel despite existing ignore rules. No broad force-add.
   Include exact component implementations, removal, clean retained release,
   model resources, package defaults, tests/pilot and handoffs. Historical immutable
   `9c02...` resources are catalog/history material only and excluded from the wheel.
   Concurrent Advisory review documents are explicitly labelled in the reviewed
   list. Exclude all logs, SQLite/review data, environments, journals, evaluation
   outputs, local config, tracker store and `.codex-tmp/**` per `git-exclude.txt`.

Local publication/default adoption are executed under the Owner's instruction.
Git publication and external physical installation are not claimed. The latter is
dispositioned to Task 10; publication does not itself switch running services.
No Task 09 implementation/receiving defect remains; operational activation and
Task 10 issuance are separate from this completed receiving.

## Prior baseline, rollback and Task 10 input

Prior received wheel `.codex-tmp/trek6-removal-20261007/application/ck3chronicle-0.0.1-py3-none-any.whl`,
SHA-256 `1a325cd40eb29878e6c7c44a25615ea3eb3e47e4173eb6b72c3d6f8e596fb7ae`,
and operational R3 wheel `.codex-tmp/pipeline-r3-packaging-20261005/application/ck3chronicle-0.0.1-py3-none-any.whl`,
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`, remain immutable.
The prior received wheel is logging-enabled and Observer-free; R3 is the separate
production rollback identity. Follow the [existing cutover record](learner-next-release/PIPELINE_CUTOVER.md)
for any separately authorized live action. Keep existing Runs and lineage; never
reset/reingest history as rollback. `P/before/` preserves receiving edits;
`.codex-tmp/trek6-production-20261007/before/` preserves the three actual
pre-publication metadata files. Restore only guarded files/metadata whose current hashes match this delivery
or a recorded adoption, reconciling intervening work; retain all new/old releases.

Task 10 receives W/I above, offline chardet wheel, source inventory and build recipe
`P/build.py`, the explicit catalog selection interfaces in [RELEASES](RELEASES.md),
public `HandlerClient`, and the shared logging owner. Current operational config
is cwd-resolved `config.toml`; explicit `--models-root`, Learner `--root/--release`,
receipt/log-dir and root command database/log-dir interfaces work as documented.
No general root `--config`/LocalAppData setup flow is implemented here. Task 10 must
still deliver its Windows runtime/bundle choice, central explicit configuration,
first-run validation/database creation, safe repeat setup, user package selection
and launch UX, and genuine installation/setup evidence. This venv on a developer
machine is not a cold-machine installer. Physical external-placement verification
belongs to Task 10 under the Owner's subsequent disposition.
