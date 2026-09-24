---
title: Malāk Governed Engineering Evidence Focus V0 — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-24
baseline_commit: 3716a7019d475bb41b8d593b8a5725cfc3fb2c8c
g0_result: pass
design_authorized_by: owner
design_authorized_at: 2026-09-24
risk_class: 3
critical_contract: true
red_authorized: true
red_authorized_by: owner
red_authorized_at: 2026-09-24
implementation_authorized: false
runtime_execution_authorized: false
runtime_delta: 0
authority_effect: none
rdd_stage_2_authorized: false
related:
  - docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TEST-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-INTERNAL-INTERACTION-TRACE-V0-G0-G1-DESIGN.md
  - docs/development/malak_construction_protocol.md
  - src/malak/capabilities/_engineering_evidence.py
  - src/malak/capabilities/engineering_inspect.py
  - src/malak/capabilities/engineering_analyze.py
  - src/malak/capabilities/engineering_propose.py
  - src/malak/app/internal_interaction.py
---

# Malāk Governed Engineering Evidence Focus V0 — G0/G1 Design

## 1. Propósito

Cerrar el gap observado durante el primer Self-Review real de Malāk sin aumentar
arbitrariamente límites de contexto ni cambiar el modelo usado para la prueba.

El objetivo es que cada foco de revisión declare de forma explícita qué evidencia
necesita, cómo se demuestra su completitud y qué conjunto exacto consumen
Inspect, Analyze y Propose.

Principio rector:

```text
evidence selection
!= first N literal matches

complete focus evidence
= declared selectors
+ exact baseline binding
+ deterministic bounded extraction
+ explicit completeness result
```

Este gate no autoriza RED, implementación ni una tercera ejecución U01.

## 2. Baseline G0

Baseline exacto de admisión:

```text
repository: Aranwill/jarvis
branch: main
baseline: 3716a7019d475bb41b8d593b8a5725cfc3fb2c8c
open PRs observed before admission: none
permanent remote branch observed: main
```

Estado integrado relevante:

```text
Engineering Inspect E2                  INTEGRATED
Engineering Analyze E3                  INTEGRATED
Engineering Propose E4                  INTEGRATED
Self-Review Evidence Packet             INTEGRATED
Internal Interaction Trace V0           INTEGRATED
Live / Replay Projection V0             INTEGRATED
Internal Interaction Test V0            INTEGRATED
Governed Self-Review Bootstrap          CONCEPT INTEGRATED
```

Este G0 es focal. No declara una nueva auditoría integral del repositorio y no
reemplaza el File Coverage Ledger de la auditoría V1.

## 3. Evidencia observada que origina el gate

El primer bootstrap real conservó dos observaciones materiales:

```text
run bootstrap-u01-20260923-001
-> Inspect COMPONENT_FAILED
-> terminal INCONCLUSIVE
-> causa exacta no preservada por trace
-> OBS-02 separado de este gate

run bootstrap-u01-20260923-002
-> Inspect GROUNDED
-> repository evidence 12
-> knowledge evidence 12
-> context_truncated=true
-> Analyze UNCONFIRMED
-> reason: analysis requires complete untruncated evidence
-> Propose NOT EXECUTED
-> terminal INCONCLUSIVE
```

La causa estructural del segundo run está en la semántica actual de Engineering:

```text
subject literal
-> scan
-> global bounded first matches
-> context_truncated when more evidence exists
```

E2 puede producir una inspección grounded con la limitación visible.
E3, correctamente fail-closed, no permite grounded analysis con evidencia
truncada.

Disposición:

```text
increase 12 -> arbitrary larger N      REJECT
weaken E3 completeness requirement     REJECT
hide context_truncated                 REJECT
change local model to mask retrieval   REJECT
focus-aware evidence selection         ADOPT
```

## 4. Gap material

El gap no es falta de capacidad cognitiva demostrada.

El gap es que el contrato actual no puede responder de forma determinista:

```text
¿qué fuentes son obligatorias para este foco?
¿qué evidencia exacta fue seleccionada?
¿esa selección está completa respecto del foco declarado?
¿Inspect, Analyze y Propose consumieron el mismo evidence set?
```

Por tanto:

```text
EVID-01
literal subject retrieval can truncate material evidence

EVID-02
E2 can continue with visible truncation while E3 requires complete evidence
```

Ambos findings se abordan como un único contrato de evidencia focal gobernada.

## 5. Decisión G1

Se introduce conceptualmente un contrato inmutable:

