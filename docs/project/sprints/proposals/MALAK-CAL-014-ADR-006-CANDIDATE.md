---
title: Malāk CAL-014 — ADR-006 Candidate Draft
status: gate_candidate
authority: non_normative_adr_candidate
language: es
as_of_date: 2026-09-13
source_baseline: b61c2764b708bf96ca3829e5a9959a0c5e53ad2c
future_target_path: docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
future_target_must_not_exist: true
adr_acceptance_authorized: false
normative_activation_authorized: false
law_materialization_authorized: false
owner_local_materialization_required: true
implementation_authorized: false
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-DURABLE-RELIANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/architecture/adr/ADR-TEMPLATE.md
---

# Malāk CAL-014 — ADR-006 Candidate Draft

## 1. Propósito

Preservar el contenido exacto candidato de una futura
`ADR-006 — Protected Durable Reliance Preconditions` sin crear remotamente una ADR
normativa ni aceptar una decisión arquitectónica.

```text
candidate draft != ADR-006 file
candidate draft != Accepted ADR
Accepted ADR != implementation authorization
```

## 2. Precondiciones

Antes de cualquier materialización local:

```text
ADR-006 target path MUST NOT EXIST
Scope Freeze MUST remain applicable
Cognitive Constitution blob = 34ecc6685dd686f9e7143b3547b61ec0d91c7c41
Blueprint blob = 9c09b26d040164955e99cc27c362b0e72373dc3f
Decision Index blob = 9d3c12a80adfbbca5bb9cdb6c90c933dab19c427
```

Cualquier diferencia material produce `STOP` y reapertura del gate afectado.

## 3. Contenido futuro candidato

El siguiente bloque es el contenido candidato completo del futuro archivo
`docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md` durante
su fase `Proposed`.

~~~~markdown
---
id: ADR-006
title: Protected Durable Reliance Preconditions
status: proposed
date: <activation-date>
author: Hector Rodriguez
reviewed_by: ChatGPT
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

Proposed

La presencia de este archivo no constituye aceptación, activación normativa,
autorización de implementación, Persistence Authorization ni autorización de
Persistent Memory.

```text
Proposal != Acceptance != Implementation != Authority
```

---

## Contexto

Malāk ya separa evidencia, autoridad, finalización, autorización y ejecución. La
Cognitive Constitution exige evidencia, trazabilidad, coherencia, consistencia
temporal y aprendizaje controlado. El Blueprint mantiene Zero Trust, Human in
Control, ownership único, contratos públicos y prohibición de reinterpretar
resultados o evidence como autoridad.

El baseline implementado ya dispone de Candidate Content Identity y propagación /
binding end-to-end suficiente a través de la cadena gobernada de Episodic Admission.
Ese trabajo resolvió la condición histórica que mantenía diferida CAL-014 en
ADR-005, pero no convierte por sí mismo Memory, Knowledge, evidencia externa o
artefactos derivados en fundamentos válidos para efectos durables.

El gap arquitectónico restante es proteger la transición mediante la cual material
retenido, recuperado, admitido o derivado pasa a ser utilizado como fundamento
material de una transición durable o de una decisión de alto impacto.

```text
retention != reliance
storage != trust
retrieval != trust
identity != trust
integrity != semantic truth
provenance != trust
trust != authority
```

---

## Decisión candidata

Si ADR-006 es aceptada, Malāk adoptará las siguientes propiedades arquitectónicas.

### 1. Durable reliance es una transición protegida independiente

`Durable reliance` será tratado como una transición distinta de:

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
y al contexto de reliance. Compartir únicamente un identificador lógico, fuente
declarada, storage location, historial de admisión o relación de derivación no
constituye binding suficiente.

### 3. Garantías no transitivas ni reutilizables por default

Una garantía válida para un artefacto, versión, derivación, propósito, contexto o
momento no se presume válida para otro.

```text
guarantee(A) != guarantee(B)
guarantee(T1) != automatically valid at T2
rehash != clean provenance
```

Cuando la policy aplicable requiera revalidación, una garantía stale o no
revalidable deberá fallar cerrado.

### 4. Fail-closed ante garantía requerida ausente o no aplicable

