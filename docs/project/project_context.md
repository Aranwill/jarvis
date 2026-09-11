---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-09-11
as_of_commit: e45a3e3c0ebf657a513596aa74452413479c05d1
branch: main
certification_branch: null
candidate_commit: null
certification_status: current_main_validated
baseline: v0.6.0-alpha
language: es
---

# Contexto del proyecto Malāk

## Propósito

Este documento proporciona una visión consolidada del estado operativo observado
del repositorio de Malāk.

Es derivado, informativo y no normativo. Está destinado a ayudar a desarrolladores
y asistentes automatizados a recuperar contexto actual sin convertir este resumen
en una fuente de autoridad.

No reemplaza ni modifica:

- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Kernel Specification;
- ADR aceptados;
- contratos centrales;
- SECURITY.md;
- fichas de sprint y proposal records;
- historial Git.

Ante conflicto prevalece la fuente de mayor autoridad y la evidencia Git más
reciente aplicable.

---

## Regla persistente de idioma

- La comunicación y documentación nueva de Malāk debe redactarse en español.
- Identificadores técnicos, clases, funciones, APIs, comandos y rutas existentes
  permanecen en su forma original cuando traducirlos afectaría consistencia.
- Fuentes externas en otro idioma deben explicarse en español.

---

## Fuentes de evidencia de este snapshot

Estado observado:

```text
Malāk
repository: Aranwill/jarvis
branch: main
HEAD: e45a3e3c0ebf657a513596aa74452413479c05d1
latest integrated unit: PR #111 — Assurance Signal Authority G0/G1
Validation on current HEAD: success

Malāk Project Vault
repository: Aranwill/malak-project-vault
branch: main
HEAD: 34f0416a8d312f4f27b9b36c3733cc2703772364
last reconciled Malāk source HEAD: 5865da6a5e502fe71e35e2e38bc4cceaab9b3600
current disposition: drift esperado; nueva reconciliación pendiente

Vault Sync Agent
repository: Aranwill/malak-vault-sync-agent
branch: main
HEAD: f6eb42715dd7771f3bcf7909a99f7e4e7db465c1
operating mode: manual-on-demand
```

El Vault es una proyección derivada. Su drift actual no altera la autoridad de
`Aranwill/jarvis/main`, pero debe reconciliarse antes de un gate que exija drift
cero.

El documento `docs/project/status/MALAK-POST-AUDIT-REBASELINE-20260911.md`
queda preservado como snapshot histórico del punto `main@5865da6a`; ya no debe
interpretarse como current state.

---

## Clasificación documental

### Fuentes normativas principales

1. `docs/governance/cognitive_constitution.md`
2. `docs/governance/governance_constitution.md`
3. `docs/architecture/blueprint.md`
4. `docs/architecture/kernel.md`
5. `docs/architecture/architecture_quality_gates.md`
6. ADR aceptados y contratos públicos aprobados
7. `SECURITY.md`
8. estándares de desarrollo y repositorio aplicables

### Fuentes históricas

Incluyen snapshots de release, changelogs, registros de migración, proposal
records cerrados, fichas de sprint e historial Git. Describen su propio punto
temporal y no deben reescribirse para simular estado actual.

### Fuentes derivadas

Incluyen este documento, `docs/project/implementation_roadmap.md`, resúmenes de
estado no normativos y el Malāk Project Vault.

```text
derived state != authority
planning != authorization
evidence != authority
```

---

## Snapshot operativo actual

