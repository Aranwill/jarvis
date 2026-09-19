---
title: Malāk E5-F1 — Governed Git Delivery — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-19
baseline_commit: 1b4bc19769344458e1af7943c45c34a2fb8a67e5
vault_reconciliation_commit: 980491c8dce53b254571902ca52786796e8eee49
g0_result: pass_for_design
g0_ledger: docs/project/sprints/proposals/MALAK-E5-F1-GOVERNED-GIT-DELIVERY-G0-COVERAGE-LEDGER.md
design_authorized_by: owner
design_authorized_at: 2026-09-19
red_authorized: false
implementation_authorized: false
risk_class: 3
---

# Malāk E5-F1 — Governed Git Delivery — G0/G1 Design

## 1. Propósito

Incorporar a la Terminal Adaptativa un cierre natural de implementación:

```text
implementation
→ validation
→ push
→ human PR / merge
→ safe branch cleanup
```

E5-F1 no crea un shell Git genérico.

Objetivo:

> Facilitar push y limpieza post-merge mediante operaciones Git explícitas,
> acotadas y verificables, sin saltar PDP/PEP, confirmación humana ni auditoría.

---

## 2. Baseline y admisión

```text
Malāk main
1b4bc19769344458e1af7943c45c34a2fb8a67e5

Vault main
980491c8dce53b254571902ca52786796e8eee49

E5-A  Command Surface          INTEGRATED
E5-B1 Read-only Explorer      INTEGRATED
E5-F1 Governed Git Delivery   NOT AUTHORIZED before this design
```

G0:

```text
tracked files discovered = 262
tracked files classified = 262
silently omitted files   = 0

design admission          PASS
Git write implementation BLOCKED
```

Las cuatro preguntas de ley pasan para diseño. Kernel y Planner permanecen sin
cambios.

---

## 3. Frontera obligatoria

Una operación Git con side effects sólo puede seguir esta ruta:

```text
CLI intent
→ deterministic preflight
→ AuthorizationRequest + operation binding
→ PDP
→ governed human confirmation
→ PEP
→ protected Git operation
→ deterministic verification
→ audit evidence
```

Prohibido:

```text
CLI → subprocess git write
```

---

## 4. Partición adaptativa

```text
F1-A Git Delivery Preflight
  READ-ONLY
  READY FOR RED AUTHORIZATION

F1-B Governed Push
  DESIGN COMPLETE
  IMPLEMENTATION BLOCKED

F1-C Governed Branch Cleanup
  DESIGN COMPLETE
  IMPLEMENTATION BLOCKED
```

Blockers de B/C:

1. la CLI aún no compone un SecurityContext/PDP/PEP operacional;
2. no existe HumanConfirmationVerifier concreto de producción.

No se resuelven con bypass local.

---

## 5. Namespace curado

```text
/git help
/git status
/git plan push <branch>
/git plan cleanup <branch>
```

Futuro, cuando seguridad esté compuesta:

```text
/git push <branch>
/git cleanup <branch>
```

Nunca:

```text
/git exec ...
/git raw ...
/git <arbitrary shell text>
```

No se aceptan opciones Git arbitrarias.

---

## 6. Git operacional != E0

E0 permanece snapshot-bound y read-only.

F1 necesita estado operacional vivo, por lo que el owner candidato es un
`GitDeliveryInspector` separado, read-only y determinista.

Debe observar:

- repository identity;
- current branch;
- HEAD;
- worktree cleanliness;
- remote identity;
- upstream;
- ahead/behind;
- default branch;
- branch existence;
- merge ancestry.

Reglas:

- argv explícito;
- `shell=False`;
- comandos Git allowlisted;
- no fetch/pull automático;
- no write durante preflight;
- no cwd implícito.

---

## 7. F1-A — Preflight

### /git status

Salida mínima:

```text
repository_identity
current_branch
head_sha
worktree_clean
remote
upstream
ahead
behind
default_branch
delivery_ready
reasons[]
```

Remote URLs con secretos nunca se imprimen completas.

### /git plan push <branch>

Elegible sólo si:

- repo/remoto coinciden con configuración;
- branch explícita y válida;
- HEAD no detached;
- current branch == requested branch;
- branch != default branch;
- worktree limpio;
- no divergence incompatible;
- HEAD exacto queda capturado.

Salida:

```text
eligible
branch
head_sha
remote
ahead
behind
reasons[]
operation_fingerprint
```

### /git plan cleanup <branch>

Elegible sólo si:

- branch explícita, válida y sin wildcard;
- branch != default branch;
- current branch != target;
- worktree limpio;
- target SHA conocido;
- ancestry contra default branch verificable;
- target está efectivamente mergeado;
- presencia local/remota declarada.

