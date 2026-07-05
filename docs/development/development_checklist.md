# Development Checklist

Versión: 0.6.0-alpha

Estado: Activo

---

# Objetivo

Este documento define el proceso obligatorio de validación antes de cerrar cualquier Sprint, Release o modificación importante del proyecto.

Todo cambio deberá superar este checklist antes de considerarse finalizado.

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
- [ ] Respeta Human in Control.

---

# Runtime

Validar:

- [ ] El Runtime inicia correctamente.
- [ ] El Launcher funciona correctamente.
- [ ] El Logger funciona correctamente.
- [ ] No existen errores de imports.
- [ ] No existen dependencias rotas.

---

# Testing

Validar:

- [ ] Todos los tests pasan correctamente.
- [ ] No existen tests desactualizados.
- [ ] No existen referencias al namespace anterior.

---

# Código

Validar:

- [ ] No existen TODO olvidados.
- [ ] No existen FIXMEs sin documentar.
- [ ] No existen archivos temporales.
- [ ] No existen artefactos de prueba.
- [ ] No existen rutas hardcodeadas nuevas.

---

# Documentación

Validar:

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

---

# Certificación

Antes de cerrar el Sprint confirmar:

- [ ] El proyecto continúa respetando los principios fundacionales de Malāk.
- [ ] El proyecto puede continuar evolucionando sin refactorizar el Kernel.
- [ ] La implementación quedó preparada para el siguiente Sprint.

---

# Regla Fundamental

Si cualquiera de los puntos anteriores falla:

La implementación NO debe considerarse terminada.

Primero se corrige.

Después se certifica.

Finalmente se continúa con el siguiente Sprint.