# Task 07 prompt revision — changes for owner review

## Current authority — 2026-09-28

The older review below is historical. Its generation replay, database-wide lineage,
pending cleanup and pending location-stack wording is superseded by the
[current Task 07 prompt](TASK07_PROMPT.md) and
[scope/decision ledger](TASK07_SCOPE_REVIEW.md). Task 06B and 07C are delivered;
Task 07 is not. All completed captures, including failed/unprocessed ones, are now
eligible for raw-log expiry after 30 elapsed days from capture time. Keep the older
review for evidence, not executable instructions.

**Task 07 remains a concise list of five deliverables.**
See the [scope and version inventory](TASK07_SCOPE_REVIEW.md) and
[revised draft](TASK07_PROMPT.md). It delivers ingest and
retention APIs, one manual ingest command, versioned Run/playset storage,
a watcher-team handoff and verification. The watcher team owns both automatic
triggers; retention runs periodically even without ingestion. Earlier rationale
below is historical. Malformed-playset disposition and exact cadence remain open.

## After Task 06B completion — 2026-09-28

Reviewed the cleanup handoff, portable archive README and rollback script against
the cleaned checkout. All 120 recorded actions matched the checkout at review
entry; the recorded before/after payload hashes also matched. Recovery scripts
were inspected but not executed, and the archive was left unchanged.

The [Task 07 draft](TASK07_PROMPT.md) was reviewed at this
checkpoint. Removed completed retirement/relocation instructions, stale
claims about the deleted pending inspector, and repeated warnings about removed
providers. Current matching, storage, playset reception and genuine-input
verification requirements remain.

One functional clarification matters: the surviving `read_capture_metadata`
helper reads historical `manifest.json`. Task 07 now positively specifies reading
the producer's `capture-metadata.json` in its new input reader. The other retained
harvester helpers remain suitable for their named hashing/selection/copy purposes.
No source or package changes were made during this prompt review.

The following sections preserve earlier revision rationale. Cleanup-pending
language there is historical; the current prompt and completed 06B handoff govern.

## Earlier revision rationale

2026-09-28. Compared `TASK07_PROMPT.md` in the supplied
prompt ZIP with both Task 06 handoffs, the watcher active-playset delivery,
current selection and relevant source APIs.
This is a prompt review; Task 07 has not been executed.

Use the [revised Task 07 prompt](TASK07_PROMPT.md).
The owner subsequently authorized [Task 06B cleanup](06B_DEPRECATED_CODE_CLEANUP.md)
before Task 07, including disabling unused old CLI paths. `harvester.py` is retained
and cleaned in place; its relocation requirement came from the older C1/C2 workplan
and is now superseded. Task 07 reuses its helpers and creates no capture module.
Its purpose is protected inputs, capture support, one processor and fresh-generation
replay, now including receipt and Run storage of the watcher-produced playset.

| Change | Rationale |
|---|---|
| Reference both Task 06 handoffs and the selected v45 package (model schema 5, matcher API v2). | The original storage handoff's APIs remain current, but its original package and totals are historical. |
| Replace the emissions/recovery/normalization chain with `read_log` → `classify_raw` → contract preparation → accumulation and `write_run`. | The pinned package and classifier already recover, match and bind. Literal choices must survive unchanged; orchestration must not reprocess them. |
| Require every classifier result to reach `ReviewWriter.observe` exactly once. | Task 06 derives complete accounting from the whole stream, including successful record assignments. Feeding only unmatched results would break integration. |
| Keep Run IDs, two-part shard publication, transaction handling and bounded cleanup in the existing Task 06 implementation. | Task 07 extends that implementation with playset values; it does not invent another storage protocol. |
| Make the preparation-to-parser byte/hash correspondence explicit. | `read_log` rereads the path after preparation. The stored full-file hash must describe the bytes actually processed, as required by the existing duplicate/input contract. |
| Reuse capture/input helpers in `harvester.py`; replace the old F1 extraction port with a JSON receiver. | Relocating working capture is unnecessary. The watcher owns extraction; preserve its debug-copy option, callback and writer in place. |
| Explicitly authorize edits to pipeline schema, repository, review and necessary domain types. | Normalized Run/member rows, an ordered read API and playset serialization into the manifest exceed the earlier two-file interface-fix allowance. This is a bounded expansion for the delivered feature. |
| Version SQL/manifest extensions and use fresh generations. | Task 06 schema 1 has no member table, and its manifest has no playset. Keep diagnostic semantics and the existing completion protocol while extending these formats. |
| Preserve both complete logs and the watcher JSON during preparation/replay. | SQL becomes canonical for reports; retained producer evidence supports replay without consulting today's descriptors or old SQL. Missing playset remains unavailable, not an unmodded Run. |
| Require replayable input provenance and concrete pending/retained paths. | Rebuild must retain known lifecycle/capture facts without importing old SQL. The input metadata and per-Run review manifest serve different purposes. |
| Clarify generation lineage and partial replay results. | Task 06 refuses changed lineage in an existing generation. Replay preserves prior generations and reports earlier accepted Runs honestly if a later input fails. |
| Clarify `--db` as a generation directory; retain the operator-review checkpoint. | Actual storage owns `generation.sqlite3` plus review files under one root. First-generation creation, generation naming and batch failure policy still need a concrete operator proposal, not an implicit default. |
| Replace permissive in-memory/sample checks with complete genuine native evidence and bounded integration checks. | This carries forward the owner's no-synthetics rule. It verifies the new routes and composition without repeating the learner's full campaign. |
| Require a durable Task 07 handoff plus current status/planning updates. | The old prompt explicitly forbade a handoff file. Task 08 needs stable callable interfaces and the owner-reviewed command contract. |

