---
title: Malāk Research Horizon Map
status: concept
authority: non_normative
document_role: research_horizon_reconciliation
language: es
created: 2026-09-09
as_of_branch: main
as_of_commit: 6458fd98b3af16401d485495eb7cd1eae4b23881
related:
  - documents/projects/jarvis/ideas.md
  - docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
  - docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
  - docs/project/concepts/MALAK_COGNITIVE_DATASET_FOUNDATION.md
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
| Memory & Knowledge Trust / Poisoning | `GAP_CANDIDATE` | futura Memory + IDEA-013 / IDEA-016 | Hay provenance, authority, freshness y promotion gates; falta explicitar admisión defensiva y propagación de contaminación. |
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

## 6. GAP CANDIDATE — Memory & Knowledge Trust / Poisoning

La futura Memory no deberá reducirse a almacenamiento y similarity search.

Antes de que una observación pueda influir persistentemente en Malāk deberá existir
conceptualmente una frontera de admisión:

```text
Memory Candidate
      ↓
Provenance
      ↓
Type / Domain / Scope
      ↓
Trust classification
      ↓
Temporal validity
      ↓
Conflict / contamination checks
      ↓
Admission decision
      ↓
Retrieval eligibility
```

Separación obligatoria:

```text
Conversation → Ephemeral Context
Experience   → Episodic Memory candidate
Stable fact  → Semantic Memory candidate
Procedure    → Procedural Memory candidate
Evidence     → Knowledge candidate
```

Propiedades candidatas:

- provenance obligatorio cuando exista;
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

Este gap deberá intentar reforzar futura Memory, IDEA-013 e IDEA-016 antes de
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
3. Memory / Knowledge Admission & Poisoning Defense
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
Implementación autorizada: ninguna
```

### Resultado final

La revisión confirma que gran parte de la visión futura ya estaba distribuida
de forma coherente en Malāk, especialmente en Long Horizon, IDEA-001, IDEA-002,
IDEA-003, IDEA-005, IDEA-006, IDEA-013, IDEA-016, IDEA-019, IDEA-021, IDEA-023 e
IDEA-024.

Los gaps que merecen permanecer visibles son principalmente:

1. `Compromise Containment & Trust Revocation` sistémico;
2. `Memory & Knowledge Trust / Poisoning` con admisión explícita;
3. `AI Supply-Chain Trust` para artefactos AI y externos;
4. `Agent Identity & Delegation` verificable y revocable;
5. `Data Classification & Disclosure Control` transversal;
6. generalización de `Prompt & Context Trust Boundary`.

Ninguno de estos gaps constituye por sí mismo autorización para crear una nueva
capability, componente o sprint.
