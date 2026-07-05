# ==========================================================
# Malāk - Update Models
# Genera models.md desde ollama list
# ==========================================================

[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()

$ErrorActionPreference = "Stop"

$ProjectRoot = "D:\Ollama\jarvis"

$OutputFile = Join-Path `
    $ProjectRoot `
    "documents\projects\jarvis\models.md"

$Now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Malāk - Actualizando models.md" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ----------------------------------------------------------
# Verificar Ollama
# ----------------------------------------------------------

try {
    $ollamaVersion = ollama --version
}
catch {
    Write-Host "ERROR: Ollama no disponible." -ForegroundColor Red
    exit 1
}

# ----------------------------------------------------------
# Obtener modelos
# ----------------------------------------------------------

$ollamaModels = ollama list

# ----------------------------------------------------------
# Crear documento
# ----------------------------------------------------------

$doc = @()

$doc += "# Modelos Instalados"
$doc += ""
$doc += "**Generado automáticamente**"
$doc += ""
$doc += "**Fecha:** $Now"
$doc += ""
$doc += "---"
$doc += ""
$doc += "## Fuente"
$doc += ""
$doc += '```powershell'
$doc += "ollama list"
$doc += '```'
$doc += ""
$doc += "## Versión de Ollama"
$doc += ""
$doc += '```text'
$doc += "$ollamaVersion"
$doc += '```'
$doc += ""
$doc += "## Modelos Detectados"
$doc += ""
$doc += '```text'

foreach ($line in $ollamaModels) {
    $doc += $line
}

$doc += '```'
$doc += ""
$doc += "## Roles"
$doc += ""
$doc += "La asignación de modelos por rol se define en:"
$doc += ""
$doc += '```text'
$doc += "configs/models.yaml"
$doc += '```'
$doc += ""
$doc += "## Observaciones"
$doc += ""
$doc += "- Documento generado automáticamente."
$doc += "- No editar manualmente."
$doc += "- Actualizar mediante scripts/update-models.ps1."
$doc += "- Los modelos pueden variar durante la fase de laboratorio."

# ----------------------------------------------------------
# Guardar archivo
# ----------------------------------------------------------

$doc | Out-File `
    -FilePath $OutputFile `
    -Encoding utf8

Write-Host ""
Write-Host "Archivo actualizado:" -ForegroundColor Green
Write-Host $OutputFile -ForegroundColor Green
Write-Host ""
Write-Host "Proceso finalizado." -ForegroundColor Green