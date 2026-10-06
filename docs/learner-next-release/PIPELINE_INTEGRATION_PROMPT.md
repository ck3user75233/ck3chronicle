# Pipeline continuation — receive Reporting repairs and finish integration

Receiving and the subsequent R3 packaging correction are complete; see the current
[receipt](PIPELINE_RECEIVING.md#r3-packaging-closed--2026-10-05). The next proposed
owner assignment is [production cutover](PIPELINE_ACTIVATION_PROMPT.md). This
earlier preparation assignment and its hold do not themselves authorize activation.

Updated 2026-10-05 after Data Intelligence's R1/R2/R5 delivery. Resume the existing
Pipeline task. This replaces the earlier intake prompt for work already completed.
Receive the repaired application and finish concrete deployment preparation;
production activation remains a separate owner decision.

## Current position and exact inputs

Checkout: `C:\Users\nateb\Documents\ck3chronicle`. Paths below are checkout-relative.
Read root/applicable `AGENTS.md`, development instructions, current status/handoff
openings, and [Reporting repair delivered](PIPELINE_RECEIVING.md#reporting-repair-delivered--2026-10-05).
Use the current openings of [release README](README.md) and [HANDOFF](HANDOFF.md).
Older open-defect statements below those updates describe the original artifact.
Preserve concurrent work and original receipts.

Your original receiving already passed genuine ingestion, storage, native
reconstruction and unresolved review preservation. Data Intelligence now reports
R1 (repeated-layout reporting), R2 (preserved-byte exports) and R5 (timestamp-based
exclusion from ordinary operations) repaired and verified. Independently receive
that delivery. Keep learner v61/parser v1.8 package **`4ac4e8ee92346e6d14eacfbf`**;
no new learning, model publication or database reset is needed.

For this continuation, **Pipeline owns application packaging and deployment**:
the application wheel, included resources/dependencies, installed defaults,
installation instructions and rollback arrangement. Learner continues to own
immutable learner/model/parser distributions and their pins; Data Intelligence
owns Reporting implementation. This assigns an existing team responsibility,
not a new team or an additional approval stage.
The standing responsibility record is [team governance](../team-governance/README.md).

Repair root **R**: `.codex-tmp/reporting-repair-20261005/`.
Original Pipeline evidence **P**: `.codex-tmp/pipeline-receiving-20261005/`.
Original combined-release evidence **OUT**: `.codex-tmp/combined-release-20261005/`.

- New application: `R/final/application/ck3chronicle-0.0.1-py3-none-any.whl`.
  SHA-256: `3b4b20881233174a1858b4fc960b0318555d0ef9387909ca4584c53772e68890`.
- Artifact/source correspondence: `R/artifact.json` and `R/repair.patch`.
  Six application members changed; retained learner/model/parser distributions,
  catalogs and packaged selection are reported unchanged. The decoder change
  extracts the existing display helper; verify native decoding remains unchanged.
- Producer checks: `R/installed-first/receipt.json`, `R/installed-final/receipt.json`,
  `R/focused-final/receipt.json` and `R/installed-pins.json`.
- Dependency: `OUT/wheelhouse/chardet-7.6.0-cp312-cp312-win_amd64.whl`, SHA-256
  `99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64`.
- Installed selections: `OUT/proposed-selection.json` for the new package;
  `P/rollback-installed-selection.json` for the previous package. Do not use the
  checkout's old `candidates/` selection as installed rollback.

## Receive and prepare

1. Authenticate the new wheel, changed members, retained package pins and
   dependencies. Use a separate clean receiving/staged installation with explicit
   disposable configuration; preserve the original and producer installations.
   Follow the offline installation recipe in the repair receipt. Verify installed
   imports without ambient checkout modules and authenticate the new selection
   and rollback against installed resources.

2. Perform focused receiving through `HandlerClient` and the installed root CLI
   on the **existing disposable database** in `P/database.json`. Inspect the
   supplied checker before running it, choose a fresh output label, and execute it
   with your receiving interpreter from the documented disposable context.
   `R/check_genuine.py --label <fresh-label> --cli` and recorded commands provide
   the receiving path. Do not overwrite `focused-final` or rerun ingestion setup.
   Verify these behaviors and actual output contents:

   - R1: BND9AS/OSPK8G reports in JSON/HTML/text, meaningful repeated templates,
     counts, filters and actual repeated bindings.
   - R2: genuine session-55 native values survive JSON round trips; HTML/text
     display preserved bytes safely. Check the delivered exports and relevant
     appendix behavior within the documented genuine-evidence limits.
   - R5: missing-time XH88PI appears in ordinary Run listings and all-Run message
     searches, and named reports work with/without optional history. Missing
     timestamps affect **only chronological operations**. Do not substitute times
     or drop matching Runs from nonchronological queries, counts or pagination.
   - Old-package DQT13M reporting and package-scoped history remain correct.

3. Reuse valid original ingestion/storage/review and Learner full-corpus evidence.
   Confirm unchanged processing components and native decoder behavior against
   authenticated artifacts; repeat ingestion only if an actual changed dependency
   or receiving failure makes a bounded genuine-input check necessary. Do not
   restart the 73-log build or a broad verification campaign.

4. Own and complete the application installation arrangement, including R3.
   The delivered repair wheel still has the default-path defect. The documented
   explicit selection override is an available deployment arrangement; verify
   and document it, including installed rollback, if retained. Keep any remaining
   wheel defect accountable to Pipeline rather than referring it to an unnamed
   packaging owner. Bounded application packaging corrections are within this
   assignment: if correcting the bundled default/resources, build a new wheel in
   fresh directories, record its new hash/source correspondence, and receive that
   final artifact. Preserve retained learner/model/parser bytes and live selection;
   do not patch or relabel a delivered wheel. Update checks only as warranted by
   the additional packaging change. Verify default loading and rollback against
   the exact final installation.
   R4 new-model syntax selectors remain separately owned Reporting work; preserve
   explicit unsupported-query behavior rather than presenting unavailable counts
   as zero or broadening this task into selector research.

5. Update [PIPELINE_CUTOVER.md](PIPELINE_CUTOVER.md) to the **final wheel and final
   staged environment**; its current artifact paths and defect status predate this
   repair. Refresh relevant runtime observations read-only and document exact
   selections, database/configuration, capture-safe transition, backup/rollback
   and post-switch checks. Old PIDs/heartbeats are historical observations, not
   current process authority. Complete receiving and staging before presenting
   the concrete operational decision to the owner.

## Closure and boundaries

Append your receiving result to [PIPELINE_RECEIVING.md](PIPELINE_RECEIVING.md) and
update current release/status pointers concisely. Separate producer-reported
checks, your independent checks, remaining limitations and readiness to activate.
Report **READY FOR OWNER ACTIVATION DECISION**, or the exact unresolved defect,
impact and accountable owner. Passing producer checks alone do not close receipt.

R2's existing nonblocking disposition stands; do not ask for it again or turn
unrepresented source/appendix cases into new gates. A newly demonstrated regression
must still be reported with its scope. Activation and a naturally completed live
lifecycle remain distinct from disposable receiving.

Keep the existing production database. No live pin/configuration switch, runtime
service restart, production ingestion, reset, backlog reprocessing, commits or
pushes are authorized here. Missing historical facts stay missing. No synthetic
case may be created or executed without specific owner approval for that test;
no mock clients or injected failures are authorized. Do not read the rejected
shared-database-handler design or its continuation instructions.
