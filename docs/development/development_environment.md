# Development Environment

Versión: 0.6.0-alpha

Estado: Activo

---

# Objetivo

Este documento define el entorno oficial de desarrollo de Malāk.

Todo desarrollador deberá utilizar este entorno para garantizar que el Runtime, las pruebas y la arquitectura permanezcan reproducibles.

---

# Versión Oficial de Python

Python 3.12.x

Actualmente validado con:

Python 3.12.10

---

# Entorno Virtual

El proyecto utiliza un entorno virtual dedicado.

Ubicación:

.venv/

Su utilización es obligatoria para ejecutar:

- Runtime
- Tests
- Herramientas de desarrollo

---

# Herramientas oficiales

Actualmente:

- Python
- pip
- pytest

Las futuras herramientas deberán documentarse aquí antes de incorporarse al proyecto.

---

# Ejecución del Runtime

Actualmente:

```powershell
python src/app/main.py
```

En el futuro el Launcher oficial podrá evolucionar, pero deberá permanecer documentado aquí.

---

# Ejecución de Tests

Desde el entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Todos los tests deben finalizar exitosamente antes de cerrar un Sprint.

---

# Principios

El entorno de desarrollo debe ser:

- reproducible
- simple
- documentado
- independiente del equipo utilizado

No se permitirá depender de configuraciones locales no documentadas.

---

# Mantenimiento

Toda modificación del entorno deberá actualizar este documento antes de incorporarse al proyecto.