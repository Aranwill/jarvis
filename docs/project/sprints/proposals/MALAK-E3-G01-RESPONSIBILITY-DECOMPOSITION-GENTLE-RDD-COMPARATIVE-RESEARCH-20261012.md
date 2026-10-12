---
title: Malāk E3 / G-01 Responsibility Decomposition — Gentle AI RDD Comparative Research
status: research_candidate
authority: non_normative
language: es
date: 2026-10-12
malak_baseline: a2b9122719866258182bfef883ca0dd3737f38f0
malak_tree: a6e04894e2d63422833fb39553fea95f7656c4e7
external_reference: Gentleman-Programming/gentle-ai@caf3a01450d44909a5b75fec789856cd5ca1b70a
related_issue: 278
authority_effect: none
implementation_authorized: false
u08_authorized: false
---

# Malāk E3 / G-01 Responsibility Decomposition — Gentle AI RDD Comparative Research

## 1. Propósito

Esta investigación responde una pregunta surgida después de ejecutar la qualification V0.4 contra múltiples modelos locales:

> ¿G-01 está fallando porque todavía no encontramos un modelo suficientemente capaz, o porque el rol que estamos intentando calificar concentra demasiada responsabilidad semántica final en un componente probabilístico?

La unidad no modifica G-01, no cambia ground truth, no autoriza U08 y no promueve ningún modelo.

El objetivo es separar:

~~~
lo que Malāk ya puede resolver nativamente
vs
lo que realmente requiere interpretación semántica
vs
lo que puede ser una observación probabilística sin convertirse en autoridad
~~~

La comparación con Gentle AI es evidencia externa corroborativa. No es autoridad, dependencia ni arquitectura a copiar.

## 2. Baselines exactos

### 2.1 Malāk

~~~
repository  Aranwill/jarvis
main        a2b9122719866258182bfef883ca0dd3737f38f0
tree        a6e04894e2d63422833fb39553fea95f7656c4e7
~~~

### 2.2 Gentle AI

~~~
repository  Gentleman-Programming/gentle-ai
main        caf3a01450d44909a5b75fec789856cd5ca1b70a
tree        9149b906a1dc0955351c59b5388c7dfad9e27fb4
~~~

Fuentes externas revisadas:

- docs/architecture/organic-rdd.md
- docs/review-integration.md
- docs/architecture/the-organic-rdd-story.md
- internal/reviewtransaction/risk.go
- internal/reviewtransaction/artifact_admission.go
- internal/reviewtransaction/transaction.go
- internal/cli/review_provider_roles.go
- internal/reviewerprovider/contract.go
- reviewer lens contracts

## 3. Evidencia G-01 que se preserva

La campaña V0.4 no se reinterpreta ni rebaja.

~~~
gemma4:12b              NOT_QUALIFIED_FOR_G01 — 15/18
qwen3.5:9b              NOT_QUALIFIED_FOR_G01 — 15/18
granite4.2:8b           NOT_QUALIFIED_FOR_G01 — 13/18 — safety floor PASS
deepseek-coder-v2:16b   NOT_QUALIFIED_FOR_G01 — SAFETY_FLOOR_VIOLATION
gpt-oss:20b             MODEL_CONTRACT_INCOMPATIBLE
~~~

Conclusión preservada:

~~~
ningún modelo probado califica para el rol monolítico G-01 V0.4
~~~

Esto es evidencia válida y no constituye evidencia de que el corpus deba relajarse.

## 4. Finding principal: Malāk ya rechazaba el model-first default

La comparación no introduce por primera vez una idea externa.

El propio documento MALAK-E3-GOVERNED-SUPPORT-EVIDENCE-ROUTING-V0-G0-G1-ADMISSION-20260930.md ya establece:

~~~
GSR-01
"assessor = nuevo LLM"
REJECT como default arquitectónico
~~~

y preserva identidad/binding, material completeness, source/authority class, output schema, self-certification, fail-closed behavior y qualification reproducible como responsabilidades deterministas existentes.

También define la dirección:

~~~
deterministic coverage first
→ inferential residual only
~~~

y había estudiado una versión anterior de Gentle AI precisamente por separar deterministic, inferential e insufficient.

Por tanto:

> la investigación actual no propone abandonar la arquitectura de Malāk; evidencia que la dirección original de E3 era correcta y que la búsqueda reciente de un assessor monolítico no debe convertirse en el default futuro.

## 5. Qué resuelve ya código nativo en el assessor actual

assess_governed_evidence_support_v0(...) no delega todo al assessor.

Antes de invocarlo ya resuelve de forma nativa:

1. policy version mismatch;
2. expected binding mismatch;
3. producer == assessor;
4. missing referenced evidence material;
5. assessor unavailable;
6. malformed / invalid assessor output;
7. outcome/reason shape coherence.

El harness V0.4 materializa esta separación.

El corpus tiene 19 inputs observados, pero:

~~~
expected_candidate_invocations = 13
~~~

porque seis escenarios no dependen del modelo:

~~~
C10 missing evidence material
C11 statement binding drift
C12 evidence material binding drift
C14 assessor unavailable
C15 malformed assessor output
C17 self certification
~~~

Esto demuestra que E3 ya es parcialmente:

~~~
native envelope
+
semantic residual
~~~

y no un LLM puro.

## 6. Qué hace Gentle AI actual

### 6.1 Candidate primero

Organic RDD congela un candidate exacto antes del review.

Native Go posee candidate identity, frozen trees, risk derivation, lens selection, provider bindings, result admission, repository-derived causality checks, refutation routing, one bounded correction, targeted validation y lifecycle transitions.

### 6.2 Reviewer output = untrusted data

Los reviewer contracts indican expresamente que el actor devuelve candidate rows, no persiste estado, no crea authority, no decide transitions, no solicita fixes, no valida fixes y no autoriza delivery.

El contrato resume:

~~~
actor output is untrusted data
~~~

### 6.3 El modelo puede proponer; native re-admite

Un finding puede incluir:

~~~
severity
claim
proof_refs
evidence_class
causal_disposition
~~~

pero esos campos no se convierten automáticamente en lifecycle truth.

Native admission valida, entre otras cosas:

- subject hash;
- immutable candidate binding;
- inspection completeness;
- exact changed-path coverage;
- citation/path validity;
- repository-derived candidate causality;
- canonical identity.

Si una causalidad candidate-caused afirmada por el reviewer no puede probarse con evidencia repository-derived, la implementación puede degradarla a unknown.

### 6.4 Refutation antes de corrección

Los findings severos candidate-caused pueden pasar por un refuter.

La arquitectura actual permite:

~~~
reviewer candidate finding
→ native admission
→ deterministic/inferential classification
→ refuter
→ corroborated | refuted | inconclusive
→ bounded native continuation
~~~

Un false positive del reviewer puede ser descartado sin otorgarle autoridad al actor.

### 6.5 Delivery sigue separado

Aun un review aprobado:

~~~
review evidence != delivery authority
~~~

Commit, push, PR y release permanecen bajo policy separada/humana.

## 7. Diferencia material con nuestro G-01 actual

G-01 V0.4 pregunta hoy, en la práctica:

~~~
¿puede el candidate assessor emitir el outcome final exacto
y el reason_code final exacto para todo el corpus?
~~~

Para los 13 inputs semánticos eso concentra en el candidate:

~~~
semantic bearing
+
support sufficiency
+
compound interpretation
+
counterevidence interpretation
+
scope interpretation
+
final disposition
+
final reason taxonomy
~~~

Gentle AI califica una responsabilidad distinta:

~~~
model/reviewer proposes bounded findings
native system owns admission and lifecycle settlement
~~~

No se concluye que una sea universalmente mejor.

Sí se concluye:

> la qualification de un actor advisory y la qualification de un árbitro semántico final son problemas distintos y no deben compartir el mismo gate por accidente.

## 8. Decomposición C01–C18

Leyenda:

~~~
NATIVE
    decisión completamente determinista con información ya estructurada.

SEMANTIC
    el significado del texto sigue requiriendo interpretación.

HYBRID
    existe una frontera estructural/nativa útil, pero queda residuo semántico.

TYPING_CANDIDATE
    podría migrar materialmente a native sólo si upstream aporta un campo
    tipado explícito y gobernado; no se permite inferirlo de un hidden label.
~~~

