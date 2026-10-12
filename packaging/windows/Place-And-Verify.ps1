[CmdletBinding()]
param(
    [string]$Destination,
    [string]$StateRoot = (Join-Path $env:LOCALAPPDATA 'ck3chronicle-task10-acceptance'),
    [string]$CaptureDirectory,
    [switch]$VerifyRepeatSetup,
    [switch]$InspectOnly
)
$ErrorActionPreference = 'Stop'
$control = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'TRANSFER.json') -Raw | ConvertFrom-Json
$source = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'ck3chronicle'))
$checkout = [IO.Path]::GetFullPath($control.checkout).TrimEnd('\')

function File-Sha256([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hasher.ComputeHash($stream))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose(); $stream.Dispose() }
}

function Is-Within([string]$Path, [string]$Root) {
    return $Path.Equals($Root, [StringComparison]::OrdinalIgnoreCase) -or
        $Path.StartsWith($Root.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)
}
function Assert-PhysicalPath([string]$Path) {
    if (-not [IO.Path]::IsPathRooted($Path) -or $Path -notmatch '^[A-Za-z]:\\') {
        throw "Use a full local drive path: $Path"
    }
    $cursor = [IO.Path]::GetFullPath($Path)
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            $entry = Get-Item -LiteralPath $cursor -Force
            if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Reparse/junction paths require separate physical-location review: $cursor"
            }
        }
        $parent = Split-Path -Path $cursor -Parent
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
}
function Assert-Bundle([string]$Root) {
    $manifestPath = Join-Path $Root 'release-manifest.json'
    if ((File-Sha256 $manifestPath) -ne $control.manifest_sha256) {
        throw 'Bundle manifest differs from the pinned transfer candidate.'
    }
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    foreach ($member in $manifest.files.PSObject.Properties) {
        $path = [IO.Path]::GetFullPath((Join-Path $Root $member.Name))
        if (-not (Is-Within $path $Root)) { throw 'Manifest member escapes bundle.' }
        if ((File-Sha256 $path) -ne $member.Value) {
            throw "Candidate file mismatch: $($member.Name)"
        }
    }
    $count = @(Get-ChildItem -LiteralPath $Root -Recurse -File -Force).Count
    if ($count -ne (@($manifest.files.PSObject.Properties).Count + 1)) { throw 'Unexpected bundle files.' }
    Write-Host "Authenticated $count files: $($manifest.label)"
}

