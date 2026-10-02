---
title: E3 Positive Qualification Consumption Trust Boundary V0 — G0/G1 Design
status: design-candidate
authority: evidence-only / no authority effect
as_of_date: 2026-10-02
source_baseline: f05d7019dbea062f5fa6a19a91bbc05a9936abe7
unit: E3 Positive Qualification Consumption Trust Boundary V0
gate: G0/G1
risk_class: 3
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_wiring_authorized: false
internal_interaction_wiring_authorized: false
support_sufficient_authorized: false
protected_finalization_authorized: false
rdd_stage_2_authorized: false
authority_effect: none
language: es
---

# E3 Positive Qualification Consumption Trust Boundary V0

## 1. Estado de autoridad

El Owner autorizó avanzar exclusivamente con G0/G1 de la unidad candidata:

```text
E3 Positive Qualification Consumption Trust Boundary V0
```

Esta autorización permite:

- relevar el baseline exacto;
- demostrar la necesidad de una frontera positiva separada;
- adaptar patrones ya existentes de Malāk;
- definir contratos conceptuales, bindings y fail-closed semantics;
- producir Malāk Alignment Matrix;
- realizar Writer prechecks de Critical Contract Hardening, Cuatro Preguntas,
  Design 4R y RDD Stage 1 Design Check;
- definir un RED futuro todavía NO autorizado;
- fijar stop conditions y Correction Budget candidato.

No autoriza:

- código productivo;
- tests RED/GREEN;
- cambios a `route_governed_support_evidence_v0`;
- cambios a `SecurityContext`, PDP, PEP o policy rules operativas;
- wiring hacia `InternalInteractionTestV0`;
- wiring hacia Conversation;
- `support_sufficient`;
- Protected Finalization;
- modelo/provider/runtime;
- store, registry o database;
- PKI, firmas, nonce o identidad criptográfica nueva;
- network verifier;
- RDD Stage 2;
- Sprint 7.12;
- Ready o Merge sin decisión humana.

Separaciones vigentes:

```text
Design != Implementation
G0/G1 PASS != RED authorization
Evidence != Authority
Qualification review != routing decision
Routing decision != execution authority
DETERMINISTIC != semantic truth
```

---

## 2. Baseline exacto

Baseline fuente congelado:

```text
repository  Aranwill/jarvis
branch      main
commit      f05d7019dbea062f5fa6a19a91bbc05a9936abe7
```

Ese baseline incorpora:

- PR #235 — E3 Governed Support Evidence Routing V0;
- PR #240 — Governed Qualification Consumption V0 fail-closed;
- PR #241 — reconciliación CURRENT_STATE post-#235;
- PR #239 — CLOSED / NOT MERGED / historical evidence only.

La lógica productiva vigente conserva:

```text
exactly one structurally eligible FULL oracle
+
caller-controlled coherent qualification
        ↓
INFERENTIAL / INFERENTIAL_RESIDUAL
```

El comentario productivo vigente declara que el happy path positivo
`DETERMINISTIC` queda diferido hasta una frontera de consumo separada.

---

## 3. Resultado formal G0

Problema mínimo:

```text
¿Cómo puede routing consumir una qualification externamente gobernada
sin aceptar como trust material algo fabricable íntegramente
por el mismo caller/request que solicita el routing?
```

Resultado:

```text
G0 RESULT               PASS
candidate disposition   ADAPT
risk class              3 / HIGH
critical contract       YES
independent blockers   3 on ae3fe7ed... / correction materialized
blocker closure         PENDING INDEPENDENT RE-REVIEW
implementation          NOT AUTHORIZED
authority_effect        none
```

`ADAPT` significa:

- reutilizar el patrón arquitectónico ya validado por Malāk;
- no copiar literalmente Memory;
- no crear un segundo sistema de autoridad;
- no tratar tipos Python, hashes o strings como prueba de externalidad;
- separar request-controlled material de composition-admitted material.

---

## 4. Necesidad demostrada por el baseline

PR #240 cerró correctamente el siguiente anti-pattern:

```text
caller qualification
+
caller review evidence
+
PASS/PASS
+
exact-looking bindings
        ↓
apparent trust
        ↓
DETERMINISTIC
```

Ese path queda prohibido.

La condición ya asentada es:

```text
caller-controlled coherent declarations
!= externally governed qualification
```

También:

```text
exact hashes/bindings
= integrity / reconciliation evidence

exact hashes/bindings
!= provenance authentication
!= permission
!= authority
```

Por tanto el siguiente problema no es agregar más campos al request.
El problema es crear una frontera cuya fuente de trust material no sea el request.

---

## 5. Precedentes internos de Malāk

### 5.1 Episodic Admission Assessment Producer Authorization

PR #85 ya separó:

```text
assessment value
!= structural provenance
!= producer identity
!= producer authorization
!= admission decision
!= authority
```

También congeló:

```text
SecurityContext authenticated
!= cryptographic identity
```

Y reutilizó el Security Control Plane existente en vez de crear:

```text
MemoryTrustManager
ProducerAuthorityRegistry
MemoryPermissionEngine
```

### 5.2 Governed Input Projection

PR #88 materializó el patrón:

