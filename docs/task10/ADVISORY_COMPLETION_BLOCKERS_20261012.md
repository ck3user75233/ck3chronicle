# Task 10: why completion is stalled

## Subsequent Owner correction — 2026-10-12

The Owner explicitly removes additional Python/ripgrep verification: the existing
local dependencies are known to work. Upstream downloads/comparisons are not
Task 10 prerequisites, and GitHub access is intentionally restricted. **The
earlier download action and upstream-verification blocker below are superseded;
do not execute that action on the authority of this review.** The local
ck3chronicle candidate remains the development authority; no remote application
comparison was required. "Pinned originals" was misleading Advisory wording,
not evidence that local files were invalid or altered.

The issued 10B prompt assigned runtime/dependency versions, hashes and notices;
it did not specifically mandate downloading upstream archives. That was the
producer's chosen verification route, which Advisory incorrectly presented as
an unconditional Owner prerequisite. The [10B](../task10-deliverables/10B_DISTRIBUTION.md)
and [10C](../task10-deliverables/10C_ACCEPTANCE.md) instructions now record the
Owner's disposition. Preserve existing dependencies and included notices, finish
the newly requested manual revision, assemble the final local candidate and
complete installed-product acceptance. Keep normal bundle hashes and original
evidence; no dependency substitution or new provenance campaign is requested.

The following is the earlier dated review, retained with that correction.

Advisory review, 2026-10-12, approximately 07:33 UTC / 15:33 Hong Kong.
Fresh protected tracker retrieval, current handoffs, direct archive/manual checks
and local Git inspection. No implementation, tracker mutation, dispatch, build,
installation, service operation or publication was performed by this review.

## Owner conclusion

The remaining Task 10 work is concentrated in **Launch & Distribution 10B and
10C**. Pipeline's corrected application, the revised manual, Watcher retention
documentation and workflows are received and completed. No new failed product
acceptance check is reported in the latest continuation. Completion is stalled
on upstream acquisition/provenance, final bundle assembly and access to the
required external interactive test environment. Source publication is separately
unfinished in this checkout.

Advisory correction: my earlier advice repeated a secondhand claim that Watcher
owed an already-authorized reconciliation implementation. The original authority
was not established. CMT-160 corrects that claim; CMT-168/169 record the Owner's
explicit deferral of newly discussed ingestion/hash lookup, failed-Run metadata
and retry work until after Task 10. That work is **not a completion prerequisite**.
Do not reissue the earlier Watcher implementation continuation.

## Concrete blockers and the next action

| Finding | What is actually wrong or missing | Accountable next action |
|---|---|---|
| Upstream acquisition failed | The 10B receipt at 2026-10-12 01:31:51 UTC / 09:31:51 HKT records `Unable to connect to the remote server`, with zero acquired assets. The upstream directory currently contains only that receipt. Correspondence of bundled runtime/tools to upstream archives and complete native/Rust notices remains unverified. | A network-capable local session runs the existing download-only script below. **10B / TREK-10** compares the acquired payloads/build metadata, completes notices and records its findings. No new product decision is required. |
| The final combined ZIP does not exist | C10 contains application 0.0.3 but six older manual pages. The exact final manual inputs already exist and authenticate. This is outstanding assembly, not a missing Docs delivery. No later candidate archive was found in the Task 10B artifact tree or current deliveries. | **10B / TREK-10** consumes CMT-149's frozen 10D-r2 inputs and received 0.0.3, then creates a new identified archive with completed provenance/notices, owned installation/release notes, manifest and receipt. Preserve C9/C10. |
| Final installation/console acceptance cannot be completed in the current session | The recorded host is a developer Windows machine, and the session can write only inside the checkout. It cannot demonstrate a clean machine or perform the required outside-checkout installation. Final ordinary-console Ctrl+C and explicit handler stop are still unperformed. This is missing evidence, not an observed stop failure. | **10C / TREK-16** uses the final bundle on an authorized Windows x64 environment with separate state and an ordinary interactive console. Document actual prerequisites and absence of developer dependencies; verify affected journeys and shutdown, reusing valid unchanged evidence. |
| Stale producer instructions cause unnecessary waits | TREK-10's current description and the top continuation in `DISTRIBUTION_HANDOFF.md` still say Watcher and final Docs delivery are pending. Later CMT-149/159/168/170 supersede those waits. Reopening acceptance without the missing bundle/access has produced another evidence checkpoint, not final execution. | **10B** updates its current summary and own handoff on resumption, preserves historical receipts, and proceeds from CMT-170. Do not send the Owner back to Pipeline/Watcher/Docs for already resolved work. |
| Source checkpoint has not been published from this checkout | HEAD and cached origin/main are still Task 09 commit `709ea7842a0202c420b43355b18be91d8ca196a3`; Task 10 changes remain uncommitted. The planned publication handoff is absent. A fresh `ls-remote` failed to connect to GitHub port 443, so the live server head is unknown. | The dedicated **publication assignment** needs a Git-writable, network-capable session. Publish the reviewed source checkpoint under the already prepared prompt. This can proceed separately from final Task 10 acceptance. |

