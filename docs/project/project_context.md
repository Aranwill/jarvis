---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-09-10
as_of_commit: 2e8c5d7318678caeb67c8906c951935832760003
branch: main
certification_branch: null
candidate_commit: 59f592e2e36d11bbd14f7d9d93b1dac4f442c108
certification_status: sprint_7_11_completed
baseline: v0.6.0-alpha
---

# Contexto del proyecto Malāk

## Propósito

Este documento proporciona una visión consolidada del estado observado del repositorio de Malāk.

Es un documento derivado, informativo y no normativo, destinado a ayudar a desarrolladores y asistentes automatizados a recuperar eficientemente el contexto operativo actual del proyecto.

No reemplaza, modifica ni reinterpreta:

- la Constitución Cognitiva;
- la Constitución de Gobernanza;
- el Blueprint;
- la especificación del Kernel;
- los ADR aceptados;
- los contratos centrales;
- la política de seguridad;
- los registros de release;
- las fichas de sprint aprobadas;
- el historial Git.

Si este documento entra en conflicto con una fuente normativa, histórica o con evidencia más reciente del repositorio oficial, prevalece la fuente con mayor autoridad.

---

## Regla persistente de idioma

La comunicación y la documentación futura de Malāk deben aplicar estas reglas:

- Todas las respuestas al propietario del proyecto deben estar en español.
- Toda documentación nueva debe redactarse en español.
- Los análisis, planes, informes, ADR, RFC, notas de diseño y propuestas deben estar en español.
- Los nombres de clases, funciones, módulos, APIs, comandos, rutas y términos técnicos existentes pueden mantenerse en inglés.
- No se deben traducir identificadores técnicos ni nombres existentes cuando hacerlo afecte la consistencia del código o del repositorio.
- Cuando una fuente esté en inglés, su contenido debe explicarse en español.

---

## Límites de la evidencia

Este contexto fue reconciliado a partir de:

- inspección del repositorio oficial `Aranwill/jarvis`;
- rama permanente `main`;
- historial Git y commits integrados;
- documentación oficial y derivada vigente;
- fichas de sprint;
- arquitectura implementada documentada;
- resultados de validación registrados durante el cierre del Sprint 7.8;
- revalidación local del baseline previa a la activación del Sprint 7.9;
- evidencia candidate-bound, cierre y validación post-merge de Sprint 7.11;
- integración posterior de Episodic Memory Admission, Assessment Provenance,
  Assessment Producer Authorization y Governed Input Projection;
- validación candidate-bound multiplataforma del candidate de PR #88;
- estado sincronizado del Malāk Project Vault con el HEAD post-PR #88.

El documento:

```text
PROJECT - MANIFIESTO MALAK (1).docx
```

permanece rechazado y no debe utilizarse como fuente de autoridad ni influir en decisiones de Malāk.

---

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

- este `project_context.md`;
- resúmenes de estado marcados explícitamente como no normativos;
- artefactos derivados del Malāk Project Vault.

Los documentos derivados pueden informar evidencia y contexto de planificación, pero no pueden aprobar arquitectura, alcance de sprint ni implementación.

---

## Snapshot validado del repositorio

```text
Repositorio oficial:             Aranwill/jarvis
Raíz Git local:                  D:\Ollama\jarvis
Rama permanente:                 main
Commit integración Sprint 7.11: 3413e8ccb348440aea757d1feccde25c65be011f
HEAD integrado actual:           2e8c5d7318678caeb67c8906c951935832760003
Baseline nominal:                v0.6.0-alpha
Último sprint integrado:         Sprint 7.11 — Reproducible Validation Pipeline Foundation
Última unidad de producto:       Episodic Admission Governed Input Projection Boundary
Última ruta conversacional:      Sprint 7.10 — Conversation Session Isolation Foundation
Sprint activo autorizado:        ninguno
Rama de implementación activa:   ninguna
Candidato Sprint 7.11:           59f592e2e36d11bbd14f7d9d93b1dac4f442c108
Estado Sprint 7.11:              completado e integrado
Sprint posterior autorizado:     ninguno
Unidad posterior autorizada:     ninguna
RDD Stage 2:                     no autorizado
```

Sprint 7.11 — `Reproducible Validation Pipeline Foundation` fue admitido,
autorizado, implementado, validado e integrado mediante PR #65.

El candidato final validado fue:

