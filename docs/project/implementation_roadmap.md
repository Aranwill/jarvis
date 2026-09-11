---
title: Hoja de ruta de implementación de Malāk
status: activo
authority: no normativa
document_role: canonical_derived_implementation_roadmap
as_of_date: 2026-09-11
as_of_commit: e45a3e3c0ebf657a513596aa74452413479c05d1
branch: main
baseline: v0.6.0-alpha
certification_branch: null
candidate_commit: null
certification_status: current_main_validated
legacy_planning_source:
  - docs/project/roadmap.md
language: es
---

# Hoja de ruta de implementación de Malāk

## Propósito

Este documento es la fuente **derivada y no normativa** para consultar la
planificación de implementación vigente de Malāk.

Centraliza:

- estado material de referencia;
- estado de sprints y unidades posteriores;
- gates autorizados o no autorizados;
- iniciativas futuras reconocidas;
- propuestas pendientes;
- disposición de planificación legacy.

No reemplaza Constituciones, Blueprint, ADR, SECURITY.md, contratos ni
specifications aprobadas.

```text
roadmap != authorization
evidence != authority
proposal != approval
```

---

# 1. Autoridad y regla de admisión

La presencia de una iniciativa en este roadmap no concede permiso para diseñarla
o implementarla.

Toda nueva unidad debe pasar, como mínimo, por:

1. inspección del baseline vigente;
2. identificación de una necesidad real;
3. revisión de arquitectura, seguridad y gobernanza;
4. definición de alcance y fuera de alcance;
5. análisis de dependencias, riesgo y rollback;
6. specification/design verificable;
7. debate;
8. aprobación explícita del Owner;
9. implementación candidate-bound cuando corresponda;
10. validación, revisión y merge humano.

La aprobación de una unidad no autoriza la siguiente.

El Owner puede aprobar, redefinir, diferir, reemplazar, rechazar o archivar
cualquier propuesta.

---

# 2. Modelo documental

```text
ROADMAP.md
   ↓
docs/project/implementation_roadmap.md
   ├── ideas → documents/projects/jarvis/ideas.md
   ├── concepts → docs/project/concepts/
   └── evidence → docs/project/sprints/ + proposals/
```

Responsabilidades:

- `ROADMAP.md`: punto de entrada breve;
- este archivo: planificación derivada canónica;
- `ideas.md`: registro de ideas;
- `concepts/`: referencias conceptuales;
- `sprints/` y `proposals/`: alcance, ejecución y evidencia de unidades concretas.

Las fichas de sprint y proposal records no deben convertirse en un segundo
roadmap, y este roadmap no debe duplicar su evidencia detallada.

---

# 3. Estado de referencia actual

```text
repository:
Aranwill/jarvis

permanent branch:
main

current integrated HEAD:
e45a3e3c0ebf657a513596aa74452413479c05d1

nominal baseline:
v0.6.0-alpha

last numbered sprint:
Sprint 7.11 — Reproducible Validation Pipeline Foundation

last conversational/runtime sprint:
Sprint 7.10 — Conversation Session Isolation Foundation

latest episodic Memory unit:
Governed Projection Consumption Boundary

latest cognitive code unit:
G2A — Protected Finalization Foundation

latest cognitive design unit:
Assurance Signal Authority Boundary — G0/G1

active sprint:
NONE

active implementation branch:
NONE
```

Repositorio derivado observado:

```text
Vault main:
34f0416a8d312f4f27b9b36c3733cc2703772364

last Malāk source reconciled into Vault:
5865da6a5e502fe71e35e2e38bc4cceaab9b3600

Vault drift against current Malāk HEAD:
EXPECTED / PENDING RECONCILIATION
```

Sync Agent baseline observado:

```text
Aranwill/malak-vault-sync-agent
main@f6eb42715dd7771f3bcf7909a99f7e4e7db465c1
operating mode: manual-on-demand
```

El Vault no concede autoridad sobre Malāk.

---

# 4. Baseline funcional materializado

## 4.1 Ruta conversacional

La ruta vigente continúa siendo:

```text
Request
  ↓
Kernel.receive()
  ↓
Planner
  ↓
CapabilityRegistry
  ↓
ConversationCapability
  ↓
ConversationService
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
Response
```

Sprint 7.9 añadió continuidad efímera y Sprint 7.10 aislamiento por sesión.

