\# Security Policy
Versión: 1.0
Estado: Activo
\---

\# Principio
Jarvis adopta una arquitectura \*\*Zero Trust\*\*.
Ningún componente debe asumir confianza implícita sobre otro componente.
Toda interacción deberá ser validada explícitamente.
\---

\# Objetivos

\- Minimizar la superficie de ataque.
\- Reducir privilegios.
\- Aislar capacidades.
\- Registrar eventos relevantes.
\- Facilitar auditorías.

\---

\# Principios de Seguridad

\## Least Privilege

Cada Capability solo podrá acceder a los recursos estrictamente necesarios.

\---

\## Explicit Validation

Toda entrada deberá validarse antes de ser utilizada.

\---

\## Capability Isolation

Las capacidades deberán ser independientes y no compartir estado interno.

\---
\## Auditability

Las decisiones relevantes deberán quedar registradas para permitir auditorías posteriores.

\---
\## Human in Control

Las acciones críticas requerirán validación humana.

\---
\# Reporte de vulnerabilidades

Actualmente el proyecto se encuentra en fase Alpha.
Las vulnerabilidades deberán documentarse mediante GitHub Issues y corregirse antes de cada Release estable.

