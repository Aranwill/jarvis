---
title: Malāk Governed Self-Review Bootstrap Task
status: concept
authority: non_normative
document_role: governed_self_review_bootstrap_reference
language: es
created: 2026-09-20
baseline_commit: 419d71f05233f98eecd849e986ae5af9a5d8a068
planning_disposition: owner_requested_first_task_candidate
critical_contract: true
implementation_authorized: false
execution_authorized: false
runtime_delta: 0
authority_effect: none
rdd_stage_2_authorized: false
related:
  - docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md
  - documents/projects/jarvis/ideas.md
  - docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
  - SECURITY.md
  - docs/development/malak_construction_protocol.md
---

# Malāk Governed Self-Review Bootstrap Task

## 1. Propósito

Preservar como una de las primeras tareas candidatas de Malāk, cuando exista una
ruta gobernada capaz de inspeccionar, analizar y proponer mejoras sobre su propio
baseline.

La tarea no consiste en que Malāk se modifique. Consiste en comprobar si puede:

    leer su baseline real
      -> entender contratos y límites
      -> contrastar evidencia actual
      -> detectar gaps materiales reales
      -> distinguir gap actual de deuda histórica
      -> investigar sólo cuando exista necesidad
      -> proponer hardening acotado
      -> entregar evidencia y propuesta al Owner
      -> STOP

Principio rector:

La autoinspección puede producir findings y propuestas. No produce autoridad
para modificar el baseline.

## 2. Decisión de planificación preservada

El Owner indicó que la revisión de hardening posterior a
MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 debe quedar reservada como una de
las primeras tareas reales de Malāk.

Esta decisión significa únicamente:

    FIRST-TASK CANDIDATE
    != automatic next execution
    != sprint authorization
    != implementation authorization
    != self-modification authority

La ejecución futura requiere nuevamente baseline vigente, admission review
aplicable, Construction Protocol vigente y autorización explícita del Owner.

## 3. Origen de la tarea

La auditoría V1 quedó integrada mediante PR #173 en:

    main@419d71f05233f98eecd849e986ae5af9a5d8a068

Resultado material:

    units reviewed: 13 / 13
    current blocking findings: 0
    runtime remediation required: 0
    authority expansion required: 0

También preservó:

    U01 Core Kernel
    -> CURRENT_STATE_REVALIDATED
    -> historical evidence limitation only

    U04 Observability
    -> CURRENT_STATE_REVALIDATED
    -> historical evidence limitation only

    RR-03
    -> strong SecurityContext provenance
    -> accepted residual risk
    -> non-blocking in current baseline

Por lo tanto, esta tarea futura no nace de un defecto conocido que deba
corregirse ahora. Nace como ejercicio gobernado para comprobar que Malāk pueda
revisarse a sí misma sin inventar trabajo ni ampliar autoridad.

## 4. Resultado esperado

La tarea debe producir uno de estos resultados:

    NO_CHANGE_RECOMMENDED
    HARDENING_PROPOSAL
    RESEARCH_REQUIRED
    DEFER
    INCONCLUSIVE

No existe obligación de encontrar una mejora.

    no material gap found
    -> valid result
    -> NO_CHANGE_RECOMMENDED

La ausencia de una propuesta es preferible a fabricar necesidad.

## 5. Inputs obligatorios

En el momento de ejecución, Malāk debe utilizar como mínimo:

- current exact main baseline;
- AGENTS.md;
- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- Architecture Quality Gates;
- SECURITY.md;
- ADR aceptados;
- Malāk Construction Protocol;
- Development Checklist;
- implementation roadmap;
- ideas.md;
- MALAK_RESEARCH_HORIZON_MAP.md;
- concepts relevantes;
- código y tests actuales;
- CI/evidencia actual;
- última auditoría o reconciliación aplicable.

La auditoría V1 es baseline comparativo, no source of law.

## 6. Primer foco de revisión

### 6.1 U01 — Core Kernel

La limitación histórica D-U01-001 no es deuda de implementación.

Malāk deberá preguntar:

- ¿existe hoy un gap material del Kernel?
- ¿algún cambio posterior erosionó Kernel First o Capability First?
- ¿apareció lógica de dominio, autoridad, Memory, Security o Engineering dentro
  del Kernel sin justificación?
- ¿existe complejidad nueva que pueda eliminarse sin perder una capacidad real?

Regla:

    historical evidence gap != hardening requirement

### 6.2 U04 — Observability

La limitación histórica D-U04-001 tampoco es deuda de implementación.

Malāk deberá comprobar que el baseline actual preserve:

    metrics != audit
    telemetry != authority
    observation != evaluation
    evaluation != authorization

y deberá buscar evidencia real de drift, ruido, acoplamiento o complejidad
innecesaria.

