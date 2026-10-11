---
title: Malāk Research Horizon Map
status: concept
authority: non_normative
document_role: research_horizon_reconciliation
language: es
created: 2026-09-09
updated: 2026-10-10
as_of_branch: main
as_of_commit: 02daf578012c662f0686357aa48b25722897c82a
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

La mejora deberá buscar propiedades demostrables, no copiar workflows externos. La
preferencia conceptual es: observación determinista cuando sea suficiente; evidencia
estructurada; evaluación probabilística sólo cuando aporte información material; y
experimentación aislada antes de recomendar cambios estructurales.

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

El residual inmediato ya no es `Projection → Admission` ni Candidate Content
Identity. El baseline actual ya materializa identidad de contenido episódico,
su propagación/binding, Persistence Readiness y la composición gobernada del
`AuthorizationRequest` de persistencia. La frontera productiva continúa detenida
antes de la decisión/enforcement de autorización y antes de cualquier durable
write.

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
Persistence readiness
      ↓
Persistence AuthorizationRequest composition
      ↓
PDP decision / PEP enforcement              ← NOT PRODUCTIVELY WIRED
      ↓
Protected durable write                      ← NOT AUTHORIZED
      ↓
Stored Memory                                ← NOT AUTHORIZED
      ↓
Trust-aware retrieval eligibility
      ↓
Knowledge candidate when applicable
```

Estado material observado a `02daf578012c662f0686357aa48b25722897c82a`:

```text
candidate contracts                         implemented
admission policy                            implemented
assessment provenance                       implemented
assessment producer authorization           implemented
governed input projection                   implemented
projection -> admission consumption         implemented
candidate content identity                  implemented
content identity propagation                implemented
episodic persistence readiness              implemented
Persistence AuthorizationRequest composer   implemented / isolated
PDP / PEP security primitives               implemented generically
persistence decision/enforcement wiring      NOT AUTHORIZED
protected durable write                     NOT AUTHORIZED
persistent Memory                           NOT AUTHORIZED
retrieval                                   NOT AUTHORIZED
Knowledge promotion                         NOT AUTHORIZED
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

## 14. Relación con investigación de seguridad 2026

Las revisiones futuras deberán continuar contrastando Malāk contra, entre otros:

- OWASP Top 10 para aplicaciones web;
- OWASP Top 10 para aplicaciones LLM/GenAI;
- OWASP Agentic Security y Agent Control Standard;
- NIST AI RMF / perfiles de ciberseguridad para AI;
- MITRE ATLAS;
- investigación académica sobre prompt injection, tool poisoning, persistent
  state corruption, memory poisoning y delegated authority;
- incidentes reales de sistemas agentic y AI-assisted development.

Estos marcos son referencias de aplicabilidad, no fuentes de autoridad superiores
a Blueprint, Constituciones o Gobernanza.

La revisión deberá concentrarse en propiedades de sistema:

```text
information flow
identity
delegated authority
persistent state
supply chain
containment
provenance
detection
recovery
```

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

---

## 18. Estado

```text
Documento: Research Horizon Map / reconciliation
Autoridad: no normativa
Baseline modificado: no
Arquitectura aprobada: no
Sprint autorizado: ninguno
Implementación autorizada por este documento: ninguna
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
6. generalización de `Prompt & Context Trust Boundary`.

Ninguno de estos gaps constituye por sí mismo autorización para crear una nueva
capability, componente o sprint.

---

## 19. Evidence Map — artefactos externos revisados e insumos futuros

Revisión realizada: `2026-09-12`
Baseline contrastado: `Aranwill/jarvis/main@cd50c308e1f5a1481851d6402ae4435341410d27`
Suplemento de evidencia revisado: `2026-09-20`

Esta sección **agrega evidencia** a la reconciliación existente sin modificar ni
reclasificar las secciones 1–18.

Principio rector:

> **Malāk adopta propiedades demostradas, no arquitecturas externas.**

Una referencia preservada aquí describe un artefacto ya revisado y la propiedad
que se extrajo de él. No es una instrucción para volver a consultar Internet, no
es contenido confiable vivo, no es una dependencia y no adquiere autoridad sobre
la arquitectura de Malāk.

```text
artefacto externo revisado
        ↓
