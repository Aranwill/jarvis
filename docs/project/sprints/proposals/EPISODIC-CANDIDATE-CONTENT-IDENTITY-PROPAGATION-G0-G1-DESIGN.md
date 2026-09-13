---
title: Episodic Candidate Content Identity Propagation & Binding — G0/G1 Design Record
status: g1_design_review_hardened
authority: owner-authorized design analysis
as_of_date: 2026-09-12
unit: Episodic Candidate Content Identity Propagation & Binding Boundary
gate: G1
source_baseline: 0466e18075fd6bce6243e03f701a377fd34469dd
vault_reconciliation_status_at_start: pass
vault_head_at_start: 62c56b06ffc4e4172e574a3af116c7be1605e55e
risk_class: 3
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
g0_authorized: true
g1_authorized: true
g2_authorized: false
implementation_authorized: false
persistent_memory_authorized: false
persistence_authorization_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
runtime_wiring_authorized: false
kernel_change_authorized: false
security_control_plane_change_authorized: false
sprint_7_12_authorized: false
compromise_aware_binding_required: true
verification_transitivity_allowed: false
self_attestation_allowed: false
candidate_id_fallback_allowed: false
language: es
---

# Episodic Candidate Content Identity Propagation & Binding — G0/G1 Design Record

## 1. Estado de autoridad

El Owner autorizó avanzar exclusivamente con **G0/G1 de diseño** para la unidad:

```text
Episodic Candidate Content Identity Propagation & Binding Boundary
```

La autorización parte del cierre completo de `Episodic Candidate Content Identity G2`,
con implementación integrada en `main`, validación post-merge y reconciliación del
Project Vault sin drift.

Esta unidad responde solamente:

> ¿cómo debe propagarse la identidad exacta del contenido de un
> `EpisodicMemoryCandidate` a través de la cadena episódica gobernada para impedir
> que evidencia o decisiones válidas para un contenido sean reutilizadas contra
> otro contenido que conserve el mismo `candidate_id`, sin confundir presencia de
> una identidad con verificación independiente, trust, autenticidad o autoridad?

Esta autorización comprende **análisis G0, decisión arquitectónica G1 y scope freeze
documental**.

No autoriza:

- código productivo;
- tests de implementación;
- G2-SPEC;
- implementación;
- Persistence Authorization;
- Memory persistente;
- almacenamiento;
- retrieval / RAG;
- Knowledge;
- Conversation wiring;
- cambios de Kernel;
- cambios del Security Control Plane;
- firmas, HMAC, PKI o remote attestation;
- replay protection general;
- Sprint 7.12;
- RDD Stage 2;
- merge automático.

Separaciones obligatorias:

```text
candidate_id != candidate content identity
identity carried != identity verified against actual candidate
identity verified != producer/component trusted
content identity != source authenticity
content integrity != source trust
content integrity != truth
content identity binding != producer authorization
producer authorization != signal truth
component output != authority
component self-assertion != independent verification
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored Memory
Evidence != Authority
```

---

## 2. Baseline exacto y cierre previo

Baseline fuente congelado para este G0/G1:

```text
repository: Aranwill/jarvis
branch:     main
commit:     0466e18075fd6bce6243e03f701a377fd34469dd
```

Ese commit integra PR #123 — implementación de `Episodic Candidate Content Identity G2`.

Project Vault reconciliado al inicio:

```text
repository: Aranwill/malak-project-vault
branch:     main
commit:     62c56b06ffc4e4172e574a3af116c7be1605e55e
```

El Sync Agent reportó posteriormente para Malāk:

```text
base_commit == head_commit == 0466e18075fd6bce6243e03f701a377fd34469dd
changed_files: 0
document_candidates: 0
validation_findings: 0
conclusion: pass
proposal_created: false
```

Por tanto, este diseño no se abre sobre drift conocido ni sobre una propuesta pendiente.

---

## 3. Estado material de la cadena episódica

El baseline dispone de la siguiente cadena aislada:

```text
EpisodicMemoryCandidate
        ↓
AdmissionAssessment
        ↓
Assessment Provenance
VALID | HOLD | INVALID
        ↓
Assessment Producer Authorization
AUTHORIZED | HOLD | DENIED
        ↓
Governed Input Projection
READY | HOLD | DENIED
        ↓
Governed Projection Consumption
BLOCKED | EVALUATED
        ↓
Episodic Admission
REJECT | HOLD | ELIGIBLE
        ↓
STOP
```

Además existe ahora:

```text
EpisodicMemoryCandidate
        ↓
canonical candidate representation v1
        ↓
SHA-256
        ↓
EpisodicCandidateContentIdentity
```

La identidad implementada contiene:

```text
candidate_id
digest_algorithm
digest_hex
canonicalization_version
policy_version
```

y puede verificarse contra un candidate mediante:

```text
MATCH | MISMATCH
```

La implementación de G2 no la propaga todavía a la cadena downstream.

---

## 4. Resultado formal G0 — necesidad demostrada

La cadena actual sigue usando principalmente `candidate_id` como correlación entre
artefactos.

Eso permite demostrar:

```text
assessment.candidate_id
== provenance.candidate_id
== producer_authorization.candidate_id
== projection.candidate_id
== candidate.candidate_id
```

pero no demuestra:

```text
all artifacts refer to the same exact candidate content
```

