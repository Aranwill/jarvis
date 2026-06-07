# ==========================================================
# Jarvis - Cierre
# ==========================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Cerrando Jarvis" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------
# Backup automático
# ----------------------------------------------------------

$backupScript = "D:\Ollama\jarvis\scripts\backup-jarvis.ps1"

if (Test-Path $backupScript) {

    try {

        Write-Host "Creando backup..." `
            -ForegroundColor Cyan

        & $backupScript

        Write-Host "Backup completado." `
            -ForegroundColor Green
    }
    catch {

        Write-Host ""
        Write-Host `
            ("ERROR durante el backup: " +
             $_.Exception.Message) `
            -ForegroundColor Red

        throw
    }
}
else {

    Write-Host `
        "No se encontro backup-jarvis.ps1" `
        -ForegroundColor Yellow
}

# ----------------------------------------------------------
# Detener modelos Ollama
# ----------------------------------------------------------

Write-Host ""
Write-Host "Deteniendo modelos activos..." `
    -ForegroundColor Yellow

$runningModels = ollama ps | Select-Object -Skip 1

foreach ($line in $runningModels) {

    if ($line.Trim() -ne "") {

        $modelName = ($line -split '\s+')[0]

        Write-Host `
            ("Deteniendo: " + $modelName) `
            -ForegroundColor Yellow

        ollama stop $modelName *> $null
    }
}

Write-Host "Modelos detenidos." `
    -ForegroundColor Green

# ----------------------------------------------------------
# Detener Open WebUI
# ----------------------------------------------------------

Write-Host ""
Write-Host "Deteniendo Open WebUI..." `
    -ForegroundColor Yellow

docker stop open-webui *> $null

Write-Host "Open WebUI detenido." `
    -ForegroundColor Green

# ----------------------------------------------------------
# Cerrar Edge dedicado Jarvis
# ----------------------------------------------------------

Write-Host ""
Write-Host "Cerrando ventana Jarvis..." `
    -ForegroundColor Yellow

$edgeProcesses = Get-CimInstance Win32_Process |
Where-Object {

    $_.Name -eq "msedge.exe" -and
    $_.CommandLine -match "edge-profile"
}

if ($edgeProcesses) {

    foreach ($proc in $edgeProcesses) {

        try {

            Stop-Process `
                -Id $proc.ProcessId `
                -Force `
                -ErrorAction SilentlyContinue
        }
        catch {
        }
    }

    Write-Host "Ventana Jarvis cerrada." `
        -ForegroundColor Green
}
else {

    Write-Host `
        "No se encontro instancia Edge de Jarvis." `
        -ForegroundColor Yellow
}

# ----------------------------------------------------------
# Validacion Final
# ----------------------------------------------------------

Write-Host ""
Write-Host "Estado de Ollama:" `
    -ForegroundColor Cyan

ollama ps

Write-Host ""

Write-Host "Estado de Docker:" `
    -ForegroundColor Cyan

docker ps

Write-Host ""

Write-Host "Jarvis cerrado correctamente." `
    -ForegroundColor Green

Write-Host "Recursos liberados." `
    -ForegroundColor Green

Write-Host ""