```text
Repositorio oficial:              Aranwill/jarvis
Rama permanente:                  main
HEAD integrado actual:            e45a3e3c0ebf657a513596aa74452413479c05d1
Baseline nominal:                 v0.6.0-alpha
Último sprint numerado:           Sprint 7.11 — Reproducible Validation Pipeline Foundation
Última ruta conversacional:       Sprint 7.10 — Conversation Session Isolation Foundation
Última unidad episódica:          Governed Projection Consumption Boundary
Última unidad de código cognitivo: G2A — Protected Finalization Foundation
Último diseño cognitivo:          Assurance Signal Authority Boundary — G0/G1
Sprint activo autorizado:         ninguno
Rama de implementación activa:    ninguna
Sprint 7.12:                      no autorizado
Signal Boundary G2:               no autorizado
Conversation Finalization G2B:    no autorizado / bloqueado por signal-producer gap
Candidate Content Identity G2:    no autorizado
Persistence Authorization:        no autorizado
RDD Stage 2:                      no autorizado
```

---

## Evolución integrada después de Sprint 7.11

Las unidades siguientes fueron autorizadas e integradas de forma independiente;
no constituyen Sprint 7.12:

```text
Episodic Memory Admission Boundary        PR #76
        ↓
Assessment Provenance Boundary            PR #82
        ↓
Assessment Producer Authorization         PR #85
        ↓
Governed Input Projection Boundary        PR #88
        ↓
Governed Projection Consumption Boundary  PR #92
```

La cadena episódica continúa aislada de Conversation/runtime y no persiste
Memory.

PR #93 integró únicamente G0/G1 de `Episodic Candidate Content Identity`.
Candidate Content Identity G2, propagación de identidad y cualquier uso como
precondición de persistencia continúan sin autorización.

PR #97–#99 preservaron y diseñaron la dirección Evidence-Bound / Progressive
Cognitive Assurance. La promoción normativa posterior quedó reflejada mediante
ADR-005, Blueprint v0.6.2-alpha y Cognitive Constitution v1.1.0, incluyendo la
separación entre generación y finalización y finalización vinculada a evidencia.

---

## G2A — Protected Finalization Foundation

PR #110 fue integrada mediante:

```text
ecb1315946f47534135bbdc73d94ccf88df0d8d6
```

Materializó una foundation aislada bajo:

```text
src/malak/core/protected_finalization.py
```

con tests candidate-bound en:

```text
tests/test_protected_finalization.py
```

La foundation representa de forma ejecutable:

```text
Generated Candidate
        !=
Final Response

ProtectedResponseCandidate
        +
explicit assurance input
        ↓
deterministic evaluation
        ↓
ACCEPT | ABSTAIN | BLOCK
```

Propiedades preservadas:

- evaluator puro y determinista;
- policy versionada;
- `BLOCK` ante violación explícita de policy;
- `ABSTAIN` ante applicability no resuelta, contradicción no resuelta o soporte
  insuficiente cuando aplica;
- `ACCEPT` únicamente para estados explícitamente permitidos;
- sin side effects;
- sin acceso a provider/runtime;
- sin Kernel wiring;
- sin Conversation wiring;
- sin Memory/Knowledge/retrieval;
- sin `QUALIFY` inventado;
- sin ampliación de autoridad.

G2A no convierte todavía la conversación real de Malāk en una ruta protegida.

---

## Assurance Signal Authority Boundary — G0/G1

PR #111 fue integrada en el HEAD actual:

```text
e45a3e3c0ebf657a513596aa74452413479c05d1
```

El diseño G0/G1 confirmó que G2A no debe alimentarse desde metadata implícita ni
desde decisiones de dominios ajenos.

Separación requerida:

```text
observation
!= producer authorization
!= projected signal
!= finalization decision
!= authority
```

Los signals de G2A requieren ownership explícito y proyección determinista.

En particular:

- `applicability` y `evidence_required` pertenecen a policy cognitiva versionada;
- `support_sufficient` exige evaluación de evidencia real;
- `contradiction_unresolved` exige evaluación explícita;
- `policy_violation` no debe derivarse automáticamente de cualquier `DENY` del
  Security PDP.

El Security PDP continúa gobernando autorización de operaciones, no verdad ni
suficiencia cognitiva.

### Estado de autorización

