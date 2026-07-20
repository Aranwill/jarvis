# Estado Actual del Proyecto Jarvis

> **Documento histórico legacy.**
> Este archivo describe el estado de Jarvis v0.4.1 y no representa el estado actual de Malāk.
> No posee autoridad normativa, operativa ni de planificación.
**Versión:** v0.4.1
**Estado:** Operativo / Estable local
**Última actualización:** 2026-06-07
**Ruta principal del proyecto:** `D:\Ollama\jarvis`

---

# 1. Objetivo del Proyecto

Jarvis es un asistente personal local diseñado para ejecutarse en infraestructura propia, con foco en:

* Privacidad.
* Ejecución local de modelos LLM.
* Memoria documental.
* Recuperación de conocimiento mediante RAG.
* Asistencia técnica y programación.
* Automatizaciones futuras con n8n.
* Arquitectura modular basada en agentes.
* Posible integración futura de voz.
* Operación local-first.

---

# 2. Estado General

Jarvis se encuentra actualmente en estado:

```text
Operativo / Estable local
```

La instalación base ya fue validada con:

* Ollama.
* Docker Desktop.
* Open WebUI.
* RAG funcional.
* ChromaDB integrado en Open WebUI.
* Git local.
* Backups automáticos.
* Documentación estructurada.

El proyecto se encuentra en fase de consolidación documental y preparación para:

* Seguridad IA.
* Automatización.
* Memoria avanzada.
* Agentes especializados.
* Integración futura de voz.

---

# 3. Hardware Actual

## Equipo Principal

* CPU: Intel Core i7-11700K
* GPU: NVIDIA RTX 2060 12GB
* RAM: 16GB DDR4 3200MHz
* Objetivo futuro: 32GB DDR4
* Motherboard: ASUS TUF Gaming Z590
* Almacenamiento:

  * 500GB M.2 SSD
  * 240GB SATA SSD
  * 1TB SSD
* Cooling: Cooler Master 240mm AIO
* PSU: Redragon 600W 80+ Bronze

---

# 4. Estructura Actual del Proyecto

Ruta principal:

```text
D:\Ollama\jarvis
```

Estructura actual:

```text
jarvis
├── agents
├── backups
├── configs
├── documents
├── logs
├── memory
├── models
├── scripts
├── workflows
├── .gitignore
└── README.md
```

## Descripción de carpetas

### agents

Contendrá agentes especializados futuros:

* Planner Agent
* Coder Agent
* Validator Agent
* Memory Agent

### backups

Contiene respaldos automáticos del proyecto.

### configs

Contiene archivos de configuración del proyecto.

Archivos relevantes:

```text
configs/models.yaml
```

### documents

Contiene documentación, notas, PDFs y archivos de conocimiento del proyecto.

Ruta principal de documentación Jarvis:

```text
documents/projects/jarvis
```

### logs

Contiene registros operativos.

### memory

Contiene datos relacionados con memoria local, sesiones, embeddings o vectorización cuando corresponda.

### models

Contiene estructura local de modelos de Ollama.

Subcarpetas principales:

```text
models/blobs
models/manifests
```

La carpeta `blobs` contiene archivos pesados de modelos y no debe versionarse.

### scripts

Contiene scripts de operación.

Scripts principales:

```text
iniciar-jarvis.ps1
cerrar-jarvis.ps1
backup-jarvis.ps1
update-models.ps1
```

### workflows

Contendrá workflows futuros de n8n.

---

# 5. Componentes Operativos

## Ollama

Motor local para ejecutar modelos LLM.

Estado:

```text
Operativo
```

Uso actual:

* Ejecución local de modelos.
* Gestión de modelos instalados.
* Integración con Open WebUI.

---

## Docker Desktop

Utilizado para ejecutar servicios auxiliares.

Estado:

```text
Operativo
```

Uso actual:

* Ejecución de Open WebUI mediante contenedor.
* Base para futuras integraciones con servicios auxiliares.

---

## Open WebUI

Interfaz principal de Jarvis.

URL local:

```text
http://localhost:3000
```

Estado:

```text
Operativo
```

Funciones actuales:

* Chat local.
* Selección de modelos.
* Historial de conversaciones.
* Gestión de conocimiento.
* RAG integrado.
* Uso de colecciones documentales.

---

## ChromaDB Integrado

Jarvis utiliza actualmente la memoria vectorial integrada en Open WebUI.

Estado:

```text
Operativo
```

Nota:

ChromaDB dedicado externo se mantiene como componente pendiente para fases futuras.

---

## Git

Control de versiones local.

Estado:

```text
Operativo
```

Validaciones actuales:

* Repositorio local inicializado.
* `.gitignore` configurado.
* Tag `v0.4` creado.
* Cambios documentales en curso para v0.4.1.

---

## Backups

Sistema de respaldo automático.

Estado:

```text
Operativo
```

Uso actual:

* Backup automático durante el cierre.
* Respaldo de documentación.
* Respaldo de memoria/vector DB cuando corresponda.

---

# 6. Modelos

Jarvis separa dos conceptos:

1. Modelos instalados en Ollama.
2. Modelos asignados por rol operativo.

## Modelos instalados

Los modelos instalados se documentan automáticamente en:

```text
documents/projects/jarvis/models.md
```

Este archivo debe generarse mediante:

```powershell
.\scripts\update-models.ps1
```

## Modelos asignados por rol

La asignación de modelos por rol se define en:

```text
configs/models.yaml
```

Roles previstos:

* General
* Programación
* Embeddings
* Respaldo rápido
* Experimental

## Política

Este documento no debe contener listas rígidas de modelos instalados.

Motivo:

* Los modelos pueden cambiar durante la fase de laboratorio.
* Se evita duplicación de información.
* Se evita contradicción entre documentación y estado real de Ollama.
* `models.md` funciona como fuente actualizada de modelos instalados.
* `models.yaml` funciona como fuente de asignación por rol.

---

# 7. Base de Conocimiento

Colección actual en Open WebUI:

```text
Jarvis
```

Estado:

```text
Funcional
```

Documentación principal del proyecto:

```text
D:\Ollama\jarvis\documents\projects\jarvis
```

Archivos relevantes:

```text
proyecto_jarvis_base.md
arquitectura.md
roadmap.md
decisiones.md
changelog.md
setup.md
estado_actual.md
security.md
models.md
```

Notas:

* La calidad del RAG depende directamente de la claridad documental.
* Cada cambio importante en documentación debe reindexarse o volver a cargarse en Open WebUI.
* `estado_actual.md` debe responder al estado operativo actual.
* `arquitectura.md` debe describir el diseño del sistema.
* `roadmap.md` debe contener fases futuras.
* `decisiones.md` debe registrar decisiones aceptadas.
* `changelog.md` debe registrar cambios históricos.
* `models.md` debe documentar modelos instalados.
* `security.md` debe definir políticas de seguridad IA.

---

# 8. RAG Actual

El sistema ya puede responder usando documentación propia.

Flujo operativo resumido:

```text
Usuario
↓
Open WebUI
↓
Colección Jarvis
↓
Recuperación RAG
↓
Modelo Conversacional Activo
↓
Respuesta
```

Estado:

```text
Funcional
```

Validaciones realizadas:

* Open WebUI recupera fuentes desde documentos cargados.
* Jarvis responde sobre hardware, objetivos, roadmap y arquitectura.
* La calidad mejora cuando los documentos son explícitos y actualizados.

Limitación actual:

* El RAG puede quedar desactualizado si se modifican documentos locales pero no se actualiza la colección en Open WebUI.

Acción recomendada:

* Reindexar o reemplazar documentos en la colección Jarvis después de cambios relevantes.

---

# 9. Arquitectura Operativa

La arquitectura operativa completa se documenta en:

```text
documents/projects/jarvis/arquitectura.md
```

Resumen actual:

```text
Usuario
↓
Open WebUI
↓
Colección de Conocimiento Jarvis
↓
Recuperación RAG
↓
Modelo Conversacional Activo
↓
Respuesta
```

Componentes activos:

* Docker Desktop
* Ollama
* Open WebUI
* Colección de Conocimiento Jarvis
* RAG integrado
* Modelos locales
* Git local
* Backups automáticos

Componentes pendientes:

* ChromaDB dedicado externo
* n8n
* Whisper
* Piper
* Planner Agent
* Coder Agent
* Validator Agent
* Memory Agent

---

# 10. Scripts de Inicio, Cierre y Mantenimiento

Ubicación:

```text
D:\Ollama\jarvis\scripts
```

Scripts principales:

```text
iniciar-jarvis.ps1
cerrar-jarvis.ps1
backup-jarvis.ps1
update-models.ps1
```

## iniciar-jarvis.ps1

Función:

* Abrir Docker Desktop.
* Esperar disponibilidad de Docker.
* Iniciar contenedor de Open WebUI.
* Abrir navegador en `http://localhost:3000`.

Comando:

```powershell
cd D:\Ollama\jarvis\scripts
.\iniciar-jarvis.ps1
```

---

## cerrar-jarvis.ps1

Función:

* Detener modelos cargados en Ollama.
* Detener Open WebUI.
* Ejecutar backup cuando corresponda.
* Verificar estado de Ollama.
* Verificar estado de Docker.
* Liberar recursos.

