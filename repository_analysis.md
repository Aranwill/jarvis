# Análisis del repositorio Malāk

Fecha de inspección: 2026-07-14

Repositorio analizado: `D:\Ollama\jarvis`

Commit inspeccionado: `71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c`

Naturaleza del documento: informe derivado, informativo y no normativo

Este informe consolida evidencia obtenida mediante inspección de solo lectura, comandos de Git y ejecución controlada de tests. No reemplaza ni reinterpreta el Blueprint, la Constitución Cognitiva, la Constitución de Gobernanza, la especificación del Kernel, los ADR ni los registros de release. El documento rechazado `PROJECT - MANIFIESTO MALAK (1).docx` fue excluido y no se utilizó como fuente.

# Resumen ejecutivo

## 1. Rama activa y estado de Git

La raíz Git efectiva es `D:\Ollama\jarvis`; `D:\Ollama` es una carpeta contenedora y no un repositorio. La rama activa es `refactor/rename-malak`, con HEAD en `71d13fc`, merge del PR #5 `feature/runtime-performance-profile`. El árbol estaba limpio antes de crear este informe y no presentaba cambios staged, unstaged ni untracked. La rama seguía la referencia local `origin/refactor/rename-malak`; no se ejecutó `fetch`, por lo que no se verificó el estado remoto en tiempo real. El tag `v0.6.0-alpha` está 32 commits detrás de HEAD.

## 2. Estructura relevante del repositorio

El código vive bajo `src/malak`, dividido en contratos, core, Kernel, capacidades, servicios, proveedores y runtimes. `src/app/main.py` es el punto de entrada actual. Los tests están en `tests/`; la documentación normativa y técnica se distribuye entre `docs/architecture`, `docs/governance`, `docs/development`, `docs/operations`, `docs/project` y `docs/knowledge`. Los registros históricos del proyecto y releases están en `documents/projects/jarvis`. Existen además scripts PowerShell para desarrollo, ejecución, pruebas, backups y operación local.

## 3. Documentación crítica encontrada

Se encontraron activos el Blueprint, las Constituciones Cognitiva y de Gobernanza, la especificación del Kernel, los Architecture Quality Gates, el Development Checklist, el entorno de desarrollo, la política de seguridad, el estándar del repositorio, la arquitectura operativa, ADR-001 y el release certificado `v0.6.0-alpha`. Estas fuentes confirman Kernel First, Capability First, Runtime Independence, Human in Control, Zero Trust, trazabilidad y contratos públicos como restricciones centrales.

## 4. Entorno, dependencias y comandos de validación

El entorno oficial es `.venv` con Python 3.12.10, pip 26.1.2 y pytest 9.1.1. `pyproject.toml` no declara dependencias de producción. No están instalados ni configurados Ruff, mypy, pytest-cov o Poetry. `uv` existe globalmente, pero no está definido como herramienta oficial. La validación principal es `.\.venv\Scripts\python.exe -m pytest`; `scripts\test.ps1` activa el entorno y ejecuta pytest en modo verbose. El launcher declarado ejecuta `python src\app\main.py`.

## 5. Estado de tests

La suite contiene 51 pruebas y finalizó con `51 passed in 0.15s`. Una primera ejecución dentro del aislamiento produjo 45 éxitos y 6 errores de preparación por permisos sobre la carpeta temporal de Windows; los cuerpos de esos seis tests no habían fallado. La repetición con acceso autorizado a temporales completó las 51 pruebas correctamente. Git permaneció limpio después de la validación.

## 6. Diferencias respecto del contexto conocido de Malāk

El último PR integrado es el #5, no el #4. Existen 51 tests, no 9. Además de métricas persistentes JSONL, ya existe un perfil estadístico de rendimiento del runtime. OllamaRuntime está implementado. Sin embargo, el release certificado aún registra 21 pruebas y presenta OllamaRuntime como pendiente. Sprint 7.0 y Sprint 7.5 no están formalizados en los documentos rastreados.

## 7. Riesgos o inconsistencias

