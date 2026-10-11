---
title: Contexto del proyecto Malāk
status: derived
authority: non-normative
as_of_date: 2026-10-10
as_of_commit: 02daf578012c662f0686357aa48b25722897c82a
branch: main
certification_branch: null
candidate_commit: null
certification_status: sprint_7_11_completed
baseline: v0.6.0-alpha
---

# Contexto del proyecto Malāk

## Propósito

Este documento proporciona una visión consolidada del estado observado del repositorio de Malāk.

Es un documento derivado, informativo y no normativo, destinado a ayudar a desarrolladores y asistentes automatizados a recuperar eficientemente el contexto operativo actual del proyecto.

No reemplaza, modifica ni reinterpreta:

- la Constitución Cognitiva;
- la Constitución de Gobernanza;
- el Blueprint;
- la especificación del Kernel;
- los ADR aceptados;
- los contratos centrales;
- la política de seguridad;
- los registros de release;
- las fichas de sprint aprobadas;
- el historial Git.

Si este documento entra en conflicto con una fuente normativa, histórica o con evidencia más reciente del repositorio oficial, prevalece la fuente con mayor autoridad.

---

## Regla persistente de idioma

La comunicación y la documentación futura de Malāk deben aplicar estas reglas:

- Todas las respuestas al propietario del proyecto deben estar en español.
- Toda documentación nueva debe redactarse en español.
- Los análisis, planes, informes, ADR, RFC, notas de diseño y propuestas deben estar en español.
- Los nombres de clases, funciones, módulos, APIs, comandos, rutas y términos técnicos existentes pueden mantenerse en inglés.
- No se deben traducir identificadores técnicos ni nombres existentes cuando hacerlo afecte la consistencia del código o del repositorio.
- Cuando una fuente esté en inglés, su contenido debe explicarse en español.

---

## Límites de la evidencia

Este contexto fue reconciliado a partir de:

- inspección del repositorio oficial `Aranwill/jarvis`;
- rama permanente `main`;
- historial Git y commits integrados;
- documentación oficial y derivada vigente;
- fichas de sprint;
- arquitectura implementada documentada;
- resultados de validación registrados durante el cierre del Sprint 7.8;
- revalidación local del baseline previa a la activación del Sprint 7.9;
- evidencia candidate-bound, cierre y validación post-merge de Sprint 7.11;
- integración posterior de Episodic Memory Admission, Assessment Provenance,
  Assessment Producer Authorization, Governed Input Projection y Governed
  Projection Consumption;
- validación candidate-bound multiplataforma del candidate de PR #92 y
  validación local post-G3 reportada por el Owner;
- reconciliación post-auditoría hasta `main@5865da6a5e502fe71e35e2e38bc4cceaab9b3600`;
- implementación y validación aislada de G2A — Protected Finalization Foundation
  mediante PR #110;
- integración documental de Assurance Signal Authority Boundary G0/G1 mediante
  PR #111;
- specification endurecida de G2 mediante PR #117 e implementación aislada de
  Assurance Signal Authority & Projection Foundation mediante PR #118;
- integración del Evidence Map externo como input futuro mediante PR #120;
- integración de E0 — Repository Read mediante PR #147;
- integración de E1 — Governed Knowledge Read mediante PR #148;
- integración de E2 — Engineering Inspect mediante PR #149;
- integración de E3 — Engineering Analyze mediante PR #150;
- integración de E4 — Engineering Propose mediante PR #152;
- validación candidate-bound final de E4 mediante Validation #330, con
  `1168 passed` en Ubuntu y Windows;
- integración de MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 mediante PR #173,
  con 13/13 unidades revisadas, 0 findings bloqueantes actuales y separación
  explícita entre evidencia histórica y revalidación de estado actual;
- integración de Governed Self-Review Bootstrap Task mediante PR #174 como
  referencia conceptual no normativa y candidata a una de las primeras tareas
  gobernadas de autoinspección; ejecución e implementación permanecen no
  autorizadas;
- integración de Repository Structural Projection V0 mediante PR #164 y
  Repository Structural Lookup V0 mediante PR #166;
- integración de Structural Evidence en E2 mediante PR #168 y de su observabilidad
  determinista mediante PR #170, sin propagación a E3/E4;
- integración de E2 Structural Evidence Evaluation Pack V0 mediante PR #177 como
  tooling de evaluación reproducible, sin nueva Capability, sin cambios de Kernel
  o Planner, sin persistencia y sin authority delta;
- validación post-merge de PR #177 mediante Validation #428, con `1278 passed`
  en Ubuntu y Windows, `compileall` PASS y diff validation PASS;
- integración de Internal Interaction Trace V0 mediante PR #180;
- integración de Live / Replay Visual Projection V0 mediante PR #182;
- integración de Internal Interaction Test V0 mediante PR #184;
- integración de Governed Engineering Evidence Focus V0 mediante PR #186,
  con Validation #495 y `1493 passed` en Ubuntu y Windows;
- integración de Live Elapsed / OBS-01 mediante PR #188 y Validation #502;
- integración de Safe Diagnostics / OBS-02 mediante PR #189 y Validation #513;
- integración de Runtime / Model Provenance mediante PR #190 y Validation #541;
- integración de Analyze Structured Output Contract V0 mediante PR #194 y
  Validation #565;
- integración de Runtime Generation Contract V0 mediante PR #197 y
  Validation #597;
- integración de E4 Reference-Bounded Structured Output V0 mediante PR #201 y
  Validation #611;
- promoción de KIC-01..KIC-07 a la Kernel Specification mediante PR #205;
- integración de KAF-01 mediante PR #208 y Validation #630;
- integración de E3 Epistemic Calibration mediante PR #209 y Validation #634,
  con `1599 passed` en Ubuntu y Windows;
- integración de la admisión del Octavo U01 mediante PR #210 y ejecución
  autorizada de `bootstrap-u01-20260927-008`, con disposición cognitiva
  histórica `INCONCLUSIVE` y `7 ALIGNED + 1 UNRESOLVED + 1 PARTIAL`;
- auditoría semántica del Octavo U01 con disposición
  `GAP_REQUIRES_HARDENING` y findings `E008-SG-01..03`;
- integración de Governed Engineering Relation Catalog Foundation mediante
  PR #212, con Candidate FULL 4R PASS, RDD Stage 1 Candidate Conformance PASS y
  `authority_effect = none`;
- validación post-merge de PR #212 mediante Validation #648 sobre
  `main@da4db9de845612adb42a041236f8283f0278e7d3`, con `1622 passed` en Ubuntu y Windows,
  `compileall`, candidate identity y candidate diff en PASS;
- integración de `E3 Governed Relation Consumption V0` mediante PR #215 sobre
  candidate `97cf22957b260ba6e9fec79fadec7a79654c1777`, con catálogo gobernado
  exacto expuesto al packet focalizado, `relation_id` obligatorio y allowlisted
  cuando el catálogo es no vacío, rechazo fail-closed de IDs desconocidos y
  preservación del contrato genérico cuando el catálogo está vacío;
- Validation #659 candidate-bound de PR #215 con `1626 passed` en Ubuntu y
  Windows, `compileall`, candidate identity y candidate diff en PASS; el merge
  `c87afd8c784fc1cfa50915425789679168db4cae` conserva el mismo árbol validado;
- Validation #660 revalidó post-merge
  `main@c87afd8c784fc1cfa50915425789679168db4cae` con `1626 passed` en Ubuntu
  y Windows, `compileall`, candidate identity y candidate diff en PASS;
- PR #215 no amplió autoridad ni hizo E4 relation-aware: `relation_id` identifica
  la relación gobernada evaluada, no verdad semántica, clasificación esperada,
  prioridad ni autorización;
- integración de `E3 Governed Relation Coverage & Uniqueness V0` mediante
  PR #218 sobre candidate `b6d3d7d42c69610d1e26fbee2ad1778ee45755d0`,
  exigiendo cobertura exacta y única del catálogo gobernado en E3 focalizado,
  canonización al orden del catálogo y rechazo pre-modelo cuando el catálogo
  supera la capacidad máxima de findings;
- Candidate FULL 4R PASS, Fix Validator PASS y RDD Stage 1 Candidate Conformance
  PASS para PR #218, con Validation #667 candidate-bound y `1633 passed` en
  Ubuntu y Windows;
- merge de PR #218 en
  `70989b1878f1f4f9289c65611c3d7b561d5ae286`, conservando el árbol del
  candidate validado, y Validation #668 post-merge con `1633 passed` en
  Ubuntu y Windows, `compileall`, candidate identity y candidate diff en PASS;
- PR #218 no demuestra semantic entailment: E008-SG-02 permanece abierto,
  E008-SG-03 continúa como assurance boundary y no hubo nueva ejecución de
  Runtime Self-Review;
- integración de `E3 Structured Evidence Role Binding V0` mediante PR #222
  sobre candidate `e4632bc4b94da93ce9003d066a47403c8e87b191`, con
  `supporting_repository_refs`, `supporting_knowledge_refs`,
  `limiting_or_counterevidence_refs` y `uncertainty_basis` ligados al
  evidence packet exacto del path relation-aware;
- Validation #681 candidate-bound de PR #222 con `1644 passed` en Ubuntu y
  Windows, `compileall`, candidate identity y candidate diff en PASS, después
  de bounded correction 1/2 limitada a fixtures/tests de compatibilidad;
- merge de PR #222 en
  `9b40820790a2179b1dc42c60a714ac3d1686b2e7`, con árbol idéntico al candidate
  validado, y Validation #682 post-merge con `1644 passed` en Ubuntu y Windows;
