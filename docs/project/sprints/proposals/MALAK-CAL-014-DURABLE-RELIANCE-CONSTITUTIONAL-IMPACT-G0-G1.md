---
title: Malāk CAL-014 Durable Reliance — Constitutional Impact Review G0/G1
status: gate_candidate
authority: constitutional_impact_review
language: es
as_of_date: 2026-09-13
source_baseline: 0bf4f839f73de075589129886b044918622b53e7
vault_drift_zero_observed: true
constitutional_change_authorized: false
blueprint_change_authorized: false
governance_constitution_change_authorized: false
adr_creation_authorized: false
implementation_authorized: false
persistence_authorization_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
rdd_stage_2_authorized: false
sprint_7_12_authorized: false
alignment_matrix_ref: "section-12"
related:
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/architecture_quality_gates.md
  - docs/architecture/adr/ADR-002-policy-enforcement-boundary.md
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - SECURITY.md
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/project/sprints/proposals/EPISODIC-MEMORY-ADMISSION-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-PROPAGATION-G0-G1-DESIGN.md
  - docs/development/malak_construction_protocol.md
---

# Malāk CAL-014 Durable Reliance — Constitutional Impact Review G0/G1

## 1. Estado de autoridad

El Owner autorizó exclusivamente la reapertura G0/G1 de:

```text
CAL-014 — Source Identity and Content Integrity before Durable Reliance
```

La unidad puede:

- revisar por qué CAL-014 fue diferida;
- comprobar si la condición de reapertura ya existe en el baseline;
- contrastar la intención contra Constitución Cognitiva, Gobernanza, Blueprint,
  Security, ADR y contratos vigentes;
- aplicar la Malāk Alignment Matrix;
- incorporar la evidencia externa ya preservada en el Evidence Map;
- clasificar CAL-014 como `EXISTING`, `CLARIFY`, `NEW_CONSTITUTIONAL_CANDIDATE`,
  `POLICY_ONLY` o `DEFER`;
- proponer el delta normativo mínimo para una futura decisión humana.

La unidad NO puede:

- modificar ninguna Constitución;
- modificar Blueprint;
- crear o aceptar un ADR;
- autorizar Persistence Authorization;
- autorizar Persistent Memory;
- crear Durable Subject Binding;
- modificar código o tests;
- crear storage, repository, filesystem, database o vector store;
- implementar retrieval o Knowledge;
- modificar Security Control Plane;
- abrir Sprint 7.12;
- activar RDD Stage 2;
- ampliar autoridad.

```text
Review
!= Amendment
!= ADR acceptance
!= Specification
!= Implementation
!= Authority
```

---

## 2. Baseline congelado

Fuente oficial:

```text
Aranwill/jarvis
main@0bf4f839f73de075589129886b044918622b53e7
```

Estado downstream observado antes de abrir esta unidad:

```text
Project Vault reconciled
base_commit == head_commit == 0bf4f839...
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

El drift cero elimina ambigüedad operativa downstream; no concede autoridad
normativa.

---

## 3. Por qué CAL-014 fue diferida

La revisión constitucional previa clasificó CAL-014 como:

```text
DISPOSITION: DEFER
```

La causa no fue conflicto con Malāk ni falta de necesidad conceptual. Fue una
condición arquitectónica explícita:

```text
Candidate Content Identity G2 = absent
end-to-end content binding = absent
Persistence Authorization = absent
persistent Memory/Knowledge reliance = absent
```

La instrucción preservada fue:

```text
revisar nuevamente después de
Candidate Content Identity + binding suficiente
```

ADR-005 mantuvo la misma dependencia diferida y prohibió interpretar su aceptación
como autorización de Persistence Authorization o Persistent Memory.

---

## 4. G0 — condición de reapertura

El baseline actual ya contiene:

```text
EpisodicCandidateContentIdentity
        ↓
content identity propagation through governed admission chain
        ↓
local verification against actual candidate
        ↓
