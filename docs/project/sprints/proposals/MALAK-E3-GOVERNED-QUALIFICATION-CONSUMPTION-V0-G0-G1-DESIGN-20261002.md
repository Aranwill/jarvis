---
title: E3 Governed Qualification Consumption V0 — G0/G1 Design
status: design-candidate
authority: evidence-only / no authority effect
as_of_date: 2026-10-02
trigger: PR #239 / F235-B01
---

# E3 Governed Qualification Consumption V0

## 1. Problema

PR #239 demostró causalmente que una qualification coherente pero controlada por
el caller podía habilitar `DETERMINISTIC`. El primer GREEN candidate
`def2fa10ebbf870fc8119b9871595d7031f8c0b3` separó un objeto de review, pero
permitió que el mismo caller construyera sus resultados `PASS`.

Por tanto:

~~~text
caller-controlled coherent declarations
!= externally grounded qualification
~~~

El candidate citado permanece evidencia histórica de un intento que no cierra el
trust boundary. Este documento no lo convierte en PASS.

## 2. Objetivo

Definir el contrato mínimo mediante el cual routing pueda consumir una
qualification ya revisada externamente y ligada a material exacto, sin:

- autenticar personas dentro del runtime;
- convertir evidencia en authority;
- introducir store, registry, database, PKI o firmas;
- introducir RDD Stage 2;
- permitir self-certification del caller.

## 3. Clasificación

Este contrato es CRÍTICO porque interpreta trust/provenance/evidence y candidate
binding para una decisión de routing.

Risk class candidato: 3 / HIGH.

La secuencia obligatoria es la de
`docs/development/malak_construction_protocol.md §5.5`.

## 4. Baseline y trazabilidad

Cadena causal:

~~~text
PR #235
→ F235-B01

PR #236
→ Deterministic Oracle Qualification Evidence V0 design

PR #237
→ RED/GREEN de qualification; GREEN falla FULL 4R

PR #238
→ corrige trust boundary:
   structural validation != independent qualification review

PR #239
→ RED demuestra que self-declared qualification todavía habilita DETERMINISTIC
→ candidate def2fa10... intenta separar review evidence
→ precheck demuestra que el caller todavía puede fabricar PASS
→ STOP
~~~

Fuentes aplicables principales:

- Cognitive Constitution.
- Governance Constitution.
- Blueprint.
- SECURITY.md.
- Architecture Quality Gates.
- Engineering Method.
- Malāk Construction Protocol.
- MALAK-EVIDENCE-MANIFEST/v1.
- contrato corregido de PR #238.
- código/tests exactos de PR #239.

## 5. Malāk Alignment Matrix

| source | authority class | invariant / intent | disposition | implementation effect |
|---|---|---|---|---|
| Cognitive Constitution | normative protected | evidencia trazable, incertidumbre explícita | ADAPT | no confiar en declaración caller-controlled |
| Governance Constitution | normative protected | Human in Control; evidence != authority | ADOPT | authority_effect siempre none |
| Blueprint | architecture | Kernel simple y boundaries explícitos | ADOPT | Kernel delta 0 |
| SECURITY.md | protected security policy | Zero Trust; fail-closed; identidad fuerte aún no implementada | ADAPT | no PKI/firmas; missing/unverifiable evidence no habilita DETERMINISTIC |
| Architecture Quality Gates | architecture | límites y contratos verificables | ADOPT | contrato bounded y reversible |
| Engineering Method | development contract | Writer != Reviewer != Validator != Authority | ADOPT | review externo no se reemplaza por caller strings |
| Construction Protocol §5.5 | development contract | secuencia crítica no sustituible | ADOPT | no RED antes de pre-RED gates |
| Evidence Manifest v1 | development contract | active evidence externa al candidate + exact candidate binding | ADAPT | reutilizar anti-recursión; no crear receipt/store |
| PR #238 contract correction | active/historical design evidence | structural PASS != independent review PASS | ADOPT | consumo exige external qualification evidence exacta |
| PR #239 RED | active candidate evidence | self-declared qualification no debe producir DETERMINISTIC | ADOPT | negative behavior obligatorio |

Nada de esta matriz constituye autorización de implementación.

## 6. Contrato conceptual

Nombre candidato:

~~~text
GovernedQualificationConsumptionV0
~~~

Responsabilidad:

~~~text
exact qualification material
        +
structural validation evidence
        +
independent qualification review evidence external to active candidate
        +
exact binding
        ↓
bounded consumption eligibility
        ↓
routing
~~~

El contrato NO autentica al reviewer. La independencia real permanece propiedad
del proceso externo gobernado.

## 7. Separaciones obligatorias

~~~text
caller declaration
!= external qualification evidence

structural_validator_result
!= qualification_review_result

qualification_review_result
!= consumption eligibility

consumption eligibility
!= RDD manifest result

RDD manifest result
!= RDD Candidate Conformance

