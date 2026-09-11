<#
.SYNOPSIS
One-time conversion of pre-reboot protected-run records into pending metadata.

.DESCRIPTION
This is a bounded migration utility, not a runtime receipt subsystem. It reads
one old protected JSON record for each existing pending capture, validates any
separately preserved exception.txt, and writes only:

  pending/<capture-id>/capture-metadata.json
  pending/<capture-id>/crash/exception.txt  (when the old record proves it)

Preview is the default. Pass -Apply only after the complete preflight succeeds.
The old record tree is never changed or deleted by this script.
#>

#requires -Version 7.5

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string] $RuntimeRoot,

    [switch] $Apply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function ConvertTo-SortedValue {
    param([AllowNull()] $Value)

    if ($null -eq $Value) {
        return $null
    }
    if ($Value -is [string] -or $Value -is [ValueType]) {
        return $Value
    }
    if ($Value -is [System.Collections.IDictionary]) {
        $ordered = [ordered]@{}
        foreach ($key in ($Value.Keys | ForEach-Object { [string] $_ } | Sort-Object)) {
            $ordered[$key] = ConvertTo-SortedValue $Value[$key]
        }
        return $ordered
    }
    if ($Value -is [pscustomobject]) {
        $ordered = [ordered]@{}
        foreach ($property in ($Value.PSObject.Properties | Sort-Object Name)) {
            $ordered[$property.Name] = ConvertTo-SortedValue $property.Value
        }
        return $ordered
    }
    if ($Value -is [System.Collections.IEnumerable]) {
        return @($Value | ForEach-Object { ConvertTo-SortedValue $_ })
    }
    return $Value
}

function ConvertTo-CanonicalJson {
    param([AllowNull()] $Value)

    return (ConvertTo-SortedValue $Value | ConvertTo-Json -Depth 20 -Compress)
}

function Assert-Equal {
    param(
        [AllowNull()] $Actual,
        [AllowNull()] $Expected,
        [string] $Message
    )

    if ($Actual -ne $Expected) {
        throw "$Message (expected '$Expected', got '$Actual')"
    }
}

$resolvedRuntime = (Resolve-Path -LiteralPath $RuntimeRoot).Path
$pendingRoot = Join-Path $resolvedRuntime 'pending'
$recordRoot = Join-Path $resolvedRuntime 'run_receipts\protected'
$exceptionRoot = Join-Path $resolvedRuntime 'crash_evidence'

foreach ($requiredDirectory in @($pendingRoot, $recordRoot)) {
    if (-not (Test-Path -LiteralPath $requiredDirectory -PathType Container)) {
        throw "required migration directory is missing: $requiredDirectory"
    }
}

$pendingDirectories = @(
    Get-ChildItem -LiteralPath $pendingRoot -Directory -Force |
        Where-Object { -not $_.Name.StartsWith('.') } |
        Sort-Object Name
)
$plan = [System.Collections.Generic.List[object]]::new()
$preflightErrors = [System.Collections.Generic.List[string]]::new()

