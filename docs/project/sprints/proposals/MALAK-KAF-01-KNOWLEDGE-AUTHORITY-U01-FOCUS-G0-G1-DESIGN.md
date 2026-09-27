---
title: Malāk KAF-01 — Knowledge Authority / U01 Focus Fidelity — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation_design
language: es
created: 2026-09-27
baseline_commit: 48da0bb9c69bacee1088bf05ac9499de07115da6
finding_id: PREREQUISITE-KAF-01
risk_class: 3
critical_contract: true
implementation_authorized: false
red_authorized: false
green_authorized: false
runtime_execution_authorized: false
eighth_u01_authorized: false
self_modification_authorized: false
authority_effect: none
related:
  - AGENTS.md
  - docs/architecture/kernel.md
  - docs/project/sprints/proposals/MALAK-E1-GOVERNED-KNOWLEDGE-READ-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-GOVERNED-ENGINEERING-EVIDENCE-FOCUS-V0-G0-G1-DESIGN.md
  - docs/project/sprints/proposals/MALAK-U007-F04-F06-E3-EPISTEMIC-CALIBRATION-G0-G1-DESIGN.md
  - src/malak/knowledge/knowledge_reader.py
  - src/malak/capabilities/_engineering_analysis.py
  - src/malak/capabilities/_engineering_evidence.py
---

# Malāk KAF-01 — Knowledge Authority / U01 Focus Fidelity — G0/G1 Design

## 1. Propósito

Cerrar el prerrequisito detectado durante U007-F04/F06:

~~~text
PREREQUISITE-KAF-01
Knowledge Authority / U01 Focus fidelity
~~~

Problema compuesto:

~~~text
A. docs/architecture/kernel.md
   is an approved specification by repository hierarchy

   but E1 currently classifies it as:
   ARCHITECTURE_REFERENCE / reference

B. U01 Core Kernel focus
   does not require docs/architecture/kernel.md

   so focus_complete == true
   does not guarantee Kernel Specification presence
~~~

Este gate diseña la corrección.

No implementa todavía.

## 2. Baseline

~~~text
repository:
Aranwill/jarvis

main:
48da0bb9c69bacee1088bf05ac9499de07115da6
~~~

Estado relevante:

~~~text
PR #205
-> Kernel Specification v0.6.1-alpha
-> KIC-01..KIC-07 integrated

PR #206
-> E3 epistemic calibration G0/G1 integrated
-> Eighth U01 blocked on KAF-01
~~~

## 3. Fuente de autoridad documental

AGENTS.md establece precedencia:

~~~text
1. Cognitive Constitution
2. Governance Constitution
3. Blueprint
4. approved specifications, including Kernel Specification
5. Accepted ADRs
...
~~~

Por tanto:

~~~text
Kernel Specification
!= generic architecture reference

Kernel Specification
!= same authority tier as Blueprint
~~~

La representación E1 actual pierde esa distinción.

## 4. Estado E1 actual

E1 define:

~~~text
GOVERNING / normative
-> Cognitive Constitution
-> Governance Constitution
-> Blueprint