```text
Signal Authority G0/G1: integrated
Signal Boundary G2: NOT AUTHORIZED
Conversation Finalization G2B: NOT AUTHORIZED
```

G2B permanece bloqueado hasta que exista un productor explícito y autorizado de
applicability/evidence signals.

---

## Ruta conversacional implementada

La ruta runtime vigente continúa siendo:

```text
CLI
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

Sprint 7.9 añadió continuidad conversacional efímera y Sprint 7.10 aislamiento
por `session_id`.

La conversación continúa siendo efímera. No existe persistencia conversacional
ni Memory persistente.

La inspección G0 de Progressive Cognitive Assurance confirmó que actualmente el
provider output puede llegar a `Response` sin pasar por G2A. Además, el historial
conversacional existente se construye antes de una futura finalización protegida.
Ese gap es conocido y **no está autorizado corregirlo mediante G2B todavía**.

---

## Memory — estado actual

La cadena aislada materializada es:

```text
EpisodicMemoryCandidate
        ↓
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
Governed Projection Consumption
BLOCKED | EVALUATED
        ↓
Episodic Admission
REJECT | HOLD | ELIGIBLE
        ↓
STOP
```

Se preserva:

```text
Candidate != Decision
payload != control metadata
structural provenance != authenticated identity
AUTHORIZED != trusted truth
Projection READY != Admission ELIGIBLE
Consumption EVALUATED != persistence authorization
ELIGIBLE != Stored
```

Continúan fuera de alcance:

- Conversation/runtime wiring de la cadena episódica;
- Candidate Content Identity G2;
- Persistence Authorization;
- Memory persistente;
- retrieval;
- Knowledge operativo.

---

## Seguridad — foundations preservadas

El Security Control Plane mantiene separación entre:

```text
solicitar
→ decidir
→ aplicar
→ auditar
→ ejecutar operación protegida
```

El PDP permanece determinista, sin LLM, con denegación por defecto y
comportamiento fail-closed.

El PEP no acepta decisiones aportadas por el llamador y permanece separado del
Kernel y Planner.

El Secure Context Lifecycle conserva `Clock`, validación temporal, emisión,
renovación y propagación inmutable en memoria.

Permanece registrado como riesgo residual histórico:

```text
7.7-D-001 — Strong SecurityContext Provenance
classification: ACCEPTED_RESIDUAL_RISK
severity: MEDIUM
blocking_release: NO
```

No habilita por sí mismo trabajo de seguridad adicional.

---

## Malāk Project Vault

El Vault:

- es derivado;
- no posee autoridad operativa;
- no modifica automáticamente el repositorio oficial;
- requiere revisión humana para propuestas gobernadas;
- conserva snapshots históricos;
- puede proyectar cambios observados desde Malāk.

Última reconciliación aceptada:

```text
Vault main@34f0416a8d312f4f27b9b36c3733cc2703772364
represents Malāk main@5865da6a5e502fe71e35e2e38bc4cceaab9b3600
```

Estado actual:

```text
Malāk main@e45a3e3c0ebf657a513596aa74452413479c05d1
Vault reconciliation: pending
known drift: expected after PR #110 + PR #111
```

La reconciliación del Vault es un paso operativo derivado y no constituye nuevo
sprint ni autorización cognitiva.

---

## Planificación vigente

La fuente derivada canónica para planificación es:

```text
docs/project/implementation_roadmap.md
```

El estado actual es:

```text
LAST COMPLETED NUMBERED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST CONVERSATIONAL/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

LATEST EPISODIC MEMORY UNIT
Governed Projection Consumption Boundary

LATEST COGNITIVE CODE UNIT
G2A — Protected Finalization Foundation

LATEST COGNITIVE DESIGN UNIT
Assurance Signal Authority Boundary — G0/G1

ACTIVE AUTHORIZED SPRINT
NONE

SIGNAL BOUNDARY G2
NOT AUTHORIZED

