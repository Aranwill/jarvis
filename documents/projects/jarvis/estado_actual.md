# Estado Actual del Proyecto Jarvis

**Versión:** v0.3  
**Estado:** Operativo / Primera versión funcional local  
**Última actualización:** 2026-05-30  
**Ruta principal del proyecto:** `D:\Ollama`

---

# 1. Objetivo del Proyecto

Jarvis es un asistente personal local diseñado para ejecutarse en infraestructura propia, con foco en:

- Privacidad.
- Ejecución local de modelos LLM.
- Memoria documental.
- Recuperación de conocimiento mediante RAG.
- Asistencia técnica y programación.
- Automatizaciones futuras con n8n.
- Arquitectura modular basada en agentes.
- Posible integración futura de voz.

---

# 2. Hardware Actual

## Equipo Principal

- CPU: Intel Core i7-11700K
- GPU: NVIDIA RTX 2060 12GB
- RAM: 16GB DDR4 3200MHz
- Objetivo futuro: 32GB DDR4
- Motherboard: ASUS TUF Gaming Z590
- Almacenamiento:
  - 500GB M.2 SSD
  - 240GB SATA SSD
  - 1TB SSD
- Cooling: Cooler Master 240mm AIO
- PSU: Redragon 600W 80+ Bronze

---

# 3. Estructura Actual del Proyecto

```text
D:\Ollama

├── docker
│   └── open-webui
│
├── jarvis
│   ├── agents
│   │   ├── planner
│   │   ├── coder
│   │   ├── validator
│   │   └── memory
│   │
│   ├── memory
│   │   ├── chromadb
│   │   ├── embeddings
│   │   └── sessions
│   │
│   ├── documents
│   │   ├── books
│   │   ├── notes
│   │   ├── pdfs
│   │   └── projects
│   │       └── jarvis
│   │
│   ├── workflows
│   │   └── n8n
│   │
│   ├── models
│   ├── configs
│   ├── logs
│   ├── scripts
│   └── backups
│
└── temp
```

---

# 4. Componentes Instalados y Operativos

## Ollama

Motor local para ejecutar modelos LLM.

Estado:

- Instalado.
- Operativo.
- Detecta y ejecuta modelos correctamente.
- Usa GPU cuando el modelo lo permite.

---

## Docker Desktop

Utilizado para ejecutar servicios auxiliares.

Estado:

- Instalado.
- Operativo.
- Docker CLI funcional.
- Open WebUI ejecutándose mediante contenedor.

---

## Open WebUI

Interfaz principal de Jarvis.

URL local:

```text
http://localhost:3000
```

Funciones actuales:

- Chat local.
- Selección de modelos.
- Historial de conversaciones.
- Gestión de conocimiento.
- RAG integrado.
- Uso de colecciones documentales.

Estado:

- Instalado.
- Operativo.
- Conectado correctamente con Ollama.

---

# 5. Modelos Instalados

## Qwen3.5:9B

Rol:

- Modelo principal recomendado para Jarvis.

Uso:

- Conversación general.
- Análisis.
- Arquitectura.
- Planificación.
- Documentación.
- Razonamiento sobre el proyecto.

Notas:

- Mejor calidad que Qwen2.5.
- Puede tardar más en responder.
- Tiene contexto muy alto por defecto.
- Puede utilizar modo thinking/razonamiento.

---

## Qwen2.5:7B

Rol:

- Modelo alternativo / respaldo.

Uso:

- Respuestas rápidas.
- Validación comparativa.
- Conversación general.

Notas:

- Corre 100% en GPU en la RTX 2060.
- Contexto observado: 16384.
- Más rápido que Qwen3.5.

---

## DeepSeek-Coder:6.7B

Rol:

- Modelo especializado en programación.

Uso:

- Python.
- PowerShell.
- Docker.
- Automatizaciones.
- n8n.
- Debugging.
- Scripts del proyecto.

---

## Nomic-Embed-Text

Rol:

- Modelo de embeddings.

Uso:

- RAG.
- Recuperación documental.
- Búsqueda semántica.
- Base de conocimiento.

