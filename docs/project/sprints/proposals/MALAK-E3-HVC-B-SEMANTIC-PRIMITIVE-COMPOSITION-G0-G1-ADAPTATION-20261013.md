---
title: Malāk E3 HVC-B — Semantic Primitive Composition — G0/G1 Adaptation
status: design_adaptation_candidate
authority: non_normative
language: es
date: 2026-10-13
baseline_commit: 95eba75dc12b5ec27fa9eaab33f499d9440108b0
baseline_tree: 8d729fc17e5382f15343b702c48d0acdc8195c4b
trigger_issue: 311
parent_issue: 310
risk_class: 3_HIGH
critical_contract: true
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
specific_production_model_selected: false
support_sufficient_wiring_authorized: false
protected_finalization_wiring_authorized: false
hvc_c_settlement_authorized: false
kernel_delta: 0
planner_delta: 0
---

# HVC-B — Semantic Primitive Composition — G0/G1 Adaptation

## 1. Propósito

Adaptar el diseño HVC-B después del resultado terminal de #310.

#310 demostró que ningún mecanismo evaluado debe poseer por sí solo las cuatro
dimensiones de `SemanticObservationV0`. El objetivo de esta unidad es definir la
composición mínima de **primitives semánticos estrechos**, preservando exactamente
la frontera HVC-A y sin trasladar settlement desde HVC-C.

```text
primitive signal != SemanticObservationV0 truth
primitive composition != settlement
observation != support_sufficient
evidence != authority
```

Esta unidad es Design / Documentation only.

## 2. Baseline exacto

```text
repository        Aranwill/jarvis
main              95eba75dc12b5ec27fa9eaab33f499d9440108b0
tree              8d729fc17e5382f15343b702c48d0acdc8195c4b
HVC-A             integrated
HVC-B G0/G1       integrated
#310              CLOSED / INCONCLUSIVE / NO_SELECTION
G-01 V0.4         PRESERVED / NOT PASSED
U08               BLOCKED
risk              3_HIGH
critical_contract YES
authority_effect  none
```

## 3. Construction Preflight

```text
work_unit                    issue #311
work_type                    MATERIAL_G0_G1_DESIGN_ADAPTATION
last_stable_checkpoint       main@95eba75dc12b5ec27fa9eaab33f499d9440108b0
P0 repository/baseline       PASS
P1 sources/hierarchy         PASS
P2 invariants                PASS
P3 authority direction       PASS
P4 reuse/necessity           PASS / REUSE + ADAPT + COMPOSE
P5 risk                      3_HIGH
critical_contract            YES
Design 4R                    REQUIRED
RDD Stage 1 Design Check     REQUIRED
RDD Stage 2 future candidate REQUIRED
P6 scope                     FROZEN
P7 result                    PASS
authority_effect             none
```

Preflight PASS autoriza sólo este diseño.

## 4. Evidencia experimental heredada de #310

La evidencia local fue exploratoria y no es nueva autoridad normativa.

| Mecanismo | Señal útil observada | Límite observado | Disposición |
|---|---|---|---|
| Qwen 3.5 9B | soporte acotado / schema | LIMITS, scope, false FULL | NOT_QUALIFIED |
| Gemma 4 12B | mejor worker amplio observado | C05 enum inválido estable; C09 overcommit | ESCALATION_CANDIDATE_ONLY / NOT_SELECTED |
| DeBERTa NLI | entailment/contradiction primitive; ~18–20 ms | neutral colapsa LIMITS/UNKNOWN; contradiction over-fire | NARROW_PRIMITIVE_CANDIDATE |
| MiniCheck | soporte directo; ~72–79 ms | partial compound support falla; artifact no canónico | RESEARCH_ONLY |
| jevos-v4 | preguntas tipadas; ~50–66 ms residente CPU | C05 falla; C09 conflictivo; licencia pesos UNCONFIRMED | NARROW_PRIMITIVE_CANDIDATE / DUE_DILIGENCE |

Resultado heredado:

```text
full SemanticObservationV0 verifier = NOT_SELECTED
thresholds from known corpus         = FORBIDDEN
known C05/C09 tuning                 = FORBIDDEN as qualification
```

## 5. Restricción principal de HVC-A

HVC-A ya congela:

```text
1 SemanticObservationV0
↔ exactly 1 evidence_ref

claim_part_id
↔ sólo si upstream lo aporta de forma autorizada

implicit claim decomposition = forbidden
multi-observation aggregation = HVC-C
```

Por lo tanto HVC-B **no puede** resolver sus fallos creando automáticamente
claim parts, cortando evidence text o agregando varias observaciones para fabricar
una stance favorable.

## 6. Modelo de primitive seleccionado

Un primitive es una función semántica acotada y side-effect-free:

```text
PrimitiveV0(
  exact binding,
  exact claim target,
  exact evidence_ref material
)
→
YES | NO | UNKNOWN
+ mechanism identity
+ config identity
+ provenance
+ authority_effect=none
```

El primitive responde **una sola propiedad**. No produce `SemanticObservationV0`
completo, settlement, confidence-as-truth ni acción.

Primitives admisibles conceptualmente:

```text
MATERIAL_BEARING
AFFIRMATIVE_SUPPORT_EXISTS
LIMITING_NON_ESTABLISHMENT_EXISTS
INCOMPATIBLE_ASSERTION_EXISTS
EXPLICIT_EXTERNAL_DEPENDENCY_EXISTS
FULL_AFFIRMATIVE_COVERAGE
```

No se exige que exista un modelo distinto por primitive. Un mecanismo puede servir
más de uno sólo después de qualification separada por responsabilidad.

## 7. Responsibility → primitive matrix

| Dimensión HVC-A | Determinístico antes de modelo | Primitive permitido | Default fail-closed |
|---|---|---|---|
| material_bearing | binding/material presence/identity | MATERIAL_BEARING | UNKNOWN |
| semantic_stance | invalid-combination rejection | SUPPORT / LIMIT / CONTRADICTION primitives | UNKNOWN |
| scope_dependency | exact explicit structured dependency si upstream ya la codifica | EXPLICIT_EXTERNAL_DEPENDENCY_EXISTS | UNKNOWN |
| coverage | sólo facts estructurales ya autorizados; sin decomposición implícita | FULL_AFFIRMATIVE_COVERAGE | UNKNOWN |

Regla: si una dimensión no tiene evidencia semántica calificada suficiente, queda
`UNKNOWN`. No se completa por inferencia lateral.

## 8. Deterministic composition boundary

La composición HVC-B sólo puede combinar primitives que compartan exactamente:

```text
policy_version
baseline_commit
focus_id
evidence_set_digest
relation_id
finding_fingerprint
evidence_ref
claim_part_id? exact
primitive contract version
```

Cualquier mismatch invalida la composición.

La composición **no** cruza evidence refs y **no** agrega claim parts distintos.

## 9. Conflict lattice

Las señales se tratan como independientes; conflicto no implica voting.

### 9.1 Material

```text
MATERIAL yes + NON_MATERIAL evidence impossible by contract
ambiguous / primitive unavailable
→ material_bearing = UNKNOWN
```

### 9.2 Stance

Para el mismo binding:

```text
support=YES
limit=NO
contradiction=NO
→ candidate SUPPORTS

support=NO
limit=YES
contradiction=NO
→ candidate LIMITS

support=NO
limit=NO
contradiction=YES
→ candidate CONTRADICTS

all NO
→ UNKNOWN

any required signal UNKNOWN
→ UNKNOWN unless a future proof shows the remaining signal is sufficient

two-or-more YES
→ CONFLICT
→ UNKNOWN

invalid / unavailable
→ UNKNOWN
```

No existe majority vote.

### 9.3 Scope

```text
explicit_external_dependency=YES
→ EXTERNAL_REQUIRED

explicit_external_dependency=NO
→ NONE sólo si el primitive fue calificado específicamente para distinguir
   "no explicit dependency in visible observation" de ordinary uncertainty

otherwise
→ UNKNOWN
```

