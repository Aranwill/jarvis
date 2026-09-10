# AGENTS.md — Instrucciones del repositorio Malāk

## Propósito

Este archivo define las reglas operativas que deben seguir los asistentes automatizados y los agentes de desarrollo al trabajar en el repositorio de Malāk.

Estas instrucciones rigen el trabajo en el repositorio. No reemplazan, modifican ni reinterpretan los documentos normativos de arquitectura y gobernanza del proyecto.

## Regla persistente de idioma

- Todas las respuestas al propietario del proyecto deben estar en español.
- Toda documentación nueva debe redactarse en español.
- Los análisis, planes, informes, ADR, RFC, notas de diseño y propuestas deben estar en español.
- Los nombres de clases, funciones, módulos, APIs, comandos, rutas y términos técnicos existentes pueden mantenerse en inglés.
- No se deben traducir identificadores técnicos ni nombres existentes cuando hacerlo afecte la consistencia del código o del repositorio.
- Cuando una fuente esté en inglés, su contenido debe explicarse en español.

## Raíz del repositorio

La raíz Git efectiva del repositorio es:

```text
D:\Ollama\jarvis
```

Ejecuta Git, Python, los tests y los comandos de validación desde este directorio, salvo que una tarea aprobada requiera explícitamente otra ubicación.

`D:\Ollama` es el espacio de trabajo contenedor, no la raíz del repositorio Git.

## Identidad del proyecto

- Nombre oficial: Malāk
- Identificador técnico: `malak`
- Nombre histórico: Jarvis
- Namespace del código fuente Python: `src/malak`
- Baseline nominal: `v0.6.0-alpha`

Las referencias históricas a Jarvis pueden conservarse cuando sean necesarias para la trazabilidad. No deben interpretarse como la identidad actual del proyecto.

## Autoridad y precedencia documental

Cuando exista conflicto entre documentos, aplica este orden:

1. Constitución Cognitiva.
2. Constitución de Gobernanza.
3. Blueprint.
4. Especificaciones aprobadas, incluida la especificación del Kernel.
5. Architecture Decision Records aceptados.
6. Capabilities y contratos públicos.
7. Configuración.
8. Documentación operativa y de desarrollo.
9. Registros históricos.
10. Documentos derivados e informativos.

Las fuentes principales incluyen:

- `docs/governance/cognitive_constitution.md`
- `docs/governance/governance_constitution.md`
- `docs/architecture/blueprint.md`
- `docs/architecture/kernel.md`
- `docs/architecture/architecture_quality_gates.md`
- `docs/development/engineering_method.md`
- `docs/development/development_checklist.md`
- `docs/development/malak_construction_protocol.md`
- `SECURITY.md`

Para revisiones de próxima implementación, seguridad, capacidades futuras o arquitectura de horizonte, deberá consultarse además de forma explícita:

- `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md`
- `docs/project/concepts/README.md`
- las referencias aplicables bajo `docs/project/concepts/**`.

`MALAK_RESEARCH_HORIZON_MAP.md` es una referencia conceptual no normativa. Su lectura obligatoria evita perder gaps y restricciones ya investigados; no aumenta su autoridad ni convierte un gap en roadmap o autorización.

Los documentos derivados pueden resumir evidencia, pero no pueden establecer arquitectura, gobernanza, estado de release ni alcance aprobado de un sprint.

Los snapshots históricos de release describen el estado certificado en su fecha original. No deben reescribirse silenciosamente para coincidir con un HEAD posterior.

## Recuperación de contexto: Vault-first

Para consultas ordinarias de contexto, continuidad, estado general, roadmap,
decisiones, arquitectura conocida o referencias conceptuales de Malāk, utiliza
el Malāk Project Vault como punto de entrada de recuperación de contexto.

Secuencia predeterminada:

```text
08-session-context/MALAK_SESSION_CONTEXT.md
        ↓
documento especializado del Vault cuando sea necesario
        ↓
respuesta basada en contexto derivado vigente
```

La fuente de autoridad y la fuente de recuperación de contexto son conceptos
distintos. `Aranwill/jarvis/main` continúa siendo la fuente de verdad; el Vault
es la fuente derivada preferida para recuperar contexto de forma eficiente.

No realices por defecto una revisión transversal de Malāk, Vault y Sync Agent
para una consulta ordinaria si el Vault aporta contexto suficiente y coherente.

Escala a las fuentes oficiales de Malāk cuando:

- la tarea vaya a modificar código o documentación oficial de Malāk;
- se requiera evidencia exacta de implementación, tests o estado operativo;
- se requiera autoridad normativa, arquitectónica, de seguridad o gobernanza;
- el Vault presente contradicciones, gaps, drift o estado no reconciliado;
- la información necesaria no esté disponible o sea incierta en el Vault;
- se solicite una auditoría, certificación o revisión independiente desde fuente;
- el propietario solicite explícitamente revisar directamente el repositorio.

