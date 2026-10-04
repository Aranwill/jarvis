---
title: Malāk E3 Governed Blind Assessor Experiment Harness V0 — Case-set Byte Stability Design Amendment
status: design_candidate
authority: non_normative
language: es
as_of_date: 2026-10-04
baseline_commit: 0b365e4e60caf103a977a0ddc8adf7ff5bcfec33
supersedes: none
amends: MALAK-E3-GOVERNED-BLIND-ASSESSOR-EXPERIMENT-HARNESS-V0-G0-G1-DESIGN-20261004
trigger: F254-RED-01
risk_class: 3
critical_contract: true
runtime_delta: 0
green_authorized: false
authority_effect: none
---

# E3 Governed Blind Assessor Experiment Harness V0 — Case-set Byte Stability Design Amendment

## 1. Trigger

PR-B #254 fue creada desde:

`0b365e4e60caf103a977a0ddc8adf7ff5bcfec33`

con RED candidate:

`b59560ccc4b4d601cd945ff8ce13099c96a5458b`.

Validation #796 / run `37227200322` mostró:

~~~text
Ubuntu   20 failed / 1879 passed
Windows  21 failed / 1878 passed
~~~

Los 20 failures comunes son RED causal por comportamiento no implementado.

Windows añade un failure material previo al harness:

~~~text
profile.expected_case_set_digest
!= SHA256(CASE_SET.read_bytes())
~~~

Finding:

~~~text
F254-RED-01
severity: MATERIAL
type: CROSS_PLATFORM_EXACT_BYTE_IDENTITY_DRIFT
authority_effect: none
~~~

## 2. Root cause

El Design integrado exige:

~~~text
expected_case_set_digest =
SHA-256 lowercase de los bytes exactos del cases.json leído
~~~

El Qualification Pack existente también usa:

~~~text
raw = path.read_bytes()
case_set_digest = SHA256(raw)
~~~

Por tanto el producer y el consumer ligan bytes físicos del path leído.

El blob Git actual de:

`evaluations/e3_governed_evidence_support_assessor_v0/cases.json`

está normalizado a LF y su digest esperado es:

`23e045b5e5aede8341323c486e77893d7161899f0c20870703efff28789f3f83`.

Sin un atributo repository-controlled, Git puede materializar CRLF en Windows según
`core.autocrlf` / `core.eol`. Esto cambia los bytes físicos y, por diseño,
cambia el digest.

Fuente externa primaria de comportamiento Git:

`https://git-scm.com/docs/gitattributes`

La documentación oficial establece que `eol=lf` hace que el working tree use LF
para el path afectado y evita la conversión a CRLF en checkout.

## 3. Why STOP was correct

La PR-A original congeló future PR-B a tres archivos y agotó:

~~~text
Correction Budget = 2 / 2
~~~

Cambiar ahora cualquiera de estos puntos sin Design Amendment sería inválido:

- ampliar PR-B a un cuarto archivo;
- reinterpretar "exact bytes";
- cambiar el consumer existente;
- introducir una canonicalización nueva;
- introducir dependencia de Git blob/subprocess.

Por tanto:

~~~text
F254-RED-01 MATERIAL
+ exhausted Design Correction Budget
→ STOP
→ separate Design Amendment PR
~~~

PR #254 permanece Draft y RED. No se autoriza GREEN.

## 4. Alternatives reviewed

### A. Normalize CRLF → LF inside the harness

Disposition:

`REJECT`

Reason:

- cambia la semántica de "bytes exactos leídos";
- el Qualification Pack existente seguiría leyendo bytes físicos del path;
- producer y consumer podrían divergir;
- convertiría un finding de identidad en una transformación silenciosa.

### B. Redefine expected_case_set_digest as canonical JSON digest

Disposition:

`REJECT`

Reason:

- cambia el contrato ya consumido;
- el artifact `case_set_digest` del Qualification Pack sigue siendo raw-byte bound;
- crea dos identidades distintas bajo un mismo nombre;
- requeriría contract redesign mayor.

### C. Bind profile to Git blob bytes through git subprocess / object lookup

Disposition:

`DEFER / REJECT FOR V0`

Reason:

- añade dependencia ambient de Git repository state;
- introduce una nueva lookup seam no necesaria;
- producer y Qualification Pack seguirían con fuentes de bytes distintas.

### D. Version-controlled path-specific LF checkout policy

Disposition:

`ADOPT`

Exact future rule:

~~~gitattributes
/evaluations/e3_governed_evidence_support_assessor_v0/cases.json text eol=lf
~~~

Why:

- preserva la semántica raw/exact-byte ya aprobada;
- preserva Qualification Pack sin cambios;
- mantiene el blob LF ya existente;
- estabiliza working-tree bytes en Ubuntu y Windows;
- limita el efecto a un solo case-set;
- no toca runtime ni authority.

## 5. Amended scope

Future PR-B scope, sólo tras review/merge humano de este amendment y nueva
autorización explícita del Owner:

~~~text
ALLOW
.gitattributes
evaluations/e3_governed_evidence_support_assessor_v0/experiment_profile.json
scripts/run_e3_governed_blind_assessor_experiment.py
tests/test_e3_governed_blind_assessor_experiment.py
~~~

Exact `.gitattributes` delta permitted:

~~~text
/evaluations/e3_governed_evidence_support_assessor_v0/cases.json text eol=lf
~~~

No se autoriza ningún wildcard global ni regla adicional.

