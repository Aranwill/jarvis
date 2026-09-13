---
title: Malāk CAL-014 — Normative Scope Interpretive Hardening
status: gate_candidate
authority: scope_freeze_clarification
language: es
as_of_date: 2026-09-13
source_baseline: d262114a859b55251c2856cd02d836b80e2ad7c8
supersedes_scope_shape: false
reopens_scope_for_interpretation_only: true
interpretive_precedence_over:
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
normative_activation_authorized: false
law_materialization_authorized: false
adr_acceptance_authorized: false
implementation_authorized: false
persistence_intent_authorized: false
persistence_authorization_authorized: false
persistent_memory_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
rdd_stage_2_authorized: false
sprint_7_12_authorized: false
exact_candidate_refresh_required: true
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-DURABLE-RELIANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
  - docs/project/sprints/proposals/MALAK-CAL-014-COGNITIVE-CONSTITUTION-CANDIDATE-PATCH.md
  - docs/project/sprints/proposals/MALAK-CAL-014-BLUEPRINT-CANDIDATE-PATCH.md
  - docs/project/sprints/proposals/MALAK-CAL-014-ADR-006-CANDIDATE.md
  - docs/project/sprints/proposals/MALAK-CAL-014-DECISION-INDEX-CANDIDATE-PATCH.md
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/architecture/decisions/decision-index.md
  - SECURITY.md
  - docs/development/malak_construction_protocol.md
---

# Malāk CAL-014 — Normative Scope Interpretive Hardening

## 1. Propósito

Reabrir de forma estrictamente acotada el Scope Freeze de CAL-014 para eliminar
ambigüedades interpretativas antes de considerar definitivo cualquier wording
normativo candidato.

Esta unidad no cambia la forma arquitectónica ya seleccionada:

```text
CC-013 — one new independent constitutional principle
R-023 — one protected durable reliance architectural rule
ADR-006 — Protected Durable Reliance Preconditions
Decision Index — conditional bookkeeping after human ADR acceptance
```

```text
interpretive hardening
!= architectural redesign
!= normative activation
!= ADR acceptance
!= implementation authorization
```

No se crea ninguna nueva layer, service, manager, capability, runtime o storage.

---

## 2. Baseline y estado real del paquete candidato

Baseline autoritativo de esta revisión:

```text
main@d262114a859b55251c2856cd02d836b80e2ad7c8
```

Ese baseline ya contiene el merge de PR #130 con cuatro documentos candidatos no
normativos bajo `docs/project/sprints/proposals/`.

Por tanto:

```text
PR #130 merged candidate package
= historical / non-normative candidate evidence

PR #130 merge
!= normative activation
!= ADR-006 acceptance
!= implementation authorization
!= Persistence Authorization
!= Persistent Memory authorization
```

El wording de esos cuatro documentos queda **superseded as final candidate wording**
allí donde este hardening establece una semántica más estricta. No se requiere
revertir PR #130: se conserva su valor histórico y de trazabilidad.

---

## 3. Precedencia interpretativa

El Scope Freeze original conserva autoridad sobre:

- la forma arquitectónica `CC-013 + R-023 + ADR-006 + conditional Decision Index`;
- los archivos normativos que eventualmente podrían cambiar;
- los límites de scope no afectados por este documento;
- las prohibiciones de introducir runtime, storage o nuevos componentes.

Este Interpretive Hardening controla la semántica y el wording para todas las
materias que regula expresamente.

```text
for architectural shape and unaffected constraints
→ Original Scope Freeze controls

for semantics/wording covered by this hardening
→ Interpretive Hardening controls

on overlap or conflict
→ Interpretive Hardening prevails
```

No queda a discreción del lector futuro decidir si existe o no un “conflicto
interpretativo”: toda materia expresamente regulada aquí usa esta versión como fuente
controlante.

---

## 4. Razón de reapertura

La revisión anti-misinterpretation identificó superficies donde una implementación
futura podía satisfacer una lectura literal mínima y aun apartarse de la intención
gobernada de Malāk.

Hallazgos consolidados:

```text
P0-1  constitutional fallback could be read as implicit retention authority
P0-2  authorization ownership could be blurred across Governance/Security/Memory
P0-3  high-impact protection could be bypassed through missing classification
P0-4  governed policy could be misread as allowed to waive constitutional floor
P1-1  policy could manufacture “non-applicability” to evade a material guarantee
P1-2  exact material / relevant derivation / reliance context lacked frozen meaning
P1-3  origin/producer identity applicability lacked a governed rule
P1-4  precedence between Scope Freeze and Interpretive Hardening was implicit
```

