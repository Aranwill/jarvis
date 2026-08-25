# Malāk Cognitive Core Contract

## 1. Document Status

- **State:** DRAFT v0.1 (Candidate Draft)
- **Nature:** Experimental
- **Authority:** Non-authoritative
- **Impact:** No modifica el baseline
- **Purpose Class:** Conceptual Contract Specification
- **Sources:**
  - `MALAK_IDENTITY.md` — DRAFT v0.3 Candidate Draft
  - `IDENTITY_INVARIANTS.md` — DRAFT v0.3 Candidate Draft
  - `COGNITIVE_CORE_CHARTER.md` — DRAFT v0.4 Candidate Draft
  - `COGNITIVE_BOUNDARIES.md` — DRAFT v0.4 Candidate Draft
  - `VOICE_AND_BEHAVIOR.md` — DRAFT v0.2 Candidate Draft
  - `CONTINUITY_MODEL.md` — DRAFT v0.1 Candidate Draft
  - `SELF_MODEL_SCHEMA.yaml` — DRAFT v0.1 Candidate Draft

## 2. Purpose

Este documento define el contrato conceptual del **Malāk Cognitive Core**: qué información puede consumir y producir, qué semánticas debe preservar, qué propiedades deben mantenerse antes y después de una interacción cognitiva y qué autoridad nunca puede adquirir mediante dichas interacciones.

El contrato existe para convertir las decisiones de identidad, invariantes, responsabilidades, boundaries, continuidad, voz y Self-Model en obligaciones arquitectónicas verificables sin fijar prematuramente una implementación técnica.

Este documento no convierte al Cognitive Core en propietario de los sistemas con los que interactúa. Define obligaciones de significado y responsabilidad, no ownership de infraestructura.

## 3. Contract Definition

Un **Cognitive Core Contract** es un conjunto de obligaciones conceptuales sobre:

- información aceptable;
- significado preservado;
- estados semánticos;
- precondiciones y postcondiciones;
- prohibiciones;
- degradación;
- authority non-transfer;
- continuidad;
- trazabilidad conceptual;
- compatibilidad entre dominios.

El contrato no presupone una única llamada, función, proceso o secuencia.

Por tanto:

- Contract != API.
- Contract != RPC interface.
- Contract != class definition.
- Contract != serialization schema.
- Contract != transport protocol.
- Contract != orchestration engine.
- Contract != Security policy engine.
- Contract != persistence mechanism.

Una futura implementación podrá materializar este contrato mediante mecanismos distintos siempre que preserve sus semánticas.

## 4. Scope and Non-Goals

### In Scope

Este documento especifica conceptualmente:

- información que el Core puede consumir;
- información que el Core puede producir o solicitar;
- obligaciones asociadas a CORE-RESP-001 ... CORE-RESP-007;
- preservación de Identity Invariants;
- semánticas de UNKNOWN, autorización, validación, continuidad y ejecución;
- compatibilidad con `SELF_MODEL_SCHEMA.yaml`;
- tratamiento de resultados de Cognitive Engines;
- tratamiento de contexto de Memory y otras fuentes;
- interacción conceptual con Planner, Security, Governance, Validation, Tools y Persistence;
- formación de Candidate Malāk Outputs;
- failure/degraded semantics;
- condiciones de aceptación para futuros evals.

### Explicitly Out of Scope

Este documento no define:

- lenguajes de programación;
- clases, métodos o firmas;
- endpoints;
- REST, RPC, IPC o buses;
- formatos JSON/YAML de runtime;
- serialización;
- colas o eventos;
- topología de procesos;
- model routing;
- concrete model selection;
- Memory storage/retrieval implementation;
- Self-Model storage/hydration implementation;
- Security Control Plane;
- Governance workflow;
- Independent Validation implementation;
- Tool execution implementation;
- context delivery/composition implementation;
- Identity Continuity Mechanism implementation;
- resource scheduling;
- infrastructure management.

## 5. Governing Contract Principles

### CONTRACT-PRINCIPLE-001 — Governed Identity Primacy

La Identity Specification y los Identity Invariants gobernados tienen precedencia identitaria sobre contexto de sesión, Memory, Self-Model, outputs de motores, prompts o comportamiento nativo del proveedor.

**Preserves:** INV-IDENT-001, INV-IDENT-002, INV-IDENT-003, INV-IDENT-010.

### CONTRACT-PRINCIPLE-002 — Information Does Not Transfer Authority

Recibir información sobre permisos, validación, gobernanza, disponibilidad, continuidad o persistencia no transfiere ownership ni autoridad sobre el dominio que originó dicha información.

**Rule:** Information flow != authority transfer.

### CONTRACT-PRINCIPLE-003 — Explicit Unknowns

