---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-09-10
as_of_commit: 3788caf68ac14da37040f06a0da3e0fe9db5a2db
branch: main
baseline: v0.6.0-alpha
last_numbered_sprint: 7.11
last_runtime_sprint: 7.10
latest_product_unit: Episodic Admission Governed Projection Consumption Boundary
latest_design_unit: Episodic Candidate Content Identity Boundary G0/G1
active_authorized_sprint: null
active_authorized_implementation: null
rdd_stage_1: adopted
rdd_stage_2_authorized: false
language: es
---

# Contexto del proyecto Malāk

## 1. Propósito y autoridad

Este documento es un snapshot derivado, informativo y no normativo del estado
observado de Malāk. Su objetivo es permitir recuperación rápida de contexto sin
convertirse en una segunda fuente de ley.

No reemplaza ni modifica:

- Constitución Cognitiva;
- Constitución de Gobernanza;
- Blueprint;
- especificación del Kernel;
- ADR aceptados;
- contratos públicos aprobados;
- `SECURITY.md`;
- fichas de sprint;
- historial Git;
- decisiones humanas de autorización.

Ante conflicto prevalece la fuente de mayor autoridad y, para estado material,
el repositorio oficial `Aranwill/jarvis/main`.

```text
Derived context != normative authority
Evidence != Decision != Authority
```

---

## 2. Regla persistente de idioma

La comunicación con el Owner y la documentación nueva de Malāk se mantienen en
español. Identificadores técnicos existentes —clases, funciones, módulos, APIs,
rutas, comandos y términos de contrato— pueden conservarse en inglés para no
romper consistencia técnica.

---

## 3. Snapshot actual

```text
Repositorio oficial:              Aranwill/jarvis
Raíz Git local:                   D:\Ollama\jarvis
Rama permanente:                  main
HEAD de referencia:               3788caf68ac14da37040f06a0da3e0fe9db5a2db
Baseline nominal:                 v0.6.0-alpha
Último sprint numerado integrado: Sprint 7.11
Última ruta conversacional:       Sprint 7.10
Última unidad de producto:        Governed Projection Consumption
Última unidad de diseño:          Candidate Content Identity G0/G1
Sprint activo autorizado:         ninguno
Implementación activa autorizada: ninguna
Sprint 7.12:                      no autorizado
RDD Stage 2:                      no autorizado
```

`3788caf68ac14da37040f06a0da3e0fe9db5a2db` integra PR #93, design record G0/G1
de `Episodic Candidate Content Identity Boundary`.

La unidad funcional más reciente sigue siendo PR #92 —
`Episodic Admission Governed Projection Consumption Boundary`, integrada en:

```text
9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

El design G0/G1 posterior no añade comportamiento productivo.

---

## 4. Estado histórico del bloque 7.x

| Sprint | Estado | Resultado principal |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición externa con `OllamaRuntime` |
| 7.2 | Cerrado | `RuntimeMetricSink` |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Eventos operativos, métricas y sincronización gobernada |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Certificación interna del baseline |
| 7.8 | Completado | Cognitive Conversation Execution Path |
| 7.9 | Completado | Conversation Continuity Foundation |
| 7.10 | Completado | Conversation Session Isolation Foundation |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation |

Sprint 7.11 continúa siendo el último sprint numerado. Las unidades episódicas de
Memory posteriores fueron autorizadas e integradas como unidades independientes y
**no constituyen Sprint 7.12**.

Commit de integración de Sprint 7.11:

```text
3413e8ccb348440aea757d1feccde25c65be011f
```

Candidate final documentado de Sprint 7.11:

```text
59f592e2e36d11bbd14f7d9d93b1dac4f442c108
388 passed
compileall: PASS
git diff --check: PASS
FULL 4R: PASS
independent validation: PASS
```

---

## 5. Ruta conversacional vigente

La última ruta conversacional/runtime integrada continúa siendo Sprint 7.10:

```text
CLI
→ Application Composition
→ Kernel.receive()
→ Planner
→ CapabilityRegistry
→ ConversationCapability
→ ConversationService
→ ConversationProviderRegistry
→ RuntimeConversationProvider
→ LLMRuntime
→ Response
```

Propiedades preservadas:

- Kernel independiente de providers, runtimes y modelos concretos;
- `ConversationCapability` como adapter detrás de la frontera de Capability;
- continuidad efímera mediante `InMemoryConversationContext`;
- aislamiento por `session_id`;
- `session context != SecurityContext`;
- conversación sin persistencia en Memory;
- Ollama permanece como runtime reemplazable, no autoridad del Kernel.

---

## 6. Security Control Plane vigente

Sprint 7.5 materializó la separación:

```text
request
→ authorization decision
→ enforcement
→ protected operation
→ evidence / audit
```

Componentes principales:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`;
- Policy Decision Point determinista;
- Policy Enforcement Point;
- auditoría de autorización separada de métricas y eventos.

