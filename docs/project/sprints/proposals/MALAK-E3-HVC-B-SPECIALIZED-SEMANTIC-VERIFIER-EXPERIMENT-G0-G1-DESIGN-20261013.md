---
title: Malāk E3 HVC-B — Specialized Semantic Verifier Experiment — G0/G1 Design
status: g0_g1_candidate
authority: non_normative
language: es
date: 2026-10-13
baseline_commit: c36b67a187d6991be05cb11cfe1cddc96558a059
baseline_tree: e7b84151ef60a568daee871baaaa382284a911f3
trigger_issue: 307
risk_class: 3_HIGH
critical_contract: true
authority_effect: none
implementation_authorized: false
red_authorized: false
green_authorized: false
support_sufficient_wiring_authorized: false
protected_finalization_wiring_authorized: false
u08_authorized: false
kernel_delta: 0
planner_delta: 0
---

# HVC-B — Specialized Semantic Verifier Experiment — G0/G1 Design

## 1. Propósito

Diseñar el experimento mínimo para evaluar un mecanismo semántico especializado, reemplazable y aislado que produzca únicamente observaciones compatibles con `SemanticObservationV0`.

Esta unidad no selecciona todavía un verifier concreto, no implementa runtime, no habilita network/tools, no modifica Kernel/Planner, no produce `support_sufficient` y no conecta Protected Finalization.

```text
mechanism output != settlement
observation != support_sufficient
qualification != production authorization
evidence != authority
```

## 2. Baseline y admisión B0

```text
repository        Aranwill/jarvis
main              c36b67a187d6991be05cb11cfe1cddc96558a059
tree              e7b84151ef60a568daee871baaaa382284a911f3
tracked blobs     396
tree truncated    false
HVC-A             integrated
G-01 V0.4         NOT PASSED
U08               BLOCKED
B0_RESULT         PASS
risk              3_HIGH
critical_contract YES
authority_effect  none
```

B0 PASS sólo autoriza este Design G0/G1.

## 3. G0 — problema real

El rol monolítico G-01 V0.4 no fue calificado. El baseline ya resuelve determinísticamente una parte del dominio y dispone de routing, binding, qualification y finalization separados.

El gap es estrecho: producir una observación semántica acotada sobre evidencia exacta, sin conceder al mecanismo settlement, finalization ni authority.

## 4. Component / Logic Reuse Review

| Superficie | Disposición |
|---|---|
| `SemanticObservationV0` | REUSE |
| HVC-A binding / exact `evidence_ref` | REUSE |
| focused evidence + `evidence_set_digest` | REUSE |
| deterministic routing | REUSE |
| blind visible/hidden qualification pattern | REUSE / ADAPT |
| qualification identity / bundle discipline | REUSE / ADAPT |
| G-01 V0.4 corpus | PRESERVE benchmark |
| Assurance Signal | NO_CHANGE |
| Protected Finalization | NO_CHANGE |
| Kernel / Planner | NO_CHANGE |
| SemanticEngine | REJECT |
| VerificationGovernor | REJECT |
| HybridVerificationManager | REJECT |
| ResponseAssuranceLayer | REJECT |
| persistent verifier registry | REJECT |

```text
reuse_disposition = REUSE + ADAPT + COMPOSE
NEW component      = NOT_ADMISSIBLE on present evidence
```

## 5. Necessity & Complexity Review

`src/malak/capabilities/_engineering_analysis.py` es un hotspot de complejidad: contiene assessment E3, routing, qualification helpers y HVC-A.

Esto no autoriza extraer un subsistema automáticamente. Para una futura PR-B:

1. intentar primero la mínima adaptación compatible con responsabilidad existente;
2. si el verifier adapter introduce acoplamiento material, justificar una extracción estrecha de adapter/evaluation logic;
3. toda extracción debe ser side-effect-free, sin authority, lifecycle, registry, manager ni dependencia de Kernel;
4. no mezclar refactor lateral salvo necesidad demostrada para límites o testabilidad.

## 6. G1 — contrato experimental

Entrada gobernada:

```text
baseline_commit
focus_id
evidence_set_digest
relation_id
finding_fingerprint
exact evidence_ref
claim root or authorized claim_part_id
visible evidence material only
```

Salida permitida: `SemanticObservationV0` con sus cuatro dimensiones, rationale bounded opcional para auditoría, mechanism identity/provenance y `authority_effect=none`.

El mechanism no puede producir `E3 SUPPORTED`, `support_sufficient`, Final Response, policy decision, tool/network request, nueva scope, Memory/Knowledge mutation ni authority.

## 7. Blind qualification y fail-closed

Hidden ground truth permanece fuera del input. Debe fallar cerrado ante forbidden label leakage, binding mismatch, malformed output, dimensión faltante, enum desconocido, mechanism unavailable, self-certification o evidence material drift.

## 8. Métricas obligatorias

No se admite un único accuracy global. Deben medirse como mínimo:

- accuracy por `material_bearing`, `semantic_stance`, `scope_dependency` y `coverage`;
- false SUPPORTS rate;
- false FULL rate;
- confusión LIMITS↔CONTRADICTS;
- UNKNOWN preservation rate;
- EXTERNAL_REQUIRED recall;
- binding violation rate;
- schema failure rate;
- abstention rate;
- latency / memory / CPU sólo cuando exista entorno ejecutable.

Los thresholds exactos se congelan antes de RED y no pueden ajustarse después de observar resultados.

## 9. Candidate mechanism selection

Este G1 no selecciona producto/modelo. Un mecanismo futuro deberá evaluarse por replaceability, structured-output fit, reproducibility, licencia/supply-chain trust, recursos, ausencia de side effects/network oculto, configuration identity, version pinning y comportamiento UNKNOWN/abstention.

Sin acceso al equipo local del Owner: `resource fit = UNTESTED` y `local execution = UNTESTED`.

## 10. Authority flow

```text
CONTROL / REQUEST / POLICY
Malāk upstream
      ↓
semantic verifier

OBSERVATION / DEFICIT / ERROR
Malāk upstream
      ↑
semantic verifier

authority_effect = none
```

`EXTERNAL_REQUIRED` informa déficit; no ordena adquirir evidencia.

## 11. Security Horizon Check

- input evidence = untrusted data;
- no prompt injection → control;
- no tools/network por default;
- no persistence;
- no Memory/Knowledge write;
- no provider trust implícito;
- unavailable/malformed → INCONCLUSIVE;
- missing assurance nunca reduce el assurance floor.

## 12. Cuatro preguntas de ley

- Blueprint: PASS — Model Agnostic, Kernel/Planner delta 0.
- Cognitive Constitution: PASS — deterministic first, additional cognition only for material deficit, Generation != Finalization, Evidence != Authority.
- Governance Constitution: PASS — Human in Control, least privilege, no self-elevation.
- Kernel complexity: PASS — HVC-B no agrega lógica al Kernel.

## 13. Design 4R

### Risk — PASS
Riesgos: false semantic support, coupling, label leakage, prompt injection, silent resource degradation, malformed output, hidden network y overclaim. Mitigación: exact binding, blind GT, replaceability, fail-closed, métricas por boundary y ausencia de positive settlement en HVC-B.

### Readability — PASS WITH CONDITION
Debe mantenerse la separación routing → observation → qualification → future HVC-C settlement → assurance projection → finalization → authority. No introducir manager universal. El hotspot `_engineering_analysis.py` debe revaluarse en PR-B.

### Reliability — PASS
Mechanism/config/schema/corpus candidate-bound; hidden GT; exact structured output; thresholds pre-frozen.

### Resilience — PASS
Unavailable/malformed/binding drift/unknown/resource unavailable nunca obtienen resultado favorable.

## 14. RDD Stage 1 Design Check

```text
candidate identity strategy                PASS
baseline/candidate binding                 PASS
evidence provenance                       PASS
Writer / Reviewer / Validator / Authority PASS
PASS | FAIL | INCONCLUSIVE discipline     PASS
candidate change invalidates evidence     PASS
bounded correction defined                PASS
independent fix validation future         REQUIRED
RDD Stage 2 future implementation         REQUIRED
authority_effect                          none
```

Resultado: `RDD_STAGE_1_DESIGN_CHECK = PASS`.

## 15. Futuro PR-B — no autorizado por este documento

Candidate mínimo esperado: tests RED del verifier adapter/evaluator, adapter/evaluation logic estrictamente necesaria, evaluation runner/artifact HVC-B y exact mechanism/config identity. Quedan fuera production routing, HVC-C settlement, `support_sufficient`, Protected Finalization y Kernel/Planner.

Si la necesidad exige salir de esos límites: `STOP → reopen admission`.

## 16. Secuencia crítica

```text
G0/G1 integrated
→ RED
→ Owner GREEN authorization
→ GREEN
→ targeted validation
→ Candidate FULL 4R
→ Bounded Correction / Fix Validator if needed
→ E2E / integration-equivalent
→ CI exact candidate
→ independent validation
→ RDD Stage 1 Candidate Conformance
→ RDD Stage 2 Receipt
→ human review
→ Owner Ready / Merge
→ post-merge reconciliation
```

## 17. Terminal design result

```text
G0                               PASS
G1                               PASS / ADAPT
architecture mode                REUSE + ADAPT + COMPOSE
specific verifier                NOT_SELECTED
new manager/service              REJECTED
new authority                    NONE
Kernel / Planner delta           0 / 0
G-01 V0.4                        PRESERVED / NOT PASSED
HVC-A                            REUSED
HVC-C settlement                 NOT IMPLEMENTED
support_sufficient               NOT AUTHORIZED
Protected Finalization           NOT WIRED
U08                              BLOCKED
implementation                   NOT AUTHORIZED
RED / GREEN                      NOT AUTHORIZED
authority_effect                 none
Ready / Merge                    OWNER ONLY
```