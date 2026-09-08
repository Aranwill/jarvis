---
title: Hoja de ruta de implementación de Malāk
status: activo
authority: no normativa
document_role: canonical_derived_implementation_roadmap
as_of_date: 2026-09-08
as_of_commit: 3413e8ccb348440aea757d1feccde25c65be011f
branch: main
baseline: v0.6.0-alpha
certification_branch: null
candidate_commit: 59f592e2e36d11bbd14f7d9d93b1dac4f442c108
certification_status: sprint_7_11_completed
legacy_planning_source:
  - docs/project/roadmap.md
language: es
---

# Hoja de ruta de implementación de Malāk

## Propósito

Este documento constituye la fuente derivada canónica para consultar la
planificación de implementación vigente de Malāk.

Centraliza:

- estado de referencia del baseline;
- sprints completados;
- estado de autorización de nuevas unidades;
- iniciativas incorporadas a planificación futura;
- propuestas pendientes;
- disposición de planificación legacy;
- relaciones entre ideas, concepts y fichas de sprint.

Este documento es deliberadamente **derivado y no normativo**.

No reemplaza ni modifica ninguna fuente de ley, arquitectura, seguridad,
gobernanza o contrato aprobado.

---

# 1. Clasificación y autoridad

Este roadmap:

- no aprueba arquitectura;
- no modifica arquitectura;
- no autoriza implementación;
- no reemplaza fuentes normativas;
- no establece automáticamente el próximo sprint;
- no convierte una recomendación en obligación;
- no concede autoridad a ningún componente;
- no puede utilizarse para modificar documentos protegidos.

Ante conflicto prevalece la jerarquía documental oficial de Malāk.

```text
roadmap != autorización
idea != roadmap
concept != baseline
evidence != authority
```

---

# 2. Regla de admisión de nuevas unidades

La existencia, numeración, posición, título o ficha de un sprint no constituye
autorización para implementarlo.

Toda nueva unidad debe someterse, como mínimo, a:

1. verificación de `main` y del HEAD exacto;
2. inspección del baseline vigente;
3. inventario y clasificación de fuentes aplicables;
4. revisión de código, pruebas y documentación relevantes;
5. identificación de una necesidad real y comprobada;
6. contraste con roadmap, `ideas.md` y `concepts/**`;
7. clasificación ADOPT / ADAPT / OBSERVE / REJECT cuando aplique;
8. definición de alcance y fuera de alcance;
9. evaluación de riesgos, dependencias y rollback;
10. validación mediante las cuatro preguntas obligatorias;
11. especificación verificable;
12. aprobación explícita e inequívoca del propietario.

La aprobación de una unidad anterior no autoriza automáticamente la siguiente.

---

# 3. Modelo documental de planificación

```text
ROADMAP.md
   │
   ▼
docs/project/implementation_roadmap.md
   │
   ├── references → documents/projects/jarvis/ideas.md
   ├── references → docs/project/concepts/**
   └── references → docs/project/sprints/SPRINT-*.md
```

## `ROADMAP.md`

Punto de entrada pequeño. No debe duplicar estado detallado.

## `implementation_roadmap.md`

Fuente derivada canónica para planificación vigente.

## `ideas.md`

Registro de ideas, visión e iniciativas. Una idea no se convierte
automáticamente en roadmap.

## `concepts/**`

Referencias conceptuales no normativas. Informan evaluación, pero no autorizan
implementación.

## `sprints/`

Evidencia de ejecución, validación y cierre de unidades concretas. No debe actuar
como segundo roadmap.

---

# 4. Estado de referencia

```text
REPOSITORY
Aranwill/jarvis

PERMANENT BRANCH
main

SOURCE HEAD
3413e8ccb348440aea757d1feccde25c65be011f

NOMINAL BASELINE
v0.6.0-alpha

LAST INTEGRATED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST PRODUCT/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

ACTIVE AUTHORIZED SPRINT
NONE

ACTIVE IMPLEMENTATION BRANCH
NONE

RDD STAGE 1
ADOPTED

RDD STAGE 2
NOT AUTHORIZED
```

Sprint 7.11 fue integrado mediante PR #65.

