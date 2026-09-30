---
title: Malāk E3 Governed Evidence Support Assessor Qualification Pack V0 — G0/G1 Admission
status: admission_candidate
authority: non_normative
language: es
baseline_commit: e8b81c2786e0764c232ad750dc13d60166aa5359
trigger_finding: E008-SG-02
upstream_contract: E3 Governed Evidence Support Assessment V0
runtime_delta: 0
authority_effect: none
implementation_authorized: false
red_authorized: false
rdd_stage_2_authorized: false
---

# Malāk E3 Governed Evidence Support Assessor Qualification Pack V0 — G0/G1 Admission

## 1. Propósito

Determinar si Malāk necesita un mecanismo reproducible para **calificar candidatos
de support assessor** antes de seleccionar, integrar o confiar en alguno dentro
del path E3.

La unidad propuesta no implementa un assessor productivo. Tampoco selecciona
modelo, provider, NLI, embeddings, RAG, GraphRAG ni un segundo modelo obligatorio.

La pregunta acotada es:

> ¿Cómo puede Malāk medir, de forma reproducible y con ground truth independiente,
> si un mecanismo candidato de assessor cumple el safety floor congelado por el
> contrato V0, sin convertir el evaluator, su score o el resultado de la evaluación
> en autoridad?

Principios:

```text
assessor candidate != qualified runtime producer
evaluation PASS != production authorization
evaluation score != semantic truth
judge confidence != support sufficiency
same-model agreement != independence
evidence != authority
```

## 2. Baseline y necesidad actual

Baseline de admisión:

```text
main@e8b81c2786e0764c232ad750dc13d60166aa5359
```

Estado relevante:

```text
E3 Structured Evidence Role Binding V0       INTEGRATED — PR #222
E3 Governed Evidence Support Assessment V0   INTEGRATED — PR #224
E008-SG-02                                    OPEN
semantic_assurance                            NOT_VERIFIED
support_sufficient                            NOT WIRED / NOT AUTHORIZED
authority_effect                              none
RDD Stage 2                                   NOT AUTHORIZED
Sprint 7.12                                   NOT AUTHORIZED
```

El contrato `assess_governed_evidence_support_v0(...)` está implementado y
validado como frontera bounded, pero no existe en el baseline un mecanismo
productivo aprobado que desempeñe el rol de `support assessor`.

La búsqueda del repositorio confirmó que las invocaciones actuales del assessment
se limitan a su test focalizado. Esto es coherente con el scope de PR #224 y no
constituye un bug, pero impide demostrar que un assessor real satisface las
garantías requeridas.

Por ello:

```text
missing qualified assessor
!= runtime defect
!= permission to select a model
!= permission to wire support_sufficient
```

La necesidad demostrada es **meta-evaluación antes de adopción**.

## 3. Reutilización antes de crear arquitectura

Malāk ya posee un patrón de evaluation tooling:

```text
E2 Structural Evidence Evaluation Pack V0 — PR #177
```

Ese patrón separa:

- case-set versionado;
- ground truth;
- runner determinista;
- identidad/digests del harness;
- métricas;
- evidence output;
- autoridad.

La dirección candidata reutiliza esas propiedades **sin crear un Evaluation
Manager, Benchmark Service, Judge Manager o framework genérico**.

```text
reuse pattern
!= reuse semantics
!= new shared framework
```

El pack E3 debe ser específico al contrato de soporte V0.

## 4. Evidencia externa revisada

Las referencias externas actúan como corroboración e implementation input, nunca
como autoridad de Malāk.

### EXT-A — OpenAI, 2026-05-29

*A shared playbook for trustworthy third party evaluations*

https://openai.com/index/trustworthy-third-party-evaluations-foundations/

Propiedad extraída:

- una evaluación debe declarar qué claim intenta sostener;
- harness, recursos/budget y validity checks forman parte de la interpretación
  del resultado;
- un score aislado no demuestra que la evaluación mida el comportamiento
  pretendido.

Disposición: **ADAPT**.

### EXT-B — Yang et al., 2026

*Quantifying and Mitigating Self-Preference Bias of LLM Judges*

https://arxiv.org/abs/2604.22891

Propiedad extraída:

- self-preference puede distorsionar evaluaciones LLM-as-a-judge;
- mayor capacidad del judge no implica automáticamente menor sesgo.

