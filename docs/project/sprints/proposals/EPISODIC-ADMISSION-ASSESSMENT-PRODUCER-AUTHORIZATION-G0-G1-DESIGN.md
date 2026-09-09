---
title: Episodic Admission Assessment Producer Authorization Boundary — G0/G1 Design Record
status: g1_design_review_pass
authority: owner-approved design record
as_of_date: 2026-09-09
unit: Episodic Admission Assessment Producer Authorization Boundary
gate: G1
source_baseline: 42bc41687a99d236b8ee59bae670bef2d37858e1
risk_class: 3
vault_reconciliation_status_at_start: resolved
vault_head_at_start: c8761523bc0176a06c1668b2ce5cf329f1d52b96
sync_agent_head_at_start: 71b21e0a192017353075954e06e2b55f5f8e2255
implementation_authorized: false
security_control_plane_change_authorized: false
admission_wiring_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
vault_reconciliation_required_before_implementation: true
language: es
---

# Episodic Admission Assessment Producer Authorization Boundary — G0/G1 Design Record

## 1. Estado de autoridad

El Owner autorizó **G1 exclusivamente para diseño** de la unidad mínima:

```text
Episodic Admission Assessment Producer Authorization Boundary
```

Esta autorización permite registrar el resultado formal de G0, definir la frontera entre provenance estructural y autorización del productor, evaluar la reutilización del Security Control Plane vigente, establecer reglas de influencia asimétrica, negative scenarios, FULL 4R, stop conditions y preguntas de G2.

No autoriza:

- código productivo;
- tests de implementación;
- cambios a `SecurityContext`;
- cambios a PDP o PEP;
- nuevas policy rules operativas;
- wiring hacia `episodic_admission.py`;
- Conversation o runtime wiring;
- persistencia, retrieval o Knowledge;
- agentes, tools o red;
- identidad criptográfica, PKI, firmas, nonce o replay protection;
- `TrustManager`, `ProducerRegistry` o authority service universal;
- Sprint 7.12;
- RDD Stage 2;
- merge sin aprobación humana.

```text
Design != Implementation
Authorization design != Authorization grant
Assessment != Authority
Evidence != Authority
```

---

## 2. Binding al baseline y estado cross-repository

Baseline fuente congelado para G0/G1:

```text
Aranwill/jarvis
main
42bc41687a99d236b8ee59bae670bef2d37858e1
```

Estado cross-repository verificado antes de abrir G1:

```text
Malāk main:
42bc41687a99d236b8ee59bae670bef2d37858e1

Project Vault main:
c8761523bc0176a06c1668b2ce5cf329f1d52b96

Vault Sync Agent main:
71b21e0a192017353075954e06e2b55f5f8e2255

post-reconciliation dry-run:
base_commit == head_commit == 42bc4168...
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Por tanto al inicio de esta unidad:

```text
BASELINE_DRIFT = 0
PROJECTION_DRIFT = 0
STATE_DRIFT = 0
```

Si este design record se integra, la proyección downstream deberá reconciliarse otra vez antes de cualquier implementación posterior.

---

## 3. Resultado formal G0

La unidad inicialmente considerada era:

```text
Assessment Provenance -> Episodic Admission Wiring
```

Resultado:

```text
DIRECT WIRING: NOT YET
```

Motivo: `assessment_provenance.py` valida estructura, candidate binding, producer role declarado y compatibilidad role/kind, pero no demuestra que el caller que declara ese role tenga autoridad gobernada para producir una assessment que pueda influir en admisión.

El riesgo concreto es:

```text
producer_role = SECURITY_TRUST_STATE
value = ACCEPTABLE
        ↓
structural provenance = VALID
        ↓
naive adapter
        ↓
source_security_status = ACCEPTABLE
        ↓
possible trust increase / ELIGIBLE
```

Eso violaría:

```text
declared producer role != authorized producer
VALID provenance != trusted truth
lower-trust input must not increase trust
```

G0 selecciona por tanto la unidad mínima:

```text
Episodic Admission Assessment Producer Authorization Boundary
```

Disposición:

```text
G0 RESULT: PASS
candidate disposition: ADAPT
risk class: 3 — HIGH
blocking findings: 0
implementation authorized: false
```

---

## 4. Necesidad real

El baseline dispone ahora de dos fronteras aisladas:

```text
Assessment Provenance Boundary
        ↓