Consulta el Vault Sync Agent únicamente cuando la tarea involucre sincronización,
mapping, cobertura, reconciliación, propuestas de sync o un fallo reportado por
ese mecanismo.

El `Minimum Review Set` transversal definido a continuación aplica a revisiones
integrales, auditorías, reconciliaciones y detección de drift; no constituye el
procedimiento predeterminado para recuperación ordinaria de contexto.

## Revisión integral del proyecto y detección de drift

Cuando la tarea solicite una revisión integral del estado de Malāk, validar el
baseline, analizar arquitectura, determinar próximos pasos, contrastar roadmap,
detectar inconsistencias o reconciliar los repositorios relacionados, la revisión
deberá ser transversal y basada en evidencia.

Una revisión no deberá declararse completa por haber inspeccionado únicamente
`README.md`, el roadmap, el código o el último sprint.

### Minimum Review Set

Salvo que el alcance solicitado sea explícitamente más pequeño, una revisión
integral deberá considerar, como mínimo y según aplicabilidad:

```text
Malāk — source of truth
├── AGENTS.md
├── Constituciones aplicables
├── Blueprint
├── Architecture Quality Gates
├── SECURITY.md                         ← política de seguridad obligatoria
├── docs/development/engineering_method.md
├── docs/development/malak_construction_protocol.md
├── especificaciones y contratos aplicables
├── baseline vigente
├── sprint vigente o último baseline cerrado
├── implementation roadmap
├── ADR aceptados
├── Decision Index y decisiones relevantes
├── documents/projects/jarvis/ideas.md
├── docs/project/concepts/README.md
├── docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
├── docs/project/concepts/**          ← lectura recursiva obligatoria
├── código afectado
└── tests y evidencia aplicables

Project Vault — proyección derivada
├── CURRENT_BASELINE.md
├── CURRENT_COMPONENTS_MAP.md
├── IMPLEMENTATION_ROADMAP.md
├── PENDING_DECISIONS.md
├── MALAK_SESSION_CONTEXT.md
├── CONCEPTUAL_FOUNDATIONS.md
└── KNOWLEDGE_INDEX.md

Vault Sync Agent — mecanismo de reconciliación
├── baseline / HEAD vigente
├── reglas de candidate mapping
├── cobertura de rutas fuente
├── rutas no mapeadas
├── estado de sincronización
├── propuestas pendientes
└── evidencia de reconciliación
```

### Cobertura exhaustiva obligatoria

Toda revisión declarada `integral`, `completa`, `transversal`, de admisión de sprint, certificación, reconciliación o auditoría debe comenzar por un inventario recursivo de todos los archivos trackeados de los repositorios incluidos en el alcance.

Cada archivo debe recibir una clasificación o disposición explícita. La profundidad de lectura puede ser proporcional al rol del artefacto y a la pregunta, pero ningún archivo puede quedar fuera del inventario por no coincidir con una búsqueda textual.

La revisión debe poder demostrar conceptualmente:

```text
tracked files discovered = N
tracked files classified = N
silently omitted files   = 0
```

Utiliza un File Coverage Ledger o evidencia equivalente con, como mínimo:

```text
path
repository
artifact_type
authority_class
review_relevance
review_depth
disposition
related_findings
```

Disposiciones candidatas:

```text
FULL_READ
TARGETED_READ
STRUCTURAL_INSPECTION
HISTORICAL_REFERENCE
GENERATED_OR_DERIVED
NOT_APPLICABLE_WITH_REASON
PROTECTED
REJECTED_DO_NOT_READ
```

Un archivo expresamente prohibido por estas instrucciones debe aparecer en el inventario como `REJECTED_DO_NOT_READ`; no debe abrirse, resumirse ni procesarse.

La cobertura exhaustiva no obliga a leer todos los archivos con la misma profundidad. Obliga a que todos sean descubiertos, clasificados y tratados deliberadamente.

### Conjunto obligatorio para planificar la próxima implementación

Cuando la tarea consista en determinar el próximo cambio, admitir un sprint,
preparar un plan de implementación o decidir qué trabajo debe realizarse a
continuación, la revisión deberá contrastar explícitamente, según aplicabilidad:

```text
SECURITY.md
        ↓
política activa, límites actuales, riesgo residual y requisitos de seguridad

docs/project/implementation_roadmap.md
        ↓
planificación derivada vigente

documents/projects/jarvis/ideas.md
        ↓
ideas, visión e iniciativas todavía no necesariamente promovidas

docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
        ↓
gaps, refuerzos y líneas WATCH ya reconciliadas; referencia no normativa

docs/project/concepts/**
        ↓
referencias conceptuales no normativas; lectura recursiva cuando el tema aplique

docs/development/engineering_method.md
        ↓
método de ingeniería, revisión, bounded correction y validación

docs/development/malak_construction_protocol.md
        ↓
cobertura exhaustiva, incorporación progresiva, gates, métricas y RDD experimental
```

