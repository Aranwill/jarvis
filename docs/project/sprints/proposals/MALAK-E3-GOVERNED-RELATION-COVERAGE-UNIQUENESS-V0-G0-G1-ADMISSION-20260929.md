---
title: Malāk E3 — Governed Relation Coverage & Uniqueness V0 — G0/G1 Admission
status: design_candidate
authority: non-normative
language: es
as_of_date: 2026-09-29
baseline_commit: de0427d32a6ee2642ad70a6ed410a0288982bfa6
g0: PASS
g1: PASS
critical_contract_hardening: PASS
four_law_questions: PASS
design_4r: PASS
rdd_stage_1_design_check: PASS
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
self_modification_authorized: false
authority_effect: none
---

# Malāk E3 — Governed Relation Coverage & Uniqueness V0

## 1. Propósito

Evaluar y congelar el siguiente gate mínimo posterior a PR #215 para endurecer
el conjunto de findings de E3 cuando existe un catálogo gobernado de relaciones.

Esta unidad no introduce un verificador semántico, no ejecuta Runtime
Self-Review y no afirma que una cita sostenga semánticamente un claim.

El objetivo V0 es más estrecho:

```text
governed relation catalog
        ↓
E3 focused analysis
        ↓
exactly one finding per governed relation
        ↓
no omissions
no duplicate relation evaluations
stable catalog-order projection
```

## 2. Baseline exacto

```text
repository  Aranwill/jarvis
branch      main
baseline    de0427d32a6ee2642ad70a6ed410a0288982bfa6
PR #215     integrated
PR #216     CURRENT_STATE reconciliation integrated
Validation #662 post-merge PASS
authority_effect none
```

El último sprint numerado integrado continúa siendo Sprint 7.11. Esta unidad no
crea ni autoriza Sprint 7.12.

## 3. Trigger material

El audit histórico del Octavo U01 identificó:

```text
E008-SG-01  SEMANTIC_GROUNDING_GAP
            FALSE_UNRESOLVED / conflicting treatment of one material relation

E008-SG-02  EVIDENCE_BINDING_GAP
            known evidence id != semantically supporting evidence

E008-SG-03  ASSURANCE_LABEL_BOUNDARY
            GROUNDED != semantic entailment verified
```

PR #212 creó identidad gobernada de relación. PR #215 hizo que E3 consuma
`relation_id` únicamente para focuses con catálogo no vacío y rechace IDs fuera
del catálogo.

El parser vigente todavía acepta, para un catálogo gobernado:

```text
subset of catalog relations
duplicate findings with the same governed relation_id
arbitrary finding order
```

Por tanto:

```text
relation membership validation
!= relation set completeness
!= relation uniqueness
!= semantic entailment
```

Este es el trigger actual de esta admisión.

## 4. G0 — disposición

```text
disposition: ADOPT
scope: E3 focused governed relation set integrity only
need: demonstrated by current parser contract + E008-SG-01 lineage
new architecture: no
new capability: no
new runtime/provider: no
new authority: no
runtime execution: no
```

No existe necesidad demostrada de un manager, registry, semantic reviewer,
segundo modelo, agente, servicio o dependencia nueva.

## 5. G1 — contrato candidato

Para `EngineeringAnalyzeCapability` con un
`GovernedEngineeringEvidenceFocus` cuyo `governed_relations` sea no vacío:

1. el catálogo efectivo continúa ligado al `evidence_set_digest`;
2. `relation_id` continúa limitado al enum exacto del catálogo;
3. el número de findings debe ser exactamente igual al número de relaciones;
4. cada `relation_id` gobernado debe aparecer exactamente una vez;
5. una relación omitida falla cerrado;
6. una relación duplicada falla cerrado;
7. un ID desconocido continúa fallando cerrado;
8. después de validar cobertura exacta, los findings se proyectan en el orden
   declarado por el catálogo para estabilizar `A1..An`;
9. un catálogo cuyo tamaño exceda la capacidad máxima de findings de E3 falla
   antes de aceptar una respuesta de modelo;
10. catálogo vacío conserva exactamente el contrato genérico vigente.

La postcondición candidata es:

```text
focused governed catalog != empty

set(finding.relation_id) == set(catalog.relation_id)
count(findings) == count(catalog)
count(each relation_id) == 1

then:
analysis.findings order == catalog order
```

## 6. Límites semánticos

Este gate **NO** demuestra:

```text
evidence ref semantically supports claim
finding classification is true
two different relation_ids can never overlap semantically
GROUNDED == semantic entailment verified
relation identity == authority
```

