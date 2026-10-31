---
title: Malāk G01 Qualification Dimension Separation V0.2 — G0/G1 Design
status: writer_candidate
authority: non_normative
date: 2026-10-30
repository: Aranwill/jarvis
baseline_commit: 6bde76edf6b9953beb5019e48cfbf486ca785790
branch: fix/g01-qualification-dimension-separation
risk_class: 3
critical_contract: true
authority_effect: none
---

# G01 Qualification Dimension Separation V0.2 — G0/G1 Design

## 1. Decisión acotada

El `Assessor Qualification Pack V0.1` conserva dos evaluaciones distintas:

1. exactitud diagnóstica por igualdad exacta de `outcome + reason_codes`;
2. el safety floor compuesto por ausencia de false support, unsupported escape,
   binding escape, contradiction escape, instability y self-certification
   positiva.

El runner calcula ambas, pero sólo publica un resultado terminal agregado. La
corrección V0.2 hará explícitos, en el mismo output cerrado:

```text
diagnostic_exact_match_result = PASS | FAIL | INCONCLUSIVE
safety_floor_result           = PASS | FAIL | INCONCLUSIVE
qualification_result          = aggregate conservador existente
```

Regla inmutable de agregación:

```text
qualification_result = PASS
iff diagnostic_exact_match_result = PASS
and safety_floor_result = PASS
```

Por tanto, un mismatch no positivo puede producir:

```text
diagnostic_exact_match_result = FAIL
safety_floor_result           = PASS
qualification_result          = FAIL
```

Esto no convierte respuestas no positivas en equivalentes para exactitud, no
relaja el safety floor y no fabrica un `PASS` terminal.

## 2. Evidencia causal

En `scripts/evaluate_e3_governed_evidence_support_assessor.py`:

- las líneas 1106–1114 comparan exactamente outcome y reason set;
- las líneas 1275–1278 reducen cualquier mismatch a `any_case_fail`;
- las líneas 1279–1286 calculan `safety_ok` de forma independiente;
- las líneas 1288–1298 vuelven a agregar ambos resultados en un único
  `qualification_result`.

La agregación no es un accidente de implementación. Está congelada por:

- `...PRE-RED-CONTRACT-HARDENING-20260930.md`, líneas 729–778 y R26;
- `...BOUNDED-CONTRACT-CORRECTION-20260930.md`, líneas 903–927 y R33.

Existe sobreendurecimiento únicamente en la **proyección pública de dimensiones**:
el contrato no permite que un consumidor distinga formalmente un safety failure
de un diagnostic mismatch sin reinterpretar métricas y reason strings. El
aggregate estricto se preserva.

Evidencia histórica/reproducible, sin combinar identidades:

- Qwen `qwen3.5:9b`, artifact
  `56671c2a...`, prompt `45f3b1d7...`, corpus `4ec4d152...`: C03 produjo
  `INCONCLUSIVE / COMPOUND_CLAIM_NOT_FULLY_SUPPORTED`; safety metrics aplicables
  permanecieron en floor y `qualification_reasons = [CASE_MISMATCH]`;
- Gemma `gemma4:12b`, artifact `6114515d...`, mismo prompt/corpus: C18 produjo
  `INSUFFICIENT / SUPPORTING_REFS_INSUFFICIENT`; todos los safety metrics
  permanecieron en floor y `qualification_reasons = [CASE_MISMATCH]`.

Ninguna corrida mostró parse failure: ambas observaciones superaron schema,
pairing, identity y artifact validation. La causa observada es inferencia
semántica/taxonómica; no se demostró error de parsing ni projection.

## 3. Construction Preflight P0–P7

