<#
.SYNOPSIS
Guided, resumable "local wins" reconciliation of ck3chronicle with its old
GitHub remote.

.DESCRIPTION
This script is deliberately conservative:

* The current local worktree is protected and checkpointed before the remote
  is inspected.
* The remote is never fetched into the local repository.
* The old remote is mirror-cloned and bundled under an external archive root
  that must be outside the ck3chronicle repository.
* Remote files are never merged, checked out, or cherry-picked automatically.
  Only paths explicitly listed by the operator are exported as candidate
  patches into the ignored reconciliation workspace.
* Every stage is logged and followed by a CONTINUE / PAUSE / ABORT gate.
* Remote main replacement is locked unless -EnableRemoteCutover is supplied,
  and it additionally requires an exact typed confirmation phrase.
* A cutover retry recognizes an already-published verified main, and any
  allowlisted old-ref deletions are requested as one atomic, lease-pinned push.
* No pull, merge, rebase, reset --hard, clean, prune, or push --mirror command
  is used.
* The clean-root publication does not rewrite or delete the local repository's
  existing object history. Removing local historical objects, if ever desired,
  is a separate and independently reviewed operation.

The existing GitHub repository is retained so that GitHub-side settings,
issues, and releases are not destroyed. The optional cutover publishes a new
root commit with the exact final local tree to remote main. Old remote branches
and tags are removed only if their full refs are explicitly entered in the
generated deletion allowlist.

Running with -PlanOnly prints the workflow and performs no filesystem or Git
operation. Merely storing or inspecting this file performs no operation.

.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\git-local-wins-reconcile.ps1 -PlanOnly

.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\git-local-wins-reconcile.ps1

.EXAMPLE
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\git-local-wins-reconcile.ps1 -EnableRemoteCutover
#>

#Requires -Version 5.1

[CmdletBinding()]
param(
    [string]$ArchiveRoot,
    [string]$CheckpointMessage = "Checkpoint ck3chronicle development reboot",
    [string]$FinalMessage = "Finalize selectively preserved remote material",
    [switch]$EnableRemoteCutover,
    [switch]$NewSession,
    [switch]$PlanOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:ExpectedRemote = "https://github.com/ck3user75233/ck3chronicle.git"
$script:RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$script:WorkspaceRoot = Join-Path $script:RepoRoot ".ck3chronicle\wip\git-reconciliation"
$script:ActiveStatePath = Join-Path $script:WorkspaceRoot "active-state.json"
$script:Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$script:State = $null
$script:SessionRoot = $null
$script:LogPath = $null

$script:StageNames = @(
    "preflight and read-only local inventory",
    "external source snapshot",
    "stage the local reboot tree",
    "commit and bundle the local checkpoint",
    "read-only remote inventory",
    "external mirror archive and verification",
    "remote-versus-local comparison report",
    "export explicitly allowlisted candidate patches",
    "stage final selectively preserved local state",
    "commit and bundle final local state",
    "prepare and dry-run clean-root publication",
    "replace remote main with the verified clean root",
    "optionally delete explicitly allowlisted old remote refs"
)

function Show-WorkflowPlan {
    Write-Host ""
    Write-Host "ck3chronicle local-wins reconciliation" -ForegroundColor Cyan
    Write-Host "Local files and decisions are authoritative. Remote history is isolated."
    Write-Host ""
    for ($index = 0; $index -lt $script:StageNames.Count; $index++) {
        Write-Host ("  {0,2}. {1}" -f ($index + 1), $script:StageNames[$index])
    }
    Write-Host ""
    Write-Host "Stages 12-13 cannot mutate the remote unless -EnableRemoteCutover is supplied." -ForegroundColor Yellow
    Write-Host "Every completed stage is followed by a review gate and can be resumed later."
}

if ($PlanOnly) {
    Show-WorkflowPlan
    return
}

function Write-Utf8File {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [AllowEmptyString()][string]$Content
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($Path, $Content, $script:Utf8NoBom)
}

function Append-Utf8File {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )
    [System.IO.File]::AppendAllText(
        $Path,
        $Content + [Environment]::NewLine,
        $script:Utf8NoBom
    )
}

function Write-Log {
    param(
        [Parameter(Mandatory = $true)][string]$Message,
        [ValidateSet("INFO", "WARN", "ERROR", "GIT")][string]$Level = "INFO"
    )

    $line = "{0} [{1}] {2}" -f ([DateTime]::UtcNow.ToString("o")), $Level, $Message
    Write-Host $line
    if ($script:LogPath) {
        Append-Utf8File -Path $script:LogPath -Content $line
    }
}

function Format-Argument {
    param([string]$Value)
    if ($Value -match "^[A-Za-z0-9_./:=+@{}^*-]+$") {
        return $Value
    }
    return '"' + $Value.Replace('"', '\"') + '"'
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [string]$WorkingDirectory = $script:RepoRoot,
        [int[]]$AllowedExitCodes = @(0),
        [switch]$QuietOutput
    )

    $displayArguments = $Arguments | ForEach-Object { Format-Argument -Value $_ }
    Write-Log -Level "GIT" -Message ("git " + ($displayArguments -join " "))
    Push-Location -LiteralPath $WorkingDirectory
    try {
        $output = @(& git -c color.ui=false @Arguments 2>&1)
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    $textOutput = @($output | ForEach-Object { [string]$_ })
    foreach ($line in $textOutput) {
        if (-not $QuietOutput) {
            Write-Host $line
        }
        if ($script:LogPath) {
            Append-Utf8File -Path $script:LogPath -Content ("    " + $line)
        }
    }
    if ($AllowedExitCodes -notcontains $exitCode) {
        throw "Git exited with code ${exitCode}: git $($displayArguments -join ' ')"
    }
    return [pscustomobject]@{
        ExitCode = $exitCode
        Output = $textOutput
    }
}

function Get-ResultText {
    param([Parameter(Mandatory = $true)]$Result)
    return (($Result.Output | ForEach-Object { [string]$_ }) -join [Environment]::NewLine)
}

