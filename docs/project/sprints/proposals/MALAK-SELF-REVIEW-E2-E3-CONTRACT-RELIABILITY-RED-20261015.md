---
title: "E2/E3 Contract Reliability V1 — checkpoint RED"
language: es
classification: derived
repository: Aranwill/jarvis
as_of_commit: e248756f464c8ef37ebc4a632bc084474f2a7290
authority_effect: none
---

# Checkpoint RED — PR-B

Documento derivado, no normativo. Registra pruebas nuevas contra el código del
baseline integrado; no certifica GREEN ni mejora empírica.

## Identidad y autorización

Design PR #328 integrada por el Owner en
`e248756f464c8ef37ebc4a632bc084474f2a7290`.
Rama: `fix/self-review-e2-e3-contract-reliability-20261015`.
El candidate completo es el commit de esta Implementation PR; el body registra
su SHA exacto. No hay autorreferencia al SHA del commit dentro de su contenido.

Test blob Git: `f367746ae469a46782dfd679af1a065d5eca124f`.
Sólo se añaden este registro y el archivo de tests; ningún archivo productivo,
test anterior, workflow, ley, dependencia o resultado histórico cambia.

El Owner autorizó reanudar con los mismos privilegios de código, tests y PR,
sin merge. El diseño integrado exige autorización humana aplicable **sobre el
RED futuro** antes de GREEN; esta autorización general no se presenta como
decisión candidate-bound sobre pruebas que todavía no existían.

## Construction Preflight revalidado

preflight_version=0.1.0; work_unit=E2/E3 Contract Reliability PR-B RED;
work_type=critical-contract implementation checkpoint; authority_effect=none.

- P0 PASS: main remoto exacto, merge humano confirmado y única PR previa abierta
  #324 identificada como research-only; no rama específica activa previa.
- P1 PASS para RED: comparación remota entre baseline anterior 5612214… y main
  demuestra que sólo se añadieron los dos documentos de PR #328. Los 191 blobs
  recuperados localmente coinciden con sus identidades oficiales, incluidos
  código/tests y fuentes aplicables. Se reutiliza la revisión documental
  integrada únicamente donde los blobs y alcance no cambiaron.
- P2 PASS: pruebas offline, sin ejecución de modelos ni cambio Kernel,
  permisos, ley, persistencia o finalización.
- P3 PASS: ADR-003; requests upstream→downstream y resultados informativos;
  ninguna prueba convierte output en autoridad.
- P4 ADAPT/COMPOSE: fixtures existentes de E2 y role-binding E3; ningún módulo
  productivo, manager, service, registry ni dependencia nuevos.
- P5 risk_class=3 para la implementación; critical_contract=YES; FULL 4R,
  RDD Stage 1 y Stage 2 requeridos para cierre posterior; no ejecutados por
  anticipado ni inferidos desde este RED.
- P6 FROZEN: test nuevo y este registro. GREEN futuro limitado al diseño
  integrado y capabilities previstas; cualquier ampliación requiere disposición.
- P7 PASS para entrar en RED exclusivamente.

Esta es revalidación incremental de una unidad ya admitida, no auditoría global.
Inventario remoto vigente: 396 blobs heredados, todos conservados. El ledger
integrado de PR #328 clasifica esos archivos; se agregan dos: tests=FULL_READ /
implementation evidence, este documento=FULL_READ / derived. Ningún archivo
REJECTED_DO_NOT_READ fue abierto como parte de esta reanudación.

## Gates pre-RED

G0/G1, hardening y RDD Design Check: diseño integrado de PR #328, sin delta de
semántica en este checkpoint. Las fuentes normativas no se modifican.
Cuatro preguntas: compatible con Blueprint (Capability First); compatible
con CC-002/003/004/005/006/011/012 (evidencia, incertidumbre y minimización);
compatible con Gobernanza (ninguna autoridad nueva); Kernel simple (delta 0).

Design 4R, revalidación del productor para RED:
- Risk PASS: negativos desconocidos/tipos/duplicados y no retry; C03 excluido.
- Readability PASS: V1 versionado y salida canónica verificados por tests.
- Reliability PASS para diseño: límites/roles/orden y una llamada explícitos;
  implementación aún ausente; no mejora cognitiva afirmada.
- Resilience PASS para diseño: malformed/overflow deben rechazar sin fallback.
  La prueba overflow usa un schema JSON válido mayor al presupuesto.