The other workstation could provide the acceptance environment **if its actual
state meets the clean-machine requirement**. Test before installing developer
dependencies when practical. A second PC or a fresh folder alone proves neither
clean-machine compatibility nor native dependency completeness. C9's prior
external installation is valid historical evidence; it is not final C10-or-later
acceptance. No blanket repeat of completed workflows is needed.

### Exact bounded download action

Run this in an ordinary network-capable PowerShell session on this workstation:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'C:\Users\nateb\Documents\ck3chronicle\packaging\windows\Fetch-UpstreamInputs.ps1'
```

I inspected the script: it downloads about 88 MB of three pinned GitHub assets,
hash-checks them and writes an acquisition receipt beneath
`.codex-tmp/task10b/upstream/`. It does not extract, execute, install or activate
them; mismatching/partial bytes are preserved. This review did not execute the
download. A successful download alone does not finish provenance/notices:
10B must perform the payload/build-metadata and notice comparison afterward.

### Bounded continuation for Launch & Distribution

> Resume TREK-10 from latest CMT-170 and later comments, using the protected
> helper. Pipeline 0.0.3 and exact CMT-149/10D-r2 manual inputs are received;
> Watcher is completed and the ingestion redesign is deferred by CMT-168/169.
> Remove those stale waits from your current summary. Finish upstream binary
> correspondence/notices, then build and deliver one new authenticated final
> archive. If acquisition is still unavailable, identify the exact failed
> download and complete independent preparation; do not reissue producer work
> or repeatedly send acceptance back through unchanged checks.

Then **TREK-16** receives that artifact and completes the authorized external
clean-Windows/ordinary-console checks. The final Owner acceptance decision follows
those results. No team was dispatched by saving this review.

## Work that should no longer block completion

| Record | Current state |
|---|---|
| TREK-9 / Pipeline | Completed; application 0.0.3 received CMT-144/148/158, including corrected help and 1,024 completed-result cache. No remaining Pipeline defect in that delivered scope. |
| TREK-11 / Docs | Completed; 10D-r2 delivered CMT-149/150 and received CMT-159. Packaging owns inclusion. |
| TREK-12 / Watcher | Completed; retention prose received CMT-157, later design discussion deferred CMT-168. No runtime implementation delivery is implied. |
| TREK-15 / workflows | Completed against CMT-131; no new guide defect. |
| TREK-7, TREK-13, TREK-14 | Still `in_progress` despite last comments being receipts CMT-80/110/111. L&D design, Reporting and Learner respectively should close their received scope and correct current text. These are administrative tails, not blockers for the final bundle. |
| Trekker itself | Fresh protected reads succeed with `recoveryRequired: null`. The old CMT-132 decoder incident is resolved; no new incomplete operation was observed. |

## What is known about actual software failures

The latest 10C checkpoint CMT-171 reports **no new failed product check or concrete
defect**. C10 has installed command/import/model verification, and prior genuine
C9 processing/reporting evidence is retained with its original identity. That
does not prove final external or clean-machine operation.

The separate incident investigation (CMT-164/165/167) records real historical
handler reachability/submission failures and a September manual-ingest staging
access denial. It distinguishes those from completed-result cache eviction and
classification/SQL failures. In its retained production census, 148
`ingestion_not_completed` observations were duplicate-log outcomes with zero
associated errors. No occurrence of the proposed unavailable-result recovery
branch was found in the inspected journals. These are prior investigators'
findings; I did not rerun their log census or inspect current production in this
review. They do not establish a current production outage or justify silently
adding the deferred ingestion design to Task 10.

## Independent artifact and source observations

Current integration package:
`.codex-tmp/task10b/resume-20261012/build/ck3chronicle-0.0.3-task10b-candidate10-win-x64.zip`.
Fresh SHA-256:
`b4431ccbda13ba9ca69af0c9da38c519f8e166de2d51adc7e955e89699d65c02`.

The frozen manual edition hashes to
`5c7eb0f40faf4e98724d7aaa746875a278fc28e303b7db12d9c6cac005c8c80c`;
all 13 document inputs still match their recorded pins. Direct ZIP comparison
finds older bytes for `CLI_REFERENCE.md`, `CONFIGURATION_REFERENCE.md`,
`INSTALLATION.md`, `README.md`, `RELEASE_REFERENCE.md` and
`REPORT_QUERY_REFERENCE.md` under `docs/user/`. This report does not claim a new
full-package execution or a fresh check of all 1,503 payload members.

Fresh tracker snapshots and `artifact-review.json` are preserved under
`.codex-tmp/advisory-task10-20261012/`. Current technical sources are
[10C receiving](../TASK10_HANDOFF.md),
[10B handoff](DISTRIBUTION_HANDOFF.md),
[Docs handoff](DOCUMENTATION_HANDOFF.md), and
[the publication prompt](../task10-deliverables/SOURCE_CHECKPOINT_PUBLICATION_20261011.md).
No protected state, original receipt or component-authored handoff was overwritten.
