# Anti-Slop Audit PowerShell Helper
param(
    [string]$Target = ".",
    [switch]$Strict
)

$scriptPath = Join-Path $PSScriptRoot "audit_anti_slop.py"

if ($Strict) {
    python $scriptPath $Target --strict
} else {
    python $scriptPath $Target
}

exit $LASTEXITCODE
