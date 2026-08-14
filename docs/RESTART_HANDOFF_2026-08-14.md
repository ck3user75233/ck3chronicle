# Restart handoff — 2026-08-14

Recorded at approximately 2026-08-14 20:45 Asia/Hong_Kong so the current
Codex task and the PC can be stopped without relying on conversation memory.

## Source checkpoint

- canonical repository: `C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle`
- working branch: `codex/ck3chronicle-reboot`
- handoff parent commit: `683eb11f2c5ffa8a305d2938ab9461b19db7c069`
- isolated documentation worktree branch: `codex/ck3chronicle-phase1-exit`
- last verified reboot-owned fast suite: 86 passed
- phase truth: reboot-planning Phase 0 is complete; Product Phase 1 is active
  and has not passed its independent exit gate; Product Phases 2–6 have not
  been entered

The current executable release-test boundary is intentional. Implementation
agents may document callable functions, CLI commands, schemas, inputs,
outputs, and side effects. They must not author, edit, or run the executable
Phase 1 exit harness, its fixtures or mutations, private holdout selection, or
scorer code. The independent roles and implementation handoff are defined in
`PHASE1_EXIT_PROTOCOL.md` and `PHASE1_EVALUATION_INTERFACE.md`.

## Runtime state at shutdown handoff

- CK3 was not running.
- watcher process PID 25912 was still running and responsive.
- the watcher is a foreground/manual-start facility; it will stop at PC
  shutdown and must be started again after login.
- the running watcher predates the newest committed watcher code. Restarting
  it is required before the bounded-heartbeat/cleanup changes take effect.
- the 2026-08-14 19:51 local process-exit capture is protected at:
  `C:\Users\nateb\AppData\Local\ck3chronicle\pending\20260814T115119.168267Z-9y_jx3_5`
- that pending capture has not yet been finalized, registered, parsed,
  classified, or reported. It must not be copied again or deleted.
- its approved files include `error.log` (299,380 bytes), `debug.log`
  (21,431,997 bytes), `game.log` (36,587 bytes), and the three auxiliary logs.

Safe first commands after restart, from any PowerShell working directory:

```powershell
& 'C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle\.venv\Scripts\ck3chronicle.exe' process-pending
& 'C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle\.venv\Scripts\ck3chronicle.exe' audit-db
& 'C:\Users\nateb\Documents\CK3 Mod Project 1.18\ck3chronicle\.venv\Scripts\ck3chronicle.exe' watch
```

Run `process-pending` before starting another CK3 game. Start `watch` before
starting CK3 if lifecycle observation is to be tested. `watch` remains a
foreground process; automatic login startup is not released.

## Crash evidence decision

Recent crash-folder `error.log`, `debug.log`, and `game.log` files were compared
with the normal watcher copy using exact SHA-256 hashes. The three files matched
byte-for-byte for both observed recent crashes:

- crash `ck3_20260814_192020` matched finalized evidence bundle
  `ead9ddf088dcfef37716421a165c53264d2b89f29783e65a5b61c211460c49b6`;
- crash `ck3_20260814_195110` matched the protected 19:51 pending capture.

Therefore the normal copy-first watcher already preserves the crash-generated
log bytes. Do not add a second unconditional copy of identical crash-folder
logs. What is missing is provenance: the database must record that a run ended
in a crash and that a timestamped source file came from, or is exactly equal
to, the corresponding crash snapshot.

Crash is a property of a run, not of a content-addressed evidence bundle.
Identical bytes may be observed after both a normal exit and a crash. The next
run-identity design should therefore include:

- a durable run/observation identity linked to the deduplicated evidence
  bundle;
- termination kind (`normal`, `crash`, or `unknown`);
- a crash event containing folder identity and association evidence;
- per-run file origin (`live_normal`, `live_after_crash`, or
  `crash_snapshot`) and exact/different/unavailable equivalence;
- parsed-block provenance through the exact archived source-file row.

On exit, the watcher must continue copying the live logs first. Crash-folder
discovery and hash comparison may happen afterward. Preserve a crash-folder
copy only when its bytes differ from the protected live copy.

## Next implementation sequence

The immediate checkpoint is still Phase 1 architecture, not resolver work:

1. Separate durable run identity/chronology from deduplicated evidence-bundle
   identity, including the crash provenance described above.
2. Make runtime `Mounted Data:` provenance exact and store explicit
   complete/partial/absent/malformed/truncated/ambiguous states. Keep
   authoritative mount order separate from optional inventory enrichment.
3. Replace all-in-memory parse accumulation with memory-bounded staged or
   batch persistence while retaining transactional replacement guarantees.
4. Reconcile the semantic model/oracles and add the PostValidate boundary:
   assign a contract first; then validate key, locator, and structured slots;
   invalid L2 extraction falls back to L1 or unknown rather than inventing a
   contract.
5. Make `process-pending` the canonical public vertical slice, retire the
   obsolete `analyze --logs` expectation, and define one versioned command
   success/error envelope.
6. Make `latest` select the newest reportable run and freeze stable text/JSON
   report projections.
7. Freeze the resulting candidate, then hand it to the independent evaluator
   roles. Implementation agents do not create the executable exit tests.

On-action/culture resolvers, full override-chain diffs, broad Git/mod update
context, automated fixability scoring, MCP integration, and the claim journal
product are not prerequisites for the Phase 1 exit.

## Product direction retained for later phases

The claim journal remains the north-star workflow. A patching agent should be
able to submit an immutable claim identifying the baseline run, exact semantic
contract/template IDs and model version, expected reduction, patch file,
line/hunk evidence, before/after hashes, commit, and diff. After a comparable
follow-up run, ck3chronicle should publish an immutable reply of fixed,
partially fixed, unchanged, worse, or inconclusive, with exact counts and any
new errors associated with the patch file. Causation language requires A/B or
rollback evidence; otherwise the product should say newly observed and
associated, not spawned by the patch.