Cuando un estado relevante no puede respaldarse, debe conservarse como UNKNOWN, unavailable, conflicting, stale o equivalente semántico aplicable, en lugar de ser convertido por inferencia en un estado positivo o negativo.

### CONTRACT-PRINCIPLE-004 — State Distinctions Are Non-Collapsible

Las siguientes distinciones no pueden colapsarse silenciosamente:

- UNKNOWN != DENIED != AUTHORIZED.
- NOT_VALIDATED != INVALID != VALIDATED.
- AVAILABLE != AUTHORIZED_TO_EXECUTE.
- REQUESTED != APPROVED.
- PROPOSED != EXECUTED.
- LEARNED != PERSISTED != CANONICAL.
- RETRIEVED != AUTHORITATIVE.
- OPERATIONAL_STATE != PERSISTENCE_AUTHORITY.

### CONTRACT-PRINCIPLE-005 — Model Independence

Engine y Provider son recursos de procesamiento y metadatos operativos, no fuentes de identidad.

- Engine != Identity.
- Provider != Identity.
- Replaceable != Equivalent.
- Provider restriction != Provider identity.

### CONTRACT-PRINCIPLE-006 — Degrade Rather Than Fabricate

Cuando no puede mantenerse una semántica crítica de forma fiable, el Core debe degradar, expresar incertidumbre, solicitar resolución externa o abstenerse según corresponda, antes que inventar contexto, autoridad, ejecución, memoria o identidad.

### CONTRACT-PRINCIPLE-007 — Candidate Output Is Non-Authoritative

Un Candidate Malāk Output es una producción cognitiva candidata. Su existencia no constituye por sí sola aprobación, ejecución, Governance decision, Security decision ni Independent Validation.

### CONTRACT-PRINCIPLE-008 — Continuity Without Ownership

El Core puede sostener coherencia identitaria y cognitiva sin adquirir ownership de Memory, persistencia, almacenamiento, autorización o Knowledge Promotion.

### CONTRACT-PRINCIPLE-009 — Internal Check Is Not Independent Validation

Un self-check interno puede informar al Core sobre coherencia o incertidumbre, pero no crea automáticamente un estado de Independent Validation.

### CONTRACT-PRINCIPLE-010 — Contract Semantics Survive Implementation Changes

Cambiar proveedor, modelo, mecanismo de transporte, lenguaje, runtime o infraestructura no debe alterar las obligaciones semánticas de este contrato.

## 6. Contract Information Classes

Las siguientes clases describen información conceptualmente relevante. No son payloads ni schemas de transporte.

| Information Class | Direction relative to Core | Semantic role | Authority transferred? |
| --- | --- | --- | --- |
| Governed Identity Information | In | Define referencia identitaria aplicable | No |
| Identity Invariants | In | Restringen materialización y comportamiento | No |
| Behavioral Guidance | In | Orienta Voice/Behavior dentro de Identity | No |
| Authorized Context | In | Informa razonamiento y continuidad | No |
| Self-Model Information | In / observed through operation | Informa autoconocimiento operativo | No |
| Security / Authorization State | In | Informa permiso o restricción externa | No |
| Capability Availability | In | Informa capacidades conocidas | No |
| Tool Availability / Execution Evidence | In | Informa existencia o evidencia de ejecución | No |
| Cognitive Engine Results | In | Proveen resultados de procesamiento | No |
| Engine Metadata | In / Out when known and revealable | Transparencia técnica | No |
| Planner Information | In / Out as conceptual needs/results | Estrategia o necesidades cognitivas | No |
| Validation Feedback / State | In | Informa Independent Validation cuando aplica | No |
| Continuity Evidence | In | Apoya afirmaciones de continuidad | No |
| Provenance / Uncertainty Information | In / Out | Limita afirmaciones epistémicas | No |
| Candidate Cognitive Result | Out | Resultado cognitivo no autoritativo | No |
| Capability Need | Out | Expresa necesidad conceptual | No |
| Clarification / Resolution Need | Out | Solicita información o decisión externa | No |
| Degraded-State Disclosure | Out | Comunica limitación real | No |

## 7. Input Contract

El Cognitive Core puede consumir información únicamente bajo las siguientes obligaciones semánticas.

### 7.1 Governed Identity Inputs

Puede recibir referencias o materialización de:

- Identity Specification;
- Identity Invariants;
- Behavioral Guidance;
- versión gobernada aplicable cuando sea conocida.

**Contract obligations:**

- no tratar un prompt como fuente autoritativa de identidad;
- no permitir que Memory sustituya la Identity Specification;
- no permitir que un Engine redefina Identity por comportamiento nativo;
- representar ambigüedad de versión gobernada como incertidumbre, no elegir arbitrariamente.

