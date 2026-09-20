---
title: MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 — Batch E
status: completed
authority: derived_audit
baseline_commit: b1093f291e4a83af779302454485f46f21644801
units:
  - U08
  - U09
authority_effect: none
remediation_authorized: false
---

# Batch E — Engineering Intelligence and Repository Structural Evidence

## 1. Resultado

```text
U08 Engineering E0–E4 evidence path
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

U09 Repository structural evidence
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

current blocking findings: 0
authority expansion found: 0
write/side-effect expansion found: 0
silent S propagation to E3/E4: 0
retroactive PASS fabrication: 0
```

## 2. U08 — Engineering E0–E4 evidence path

U08 comprende la cadena:

```text
E0 Repository Read
→ E1 Governed Knowledge Read
→ E2 Engineering Inspect
→ E3 Engineering Analyze
→ E4 Engineering Propose
```

La cadena conserva una separación progresiva:

```text
read
!= classified knowledge
!= inspection
!= analysis
!= proposal
!= authorization
!= implementation
```

### E0 — Repository Read

PR #147:

```text
title: feat(e0): add hardened commit-bound repository reader

baseline:
39366da01f793cf8f5d3856c47457954ee758925

candidate:
31a33d13623298cc70c534d5f8352bbf0a58ca25

merge:
a91bca0bcf8c0bc2c3972497b034e19b9f7eda7a
```

RED:

```text
Ubuntu:  16 failed / 922 passed
Windows: 16 failed / 922 passed
```

GREEN/final:

```text
969 passed
compileall PASS
diff check PASS
candidate identity PASS
Validation run 285 / 35405118096: success
```

FULL 4R:

```text
Risk         PASS
Readability  PASS
Reliability  PASS
Resilience   PASS
```

Current contract:

- captures one exact Git HEAD;
- captures its tree;
- later worktree/staged/untracked/HEAD changes do not alter the view;
- reads exact captured blob object IDs;
- hard resource ceilings cannot be raised by caller configuration;
- rejects invalid root/path/query/budget conditions;
- read-only;
- repository content does not become authority.

### E1 — Governed Knowledge Read

PR #148:

```text
baseline:
a91bca0bcf8c0bc2c3972497b034e19b9f7eda7a

candidate:
6cf561d9fc5d9471efa97aeffd444fe8ee92e418

merge:
50a80babeca4367a20dd7f730ef2c536c87a9d08
```

RED:

```text
Ubuntu:  30 failed / 969 passed
Windows: 30 failed / 969 passed
```

GREEN/final:

```text
1003 passed
compileall PASS
diff check PASS
candidate identity PASS
Validation run 297 / 35441384389: success
```

Current contract:

```text
source_class != authority
authority_class != authorization
document role != snapshot authority
captured commit != trusted baseline
policy != authority
```

E1:

- composes over E0;
- preserves baseline/path/blob provenance;
- classifies documentary role only;
- does not parse source content to infer permission;
- fails if E0/E1 binding drifts.

### E2 — Engineering Inspect

PR #149:

```text
baseline:
50a80babeca4367a20dd7f730ef2c536c87a9d08

RED:
5ea8f7a1880e023988a17cb401a28d1517771edb

final candidate:
91412656b0c6bcbda8a84b3ab6642d0e2a5760e1

merge:
d0e205d3e19acf80ba8f110a2ea76c77bd6c0581

Validation run 309 / 35442478656: success
```

Final validation:

```text
1047 passed Ubuntu
1047 passed Windows
compileall PASS
diff check PASS
candidate identity PASS
```

Current contract:

- E0/E1 must share baseline;
- deterministic evidence collection before inference;
- no evidence → `UNCONFIRMED` and zero model call;
- at most one stateless model inference;
- evidence packet is untrusted data, not instructions;
- references R/K/S are validated fail-closed;
- no tools, agents, execution loop, repository writes or session persistence;
- `authority_effect: none`.

Historical hardening preserved a fixture finding where `K1` was cited without
Knowledge evidence; only the test fixture was corrected and the complete
validation reran.