No borra nada.

---

## 8. Operation binding

Toda write futura usa `AuthorizationOperationBinding`.

Push liga como mínimo:

```text
operation = git.push
repository_identity
remote_identity
branch
head_sha
force = false
```

Cleanup liga como mínimo:

```text
operation = git.cleanup
repository_identity
remote_identity
branch
target_sha
default_branch
verified_default_head_sha
force = false
```

Si cambia repo, remote, branch o SHA:

```text
binding changes
→ confirmation invalid
→ new preflight required
```

---

## 9. F1-B — Governed Push

Ruta futura:

```text
/git push <branch>
→ fresh preflight
→ AuthorizationRequest
→ PDP
→ human confirmation
→ PEP
→ ProtectedGitPush
→ verify remote ref == expected HEAD
→ audit
```

V0:

- sólo remote configurado;
- sólo branch explícita;
- no default branch;
- no tags/refspec libre;
- no wildcard;
- no force / force-with-lease;
- no delete;
- una rama por operación.

Un push ya satisfecho puede devolver `NO_OP`.

---

## 10. F1-C — Governed Branch Cleanup

Ruta futura:

```text
/git cleanup <branch>
→ fresh cleanup preflight
→ merged eligibility verified
→ AuthorizationRequest
→ human confirmation
→ PEP
→ safe deletion
→ verify absence
→ audit
```

V0:

- default branch jamás elegible;
- current branch jamás elegible;
- protected names jamás elegibles;
- no wildcard/pattern deletion;
- no `git branch -D`;
- local delete usa semántica segura equivalente a `git branch -d`;
- remote delete, si existe, queda ligado explícitamente;
- ausencia local/remota se informa, no amplía autoridad.

Antes de borrar se conserva target SHA en evidencia.

---

## 11. Seguridad y confirmación humana

Scopes separados:

```text
git.delivery / push
git.delivery / cleanup_branch
```

No wildcards.

Una pregunta `[y/N]` por sí sola no sustituye el Security Control Plane.

Antes de writes debe existir HumanConfirmationVerifier concreto y evidencia
ligada a:

- subject;
- permission;
- request;
- operation binding;
- confirmer;
- timestamp.

Git writes deben pasar por `StrictPolicyEnforcementPoint`.

---

## 12. Fail-closed

Ejemplos:

```text
dirty worktree               → DENY
detached HEAD                → DENY
branch mismatch              → DENY
default branch target        → DENY
remote mismatch              → DENY
divergence uncertainty       → DENY
binding mismatch             → DENY
confirmation unavailable     → DENY
audit unavailable            → DENY before write
merge ancestry unknown       → DENY cleanup
```

Credenciales nunca se incluyen en logs/auditoría.

---

## 13. Scope futuro

F1-A RED candidato:

```text
tests/test_git_delivery.py
tests/test_cli.py
```

F1-A GREEN candidato:

```text
src/malak/infrastructure/git_delivery.py
src/malak/app/cli.py
```

F1-B/C no reciben scope de implementación hasta resolver los blockers de
seguridad.

---

## 14. RED futuro F1-A

Debe cubrir al menos:

- status repo/branch/HEAD/worktree/remotes;
- secrets redacted;
- no cwd fallback;
- plan push exact branch;
- default-branch push denied;
- dirty/detached/diverged denied;
- no force;
- cleanup default/current/wildcard denied;
- unknown/unmerged ancestry denied;
- merged eligible branch accepted;
- zero mutations;
- zero network writes;
- zero LLM;
- E5 regressions green.

---

## 15. Stop conditions

STOP si se intenta:

- convertir E0 en writer;
- ejecutar shell libre;
- aceptar opciones Git arbitrarias;
- force-push;
- borrar default branch;
- wildcard delete;
- bypass PDP/PEP;
- usar confirmación textual como autoridad sin verifier;
- registrar secretos;
- inferir merge por nombre de rama;
- auto-merge PR;
- ampliar Kernel/Planner.

---

## 16. Resultado

```text
E5-F1 Governed Git Delivery

G0 design admission      PASS
G1 design                COMPLETE

F1-A Git Preflight       READY FOR RED AUTHORIZATION
F1-B Governed Push       IMPLEMENTATION BLOCKED
F1-C Branch Cleanup      IMPLEMENTATION BLOCKED

RED                      NOT AUTHORIZED
GREEN                    NOT AUTHORIZED
Git writes               NOT AUTHORIZED
```

Principio:

```text
Convenience != Authority
Git command != shell
Preflight before permission
Permission before execution
Verification after execution
```
