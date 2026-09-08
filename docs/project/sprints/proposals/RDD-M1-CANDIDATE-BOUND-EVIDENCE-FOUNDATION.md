---
title: RDD-M1 — Candidate-Bound Evidence Foundation
status: autorizado_para_stage_1
authority: documentación operativa de admisión
as_of_date: 2026-09-08
baseline_commit: e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0
branch: feat/rdd-m1-evidence-foundation
unit_id: RDD-M1
rdd_stage_from: 0
rdd_stage_to: 1
stage_2_authorized: false
language: es
---

# RDD-M1 — Candidate-Bound Evidence Foundation

## Estado y autorización

```text
Stage 0 → Stage 1
G0–G6 autorizados
Stage 2 NO autorizado
```

El propietario autorizó el 2026-09-08 incorporar la lógica madura de RDD al
método propio de Malāk sin copiar infraestructura externa.

La intención es:

```text
reutilizar método existente
→ estructurar evidencia candidate-bound
→ validar de forma determinista
→ medir utilidad
→ decidir después si Stage 2 merece admisión
```

---

## Necesidad comprobada

Malāk ya define:

- Candidate Identity;
- riesgo 0–4 y 4R proporcional;
- `Writer != Reviewer != Validator != Authority`;
- Bounded Correction y Correction Budget;
- validación independiente;
- `PASS | FAIL | INCONCLUSIVE`;
- gates, findings y trazabilidad.

El gap es únicamente de representación:

```text
evidencia existente
+
candidate identity existente

→ falta un artefacto estructurado mínimo
  que demuestre a qué candidato corresponde la evidencia
```

RDD-M1 cubre solo ese gap mediante `MALAK-EVIDENCE-MANIFEST/v1` y tooling de
desarrollo read-only.

---

## Invariantes no negociables

### I1 — Authority flows downward only

```text
CONTROL / AUTHORITY / PERMISSIONS / COMMANDS
                    ↓
```

La autoridad solo fluye desde upstream hacia downstream por contratos y permisos
previamente concedidos.

### I2 — No self-escalation

Ningún helper, validator, reviewer, manifest, agente o componente downstream
puede elevar, modificar, renovar, reinterpretar o ampliar su propia autoridad o
scope.

```text
self-escalation possible
→ DESIGN INVALID
→ STOP
```

### I3 — Upward information carries zero authority

```text
RESULTS / FINDINGS / METRICS / EVIDENCE
                    ↑
```

El retorno ascendente es información, nunca poder de decisión.

```text
Evidence != Receipt != Validation != Decision != Authority
```

### I4 — Candidate-bound traceability

```text
candidate changes
→ identity changes
→ previous evidence does not certify the new candidate
→ affected evidence must be revalidated
```

### I5 — External auditability

Un auditor independiente debe poder reconstruir desde artefactos preservados:

```text
baseline
→ scope
→ candidate
→ validations / 4R
→ findings
→ correction cuando exista
→ new candidate cuando exista
→ terminal result
→ human decision separada
```

La reconstrucción no puede depender de memoria conversacional, chain-of-thought,
la misma terminal, modelo o proveedor.

### I6 — Auditability != premature infrastructure

Auditabilidad no autoriza PKI, firmas, Merkle, hash chaining, databases, stores de
autoridad, attestation ni lifecycle engines.

---

## Cuatro preguntas obligatorias

| Pregunta | Resultado | Condición |
|---|---|---|
| ¿Respeta el Blueprint? | PASS | tooling fuera del runtime; ADR-003 preservada |
| ¿Respeta la Constitución Cognitiva? | PASS | no participa en cognición, Memory ni Knowledge |
| ¿Respeta Gobernanza? | PASS | evidencia sin autoridad; mínimo privilegio y separación |
| ¿Mantiene simple el Kernel? | PASS | `Kernel delta = 0` |

---

## Reutilización y componentes

RDD-M1 reutiliza los mecanismos ya definidos por Malāk; no crea otro sistema de
review, autorización o corrección.

No se justifican y no deben aparecer:

```text
RDDService
RDDManager
CandidateManager
ReviewEngine
ReceiptStore
ValidationService
EvidenceRegistry
AuthorityStore
ReviewOrchestrator
```

