---
title: "Malāk #334 — investigación del residual E2"
date: 2026-10-18
authority: non_normative_investigation_record
repository: Aranwill/jarvis
baseline_commit: 23de7f1ce720955190e81e1adbf140ea2b4fdd64
baseline_tree: 57b4fa23bed5a9920461ee8c4823dbf462a33a98
status: INCONCLUSIVE
implementation_status: NOT_IMPLEMENTED
authority_effect: none
---

# #334 — Resultado: INCONCLUSIVE / STOP

Este registro derivado preserva la investigación; no certifica una solución.
La subcausa histórica de C02 no está demostrada con las fuentes disponibles.
No se implementó una corrección especulativa ni se ejecutó ningún modelo.

## Identidad, autorización y alcance

El `main` remoto y el checkout inicial coinciden exactamente con el baseline y
tree del encabezado. No existe delta respecto del baseline declarado en el encargo.
La rama dedicada es `investigation/issue-334-e2-contract-residual`.
No se reutilizaron ramas de #330/#331/#332.

La instrucción del Owner autoriza investigar, implementar y preparar PR sin merge,
subordinando el avance a la demostración de causa raíz y a los gates del encargo.
Este checkpoint publica únicamente un registro de STOP, no una Implementation PR
completa ni una Design PR aprobada. El candidate de este registro se identifica
por SHA/tree en el body de la PR para evitar autorreferencia del commit.

Scope del checkpoint: este archivo únicamente. `risk_class=1` para el registro
documental sin efectos ejecutables. La eventual modificación de E2 corresponde a
`risk_class=3`, `critical_contract=true`; no se reduce su clasificación.
Kernel, Planner, gobernanza, fixtures, oracle y runtime permanecen sin cambios.

## Fuentes y límites de recuperación

Se empezó por `AGENTS.md`, Construction Preflight, Construction Protocol y
Development Checklist. Se consultaron las Constituciones, SECURITY y ADR-003;
Blueprint, Engineering Method, Architecture Quality Gates, CURRENT_STATE,
ideas y conceptos se consultaron de forma focalizada. No se declara una auditoría
integral, admisión cerrada ni lectura exhaustiva de todas las fuentes derivadas.

Se recuperaron #319/#327/#330/#334, la historia de PR #331/#332/#333 y el código
E2, helpers de validación, ConversationRequest, transporte Ollama y tests
focalizados. Las fuentes históricas informan, no conceden autoridad.

El paquete V2 se recuperó y verificó sin ejecutarlo:

```text
MALAK-PR333-G2-C02-C03-EXECUTION-PACKAGE-V2.zip
sha256=ea24f5f44b89f7a448a4f55b0ba2200071788bf9f1024cd26338d05155582554
```

Se inspeccionó sólo el script executor. No se abrieron los requests congelados,
fixtures, oracle, rubric ni expected labels. Una búsqueda de archivos devolvió
automáticamente snippets suplementarios ajenos al diagnóstico, incluidos registros
de evaluación protegidos; no se solicitaron sus cuerpos ni se utilizaron como
evidencia técnica. Este actor no reclama certificación independiente de blindness.

El paquete es anterior a la ejecución: no es un paquete de resultados de C02.
No se recibió el directorio de resultados real ni un output rechazado conservado.
La búsqueda no demuestra que no exista una copia privada en la máquina del Owner.

## Construction Preflight: disposición real

| Checkpoint | Resultado y alcance |
|---|---|
| P0 | PASS: repositorio, baseline, tree, incidente e instrucción identificados |
| P1 | PARTIAL: lectura focalizada suficiente para registrar el bloqueo; no admisión de implementación |
| P2 | PASS para investigación: no modelos, no escritura productiva, fail-closed preservado |
| P3 | PASS: findings son información ascendente, `authority_effect=none` |
| P4 | ADAPT candidato: parser, schema y safe rejection existentes; ningún nuevo manager/service/registry justificado |
| P5 | Futuro cambio: risk 3, contrato crítico, FULL 4R y validación independiente requeridos |
| P6 | Scope de fix no congelable sin atribuir la subcausa; sólo registro documental |
| P7 | INCONCLUSIVE para implementación; STOP |

No se declara Preflight PASS de implementación. El registro del bloqueo no es
una transición a G0/G1, RED o GREEN.

## Hallazgo demostrado: pérdida de discriminación del error

En `engineering_inspect.py`, `_try_parse_and_validate_inspection_output` captura
`RuntimeError` y `UnicodeEncodeError` y devuelve `None`. La capability convierte
ese resultado en `_safe_inspection_rejection(raw_analysis)`.
Ese adaptador emite siempre el mismo reason/code/detail, con digest y bytes.

