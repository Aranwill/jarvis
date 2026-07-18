@'
# Malāk

Malāk es una plataforma cognitiva personal ejecutada localmente, diseñada para ser modular, gobernable, extensible y agnóstica respecto del modelo de IA utilizado.

## Estado actual

Versión actual:

~~~~text
v0.6.0-alpha
~~~~

Estado:

~~~~text
Foundation Implementation
~~~~

La interfaz disponible actualmente es una CLI técnica de validación del subsistema conversacional.

Esta CLI utiliza `MockLLMRuntime` y no representa todavía el pipeline cognitivo completo de Malāk.

## Requisitos

- Python 3.12.x
- `pip`
- entorno virtual local

Versión validada actualmente:

~~~~text
Python 3.12.10
~~~~

## Preparación del entorno

Desde la raíz del repositorio:

~~~~powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
~~~~

La instalación editable permite utilizar el paquete `malak` desde el layout `src` sin configurar manualmente `PYTHONPATH`.

## Ejecución de la CLI

Con el entorno virtual activado:

~~~~powershell
python -m malak.app.cli
~~~~

Comandos disponibles:

~~~~text
help
status
exit
quit
salir
~~~~

Ejemplo:

~~~~text
Malāk CLI
Runtime activo: MockLLMRuntime
Escribe 'help' para ver los comandos disponibles.
Tú> Hola Malāk
Malāk> [RUNTIME] Hola Malāk
~~~~

## Validación

Ejecutar la suite completa:

~~~~powershell
python -m pytest -v
~~~~

Validar compilación:

~~~~powershell
python -m compileall src tests
~~~~

Estado validado durante el Sprint 7.0:

~~~~text
57 passed
~~~~

## Alcance actual de la CLI

La CLI implementada permite:

- ingresar mensajes por terminal;
- construir un `ConversationRequest`;
- delegar la solicitud mediante `ConversationService`;
- utilizar un provider registrado;
- procesar la solicitud con `MockLLMRuntime`;
- mostrar un `ConversationResponse`;
- ejecutar comandos básicos de ayuda, estado y cierre;
- manejar entradas vacías e interrupciones de consola.

## Fuera de alcance actual

Todavía no forman parte de esta CLI:

- `OllamaRuntime` como runtime activo;
- memoria conversacional;
- historial persistente;
- herramientas externas;
- agentes;
- navegación;
- GraphRAG;
- interfaz gráfica;
- ejecución autónoma.

## Documentación

La documentación principal se encuentra en:

~~~~text
docs/
~~~~

Documentos relevantes:

~~~~text
docs/architecture/blueprint.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/development/development_environment.md
docs/project/implementation_roadmap.md
docs/project/sprints/SPRINT-7.0.md
~~~~

## Principios

Malāk mantiene como principios centrales:

- Kernel First
- Capability First
- Runtime Independence
- Human in Control
- Zero Trust interno
- cambios pequeños, trazables y reversibles
'@ | Set-Content -Path .\README.md -Encoding utf8