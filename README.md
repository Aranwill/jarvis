# Malāk

Malāk es una plataforma cognitiva personal ejecutada localmente, diseñada para ser modular, gobernable, extensible y agnóstica respecto del modelo de inteligencia artificial utilizado.

## Estado actual

Versión actual:

```text
v0.6.0-alpha
```

Estado de desarrollo:

```text
Foundation Implementation
```

Rama permanente:

`main`

Último sprint numerado completado e integrado:

```text
Sprint 7.11 — Reproducible Validation Pipeline Foundation
```

Última ruta conversacional numerada integrada:

```text
Sprint 7.10 — Conversation Session Isolation Foundation
```

Después de Sprint 7.11 se integraron unidades aisladas de Memory y Cognitive Assurance sin constituir Sprint 7.12. El baseline actual incluye `EpisodicCandidateContentIdentity` y su propagación/binding gobernado a través de la cadena episódica, además de G2A — Protected Finalization Foundation y G2 — Assurance Signal Authority & Projection Foundation en aislamiento.

CAL-014 — Protected Durable Reliance está activado normativamente mediante CC-013, R-023 y ADR-006. Esa activación, por sí sola, no autoriza Persistence Authorization, Persistent Memory, Conversation G2B ni Sprint 7.12. RDD Stage 2 fue adoptado posteriormente y de forma separada mediante PR #267.

La interfaz disponible actualmente es una CLI técnica que conserva la ruta conversacional y expone, además, superficies read-only de Engineering, Explorer, Trace y Governed Self-Review.

Estas superficies permiten inspeccionar el baseline, explorar Repository/Knowledge, ejecutar Engineering Inspect/Analyze/Propose bajo sus contracts y reproducir o inspeccionar trazas de Self-Review. No conceden autoridad de modificación, merge ni self-modification.

La CLI puede utilizar:

- `MockLLMRuntime`;
- `OllamaRuntime`.

La selección del runtime se realiza mediante configuración externa en la frontera de aplicación.

Las solicitudes conversacionales ordinarias ingresan actualmente mediante la frontera cognitiva `Kernel.receive()`.

La conversación se encuentra integrada detrás de la abstracción `Capability`, preservando la independencia del Kernel respecto de servicios, providers, runtimes y modelos concretos.

Sprint 7.9 añadió continuidad conversacional efímera en memoria y Sprint 7.10 añadió aislamiento explícito por `session_id`, sin introducir persistencia ni Memory cognitiva.

## Arquitectura actual de la CLI

```text
Variables de entorno
        ↓
CLIConfiguration
        ↓
Application Composition
        ↓
Kernel.receive()
        ↓
Planner
        ↓
CapabilityRegistry
        ↓
ConversationCapability
        ↓
ConversationService
        ↓
ConversationProviderRegistry
        ↓
RuntimeConversationProvider
        ↓
LLMRuntime
├── MockLLMRuntime
└── OllamaRuntime
        ↓
Response
```

La construcción de runtimes, providers y servicios permanece en la frontera de aplicación.

El Kernel continúa desacoplado de implementaciones concretas de runtime y modelo.

## Requisitos

- Python 3.12.x
- `pip`
- entorno virtual local
- Ollama, únicamente para ejecutar `OllamaRuntime`

Versión de Python validada:

```text
Python 3.12.10
```

## Preparación del entorno

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

La instalación editable permite utilizar el paquete `malak` desde el layout `src` sin configurar manualmente `PYTHONPATH`.

## Ejecución con MockLLMRuntime

`MockLLMRuntime` es el runtime predeterminado y no requiere servicios externos.

```powershell
python -m malak.app.cli
```

El comando:

```text
status
```

debe mostrar un estado equivalente a:

```text
Estado: operativo | Provider: mock | Runtime: MockLLMRuntime
```

## Ejecución con OllamaRuntime

### Requisitos previos