```text
59f592e2e36d11bbd14f7d9d93b1dac4f442c108
```

La integración se realizó mediante PR #65 con merge commit:

```text
3413e8ccb348440aea757d1feccde25c65be011f
```

Evidencia del candidato y validación post-merge:

```text
388 passed
compileall: PASS
git diff --check: PASS
FULL 4R: PASS
independent validation: PASS
post-merge Validation: success
```

Después de Sprint 7.11, el Owner autorizó de forma separada y acotada una serie
de unidades episódicas aisladas de Memory.

La primera fue G3 — `Episodic Memory Admission Boundary`, integrada mediante PR #76:

~~~text
candidate:
e3e3c2aa6031d4a6a9ad8f3a3c529a9453cbbe9b

merge:
2d5fe87c304927baeab29e5649f2383030e1a1fd

pytest:
431 passed

compileall:
PASS

git diff --check:
PASS

post-merge Validation:
success
~~~

Después se integraron, cada una mediante autorización y gate separados:

```text
PR #82
Episodic Admission Assessment Provenance Boundary

PR #85
Episodic Admission Assessment Producer Authorization Boundary

PR #88
Episodic Admission Governed Input Projection Boundary
```

El HEAD material resultante es:

```text
2e8c5d7318678caeb67c8906c951935832760003
```

El candidate de PR #88:

```text
87a7e31e0735edd25a80a693cf3f437f7a1501fc
```

pasó `Validation` candidate-bound en `ubuntu-latest`, `windows-latest` y
`macos-latest`, incluyendo candidate identity, suite completa, `compileall` y
candidate diff validation.

La cadena materializada preserva:

```text
Assessment Provenance
!= authenticated identity
!= trusted truth

Producer Authorization
!= trusted truth
!= Admission eligibility
!= persistence authorization
!= authority

Projection READY
!= Admission ELIGIBLE
!= Stored
!= Authority
```

La proyección no llama `evaluate_episodic_candidate(...)`; el consumo
`Projection → Admission` permanece como frontera posterior no autorizada.

Permanece fuera de alcance:

~~~text
runtime wiring
Projection -> Admission wiring
Memory persistente
retrieval
Knowledge
Kernel changes
Conversation changes
Security authority expansion
Observability changes
external dependencies
Sprint 7.12
RDD Stage 2
~~~

Sprint 7.10 permanece como la última ruta conversacional/runtime integrada.
No existe actualmente ninguna unidad posterior a Governed Input Projection
autorizada.

La sincronización del Malāk Project Vault es una proyección derivada posterior.
El Vault se encuentra sincronizado con el HEAD post-PR #88 y su estado no
modifica el cierre oficial del sprint ni concede autoridad sobre
`Aranwill/jarvis/main`.

