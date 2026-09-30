---
title: Malāk E3 Governed Support Evidence Routing V0 — Pre-RED Critical Contract Hardening
status: pre_red_hardening_candidate
authority: design_evidence_only
language: es
as_of_date: 2026-09-30
source_baseline: 38b62916a2e8858876ed6b6012826c37af0edc85
source_admission_merge: 38b62916a2e8858876ed6b6012826c37af0edc85
trigger_finding: E008-SG-02
risk_class: 3_HIGH
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
model_provider_experiment_authorized: false
support_sufficient_wiring_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
---

# Malāk E3 Governed Support Evidence Routing V0 — Pre-RED Critical Contract Hardening

## 1. Propósito

Endurecer antes de RED el contrato mínimo de routing admitido por
`MALAK-E3-GOVERNED-SUPPORT-EVIDENCE-ROUTING-V0-G0-G1-ADMISSION-20260930.md`.

Este gate no implementa un router, oracle, assessor, model, provider, harness ni
wiring downstream. Su única función es cerrar las interpretaciones materiales
conocidas que podrían producir un routing fail-open, exponer ground truth,
seleccionar un oracle por heurística o convertir una clasificación de evidencia
en autoridad.

La pregunta exacta es:

> Dado un subject E3 ligado a baseline, focus, evidence set, relation y finding,
> ¿puede Malāk clasificar de forma determinista y fail-closed si existe un oracle
> gobernado con cobertura total de la pregunta exacta, si queda residuo
> inferencial o si el material es insuficiente, sin ejecutar todavía un modelo ni
> producir `support_sufficient`?

## 2. Baseline y cobertura

```text
repository            Aranwill/jarvis
baseline              38b62916a2e8858876ed6b6012826c37af0edc85
baseline tree         7dfa8430fd01f6ad6789debe61a9b0c043d73a42
tracked blobs         351
recursive truncated   false
```

El File Coverage Ledger de este gate contiene exactamente 351 filas de artefactos
más header y reconcilia el árbol completo del baseline.

La cobertura reutiliza la clasificación ya cerrada del ledger G0/G1 únicamente
como evidencia previa; se revalida contra el árbol actual y agrega los dos
artefactos integrados por PR #233. Reusar clasificación no concede autoridad de
cambio.

No se abrió ni procesó ningún archivo marcado `REJECTED_DO_NOT_READ`.

## 3. Scope congelado

### 3.1 Dentro de scope

```text
support evidence route contract
deterministic oracle eligibility
deterministic oracle full-coverage requirement
exact relation/question binding
routing precedence
blind experiment projection boundary
unknown/missing/duplicate handling
skip/bypass resistance
candidate/evidence invalidation
resource and side-effect boundaries
Design 4R
RDD Stage 1 Design Check
```

### 3.2 Fuera de scope

```text
src/malak/** implementation
tests/** RED
oracle implementation
oracle registry / manager
assessor implementation
assessor execution
Ollama
external LLM/API
provider selection
network
tools
Memory / persistence
E4 changes
Protected Finalization changes
Assurance Signal Projection changes
support_sufficient wiring
Kernel / Planner / Registry changes
RDD Stage 2
Sprint 7.12
```

## 4. Separación de responsabilidades

```text
Governed Evidence Focus
        ↓
exact relation + evaluation question
        ↓
bound finding/evidence packet
        ↓
Support Evidence Routing V0
        ├─ DETERMINISTIC
        ├─ INFERENTIAL
        └─ INSUFFICIENT
        ↓
future bounded mechanism, if separately authorized

routing != oracle execution
routing != support assessment result
routing != support_sufficient
routing != finalization
routing != authority
```

El router futuro no modifica el finding, no reescribe evidence roles, no produce
verdad, no crea permisos y no decide Ready/Merge.

## 5. Routing subject identity

Toda decisión válida debe quedar ligada como mínimo a:

```text
routing_policy_version
baseline_commit
focus_id
evidence_set_digest
relation_id
evaluation_question_identity
finding_fingerprint
resolved evidence material identity
eligible oracle contract identity, when applicable
oracle qualification identity, when applicable
```

`evaluation_question_identity` debe derivarse de la pregunta gobernada exacta y
no de keywords, embeddings, similitud textual ni inferencia libre.

