# Development Checklist

Versión: 0.6.0-alpha

Estado: Activo

---

# Objetivo

Este documento define el proceso obligatorio de validación antes de cerrar cualquier Sprint, Release o modificación importante del proyecto.

Todo cambio deberá superar este checklist antes de considerarse finalizado.

La metodología de ingeniería aplicable se define en `docs/development/engineering_method.md`.

La disciplina transversal de revisión, incorporación progresiva de capacidades, gates, métricas, RDD experimental y reconciliación derivada se define en `docs/development/malak_construction_protocol.md`.

---

# Arquitectura

Antes de aprobar un cambio validar:

- [ ] Respeta el Blueprint.
- [ ] Respeta la Constitución Cognitiva.
- [ ] Respeta la Constitución de Gobernanza.
- [ ] Simplifica o mantiene simple el Kernel.
- [ ] No rompe la arquitectura orientada a eventos.
- [ ] Respeta Capability First.
- [ ] Respeta Runtime Independence.
- [ ] Toda integración externa utiliza contratos públicos.
- [ ] El Kernel no depende de implementaciones concretas.
- [ ] Respeta Human in Control.

---

# Cobertura de revisión integral

Cuando el trabajo sea una revisión integral, auditoría, certificación, reconciliación o admission review, validar:

- [ ] Se levantó un inventario recursivo de todos los archivos trackeados de cada repositorio incluido en el alcance.
- [ ] Cada archivo inventariado recibió una clasificación o disposición explícita; archivos omitidos silenciosamente: `0`.
- [ ] La profundidad de lectura fue proporcional al rol del artefacto y al problema, sin utilizar búsquedas textuales como sustituto del inventario.
- [ ] Los archivos protegidos o expresamente prohibidos fueron identificados sin abrirse ni procesarse y quedaron clasificados con la razón correspondiente.
- [ ] Cuando el alcance fue global, se contrastaron `Aranwill/jarvis`, `Aranwill/malak-project-vault` y `Aranwill/malak-vault-sync-agent` según disponibilidad y autoridad.
- [ ] Los findings distinguen fuente oficial, proyección derivada y mecanismo de sincronización.

---

# Incorporación progresiva de capacidades futuras

Antes de admitir una nueva unidad funcional o diseñar una capability futura, validar:

- [ ] La necesidad fue demostrada desde el baseline actual y no únicamente desde una secuencia histórica del roadmap.
- [ ] Se consultó `SECURITY.md` y se identificaron restricciones, riesgo residual o precondiciones activadas por la superficie propuesta.
- [ ] Se consultó `docs/project/implementation_roadmap.md`.
- [ ] Se consultó `documents/projects/jarvis/ideas.md`.
- [ ] Se leyó explícitamente `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md` cuando la tarea busca determinar la próxima implementación.
- [ ] Se revisó `docs/project/concepts/README.md` y recursivamente `docs/project/concepts/**` para las referencias relacionadas con la necesidad.
- [ ] Las ideas o conceptos candidatos fueron revalidados contra Blueprint, Constituciones, Gobernanza, `SECURITY.md`, ADR, código, tests, riesgos y dependencias vigentes.
- [ ] Cada propuesta reutilizada fue clasificada explícitamente como `ADOPT`, `ADAPT`, `OBSERVE` o `REJECT`.
- [ ] Se distinguió `security requirement != implemented control` y `research gap != roadmap`.
- [ ] Ninguna idea, concepto, research gap o referencia futura fue interpretada como autorización automática de implementación o sprint.
- [ ] No se rediseñó desde cero una capacidad sin comprobar primero si su intención ya estaba preservada en `ideas.md`, `MALAK_RESEARCH_HORIZON_MAP.md` o `docs/project/concepts/**`.

---

# Seguridad

Para todo cambio con impacto de seguridad, autoridad, identidad, contexto, persistencia, red, agentes, tools, modelos, datos o integraciones externas, validar según aplicabilidad:

- [ ] Se revisó `SECURITY.md` como política protegida y se preservó su precedencia documental.
- [ ] El cambio distingue controles implementados de requisitos o capacidades futuras.
- [ ] Se preservan Zero Trust, Defense in Depth, Least Privilege, Least Context y Human in Control.
- [ ] Una ausencia, inconsistencia o fallo de autorización no se convierte en permiso; el comportamiento es deny-by-default / fail-closed cuando corresponde.
- [ ] LLM output, tool output, retrieval, Memory, evidence, score o receipt no se interpretan como autoridad.
- [ ] La ruta sensible conserva separación entre request, decision, enforcement, protected operation y evidence/audit.
- [ ] Si ingresa contenido no confiable, se evaluó Prompt & Context Trust Boundary e indirect prompt injection.
- [ ] Si se incorporan datos sensibles o persistencia, se evaluaron minimización, finalidad, disclosure, retención y redaction.
- [ ] Si se incorpora un modelo, dependency, dataset, skill, plugin, container, MCP/A2A server/adapter u otro artefacto externo, se evaluaron provenance, integridad, trust, permisos requeridos, rollback y supply-chain risk.
- [ ] Si existe delegación entre agentes, tools o componentes, la autoridad efectiva no puede superar la autoridad del delegador ni los scopes/policies aplicables.
- [ ] Si un componente puede ser comprometido, se evaluaron revocación, aislamiento, blast radius, preservación de evidencia, recovery y revalidación antes de reintroducción.
- [ ] El diseño no depende de la cooperación de un componente sospechado para revocar autoridad o preservar evidencia crítica.
- [ ] Un incidente o mejora no concede autoridad para modificar políticas, PDP/PEP, leyes fundacionales o baseline productivo.
- [ ] No se habilita `hack back` autónomo ni respuesta fuera de infraestructura propia/expresamente autorizada.
- [ ] Los riesgos residuales nuevos o existentes quedaron explícitos y no fueron ocultados por una validación parcial.

---

# Especificación y método de desarrollo

Cuando corresponda al alcance y riesgo del cambio, validar:

- [ ] El comportamiento esperado fue especificado antes de considerar terminada la implementación.
- [ ] La especificación identifica requisitos, escenarios o criterios de aceptación verificables.
- [ ] La especificación no contradice Constitución Cognitiva, Constitución de Gobernanza, Blueprint, ADR aceptados ni contratos superiores aplicables.
- [ ] Las decisiones arquitectónicas significativas permanecen en ADR u otros artefactos de arquitectura y no fueron duplicadas como decisiones de implementación dentro de la especificación.
- [ ] Existe trazabilidad suficiente entre requisito o escenario, test, implementación y evidencia de validación.
- [ ] Seguridad, autorización, contratos públicos, límites del Kernel y lógica determinista crítica utilizaron TDD cuando fue técnicamente viable.
- [ ] Las correcciones de defectos reproducibles incorporan prueba de regresión cuando fue técnicamente viable.
- [ ] Toda excepción relevante a TDD está justificada y no reduce la validación obligatoria de seguridad, contratos o comportamiento crítico.
- [ ] Ninguna herramienta de SDD o testing fue convertida implícitamente en fuente de autoridad arquitectónica.

---

# Planificación y ejecución por gates

Cuando el cambio sea material, validar:

- [ ] El plan fue dividido en gates pequeños, verificables y reversibles.
- [ ] Cada gate declaró objetivo, precondiciones, alcance, fuera de alcance, validación, STOP condition y rollback cuando correspondía.
- [ ] Se registró la identidad del candidato evaluado cuando correspondía.
- [ ] No se avanzó al gate siguiente con un `FAIL` bloqueante o un `INCONCLUSIVE` no resuelto.
- [ ] Un fallo local no fue utilizado para ampliar automáticamente archivos, componentes, arquitectura o dependencias.
- [ ] Las métricas aplicables del gate fueron registradas o marcadas explícitamente como `N/A`.

---

# Revisión proporcional al riesgo

Cuando corresponda, validar:

- [ ] El cambio posee una clasificación de riesgo proporcional a su impacto.
- [ ] La revisión utilizó los lentes 4R necesarios: Risk, Readability, Reliability y Resilience.
- [ ] Cuando correspondió FULL 4R, cada lente produjo estado, preguntas evaluadas, findings y evidencia propios en lugar de una única etiqueta `4R PASS`.
- [ ] Los cambios triviales no fueron sometidos a controles desproporcionados sin evidencia que justificara el escalamiento.
- [ ] Los cambios de riesgo alto o crítico fueron sometidos a FULL 4R.
- [ ] Un finding que reveló mayor riesgo produjo escalamiento de revisión cuando correspondía.
- [ ] Writer, Reviewer, Validator y Authority permanecieron separados cuando el riesgo del cambio lo exigía.
- [ ] El reviewer no modificó el candidato ni se concedió autoridad para aprobarlo.

