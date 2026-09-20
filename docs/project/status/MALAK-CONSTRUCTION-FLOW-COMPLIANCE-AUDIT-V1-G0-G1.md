---
title: MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 — G0/G1
status: in_progress
authority: derived_audit
language: es
baseline_commit: b1093f291e4a83af779302454485f46f21644801
runtime_authority: none
implementation_authorized: false
remediation_authorized: false
rdd_stage_2_authorized: false
---

# MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 — G0/G1

## 1. Propósito

Auditar retrospectivamente las implementaciones y cambios materiales presentes
en el baseline actual de Malāk contra el flujo de construcción canónico vigente.

La auditoría determina qué evidencia existe, qué puede revalidarse hoy y qué
gaps materiales requieren hardening. No reescribe la historia ni concede
autoridad para corregir findings.

## 2. Baseline y cobertura G0

```text
repository: Aranwill/jarvis
branch: main
baseline: b1093f291e4a83af779302454485f46f21644801

tracked files discovered: 272
tracked files classified: 272
silently omitted files: 0
tree truncated: false
G0: PASS
```

Ledger:

`docs/project/status/MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1-FILE-COVERAGE.tsv`

## 3. Regla temporal

El flujo endurecido actual no se aplica retroactivamente como requisito histórico
a implementaciones creadas antes de su existencia.

```text
missing historical evidence
!= historical non-compliance
```

La auditoría distingue:

```text
historical evidence that actually exists
current-state revalidation
current material gap
```

Queda prohibido:

- reconstruir PASS desde memoria o conversación;
- crear receipts/manifests retroactivos para simular evidencia histórica;
- atribuir Design 4R/RDD histórico si no existe evidencia contemporánea;
- reescribir commits históricos;
- convertir tests actuales en prueba de que un gate histórico ocurrió.

## 4. Disposiciones terminales por unidad

Cada unidad material recibe exactamente una disposición principal:

```text
HISTORICALLY_EVIDENCED
CURRENT_STATE_REVALIDATED
PARTIALLY_EVIDENCED
UNCONFIRMED
GAP_REQUIRES_HARDENING
NOT_APPLICABLE_WITH_REASON
```

Semántica:

- `HISTORICALLY_EVIDENCED`: existe evidencia histórica suficiente del proceso
  aplicable en su época y no se detecta gap material actual.
- `CURRENT_STATE_REVALIDATED`: el comportamiento/contrato actual puede
  revalidarse, pero no existe evidencia histórica suficiente para certificar
  todo el proceso original.
- `PARTIALLY_EVIDENCED`: existe evidencia verificable de algunos gates, pero
  no alcanza para cerrar la unidad y todavía no se completó revalidación actual.
- `UNCONFIRMED`: evidencia insuficiente para afirmar cumplimiento o gap.
- `GAP_REQUIRES_HARDENING`: existe una brecha material verificable en el
  baseline actual.
- `NOT_APPLICABLE_WITH_REASON`: la unidad o etapa no está sujeta al control y
  conserva razón explícita.

## 5. Estados de evidencia por etapa

Cada etapa aplicable se registra como uno de:

```text
HISTORICAL_PASS
CURRENT_REVALIDATION_PASS
N/A_WITH_REASON
UNCONFIRMED
FAIL_CURRENT
```

`HISTORICAL_PASS` requiere evidencia contemporánea verificable.
`CURRENT_REVALIDATION_PASS` nunca se presenta como PASS histórico.

## 6. Flujo canónico evaluado

La referencia única de orden es
`docs/development/malak_construction_protocol.md §5.5`.

Etapas auditables:

```text
G0 / admission
G1 design
Critical Contract Hardening
four law questions
Design 4R
RDD Stage 1 Design Check
RED
GREEN
targeted validation
Candidate FULL 4R
Bounded Correction
Fix Validator
affected revalidation
E2E / integration
CI / candidate-bound evidence
independent validation when applicable
RDD Stage 1 Candidate Conformance
human review
Owner Ready / Merge
post-merge validation / reconciliation
```

No todas las etapas existían históricamente ni aplican a toda unidad. Las
disposiciones `N/A_WITH_REASON` deben estar justificadas.

## 7. Unidades materiales V1

| ID | Unidad | Superficie principal |
| --- | --- | --- |
| U01 | Core Kernel & capability foundation | kernel, registry, planner, contracts, request/response/types |
| U02 | Conversation & model runtime | conversation service/context/registry, LLM runtime, Ollama/mock, provider/composition |
| U03 | Security control plane & secure context lifecycle | contracts, PDP/PEP, authorization audit, issuer/validator/renewer/propagation |
| U04 | Observability & runtime performance evidence | operational events, metric stores/sinks, performance profiling |
| U05 | Episodic admission governed chain | admission, provenance, producer authorization, governed input/projection consumption |
| U06 | Candidate identity & persistence boundary | candidate content identity, persistence authorization/readiness |
| U07 | Assurance & protected finalization | assurance signal projection, protected finalization, evidence-bound transition |
| U08 | Engineering E0–E4 evidence path | repository read, knowledge read, inspect/analyze/propose, engineering evidence |
| U09 | Repository structural evidence | structural projection, lookup, E2 integration, observability |
| U10 | CLI & application composition | CLI entry, composition, capability exposure |
| U11 | Construction evidence & validation pipeline | validation workflow, malak_evidence, Evidence Manifest, RDD M1, Sprint 7.11 |
| U12 | Normative/architectural promotions | ADR-004/005/006, constitutional/Blueprint promotions and critical contract changes |
| U13 | Current construction-flow hardening & Evaluation Pack design | PR-era hardening represented by current protocol/checklist/AGENTS/Evaluation Pack |

