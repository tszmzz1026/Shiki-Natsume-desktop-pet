<#
Link an existing local GPT-SoVITS bundle into this project as tts\g50
without copying the ~14GB runtime. Recreate the link after moving the
project or the source bundle.

Usage:
    powershell -ExecutionPolicy Bypass -File scripts\reuse_tts_bundle.ps1
    powershell -ExecutionPolicy Bypass -File scripts\reuse_tts_bundle.ps1 -Source C:\path\to\g50
#>
param(
    [string]$Source = "C:\Users\ASUS\Desktop\sakura-v0.9.7-windows-x64\tts\g50"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$LinkPath = Join-Path $ProjectRoot "tts\g50"

if (-not (Test-Path -LiteralPath $Source -PathType Container)) {
    Write-Error "Source bundle not found: $Source"
    exit 1
}
if (-not (Test-Path -LiteralPath (Join-Path $Source "runtime\python.exe"))) {
    Write-Error "Source bundle has no runtime\python.exe: $Source"
    exit 1
}
if (-not (Test-Path -LiteralPath (Join-Path $Source "api_v2.py"))) {
    Write-Error "Source bundle has no api_v2.py: $Source"
    exit 1
}

if (Test-Path -LiteralPath $LinkPath) {
    $item = Get-Item -LiteralPath $LinkPath
    Write-Host "TTS bundle link already exists: $LinkPath"
    if ($item.LinkType) {
        Write-Host "Links to: $($item.Target)"
    }
    exit 0
}

New-Item -ItemType Directory -Path (Join-Path $ProjectRoot "tts") -Force | Out-Null
New-Item -ItemType Junction -Path $LinkPath -Target $Source | Out-Null
Write-Host "Created TTS bundle junction:"
Write-Host "  $LinkPath"
Write-Host "  -> $Source"