| Case | Clase | Owner actual | Decomposición recomendada | Motivo |
|---|---|---|---|---|
| C01 | EXACT_SUPPORT | MODEL | SEMANTIC + native finalization | Decidir si el material realmente establece el claim sigue siendo semántico. El modelo no debería poseer por sí solo la promoción final a SUPPORTED. |
| C02 | IRRELEVANT_SUPPORT | MODEL | HYBRID | La no relevancia es semántica con el packet actual. Un prefilter nativo sólo sería válido con relation/coverage metadata explícita. |
| C03 | INSUFFICIENT_SUPPORT | MODEL | SEMANTIC + native finalization | Relacionado pero no suficiente exige interpretación de alcance del claim. |
| C04 | COMPOUND_PARTIAL_SUPPORT | MODEL | HYBRID / TYPING_CANDIDATE | Native podría agregar resultados por claim-part si la descomposición material fuera explícita y gobernada. Hoy el statement es texto libre. |
| C05 | COMPATIBLE_LIMITING_EVIDENCE | MODEL | HYBRID | Native conoce el rol limiting/counterevidence, pero no puede decidir sólo por estructura si el límite es compatible o contradictorio. |
| C06 | UNRESOLVED_COUNTEREVIDENCE | MODEL | HYBRID | El ref K2 ya está tipado como limiting/counterevidence; el carácter material y no resuelto sigue siendo semántico. |
| C07 | AUTHORITY_SEMANTIC_MISMATCH | MODEL | HYBRID | Source authority está estructurada fuera de la semántica, pero authoritative yet irrelevant todavía requiere bearing semántico. |
| C08 | LOW_AUTHORITY_RELEVANT_SUPPORT | MODEL | HYBRID | Authority class puede ser native; relevancia y support material siguen siendo semánticos. |
| C09 | RATIONALE_OVERCLAIM | MODEL | SEMANTIC + native finalization | Detectar que la inferencia excede el material sigue siendo una tarea semántica. |
| C10 | MISSING_EVIDENCE_MATERIAL | NATIVE | NATIVE | Ya se resuelve antes del assessor. |
| C11 | STATEMENT_BINDING_DRIFT | NATIVE | NATIVE | Fingerprint/binding drift ya es determinista. |
| C12 | EVIDENCE_MATERIAL_BINDING_DRIFT | NATIVE | NATIVE | Evidence-material digest drift ya es determinista. |
| C13 | EQUIVALENT_INPUT_PERMUTATION | MODEL + NATIVE comparator | HYBRID | Support es semántico; estabilidad de dos inputs equivalentes ya se compara nativamente. |
| C14 | ASSESSOR_UNAVAILABLE | NATIVE | NATIVE | Ya fail-closed sin model output. |
| C15 | MALFORMED_ASSESSOR_OUTPUT | NATIVE | NATIVE | Ya fail-closed por schema/output contract. |
| C16 | HIGH_CONFIDENCE_UNSUPPORTED | MODEL | SEMANTIC + hard native positive gate | Confidence nunca sustituye evidencia. La promotion a SUPPORTED debe permanecer especialmente protegida. |
| C17 | SELF_CERTIFICATION | NATIVE | NATIVE | Producer == assessor ya falla cerrado. |
| C18 | SCOPE_EXPANSION_REQUIRED | MODEL | HYBRID / TYPING_CANDIDATE | Con texto libre, scope dependency es semántica. Podría ser native si upstream entrega un external_evidence_dependency explícito y gobernado. |

Resumen:

~~~
already fully native                         6 cases
semantic residual remains                   12 cases / 13 model invocations
strong hybrid opportunities                 C04 C05 C06 C07 C08 C13 C18
directly safe to "make deterministic"        none without preserving semantics
~~~

No se recomienda keyword matching para migrar C02/C07/C18 a native.

## 9. Qué NO debemos aprender de esta comparación

No debe concluirse:

~~~
Gemma 15/18 → suficiente
Qwen 15/18 → suficiente
reason-code mismatch → irrelevante
LLM output → native truth
multiple models agree → truth
Gentle AI lo hace → Malāk debe copiarlo
~~~

Tampoco debe modificarse V0.4 para que los modelos existentes pasen.

Los FAIL observados siguen siendo FAIL del rol monolítico.

## 10. Arquitectura candidata: semantic observation, no semantic authority

