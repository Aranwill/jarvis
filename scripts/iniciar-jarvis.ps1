Write-Host "Iniciando Jarvis..." -ForegroundColor Cyan

Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

Write-Host "Esperando que Docker arranque..." -ForegroundColor Yellow
Start-Sleep -Seconds 20

docker start open-webui

Write-Host "Abriendo Open WebUI..." -ForegroundColor Green
Start-Process "http://localhost:3000"

Write-Host "Jarvis iniciado correctamente." -ForegroundColor Green