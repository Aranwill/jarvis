---
title: Malāk Progressive Cognitive Assurance Runtime — G2A Implementation Candidate Spec
status: implemented_candidate
authority: owner_authorized_candidate
language: es
as_of_date: 2026-09-11
source_baseline: cba99129e1f18f465332329c7edf1018e4379ccb
validated_candidate_sha: 3f74072d7911dfff648151bb0f7969cc84f30942
owner_authorized_at: 2026-09-11
implementation_authorized: true
g2a_authorized: true
g2a_candidate_validation: success
g2b_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
candidate_content_identity_g2_authorized: false
persistence_authorization_authorized: false
related:
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G0-INSPECTION.md
  - docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G1-DESIGN.md
---

# Malāk Progressive Cognitive Assurance Runtime — G2A Implementation Candidate Spec

## 1. Autorización

El Owner autorizó explícitamente el 2026-09-11 la implementación de:

```text
G2A — Protected Finalization Foundation
```

La autorización queda limitada a esta unidad aislada.

```text
G2A authorized
!=
G2B authorized
!=
Sprint 7.12 authorized
!=
RDD Stage 2 authorized
```

---

## 2. Objetivo verificable

Materializar una foundation determinista que represente y evalúe la transición conceptual:

```text
Generated Candidate
        ↓
Explicit Assurance Input
        ↓
Deterministic Finalization Evaluation
        ↓
Finalization Decision
```

sin conectarla todavía a la conversación real.

G2A debe demostrar:

```text
candidate != decision
unknown != accepted
policy violation != uncertainty
missing support != sufficient support
```

---

## 3. Ubicación seleccionada

La foundation se implementa como módulo interno:

```text
src/malak/core/protected_finalization.py
```

Esta ubicación NO crea una nueva layer arquitectónica, service, manager ni authority domain.

El módulo contiene únicamente:

- contratos inmutables;
- enums cerrados;
- validación estructural;
- evaluator determinista puro.

El Kernel no importa este módulo en G2A.

---

## 4. Candidate contract

```text
ProtectedResponseCandidate
├── request_id
├── session_id
├── content
├── provider
└── model
```

Reglas:

- `request_id` y `session_id` deben ser strings canónicos no vacíos;
- `content` debe ser string no blank y se preserva exactamente;
- `provider` y `model` son provenance técnica opcional;
- provenance técnica no implica autoridad;
- no se introduce hash, firma, nonce ni Content Identity G2.

```text
request correlation != content identity
provider identity != source authority
```

---

## 5. Applicability contract

Estados:

```text
NOT_APPLICABLE
REQUIRED
UNRESOLVED
```

`UNRESOLVED` nunca puede degradarse silenciosamente a `NOT_APPLICABLE`.

---

## 6. Assurance input contract

```text
ProtectedFinalizationInput
├── applicability
├── evidence_required
├── support_sufficient
├── contradiction_unresolved
└── policy_violation
```

Todos los signals son explícitos.

No existen defaults favorables.

Reglas:

```text
missing signal != favorable signal
model confidence != support_sufficient
absence of contradiction signal != contradiction resolved
```

La combinación:

```text
NOT_APPLICABLE + evidence_required=True
```

se considera inconsistente y no puede producir aceptación.

---

## 7. Decision contract

```text
ProtectedFinalizationDecision
├── request_id
├── outcome
├── reason_code
├── evaluated_at
└── policy_version
```

Outcomes implementados en G2A:

```text
ACCEPT
ABSTAIN
BLOCK
```

`QUALIFY` permanece semánticamente reservado pero no se implementa en G2A porque no existe `qualified_content` autorizado.

```text
no qualified content producer
→ no QUALIFY runtime outcome
```

---

## 8. Policy version

```text
protected-finalization/v1
```

La versión forma parte de toda decisión válida.

---

## 9. Precedencia determinista

La evaluación aplica exactamente esta precedencia:

```text
1. invalid contract / invalid evaluated_at
   → exception / no decision / no ACCEPT

2. policy_violation=True
   → BLOCK

3. applicability=UNRESOLVED
   → ABSTAIN

4. applicability=NOT_APPLICABLE + evidence_required=True
   → ABSTAIN

5. applicability=NOT_APPLICABLE
   → ACCEPT

6. applicability=REQUIRED + contradiction_unresolved=True
   → ABSTAIN

7. applicability=REQUIRED + evidence_required=True + support_sufficient=False
   → ABSTAIN

8. applicability=REQUIRED + applicable checks satisfied
   → ACCEPT
```

No existe score, majority vote, LLM verifier ni retry.

---

## 10. Reason codes

G2A congela reason codes explícitos:

```text
POLICY_VIOLATION
APPLICABILITY_UNRESOLVED
INCONSISTENT_ASSURANCE_INPUT
ASSURANCE_NOT_APPLICABLE
CONTRADICTION_UNRESOLVED
INSUFFICIENT_SUPPORT
ASSURANCE_SATISFIED
```

Los reason codes son evidencia de la evaluación; no son autoridad independiente.

---

## 11. evaluated_at

`evaluated_at` debe ser `datetime` timezone-aware en UTC.

El evaluator no consulta reloj global.

Esto preserva determinismo respecto de inputs explícitos.

---

## 12. Side effects prohibidos

G2A no puede:

- llamar red;
- invocar providers;
- invocar LLMs;
- leer o escribir Memory;
- leer o escribir Knowledge;
- persistir decisiones;
- emitir eventos obligatorios;
- modificar historial;
- modificar Kernel;
- modificar ConversationService;
- modificar ConversationCapability;
- modificar CLI;
- generar texto lingüístico alternativo;
- crear receipts durables.

La implementación candidate respeta estas restricciones.

---

## 13. Archivos de implementación autorizados

```text
src/malak/core/protected_finalization.py
tests/test_protected_finalization.py
```

Más este documento de especificación y la reconciliación documental de G1.

No se incorporaron dependencias externas ni otros cambios de runtime.

---

## 14. Tests obligatorios

Existe cobertura explícita de:

```text
wrong candidate type
→ fail safe

wrong assurance input type
→ fail safe

non-UTC evaluated_at
→ fail safe

policy violation
→ BLOCK

UNRESOLVED applicability
→ ABSTAIN

NOT_APPLICABLE + evidence_required
→ ABSTAIN

NOT_APPLICABLE valid
→ ACCEPT

REQUIRED + contradiction unresolved
→ ABSTAIN

REQUIRED + evidence required + insufficient support
→ ABSTAIN

REQUIRED + evidence required + sufficient support
→ ACCEPT

REQUIRED + evidence not required + no blockers
→ ACCEPT

same inputs
→ same outcome/reason/policy semantics
```

También se prueban invariantes estructurales de IDs, content y tipos booleanos.

---

## 15. Evidencia de validación candidate-bound

Candidate certificado antes de este cierre documental:

```text
3f74072d7911dfff648151bb0f7969cc84f30942
```

GitHub Actions Validation run `114` ejecutó la matriz:

```text
ubuntu-latest  → success
macos-latest   → success
windows-latest → success
```

Cada job completó exitosamente:

```text
Verify candidate identity
pytest
compileall
git diff --check
```

La corrida Ubuntu reportó:

```text
676 passed
```

El commit que contiene este cierre documental debe volver a pasar la misma matriz antes de considerarse candidate final de la PR.

---

## 16. Stop conditions

No se activó ninguna stop condition de G2A.

No hubo:

- Kernel changes;
- provider/runtime changes;
- Conversation wiring;
- history mutation;
- Content Identity G2;
- Memory/Knowledge;
- persistence;
- external dependencies;
- probabilistic classification;
- generated qualification content;
- expansion of public `Response` contract.

---

## 17. Estado posterior

```text
Protected Finalization Foundation:
IMPLEMENTED IN ISOLATION / VALIDATED

Live conversation assurance:
NOT IMPLEMENTED

G2B:
BLOCKED BY SIGNAL-PRODUCER GAP / NOT AUTHORIZED

Sprint 7.12:
NOT AUTHORIZED

RDD Stage 2:
NOT AUTHORIZED
```

La existencia de G2A no permite afirmar que toda respuesta conversacional de Malāk ya atraviesa assurance cognitivo runtime.