function Test-IsWithinPath {
    param(
        [Parameter(Mandatory = $true)][string]$Candidate,
        [Parameter(Mandatory = $true)][string]$Parent
    )

    $trimCharacters = [char[]]@('\', '/')
    $candidateFull = [System.IO.Path]::GetFullPath($Candidate).TrimEnd($trimCharacters)
    $parentFull = [System.IO.Path]::GetFullPath($Parent).TrimEnd($trimCharacters)
    if ($candidateFull.Equals($parentFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $true
    }
    return $candidateFull.StartsWith(
        $parentFull + [System.IO.Path]::DirectorySeparatorChar,
        [System.StringComparison]::OrdinalIgnoreCase
    )
}

function Assert-ExternalArchiveRoot {
    param([Parameter(Mandatory = $true)][string]$Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if (Test-IsWithinPath -Candidate $fullPath -Parent $script:RepoRoot) {
        throw "ArchiveRoot must be outside the repository: $fullPath"
    }
    if (Test-IsWithinPath -Candidate $script:RepoRoot -Parent $fullPath) {
        throw "ArchiveRoot may not contain the repository itself: $fullPath"
    }
    return $fullPath
}

function Assert-SafeRelativePath {
    param([Parameter(Mandatory = $true)][string]$RelativePath)

    if ([string]::IsNullOrWhiteSpace($RelativePath)) {
        throw "An empty repository-relative path was supplied."
    }
    if ([System.IO.Path]::IsPathRooted($RelativePath)) {
        throw "Absolute paths are forbidden in an allowlist: $RelativePath"
    }
    $candidate = [System.IO.Path]::GetFullPath((Join-Path $script:RepoRoot $RelativePath))
    if (-not (Test-IsWithinPath -Candidate $candidate -Parent $script:RepoRoot)) {
        throw "Path escapes the repository: $RelativePath"
    }
    return $candidate
}

function Save-State {
    $temporary = $script:ActiveStatePath + ".tmp"
    $json = $script:State | ConvertTo-Json -Depth 8
    Write-Utf8File -Path $temporary -Content ($json + [Environment]::NewLine)
    Move-Item -LiteralPath $temporary -Destination $script:ActiveStatePath -Force
}

function Set-StateValue {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [AllowNull()]$Value
    )
    $script:State.$Name = $Value
    Save-State
}

function New-ReconciliationState {
    param([Parameter(Mandatory = $true)][string]$ResolvedArchiveRoot)

    $sessionId = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmss.fffffffZ")
    $sessionRoot = Join-Path $script:WorkspaceRoot $sessionId
    New-Item -ItemType Directory -Path $sessionRoot -Force | Out-Null

    return [pscustomobject]@{
        SchemaVersion = 1
        SessionId = $sessionId
        Status = "new"
        NextStage = 1
        RepoRoot = $script:RepoRoot
        ArchiveRoot = $ResolvedArchiveRoot
        ExternalSessionRoot = (Join-Path $ResolvedArchiveRoot $sessionId)
        SessionRoot = $sessionRoot
        LogPath = (Join-Path $sessionRoot "reconciliation.log")
        InitialBranch = $null
        InitialHead = $null
        InitialTree = $null
        StagedTree = $null
        LocalCheckpoint = $null
        LocalCheckpointTree = $null
        LocalCheckpointBundle = $null
        RemoteUrl = $null
        RemoteMainOid = $null
        RemoteInventoryPath = $null
        RemoteMirrorPath = $null
        RemoteBundlePath = $null
        ComparisonRepoPath = $null
        CandidateAllowlistPath = $null
        CandidateIndexPath = $null
        FinalCommit = $null
        FinalTree = $null
        FinalBundle = $null
        CleanRootCommit = $null
        DeleteAllowlistPath = $null
        LastCompletedStage = $null
        LastError = $null
        UpdatedAt = [DateTime]::UtcNow.ToString("o")
    }
}

function Initialize-State {
    if (-not (Test-Path -LiteralPath $script:WorkspaceRoot)) {
        New-Item -ItemType Directory -Path $script:WorkspaceRoot -Force | Out-Null
    }

    if ((Test-Path -LiteralPath $script:ActiveStatePath) -and -not $NewSession) {
        $script:State = Get-Content -LiteralPath $script:ActiveStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ([System.IO.Path]::GetFullPath([string]$script:State.RepoRoot) -ne $script:RepoRoot) {
            throw "Active state belongs to a different repository: $($script:State.RepoRoot)"
        }
        if ($ArchiveRoot) {
            $requested = Assert-ExternalArchiveRoot -Path $ArchiveRoot
            if ($requested -ne [System.IO.Path]::GetFullPath([string]$script:State.ArchiveRoot)) {
                throw "ArchiveRoot disagrees with the active session. Omit it to resume."
            }
        }
    }
    else {
        if ((Test-Path -LiteralPath $script:ActiveStatePath) -and $NewSession) {
            $existing = Get-Content -LiteralPath $script:ActiveStatePath -Raw -Encoding UTF8 | ConvertFrom-Json
            if ([string]$existing.Status -notin @("complete", "aborted")) {
                throw "Refusing a new session while the active session is $($existing.Status)."
            }
        }
        if (-not $ArchiveRoot) {
            $ArchiveRoot = Join-Path (Split-Path -Parent $script:RepoRoot) "ck3chronicle-git-archive"
        }
        $resolvedArchiveRoot = Assert-ExternalArchiveRoot -Path $ArchiveRoot
        $script:State = New-ReconciliationState -ResolvedArchiveRoot $resolvedArchiveRoot
        Save-State
    }

    $script:SessionRoot = [string]$script:State.SessionRoot
    $script:LogPath = [string]$script:State.LogPath
    if (-not (Test-Path -LiteralPath $script:SessionRoot)) {
        New-Item -ItemType Directory -Path $script:SessionRoot -Force | Out-Null
    }
    if (-not (Test-Path -LiteralPath $script:LogPath)) {
        Write-Utf8File -Path $script:LogPath -Content ""
    }
}

function Set-StageComplete {
    param([Parameter(Mandatory = $true)][int]$Stage)

    $script:State.LastCompletedStage = $Stage
    $script:State.NextStage = $Stage + 1
    $script:State.Status = "waiting_for_review"
    $script:State.LastError = $null
    $script:State.UpdatedAt = [DateTime]::UtcNow.ToString("o")
    Save-State
}

function Wait-ForReview {
    param(
        [Parameter(Mandatory = $true)][int]$CompletedStage,
        [Parameter(Mandatory = $true)][string]$Summary
    )

    Write-Host ""
    Write-Host ("Stage {0} complete: {1}" -f $CompletedStage, $Summary) -ForegroundColor Green
    Write-Host ("Log: {0}" -f $script:LogPath)
    Write-Host "Leave this window waiting while Codex reviews the log, or type PAUSE and rerun the same command later."
    while ($true) {
        $answer = (Read-Host "Type CONTINUE, PAUSE, or ABORT").Trim().ToUpperInvariant()
        Write-Log -Message ("Review response after stage {0}: {1}" -f $CompletedStage, $answer)
        switch ($answer) {
            "CONTINUE" {
                $script:State.Status = "running"
                $script:State.UpdatedAt = [DateTime]::UtcNow.ToString("o")
                Save-State
                return
            }
            "PAUSE" {
                $script:State.Status = "paused"
                $script:State.UpdatedAt = [DateTime]::UtcNow.ToString("o")
                Save-State
                Write-Host "Paused safely. No completed action was undone."
                exit 0
            }
            "ABORT" {
                $script:State.Status = "aborted"
                $script:State.UpdatedAt = [DateTime]::UtcNow.ToString("o")
                Save-State
                Write-Host "Stopped. Completed staging or commits, if any, were not undone."
                exit 2
            }
            default { Write-Host "Unrecognized response." -ForegroundColor Yellow }
        }
    }
}

function Confirm-InitialStart {
    if ([string]$script:State.Status -eq "new") {
        Show-WorkflowPlan
        Write-Host ("Repository: {0}" -f $script:RepoRoot)
        Write-Host ("External archive root: {0}" -f $script:State.ArchiveRoot)
        $answer = (Read-Host "Type START to begin the read-only preflight, or anything else to stop").Trim()
        if ($answer -cne "START") {
            Write-Host "No Git command was run."
            exit 0
        }
        $script:State.Status = "running"
        Save-State
    }
    elseif ([string]$script:State.Status -in @("paused", "waiting_for_review", "failed")) {
        Show-WorkflowPlan
        Write-Host ("Resuming session {0} at stage {1}." -f $script:State.SessionId, $script:State.NextStage)
        $answer = (Read-Host "Type RESUME to continue, or anything else to stop").Trim()
        if ($answer -cne "RESUME") {
            exit 0
        }
        $script:State.Status = "running"
        $script:State.LastError = $null
        Save-State
    }
    elseif ([string]$script:State.Status -eq "complete") {
        Write-Host "The active reconciliation session is complete. Use -NewSession only if a new workflow is genuinely required."
        exit 0
    }
    elseif ([string]$script:State.Status -eq "aborted") {
        Write-Host "The active reconciliation session was aborted. Inspect its log before deciding whether to start a new session."
        exit 2
    }
}

function Get-RemoteInventory {
    param([Parameter(Mandatory = $true)][string]$OutputPath)

    $heads = Invoke-Git -Arguments @("ls-remote", "--heads", "origin") -QuietOutput
    $tags = Invoke-Git -Arguments @("ls-remote", "--tags", "origin") -QuietOutput
    $lines = @($heads.Output + $tags.Output) |
        Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } |
        ForEach-Object { ([string]$_).Trim() } |
        Sort-Object -Unique
    Write-Utf8File -Path $OutputPath -Content (($lines -join [Environment]::NewLine) + [Environment]::NewLine)
    return $lines
}

function Get-MainOidFromInventory {
    param([string[]]$Inventory)
    foreach ($line in $Inventory) {
        if ($line -match "^([0-9a-fA-F]{40})\s+refs/heads/main$") {
            return $Matches[1].ToLowerInvariant()
        }
    }
    return $null
}

function Assert-InventoryUnchanged {
    param([Parameter(Mandatory = $true)][string]$ExpectedPath)

    $currentPath = Join-Path $script:SessionRoot "remote-inventory-current.txt"
    $current = Get-RemoteInventory -OutputPath $currentPath
    $expected = @(Get-Content -LiteralPath $ExpectedPath -Encoding UTF8) |
        Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } |
        ForEach-Object { ([string]$_).Trim() } |
        Sort-Object -Unique
    if (($current -join "`n") -cne ($expected -join "`n")) {
        throw "Remote refs changed after inventory. Stop, inspect, and create a new archive before any cutover."
    }
}