```text
raw assessment
+
provenance
+
producer authorization
        ↓
governed projection
READY | HOLD | DENIED
```

La projection no equivale a la decisión de dominio.

### 5.3 Governed Projection Consumption

PR #92 materializó:

```text
READY projection
        ↓
validate consumption bindings
        ↓
ephemeral effective view
        ↓
existing policy
```

Y preservó:

```text
Projection READY != Admission ELIGIBLE
Admission Decision != Persistence Authorization
Evidence != Authority
```

### 5.4 Disposición

El patrón es aplicable por analogía arquitectónica:

```text
qualification material
+
review evidence
+
governed producer/operation authorization
        ↓
governed review admission/projection
        ↓
bounded consumption context
        ↓
routing
```

No se reutilizan contratos Memory ni semánticas de persistencia.

---

## 6. Malāk Alignment Matrix

| source | authority class | invariant / intent | disposition | efecto de diseño |
|---|---|---|---|---|
| Cognitive Constitution | normative protected | Evidence != Authority; reliance proporcional al riesgo | ADOPT | missing/unverifiable guarantee no habilita DETERMINISTIC |
| Governance Constitution | normative protected | Human in Control para decisiones críticas | ADOPT | Owner conserva admisión/Ready/Merge |
| Blueprint | architecture | Kernel First; Human in Control; Zero Trust | ADOPT | Kernel delta 0 |
| SECURITY.md | protected security policy | Zero Trust, fail-closed, no confianza implícita | ADOPT | request data no puede auto-certificarse |
| Architecture Quality Gates | architecture | Kernel pequeño; critical decisions auditables/reversibles | ADOPT | boundary fuera del Kernel |
| Engineering Method | development contract | agentes/reviews no amplían su propia autoridad | ADOPT | review != authority; independent gates |
| Construction Protocol §5.5 | development contract | secuencia crítica no sustituible | ADOPT | no RED antes de pre-RED PASS + Owner |
| Evidence Manifest v1 | development contract | exact candidate binding; producer/validator provenance != permission | ADAPT | candidate/material drift invalida admission afectada |
| PR #85 | integrated precedent | producer authorization separada de provenance | ADAPT | reutilizar Security Control Plane, no Memory contracts |
| PR #88 | integrated precedent | governed projection | ADAPT | raw review no llega directamente a routing |
| PR #92 | integrated precedent | governed consumption | ADAPT | projection READY no equivale a routing DETERMINISTIC |
| PR #240 | active integrated contract | caller-controlled review never sufficient | ADOPT | request no porta positive trust credential |

Nada de esta matriz concede autorización de implementación.

---

## 7. Threat model G0

### 7.1 Amenaza primaria

```text
request/caller can construct:
- qualification
- review-shaped object
- PASS strings
- matching actor IDs
- matching hashes
        ↓
false-positive DETERMINISTIC
```

### 7.2 Amenazas secundarias

- stale review tras cambio de candidate;
- review ligado a bundle distinto;
- permission scope incorrecto;
- authorization decision ligada a otra operación;
- duplicate admission para la misma qualification;
- ambiguous FULL oracle;
- trust material suministrado por el request;
- bypass directo al routing free function;
- reinterpretar RDD-M1 como runtime credential;
- convertir `authenticated=True` en identidad fuerte;
- copiar evidencia histórica dentro del repo y tratarla como review activa.

### 7.3 No amenaza resuelta por V0

V0 NO demuestra identidad criptográfica humana.

Riesgo residual vigente:

```text
SecurityContext.authenticated == current governed trust assertion
SecurityContext.authenticated != cryptographic proof
```

Si el happy path exige identidad criptográfica fuerte para ser correcto:

```text
STOP
→ scope escalation
→ identity / provenance architecture
```

---

## 8. Alternativas evaluadas

### A — agregar `qualification_review_evidence` al routing request

```text
request
+ qualification
+ review evidence
→ route(...)
```

Disposición:

```text
REJECT
```

Motivo: reproduce exactamente el problema cerrado por #240.

### B — boolean/token/hash de verificación

Ejemplos:

```text
verified=true
review_token="..."
digest matches
qualifier_subject_id != producer_subject_id
```

Disposición:

```text
REJECT
```

Motivo: integridad o declaración no demuestran provenance/authority.

### C — nuevo trust registry/store

Disposición:

```text
DEFER / STOP IF REQUIRED
```

No existe necesidad demostrada todavía.

### D — reutilizar RDD-M1 como credential runtime

Disposición:

```text
REJECT
```

RDD-M1 es evidencia de desarrollo y candidate conformance, no permission ni runtime credential.

### E — usar sólo SecurityContext/PDP y declarar externalidad resuelta

Disposición:

```text
REJECT AS CLAIM
ADAPT AS CONTROL
```

El Security Control Plane aporta autorización gobernada, exact permission matching,
operation binding y fail-closed behavior, pero el baseline no posee raíz
criptográfica fuerte de identidad/provenance.

Por tanto:

```text
PDP authorization
!= cryptographic externality proof
```

### F — composition-admitted trust material + existing Security Control Plane

Disposición:

```text
ADOPT FOR G1 DESIGN
```

Flujo:

```text
externally reviewed qualification evidence
        ↓
Owner/governed admission at composition boundary
        ↓
exact operation binding
        ↓
existing Security Control Plane
        ↓
governed qualification admission/projection
        ↓
immutable consumption boundary
        ↓
routing request
```

Propiedad central:

```text
request supplies request material
composition supplies admitted trust material
request cannot supply/override admitted trust material
```

---

## 9. Decisión G1-D1 — Composition Admission Seam exacta

La positive qualification evidence no será un parámetro model-facing ni
request-facing.

Prohibido:

```text
route(..., qualification_review_evidence=request.review)
route(..., authorization_decision=request.decision)
route(..., ready_admission=request.admission)
```

### 9.1 Actores y control de entrada

V0 congela dos superficies distintas:

```text
REQUEST SURFACE
- routing subject
- bounded oracle contracts
- declared evidence completeness
- scope-expansion signal

COMPOSITION / GOVERNED CONFIGURATION SURFACE
- raw qualification review material selected/admitted by Owner/governed configuration
- SecurityContext supplied by governed application configuration
- configured PolicyDecisionPoint
- configured SecurityContextValidator / Clock
```

El actor/request que solicita routing:

- no recibe referencia a la factory de admission;
- no puede aportar ni sustituir el `SecurityContext` de admission;
- no puede aportar el `AuthorizationRequest`;
- no puede aportar el `AuthorizationDecision`;
- no puede aportar `HumanConfirmationEvidence` a la llamada request-facing;
- no puede aportar una `GovernedQualificationReviewAdmissionV0`;
- no puede reemplazar la instancia de `GovernedQualificationConsumptionBoundaryV0`
  ya compuesta.

La distinción es una propiedad de la interfaz y de ownership de objetos, no una
afirmación criptográfica sobre procesos Python.

### 9.2 Operación gobernada de admisión

PermissionScope V0 candidato y congelado para RED:

```text
resource = "engineering.qualification_review_consumption"
action   = "admit"
```

La operación positiva se realiza exclusivamente en la seam de composition:

```text
governed configuration / Owner-selected review material
        ↓
derive canonical review-material digest
        ↓
derive AuthorizationOperationBinding internally
        ↓
construct AuthorizationRequest internally
        ↓
configured PDP.decide(request [, confirmation when policy requires])
        ↓
receive AuthorizationDecision from configured PDP
        ↓
validate exact request/decision/binding/permission/context coherence
        ↓
GovernedQualificationReviewAdmissionV0
READY | HOLD | DENIED
        ↓
construct immutable GovernedQualificationConsumptionBoundaryV0
```

Ni el `AuthorizationOperationBinding` ni la decisión positiva se aceptan como
datos terminales proporcionados por el routing request.

### 9.3 Obtención y aplicación de la decisión

La admission primitive/factory es responsable de:

1. derivar el binding desde el material exacto que está siendo admitido;
2. construir el `AuthorizationRequest` con el PermissionScope exacto;
3. invocar el PDP configurado;
4. recibir directamente su `AuthorizationDecision`;
5. comprobar que `request_id`, permission, operation binding y SecurityContext
   corresponden a la operación construida;
6. materializar READY sólo si la decisión recibida permite esa operación y todas
   las dimensiones de review obligatorias son PASS.

Prohibido:

```text
caller creates AuthorizationDecision(allowed=True)
→ admission accepts it as proof
```

### 9.4 Evento Human-in-Control / gobernado

Para V0, la entrada del review material a la configuration surface es una acción
gobernada separada del request y bajo control del Owner/proceso expresamente
autorizado.

Si la policy configurada exige confirmación humana, se reutiliza el mecanismo
existente y su exact operation binding. Si la policy permite la operación sin
confirmación adicional, esa decisión del PDP no elimina ni reemplaza la autoridad
humana terminal sobre el proceso de desarrollo, Ready o Merge.

```text
Owner/governed configuration admission
!= PR Ready
!= Merge
!= semantic truth
```

### 9.5 Propiedad de no sustitución

Después de composition:

```text
request
        ↓
existing boundary instance
        ↓
route(request material, oracles)
```

No existe en la API request-facing un setter, factory argument, admission object,
review object, decision object o configuration hook capaz de reemplazar el
admitted set.

Un test que sólo construya tipos equivalentes no satisface esta propiedad.
El negativo debe intentar inyección/sustitución a través de la misma seam pública
que usa el positivo y demostrar que no puede producir una admission READY.

La creación de la boundary pertenece a composition/configuration, no al request.

---

## 10. Decisión G1-D2 — no segundo sistema de autoridad

No crear:

```text
QualificationTrustManager
QualificationReviewerRegistry
EngineeringPermissionEngine
TrustedReviewerList
```

Se adapta el Security Control Plane existente:

```text
SecurityContext
PermissionScope
AuthorizationOperationBinding
AuthorizationRequest
AuthorizationDecision
StaticPolicyDecisionPoint
```

El diseño no cambia sus contratos en G1.

---

## 11. Decisión G1-D3 — operation binding exacto

La autorización de admitir review material debe estar ligada a la operación exacta.

Namespace candidato:

```text
engineering.qualification_review_consumption
```

