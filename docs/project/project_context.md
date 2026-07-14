---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-07-14
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
branch: refactor/rename-malak
baseline: v0.6.0-alpha
---

# Contexto del proyecto Malāk

## Propósito

Este documento proporciona una visión consolidada del estado observado del repositorio de Malāk.

Es un documento derivado, informativo y no normativo, destinado a ayudar a desarrolladores y asistentes automatizados a recuperar eficientemente el contexto del proyecto.

No reemplaza, modifica ni reinterpreta:

- la Constitución Cognitiva;
- la Constitución de Gobernanza;
- el Blueprint;
- la especificación del Kernel;
- los ADR aceptados;
- los contratos centrales;
- la política de seguridad;
- los registros de release.

Si este documento entra en conflicto con una fuente normativa o histórica, prevalece la fuente con autoridad.

## Regla persistente de idioma

La comunicación y la documentación futura de Malāk deben aplicar estas reglas:

- Todas las respuestas al propietario del proyecto deben estar en español.
- Toda documentación nueva debe redactarse en español.
- Los análisis, planes, informes, ADR, RFC, notas de diseño y propuestas deben estar en español.
- Los nombres de clases, funciones, módulos, APIs, comandos, rutas y términos técnicos existentes pueden mantenerse en inglés.
- No se deben traducir identificadores técnicos ni nombres existentes cuando hacerlo afecte la consistencia del código o del repositorio.
- Cuando una fuente esté en inglés, su contenido debe explicarse en español.

## Límites de la evidencia

Este contexto fue elaborado a partir de:

- inspección del repositorio;
- metadatos locales de Git;
- código fuente rastreado;
- documentación rastreada del proyecto;
- entorno oficial de Python;
- ejecución controlada de la suite completa de tests;
- `repository_analysis.md`, aceptado como evidencia informativa.

No se ejecutó `git fetch` contra el remoto. Por lo tanto, las afirmaciones sobre la rama remota se refieren únicamente a la referencia de seguimiento remoto almacenada localmente.

El documento:

```text
PROJECT - MANIFIESTO MALAK (1).docx
```

está rechazado y no fue utilizado como fuente. No debe influir en Malāk.

## Clasificación documental

### Fuentes normativas

Las principales fuentes de cumplimiento obligatorio son:

1. `docs/governance/cognitive_constitution.md`
2. `docs/governance/governance_constitution.md`
3. `docs/architecture/blueprint.md`
4. `docs/architecture/kernel.md`
5. `docs/architecture/architecture_quality_gates.md`
6. ADR aceptados y contratos públicos aprobados
7. `SECURITY.md`
8. estándares aplicables de desarrollo y repositorio

### Fuentes históricas

Las fuentes históricas incluyen:

- snapshots de release;
- changelogs;
- registros de migración;
- historial de Git;
- historial de ADR aceptados;
- documentos que conservan intencionalmente la identidad anterior de Jarvis.

Los snapshots históricos describen el estado certificado en su fecha. Una diferencia entre un snapshot histórico y el HEAD actual no constituye, por sí sola, permiso para reescribir ese snapshot.

### Fuentes derivadas

Las fuentes derivadas incluyen:

- `repository_analysis.md`;
- este `project_context.md`;
- futuros resúmenes de estado marcados explícitamente como no normativos.

Los documentos derivados pueden informar evidencia y contexto de planificación, pero no pueden aprobar arquitectura, alcance de sprint ni implementación.

## Snapshot validado del repositorio

```text
Raíz Git efectiva:  D:\Ollama\jarvis
Rama activa:        refactor/rename-malak
HEAD inspeccionado: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
Baseline nominal:   v0.6.0-alpha
Distancia del tag:  32 commits
Último PR integrado: PR #5 — feature/runtime-performance-profile
```

El árbol de trabajo estaba limpio antes de crear `repository_analysis.md`.

`repository_analysis.md` es un informe creado intencionalmente que estaba untracked cuando se propuso este contexto. Su presencia no debe confundirse con una modificación del código de producción.

La rama local estaba alineada con la referencia almacenada localmente:

```text
origin/refactor/rename-malak
```

La sincronización remota no se verificó a través de la red.

## Estructura relevante del repositorio