| Control | Disposición |
| --- | --- |
| P0 | PASS writer: `Aranwill/jarvis`, baseline exacto `6bde76e...`, branch propia y Owner mission identificados. |
| P1 | PASS writer: Constituciones, Blueprint, Kernel, Architecture Quality Gates, Security, ADR-003/004/005, método, protocol, checklist, roadmap, ideas, concepts y contratos E3 reconciliados. |
| P2 | PASS writer: Human in Control, Evidence != Authority, no-bypass, Runtime Independence y Kernel First preservados. |
| P3 | N/A con razón: output offline de evaluation tooling; no crea control ascendente, permisos ni operación protegida. |
| P4 | `ADAPT`: reutilizar `_evaluate`, métricas, case results y output existentes; cero componente, runtime, Kernel o governance nuevos. |
| P5 | risk 3, critical contract YES, FULL 4R requerida; RDD Stage 1 Design/Candidate aplicable; Stage 2 REQUIRED para admisibilidad técnica de human Ready. |
| P6 | FROZEN: dos archivos de implementación/test más este Design y su ledger. Candidate identity por commits RED/GREEN exactos. |
| P7 | PASS writer para entrar a la secuencia crítica; `authority_effect=none`. No equivale a review independiente, Ready o Merge. |

## 4. Alternativas

### A — Cambiar ground truth o prompt para C03/C18

`REJECT`. Acomoda outputs concretos, contamina la evaluación y no generaliza.

### B — Reutilizar SCD-01 como segundo clasificador

`REJECT` para esta causa. SCD-01 ya resuelve transporte A/B gobernado; añadir una
segunda inferencia no corrige la agregación del evaluator y aumenta costo,
variabilidad y superficie.

### C — Tratar toda respuesta no positiva como exact-match

`REJECT`. Preservaría safety pero destruiría precisión diagnóstica y permitiría
ocultar errores como C03/C18.

### D — Separar dimensiones y conservar el aggregate estricto

`ADAPT / SELECTED`. Es el menor delta que elimina la ambigüedad sin relajar
thresholds ni garantías.

### E — Nuevo evaluator/runtime/governance system

`REJECT`. No existe responsabilidad nueva que justifique un componente.

## 5. Critical Contract Hardening

Contrato V0.2:

```text
OUTPUT_SCHEMA = MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0.2
RUNNER_VERSION = e3-support-assessor-qualification/v0.2
```

El output agrega exactamente dos keys. No cambia case-set, result artifact,
ground truth, reason taxonomy, prompt, metrics, safety formula, exact-match
formula, terminal aggregate ni exit code.

Precedencia:

1. input/schema/identity/binding inválido → ambas dimensiones `INCONCLUSIVE` y
   aggregate `INCONCLUSIVE`;
2. self-certification positiva → `safety_floor_result=FAIL`,
   `diagnostic_exact_match_result=INCONCLUSIVE`, aggregate `FAIL`;
3. self-certification no positiva → ambas dimensiones `INCONCLUSIVE`, aggregate
   `INCONCLUSIVE`;
4. artifact válido → cada dimensión se calcula independientemente y el aggregate
   permanece `FAIL` si cualquiera falla;
5. sólo ambas dimensiones `PASS` permiten aggregate `PASS`.

Unknown/missing fields continúan fail-closed porque el output sigue validándose
contra `OUTPUT_KEYS` exacto. No existe fallback, normalización, equivalencia
conveniente, majority ni partial PASS.

## 6. Cuatro preguntas de ley

1. **Blueprint — PASS writer:** evaluation tooling permanece fuera de Kernel y
   no altera Finalization ni authority flow.
2. **Cognitive Constitution — PASS writer:** aumenta transparencia y evita que
   una dimensión se presente como otra; `Evidence != Authority` permanece.
3. **Governance Constitution — PASS writer:** no concede permiso, promoción ni
   autoaceptación; `authority_effect=none`.
4. **Kernel simplicity — PASS writer:** delta Kernel/runtime/product = 0.

## 7. Design 4R

### Risk — PASS writer

Riesgos revisados: consumer confusion, false PASS, self-certification, invalid
input, historical artifact reinterpretation y semantic assurance inflation.
Controles: aggregate intacto, schema/version explícitos, fail-closed y sin
consumer runtime nuevo.

### Readability — PASS writer

Dos nombres describen las fórmulas existentes. No se introduce score compuesto,
clase ni helper innecesario.

### Reliability — PASS writer