Binding version candidato:

```text
v0
```

El digest conceptual debe cubrir de forma canónica al menos:

```text
repository
routing_baseline_commit
qualification_identity
qualification_evidence_digest
oracle_id
oracle_version
oracle_content_digest
relation_id
evaluation_question_identity
input_contract_identity
output_contract_identity
coverage_claim
oracle_producer_subject_id
qualification_reviewer_subject_id
reviewed_obligation_catalog_digest
structural_validator_result
catalog_completeness_result
independence_review_result
verification_material_review_result
qualification_review_result
evidence_references
authority_effect
```

Regla:

```text
AuthorizationRequest.operation_binding
==
AuthorizationDecision.operation_binding
==
canonical admission operation binding
```

Mismatch:

```text
DENIED / no DETERMINISTIC
```

---

## 12. Decisión G1-D4 — Human in Control

Por riesgo HIGH y por tratarse de trust material que puede abrir
`DETERMINISTIC`, la admisión del review material ocurre exclusivamente desde
la surface gobernada de composition/configuration. El Owner o proceso
explícitamente autorizado controla qué material entra a esa surface.

La policy configurada puede además exigir confirmación humana explícita mediante
el mecanismo existente. Esa confirmación es un control de autorización de la
operación exacta; no es el único elemento que separa request de configuration.

Separación:

```text
HumanConfirmationEvidence
!= qualification review
!= semantic truth
!= permanent permission
```

La confirmación, cuando la policy la requiera:

- debe estar ligada al request de autorización exacto;
- debe conservar el exact `operation_binding`;
- no amplía permission scope;
- no modifica una decisión anterior;
- no autoriza Ready/Merge;
- no constituye una garantía criptográfica nueva.

La policy rule operativa concreta NO se crea en G1.

---

## 13. Decisión G1-D5 — review evidence contract

Nombre candidato:

```text
GovernedQualificationReviewEvidenceV0
```

Campos mínimos candidatos:

```text
repository
evaluated_candidate_commit
qualification_identity
qualification_bundle_digest
reviewed_oracle_id
reviewed_oracle_version
reviewed_oracle_content_digest
reviewed_relation_id
reviewed_evaluation_question_identity
reviewed_input_contract_identity
reviewed_output_contract_identity
reviewed_coverage_claim
reviewed_oracle_producer_subject_id
reviewed_obligation_catalog_digest
structural_validator_result
catalog_completeness_result
independence_review_result
verification_material_review_result
qualification_review_result
reviewer_subject_id
evidence_references
authority_effect
```

Terminal review dimensions:

```text
PASS | FAIL | INCONCLUSIVE
```

Regla:

```text
any required FAIL/INCONCLUSIVE
→ not admissible for positive deterministic consumption
```

El objeto raw es evidence-shaped data.
Su mera construcción NO habilita routing.

---

## 14. Decisión G1-D6 — admission/projection contract

Nombre candidato:

```text
GovernedQualificationReviewAdmissionV0
```

Outcome candidato:

```text
READY | HOLD | DENIED
```

Responsabilidad:

- validar schema/bounds;
- validar exact qualification/review binding;
- validar candidate/material binding;
- validar permission scope;
- validar request/decision coherence;
- validar exact operation binding;
- derivar internamente el canonical review-material digest;
- derivar internamente el `AuthorizationOperationBinding`;
- construir internamente el `AuthorizationRequest`;
- invocar el PDP configurado y recibir directamente su decisión;
- validar temporal coherence al momento de admission;
- validar policy decision obtenida del PDP configurado;
- retener el contexto temporal mínimo requerido para revalidación en consumo;
- rechazar authority effect distinto de `none`;
- producir una projection/admission inmutable.

No responsabilidad:

- decidir routing;
- demostrar semantic truth;
- autenticar criptográficamente al reviewer;
- ejecutar red;
- consultar store;
- ejecutar modelo;
- autorizar cambios;
- aceptar un `AuthorizationDecision` caller-supplied como evidencia de origen;
- aceptar una admission READY caller-supplied como trust credential.

---

## 15. Decisión G1-D7 — consumption boundary y vigencia

Nombre candidato:

```text
GovernedQualificationConsumptionBoundaryV0
```

La boundary se crea desde composition con admissions materializadas y bounded.

Propiedades:

```text
immutable admitted set
bounded cardinality
no request mutation
no runtime network
no store lookup
no global registry
no hidden mutable cache
authority_effect = none
```

### 15.1 Lifetime V0

V0 adopta la semántica conservadora:

```text
positive admission lifetime
<= lifetime of the SecurityContext that authorized its admission
```

Una admission READY retiene, como mínimo verificable:

```text
authorization_context_id
authorization_subject_id
authorization_context_issued_at
authorization_context_expires_at
admission_evaluated_at
authorization_request_id
authorization_operation_binding
```

La admission NO se convierte en snapshot durable que sobreviva automáticamente
a la expiración del contexto de autorización.

### 15.2 Clock y revalidación en consumo

La boundary recibe en composition un `Clock` gobernado/injectable compatible con
el modelo temporal existente. El request-facing route call no acepta
`evaluated_at`, `now` ni otro valor temporal controlado por el caller.

