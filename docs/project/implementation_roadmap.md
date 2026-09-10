---
title: Hoja de ruta de implementación de Malāk
status: activo
authority: no normativa
document_role: canonical_derived_implementation_roadmap
as_of_date: 2026-09-10
as_of_commit: 3788caf68ac14da37040f06a0da3e0fe9db5a2db
branch: main
baseline: v0.6.0-alpha
last_numbered_sprint: 7.11
latest_product_unit: Episodic Admission Governed Projection Consumption Boundary
latest_design_unit: Episodic Candidate Content Identity Boundary G0/G1
active_authorized_sprint: null
active_authorized_implementation: null
rdd_stage_1: adopted
rdd_stage_2_authorized: false
legacy_planning_source:
  - docs/project/roadmap.md
language: es
---

# Hoja de ruta de implementación de Malāk

## 1. Propósito

Esta es la fuente derivada canónica para consultar la planificación de
implementación vigente de Malāk.

Centraliza:

- baseline de referencia;
- trabajo integrado;
- estado de autorización;
- siguiente gap técnicamente demostrado;
- iniciativas futuras reconocidas;
- gates que deben satisfacerse antes de avanzar.

Es deliberadamente **no normativa**.

```text
Roadmap != approval
Plan != authority
Evidence != authority
```

No sustituye Blueprint, Constituciones, Kernel, ADR, `SECURITY.md`, contratos,
fichas de sprint ni decisiones del Owner.

---

## 2. Regla de admisión

La existencia de una entrada en este documento no autoriza implementación.

Toda nueva unidad debe atravesar, según aplicabilidad:

```text
G0 necesidad
→ G1 diseño
→ Owner gate
→ G2 specification
→ Owner gate
→ TDD RED
→ G3 implementación mínima
→ GREEN
→ FULL 4R
→ bounded correction si aplica
→ independent validation
→ Draft PR
→ revisión humana
→ Ready humano
→ merge humano
→ post-merge validation
→ Vault reconciliation
```

Una unidad anterior no autoriza la siguiente.

---

## 3. Estado de referencia

```text
Repositorio:                       Aranwill/jarvis
Rama permanente:                   main
HEAD de referencia:                3788caf68ac14da37040f06a0da3e0fe9db5a2db
Baseline nominal:                  v0.6.0-alpha
Último sprint numerado:            Sprint 7.11
Última ruta conversacional/runtime:Sprint 7.10
Última unidad de producto:         Governed Projection Consumption
Última unidad de diseño:           Candidate Content Identity G0/G1
Sprint activo autorizado:          ninguno
Implementación activa autorizada:  ninguna
Sprint 7.12:                       no autorizado
RDD Stage 2:                       no autorizado
```

El HEAD actual integra PR #93, que agrega únicamente G0/G1 de Candidate Content
Identity. La última unidad de código productivo permanece PR #92, integrada en
`9438c66e315faa2b4c8c3f0a99d4e1e9619992c3`.

---

## 4. Sprints 7.x

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición con `OllamaRuntime` fuera del Kernel |
| 7.2 | Cerrado | `RuntimeMetricSink` |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Observabilidad operativa y Vault sync gobernado |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Certificación interna del baseline |
| 7.8 | Completado | Cognitive Conversation Execution Path |
| 7.9 | Completado | Conversation Continuity Foundation |
| 7.10 | Completado | Conversation Session Isolation Foundation |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation |

No existe Sprint 7.12 autorizado.

Las unidades de Memory posteriores a 7.11 no cambian la numeración histórica.

---

## 5. Ruta conversacional/runtime

La ruta conversacional integrada sigue siendo:

```text
Request
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

Continúa siendo efímera y separada de Memory persistente.

No está planificado automáticamente conectar la cadena episódica a esta ruta.
Cualquier wiring requerirá necesidad demostrada, threat model y autorización
propia.

---

## 6. Cadena episódica integrada

Secuencia de unidades integradas después de Sprint 7.11:

```text
PR #76  Episodic Memory Admission Boundary
PR #82  Assessment Provenance Boundary
PR #85  Assessment Producer Authorization Boundary
PR #88  Governed Input Projection Boundary
PR #90  Projection Consumption G0/G1
PR #91  Projection Consumption G2
PR #92  Governed Projection Consumption G3
PR #93  Candidate Content Identity G0/G1
```

Estado productivo actual:

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

No existe todavía:

```text
Persistence Authorization
Stored Episodic Memory
Trust-aware retrieval
Knowledge promotion
Conversation/runtime wiring
```

---

## 7. Estado de las fronteras de Memory

| Frontera | Estado material |
|---|---|
| Episodic candidate contracts | `IMPLEMENTED` |
| Admission policy | `IMPLEMENTED` |
| Assessment provenance | `IMPLEMENTED` |
| Producer authorization | `IMPLEMENTED` |
| Governed input projection | `IMPLEMENTED` |
| Projection → Admission consumption | `IMPLEMENTED` |
| Candidate content identity | `G0/G1 ONLY` |
| Content identity propagation | `NOT DESIGNED/NOT AUTHORIZED` |
| Persistence authorization | `NOT AUTHORIZED` |
| Persistent Memory | `NOT AUTHORIZED` |
| Retrieval | `NOT AUTHORIZED` |
| Knowledge promotion | `NOT AUTHORIZED` |

Separaciones permanentes:

```text
Projection READY != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored
Stored != trusted-for-retrieval
Memory != Knowledge
Knowledge != Policy
Policy != Authority
```

---

## 8. Candidate Content Identity — gap inmediato demostrado

G0/G1 de PR #93 determinó:

```text
candidate_id binding
!=
candidate content identity
```

Mientras la cadena terminaba en una decisión pura, ese residual podía permanecer
visible. Antes de habilitar cualquier estado durable, el sistema debe poder
probar que el candidate evaluado y el payload que una futura operación pretende
persistir son materialmente el mismo contenido estructurado.

Dirección conceptual seleccionada:

```text
EpisodicMemoryCandidate
        ↓
canonical representation v1
        ↓
deterministic digest
        ↓
EpisodicCandidateContentIdentity sidecar
```

No se cambia `candidate_id` por un hash y no se introduce todavía PKI, firmas,
HMAC, nonce ni anti-replay.

```text
Content identity != authenticity
Content identity != trust
Content identity != truth
Content identity != authorization
```

---

## 9. Siguiente unidad candidata — NO autorizada

Nombre candidato:

```text
Episodic Candidate Content Identity Boundary — G2 Specification
```

Estado:

```text
candidate only
G2 authorization: false
implementation authorization: false
```

Antes de G2 deben cerrarse:

1. corrective packet de documentación derivada post-#93;
2. revisión humana y merge de ese packet;
3. sincronización gobernada del Project Vault;
4. dry-run final con drift cero;
5. aprobación separada del Owner para G2.

Una eventual G2 deberá congelar como mínimo:

- campos exactos incluidos en la identidad;
- representación canónica determinista;
- domain separation;
- versión de canonicalización;
- encoding UTF-8;
- representación de `None`, bools, enums y strings;
- normalización temporal UTC y precisión;
- algoritmo de digest;
- formato del digest;
- determinismo entre procesos/plataformas;
- failure semantics;
- vectores de prueba conocidos;
- presupuesto máximo de archivos para eventual G3.

G2 deberá decidir también si `control` forma parte de la identidad completa o si
se requieren identidades separadas de payload y envelope. Esa decisión no debe
inferirse desde este roadmap.

---

## 10. Persistence Authorization — diferida

Persistence Authorization permanece **diferida**.

No debe diseñarse como un simple:

```text
if admission == ELIGIBLE: store()
```

Antes de cualquier implementación deberá existir binding suficiente entre:

```text
candidate content
↔ governed assessments
↔ projection
↔ admission decision
↔ persistence request
```

y deberán reevaluarse los requisitos de `SECURITY.md` sobre provenance,
integridad, sensitivity, finalidad, retención, revocación y quarantine.

La futura autorización de persistencia deberá ser una decisión separada de la
policy de Admission y no podrá derivarse automáticamente de `ELIGIBLE`.

---

## 11. Trabajo futuro reconocido, no autorizado

### 11.1 Memory & Knowledge Trust

Después de resolver identidad/binding y Persistence Authorization, la dirección
conceptual sigue siendo:

```text
Stored Memory
→ trust-aware retrieval eligibility
→ retrieval
→ Knowledge candidate when applicable
→ governed promotion
```

La recuperación no podrá basarse únicamente en similitud.

### 11.2 Prompt & Context Trust Boundary

Todo contenido externo, tool output, retrieved memory o knowledge candidate debe
ser tratado como DATA, no como autoridad o instrucciones privilegiadas.

### 11.3 Compromise Containment & Trust Revocation

El diseño futuro deberá permitir degradar trust, revocar, marcar `SUSPECT`,
`TAINTED`, `REVOKED`, aislar y revalidar estado relacionado cuando exista
evidencia de compromiso.

### 11.4 AI Supply-Chain Trust

Continúa como gap candidato para artefactos como models, adapters, datasets,
skills, plugins, MCP servers, containers y knowledge sources.

### 11.5 Agent Identity & Delegation

Continúa diferido hasta que exista una necesidad operacional real. Delegación no
podrá ampliar autoridad.

### 11.6 Durable Cognitive Execution / Agents

Permanece en Long Horizon. No se justifica introducir agentes, managers o task
engines mientras la superficie actual no lo requiera.

---

## 12. Seguridad y autoridad

Antes de Memory persistente, agentes, tools, red o mensajería externa deben
reevaluarse los límites actuales:

- Strong SecurityContext Provenance;
- identidad criptográfica;
- nonce / replay protection;
- secretos;
- disclosure;
- auditabilidad;
- revocación;
- aislamiento;
- resource governance.

La existencia de estos gaps **no autoriza** implementarlos ahora.

---

## 13. Project Vault

El Project Vault es downstream y derivado.

```text
Aranwill/jarvis/main = source of truth
Project Vault        = derived projection
```

La última sincronización verificada antes de PR #93 refleja:

```text
Malāk 9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