```text
baseline:
deb759ee9855737a24b169e03bde2028c7db7f33

candidate:
59f592e2e36d11bbd14f7d9d93b1dac4f442c108

merge commit:
3413e8ccb348440aea757d1feccde25c65be011f
```

Evidencia del candidato final:

```text
pytest:                 388 passed
compileall:             PASS
diff-check:             PASS
FULL 4R:                PASS
independent validation: PASS
G0–G6:                  PASS
```

La validación post-merge de GitHub Actions sobre el HEAD integrado concluyó con
`success`.

---

# 5. Arquitectura implementada relevante para planificación

El Kernel permanece desacoplado de:

- runtimes concretos;
- providers concretos;
- modelos concretos;
- configuración externa de runtime.

Ruta cognitiva conversacional implementada:

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
  ↕
InMemoryConversationContext
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
Response
```

Sprint 7.9 añadió continuidad conversacional efímera.

Sprint 7.10 añadió aislamiento por `session_id` sin introducir persistencia ni
Memory.

Separación vigente:

```text
Conversation History != Memory != Knowledge
```

La construcción de providers, runtimes, servicios y configuración permanece
fuera del Kernel.

La finalización de esta ruta no autoriza nuevas capabilities ni ampliación de
autoridad.

---

# 6. Security foundations implementadas

Sprint 7.5 estableció Security Control Plane Foundation:

```text
solicitar
→ decidir
→ aplicar
→ auditar
→ ejecutar operación protegida
```

Incluye:

- contratos de autorización;
- PDP determinista;
- PEP fail-closed;
- auditoría de autorización;
- default-deny;
- Human in Control.

Sprint 7.6 estableció Secure Context Lifecycle Foundation:

- `SecurityContext` temporal;
- `Clock` / `SystemClock`;
- `SecurityContextValidator`;
- `SecurityContextIssuer`;
- `SecurityContextRenewer`;
- lineage;
- `SecurityContextEnvelope`;
- enforcement temporal en PDP.

Riesgo residual preservado:

```text
7.7-D-001 — Strong SecurityContext Provenance
classification: ACCEPTED_RESIDUAL_RISK
severity: MEDIUM
blocking_release: NO
```

Continúan fuera del baseline actual:

- nonce y replay protection;
- identidad criptográfica fuerte;
- MFA;
- Secure Message Bus;
- Secure Context Manager criptográfico completo.

---

# 7. Validation Foundation — Sprint 7.11

Sprint 7.11 incorporó una pipeline mínima y reproducible:

```text
candidate / PR
    ↓
read-only GitHub Actions
    ↓
exact candidate identity
    ↓
pytest
compileall
candidate-bound diff-check
    ↓
technical evidence
```

Propiedades:

- `pull_request` y `push` a `main`;
- `permissions: contents: read`;
- sin `pull_request_target`;
- sin write permissions;
- sin secrets de entrega;
- `persist-credentials: false`;
- `fetch-depth: 0`;
- Windows + Python 3.12;
- `actions/checkout@v6`;
- `actions/setup-python@v6`;
- `pytest>=9,<10` solo como dependencia de desarrollo;
- `[project].dependencies = []` preservado.

Invariante:

```text
Evidence != Receipt != Validation != Decision != Authority
```

La pipeline no posee delivery authority.

---

# 8. Estado de sprints del bloque 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición con `OllamaRuntime` mediante configuración externa |
| 7.2 | Cerrado | `RuntimeMetricSink` de solo escritura |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Observabilidad y sincronización gobernada del Vault |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Validación integral y certificación interna |
| 7.8 | Completado | Cognitive Conversation Execution Path Foundation |
| 7.9 | Completado | Conversation Continuity Foundation |
| 7.10 | Completado | Conversation Session Isolation Foundation |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation |

Fichas canónicas:

```text
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

Los artefactos bajo `sprints/proposals/` preservan admisión, diseños o evidencia
intermedia y no deben reemplazar la ficha final de un sprint integrado.

---

# 9. Estado de autorización

```text
SPRINT 7.11 COMPLETADO E INTEGRADO
NINGUNA UNIDAD POSTERIOR AUTORIZADA
```

