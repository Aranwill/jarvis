---
title: MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 — Batch B
status: completed
authority: derived_audit
baseline_commit: b1093f291e4a83af779302454485f46f21644801
units:
  - U03
  - U07
  - U12
authority_effect: none
remediation_authorized: false
---

# Batch B — Security, assurance and normative critical contracts

## 1. Resultado

```text
U03 Security control plane & secure context lifecycle
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

U07 Assurance & protected finalization
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

U12 Normative / architectural promotions
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

current blocking findings: 0
historical resolved findings: preserved
remediation authorized: false
```

## 2. Nota sobre historia sanitizada

La historia Git de Malāk fue posteriormente sanitizada/reconstruida. Por ello,
algunas PR históricas preservan candidate/merge SHA originales mientras el
`main` actual contiene commits reescritos equivalentes con identidad distinta.

La auditoría aplica:

```text
historical PR evidence
→ evidence of historical process

current repository content
→ evidence of current state

historical SHA no longer ancestor after rewrite
!= historical process never happened
```

No se usa ancestry antiguo para certificar el baseline actual después del
history rewrite. El baseline actual se revalida por contenido, contratos,
tests y CI vigentes.

## 3. U03 — Security control plane & secure context lifecycle

### Evidencia histórica

Sprint 7.5 preserva un desarrollo incremental de riesgo alto con aprobación
humana por incremento y separaciones explícitas:

```text
request
!= authorize
!= enforce/execute
!= audit
```

PRs verificadas:

```text
#15 Authorization contracts
  merge c0a4283b100609daeb4b3422dd28634df9d851b6

#17 Minimal PDP
  merge 78799deabba5009e66c219220349e8202f5464bb

#19 Initial PEP
  merge af64b062aa1395ba7f7bdd59e5c1099ded68b683

#22 Authorization audit contracts
  merge 418358cc5b543c59cf4b113f42e762f6c78eec59

#23 Audit integration into PEP
  merge 38b0917c5b8dba5c5a4ef4db157e78ac428ab4bc
```

Sprint 7.6 preserva:

```text
risk: Level 3 — High
SDD
TDD
FULL 4R
independent validation
human acceptance
339 passed
compileall PASS
git diff --check PASS
```

PRs verificadas:

```text
#39 SecurityContext lifecycle contract
#40 cumulative lifecycle/PDP integration
#42 SecurityContext propagation contract
```

La ficha de sprint preserva además PR #41 para validity-window semantics.

Sprint 7.7 realizó certificación integral del bloque, rollback review y
promoción humana explícita. Preservó:

```text
7.7-D-001 strong SecurityContext provenance
classification: ACCEPTED_RESIDUAL_RISK
severity: MEDIUM
blocking_release: NO
```

Ese riesgo residual es de producto/seguridad futura; no constituye por sí mismo
un gap del flujo de construcción.

### Revalidación actual

Código y tests actuales preservan, entre otros:

- exact allow/deny matching;
- default/fail-closed denial paths;
- no wildcard subject/permission;
- authentication before policy;
- temporal validity before policy;
- exact operation binding PDP→PEP;
- mismatched binding blocked before execution;
- audit-before-operation;
- audit failure blocks an otherwise allowed operation;
- decision failure remains fail-closed;
- immutable audit records without sensitive payloads;
- issuer/validator/renewer responsibilities separated;
- renewal does not revive expired contexts;
- propagation preserves exact context and does not reconstruct authority.

Validation #401 sobre `main@b1093f29...` ejecutó la suite completa con jobs
Ubuntu y Windows en `success`.

### Matriz U03

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / admission | HISTORICAL_PASS | Sprint 7.5/7.6 scope and approval records |
| G1 design | HISTORICAL_PASS | contracts, ADR-002 and lifecycle design |
| Critical Contract Hardening | N/A_WITH_REASON | checkpoint nominal posterior; threat/fail-closed review sí existía |
| four law questions | HISTORICAL_PASS | Sprint 7.6 records all four |
| Design 4R | N/A_WITH_REASON | separación nominal Design 4R posterior |
| RDD Stage 1 Design Check | N/A_WITH_REASON | RDD Stage 1 posterior |
| RED / GREEN | N/A_WITH_REASON | nomenclatura posterior; TDD histórico preservado |
| targeted validation | HISTORICAL_PASS | focused tests per increments |
| Candidate FULL 4R | HISTORICAL_PASS | Sprint 7.6 final 4R |
| Bounded Correction | HISTORICAL_PASS | incremental findings/corrections preserved by sprint history |
| Fix Validator / affected revalidation | HISTORICAL_PASS | independent validation + revalidation |
| E2E / integration | HISTORICAL_PASS | PDP/PEP/audit/lifecycle integration |
| CI candidate-bound | N/A_WITH_REASON | reusable candidate-bound CI introduced later by Sprint 7.11 |
| independent validation | HISTORICAL_PASS | Sprint 7.6 |
| RDD Candidate Conformance | N/A_WITH_REASON | formal checkpoint posterior |
| human review / merge | HISTORICAL_PASS | PR sequence + owner approvals |
| post-merge validation | HISTORICAL_PASS | Sprint 7.6/7.7 records |