bound terminal consumption result
```

La implementación integrada también preserva:

```text
candidate_id != candidate content identity
content identity != trust
producer permission != content identity
bound artifact != independently trustworthy artifact
Consumption EVALUATED != Persistence Authorization
ELIGIBLE != Stored
```

Por tanto:

```text
REOPEN CONDITION: SATISFIED
```

Esto no demuestra todavía readiness para persistencia. Demuestra únicamente que
la razón arquitectónica que impedía evaluar normativamente CAL-014 dejó de estar
vigente.

### G0 result

```text
G0 RESULT: PASS
necessity: demonstrated
reopen precondition: satisfied
blocking findings: 0
amendment authorized: false
```

---

## 5. Definición precisa de `durable reliance`

G1 debe evitar una ambigüedad importante:

```text
durable retention
!=
durable reliance

durable storage alone
!=
durable reliance
```

`Durable reliance` significa que Malāk permite que contenido, evidencia, Memory,
Knowledge o un artefacto derivado influya materialmente como base aceptada para:

- un efecto persistente;
- una decisión de alto impacto;
- una futura decisión cuya corrección dependa de ese material;
- promoción o reutilización durable donde la identidad/integridad/provenance sean
  materialmente relevantes.

Existe influencia material cuando el material retenido participa como input
aceptado en una decisión, promoción, evaluación relevante para autorización,
efecto persistente u otra transición de estado durable cuya corrección dependa de
él. La mera presencia física o lógica del material en almacenamiento no satisface
esta definición.

```text
retained material
+ materially relied upon by a governed transition
→ durable reliance

retained material
without trusted/reliance semantics
→ retention only
```

No significa que todo byte almacenado deba ser previamente confiable.

Ejemplos que pueden requerir retención durable sin conceder trust:

```text
forensic evidence
quarantined payload
rejected candidate retained under explicit retention policy
audit artifact
```

Regla obligatoria:

```text
stored for evidence/quarantine
!=
trusted for cognitive or operational reliance
```

CAL-014 no debe impedir preservación forense gobernada ni convertir almacenamiento
en trust.

---

## 6. Cobertura normativa vigente

### 6.1 Cognitive Constitution

La Constitución ya cubre parcialmente la intención mediante:

- `CC-003 — Evidencia sobre especulación`;
- `CC-007 — Trazabilidad`;
- `CC-008 — Coherencia`;
- `CC-009 — Consistencia Temporal`;
- `CC-010 — Aprendizaje Controlado`;
- `CC-011 — Generation != Finalization / Evidence != Authority`;
- `CC-012 — Finalización Vinculada a Evidencia`.

Pero ninguna regla vigente expresa de forma general que, antes de reliance durable,
las garantías aplicables de identidad, integridad y provenance deban estar
satisfechas proporcionalmente al riesgo.

`CC-010` cubre aprendizaje permanente, pero CAL-014 también alcanza reliance
material sobre evidencia externa, Memory, Knowledge y artefactos derivados sin
reducirse a "aprendizaje".

Conclusión:

```text
coverage: PARTIAL
not sufficient for EXISTING
```

### 6.2 Governance Constitution

Gobernanza ya clasifica guardar Memory como operación persistente de Nivel 2 y
separa autorización de ejecución. También exige seguridad por defecto,
trazabilidad, mínimo privilegio, separación de responsabilidades, consistencia y
auditoría de modificaciones permanentes.

Por tanto la Gobernanza ya posee el dueño correcto de:

```text
whether a persistent operation is permitted
```

CAL-014 no debe duplicar esa responsabilidad.

Conclusión:

```text
Governance delta required: NO
```

### 6.3 Blueprint

Blueprint ya exige:

```text
Constitution First
Governance First
Human in Control
Zero Trust
Security by Design
Everything is Observable
Everything is Auditable
Specification & Verification First
```

También preserva:

```text
Memory as an independent responsibility
Kernel does not store Memory
public contracts between modules
no authority transfer through results/evidence
no bypass of validation/authority layers
```

No se demuestra necesidad de una nueva layer, service, manager o Kernel change.

Conclusión:

```text
architectural mechanism delta required by CAL-014: NO
```

Una futura enmienda constitucional deberá seguir el proceso normativo vigente,
incluyendo la actualización/versionado del Blueprint y un ADR aprobado cuando
corresponda, pero eso es un gate posterior y humano.

### 6.4 SECURITY.md

Security ya preserva requisitos muy cercanos:

```text
Having access to data
!=
permission to disclose, persist or reuse it
```

Y exige considerar para futuras superficies persistentes, según aplicabilidad:

- provenance;
- source authority;
- confidence;
- temporal validity;
- contradictions;
- poisoning / taint;
- sensitivity;
- owner/origin;
- purpose;
- scope;
- retention;
- exportability;
- remote-model eligibility;
- redaction;
- consent / human review;
- revocation / supersession / quarantine.

Security constituye una política y restricción fuerte, pero no sustituye la
pregunta constitucional sobre qué condición permanente debe preceder durable
reliance a través de Memory, Knowledge y evidencia.

Conclusión:

```text
Security coverage: STRONG / REINFORCING
constitutional duplication: NO
```

---

## 7. Distinciones que CAL-014 debe preservar

El principio futuro, si llega a promoverse, debe conservar como invariantes:

```text
logical id
!= content identity