En cada consumo positivo candidato:

```text
consume_at = boundary.clock.now()

authorization_context_issued_at
<= admission_evaluated_at
<= consume_at
< authorization_context_expires_at
```

Si el contexto expiró entre creation y consumption:

```text
READY at creation
        ↓ time
expired at consumption
        ↓
ADMISSION_STALE
        ↓
no DETERMINISTIC
```

No se introduce store, revocation registry ni lifetime persistente nuevo.

### 15.3 API request-facing

La boundary expone conceptualmente:

```text
route(
    routing subject,
    bounded oracle contracts
)
→ GovernedSupportEvidenceRoutingV0
```

No expone:

```text
qualification_review_evidence
authorization_decision
human_confirmation
trusted_reviewer
verified flag
admission
consume_at
clock
```

como parámetros del request-facing route call.

---

## 16. Decisión G1-D8 — relación con routing existente

`route_governed_support_evidence_v0` conserva por defecto su semántica
fail-closed actual.

No debe convertirse en una función que reciba caller-supplied trust material.

Dirección candidata:

```text
existing structural routing checks
        ↓
exactly one FULL structurally eligible oracle?
        ├── no  → existing INFERENTIAL / INSUFFICIENT / error reason
        └── yes
              ↓
boundary has exactly one READY admitted review
bound to that exact qualification + subject?
        ├── no  → INFERENTIAL
        └── yes → DETERMINISTIC
```

Implementation note todavía no congelada:

- evitar duplicar P01–P09;
- preferir extraer/reutilizar una primitive interna pura de selección estructural;
- no copiar la lógica de `route_governed_support_evidence_v0`;
- cualquier refactor debe conservar la API pública y los resultados fail-closed.

Si no puede evitarse duplicación material o ampliación de API pública:

```text
STOP
→ scope review
```

---

## 17. Candidate binding

Toda admission positiva debe quedar ligada a:

```text
repository
routing baseline commit
qualification identity
qualification evidence digest
oracle content identity
relation identity
evaluation question identity
input/output contract identities
obligation catalog digest
review material digest
authorization operation binding
```

Cambio material:

```text
A → B
        ↓
admission bound to A becomes stale
        ↓
no DETERMINISTIC
        ↓
affected evidence must be revalidated
```

No hay herencia por igualdad parcial.

---

## 18. External review y process evidence

La fuente externa puede seguir siendo, según proceso gobernado:

- PR review ligado al SHA exacto;
- validator artifact ligado al SHA exacto;
- informe independiente externo ligado al SHA exacto.

Pero:

```text
evidence reference string
!= authenticated origin
```

La admisión V0 registra y liga esa evidencia.
No pretende convertir referencias textuales en firmas.

El Human-in-Control admission step es parte del trust model V0.

---

## 19. Fail-closed semantics

Como mínimo:

```text
missing admission
→ INFERENTIAL

raw review supplied by request
→ ignored/rejected; no DETERMINISTIC

wrong repository
→ no DETERMINISTIC

wrong candidate
→ no DETERMINISTIC

wrong qualification identity
→ no DETERMINISTIC

wrong qualification digest
→ no DETERMINISTIC

wrong oracle content identity
→ no DETERMINISTIC

wrong relation/question identity
→ no DETERMINISTIC

wrong contract identity
→ no DETERMINISTIC

wrong obligation catalog digest
→ no DETERMINISTIC

review FAIL
→ no DETERMINISTIC

review INCONCLUSIVE
→ no DETERMINISTIC

authorization missing
→ no DETERMINISTIC

authorization denied
→ no DETERMINISTIC

permission mismatch
→ no DETERMINISTIC

operation binding mismatch
→ no DETERMINISTIC

stale temporal/security context at admission
→ no DETERMINISTIC

context valid at admission but expired before consumption
→ ADMISSION_STALE
→ no DETERMINISTIC

duplicate READY admissions
→ no DETERMINISTIC

ambiguous FULL oracle
→ existing ORACLE_AMBIGUOUS

exact one FULL + exact READY admission
→ candidate DETERMINISTIC happy path
```

---

## 20. No silent downgrade de findings

Deben distinguirse:

```text
STRUCTURAL INVALID
AUTHORIZATION DENIED
ADMISSION HOLD
ADMISSION DENIED
ADMISSION MISSING
ADMISSION STALE
ADMISSION AMBIGUOUS
INFERENTIAL RESIDUAL
EVIDENCE INSUFFICIENT
```

No colapsar todo a un `False` o `verified=False`.

Reason codes exactos se congelarán antes de RED.

---

## 21. Resource / side-effect boundary

Target V0:

```text
network calls                 0
new external dependencies     0
database                      0
store                         0
registry                      0
PKI/signatures                0
Kernel delta                  0
Planner delta                 0
model/provider delta          0
Conversation delta            0
InternalInteraction wiring    0
support_sufficient delta      0
Protected Finalization delta  0
RDD Stage 2 delta             0
authority delta               0
```

La composition root puede ser parte del implementation scope futuro sólo si
es necesaria para demostrar separación request/composition.

Eso no autoriza wiring hacia un flujo vivo.

---

## 22. API / trust boundary rule

