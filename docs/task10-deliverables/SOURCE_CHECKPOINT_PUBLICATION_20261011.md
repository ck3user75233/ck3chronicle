# Owner assignment: publish the current source checkpoint for a second workstation

**Superseded for the Owner's 2026-10-13 continuation by
[Advisory local checkpoint and install-package review](ADVISORY_LOCAL_CHECKPOINT_AND_INSTALL_PACKAGE_REVIEW_20261013.md).**
This machine is the sole active development workstation. The new assignment
begins with a read-only local review of all changes, includes the selected complete
install ZIP in a proposed controlled tracked folder, and leaves staging/commit
execution and any push for the resulting concrete plan. Do not use this older
prompt's blanket ZIP exclusion, stale candidate pointer or immediate push steps
for that new review. The original dated instructions below are historical.

Prepared 2026-10-11. Issue this prompt in a new chat on the existing workstation.

## Objective and authority

Checkout: `C:\Users\nateb\Documents\ck3chronicle`.
Expected remote: `https://github.com/ck3user75233/ck3chronicle.git`.

Review the current local changes, commit the intended source/documentation work
and push it to the existing remote so I can clone the repository on another
workstation. **This assignment authorizes Git staging, commits, fetching and a
normal push to `origin/main`.** Complete the review and publication without asking
for this same authorization again. Preserve concurrent/unrelated work. If a
working branch is needed, use `codex/` and bring the reviewed checkpoint to main
without rewriting published history.

Publish a truthful development checkpoint, not a completed Task 10 release.
Task 10's application/Watcher follow-ups, final bundle/manual integration and
acceptance remain open. Do not require those implementation assignments to finish
before publishing the current coherent source state. Do not implement their
repairs in this publication task or mark them completed.

No final Task 10 tag, hosted release/binary upload, model build, re-pin, runtime
configuration change, deployment, service start/stop/restart, retention change or
data reclamation is authorized. Do not modify immutable retained releases or
already received artifacts. Do not force-push, reset away work, run `git clean`,
or use a blanket `git add -A` on this mixed working tree.

## Retrieve the current evidence

Read root `AGENTS.md`, `docs/PROJECT_PLAN.md`, `docs/PROJECT_STATUS.md`,
`docs/CURRENT_HANDOFF.md`, `docs/team-governance/README.md`,
`docs/DEVELOPMENT_ENVIRONMENT.md`, `docs/TASK10_HANDOFF.md`,
`docs/TREKKER_CMT132_RECOVERY.md`, and
`docs/task10/OWNER_STATUS_AND_TESTING_20261011.md`.
Follow the current handoffs rather than reconstructing all repository history.

Refresh the relevant tracker state through the protected route only:

```powershell
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilot = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs'
& $pilotNode $pilot team-state launch-distribution
& $pilotNode $pilot task-list
& $pilotNode $pilot task-show TREK-9
& $pilotNode $pilot task-show TREK-10
& $pilotNode $pilot task-show TREK-11
& $pilotNode $pilot task-show TREK-12
& $pilotNode $pilot task-show TREK-16
```

Run these serially. Use the canonical store documented in
`docs/TREKKER_CLI_PILOT_HANDOFF.md`. No raw tracker/SQL, alternate store/helper or
invented IDs. CMT-132 is already committed and reconciled; **do not replay it**.
Read later comments and stop/reconcile a genuinely new incomplete write before
retrying. This publication assignment does not replace the existing component
or receiving records. No team dispatch is authorized.

At preparation, `main` and cached `origin/main` were Task 09 commit
`709ea7842a0202c420b43355b18be91d8ca196a3`. Live remote inspection failed to connect;
refresh the real server state before deciding how to publish. Inspect all
worktrees and preserve the unrelated `codex/pipeline-inspection` worktree.

## Review and prepare the exact checkpoint

1. Record branch, HEAD, remotes, worktrees, tracked diff and untracked inventory.
   Check later changes before staging and again before committing; other owning
   chats may have progressed since preparation. Coordinate a stable snapshot of
   any actively edited files. Do not freeze teams by inventing an approval gate.
2. Review the intended Task 10 application/configuration/storage changes, new
   `setup.py` and `pipeline/runtime_identity.py`, packaging catalogs/Windows build
   recipe, `pyproject.toml`, user manual/assets, assignment/handoff/status documents,
   and requirement-derived test changes. Include the recovered pilot's owning
   `tools/work_state/pilot.mjs`, new `tools/work_state/toon_output.mjs`, genuine
   regression tests/fixture under `tests/work_state/`, and recovery documentation.
   Include relevant Advisory/status and Learner storage/reclamation Markdown
   receipts already prepared locally, not their generated runtime payloads.
   This is an expected inventory, not permission to stage unknown files blindly.