---

# Corrección acotada

Cuando un finding requirió corrección, validar:

- [ ] La corrección tuvo objetivo y alcance explícitos.
- [ ] Se definieron archivos o componentes autorizados cuando correspondía.
- [ ] Se definió un Correction Budget proporcional al finding.
- [ ] El Fix Actor no amplió silenciosamente el alcance.
- [ ] No se introdujeron dependencias, cambios arquitectónicos o modificaciones de contratos fuera del presupuesto autorizado.
- [ ] Si la corrección no podía resolverse dentro del presupuesto, se escaló en lugar de ampliar automáticamente el scope.
- [ ] El número de rondas de corrección permaneció dentro del límite definido.

---

# Validación independiente de correcciones

Cuando hubo corrección acotada, validar:

- [ ] Un Fix Validator verificó el delta resultante de forma independiente cuando el riesgo lo justificaba.
- [ ] El validator comprobó que solo se modificaron archivos o componentes autorizados.
- [ ] El validator comprobó que el finding fue realmente resuelto.
- [ ] El validator comprobó regresiones, contratos y arquitectura aplicables.
- [ ] El resultado se clasificó como `PASS`, `FAIL` o `INCONCLUSIVE`.
- [ ] `INCONCLUSIVE` nunca fue interpretado como `PASS`.
- [ ] Un resultado `FAIL` produjo evidencia suficiente de la causa.
- [ ] La validación corresponde al candidato exacto evaluado.

---

# Runtime

Validar:

- [ ] El Runtime inicia correctamente.
- [ ] Todo Runtime implementa el contrato oficial (`LLMRuntime`) cuando corresponda.
- [ ] Todo Runtime posee una implementación de prueba (Mock) cuando corresponda.
- [ ] No existen dependencias directas entre Runtime y Kernel.
- [ ] El Launcher funciona correctamente.
- [ ] El Logger funciona correctamente.
- [ ] No existen errores de imports.
- [ ] No existen dependencias rotas.

---

# Testing

Validar:

- [ ] Todo contrato nuevo posee al menos un test asociado.
- [ ] Toda abstracción posee una implementación de prueba cuando corresponda.
- [ ] Los tests cubren los criterios de aceptación relevantes definidos por la especificación cuando corresponda.
- [ ] Los cambios de seguridad incluyen casos negativos y fail-closed cuando corresponda.
- [ ] Los flujos integrados modificados poseen pruebas de integración o E2E proporcionales al riesgo cuando corresponda.
- [ ] Todos los tests pasan correctamente.
- [ ] No existen tests desactualizados.
- [ ] No existen referencias al namespace anterior.

---

# Código

Validar:

- [ ] No existen dependencias circulares.
- [ ] Los imports respetan la arquitectura definida.
- [ ] No existen TODO olvidados.
- [ ] No existen FIXMEs sin documentar.
- [ ] No existen archivos temporales.
- [ ] No existen artefactos de prueba.
- [ ] No existen rutas hardcodeadas nuevas.
- [ ] La solución es proporcional al problema y no introduce complejidad innecesaria.

---

# Evidencia y comportamiento operacional

Cuando forme parte del alcance del cambio, validar:

- [ ] Las métricas relevantes poseen baseline o punto de comparación identificable.
- [ ] Las pruebas E2E distinguen claramente comportamiento esperado, resultado y condiciones ambientales.
- [ ] Las afirmaciones de mejora se apoyan en evidencia reproducible y no únicamente en apreciación cualitativa.
- [ ] La evidencia no se interpreta como autorización para ampliar alcance o modificar gobernanza.
- [ ] La identidad del candidato está registrada mediante commit SHA, hash u otro identificador verificable cuando corresponda.
- [ ] Si el candidato cambió después de una revisión o validación, la evidencia previa fue revalidada.
- [ ] Los receipts, si existen, están ligados al candidato exacto y no sustituyen la aprobación humana requerida.

---

# Perfil RDD progresivo

Cuando se utilicen receipts o evidencia estructurada inspirada en Receipt-Driven Development, validar:

- [ ] Se preservó `Evidence != Receipt != Validation != Decision != Authority`.
- [ ] El receipt o manifest está ligado a una identidad exacta de candidato.
- [ ] Un cambio de candidato invalidó o provocó revalidación de la evidencia candidate-bound afectada.
- [ ] Los únicos estados de validación utilizados por el receipt fueron `PASS`, `FAIL` o `INCONCLUSIVE`.
- [ ] Un receipt no produjo estados de autoridad como `APPROVED`, `AUTHORIZED` o `MERGED`.
- [ ] La adopción fue proporcional y experimental; no se creó infraestructura RDD adicional sin necesidad demostrada y autorización separada.
- [ ] Se midió si el perfil RDD aportó trazabilidad útil o burocracia innecesaria antes de promoverlo a un contrato o subsistema formal.

---

# Documentación

Validar:

- [ ] La documentación refleja el estado real de la implementación.
- [ ] Las especificaciones aprobadas reflejan el comportamiento aceptado cuando corresponda.
- [ ] Las decisiones arquitectónicas significativas fueron registradas (ADR cuando corresponda).
- [ ] Los metadatos del AKS permanecen consistentes.
- [ ] Documentación actualizada.
- [ ] Changelog actualizado cuando corresponda.
- [ ] Decisiones arquitectónicas documentadas.
- [ ] Nuevos componentes documentados.
- [ ] Si cambió una política, límite o postura de seguridad, `SECURITY.md` fue revisado y reconciliado sin presentar requisitos futuros como controles ya implementados.
- [ ] Si cambió una visión, gap o clasificación de investigación relevante, `MALAK_RESEARCH_HORIZON_MAP.md`, `docs/project/concepts/README.md` y las ideas relacionadas fueron revisadas para evitar drift conceptual.
- [ ] Al cerrar un Sprint, `README.md` fue revisado y reconciliado con el baseline integrado; cuando corresponda refleja el último Sprint completado, el estado operativo, la evidencia de validación y las capacidades disponibles.
- [ ] Al cerrar un Sprint, las fuentes `CURRENT_STATE` aplicables fueron revisadas y reconciliadas después del merge, o se documentó explícitamente que no requerían cambios.

---

# Reconciliación derivada post-merge

Después de integrar un cambio en `Aranwill/jarvis/main`, validar:

- [ ] Se evaluó si las rutas modificadas están observadas o mapeadas por el Malāk Vault Synchronization Agent.
- [ ] Se verificó explícitamente la cobertura de nuevas referencias obligatorias o rutas relevantes introducidas en `AGENTS.md`, `SECURITY.md` y `docs/project/concepts/**`.
- [ ] Cuando correspondía, el Project Vault fue reconciliado mediante el flujo gobernado del Sync Agent.
- [ ] El Vault y el Sync Agent permanecieron explícitamente subordinados a `Aranwill/jarvis/main` como fuente de verdad.
- [ ] Un fallo de sincronización dejó el drift visible y no fue presentado como reconciliación exitosa.
- [ ] Antes de admitir una nueva unidad de trabajo no permanecía `BASELINE_DRIFT`, `PROJECTION_DRIFT`, `STATE_DRIFT` o drift semántico downstream relevante sin resolver, reconciliar o aceptar explícitamente como riesgo documentado.
- [ ] La reconciliación downstream no fue interpretada como condición para reabrir un Sprint ya cerrado ni como autoridad sobre el baseline oficial.

---

# Git

Validar:

- [ ] Git limpio.
- [ ] Commit realizado.
- [ ] Push realizado.
- [ ] Historial preservado.
- [ ] La rama se encuentra sincronizada con el repositorio remoto.
- [ ] El commit o candidato validado corresponde al contenido realmente revisado.

---

# Certificación

Antes de cerrar el Sprint confirmar:

- [ ] El proyecto continúa respetando los principios fundacionales de Malāk.
- [ ] El proyecto puede continuar evolucionando sin refactorizar el Kernel.
- [ ] La implementación quedó preparada para el siguiente Sprint.
- [ ] Los criterios de aceptación aplicables están satisfechos por evidencia verificable.
- [ ] La aceptación humana requerida fue obtenida antes de promover el cambio al baseline.
- [ ] No permanece un `FAIL` o `INCONCLUSIVE` crítico sin resolución o aceptación explícita de riesgo.
- [ ] La reconciliación documental post-merge fue completada antes de declarar cerrado el Sprint.
- [ ] Si existían proyecciones downstream afectadas, su reconciliación quedó completada o explícitamente registrada como pendiente antes de iniciar la siguiente admission review.

---

# Regla Fundamental

Si cualquiera de los puntos obligatorios aplicables falla:

La implementación NO debe considerarse terminada.

Primero se corrige.

Después se certifica.

Finalmente se continúa con el siguiente Sprint.