---

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
│       ├── app/
│       ├── capabilities/
│       ├── contracts/
│       ├── core/
│       ├── events/
│       ├── identity/
│       ├── infrastructure/
│       ├── kernel/
│       ├── memory/
│       ├── observability/
│       ├── providers/
│       ├── runtime/
│       ├── security/
│       ├── services/
│       └── shared/
├── tests/
├── CHANGELOG.md
├── PROJECT.md
├── README.md
├── ROADMAP.md
├── SECURITY.md
└── pyproject.toml
```

`D:\Ollama` es el espacio de trabajo contenedor y no la raíz Git. Los comandos del repositorio deben ejecutarse desde:

```text
D:\Ollama\jarvis
```

---

## Arquitectura implementada actual

### Flujo Kernel–Planner–Capability

La frontera cognitiva oficial permanece orientada al Kernel:

```text
Interface Layer
→ Application Composition
→ Kernel.receive()
→ Planner
→ CapabilityRegistry
→ Capability
→ Response
```

El Kernel:

- coordina el flujo;
- permanece independiente de providers concretos;
- permanece independiente de runtimes concretos;
- permanece independiente de modelos concretos;
- no depende directamente de Ollama;
- no contiene lógica de configuración de infraestructura;
- no incorpora autoridad autónoma;
- no accede directamente a Internet;
- no debe convertirse en orquestador de infraestructura.

El bootstrap mínimo del Kernel conserva `EchoCapability` como Capability
determinista para validaciones estructurales.

La composición conversacional vigente es distinta: se construye en la frontera
de aplicación, registra `ConversationCapability` y configura el `Planner` para
resolver esa capability sin introducir `ConversationService`, providers,
runtimes o modelos dentro del Kernel.

### Stack conversacional

El stack conversacional implementado contiene:

- `ConversationCapability`;
- `ConversationMessage`;
- `ConversationRequest`;
- `ConversationResponse`;
- `ConversationProvider`;
- `RuntimeConversationProvider`;
- `ConversationProviderRegistry`;
- `ConversationProviderNotFoundError`;
- `ConversationService`;
- `InMemoryConversationContext`;
- `LLMRuntime`;
- `MockLLMRuntime`;
- `OllamaRuntime`.

Ruta cognitiva conversacional vigente:

```text
CLI
→ CLIConfiguration
→ Application Composition
→ Kernel.receive()
→ Planner
→ CapabilityRegistry
→ ConversationCapability
→ ConversationService
→ ConversationProviderRegistry
→ RuntimeConversationProvider
→ LLMRuntime
→ Response
```

La selección y construcción del runtime, provider y servicios se realiza en la
frontera de aplicación mediante configuración externa.

Sprint 7.9 añadió continuidad conversacional efímera mediante
`InMemoryConversationContext`, integrada opcionalmente en `ConversationService`
y mantenida fuera del Kernel y de `SecurityContext`.

Sprint 7.10 añade aislamiento explícito de sesiones conversacionales.
`Request.session_id` se preserva a través de la frontera de Capability,
`ConversationService` selecciona el contexto mediante esa identidad y
`InMemoryConversationContext` mantiene ventanas independientes por sesión.

La evolución no introduce persistencia, Memory ni estado conversacional
dentro del Kernel o de `SecurityContext`.

### Episodic Memory Admission chain — estado post-PR #88

La Memory Layer posee ahora varias fronteras aisladas bajo:

~~~text
src/malak/memory/
~~~

La policy de admisión original permanece pura y determinista:

~~~text
EpisodicMemoryCandidate
+
EpisodicAdmissionSignals
        ↓
REJECT | HOLD | ELIGIBLE
~~~

Sobre esa foundation se integró una cadena de evidencia y proyección separada:

~~~text
AdmissionAssessment
        ↓
Assessment Provenance
VALID | HOLD | INVALID
        ↓
Assessment Producer Authorization
AUTHORIZED | HOLD | DENIED
        ↓
Governed Input Projection
READY | HOLD | DENIED
        ↓
STOP
~~~

La proyección reconstruye un `EpisodicAdmissionContext` y
`EpisodicAdmissionSignals` efectivos solo cuando existe evidencia completa,
coherente, candidate-bound y autorizada. Source authority, confidence,
sensitivity y temporal validity no se heredan como trust por mera presencia en
`candidate.control`.

Se preservan explícitamente:

~~~text
Candidate != Decision
payload != control metadata
source authority != confidence != security trust != temporal validity
structural provenance != authenticated identity
AUTHORIZED != trusted truth
Projection READY != Admission ELIGIBLE
ELIGIBLE != persistence authorization
HOLD != retention authorization
~~~

La projection no ejecuta Admission y no modifica la precedencia de la policy.
Un wiring posterior deberá ser autorizado de forma independiente.

Toda la cadena continúa desconectada de `ConversationCapability`,
`ConversationService`, Kernel y observabilidad; tampoco persiste ni recupera
Memory.

### Integración Kernel–ConversationService

Sprint 7.8 estableció y validó formalmente la integración entre el pipeline
cognitivo y el subsistema conversacional mediante `ConversationCapability`.

La frontera preservada es:

```text
Kernel
→ Capability
```

`ConversationCapability` adapta la solicitud del pipeline cognitivo al contrato
de `ConversationService` y transforma su resultado para devolverlo por la
frontera de Capability.

Por lo tanto:

- `Kernel.receive()` y `ConversationService` ya forman parte de una misma ruta
  cognitiva conversacional validada;
- el Kernel no conoce `ConversationService`;
- el Kernel no conoce providers concretos;
- el Kernel no conoce runtimes concretos;
- el Kernel no conoce modelos concretos;
- la evidencia de ejecución no concede autoridad ni altera el flujo de control.

---

## Abstracción de runtime

`LLMRuntime` permanece como el único punto de abstracción para integraciones de runtime LLM.

Runtimes implementados:

- `MockLLMRuntime`;
- `OllamaRuntime`.

### MockLLMRuntime

Uso:

- desarrollo;
- pruebas deterministas;
- validaciones reproducibles;
- ejecución sin servicio externo.

### OllamaRuntime

Estado:

```text
implementado
```

Características:

- integración local con Ollama;
- composición externa al Kernel;
- configuración mediante variables de entorno;
- validación de entrada;
- manejo de errores HTTP;
- manejo de errores de conexión;
- manejo de timeout;
- validación de payloads;
- soporte para métricas mediante interfaces desacopladas.

La integración real fue validada durante Sprint 7.8 con `OllamaRuntime` y un modelo local, sin convertir Ollama en dependencia del Kernel.

---

## Métricas, eventos operativos y auditoría

Los tres subsistemas permanecen separados.

### Métricas

Se utilizan para medir rendimiento y comportamiento cuantificable.

El repositorio contiene:

- muestras normalizadas de métricas;
- almacenamiento en memoria;
- almacenamiento JSONL;
- perfiles de rendimiento;
- generación de perfiles estadísticos.

### Eventos operativos

Sprint 7.4 incorporó:

- `OperationalEvent`;
- `OperationalEventSink`;
- stores operativos separados;
- correlación mediante `request_id`;
- integración opcional desde la CLI.

### Auditoría de seguridad

Sprint 7.5 incorporó evidencia estructurada de autorización separada de métricas y eventos operativos.

No existe un envelope universal entre métricas, eventos y auditoría.

No comparten:

- contratos;
- stores;
- políticas de error;
- políticas de retención;
- autoridad.

Pueden compartir únicamente convenciones mínimas de trazabilidad.

---

## Security Control Plane Foundation

El Sprint 7.5 está cerrado.

La fundación implementada establece separación entre:

```text
solicitar
→ decidir
→ aplicar
→ auditar
→ ejecutar operación protegida
```

Componentes fundamentales:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`;
- Policy Decision Point mínimo;
- Policy Enforcement Point inicial;
- contratos de auditoría de autorización;
- integración fail-closed de la evidencia de auditoría.