RDD Candidate Conformance
!= Owner approval

evidence
!= authority
~~~

## 8. Evidencia activa y anti-recursión

Se reutiliza el principio de `MALAK-EVIDENCE-MANIFEST/v1`:

~~~text
active qualification review evidence
→ external to candidate worktree
→ auditable
→ bound to exact candidate/material

candidate A changes to B
→ evidence bound to A is stale for B
→ affected evidence must be revalidated
~~~

Soportes compatibles en V0:

- conversación/review de PR ligada al SHA exacto;
- artefacto de validator ligado al SHA exacto;
- informe independiente externo ligado al SHA exacto.

Una copia histórica dentro del repo no certifica el commit que la contiene.

## 9. Binding mínimo requerido

La evidencia consumible debe poder reconciliar, como mínimo:

~~~text
repository
evaluated_candidate_commit
qualification_bundle_digest
reviewed_relation_id
reviewed_evaluation_question_identity
reviewed_obligation_catalog_digest
structural_validator_result
catalog_completeness_result
independence_review_result
verification_material_review_result
qualification_review_result
evidence_references
authority_effect
~~~

Los actor IDs son provenance y pueden conservarse, pero:

~~~text
distinct actor strings
!= cryptographic proof of independence
~~~

La independencia se demuestra externamente por proceso/evidencia, no por una
comparación de strings dentro de routing.

## 10. Semántica fail-closed

~~~text
caller-declared PASS only
→ NOT ELIGIBLE FOR DETERMINISTIC

missing external qualification evidence
→ NOT ELIGIBLE FOR DETERMINISTIC

wrong repository
→ NOT ELIGIBLE FOR DETERMINISTIC

wrong evaluated candidate
→ NOT ELIGIBLE FOR DETERMINISTIC

wrong bundle digest
→ NOT ELIGIBLE FOR DETERMINISTIC

wrong obligation catalog digest
→ NOT ELIGIBLE FOR DETERMINISTIC

structural FAIL | INCONCLUSIVE
→ NOT ELIGIBLE FOR DETERMINISTIC

any required external review dimension FAIL | INCONCLUSIVE
→ NOT ELIGIBLE FOR DETERMINISTIC

duplicate/ambiguous matching evidence
→ NOT ELIGIBLE FOR DETERMINISTIC

exact externally reviewed evidence + exact bindings + all required PASS
→ ELIGIBLE FOR DETERMINISTIC
~~~

`ELIGIBLE` describe una condición de consumo. No es authority, approval ni
permission.

## 11. Candidate identity

El RED futuro deberá congelar explícitamente:

- baseline commit;
- candidate commit;
- qualification evaluated candidate;
- bundle digest;
- obligation catalog digest.

Un cambio material invalida la evidencia afectada.

No se permite heredar PASS por igualdad parcial de IDs lógicos.

## 12. Input boundary

Routing no debe aceptar como prueba suficiente un objeto cuyo claim terminal pueda
ser fabricado íntegramente por el mismo caller que solicita el routing.

El diseño de implementación debe elegir una proyección bounded derivada de
evidencia externa reconciliada. Si para lograrlo aparece necesidad de store,
registry, PKI, network verification o nueva authority surface:

~~~text
STOP
→ scope review
~~~

No se improvisará un boolean `verified=true`, token opaco o string `PASS`.

## 13. Unknown / missing / duplicate

Toda ausencia, contradicción, stale binding, duplicidad o imposibilidad de
reconciliar evidencia requerida falla cerrado respecto de `DETERMINISTIC`.

El fallback existente sólo puede utilizarse si su propio contrato lo permite; este
gate no amplía ni redefine `support_sufficient`.

## 14. Resource / side-effect boundary

V0 debe permanecer:

~~~text
network calls             0
new external dependencies 0
database/store            0
registry                  0
PKI/signatures            0
Kernel delta              0
Planner delta             0
provider/model delta      0
authority delta           0
RDD Stage 2 delta         0
~~~

## 15. Future RED — NOT AUTHORIZED YET

Después de PASS independiente de Hardening + leyes + Design 4R + RDD Stage 1
Design Check, un RED podrá materializar como mínimo:

~~~text
GC-R01 caller-only coherent qualification → no DETERMINISTIC
GC-R02 missing external evidence → no DETERMINISTIC
GC-R03 wrong candidate → no DETERMINISTIC
GC-R04 wrong bundle digest → no DETERMINISTIC
GC-R05 wrong catalog digest → no DETERMINISTIC
GC-R06 structural FAIL → no DETERMINISTIC
GC-R07 structural INCONCLUSIVE → no DETERMINISTIC
GC-R08 completeness FAIL/INCONCLUSIVE → no DETERMINISTIC
GC-R09 independence review FAIL/INCONCLUSIVE → no DETERMINISTIC
GC-R10 verification material review FAIL/INCONCLUSIVE → no DETERMINISTIC
GC-R11 qualification review FAIL/INCONCLUSIVE → no DETERMINISTIC
GC-R12 duplicate matching evidence → no DETERMINISTIC
GC-R13 stale evidence after candidate/material change → no DETERMINISTIC
GC-R14 exact externally reviewed evidence may become DETERMINISTIC-eligible
GC-R15 authority_effect != none rejected
GC-R16 unbounded/generator input rejected without consumption
GC-R17 no Kernel/provider/model/network/store/registry/Stage2 effect
~~~

