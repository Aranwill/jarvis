---
id: ADR-006
title: Protected Durable Reliance Preconditions
status: accepted
date: 2026-09-13
author: Hector Rodriguez
reviewed_by: []
version: 0.6.0-alpha

tags:
  - architecture
  - decision
  - cognition
  - memory
  - knowledge
  - security
  - provenance
  - integrity

related:
  - DOC-ARQ-BLUEPRINT
  - DOC-GOV-COGNITIVE-CONSTITUTION
  - ADR-005
  - docs/project/sprints/proposals/MALAK-CAL-014-DURABLE-RELIANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-SCOPE-INTERPRETIVE-HARDENING.md

affects:
  - Blueprint
  - Cognitive Constitution
  - Memory Layer
  - Knowledge Layer
  - durable reliance transitions

depends_on:
  - Cognitive Constitution
  - Governance Constitution
  - Blueprint

supersedes: null
superseded_by: null

graph:
  node_type: ArchitectureDecision
  priority: High
---

# ADR-006 — Protected Durable Reliance Preconditions

## Estado

Accepted

ADR-006 fue aceptada explícitamente por el Owner el 2026-09-13 mediante
el gate humano de activación normativa. La aceptación de esta decisión no
constituye autorización de implementación.

Esta aceptación activa únicamente la decisión normativa descrita en este ADR y
se materializa conjuntamente con CC-013, R-023 y la indexación correspondiente
en Decision Index.

No autoriza Persistence Authorization, Persistent Memory, RDD Stage 2 ni
Sprint 7.12.

```text
Proposal != Acceptance != Implementation != Authority
```

---

## Contexto

Malāk ya separa evidencia, autoridad, autorización, enforcement y ejecución. El
baseline implementado dispone de Candidate Content Identity y propagación/binding
end-to-end suficiente para cerrar la condición histórica que mantenía diferida
CAL-014 en ADR-005. Ese hecho no convierte por sí mismo Memory, Knowledge, evidencia
externa o artefactos derivados en fundamento válido para efectos durables.

El gap arquitectónico es la transición mediante la cual material retenido,
recuperado, admitido o derivado pasa a ser utilizado como fundamento material de una
transición durable o de una decisión de alto impacto.

```text
retention != reliance
storage != trust
retrieval != trust
identity != trust
integrity != semantic truth
provenance != trust
trust != authority
permission to persist != permission to rely
repeated observation != canonical Knowledge
```

---

## Definiciones interpretativas

### Exact material

`Exact material` es el contenido o representación material realmente utilizado como
fundamento de la transición o decisión.

```text
exact material
!= logical ID
!= pointer
!= alias
!= source label
!= storage location
!= historical candidate/admission ID
```

Una specification futura puede definir representación canonical o mecanismo de
binding, pero no puede sustituir el material real por un identificador indirecto.

### Relevant derivation

`Relevant derivation` es provenance/lineage suficiente para reconstruir los cambios
materiales entre el origen o antecedente pertinente y el artefacto objeto de
reliance.

```text
relationship exists != derivation sufficiently known
rehash / rewrap / copy != provenance reset
```

Una transformación material para identity, integrity, provenance, trust, authority,
admissibility o applicability no puede omitirse silenciosamente.

### Reliance context

`Reliance context` comprende, según aplicabilidad, propósito, operación o transición
concreta, policy vigente, estado temporal y contextos de autoridad/seguridad
necesarios para evaluar si las garantías continúan siendo válidas.

```text
same content != same reliance context
previously valid context != current applicability
```

---

## Decisión

Malāk adopta las siguientes propiedades arquitectónicas.

### 1. Durable reliance es una transición protegida independiente

`Durable reliance` es distinta de:

```text
retention
storage
retrieval
admission
authorization
execution
```

La existencia previa de cualquiera de esos estados no convierte el material en
fundamento válido para un efecto durable.

### 2. Garantías ligadas al sujeto exacto