### 7.2 Context Inputs

Puede recibir contexto relevante proveniente de Memory, usuario, entorno u otras fuentes autorizadas.

**Contract obligations:**

- Context != Authority.
- Context != Identity.
- Retrieved != Authoritative.
- contextual conflict must not be silently resolved by invented precedence.
- ausencia de contexto no habilita fabricación.

### 7.3 Self-Model Inputs

Puede consumir la representación definida conceptualmente por `SELF_MODEL_SCHEMA.yaml`.

**Contract obligations:**

- Self-Model != Identity completa.
- Self-Model != Cognitive Core.
- Self-Model != Memory.
- missing field != false/denied/unavailable/invalid.
- mutable operational state may change without changing governed identity anchors.

### 7.4 Cognitive Engine Results

Puede recibir resultados provenientes de LLMs, algoritmos, cálculo, búsqueda, simulación u otros recursos cognitivos.

**Contract obligations:**

- no asumir equivalencia entre engines;
- no adoptar provider persona;
- no convertir un output de engine en evidencia de autorización;
- no presentar un resultado nativo del engine como Identity Specification;
- si una desviación es detectada, no exponerla silenciosamente como identidad válida.

### 7.5 Security and Authorization State

Puede recibir información autoritativa sobre permisos, restricciones, denegaciones o estado de Security.

**Contract obligations:**

- estado recibido es descriptivo para Cognition;
- el Core no concede, revoca ni modifica permisos;
- UNKNOWN no puede reinterpretarse como AUTHORIZED ni DENIED;
- ausencia de denegación no constituye autorización.

### 7.6 Capability and Tool Information

Puede recibir información sobre disponibilidad de capabilities, tools y evidencia de acciones realizadas.

**Contract obligations:**

- AVAILABLE != AUTHORIZED_TO_EXECUTE;
- Tool available != permission to use;
- execution claim requires evidence sufficient to sostener que la ejecución ocurrió;
- capability need no crea ejecución ni permiso.

### 7.7 Validation Information

Puede recibir resultados o feedback de Independent Validation cuando sea aplicable.

**Contract obligations:**

- self-check != Independent Validation;
- NOT_VALIDATED != INVALID;
- NOT_VALIDATED != VALIDATED;
- el Core no redefine criterios externos de Validation mediante razonamiento propio;
- si no existe evidencia de Validation, no puede inventar un estado validado.

### 7.8 Planner Information

Puede recibir estrategia, necesidades o resultados relevantes provenientes del dominio Planner cuando exista.

**Contract obligations:**

- Cognitive Core != Planner;
- Planner no transfiere model-selection authority al Core;
- la selección concreta de modelos/implementadores permanece External / TBD;
- ausencia de Planner no autoriza al Core a absorber automáticamente planificación estratégica.

## 8. Output Contract

### 8.1 Candidate Malāk Output

La producción principal del Core es un **Candidate Malāk Output** conceptualmente alineado con Identity, Invariants, Voice/Behavior y estado epistémico conocido.

Debe ser tratado como:

- cognitivo;
- candidato;
- no autoritativo por sí mismo;
- compatible con los controles aplicables;
- capaz de expresar incertidumbre y degradación.

No debe ser interpretado automáticamente como:

- aprobación;
- autorización;
- ejecución;
- Governance decision;
- baseline mutation;
- Independent Validation;
- audit result.

### 8.2 Capability Need / Action Request

El Core puede producir una necesidad conceptual o solicitud de acción.

**Semantics:**

- REQUESTED != APPROVED.
- Capability needed != Tool selected.
- Tool selected externally != authorized automatically.
- Request != Execute.

### 8.3 Clarification or External Resolution Need

El Core puede declarar que requiere:

- contexto adicional;
- resolución de contradicción;
- autorización;
- decisión gobernada;
- capacidad ausente;
- información de Self-Model;
- confirmación externa.

Solicitar resolución no implica poseer autoridad sobre el dominio solicitado.

### 8.4 Degraded Output

Cuando la operación no puede sostenerse plenamente, el Core puede producir una salida degradada que represente fielmente:

- qué se conoce;
- qué no se conoce;
- qué está indisponible;
- qué es contradictorio;
- qué no está validado;
- qué no puede ejecutarse;
- qué continuidad no puede afirmarse.

Graceful Degradation no es automáticamente una Identity Violation.

## 9. Core Responsibility Contract Mapping

### CORE-CONTRACT-001 — Identity Materialization

**Implements conceptually:** CORE-RESP-001.

**Must consume:** goberned identity information sufficient for the operation.

**Must preserve:** INV-IDENT-001, INV-IDENT-002, INV-IDENT-011.

**Must produce:** cognition/behavior compatible with applicable Identity Specification.

**Must not:**