Disposición: **CORROBORATE / ADAPT**.

### EXT-C — Wang et al., 2026

*Time to REFLECT: Can We Trust LLM Judges for Evidence-based Research Agents?*

https://arxiv.org/abs/2605.19196

Propiedad extraída:

- antes de usar judges para supervisar sistemas evidence-based debe evaluarse al
  judge;
- evidence verification continúa siendo una clase difícil y requiere
  meta-evaluación específica.

Disposición: **CORROBORATE / ADAPT**.

Estas fuentes refuerzan una decisión ya coherente con el baseline:

```text
evaluate assessor before relying on assessor
```

No autorizan modelos, providers ni arquitectura externa.

## 5. Alternativas

### A — Mismo producer / mismo modelo se autoevalúa

**REJECT**

Contradice el contrato upstream. Same model + second prompt no demuestra
independencia y expone self-preference/self-certification.

### B — Algoritmo determinista general de semantic entailment

**REJECT**

Ya fue descartado en el hardening previo: no existe una regla local simple que
pueda certificar entailment semántico general sin falsa garantía o una nueva
fuente cognitiva.

### C — Elegir ahora un segundo modelo y conectarlo a E3

**OBSERVE / NO ADMITIDO COMO SIGUIENTE IMPLEMENTACIÓN**

Podría ser un candidato experimental futuro, pero seleccionarlo antes de contar
con un protocolo de calificación convertiría elección tecnológica en supuesto de
calidad.

### D — Assessor Qualification Pack V0 offline y bounded

**ADAPT — CANDIDATE DIRECTION**

Case-set + ground truth independiente + scorer determinista + identity/provenance
del mecanismo evaluado.

No llama al assessor desde CI. Califica un artifact de resultados producido por
una ejecución experimental separada y autorizada.

### E — Revisión humana como único assessor permanente

**OBSERVE / FALLBACK VÁLIDO**

La revisión humana puede seguir siendo referencia o fallback, pero usarla como
único path permanente no resuelve escalabilidad ni produce por sí sola un
contrato de evaluación reproducible.

## 6. Frontera propuesta

La futura unidad, si supera hardening y obtiene autorización separada, será
**evaluation tooling**, no runtime productivo.

Flujo conceptual:

```text
independently reviewed case-set
        +
ground truth
        ↓
authorized assessor experiment
        ↓
assessor-result artifact
        ↓
deterministic qualification runner
        ↓
metrics + per-case evidence
        ↓
PASS | FAIL | INCONCLUSIVE
        ↓
human / next admission
```

El runner de calificación:

- no selecciona modelo/provider;
- no ejecuta red;
- no llama tools;
- no persiste Memory/Knowledge;
- no modifica repo;
- no produce `support_sufficient`;
- no modifica findings E3;
- no decide integración;
- no concede autoridad.

## 7. Claim exacto del pack

El único claim que un PASS puede sostener es:

> Bajo el case-set, harness, configuración, presupuesto e identidad de mecanismo
> registrados, el assessor candidate cumplió el safety floor V0 observado.

No puede sostener:

```text
assessor is universally correct
assessor proves semantic truth
assessor is authorized for runtime
SUPPORTED == truth
PASS == support_sufficient authorization
PASS == merge/production authority
```

## 8. Corpus V0

El pack reutilizará como mínimo las clases C01–C18 ya congeladas por el
Pre-RED Contract Specification de PR #224:

```text
C01 exact support
C02 real ref but irrelevant material
C03 insufficient support
C04 compound claim, one clause supported
C05 compatible limiting evidence
C06 unresolved material counterevidence
C07 normative authority but semantically irrelevant
C08 low-authority context semantically relevant
C09 rationale overclaims refs
C10 missing resolved material
C11 stale fingerprint after statement drift
C12 evidence material changed under same logical ref
C13 equivalent ref permutation
C14 assessor unavailable
C15 malformed assessor output
C16 high-confidence but insufficient support
C17 self-certifying producer/assessor provenance
C18 scope expansion required
```

El contenido exacto de fixtures y labels deberá congelarse durante Critical
Contract Hardening. La ground truth no puede derivarse únicamente del mecanismo
bajo evaluación.

## 9. Ground truth y separación de roles

Mínimo:

```text
case author
!= ground-truth reviewer
!= qualification runner implementation actor
!= assessor candidate
!= production authority
```