Hay deriva entre implementación y documentación: roadmaps antiguos, referencias activas a Jarvis, checklist de migración atrasado, release histórico desfasado respecto de HEAD y documentos que aún sitúan la prioridad en Sprint 6.6. `documentation_architecture.md` está en Draft e incompleto. No hay lint, chequeo de tipos ni cobertura configurados. Abrir `D:\Ollama` en lugar de la raíz Git efectiva aumenta el riesgo de ejecutar comandos en el nivel incorrecto.

## 8. Propuesta de ubicación para `AGENTS.md`

La ubicación recomendada es `D:\Ollama\jarvis\AGENTS.md`, en la raíz Git efectiva, para que sus reglas cubran todo el repositorio.

## 9. Próximos pasos recomendados

Crear y revisar `AGENTS.md`; crear un contexto derivado en `docs/project/project_context.md`; formalizar la secuencia Sprint 7.0/Sprint 7.5 sin alterar documentos fundacionales; clasificar la deuda documental; y mantener todo cambio futuro pequeño, autorizado, reversible, validado y asociado a una rama, PR y rollback claros.

# Análisis detallado

## Alcance y método

La inspección comprendió:

- estructura física y archivos rastreados;
- raíz, rama, HEAD, tags, historial y estado de Git;
- entorno virtual, intérprete y herramientas instaladas;
- configuración declarada en `pyproject.toml`;
- scripts de desarrollo, ejecución y tests;
- documentación arquitectónica, cognitiva, de gobernanza, seguridad, desarrollo, operación, proyecto y releases;
- componentes centrales del código;
- ejecución controlada de la suite completa;
- verificación posterior del estado de Git.

No se ejecutaron commits, push, merge, creación de PR, eliminación de archivos, cambios de configuración ni implementación de Sprint 7.0. Tampoco se probaron llamadas reales a Ollama ni servicios externos.

## Raíz efectiva y disposición física

La carpeta inicialmente abierta, `D:\Ollama`, contiene al menos:

```text
D:\Ollama
├── docker/
├── jarvis/
└── conexion de modelos en local.txt
```

`git rev-parse` falla en `D:\Ollama`, mientras que en `D:\Ollama\jarvis` devuelve la raíz válida. Por tanto, la raíz operativa oficial observada es:

```text
D:\Ollama\jarvis
```

La estructura relevante del repositorio es:

```text
jarvis/
├── .git/
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md
├── configs/
│   └── models.yaml
├── docs/
│   ├── architecture/
│   │   ├── adr/
│   │   ├── decisions/
│   │   ├── schemas/
│   │   ├── blueprint.md
│   │   ├── kernel.md
│   │   ├── architecture_quality_gates.md
│   │   ├── documentation_architecture.md
│   │   └── knowledge_model.md
│   ├── development/
│   ├── governance/
│   ├── knowledge/
│   ├── operations/
│   └── project/
├── documents/projects/jarvis/
│   └── releases/v0.6.0-alpha.yaml
├── examples/
├── scripts/
├── src/
│   ├── app/main.py
│   └── malak/
│       ├── capabilities/
│       ├── contracts/
│       ├── core/
│       ├── events/
│       ├── identity/
│       ├── infrastructure/
│       ├── kernel/
│       ├── providers/
│       ├── runtime/
│       ├── services/
│       └── shared/
├── tests/
├── CHANGELOG.md
├── PROJECT.md
├── README.md
├── ROADMAP.md
├── SECURITY.md
├── manifest.yaml
└── pyproject.toml
```

Existen directorios operativos ignorados por Git, como `.venv`, `.pytest_cache`, `data`, `logs`, `memory`, `runtime`, `backups` y almacenamiento local. Su presencia no equivale a componentes versionados de la implementación.

## Git y baseline

Estado observado antes del informe:

```text
Rama:      refactor/rename-malak
HEAD:      71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
Tracking:  origin/refactor/rename-malak
Estado:    limpio
Tag base:  v0.6.0-alpha
Describe:  v0.6.0-alpha-32-g71d13fc
```