También deberán revisarse el baseline vigente, la última ficha de sprint
integrada y las fuentes normativas o técnicas afectadas.

`SECURITY.md` y `MALAK_RESEARCH_HORIZON_MAP.md` no deben omitirse únicamente porque el próximo cambio parezca funcional y no de seguridad: una nueva superficie puede activar una restricción, dependencia o gap previamente invisible desde el roadmap.

La revisión debe distinguir explícitamente:

```text
roadmap        != autorización
idea           != roadmap
concepto       != baseline
research gap   != implementación aprobada
security requirement != capability implementada
método         != autoridad arquitectónica
evidencia      != permiso para ampliar alcance
receipt        != autoridad
```

No se debe proponer una implementación basándose únicamente en el roadmap ni
únicamente en una idea o referencia conceptual.

### Incubación progresiva de capacidades futuras

Antes de diseñar desde cero una nueva capacidad, consulta primero el roadmap, `documents/projects/jarvis/ideas.md`, `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md` y `docs/project/concepts/**` para determinar si la intención futura ya fue explorada o preservada.

La necesidad debe nacer del baseline vigente. Una idea o concepto relacionado se revalida contra arquitectura, gobernanza, `SECURITY.md`, código, tests, riesgos y dependencias actuales y se clasifica como:

```text
ADOPT
ADAPT
OBSERVE
REJECT
```

La clasificación organiza la decisión; no concede autorización.

No se debe ignorar una intención futura ya preservada ni forzarla sobre un baseline que todavía no demuestra necesidad.

### Planificación por gates cortos, deterministas y reversibles

Todo plan de implementación material deberá dividirse en gates pequeños y
verificables. Cada gate debe declarar, cuando corresponda:

```text
objetivo exacto
precondición
candidate identity
risk class
archivos autorizados
cambio mínimo esperado
fuera de alcance
validación focalizada
métricas
4R aplicable
resultado esperado
condición de STOP
checkpoint / rollback
```

Reglas operativas:

- un gate debe resolver una preocupación principal;
- toda modificación debe ser acotada, determinista, observable y proporcional al objetivo autorizado;
- el candidate debe contener únicamente el cambio mínimo necesario para resolver el invariante u objetivo aprobado;
- cualquier refactor, limpieza, simplificación, reorganización o mejora lateral no necesaria debe quedar fuera del candidate y requiere un scope/gate separado;
- comenzar con tests focalizados y ampliar validación de forma proporcional;
- no avanzar al gate siguiente si el gate actual no está verde;
- un `INCONCLUSIVE` no equivale a `PASS`;
- un fallo no autoriza ampliar automáticamente archivos, arquitectura o scope;
- el checkpoint debe permitir identificar con claridad el último estado verde;
- repetir una validación solo cuando cambió el artefacto o nueva evidencia la
  invalida;
- la suite completa y la validación de integración corresponden al cierre o a
  puntos de riesgo que realmente lo justifiquen.

Formato conceptual recomendado:

```text
Gate N
├── objetivo
├── scope exacto
├── candidate identity
├── archivos
├── modificación
├── test / check
├── metrics
├── 4R evidence
├── expected result
├── STOP si falla
└── rollback al último checkpoint verde
```

Cuando corresponda FULL 4R, `Risk`, `Readability`, `Reliability` y `Resilience` deben registrar evidencia separada; una única etiqueta `4R PASS` no basta como demostración.

El perfil RDD de Malāk es progresivo: Candidate Identity, evidencia candidate-bound, validación independiente y receipts experimentales pueden utilizarse para mejorar trazabilidad, pero `Evidence != Receipt != Validation != Decision != Authority`. Ningún receipt puede aprobar, autorizar, promover o mergear un candidato.

Como adaptación incremental de RDD en Malāk, el alcance del candidate no debe expandirse durante implementación, corrección o review para incorporar mejoras laterales. Una necesidad nueva se registra y se somete a su propio gate; no se introduce silenciosamente en el candidate vigente. Esta regla no activa RDD Stage 2.

Esta disciplina operacional complementa
`docs/development/engineering_method.md` y `docs/development/malak_construction_protocol.md`; no las reemplaza ni eleva la autoridad de `AGENTS.md` sobre las fuentes normativas.

### Lectura obligatoria de referencias conceptuales

`docs/project/concepts/**` y todas sus subcarpetas forman parte del contexto
obligatorio cuando una revisión trate, entre otros temas:

- arquitectura futura;
- agentes;
- sandbox;
- cognición;
- modelos;
- conocimiento;
- memoria;
- seguridad;
- ingeniería;
- evidencia;
- evaluación;
- resource governance;
- self-development;
- capacidades todavía no promovidas al roadmap.

En toda revisión cuyo objetivo sea **determinar la próxima implementación de Malāk**, `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md` debe recibir lectura explícita además del inventario recursivo. No debe considerarse cubierto únicamente por haber listado el glob `docs/project/concepts/**`.

Los documentos de `docs/project/concepts/**` continúan siendo referencias
conceptuales no normativas.

Su lectura obligatoria:

```text
NO aumenta su autoridad
NO modifica la precedencia documental
NO autoriza implementación
NO autoriza sprint
NO convierte una idea en baseline
```

En caso de conflicto, deberán prevalecer las fuentes normativas y las decisiones
aprobadas según la jerarquía documental de este archivo.

### Revisión transversal entre repositorios

Cuando la tarea implique estado global del proyecto, reconciliación o detección
de inconsistencias, deberá contrastarse, cuando estén accesibles:

```text
Aranwill/jarvis
        ↓
source of truth

Aranwill/malak-project-vault
        ↓
proyección derivada

Aranwill/malak-vault-sync-agent
        ↓
mecanismo determinista de detección y propuesta
```

Cuando existan instrucciones locales (`AGENTS.md`) en cualquiera de los tres
repositorios, deberán leerse y aplicarse para el trabajo realizado dentro de ese
repositorio. Las reglas locales no pueden elevar la autoridad del Vault ni del
Sync Agent sobre Malāk.

El Vault y el Sync Agent no pueden corregir, reinterpretar ni superar la
autoridad documental del repositorio oficial de Malāk.

Una coincidencia entre documentos derivados tampoco convierte una afirmación en
verdad si contradice la fuente oficial.

### Taxonomía mínima de drift

Las inconsistencias detectadas deberán identificarse explícitamente en lugar de
describirse de forma genérica.

Utiliza, cuando corresponda, categorías como:

```text
BASELINE_DRIFT
ARCHITECTURE_DRIFT
DOCUMENTATION_DRIFT
CONCEPTUAL_DRIFT
PROJECTION_DRIFT
SYNC_DRIFT
COVERAGE_DRIFT
ENCODING_DRIFT
STATE_DRIFT
```

Ejemplos:

```text
BASELINE_DRIFT
→ Vault describe un HEAD anterior al baseline oficial.

CONCEPTUAL_DRIFT
→ una referencia conceptual importante existe en Malāk pero no está proyectada
  o relacionada correctamente en el índice conceptual derivado.

PROJECTION_DRIFT
→ el Vault resume de forma incompleta o contradictoria una fuente oficial.

SYNC_DRIFT
→ el Sync Agent no refleja correctamente un cambio que su mapping debería
  detectar.

COVERAGE_DRIFT
→ aparece una ruta fuente relevante que no está cubierta por las reglas de
  sincronización.

ENCODING_DRIFT
→ el contenido persistido presenta corrupción o transformación de caracteres.

STATE_DRIFT
→ el estado persistido, propuesta pendiente o cursor no representan de forma coherente la realidad verificable.
```

Todo finding de drift deberá, cuando sea posible, indicar:

```text
tipo
fuente de verdad
artefacto divergente
evidencia
impacto
acción recomendada
```

Detectar drift no concede autorización para corregirlo.

La corrección deberá respetar alcance, riesgo, revisión humana y disciplina Git.

### Cobertura de nuevas rutas

Cuando aparezca una nueva carpeta o familia documental relevante en Malāk,
deberá verificarse si el Sync Agent la reconoce.

Una ruta nueva no deberá considerarse correctamente integrada únicamente porque
exista en Git.

Cuando corresponda deberá comprobarse:

```text
source path
    ↓
mapping rule
    ↓
Vault candidate
    ↓
human review / reconciliation
```

Si una ruta relevante no está cubierta por ninguna regla y no está
explícitamente ignorada, deberá reportarse como `COVERAGE_DRIFT`.

No se deberá ampliar automáticamente el mapping para silenciar el finding.

## Fuente rechazada

El siguiente documento está rechazado y nunca debe utilizarse como fuente, referencia, autoridad o inspiración para Malāk:

```text
PROJECT - MANIFIESTO MALAK (1).docx
```

No se debe leer, resumir, citar, indexar, transformar ni incorporar su contenido al proyecto.

En una revisión integral puede aparecer únicamente en el inventario con disposición `REJECTED_DO_NOT_READ`.

## Evaluación obligatoria previa a cualquier cambio

Antes de modificar cualquier archivo, responde explícitamente:

1. ¿El cambio propuesto respeta el Blueprint?
2. ¿El cambio propuesto respeta la Constitución Cognitiva?
3. ¿El cambio propuesto respeta la Gobernanza?
4. ¿El cambio propuesto hace al Kernel más simple o más complejo?

Si alguna respuesta es negativa, dudosa o no está respaldada por evidencia:

- detente antes de editar;
- identifica el conflicto;
- identifica la fuente o el principio afectado;
- solicita instrucciones explícitas al usuario.

Toda acción propuesta debe indicar también su nivel de riesgo cuando corresponda.

## Principios permanentes de ingeniería

Todo trabajo debe preservar:

- Kernel First.
- Capability First.
- Runtime Independence.
- Human in Control.
- Zero Trust internally.
- Seguridad por defecto.
- Denegación por defecto para operaciones sensibles.
- Mínimo privilegio.
- Contratos públicos entre componentes.
- Separación de responsabilidades.
- Trazabilidad y auditabilidad.
- Cambios pequeños, incrementales y reversibles.

El Kernel coordina. No debe absorber lógica de negocio, comportamiento específico de proveedores, ejecución de herramientas ni responsabilidades pertenecientes a Capabilities u otras capas.

Toda funcionalidad nueva pertenece a una Capability, salvo que una decisión arquitectónica explícitamente aprobada establezca lo contrario.

Ningún runtime, proveedor o modelo puede convertirse en una dependencia directa del Kernel.

Ninguna interfaz puede puentear el Kernel ni alterar el flujo arquitectónico aprobado sin una decisión de diseño aprobada. Un harness limitado de Interface Layer sólo puede considerarse con aprobación humana explícita, debe identificarse como infraestructura limitada de validación y nunca debe presentarse como el pipeline completo de Malāk ni como su arquitectura definitiva.

## Control de alcance

No implementes funcionalidad fuera de la tarea o el sprint explícitamente aprobados.

No adelantes capacidades posteriores porque aparezcan en un roadmap, documento histórico o visión arquitectónica.

No se deben introducir agentes, herramientas externas, automatización del sistema operativo, navegación, mensajería externa ni memoria sensible antes de que sus fundamentos requeridos de seguridad y gobernanza estén formalmente aprobados.

Una declaración de planificación contenida en un documento derivado no constituye autorización para implementarla.

## Áreas protegidas

No modifiques los siguientes elementos sin una autorización explícita que identifique los archivos afectados y el cambio previsto:

- Implementación o responsabilidades del Kernel.
- Contratos centrales e interfaces públicas.
- Blueprint.
- Constitución Cognitiva.
- Constitución de Gobernanza.
- Reglas de gobernanza.
- Architecture Quality Gates.
- ADR aceptados o el Decision Index.
- Fundamentos de seguridad.
- Snapshots históricos de release.
- Metadatos de release.
- Reglas del Architecture Knowledge System.

Una solicitud para implementar una funcionalidad ordinaria no autoriza implícitamente cambios en áreas protegidas.

## Secuencia de trabajo obligatoria

Para cualquier cambio:

1. Inspecciona el estado actual del repositorio.
2. Lee las fuentes normativas y técnicas aplicables.
3. Confirma el alcance aprobado.
4. Realiza la evaluación obligatoria de cuatro preguntas.
5. Presenta un plan conciso.
6. Presenta el diff completo propuesto o el contenido exacto propuesto.
7. Espera autorización cuando sea necesaria.
8. Aplica el cambio viable más pequeño.
9. Ejecuta una validación proporcional al cambio.
10. Revisa el diff resultante y el estado de Git.
11. Informa resultados, limitaciones e instrucciones de rollback.

No mezcles limpieza, refactorización o cambios documentales no relacionados con el trabajo solicitado.

## Disciplina de Git y sprints

El flujo de trabajo permanente es:

```text
Un sprint
→ una rama dedicada
→ un alcance explícitamente aprobado
→ una validación completa
→ un Pull Request en Draft
→ revisión explícita
→ Ready for Review con autorización humana
→ merge con autorización humana separada
→ un punto claro de rollback
```

No realices ninguna de las siguientes acciones sin autorización explícita:

- crear, eliminar o cambiar ramas;
- realizar commit;
- realizar push;
- realizar pull o fetch cuando importe el estado de la red;
- realizar merge;
- realizar rebase;
- realizar reset;
- crear tags;
- realizar stash;
- crear un Pull Request;
- actualizar materialmente un Pull Request;
- eliminar archivos;
- reescribir el historial.

Nunca utilices operaciones destructivas de Git para descartar cambios del usuario.

Conserva las modificaciones preexistentes y los archivos untracked no relacionados. Si se superponen con el trabajo solicitado, detente e informa el conflicto.

### Pull Requests siempre en Draft