VALID | HOLD | INVALID

Episodic Admission Boundary
        ↓
REJECT | HOLD | ELIGIBLE
```

Entre ambas falta responder de forma gobernada:

```text
¿quién está autorizado a producir esta assessment
para este tipo de assessment
y con qué alcance de influencia?
```

La provenance estructural actual responde:

```text
qué assessment
para qué candidate
qué kind
qué role declarado
qué producer reference declarada
qué rule reference
qué timestamp
```

No responde:

```text
qué principal autorizado produjo realmente el control
si ese principal tiene permiso para esa dimensión
si puede aumentar trust
si puede reducir trust
si puede forzar review
si puede provocar hard reject
```

---

## 5. Separaciones obligatorias

```text
ASSESSMENT VALUE
!=
STRUCTURAL PROVENANCE
!=
PRODUCER REFERENCE
!=
PRODUCER IDENTITY
!=
PRODUCER AUTHORIZATION
!=
INFLUENCE PERMISSION
!=
ADMISSION INPUT
!=
ADMISSION DECISION
!=
PERSISTENCE AUTHORIZATION
!=
AUTHORITY
```

También:

```text
producer_role declared != producer authority
SecurityContext authenticated != cryptographic identity
AuthorizationDecision != admission decision
admission decision != storage authorization
```

---

## 6. Decisión arquitectónica G1-D1 — Memory no crea un segundo sistema de autoridad

La autorización del productor no debe resolverse mediante:

```text
MemoryTrustManager
ProducerAuthorityRegistry
MemoryPermissionEngine
hard-coded trusted producer list inside Memory
```

El baseline ya dispone de un Security Control Plane con:

```text
SecurityContext
PermissionScope
AuthorizationRequest
AuthorizationDecision
StaticPolicyDecisionPoint
Policy Enforcement Point
```

El PDP vigente:

- valida `SecurityContext`;
- deniega sujetos no autenticados;
- deniega contextos expirados;
- usa reglas exactas `subject_id + PermissionScope`;
- no admite wildcards;
- falla cerrado si no existe policy aplicable;
- puede requerir confirmación humana.

Por tanto la dirección preferida es:

```text
Memory asks for governed authorization evidence
        ↓
existing Security Control Plane evaluates authority
        ↓
Memory verifies binding of that evidence
        ↓
STOP
```

G1 **no autoriza todavía** llamadas runtime al PDP ni nuevas `PolicyRule`.

---

## 7. Decisión G1-D2 — `producer_reference` permanece opaca

La `producer_reference` de `AdmissionAssessment` fue diseñada como referencia estructural opaca.

No debe reinterpretarse ahora como:

```text
SecurityContext.subject_id
verified identity
principal id
permission token
```

Por tanto un futuro authorization contract deberá aportar su propio binding explícito al principal autorizado sin cambiar retroactivamente el significado de `producer_reference`.

```text
producer_reference
!= producer_subject_id
unless a future approved contract explicitly proves/binds them
```

---

## 8. Decisión G1-D3 — autorización dimensional y por influencia

Autorización para producir una dimensión no implica autoridad universal.

```text
permission to assess SENSITIVITY
!= permission to assess SOURCE_SECURITY_STATUS
```

Además, incluso dentro del mismo `AssessmentKind`, el efecto importa.

G1 reconoce cuatro clases conceptuales de influencia:

```text
TRUST_INCREASING
TRUST_REDUCING
REVIEW_FORCING
HARD_REJECT
```

Estas clases describen el posible efecto downstream; **no son todavía enums autorizados para implementación**.

Regla:

```text
producer authorization
must be at least as strong as
kind scope + permitted influence class
```

Un productor autorizado para reportar sospecha no obtiene por ello autoridad para limpiar sospecha.

```text
can report SUSPECT
!= can produce ACCEPTABLE
```

---

## 9. Decisión G1-D4 — no inferir dirección de trust desde strings abiertos

Algunos valores actuales tienen semántica cerrada suficiente:

```text
SOURCE_SECURITY_STATUS:
ACCEPTABLE   -> potentially trust-increasing
UNASSESSED   -> review / no increase
SUSPECT      -> trust-reducing / review
TAINTED      -> hard-reject candidate effect
REVOKED      -> hard-reject candidate effect