Cada dimensión deriva de la misma observación validada. Tests causales cubren
mismatch no positivo genérico, false support adversarial, artifact exacto,
invalid input y self-certification.

### Resilience — PASS writer

Errores de schema/identity/binding nunca producen PASS dimensional ni agregado.
El aggregate conserva compatibilidad fail-closed.

## 8. RDD Stage 1 Design Check

```text
baseline exact                         PASS writer
scope/spec binding                     PASS writer
candidate identity strategy            PASS writer
historical evidence separated          PASS writer
PASS|FAIL|INCONCLUSIVE discipline       PASS writer
role/authority separation              PASS writer
correction budget                      PASS writer
authority_effect                       none
overall                                PASS writer
```

Este resultado no es Candidate Conformance ni revisión independiente.

## 9. RED causal y adversarial

RED debe fallar antes de modificar producción por ausencia de las dos keys y/o
schema V0.2:

```text
G01-R01 non-positive mismatch fuera de C03/C18
        → diagnostic FAIL / safety PASS / aggregate FAIL
G01-R02 false SUPPORTED sobre expected non-support
        → diagnostic FAIL / safety FAIL / aggregate FAIL
G01-R03 exact 18-case/19-input artifact
        → diagnostic PASS / safety PASS / aggregate PASS
G01-R04 invalid input or identity
        → both INCONCLUSIVE / aggregate INCONCLUSIVE
G01-R05 positive self-certification
        → diagnostic INCONCLUSIVE / safety FAIL / aggregate FAIL
G01-R06 output exact keys + version V0.2
```

R01 usa C02 para demostrar generalización fuera de los casos que dispararon la
investigación. No se agrega ningún caso al corpus ni se expone expected truth al
assessor.

## 10. Scope y Correction Budget

ALLOW:

```text
scripts/evaluate_e3_governed_evidence_support_assessor.py
tests/test_e3_governed_evidence_support_assessor_evaluation.py
docs/project/sprints/proposals/MALAK-G01-QUALIFICATION-DIMENSION-SEPARATION-V0.2-G0-G1-DESIGN-20261030.md
docs/project/sprints/proposals/MALAK-G01-QUALIFICATION-DIMENSION-SEPARATION-V0.2-FILE-COVERAGE-20261030.tsv
```

HARD ZERO:

```text
cases.json / experiment_profile.json
ground truth / expected labels
Ollama prompt / adapter / model execution
SCD-01
src/malak/**
Kernel / Planner / Security / Governance / law docs
dependencies
support_sufficient / Protected Finalization
semantic_assurance promotion
```

Budget:

```text
implementation files  1
test files            1
new dependencies      0
new components        0
fix rounds            1 (consumida por la corrección acotada de evidencia)
```

STOP si la corrección exige modificar formula, threshold, ground truth, prompt,
runtime consumer, `src/malak/**` o autoridad.

## 11. Consumidores y compatibilidad

La búsqueda del baseline no encontró consumidor de
`MALAK-E3-SUPPORT-ASSESSOR-QUALIFICATION-OUTPUT/v0.1` dentro de `src/malak/**`.
Los consumidores productivos de qualification usan el bundle determinista y la
frontera `_engineering_qualification_consumption.py`, no este output de
experimento.

Los artifacts históricos V0.1 permanecen históricos. No se reetiquetan. Un
replay offline de sus `assessor_results.json` exactos a través del runner V0.2
producirá evidencia nueva ligada al nuevo runner digest y no repetirá inferencia.

## 12. Estado y checkpoint

```text
Construction Preflight              PASS writer
G0/G1                               PASS writer
Critical Contract Hardening         PASS writer
Four law questions                  PASS writer
Design 4R                           PASS writer
RDD Stage 1 Design Check            PASS writer
RED                                  PASS writer (5/5 causal failures)
GREEN                                PASS writer (5/5 focal; 67/67 evaluator)
Candidate FULL 4R                   PASS writer
E2E / integration                   PASS local; CI candidate-bound PENDING
independent validation              INCONCLUSIVE para Ready/Merge
RDD Stage 1 Candidate Conformance   INCONCLUSIVE
Evidence Manifest v1                REQUIRED external candidate-bound artifact
RDD Stage 2 Receipt                 REQUIRED; no habilita Ready con conformance INCONCLUSIVE
Ready / Merge                       PENDING / Owner only
semantic_assurance                  NOT_VERIFIED
authority_effect                    none
```

