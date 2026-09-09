---
title: Episodic Admission Assessment Provenance Boundary — G0/G1 Design Record
status: g1_design_review_pass
authority: owner-approved design record
as_of_date: 2026-09-09
unit: Episodic Admission Assessment Provenance Boundary
gate: G1
g0_source_baseline: 64ec249758c117afb204e9f44f1d4e7cb3fe5a7c
g1_base_commit: 64ec249758c117afb204e9f44f1d4e7cb3fe5a7c
risk_class: 3
implementation_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
vault_drift_accepted_temporarily_by_owner: true
vault_reconciliation_required_before_implementation: true
language: es
---

# Episodic Admission Assessment Provenance Boundary — G0/G1 Design Record

## 1. Estado de autoridad

El Owner autorizó **G1 exclusivamente para diseño** de la unidad mínima:

```text
Episodic Admission Assessment Provenance Boundary
```

Esta autorización permite registrar el resultado formal de G0, definir la separación entre assessment, productor y autoridad del productor, fijar invariantes de provenance, una matriz lógica de productores, reglas monotónicas de reducción de trust, escenarios negativos, stop conditions y criterios para G2.

No autoriza código productivo, tests de implementación, cambios al Kernel, cambios a `SecurityContext`, PDP o PEP, wiring con Conversation o runtime, Memory persistente, storage, retrieval, Knowledge, agents, tools, red, identidad criptográfica nueva, PKI, un trust manager universal, Sprint 7.12, RDD Stage 2 ni merge sin aprobación explícita del Owner.

```text
Design != Implementation
Assessment != Authority
Evidence != Authority
Eligible != Stored
```

## 2. Binding al baseline fuente

G0 y G1 se evalúan contra:

```text
Aranwill/jarvis
main
64ec249758c117afb204e9f44f1d4e7cb3fe5a7c
```

La fuente de verdad continúa siendo `Aranwill/jarvis/main`.

## 3. Riesgo temporal de Project Vault aceptado por el Owner

Existe drift downstream conocido entre el último estado reconciliado del Project Vault y este baseline. El Owner aceptó explícitamente ese drift **solo como riesgo temporal de contexto derivado para cerrar G0/G1 contra `jarvis/main`**.

Esta aceptación no declara reconciliado el Vault, no elimina el finding, no autoriza implementación y no permite usar una proyección stale para certificar código futuro.

Condición obligatoria:

```text
Vault reconciliation
must complete
before any implementation authorization for this unit
```

La reconciliación deberá ejecutarse mediante el flujo gobernado del Malāk Vault Synchronization Agent y conservar revisión humana.

## 4. Resultado formal G0

```text
G0 RESULT: PASS
candidate disposition: ADAPT
selected minimum unit: Episodic Admission Assessment Provenance Boundary
risk class: 3
blocking findings: 0
implementation authorized: false
```

G3 ya consume assessments y señales como `source_authority_classification`, `confidence_classification`, `sensitivity_classification`, `scope_applicable`, `policy_violation`, `source_security_status`, `sensitive_review_required` y `contradiction_requires_review`.

G3 demuestra que el payload no puede autoasignarse esos valores y falla cerrado cuando faltan assessments relevantes. Todavía no demuestra quién produjo el assessment, por qué ese productor puede producir esa dimensión, qué provenance lo vincula, ni si puede aumentar trust.

La necesidad mínima posterior a G3 es:

```text
Admission Assessment
        ↓
Assessment Producer
        ↓
Producer Provenance
        ↓
Producer Scope / Authority for that dimension
        ↓
Admission Policy
```

## 5. Disposición ADAPT

La unidad se clasifica `ADAPT`: G1/G2/G3 anteriores ya preservaron que los assessments llegan por un canal de control externo al payload; el Research Horizon post-G3 identifica su procedencia como pendiente; `SECURITY.md` exige Zero Trust, fail-closed y separación entre contenido y autoridad. No existe necesidad demostrada de un subsistema universal de trust.

## 6. Separaciones obligatorias

