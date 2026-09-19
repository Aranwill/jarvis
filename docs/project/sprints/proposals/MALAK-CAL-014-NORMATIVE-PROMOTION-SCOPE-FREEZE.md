---
title: Malāk CAL-014 — Normative Promotion Scope Freeze
status: gate_candidate
authority: scope_freeze
language: es
as_of_date: 2026-09-13
source_baseline: 69cccf23b773c89c31b47a2ef1cad75ebf76b237
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
alignment_matrix_ref: "section-13"
related:
  - docs/project/sprints/proposals/MALAK-CAL-014-DURABLE-RELIANCE-CONSTITUTIONAL-IMPACT-G0-G1.md
  - docs/governance/cognitive_constitution.md
  - docs/governance/governance_constitution.md
  - docs/architecture/blueprint.md
  - docs/architecture/architecture_quality_gates.md
  - docs/architecture/adr/ADR-005-evidence-bound-final-response-transition.md
  - docs/architecture/adr/ADR-TEMPLATE.md
  - docs/architecture/decisions/decision-index.md
  - SECURITY.md
  - docs/development/malak_construction_protocol.md
---

# Malāk CAL-014 — Normative Promotion Scope Freeze

## 1. Propósito

Congelar el perímetro exacto de una posible promoción normativa de:

```text
CAL-014 — Source Identity and Content Integrity before Durable Reliance
```

antes de materializar cualquier modificación de ley.

```text
scope freeze
!= constitutional amendment
!= ADR acceptance
!= Blueprint activation
!= implementation
!= authority
```

Esta unidad prepara una futura decisión humana. No activa CAL-014.

---

## 2. Baseline congelado

Fuente oficial congelada:

```text
repository: Aranwill/jarvis
branch: main
commit: 69cccf23b773c89c31b47a2ef1cad75ebf76b237
```

---

## 3. Frontera de escritura de ley

El Construction Protocol establece una frontera especial para:

```text
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/adr/** cuando una ADR crea, acepta o modifica arquitectura normativa
docs/architecture/decisions/decision-index.md cuando forma parte de una promoción normativa
```

Por tanto, esta PR queda limitada a este único archivo no normativo:

```text
docs/project/sprints/proposals/MALAK-CAL-014-NORMATIVE-PROMOTION-SCOPE-FREEZE.md
```

Los documentos de ley deben permanecer byte-for-byte sin modificación en esta unidad.

Cualquier futura materialización normativa deberá realizarla el Owner localmente,
hunk-by-hunk, con revisión conjunta y validación candidate-bound.

---

## 4. Problema normativo exacto

El G0/G1 integrado concluyó:

```text
CAL-014 previous disposition: DEFER
CAL-014 current design disposition: NEW_CONSTITUTIONAL_CANDIDATE
```

La razón histórica del `DEFER` quedó satisfecha porque el baseline ya posee:

```text
Candidate Content Identity
+
end-to-end content binding through governed admission
```

El gap restante no es de hashing ni de autorización operativa. Es normativo:

```text
no current constitutional invariant explicitly requires
applicable identity + integrity + provenance
before material durable reliance
```

---

## 5. Alternativas de ubicación constitucional

### A — Extender únicamente CC-003

Rechazada.

`CC-003 — Evidencia sobre especulación` gobierna la suficiencia y naturaleza de la
evidencia utilizada para conclusiones. No define por sí sola la transición por la
cual material previamente retenido, admitido o recuperado pasa a ser fundamento de
un efecto durable.

### B — Extender únicamente CC-010

Rechazada.

`CC-010 — Aprendizaje Controlado` cubre aprendizaje permanente, pero CAL-014 también
alcanza evidencia externa, Memory, Knowledge y artefactos derivados utilizados como
fundamento material sin reducirse necesariamente a "aprendizaje".

### C — Reescribir CC-011 / CC-012

Rechazada.

CC-011 y CC-012 gobiernan la frontera Candidate Response → Final Response. Durable
reliance es una transición distinta y no debe mezclarse con finalización de respuesta.

### D — Resolverlo solo mediante SECURITY.md

Rechazada como solución completa por el G0/G1.

