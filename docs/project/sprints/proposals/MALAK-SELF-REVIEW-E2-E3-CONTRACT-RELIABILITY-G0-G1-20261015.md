---
title: "Malāk — E2/E3 Contract Reliability: diagnóstico y diseño candidato"
status: proposed_for_owner_review
authority: non_normative_proposal
language: es
date: 2026-10-15
repository: Aranwill/jarvis
baseline_commit: 5612214fd820adffc8627ed6f7b51a0416729d43
baseline_tree: 2b039add0420032a563aa588a66fc0dea2a95821
issues: [319, 327]
critical_contract: true
implementation_status: NOT_IMPLEMENTED
authority_effect: none
---

# E2/E3 Contract Reliability — diagnóstico y diseño candidato

## Resultado y frontera de esta entrega

Esta entrega documenta un diagnóstico parcial, una solución candidata concreta y
un plan de verificación. No contiene implementación ni afirma una mejora medida.
La solicitud del Owner autoriza ingeniería de punta a punta, pero conserva los
gates vigentes y prohíbe merge. El Construction Protocol §5.1.1 exige para esta
unidad material con diseño formal: PR-A documental, revisión y Ready/Merge humanos,
main reconciliado con el diseño aprobado, y luego PR-B de implementación.
§5.5 exige además RED antes de la autorización humana aplicable para GREEN.
No se interpreta la autorización inicial como sustituto de estas decisiones
candidate-bound. No se modifica el protocolo para eludir esta frontera.

La PR-A permanece Draft. Su promoción e integración corresponden al Owner.
No se ha iniciado RED/GREEN ni una serie experimental con modelos.

## Identidad, fuentes y admisión documental

Baseline remoto verificado: `5612214fd820adffc8627ed6f7b51a0416729d43`.
Tree recursivo: `2b039add0420032a563aa588a66fc0dea2a95821`, no truncado,
394 blobs del baseline descubiertos y clasificados en el ledger adjunto;
el ledger incluye además los dos documentos nuevos de esta PR-A (396 filas); inventario no significa
lectura completa del repositorio. La revisión es incremental del dominio E2/E3,
no una auditoría integral de Malāk.

Se verificaron #319 y sus dos comentarios, #327 y sus tres comentarios, ramas
remotas y PRs abiertas. Sólo #324 estaba abierta: research-only, excluida.
No existía una rama activa dedicada a esta corrección. Las dos ramas HVC no
se reutilizan. El baseline sigue coincidiendo con el indicado por el encargo.

La clonación Git por HTTPS no estuvo disponible: falló solicitando credenciales.
Se recuperaron fuentes mediante el conector autorizado y se reconstruyeron 191
blobs locales con identidad Git SHA-1 verificada contra el tree remoto. No se
presenta este conjunto como checkout completo ni como worktree Git limpio.
Las escrituras de esta propuesta utilizan la rama remota dedicada.

Construction Preflight 0.1.0, unidad documental de diagnóstico/diseño:

| Campo | Disposición |
|---|---|
| P0 | PASS: repositorio, baseline y encargo exactos identificados |
| P1 | PASS para análisis documental acotado; fuentes y profundidades en ledger |
| P2 | PASS: propuesta sin ejecución productiva, sin bypass ni delta Kernel |
| P3 | PASS: findings ascendentes con authority_effect=none; sin control ascendente |
| P4 | ADAPT / COMPOSE; sin nuevo subsistema |
| P5 | Diseño documental risk 2; implementación propuesta risk 3; critical_contract=YES |
| P6 | FROZEN para los dos documentos de esta PR-A; implementación futura separada |
| P7 | PASS sólo para preparar esta propuesta documental |

Este preflight no admite RED, GREEN, modelo, Ready, Merge ni conformance de una
implementación inexistente. El diseño no adquiere autoridad por publicarse.

## Diagnóstico: observaciones verificadas y límites

Los errores C01/E3 y C02/E2 provienen del encargo entregado por el Owner.
No se recibieron en esta tarea los outputs crudos, trazas completas, capturas
de requests efectivas ni digest del modelo de esos intentos. Los comentarios
de #327 confirman admisiones y preservación de C01, pero no contienen ambos
outputs originales. No se atribuye causalidad exclusiva al modelo o al harness.