Se preserva:

```text
Capability != Permission
Decision != Execution
Execution != Evidence
Evidence != Authority
```

Sprint 7.6 añadió lifecycle temporal de `SecurityContext`, `Clock`, validator,
issuer, renewer y `SecurityContextEnvelope`, sin introducir todavía PKI, firmas,
nonce, replay protection, MFA, Secure Message Bus o identidad criptográfica
fuerte.

El finding histórico `7.7-D-001 — Strong SecurityContext Provenance` permanece
como riesgo residual aceptado y debe reevaluarse antes de superficies de mayor
riesgo.

---

## 7. Episodic Memory — cadena integrada actual

Después de Sprint 7.11 se integró incrementalmente una cadena episódica aislada:

```text
PR #76  Episodic Memory Admission Boundary
PR #82  Assessment Provenance Boundary
PR #85  Assessment Producer Authorization Boundary
PR #88  Governed Input Projection Boundary
PR #90  Projection Consumption G0/G1 design
PR #91  Projection Consumption G2 specification
PR #92  Governed Projection Consumption implementation
PR #93  Candidate Content Identity G0/G1 design
```

La cadena productiva actual bajo `src/malak/memory/` es:

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

`Governed Projection Consumption` consume únicamente projections válidas y, para
`READY`, construye una vista efímera del candidate usando el
`projection.effective_context` junto con `projection.effective_signals` antes de
llamar a la policy de Admission existente. No reabre trust desde los campos
trust-sensitive del `candidate.control` original.

La cadena sigue desconectada de:

- Conversation/runtime;
- Kernel;
- almacenamiento persistente;
- retrieval;
- Knowledge;
- agentes y tools;
- red;
- nuevos side effects.

---

## 8. Invariantes de Memory ya preservados

```text
Candidate != Decision
payload != control metadata
structural provenance != authenticated identity
Producer Authorization != trusted truth
Projection READY != Admission ELIGIBLE
Projection HOLD != Admission HOLD automatically
Projection DENIED != Candidate REJECT automatically
Admission ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored Memory
Memory != Knowledge
Knowledge != Policy
Policy != Authority
```

`ELIGIBLE` sigue terminando en `STOP`.

No existe todavía Persistence Authorization ni almacenamiento de Episodic Memory.

---

## 9. Candidate Content Identity — estado G0/G1

PR #93 integró únicamente análisis y diseño. La necesidad detectada es:

```text
candidate_id binding
!=
candidate content identity
```

`candidate_id` sirve como identidad lógica/correlacional, pero dos instancias
pueden compartir el mismo ID y diferir en `origin`, `experience`, `control` o
`created_at`.

Por eso G0 determinó que **Persistence Authorization todavía no es la siguiente
implementación admisible**.

La dirección G1 seleccionada es una frontera aditiva y pura:

```text
EpisodicMemoryCandidate
        ↓
versioned deterministic canonical representation
        ↓
cryptographic digest
        ↓
EpisodicCandidateContentIdentity sidecar
```

Separaciones obligatorias:

```text
Content identity != source authenticity
Content integrity != source trust
Content integrity != truth
Content integrity != Admission ELIGIBLE
Content identity != Authority
```

La selección conceptual favorece una función hash estándar disponible en la
stdlib —SHA-256 es el candidato actual—, pero G2 todavía deberá congelar el
formato canónico exacto y los vectores de prueba antes de cualquier
implementación.

No están autorizados todavía:

- G2 de Candidate Content Identity;
- implementación de Candidate Content Identity;
- propagación del digest por assessments/projection/consumption;
- Persistence Authorization;
- Memory persistente;
- PKI, firmas, HMAC, nonce o replay protection.

---

## 10. Validación reciente

Candidate final de PR #92:

```text
5139d95aaa2c30971b3979ca7c3917067856a428
```

GitHub Actions validó ese SHA exacto en Ubuntu, Windows y macOS con:

```text
pytest: PASS
compileall: PASS
candidate identity: PASS
git diff --check: PASS
```

Ubuntu reportó:

```text
645 passed
```