- PR #222 endurece estructuralmente E008-SG-02 pero no demuestra semantic
  entailment: `semantic_assurance: NOT_VERIFIED`, E008-SG-02 permanece OPEN y
  E008-SG-03 continúa como assurance boundary; E4 permanece relation-less y
  `authority_effect = none`;

El documento:

```text
PROJECT - MANIFIESTO MALAK (1).docx
```

permanece rechazado y no debe utilizarse como fuente de autoridad ni influir en decisiones de Malāk.

---

## Clasificación documental

### Fuentes normativas

Las principales fuentes de cumplimiento obligatorio son:

1. `docs/governance/cognitive_constitution.md`
2. `docs/governance/governance_constitution.md`
3. `docs/architecture/blueprint.md`
4. `docs/architecture/kernel.md`
5. `docs/architecture/architecture_quality_gates.md`
6. ADR aceptados y contratos públicos aprobados
7. `SECURITY.md`
8. estándares aplicables de desarrollo y repositorio

### Fuentes históricas

Las fuentes históricas incluyen:

- snapshots de release;
- changelogs;
- registros de migración;
- historial de Git;
- historial de ADR aceptados;
- documentos que conservan intencionalmente la identidad anterior de Jarvis.

Los snapshots históricos describen el estado certificado en su fecha. Una diferencia entre un snapshot histórico y el HEAD actual no constituye, por sí sola, permiso para reescribir ese snapshot.

### Fuentes derivadas

Las fuentes derivadas incluyen:

- este `project_context.md`;
- resúmenes de estado marcados explícitamente como no normativos;

Los documentos derivados pueden informar evidencia y contexto de planificación, pero no pueden aprobar arquitectura, alcance de sprint ni implementación.

---

## Snapshot validado del repositorio

```text
Repositorio oficial:               Aranwill/jarvis
Raíz Git local:                    D:\Ollama\jarvis
Rama permanente:                   main
Commit integración Sprint 7.11:   3413e8ccb348440aea757d1feccde25c65be011f
Main HEAD reconciliado:             a05aa5f081971f36c133ac50dc0756f938a26a1a
Baseline material/productivo reconciliado: e1a1973b7b6cf635337a77e81410ebb873f57bde
Baseline nominal:                  v0.6.0-alpha
Último sprint numerado integrado:  Sprint 7.11 — Reproducible Validation Pipeline Foundation
Última ruta conversacional:        Sprint 7.10 — Conversation Session Isolation Foundation
Engineering Intelligence:          E0–E4 + E5-A/B1 integrados; E5-B2/B3 diferidos
Internal Interaction Trace V0:     integrado — PR #180
Live / Replay Projection V0:       integrado — PR #182
Internal Interaction Test V0:      integrado — PR #184
Governed Evidence Focus V0:        integrado — PR #186
Live Elapsed / OBS-01:             integrado — PR #188
Safe Diagnostics / OBS-02:         integrado — PR #189
Runtime / Model Provenance:        integrado — PR #190
Analyze Structured Output V0:      integrado — PR #194
Runtime Generation Contract V0:    integrado — PR #197
E4 Reference-Bounded Output V0:    integrado — PR #201
Kernel KIC-01..KIC-07:             promoción normativa integrada — PR #205
KAF-01:                            integrado — PR #208
E3 Epistemic Calibration:          integrado — PR #209
Governed Relation Catalog U01:     integrado — PR #212
E3 Governed Relation Consumption:  integrado — PR #215 / authority_effect none
E3 Relation Coverage & Uniqueness:  integrado — PR #218 / authority_effect none
E3 Structured Evidence Role Binding: integrado — PR #222 / authority_effect none
E3 Governed Evidence Support Assessment: integrado — PR #224 / semantic_assurance NOT_VERIFIED / authority_effect none
E3 Assessor Qualification Pack V0.1: integrado — PR #230 / offline evaluation / authority_effect none
E3 Governed Support Evidence Routing V0: integrado — PR #235 / authority_effect none
E3 Governed Qualification Consumption V0: integrado en línea #235/#240 / fail-closed
E3 Positive Qualification Consumption Trust Boundary V0: integrado — PR #250 / authority_effect none
Construction two-PR model:          integrado — PR #251 / process-only
Última validación candidate-bound:  Validation #37169199842 / 1875 passed Ubuntu + Windows
Última validación post-merge:       Validation #37208582290 / 1875 passed Ubuntu + Windows
Seventh U01:                       bootstrap-u01-20260926-007 / INCONCLUSIVE
Seventh findings:                  3 ALIGNED + 3 UNRESOLVED
U007-F05 / KAF-01 / E3 Calibration: cerrados e integrados
Eighth U01:                        bootstrap-u01-20260927-008 / INCONCLUSIVE
Eighth findings:                   7 ALIGNED + 1 UNRESOLVED + 1 PARTIAL
Semantic grounding audit:          histórico GAP_REQUIRES_HARDENING / sin nueva reevaluación runtime
E008-SG-01 structural hardening:    PR #218 integrado / exact coverage + uniqueness + canonical order
E008-SG-02 evidence binding:        OPEN / PR #222 + #224 + #230 + #235 + #250 integrados; positive qualification consumption existe, semantic entailment NOT_VERIFIED y no hay assessor productivo autorizado
E008-SG-03 assurance boundary:      preservado / GROUNDED != semantic entailment verified
Relation catalog foundation:       integrado — PR #212
E3 relation consumption:           integrado — PR #215 / relation identity != semantic truth
E3 relation coverage/uniqueness:   integrado — PR #218
E3 structured evidence role binding: integrado — PR #222 / exact packet refs + role separation
E3 governed evidence support assessment: integrado — PR #224 / bounded support assessment / semantic_assurance NOT_VERIFIED
E4 relation consumption:           sin cambio / no relation-aware
Runtime Self-Review:               run 008 ejecutado; nueva ejecución requiere admisión + preflight + autorización separada
RDD Stage 1 PR #212:               PASS / authority_effect none
RDD Stage 1 PR #222:               PASS / authority_effect none
RDD Stage 1 PR #230:               PASS / authority_effect none
RDD Stage 1 PR #250:               PASS / authority_effect none
Self-modification:                 no autorizada
RDD Stage 2:                       no autorizado
Structural Evidence E3/E4:         diferido / no propagado
Structural Delta:                  diferido
```

Sprint 7.11 — `Reproducible Validation Pipeline Foundation` fue admitido,
autorizado, implementado, validado e integrado mediante PR #65.

El candidato final validado fue:

```text
59f592e2e36d11bbd14f7d9d93b1dac4f442c108
```

La integración se realizó mediante PR #65 con merge commit:

```text
3413e8ccb348440aea757d1feccde25c65be011f
```

Evidencia del candidato y validación post-merge:

```text
388 passed
compileall: PASS
git diff --check: PASS
FULL 4R: PASS
independent validation: PASS
post-merge Validation: success
```

Después de Sprint 7.11, el Owner autorizó de forma separada y acotada una serie
de unidades episódicas aisladas de Memory.

La primera fue G3 — `Episodic Memory Admission Boundary`, integrada mediante PR #76:

~~~text
candidate:
e3e3c2aa6031d4a6a9ad8f3a3c529a9453cbbe9b

merge:
2d5fe87c304927baeab29e5649f2383030e1a1fd

pytest:
431 passed

compileall:
PASS

git diff --check:
PASS

post-merge Validation:
success
~~~

Después se integraron, cada una mediante autorización y gate separados:

```text
PR #82
Episodic Admission Assessment Provenance Boundary

PR #85
Episodic Admission Assessment Producer Authorization Boundary

PR #88
Episodic Admission Governed Input Projection Boundary

PR #92
Episodic Admission Governed Projection Consumption Boundary
```

El HEAD de producto resultante de esa cadena es:

```text
9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

El candidate de PR #92:

```text
5139d95aaa2c30971b3979ca7c3917067856a428
```

pasó `Validation` candidate-bound en `ubuntu-latest`, `windows-latest` y
`macos-latest`, incluyendo candidate identity, suite completa, `compileall` y
candidate diff validation. Ubuntu reportó `645 passed`.

La cadena materializada preserva:

```text
Assessment Provenance
!= authenticated identity
!= trusted truth

Producer Authorization
!= trusted truth
!= Admission eligibility
!= persistence authorization
!= authority

Projection READY
!= Admission ELIGIBLE
!= Stored
!= Authority