propiedad observada
        ↓
línea de Malāk relacionada
        ↓
future admission review
        ↓
ADOPT / ADAPT / OBSERVE / REJECT
        ↓
diseño propio de Malāk cuando corresponda
```

La lectura explícita de este documento y la clasificación de material futuro ya
están exigidas por `docs/development/malak_construction_protocol.md`. Por ello,
cuando una entrada marcada `IMPLEMENTATION_INPUT` sea materialmente relevante a
una capability o responsabilidad bajo admisión, deberá entrar en el inventario de
fuentes aplicables y recibir disposición explícita dentro de ese proceso.

Esto **no autoriza implementación**. Significa únicamente que la evidencia ya
obtenida no debe perderse ni quedar fuera del scope cuando llegue el momento de
diseñar o implementar la superficie relacionada.

### 19.1. Roles de uso futuro

```text
CORROBORATION
→ refuerza una decisión, límite o dirección que Malāk ya preserva.

IMPLEMENTATION_INPUT
→ si la línea relacionada entra en admission, la propiedad observada debe ser
  considerada y recibir disposición explícita antes del diseño/implementación.

WATCH_SIGNAL
→ señal relevante que todavía requiere nueva revalidación antes de convertirse
  en input de diseño.
```

Los roles pueden coexistir. Ninguno equivale a roadmap, prioridad, sprint,
aprobación o autoridad.

### 19.2. Ledger de evidencia revisada

| ID | Artefacto revisado / identidad | Alcance exacto revisado | Propiedad observada | Línea Malāk relacionada | Uso futuro | No implica |
|---|---|---|---|---|---|---|
| `EXT-01` | NIST — *Back to the Future: Why Agentic AI Needs a Strong Identity Foundation* — 2026-08-27 | identidad de agentes/workloads, credenciales acotadas y de corta vida, separación respecto de identidad humana | la seguridad agentic necesita identidad verificable y lifecycle de credenciales fuera del modelo | Agent Identity & Delegation / Security Control Plane | `CORROBORATION` + `IMPLEMENTATION_INPUT` | adoptar automáticamente OAuth, SPIFFE, JWT, X.509 o una PKI concreta |
| `EXT-02` | ACSC/CISA/NSA/Cyber Centre Canada/NCSC-NZ/NCSC-UK — *Careful adoption of agentic AI services* — 2026-05-01 | principals distintos, least privilege, credenciales efímeras, resource limits, human control points, aislamiento, monitoreo y rollback | la autoridad agentic debe estar acotada, verificable y revocable en runtime | Agent Identity / Resource Governance / Containment / Human in Control | `CORROBORATION` + `IMPLEMENTATION_INPUT` | importar su arquitectura o convertir controles externos en autoridad Malāk |
| `EXT-03` | ASD — *Agentic AI Harnesses — The layer above the model* — 2026-09-11 | seguridad, gobernanza, validación, monitoreo y assurance fuera del modelo | controles críticos deben vivir también en el sistema/harness y no depender del prompt o comportamiento probabilístico | `Model != System` / Security Control Plane | `CORROBORATION` | adoptar un harness concreto |
| `EXT-04` | Google Developers — *Build zero-trust AI agents with Google's Agent Development Kit* — 2026-08-17 | identidad/signing para writes, sandboxing, restricciones de egress/resources y gateways deterministas | side effects agentic requieren fronteras verificables fuera del LLM | Zero Trust / Sandbox / provenance / protected execution | `CORROBORATION` + `IMPLEMENTATION_INPUT` | adoptar ADK, gVisor o su composición concreta como diseño de Malāk |
| `EXT-05` | Anthropic — *How we contain Claude across products* — 2026-05-25 | containment, blast radius, approval fatigue, tool output, memory y subagent trust | hard boundaries deben sobrevivir a fallos probabilísticos; Human in Control no debe reducirse a aprobación de cada microacción | Containment / Prompt & Context Trust / Human in Control | `CORROBORATION` + `IMPLEMENTATION_INPUT` | eliminar checkpoints humanos reservados ni copiar su infraestructura |
| `EXT-06` | A2A Protocol — specification revisada 2026-09-12; snapshot externo inmutable no preservado | semántica de `TASK_STATE_AUTH_REQUIRED`, scope, validez y revocación | requerir autorización no equivale a poseer autorización para ejecutar | Governed Interoperability / Authorization | `CORROBORATION` + `WATCH_SIGNAL` | adoptar A2A como autoridad interna o protocolo obligatorio |
| `EXT-07` | OWASP GenAI Security Project — *Top 10 for Agentic Applications 2026* — 2025-12-09 | goal hijack, tool misuse, privilege abuse, supply chain, memory/context poisoning, inter-agent communication, cascading failures y rogue agents | el threat model agentic requiere controles sistémicos más allá de prompting | Security Horizon / agents / tools / Memory | `CORROBORATION` | implementar una taxonomía OWASP como arquitectura |
| `EXT-08` | OWASP GenAI Security Project — *Memory Is a Feature. It Is Also an Attack Surface* — 2026-05-13 | contaminación persistente y memory/context poisoning entre interacciones | Memory persistente es una frontera de trust capaz de transportar compromiso | Memory & Knowledge Trust / Poisoning | `CORROBORATION` + `IMPLEMENTATION_INPUT` | adoptar un memory framework o habilitar persistencia |
| `EXT-09` | W3C — *PROV-Overview* — 2013 | entidades, actividades, agentes, derivación, atribución y provenance | provenance puede representarse separadamente de decisión y autoridad | AI Supply-Chain Trust / evidence lineage / future RDD | `IMPLEMENTATION_INPUT` | adoptar el modelo PROV completo o sus schemas como contrato Malāk |
| `EXT-10` | SLSA v1.2 — *Provenance* | identidad del artefacto y attestations sobre cómo fue producido | provenance/integridad puede ligar un artefacto a su proceso de producción sin autorizar su uso | AI Supply-Chain Trust / candidate evidence | `IMPLEMENTATION_INPUT` | adoptar SLSA completo ni convertir provenance en autorización |
| `EXT-11` | seL4 — documentación de *Capabilities* revisada 2026-09-12; snapshot externo inmutable no preservado | tokens no falsificables con derechos explícitos y acotados | autoridad mínima explícita puede expresarse mediante derechos verificables | Capability First / explicit authority | `CORROBORATION` + `IMPLEMENTATION_INPUT` | equiparar la `capability` de seL4 con la Capability funcional de Malāk |
| `EXT-12` | Google — *Zanzibar: Google's Consistent, Global Authorization System* — USENIX ATC 2019 | autorización como infraestructura separada, consistente y evaluable | autorización merece semántica/control propios y no inferencias dispersas por consumidor | Security Control Plane / Authorization | `CORROBORATION` + `IMPLEMENTATION_INPUT` | copiar Zanzibar o introducir infraestructura global innecesaria |
| `EXT-13` | SPIFFE — workload identity specifications/docs revisadas 2026-09-12; snapshot externo inmutable no preservado | workload identity verificable y credenciales de vida acotada | una identidad de workload puede separarse de identidad humana y tener lifecycle propio | Agent Identity & Delegation | `IMPLEMENTATION_INPUT` | seleccionar SPIFFE automáticamente como implementación |
| `EXT-14` | Kubernetes — patrón/documentación de Controllers revisada 2026-09-12; snapshot externo inmutable no preservado | desired state, observed state y reconciliation loop | sistemas dinámicos deben poder reconciliar estado deseado con estado realmente observado | Durable Cognitive Execution / runtime lifecycle | `IMPLEMENTATION_INPUT` | Kubernetes, controller-runtime o sus APIs como dependencia |
| `EXT-15` | Erlang/OTP — Supervisor Behaviour docs revisadas 2026-09-12; snapshot externo inmutable no preservado | supervision trees, restart strategies y restart intensity | recuperación de procesos requiere supervisión explícita y límites, no reinicio ciego | Task / process lifecycle / Resource Governance | `IMPLEMENTATION_INPUT` | copiar OTP, sus estrategias o límites numéricos |
| `EXT-16` | Temporal — documentación de durable execution revisada 2026-09-12; snapshot externo inmutable no preservado | persistencia de progreso, retries/replay, idempotencia, side effects y compensation | ejecución durable exige semántica explícita de retry/resume/replay/idempotence/compensation | Long Horizon / Durable Cognitive Execution | `IMPLEMENTATION_INPUT` | adoptar Temporal como workflow engine de Malāk |
| `EXT-17` | OpenTelemetry — context propagation docs revisadas 2026-09-12; snapshot externo inmutable no preservado | trace/span context y propagación causal entre procesos/servicios | correlación causal puede mejorar observabilidad sin convertir telemetry en evidencia o autoridad | Observability / forensics / long-horizon execution | `IMPLEMENTATION_INPUT` | convertir spans/logs en evidencia canónica automáticamente |
| `EXT-18` | OpenAI — *A shared playbook for trustworthy third party evaluations* — 2026-05-29 | modelo, tools, harness, environment, safeguards, budget y validity checks como contexto de una evaluación | un resultado de evaluación no es interpretable sin contexto suficiente sobre cómo fue producido | RDD evolution / validation evidence | `CORROBORATION` + `IMPLEMENTATION_INPUT` | autorizar RDD Stage 2 ni copiar un harness de evaluación |
| `EXT-19` | OpenAI — *Separating signal from noise in coding evaluations* — 2026-07-08 | calidad de tareas, tests y cobertura como condición de validez de evaluación | `PASS` no garantiza evidencia válida si el instrumento de evaluación está defectuoso | Engineering validation / future RDD | `CORROBORATION` | tratar benchmarks externos como autoridad |
| `EXT-20` | Anthropic — *Demystifying evals for AI agents* — 2026-01-09 | trayectorias multistep, tool calls y cambios de estado en evaluaciones agentic | evaluar solo output final puede ocultar fallos importantes de proceso | Agent evaluation / future validation | `CORROBORATION` + `IMPLEMENTATION_INPUT` | adoptar su framework o métricas sin revalidación propia |
| `EXT-21` | USENIX Security 2026 — *AttriGuard: Defeating Indirect Prompt Injection in LLM Agents via Causal Attribution of Tool Invocations* | causal attribution de tool invocations frente a indirect prompt injection | vincular una acción con su causa/intención puede ayudar a distinguir user intent de contenido no confiable | Prompt & Context Trust / tool provenance | `WATCH_SIGNAL` | asumir madurez suficiente ni incorporar el método experimental ahora |
| `EXT-22` | Gentleman Programming `gentle-pi` — `main@6e4478c04615b0c013a017178dcfefa51579982d` | native RDD workflow, review integration, runner/protocol, task lifecycle y presence projection | candidate freeze, explicit lineage, candidate-bound receipts, bounded correction, review sin delivery authority, typed lifecycle y bounded concurrency son propiedades implementables | future RDD / Task lifecycle / agent execution | `IMPLEMENTATION_INPUT` + `WATCH_SIGNAL` | copiar Pi, OpenSpec, schemas, defaults, CLI/TUI, authority model ni autorizar RDD Stage 2 |
| `EXT-23` | Anthropic — *How we built our multi-agent research system* / agent-team patterns revisados 2026-09-20 | coordinación de subagentes, paralelismo, espera y persistencia de resultados fuera del coordinador | el trabajo largo puede progresar mediante dependencias y artefactos sin convertir chat libre ni contexto vivo en fuente de estado | Governed Swarm / Long Horizon / Task State | `CORROBORATION` + `IMPLEMENTATION_INPUT` | copiar su harness, mantener agentes vivos por defecto o adoptar su modelo de autoridad |
| `EXT-24` | Microsoft AutoGen — GraphFlow docs revisadas 2026-09-20 | fan-out, joins `all/any`, branching y loops explícitos en grafos dirigidos | dependencias de tareas pueden tener semántica estructurada y evaluable fuera del razonamiento libre del agente | Execution Graph / Mission Orchestration | `IMPLEMENTATION_INPUT` + `WATCH_SIGNAL` | adoptar AutoGen, su runtime o sus APIs como dependencia |
| `EXT-25` | Gentleman Programming — Gentle AI ODD/RDD, `main` revisado 2026-09-20 | ODD separa autorización, exploración, incertidumbre, proporcionalidad y ejecución; RDD revisa candidatos terminados con identidad/evidencia acotada | separar método de trabajo, assurance y delivery evita convertir una metodología externa en autoridad; formalizar sólo cuando complejidad/recoverability lo justifiquen | Engineering Method / future RDD / Engineering Intelligence | `CORROBORATION` + `IMPLEMENTATION_INPUT` | adoptar ODD/RDD como framework, copiar Engram como Task State o importar sus heurísticas numéricas |

| `EXT-26` | Stanford MAST — Agent JIT Compilation, ICML 2026 | planes ejecutables con pre/postcondiciones, validación contra tools y selección considerando coste | planes y decisiones de ejecución pueden expresarse mediante contratos verificables antes de delegar razonamiento libre | Execution Contracts / Planning / deterministic validation | `IMPLEMENTATION_INPUT` + `WATCH_SIGNAL` | adoptar su planner, compiler, tool protocol o arquitectura completa |
| `EXT-27` | Zheng et al. — *Dream-RSI: Recursive Self-Improvement through Evolving Worlds*, arXiv:2609.14858 + official `zhengkid/Dream-RSI`, revisados 2026-10-10 | historial de discovery como replay simulator y evaluación off-policy de políticas de exploración sin modificar el coding agent subyacente | estudiar replay contrafactual gobernado para comparar estrategias de exploración con evidencia histórica antes de ejecutar nuevas trayectorias costosas | IDEA-002 / Governed Self-Review / Trace & Replay / future Sandbox | `CORROBORATION` + `RESEARCH_INPUT` | adoptar recursive self-modification, promoción automática de policy, tratar replay como verdad/memoria/autoridad o introducir un `DreamManager` |


### 19.3. Regla de revalidación

El ledger preserva **lo que fue revisado en esta fecha**, no lo que una fuente
externa pueda contener después.

```text
artifact identity
!= live external content