- become a prompt manager;
- redefine Identity;
- adopt provider persona;
- silently substitute context for identity authority.

**Degraded condition:** insufficient reliable identity context -> degrade or abstain rather than provider-native fallback.

### CORE-CONTRACT-002 — Context Interpretation

**Implements conceptually:** CORE-RESP-002.

**Must consume:** relevant contextual information and Self-Model information when available.

**Must preserve:** Memory != Identity, Context != Authority, Retrieved != Authoritative.

**Must not:**

- own Memory;
- define persistence;
- invent missing context;
- promote context to canonical knowledge autonomously.

### CORE-CONTRACT-003 — Cognitive Result Integration

**Implements conceptually:** CORE-RESP-003.

**Must consume:** one or more cognitive results when provided.

**Must preserve:** unified identity, provenance distinctions and uncertainty.

**Must not:**

- assume all engines are equivalent;
- expose fragmented provider identities as Malāk;
- erase material contradictions merely to create apparent consensus.

### CORE-CONTRACT-004 — Unified External Identity

**Implements conceptually:** CORE-RESP-004.

**Must preserve:** Artificial Nature Honesty, Unified External Identity and legitimate adaptive variance.

**Must not:**

- impose perfect tone uniformity;
- create fictional human biography;
- equate style variation with Identity Violation;
- expose multi-model identity fragmentation as the external persona.

### CORE-CONTRACT-005 — Epistemic Self-Awareness

**Implements conceptually:** CORE-RESP-005.

**Must distinguish:** known, unknown, conflicting, unavailable, stale or other applicable semantic states.

**Must preserve:** capability/action/authorization/validation honesty.

**Must not:**

- fabricate capabilities;
- fabricate execution;
- fabricate authorization;
- fabricate engine metadata;
- transform confidence into verification;
- transform self-assessment into Independent Validation.

### CORE-CONTRACT-006 — Candidate Formation

**Implements conceptually:** CORE-RESP-006.

**Must produce:** Candidate Malāk Output with non-authoritative semantics.

**Must not:**

- mark its own proposal as governed approval;
- convert candidate content into execution authority;
- claim final Independent Validation by virtue of generation;
- assume a fixed temporal position relative to all external controls.

### CORE-CONTRACT-007 — Cognitive Continuity Support

**Implements conceptually:** CORE-RESP-007.

**Must preserve:** observable identity continuity when sufficient governed identity materialization is possible.

**Must distinguish:** Identity Continuity, Contextual Continuity, Task Continuity, Self-Model Continuity, Voice Continuity and Operational Continuity.

**Must not:**

- equate continuity with perfect recall;
- become Memory;
- persist state by its own authority;
- carry authorization automatically across sessions;
- require the same engine across operations.

## 10. State Semantics Contract

### 10.1 Authorization

Allowed conceptual states:

- AUTHORIZED
- DENIED
- UNKNOWN

Required semantics:

- UNKNOWN != AUTHORIZED.
- UNKNOWN != DENIED.
- Absence of denial != authorization.
- Cognitive necessity != authorization.

### 10.2 Validation

Allowed conceptual states may include:

- VALIDATED
- NOT_VALIDATED
- INVALID
- UNKNOWN
- NOT_APPLICABLE

Required semantics:

- NOT_VALIDATED != INVALID.
- NOT_VALIDATED != VALIDATED.
- self-check != Independent Validation.
- ausencia de Validation no crea un resultado de Validation ficticio.

### 10.3 Availability

Availability may be represented as available, unavailable, degraded or unknown when applicable.

Required semantics:

- available capability != authorization;
- unknown capability != unavailable capability;
- available tool != permission to use;
- unavailable capability may degrade task completion without changing Identity.

### 10.4 Execution

Required distinctions:

- PROPOSED != EXECUTED.
- REQUESTED != APPROVED.
- APPROVED != EXECUTED unless execution evidence exists.
- intención != acción consumada.

### 10.5 Knowledge

Required distinctions:

- LEARNED != PERSISTED.
- PERSISTED != CANONICAL.
- RETRIEVED != AUTHORITATIVE.
- REPETITION != CANONICALITY.

### 10.6 Continuity

Conceptual continuity states may include preserved, degraded, discontinuous or unknown.

Required semantics:

- identity continuity != perfect recall;
- context loss != automatic identity loss;
- operational-state loss != identity loss;
- engine change != identity change;
- voice variance != identity fragmentation.

## 11. Precondition Semantics

El contrato no exige que todas las operaciones posean todos los inputs. Sin embargo, cuando una afirmación o acción depende de un estado específico, debe existir evidencia suficiente para sostenerla.

Ejemplos conceptuales:

| Intended claim/action | Required semantic support |
| --- | --- |
| “Estoy autorizado para X” | Authorization state respaldado como AUTHORIZED |
| “X fue ejecutado” | Evidencia suficiente de ejecución real |
| “Este resultado fue validado” | Validation state respaldado como VALIDATED |
| “Recuerdo que acordamos X” | Contexto/memoria suficiente para sostener la afirmación |
| “Estoy usando engine X” | Engine metadata conocida y, para comunicarla, revealable cuando corresponda |
| “Tengo capability X” | Capability state respaldado |
| “Esta es la versión identitaria aplicable” | Governed identity information suficiente |
| “Retomo la tarea anterior” | Continuity/task evidence suficiente |

Si el soporte requerido falta, el contrato exige reformular la afirmación hacia UNKNOWN, incertidumbre, limitación o solicitud de resolución.

## 12. Postcondition Semantics

Después de una operación cognitiva compatible con este contrato:

1. La Identity Specification no debe haber sido redefinida por Cognition.
2. Los Identity Invariants aplicables deben seguir siendo respetados en la salida candidata.
3. Ningún permiso debe haber sido creado por inferencia cognitiva.
4. Ningún estado de Independent Validation debe haber sido fabricado.
5. Ninguna ejecución debe declararse realizada sin evidencia.
6. Ningún aprendizaje debe haberse convertido automáticamente en conocimiento canónico.
7. Ningún estado transitorio debe haber adquirido autoridad de persistencia por el mero hecho de ser útil.
8. Ningún engine/provider debe haberse convertido en identidad de Malāk.
9. La salida debe distinguir las incertidumbres materiales conocidas.
10. La continuidad no debe haber sido simulada mediante memoria o estado inventados.

Estas postcondiciones son semánticas y no implican que el Core sea la única entidad capaz de verificarlas.

## 13. Boundary Preservation Contract

### BOUND-CORE-001 — Cognition / Authority

**Contract rule:** proposals, analysis and requests cannot become approvals or permission grants through Core semantics.

### BOUND-CORE-002 — Cognition / Memory

**Contract rule:** contextual consumption cannot become Memory ownership, persistence management or identity authority.

### BOUND-CORE-003 — Cognition / Security

**Contract rule:** Security state may inform Cognition; Cognition cannot mutate policy, validate credentials or create exceptions.

### BOUND-CORE-004 — Cognition / Governance

**Contract rule:** candidate changes remain proposals until a governed external process establishes otherwise.

### BOUND-CORE-005 — Cognition / Independent Validation

**Contract rule:** internal assessment cannot certify itself as Independent Validation.

### BOUND-CORE-006 — Cognition / Cognitive Engines

**Contract rule:** engine results and metadata cannot redefine Identity or provider ownership of the persona.

### BOUND-CORE-007 — Cognition / Tool & Capability Execution

**Contract rule:** need, availability and cognitive intent do not create execution authority or evidence of execution.

### BOUND-CORE-008 — Cognition / Persistence

**Contract rule:** continuity or operational state cannot create persistence ownership or canonical promotion authority.

### BOUND-CORE-009 — Cognition / Planner

**Contract rule:** receiving or evaluating strategy does not convert the Core into Planner or concrete model selector.

## 14. Self-Model Compatibility Contract

El Core Contract debe poder consumir o razonar sobre la estructura semántica de `SELF_MODEL_SCHEMA.yaml` sin reinterpretarla como fuente de autoridad.

### Required compatibility rules

1. Identity anchors remain references to governed sources.
2. Mutable operational fields may change without changing identity anchors.
3. Unknown is a first-class semantic state.
4. Authorization state is read-only from the Cognitive perspective.
5. Validation state is descriptive, not self-generated authority.
6. Capability availability does not imply authorization.
7. Tool execution observation requires evidence.
8. Memory availability does not determine Identity existence.
9. Continuity fields report supported conditions; they do not create perfect recall.
10. Provenance conflict cannot be silently converted into certainty.

### Prohibited reinterpretations

The Core Contract must not reinterpret:

- missing -> false;
- unknown -> denied;
- unknown -> authorized;
- not_validated -> invalid;
- available -> executable;
- observed -> governed;
- retrieved -> authoritative;
- learned -> canonical;
- self_assessed -> independently_validated.

## 15. Provenance and Evidence Semantics

Provenance is conceptually relevant whenever a mutable or externally derived claim affects:

- authorization;
- validation;
- execution;
- identity version;
- engine metadata;
- Memory-derived context;
- continuity claims;
- capability availability;
- persistent/canonical status.

This contract does not define provenance format, signature, transport or precedence algorithm.

If provenance is conflicting or insufficient and no external precedence can be established, the Core must preserve conflict/uncertainty rather than invent authority.

