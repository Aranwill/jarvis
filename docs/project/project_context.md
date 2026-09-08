---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-09-08
as_of_commit: 3413e8ccb348440aea757d1feccde25c65be011f
branch: main
certification_branch: null
candidate_commit: 59f592e2e36d11bbd14f7d9d93b1dac4f442c108
certification_status: sprint_7_11_completed
baseline: v0.6.0-alpha
---

# Contexto del proyecto Malāk

## Propósito

Este documento ofrece una vista compacta del estado operativo observado de
Malāk para recuperación de contexto.

Es derivado, informativo y no normativo.

No reemplaza ni modifica:

- Constitución Cognitiva;
- Constitución de Gobernanza;
- Blueprint;
- Kernel;
- Architecture Quality Gates;
- ADR aceptados;
- contratos públicos;
- `SECURITY.md`;
- fichas de sprint;
- historial Git;
- `docs/project/implementation_roadmap.md`.

Ante conflicto, prevalece la fuente oficial de mayor autoridad o la evidencia
más reciente del repositorio `Aranwill/jarvis/main`.

---

## Regla de no duplicación

Este documento no mantiene una segunda copia extensa del roadmap ni de la
historia de ejecución de cada sprint.

```text
estado operativo compacto
        → project_context.md

planificación derivada vigente
        → implementation_roadmap.md

alcance + ejecución + evidencia + cierre
        → docs/project/sprints/SPRINT-*.md

ideas y visión futura
        → documents/projects/jarvis/ideas.md

referencias conceptuales
        → docs/project/concepts/**
```

Los snapshots históricos se preservan en sus fuentes originales y no deben
reescribirse para aparentar que describen el presente.

---

## Baseline observado

```text
Repositorio oficial:             Aranwill/jarvis
Rama permanente:                 main
HEAD oficial observado:          3413e8ccb348440aea757d1feccde25c65be011f
Baseline nominal:                v0.6.0-alpha
Último sprint integrado:         Sprint 7.11 — Reproducible Validation Pipeline Foundation
Último sprint funcional runtime: Sprint 7.10 — Conversation Session Isolation Foundation
Sprint activo autorizado:        ninguno
Rama de implementación activa:   ninguna
RDD Stage 1:                     adopted
RDD Stage 2:                     not authorized
```

Sprint 7.11 fue integrado mediante PR #65.

```text
baseline inicial:
deb759ee9855737a24b169e03bde2028c7db7f33

candidate final:
59f592e2e36d11bbd14f7d9d93b1dac4f442c108

merge commit:
3413e8ccb348440aea757d1feccde25c65be011f
```

Evidencia del candidato final registrada durante el cierre:

```text
pytest:                 388 passed
compileall:             PASS
diff-check:             PASS
FULL 4R:                PASS
independent validation: PASS
G0–G6:                  PASS
```

Después del merge, el workflow `Validation` se ejecutó nuevamente sobre el HEAD
integrado de `main` y concluyó con `success`.

Ningún PASS técnico autoriza automáticamente una unidad posterior.

---

## Estado de sprints 7.x

| Sprint | Estado | Resultado principal |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición con `OllamaRuntime` mediante configuración externa |
| 7.2 | Cerrado | `RuntimeMetricSink` de solo escritura |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Observabilidad y sincronización gobernada del Vault |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Validación integral y certificación interna del baseline |
| 7.8 | Completado | Cognitive Conversation Execution Path Foundation |
| 7.9 | Completado | Conversation Continuity Foundation |
| 7.10 | Completado | Conversation Session Isolation Foundation |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation |

La evidencia detallada corresponde a las fichas de sprint y no se duplica aquí.

---

## Arquitectura implementada relevante

### Pipeline cognitivo conversacional

La ruta funcional vigente permanece:

```text
CLI
  ↓
Request(content, session_id, ...)
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

Propiedades preservadas:

- Kernel pequeño y desacoplado;
- `ConversationCapability` como frontera con el subsistema conversacional;
- providers y runtimes construidos fuera del Kernel;
- `Request.session_id` preservado a través de la Capability;
- historial efímero aislado por sesión;
- conversación sin persistencia;
- Runtime Independence;
- Model Agnostic;
- Capability First.

Separación vigente:

```text
Conversation History != Memory != Knowledge
```

No existe Memory persistente, RAG, GraphRAG, agentes ni Sandbox en el baseline
actual.

---

## Security Control Plane

La foundation vigente incluye:

```text
AuthorizationRequest
AuthorizationDecision
Policy Decision Point
Policy Enforcement Point
Authorization Audit
SecurityContext lifecycle
```

Propiedades centrales:

- PDP determinista;
- sin LLM en autorización;
- default-deny;
- fail-closed;
- PEP separado del Kernel y del Planner;
- confirmación humana explícita cuando corresponde;
- auditoría separada de métricas y eventos operativos;
- lifecycle temporal explícito de `SecurityContext`;
- emisión, validación y renovación con lineage;
- propagación inmutable mediante `SecurityContextEnvelope`.

Riesgo residual preservado:

```text
7.7-D-001 — Strong SecurityContext Provenance
classification: ACCEPTED_RESIDUAL_RISK
severity: MEDIUM
blocking_release: NO
```

Todavía no se implementan de forma completa:

- PKI;
- nonce;
- replay protection;
- identidad criptográfica fuerte;
- MFA;
- Secure Message Bus;
- Secure Context Manager criptográfico completo.

Ese riesgo debe revaluarse antes de habilitar rutas operativas de mayor riesgo.

---

## Observabilidad

Métricas, eventos operativos y auditoría permanecen separados.

```text
Metrics
!=
Operational Events
!=
Security Audit
```

Pueden compartir identificadores mínimos de trazabilidad, pero no contrato,
store, política de error, retención ni autoridad.

---

## Validation Foundation — Sprint 7.11

Malāk dispone ahora de una pipeline reproducible de validación:

```text
candidate / PR
    ↓
