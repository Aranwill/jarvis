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

```text
Python 3.12.10
```

---

# Entorno Virtual

El proyecto utiliza un entorno virtual dedicado.

Ubicación:

```text
.venv/
```

Su utilización es obligatoria para ejecutar:

- Runtime
- CLI
- Tests
- Herramientas de desarrollo

Activación en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Validación del intérprete activo:

```powershell
python -c "import sys; print(sys.executable)"
```

La salida debe apuntar al entorno virtual del repositorio:

```text
D:\ollama\jarvis\.venv\Scripts\python.exe
```

No deben instalarse dependencias del proyecto de forma improvisada en el intérprete global de Python.

---

# Instalación editable

Desde la raíz del repositorio y con el entorno virtual activado:

```powershell
python -m pip install -e .
```

La instalación editable permite ejecutar el paquete sin configurar `PYTHONPATH`.

---

# Herramientas oficiales

Actualmente:

- Python
- pip
- pytest
- Ollama, requerido únicamente para validaciones reales con `OllamaRuntime`

Las futuras herramientas deberán documentarse aquí antes de incorporarse al baseline del proyecto.

---

# Ejecución de la CLI de desarrollo

La interfaz iniciada en el Sprint 7.0 es una CLI técnica de validación del subsistema conversacional.

No representa el pipeline cognitivo completo de Malāk y no modifica el Kernel.

La ejecución estable se realiza mediante:

```powershell
python -m malak.app.cli
```

La CLI admite dos runtimes:

```text
MockLLMRuntime
OllamaRuntime
```

La selección se realiza mediante configuración externa interpretada en la frontera de aplicación.

---

# Ejecución con MockLLMRuntime

`MockLLMRuntime` es el modo predeterminado.

No requiere variables de entorno ni servicios externos:

```powershell
python -m malak.app.cli
```

El comando:

```text
status
```

debe mostrar:

```text
Estado: operativo | Provider: mock | Runtime: MockLLMRuntime
```

---

# Ejecución con OllamaRuntime

## Requisitos

- Ollama instalado.
- Servicio local de Ollama activo.
- Al menos un modelo local disponible.
- Entorno virtual de Malāk activado.
- Instalación editable vigente.

Verificación de modelos:

```powershell
ollama list
```

Verificación del servicio HTTP:

```powershell
Invoke-RestMethod http://localhost:11434/api/tags
```

## Variables de entorno

### Runtime

```powershell
$env:MALAK_RUNTIME = "ollama"
```

### Modelo

```powershell
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
```

El nombre debe coincidir con un modelo disponible en:

```powershell
ollama list
```

### URL base

```powershell
$env:MALAK_OLLAMA_BASE_URL = "http://localhost:11434"
```

La URL base predeterminada es:

```text
http://localhost:11434
```

## Inicio de la CLI

```powershell
python -m malak.app.cli
```

El comando:

```text
status
```

debe mostrar:

```text
Estado: operativo | Provider: ollama | Runtime: OllamaRuntime
```

Las variables configuradas mediante `$env:` se aplican únicamente a la sesión actual de PowerShell.

No deben incorporarse secretos, prompts sensibles ni información privada en scripts versionados o documentación de pruebas.

---

# Configuración admitida

| Variable | Obligatoria | Valor predeterminado |
|---|---:|---|
| `MALAK_RUNTIME` | No | `mock` |
| `MALAK_OLLAMA_MODEL` | Sí, cuando el runtime es `ollama` | Sin valor |
| `MALAK_OLLAMA_BASE_URL` | No | `http://localhost:11434` |

Valores admitidos para `MALAK_RUNTIME`:

```text
mock
ollama
```

Un runtime desconocido debe ser rechazado de forma controlada.

---

# Ejecución de Tests

Desde el entorno virtual:

```powershell
python -m pytest -q
```

Todos los tests deben finalizar exitosamente antes de cerrar un sprint.

Las pruebas automatizadas de la CLI y de `OllamaRuntime` no deben requerir obligatoriamente un servicio Ollama activo. Las llamadas HTTP deben sustituirse o controlarse en las pruebas deterministas.

La conexión real con Ollama se valida mediante una prueba manual separada y documentada.

Validación adicional de compilación:

```powershell
python -m compileall src tests
```

Validación del diff:

```powershell
git diff --check
```

---

# Validación manual de OllamaRuntime

Secuencia reproducible:

```powershell
ollama list
Invoke-RestMethod http://localhost:11434/api/tags

$env:MALAK_RUNTIME = "ollama"
$env:MALAK_OLLAMA_MODEL = "qwen3.5:9b"
$env:MALAK_OLLAMA_BASE_URL = "http://localhost:11434"

python -m malak.app.cli
```

Dentro de la CLI:

```text
status
```

Después, enviar un prompt breve y no sensible, comprobar que se recibe una respuesta y finalizar mediante:

```text
exit
```

---

# Principios

El entorno de desarrollo debe ser:

- reproducible;
- simple;
- documentado;
- independiente del equipo utilizado;
- explícito respecto de dependencias ambientales;
- seguro para pruebas locales;
- desacoplado del Kernel.

No se permitirá depender de configuraciones locales no documentadas.

La selección del runtime no debe trasladarse al Kernel ni a los contratos conversacionales centrales.

---

# Metodología de ingeniería

La metodología oficial de ingeniería aplicable al desarrollo de Malāk se define en:

```text
docs/development/engineering_method.md
```

Esta metodología incorpora, según el alcance y el riesgo del cambio:

- Specification-Driven Development (SDD).
- Test-Driven Development (TDD).
- revisión proporcional al riesgo mediante los lentes 4R.
- Bounded Correction y Correction Budget.
- validación independiente de correcciones.
- evidencia verificable ligada al candidato cuando corresponda.

Estas prácticas no modifican el Runtime ni el Kernel y no constituyen una fuente de autoridad superior a la arquitectura o gobernanza del proyecto.

OpenSpec, Gentle AI y otras herramientas externas relacionadas con SDD, TDD, 4R o Receipt-Driven Development no forman parte del baseline oficial mientras no sean evaluadas, aprobadas y documentadas explícitamente.

Receipt-Driven Development permanece en observación como línea prometedora para futuras capacidades multiagente, especialmente en relación con candidate identity, receipts, revisión independiente y trazabilidad verificable.


---

# Mantenimiento

Toda modificación del entorno deberá actualizar este documento antes de incorporarse al proyecto.