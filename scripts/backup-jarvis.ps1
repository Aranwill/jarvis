$fecha = Get-Date -Format "yyyy-MM-dd_HH-mm"

$destino = "D:\Ollama\jarvis\backups\$fecha"

Write-Host "Creando backup..." -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $destino | Out-Null

Copy-Item `
"D:\Ollama\docker\open-webui\vector_db" `
"$destino\vector_db" `
-Recurse

Copy-Item `
"D:\Ollama\jarvis\documents" `
"$destino\documents" `
-Recurse

Write-Host "Backup completado." -ForegroundColor Green