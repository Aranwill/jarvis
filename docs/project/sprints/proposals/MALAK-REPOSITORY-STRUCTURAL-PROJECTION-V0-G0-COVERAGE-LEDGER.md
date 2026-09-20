---
title: Malāk Repository Structural Projection V0 — G0 File Coverage Ledger
status: gate_pass
authority: operational admission evidence
as_of_date: 2026-09-20
unit_id: MALAK-REPOSITORY-STRUCTURAL-PROJECTION-V0
gate: G0
source_baseline: e14787431f864f74226706ad8655a348ee102d77
language: es
---

# Malāk Repository Structural Projection V0 — G0 File Coverage Ledger

## Resultado

```text
G0 RESULT: PASS
blocking findings: 0
tracked files discovered: 262
tracked files classified: 262
silently omitted files: 0
implementation code touched: 0
```

El árbol Git recursivo del baseline oficial
`e14787431f864f74226706ad8655a348ee102d77` declaró
`truncated: false`.

El archivo expresamente rechazado
`PROJECT - MANIFIESTO MALAK (1).docx` no estaba presente en el baseline.
Si reaparece deberá clasificarse `REJECTED_DO_NOT_READ` y no abrirse.

---

## Inventario por familia

```text
.github/**          2
root/config        18
docs/**           108
documents/**       10
src/**             74
tests/**           50
---------------------
tracked blobs     262
classified blobs  262
silently omitted    0
```

Disposiciones aplicadas:

```text
FULL_READ                    19
TARGETED_READ                21
STRUCTURAL_INSPECTION       126
HISTORICAL_REFERENCE         58
NOT_APPLICABLE_WITH_REASON   38
```

La cobertura exhaustiva se realizó por inventario Git completo, clasificación
por rol y lectura proporcional al riesgo. Ningún archivo quedó fuera por no
coincidir con una búsqueda textual.

---

## Lectura profunda requerida

```text
AGENTS.md
SECURITY.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/kernel.md
docs/architecture/architecture_quality_gates.md
docs/architecture/adr/ADR-003-directional-communication-and-authority-flow.md
docs/architecture/adr/ADR-004-specification-and-verification-first.md
docs/development/engineering_method.md
docs/development/development_checklist.md
docs/development/malak_construction_protocol.md
docs/project/implementation_roadmap.md
docs/project/project_context.md
documents/projects/jarvis/ideas.md
docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
src/malak/infrastructure/repository_reader.py
src/malak/capabilities/_engineering_evidence.py
src/malak/app/composition.py
tests/test_architecture_invariants.py
pyproject.toml
```

---

# Findings de admisión

## RSPV0-G0-01 — E0 ya provee el snapshot exacto requerido

```text
OBSERVED
blocking: no
```

`GitRepositoryReader` ya captura un commit exacto, enumera tracked files y
lee blobs por identidad Git. Working tree, staged y untracked quedan fuera de
la vista.

Disposition:

```text
REUSE E0
DO NOT MODIFY E0
```

## RSPV0-G0-02 — La búsqueda literal no cubre estructura sintáctica

```text
OBSERVED
blocking: no
```

E0 puede localizar texto, pero no expone hechos estructurados sobre:

- módulos Python;
- clases, funciones y métodos;
- imports absolutos o relativos.

El gap es material para Engineering Intelligence porque esas preguntas hoy
requieren inferencia posterior sobre texto.

## RSPV0-G0-03 — AST ya es una técnica aceptada en el baseline

```text
OBSERVED
blocking: no
```

`tests/test_architecture_invariants.py` ya usa `ast` de la standard library
para verificar imports y fronteras arquitectónicas.

La propuesta no introduce parser externo ni una técnica nueva de confianza.

## RSPV0-G0-04 — IDEA-013 ya preserva la dirección correcta

```text
OBSERVED
blocking: no
```

IDEA-013 contempla proyecciones regenerables, hasheadas, versionadas y
source-linked, y pide evaluar primero un Repository Knowledge Map mínimo.

V0 no implementará ese mapa completo. Admitirá solamente una proyección
estructural mínima reutilizable.

## RSPV0-G0-05 — La primitive pertenece a Infrastructure

```text
OBSERVED
blocking: no
```

La responsabilidad propuesta es técnica: derivar hechos sintácticos desde
blobs ya capturados por E0.

No decide arquitectura, policy, autoridad ni estrategia cognitiva.

No requiere cambios en Kernel, Planner, Capability Registry, Conversation,
Knowledge o Security Control Plane.

---

# Security Horizon

| Línea | Resultado |
| --- | --- |
| Prompt & Context Trust | NOT_APPLICABLE — cero prompt/LLM |
| Identity & Delegation | NOT_APPLICABLE |
| Compromise Containment | NOT_APPLICABLE |
| Memory / Knowledge Poisoning | NOT_APPLICABLE |
| AI Supply Chain | ALREADY_COVERED — Python stdlib solamente |
| Data Disclosure | NOT_APPLICABLE — proyección local read-only |
| Resource Governance | REQUIRES_REINFORCEMENT — hard bounds de files/bytes/facts/output |
| Observability / Evidence | ALREADY_COVERED — baseline/path/blob/line binding |
| Human in Control | ALREADY_COVERED — evidence only, authority delta 0 |

No existe `BLOCKING_GAP` para diseñar V0.

---

# Malāk Alignment Matrix

| Fuente | Disposición | Efecto V0 |
| --- | --- | --- |
| Cognitive Constitution | ADOPT | regla/herramienta determinista antes de inferencia probabilística |
| Governance Constitution | ADOPT | read-only, sin nueva autoridad |
| Blueprint | ADAPT | primitive técnica en Infrastructure; Kernel delta 0 |
| Architecture Quality Gates | ADOPT | Kernel First, Capability First, Runtime Independence preservados |
| SECURITY.md | ADOPT | Zero Trust; evidence != authority; hard bounds |
| ADR-003 | ADOPT | downstream produce evidencia, no control upstream |
| ADR-004 | ADOPT | G0/G1 + RED antes de GREEN |
| E0 Repository Read | REUSE | único owner del snapshot y blob identity |
| IDEA-013 | ADAPT | primera proyección mínima; no Knowledge Map completo |
| Research Horizon | ADOPT | instrumentos deterministas antes de cognición adicional |
| baseline tests | REUSE | `ast` ya usado para assurance estructural |

---

# Cierre G0

```text
Repository Structural Projection V0
G0 = PASS

new external dependency     = no
new persistent store        = no
new index/cache             = no
Kernel change               = no
Planner change              = no
Security authority change   = no
write authority             = no
LLM/provider dependency     = no
resource bounds required    = yes
```

Este PASS autoriza únicamente G1 documental.
