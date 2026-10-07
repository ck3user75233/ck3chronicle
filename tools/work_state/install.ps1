# Installs only the pinned, checkout-local pilot toolchain. Does not initialize
# Trekker or enroll work. Run with all pilot clients stopped.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$pilotSource = 'C:\Users\nateb\Documents\ck3chronicle\tools\work_state'
$pilotStore = 'C:\Users\nateb\Documents\ck3chronicle\.ck3chronicle\wip\tooling\work-state'
$pilotToolchain = Join-Path $pilotStore 'toolchain'
$pilotLock = Join-Path $pilotStore '.access-lock'
$pilotNode = 'C:\Program Files\nodejs\node.exe'
$pilotNpmCli = 'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js'
$pilotOwnedLock = $false
$pilotChildOutstanding = $false
# Keep native arguments free of embedded quotes: Windows PowerShell 5.1 strips
# those quotes when invoking node.exe, unlike newer PowerShell argument passing.
$pilotPlatform = & $pilotNode -p process.platform
if ($LASTEXITCODE -ne 0) { throw 'Node platform detection failed.' }
$pilotArchitecture = & $pilotNode -p process.arch
if ($LASTEXITCODE -ne 0) { throw 'Node architecture detection failed.' }
if ($pilotPlatform -ne 'win32' -or $pilotArchitecture -ne 'x64') { throw 'The pilot requires x64 Windows.' }
$pilotNodeVersion = & $pilotNode --version
if ($LASTEXITCODE -ne 0) { throw 'Node version detection failed.' }
if (-not ($pilotNodeVersion -match '^v(\d+)\.\d+\.\d+$') -or [int]$Matches[1] -lt 18) {
    throw "Node 18 or newer is required; found $pilotNodeVersion."
}
# Invoke the bundled npm CLI explicitly. npm.cmd can redirect to a different
# user-prefix npm installation; record the version actually used, not an
# observation made in another account/session.
$pilotNpmVersion = & $pilotNode $pilotNpmCli --version
if ($LASTEXITCODE -ne 0 -or $pilotNpmVersion -notmatch '^\d+\.\d+\.\d+$') {
    throw "Cannot determine the bundled npm version: $pilotNpmVersion"
}
Write-Output "Installing with Node $pilotNodeVersion and npm $pilotNpmVersion."
New-Item -ItemType Directory -Path $pilotStore -Force | Out-Null
$pilotRetention = Join-Path $pilotStore 'RETAIN-WORK-STATE.txt'
if (-not (Test-Path -LiteralPath $pilotRetention)) {
    @'
RETAIN: canonical CK3Chronicle Trekker pilot work state.
This entire directory is excluded from disposable wip/tooling cleanup.
Do not remove it during runtime, capture, archive, verification or cache cleanup.
All sessions/worktrees use this absolute location and tools/work_state/pilot.mjs.
Do not initialize another store. Back up the complete directory with clients
stopped; see docs/TREKKER_CLI_PILOT_HANDOFF.md. No product runtime belongs here.
'@ | Set-Content -LiteralPath $pilotRetention -Encoding utf8
}
try {
    # New-Item (without -Force) fails if another client owns this directory.
    New-Item -ItemType Directory -Path $pilotLock -ErrorAction Stop | Out-Null
    $pilotOwnedLock = $true
    @{ pid = $PID; host = $env:COMPUTERNAME; startedAt = [DateTime]::UtcNow.ToString('o');
       operation = 'install'; executable = (Get-Process -Id $PID).Path } |
        ConvertTo-Json | Set-Content -LiteralPath (Join-Path $pilotLock 'owner.json') -Encoding utf8
    if (Test-Path -LiteralPath (Join-Path $pilotStore 'incomplete-operation.json')) {
        throw 'An incomplete tracker operation must be reconciled before replacing its toolchain.'
    }
    New-Item -ItemType Directory -Path $pilotToolchain -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $pilotSource 'package.json') -Destination $pilotToolchain
    $pilotLockedManifest = Join-Path $pilotSource 'package-lock.json'
    $pilotInstallMode = 'install'
    if (Test-Path -LiteralPath $pilotLockedManifest) {
        Copy-Item -LiteralPath $pilotLockedManifest -Destination $pilotToolchain
        $pilotInstallMode = 'ci'
    }
    $pilotChildOutstanding = $true
    & $pilotNode $pilotNpmCli $pilotInstallMode --prefix $pilotToolchain --cache (Join-Path $pilotToolchain 'npm-cache') --no-audit --no-fund --fetch-retries=0 --fetch-timeout=20000
    $pilotChildOutstanding = $false
    if ($LASTEXITCODE -ne 0) { throw "Pinned package installation failed ($LASTEXITCODE); pilot is not delivered." }
    $pilotManifest = Get-Content -Raw -LiteralPath (Join-Path $pilotSource 'package.json') | ConvertFrom-Json
    foreach ($pilotDependency in $pilotManifest.dependencies.PSObject.Properties) {
        $pilotInstalledManifest = Join-Path $pilotToolchain ('node_modules/' + $pilotDependency.Name + '/package.json')
        $pilotInstalled = Get-Content -Raw -LiteralPath $pilotInstalledManifest | ConvertFrom-Json
        if ($pilotInstalled.version -ne $pilotDependency.Value) { throw "Pin mismatch: $($pilotDependency.Name)" }
    }
    $pilotBun = Join-Path $pilotToolchain 'node_modules/bun/bin/bun.exe'
    if ((& $pilotBun --version) -ne '1.3.10' -or $LASTEXITCODE -ne 0) { throw 'Bun executable/version not verified.' }
    Copy-Item -LiteralPath (Join-Path $pilotToolchain 'package-lock.json') -Destination $pilotLockedManifest
    @{ recordedAt = [DateTime]::UtcNow.ToString('o'); store = $pilotStore;
       node = $pilotNodeVersion; npm = $pilotNpmVersion; nodeExecutable = $pilotNode;
       npmCli = $pilotNpmCli; dependencies = $pilotManifest.dependencies;
       lockSha256 = (Get-FileHash -LiteralPath $pilotLockedManifest -Algorithm SHA256).Hash;
       state = 'Installed; real protected init/reads and handoff update still required' } |
        ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $pilotToolchain 'installation.json') -Encoding utf8
    Write-Output 'Pinned toolchain installed. Use pilot.mjs versions, then init only for the first store initialization.'
} finally {
    if ($pilotOwnedLock -and -not $pilotChildOutstanding) {
        Remove-Item -LiteralPath (Join-Path $pilotLock 'owner.json') -ErrorAction Stop
        Remove-Item -LiteralPath $pilotLock -ErrorAction Stop
    }
    if ($pilotOwnedLock -and $pilotChildOutstanding) { Write-Warning 'Installer interrupted: lock retained. Inspect child processes before recovery.' }
}