No se exige que cada rol sea una persona distinta en todo contexto, pero la
evidencia debe demostrar que el mecanismo evaluado no creó o aprobó su propio
ground truth.

Si la independencia no puede demostrarse:

```text
evaluation result = INCONCLUSIVE
```

## 10. Identidad de evaluación

Un resultado comparable deberá quedar ligado como mínimo a:

```text
malak_baseline_commit
case_set_schema_version
case_set_digest
ground_truth_review_digest
qualification_runner_version
qualification_runner_digest
assessor_mechanism_id
assessor_mechanism_version
assessor_config_digest
assessor_result_artifact_digest
harness_policy_version
harness_policy_digest
budget_manifest_digest
```

Si el mecanismo es model-based, la identidad deberá incluir además, según
aplicabilidad:

```text
provider identity
model identity/version
weights/artifact identity when locally controlled
system/prompt template digest
generation/runtime settings
input/output byte budgets
attempt/retry policy
```

Cambiar materialmente cualquiera de estas entradas invalida comparación directa
sin reevaluación.

## 11. Resultado y schema conceptual

Resultado terminal del pack:

```text
PASS | FAIL | INCONCLUSIVE
```

Semántica:

- `PASS`: safety floor observado y ningún case crítico inválido bajo la identidad
  exacta evaluada;
- `FAIL`: al menos una violación material del safety floor o case crítico;
- `INCONCLUSIVE`: ground truth, binding, identity, artifact, harness o evidencia
  insuficiente para emitir PASS/FAIL confiable.

Cada case deberá preservar:

```text
case_id
expected_disposition
observed_disposition
expected_reason_class
observed_reason_codes
case_result
mismatch_reasons[]
```

El output global deberá preservar `authority_effect = none`.

## 12. Métricas y safety floor

Métricas existentes que deben calcularse cuando sean materialmente evaluables:

```text
false_support_acceptance_rate
unsupported_claim_escape_rate
false_inconclusive_rate
contradiction_handling_recall
assessment_stability_on_equivalent_inputs
binding_drift_detection_rate
```

Safety floor heredado y no relajable:

```text
false support acceptance                         = 0
binding drift escapes                            = 0
unresolved counterevidence promoted to SUPPORTED = 0
self-certification promoted to SUPPORTED         = 0
```

`false_inconclusive_rate` se mide; no se convierte todavía en threshold
arbitrario. Optimizar cobertura nunca puede relajar el safety floor.

Para mecanismos probabilísticos, número de repeticiones, temperatura, seed
cuando exista, budgets y estabilidad deberán congelarse en Critical Contract
Hardening antes de RED. Esta admission no inventa esos números.

## 13. Seguridad

### Prompt & Context Trust Boundary

**REQUIRES_REINFORCEMENT**

Claim, rationale y evidence packet son untrusted data. Ningún contenido embebido
puede modificar el protocolo del evaluator.

### AI Supply-Chain Trust

**CONDITIONAL / DEFERRED**

Se activa sólo al seleccionar un modelo/provider/weights real. No es requisito
para construir el pack determinista.

### Data disclosure

**NO NEW DISCLOSURE IN V0 PACK**

El case-set deberá usar material de evaluación controlado. Una ejecución futura
contra providers remotos requerirá gate separado para disclosure y data
classification.

### Resource Governance

**REQUIRES_FREEZE BEFORE MODEL-BASED RED**

Budget, attempts, retries y límites de entrada/salida forman parte del resultado
de evaluación.

### Human in Control

**PRESERVED**

PASS del pack sólo habilita revisión/admission posterior. No habilita producción.

## 14. Relación con `support_sufficient`

Fuera de scope:

```text
assessment outcome
        X
support_sufficient
```

Ni el pack ni un assessor candidate pueden escribir directamente
`support_sufficient`.

El mapping:

```text
GovernedEvidenceSupportAssessmentV0
→ future signal producer / adapter
→ Assurance Signal Boundary
```

requiere freeze y authorization separados.

## 15. Candidate implementation surface futura

Si se autoriza después de hardening:

```text
evaluations/e3_governed_evidence_support_assessor_v0/cases.json
scripts/evaluate_e3_governed_evidence_support_assessor.py
tests/test_e3_governed_evidence_support_assessor_evaluation.py
```

Preferencias:

- stdlib cuando sea suficiente;
- no nueva Capability;
- no service/manager/layer;
- no `src/malak/**` necesario para el pack;
- reutilizar patrones probados de PR #177 sin generalizar framework.

Cualquier necesidad de tocar `src/malak/**` durante esta unidad:

```text
STOP
→ separate gate
```

## 16. Scope prohibido

```text
src/malak/**
Kernel
Planner
Registry
Protected Finalization
Assurance Signal Boundary
support_sufficient producer/wiring
Conversation G2B
Memory/persistence
Knowledge/RAG
agents
tools
network access
model/provider selection
Ollama execution in PR validation
new dependency
RDD Stage 2
Sprint 7.12
normative changes
```

## 17. File Coverage Ledger

Ledger persistido:

`docs/project/sprints/proposals/MALAK-E3-GOVERNED-EVIDENCE-SUPPORT-ASSESSOR-QUALIFICATION-V0-FILE-COVERAGE.tsv`

Cobertura:

```text
tracked files discovered = 339
tracked files classified = 339
silently omitted files   = 0
recursive tree truncated = false
```

El archivo expresamente rechazado:

`PROJECT - MANIFIESTO MALAK (1).docx`

no está presente en este baseline. No fue abierto, resumido ni utilizado.

## 18. Gate de baseline post-merge

La admission fue iniciada desde el merge exacto de PR #227:

```text
e8b81c2786e0764c232ad750dc13d60166aa5359
```

Antes de cerrar G0/G1 como PASS debe existir Validation #692 post-merge
`SUCCESS` en Ubuntu y Windows sobre ese SHA exacto.

Si Validation #692 falla o el HEAD material cambia antes de cerrar la admission:

```text
STOP
→ rebaseline
→ affected evidence revalidation
```

## 19. G0 — necesidad

```text
need demonstrated                         PASS
existing runtime defect required          NO
existing pattern reusable                 YES — PR #177
new runtime component required            NO
model/provider choice required now        NO
support_sufficient wiring required now    NO
authority expansion                       NO
```

## 20. G1 — dirección mínima

Dirección candidata:

```text
Assessor Qualification Pack V0
→ offline evaluation tooling
→ independently reviewed ground truth
→ deterministic scorer
→ candidate mechanism identity/provenance
→ no production wiring
```

Disposición:

```text
ADAPT
```

No se promueve un framework genérico.

## 21. Cuatro lentes preliminares

### Architecture

PASS para continuar a Critical Contract Hardening.

La dirección reutiliza evaluation tooling y evita Kernel/runtime delta.

### Security

PASS condicionado.

No abre red/model/provider en V0. Los controles de supply-chain, disclosure y
resource budget se vuelven blocking antes de evaluar un mecanismo model-based.

### Governance

PASS.

`authority_effect = none`; PASS de evaluación no concede producción ni merge.

### Development

PASS.

El gate es pequeño, reversible y separa meta-evaluación de integración.

## 22. Secuencia de construcción

Estado al cierre de esta admission candidate:

```text
G0 / admission                         CANDIDATE
G1 design                              CANDIDATE
Critical Contract Hardening            NOT EXECUTED
Cuatro preguntas de ley (contract)     NOT EXECUTED
Design 4R                              NOT EXECUTED
RDD Stage 1 Design Check               NOT EXECUTED
RED                                    NOT AUTHORIZED
GREEN                                  NOT AUTHORIZED
Candidate FULL 4R                      NOT APPLICABLE YET
CI candidate-bound                     NOT APPLICABLE YET
RDD Candidate Conformance              NOT APPLICABLE YET
```

La validación de esta PR documental no sustituye ninguna etapa posterior.

## 23. G0/G1 admission result

Resultado condicionado a Validation #692 post-merge:

```text
candidate direction                     ADAPT
blocking architecture gap               NO
blocking governance gap                 NO
blocking security gap for offline pack  NO
model/provider gate                      DEFERRED until candidate mechanism selection
support_sufficient mapping               OUT OF SCOPE
runtime integration                      OUT OF SCOPE
authority_effect                         none
```

Si la precondición de baseline queda verde:

```text
G0/G1 = PASS
NEXT = Critical Contract Hardening
IMPLEMENTATION = NOT AUTHORIZED
RED = NOT AUTHORIZED
```

Si no queda verde:

```text
G0/G1 = INCONCLUSIVE
STOP
```
