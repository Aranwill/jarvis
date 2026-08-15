# Development Checklist

Versión: 0.6.0-alpha

Estado: Activo

---

# Objetivo

Este documento define el proceso obligatorio de validación antes de cerrar cualquier Sprint, Release o modificación importante del proyecto.

Todo cambio deberá superar este checklist antes de considerarse finalizado.

La metodología de ingeniería aplicable se define en `docs/development/engineering_method.md`.

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

# Revisión proporcional al riesgo

Cuando corresponda, validar:

- [ ] El cambio posee una clasificación de riesgo proporcional a su impacto.
- [ ] La revisión utilizó los lentes 4R necesarios: Risk, Readability, Reliability y Resilience.
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

---

# Regla Fundamental

Si cualquiera de los puntos obligatorios aplicables falla:

La implementación NO debe considerarse terminada.

Primero se corrige.

Después se certifica.

Finalmente se continúa con el siguiente Sprint.