Escenario residual:

```text
Candidate A
candidate_id = "candidate-1"
content      = X
identity     = DX

↓ assessments / evidence / decisions

Candidate B
candidate_id = "candidate-1"
content      = Y
identity     = DY

DX != DY
```

Si únicamente se compara `candidate_id`, una cadena producida para X puede ser
re-pareada con Y.

La inmutabilidad del objeto no evita este caso porque pueden existir dos instancias
válidas distintas con el mismo ID.

Por tanto:

```text
candidate_id binding
!=
content identity binding
```

Y también:

```text
correct digest exists
!=
downstream evidence is bound to that digest
```

Conclusión G0:

```text
Persistence Authorization remains BLOCKED.
```

Antes de diseñarla debe existir binding end-to-end suficiente hasta el artefacto
gobernado que represente la evaluación consumida.

Disposición G0:

```text
G0 RESULT: PASS
necessity: demonstrated
candidate disposition: HARDEN
risk class: 3 — HIGH
blocking findings for design: 0
implementation authorized: false
```

---

## 5. Threat / failure model de esta unidad

La unidad protege primariamente contra **re-pairing estructural** y downgrade de
binding dentro de la cadena episódica. Después del hardening G1 también congela
qué puede y qué no puede afirmarse cuando un componente está comprometido.

### 5.1. Sustitución same-ID

```text
old candidate content + valid evidence
            ↓
new candidate content with same candidate_id
```

Debe fallar cerrado.

### 5.2. Reutilización de assessment stale

Un `AdmissionAssessment` producido para identidad DX no debe poder participar en
una projection para DY aunque ambos candidates compartan `candidate_id`.

### 5.3. Reutilización de provenance o producer authorization

Una decisión de provenance o autorización válida para DX no debe poder re-parearse
con un assessment equivalente en IDs pero ligado a DY.

### 5.4. Reutilización de temporal evidence

`GovernedTemporalControlEvidence` afecta campos trust-sensitive de validez temporal.
No debe poder trasladarse silenciosamente de DX a DY usando solamente el ID lógico.

### 5.5. Projection stale

Una `GovernedAdmissionInputProjection` READY para DX no debe poder consumirse contra
DY aunque el ID textual coincida.

### 5.6. Downgrade / fallback

La ausencia de content identity no debe provocar fallback a:

```text
candidate_id-only acceptance
```

### 5.7. Metadata criptográfica incompatible

Una identidad con algoritmo, canonicalization version o policy version incompatible
no debe aceptarse por comparación parcial del digest.

### 5.8. Presencia confundida con verificación

Transportar un sidecar no prueba que el componente haya verificado el candidate real.

Regla:

```text
identity present
!=
identity verified against actual candidate
```

Ningún artefacto puede aumentar su autoridad incluyendo un flag equivalente a:

```text
verified = true
```

si ese flag proviene del mismo componente que produce el artefacto.

### 5.9. Verificación transitiva

Queda prohibida la inferencia:

```text
component A verified
therefore component B may trust without verifying
```

Cuando una frontera dispone del candidate real, verifica localmente por sí misma.

No se admiten como sustitutos:

- caches globales de "verified";
- tokens de verificación reutilizables;
- booleans transitivos;
- headers internos de confianza;
- "already checked" como bypass del recompute/verify requerido.

### 5.10. Self-attestation de componente

Un componente no puede convertir su propio output en evidencia independiente de su
integridad mediante texto, metadata o una identity que él mismo copió.

```text
component says "I verified it"
!=
independent verification
```

La siguiente frontera trata el output recibido como DATA sujeto a su propio contrato.

### 5.11. TOCTOU / re-resolution por `candidate_id`

Una frontera que verifica un candidate concreto no debe:

```text
verify candidate instance X
↓
resolve again by candidate_id
↓
operate on candidate instance Y
```

La operación protegida debe continuar sobre la **misma instancia/material** cuya
identity fue calculada o verificada dentro de esa invocación.

Este requisito bloquea una sustitución entre check y use aunque X e Y compartan ID.

### 5.12. Unable-to-verify

Si una frontera que debe verificar no puede hacerlo por:

- metadata incompatible;
- identidad ausente;
- tipo inválido;
- versión desconocida;
- error de contrato;
- imposibilidad material de obtener la comprobación requerida;

no existe modo `best effort`.

```text
unable to verify
=> fail closed
```

Nunca:

```text
unable to verify
=> candidate_id fallback
```

### 5.13. Componente comprometido con output consistentemente falso

Esta unidad **no** pretende demostrar honestidad del código que ejecuta una frontera.

Un componente comprometido puede, dependiendo de su posición:

- producir un assessment semánticamente falso pero ligado correctamente a DX;
- producir una projection internamente consistente para DX con señales incorrectas;
- omitir un check si el propio código de esa frontera fue sustituido;
- copiar una identity válida y afirmar que la verificó.

El SHA-256 in-process no puede demostrar que el código que lo evaluó fue honesto.

Por tanto:

```text
content-bound output
!=
tamper-proof output
!=
independently trustworthy output
```

Este límite debe permanecer explícito para impedir que Content Identity se expanda
por interpretación hasta convertirse en una falsa garantía universal de seguridad.

---

## 6. Qué problema NO intenta resolver esta unidad

Esta unidad no prueba:

- identidad real de una persona o productor;
- autenticidad criptográfica de una fuente;
- verdad del contenido;
- corrección semántica de un assessment;
- honestidad del código de un componente comprometido;
- integridad de ejecución / remote attestation;
- autorización para persistir;
- autorización para recuperar;
- freshness de credenciales fuera de contratos ya existentes;
- anti-replay de transporte;
- unicidad global de `candidate_id`;
- integridad genérica de todos los artefactos de Malāk;
- integridad de `AuthorizationRequest` o `AuthorizationDecision` más allá de sus
  contratos actuales;
- integridad de archivos, DB, red o almacenamiento.

La responsabilidad es únicamente:

```text
this downstream artifact claims/binds to this exact candidate content identity
```

y, en fronteras con candidate real:

```text
this presented identity MATCHES this actual candidate content
```

No significa:

```text
this artifact is true / trusted / authentic / independently attested / authorized to persist
```

---

## 7. Inventario de artefactos y gap actual

### 7.1. `EpisodicMemoryCandidate`

Estado actual:

```text
candidate_id + structured content
```

Decisión G1:

```text
UNCHANGED
```

La identidad permanece como sidecar explícito; no se convierte `candidate_id` en hash.

### 7.2. `EpisodicCandidateContentIdentity`

Estado actual:

```text
implemented / immutable / deterministic / versioned
```

Decisión G1:

```text
REUSE AS THE BINDING TOKEN
```

No se crea un segundo digest type ni un alias de digest sin metadata.

### 7.3. `AdmissionAssessment`

Estado actual:

```text
assessment_id
candidate_id
kind
value
producer metadata
```

Gap:

```text
candidate_id only
```

Decisión G1:

```text
MUST carry exact candidate content identity
```

Portarla significa **binding declarado por contrato**, no verificación independiente.

### 7.4. `AssessmentProvenanceDecision`

Estado actual:

```text
assessment_id
candidate_id
kind
outcome
reason
```

Decisión G1:

```text
MUST echo exact candidate content identity
```

El echo conserva binding; no constituye attestation.

### 7.5. `AssessmentProducerAuthorizationEvidence`

Estado actual:

```text
assessment_id
candidate_id
kind
influence_class
producer_subject_id
AuthorizationRequest
AuthorizationDecision
```

Decisión G1:

```text
MUST carry exact candidate content identity
```

El Security `AuthorizationRequest` / `AuthorizationDecision` permanece sin cambios.
La autorización prueba permiso scoped del productor, no identidad material del candidate.

### 7.6. `AssessmentProducerAuthorizationDecision`

Decisión G1:

```text
MUST echo exact candidate content identity
```

### 7.7. `GovernedTemporalControlEvidence`

Estado actual:

```text
candidate_id
valid_from
valid_until
policy/rule reference
producer auth evidence
```

Decisión G1:

```text
MUST carry exact candidate content identity
```

El control temporal no puede ser una excepción al binding.

### 7.8. `GovernedAdmissionInputProjection`

Estado actual:

```text
candidate_id
outcome
reason
effective_context
effective_signals
...
```

Decisión G1:

```text
MUST carry exact candidate content identity for READY, HOLD and DENIED
```

La projection function dispone del candidate real y por ello debe verificar/recomputar
localmente la identity durante su propia invocación.

### 7.9. `GovernedAdmissionConsumptionResult`

Estado actual:

```text
candidate_id
outcome
reason
admission_decision?
```

Decisión G1 endurecida:

```text
MUST carry:
- actual_candidate_content_identity
- presented_projection_content_identity
```

Semántica:

```text
actual_candidate_content_identity
=
identity calculada/verificada del candidate realmente recibido por Consumption

presented_projection_content_identity
=
identity que la projection presentó a Consumption
```

Para `EVALUATED`:

```text
actual == presented
```

Para `BLOCKED` por content mismatch:

```text
actual != presented
```

Esta distinción preserva evidencia del conflicto y evita que un resultado de bloqueo
borre cuál fue la identity stale/presentada.

Para bloqueos no relacionados con identity, ambas identities deben seguir reflejando
el estado real/presentado disponible sin convertir igualdad en trust.

### 7.10. `EpisodicAdmissionDecision`

Estado actual:

```text
candidate_id
outcome
reason
evaluated_at
policy_version
```

Decisión G1:

```text
UNCHANGED BY THIS UNIT
```

Justificación:

- Admission es una policy pura existente;
- no debe adquirir dependencia sobre hashing para evaluar reglas;
- el adapter de consumo es la frontera gobernada que controla acceso a Admission;
- el `GovernedAdmissionConsumptionResult` content-bound puede contener la decisión
  de Admission sin convertir esa decisión interna en evidencia suficiente de persistencia.

Regla futura obligatoria:

```text
raw EpisodicAdmissionDecision
!=
Persistence Authorization input
```

Una futura Persistence Authorization deberá evaluar el artefacto gobernado
content-bound apropiado y no aceptar una AdmissionDecision aislada como prueba suficiente.

---

## 8. Alternativas evaluadas en G0/G1

### 8.1. Alternativa A — seguir usando solo `candidate_id`

```text
REJECT
```

No resuelve same-ID substitution.

### 8.2. Alternativa B — verificar content identity únicamente en Consumption

```text
REJECT AS INSUFFICIENT
```