Estos IDs son design candidate, no RED ejecutado.

## 16. Correction Budget candidato

Si el pre-RED gate autoriza implementación:

~~~text
allowed production files:
  - src/malak/capabilities/_engineering_analysis.py

allowed test files:
  - tests/test_e3_routing_qualification_binding_v0.py
  - tests/test_e3_governed_support_evidence_routing_v0.py

new dependencies: 0
Kernel delta: 0
runtime/provider delta: 0
architecture delta: 0
authority delta: 0
max bounded correction rounds: 2
~~~

La necesidad de un segundo production file requiere STOP y scope review.

## 17. Out of scope

- modificación de PR #235;
- `support_sufficient`;
- Kernel / Planner / Registry;
- provider/model/runtime;
- persistent store/database;
- receipt registry;
- PKI/signatures;
- authenticated human identity;
- network validation;
- RDD Stage 2;
- Ready / merge;
- cambios normativos.

## 18. Rollback

Mientras este gate sea sólo documental:

~~~text
rollback = revert design-record commit
runtime effect = 0
authority effect = none
~~~

Una implementación futura deberá conservar rollback al comportamiento anterior
sin migraciones persistentes.

## 19. Cuatro preguntas de ley — Writer precheck

Blueprint:
- Kernel delta 0.
- boundary localizado en E3 routing.
- WRITER CANDIDATE PASS.

Cognitive Constitution:
- evidencia exacta antes de reliance.
- incertidumbre no se convierte en PASS.
- WRITER CANDIDATE PASS.

Governance Constitution:
- evidence != authority.
- Owner conserva Ready/Merge.
- WRITER CANDIDATE PASS.

Kernel complexity:
- no Kernel delta.
- no framework/registry nuevo.
- WRITER CANDIDATE PASS.

Estas disposiciones no sustituyen revisión independiente.

## 20. Design 4R — Writer precheck

Risk:
- riesgo dominante: false-positive DETERMINISTIC por self-certification.
- mitigación: evidencia externa + exact binding + fail-closed.
- WRITER CANDIDATE PASS.

Readability:
- una responsabilidad: determinar elegibilidad de consumo de qualification.
- sin manager/framework.
- WRITER CANDIDATE PASS.

Reliability:
- bindings explícitos e invalidación por candidate/material change.
- WRITER CANDIDATE PASS.

Resilience:
- missing/stale/ambiguous/unverifiable → no DETERMINISTIC.
- WRITER CANDIDATE PASS.

Terminal:

~~~text
PENDING INDEPENDENT DESIGN 4R
~~~

## 21. RDD Stage 1 Design Check — Writer precheck

El diseño preserva explícitamente:

- candidate identity strategy;
- baseline/candidate/material binding;
- evidence provenance;
- Writer / Reviewer / Validator / Authority separation;
- PASS | FAIL | INCONCLUSIVE para gates/reviews;
- INCONCLUSIVE != PASS;
- candidate/material change invalida evidencia afectada;
- bounded correction;
- independent validation cuando aplique;
- authority_effect = none;
- RDD Stage 2 NOT AUTHORIZED.

Writer precheck:

~~~text
CANDIDATE PASS
~~~

Terminal:

~~~text
PENDING INDEPENDENT RDD STAGE 1 DESIGN CHECK
~~~

## 22. Estado del gate

~~~text
Owner authorization for design gate        YES
G0 / admission                             DESIGN CANDIDATE
G1                                         DESIGN CANDIDATE
Critical Contract Hardening                PENDING INDEPENDENT REVIEW
Four Questions                             WRITER CANDIDATE PASS
Design 4R                                  PENDING INDEPENDENT REVIEW
RDD Stage 1 Design Check                   PENDING INDEPENDENT REVIEW

RED                                         NOT AUTHORIZED
GREEN                                       NOT AUTHORIZED
PR #235                                     FROZEN
PR #239                                     DRAFT
Ready                                       OWNER ONLY
Merge                                       OWNER ONLY
RDD Stage 2                                 NOT AUTHORIZED
authority_effect                            none
~~~

## 23. Siguiente transición lícita

~~~text
independent pre-RED review
        ↓
Critical Contract Hardening
        ↓
Four Questions
        ↓
Design 4R
        ↓
RDD Stage 1 Design Check
        ↓
Owner decision on RED
~~~

No se implementa routing ni se modifica PR #235 dentro de este gate.
