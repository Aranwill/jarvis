---
title: Malāk U007-F05 — Kernel Instance Architecture Clarification — G0/G1 Design
status: proposed
authority: non_normative
document_role: architecture_clarification_design
language: es
created: 2026-09-27
baseline_commit: 785bf3230e82339555405e155b89e33e47efb78e
finding_id: U007-F05
source_run_id: bootstrap-u01-20260926-007
risk_class: 2
architecture_change: clarification_only
critical_contract_change: false
implementation_authorized: false
normative_promotion_authorized: false
runtime_execution_authorized: false
eighth_u01_authorized: false
self_modification_authorized: false
authority_effect: none
related:
  - docs/project/status/MALAK-SEVENTH-U01-UNRESOLVED-CLASSIFICATION-AUDIT-20260927.md
  - docs/architecture/blueprint.md
  - docs/architecture/kernel.md
  - docs/architecture/architecture_quality_gates.md
  - docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
  - src/malak/app/composition.py
  - docs/development/malak_construction_protocol.md
---

# Malāk U007-F05 — Kernel Instance Architecture Clarification — G0/G1 Design

## 1. Propósito

Cerrar mediante diseño la ambigüedad documental detectada por Seventh U01:

~~~text
U007-F05
multiple Kernel instances
-> B — genuine documentation / normative ambiguity
~~~

Pregunta de diseño:

~~~text
¿La arquitectura de Malāk exige una única instancia técnica de Kernel,
o exige una única responsabilidad / frontera lógica de Kernel?
~~~

Este gate no cambia producción.

No modifica todavía:

~~~text
docs/architecture/kernel.md
docs/architecture/blueprint.md
src/malak/**
tests/**
Evidence Focus
E3
runtime
~~~

## 2. Baseline

~~~text
repository:
Aranwill/jarvis

branch:
main

baseline:
785bf3230e82339555405e155b89e33e47efb78e
~~~

PR #203 quedó integrada sin drift.

No existen PRs abiertas al momento de abrir este gate.

## 3. Trigger verificable

Seventh U01 produjo un finding UNRESOLVED sobre:

~~~text
EngineeringKernelSet
-> multiple Kernel instances
~~~

La auditoría posterior clasificó ese finding como:

~~~text
B — genuine documentation / normative ambiguity
~~~

y no como:

~~~text
A — genuine current architecture gap
~~~

La evidencia actual no justifica cambiar código.

Sí justifica aclarar semántica arquitectónica.

## 4. Estado implementado actual

La composición actual contiene:

~~~text
EngineeringKernelSet
-> kernels: dict[str, Kernel]
~~~

Cada superficie Engineering se construye mediante:

~~~text
Capability
+ CapabilityRegistry(exactly one capability)
+ Planner(capability_name=exact capability)
-> Kernel
~~~

La implementación comparte entre esas superficies:

~~~text
one GitRepositoryReader
one captured baseline
one GovernedKnowledgeReader
one ConversationService
one provider/model configuration
one RuntimeGenerationContract
~~~

No existe evidencia de:

~~~text
separate authority domains
separate persistent state
separate Memory ownership
separate policy ownership
separate architectural Kernel specifications
~~~

## 5. Intención histórica ya preservada

E5 Engineering CLI documentó explícitamente:

~~~text
one fixed Kernel per capability
~~~

y:

~~~text
/engineering inspect
-> Kernel[engineering_inspect]

/engineering analyze
-> Kernel[engineering_analyze]

/engineering propose
-> Kernel[engineering_propose]
~~~

Razón:

~~~text
CLI command routing
!= capability execution bypass

every capability
-> Kernel.receive(...)
~~~

Por tanto la multiplicidad técnica ya fue deliberada.

El problema es que esa intención vive en un design record no normativo,
mientras la Kernel Specification habla conceptualmente de:

~~~text
the Kernel
Malāk Kernel
Kernel First
~~~

sin declarar la semántica de cardinalidad.

## 6. Jerarquía documental

AGENTS.md establece:

~~~text
1. Cognitive Constitution
2. Governance Constitution
3. Blueprint
4. approved specifications, including Kernel Specification
5. accepted ADRs
...
~~~

Por tanto:

~~~text
Blueprint
-> define principios y responsabilidades generales

Kernel Specification
-> owner correcto de semántica específica del Kernel

E5 design
-> evidencia histórica de intención
-> no autoridad normativa
~~~

## 7. G0 — inventario material del problema

Fuentes de máxima relevancia:

| Fuente | Clase | Relevancia | Disposición |
|---|---|---:|---|
| Cognitive Constitution | normativa | límites de cognición/autoridad | ADOPT |
| Governance Constitution | normativa | Human in Control / authority | ADOPT |
| Blueprint | arquitectura maestra | Kernel First / Capability First | ADOPT |
| Kernel Specification | especificación aprobada | semántica concreta del Kernel | ADAPT |
| Architecture Quality Gates | arquitectura | Kernel small/stable/deterministic | ADOPT |
| E5 Engineering CLI design | histórico no normativo | one fixed Kernel per capability | ADAPT |
| composition.py | implementación actual | múltiples instancias fixed | CURRENT STATE |
| PR #203 audit | derived audit | finding B | INPUT ONLY |

Resultado G0:

~~~text
need demonstrated            YES
production defect proven     NO
architecture contradiction   NO
documentation ambiguity      YES
normative owner identified   YES
~~~

G0:

~~~text
PASS
~~~

## 8. Decisión G1

La interpretación candidata es:

~~~text
Malāk posee una única responsabilidad arquitectónica de Kernel.

Kernel First gobierna:
- ownership;
- responsibilities;
- routing boundary;
- invariants;
- authority separation;
- complexity.

Kernel First NO implica:
- singleton process;
- singleton Python object;
- global mutable Kernel instance.
~~~

Una aplicación puede materializar más de una instancia técnica de Kernel
si cada instancia:

~~~text
implements the same Kernel contract
remains small and deterministic
contains no business logic
owns no persistent state
owns no independent authority
owns no independent policy
does not bypass Capability routing
does not create a separate architectural Kernel
~~~

La cardinalidad de objetos no cambia la cardinalidad de la responsabilidad
arquitectónica.

## 9. Definiciones propuestas

### 9.1 Logical Core Kernel

~~~text
Logical Core Kernel
=
the single architectural responsibility and invariant boundary
defined by Blueprint + Kernel Specification
~~~

No describe necesariamente una instancia única en memoria.

### 9.2 Kernel instance

~~~text
Kernel instance
=
a concrete runtime/application object implementing the Kernel contract
for a bounded composition surface
~~~

Una instancia:

~~~text
!= separate architectural Kernel
!= new authority domain
!= new governance domain
!= new cognitive center
~~~

### 9.3 Fixed Kernel instance

Para el patrón Engineering actual:

~~~text
fixed Kernel instance
=
Kernel object composed with
one deterministic Planner
+
one CapabilityRegistry
bound to exactly one capability
~~~

Su propósito es preservar:

~~~text
Capability execution
through
Kernel.receive(...)
~~~

sin introducir routing cognitivo adicional.

## 10. Invariantes normativas candidatas

La futura aclaración de Kernel Specification deberá expresar como mínimo:

~~~text
KIC-01
Kernel First is responsibility-centric, not singleton-object-centric.

KIC-02
Multiple concrete Kernel instances MAY exist at application composition
boundaries when they implement the same Kernel contract.

KIC-03
Such instances MUST NOT create independent authority, policy, memory,
business logic or persistent state.

KIC-04
Instance multiplicity MUST NOT bypass Capability First or Kernel.receive(...).

KIC-05
Instance multiplicity MUST NOT imply multiple architectural Core Kernels.

KIC-06
Any instance that adds divergent responsibility, policy, authority,
state ownership or hidden routing requires a separate architecture gate.

KIC-07
Kernel responsibility remains small, stable and deterministic.
~~~

## 11. Qué NO se está decidiendo

Este gate no decide:

~~~text
how many Kernel instances future Malāk should use
whether one global Kernel would be better
whether EngineeringKernelSet should be refactored
whether Planner should become shared
whether CapabilityRegistry should become shared
whether current class name EngineeringKernelSet should change
~~~

Tampoco decide:

~~~text
agents
scheduler
orchestrator
execution layer
future Capability Manager implementation
~~~

## 12. Blueprint disposition

Blueprint ya define:

~~~text
P-001 Kernel First
P-004 Capability First
P-005 Human in Control
P-011 Runtime Independence
~~~

y describe Kernel como responsabilidad arquitectónica.

No declara cardinalidad de objetos.

Por tanto:

~~~text
Blueprint change:
NOT REQUIRED
~~~

Razón:

~~~text
the clarification does not alter a Blueprint principle,
layer, ownership or general architecture shape
~~~

Agregar cardinalidad técnica al Blueprint aumentaría detalle en el documento
equivocado.

## 13. Kernel Specification disposition

Kernel Specification es el owner correcto porque define:

~~~text
what Kernel is
what Kernel owns
what Kernel must not do
~~~

La futura promoción deberá ser mínima y localizada.

Candidate future delta:

~~~text
docs/architecture/kernel.md
ONLY
~~~

Contenido esperado:

~~~text
a short section:
Logical Kernel vs concrete instances

+
explicit invariants KIC-01..KIC-07
or semantically equivalent language
~~~

## 14. ADR / Decision Index disposition

No se introduce una nueva decisión arquitectónica.

Se aclara una decisión ya materializada y compatible con Blueprint.

Por tanto:

~~~text
new ADR:
N/A

Decision Index change:
N/A
~~~

Razón:

~~~text
no new architecture choice
no supersession
no new authority model
no new component
no new ownership
~~~

Si durante futura promoción aparece una decisión nueva:

~~~text
STOP
-> return to G1
-> reevaluate ADR need
~~~

## 15. Architecture Quality Gates

### Gate 1 — Blueprint Compliance

~~~text
PASS
~~~

No cambia Blueprint semantics.

### Gate 2 — Cognitive Constitution

~~~text
PASS
~~~

No cambia cognición.

### Gate 3 — Governance Constitution

~~~text
PASS
~~~

No cambia autoridad.

### Gate 4 — Kernel First

~~~text
PASS
~~~

La aclaración refuerza que Kernel First limita responsabilidad y complejidad.

### Gate 5 — Capability First

~~~text
PASS
~~~

Fixed instances existen precisamente para mantener execution through Kernel
sin absorber capability behavior.

### Gate 6 — Runtime Independence

~~~text
PASS
~~~

La regla no depende de Ollama, modelo ni provider.

### Gate 7 — Human in Control

~~~text
PASS
~~~

No introduce decisiones automáticas.

### Gate 8 — AKS

~~~text
PASS WITH FUTURE KERNEL SPEC UPDATE
~~~

No ADR/Index required unless scope changes.

### Gate 9 — Traceability

~~~text
PASS
~~~

U007-F05 -> PR #203 -> this G0/G1 -> future normative candidate.

### Gate 10 — Release Readiness

~~~text
NOT APPLICABLE TO THIS DESIGN
~~~

No release action.

## 16. Malāk Alignment Matrix

| Fuente | Autoridad | Invariante | Baseline | Disposición | Efecto |
|---|---|---|---|---|---|
| Cognitive Constitution | normativa | Evidence != Authority | unchanged | ADOPT | none |
| Governance Constitution | normativa | Human in Control | unchanged | ADOPT | none |
| Blueprint | architecture master | Kernel First / Capability First | aligned | ADOPT | no Blueprint edit |
| Kernel Specification | approved specification | Kernel responsibility | cardinality ambiguous | ADAPT | clarify semantics |
| Architecture Quality Gates | architecture | small/stable/deterministic Kernel | aligned | ADOPT | explicit guardrails |
| E5 design | non-normative historical | one fixed Kernel per capability | implemented | ADAPT | promote intent only |
| composition.py | implementation | fixed Kernel instances | current | ADOPT AS EVIDENCE | no code change |
| PR #203 audit | derived | U007-F05=B | current finding | OBSERVE/INPUT | no authority |

Separación:

~~~text
historical design
!= normative truth

current code
!= architecture authority

derived audit
!= architecture authority
~~~

## 17. Four Questions of Law

### 17.1 Blueprint

~~~text
PASS
~~~

La interpretación es consistente con Kernel First y Capability First.

### 17.2 Cognitive Constitution

~~~text
PASS
~~~

No altera generación, finalización, evidencia ni cognición.

### 17.3 Governance Constitution

~~~text
PASS
~~~

No cambia Human in Control ni autoridad.

### 17.4 Kernel complexity

~~~text
PASS
~~~

No agrega responsabilidad ni código al Kernel.

## 18. Design 4R

### Risk

~~~text
PASS
~~~

Riesgo principal:

~~~text
clarification accidentally legitimizes arbitrary Kernel proliferation
~~~

Mitigación:

~~~text
KIC-02..KIC-06 constrain multiplicity
instance count alone != justification
divergent responsibility -> new gate
~~~

### Readability

~~~text
PASS
~~~

Se separan explícitamente:

~~~text
logical responsibility
vs
concrete instance
~~~

### Reliability

~~~text
PASS
~~~

La aclaración corresponde con:

~~~text
current code
E5 design
Blueprint principles
Quality Gates
~~~

sin inventar una arquitectura nueva.

### Resilience

~~~text
PASS
~~~

Future drift queda fail-closed:

~~~text
new independent authority/state/policy/routing
-> clarification no longer sufficient
-> separate architecture gate required
~~~

## 19. Critical Contract Hardening

Disposition:

~~~text
N/A
~~~

Reason:

~~~text
this gate does not alter an executable contract,
public API, parser, authority boundary, evidence contract,
runtime contract or acceptance semantics
~~~

Evidence:

~~~text
future candidate is documentation-only
production delta = 0
~~~

La aclaración sigue siendo material por autoridad documental y por eso conserva:

~~~text
Four Questions
Design 4R
RDD Stage 1
candidate-bound CI
human review
~~~

## 20. RED / GREEN

### RED

~~~text
N/A
~~~

Reason:

~~~text
no executable behavior is introduced or changed
~~~

### GREEN

~~~text
N/A
~~~

Reason:

~~~text
no production implementation exists for this clarification
~~~

La futura promoción normativa deberá validarse por:

~~~text
document diff review
full regression CI
architecture consistency review
candidate-bound evidence
~~~

## 21. RDD Stage 1 Design Check

~~~text
candidate identity strategy            PASS
baseline/candidate binding             PASS
evidence provenance                    PASS
Writer/Reviewer/Validator separation   PASS
human Authority separation             PASS
PASS/FAIL/INCONCLUSIVE discipline      PASS
candidate change invalidation          PASS
bounded correction semantics           PASS
authority_effect                       none
RDD Stage 2                             NOT AUTHORIZED
~~~

Resultado:

~~~text
PASS
~~~

## 22. Future normative promotion scope

Una futura promoción, si el Owner la autoriza, queda congelada a:

~~~text
allowed:
docs/architecture/kernel.md

forbidden:
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/architecture/decisions/decision-index.md
docs/architecture/adr/**
src/**
tests/**
SECURITY.md
governance constitutions
Evidence Focus
E3
runtime
~~~

Expected delta:

~~~text
documentation clarification only
architecture shape unchanged
runtime behavior unchanged
authority unchanged
~~~

## 23. Future candidate acceptance criteria

El candidate normativo futuro deberá demostrar:

~~~text
A01
Kernel remains one logical architectural responsibility.

A02
Multiple concrete instances do not imply multiple architectural Kernels.

A03
Multiple instances are allowed only as bounded composition mechanisms.

A04
No independent authority/state/policy/business logic is granted.

A05
Capability execution remains through Kernel.receive(...).

A06
Any divergent responsibility requires a new architecture gate.

A07
Blueprint remains unchanged because no principle changes.

A08
ADR/Decision Index remain unchanged because no new decision is introduced.

A09
production delta = 0.

A10
authority_effect = none.
~~~

## 24. Correction budget

Future normative candidate:

~~~text
maximum bounded correction rounds:
2
~~~

Corrections may only address:

~~~text
wording ambiguity
internal contradiction
unintended scope expansion
traceability omission
~~~

If a correction requires:

~~~text
Blueprint change
ADR creation
code change
Kernel behavior change
Planner behavior change
authority change
~~~

then:

~~~text
STOP
-> scope invalidated
-> return to G1
~~~

## 25. E3 / epistemic calibration boundary

Este gate NO modifica E3.

U007-F04 y U007-F06 permanecen separados.

Orden obligatorio:

~~~text
U007-F05 architecture semantics
first

then
U007-F04 + U007-F06 epistemic calibration
~~~

Razón:

~~~text
do not tune Analyze around an unresolved governing ambiguity
~~~

## 26. Runtime boundary

No se autoriza:

~~~text
runtime execution
Eighth U01
retry of run 007
forced E4 runtime coverage
~~~

Run 007 permanece:

~~~text
INCONCLUSIVE
~~~

## 27. G0/G1 disposition

~~~text
G0                              PASS
G1                              PASS
Architecture Quality Gates      PASS
Four Questions of Law           PASS
Design 4R                       PASS
Critical Contract Hardening     N/A — no executable/authority contract delta
RDD Stage 1 Design Check        PASS
RED                             N/A — documentation-only future promotion
GREEN                           N/A — documentation-only future promotion

normative promotion             NOT AUTHORIZED
Kernel Specification edit       NOT AUTHORIZED
production implementation       NOT AUTHORIZED
E3 correction                   NOT AUTHORIZED
runtime execution               NOT AUTHORIZED
Eighth U01                      NOT AUTHORIZED
self-modification               NOT AUTHORIZED
authority_effect                none
~~~

## 28. Next lawful transition

~~~text
candidate-bound CI for this G0/G1 design
-> Owner human review
-> Owner merge
-> separate explicit authorization
   for normative promotion to docs/architecture/kernel.md
~~~