No diagnostic classification, Error Contract, Run-ID format or storage-completion
redesign is proposed. SQL and manifest extensions are now explicitly required for
the playset. The Script location-stack investigation and documented v45 model limits
remain learner work; Task 07 preserves selected outcomes. Task 06B now owns early
source retirement; new application activation remains later.

The operator checkpoint remains substantive: Task 07 must propose explicit initial
generation creation, batch stop/continue behavior and the Run disposition for a
malformed/mismatched completed playset after preparing reviewable work. Missing
templates are already allowed. This revision does not silently equate an invalid
completed template with an absent one or claim the remaining choices are approved.

One retained verification gap needs care: the pinned parser requires a native
header for nonempty input, and Task 06 does not demonstrate a genuine supported
log with no diagnostic emissions. Task 07 must not fabricate such a file or invent
an alternative parser. Carry any native evidence or parser limitation to the
appropriate owner/team without imposing a matched-template requirement on input.

## Watcher handoff quality check and sequencing

Keep the watcher handoff as the producer specification and delivery evidence;
the revised Task 07 prompt is the receiving implementation assignment. They are
linked, with overlapping receiving instructions reconciled here rather than
deleting useful producer knowledge.

Read-only source inspection confirms error-then-debug copying, the pre-publication
callback, watcher-owned extraction, template serialization, expected I/O failure
handling and unchanged error-only manual defaults. The old pending inspector does
reject `playset.json`, as reported. Task 06 schema/repository/review code also
confirms that normalized playset storage and manifest fields are receiving work,
not an already-delivered interface.

Independently checked the handoff's retained native example: both full-log hashes,
joined ID, capture-time agreement, six member fields, consecutive order, and all
132 emitted mount paths in their original order agree. There are 133 members
including base. This check used the actual producer's mount reader and retained
native bytes, with no writes. It did not independently re-resolve descriptor names
or establish a live lifecycle. The watcher's reported 39 checks were not rerun;
their simulated lifecycle/failure checks do not replace this task's real-input rule.

The failure boundary needs precise wording: producer-template absence may mean
historical/manual input or generation failure. The cause is not encoded in
capture metadata; processing must not invent it or require journal reconstruction.
A present malformed/mismatched template is a distinct receiving problem whose
Run-level handling belongs in the explicit operator proposal.

Run Task 06B first. Recommended execution order within Task 07 afterward:

1. Reuse the retained capture interface; implement protected-input and
   version-1 playset reception.
2. Extend Run/member SQL, the ordered read API and derived review manifest under
   the existing completion protocol, using fresh schema/versioned generations.
3. Compose processing and replay through that boundary.
4. Verify paired native evidence and historical error-only evidence; deliver the
   revised storage/API handoff and operator proposal before Task 08.

The watcher delivery is complete and can continue capturing while Task 07 uses
disposable copies. The current handoff records subsequent live activation; the
producer handoff's earlier no-live-operation statements describe its verification
pass. Task 07 must neither disturb that watcher nor send its new pairs through the
old pending inspector. Task 06B removes that obsolete receiver and its command
path; new application activation remains later.

These prompt-review passes changed documentation only. Product code, selected
resources, live watcher and runtime evidence were left unchanged. Task 06B's
implementation handoff will record the actual cleanup separately.
