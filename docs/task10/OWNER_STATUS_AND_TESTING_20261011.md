# Task 10: remaining work and testing the available package

Owner direction, 2026-10-12: defer the newly discussed ingestion/hash-lookup,
failed-Run metadata and retry changes until Task 10 is complete. The initial
reconciliation-authority question is withdrawn; the proposed Watcher lookup
does not run in the delivered application and is not a Task 10 acceptance
requirement. No ingestion design decision is needed to finish Task 10.

This dated review is superseded for current state by
[Task 10 receiving](../TASK10_HANDOFF.md): Pipeline 0.0.3 and
10D-r2 are received; final 10B provenance/notices/manual inclusion
and 10C external clean-Windows/ordinary-console checks remain.
The earlier Watcher reconciliation action below is historical.

Latest 10C retrieval, 2026-10-12: **CMT-135/169** and current producer records
still contain no final combined archive. **TREK-10 / CMT-170** now records its
remaining provenance/notices/manual-inclusion action and the Owner's deferral
of the Watcher discussion. Prior acceptance remains preserved. Windows x64,
PowerShell 5.1 and Windows Forms/.NET are observed on the current developer host;
Git/Node/development Python are present, so this is not clean-machine evidence.
Final external installation and ordinary-console stopping remain **TREK-16**
work in an environment that permits them; this session allows checkout writes
only. See the receiving handoff for exact observations and evidence.

Advisory review, 2026-10-11, approximately 10:40 UTC / 18:40 Hong Kong.
Prepared against fresh protected Trekker reads, current handoffs, local Git state
and the actual C9 archive. This review changes no tracker records or runtime state.

Task 10 is **usable for a C9 trial, but not ready for final Owner acceptance**.
The tracker recovery is complete. The remaining substantive work is the owning
Pipeline/Watcher corrections, final distribution provenance/manual integration,
and acceptance of that final bundle. Several `in_progress` records only need
administrative closure; they are not missing implementations.

## What each team still needs to do

| Owner / record | Already delivered or received | Exact remaining action and dependency |
|---|---|---|
| Launch & Distribution: 10A design, TREK-7 | Corrected first-use design received in CMT-80 | Close the received design record and correct its stale current description. No additional design obligation found. TREK-8 is the archived duplicate; do not revive it. |
| Pipeline: 10A.1, TREK-9 | Initial application received CMT-83. The 1,024-result cache source/wheel delivered CMT-126 and technically received CMT-132; recovery recorded CMT-133 | Finish CMT-106: correct `ingest --package-id` help to describe saved configured model selection, and reconcile the GUI confirmation wording in `docs/user/PIPELINE_REFERENCE.md` with the accepted C9 wizard. Incorporate received Watcher application changes through the owning source/artifact process. Deliver the resulting authenticated application wheel/reference to 10B/10D and obtain receipt. Do not redo the received cache change. |
| Watcher: TREK-12 | Original technical reference received CMT-109 | Finish CMT-122/CMT-134: correct the r1 handoff's advice to disable retention; enabled retention with ingestion disabled is an intentional supported choice. Identify and deliver the already Owner-requested unavailable-request-result reconciliation using persisted Run metadata and full log hash. No replacement implementation/delivery was found. Supply exact source/evidence to Pipeline and Docs; do not describe the requested behavior as shipped. |
| Launch & Distribution: 10B distribution, TREK-10 | C9 actual external GUI/setup receipt CMT-91; partial receiving CMT-129 | Finish CMT-127/CMT-129: establish upstream runtime/tool binary correspondence and complete native dependency notices; consume the received next application and final manual; build a **new identified archive**, manifest and hash receipt. Deliver to 10C. A prepared acquisition script is not completed provenance verification. Preserve C9 unchanged. |
| Launch & Distribution: 10D manual, TREK-11 | Canonical manual received as usable review edition, CMT-130 | Correct stale coverage-handoff wording that says the 1,024-result producer delivery is missing (CMT-126/CMT-132 now exist). Keep the accurate C9=256 statement until describing a different bundle. Receive owning Pipeline/Watcher reference corrections, identify the final manual edition/hashes and hand them to 10B. The complete manual still needs inclusion in the final archive. |
| Reporting / Data Intelligence: TREK-13 | Technical contribution received CMT-110 | Close the received contribution and replace stale pending-receipt current text. No outstanding producer repair found. Return only a concrete later defect to this owner. |
| Learner: TREK-14 | Technical contribution received CMT-111 | Close the received contribution and replace stale pending-receipt current text. No new model, training or retained-release change is required by the outstanding packaging work. Storage reclamation is separate work. |
| Launch & Distribution: 10E workflows, TREK-15 | Received CMT-131; now **completed** following recovery | No outstanding guide defect. Retain the received content and its evidence; any actual replacement-edition correction returns to this record. Final bundle/environment receiving belongs to TREK-16. |
| Launch & Distribution: 10C acceptance, TREK-16 | Partial genuine receiving and its limits recorded CMT-135 and the Task 10 handoff | Receive the final archive/manual and affected corrections; verify an authorized isolated installation physically outside the checkout, clean-Windows prerequisites/native dependencies, and ordinary-console Watcher Ctrl+C plus handler stop. Reuse unchanged genuine evidence with its original identity; repeat only checks affected by changes. Produce final acceptance recommendation for the Owner. |