Una fuente puede contribuir a más de una unidad; eso no duplica findings.

## 8. Scope boundary

### In scope

- repositorio oficial Malāk;
- código actual;
- tests actuales;
- Git/PR/CI verificable;
- ADR, sprint records, proposals y status docs existentes;
- proceso de construcción y evidencia interno.

### Out of scope como autoridad

- Vault;
- Vault Sync Agent;
- memoria conversacional;
- afirmaciones no preservadas en Malāk.

Observaciones de Vault/Agent pueden registrarse como evidencia externa de proceso,
pero no cambian el verdict de una implementación de Malāk ni adquieren autoridad.

## 9. Findings

Cada finding debe contener:

```text
finding_id
unit_id
type
source_of_truth
divergent_artifact_or_behavior
evidence
impact
current_or_historical
severity
disposition
remediation_authorized: false
authority_effect: none
```

Tipos preferidos cuando apliquen:

```text
BASELINE_DRIFT
ARCHITECTURE_DRIFT
DOCUMENTATION_DRIFT
CONCEPTUAL_DRIFT
ENCODING_DRIFT
STATE_DRIFT
PROCESS_EVIDENCE_GAP
CURRENT_CONTROL_GAP
```

La severidad describe impacto; no autoriza trabajo.

## 10. Orden de ejecución

La auditoría se ejecutará por batches para preservar evidencia y evitar un
verdict global basado en muestreo:

```text
Batch A: U11 + U13
  proceso de construcción actual y pipeline de evidencia

Batch B: U03 + U07 + U12
  authority/security/assurance/normative critical contracts

Batch C: U05 + U06
  episodic memory and persistence boundary

Batch D: U01 + U02 + U04 + U10
  core/runtime/observability/application

Batch E: U08 + U09
  engineering intelligence and structural evidence

Final:
  cross-unit reconciliation
  finding deduplication
  disposition per unit
  residual-risk register
```

Un batch no puede declarar PASS sobre unidades todavía no revisadas.

## 11. Critical Contract Hardening del audit contract

Esta auditoría produce evidencia que puede influir en decisiones futuras, por lo
que se trata como superficie crítica de evaluation/evidence.

Controles cerrados:

- schema de estados cerrado;
- evidencia histórica separada de revalidación actual;
- ausencia de evidencia no implica incumplimiento;
- no hay PASS por promedio;
- findings visibles por unidad;
- ningún finding autoriza remediation;
- fuentes externas no ganan autoridad;
- no existe auto-promoción de resultados;
- scope fijo U01–U13 para V1.

Ambigüedad material conocida no resuelta => `INCONCLUSIVE`.

## 12. Cuatro preguntas de ley

```text
Blueprint                         PASS
Cognitive Constitution           PASS
Governance Constitution          PASS
Kernel complexity delta          0 / PASS
```

La auditoría no modifica runtime, autoridad ni Kernel.

## 13. Design 4R

### Risk — PASS

Riesgos revisados: retroactive compliance fabrication, missing-evidence
misclassification, authority confusion, favorable sampling y remediation scope
creep.

Mitigaciones: estados cerrados, ledger exhaustivo, unit registry, no-retroactive
receipts, authority zero y batches completos.

### Readability — PASS

Separación explícita entre evidencia histórica, revalidación actual, finding
actual y autoridad. Unidades y estados poseen semántica cerrada.

### Reliability — PASS

Baseline exacto, 272/272 archivos clasificados, schema por etapa y verdict por
unidad. No se permite verdict global antes del cierre cross-unit.

### Resilience — PASS

Información faltante produce `UNCONFIRMED`, no PASS. Contradicción produce
finding. Cambio de baseline invalida el cierre y exige rebaseline/revalidación.

## 14. RDD Stage 1 Design Check

```text
baseline identity                       PASS
audit candidate identity strategy       PASS
evidence provenance                     PASS
Reviewer/Validator/Authority separation PASS
PASS|FAIL|INCONCLUSIVE discipline       PASS
missing evidence fail-safe              PASS
candidate-change invalidation           PASS
bounded remediation authority           none
authority_effect                        none
RDD Stage 2                             NOT AUTHORIZED
```

La auditoría generará evidencia candidate-bound en su branch/PR. Su resultado no
puede aprobar remediation ni merge.

## 15. RED/GREEN

```text
RED:   N/A_WITH_REASON
GREEN: N/A_WITH_REASON
reason: esta unidad es una auditoría read-only del baseline y no introduce
        comportamiento ejecutable.
```

Las verificaciones de la auditoría son checks de evidencia/revalidación, no una
implementación disfrazada.

## 16. Estado

```text
G0 coverage                         PASS
G1 audit contract                   ADMITTED
Critical Contract Hardening         PASS
four law questions                  PASS
Design 4R                           PASS
RDD Stage 1 Design Check            PASS
runtime delta                       0
remediation authority               0

Batch A                             AUTHORIZED BY OWNER "avanza"
Batch B-E                           PENDING EXECUTION
final audit verdict                 PENDING
```
