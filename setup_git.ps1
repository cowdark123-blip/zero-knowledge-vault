$gitBinDir = "C:\Users\xuanhoang\.gemini\antigravity\scratch\bin\git"
if (-not (Test-Path $gitBinDir)) {
    New-Item -ItemType Directory -Force -Path $gitBinDir
}

$zipUrl = "https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/MinGit-2.44.0-64-bit.zip"
$tempZip = Join-Path $env:TEMP "mingit.zip"

Write-Host "Downloading MinGit..."
Invoke-WebRequest -Uri $zipUrl -OutFile $tempZip

Write-Host "Extracting MinGit..."
Expand-Archive -Path $tempZip -DestinationPath $gitBinDir -Force
Remove-Item -Force $tempZip

$gitExe = Join-Path $gitBinDir "cmd\git.exe"
Write-Host "Git path: $gitExe"