No existe Memory conversacional persistente.

## 4.2 Cadena episódica aislada

Después de Sprint 7.11 se integró, mediante gates independientes:

```text
Episodic Memory Admission Boundary        PR #76
        ↓
Assessment Provenance Boundary            PR #82
        ↓
Assessment Producer Authorization         PR #85
        ↓
Governed Input Projection Boundary        PR #88
        ↓
Governed Projection Consumption Boundary  PR #92
```

Semántica preservada:

```text
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Consumption EVALUATED != Stored
Evidence != Authority
```

La cadena continúa sin Conversation/runtime wiring, persistencia, retrieval ni
Knowledge operativo.

## 4.3 Candidate Content Identity

PR #93 integró solamente G0/G1.

```text
Candidate Content Identity G2: NOT AUTHORIZED
implementation / propagation: NOT AUTHORIZED
```

El diseño existente pertenece al dominio `EpisodicMemoryCandidate`; no debe
reutilizarse como identidad genérica de respuesta sin un gate independiente.

---

# 5. Progressive Cognitive Assurance — estado actual

La dirección Evidence-Bound / Progressive Cognitive Assurance fue desarrollada
conceptualmente y promovida normativamente mediante los artefactos aplicables,
incluyendo ADR-005, Blueprint v0.6.2-alpha y Cognitive Constitution v1.1.0.

La regla fundamental es:

```text
Generation != Finalization
Candidate != Accepted Response
Evidence != Authority
```

## 5.1 G2A — Protected Finalization Foundation

PR #110 integró G2A en:

```text
ecb1315946f47534135bbdc73d94ccf88df0d8d6
```

La unidad materializa contratos y evaluator determinista aislados:

```text
ProtectedResponseCandidate
        +
explicit assurance input
        ↓
ACCEPT | ABSTAIN | BLOCK
```

No materializa todavía:

- Signal Producers;
- Conversation wiring;
- history-after-finalization;
- provider/runtime integration;
- Memory/Knowledge integration;
- `QUALIFY`;
- autoridad adicional.

## 5.2 Assurance Signal Authority G0/G1

PR #111 quedó integrada en el HEAD actual:

```text
e45a3e3c0ebf657a513596aa74452413479c05d1
```

El diseño establece:

```text
observation
!= producer authorization
!= projected signal
!= finalization decision
!= authority
```

Ownership previsto:

- `applicability`: policy cognitiva versionada;
- `evidence_required`: policy cognitiva versionada;
- `support_sufficient`: evaluación explícita de evidencia real;
- `contradiction_unresolved`: evaluación explícita;
- `policy_violation`: señal autorizada del dominio aplicable, no cualquier
  `DENY` de Security.

El Security PDP gobierna autorización de operaciones, no verdad ni suficiencia
de evidencia.

## 5.3 Gates posteriores

```text
Signal Boundary G2
NOT AUTHORIZED

Conversation Finalization G2B
NOT AUTHORIZED
BLOCKED BY SIGNAL-PRODUCER GAP
```

G2B no debe conectarse a Conversation hasta que exista un productor autorizado
y explícito de applicability/evidence signals.

---

# 6. Estado de autorización

| Unidad / frontera | Estado |
|---|---|
| Sprint 7.11 | Completado e integrado |
| Episodic Admission → Governed Projection Consumption | Integrado |
| Candidate Content Identity G0/G1 | Integrado |
| Candidate Content Identity G2 | **No autorizado** |
| Cognitive Assurance normative promotion | Integrada |
| G2A Protected Finalization Foundation | Integrado |
| Assurance Signal Authority G0/G1 | Integrado |
| Signal Boundary G2 | **No autorizado** |
| Conversation Finalization G2B | **No autorizado / bloqueado** |
| Persistence Authorization | **No autorizado** |
| Memory persistente | **No autorizado** |
| Retrieval / Knowledge runtime | **No autorizado** |
| Sprint 7.12 | **No autorizado** |
| RDD Stage 2 | **No autorizado** |
| Authority expansion | **Ninguna** |

RDD Stage 1 permanece adoptado. RDD Stage 2 requiere autorización independiente.

---

# 7. Secuencia inmediata de planificación

El estado actual requiere cerrar primero la coherencia derivada:

```text
reconciliar canonical derived docs contra e45a3e3
        ↓
reconciliar Malāk Project Vault
        ↓
confirmar drift cero o riesgo explícitamente aceptado
        ↓
debatir Signal Boundary G2
        ↓
Owner authorization explícita si corresponde
```

La sincronización del Vault no constituye un sprint ni autoriza G2.

No debe abrirse G2B directamente.

---

# 8. Sprints 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición con `OllamaRuntime` |
| 7.2 | Cerrado | `RuntimeMetricSink` |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Logs, métricas, eventos y sincronización gobernada |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Certificación interna del baseline |
| 7.8 | Completado | Cognitive Conversation Execution Path Foundation |
| 7.9 | Completado | Conversation Continuity Foundation |
| 7.10 | Completado | Conversation Session Isolation Foundation |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation |

Las unidades posteriores no alteran la numeración histórica y no constituyen
Sprint 7.12.

Para evidencia detallada consultar las fichas `SPRINT-7.x.md` y los proposal
records correspondientes.

---

# 9. Foundations de seguridad preservadas

Security Control Plane mantiene:

```text
request
→ decision
→ enforcement
→ audit
→ protected operation
```

Propiedades:

- PDP determinista;
- sin LLM;
- deny-by-default;
- fail-closed;
- confirmación humana cuando aplica;
- PEP separado del Kernel/Planner;
- evidencia de autorización separada de métricas/eventos.

Secure Context Lifecycle mantiene validación temporal, emisión, renovación,
lineage y propagación inmutable en memoria.

Riesgo residual preservado:

```text
7.7-D-001 — Strong SecurityContext Provenance
ACCEPTED_RESIDUAL_RISK / MEDIUM / non-blocking
```

No habilita automáticamente identidad criptográfica, MFA, replay protection,
Secure Message Bus ni rutas operativas de alto riesgo.

---

# 10. Iniciativas reconocidas para planificación futura

Su presencia aquí **no autoriza diseño detallado ni implementación**.

## 10.1 Sandbox Containment & Evaluation Evidence Foundation

Objetivos potenciales:

- aislamiento y entornos descartables;
- control de red, archivos y procesos;
- límites de CPU/RAM/VRAM/disco/tiempo;
- telemetría externa;
- evidencia reproducible;
- snapshots/hashes;
- kill switch, timeout y cuarentena;
- pruebas de contención;
- revisión humana.

Estado: `planning recognized / not approved / no sprint`.

## 10.2 Segmented Domain Governance Foundation

Objetivos potenciales:

- Malāk como control plane horizontal;
- Domain Packs subordinados;
- precedencia de policy explícita;
- impedir ampliación de autoridad desde capas inferiores;
- impedir contaminación del Kernel con lógica sectorial.

Estado: `planning recognized / not approved / no sprint`.

## 10.3 Knowledge Intake & External Evidence Governance

Objetivos potenciales:

- gobernar fuentes externas;
- procedencia, licencia y vigencia;
- originales preservados;
- índices/grafos reconstruibles;
- saneamiento y validación;
- prevención de autocontaminación.

Estado: `planning recognized / not approved / no sprint`.

## 10.4 Security Learning, Adversarial Evaluation & Deception

Objetivos potenciales:

- laboratorios locales;
- CTF autorizados;
- aprendizaje defensivo;
- evaluación externa de agentes;
- deception defensiva aislada;
- transformación de evidencia en propuestas defensivas.

No habilita:

- malware;
- Tor;
- honeypots públicos;
- pentesting no autorizado;
- navegación autónoma;
- respuesta ofensiva.

Estado: `planning recognized / not approved / no sprint`.

---

# 11. Legacy Planning & Disposition Registry

`docs/project/roadmap.md` es planificación temprana preservada como legacy.

```text
legacy != vigente
legacy != descartado
```

Estados informativos:

| Estado | Significado |
|---|---|
| `materializado` | Existe implementación o equivalente verificable |
| `parcialmente_materializado` | Existe una parte de la intención |
| `preservado` | Intención futura válida |
| `evolucionado` | Reformulada por arquitectura posterior |
| `candidato_tecnologico` | Tecnología candidata, no compromiso |
| `requiere_revision` | Evidencia insuficiente para disposición final |
| `hito_historico` | Valor principalmente histórico |

Disposición vigente:

| Elemento legacy | Disposición | Interpretación actual |
|---|---|---|
| Ollama | `materializado` | Existe `OllamaRuntime`; continúa detrás de `LLMRuntime` |
| Open WebUI | `candidato_tecnologico`, `hito_historico` | No es componente obligatorio |
| Qwen2.5 | `candidato_tecnologico` | Modelo histórico/candidato; Model Agnostic preservado |
| DeepSeek | `candidato_tecnologico` | Sin dependencia permanente |
| Validación RAG | `preservado` | Capacidad futura |
| Optimización embeddings | `preservado` | Relevante para retrieval futuro |
| Base documental | `evolucionado` | Evolucionó hacia Knowledge/AKS/retrieval |
| n8n | `candidato_tecnologico` | No es requisito arquitectónico |
| Automatizaciones | `preservado` | Capacidad futura gobernada |
| ChromaDB | `hito_historico`, `candidato_tecnologico` | Vector DB futura debe ser sustituible |
| Memoria Documental | `evolucionado` | Evolucionó hacia Memory / Knowledge / AKS |
| Seguridad IA | `evolucionado` | Evolucionó hacia foundations actuales |
| OWASP LLM Top 10 | `preservado` | Referencia futura de seguridad |
| Prompt Injection | `preservado` | Amenaza relevante para contenido externo/tools |
| SSRF | `preservado` | Amenaza relevante para capacidades de red |
| Auditoría documental | `evolucionado` | Relacionada con AKS/trazabilidad/gobernanza |
| Voice | `preservado` | Capacidad futura |
| Whisper | `candidato_tecnologico` | Tecnología candidata de Voice |
| Piper | `candidato_tecnologico` | Tecnología candidata de Voice |
| Agentes | `preservado` | Futuro sujeto a seguridad/gobernanza |
| Module Registry | `requiere_revision` | Responsabilidad aún no clasificada |
| Event Bus | `preservado` | Concepto sujeto a evaluación del baseline |
| Lifecycle Manager | `requiere_revision` | No se asume equivalencia con mecanismos actuales |
| Health Manager | `preservado`, `requiere_revision` | Responsabilidad exacta pendiente |
| HelloCapability | `hito_historico` | Hito mínimo ya superado |
| Procesamiento de Request | `materializado` | Existe flujo mediante Kernel |
| Tests del Kernel | `materializado` | Existe validación automatizada |
| Baseline Kernel v1.0 | `hito_historico` | Nomenclatura histórica |
| Memory Layer | `parcialmente_materializado` | Admission→Consumption materializado; Identity G2/Persistence/retrieval pendientes |
| Knowledge Layer | `preservado` | Capacidad futura |
| RAG | `preservado` | Capacidad futura |
| Vector DB | `candidato_tecnologico` | Infraestructura futura sustituible |
| Planning Engine | `parcialmente_materializado` | Existe Planner mínimo |
| Reasoning Engine | `preservado`, `requiere_revision` | Arquitectura futura no definida |
| Capabilities reales | `parcialmente_materializado` | Existen algunas; futuras siguen Capability First |
| FastAPI | `candidato_tecnologico` | Tecnología candidata |
| IoT | `preservado` | Capacidad futura |
| Vision | `preservado` | Capacidad futura |
| OSINT | `evolucionado` | Parte evolucionó hacia Evidence Acquisition |
| Workflows | `preservado` | Capacidad futura |
| Malāk Platform v1.0 | `preservado` | Visión de largo plazo, no release plan aprobado |

Una disposición legacy puede cambiar solo mediante evaluación explícita.

---

# 12. Propuestas y decisiones pendientes

| Propuesta / decisión | Estado | Observación |
|---|---|---|
| Reconciliación del Vault a `e45a3e3…` | Pendiente | Operación derivada, no sprint |
| Semántica de `docs/project/status/` frente al Sync Agent | Pendiente | No mapear globalmente sin diseño; snapshot post-audit ya superseded |
| Signal Boundary G2 | No aprobada | G0/G1 integrado por PR #111; requiere scope + autorización |
| Conversation Finalization G2B | Bloqueada / no aprobada | Requiere productor autorizado de signals |
| Candidate Content Identity G2 | No aprobada | G0/G1 integrado por PR #93 |
| Persistence Authorization | No aprobada | Gate independiente posterior |
| Preparación AKS para GraphRAG | No aprobada | No implica implementar GraphRAG |
| Module Registry legacy | Requiere revisión | Determinar si sigue siendo necesario |
| Lifecycle Manager legacy | Requiere revisión | Comparar intención legacy con lifecycle actual |
| Health Manager legacy | Requiere revisión | Definir responsabilidad mínima |