Task 09 / TREK-6 remains completed; its completion excludes live activation.
The source checkpoint requested today does not reopen Task 09 or finish Task 10.
No unified shard/diagnostic view, flattened export, NiceGUI implementation or new
training exercise is added to the issued scope.

### Recommended continuation order

1. Resume **Pipeline TREK-9 (CMT-106/126/132/133)** and **Watcher TREK-12
   (CMT-122/134)** for their existing owning corrections. In parallel, L&D can
   finish 10B provenance/notices and 10D's factual handoff correction.
2. Pipeline delivers the corrected application containing the received owning
   changes. Docs freezes the matching manual. **10B** builds and authenticates
   one replacement bundle containing those exact inputs.
3. **10C TREK-16 (CMT-135)** receives that bundle and finishes the outstanding
   installation/environment/ordinary-stop evidence; the Owner then decides
   acceptance. Close TREK-7/13/14 on their existing receipts independently.

These are continuations of existing assignments, not new dispatches. Teams should
retrieve the cited comments and linked handoffs themselves. Source publication,
hosted release publication and live activation remain distinct actions.

## Package available to test now

The latest located archive is **Windows x64 candidate 9**, about 20.9 MB:

`C:\Users\nateb\Documents\ck3chronicle\.codex-tmp\task10b\build\ck3chronicle-0.0.2-task10b-candidate9-win-x64.zip`

Freshly recomputed archive SHA-256:

```text
db1ed81f050e13c93652681e829c18ef282a92965c116aee0fc59cea49eedfc1
```

The C9 manifest hashes to
`066ae6f7378372074c575cd9c5c8e75257c809ec65575526a0fee7979f9f4aa5`.
Its application wheel is
`2de516e02aae2e858f1b2f2d34a5ec89ba69306e7001477c29d1857d9ffbd594`
(version 0.0.2, 256-result cache). The newer, technically received 1,024-result
wheel is separately at
`.codex-tmp/pipeline-cache-1024/application/ck3chronicle-0.0.2-py3-none-any.whl`,
hash `94987fb06eeac685eb5b57a87edc41e58da1df9730ff8bf15ba7a023750ab489`.
That newer wheel has **not** been incorporated into C9. Do not replace the wheel
inside the authenticated archive by hand.

C9 has a dated actual external-install receipt (2026-10-08T12:02:56Z), including
GUI setup, private Python/ripgrep and 1,492 authenticated files. The recorded
external installation is
`C:\Users\nateb\AppData\Local\Programs\ck3chronicle-task10-c9`.
That is a test installation, not proof of production cutover. This review did not
reinspect or launch that external copy. Later 10C receiving exercised genuine
input, reports, queries, repeat setup and external SQLite against an isolated
C9 installation; Run `20261008-3WKDZ4` had 1,066 diagnostic records and 1,838
occurrences. Those are existing receipts, not tests rerun in this review.

