
---
id: MALAK-RDD-STAGE-2-CANDIDATE-BOUND-VALIDATION-RECEIPT-V1-G0-G1
title: RDD Stage 2 — Candidate-Bound Validation Receipt V1 — G0/G1 Design
status: DRAFT_CANDIDATE
date: 2026-10-10
repository: Aranwill/jarvis
baseline: 1e00dadc6151c38e9e7302d59e11fb7b75cba6d9
work_type: G0/G1 critical design
risk_class: 3
critical_contract: true
rdd_stage_2_design_authorized: true
rdd_stage_2_runtime_authority: none
authority_effect: none
---

# RDD Stage 2 — Candidate-Bound Validation Receipt V1 — G0/G1 Design

## 1. Instrucción del Owner y frontera

El Owner autorizó el 2026-10-10 avanzar hacia la implementación de RDD Stage 2
en Malāk con una condición explícita:

- los cambios de bajo/medio riesgo deben conservar proporcionalidad y evitar
  burocracia redundante;
- los componentes o contratos de riesgo alto/crítico deben seguir endureciéndose
  sin abrir ambigüedades y deben poder aplicar el sistema RDD completo;
- Stage 2 no puede degradar Human in Control ni convertir Evidence/Receipt en
  Authority.

Esta unidad autoriza **Design**. No autoriza por sí sola GREEN, Ready, Merge,
runtime authority, Cognitive Receipt, Protected Finalization, Persistence
Authorization, model promotion, producción ni RDD Stage 3+.

```text
Evidence != Receipt != Validation != Decision != Authority
Receipt validity != Candidate Conformance PASS
Candidate Conformance PASS != Owner approval
Receipt != Ready
Receipt != Merge
authority_effect = none
```

## 2. Problema verificable

RDD Stage 1 ya liga Evidence al candidate exacto mediante
`MALAK-EVIDENCE-MANIFEST/v1` y Candidate Conformance.

El ciclo de PR #264 mostró un gap operacional concreto: el candidate y sus
validaciones podían estar correctamente cerrados, pero la representación reusable
del paquete de Evidence seguía requiriendo reconstrucción manual y aclaraciones
adicionales.

Stage 2 debe resolver únicamente este problema:

> producir un artefacto externo, determinista y candidate-bound que preserve el
> resultado terminal de Candidate Conformance y las identidades mínimas necesarias
> para verificar posteriormente qué candidate fue evaluado y con qué Evidence.

Stage 2 no vuelve a revisar el código ni sustituye Stage 1.

## 3. Fuentes gobernantes y inputs

### 3.1 Normativas / arquitectura

- Cognitive Constitution;
- Governance Constitution;
- Blueprint;
- ADR-005 — Evidence-Bound Final Response Transition;
- ADR-006 — Protected Durable Reliance Preconditions;
- AGENTS.md;
- Engineering Method §15;
- Construction Protocol ``5.4–5.5;
- Evidence Manifest v1.

### 3.2 Reuse obligatorio

```text
Candidate Identity / Git SHA binding       REUSE
Git ancestry checks                       REUSE
MALAK-EVIDENCE-MANIFEST/v1               REUSE
scripts/malak_evidence.py validation      REUSE / ADAPT
PASS | FAIL | INCONCLUSIVE                REUSE
authority_effect = none                   REUSE
Writer/Reviewer/Validator/Authority split REUSE
canonical JSON + SHA-256                  ADAPT
new Receipt schema                       NEW / JUSTIFIED
new receipt helper                       NEW / JUSTIFIED
new runtime component/service/store      REJECT
```

La superficie NEW se justifica porque Stage 1 no posee un artifact type que
represente un Receipt y el contrato vigente prohíbe fingir que el Manifest ya lo es.

## 4. Relación con RDD externo

Malāk mantiene su RDD como adaptación propia. La implementación externa de Gentle
AI es input de investigación, no autoridad.

La evolución externa reciente hacia una transacción más atómica y con menos pasos
refuerza una restricción para Malāk: Stage 2 sólo se admite si aporta una garantía
propia verificable y no si duplica narrativamente Stage 1.

La garantía propia de este V1 será:

```text
terminal Stage 1 evidence
        ↓
deterministic external receipt
        ↓
exact candidate applicability check
        ↓
reusable audit/readback
```