Cambio material de cualquiera de esos bindings invalida la decisión previa.

No se crea en V0 un registry global, content-identity subsystem ni nueva capa de
autoridad.

## 6. Route kind — enum cerrado

Una clasificación de routing exitosa usa exactamente:

```text
DETERMINISTIC
INFERENTIAL
INSUFFICIENT
```

### DETERMINISTIC

Sólo es admisible cuando existe exactamente un oracle gobernado elegible,
ligado a la relation/question exacta, con qualification vigente y cobertura total
demostrada para esa pregunta y sus inputs requeridos.

```text
oracle exists
+ exact relation binding
+ exact question binding
+ exact input contract
+ qualification bound to oracle version/content
+ full coverage demonstrated
+ required material present
= DETERMINISTIC eligible
```

`DETERMINISTIC` no significa que el oracle ya se haya ejecutado ni que el
finding esté soportado.

### INFERENTIAL

Es admisible cuando no existe un oracle determinista elegible con cobertura total,
pero el packet está estructuralmente completo y acotado para que una futura
evaluación semántica pueda ser considerada.

```text
INFERENTIAL
!= call LLM
!= model authorized
!= human review authorized
!= support sufficient
```

En este gate sólo identifica residuo inferencial.

### INSUFFICIENT

Se usa cuando el material requerido para el subject no está disponible,
completo, ligado o dentro del scope necesario para una futura evaluación bounded.

`INSUFFICIENT` no significa que el finding sea falso.

## 7. Fallos de contrato no son un cuarto route kind

Los fallos estructurales del propio routing no se degradan silenciosamente a una
de las tres rutas.

Ejemplos:

```text
unknown policy version
malformed input
relation/question binding mismatch
duplicate eligible full-coverage oracles
stale oracle qualification
invalid oracle identity
candidate/evidence binding mismatch
unbounded input
```

Resultado del gate/evaluador:

```text
INCONCLUSIVE
no route record positivo
no fallback
no authority effect
```

Así se preserva la triada semántica sin convertir errores de contrato en
`INSUFFICIENT`.

## 8. Oracle contract mínimo

Un oracle determinista candidato debe declarar de forma verificable:

```text
oracle_id
oracle_version
oracle_content_digest
relation_id
evaluation_question_identity
input_contract_identity
output_contract_identity
qualification_identity
coverage_claim = FULL
authority_effect = none
side_effect_class = NONE
```

La declaración `coverage_claim = FULL` por sí sola no es evidencia de cobertura.

La eligibility exige qualification independiente o evidencia determinista
equivalente que demuestre el alcance exacto.

```text
oracle self-declaration
!= qualification
!= full coverage
```

## 9. Full-coverage rule

Un oracle sólo puede llevar a `DETERMINISTIC` si resuelve la pregunta completa
dentro del contrato gobernado.

No son cobertura total:

```text
una cláusula de una pregunta compuesta
una heurística por nombre
un test relacionado pero no equivalente
un grep o literal match
una mayoría de checks
un score
una confidence
un documento de alta autoridad semánticamente irrelevante
un resultado histórico sobre otra versión
```

Una cobertura parcial puede servir como evidencia de diseño futura, pero en V0:

```text
PARTIAL oracle
→ never DETERMINISTIC route
```

## 10. Eligibility y unicidad

La selección no usa prioridad implícita ni first-match.

```text
0 eligible FULL oracle
→ evaluar completitud estructural del packet
→ INFERENTIAL o INSUFFICIENT

1 eligible FULL oracle
→ DETERMINISTIC

>1 eligible FULL oracle para el mismo subject exacto
→ INCONCLUSIVE
→ no arbitrary winner
```

Si dos oracles son materialmente equivalentes, una política futura podrá
canonicalizarlos, pero no se inventa esa equivalencia en V0.

## 11. Precedencia determinista

Orden obligatorio antes de cualquier futura ejecución:

```text
P01 top-level schema / hard bounds
P02 routing policy version
P03 baseline / focus / evidence-set binding
P04 finding fingerprint / resolved material binding
P05 relation identity / evaluation-question identity
P06 oracle contract identity and qualification binding
P07 eligible FULL-oracle cardinality
P08 required material completeness
P09 route classification
```

P01-P08 no pueden ser sustituidos por un model, prompt, reviewer libre ni
confidence score.