external evidence
!= trusted instruction

implementation input
!= implementation authorization
```

Si una futura admission review necesita comprobar que una propiedad externa sigue
vigente, cambió materialmente o requiere mayor detalle, esa comprobación debe ser
una acción de research nueva, explícita y acotada. El contenido nuevo no sustituye
silenciosamente lo registrado aquí.

### 19.4. Research Incubation Backlog — QA, Dreams y Methodology Distillation

Este backlog preserva líneas solicitadas por el Owner para futuras evaluaciones.
No crea una `EXT`, Capability, subsystem, service, manager, sprint ni dependencia.

Frontera común:

```text
research entry != roadmap
research method != capability
metric != proof of quality
finding != refactor authorization
counterfactual != fact
external system != authority
```

#### A. Software Quality Assurance & Engineering Research

**Disposición:** `ADAPT / REINFORCE_EXISTING / RESEARCH`.

Dueños existentes que deben reutilizarse antes de crear cualquier superficie:

- IDEA-009 — Development Tooling Foundation;
- IDEA-014 — Complexity Budget Foundation;
- IDEA-017 — External Research & Assurance Review;
- `STD-001 Coding Standards`;
- `LPK-001 Clean Code - Functions`;
- Engineering Method, Construction Protocol, 4R y candidate-bound validation.

Líneas a investigar y medir de forma proporcional:

```text
QA procedures
├── quality planning / acceptance criteria
├── verification strategy
├── regression strategy
├── defect classification
├── candidate/release quality evidence
└── quality gates