Antes de durable reliance deberán satisfacerse, proporcionalmente al riesgo, las
garantías aplicables de identidad, integridad y provenance exigidas por la
Constitución Cognitiva y por las policies/specifications vigentes.

Las garantías deberán quedar ligadas al material exacto, a la derivación relevante
y al contexto actual de reliance. Compartir únicamente un identificador lógico,
fuente declarada, storage location, historial de admisión o relación de derivación
no constituye binding suficiente.

### 3. Policy refina; no puede reducir el piso constitucional

Una policy puede refinar:

```text
how an applicable constitutional guarantee is instantiated
how sufficiency is evaluated
risk-proportional depth
revalidation conditions
conditional applicability within superior governed criteria
```

Una policy no puede:

```text
waive an applicable constitutional requirement
manufacture non-applicability to evade a material guarantee
declare a required guarantee satisfied by absence of evidence
convert missing evaluation capability into PASS
lower the constitutional floor for convenience/cost/latency
infer trust from prior storage/admission/repetition
```

Toda no-aplicabilidad material que elimine una garantía deberá ser:

```text
governed
+ justified
+ reconstructible/auditable
+ compatible with superior invariants
```

Costo, latencia, convenience, ausencia de evaluator o preferencia del
producer/presenter no constituyen por sí solos justificación válida.

Si una obligación constitucional material es aplicable y no existe capacidad
autorizada para evaluarla:

```text
no evaluation capability != no assurance required
result -> fail closed for durable reliance
```

### 4. Garantías no transitivas ni reutilizables por default

Una garantía válida para un artefacto, versión, derivación, propósito, contexto o
momento no se presume válida para otro.

```text
guarantee(A) != guarantee(B)
guarantee(T1) != automatically valid at T2
rehash != clean provenance
```

Cuando la policy aplicable requiera revalidación, una garantía stale o no
revalidable deberá fallar cerrado.

### 5. High-impact classification es gobernada y fail-closed

La clasificación de alto impacto deberá ser gobernada y reconstructible/auditable.
No puede ser autoasignada ni auto-rebajada por producer, presenter, model, agent o
componente interesado.

```text
unable to determine impact != low impact
unclassified != low impact
missing classifier != low impact
```

Cuando incertidumbre material pueda cambiar las garantías exigibles:

```text
apply high-impact protections OR block/escalate
never downgrade by default
```

### 6. Origin/producer identity applicability es gobernada

La identidad de origen/productor es materialmente aplicable cuando correctness,
provenance, trust, authority, admissibility o risk dependen de quién o qué produjo,
originó o transformó materialmente el contenido.

La aplicabilidad deberá surgir de rules/policies gobernadas o de una invariante
superior aplicable.

```text
producer says identity irrelevant != identity not applicable
presenter lacks identity != identity requirement waived
```

Si la identidad materialmente requerida no puede establecerse, la transición falla
cerrado.

### 7. Fail-closed ante garantía requerida ausente, stale, unbound o no justificable

```text
required but unavailable != implicitly satisfied
required but stale != satisfied
required but unbound != satisfied
unjustified non-applicability != satisfied
```

Ausencia de contradicción, taint detectado o incidentes conocidos no equivale a
evidencia positiva suficiente. Admission previa, storage previo, repetición o
consenso tampoco elevan material a trusted por default.

### 8. Integridad, provenance, trust y authority permanecen separados

```text
content integrity != semantic truth
verified digest != authentic producer
source authenticity != truthful content
declared provenance != verified provenance
known provenance != trust
source identity != authority
stored != trusted
```

Ningún producer o presenter puede autoafirmar la suficiencia de sus propias
garantías.

### 9. Governance conserva autorización operativa

Governance y la policy de autorización aplicable conservan ownership sobre si una
operación persistente o protegida está permitida.

```text
CAL-014 compliance != permission to persist
CAL-014 compliance != Persistence Authorization
```

### 10. Security conserva constraints y enforcement

Security constrains y enforces una permission aplicable. No adquiere autoridad
operativa autónoma ni lifecycle ownership de Memory.