No se simula independencia. La revisión/promoción humana de PR #328 es un hecho
verificado; no se inventa un informe independiente no recibido.

## Validación ejecutada

Entorno local: recuperación parcial de 191 blobs verificados, venv existente;
no checkout Git completo. El directorio de trabajo de la ejecución registrada
fue la raíz local `baseline/`. No se afirma que exista en este host la ruta
Windows oficial. No se cambiaron dependencias.

Comando RED:

```text
.venv/bin/python -m pytest tests/test_e2_e3_contract_reliability_v1.py -q --tb=short
```

Resultado: **32 failed, 2 passed, 1.72 s**, exit 1 esperado del checkpoint RED.

Cobertura de los 34 casos:
- E2: renderer de assertions, schema con catálogo real, versión, campos extra,
  citas reservadas fuera de refs, refs inexistentes/de fuente incompatible,
  duplicación de refs, UTF-8 por campo, cardinalidad, tipos, keys duplicadas,
  NaN, JSON truncado y rechazo de prosa legacy.
- E3: proyección y preservación de clasificación/texto/incertidumbre, LIMIT
  sin soporte implícito, omisión, orden del bundle, ref desconocida, key
  duplicada, schema disperso, integración canónica, catálogo vacío y overflow
  pre-model con cero llamadas.

Los dos PASS corresponden a guards ya existentes: cita S1 desconocida en prosa
E2 y rechazo strict-JSON de una key repetida E3. No prueban el adapter futuro.

Fallos representativos:
- E2 imprime el objeto JSON como prosa en vez de renderizar citas validadas;
  response_json_schema sigue None; acepta tipos/campos/límites inválidos V1.
- E3 rechaza schema_id porque aún espera el envelope histórico; schema sin
  evidence_roles y sin versión; overflow no se detiene por presupuesto antes
  de llamar al provider.

Primera ejecución exploratoria: 33 failed / 1 passed; se corrigieron dos
problemas del test, sin cambios productivos: el guard de duplicate keys usa
el mensaje público strict JSON ya existente y el overflow ahora inyecta JSON
válido en vez de whitespace no trimmed. Ese resultado exploratorio no es el
checkpoint congelado.

Regresión del baseline:

```text
.venv/bin/python -m pytest tests/test_engineering_inspect.py tests/test_engineering_analyze.py tests/test_governed_engineering_evidence_focus_v0.py tests/test_engineering_propose.py tests/test_e3_structured_evidence_role_binding_v0.py tests/test_e3_governed_support_evidence_routing_v0.py tests/test_e3_governed_evidence_support_assessment_v0.py tests/test_ollama_runtime.py tests/test_runtime_generation_contract_red.py tests/test_internal_interaction_v0.py -q
```

**423 passed, 12.26 s**. Suite completa no ejecutada sobre recuperación parcial.
CI remoto pendiente del candidate de esta PR; se espera exit no cero en RED.
Un runner rojo en este checkpoint no es evidencia de regresión productiva;
tampoco se oculta ni se altera el workflow para volverlo verde.

## Estado de ejecución y pasos restantes

```yaml
RED_REPRODUCED: YES
RED_TESTS: 32_FAILED_2_PASSED
BASELINE_REGRESSION_TESTS: 423_PASSED
SOLUTION_IMPLEMENTED: NO
GREEN: NOT_STARTED
CANDIDATE_FULL_4R: NOT_RUN
INDEPENDENT_VALIDATION: NOT_RUN
RDD_CANDIDATE_CONFORMANCE: NOT_RUN
RDD_STAGE_2_RECEIPT: NOT_ISSUED
MODEL_CALLS: 0
C03_ORIGINAL_PILOT_CONSUMED: NO
CONTRACT_RELIABILITY_IMPROVED: INCONCLUSIVE
MERGE_AUTHORIZED: NO
authority_effect: none
```

Siguiente transición: autorización humana explícita sobre el SHA RED de esta
Implementation PR para GREEN. No requiere merge del RED ni una PR adicional.
Después: adapter mínimo, actualización justificada de fixtures que producen el
wire antiguo manteniendo sus invariantes, targeted tests, Candidate FULL 4R,
E2E/CI, validación independiente y RDD candidate-bound antes de revisión final.

Rollback actual: cerrar esta PR o revertir únicamente sus dos adiciones; no
se elimina ni reescribe evidencia histórica. C01/C02 intactos, C03 no consumido,
sin HVC ni llamadas a /api/chat. Issues #319/#327 permanecen abiertas.