content identity
!= source authenticity

provenance
!= trust

trust
!= authority

admission eligibility
!= persistence authorization

persistence authorization
!= durable write

durable write
!= trusted retrieval

stored
!= trusted

retention
!= reliance

evidence
!= authority
```

También:

```text
cryptographic mechanism
!= constitutional requirement
```

La Constitución puede exigir una propiedad; no debe congelar SHA-256, HMAC,
firmas, PKI, nonce, TTL, database schema, reason codes ni un algoritmo concreto.

### 7.1 Interpretaciones explícitamente prohibidas

CAL-014 no deberá reinterpretarse en el futuro como ninguna de estas equivalencias:

```text
stored
→ trusted

verified digest
→ authentic producer

known provenance
→ truthful content

previously eligible
→ currently valid

authorized operation
→ trusted payload

absence of taint
→ proof of safety

retention permission
→ reuse permission

repeated observation
→ canonical Knowledge
```

La ausencia de una señal negativa no constituye evidencia positiva suficiente.
Una garantía requerida pero no disponible no puede considerarse satisfecha por
default ni reemplazarse por historial de almacenamiento, frecuencia de reutilización
o falta de contradicción detectada.

---

## 8. Evidencia interna de diseño ya existente

### 8.1 Episodic Memory Admission G0/G1

La unidad original de Admission ya congeló:

```text
HOLD != retention authorization
HOLD != storage authorization
ELIGIBLE != persistence authorization
Admission Decision != Persistence Authorization != Storage
Eligible != Stored
Stored != Retrieved
Retrieved != Trusted for every task
```

También preservó hooks de data handling previos a persistence y escenarios
negativos para taint, revocation, metadata spoofing, missing inputs y source
authority separation.

Disposición:

```text
ADOPT
```

### 8.2 Candidate Content Identity + Propagation

Las unidades de Content Identity materializaron el prerequisito técnico que CAL-014
esperaba:

```text
logical candidate_id
+
exact material content identity
+
end-to-end binding through admission chain
```

Sin convertir identidad en trust o autorización.

Disposición:

```text
ADOPT
```

### 8.3 ADR-002 — PDP / PEP enforcement boundary

ADR-002 ya impide que el caller aporte una `AuthorizationDecision` fabricada como
autoridad al PEP y separa decisión de enforcement. También reconoce que replay,
TTL y mecanismos equivalentes requieren diseño posterior.

Disposición:

```text
ADOPT AS SEPARATE SECURITY RESPONSIBILITY
```

CAL-014 no debe absorber PDP/PEP ni convertir content identity en permiso.

---

## 9. Evidence Map — investigación externa preservada

Esta unidad no vuelve a consultar Internet ni convierte fuentes externas en
instrucciones. Consume únicamente propiedades ya preservadas en el Evidence Map.

### EXT-08 — OWASP Memory poisoning

Propiedad preservada:

```text
persistent Memory/context can transport compromise across interactions
```

Uso:

```text
CORROBORATION + IMPLEMENTATION_INPUT
```

Disposición:

```text
ADOPT property
REJECT architecture import
```

### EXT-09 — W3C PROV

Propiedad preservada:

```text
entity / activity / agent / derivation / attribution can remain separate
```

Uso:

```text
IMPLEMENTATION_INPUT
```

Disposición:

```text
ADAPT for future lineage design
REJECT full PROV schema adoption by default
```

### EXT-10 — SLSA provenance

Propiedad preservada:

```text
artifact identity + production provenance
!= authorization to use the artifact
```

Disposición:

```text
ADOPT separation
REJECT SLSA as mandatory Malāk architecture
```

### EXT-12 — Zanzibar authorization separation

Propiedad preservada:

```text
authorization deserves explicit, separately evaluable semantics
```

Disposición:

```text
ADAPT for future Persistence Authorization
NOT part of constitutional mechanism
```

### EXT-16 — Durable execution / retry semantics

Propiedad preservada:

```text
durable side effects require explicit retry/replay/idempotency semantics
```

Disposición:

```text
OBSERVE / IMPLEMENTATION_INPUT for future protected durable write
NOT part of CAL-014 normative text
```

### EXT-01 / EXT-02 — scoped and short-lived authority

Propiedad preservada:

```text
authority should be bounded, contextual, revocable and preferably short-lived
```

Disposición:

```text
OBSERVE for future authorization freshness/replay design
NOT part of CAL-014 mechanism
```

Regla:

```text
external evidence
!= authority

