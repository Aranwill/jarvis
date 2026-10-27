---
title: "Malāk — SCD-01 Runtime Bridge / pre-RED boundary"
date: 2026-10-27
authority: non_normative_pre_red_record
repository: Aranwill/jarvis
baseline_commit: 4d90dec45516ad4fbf8b762b59ab856c6aecf82f
baseline_tree: 6371af0a178ee20c1576782be0f3a67422d3e5c9
branch: research/scd01-runtime-bridge-red-20261027
critical_contract: true
risk_class: 3
status: PRE_RED_INCONCLUSIVE_STOP
implementation_status: NOT_STARTED
red_executed: false
model_calls: 0
authority_effect: none
---

# SCD-01 — Construction Preflight y frontera de integración pre-RED

## 1. Decisión exacta

El Owner autorizó el 27 de octubre de 2026 una sola rama SCD-01, preflight y trabajo hasta el checkpoint RED, **sin GREEN, 32 solicitudes A/B, G01, C03, G2, Ready o merge**. Esta autorización no modifica los controles anteriores que el Construction Protocol exige satisfacer antes de RED.

Resultado de este checkpoint: **INCONCLUSIVE / STOP para iniciar RED**. No se interpreta un antecedente de G0/G1 ni la suite offline como PASS del Critical Contract Hardening. No se crean tests falsamente rojos ni se toma un fallo de importación como RED conductual. La rama contiene por ahora este único registro preparatorio.

## 2. Identidad y materiales verificables

- Baseline: `main@4d90dec45516ad4fbf8b762b59ab856c6aecf82f`; tree reportado en revisión G1: `6371af0a178ee20c1576782be0f3a67422d3e5c9`.
- Fuente E3 actual: `scripts/run_e3_governed_blind_assessor_ollama_experiment.py`, blob de GitHub `8ee7aaf92449b41461eab64ddbabfc1678fc76a6`. Consultado desde GitHub por la sesión actual, incluidos `EXACT_SYSTEM_PROMPT`, `EXACT_USER_PREFIX`, `EXACT_RESPONSE_JSON_SCHEMA`, `ConversationRequest`, `OllamaRuntime`, `capture_provenance`, y sus presupuestos.
- Contrato público de transporte: `src/malak/core/conversation.py`, `src/malak/runtime/runtime_generation_contract.py` y `src/malak/runtime/ollama_runtime.py`; **REUSE**, sin runtime paralelo ni imports internos E3 cuya compatibilidad no se haya demostrado.
- El paquete externo `MALAK-SCD01-RUNTIME-BRIDGE-OFFLINE-20261027.zip` conserva material congelado y reporta 105 PASS sintéticos, 32 descriptores simulados y cero invocaciones al runtime real. Es evidencia preparatoria **no integrada a GitHub**.
- Prompts: A 2512 bytes / SHA-256 `22b29f8841473fdcea30fa531d6b9d7535eb1abbdecb57fca44c52df477a67ab`; B 3760 bytes / SHA-256 `82e775aba848baa49c65d9f2926e6f631c9bd5b3dcf6dd5fe4ec4390bd774076`.
- Corpus: 16 casos, SHA-256 `d1a5b859e6c45e09bf1cefc1d7053ffb24b5dff74e160bb31d63acaf976f1ae8`; schedule: 32 requests (16 A/16 B), SHA-256 `6ceae88c04a99e74ae80a3934f12fb27335f4db9038982599d84967d139d02f3`. No existe ground truth normativo 16/16.

## 3. Construction Preflight P0–P7 (scope actual)

