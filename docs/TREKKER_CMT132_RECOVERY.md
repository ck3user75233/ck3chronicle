# Trekker CMT-132 recovery and decoder repair

2026-10-10, Asia/Hong_Kong. Owner explicitly assigned recovery of the committed
TREK-9 CMT-132 and investigation/repair of the output decoder. **Resolved.**
CMT-132 was not replayed, changed or deleted. No raw CLI/SQL, alternate store,
dependency upgrade, product runtime action or Git publication was used.

## Failure and cause

The October 8 protected `comment TREK-9` call committed CMT-132, then failed while
decoding its response: `Expected 10 inline array items, but got 18`. The helper
correctly retained its incomplete-operation marker and blocked subsequent writes.
The empty `completedSteps` array meant response decoding had not completed; it
did not mean the database write had rolled back.

Protected `task-show TREK-9` confirmed one exact author/content match to the saved
request. A new protected `history CMT-132` reproduced the same decoder failure
without writing anything. Offline encode/decode of the genuine saved comment also
reproduced the exact exception.

Pinned TOON 2.1.0's `parseArrayHeaderLine` searches the entire object-field line
for `[` when its key is unquoted. It scans past `content:` into the already quoted
value beginning `[10C cache receiving disposition]`. Its bracket parser accepts
the leading `10` as a length and treats later prose/commas as array data. Quoting
the value was already correct; the problem is the decoder's header recognition.
Nested history snapshots have the same exposure. Tabular comment-list reads could
succeed, explaining why the saved comment was visible despite the add failure.

## Repair

`tools/work_state/toon_output.mjs` quotes simple object keys in the CLI's TOON
output before passing it to the same pinned decoder with **strict mode enabled**.
Quoted keys select its quote-aware parsing branch, which correctly sees the colon
after the key instead of a following array header. `pilot.mjs` uses this adapter
for all command responses, including nested history output.

Values, real array headers, tabular rows, persisted records, dependency pins and
existing mutation/read-back checks are unchanged. No permissive decoder fallback
or automatic retry/marker clearing was added. The helper remains the sole tracker
access route. Keep the new module alongside `pilot.mjs` when preserving helper
source; it is not an alternate tracker client.

## Reconciliation performed

- Fresh protected reads confirmed CMT-132 once with exact intended author/content.
  After the adapter repair, protected history returned its single create event
  **256**, timestamp **2026-10-08T20:43:46Z**.
- Fresh OS inventory showed **no Node/Bun/npm/npx processes** and no access lock.
  The previously uncertain Node PID 20648 was no longer present. CIM command-line
  access remained denied; no unidentified live client was ignored or stopped.
- Acquired the canonical `.access-lock` exclusively with maintenance owner
  metadata. Rechecked the exact pending token and operation; copied and SHA-256
  verified the original marker in canonical retained recovery storage. Only then
  removed the reconciled original marker and released this operation's lock.
- Archive: `.ck3chronicle/wip/tooling/work-state/recovery/CMT-132-20261010T113212Z/`.
  Its `reconciliation.json` records the original marker hash and evidence path.
- Refreshed affected records before performing only the outstanding handoff work.
  Original prepared requests remain intact; new requests clearly distinguish
  prior 10C receiving from this chat's tooling repair.

| Record | Completed recovery action |
|---|---|
| TREK-9 | **CMT-133** documents this repair; original CMT-132 remains exactly once. Application help/reference follow-up remains open. |
| TREK-12 | **CMT-134** posts the previously prepared 10C coordination of existing CMT-122 work. No new implementation commission. |
| TREK-15 | Updated to **completed**, implementing already-saved 10C receipt CMT-131. Final distribution acceptance remains TREK-16. |
| TREK-16 | Updated current description and posted **CMT-135**, preserving prior receiving limits and recording resolved tooling recovery. Remains **in_progress**. |

All five protected mutations completed their normal read-back with no pending
marker. CMT-129/130/131/132 were not repeated. Task 10's remaining product and
distribution obligations were not declared complete by this tooling repair.

## Verification and retained evidence

Run offline regressions with:

```powershell
& 'C:\Program Files\nodejs\node.exe' --test tests/work_state/toon_output.test.mjs
```

Four tests pass using genuine saved CMT-132/comment-list/native-history data:
original pinned-decoder failure, exact comment preservation, tabular list
preservation and nested history preservation. No test creates tracker records.
Helper/module syntax checks pass. Actual protected history reads and the five
required writes above verify the repaired integration on the canonical store.

Ignored evidence: `.codex-tmp/trekker-recovery-20261010/` includes original/fresh
protected reads, reproduced TOON text, decoder verification, process observation,
marker reconciliation, prepared recovery requests and actual write receipts.
The original `.codex-tmp/task10c/` incident/request evidence is preserved.

This repair addresses the observed TOON ambiguity. It does not claim exhaustive
TOON conformance or test interrupted writers/concurrent clients. The existing
fail-closed marker and manual stopped-client recovery requirements remain in force.
