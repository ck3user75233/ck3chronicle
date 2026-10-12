# Advisory — review all local changes and prepare a source-and-package checkpoint

Owner assignment for a new Advisory chat, 2026-10-13.
Checkout: `C:\Users\nateb\Documents\ck3chronicle`.

## Starting facts and objective

**This machine is currently the only workstation doing active ck3chronicle
development.** The current development work is local. Do not assume the remote
contains newer work, that another workstation has contributed changes, or that
local work needs to be reconciled to a more authoritative remote version.
Multiple chats may edit this same checkout; inspect the actual current files.

The Owner intends to begin development on another workstation soon and use the
Git repository to bring it up to date. Review **every local change outside Git's
ignore rules**, together with all changed tracked files, for tracking, staging
and committing. Do not restrict the review to Task 10, a prior selected file list,
your own edits or a presumed team boundary. Give every change a disposition.

The Owner also wants the **complete proposed install package under review for
shipping included in Git**, in a controlled release-candidate folder. A clone
should contain the actual install ZIP as well as the source, documentation and
build recipes. This explicitly supersedes the earlier proposal to keep every
ZIP outside Git and transfer the package separately.

This prompt replaces `SOURCE_CHECKPOINT_PUBLICATION_20261011.md` for this task.
The immediate assignment is a read-only Git audit, review and concrete checkpoint
preparation. Produce recommendations for ignore rules, package inclusion and the
exact staging/commit plan. **Do not stage, commit, fetch, pull or push during this
initial review.** "Consider for committing" and "possibly pushing" do not mean
publish immediately. Prepare the complete proposal before presenting any remaining
execution decision. Do not use a generic permission question to avoid the review.

## 1. Inventory local changes without mutating Git

Read root instructions, current plan/status/handoff and the relevant current
technical handoffs. Retrieve `team-state advisory`, `task-list` and the relevant
actual package/manual/acceptance records through
`C:\Program Files\nodejs\node.exe` invoking the absolute
`C:\Users\nateb\Documents\ck3chronicle\tools\work_state\pilot.mjs` helper.
Use the canonical store and serial operations from the pilot handoff; no raw
tracker reads, alternate store or duplicate producer records.

Use ordinary read-only Git commands, not direct edits to
`.git`. Suppress optional index refresh writes with `--no-optional-locks`; avoid
external diff/text-conversion helpers. Example starting commands:

```powershell
$repo = 'C:\Users\nateb\Documents\ck3chronicle'
git --no-optional-locks -C $repo -c core.fsmonitor=false rev-parse --show-toplevel
git --no-optional-locks -C $repo -c core.fsmonitor=false status --porcelain=v1 --untracked-files=all
git --no-optional-locks -C $repo diff --no-ext-diff --no-textconv --name-status
git --no-optional-locks -C $repo diff --cached --no-ext-diff --no-textconv --name-status
git --no-optional-locks -C $repo ls-files --others --exclude-standard
git --no-optional-locks -C $repo worktree list --porcelain
```

Inspect full staged and unstaged diffs, untracked contents, deletions, renames,
binary files, sizes, submodule/nested-repository status where relevant, and local
commits not represented by cached tracking refs. Existing tracked files remain
in scope even if an ignore pattern now matches them. Preserve existing staged
work; do not reset the index. Never run `git clean` or restore over local changes.

The initial Git inspection must leave the index, objects, refs, configuration
and working files unchanged. Save the inventory afterward under an ignored
review directory; writing the report is distinct from changing Git state.
Read-only access is often possible when `.git` writes are restricted. If a command
is denied, record the exact command/error and continue other available inspection;
do not test access by making a write or bypassing restrictions.

Network access is intentionally controlled. **No remote access is needed for
this local review.** Local `origin/main` is a cached reference, not a live server
observation. Report what local evidence establishes without inventing remote
divergence or treating network unavailability as an audit blocker.

## 2. Review every change and the ignore policy

Create a complete path-level disposition inventory, grouped for readability:

- Track/include: source, tests, tools, documentation, build recipes, necessary
  retained resources and other appropriate project content.
- Recommend ignoring: explain the actual generated, private, machine-specific
  or disposable content and the narrow rule that would cover it.
- Recommend removing an ignore or adding a scoped exception: explain why the
  file is needed in a clone and how to avoid admitting unrelated runtime data.
- Hold for a specific reason: identify the concrete issue and resolution, not
  simply "outside my task" or "authored by another team".