Test Coverage
├── line coverage
├── branch coverage
├── coverage delta
├── critical-contract coverage
└── uncovered-risk analysis

Test Effectiveness
├── Mutation Testing
├── mutation score
├── surviving-mutant analysis
├── weak-test detection
└── redundant-test detection when demonstrable

Advanced Testing
├── Property-Based Testing
├── invariant testing
├── boundary / negative testing
├── regression testing
└── fuzzing when applicable

Quality Metrics
├── cyclomatic / cognitive complexity
├── duplication
├── coupling / cohesion
├── maintainability
├── public-surface growth
├── dependency growth
└── change blast radius

Test Health
├── flaky-test detection
├── test runtime
├── failure / regression rate
└── deterministic reproducibility

Static Quality
├── linting
├── type checking
├── dead-code detection
├── dependency analysis
└── security/static analysis

Quality Evolution
├── Quality Baseline
├── candidate vs baseline
├── Quality Regression
└── Quality Drift
```

`Clean Code` se conserva como sublínea de mantenibilidad, no como autoridad ni
dogma. La meta es evidencia de legibilidad, simplicidad, coupling, cohesión,
duplicación y coste de cambio, no una refactorización estética automática.

Guardrails:

```text
coverage != test quality
mutation score != correctness
lint PASS != maintainability
quality metric != Authority
code smell != authorization to refactor
```

El baseline actual sólo integra `pytest` como dependencia de desarrollo y la CI
vigente ejecuta pytest, compileall, Candidate Identity y diff validation.
Herramientas como `pytest-cov`, Mutation Testing frameworks, Hypothesis, Ruff,
mypy u otras permanecen **candidates de investigación/tooling**, no dependencias
seleccionadas ni autorizadas.

#### B. Dream-RSI → Governed Counterfactual Replay

**Disposición:** `ADAPT / RESEARCH`.

Dream-RSI aporta como señal útil la separación entre el coding agent y una
política de exploración que puede evaluarse contra discovery histories
reutilizadas como replay simulators. Malāk no debe adoptar su framing de
recursive self-improvement como autoridad ni permitir auto-promoción.

Adaptación conceptual candidata:

```text
bounded historical trace / discovery evidence
        ↓
