# Open HTML coverage report in the default browser (requires htmlcov/index.html)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Index = Join-Path $Root "htmlcov\index.html"

if (-not (Test-Path $Index)) {
    Write-Host "htmlcov/index.html not found. Generating report first ..."
    & (Join-Path $PSScriptRoot "run-coverage.ps1")
    if (-not (Test-Path $Index)) {
        Write-Error "Failed to generate HTML coverage. Run: powershell -File scripts/run-coverage.ps1"
    }
}

Write-Host "Opening: $Index"
Start-Process (Resolve-Path $Index).Path
