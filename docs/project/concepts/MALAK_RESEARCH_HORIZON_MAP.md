---
title: Malāk Research Horizon Map
status: concept
authority: non_normative
document_role: research_horizon_reconciliation
language: es
created: 2026-09-09
updated: 2026-09-10
as_of_branch: main
as_of_commit: 3788caf68ac14da37040f06a0da3e0fe9db5a2db
related:
  - documents/projects/jarvis/ideas.md
  - docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
  - docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
  - docs/project/concepts/MALAK_COGNITIVE_DATASET_FOUNDATION.md
  - SECURITY.md
purpose: >
  Preservar la reconciliación entre la visión futura de Malāk, la investigación
  y el baseline material, identificando refuerzos y gaps sin crear autoridad ni
  autorizar implementación.
---

# Malāk Research Horizon Map

## 1. Propósito

Este documento responde:

> ¿Qué parte de la visión futura ya está representada, qué debe reforzarse y qué
> sigue siendo un gap real después del baseline actual?

No modifica Blueprint, Constituciones, Kernel, `SECURITY.md`, ADR ni contratos.
No autoriza sprints, agentes, Memory persistente, tools, MCP/A2A, Sandbox,
Internet, PKI, firmas ni cambios de autoridad.

```text
Research != architecture approval
Concept != implementation authorization
Evidence != authority
```

---

## 2. Método de reconciliación

Estados utilizados:

```text
ALIGNED
REINFORCE_EXISTING
GAP_CANDIDATE
WATCH
IRRELEVANT
CONFLICTS_WITH_VISION
```

Regla:

```text
research / idea
        ↓
diff contra baseline actual
        ↓
¿ya existe dueño conceptual/material?
   ┌────┴────┐
  sí        no
   ↓         ↓
reforzar   gap candidato
              ↓
        necessity review futuro
```

Se debe preferir ampliar una responsabilidad existente cuando sea limpio antes
que crear managers, registries o subsistemas nuevos.

---

## 3. Resultado ejecutivo post-PR #93

| Línea | Estado | Dueño conceptual principal | Estado actual |
|---|---|---|---|
| Durable Cognitive Execution | `ALIGNED` | Long Horizon / IDEA-023 / IDEA-024 | Task State, checkpoints, recovery e idempotencia ya están contemplados conceptualmente. |
| Governed Self-Improvement | `ALIGNED` | IDEA-002 / Long Horizon | Malāk puede observar, investigar y proponer; no puede autoaprobar cambios de producción. |
| Resource Governance | `ALIGNED` | IDEA-003 | Presupuestos y límites están contemplados para futuras capacidades costosas. |
| Deception / Honeypots / Adversarial Evaluation | `ALIGNED` | IDEA-019 / IDEA-010 | Deception, honeytokens, red/purple team e aislamiento ya tienen dueño conceptual. |
| Incident Forensics / Attack Path | `ALIGNED` | IDEA-019 | Timeline, attack path, evidence package, recovery y regression learning ya están contemplados. |
| Prompt & Context Trust Boundary | `REINFORCE_EXISTING` | IDEA-006 / IDEA-013 / IDEA-016 / Security | Debe generalizarse a toda entrada no confiable, incluyendo Memory recuperada y tool output. |
| Memory & Knowledge Trust / Poisoning | `REINFORCE_EXISTING` | Memory chain + IDEA-013 / IDEA-016 | Provenance, producer authorization, governed projection y Projection→Admission consumption ya están materializados. El gap inmediato es content identity/binding antes de Persistence Authorization. |
| Candidate Content Identity | `GAP_CANDIDATE` parcialmente madurado | Memory | G0/G1 integrado por PR #93; G2 e implementación no autorizados. |
| AI Supply-Chain Trust | `GAP_CANDIDATE` | IDEA-004 / IDEA-009 / IDEA-011 / IDEA-016 | Falta una política unificada de admisión para artefactos AI. |
| Agent Identity & Delegation | `GAP_CANDIDATE` | IDEA-005 / IDEA-024 / Security | Falta cadena verificable de delegación y revocación derivada. |
| Compromise Containment & Trust Revocation | `GAP_CANDIDATE` | IDEA-019 / IDEA-001 / Security | Falta propagación sistémica de desconfianza hacia estado relacionado. |
| Data Classification & Disclosure Control | `GAP_CANDIDATE` | Context / Memory / Knowledge / Security | Least Context existe; falta clasificación transversal suficientemente explícita. |
| Governed Interoperability | `WATCH` | adapters futuros | Preservar `protocol-ready, not protocol-dependent`. |
| Governed Procedural Learning | `REINFORCE_EXISTING` | IDEA-002 / Skills-on-Demand / Knowledge | Aprendizaje procedimental debe promoverse mediante governance, no autoejecutarse. |
| Multimodal Perception | `WATCH` | futura Perception boundary | Relevante a largo plazo, sin necesidad material actual. |
| World Models | `WATCH` | futura investigación | No existe necesidad demostrada actualmente. |
| Autonomous self-modification | `CONFLICTS_WITH_VISION` | — | La automodificación productiva autónoma permanece prohibida. |