### Policy Decision Point

Propiedades:

- determinista;
- sin LLM;
- denegación por defecto;
- fail-closed;
- confirmación humana explícita cuando corresponde;
- ninguna confirmación modifica retroactivamente una decisión anterior.

### Policy Enforcement Point

Propiedades:

- consulta directamente al PDP inyectado;
- no acepta decisiones aportadas por el llamador;
- exige asociación consistente entre solicitud y decisión;
- ejecuta la operación protegida únicamente ante una decisión válida y permitida;
- bloquea ante errores, incongruencias o respuestas inválidas;
- permanece separado del Kernel y del Planner.

### Auditoría de autorización

La evidencia de autorización:

- es estructurada;
- permanece separada de métricas y eventos operativos;
- forma parte del comportamiento fail-closed;
- no concede autoridad;
- no reemplaza la decisión de autorización.

---

## Secure Context Lifecycle Foundation

El Sprint 7.6 está cerrado.

La fundación implementada establece un lifecycle temporal explícito para
`SecurityContext`, sin ampliar autoridad ni introducir todavía identidad
criptográfica o transporte seguro entre procesos.

Componentes incorporados o consolidados:

- `SecurityContext` con `context_id`, `session_id`, `subject_id`,
  `authenticated`, `issued_at`, `expires_at` y `parent_context_id`;
- frontera temporal `Clock` / `SystemClock`;
- `SecurityContextValidator`;
- `SecurityContextIssuer`;
- `SecurityContextRenewer`;
- enforcement temporal en `StaticPolicyDecisionPoint`;
- semántica de validez `issued_at <= now < expires_at`;
- `SecurityContextEnvelope` para propagación inmutable en memoria.

Propiedades relevantes:

- contextos futuros son inválidos antes de `issued_at`;
- contextos expiran exactamente en `expires_at`;
- la renovación exige que el contexto anterior continúe vigente;
- la renovación preserva sesión, sujeto y estado de autenticación;
- cada renovación genera un nuevo `context_id` y conserva lineage mediante
  `parent_context_id`;
- el PDP valida lifecycle antes de evaluar políticas;
- la propagación conserva el mismo `SecurityContext` sin reconstruirlo;
- Validator, Issuer, Renewer y Envelope no conceden permisos;
- Kernel, Planner y runtimes permanecieron fuera del alcance.