| Plano | C01/E3 | C02/E2 |
|---|---|---|
| model behavior | El incidente informado asignó una ref a soporte y a limitación | El incidente informado emitió S1–S6 sin evidencia estructural |
| contract/interface | Las tres listas de roles se generan independientemente. El schema limita pertenencia y unicidad dentro de cada lista, pero no expresa disjunción entre listas | El prompt fijo menciona R#, K# y S#; en foco, structural_evidence se fuerza a lista vacía. La salida E2 es prosa sin response_json_schema |
| parser/governance | parse_engineering_finding rechaza explícitamente la intersección. Es el comportamiento correcto | _validate_model_evidence_refs rechaza refs desconocidas. Es el comportamiento correcto |
| execution harness | El código entrega un schema y usa una llamada stateless; falta el request original para confirmar el payload del incidente | El código usa una llamada con history=(); falta el request original para confirmar el contexto efectivo del incidente |

Fuentes técnicas, todas en el baseline exacto:

- `src/malak/capabilities/engineering_inspect.py`: `_SYSTEM_PROMPT`, `execute`,
  `_validate_model_evidence_refs`; foco sin S#, generación libre y rechazo posterior.
- `src/malak/capabilities/engineering_analyze.py`:
  `_build_relation_response_json_schema`; enums por fuente, uniqueItems por lista.
- `src/malak/capabilities/_engineering_analysis.py`: `ANALYZE_SYSTEM_PROMPT`,
  `run_engineering_analysis`, `parse_engineering_finding`; checks de refs,
  disjunción, incertidumbre, soporte requerido y límites.
- `src/malak/runtime/ollama_runtime.py`: schema transportado en `format`.
- `src/malak/services/conversation_service.py`: despacho sin responsabilidad de retries.

La causa compartida soportada por código es una interfaz que delega al generador
obligaciones estructurales evitables y las comprueba después. Los mecanismos
concretos difieren: namespace no disponible sugerido por E2 frente a asignación
multilista en E3. No existe evidencia suficiente para concluir que qwen3.5:9b
sea incapaz, que un modelo mayor baste, o que todos los fallos tengan una sola causa.
Exceso de responsabilidades y presión del presupuesto de salida son hipótesis
secundarias; no se presentan como hechos medidos.

## Solución candidata mínima

ADAPT de las capabilities existentes y COMPOSE con sus parsers actuales:
una representación intermedia acotada, específica de cada etapa, y proyección
determinista local. No nuevo manager, service, registry, orquestador o modelo.
Una inferencia por etapa; cero reparaciones o reintentos automáticos.

### E2: assertions con refs tipadas

Cambiar la salida del modelo de prosa con citas embebidas a un objeto estricto:
`schema_id`, `summary`, `assertions`, `uncertainties`. Cada assertion contiene exactamente
`kind`, `text`, `evidence_refs`; kind pertenece a OBSERVED, KNOWLEDGE_CONTEXT,
INTERPRETATION o UNCERTAINTY. El schema se deriva sólo del evidence bundle
admitido. Las refs son enums de identificadores exactos disponibles; si no hay
refs, la lista sólo admite vacío. No usar un enum vacío incompatible con el runtime.

Los textos no pueden introducir citas reservadas fuera de evidence_refs.
El parser rechaza refs desconocidas, keys extra/duplicadas, tipos inválidos,
JSON no finito, límites excedidos y namespaces fuera del bundle. El renderer
inserta citas desde los campos validados y conserva la comprobación final actual.
El prompt declara el catálogo real: una ausencia de S# nunca sugiere S# como cita.
La asignación kind debe seguir siendo interpretación del modelo; no prueba verdad.

### E3 focalizado: una asignación por ref

Por finding conservar classification, statement, rationale, uncertainty_basis
y relation_id. Sustituir únicamente la forma model-visible de las tres listas
por `evidence_roles`: mapa disperso con propiedades permitidas exclusivamente
para las refs disponibles, cada valor SUPPORT o LIMIT. additionalProperties=false
y maxProperties=16; el parser impone también ese límite. Las claves son opcionales: una
ref omitida significa no citada, nunca soporte implícito. No se agrega UNUSED al wire.
Las refs se originan en el catálogo inmutable del bundle; no en texto del modelo.
Los objetos con keys duplicadas se rechazan antes de construir un dict.

