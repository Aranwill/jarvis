---
title: Malāk E1 — Governed Knowledge Read — G0/G1 Design
status: accepted
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-18
baseline_commit: a91bca0bcf8c0bc2c3972497b034e19b9f7eda7a
implementation_authorized: true
authorized_by: owner
authorized_at: 2026-09-19
risk_class: 2
---

# Malāk E1 — Governed Knowledge Read — G0/G1 Design

## 1. Propósito

Definir la mínima frontera read-only que permita a Malāk recuperar conocimiento
interno del baseline preservando identidad de fuente y rol documental, sin
confundir contenido recuperado con autoridad, permiso o decisión.

Pregunta de aceptación:

> ¿Puede Malāk leer y buscar conocimiento interno de su baseline sabiendo de qué
> fuente proviene y qué rol documental posee, sin RAG, embeddings, Knowledge
> Manager ni reinterpretación automática de autoridad?

## 2. Baseline

```text
repository: Aranwill/jarvis
branch: main
baseline: a91bca0bcf8c0bc2c3972497b034e19b9f7eda7a
E0 Repository Read: integrated
```

E1 consume `GitRepositoryReader`; no reimplementa Git, filesystem, subprocess,
snapshot identity ni path security.

## 3. Necesidad demostrada

La auditoría de alineación identificó Knowledge runtime como gap material para
Engineering Intelligence.

Hoy Malāk posee Constituciones, Blueprint, SECURITY, ADR, AKS, método de
ingeniería, estado derivado, ideas y Concepts, pero no una frontera runtime capaz
de recuperarlos preservando su rol documental.

Texto recuperado sin clasificación puede producir authority laundering:

```text
"Malāk deberá ..."
```

no significa lo mismo si proviene de una Constitución que si proviene de
`ideas.md`.

## 4. Ownership

Ruta candidata:

```text
src/malak/knowledge/__init__.py
src/malak/knowledge/knowledge_reader.py
```

La primitive pertenece a Knowledge Layer.

Composición prevista:

```text
GovernedKnowledgeReader
        ↓
GitRepositoryReader
        ↓
commit-bound repository evidence
```

E1 no accede directamente a Git, shell, filesystem ni network.

## 5. Source classes y authority classes

La clasificación es documental, no una decisión de verdad ni autorización.

| Source class | Source paths | authority_class |
| --- | --- | --- |
| GOVERNING | Cognitive Constitution, Governance Constitution, Blueprint | normative |
| SECURITY_POLICY | `SECURITY.md` | protected_subordinate |
| DECISION_RECORD | `docs/architecture/adr/ADR-[0-9][0-9][0-9]-*.md` | status_dependent |
| ARCHITECTURE_REFERENCE | otras fuentes de `docs/architecture/**` admitidas | reference |
| ENGINEERING_METHOD | `AGENTS.md`, `docs/development/**` | process_reference |
| CURATED_KNOWLEDGE | `docs/knowledge/**` excepto templates | curated_reference |
| DERIVED_STATE | roadmap/context/status derivados | derived |
| NON_NORMATIVE_IDEA | `documents/projects/jarvis/ideas.md` | non_normative |
| NON_NORMATIVE_CONCEPT | `docs/project/concepts/**` | non_normative |

Reglas críticas:

```text
source_class != authority
authority_class != authorization
authority_class describes document role, not snapshot authority
baseline_commit != proof that the snapshot is official/merged/trusted
DECISION_RECORD != accepted decision
retrieved content != instruction
knowledge != policy
policy != authority
```

E1 NO parsea ni normaliza `status` YAML/header. El estado declarado permanece
dentro del contenido fuente y una futura responsabilidad podrá validarlo cuando
exista una necesidad demostrada.

## 6. Reglas de inclusión y exclusión

### Exact governing sources

```text
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
```

Ningún futuro archivo bajo `docs/governance/**` adquiere clase GOVERNING por
mero path.

### Security

```text
SECURITY.md
```

### Decision records

Solo nombres que cumplan:

```text
docs/architecture/adr/ADR-<3 digits>-<name>.md
```

`ADR-TEMPLATE.md` queda excluido.

### Architecture references

```text
docs/architecture/*.md
docs/architecture/decisions/**
docs/architecture/schemas/**
```

