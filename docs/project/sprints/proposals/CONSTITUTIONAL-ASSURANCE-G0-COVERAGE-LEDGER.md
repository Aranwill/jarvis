---
title: Constitutional Assurance — G0 File Coverage Ledger
status: gate_pass
authority: evidencia operativa de admisión
as_of_date: 2026-09-08
unit: Objective Architecture Invariants Foundation
gate: G0
source_baseline: 5fa2ae2586aec3498710f6722407e371b3e58d1f
project_vault_baseline: 42a9c29561b856e731303cd563687d366b9b2048
sync_agent_baseline: e77e276b6bb913f0814b990be9ff5ec1c9542693
issue: 68
risk_class: 3
rdd_stage_2_authorized: false
language: es
---

# Constitutional Assurance — G0 File Coverage Ledger

## Estado de autoridad

El propietario autorizó la **admisión G0** de una unidad mínima derivada de:

```text
IDEA-012 — Constitutional Assurance Foundation
```

Esta autorización permite únicamente:

- congelar baseline;
- demostrar cobertura de fuentes;
- revalidar necesidad y encaje arquitectónico;
- seleccionar invariantes objetivas ya verdaderas;
- fijar scope y guardrails para diseño posterior.

No autoriza:

- implementación;
- tests nuevos;
- cambios de producción;
- cambios del Kernel;
- cambios del Security Control Plane;
- RDD Stage 2;
- asignación automática de Sprint;
- merge.

Issue de autoridad y seguimiento:

```text
#68 — Admission: Constitutional Assurance — Objective Architecture Invariants
```

---

# 1. Resultado G0

```text
G0 RESULT: PASS
blocking findings: 0
tracked files discovered: 174
tracked files classified: 174
silently omitted files: 0
production code touched: 0
new tests touched: 0
Kernel touched: 0
Security touched: 0
CI touched: 0
```

Baseline fuente congelado:

```text
Aranwill/jarvis
main
5fa2ae2586aec3498710f6722407e371b3e58d1f
```

Estado downstream observado antes de esta admisión:

```text
Aranwill/malak-project-vault/main
42a9c29561b856e731303cd563687d366b9b2048
merge message: docs(vault): synchronize Malak 5fa2ae25

Aranwill/malak-vault-sync-agent/main
e77e276b6bb913f0814b990be9ff5ec1c9542693
```

La ejecución `run-once` aportada por el operador contra `5fa2ae25` concluyó:

```text
base_commit == head_commit
changed_files = 0
document_candidates = 0
validation_findings = 0
conclusion = pass
proposal_created = false
```

Por tanto no existe drift downstream conocido que bloquee esta admisión.

---

# 2. Inventario exhaustivo del repositorio fuente

Los árboles Git recursivos inspeccionados declararon `truncated: false` por
familia. El conteo de blobs trackeados del baseline es:

```text
root files                         8
.github/**                         2
configs/**                         1
docs/**                           55
documents/**                      10
examples/**                        1
scripts/**                         8
src/**                            55
tests/**                          34
------------------------------------
tracked blobs                    174
classified blobs                 174
silently omitted                  0
```

Cada blob queda cubierto mediante una disposición explícita o un catch-all de
familia. La profundidad de lectura es proporcional a autoridad y relevancia.

El documento rechazado por `AGENTS.md` no aparece entre estos 174 blobs
trackeados. No fue leído, resumido, citado ni procesado.

---

# 3. Disposiciones utilizadas

```text
FULL_READ
TARGETED_READ
STRUCTURAL_INSPECTION
HISTORICAL_REFERENCE
GENERATED_OR_DERIVED
NOT_APPLICABLE_WITH_REASON
```

No se identificaron blobs trackeados que requirieran `PROTECTED` o
`REJECTED_DO_NOT_READ`.

---

# 4. File Coverage Ledger — autoridad y método

## FULL_READ

```text
AGENTS.md
SECURITY.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/architecture_quality_gates.md
docs/architecture/kernel.md
docs/architecture/adr/ADR-002-policy-enforcement-boundary.md
docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md
docs/architecture/adr/ADR-004-specification-and-verification-first.md
docs/development/evidence_manifest.md
docs/development/malak_construction_protocol.md
docs/project/sprints/SPRINT-7.11.md
scripts/malak_evidence.py
tests/test_malak_evidence.py
```

Razón: leyes, límites de Kernel y seguridad, autoridad direccional,
especificación/verificación, Construction Protocol, RDD Stage 1 y último sprint
integrado.

## TARGETED_READ

```text
docs/architecture/blueprint.md
docs/architecture/decisions/decision-index.md
docs/development/engineering_method.md
docs/development/development_checklist.md
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/roadmap.md
documents/projects/jarvis/ideas.md
docs/project/concepts/README.md
docs/project/concepts/GOVERNED_EPHEMERAL_AGENT_EXECUTION_EVIDENCE_REFERENCE.md
docs/project/concepts/GOVERNED_SWARM_LONG_HORIZON_REFERENCE.md
docs/project/concepts/MALAK_COGNITIVE_DATASET_FOUNDATION.md
src/malak/app/cli.py
src/malak/kernel/kernel.py
src/malak/kernel/bootstrap.py
src/malak/security/**
tests/test_kernel.py
tests/test_policy_decision_point.py
tests/test_policy_enforcement_point.py
.github/workflows/validation.yml
pyproject.toml
```

