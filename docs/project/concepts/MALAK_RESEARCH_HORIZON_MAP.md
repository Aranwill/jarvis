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
| Prompt & Context Trust Boundary | `REINFORCE_EXISTING` | IDEA-006 / IDEA-013 / IDEA-016 | Existe protección de prompt injection para evidencia externa, pero debe generalizarse a todo contenido no confiable. |
| Memory & Knowledge Trust / Poisoning | `REINFORCE_EXISTING` | Episodic Admission + Provenance + Producer Authorization + Governed Projection/Consumption + futura Memory + IDEA-013 / IDEA-016 | El baseline ya valida provenance estructural, autorización scoped del productor, proyección gobernada y consumo controlado hacia Admission; permanecen pendientes Candidate Content Identity/propagación y trust, taint, revocation y quarantine hacia persistencia, retrieval y Knowledge. |
| AI Supply-Chain Trust | `GAP_CANDIDATE` | IDEA-004 / IDEA-009 / IDEA-011 / IDEA-016 | Existen hashes, model governance y SLSA como referencia, pero falta una política conceptual unificada de admisión de artefactos AI. |
| Agent Identity & Delegation | `GAP_CANDIDATE` | IDEA-005 / IDEA-024 / Security Control Plane | Identidad, TTL, scopes y no autoelevación existen; falta cadena de delegación verificable y revocación derivada. |
| Compromise Containment & Trust Revocation | `GAP_CANDIDATE` | IDEA-019 / IDEA-001 / Security Control Plane | Existe cuarentena local; falta explicitar respuesta sistémica y propagación de desconfianza. |
| Data Classification & Disclosure Control | `GAP_CANDIDATE` | Context / Knowledge / Security | Least Context y minimización existen, pero no una clasificación transversal suficientemente explícita. |
| Governed Interoperability (MCP/A2A) | `WATCH` | adapters futuros / contratos internos | Preservar `protocol-ready, not protocol-dependent`; ningún protocolo externo será autoridad interna. |
| Governed Procedural Learning | `REINFORCE_EXISTING` | IDEA-002 / Skills-on-Demand / Knowledge Governance | La promoción de procedimientos aprendidos debe permanecer gobernada y no autoejecutable. |
| Multimodal Perception Boundary | `WATCH` | futura Interface/Perception boundary | Visión, audio y otras percepciones son relevantes a largo plazo, sin necesidad actual de nuevo subsistema. |
| World models | `WATCH` | futura investigación de percepción/entorno | No existe necesidad actual; reevaluar solo si tareas reales demuestran valor. |
| Autonomous self-modification | `CONFLICTS_WITH_VISION` | — | La automodificación productiva autónoma permanece prohibida; la mejora debe seguir siendo gobernada y basada en propuestas. |

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

IDEA-002 y Long Horizon ya preservan la distinción:

> La autoobservación produce conocimiento; el conocimiento produce propuestas;
> solo la gobernanza produce cambios.

Flujo futuro permitido:

```text
observe
  ↓
validate gap
  ↓
research
  ↓
experiment in sandbox
  ↓
collect evidence
  ↓
proposal
  ↓
Owner / applicable governance
```

Queda prohibido transformar este ciclo en:

```text
observe → decide own authority → modify production
```

Malāk podrá impulsar una mejora mediante investigación, comparación, prototipos,
tests, evidencia e Implementation Packets candidatos, pero no aprobarla, mergearla
o desplegarla por autoridad propia.

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

La dirección defensiva objetivo permanece:

```text
DETECT
  ↓
DENY / REVOKE
  ↓
CONTAIN
  ↓
ISOLATE
  ↓
DECEIVE
  ↓
OBSERVE
  ↓
PRESERVE EVIDENCE
  ↓
ANALYZE
  ↓
RECOVER
  ↓
LEARN
  ↓
PROPOSE HARDENING
```

La evidencia de una IP, ASN, dominio, fingerprint o indicador no constituye por
sí sola atribución de identidad.