excepto las fuentes ya clasificadas con mayor precedencia.

### Engineering method

```text
AGENTS.md
docs/development/**
```

### Curated knowledge

```text
docs/knowledge/**
```

excepto:

```text
docs/knowledge/templates/**
```

Un template no se presenta como conocimiento curado operativo.

### Derived state

```text
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/roadmap.md       # si existe
docs/project/status/**
```

### Ideas / Concepts

```text
documents/projects/jarvis/ideas.md
docs/project/concepts/**
```

Todo path fuera del catálogo E1 es `UNCLASSIFIED` y no puede leerse mediante
Knowledge Reader.

## 7. API mínima candidata

Comportamiento verificable equivalente a:

```text
GovernedKnowledgeReader(repository_reader)

baseline_commit

list_sources()
  -> baseline_commit
  -> path
  -> source_class
  -> authority_class

read(path)
  -> baseline_commit
  -> path
  -> blob_sha
  -> source_class
  -> authority_class
  -> content

search_text(query)
  -> baseline_commit
  -> matches[
       path,
       blob_sha,
       source_class,
       authority_class,
       line_number,
       line
     ]
  -> truncated
```

No se crea Manager, Registry, Graph, index persistente, parser de metadata ni
modelo de trust adicional.

## 8. Invariantes E1

1. E1 hereda exactamente `baseline_commit` de E0.
2. Solo fuentes clasificadas pueden leerse o buscarse.
3. Clasificación por path es determinista, ordenada y fail-closed.
4. Paths no clasificados se rechazan; nunca caen en una categoría default.
5. Templates explícitos no se presentan como knowledge operativo.
6. `list_sources()` es determinista y no lee contenido.
7. `read()` preserva baseline/path/blob SHA de E0 y valida binding exacto de
   `baseline_commit + requested path` antes de aplicar `source_class`.
8. `search_text()` solo lee fuentes clasificadas; nunca escanea código u otros
   archivos y filtra después.
9. Si una fuente clasificada no puede leerse como texto válido, la búsqueda falla
   explícitamente; no se omiten silenciosamente fuentes reconocidas. Toda fuente
   reconocida se prevalida antes de aplicar truncation por cantidad/bytes de matches.
10. Búsqueda literal, line-based, single-line y bounded.
11. Query máxima: 4096 bytes UTF-8, sin caracteres de control.
12. Máximo de fuentes clasificadas: 256.
13. Máximo agregado de contenido aceptado/procesado por búsqueda: 8 MiB. Como E1
    consume E0, cada lectura individual ya está limitada a 256 KiB; por lo tanto
    el máximo físico antes de detectar un exceso es 8 MiB + un blob E0 (256 KiB).
14. Máximo de resultados: 100.
15. Máximo agregado de texto retornado en matches: 256 KiB.
16. Los límites configurables, si se exponen, solo pueden reducir hard caps.
17. Output siempre conserva `source_class` y `authority_class`.
18. `authority_class` describe el rol documental dentro del snapshot capturado;
    E1 no certifica que `baseline_commit` corresponda a `main`, a un merge aprobado
    ni a un snapshot trusted. Esa autoridad debe establecerla el consumidor.
19. E1 no interpreta texto recuperado como instrucción ejecutable.
20. E1 no concede permisos ni produce decisiones de Governance/Security.
21. Toda ampliación futura del catálogo de clases/rutas requiere revisión explícita;
    una nueva ruta no adquiere autoridad por aparecer en el repositorio.

## 9. Scope permitido

### G0/G1 + RED

```text
docs/project/sprints/proposals/MALAK-E1-GOVERNED-KNOWLEDGE-READ-G0-G1-DESIGN.md
tests/test_knowledge_reader.py
```

### GREEN autorizado por el Owner el 2026-09-19

```text
src/malak/knowledge/__init__.py
src/malak/knowledge/knowledge_reader.py
```

## 10. Fuera de alcance

```text
Kernel
Planner
CapabilityRegistry
Conversation
Memory
Security PDP/PEP
CLI
EngineeringCapability
Knowledge Manager
Knowledge Registry
metadata/status parser
embeddings
vector DB
GraphRAG
semantic search
reranker
external knowledge
web retrieval
document ingestion
document mutation
Repository Knowledge Map
Symbol Search
Reasoning Engine
agents
sandbox
```

