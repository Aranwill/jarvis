---
title: "Malāk #334 — contrato prospectivo de diagnóstico E2"
date: 2026-10-18
authority: non_normative_proposal
baseline_commit: 23de7f1ce720955190e81e1adbf140ea2b4fdd64
baseline_tree: 57b4fa23bed5a9920461ee8c4823dbf462a33a98
risk_class: 3
critical_contract: true
authority_effect: none
---

# G0/G1 — diagnóstico seguro y alineación focused

## Admisión y scope

El Owner aprobó «aprobado, avanza» tras la propuesta explícita de preservar
`C02_HISTORICAL_ROOT_CAUSE=INCONCLUSIVE` y continuar con hardening prospectivo.
La evidencia real V2 y sus hashes constan en el informe de investigación de #334.
El `main` remoto continúa exactamente en el baseline de este encabezado.
Candidate inicial de esta reentrada: `d545d6891d7442e760011581622b8b3f967ba36e`.

Necesidad demostrada: el adaptador actual elimina la distinción entre rechazos
materialmente diferentes. Además, el schema permite assertions OBSERVED con
refs knowledge o sin refs, que el parser rechaza. No se atribuye ninguno a C02.

Scope congelado: `src/malak/capabilities/engineering_inspect.py`, nuevo
`tests/test_e2_contract_diagnostics_v2.py`, adaptación de expectativas de metadata
en `tests/test_e2_e3_contract_reliability_v1.py`, este diseño, ledger e informe #334.
Fuera: helpers compartidos de E3, runtime, ConversationRequest, Kernel, Planner,
leyes, fixtures, modelos, sampling y ejecución del piloto. Dependencias nuevas: 0.

Se conserva la rama dedicada y PR #335 conforme a la instrucción específica del
Owner de trabajar todo en ella y dejarlo sin mergear. Design, RED y GREEN tendrán
commits/evidencias separados; la PR nunca se promoverá por el asistente.
La autorización GREEN posterior a RED sigue siendo un gate separado obligatorio
del Construction Protocol §5.1.1 y §5.5. No se infiere de esta aprobación pre-RED.

Construction Preflight revalidado: P0 baseline/ref/instrucción PASS; P1 fuentes
rectoras reconciliadas, clasificación y profundidad reales en ledger; P2 Human in
Control, fail-closed, Runtime Independence y Capability First PASS; P3 resultados
informativos ascendentes según ADR-003 PASS; P4 ADAPT de parser/schema/metadata;
P5 risk 3, critical contract, FULL 4R/independent validation/RDD 1+2 requeridos;
P6 scope congelado y commits exactos por checkpoint; P7 PASS para entrar al diseño.
No equivale a autorización GREEN, validación independiente, Ready ni merge.

## Reutilización y complejidad

ADAPT: schema y builder existentes, helper bounded_nonempty_string, strict JSON,
renderer y safe rejection. No se crea un servicio, manager, registry ni store.
Una excepción privada tipada podrá transportar exclusivamente subcódigo/campo
locales entre parser y adaptador; no es un contrato público ni un componente nuevo.
No transportará el raw output, valores desconocidos ni la excepción original.
La alternativa de inferir códigos desde cualquier mensaje dinámico es REJECT.
La clasificación de los fallos del helper compartido, si se utiliza, será por
igualdad contra mensajes locales completos conocidos; todo caso no reconocido
seguirá rechazado con subcódigo UNCLASSIFIED, sin copiar su mensaje.

## G1 — contrato verificable

### Diagnóstico público

Para todo rechazo E2 posterior a generación cuya respuesta sea string, el error
será RuntimeError con JSON canónico y exactamente estas keys:

```text
authority_effect
output_bytes
output_sha256
output_encoding
reason_code
validator_code
validator_detail
validator_subcode
validator_field
```

Se conservan los valores locales de reason_code, validator_code y validator_detail
de #330. `output_encoding=UTF8` implica digest/bytes de la respuesta exacta, sin
normalización. Si el string contiene un surrogate literal no codificable:
`output_encoding=INVALID_UTF8`, bytes/digest null y subcódigo OUTPUT_INVALID_UNICODE.
No se inventan bytes mediante replacement, surrogatepass ni escapes.

Taxonomy cerrada inicial:

```text
OUTPUT_EMPTY OUTPUT_LIMIT OUTPUT_INVALID_UNICODE
JSON_SYNTAX JSON_DUPLICATE_KEYS JSON_NONFINITE ROOT_TYPE EXACT_KEYS SCHEMA_ID
TEXT_EMPTY TEXT_CONTROL TEXT_RESERVED_REF TEXT_UTF8_BYTES TEXT_INVALID_UNICODE
ASSERTIONS_LIMIT ASSERTION_TYPE ASSERTION_KIND REFS_LIMIT REF_TYPE DUPLICATE_REFS
UNKNOWN_REF MISSING_REFS REF_ROLE UNCERTAINTIES_LIMIT RENDER_REF UNCLASSIFIED
```