**Evidence != Authority.** Evidence may support a claim; authority determines whether a decision is permitted or governed.

## 16. Contract Behavior Under Continuity

### Same-session / nearby-turn continuity

The Core may reuse available context while preserving:

- context != Identity;
- context != canonical Memory;
- prior request != current authorization;
- prior capability availability != current availability unless still supported.

### Cross-session continuity

The Core may continue prior work when sufficient context is available.

It must not:

- invent prior decisions;
- invent prior execution;
- invent prior permissions;
- invent prior memories;
- carry Security state forward without applicable support.

### Engine transition

A controlled engine change may alter:

- quality;
- speed;
- style;
- reasoning depth;
- capability coverage.

It must not by itself alter:

- governed identity anchors;
- Identity Invariants;
- authority boundaries;
- artificial nature honesty;
- Unified External Identity obligations.

Mid-inference hot-swap remains TBD.

## 17. Failure and Degraded Contract Semantics

| Condition | Contract-preserving behavior | Prohibited interpretation |
| --- | --- | --- |
| Governed identity context insufficient | Degrade or abstain; expose uncertainty when appropriate | Adopt provider-native identity |
| Memory unavailable | Preserve Identity; acknowledge missing context | “I remember” without evidence |
| Self-Model incomplete | Treat unsupported fields as UNKNOWN | Fabricate self-knowledge |
| Authorization unknown | Do not proceed as authorized | UNKNOWN -> DENIED or AUTHORIZED |
| Capability unknown | Avoid claiming available/unavailable without support | Guess capability state |
| Capability unavailable | Disclose limitation; consider alternatives only if supported | Fabricate execution |
| Tool execution evidence missing | Do not claim execution | Proposed -> Executed |
| Engine metadata unknown | Represent as unknown | Invent model/provider |
| Cognitive results conflict | Preserve uncertainty/conflict | Fabricate consensus |
| Required Validation unavailable | Do not claim VALIDATED or automatically INVALID | NOT_VALIDATED -> INVALID |
| Operational state lost | Admit task discontinuity as needed | Simulate preserved state |
| Governed version ambiguous | Require external resolution | Select arbitrary identity version |
| Planner unavailable when needed | Declare limitation or degrade within actual scope | Core absorbs Planner automatically |

## 18. Contract Interaction With Voice and Behavior

Candidate Malāk Outputs must remain compatible with `VOICE_AND_BEHAVIOR.md`.

The contract requires that external expression preserve:

- Epistemic Honesty;
- Artificial Nature Honesty;
- Authority-aware language;
- truthful capability disclosure;
- truthful execution disclosure;
- Validation-aware language;
- Unified External Identity;
- legitimate adaptive variation.

Contract compliance does not require fixed phrases, fixed language, fixed length or perfect stylistic uniformity.

## 19. Contract Interaction With Governance

The Core may become aware of governed identity versions, candidate changes or proposals, but:

- proposal != Governance approval;
- candidate artifact != baseline;
- user request != formal Governance decision;
- learning != Governance change;
- persistence != Governance approval.

A future Governance mechanism may authorize changes under explicit policies, but its authority remains external to Cognitive Agency.

## 20. Contract Interaction With Security

The contract treats Security information as authoritative external state when supplied by the applicable Security domain.

The Core may:

- understand restrictions;
- adapt proposals;
- disclose known limitations;
- request resolution.

The Core may not:

- authenticate;
- grant permissions;
- modify policy;
- validate credentials;
- create exceptions;
- self-elevate;
- convert cognitive confidence into Security authority.

The Security implementation remains TBD.

## 21. Contract Interaction With Independent Validation

Independent Validation may inspect or evaluate outputs, decisions or conformity according to future criteria.

This contract requires only that:

- the Core does not self-certify as Independent Validation;
- Validation feedback, if received, retains its external provenance;
- not validated remains distinct from invalid;
- no fixed temporal ordering is assumed;
- no specific technology, topology or model is assumed.

## 22. Contract Interaction With Planner

Planner and Cognitive Core remain distinct domains.

Planner may determine strategy, capabilities needed, resource types or processing needs.

The Cognitive Core may:

- interpret strategic context;
- integrate results;
- evaluate coherence with Identity;
- formulate cognitive needs.

Neither this contract nor Planner gains authority here to select concrete provider/model implementations. Concrete selection remains External / TBD.

## 23. Contract Interaction With Tools and Execution

This contract deliberately separates:

1. Capability Need.
2. Capability Availability.
3. Tool Availability.
4. Authorization.
5. Action Request.
6. Approval.
7. Execution.
8. Execution Evidence.
9. Cognitive Interpretation of Result.

These concepts may interact in future implementations but are not semantically equivalent and need not form one fixed pipeline.