Ningún low score se transforma en NONE.

### 9.4 Coverage

```text
full_coverage=YES
AND candidate stance=SUPPORTS
AND material=MATERIAL
→ FULL candidate

full_coverage=NO
→ NOT FULL, pero NO autoriza PARTIAL

PARTIAL
→ sólo puede emitirse si el binding ya contiene estructura autorizada suficiente
   para demostrar soporte afirmativo parcial sin decomposición implícita

otherwise
→ UNKNOWN
```

Por diseño, `PARTIAL` puede permanecer frecuentemente UNKNOWN en HVC-B hasta que
upstream provea estructura autorizada o un mecanismo sea calificado para esa
semántica exacta.

## 10. C05/C09 hard boundaries

C05 y C09 permanecen sin cambios.

```text
rewrite evidence           FORBIDDEN for qualification
rewrite claim              FORBIDDEN for qualification
threshold tuning           FORBIDDEN
prompt tuning to GT        FORBIDDEN
GT change to model output  FORBIDDEN
```

Pueden usarse como regression/adversarial references, no como corpus ciego nuevo.

## 11. Progressive cognition / escalation

Orden permitido:

```text
deterministic precheck
→ smallest qualified primitive
→ deterministic conflict/UNKNOWN
→ optional bounded escalation
→ UNKNOWN if unresolved
```

Una escalación a modelo grande sólo se admite si:

1. el caso sigue `UNKNOWN` después de primitives normales;
2. el material es suficientemente importante para justificar coste;
3. el modelo grande está calificado para **ese subrol exacto**;
4. su salida sigue sin authority;
5. no reemplaza fail-closed por una respuesta obligatoria.

Gemma observado en #310 no queda seleccionado por este documento.

## 12. Anti-overengineering

Rechazado:

```text
semantic verifier manager
model registry persistente
ensemble voting
always-on multi-model chain
new Capability
new Kernel/Planner logic
new governance layer
implicit decomposer
automatic evidence splitter
global confidence score
```

Preferido:

```text
pure primitive adapter(s)
existing HVC-A enums/bindings
existing qualification identity patterns
deterministic composition function
UNKNOWN as valid terminal observation dimension
```

## 13. Performance budget

No se congela un producto/modelo, pero sí la política:

- normal path: no large model si deterministic/small primitive resuelve;
- resident small primitive preferido cuando esté calificado;
- model load/unload por pregunta no es arquitectura objetivo;
- latency/memory son qualification evidence, no authority;
- performance nunca permite relajar semantic safety.

Las mediciones #310 demuestran viabilidad local, no thresholds normativos.

## 14. Supply-chain rule

Un mecanismo ejecutable requiere antes de selection:

```text
exact upstream identity
exact weight/artifact digest
explicit admissible license scope
offline inference after provisioning
no hidden tool/network authority
dependency/runtime identity
reproducible local load
```

`UNCONFIRMED` en licencia o artifact provenance bloquea selección productiva.

## 15. Fresh blind qualification plan

El corpus HVC-A conocido ya no sirve para tuning/selection ciego.

Antes de RED de un primitive específico deberá existir:

1. fresh visible case-set;
2. hidden GT construido independientemente;
3. mismas boundaries semánticas, nuevos contenidos;
4. mecanismos/prompt/config congelados antes de abrir hidden GT;
5. métricas por primitive, no sólo global accuracy;
6. false favorable rates;
7. conflict/UNKNOWN preservation;
8. repeated deterministic/reproducibility checks;
9. resource measurements;
10. independent validation.

No se permite seleccionar thresholds mirando primero hidden GT.

## 16. Candidate selection strategy futura

La futura selección puede elegir:

- un único mecanismo para varios primitives **si cada subrol pasa qualification**;
- mechanisms diferentes para subroles disjuntos si el valor incremental justifica complejidad;
- ningún mecanismo y devolver UNKNOWN.

No se permite seleccionar un mecanismo por benchmark publicado solamente.