Permanecen fuera de alcance:

- nonce y replay protection;
- identidad y firmas criptográficas;
- MFA;
- Secure Context Manager criptográfico completo;
- Secure Message Bus;
- IPC seguro;
- receipts / RDD;
- agentes, navegación y rutas operativas reales de alto riesgo.

---

## Riesgo de seguridad residual

Permanece registrado el finding:

```text
7.7-D-001 — Strong SecurityContext Provenance
classification: ACCEPTED_RESIDUAL_RISK
severity: MEDIUM
blocking_release: NO
```

La foundation actual todavía no incorpora de forma completa:

- PKI;
- nonce;
- replay protection;
- identidad criptográfica fuerte;
- MFA;
- Secure Message Bus;
- Secure Context Manager criptográfico completo.

Este riesgo no bloquea el baseline actual, pero debe permanecer visible antes de
incorporar agentes, tools, red, mensajería externa, automatización o rutas
operativas de mayor riesgo.

Su existencia no autoriza por sí sola una implementación de seguridad adicional.

---

## Estado de sprints

Estado del bloque 7.x:

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición de CLI con `OllamaRuntime` |
| 7.2 | Cerrado | `RuntimeMetricSink` |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Logs, métricas, eventos operativos y sincronización gobernada |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Validación de baseline y release interna |
| 7.8 | Completado | Cognitive Conversation Execution Path Foundation |
| 7.9 | Completado | Conversation Continuity Foundation; cierre aprobado por el propietario |
| 7.10 | Completado | Conversation Session Isolation Foundation; integrado y validado post-merge |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation; integrado y validado post-merge |

Las unidades episódicas integradas después de Sprint 7.11 no constituyen Sprint
7.12 y no alteran la numeración histórica del bloque 7.x.

### Sprint 7.0

Estado:

```text
cerrado
```

Resultado:

- CLI técnica mínima;
- soporte para `MockLLMRuntime`;
- comandos básicos;
- control de errores;
- sin integración formal con `Kernel.receive`.

### Sprint 7.1

Estado:

```text
cerrado
```

Resultado:

- soporte para `OllamaRuntime`;
- configuración externa;
- Runtime Independence preservada;
- Kernel sin modificación.

### Sprint 7.2

Estado:

```text
cerrado
```

Resultado:

- `RuntimeMetricSink`;
- contrato estructural de solo escritura;
- separación respecto de stores concretos.

### Sprint 7.3

Estado:

```text
cerrado
```

Resultado:

- estabilización del límite entre `ConversationService`, provider y runtime;
- incorporación de `RuntimeConversationProvider`;
- fortalecimiento de `ConversationProviderRegistry`;
- manejo explícito de provider inexistente;
- Kernel y Planner intactos.

### Sprint 7.4

Estado:

```text
cerrado
```

Resultado:

- consolidación de eventos operativos;
- correlación desde CLI;
- separación entre métricas, eventos y auditoría;
- sincronización gobernada del Vault.

### Sprint 7.5

Estado:

```text
cerrado
```

Resultado:

- contratos fundamentales de autorización;
- PDP mínimo determinista;
- PEP inicial;
- auditoría de autorización;
- revisión integral y cierre;
- sin habilitar rutas operativas reales de alto riesgo.

El cierre del Sprint 7.5 no autoriza automáticamente ningún sprint posterior.

### Sprint 7.6

Estado:

```text
cerrado
```

Resultado:

- lifecycle temporal explícito para `SecurityContext`;
- frontera `Clock`;
- validación temporal determinista;
- emisión y renovación con lineage;
- enforcement fail-closed en PDP;
- semántica `issued_at <= now < expires_at`;
- propagación inmutable en memoria mediante `SecurityContextEnvelope`;
- Kernel, Planner y runtimes sin cambios;
- sin identidad criptográfica, replay protection ni Secure Message Bus.

El cierre del Sprint 7.6 no autoriza automáticamente Sprint 7.7 ni ninguna
implementación posterior.

### Sprint 7.7

Estado:

```text
cerrado
```

Resultado:

- validación integral y certificación interna del baseline;
- reconciliación de arquitectura y documentación;
- cierre del proceso de certificación;
- preservación de `7.7-D-001` como riesgo residual aceptado, MEDIUM y no bloqueante.

### Sprint 7.8

