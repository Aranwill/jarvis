---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-08-16
as_of_commit: 34c711c7ecd73fb4187d675e1be6efbeee8c8b3
branch: main
certification_branch: sprint/7.7-baseline-certification
candidate_commit: 34c711c7ecd73fb4187d675e1be6efbeee8c8b3
certification_status: sprint_7_7_active
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
- resultados de validación registrados durante el cierre del Sprint 7.6;
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

- `repository_analysis.md`;
- este `project_context.md`;
- resúmenes de estado marcados explícitamente como no normativos;
- artefactos derivados del Malāk Project Vault.

Los documentos derivados pueden informar evidencia y contexto de planificación, pero no pueden aprobar arquitectura, alcance de sprint ni implementación.

---

## Snapshot validado del repositorio

```text
Repositorio oficial:   Aranwill/jarvis
Raíz Git local:        D:\Ollama\jarvis
Rama permanente:       main
HEAD observado:        34c711c7ecd73fb4187d675e1be6efbeee8c8b3
Baseline nominal:      v0.6.0-alpha
Último sprint cerrado: Sprint 7.6 — Secure Context Lifecycle Foundation
Próximo sprint:        ninguno autorizado
```

Último cambio observado en `main`:

```text
8214974 Merge pull request #42 from Aranwill/sprint/7.6-h-context-propagation-contract
```


El cambio funcional más reciente integrado en `main` cerró el alcance técnico del Sprint 7.6 mediante la PR #42, incorporando el contrato de propagación contextual sobre el lifecycle ya validado. Esta integración no autoriza Sprint 7.7 ni ninguna implementación posterior.

La rama `main` es la única rama permanente y debe tratarse como fuente del baseline operativo actual.

Las ramas temporales de documentación, feature, corrección o sprint no constituyen baseline hasta su integración y validación.

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
│       ├── capabilities/
│       ├── contracts/
│       ├── core/
│       ├── events/
│       ├── identity/
│       ├── infrastructure/
│       ├── kernel/
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

El flujo orientado al Kernel permanece:

```text
Interface Layer
→ Kernel
→ Planner
→ Capability Registry
→ Capability
→ Response
```

La ruta de código implementada comienza en `Kernel.receive`.

El Kernel:

- coordina el flujo;
- permanece independiente de proveedores concretos;
- permanece independiente de runtimes concretos;
- no depende directamente de Ollama;
- no contiene lógica de configuración de infraestructura;
- no incorpora autoridad autónoma;
- no accede directamente a Internet;
- no debe convertirse en orquestador de infraestructura.

El registry predeterminado contiene `EchoCapability`, utilizada como Capability mínima y determinista para validar el flujo Kernel–Planner–Capability.

### Stack conversacional

El stack conversacional implementado contiene:

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

Ruta técnica vigente:

```text
CLI
→ ConversationService
→ ConversationProviderRegistry
→ RuntimeConversationProvider
→ LLMRuntime
```

La CLI permite composición externa del runtime mediante configuración, sin modificar el Kernel.

### Límite de integración Kernel–ConversationService

No existe una integración formal y validada entre:

```text
Kernel.receive
```

y:

```text
ConversationService
```

Por lo tanto:

- el pipeline Kernel–Planner–Capability y el stack conversacional continúan siendo rutas separadas;
- la CLI técnica no representa por sí sola el pipeline cognitivo completo de Malāk;
- no debe introducirse un puente entre ambas rutas sin necesidad funcional concreta, contrato explícito y aprobación humana.

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

La integración real fue validada anteriormente con un modelo local, sin convertir Ollama en dependencia del Kernel.

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
| 7.7 | Activo | Certificación de baseline; 7.7-A y 7.7-B completados; 7.7-C en curso |

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

---

## Validación

Última validación integral documentada del cierre del Sprint 7.6:

```text
339 total passed
compileall: PASS
git diff --check: PASS
working tree: clean
```

La revisión integral no registró defectos bloqueantes.

Todos los incrementos 7.6-A a 7.6-H fueron revisados mediante 4R y aceptados
humanamente antes de consolidar el cierre.

Kernel, Planner y runtimes permanecieron intactos durante el Sprint 7.6.

Antes de iniciar cualquier nueva implementación debe revalidarse localmente:

- rama actual;
- sincronización con `origin/main`;
- working tree;
- versión de Python;
- dependencias;
- suite completa;
- `compileall`;
- `git diff --check`.

---

## Estado del baseline

Baseline nominal:

```text
v0.6.0-alpha
```

El tag nominal no debe confundirse con el HEAD de desarrollo actual.

El baseline integrado vigente en `main` continúa siendo la referencia operativa
estable previa a la certificación.

El proceso de certificación actual evalúa un candidate baseline separado:

```text
baseline integrado previo: main
candidate técnico: 34c711c7ecd73fb4187d675e1be6efbeee8c8b3
rama de certificación: sprint/7.7-baseline-certification
Sprint 7.7: activo
7.7-A: completado
7.7-B: completado
7.7-C: en curso
release promovida: no
```

No debe certificarse una nueva release ni crearse un nuevo tag sin un proceso específico de validación y aprobación.

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

## Propuestas posteriores al Sprint 7.6

Sprint 7.7 está autorizado y activo como proceso formal de certificación de baseline y release interna.

Existen propuestas documentales preliminares para:

- preparación del AKS para futura representación como grafo;

Su existencia, numeración o posición no constituye autorización.

Tampoco se consideran autorizadas por defecto:

- Secure Context Manager criptográfico completo;
- identidad criptográfica completa;
- nonce y replay protection;
- prevención persistente de replay;
- persistencia avanzada de auditoría;
- agentes;
- navegación;
- herramientas externas;
- memoria sensible;
- automatización del sistema operativo;
- Evidence Acquisition Foundation;
- Sandbox Containment;
- GraphRAG;
- capacidades ofensivas o autónomas.

Cada iniciativa debe atravesar gobernanza, alcance, riesgos, dependencias, rollback y aprobación humana.

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

Antes de cualquier modificación importante se deben responder las cuatro preguntas obligatorias:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Hace al Kernel más simple o más complejo?

Si alguna respuesta es negativa o dudosa, la implementación debe detenerse y rediseñarse antes de escribir código.

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

La metodología vigente es:

```text
necesidad real
→ análisis arquitectónico
→ alcance aprobado
→ rama temporal
→ implementación pequeña
→ pruebas
→ validación
→ documentación
→ Pull Request
→ revisión
→ merge
→ baseline estable
```

Una fase no se considera cerrada hasta que:

- código;
- tests;
- documentación;
- telemetría relevante;
- estado del repositorio

estén sincronizados.

No se debe iniciar el siguiente sprint hasta aceptar explícitamente el nuevo baseline.

---

## Política de actualización

Este documento está vinculado al estado observado:

```text
34c711c7ecd73fb4187d675e1be6efbeee8c8b3
```

Debe volver a validarse cuando:

- `HEAD` cambie de manera material;
- un sprint se formalice, active o cierre;
- se certifique una nueva release;
- cambie arquitectura o gobernanza;
- cambien resultados de tests;
- cambie la raíz del repositorio;
- cambie el entorno de desarrollo;
- se incorpore una nueva frontera de seguridad;
- se modifique el estado operativo del Vault.

Las actualizaciones deben distinguir claramente entre:

- evidencia verificada del repositorio;
- registros históricos;
- estado derivado;
- contexto de planificación;
- decisiones normativas aprobadas.

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