Assert-PhysicalPath $source
$checkScript = Join-Path $PSScriptRoot 'external_check.py'
if ((File-Sha256 $checkScript) -ne $control.external_check_sha256) {
    throw 'External check script differs from the pinned transfer.'
}
$bundle = $source
if ($Destination) {
    $bundle = [IO.Path]::GetFullPath($Destination).TrimEnd('\')
    Assert-PhysicalPath $bundle
    if (Test-Path -LiteralPath $bundle) { throw "Destination already exists; choose a new folder: $bundle" }
}
$state = [IO.Path]::GetFullPath($StateRoot).TrimEnd('\')
Assert-PhysicalPath $state
if ((Is-Within $bundle $checkout) -or (Is-Within $checkout $bundle)) {
    if (-not $InspectOnly) { throw 'Move this transfer folder outside the checkout, or pass -Destination with a new external folder.' }
    Write-Host 'InspectOnly: candidate remains inside checkout; external placement is NOT verified.'
}
if ((Is-Within $state $checkout) -or (Is-Within $checkout $state) -or
    (Is-Within $state $bundle) -or (Is-Within $bundle $state)) {
    throw 'StateRoot must be physically outside checkout and separate from the installed bundle.'
}
Write-Host ''
Write-Host 'CK3Chronicle installation'
Write-Host "Application folder: $bundle"
if ($Destination) {
    Write-Host 'This location was supplied by -Destination in the command you ran.'
    $userPrograms = [IO.Path]::GetFullPath((Join-Path $env:LOCALAPPDATA 'Programs'))
    if (Is-Within $bundle $userPrograms) {
        Write-Host 'It is in the Programs folder for your Windows account, outside the developer checkout.'
    }
    Write-Host 'The bundled application and its Python runtime will be copied here.'
} else {
    Write-Host 'You chose this location by moving or extracting the application folder here.'
}
Write-Host "Settings and saved runs: $state"
Write-Host 'This separate folder is for this fresh verification setup; existing setups are left alone.'
Write-Host 'First we verify the application files. Then setup will ask for your CK3 folders.'
Assert-Bundle $source
if ($InspectOnly) {
    Write-Host 'Read-only inspection complete. No placement, setup or external execution performed.'
    return
}
# A new state root avoids touching any existing user/production data. Preserve it on failure.
if (Test-Path -LiteralPath $state) { throw 'StateRoot already exists; choose a fresh acceptance-state directory. Existing contents were preserved.' }
if ($Destination) {
    New-Item -ItemType Directory -Path $bundle | Out-Null
    Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $bundle -Recurse
    Assert-Bundle $bundle
}
New-Item -ItemType Directory -Path $state | Out-Null
Write-Host ''
Write-Host "Installation ready: $bundle"
Write-Host "Setup opens next. Its settings will be saved under: $state"
$receiptPath = Join-Path $state 'placement-receipt.json'
$receipt = [ordered]@{
    started_utc = [DateTime]::UtcNow.ToString('o'); bundle = $bundle; state = $state
    source_checkout = $checkout; manifest_sha256 = $control.manifest_sha256
    physically_external = $true; copied_by_script = [bool]$Destination
    status = 'placement verified; setup/checks pending'; clean_machine = $false
    repeat_setup_requested = [bool]$VerifyRepeatSetup
    repeat_setup_verified = $false
}
function Save-Receipt { $receipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $receiptPath -Encoding UTF8 }
Save-Receipt
try {
    $config = Join-Path $state 'settings\paths.toml'
    $data = Join-Path $state 'data'
    Write-Host 'This is a fresh setup with separate data. Choose each CK3 folder and accept it individually.'
    & (Join-Path $bundle 'Setup.cmd') --config $config --data-root $data
    if ($LASTEXITCODE -ne 0) { throw "Guided setup returned $LASTEXITCODE; preserve effects and inspect before retrying." }
    $argsForCheck = @('-I', '-B', '-X', 'utf8', $checkScript, '--bundle', $bundle, '--state', $state)
    if ($CaptureDirectory) { $argsForCheck += @('--capture-directory', [IO.Path]::GetFullPath($CaptureDirectory)) }
    & (Join-Path $bundle 'runtime\python.exe') @argsForCheck
    if ($LASTEXITCODE -ne 0) { throw "Installed checks returned $LASTEXITCODE; see evidence and verification.json." }
    if ($VerifyRepeatSetup) {
        Write-Host 'Setup and installed checks passed. You requested an additional repeat-setup test.'
        Write-Host 'This checks that saved data survives setup again; it is not a repair or a required installation step.'
        Write-Host 'Keep paths/model and affirm each external root again.'
        & (Join-Path $bundle 'Setup.cmd') --config $config --data-root $data
        if ($LASTEXITCODE -ne 0) { throw "Repeat setup returned $LASTEXITCODE." }
        & (Join-Path $bundle 'runtime\python.exe') -I -B -X utf8 $checkScript --bundle $bundle --state $state --check-repeat
        if ($LASTEXITCODE -ne 0) { throw "Repeat preservation check returned $LASTEXITCODE." }
        $receipt.repeat_setup_verified = $true
    }
    Assert-Bundle $bundle
    $receipt.status = 'external placement and bounded installed checks passed; see verification.json for untested items'
    $receipt.finished_utc = [DateTime]::UtcNow.ToString('o')
    Save-Receipt
    Write-Host "Receipt: $receiptPath"
    Write-Host 'The watcher was not started. Existing setups were left unchanged. Clean-machine verification remains separate.'
} catch {
    $receipt.status = 'incomplete; preserve installation and state for review'
    $receipt.error = $_.Exception.Message
    Save-Receipt
    throw
}
