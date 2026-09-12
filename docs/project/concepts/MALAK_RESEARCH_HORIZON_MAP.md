---
title: Malāk Research Horizon Map
status: concept
authority: non_normative
document_role: research_horizon_reconciliation
language: es
created: 2026-09-09
as_of_branch: main
as_of_commit: cc9c7373879555a3eb267cd91be5228207427ae8
external_evidence_reviewed: 2026-09-12
external_evidence_baseline_commit: cd50c308e1f5a1481851d6402ae4435341410d27
related:
  - documents/projects/jarvis/ideas.md
  - docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
  - docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
  - docs/project/concepts/MALAK_COGNITIVE_DATASET_FOUNDATION.md
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - SECURITY.md
purpose: >
  Preservar la reconciliación entre la visión futura de Malāk, la investigación
  externa reciente y los conceptos ya existentes, identificando únicamente los
  refuerzos y gaps reales sin crear una segunda fuente de autoridad ni autorizar
  implementación.
---

# Malāk Research Horizon Map

## 1. Propósito

Este documento preserva la reconciliación realizada sobre la dirección futura de
Malāk después de revisar los conceptos existentes, el registro de ideas y la
investigación reciente sobre sistemas agentic, memoria, seguridad, identidad,
interoperabilidad, ejecución durable y resiliencia.

Su función es responder:

> ¿Qué parte de la visión futura ya está representada en Malāk, qué debe
> reforzarse y qué constituye todavía un gap conceptual real?

Este documento:

- no modifica el baseline;
- no modifica Blueprint, Constitución Cognitiva ni Gobernanza;
- no autoriza un sprint;
- no autoriza agentes, Memory persistente, tools, MCP, A2A, Sandbox ni acceso externo;
- no crea nuevos componentes, managers, registries o servicios;
- no convierte investigación externa en autoridad;
- no aprueba arquitectura detallada;
- no sustituye `ideas.md`;
- no sustituye las referencias de Long Horizon o ejecución agentic efímera.

Toda promoción futura deberá volver a verificarse contra el baseline vigente y
pasar por `Necessity & Complexity Review`.

---

## 2. Método de reconciliación

Cada línea de investigación se clasifica mediante uno de estos estados:

```text
ALIGNED
REINFORCE_EXISTING
GAP_CANDIDATE
WATCH
IRRELEVANT
CONFLICTS_WITH_VISION
```

Significado:

- `ALIGNED`: ya existe representación conceptual suficiente;
- `REINFORCE_EXISTING`: existe dueño conceptual, pero una propiedad debe quedar más explícita;
- `GAP_CANDIDATE`: falta una propiedad importante o su dueño todavía no está suficientemente definido;
- `WATCH`: relevante para el futuro, sin necesidad actual demostrada;
- `IRRELEVANT`: no aporta a la dirección de Malāk;
- `CONFLICTS_WITH_VISION`: contradice soberanía, Human in Control o límites constitucionales.

Regla:

```text
Research
   ↓
DIFF contra Malāk existente
   ↓
¿ya existe?
 ┌───────┴────────┐
 sí              no
 ↓                ↓
reforzar      ¿gap real?
                  ↓
            propuesta candidata
```

Solo un `GAP_CANDIDATE` demostrado puede originar posteriormente una nueva idea,
y aun así deberá preferirse ampliar una responsabilidad existente cuando sea
arquitectónicamente limpio.

---

## 3. Resultado ejecutivo