El esquema no concede soporte por omisión. Un mapa vacío sólo puede pasar si
el contrato canónico de la clasificación y la incertidumbre ya lo permite. Una
ref no puede ocupar dos roles; una key JSON duplicada siempre se rechaza.
La proyección hace exclusivamente:

1. SUPPORT + fuente repository → supporting_repository_refs.
2. SUPPORT + fuente knowledge → supporting_knowledge_refs.
3. LIMIT → limiting_or_counterevidence_refs.
4. Ref no seleccionada → no se incluye en las listas finales; el bundle original no se altera.

La fuente se obtiene del bundle validado, nunca se infiere de texto libre ni se
elige por conveniencia. Después se ejecuta el parser vigente completo sobre el
objeto proyectado. No cambia clasificación, rationale, incertidumbre ni relación.
No elimina conflictos del formato antiguo, no completa refs inventadas y no
convierte errores en UNRESOLVED o PASS. El formato nuevo se versiona explícitamente
en la implementación; no se auto-detecta ni repara un formato antiguo inválido.

La función de proyección es pura, interna a la capability; no adquiere autoridad.
La ruta no focalizada mantiene su contrato existente, salvo necesidad demostrada
y nueva disposición explícita. Los consumidores E4 siguen recibiendo los campos
canónicos actuales. La compatibilidad E3/E4 se debe verificar sin ejecutar E4
del piloto original.

### Formatos y presupuestos congelados de la propuesta V1

Envelope model-visible E2: exactamente `schema_id`, `summary`, `assertions`,
`uncertainties`, con schema_id constante `malak.e2.assertions.v1`.
Envelope E3 focalizado: exactamente `schema_id`, `summary`, `findings`,
`uncertainties`, con schema_id constante `malak.e3.ref-role-map.v1`.
El adapter consume schema_id validado y entrega al parser canónico únicamente
sus campos históricos. La versión se selecciona por código/configuración de
la ruta admitida, nunca mediante autodetección de un output malformado.

- Prompt: conservar 65.536 bytes UTF-8 del baseline.
- Schema serializado: máximo 65.536 bytes UTF-8, reutilizando el mismo presupuesto
  numérico; límite adicional explícito, no evidencia de cabida en tokens.
- Output: conservar 65.536 bytes UTF-8. No completar JSON cortado.
- E3: máximo 16 findings y 16 refs seleccionadas por finding, ya vigentes.
- E2: máximo 16 assertions, 16 refs por assertion, summary de 8.192 bytes,
  texto por assertion de 4.096 bytes, 16 uncertainties de 4.096 bytes cada una.
  Son presupuestos candidatos reutilizados de E3 para acotar E2; no son límites
  históricos de E2. El límite global de salida prevalece sobre su suma.
- Limitar siempre por bytes en parser. maxLength del schema, cuando se use,
  cuenta caracteres y no sustituye esa validación UTF-8.
- Enums de refs vacíos: lista sólo vacía en E2; mapa sin propiedades en E3.
  No emitir un `enum: []`. Nunca generar refs de relleno.
- Claves/ref order: orden del bundle validado, repository y después knowledge;
  la proyección usa ese mismo orden. JSON canónico sort_keys=True,
  ensure_ascii=False y separators compactos para hashes y tamaño.
- Prompt se limita antes de construir schema; schema se mide antes de invocar
  generate. Overflow → error técnico pre-model, cero llamadas; sin truncación,
  partición, reducción del bundle ni fallback automático.

La asignación total obligatoria de la primera propuesta se descarta: hacía
crecer el output con todo el catálogo aunque el contrato final admite sólo 16
refs seleccionadas. El mapa disperso conserva la exclusividad sin ese coste.
No se exige al modelo emitir valores UNUSED para cada evidencia no utilizada.

E2 OBSERVED exige refs repository; KNOWLEDGE_CONTEXT exige refs knowledge;
INTERPRETATION exige refs del bundle; UNCERTAINTY permite refs vacías. Esto no
valida entailment. Strings y campos extra/duplicados se validan estrictamente;
no se permiten citas reservadas R#/K#/S#/A# embebidas fuera de campos de refs.