```text
GovernedEngineeringEvidenceFocus
├─ focus_id
├─ focus_label
├─ subject
├─ repository_required_selectors
├─ knowledge_required_selectors
├─ supplemental_terms
├─ completeness_criteria
├─ evidence_budget
└─ authority_effect = none
```

El contrato:

- describe evidencia;
- no decide findings;
- no concede autoridad;
- no selecciona modelos;
- no modifica policies;
- no ejecuta herramientas;
- no escribe el repositorio.

No se crea un Manager, Registry, Agent, Scheduler, Memory ni nueva base de datos.

## 6. Selector contract V0

V0 admite únicamente selectores deterministas de fuente:

```text
EXACT_PATH
PATH_PREFIX
```

No se admiten en V0:

```text
model-selected paths
semantic free-form retrieval
regex arbitrario desde input humano
network search
dynamic glob supplied by user
```

Cada selector requerido debe resolver contra el mismo snapshot Git capturado.

Resultado por selector:

```text
RESOLVED
MISSING
UNREADABLE
TRUNCATED
```

Cualquier selector requerido distinto de RESOLVED:

```text
focus_complete = false
-> INCONCLUSIVE
-> no Analyze grounded
-> no Propose
```

## 7. Evidence extraction V0

Dentro de las fuentes resueltas se permiten términos internos fijados por el
focus contract para extraer evidencia bounded.

La limitación deja de ser global por tipo y pasa a ser demostrable por selector.

Regla:

```text
required selector
-> all required matches within its declared budget
-> if budget exceeded: TRUNCATED
-> focus_complete=false
```

No se descartan silenciosamente matches obligatorios.

La evidencia suplementaria utiliza un budget separado:

```text
supplemental evidence
-> may discover extra context
-> may be bounded
-> supplemental truncation is visible
-> cannot convert an incomplete required focus into complete
-> cannot grant authority
```

La completitud es siempre relativa al contrato declarado del foco; no significa
conocimiento absoluto de todo el repositorio.

## 8. Frozen evidence identity

Cada ejecución focal debe materializar una identidad determinista del evidence
set.

Campos conceptuales mínimos:

```text
schema
baseline_commit
focus_id
selector_results
source path
blob_sha
line / bounded excerpt identity
required_or_supplemental
truncation state
evidence_set_digest
authority_effect
```

`evidence_set_digest` se deriva de una representación canónica ordenada y no
incluye timestamps ni outputs del modelo.

Principio:

```text
same baseline
+ same focus contract
+ same repository snapshot
-> same evidence_set_digest
```

## 9. Invariante Inspect / Analyze / Propose

Para un mismo slice:

```text
Inspect evidence_set_digest
==
Analyze evidence_set_digest
==
Propose evidence_set_digest when Propose runs
```

No es obligatorio que las tres etapas compartan el mismo objeto Python en
memoria. Sí es obligatorio que la selección sea determinista y que la identidad
material del evidence set coincida.

Mismatch:

```text
-> existing validation failure semantics
-> INCONCLUSIVE
-> STOP
```

V0 no amplía todavía el enum de reason codes del Trace únicamente para este caso.

## 10. Relación con SelfReviewEvidencePacket

No se reemplaza el packet existente.

Separación:

```text
SelfReviewEvidencePacket
-> demuestra disponibilidad del baseline general obligatorio

GovernedEngineeringEvidenceFocus
-> demuestra suficiencia/completitud del slice específico
```

Por tanto:

```text
packet READY
!= focus COMPLETE

focus COMPLETE
requires packet READY first
```

## 11. Bootstrap Multi-Focus

El bootstrap conserva exactamente tres slices iniciales:

```text
U01   Core Kernel
U04   Observability
RR-03 Strong SecurityContext Provenance
```

Los tres deben ejecutarse, cuando sean autorizados, sobre el mismo
`baseline_commit`.

No se admite agregarlos en un único subject compuesto.

### 11.1 U01 — Core Kernel

Subject estable:

```text
Kernel
```

Fuentes de implementación candidatas obligatorias:

```text
src/malak/kernel/
src/malak/services/planner.py
src/malak/contracts/capability.py
src/malak/app/composition.py
tests/test_kernel.py
```

Fuentes gobernadas candidatas obligatorias:

```text
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md
```

Preguntas preservadas:

```text
material Kernel gap?
Kernel First / Capability First erosion?
domain/authority/Memory/Security/Engineering leakage into Kernel?
removable complexity without loss of capability?
```

### 11.2 U04 — Observability

Subject estable:

```text
Observability
```

Fuentes de implementación candidatas obligatorias:

```text
src/malak/observability/
src/malak/runtime/runtime_metrics.py
src/malak/runtime/runtime_performance_profile.py
src/malak/runtime/runtime_performance_profiler.py
tests/   -> observability/runtime-metrics related tests selected deterministically
```

Fuentes gobernadas candidatas obligatorias:

```text
docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-BATCH-D.md
docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md
docs/project/sprints/proposals/MALAK-E2-STRUCTURAL-EVIDENCE-OBSERVABILITY-V0-G0-G1-DESIGN.md
```

Invariantes:

```text
metrics != audit
telemetry != authority
observation != evaluation
evaluation != authorization
```

### 11.3 RR-03 — Strong SecurityContext Provenance

Subject estable:

```text
SecurityContext Provenance
```

Fuentes de implementación candidatas obligatorias:

```text
src/malak/security/contracts.py
src/malak/security/context_issuer.py
src/malak/security/context_validator.py
src/malak/security/context_renewer.py
src/malak/security/context_propagation.py
src/malak/security/pdp.py
tests/ -> SecurityContext lifecycle/provenance related tests selected deterministically
```

Fuentes gobernadas candidatas obligatorias:

```text
SECURITY.md
docs/architecture/adr/ADR-002-policy-enforcement-boundary.md
docs/project/concepts/GOVERNED_SELF_REVIEW_BOOTSTRAP_TASK.md
docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FINAL.md
docs/project/sprints/SPRINT-7.7.md
docs/project/sprints/SPRINT-7.9.md
```

Estado heredado:

```text
ACCEPTED_RESIDUAL_RISK
non-blocking
no automatic remediation
```

La existencia del riesgo residual no permite convertir el resultado en GAP sin
evidencia actual.

## 12. Aggregation semantics

Cada slice conserva su resultado sin reinterpretación global.

```text
U01 result
U04 result
RR-03 result
```

Reglas:

```text
INCONCLUSIVE in one slice
-> remains visible
-> cannot be hidden by another PASS-like result

DEFERRED / NOT_EXECUTED
-> bootstrap complete = false

NO_CHANGE_RECOMMENDED
-> valid slice result

finding
-> no authority
```

No se introduce score global ni majority vote.

## 13. Bounded result and prompt discipline

El focus contract no autoriza prompts ilimitados.

Se preservan hard ceilings de bytes y outputs existentes.

Si required evidence no cabe dentro de un límite declarado:

```text
do not silently trim
do not raise global limit automatically
-> focus INCONCLUSIVE
-> evidence budget requires separate review
```

Esto diferencia:

```text
capacity problem
from
selection/completeness problem
```

## 14. Model isolation

Este gate no cambia el modelo local.

Regla experimental:

```text
fix evidence selection first
-> repeat with same model/runtime
-> compare behavior
-> only then benchmark alternate models
```

Cambiar modelo y retrieval en el mismo gate impediría atribuir causalidad.

La ampliación futura de model provenance se mantiene separada de este G1.

## 15. Compatibility boundary

La semántica actual de comandos directos:

```text
/engineering inspect <subject>
/engineering analyze <subject>
/engineering propose <subject>
```

no debe cambiar silenciosamente por este gate.

El focus contract se aplica al Self-Review gobernado y sólo podrá reutilizarse
por otras superficies mediante un gate explícito.

Se preserva:

```text
generic Engineering subject semantics
!= governed Self-Review focus semantics
```

## 16. Application / architecture boundary

No se modifica:

```text
Kernel
Planner
CapabilityRegistry authority
SecurityContext
Memory
Knowledge admission
Trace event schema
LIVE/REPLAY source of truth
```

La solución debe permanecer en Engineering / application orchestration y
reutilizar E0/E1/E2/E3/E4 existentes.

Un RED futuro puede demostrar que un helper/contract adicional es necesario,
pero no puede introducir una nueva capa de arquitectura sin volver al Owner.

## 17. Candidate delta máximo para RED futuro

RED podrá apuntar únicamente a demostrar contratos, no a implementar GREEN.

Áreas candidatas:

```text
src/malak/capabilities/_engineering_evidence.py
src/malak/capabilities/engineering_inspect.py
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_analyze.py
src/malak/capabilities/engineering_propose.py
src/malak/app/internal_interaction.py
src/malak/app/internal_interaction_test_v0.py
tests/test_engineering_inspect.py
tests/test_engineering_analyze.py
tests/test_engineering_propose.py
tests/test_internal_interaction_v0.py
tests/test_internal_interaction_test_v0_harness.py
```

La lista es budget máximo de superficie candidata, no autorización para tocar
todos los archivos.

