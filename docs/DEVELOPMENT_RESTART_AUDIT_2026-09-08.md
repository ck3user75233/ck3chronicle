# Development restart audit — 2026-09-08

This audit answers the four restart questions separately. Each section begins
with the documentation/evidence located before giving a verdict.

## 1. Is relocation into the ck3chronicle directory complete?

Located authority/evidence:

- `AGENTS.md` and `docs/WORKSPACE_ROUTING.md` define the canonical repository
  and runtime boundaries.
- `docs/REPOSITORY_AND_BACKUP.md` defines what belongs in Git versus the ignored
  local runtime.
- `.ck3chronicle/wip/runtime/migration/runtime-import-receipt.json` is the
  machine-local relocation receipt.

Verdict: **the physical runtime relocation is complete**. The receipt records
251 files and 3,938,533,553 bytes copied and hash-verified on 2026-08-29 from
the old LocalAppData runtime to
`C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\runtime`. The current
configuration, database, sessions, pending queue, and watcher records are under
that canonical checkout. No active code needs the old root.

Qualification: the local runtime is intentionally ignored and needs its own
backup. Git protects the reusable software and project method, not captured CK3
evidence or the production SQLite database.

## 2. Is the Git repository intact, functional, and current?

Located authority/evidence:

- `AGENTS.md`, `docs/WORKSPACE_ROUTING.md`, and
  `docs/REPOSITORY_AND_BACKUP.md` define Git ownership and the canonical remote.
- Local Git references, object verification, worktree status, packaging files,
  and CI were inspected directly.

Verdict by property:

| Property | Result | Evidence |
|---|---|---|
| Correct standalone root | Yes | `git rev-parse --show-toplevel` returns the canonical checkout. |
| Correct remote | Yes locally | `origin` is `https://github.com/ck3user75233/ck3chronicle.git`. |
| Object database intact | Yes | Full fsck found no missing/corrupt reachable object. |
| Branch/ref coherent | Yes locally | Branch and local origin-tracking ref both point to `a5925fa`. |
| Canonical `main` tracking | **Not configured locally** | `remote.origin.fetch` names only `codex/ck3chronicle-reboot`; no `refs/remotes/origin/main` exists. Restore the ordinary all-heads fetchspec and fetch before comparing/promoting to `main`. |
| Complete worktree representable | Yes | An isolated throwaway Git index/object directory staged all intended tracked/untracked changes, passed `git diff --cached --check`, and wrote a complete tree; the probe was then removed. The unrelated local sandbox/security transfer package is explicitly ignored. |
| Current work reflected in a commit/remote | **No** | The large reboot remains unstaged/uncommitted. |
| Package structure/import surface | Yes | The agent-accessible project `.venv` imports the current editable package and CLI successfully; the earlier checks also parsed 64 Python files and imported 52 package modules. |
| Current post-edit tests | Yes | All 14 current requirement-derived checks pass through the project `.venv`: six watcher/capture and eight recovery/identity checks. Isolated imports, CLI help, and `pip check` pass as well. The inaccessible optional owner environment is not a verification dependency. |

Therefore the repository is structurally intact, but it is not yet a fully
recoverable representation of the current source state. A reviewed commit and
push are required. This task's filesystem policy permits worktree writes but
not writes under `.git`, and outbound GitHub access failed, so it cannot create
that checkpoint itself. The live remote could not be fetched; only the existing
local remote-tracking ref was compared.

## 3. Is the project plan documented and understood?

Located authority/evidence:

- `docs/OWNER_PRODUCT_INTENT.md` — product boundary and vocabulary.
- `docs/TRUSTED_RUN_SPEC.md` — first-capability requirements.
- `docs/PROJECT_PLAN.md` — named milestone dependencies and release sequence.
- `docs/REQUIREMENTS_AND_TESTING.md` — requirement/test traceability.
- `docs/ARCHITECTURE_AND_DATA_LINEAGE.md` and
  `docs/DATA_COMPATIBILITY_AND_OPERATIONS.md` — target data and operations.
- `docs/PROJECT_STATUS.md` and `docs/CURRENT_HANDOFF.md` — current truth and
  continuation order.

Verdict: **the named milestone plan is coherent and Trusted Run is clearly
first, but the prior status/handoff was stale**. It claimed 37 sessions and two
pending captures, instructed immediate production processing, and did not
record the interrupted database transaction. The current status and handoff
now record 38 sessions, 22 pending captures, database recovery, watcher review,
the disabled production command, and the rehearsal-first recovery order.

Owner review reset the test tree. The only tests now present were written after
that reset from explicit watcher/capture requirements and the approved
ingestion-recovery requirements. New verification must continue to trace
directly to an active owner-directed requirement.

## 4. Is the broken error-log parse/database process documented and understood?

Located authority/evidence:

- The overlooked 2026-08-29 plan was recovered byte-for-byte from dangling Git
  blob `e6084af5a604281ad68fe6da158de1369632ac13` and used as an
  incident-recovery input. The obsolete active plan was later deleted after the
  ingestion diagnosis completed; its mechanisms do not create current product
  requirements or test gates.
- The old `docs/CURRENT_HANDOFF.md` instructed `process-pending --json` but
  contained no failure record.
