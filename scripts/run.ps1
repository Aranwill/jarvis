
# LEGACY ENTRYPOINT
#
# Este script ejecuta src/app/main.py, un bootstrap histórico de Malak.
#
# No inicia la ruta cognitiva conversacional actual.
# El entrypoint operativo vigente es:
#
#     python -m malak.app.cli
#
# Se conserva exclusivamente por trazabilidad histórica.

& "$PSScriptRoot\..\.venv\Scripts\Activate.ps1"

python src\app\main.py