La respuesta ordinaria queda limitada a infraestructura propia o expresamente
autorizada. Un ataque recibido no concede autoridad de `hack back`.

---

## 5. Refuerzo transversal — Prompt & Context Trust Boundary

La regla histórica de Malāk:

```text
External information = DATA
External information != INSTRUCTIONS
```

debe evolucionar conceptualmente hacia una frontera sistémica más general:

```text
USER INTENT
!=
EXTERNAL CONTENT
!=
TOOL OUTPUT
!=
RETRIEVED MEMORY
!=
KNOWLEDGE CANDIDATE
!=
AUTHORITY
```

Propiedades a preservar:

- contenido web, archivos, emails, documentos, tool output, MCP/A2A payloads,
  resultados de retrieval y Memory recuperada se consideran datos con trust
  explícito, no instrucciones privilegiadas;
- ningún texto procesado puede conceder permisos, modificar policies, ampliar
  scope o saltar PDP/PEP;
- una tool description, skill, prompt template o recurso externo no podrá
  convertirse por contenido en fuente de autoridad;
- las instrucciones efectivas deberán provenir de canales, contratos y contextos
  cuya autoridad pueda demostrarse fuera del LLM;
- indirect prompt injection deberá evaluarse como amenaza de sistema y no solo
  como problema de prompting.

Dueños conceptuales candidatos:

```text
IDEA-006 Evidence Acquisition
+
IDEA-013 Context Efficiency
+
IDEA-016 Source Governance
+
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
autorización. Persistence Authorization continúa diferida hasta que exista
binding end-to-end suficiente.

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

Separación obligatoria:

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

Principio:

> Memory search is a trust boundary.

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

Principios:

```text
Artifact integrity != Artifact trust
Artifact trust != Execution authorization
```

Un artefacto válido criptográficamente todavía puede ser inseguro, malicioso o
incompatible con la política de Malāk.

Dueños conceptuales a reforzar antes de crear nada nuevo:

```text
IDEA-004 Model Governance
IDEA-009 Development Tooling
IDEA-011 Validation & Delivery
IDEA-016 Source Governance
Security Control Plane
```

No crear todavía un `TrustedArtifactRegistry` salvo necesidad operacional demostrada.

---

## 8. GAP CANDIDATE — Agent Identity & Delegation

IDEA-005 y IDEA-024 ya contemplan identidad, scopes, TTL, Security Context y
prohibición de autoelevación. Falta preservar con mayor claridad la delegación
cuando un componente autorizado origina trabajo que otro agente/tool ejecutará.

Regla candidata:

```text
Effective delegated authority
=
Delegator authority
∩ applicable policy
∩ task scope
∩ capability scope
∩ resource limits
∩ TTL
```

Nunca:

```text
delegation → authority expansion
```

Una futura cadena de delegación podrá necesitar evidencia de:

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

La revocación del contexto padre deberá poder invalidar autoridad derivada cuando
la política lo requiera.

La identidad criptográfica fuerte, firmas, nonce/replay protection, PKI y
mecanismos equivalentes permanecen sujetos a diseño y revisión propios.

---

## 9. GAP CANDIDATE — Compromise Containment & Trust Revocation

IDEA-001 e IDEA-019 ya contemplan kill switch, quarantine, destrucción de sandbox,
revocación y niveles de contingencia. El gap identificado es convertir esa
respuesta local en una propiedad sistémica de componentes reemplazables.

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

Principio rector candidato:

> Compromise must reduce authority, never expand investigation privileges.

Secuencia defensiva candidata:

```text
SUSPECT
  ↓
FREEZE / REVOKE AUTHORITY
  ↓
CUT OR RESTRICT COMMUNICATION
  ↓
ISOLATE
  ↓
QUARANTINE
  ↓
PRESERVE EVIDENCE
  ↓
ASSESS BLAST RADIUS
  ↓
