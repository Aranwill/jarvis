\# Malāk Repository Standard



Versión: 1.0  

Estado: Activo  

Sprint: Sprint 2A.1 — Repository Refactoring



\---



\# Objetivo



Este documento define la organización física oficial del repositorio Malāk. La estructura aquí definida implementa la arquitectura lógica establecida por el Blueprint y no la reemplaza.



Su propósito es asegurar que la estructura física del proyecto refleje la arquitectura lógica definida en el Blueprint, el Kernel, la Constitución Cognitiva y la Constitución de Gobernanza.



\---



\# Principios



\- Kernel First.

\- Capability First.

\- Human in Control.

\- Model Agnostic.

\- Zero Trust.

\- Event Driven.

\- Separación estricta entre Memory y Knowledge.

\- Separación estricta entre código, configuración, datos y documentación.



\---



\# Estructura Oficial



La siguiente estructura representa las rutas raíz trackeadas del baseline vigente. La ausencia de una ruta en este árbol significa que no forma parte de la estructura física actual; su incorporación futura deberá tratarse como un cambio explícito del repositorio.



```text

Malāk/

├── .github/

├── configs/

├── docs/

├── documents/

├── examples/

├── scripts/

├── src/

├── tests/

├── .gitignore

├── AGENTS.md

├── CHANGELOG.md

├── PROJECT.md

├── pyproject.toml

├── README.md

├── ROADMAP.md

└── SECURITY.md

```



`data/` y `docker/` no forman parte del baseline trackeado vigente. Su aparición en versiones históricas de este estándar no constituye una reserva ni una autorización para introducirlas sin una necesidad y revisión explícitas.