### E3 — Engineering Analyze

PR #150:

```text
baseline:
d0e205d3e19acf80ba8f110a2ea76c77bd6c0581

candidate:
79fca79d24e1ee30c96aacd470e3267802aa1f77

merge:
c48b72b7af95f1edc9bcd357f64aeb9d5a34f5c8

Validation run 324 / 35445357957: success
```

Final validation:

```text
1114 passed Ubuntu
1114 passed Windows
compileall PASS
diff check PASS
candidate identity PASS
```

Current contract:

- shared deterministic evidence collector with E2;
- truncated evidence → `UNCONFIRMED`;
- structured findings only;
- generated ref-like tokens cannot create evidence;
- relational findings require valid repository + knowledge refs;
- no proposal or execution;
- `finding != authorization`;
- `authority_effect: none`.

### E4 — Engineering Propose

PR #152:

```text
baseline:
f0362ef77d06ce7852851345295f374c57f4ddd3

RED:
2cc25d07...

final candidate:
3463f1c391f6a11de70a0d6ecfc37c4127da21cb

merge:
14122dd2d0c94d1c2d5ba1a68b6ae43bcb1c2c9e

Validation #330 / 35449064313: success
```

RED:

```text
54 expected E4 failures
1114 pre-E4 tests remain PASS
```

GREEN:

```text
1168 passed Ubuntu
1168 passed Windows
compileall PASS
candidate identity PASS
candidate diff PASS
```

Current contract:

- proposal is generated only from actionable grounded analysis;
- UNCONFIRMED / UNRESOLVED / CONTRADICTION do not call proposal model;
- ALIGNED-only produces no proposal;
- finding/evidence refs are strictly validated;
- generated text cannot inject reserved refs;
- proposal includes bounded validation plan, risks and assumptions;
- no Planner/CLI/tools/Git/sandbox/agent/write execution authority;
- proposal returns to Owner;
- `Evidence != Authority`;
- `Finding != Authorization`.

### Matriz U08

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / admission | HISTORICAL_PASS | E0/E1/E2/E3/E4 G0/G1 designs |
| G1 design | HISTORICAL_PASS | bounded designs per capability |
| Critical Contract Hardening | HISTORICAL_PASS | fail-closed/hard ceilings/authority laundering controls |
| four law questions | HISTORICAL_PASS | preserved in designs/reviews |
| Design 4R | PARTIALLY_EVIDENCED | designs predate formal split but design reviews exist |
| RDD Stage 1 Design Check | PARTIALLY_EVIDENCED | candidate-bound evidence used; formal terminal checkpoint evolved later |
| RED | HISTORICAL_PASS | exact RED candidates / expected failures |
| GREEN | HISTORICAL_PASS | exact GREEN candidates |
| targeted validation | HISTORICAL_PASS | capability-specific suites |
| Candidate FULL 4R | HISTORICAL_PASS | PR #147–#152 evidence |
| Bounded Correction | HISTORICAL_PASS | E2 fixture correction, E3 hardening iterations |
| Fix Validator / affected revalidation | HISTORICAL_PASS | complete CI reruns |
| E2E / integration | HISTORICAL_PASS | E0→E1→E2→E3→E4 boundaries tested incrementally |
| CI candidate-bound | HISTORICAL_PASS | Validation #285/#297/#309/#324/#330 |
| independent validation | HISTORICAL_PASS | Ubuntu + Windows candidate workflows |
| RDD Candidate Conformance | PARTIALLY_EVIDENCED | structured candidate evidence predates current explicit checkpoint |
| human review / merge | HISTORICAL_PASS | Draft and Owner-only merge preserved |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | Validation #401 on current main |

### Disposición U08

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current construction-flow gap: none found
```

## 3. U09 — Repository Structural Evidence

U09 comprises:

```text
Repository Structural Projection V0
→ Repository Structural Lookup V0
→ E2 Structural Evidence Integration V0
→ E2 Structural Evidence Observability V0
```

The following remain outside the implemented unit:

```text
Structural Delta
→ DEFERRED