MARK RELATED STATE / CREDENTIALS / ARTIFACTS AS SUSPECT
  ↓
ROTATE / REVOKE / REVALIDATE
  ↓
REBUILD FROM KNOWN-GOOD
  ↓
RESTORE ONLY TRUSTED STATE
  ↓
VERIFY BEFORE REINTRODUCTION
```

Debe evitarse eliminar inmediatamente un componente si eso destruye evidencia
forense necesaria.

Preferencia futura:

```text
compromised component
        ↓
discard after evidence preservation
        ↓
instantiate known-good component
        ↓
verify identity + provenance
        ↓
restore only trusted state
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

la contención deberá poder evaluar:

```text
A → QUARANTINE
B → REVOKE / ROTATE candidate
C/D/E → SUSPECT → VALIDATE
```

La relación no implica que todos los activos estén comprometidos, sino que su
trust debe volver a demostrarse cuando el riesgo lo justifique.

La detección, revocación y preservación de evidencia crítica no deberán depender
de la cooperación del componente sospechado.

Dueños conceptuales a reforzar:

```text
Security Control Plane
IDEA-001 Sandbox / Evidence
IDEA-019 Incident Response / Deception
IDEA-005 Secure Context
IDEA-021 Emergency Control Surface
```

---

## 10. GAP CANDIDATE — Data Classification & Disclosure Control

`Least Context`, privacidad y minimización ya existen como principios, pero la
futura expansión de Malāk hacia Memory, tools, agents y servicios externos
requerirá distinguir explícitamente la sensibilidad y el uso permitido de datos.

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

Principio:

```text
Having access to data
!=
permission to disclose, persist or reuse it
```

No crear todavía un sistema universal de labels. Primero deberá existir una
superficie real que necesite esta clasificación.

---

## 11. Interoperabilidad gobernada

La dirección preservada es:

```text
Malāk Capability / Tool Contract
          │
          ▼
Interoperability Adapter
       ┌──┴───┐
       ▼      ▼
      MCP     A2A
```

Principio:

> Protocol-ready, not protocol-dependent.

Reglas futuras:

- MCP, A2A o protocolos equivalentes no entran al Kernel como autoridad;
- adapters consumen contratos internos de Malāk;
- mensajes y tool outputs externos se tratan como contenido no confiable;
- identidad externa no se convierte automáticamente en identidad interna;
- cada operación protegida continúa pasando por Security Control Plane;
- tool metadata, schemas o descripciones no conceden permisos;
- egress, recursos, secretos y scope continúan gobernados por Malāk.

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

Esta sección es el **registro canónico de evidencia externa** para este documento.
Su objetivo es evitar copiar catálogos de fuentes en `SECURITY.md`, `ideas.md`,
roadmaps u otras referencias y reducir así drift documental.

La evidencia externa:

```text
puede reforzar una propiedad
puede demostrar un gap
puede justificar mantener una línea bajo WATCH

pero

NO modifica la jerarquía documental
NO crea una capability
NO promueve una idea al roadmap
NO autoriza un sprint
NO convierte una práctica externa en arquitectura de Malāk
```

### 14.1. Clases de evidencia

Para esta reconciliación se usa la siguiente precedencia orientativa:

```text
E1 — estándares, organismos públicos, especificaciones formales
E2 — documentación primaria de sistemas/productos y postmortems verificables
E3 — investigación académica publicada o revisada
E4 — implementación open-source inspeccionable
E5 — comunidades, foros y experiencia anecdótica
```

La precedencia no sustituye el análisis de aplicabilidad. Una fuente `E1` puede
ser irrelevante para Malāk y una observación `E4` puede revelar una propiedad
útil. Las fuentes `E5` sirven para detectar fricción operativa o corroborar una
tendencia; no deben establecer por sí solas requisitos de seguridad, arquitectura
o gobernanza.

### 14.2. Registro de fuentes

