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

# Ejecución de la CLI de desarrollo

La interfaz disponible en el Sprint 7.0 es una CLI técnica de validación del subsistema conversacional.

No representa el pipeline cognitivo completo de Malāk y utiliza actualmente `MockLLMRuntime`.

Desde la raíz del repositorio, con el entorno virtual activado:

```powershell
python -m pip install -e .
python -m malak.app.cli

---

# Ejecución de Tests

Desde el entorno virtual:

```powershell
python -m pytest -v
```

Todos los tests deben finalizar exitosamente antes de cerrar un Sprint.

Validación adicional de compilación:

```powershell
python -m compileall src tests

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