STOP y volver al Owner si el cierre requiere:

```text
Kernel change
Planner change
Request contract expansion
persistent state
Memory
new DB
new event bus
agent
scheduler
network research
Trace schema expansion
generic Engineering behavior change
```

## 18. RED requirements futuros

RED deberá demostrar al menos:

```text
F01 focus has exact immutable identity
F02 focus baseline mismatch fails closed
F03 missing required selector -> incomplete
F04 unreadable required selector -> incomplete
F05 required selector budget overflow -> incomplete
F06 supplemental truncation remains visible
F07 supplemental evidence cannot make required focus complete
F08 evidence_set_digest deterministic
F09 same baseline + focus -> same evidence_set_digest
F10 Inspect/Analyze evidence identity mismatch -> INCONCLUSIVE
F11 Propose cannot run from incomplete focus
F12 U01/U04/RR-03 preserve independent results
F13 one INCONCLUSIVE slice cannot be hidden globally
F14 DEFERRED/NOT_EXECUTED prevents bootstrap-complete claim
F15 no global arbitrary evidence-limit increase
F16 generic /engineering behavior unchanged
F17 Kernel/Planner unchanged
F18 authority_effect always none
```

RED must fail against the current baseline for the new behavior before GREEN is
considered.

## 19. Critical Contract Hardening

Este contrato es crítico porque define evidence selection y completeness usados
por Engineering para producir findings/proposals.

Interpretaciones materiales cerradas:

1. Focus completeness no significa omnisciencia del repositorio.
2. Required selector missing no se convierte en supplemental search.
3. Supplemental evidence no puede satisfacer un selector obligatorio.
4. Truncation requerida no puede declararse complete.
5. Más contexto no equivale automáticamente a mejor evidencia.
6. El modelo no decide qué fuentes son obligatorias.
7. El usuario no puede inyectar selectores libres desde CLI V0.
8. Evidence digest identifica selección; no certifica verdad semántica.
9. Igual evidence set no obliga a modelos probabilísticos a devolver igual texto.
10. Slice result no se convierte en autoridad.
11. RR-03 residual risk no implica GAP actual.
12. Bootstrap incompleto no puede presentarse como completo.
13. Este gate no autoriza cambiar el modelo.
14. Este gate no autoriza el tercer U01.

Adversarial/fail-open review:

```text
unknown selector kind             -> reject
duplicate selector                -> reject or canonical de-dup before run
selector outside declared focus   -> reject
baseline mismatch                 -> STOP
missing source                    -> INCONCLUSIVE
unreadable source                 -> INCONCLUSIVE
required truncation               -> INCONCLUSIVE
digest mismatch across stages     -> INCONCLUSIVE
unknown focus_id                  -> reject
authority_effect != none          -> reject
```

Known material ambiguity unresolved:

```text
0
```

## 20. Malāk Alignment Matrix

| Fuente | Clase | Invariante/intención | Evidencia baseline | Disposición | Efecto |
| --- | --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia explícita, incertidumbre visible | E2/E3 fail-closed | ADOPT | completeness explícita |
| Governance Constitution | normativa | Human in Control; evidence != authority | authority_effect none | ADOPT | ningún focus concede authority |
| Blueprint | arquitectura | Kernel First / Capability First | Kernel desacoplado | ADOPT | Kernel delta 0 |
| SECURITY.md | protegida | provenance y fail-closed | RR-03 preservado | ADOPT | no auto-remediation |
| Architecture Quality Gates | arquitectura | minimizar complejidad y drift | collector compartido existente | ADAPT | extender selección, no framework |
| Construction Protocol | proceso | critical-contract sequence | §5.2–§5.5 | ADOPT | hardening + 4R + RDD |
| Self-Review Bootstrap | concepto | U01/U04/RR-03 separados; no-change válido | integrated | ADOPT | multi-focus bounded |
| Internal Interaction Test V0 | design integrado | U01 slice fijo y read-only | integrated | ADAPT | reemplazar limitación literal en futuro gate |
| current Engineering code | implementación | literal subject + bounded matches | current main | ADAPT | focus-aware path sólo para Self-Review |
| prior runtime evidence | evidencia | context_truncated -> E3 UNCONFIRMED | run 002 | ADOPT | causal input del gate |

Separación obligatoria:

```text
alignment evidence != authority
design PASS != RED authorization
RED authorization != GREEN authorization
GREEN != runtime execution authorization
```

## 21. Cuatro preguntas de ley

### 21.1 Blueprint

PASS.