SCOPE_APPLICABLE:
false        -> hard-reject candidate effect
true         -> potentially permissive / trust-increasing

POLICY_VIOLATION:
true         -> hard-reject candidate effect
false        -> potentially permissive / clearing

SENSITIVE_REVIEW_REQUIRED:
true         -> review-forcing
false        -> potentially permissive / clearing

CONTRADICTION_REQUIRES_REVIEW:
true         -> review-forcing
false        -> potentially permissive / clearing
```

Pero otras dimensiones siguen siendo strings sin taxonomía universal aprobada:

```text
SOURCE_AUTHORITY
CONFIDENCE
SENSITIVITY
```

G1 prohíbe inferir automáticamente `TRUST_INCREASING` o `TRUST_REDUCING` desde esos strings sin una policy/taxonomía gobernada futura.

Esto evita introducir una taxonomía global de trust no requerida por el baseline.

---

## 10. Decisión G1-D5 — input no autorizado no controla admisión

Una assessment sin autorización gobernada suficiente no puede mutar directamente los inputs efectivos de admisión.

```text
structurally VALID
+
producer authorization missing/denied
        ↓
NO direct admission control value
```

El contenido o evidencia no autorizada puede convertirse en input para un evaluador gobernado futuro, pero no puede autoemitir el control efectivo.

Esto también evita un vector de DoS:

```text
attacker self-declares SECURITY_TRUST_STATE
value = REVOKED
        ↓
must NOT automatically hard-reject candidate
```

Por tanto la regla monotónica previa se interpreta como:

```text
governed lower-trust evidence may support conservative downgrade
unauthorized content cannot directly impose downgrade or upgrade
```

---

## 11. Decisión G1-D6 — autorización positiva y restrictiva son asimétricas

La policy futura deberá impedir que una autorización restrictiva se reutilice para efectos permisivos.

Ejemplos:

```text
permission to mark SUSPECT
!= permission to mark ACCEPTABLE

permission to require review
!= permission to clear review

permission to report violation
!= permission to declare clean

permission to revoke
!= permission to restore trust
```

Una transición de restauración o clearing deberá requerir autoridad explícita apropiada y policy aplicable.

```text
SUSPECT -> ACCEPTABLE
TAINTED -> ACCEPTABLE
REVOKED -> ACCEPTABLE
policy_violation true -> false
review_required true -> false
```

no pueden surgir por la sola presencia de provenance estructural válida.

---

## 12. Relación candidata con Security Control Plane

El Security Control Plane actual puede expresar permisos exactos mediante `PermissionScope(resource, action)` y decisiones deny-by-default.

Eso hace viable explorar en G2 un modelo conceptualmente equivalente a:

```text
producer subject
        ↓
SecurityContext
        ↓
permission scoped to assessment kind / influence
        ↓
AuthorizationRequest
        ↓
PDP
        ↓
AuthorizationDecision
```

G1 no congela todavía strings como:

```text
resource = "memory.assessment..."
action   = "produce..."
```

ni decide si la autorización será per-assessment o reutilizable por scope/TTL.

Esas decisiones pertenecen a G2.

---

## 13. Límite de identidad y seguridad residual

El baseline conserva el riesgo conocido:

```text
SecurityContext identity/provenance
is not yet backed by a strong cryptographic root
```

Por tanto incluso una futura reutilización del PDP deberá describirse correctamente:

```text
governed internal authorization under current Security Control Plane
!= cryptographically proven external identity
```

G1 no autoriza usar esta frontera para producers remotos, agentes externos, tools externas o entornos hostiles como si existiera autenticación criptográfica fuerte.

Antes de esos escenarios deberán reevaluarse PKI, firmas, nonce/replay protection y secure messaging según SECURITY.md.

---

## 14. Frontera candidata para G2

Flujo conceptual preferido:

```text
AdmissionAssessment
        ↓
validate structural provenance
        ↓
VALID provenance?
        ↓ yes
classify allowed influence where semantics are governed
        ↓