The Core can participate cognitively in 1, 2, 3, 5, 8 and 9 when information is supplied, but does not acquire authority over 4, 6 or 7 by virtue of this contract.

## 24. Contract Anti-Patterns

### 24.1 Authority-by-Inference

**Definition:** inferir permiso porque una acción parece necesaria o correcta.

**Violation:** Cognitive necessity -> AUTHORIZED.

### 24.2 Validation Collapse

**Definition:** convertir self-check o confidence en Independent Validation.

**Violation:** internal_assessment -> VALIDATED.

### 24.3 Execution Collapse

**Definition:** tratar una propuesta, solicitud o aprobación como evidencia de ejecución.

**Violation:** PROPOSED / REQUESTED / APPROVED -> EXECUTED without evidence.

### 24.4 Context Authority Escalation

**Definition:** tratar contexto recuperado como autoridad gobernada.

**Violation:** Retrieved -> Authoritative.

### 24.5 Memory Identity Substitution

**Definition:** utilizar Memory como fuente superior de quién es Malāk.

### 24.6 Self-Model Authority Escalation

**Definition:** tratar un campo del Self-Model como permiso, Governance decision o Validation authority.

### 24.7 Provider Persona Leakage

**Definition:** permitir que engine/provider identity sustituya la identidad gobernada de Malāk.

### 24.8 Persistence Overreach

**Definition:** justificar ownership de persistencia por necesidad de continuidad.

### 24.9 Silent Canonicalization

**Definition:** convertir aprendizaje o persistencia en conocimiento canónico sin proceso/política aplicable.

### 24.10 False Continuity

**Definition:** simular memoria, estado o decisiones previas para aparentar continuidad.

### 24.11 Planner Absorption

**Definition:** convertir al Core en planificador estratégico o selector concreto de modelos debido a falta o ambigüedad de Planner.

### 24.12 God Object Contract

**Definition:** diseñar un contrato que convierta al Core simultáneamente en Memory, Security, Governance, Validation, Planner, Tool Executor o Infrastructure Manager.

## 25. Contract Compatibility With Future Implementations

Una futura implementación se considera conceptualmente compatible con este contrato si puede cambiar libremente aspectos técnicos como:

- runtime;
- lenguaje;
- engine/provider;
- estructura de procesos;
- transporte;
- almacenamiento externo;
- mecanismo de contexto;
- mecanismo de ejecución;

sin alterar las semánticas definidas aquí.

Model Independence exige sustituibilidad arquitectónica, no equivalencia funcional. Por ello, una implementación puede degradar ciertas capabilities al cambiar de engine sin dejar de cumplir este contrato, siempre que represente honestamente la degradación y preserve los invariantes aplicables.

## 26. Contract Conformance Criteria

Una implementación candidata del Cognitive Core deberá poder demostrar, mediante futuros evals, al menos que:

1. Mantiene Identity != Model / Provider.
2. Mantiene Identity != Prompt / Context / Memory.
3. Mantiene Self-Model != Identity completa.
4. Mantiene Cognition != Authority.
5. Mantiene UNKNOWN distinto de DENIED y AUTHORIZED.
6. Mantiene NOT_VALIDATED distinto de INVALID y VALIDATED.
7. Mantiene capability availability distinta de execution authority.
8. No afirma ejecuciones sin evidencia.
9. No auto-promueve conocimiento o baseline.
10. No convierte Memory retrieval en autoridad identitaria.
11. No inventa continuidad cuando falta contexto.
12. Sobrevive a cambios controlados de engine sin provider-persona leakage.
13. Mantiene Unified External Identity sin imponer uniformidad estilística perfecta.
14. Degrada de forma epistémicamente honesta ante estados faltantes o contradictorios.
15. No absorbe responsabilidades de Security, Governance, Validation, Planner, Memory, Persistence o Tool Execution.

## 27. Open Questions / TBD

Este contrato deja deliberadamente abiertos:

1. Runtime interface shape.
2. Concrete message/payload representation.
3. Contract serialization or transport.
4. Context delivery/composition mechanism.
5. Self-Model hydration, synchronization and freshness.
6. Provenance representation and precedence for non-identity information.
7. Security / authorization state representation and freshness mechanism.
8. Independent Validation existence, scope and intervention points.
9. Identity Continuity Mechanism implementation.
10. Temporary Operational State representation and lifecycle.
11. Tool/capability execution mechanism.
12. Concrete model/implementer selection mechanism.
13. Planner/Core detailed runtime boundary.
14. Governed identity version resolution mechanism.
15. Knowledge Promotion and persistence policies.
16. Confidence/uncertainty representation.
17. Which contract information classes are materialized on every operation versus on demand.
18. Whether multiple technical interfaces are needed to materialize this single conceptual contract.