3. Distinguish source/build recipes/manual assets from generated artifacts and
   machine state. Keep ignored ZIPs/wheels, `.codex-tmp/`, `.ck3chronicle/`, local
   TOML/runtime paths, virtual environments, databases, captured logs, research
   outputs and secrets out of the commit. Review fixtures/documents for actual
   sensitive content; existing evidence paths alone are not an instruction to
   erase provenance. Do not force-add ignored runtime evidence to make links
   appear portable.
4. Preserve already tracked model and Learner closure. `.gitattributes` marks
   `/learners/releases/**` and `/models/**` as `-text`; do not normalize their
   bytes. Confirm declared package data/source inputs remain available from the
   committed tree, and inspect any apparent pin/catalog changes against the
   received source handoffs. Distinguish a local registration/path change from
   immutable payload identity. Do not regenerate a manifest to hide a mismatch.
5. Update only the coordinated current publication/continuation text needed to
   describe this checkpoint. Preserve dated historical receipts. State that C9,
   the newer 1,024-result wheel and the final manual are not yet one final bundle.
   Do not claim the new source commit reproduces C9's older application hash or
   proves all outstanding repairs are integrated.
6. Stage an explicit reviewed file list. Inspect the staged diff, accidental
   deletions, whitespace checks and file sizes; exclude unrelated changes without
   deleting them. Use cohesive commits if that improves review. Record precisely
   what remains unstaged and why.

## Verification and publication

Use the repository's existing environment and relevant checks. For the changed
runtime source run the required logging-ownership check:

```powershell
.\.venv\Scripts\python.exe -B tools/check_runtime_logging.py
& 'C:\Program Files\nodejs\node.exe' --test tests/work_state/toon_output.test.mjs
```

The Node checks use genuine saved tracker records and the pinned local tooling;
inspect their prerequisites before running. Verify any other affected source or
packaging contracts with appropriate existing checks and received evidence.
Do not blindly run tests that start production clients, invent histories, inject
failures or perform reingestion. Do not rerun expensive model builds merely to
publish unchanged retained resources. Report failures and unavailable checks
honestly; fix only publication/tooling issues within this assignment and return
component defects to their existing owners.

Fetch the remote and inspect divergence. If it advanced, integrate reviewed work
without force or loss; resolve routine conflicts while preserving the owning
intent. A genuinely ambiguous conflict needs a precise question, not a reset.
Commit the reviewed checkpoint and push normally to `origin/main`. Verify the
actual remote main SHA matches the intended published commit. A local commit,
cached tracking ref or prepared push command alone does not prove publication.

If this chat's tool permissions or network prevent a necessary Git action,
complete all available review/preparation and give the exact remaining owner-run
command with the concrete error and current state. Do not bypass restrictions,
claim success, or request generic permission already granted by this prompt.

## Workstation handoff and stopping point

Write `docs/task10/SOURCE_CHECKPOINT_PUBLICATION_HANDOFF.md` with the included
scope, verification, remaining Task 10 obligations, and portable setup references.
Include it in the checkpoint where practical. Avoid trying to place a commit's
own final SHA inside itself; report the final local/remote SHAs in the chat after
publication. Clearly distinguish a prepared handoff from verified remote success.

Supply exact new-workstation commands such as:

```powershell
git clone https://github.com/ck3user75233/ck3chronicle.git C:\Users\nateb\Documents\ck3chronicle
git -C C:\Users\nateb\Documents\ck3chronicle rev-parse HEAD
```

Adjust the destination for the other workstation's account and do not overwrite
an existing checkout. For an existing clean clone, provide the appropriate
non-destructive fetch/fast-forward route. Give the expected full published SHA
and the current development-environment instructions. Do not assume the local
virtual environment transfers with Git.

Also identify the files/state that a clone will **not** supply:

- Testable C9 ZIP:
  `C:\Users\nateb\Documents\ck3chronicle\.codex-tmp\task10b\build\ck3chronicle-0.0.2-task10b-candidate9-win-x64.zip`.
  Expected SHA-256
  `db1ed81f050e13c93652681e829c18ef282a92965c116aee0fc59cea49eedfc1`;
  authenticate it again if presenting it as the current copy. It must be copied
  separately, and remains an interim candidate with documented acceptance gaps.
- Runtime configuration, production history and ignored evidence do not transfer.
  The new workstation's test setup needs its own explicit local paths/state.
- The protected Trekker helper/toolchain depends on this workstation's canonical
  store and absolute paths. Do not initialize another empty store or fork its
  history on the second PC. Tracker migration/synchronization is a separate
  coordination decision; continue canonical tracker operations here meanwhile.

Finish with the commit(s), verified remote SHA, checks/limits, remaining local
changes and exact clone/package instructions. Do not keep implementing Task 10,
tag a final release or activate production after this source handoff is complete.