No se adopta CLI, authority store, delivery gate, defaults, runner ni lifecycle de
terceros.

## 5. Separación de conceptos

### 5.1 RDD Stage 2 Receipt

`Candidate-Bound Validation Receipt` es un artifact de ingeniería.

### 5.2 Cognitive Receipt

`Cognitive Receipt` pertenece a otra línea futura relacionada con cognition,
Protected Finalization y/o durable reliance.

```text
RDD Stage 2 Receipt != Cognitive Receipt
```

Esta unidad no diseña ni activa Cognitive Receipt.

## 6. Aplicabilidad propuesta

Después de su futura integración:

```text
risk_class 0  → Stage 2 NOT_APPLICABLE
risk_class 1  → Stage 2 NOT_APPLICABLE
risk_class 2  → Stage 2 OPTIONAL / explicit admission only
risk_class 3  → Stage 2 REQUIRED
risk_class 4  → Stage 2 REQUIRED
```

Esto no modifica todavía la política Stage 1 para riesgo bajo/medio. Esa decisión
se evaluará en una unidad read-only separada de RDD Effectiveness Review.

Para riesgo 3/4, el sistema completo debe conservar:

```text
Design
→ RED/GREEN cuando aplique
→ targeted validation
→ FULL 4R
→ E2E/integration
→ CI candidate-bound
→ independent validation
→ RDD Stage 1 Candidate Conformance
→ RDD Stage 2 Receipt
→ human review
→ Owner Ready / Merge
```

## 7. Preconditions de emisión

Stage 2 V1 sólo puede emitir un Receipt cuando existen:

1. repository exacto;
2. baseline exacto;
3. candidate exacto;
4. candidate tree exacto derivable por Git;
5. baseline ancestor del candidate;
6. un **MALAK-EVIDENCE-MANIFEST/v1 real y válido** ligado al mismo candidate;
7. Candidate Conformance terminal `PASS | FAIL | INCONCLUSIVE`;
8. provenance del validator;
9. referencia externa al resultado de Candidate Conformance;
10. `authority_effect = none`.

### 7.1 Hardening crítico

Para Stage 2 V1 no se acepta como input una colección informal de comments ni una
representación equivalente no materializada.

```text
risk 3/4 + Stage 2
→ MALAK-EVIDENCE-MANIFEST/v1 required
→ no comment-only equivalent
→ no inferred package
```

Una futura versión podrá evaluar un equivalent canonicalizado si existe evidencia
de necesidad. V1 prioriza claridad y fail-closed.

## 8. Schema propuesto

Identidad:

```text
MALAK-RDD-VALIDATION-RECEIPT/v1
```

Shape exacto propuesto:

```json
{
  "schema": "MALAK-RDD-VALIDATION-RECEIPT/v1",
  "repository": "Aranwill/jarvis",
  "baseline_commit": "<40-char sha>",
  "candidate_commit": "<40-char sha>",
  "candidate_tree": "<40-char sha>",
  "unit_id": "<non-empty>",
  "risk_class": 3,
  "specification_reference": "<non-empty>",
  "scope_reference": "<non-empty>",
  "stage1_manifest_schema": "MALAK-EVIDENCE-MANIFEST/v1",
  "stage1_manifest_digest": "<sha256>",
  "stage1_manifest_result": "PASS",
  "candidate_conformance_result": "PASS",
  "candidate_conformance_reference": "<external evidence ref>",
  "correction_round": 0,
  "finding_refs": [],
  "validator": "<validator provenance>",
  "independence_reference": "<external evidence ref>",
  "evidence_references": ["<ref>"],
  "issued_at": "<UTC ISO-8601>",
  "receipt_digest": "<sha256>",
  "authority_effect": "none"
}
```

No se permiten keys extra en V1.

## 9. Canonicalización e integridad

### 9.1 Stage 1 manifest digest

El digest se calcula sobre el JSON parseado del Manifest serializado de forma
canónica:

```text
UTF-8
sort_keys = true
separators = (",", ":")
ensure_ascii = false
no insignificant whitespace
SHA-256
```

Por tanto, cambios de indentación no cambian el digest, pero cualquier cambio
semántico sí.