Hard-zero permanece:

~~~text
src/malak/**
evaluations/e3_governed_evidence_support_assessor_v0/cases.json content
scripts/evaluate_e3_governed_evidence_support_assessor.py
scripts/evaluate_e3_deterministic_oracle_qualification.py
Kernel
Planner
Security contracts / PDP / PEP
Conversation
runtime/provider/model implementation
dependencies
network
support_sufficient
Protected Finalization
RDD Stage 2
~~~

## 6. Identity contract after amendment

The semantic contract remains unchanged:

~~~text
case-set raw bytes
→ SHA256
→ expected_case_set_digest
→ artifact.case_set_digest
→ Qualification Pack independent recomputation
~~~

The amendment changes only the repository checkout precondition:

~~~text
version-controlled case-set path
→ text eol=lf
→ platform-stable physical bytes
→ same SHA256 on Ubuntu and Windows
~~~

Expected current digest remains:

`23e045b5e5aede8341323c486e77893d7161899f0c20870703efff28789f3f83`.

No canonicalization or line-ending normalization is performed by the harness.

## 7. RED re-entry after amendment

The current RED candidate remains historical Evidence:

`b59560ccc4b4d601cd945ff8ce13099c96a5458b`.

It must not be patched in place before this amendment is integrated.

After human merge of this Design Amendment and Owner re-authorization of the
expanded four-file PR-B scope:

1. PR-B baseline must be updated to the amendment merge commit;
2. candidate identity changes;
3. `.gitattributes` exact scoped rule is added;
4. RED tests are rerun on Ubuntu and Windows;
5. expected RED must be causal on both platforms;
6. only then may Owner consider separate GREEN authorization.

Expected cross-platform RED:

~~~text
profile fixture validation                 PASS
case-set exact-byte digest                 PASS
public seam/import validation              PASS
new behavioral obligations                 FAIL — NotImplementedError
unrelated existing suite                   PASS
~~~

## 8. Security Horizon

This amendment:

- does not add network;
- does not add a model/provider;
- does not change candidate-visible material;
- does not add repo writes at runtime;
- does not change PDP/PEP/Security contracts;
- does not authorize support_sufficient;
- does not authorize RDD Stage 2;
- does not treat digest as proof of origin.

~~~text
stable bytes != trusted origin
digest equality != Authority
CI parity != semantic truth
~~~

## 9. Four Questions of Law

### Blueprint

PASS — evaluation tooling only; no Kernel/Planner/runtime delta.

### Cognitive Constitution

PASS — deterministic identity precondition, no cognitive authority change.

### Governance Constitution

PASS — STOP preserved, no silent scope expansion, Owner authority preserved.

### Kernel complexity

PASS — no Kernel delta.

## 10. Design 4R

### Risk — PASS candidate

The path-specific rule removes platform-dependent digest drift without weakening
the exact-byte contract.

Residual risk: future movement/rename of the case-set path invalidates the
attribute rule and requires revalidation.

### Readability — PASS candidate

~~~text
Git checkout policy
!= case-set content
!= experiment profile
!= harness
!= Qualification Pack
!= Authority
~~~

### Reliability — PASS candidate

Exact bytes become deterministic across supported CI OSes while producer and
consumer continue using the same raw-byte digest semantics.

### Resilience — PASS candidate

If the attribute is absent, wrong, broadened, or the path changes, cross-platform
digest tests must fail closed before GREEN.

## 11. Future RED requirements added

~~~text
GBAEH-R41 .gitattributes contains exactly the path-specific cases.json text eol=lf rule required by this amendment.
GBAEH-R42 Ubuntu and Windows read identical cases.json bytes and compute the same expected_case_set_digest.
GBAEH-R43 expected_case_set_digest remains 23e045b5e5aede8341323c486e77893d7161899f0c20870703efff28789f3f83 for the unchanged current case-set.
GBAEH-R44 no harness-side CRLF/LF normalization or canonicalization is used to satisfy R42/R43.
GBAEH-R45 Qualification Pack remains unchanged and independently recomputes artifact.case_set_digest from raw case-set bytes.
~~~

R01..R40 remain unchanged except that their case-set raw-byte precondition is now
made cross-platform deterministic by R41..R45.

## 12. Invalidation

Invalidate affected evidence if any of:

- `.gitattributes` rule changes;
- case-set path changes;
- case-set blob bytes change;
- expected digest changes;
- Qualification Pack raw-byte digest behavior changes;
- supported CI checkout behavior changes.

No stale PASS may be reused.

## 13. Gate state

~~~text
PR #253 Design                         MERGED / PASS
PR #254 RED                            OPEN / DRAFT / FROZEN
F254-RED-01                            MATERIAL
Design Correction Budget              EXHAUSTED 2 / 2
Design Amendment                       THIS PR — CANDIDATE
Independent pre-RED amendment review   REQUIRED
GREEN                                  NOT AUTHORIZED
Ready / Merge                          OWNER ONLY
model/provider experiment              NOT AUTHORIZED
RDD Stage 2                            NOT AUTHORIZED
authority_effect                       none
~~~

## 14. Next lawful transition

~~~text
candidate-bound CI for this docs-only amendment
→ independent pre-RED Design Amendment Review
→ human review
→ Owner Ready / Merge decision
→ post-merge reconciliation
→ explicit Owner re-authorization of expanded four-file PR-B scope
→ cross-platform RED re-entry
~~~

PASS of this amendment does not authorize GREEN.
