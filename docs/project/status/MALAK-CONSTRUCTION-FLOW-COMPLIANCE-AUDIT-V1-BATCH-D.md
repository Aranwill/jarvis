---
title: MALAK-CONSTRUCTION-FLOW-COMPLIANCE-AUDIT-V1 — Batch D
status: completed
authority: derived_audit
baseline_commit: b1093f291e4a83af779302454485f46f21644801
units:
  - U01
  - U02
  - U04
  - U10
authority_effect: none
remediation_authorized: false
---

# Batch D — Core, runtime, observability and application composition

## 1. Resultado

```text
U01 Core Kernel & capability foundation
→ CURRENT_STATE_REVALIDATED
→ historical process evidence incomplete for current flow
→ current material gap: none found

U02 Conversation & model runtime
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

U04 Observability & runtime performance evidence
→ CURRENT_STATE_REVALIDATED
→ historical process evidence mixed / pre-hardening
→ current material gap: none found

U10 CLI & application composition
→ HISTORICALLY_EVIDENCED
→ current-state revalidation PASS

current blocking findings: 0
historical/process evidence gaps added: 2
authority_effect: none
```

## 2. U01 — Core Kernel & capability foundation

### Evidencia histórica

PR #1 — `feat(kernel): implement Kernel MVP foundation`

```text
base: 6e763c86...
candidate: 38e9f3aa...
merge: 01fac351...

scope:
- Kernel MVP
- automated pytest
- development scripts

evidence:
- tests successful
- Sprint 2B completed
```

El material es real, pero pertenece a una etapa muy anterior al flujo actual.
No conserva evidencia suficiente para reconstruir retrospectivamente:

- Design 4R;
- Critical Contract Hardening;
- bounded correction;
- independent candidate validator;
- candidate-bound CI;
- RDD Stage 1 Candidate Conformance;
- exact post-merge reconciliation.

Aplicar esas obligaciones retroactivamente sería incorrecto.

### Revalidación actual

El baseline actual conserva un Kernel mínimo:

```text
Request
→ empty-input guard
→ Planner.resolve()
→ CapabilityRegistry.get()
→ Capability.execute(Request)
→ Response
```

Propiedades verificadas:

- Planner es determinista y configurable;
- CapabilityRegistry rechaza duplicados;
- Kernel acepta Planner/Registry inyectados;
- Capability recibe `Request` completo;
- Kernel no almacena Memory;
- Kernel no conoce providers/runtimes concretos;
- Kernel no ejecuta persistencia;
- Kernel no contiene lógica de Engineering/Memory/Security específica.

Tests actuales cubren:

```text
kernel response
empty input
capability dispatch
injected planner/registry
planner routing
registry registration/listing
```

Validation #401 revalida el baseline completo en Ubuntu y Windows.

### Finding U01

```text
D-U01-001
type: PROCESS_EVIDENCE_GAP
current_or_historical: historical
severity: INFO
source_of_truth: current construction protocol
divergent_artifact: historical Kernel MVP process record
impact: full current-flow compliance cannot be claimed historically
disposition: CURRENT_STATE_REVALIDATED
remediation_authorized: false
authority_effect: none
```

No se recomienda crear receipts retroactivos ni reescribir Sprint 2B.

### Matriz U01

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / G1 | PARTIALLY_EVIDENCED | MVP scope exists, current formal contract did not exist |
| Critical Contract Hardening | N/A_WITH_REASON | checkpoint posterior |
| four law questions | UNCONFIRMED | not preserved for original MVP |
| Design 4R | N/A_WITH_REASON | posterior |
| RDD Stage 1 Design Check | N/A_WITH_REASON | posterior |
| RED / GREEN | UNCONFIRMED | tests exist, exact TDD sequence not preserved |
| targeted validation | HISTORICAL_PASS | pytest evidence |
| Candidate FULL 4R | N/A_WITH_REASON | posterior |
| Bounded Correction / Fix Validator | UNCONFIRMED | not preserved |
| E2E / integration | PARTIALLY_EVIDENCED | later sprints exercise Kernel end-to-end |
| CI candidate-bound | N/A_WITH_REASON | introduced later |
| human review / merge | HISTORICAL_PASS | PR #1 merged |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | Validation #401 |

### Disposición U01

```text
CURRENT_STATE_REVALIDATED
current construction-flow gap: none found
historical full-flow claim: NOT MADE
```

## 3. U02 — Conversation & model runtime

### Cadena histórica

PR #3 — Ollama runtime:

```text
LLMRuntime abstraction preserved
OllamaRuntime implemented
RuntimeMetrics diagnostic/ephemeral
27 tests PASS
compileall PASS
real execution validation
Kernel independent from concrete runtime
```

PR #13 / Sprint 7.3:

```text
ConversationService
→ ConversationProviderRegistry
→ RuntimeConversationProvider
→ LLMRuntime

74 passed
compileall PASS
diff-check PASS
rollback bounded
Kernel / Planner / Capability unchanged
```

PR #45 / Sprint 7.8:

```text
CLI
→ Kernel
→ Planner
→ CapabilityRegistry
→ ConversationCapability
→ RuntimeConversationProvider
→ LLMRuntime

348 tests PASS
compileall PASS
pip check PASS
diff-check PASS
real Ollama inference PASS
```

PR #56 / Sprint 7.9:

```text
conversation continuity in memory only
365 passed
compileall PASS
diff-check PASS
real runtime PASS
FULL 4R PASS
bounded findings G-R01 / H-R01 closed
no persistent Memory
```

PR #58 / Sprint 7.10:

```text
session isolation
372 tests PASS
compileall PASS
diff-check PASS
post-merge validation PASS
no persistence / RAG / agents / Sandbox
```

### Revalidación actual

`ConversationService`:

- provider resolution only;
- optional bounded in-memory context;
- session-specific history;
- records only successful exchanges;
- provider failure leaves context unchanged;
- no persistence/governance policy.

`InMemoryConversationContext`:

- per-session bounded exchanges;
- session-specific snapshot/clear;
- no global default session;
- no disk write.

`RuntimeConversationProvider` remains a thin adapter over injected `LLMRuntime`.

`OllamaRuntime` currently includes:

- explicit model/prompt validation;
- bounded request/response byte limits;
- network timeout;
- response-shape validation;
- technical metrics only;
- metric persistence only through explicitly injected sink.

### Disposición U02

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current construction-flow gap: none found
```

## 4. U04 — Observability & runtime performance evidence

### Historical waves

PR #3:

```text
RuntimeMetrics
diagnostic + ephemeral
no persistence
no automatic timeout adjustment
27 tests PASS
```

PR #4:

```text
RuntimeMetricSample
InMemory + JSONL stores
technical telemetry only
no prompt/response persistence
real JSONL validation
41 tests PASS
compileall PASS
Kernel unchanged
```

PR #14 / Sprint 7.4:

```text
operational events kept separate from runtime metrics and security audit
append-only JSONL store
strict six-field allowlist
4096-byte line limit
CLI correlation through request_id
main() does not create persistence implicitly

94 focused tests PASS
121 full tests PASS
compileall PASS
diff-check PASS
privacy/security review PASS
rollback PASS
```

The sprint also preserved non-blocking future debt:

- rotation / growth limits;
- retention / deletion;
- concurrency;
- partial corruption recovery;
- file permissions.

Those are product hardening horizons, not construction-flow violations.

### Current-state revalidation

Runtime metrics:

- JSONL samples exclude prompts and generated responses;
- explicit typed reconstruction;
- malformed persisted data fails visibly;
- profiler is pure aggregation;
- profiler does not read stores, invoke runtimes or apply config;
- timeout recommendation is descriptive, not authority.

Operational events:

- separate contract/store from runtime metrics;
- strict allowlisted fields;
- line-size bound;
- no implicit store creation by CLI;
- telemetry does not alter authorization.

Because the earliest runtime-metrics work predates the hardened construction
sequence, the unit cannot be labeled fully historically compliant with the
current flow.

### Finding U04

```text
D-U04-001
type: PROCESS_EVIDENCE_GAP
current_or_historical: historical
severity: INFO
source_of_truth: current construction protocol
divergent_artifact: early runtime metrics implementation history
impact: Design 4R/RDD/candidate-bound stages cannot be reconstructed for the earliest wave
disposition: CURRENT_STATE_REVALIDATED
remediation_authorized: false
authority_effect: none
```

### Matriz U04

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / G1 | PARTIALLY_EVIDENCED | strong Sprint 7.4 record, earlier metric waves predate current flow |
| Critical Contract Hardening | N/A_WITH_REASON | checkpoint posterior |
| four law questions | HISTORICAL_PASS | Sprint 7.4 |
| Design 4R | N/A_WITH_REASON | split posterior |
| RDD Stage 1 Design Check | N/A_WITH_REASON | posterior |
| RED / GREEN | UNCONFIRMED | not uniformly preserved across early waves |
| targeted validation | HISTORICAL_PASS | PR #3/#4/#14 |
| Candidate FULL 4R | UNCONFIRMED | not preserved for early metric waves |
| Bounded Correction / Fix Validator | PARTIALLY_EVIDENCED | Sprint 7.4 incremental gates, not current formal loop |
| E2E / integration | HISTORICAL_PASS | runtime metrics + JSONL; CLI events + JSONL |
| CI candidate-bound | N/A_WITH_REASON | reusable candidate-bound CI introduced later |
| human review / merge | HISTORICAL_PASS | PR #3/#4/#14 |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | Validation #401 |

### Disposición U04

```text
CURRENT_STATE_REVALIDATED
current construction-flow gap: none found
historical full-flow claim: NOT MADE
```

## 5. U10 — CLI & application composition

### Historical foundation

Sprint 7.3 stabilized provider/service/CLI behavior.

Sprint 7.8 moved normal prompts through:

```text
CLI → Kernel.receive(...)
```

Sprint 7.10 made `new` rotate session identity instead of using a global
conversation identity.

### Later Engineering CLI hardening

PR #155 — Adaptive Engineering CLI:

```text
RED candidate 08db7651...
16 expected failures on Ubuntu/Windows