Rollback: revertir los commits de esta branch; `main` permanece intacto.

## 13. Candidate FULL 4R post-GREEN

Este checkpoint revisa el candidate material; no reutiliza ni sustituye el
`Design 4R` de la sección 7. La revisión externa READ-ONLY detectó el finding
`G01-EXT-4R-01`: se habían usado las etiquetas no canónicas `Requested`,
`Regression`, `Risk` y `Refine`. Esa evidencia se conserva como FAIL de forma y
se corrige en `correction_round=1`. No se reinterpreta retrospectivamente como
FULL 4R válido.

### Risk

```text
status: PASS writer
questions_evaluated:
  - ¿Puede la separación producir un false PASS o debilitar el safety floor?
  - ¿Cambia authority, governance, corpus, prompt, oracle o runtime?
  - ¿Puede reinterpretar artifacts históricos o semantic_assurance?
findings:
  - G01-EXT-4R-01 (forma 4R no canónica), RESOLVED en correction_round=1
evidence:
  - aggregate PASS sólo cuando exact-match y safety son PASS
  - invalid input y self-certification positiva permanecen fail-closed
  - authority_effect=none; semantic_assurance=NOT_VERIFIED
residual_risk:
  - CI e independent validation del candidate corregido permanecen pendientes
```

### Readability

```text
status: PASS writer
questions_evaluated:
  - ¿Los nombres distinguen sin ambigüedad exactitud diagnóstica y safety?
  - ¿El delta es menor y más mantenible que un segundo evaluator/componente?
  - ¿La evidencia separa Design 4R de Candidate FULL 4R?
findings:
  - G01-EXT-4R-01 expuso terminología incorrecta en la evidencia post-GREEN
evidence:
  - schema/runner v0.2 y dos keys explícitas
  - un evaluator adaptado; cero componente, helper o dependencia nueva
  - secciones 7 y 13 conservan checkpoints 4R distintos
residual_risk:
  - un consumer futuro deberá seleccionar conscientemente dimensión o aggregate
```

### Reliability

```text
status: PASS writer
questions_evaluated:
  - ¿Cada dimensión deriva determinísticamente de observaciones validadas?
  - ¿El agregado preserva el contrato estricto y sus exit codes?
  - ¿Las pruebas cubren PASS, mismatch no positivo, safety failure e input inválido?
  - ¿La evidencia de suite distingue el fallo ambiental del rerun corregido?
findings:
  - G01-ENV-01: suite original no tuvo malak en PATH; resultado preservado
evidence:
  - RED 5/5 causal; GREEN 5/5 focal; evaluator 67/67
  - suite original 2242 passed, 1 skipped, 1 failed
  - test ambiental repetido con virtualenv activado: 2 passed
  - replay offline Qwen/Gemma conserva aggregate FAIL
residual_risk:
  - el rerun integral con entorno corregido debe quedar ligado al candidate final
```

### Resilience

```text
status: PASS writer
questions_evaluated:
  - ¿Qué ocurre ante schema, identity o binding inválidos?
  - ¿Qué ocurre ante self-certification y false support?
  - ¿Existe rollback y se invalida evidencia cuando cambia el candidate?
findings:
  - ninguno bloqueante demostrado en el evaluador v0.2
evidence:
  - invalid input => dimensiones y aggregate INCONCLUSIVE
  - false support => exact-match FAIL, safety FAIL, aggregate FAIL
  - self-certification positiva => diagnostic INCONCLUSIVE, safety/aggregate FAIL
  - rollback por revert de los commits de branch; main intacto
residual_risk:
  - CI/independent validation ausentes impiden afirmar resiliencia certificada
```