isolated replay representation
        ↓
counterfactual exploration variants
        ↓
objective / independent evaluation
        ↓
candidate lesson or proposal
        ↓
human-governed admission
```

Separaciones obligatorias:

```text
replay != Memory
counterfactual != fact
candidate lesson != Knowledge
policy improvement != self-modification
evaluation result != promotion
Evidence != Authority
```

Antes de crear cualquier componente nuevo deberán evaluarse REUSE/COMPOSE de
IDEA-002, Governed Self-Review, Trace/Replay y la futura Sandbox/Evaluation
Evidence Foundation.

#### C. Research loops / AutoResearch-style exploration

**Disposición:** `REINFORCE_EXISTING`.

La propiedad útil es un ciclo acotado:

```text
question / hypothesis
→ bounded experiment
→ reproducible evidence
→ compare against baseline
→ finding
→ proposal
→ Owner / governance
```

Debe reutilizar IDEA-002 e IDEA-017. No autoriza adquisición autónoma ilimitada,
promoción automática de findings, modificación de código ni self-improvement.

#### D. Reverse Engineering / Methodology Distillation

**Disposición:** `RESEARCH METHOD`.

Aplicable únicamente a sistemas, repositorios, papers, interfaces o entornos
públicos o expresamente autorizados.

```text
observable behavior / public contracts / docs / traces
        ↓