Todo Pull Request nuevo deberá crearse inicialmente en estado `Draft`.

Flujo obligatorio:

```text
branch
   ↓
changes
   ↓
local validation
   ↓
commit
   ↓
push
   ↓
Draft Pull Request
   ↓
assistant / agent presents scope, diff and evidence
   ↓
Owner performs visual review in GitHub
   ↓
Owner decides whether changes are acceptable
   ↓
Owner manually promotes to Ready for Review
   ↓
final human review
   ↓
explicit merge authorization
```

La creación del Pull Request y su merge son acciones distintas y requieren
autorización humana independiente.

La transición de Draft a Ready for Review no es una acción delegable al
asistente, agente o automatización.

Promoción a Ready for Review exclusivamente humana

Antes de promover un Pull Request, el Owner deberá realizar una revisión visual
desde GitHub que incluya, como mínimo:

archivos modificados;
diff completo;
alcance declarado;
evidencia de validación;
cambios inesperados o fuera de alcance.

El Owner podrá entonces:

REQUEST CHANGES
DEFER
CLOSE
READY FOR REVIEW

Los asistentes, agentes y automatizaciones:

- pueden preparar cambios;
- pueden validar cambios;
- pueden realizar commit y push cuando estén explícitamente autorizados;
- pueden crear el Pull Request únicamente como Draft;
- pueden presentar evidencia y findings;
- pueden indicar que el Draft está listo para revisión humana;
- no pueden promover un Pull Request a `Ready for Review`;
- no pueden utilizar CLI, API, connector ni automatización para realizar esa transición;
- no pueden interpretar una expresión de conformidad como permiso para promoverlo;
- no pueden sustituir la revisión visual del Owner.

Incluso si el Owner expresa verbalmente que el contenido parece correcto, la
promoción deberá ser realizada manualmente por el Owner desde la interfaz de
GitHub.

Un PR en Draft:

representa una propuesta pendiente de revisión;
no implica aprobación;
no se convierte automáticamente en Ready for Review por tener tests en verde;
no se convierte automáticamente en Ready for Review por ausencia de findings;
no deberá mergearse mientras permanezca en Draft.

Los cambios materiales introducidos después de una revisión deberán volver a
evaluarse visualmente antes de que el Owner decida promover o mergear el PR.

Cuando se utilice GitHub CLI para crear un Pull Request:

gh pr create --draft ...

Cuando se utilice una API o herramienta equivalente, deberá establecerse
explícitamente el estado Draft durante la creación.

Ninguna herramienta utilizada por asistentes o agentes deberá ejecutar la
operación equivalente a:

Draft
→ Ready for Review

Principios:

El productor prepara la propuesta; el humano decide cuándo está lista para
ser considerada formalmente.

Author != Reviewer != Authority.

Esta regla aplica también a cambios documentales, salvo que una política futura
aprobada establezca explícitamente una excepción.

## Operaciones sensibles y externas

Aplica denegación por defecto a:

- eliminación de archivos;
- escrituras fuera del repositorio;
- acciones administrativas;
- elevación de privilegios;
- cambios en el sistema operativo;
- APIs externas;
- navegación de red;
- servicios pagos;
- mensajes o correos electrónicos;
- secretos o credenciales;
- datos personales sensibles;
- acciones irreversibles.

Las operaciones sensibles, externas o críticas requieren autorización explícita antes de ejecutarse.

Ningún agente puede elevar sus propios permisos ni debilitar un control de seguridad para completar una tarea.

## Entorno de desarrollo

Entorno oficial:

```text
.venv
Python 3.12.x
```

Intérprete validado:

```text
Python 3.12.10
```

Utiliza el entorno del proyecto en lugar del intérprete global:

```powershell
.\.venv\Scripts\python.exe
```

No añadas dependencias ni herramientas de desarrollo salvo que estén explícitamente aprobadas y documentadas.

## Comandos de validación

Ejecuta la suite completa de tests con:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

El repositorio también proporciona:

```powershell
.\scripts\test.ps1
```

Comprobaciones útiles de Git en modo de solo lectura:

```powershell
git status --short --branch
git diff --check
git diff --stat
git diff --cached --check
git diff --cached --stat
git diff --name-only
git diff --cached --name-only
```

La validación debe ser proporcional al riesgo. Un sprint o release no puede considerarse completo hasta que supere el checklist de desarrollo aplicable.

Si un test no puede ejecutarse debido a restricciones del entorno, distingue un fallo de preparación ambiental de un fallo del producto e informa ambos con precisión.

## Disciplina de encoding y caracteres especiales

Todos los archivos de texto creados o modificados deberán conservar encoding
UTF-8 y caracteres especiales correctos, incluidos acentos, `ñ`, `ā` y símbolos
utilizados por la documentación del proyecto.

