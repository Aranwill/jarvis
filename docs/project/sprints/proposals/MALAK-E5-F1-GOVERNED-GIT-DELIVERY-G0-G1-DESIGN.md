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

Incorporar a la Terminal Adaptativa un flujo natural para cerrar una
implementación sin depender de bloques PowerShell repetitivos, preservando
seguridad, Human in Control y trazabilidad.

Intención del Owner:

```text
implementation
  ↓
validation
  ↓
push
  ↓
human PR / merge
  ↓
safe branch cleanup
```

E5-F1 no crea un shell Git genérico.

Pregunta de aceptación:

> ¿Puede Malāk facilitar push y limpieza post-merge mediante operaciones Git
> explícitas, acotadas y verificables, sin permitir comandos arbitrarios ni
> saltar PDP/PEP, confirmación humana o auditoría?

---

## 2. Baseline

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

---

## 3. Cuatro preguntas de ley

```text
Blueprint                  PASS FOR DESIGN
Cognitive Constitution     PASS FOR DESIGN
Governance Constitution    PASS FOR DESIGN
Kernel complexity          NO DELTA
```

Condición obligatoria:

Git writes sólo pueden pasar a implementación cuando la ruta sea:

```text
CLI intent
  ↓
deterministic preflight
  ↓
AuthorizationRequest + exact operation binding
  ↓
PDP
  ↓
human confirmation when required
  ↓
PEP
  ↓
protected Git operation
  ↓
verification
  ↓
audit evidence
```

Nunca:

```text
CLI
  ↓
subprocess git push/delete
```

---

## 4. Partición adaptativa

```text
E5-F1-A — Git Delivery Preflight
  status / plan / eligibility
  READ-ONLY
  ADMISSIBLE

E5-F1-B — Governed Push
  protected external write
  DESIGN COMPLETE
  IMPLEMENTATION BLOCKED

E5-F1-C — Governed Branch Cleanup
  protected local/remote deletion
  DESIGN COMPLETE
  IMPLEMENTATION BLOCKED
```

Los blockers de B/C son:

1. Security Control Plane no compuesto en la CLI.
2. No existe HumanConfirmationVerifier concreto de producción.

No se resolverán mediante bypass local.

---

## 5. Namespace curado

Namespace:

```text
/git
```

No existe passthrough.

Prohibido:

```text
/git <arbitrary shell text>
/git exec ...
/git raw ...
```

F1-A V0:

```text
/git help
/git status
/git plan push <branch>
/git plan cleanup <branch>
```

F1-B/C futuros:

```text
/git push <branch>
/git cleanup <branch>
```

Estos comandos futuros inician una operación protegida; no implican ejecución
sin autorización.

---

## 6. Git operacional != E0

E0 permanece snapshot-bound y read-only.

E5-F1 necesita observar estado operacional vivo:

- current branch;
- HEAD;
- worktree cleanliness;
- remote names;
- remote URL identity;
- upstream;
- ahead/behind;
- default branch;
- local branch existence;
- remote branch existence;
- ancestry/merge eligibility.

Por lo tanto:

```text
GitRepositoryReader != GitDeliveryInspector
```

El futuro `GitDeliveryInspector`:

- es read-only;
- vive fuera de E0;
- usa comandos Git allowlisted;
- usa argv explícito;
- usa `shell=False`;
- no modifica refs;
- no hace fetch/pull automáticamente;
- no escribe red.

No se crea en G0/G1.

---

## 7. F1-A — Preflight

### /git status

Debe presentar al menos:

```text
repository_root
repository_identity
current_branch
head_sha
worktree_clean
remote_name
remote_identity
upstream
ahead
behind
default_branch
delivery_ready
reasons[]
```

No imprime credenciales embebidas en remote URLs.

### /git plan push <branch>

Debe fallar cerrado salvo que:

- repository root sea explícito;
- repo identity coincida con configuración;
- remote exacto sea permitido;
- branch sea sintácticamente válida;
- branch sea explícita;
- HEAD no esté detached;
- current branch == requested branch;
- branch != default branch;
- worktree esté limpio;
- no exista operación Git conflictiva;
- upstream/divergence sea compatible con push no forzado;
- HEAD SHA quede capturado en el plan.

Salida:

```text
action: push
eligible: true|false
branch
head_sha
remote
upstream
ahead
behind
reasons[]
operation_fingerprint
```