Consumption EVALUATED
!= persistence authorization
!= Authority
```

La proyección continúa sin ejecutar por sí misma la policy de Admission. La
frontera de consumo integrada en PR #92 valida la projection, construye una vista
efímera con `effective_context` y, únicamente cuando es consumible, delega una
vez a `evaluate_episodic_candidate(...)`. No persiste Memory ni introduce side
effects.

Después de esa cadena se integraron, también mediante gates separados:

- PR #93: G0/G1 de `Episodic Candidate Content Identity Boundary`;
- PR #97–#99: investigación y diseño de Evidence-Bound Cognition / Progressive
  Cognitive Assurance;
- PR #100–#109: activación normativa, trazabilidad, reconciliaciones y fixes del
  baseline auditado hasta `5865da6a5e502fe71e35e2e38bc4cceaab9b3600`;
- PR #110: G2A — `Protected Finalization Foundation`, implementado y validado en
  aislamiento;
- PR #111: `Assurance Signal Authority Boundary — G0/G1`, documental;
- PR #117: hardening de la specification candidata de G2;
- PR #118: `Assurance Signal Authority & Projection Foundation — G2`, implementada
  y validada en aislamiento;
- PR #120: Evidence Map externo agregado de forma aditiva al Research Horizon.

G2A incorpora `ProtectedResponseCandidate`, `ProtectedFinalizationInput`, una
policy determinista versionada y outcomes `ACCEPT | ABSTAIN | BLOCK`, sin wiring
con Conversation, Kernel, Memory, Knowledge ni persistencia.

G2 incorpora una proyección determinista same-process desde evidencia de signals
y decisiones de autorización estructuralmente verificadas hacia
`ProtectedFinalizationInput`. Valida binding de request/session/candidate,
producer subject/authentication, permission scope sensible a kind+value,
coherencia temporal, authorization binding, policy version, exact completeness y
permutaciones, y falla cerrado ante inconsistencias. No decide verdad cognitiva,
no persiste, no hace I/O ni red y no prueba por sí solo provenance criptográfica
del `AuthorizationDecision`.

En ese corte histórico, hasta PR #120, permanecía fuera de alcance:

~~~text
Conversation/runtime wiring de la cadena episódica
Candidate Content Identity G2 / implementation / propagation
Persistence Authorization
Memory persistente
retrieval
Knowledge
Kernel changes
Conversation Finalization Integration / G2B
Security authority expansion
Observability changes
external dependencies
Sprint 7.12
RDD Stage 2
~~~

Ese bloque es histórico y no describe por sí solo el estado mutable actual. Las
integraciones posteriores de Candidate Content Identity, su propagation/binding,
Persistence Readiness y Authorization Request Composition se reflejan en la
sección de planificación vigente de este documento.

Sprint 7.10 permanece como la última ruta conversacional/runtime integrada.
G2A y G2 son foundations aisladas de finalización protegida y assurance signal
projection; no constituyen assurance conversacional end-to-end.


---

## Estructura relevante del repositorio

```text
jarvis/
├── .github/
├── configs/
├── docs/
│   ├── architecture/
│   ├── development/
│   ├── governance/
│   ├── knowledge/
│   ├── operations/
│   └── project/
├── documents/projects/jarvis/
├── examples/
├── scripts/
├── src/
│   ├── app/
│   └── malak/
│       ├── app/
│       ├── capabilities/
│       ├── contracts/
│       ├── core/
│       ├── events/
│       ├── identity/
│       ├── infrastructure/
│       ├── kernel/
│       ├── memory/
│       ├── observability/
│       ├── providers/
│       ├── runtime/
│       ├── security/
│       ├── services/
│       └── shared/
├── tests/
├── CHANGELOG.md
├── PROJECT.md
├── README.md
├── ROADMAP.md
├── SECURITY.md
└── pyproject.toml
```

`D:\Ollama` es el espacio de trabajo contenedor y no la raíz Git. Los comandos del repositorio deben ejecutarse desde:

```text
D:\Ollama\jarvis
```

---

## Arquitectura implementada actual

### Engineering Intelligence — E0–E5-B1

El vertical bounded de Engineering Intelligence, sus superficies read-only y el
tooling de evaluación estructural de E2 están reconciliados contra
`main@e29d3dc79445506aa9bb4e59a8383524d627db68`:

```text
E0 Repository Read          PR #147  INTEGRATED
        +
E1 Governed Knowledge Read  PR #148  INTEGRATED
        ↓
shared bounded evidence
        ├── E2 Engineering Inspect  PR #149  INTEGRATED
        └── structured analysis
              ├── E3 Engineering Analyze  PR #150  INTEGRATED
              └── E4 Engineering Propose  PR #152  INTEGRATED
                                                ↓
                                              Owner

E5-A Command Surface        PR #155  INTEGRATED
E5-B1 Read-only Explorer    PR #157  INTEGRATED
E5-B2 Runtime Context       DEFERRED
E5-B3 Engineering Artifacts DEFERRED

Repository Structural Projection V0     PR #164  INTEGRATED
Repository Structural Lookup V0         PR #166  INTEGRATED
E2 Structural Evidence Integration V0   PR #168  INTEGRATED
E2 Structural Evidence Observability V0 PR #170  INTEGRATED
E2 Structural Evidence Evaluation Pack  PR #177  INTEGRATED / EVALUATION TOOLING

Structural Evidence propagation E3/E4   DEFERRED
Structural Delta                        DEFERRED
```

E0–E4 permanecen read-only y E5-A/B1 sólo exponen esas capacidades y readers
mediante routing/navegación deterministas de aplicación. No introducen writes,
agents, sandbox ni autoridad operacional. E3 produce findings grounded y E4
transforma únicamente findings elegibles en propuestas bounded para revisión
humana.

Se preserva:

```text
analysis != decision
finding != authorization
proposal != decision
proposal != authorization
proposal != implementation
proposal != execution
evidence != authority
```

La validación final de E4 utilizó candidate
`3463f1c391f6a11de70a0d6ecfc37c4127da21cb`, Validation #330, con
`1168 passed` en Ubuntu y Windows. El merge de PR #152 produjo
`14122dd2d0c94d1c2d5ba1a68b6ae43bcb1c2c9e`.

### Flujo Kernel–Planner–Capability

La frontera cognitiva oficial permanece orientada al Kernel:

```text
Interface Layer
→ Application Composition
→ Kernel.receive()
→ Planner
→ CapabilityRegistry
→ Capability
→ Response
```

El Kernel:

- coordina el flujo;
- permanece independiente de providers concretos;
- permanece independiente de runtimes concretos;
- permanece independiente de modelos concretos;
- no depende directamente de Ollama;
- no contiene lógica de configuración de infraestructura;
- no incorpora autoridad autónoma;
- no accede directamente a Internet;
- no debe convertirse en orquestador de infraestructura.

El bootstrap mínimo del Kernel conserva `EchoCapability` como Capability
determinista para validaciones estructurales.

La composición conversacional vigente es distinta: se construye en la frontera
de aplicación, registra `ConversationCapability` y configura el `Planner` para
resolver esa capability sin introducir `ConversationService`, providers,
runtimes o modelos dentro del Kernel.

### Stack conversacional

El stack conversacional implementado contiene:

- `ConversationCapability`;
- `ConversationMessage`;
- `ConversationRequest`;
- `ConversationResponse`;
- `ConversationProvider`;
- `RuntimeConversationProvider`;
- `ConversationProviderRegistry`;
- `ConversationProviderNotFoundError`;
- `ConversationService`;
- `InMemoryConversationContext`;
- `LLMRuntime`;
- `MockLLMRuntime`;
- `OllamaRuntime`.

Ruta cognitiva conversacional vigente:

```text
CLI
→ CLIConfiguration
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

La selección y construcción del runtime, provider y servicios se realiza en la
frontera de aplicación mediante configuración externa.

Sprint 7.9 añadió continuidad conversacional efímera mediante
`InMemoryConversationContext`, integrada opcionalmente en `ConversationService`
y mantenida fuera del Kernel y de `SecurityContext`.

Sprint 7.10 añade aislamiento explícito de sesiones conversacionales.
`Request.session_id` se preserva a través de la frontera de Capability,
`ConversationService` selecciona el contexto mediante esa identidad y
`InMemoryConversationContext` mantiene ventanas independientes por sesión.

La evolución no introduce persistencia, Memory ni estado conversacional
dentro del Kernel o de `SecurityContext`.

### Episodic Memory Admission chain — estado post-PR #92

La Memory Layer posee ahora varias fronteras aisladas bajo:

~~~text
src/malak/memory/
~~~

La policy de admisión original permanece pura y determinista:

~~~text
EpisodicMemoryCandidate
+
EpisodicAdmissionSignals
        ↓
REJECT | HOLD | ELIGIBLE
~~~

Sobre esa foundation se integró una cadena de evidencia, proyección y consumo separada:

~~~text
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
~~~

La proyección reconstruye un `EpisodicAdmissionContext` y
`EpisodicAdmissionSignals` efectivos solo cuando existe evidencia completa,
coherente, candidate-bound y autorizada. Source authority, confidence,
sensitivity y temporal validity no se heredan como trust por mera presencia en
`candidate.control`.

Se preservan explícitamente:

~~~text
Candidate != Decision
payload != control metadata
source authority != confidence != security trust != temporal validity
structural provenance != authenticated identity
AUTHORIZED != trusted truth
Projection READY != Admission ELIGIBLE
Consumption EVALUATED != persistence authorization
ELIGIBLE != persistence authorization
HOLD != retention authorization
~~~

La projection no modifica la precedencia de Admission. El adapter de consumo
bloquea projections no consumibles y delega exactamente una vez a la policy de
admisión para un candidate efectivo efímero cuando corresponde.

Toda la cadena continúa desconectada de `ConversationCapability`,
`ConversationService`, Kernel y observabilidad; tampoco persiste ni recupera
Memory.

### Protected Finalization Foundation — G2A

PR #110 integró una foundation aislada bajo:

```text
src/malak/core/protected_finalization.py
```

Contratos principales:

```text
ProtectedResponseCandidate
ProtectedFinalizationInput
ProtectedFinalizationDecision
AssuranceApplicability
ProtectedFinalizationOutcome
ProtectedFinalizationReason
```

La policy `protected-finalization/v1` es determinista y produce únicamente:

```text
ACCEPT | ABSTAIN | BLOCK
```

Preserva:

```text
candidate != decision
unknown != accepted
missing support != sufficient support
provider identity != source authority
Evidence != Authority
Generation != Finalization
```

