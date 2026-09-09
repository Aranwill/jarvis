---
title: Episodic Memory Admission Boundary — G0/G1 Design Record
status: design_authorized
authority: owner-approved design record
as_of_date: 2026-09-09
unit: Episodic Memory Admission Boundary Foundation
gate: G1
source_baseline: 10d6945d6f19a61c9dc9724738545107b9148707
issue: 72
risk_class: 3
implementation_authorized: false
persistent_memory_authorized: false
knowledge_implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
language: es
---

# Episodic Memory Admission Boundary — G0/G1 Design Record

## 1. Estado de autoridad

El propietario autorizó **G1 exclusivamente para diseño** de la unidad mínima:

```text
Episodic Memory Admission Boundary Foundation
```

La autorización permite:

- especificar la frontera entre experiencia conversacional y candidato de memoria episódica;
- definir identidad del candidato y binding de provenance;
- definir scope, dominio, propósito y validez temporal;
- definir semántica de trust, contradicción, taint, revocación y supersession;
- definir outcomes de admisión y escenarios negativos;
- definir hooks mínimos de clasificación de datos requeridos antes de persistencia futura;
- definir contratos futuros y stop conditions.

No autoriza:

- Memory persistente;
- base de datos, filesystem, SQLite o vector store;
- embeddings, RAG o GraphRAG;
- retrieval;
- implementación de Knowledge;
- memoria semántica, procedimental o archivada;
- summarization o promotion automática;
- decisiones de trust realizadas por un LLM;
- nuevos managers, registries o servicios runtime;
- cambios de Kernel;
- cambios de `SecurityContext` o Security Control Plane;
- agents, tools o red;
- asignación de Sprint 7.12;
- RDD Stage 2;
- merge sin aprobación explícita del propietario.

La autoridad final permanece humana.

---

## 2. Resultado G0 incorporado

La revisión G0 sobre el baseline vigente concluyó:

```text
G0 RESULT: PASS
candidate disposition: ADAPT
selected minimum unit: Episodic Memory Admission Boundary Foundation
risk class: 3
blocking findings: 0
implementation authorized: false
```

La adaptación desde `Trustworthy Memory & Knowledge Admission Foundation` fue necesaria para preservar una separación permanente de Malāk:

```text
Conversation != Memory
Memory != Knowledge
Knowledge != Policy
Policy != Authority
```

La unidad mínima no intenta diseñar simultáneamente Memory y Knowledge.

---

## 3. Necesidad demostrada

El baseline actual ya produce intercambios conversacionales aislados por sesión mediante contexto efímero en memoria.

Existe por tanto una experiencia real que podría, en una evolución futura, originar un candidato de memoria episódica.

No existe todavía una frontera gobernada que determine si una experiencia puede influir persistentemente en Malāk.

La necesidad mínima es entonces:

```text
Conversation Exchange
        ↓
Experience
        ↓
Episodic Memory Candidate
        ↓
Admission Boundary
```

No es:

```text
Conversation
   ↓
automatic persistence
```

ni:

```text
LLM output
   ↓
automatic memory
```

---

## 4. Regla cognitiva central

Un resultado generado o una experiencia observada puede convertirse en **candidate**.

No adquiere trust, autoridad o permanencia por ese hecho.

```text
LLM output != trust
LLM output != authority
LLM output != memory merely because it was generated
```

Todo aprendizaje permanente deberá atravesar validación gobernada y conservar trazabilidad, reversibilidad y auditabilidad.

---

## 5. Objeto diseñado

G1 diseña únicamente el concepto lógico `EpisodicMemoryCandidate`.

No se aprueba ese nombre como clase Python ni contrato definitivo.

Propiedades conceptuales mínimas:

```text
candidate_id
origin
conversation_session_id
request_id / exchange identity when available
created_at
subject_scope
domain
purpose
source_authority
confidence
temporal_validity
sensitivity / disclosure constraints
trust_state
admission_state
lineage / derived_from
```

No todos los campos deberán necesariamente materializarse con esos nombres.

El objetivo es fijar información suficiente para decidir admisión sin depender del contenido semántico desnudo.

