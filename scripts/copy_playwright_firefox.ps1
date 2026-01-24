param(
    [string]$PlaywrightCache = "$env:USERPROFILE\.cache\ms-playwright",
    [string]$OutDir = ".\bin\firefox"
)

Write-Host "Locating Playwright Firefox in $PlaywrightCache"

# Find the firefox-* directories
$firefoxDirs = Get-ChildItem -Path $PlaywrightCache -Directory -Filter "firefox-*" -ErrorAction SilentlyContinue
if (-not $firefoxDirs) {
    Write-Error "Could not find Playwright firefox folder in cache: $PlaywrightCache"
    exit 1
}

# Choose the newest folder
$dir = $firefoxDirs | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$sourceDir = Join-Path $dir.FullName "firefox"
if (-not (Test-Path $sourceDir)) {
    Write-Error "Playwright firefox executable folder not found under $($dir.FullName)"
    exit 1
}

Write-Host "Copying from $sourceDir -> $OutDir"
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }
Copy-Item -Path (Join-Path $sourceDir "*") -Destination $OutDir -Recurse -Force

if (Test-Path (Join-Path $OutDir "firefox.exe")) {
    Write-Host "Firefox copied to $OutDir"
    exit 0
} else {
    Write-Error "Failed to copy Firefox executable to $OutDir"
    exit 2
}