Estado:

```text
completado
```

Resultado:

- primera ruta cognitiva conversacional end-to-end;
- incorporación de `ConversationCapability` como adapter detrás de la frontera de Capability;
- integración `Kernel.receive()` → `Planner` → `CapabilityRegistry` → `ConversationCapability`;
- preservación de Runtime Independence;
- validación determinista con `MockLLMRuntime`;
- validación real con `OllamaRuntime`;
- 348 pruebas totales aprobadas durante el cierre documentado.

El cierre de Sprint 7.8 no autorizó automáticamente Sprint 7.9 ni ninguna otra
unidad de implementación.

Sprint 7.9 fue autorizado posteriormente mediante un proceso independiente de
inspección, definición, evaluación, debate y aprobación explícita.

### Sprint 7.9

Estado:

```text
completado
```

Objetivo autorizado:

- continuidad conversacional efímera durante una conversación activa;
- historial estructurado y limitado en memoria;
- limpieza explícita del contexto conversacional;
- integración aditiva y reversible;
- preservación de Kernel, Planner, Capability contract y SecurityContext.

Baseline de activación:

```text
2864435401353e5abcfcb51fc276361a0225c2b7
```

Rama temporal:

```text
sprint/7.9-conversation-continuity
```

Estado de ejecución:

```text
gates 7.9-A → 7.9-H: PASS
candidato funcional validado: d58b8ec98d48f5e2eac115d1d54b193e1df617fd
suite final: 365 passed
runtime real: PASS
revisión final 4R: PASS
cierre del sprint: aprobado por el propietario el 2026-09-03
```

Sprint 7.9 no autoriza Memory persistente, agentes, tools, Sandbox, navegación,
Internet, RAG, GraphRAG, cambios del Kernel, generalización del contrato
Capability ni ampliación de autoridad.

---

## Validación

Última validación integral documentada durante el cierre de Sprint 7.8:

```text
348 total passed
compileall: PASS
git diff --check: PASS
```

La ruta cognitiva conversacional fue validada tanto con runtime determinista como
con `OllamaRuntime`, preservando el desacoplamiento del Kernel.

Antes de activar Sprint 7.9 se revalidó localmente el baseline de referencia:

```text
main == origin/main
commit reconciliado: 2864435401353e5abcfcb51fc276361a0225c2b7
working tree: clean
Python: 3.12.10
virtual environment: .venv
pytest: 348 passed
compileall: PASS
git diff --check: PASS
```

La validación anterior certifica el punto de partida técnico del sprint.

El candidato funcional de Sprint 7.9 fue validado posteriormente:

```text
candidate: d58b8ec98d48f5e2eac115d1d54b193e1df617fd
pytest: 365 passed
compileall: PASS
git diff --check baseline..candidate: PASS
runtime real: PASS
revisión final 4R: PASS
```

La implementación, validación y revisión están completas. El propietario
aprobó explícitamente el cierre del Sprint 7.9 el 2026-09-03.

La actualización de este documento registra evidencia y una autorización humana
ya emitida; no crea autoridad por sí misma ni autoriza ningún sprint posterior.

La evidencia candidate-bound más reciente de la cadena episódica corresponde al
candidate de PR #88 `87a7e31e0735edd25a80a693cf3f437f7a1501fc`, cuya ejecución
`Validation` concluyó con `success` en Ubuntu, Windows y macOS.

---

## Estado del baseline

Baseline nominal:

```text
v0.6.0-alpha
```

El baseline nominal no debe confundirse con el commit de desarrollo utilizado
como referencia de reconciliación.

Estado reconciliado:

```text
rama permanente: main
HEAD material de referencia: 2e8c5d7318678caeb67c8906c951935832760003
commit integración Sprint 7.11: 3413e8ccb348440aea757d1feccde25c65be011f
Sprint 7.7: cerrado
Sprint 7.8: completado
Sprint 7.9: completado
Sprint 7.10: completado
Sprint 7.11: completado e integrado
última ruta conversacional/runtime: Sprint 7.10
última unidad de producto: Episodic Admission Governed Input Projection Boundary
candidato final Sprint 7.11: 59f592e2e36d11bbd14f7d9d93b1dac4f442c108
certification branch activa: no
release promovida adicional: no
sprint actualmente autorizado: ninguno
unidad posterior autorizada: ninguna
RDD Stage 2: no autorizado
```