Security conserva ownership de enforcement y de las restricciones de seguridad
aplicables a poisoning, taint, revocation, quarantine, disclosure, consent,
freshness/replay e idempotency. Esto no transfiere a Security el ownership de la
semántica de lifecycle de Memory ni de la autorización operativa de Gobernanza.
La obligación evaluada es transversal a Memory, Knowledge, evidencia externa y
artefactos derivados.

### E — Añadir un único principio constitucional nuevo

Seleccionada.

```text
CC-013 — Protected Durable Reliance
```

La nueva cláusula deberá ser mechanism-neutral y no modificar CC-001..CC-012.

---

## 6. Paquete normativo futuro mínimo

Si el Owner autoriza una promoción posterior, el paquete activo máximo queda
congelado a cuatro targets normativos:

```text
1. docs/governance/cognitive_constitution.md
2. docs/architecture/blueprint.md
3. docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
4. docs/architecture/decisions/decision-index.md
```

No se autoriza todavía crear ni modificar ninguno de ellos.

Deben permanecer fuera del paquete activo:

```text
docs/governance/governance_constitution.md
SECURITY.md
docs/architecture/kernel.md
docs/architecture/architecture_quality_gates.md
docs/architecture/knowledge_model.md
AGENTS.md
docs/project/implementation_roadmap.md
src/**
tests/**
```

---

## 7. Delta candidato — Cognitive Constitution

Target vigente:

```text
docs/governance/cognitive_constitution.md
body version: 1.1.0
blob at frozen baseline: 34ecc6685dd686f9e7143b3547b61ec0d91c7c41
```

Una futura promoción solo puede proponer:

### 7.1 Metadatos

1. mantener `frontmatter.version: 0.6.0-alpha`;
2. actualizar `date` a la fecha real de activación;
3. actualizar `history.updated` a la fecha real de activación;
4. añadir `ADR-006` a `related.adr`;
5. cambiar la versión constitucional visible `1.1.0 → 1.2.0`.

### 7.2 Nuevo principio máximo permitido

Añadir exactamente un principio después de CC-012:

```text
## CC-013 — Reliance Durable Protegido
```

Texto candidato congelado:

> Antes de que Memory, Knowledge, evidencia externa o artefactos derivados sean
> utilizados como fundamento material de una transición durable, o de una decisión
> de alto impacto cuya corrección dependa materialmente de ese contenido, Malāk
> deberá satisfacer, proporcionalmente al riesgo y en el momento del reliance,
> garantías aplicables y suficientes ligadas al material exacto y a su derivación
> relevante sobre identidad de origen o productor cuando corresponda, integridad
> del contenido y provenance. La suficiencia será determinada por las reglas y
> policies gobernadas aplicables, no por autoafirmación del material, de su productor
> ni del componente que lo presenta.
>
> Estas garantías no son transitivas ni reutilizables por default entre artefactos,
> versiones, derivaciones, contextos, propósitos o momentos distintos. Un
> identificador lógico, la igualdad de fuente declarada, la mera presencia o
> recuperación del material, su admisión o almacenamiento previo, el consenso, la
> repetición, la ausencia de contradicciones detectadas o la confianza declarada no
> sustituyen una garantía material aplicable. `content integrity != semantic truth`,
> `provenance != trust` y `source identity != authority`.
>
> Cuando una garantía material requerida no pueda establecerse, no sea aplicable al
> material exacto, haya quedado obsoleta para la transición o no pueda revalidarse
> cuando corresponda, no podrá considerarse implícitamente satisfecha. Malāk deberá
> limitar, retener o poner en cuarentena para revisión, negar o abstenerse según las
> políticas aplicables. La retención o cuarentena de revisión no autoriza reliance
> posterior sin una nueva evaluación aplicable.
>
> Esta regla no convierte identidad, integridad, provenance, receipts,
> almacenamiento ni evidencia en trust o autoridad; no impide retención forense o
> cuarentena gobernada de material no confiable; y no prescribe un mecanismo
> criptográfico, tecnología de almacenamiento o implementación concreta.

No se permite modificar CC-001..CC-012 en este paquete.

---

## 8. Delta candidato — Blueprint

Target vigente:

```text
docs/architecture/blueprint.md
Blueprint version: 0.6.2-alpha
blob at frozen baseline: 9c09b26d040164955e99cc27c362b0e72373dc3f
```

