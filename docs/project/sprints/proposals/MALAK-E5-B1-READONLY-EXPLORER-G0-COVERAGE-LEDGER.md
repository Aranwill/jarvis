---
title: Malāk E5-B1 — G0 File Coverage Ledger
status: gate_pass
authority: operational admission evidence
as_of_date: 2026-09-19
unit_id: MALAK-E5-B1
gate: G0
source_baseline: a33aba233115830e002c6a6646aa1a701f77aa8d
language: es
---

# Malāk E5-B1 — G0 File Coverage Ledger

## Resultado

```text
G0 RESULT: PASS
blocking findings: 0
tracked files discovered: 260
tracked files classified: 260
silently omitted files: 0
implementation code touched: 0
```

El árbol Git recursivo del baseline oficial
`a33aba233115830e002c6a6646aa1a701f77aa8d` declaró `truncated: false`.

`50e64b2137d5ec1a53bf3cc47bca0fcbb9e21874`.

No se detectó el archivo expresamente rechazado
`PROJECT - MANIFIESTO MALAK (1).docx`. Si reaparece deberá clasificarse
`REJECTED_DO_NOT_READ` y no abrirse.

---

## Inventario por familia

```text
.github/**                  2
architecture              14
development                5
governance                 2
knowledge                 10
concepts                   6
project state              6
sprints/proposals         62
ideas/history             10
src/malak/**              73
tests/**                  50
other                     20
----------------------------
tracked blobs            260
classified blobs         260
silently omitted           0
```

---

## Lectura profunda requerida

```text
AGENTS.md
SECURITY.md
docs/governance/cognitive_constitution.md
docs/governance/governance_constitution.md
docs/architecture/blueprint.md
docs/architecture/architecture_quality_gates.md
docs/development/malak_construction_protocol.md
docs/project/implementation_roadmap.md
docs/project/project_context.md
docs/project/sprints/proposals/MALAK-E5-ENGINEERING-CLI-G0-G1-DESIGN.md
src/malak/app/cli.py
src/malak/app/composition.py
src/malak/infrastructure/repository_reader.py
src/malak/knowledge/knowledge_reader.py
src/malak/services/conversation_context.py
src/malak/capabilities/_engineering_evidence.py
tests/test_cli.py
tests/test_app_composition.py
tests/test_repository_reader.py
tests/test_knowledge_reader.py
```

Razón: ley, baseline actual y owners reales de lectura/navegación.

El resto del repositorio quedó cubierto mediante inspección estructural,
clasificación por familia y antecedentes históricos proporcionales al riesgo.

---

# Findings de admisión

## E5B1-G0-01 — E0 ya posee navegación read-only suficiente

```text
OBSERVED
blocking: no
```

`GitRepositoryReader` ya implementa:

- `list_tracked_files()`;
- `read_text(path)`;
- `search_text(query)`;
- snapshot Git inmutable por baseline;
- validación de paths;
- límites de bytes, blobs, resultados y timeout.

E5-B1 no necesita otro repository reader.

## E5B1-G0-02 — E1 ya posee navegación documental gobernada

```text
OBSERVED
blocking: no
```

`GovernedKnowledgeReader` ya implementa:

- `list_sources()`;
- `read(path)`;
- `search_text(query)`;
- `source_class`;
- `authority_class`;
- binding al mismo baseline E0.

E5-B1 no necesita otro índice documental.

## E5B1-G0-03 — Sessions no tiene catálogo navegable

```text
OBSERVED
blocking: no
disposition: DEFERRED
```

`InMemoryConversationContext` sólo mantiene history efímero por un
`session_id` conocido. No existe API de listado, metadata durable o catálogo
de sesiones.

Crear un session browser ahora inventaría un sistema nuevo para alimentar UI.

## E5B1-G0-04 — Evidence / findings / proposals no poseen store navegable

```text
OBSERVED
blocking: no
disposition: DEFERRED
```

Engineering produce evidencia/resultados durante requests, pero el baseline no
contiene un runtime registry durable para navegarlos posteriormente.

El evidence manifest de validación de candidates tiene otra responsabilidad y
no debe reutilizarse como artifact store de terminal.

## E5B1-G0-05 — El Explorer puede compartir exactamente el snapshot de E5-A

```text
OBSERVED
blocking: no
```

E5-A ya crea un único `GitRepositoryReader` y un único
`GovernedKnowledgeReader` para E2/E3/E4. E5-B1 debe proyectar esas mismas
instancias; crear readers paralelos sería drift de baseline innecesario.

---

# Security Horizon

| Línea | Resultado |
| --- | --- |
| Prompt & Context Trust | ALREADY_COVERED — parser exacto; cero LLM routing |
| Identity & Delegation | NOT_APPLICABLE |
| Compromise Containment | NOT_APPLICABLE |
| Memory / Knowledge Poisoning | ALREADY_COVERED — E1 conserva clasificación |
| AI Supply Chain | ALREADY_COVERED — cero dependencia nueva |
| Data Disclosure | REQUIRES_REINFORCEMENT — salida de terminal debe quedar bounded |
| Resource Governance | ALREADY_COVERED — E0/E1 ya poseen límites hard |
| Human in Control | ALREADY_COVERED — read-only, authority effect none |

No existe `BLOCKING_GAP` para diseñar E5-B1.

---

# Cierre G0

```text
E5-B1 Read-only Explorer
G0 = PASS

new reader required        = no
new store required         = no
new dependency required    = no
Kernel change required     = no
Planner change required    = no
write authority required   = no
```

Este PASS autoriza únicamente G1 documental.