---

## 4. Governed Self-Improvement

La dirección permitida continúa siendo:

```text
observe
→ identify gap
→ research
→ experiment in authorized isolation
→ collect evidence
→ proposal
→ human/applicable governance
→ implementation only if authorized
```

Nunca:

```text
observe
→ decide own authority
→ modify production autonomously
```

La autoobservación produce información; la gobernanza produce autoridad de
cambio.

---

## 5. Defensa, deception y forensics

La postura defensiva conceptual permanece:

```text
DETECT
→ DENY / REVOKE
→ CONTAIN
→ ISOLATE
→ DECEIVE
→ OBSERVE
→ PRESERVE EVIDENCE
→ ANALYZE
→ RECOVER
→ LEARN
→ PROPOSE HARDENING
```

Futuras capacidades podrán, dentro de infraestructura propia o expresamente
autorizada y bajo los gates correspondientes:

- detectar y bloquear;
- aislar componentes o sesiones;
- revocar credenciales y autoridad;
- activar kill switches;
- desplegar honeypots, honeynets, honeytokens y canary resources;
- observar comportamiento adversarial en entornos contenidos;
- reconstruir attack paths;
- preservar evidencia forense;
- generar security regression candidates;
- proponer hardening.

Una IP, ASN, dominio, fingerprint o hash es evidencia técnica, no atribución de
identidad por sí sola.

```text
attack received != authority to hack back
```

Malāk no obtiene autoridad ofensiva automática por haber sido atacada.

---

## 6. Prompt & Context Trust Boundary

Regla transversal:

```text
USER INTENT
!= EXTERNAL CONTENT
!= TOOL OUTPUT
!= RETRIEVED MEMORY
!= KNOWLEDGE CANDIDATE
!= AUTHORITY
```

Debe preservarse que:

- contenido web, archivos, emails y documentos sean DATA;
- tool output, MCP/A2A payloads y retrieved Memory sean DATA;
- ningún texto conceda permisos, modifique policies o amplíe scope;
- instrucciones efectivas para operaciones protegidas deriven de contratos,
  contexto e identidad verificables fuera del LLM;
- indirect prompt injection sea una amenaza sistémica, no solo de prompting.

No se justifica todavía un `PromptInjectionManager` universal.

---

## 7. Memory & Knowledge Trust — estado actual

La cadena episódica materializada es ahora:

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
        ↓
STOP
```

Por tanto ya no es gap:

- provenance estructural del assessment;
- autorización scoped del productor;
- reconstrucción gobernada de inputs;
- consumo `Projection → Admission` sin fallback trust-sensitive desde
  `candidate.control`.

Permanece:

```text
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
ELIGIBLE != Stored
Stored != trusted-for-retrieval
Memory != Knowledge
```

---

## 8. Candidate Content Identity — nuevo hardening inmediato

PR #93 maduró el residual:

```text
candidate_id binding
!=
candidate content identity
```

Dos instancias pueden compartir `candidate_id` y contener datos distintos. La
inmutabilidad de una dataclass no convierte al objeto en content-addressed.

Dirección conceptual seleccionada:

```text
EpisodicMemoryCandidate
        ↓
canonical candidate representation v1
        ↓
deterministic digest
        ↓
EpisodicCandidateContentIdentity
```

La frontera debe permanecer:

- pura;
- determinista;
- versionada;
- reproducible entre plataformas;
- independiente de `repr()`/`pickle`;
- separada de autenticidad, trust y autorización.

SHA-256 mediante stdlib es candidato actual, no una autorización de
implementación.

G2 todavía debe decidir exactamente:

- qué campos entran en la representación;
- si se identifica candidate completo o se separan payload/envelope identities;
- formato canónico;
- timestamps;
- domain separation;
- encoding;
- digest format;
- test vectors.

---

## 9. Frontera objetivo completa de Memory

La dirección de maduración continúa siendo:

```text
Memory Candidate
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
Admission evaluation
      ↓
Candidate content identity / strong binding
      ↓
Persistence authorization
      ↓
Stored Memory
      ↓
Trust-aware retrieval eligibility
      ↓
Retrieval
      ↓
Knowledge candidate when applicable
      ↓