Comando:

```powershell
cd D:\Ollama\jarvis\scripts
.\cerrar-jarvis.ps1
```

Validación posterior:

```powershell
ollama ps
docker ps
```

---

## backup-jarvis.ps1

Función:

* Respaldar documentación.
* Respaldar memoria/vector DB cuando corresponda.
* Crear respaldo operativo del estado actual del proyecto.

---

## update-models.ps1

Función:

* Ejecutar `ollama list`.
* Generar `documents/projects/jarvis/models.md`.
* Mantener la documentación de modelos sincronizada con Ollama.

Comando recomendado:

```powershell
cd D:\Ollama\jarvis
powershell -ExecutionPolicy Bypass -File .\scripts\update-models.ps1
```

---

# 11. Estado de Implementación

## Completado

* Instalación de Ollama.
* Instalación de Docker Desktop.
* Instalación de Open WebUI.
* Integración Open WebUI con Ollama.
* Descarga y prueba de modelos locales.
* Creación de estructura del proyecto.
* Creación de base de conocimiento Jarvis.
* Primera prueba RAG funcional.
* Scripts de inicio y cierre.
* Script de backup.
* Git local.
* Tag v0.4.
* ChromaDB integrado en Open WebUI.
* Documentación base del proyecto.
* Separación documental entre arquitectura, estado, roadmap, decisiones y changelog.

---

## En curso

* Consolidación documental v0.4.1.
* Creación y uso de `manifest.yaml`.
* Creación y uso de `configs/models.yaml`.
* Generación automática de `models.md`.
* Limpieza de modelos hardcodeados en documentación.
* Preparación de `security.md`.
* Mejora de scripts para evitar dependencias rígidas de modelos concretos.

---

## Pendiente

* Validación completa de v0.4.1.
* Reindexado de documentos actualizados en Open WebUI.
* Implementación completa de fase de seguridad IA.
* ChromaDB dedicado externo.
* Automatizaciones con n8n.
* Integración de voz con Whisper y Piper.
* Implementación real de agentes.
* Pruebas de recuperación documental más amplias.
* Definición de métricas de calidad para RAG.

---

# 12. Problemas o Limitaciones Detectadas

## Documentación desincronizada

Estado:

```text
En corrección
```

Problema:

Algunos documentos mantenían listas rígidas de modelos, versiones o componentes.

Acción:

* Separar modelos instalados en `models.md`.
* Separar roles de modelos en `configs/models.yaml`.
* Mantener arquitectura sin nombres rígidos de modelos.
* Mantener `estado_actual.md` como estado operativo, no como inventario duplicado.

---

## Modelos en fase de laboratorio

Estado:

```text
Esperado
```

Problema:

Los modelos instalados cambian frecuentemente durante pruebas.

Acción:

* No registrar modelos manualmente en múltiples documentos.
* Generar `models.md` desde `ollama list`.
* Registrar asignación por rol en `configs/models.yaml`.

---

## RAG depende de la calidad documental

Estado:

```text
Vigente
```

Observación:

Cuando los documentos son vagos o contradictorios, el modelo puede responder con generalidades o recuperar información vieja.

Acción:

* Mantener documentos claros.
* Usar fuentes únicas.
* Reindexar documentos después de cambios.
* Evitar duplicación innecesaria entre archivos.

---

## ChromaDB dedicado externo pendiente

Estado:

```text
Pendiente
```

Observación:

La fase actual utiliza ChromaDB integrado en Open WebUI.

Acción:

* Mantener ChromaDB integrado durante v0.4.1.
* Evaluar ChromaDB dedicado en fase de memoria avanzada.

---

## Seguridad IA pendiente

Estado:

```text
Pendiente
```

Observación:

Antes de habilitar agentes, navegación web o automatizaciones avanzadas, se debe definir una política de seguridad.

Acción:

* Crear y mantener `security.md`.
* Incorporar controles contra prompt injection.
* Incorporar política SSRF.
* Priorizar RAG local.
* Tratar contenido externo como datos, no instrucciones.

---

# 13. Roadmap Referenciado

El roadmap completo se mantiene en:

```text
documents/projects/jarvis/roadmap.md
```

Resumen actual:

## Fase 1 - Base Local

Estado:

```text
Completada
```

Incluye:

* Ollama
* Docker Desktop
* Open WebUI
* Modelos locales
* Base documental
* Primer RAG
* Scripts operativos

---

## Fase 2 - Documentación y Memoria

Estado:

```text
En curso
```

Incluye:

* Consolidación documental
* Fuente de verdad del proyecto
* Limpieza de inconsistencias
* Reindexado de conocimiento