implementation input
!= implementation authorization
```

---

## 10. Alternativas G1

### A — Mantener CAL-014 en `DEFER`

Rechazada.

La razón explícita de defer era falta de Content Identity + binding suficiente.
Ese prerequisito ya está implementado en el baseline.

Mantener `DEFER` sin una nueva razón sería perder trazabilidad y dejar una deuda
normativa artificial.

### B — Reclasificar CAL-014 como `EXISTING`

Rechazada.

Los principios actuales cubren evidencia, trazabilidad, temporalidad, aprendizaje
controlado y autorización de operaciones persistentes, pero no expresan de forma
inequívoca la precondición de identidad/integridad/provenance antes de reliance
durable.

### C — Resolverlo únicamente en `SECURITY.md` / policy

Rechazada como solución completa.

Security posee requisitos operativos fuertes, pero la propiedad que se evalúa es
transversal a evidence, Memory y Knowledge. Reducirla a un detalle de una
implementación de Memory permitiría que otra superficie durable reinterpretara la
regla.

Los mecanismos concretos sí permanecen en Security/spec/policy.

### D — Promover CAL-014 original literalmente

No seleccionada sin adaptación.

La formulación conceptual original es correcta en dirección, pero puede confundirse
con una obligación de autenticar criptográficamente toda fuente o impedir retención
forense de material no confiable.

### E — Promover un principio mínimo y mechanism-neutral

Seleccionada como candidato G1.

Debe exigir propiedades proporcionales al riesgo antes de reliance durable y, a la
vez, preservar:

```text
retention != reliance
identity != trust
trust != authority
```

---

## 11. G1 — delta normativo mínimo candidato

### Disposición

```text
CAL-014
OLD: DEFER
NEW G1 DISPOSITION: NEW_CONSTITUTIONAL_CANDIDATE
```

No significa que la Constitución haya sido modificada.

### Formulación candidata

Nombre candidato, no numeración oficial:

```text
Durable Reliance requires applicable Identity, Integrity and Provenance
```

Texto normativo candidato:

> Antes de que Memory, Knowledge, evidencia externa o artefactos derivados sean
> utilizados como fundamento material para efectos durables o decisiones de alto
> impacto, Malāk deberá satisfacer, proporcionalmente al riesgo y según
> aplicabilidad, garantías suficientes sobre identidad de fuente, identidad e
> integridad del contenido y provenance. Un identificador lógico, la mera presencia
> o recuperación del material, su admisión previa, su almacenamiento, el consenso o
> la confianza declarada no sustituyen esas garantías. Cuando una garantía material
> requerida no pueda establecerse, no podrá considerarse implícitamente satisfecha:
> Malāk deberá limitar, retener para revisión, negar o abstenerse según la policy
> aplicable.

Aclaración normativa candidata:

> Esta regla no convierte identidad, provenance, receipts, almacenamiento ni
> evidencia en trust o autoridad; no impide retención forense o cuarentena gobernada
> de material no confiable; y no prescribe un mecanismo criptográfico, tecnología de
> almacenamiento o implementación concreta. Una admisión previa, almacenamiento
> previo, reutilización frecuente o ausencia de contradicción detectada tampoco
> sustituyen una garantía material requerida en el momento de reliance.

Regla fail-closed candidata:

```text
required but unavailable
!= implicitly satisfied
```

### Por qué es mínimo

No agrega una taxonomía, algoritmo ni componente.

Agrega una única invariante permanente:

```text
material durable reliance
requires
risk-proportional applicable identity + integrity + provenance
```

Todo mecanismo queda en specifications, policies y Security.

---

## 12. Malāk Alignment Matrix

| source | source_authority_class | applicable_invariant_or_intent | baseline_evidence | alignment_disposition | implementation_effect | deferred_or_rejected_effect | rationale | traceability_reference |
|---|---|---|---|---|---|---|---|---|
| Cognitive Constitution | constitutional | evidence, traceability, temporal consistency, controlled permanent learning, Evidence != Authority | CC-003/007/009/010/011/012 active | ADAPT | TO IMPLEMENT only if future normative activation is owner-approved | no mechanism, no persistence | existing coverage is partial; durable reliance condition is not explicit | `docs/governance/cognitive_constitution.md` |
| Governance Constitution | constitutional | persistent Memory is governed Level-2 operation; audit and consistency required | persistent operations already classified | ADOPT | NOT IMPLEMENTED by this review | no duplicate constitutional rule | authorization/execution already has an owner | `docs/governance/governance_constitution.md` |
| Blueprint | architecture master | Constitution/Governance First, Zero Trust, Security by Design, Memory ownership, public contracts, no bypass | active R-006/R-011/R-017..R-021/P-012 | ADOPT | NOT IMPLEMENTED | no new layer/service/manager/Kernel delta | candidate principle fits existing architecture | `docs/architecture/blueprint.md` |
| SECURITY.md | protected security requirements | access != permission to persist/reuse; provenance, taint, classification, retention, revocation | requirements already preserved | ADOPT | future design must comply | no universal trust manager | strong operational reinforcement, not replacement for constitutional invariant | `SECURITY.md` |
| Architecture Quality Gates | architectural governance | Blueprint/Constitution/Governance/Human-in-Control/traceability gates | active gates | ADOPT | future normative package must pass | no bypass | required acceptance envelope | `docs/architecture/architecture_quality_gates.md` |
| ADR-002 | accepted ADR | decision != enforcement; caller cannot inject authority; no blind retry | PDP/PEP boundary implemented | ADOPT | future Persistence Authorization remains separate | CAL-014 must not become an authorization token | preserves Security ownership | `docs/architecture/adr/ADR-002-policy-enforcement-boundary.md` |
| ADR-005 | accepted ADR | Evidence != Authority; CAL-014 deferred until Content Identity + binding | defer condition now satisfied | ADAPT | reopen review now | ADR-005 itself grants no persistence authority | explicit historical trigger reached | `docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md` |
| Episodic Memory Admission G0/G1 | owner-approved design record | HOLD != retention authorization; ELIGIBLE != persistence authorization; data-handling hooks | design properties implemented progressively downstream | ADOPT | future durable design reuses separations | no automatic persistence | direct precursor to this unit | `docs/project/sprints/proposals/EPISODIC-MEMORY-ADMISSION-G0-G1-DESIGN.md` |
| Candidate Content Identity | implemented design/baseline | logical id != content identity; identity != trust | sidecar implemented and tested | ADOPT | prerequisite fulfilled | no source authenticity claim | satisfies first deferred dependency | `docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-G0-G1-DESIGN.md`; `docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-G2-IMPLEMENTATION-CANDIDATE-SPEC.md`; `src/malak/memory/candidate_content_identity.py` |
| Content Identity Propagation | implemented design/baseline | end-to-end material binding; no transitive trust | propagation implemented through terminal Consumption | ADOPT | prerequisite fulfilled | no persistence authority | satisfies second deferred dependency | `docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-PROPAGATION-G0-G1-DESIGN.md`; `docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-PROPAGATION-G2-IMPLEMENTATION-CANDIDATE-SPEC.md`; `src/malak/memory/governed_projection_consumption.py` |
| Evidence-Bound Cognition Foundation | non-normative concept | CAL-014 conceptual intent | candidate law preserved | ADAPT | candidate wording refined | original wording not promoted verbatim | preserve intent without overclaim | `docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md` |
| Research Horizon Evidence Map EXT-08 | external evidence / corroboration + input | persistent Memory is attack surface | evidence previously reviewed | ADAPT | future Memory threat model input | no OWASP architecture import | supports need, no authority | `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md#19` |
| Evidence Map EXT-09 | external implementation input | provenance can be separate from decision/authority | evidence previously reviewed | ADAPT | future lineage input | no full PROV schema | supports original/derived distinction | `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md#19` |
| Evidence Map EXT-10 | external implementation input | artifact identity/provenance != authorization | evidence previously reviewed | ADOPT | preserve separation | no SLSA adoption | aligns directly with Malāk invariant | `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md#19` |
| Evidence Map EXT-12 | external corroboration + input | authorization is separately evaluable | evidence previously reviewed | ADAPT | future Persistence Authorization input | not constitutional mechanism | reinforces separation of responsibility | `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md#19` |
| Evidence Map EXT-16 | external implementation input | durable side effects need retry/replay/idempotency semantics | evidence previously reviewed | OBSERVE | DEFERRED to protected durable write | no Temporal dependency | relevant later, not CAL-014 text | `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md#19` |
| ideas.md / IDEA-016 | non-normative incubation | preserve original source, provenance, authority, retention, governed promotion | future planning intent | ADAPT | future design input | no Source Registry/GraphRAG implied | compatible but lower authority | `documents/projects/jarvis/ideas.md` |
| current code/tests | executable baseline | content identity + propagation are real, Persistence remains absent | current `src/malak/memory/**` and tests | ADOPT | prerequisite observed | no code delta in this review | baseline drives review | `main@0bf4f839f73de075589129886b044918622b53e7` |

