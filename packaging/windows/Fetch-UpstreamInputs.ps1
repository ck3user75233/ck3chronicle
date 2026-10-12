#requires -Version 5.1
<#
.SYNOPSIS
Downloads pinned build inputs for provenance and notice review. Installs nothing.
.DESCRIPTION
Run from any directory. Files go into the checkout's ignored
.codex-tmp/task10b/upstream directory unless Destination is supplied.
Existing matching archives are reused. Mismatches and interrupted downloads
are preserved for review. Nothing is extracted or executed.
#>
[CmdletBinding()]
param(
    [string]$Destination,
    [switch]$InspectOnly
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Get-Sha256([string]$Path) {
    $stream = [IO.File]::OpenRead($Path)
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose(); $stream.Dispose() }
}

$pinPath = Join-Path $PSScriptRoot 'upstream-inputs.json'
$pins = Get-Content -LiteralPath $pinPath -Raw | ConvertFrom-Json
if (-not $Destination) {
    $repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
    $Destination = Join-Path $repoRoot '.codex-tmp\task10b\upstream'
}
$Destination = [IO.Path]::GetFullPath($Destination)
Write-Host 'Task 10B: download build inputs for provenance and notices'
Write-Host "Archive directory: $Destination"
Write-Host 'Downloads about 88 MB from the pinned GitHub releases.'
Write-Host 'This does not install, extract, run, or replace application files or settings.'

foreach ($asset in $pins.assets) {
    if ($asset.filename -ne [IO.Path]::GetFileName($asset.filename) -or
        $asset.filename -in @('', '.', '..') -or
        $asset.sha256 -notmatch '^[0-9a-f]{64}$' -or
        ([uri]$asset.url).Scheme -ne 'https' -or
        ([uri]$asset.url).Host -ne 'github.com') {
        throw 'Invalid pinned asset. Inspect upstream-inputs.json before continuing.'
    }
    $target = Join-Path $Destination $asset.filename
    Write-Host "`n$($asset.label)"
    Write-Host "  $($asset.url)"
    Write-Host "  Expected SHA-256: $($asset.sha256)"
    if (Test-Path -LiteralPath $target) {
        if ((Get-Sha256 $target) -ne $asset.sha256) {
            throw "Existing archive has a different hash; preserved without replacement: $target"
        }
        Write-Host '  Found matching archive; it will be reused.'
    } else { Write-Host '  Archive not present; download needed.' }
}
if ($InspectOnly) {
    Write-Host "`nInspection complete. No downloads or writes performed."
    exit 0
}

[IO.Directory]::CreateDirectory($Destination) | Out-Null
$receiptPath = Join-Path $Destination ('receipt-' + [guid]::NewGuid().ToString('N') + '.json')
$receipt = [ordered]@{
    started_utc = [DateTime]::UtcNow.ToString('o')
    status = 'incomplete'
    destination = $Destination
    pins_sha256 = Get-Sha256 $pinPath
    script_sha256 = Get-Sha256 $PSCommandPath
    assets = @()
    limitation = 'Archive hashes only. Payload comparison, native dependency and notice review remain required. No installation performed.'
}
$previousTls = [Net.ServicePointManager]::SecurityProtocol
try {
    [Net.ServicePointManager]::SecurityProtocol = $previousTls -bor [Net.SecurityProtocolType]::Tls12
    foreach ($asset in $pins.assets) {
        $target = Join-Path $Destination $asset.filename
        $reused = Test-Path -LiteralPath $target
        if (-not $reused) {
            $partial = $target + '.' + [guid]::NewGuid().ToString('N') + '.partial'
            Write-Host "`nDownloading $($asset.filename) ..."
            $client = New-Object Net.WebClient
            try {
                $client.Headers['User-Agent'] = 'ck3chronicle-task10b-input-receipt'
                $client.DownloadFile($asset.url, $partial)
            } catch {
                throw "Download failed; any partial bytes are retained at $partial. $($_.Exception.Message)"
            } finally { $client.Dispose() }
            if ((Get-Sha256 $partial) -ne $asset.sha256) {
                throw "Downloaded hash differs from the published pin. Bytes retained at $partial; not adopted."
            }
            [IO.File]::Move($partial, $target)
        }
        $actualHash = Get-Sha256 $target
        if ($actualHash -ne $asset.sha256) { throw "Archive changed during acquisition: $target" }
        $receipt.assets += [ordered]@{
            file = $target; url = $asset.url; hash_source = $asset.hash_source
            sha256 = $actualHash; bytes = (Get-Item -LiteralPath $target).Length; reused = [bool]$reused
        }
        Write-Host "Verified: $($asset.filename)"
    }
    $receipt.status = 'all pinned archives authenticated; payload review pending'
} catch {
    $receipt.error = $_.Exception.Message
    throw
} finally {
    [Net.ServicePointManager]::SecurityProtocol = $previousTls
    $receipt.finished_utc = [DateTime]::UtcNow.ToString('o')
    [IO.File]::WriteAllText($receiptPath, ($receipt | ConvertTo-Json -Depth 8), (New-Object Text.UTF8Encoding($false)))
    Write-Host "Receipt: $receiptPath"
}
Write-Host 'Download complete. Resume Task 10B to compare payloads and finish notices.'