Campos cerrados: output, schema_id, summary, assertions, assertions[].kind,
assertions[].text, assertions[].evidence_refs, uncertainties, uncertainties[].
No índices, refs, keys ni nombres derivados del output. Las keys desconocidas,
refs desconocidas y constantes JSON no finitas no se copian al diagnóstico.
El error público debe carecer de cause/context originales y su traceback
formateado por defecto no debe mostrar contenido rechazado.

Se ejecuta una sola validación y cero llamadas adicionales al provider. No repair,
retry, fallback, partial acceptance, persistence ni uso posterior del output.
Excepciones inesperadas ajenas al contrato no se convierten silenciosamente en
aceptación ni se capturan mediante `except Exception`.

### Alineación focused

El builder existente recibirá una opción focused con default false. Sólo en modo
focused, `assertions.items.anyOf` expresará las ramas de kind/ref:

| kind | catálogo permitido | minItems |
|---|---|---|
| OBSERVED | repository | 1 |
| KNOWLEDGE_CONTEXT | knowledge | 1 |
| INTERPRETATION | todos los refs seleccionados | 1 |
| UNCERTAINTY | todos los refs seleccionados | 0 |

Una rama grounded sin catálogo disponible se omite; UNCERTAINTY permanece.
Se preservan maxItems=16, uniqueItems, keys exactas y el resto del schema.
Se mantienen las propiedades comunes para compatibilidad con consumidores
existentes; las restricciones `anyOf` son adicionales según JSON Schema.
El prompt focused contiene el schema canónico completo y respeta 64 KiB.
Schema/prompt nofocused quedan iguales; sólo su error seguro gana diagnóstico,
necesario porque la misma validación es compartida por ambos modos.

Las descriptions focused explicarán también no whitespace-only, controles/formato,
surrogates y límites UTF-8. Son orientación, no enforcement. No se confunde
maxLength en caracteres con max bytes. No se reduce maxLength para simular bytes.
No se añade pattern/not/allOf como frontera de corrección no calificada.

El parser sigue siendo el enforcement final, incluso si un provider ignora una
restricción del schema. La aceptación semántica no cambia. Arrays vacíos de
assertions/uncertainties y UNCERTAINTY sin refs siguen válidos.

El soporte exacto de `anyOf` junto a otros keywords en el backend/version del
Owner queda como riesgo residual para la futura validación PRE-MODEL; no se
declara medido por tests mock. No se ejecutan modelos para calificarlo aquí.

## Critical Contract Hardening

Threat model: output no confiable intenta filtrar contenido a través de error,
unknown keys/refs, Unicode, cause/context o logs. Sólo enums/metadata local y
digest/bytes cruzan la frontera. No se serializan traceback locals.
Los límites permanecen fail-closed; el diagnóstico no interpreta evidencia como
permiso. Exact keys, duplicados, namespace y cardinalidad mantienen rechazo.
Múltiples defectos se clasifican por la primera regla determinista; no se promete
un conjunto completo de errores ni se hace un segundo parse para diagnosticar.

Reglas para RED: demostrar el colapso diagnóstico en casos sintéticos diferenciados
y la falta de exclusión de wrong-role/missing-refs en focused. No ejecutar casos
C01/C02/C03. Tests válidos, límites, unknown/duplicate refs/keys, surrogates,
one-call y nonfocused protegerán aceptación y no leakage. Comparar casos válidos
con el baseline; no convertir los probes en una atribución histórica.

## Malāk Alignment Matrix