El último historial relevante observado fue:

```text
71d13fc Merge pull request #5 from Aranwill/feature/runtime-performance-profile
be99f77 test(runtime): cover performance profile boundaries
f9f91c1 feat(runtime): add performance profile aggregation
5b5f1de Merge pull request #4 from Aranwill/feature/runtime-metrics-profile
d90d084 chore(runtime): ignore local runtime metrics data
a6719d4 feat(runtime): add persistent JSONL metric store
6170e22 feat(runtime): add runtime metric sampling and store
e24f992 Merge pull request #3 from Aranwill/feature/ollama-runtime
```

No hay un tag apuntando a HEAD. `v0.6.0-alpha` continúa siendo el baseline nominal y de paquete, pero no representa el estado exacto del código actual. La afirmación de sincronización con GitHub sólo puede hacerse contra la referencia remota local, ya que no se realizó acceso de red ni `git fetch`.

## Arquitectura implementada observada

### Kernel mínimo

`Kernel.receive`:

1. recibe un `Request`;
2. rechaza contenido vacío de forma determinista;
3. consulta al `Planner`;
4. resuelve la Capability en `CapabilityRegistry`;
5. ejecuta la Capability seleccionada;
6. devuelve un `Response`.

El bootstrap registra `EchoCapability`, y el Planner MVP resuelve siempre `echo`. El flujo ejecutable mínimo observado es:

```text
Request → Kernel → Planner → Capability Registry → EchoCapability → Response
```

El Kernel no invoca Ollama directamente ni contiene lógica concreta de runtime, lo que preserva el desacoplamiento central.

### Conversación y runtimes

Se verificó la existencia de:

- `ConversationRequest`;
- `ConversationResponse`;
- `ConversationProvider`;
- `ConversationProviderRegistry`;
- `ConversationService`;
- `LLMRuntime`;
- `MockLLMRuntime`;
- `OllamaRuntime`.

`ConversationService` resuelve proveedores mediante el registry. `LLMRuntime` define el contrato abstracto `generate`. `MockLLMRuntime` proporciona una implementación determinista para desarrollo y tests. `OllamaRuntime` usa la API HTTP local de Ollama, valida modelo y prompt, maneja errores HTTP, conexión, timeout y JSON inválido, y devuelve un `ConversationResponse` desacoplado del Kernel.

### Métricas y perfiles de rendimiento

`OllamaRuntime` extrae métricas del payload cuando la respuesta es válida. La implementación contiene:

- `RuntimeMetrics` para métricas inmediatas;
- `RuntimeMetricSample` para muestras normalizadas;
- almacenamiento en memoria;
- `JsonlRuntimeMetricStore` para persistencia local;
- `RuntimePerformanceProfile` como resultado inmutable;
- `RuntimePerformanceProfiler` para agregación estadística descriptiva.

El profiler calcula promedios, máximos, rendimiento en tokens por segundo, timeout observado, timeout recomendado y nivel de confianza. Su propia documentación aclara que no cambia automáticamente la configuración del runtime, lo cual mantiene Human in Control y limita su responsabilidad.

### Punto de entrada

`src/app/main.py` configura la ruta de imports y registra mensajes de inicio. No procesa argumentos ni inicia todavía un ciclo conversacional. En consecuencia, la CLI mínima prevista para Sprint 7.0 no está implementada en el estado inspeccionado.

## Fuentes documentales y precedencia

### Fundacionales y arquitectónicas

- `docs/architecture/blueprint.md`: documento maestro activo, versión `0.6.0-alpha`.
- `docs/governance/cognitive_constitution.md`: principios cognitivos permanentes.
- `docs/governance/governance_constitution.md`: control operativo, niveles de riesgo y autorizaciones.
- `docs/architecture/kernel.md`: responsabilidades y límites del Kernel.
- `docs/architecture/architecture_quality_gates.md`: gates obligatorios para cambios significativos.
- `docs/architecture/adr/ADR-001-identity-migration-jarvis-to-malak.md`: decisión aceptada de identidad.
- `docs/architecture/decisions/decision-index.md`: índice oficial de ADR.