Una futura promoción solo puede proponer:

1. `frontmatter.version: 0.6.2-alpha → 0.6.3-alpha`;
2. añadir `ADR-006` a `related.adr`;
3. actualizar `history.updated` a la fecha real de activación;
4. `Blueprint Versión: 0.6.2-alpha → 0.6.3-alpha`;
5. mantener `Project Version: v0.6.0-alpha` sin cambios;
6. actualizar `Última revisión arquitectónica` a la fecha real de activación;
7. actualizar `# 13. Estado del Blueprint` a `Blueprint v0.6.3-alpha`;
8. añadir exactamente una regla después de R-022:

```text
## R-023 — Transición protegida hacia Reliance Durable
```

Texto candidato congelado:

> La retención, almacenamiento, recuperación o admisión previa de material no lo
> convierte por sí mismo en fundamento válido para reliance durable.
>
> Toda transición en la que Memory, Knowledge, evidencia externa o un artefacto
> derivado pase a ser fundamento material de un efecto durable, o de una decisión
> de alto impacto cuya corrección dependa materialmente de ese contenido, deberá
> satisfacer las garantías aplicables de identidad, integridad y provenance
> definidas por la Constitución Cognitiva y las policies/specifications vigentes.
> Las garantías deberán corresponder al material exacto, a la derivación relevante
> y al contexto de la transición; no podrán heredarse únicamente por compartir un
> identificador lógico, fuente declarada, ubicación de almacenamiento, historial de
> admisión o relación de derivación.
>
> Una garantía válida para un artefacto, versión, contexto o momento no se presume
> válida para otro. Cuando una garantía material requerida no pueda establecerse o
> haya dejado de ser aplicable, la transición deberá fallar de forma cerrada y
> limitarse, retenerse o ponerse en cuarentena para revisión, negarse o abstenerse
> según la policy aplicable. Retención o cuarentena no equivalen a autorización para
> reliance posterior.
>
> Esta regla define una propiedad arquitectónica y no prescribe por sí misma una
> nueva layer, service, manager, mecanismo criptográfico, storage technology ni
> implementación concreta.

Queda prohibido modificar el diagrama general, ownership de capas, Kernel, Memory
Layer, Knowledge Layer o flujo R-017..R-022 para expresar CAL-014.

---

## 9. Delta candidato — ADR-006

Número disponible observado en el baseline:

```text
ADR-001..ADR-005 = existentes
ADR-006 = disponible
```

Path futuro congelado:

```text
docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
```

Título candidato:

```text
ADR-006 — Protected Durable Reliance Preconditions
```

La futura ADR deberá decidir únicamente que:

1. durable reliance constituye una transición protegida distinta de retention,
   storage, retrieval, admission y authorization;
2. las garantías aplicables de identity, integrity y provenance deben satisfacerse
   proporcionalmente al riesgo para el material exacto, la derivación relevante y
   el contexto de reliance antes de esa transición;
3. las garantías no son transitivas ni reutilizables por default entre artefactos,
   versiones, derivaciones, contextos, propósitos o momentos distintos;
4. `stored != trusted`, `retention != reliance`, `identity != trust`,
   `integrity != semantic truth`, `provenance != trust` y `trust != authority`
   permanecen invariantes;
5. `required but unavailable != implicitly satisfied` y una garantía obsoleta o no
   ligada al sujeto exacto no satisface el requisito;
6. Governance conserva ownership sobre si una operación persistente está permitida;
7. Security conserva ownership sobre enforcement y sobre las restricciones de
   seguridad aplicables a taint, revocation, quarantine, disclosure, consent,
   freshness/replay e idempotency; esto no convierte a Security en owner del
   lifecycle de Memory;
8. Memory Layer conserva el ownership de la futura semántica de lifecycle de Memory
   cuando esa capacidad sea diseñada y autorizada, subordinada a Constitución,
   Governance y Security; esta ADR no autoriza ese lifecycle ni Persistent Memory;
9. la decisión no crea una nueva layer/service/manager ni prescribe storage,
   criptografía, schema, TTL, nonce, provider o algoritmo.

Relación con ADR-005:

```text
ADR-006 references ADR-005 for historical traceability
ADR-006 resolves the CAL-014 deferred condition recorded by ADR-005
ADR-006 does NOT depend operationally on ADR-005 finalization semantics
ADR-006 does NOT supersede ADR-005 as a whole
```

La ADR deberá permanecer `Proposed` hasta una activación humana explícita.

---

## 10. Delta candidato — Decision Index

Target vigente:

```text
docs/architecture/decisions/decision-index.md
Total ADRs: 5
Accepted: 5
blob at frozen baseline: 9d3c12a80adfbbca5bb9cdb6c90c933dab19c427
```

El índice solo se modifica si ADR-006 es aceptada por el Owner.

Transformaciones máximas permitidas:

1. añadir en la primera tabla después de ADR-005:

```text
| ADR-006 | Accepted | <activation-date> | Protected Durable Reliance Preconditions | Architecture / Cognition / Memory |
```

2. añadir en la segunda tabla después de ADR-005:

```text
| ADR-006 | Protected Durable Reliance Preconditions | Accepted | <activation-date> | Architecture |
```

3. `Total ADRs: 5 → 6`;
4. `Accepted: 5 → 6`.

No se modifica ninguna ADR previa ni otra estadística.

---

## 11. Lo que CAL-014 no puede significar

La promoción normativa no puede crear estas equivalencias:

```text
stored -> trusted
verified digest -> authentic producer
content integrity -> semantic correctness / truth
source authenticity -> truthful content
known provenance -> truthful content
declared provenance -> verified provenance
previously eligible -> currently valid
authorized operation -> trusted payload
permission to store -> permission to rely
absence of taint -> proof of safety
absence of contradiction -> positive validation
retention permission -> reuse permission
repeated observation -> canonical Knowledge
guarantee for artifact A -> guarantee for artifact B
guarantee at T1 -> automatically valid at T2
fresh hash of derived artifact -> clean provenance
```

Tampoco puede implicar:

```text
constitutional requirement = cryptographic mechanism
constitutional requirement = storage authorization
constitutional requirement = Persistence Authorization
constitutional requirement = Persistent Memory readiness
```

### 11.1 Bypass / laundering paths explícitamente bloqueados

El paquete normativo futuro deberá conservar como amenazas interpretativas:

```text
trust laundering through storage / retrieval / repetition
identity laundering through re-hashing or re-wrapping derived content
provenance truncation across derivation boundaries
stale-guarantee replay
cross-artifact or cross-context guarantee reuse
authorization laundering: permission to persist -> permission to rely
self-attestation of sufficiency by the producing or presenting component
```

Cerrar uno de estos caminos no puede utilizarse como prueba de que los demás están
cerrados.

---

## 12. Security Horizon preservado

La promoción normativa puede ser válida aunque todavía no exista Persistent Memory.

Antes de implementar cualquier runtime que materialice durable reliance continúan
siendo bloqueantes, según aplicabilidad:

```text
- exact reliance subject / content binding
- derivation / lineage binding for derived material
- guarantee applicability, freshness and non-transitivity semantics
- explicit fail-closed handling when a required guarantee is unavailable
```

Y antes de cualquier protected durable write continúan siendo además bloqueantes:

```text
- exact persistence subject / payload binding
- authorization freshness and replay semantics
- taint / revocation / quarantine lifecycle
- retention / disclosure / consent policy
- idempotency / partial-failure semantics
```

```text
normative activation readiness
!= durable reliance runtime readiness
!= persistence implementation readiness
```

---

## 13. Malāk Alignment Matrix

