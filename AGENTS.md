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
- `docs/development/development_checklist.md`
- `SECURITY.md`

Los documentos derivados pueden resumir evidencia, pero no pueden establecer arquitectura, gobernanza, estado de release ni alcance aprobado de un sprint.

Los snapshots históricos de release describen el estado certificado en su fecha original. No deben reescribirse silenciosamente para coincidir con un HEAD posterior.

## Fuente rechazada

El siguiente documento está rechazado y nunca debe utilizarse como fuente, referencia, autoridad o inspiración para Malāk:

```text
PROJECT - MANIFIESTO MALAK (1).docx
```

No se debe leer, resumir, citar, indexar, transformar ni incorporar su contenido al proyecto.

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
→ un Pull Request
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
- crear o actualizar un Pull Request;
- eliminar archivos;
- reescribir el historial.

Nunca utilices operaciones destructivas de Git para descartar cambios del usuario.

Conserva las modificaciones preexistentes y los archivos untracked no relacionados. Si se superponen con el trabajo solicitado, detente e informa el conflicto.

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
git diff --cached --stat
```

La validación debe ser proporcional al riesgo. Un sprint o release no puede considerarse completo hasta que supere el checklist de desarrollo aplicable.

Si un test no puede ejecutarse debido a restricciones del entorno, distingue un fallo de preparación ambiental de un fallo del producto e informa ambos con precisión.

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
2. lectura del código, pruebas y documentación aplicables;
3. identificación de una necesidad real y comprobada de Malāk;
4. justificación de su utilidad cognitiva, arquitectónica, operativa o de gobernanza;
5. definición explícita del alcance y de lo que queda fuera de alcance;
6. evaluación de riesgos, dependencias, impacto y rollback;
7. validación mediante las cuatro preguntas obligatorias;
8. presentación del plan de ejecución al propietario;
9. debate y revisión integral del plan;
10. aprobación explícita e inequívoca del propietario.

Sin la aprobación explícita del propietario no se debe:

- crear una rama;
- modificar documentación o código;
- incorporar una dependencia;
- cambiar contratos;
- ejecutar una implementación;
- realizar commits, push, Pull Requests o merges.

La aprobación de un sprint anterior no autoriza automáticamente el siguiente.

El orden, número o título de un sprint en un roadmap no obliga a ejecutarlo. Un sprint puede ser redefinido, diferido, reemplazado o descartado cuando su justificación no sea suficiente o cuando exista una alternativa más coherente con los documentos normativos y el baseline vigente.