## 17. Security / authority direction

```text
CONTROL / REQUEST / POLICY
Malāk upstream
      ↓
primitive worker

SIGNAL / UNKNOWN / ERROR
Malāk upstream
      ↑
primitive worker

authority_effect = none
```

Evidence text y claim text son datos no confiables, no instrucciones.

## 18. Component / Logic Reuse Review

| Superficie | Disposición |
|---|---|
| SemanticObservationV0 | REUSE |
| exact evidence binding | REUSE |
| HVC-A fail-closed combinations | REUSE |
| blind qualification pattern | REUSE / ADAPT |
| qualification identity/bundle discipline | REUSE / ADAPT |
| deterministic routing | REUSE |
| HVC-C settlement | NO_CHANGE / future |
| Assurance Signal | NO_CHANGE |
| Protected Finalization | NO_CHANGE |
| Kernel / Planner | NO_CHANGE |
| new manager/service/registry | REJECT |

```text
architecture mode = REUSE + ADAPT + COMPOSE
NEW component     = NOT_ADMISSIBLE on present evidence
```

## 19. Design 4R

### Risk — PASS

Principales riesgos: semantic invention, primitive conflict, threshold laundering,
implicit decomposition, supply-chain ambiguity y escalation creep.

Mitigación: exact bindings, closed primitive contracts, UNKNOWN, no voting, no
cross-binding composition, fresh blind corpus y no production model selection.

### Readability — PASS

La cadena queda explícita:

```text
binding
→ primitive signal(s)
→ deterministic observation composition
→ SemanticObservationV0 candidate
→ future HVC-C settlement
→ assurance
→ finalization
→ authority
```

### Reliability — PASS

Identity de mechanism/config/artifact queda candidate-bound. Un cambio invalida
qualification previa. Conflict y missing signal no producen fallback favorable.

### Resilience — PASS

Unavailable, malformed, conflict, license UNCONFIRMED, binding mismatch o
unknown semantics producen UNKNOWN/invalid, nunca positive settlement.

```text
DESIGN_4R = PASS
```

## 20. RDD Stage 1 Design Check

```text
candidate identity strategy                PASS
baseline/candidate binding                 PASS
evidence provenance                        PASS
Writer / Reviewer / Validator / Authority PASS
PASS | FAIL | INCONCLUSIVE discipline     PASS
candidate change invalidates evidence     PASS
bounded correction                         PASS
independent fix validation future         REQUIRED
RDD Stage 2 future implementation         REQUIRED
authority_effect                          none
```

`RDD_STAGE_1_DESIGN_CHECK = PASS`.

## 21. Qué NO autoriza este diseño

```text
specific mechanism selection   NO
thresholds                     NO
RED                            NO
GREEN                          NO
runtime integration            NO
production routing             NO
HVC-C                          NO
support_sufficient             NO
Protected Finalization         NO
U08                            NO
Ready / Merge                  OWNER ONLY
```

## 22. Próximo gate propuesto

Después de integrar este diseño, el siguiente gate debe ser **fresh blind primitive
qualification design**, no implementación productiva.

Primero se seleccionará un único primitive role de alto valor y bajo acoplamiento
para probar la metodología. La elección debe hacerse con evidencia y sin
reutilizar C05/C09 como tuning set.

## 23. Terminal design result

```text
#310 full verifier selection       NO_SELECTION
#311 design adaptation             PASS
architecture                       SEMANTIC_PRIMITIVES + DETERMINISTIC_COMPOSITION
cross-binding aggregation          FORBIDDEN
implicit decomposition             FORBIDDEN
conflict                           UNKNOWN
unproven dimension                 UNKNOWN
large model                        ESCALATION_ONLY / NOT_SELECTED
specific production model          NOT_SELECTED
new manager/service                REJECTED
Kernel / Planner delta             0 / 0
HVC-C settlement                   NOT IMPLEMENTED
implementation                     NOT AUTHORIZED
RED / GREEN                        NOT AUTHORIZED
authority_effect                   none
```
