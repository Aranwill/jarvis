# Knowledge Model

Versión: 0.6.0-alpha

Estado: Activo

ID: DOC-ARQ-001

---

# Objetivo

Este documento define el modelo oficial de representación del conocimiento dentro de Malāk.

No describe una implementación concreta.

Define el contrato conceptual que deberán respetar todos los documentos, decisiones arquitectónicas, capacidades, modelos de conocimiento y futuras implementaciones de RAG y GraphRAG.

---

# Principios

El conocimiento dentro de Malāk deberá ser:

- Identificable
- Trazable
- Auditable
- Versionable
- Relacionable
- Independiente del formato físico
- Independiente de la tecnología utilizada para indexarlo

Todo conocimiento deberá poder evolucionar sin perder su historia.

---

# Identidad de los documentos

Todo documento del proyecto posee una identidad única.

El nombre del archivo no representa la identidad.

La identidad se representa mediante un identificador estable.

Ejemplos:

- DOC-ARQ-001
- ADR-001
- GOV-001
- CAP-001
- KER-001

Los identificadores nunca deberán reutilizarse.

---

# Metadatos obligatorios

Todo documento deberá incorporar metadatos estructurados.

Los metadatos constituyen la fuente oficial para:

- auditoría
- trazabilidad
- RAG
- GraphRAG
- futuras bases de conocimiento

El formato oficial será YAML Front Matter.

---

# Relaciones

Todo documento podrá declarar relaciones explícitas.

Ejemplos:

- related
- affects
- depends_on
- supersedes
- superseded_by
- references
- implements
- implemented_by

Las relaciones representan conocimiento estructurado.

No deberán inferirse únicamente desde el texto.

---

# Taxonomía

Los documentos deberán clasificarse mediante una taxonomía estable.

Ejemplos:

- Architecture
- Governance
- Capability
- Kernel
- Runtime
- Development
- Decision
- Security
- Vision

La taxonomía podrá evolucionar preservando compatibilidad histórica.

---

# Compatibilidad con RAG

Los documentos deberán poder indexarse completamente mediante motores RAG tradicionales.

La representación textual deberá permanecer autosuficiente.

---

# Compatibilidad con GraphRAG

Todo documento deberá poder convertirse en uno o más nodos dentro de un grafo de conocimiento.

Las relaciones explícitas deberán convertirse en aristas.

Los identificadores deberán transformarse en nodos persistentes.

El modelo de conocimiento nunca dependerá de una tecnología específica de GraphRAG.

---

# Evolución

El modelo de conocimiento deberá evolucionar mediante decisiones arquitectónicas registradas (ADR).

Toda modificación relevante deberá preservar:

- compatibilidad histórica
- trazabilidad
- gobernanza
- consistencia del conocimiento

Ninguna implementación futura podrá violar los principios definidos en este documento sin una ADR aprobada.

Las relaciones entre documentos y sus implementaciones deberán preservarse de forma explícita para permitir la evolución futura del Architecture Knowledge System (AKS) hacia un grafo de conocimiento navegable y auditable.