Stage 1 puede añadir únicamente:

```text
1 contrato de desarrollo
1 helper determinista read-only
1 módulo de tests focalizados
1 manifest piloto histórico
```

Objetivos permanentes:

```text
new architectural components = 0
new runtime components = 0
new dependencies = 0
Kernel delta = 0
runtime delta = 0
authority effects = 0
```

---

## Alcance autorizado

### IN SCOPE

- `MALAK-EVIDENCE-MANIFEST/v1`;
- binding por Git commit;
- baseline/candidate existence y ancestry;
- validación estructural estricta;
- `PASS | FAIL | INCONCLUSIVE`;
- 4R proporcional;
- finding references y correction round;
- provenance mínima de producer/validator;
- stale candidate detection;
- external reconstruction;
- tests y dogfood;
- medición de overhead.

### OUT OF SCOPE

```text
Kernel / Planner / capabilities
Conversation / Memory / Knowledge
Security Control Plane / PDP / PEP
runtimes / providers
agents / autonomous review / autonomous correction
database / registry / receipt store / authority store
PKI / signatures / Merkle / hash chaining / CAS
provider bindings / lifecycle engine
auto-merge / delivery enforcement / branch protection
Stage 2 receipts
```

---

## Ubicaciones aprobadas

No se crea una nueva familia `docs/project/evidence/**`.

```text
contract
  docs/development/evidence_manifest.md

helper
  scripts/malak_evidence.py

tests
  tests/test_malak_evidence.py

pilot manifest
  docs/project/sprints/proposals/RDD-M1-EVIDENCE-MANIFEST.json
```

Estas familias ya son observadas por el Sync Agent, por lo que RDD-M1 no requiere
modificar mappings downstream.

---

## Gates

```text
G0 Admission & Baseline Review
   ↓
G1 Evidence Contract v1
   ↓
G2 Candidate Identity Binding
   ↓
G3 Manifest Validation Tooling
   ↓
G4 Existing-Method Binding / review
   ↓
G5 Dogfood Candidate
   ↓
G6 Closure & Utility Review
```

Cada gate debe declarar `PASS`, `FAIL` o `INCONCLUSIVE` cuando corresponda. Un
`FAIL` bloqueante o `INCONCLUSIVE` no resuelto impide promoción.

Stage 2 requiere una nueva admission review y autorización explícita.

---

## Métricas mínimas

```text
candidate_binding_detection = 100%
stale_evidence_detection = 100%
new_dependencies = 0
runtime_delta = 0
kernel_delta = 0
authority_effects = 0
false_authority_states = 0
```

Además se registrará cualitativamente:

- pasos manuales;
- overhead de review;
- facilidad de reconstrucción externa.

---

## Stop conditions

Detener y escalar si la unidad requiere:

- modificar Kernel, Blueprint, Governance o Security authority;
- crear una Capability o dependencia externa;
- permitir self-authorization/self-escalation;
- convertir evidencia en autoridad;
- ocultar o reescribir evidencia histórica;
- auto-fix fuera del Correction Budget;
- auto-merge o delivery enforcement;
- ampliar scope desde un finding.

Ante evidencia insuficiente:

```text
INCONCLUSIVE
```

Nunca `PASS` por defecto.

---

## Rollback

El rollback elimina contrato, helper, tests y artefactos de Stage 1 sin migrar
runtime ni datos de usuario. Los manifests históricos ya emitidos pueden
preservarse como evidencia de sus candidatos originales.

---

## Definition of Done — RDD-M1

```text
[ ] candidate binding exacto y reproducible
[ ] stale evidence detection
[ ] baseline ancestry validada
[ ] manifest v1 estricto
[ ] FULL 4R representable cuando aplica
[ ] bounded correction conserva historia
[ ] evidence carries zero authority
[ ] external reconstruction viable
[ ] new dependencies = 0
[ ] Kernel/runtime/security delta = 0
[ ] targeted tests PASS
[ ] full suite PASS
[ ] compileall PASS
[ ] git diff --check PASS
[ ] independent validation completed
[ ] human governance completed
[ ] downstream reconciliation evaluated
```

Hasta satisfacer esta lista, RDD-M1 permanece candidato y el PR debe continuar
en Draft.