E2 Structural Evidence Evaluation Pack V0
→ DESIGN ONLY
→ RED NOT AUTHORIZED
→ GREEN NOT AUTHORIZED
```

Neither is classified as a current gap.

### Structural Projection V0

Design PR #163:

```text
G0 PASS
design admitted
RED NOT AUTHORIZED at design merge
GREEN NOT AUTHORIZED at design merge
runtime delta 0
```

Implementation PR #164:

```text
baseline:
2e5f97aac41804461ceadd81680762b9e2313d13

candidate:
51b9d465674ad8443adf11bee44385bf52e6e8d1

merge:
a1028f626cdca2da9979002a21d70645ed848e3e

Validation run 362 / 35519024017: success
```

RED:

```text
expected failure: repository_structure module absent
1196 pre-existing tests PASS on Ubuntu/Windows
```

Current contract/tests freeze:

- projection baseline-bound to E0;
- deterministic projection/digest;
- working tree/staged/untracked ignored;
- captured reader does not move when HEAD advances;
- exact module/symbol/import syntax facts;
- no semantic dependency inference;
- syntax error fails without partial projection;
- stable ordering;
- hard file/byte/fact ceilings;
- no authority/execution fields;
- no DB/cache/index/network/LLM/write.

### Structural Lookup V0

Design PR #165:

```text
G0 PASS
Structural Lookup admitted
Structural Delta deferred
runtime delta 0
```

Implementation PR #166:

```text
candidate:
75172332201abca62b0dab7399029d17cc368206

merge:
2a00a16618a7f11403edd06f051fd8cbb68849ed

Validation run 367 / 35520935651: success
```

Current contract/tests freeze:

- exact symbol lookup only;
- exact module symbols/imports only;
- missing exact symbol → None;
- duplicate exact symbol → fail closed;
- blank/non-string query rejected;
- stable source order;
- no projection mutation;
- no I/O;
- no fuzzy/substring/ranking/semantic resolution;
- no authority/scoring surface.

### E2 Structural Evidence Integration V0

Design PR #167:

```text
G0 PASS
integration admitted
Structural Delta deferred
RED/GREEN still Owner-only
```

Implementation PR #168:

```text
candidate:
5e28b9a3171eeb5132f5573f5b230b5c6103a599

merge:
79319eef23cdd1490531d01de914712811135d9d

Validation #375 / 35523380281: success
```

Current contract:

- optional `RepositoryStructuralProjection` only on E2 Inspect;
- E0/E1/S baseline exact-match required;
- exact `RepositoryStructuralLookup`;
- max 12 structural refs;
- truncation explicit;
- R=K=S=0 → UNCONFIRMED and zero provider calls;
- S reports syntax only;
- S != semantic dependency;
- S != architecture assessment;
- S != authority.

Composition creates one structural projection from the same
`GitRepositoryReader` snapshot and injects it only into E2.

### E2 Structural Evidence Observability V0

Design PR #169:

```text
G0 PASS
observability admitted
metrics != authority
Structural Delta remains deferred
```

Implementation PR #170:

```text
candidate:
ac4438e1094871a974275f3fb6a0f441e7016d5b

merge:
5c942d27ea610873182ded77b85d0364bfbe15a0

Validation #380 / 35532873672: success
```

Signals:

```text
repository_evidence_count
knowledge_evidence_count
structural_evidence_count

repository_citation_count
knowledge_citation_count
structural_citation_count

