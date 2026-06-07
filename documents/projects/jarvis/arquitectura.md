# Arquitectura Operativa Actual

**Versión:** v0.4.1

**Estado:** Operativa

**Última actualización:** 2026-06-07

---

# Objetivo

Definir la arquitectura operativa actual de Jarvis, describiendo el flujo de consulta, componentes activos, componentes pendientes y la gestión de modelos dentro del proyecto.

---

## Flujo de Consulta

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

Descripción:

1. El usuario realiza una consulta desde Open WebUI.
2. Open WebUI consulta la colección documental Jarvis.
3. El sistema recupera contexto relevante mediante RAG.
4. El contexto recuperado se envía al modelo conversacional activo.
5. El modelo genera la respuesta final.

---

## Flujo de Indexación Documental

```text
Documento
↓
Open WebUI
↓
Chunking
↓
Modelo de Embeddings
↓
Vectorización
↓
Colección de Conocimiento Jarvis
```

Descripción:

1. Los documentos son cargados a la colección Jarvis.
2. Open WebUI divide los documentos en fragmentos (chunks).
3. El modelo de embeddings genera representaciones vectoriales.
4. Los vectores se almacenan en la base de conocimiento.
5. Posteriormente pueden recuperarse mediante RAG.

---

## Componentes Activos

### Infraestructura

* Docker Desktop
* Ollama
* Open WebUI

### Conocimiento

* Colección de Conocimiento Jarvis
* Recuperación RAG
* Memoria vectorial integrada en Open WebUI

### Modelos

* Modelos locales gestionados mediante Ollama
* Modelo conversacional activo
* Modelo de embeddings activo

### Gestión

* Git local
* Backups automáticos
* Documentación estructurada

---

## Modelos

Jarvis separa dos conceptos:

### 1. Modelos Instalados

Los modelos instalados se documentan automáticamente en:

```text
documents/projects/jarvis/models.md
```

Este archivo refleja el estado real de Ollama y puede cambiar durante la fase de laboratorio.

---

### 2. Modelos Asignados por Rol

Los modelos asignados por rol se definen en:

```text
configs/models.yaml
```

Roles previstos:

* General
* Programación
* Embeddings
* Respaldo
* Experimental

---

### Política

Los documentos de arquitectura no deben contener listas rígidas de modelos.

Objetivos:

* Evitar inconsistencias documentales.
* Permitir pruebas de modelos sin modificar múltiples documentos.
* Mantener una única fuente de verdad para modelos instalados.
* Facilitar futuras automatizaciones.

---

## Componentes Pendientes

### Memoria

* ChromaDB dedicado externo
* Separación de memorias especializadas
* Sincronización documental avanzada

### Automatización

* n8n
* Workflows automatizados
* Integración con agentes

### Voz

* Whisper
* Piper

### Agentes

* Planner Agent
* Coder Agent
* Validator Agent
* Memory Agent

---

## Arquitectura Objetivo

```text
Usuario
↓
Planner Agent
↓
RAG Local
↓
¿Existe información suficiente?
↓
SI
↓
Respuesta

NO
↓
Web Agent
↓
Consulta Internet
↓
Validación de Fuentes
↓
Validator Agent
↓
Respuesta
```

---

## Principios de Diseño

### Local First

Jarvis prioriza ejecución local siempre que sea posible.

---

### RAG Primero

La documentación propia tiene prioridad sobre fuentes externas.

```text
RAG Local
↓
Internet
```

---

### Modularidad

Cada componente debe poder evolucionar independientemente:

* Modelos
* Memoria
* Automatizaciones
* Voz
* Agentes

---

### Escalabilidad

La arquitectura debe permitir:

* Cambiar modelos sin rediseñar el sistema.
* Agregar agentes especializados.
* Incorporar nuevas fuentes de conocimiento.
* Integrar herramientas externas de forma controlada.

---

## Estado Actual

Estado general:

```text
Operativo
```

Componentes validados:

* Ollama
* Open WebUI
* Docker Desktop
* Git
* Backups automáticos
* RAG funcional
* Documentación estructurada

Jarvis se encuentra actualmente en fase de consolidación documental y preparación para memoria avanzada, seguridad IA y futuras automatizaciones.