## 12. Material completeness para residuo inferencial

`INFERENTIAL` sólo exige completitud estructural bounded; no afirma suficiencia
semántica.

Como mínimo:

```text
statement present and bounded
relation/question exact
all explicit support refs resolve
all explicit limiting/counterevidence refs resolve
evidence roles structurally valid
baseline/focus/evidence-set binding exact
no scope expansion required merely to materialize declared refs
```

Cuando lo declarado no puede materializarse, la ruta es `INSUFFICIENT`, no
`INFERENTIAL`.

## 13. No-fallback / bypass resistance

Reglas obligatorias:

1. ausencia de oracle nunca equivale a `SUPPORTED`;
2. partial oracle nunca se promociona a FULL por fallback;
3. oracle unavailable o malformed después de una futura selección
   `DETERMINISTIC` no cambia automáticamente a `INFERENTIAL`;
4. un error de routing no habilita assessor/model execution;
5. `INSUFFICIENT` no puede invocar un assessor para "rellenar" evidencia faltante;
6. `INFERENTIAL` no ejecuta un LLM por existir;
7. unknown relation/question no usa nearest match;
8. duplicate eligible oracle no usa first/last wins;
9. tests no son importados como runtime productivo;
10. ninguna downstream layer puede convertir route kind en autoridad.

Cualquier política de fallback futura requiere su propio gate y causal tests.

## 14. Blind Experiment Projection

Antes de evaluar cualquier assessor/oracle candidate contra un corpus con ground
truth debe existir una frontera ciega.

### 14.1 Ground truth permitido sólo del lado de qualification

Puede existir en el corpus:

```text
expected_outcome
expected_reason_codes
critical_properties
case_class
expected_route
reviewer annotations
qualification thresholds
```

### 14.2 Candidate projection

El mecanismo evaluado puede recibir únicamente material necesario para resolver
su tarea:

```text
opaque input identity
subject
relation/evaluation question
repository evidence material
knowledge evidence material
binding expectations strictly required by the candidate contract
bounded policy/config material explicitly allowed
```

No recibe ground truth ni derivados equivalentes.

### 14.3 Separación temporal

```text
hidden ground truth
        │
        ├────────────── qualification/reviewer side
        │
blind projection
        ↓
candidate mechanism
        ↓
candidate result artifact sealed
        ↓
qualification compares artifact vs hidden ground truth
```

La comparación con ground truth ocurre después de producir y sellar el artifact
del candidato.

### 14.4 Leakage

Cualquier canal que entregue expected labels, reasons o propiedades críticas al
candidate invalida el experimento.

```text
ground-truth leakage > 0
→ qualification cannot PASS
```

## 15. Authority boundaries

Invariantes:

```text
route kind                != authority
oracle result             != authority
qualification PASS        != authority
assessment SUPPORTED      != authority
support_sufficient        != authority
model output              != authority
human review evidence     != merge authority
```

`authority_effect` permanece exactamente `none`.

## 16. Side-effect y resource boundaries

Este V0 de routing se diseña como pure/bounded decision surface.

No debe:

```text
open network
call provider/model
execute tools
write files
persist Memory/Knowledge
mutate candidate
modify evidence
spawn agents
invoke Kernel routing
consume unbounded collections
```

Inputs futuros deben estar materializados y bounded antes del routing.

## 17. Unknown / missing / duplicate handling

```text
unknown version                  → INCONCLUSIVE
unknown relation/question        → INCONCLUSIVE
missing required binding         → INCONCLUSIVE
missing declared evidence        → INSUFFICIENT
duplicate logical evidence ref   → INCONCLUSIVE
duplicate FULL oracle candidate  → INCONCLUSIVE
stale oracle qualification       → INCONCLUSIVE
oracle contract malformed        → INCONCLUSIVE
scope expansion required         → INSUFFICIENT
```

Ninguno produce `DETERMINISTIC` por fallback.

## 18. Invalidation y rollback

Invalida routing evidence previa:

```text
baseline changes materially
focus changes
evidence_set changes
relation/evaluation question changes
finding fingerprint changes
resolved evidence material changes
oracle implementation/content digest changes
oracle contract changes
oracle qualification changes/expires
routing policy version changes
blind projection policy changes for evaluation evidence
```