For each proposed `.gitignore` change show the exact rule/diff, affected paths
and rationale. Check repository, local exclude and configured global ignore
sources as applicable. Use read-only `git check-ignore -v` to identify the rule
actually responsible; use its `--no-index` option when examining tracked paths.
Ignoring a tracked file does not untrack it: explain any proposed index removal
separately and preserve the local file. Do not apply ignore changes in this phase.

Review ignored areas selectively for **needed transfer inputs**, especially the
selected install ZIP and build/material dependencies. Do not hash or propose
tracking the entire experimental/runtime archive. Keep secrets, local databases,
captured CK3 logs, virtual environments, caches and the canonical Trekker database
out unless a specific, justified Owner decision changes that treatment. Preserve
already tracked immutable model/Learner resources and their byte-preserving
`.gitattributes` rules. Do not regenerate model pins or normalize retained bytes.

## 3. Prepare the tracked install package

Identify the latest actual complete candidate from current deliveries and local
artifacts. At prompt preparation the handoff identifies:

```text
.codex-tmp/task10-final-20261012/build/ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip
SHA-256: 97f52263beca3387390d220d33ea461d6e60edaca7e70314096f473566750771
Size: 20,980,042 bytes
Application: 0.0.3; manual: manual-20261012-r4-application0.0.3
```

Refresh this pointer before selecting it. Do not automatically fall back to C9,
C10 or a standalone wheel. Verify the selected ZIP against its local delivery
receipt and inspect its member inventory for completeness and accidental private
state. Reuse existing component verification; the Owner has removed upstream
Python/ripgrep comparison/download requirements.

Prepare a controlled location such as:

```text
release-candidates/task10/candidate11/
    ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip
    SHA256SUMS
    README.md
    release-manifest.json
```

Use the actual selected candidate identity if newer. **Copy**, never move or
overwrite, the received archive; verify source/destination hashes. This task
authorizes preparing these new working-tree files after the read-only inventory,
but not staging them yet. Include the actual ZIP in the proposed Git tree, not
just a path, download link or Git LFS pointer that requires a separate service.
Do not extract thousands of duplicate installed files into the source tree.

Propose a narrowly scoped exception to the current `*.zip` ignore rule for the
selected controlled artifact. Keep `.codex-tmp/` and unrelated ZIPs ignored.
Inspect actual size and local Git configuration before recommending any special
storage mechanism; do not introduce LFS or a new hosting workflow by default.

The package README should state the artifact's purpose, version, checksum,
included manual/model identities, extraction/start instructions and actual
acceptance limits. Copy the existing release manifest unchanged where useful.
Keep any sanitized publication summary distinct from original private receipts;
never alter the authenticated ZIP. Label it a proposed release candidate, not
an accepted production deployment. It need not wait for final acceptance to be
included in this source-and-package checkpoint.

## 4. Recommend the exact checkpoint and workstation handoff

Write `docs/ADVISORY_LOCAL_CHECKPOINT_REVIEW_20261013.md` with:

1. Observed local branch/HEAD, inventory totals and complete path dispositions.
2. Proposed ignore changes, including files to bring into tracking.
3. Selected package, prepared controlled paths, hashes and acceptance status.
4. Explicit proposed staging paths, logical commit grouping/message(s), and
   relevant validation or existing evidence. Do not hide runtime/dependency
   actions inside nominal checks or create new product test campaigns.
5. What a new clone will supply and what remains machine-local. Explain required
   environment/configuration setup and references. Do not initialize a second
   independent Trekker store to compensate for its absence from Git.
6. The exact next local staging/commit commands and an **optional separate push
   step**, with any real execution/access limitation stated plainly.

Refresh local status before finalizing the plan so edits made by other chats
during review are accounted for. Include this review, the new prompt and prepared
package files in the final proposed inventory. Do not silently discard unfinished
but legitimate development work merely because it is not a final release.

For any later Owner-authorized push, restrict actions to this repository and its
verified configured remote. A live remote check would establish the actual
destination state; it would not presume the server is ahead. An unexpected ref
mismatch is something to report and understand, not permission to pull, merge,
reset or force-push over the sole active development checkout. Do not touch other
projects or change global Git/network/security settings.

Conclude with the concrete proposed checkpoint and any genuinely unresolved
inclusion decision. State clearly whether changes are merely prepared, staged,
committed or pushed. This review ends with a ready-to-execute local plan and
prepared package; it does not claim that another machine can fetch unpushed work.
