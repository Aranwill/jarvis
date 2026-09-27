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

Último sprint numerado completado e integrado:

```text
Sprint 7.11 — Reproducible Validation Pipeline Foundation
```

Última ruta conversacional/runtime integrada:

```text
Sprint 7.10 — Conversation Session Isolation Foundation
```

Después de Sprint 7.11 se integraron unidades aisladas de Memory y Cognitive Assurance sin constituir Sprint 7.12. El baseline actual incluye `EpisodicCandidateContentIdentity` y su propagación/binding gobernado a través de la cadena episódica, además de G2A — Protected Finalization Foundation y G2 — Assurance Signal Authority & Projection Foundation en aislamiento.

CAL-014 — Protected Durable Reliance está activado normativamente mediante CC-013, R-023 y ADR-006. Esa activación no autoriza Persistence Authorization, Persistent Memory, Conversation G2B, RDD Stage 2 ni Sprint 7.12.

La interfaz disponible actualmente es una CLI técnica que conserva la ruta conversacional y expone, además, superficies read-only de Engineering, Explorer, Trace y Governed Self-Review.

Estas superficies permiten inspeccionar el baseline, explorar Repository/Knowledge, ejecutar Engineering Inspect/Analyze/Propose bajo sus contracts y reproducir o inspeccionar trazas de Self-Review. No conceden autoridad de modificación, merge ni self-modification.

La CLI puede utilizar:

- `MockLLMRuntime`;
- `OllamaRuntime`.

La selección del runtime se realiza mediante configuración externa en la frontera de aplicación.

Las solicitudes conversacionales ordinarias ingresan actualmente mediante la frontera cognitiva `Kernel.receive()`.

La conversación se encuentra integrada detrás de la abstracción `Capability`, preservando la independencia del Kernel respecto de servicios, providers, runtimes y modelos concretos.

Sprint 7.9 añadió continuidad conversacional efímera en memoria y Sprint 7.10 añadió aislamiento explícito por `session_id`, sin introducir persistencia ni Memory cognitiva.

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

| Variable | Obligatoria | Uso / valor |
|---|---:|---|
| `MALAK_RUNTIME` | No | `mock` por defecto; `ollama` para runtime local |
| `MALAK_OLLAMA_MODEL` | Sí cuando el runtime es `ollama` | Modelo solicitado |
| `MALAK_OLLAMA_BASE_URL` | No | `http://localhost:11434` |
| `MALAK_REPOSITORY_ROOT` | Sí para Engineering / Explorer / Trace / Self-Review | Raíz del snapshot Git |
| `MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS` | Sólo cuando se configura generation contract | Presupuesto de contexto |
| `MALAK_OLLAMA_MAX_OUTPUT_TOKENS` | Sólo cuando se configura generation contract | Presupuesto máximo de salida |
| `MALAK_OLLAMA_THINKING` | Sólo cuando se configura generation contract | `enabled` o `disabled` |

Valores admitidos para `MALAK_RUNTIME`:

```text
mock
ollama
```

Un runtime desconocido debe ser rechazado de forma controlada.

Las tres variables del `RuntimeGenerationContract` deben configurarse juntas. Una configuración parcial se rechaza. Cuando el contrato está presente, preserva explícitamente:

```text
context_window_tokens
max_output_tokens
thinking_enabled
truncate=false
shift=false
```

El contrato es request-scoped y no altera el comportamiento conversacional ordinario cuando no fue configurado.

## Comandos de la CLI

```text
help
ayuda
status
new

/engineering help
/engineering inspect <subject>
/engineering analyze <subject>
/engineering propose <subject>

/explore help
/explore repo list [prefix]
/explore repo read <path>
/explore repo search <text>
/explore knowledge list
/explore knowledge read <path>
/explore knowledge search <text>

/trace help
/trace replay <run_id>
/trace inspect <run_id> <node_id>

/self-review help
/self-review test-v0 <run_id> <validation_ref> [<validation_ref> ...]

exit
quit
salir
```

La CLI también controla:

- entradas vacías;
- continuidad conversacional efímera durante la ejecución;
- reinicio del contexto activo mediante `new`, con rotación de sesión;
- interrupciones mediante `Ctrl + C`;
- finalización mediante EOF;
- errores del runtime presentados como errores controlados.

Los comandos propios de la CLI permanecen en la frontera de aplicación y no se convierten artificialmente en capabilities.

## Validación automatizada

Ejecutar la suite completa:

```powershell
python -m pytest -q
```

La última implementación productiva integrada de esta línea fue E3 Epistemic Calibration (PR #209), validada candidate-bound con:

```text
candidate:
c7a3ec63d8280192bb17f4828759cdf0d8033242

Validation #634

Ubuntu:
1599 passed

Windows:
1599 passed

compileall:
PASS

candidate identity:
PASS

candidate diff:
PASS

Kernel delta:
0

Planner delta:
0

authority_effect:
none
```

El baseline integrado posterior corresponde a `main@32d15ba049ec4a2ef4d46108edfee1d6a59d1f8c`.

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
4. opcionalmente ejecutar `new` y comprobar que se inicia una nueva sesión conversacional;
5. finalizar mediante `exit`.

La integración real fue validada con:

```text
qwen3.5:9b
```

La ruta arquitectónica continúa utilizando `OllamaRuntime` sin introducir dependencias de Ollama dentro del Kernel.

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
- mantener continuidad conversacional efímera;
- aislar el contexto conversacional por `session_id`;
- reiniciar el contexto mediante `new` sin persistencia;
- retornar la respuesta a través de la frontera cognitiva;
- gestionar comandos básicos y errores controlados;
- ejecutar `/engineering inspect|analyze|propose` sobre el baseline configurado;
- explorar Repository y Knowledge mediante `/explore` en modo read-only;
- reproducir e inspeccionar artefactos de trace mediante `/trace`;
- ejecutar el harness gobernado `/self-review test-v0` únicamente cuando se cumplen sus precondiciones de admisión.

Las superficies Engineering, Explorer, Trace y Self-Review no convierten evidencia, findings o propuestas en autoridad y no habilitan self-modification.

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
docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
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
docs/project/sprints/SPRINT-7.9.md
docs/project/sprints/SPRINT-7.10.md
docs/project/sprints/SPRINT-7.11.md
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