### Disposición U03

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current construction-flow gap: none found
accepted product residual risk: preserved
```

## 4. U07 — Assurance & protected finalization

### Secuencia histórica

PR #110:

```text
G2A Protected Finalization Foundation
G0 PASS / ADAPT
G1 PASS / SPLIT
Owner authorization
candidate: 7cae3dcb854207175b716b66c9c569a335f81516
Validation #124: Ubuntu/macOS/Windows PASS
G2B: NOT AUTHORIZED
```

PR #111:

```text
Assurance Signal Authority Boundary G0/G1
documentation only
no implementation authority
```

PR #117:

```text
G2 specification hardening
request/session binding
temporal coherence
bounded cardinality
deterministic precedence
no implementation authority
```

PR #118:

```text
Owner-authorized G2 implementation
baseline: 7339805d...
candidate: 0bd6fa4f...
Validation #147: Ubuntu/Windows PASS

RED candidate:
82032c3eef7ab75d40abb35a7a4ff79e28e66a95
→ tests fail because module absent

GREEN:
assurance_signal_projection.py

bounded correction:
F002 cardinality guard before nested inspection

FULL 4R:
Risk / Readability / Reliability / Resilience PASS

Ready/merge:
Owner-only
```

### Revalidación actual

`protected_finalization.py` sigue siendo un evaluator determinista aislado:

```text
ACCEPT | ABSTAIN | BLOCK
explicit reason codes
no provider/LLM call
no persistence
no conversation wiring
```

`assurance_signal_projection.py` mantiene:

```text
READY | HOLD | DENIED
exact signal kinds
request/session binding
producer subject binding
value-sensitive permission
temporal checks
max cardinality = 5
no favorable coercion/default
```

Tests actuales cubren missing/duplicate signals, wrong permission,
unauthenticated contexts, request/session mismatch, temporal invalidity,
cardinality-before-element-inspection, unknown policy versions and deterministic
permutation behavior.

Validation #401 confirma suite integrada vigente en Ubuntu y Windows.

### Matriz U07

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / G1 | HISTORICAL_PASS | PR #110/#111/#117 |
| Critical Contract Hardening | HISTORICAL_PASS | PR #117 explicit hardening, aunque nombre formal actual es posterior |
| four law questions | PARTIALLY_EVIDENCED | principios/limits preserved, no se relabelan como checkpoint actual sin registro exacto para cada subunit |
| Design 4R | N/A_WITH_REASON | checkpoint nominal posterior |
| RDD Stage 1 Design Check | PARTIALLY_EVIDENCED | RDD Stage 1 ya existía, pero no se reconstruye un checkpoint terminal inexistente |
| RED | HISTORICAL_PASS | PR #118 RED candidate exacto |
| GREEN | HISTORICAL_PASS | PR #118 implementation candidate |
| targeted validation | HISTORICAL_PASS | focused tests |
| Candidate FULL 4R | HISTORICAL_PASS | PR #118 |
| Bounded Correction | HISTORICAL_PASS | F002 |
| Fix Validator / revalidation | HISTORICAL_PASS | correction revalidated before final review |
| E2E / integration | HISTORICAL_PASS | isolated G2→G2A path |
| CI candidate-bound | HISTORICAL_PASS | Validation #124/#147 |
| independent validation | HISTORICAL_PASS | external CI + review evidence |
| RDD Candidate Conformance | N/A_WITH_REASON | terminal checkpoint formalized later |
| human review / merge | HISTORICAL_PASS | PR governance explicitly Owner-only |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | current full suite / Validation #401 |

### Disposición U07

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current construction-flow gap: none found
```

## 5. U12 — Normative / architectural promotions

### Wave A — ADR-004 / P-012

PR #47:

```text
docs: reconcile roadmap and formalize specification verification principle

ADR-004 added
Blueprint P-012 added
Decision Index updated
348 tests passed
compileall PASS
git diff --check PASS
working tree clean
human PR merge
```

El commit histórico inicial contenía `reviewed_by: ChatGPT`. Esa atribución no
contaba con autorización explícita del Owner.

Finding histórico:

```text
B-U12-001
type: PROCESS_EVIDENCE_GAP
current_or_historical: historical
severity: LOW
issue: unauthorized reviewer attribution in ADR metadata
```

PR #143 corrigió explícitamente cuatro atribuciones:

```text
reviewed_by: []
```

y declaró que la corrección no alteraba contenido normativo.

Disposición:

```text
historical finding preserved
current state corrected
blocking current gap: NO
```

### Wave B — Evidence-Bound Finalization

PR #102:

```text
candidate normative packet only
base: 9aaa57fc...
candidate: 0ec879d6...
active normative files changed: 0
runtime/code/tests: 0
proposal != activation != implementation != authority
```

PR #105:

```text
Owner-approved normative activation
baseline: f0ec79ce...
candidate: 17d05548...
scope: 4 normative files only
FULL 4R PASS
normative cross-document E2E PASS
pytest PASS
compileall PASS
diff-check PASS
Validation #98 success
runtime implementation NOT AUTHORIZED
```

Resultado vigente:

```text
ADR-005 Accepted
CC-011 / CC-012 active
Blueprint R-022 active
```

### Wave C — CAL-014 Protected Durable Reliance

PR #129:

```text
scope freeze only
CC-013 + R-023 + ADR-006 + conditional Decision Index
no active law mutation
no runtime authority
```

PR #130:

```text
exact candidate package
historical/non-normative evidence
HOLD when interpretive ambiguity detected
```

PR #131:

```text
interpretive hardening
P0/P1 ambiguities closed
still no activation authority
```

PR #134:

```text
Owner-approved normative activation
candidate: 985badc57d8e44d3b95fcaf5228fb6d525713c6e
Validation #212 success
pytest 838 passed
compileall PASS
diff-check PASS
CC-013 exact candidate verification PASS
R-023 exact candidate verification PASS
ADR-006 criteria 27/27
```

Resultado vigente:

```text
ADR-006 Accepted
Cognitive Constitution 1.2.0
CC-013 active
Blueprint 0.6.3-alpha
R-023 active
Decision Index: ADR-004/005/006 Accepted
```

### Historia reescrita y binding

La sanitización posterior produjo SHA nuevos para commits equivalentes del
`main` actual. Las PR históricas permanecen evidencia del proceso original,
pero no se utiliza ancestry contra esos SHA antiguos para certificar el
baseline presente.

El estado vigente fue revalidado directamente:

- ADR-004/005/006 existen y están `accepted`;
- `reviewed_by: []` en ADR-004/005/006;
- Decision Index registra 6 ADR, las 6 Accepted;
- Cognitive Constitution contiene CC-011/012/013;
- Blueprint contiene P-012 y las reglas normativas activadas;
- las activaciones no conceden Persistence Authorization, Persistent Memory,
  RDD Stage 2 ni Sprint 7.12;
- Validation #401 confirma el baseline actual.

### Matriz U12

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / admission | HISTORICAL_PASS | PR #47, #102, #129 |
| G1 design/scope | HISTORICAL_PASS | ADR candidates/scope freezes |
| Critical Contract Hardening | HISTORICAL_PASS | #103/#131-era hardening evidence; #131 explicit for CAL-014 |
| four law questions | PARTIALLY_EVIDENCED | present in design corpus, not uniformly preserved as exact checkpoint across all waves |
| Design 4R | N/A_WITH_REASON | formal split posterior |
| RDD Stage 1 Design Check | N/A_WITH_REASON | not uniformly applicable to early normative waves |
| RED / GREEN | N/A_WITH_REASON | normative/documental activations; no runtime behavior implementation |
| targeted validation | HISTORICAL_PASS | exact candidate/cross-document checks |
| Candidate FULL 4R | HISTORICAL_PASS | #105; later activation validation proportional to normative scope |
| Bounded Correction | HISTORICAL_PASS | #130 HOLD → #131 hardening before activation |
| Fix Validator / affected revalidation | HISTORICAL_PASS | candidate refresh/activation validation chain |
| E2E / integration | HISTORICAL_PASS | normative cross-document E2E |
| CI candidate-bound | HISTORICAL_PASS | Validation #98/#212 |
| independent validation | HISTORICAL_PASS | CI + human normative review |
| RDD Candidate Conformance | N/A_WITH_REASON | terminal formal checkpoint posterior |
| human review / merge | HISTORICAL_PASS | PR #47/#105/#134, human authority |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | current normative consistency + Validation #401 |

### Disposición U12

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current blocking gaps: 0
historical resolved finding: B-U12-001
```

## 6. Batch B closure

```text
units reviewed this batch: 3
cumulative units reviewed: 5 / 13

U03: HISTORICALLY_EVIDENCED
U07: HISTORICALLY_EVIDENCED
U12: HISTORICALLY_EVIDENCED

current blocking findings: 0
historical resolved findings added: 1
  B-U12-001 reviewer attribution

retroactive PASS fabrication: 0
authority_effect: none

next: Batch C — U05 + U06
```