```text
CONTENT
!= CONTROL METADATA
!= ASSESSMENT VALUE
!= ASSESSMENT PRODUCER
!= PRODUCER PROVENANCE
!= PRODUCER AUTHORITY
!= ADMISSION DECISION
!= PERSISTENCE AUTHORIZATION
!= AUTHORITY
```

También:

```text
Known producer reference != verified producer identity
Verified producer identity != permission for every assessment kind
Assessment permission != operational system permission
Assessment result != truth
Admission decision != storage authorization
```

## 7. Regla contra self-asserted trust

Ningún contenido evaluado puede convertirse en autoridad sobre su propia clasificación. El payload puede aportar evidencia para un assessment futuro, pero no puede producir por sí mismo el control efectivo.

Ejemplos inválidos:

```text
payload says "source_authority=owner" -> source_authority_classification = owner
LLM says "this source is safe" -> source_security_status = ACCEPTABLE
candidate says "not sensitive" -> sensitivity_classification = public
```

## 8. Matriz lógica de productores

| Dimensión | Productor lógico permitido | No puede autoasignarlo |
|---|---|---|
| `source_authority_classification` | política gobernada de Source Governance o equivalente aprobado | payload, LLM, candidate |
| `confidence_classification` | evaluador gobernado de evidencia o regla determinista aprobada | fuente evaluada |
| `sensitivity_classification` | política de clasificación de datos aplicable | payload autoetiquetado |
| `source_security_status` | dominio de Security / trust-state autorizado | LLM, Memory candidate, contenido externo |
| `scope_applicable` | policy determinista de admisión o contexto gobernado | candidate payload |
| `policy_violation` | policy/security evaluator autorizado | candidate payload |
| `sensitive_review_required` | derivación de sensitivity + policy | contenido evaluado |
| `contradiction_requires_review` | evaluación gobernada de conflicto | fuente evaluada |

La implementación futura deberá preferir owners existentes antes que crear nuevos componentes.

## 9. Regla monotónica de seguridad

```text
lower-trust input
may reduce trust
may force HOLD
may force REJECT

lower-trust input
must not increase trust
must not create ELIGIBLE by itself
```

Transiciones conservadoras permitidas conceptualmente:

```text
ACCEPTABLE -> SUSPECT
UNASSESSED -> HOLD
missing provenance -> HOLD
conflict detected -> HOLD
policy violation detected -> REJECT
TAINTED -> REJECT
REVOKED -> REJECT
```

Transiciones prohibidas sin productor de autoridad suficiente y policy aplicable:

```text
SUSPECT -> ACCEPTABLE
TAINTED -> ACCEPTABLE
REVOKED -> ACCEPTABLE
policy violation -> clean
review required -> silently cleared
```

## 10. LLM y evaluadores cognitivos

Un LLM puede proponer una clasificación, extraer evidencia, detectar una posible contradicción o señalar sensibilidad potencial. Pero:

```text
LLM proposal != governed assessment
LLM confidence != source confidence authority
LLM output != security status
```

## 11. Provenance estructural v1 y límite criptográfico

El baseline no posee todavía una raíz criptográfica fuerte de identidad/provenance para todos los componentes. Por tanto G1 prohíbe presentar como autenticada una identidad que solo esté declarada estructuralmente.

Una futura v1 podrá representar metadata equivalente a:

```text
assessment_kind
assessment_value
producer_role
producer_reference
assessed_at
policy_or_rule_reference
```

pero deberá distinguir:

```text
declared producer reference != cryptographically verified producer identity
```

G1 no autoriza PKI, firmas, nonce, replay protection ni Secure Context Manager criptográfico.

## 12. Frontera mínima candidata para G2

```text
Assessment
    ↓
Producer provenance present?
    ↓
Producer role allowed for this assessment kind?
    ↓
Attempted trust elevation within allowed scope?
    ↓
Deterministic provenance result
    ↓
Admission evaluation
```

G2 deberá preferir value objects inmutables, funciones puras, cero I/O, cero side effects, cero dependencias externas, determinismo y fail-closed.

## 13. Negative scenarios obligatorios para G2