obtain / receive producer authorization evidence
        ↓
verify binding:
  assessment
  candidate
  kind
  producer principal
  permission scope
  decision
  validity window
        ↓
AUTHORIZED | HOLD | DENIED
        ↓
STOP
```

Todavía no:

```text
AUTHORIZED
        ↓
automatic conversion to EpisodicAdmissionContext / Signals
        ↓
evaluate_episodic_candidate(...)
```

Ese wiring continuará requiriendo autorización separada.

---

## 15. Semántica candidata de resultado

G2 deberá decidir nombres exactos, pero G1 preserva conceptualmente:

```text
AUTHORIZED
HOLD
DENIED
```

Semántica:

```text
AUTHORIZED
!= trusted truth
!= ELIGIBLE
!= persistence authorization

HOLD
!= admission HOLD automatically
!= retention authorization

DENIED
!= candidate REJECT automatically
```

La frontera decide únicamente si la assessment puede **ser considerada como input gobernado** para una etapa posterior.

---

## 16. Negative scenarios obligatorios para G2/TDD futuro

- **PA-A1 — Structural provenance cannot authorize:** `VALID` provenance sin evidencia de autorización nunca habilita un efecto permisivo.
- **PA-A2 — Declared role cannot grant permission:** `producer_role=SECURITY_TRUST_STATE` no sustituye una decisión de autorización.
- **PA-A3 — Producer reference remains opaque:** una `producer_reference` textual no se convierte en `subject_id` por inferencia.
- **PA-A4 — Wrong subject binding fails closed:** autorización para otro principal no puede reutilizarse.
- **PA-A5 — Wrong candidate binding fails closed:** evidencia ligada a otro candidate no se reutiliza.
- **PA-A6 — Wrong assessment kind fails closed:** permiso para `SENSITIVITY` no autoriza `SOURCE_SECURITY_STATUS`.
- **PA-A7 — Restrictive permission cannot clear trust:** permiso para degradar/review no autoriza `ACCEPTABLE` o clear.
- **PA-A8 — Permissive effect requires explicit scope:** una assessment que aumenta elegibilidad no se admite con autorización ambigua.
- **PA-A9 — Unauthorized negative value cannot DoS:** un caller no autorizado no puede autoemitir `REVOKED`, `TAINTED`, policy violation o review efectivo.
- **PA-A10 — Expired/invalid SecurityContext fails closed:** autorización basada en contexto inválido no es utilizable.
- **PA-A11 — Denied PDP decision stays denied:** Memory no reinterpretará `allowed=False`.
- **PA-A12 — Decision/request mismatch fails closed:** `AuthorizationDecision.request_id` debe corresponder a la request usada.
- **PA-A13 — Missing evidence cannot become AUTHORIZED:** ausencia o ambigüedad produce `HOLD`/`DENIED`, nunca promoción.
- **PA-A14 — Open-string classifications do not infer trust direction:** authority/confidence/sensitivity no generan effect class sin policy gobernada.
- **PA-A15 — Authorization does not wire admission:** un resultado `AUTHORIZED` no llama por sí mismo a `evaluate_episodic_candidate`.
- **PA-A16 — Authorization does not persist:** ninguna decisión autoriza storage.
- **PA-A17 — Deterministic binding:** mismos inputs producen mismo resultado.
- **PA-A18 — No side effects:** la validación local no persiste, no usa red y no llama al LLM.

---

## 17. Preguntas que G2 deberá congelar

1. Contrato inmutable exacto de request/evidence/decision para producer authorization.
2. Cómo ligar el principal autorizado al assessment sin reinterpretar `producer_reference`.
3. Si se reutilizan directamente `AuthorizationRequest` + `AuthorizationDecision` o se define un wrapper memory-local sin autoridad propia.
4. Convención determinista de `PermissionScope` por `AssessmentKind` e influence class.
5. Cómo representar `influence class` sin crear una taxonomía universal innecesaria.
6. Qué valores pueden clasificarse de forma cerrada y cuáles deben permanecer `UNCLASSIFIED` hasta existir policy específica.
7. Si la autorización es per-assessment, per-candidate o scoped con TTL.
8. Binding mínimo requerido: assessment_id, candidate_id, kind, subject, permission, request_id, evaluated_at.
9. Precedencia entre provenance `HOLD/INVALID` y authorization `HOLD/DENIED`.
10. Cómo tratar una decisión permitida cuya request o context ya no sea válido al momento de consumo.
11. Si alguna influencia requiere `REQUIRE_HUMAN_CONFIRMATION` y bajo qué policy.
12. Cómo preservar una futura migración a identidad criptográfica sin cambiar la semántica de v1.
13. Cómo impedir replay/reuse indebido sin fingir nonce support que todavía no existe.
14. Qué evidence negativa no autorizada puede elevarse únicamente como señal para revisión sin controlar admission.

---

## 18. FULL 4R — G1

### Risk — PASS

Riesgos evaluados:

- self-asserted producer authority;
- role spoofing;
- trust elevation por provenance estructural;
- DoS mediante assessment negativa autoemitida;
- clearing indebido de `SUSPECT`, `REVOKED`, violation o review;
- duplicación del Security Control Plane dentro de Memory;
- confusión entre autorización interna y identidad criptográfica;
- authority inversion desde Memory hacia Security.

Riesgo residual explícito: el Security Control Plane actual no constituye una raíz criptográfica fuerte para producers externos/remotos.

### Readability — PASS

La unidad conserva una responsabilidad: determinar si una assessment structurally valid posee autorización gobernada suficiente para ser considerada en una etapa posterior.

No se introduce `TrustManager`, registry global ni taxonomía universal.

### Reliability — PASS condicionado a G2

G2 deberá exigir binding determinista entre assessment, candidate, principal, permission y authorization decision; `allowed=False` no puede reinterpretarse; ausencia/ambigüedad falla cerrado.

### Resilience — PASS condicionado a G2

El diseño evita tanto trust elevation como hard-reject DoS por self-assertion. Evidencia no autorizada puede alimentar evaluación posterior, pero no controlar directamente admisión.

---

## 19. Compatibilidad con arquitectura y gobernanza

```text
Blueprint compliance: PASS
Cognitive Constitution: PASS
Governance Constitution: PASS
Kernel simplicity: PASS
Human in Control: PASS
Zero Trust: PASS
Defense in Depth: PASS
Runtime Independence: PASS
```

La autoridad permanece en Security/Governance; Memory consume decisiones y evidencia sin autoasignarse permisos.

```text
Security authority
        ↓