Notas:

- No se usa para conversar.
- Se usa para convertir documentos en vectores.

---

# 6. Base de Conocimiento

Colección actual en Open WebUI:

```text
Jarvis
```

Estado:

- Creada.
- Funcional.
- Probada mediante consultas RAG.
- Open WebUI recupera fuentes desde los documentos cargados.

Documentos actuales del proyecto:

```text
D:\Ollama\jarvis\documents\projects\jarvis
```

Archivos:

- `proyecto_jarvis_base.md`
- `arquitectura.md`
- `roadmap.md`
- `decisiones.md`
- `changelog.md`
- `setup.md`
- `ideas.md`

Notas:

- `ideas.md` puede mantenerse como placeholder o completarse más adelante.
- Es recomendable mantener actualizados estos archivos y volver a subirlos a la colección Jarvis cuando cambien.

---

# 7. RAG Actual

El sistema ya puede responder usando documentación propia.

Flujo actual:

```text
Usuario
↓
Open WebUI
↓
Colección Jarvis
↓
Recuperación RAG
↓
Modelo LLM
↓
Respuesta
```

Se validó que:

- Open WebUI recupera fuentes.
- Las respuestas citan documentos como `proyecto_jarvis_base.md`.
- El modelo puede responder sobre hardware, objetivos, roadmap y arquitectura.
- La calidad depende directamente de la claridad de los documentos cargados.

---

# 8. Arquitectura Operativa Actual

```text
Usuario
↓
Open WebUI
↓
Colección de Conocimiento Jarvis
↓
Nomic-Embed-Text
↓
Recuperación RAG
↓
Qwen3.5:9B / Qwen2.5:7B
↓
Respuesta
```

Componentes activos:

- Docker Desktop.
- Open WebUI.
- Ollama.
- Qwen3.5:9B.
- Qwen2.5:7B.
- DeepSeek-Coder:6.7B.
- Nomic-Embed-Text.

Componentes pendientes:

- ChromaDB dedicado.
- n8n.
- Whisper.
- Piper.
- Planner Agent.
- Coder Agent.
- Validator Agent.
- Memory Agent.

---

# 9. Scripts de Inicio y Cierre

Ubicación:

```text
D:\Ollama\jarvis\scripts
```

Archivos:

- `iniciar-jarvis.ps1`
- `cerrar-jarvis.ps1`

## iniciar-jarvis.ps1

Función:

- Abre Docker Desktop.
- Espera la inicialización.
- Inicia el contenedor `open-webui`.
- Abre `http://localhost:3000`.

Comando:

```powershell
cd D:\Ollama\jarvis\scripts
.\iniciar-jarvis.ps1
```

## cerrar-jarvis.ps1

Función:

- Detiene modelos cargados en Ollama.
- Detiene el contenedor `open-webui`.
- Verifica estado de Ollama.
- Verifica estado de Docker.
- Libera GPU.

Comando:

```powershell
cd D:\Ollama\jarvis\scripts
.\cerrar-jarvis.ps1
```

Validación de cierre:

```powershell
ollama ps
docker ps
```

Ambos deben quedar vacíos.

---

# 10. Estado de Implementación

## Completado

- Instalación de Ollama.
- Instalación de Docker Desktop.
- Instalación de Open WebUI.
- Integración Open WebUI con Ollama.
- Descarga de modelos principales.
- Creación de estructura del proyecto.
- Creación de base de conocimiento Jarvis.
- Primera prueba RAG funcional.
- Scripts de inicio y cierre.
- Documentación base del proyecto.

---

# 11. Problemas o Limitaciones Detectadas

## Qwen3.5:9B puede ser lento

Causa probable:

- Contexto muy alto por defecto.
- Mayor consumo que Qwen2.5.
- Uso parcial CPU/GPU en ciertas configuraciones.

Acciones recomendadas:

- Usar Qwen2.5 para consultas rápidas.
- Usar Qwen3.5 para análisis más complejos.
- Evaluar ajuste de `num_ctx` en Open WebUI/Ollama.

---

## RAG depende de la calidad documental

