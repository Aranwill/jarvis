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

CAL-014 — Protected Durable Reliance está activado normativamente mediante CC-013, R-023 y ADR-006. Esa activación no autoriza Persistence Authorization, Persistent Memory, Conversation G2B, RDD Stage 2 ni Sprint 7.12.

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

/self-review help
/self-review test-v0 <run_id> <validation_ref> [<validation_ref> ...]

exit
quit
salir
```

La CLI también controla:

- entradas vacías;
- continuidad conversacional efímera durante la ejecución;
- reinicio del contexto activo mediante `new`, con rotación de sesión;
- interrupciones mediante `Ctrl + C`;
- finalización mediante EOF;
- errores del runtime presentados como errores controlados.

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
Protected Finalization            NOT AUTHORIZED
model promotion                   NOT AUTHORIZED
production admission              NOT AUTHORIZED
RDD Stage 2                       NOT AUTHORIZED
```

La siguiente transición sólo puede considerarse mediante una instrucción
separada del Owner que nombre el modelo local exacto para un live experiment.
Qualification evidence continúa siendo Evidence y no semantic truth, permiso,
promoción ni Authority.

## Reconciliación CURRENT — E3 Assessor Qualification Ground-Truth Repair V0.2

Esta sección **supersede para el estado CURRENT** las transiciones descritas en reconciliaciones anteriores que todavía presentaban el live Ollama experiment como no ejecutado o el exact model como no seleccionado.

PR #262 integró únicamente el G0/G1 Design de `E3 Assessor Qualification Ground-Truth Repair V0.2`. El merge conserva exactamente el árbol del candidate validado:

```text
main baseline                         82d79484630b8636582971e37678f16daf5f1c6c
PR #262 candidate                     971a2b8d9a1f7e2a7042640dbad23aa11d180e6e
candidate / merge tree                96fd81cf6d29d0e346392ec6b4e422dacb996903
Independent Design Fix Validation B   PASS
candidate Validation #831             SUCCESS
post-merge Validation #832            SUCCESS
Ubuntu / Windows                      1981/1981 PASS
authority_effect                      none
```

El trigger del repair es un `FAIL` independiente del ground truth ligado al case-set digest histórico. Ese resultado **no es un FAIL de qwen3.5:9b ni de otro assessor**. Impide usar el oracle viejo para producir una qualification semántica defendible.

```text
Ground-Truth Repair V0.2 Design       INTEGRATED — PR #262
old case-set digest                    23e045b5e5aede8341323c486e77893d7161899f0c20870703efff28789f3f83
independent old ground-truth review    FAIL
qualification against old oracle       BLOCKED
assessor semantic qualification        UNKNOWN
prior live Run #3                      HISTORICAL EXECUTION EVIDENCE ONLY
historical experimental model          qwen3.5:9b / NOT PROMOTED
future PR-B                             NOT AUTHORIZED
repaired case-set digest                NOT CREATED
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

El Design integrado congela:

```text
scenario label != scenario evidence
expected outcome != proof of expected outcome
contract validity != semantic validity
equivalence != material support
```

El resultado live previo permanece preservado sólo como evidencia histórica de ejecución. Sus respuestas no pueden utilizarse para construir o ajustar el ground truth reparado.

La siguiente transición legal es:

```text
separate Owner authorization for PR-B
→ RED
→ GREEN
→ targeted validation
→ Candidate FULL 4R
→ independent ground-truth review on NEW exact digest
→ independent candidate validation
→ RDD Stage 1 Candidate Conformance
→ Owner review / Ready / Merge
→ post-merge reconciliation
→ separately authorized new live model experiment
→ Qualification Pack
→ PASS | FAIL | INCONCLUSIVE
```

PR #262 no autoriza ninguna de esas etapas posteriores.