| ID | Clase | Fuente primaria | Evidencia relevante para Malāk |
|---|---|---|---|
| `EXT-01` | `E1` | NIST, *Back to the Future: Why Agentic AI Needs a Strong Identity Foundation*, 2026-08-27 — https://www.nist.gov/blogs/cybersecurity-insights/back-future-why-agentic-ai-needs-strong-identity-foundation | Los guardrails del modelo no bastan para seguridad agentic; identidad fuerte y credenciales/autorizaciones acotadas son fundaciones del sistema. |
| `EXT-02` | `E1` | ACSC + CISA + NSA + Cyber Centre Canadá + NCSC-NZ + NCSC-UK, *Careful adoption of agentic AI services*, 2026-05-01 — https://www.cyber.gov.au/business-government/secure-design/artificial-intelligence/careful-adoption-of-agentic-ai-services | Recomienda least privilege, agentes como principals criptográficos distintos, credenciales efímeras, límites de recursos, aislamiento, human control points, monitoreo, rollback y autorización verificada en runtime. |
| `EXT-03` | `E1` | ASD, *Agentic AI Harnesses — The layer above the model*, 2026-09-11 — https://www.cyber.gov.au/business-government/secure-design/artificial-intelligence/agentic-ai-harnesses | El harness y la infraestructura circundante deben aplicar seguridad, gobernanza, validación, supervisión y supply-chain assurance en lugar de depender solo del comportamiento del modelo o del prompt. |
| `EXT-04` | `E2` | Google Developers, *Build zero-trust AI agents with Google's Agent Development Kit*, 2026-08-17 — https://developers.googleblog.com/build-zero-trust-ai-agents-with-googles-agent-development-kit/ | Los agentes que mutan estado real requieren fronteras Zero Trust y validación determinista fuera del LLM. |
| `EXT-05` | `E2` | Anthropic, *How we contain Claude across products*, 2026-05-25 — https://www.anthropic.com/engineering/how-we-contain-claude | Refuerza containment por entorno y blast-radius control; los controles probabilísticos del modelo no sustituyen fronteras duras. También documenta approval fatigue, por lo que Human in Control no debe reducirse a pedir permiso por cada microacción. |
| `EXT-06` | `E1` | A2A Protocol, specification — https://a2a-protocol.org/dev/specification/ | `TASK_STATE_AUTH_REQUIRED` no constituye autorización; scope, validez y revocación deben definirse y verificarse antes de ejecutar. |
| `EXT-07` | `E1` | OWASP GenAI Security Project, *Top 10 for Agentic Applications 2026*, 2025-12-09 — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ | Goal hijack, tool misuse, identity/privilege abuse, supply chain, memory/context poisoning, insecure inter-agent communication, cascading failures, human-agent trust exploitation y rogue agents coinciden con amenazas ya preservadas en Malāk. |
| `EXT-08` | `E2` | OWASP GenAI Security Project, *Memory Is a Feature. It Is Also an Attack Surface*, 2026-05-13 — https://genai.owasp.org/2026/05/13/memory-is-a-feature-it-is-also-an-attack-surface/ | El estado persistente puede transportar prompt injection y contaminación más allá de la interacción original; refuerza Memory admission, taint, revocation y quarantine. |
| `EXT-09` | `E1` | W3C, *PROV-Overview*, 2013 — https://www.w3.org/TR/prov-overview/ | Modela provenance mediante entidades, actividades y agentes; aporta vocabulario maduro para derivación, atribución y trazabilidad sin confundir provenance con autoridad. |
| `EXT-10` | `E1` | SLSA v1.2, *Provenance* — https://slsa.dev/spec/v1.2/provenance | Provenance verificable describe dónde, cuándo y cómo se produjo un artefacto; refuerza AI Supply-Chain Trust y el futuro binding de evidencia a candidatos. |
| `EXT-11` | `E1` | seL4, *Capabilities* — https://docs.sel4.systems/Tutorials/capabilities.html | En seL4 una capability es un token no falsificable que porta derechos concretos. No equivale al término funcional `Capability` de Malāk; sirve como precedente de autoridad explícita, mínima y verificable. |
| `EXT-12` | `E3` | Google, *Zanzibar: Google's Consistent, Global Authorization System*, USENIX ATC 2019 — https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/ | Muestra autorización como infraestructura separada, consistente y centralmente evaluable en lugar de inferencia dispersa en cada consumidor. |
| `EXT-13` | `E1` | SPIFFE, workload identity specifications — https://spiffe.io/docs/latest/spiffe/concepts/ | SVIDs aportan identidad criptográficamente verificable y de corta vida para workloads; refuerza Agent Identity, revocabilidad y separación entre identidad del workload y credenciales humanas. |
| `EXT-14` | `E2` | Kubernetes, *Controllers* — https://kubernetes.io/docs/concepts/architecture/controller/ | Control loops comparan estado deseado y observado; refuerza una futura reconciliación de identity/runtime/resource state sin asumir que una autorización histórica sigue vigente. |
| `EXT-15` | `E2` | Erlang/OTP, *Supervisor Behaviour* — https://www.erlang.org/doc/system/sup_princ.html | Supervision trees, restart strategies y restart intensity aportan precedentes maduros para lifecycle, contención de fallos y escalamiento de procesos. |
| `EXT-16` | `E2` | Temporal, documentation — https://docs.temporal.io/ | Durable execution preserva progreso ante crashes/fallos y refuerza que retries, resume/replay, idempotencia y compensación deben tratarse como problemas explícitos antes de repetir side effects. |
| `EXT-17` | `E1` | OpenTelemetry, *Context propagation* — https://opentelemetry.io/docs/concepts/context-propagation/ | Trace/span context permite reconstruir causalidad a través de procesos y servicios; útil para observabilidad, sin convertir telemetry en evidencia o autoridad por sí sola. |
| `EXT-18` | `E2` | OpenAI, *A shared playbook for trustworthy third party evaluations*, 2026-05-29 — https://openai.com/index/trustworthy-third-party-evaluations-foundations/ | La validez de una evaluación depende también de harness, herramientas, entorno y configuración; refuerza candidate-bound evidence más allá del resultado final. |
| `EXT-19` | `E2` | OpenAI, *Separating signal from noise in coding evaluations*, 2026-07-08 — https://openai.com/index/separating-signal-from-noise-coding-evaluations/ | Una auditoría estimó ~30 % de tareas problemáticas en SWE-Bench Pro; un PASS puede ser evidencia defectuosa si el instrumento de evaluación no es válido. |
| `EXT-20` | `E2` | Anthropic, *Demystifying evals for AI agents*, 2026-01-09 — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents | Evals agentic deben considerar trayectorias multistep, tools y cambios de estado; refuerza evidencia de proceso y no solo evaluación de output final. |
| `EXT-21` | `E3` | USENIX Security 2026, *AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via Causal Attribution of Tool Invocations* — https://www.usenix.org/conference/usenixsecurity26/presentation/he-yu | Propone atribución causal de tool calls para distinguir intención del usuario de observaciones no confiables. Resultado prometedor, todavía experimental: `WATCH`. |
| `EXT-22` | `E4` | Gentleman Programming, `gentle-pi`, inspeccionado en `main@6e4478c04615b0c013a017178dcfefa51579982d` — https://github.com/Gentleman-Programming/gentle-pi | RDD nativo conserva candidate freeze, lineage, receipts ligados al candidato, correction acotada y review sin delivery authority; su TUI separa procesos RPC, estado tipado, concurrencia acotada y proyección de UI. La propia línea RDD se declara inestable, por lo que se usa como evidencia de implementación, no como metodología a copiar. |

