---
title: Malāk E5-F1 — Governed Git Delivery — G0 File Coverage Ledger
status: gate_pass_with_write_blockers
authority: operational admission evidence
as_of_date: 2026-09-19
unit_id: MALAK-E5-F1
gate: G0
source_baseline: 1b4bc19769344458e1af7943c45c34a2fb8a67e5
vault_baseline: 980491c8dce53b254571902ca52786796e8eee49
language: es
---

# Malāk E5-F1 — G0 File Coverage Ledger

## Resultado

```text
G0 RESULT: PASS FOR DESIGN
write implementation: BLOCKED
blocking findings for design: 0
blocking findings for Git writes: 2

tracked files discovered: 262
tracked files classified: 262
silently omitted files: 0
implementation code touched: 0
```

El árbol Git recursivo del baseline oficial
`1b4bc19769344458e1af7943c45c34a2fb8a67e5` declaró `truncated: false`.

El Project Vault se encuentra reconciliado en
`980491c8dce53b254571902ca52786796e8eee49`.

---

## Inventario por familia

```text
.github/**                  2
architecture              14
development                5
governance                 2
knowledge                 10
concepts                   6
project state              6
sprints/proposals         64
src/malak/**              73
tests/**                  50
other                     30
----------------------------
tracked blobs            262
classified blobs         262
silently omitted           0
```

---

## Lectura profunda requerida

```text
AGENTS.md
SECURITY.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/development/malak_construction_protocol.md
docs/development/engineering_method.md
docs/project/repository_standard.md
docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
docs/project/sprints/proposals/MALAK-E5-B1-READONLY-EXPLORER-G0-G1-DESIGN.md
src/malak/app/cli.py
src/malak/app/composition.py
src/malak/infrastructure/repository_reader.py
src/malak/security/contracts.py
src/malak/security/pdp.py
src/malak/security/pep.py
src/malak/security/audit.py
src/malak/security/context_validator.py
src/malak/security/context_issuer.py
tests/test_cli.py
tests/test_authorization_contracts.py
tests/test_policy_decision_point.py
tests/test_policy_enforcement_point.py
tests/test_authorization_audit.py
```

Razón: E5-F1 introduce potencialmente operaciones externas con side effects,
por lo que debe reutilizar la frontera de seguridad ya existente y no crear una
ruta paralela de autorización en la CLI.

---

# Findings

## E5F1-G0-01 — No existe Git writer en producción

```text
status: OBSERVED
blocking design: no
blocking writes: no
```

El baseline sólo contiene `GitRepositoryReader`, deliberadamente read-only.

No se observaron en `src/malak/**` primitivas de:

- `git push`;
- creación o borrado de ramas;
- modificación de remotos;
- merge;
- force-push.

Disposición: cualquier writer futuro debe ser un adapter operacional separado
de E0.

## E5F1-G0-02 — El Security Control Plane existe como contratos

```text
status: OBSERVED
blocking design: no
blocking writes: no
```

El baseline ya contiene:

- `PermissionScope`;
- `SecurityContext`;
- `AuthorizationRequest`;
- `AuthorizationOperationBinding`;
- `HumanConfirmationEvidence`;
- `StaticPolicyDecisionPoint`;
- `StrictPolicyEnforcementPoint`;
- auditoría fail-closed.

Esto permite diseñar Git write operations sin inventar otro modelo de
autorización.

## E5F1-G0-03 — Security Control Plane no está compuesto en la CLI

```text
status: BLOCKING_GAP
blocking design: no
blocking writes: yes
```

No existe en el baseline actual composición de:

```text
CLI
→ SecurityContext
→ PDP
→ PEP
→ protected Git operation
```

Disposición:

- F1-A read-only preflight puede avanzar;
- F1-B/F1-C write execution no puede avanzar hasta existir composición
  explícita de seguridad para la terminal.

## E5F1-G0-04 — No existe HumanConfirmationVerifier concreto de producción

```text
status: BLOCKING_GAP
blocking design: no
blocking writes: yes
```

El protocolo `HumanConfirmationVerifier` existe, pero no se observó una
implementación productiva concreta.

Una confirmación textual directa dentro de `cli.py` no puede sustituir esta
frontera sin una decisión de diseño separada.

## E5F1-G0-05 — Branch cleanup requiere prueba de elegibilidad

```text
status: OBSERVED
blocking design: no
blocking writes: no
```

Borrar una rama debe depender de evidencia determinista, como mínimo:

- repo y remote exactos;
- default branch conocida;
- target branch explícita;
- target != default branch;
- target != current protected branch;
- existencia local/remota observada;
- worktree limpio;
- ancestry/merge verificable contra default branch;
- zero wildcard;
- zero force deletion por defecto.

No debe inferirse elegibilidad a partir del nombre de la rama.

---

# Security Horizon

| Línea | Resultado |
| --- | --- |
| Prompt & Context Trust | ALREADY_COVERED — namespace exacto, cero LLM routing |
| Identity & Delegation | REQUIRES_REINFORCEMENT — CLI aún no posee SecurityContext operacional |
| Compromise Containment | ALREADY_COVERED — no shell passthrough, operación acotada |
| Memory / Knowledge | NOT_APPLICABLE |
| Supply Chain | ALREADY_COVERED — cero dependencia nueva necesaria |
| Data / Secrets | REQUIRES_REINFORCEMENT — nunca loggear credenciales/remotes con secretos |
| Resource Governance | ALREADY_COVERED — comandos discretos, sin loops |
| Human in Control | BLOCKING FOR WRITES — confirmación gobernada requerida |
| Auditability | BLOCKING FOR WRITES — ejecución debe pasar PEP + audit |

---

# Cierre G0

```text
E5-F1 design                     PASS
F1-A read-only preflight         ADMISSIBLE
F1-B governed push               DESIGNABLE / IMPLEMENTATION BLOCKED
F1-C governed branch cleanup     DESIGNABLE / IMPLEMENTATION BLOCKED

new Git writer required          yes
new dependency required          no
Kernel change required           no
Planner change required          no
Security core rewrite required   no
CLI security composition needed  yes
human confirmation verifier      needed before writes
FULL 4R for write implementation required
```

Este PASS autoriza únicamente G1 documental.