En particular:

```text
E008-SG-02 remains OPEN / OUT OF SCOPE
E008-SG-03 remains an explicit assurance boundary
```

El gate sólo reduce una clase determinista de inconsistencia ligada a
E008-SG-01: múltiples disposiciones para una misma relación gobernada o
relaciones gobernadas omitidas.

## 7. Impacto E3 / E4 / internal interaction

### E3 focalizado con catálogo

Cambio candidato:

```text
membership only
→ exact coverage + uniqueness + canonical order
```

### E3 genérico / catálogo vacío

```text
NO CHANGE
```

### E4

E4 usa el parser compartido con `allowed_relation_ids=()` y su schema legado.

```text
E4 relation-aware behavior       NO
E4 proposal eligibility          NO CHANGE
E4 authorization semantics       NO CHANGE
```

### Internal Interaction

El encabezado legado:

```text
[A#] classification=<...>
```

debe preservarse. La canonización del orden puede estabilizar los refs `A#`,
pero no modifica la autoridad del terminal mapper.

## 8. Critical Contract Hardening

```text
contract owner            EngineeringAnalyze focused relation path
catalog source            GovernedEngineeringEvidenceFocus.governed_relations
catalog identity          evidence_set_digest-bound
empty catalog             legacy behavior
non-empty catalog         exact coverage required
unknown relation          reject
missing relation          reject
duplicate relation        reject
catalog > E3 max findings reject before grounded result
output order              canonical catalog order
classification enum       unchanged
evidence refs             unchanged
authority_effect          none
```

Fail-closed matrix:

| Caso | Disposición |
|---|---|
| catálogo vacío | comportamiento vigente |
| catálogo con 2 relaciones / 1 finding | rechazo |
| catálogo con 2 relaciones / 2 findings mismo ID | rechazo |
| catálogo con 2 relaciones / un ID desconocido | rechazo |
| catálogo con cobertura completa en orden inverso | aceptar + canonizar |
| catálogo mayor al límite E3 | rechazo |
| U04 / RR-03 actuales | sin cambio |

Resultado:

```text
Critical Contract Hardening: PASS
```

## 9. Cuatro preguntas de ley

### Blueprint

No cambia Kernel, Planner, CapabilityRegistry ni composición arquitectónica.
Endurece una Capability existente.

```text
PASS
```

### Constitución Cognitiva

Refuerza CC-003, CC-004, CC-005, CC-006, CC-008 y CC-012 mediante una regla
determinista mínima que impide omitir o duplicar relaciones gobernadas.

No presenta el resultado como verdad semántica.

```text
PASS
```

### Gobernanza

No agrega acciones externas, writes, autoridad o auto-promoción. El Owner
conserva Ready/Merge y cualquier ejecución Runtime Self-Review requiere gate
separado.

```text
PASS
```

### Complejidad / Kernel

No toca Kernel y reutiliza el catálogo, schema y parser existentes.

```text
PASS
```

## 10. Malāk Alignment Matrix

| Fuente / principio | Relación con el candidato | Disposición |
|---|---|---|
| Cognitive Constitution | evidencia, coherencia, contradicciones expuestas, proporcionalidad | ADOPT |
| Governance Constitution | Human in Control, separación de responsabilidades | ADOPT |
| Blueprint | Capability First / Kernel First preservados | ADOPT |
| Architecture Quality Gates | sin nuevo componente ni autoridad; trazabilidad obligatoria | ADOPT |
| SECURITY.md | fail-closed y mínimo privilegio; no abre nueva superficie sensible | ADOPT |
| CURRENT_STATE | PR #215 creó el trigger concreto | ADOPT |
| Eighth U01 Semantic Grounding Audit | E008-SG-01 aporta causa material | ADAPT |
| Evidence-Bound Cognition Foundation | CAL-003/CAL-006 corroboran intención; concepto no es autoridad | ADAPT |
| Research Horizon Map | no exige nueva superficie; RDD Stage 2 sigue fuera | OBSERVE |
| ideas.md | no se detectó una dependencia necesaria para este gate | OBSERVE |
| Structural Evidence E2 | no requerido para coverage/uniqueness | OBSERVE |
| E008-SG-02 semantic evidence binding | problema real pero distinto | DEFER |
| E008-SG-03 assurance label boundary | se preserva explícito; no se sobredeclara | DEFER |

## 11. Security Horizon Check

No se introduce:

```text
Memory persistente
retrieval
agents
tools
network
sandbox
external execution
sensitive data flow
delegation
new authorization
```

Los controles aplicables ya existen en la frontera actual:

```text
Prompt & Context Trust Boundary   ALREADY_COVERED
Resource Governance              ALREADY_COVERED
Human in Control                 ALREADY_COVERED
fail-closed parsing              ALREADY_COVERED
AI supply-chain new exposure     NOT_APPLICABLE
Agent delegation                 NOT_APPLICABLE
Data disclosure new surface      NOT_APPLICABLE
```

Resultado:

```text
Security Horizon Check: PASS
blocking security gap: none
```

## 12. Design 4R

### Risk

Reduce aceptación de outputs incompletos/duplicados. No eleva autoridad.

```text
PASS
```

### Readability

La regla es expresable como igualdad de conjuntos + unicidad + orden canónico,
sin introducir abstracciones nuevas.

```text
PASS
```

### Reliability

Las mismas relaciones gobernadas producen el mismo orden de findings aceptados.
Omisiones y duplicados fallan cerrado.

```text
PASS
```

### Resilience

Model output incompleto, repetido o fuera del catálogo no puede degradarse
silenciosamente a un resultado `GROUNDED`.

```text
PASS
```

Resultado:

```text
Design 4R: PASS
```

## 13. RDD Stage 1 Design Check

```text
baseline exact                    PASS
problem evidence                  PASS
scope frozen                      PASS
candidate contract explicit       PASS
failure semantics explicit        PASS
authority_effect none             PASS
RDD Stage 2 effects               NONE
```

Resultado:

```text
RDD Stage 1 Design Check: PASS
```

Esto no constituye Candidate Conformance.

## 14. RED candidato — NO AUTORIZADO

Cuando exista autorización separada, el RED mínimo deberá demostrar causalmente:

```text
R01 missing governed relation fails closed
R02 duplicate governed relation fails closed
R03 complete coverage is accepted
R04 complete out-of-order coverage is canonized to catalog order
R05 catalog beyond E3 finding capacity fails closed
R06 empty catalog preserves existing generic E3 contract
R07 E4 legacy relation-less analysis remains unchanged
```

Los tests existentes de PR #215 continúan cubriendo catálogo en packet, schema
allowlist, aceptación de ID conocido y rechazo de ID desconocido.

## 15. Scope candidato futuro

Producción, si RED es autorizado:

```text
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/engineering_analyze.py
```

Tests previstos:

```text
tests/test_e3_governed_relation_coverage_uniqueness_v0.py
tests/test_engineering_propose.py            only if compatibility requires it
tests/test_internal_interaction_test_v0_harness.py only if compatibility requires it
```

No modificar:

```text
Kernel
Planner
CapabilityRegistry
Memory
SecurityContext
runtime/provider
Governance Constitution
Cognitive Constitution
Blueprint
E4 eligibility
Structural Evidence
Structural Delta
persistence
```

## 16. Correction Budget candidato

Si se autoriza implementación:

```text
bounded correction budget: max 2 rounds
scope expansion: prohibited
new material requirement: STOP → separate gate
```

## 17. File Coverage

La admission review comenzó por inventario recursivo del baseline:

```text
tracked files discovered = 329
tracked files classified = 329
silently omitted files   = 0
```

El ledger completo se preserva en:

```text
MALAK-E3-GOVERNED-RELATION-COVERAGE-UNIQUENESS-V0-FILE-COVERAGE.tsv
```

El documento rechazado por AGENTS.md no aparece entre los 329 blobs trackeados
del baseline actual. No fue abierto, buscado por contenido ni utilizado como
evidencia. Si reaparece en un baseline futuro, deberá clasificarse
`REJECTED_DO_NOT_READ`.

## 18. Disposición

```text
G0                               PASS
G1                               PASS
Critical Contract Hardening      PASS
Four Questions                   PASS
Malāk Alignment Matrix           PASS
Security Horizon Check           PASS
Design 4R                        PASS
RDD Stage 1 Design Check         PASS

RED                              NOT AUTHORIZED
GREEN                            NOT AUTHORIZED
Runtime Self-Review              NOT AUTHORIZED
RDD Stage 2                      NOT AUTHORIZED
Ready / Merge                    OWNER ONLY
authority_effect                 none
```

## 19. Siguiente transición lícita

```text
Owner reviews this admission/design
        ↓
explicit RED authorization
        ↓
materialize causal RED only
```

No se debe ejecutar otro Runtime Self-Review para validar este diseño.