### Matrix result

```text
alignment conflicts: 0
lower-authority source overriding higher authority: 0
historical snapshot substituted for baseline: 0
implementation authority inferred from evidence: 0
```

---

## 13. Security Horizon Check

| Horizon | Result | Rationale |
|---|---|---|
| Prompt / Context Trust Boundary | NOT_APPLICABLE to normative delta | no prompt/runtime path introduced |
| Identity / Delegation | REQUIRES_REINFORCEMENT later | source/workload identity and replay remain future design concerns |
| Compromise Containment / Trust Revocation | REQUIRES_REINFORCEMENT before real Persistent Memory | durable state must support distrust/revalidation lifecycle |
| Memory / Knowledge poisoning | REQUIRES_REINFORCEMENT | central motivation for CAL-014 |
| AI supply-chain trust | DEFERRED | relevant to external artifact provenance, not necessary for this amendment review |
| Data classification / disclosure | REQUIRES_REINFORCEMENT before durable write | retention/consent/redaction are future Persistence design inputs |
| Resource Governance | NOT_APPLICABLE to normative delta | no runtime resources added |
| Observability / evidence / Human in Control | ALREADY_COVERED for review | future persistent effects still require auditable governed operations |

No `BLOCKING_GAP` impide concluir el review normativo.

Los `REQUIRES_REINFORCEMENT` sí bloquean inferir que Persistent Memory está lista.

