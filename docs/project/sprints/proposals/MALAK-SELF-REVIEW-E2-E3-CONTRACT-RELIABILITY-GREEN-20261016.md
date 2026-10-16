---
title: "E2/E3 Contract Reliability V1 — implementación GREEN"
classification: derived
language: es
repository: Aranwill/jarvis
as_of_commit: e248756f464c8ef37ebc4a632bc084474f2a7290
date: 2026-10-16
authority_effect: none
---

# Implementación V1 — PR #329

Registro derivado, no normativo. El candidate de implementación se identifica por
el SHA exacto publicado en la PR y por los blobs del diff; este documento no
intenta incluir el SHA del commit que lo contiene. La evidencia activa posterior
permanece externa al candidate, conforme Evidence Manifest v1.

## Autorización y preflight

El Owner respondió **«Autorizo green»** al checkpoint RED
`55f3453362357d515e5dcdf5a427b4bdcff55bfb`. La transición está autorizada;
Ready y Merge siguen siendo humanos y el merge no está autorizado.
Se conserva el commit RED y su registro sin reescritura.

Preflight revalidado: P0 baseline/RED/branch exactos; P1 fuentes normativas,
contratos y diseño sin delta desde la admisión; P2 invariantes conservados;
P3 ADR-003 con retorno informativo y authority_effect=none; P4 ADAPT/COMPOSE;
P5 risk 3 / critical_contract / FULL 4R y RDD aplicables; P6 scope V1 aprobado;
P7 PASS para GREEN, no para cierre. Se mantiene la evaluación de ley, Design 4R
y RDD Design Check de PR #328; no se sustituyen validaciones del candidate.

Se reconstruyó localmente el snapshot oficial completo mediante el conector:
396 blobs con identidad verificada, tree `5bf63bf75be0c4730f53df6ee6f47c707b29aaec`
y commit firmado exacto `e248756f464c8ef37ebc4a632bc084474f2a7290`.
La firma y payload se preservaron al recuperar el objeto Git y se comprobó su SHA.
Se importó también el RED exacto; no se fabricó una identidad local equivalente.
No hay clonación autenticada ni historia completa anterior al baseline; el
baseline marca la frontera shallow local. El ancestry baseline→RED→GREEN es
verificable. El historial remoto sigue intacto.

## Cambios

- E2: schema `malak.e2.assertions.v1` derivado del catálogo admitido; strict JSON,
  claves exactas/únicas, tipos, kinds, refs y budgets UTF-8. El renderer inserta
  citas sólo desde refs validadas; se conserva el validador final de citas.
- E3 con relaciones gobernadas: schema `malak.e3.ref-role-map.v1`, mapa disperso
  exclusivo SUPPORT/LIMIT y proyección pura en orden del bundle. El parser
  canónico completo sigue ejecutándose y rechaza soporte insuficiente, overlap,
  fuentes incorrectas, mala incertidumbre y cobertura inválida de relaciones.
- E3 sin relaciones y la interpretación canónica E4 conservan el contrato previo.
- Sin autodetección ni reparación del wire anterior, fallback o retry. Se conserva
  una llamada stateless por etapa, con history=(). Prompt y output conservan
  65.536 bytes; el schema efectivo queda limitado antes de generar. E3 reutiliza
  el guard existente de ConversationRequest, sin cambiar core ni runtime.

Archivos productivos: `engineering_inspect.py`, `engineering_analyze.py`.
El shared parser `_engineering_analysis.py`, Kernel, readers, binding, runtime,
contratos públicos, ley y workflows permanecen idénticos al baseline.

## Scope adicional necesario y revisado

Se adaptaron fixtures de `test_engineering_inspect.py`,
`test_engineering_analyze.py`, role-binding, relation consumption/coverage,
`test_internal_interaction_v0.py` y `test_internal_interaction_test_v0_harness.py`.
Sólo cambió el wire emitido por los doubles; las assertions de guards canónicos,
source binding, contexto, conteos, autoridad e integración se conservan.
Los negativos de overlap/fuente siguen ejecutando directamente el parser canónico.
El archivo nuevo V1 cubre además el adapter y la ruta completa real.