El orden de precedencia expresado por la Constitución Cognitiva es:

1. Constitución Cognitiva.
2. Constitución de Gobernanza.
3. Blueprint.
4. Especificaciones.
5. Capabilities.
6. Configuración.

### Desarrollo, seguridad y operación

- `docs/development/development_environment.md` fija Python 3.12.x, `.venv`, pip y pytest.
- `docs/development/development_checklist.md` exige validación arquitectónica, runtime, tests, código, documentación y Git.
- `SECURITY.md` declara Zero Trust, mínimo privilegio, validación explícita, aislamiento, auditoría y control humano.
- `docs/project/repository_standard.md` define la organización física esperada.
- `docs/operations/operational_architecture.md` describe el entorno Ollama/Open WebUI/RAG histórico.
- `.github/PULL_REQUEST_TEMPLATE.md` incluye validación de Blueprint, constituciones y Kernel.

### Release y proyecto

- `documents/projects/jarvis/releases/v0.6.0-alpha.yaml` registra una release interna certificada.
- `PROJECT.md` define Malāk como identidad oficial y Jarvis como nombre anterior.
- `README.md`, `CHANGELOG.md`, `ROADMAP.md` y `docs/project/roadmap.md` contienen información útil, pero parte de ella está desactualizada.

El release certificado debe entenderse como evidencia histórica de la certificación realizada en su fecha, no como inventario dinámico de HEAD. Modificarlo retroactivamente podría degradar trazabilidad; una actualización futura debería realizarse mediante un nuevo artefacto o una decisión explícita de gobernanza.

## Principios relevantes confirmados

El Blueprint y los quality gates establecen:

- Kernel First;
- Constitution First;
- Governance First;
- Capability First;
- Human in Control;
- Zero Trust;
- Model Agnostic;
- Security by Design;
- observabilidad y auditoría;
- Runtime Independence;
- comunicación mediante contratos públicos;
- separación entre planificación, razonamiento, memoria, conocimiento y ejecución;
- prohibición de incorporar lógica de negocio al Kernel;
- ADR para cambios arquitectónicos.

La Constitución Cognitiva prioriza comprensión, evidencia, proporcionalidad, minimización, trazabilidad, coherencia, reversibilidad y aprendizaje controlado. La Constitución de Gobernanza exige autorización explícita para operaciones externas o críticas, mínimo privilegio, estados consistentes y rollback cuando sea técnicamente posible.

## Entorno y herramientas

### Entorno oficial

```text
Python:  3.12.10
pip:     26.1.2
pytest:  9.1.1
venv:    D:\Ollama\jarvis\.venv
```

El Python global detectado también es 3.12.10, pero los documentos obligan a usar el entorno dedicado.

### Dependencias declaradas

`pyproject.toml` contiene:

```toml
[project]
name = "malak"
version = "0.6.0-alpha"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

No se observaron lockfiles, requirements, configuración de cobertura, lint o análisis estático. La ausencia de dependencias declaradas concuerda con el uso de biblioteca estándar en el runtime inspeccionado.

### Comandos disponibles

Preparar una terminal de desarrollo:

```powershell
.\scripts\dev.ps1
```

Ejecutar tests:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

o:

```powershell
.\scripts\test.ps1
```

Ejecutar el launcher:

```powershell
.\.venv\Scripts\python.exe src\app\main.py
```

o:

```powershell
.\scripts\run.ps1
```

Validaciones Git de solo lectura recomendables:

```powershell
git status --short --branch
git diff --check
git diff --stat
git diff --cached --stat
```

## Tests y evidencia de validación

La suite rastreada contiene 14 módulos de test y 51 casos recolectados. Cubre:

- Kernel;
- Capability Registry;
- Planner;
- contratos conversacionales;
- registry y service conversacionales;
- proveedor mock;
- contrato LLMRuntime;
- MockLLMRuntime y OllamaRuntime;
- integración del runtime;
- métricas inmediatas;
- muestras y stores de métricas;
- persistencia JSONL;
- profiler de rendimiento.

Resultado definitivo:

```text
................................................... [100%]
51 passed in 0.15s
```

La incidencia inicial de temporales fue ambiental:

```text
45 passed, 6 setup errors
PermissionError sobre la carpeta temporal administrada por pytest
```

Al ejecutar la misma suite con acceso autorizado a los temporales de Windows, los seis casos restantes pasaron. No se realizó ninguna corrección de código para obtener el resultado verde.

## Comparación con el contexto conocido

### Coincidencias

- Proyecto oficial: Malāk.
- Baseline nominal: `v0.6.0-alpha`.
- Rama esperada: `refactor/rename-malak`.
- Kernel, Planner MVP, Capability Registry y EchoCapability existen.
- El flujo mínimo conocido es consistente con el código.
- `LLMRuntime` es la abstracción central de runtimes observada.
- `MockLLMRuntime` y `OllamaRuntime` existen.
- Los contratos, provider registry y service conversacionales existen.
- Hay telemetría y métricas persistibles en JSONL.
- El Kernel no depende directamente de Ollama.

### Diferencias

| Tema | Contexto conocido | Estado observado |
|---|---|---|
| Último PR | PR #4 | PR #5 integrado |
| Tests | 9 en verde | 51 en verde |
| Métricas | Persistencia JSON | Persistencia JSONL y profiler agregado |
| Baseline | `v0.6.0-alpha` | HEAD 32 commits después del tag |
| Próximo sprint | Sprint 7.0 | No formalizado en documentos rastreados |
| Sprint 7.5 | Security Control Plane Foundation | No aparece en documentos rastreados |
| Raíz abierta | Presunta raíz oficial | Git real en `D:\Ollama\jarvis` |

La definición del Sprint 7.5 proporcionada por el usuario es contexto autorizado de planificación, pero todavía no constituye una fuente versionada dentro del repositorio. Debe registrarse de forma derivada o formalizarse mediante el proceso de gobernanza correspondiente antes de tratarse como documentación oficial.

## Riesgos, deuda e inconsistencias

### Deriva documental

1. `documents/projects/jarvis/releases/v0.6.0-alpha.yaml` declara 21 tests y OllamaRuntime pendiente.
2. Blueprint y Kernel aún indican Sprint 6.5/6.6 como estado o prioridad actual.
3. `ROADMAP.md` y `docs/project/roadmap.md` describen fases ya superadas como pendientes.
4. `PROJECT.md` marca namespace y código como pendientes de migración, aunque `src/malak` ya existe.
5. `SECURITY.md` todavía usa Jarvis como identidad activa.
6. Scripts, rutas y carpetas históricas conservan el nombre Jarvis.
7. `documentation_architecture.md` está en Draft y termina antes de completar los dominios documentales.
8. El índice de decisiones contiene una primera tabla vacía y una segunda con ADR-001, señal de consolidación incompleta.

Estas inconsistencias no justifican modificar documentos fundacionales sin autorización. Primero deben clasificarse entre historia válida, deuda editorial, fuente normativa y snapshot de release.

### Validación limitada

- No hay cobertura configurada; “51 passed” no expresa porcentaje de cobertura.
- No hay lint ni análisis de tipos oficiales.
- No se validó Ollama contra un servicio real durante esta inspección.
- No se ejecutó el ciclo operativo completo porque el launcher sólo registra el inicio.
- No se verificó el remoto en línea.

### Riesgo operativo por raíz anidada

Trabajar desde `D:\Ollama` puede provocar:

- errores al ejecutar Git;
- creación accidental de archivos fuera del repositorio;
- confusión entre datos de Open WebUI y código de Malāk;
- rutas incorrectas en automatizaciones o instrucciones para agentes.

La mitigación recomendada es abrir `D:\Ollama\jarvis` como workspace y declarar esa raíz en `AGENTS.md`.

### Riesgo de adelanto funcional

Los roadmaps históricos mencionan agentes, herramientas, navegación, automatización, memoria y controles del sistema operativo. Según el contexto autorizado, esas funciones no deben adelantarse antes de Security Control Plane Foundation. Cualquier trabajo futuro debe distinguir expresamente entre visión arquitectónica y alcance aprobado del sprint.

## Propuesta para AGENTS.md

Ubicación:

```text
D:\Ollama\jarvis\AGENTS.md
```

Contenido recomendado:

1. Identidad de Malāk y raíz Git efectiva.
2. Jerarquía y precedencia de documentos.
3. Las cuatro preguntas obligatorias antes de cualquier cambio.
4. Kernel First, Capability First, Runtime Independence, Human in Control y Zero Trust interno.
5. Flujo `plan → diff propuesto → autorización → cambio → tests → diff final → rollback`.
6. Protección explícita de Kernel, contratos, Blueprint, constituciones, gobernanza y releases.
7. Prohibición de commits, push, merge, PR y eliminación sin autorización.
8. Regla de un sprint, una rama, validación completa, un PR y rollback claro.
9. Comandos oficiales de entorno y validación.
10. Preservación de cambios locales ajenos.
11. Prohibición de adelantar funciones fuera del alcance aprobado.
12. Exclusión de `PROJECT - MANIFIESTO MALAK (1).docx` como fuente.
13. Distinción entre documentos normativos, históricos y derivados.

No se recomienda codificar en `AGENTS.md` una prohibición permanente y específica sobre Sprint 7.0. La regla durable debería ser que ningún sprint se implementa sin alcance y autorización explícitos.

## Propuesta de contexto consolidado

Ubicación sugerida:

```text
docs/project/project_context.md
```

Metadatos recomendados:

```yaml
status: derived
authority: non-normative
as_of_date: 2026-07-14
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
baseline: v0.6.0-alpha
```

El documento debería contener:

- propósito y límites;
- precedencia de fuentes;
- baseline certificado frente a HEAD;
- arquitectura actualmente implementada;
- componentes y contratos existentes;
- estado validado del entorno y tests;
- historial reciente de PR;
- divergencias documentales conocidas;
- secuencia aprobada Sprint 7.0/Sprint 7.5;
- funciones expresamente pospuestas;
- documento rechazado y excluido;
- método y fecha de validación.

Debe indicar que cualquier conflicto se resuelve a favor de las fuentes fundacionales y que el documento consolidado puede quedar obsoleto al cambiar HEAD.

## Próximos pasos recomendados

1. Reabrir o configurar el workspace en `D:\Ollama\jarvis`.
2. Revisar y autorizar un diff separado para `AGENTS.md`.
3. Revisar y autorizar un diff separado para `docs/project/project_context.md`.
4. Clasificar la deuda documental sin editar todavía fuentes fundacionales.
5. Decidir cómo formalizar Sprint 7.0 y Sprint 7.5 en la documentación gobernada.
6. Mantener el release `v0.6.0-alpha` como snapshot histórico salvo decisión explícita.
7. Considerar en un trabajo futuro y autorizado herramientas mínimas de calidad, sin incorporarlas informalmente.
8. Antes de Sprint 7.0, definir rama, alcance, validación, PR y rollback.
9. Antes de agentes, herramientas externas, automatización, navegación o memoria sensible, completar el alcance aprobado de Security Control Plane Foundation.

## Evaluación arquitectónica de este informe

1. ¿Respeta el Blueprint? Sí. Es un artefacto informativo y no cambia la arquitectura.
2. ¿Respeta la Constitución Cognitiva? Sí. Distingue evidencia, inferencias, límites y contexto no versionado.
3. ¿Respeta la Gobernanza? Sí. Es una modificación pequeña, reversible y auditable autorizada por el usuario.
4. ¿Hace al Kernel más simple o más complejo? No modifica el Kernel ni sus responsabilidades.