G2A permanece aislado. No modifica `ConversationCapability`,
`ConversationService`, historial, Kernel, provider/runtime, Memory, Knowledge o
persistencia.

PR #111 confirmó el gap de autoridad de los signals y PR #118 integró G2 como
frontera determinista de proyección autorizada. El estado resultante preserva:

```text
producer permission != signal truth
Security authorization != Cognitive policy disposition
G2 READY != G2A ACCEPT
```

G2 construye `ProtectedFinalizationInput` solo ante evidencia completa, coherente
y autorizada, pero permanece same-process y aislado de Conversation/runtime.
Conversation G2B continúa bloqueado y no autorizado.

### Integración Kernel–ConversationService

Sprint 7.8 estableció y validó formalmente la integración entre el pipeline
cognitivo y el subsistema conversacional mediante `ConversationCapability`.

La frontera preservada es:

```text
Kernel
→ Capability
```

`ConversationCapability` adapta la solicitud del pipeline cognitivo al contrato
de `ConversationService` y transforma su resultado para devolverlo por la
frontera de Capability.

Por lo tanto:

- `Kernel.receive()` y `ConversationService` ya forman parte de una misma ruta
  cognitiva conversacional validada;
- el Kernel no conoce `ConversationService`;
- el Kernel no conoce providers concretos;
- el Kernel no conoce runtimes concretos;
- el Kernel no conoce modelos concretos;
- la evidencia de ejecución no concede autoridad ni altera el flujo de control.

---

## Abstracción de runtime

`LLMRuntime` permanece como el único punto de abstracción para integraciones de runtime LLM.

Runtimes implementados:

- `MockLLMRuntime`;
- `OllamaRuntime`.

### MockLLMRuntime

Uso:

- desarrollo;
- pruebas deterministas;
- validaciones reproducibles;
- ejecución sin servicio externo.

### OllamaRuntime

Estado:

```text
implementado
```

Características:

- integración local con Ollama;
- composición externa al Kernel;
- configuración mediante variables de entorno;
- validación de entrada;
- manejo de errores HTTP;
- manejo de errores de conexión;
- manejo de timeout;
- validación de payloads;
- soporte para métricas mediante interfaces desacopladas;
- límites explícitos de tamaño para payloads de transporte incorporados por el
  fix de PR #109.

La integración real fue validada durante Sprint 7.8 con `OllamaRuntime` y un modelo local, sin convertir Ollama en dependencia del Kernel.

---

## Métricas, eventos operativos y auditoría

Los tres subsistemas permanecen separados.

### Métricas

Se utilizan para medir rendimiento y comportamiento cuantificable.

El repositorio contiene:

- muestras normalizadas de métricas;
- almacenamiento en memoria;
- almacenamiento JSONL;
- perfiles de rendimiento;
- generación de perfiles estadísticos.

### Eventos operativos

Sprint 7.4 incorporó:

- `OperationalEvent`;
- `OperationalEventSink`;
- stores operativos separados;
- correlación mediante `request_id`;
- integración opcional desde la CLI.

### Auditoría de seguridad

Sprint 7.5 incorporó evidencia estructurada de autorización separada de métricas y eventos operativos.

No existe un envelope universal entre métricas, eventos y auditoría.

No comparten:

- contratos;
- stores;
- políticas de error;
- políticas de retención;
- autoridad.

Pueden compartir únicamente convenciones mínimas de trazabilidad.

---

## Security Control Plane Foundation

El Sprint 7.5 está cerrado.

La fundación implementada establece separación entre:

```text
solicitar
→ decidir
→ aplicar
→ auditar
→ ejecutar operación protegida
```