| source / clase | invariante e intención | evidencia baseline | disposición / efecto | rechazado/diferido y razón | trazabilidad |
|---|---|---|---|---|---|
| Cognitive Constitution / normativa | CC-002/003/011/012, no inventar ni finalizar generación | C02 sin subcausa; parser final | ADOPT: INCONCLUSIVE histórico y enforcement final | REJECT atribución especulativa | informe #334 y parser |
| Governance Constitution / normativa | Human in Control y mínimos privilegios | E2 read-only | ADOPT: mismo authority_effect none y gate GREEN separado | REJECT Ready/Merge/modelos automáticos | GOV-001/004; §5.5 |
| Blueprint y Kernel / normativos | Capability First, Runtime Independence | lógica E2 en capability | ADAPT: solución local sin acoplar a Ollama | REJECT Kernel/Planner/runtime delta | P-004/011 |
| SECURITY / protegida | Zero Trust, disclosure mínimo | error safe sin raw | ADAPT: taxonomy local cerrada | REJECT raw logs/persistencia | SECURITY §§3,6,12 |
| ADR-003 / aceptado | información upstream no es autoridad | errores retornan al executor | ADOPT: diagnóstico informativo | REJECT policy mutation | ADR-003 §§1–4 |
| Quality Gates / normativa | simplicidad, testabilidad, trazabilidad | parser/schema existentes | ADAPT sin subsistema | REJECT manager/store | gates 4–9 |
| Engineering Method y Construction / operativa | gates, 4R, RDD, independencia | PR lineage verificable | ADOPT: commits/gates exactos | REJECT autovalidación independiente | protocolo §5.5 |
| Roadmap CURRENT / derivada | cierre #330 y nuevo freeze | main@23de7f1 | ADAPT: nueva unidad acotada | DEFER reconciliación post-merge | sección CURRENT E2/E3 |
| ideas IDEA-002 / conceptual | observar, validar, proponer | incidente preservado | ADAPT observabilidad existente | DEFER self-improvement/training | ampliación Governed Evolution |
| horizon/concepts / conceptuales | observación determinista y no sobreingeniería | helpers y metadata existentes | ADOPT reuso; OBSERVE agentes/dataset | DEFER nuevos sistemas | horizon §4.2, swarm §4 |

## Cuatro preguntas de ley — productor

Blueprint PASS: E2 conserva responsabilidad, runtime genérico y cero bypass.
Cognitive Constitution PASS: salida rechazada sigue candidata; causa desconocida
no se inventa. Governance Constitution PASS: no autoridad ni side effects nuevos.
Kernel complexity PASS: delta cero. No se modifican documentos normativos.

## Design FULL 4R — productor

| lente | resultado | preguntas / evidencia | riesgo residual |
|---|---|---|---|
| Risk | PASS | ¿filtra raw o concede autoridad? enums locales, no cause/context, tests adversariales previstos | error no reconocido se clasifica UNCLASSIFIED |
| Readability | PASS | ¿duplica validación o crea sistema? reuse de helpers, clasificación local y builder existente | taxonomy requiere mantener tabla junto al parser |
| Reliability | PASS | ¿mismo acceptance y roles representados? parser intacto semánticamente, ramas schema y casos válidos/negativos | decoder real no medido; no se promete generation compliance |
| Resilience | PASS | ¿Unicode/malformed/overflow causan fuga o retry? diagnóstico bounded, hash sólo si codificable y single-attempt | raw inválido no posee digest UTF-8; se informa null |

No sustituye Candidate FULL 4R ni validación independiente. Blocking findings de
diseño del productor: ninguno en el alcance definido; residuales explícitos arriba.

## RDD Stage 1 Design Check — productor

PASS: baseline exacto; candidates commit/tree; evidencia externa al candidate
material; Writer distinto de reviewer/validator externo y Owner; enums terminales
PASS/FAIL/INCONCLUSIVE; invalidación por nuevo candidate; manifest v1 y Stage 2
requeridos por riesgo 3. Validación independiente real pendiente, no simulada.
Correction Budget: una ronda, sólo los archivos congelados; finding que exija
helpers/runtime/leyes o nueva arquitectura produce STOP/ESCALATE.
No se emite Candidate Conformance antes de FULL 4R/E2E/CI/independent validation.

## Gates y rollback

G0/G1 y pre-RED en este documento; RED = nuevo test sobre baseline sin producción;
Owner GREEN = decisión posterior al RED exacto; GREEN = delta mínimo aprobado;
targeted → FULL 4R → bounded correction/fix validation si aplica → E2E → CI →
independent validation → RDD Candidate Conformance/receipt → revisión humana.
Cada checkpoint tiene SHA/tree y resultado; no se reutiliza evidencia afectada.
Rollback por nuevo commit sobre archivos del scope; no se descarta historia.

```text
C01_ATTEMPT=CONSUMED; C01_RETRY=FORBIDDEN
C02_ATTEMPT=CONSUMED; C02_RETRY=FORBIDDEN
C03_ATTEMPT=NOT_STARTED; C03=HOLD
E3_C02=NOT_ATTEMPTED; E4=NOT_AUTHORIZED
MODEL_CALLS=0; API_CHAT_CALLS=0
CURRENT_PREMODEL_FREEZE_REUSE=FORBIDDEN_AFTER_EXECUTABLE_CHANGE
CURRENT_OWNER_G2_REUSE=FORBIDDEN_AFTER_EXECUTABLE_CHANGE
DESIGN_RESULT=PASS_PRODUCER
INDEPENDENT_VALIDATION=PENDING
GREEN_AUTHORIZED=NO
authority_effect=none
```

Soporte externo informativo: documentación oficial JSON Schema sobre annotations;
Ollama structured outputs y release v0.34.4 (actualiza sus backends; no garantiza
un subset exacto). No son autoridad del proceso ni prueba del runtime del Owner.