Ninguno invalida CAL-014. Todos requieren cierre antes de futura materialización
normativa.

---

## 5. Separaciones reforzadas

Quedan congeladas:

```text
constitutional failure handling
!= retention authorization
!= quarantine authorization
!= persistence authorization

Governance authorization
!= Security constraint/enforcement
!= Memory lifecycle semantics

policy refinement
!= constitutional waiver

conditional applicability refinement
!= manufactured non-applicability

absence of an evaluation policy
!= absence of a constitutional obligation

risk classification
!= producer/presenter self-classification

unclassified
!= low impact

origin/producer identity applicability
!= producer discretion

exact material
!= logical ID
!= pointer
!= alias
!= storage location

relevant derivation
!= mere relation label

reliance context
!= historical context copied forward by default
```

Y permanecen vigentes:

```text
retention != reliance
storage != trust
retrieval != trust
identity != trust
integrity != semantic truth
provenance != trust
trust != authority
Evidence != Authority
Decision != Enforcement != Execution
```

---

## 6. Cierre P0 — autorización de retention / quarantine

CAL-014 no concede autoridad operativa para crear un efecto persistente.

Ownership congelado:

```text
Governance / applicable authorization policy
→ grants or denies operational permission

Security
→ constrains and enforces an otherwise applicable permission

Memory Layer
→ owns future domain lifecycle semantics

Security constraint
!= operational authority

Memory lifecycle semantics
!= operational authority
```

Por tanto:

```text
CAL-014 failure
→ block / limit / deny / abstain the reliance transition

retention or quarantine
→ only when independently permitted by applicable Governance/authorization policy
   and subject to applicable Security constraints/enforcement
   and applicable Memory lifecycle semantics

independently permitted retention/quarantine
!= later reliance permission
```

Una policy cognitiva puede seleccionar conceptualmente una ruta de revisión, pero
no puede materializar retention/quarantine sin autorización operativa independiente.

---

## 7. Cierre P0 — policy cannot weaken the constitutional floor

La frase `garantías aplicables y suficientes` no delega a una policy inferior la
facultad de anular el principio constitucional.

Una policy puede refinar:

```text
- how an applicable constitutional guarantee is instantiated;
- how sufficiency is evaluated;
- risk-proportional depth;
- revalidation conditions;
- conditional applicability only within superior governed criteria.
```

Una policy NO puede:

```text
- waive an applicable constitutional requirement;
- manufacture non-applicability to evade a material guarantee;
- declare a required guarantee satisfied by absence of evidence;
- convert missing evaluation capability into PASS;
- lower the constitutional floor to zero for convenience/cost/latency;
- infer trust from prior storage/admission/repetition;
- use missing policy/evaluator as evidence that no assurance is required.
```

Toda conclusión material de no-aplicabilidad que elimine una garantía deberá ser:

```text
governed
+ justified
+ reconstructible/auditable
+ compatible with superior invariants
```

Y nunca podrá basarse únicamente en:

```text
cost
latency
implementation convenience
missing evaluator
producer preference
presenter preference
```

Si una obligación constitucional material es aplicable y no existe una policy o
mecanismo autorizado capaz de evaluarla:

```text
no applicable evaluation capability
!= no assurance required

result
→ fail closed for durable reliance
```

---

## 8. Definiciones interpretativas mínimas

Estas definiciones no prescriben schema, algoritmo, storage, cryptography ni
componente.

### 8.1 Exact material

`Material exacto` significa el contenido o representación material realmente usado
como fundamento de la transición o decisión.

No queda establecido únicamente por:

```text
logical ID
pointer
alias
source label
storage location
historical candidate/admission ID
```

Una specification futura podrá definir la representación canonical o binding
necesario, siempre que preserve esta propiedad.

### 8.2 Relevant derivation

`Derivación relevante` significa provenance/lineage suficiente para reconstruir los
cambios materiales entre el origen o antecedente pertinente y el artefacto objeto de
reliance.

```text
relationship exists
!= derivation sufficiently known

rehash / rewrap / copy
!= provenance reset
```