scoped authorization evidence
        ↓
Memory validation
        ↓
possible downstream use
```

Nunca:

```text
Memory assessment
        ↑
creates Security authority
```

---

## 20. Stop conditions

Detener y volver al Owner si G2 o una implementación futura requiere:

- modificar Kernel;
- modificar Constitución, Blueprint o AQG;
- modificar `SecurityContext` sin autorización explícita;
- modificar PDP/PEP sin autorización explícita;
- introducir una autoridad paralela dentro de Memory;
- asumir identidad criptográfica inexistente;
- permitir direct admission wiring en esta unidad;
- persistencia, retrieval o Knowledge;
- agents/tools/red;
- dependency externa;
- registry persistente;
- taxonomía universal de trust;
- permitir que input no autorizado imponga un hard reject o trust increase;
- Sprint 7.12;
- RDD Stage 2.

---

## 21. Precondiciones antes de una implementación futura

```text
G2 candidate specification approved
exact implementation baseline reverified
Project Vault reconciled
TDD scenarios frozen
file/change budget frozen
FULL 4R plan frozen
Owner implementation authorization explicit
```

La integración de este design record no autoriza automáticamente G2 ni implementación.

---

## 22. Resultado G1

```text
G1 RESULT: PASS
unit: Episodic Admission Assessment Producer Authorization Boundary
disposition: ADAPT
risk class: 3 — HIGH
design accepted: true
implementation authorized: false
security changes authorized: false
admission wiring authorized: false
persistent memory authorized: false
retrieval authorized: false
knowledge authorized: false
sprint 7.12 authorized: false
rdd stage 2 authorized: false
vault reconciliation required before implementation: true
```

Próximo paso permitido únicamente mediante nueva autorización del Owner:

```text
G2 — Assessment Producer Authorization Implementation Candidate Specification
```