Razón: verificar que las invariantes candidatas describen el baseline real y no
una arquitectura aspiracional.

## STRUCTURAL_INSPECTION

```text
remaining .github/**
configs/**
remaining docs/architecture/**
remaining docs/development/**
remaining docs/governance/**
docs/knowledge/**
docs/operations/**
remaining docs/project/**
remaining documents/projects/jarvis/** excluding archive/releases historical
examples/**
remaining scripts/**
src/app/**
remaining src/malak/**
remaining tests/**
root project files not listed above
```

Resultado estructural relevante:

```text
Kernel has no concrete runtime/provider dependency
Security Control Plane has no runtime/provider/LLM dependency
existing CI already executes the complete pytest suite
RDD Stage 1 already enforces evidence authority_effect = none
```

## HISTORICAL_REFERENCE

```text
docs/project/sprints/SPRINT-7.0.md ... SPRINT-7.10.md
docs/project/sprints/proposals/RDD-M1-*.md
docs/project/sprints/proposals/SPRINT-7.11-*.md
docs/project/sprints/proposals/SPRINT-7.3-SECOND-CAPABILITY-DRAFT.md
documents/projects/jarvis/archive/**
documents/projects/jarvis/releases/**
```

Estas fuentes sirven como precedente y trazabilidad, no desplazan el estado del
baseline actual.

## GENERATED_OR_DERIVED

```text
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/roadmap.md
ROADMAP.md
```

Cuando también figuran en `TARGETED_READ`, prevalece esa profundidad. Esta
clasificación registra solamente su autoridad derivada.

## NOT_APPLICABLE_WITH_REASON

```text
configs/**
examples/**
```

No participan en las invariantes seleccionadas y no justifican modificación.

---

# 5. Revalidación de IDEA-012

IDEA-012 conserva una intención válida:

```text
principios arquitectónicos/constitucionales objetivos
→ invariantes verificables
```

pero su Foundation completa no se adopta como una unidad monolítica.

Disposición:

```text
IDEA-012 = ADAPT
```

Razón:

- solo deben automatizarse invariantes objetivas y deterministas;
- tests no sustituyen interpretación constitucional humana;
- el baseline actual ya posee CI reproducible para ejecutar tests nuevos;
- no existe necesidad de un Constitutional Engine runtime para este paso;
- no existe necesidad de nuevas dependencias, servicios o contratos.

La unidad candidata queda reducida a un conjunto mínimo de invariantes ya
demostrables.

---

# 6. Invariantes seleccionadas

## CA-I1 — Kernel Concrete Execution Isolation

### Regla admitida

`src/malak/kernel/**` no debe adquirir dependencia directa hacia implementaciones
concretas de ejecución conversacional o inferencia.

Fronteras concretas seleccionadas para eventual verificación:

```text
forbidden direct imports from src/malak/kernel/**:
- malak.runtime.*
- malak.providers.*
- malak.services.conversation_service
```

### Evidencia de baseline

`Kernel` actualmente depende de:

```text
malak.core.request
malak.core.response
malak.kernel.bootstrap
malak.kernel.registry
malak.services.planner
```

`bootstrap.py` registra la Capability determinista `EchoCapability` y no
construye runtime/provider/conversation service.

La invariante es deliberadamente **estrecha**. No intenta convertir cualquier
posible dependencia futura de políticas o contratos en una prohibición global.

Resultado:

```text
baseline satisfies invariant = YES
candidate disposition = ADOPT
```

---

## CA-I2 — Security Runtime/Provider Independence

### Regla admitida

El Security Control Plane debe permanecer independiente de implementaciones de
inferencia y providers concretos.

Fronteras concretas seleccionadas para eventual verificación:

```text
forbidden direct imports from src/malak/security/**:
- malak.runtime.*
- malak.providers.*
- malak.core.llm_runtime
```

La regla no cambia PDP, PEP, `SecurityContext`, contratos, lifecycle ni
comportamiento de autorización.

Resultado:

```text
baseline satisfies invariant = YES
candidate disposition = ADOPT
```

---

## CA-I3 — Evidence Carries Zero Authority

### Regla

RDD Stage 1 ya define y ejecuta:

```text
RESULTS = PASS | FAIL | INCONCLUSIVE
authority_effect = none
```

El helper rechaza cualquier otro `authority_effect`, y los tests actuales ya
cubren explícitamente que `approved` y campos de authority/delivery agregados son
inválidos.

Resultado:

```text
baseline satisfies invariant = YES
existing deterministic proof = YES
new duplicate test justified = NO
candidate disposition = ADOPT EXISTING EVIDENCE
```

G1 no deberá duplicar esta cobertura salvo que encuentre un gap objetivo.