Un test positivo que construya todos los objetos desde el mismo request fixture
NO demuestra la propiedad requerida.

El RED/GREEN futuro debe distinguir al menos:

```text
REQUEST MATERIAL
vs
COMPOSITION-ADMITTED MATERIAL
```

La API request-facing no debe tener campo/parámetro para inyectar el material
admitido, su AuthorizationRequest/Decision, su SecurityContext, su Clock o la
factory/configuration que produce la boundary.

Si la implementación sólo cambia nombres pero sigue permitiendo:

```text
caller creates ELIGIBLE object
→ passes object directly
→ DETERMINISTIC
```

el diseño debe considerarse FAIL.

---

## 23. Relación con Internal Interaction Test V0

Fuera de scope de esta unidad:

```text
/self-review test-v0
InternalInteractionTestV0Harness
CLI routing wiring
```

Secuencia esperada:

```text
this trust boundary
        ↓
independent closure / merge
        ↓
separate integration/wiring gate
        ↓
InternalInteraction E3 routing path
        ↓
new runtime admission/preflight
        ↓
/self-review test-v0
```

No mezclar trust-boundary correctness con live-flow integration.

---

## 24. Future RED — NOT AUTHORIZED

IDs candidatos:

```text
PQCTB-R01 caller-only FULL qualification → no DETERMINISTIC
PQCTB-R02 caller-supplied review object → no DETERMINISTIC
PQCTB-R03 request cannot supply/replace admission factory, SecurityContext, PDP decision or boundary
PQCTB-R04 missing composition admission → INFERENTIAL
PQCTB-R05 wrong repository → no DETERMINISTIC
PQCTB-R06 wrong candidate → no DETERMINISTIC
PQCTB-R07 wrong qualification identity/digest → no DETERMINISTIC
PQCTB-R08 wrong oracle identity/content digest → no DETERMINISTIC
PQCTB-R09 wrong relation/question/contract binding → no DETERMINISTIC
PQCTB-R10 wrong catalog digest → no DETERMINISTIC
PQCTB-R11 catalog_completeness_result FAIL/INCONCLUSIVE with all other material PASS → no READY / no DETERMINISTIC
PQCTB-R12 structural review FAIL/INCONCLUSIVE → no DETERMINISTIC
PQCTB-R13 independence review FAIL/INCONCLUSIVE → no DETERMINISTIC
PQCTB-R14 verification review FAIL/INCONCLUSIVE → no DETERMINISTIC
PQCTB-R15 qualification review FAIL/INCONCLUSIVE → no DETERMINISTIC
PQCTB-R16 missing authorization → no DETERMINISTIC
PQCTB-R17 denied authorization → no DETERMINISTIC
PQCTB-R18 permission mismatch → no DETERMINISTIC
PQCTB-R19 operation binding mismatch → no DETERMINISTIC
PQCTB-R20 context invalid/stale at admission → no DETERMINISTIC
PQCTB-R21 context valid at admission then expired before consumption → ADMISSION_STALE / no DETERMINISTIC
PQCTB-R22 duplicate READY admissions → no DETERMINISTIC
PQCTB-R23 ambiguous FULL oracles → ORACLE_AMBIGUOUS
PQCTB-R24 governed configuration + configured PDP + one exact READY + one exact FULL → DETERMINISTIC
PQCTB-R25 positive route reports selected exact oracle_id
PQCTB-R26 authority_effect != none rejected
PQCTB-R27 no Kernel/Planner/model/provider/network/store/registry/Stage2 effect
PQCTB-R28 route structural semantics P01–P09 remain regression-equivalent
PQCTB-R29 request-facing signature exposes no review/admission/decision/context/clock trust input
PQCTB-R30 raw RDD manifest/review references cannot act as runtime credential
PQCTB-R31 material/candidate change invalidates prior admission```

Estos tests son design candidates; no están autorizados.

---

## 25. E2E equivalente futuro

Aunque esta unidad permanezca aislada de runtime, §5.5 exige no omitir E2E.

E2E equivalente mínimo futuro:

```text
Owner/governed configuration selects raw review material
        ↓
admission factory derives exact operation binding
        ↓
admission factory constructs AuthorizationRequest
        ↓
configured PDP returns AuthorizationDecision
        ↓
admission validates exact decision/binding/context/review dimensions
        ↓
READY admission
        ↓
composition constructs immutable consumption boundary with governed Clock
        ↓
request supplies only routing subject + exact FULL oracle
        ↓
boundary revalidates admission lifetime at consume time
        ↓
DETERMINISTIC
```

Negative E2E sobre la MISMA seam:

```text
request attempts to supply/replace:
review material OR
AuthorizationDecision OR
SecurityContext OR
READY admission OR
consumption boundary
        ↓
no governed admission replacement path
        ↓
missing/non-matching composition admission
        ↓
INFERENTIAL / blocked
```

Temporal negative E2E:

```text
valid context
→ READY admission
→ advance governed Clock beyond context.expires_at
→ consume same immutable boundary
→ ADMISSION_STALE
→ no DETERMINISTIC
```