Governed Knowledge promotion
```

Estado material actual:

```text
candidate contracts                     IMPLEMENTED
admission policy                        IMPLEMENTED
assessment provenance                   IMPLEMENTED
assessment producer authorization       IMPLEMENTED
governed input projection               IMPLEMENTED
projection -> admission consumption     IMPLEMENTED
candidate content identity              G0/G1 ONLY
content identity propagation            NOT YET
persistence authorization               NOT YET
persistent Memory                       NOT YET
retrieval                               NOT YET
Knowledge promotion                     NOT YET
```

---

## 10. Persistencia futura

La futura Memory no debe reducirse a storage + similarity search.

Antes de persistir deberán poder tratarse proporcionalmente:

- provenance;
- content identity;
- source authority;
- confidence;
- scope/domain/purpose;
- temporal validity;
- sensitivity;
- contradiction;
- trust state;
- taint/revocation;
- retention;
- quarantine;
- disclosure constraints.

Principio:

> Memory storage is a trust boundary, and Memory retrieval is another trust boundary.

`ELIGIBLE` no debe transformarse directamente en una operación de escritura.

---

## 11. Trust, taint, revocation y quarantine

Downstream de persistencia, el sistema deberá poder representar estados o
equivalentes como:

```text
UNASSESSED
ACCEPTABLE
SUSPECT
TAINTED
SUPERSEDED
REVOKED
QUARANTINED
```

Una fuente comprometida puede reducir el trust de estado derivado sin demostrar
automáticamente que cada elemento esté comprometido.

La relación debe disparar revalidación proporcional, no atribución automática.

---

## 12. AI Supply-Chain Trust

La cadena futura puede incluir:

```text
packages
models / weights / GGUF
LoRA / adapters
embedding models
datasets
prompt templates
skills
agent definitions
MCP servers
plugins / tools
containers
knowledge sources
```

Propiedades candidatas de admisión:

- origen y provenance;
- versión;
- hash e integridad;
- firma cuando aplique;
- licencia;
- vulnerabilidades;
- dependencias transitivas;
- permisos requeridos;
- rollback;
- actualización;
- cuarentena/retiro.

```text
Artifact integrity != Artifact trust
Artifact trust != Execution authorization
```

---

## 13. Agent Identity & Delegation

Toda futura delegación debe respetar:

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

La delegación no puede producir elevación.

Firmas, identidad fuerte y revocación derivada requieren diseño separado antes
de uso operacional.

---

## 14. Data Classification & Disclosure

Acceso no implica permiso de reutilización:

```text
Having access to data
!= permission to persist
!= permission to disclose
!= permission to export
!= permission to reuse
```

Futuras superficies deberán considerar sensibilidad, finalidad, retención,
redaction, uso por modelos remotos, consentimiento y límites de exportación.

---

## 15. Governed Interoperability

MCP/A2A y protocolos futuros permanecen `WATCH`.

Principio:

```text
protocol-ready
not protocol-dependent
```

Ningún protocolo, manifest, tool description o peer externo podrá convertirse en
autoridad interna por contenido.

---

## 16. Governed Procedural Learning

Malāk podrá aprender candidatos de procedimientos, pero la promoción seguirá el
mismo principio de mejora gobernada:

```text
observed procedure
→ candidate
→ evaluation
→ evidence
→ proposal
→ governance
→ approved skill/procedure only if authorized
```

No se permite aprendizaje procedimental que se auto-promueva a ejecución
privilegiada.

---

## 17. Qué no debe crearse todavía

No existe necesidad actual demostrada para:

- Universal Trust Manager;
- Universal Integrity Manager;
- global Memory orchestrator;
- autonomous Agent Manager;
- protocol authority adapter;
- world model subsystem;
- general-purpose persistence engine para Memory;
- self-modification service.

Cuando un gap pueda resolverse con una frontera específica, pequeña y pura, esa
opción debe preferirse.

---

## 18. Próxima maduración candidata

El único siguiente hardening de Memory suficientemente demostrado en el baseline
actual es:

```text
Episodic Candidate Content Identity Boundary
```

Estado:

```text
G0/G1 integrated
G2 not authorized
implementation not authorized
```

Precondiciones antes de G2:

```text
canonical derived docs reconciled
→ human merge
→ Project Vault reconciled
→ drift = 0
→ explicit Owner authorization
```

Después de esa unidad todavía deberá evaluarse **cómo propagar** la identidad a
la cadena antes de Persistence Authorization. No debe asumirse que calcular un
digest local resuelve automáticamente el binding end-to-end.

---

## 19. Invariantes de visión

```text
Model != System
Intelligence != Authority
Memory != Knowledge
Knowledge != Policy
Policy != Authority
Evidence != Authority
Content identity != authenticity
Authenticity != trust
Trust != truth
ELIGIBLE != Stored
Compromise must reduce authority
```

Y para self-improvement:

```text
Malāk may propose change
Malāk may not self-authorize production change
```

---

## 20. Declaración final

Este mapa preserva dirección de investigación y gaps. No crea una obligación de
implementación ni promueve automáticamente ninguna idea.

El baseline material y las fuentes normativas continúan prevaleciendo.