### 9.2 Receipt digest

`receipt_digest` se calcula sobre el Receipt canónico excluyendo únicamente el
campo `receipt_digest`.

El validator debe recomputarlo y fallar ante mismatch.

## 10. Resultado vs validez

El Receipt puede preservar:

```text
candidate_conformance_result = PASS | FAIL | INCONCLUSIVE
```

La validación estructural del Receipt es independiente:

```text
receipt validator PASS
!= candidate_conformance_result PASS
```

Un Receipt válido con `FAIL` o `INCONCLUSIVE` preserva correctamente un
resultado bloqueante.

Para riesgo 3/4:

```text
human Ready admissible
only if
receipt structurally valid
AND receipt applicable to exact current candidate
AND candidate_conformance_result = PASS
```

El Receipt no concede Ready; sólo satisface una precondición de Evidence.

## 11. Candidate change / stale detection

```text
receipt.candidate_commit != expected candidate
→ STALE_CANDIDATE
→ FAIL for applicability
```

El Receipt histórico permanece íntegro como registro, pero no puede reutilizarse
para un candidate nuevo.

```text
candidate changes
→ affected Stage 1 Evidence revalidated
→ new Candidate Conformance
→ new Stage 2 Receipt
```

## 12. Anti-recursion / ubicación del artifact

El Receipt **no puede escribirse dentro del árbol Git trackeado del candidate que
describe**.

V1 debe usar:

```text
stdout
OR
explicit --output outside repository root
```

El helper debe rechazar un output path dentro del repository root.

Motivo:

```text
write receipt into candidate tree
→ candidate identity changes
→ receipt stale at birth
→ REJECT
```

Persistencia/publicación remota del Receipt queda fuera de V1. GitHub artifacts,
PR comments, external archive o mecanismos posteriores pueden evaluarse
separadamente.

## 13. Validator / producer propuesto

Se propone reutilizar el patrón de `scripts/malak_evidence.py` mediante un helper
de desarrollo:

```text
scripts/malak_rdd_receipt.py
```

Responsabilidades permitidas:

- validar el Manifest Stage 1 reutilizando/adaptando reglas existentes;
- comprobar Git object existence;
- comprobar ancestry;
- derivar candidate tree;
- calcular canonical digests;
- emitir Receipt;
- validar Receipt;
- verificar `--expected-candidate` o `--require-current`;
- devolver JSON machine-readable;
- fail-closed.

Responsabilidades prohibidas:

- modificar source/runtime;
- commit/push/PR;
- Ready/Merge;
- consultar un LLM;
- inferir independencia de actores;
- declarar authority;
- almacenar receipts en un registry;
- red;
- secrets;
- signatures;
- model/provider selection.

## 14. Provenance e independencia

`validator` e `independence_reference` son provenance, no permisos.

El helper no puede probar identidad humana ni aislamiento de sesión.

```text
declared validator provenance
!= proven independent actor
```

Cuando independencia sea obligatoria, la evidencia externa continúa siendo
necesaria y debe ser referenciada.

## 15. Técnicas diferidas

Fuera de V1:

- hash chaining entre Receipts;
- firmas criptográficas;
- signed Receipts;
- Merkle transparency;
- external attestation;
- hardware-backed attestation;
- receipt registry/store/database;
- network publication;
- automatic delivery gate;
- auto-merge;
- runtime consumption;
- Cognitive Receipt;
- Protected Finalization wiring;
- Persistence Authorization;
- Stage 3+.

Cada una requiere necesidad y admisión propias.

## 16. Allowlist candidata de Implementation PR-B

Después de aprobación/merge humano de este Design:

```text
docs/development/rdd_validation_receipt.md
scripts/malak_rdd_receipt.py
tests/test_malak_rdd_receipt.py
docs/development/engineering_method.md
docs/development/malak_construction_protocol.md
docs/development/development_checklist.md
AGENTS.md
```

No se autoriza una octava superficie sin STOP + re-admission.

No `src/malak/**`, runtime, Kernel, Planner, dependencies, SECURITY, Constitution,
Blueprint ni ADR delta.

## 17. RED requirements

RED debe demostrar al menos:

- missing required key rejected;
- extra key rejected;
- wrong schema rejected;
- wrong repository rejected;
- invalid SHA rejected;
- missing candidate/baseline Git object rejected;
- baseline not ancestor rejected;
- wrong candidate tree rejected;
- invalid Stage 1 Manifest rejected;
- Manifest candidate mismatch rejected;
- Manifest digest mismatch rejected;
- Receipt digest mismatch rejected;
- stale expected candidate rejected;
- dirty worktree with `--require-current` rejected;
- output inside repository root rejected;
- `authority_effect != none` rejected;
- PASS/FAIL/INCONCLUSIVE conformance preserved exactly;
- risk 3/4 without FULL 4R Manifest cannot issue;
- receipt validator PASS does not rewrite conformance result.

## 18. GREEN acceptance

GREEN sólo puede agregar la mínima implementación necesaria para hacer pasar RED
sin introducir runtime components, stores, network, dependencies o delivery
authority.

## 19. Candidate FULL 4R

Por `risk_class = 3`, Implementation PR-B requiere FULL 4R completo.

### Risk

Evaluar:

- receipt spoofing;
- stale candidate reuse;
- manifest substitution;
- result confusion;
- output recursion;
- path traversal;
- provenance overclaim;
- authority smuggling.

### Readability

Evaluar:

- schema pequeño;
- semántica no ambigua;
- helper reuse;
- ausencia de framework/manager/service.

### Reliability

Evaluar:

- deterministic canonicalization;
- exact digest recomputation;
- Git binding;
- fail-closed;
- cross-platform behavior.

### Resilience

Evaluar:

- missing/corrupt files;
- unavailable Git objects;
- dirty worktree;
- interrupted output;
- invalid timestamps;
- stale receipts.

## 20. RDD Stage 1 Design Check — candidate

Este Design debe ser revisado independientemente antes de RED.

Debe comprobar:

```text
Candidate Identity strategy         PRESENT
baseline/candidate binding          PRESENT
Evidence provenance                 PRESENT
Writer != Reviewer != Validator     REQUIRED
PASS|FAIL|INCONCLUSIVE              PRESERVED
INCONCLUSIVE != PASS                PRESERVED
candidate change invalidation       PRESERVED
Bounded Correction                  REQUIRED
independent fix validation          WHEN REQUIRED
authority_effect                    none
Stage 2 Receipt != Authority        PRESERVED
Stage 3+                            NOT AUTHORIZED
```

Un PASS de este Design Check no autoriza GREEN ni implementación.

## 21. Security Horizon Check

Antes de RED de PR-B debe revalidarse:

- ninguna key/secret;
- ninguna network call;
- output path confinement;
- no symlink/path escape que permita escribir dentro del repo;
- canonicalization determinista;
- subprocess Git con argv fijo/no shell;
- no trust en Receipt fields para autoridad;
- no persistent registry;
- no external dependency.

## 22. Correction Budget

Para Design:

```text
max correction rounds = 1
scope = this design document only
```

Para Implementation PR-B:

```text
max correction rounds = 1
scope = allowlist de §16
no lateral refactor
```

Una necesidad adicional material produce STOP + nueva admisión.

## 23. Relación con simplificación futura de RDD

Esta unidad **no** decide cuánto Stage 1 debe aplicarse a riesgo 0–2.

Se abrirá una revisión read-only separada:

```text
RDD Effectiveness Review
→ recent Malāk PRs
→ defect-detection value per gate
→ redundancy/cost
→ proposal for proportional Stage 1 applicability
```

La condición del Owner ya queda preservada como objetivo:

```text
low/medium risk
→ proportional assurance

high/critical risk
→ no ambiguity
→ full assurance path
→ Stage 1 + Stage 2 when adopted
```

## 24. Terminal Design state

```text
Design candidate = DRAFT
implementation = NOT YET AUTHORIZED BY DESIGN MERGE
RED = NOT YET AUTHORIZED
GREEN = NOT YET AUTHORIZED
Stage 2 runtime authority = none
Cognitive Receipt = NOT AUTHORIZED
Protected Finalization wiring = NOT AUTHORIZED
Persistence Authorization = NOT AUTHORIZED
RDD Stage 3+ = NOT AUTHORIZED
Ready / Merge = OWNER ONLY
authority_effect = none
```