Rollback consiste en volver al último candidate/baseline cuya evidencia siga
ligada y válida. No se reutiliza un PASS stale.

## 19. Métricas mínimas de un futuro RED/GREEN

Sin thresholds de optimización aún:

```text
deterministic_route_count
inferential_route_count
insufficient_route_count
routing_inconclusive_count
partial_oracle_promoted_to_deterministic_count
stale_oracle_promoted_count
ambiguous_oracle_auto_selected_count
ground_truth_leakage_count
model_or_provider_calls_during_routing
authority_effect_violations
```

Safety floor:

```text
partial oracle promoted                      = 0
stale oracle promoted                        = 0
ambiguous oracle auto-selected               = 0
ground-truth leakage                         = 0
model/provider calls during routing          = 0
authority_effect violations                  = 0
```

## 20. RED causal matrix — no autorizado todavía

Un RED futuro, con autorización humana separada, debe demostrar causalmente al
menos:

```text
R01 route kind enum is closed to DETERMINISTIC/INFERENTIAL/INSUFFICIENT
R02 exact unique FULL oracle can route DETERMINISTIC
R03 PARTIAL oracle can never route DETERMINISTIC
R04 no FULL oracle + complete bounded material routes INFERENTIAL
R05 incomplete declared material routes INSUFFICIENT
R06 unknown policy/version produces no positive route
R07 stale oracle qualification cannot route DETERMINISTIC
R08 multiple eligible FULL oracles fail closed
R09 relation mismatch cannot route DETERMINISTIC
R10 evaluation-question drift invalidates prior routing
R11 evidence/finding drift invalidates prior routing
R12 routing does not call model/provider
R13 INFERENTIAL classification does not execute assessor
R14 INSUFFICIENT classification does not execute assessor
R15 deterministic oracle failure does not silently fallback
R16 authority_effect other than none fails closed
R17 blind projection excludes ground-truth fields
R18 qualification compares only after candidate artifact is produced
R19 generic E3 behavior remains unchanged
R20 E4 remains unchanged
R21 Kernel/Planner/Registry remain untouched
R22 support_sufficient remains unwired
```

Compatibility guards ya verdes no deben etiquetarse como causal RED si no fallan
por ausencia del nuevo contrato.

## 21. Candidate implementation surface — no autorizada

Si RED fuese autorizado y demostrara necesidad, la primera superficie a evaluar
debe ser la mínima que reutilice primitivas E3 existentes.

La ubicación exacta no se congela en este gate.

Preferencias:

```text
no new manager
no new registry unless necessity is demonstrated
no Kernel change
no provider/model dependency
no duplicate support subsystem
prefer pure helper/contract near existing E3 support logic when justified
```

Los tests existentes pueden inspirar invariantes, pero runtime no importará
`tests/**`.

## 22. External-reference boundary

Este hardening no incorpora código, schema, state machine, runtime ni autoridad
de repositorios externos.

La comparación con Gentle AI / Gentle Shell preservada en G0/G1 permanece
evidencia histórica/comparativa. Este contrato se deriva del baseline interno y
de las fundaciones de Malāk.

```text
external observation
→ principle candidate
→ Malāk revalidation
→ internal derivation
!= copied implementation
!= architectural authority
```

No se agrega dependencia externa.

## 23. Ambiguity / adversarial interpretation review

Se cierran explícitamente estas interpretaciones materiales:

| interpretación adversarial | disposición |
|---|---|
| "si no hay oracle, usar modelo" | REJECT — INFERENTIAL no ejecuta nada |
| "oracle parcial es mejor que ninguno" | REJECT para DETERMINISTIC |
| "dos oracles permiten elegir cualquiera" | REJECT — INCONCLUSIVE |
| "qualification anterior sirve tras cambiar oracle" | REJECT — stale binding |
| "alta autoridad documental prueba soporte" | REJECT — authority != semantic support |
| "INSUFFICIENT puede completarse con imaginación del assessor" | REJECT |
| "DETERMINISTIC significa SUPPORTED" | REJECT |
| "ground truth puede ir en prompt porque es sólo eval" | REJECT |
| "tests pueden importarse como runtime" | REJECT |
| "route kind puede alimentar support_sufficient directamente" | REJECT en este gate |