### /git plan cleanup <branch>

Debe fallar cerrado salvo que:

- branch sea explícita y válida;
- branch != default branch;
- branch no sea wildcard;
- current branch != target branch;
- worktree esté limpio;
- target commit exista;
- default branch remota observada sea coherente;
- target commit sea ancestor del default branch verificado;
- local/remote presence quede declarada;
- no exista incertidumbre de ancestry.

Salida:

```text
action: cleanup
eligible: true|false
branch
target_sha
default_branch
default_head_sha
local_present
remote_present
merged_verified
reasons[]
operation_fingerprint
```

No borra nada.

---

## 8. Repository / remote identity

F1 no confía en el cwd.

Debe existir configuración explícita de identidad operacional.

Conceptualmente:

```text
repository_root
expected_repository_identity
remote_name
expected_remote_identity
```

Remote identity debe normalizar URL sin exponer secretos.

Si la URL contiene credentials/tokens:

- se usan sólo para Git;
- nunca se muestran completas;
- nunca entran en audit;
- nunca forman parte textual de errores.

La comparación de identidad debe basarse en una forma canónica segura.

---

## 9. Protected operation binding

Cada write futuro debe quedar ligado a una operación exacta mediante
`AuthorizationOperationBinding`.

Payload conceptual de push:

```text
operation = git.push
repository_identity
remote_identity
branch
head_sha
expected_upstream
force = false
```

Payload conceptual de cleanup:

```text
operation = git.cleanup
repository_identity
remote_identity
branch
target_sha
default_branch
verified_default_head_sha
local_delete
remote_delete
force = false
```

Se serializa canónicamente y se liga por digest.

Si cualquier campo cambia:

```text
operation binding changes
→ previous confirmation invalid
→ re-preflight required
```

---

## 10. F1-B — Governed Push

Cuando los blockers de seguridad estén resueltos:

```text
/git push <branch>
  ↓
fresh preflight
  ↓
eligible?
  ├─ no → DENY
  └─ yes
       ↓
AuthorizationRequest
       ↓
PDP
       ↓
human confirmation
       ↓
PEP
       ↓
ProtectedGitPush.execute()
       ↓
verify remote ref == expected HEAD
       ↓
audit
```

Reglas V0:

- sólo remote configurado;
- sólo branch explícita;
- no default branch;
- no tags;
- no wildcard;
- no refspec libre;
- no `--force`;
- no `--force-with-lease`;
- no delete;
- no arbitrary options;
- no push múltiple.

Initial upstream puede admitirse únicamente como forma fija equivalente a
`push --set-upstream <remote> <branch>`.

---

## 11. F1-C — Governed Branch Cleanup

Objetivo: limpiar una rama después de merge humano verificado.

El comando conceptual:

```text
/git cleanup <branch>
```

no significa "borrar porque el usuario escribió el nombre".

Ruta:

```text
fresh cleanup preflight
  ↓
target merged into verified default branch?
  ├─ no / unknown → DENY
  └─ yes
       ↓
AuthorizationRequest
       ↓
human confirmation
       ↓
PEP
       ↓
delete eligible refs
       ↓
verify absence
       ↓
audit
```

Reglas:

- default branch jamás elegible;
- current branch jamás elegible;
- protected names configurables;
- no wildcard;
- no pattern deletion;
- no `git branch -D` en V0;
- local delete usa semántica segura equivalente a `git branch -d`;
- remote delete, si se admite, es operación explícitamente ligada;
- remote already absent no convierte local cleanup en fallo;
- local already absent no autoriza remote delete por sí mismo.

---

## 12. Human confirmation

Una simple pregunta `[y/N]` no sustituye el Security Control Plane.

Antes de habilitar writes debe existir una implementación concreta de
`HumanConfirmationVerifier`.

La UX puede ser interactiva, pero la evidencia deberá quedar ligada a:

- subject;
- permission;
- original request;
- new request;
- operation binding;
- timestamp;
- confirmer.

La confirmación no es reutilizable después de cambios de branch/SHA/remote.

---

## 13. Permission scopes

Scopes conceptuales separados:

```text
resource: git.delivery
action: push

resource: git.delivery
action: cleanup_branch
```

No usar:

```text
resource: git
action: *
```

No wildcards.