Prueba de diseño local, sin modelo ni cambios productivos: 729 asignaciones
posibles de seis refs entre no seleccionada/SUPPORT/LIMIT; todas preservan
la disjunción y el conjunto seleccionado. No se afirma que todas pasen los
checks semánticos/estructurales finales. Sizing de un ejemplo de schema E3
con una relación: 6 refs=1.107 bytes; 16=1.447; 128=5.365; 512=19.119;
1.024=37.551. Es un ejemplo medido, no el máximo universal del serializer futuro.
El guard exacto de 65.536 bytes se comprueba sobre cada request real.

La cabida en bytes no garantiza cabida en context_window_tokens ni soporte
perfecto del constrained decoder. El runtime actual valida los conteos
reportados de tokens, pero eso no demuestra por sí solo ausencia de truncación.
Antes de una nueva serie real se debe congelar/capturar el contexto efectivo,
configuración y provenance con los controles pre-model admitidos. Si esa
precondición es INCONCLUSIVE, no se ejecuta el experimento. No se propone
cambiar ni el runtime ni el freeze original en esta PR-A.

## Por qué proyección no equivale a reparación

La proyección sólo transforma una representación válida y no ambigua en otra
representación equivalente. Un intermediate inválido falla sin proyectarse.
La disjunción resulta de la representación, pero la corrección semántica de
SUPPORT/LIMIT sigue siendo probabilística. Validación estructural no demuestra
entailment. Se conserva tanto la incertidumbre como la posibilidad de rechazo.

## Alternativas evaluadas

| Alternativa | Disposición y razón |
|---|---|
| No cambiar | Conserva seguridad pero conserva fragilidad; control comparativo necesario |
| Sólo añadir instrucciones | Menor delta; no elimina asignaciones multilista contradictorias |
| Relajar parser o deduplicar overlap | REJECT: cambia el significado y esconde errores |
| Refs libres y normalización aproximada | REJECT: fabricaría binding o corregiría evidencia por heurística |
| Modelo mayor como única corrección | OBSERVE: requiere benchmark; no resuelve por diseño la fragilidad |
| Segunda llamada de repair/reviewer | DEFER: mayor coste y otra responsabilidad probabilística; déficit no probado |
| Un llamado por cada ref | DEFER: aumenta llamadas, latencia y composición sin evidencia de necesidad |
| Condicionales cruzados en JSON Schema | DEFER: más complejidad y soporte dependiente del runtime; parser sigue necesario |
| Un rol único por ref + parser final | ADAPT/COMPOSE candidato: elimina duplicación representacional sin decidir semántica |

## Malāk Alignment Matrix y reutilización

| Fuente / autoridad | Invariante o intención | Disposición / efecto |
|---|---|---|
| Cognitive Constitution / normativa | CC-002/003/004: evidencia e incertidumbre; CC-005/006: minimización; CC-011/012: Generation != Finalization | ADOPT; modelo propone, parser rechaza; no certeza inventada |
| Governance Constitution / normativa | GOV-001/004/005/006 | ADOPT; sin nuevos permisos, side effects ni autoridad |
| Blueprint / normativo | Kernel First, Capability First, Runtime Independence, Specification & Verification First | ADAPT dentro de capabilities existentes; Kernel sin delta |
| ADR-003 / aceptado | Resultados ascendentes authority_effect=none | ADOPT; sin órdenes ascendentes ni bypass |
| ADR-004 / aceptado | Especificar y verificar antes de aceptación | ADOPT; PR-A antes de PR-B |
| SECURITY.md / política protegida | Zero Trust, Least Context, fail-closed, datos != instrucciones | ADOPT; schema no sustituye enforcement |
| Architecture Quality Gates / normativa | Dependencias, contratos y separación | ADOPT; sin nuevo subsistema o ciclos |
| Roadmap vigente / derivado | E2/E3/E4 y foco ya integrados | REUSE; snapshots históricos no se convierten en autoridad corriente |
| ideas.md / conceptual | IDEA-002: mejorar observaciones sin autoaprobarse | ADAPT; propuesta con evidencia, sin aprendizaje persistente |
| Research Horizon / conceptual | Reforzar existente; autonomous self-modification incompatible | ADAPT interfaz; REJECT automodificación |
| Evidence-Bound Cognition / conceptual | Model alignment != enforcement | ADOPT principio; sin promover CAL ni ley nueva |
| Cognitive Dataset / conceptual | Evaluación separada antes de training | ADOPT separación; training DEFERRED |
| Bootstrap Task / conceptual | findings y NO_CHANGE válidos; propuesta != autorización | ADOPT; sin obligación de PASS |
| Swarm / Ephemeral Execution / conceptuales | Complejidad y contexto acotados | OBSERVE; agentes y sandboxes no necesarios |
| Código y tests E2/E3 / implementación | Focus, schemas, guards y renderer existentes | REUSE / ADAPT / COMPOSE; no nuevo framework |