CONVERSATION FINALIZATION G2B
NOT AUTHORIZED

CANDIDATE CONTENT IDENTITY G2
NOT AUTHORIZED

PERSISTENCE AUTHORIZATION
NOT AUTHORIZED

RDD STAGE 2
NOT AUTHORIZED
```

La siguiente decisión funcional debe tomarse solo después de reconciliar el
Vault o aceptar explícitamente el drift como riesgo para un gate concreto.

---

## Capacidades explícitamente postergadas

Sin una unidad aprobada de manera independiente no se deben introducir:

- agentes autónomos;
- ejecución libre de herramientas externas;
- navegación externa;
- comunicaciones externas automáticas;
- control autónomo del sistema operativo;
- Memory persistente sensible;
- retrieval/Knowledge operativo;
- Candidate Content Identity G2;
- Persistence Authorization;
- Signal Boundary G2;
- Conversation Finalization G2B;
- RDD Stage 2;
- modificación automática de políticas, Kernel, Blueprint o Constituciones;
- elevación automática de privilegios;
- autoaprobación de decisiones.

---

## Disciplina de trabajo

La evolución de Malāk mantiene:

```text
idea o necesidad
→ evaluación
→ specification / design
→ ADR cuando corresponda
→ alcance aprobado
→ rama temporal
→ TDD / implementación
→ 4R
→ Bounded Correction cuando aplique
→ Independent Validation
→ evidencia
→ Pull Request
→ revisión humana
→ merge humano
→ baseline
```

Principios persistentes:

- Kernel First;
- Capability First;
- Runtime Independence;
- Vendor Independence;
- Human in Control;
- Zero Trust;
- Defense in Depth;
- mínimo privilegio;
- autorización explícita;
- contratos estables;
- cambios pequeños, trazables y reversibles;
- separación entre autoridad cognitiva y autoridad de seguridad;
- evidencia no equivalente a autoridad.

Antes de cambios importantes deben responderse las cuatro preguntas:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Cognitive Constitution?
3. ¿Respeta Governance?
4. ¿Preserva o reduce la complejidad del Kernel?

---

## Artefactos protegidos

No modificar sin autorización explícita y proceso aplicable:

- Kernel;
- contratos centrales;
- Blueprint;
- Cognitive Constitution;
- Governance Constitution;
- políticas de seguridad;
- ADR aceptados;
- snapshots históricos;
- metadatos de release.

---

## Referencias de evidencia detallada

Para historia y validación detallada consultar:

```text
docs/project/sprints/SPRINT-7.0.md ... SPRINT-7.11.md
docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G0-INSPECTION.md
docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G2A-IMPLEMENTATION-CANDIDATE-SPEC.md
docs/project/sprints/proposals/MALAK-ASSURANCE-SIGNAL-AUTHORITY-G0-G1-DESIGN.md
docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
```

Este contexto no replica toda esa evidencia para evitar drift y duplicación.

---

## Política de actualización

Este documento queda reconciliado contra:

```text
main@e45a3e3c0ebf657a513596aa74452413479c05d1
active_work_branch@NONE
```

Debe revalidarse cuando:

- `HEAD` cambie materialmente el contexto descrito;
- se integre una unidad funcional relevante;
- se active o cierre un sprint;
- cambie arquitectura o gobernanza;
- cambie materialmente el estado del Vault;
- se certifique una release;
- se incorpore una nueva frontera de seguridad o cognición.

Los registros históricos no deben reescribirse para aparentar presente.

---

## Declaración de ausencia de autoridad normativa

Este documento no puede:

- aprobar un sprint;
- autorizar implementación;
- modificar arquitectura o gobernanza;
- redefinir Kernel o contratos;
- certificar una release;
- anular un ADR;
- conceder permisos;
- ampliar autoridad operativa.

Su propósito es proporcionar un snapshot de contexto actual, trazable y
conveniente.