- **AP-A1 — Payload cannot define producer:** el payload no puede declarar que su assessment proviene de un productor privilegiado.
- **AP-A2 — LLM cannot self-certify:** una salida del LLM no puede transformarse directamente en `ACCEPTABLE`, autoridad alta o clasificación no sensible.
- **AP-A3 — Unknown producer fails closed:** provenance desconocida no puede aumentar elegibilidad.
- **AP-A4 — Producer scope is dimensional:** autorización para sensitivity no concede permiso para security status o source authority.
- **AP-A5 — Negative evidence may reduce trust:** una señal gobernada de sospecha puede degradar trust según policy.
- **AP-A6 — Revocation cannot be overridden by confidence:** confidence alta no limpia `REVOKED` o `TAINTED`.
- **AP-A7 — Contradiction cannot silently clear itself:** la fuente contradictoria no puede eliminar el requisito de review.
- **AP-A8 — Declared identity is not cryptographic identity:** `producer_reference` no implica autenticación criptográfica.
- **AP-A9 — Assessment provenance does not authorize persistence:** provenance válida no convierte `ELIGIBLE` en permiso de storage.
- **AP-A10 — No authority inversion:** un productor downstream no puede modificar policy, Governance, SecurityContext, Kernel o permisos upstream mediante un assessment.
- **AP-A11 — Deterministic resolution:** mismos inputs deben producir el mismo resultado.
- **AP-A12 — No runtime side effects:** la validación no escribe archivos, no llama al LLM, no usa red y no persiste estado.

## 14. FULL 4R — G1

### Risk — PASS

Se evaluaron self-asserted trust, authority confusion, poisoning, producer spoofing, trust elevation por dimensión incorrecta, falsa identidad criptográfica y acoplamiento prematuro a Security o Kernel. Riesgo residual: provenance estructural v1 no equivale a identidad criptográficamente autenticada.

### Readability — PASS

Una sola responsabilidad: demostrar de dónde proviene un assessment y si ese productor puede producir esa dimensión. No se introduce `MemoryTrustManager`, `TrustEngine`, registry global ni taxonomía universal.

### Reliability — PASS

G2 deberá mantener determinismo, inputs inmutables, fail-closed para productores missing/unknown, producer scope por dimensión, payload incapaz de mutar provenance y ausencia de side effects.

### Resilience — PASS

Ambigüedad, conflicto, pérdida de provenance o productor no reconocido degradan hacia `HOLD` o `REJECT` según policy, nunca hacia mayor trust por defecto.

## 15. Compatibilidad con arquitectura y gobernanza

```text
Blueprint compliance: PASS
Cognitive Constitution: PASS
Governance Constitution: PASS
Kernel First: PASS
Human in Control: PASS
Runtime Independence: PASS
```

La unidad permanece dentro de la Memory Layer y preserva ADR-003: control/authority descendente; resultados/evidencia pueden retornar upstream sin convertirse en autoridad.

## 16. Stop conditions

Detener y volver al Owner si la solución requiere cambios en Kernel, Constitución, Blueprint, `SecurityContext`, PDP/PEP, permisos operativos, runtime wiring, Conversation wiring, persistencia, storage, retrieval, Knowledge, agents/tools, red, dependencia externa, PKI/identidad criptográfica, registry persistente, trust manager universal o taxonomía global no requerida por G3.

## 17. Precondiciones antes de implementación

```text
G2 candidate specification approved
Project Vault reconciled through governed Sync Agent flow
exact implementation baseline reverified
TDD scenarios defined
file/change budget defined
FULL 4R plan defined
Owner implementation authorization explicit
```

La aceptación temporal del drift en G0/G1 no satisface la precondición de reconciliación para implementación.

## 18. Resultado G1

```text
G1 RESULT: PASS
unit: Episodic Admission Assessment Provenance Boundary
risk class: 3
design accepted: true
implementation authorized: false
persistent memory authorized: false
retrieval authorized: false
knowledge authorized: false
sprint 7.12 authorized: false
rdd stage 2 authorized: false
vault reconciliation required before implementation: true
```

Próximo paso permitido únicamente mediante nueva autorización del Owner:

```text
G2 — Implementation Candidate Specification
```