### 6.3 RR-03 — Strong SecurityContext Provenance

Este es el principal watch item técnico heredado de la auditoría.

Estado actual:

    ACCEPTED_RESIDUAL_RISK
    non-blocking
    no immediate remediation authorization

Debe reabrirse materialmente cuando una futura superficie dependa de:

- agentes operativos;
- tools con side effects;
- delegación;
- ejecución externa;
- persistencia;
- Protected Durable Write;
- autoridad cross-process;
- identidad fuerte;
- secretos;
- IPC o message bus;
- trust revocation;
- provenance verificable para decisiones sensibles.

Pregunta obligatoria:

¿La autoridad que esta superficie pretende consumir puede demostrarse con la
fuerza necesaria para el riesgo que introduce?

Resultados posibles:

    ALREADY_COVERED
    REQUIRES_REINFORCEMENT
    BLOCKING_GAP
    DEFERRED
    NOT_APPLICABLE

## 7. Flujo permitido de la tarea

    G0 / exact baseline
      -> scope freeze
      -> evidence collection
      -> current-state inspection
      -> cross-unit invariant check
      -> gap classification
      -> research only if a real uncertainty/gap requires it
      -> analysis
      -> proposal candidate
      -> validation plan
      -> Owner
      -> STOP

No está permitido:

    inspect
    -> decide own authority
    -> edit production
    -> approve
    -> merge

## 8. Contrato de findings

Todo finding futuro debe distinguir:

- finding_id;
- source_of_truth;
- baseline_evidence;
- current_behavior;
- historical_context;
- impact;
- severity;
- confidence;
- unresolved_evidence;
- recommended_disposition;
- authority_effect: none.

Estados permitidos del análisis:

    ALIGNED
    GAP
    UNCONFIRMED
    CONTRADICTION
    NOT_APPLICABLE

Reglas:

    UNCONFIRMED != GAP
    GAP != authorization
    finding != fix
    finding != sprint
    finding != merge

## 9. Contrato de propuesta

Una propuesta de hardening debe contener como mínimo:

- necesidad demostrada;
- evidencia exacta;
- componente afectado;
- riesgo actual;
- alternativa de no cambio;
- cambio mínimo suficiente;
- impacto esperado;
- archivos/componentes previstos;
- fuera de alcance;
- tests/validaciones requeridas;
- rollback;
- riesgos residuales;
- complejidad introducida o eliminada;
- relación con contratos vigentes.

Debe terminar en:

    PROPOSED_FOR_OWNER_REVIEW
    authority_effect: none

No puede terminar en estados de aprobación, autorización, Ready, merge o deploy.

## 10. Critical Contract Hardening

Esta referencia toca self-improvement y por la sección 5.2 del Construction
Protocol se trata como contrato crítico conceptual.

Interpretaciones materiales cerradas:

1. Primera tarea no significa ejecución automática.
2. Autoinspección no significa autoaprobación.
3. Hardening review no presupone que exista un defecto.
4. Audit V1 sigue siendo documento derivado, no ley.
5. U01/U04 no deben corregirse por falta de evidencia histórica.
6. RR-03 no autoriza criptografía, PKI ni nuevas capas por anticipación.
7. Un LLM no puede convertir retórica de mejora en necesidad.
8. El resultado no cambiar nada es válido.

Resultado:

    known material ambiguity unresolved: 0
    authority expansion: 0
    runtime delta: 0
    implementation authorization: 0

## 11. Malāk Alignment Matrix

| Fuente | Clase | Invariante/intención | Disposición | Efecto |
|---|---|---|---|---|
| Cognitive Constitution | normativa | cognición gobernada y evidencia | ADOPT | revisión grounded, no autoautoridad |
| Governance Constitution | normativa | Human in Control | ADOPT | Owner conserva aprobación y merge |
| Blueprint | normativa | Kernel First / Capability First | ADOPT | Kernel delta 0 |
| Architecture Quality Gates | arquitectura | limitar drift y complejidad | ADOPT | toda propuesta justifica delta |
| SECURITY.md | política protegida | Zero Trust; Intelligence != Authority; RR de SecurityContext | ADOPT | RR-03 es watch item |
| ADR-003 | ADR aceptada | evidence/result no transfiere autoridad | ADOPT | findings/propuestas informativos |
| ADR-004 | ADR aceptada | Specification & Verification First | ADOPT | remediation futura requiere diseño propio |
| Audit V1 | derived audit | baseline comparativo; 0 blocking gaps | ADOPT | punto de partida, no ley |
| IDEA-002 | no normativa | mejora gobernada por observación y propuesta | ADOPT | bootstrap real |
| Research Horizon | no normativa | Governed Self-Improvement ALIGNED | ADOPT | reutiliza intención existente |
| E0-E4 Engineering | baseline | read -> inspect -> analyze -> propose | REUSE | preferir capacidades existentes |
| D-U01-001 / D-U04-001 | evidencia histórica | límites epistemológicos | OBSERVE | nunca auto-remediation |
| RR-03 | riesgo residual | provenance fuerte pendiente | OBSERVE / REASSESS | escala sólo con necesidad real |
| RDD Stage 2 | no autorizado | fuera de alcance | REJECT | permanece no autorizado |