| Línea | Estado | Dueño conceptual principal | Resultado |
|---|---|---|---|
| Durable Cognitive Execution | `ALIGNED` | Long Horizon / IDEA-023 / IDEA-024 | Ya existen Task State, checkpoints, recovery, idempotencia y continuidad fuera del LLM. |
| Governed Self-Improvement | `ALIGNED` | IDEA-002 / Long Horizon | Malāk observa, investiga, experimenta y propone; no se autoaprueba ni modifica el baseline por autoridad propia. |
| Resource Governance | `ALIGNED` | IDEA-003 | Presupuestos y límites de recursos ya están contemplados. |
| Deception / Honeypots / Adversarial Evaluation | `ALIGNED` | IDEA-019 / IDEA-010 | Honeypots, honeytokens, Adversarial Twin, red/purple team y aislamiento ya están representados. |
| Incident Forensics / Attack Path | `ALIGNED` | ampliación IDEA-019 | Ya se contemplan timeline, IP observada, attack path, evidence package, recovery y security regression learning. |
| Prompt & Context Trust Boundary | `REINFORCE_EXISTING` | `SECURITY.md` / IDEA-006 / IDEA-013 / IDEA-016 | La política ya establece la frontera de contenido no confiable; el delta de research es verificar su generalización operacional y futuras técnicas de atribución causal. |
| Memory & Knowledge Trust / Poisoning | `REINFORCE_EXISTING` | Episodic Admission + Provenance + Producer Authorization + Governed Projection/Consumption + futura Memory + IDEA-013 / IDEA-016 | El baseline ya valida provenance estructural, autorización scoped del productor, proyección gobernada y consumo controlado hacia Admission; permanecen pendientes Candidate Content Identity/propagación y trust, taint, revocation y quarantine hacia persistencia, retrieval y Knowledge. |
| AI Supply-Chain Trust | `GAP_CANDIDATE` | IDEA-004 / IDEA-009 / IDEA-011 / IDEA-016 | Existen hashes, model governance y referencias de provenance; falta una política conceptual unificada de admisión de artefactos AI. |
| Agent Identity & Delegation | `GAP_CANDIDATE` | `SECURITY.md` / IDEA-005 / IDEA-024 / Security Control Plane | La política ya exige delegación no expansiva; falta una cadena verificable de identidad/delegación y revocación derivada. |
| Compromise Containment & Trust Revocation | `GAP_CANDIDATE` | `SECURITY.md` / IDEA-019 / IDEA-001 / Security Control Plane | La política ya define la postura de contención; falta explicitar propagación sistémica de desconfianza y reemplazabilidad de componentes. |
| Data Classification & Disclosure Control | `GAP_CANDIDATE` | `SECURITY.md` / Context / Knowledge | La política ya limita disclosure/reuse; falta una clasificación transversal suficientemente explícita cuando exista superficie real que la necesite. |
| Governed Interoperability (MCP/A2A) | `WATCH` | `SECURITY.md` / adapters futuros / contratos internos | La política conserva precedencia sobre protocolos externos; investigar adapters solo ante necesidad demostrada. |
| Governed Procedural Learning | `REINFORCE_EXISTING` | IDEA-002 / Skills-on-Demand / Knowledge Governance | La promoción de procedimientos aprendidos debe permanecer gobernada y no autoejecutable. |
| Multimodal Perception Boundary | `WATCH` | futura Interface/Perception boundary | Visión, audio y otras percepciones son relevantes a largo plazo, sin necesidad actual de nuevo subsistema. |
| World models | `WATCH` | futura investigación de percepción/entorno | No existe necesidad actual; reevaluar solo si tareas reales demuestran valor. |
| Autonomous self-modification | `CONFLICTS_WITH_VISION` | Governance / IDEA-002 | La automodificación productiva autónoma permanece fuera de la visión; la mejora continúa gobernada y basada en propuestas. |

---

## 4. Lo ya cubierto y que no debe duplicarse

### 4.1. Durable Cognitive Execution

Long Horizon ya preserva:

```text
Task
 ↓
Checkpoint
 ↓
Action
 ↓
Evidence / Receipt candidate
 ↓
Checkpoint
 ↓
Pause / Interrupt
 ↓
Recover
 ↓
Validate
 ↓
Resume
```

También contempla Persistent Task State, side effects, idempotencia y recuperación.
No debe crearse una nueva iniciativa de Durable Execution mientras esos conceptos
sean suficientes.

### 4.2. Governed Self-Improvement

IDEA-002 y Long Horizon ya preservan la distinción entre observación, propuesta y
gobernanza. Este mapa no vuelve a definir esa regla; únicamente registra que la
investigación externa revisada no aporta evidencia suficiente para relajarla.

Malāk podrá impulsar una mejora mediante investigación, comparación, prototipos,
tests, evidencia e Implementation Packets candidatos, pero su autoridad y
promoción continúan regidas por Governance, `ideas.md` y el Construction Protocol.

### 4.3. Adversarial Security, Deception y Forensics

IDEA-019 ya contempla:

- detección y contención;
- aislamiento y bloqueo;
- revocación de credenciales y cierre de sesiones;
- kill switches;
- honeypots, honeynets y honeytokens;
- Adversarial Twin;
- observación externa;
- roles de contingencia;
- niveles de contingencia;
- forensics;
- IP y otros indicadores técnicos;
- reconstrucción del camino del ataque;
- security regression learning;
- red team / purple team autorizado.

`SECURITY.md` es el dueño normativo de la postura de respuesta, alcance permitido,
contención y prohibición de ampliar autoridad por causa de un incidente. Este
mapa conserva únicamente la relación con líneas futuras de investigación y no
reproduce la secuencia normativa de respuesta.

La evidencia de una IP, ASN, dominio, fingerprint o indicador no constituye por
sí sola atribución de identidad.

---

## 5. Refuerzo transversal — Prompt & Context Trust Boundary

`SECURITY.md` es el dueño normativo de Prompt & Context Trust Boundary y de la
separación entre contenido externo, instrucciones y autoridad. Este mapa no
reproduce esa ley.

