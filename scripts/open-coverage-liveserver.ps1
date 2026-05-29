# Generate HTML coverage (if needed) and serve htmlcov/ via Live Server
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Index = Join-Path $Root "htmlcov\index.html"
if (-not (Test-Path $Index)) {
    Write-Host "Generating coverage HTML ..."
    & (Join-Path $PSScriptRoot "run-coverage.ps1") | Out-Null
}

$Port = 5500
$Url = "http://127.0.0.1:$Port/index.html"

Write-Host "Starting Live Server for htmlcov/ at $Url"
Write-Host "Stop with Ctrl+C in this terminal."
npx --yes live-server htmlcov --port=$Port --open=/index.html --watch=.