first GREEN: 6900db58...
manual review found blocker:
contextual ConversationService reused by stateless Engineering

corrected GREEN: 86a059df...
1186 tests PASS on Ubuntu/Windows
compile PASS
candidate diff PASS
```

Correction preserved:

- contextual service for Conversation;
- separate stateless service for E2/E3/E4;
- same runtime/provider/model config;
- exact explicit `MALAK_REPOSITORY_ROOT`;
- no implicit cwd fallback;
- capability execution remains behind Kernel.

PR #157 — Read-only Explorer:

```text
RED: 10 expected failures
GREEN: 68bc81fd...
1196 tests PASS Ubuntu/Windows
compile PASS
candidate diff PASS

/explore is deterministic
no LLM call
no Engineering capability execution
no write authority
same captured repository/knowledge readers
```

### Current-state revalidation

`composition.py` currently composes:

```text
Conversation Kernel
+
EngineeringKernelSet
  ├─ one GitRepositoryReader snapshot
  ├─ one GovernedKnowledgeReader
  ├─ one structural projection for inspect only
  └─ fixed Kernel/Planner per E2/E3/E4 capability
```

Tests freeze:

- one exact Engineering baseline;
- same repository/knowledge readers across E2/E3/E4;
- structural projection only for inspect;
- later Git HEAD movement does not mutate captured baseline.

CLI tests freeze:

- runtime/provider configuration;
- conversation routing through Kernel;
- session continuity and `new`;
- explicit repository root only;
- Engineering stateless service;
- malformed `/engineering` fails closed;
- malformed `/explore` fails closed;
- Explorer never falls back to Conversation;
- Engineering/Explorer status reports captured baseline;
- correlated operational events;
- started-event failure blocks execution;
- final-event failure does not erase a valid result.

### Matriz U10

| Etapa actual | Estado auditado | Evidencia / razón |
| --- | --- | --- |
| G0 / G1 | HISTORICAL_PASS | Sprint 7.3/7.8/7.10 + E5 designs |
| Critical Contract Hardening | HISTORICAL_PASS | #155 manual blocker + corrected candidate, #157 boundaries |
| four law questions | HISTORICAL_PASS | preserved across sprint/E5 designs |
| Design 4R | PARTIALLY_EVIDENCED | later E5 design/reviews, formal split evolved over time |
| RDD Stage 1 Design Check | PARTIALLY_EVIDENCED | later E5 units candidate-bound |
| RED | HISTORICAL_PASS | #155/#157 |
| GREEN | HISTORICAL_PASS | corrected/final candidates |
| targeted validation | HISTORICAL_PASS | CLI/composition focused tests |
| Candidate FULL 4R | HISTORICAL_PASS | later E5 units / sprint final reviews |
| Bounded Correction | HISTORICAL_PASS | #155 first GREEN blocker corrected |
| Fix Validator / affected revalidation | HISTORICAL_PASS | corrected candidate cross-platform CI |
| E2E / integration | HISTORICAL_PASS | CLI→Kernel path, Engineering command surfaces |
| CI candidate-bound | HISTORICAL_PASS | #155/#157 |
| independent validation | HISTORICAL_PASS | CI + manual runtime review |
| human review / merge | HISTORICAL_PASS | Draft/Owner-only boundaries preserved |
| post-merge/current validation | CURRENT_REVALIDATION_PASS | Validation #401 |

### Disposición U10

```text
HISTORICALLY_EVIDENCED
current-state revalidation: PASS
current construction-flow gap: none found
```

## 6. Batch D closure

```text
units reviewed this batch: 4
cumulative units reviewed: 11 / 13

U01: CURRENT_STATE_REVALIDATED
U02: HISTORICALLY_EVIDENCED
U04: CURRENT_STATE_REVALIDATED
U10: HISTORICALLY_EVIDENCED

current blocking findings: 0
historical/process evidence gaps added:
- D-U01-001
- D-U04-001

retroactive receipts created: 0
runtime remediation performed: 0
authority_effect: none

next gate:
Batch E — U08 + U09
NOT STARTED
requires separate owner advance
```
