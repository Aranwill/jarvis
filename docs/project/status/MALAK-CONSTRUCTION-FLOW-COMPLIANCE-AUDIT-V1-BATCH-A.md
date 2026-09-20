---
title: MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 — Batch A
status: completed
authority: derived_audit
baseline_commit: b1093f291e4a83af779302454485f46f21644801
units:
  - U11
  - U13
authority_effect: none
remediation_authorized: false
---

# Batch A — Construction evidence pipeline and current flow hardening

## 1. Resultado

```text
U11 Construction evidence & validation pipeline
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

U13 Current construction-flow hardening & Evaluation Pack design
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

current blocking findings: 0
remediation authorized: false
```

## 2. U11 — Construction evidence & validation pipeline

### Evidencia histórica principal

- RDD-M1 G0 ledger sobre baseline `e8c1e5c...`;
- RDD-M1 Candidate-Bound Evidence Foundation;
- PR #64, candidate `6e2740b02482db05e84bf62cb51e05320e32a16e`;
- merge `deb759ee9855737a24b169e03bde2028c7db7f33`;
- `MALAK-EVIDENCE-MANIFEST/v1`;
- `scripts/malak_evidence.py` + tests;
- Sprint 7.11 G0 ledger y diseño;
- PR #65, candidate `59f592e2e36d11bbd14f7d9d93b1dac4f442c108`;
- Validation run `34276529587` sobre candidate exacto;
- merge `3413e8ccb348440aea757d1feccde25c65be011f`;
- ficha integrada `SPRINT-7.11.md`.

### Hallazgos históricos preservados

RDD-M1 preserva:

```text
RDD-M1-F001
RDD-M1-F002
RDD-M1-F003
RDD-M1-F004
```

F004 quedó como FAIL histórico y se produjo una re-admission separada; no fue
reescrito como PASS.

Sprint 7.11 preserva:

```text
SPRINT-7.11-F001
deprecated Node20 action runtime
→ bounded correction
→ checkout/setup-python v6
→ revalidation PASS
```

### Matriz de etapas U11

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / admission | HISTORICAL_PASS | RDD-M1 + Sprint 7.11 coverage ledgers |
| G1 design | HISTORICAL_PASS | contratos de ambas unidades |
| Critical Contract Hardening | N/A_WITH_REASON | checkpoint nominal introducido después; invariantes/threat review históricos se preservan sin relabel retroactivo |
| four law questions | HISTORICAL_PASS | RDD-M1 documenta las cuatro preguntas |
| Design 4R | N/A_WITH_REASON | separación Design 4R/Candidate FULL 4R es posterior |
| RDD Stage 1 Design Check | N/A_WITH_REASON | checkpoint formal posterior; RDD-M1 es la unidad que fundó Stage 1 |
| RED | N/A_WITH_REASON | taxonomía RED/GREEN posterior |
| GREEN | N/A_WITH_REASON | taxonomía RED/GREEN posterior |
| targeted validation | HISTORICAL_PASS | helper/tests + dogfood candidate-bound |
| Candidate FULL 4R | HISTORICAL_PASS | PR #64/#65 registran FULL 4R sobre candidates congelados |
| Bounded Correction | HISTORICAL_PASS | RDD-M1 findings + Sprint 7.11 F001 |
| Fix Validator | HISTORICAL_PASS | independent validation posterior a correction; no se infiere autoridad |
| affected revalidation | HISTORICAL_PASS | candidates corregidos revalidados |
| E2E / integration | HISTORICAL_PASS | dogfood del workflow y validation pipeline |
| CI / candidate-bound evidence | HISTORICAL_PASS | run 34276529587 sobre `59f592e2...` |
| independent validation | HISTORICAL_PASS | PR #64/#65 + G6 |
| RDD Candidate Conformance | N/A_WITH_REASON | checkpoint terminal formal posterior; manifests/G6 históricos no se renombran |
| human review | HISTORICAL_PASS | PR #64/#65 preservan human-only boundary |
| Owner Ready / Merge | HISTORICAL_PASS | ambas PR fueron mergeadas por Owner; automation sin merge authority |
| post-merge validation / reconciliation | HISTORICAL_PASS | ficha Sprint 7.11 registra Validation post-merge success; run histórico no aparece ya en consulta actual por SHA |

### Revalidación actual U11

El workflow actual conserva:

```text
pull_request + push main
exact candidate checkout
candidate identity check
contents: read
persist-credentials: false
pytest
compileall
candidate diff validation
ubuntu-latest + windows-latest
```

Validation #401:

```text
event: push
HEAD: b1093f291e4a83af779302454485f46f21644801
Ubuntu:  PASS
Windows: PASS
all workflow steps: PASS
```