- Ollama instalado;
- servicio local de Ollama activo;
- al menos un modelo local disponible;
- entorno virtual de Malāk activado.

Verificar los modelos instalados:

```powershell
ollama list
```

Verificar el servicio HTTP local:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

### Configuración externa

Seleccionar Ollama como runtime:

```powershell
$env:MALAK_RUNTIME = "ollama"
```

Seleccionar el modelo:

```powershell
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
```

Configurar la URL base:

```powershell
$env:MALAK_OLLAMA_BASE_URL = "http://localhost:11434"
```

Iniciar la CLI:

```powershell
python -m malak.app.cli
```

El comando:

```text
status
```

debe mostrar un estado equivalente a:

```text
Estado: operativo | Provider: ollama | Runtime: OllamaRuntime
```

Las variables configuradas mediante `$env:` se aplican únicamente a la sesión actual de PowerShell.

## Variables admitidas

| Variable | Obligatoria | Uso / valor |
|---|---:|---|
| `MALAK_RUNTIME` | No | `mock` por defecto; `ollama` para runtime local |
| `MALAK_OLLAMA_MODEL` | Sí cuando el runtime es `ollama` | Modelo solicitado |
| `MALAK_OLLAMA_BASE_URL` | No | `http://localhost:11434` |
| `MALAK_REPOSITORY_ROOT` | Sí para Engineering / Explorer / Trace / Self-Review | Raíz del snapshot Git |
| `MALAK_OLLAMA_CONTEXT_WINDOW_TOKENS` | Sólo cuando se configura generation contract | Presupuesto de contexto |
| `MALAK_OLLAMA_MAX_OUTPUT_TOKENS` | Sólo cuando se configura generation contract | Presupuesto máximo de salida |
| `MALAK_OLLAMA_THINKING` | Sólo cuando se configura generation contract | `enabled` o `disabled` |

Valores admitidos para `MALAK_RUNTIME`:

```text
mock
ollama
```

Un runtime desconocido debe ser rechazado de forma controlada.

Las tres variables del `RuntimeGenerationContract` deben configurarse juntas. Una configuración parcial se rechaza. Cuando el contrato está presente, preserva explícitamente:

```text
context_window_tokens
max_output_tokens
thinking_enabled
truncate=false
shift=false
```

El contrato es request-scoped y no altera el comportamiento conversacional ordinario cuando no fue configurado. `/self-review test-v0` exige que este contrato esté configurado de forma completa.

## Comandos de la CLI

```text
help
ayuda
status
doctor
new

/engineering help
/engineering inspect <subject>
/engineering analyze <subject>
/engineering propose <subject>

/explore help
/explore repo list [prefix]
/explore repo read <path>
/explore repo search <text>
/explore knowledge list
/explore knowledge read <path>
/explore knowledge search <text>

/trace help
/trace replay <run_id>
/trace inspect <run_id> <node_id>
/trace summary <run_id>

/self-review help
/self-review test-v0 <run_id> <validation_ref> [<validation_ref> ...]

exit
quit
salir
```

El comando `status` también informa `Intercambios retenidos: N` para la sesión activa. El valor sólo cuenta intercambios completos que siguen en el contexto efímero (máximo seis por defecto); no muestra mensajes, no consulta otras sesiones ni persiste datos. Después de `new`, el recuento vuelve a cero.

El comando `doctor` muestra únicamente diagnóstico local read-only. `CLI: VERIFIED` indica que se ejecutó el comando; `Contexto: VERIFIED` sólo confirma una lectura del contador efímero de la sesión activa. `CONFIGURED` indica una composición seleccionada, no un componente saludable. El comando comprueba adicionalmente si el provider seleccionado está presente en el registro local de `ConversationService`, informando `Provider: REGISTERED (registro local)` o `Provider: NOT_REGISTERED (registro local)` sin ejecutar al provider ni divulgar su nombre. Esta comprobación no acredita salud, disponibilidad ni autorización. El comando nunca consulta modelos o endpoints, no prueba PDP/PEP y siempre termina con `Salud global: NOT_CERTIFIED`; no modifica el historial ni autoriza operaciones.