Separaciones:

    alignment evidence != authority
    ADOPT != implementation authorization
    REUSE != execution authorization
    OBSERVE != remediation

## 12. Cuatro preguntas de ley

1. Blueprint: PASS.
   No cambia Kernel ni arquitectura; reutiliza capacidades y fuentes existentes.

2. Cognitive Constitution: PASS.
   Prioriza evidencia, contradicción visible y no cambio cuando no hay necesidad.

3. Governance Constitution: PASS.
   Findings y propuestas terminan en Owner; no existe self-approval.

4. Kernel complexity: PASS.
   Kernel delta 0; runtime delta 0.

## 13. Design 4R

### Risk — PASS

Riesgos revisados:

- self-authorization por reinterpretación;
- improvement bias;
- fabricación de deuda desde gaps históricos;
- authority laundering desde Audit V1;
- scope creep desde RR-03;
- infraestructura preventiva sin necesidad.

Controles: estados cerrados, evidencia actual obligatoria, Owner boundary,
NO_CHANGE_RECOMMENDED válido y prohibición de auto-remediation.

### Readability — PASS

La tarea distingue observar, analizar, proponer, autorizar, implementar y mergear.

### Reliability — PASS

Baseline exacto, inputs definidos, findings estructurados y trazabilidad requerida.

### Resilience — PASS

Evidencia insuficiente produce UNCONFIRMED o INCONCLUSIVE, nunca una mejora
inventada ni permiso de ejecución.

## 14. RDD Stage 1 Design Check

    baseline identity strategy                PASS
    future candidate identity strategy        PASS
    evidence provenance                       PASS
    Writer/Reviewer/Validator/Authority split PASS
    PASS|FAIL|INCONCLUSIVE discipline         PASS
    candidate change invalidates evidence     PASS
    bounded correction semantics              PASS
    authority_effect                          none
    RDD Stage 2                               NOT AUTHORIZED

La ejecución futura sólo podrá producir Candidate Conformance cuando exista un
candidate material y después de las validaciones requeridas.

## 15. Disposición RED / GREEN

Para esta referencia conceptual:

    RED:   N/A_WITH_REASON
    GREEN: N/A_WITH_REASON

Razón:

- no se implementa comportamiento ejecutable;
- no se crea capability;
- no se modifica runtime;
- no se crea agente;
- no se crea scheduler;
- no se habilita self-improvement operacional.

Cualquier implementación futura deberá abrir un candidate separado y recorrer
la secuencia crítica aplicable desde G0/G1.

## 16. Readiness para ejecutar esta tarea en el futuro

Podrá proponerse su ejecución cuando exista una ruta gobernada suficiente para:

1. capturar un baseline exacto;
2. leer repositorio y conocimiento gobernado;
3. inspeccionar evidencia;
4. analizar findings;
5. producir propuestas estructuradas;
6. preservar authority_effect = none;
7. detenerse antes de modificar el baseline;
8. entregar el resultado al Owner.

No se exige un agente autónomo para cumplir estos criterios.

Si las capacidades existentes son suficientes, deben reutilizarse antes de crear
orquestación adicional.

## 17. Criterio de éxito del bootstrap

La primera ejecución será útil si demuestra que Malāk puede:

    conocerse sin inventarse
    detectar sin autoautorizarse
    proponer sin automodificarse
    aceptar que no existe mejora cuando la evidencia no la justifica
    escalar incertidumbre en lugar de ocultarla

La tarea también puede servir como benchmark temprano de Engineering
Intelligence y Governed Self-Improvement.

La calidad se evaluará por groundedness, trazabilidad, disciplina de autoridad y
capacidad de concluir NO_CHANGE_RECOMMENDED, no por cantidad de cambios
propuestos.

## 18. Estado

    conceptual capture: COMPLETE
    G0/G1 design: COMPLETE
    critical contract hardening: PASS
    four law questions: PASS
    Design 4R: PASS
    RDD Stage 1 Design Check: PASS

    runtime delta: 0
    implementation authorization: 0
    execution authorization: 0
    authority_effect: none

    future task priority:
    one of the first governed self-review tasks
    subject to exact-baseline admission + explicit Owner authorization
