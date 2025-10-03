# Remove-OldStubs.ps1
param(
  # Path to the 'modules' directory (relative or absolute)
  [string]$ModulesPath = "docs\modules",

  # Dry-run by default. Omit -WhatIfMode to actually delete files.
  [switch]$WhatIfMode = $true
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $ModulesPath)) {
  Write-Error "Modules path not found: $ModulesPath"
  exit 1
}

# Target filenames to remove (case-insensitive)
$Targets = @(
  "changelog.md",
  "contracts.md",
  "dependencies.md",
  "examples.md",
  "interfaces.md",
  "lifecycle.md",
  "operations.md",
  "storage.md"
)

Write-Host "Scanning: $ModulesPath" -ForegroundColor Cyan
Write-Host "Targets: $($Targets -join ', ')" -ForegroundColor Cyan
Write-Host ("Mode   : {0}" -f ($(if ($WhatIfMode) { "DRY RUN (no deletions)" } else { "DELETE" }))) -ForegroundColor Yellow

# Find matching files under 'modules' recursively
$files = Get-ChildItem -LiteralPath $ModulesPath -Recurse -File -Force -Include $Targets

if (-not $files) {
  Write-Host "No matching files found." -ForegroundColor Green
  exit 0
}

# Show what will be (or would be) removed
Write-Host "`nMatched files:" -ForegroundColor Cyan
$files | ForEach-Object { Write-Host " - $($_.FullName)" }

# Remove files
$removeParams = @{ Force = $true; ErrorAction = "Stop" }
if ($WhatIfMode) { $removeParams["WhatIf"] = $true }

Write-Host "`nProcessing removals..." -ForegroundColor Yellow
$files | ForEach-Object {
  # Clear read-only if set
  try {
    if ($_.Attributes -band [IO.FileAttributes]::ReadOnly) {
      Attrib -R -- $_.FullName | Out-Null
    }
  } catch { }

  Remove-Item -LiteralPath $_.FullName @removeParams -Verbose
}

Write-Host "`nDone." -ForegroundColor Green