El commit `3413e8ccb348440aea757d1feccde25c65be011f` continúa siendo el estado de
`main` resultante de integrar Sprint 7.11, pero ya no es el HEAD material actual.

Sprint 7.11 no modificó el producto/runtime. La última ruta conversacional/runtime
permanece Sprint 7.10, mientras que las unidades episódicas posteriores ampliaron
la Memory Layer de forma aislada hasta Governed Input Projection.

No debe certificarse una nueva release, crear o mover un tag, abrir Sprint 7.12,
implementar el consumo `Projection → Admission` o ampliar autoridad sin un
proceso específico de evaluación y aprobación.

---

## Malāk Project Vault

Repositorio derivado:

```text
Aranwill/malak-project-vault
```

Rama:

```text
main
```

El Vault:

- permanece separado del repositorio oficial;
- es derivado;
- no tiene autoridad operativa;
- no puede modificar Malāk automáticamente;
- utiliza Obsidian únicamente como interfaz humana;
- conserva snapshots históricos inmutables;
- puede proyectar cambios detectados en el repositorio oficial;
- requiere revisión humana para reconciliaciones gobernadas.

El Vault fue sincronizado después de PR #88 con el HEAD oficial:

```text
2e8c5d7318678caeb67c8906c951935832760003
```

El repositorio oficial `Aranwill/jarvis/main` continúa siendo la fuente de verdad para:

- código;
- tests;
- documentación oficial;
- contratos;
- arquitectura;
- sprints;
- historial Git.

---

## Planificación vigente — post-PR #88

Sprint 7.8 está completado.

Sprint 7.9 fue completado y su cierre fue aprobado explícitamente por el
propietario el 2026-09-03.

Sprint 7.10 fue completado e integrado y su cierre fue aprobado explícitamente por el propietario el 2026-09-04.

Sprint 7.11 fue completado, integrado mediante PR #65 y validado nuevamente sobre `main`.

Después de Sprint 7.11 fueron integradas de forma separada Episodic Memory
Admission, Assessment Provenance, Assessment Producer Authorization y Governed
Input Projection. Ninguna de esas unidades constituye Sprint 7.12.

Actualmente:

```text
LAST COMPLETED NUMBERED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST CONVERSATIONAL/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

LATEST PRODUCT UNIT
Episodic Admission Governed Input Projection Boundary

ACTIVE AUTHORIZED SPRINT
NONE

SUBSEQUENT SPRINT
NONE AUTHORIZED

UNIT AFTER GOVERNED INPUT PROJECTION
NONE AUTHORIZED

RDD STAGE 2
NOT AUTHORIZED
```

La fuente derivada canónica para planificación es:

```text
docs/project/implementation_roadmap.md
```

La ficha operativa del último sprint numerado integrado es:

```text
docs/project/sprints/SPRINT-7.11.md
```

Las ideas registradas en `documents/projects/jarvis/ideas.md`, las referencias
de `docs/project/concepts/` y las iniciativas reconocidas para planificación
futura pueden informar la implementación únicamente dentro del alcance
autorizado.

Se mantiene:

```text
idea != roadmap
roadmap != aprobación
evidencia != autoridad
Projection READY != Admission ELIGIBLE
ELIGIBLE != Stored
```

`project_context.md` no duplica el roadmap ni concede autoridad.

Agentes, tools, red, navegación, mensajería externa, automatización y otras
rutas operativas de mayor riesgo continúan postergadas salvo autorización
independiente y foundations suficientes.

---

## Capacidades explícitamente postergadas

Hasta que un sprint o unidad aprobada las autorice, no se deben introducir:

- agentes autónomos;
- ejecución libre de herramientas externas;
- control autónomo del sistema operativo;
- navegación externa;
- comunicaciones externas automáticas;
- memoria persistente sensible sin controles aprobados;
- wiring `Projection → Admission` sin evaluación y autorización separadas;
- elevación automática de privilegios;
- acciones destructivas;
- integraciones externas ocultas;
- modificación automática de políticas;
- modificación automática del Kernel;
- autoaprobación de decisiones;
- cambios autónomos sobre Blueprint, Constituciones o Gobernanza.

---

## Restricciones permanentes de trabajo

Todo trabajo futuro debe preservar:

- Kernel First;
- Capability First;
- Runtime Independence;
- Vendor Independence;
- Human in Control;
- Zero Trust interno;
- Defense in Depth;
- denegación por defecto para acciones sensibles;
- mínimo privilegio;
- autorización explícita;
- contratos públicos estables;
- cambios pequeños, trazables y reversibles;
- separación entre autoridad cognitiva y autoridad de seguridad;
- trazabilidad completa.

La metodología vigente combina:

```text
SDD
+ TDD
+ 4R
+ Bounded Correction
+ Independent Validation
```

ADR-003 preserva la dirección de autoridad:

```text
CONTROL / AUTHORITY
Upstream → Downstream

RESULTS / EVENTS / EVIDENCE
Downstream → Upstream
```

La evidencia puede informar una decisión, pero nunca concede autoridad.

ADR-004 establece `Specification & Verification First`: todo cambio
significativo debe definir comportamiento esperado y criterios verificables antes
de ser aceptado en el baseline.

Antes de cualquier modificación importante se deben responder las cuatro
preguntas obligatorias:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Preserva o reduce la complejidad del Kernel?

Si alguna respuesta es negativa, dudosa o carece de evidencia suficiente, el
trabajo debe detenerse antes de editar.

---

## Artefactos protegidos

No modificar sin autorización explícita y proceso de gobernanza aplicable:

- Kernel;
- contratos centrales;
- Blueprint;
- Constitución Cognitiva;
- Constitución de Gobernanza;
- políticas de seguridad;
- ADR aceptados;
- fundamentos de seguridad;
- snapshots históricos;
- metadatos de release.

Ningún agente, runtime, capability o herramienta puede modificar estos artefactos durante operación normal.

---

## Disciplina de sprints

La evolución de Malāk debe mantener una cadena explícita de promoción:

```text
idea o necesidad real
→ evaluación
→ roadmap cuando corresponda
→ specification
→ ADR cuando corresponda
→ alcance aprobado
→ rama temporal
→ TDD / implementación
→ 4R
→ Bounded Correction cuando sea necesaria
→ Independent Validation
→ evidencia
→ Draft Pull Request
→ revisión visual humana
→ promoción humana a Ready for Review
→ autorización humana de merge
→ baseline
```

No todos los cambios requieren un sprint funcional. Una corrección documental
acotada puede ejecutarse como corrective packet independiente cuando el alcance,
la evidencia y la autoridad estén explícitamente delimitados.

Una fase no se considera cerrada hasta que:

- código, cuando aplique;
- tests, cuando apliquen;
- documentación;
- evidencia relevante;
- estado del repositorio

estén reconciliados.

No se debe iniciar el siguiente sprint o unidad funcional hasta evaluar el
baseline resultante y obtener aprobación explícita.

---

## Política de actualización

Este documento fue reconciliado contra el estado observado después de integrar
PR #88 — `Episodic Admission Governed Input Projection Boundary`:

```text
main@2e8c5d7318678caeb67c8906c951935832760003
active_work_branch@NONE
```

`as_of_commit` identifica el commit de referencia utilizado para reconstruir el
contexto, no una obligación de reescribir el documento ante cada commit
puramente mecánico o documental.

Debe volver a validarse cuando:

- `HEAD` cambie de manera material para el contexto descrito;
- un sprint se formalice, active o cierre;
- una unidad funcional aislada relevante se integre;
- se certifique una nueva release;
- cambie arquitectura o gobernanza;
- cambien resultados de tests relevantes;
- cambie la raíz del repositorio;
- cambie el entorno de desarrollo de forma material;
- se incorpore una nueva frontera de seguridad;
- se modifique de forma material el estado operativo del Vault.

Las actualizaciones deben distinguir claramente entre:

- evidencia verificada del repositorio;
- registros históricos;
- estado derivado;
- contexto de planificación;
- decisiones normativas aprobadas.

Los registros históricos no deben reescribirse para aparentar que describen el
presente.

---

## Declaración de ausencia de autoridad normativa

Este documento no puede:

- aprobar un sprint;
- autorizar una implementación;
- modificar arquitectura;
- cambiar gobernanza;
- redefinir el Kernel;
- modificar contratos;
- certificar una release;
- anular un ADR;
- convertir una propuesta en alcance aprobado;
- conceder permisos;
- ampliar autoridad operativa.

Su único propósito es proporcionar un snapshot de contexto trazable, actualizado y conveniente.