No está autorizado automáticamente:

- Sprint 7.12;
- cualquier otra unidad posterior;
- RDD Stage 2;
- Memory persistente;
- nuevas capabilities;
- agentes;
- tools;
- Sandbox;
- navegación;
- GraphRAG;
- ampliación de autoridad.

Toda unidad posterior deberá atravesar un proceso independiente de admisión y
aprobación.

---

# 10. Iniciativas reconocidas para planificación futura

Las siguientes iniciativas ya estaban incorporadas a planificación futura antes
de esta consolidación.

Su presencia aquí:

```text
NO autoriza diseño detallado
NO autoriza implementación
NO asigna sprint
```

## 10.1 Sandbox Containment & Evaluation Evidence Foundation

Propósito:

- aislamiento;
- entornos descartables;
- control de red, archivos y procesos;
- límites de recursos;
- telemetría externa al agente;
- evidencia reproducible;
- kill switch, timeout y cuarentena;
- pruebas de contención;
- revisión humana.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

## 10.2 Segmented Domain Governance Foundation

Propósito:

- preservar Malāk como control plane horizontal;
- permitir Domain Packs subordinados;
- impedir ampliación de autoridad desde capas inferiores;
- evitar contaminación del Kernel con lógica sectorial.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

## 10.3 Knowledge Intake & External Evidence Governance

Propósito:

- gobernar fuentes externas;
- conservar procedencia, autoridad, licencia y vigencia;
- tratar índices y grafos como proyecciones reconstruibles;
- incorporar saneamiento y validación;
- prevenir autocontaminación.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

## 10.4 Security Learning, Adversarial Evaluation & Deception

Propósito:

- laboratorios locales;
- CTF autorizados;
- aprendizaje defensivo;
- evaluación externa de agentes;
- deception defensiva aislada;
- transformar evidencia en propuestas defensivas.

Estado:

```text
Planificación futura reconocida.
Diseño detallado no aprobado.
Implementación no aprobada.
Sin número de sprint.
```

Estas iniciativas no habilitan agentes autónomos, navegación, malware,
honeypots públicos, pentesting no autorizado ni respuesta ofensiva.

Otras ideas preservadas en `ideas.md` continúan con el estado declarado allí y
no se promueven al roadmap por esta consolidación.

---

# 11. Legacy Planning & Disposition Registry

El archivo:

```text
docs/project/roadmap.md
```

contiene planificación temprana anterior a la arquitectura documental vigente.

```text
legacy != vigente
legacy != descartado
```

La consolidación preserva su valor histórico sin convertirlo en planificación
operativa.

## Estados de disposición

| Estado | Significado |
|---|---|
| `materializado` | Existe implementación o equivalente verificable |
| `parcialmente_materializado` | Parte de la intención existe |
| `preservado` | Intención futura todavía válida |
| `evolucionado` | Reformulada por arquitectura o concepto posterior |
| `candidato_tecnologico` | Tecnología candidata sin compromiso |
| `requiere_revision` | Falta evidencia para clasificar definitivamente |
| `hito_historico` | Se conserva principalmente por trazabilidad |

## Disposición principal

