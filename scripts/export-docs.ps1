param(
  [string] $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
  [string] $OutDir = (Join-Path $ProjectRoot "exports")
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $OutDir)) {
  New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
}

$stamp = Get-Date -Format "yyyyMMdd_HHmmss"
$zipName = "MagicSquare_XX_docs_$stamp.zip"
$zipPath = Join-Path $OutDir $zipName

$items = @(
  "README.md",
  "Report",
  "Prompting",
  ".cursor\magicsquare-rules.yaml",
  ".cursor\rules"
)

$paths = @()
foreach ($i in $items) {
  $p = Join-Path $ProjectRoot $i
  if (Test-Path -LiteralPath $p) {
    $paths += $p
  }
}

if ($paths.Count -eq 0) {
  throw "Nothing to export. Expected README.md/Report/Prompting/.cursor files under $ProjectRoot"
}

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -Force -LiteralPath $zipPath
}

Compress-Archive -Path $paths -DestinationPath $zipPath -Force

Write-Host "Exported to: $zipPath"