## Riesgo, cuatro preguntas y 4R

critical_contract=YES por Construction Protocol §5.2, criterio 2: produce o
interpreta evidence/evaluation usada por gates. No se amplía esa definición.
La implementación propuesta es risk 3 por el cambio en interpretación de refs.
El candidate documental es risk 2 y no activa una superficie productiva.

Cuatro preguntas: Blueprint compatible al permanecer en capabilities;
CC compatible al preservar incertidumbre y rechazo; Gobernanza compatible al
mantener authority_effect=none; Kernel simple con delta cero. Estas respuestas
evalúan la propuesta, no certifican una implementación inexistente.

| Lente Design 4R | Evidencia / disposición |
|---|---|
| Risk | PASS del productor: budgets explícitos y parser final obligatorio; decoder no confiable y freeze real siguen siendo riesgos controlados |
| Readability | Una asignación explícita por ref; nombres canónicos finales conservados. PASS como revisión del productor, no independiente |
| Reliability | PASS del productor para diseño: disjunción por representación y rechazo sin repair. Mejora real NOT_MEASURED; requiere PR-B y serie nueva |
| Resilience | PASS del productor para diseño: overflow/malformed/duplicate definidos como rechazo. Pruebas de implementación pendientes en PR-B |

Design 4R del productor: PASS documental; no es validación independiente ni FULL 4R de implementación. G1, Critical Contract Hardening y RDD
Stage 1 Design Check requieren revisión del candidate documental actualizado. Candidate FULL 4R, RED, GREEN,
E2E del cambio, CI de implementación, validación independiente, RDD Candidate
Conformance y Receipt risk 3 no se han ejecutado. Ninguna etapa se sustituye
por tests verdes del baseline. La PR permite revisar el diagnóstico y el diseño concreto; no certifica una implementación.

## Implementación futura: scope y gates

PR-B desde main reconciliado con diseño admitido. Archivos candidatos:
`engineering_inspect.py`, `engineering_analyze.py`, `_engineering_analysis.py`,
tests E2/E3/focus/role-binding y tooling experimental mínimo sólo si se justifica.
No autoriza cambios en Kernel, ley, security foundations o readers/binding.
Un archivo adicional requiere registrar necesidad y revalidar scope.

1. G1 hardening: revisar los formatos y budgets V1 congelados y completar
   RDD Design Check sobre el candidate documental exacto.
2. Tras revisión/promoción humana del diseño y main reconciliado: RED con
   negativos y criterios del intermediate, SHA exacto y evidencia conservada.
3. Tras autorización humana aplicable sobre RED: GREEN mínimo, proyección y
   parsers; sin refactor lateral. Targeted tests y FULL 4R candidate-bound.
4. Bounded Correction/Fix Validator cuando haya findings; revalidación afectada.
5. E2E, CI, validación independiente, RDD Stage 1 Candidate Conformance y
   Stage 2 Receipt risk 3. Ready y Merge humanos separados.

STOP ante cambio de baseline, evidencia incompleta, mezcla con HVC, violación
de blindness, presupuesto sin cerrar, regresión o gate FAIL/INCONCLUSIVE.
Rollback: abandonar cambios de PR-A no integrada; una futura PR-B usa revert
acotado al candidate, nunca reset destructivo ni borrado de evidencia histórica.

## Verificación requerida y experimento nuevo

Tests futuros, antes de declarar mejora:

- refs desconocidas y de otra fuente rechazadas en ambas representaciones;
- overlap del contrato canónico sigue rechazado; keys duplicadas del intermediate rechazadas;
- malformed JSON, no finitos, keys extra/ausentes, tipos y límites incorrectos fallan;
- permutaciones de refs y roles proyectan determinísticamente, sin perder binding;
- SUPPORT/LIMIT y omisión no transforman clasificación ni incertidumbre;
- duplicación/omisión de relation_id y soporte insuficiente siguen rechazados;
- history vacío, una llamada por etapa, sin retrieval/tools adicionales;
- prompts/contexto reconstruidos sólo con allowlist; oracle/rubric fuera del request;
- authority_effect=none y compatibilidad con consumidores finales;
- presupuesto máximo sin truncación y sin fallback;
- evidencia C01/C02 no tocada y C03 original no invocado.