La tabla no establece secuencia obligatoria salvo dependencias explícitas.

---

# 13. Regla de admisión de Capabilities

Una Capability nueva debe añadir funcionalidad:

```text
real
necesaria
permanente
```

No debe crearse solo para demostrar routing, Registry, coverage o completar una
secuencia histórica.

La infraestructura interna debe validarse con tests, doubles, fixtures,
contratos e integración controlada.

---

# 14. Restricciones estructurales

Antes de agentes, tools, navegación, mensajería externa, automatización del SO,
Memory sensible o Capabilities de alto riesgo deben existir las foundations
requeridas.

Ninguna propuesta puede:

- contaminar el Kernel con lógica de negocio;
- acoplar Kernel a runtime/provider/model;
- introducir dependencias no aprobadas;
- modificar contratos centrales sin revisión;
- usar hardware actual como arquitectura permanente;
- convertir evidencia o outputs probabilísticos en autoridad.

---

# 15. Referencias de ejecución y evidencia

Sprints numerados:

```text
docs/project/sprints/SPRINT-7.0.md
...
docs/project/sprints/SPRINT-7.11.md
```

Fronteras posteriores relevantes:

```text
docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G0-INSPECTION.md
docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-PROGRESSIVE-COGNITIVE-ASSURANCE-RUNTIME-G2A-IMPLEMENTATION-CANDIDATE-SPEC.md
docs/project/sprints/proposals/MALAK-ASSURANCE-SIGNAL-AUTHORITY-G0-G1-DESIGN.md
```

La evidencia detallada pertenece a esos registros y al historial Git; no se
duplica aquí.

---

# 16. Relación con ideas y concepts

`documents/projects/jarvis/ideas.md` preserva ideas.

`docs/project/concepts/` preserva referencias conceptuales.

```text
idea != roadmap
concept != roadmap
roadmap != authorization
```

La promoción debe ser explícita y referenciada.

---

# 17. Regla de actualización

Este roadmap debe revalidarse ante:

- cambio material del HEAD que altere la planificación descrita;
- integración de una unidad funcional relevante;
- apertura/cierre formal de un sprint;
- decisión arquitectónica que afecte planificación;
- cambio material de gobernanza;
- promoción/rechazo/supersedencia de iniciativas;
- cambio material del estado del Vault cuando constituya una precondición de
  planificación.

Commits puramente mecánicos que no alteran planificación no obligan por sí solos
a reescribir `as_of_commit`.

Registros históricos no deben reescribirse silenciosamente.

---

# 18. Estado actual de planificación

```text
CURRENT INTEGRATED HEAD
e45a3e3c0ebf657a513596aa74452413479c05d1

PERMANENT BRANCH
main

NOMINAL VERSION
v0.6.0-alpha

LAST COMPLETED NUMBERED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST CONVERSATIONAL/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

LATEST EPISODIC MEMORY UNIT
Governed Projection Consumption Boundary

LATEST COGNITIVE CODE UNIT
G2A — Protected Finalization Foundation

LATEST COGNITIVE DESIGN UNIT
Assurance Signal Authority Boundary — G0/G1

VAULT
PENDING RECONCILIATION FROM MALAK 5865da6a TO e45a3e3

ACTIVE SPRINT
NONE

SPRINT 7.12
NOT AUTHORIZED

SIGNAL BOUNDARY G2
NOT AUTHORIZED

CONVERSATION FINALIZATION G2B
NOT AUTHORIZED / BLOCKED

CANDIDATE CONTENT IDENTITY G2
NOT AUTHORIZED

PERSISTENCE AUTHORIZATION
NOT AUTHORIZED

RDD STAGE 2
NOT AUTHORIZED

LAW DOCUMENTS
OUT OF SCOPE

AUTHORITY EXPANSION
NONE
```

---

# 19. Principio de cierre

La planificación de Malāk debe permanecer:

```text
trazable
→ gobernada
→ incremental
→ reversible
→ subordinada a autoridad superior
```

El roadmap organiza intención.

No crea autoridad.

La evidencia puede producir una propuesta.

La propuesta puede producir una decisión humana.

Solo una decisión autorizada puede producir implementación.
