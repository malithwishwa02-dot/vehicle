param(
    [Parameter(Mandatory=$true)][string]$Url,
    [string]$OutDir = ".\bin"
)

if (-not (Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir | Out-Null
}

$OutPath = Join-Path $OutDir "RunAsDate.exe"
Write-Host "Downloading RunAsDate from $Url -> $OutPath"
Invoke-WebRequest -Uri $Url -OutFile $OutPath -UseBasicParsing
if (Test-Path $OutPath) { Write-Host "Downloaded RunAsDate.exe"; exit 0 } else { Write-Error "Failed to download RunAsDate"; exit 1 }