| Control | Disposición y evidencia |
| --- | --- |
| P0 — Identidad | PASS: repo, baseline, owner instruction, rama y trabajo pre-RED identificados; ninguna modificación de `main`. |
| P1 — Jerarquía | PASS en localización/reconciliación: `AGENTS.md`, preflight, protocol, checklist, Engineering Method, Blueprint, constituciones, Security y contratos E3. G1 independiente fue PASS **solo diseño**. Hardening independiente posterior: INCONCLUSIVE/STOP; no se rebautiza como PASS. |
| P2 — Invariantes | PASS para esta documentación: Kernel First, Capability First, Runtime Independence, Human in Control, zero-trust y fail-closed intactos. |
| P3 — Topología de autoridad | PASS de diseño: adapter experimental aguas abajo → resultados informativos; nada modifica políticas, Kernel, baseline, autoridad o E3. |
| P4 — Reuse | ADAPT/COMPOSE: reutilizar tipos públicos `ConversationRequest`, `RuntimeGenerationContract`, `OllamaRuntime` y funciones puras del paquete offline cuya firma y procedencia se verifiquen. No nuevo runtime, Kernel, scorer normativo ni subsistema de gestión. |
| P5 — Riesgo/revisión | `risk_class=3`; `critical_contract=YES`; Critical Contract Hardening **INCONCLUSIVE/STOP**, por lo que la admisión a RED es **INCONCLUSIVE**. Design 4R y RDD Stage 1 Design Check no se promueven por similitud. |
| P6 — Scope e identidad | FROZEN para preparación: este registro solamente. Scope candidato de implementación posterior: un adapter experimental de despacho y tests de integración con transport interceptado, más referencias congeladas necesarias. No se autorizan cambios a `src/malak/**`, E2/E3, oracles, contratos normativos, corpus/prompt/schedule ni ejecución de modelos. Commit de RED deberá tener SHA/tree propios. |
| P7 — Resultado | `INCONCLUSIVE/STOP` para gate RED; `authority_effect=none`. Preparación documentada sin GREEN, sin ejecución, sin CI de un candidato RED. |

### Cuatro preguntas de ley — disposición preparatoria, no gate aprobado

1. Blueprint: conforme al separar experimental adapter de Kernel/Runtime (**candidato PASS**, sin implementación).
2. Cognitive Constitution: salida del modelo sigue siendo candidata y no autoridad (**candidato PASS**).
3. Governance Constitution: Human in Control, sin autoaprobación, no bypass (**candidato PASS**).
4. Kernel: complejidad **sin cambio**.
**Estos cuatro juicios no constituyen por sí mismos el gate formal post-hardening.**

### Design 4R — preparación proporcional

- **Risk**: riesgo de transformar errores de parser/provenance en etiquetas y de habilitar modelos implícitamente; prevenir con no red en tests, sin retry y fuente congelada.
- **Readability**: adapter específico y minimalista; evitar duplicar un parser genérico o crear otro runtime.
- **Reliability**: verificar firma real, dos brazos/pairing, bytes de A/B, blind projection `{statement,evidence}`, schema exacto y trazabilidad candidate-bound.
- **Resilience**: identidad del modelo, provenance antes/después, drift global `STOP`, fallos de transporte `INFRA_ERROR`, parse inválido `INVALID_OBSERVATION`; 32 filas siempre contabilizadas; `NOT_EXECUTED` nunca equivale a PASS.
Disposición: **PREPARED / NOT_APPROVED**; Candidate FULL 4R queda pos-GREEN.

### RDD Stage 1 Design Check — preparación, no PASS

Fuentes identificadas y material congelado con digest; writer/validator/Owner separados; evidencia no equivale a receipt ni autoridad; candidate RED aún inexistente. Estado **NOT_EXECUTED / NOT_ADMITTED**.

## 4. Reconciliación del hardening independiente

El informe `MALAK-SCD01-INDEPENDENT-CRITICAL-CONTRACT-HARDENING(1).md` del 26-10 terminó **INCONCLUSIVE/STOP**:

- **F-HARD-01 / GitHub inaccessible**: en esta sesión se recuperó desde GitHub el blob E3 `8ee7aaf92449b41461eab64ddbabfc1678fc76a6` y se reconstruyó `EXACT_SYSTEM_PROMPT` con las 18 cadenas literales y el separador LF del código fuente. Sobre esos **2512 bytes ASCII** se recalculó SHA-256 `22b29f8841473fdcea30fa531d6b9d7535eb1abbdecb57fca44c52df477a67ab`, igual al prompt A congelado. `SOURCE_A_HASH_MATCH=PASS` es evidencia técnica nueva del actor actual, **no** una nueva revisión independiente, ni una verificación del template completo o del despacho HTTP. B y su adición permanecen protegidos por los hashes y comprobaciones offline del paquete.
- **F-HARD-02 / construct**: el Owner ya delimitó la finalidad a **piloto observacional A/B**, no certificación causal de reparación C03. Los 12 casos con adjudicación única son **candidatos**, los cuatro ambiguos quedan aparte y no se les asigna etiqueta por conveniencia. El piloto no permite afirmar que resolvió el caso compound-parcial.
- **H-03** admisión de oracle: **PENDING pre-run**, no bloquea diseñar un RED conductual offline. Scoring normativo/exact-match sigue NO ADMITIDO.
- **H-04** provenance y perfil real: **PENDING pre-run**; el test RED deberá interceptar el transporte y demostrar la frontera, no llamar a Ollama.
- **H-05/H-06** comparabilidad, parser y fail-closed: estáticamente preparadas; integración efectiva pendiente.