En el executor V2, `FrozenProvider.generate` calcula hash/bytes del contenido y
devuelve la respuesta. No guarda el contenido en una propiedad ni en un archivo.
El bloque de fallo conserva `raw_model_response_sha256`,
`raw_model_response_bytes`, `exception_type` y `exception_message` en el estado
del intento. No conserva la excepción interna eliminada por el adaptador E2.

Por tanto, el código explica por qué la metadata pública no distingue subcausas.
No demuestra cuál de ellas ocurrió en C02. El digest sirve para comparar una
copia existente; no permite recuperar el contenido ni la rama de validación.

La recepción de una respuesta de `/api/chat` tampoco demuestra que un validador
JSON Schema independiente haya certificado todas sus restricciones. El runtime
de Malāk transporta `format`, pero no valida la respuesta contra todo ese schema.

## Probes deterministas sobre el baseline

Se ejecutaron ocho entradas sintéticas de funciones puras, sin runtime ni casos
del piloto. Cada entrada se contrastó con los keywords efectivos del schema
focused: object, required, additionalProperties, array, maxItems, uniqueItems,
string, minLength, maxLength, enum y const. `description` es anotación.
El checker exploratorio sólo cubrió ese schema; no es una nueva implementación
de JSON Schema ni una calificación del decoder de Ollama.

| Entrada sintética | Schema actual | Parser final | Subcausa sintética |
|---|---|---|---|
| Output válido con OBSERVED/R1 | admite | acepta | ninguna |
| OBSERVED con `evidence_refs=[]` | admite | rechaza | grounded assertion requires evidence refs |
| OBSERVED con ref disponible K1 | admite | rechaza | OBSERVED requires repository refs |
| Summary con token reservado | admite | rechaza | reserved evidence/analysis ref token |
| Summary de un espacio | admite | rechaza | non-empty string tras `strip()` |
| Summary con U+200B | admite | rechaza | forbidden format character |
| Summary de 4097 caracteres `á` | admite | rechaza | supera 8192 bytes UTF-8 |
| Summary con surrogate escapado | no lo excluye expresamente | rechaza | UnicodeEncodeError al codificar |

Los siete rechazos llegan al mismo `DETERMINISTIC_VALIDATION_REJECTED`.
El surrogate escapado se serializó con `ensure_ascii=True`; no se reemplazaron
bytes inválidos ni se relajó el parser. La representabilidad Unicode del runtime
no se considera demostrada por este probe Python.

Estos probes demuestran discrepancias y ambigüedad del diagnóstico agregado.
**No constituyen RED causal exacto de C02 ni un GREEN de #334.**

## Por qué #330 no demuestra cierre de esta clase completa

#330 reforzó la exposición del contrato con schema canónico, `response_contract`
y descriptions, y conservó el parser. El schema sigue sin vincular `kind` con
namespace/cardinalidad de refs y usa longitud de caracteres frente a límites de
bytes del parser. Las descriptions no implementan prohibiciones de texto.
No hay evidencia para atribuir C02 a reserved refs por analogía con C01.

Otras rutas inspeccionadas: exact keys, unknown refs, duplicate refs, duplicate
JSON keys, JSON no finito, arrays vacíos, summary/assertions/uncertainties y
validación de citas tras render. Los límites y rechazos existentes permanecen.
La duplicación de claves es una propiedad de la representación JSON antes de
convertirla en objeto; no se solventa por un schema de objeto ya decodificado.

## Diseño posible, no aprobado ni implementado

La opción mínima de observabilidad es adaptar las ramas existentes para producir
un enum de razón local cerrado y un identificador de campo local cerrado, sin
copiar valores, refs, claves desconocidas, excepciones dinámicas, traceback ni
texto rechazado. Preservar digest/bytes exactos y single-attempt semantics.
La aceptación final debe seguir usando las mismas reglas, sin normalización,
repair, partial acceptance, fallback ni retry.

Esta mejora futura diagnosticaría rechazos futuros; no recuperaría la subcausa
histórica de C02. Requiere diseño específico, tests de no leakage y validación
independiente. No se concede PASS anticipado a su seguridad.

En JSON Schema general, ramas por `kind` pueden vincular enums/cardinalidad de
refs. `pattern`/`not`/`allOf` pueden expresar determinadas restricciones; su
compatibilidad con el decoder y versión reales de Ollama no está calificada aquí.
Un `maxLength` de caracteres no equivale al límite UTF-8 del parser; imponer uno
más corto puede excluir outputs actualmente válidos y requiere decisión explícita.

Se rechazaron como respuesta al incidente: adivinar el token; ejecutar C02 de
nuevo; usar C03 para investigar; relajar el parser; sanitizar output; cambiar de
modelo/sampling; y presentar una mejora genérica como solución causal probada.
No se agrega persistencia forense al producto.

