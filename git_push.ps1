$gitExe = "C:\Users\xuanhoang\.gemini\antigravity\scratch\bin\git\cmd\git.exe"
$repoDir = "C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault"
$remoteUrl = "https://github.com/cowdark123-blip/zero-knowledge-vault.git"

Set-Location $repoDir

Write-Host "1. Initializing Git repository..."
& $gitExe init

Write-Host "2. Configuring Git user..."
& $gitExe config user.name "antigravity-bot"
& $gitExe config user.email "bot@antigravity.ai"

Write-Host "3. Adding files..."
& $gitExe add .

Write-Host "4. Committing..."
& $gitExe commit -m "Initial commit: Zero-Knowledge Password Manager PWA & Cloud Sync"

Write-Host "5. Setting branch main..."
& $gitExe branch -M main

Write-Host "6. Configuring remote origin..."
& $gitExe remote remove origin 2>$null
& $gitExe remote add origin $remoteUrl

Write-Host "7. Pushing to $remoteUrl..."
& $gitExe push -u origin main
