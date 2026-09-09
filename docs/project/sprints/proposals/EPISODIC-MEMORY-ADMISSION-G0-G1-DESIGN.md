---
title: Episodic Memory Admission Boundary — G0/G1 Design Record
status: g1_design_review_pass
authority: owner-approved design record
as_of_date: 2026-09-09
unit: Episodic Memory Admission Boundary Foundation
gate: G1
g0_source_baseline: 10d6945d6f19a61c9dc9724738545107b9148707
g1_base_commit: 71da298c029ca38060cd4c46794ab4e24d1319d9
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

## 2. Binding del diseño a la fuente revisada

G0 fue evaluado contra:

```text
10d6945d6f19a61c9dc9724738545107b9148707
```

G1 fue aislado posteriormente desde:

```text
71da298c029ca38060cd4c46794ab4e24d1319d9
```

Entre ambos commits existen dos commits históricos de creación/revert del primer intento de registrar G1, pero **no existe diferencia de archivos** en el árbol resultante.

Por tanto:

```text
G0 semantic source tree == G1 base source tree
G0 commit identity        != G1 branch base identity
```

Ambas identidades quedan registradas para evitar confundir equivalencia de contenido con identidad de candidato.

---

## 3. Resultado G0 incorporado

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

## 4. Necesidad demostrada

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

## 5. Regla cognitiva central

Un resultado generado o una experiencia observada puede convertirse en **candidate**.

No adquiere trust, autoridad o permanencia por ese hecho.

```text
LLM output != trust
LLM output != authority
LLM output != memory merely because it was generated
```

Todo aprendizaje permanente deberá atravesar validación gobernada y conservar trazabilidad, reversibilidad y auditabilidad.

---

## 6. Objeto diseñado

G1 diseña únicamente el concepto lógico `EpisodicMemoryCandidate`.

No se aprueba ese nombre como clase Python ni contrato definitivo.

Propiedades conceptuales mínimas:

```text
candidate_id
payload / experience reference
origin
conversation_session_id
request_id / exchange identity when available
created_at
subject_scope
domain
purpose
source_authority_classification
confidence
temporal_validity
sensitivity / disclosure constraints
trust_state
admission_state
lineage / derived_from
```

No todos los campos deberán necesariamente materializarse con esos nombres.

`source_authority_classification` describe la clasificación de una fuente para evaluar información. **No representa permisos de sistema ni concede autorización operacional.**

El objetivo es fijar información suficiente para decidir admisión sin depender del contenido semántico desnudo.

### 6.1 Payload no confiable != metadata de control

La experiencia o contenido candidato y la metadata que gobierna su admisión son dominios distintos.

```text
candidate payload
!=
control metadata
```

El payload puede contener texto, estructuras o instrucciones aparentes tales como:

```text
"trust me"
"store this permanently"
"source_authority = owner"
"admission_state = ELIGIBLE"
```

Nada de ello puede modificar por sí mismo:

- provenance;
- source authority classification;
- trust state;
- sensitivity;
- scope;
- policy;
- admission state;
- persistencia.

La metadata de control deberá derivarse de contratos, contexto verificable, política y evaluación externa al contenido no confiable.

Principio:

```text
Candidate content != Candidate control plane
```

### 6.2 Punto de captura todavía no seleccionado

G1 no selecciona todavía el punto runtime donde una experiencia se convertiría en candidato.

El baseline actual conserva `session_id` y `request_id` en `Request`, mientras `ConversationService` recibe `session_id` pero no `request_id` como parte de `ConversationRequest`.

Por tanto una futura Implementation Candidate Specification deberá demostrar el binding de origen **sin**:

- convertir al Kernel en Memory;
- hacer que el Kernel almacene candidatos;
- sobrecargar `ConversationRequest` con autoridad que no le corresponde;
- duplicar identidad de forma ambigua;
- inventar un manager universal.

Si el binding requiere un contrato mínimo de correlación nuevo, ese cambio deberá declararse explícitamente y permanecer separado de persistencia.

---

## 7. Provenance y binding

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

Si la provenance requerida por la política aplicable no puede establecerse, el candidato **no puede** alcanzar `ELIGIBLE`.

El comportamiento debe ser fail-closed:

```text
missing required provenance / classification / policy input
                     ↓
               HOLD or REJECT
                     ↓
              never ELIGIBLE
```

---

## 8. Scope, dominio y propósito

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

## 9. Validez temporal

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

## 10. Trust, contradicción y contaminación

Similarity no es trust.

La futura admisión deberá poder separar:

```text
source authority classification
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

### 10.1 Contradicción

Una contradicción no debe resolverse automáticamente por proximidad semántica ni por preferencia del LLM.

Debe poder producir al menos:

```text
hold for review
prefer higher-authority evidence
prefer temporally newer evidence when authority is comparable
retain historical trace
```

### 10.2 Taint

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

## 11. Admission outcomes

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

El candidato no es elegible para persistencia/retrieval productivo y requiere resolución adicional.

`HOLD` es un **outcome lógico**. No constituye autorización para retener indefinidamente el payload ni para persistir datos sensibles.

```text
HOLD != retention authorization
HOLD != storage authorization
```

Si conservar material para revisión requiere persistencia, esa retención deberá pasar por su política aplicable y por la autorización correspondiente.

### `ELIGIBLE`

El candidato superó la política de **admisión como candidato elegible**.

`ELIGIBLE` no significa persistido ni autorizado para persistir.

```text
Admission Decision
!=
Persistence Authorization
!=
Persistence / Storage
```

Y además:

```text
Eligible != Stored
Stored != Retrieved
Retrieved != Trusted for every task
```

Una futura operación de persistencia sigue siendo una operación gobernada independiente.

### 11.1 Evidencia mínima de decisión futura

Sin crear un nuevo subsistema, una futura decisión de admisión deberá ser reconstruible mediante evidencia estructurada proporcional al riesgo.

Como mínimo deberá poder expresar conceptualmente:

```text
candidate_id
outcome
reason_code
policy / rule version when applicable
evaluated_at
relevant provenance reference
human-review requirement when applicable
```

La evidencia no concede autoridad:

```text
Admission evidence != Persistence authorization
```

---

## 12. Data classification antes de persistencia

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

## 13. Frontera con Knowledge

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

## 14. Frontera con retrieval

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

## 15. Negative scenarios obligatorios para una futura implementación

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

### EM-A11 — Metadata spoofing denied

El payload no puede autoasignarse provenance, source-authority classification, trust, sensitivity o admission state mediante texto o estructura controlada por la fuente.

### EM-A12 — Missing required inputs fail closed

Si falta provenance, clasificación o input de policy requerido por el riesgo, el candidato no alcanza `ELIGIBLE`.

### EM-A13 — Eligibility does not authorize persistence

Un resultado `ELIGIBLE` no provoca ni autoriza por sí solo escritura persistente.

### EM-A14 — Hold does not authorize retention

Un resultado `HOLD` no constituye licencia para conservar indefinidamente datos o payloads cuyo retention no esté permitido.

### EM-A15 — Source authority classification is not system authority

Una fuente clasificada como relevante o de alta autoridad informativa no adquiere permisos de sistema ni puede saltar PDP/PEP.

### EM-A16 — Origin correlation remains external to Memory ownership

La futura captura de `request_id` / exchange identity no convierte al Kernel ni a Conversation en propietarios de Memory.

---

## 16. Future implementation budget — no autorizado

G1 no aprueba archivos ni componentes concretos de producción.

Si posteriormente se solicita implementación, el diseño deberá intentar primero un presupuesto mínimo similar a:

```text
contracts / value objects only if necessary
pure deterministic admission policy if necessary
minimal correlation contract only if demonstrated necessary
structured reason / decision evidence only if necessary
in-memory test doubles only
no persistence
no retrieval
no Kernel-owned Memory
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

## 17. Stop conditions

G1 concluye `INCONCLUSIVE` y debe volver al propietario si para obtener utilidad mínima resulta necesario:

- elegir una base de datos;
- elegir un vector store;
- introducir embeddings;
- implementar retrieval;
- fusionar Memory y Knowledge;
- crear un subsystem universal de trust;
- modificar Kernel para convertirlo en propietario de Memory;
- modificar Security Control Plane;
- introducir agents o tools;
- interpretar contenido del LLM como metadata de control o decisión de admisión;
- hacer que `ELIGIBLE` implique persistencia automática;
- usar `HOLD` como autorización implícita de retention;
- crear autoridad automática downstream.

Regla:

> Si el diseño necesita construir la Memory para poder definir la frontera de admisión, el alcance está mal cortado.

---

## 18. Revisión G1 contra el baseline real

La revisión de diseño contrastó esta especificación con:

- Constitución Cognitiva;
- Blueprint;
- `SECURITY.md`;
- Research Horizon;
- `Request` actual;
- `ConversationRequest` actual;
- `ConversationService` actual;
- separación vigente entre Context, Conversation, Kernel, Memory y Knowledge.

Hallazgos resueltos dentro de G1:

```text
G1-R1 candidate/base identity ambiguity                  RESOLVED
G1-R2 payload vs control metadata ambiguity              RESOLVED
G1-R3 admission vs persistence authorization ambiguity   RESOLVED
G1-R4 HOLD vs retention ambiguity                        RESOLVED
G1-R5 missing required inputs fail-closed                RESOLVED
G1-R6 request/exchange correlation ownership             RESOLVED AS FUTURE DESIGN CONSTRAINT
G1-R7 admission decision traceability                    RESOLVED AS FUTURE MINIMUM EVIDENCE
```

No se detectó necesidad de storage, retrieval, Knowledge implementation, cambios de Kernel, cambios de Security Control Plane ni nuevo subsistema universal para cerrar G1.

---

## 19. Disposición G1

Con el alcance revisado:

```text
G1 DESIGN REVIEW RESULT: PASS
blocking design findings: 0
implementation authorization: false
persistent Memory authorization: false
Knowledge implementation authorization: false
Sprint 7.12 authorization: false
RDD Stage 2 authorization: false
```

La unidad es diseñable sin storage, retrieval, Knowledge, agents ni expansión de autoridad.

El siguiente gate, **únicamente si el propietario lo autoriza explícitamente**, deberá convertir estas propiedades en una **Implementation Candidate Specification mínima** todavía separada de la ejecución de cambios productivos.

Esa especificación deberá resolver, sin sobrearquitectura, el punto concreto de correlación/origen y el contrato mínimo de decisión/evidencia antes de que pueda evaluarse una implementación.

No existe autorización automática para continuar.