The ZIP contains only the early Distribution/Pipeline references and Pipeline
handoff, **not the complete current manual**. Use the repository's
[manual index](../user/README.md), [installation instructions](../user/INSTALLATION.md)
and [workflows](../user/WORKFLOWS.md). Copy `docs/user/` separately if testing
before the source checkpoint is pushed/cloned. Provenance/notices and final
clean-machine/console-stop acceptance remain incomplete.

### Isolated trial on the other workstation

Copy the ZIP separately from Git. Check its hash with `Get-FileHash -Algorithm
SHA256 -LiteralPath '<downloaded ZIP path>'`, then extract the whole archive to a
new folder outside the checkout. Open PowerShell in the extracted folder that
contains the CMD files. These commands are instructions for the Owner; they were
not executed by this review:

```powershell
.\Verify.cmd
$testState = Join-Path $env:LOCALAPPDATA 'ck3chronicle-c9-test'
.\Setup.cmd --config "$testState\settings\paths.toml" --data-root "$testState\data"
.\Start.cmd --config "$testState\settings\paths.toml"
# Play CK3 normally and let it exit normally.
# Stop the foreground watcher with Ctrl+C and wait for it to return.
.\ck3chronicle.cmd --config "$testState\settings\paths.toml" runtime-stop
```

Setup's final **Save settings** commits the choices. Check the suggested CK3/log
folders and keep the isolated test storage. Start launches the Watcher, not CK3;
it can process pending captures and apply configured raw-log retention. The
handler is independent, hence the explicit final `runtime-stop`. Avoid observing
the same live CK3 session with a second watcher on the current workstation.

The bundle supplies Python/chardet/ripgrep. Windows PowerShell 5.1 and the Windows
.NET Framework desktop components are required for its GUI. CK3 and its logs
directory must exist; a current `error.log` is not a setup prerequisite. A doctor
exit 2 can mean write access is deliberately unverified; read the actual finding.

Testing before installing Python/Git/developer dependencies on the other machine
could provide useful clean-machine evidence. Record the actual environment,
archive hash, commands and results. A second PC alone is not proof of a clean
environment, and a successful C9 trial does not accept an as-yet unbuilt final
bundle.

## Source transfer to the other workstation

The local `main` and cached `origin/main` still identify Task 09 commit
`709ea7842a0202c420b43355b18be91d8ca196a3`. A live `ls-remote` attempt failed to
connect to GitHub; this review cannot assert the current server head. Before these
two Advisory documents, the checkout contained 22 modified tracked files and 55
untracked files. Task 10 code, manual, Windows build recipe and tracker decoder
repair therefore need deliberate source publication.

Use the [ready-to-issue publication prompt](../task10-deliverables/SOURCE_CHECKPOINT_PUBLICATION_20261011.md).
It authorizes the new task to publish a reviewed **source checkpoint**, with
unfinished Task 10 work disclosed. It does not request a final release tag,
hosted binary upload or activation.

Git will not transfer `.codex-tmp/` (including C9), local configuration, production
history or the canonical Trekker store. Preserve the already tracked pinned
model/Learner resources as bytes. The new workstation must not initialize an
alternate Trekker history merely because the canonical local store is absent.

## Evidence and limits

Fresh protected `team-state advisory`, `task-list` and relevant `task-show` outputs
are preserved in `.codex-tmp/advisory-task10-20261011/`, alongside `package.json`.
They report `recoveryRequired: null`; the latest relevant comments are the receipts
and recovery continuations cited above. Tracker descriptions were not overwritten.
Archive hash/member inspection and local Git inspection were performed; package
execution, clean-machine testing, remote publication and production inspection
were not performed in this review.

Technical continuation sources:
[Task 10 handoff](../TASK10_HANDOFF.md),
[Pipeline handoff](PIPELINE_HANDOFF.md),
[distribution handoff](DISTRIBUTION_HANDOFF.md),
[documentation handoff](DOCUMENTATION_HANDOFF.md),
[Watcher contribution](WATCHER_DOCUMENTATION_HANDOFF.md),
[workflow handoff](WORKFLOWS_HANDOFF.md), and
[tracker recovery](../TREKKER_CMT132_RECOVERY.md).