```text
jarvis/
├── .github/
├── configs/
├── docs/
│   ├── architecture/
│   ├── development/
│   ├── governance/
│   ├── knowledge/
│   ├── operations/
│   └── project/
├── documents/projects/jarvis/
├── examples/
├── scripts/
├── src/
│   ├── app/
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

`D:\Ollama` es el espacio de trabajo contenedor y no la raíz Git. Los comandos del repositorio deben ejecutarse desde `D:\Ollama\jarvis`.

## Arquitectura implementada actual

### Flujo observado del Kernel

El flujo observado orientado al Kernel es:

```text
Interface Layer
→ Kernel
→ Planner
→ Capability Registry
→ Capability
→ Response
```

La ruta de código implementada comienza en `Kernel.receive`. Interface Layer es el límite arquitectónico de entrada definido para la interacción con el usuario; todavía no se ha implementado una integración formal de CLI.

El registry predeterminado contiene `EchoCapability`. El Planner MVP actual resuelve las solicitudes hacia esa Capability.

El Kernel coordina el flujo y no depende directamente de Ollama ni de otro LLM runtime concreto.

### Stack conversacional observado

El repositorio contiene:

- `ConversationRequest`;
- `ConversationResponse`;
- `ConversationProvider`;
- `ConversationProviderRegistry`;
- `ConversationService`.

El stack conversacional observado es:

```text
ConversationService
→ Provider Registry
→ Provider
→ LLMRuntime
```

El servicio conversacional resuelve proveedores mediante `ConversationProviderRegistry`, preservando la separación respecto de implementaciones concretas.

### Límite de integración aún no resuelto

No existe una integración formal y validada entre `Kernel.receive` y `ConversationService` en el baseline inspeccionado.

Por lo tanto, el flujo observado del Kernel y el stack conversacional deben tratarse como rutas separadas hasta que una decisión de diseño aprobada defina su integración.

Sprint 7.0 permanece condicionado a una decisión de diseño previa sobre la ruta de integración. Este documento no resuelve esa decisión ni autoriza cambios en el Kernel o los contratos centrales.

La siguiente ruta sólo puede evaluarse como un posible harness limitado de Interface Layer:

```text
CLI
→ ConversationService
→ Provider Registry
→ Provider
→ LLMRuntime
```

Un harness de este tipo:

- requiere aprobación humana explícita antes de su implementación;
- debe documentarse como infraestructura limitada de validación;
- no debe describirse como la arquitectura definitiva;
- no debe presentarse como el pipeline completo de solicitudes de Malāk;
- no debe utilizarse para puentear o redefinir silenciosamente el flujo del Kernel.

### Abstracción de runtime

`LLMRuntime` es la abstracción observada para los LLM runtimes.

Los runtimes implementados incluyen:

- `MockLLMRuntime`;
- `OllamaRuntime`.

`MockLLMRuntime` permite desarrollo y testing deterministas.

`OllamaRuntime` implementa comunicación HTTP local con Ollama y gestiona validación de entrada, errores HTTP, errores de conexión, timeouts y payloads inválidos. No es una dependencia directa del Kernel.

### Métricas de runtime

El repositorio contiene:

- métricas de respuesta del runtime;
- muestras normalizadas de métricas;
- almacenamiento de métricas en memoria;
- almacenamiento persistente JSONL de métricas;
- perfiles inmutables de rendimiento del runtime;
- generación de perfiles estadísticos de rendimiento del runtime.

El profiler es descriptivo. No cambia automáticamente el timeout ni la configuración del runtime.

### Punto de entrada de la aplicación

`src/app/main.py` es el punto de entrada actual del launcher.

En el commit inspeccionado inicializa el logging e informa el inicio de la aplicación. Todavía no implementa un bucle conversacional interactivo de línea de comandos.

Por lo tanto, Sprint 7.0 no está implementado.

## Entorno de desarrollo

Entorno oficial del proyecto:

```text
Entorno virtual: .venv
Python:          3.12.10
pip:             26.1.2
pytest:          9.1.1
```

`pyproject.toml` declara:

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

Actualmente no hay dependencias de producción declaradas.

Actualmente el repositorio no define configuración oficial para:

- Ruff;
- mypy;
- pytest-cov;
- Poetry.

`uv` estaba disponible globalmente durante la inspección, pero no es una herramienta oficial del proyecto en la documentación de desarrollo rastreada.

## Validación

Comando oficial para la suite completa:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Script alternativo del proyecto:

```powershell
.\scripts\test.ps1
```

Resultado validado en el commit inspeccionado:

```text
51 passed in 0.15s
```

Una ejecución inicial aislada produjo:

```text
45 passed
6 setup errors
```

Los seis errores ocurrieron antes de ejecutar los tests porque pytest no pudo acceder a su directorio temporal de Windows. Al volver a ejecutar la misma suite con acceso autorizado al directorio temporal, los 51 tests pasaron correctamente.

No fue necesaria ninguna modificación del código de producción.

La validación confirma el éxito de los tests, pero no establece un porcentaje de cobertura porque no hay herramientas de cobertura configuradas.

## Evolución reciente del repositorio

El trabajo integrado relevante después del baseline nominal incluye:

```text
PR #3 — Ollama Runtime
PR #4 — Runtime Metrics Profile
PR #5 — Runtime Performance Profile
```

HEAD está 32 commits después del tag `v0.6.0-alpha`. La versión del paquete continúa siendo `0.6.0-alpha`.

El tag es el baseline nominal certificado; HEAD es el estado de desarrollo posterior.

## Divergencias documentales conocidas

Se observaron las siguientes diferencias:

1. El snapshot certificado del release `v0.6.0-alpha` registra 21 tests, mientras que HEAD contiene 51 tests en verde.
2. El snapshot del release presenta OllamaRuntime como pendiente, aunque está implementado en HEAD.
3. Las secciones de estado del Blueprint y del Kernel todavía se refieren a Sprint 6.5 o Sprint 6.6.
4. Los roadmaps de la raíz y del proyecto contienen fases que la implementación ya ha superado.
5. `PROJECT.md` conserva elementos del checklist de migración que ya no coinciden con `src/malak`.
6. `SECURITY.md` todavía utiliza Jarvis en redacción activa.
7. Los scripts y las rutas históricas de almacenamiento conservan la identidad anterior de Jarvis.
8. `docs/architecture/documentation_architecture.md` está en estado Draft e incompleto.
9. Sprint 7.0 no está formalizado en la documentación rastreada del proyecto.
10. Sprint 7.5 no está formalizado en la documentación rastreada del proyecto.

Estas divergencias se registran para su clasificación futura. No autorizan ediciones de documentos normativos ni de snapshots históricos.

## Contexto actual de planificación

El siguiente contexto de planificación fue proporcionado y confirmado por el propietario del proyecto. Se registra aquí como contexto no normativo y no como autorización de implementación.

### Sprint 7.0

Próximo sprint previsto:

```text
Sprint 7.0 — CLI mínima con MockLLMRuntime
```

Estado observado:

- no implementado;
- no definido formalmente en la documentación rastreada de sprints;
- condicionado a una decisión de diseño aprobada sobre la ruta de integración entre Interface Layer, `Kernel.receive` y `ConversationService`;
- este documento no autoriza ninguna implementación.

Antes de su implementación, Sprint 7.0 requiere:

- una rama dedicada;
- alcance explícito;
- revisión de arquitectura y gobernanza;
- criterios de validación;
- un Pull Request;
- un punto claro de rollback.

### Sprint 7.5

Fundamento de seguridad previsto:

```text
Sprint 7.5 — Security Control Plane Foundation
```

Estado observado:

- no implementado;
- no definido formalmente en la documentación rastreada del repositorio;
- debe someterse a gobernanza y delimitación de alcance antes de su implementación.

La restricción de secuencia prevista establece que debe preceder a:

- agentes;
- herramientas externas;
- automatización del sistema operativo;
- navegación;
- mensajería externa;
- memoria sensible;
- otras ejecuciones autónomas de alto impacto.

Esta declaración de secuencia no define la arquitectura ni el alcance detallado de Sprint 7.5. Su formalización requiere el proceso de gobernanza y arquitectura aplicable.

## Capacidades explícitamente postergadas

Hasta que un sprint aprobado las autorice y existan los fundamentos de seguridad requeridos, no se deben introducir:

- agentes autónomos;
- ejecución de herramientas externas;
- control del sistema operativo;
- navegación web;
- comunicaciones externas;
- memoria persistente sensible;
- elevación automática de privilegios;
- acciones destructivas;
- integraciones externas ocultas;
- cambios automáticos en la seguridad del runtime o en la política de timeout.

Las referencias a estas capacidades en la visión arquitectónica o en roadmaps históricos no constituyen autorización.

## Restricciones permanentes de trabajo

Todo trabajo futuro debe preservar:

- Kernel First;
- Capability First;
- Runtime Independence;
- Human in Control;
- Zero Trust internally;
- denegación por defecto para acciones sensibles;
- mínimo privilegio;
- autorización explícita;
- contratos públicos;
- cambios pequeños y reversibles;
- trazabilidad.

Antes de cualquier cambio, responde:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Hace al Kernel más simple o más complejo?

Si alguna respuesta es negativa o dudosa, detente antes de editar.

## Artefactos protegidos

No modifiques sin autorización explícita:

- el Kernel;
- los contratos centrales;
- Blueprint;
- Constitución Cognitiva;
- Constitución de Gobernanza;
- reglas de gobernanza;
- ADR aceptados;
- fundamentos de seguridad;
- snapshots históricos de release;
- metadatos de release.

No realices commit, push, merge, creación de PR ni eliminación de archivos sin autorización explícita.

## Disciplina de sprints

El ciclo de desarrollo obligatorio es:

```text
Un sprint
→ una rama
→ un alcance aprobado
→ una validación completa
→ un Pull Request
→ un punto claro de rollback
```

No se puede añadir de forma oportunista ninguna capacidad ajena al sprint aprobado.

## Política de actualización

Este documento está vinculado a:

```text
71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
```

Debe volver a validarse cuando:

- HEAD cambie de manera material;
- un sprint se formalice o complete;
- se certifique un nuevo release;
- cambie la arquitectura o la gobernanza;
- cambien los resultados de los tests;
- cambie la raíz del repositorio o el entorno de desarrollo.

Las actualizaciones de este documento deben preservar los hechos históricos y distinguir claramente entre:

- evidencia verificada del repositorio;
- registros históricos;
- contexto de planificación proporcionado por el propietario;
- decisiones normativas aprobadas.

## Declaración de ausencia de autoridad normativa

Este documento no puede:

- aprobar un sprint;
- autorizar una implementación;
- modificar la arquitectura;
- cambiar la gobernanza;
- redefinir el Kernel;
- modificar contratos;
- certificar un release;
- anular un ADR;
- convertir contexto de planificación en alcance normativo.

Su único propósito es proporcionar un snapshot de contexto trazable, actual y conveniente.