Esta validación es obligatoria:

1. inmediatamente después de crear o modificar un archivo de texto;
2. antes de realizar staging;
3. después del staging, verificando que working tree e index contienen el mismo
   contenido;
4. nuevamente antes de cualquier `push` que publique esos cambios.

### Validación UTF-8 en PowerShell

Para inspeccionar un archivo textual utiliza lectura UTF-8 explícita:

```powershell
Get-Content <archivo> -Raw -Encoding UTF8
```

Para detectar indicadores comunes de mojibake sin introducir esos mismos
caracteres dentro de la regla de validación:

```powershell
$mojibakePattern = '{0}|{1}|{2}' -f [char]0x00C3, [char]0x00C2, [char]0xFFFD

Get-Content <archivo> -Raw -Encoding UTF8 |
    Select-String -Pattern $mojibakePattern
```

La salida esperada es vacía.

No utilices `git show | Select-String` como prueba de integridad Unicode.
La combinación de Git y PowerShell puede representar incorrectamente caracteres
aunque el blob persistido sea válido.

`git diff --check` continúa siendo obligatorio cuando corresponda, pero valida
problemas del diff y whitespace; no demuestra por sí mismo que el encoding sea
correcto.

### Verificación working tree ↔ staged blob

Después de `git add`, los archivos staged deberán compararse con el contenido
validado del working tree.

Ejemplo conceptual en PowerShell:

```powershell
$working = git hash-object -- <archivo>
$staged = (git ls-files -s -- <archivo>).Split()[1]
$working -eq $staged
```

El resultado esperado es:

```text
True
```

Si el hash difiere:

- detener el flujo;
- no realizar commit;
- identificar qué cambió entre working tree e index;
- volver a validar contenido y encoding antes de continuar.

### Validación previa al push

Antes de todo `push` con archivos de texto modificados:

- repetir el control UTF-8 sobre los archivos afectados;
- ejecutar `git diff --check` o `git diff --cached --check` según corresponda;
- confirmar que el commit o index contiene únicamente el alcance aprobado;
- no inferir integridad Unicode a partir de cómo una terminal renderiza `git show`.

Si se detecta corrupción o transformación de caracteres, clasificarla como
`ENCODING_DRIFT` y detener la publicación hasta resolverla y revalidarla.

## Clasificación documental

Identifica siempre los documentos como uno de los siguientes tipos:

### Normativo

Define arquitectura, cognición, gobernanza, seguridad o contratos técnicos aprobados de cumplimiento obligatorio.

### Histórico

Registra un release, una decisión, una migración o un estado certificado anterior.

### Derivado

Consolida o resume evidencia por conveniencia. Es informativo y no normativo.

Los documentos derivados deben:

- identificar su commit fuente y su fecha;
- declarar que no son normativos;
- distinguir la evidencia verificada del contexto de planificación proporcionado por el usuario;
- subordinarse a las fuentes normativas en caso de conflicto;
- evitar corregir silenciosamente registros históricos;
- volver a validarse cuando HEAD cambie de manera material.

## Finalización y rollback

Todo cambio completado debe informar:

- archivos modificados;
- validación realizada;
- resultados de los tests;
- incertidumbre restante;
- estado resultante de Git;
- método de rollback.

El rollback debe limitarse a los archivos modificados y no debe descartar trabajo no relacionado del usuario.

Ningún cambio está completo sólo porque se haya escrito código. Está completo únicamente cuando el alcance, la validación, la documentación y el rollback son claros.

## Justificación y aprobación obligatorias de cada sprint

La existencia de un sprint, una ficha de sprint, una entrada de roadmap, una recomendación técnica o una capacidad prevista no constituye autorización para implementarla.

Todos los sprints pendientes se consideran exclusivamente propuestas o recomendaciones hasta completar, como mínimo, las siguientes etapas:

1. inspección completa del baseline vigente;
2. inventario y clasificación exhaustivos de los archivos del alcance de revisión;
3. lectura del código, pruebas y documentación aplicables;
4. contraste de `SECURITY.md`, roadmap, `ideas.md`, `MALAK_RESEARCH_HORIZON_MAP.md` y `docs/project/concepts/**`;
5. identificación de una necesidad real y comprobada de Malāk;
6. justificación de su utilidad cognitiva, arquitectónica, operativa o de gobernanza;
7. definición explícita del alcance y de lo que queda fuera de alcance;
8. evaluación de riesgos, dependencias, impacto y rollback;
9. validación mediante las cuatro preguntas obligatorias;
10. definición de gates, métricas y 4R aplicable;
11. presentación del plan de ejecución al propietario;
12. debate y revisión integral del plan;
13. aprobación explícita e inequívoca del propietario.

Sin la aprobación explícita del propietario no se debe:

- crear una rama;
- modificar documentación o código;
- incorporar una dependencia;
- cambiar contratos;
- ejecutar una implementación;
- realizar commits, push, Pull Requests o merges.

La aprobación de un sprint anterior no autoriza automáticamente el siguiente.

El orden, número o título de un sprint en un roadmap no obliga a ejecutarlo. Un sprint puede ser redefinido, diferido, reemplazado o descartado cuando su justificación no sea suficiente o cuando exista una alternativa más coherente con los documentos normativos y el baseline vigente.

## Prevención de drift y cierre de revisiones

### State-Bearing Document Registry

Para evitar que documentación histórica o conceptual sea interpretada como
estado vigente, las fuentes documentales deberán clasificarse por función.

#### CURRENT_STATE_CORE

Estas fuentes pueden representar estado operativo o de planificación vigente:

- `README.md`
- `docs/project/project_context.md`
- `docs/project/implementation_roadmap.md`

Deben permanecer semánticamente compatibles con el baseline material vigente.

Un commit puramente documental, de merge o de sincronización no obliga por sí
solo a reemplazar todos sus `as_of_commit`. Cada documento deberá declarar qué
representa su commit de referencia.

#### DOMAIN_CURRENT_STATE

Representan estado vigente únicamente dentro de su dominio:

- `PROJECT.md` — identidad y migración del proyecto;
- `docs/development/development_environment.md` — entorno oficial de desarrollo;
- `documents/projects/jarvis/models.md` — inventario local de modelos cuando
  corresponda validarlo.

No deben utilizarse como sustituto del estado arquitectónico o de planificación.

#### NORMATIVE_PROTECTED

Incluye Constituciones, Blueprint, Kernel specification, Architecture Quality
Gates, ADR aceptados, contratos públicos y `SECURITY.md`.

Su metadata histórica o de certificación no debe reinterpretarse
automáticamente como estado operativo corriente.

#### HISTORICAL

Incluye fichas de sprint cerradas, snapshots y evidencia de release.

Los commits, resultados de tests y estados registrados allí pertenecen al
momento histórico que documentan y no constituyen drift por ser anteriores al
HEAD actual.

#### LEGACY

Documentación preservada por trazabilidad que ya no representa el estado
corriente.

Debe incluir una advertencia explícita que identifique su carácter legacy y
dirija hacia la fuente vigente correspondiente.

#### CONCEPTUAL

Incluye `docs/project/concepts/**`, `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md` y registros de ideas.

Describe posibilidades, gaps, refuerzos y referencias; no baseline, roadmap ni autorización.

### Review Closure Gate

Una revisión integral no podrá declararse completa hasta que:

1. se cierre el File Coverage Ledger del alcance con omisiones silenciosas igual a cero;
2. se identifiquen las fuentes CURRENT_STATE aplicables;
3. se contrasten entre sí y contra código/tests cuando corresponda;
4. las referencias antiguas encontradas sean clasificadas explícitamente como estado vigente, histórico, legacy o drift;
5. se contrasten Project Vault y Sync Agent cuando el alcance sea global;
6. se registren findings pendientes, si existen;
7. se cierre primero el inventario de drift antes de iniciar correcciones.

No se utilizará el patrón:

detectar → corregir → continuar buscando → detectar nuevamente.

El patrón requerido será:

inventario → clasificación → corrective packet → validación → cierre.

### Reconciliación derivada después de merge

Después de integrar un cambio en `Aranwill/jarvis/main`, debe evaluarse si las rutas modificadas están observadas o mapeadas por el Malāk Vault Synchronization Agent.

Cuando corresponda, el Project Vault debe reconciliarse mediante el flujo gobernado del Sync Agent antes de utilizar la proyección derivada como base de una nueva admission review.

La reconciliación downstream:

```text
NO reabre el sprint ya cerrado
NO convierte el Vault en source of truth
NO concede autoridad al Sync Agent
```

Si existe `BASELINE_DRIFT`, `PROJECTION_DRIFT`, `STATE_DRIFT` o drift semántico downstream relevante, la siguiente admission review debe esperar a que el finding sea reconciliado, resuelto o aceptado explícitamente como riesgo documentado.

### Auditoría completa vs revisión incremental

Una auditoría transversal completa se realizará cuando exista un trigger
concreto, entre ellos:

- cierre o promoción material de baseline;
- cambio de arquitectura o gobernanza;
- nueva familia documental relevante;
- cambio de mapping del Sync Agent;
- evidencia de drift sistémico;
- solicitud explícita del propietario.

Fuera de esos triggers se utilizará revisión incremental y proporcional al
cambio.

Una vez cerrado un inventario de drift no deberá iniciarse otra búsqueda global
sin un nuevo trigger verificable.