- `src/ck3chronicle/processing.py`, `harvester.py`, and `archive_registry.py`
  define the current finalization/registration/parse/classify/project batch.
- The production database, its rollback journal, pending queue, old metadata
  records, exception store, and read-only audit outputs were inspected.

What is proven:

- A prior production write ended with a 32,743,664-byte hot SQLite rollback
  journal. A verified pre-recovery copy exists; normal SQLite rollback recovery
  completed; the database is structurally sound and readable.
- The old command finalized all pending directories and then walked every
  historical session. The replacement requires one exact pending capture or
  one exact historical session, prints a read-only frozen plan, and requires
  `--execute` before mutation.
- The 22 pending captures use the old six-log layout and external metadata
  records. Current finalization can read the old logs, but without conversion it
  would replace known lifecycle/crash facts with `legacy_pending`/`unknown` and
  omit the seven separately preserved exception attachments.
- The old metadata and all seven exception claims validate. The one-time
  converter was applied only to the readable rehearsal copy: 22 metadata files
  and seven exceptions converted, followed by an idempotent zero-change
  preview. Production remains untouched.
- Nate copied the 22 protected directories to the prepared rehearsal root. All
  132 copied files (728,770,249 bytes) are readable and agree with the watcher
  records by name, size, and source mtime; retained metadata and exception
  hashes match. The old records did not contain a hash for every principal log,
  so no stronger source-versus-copy hash claim is made.
- The ACL cause is exact: Python `tempfile.mkdtemp()` created protected
  owner-only watcher staging directories, and rename retained those DACLs. A
  controlled Windows probe reproduced it. The owner did not request this
  behavior. Future watcher captures now use an inheriting ordinary directory.
- A flushed processor journal, OS-held exclusivity lease, strict read-only
  exact-session plan, and bounded existing-session execution are implemented.
- A byte-verified disposable Run ID 14 rehearsal reproduced the stall at
  `DELETE FROM source_blocks`. Both referencing child tables lacked an index
  beginning with `source_block_pk`, so SQLite scanned roughly 1.5 million child
  rows for every deleted source block. Storage schema v3 adds those indexes.
- After the fix, the affected retained run completed parse, classification,
  and projection in 159.663 seconds with clean SQLite integrity and no foreign
  key errors. The formerly stalled source-block delete took 217.344 ms.
- All 22 copied pending captures then completed one at a time as Run IDs 39–60.
  Their 702,113 source blocks produced 720,090 semantic occurrences and 16,271
  clusters. Final verification rehashed all 22 archives/139 retained files,
  reconciled every database projection/counter, found no duplicate
  `error.log` hash, and returned `quick_check=ok` with no foreign-key errors.
- Measured repeated work was also corrected: immutable per-block projection
  evidence improved one real preparation path 23.97x; classification reuse for
  the same `raw_block_pk` and source family improved another real comparison
  36.52x with identical ordered results. Storage schemas v4–v6 supply the
  additional measured deletion and validation indexes.
- A deliberate mid-transaction interruption preserved the hot journal,
  recovered through standard SQLite rollback, released the processor lease,
  and completed on an exact-session retry. This proves the journal and bounded
  recovery path rather than merely describing it.

What is not proven:

- Whether the original production process ended by exception, manual kill, or
  another interruption; no durable processor log existed then.
- The first production item has not been executed because production remains
  deliberately disabled pending a new backup and separate owner approval.

Verdict: **the historical-session stall and the complete 22-item legacy pending
path are isolated, corrected, logged, and proven on disposable copies**.
Production processing stays off solely because backup/review/approval is a
separate operational decision, not because the failure remains unexplained.

## 5. Watcher restart readiness

Located authority/evidence:

- `src/ck3chronicle/watcher.py`, `harvester.py`, and the `watch` CLI path were
  traced end to end.
- The last watcher heartbeat/process state and pending output history were
  inspected.

Verdict: **the working-tree design is appropriately capture-only, and three
pre-restart defects have been corrected; restart is deliberately deferred**.
The watcher copies only `error.log`, fsyncs and stability-checks that copy,
publishes atomically to pending, and does not process the queue. All six watcher
checks pass through the repository
`.venv`, including the real Windows ACL-inheritance check. One watcher can be
started after the current handoff review and separate explicit startup decision,
without enabling `process-pending`.

## 6. Where did the duplicate/receipt context come from?

Located authority/evidence:

- Git commits `934cd6d`, `af1d583`, `bc94c05`, `e5cee1a`, `76fb2d5`, and
  `bae136e` were inspected alongside the deleted receipt/provenance test and
  report surfaces.
- `docs/BANNED_IDEAS.md` records the exact prohibition and provenance chain.

Verdict: **the poisoning began with a fabricated lifecycle test, not observed
CK3 behavior or an owner requirement**. `934cd6d` simulated two process exits
using the same unchanged fixture; `af1d583` promoted that artifact into a
one-content/many-observation receipt architecture, and later commits propagated
it. The reboot deletes those tests/modules/docs and capture schema v4 removes
the remaining second identity: `sessions.session_id` is the sole Run ID and
`run_metadata` is one-to-one with it. Historical commits remain ordinary audit
evidence; the active branch tip will no longer contain the rejected design once
the reboot is committed and pushed.