```text
required but unavailable != implicitly satisfied
required but stale != satisfied
required but unbound != satisfied
```

La ausencia de contradicciones, taint detectado o incidentes conocidos no equivale
a evidencia positiva suficiente. Una admisión previa, almacenamiento previo,
repetición frecuente o consenso tampoco elevan material a trusted por default.

### 5. Integridad, provenance, trust y authority permanecen separados

La decisión congela estas separaciones:

```text
content integrity != semantic truth
verified digest != authentic producer
source authenticity != truthful content
declared provenance != verified provenance
known provenance != trust
source identity != authority
stored != trusted
```

Ningún componente productor o presentador puede autoafirmar la suficiencia de sus
propias garantías.

### 6. Governance conserva autorización operativa

La Governance Constitution y sus policies conservan ownership sobre si una
operación persistente o protegida está permitida.

```text
CAL-014 compliance != permission to persist
CAL-014 compliance != Persistence Authorization
```

### 7. Security conserva enforcement y restricciones de seguridad

Security conserva ownership sobre enforcement y sobre restricciones aplicables a:

- taint;
- revocation;
- quarantine;
- disclosure;
- consent;
- freshness/replay;
- idempotency;
- otros controles de seguridad aplicables.

Esto no convierte a Security en owner del lifecycle semántico de Memory. Esta ADR
tampoco asigna ownership sobre la futura semántica de partial-failure de un write
protegido; ese límite deberá resolverse en el gate operativo correspondiente.

### 8. Memory Layer conserva lifecycle de dominio

Memory Layer conservará ownership sobre la futura semántica de lifecycle de Memory
cuando dicha capacidad sea diseñada y autorizada, subordinada a Constitución,
Governance y Security.

Esta ADR no autoriza Persistent Memory ni define todavía storage, retention runtime,
retrieval eligibility, supersession, quarantine implementation o promotion a
Knowledge.

### 9. La propiedad no crea automáticamente un componente

```text
constitutional requirement
!= automatic new layer/service/manager
```

La decisión no prescribe:

- database o storage provider;
- schema;
- hash/HMAC/PKI;
- nonce/TTL;
- vector store;
- encryption mechanism;
- provider/model;
- threshold;
- algoritmo concreto.

---

## Relación con ADR-005

ADR-005 queda preservada sin supersession.

```text
ADR-006 references ADR-005 for historical traceability
ADR-006 resolves the CAL-014 deferred condition recorded by ADR-005
ADR-006 does NOT depend operationally on Final Response semantics
ADR-006 does NOT supersede ADR-005 as a whole
```

---

## Alternativas consideradas

### A. Resolver CAL-014 únicamente en SECURITY.md

Rechazada como solución completa.

Security posee enforcement y restricciones de seguridad, pero durable reliance es
una propiedad transversal a Memory, Knowledge, evidencia externa y artefactos
derivados y no debe transferir a Security ownership del lifecycle cognitivo.

### B. Extender únicamente CC-003 o CC-010

Rechazada.

CC-003 gobierna evidencia y CC-010 aprendizaje permanente. Ninguna cubre por sí
sola toda transición de material previamente retenido/recuperado hacia reliance
durable.

### C. Convertir Content Identity en prueba de confianza

Rechazada.

Una identidad material estable demuestra igualdad/diferencia de contenido bajo el
contrato definido; no demuestra verdad semántica, productor auténtico, trust ni
authority.

### D. Crear un `Durable Reliance Manager` inmediatamente

Rechazada.

La necesidad demostrada es una propiedad arquitectónica. Un nuevo componente solo
podrá justificarse si una specification futura demuestra una responsabilidad real
que no pueda expresarse mediante fronteras existentes.

### E. Considerar cualquier almacenamiento como reliance

Rechazada.

Debe seguir siendo posible retener evidencia forense o material en cuarentena sin
convertirlo en trusted ni permitir su reutilización material.

---

## Consecuencias

### Positivas

- reduce trust laundering a través de storage, retrieval o repetición;
- evita reutilización implícita de garantías entre artefactos/contextos;
- preserva provenance a través de derivaciones;
- obliga a tratar freshness y applicability como parte de la transición;
- mantiene separadas autoridad operativa, seguridad y lifecycle de Memory;
- permite retención forense/quarantine sin elevar material a trust.