```text
Security constraint/enforcement != operational authority
```

Security puede imponer controles aplicables a taint, revocation, quarantine,
disclosure, consent, freshness/replay, idempotency y otros requisitos de seguridad,
sin convertirse en fuente autónoma de permiso.

### 11. Memory Layer conserva lifecycle semantics de dominio

Memory Layer conservará ownership sobre futuras lifecycle semantics de Memory cuando
esa capacidad sea diseñada y autorizada, subordinada a Constitution, Governance y
Security.

```text
Memory lifecycle semantics != operational authority
```

Esta ADR no autoriza Persistent Memory ni define storage, retention runtime,
retrieval eligibility, supersession, quarantine implementation o promotion a
Knowledge.

### 12. Failure handling cognitivo permanece separado de retention/quarantine

Cuando CAL-014 falla:

```text
block / limit / deny / abstain the reliance transition
```

Cualquier retention o quarantine es un efecto operativo separado y solo puede
ocurrir cuando exista authorization independiente bajo Governance/policy de
autorización aplicable, sujeta a Security constraints/enforcement y a Memory
lifecycle semantics aplicables.

```text
retention/quarantine authorization != later reliance permission
```

### 13. Partial-failure permanece diferido al gate operativo

La futura semántica de partial-failure de un protected durable write deberá resolverse
en el gate operativo correspondiente. Esta ADR no le asigna ownership por inferencia
a Governance, Security ni Memory.

### 14. La propiedad no crea automáticamente un componente

```text
constitutional requirement != automatic new layer/service/manager
```

La decisión no prescribe database, storage provider, schema, hash/HMAC/PKI,
nonce/TTL, vector store, encryption mechanism, provider/model, threshold ni algoritmo
concreto.

### 15. Runtime readiness permanece separado de la activación normativa

La aceptación de esta ADR y la activación de CC-013/R-023 no demuestran que exista
runtime autorizado o suficientemente diseñado.

```text
normative activation readiness
!= durable reliance runtime readiness
!= persistence implementation readiness
```

Antes de cualquier durable reliance runtime deberán quedar resueltos y validados,
como mínimo:

```text
exact reliance subject/content binding
derivation/lineage binding
applicability + freshness + non-transitivity
fail closed when a required guarantee is unavailable
```

Antes de cualquier protected durable write deberán resolverse además:

```text
exact persistence subject/payload binding
authorization freshness/replay
taint/revocation/quarantine lifecycle
retention/disclosure/consent
idempotency/partial-failure
```

Estos requisitos son readiness gates futuros; no autorizan ni prescriben su
implementación en esta ADR.

---

## Threats explícitamente bloqueados

La decisión está diseñada para impedir, como mínimo:

```text
trust laundering through storage / retrieval / repetition
identity laundering through re-hashing or re-wrapping derived content
provenance truncation across derivation boundaries
stale-guarantee replay
cross-artifact or cross-context guarantee reuse
authorization laundering: permission to persist -> permission to rely
self-attestation of sufficiency by producer/presenter
risk laundering through relabeling or missing classification
```

---

## Relación con ADR-005

ADR-005 queda preservada sin supersession.

```text
ADR-006 references ADR-005 for historical traceability
ADR-006 resolves the CAL-014 deferred condition recorded by ADR-005
ADR-006 does NOT depend operationally on ADR-005 finalization semantics
ADR-006 does NOT supersede ADR-005 as a whole
```

---

## Alternativas consideradas

### A. Resolver CAL-014 únicamente en SECURITY.md

Rechazada: durable reliance es una propiedad transversal y Security no debe absorber
operational authority ni Memory lifecycle semantics.

### B. Extender únicamente CC-003 o CC-010

Rechazada: ninguna cubre por sí sola toda transición de material previamente
retenido/recuperado hacia durable reliance.

### C. Convertir Content Identity en prueba de confianza

Rechazada: content identity no demuestra semantic truth, producer authenticity,
trust ni authority.

