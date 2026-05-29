# Create .venv and install dev dependencies for pytest (MagicSquare_XX)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment .venv ..."
    python -m venv .venv
}

Write-Host "Installing dependencies from requirements-dev.txt ..."
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

Write-Host ""
Write-Host "Done. Activate and run tests:"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  pytest tests/unit/boundary/test_ac_fr_01_01_invalid_size.py -v"
Write-Host ""
Write-Host "Coverage (pytest-cov + HTML htmlcov/):"
Write-Host "  powershell -File scripts/run-coverage.ps1"
Write-Host "  powershell -File scripts/open-coverage-html.ps1"