Al integrar PR #93 y este corrective packet, el Vault deberá reconciliarse de
nuevo mediante:

```text
dry-run
→ controlled-proposal
→ Draft PR
→ human review/merge
→ accept-proposal --expected-commit <new Malāk HEAD>
→ dry-run proof drift=0
```

El Sync Agent no concede autoridad ni mergea por sí mismo.

---

## 14. Evidencia reciente

PR #92 final candidate:

```text
5139d95aaa2c30971b3979ca7c3917067856a428
```

Validación independiente GitHub Actions:

```text
Ubuntu:  PASS
Windows: PASS
macOS:   PASS
Ubuntu pytest: 645 passed
compileall: PASS
diff-check: PASS
candidate identity: PASS
```

Validación local post-merge reportada por el Owner:

```text
HEAD: 9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
pytest: 645 passed
compileall -f tests: PASS
compileall -f src tests scripts: PASS
git diff --check: PASS
working tree: clean
```

PR #93 fue docs-only y su candidate
`4d41776b62fd4f001c850396cb35d365c59a6e0a` pasó Validation.

---

## 15. Disposición de planificación legacy

Los documentos históricos, fichas de sprint, commits y snapshots conservan su
valor de trazabilidad. Este roadmap no debe duplicar todo su contenido.

`ROADMAP.md` funciona como punto de entrada; este archivo es la fuente derivada
canónica de planificación actual. `documents/projects/jarvis/ideas.md` conserva
ideas y `docs/project/concepts/` conserva referencias conceptuales.

```text
idea != roadmap
roadmap != specification
specification != approval
approval != authority beyond scope
```

---

## 16. Restricciones de la siguiente iteración

Hasta autorización separada no se debe:

- abrir Sprint 7.12;
- iniciar RDD Stage 2;
- implementar Candidate Content Identity;
- implementar Persistence Authorization;
- persistir Episodic Memory;
- añadir retrieval/RAG/GraphRAG;
- promover Knowledge;
- conectar Memory al runtime conversacional;
- introducir agentes, tools, Sandbox, navegación o MCP/A2A operativo;
- añadir PKI, firmas, nonce o replay protection por arrastre;
- modificar Kernel, Blueprint, Constituciones o Security Control Plane sin gate
  propio.

---

## 17. Próximo checkpoint

```text
CURRENT:
main@3788caf68ac14da37040f06a0da3e0fe9db5a2db
Candidate Content Identity G0/G1 integrated

NEXT REQUIRED:
canonical docs corrective packet
→ human merge
→ Vault reconciliation
→ drift=0

THEN, ONLY IF OWNER AUTHORIZES:
G2 Candidate Content Identity Specification
```

Nada en este documento constituye esa autorización.