El delta de investigación que permanece abierto es comprobar, cuando existan
superficies reales, cómo aplicar de forma consistente esa frontera a:

- contenido web, archivos, emails y documentos;
- tool output y payloads de interoperabilidad;
- retrieval y Memory recuperada;
- futuros resultados producidos por agentes o subprocesos;
- causal attribution de acciones cuando la técnica alcance madurez suficiente.

Dueños conceptuales relacionados:

```text
SECURITY.md
IDEA-006 Evidence Acquisition
IDEA-013 Context Efficiency
IDEA-016 Source Governance
Security Control Plane
```

No crear todavía un `PromptInjectionManager` ni un motor universal de trust.

---

## 6. REINFORCE EXISTING — Memory & Knowledge Trust / Poisoning

La fundación episódica aislada de Memory ya no se limita al G3 original de
`Episodic Memory Admission Boundary`.

El baseline dispone ahora de fronteras separadas para:

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
```

La evolución integrada mediante PR #82, PR #85, PR #88 y PR #92 elimina como gap
pendiente la provenance estructural de assessments, la autorización scoped de sus
productores y el consumo controlado de una projection hacia la policy existente
de Admission. La proyección gobernada bloquea fallback trust-sensitive desde
`candidate.control`, exige cardinalidad exacta y gobierna temporal validity
mediante evidencia dedicada autorizada; el adapter de consumo bloquea projections
no consumibles y delega exactamente una vez a Admission cuando corresponde.

Se preserva deliberadamente:

```text
Projection READY != Admission ELIGIBLE
Projection HOLD != Admission HOLD automatically
Projection DENIED != Candidate REJECT automatically
Consumption EVALUATED != persistence authorization
ELIGIBLE != persistence authorization
```

El residual inmediato ya no es `Projection → Admission`. PR #93 demostró que
`candidate_id` binding no equivale a identidad del contenido del candidate y
seleccionó G0/G1 para un `EpisodicCandidateContentIdentity` determinista y
versionado. G2, implementación y propagación de esa identidad permanecen sin
autorización en el snapshot histórico de esta sección. Persistence Authorization
continúa diferida en ese snapshot hasta que exista binding end-to-end suficiente.

Después de esa frontera, el trabajo restante incluye propagar de forma gobernada
trust, taint, revocation y quarantine hacia persistencia, retrieval y promoción a
Knowledge.

La futura Memory no deberá reducirse a almacenamiento y similarity search.

La frontera completa objetivo continúa siendo:

```text
Memory Candidate
      ↓
Candidate content identity / binding
      ↓
Assessment production
      ↓
Assessment provenance
      ↓
Producer authorization
      ↓
Governed temporal control
      ↓
Governed input projection
      ↓
Governed projection consumption
      ↓
Admission evaluation
      ↓
Persistence authorization
      ↓
Stored Memory
      ↓
Trust-aware retrieval eligibility
      ↓
