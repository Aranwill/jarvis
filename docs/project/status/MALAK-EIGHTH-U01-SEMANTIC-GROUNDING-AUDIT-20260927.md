---
title: Malāk Eighth U01 — Semantic Grounding Audit
status: proposed
authority: derived_audit
document_role: runtime_followup_audit
language: es
created: 2026-09-27
baseline_commit: 2a2e0407a8472186775fa1ecd17f94f37721636a
run_id: bootstrap-u01-20260927-008
focus_id: U01
focus_label: U01 Core Kernel
runtime_result: inconclusive
audit_disposition: gap_requires_hardening
implementation_authorized: false
architecture_change_authorized: false
runtime_execution_authorized: false
self_modification_authorized: false
authority_effect: none
related:
  - docs/project/sprints/proposals/MALAK-EIGHTH-U01-ADMISSION-REVIEW-20260927.md
  - docs/project/status/MALAK-SEVENTH-U01-UNRESOLVED-CLASSIFICATION-AUDIT-20260927.md
  - docs/project/sprints/proposals/MALAK-U007-F04-F06-E3-EPISTEMIC-CALIBRATION-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
  - docs/architecture/kernel.md
---

# Malāk Eighth U01 — Semantic Grounding Audit

## 1. Propósito

Auditar el resultado del Octavo U01 sin ejecutar nuevamente el runtime, sin
modificar los artifacts locales y sin convertir el resultado del modelo en
autoridad arquitectónica.

Run auditado:

~~~text
run_id:
bootstrap-u01-20260927-008

baseline:
2a2e0407a8472186775fa1ecd17f94f37721636a

focus:
U01 — Core Kernel

runtime:
OllamaRuntime 0.33.3

model:
qwen3.5:9b
~~~

Esta auditoría distingue expresamente:

~~~text
artifact integrity
!= execution correctness
!= structural grounding
!= semantic support
!= architectural truth
!= authority
~~~

## 2. Alcance y límites

Incluido:

- identidad y baseline del run;
- existencia e integridad de artifacts;
- continuidad de Focus U01;
- coherencia del trace y de la disposición terminal;
- relación entre findings y evidence refs declaradas;
- coherencia interna entre findings;
- contraste de A6 con la especificación vigente de Kernel.

Fuera de alcance:

- ejecutar `/self-review`;
- llamar Ollama u otro modelo;
- regenerar artifacts;
- reconstruir un PASS retroactivo;
- modificar Kernel, Planner, CapabilityRegistry o runtime;
- autorizar RED, GREEN, implementación, Ready o merge.

## 3. Baseline y preflight

El preflight local confirmó:

~~~text
repository   D:\Ollama\jarvis
branch       main
HEAD         2a2e0407a8472186775fa1ecd17f94f37721636a
working tree clean
AGENTS.md    readable
~~~

El commit corresponde a:

~~~text
Merge pull request #210 from Aranwill/docs/eighth-u01-admission-20260927
~~~

La auditoría fue ejecutada en modo de sólo lectura.

## 4. Integridad del artifact set

El directorio local contiene exactamente los ocho artifacts esperados:

~~~text
assessment.json
attestation.json
diagnostics.jsonl
evidence.json
manifest.json
outcome.json
runtime_provenance.json
trace.jsonl
~~~

La attestation registra SHA-256 para los siete archivos distintos de la propia
attestation. Cada digest fue recalculado y coincidió exactamente.

Resultado:

~~~text
artifact presence      PASS
attestation integrity  PASS
diagnostics            0 records
trace                   12 ordered events
authority_effect       none
~~~

## 5. Identidad y continuidad de evidencia

~~~text
baseline_commit:
2a2e0407a8472186775fa1ecd17f94f37721636a

focus_id:
U01

focus_complete:
true

evidence_set_digest:
954a5f894ca899664c431724a84e5749e08963e370ca6538707e6d8608bece3f

missing_required_sources:
0

unreadable_required_sources:
0

context_truncated:
false
~~~

Inspect y Analyze conservaron el mismo baseline, `focus_id` y
`evidence_set_digest`.

Resultado:

~~~text
baseline binding       PASS
focus continuity       PASS
required source load   PASS
evidence digest        PASS
~~~

## 6. Resultado operacional preservado

El run produjo:

~~~text
inspection_status       GROUNDED
analysis_status         GROUNDED
proposal_status         NOT_RUN
finding_count           9
classifications         7 ALIGNED + 1 UNRESOLVED + 1 PARTIAL
terminal_disposition    INCONCLUSIVE
~~~

El runner aplicó correctamente su contrato vigente:

~~~text
UNRESOLVED present
-> Propose SKIPPED / precondition_not_met
-> terminal INCONCLUSIVE
~~~

Por tanto:

~~~text
terminal aggregation correctness  PASS
fail-closed behavior               PASS
E4 eligibility enforcement         PASS
~~~

Este PASS operacional no certifica la corrección semántica de los findings.

## 7. Finding E008-SG-01 — contradicción interna A4/A6

### 7.1 A4

A4 declara `ALIGNED`:

~~~text
Architecture maintains single Core Kernel with Capability routing via registry.
~~~

Su rationale reconoce que `EngineeringKernelSet` contiene un diccionario de
instancias pero que esa composición no crea duplicación del Core Kernel.

### 7.2 A6

A6 declara `UNRESOLVED`:

~~~text
Uncertainty exists regarding whether multiple Kernel instances in composition
layer represent compliant specialization or violation of single Core Kernel
principle.
~~~

Las dos conclusiones evalúan materialmente la misma relación actual y no quedan
reconciliadas dentro del análisis.

### 7.3 Evidencia normativa disponible

El Evidence Focus suministró `docs/architecture/kernel.md` como
`APPROVED_SPECIFICATION / normative_subordinate`.

La fuente contiene:

~~~text
KIC-02
Pueden existir múltiples instancias concretas de Kernel en fronteras de
composición de aplicación cuando implementan el mismo contrato de Kernel.

KIC-05
Más de una instancia concreta no implica más de un Core Kernel arquitectónico.
~~~

La implementación observada usa el patrón permitido:

~~~text
one fixed Planner
+ one bounded CapabilityRegistry
+ one Kernel contract
+ shared repository baseline / service / provider configuration
-> application composition instances
~~~

No se observó autoridad, policy, estado durable, lógica de negocio o routing
arquitectónico divergente entre instancias.

### 7.4 Clasificación

~~~text
E008-SG-01
type: SEMANTIC_GROUNDING_GAP
severity: material
classification: FALSE_UNRESOLVED
~~~

A6 no demuestra un defecto del Kernel. Demuestra que el análisis no aplicó una
regla normativa suministrada que resolvía la relación actual.

## 8. Finding E008-SG-02 — claim-to-evidence binding defectuoso

El parser confirmó que todos los IDs declarados existían. La revisión de su
contenido encontró bindings materiales incorrectos o insuficientes.

Ejemplos representativos:

| Finding | Claim del rationale | Ref declarado | Evidencia real |
| --- | --- | --- | --- |
| A3 | `Composition.py R83` demuestra el constructor de Kernel | R83 | `src/malak/services/planner.py:8` |
| A4 | menciona R78 y R42-R43 como soporte | R98 | declaración de un test que instancia `Kernel()` |
| A6 | identifica K78 como Blueprint | K78 | referencia conceptual no normativa del bootstrap |
| A7 | R93 demuestra ausencia de provider/runtime | R93 | declaración de `test_kernel_rejects_empty_request` |
| A9 | R90 demuestra manejo de capability desconocida | R90 | declaración de `test_kernel_returns_response` |

El problema no es una ref inexistente. Es:

~~~text
known evidence id
!= semantically supporting evidence
~~~

Clasificación:

~~~text
E008-SG-02
type: EVIDENCE_BINDING_GAP
severity: material
classification: STRUCTURALLY_VALID_SEMANTICALLY_UNVERIFIED
~~~

## 9. Finding E008-SG-03 — límite real de `GROUNDED`

El contrato vigente asigna `GROUNDED` después de validar:

- JSON y claves exactas;
- límites y enums;
- IDs de evidencia conocidos;
- ausencia de duplicados;
- combinación R+K para clases relacionales;
- baseline, focus y authority envelope.

No ejecuta una verificación determinista de que cada línea citada sostenga el
claim ni una reconciliación semántica entre findings.

Por tanto, en el contrato actual:

~~~text
GROUNDED
-> structurally grounded to a real evidence packet
!= semantic entailment verified
!= cross-finding consistency verified
~~~

Clasificación:

~~~text
E008-SG-03
type: ASSURANCE_LABEL_BOUNDARY
severity: material
classification: CONTRACT_LIMIT_EXPOSED
~~~

## 10. Root cause groups

### SG-CONSISTENCY

El output admite findings materialmente incompatibles sin una disposición de
conflicto explícita.

### SG-BINDING

La validación comprueba identidad de refs pero no soporte semántico del claim.

### SG-ASSURANCE

El término `GROUNDED` puede ser interpretado con mayor fuerza que la garantía
técnica realmente aplicada.

No se observó root cause en:

~~~text
artifact writer
attestation
trace
baseline binding
focus completeness
runtime provenance
terminal mapper
Kernel
Planner
CapabilityRegistry
~~~

## 11. Disposición de auditoría

~~~text
artifact integrity             PASS
execution trace                PASS
focus/baseline continuity      PASS
terminal fail-closed behavior  PASS
semantic finding consistency   FAIL
claim-to-evidence assurance    GAP
current Kernel defect          NOT DEMONSTRATED
overall audit disposition      GAP_REQUIRES_HARDENING
~~~

El resultado original permanece históricamente:

~~~text
INCONCLUSIVE
~~~

No se reescribe como PASS ni como FAIL retroactivo.

## 12. Remediation boundary

Un corrective packet separado puede evaluar controles mínimos para:

1. detectar o exponer contradicciones internas materiales;
2. hacer explícito el binding claim -> evidence;
3. distinguir grounding estructural de assurance semántico;
4. preservar el comportamiento fail-closed;
5. mantener E4 y toda autoridad humana sin ampliación.

No se justifica cambiar:

~~~text
Kernel
Planner
CapabilityRegistry
runtime/provider
governance
architecture authority
~~~

## 13. File Coverage Ledger focalizado

| Path / artifact | Clase | Profundidad | Disposición |
| --- | --- | --- | --- |
| `runtime/internal_interaction/bootstrap-u01-20260927-008/*` | runtime evidence local | FULL / targeted por artifact | HISTORICAL_REFERENCE |
| `docs/project/sprints/proposals/MALAK-EIGHTH-U01-ADMISSION-REVIEW-20260927.md` | admission design | FULL / targeted | HISTORICAL_REFERENCE |
| `docs/project/status/MALAK-SEVENTH-U01-UNRESOLVED-CLASSIFICATION-AUDIT-20260927.md` | derived audit | TARGETED_READ | HISTORICAL_REFERENCE |
| `docs/project/sprints/proposals/MALAK-U007-F04-F06-E3-EPISTEMIC-CALIBRATION-G0-G1-DESIGN.md` | implementation design | TARGETED_READ | HISTORICAL_REFERENCE |
| `docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md` | accepted design | TARGETED_READ | HISTORICAL_REFERENCE |
| `docs/architecture/kernel.md` | approved specification | TARGETED_READ | PROTECTED |
| `src/malak/app/composition.py` | current implementation | FULL_READ | STRUCTURAL_INSPECTION |
| `src/malak/kernel/kernel.py` | current implementation | FULL_READ | STRUCTURAL_INSPECTION |
| `src/malak/kernel/registry.py` | current implementation | FULL_READ | STRUCTURAL_INSPECTION |
| `src/malak/services/planner.py` | current implementation | FULL_READ | STRUCTURAL_INSPECTION |
| `tests/test_kernel.py` | test contract | FULL_READ | STRUCTURAL_INSPECTION |
| `src/malak/capabilities/_engineering_analysis.py` | E3 contract | TARGETED_READ | STRUCTURAL_INSPECTION |
| `src/malak/app/internal_interaction.py` | workflow aggregator | TARGETED_READ | STRUCTURAL_INSPECTION |
| `tests/test_engineering_analyze.py` | test contract | TARGETED_READ | STRUCTURAL_INSPECTION |

El documento rechazado por `AGENTS.md` no fue abierto ni procesado.

## 14. Autoridad

Esta auditoría:

~~~text
does not authorize implementation
does not authorize RED
does not authorize GREEN
does not authorize another runtime execution
does not authorize self-modification
does not authorize Ready or merge
authority_effect: none
~~~