Debe ejecutarse sobre el candidate exacto. El positivo y el negativo deben
atravesar la misma composition admission seam; fixtures no pueden fabricar
`AuthorizationDecision(allowed=True)` o READY como sustituto de la invocación
del PDP configurado.

---

## 26. Correction Budget candidato

Sólo aplicable si pre-RED gates pasan y el Owner autoriza RED.

Budget inicial candidato:

```text
preferred production files:
  - src/malak/capabilities/_engineering_analysis.py
  - one new bounded module under src/malak/capabilities/ OR src/malak/core/
  - src/malak/app/composition.py ONLY if required to prove request/composition separation

preferred test files:
  - one new focused test module
  - existing E3 routing tests only for regression/causal coverage

new dependencies                 0
Kernel files                     0
Planner files                    0
runtime/provider files           0
CLI/InternalInteraction files    0
Security contract changes        0
PDP/PEP semantic changes          0
policy rule activation           separate explicit decision
Clock                             existing governed primitive only
max bounded correction rounds    2
```

Si se necesita:

- modificar `SecurityContext`;
- cambiar PDP/PEP semantics;
- crear store/registry;
- agregar PKI/signatures;
- introducir network verification;
- tocar Kernel/Planner;
- ampliar a `support_sufficient`;
- cablear InternalInteraction;

entonces:

```text
STOP
→ scope review
```

---

## 27. Cuatro Preguntas de Ley — Writer precheck

### Blueprint

- Kernel delta 0.
- Boundary permanece fuera del Kernel.
- Capability/Engineering responsibility localizada.
- Writer candidate: PASS.

### Cognitive Constitution

- Evidence != Authority preservado.
- Exact material binding antes de reliance.
- Missing guarantee no se interpreta como satisfecha.
- Writer candidate: PASS.

### Governance Constitution

- Human in Control preservado.
- Admission/Ready/Merge siguen humanos.
- No self-authorization del evaluator.
- Writer candidate: PASS.

### Kernel complexity

- No manager/registry/framework nuevo.
- No Kernel delta.
- Composition boundary sólo si es causalmente necesaria.
- Writer candidate: PASS.

Terminal:

```text
PENDING INDEPENDENT FOUR QUESTIONS
```

---

## 28. Critical Contract Hardening — Writer precheck

Ambigüedades cerradas en Writer pass:

1. `authenticated=True` NO significa identidad criptográfica.
2. PDP decision NO demuestra semantic truth.
3. Review evidence raw NO habilita routing.
4. Admission READY NO equivale a routing decision.
5. DETERMINISTIC NO equivale a authority.
6. Trust material NO llega desde request arguments.
7. RDD-M1 NO es credential runtime.
8. Candidate/material drift invalida admission afectada.
9. Duplicate/ambiguous admission falla cerrado.
10. Positive path requiere exact one FULL + exact one READY admission.
11. InternalInteraction wiring queda separado.
12. Security architecture escalation produce STOP.
13. Composition, no request, construye AuthorizationRequest y obtiene directamente la decisión del PDP configurado.
14. PermissionScope de admission queda congelado a engineering.qualification_review_consumption / admit.
15. Request no puede suministrar/sustituir SecurityContext, AuthorizationDecision, admission, Clock o boundary.
16. Admission positiva no sobrevive automáticamente a SecurityContext.expires_at.
17. Consumption revalida lifetime mediante Clock gobernado no controlado por request.
18. catalog_completeness FAIL/INCONCLUSIVE bloquea READY aun con digest correcto.

Writer precheck:

```text
CANDIDATE PASS
```

Terminal:

```text
PENDING INDEPENDENT CRITICAL CONTRACT HARDENING
```

---

## 29. Design 4R — Writer precheck

### Risk

Riesgo dominante:

```text
false-positive DETERMINISTIC by self-certification
```

Mitigación:

- request/composition separation;
- exact operation binding;
- existing Security Control Plane;
- fail-closed admission;
- exact candidate/material binding;
- human governance.

Writer candidate: PASS.

### Readability

Responsabilidades separadas:

```text
review evidence
→ admission/projection
→ consumption boundary
→ routing
```

Sin manager universal.

Writer candidate: PASS.

### Reliability

- bounded immutable material;
- exact identities;
- deterministic matching;
- no network/store;
- stale evidence invalidation;
- configured-PDP decision acquisition at composition seam;
- governed Clock revalidation on every positive consumption;
- catalog completeness causal rejection;
- regression preservation P01–P09.

Writer candidate: PASS.

### Resilience

- missing/invalid/stale/duplicate/denied → no DETERMINISTIC;
- valid-at-admission but expired-at-consumption → ADMISSION_STALE;
- catalog completeness FAIL/INCONCLUSIVE → no READY;
- request-side substitution attempts → no positive admission replacement;
- no fallback que convierta ausencia de trust en positive route;
- rollback local y sin migraciones.

Writer candidate: PASS.

Terminal:

```text
PENDING INDEPENDENT DESIGN 4R
```

---

## 30. RDD Stage 1 Design Check — Writer precheck

El diseño preserva:

- exact baseline/candidate strategy;
- candidate-bound evidence;
- explicit risk class;
- external/process provenance separada de permission;
- Writer / Reviewer / Validator / Authority separation;
- PASS | FAIL | INCONCLUSIVE;
- INCONCLUSIVE != PASS;
- affected evidence invalidation after candidate change;
- bounded correction;
- independent validation;
- E2E equivalent;
- authority_effect = none;
- RDD Stage 2 NOT AUTHORIZED.

Además:

```text
RDD evidence
!= runtime trust credential
```

Writer precheck:

```text
CANDIDATE PASS
```

Terminal:

```text
PENDING INDEPENDENT RDD STAGE 1 DESIGN CHECK
```

---

## 31. Stop conditions

STOP inmediato si el pre-RED review demuestra cualquiera de estas necesidades:

```text
cryptographic identity required for correctness
persistent trust store required
reviewer registry required
network verifier required
new authority service required
SecurityContext contract change required
PDP semantic change required
Kernel/Planner participation required
support_sufficient coupling required
InternalInteraction wiring required in same unit
duplicated routing P01–P09 unavoidable
request can still inject positive trust material
governed decision cannot be obtained/applied without accepting caller-supplied AuthorizationDecision
admission lifetime cannot be revalidated with existing governed Clock primitive
```

Cada STOP exige scope review separado.

---

## 32. Rollback

G0/G1 candidate:

```text
production delta   0
test delta         0
runtime delta      0
authority delta    0
rollback           revert design-record commit
```

Una implementación futura deberá ser reversible sin migración persistente.

---

## 33. Estado del gate

```text
Owner authorization for G0/G1                  YES
baseline                                        f05d7019dbea062f5fa6a19a91bbc05a9936abe7
G0 / admission                                  WRITER PASS
G1 design                                       DESIGN CANDIDATE
Malāk Alignment Matrix                          MATERIALIZED
Critical Contract Hardening                     WRITER CANDIDATE PASS
Four Questions                                  WRITER CANDIDATE PASS
Design 4R                                       WRITER CANDIDATE PASS
RDD Stage 1 Design Check                        WRITER CANDIDATE PASS

Independent review on ae3fe7ed...               FAIL / HISTORICAL
F242-PRED-01 bounded design correction           MATERIALIZED / PENDING RE-REVIEW
F242-PRED-02 bounded design correction           MATERIALIZED / PENDING RE-REVIEW
F242-PRED-03 bounded design correction           MATERIALIZED / PENDING RE-REVIEW
Independent Critical Contract Hardening         PENDING ON NEW CANDIDATE
Independent Four Questions                      PENDING ON NEW CANDIDATE
Independent Design 4R                           PENDING ON NEW CANDIDATE
Independent RDD Stage 1 Design Check            PENDING ON NEW CANDIDATE
PRE-RED ADMISSION                               PENDING

RED                                              NOT AUTHORIZED
GREEN                                            NOT AUTHORIZED
InternalInteraction wiring                       NOT AUTHORIZED
support_sufficient                               NOT AUTHORIZED
Protected Finalization                           NOT AUTHORIZED
RDD Stage 2                                      NOT AUTHORIZED
Ready                                            OWNER ONLY
Merge                                            OWNER ONLY
authority_effect                                 none
```

---
## 34. Bounded correction — independent review F242-PRED-01/02/03

El independent Pre-RED Design Review del candidate:

```text
ae3fe7ed7b68462f04c5ac676e9a5e11dc2d383f
```

emitió:

```text
PRE-RED DESIGN REVIEW = FAIL
```

con tres findings bloqueantes:

```text
F242-PRED-01  composition admission seam / configured PDP enforcement
F242-PRED-02  admission lifetime / temporal revalidation
F242-PRED-03  catalog completeness causal RED coverage
```

Esta revisión permanece evidencia histórica ligada exclusivamente a
`ae3fe7ed...`.

La bounded correction de este design record:

- congela la composition admission seam;
- define qué controla request y qué controla governed configuration;
- congela PermissionScope `engineering.qualification_review_consumption/admit`;
- exige derivación interna del operation binding;
- exige que admission invoque el PDP configurado y reciba directamente su decisión;
- prohíbe caller-supplied AuthorizationDecision/READY como prueba positiva;
- congela lifetime máximo al SecurityContext de autorización;
- exige revalidación en consumo mediante Clock gobernado no request-controlled;
- agrega cobertura causal de catalog completeness FAIL/INCONCLUSIVE;
- endurece Security contract changes y PDP/PEP semantic changes a límite 0.

```text
finding closure
!= writer assertion
```

Por tanto:

```text
F242-PRED-01 = CORRECTION MATERIALIZED / PENDING INDEPENDENT RE-REVIEW
F242-PRED-02 = CORRECTION MATERIALIZED / PENDING INDEPENDENT RE-REVIEW
F242-PRED-03 = CORRECTION MATERIALIZED / PENDING INDEPENDENT RE-REVIEW
```

No se autoriza RED por esta corrección.

---

## 35. Siguiente transición lícita

```text
independent read-only pre-RED review
        ↓
Critical Contract Hardening
        ↓
Four Questions
        ↓
Design 4R
        ↓
RDD Stage 1 Design Check
        ↓
PRE-RED ADMISSION
        ↓
Owner decision on RED
```

No se materializa ningún RED antes de esa decisión humana.
