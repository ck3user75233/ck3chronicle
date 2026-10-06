# Production cutover — executed 2026-10-05

## Current production database after replacement

The [database replacement](PIPELINE_RECEIVING.md#database-replacement-complete--2026-10-05)
completed on 2026-10-05. Active database/configuration authority:
`.ck3chronicle/wip/runtime/ck3chronicle-schema3-20261005T112504Z.sqlite3` in checkout
`config.toml`. It contains 31 all-new-model Runs; the old active database/review
namespace has been archived only in
`.codex-tmp/pipeline-refresh-20261005/backup-20261005T120734Z/retired-original/`.
Current watcher 51024 (launcher 55312), handler 54908 (launcher 60264), instance
`f474dbf7100a44399e2ae4a6a05f6375`. Final R3 installed environment/package is unchanged.
Natural lifecycle, stored lineage, native reconstruction and reports are verified.
There is no pending switch, ingestion backlog among the 31 readable captures or
legacy fallback. R4 syntax remains Reporting-owned.

The model-cutover instructions below are historical. Their September 28 database
path and process IDs must not be used for current operations. Re-observe current
process/game/request state before any future restart. Backups must never overwrite
newer records. The exact replacement evidence is under
`.codex-tmp/pipeline-refresh-20261005/`.

## Earlier model-cutover record (before database replacement)

**Production is on `4ac4e8ee92346e6d14eacfbf`; no rollback.** The owner assigned
the execution prompt and superseded the prior activation hold for this operation.
The [activation receipt](PIPELINE_RECEIVING.md#production-activated--2026-10-05)
records the verified backup, actual times, process identities and checks.

Checkout selection switched at **09:57:58.533 UTC**; installed watcher launched
at **09:57:58.560 UTC**. Final wheel SHA-256 remains
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`.
Active environment: `.codex-tmp/pipeline-r3-packaging-20261005/deployment`.
Watcher launcher/actual PID: **64756 / 64444**. Handler launcher/actual PID:
**65896 / 47932**, instance `88739409838c4e38936bebc72166ae33`.
Backup: `.codex-tmp/pipeline-activation-20261005/backup-20261005T095647Z/`
(187 files; hash-verified). Existing database/configuration and all 30 stored Runs
are preserved. Installed default needed no replacement.

At 10:01:22 UTC, new heartbeat/handler, normal startup duplicate accounting,
existing-Run JSON/HTML/text reports and evidence preservation passed. R1/R2/R3/R5
receiving remains closed. R4's new-model syntax preset remains unavailable and
Reporting-owned. **New-package live ingestion/lifecycle is pending**: no new
unique capture occurred. Pipeline owns the next natural capture's hash/lineage,
facts/counts/playset/review and report verification detailed in the receipt.

The steps below are the prepared runbook used for this operation, retained for
reproduction and rollback context. Its old process IDs/times and previous-selection
description are historical, not current authority. Do not rerun the switch against
the active service. For any rollback, refresh current process identity and game/
capture state, use the same safe boundary, and authenticate the installed previous
`releases/` selection. Preserve all Runs/captures; never restore the backup over
newer data. Current observations/scripts are in
`.codex-tmp/pipeline-activation-20261005/`; original staged receipts remain intact.

## Exact deployment and rollback inputs

All paths below are absolute after defining `$projectRoot`:

```powershell
$projectRoot = 'C:\Users\nateb\Documents\ck3chronicle'
$ErrorActionPreference = 'Stop'
$receiptRoot = Join-Path $projectRoot '.codex-tmp\pipeline-r3-packaging-20261005'
$originalReceiptRoot = Join-Path $projectRoot '.codex-tmp\pipeline-receiving-20261005'
$wheelFile = Join-Path $receiptRoot 'application\ck3chronicle-0.0.1-py3-none-any.whl'
$releaseRoot = Join-Path $projectRoot '.codex-tmp\combined-release-20261005'
$deploymentRoot = Join-Path $receiptRoot 'deployment'
$deploymentPython = Join-Path $deploymentRoot 'Scripts\python.exe'
$runtimeRoot = Join-Path $projectRoot '.ck3chronicle\wip\runtime'
$databaseFile = Join-Path $runtimeRoot 'ck3chronicle-schema3-20260928T211854Z.sqlite3'
$newSelection = Join-Path $projectRoot 'packaging\models\selection.json'
$oldCheckoutSelection = Join-Path $releaseRoot 'previous-selection.json'
$oldInstalledSelection = Join-Path $originalReceiptRoot 'rollback-installed-selection.json'
$installedSelection = Join-Path $deploymentRoot 'share\ck3chronicle\models\selection.json'
Set-Location -LiteralPath $projectRoot
```

Deployment is a separate CPython 3.12 environment installed offline from the
**final Pipeline R3 wheel** at `$wheelFile`, SHA-256
`7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959`, and supplied
chardet wheel SHA-256
`99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64`.
No development/editable installation or ambient `PYTHONPATH` is used.

The final dormant environment is
`.codex-tmp/pipeline-r3-packaging-20261005/deployment`. All 556 installed code/resource
files exactly match the wheel, including the valid default selection. Default
package/classifier loading and installed rollback authenticate from `C:\Windows`;
all 394 new-package definitions and previous-package definitions render. Installed
`pip check` passes. See `S/artifact.json` and `S/installed-receipt.json` (S is the
new receipt root). **No corrective post-install file replacement is required or
performed. Pipeline closes R3.**

Only the packaged selection differs among code/resource members from the accepted
Reporting wheel. Existing independent genuine handler/CLI results at
`R/pipeline-independent-final/receipt.json` and Q's output checks are reused;
no ingestion or reporting campaign was repeated. R is
`.codex-tmp/reporting-repair-20261005`; Q is the prior
`.codex-tmp/pipeline-reporting-receiving-20261005`. Their artifacts and installations
remain intact. Dist-info also records the root README's concurrent governance link
and the updated RECORD; no application executable changed.

Completed offline installation recipe (use a fresh directory when reproducing;
do not overwrite the verified environment; copy the receipt scripts/artifact/context
to a fresh receipt root first and set `$receiptRoot`, `$wheelFile`, `$deploymentRoot`,
`$deploymentPython` and `$installedSelection` accordingly):

```powershell
if ((Get-FileHash -LiteralPath $wheelFile -Algorithm SHA256).Hash -ne '7239a0c5b89e52f2df1d31028bdbf21b086e3600bf7c079347a1ee4f1d982959') { throw 'Wrong application artifact.' }
$dependencyWheel = Join-Path $releaseRoot 'wheelhouse\chardet-7.6.0-cp312-cp312-win_amd64.whl'
if ((Get-FileHash -LiteralPath $dependencyWheel -Algorithm SHA256).Hash -ne '99bdf02c44a943448e82196ea735bd057a3ecc3e0b9a82dbbeff8f563fd9ae64') { throw 'Wrong dependency artifact.' }
if (Test-Path -LiteralPath $deploymentRoot) { throw 'Use a fresh installation directory.' }
& "$projectRoot\.venv\Scripts\python.exe" -B -m venv $deploymentRoot
if ($LASTEXITCODE -ne 0) { throw 'Environment creation failed.' }
& $deploymentPython -I -B -m pip install --no-index --no-deps $dependencyWheel $wheelFile
if ($LASTEXITCODE -ne 0) { throw 'Installation failed.' }
& $deploymentPython -I -B -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Dependency check failed.' }
Push-Location -LiteralPath 'C:\Windows'
try {
    & $deploymentPython -I -B (Join-Path $receiptRoot 'installed_check.py')
    if ($LASTEXITCODE -ne 0) { throw 'Installed default/rollback check failed.' }
} finally { Pop-Location }
```

The new installed application fingerprint is
`application-source-sha256:64f8a970c935120be483b3b1d5272fc3abe9d581b3d9b9b81a267f6147eeef5d`.
Existing Runs retain their actual original ingestion lineage. Processing components,
model/parser distributions and native decoder AST are unchanged, so original
ingestion/storage/review/full-corpus evidence is reused; no ingestion was repeated
for the Reporting or R3 packaging continuations.

Live checkout selection remains the previous package, hash
`d84ab9e9a1f455a7cb614b8ec9a988865df1ed36d1b68b4142da1706fdfe2e33`.
New package is `4ac4e8ee92346e6d14eacfbf`, pin
`839548e8c8143e01b63059848557dc94e9fe66f5e1924f6026442f7331a8ba9f`.
Previous package is `68f1ae5db205ab46afef9c4d`, pin
`2a84fe9c734a558e757df54649eac0812ea380a80ac8a2d0fe17129d50f24a5f`.
The previous checkout selection uses `candidates/`; installed rollback must use
the separately authenticated `releases/` selection. This resolves deployment
paths without changing either retained executable package or relabeling the wheel.

Configuration remains `$projectRoot\config.toml`; it points to the exact schema-3
database above and existing pending/review roots. The installed watcher must be
started with the **project root as working directory** to use this authority.

## Safe boundary and process identity

Before the authorized operation, refresh `S/observe.py` and `Get-Process` results.
At **2026-10-05 09:44:32 UTC**, watcher PID 30816 and handler PID 23252 were
observed with their October 2 creation times; the handler instance was
`ca3faf45a4514e5cab542769c2a3c70f`. The fresh heartbeat was **absent**: the previously
observed CK3 session had ended naturally. Latest completed Run `20261005-0UM3HN`
uses the old package. Thirty readable pending captures match the 30 stored Runs;
22 older directories remain inaccessible. These are new read-only observations,
not durable process authority; compare creation times from `S/live-processes.json` and
the current heartbeat/hello before addressing any process. If they differ,
refresh the observation and update the concrete target before continuing.

1. If CK3 is running at execution time, wait for it to **exit naturally**. Do not stop it.
   Require a fresh watcher heartbeat with `state: absent`, no `ck3` process, and
   completed publication/ingestion evidence for the ending session. Check the
   protected capture's hash against public `find_run_by_log_hash` / `get_run`.
   Do not infer a completed Run from an unavailable request result.
2. Re-inventory configured pending storage. Account for any new captures and
   active request references; allow in-flight work to reach terminal outcomes.
   Require no active `.copying-*` publication. Preserve every protected capture,
   including not-completed inputs. The 22 previously inaccessible directories
   remain untouched; do not repair permissions or reconstruct them here.
3. With the game absent and capture/ingestion idle, stop only the verified watcher
   process. The current CLI has no shutdown endpoint; this is a bounded OS stop
   at the safe idle boundary, not a claimed graceful KeyboardInterrupt. Do not
   stop all Python processes. Let its venv launcher exit. Recheck game absence.
4. Shut down the **existing handler** through its client, then confirm that the
   old PID/instance and pipe have gone. Never start a competing handler. Reads
   that could auto-start the old handler must cease during this interval.

After the preceding guards and owner authorization, the concrete stop calls are:

```powershell
# This block follows the capture/request-drain checks above.
$heartbeat = Get-Content -LiteralPath (Join-Path $runtimeRoot 'watch\watcher-heartbeat.json') -Raw | ConvertFrom-Json
if ($heartbeat.state -ne 'absent' -or (Get-Process ck3 -ErrorAction SilentlyContinue)) { throw 'Game is active.' }
if (((Get-Date).ToUniversalTime() - [DateTimeOffset]::Parse($heartbeat.timestamp_utc).UtcDateTime).TotalSeconds -gt 90) { throw 'Heartbeat is stale.' }
$observedWatcherPid = [int]$heartbeat.watcher_pid
$priorProcesses = Get-Content -LiteralPath (Join-Path $receiptRoot 'live-processes.json') -Raw | ConvertFrom-Json
$priorWatcher = $priorProcesses | Where-Object Id -EQ $observedWatcherPid
$currentWatcher = Get-Process -Id $observedWatcherPid -ErrorAction Stop
if (-not $priorWatcher -or $currentWatcher.StartTime.ToUniversalTime() -ne ([datetime]$priorWatcher.StartTime).ToUniversalTime()) { throw 'Watcher identity changed; refresh receipt.' }
Stop-Process -Id $observedWatcherPid
Wait-Process -Id $observedWatcherPid -Timeout 10 -ErrorAction SilentlyContinue
if (Get-Process -Id $observedWatcherPid -ErrorAction SilentlyContinue) { throw 'Watcher has not exited.' }

@'
from pathlib import Path
from ck3chronicle.pipeline.request_handler import HandlerClient
c = HandlerClient(Path('.ck3chronicle/wip/runtime/ck3chronicle-schema3-20260928T211854Z.sqlite3'))
assert c._rpc('hello')['instance'] == 'ca3faf45a4514e5cab542769c2a3c70f'
c.shutdown()
'@ | & $deploymentPython -I -B -
if ($LASTEXITCODE -ne 0) { throw 'Handler shutdown did not complete; do not switch.' }
Wait-Process -Id 23252 -Timeout 10 -ErrorAction SilentlyContinue
if (Get-Process -Id 23252 -ErrorAction SilentlyContinue) { throw 'Old handler has not exited.' }
```

The snapshot/inspection script deliberately probes the existing pipe before public
reads. It must not be used during the stopped interval to create a replacement.
Normal request shutdown may reject unfinished preparation; any such input remains
protected and is handled by the existing startup scan/duplicate boundary, never
by a second parallel ingestion loop.

## Selection and start, after authorization and the safe boundary

Make a uniquely named rollback backup of the closed database, its complete review
namespace, configuration, both selections and pending captures/metadata/playsets
before switching. Include the current installed selection in addition to the
previous installed rollback selection. Copy; do not move or expire evidence. No reset is involved.
Keep this backup outside Git. If a game starts during the interval, preserve its
logs and explicitly record that attachment cannot prove an observed full lifecycle.

```powershell
$backupRoot = Join-Path $receiptRoot ('cutover-backup-' + (Get-Date -AsUTC -Format 'yyyyMMddTHHmmssZ'))
New-Item -ItemType Directory -Path $backupRoot -ErrorAction Stop | Out-Null
Copy-Item -LiteralPath $databaseFile -Destination $backupRoot
Copy-Item -LiteralPath (Join-Path $projectRoot 'config.toml') -Destination $backupRoot
Copy-Item -LiteralPath (Join-Path $runtimeRoot 'review') -Destination $backupRoot -Recurse
$inventoryFile = Join-Path $receiptRoot 'live-observation.json'
$inventory = Get-Content -LiteralPath $inventoryFile -Raw | ConvertFrom-Json
Copy-Item -LiteralPath $inventoryFile -Destination $backupRoot
$pendingBackup = Join-Path $backupRoot 'pending'
New-Item -ItemType Directory -Path $pendingBackup -ErrorAction Stop | Out-Null
foreach ($capture in $inventory.pending) {
    if ($capture.status -eq 'inaccessible') { continue } # unknown paths retained in inventory
    if ($capture.status -notin @('stored','not_stored')) { throw 'Unaccounted pending input; resolve before switching.' }
    $copyTarget = Join-Path $pendingBackup (Split-Path -Leaf $capture.path)
    New-Item -ItemType Directory -Path $copyTarget -ErrorAction Stop | Out-Null
    foreach ($captureName in @('error.log','debug.log','capture-metadata.json','playset.json')) {
        $captureFile = Join-Path $capture.path $captureName
        if (Test-Path -LiteralPath $captureFile) { Copy-Item -LiteralPath $captureFile -Destination $copyTarget -ErrorAction Stop }
    }
}
Copy-Item -LiteralPath $oldCheckoutSelection -Destination (Join-Path $backupRoot 'previous-checkout-selection.json')
Copy-Item -LiteralPath $oldInstalledSelection -Destination (Join-Path $backupRoot 'previous-installed-selection.json')
Copy-Item -LiteralPath $installedSelection -Destination (Join-Path $backupRoot 'staged-installed-selection.json')

# The installed selection is already correct from the wheel; verify, do not replace.
if ((Get-FileHash -LiteralPath $installedSelection -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $newSelection -Algorithm SHA256).Hash) { throw 'Staged default changed; re-authenticate before cutover.' }
Copy-Item -LiteralPath $newSelection -Destination (Join-Path $projectRoot 'models\selection.json')

# Suppress ambient module paths in both watcher and its handler child.
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
$env:PYTHONNOUSERSITE = '1'
& $deploymentPython -I -B -c "from ck3chronicle.pipeline.catalog import load_selected_package; p=load_selected_package(); assert p.manifest['package_id']=='4ac4e8ee92346e6d14eacfbf'; print(p.manifest_sha256)"
if ($LASTEXITCODE -ne 0) { throw 'Installed default authentication failed; do not start.' }
$newWatcher = Start-Process -FilePath $deploymentPython `
    -ArgumentList '-I','-B','-m','ck3chronicle.cli','watch' `
    -WorkingDirectory $projectRoot -WindowStyle Hidden -PassThru
```

The watcher starts the sole handler via existing startup submissions. Do not also
run manual ingest or a second watcher. Startup duplicate outcomes for retained
hashes are expected; they are not reprocessing. Do not alter retention settings or
run manual expiry during cutover. Preserve newly published captures throughout.

## Post-switch checks and rollback

- Record new launcher and actual watcher PID, fresh heartbeat, runtime lease,
  handler hello PID/instance, bootstrap log and correlated runtime events. Confirm
  configured database identity remains `ck3chronicle-schema3-20260928T211854Z`.
- Authenticate the installed default and module origins again. On the next
  **naturally completed new unique capture**, public `get_run` must show the new
  package/pin, parser v1.8/hash, matcher v3 and installed application lineage.
  Reconcile counts, facts, playset and review availability. Without such a capture,
  record live new-package ingestion/lifecycle verification as **pending**.
- Read an existing old Run and the new Run through the public handler. Scope Run
  lists/history by package. Check JSON/HTML/text exports, meaningful repeated
  templates and reversible native byte values against the repaired behavior.
  Ordinary listings/searches and named reports must retain missing-time Runs;
  only chronological placement can be unavailable. The new syntax preset remains
  unavailable until R4 is received. Source-reading limitations must not be
  converted into failed known-UTF-8 ingestion.
- If rollback is required, use the same absent-game/capture-drained boundary,
  stop the new watcher, shut down its handler, restore `$oldCheckoutSelection`
  to checkout selection and `$oldInstalledSelection` to installed selection,
  authenticate the previous pin, and start **the verified installed application**
  with the same command above. Its genuine old-package ingestion/report control
  passed. This is a package rollback on a known application, not a recreation of
  the old process's unavailable in-memory code.
- Keep the same database and every new-package Run. Do not restore a database
  backup over newer Runs, delete new captures, create duplicate Run IDs, or replay
  old hashes. Backup restoration/data loss would require a separate decision.

If any further application changes arrive before activation, authenticate their
new artifact identity and repeat only warranted receiving checks before updating
this runbook. Keep original, Reporting-repair and final R3 artifacts immutable.
No additional repair or learner/model build is required. The owner-authorized
cutover above is complete; these historical commands must not be blindly rerun.