### Negativas

- futuras capabilities de Memory/Knowledge deberán modelar binding, freshness y
  provenance con mayor precisión;
- algunos flujos podrán producir `HOLD`, deny o abstention en vez de reutilizar
  evidencia previa de forma implícita;
- la futura persistencia requerirá más contratos antes de habilitar side effects.

### Riesgos

- policies futuras podrían definir assurance insuficiente;
- implementaciones podrían intentar usar hashes como sustituto de provenance;
- una autorización válida podría ser reutilizada fuera de contexto si no se resuelve
  replay/freshness en gates posteriores;
- lifecycle post-write de revocation/quarantine sigue pendiente antes de Persistent
  Memory real.

Mitigación normativa:

```text
mechanism-neutral law
+ exact-material binding
+ non-transitivity
+ fail-closed applicability
+ explicit ownership boundaries
```

---

## Impacto arquitectónico

Impacto permitido:

```text
Cognitive Constitution → CC-013
Blueprint              → R-023 + v0.6.3-alpha bookkeeping
ADR repository         → ADR-006
Decision Index         → only after human acceptance
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

## Relación con Gobernanza

La decisión respeta la precedencia constitucional y no crea permiso operativo.
Governance conserva decisión de autorización sobre operaciones persistentes y
protegidas. Security conserva enforcement y restricciones de seguridad. Memory
conserva su futuro lifecycle de dominio.

```text
Evidence != Authority
Decision != Enforcement != Execution
CAL-014 compliance != operational permission
```

---

## Compatibilidad con AKS / GraphRAG

La ADR puede representarse como decisión arquitectónica permanente y relacionarse
con Cognitive Constitution, Blueprint, ADR-005, Memory y Knowledge. Esta
representación no convierte GraphRAG/AKS en runtime autorizado ni autoriza retrieval.

---

## Criterio de aceptación

- [ ] CC-013 permanece mechanism-neutral.
- [ ] R-023 expresa solo la propiedad arquitectónica necesaria.
- [ ] CC-001..CC-012 permanecen semánticamente intactos.
- [ ] Governance Constitution permanece sin cambios.
- [ ] Security conserva enforcement sin absorber Memory lifecycle.
- [ ] Memory conserva ownership de su lifecycle futuro sin quedar autorizada a persistir.
- [ ] forensic/quarantine retention permanece posible sin trust/reliance.
- [ ] identity, integrity y provenance permanecen distintas de truth, trust y authority.
- [ ] garantías permanecen ligadas al material exacto, derivación relevante y contexto.
- [ ] stale, unavailable, non-applicable o unbound nunca se convierten en satisfied por default.
- [ ] no se crea nueva layer/service/manager.
- [ ] no se crea Persistence Authorization ni Persistent Memory.
- [ ] ADR-005 queda preservada sin dependencia operativa de Final Response.
- [ ] Decision Index solo cambia tras aceptación humana.
- [ ] Owner acepta explícitamente el paquete normativo.
~~~~

## 4. Activación futura

Este candidate draft solo define el contenido `Proposed`.

Una futura aceptación de ADR-006 requiere un gate humano separado que, como mínimo,
debe convertir de forma explícita:

```text
frontmatter status: proposed -> accepted
## Estado: Proposed -> Accepted
Decisión candidata -> Decisión
```

y registrar la aceptación humana junto con los hunks normativos de CC-013/R-023.

Ese futuro gate debe volver a validar blobs, coherencia normativa y ausencia de
autoridad de implementación.

## 5. Stop conditions

Detener si:

- ADR-006 ya existe en el target normativo;
- aparece necesidad de modificar Governance Constitution o SECURITY.md;
- se requiere una nueva layer/service/manager;
- se intenta convertir Content Identity en trust/authority;
- se requiere resolver storage/DB/schema/PKI/nonce/TTL;
- se intenta autorizar Persistence Intent, Persistence Authorization o Persistent Memory;
- se pretende aceptar remotamente ADR-006 mediante este candidate file.