No se agrega lógica al Kernel ni Planner. La selección permanece en Engineering /
application boundary.

### 21.2 Cognitive Constitution

PASS.

La propuesta aumenta trazabilidad epistemológica: evidencia insuficiente produce
INCONCLUSIVE y no una conclusión inventada.

### 21.3 Governance Constitution

PASS.

El focus contract no otorga permisos, no modifica baseline y termina en Owner.

### 21.4 Kernel complexity

PASS.

```text
Kernel planned delta  0
Planner planned delta 0
```

## 22. Design 4R

### Risk — PASS

Riesgos principales:

- falsa completitud;
- selector demasiado amplio;
- truncamiento oculto;
- supplemental evidence usado como required;
- drift de evidence set entre E2/E3/E4;
- scope creep hacia generic Engineering;
- uso de RR-03 como excusa para remediation.

Controles: selector cerrado, baseline binding, estado de completitud explícito,
digest determinista, slices independientes y Owner boundary.

### Readability — PASS

La separación propuesta es:

```text
global packet
-> focus contract
-> focus evidence set
-> Engineering stages
-> slice result
```

No requiere Manager/Registry adicional.

### Reliability — PASS

Mismos inputs deben producir misma selección y digest. Missing/truncated required
evidence falla cerrado.

### Resilience — PASS

El sistema puede terminar INCONCLUSIVE sin aumentar límites, cambiar modelo ni
fabricar evidencia.

## 23. RDD Stage 1 Design Check

```text
baseline identity strategy                 PASS
candidate identity strategy                PASS
evidence provenance                        PASS
Writer/Reviewer/Validator/Authority split  PASS
PASS|FAIL|INCONCLUSIVE discipline          PASS
candidate change invalidates evidence      PASS
bounded correction semantics               PASS
authority_effect                           none
RDD Stage 2                                NOT AUTHORIZED
```

Candidate identity futura deberá estar ligada al SHA exacto de la branch RED/GREEN.
Un cambio material de selectores, criterios de completitud o digest invalida la
evidencia previa.

## 24. OBS-01 / OBS-02 / Model Trace

Permanecen explícitamente fuera de alcance de este candidate:

```text
OBS-01 heartbeat / elapsed
OBS-02 diagnostic cause preservation
model tag/digest/context-window provenance
```

Son compatibles con este diseño y se abordarán después de cerrar EVID-01/EVID-02
o mediante un gate separado si el Owner así lo decide.

No se mezclan aquí para conservar causalidad y un delta acotado.

## 25. Stop conditions

STOP si:

- hace falta cambiar Kernel/Planner;
- una fuente requerida sólo puede elegirse mediante LLM;
- se necesita ocultar truncation para obtener PASS;
- se propone aumentar límites globales como solución primaria;
- generic Engineering cambia sin gate separado;
- un slice necesita baseline distinto;
- RR-03 se convierte automáticamente en remediation;
- un evidence mismatch se normaliza;
- se intenta ejecutar un tercer U01 antes de cerrar este gate;
- el diseño requiere Memory, Agent, Library externa, red o persistencia nueva.

## 26. Rollback conceptual

Hasta RED no existe runtime delta.

Si una futura implementación no puede demostrar selección determinista y
compatibilidad:

```text
revert candidate branch
-> current Engineering semantics remain intact
-> current Self-Review V0 remains fail-closed
```

No se modifica evidencia histórica de los runs anteriores.

## 27. G0/G1 disposition

```text
G0                                  PASS
G1                                  PASS
Critical Contract Hardening         PASS
Four law questions                  PASS
Design 4R                           PASS
RDD Stage 1 Design Check            PASS
known material ambiguity            0

RED authorization                   GRANTED BY OWNER POST-PR #185
implementation authorization        NOT GRANTED
runtime execution authorization     NOT GRANTED
third U01 execution                 BLOCKED
authority_effect                    none
runtime delta                       0
```

Siguiente gate permitido:

```text
RED tests only
-> candidate-bound failure evidence
-> STOP for Owner review / explicit GREEN authorization
```

## 28. RED authorization checkpoint

Después del merge humano de PR #185, el Owner autorizó avanzar al gate RED.

```text
design merge commit                a3efb42fa6ba2a441ca161c488fef554a1713b76
RED authorization                  GRANTED
GREEN / implementation             NOT AUTHORIZED
runtime execution                  NOT AUTHORIZED
third U01 execution                BLOCKED
authority_effect                   none
```

El RED candidate debe limitarse a tests y a esta actualización documental de
autoridad. No puede introducir código productivo ni corregir todavía los fallos
esperados.