`scripts/malak_evidence.py` continúa fail-closed, valida schema exacto,
candidate/baseline existence, ancestry, aggregation y `authority_effect=none`.

### Disposición U11

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current material gap: none found in Batch A
```

Limitación:

El run post-merge histórico de Sprint 7.11 registrado en la ficha integrada no
es recuperado actualmente por la consulta directa de runs por ese SHA. Se
conserva como evidencia histórica documental contemporánea; no se usa para
inventar un nuevo PASS candidate-bound.

## 3. U13 — Current construction-flow hardening & Evaluation Pack design

### Evidencia histórica principal

PR #171:

```text
base: 5c942d27...
candidate: 99298a77...
merge: 4796f4b2...
G0/G1 hardened
four law questions PASS
Design 4R PASS
RDD Stage 1 Design Check PASS
runtime delta 0
```

La revisión post-merge detectó dos findings reales:

```text
F-001 RDD Candidate Conformance estaba antes de Candidate FULL 4R
F-002 Bounded Correction había desaparecido del flujo crítico
```

Los findings no se corrigieron reescribiendo #171. Se abrió remediation
candidate separado, PR #172.

PR #172:

```text
base: 4796f4b2...
candidate: 6b3ed5b6...
merge: b1093f291...
F-001 resolved
F-002 resolved
four law questions PASS
Design 4R PASS
RDD Stage 1 Design Check PASS
Candidate FULL 4R PASS
documental E2E PASS
RDD Stage 1 Candidate Conformance PASS
authority_effect none
```

Validation #400:

```text
candidate: 6b3ed5b676bf2f1f9bfe39e266ee594facd5a53c
Ubuntu:  PASS
Windows: PASS
```

Post-merge:

```text
candidate tree = 4197753bccaa494b5530bdac853242aff26900c1
merge tree     = 4197753bccaa494b5530bdac853242aff26900c1
content delta  = 0
```

Validation #401:

```text
event: push
HEAD: b1093f291e4a83af779302454485f46f21644801
Ubuntu:  PASS
Windows: PASS
```

### Matriz de etapas U13

| Etapa | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / admission | HISTORICAL_PASS | #171/#172 |
| G1 design | HISTORICAL_PASS | Evaluation Pack + remediation contract |
| Critical Contract Hardening | HISTORICAL_PASS | #171/#172 |
| four law questions | HISTORICAL_PASS | #171/#172 |
| Design 4R | HISTORICAL_PASS | candidate-bound revalidation preserved |
| RDD Stage 1 Design Check | HISTORICAL_PASS | #171/#172 |
| RED | N/A_WITH_REASON | #172 documental, runtime delta 0 |
| GREEN | N/A_WITH_REASON | #172 documental, runtime delta 0 |
| targeted validation | HISTORICAL_PASS | deterministic order/stale-pattern checks |
| Candidate FULL 4R | HISTORICAL_PASS | #172 exact candidate |
| Bounded Correction | N/A_WITH_REASON | findings fueron post-merge y se trataron como remediation candidate nuevo, no in-candidate fix |
| Fix Validator | N/A_WITH_REASON | no in-candidate correction loop; remediation recibió validación propia |
| affected revalidation | HISTORICAL_PASS | #172 revalidó el contrato corregido |
| E2E / integration | HISTORICAL_PASS | documental E2E equivalent |
| CI / candidate-bound evidence | HISTORICAL_PASS | Validation #400 |
| independent validation | HISTORICAL_PASS | GitHub Actions + deterministic repository checks |
| RDD Candidate Conformance | HISTORICAL_PASS | manifest Stage 1 externo al candidate en #172 |
| human review | HISTORICAL_PASS | PR workflow preserved |
| Owner Ready / Merge | HISTORICAL_PASS | Owner-only; merge manual |
| post-merge validation / reconciliation | HISTORICAL_PASS | tree identity + Validation #401 + internal reconciliation |

### Disposición U13

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current material gap: none found in Batch A
```

## 4. External support observations — no verdict de Malāk

Durante el ciclo posterior se observaron en Vault/Agent:

```text
AUDIT_INDEX stale mapping
local Vault object unavailable before ancestry verification
```

Ambas observaciones permanecen fuera del verdict U11/U13 porque Vault/Agent no
son arquitectura ni authority de Malāk. Pueden informar una revisión separada de
soporte, pero no se promueven a findings de implementación de Malāk.

## 5. Batch A closure

```text
units reviewed: 2 / 13
U11: HISTORICALLY_EVIDENCED
U13: HISTORICALLY_EVIDENCED
blocking current findings: 0
historical resolved findings preserved: yes
retroactive PASS fabrication: 0
authority_effect: none

next: Batch B — U03 + U07 + U12
```