Componentes fundamentales:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationDecision`;
- Policy Decision Point mínimo;
- Policy Enforcement Point inicial;
- contratos de auditoría de autorización;
- integración fail-closed de la evidencia de auditoría.

### Policy Decision Point

Propiedades:

- determinista;
- sin LLM;
- denegación por defecto;
- fail-closed;
- confirmación humana explícita cuando corresponde;
- ninguna confirmación modifica retroactivamente una decisión anterior.

### Policy Enforcement Point

Propiedades:

- consulta directamente al PDP inyectado;
- no acepta decisiones aportadas por el llamador;
- exige asociación consistente entre solicitud y decisión;
- ejecuta la operación protegida únicamente ante una decisión válida y permitida;
- bloquea ante errores, incongruencias o respuestas inválidas;
- permanece separado del Kernel y del Planner.

### Auditoría de autorización

La evidencia de autorización:

- es estructurada;
- permanece separada de métricas y eventos operativos;
- forma parte del comportamiento fail-closed;
- no concede autoridad;
- no reemplaza la decisión de autorización.

---

## Secure Context Lifecycle Foundation

El Sprint 7.6 está cerrado.

La fundación implementada establece un lifecycle temporal explícito para
`SecurityContext`, sin ampliar autoridad ni introducir todavía identidad
criptográfica o transporte seguro entre procesos.

Componentes incorporados o consolidados:

- `SecurityContext` con `context_id`, `session_id`, `subject_id`,
  `authenticated`, `issued_at`, `expires_at` y `parent_context_id`;
- frontera temporal `Clock` / `SystemClock`;
- `SecurityContextValidator`;
- `SecurityContextIssuer`;
- `SecurityContextRenewer`;
- enforcement temporal en `StaticPolicyDecisionPoint`;
- semántica de validez `issued_at <= now < expires_at`;
- `SecurityContextEnvelope` para propagación inmutable en memoria.

Propiedades relevantes:

- contextos futuros son inválidos antes de `issued_at`;
- contextos expiran exactamente en `expires_at`;
- la renovación exige que el contexto anterior continúe vigente;
- la renovación preserva sesión, sujeto y estado de autenticación;
- cada renovación genera un nuevo `context_id` y conserva lineage mediante
  `parent_context_id`;
- el PDP valida lifecycle antes de evaluar políticas;
- la propagación conserva el mismo `SecurityContext` sin reconstruirlo;
- Validator, Issuer, Renewer y Envelope no conceden permisos;
- Kernel, Planner y runtimes permanecieron fuera del alcance.

Permanecen fuera de alcance:

- nonce y replay protection;
- identidad y firmas criptográficas;
- MFA;
- Secure Context Manager criptográfico completo;
- Secure Message Bus;
- IPC seguro;
- receipts / RDD;
- agentes, navegación y rutas operativas reales de alto riesgo.

---

## Riesgo de seguridad residual

Permanece registrado el finding:

```text
7.7-D-001 — Strong SecurityContext Provenance
classification: ACCEPTED_RESIDUAL_RISK
severity: MEDIUM
blocking_release: NO
```

La foundation actual todavía no incorpora de forma completa:

- PKI;
- nonce;
- replay protection;
- identidad criptográfica fuerte;
- MFA;
- Secure Message Bus;
- Secure Context Manager criptográfico completo.

Este riesgo no bloquea el baseline actual, pero debe permanecer visible antes de
incorporar agentes, tools, red, mensajería externa, automatización o rutas
operativas de mayor riesgo.

Su existencia no autoriza por sí sola una implementación de seguridad adicional.

---

## Estado de sprints

Estado del bloque 7.x:

| Sprint | Estado | Resultado |
|---|---|---|
| 7.0 | Cerrado | CLI mínima con `MockLLMRuntime` |
| 7.1 | Cerrado | Composición de CLI con `OllamaRuntime` |
| 7.2 | Cerrado | `RuntimeMetricSink` |
| 7.3 | Cerrado | Conversation Provider Boundary Stabilization |
| 7.4 | Cerrado | Logs, métricas, eventos operativos y sincronización gobernada |
| 7.5 | Cerrado | Security Control Plane Foundation |
| 7.6 | Cerrado | Secure Context Lifecycle Foundation |
| 7.7 | Cerrado | Validación de baseline y release interna |
| 7.8 | Completado | Cognitive Conversation Execution Path Foundation |
| 7.9 | Completado | Conversation Continuity Foundation; cierre aprobado por el propietario |
| 7.10 | Completado | Conversation Session Isolation Foundation; integrado y validado post-merge |
| 7.11 | Completado | Reproducible Validation Pipeline Foundation; integrado y validado post-merge |

Las unidades episódicas y cognitivas integradas después de Sprint 7.11 no
constituyen Sprint 7.12 y no alteran la numeración histórica del bloque 7.x.

### Sprint 7.0

Estado:

```text
cerrado
```

Resultado:

- CLI técnica mínima;
- soporte para `MockLLMRuntime`;
- comandos básicos;
- control de errores;
- sin integración formal con `Kernel.receive`.

### Sprint 7.1

Estado:

```text
cerrado
```

Resultado:

- soporte para `OllamaRuntime`;
- configuración externa;
- Runtime Independence preservada;
- Kernel sin modificación.

### Sprint 7.2

Estado:

```text
cerrado
```

Resultado:

- `RuntimeMetricSink`;
- contrato estructural de solo escritura;
- separación respecto de stores concretos.

### Sprint 7.3

Estado:

```text
cerrado
```

Resultado:

- estabilización del límite entre `ConversationService`, provider y runtime;
- incorporación de `RuntimeConversationProvider`;
- fortalecimiento de `ConversationProviderRegistry`;
- manejo explícito de provider inexistente;
- Kernel y Planner intactos.

### Sprint 7.4

Estado:

```text
cerrado
```

Resultado:

- consolidación de eventos operativos;
- correlación desde CLI;
- separación entre métricas, eventos y auditoría;

### Sprint 7.5

Estado:

```text
cerrado
```

Resultado:

- contratos fundamentales de autorización;
- PDP mínimo determinista;
- PEP inicial;
- auditoría de autorización;
- revisión integral y cierre;
- sin habilitar rutas operativas reales de alto riesgo.

El cierre del Sprint 7.5 no autoriza automáticamente ningún sprint posterior.

### Sprint 7.6

Estado:

```text
cerrado
```

Resultado:

- lifecycle temporal explícito para `SecurityContext`;
- frontera `Clock`;
- validación temporal determinista;
- emisión y renovación con lineage;
- enforcement fail-closed en PDP;
- semántica `issued_at <= now < expires_at`;
- propagación inmutable en memoria mediante `SecurityContextEnvelope`;
- Kernel, Planner y runtimes sin cambios;
- sin identidad criptográfica, replay protection ni Secure Message Bus.

El cierre del Sprint 7.6 no autoriza automáticamente Sprint 7.7 ni ninguna
implementación posterior.

### Sprint 7.7

Estado:

```text
cerrado
```

Resultado:

- validación integral y certificación interna del baseline;
- reconciliación de arquitectura y documentación;
- cierre del proceso de certificación;
- preservación de `7.7-D-001` como riesgo residual aceptado, MEDIUM y no bloqueante.

### Sprint 7.8

Estado:

```text
completado
```

Resultado:

- primera ruta cognitiva conversacional end-to-end;
- incorporación de `ConversationCapability` como adapter detrás de la frontera de Capability;
- integración `Kernel.receive()` → `Planner` → `CapabilityRegistry` → `ConversationCapability`;
- preservación de Runtime Independence;
- validación determinista con `MockLLMRuntime`;
- validación real con `OllamaRuntime`;
- 348 pruebas totales aprobadas durante el cierre documentado.

El cierre de Sprint 7.8 no autorizó automáticamente Sprint 7.9 ni ninguna otra
unidad de implementación.

Sprint 7.9 fue autorizado posteriormente mediante un proceso independiente de
inspección, definición, evaluación, debate y aprobación explícita.

### Sprint 7.9

Estado:

```text
completado
```

Objetivo autorizado:

- continuidad conversacional efímera durante una conversación activa;
- historial estructurado y limitado en memoria;
- limpieza explícita del contexto conversacional;
- integración aditiva y reversible;
- preservación de Kernel, Planner, Capability contract y SecurityContext.

Baseline de activación:

```text
2864435401353e5abcfcb51fc276361a0225c2b7
```

Rama temporal:

```text
sprint/7.9-conversation-continuity
```

Estado de ejecución:

```text
gates 7.9-A → 7.9-H: PASS
candidato funcional validado: d58b8ec98d48f5e2eac115d1d54b193e1df617fd
suite final: 365 passed
runtime real: PASS
revisión final 4R: PASS
cierre del sprint: aprobado por el propietario el 2026-09-03
```

Sprint 7.9 no autoriza Memory persistente, agentes, tools, Sandbox, navegación,
Internet, RAG, GraphRAG, cambios del Kernel, generalización del contrato
Capability ni ampliación de autoridad.

---

## Validación

Última validación integral documentada durante el cierre de Sprint 7.8:

```text
348 total passed
compileall: PASS
git diff --check: PASS
```

La ruta cognitiva conversacional fue validada tanto con runtime determinista como
con `OllamaRuntime`, preservando el desacoplamiento del Kernel.

Antes de activar Sprint 7.9 se revalidó localmente el baseline de referencia:

```text
main == origin/main
commit reconciliado: 2864435401353e5abcfcb51fc276361a0225c2b7
working tree: clean
Python: 3.12.10
virtual environment: .venv
pytest: 348 passed
compileall: PASS
git diff --check: PASS
```

La validación anterior certifica el punto de partida técnico del sprint.

El candidato funcional de Sprint 7.9 fue validado posteriormente:

```text
candidate: d58b8ec98d48f5e2eac115d1d54b193e1df617fd
pytest: 365 passed
compileall: PASS
git diff --check baseline..candidate: PASS
runtime real: PASS
revisión final 4R: PASS
```

La implementación, validación y revisión están completas. El propietario
aprobó explícitamente el cierre del Sprint 7.9 el 2026-09-03.

La actualización de este documento registra evidencia y una autorización humana
ya emitida; no crea autoridad por sí misma ni autoriza ningún sprint posterior.

La evidencia candidate-bound más reciente de la cadena episódica corresponde al
candidate de PR #92 `5139d95aaa2c30971b3979ca7c3917067856a428`, cuya ejecución
`Validation` concluyó con `success` en Ubuntu, Windows y macOS; Ubuntu reportó
`645 passed`.

La evidencia candidate-bound de G2A corresponde a PR #110. Su candidate final
pasó `Validation` en Ubuntu, macOS y Windows, incluyendo candidate identity,
pytest, `compileall` y candidate diff validation; una corrida Ubuntu sobre el
mismo código G2A reportó `676 passed`.

La evidencia candidate-bound de G2 corresponde a PR #118 y candidate
`0bd6fa4f7be908fc7bec3c5fa49b80b40acc3dfb`. Validation #147 pasó en Ubuntu y
Windows con candidate identity, suite completa, `compileall` y candidate diff;
FULL 4R concluyó PASS. El merge fue `cd50c308e1f5a1481851d6402ae4435341410d27`.

PR #120, exclusivamente documental, pasó candidate-bound Validation en Ubuntu y
Windows y su push post-merge sobre `main@3690d5f50183eec51d7edde2eb5e0954582f1f3a`
concluyó `success`.

---

## Estado del baseline

Baseline nominal:

```text
v0.6.0-alpha
```

El baseline nominal no debe confundirse con el commit de desarrollo utilizado
como referencia de reconciliación.

Estado reconciliado:

```text
rama permanente: main
HEAD integrado de referencia: e29d3dc79445506aa9bb4e59a8383524d627db68
commit integración Sprint 7.11: 3413e8ccb348440aea757d1feccde25c65be011f
Sprint 7.7: cerrado
Sprint 7.8: completado
Sprint 7.9: completado
Sprint 7.10: completado
Sprint 7.11: completado e integrado
última ruta conversacional/runtime: Sprint 7.10
última foundation previa: Assurance Signal Authority & Projection Foundation — G2
última unidad funcional/runtime integrada: E5-B1 — Read-only Explorer
Engineering Intelligence E0: integrado
Engineering Intelligence E1: integrado
Engineering Intelligence E2: integrado
Engineering Intelligence E3: integrado
Engineering Intelligence E4: integrado
Engineering Intelligence E5-A: integrado
Engineering Intelligence E5-B1: integrado
Engineering Intelligence E5-B2/B3: diferido
Repository Structural Projection V0: integrado
Repository Structural Lookup V0: integrado
E2 Structural Evidence Integration V0: integrado
E2 Structural Evidence Observability V0: integrado
E2 Structural Evidence Evaluation Pack V0: integrado / evaluation tooling
Structural Evidence propagation E3/E4: diferido
Structural Delta: diferido
último diseño Memory: Episodic Candidate Content Identity G0/G1
última unidad cognitiva de assurance: Assurance Signal Boundary G2
candidate E4: 3463f1c391f6a11de70a0d6ecfc37c4127da21cb
merge E4: 14122dd2d0c94d1c2d5ba1a68b6ae43bcb1c2c9e
validation E4: Validation #330 / 1168 passed Ubuntu + Windows
certification branch activa: no
release promovida adicional: no
sprint actualmente autorizado: ninguno
Signal Boundary G2: integrado / aislado
Conversation G2B: bloqueado / no autorizado
RDD Stage 2: no autorizado
post-merge Validation #428: 1278 passed Ubuntu + Windows / PASS
```

El commit `3413e8ccb348440aea757d1feccde25c65be011f` continúa siendo el estado de
`main` resultante de integrar Sprint 7.11, pero ya no es el HEAD material actual.

Sprint 7.11 no modificó el producto/runtime. La última ruta conversacional/runtime
permanece Sprint 7.10. Las unidades episódicas posteriores ampliaron la Memory
Layer de forma aislada; PR #110 añadió G2A y PR #118 añadió G2 como foundations
aisladas sin wiring conversacional.

No debe certificarse una nueva release, crear o mover un tag, abrir Sprint 7.12,
habilitar Persistence Authorization decision/enforcement, Protected Durable
Write, Persistent Memory o Conversation G2B sin un proceso específico de
evaluación y aprobación.

---

## Planificación vigente — post-E3 / D0

Sprint 7.8 está completado.

Sprint 7.9 fue completado y su cierre fue aprobado explícitamente por el
propietario el 2026-09-03.

Sprint 7.10 fue completado e integrado y su cierre fue aprobado explícitamente por el propietario el 2026-09-04.

Sprint 7.11 fue completado, integrado mediante PR #65 y validado nuevamente sobre `main`.

Después de Sprint 7.11 fueron integradas de forma separada Episodic Memory
Admission, Assessment Provenance, Assessment Producer Authorization, Governed
Input Projection y Governed Projection Consumption. Ninguna de esas unidades
constituye Sprint 7.12.

PR #93 integró G0/G1 de Candidate Content Identity; PR #123 integró su G2 y
PR #126 integró Content Identity Propagation & Binding G2. Más adelante, PR #140
integró Episodic Persistence Readiness G2B y PR #146 integró G2P-B —
Authorization Request Composition. Estas dos últimas fronteras permanecen
aisladas: readiness/request composition != authorization decision/enforcement !=
durable write.

PR #97–#99 preservaron y diseñaron la dirección de Evidence-Bound Cognition y
Progressive Cognitive Assurance. Después del rebaseline y los fixes de auditoría
hasta PR #109, PR #110 implementó G2A en aislamiento, PR #111 integró G0/G1 del
Assurance Signal Authority Boundary, PR #118 integró G2 en aislamiento y PR #120
agregó el Evidence Map externo al Research Horizon sin autorizar implementación
adicional.

Actualmente:

```text
LAST COMPLETED NUMBERED SPRINT
Sprint 7.11 — Reproducible Validation Pipeline Foundation