### 13.1 Readiness boundary: review normativo vs durable write

La ausencia de `BLOCKING_GAP` en este G0/G1 aplica únicamente a la capacidad de
concluir el review normativo de CAL-014.

```text
NO BLOCKING_GAP FOR:
CAL-014 normative review

BUT

BLOCKING BEFORE PROTECTED DURABLE WRITE:
- exact persistence subject / payload binding
- authorization freshness and replay semantics
- taint / revocation / quarantine lifecycle
- retention / disclosure / consent policy
- idempotency / partial-failure semantics
```

Por tanto:

```text
normative review readiness
!=
persistence implementation readiness
```

Ninguna conclusión de esta PR puede reutilizarse como evidencia de que esos cinco
frentes estén resueltos. Cada uno deberá obtener diseño, ownership, validación y
autorización propios según su gate aplicable.

---

## 14. Qué permanece fuera del principio constitucional

Aunque CAL-014 sea promovida en un gate posterior, deberán seguir fuera de la
Constitución:

```text
SHA-256 / digest algorithm
canonicalization format
HMAC / signatures / PKI
source attestation mechanism
nonce / replay implementation
TTL numbers
persistence intent schema
retention taxonomy
reason codes
PDP rule names
PEP implementation
storage technology
database schema
idempotency mechanism
retry strategy
quarantine storage design
retrieval ranking
Knowledge promotion policy
```