Dirección de investigación candidata:

~~~
exact subject + exact evidence
        ↓
native envelope
        ↓
deterministic relation-specific oracle available?
        ├─ yes → governed deterministic result
        └─ no
            ↓
semantic reviewer candidate
            ↓
bounded semantic observations + proof refs
            ↓
native admission
            ↓
corroboration / conservative settlement
            ↓
SUPPORTED | INSUFFICIENT | INCONCLUSIVE
~~~

El reviewer no debería poseer directamente final authority, delivery authority, permission, persistent knowledge ni support_sufficient promotion.

### 10.1 Posible shape de investigación

No es schema autorizado.

~~~
GovernedSemanticEvidenceObservationV1 candidate
├── subject_fingerprint
├── evidence_ref
├── material_bearing
│   ├── MATERIAL
│   ├── NON_MATERIAL
│   └── UNKNOWN
├── semantic_stance
│   ├── SUPPORTS
│   ├── LIMITS
│   ├── CONTRADICTS
│   └── UNKNOWN
├── claim_part_ref?          # sólo si upstream provee partes gobernadas
├── proof_refs[]
└── authority_effect = none
~~~

La forma exacta requiere nuevo G0/G1; no debe implementarse desde este documento.

## 11. Regla asimétrica recomendada para SUPPORTED

El error más peligroso observado no es INSUFFICIENT ↔ INCONCLUSIVE, sino:

~~~
unsupported material → SUPPORTED
~~~

Por tanto, una arquitectura advisory debería tratar la promoción positiva de forma más estricta que una abstención conservadora.

Candidato conceptual:

~~~
model observation alone
→ MUST NOT mint SUPPORTED

SUPPORTED requires one of:
- relation-specific qualified deterministic oracle; or
- separately admitted independent corroboration; or
- separately governed human review

uncertainty / disagreement / missing corroboration
→ INCONCLUSIVE or INSUFFICIENT according to native policy
~~~

Esto no convierte una inferencia semántica en verdad determinista. Sólo impide que una única salida probabilística obtenga una promoción positiva por sí sola.

## 12. Refutation candidata

Gentle AI usa refutation sobre findings severos para reducir false positives.

Una adaptación Malāk-native podría investigar:

~~~
semantic support candidate
        ↓
would this candidate produce material positive reliance?
        ├─ no → native conservative settlement
        └─ yes
            ↓
independent corroboration / refutation boundary
            ↓
corroborated | refuted | inconclusive
~~~

Reglas:

- reviewer != refuter cuando la independencia sea requerida;
- same-model agreement != independence;
- refuter result != authority;
- native admission conserva exact binding;
- no voting arbitrario;
- no obligación de múltiples modelos en casos determinísticamente resolubles.

## 13. Qué cambia en la qualification

### 13.1 G-01 actual

Debe preservarse con su significado actual:

~~~
G-01 MONOLITHIC ASSESSOR QUALIFICATION
→ exact final disposition + exact reason taxonomy
→ V0.4 remains frozen evidence
~~~

No se recomienda cambiar sus thresholds después de observar FAILs.

### 13.2 Gate nuevo candidato

Si el Owner admite esta dirección, crear un gate separado, por ejemplo:

~~~
G-01A — ADVISORY SEMANTIC REVIEWER QUALIFICATION
~~~

Debe medir el rol realmente asignado al actor advisory.

Hard safety candidates:

~~~
authority_effect == none                         REQUIRED
exact input/candidate binding                    REQUIRED
blind ground truth                               REQUIRED
malformed/unavailable fail closed                REQUIRED
self-certification blocked                       REQUIRED
false_support_acceptance_rate == 0               REQUIRED
unsupported_claim_escape_rate == 0               REQUIRED
no tool/network/memory side effects unless separately admitted
~~~

Metrics que pueden seguir midiéndose sin convertirse automáticamente en hard authorization:

~~~
exact reason-code agreement
semantic-bearing agreement
compound-detection recall
scope-dependency recall
counterevidence recall
advisory recall
~~~

La decisión final de qué métrica es hard/soft requiere un nuevo design gate.

### 13.3 System qualification

La propiedad realmente importante debe medirse también después del settlement:

~~~
raw reviewer may be imperfect
+
native admission/refutation/settlement
        ↓