La CLI también controla:

- entradas vacías;
- continuidad conversacional efímera durante la ejecución;
- reinicio del contexto activo mediante `new`, con rotación de sesión;
- interrupciones mediante `Ctrl + C`;
- finalización mediante EOF;
- errores del runtime presentados como errores controlados.

`/trace summary <run_id>` muestra un resumen read-only de la traza observada (`trace.jsonl`): estado y duración registrada por nodo, y códigos de causa disponibles, sin conferir autoridad (`authority_effect: none`).

Los comandos propios de la CLI permanecen en la frontera de aplicación y no se convierten artificialmente en capabilities.

## Validación automatizada

Ejecutar la suite completa:

```powershell
python -m pytest -q
```

La última implementación productiva integrada de esta línea fue E3 Epistemic Calibration (PR #209), validada candidate-bound con:

```text
candidate:
c7a3ec63d8280192bb17f4828759cdf0d8033242

Validation #634

Ubuntu:
1599 passed

Windows:
1599 passed

compileall:
PASS

candidate identity:
PASS

candidate diff:
PASS

Kernel delta:
0

Planner delta:
0

authority_effect:
none
```

El baseline material/productivo reconciliado por esta documentación corresponde a `main@7b1fe7621b1dad48cc8508390e2ad78faa3e3004`.

Validar compilación:

```powershell
python -m compileall src tests
```

Validar formato del diff:

```powershell
git diff --check
```

Las pruebas automatizadas no requieren obligatoriamente un servicio Ollama activo. Las llamadas HTTP utilizadas por `OllamaRuntime` se sustituyen o controlan en las pruebas deterministas.

## Validación manual con Ollama

Secuencia validada:

```powershell
ollama list
Invoke-RestMethod http://localhost:11434/api/tags

$env:MALAK_RUNTIME = "ollama"
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
$env:MALAK_OLLAMA_BASE_URL = "http://localhost:11434"

python -m malak.app.cli
```

Dentro de la CLI:

1. ejecutar `status`;
2. enviar un prompt breve y no sensible;
3. comprobar que se recibe una respuesta;
4. opcionalmente ejecutar `new` y comprobar que se inicia una nueva sesión conversacional;
5. finalizar mediante `exit`.

La integración real fue validada con:

```text
qwen3.5:9b
```

La ruta arquitectónica continúa utilizando `OllamaRuntime` sin introducir dependencias de Ollama dentro del Kernel.

## Alcance actual

La CLI permite:

- ingresar mensajes por terminal;
- generar la solicitud de entrada hacia el Kernel;
- enrutar solicitudes conversacionales ordinarias mediante `Kernel.receive()`;
- resolver la capability `conversation` mediante `Planner` y `CapabilityRegistry`;
- adaptar la solicitud mediante `ConversationCapability`;
- delegar la generación mediante `ConversationService`;
- resolver el provider mediante `ConversationProviderRegistry`;
- utilizar `MockLLMRuntime` u `OllamaRuntime`;
- mantener continuidad conversacional efímera;
- aislar el contexto conversacional por `session_id`;
- reiniciar el contexto mediante `new` sin persistencia;
- retornar la respuesta a través de la frontera cognitiva;
- gestionar comandos básicos y errores controlados;
- ejecutar `/engineering inspect|analyze|propose` sobre el baseline configurado;
- explorar Repository y Knowledge mediante `/explore` en modo read-only;
- reproducir e inspeccionar artefactos de trace mediante `/trace`;
- ejecutar el harness gobernado `/self-review test-v0` únicamente cuando se cumplen sus precondiciones de admisión.

Las superficies Engineering, Explorer, Trace y Self-Review no convierten evidencia, findings o propuestas en autoridad y no habilitan self-modification.

La ruta conversacional actual es:

```text
Request
  ↓
Kernel.receive()
  ↓
Planner
  ↓
CapabilityRegistry
  ↓
ConversationCapability
  ↓
ConversationService
  ↓
ConversationProviderRegistry
  ↓
RuntimeConversationProvider
  ↓
LLMRuntime
  ↓
Response
```

## Fuera de alcance actual

Todavía no forman parte de esta CLI:

- memoria conversacional persistente;
- historial persistente de conversaciones;
- agentes;
- herramientas externas;
- navegación;
- GraphRAG;
- interfaz gráfica;
- ejecución autónoma;
- aplicación automática de recomendaciones de rendimiento;
- modificación automática de timeout, modelo o permanencia en memoria.

## Documentación

Documentos relevantes:

```text
docs/architecture/blueprint.md
docs/architecture/kernel.md
docs/architecture/adr/ADR-006-protected-durable-reliance-preconditions.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/development/development_environment.md
docs/project/implementation_roadmap.md
docs/project/sprints/SPRINT-7.0.md
docs/project/sprints/SPRINT-7.1.md
docs/project/sprints/SPRINT-7.2.md
docs/project/sprints/SPRINT-7.3.md
docs/project/sprints/SPRINT-7.4.md
docs/project/sprints/SPRINT-7.5.md
docs/project/sprints/SPRINT-7.6.md
docs/project/sprints/SPRINT-7.7.md
docs/project/sprints/SPRINT-7.8.md
docs/project/sprints/SPRINT-7.9.md
docs/project/sprints/SPRINT-7.10.md
docs/project/sprints/SPRINT-7.11.md
```

## Principios

Malāk mantiene como principios centrales:

- Kernel First;
- Capability First;
- Runtime Independence;
- Human in Control;
- Zero Trust interno;
- configuración externa al Kernel;
- cambios pequeños, probados, trazables y reversibles;
- separación entre medición, recomendación y configuración efectiva.


## Reconciliación CURRENT — E3 Governed Evidence Support Assessment V0

Estado reconciliado al baseline `main@7b1fe7621b1dad48cc8508390e2ad78faa3e3004`:

- PR #224 integró `E3 Governed Evidence Support Assessment V0` sobre candidate `ad24d5b6de7a3c3e4dcb5643e5906df8bc8682f6`.
- El merge commit es `7b1fe7621b1dad48cc8508390e2ad78faa3e3004`.
- Validation #686 post-merge terminó PASS en Ubuntu y Windows, incluyendo candidate identity, suite de tests, `compileall` y candidate diff.
- El contrato bounded distingue `SUPPORTED | INSUFFICIENT | INCONCLUSIVE` sin convertir soporte en verdad, hecho verificado, decisión ni autoridad.
- `E008-SG-02` permanece `OPEN`: existe el contrato gobernado de assessment de soporte, pero `semantic_assurance` continúa `NOT_VERIFIED`.
- `support_sufficient` permanece sin wiring y no autorizado por esta unidad.
- `authority_effect = none`.
- RDD Stage 2 permanece `NOT AUTHORIZED`.
- Sprint 7.12 permanece `NOT AUTHORIZED`.

Esta reconciliación es derivada y no autoriza una nueva implementación.

## Reconciliación CURRENT — E3 Assessor Qualification Pack V0.1

Estado reconciliado al baseline integrado `main@ae22f3be23ff1c30093d071c74e86db84c34098e`:

- PR #231 integró la bounded contract correction V0.1 que materializa inputs/observations reproducibles para C05/C11/C12/C13.
- PR #230 integró `E3 Assessor Qualification Pack V0.1` sobre candidate `f65f591cd53c702949012836aace7a2cdd0013d0`.
- El merge commit `ae22f3be23ff1c30093d071c74e86db84c34098e` conserva exactamente el tree `18a0eead6b98ec85c17f7450c4bcfc687bedb3e8` del candidate validado.
- Validation #713 candidate-bound terminó PASS con `1730 passed` en Ubuntu y Windows, además de `compileall` y candidate diff.
- Validation #714 post-merge terminó PASS con `1730 passed` en Ubuntu y Windows sobre el merge exacto.
- El pack offline contiene 18 casos / 19 inputs, runner determinista de stdlib y evaluación fail-closed de schema, identity, bindings, métricas y estabilidad equivalente.
- La unidad califica artifacts de mecanismos assessor; no selecciona, integra ni autoriza un assessor productivo, modelo o provider.
- `E008-SG-02` permanece `OPEN`; `semantic_assurance` continúa `NOT_VERIFIED`.
- `support_sufficient` permanece sin wiring y no autorizado.
- `authority_effect = none`; RDD Stage 2 permanece `NOT AUTHORIZED`; Sprint 7.12 permanece `NOT AUTHORIZED`.

Esta reconciliación es derivada. Qualification evidence no equivale a semantic truth, decisión, permiso ni autoridad.

## Reconciliación CURRENT — E3 Qualification Consumption / Positive Trust Boundary V0

Estado reconciliado al baseline actual:

```text
main HEAD                           a05aa5f081971f36c133ac50dc0756f938a26a1a
último baseline material/producto  e1a1973b7b6cf635337a77e81410ebb873f57bde
último candidate funcional         1143ce2c7818096c393d2fb0cb2986f48440eb93
post-merge Validation              #37208582290 / 1875 passed Ubuntu + Windows
authority_effect                    none
```

- PR #235 integró `E3 Governed Support Evidence Routing V0` y la línea fail-closed de qualification consumption.
- PR #250 integró `E3 Positive Qualification Consumption Trust Boundary V0` sobre el candidate exacto `1143ce2c7818096c393d2fb0cb2986f48440eb93`; el merge commit es `e1a1973b7b6cf635337a77e81410ebb873f57bde`.
- La validación post-merge #37208582290 concluyó PASS con `1875/1875` tests en Ubuntu y Windows, además de `compileall` y diff-check.
- El path positivo ya puede alcanzar `DETERMINISTIC` únicamente mediante material de qualification ligado exactamente, admission composition-owned, PDP/PEP, READY gobernado, RuntimeQualificationBindingV0 exacto y validación temporal de consumo.
- Una qualification `FULL` controlada por el caller, ambigua, stale, con identity/binding drift o sin admission positiva continúa sin habilitar `DETERMINISTIC`.
- PR #251 formalizó la topología gobernada `Design / Documentation PR → Implementation / Governed Construction Cycle PR` sin modificar runtime, seguridad ni autoridad.

Estado epistemológico preservado:

```text
E008-SG-02             OPEN
semantic_assurance     NOT_VERIFIED
support_sufficient     NOT WIRED / NOT AUTHORIZED
productive assessor    NOT SELECTED / NOT AUTHORIZED
RDD Stage 2            NOT AUTHORIZED
Sprint 7.12            NOT AUTHORIZED
self-modification      NOT AUTHORIZED
authority_effect       none
```

La siguiente dirección **candidata de planificación**, todavía no autorizada, es estudiar una frontera ciega de experimento para assessor, con working name:

```text
E3 Blind Assessor Experiment Boundary V0
```

Objetivo provisional:

```text
full governed case set + hidden ground truth
        ↓
assessor-visible blind projection
        ↓
separately authorized assessor experiment
        ↓
bound assessor-result artifact
        ↓
existing Assessor Qualification Pack V0.1
        ↓
PASS | FAIL | INCONCLUSIVE
        ↓
Evidence for later human admission
```

La unidad candidata debe reutilizar el corpus, schemas, qualification runner, identities y Evidence existentes; no autoriza selección de model/provider, red, nueva Capability, store/registry, `support_sufficient`, semantic truth, runtime wiring ni RDD Stage 2.

Esta reconciliación es derivada y no concede autoridad de Design, RED, GREEN, implementación, Ready, Merge ni promoción.


## Reconciliación CURRENT — E3 Governed Local Ollama Assessor Experiment V0

El baseline actual incorpora la cadena gobernada diseñada e integrada mediante
PR #257, PR #258 y PR #259:

```text
Governed Blind Assessor Experiment Harness V0
        ↓
hardened OllamaRuntime local trust boundary
        ↓
Governed Local Ollama Assessor Adapter V0
        ↓
existing RESULTS/v0.1 + Qualification Pack
```

Estado integrado más reciente:

```text
baseline material reconciliado   0a40aa1143f120f7b5a4b544ea49f4b352254b5a
PR #259 candidate                 4bedb40a2d52b1bebad45f796ab9dbf2e5de1663
candidate / merge tree            b14287fa66303c0e4f1c6c62c0af47f08a5dbd8f
post-merge Validation #824        SUCCESS
Ubuntu                            1981/1981 PASS
Windows                           1981/1981 PASS
authority_effect                  none
```

El adapter es una superficie experimental evaluation-side y no convierte a
Ollama ni a ningún modelo en mecanismo productivo de Malāk. La ejecución real
del experimento permanece separada.

```text
live Ollama assessor experiment   NOT AUTHORIZED
exact assessor model              NOT SELECTED / NOT AUTHORIZED
semantic_assurance                NOT_VERIFIED
support_sufficient                NOT WIRED / NOT AUTHORIZED
Protected Finalization Foundation  INTEGRATED / ISOLATED
Protected Finalization productive wiring/use beyond foundation  NOT AUTHORIZED
model promotion                   NOT AUTHORIZED
production admission              NOT AUTHORIZED
RDD Stage 2                       NOT AUTHORIZED
```

La siguiente transición sólo puede considerarse mediante una instrucción
separada del Owner que nombre el modelo local exacto para un live experiment.
Qualification evidence continúa siendo Evidence y no semantic truth, permiso,
promoción ni Authority.

## Reconciliación CURRENT — E3 Assessor Qualification Ground-Truth Repair V0.2

Esta sección **supersede para el estado CURRENT** la reconciliación post-PR #262
que todavía presentaba PR-B como futura y el case-set reparado como inexistente.

PR #262 integró el G0/G1 Design y PR #264 integró la implementación acotada del
repair sobre el allowlist cerrado de cuatro archivos. El merge de PR #264 conserva
exactamente el contenido del candidate validado:

```text
main reconciliado                       73f3a953a1e49a6eb1fac61978e29af1a8d9cc37
PR #264 candidate                       01c159f989f9c2d845d504b0a847ee58b618f56e
candidate → merge content               IDENTICAL / 0 file delta
repaired case-set digest                c76e47c7a788173f5ae137094f0fd0d2bbb1076a799d5b265b6e17a4841cdb77
Ground-Truth Review B                   PASS
Corrected Candidate FULL 4R             PASS
Independent Candidate Revalidation C    PASS
RDD Stage 1 Candidate Conformance       PASS
candidate Validation #842               SUCCESS / 1989 passed Ubuntu + Windows
post-merge Validation #843              SUCCESS / 1989 passed Ubuntu + Windows
authority_effect                        none
```

Disposición CURRENT:

```text
Ground-Truth Repair V0.2 Design         INTEGRATED — PR #262
Ground-Truth Repair V0.2 implementation INTEGRATED — PR #264
old case-set digest                     HISTORICAL / SUPERSEDED FOR NEW QUALIFICATION
independent old ground-truth review     FAIL — HISTORICAL
qualification against old oracle        BLOCKED — HISTORICAL
prior live Run #3                       HISTORICAL EXECUTION EVIDENCE ONLY
historical experimental model           qwen3.5:9b / NOT PROMOTED
repaired case-set digest                c76e47c7a788173f5ae137094f0fd0d2bbb1076a799d5b265b6e17a4841cdb77
repaired case-set                       INTEGRATED / candidate-bound validation PASS
new assessor semantic qualification     NOT YET RE-RUN
new live experiment / rerun             NOT AUTHORIZED
semantic_assurance                      NOT_VERIFIED
E008-SG-02                              OPEN
support_sufficient                      NOT WIRED / NOT AUTHORIZED
Protected Finalization                  NOT AUTHORIZED
model promotion                         NOT AUTHORIZED
production admission                    NOT AUTHORIZED
RDD Stage 2                             NOT AUTHORIZED
authority_effect                        none
```

El FAIL histórico del oracle viejo no es un FAIL de qwen3.5:9b ni de otro
assessor. Run #3 permanece sólo como Evidence histórica y sus respuestas no
certifican el case-set reparado.

La siguiente transición posible requiere una instrucción humana separada:

```text
Ground-Truth Repair V0.2 integrated
        ↓
separately authorized new live model experiment / qualification rerun
        ↓
bound assessor-result artifact
        ↓
existing Qualification Pack
        ↓
PASS | FAIL | INCONCLUSIVE
        ↓
Evidence for later human decision
```

El merge de PR #264 no autoriza ese experimento, selección/promoción de modelo,
`support_sufficient`, Protected Finalization, production admission ni RDD Stage 2.
Qualification evidence continúa siendo Evidence y no semantic truth, permiso,
decisión o Authority.

## Reconciliación CURRENT — PR #267 / RDD Stage 2

Esta sección supersede **únicamente para el estado CURRENT** las declaraciones
anteriores que todavía presentan RDD Stage 2 como `NOT AUTHORIZED`. Los registros
históricos conservan el estado que era correcto para su candidate/baseline y no
deben reescribirse retroactivamente.

Estado reconciliado:

```text
main HEAD                           02daf578012c662f0686357aa48b25722897c82a
main tree                           f5e3788f6990a549238c41a8a946861ddedb5ef6
PR #267 candidate                  48b147e69812f29bd94e9f2df236f9cc357921b2
PR #267 candidate tree             f5e3788f6990a549238c41a8a946861ddedb5ef6
post-merge Validation #853         SUCCESS
Ubuntu                             2016/2016 PASS
Windows                            2016/2016 PASS
RDD Stage 1                       ADOPTED / ACTIVE
RDD Stage 2                       ADOPTED / ACTIVE
risk 0/1                          NOT_APPLICABLE
risk 2                            OPTIONAL / explicit admission only
risk 3/4                          REQUIRED
RDD Stage 3+                      NOT AUTHORIZED
Cognitive Receipt                 NOT AUTHORIZED
Protected Finalization            NOT AUTHORIZED
Persistence Authorization decision/enforcement  NOT AUTHORIZED
Persistent Memory                 NOT AUTHORIZED
authority_effect                  none
```

RDD Stage 2 materializa un `Candidate-Bound Validation Receipt` separado del
Manifest Stage 1. Continúa vigente:

```text
Evidence != Receipt != Validation != Decision != Authority
Receipt validator PASS != Ready != Merge != Authority
```

Esta reconciliación es derivada y no normativa.


## Reconciliación CURRENT — E2/E3 Contract Reliability + E2 Output Contract Alignment — 2026-10-17

El baseline integrado incorpora la cadena de corrección de contract reliability
de self-review y el E2 Output Contract Alignment:

```text
PR #329 merge          8c401b2bed1c114efadba3777c7662f45e56e8c6
PR #331 design merge   8f45e34f2e48fc72210d4d272372bf3be098e535
PR #332 merge / main   961a5a78450c5cd3c2854a3d404e124f97530cda
candidate/tree #332    fef90dd5d6374bc8227fbc31fb508326a5907df1
                       9967ca9682abcea7ecd23b0071c1cca7f9c4dd6b
```

El merge tree de #332 coincide exactamente con el tree del candidate validado.
La validación candidate-bound final cerró F01 y F02, con full suite local
`2097 passed, 1 skipped`, E2E `147 passed` y Validation
`38997285237` attempt 3 en PASS para Ubuntu y Windows.

La ruta E2 focused conserva el parser determinista como enforcement final,
agrega el schema canónico como `response_contract` model-visible y mantiene
separado el `evidence_packet` no confiable. El rechazo posterior a generación
no persiste ni expone raw output; publica únicamente metadata local acotada más
digest/byte count. No se agregaron retries, repair ni fallback.

```text
C01_ATTEMPT                 CONSUMED
C01_RETRY                   FORBIDDEN
C02                         HOLD
C03                         HOLD
MODEL_EXECUTION_AUTHORIZED  NO
```

El PRE-MODEL freeze y Owner G2 anteriores no son reutilizables después del cambio
de contexto model-visible. Antes de cualquier nueva ejecución se requiere un
nuevo freeze y una nueva decisión Owner G2.

Esta sección supersede, sólo para el estado CURRENT de esta línea, referencias
anteriores de baseline conservadas en el README como historial.


## CURRENT — recuperación técnica E2 post-PR #335 (2026-10-18)

Esta sección supersede únicamente el estado CURRENT de esta línea descrito
arriba. Los snapshots y resultados anteriores se conservan como historia.

Integrado validado: `99698bbeab6d38241a9206756e69fd4ca71f6221`, tree
`f9dbf0d9a7bdd3c852440379e8a3b30f4b0e385f`. #334 fue reformulada por el Owner
como hardening prospectivo: diagnóstico E2 con subcausa/campo locales cerrados
y schema focused con variantes completas por kind/ref. El parser conserva
rechazo fail-closed; sin retries, repair, aceptación parcial ni persistencia nueva.

La causa histórica de C02 permanece **INCONCLUSIVE**: el output rechazado no
fue conservado. Esta implementación no demuestra qué regla falló en ese intento
ni califica el decoder real de Ollama. Su compatibilidad efectiva queda como
residual a resolver/disponer en el nuevo contexto PRE-MODEL antes de ejecución.

El merge de #335 ocurrió con gates pendientes; la integración/CI inicial también
precedió al Independent Fix Validator. F335-V01/V02 conservan **FAIL histórico**.
El Owner eligió recuperar el integrado y preservar esos incumplimientos. La
validación independiente posterior aprobó provenance, Fix Validator F334-01,
Gate C, contrato/regresión y FULL 4R actuales. No se retrocertifica el proceso.

Evidencia de recuperación sobre el integrado: afectados 193 PASS, integración
202 PASS, diferencial sintético 704 casos y CI Ubuntu/Windows 2153 PASS por
plataforma. [Validación independiente final](https://github.com/Aranwill/jarvis/pull/335#issuecomment-6254764581)
y [RDD Candidate Conformance actual](https://github.com/Aranwill/jarvis/pull/335#issuecomment-6254769371)
son evidencia sin autoridad. RDD Stage 1/2 nuevo corresponde al merge exacto;
los manifests/receipts premerge siguen históricos e INCONCLUSIVE.

```text
C01_ATTEMPT                 CONSUMED
C01_RETRY                   FORBIDDEN
C02_ATTEMPT                 CONSUMED
C02_RETRY                   FORBIDDEN
C03_ATTEMPT                 NOT_STARTED
C03                         HOLD
E3_C02                      NOT_ATTEMPTED
E4                          NOT_AUTHORIZED
MODEL_EXECUTION_AUTHORIZED  NO
PROCESS_CONFORMANCE_HISTORICAL FAIL
authority_effect            none
```

No se reutilizan el freeze PRE-MODEL ni Owner G2 anteriores. La próxima frontera
es reconciliación post-merge de esta actualización y después **NEW PRE-MODEL
freeze → independent freeze validation → NEW Owner G2**. Ningún receipt ni cierre
de ingeniería admite por sí solo modelos, piloto, siguiente sprint o ejecución.