### D. Crear un `Durable Reliance Manager` inmediatamente

Rechazada: la necesidad demostrada es una propiedad arquitectónica; un nuevo
componente requeriría justificación posterior independiente.

### E. Considerar cualquier almacenamiento como reliance

Rechazada: debe poder existir forensic/quarantine retention sin trust ni permiso de
reutilización material.

---

## Consecuencias

### Positivas

- reduce trust laundering por storage/retrieval/repetition;
- bloquea manufactured non-applicability;
- evita risk laundering por falta de clasificación;
- evita reutilización implícita de garantías entre artefactos/contextos/tiempos;
- preserva provenance a través de derivaciones;
- mantiene separadas operational authorization, Security enforcement y Memory lifecycle;
- permite forensic/quarantine retention sin elevar material a trust.

### Negativas

- futuras capabilities de Memory/Knowledge deberán modelar binding, freshness,
  applicability y provenance con mayor precisión;
- algunos flujos producirán HOLD/deny/abstention en vez de reutilizar evidencia
  previa de forma implícita;
- futura persistence requerirá contratos adicionales antes de side effects.

### Riesgos restantes

- specifications futuras podrían intentar convertir mecanismos en sustitutos de las
  garantías constitucionales;
- replay/freshness operacional requerirá gates específicos;
- protected write partial-failure sigue diferido;
- lifecycle post-write sigue pendiente antes de Persistent Memory real.

---

## Impacto arquitectónico

Impacto permitido:

```text
Cognitive Constitution -> CC-013
Blueprint              -> R-023 + v0.6.3-alpha bookkeeping
ADR repository         -> ADR-006
Decision Index         -> only after human acceptance
```

Impacto explícitamente no autorizado:

```text
Governance Constitution
SECURITY.md
Kernel
new layer/service/manager
src/**
tests/**
Persistence Intent
Persistence Authorization
Persistent Memory
retrieval/RAG/Knowledge runtime
RDD Stage 2
Sprint 7.12
```

---

## Criterio de aceptación

- [x] CC-013 permanece mechanism-neutral.
- [x] R-023 expresa solo la propiedad arquitectónica necesaria.
- [x] CC-001..CC-012 permanecen semánticamente intactos.
- [x] Governance Constitution permanece sin cambios.
- [x] policy refinement no puede convertirse en constitutional waiver.
- [x] manufactured non-applicability queda prohibida.
- [x] material non-applicability exige governed + justified + reconstructible/auditable.
- [x] no evaluation capability falla cerrado cuando la obligación material aplica.
- [x] high-impact classification es governed + auditable + non-self-downgradeable.
- [x] `unable to determine impact != low impact`.
- [x] origin/producer identity applicability es gobernada.
- [x] exact material, relevant derivation y reliance context preservan sus definiciones.
- [x] Governance authorization, Security enforcement y Memory lifecycle permanecen separados.
- [x] failure handling cognitivo no concede retention/quarantine/persistence authority.
- [x] forensic/quarantine retention permanece posible solo bajo authorization independiente.
- [x] identity, integrity y provenance permanecen distintas de truth, trust y authority.
- [x] garantías permanecen no transitivas y ligadas al material/contexto aplicable.
- [x] stale, unavailable, unjustified non-applicability o unbound nunca pasan por default.
- [x] partial-failure permanece diferido sin ownership inferido.
- [x] normative activation readiness permanece distinta de runtime/persistence readiness.
- [x] durable reliance runtime gate conserva binding/lineage/applicability/freshness/fail-closed.
- [x] protected durable write gate conserva payload binding, authorization freshness/replay,
      lifecycle, consent/disclosure/retention e idempotency/partial-failure.
- [x] no se crea nueva layer/service/manager.
- [x] no se crea Persistence Authorization ni Persistent Memory.
- [x] ADR-005 queda preservada sin dependencia operativa de Final Response.
- [x] Decision Index solo cambia tras aceptación humana.
- [x] Owner acepta explícitamente el paquete normativo.
