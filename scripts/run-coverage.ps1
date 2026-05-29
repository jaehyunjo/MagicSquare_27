# Run AC-FR-01-01 tests with coverage (requires .venv + pytest-cov)
# Generates terminal summary + HTML report at htmlcov/index.html
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    Write-Error "Missing .venv. Run: powershell -File scripts/setup-venv.ps1"
}

$Target = "tests/unit/boundary/test_ac_fr_01_01_invalid_size.py"
$HtmlDir = Join-Path $Root "htmlcov"
$HtmlIndex = Join-Path $HtmlDir "index.html"

$Args = @(
    "-m", "pytest", $Target,
    "-v",
    "--cov=magicsquare.boundary",
    "--cov=magicsquare.control",
    "--cov=magicsquare.domain",
    "--cov-config=.coveragerc",
    "--cov-report=term-missing",
    "--cov-report=html:htmlcov"
)

Write-Host "pytest + coverage: $Target"
& $Python @Args
$ExitCode = $LASTEXITCODE

Write-Host ""
if (Test-Path $HtmlIndex) {
    $Resolved = (Resolve-Path $HtmlIndex).Path
    Write-Host "HTML coverage report: $Resolved"
    Write-Host "Open in browser:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\scripts\open-coverage-html.ps1"
    Write-Host "Or open the file directly: htmlcov\index.html"
} else {
    Write-Warning "HTML report was not created. Check pytest-cov install and .coveragerc."
}

exit $ExitCode