Bloquearía una projection stale en la última frontera, pero dejaría assessments,
provenance, producer authorization y temporal evidence semánticamente ambiguos.

### 8.3. Alternativa C — propagar únicamente `digest_hex`

```text
REJECT
```

Motivos:

- pierde algoritmo;
- pierde canonicalization version;
- pierde policy version;
- permite comparaciones parciales ambiguas;
- duplica un contrato ya implementado.

### 8.4. Alternativa D — crear un `CandidateBindingId` nuevo

```text
REJECT
```

Sería un alias adicional para información ya representada por
`EpisodicCandidateContentIdentity`.

### 8.5. Alternativa E — generic `IntegrityEnvelope[T]`

```text
REJECT FOR CURRENT UNIT
```

Generaliza prematuramente fuera de episodic Memory y puede confundirse con integridad
universal o autenticidad.

### 8.6. Alternativa F — `UniversalIntegrityManager` / registry global

```text
REJECT
```

No existe necesidad de estado global, manager, registry, filesystem, DB ni network.

### 8.7. Alternativa G — convertir `candidate_id` en hash

```text
REJECT
```

`candidate_id` conserva su semántica de correlación lógica.

### 8.8. Alternativa H — firmas / HMAC / PKI / attestation ahora

```text
DEFER
```

Autenticidad o integridad de ejecución no son el problema mínimo de esta unidad.
Si un threat model futuro demuestra que Persistence necesita independencia frente a
compromiso del proceso/productor, deberá abrirse una unidad separada.

### 8.9. Alternativa I — propagar el sidecar completo existente

```text
SELECT
```

La identidad completa ya es:

- inmutable;
- versionada;
- explícita;
- domain-specific;
- determinista;
- validable contra el candidate.

### 8.10. Alternativa J — confiar transitivamente en un `verified` upstream

```text
REJECT
```

Un flag producido por la misma frontera no constituye verificación independiente y
crearía un bypass permanente ante compromiso o stale state.

### 8.11. Alternativa K — cache global de identity verification

```text
REJECT FOR CURRENT UNIT
```

Además de introducir estado global, reabre TOCTOU y vuelve ambiguo qué candidate
material fue verificado.

---

## 9. Decisión G1 — arquitectura seleccionada

G1 selecciona propagación **explícita, obligatoria, por contrato y fail-closed** del
mismo `EpisodicCandidateContentIdentity`, con verificación local no transitiva en las
fronteras que poseen el candidate real.

Cadena objetivo:

```text
EpisodicMemoryCandidate
        ↓
compute content identity
        ↓
EpisodicCandidateContentIdentity
        ↓
AdmissionAssessment
[candidate_id + carried identity]
        ↓
AssessmentProvenanceDecision
[same carried identity]
        ↓
AssessmentProducerAuthorizationEvidence / Decision
[same carried identity]
        ↓
GovernedTemporalControlEvidence
[same carried identity]
        ↓
Governed Admission Input Projection
[recompute/verify against actual candidate locally]
        ↓
Governed Projection Consumption
[recompute/verify against same actual candidate locally]
        ↓
GovernedAdmissionConsumptionResult
[actual identity + presented projection identity]
        ↓
STOP
```

El objetivo no es que cada artefacto posea un hash distinto.

Todos propagan **la identidad del mismo candidate content**, sin afirmar por ello que
cada productor o componente sea confiable.

---

## 10. Invariante de binding

Para todo artefacto candidato relacionado con contenido:

```text
artifact.candidate_id
== artifact.candidate_content_identity.candidate_id
```

Y para toda cadena compatible:

```text
assessment.identity
== provenance.identity
== producer_evidence.identity
== producer_decision.identity
== temporal_evidence.identity
== projection.identity
```

Cuando existe acceso al candidate real:

```text
verify_episodic_candidate_content_identity(candidate, presented_identity)
== MATCH
```

La igualdad requerida es sobre el sidecar completo, no únicamente sobre
`digest_hex`.

Eso incluye:

```text
digest_algorithm
canonicalization_version
policy_version
digest_hex
candidate_id
```

Pero queda congelado:

```text
sidecar equality
!=
component integrity
```

---

## 11. Mandatory binding — no compatibility downgrade

G1 prohíbe introducir:

```text
candidate_content_identity: Optional[...]
```

como mecanismo de migración productiva.

También prohíbe:

```text
if identity is None:
    fallback to candidate_id
```

No habrá modo `legacy`, feature flag, env var ni configuración para omitir binding.

La futura implementación deberá actualizar de forma atómica los contratos y tests
afectados dentro del candidate de implementación.

---

## 12. Compromise-Aware Binding — reglas duras

Esta sección forma parte del scope freeze y no es comentario informativo.

### 12.1. Carried vs verified vs trusted

Se congelan tres estados conceptuales distintos:

```text
CARRIED
identity está presente en el artefacto

VERIFIED LOCALLY
la frontera actual posee el candidate real y obtiene MATCH por sí misma

TRUSTED COMPONENT
propiedad externa a esta unidad; NO se deriva de CARRIED ni VERIFIED
```

No se introduce un enum productivo con estos nombres salvo que G2 demuestre necesidad.
La distinción es semántica y obligatoria.

### 12.2. Verificación no transitiva

Projection y Consumption no pueden aceptar como sustituto de su propia verificación:

```text
upstream_verified
verified_at
verification_token
trusted_by_previous_component
```

ni equivalentes.

### 12.3. No self-attestation

Un artefacto no puede autoelevarse por incluir metadata que afirme:

```text
integrity_verified
trusted
attested
safe
```

La siguiente frontera evalúa únicamente propiedades que pueda comprobar bajo su
contrato y autoridad actuales.

### 12.4. Same-material-after-check

Después de verificar un candidate, la frontera debe seguir operando sobre ese mismo
objeto/material dentro de la misma invocación.

Prohibido:

```text
verify(candidate_X)
resolve(candidate_id)
use(candidate_Y)
```

### 12.5. No verification cache as authority

Una cache puede ser estudiada en el futuro por performance, pero no puede convertirse
en autoridad de binding sin un diseño separado que preserve material identity,
invalidación y TOCTOU.

Esta unidad no autoriza tal cache.

### 12.6. Fail closed on unverifiable state

Cualquier estado donde el binding requerido no pueda comprobarse no debe producir:

```text
READY
AUTHORIZED
EVALUATED
```

por fallback.

### 12.7. Component-compromise boundary

Si el código de la misma frontera que debería verificar está comprometido, el atacante
puede omitir el check. Esta unidad no puede resolverlo desde dentro del mismo proceso.

No se permite documentar G1/G2 futuro como si content binding diera garantía contra
arbitrary code execution o sustitución del verificador.

---

## 13. Reglas por frontera

### 13.1. Assessment construction

`AdmissionAssessment` deberá exigir una instancia válida de
`EpisodicCandidateContentIdentity`.

Su constructor deberá preservar:

```text
assessment.candidate_id
== assessment.candidate_content_identity.candidate_id
```

Una inconsistencia interna de construcción es error de contrato, no `HOLD`.

El constructor no puede declarar que verificó el candidate porque no recibe
necesariamente el candidate real.

### 13.2. Assessment Provenance

G1 selecciona que la validación de provenance deje de depender exclusivamente de
un `expected_candidate_id` y reciba una expectativa content-bound.

Contrato conceptual:

```text
validate_assessment_provenance(
    assessment,
    expected_candidate_content_identity,
    evaluated_at,
)
```

Debe exigir:

```text
assessment.candidate_content_identity
== expected_candidate_content_identity
```

Mismatch conocido y explícito:

```text
outcome: INVALID
```

No `HOLD`, porque existe evidencia contradictoria de binding.

G2 congelará el nombre exacto del reason code.

### 13.3. Producer Authorization

Debe exigir igualdad exacta de content identity entre:

```text
assessment
provenance_decision
authorization_evidence
authorization_decision output
```

Una incompatibilidad conocida debe terminar fail-closed como:

```text
DENIED
```

No cambia las reglas del PDP ni el significado de `AuthorizationDecision`.

Tampoco convierte permiso del productor en prueba de corrección semántica.

### 13.4. Governed Temporal Control

Temporal evidence deberá incluir la misma identidad.

La projection deberá tratar una identidad temporal incompatible como:

```text
DENIED
```

No debe reducirse a `candidate_id` mismatch solamente.

### 13.5. Governed Projection construction

La función de proyección posee acceso al `EpisodicMemoryCandidate` real.

Por tanto, G1 exige que **esta invocación** recompute o verifique explícitamente la
identity actual del candidate y compruebe que toda evidencia de entrada está ligada
a ella.

Conceptualmente:

```text
actual_identity = compute(candidate)

for every assessment bundle:
    bundle identity == actual_identity

temporal identity == actual_identity
```

Cualquier stale/re-paired identity conocida:

```text
DENIED
```

antes de producir READY.

La projection resultante deberá incluir `actual_identity` en todos sus outcomes.

No puede aceptar `verified upstream` como sustituto de este paso.

### 13.6. Governed Projection Consumption

Consumption vuelve a disponer del candidate real.

Antes de consumir READY/HOLD/DENIED debe verificar localmente:

```text
actual_identity = compute(candidate)
verify(candidate, projection.candidate_content_identity) == MATCH
```

Si no coincide:

```text
BLOCKED
```

El content binding check debe ocurrir antes de delegar a Admission.

No se llama `evaluate_episodic_candidate` ante mismatch.

La misma instancia `candidate` verificada debe ser la utilizada para construir la
vista efectiva y delegar a Admission; no se re-resuelve por `candidate_id`.

### 13.7. Consumption Result — preservación de evidencia

El resultado deberá llevar:

```text
actual_candidate_content_identity
presented_projection_content_identity
```

Para `EVALUATED`:

```text
actual == presented == compute(candidate)
```

Para un `BLOCKED` por mismatch:

```text
actual == compute(candidate)
presented == projection.candidate_content_identity
actual != presented
```

Eso permite distinguir:

```text
qué candidate real fue recibido
vs.
qué identity intentó presentar la projection
```

sin convertir el resultado en una attestation independiente.

---

## 14. Precedencia de fallos

G1 no congela todavía todos los rankings exactos de reasons; eso corresponde a G2.

Sí congela estas reglas:

```text
known content identity mismatch
=> fail closed
```

Y:

```text
missing binding is not a HOLD-compatible legacy state
```

Precedencias mínimas:

1. type / structural contract errors se rechazan al construir;
2. content identity mismatch conocido se evalúa antes de producir READY/AUTHORIZED;
3. Projection verifica localmente contra el candidate antes de READY;
4. Consumption verifica localmente identity antes de Admission;
5. una incompatibilidad de identity no puede transformarse en un resultado permisivo
   por otra señal posterior;
6. un claim de `verified` upstream nunca altera esta precedencia.

G2 deberá congelar reason codes y rankings exactos sin alterar estas reglas.

---

## 15. `candidate_id` se conserva

G1 no elimina `candidate_id` de ningún contrato.

Motivo:

```text
candidate_id             = logical correlation
content identity sidecar = exact material identity
```

Ambos tienen responsabilidades distintas.

La redundancia es deliberada y se valida:

```text
identity.candidate_id == artifact.candidate_id
```

No se permite que digest sustituya semánticamente IDs operativos existentes.

---

## 16. El sidecar completo se propaga; no se re-canonicaliza downstream

Los módulos downstream no deben volver a implementar canonicalización del candidate.

Regla:

```text
candidate_content_identity.py
=
sole owner of candidate content canonicalization v1
```

Los demás módulos:

- almacenan/propagan el sidecar;
- comparan sidecars;
- usan `compute_...` o `verify_...` únicamente cuando tienen el candidate real;
- no reconstruyen manualmente digest inputs;
- no interpretan `digest_hex` por separado;
- no crean un segundo concepto de "verified identity" persistente.

---

## 17. Security boundary permanece separada

`AssessmentProducerAuthorizationEvidence` contiene Security contracts porque debe
probar permiso scoped del productor.

G1 no modifica:

```text
AuthorizationRequest
AuthorizationDecision
PermissionScope
PDP
PEP
SecurityContext
```

La content identity no concede permiso y el permiso no valida contenido.

```text
producer permission
!=
candidate content identity
```

Y:

```text
candidate content identity
!=
producer permission
```

Un componente productor comprometido tampoco se vuelve confiable por portar una
identity correcta.

---

## 18. Admission policy permanece pura

No se modifica `evaluate_episodic_candidate` ni la precedence existente de Admission.

La protección ocurre alrededor de Admission:

```text
bound projection
    ↓
local content verification in Consumption
    ↓
Admission evaluation
    ↓
bound Consumption result
```

La AdmissionDecision interna sigue representando solamente el resultado de policy.

No se debe interpretar:

```text
AdmissionDecision.candidate_id
```

como prueba criptográfica de content binding.

---

## 19. Future Persistence Authorization dependency

Esta unidad es una precondición, no una autorización de persistencia.

Después de completar una futura implementación de Propagation / Binding deberá
existir una revisión independiente que pregunte al menos:

```text
1. ¿es suficiente el bound consumption result como evidencia estructural?
2. ¿qué evidencia de producer authorization necesita persistencia?
3. ¿Persistence necesita confianza adicional sobre la ejecución/productor?
4. ¿el threat model requiere aislamiento, firma o attestation independiente?
5. ¿cómo se preserva/verifica content identity en write/read durable?
```

Hasta entonces:

```text
Persistence Authorization: NOT AUTHORIZED
Persistent Memory: NOT AUTHORIZED
```

Y aun después:

```text
content binding complete
!=
persistence authorization granted
```

Especialmente:

```text
terminal content-bound artifact
!=
tamper-proof artifact
!=
independently trustworthy artifact
```

---

## 20. Estrategia de implementación futura — atomic packet

G1 evalúa la división lógica inicial P1–P4:

```text
P1 Candidate → Assessment
P2 Assessment → Provenance / Producer Authorization
P3 Projection construction
P4 Projection → Consumption result
```

Estas fases son útiles para TDD y revisión interna, pero **no deben integrarse como
cuatro estados parciales de main**.

Motivo:

- un contrato obligatorio no debe quedar opcional entre merges;
- intermediate compatibility modes crearían bypass;
- la cadena debe cambiar de candidate-id-only a content-bound de forma coherente.

Decisión G1:

```text
logical phases: P1 → P2 → P3 → P4
integration unit: ONE ATOMIC IMPLEMENTATION CANDIDATE
```

G2 podrá subdividir commits TDD dentro de la misma rama candidata sin autorizar
merges parciales.

---

## 21. Scope freeze candidato para G2

Si el Owner autoriza posteriormente G2-SPEC, el alcance productivo candidato queda
limitado inicialmente a **cuatro módulos existentes**:

```text
src/malak/memory/assessment_provenance.py
src/malak/memory/assessment_producer_authorization.py
src/malak/memory/governed_input_projection.py
src/malak/memory/governed_projection_consumption.py
```

Tests candidatos correspondientes:

```text
tests/test_episodic_assessment_provenance.py
tests/test_assessment_producer_authorization.py
tests/test_governed_input_projection.py
tests/test_governed_projection_consumption.py
```

Fuera del file budget inicial:

```text
src/malak/memory/candidate_content_identity.py
src/malak/memory/episodic_admission.py
src/malak/memory/__init__.py
src/malak/security/**
src/malak/core/**
src/malak/services/**
src/malak/capabilities/**
Vault
Sync Agent
```

`candidate_content_identity.py` se consume como dependencia estable; no se modifica
salvo que G2 demuestre una inconsistencia real en el contrato ya integrado.

Cualquier quinto módulo productivo requerido implica:

```text
STOP → demonstrate necessity → owner review → new scope decision
```

---

## 22. File / dependency budget preliminar

G1 congela para una futura G2-SPEC este presupuesto inicial:

```yaml
production_files_new: 0
existing_production_files_modified: 4
test_files_new: 0
existing_test_files_modified: 4
external_dependencies_added: 0
kernel_delta: 0
security_contract_delta: 0
conversation_delta: 0
persistence_delta: 0
retrieval_delta: 0
authority_delta: 0
```

Los LOC guardrails exactos pertenecen a G2-SPEC una vez inspeccionado el diff
candidato detallado.

---

## 23. TDD contract candidato para una futura implementación

G2 deberá congelar tests que demuestren al menos:

### 23.1. Structural binding

- `AdmissionAssessment` exige content identity;
- `candidate_id` y identity.candidate_id deben coincidir;
- provenance decision conserva identity exacta;
- producer authorization evidence/decision conserva identity exacta;
- temporal evidence conserva identity exacta;
- projection conserva identity exacta;
- consumption result conserva actual + presented identities.

### 23.2. Same-ID substitution

Dos candidates con:

```text
same candidate_id
different material content
```

deben producir identities distintas y la cadena stale debe fallar cerrada.

### 23.3. Cross-artifact re-pairing

Debe probarse mismatch independiente en:

- assessment ↔ provenance;
- assessment ↔ producer evidence;
- assessment ↔ producer decision;
- temporal evidence ↔ candidate;
- assessment bundle ↔ candidate;
- projection ↔ candidate.

### 23.4. Metadata downgrade

Identities con:

- algorithm incompatible;
- canonicalization version incompatible;
- policy version incompatible;
- digest incompatible;

deben fallar cerradas cuando se verifican contra el candidate.

### 23.5. No candidate-id fallback

No debe existir caso donde una identity incompatible sea aceptada únicamente porque:

```text
candidate_id matches
```

### 23.6. Admission isolation

Ante projection identity mismatch:

```text
Consumption = BLOCKED
Admission evaluator = not invoked
```

### 23.7. Bound terminal result

Un `EVALUATED` debe demostrar:

```text
result.actual_identity
== result.presented_identity
== projection.identity
== computed candidate identity
```

Un `BLOCKED` por mismatch debe demostrar:

```text
result.actual_identity == computed candidate identity
result.presented_identity == projection.identity
result.actual_identity != result.presented_identity
```

### 23.8. Verification non-transitivity

Tests deben impedir un diseño donde Projection o Consumption puedan saltarse su
verificación local usando un flag/campo upstream equivalente a `verified`.

No es obligatorio introducir mocks; puede demostrarse por API/superficie contractual.

### 23.9. Same-material-after-check

La implementación no debe resolver otro candidate por `candidate_id` después del
check. G2 deberá seleccionar una prueba estructural o de comportamiento que proteja
esta propiedad sin introducir infraestructura innecesaria.

### 23.10. Unable-to-verify fail closed

Metadata no soportada o estado unverificable no debe producir READY/EVALUATED por
fallback.

### 23.11. Regression

- todo el suite existente debe permanecer PASS;
- canonical vectors A/B/C de Candidate Content Identity permanecen intactos;
- Admission precedence permanece intacta;
- Producer Authorization permission semantics permanecen intactas.

---

## 24. FULL 4R requerido

Risk class 3 exige FULL 4R en futura implementación.

### Risk

Demostrar que content identity:

- no se convierte en trust;
- no concede producer authorization;
- no concede Admission eligibility;
- no concede Persistence Authorization;
- no cambia Security authority;
- no se presenta falsamente como protección frente a un verificador comprometido.

### Readability

Un reviewer debe poder seguir visualmente:

```text
candidate content identity
→ carried by assessment
→ carried by provenance
→ carried by producer authorization
→ carried by temporal evidence
→ locally verified by projection
→ locally verified by consumption
→ actual/presented identities preserved in result
```

sin inferencia oculta ni helper genérico opaco.

### Reliability

Demostrar:

- exact sidecar propagation;
- same-ID substitution failure;
- stale evidence failure;
- non-transitive verification;
- actual vs presented terminal evidence;
- Ubuntu + Windows candidate-bound PASS;
- full pytest;
- compileall;
- diff-check.

### Resilience

Demostrar:

- no optional downgrade;
- no digest-only comparison;
- incompatible metadata fail-closed;
- no candidate_id fallback;
- no `verified upstream` bypass;
- no re-resolution by ID after local verification;
- no path alternativo hacia Admission desde una projection stale dentro de esta frontera.

---

## 25. RDD Stage 1

Una futura implementación deberá emitir `MALAK-EVIDENCE-MANIFEST/v1` ligado al SHA
exacto del candidate.

Debe incluir al menos:

- baseline SHA;
- candidate SHA;
- risk class;
- file budget;
- FULL 4R;
- pytest;
- compileall;
- diff-check;
- Ubuntu observation;
- Windows observation;
- correction rounds;
- blocking findings.

Se mantiene:

```text
Stage 1 evidence
!=
independent reviewer authority
!=
validator authority
!=
merge authority
```

RDD Stage 2 permanece no autorizado.

---

## 26. STOP conditions

Una futura G2 o implementación debe detenerse si requiere:

- modificar `EpisodicMemoryCandidate`;
- convertir `candidate_id` en digest;
- cambiar canonicalization v1 sin una inconsistencia demostrada;
- cambiar los vectores normativos para hacer pasar implementación;
- modificar Admission precedence;
- modificar `EpisodicAdmissionDecision` para obtener content binding;
- modificar Security contracts / PDP / PEP;
- introducir Persistence Authorization;
- introducir Memory store;
- introducir retrieval;
- introducir runtime wiring;
- introducir HMAC, firmas, PKI o attestation;
- introducir dependencia externa;
- hacer identity opcional;
- agregar legacy fallback a `candidate_id`;
- agregar un manager/registry global;
- agregar un cache de "verified" como autoridad;
- agregar self-attestation como bypass;
- re-resolver candidate por ID después del check dentro de la misma frontera;
- requerir un quinto módulo productivo sin nueva revisión de scope;
- usar digest como trust score o authority signal;
- afirmar protección frente a compromise del propio verificador sin una unidad de
  seguridad independiente que la demuestre.

---

## 27. Riesgos residuales después de esta unidad

Incluso después de una futura implementación correcta permanecerán fuera:

### R1 — authenticity

El hash no demuestra quién originó el contenido.

### R2 — truth

Un contenido falso puede tener identidad perfecta.

### R3 — producer correctness

Un productor autorizado puede emitir un assessment incorrecto; content binding solo
prueba a qué candidate content se refiere.

### R4 — component compromise

Un componente cuyo código fue comprometido puede generar output semánticamente falso,
omitir checks o mentir sobre haber verificado. La siguiente frontera puede limitar el
impacto solo cuando dispone de evidencia/candidate que pueda verificar por sí misma.

### R5 — authorization replay externo

La unidad no crea anti-replay general para Security contracts.

### R6 — persistence policy

Todavía faltará decidir qué evidencia exacta autoriza o bloquea almacenamiento.

### R7 — stored-content integrity

Esta unidad no define cómo una futura Memory store preservará/verificará identidad
durante escritura y lectura.

### R8 — execution trust / attestation

No se define aislamiento, firma de artefactos, process identity, TPM/TEE, remote
attestation ni validación fuera del proceso. Solo deberán considerarse si un threat
model futuro demuestra necesidad.

### R9 — retrieval / Knowledge

No define taint, revocation, quarantine, retrieval eligibility ni promoción a Knowledge.

---

## 28. Interpretaciones explícitamente prohibidas

Una implementación o documento futuro contradice este G1 si afirma cualquiera de:

```text
"tiene el digest correcto, por lo tanto es confiable"
"Producer Authorization significa que el assessment es verdadero"
"Projection lo verificó, por lo tanto Consumption no necesita verificar"
"el result está content-bound, por lo tanto es tamper-proof"
"candidate_id coincide, así que una identity ausente es aceptable"
"verified=True convierte self-attestation en evidencia independiente"
"un hash in-process prueba que el componente no fue comprometido"
```

Estas equivalencias quedan normativamente rechazadas por este design record.

---

## 29. Orden de maduración preservado

La secuencia correcta continúa siendo:

```text
Candidate Content Identity                 COMPLETE
        ↓
Content Identity Propagation / Binding     THIS G0/G1
        ↓
independent G2-SPEC                        NOT AUTHORIZED
        ↓
implementation                             NOT AUTHORIZED
        ↓
post-merge reconciliation                  future
        ↓
Persistence Authorization G0/G1            NOT AUTHORIZED
        ↓
possible execution-trust hardening         ONLY IF DEMONSTRATED NECESSARY
        ↓
Persistent Memory                          NOT AUTHORIZED
        ↓
Trust-aware retrieval                      NOT AUTHORIZED
        ↓
Knowledge promotion                        NOT AUTHORIZED
```

No se permite saltar directamente a persistencia porque exista un digest o un bound
consumption result.

---

## 30. Resultado final G0/G1

```text
unit:
Episodic Candidate Content Identity Propagation & Binding Boundary

G0 necessity: PASS
G1 architecture: SELECTED + COMPROMISE-AWARE HARDENED
risk class: 3 — HIGH

selected direction:
mandatory propagation of the existing full EpisodicCandidateContentIdentity sidecar
through the governed episodic evidence chain

verification model:
local, explicit, non-transitive where actual candidate is available

self-attestation:
PROHIBITED as independent evidence

TOCTOU rule:
verify and use the same candidate material within the same invocation

selected terminal binding:
GovernedAdmissionConsumptionResult carrying both actual candidate identity and
presented projection identity

terminal semantics:
content-bound artifact != tamper-proof artifact != independently trustworthy artifact

raw EpisodicAdmissionDecision:
NOT sufficient for future Persistence Authorization

implementation shape:
logical P1-P4 phases inside ONE atomic implementation candidate

candidate production scope:
4 existing memory modules
0 new production modules
0 external dependencies
0 Kernel changes
0 Security contract changes
0 Persistence changes

G2 authorized: false
implementation authorized: false
Persistence Authorization authorized: false
Persistent Memory authorized: false
RDD Stage 2 authorized: false
Sprint 7.12 authorized: false
```

Disposición:

```text
G0/G1 RESULT: ADOPT FOR OWNER REVIEW
NEXT GATE: explicit Owner authorization for G2-SPEC only
```

La aprobación de este documento no constituye autorización automática de código.