Knowledge candidate when applicable
```

Estado material observado a `cc9c7373879555a3eb267cd91be5228207427ae8`:

```text
candidate contracts                       implemented
admission policy                          implemented
assessment provenance                     implemented
assessment producer authorization         implemented
governed input projection                 implemented
projection -> admission consumption       implemented
candidate content identity                G0/G1 ONLY
content identity propagation              NOT DESIGNED / NOT AUTHORIZED
persistence authorization                 NOT AUTHORIZED
persistent Memory                         NOT AUTHORIZED
retrieval                                 NOT AUTHORIZED
Knowledge promotion                       NOT AUTHORIZED
```

Separación histórica preservada para esta línea:

```text
Conversation → Ephemeral Context
Experience   → Episodic Memory candidate
Stable fact  → Semantic Memory candidate
Procedure    → Procedural Memory candidate
Evidence     → Knowledge candidate
```

Propiedades candidatas que permanecen relevantes downstream:

- source authority y confidence separados;
- scope y dominio explícitos;
- temporal validity / freshness;
- detección de contradicción;
- capacidad de marcar entradas como `SUSPECT`, `TAINTED`, `SUPERSEDED` o
  equivalentes antes de reutilizarlas;
- revocación o quarantine de memoria derivada de una fuente comprometida;
- no promover automáticamente resultados de incidentes, agentes o herramientas
  a conocimiento canónico;
- retrieval condicionado por trust, aplicabilidad y autoridad, no únicamente por similitud.

El trabajo pendiente deberá reforzar futura Memory, IDEA-013 e IDEA-016 antes de
justificar una iniciativa independiente.

---

## 7. GAP CANDIDATE — AI Supply-Chain Trust

La cadena de suministro futura de Malāk no estará formada solamente por paquetes
de software.

Podrá incluir:

```text
packages
dependencies
models
GGUF / weights
LoRA / adapters
embedding models
datasets
prompt templates
skills
agent definitions
MCP servers
A2A adapters
plugins / external tools
containers / images
knowledge sources
```

Antes de admitir un artefacto relevante deberá poder evaluarse, proporcionalmente
al riesgo:

- origen;
- versión;
- hash;
- firma cuando exista y sea útil;
- provenance;
- licencia;
- integridad;
- vulnerabilidades conocidas;
- permisos/capacidades requeridos;
- dependencias transitivas;
- posibilidad de rollback;
- política de actualización;
- capacidad de cuarentena o retiro.

`SECURITY.md` conserva las restricciones normativas de supply-chain trust. El
gap de research es cómo materializar admission/provenance de artefactos AI sin
crear prematuramente un registry universal ni copiar esquemas externos completos.

Dueños conceptuales a reforzar antes de crear nada nuevo:

```text
SECURITY.md
IDEA-004 Model Governance
IDEA-009 Development Tooling
IDEA-011 Validation & Delivery
IDEA-016 Source Governance
Security Control Plane
```

No crear todavía un `TrustedArtifactRegistry` salvo necesidad operacional demostrada.

---

## 8. GAP CANDIDATE — Agent Identity & Delegation

`SECURITY.md` es el dueño de la regla de delegación no expansiva y de los límites
de autoridad efectiva. Este mapa no conserva una segunda fórmula normativa.

IDEA-005 y IDEA-024 ya contemplan identidad, scopes, TTL, Security Context y
prohibición de autoelevación. El gap de investigación restante es una cadena de
delegación verificable y revocable cuando un componente autorizado origina
trabajo que otro agente, tool o executor realizará.

Una futura investigación podrá necesitar evidencia de:

- quién originó la delegación;
- identidad del receptor;
- propósito;
- scope;
- recursos;
- restricciones;
- issuer;
- issued_at / expires_at;
- revocation status;
- parent context o referencia equivalente;
- evidencia de autorización.

La identidad criptográfica fuerte, firmas, nonce/replay protection, PKI y
mecanismos equivalentes permanecen sujetos a diseño y revisión propios.

---

## 9. GAP CANDIDATE — Compromise Containment & Trust Revocation

`SECURITY.md` es el dueño normativo de la reducción de autoridad ante compromiso,
la secuencia de contención, preservación de evidencia y reintroducción segura.
Este mapa no replica esas reglas.

IDEA-001 e IDEA-019 ya contemplan kill switch, quarantine, destrucción de sandbox,
revocación y niveles de contingencia. El gap de investigación identificado es
convertir la respuesta local en una propiedad sistémica de componentes
reemplazables y estudiar cómo propagar desconfianza sin asumir compromiso total.

Aplica potencialmente a:

```text
runtime
provider
model
agent
tool
skill
MCP/A2A adapter
plugin
memory backend
knowledge source
sandbox
external service
```

### Propagación de desconfianza

Si un componente comprometido A interactuó con otros activos:

```text
A
├── used credential B
├── wrote artifact C
├── contacted component D
└── produced state E
```

la investigación futura deberá determinar cómo marcar y revalidar de forma
proporcional esos activos sin asumir que todos están comprometidos.

Dueños conceptuales a reforzar:

```text
SECURITY.md
Security Control Plane
IDEA-001 Sandbox / Evidence
IDEA-019 Incident Response / Deception
IDEA-005 Secure Context
IDEA-021 Emergency Control Surface
```

---

## 10. GAP CANDIDATE — Data Classification & Disclosure Control

`SECURITY.md` es el dueño de las restricciones normativas sobre acceso, disclosure,
persistencia y reuse. Este mapa no vuelve a declarar esa ley.

`Least Context`, privacidad y minimización ya existen como principios, pero la
futura expansión de Malāk hacia Memory, tools, agents y servicios externos puede
requerir una clasificación transversal más explícita.

Dimensiones candidatas, sin aprobar taxonomía:

- sensibilidad;
- propietario/origen;
- finalidad permitida;
- domain/scope;
- retención;
- posibilidad de exportación;
- posibilidad de uso por modelos remotos;
- posibilidad de persistencia en Memory;
- posibilidad de incluirse en evidencia o reportes;
- redaction / minimización;
- requisitos de consentimiento o revisión humana.

No crear todavía un sistema universal de labels. Primero deberá existir una
superficie real que necesite esta clasificación.

---

## 11. Interoperabilidad gobernada

`SECURITY.md` es el dueño normativo de la postura de interoperabilidad y de la
precedencia de contratos internos sobre protocolos externos. Este mapa conserva
únicamente el estado `WATCH` y el gap de investigación.

Cuando exista un caso de uso real, la evaluación deberá comprobar que cualquier
adapter futuro:

- consume contratos internos de Malāk;
- mantiene identidad externa separada de autoridad interna;
- trata mensajes, metadata, schemas y tool outputs externos como contenido no
  confiable;
- mantiene egress, secretos, recursos y scope bajo los planos de control propios.

No existe necesidad demostrada de una capa universal de MCP/A2A.

---

## 12. Governed Procedural Learning

Malāk podrá aprender procedimientos sin concederse autoridad para cambiarse.

Flujo candidato:

```text
Observed executions
       ↓