El Owner reportó además validación local post-merge sobre:

```text
main@9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

con:

```text
645 passed
python -m compileall -q -f tests: PASS
python -m compileall -q -f src tests scripts: PASS
git diff --check: PASS
working tree: clean
```

Esta evidencia local se registra como observada/reportada por el Owner; no se
presenta como ejecución remota del asistente.

El candidate docs-only de PR #93
`4d41776b62fd4f001c850396cb35d365c59a6e0a` pasó el workflow `Validation`.

---

## 11. Malāk Project Vault

Repositorio derivado:

```text
Aranwill/malak-project-vault
```

El Vault:

- no es fuente de autoridad;
- no escribe directamente `jarvis/main`;
- mantiene snapshots históricos inmutables;
- recibe propuestas gobernadas mediante el Sync Agent;
- exige revisión y merge humanos;
- debe demostrar drift cero antes de la siguiente implementación cuando la
  reconciliación sea un gate declarado.

La última reconciliación verificada antes de PR #93 reflejó el product baseline:

```text
9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

PR #93 y este corrective packet documental avanzan el repositorio oficial y,
por tanto, requerirán una nueva reconciliación del Vault antes de G2 de Candidate
Content Identity.

---

## 12. Planificación inmediata y gates

La secuencia vigente es:

```text
G0/G1 Candidate Content Identity   INTEGRATED (#93)
        ↓
canonical derived docs reconcile  THIS PACKET
        ↓
human review + merge
        ↓
Vault reconciliation / drift = 0
        ↓
separate Owner authorization
        ↓
G2 Candidate Content Identity Specification
        ↓
STOP
```

Este documento no concede esa autorización separada.

Una futura G2 deberá, como mínimo, congelar:

- set exacto de campos incluidos en identidad;
- canonicalización determinista;
- domain separation/versioning;
- UTF-8 y representación de `None`;
- timestamps UTC y precisión;
- algoritmo/digest encoding;
- invariantes de orden;
- vectores de prueba multiplataforma;
- presupuesto mínimo de archivos para un eventual G3.

---

## 13. Capacidades explícitamente no autorizadas

Hasta nueva aprobación independiente permanecen fuera de alcance:

- Sprint 7.12;
- RDD Stage 2;
- Persistence Authorization;
- Memory persistente;
- retrieval / RAG / GraphRAG;
- Knowledge promotion;
- wiring de Memory con Conversation/runtime;
- agentes autónomos;
- tools externas operativas;
- navegación o Internet autónomo;
- Sandbox operativo;
- MCP/A2A operativo;
- PKI, firmas, nonce y replay protection;
- autoelevación de privilegios;
- cambios autónomos de Blueprint, Constituciones, Kernel o policies;
- `hack back` autónomo.

---

## 14. Restricciones permanentes de construcción

Todo trabajo futuro debe preservar:

- Kernel First;
- Capability First;
- Runtime Independence;
- Vendor Independence;
- Human in Control;
- Zero Trust;
- Defense in Depth;
- least privilege / least context;
- fail-closed para operaciones sensibles;
- cambios pequeños, trazables y reversibles;
- contratos explícitos;
- separación entre evidencia, decisión, ejecución y autoridad;
- revisión humana para Ready y merge.

Metodología vigente:

```text
SDD
+ TDD
+ FULL 4R
+ Bounded Correction
+ Independent Validation
```

Preguntas obligatorias antes de modificaciones significativas:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Preserva o reduce la complejidad del Kernel?

Si alguna respuesta es negativa, dudosa o carece de evidencia suficiente, el
trabajo debe detenerse antes de editar.

---

## 15. Política de actualización

Este snapshot se reconcilia contra:

```text
Aranwill/jarvis/main@3788caf68ac14da37040f06a0da3e0fe9db5a2db
```

Debe revisarse cuando cambie materialmente:

- la arquitectura implementada;
- el último sprint o unidad integrada;
- el estado de autorización;
- la evidencia de validación relevante;
- la postura de seguridad;
- el estado del Vault;
- la planificación inmediata.

Los registros históricos no se reescriben para aparentar que describen el
presente. Git y las fichas de sprint conservan la trazabilidad histórica.

---

## 16. Declaración final de autoridad

Este documento no puede aprobar un sprint, autorizar implementación, modificar
arquitectura, cambiar gobernanza, redefinir el Kernel, certificar una release,
conceder permisos, promover una propuesta ni ampliar autoridad operativa.

Su único propósito es describir de forma trazable y conveniente el estado
observado del proyecto.