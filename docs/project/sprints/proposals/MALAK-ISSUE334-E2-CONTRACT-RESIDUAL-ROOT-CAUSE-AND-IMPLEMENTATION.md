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


## Reentrada con resultados reales V2 — 2026-10-18

Esta sección complementa el checkpoint inicial y sustituye únicamente su
afirmación de que no se había recibido el directorio real. La causa histórica
continúa INCONCLUSIVE.

El Owner adjuntó ambos ZIP. Identidad calculada:

- executor V2: `ea24f5f44b89f7a448a4f55b0ba2200071788bf9f1024cd26338d05155582554`;
- resultados V2: `e4bb7ad469a58330ba7f08fdea0325d5bef600af2906b3841ce8e303f7b1e275`.

El ZIP de resultados contiene exactamente tres archivos:
`EXECUTION-PREFLIGHT.json`, `RUN-STATE.json` y `FILES-MANIFEST.json`.
Se recalcularon y verificaron todos los hashes declarados en su manifest:

| Archivo | SHA-256 verificado |
|---|---|
| EXECUTION-PREFLIGHT.json | 21df068d4f839eb0e78a29f55d36ae5035076cad59f5559486d2632c04927dc9 |
| RUN-STATE.json | 75d54e7c605502dcf502a36fd46c282b45c7e25d580a65306806c7167de795ec |

Baseline/tree coinciden con el incidente. El registro E2 contiene una invocación
y estado CONSUMED; C03 y E3 no aparecen como ejecutados. Las capturas git_before,
git_after e inicial son iguales y limpias. La provenance antes/después coincide
salvo el timestamp, incluido digest de modelo y configuración de generación.
Esto verifica consistencia de evidencia capturada, no una reobservación del host.

La metadata interna y la del executor coinciden:

```text
output_bytes=1658
output_sha256=7034897f9b28e217c0a9c7e251e961324d1195776916d0c87be7cd6b14f5060e
reason_code=E2_OUTPUT_CONTRACT_REJECTED
validator_code=DETERMINISTIC_VALIDATION_REJECTED
```

No existe raw output ni excepción interna con subcausa en estos tres archivos.
La metadata no contiene un ref o campo que identifique la regla rechazada.
Los 1658 bytes descartan el guard de output total (>65536 bytes) y las
infracciones de límites de bytes de free-text (4096/8192): un string JSON
decodificado válido en UTF-8 no puede superar esos límites partiendo de ese
documento de 1658 bytes. Surrogates inválidos son otra clase y siguen sin
descartarse. Tampoco se atribuye por eliminación el fallo a reserved refs:
siguen posibles otras condiciones de contenido, cardinalidad, roles y JSON.

Por lo tanto, pedir nuevamente este directorio no desbloquearía la atribución.
Sólo una copia adicional previamente conservada de la respuesta o de una
subcausa podría hacerlo; no se presume que exista.

### Propuesta de reformulación explícita, pendiente del Owner

Preservar `C02_HISTORICAL_ROOT_CAUSE=INCONCLUSIVE` y redefinir la unidad como
hardening prospectivo de contrato/diagnóstico E2:

1. Diseñar taxonomy cerrada de subcausas y campos, usando sólo constantes locales.
2. Conservar rechazo, exactitud digest/bytes, no leakage y no retry/repair.
3. Evaluar y cerrar discrepancias schema/parser demostrables con casos sintéticos,
   separando lo expresable en schema de las leyes reservadas al parser.
4. Completar G0/G1, hardening, Design 4R, RDD, RED/GREEN y validaciones aplicables.
5. Mantener independiente la validación final; no autodeclarar PASS.
6. Invalidar freeze/G2 al cambiar una superficie ejecutable de las enumeradas.
7. Mantener C01/C02 consumidos y C03 HOLD; no usar el piloto para diagnosticar.

Esta reformulación elimina únicamente la condición imposible de atribuir el
incidente a bytes que no están disponibles; no reduce validación ni cambia
leyes. No se considera aprobada por el simple envío del ZIP.

CI del checkpoint documental anterior:
run `39132769875`, candidate `b3cac02bc3562c8d70d1b6dadce5d29af3585cce`,
resultado `success`. Ese PASS no certifica un fix ni este nuevo commit.
No se reejecutaron los 137 tests porque no cambió código ni apareció un fallo de
producto nuevo; las verificaciones nuevas fueron integridad y coherencia de
artefactos offline. Model calls y /api/chat permanecen en cero.

## Estado de implementación prospectiva — GREEN autorizado

Esta actualización sustituye SOLUTION_IMPLEMENTED=NO para el objetivo
prospectivo aprobado; no cambia la causa histórica de C02. El Owner autorizó
GREEN después del RED 34a7d8a..., registrado en PR #335 comment 6250855094.

Implementado: subcódigos/campos locales cerrados, diagnóstico sin raw/context,
UTF-8 exacto o digest/bytes null para string no codificable; schema focused con
ramas completas kind/ref y descriptions de todas las leyes de free-text.
Se mantienen parser fail-closed, no retry/repair y nonfocused schema sin cambios.
No hay nuevas dependencias, servicios, persistencia ni cambios Kernel/Planner.

Targeted: 192 passed in 17.45s. Comparación de 704 entradas contra el parser de
main@23de7f1: acceptance y render idénticos (56 aceptadas/648 rechazadas);
nonfocused schema idéntico en cuatro catálogos. La prueba antigua de overflow
combinado se adaptó al tamaño real del contrato, conservando su condición.

FULL 4R del candidate, E2E, full suite, CI, independent validation y RDD terminal
siguen sujetos a evidencia del candidate final. Este texto no fabrica sus PASS.
Cada rechazo histórico se conserva. C01/C02 CONSUMED, retries FORBIDDEN; C03 HOLD.

```text
SOLUTION_IMPLEMENTED=YES_PROSPECTIVE_SCOPE
C02_HISTORICAL_ROOT_CAUSE=INCONCLUSIVE
CURRENT_PREMODEL_FREEZE_REUSE=FORBIDDEN
CURRENT_OWNER_G2_REUSE=FORBIDDEN
MODEL_CALLS=0
API_CHAT_CALLS=0
authority_effect=none
```
