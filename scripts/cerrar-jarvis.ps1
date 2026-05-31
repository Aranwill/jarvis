$backupScript = "D:\Ollama\jarvis\scripts\backup-jarvis.ps1"

if (Test-Path $backupScript) {
    try {
        Write-Host "Creando backup..." -ForegroundColor Cyan
        & $backupScript
    }
    catch {
        Write-Host ("Error durante el backup: " + $_.Exception.Message) -ForegroundColor Red
    }
}
else {
    Write-Host "No se encontró backup-jarvis.ps1" -ForegroundColor Yellow
}

Write-Host "Cerrando Jarvis..." -ForegroundColor Cyan

ollama stop qwen2.5:7b
ollama stop deepseek-coder:6.7b

docker stop open-webui

Write-Host ""
Write-Host "Estado de Ollama:" -ForegroundColor Yellow
ollama ps

Write-Host ""
Write-Host "Estado de Docker:" -ForegroundColor Yellow
docker ps

Write-Host ""
Write-Host "Jarvis cerrado. GPU liberada." -ForegroundColor Green