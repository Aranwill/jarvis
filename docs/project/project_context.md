---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-09-02
as_of_commit: e3c28131f491b740c352da79537cd9233d7f4979
branch: main
certification_branch: null
candidate_commit: e3c28131f491b740c352da79537cd9233d7f4979
certification_status: sprint_7_8_completed
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
- estado sincronizado del Malāk Project Vault.

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
Repositorio oficial:      Aranwill/jarvis
Raíz Git local:           D:\Ollama\jarvis
Rama permanente:          main
Commit reconciliado:      e3c28131f491b740c352da79537cd9233d7f4979
Baseline nominal:         v0.6.0-alpha
Último sprint funcional:  Sprint 7.8 — Cognitive Conversation Execution Path Foundation
Próximo sprint:           ninguno autorizado
```

El commit de referencia reconciliado en `main` es:

```text
e3c28131 Merge pull request #50 from Aranwill/docs/human-only-pr-promotion
```

Sprint 7.8 permanece como el último sprint funcional completado. Los cambios
posteriores a su cierre que ya forman parte de `main` son cambios documentales,
de gobernanza o de disciplina de ingeniería y no autorizan automáticamente una
nueva unidad de implementación.

La rama `main` es la única rama permanente y debe tratarse como fuente del
baseline operativo actual.

Las ramas temporales de documentación, feature, corrección o sprint no
constituyen baseline hasta su integración y validación.

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
- `ConversationRequest`;
- `ConversationResponse`;
- `ConversationProvider`;
- `RuntimeConversationProvider`;
- `ConversationProviderRegistry`;
- `ConversationProviderNotFoundError`;
- `ConversationService`;
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

El cierre de Sprint 7.8 no autoriza automáticamente Sprint 7.9 ni ninguna otra
unidad de implementación.

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

Antes de abrir el corrective packet documental actual se revalidó el baseline de
referencia:

```text
main == origin/main
commit reconciliado: e3c28131f491b740c352da79537cd9233d7f4979
working tree: clean
```

Antes de iniciar cualquier nueva implementación debe revalidarse localmente:

- rama actual;
- sincronización con `origin/main`;
- working tree;
- versión de Python;
- dependencias;
- suite completa;
- `compileall`;
- `git diff --check`.

La corrección de este documento no sustituye una validación funcional ni
autoriza el siguiente sprint.

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
commit de referencia: e3c28131f491b740c352da79537cd9233d7f4979
Sprint 7.7: cerrado
Sprint 7.8: completado
certification branch activa: no
release promovida adicional: no
próximo sprint autorizado: ninguno
```

El commit `e3c28131f491b740c352da79537cd9233d7f4979` es el estado de `main`
contra el cual se realiza esta reconciliación documental. Un commit documental
posterior que contenga esta corrección no altera por sí mismo el último baseline
funcional ni autoriza una nueva implementación.

No debe certificarse una nueva release, crear o mover un tag, abrir un sprint o
ampliar autoridad sin un proceso específico de evaluación y aprobación.

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

El repositorio oficial `Aranwill/jarvis/main` continúa siendo la fuente de verdad para:

- código;
- tests;
- documentación oficial;
- contratos;
- arquitectura;
- sprints;
- historial Git.

---

## Planificación posterior al Sprint 7.8

Sprint 7.8 está completado.

Actualmente:

```text
NEXT SPRINT
NONE AUTHORIZED
```

La fuente derivada canónica para planificación es:

```text
docs/project/implementation_roadmap.md
```

Las ideas registradas en `documents/projects/jarvis/ideas.md`, las referencias
de `docs/project/concepts/` y las iniciativas reconocidas para planificación
futura pueden alimentar una evaluación posterior, pero:

```text
idea != roadmap
roadmap != aprobación
evidencia != autoridad
```

`project_context.md` no debe duplicar el roadmap ni establecer por sí mismo la
secuencia del trabajo futuro.

Antes de seleccionar la próxima unidad deberán compararse las necesidades reales
del baseline, riesgos, dependencias, arquitectura, seguridad, complejidad del
Kernel y evidencia disponible.

En particular, agentes, tools, red, navegación, mensajería externa,
automatización y otras rutas operativas de mayor riesgo no deben adelantarse
mientras sus foundations de seguridad, gobernanza, contención y evidencia no
estén suficientemente justificadas y aprobadas.

---

## Capacidades explícitamente postergadas

Hasta que un sprint aprobado las autorice, no se deben introducir:

- agentes autónomos;
- ejecución libre de herramientas externas;
- control autónomo del sistema operativo;
- navegación externa;
- comunicaciones externas automáticas;
- memoria persistente sensible sin controles aprobados;
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

No se debe iniciar el siguiente sprint hasta evaluar el baseline resultante y
obtener aprobación explícita.

---

## Política de actualización

Este documento fue reconciliado contra el estado observado:

```text
main@e3c28131f491b740c352da79537cd9233d7f4979
```

`as_of_commit` identifica el commit de referencia utilizado para reconstruir el
contexto, no una obligación de reescribir el documento ante cada commit
puramente mecánico o documental.

Debe volver a validarse cuando:

- `HEAD` cambie de manera material para el contexto descrito;
- un sprint se formalice, active o cierre;
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