**La evidencia nueva no sustituye automáticamente el dictamen independiente INCONCLUSIVE/STOP.** Antes de comenzar RED debe existir una disposición válida de Critical Contract Hardening y de los gates de diseño aplicables, ligada a esta frontera exploratoria y sin reabrir oracles ni fabricar aprobaciones.

## 5. RED conductual preparado como contrato de aceptación, NO ejecutado

Fixture auténtico previsto: par A/B `P-06ABAC84A1`, con packet SHA-256 `06abac84a103acbc3f91a0cc57912cc1afdbd7e2808b0161ac7ded0a8de2b54f`, usando prompts A y B congelados. Tests a escribir tras admisión:

1. Consumidor real: dos `ConversationRequest` construidos con `RuntimeGenerationContract(8192,256,False)` llegan al `OllamaRuntime.generate` real bajo interceptación HTTP; antes del adapter la aserción de dos despachos falla con **cero**, no por falta de imports.
2. `capture_provenance` antes y después, y drift sobre respuesta simulada, bloquean despacho posterior y preservan registros `NOT_EXECUTED`.
3. Proyección ciega solo `statement,evidence`, sin ID, brazo, oracle ni ground truth model-visible.
4. Extender a 16 pares/32 filas y negativos adversariales en alcance GREEN autorizado, manteniendo scorer externo y sin ejecutar `/api/chat` real.

No se deben crear pruebas que fallen por `ModuleNotFoundError`, ausencia de archivo, shell mal configurada o mock inconexo. El RED debe fallar por la conducta que falta.

## 6. STOP y próximo checkpoint

STOP ante divergencia de identidad E3, hashes A/B, corpus/schedule, blind projection, esquema, autoridad o alcance. No iniciar RED mientras el hardening siga bloqueante; no ejecutar GREEN, G01/C03/G2, llamadas de modelo, PR Ready ni merge. Si los controles previos se reconcilian formalmente, avanzar **en esta misma rama**; una sola secuencia RED → autorización Owner GREEN sin crear otra issue/reviewer/branch por comodidad.

Rollback del checkpoint documental: revertir el commit preparatorio dentro de la rama; `main` permanece sin cambios.

---

## 7. Reconciliación focalizada del hardening — 2026-10-27

**Autoría:** escritor/actor de implementación. **Disposición:** `EVIDENCE_RECONCILED / OWNER_DISPOSITION_PENDING`; no se reclama revisión independiente nueva ni PASS de la revisión del 26-10. El hallazgo histórico `INCONCLUSIVE / STOP` permanece visible.

### H-01 — identidad de E3, prompt y schema (comprobada)

- Del conector GitHub, baseline exacto: E3 blob `8ee7aaf92449b41461eab64ddbabfc1678fc76a6`, fuente UTF-8 de 34.023 bytes SHA-256 `4737ab98526d4114386cfee3e6f7308368558a094a269e63c752abd74e9e0b10`, coincidente con la autenticación de tres blobs de la revisión externa C03 del 27-10.
- Reconstrucción de las 18 cadenas literales de `EXACT_SYSTEM_PROMPT` unidas por LF = 2.512 bytes SHA-256 `22b29f8841473fdcea30fa531d6b9d7535eb1abbdecb57fca44c52df477a67ab`: **identidad con A congelado**.
- Schema `EXACT_RESPONSE_JSON_SCHEMA` extraído de esas constantes = 483 bytes, SHA-256 `b85c86fb85fe5bed4be6a05d15b56aa67ec988612f861cd1ad200f96de46e157`, idéntico a `RESPONSE_JSON_SCHEMA` del adaptador offline.
- JSON canónico de `{system_prompt,user_prefix,response_json_schema}`: template A SHA-256 `5af5cc933925031c5e84ce4bca00cdc4df872f91fa710a7b8f97ae8ce7c3bff5`; template B `e1a1fd3af0da8c01a618fad84a911918a40d76effedb074b38bb151c143be301`.
- B sigue siendo `A + LF + adición`; 3.760 bytes SHA `82e775aba848baa49c65d9f2926e6f631c9bd5b3dcf6dd5fe4ec4390bd774076`. A, B, adición, corpus y schedule permanecen byte-idénticos a los SHA del G1. **No** se ha probado el despacho real ni la identidad HTTP efectiva.