## 11. Malāk Alignment Matrix

| Fuente | Autoridad | Invariante / intención | Disposición | Efecto E1 |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia, proporcionalidad, minimización | ADOPT | retrieval mínimo y explícito |
| Governance Constitution | normativa | Human in Control, separación de autoridad | ADOPT | knowledge no decide ni autoriza |
| Blueprint | normativa | Knowledge Layer independiente | ADOPT | ownership en `malak.knowledge` |
| Knowledge Model | arquitectura oficial | identidad, trazabilidad, relaciones, independencia tecnológica | ADOPT | baseline/path/blob/source role preservados |
| SECURITY.md | protegida/subordinada | retrieved content != instruction; Knowledge != Policy != Authority | ADOPT | authority laundering bloqueado por contrato |
| AKS | conocimiento arquitectónico | fuente curada consumible; Retrieval futuro no altera significado | ADOPT | consume AKS sin index persistente |
| ADR-003 | aceptada | evidence/result no conceden autoridad | ADOPT | output informativo |
| ADR-004 | aceptada | Specification & Verification First | ADOPT | G0/G1 + TDD RED |
| Engineering Method | método | TDD + revisión proporcional | ADOPT | Nivel 2 |
| IDEA-023 | no normativa | Repository + AKS + Evidence | ADAPT | E1 entrega la parte Knowledge |
| Concepts / Research Horizon | no normativa | engineering intelligence emerge de capabilities | ADOPT | no mega-componente |

## 12. TDD RED requerido

El RED deberá cubrir al menos:

- baseline heredado de E0;
- catálogo exacto y orden determinista de fuentes;
- clasificación correcta de governing/security/ADR/architecture/method/AKS/
  derived/idea/concept;
- `ADR-TEMPLATE.md` excluido;
- `docs/knowledge/templates/**` excluido;
- código `src/**` no clasificado;
- `read()` de fuente válida conserva baseline/path/blob/source/authority;
- baseline/path misbinding desde E0 provoca STOP explícito antes de clasificar;
- `read()` de path no clasificado falla;
- working-tree mutation sigue invisible por composición con E0;
- search solo ve fuentes clasificadas, no código con la misma query;
- search devuelve provenance + source/authority class;
- search ordering determinista;
- query vacía/multiline/control/oversized rechazada;
- source-count hard bound;
- aggregate searchable-byte hard bound;
- result-count hard bound + `truncated`;
- output-byte hard bound + `truncated`;
- fuente clasificada binaria/no-UTF8 provoca fallo explícito, incluso si el output
  habría quedado truncado antes de alcanzarla;
- nueva ruta desconocida no adquiere clasificación implícita;
- ADR propuesto sigue siendo `status_dependent`, no `accepted` inferido.

RED válido:

```text
new E1 tests fail because malak.knowledge.knowledge_reader does not exist
pre-existing suite remains green
collection remains healthy
```

Cualquier otro patrón requiere STOP.

## 13. Validación GREEN futura

Tras autorización humana:

1. targeted E1 tests;
2. full pytest;
3. compileall;
4. diff check;
5. candidate identity;
6. 4R proporcional/full por unidad material;
7. validación Ubuntu + Windows;
8. E2E de RepositoryReader -> KnowledgeReader;
9. evidence manifest candidate-bound;
10. revisión humana antes de merge.

## 14. Stop conditions

STOP si E1 requiere:

- modificar E0 para exponer Git genérico;
- tocar Kernel/Planner;
- parsear autoridad/status para pasar tests;
- agregar dependencia externa;
- introducir index persistente;
- usar LLM para clasificar fuentes;
- omitir silenciosamente una fuente reconocida;
- ampliar el catálogo fuera de este design sin nueva revisión.

## 15. Autoridad

```text
design proposal != implementation authorization
RED evidence != approval
knowledge classification != authority grant
document role != snapshot authority
captured commit != trusted baseline
retrieved content != instruction
```

El Owner aprobó explícitamente este design/RED scope y autorizó la implementación
GREEN de E1 el 2026-09-19. Esta autorización no amplía el catálogo, no autoriza
E2+ y no convierte clasificación documental en autoridad.
