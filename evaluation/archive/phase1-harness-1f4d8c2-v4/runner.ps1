param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $HarnessArgs
)

$ErrorActionPreference = 'Stop'
$evaluatorPython = 'C:\Users\nateb\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$harness = Join-Path $PSScriptRoot 'harness.py'

if (-not (Test-Path -LiteralPath $evaluatorPython -PathType Leaf)) {
    throw "Pinned evaluator Python is absent: $evaluatorPython"
}

& $evaluatorPython -B $harness @HarnessArgs
exit $LASTEXITCODE