candidate procedure
       ↓
evidence / evaluation
       ↓
security review
       ↓
owner / knowledge governance approval
       ↓
Skill / Procedure artifact
       ↓
load on demand when authorized
```

Un procedimiento aprendido:

```text
Skill != Capability
Skill != Permission
Skill != Policy
Skill != Authority
```

La futura promoción de procedimientos deberá reutilizar IDEA-002, Skills-on-Demand,
Knowledge Governance y validación existente antes de crear un nuevo sistema de
procedural learning.

---

## 13. Multimodal Perception Boundary — WATCH

A largo plazo Malāk podrá necesitar procesar:

```text
text
audio
vision
files
system state
sensor / environment observations
```

Principio candidato:

```text
Perception != Authority
Observation != Truth
```

Toda percepción deberá entrar mediante adapters/capabilities gobernadas, conservar
provenance cuando corresponda y quedar fuera del plano de autoridad.

No existe necesidad actual suficiente para crear una nueva Perception Layer ni
incorporar world models.

---

## 14. Mapa de evidencia externa validada — 2026-09-12

Esta sección es el **ledger canónico de evidencia externa revisada** para esta
capa conceptual. Preserva qué artefacto fue analizado, qué propiedad concreta se
extrajo y a qué dueño existente de Malāk se relaciona.

Principio rector:

> **Malāk adopta propiedades demostradas, no arquitecturas externas.**

Las referencias registradas son identidades descriptivas de artefactos ya
revisados. No constituyen instrucciones de retrieval, contenido confiable,
dependencias vivas ni autoridad. Toda revalidación futura requiere una nueva
acción de research explícita y acotada.

### 14.1. Clases de evidencia

Para esta reconciliación se usa la siguiente precedencia orientativa:

```text
E1 — estándares, organismos públicos, especificaciones formales
E2 — documentación primaria de sistemas/productos y postmortems verificables
E3 — investigación académica publicada o revisada
E4 — implementación open-source inspeccionable
E5 — comunidades, foros y experiencia anecdótica
```

La precedencia no sustituye el análisis de aplicabilidad. Las fuentes `E5` sirven
solo como señal de fricción operativa o tendencia; no establecen por sí solas
requisitos de seguridad, arquitectura o gobernanza.

### 14.2. Familias permanentes de referencia

Estas familias forman parte del radar de investigación de Malāk y **no deben
eliminarse** porque una revisión puntual utilice artefactos más concretos:

- OWASP Top 10 para aplicaciones web;
- OWASP Top 10 para aplicaciones LLM/GenAI;
- OWASP Agentic Security y Agent Control Standard;
- NIST AI RMF y perfiles de ciberseguridad aplicables a AI;
- MITRE ATLAS;
- investigación académica sobre prompt injection, tool poisoning, persistent
  state corruption, memory poisoning y delegated authority;
- incidentes reales de sistemas agentic y AI-assisted development;
- estándares y prácticas maduras de provenance, workload identity, autorización,
  durable execution, supervision, observability y supply-chain assurance.

Estas familias son radar, no dependencias ni autorización para incorporar
controles por taxonomía.

### 14.3. Roles de la evidencia

Cada artefacto revisado puede cumplir uno o más roles:

```text
CORROBORATION
→ respalda una propiedad que ya posee dueño en Malāk.

RESEARCH_INPUT
→ aporta una propiedad útil para investigar o adaptar con semántica propia.

WATCH_SIGNAL
→ relevante o prometedor, pero inmaduro, no necesario o insuficiente para
  derivar arquitectura actual.