Observación:

- Cuando los documentos son vagos, el modelo responde con generalidades.
- Cuando los documentos son explícitos, el modelo responde con mayor precisión.

Acción recomendada:

- Mantener documentos claros y actualizados.
- Agregar `estado_actual.md` como fuente de verdad.
- Reindexar documentos cuando se actualicen.

---

## ChromaDB dedicado aún no implementado

Estado:

- Open WebUI usa su propia gestión interna para conocimiento/RAG.
- ChromaDB dedicado se evaluará más adelante.

---

# 12. Roadmap Actualizado

## Fase 1 - Base Local

Estado: Completada.

Incluye:

- Ollama.
- Docker.
- Open WebUI.
- Modelos locales.
- Base documental.
- Primer RAG.
- Scripts operativos.

---

## Fase 2 - Documentación y Memoria

Estado: En curso.

Objetivos:

- Mejorar documentación.
- Crear y mantener:
  - `estado_actual.md`
  - `decisiones.md`
  - `setup.md`
  - `changelog.md`
  - `arquitectura.md`
  - `roadmap.md`
- Reindexar conocimiento en Open WebUI.

---

## Fase 3 - Memoria Avanzada

Estado: Pendiente.

Evaluar:

- ChromaDB dedicado.
- Sincronización documental.
- Mejoras de RAG.
- Separación de memoria personal, técnica y documental.

---

## Fase 4 - Automatización

Estado: Pendiente.

Tecnología:

- n8n.

Objetivos:

- Workflows locales.
- Automatizaciones.
- Acciones controladas.
- Integración futura con Jarvis.

---

## Fase 5 - Voz

Estado: Pendiente.

Tecnologías:

- Whisper.
- Piper.

Objetivo:

- Entrada por voz.
- Salida por voz.
- Interacción más natural.

---

## Fase 6 - Agentes

Estado: Pendiente.

Agentes previstos:

- Planner Agent.
- Coder Agent.
- Validator Agent.
- Memory Agent.

Objetivo:

- Separar responsabilidades.
- Mejorar modularidad.
- Evitar un chatbot monolítico.

---

# 13. Configuración Recomendada Actual

```text
Jarvis General:
Qwen3.5:9B

Jarvis Rápido / Respaldo:
Qwen2.5:7B

Jarvis Programador:
DeepSeek-Coder:6.7B

Jarvis Memoria / RAG:
Nomic-Embed-Text

Interfaz:
Open WebUI

Motor:
Ollama

Contenedores:
Docker Desktop
```

---

# 14. Próximo Paso Recomendado

Crear o mantener este archivo como:

```text
D:\Ollama\jarvis\documents\projects\jarvis\estado_actual.md
```

Luego:

1. Subirlo a la colección `Jarvis`.
2. Consultar:

```text
#Jarvis

¿Cuál es el estado actual del proyecto?
```

3. Validar que la respuesta cite `estado_actual.md`.
4. Continuar mejorando documentación antes de instalar más componentes.

---

# 15. Resumen Ejecutivo

Jarvis v0.3 ya cuenta con una base local funcional:

- Modelos locales mediante Ollama.
- Interfaz Open WebUI.
- Base de conocimiento propia.
- RAG operativo.
- Estructura de carpetas organizada.
- Scripts de inicio y cierre.
- Documentación inicial.

El proyecto está listo para pasar de instalación técnica a consolidación documental, memoria avanzada y futuras automatizaciones.


# Actualización Estado Actual

## Infraestructura Validada

Fecha: 2026-05-31

### Componentes Operativos

* Ollama
* Docker Desktop
* Open WebUI
* ChromaDB integrado
* RAG funcional

### Gestión

* Git inicializado
* Repositorio local operativo
* Tag v0.4 creado
* .gitignore configurado

### Automatización

* iniciar-jarvis.ps1
* cerrar-jarvis.ps1
* backup-jarvis.ps1

### Backups

* Backup automático ejecutado al cierre
* Respaldo de vector_db
* Respaldo de documents

### Estado General

Jarvis v0.4 validado y operativo.