## Validación ejecutada

Entorno: Linux, Python 3.12.14, entorno local `.venv`, pytest 9.1.1 dentro del
rango dev ya declarado. No se modificaron dependencias del repositorio.
No se reclama equivalencia observada con Python 3.12.10/Windows del Owner.

```text
.venv/bin/python -m pytest tests/test_e2_e3_contract_reliability_v1.py tests/test_engineering_inspect.py -q --tb=short
137 passed in 6.75s
exit=0
```

Resultado ligado al baseline exacto; no certifica un candidate con fix.
Los tests existentes cubren aceptación, rechazos, no retry, canonicalización,
metadata segura y límites/surrogates. No se ejecutó suite completa, E2E completo
ni modelo. No se introdujeron tests RED fuera de la secuencia de admisión.

| Gate de implementación | Disposición |
|---|---|
| ROOT_CAUSE histórica C02 | INCONCLUSIVE |
| G0/G1 / Critical Contract Hardening | BLOCKED; no diseño de fix congelado |
| Cuatro preguntas de ley / Design 4R / RDD Design Check | NOT_EXECUTED para fix |
| RED causal / GREEN | NOT_EXECUTED; bloqueo anterior |
| Targeted baseline | PASS, 137 tests; no certifica solución |
| Candidate FULL 4R / E2E / CI de implementación | NOT_EXECUTED |
| Independent validation | NOT_EXECUTED; este actor no es su propio validator |
| RDD Stage 1 Candidate Conformance / Stage 2 Receipt | BLOCKED |
| Human review / Ready / Merge | NO promoción; NO merge |

Revisión proporcional del registro documental: Risk — no raw real ni autoridad;
Readability — separación expresa entre probes e incidente; Reliability — SHAs,
fuentes y resultados identificados; Resilience — STOP y preservación histórica.
No equivale a FULL 4R del producto ni a validación independiente.

## Reentrada concreta

Primero recuperar el directorio real de resultados V2, conservándolo fuera del
Git root. Leer sólo el registro de fallo y provenance autorizados, sin material
oracle/rubric/labels. Verificar baseline, contador de generación y digest/bytes
contra el incidente; no ejecutar el executor.

Si existe una copia previa del output rechazado o un registro interno con
subcausa, realizar diagnóstico offline con disclosure mínimo y autorización
forense aplicable. Si sólo existen los hashes y la excepción agregada, mantener
`ROOT_CAUSE=INCONCLUSIVE`: hará falta reformular explícitamente el criterio de
la unidad hacia hardening/observabilidad prospectiva, sin afirmar una causa
histórica irrecuperable. Esa reformulación no está asumida por este registro.

## Freeze, historial y rollback

Este checkpoint no modifica las superficies ejecutables ni vuelve a admitir G2.
No afirma invalidación por un cambio de parser/schema que no ocurrió.
Para cualquier futura corrección en las superficies enumeradas por el encargo:

```text
CURRENT_PREMODEL_FREEZE_REUSE=FORBIDDEN
CURRENT_OWNER_G2_REUSE=FORBIDDEN
new post-merge baseline -> NEW PRE-MODEL freeze
-> independent freeze validation -> NEW Owner G2
```

Estado experimental preservado:

```text
C01_ATTEMPT=CONSUMED
C01_RETRY=FORBIDDEN
C02_ATTEMPT=CONSUMED
C02_RETRY=FORBIDDEN
C03_ATTEMPT=NOT_STARTED
C03=HOLD
E3_C02=NOT_ATTEMPTED
E4=NOT_AUTHORIZED
MODEL_CALLS_THIS_INVESTIGATION=0
API_CHAT_CALLS_THIS_INVESTIGATION=0
AUTHORITY_EFFECT=none
SOLUTION_IMPLEMENTED=NO
UNIT_RESULT=INCONCLUSIVE
```

Rollback: el registro puede abandonarse cerrando la Draft PR o revertirse mediante
un nuevo commit limitado a este archivo. No se requiere rollback de producción.

## Referencias

- https://github.com/Aranwill/jarvis/issues/334
- https://github.com/Aranwill/jarvis/issues/327#issuecomment-6250524746
- https://github.com/Aranwill/jarvis/issues/327#issuecomment-6250493120
- https://github.com/Aranwill/jarvis/pull/331
- https://github.com/Aranwill/jarvis/pull/332
- https://github.com/Aranwill/jarvis/pull/333
- https://docs.ollama.com/capabilities/structured-outputs — schema en `format`,
  recomendación de reflejarlo en prompt y validar la respuesta; no certifica el
  subset ni los bytes del runtime histórico del Owner.
- https://json-schema.org/understanding-json-schema/reference/annotations —
  `description` documenta; no es assertion de validación.
