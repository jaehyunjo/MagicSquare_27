param(
  [Parameter(Mandatory = $true)]
  [string] $Title,

  [string] $ProjectRoot = "",
  [string] $PromptDir = ""
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($ProjectRoot)) {
  $scriptDir = $PSScriptRoot
  if ([string]::IsNullOrWhiteSpace($scriptDir)) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
  }
  $ProjectRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
}

if ([string]::IsNullOrWhiteSpace($PromptDir)) {
  $PromptDir = (Join-Path $ProjectRoot "Prompting")
}

if (-not (Test-Path -LiteralPath $PromptDir)) {
  New-Item -ItemType Directory -Force -Path $PromptDir | Out-Null
}

function Slugify([string] $s) {
  $t = $s.ToLowerInvariant()
  $t = $t -replace "\s+", "_"
  $t = $t -replace "[^a-z0-9_]+", ""
  $t = $t.Trim("_")
  if ([string]::IsNullOrWhiteSpace($t)) { $t = "prompt" }
  return $t
}

$existing = Get-ChildItem -LiteralPath $PromptDir -Filter "*.md" -File |
  Where-Object { $_.Name -match "^\d{2}\." } |
  ForEach-Object { [int]$_.Name.Substring(0, 2) }

$next = 1
if ($existing.Count -gt 0) {
  $next = ($existing | Measure-Object -Maximum).Maximum + 1
}

$n = ([int]$next).ToString("D2")
$slug = Slugify $Title
$fileName = "$n.cursor_$slug`_prompt.md"
$path = Join-Path $PromptDir $fileName

if (Test-Path -LiteralPath $path) {
  throw "Prompt already exists: $path"
}

$content = @"
# $Title

## Goal
- 

## Context
- Project: MagicSquare_XX
- Profile: MS4X4_STD_V1 (magic constant 34, 10 lines)
- Scope: verification first (Valid/Invalid/InputError)

## Prompt

<paste your prompt here>

## Notes / Outcome
- 
"@

Set-Content -LiteralPath $path -Value $content -Encoding UTF8
Write-Host "Created: $path"