LAST CONVERSATIONAL/RUNTIME SPRINT
Sprint 7.10 — Conversation Session Isolation Foundation

LATEST INTEGRATED CODE UNIT
E5-B1 — Read-only Explorer

ENGINEERING INTELLIGENCE
E0 INTEGRATED
E1 INTEGRATED
E2 INTEGRATED
E3 INTEGRATED
E4 INTEGRATED
E5-A COMMAND SURFACE INTEGRATED
E5-B1 READ-ONLY EXPLORER INTEGRATED
E5-B2/B3 DEFERRED

LATEST PRE-E0/E4 CODE FOUNDATION
Assurance Signal Authority & Projection Foundation — G2

LATEST MEMORY CODE UNIT
G2P-B — Episodic Persistence Authorization Request Composition — INTEGRATED / ISOLATED

LATEST COGNITIVE ASSURANCE UNIT
Assurance Signal Boundary G2 — INTEGRATED / ISOLATED

ACTIVE AUTHORIZED SPRINT
NONE

SUBSEQUENT SPRINT
NONE AUTHORIZED

SIGNAL BOUNDARY G2
INTEGRATED / ISOLATED

CONVERSATION G2B
BLOCKED / NOT AUTHORIZED

CANDIDATE CONTENT IDENTITY G2
INTEGRATED — PR #123

CONTENT IDENTITY PROPAGATION & BINDING G2
INTEGRATED — PR #126

EPISODIC PERSISTENCE READINESS G2B
INTEGRATED / ISOLATED — PR #140

PERSISTENCE AUTHORIZATION REQUEST COMPOSITION G2P-B
INTEGRATED / ISOLATED — PR #146

PERSISTENCE AUTHORIZATION DECISION / ENFORCEMENT
NOT AUTHORIZED

PROTECTED DURABLE WRITE
NOT AUTHORIZED

PERSISTENT MEMORY
NOT AUTHORIZED

RDD STAGE 2
ADOPTED / ACTIVE — proportional applicability
```

La fuente derivada canónica para planificación es:

```text
docs/project/implementation_roadmap.md
```

Ese roadmap se reconcilia en el mismo corrective packet contra este baseline.

La ficha operativa del último sprint numerado integrado es:

```text
docs/project/sprints/SPRINT-7.11.md
```

Las ideas registradas en `documents/projects/jarvis/ideas.md`, las referencias
de `docs/project/concepts/` y las iniciativas reconocidas para planificación
futura pueden informar la implementación únicamente dentro del alcance
autorizado.

El Evidence Map de `MALAK_RESEARCH_HORIZON_MAP.md` incorpora artefactos externos
revisados con roles `CORROBORATION`, `IMPLEMENTATION_INPUT` y `WATCH_SIGNAL`.
Una entrada aplicable debe ser considerada en futura admission review según el
Construction Protocol, pero `implementation input != implementation authorization`.

Se mantiene:

```text
idea != roadmap
roadmap != aprobación
evidencia != autoridad
Projection READY != Admission ELIGIBLE
Consumption EVALUATED != persistence authorization
ELIGIBLE != Stored
Generation != Finalization
G2 READY != G2A ACCEPT
```

`project_context.md` no duplica el roadmap ni concede autoridad.

Agentes, tools, red, navegación, mensajería externa, automatización y otras
rutas operativas de mayor riesgo continúan postergadas salvo autorización
independiente y foundations suficientes.

---

## Capacidades explícitamente postergadas

Hasta que un sprint o unidad aprobada las autorice, no se deben introducir:

- agentes autónomos;
- ejecución libre de herramientas externas;
- control autónomo del sistema operativo;
- navegación externa;
- comunicaciones externas automáticas;
- memoria persistente sensible sin controles aprobados;
- Protected Durable Write sin admission y autorización propias;
- Persistence Authorization decision/enforcement más allá del request composer integrado, sin diseño y autorización propios;
- Conversation Finalization Integration / G2B mientras no exista una admisión
  específica que resuelva producers reales y semántica del historial;
- elevación automática de privilegios;
- acciones destructivas;
- integraciones externas ocultas;
- modificación automática de políticas;
- modificación automática del Kernel;
- autoaprobación de decisiones;
- cambios autónomos sobre Blueprint, Constituciones o Gobernanza.

---

## Restricciones permanentes de trabajo

Todo trabajo futuro debe preservar:

- Kernel First;
- Capability First;
- Runtime Independence;
- Vendor Independence;
- Human in Control;
- Zero Trust interno;
- Defense in Depth;
- denegación por defecto para acciones sensibles;
- mínimo privilegio;
- autorización explícita;
- contratos públicos estables;
- cambios pequeños, trazables y reversibles;
- separación entre autoridad cognitiva y autoridad de seguridad;
- trazabilidad completa.

La metodología vigente combina:

```text
SDD
+ TDD
+ 4R
+ Bounded Correction
+ Independent Validation
```

ADR-003 preserva la dirección de autoridad:

```text
CONTROL / AUTHORITY
Upstream → Downstream