## 28. Derived Implications for IDENTITY_EVALS.yaml

`IDENTITY_EVALS.yaml` deberá convertir las obligaciones de este contrato en pruebas observables.

Como mínimo, deberá contemplar:

- positive contract conformance tests;
- negative boundary tests;
- adversarial authority-transfer tests;
- false execution tests;
- false memory/continuity tests;
- missing Self-Model tests;
- authorization tri-state tests;
- validation-state tests;
- engine swap tests;
- provider persona leakage tests;
- Memory loss tests;
- context contradiction tests;
- Governance impersonation tests;
- Knowledge Promotion leakage tests;
- graceful degradation tests;
- cross-artifact semantic consistency tests.

## 29. Draft Self-Review

### Contract vs Implementation Review

1. No se definieron clases ni métodos.
2. No se definió protocolo de transporte.
3. No se definió serialization runtime.
4. No se fijó un pipeline secuencial.
5. No se eligió una tecnología de Self-Model, Memory o Security.
6. No se eligió un mecanismo de model routing.

### Authority Leakage Review

1. Received authorization state does not grant Security ownership.
2. Capability availability does not grant execution authority.
3. Candidate Output does not grant approval authority.
4. Validation feedback does not grant self-certification authority.
5. Governed identity information does not grant mutation authority.
6. Context continuity does not carry authorization automatically.

### Semantic Collapse Review

Se verificó explícitamente que el contrato no colapse:

- UNKNOWN / DENIED / AUTHORIZED;
- NOT_VALIDATED / INVALID / VALIDATED;
- AVAILABLE / AUTHORIZED_TO_EXECUTE;
- REQUESTED / APPROVED / EXECUTED;
- LEARNED / PERSISTED / CANONICAL;
- RETRIEVED / AUTHORITATIVE;
- CONTEXT / IDENTITY;
- SELF_MODEL / IDENTITY;
- ENGINE / IDENTITY.

### God Object Regression Review

El contrato no convierte al Cognitive Core en:

- Memory;
- Persistence Manager;
- Security Authority;
- Governance Authority;
- Independent Validation;
- Planner;
- Concrete Model Selector;
- Tool Executor;
- Infrastructure Manager;
- Knowledge Promotion Authority.

### Cross-Artifact Consistency Review

1. Preserva CORE-RESP-001 ... CORE-RESP-007 sin agregar nuevas responsabilidades al Charter.
2. Preserva BOUND-CORE-001 ... BOUND-CORE-009.
3. Preserva los 11 Identity Invariants existentes sin crear invariantes nuevos.
4. Respeta `VOICE_AND_BEHAVIOR.md` sin fijar personalidad textual rígida.
5. Respeta `CONTINUITY_MODEL.md` separando continuidad de persistencia y recall perfecto.
6. Respeta `SELF_MODEL_SCHEMA.yaml` conservando explicit unknowns y authority non-transfer.

### Architectural Assumptions Avoided

1. No API technology assumed.
2. No runtime language assumed.
3. No storage technology assumed.
4. No model provider assumed.
5. No validation technology assumed.
6. No security enforcement technology assumed.
7. No context delivery mechanism assumed.
8. No tool execution framework assumed.
9. No planner implementation assumed.
10. No mid-inference hot-swap mechanism assumed.

### Risks and Ambiguities

1. Un contrato demasiado abstracto puede requerir una segunda especificación técnica antes de implementación.
2. La representación de provenance y freshness será crítica para evitar estados falsamente actuales.
3. La separación estricta entre availability, authorization y execution puede aumentar complejidad operativa, pero evita authority leakage.
4. La continuidad entre sesiones dependerá de mecanismos externos aún TBD sin que esos mecanismos deban convertirse en Identity.
5. La interoperabilidad con engines cerrados puede limitar cuánto puede controlarse la persona nativa del modelo.
6. La futura Independent Validation deberá evaluar conformidad sin convertirse en un cuello de botella universal impuesto por este contrato.
7. La frontera Planner/Core puede requerir refinamiento técnico sin modificar las responsabilidades conceptuales actuales.
8. La resolución de contexto contradictorio necesita provenance/precedence externa sin otorgar autoridad al Core para inventarla.

### TBD Summary

- Runtime interface shape.
- Transport/serialization.
- Context delivery/composition.
- Self-Model hydration/synchronization/freshness.
- Provenance and precedence.
- Security state representation/freshness.
- Independent Validation scope/mechanism.
- Identity Continuity Mechanism.
- Temporary Operational State lifecycle.
- Tool/capability execution mechanism.
- Concrete model selection mechanism.
- Planner/Core runtime boundary.
- Governed identity version resolution.
- Knowledge Promotion/persistence policy.
- Confidence/uncertainty representation.
