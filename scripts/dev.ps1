Write-Host ""
Write-Host "=== Jarvis Development Environment ===" -ForegroundColor Cyan

& "$PSScriptRoot\..\.venv\Scripts\Activate.ps1"

python --version

Write-Host ""
Write-Host "Environment ready." -ForegroundColor Green