---

## 6. Provenance y binding

Todo candidato debe poder reconstruir de dónde provino.

Como mínimo, cuando la fuente exista:

```text
candidate
   ↓
origin type
   ↓
session / request / exchange binding
   ↓
source identity or source reference
   ↓
creation time
```

La provenance no implica trust.

```text
Known origin != trusted origin
Trusted origin != true content
True content != authorization
```

Si la provenance necesaria para un caso de riesgo no puede establecerse, el candidato debe poder quedar no elegible para promoción futura.

---

## 7. Scope, dominio y propósito

Un candidato no debe considerarse universal por defecto.

Debe poder expresar límites de aplicabilidad tales como:

```text
subject_scope
conversation_scope
project_scope
domain
purpose
```

Una experiencia válida en un contexto no debe reutilizarse automáticamente en otro.

La admisión futura deberá preservar el principio de mínimo contexto y mínimo alcance.

---

## 8. Validez temporal

La Memory futura debe poder distinguir información vigente de información histórica.

G1 define como requisito conceptual la capacidad de representar:

```text
observed_at
valid_from
valid_until / ttl when applicable
superseded_by
```

No toda memoria necesita expiración automática.

Pero la ausencia de una fecha de expiración no implica validez eterna.

---

## 9. Trust, contradicción y contaminación

Similarity no es trust.

La futura admisión deberá poder separar:

```text
source authority
confidence
content consistency
security trust
applicability
```

Un candidato podrá requerir estados equivalentes a:

```text
UNASSESSED
ELIGIBLE
SUSPECT
TAINTED
SUPERSEDED
REVOKED
REJECTED
```

Los nombres definitivos quedan abiertos a diseño posterior.

### 9.1 Contradicción

Una contradicción no debe resolverse automáticamente por proximidad semántica ni por preferencia del LLM.

Debe poder producir al menos:

```text
hold for review
prefer higher-authority evidence
prefer temporally newer evidence when authority is comparable
retain historical trace
```

### 9.2 Taint

Cuando una fuente, credencial, tool, agent o componente sea posteriormente marcado como comprometido, los candidatos derivados deberán poder reducir su trust sin asumir automáticamente que todo contenido es falso.

```text
source compromised
      ↓
derived candidates marked suspect
      ↓
revalidation required
```

La propagación de distrust no constituye una sentencia de compromiso; constituye una reducción preventiva de trust.

---

## 10. Admission outcomes

G1 no fija todavía una máquina de estados definitiva.

Sí fija que la decisión de admisión futura no debe ser binaria únicamente `store / discard`.

Outcomes conceptuales mínimos:

```text
REJECT
HOLD
ELIGIBLE
```

Con semántica:

### `REJECT`

El candidato no debe promoverse.

Motivos posibles:

- provenance insuficiente para el riesgo;
- contenido fuera de scope;
- policy violation;
- dato sensible no autorizado para persistencia;
- contamination confirmada;
- conflicto no resoluble dentro de la política vigente.

### `HOLD`

El candidato conserva identidad y evidencia suficiente para evaluación, pero no es elegible para persistencia/retrieval productivo.

### `ELIGIBLE`

El candidato superó la política de admisión aplicable.

`ELIGIBLE` no significa persistido.

```text
Eligible != Stored
Stored != Retrieved
Retrieved != Trusted for every task
```

---

## 11. Data classification antes de persistencia

Persistir memoria puede cambiar el riesgo de disclosure.

Antes de una implementación futura debe poder distinguirse, proporcionalmente:

```text
sensitivity
owner / subject
purpose
scope
retention
exportability
remote-model eligibility
redaction needs
consent / human-review requirements
```

Regla:

```text
Having access to data
!=
permission to persist, disclose or reuse it
```

Este diseño no crea todavía un sistema universal de clasificación de datos.

Define solamente el hook necesario para impedir que una futura Memory ignore esa responsabilidad.

---

## 12. Frontera con Knowledge

La unidad actual termina antes de Knowledge.