ARCHITECTURE_REFERENCE / reference
-> other admitted docs/architecture/**
~~~

Como kernel.md cae en el segundo grupo:

~~~text
docs/architecture/kernel.md
-> ARCHITECTURE_REFERENCE / reference
~~~

Esto contradice su rol aprobado en la jerarquía documental.

## 5. Estado U01 Focus actual

U01 required knowledge incluye:

~~~text
Blueprint
Architecture Quality Gates
Cognitive Constitution
Governance Constitution
Governed Self-Review Bootstrap Task
Construction Flow Audit Batch D
~~~

No incluye:

~~~text
docs/architecture/kernel.md
~~~

El supplemental search usa:

~~~text
Kernel
Capability First
Kernel First
~~~

pero supplemental:

~~~text
is bounded
may truncate
does not participate as a required selector
does not determine focus_complete
~~~

Por tanto:

~~~text
focus_complete == true
!= Kernel Specification guaranteed present
~~~

## 6. Decisión G1 — nueva clase documental explícita

Se agrega una clase E1 exacta:

~~~text
source_class:
APPROVED_SPECIFICATION

authority_class:
normative_subordinate
~~~

Semántica:

~~~text
APPROVED_SPECIFICATION
=
an explicitly catalogued approved specification
with normative force inside its declared scope
and subordinate to GOVERNING sources
~~~

Para V0 el catálogo exacto es:

~~~text
docs/architecture/kernel.md
~~~

No se usa wildcard.

## 7. Por qué no usar GOVERNING / normative

Reclasificar kernel.md como:

~~~text
GOVERNING / normative
~~~

sería demasiado fuerte porque colapsaría:

~~~text
Blueprint
and
approved subordinate specification
~~~

en la misma clase documental.

Eso perdería la precedencia existente:

~~~text
Blueprint
>
Kernel Specification
~~~

KAF-01 debe aumentar fidelidad, no aplanar autoridad.

## 8. Por qué no conservar ARCHITECTURE_REFERENCE / reference

Eso sería demasiado débil.

Una simple referencia:

~~~text
provides context
but no automatic normative force
~~~

La Kernel Specification:

~~~text
is an approved specification
and governs Kernel semantics in its declared scope
~~~

Por tanto la clasificación actual es materialmente insuficiente.

## 9. Exact-catalog rule

Nueva regla E1:

~~~text
APPROVED_SPECIFICATION
MUST be assigned only by explicit exact-path catalog.
~~~

No:

~~~text
docs/architecture/*.md
-> auto-approved
~~~

No:

~~~text
status: active
-> auto-approved by parsing
~~~

No:

~~~text
filename contains "spec"
-> auto-approved
~~~

Razón:

~~~text
classification is deterministic and fail-closed
approval is repository-governed
not inferred from naming or metadata alone
~~~

Future approved specifications require an explicit gate/catalog update.

## 10. Precedencia para Analyze

ANALYZE_SYSTEM_PROMPT deberá conocer la nueva clase:

~~~text
GOVERNING / normative
-> highest applicable documentary role represented by E1

APPROVED_SPECIFICATION / normative_subordinate
-> normative within declared scope
-> subordinate to GOVERNING
-> must not be treated as generic reference

SECURITY_POLICY / protected_subordinate
-> protected requirement
-> does not override GOVERNING
-> interactions with approved specifications follow applicable governed hierarchy

DECISION_RECORD / status_dependent
-> not automatically Accepted

ARCHITECTURE_REFERENCE / reference
-> context, not automatic normative authority
~~~

Importante:

~~~text
source_class != authorization
authority_class != runtime authority
~~~

Se modifica sólo interpretación documental.

## 11. U01 required selector

U01 deberá incorporar:

~~~text
EvidenceSelector(
  "EXACT_PATH",
  "docs/architecture/kernel.md",
  (...),
  bounded_max
)
~~~

Términos candidatos:

~~~text
"Kernel lógico e instancias concretas"
"Kernel First"
"Capability First"
"KIC-"
"Core Kernel"
"Kernel.receive"
~~~

El selector debe capturar, en el baseline actual:

~~~text
logical Kernel semantics
KIC-01..KIC-07 headings
Capability First boundary
Kernel.receive boundary
Core Kernel distinction
~~~

Bound candidato:

~~~text
max_matches <= 64
~~~

No se amplían límites globales.

## 12. Focus completeness semantics

Después de GREEN:

~~~text
kernel.md missing
-> U01 required selector MISSING
-> focus_complete false
-> no model call

kernel.md unreadable
-> selector UNREADABLE
-> focus_complete false
-> no model call

kernel.md required evidence truncated
-> selector TRUNCATED
-> focus_complete false
-> no model call
~~~

Esto convierte la Kernel Specification en parte real de la suficiencia U01.

## 13. No generalización a otros focuses

KAF-01 modifica sólo:

~~~text
U01 Core Kernel required knowledge
~~~

No cambia required selectors de:

~~~text
U04
RR-03
~~~

La nueva clase E1 puede ser visible globalmente como metadata de kernel.md,
pero no obliga a incluir esa fuente en focuses no relacionados.

## 14. Implementation scope futuro

GREEN candidato podrá tocar solamente:

~~~text
src/malak/knowledge/knowledge_reader.py
src/malak/capabilities/_engineering_analysis.py
src/malak/capabilities/_engineering_evidence.py

tests/test_knowledge_reader.py
tests/test_engineering_analyze.py
tests/test_governed_engineering_evidence_focus_v0.py
~~~

No se modifica:

~~~text
Kernel implementation
Planner
Conversation runtime
provider
generation contract
Analyze JSON schema
Analyze parser
finding classification enum
E4 eligibility
InternalInteraction terminal rules
U04 focus
RR-03 focus
~~~

## 15. RED requirements futuros

RED debe demostrar al menos:

~~~text
R01 kernel.md is classified
    APPROVED_SPECIFICATION / normative_subordinate

R02 Blueprint remains
    GOVERNING / normative

R03 generic architecture docs remain
    ARCHITECTURE_REFERENCE / reference

R04 unknown/new architecture docs do not become
    APPROVED_SPECIFICATION automatically

R05 Analyze prompt recognizes APPROVED_SPECIFICATION

R06 prompt states APPROVED_SPECIFICATION
    is subordinate to GOVERNING

R07 prompt does not convert source_class into authorization

R08 U01 knowledge_required_selectors contains
    exact docs/architecture/kernel.md

R09 focused U01 evidence contains kernel.md
    as required=true

R10 current KIC evidence is present in bounded U01 packet

R11 missing kernel.md prevents focus_complete

R12 U04/RR-03 focus definitions remain unchanged

R13 no Analyze schema/parser/classification changes

R14 authority_effect remains none
~~~

RED must be deterministic.

No real LLM inference.

## 16. GREEN budget futuro

Production delta esperado:

~~~text
E1 exact source catalog + one new documentary class

Analyze prompt:
one documentary-role rule

U01 Focus:
one required exact-path selector
~~~

No new:

~~~text
manager
registry object
metadata parser
status parser
trust engine
authority service
~~~

Correction budget:

~~~text
max bounded correction rounds: 2
~~~

## 17. Relationship with E3 Epistemic Calibration

KAF-01 y EC son orthogonal but complementary:

~~~text
KAF-01
-> correct evidence role + guaranteed U01 presence

EC
-> correct temporal/epistemic interpretation
~~~

Neither substitutes the other.

Correct sequence before Eighth U01:

~~~text
KAF-01 safe disposition
+
E3 epistemic calibration safe disposition
+
merged main
+
new admission
+
preflight
+
explicit Owner authorization
~~~

## 18. Critical Contract Hardening

KAF-01 afecta knowledge metadata consumida por reasoning gobernado.

Contrato crítico:

~~~text
YES
~~~

Interpretaciones cerradas:

~~~text
approved specification
!= governing master source

approved specification
!= generic reference

normative subordinate
!= authorization

exact catalog
!= wildcard promotion

focus_complete
must include all required selectors

supplemental evidence
!= required evidence

knowledge role
!= snapshot trust

source classification
!= runtime permission
~~~

Known material ambiguity after hardening:

~~~text
0 within KAF-01 scope
~~~

## 19. Four Questions of Law

### Blueprint — PASS

Blueprint remains governing and superior.

No architecture shape change.

### Cognitive Constitution — PASS

Improves evidence-role fidelity.

Does not grant authority.

### Governance Constitution — PASS

Human authority unchanged.

No operation authorization added.

### Kernel complexity — PASS

~~~text
Kernel delta 0
Planner delta 0
~~~

## 20. Design 4R

### Risk — PASS

Main risk:

~~~text
authority inflation
~~~

Mitigation:

~~~text
new class is normative_subordinate
not GOVERNING
not runtime authority
exact-path allowlist only
~~~

Second risk:

~~~text
focus growth / prompt growth
~~~

Mitigation:

~~~text
one exact-path selector
bounded max <= 64
global limits unchanged
~~~

### Readability — PASS

Document roles become explicit:

~~~text
GOVERNING
APPROVED_SPECIFICATION
ARCHITECTURE_REFERENCE
~~~

### Reliability — PASS

U01 no longer depends on supplemental chance to receive its own approved Kernel
Specification.

### Resilience — PASS

Future unknown architecture docs remain reference/fail-closed.

Missing required Kernel Specification blocks focused inference instead of silently
continuing.

## 21. RDD Stage 1 Design Check

~~~text
baseline identity strategy                PASS
future candidate identity strategy        PASS
evidence provenance                       PASS
Writer / Reviewer / Validator separation  PASS
Authority separation                      PASS
PASS / FAIL / INCONCLUSIVE discipline     PASS
candidate invalidation                    PASS
bounded correction                        PASS
independent fix validation                REQUIRED if corrections occur
authority_effect                           none
RDD Stage 2                                NOT AUTHORIZED
~~~

Result:

~~~text
PASS
~~~

## 22. Malāk Alignment Matrix

| Fuente | Clase | Invariante | Baseline | Disposición | Efecto |
|---|---|---|---|---|---|
| Cognitive Constitution | normative | Evidence != Authority | preserved | ADOPT | none |
| Governance Constitution | normative | Human in Control | preserved | ADOPT | none |
| Blueprint | architecture master | Blueprint precedence | GOVERNING/normative | ADOPT | unchanged |
| AGENTS.md | repository instruction | approved specs below Blueprint | explicit | ADOPT | E1 role corrected |
| Kernel Specification | approved specification | Kernel semantics / KIC-01..07 | misclassified by E1 | ADAPT | explicit source class |
| E1 design | implementation design | deterministic fail-closed source classification | no spec class | ADAPT | exact approved-spec catalog |
| E3 design | implementation design | documentary precedence | no spec class | ADAPT | prompt role rule |
| U01 Focus | implementation | complete required evidence | kernel spec not required | ADAPT | exact required selector |
| PR #206 design | non-normative | KAF-01 prerequisite | explicit | INPUT | sequencing only |

## 23. Security / authority horizon

~~~text
Prompt & Context Trust        ALREADY_COVERED
Identity & Delegation         UNCHANGED
Memory/Knowledge Poisoning    IMPROVED ROLE FIDELITY
AI Supply Chain               UNCHANGED
Resource Governance           UNCHANGED
Observability                 UNCHANGED
Human in Control              PASS
~~~

No writes to Knowledge.

No Memory change.

No network/tool side effects.

## 24. Eighth U01 gate

Current state:

~~~text
Eighth U01
NOT ADMISSIBLE
~~~

KAF-01 design PASS does not unblock it.

Only a future completed implementation candidate plus E3 calibration disposition
can remove this prerequisite.

## 25. Authorization boundary

~~~text
G0                          PASS
G1                          PASS
Critical Contract Hardening PASS
Four Questions              PASS
Design 4R                   PASS
RDD Stage 1 Design Check    PASS

RED                         NOT AUTHORIZED
GREEN                       NOT AUTHORIZED
runtime execution           NOT AUTHORIZED
Eighth U01                  NOT AUTHORIZED
self-modification           NOT AUTHORIZED
authority_effect            none
~~~

## 26. Next lawful transition

~~~text
candidate-bound CI for this design
-> Owner review / merge
-> explicit Owner authorization for KAF-01 RED
~~~

E3 Calibration RED remains a separate authorization line.