foreach ($pending in $pendingDirectories) {
    try {
        $errorLog = Join-Path $pending.FullName 'error.log'
        if (-not (Test-Path -LiteralPath $errorLog -PathType Leaf)) {
            throw 'mandatory error.log is missing or unreadable'
        }
        if ((Get-Item -LiteralPath $errorLog).Length -le 0) {
            throw 'mandatory error.log is empty'
        }

        $recordPath = Join-Path $recordRoot ($pending.Name + '.json')
        if (-not (Test-Path -LiteralPath $recordPath -PathType Leaf)) {
            throw "matching protected record is missing: $recordPath"
        }
        $record = Get-Content -Raw -LiteralPath $recordPath |
            ConvertFrom-Json -DateKind String
        Assert-Equal $record.schema 'ck3chronicle.protected-run-receipt' 'unexpected record schema'
        Assert-Equal ([int] $record.schema_version) 2 'unexpected record schema version'
        Assert-Equal $record.status 'protected' 'unexpected record status'
        Assert-Equal $record.capture_id $pending.Name 'record capture_id mismatch'
        Assert-Equal $record.pending_name $pending.Name 'record pending_name mismatch'

        if ([string]::IsNullOrWhiteSpace([string] $record.captured_at)) {
            throw 'record captured_at is missing'
        }
        if ([string]::IsNullOrWhiteSpace([string] $record.trigger)) {
            throw 'record trigger is missing'
        }
        if ($record.termination_kind -notin @('normal', 'crash', 'unknown')) {
            throw "invalid termination_kind: $($record.termination_kind)"
        }

        $exceptionStatus = [string] $record.crash_exception.status
        if ($exceptionStatus -notin @('captured', 'absent', 'unavailable', 'not_applicable')) {
            throw "invalid crash exception status: $exceptionStatus"
        }
        $exceptionSource = $null
        $exceptionDestination = $null
        if ($exceptionStatus -eq 'captured') {
            $exceptionSource = Join-Path $exceptionRoot ($pending.Name + '\exception.txt')
            if (-not (Test-Path -LiteralPath $exceptionSource -PathType Leaf)) {
                throw "captured exception evidence is missing: $exceptionSource"
            }
            $exceptionItem = Get-Item -LiteralPath $exceptionSource
            $exceptionHash = (Get-FileHash -LiteralPath $exceptionSource -Algorithm SHA256).Hash.ToLowerInvariant()
            Assert-Equal ([long] $exceptionItem.Length) ([long] $record.crash_exception.bytes) 'exception byte count mismatch'
            Assert-Equal $exceptionHash ([string] $record.crash_exception.sha256).ToLowerInvariant() 'exception SHA-256 mismatch'
            $exceptionDestination = Join-Path $pending.FullName 'crash\exception.txt'
            if (Test-Path -LiteralPath $exceptionDestination -PathType Leaf) {
                $existingException = Get-Item -LiteralPath $exceptionDestination
                $existingHash = (Get-FileHash -LiteralPath $exceptionDestination -Algorithm SHA256).Hash.ToLowerInvariant()
                Assert-Equal ([long] $existingException.Length) ([long] $record.crash_exception.bytes) 'existing pending exception byte count mismatch'
                Assert-Equal $existingHash $exceptionHash 'existing pending exception SHA-256 mismatch'
            }
        }

        $metadata = [ordered]@{
            schema_version = 1
            capture_id = [string] $record.capture_id
            captured_at = [string] $record.captured_at
            trigger = [string] $record.trigger
            process = $record.process
            observed_started_at = $record.observed_started_at
            observed_ended_at = $record.observed_ended_at
            termination_kind = [string] $record.termination_kind
            crash = $record.crash
            crash_exception = [ordered]@{
                status = $exceptionStatus
                source_rel_path = $record.crash_exception.source_rel_path
                retained_path = if ($exceptionStatus -eq 'captured') { 'crash/exception.txt' } else { $null }
            }
        }
        $metadataPath = Join-Path $pending.FullName 'capture-metadata.json'
        $alreadyConverted = $false
        if (Test-Path -LiteralPath $metadataPath -PathType Leaf) {
            $existingMetadata = Get-Content -Raw -LiteralPath $metadataPath |
                ConvertFrom-Json -DateKind String
            if ((ConvertTo-CanonicalJson $existingMetadata) -ne (ConvertTo-CanonicalJson $metadata)) {
                throw 'existing capture-metadata.json disagrees with the legacy record'
            }
            $alreadyConverted = $true
        }

        $plan.Add([pscustomobject]@{
            CaptureId = $pending.Name
            PendingDirectory = $pending.FullName
            MetadataPath = $metadataPath
            Metadata = $metadata
            AlreadyConverted = $alreadyConverted
            ExceptionStatus = $exceptionStatus
            ExceptionSource = $exceptionSource
            ExceptionDestination = $exceptionDestination
        })
    }
    catch {
        $preflightErrors.Add("$($pending.Name): $($_.Exception.Message)")
    }
}

if ($preflightErrors.Count -gt 0) {
    $preflightErrors | ForEach-Object { Write-Error $_ }
    throw "legacy pending metadata preflight failed for $($preflightErrors.Count) capture(s); nothing was changed"
}

$converted = 0
if ($Apply) {
    foreach ($item in $plan) {
        if ($null -ne $item.ExceptionSource -and -not (Test-Path -LiteralPath $item.ExceptionDestination -PathType Leaf)) {
            $exceptionDirectory = Split-Path -Parent $item.ExceptionDestination
            New-Item -ItemType Directory -Path $exceptionDirectory -Force | Out-Null
            $temporaryException = Join-Path $exceptionDirectory ('.exception-migrating-' + [guid]::NewGuid().ToString('N'))
            Copy-Item -LiteralPath $item.ExceptionSource -Destination $temporaryException
            $temporaryHash = (Get-FileHash -LiteralPath $temporaryException -Algorithm SHA256).Hash.ToLowerInvariant()
            $sourceHash = (Get-FileHash -LiteralPath $item.ExceptionSource -Algorithm SHA256).Hash.ToLowerInvariant()
            Assert-Equal $temporaryHash $sourceHash 'staged exception SHA-256 mismatch'
            Move-Item -LiteralPath $temporaryException -Destination $item.ExceptionDestination
        }

        if (-not $item.AlreadyConverted) {
            $temporaryMetadata = Join-Path $item.PendingDirectory ('.capture-metadata-migrating-' + [guid]::NewGuid().ToString('N'))
            $metadataText = ($item.Metadata | ConvertTo-Json -Depth 20) + [Environment]::NewLine
            [System.IO.File]::WriteAllText(
                $temporaryMetadata,
                $metadataText,
                [System.Text.UTF8Encoding]::new($false)
            )
            Move-Item -LiteralPath $temporaryMetadata -Destination $item.MetadataPath
            $converted++
        }
    }
}

[pscustomobject]@{
    RuntimeRoot = $resolvedRuntime
    Mode = if ($Apply) { 'applied' } else { 'preview' }
    PendingCaptures = $pendingDirectories.Count
    Ready = $plan.Count
    AlreadyConverted = @($plan | Where-Object AlreadyConverted).Count
    Converted = $converted
    CapturedExceptions = @($plan | Where-Object ExceptionStatus -eq 'captured').Count
} | ConvertTo-Json -Depth 4