```text
Experience
   ↓
Episodic Memory Candidate
   ↓
Admission
   ↓
future Episodic Memory

------------------------------ separate boundary

Evidence / stable facts
   ↓
Knowledge Candidate
   ↓
Knowledge Governance
```

Una experiencia repetida no se convierte por frecuencia en conocimiento canónico.

Una memoria episódica tampoco adquiere autoridad de fuente normativa.

Cualquier promoción futura `Memory -> Knowledge candidate` requerirá diseño y autorización independientes.

---

## 13. Frontera con retrieval

Retrieval está fuera de G1.

Sin embargo el diseño preserva una condición futura:

```text
retrieval eligibility
=
content relevance
∩ trust state
∩ scope applicability
∩ temporal validity
∩ policy
```

Por tanto similarity search por sí sola no podrá constituir política suficiente de recuperación.

---

## 14. Negative scenarios obligatorios para una futura implementación

Una eventual implementación deberá demostrar al menos estos escenarios antes de ser admitida:

### EM-A1 — No automatic memory

Un intercambio conversacional exitoso no crea Memory persistente automáticamente.

### EM-A2 — Session binding

Un candidato originado en sesión A no puede aparecer atribuido a sesión B.

### EM-A3 — Provenance preserved

La identidad del candidato conserva binding reconstruible a su origen.

### EM-A4 — LLM cannot self-admit

Contenido generado por el LLM no puede declarar por texto que debe ser almacenado o trusted y obtener ese efecto.

### EM-A5 — Authority separation

Un candidato admitido no concede permisos ni modifica policy.

### EM-A6 — Sensitive data hold/reject

Datos que requieren política de persistencia o revisión humana no pasan automáticamente a elegibilidad.

### EM-A7 — Contradiction does not silently overwrite

Una observación contradictoria no elimina silenciosamente historial previo.

### EM-A8 — Taint propagation

Si el origen es marcado como comprometido, candidatos derivados pueden reducir su trust o requerir revalidación.

### EM-A9 — Revocation

Un candidato o memoria futura puede dejar de ser elegible sin borrar necesariamente la evidencia histórica.

### EM-A10 — Knowledge separation

Admitir una experiencia como memoria episódica no la promueve a Knowledge.

---

## 15. Future implementation budget — no autorizado

G1 no aprueba archivos ni componentes concretos de producción.

Si posteriormente se solicita implementación, el diseño deberá intentar primero un presupuesto mínimo similar a:

```text
contracts / value objects only if necessary
pure deterministic admission policy if necessary
in-memory test doubles only
no persistence
no retrieval
no Kernel change
no external dependency
```

La implementación deberá preferir funciones/contratos pequeños antes que introducir:

```text
MemoryManager
TrustManager
AdmissionEngine
KnowledgeManager
UniversalContextManager
```

Estos nombres no están aprobados y representan ejemplos de sobrearquitectura a evitar.

---

## 16. Stop conditions

G1 concluye `INCONCLUSIVE` y debe volver al propietario si para obtener utilidad mínima resulta necesario:

- elegir una base de datos;
- elegir un vector store;
- introducir embeddings;
- implementar retrieval;
- fusionar Memory y Knowledge;
- crear un subsystem universal de trust;
- modificar Kernel;
- modificar Security Control Plane;
- introducir agents o tools;
- interpretar contenido del LLM como decisión de admisión;
- crear autoridad automática downstream.

Regla:

> Si el diseño necesita construir la Memory para poder definir la frontera de admisión, el alcance está mal cortado.

---

## 17. Disposición G1

Con el alcance actual:

```text
G1 DESIGN RESULT: PASS
blocking design findings: 0
implementation authorization: false
persistent Memory authorization: false
Knowledge implementation authorization: false
Sprint 7.12 authorization: false
RDD Stage 2 authorization: false
```

La unidad es diseñable sin storage, retrieval, Knowledge, agents ni cambios de autoridad.

El siguiente gate, si el propietario lo autoriza explícitamente, deberá convertir estas propiedades en una **Implementation Candidate Specification mínima**, todavía separada de la ejecución de cambios productivos.

No existe autorización automática para continuar.
