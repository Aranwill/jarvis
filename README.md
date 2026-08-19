# Malāk

Malāk es una plataforma cognitiva personal ejecutada localmente, diseñada para ser modular, gobernable, extensible y agnóstica respecto del modelo de inteligencia artificial utilizado.

## Estado actual

Versión actual:

```text
v0.6.0-alpha
```

Estado de desarrollo:

```text
Foundation Implementation
```

Rama permanente:

`main`

Baseline operativo actual:

```text
Sprint 7.8 completado — Cognitive Conversation Execution Path Foundation
```

La interfaz disponible actualmente es una CLI técnica para validar el subsistema conversacional y la primera ruta cognitiva conversacional integrada de Malāk.

La CLI puede utilizar:

- `MockLLMRuntime`;
- `OllamaRuntime`.

La selección del runtime se realiza mediante configuración externa en la frontera de aplicación.

Las solicitudes conversacionales ordinarias ingresan actualmente mediante la frontera cognitiva `Kernel.receive()`.

La conversación se encuentra integrada detrás de la abstracción `Capability`, preservando la independencia del Kernel respecto de servicios, providers, runtimes y modelos concretos.

## Arquitectura actual de la CLI

```text
Variables de entorno
        ↓
CLIConfiguration
        ↓
Application Composition
        ↓
Kernel.receive()
        ↓
Planner
        ↓
CapabilityRegistry
        ↓
ConversationCapability
        ↓
ConversationService
        ↓
ConversationProviderRegistry
        ↓
RuntimeConversationProvider
        ↓
LLMRuntime
├── MockLLMRuntime
└── OllamaRuntime
        ↓
Response
```

La construcción de runtimes, providers y servicios permanece en la frontera de aplicación.

El Kernel continúa desacoplado de implementaciones concretas de runtime y modelo.

## Requisitos

- Python 3.12.x
- `pip`
- entorno virtual local
- Ollama, únicamente para ejecutar `OllamaRuntime`

Versión de Python validada:

```text
Python 3.12.10
```

## Preparación del entorno

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

La instalación editable permite utilizar el paquete `malak` desde el layout `src` sin configurar manualmente `PYTHONPATH`.

## Ejecución con MockLLMRuntime

`MockLLMRuntime` es el runtime predeterminado y no requiere servicios externos.

```powershell
python -m malak.app.cli
```

El comando:

```text
status
```

debe mostrar un estado equivalente a:

```text
Estado: operativo | Provider: mock | Runtime: MockLLMRuntime
```

## Ejecución con OllamaRuntime

### Requisitos previos

- Ollama instalado;
- servicio local de Ollama activo;
- al menos un modelo local disponible;
- entorno virtual de Malāk activado.

Verificar los modelos instalados:

```powershell
ollama list
```

Verificar el servicio HTTP local:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

### Configuración externa

Seleccionar Ollama como runtime:

```powershell
$env:MALAK_RUNTIME = "ollama"
```

Seleccionar el modelo:

```powershell
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
```

Configurar la URL base:

```powershell
$env:MALAK_OLLAMA_BASE_URL = "http://localhost:11434"
```

Iniciar la CLI:

```powershell
python -m malak.app.cli
```

El comando:

```text
status
```

debe mostrar un estado equivalente a:

```text
Estado: operativo | Provider: ollama | Runtime: OllamaRuntime
```

Las variables configuradas mediante `$env:` se aplican únicamente a la sesión actual de PowerShell.

## Variables admitidas

| Variable | Obligatoria | Valor predeterminado |
|---|---:|---|
| `MALAK_RUNTIME` | No | `mock` |
| `MALAK_OLLAMA_MODEL` | Sí cuando el runtime es `ollama` | Sin valor |
| `MALAK_OLLAMA_BASE_URL` | No | `http://localhost:11434` |

Valores admitidos para `MALAK_RUNTIME`:

```text
mock
ollama
```