Esos elementos pertenecen a Security, specification, ADR, contracts, policies o
implementation según responsabilidad.

---

## 15. Stop conditions

Este review debe detenerse y volver al Owner si intenta:

- modificar directamente `cognitive_constitution.md`;
- modificar Governance Constitution o Blueprint;
- crear/aceptar un ADR;
- numerar oficialmente el futuro principio constitucional;
- crear contratos o APIs;
- tocar `src/` o `tests/`;
- elegir storage;
- implementar Persistence Intent;
- implementar Persistence Authorization;
- crear Memory persistente;
- fusionar retention con trust;
- exigir autenticidad criptográfica universal como ley;
- convertir Content Identity en trust o authority;
- convertir evidencia externa en autoridad;
- interpretar esta clasificación como autorización para el siguiente gate.

---

## 16. Normative Promotion Acceptance Criteria

Una futura unidad de promoción normativa de CAL-014 solo podrá concluir `PASS` si,
como mínimo, demuestra simultáneamente:

1. la formulación permanece mechanism-neutral y no congela criptografía,
   almacenamiento, taxonomy, TTL, replay o schemas concretos;
2. la responsabilidad de Governance sobre autorización y ejecución de operaciones
   persistentes no se duplica ni se desplaza;
3. Security conserva ownership de enforcement, taint, revocation, quarantine,
   retention, disclosure y controles operativos;
4. la retención forense o en cuarentena de material no confiable sigue siendo
   posible sin elevarlo a trust o reliance;
5. el principio no implica ni exige una nueva layer, service, manager o cambio de
   Kernel;
6. la promoción no crea autorización de implementación, Persistence Authorization,
   Persistent Memory, retrieval ni Knowledge;
7. identity, integrity y provenance permanecen separados de trust y authority;
8. el Owner acepta explícitamente la enmienda normativa mediante el gate humano
   correspondiente.

Cualquier incumplimiento material produce:

```text
FAIL or INCONCLUSIVE
never implicit PASS
```

---

## 17. G1 result

```text
G1 RESULT: PASS

CAL-014 previous disposition: DEFER
CAL-014 current design disposition: NEW_CONSTITUTIONAL_CANDIDATE

constitutional amendment: NOT AUTHORIZED
Blueprint amendment: NOT AUTHORIZED
ADR creation/acceptance: NOT AUTHORIZED
Persistence Intent: NOT AUTHORIZED
Persistence Authorization: NOT AUTHORIZED
Persistent Memory: NOT AUTHORIZED
implementation: NOT AUTHORIZED
blocking findings: 0
```

La razón de `NEW_CONSTITUTIONAL_CANDIDATE` es acotada:

```text
existing law covers evidence + traceability + controlled learning + governed
persistent operations

BUT

no current constitutional invariant explicitly requires applicable
identity + integrity + provenance before material durable reliance
```

La razón histórica para defer dejó de aplicar porque Content Identity y binding
end-to-end suficiente ya existen en el baseline.

---

## 18. Próximo gate posible — requiere autorización humana separada

Este G0/G1 no activa nada automáticamente.

Si el Owner aprueba continuar con la promoción normativa, el próximo paquete debe
ser separado y mínimo:

```text
CAL-014 NORMATIVE PROMOTION SCOPE FREEZE
        ↓
future constitutional amendment candidate
+ future ADR candidate
+ required Blueprint/version bookkeeping
        ↓
HUMAN REVIEW / ACCEPTANCE
```

Solo después de resolver la decisión normativa deberá retomarse:

```text
Episodic Persistence Intent / Durable Subject Binding G0/G1
```

Y aun entonces:

```text
constitutional principle
!= Persistence Authorization
!= Persistent Memory
```

---

## 19. Cierre

La reapertura confirma que Malāk llegó al punto arquitectónico que sus propios
documentos habían previsto para revisar CAL-014.

La dirección correcta no es importar una arquitectura externa ni convertir hashes
en autoridad. Es promover, si el Owner lo acepta en un gate posterior, una sola
invariante permanente y mechanism-neutral:

```text
before material durable reliance
require risk-proportional applicable
identity + integrity + provenance
```

preservando siempre:

```text
retention != reliance
identity != trust
trust != authority
Evidence != Authority
ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored Memory
```