| source | authority class | applicable invariant / intent | disposition | promotion effect | prohibited inference |
|---|---|---|---|---|---|
| Cognitive Constitution | constitutional | evidence, traceability, controlled learning, protected finalization | ADAPT | add max one independent CC-013 | no rewrite of CC-001..012 |
| Governance Constitution | constitutional | persistent operations remain governed and policy-authorized | ADOPT | NO DELTA | CAL-014 does not become permission |
| Blueprint | architecture master | Constitution/Governance First, Zero Trust, no bypass, Memory ownership | ADAPT | add max one R-023 + version bookkeeping | no new layer/service/manager |
| SECURITY.md | protected security requirements | access != permission to persist/reuse; security constraints on poisoning/revocation/data handling | ADOPT | NO DELTA | Security does not acquire Memory lifecycle ownership |
| Architecture Quality Gates | architecture governance | ADR/Blueprint/Decision Index/traceability when applicable | ADOPT | require ADR-006 + index on activation | technical PASS != normative authority |
| ADR-005 | accepted ADR | Evidence != Authority; CAL-014 defer trigger historically recorded | OBSERVE / TRACE | ADR-006 records resolution of the deferred CAL-014 condition | no operational dependency on Final Response semantics; ADR-005 not superseded |
| CAL-014 G0/G1 | owner-approved design record | NEW_CONSTITUTIONAL_CANDIDATE; mechanism-neutral; fail-closed | ADOPT | wording source for CC-013/R-023 | no implementation authorization |
| Construction Protocol | process authority | Owner-only materialization of law | ADOPT | law targets read-only in this PR | assistant/agent cannot remotely activate law |
| current baseline | executable + normative baseline | Content Identity + binding implemented; persistence absent | ADOPT | prereq demonstrated | baseline evidence != permission to persist |

Matrix result:

```text
alignment conflicts: 0
higher-authority conflict: 0
new component required: 0
Governance delta required: 0
Security delta required: 0
Kernel delta required: 0
implementation authority inferred: 0
```

---

## 14. Normative Promotion Acceptance Criteria

Una futura activación solo puede concluir `PASS` si demuestra simultáneamente:

1. CC-013 permanece mechanism-neutral;
2. R-023 expresa solo la propiedad arquitectónica necesaria;
3. CC-001..CC-012 permanecen semánticamente intactos;
4. Governance Constitution permanece sin cambios;
5. Security conserva ownership de enforcement y restricciones de seguridad sin
   absorber la semántica de lifecycle de Memory;
6. Memory Layer conserva su ownership arquitectónico sin que esta promoción
   autorice Persistent Memory o un lifecycle concreto;
7. forensic/quarantine retention sigue siendo posible sin trust/reliance;
8. identity, integrity y provenance permanecen distintas de semantic truth, trust
   y authority;
9. las garantías quedan ligadas al material exacto, derivación relevante y contexto
   aplicable, sin herencia o reutilización implícita entre artefactos o momentos;
10. `required but unavailable`, stale, non-applicable o unbound nunca se convierten
    en `satisfied` por default;
11. ninguna nueva layer/service/manager resulta necesaria;
12. no se crea autoridad de implementación, Persistence Authorization, Persistent
    Memory, retrieval ni Knowledge;
13. ADR-006 mantiene relación histórica con ADR-005 sin convertir Final Response en
    una dependencia operativa de durable reliance ni superseder ADR-005;
14. Decision Index solo cambia después de aceptación humana de ADR-006;
15. los blobs objetivo se revalidan antes de aplicar cualquier hunk;
16. `ADR-006` continúa disponible y el target path no existe antes de la
    materialización local;
17. cualquier cambio material respecto del wording congelado de CC-013, R-023 o las
    separaciones de ownership obliga a reabrir este scope freeze;
18. el Owner materializa y acepta explícitamente el paquete normativo.

Cualquier incumplimiento material produce:

```text
FAIL or INCONCLUSIVE
never implicit PASS
```

---

## 15. Precondiciones de futura materialización

Antes de una eventual edición local de ley deben comprobarse los blobs del
baseline objetivo.

Valores congelados en este review:

```text
Cognitive Constitution: 34ecc6685dd686f9e7143b3547b61ec0d91c7c41
Blueprint:              9c09b26d040164955e99cc27c362b0e72373dc3f
Decision Index:         9d3c12a80adfbbca5bb9cdb6c90c933dab19c427
ADR-006 target path:    MUST NOT EXIST before candidate materialization
```

Si alguno difiere en el momento de materialización, si `ADR-006` deja de estar
disponible o si la activación ya no parte de un baseline compatible con el scope
congelado:

```text
STOP
→ refresh baseline
→ re-evaluate affected hunks
→ revalidate Alignment Matrix
→ re-run normative coherence review
```

---

## 16. Stop conditions

Esta unidad o cualquier gate derivado debe detenerse si:

- intenta modificar remotamente un documento de ley;
- requiere más de un nuevo principio constitucional;
- requiere más de una nueva regla de Blueprint;
- requiere modificar Governance Constitution o SECURITY.md para hacer viable la
  promoción;