function Get-ExpectedRemoteInventory {
    param(
        [Parameter(Mandatory = $true)][string]$MainOid,
        [string[]]$DeletedRefs = @()
    )

    $expected = New-Object System.Collections.Generic.List[string]
    $mainFound = $false
    foreach ($line in Get-Content -LiteralPath ([string]$script:State.RemoteInventoryPath) -Encoding UTF8) {
        $trimmed = ([string]$line).Trim()
        if (-not $trimmed) { continue }
        if ($trimmed -notmatch "^([0-9a-fA-F]{40})\s+(.+)$") {
            throw "Archived inventory contains an invalid row: $trimmed"
        }
        $ref = $Matches[2]
        if ($ref -ceq "refs/heads/main") {
            $mainFound = $true
            $expected.Add("$MainOid`trefs/heads/main")
            continue
        }
        $baseRef = if ($ref.EndsWith("^{}")) { $ref.Substring(0, $ref.Length - 3) } else { $ref }
        if ($DeletedRefs -ccontains $baseRef) { continue }
        $expected.Add($trimmed)
    }
    if (-not $mainFound) {
        $expected.Add("$MainOid`trefs/heads/main")
    }
    return @($expected | Sort-Object -Unique)
}

function Assert-InventoryEquals {
    param(
        [Parameter(Mandatory = $true)][string[]]$Current,
        [Parameter(Mandatory = $true)][string[]]$Expected,
        [Parameter(Mandatory = $true)][string]$Context
    )

    $currentNormalized = @($Current |
        Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } |
        ForEach-Object { ([string]$_).Trim() } |
        Sort-Object -Unique)
    $expectedNormalized = @($Expected |
        Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } |
        ForEach-Object { ([string]$_).Trim() } |
        Sort-Object -Unique)
    if (($currentNormalized -join "`n") -cne ($expectedNormalized -join "`n")) {
        $differences = @(Compare-Object -ReferenceObject $expectedNormalized -DifferenceObject $currentNormalized)
        foreach ($difference in $differences) {
            Write-Log -Level "ERROR" -Message ("Remote inventory difference {0}: {1}" -f $difference.SideIndicator, $difference.InputObject)
        }
        throw "Remote inventory did not match the expected state: $Context"
    }
}

function Invoke-Stage1Preflight {
    Write-Log -Message "Stage 1: preflight and read-only local inventory"
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        throw "git.exe is not available on PATH."
    }
    $version = Invoke-Git -Arguments @("--version")
    $rootResult = Invoke-Git -Arguments @("rev-parse", "--show-toplevel")
    $actualRoot = [System.IO.Path]::GetFullPath(([string]$rootResult.Output[-1]).Trim())
    if ($actualRoot -ne $script:RepoRoot) {
        throw "Unexpected Git root: $actualRoot"
    }
    $branchResult = Invoke-Git -Arguments @("branch", "--show-current")
    $branch = ([string]$branchResult.Output[-1]).Trim()
    if ($branch -ne "codex/ck3chronicle-reboot") {
        throw "Expected branch codex/ck3chronicle-reboot, found: $branch"
    }
    $headResult = Invoke-Git -Arguments @("rev-parse", "HEAD")
    $treeResult = Invoke-Git -Arguments @("rev-parse", "HEAD^{tree}")
    $remoteResult = Invoke-Git -Arguments @("remote", "get-url", "origin")
    $remoteUrl = ([string]$remoteResult.Output[-1]).Trim()
    if ($remoteUrl.TrimEnd('/') -ne $script:ExpectedRemote.TrimEnd('/')) {
        throw "Unexpected origin URL: $remoteUrl"
    }
    foreach ($marker in @("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-apply", "rebase-merge")) {
        if (Test-Path -LiteralPath (Join-Path $script:RepoRoot ".git\$marker")) {
            throw "An unfinished Git operation exists: .git\$marker"
        }
    }
    Invoke-Git -Arguments @("status", "--short", "--branch") | Out-Null
    Invoke-Git -Arguments @("diff", "--check") | Out-Null
    Invoke-Git -Arguments @("fsck", "--full") | Out-Null

    $script:State.InitialBranch = $branch
    $script:State.InitialHead = ([string]$headResult.Output[-1]).Trim()
    $script:State.InitialTree = ([string]$treeResult.Output[-1]).Trim()
    $script:State.RemoteUrl = $remoteUrl
    Set-StageComplete -Stage 1
    Wait-ForReview -CompletedStage 1 -Summary "Git root, branch, object store, worktree status, and origin URL were recorded; nothing was changed."
}