El provider determinista de `scripts/evaluate_e2_structural_evidence.py` emite
assertions V1 con las mismas refs seleccionadas por su regla anterior. Su política
se versiona a v1 y cambia su digest; no se editan casos, ground truth, scoring,
umbrales, review attestation ni resultados históricos. Esta adaptación es
necesaria para verificar E2 con el wire nuevo y no introduce inferencia real.
Los casos históricos bajo evaluations/ siguen byte-idénticos.
No hay nuevos módulos, clases, dependencias, servicios, persistencia ni llamadas.

## Pruebas y errores visibles

Suite final tras todos los cambios de código/tests:

```text
.venv/bin/python -m pytest -q --tb=short
2087 passed in 35.20s
```

64 casos V1, incluidos 729 estados de asignación de seis refs ejercitados contra
la función real de proyección: disjunción, conservación del conjunto seleccionado
y de roles, orden determinista y no mutación del catálogo. Esta enumeración no
prueba entailment ni que cada estado satisfaga el contrato canónico final.

Resultados anteriores, no ocultos ni presentados como finales:
- Primera implementación: 33/34 V1 pasaban. La prueba RED de omisión esperaba
  aceptar UNRESOLVED sin refs, contradiciendo el guard canónico. Se corrigió el
  test para comprobar proyección vacía y rechazo final. Producción no se relajó.
- El schema overflow E3 reutiliza ValueError del guard vigente de ConversationRequest;
  se corrigió la expectativa de tipo del test RED, sin quitar el rechazo pre-model.
- Regresión inicial: 40 failed / 417 passed por fixtures wire antiguos y el intento
  inicial de duplicar el guard schema en el shared parser. Se eliminó ese delta
  redundante y se adaptaron fixtures; 457 passed después.
- Suite completa sobre recuperación incompleta: 304 failed / 1782 passed;
  faltaban scripts y fixtures, además de un double antiguo.
- Segunda recuperación: 84 failed / 2002 passed; se identificaron archivos locales
  truncados durante transferencia, ausencia de Git y tres fixtures E3 antiguos.
  Se recuperaron blobs completos y se verificaron sus hashes; no se publicaron
  las copias truncadas ni cambios de corpus.
- Tras reconciliar entorno/fixtures: 2086 passed; el test exhaustivo adicional
  y formato final dejan 2087 passed.

No se confunden tests del baseline, tests deterministas ni providers sintéticos
con evidencia de mejora de un modelo real. No se ejecutó /api/chat.

## Gates restantes

El candidate exacto requiere Candidate FULL 4R, E2E, CI propio, validación
independiente, RDD Stage 1 Candidate Conformance y Stage 2 Receipt risk 3.
Se registran por separado después del freeze de código. No se emite un PASS
terminal ni se declara Ready admisible por el solo resultado de pytest.
La independencia no se demuestra cambiando nombres del mismo productor.

La reducción empírica de contract failures y suficiencia de qwen3.5:9b siguen
INCONCLUSIVE. Una nueva serie real requiere materiales/configuración/provenance
congelados y contexto pre-model revalidado para estos prompts/schemas nuevos.
El freeze original no certifica el candidate cambiado. C01/C02 no se reejecutaron;
C03 continúa reservado y requiere autorización nueva para su eventual uso.

## Rollback

Antes de integración: cerrar la PR o mantenerla Draft. Para descartar únicamente
GREEN, revertir su commit conservando RED; no reset destructivo ni force-push.
Después de un eventual merge humano, revert acotado del delta de PR #329.
Issues #319/#327 siguen abiertas, PR #324 y ramas HVC no fueron modificadas.

```yaml
SOLUTION_IMPLEMENTED: YES
GOVERNANCE_RELAXED: NO
HIDDEN_RETRIES_INTRODUCED: NO
MODEL_CALLS: 0
TESTS: PASS
CONTRACT_RELIABILITY_IMPROVED: INCONCLUSIVE
QWEN_3_5_9B_SUITABILITY: INCONCLUSIVE
C03_ORIGINAL_PILOT_CONSUMED: NO
INDEPENDENT_VALIDATION: PENDING
READY_FOR_OWNER_REVIEW: NO
MERGE_AUTHORIZED: NO
authority_effect: none
```
