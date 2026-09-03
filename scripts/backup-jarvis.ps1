# ==========================================================
# Malāk - Backup
# ==========================================================

# LEGACY OPERATIONAL TOOLING
#
# Este script conserva el esquema de backup utilizado durante la etapa basada
# en Open WebUI y su vector_db.
#
# No constituye la estrategia oficial actual de persistencia o backup de Malak.
# Se conserva exclusivamente por trazabilidad y recuperación de infraestructura
# histórica.

$ErrorActionPreference = "Stop"

$fecha = Get-Date -Format "yyyy-MM-dd_HH-mm"

$destino = "D:\Ollama\jarvis\backups\$fecha"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Backup Malāk" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {

    New-Item `
        -ItemType Directory `
        -Force `
        -Path $destino | Out-Null

    Write-Host "Copiando vector_db..." `
        -ForegroundColor Yellow

    Copy-Item `
        "D:\Ollama\docker\open-webui\vector_db" `
        "$destino\vector_db" `
        -Recurse

    Write-Host "Copiando documents..." `
        -ForegroundColor Yellow

    Copy-Item `
        "D:\Ollama\jarvis\documents" `
        "$destino\documents" `
        -Recurse

    Write-Host "Copiando configs..." `
        -ForegroundColor Yellow

    Copy-Item `
        "D:\Ollama\jarvis\configs" `
        "$destino\configs" `
        -Recurse

    Write-Host "Copiando scripts..." `
        -ForegroundColor Yellow

    Copy-Item `
        "D:\Ollama\jarvis\scripts" `
        "$destino\scripts" `
        -Recurse

    if (Test-Path "D:\Ollama\jarvis\memory") {

        Write-Host "Copiando memory..." `
            -ForegroundColor Yellow

        Copy-Item `
            "D:\Ollama\jarvis\memory" `
            "$destino\memory" `
            -Recurse
    }

    $log = @"
Fecha: $(Get-Date)

Backup completado correctamente.

Contenido:
- vector_db
- documents
- configs
- scripts
- memory (si existe)
"@

    $log | Out-File `
        "$destino\backup.log" `
        -Encoding utf8

    Write-Host ""
    Write-Host "Backup completado correctamente." `
        -ForegroundColor Green

    Write-Host "Destino: $destino" `
        -ForegroundColor Green
}
catch {

    Write-Host ""
    Write-Host `
        ("ERROR: " + $_.Exception.Message) `
        -ForegroundColor Red
}