---

## Fase 3 - Memoria Avanzada

Estado:

```text
Pendiente
```

Incluye:

* ChromaDB dedicado externo
* Sincronización documental
* Mejoras RAG
* Separación de memorias

---

## Fase 3.5 - Seguridad IA

Estado:

```text
Pendiente
```

Incluye:

* security.md
* OWASP LLM Top 10
* Prompt Injection
* SSRF
* Auditoría documental
* Política de fuentes

---

## Fase 4 - Automatización

Estado:

```text
Pendiente
```

Incluye:

* n8n
* Workflows locales
* Automatizaciones controladas

---

## Fase 5 - Voz

Estado:

```text
Pendiente
```

Incluye:

* Whisper
* Piper

---

## Fase 6 - Agentes

Estado:

```text
Pendiente
```

Incluye:

* Planner Agent
* Coder Agent
* Validator Agent
* Memory Agent

---

# 14. Configuración Recomendada Actual

Jarvis ya no mantiene una lista rígida de modelos recomendados en este documento.

La configuración operativa se divide así:

## Modelos instalados

```text
documents/projects/jarvis/models.md
```

## Modelos por rol

```text
configs/models.yaml
```

## Arquitectura

```text
documents/projects/jarvis/arquitectura.md
```

## Seguridad

```text
documents/projects/jarvis/security.md
```

## Roadmap

```text
documents/projects/jarvis/roadmap.md
```

---

# 15. Procedimiento de Actualización Documental

Cuando se modifique documentación del proyecto:

1. Actualizar el archivo correspondiente.
2. Ejecutar actualización de modelos si cambió Ollama:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\update-models.ps1
```

3. Revisar cambios con Git:

```powershell
git status
git diff
```

4. Hacer commit si los cambios son correctos:

```powershell
git add .
git commit -m "Actualiza documentacion Jarvis"
```

5. Reindexar o reemplazar documentos en Open WebUI.
6. Validar con una consulta RAG:

```text
#Jarvis
¿Cuál es el estado actual del proyecto Jarvis?
```

---

# 16. Próximo Paso Recomendado

Validar v0.4.1 con el siguiente checklist:

```text
[ ] manifest.yaml creado
[ ] configs/models.yaml creado
[ ] models.md generado desde Ollama
[ ] arquitectura.md actualizado
[ ] estado_actual.md actualizado
[ ] security.md creado
[ ] scripts revisados
[ ] iniciar-jarvis.ps1 probado
[ ] cerrar-jarvis.ps1 probado
[ ] backup-jarvis.ps1 probado
[ ] documentos reindexados en Open WebUI
[ ] consulta RAG validada
[ ] git status limpio
```

Si todo pasa, crear tag:

```powershell
git tag v0.4.1
```

---

# 17. Resumen Ejecutivo

Jarvis v0.4.1 es una consolidación de la versión local funcional.

El proyecto ya cuenta con:

* Ejecución local mediante Ollama.
* Interfaz Open WebUI.
* RAG funcional.
* Colección documental Jarvis.
* Git local.
* Backups automáticos.
* Estructura modular.
* Separación entre arquitectura, estado, roadmap, decisiones y changelog.

La mejora principal de v0.4.1 es la gobernanza documental:

* `estado_actual.md` describe el estado operativo.
* `arquitectura.md` describe el diseño.
* `models.md` documenta modelos instalados.
* `configs/models.yaml` define modelos por rol.
* `manifest.yaml` coordina rutas y fuentes del proyecto.
* `security.md` prepara la fase de seguridad IA.

Jarvis está listo para continuar con seguridad IA, automatización controlada, memoria avanzada y agentes especializados.


---

# Baseline Arquitectónica

Fecha: 2026-06-28  
Versión: Jarvis v0.5.0-alpha  
Sprint: Sprint 1B cerrado / Sprint 2 iniciado  
Estado: Arquitectura base congelada

## Documentos congelados

- blueprint.md
- kernel.md

## Regla de cambio

A partir de esta baseline, los documentos `blueprint.md` y `kernel.md` no deberán modificarse directamente para decisiones nuevas de arquitectura.

Todo cambio arquitectónico deberá registrarse primero en `decisiones.md` como ADR.

## Objetivo de la siguiente fase

Iniciar Sprint 2 — Foundation Implementation.

El objetivo será implementar el primer Kernel funcional mínimo:

- arranque del sistema
- registro de módulos stub
- healthcheck
- Event Bus básico
- Capability mínima
- respuesta controlada de prueba

## Restricciones

No se implementará todavía:

- IA
- RAG
- memoria real
- ChromaDB
- SQL Server
- agentes autónomos
- automatizaciones externas