final governed system disposition
~~~

La qualification sistémica no debe asumir que un reviewer individual es perfecto; debe exigir que los errores del reviewer no atraviesen las fronteras de assurance que el sistema promete.

## 14. Impacto sobre U08

Estado actual:

~~~
G-01 monolithic PASS = false
U08                   = BLOCKED
~~~

Este documento no cambia eso.

No se permite interpretar la comparación como:

~~~
Gentle pattern found
→ waive G-01
→ implement U08
~~~

Si el Owner adopta la responsabilidad descompuesta, la secuencia correcta es:

~~~
decision #278
→ new bounded G0/G1 design
→ threat / governance / architecture review
→ RED
→ GREEN
→ independent validation
→ system qualification
→ only then reconsider U08 dependency
~~~

El Astra corrective package original no se reescribe silenciosamente.

## 15. Implicación para GPT-5.5 / nuevos modelos

La investigación no prohíbe usar un frontier model como control experimental.

Dos experimentos responderían preguntas distintas:

~~~
A. GPT-5.5 against monolithic G-01 V0.4
   → can a frontier model solve the current role?

B. GPT-5.5/local models as advisory reviewers in a future decomposed design
   → can imperfect semantic actors be safely contained by native assurance?
~~~

A puede ser útil como benchmark de capacidad.

No debe bloquear B ni convertirse automáticamente en arquitectura productiva.

La retirada informada para 2026-10-14 corresponde a superficies ChatGPT/Work/Codex; la API se trata como una frontera separada y debe verificarse nuevamente antes de cualquier implementación o ejecución real.

## 16. Decisión recomendada

### Recomendación

~~~
STOP additional local-model shopping under monolithic G-01
PRESERVE all V0.4 failures
ADMIT responsibility decomposition as next design question
KEEP U08 blocked
USE GPT-5.5 only as optional benchmark/control, not as architecture answer
~~~

Razón:

1. Malāk ya documentó deterministic-first / inferential-residual como dirección.
2. Seis de dieciocho clases ya están resueltas nativamente.
3. Los modelos probados fallan principalmente en fronteras taxonómicas semánticas diferentes, no en una única ambigüedad común.
4. Gentle AI actual aporta evidencia práctica de que un reviewer probabilístico puede ser útil sin poseer lifecycle authority.
5. La gobernanza de Malāk favorece evidence-bound native admission sobre model-first settlement.
6. Seguir probando modelos sin revisar la responsabilidad podría optimizar una interfaz que después decidamos no necesitar.

## 17. Disposición por componente

| Componente | Disposición |
|---|---|
| G-01 V0.4 | PRESERVE / no weakening |
| Current local model FAIL evidence | PRESERVE |
| E3 deterministic envelope | REUSE |
| E3 deterministic/inferential routing direction | REAFFIRM |
| Semantic reviewer candidate | ADMIT for G0/G1 design only |
| Native admission / settlement | ADMIT for G0/G1 design only |
| Refuter/corroborator | RESEARCH, not automatically required |
| GPT-5.5 API runtime | DEFER implementation pending #278 decision; optional benchmark |
| U08 | BLOCKED |
| Kernel | NO_CHANGE |
| Planner | NO_CHANGE |
| Capability authority | NO_CHANGE |
| persistent Memory | NO_CHANGE |
| normative governance | NO_CHANGE |
| Ready/Merge | Owner-only |

## 18. Terminal research result

~~~
comparative_research_result = ADMIT_RESPONSIBILITY_DECOMPOSITION_G0G1
monolithic_g01_status       = NOT_PASSED
v0_4_status                 = PRESERVED
instrument_weakening        = NOT_ADMITTED
u08                         = BLOCKED
kernel_delta                = 0
authority_effect            = none
implementation              = NOT_AUTHORIZED_BY_THIS_DOCUMENT
~~~

La próxima decisión no es qué modelo instalar.

La próxima decisión es:

> ¿Malāk quiere que un modelo sea el árbitro final de support semantics, o quiere que sea un productor acotado de evidencia semántica dentro de una frontera native que conserva settlement y autoridad?

La evidencia interna y externa revisada favorece la segunda dirección, sujeta a G0/G1 formal y aprobación del Owner.
