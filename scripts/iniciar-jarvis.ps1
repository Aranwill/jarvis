# ==========================================================
# Malāk - Inicio
# ==========================================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Iniciando Malāk" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------
# Docker Desktop
# ----------------------------------------------------------

$dockerProcess = Get-Process `
    -Name "Docker Desktop" `
    -ErrorAction SilentlyContinue

if (-not $dockerProcess) {

    Write-Host "Iniciando Docker Desktop..." `
        -ForegroundColor Yellow

    Start-Process `
        "C:\Program Files\Docker\Docker\Docker Desktop.exe"
}
else {

    Write-Host "Docker Desktop ya esta ejecutandose." `
        -ForegroundColor Green
}

# ----------------------------------------------------------
# Esperar Docker
# ----------------------------------------------------------

Write-Host ""
Write-Host "Esperando disponibilidad de Docker..." `
    -ForegroundColor Yellow

do {

    Start-Sleep -Seconds 2

    docker info *> $null

    $dockerReady = ($LASTEXITCODE -eq 0)

}
until ($dockerReady)

Write-Host "Docker disponible." `
    -ForegroundColor Green

# ----------------------------------------------------------
# Open WebUI
# ----------------------------------------------------------

Write-Host ""
Write-Host "Verificando Open WebUI..." `
    -ForegroundColor Yellow

docker start open-webui *> $null

Write-Host ""
Write-Host "Esperando respuesta de Open WebUI..." `
    -ForegroundColor Yellow

$startTime = Get-Date
$webuiReady = $false

while (-not $webuiReady) {

    try {

        $response = Invoke-WebRequest `
            -Uri "http://localhost:3000" `
            -Method GET `
            -TimeoutSec 2 `
            -UseBasicParsing

        if ($response.StatusCode -ge 200) {

            $webuiReady = $true
        }
    }
    catch {

        Start-Sleep -Seconds 2
    }
}

$elapsed = (Get-Date) - $startTime

Write-Host `
    ("Open WebUI operativo (" +
     [math]::Round($elapsed.TotalSeconds,1) +
     " segundos).") `
    -ForegroundColor Green

# ----------------------------------------------------------
# Preparar Runtime
# ----------------------------------------------------------

$RuntimePath = "D:\Ollama\jarvis\runtime"

if (-not (Test-Path $RuntimePath)) {

    New-Item `
        -ItemType Directory `
        -Path $RuntimePath | Out-Null
}

# ----------------------------------------------------------
# Perfil dedicado Edge Jarvis
# ----------------------------------------------------------

$EdgeProfile = `
    "D:\Ollama\jarvis\runtime\edge-profile"

if (-not (Test-Path $EdgeProfile)) {

    New-Item `
        -ItemType Directory `
        -Path $EdgeProfile | Out-Null
}

# ----------------------------------------------------------
# Abrir Open WebUI
# ----------------------------------------------------------

Write-Host ""
Write-Host "Abriendo Open WebUI..." `
    -ForegroundColor Green

Start-Process `
    "msedge.exe" `
    "--new-window --user-data-dir=""$EdgeProfile"" http://localhost:3000"

# ----------------------------------------------------------
# Fin
# ----------------------------------------------------------

Write-Host ""
Write-Host "Malāk iniciado correctamente." `
    -ForegroundColor Green

Write-Host ""