- requiere modificar CC-001..CC-012;
- requiere nueva layer/service/manager;
- intenta convertir Content Identity en source authenticity, trust o authority;
- intenta convertir content integrity en semantic truth o provenance en trust;
- intenta reutilizar una garantía únicamente por compartir ID, fuente, storage,
  derivación, contexto previo o historial de admisión;
- necesita que una garantía stale, no aplicable o no ligada al sujeto exacto pase
  como satisfecha;
- intenta mover el ownership del lifecycle de Memory hacia Security o Governance;
- necesita decidir storage, database, schema, encryption, PKI, nonce, TTL o
  algoritmo;
- necesita implementar Persistence Intent o Persistence Authorization;
- intenta inferir Persistent Memory readiness;
- `ADR-006` deja de estar disponible o aparece el target path antes de la
  materialización humana;
- el wording material de CC-013/R-023 o las separaciones de ownership cambian sin
  reabrir el scope freeze;
- necesita tocar `src/**` o `tests/**`;
- intenta activar RDD Stage 2 o Sprint 7.12;
- el baseline material cambia antes de activación.

---

## 17. FULL 4R — scope-freeze review

### Risk

```text
status: PASS
```

El paquete reduce superficie normativa a un principio, una regla arquitectónica,
una ADR y un update de índice condicionado. No concede runtime authority. El
hardening bloquea además trust/identity/provenance laundering, replay de garantías
y transferencia implícita de garantías entre artefactos.

### Readability

```text
status: PASS
```

Se separan explícitamente Constitution, Blueprint, ADR, Decision Index,
Governance, Security, Memory ownership y futuros mecanismos de implementación.
También se distinguen integrity, semantic truth, provenance, trust y authority.

### Reliability

```text
status: PASS
```

El scope deriva de ley vigente, G0/G1 integrado, Quality Gates, ADR-005 y baseline
content-bound ya implementado. Los targets y blobs quedan congelados, y las
garantías futuras deben permanecer ligadas al material exacto y al contexto de
reliance.

### Resilience

```text
status: PASS
```

Las stop conditions, fail-closed semantics, no-transitivity, freshness/applicability,
blob revalidation y Owner-only law materialization evitan promoción silenciosa ante
drift, sustitución de contenido, replay o falta de garantías.

Residual risk:

```text
future human activation can still introduce hunk drift
→ mitigated by local hunk-by-hunk review + candidate-bound validation

future policy can define insufficient assurance incorrectly
→ mitigated by fail-closed applicability + explicit scope/ownership boundaries
```

---

## 18. Resultado del scope freeze

```text
SCOPE FREEZE RESULT: PASS

selected constitutional shape:
CC-013 — one new independent principle

selected architectural shape:
R-023 — one protected durable reliance transition rule

future ADR:
ADR-006 — Protected Durable Reliance Preconditions

Governance Constitution delta: NO
Security delta: NO
Kernel delta: NO
runtime/code/tests delta: NO

normative activation: NOT AUTHORIZED
law materialization: NOT AUTHORIZED
ADR acceptance: NOT AUTHORIZED
Persistence Intent: NOT AUTHORIZED
Persistence Authorization: NOT AUTHORIZED
Persistent Memory: NOT AUTHORIZED
RDD Stage 2: NOT AUTHORIZED
Sprint 7.12: NOT AUTHORIZED
blocking findings: 0
```

---

## 19. Próximo gate posible

Este scope freeze no activa nada automáticamente.

Si el Owner acepta este perímetro, el próximo gate puede preparar un paquete
candidato de promoción normativa con patches exactos para revisión humana, pero
sin materializarlos remotamente en los documentos de ley.

Secuencia preservada:

```text
Scope Freeze
        ↓
Owner approval of scope
        ↓
exact candidate patches / ADR-006 draft for review
        ↓
Owner local hunk-by-hunk materialization
        ↓
FULL 4R + normative coherence validation
        ↓
candidate-bound evidence
        ↓
human commit / push / PR / merge
        ↓
post-merge validation
```

Y aun después de una eventual activación:

```text
CAL-014 active law
!= Persistence Authorization
!= Persistent Memory
```