read-only GitHub Actions
    ↓
exact candidate identity
    ↓
pytest
compileall
diff-check candidate-bound
    ↓
technical evidence
```

Características:

- `pull_request` y `push` a `main`;
- permisos `contents: read`;
- sin `pull_request_target`;
- sin secrets de escritura;
- `persist-credentials: false`;
- `fetch-depth: 0`;
- Windows + Python 3.12;
- `actions/checkout@v6`;
- `actions/setup-python@v6`;
- `pytest>=9,<10` solo como dependencia opcional de desarrollo;
- cero dependencias nuevas de runtime.

Invariante:

```text
Evidence != Receipt != Validation != Decision != Authority
```

La pipeline no puede aprobar, autorizar, mergear, desplegar ni promover releases.

---

## Engineering Method

La cadena vigente de ingeniería es:

```text
Evidencia / necesidad
        ↓
Especificación
        ↓
Pruebas
        ↓
Implementación
        ↓
4R proporcional al riesgo
        ↓
Bounded Correction cuando corresponda
        ↓
Validación independiente
        ↓
E2E / métricas / evidencia
        ↓
Gobernanza humana
        ↓
Baseline estable
```

Separación obligatoria:

```text
Writer != Reviewer != Validator != Authority
```

RDD se adopta progresivamente. El baseline actual adopta Stage 1 y no autoriza
Stage 2.

---

## Dirección de autoridad

ADR-003 preserva:

```text
CONTROL / AUTHORITY
Upstream → Downstream

RESULTS / EVENTS / EVIDENCE
Downstream → Upstream
```

El retorno de resultados o evidencia no concede control ascendente.

---

## Estado de planificación

La fuente derivada canónica es:

```text
docs/project/implementation_roadmap.md
```

Estado actual:

```text
LAST COMPLETED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST PRODUCT/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

ACTIVE AUTHORIZED SPRINT
NONE

SUBSEQUENT UNIT
NONE AUTHORIZED
```

Las ideas y conceptos pueden informar futuras evaluaciones, pero:

```text
idea != roadmap
concept != baseline
roadmap != autorización
evidence != authority
```

Toda nueva unidad deberá demostrar necesidad desde el baseline vigente y volver
a atravesar admisión, especificación, revisión y autorización humana.

---

## Project Vault

El Project Vault es una proyección derivada downstream.

```text
Aranwill/jarvis/main
        ↓
source of truth

malak-vault-sync-agent
        ↓
observa / propone

malak-project-vault
        ↓
proyección derivada
```

El Vault no puede superar la autoridad del repositorio oficial.

Después del merge de Sprint 7.11 el Vault observó correctamente el HEAD
`3413e8c…`, pero resolvió inicialmente Sprint 7.10 como última ficha porque la
ficha de cierre de 7.11 todavía residía únicamente en `sprints/proposals/`.

La consolidación de `docs/project/sprints/SPRINT-7.11.md` corrige la fuente
estructural que originó ese `STATE_DRIFT`; la reconciliación downstream deberá
verificarse después de integrar este corrective packet.

---

## Capacidades explícitamente postergadas

Sin autorización independiente no se incorporan:

- Memory persistente;
- RAG / GraphRAG;
- agentes;
- composición multiagente;
- Sandbox;
- navegación;
- ejecución libre de herramientas;
- control autónomo del sistema operativo;
- comunicaciones externas automáticas;
- autoaprobación;
- auto-merge;
- auto-deploy;
- modificación autónoma de políticas, Kernel, Blueprint o Constituciones.

---

## Reglas permanentes de trabajo

Todo cambio debe preservar:

- Kernel First;
- Constitution First;
- Governance First;
- Capability First;
- Human in Control;
- Zero Trust;
- Security by Design;
- Runtime Independence;
- Model Agnostic;
- Specification & Verification First;
- trazabilidad;
- reversibilidad;
- mínimo privilegio;
- separación de autoridad.

Antes de un cambio material deben responderse las cuatro preguntas:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Preserva o reduce la complejidad del Kernel?

---

## Política de actualización

Este documento debe revalidarse cuando:

- cambie materialmente `HEAD` respecto del contexto descrito;
- se abra o cierre un sprint;
- cambie arquitectura, gobernanza o contratos relevantes;
- cambie el estado de seguridad;
- cambie la pipeline de validación de forma material;
- se certifique una nueva release;
- exista drift downstream relevante.

`as_of_commit` identifica la fuente oficial utilizada para reconstruir esta
vista. Los commits puramente derivados posteriores no deben reinterpretarse como
nueva autoridad.

---

## Declaración final

`project_context.md` informa contexto.

No puede:

- aprobar un sprint;
- autorizar implementación;
- modificar arquitectura;
- cambiar gobernanza;
- certificar release;
- ampliar permisos;
- convertir evidencia en autoridad.