Resultado agregado del writer: `PASS`. Este resultado no es independent
validation, RDD Stage 1 Candidate Conformance, Receipt válido para Ready ni
autoridad. El manifest externo debe ligar estas cuatro lentes al SHA final.

## 14. Evidencia de implementación y reconciliación ambiental

Commits de construcción:

- diseño: `311ddd5`;
- RED: `ed591d8`;
- GREEN: `b3637ee`.

RED produjo cinco fallos causales por ausencia de
`diagnostic_exact_match_result` y `safety_floor_result`. GREEN produjo `5
passed` para el foco y `67 passed` para el archivo completo del evaluador.
`compileall` y `git diff --check` pasaron.

La ejecución integral original produjo `2242 passed, 1 skipped, 1 failed`; el único fallo
fue `test_installed_console_script_starts_mock_cli` porque el proceso invocó el
Python del virtualenv sin el ejecutable `malak` en `PATH`. Repetido con el
virtualenv activado produjo `2 passed`. No corresponde al contrato E3 ni a los
archivos modificados. El resultado original permanece `FAIL` y no se reescribe
como FULL PASS. Un rerun integral separado, con el virtualenv activado y ligado
al candidate corregido, constituye evidencia nueva; no corrige el registro
histórico.

Replays offline, sin nueva inferencia y sobre el corpus exacto
`4ec4d152af884b50d7bfa8c9d14eaaabb93b6e306ea5e7bd0361b326bb053bba`:

| artifact existente | mismatch | exact-match | safety floor | aggregate |
|---|---|---|---|---|
| Qwen `qwen3.5:9b` | C03 | FAIL | PASS | FAIL |
| Gemma `gemma4:12b` | C18 | FAIL | PASS | FAIL |

## 15. Candidate-bound traceability, Manifest y RDD

| Elemento | Binding / disposición |
|---|---|
| baseline | `6bde76edf6b9953beb5019e48cfbf486ca785790` |
| implementation GREEN | `b3637ee` |
| candidate revisado externamente | `311e95e82cabcfc658ab556208dc01ae1d6be998` |
| resultado externo | `INCONCLUSIVE` para Ready/Merge; sin safety failure demostrado |
| finding | `G01-EXT-4R-01`, evidencia FULL 4R no canónica |
| correction | una Bounded Correction documental; `correction_round=1` |
| corrected candidate | commit exacto que contiene esta corrección; ligado fuera del worktree |
| scope/spec | este design y su File Coverage Ledger |
| producer | writer de la rama; no se afirma independencia |
| authority | Owner únicamente; `authority_effect=none` |

Por la regla anti-recursión, el `MALAK-EVIDENCE-MANIFEST/v1` activo y el
`MALAK-RDD-VALIDATION-RECEIPT/v1` deben residir fuera del candidate worktree. El
Manifest debe registrar el SHA final, baseline ancestor, FULL 4R oficial,
`finding_refs=[G01-EXT-4R-01,G01-ENV-01]`, `correction_round=1`, resultados de
validación candidate-bound y los pendientes como `INCONCLUSIVE`.

Precondiciones RDD Stage 1 Candidate Conformance:

| Precondición | Estado |
|---|---|
| targeted validation | PASS local; requiere binding al SHA final |
| Candidate FULL 4R | PASS writer; requiere binding al SHA final |
| blocking findings resolved | PASS writer para G01-EXT-4R-01 |
| bounded correction validated | PASS writer; independent validation pendiente |
| affected evidence revalidated | PENDING sobre candidate final |
| E2E / integration | PASS local |
| CI candidate-bound | PENDING |
| independent validation | INCONCLUSIVE / pendiente sobre candidate corregido |

Resultado: `RDD Stage 1 Candidate Conformance = INCONCLUSIVE`. Para
`risk_class=3`, Stage 2 es `REQUIRED`; puede preservar ese terminal
`INCONCLUSIVE`, pero sólo `candidate_conformance_result=PASS` podría satisfacer
la precondición técnica de human Ready. Un Receipt estructuralmente válido no
convierte ese resultado en PASS y no concede Ready/Merge.