model_inference_count
context_truncated
```

Current semantics:

```text
citation != semantic use
citation != causal contribution
citation != correctness
evidence availability != usefulness
observability != evaluation
observability != authority
```

No telemetry service, DB, registry, persistent history or additional model call
was introduced.

### Structural propagation check — current baseline

Repository search over `src/malak/**`:

```text
structural_projection
→ app/composition.py
→ capabilities/engineering_inspect.py

structural_evidence_count
→ engineering_inspect.py only

structural_citation_count
→ engineering_inspect.py only

RepositoryStructuralLookup
→ repository_structure_lookup.py
→ engineering_inspect.py
```

Therefore:

```text
E3 Analyze structural propagation: 0
E4 Propose structural propagation: 0
```

This matches the admitted scope.

### Evaluation Pack boundary

Current design file:

`MALAK-E2-STRUCTURAL-EVIDENCE-EVALUATION-PACK-V0-G0-G1-DESIGN.md`

records:

```text
G0 PASS
G1 ADMITTED
Design 4R PASS
RDD Stage 1 Design Check PASS

RED NOT AUTHORIZED
GREEN NOT AUTHORIZED

Candidate FULL 4R PENDING
E2E/CI PENDING
RDD Candidate Conformance PENDING
Owner Ready/Merge OWNER ONLY
```

No evaluation dataset or runner exists in baseline. The audit does not promote
this design into implemented state.

### Matriz U09

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / admission | HISTORICAL_PASS | PR #163/#165/#167/#169 |
| G1 design | HISTORICAL_PASS | four bounded designs |
| Critical Contract Hardening | HISTORICAL_PASS | syntax-vs-semantics, exact lookup, no authority, no telemetry expansion |
| four law questions | HISTORICAL_PASS | design contracts preserve Blueprint/Governance/Kernel simplicity |
| Design 4R | PARTIALLY_EVIDENCED | formal split introduced at Evaluation Pack; implementation designs still reviewed |
| RDD Stage 1 Design Check | PARTIALLY_EVIDENCED | later explicit checkpoint; earlier U09 units candidate-bound but not relabeled |
| RED | HISTORICAL_PASS | #164/#166/#168/#170 |
| GREEN | HISTORICAL_PASS | exact implementation candidates |
| targeted validation | HISTORICAL_PASS | dedicated structural/E2 suites |
| Candidate FULL 4R | HISTORICAL_PASS | implementation reviews |
| Bounded Correction | N/A_WITH_REASON | no blocking correction loop required by final U09 candidates |
| Fix Validator / affected revalidation | N/A_WITH_REASON | no in-candidate blocking correction requiring separate fix actor |
| E2E / integration | HISTORICAL_PASS | projection→lookup→E2 integration→observability |
| CI candidate-bound | HISTORICAL_PASS | Validation #362/#367/#375/#380 |
| independent validation | HISTORICAL_PASS | Ubuntu + Windows |
| RDD Candidate Conformance | PARTIALLY_EVIDENCED | explicit terminal checkpoint formalized later |
| human review / merge | HISTORICAL_PASS | Owner-only boundaries preserved |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | Validation #401 |

### Disposición U09

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS

Structural Delta:
DEFERRED by design, not a gap

Evaluation Pack:
DESIGN ONLY, not implemented, not misrepresented

current construction-flow gap:
none found
```

## 4. Current baseline revalidation

Validation #401:

```text
run_id: 35535754638
event: push
HEAD: b1093f291e4a83af779302454485f46f21644801

Ubuntu:
candidate identity PASS
tests PASS
compile PASS
candidate diff PASS

Windows:
candidate identity PASS
tests PASS
compile PASS
candidate diff PASS
```

Exact historical candidate workflows recovered:

```text
E0   31a33d13...  Validation #285  success
E1   6cf561d9...  Validation #297  success
E2   91412656...  Validation #309  success
E3   79fca79d...  Validation #324  success
E4   3463f1c3...  Validation #330  success

Projection     51b9d465... Validation #362 success
Lookup         75172332... Validation #367 success
Integration    5e28b9a3... Validation #375 success
Observability  ac4438e1... Validation #380 success
```

## 5. Gate E closure

```text
units reviewed this batch: 2
cumulative units reviewed: 13 / 13

U08: HISTORICALLY_EVIDENCED
U09: HISTORICALLY_EVIDENCED

current blocking findings: 0
historical/process evidence gaps added: 0
authority escalation found: 0
write expansion found: 0
silent structural propagation found: 0

retroactive PASS fabrication: 0
runtime remediation performed: 0
authority_effect: none

Gate E: CLOSED

next:
Gate F — cross-unit reconciliation + final report
NOT STARTED
requires separate Owner advance
```