---

# 7. Alternativas rechazadas en G0

## Automatizar la Constitución completa

```text
REJECT
```

La ley contiene principios que requieren juicio contextual. Convertirlos en
checks mecánicos sería falsa precisión y podría transferir interpretación a una
herramienta.

## Crear Constitutional Engine runtime ahora

```text
REJECT
```

No existe necesidad actual demostrada. Ampliaría arquitectura, autoridad y
superficie de riesgo sin aportar valor para las tres invariantes seleccionadas.

## Integrar PEP/SecurityContext en la ruta conversacional

```text
OBSERVE
```

La foundation de seguridad existe, pero esta unidad no introduce operaciones
protegidas, tools ni efectos externos. Mezclar enforcement funcional con
assurance estructural violaría scope mínimo.

## RDD Stage 2

```text
OBSERVE
```

No es necesario para demostrar invariantes y continúa sin autorización.

## Agentes / sandbox / swarm / self-development

```text
OBSERVE
```

Aumentarían complejidad antes de demostrar necesidad operacional.

---

# 8. Findings G0

## CA-G0-F001 — evitar una prohibición de seguridad demasiado amplia en Kernel

Estado:

```text
RESOLVED BY NARROW SCOPE
```

Una regla genérica `Kernel must never import malak.security` sería más fuerte que
la evidencia necesaria y podría bloquear una futura integración legítima mediante
contratos/policies autorizados por Blueprint.

CA-I1 se limita a dependencias concretas de ejecución que hoy son objetivamente
incompatibles con Runtime Independence y la frontera de Capability.

## CA-G0-F002 — CA-I3 ya posee cobertura determinista

Estado:

```text
RESOLVED BY REUSE
```

Crear otra prueba para `authority_effect = none` duplicaría RDD Stage 1 y
contradiría minimización cognitiva/ingeniería proporcional.

G1 deberá referenciar los tests existentes en vez de copiarlos.

## CA-G0-F003 — no modificar CI para incorporar invariantes

Estado:

```text
RESOLVED BY EXISTING PIPELINE
```

Sprint 7.11 ya ejecuta `python -m pytest -q` sobre cada candidato. Un eventual
módulo de tests de arquitectura quedaría cubierto automáticamente.

No existe necesidad demostrada de modificar `.github/workflows/validation.yml`.

---

# 9. Cuatro preguntas obligatorias

```text
1. ¿Respeta el Blueprint?
   PASS
   → protege Runtime Independence, Capability First y límites ya vigentes.

2. ¿Respeta la Constitución Cognitiva?
   PASS
   → evidencia antes de acción, trazabilidad, proporcionalidad y minimización.

3. ¿Respeta Gobernanza?
   PASS
   → los checks producen evidencia; no approval ni authority.

4. ¿Preserva/reduce complejidad del Kernel?
   PASS
   → planned Kernel delta = 0.
```

---

# 10. Riesgo

```text
risk_class = LEVEL 3 / HIGH
FULL 4R required at closure if implementation is later authorized
```

Motivo:

- se protegen límites del Kernel;
- se protege independencia del Security Control Plane;
- se preserva una invariante de autoridad.

El tamaño esperado del cambio no reduce la categoría conceptual del riesgo.

---

# 11. Scope admitido para G1 design

G0 admite **diseñar**, no implementar todavía, una solución mínima capaz de
verificar CA-I1 y CA-I2.

Restricciones de diseño:

```text
expected production delta       = 0
expected Kernel delta           = 0
expected Security behavior delta= 0
expected runtime delta          = 0
expected authority delta        = 0
expected public contract delta  = 0
expected dependencies added     = 0
expected CI workflow delta      = 0
```

Preferencia preliminar a validar en G1:

```text
one focused architecture test module
Python standard library only
structural import inspection
existing pytest pipeline
reuse existing CA-I3/RDD tests
```

La ubicación exacta, forma del test y criterios RED/GREEN pertenecen a G1 y no
quedan aprobados por este documento.

---

# 12. Fuera de alcance

```text
src/malak/** modifications
Kernel changes
Security changes
Conversation changes
new runtime/provider behavior
new public contracts
new dependencies
CI workflow changes
Constitutional Engine runtime
full constitutional interpretation
Memory / Knowledge / RAG
tools / external execution
agents / sandbox / swarm
RDD Stage 2 / receipts
auto-fix / auto-approval / auto-merge / auto-deploy
branch protection / delivery enforcement
refactors unrelated to the selected invariants
```

---

# 13. Decisión G0

No se detectó conflicto normativo, drift downstream bloqueante ni necesidad de
ampliar arquitectura para proteger las invariantes seleccionadas.

```text
G0 = PASS
IDEA-012 = ADAPT
CA-I1 = ADOPT
CA-I2 = ADOPT
CA-I3 = ADOPT EXISTING EVIDENCE
next = G1 design
implementation_authorization = PENDING HUMAN AUTHORITY
Sprint assignment = NONE
RDD Stage 2 = NOT AUTHORIZED
merge authority = HUMAN-ONLY
```