Un runtime desconocido debe ser rechazado de forma controlada.

## Comandos de la CLI

```text
help
ayuda
status
exit
quit
salir
```

La CLI también controla:

- entradas vacías;
- interrupciones mediante `Ctrl + C`;
- finalización mediante EOF;
- errores del runtime presentados como errores controlados.

Los comandos propios de la CLI permanecen en la frontera de aplicación y no se convierten artificialmente en capabilities.

## Validación automatizada

Ejecutar la suite completa:

```powershell
python -m pytest -q
```

Última suite completa documentada durante la validación y cierre del Sprint 7.8:

```text
348 total passed
```

Validar compilación:

```powershell
python -m compileall src tests
```

Validar formato del diff:

```powershell
git diff --check
```

Las pruebas automatizadas no requieren obligatoriamente un servicio Ollama activo. Las llamadas HTTP utilizadas por `OllamaRuntime` se sustituyen o controlan en las pruebas deterministas.

## Validación manual con Ollama

Secuencia validada:

```powershell
ollama list
Invoke-RestMethod http://localhost:11434/api/tags

$env:MALAK_RUNTIME = "ollama"
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
$env:MALAK_OLLAMA_BASE_URL = "http://localhost:11434"

python -m malak.app.cli
```

Dentro de la CLI:

1. ejecutar `status`;
2. enviar un prompt breve y no sensible;
3. comprobar que se recibe una respuesta;
4. finalizar mediante `exit`.

La integración real fue validada con:

```text
qwen3.5:9b
```

La validación real del Sprint 7.8 confirmó la misma ruta arquitectónica utilizando `OllamaRuntime`, sin introducir dependencias de Ollama dentro del Kernel.

## Alcance actual

La CLI permite:

- ingresar mensajes por terminal;
- generar la solicitud de entrada hacia el Kernel;
- enrutar solicitudes conversacionales ordinarias mediante `Kernel.receive()`;
- resolver la capability `conversation` mediante `Planner` y `CapabilityRegistry`;
- adaptar la solicitud mediante `ConversationCapability`;
- delegar la generación mediante `ConversationService`;
- resolver el provider mediante `ConversationProviderRegistry`;
- utilizar `MockLLMRuntime` u `OllamaRuntime`;
- retornar la respuesta a través de la frontera cognitiva;
- gestionar comandos básicos y errores controlados.

La ruta conversacional actual es:

```text
Request
  ↓
Kernel.receive()
  ↓
Planner
  ↓
CapabilityRegistry
  ↓
ConversationCapability
  ↓
ConversationService
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
Response
```

## Fuera de alcance actual

Todavía no forman parte de esta CLI:

- memoria conversacional persistente;
- historial persistente de conversaciones;
- agentes;
- herramientas externas;
- navegación;
- GraphRAG;
- interfaz gráfica;
- ejecución autónoma;
- aplicación automática de recomendaciones de rendimiento;
- modificación automática de timeout, modelo o permanencia en memoria.

## Documentación

Documentos relevantes:

```text
docs/architecture/blueprint.md
docs/architecture/kernel.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/development/development_environment.md
docs/project/implementation_roadmap.md
docs/project/sprints/SPRINT-7.0.md
docs/project/sprints/SPRINT-7.1.md
docs/project/sprints/SPRINT-7.2.md
docs/project/sprints/SPRINT-7.3.md
docs/project/sprints/SPRINT-7.4.md
docs/project/sprints/SPRINT-7.5.md
docs/project/sprints/SPRINT-7.6.md
docs/project/sprints/SPRINT-7.7.md
docs/project/sprints/SPRINT-7.8.md
```

## Principios

Malāk mantiene como principios centrales:

- Kernel First;
- Capability First;
- Runtime Independence;
- Human in Control;
- Zero Trust interno;
- configuración externa al Kernel;
- cambios pequeños, probados, trazables y reversibles;
- separación entre medición, recomendación y configuración efectiva.