No queda ambigüedad material conocida sin disposición para RED.

## 24. Cuatro preguntas de ley

### 24.1 Blueprint

**PASS.**

Preserva Kernel First, Capability First y Runtime Independence. No introduce
provider/model dependency ni bypass de capas.

### 24.2 Cognitive Constitution

**PASS.**

Prioriza determinismo cuando existe prueba bounded, explicita incertidumbre y
prohíbe convertir generación/inferencia en verdad o finalización.

### 24.3 Governance Constitution

**PASS.**

`authority_effect = none`, Human in Control intacto, ningún resultado técnico
promueve candidate, Ready o merge.

### 24.4 Complejidad del Kernel

**PASS.**

Kernel delta = 0. El routing no pertenece al Kernel y no agrega responsabilidades
al core.

## 25. Design 4R — pre-RED

### Risk — PASS

Riesgos principales identificados y cerrados por contrato:

- false deterministic routing;
- stale/ambiguous oracle selection;
- inference-by-default;
- ground-truth leakage;
- fallback silencioso;
- authority confusion.

Safety floors son cero para las clases críticas.

### Readability — PASS

Se separan explícitamente:

```text
routing
oracle eligibility
oracle execution
support assessment
qualification
support_sufficient
authority
```

La triada sólo describe rutas válidas; errores estructurales permanecen
`INCONCLUSIVE`.

### Reliability — PASS

La decisión depende de identity/binding exactos, unicidad del oracle,
qualification ligada, full coverage y material completo. No usa heurística por
nombre, score o similitud.

### Resilience — PASS

Unknown, stale, duplicate, malformed y scope expansion cierran sin ejecución
adicional. No existe fallback implícito a modelo/provider.

```text
Design 4R = PASS
authority_effect = none
```

Este PASS no sustituye Candidate FULL 4R futuro.

## 26. RDD Stage 1 Design Check — pre-RED

### Candidate identity strategy

El futuro RED/GREEN se ligará a commit SHA exacto. Toda evidencia candidate-bound
se invalida si cambia el candidate material afectado.

### Baseline/candidate binding

Baseline de este diseño: `38b62916a2e8858876ed6b6012826c37af0edc85`. El futuro candidate declarará baseline
ancestor + candidate exacto.

### Evidence provenance

Fuentes de diseño: repositorio oficial, contratos E3 integrados, tests vigentes,
documentación normativa y evidencia de qualification ya integrada. Evidencia
externa comparativa no tiene autoridad.

### Role separation

```text
Writer
!= Reviewer when independent review is required
!= Validator
!= Authority
```

Owner conserva Ready/Merge.

### Result enum

Los checkpoints RDD usan únicamente:

```text
PASS
FAIL
INCONCLUSIVE
```

`INCONCLUSIVE != PASS`.

### Invalidation

Cambiar candidate, policy, oracle binding, evidence binding o blind projection
invalida la evidencia afectada.

### Bounded Correction

Un finding futuro no amplía silenciosamente scope. Corrección acotada, nuevo
candidate identity y revalidación afectada.

### Authority

```text
authority_effect = none
RDD Stage 2 = NOT AUTHORIZED
```

**RDD Stage 1 Design Check: PASS.**

Este resultado no es RDD Stage 1 Candidate Conformance.

## 27. Critical Contract Hardening result

```text
ambiguity review                    PASS
adversarial interpretation          PASS
fail-open/fail-closed               PASS
authority boundaries                PASS
input/schema strictness             PASS
candidate/evidence binding          PASS
unknown/missing/duplicate handling  PASS
skip/bypass paths                   PASS
resource/side-effect boundaries     PASS
rollback/invalidation               PASS
four law questions                  PASS
Design 4R                           PASS
RDD Stage 1 Design Check            PASS

authority_effect                    none
implementation authorized           false
RED authorized                      false
GREEN authorized                    false
model/provider experiment           false
support_sufficient wiring           false
RDD Stage 2                         false
```

No queda una ambigüedad material conocida que bloquee técnicamente el ingreso a
RED.

Por gobernanza:

> **RED queda técnicamente ADMISIBLE pero NO AUTORIZADO.**

La siguiente acción requiere autorización humana separada y deberá ser un RED
mínimo causal sobre este contrato, no una implementación productiva ni un
experimento con modelo.