### 14.3. Mapeo de evidencia → lógica de Malāk

| Propiedad / línea | Evidencia principal | Disposición | Consecuencia para Malāk |
|---|---|---|---|
| `Model != System` / hard boundaries | `EXT-02`, `EXT-03`, `EXT-04`, `EXT-05` | `REINFORCE_EXISTING` | Mantener PDP/PEP, sandbox/containment y validadores deterministas fuera del LLM. |
| Capability funcional / autoridad explícita / least privilege | `EXT-02`, `EXT-11`, `EXT-12` | `ALIGNED` | Preservar `Capability != Permission` en la semántica propia de Malāk. El modelo capability-security de seL4 se usa solo como precedente de derechos explícitos, no como equivalencia terminológica. |
| Agent Identity & Delegation | `EXT-01`, `EXT-02`, `EXT-06`, `EXT-13` | `GAP_CANDIDATE` | La evidencia eleva la relevancia de identidad criptográfica, TTL, revocación y delegación verificable, pero no autoriza diseño ni sprint. |
| Human in Control | `EXT-02`, `EXT-05` | `REINFORCE_EXISTING` | Mantener autoridad humana para decisiones sensibles y reducir approval fatigue mediante límites duros y checkpoints significativos. |
| Prompt / Context Trust Boundary | `EXT-02`, `EXT-03`, `EXT-05`, `EXT-07`, `EXT-21` | `REINFORCE_EXISTING` | Tratar tool output y contenido recuperado como datos no confiables; mantener causal attribution bajo `WATCH`. |
| Memory & Knowledge Trust / Poisoning | `EXT-07`, `EXT-08` | `REINFORCE_EXISTING` | Refuerza admission, content binding, taint, revocation, quarantine y trust-aware retrieval antes de Memory persistente. |
| AI Supply-Chain Trust / provenance | `EXT-02`, `EXT-09`, `EXT-10` | `GAP_CANDIDATE` | Reutilizar provenance e integrity concepts; no crear registry universal sin necesidad operacional. |
| RDD Stage 2 / lineage / receipts | `EXT-09`, `EXT-10`, `EXT-18`, `EXT-19`, `EXT-20`, `EXT-22` | `OBSERVE` | Hay evidencia fuerte para investigar lineage, receipt y harness identity; **RDD Stage 2 permanece NOT AUTHORIZED**. |
| Durable task/process lifecycle | `EXT-14`, `EXT-15`, `EXT-16`, `EXT-17`, `EXT-22` | `ALIGNED` / `REINFORCE_EXISTING` | Long Horizon ya posee dueño conceptual; futuras ejecuciones deberán considerar supervision, reconciliation, idempotencia, replay y compensación antes de una TUI compleja. |
| Resource Governance | `EXT-02`, `EXT-15`, `EXT-22` | `ALIGNED` | Concurrencia, tiempo, retries y procesos deben permanecer acotados y observables. |
| Interoperabilidad A2A/MCP | `EXT-06`, `EXT-07` | `WATCH` | Un estado/protocolo externo no transfiere autoridad interna; adapters siguen subordinados a contratos y Security Control Plane de Malāk. |
| Observability / causal tracing | `EXT-17` | `REINFORCE_EXISTING` | Trace context puede mejorar reconstrucción causal, preservando `Telemetry != Evidence != Authority`. |
| Causal action attribution | `EXT-21` | `WATCH` | Línea prometedora para tool provenance/intention binding; no incorporar hasta madurez y necesidad demostradas. |
| Autonomous self-modification | evidencia externa no demuestra necesidad para cambiar la frontera actual | `CONFLICTS_WITH_VISION` | Mantener `Observation → Evidence → Finding → Proposal → Human/governance`. |