candidate invariants
        ↓
cross-source corroboration
        ↓
Methodology Distillation
        ↓
compare with Malāk baseline
        ↓
ADOPT | ADAPT | OBSERVE | REJECT
        ↓
bounded experiment only when separately admitted
```

La finalidad es extraer propiedades y metodología, no copiar implementaciones.
No debe intentar recuperar secretos, interfaces ocultas, credenciales,
información protegida ni material incompatible con licencia o autorización.

```text
reverse-engineered observation != truth
distilled methodology != architecture authority
external implementation != Malāk baseline
```

#### E. Cognitive / evaluator research pendiente

Se preservan como `RESEARCH / WATCH`:

- Cognitive Dataset y cross-model invariants;
- evaluator awareness / metagaming;
- causal o mechanistic interpretability cuando la evidencia observable externa
  resulte insuficiente para una pregunta concreta;
- comparación de comportamiento entre runtimes/modelos sin convertir el modelo
  en autoridad;
- ODD permanece `OBSERVE`: sus propiedades útiles se contrastan con Preflight,
  admission, proporcionalidad, 4R y RDD ya existentes; no se crea un sistema ODD.

Estas líneas deberán demostrar una pregunta concreta, beneficio, coste,
testabilidad y ausencia de duplicación antes de promoverse.