Serie candidata `E2E3-CR-v1`, separada del piloto: casos de desarrollo nuevos,
sin reutilizar C01/C02/C03 ni oracle original. Antes de ejecutar, congelar
materiales, configuraciones, modelo/tag/digest, runtime, prompts, schema y
candidate. Comparación before/after sobre los mismos materiales nuevos y la
misma política: un intento por caso y etapa y versión, cero hidden retries;
registrar todas las llamadas, timeouts, rejects y latencias.

Propuesta de tamaño: 20 tareas nuevas, 2 etapas, 2 versiones = máximo 80
llamadas. Se debe admitir el presupuesto concreto antes de ejecución. No se
usa el output de E2 para ampliar el contexto E3. Scoring de estructura separado
del scoring de utilidad/evidencia/incertidumbre; expected labels no son input.
Criterio candidato de mejora material: al menos 50% de reducción relativa de
contract rejections frente al baseline en esa serie, sin incremento de aceptación
de negativos inválidos ni regresión semántica material. Si el baseline no falla,
el resultado de mejora será INCONCLUSIVE, no PASS. Reportar conteos, denominador
y limitación muestral; no extrapolar una garantía universal.

Los tests de proyección pueden demostrar eliminación representacional del overlap;
no demuestran reducción empírica de fallos de generación ni capacidad cognitiva.

## Evidencia ejecutada en esta entrega

Python 3.12.14; venv local; pytest 9.1.1 de la dependencia dev declarada
`pytest>=9,<10`. No cambios en dependencias del repositorio.

Primer intento de pytest: error ambiental `No module named pytest`; se instaló
la dependencia dev ya declarada y se repitió. No se ocultó como fallo de producto.

Focalizados: `test_engineering_inspect.py`, `test_engineering_analyze.py`,
`test_governed_engineering_evidence_focus_v0.py`: **192 passed, 5.33 s**.

Ampliados: `test_engineering_propose.py`,
`test_e3_structured_evidence_role_binding_v0.py`,
`test_e3_governed_support_evidence_routing_v0.py`,
`test_e3_governed_evidence_support_assessment_v0.py`, `test_ollama_runtime.py`,
`test_runtime_generation_contract_red.py`, `test_internal_interaction_v0.py`:
**231 passed, 3.84 s**.

Total: **423 passed** del baseline. Tests con providers/runtime de prueba, sin
model calls reales ni `/api/chat`. Suite completa no ejecutada: el conjunto
local es una recuperación parcial de fuentes; no se pretende certificar el repo
completo ni el cambio futuro. No hubo pruebas de una solución implementada.

## Before/after y piloto histórico

BEFORE informado por Owner: C01/E3 OUTPUT_CONTRACT_REJECTED por overlap;
C02/E2 OUTPUT_CONTRACT_REJECTED por S1–S6 desconocidas. C01 y C02 consumidos.
C03 NOT_RUN según encargo. Nada se reejecutó ni sobrescribió.

AFTER: NOT_IMPLEMENTED / NOT_MEASURED. No serie nueva ejecutada. No se reutiliza
el PASS de los guards para afirmar que el modelo ahora cumpla contratos.

qwen3.5:9b suitability=INCONCLUSIVE. No digest/provenance local de esta entrega
ni comparación empírica nueva. Un gate futuro podrá evaluar capacidad con la
misma tarea y condiciones; no seleccionar por tamaño o reputación.

C03 se preserva para posible holdout/validación posterior independiente.
Su uso necesita una autorización nueva, explícita y posterior a esta tarea.
El reviewer de implementación no puede presentarse como blind oracle annotator:
esta revisión accede a materiales de proyecto e hipótesis de evaluación.

## COMPLEXITY_DELTA

Actual en esta PR-A: 0 clases, 0 módulos, 0 contratos runtime, 0 capas runtime,
0 persistencia/estado productivo, 0 dependencias; dos documentos nuevos.