### 14.4. Contrafuerzos y límites derivados de la evidencia

La investigación no solo confirma decisiones; también introduce correcciones a
interpretaciones demasiado simples:

1. `Human in Control != Human approves everything`: el Owner conserva autoridad,
   pero la arquitectura debe reducir prompts repetitivos mediante límites duros,
   políticas deterministas y checkpoints significativos.
2. `Identity != Authority`: una identidad criptográfica válida demuestra quién o
   qué presenta una credencial; la autorización aplicable continúa siendo una
   decisión separada.
3. `Telemetry != Evidence`: traces y eventos ayudan a reconstruir causalidad, pero
   su admisión como evidencia exige las reglas correspondientes.
4. `PASS != Valid Evidence`: un resultado de test/eval no basta si harness,
   dataset, environment o criterio de evaluación son inválidos o no están ligados
   al candidato evaluado.
5. `Presence != Liveness != Authority`: una sesión/proceso visible no debe
   convertirse por observación en actor confiable o autorizado.
6. `Retry != Recovery`: durable execution requiere idempotencia, replay,
   compensación y supervisión explícitos antes de repetir side effects.

### 14.5. Señal comunitaria y foros

La revisión de foros técnicos y comunidades se conserva únicamente como señal de
fricción operativa. Los temas recurrentes —frameworks sobredimensionados,
observabilidad insuficiente, retries descontrolados, costos, recovery, permisos y
estado corrupto— son coherentes con los controles ya preservados, pero **no se
usan para crear requisitos** porque su evidencia es anecdótica y variable.