No se exige preservar transformaciones irrelevantes al riesgo, pero una
transformación material para identidad, integrity, provenance, trust, authority,
admissibility o applicability no puede omitirse silenciosamente.

### 8.3 Reliance context

`Contexto de reliance` significa, según aplicabilidad, el propósito, la operación o
transición concreta, la policy vigente, el estado temporal y los contextos de
autoridad/seguridad necesarios para evaluar si las garantías continúan siendo
válidas.

```text
same content
!= same reliance context

previously valid context
!= current applicability
```

Una specification futura puede representar este contexto de otra forma, pero no
puede asumir equivalencia solo porque el contenido permanezca igual.

---

## 9. Clasificación de high-impact

High-impact no puede ser una categoría autoasignable ni una condición que desaparezca
por falta de clasificación.

Reglas congeladas:

```text
high-impact classification
must be governed
must be reconstructible/auditable
must be fail-closed when material uncertainty affects classification

unable to determine impact
!= low impact

material uncertainty in classification
→ apply high-impact protections OR block/escalate
→ never downgrade
```

Queda prohibido:

```text
producer self-downgrade
presenter self-downgrade
model self-downgrade
agent self-downgrade
risk laundering through relabeling
“not classified” -> automatically low impact
missing classifier -> automatically low impact
```

La Constitución no necesita enumerar todas las decisiones high-impact. La
clasificación concreta pertenece a policy/specification gobernada, pero su ausencia
no crea una vía de bypass.

---

## 10. Aplicabilidad de origin / producer identity

La expresión `identidad de origen o productor cuando corresponda` no significa libre
discreción del productor o implementador.

Dicha identidad es materialmente aplicable cuando la corrección, provenance, trust,
authority, admissibility o risk de la transición depende de quién o qué produjo,
originó o transformó materialmente el contenido.

La aplicabilidad deberá ser determinada por reglas/policies gobernadas o por una
invariante superior aplicable.

```text
producer says “identity irrelevant”
!= identity not applicable

presenter lacks producer identity
!= identity requirement waived
```

Si la identidad materialmente requerida no puede establecerse, se aplica la
semántica fail-closed de CAL-014.

---

## 11. Wording constitucional candidato endurecido

Para futura materialización, este wording controla el candidate de `CC-013`:

```markdown
## CC-013 — Reliance Durable Protegido

Antes de que Memory, Knowledge, evidencia externa o artefactos derivados sean
utilizados como fundamento material de una transición durable, o de una decisión de
alto impacto cuya clasificación deba determinarse mediante reglas gobernadas,
auditables y fail-closed y cuya corrección dependa materialmente de ese contenido,
Malāk deberá satisfacer, proporcionalmente al riesgo y en el momento del reliance,
garantías aplicables y suficientes ligadas al material exacto y a su derivación
relevante sobre identidad de origen o productor cuando dicha identidad sea material
para la corrección, provenance, trust, authority, admissibility o riesgo de la
transición, integridad del contenido y provenance.

La aplicabilidad y suficiencia podrán ser refinadas por rules/policies gobernadas,
pero ninguna policy inferior podrá omitir, rebajar, declarar satisfecha por default
o convertir en opcional una obligación constitucional materialmente aplicable. La
no-aplicabilidad material que elimine una garantía deberá estar gobernada,
justificada y ser reconstructible/auditable bajo criterios superiores aplicables; no
podrá fabricarse por conveniencia, costo, latencia, ausencia de evaluator ni interés
del productor/presentador. La suficiencia no podrá surgir de autoafirmación del
material, de su productor ni del componente que lo presenta. Cuando una obligación
constitucional material sea aplicable y no exista una policy o mecanismo autorizado
capaz de evaluarla, la transición deberá fallar de forma cerrada.

La ausencia o incertidumbre material de clasificación de impacto no podrá
interpretarse como bajo impacto. Cuando dicha incertidumbre pueda alterar la
aplicabilidad de estas garantías, Malāk deberá aplicar las protecciones de alto
impacto o bloquear/escalar la transición según las policies gobernadas aplicables;
nunca degradarla por default.

Estas garantías no son transitivas ni reutilizables por default entre artefactos,
versiones, derivaciones, contextos, propósitos o momentos distintos. Un identificador
lógico, la igualdad de fuente declarada, la mera presencia o recuperación del
material, su admisión o almacenamiento previo, el consenso, la repetición, la
ausencia de contradicciones detectadas o la confianza declarada no sustituyen una
garantía material aplicable. `content integrity != semantic truth`, `provenance !=
trust` y `source identity != authority`.

Cuando una garantía material requerida no pueda establecerse, haya quedado obsoleta
para la transición, no pueda revalidarse cuando corresponda o una no-aplicabilidad
material no pueda justificarse bajo criterios gobernados, no podrá considerarse
implícitamente satisfecha. Malāk deberá impedir la transición, limitar su alcance,
negar o abstenerse según las policies aplicables.

Cualquier retención o quarantine de revisión es un efecto operativo separado y solo
podrá ocurrir cuando exista autorización independiente bajo Governance/policy de
autorización aplicable, sujeta a los controles de Security y a las semantics de
lifecycle de Memory que correspondan. Dicha autorización no concede reliance
posterior sin una nueva evaluación aplicable.

Esta regla no convierte identidad, integridad, provenance, receipts, almacenamiento
ni evidencia en trust o autoridad; no impide retención forense o quarantine
gobernada de material no confiable cuando exista autorización independiente
aplicable; y no prescribe un mecanismo criptográfico, tecnología de almacenamiento
o implementación concreta.
```