Propuesto para PR-B: 0 clases y 0 módulos nuevos; dos formas model-visible
intermedias versionadas dentro de capabilities existentes; una operación pura
de proyección E3 y un renderer E2 adaptado. Sin nueva capa desplegable,
persistencia, servicio, dependencia ni llamada adicional. La necesidad se
justifica por la falta de una representación exclusiva de roles y por las citas
libres de E2. El coste exacto se debe medir contra el diff de implementación.

## Disposición terminal

```yaml
ROOT_CAUSE: PARTIAL
SOLUTION_IMPLEMENTED: NO
GOVERNANCE_RELAXED: NO
HIDDEN_RETRIES_INTRODUCED: NO
BLINDNESS_REGRESSION: INCONCLUSIVE
CONTRACT_RELIABILITY_IMPROVED: INCONCLUSIVE
QWEN_3_5_9B_SUITABILITY: INCONCLUSIVE
TESTS: PARTIAL
C03_ORIGINAL_PILOT_CONSUMED: NO
READY_FOR_INDEPENDENT_VALIDATION: NO
READY_FOR_OWNER_REVIEW: YES
OWNER_REVIEW_SCOPE: diagnostic_and_design_proposal_only
MERGE_AUTHORIZED: NO
authority_effect: none
```

BLINDNESS_REGRESSION es INCONCLUSIVE porque no se ha construido ni capturado
el contexto de una implementación nueva; no se ejecutó ningún caso del piloto.
READY_FOR_OWNER_REVIEW describe esta propuesta incompleta, no aceptación técnica
del fix. Las decisiones pendientes son concretas: revisión de la forma intermedia/budgets
ya especificados, cierre de gates de diseño, revisión/promoción humana de PR-A y autorización
GREEN sobre el RED futuro. No se solicita relajar ninguna regla.


## Reanudación de PR-A — 2026-10-15

Construction Preflight revalidado para esta corrección documental: baseline,
AGENTS, protocolo, preflight y checklist mantienen sus blobs; scope continúa
limitado a los dos documentos de PR-A. El cambio adapta exclusivamente el diseño
admitido para revisión. La comparación con normativa/seguridad mantiene las
mismas disposiciones; no se activa ningún contrato productivo.

Estado observado antes de esta actualización: run 38823273781, Ubuntu success,
Windows in_progress en tests; candidate 4a8ba8f24cc6f9c614ffec1c9b581f4eb702f08f.
Esos resultados son históricos para ese SHA, no certifican el nuevo candidate.
No se rerunea un fallo ni se altera configuración de runners.

Revisión de diseño por lentes: Risk considera refs desconocidas, duplicadas,
namespace spoofing, prompt injection y autoridad; parser/freeze siguen siendo
fronteras. Readability considera versión, claves exactas, tipos y proyección;
se elimina el ambiguo coste de emitir UNUSED para todo el catálogo. Reliability
considera preservación de refs/roles, incertidumbre, límites y orden; enumeración
729/729 sólo demuestra el invariante matemático, no cognición. Resilience
considera overflow, output cortado, falta de provenance y decoder incompatible;
todos fallan sin retry/fallback y sin cambiar el piloto. El riesgo residual común
es utilidad cognitiva desconocida y posibles contract rejections restantes.
Las cuatro lentes concluyen PASS como evaluación documental del productor.

RDD Stage 1 Design Check del productor: PASS para la especificación. Baseline
exacto registrado; candidate se identifica por SHA Git de esta PR y blobs de los
dos documentos, sin autorreferencia imposible dentro del propio commit. Un
cambio invalida la evidencia afectada. Writer es el productor de esta PR;
reviewer/validator independientes no se simulan; Owner conserva decisiones.
Resultados terminales RDD PASS/FAIL/INCONCLUSIVE; correcciones futuras conservan
findings y requieren budget y Fix Validator cuando corresponda. Para PR-B risk 3,
Stage 1 Manifest y Stage 2 Receipt serán obligatorios según protocolo; para esta
propuesta documental risk 2 Stage 2 no se admite por inferencia y queda N/A.
Esto no es Candidate Conformance ni aceptación del fix.

La causa raíz sigue PARTIAL y la solución NOT_IMPLEMENTED. El diseño queda
preparado para revisión independiente pre-RED. El técnico que prepare PR-B debe
verificar primero promoción humana de este diseño y main reconciliado; no se
salta esa condición porque los runners del baseline terminen en verde.