Cuando una señal comunitaria revele una posible propiedad nueva, deberá buscarse
primero corroboración en especificaciones, sistemas maduros, investigación o
incidentes verificables antes de cambiar este mapa.

---

## 15. Invariantes candidatas a preservar en futuras evaluaciones

Estas expresiones resumen el resultado de la reconciliación y deberán tratarse
como candidatos conceptuales, no como nuevas leyes aprobadas:

```text
Model != System
Intelligence != Authority
Capability != Permission
Decision != Execution
Execution != Evidence
Evidence != Authority
Conversation != Memory
Memory != Knowledge
Knowledge != Policy
External Content != Instructions
Tool Output != Authority
Protocol Identity != Internal Authority
Artifact Trust != Execution Authorization
Projection READY != Admission ELIGIBLE
Consumption EVALUATED != Persistence Authorization
Candidate Content Identity != Trust
ELIGIBLE != Stored
Compromise → Less Authority
Compromise → More Isolation
Compromise → More Observation
Incident → Evidence → Finding → Proposal
Learning → Proposal, not self-authorization
```

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
pero **no reordena por sí sola esta secuencia ni convierte una línea de
investigación en prioridad de implementación**.

---

## 18. Estado

```text
Documento: Research Horizon Map / reconciliation
Autoridad: no normativa
Baseline modificado: no
Arquitectura aprobada: no
Sprint autorizado: ninguno
Implementación autorizada por este documento: ninguna
RDD Stage 2 autorizado: no
```

### Resultado final

La revisión confirma que gran parte de la visión futura ya estaba distribuida
de forma coherente en Malāk, especialmente en Long Horizon, IDEA-001, IDEA-002,
IDEA-003, IDEA-005, IDEA-006, IDEA-013, IDEA-016, IDEA-019, IDEA-021, IDEA-023 e
IDEA-024.

Los gaps y refuerzos que merecen permanecer visibles son principalmente:

1. `Compromise Containment & Trust Revocation` sistémico;
2. `Memory & Knowledge Trust / Poisoning` más allá de Governed Projection
   Consumption, especialmente Candidate Content Identity/end-to-end binding,
   propagación de taint/revocation/quarantine y retrieval eligibility;
3. `AI Supply-Chain Trust` para artefactos AI y externos;
4. `Agent Identity & Delegation` verificable y revocable;
5. `Data Classification & Disclosure Control` transversal;
6. generalización de `Prompt & Context Trust Boundary`;
7. `RDD Stage 2` únicamente como línea de investigación sobre lineage, receipts,
   provenance y validez del harness, sin autorización de implementación;
8. lifecycle durable de tasks/procesos como refuerzo de Long Horizon, no como
   justificación para introducir ahora un workflow engine o una TUI compleja.

Ninguno de estos gaps constituye por sí mismo autorización para crear una nueva
capability, componente o sprint.