RESULTS / EVENTS / EVIDENCE
Downstream → Upstream
```

La evidencia puede informar una decisión, pero nunca concede autoridad.

ADR-004 establece `Specification & Verification First`: todo cambio
significativo debe definir comportamiento esperado y criterios verificables antes
de ser aceptado en el baseline.

Antes de cualquier modificación importante se deben responder las cuatro
preguntas obligatorias:

1. ¿Respeta el Blueprint?
2. ¿Respeta la Constitución Cognitiva?
3. ¿Respeta la Gobernanza?
4. ¿Preserva o reduce la complejidad del Kernel?

Si alguna respuesta es negativa, dudosa o carece de evidencia suficiente, el
trabajo debe detenerse antes de editar.

---

## Artefactos protegidos

No modificar sin autorización explícita y proceso de gobernanza aplicable:

- Kernel;
- contratos centrales;
- Blueprint;
- Constitución Cognitiva;
- Constitución de Gobernanza;
- políticas de seguridad;
- ADR aceptados;
- fundamentos de seguridad;
- snapshots históricos;
- metadatos de release.

Ningún agente, runtime, capability o herramienta puede modificar estos artefactos durante operación normal.

---

## Disciplina de sprints

La evolución de Malāk debe mantener una cadena explícita de promoción:

```text
idea o necesidad real
→ evaluación
→ roadmap cuando corresponda
→ specification
→ ADR cuando corresponda
→ alcance aprobado
→ rama temporal
→ TDD / implementación
→ 4R
→ Bounded Correction cuando sea necesaria
→ Independent Validation
→ evidencia
→ Draft Pull Request
→ revisión visual humana
→ promoción humana a Ready for Review
→ autorización humana de merge
→ baseline
```

No todos los cambios requieren un sprint funcional. Una corrección documental
acotada puede ejecutarse como corrective packet independiente cuando el alcance,
la evidencia y la autoridad estén explícitamente delimitados.

Una fase no se considera cerrada hasta que:

- código, cuando aplique;
- tests, cuando apliquen;
- documentación;
- evidencia relevante;
- estado del repositorio

estén reconciliados.

No se debe iniciar el siguiente sprint o unidad funcional hasta evaluar el
baseline resultante y obtener aprobación explícita.

---

## Política de actualización

Este documento fue reconciliado contra el estado material observado hasta la
integración de E2 Structural Evidence Evaluation Pack V0 mediante PR #177 y su
validación post-merge #428:

```text
main@e29d3dc79445506aa9bb4e59a8383524d627db68
active_work_branch@NONE
```

`as_of_commit` identifica el commit de referencia utilizado para reconstruir el
contexto, no una obligación de reescribir el documento ante cada commit
puramente mecánico o documental.

Debe volver a validarse cuando:

- `HEAD` cambie de manera material para el contexto descrito;
- un sprint se formalice, active o cierre;
- una unidad funcional aislada relevante se integre;
- se certifique una nueva release;
- cambie arquitectura o gobernanza;
- cambien resultados de tests relevantes;
- cambie la raíz del repositorio;
- cambie el entorno de desarrollo de forma material;
- se incorpore una nueva frontera de seguridad;

Las actualizaciones deben distinguir claramente entre:

- evidencia verificada del repositorio;
- registros históricos;
- estado derivado;
- contexto de planificación;
- decisiones normativas aprobadas.

Los registros históricos no deben reescribirse para aparentar que describen el
presente.

---

## Declaración de ausencia de autoridad normativa

Este documento no puede:

- aprobar un sprint;
- autorizar una implementación;
- modificar arquitectura;
- cambiar gobernanza;
- redefinir el Kernel;
- modificar contratos;
- certificar una release;
- anular un ADR;
- convertir una propuesta en alcance aprobado;
- conceder permisos;
- ampliar autoridad operativa.

Su único propósito es proporcionar un snapshot de contexto trazable, actualizado y conveniente.


## Reconciliación CURRENT — E3 Governed Evidence Support Assessment V0

Estado reconciliado al baseline `main@7b1fe7621b1dad48cc8508390e2ad78faa3e3004`:

- PR #224 integró `E3 Governed Evidence Support Assessment V0` sobre candidate `ad24d5b6de7a3c3e4dcb5643e5906df8bc8682f6`.
- El merge commit es `7b1fe7621b1dad48cc8508390e2ad78faa3e3004`.
- Validation #686 post-merge terminó PASS en Ubuntu y Windows, incluyendo candidate identity, suite de tests, `compileall` y candidate diff.
- El contrato bounded distingue `SUPPORTED | INSUFFICIENT | INCONCLUSIVE` sin convertir soporte en verdad, hecho verificado, decisión ni autoridad.
- `E008-SG-02` permanece `OPEN`: existe el contrato gobernado de assessment de soporte, pero `semantic_assurance` continúa `NOT_VERIFIED`.
- `support_sufficient` permanece sin wiring y no autorizado por esta unidad.
- `authority_effect = none`.
- RDD Stage 2 permanece `NOT AUTHORIZED`.
- Sprint 7.12 permanece `NOT AUTHORIZED`.

Esta reconciliación es derivada y no autoriza una nueva implementación.


## Reconciliación de evidencia de proceso — PR #224

La cobertura histórica de proceso de PR #224 fue reconciliada contra Construction Protocol §5.5 en `docs/project/status/MALAK-PR224-HISTORICAL-PROCESS-EVIDENCE-RECONCILIATION-20260930.md`.

Disposición: `PARTIALLY_EVIDENCED` exclusivamente para certificabilidad histórica del flujo. Validation #685 candidate-bound y Validation #686 post-merge permanecen verificables; Candidate FULL 4R, independent validation post-GREEN y RDD Stage 1 Candidate Conformance no cuentan con evidencia persistida suficiente para reconstruir PASS. No se infiere fallo funcional ni se crea conformidad retroactiva.

## Reconciliación CURRENT — E3 Assessor Qualification Pack V0.1

Estado material verificado después de integrar PR #230:

```text
baseline integrado        main@ae22f3be23ff1c30093d071c74e86db84c34098e
candidate validado        f65f591cd53c702949012836aace7a2cdd0013d0
candidate tree            18a0eead6b98ec85c17f7450c4bcfc687bedb3e8
merge tree                18a0eead6b98ec85c17f7450c4bcfc687bedb3e8
Validation candidate      #713 / 1730 passed Ubuntu + Windows
Validation post-merge     #714 / 1730 passed Ubuntu + Windows
```

PR #231 corrigió previamente el contrato de qualification a V0.1. PR #230 integró el pack offline resultante: case-set de 18 casos / 19 inputs, runner determinista y tests R01–R33 con Fix Validators adicionales. Candidate FULL 4R, affected independent validation y RDD Stage 1 Candidate Conformance quedaron en PASS antes de la revisión humana y el merge.

La integración no agrega un assessor productivo. No selecciona modelo/provider, no ejecuta red, no modifica runtime, no produce `support_sufficient` y no promueve `semantic_assurance`.

```text
E008-SG-02          OPEN
semantic_assurance  NOT_VERIFIED
support_sufficient  NOT WIRED / NOT AUTHORIZED
authority_effect    none
RDD Stage 2         NOT AUTHORIZED
Sprint 7.12         NOT AUTHORIZED
```

La unidad integrada permite calificar de forma reproducible artifacts de un futuro mecanismo assessor dentro del evaluation pack. Elegir, ejecutar o confiar en un mecanismo real requiere una admisión y gates separados.

Esta sección supersede únicamente el snapshot CURRENT anterior para el estado del Assessor Qualification Pack; los registros históricos de PR #224/#229/#231 permanecen sin reescritura.

## Reconciliación CURRENT — E3 Qualification Consumption / Positive Trust Boundary V0

Estado material reconciliado después de #250 y reconciliación de proceso #251:

```text
main HEAD                                  a05aa5f081971f36c133ac50dc0756f938a26a1a
último baseline material/productivo       e1a1973b7b6cf635337a77e81410ebb873f57bde
candidate funcional validado              1143ce2c7818096c393d2fb0cb2986f48440eb93
post-merge Validation                     #37208582290
positive qualification consumption        INTEGRATED
construction two-PR model                 INTEGRATED / PROCESS ONLY
```

PR #250 cierra la necesidad de una frontera positiva de consumo: un caller ya no puede convertir por sí mismo una qualification `FULL` en ruta `DETERMINISTIC`, mientras que material externo/admitido y ligado exactamente puede ser consumido mediante composition-owned admission, PDP/PEP, READY gobernado, binding exacto y validación temporal.

La integración no selecciona ni ejecuta un support assessor productivo y no demuestra semantic entailment.

Límites CURRENT:

```text
Kernel / Planner wiring            NONE
provider / model wiring            NONE
productive support assessor        NOT SELECTED / NOT AUTHORIZED
support_sufficient                 NOT WIRED / NOT AUTHORIZED
semantic_assurance                 NOT_VERIFIED
E008-SG-02                         OPEN
Protected Finalization wiring      NONE
RDD Stage 2                        NOT AUTHORIZED
Sprint 7.12                        NOT AUTHORIZED
self-modification                  NOT AUTHORIZED
authority_effect                   none
```

La siguiente dirección candidata de planificación es:

```text
E3 Blind Assessor Experiment Boundary V0
```

Su necesidad preliminar deriva de que el case-set de Assessor Qualification contiene inputs y ground truth en el mismo artefacto. Antes de ejecutar un assessor real debe existir una proyección determinista que entregue únicamente el material permitido al mecanismo candidato y preserve ocultos `expected_outcome`, `expected_reason_codes` y cualquier metadata equivalente.

La unidad deberá intentar componerse con primitives existentes:

```text
existing case-set
+ existing Assessor Qualification Pack V0.1
+ existing identity/provenance/digest contracts
+ bounded result artifact
→ blind experiment boundary
```

No justifica por sí misma nuevo model/provider, red, store/registry/database, nueva Capability, Kernel/Planner wiring, `support_sufficient`, semantic truth, Protected Finalization ni RDD Stage 2.

Estado:

```text
Construction Preflight                    NOT EXECUTED FOR NEW UNIT
G0 / admission                            NOT EXECUTED
G1 design                                 NOT EXECUTED
implementation                            NOT AUTHORIZED
RED                                       NOT AUTHORIZED
GREEN                                     NOT AUTHORIZED
Ready / Merge                             OWNER ONLY
authority_effect                          none
```

Esta reconciliación actualiza CURRENT_STATE; no autoriza la unidad candidata.

## Reconciliación CURRENT — E3 Governed Blind Assessor Experiment Harness V0

Estado material reconciliado después de PR #254:

```text
baseline previo                              dfcf41868322abb67a87d704545cd74006db81f7
candidate funcional validado                 49d54b9069c71abb53e203d21a3acad2b1e62dfe
merge                                        c5be9c8463ee599530412bfb890180a03e8557e4
candidate tree / merge tree                  e0421161015f6ee4131a3e8cf6ab6ad4ba91cb6d
candidate Validation                         #803 / run 37249290867 / SUCCESS
post-merge Validation                        #804 / run 37853781224 / SUCCESS
Ubuntu                                       1915/1915 PASS
Windows                                      1915/1915 PASS
Affected Candidate FULL 4R                   PASS
E2E / Integration                            PASS
Independent Validation                       PASS
RDD Stage 1 Candidate Conformance             PASS
authority_effect                              none
```

PR #254 integró `E3 Governed Blind Assessor Experiment Harness V0` y cerró el
hueco de producer gobernado entre el case-set de qualification y el artifact que
consume el Assessor Qualification Pack V0.1.

La cadena material integrada queda:

```text
exact governed case-set
        ↓
closed experiment profile
        ↓
blind candidate-visible projection
        ↓
bounded assessor callable
        ↓
19 bound observations / 13 eligible candidate invocations
        ↓
MALAK-E3-SUPPORT-ASSESSOR-RESULTS/v0.1
        ↓
expected experiment binding verification
        ↓
existing Assessor Qualification Pack V0.1
        ↓
PASS | FAIL | INCONCLUSIVE
```

La validación post-merge #804 terminó SUCCESS sobre el merge exacto y preservó
candidate identity, suite completa, `compileall` y candidate diff validation en
Ubuntu y Windows.

Límites CURRENT preservados:

```text
productive assessor mechanism        NOT SELECTED / NOT AUTHORIZED
real model/provider experiment       NOT AUTHORIZED
network for assessor experiment      NOT AUTHORIZED
runtime producer / adapter           NOT AUTHORIZED
support_sufficient                   NOT WIRED / NOT AUTHORIZED
semantic_assurance                   NOT_VERIFIED
E008-SG-02                           OPEN
Protected Finalization wiring        NONE
RDD Stage 2                          NOT AUTHORIZED
Sprint 7.12                          NOT AUTHORIZED
self-modification                    NOT AUTHORIZED
authority_effect                     none
```

El harness integrado valida infraestructura de experimento y composición
governed; no convierte el resultado de un assessor en semantic truth y no
selecciona ni autoriza un mecanismo productivo.

La siguiente dirección candidata de planificación pasa a ser una admisión
separada para un experimento real de assessor/model/provider, con working name:

```text
E3 Governed Assessor Model/Provider Experiment Admission V0
```

Antes de cualquier ejecución real deberá atravesar Construction Preflight,
G0/G1, Security Horizon Check y decisión humana separada. La unidad candidata
debe preservar, como hard-zero inicial, cambios de Kernel/Planner, authority,
`support_sufficient`, Protected Finalization, self-modification y RDD Stage 2.

Esta sección supersede únicamente el snapshot CURRENT anterior para la próxima
unidad E3; los registros históricos y los estados previos permanecen
preservados. No autoriza Design, RED, GREEN, experimento, Ready, Merge ni
promoción.


## Reconciliación CURRENT — E3 Governed Local Ollama Assessor Experiment V0

Estado reconciliado al baseline integrado `main@0a40aa1143f120f7b5a4b544ea49f4b352254b5a`.

Cadena de construcción integrada:

```text
PR #257  Design — E3 Governed Local Ollama Assessor Experiment V0
          merge 4c3249452d06d3f894f6fb0bc4bfd6bf3be4a788