```

Estos roles describen la función de la **evidencia externa**. No reemplazan los
estados de research de §2 ni la clasificación `ADOPT / ADAPT / OBSERVE / REJECT`
del Construction Protocol.

### 14.4. Ledger de artefactos revisados

Cuando no se preservó una revisión inmutable externa, el registro se apoya en
título/organización/fecha y en una descripción acotada del alcance. No debe
asumirse que contenido externo posterior es idéntico a lo analizado.

| ID | Clase | Artefacto revisado / identidad | Alcance exacto analizado | Propiedad observada | Rol | Malāk target / owner |
|---|---|---|---|---|---|---|
| `EXT-01` | `E1` | NIST — *Back to the Future: Why Agentic AI Needs a Strong Identity Foundation* — 2026-08-27 | identidad de agentes/workloads, credenciales acotadas y de corta vida, separación respecto de identidad humana | la seguridad agentic necesita identidad verificable y lifecycle de credenciales fuera del modelo | `CORROBORATION` + `RESEARCH_INPUT` | §8 / `SECURITY.md` |
| `EXT-02` | `E1` | ACSC/CISA/NSA/Cyber Centre Canadá/NCSC-NZ/NCSC-UK — *Careful adoption of agentic AI services* — 2026-05-01 | principals distintos, least privilege, credenciales efímeras, resource limits, human control points, aislamiento, monitoreo y rollback | la autoridad agentic debe estar acotada, verificable y revocable en runtime | `CORROBORATION` + `RESEARCH_INPUT` | `SECURITY.md` / §8 / §10 / IDEA-003 |
| `EXT-03` | `E1` | ASD — *Agentic AI Harnesses — The layer above the model* — 2026-09-11 | seguridad, gobernanza, validación, supervisión y assurance en el harness/infraestructura | controles críticos no deben depender solamente del prompt o comportamiento probabilístico del modelo | `CORROBORATION` | `SECURITY.md` |
| `EXT-04` | `E2` | Google Developers — *Build zero-trust AI agents with Google's Agent Development Kit* — 2026-08-17 | Zero Trust para agentes con efectos sobre estado real y validación determinista fuera del LLM | un agente que puede producir side effects necesita fronteras de sistema independientes del modelo | `CORROBORATION` | `SECURITY.md` |
| `EXT-05` | `E2` | Anthropic — *How we contain Claude across products* — 2026-05-25 | containment del entorno, blast radius y approval fatigue | hard boundaries deben sobrevivir a fallos probabilísticos; demasiadas aprobaciones humanas pueden degradar atención | `CORROBORATION` + `RESEARCH_INPUT` | `SECURITY.md` / Human in Control |
| `EXT-06` | `E1` | A2A Protocol — specification revisada 2026-09-12; revisión inmutable no preservada | semántica de `TASK_STATE_AUTH_REQUIRED`, scope, validez y revocación | solicitar/requerir autorización no equivale a poseer autorización para ejecutar | `CORROBORATION` | §8 / `SECURITY.md` |
| `EXT-07` | `E1` | OWASP GenAI Security Project — *Top 10 for Agentic Applications 2026* — 2025-12-09 | goal hijack, tool misuse, identity/privilege abuse, supply chain, memory/context poisoning, inter-agent communication, cascading failures, human-agent trust y rogue agents | el threat model agentic requiere controles sistémicos más allá de prompting | `CORROBORATION` | `SECURITY.md` / §§5–10 |
| `EXT-08` | `E2` | OWASP GenAI Security Project — *Memory Is a Feature. It Is Also an Attack Surface* — 2026-05-13 | persistencia de contaminación, memory/context poisoning y reutilización posterior | Memory persistente es una frontera de trust y puede transportar compromiso entre interacciones | `CORROBORATION` + `RESEARCH_INPUT` | §6 / `SECURITY.md` |
| `EXT-09` | `E1` | W3C — *PROV-Overview* — 2013 | entidades, actividades, agentes, derivación, atribución y provenance | provenance puede modelarse separadamente de autoridad y decisión | `RESEARCH_INPUT` | §7 / future validation research |
| `EXT-10` | `E1` | SLSA v1.2 — *Provenance* | identidad del artefacto, origen/proceso de build y attestations | integridad/provenance verificable puede ligar evidencia a cómo se produjo un artefacto sin convertirla en autorización | `RESEARCH_INPUT` | §7 / future validation research |
| `EXT-11` | `E1` | seL4 — documentación de *Capabilities* revisada 2026-09-12; revisión inmutable no preservada | tokens no falsificables con derechos explícitos | autoridad mínima y explícita puede representarse mediante derechos verificables; el término no equivale a `Capability` funcional de Malāk | `CORROBORATION` + `RESEARCH_INPUT` | `SECURITY.md` / Capability First |
| `EXT-12` | `E3` | Google — *Zanzibar: Google's Consistent, Global Authorization System* — USENIX ATC 2019 | autorización como infraestructura separada y consistente | autorización no debe depender de inferencias dispersas en cada consumidor | `CORROBORATION` + `RESEARCH_INPUT` | §8 / Security Control Plane |
| `EXT-13` | `E1` | SPIFFE — workload identity specifications/docs revisadas 2026-09-12; revisión inmutable no preservada | identidad verificable de workloads y credenciales de vida acotada | identidad de workload puede separarse de identidad humana y operar con lifecycle propio | `RESEARCH_INPUT` | §8 |
| `EXT-14` | `E2` | Kubernetes — patrón/documentación de Controllers revisada 2026-09-12; revisión inmutable no preservada | desired state, observed state y reconciliation loop | un sistema dinámico no debe asumir que un estado deseado continúa siendo el estado real | `RESEARCH_INPUT` | §4.1 / Long Horizon |
| `EXT-15` | `E2` | Erlang/OTP — Supervisor Behaviour docs revisadas 2026-09-12; revisión inmutable no preservada | supervision trees, restart strategies y restart intensity | lifecycle y recuperación de procesos requieren supervisión explícita y límites, no reinicio ciego | `RESEARCH_INPUT` | §4.1 / IDEA-003 |
| `EXT-16` | `E2` | Temporal — documentación de durable execution revisada 2026-09-12; revisión inmutable no preservada | persistencia de progreso, retries/replay, idempotencia y side effects | recuperación durable exige semántica explícita de retry/resume/replay/compensation | `RESEARCH_INPUT` | §4.1 / Long Horizon |
| `EXT-17` | `E1` | OpenTelemetry — context propagation docs revisadas 2026-09-12; revisión inmutable no preservada | trace/span context y propagación causal entre procesos/servicios | correlación causal puede mejorar observabilidad sin convertir telemetry en evidencia o autoridad | `RESEARCH_INPUT` | Long Horizon / Engineering evidence |
| `EXT-18` | `E2` | OpenAI — *A shared playbook for trustworthy third party evaluations* — 2026-05-29 | harness, tools, environment y configuration como parte de la validez de una evaluación | un resultado no es interpretable sin contexto suficiente sobre cómo fue producido | `CORROBORATION` + `RESEARCH_INPUT` | `docs/development/malak_construction_protocol.md` / future validation research |
| `EXT-19` | `E2` | OpenAI — *Separating signal from noise in coding evaluations* — 2026-07-08 | auditoría de calidad/validez de tareas de evaluación | `PASS` no garantiza evidencia válida cuando el instrumento de evaluación está defectuoso | `CORROBORATION` | `docs/development/malak_construction_protocol.md` |
| `EXT-20` | `E2` | Anthropic — *Demystifying evals for AI agents* — 2026-01-09 | trayectorias multistep, tool calls y cambios de estado en evals agentic | evaluar solo output final puede ocultar fallos importantes del proceso | `CORROBORATION` + `RESEARCH_INPUT` | `docs/development/malak_construction_protocol.md` / future validation research |
| `EXT-21` | `E3` | USENIX Security 2026 — *AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via Causal Attribution of Tool Invocations* | causal attribution de tool invocations frente a indirect prompt injection | vincular una acción con su causa/intención puede ayudar a distinguir user intent de contenido no confiable | `WATCH_SIGNAL` | §5 |
| `EXT-22` | `E4` | Gentleman Programming `gentle-pi` — `main@6e4478c04615b0c013a017178dcfefa51579982d` | native RDD workflow, review integration, runner/protocol, task lifecycle y presence projection | candidate freeze, lineage, candidate-bound receipts, bounded correction, review sin delivery authority, typed lifecycle y bounded concurrency son propiedades implementables; la línea RDD inspeccionada permanece inestable | `RESEARCH_INPUT` + `WATCH_SIGNAL` | Construction Protocol / §4.1 / Long Horizon |

El ledger termina en el **target/owner**. No mantiene una segunda copia de la
adaptación arquitectónica ni del estado operativo del dueño. Cualquier cambio de
estado debe actualizarse en su fuente correspondiente, no aquí.

### 14.5. Contrafuerzos derivados de la evidencia

La investigación produjo estas observaciones de diseño, siempre subordinadas a
los dueños documentales aplicables:

1. Human in Control no debe degradarse en aprobación humana de cada microacción.
2. Una identidad verificable no sustituye una decisión de autorización.
3. Telemetry puede ayudar a reconstruir causalidad sin convertirse por sí sola en evidencia canónica.
4. Un `PASS` no demuestra validez del instrumento de evaluación.
5. Presence no demuestra liveness ni autoridad.
6. Retry no equivale a recovery; durable execution debe estudiar idempotencia,
   replay y compensation.
7. Un artefacto externo revisado no se convierte en dependencia externa viva.
8. Una propiedad validada externamente no autoriza adopción de la arquitectura completa que la implementa.

### 14.6. Señal comunitaria y foros

La revisión de foros técnicos y comunidades se conserva únicamente como señal de
fricción operativa. Los temas recurrentes —frameworks sobredimensionados,
observabilidad insuficiente, retries descontrolados, costos, recovery, permisos y
estado corrupto— son coherentes con controles ya preservados, pero no se usan
para crear requisitos porque su evidencia es anecdótica y variable.

Una señal comunitaria que sugiera una propiedad nueva deberá pasar por una acción
de investigación separada y buscar corroboración en especificaciones, sistemas
maduros, investigación o incidentes verificables antes de modificar este mapa.

---

## 15. Ownership de invariantes y delta de research

Este mapa **no es dueño de las leyes normativas que cita**.

- `SECURITY.md` es dueño de las invariantes de seguridad, autoridad, Prompt &
  Context Trust, delegación no expansiva, containment, disclosure e
  interoperabilidad segura.
- Las especificaciones y contratos de Memory/Admission son dueños de sus estados,
  bindings y separaciones operativas vigentes.
- Governance e `ideas.md` son dueños de límites e intención de self-improvement.
- Long Horizon y las referencias conceptuales especializadas son dueños de la
  semántica detallada de task lifecycle, ejecución agentic efímera y recursos.
- `docs/development/malak_construction_protocol.md` es dueño del perfil y estado
  operativo de RDD, candidate-bound evidence y disciplina de construcción.

Este documento conserva únicamente:

```text
research line
research classification
external evidence ledger
research delta / gap
pointer to the applicable owner
```

Si una propiedad ya tiene dueño superior o especializado, este mapa debe
referenciarla en lugar de mantener una segunda copia mutable.

---

## 16. Qué NO debe crearse por esta reconciliación

Este documento no justifica crear ahora:

- `PromptInjectionManager`;
- `MemoryTrustManager`;
- `TrustedArtifactRegistry`;
- `DelegationManager`;
- `CompromiseManager`;
- `IncidentResponseEngine`;
- `HoneypotManager`;
- `SelfImprovementManager`;
- `AutonomyManager`;
- una universal MCP layer;
- una Perception Layer;
- un workflow engine universal;
- agentes permanentes de red/blue/purple team;
- auto-hack-back;
- auto-modificación productiva.

Cada abstracción futura deberá demostrar responsabilidad propia, necesidad real,
consumidores reales, autoridad mínima, observabilidad, testabilidad, rollback y
beneficio superior al Complexity Budget.

---

## 17. Orden de maduración conceptual sugerido

No constituye roadmap ni asignación de sprint.

Cuando el baseline produzca necesidad real, el orden lógico de evaluación sería:

```text
1. Prompt / Context Trust Boundary
2. Compromise Containment & Trust Revocation
3. Memory / Knowledge Trust Propagation & Poisoning Defense after candidate content identity
4. AI Supply-Chain Trust
5. Data Classification / Disclosure
6. Agent Identity & Delegation
7. Secure MCP/A2A interoperability adapters
8. Governed Procedural Learning
9. Multimodal Perception when justified
```

Este orden expresa dependencia conceptual, no prioridad de implementación.

La evidencia externa revisada el 2026-09-12 aumenta especialmente la fuerza de
`Agent Identity & Delegation`, provenance/candidate binding y durable execution,
pero no reordena por sí sola esta secuencia ni convierte una línea de
investigación en prioridad de implementación.

---

## 18. Estado

```text
Documento: Research Horizon Map / reconciliation
Autoridad: no normativa
Baseline modificado: no
Arquitectura aprobada: no
Sprint autorizado por este documento: ninguno
Implementación autorizada por este documento: ninguna
Estado operativo de RDD: owned by docs/development/malak_construction_protocol.md
```

### Resultado final

La revisión confirma que gran parte de la visión futura ya estaba distribuida
de forma coherente en Malāk, especialmente en Long Horizon, IDEA-001, IDEA-002,
IDEA-003, IDEA-005, IDEA-006, IDEA-013, IDEA-016, IDEA-019, IDEA-021, IDEA-023 e
IDEA-024.

Los gaps y refuerzos que merecen permanecer visibles son principalmente:

1. `Compromise Containment & Trust Revocation` sistémico, sin duplicar la política de `SECURITY.md`;
2. `Memory & Knowledge Trust / Poisoning` más allá de Governed Projection
   Consumption, especialmente Candidate Content Identity/end-to-end binding,
   propagación de taint/revocation/quarantine y retrieval eligibility;
3. `AI Supply-Chain Trust` para artefactos AI y externos;
4. `Agent Identity & Delegation` verificable y revocable;
5. `Data Classification & Disclosure Control` transversal;
6. generalización operacional de `Prompt & Context Trust Boundary`;
7. investigación sobre lineage, candidate-bound receipts, provenance y validez
   del harness, cuyo estado de admisión pertenece al Construction Protocol;
8. lifecycle durable de tasks/procesos como refuerzo de Long Horizon, no como
   justificación para introducir ahora un workflow engine o una TUI compleja.

Ninguno de estos gaps constituye por sí mismo autorización para crear una nueva
capability, componente o sprint.