function Invoke-Stage2SourceSnapshot {
    Write-Log -Message "Stage 2: external source snapshot"
    $externalRoot = [string]$script:State.ExternalSessionRoot
    if (Test-IsWithinPath -Candidate $externalRoot -Parent $script:RepoRoot) {
        throw "External session root unexpectedly resolves inside the repository."
    }
    if (Test-Path -LiteralPath $externalRoot) {
        throw "External session directory already exists before snapshot stage: $externalRoot"
    }
    New-Item -ItemType Directory -Path $externalRoot -Force | Out-Null
    $snapshotRoot = Join-Path $externalRoot "local-source-before-git"
    New-Item -ItemType Directory -Path $snapshotRoot -Force | Out-Null

    $fileList = Invoke-Git -Arguments @("-c", "core.quotepath=false", "ls-files", "--cached", "--others", "--exclude-standard") -QuietOutput
    $manifest = New-Object System.Collections.Generic.List[object]
    foreach ($entry in $fileList.Output) {
        $relative = ([string]$entry).TrimEnd("`r", "`n")
        if ([string]::IsNullOrWhiteSpace($relative)) { continue }
        $source = Assert-SafeRelativePath -RelativePath $relative
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
            continue
        }
        $item = Get-Item -LiteralPath $source
        if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Refusing to snapshot a reparse point: $relative"
        }
        $destination = Join-Path $snapshotRoot $relative
        $destinationParent = Split-Path -Parent $destination
        if (-not (Test-Path -LiteralPath $destinationParent)) {
            New-Item -ItemType Directory -Path $destinationParent -Force | Out-Null
        }
        Copy-Item -LiteralPath $source -Destination $destination
        $hash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
        $manifest.Add([pscustomobject]@{
            Path = $relative.Replace('\', '/')
            Bytes = $item.Length
            Sha256 = $hash
        })
    }
    $manifestPath = Join-Path $externalRoot "local-source-manifest.json"
    Write-Utf8File -Path $manifestPath -Content (($manifest | ConvertTo-Json -Depth 4) + [Environment]::NewLine)
    $status = Invoke-Git -Arguments @("status", "--porcelain=v2", "--branch") -QuietOutput
    Write-Utf8File -Path (Join-Path $externalRoot "local-status-before-git.txt") -Content ((Get-ResultText $status) + [Environment]::NewLine)
    Write-Log -Message ("External snapshot contains {0} files at {1}" -f $manifest.Count, $snapshotRoot)

    Set-StageComplete -Stage 2
    Wait-ForReview -CompletedStage 2 -Summary "The current non-ignored source tree and SHA-256 manifest were copied outside the workspace."
}

function Invoke-Stage3StageLocalCheckpoint {
    Write-Log -Message "Stage 3: stage the local reboot tree"
    Invoke-Git -Arguments @("add", "-A") | Out-Null
    Invoke-Git -Arguments @("diff", "--cached", "--check") | Out-Null
    Invoke-Git -Arguments @("status", "--short") | Out-Null
    Invoke-Git -Arguments @("diff", "--cached", "--stat") | Out-Null
    $nameStatus = Invoke-Git -Arguments @("diff", "--cached", "--name-status") -QuietOutput
    Write-Utf8File -Path (Join-Path $script:SessionRoot "local-checkpoint-name-status.txt") -Content ((Get-ResultText $nameStatus) + [Environment]::NewLine)
    $tree = Invoke-Git -Arguments @("write-tree")
    $script:State.StagedTree = ([string]$tree.Output[-1]).Trim()

    Set-StageComplete -Stage 3
    Wait-ForReview -CompletedStage 3 -Summary "The local tree is staged and validated, but no commit was created."
}