| Elemento legacy | Disposición | Interpretación actual |
|---|---|---|
| Ollama | `materializado` | Existe `OllamaRuntime` detrás de `LLMRuntime` |
| Open WebUI | `candidato_tecnologico`, `hito_historico` | No es componente obligatorio |
| Qwen2.5 | `candidato_tecnologico` | Modelo histórico/candidato |
| DeepSeek | `candidato_tecnologico` | Modelo histórico/candidato |
| Validación RAG | `preservado` | RAG continúa como capacidad futura |
| Optimización embeddings | `preservado` | Relevante para recuperación futura |
| Base documental | `evolucionado` | Evolucionó hacia Knowledge / AKS / retrieval |
| n8n | `candidato_tecnologico` | No es requisito arquitectónico |
| Automatizaciones | `preservado` | Capacidad futura gobernada |
| ChromaDB | `hito_historico`, `candidato_tecnologico` | Vector store futuro debe ser sustituible |
| Memoria Documental | `evolucionado` | Evolucionó hacia separación Memory / Knowledge / AKS |
| Seguridad IA | `evolucionado` | Evolucionó hacia foundations de seguridad actuales |
| OWASP LLM Top 10 | `preservado` | Referencia futura de seguridad |
| Prompt Injection | `preservado` | Amenaza para evidence intake y tools |
| SSRF | `preservado` | Amenaza para futuras capacidades de red |
| Auditoría documental | `evolucionado` | AKS, trazabilidad y gobernanza documental |
| Voice | `preservado` | Capacidad futura |
| Whisper | `candidato_tecnologico` | Posible tecnología de Voice |
| Piper | `candidato_tecnologico` | Posible tecnología de Voice |
| Agentes | `preservado` | Sujetos a seguridad y gobernanza |
| Module Registry | `requiere_revision` | Responsabilidad todavía no clasificada |
| Event Bus | `preservado` | Concepto arquitectónico sujeto a baseline |
| Lifecycle Manager | `requiere_revision` | Comparar con mecanismos actuales |
| Health Manager | `preservado`, `requiere_revision` | Responsabilidad exacta pendiente |
| HelloCapability | `hito_historico` | Hito mínimo superseded por capabilities reales |
| Procesamiento de Request | `materializado` | Existe flujo mediante Kernel |
| Tests del Kernel | `materializado` | Existe validación automatizada |
| Baseline Kernel v1.0 | `hito_historico` | Nomenclatura histórica |
| Memory Layer | `preservado` | Capacidad futura separada de Knowledge |
| Knowledge Layer | `preservado` | Capacidad futura relacionada con AKS y retrieval |
| RAG | `preservado` | Capacidad futura |
| Vector DB | `candidato_tecnologico` | Infraestructura futura reconstruible |
| Planning Engine | `parcialmente_materializado` | Existe Planner mínimo |
| Reasoning Engine | `preservado`, `requiere_revision` | Intención cognitiva futura |
| Capabilities reales | `parcialmente_materializado` | Futuras capabilities siguen Capability First |
| FastAPI | `candidato_tecnologico` | Sin compromiso arquitectónico |
| IoT | `preservado` | Capacidad futura |
| Vision | `preservado` | Capacidad futura |
| OSINT | `evolucionado` | Parte evolucionó hacia Evidence Acquisition |
| Workflows | `preservado` | Relacionados con automatización/orquestación |
| Malāk Platform v1.0 | `preservado` | Visión de largo plazo, no release plan aprobado |

---

# 12. Regla de promoción

La secuencia conceptual es:

```text
legacy / idea / necesidad
        ↓
evaluación contra baseline
        ↓
roadmap cuando corresponda
        ↓
specification
        ↓
ADR cuando corresponda
        ↓
unidad aprobada
        ↓
implementation
        ↓
evidence
        ↓
human governance
        ↓
baseline
```

También puede terminar explícitamente en `REJECT` o `superseded`.

---

# 13. Propuestas pendientes de revisión

| Propuesta | Estado | Observación |
|---|---|---|
| Preparación del AKS para GraphRAG | No aprobada | No implica implementar GraphRAG |
| Unidad posterior a Sprint 7.11 | No autorizada | Debe surgir de necesidad demostrada del baseline `3413e8c…` |
| RDD Stage 2 | No autorizada | Requiere utilidad demostrada y aprobación separada |
| Module Registry legacy | Requiere revisión | Determinar si la responsabilidad sigue siendo necesaria |
| Lifecycle Manager legacy | Requiere revisión | Comparar intención con lifecycle actual |
| Health Manager legacy | Requiere revisión | Definir responsabilidad mínima antes de proponer |

La tabla no establece secuencia obligatoria.

La existencia de IDEA-012 — Constitutional Assurance Foundation y otras ideas
`aprobada_para_planificacion_futura` no equivale a selección del siguiente
sprint ni a promoción automática a esta tabla.

---

# 14. Restricciones estructurales

Antes de introducir agentes, herramientas externas, navegación, automatización
del sistema operativo, memoria sensible o capabilities de alto riesgo deben
existir las foundations requeridas y autorización independiente.

Ninguna propuesta puede:

- ampliar el Kernel con lógica de negocio;
- acoplar el Kernel a runtime, provider o modelo concreto;
- introducir dependencias no aprobadas;
- modificar contratos centrales sin revisión;
- reinterpretar evidencia como autoridad;
- asumir que el hardware actual define la arquitectura permanente.

## 14.1 Regla de admisión de Capabilities

Una Capability solo podrá incorporarse cuando añada una funcionalidad:

```text
real
necesaria
permanente
```

para Malāk.

No deben crearse Capabilities exclusivamente para:

- validar routing;
- demostrar múltiples entradas;
- probar Registry;
- aumentar cobertura artificialmente;
- completar una secuencia histórica;
- incorporar ejemplos sin utilidad funcional.

La infraestructura interna debe validarse mediante:

- tests;
- doubles;
- fixtures;
- contratos;
- integración controlada.

---

# 15. Relación con ideas y concepts

Registro de ideas:

```text
documents/projects/jarvis/ideas.md
```

Referencias conceptuales:

```text
docs/project/concepts/**
```

Reglas:

```text
idea puede informar evaluación
concept puede informar diseño
ninguno autoriza implementación
ninguno modifica baseline
```

Antes de diseñar una capacidad futura desde cero se debe verificar si su
intención ya está preservada allí.

---

# 16. Reconciliación downstream

Después de integrar un cambio material en `Aranwill/jarvis/main` debe evaluarse
la reconciliación del Project Vault mediante el Vault Sync Agent.

```text
Malāk main
   ↓
source of truth

Sync Agent
   ↓
observa / propone

Project Vault
   ↓
proyección derivada
```

La reconciliación:

- no reabre un sprint cerrado;
- no modifica autoridad;
- no convierte el Vault en source of truth;
- no autoriza una nueva unidad.

El merge de Sprint 7.11 expuso un `STATE_DRIFT` porque la evidencia final estaba
solo bajo `sprints/proposals/`, mientras el extractor downstream resolvía fichas
canónicas `docs/project/sprints/SPRINT-*.md`.

La creación de `docs/project/sprints/SPRINT-7.11.md` corrige esa fuente
estructural. La proyección del Vault debe verificarse nuevamente después de
integrar este corrective packet.

---

# 17. Regla de no duplicación

```text
project_context.md
→ snapshot operativo compacto

implementation_roadmap.md
→ planificación derivada

SPRINT-*.md
→ evidencia detallada de ejecución

ideas.md
→ ideas y visión

concepts/**
→ referencias no normativas
```

Un concepto debe tener una ubicación responsable y referencias explícitas, no
copias divergentes.

---

# 18. Regla de actualización

Este documento debe revalidarse cuando ocurra cualquiera de estos eventos:

- cambio material del baseline o `HEAD` que afecte planificación;
- cierre de un sprint;
- apertura formal de una nueva unidad;
- modificación material de contratos públicos;
- decisión arquitectónica que afecte planificación;
- promoción de una idea al roadmap;
- rechazo o supersedencia de una iniciativa;
- cambio material de gobernanza;
- drift downstream relevante.

Los registros históricos no deben reescribirse silenciosamente para coincidir
con el presente.

---

# 19. Estado actual de planificación

```text
MATERIAL BASELINE REFERENCE
3413e8ccb348440aea757d1feccde25c65be011f

PERMANENT BRANCH
main

ACTIVE SPRINT BRANCH
NONE

NOMINAL VERSION
v0.6.0-alpha

LAST INTEGRATED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST PRODUCT/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

ACTIVE SPRINT
NONE

SUBSEQUENT UNIT
NONE AUTHORIZED

RDD STAGE 2
NOT AUTHORIZED

LAW DOCUMENTS
OUT OF SCOPE

AUTHORITY EXPANSION
NONE
```

---

# 20. Principio de cierre

La planificación de Malāk debe permanecer:

```text
trazable
→ gobernada
→ incremental
→ reversible
→ subordinada a autoridad superior
```

El roadmap organiza intención.

No crea autoridad.

La evidencia puede producir una propuesta.

Solo una decisión humana autorizada puede convertir una propuesta en trabajo
admitido y, posteriormente, en baseline.