### H-02/H-05/H-06 — verificación offline reproducida

Paquete original `MALAK-SCD01-RUNTIME-BRIDGE-OFFLINE-20261027.zip`, manifest `BRIDGE-SHA256-MANIFEST.json`: **63/63 archivos** con SHA-256 y longitud correctos. Se repitió `python -m unittest discover -p 'test_*.py' -v` desde `scd_offline/`: **105 tests PASS, EXIT_CODE=0** (registro local `REPRODUCED-105-TESTS-20261027.txt`), cero modelos o requests HTTP.

Enfoque probado: 16 casos/32 requests (16 pares), proyección `statement,evidence` blind, rechazo de claves extra y duplicadas, pairing outcome/reason, drift sintético, conservación de las 32 filas y `exact_match=NOT_ADMITTED`. **No está integrado con la clase real `OllamaRuntime`**; RED exigirá un test conductual que confirme despacho mediante su clase auténtica y transporte HTTP interceptado, no un mock aislado.

### H-03 / F-HARD-02 — disposición explícita del constructo

La revisión ciega externa del 27-10, sellada antes de los datos técnicos, preservó 12 clasificaciones candidatas únicas y **cuatro casos sin etiqueta única**: `P-F3080D9666`, `P-34FFE4C6B5`, `P-06ABAC84A1`, `P-938319F1C3`. Se verificó igualdad del JSON sellado con el final (SHA-256 `7c2fa320120fc23c3c9c04372bdfb55dcbe9496cd6276252b75c91bd317f2d1f`). Ningún candidato equivale a ground truth aprobado.

**Interpretación acotada que requiere disposición del Owner:** la finalidad de SCD-01 se limita a comparar *observacionalmente* dos prompts en 16 pares; las cuatro ambigüedades nunca recibirán exact-match impuesto, y el conjunto de 12 es diagnóstico candidato, sin certificación de C03 ni afirmaciones de mejora de la discriminación compound-parcial. La frontera ambigua no se resuelve con el modelo: se **excluye expresamente del resultado que el piloto pueda acreditar**. Si se vuelve a exigir certificación de C03, `INCONCLUSIVE/STOP`.

### H-04 y gates restantes

- `RuntimeGenerationContract`: 8.192 tokens contexto, 256 output, `thinking=false` según fuente E3. Provenance real, drift check efectivo, identidad de modelo y `/api/chat` siguen `NOT_EXECUTED`; bloquean el **run**, no la especificación de un RED sin red.
- Cuatro preguntas de ley (evaluación del productor): Blueprint compatible; Constitución Cognitiva compatible; Constitución de Gobernanza compatible; Kernel sin cambios. No constituyen validación independiente ni promoción.
- Design 4R (productor, preparación): **Risk** exposición accidental de modelo/score o error de identidad; **Readability** un solo adapter scripts y contratos existentes; **Reliability** asserts conductuales sobre `OllamaRuntime.generate`, A/B, proyección e identidad; **Resilience** fail-closed sin retry, preservación de denominador, drift `STOP`. **Design 4R gate: NO AUTODECLARADO PASS.**
- RDD Stage 1 Design Check (preparación): baseline/lineage ligados a SHA, evidence/provenance, roles Writer–Reviewer–Validator–Authority diferenciados, terminal `PASS|FAIL|INCONCLUSIVE`, invalidación por cambio de candidate, Correction Budget una ronda, Stage 2 requerido por riesgo 3; **RDD Design Check: NO AUTODECLARADO PASS**.
- `operation_level=0` durante preparación/RED sin invocación de modelo ni cambios externos; `risk_class=3` del cambio de contrato experimental. En cualquier run real deberán reevaluarse nivel operativo y permisos.

**Estado terminal de esta reconciliación:** H-01 resuelto a nivel técnico y F-HARD-02 acotado mediante interpretación explícita; H-02/H-05/H-06 preparación offline comprobada; H-04/H-03 ejecución posterior pendiente. El antiguo `INCONCLUSIVE` no puede transformarse silenciosamente en `PASS`. Antes de RED se requiere disposición formal compatible con §5.2/§5.5 de la autoridad humana sobre el hardening revisado, más registro admitido de Design 4R y RDD Design Check. No se abren nuevos gates, ramas, PRs ni rondas de reviewer solo para transportar estas evidencias.