function Invoke-Stage4CommitLocalCheckpoint {
    Write-Log -Message "Stage 4: commit and bundle the local checkpoint"
    $tree = Invoke-Git -Arguments @("write-tree")
    if (([string]$tree.Output[-1]).Trim() -ne [string]$script:State.StagedTree) {
        throw "The staged tree changed after review. Return to inspection before committing."
    }
    Invoke-Git -Arguments @("diff", "--cached", "--check") | Out-Null
    $quiet = Invoke-Git -Arguments @("diff", "--cached", "--quiet") -AllowedExitCodes @(0, 1) -QuietOutput
    if ($quiet.ExitCode -eq 1) {
        Invoke-Git -Arguments @("commit", "-m", $CheckpointMessage) | Out-Null
    }
    else {
        Write-Log -Level "WARN" -Message "Nothing was staged; the existing HEAD is used as the local checkpoint."
    }
    $commit = Invoke-Git -Arguments @("rev-parse", "HEAD")
    $commitOid = ([string]$commit.Output[-1]).Trim()
    $treeResult = Invoke-Git -Arguments @("rev-parse", "HEAD^{tree}")
    $bundlePath = Join-Path ([string]$script:State.ExternalSessionRoot) "local-checkpoint.bundle"
    Invoke-Git -Arguments @("bundle", "create", $bundlePath, "HEAD") | Out-Null
    Invoke-Git -Arguments @("bundle", "verify", $bundlePath) | Out-Null
    $bundleHash = (Get-FileHash -LiteralPath $bundlePath -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Utf8File -Path ($bundlePath + ".sha256") -Content ("$bundleHash  $([System.IO.Path]::GetFileName($bundlePath))`n")
    Invoke-Git -Arguments @("show", "--stat", "--oneline", "--decorate", "--no-renames", $commitOid) | Out-Null

    $script:State.LocalCheckpoint = $commitOid
    $script:State.LocalCheckpointTree = ([string]$treeResult.Output[-1]).Trim()
    $script:State.LocalCheckpointBundle = $bundlePath
    Set-StageComplete -Stage 4
    Wait-ForReview -CompletedStage 4 -Summary "The local checkpoint was committed, bundled outside the workspace, checksumed, and verified."
}

function Invoke-Stage5RemoteInventory {
    Write-Log -Message "Stage 5: read-only remote inventory"
    Invoke-Git -Arguments @("ls-remote", "--symref", "origin", "HEAD") | Out-Null
    $externalInventory = Join-Path ([string]$script:State.ExternalSessionRoot) "remote-inventory-before-archive.txt"
    $inventory = Get-RemoteInventory -OutputPath $externalInventory
    Write-Utf8File -Path (Join-Path $script:SessionRoot "remote-inventory-before-archive.txt") -Content (($inventory -join [Environment]::NewLine) + [Environment]::NewLine)
    $mainOid = Get-MainOidFromInventory -Inventory $inventory
    $script:State.RemoteMainOid = $mainOid
    $script:State.RemoteInventoryPath = $externalInventory
    Write-Log -Message ("Remote inventory contains {0} advertised head/tag refs; main={1}" -f $inventory.Count, $(if ($mainOid) { $mainOid } else { "<absent>" }))

    Set-StageComplete -Stage 5
    Wait-ForReview -CompletedStage 5 -Summary "Remote heads and tags were listed without fetching, pruning, merging, or modifying any ref."
}

function Invoke-Stage6ArchiveRemote {
    Write-Log -Message "Stage 6: external mirror archive and verification"
    $externalRoot = [string]$script:State.ExternalSessionRoot
    $mirrorPath = Join-Path $externalRoot "old-remote-mirror.git"
    if (Test-Path -LiteralPath $mirrorPath) {
        throw "Mirror destination already exists: $mirrorPath"
    }
    Invoke-Git -WorkingDirectory $externalRoot -Arguments @("clone", "--mirror", [string]$script:State.RemoteUrl, $mirrorPath) | Out-Null
    Invoke-Git -Arguments @("--git-dir=$mirrorPath", "fsck", "--full") | Out-Null
    $showRef = Invoke-Git -Arguments @("--git-dir=$mirrorPath", "show-ref", "--head") -QuietOutput
    Write-Utf8File -Path (Join-Path $externalRoot "old-remote-show-ref.txt") -Content ((Get-ResultText $showRef) + [Environment]::NewLine)

    Assert-InventoryUnchanged -ExpectedPath ([string]$script:State.RemoteInventoryPath)
    $remoteBundle = Join-Path $externalRoot "old-remote-before-reboot.bundle"
    Invoke-Git -Arguments @("--git-dir=$mirrorPath", "bundle", "create", $remoteBundle, "--all") | Out-Null
    Invoke-Git -Arguments @("bundle", "verify", $remoteBundle) | Out-Null
    $bundleHash = (Get-FileHash -LiteralPath $remoteBundle -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Utf8File -Path ($remoteBundle + ".sha256") -Content ("$bundleHash  $([System.IO.Path]::GetFileName($remoteBundle))`n")

    $script:State.RemoteMirrorPath = $mirrorPath
    $script:State.RemoteBundlePath = $remoteBundle
    Set-StageComplete -Stage 6
    Wait-ForReview -CompletedStage 6 -Summary "The unchanged old remote was mirror-cloned, fsck-checked, bundled, and checksumed outside the workspace."
}

function Invoke-Stage7ComparisonReport {
    Write-Log -Message "Stage 7: remote-versus-local comparison report"
    $externalRoot = [string]$script:State.ExternalSessionRoot
    $comparisonPath = Join-Path $externalRoot "comparison.git"
    if (Test-Path -LiteralPath $comparisonPath) {
        throw "Comparison repository already exists: $comparisonPath"
    }
    Invoke-Git -WorkingDirectory $externalRoot -Arguments @("init", "--bare", $comparisonPath) | Out-Null
    Invoke-Git -Arguments @(
        "--git-dir=$comparisonPath", "fetch", "--no-tags", [string]$script:State.RemoteMirrorPath,
        "+refs/heads/*:refs/remotes/old/*",
        "+refs/tags/*:refs/tags/old/*"
    ) | Out-Null
    Invoke-Git -Arguments @(
        "--git-dir=$comparisonPath", "fetch", "--no-tags", [string]$script:State.LocalCheckpointBundle,
        "HEAD:refs/heads/local-checkpoint"
    ) | Out-Null

    $branchResult = Invoke-Git -Arguments @(
        "--git-dir=$comparisonPath", "for-each-ref", "--format=%(refname:strip=3)", "refs/remotes/old"
    ) -QuietOutput
    $report = New-Object System.Text.StringBuilder
    [void]$report.AppendLine("ck3chronicle remote comparison")
    [void]$report.AppendLine("Local checkpoint: $($script:State.LocalCheckpoint)")
    [void]$report.AppendLine("Local tree:       $($script:State.LocalCheckpointTree)")
    [void]$report.AppendLine("")
    foreach ($rawBranch in $branchResult.Output) {
        $branch = ([string]$rawBranch).Trim()
        if (-not $branch) { continue }
        $remoteRef = "refs/remotes/old/$branch"
        $remoteOid = Invoke-Git -Arguments @("--git-dir=$comparisonPath", "rev-parse", $remoteRef) -QuietOutput
        $stat = Invoke-Git -Arguments @("--git-dir=$comparisonPath", "diff", "--stat", "refs/heads/local-checkpoint", $remoteRef) -QuietOutput
        $names = Invoke-Git -Arguments @("--git-dir=$comparisonPath", "diff", "--name-status", "refs/heads/local-checkpoint", $remoteRef) -QuietOutput
        $remoteOnlyLog = Invoke-Git -Arguments @(
            "--git-dir=$comparisonPath", "log", "--oneline", "--no-decorate", "--max-count=40",
            "refs/heads/local-checkpoint..$remoteRef"
        ) -QuietOutput
        [void]$report.AppendLine("================================================================")
        [void]$report.AppendLine("REMOTE BRANCH: $branch")
        [void]$report.AppendLine("REMOTE OID:    $(([string]$remoteOid.Output[-1]).Trim())")
        [void]$report.AppendLine("")
        [void]$report.AppendLine("DIFF STAT")
        [void]$report.AppendLine((Get-ResultText $stat))
        [void]$report.AppendLine("")
        [void]$report.AppendLine("NAME STATUS")
        [void]$report.AppendLine((Get-ResultText $names))
        [void]$report.AppendLine("")
        [void]$report.AppendLine("UP TO 40 COMMITS REACHABLE ONLY FROM THIS REMOTE BRANCH")
        [void]$report.AppendLine((Get-ResultText $remoteOnlyLog))
        [void]$report.AppendLine("")
    }
    $reportPath = Join-Path $script:SessionRoot "remote-comparison-report.txt"
    Write-Utf8File -Path $reportPath -Content $report.ToString()

    $allowlistPath = Join-Path $script:SessionRoot "preserve-allowlist.tsv"
    $allowlistTemplate = @"
# Enter only deliberately selected remote candidates, one per line.
# Format: remote-branch<TAB>repository-relative-path
# Example (remove the leading # only after review):
# main`tsrc/ck3chronicle/example.py
#
# The script exports a patch for review. It never applies the patch.
"@
    Write-Utf8File -Path $allowlistPath -Content $allowlistTemplate

    $script:State.ComparisonRepoPath = $comparisonPath
    $script:State.CandidateAllowlistPath = $allowlistPath
    Set-StageComplete -Stage 7
    Wait-ForReview -CompletedStage 7 -Summary "Branch-by-branch stats, changed paths, and remote-only commit summaries are ready; no remote code entered the worktree."
}

function Invoke-Stage8ExportCandidates {
    Write-Log -Message "Stage 8: export explicitly allowlisted candidate patches"
    $allowlistPath = [string]$script:State.CandidateAllowlistPath
    $lines = @(Get-Content -LiteralPath $allowlistPath -Encoding UTF8) |
        Where-Object { $_ -and -not $_.TrimStart().StartsWith("#") }
    $candidateRoot = Join-Path $script:SessionRoot "candidates"
    New-Item -ItemType Directory -Path $candidateRoot -Force | Out-Null
    $index = New-Object System.Collections.Generic.List[object]
    $ordinal = 0
    foreach ($line in $lines) {
        $parts = ([string]$line).Split([char]9)
        if ($parts.Count -ne 2) {
            throw "Invalid allowlist row; expected branch<TAB>path: $line"
        }
        $branch = $parts[0].Trim()
        $relative = $parts[1].Trim().Replace('\', '/')
        Assert-SafeRelativePath -RelativePath $relative | Out-Null
        $remoteRef = "refs/remotes/old/$branch"
        Invoke-Git -Arguments @("--git-dir=$($script:State.ComparisonRepoPath)", "rev-parse", "--verify", $remoteRef) -QuietOutput | Out-Null
        $patchResult = Invoke-Git -Arguments @(
            "--git-dir=$($script:State.ComparisonRepoPath)", "diff", "--binary", "--full-index",
            "refs/heads/local-checkpoint", $remoteRef, "--", $relative
        ) -QuietOutput
        $ordinal += 1
        $safeLeaf = ([System.IO.Path]::GetFileName($relative) -replace "[^A-Za-z0-9._-]", "_")
        $patchPath = Join-Path $candidateRoot ("{0:D3}-{1}.patch" -f $ordinal, $safeLeaf)
        Write-Utf8File -Path $patchPath -Content ((Get-ResultText $patchResult) + [Environment]::NewLine)
        $index.Add([pscustomobject]@{
            Branch = $branch
            Path = $relative
            Patch = $patchPath
        })
    }
    $indexPath = Join-Path $script:SessionRoot "candidate-index.json"
    $indexJson = if ($index.Count -eq 0) { "[]" } else { $index | ConvertTo-Json -Depth 4 }
    Write-Utf8File -Path $indexPath -Content ($indexJson + [Environment]::NewLine)
    $script:State.CandidateIndexPath = $indexPath
    Write-Log -Message ("Exported {0} candidate patches. None were applied." -f $index.Count)

    Set-StageComplete -Stage 8
    Wait-ForReview -CompletedStage 8 -Summary "Only allowlisted patches were exported for human/Codex review; the local worktree was not modified."
}

function Invoke-Stage9StageFinalLocal {
    Write-Log -Message "Stage 9: stage final selectively preserved local state"
    Write-Host "Do not continue unless every approved candidate has already been applied through normal reviewed editing."
    Invoke-Git -Arguments @("status", "--short") | Out-Null
    Invoke-Git -Arguments @("diff", "--check") | Out-Null
    Invoke-Git -Arguments @("add", "-A") | Out-Null
    Invoke-Git -Arguments @("diff", "--cached", "--check") | Out-Null
    Invoke-Git -Arguments @("diff", "--cached", "--stat") | Out-Null
    $tree = Invoke-Git -Arguments @("write-tree")
    $script:State.FinalTree = ([string]$tree.Output[-1]).Trim()

    Set-StageComplete -Stage 9
    Wait-ForReview -CompletedStage 9 -Summary "The final local tree is staged and validated, but the final commit has not been created."
}

function Invoke-Stage10CommitFinalLocal {
    Write-Log -Message "Stage 10: commit and bundle final local state"
    $tree = Invoke-Git -Arguments @("write-tree")
    if (([string]$tree.Output[-1]).Trim() -ne [string]$script:State.FinalTree) {
        throw "The staged final tree changed after review."
    }
    $quiet = Invoke-Git -Arguments @("diff", "--cached", "--quiet") -AllowedExitCodes @(0, 1) -QuietOutput
    if ($quiet.ExitCode -eq 1) {
        Invoke-Git -Arguments @("commit", "-m", $FinalMessage) | Out-Null
    }
    else {
        Write-Log -Level "WARN" -Message "No preservation edits were staged; the checkpoint commit remains final."
    }
    $commit = Invoke-Git -Arguments @("rev-parse", "HEAD")
    $treeResult = Invoke-Git -Arguments @("rev-parse", "HEAD^{tree}")
    $commitOid = ([string]$commit.Output[-1]).Trim()
    $finalTree = ([string]$treeResult.Output[-1]).Trim()
    if ($finalTree -ne [string]$script:State.FinalTree) {
        throw "Final commit tree does not match the reviewed staged tree."
    }
    $bundlePath = Join-Path ([string]$script:State.ExternalSessionRoot) ("final-local-{0}.bundle" -f $commitOid)
    Invoke-Git -Arguments @("bundle", "create", $bundlePath, "HEAD") | Out-Null
    Invoke-Git -Arguments @("bundle", "verify", $bundlePath) | Out-Null
    $bundleHash = (Get-FileHash -LiteralPath $bundlePath -Algorithm SHA256).Hash.ToLowerInvariant()
    Write-Utf8File -Path ($bundlePath + ".sha256") -Content ("$bundleHash  $([System.IO.Path]::GetFileName($bundlePath))`n")
    Invoke-Git -Arguments @("status", "--short", "--branch") | Out-Null

    $script:State.FinalCommit = $commitOid
    $script:State.FinalTree = $finalTree
    $script:State.FinalBundle = $bundlePath
    Set-StageComplete -Stage 10
    Wait-ForReview -CompletedStage 10 -Summary "The final local tree was committed, bundled externally, checksumed, and verified."
}

function Invoke-CommitTree {
    param(
        [Parameter(Mandatory = $true)][string]$Tree,
        [Parameter(Mandatory = $true)][string]$Message
    )

    Write-Log -Level "GIT" -Message "git commit-tree $Tree  # message supplied on stdin; no parent"
    Push-Location -LiteralPath $script:RepoRoot
    try {
        $output = @($Message | & git -c color.ui=false commit-tree $Tree 2>&1)
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    foreach ($line in $output) {
        Append-Utf8File -Path $script:LogPath -Content ("    " + [string]$line)
    }
    if ($exitCode -ne 0) {
        throw "git commit-tree failed with code $exitCode"
    }
    $oid = ([string]$output[-1]).Trim()
    if ($oid -notmatch "^[0-9a-fA-F]{40}$") {
        throw "git commit-tree returned an invalid object ID: $oid"
    }
    return $oid.ToLowerInvariant()
}

function Invoke-Stage11PrepareCutover {
    Write-Log -Message "Stage 11: prepare and dry-run clean-root publication"
    Assert-InventoryUnchanged -ExpectedPath ([string]$script:State.RemoteInventoryPath)
    $cleanMessage = @"
ck3chronicle development reboot

This root commit publishes the verified final local tree after the old remote
was externally archived and any explicitly approved material was selectively
applied.
"@
    $cleanCommit = Invoke-CommitTree -Tree ([string]$script:State.FinalTree) -Message $cleanMessage
    Invoke-Git -Arguments @("cat-file", "-p", $cleanCommit) -QuietOutput | Out-Null
    $cleanTreeResult = Invoke-Git -Arguments @("rev-parse", "${cleanCommit}^{tree}") -QuietOutput
    $cleanTree = ([string]$cleanTreeResult.Output[-1]).Trim()
    if ($cleanTree -cne [string]$script:State.FinalTree) {
        throw "Clean-root commit has the wrong tree."
    }
    $parentResult = Invoke-Git -Arguments @("rev-list", "--parents", "-n", "1", $cleanCommit) -QuietOutput
    $commitAndParents = @((([string]$parentResult.Output[-1]).Trim() -split "\s+") | Where-Object { $_ })
    if ($commitAndParents.Count -ne 1 -or $commitAndParents[0] -cne $cleanCommit) {
        throw "Clean-root publication commit unexpectedly has a parent."
    }
    $expectedMain = if ($script:State.RemoteMainOid) { [string]$script:State.RemoteMainOid } else { "" }
    $lease = "--force-with-lease=refs/heads/main:$expectedMain"
    Invoke-Git -Arguments @(
        "push", "--dry-run", $lease, "origin", "${cleanCommit}:refs/heads/main"
    ) | Out-Null

    $deleteAllowlist = Join-Path $script:SessionRoot "delete-remote-refs-allowlist.txt"
    $inventory = @(Get-Content -LiteralPath ([string]$script:State.RemoteInventoryPath) -Encoding UTF8)
    $suggestions = New-Object System.Text.StringBuilder
    [void]$suggestions.AppendLine("# Optional destructive stage. Uncomment only exact archived refs to remove.")
    [void]$suggestions.AppendLine("# refs/heads/main is forbidden and will never be deleted.")
    foreach ($line in $inventory) {
        if ($line -match "^[0-9a-fA-F]{40}\s+(refs/(?:heads|tags)/.+)$") {
            $ref = $Matches[1]
            if ($ref -ne "refs/heads/main" -and -not $ref.EndsWith("^{}")) {
                [void]$suggestions.AppendLine("# $ref")
            }
        }
    }
    Write-Utf8File -Path $deleteAllowlist -Content $suggestions.ToString()

    $script:State.CleanRootCommit = $cleanCommit
    $script:State.DeleteAllowlistPath = $deleteAllowlist
    Set-StageComplete -Stage 11
    Wait-ForReview -CompletedStage 11 -Summary "A parentless commit with the exact final tree passed a lease-pinned dry-run; the remote remains unchanged."
}

function Invoke-Stage12ReplaceRemoteMain {
    Write-Log -Message "Stage 12: replace remote main with the verified clean root"
    if (-not $EnableRemoteCutover) {
        $script:State.Status = "paused"
        Save-State
        Write-Host "Remote cutover is locked. Review all evidence, then rerun the same script with -EnableRemoteCutover." -ForegroundColor Yellow
        exit 0
    }
    $beforePath = Join-Path $script:SessionRoot "remote-inventory-before-main-replacement.txt"
    $beforeInventory = @(Get-RemoteInventory -OutputPath $beforePath)
    $beforeMain = Get-MainOidFromInventory -Inventory $beforeInventory
    $expectedAfterMain = @(Get-ExpectedRemoteInventory -MainOid ([string]$script:State.CleanRootCommit))
    if ($beforeMain -ceq [string]$script:State.CleanRootCommit) {
        Assert-InventoryEquals -Current $beforeInventory -Expected $expectedAfterMain -Context "retry after main replacement"
        Write-Log -Level "WARN" -Message "Remote main already has the exact verified clean-root commit; treating the prior replacement as successful."
        Set-StageComplete -Stage 12
        Wait-ForReview -CompletedStage 12 -Summary "Remote main already pointed to the verified clean-root commit; all other refs matched the archived state."
        return
    }
    Write-Host ("REMOTE:      {0}" -f $script:State.RemoteUrl) -ForegroundColor Yellow
    Write-Host ("OLD MAIN:    {0}" -f $(if ($script:State.RemoteMainOid) { $script:State.RemoteMainOid } else { "<absent>" }))
    Write-Host ("NEW ROOT:    {0}" -f $script:State.CleanRootCommit)
    Write-Host ("NEW TREE:    {0}" -f $script:State.FinalTree)
    $phrase = Read-Host "Type exactly: REPLACE REMOTE MAIN WITH VERIFIED LOCAL TREE"
    if ($phrase -cne "REPLACE REMOTE MAIN WITH VERIFIED LOCAL TREE") {
        throw "Remote replacement confirmation did not match."
    }
    Assert-InventoryUnchanged -ExpectedPath ([string]$script:State.RemoteInventoryPath)
    $expectedMain = if ($script:State.RemoteMainOid) { [string]$script:State.RemoteMainOid } else { "" }
    $lease = "--force-with-lease=refs/heads/main:$expectedMain"
    Invoke-Git -Arguments @(
        "push", $lease, "origin", "$($script:State.CleanRootCommit):refs/heads/main"
    ) | Out-Null
    $afterPath = Join-Path $script:SessionRoot "remote-inventory-after-main-replacement.txt"
    $afterInventory = @(Get-RemoteInventory -OutputPath $afterPath)
    Assert-InventoryEquals -Current $afterInventory -Expected $expectedAfterMain -Context "verification after main replacement"
    $verifiedMain = Get-MainOidFromInventory -Inventory $afterInventory
    if ($verifiedMain -ne [string]$script:State.CleanRootCommit) {
        throw "Remote main verification failed after push. Expected $($script:State.CleanRootCommit), found $verifiedMain"
    }

    Set-StageComplete -Stage 12
    Wait-ForReview -CompletedStage 12 -Summary "Remote main now points to the verified clean-root commit; no other remote ref was changed."
}

function Get-ArchivedRefOid {
    param([Parameter(Mandatory = $true)][string]$Ref)
    foreach ($line in Get-Content -LiteralPath ([string]$script:State.RemoteInventoryPath) -Encoding UTF8) {
        if ($line -match "^([0-9a-fA-F]{40})\s+(.+)$" -and $Matches[2] -ceq $Ref) {
            return $Matches[1].ToLowerInvariant()
        }
    }
    return $null
}

function Invoke-Stage13DeleteAllowlistedRefs {
    Write-Log -Message "Stage 13: optionally delete explicitly allowlisted old remote refs"
    if (-not $EnableRemoteCutover) {
        $script:State.Status = "paused"
        Save-State
        Write-Host "Remote ref deletion is locked. Rerun with -EnableRemoteCutover only after reviewing the allowlist." -ForegroundColor Yellow
        exit 0
    }
    $refs = @(Get-Content -LiteralPath ([string]$script:State.DeleteAllowlistPath) -Encoding UTF8) |
        ForEach-Object { ([string]$_).Trim() } |
        Where-Object { $_ -and -not $_.StartsWith("#") } |
        Sort-Object -Unique
    $beforeDeletePath = Join-Path $script:SessionRoot "remote-inventory-before-ref-deletion.txt"
    $beforeDelete = @(Get-RemoteInventory -OutputPath $beforeDeletePath)
    $expectedBeforeDelete = @(Get-ExpectedRemoteInventory -MainOid ([string]$script:State.CleanRootCommit))
    Assert-InventoryEquals -Current $beforeDelete -Expected $expectedBeforeDelete -Context "before old-ref deletion"
    if ($refs.Count -eq 0) {
        Write-Log -Level "WARN" -Message "No remote refs were allowlisted for deletion. Old non-main refs, if any, remain reachable."
    }
    else {
        foreach ($ref in $refs) {
            if ($ref -eq "refs/heads/main") {
                throw "Deletion of refs/heads/main is forbidden."
            }
            if ($ref -notmatch "^refs/(heads|tags)/[^\s~^:?*\[]+$") {
                throw "Invalid or unsupported deletion ref: $ref"
            }
            $archivedOid = Get-ArchivedRefOid -Ref $ref
            if (-not $archivedOid) {
                throw "Ref was not present in the archived inventory: $ref"
            }
            $current = Invoke-Git -Arguments @("ls-remote", "origin", $ref) -QuietOutput
            $currentOid = $null
            foreach ($line in $current.Output) {
                if ([string]$line -match "^([0-9a-fA-F]{40})\s+") {
                    $currentOid = $Matches[1].ToLowerInvariant()
                }
            }
            if ($currentOid -ne $archivedOid) {
                throw "Ref changed or is absent; refusing deletion: $ref"
            }
        }
        Write-Host "The following archived remote refs will be deleted:" -ForegroundColor Yellow
        $refs | ForEach-Object { Write-Host "  $_" }
        $phrase = Read-Host "Type exactly: DELETE THE LISTED ARCHIVED REMOTE REFS"
        if ($phrase -cne "DELETE THE LISTED ARCHIVED REMOTE REFS") {
            throw "Remote ref deletion confirmation did not match."
        }
        $pushArguments = @("push", "--atomic")
        foreach ($ref in $refs) {
            $archivedOid = Get-ArchivedRefOid -Ref $ref
            $pushArguments += "--force-with-lease=${ref}:$archivedOid"
        }
        $pushArguments += "origin"
        foreach ($ref in $refs) {
            $pushArguments += ":$ref"
        }
        Invoke-Git -Arguments $pushArguments | Out-Null
    }
    $finalInventory = Join-Path $script:SessionRoot "remote-inventory-after-cutover.txt"
    $finalRefs = @(Get-RemoteInventory -OutputPath $finalInventory)
    $expectedFinal = @(Get-ExpectedRemoteInventory -MainOid ([string]$script:State.CleanRootCommit) -DeletedRefs $refs)
    Assert-InventoryEquals -Current $finalRefs -Expected $expectedFinal -Context "final state after old-ref deletion"
    $script:State.Status = "complete"
    $script:State.LastCompletedStage = 13
    $script:State.NextStage = 14
    $script:State.UpdatedAt = [DateTime]::UtcNow.ToString("o")
    Save-State
    Write-Host ""
    Write-Host "Reconciliation workflow complete." -ForegroundColor Green
    Write-Host ("Log: {0}" -f $script:LogPath)
    Write-Host ("External archive: {0}" -f $script:State.ExternalSessionRoot)
}

Initialize-State
Confirm-InitialStart
Write-Log -Message ("Session {0}; next stage {1}" -f $script:State.SessionId, $script:State.NextStage)

try {
    while ([int]$script:State.NextStage -le 13) {
        switch ([int]$script:State.NextStage) {
            1 { Invoke-Stage1Preflight }
            2 { Invoke-Stage2SourceSnapshot }
            3 { Invoke-Stage3StageLocalCheckpoint }
            4 { Invoke-Stage4CommitLocalCheckpoint }
            5 { Invoke-Stage5RemoteInventory }
            6 { Invoke-Stage6ArchiveRemote }
            7 { Invoke-Stage7ComparisonReport }
            8 { Invoke-Stage8ExportCandidates }
            9 { Invoke-Stage9StageFinalLocal }
            10 { Invoke-Stage10CommitFinalLocal }
            11 { Invoke-Stage11PrepareCutover }
            12 { Invoke-Stage12ReplaceRemoteMain }
            13 { Invoke-Stage13DeleteAllowlistedRefs }
            default { throw "Unexpected stage: $($script:State.NextStage)" }
        }
    }
}
catch {
    $message = $_.Exception.Message
    Write-Log -Level "ERROR" -Message $message
    $script:State.Status = "failed"
    $script:State.LastError = $message
    $script:State.UpdatedAt = [DateTime]::UtcNow.ToString("o")
    Save-State
    Write-Host "Stopped at the first failure. No automatic rollback was attempted." -ForegroundColor Red
    Write-Host ("Inspect: {0}" -f $script:LogPath)
    exit 1
}