Push y cleanup requieren reglas distintas.

---

## 14. Auditoría

Git writes deben pasar por `StrictPolicyEnforcementPoint`.

Audit mínimo:

- request_id;
- subject_id;
- permission;
- outcome;
- reason_code;
- operation binding digest;
- protected operation binding;
- protected operation permission.

Además, una ejecución exitosa debe producir evidencia operacional no secreta:

```text
action
repository identity
branch
before_sha
after/verified_sha
remote identity
verification result
```

Nunca tokens, passwords o remote URLs con credentials.

---

## 15. Failure semantics

Todo fallo sensible es fail-closed.

Ejemplos:

```text
dirty worktree                   → DENY
detached HEAD                    → DENY
branch mismatch                  → DENY
default branch target            → DENY
remote mismatch                  → DENY
ahead/behind uncertainty         → DENY
operation binding mismatch       → DENY
confirmation unavailable         → DENY
audit unavailable before write   → DENY
merge ancestry unknown           → DENY cleanup
remote verification failed       → FAIL / evidence
```

No hay fallback a shell manual dentro del mismo comando.

---

## 16. Rollback / recovery

### Push

Un push normal no debe "rollbackearse" automáticamente mediante force-push.

Si se subió una rama equivocada por un fallo imposible de prevenir,
la remediación requiere flujo humano separado.

### Cleanup

Antes de local deletion debe conservarse el target SHA en evidencia.

Una rama local eliminada puede recrearse manualmente desde SHA si sigue
disponible.

Remote branch deletion no se revierte automáticamente.

Esta irreversibilidad justifica confirmación humana y FULL 4R.

---

## 17. No-op y idempotencia

F1-A siempre es read-only.

F1-B:

- push cuando remote ref ya == HEAD puede devolver `NO_OP`;
- no debe crear un segundo efecto.

F1-C:

- local/remote branch ya ausente se reporta de forma explícita;
- ausencia no habilita acciones adicionales;
- cleanup debe ser convergente sin usar force.

---

## 18. Scope futuro

### F1-A RED candidato

```text
tests/test_git_delivery.py
tests/test_cli.py
```

### F1-A GREEN candidato

```text
src/malak/infrastructure/git_delivery.py
src/malak/app/cli.py
```

No security core changes.

### F1-B/C

No se autoriza scope hasta resolver:

- CLI SecurityContext composition;
- HumanConfirmationVerifier de producción;
- protected operation composition.

Cualquier propuesta de write que llame subprocess desde CLI directamente
produce STOP.

---

## 19. RED futuro F1-A

Cuando Owner autorice:

- status con repo/branch/HEAD/worktree/remotes;
- credentials redacted;
- explicit repository identity;
- no cwd fallback;
- plan push exact branch;
- default branch push denied;
- dirty worktree denied;
- detached HEAD denied;
- divergence denied;
- no force option;
- plan cleanup default branch denied;
- current branch cleanup denied;
- wildcard denied;
- unmerged/unknown ancestry denied;
- eligible merged branch accepted;
- zero mutations;
- zero network writes;
- zero LLM;
- existing E5 regressions green.

---

## 20. Stop conditions

STOP si F1 intenta:

- modificar E0 para convertirlo en writer;
- ejecutar shell libre;
- aceptar Git options del usuario;
- force-push;
- borrar default branch;
- wildcard deletion;
- bypass PDP/PEP;
- usar confirmación textual como autoridad sin verifier;
- registrar secretos;
- inferir merge sólo por branch name;
- auto-merge PR;
- ampliar Kernel/Planner;
- agregar dependencia innecesaria.

---

## 21. Resultado

```text
E5-F1 Governed Git Delivery

G0 design admission          PASS
G1 design                    COMPLETE

F1-A Git Preflight           READY FOR RED AUTHORIZATION
F1-B Governed Push           IMPLEMENTATION BLOCKED
F1-C Branch Cleanup          IMPLEMENTATION BLOCKED

Blockers:
- CLI security composition
- concrete HumanConfirmationVerifier

RED                          NOT AUTHORIZED
GREEN                        NOT AUTHORIZED
Git writes                   NOT AUTHORIZED
```

Principio final:

```text
Convenience != Authority
Git command != shell
Preflight before permission
Permission before execution
Verification after execution
Evidence after effect
```