PR #258  OllamaRuntime Local Trust Boundary Hardening V0
          candidate 61c7c6927ad9457dc6f64e261ab335d420412033
          merge     1706cf8dec221ab47e49f4be96da80ace5083d27
          post-merge Validation #819 SUCCESS

PR #259  Governed Local Ollama Assessor Experiment Adapter V0
          candidate 4bedb40a2d52b1bebad45f796ab9dbf2e5de1663
          merge     0a40aa1143f120f7b5a4b544ea49f4b352254b5a
          candidate Validation #823 SUCCESS
          post-merge Validation #824 SUCCESS
```

El tree del merge de PR #259 coincide exactamente con el tree del candidate
validado:

```text
candidate tree = b14287fa66303c0e4f1c6c62c0af47f08a5dbd8f
merge tree     = b14287fa66303c0e4f1c6c62c0af47f08a5dbd8f
```

Validation #824 ejecutó sobre el merge commit exacto:

```text
Ubuntu   1981/1981 PASS
Windows  1981/1981 PASS
candidate identity PASS
compileall         PASS
candidate diff     PASS
```

PR #259 cerró además, antes del merge:

```text
Candidate FULL 4R                      PASS
Offline Integration / E2E             PASS
Independent PR-B2 Validation           PASS
RDD Stage 1 Candidate Conformance      PASS
BLOCKING / MATERIAL / MINOR findings   0 / 0 / 0
authority_effect                        none
```

Estado material resultante:

- el harness gobernado de assessor ciego permanece integrado;
- `OllamaRuntime` incorpora el hardening local de transport, parsing e identidad
  requerido por el Design;
- el adapter experimental evaluation-side para Ollama local está integrado y
  compone el runtime endurecido, el blind harness y el Qualification Pack
  existentes;
- PR #259 no introdujo delta bajo `src/malak/**`, dependencias, Kernel, Planner,
  Capability ni superficies nuevas de autoridad;
- la ejecución de CI del adapter permanece fake-only y no constituye una
  ejecución de modelo real.

Límites CURRENT preservados:

```text
exact local model for assessor experiment   NOT SELECTED / NOT AUTHORIZED
live Ollama assessor experiment             NOT AUTHORIZED
remote provider / remote assessor network   NOT AUTHORIZED
semantic_assurance                          NOT_VERIFIED
E008-SG-02                                  OPEN
support_sufficient                          NOT WIRED / NOT AUTHORIZED
Protected Finalization                      NOT AUTHORIZED
model promotion                             NOT AUTHORIZED
production admission                        NOT AUTHORIZED
self-modification                           NOT AUTHORIZED
RDD Stage 2                                 NOT AUTHORIZED
Sprint 7.12                                 NOT AUTHORIZED
authority_effect                            none
```

La transición siguiente prevista por el Design no es otra implementación
automática. Sólo puede considerarse mediante una instrucción separada del Owner
que nombre el modelo local exacto para un live experiment. Esa ejecución deberá
preservar los límites ya integrados y no convierte un resultado de qualification
en semantic truth, model promotion, `support_sufficient` ni autoridad.

Esta reconciliación es derivada, no normativa, y no autoriza el live experiment
ni ninguna unidad posterior.

## Reconciliación CURRENT — PR #264 / Ground-Truth Repair V0.2

Estado derivado reconciliado contra
`main@73f3a953a1e49a6eb1fac61978e29af1a8d9cc37`.

PR #262 integró el diseño gobernado del repair. PR #264 integró la
implementación acotada del ground truth reparado después de Ground-Truth Review,
Candidate FULL 4R, Independent Candidate Validation y RDD Stage 1 Candidate
Conformance sobre el candidate exacto.

```text
PR #262 Design                         INTEGRATED
PR #264 candidate                      01c159f989f9c2d845d504b0a847ee58b618f56e
PR #264 merge/main                     73f3a953a1e49a6eb1fac61978e29af1a8d9cc37
candidate → merge content              IDENTICAL / 0 file delta
repaired case-set digest               c76e47c7a788173f5ae137094f0fd0d2bbb1076a799d5b265b6e17a4841cdb77
Ground-Truth Review B                  PASS
Corrected Candidate FULL 4R            PASS
Independent Candidate Revalidation C   PASS
RDD Stage 1 Candidate Conformance      PASS
candidate Validation #842              SUCCESS / 1989 passed Ubuntu + Windows
post-merge Validation #843             SUCCESS / 1989 passed Ubuntu + Windows
authority_effect                       none
```

Disposición CURRENT:

```text
Ground-Truth Repair V0.2 Design         INTEGRATED — PR #262
Ground-Truth Repair V0.2 implementation INTEGRATED — PR #264
old case-set digest                     HISTORICAL / SUPERSEDED FOR NEW QUALIFICATION
independent old ground-truth review     FAIL — HISTORICAL
qualification against old oracle        BLOCKED — HISTORICAL
prior live Run #3                       HISTORICAL EXECUTION EVIDENCE ONLY
historical experimental model           qwen3.5:9b / NOT PROMOTED
repaired case-set digest                c76e47c7a788173f5ae137094f0fd0d2bbb1076a799d5b265b6e17a4841cdb77
repaired case-set                       INTEGRATED / candidate-bound validation PASS
new assessor semantic qualification     NOT YET RE-RUN
new live experiment / rerun             NOT AUTHORIZED
semantic_assurance                      NOT_VERIFIED
E008-SG-02                              OPEN
support_sufficient                      NOT WIRED / NOT AUTHORIZED
Protected Finalization                  NOT AUTHORIZED
model promotion                         NOT AUTHORIZED
production admission                    NOT AUTHORIZED
RDD Stage 2                             NOT AUTHORIZED
authority_effect                        none
```

La ejecución live previa continúa reconocida exclusivamente como Evidence
histórica ligada al corpus viejo. El FAIL independiente del oracle histórico no
se atribuye al assessor ni puede reinterpretarse como un FAIL de qwen3.5:9b.

El corpus reparado sí está ahora integrado en `main`; eso no constituye por sí
mismo una nueva qualification semántica. No se ejecutó ni autorizó un nuevo
assessor experiment durante PR #264.

La próxima transición material posible requiere una nueva instrucción del Owner
que autorice explícitamente el live model experiment / qualification rerun y
delimite el mecanismo candidato aplicable. Esa transición deberá reutilizar el
case-set reparado y los contracts/harness/qualification existentes, sin inferir
`support_sufficient`, promoción, producción, Protected Finalization o RDD Stage 2.

Esta reconciliación es derivada, no normativa y no concede autoridad de
implementación, experimento, Ready, Merge o promoción.

## Reconciliación CURRENT — PR #267 / RDD Stage 2 y Research Horizon

Estado derivado vigente contra `main@02daf578012c662f0686357aa48b25722897c82a`.

```text
main tree                           f5e3788f6990a549238c41a8a946861ddedb5ef6
PR #267 candidate                  48b147e69812f29bd94e9f2df236f9cc357921b2
Independent Stage 2 Validation G   PASS / comment 6100167920
post-merge Validation #853         SUCCESS
Ubuntu / Windows                   2016 passed / 2016 passed
RDD Stage 1                        ADOPTED / ACTIVE
RDD Stage 2                        ADOPTED / ACTIVE — proportional
RDD Stage 3+                       NOT AUTHORIZED
authority_effect                   none
```

Aplicabilidad vigente de Stage 2:

```text
risk 0/1 → NOT_APPLICABLE
risk 2   → OPTIONAL / explicit admission only
risk 3/4 → REQUIRED
```

Los bloques CURRENT anteriores que contienen `RDD Stage 2 = NOT AUTHORIZED`
se conservan como trazabilidad del estado que describían en su momento; esta
sección los supersede para interpretar el estado presente.

El Research Horizon fue revalidado contra este baseline y conserva, sin crear
arquitectura nueva:

- Software Quality Assurance & Engineering Research;
- cobertura de tests, Mutation Testing, Property-Based Testing y métricas de calidad;
- Quality Baseline / Quality Regression / Quality Drift;
- Clean Code como sublínea de mantenibilidad y no como dogma;
- Dream-RSI adaptado sólo como investigación de Governed Counterfactual Replay;
- investigación tipo AutoResearch subordinada a IDEA-002 / IDEA-017;
- Reverse Engineering / Methodology Distillation sobre sistemas públicos o autorizados;
- Cognitive Dataset / cross-model invariants, evaluator awareness y causal/mechanistic interpretability como líneas Research/WATCH;
- ODD en OBSERVE, sin crear un framework ODD dentro de Malāk.

Ninguna de estas líneas autoriza tooling, refactor, nueva Capability, componente,
runtime, agente, persistencia, promoción de conocimiento o self-modification.