No se permite modificar CC-001..CC-012 para materializar CAL-014.

---

## 12. Wording arquitectónico candidato endurecido

Para futura materialización, este wording controla el candidate de `R-023`:

```markdown
## R-023 — Transición protegida hacia Reliance Durable

La retención, almacenamiento, recuperación o admisión previa de material no lo
convierte por sí mismo en fundamento válido para reliance durable.

Toda transición en la que Memory, Knowledge, evidencia externa o un artefacto
derivado pase a ser fundamento material de un efecto durable, o de una decisión de
alto impacto cuya clasificación deba determinarse mediante reglas gobernadas,
auditables y fail-closed y cuya corrección dependa materialmente de ese contenido,
deberá satisfacer las garantías aplicables de identidad, integridad y provenance
definidas por la Constitución Cognitiva y las policies/specifications vigentes.

Las garantías deberán corresponder al material exacto, a la derivación relevante y
al contexto actual de la transición; no podrán heredarse únicamente por compartir
un identificador lógico, fuente declarada, ubicación de almacenamiento, historial
de admisión o relación de derivación. Una policy puede refinar la instanciación,
suficiencia, profundidad proporcional al riesgo, revalidación y aplicabilidad
condicional dentro de criterios gobernados superiores; no puede anular una
obligación constitucional aplicable, fabricar no-aplicabilidad para evadirla ni
convertir ausencia de capacidad de evaluación en autorización para continuar.

Toda no-aplicabilidad material que elimine una garantía deberá estar gobernada,
justificada y ser reconstructible/auditable. Costo, latencia, conveniencia, ausencia
de evaluator o preferencia del productor/presentador no constituyen por sí solos
justificación válida.

La ausencia o incertidumbre material de clasificación de impacto no equivale a bajo
impacto. Si dicha incertidumbre pudiera cambiar las garantías exigibles, deberán
aplicarse protecciones de alto impacto o bloquearse/escalarse la transición; nunca
degradarse por default.

Una garantía válida para un artefacto, versión, contexto o momento no se presume
válida para otro. Cuando una garantía material requerida no pueda establecerse, haya
dejado de ser aplicable, esté stale o no pueda revalidarse cuando corresponda, la
transición deberá fallar de forma cerrada: deberá bloquearse, limitarse, negarse o
producir abstención según la policy aplicable.

Cualquier retención o quarantine de revisión es un efecto operativo separado:
requiere autorización independiente bajo Governance/policy de autorización
aplicable, queda sujeto a Security enforcement/constraints y respeta las semantics
de lifecycle de Memory correspondientes. Retención o quarantine no equivalen a
autorización para reliance posterior.

Esta regla define una propiedad arquitectónica y no prescribe por sí misma una nueva
layer, service, manager, mecanismo criptográfico, storage technology ni
implementación concreta.
```

R-001..R-022, ownership de capas, Kernel, Memory Layer, Knowledge Layer y el Blueprint
diagram permanecen fuera de alcance.

---

## 13. Requisitos adicionales para ADR-006

El draft de ADR-006 deberá incorporar, además del Scope Freeze original:

1. definiciones mínimas de `exact material`, `relevant derivation` y `reliance context`;
2. prohibición de `policy -> constitutional waiver`;
3. prohibición de manufactured non-applicability;
4. requisito de que non-applicability material sea governed + justified + auditable;
5. `no evaluation capability -> fail closed`, cuando la obligación constitucional
   sea materialmente aplicable;
6. high-impact classification gobernada, auditable y no auto-downgradeable;
7. `unable to determine impact != low impact`;
8. regla de aplicabilidad gobernada para origin/producer identity;
9. separación explícita entre Governance authorization, Security enforcement y
   Memory lifecycle semantics;
10. separación explícita entre failure handling cognitivo y autorización para
    retention/quarantine/persistence;
11. prohibición de risk laundering por relabeling o ausencia de clasificación;
12. preservación de `partial-failure` como problema del gate operativo futuro, sin
    asignarle ownership por inferencia en esta ADR.

---

## 14. Impacto sobre el exact candidate package ya mergeado

El paquete de PR #130 permanece en `main` como evidencia histórica no normativa.
Antes de cualquier activación normativa deberá existir un **candidate refresh** que:

```text
1. starts from the then-current authoritative main
2. updates CC-013 candidate to section 11 wording
3. updates R-023 candidate to section 12 wording
4. updates ADR-006 candidate to section 13 requirements
5. preserves Decision Index gating unless ADR identity/status/domain changes
6. passes candidate-bound CI
7. receives independent human review
```

Hasta entonces:

```text
PR #130 candidate wording
!= final normative candidate wording
!= active law
!= Accepted ADR
```

---

## 15. Acceptance criteria

Este hardening solo puede concluir `PASS` si:

- no modifica la forma `CC-013 + R-023 + ADR-006 + conditional Decision Index`;
- no introduce una nueva layer/service/manager;
- mantiene Governance como fuente de permiso operativo;
- mantiene Security como constraint/enforcement, no como fuente autónoma de authority;
- mantiene Memory lifecycle semantics separadas de operational authorization;
- no convierte retention/quarantine en authority implícita;
- no permite que policy inferior anule el piso constitucional;
- no permite manufactured non-applicability;
- no permite que ausencia de policy/evaluator se convierta en PASS;
- no permite `unclassified -> low impact`;
- high-impact no puede auto-downgradearse;
- origin/producer applicability no queda a discreción del productor;
- no prescribe storage, DB, schema, PKI, nonce, TTL, hashing o provider;
- no autoriza Persistence Intent, Persistence Authorization, Persistent Memory,
  retrieval/RAG/Knowledge runtime, RDD Stage 2 ni Sprint 7.12;
- law targets permanecen sin modificación remota.

Cualquier incumplimiento material produce:

```text
FAIL or INCONCLUSIVE
never implicit PASS
```

---

## 16. Stop conditions

Detener si este hardening:

- requiere modificar Governance Constitution o SECURITY.md;
- necesita redefinir CC-001..CC-012 o R-001..R-022;
- requiere nueva layer/service/manager;
- necesita conceder authority de retention/persistence desde CAL-014;
- necesita atribuir operational authority a Security o Memory lifecycle semantics;
- necesita permitir que una policy inferior waivie una obligación constitucional;
- necesita permitir manufactured non-applicability;
- necesita que una clasificación high-impact sea decidida por el productor/presenter
  interesado;
- necesita interpretar falta de clasificación como bajo impacto;
- necesita resolver mecanismos concretos de persistence/retrieval;
- intenta materializar remotamente Constitution, Blueprint, ADR-006 o Decision Index;
- intenta autorizar implementación.

---

## 17. Resultado esperado

```text
INTERPRETIVE HARDENING TARGET:

architecture shape: unchanged
constitutional floor: stronger / explicit
policy role: refinement only, never waiver
non-applicability: governed / justified / auditable
operational authority: Governance / applicable authorization policy
Security role: constraints + enforcement
Memory role: lifecycle semantics
retention authority: independent from CAL-014
high-impact classification: governed + auditable + fail-closed
unclassified: never automatic low impact
origin/producer applicability: governed
exact-material semantics: clarified
precedence: explicit
fail-closed behavior: explicit
implementation authority: none
```

Este documento no activa CAL-014. Solo endurece el perímetro que deberá respetar
cualquier futuro exact candidate y cualquier posterior materialización humana.
