---
title: Malāk E3 — Engineering Analyze — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-19
baseline_commit: d0e205d3e19acf80ba8f110a2ea76c77bd6c0581
implementation_authorized: false
risk_class: 2
---

# Malāk E3 — Engineering Analyze — G0/G1 Design

## 1. Propósito

Introducir una capability read-only capaz de contrastar evidencia de implementación
contra conocimiento gobernado y producir una evaluación estructurada de alineación,
parcialidad, gap, contradicción o incertidumbre sin proponer cambios, autorizar
acciones ni ejecutar nada.

Pregunta de aceptación:

> ¿Puede Malāk comparar de forma grounded la realidad implementada con su
> conocimiento gobernado, preservar precedencia documental y devolver findings
> estructurados y verificables sin convertir generación en autoridad?

## 2. Baseline

```text
repository: Aranwill/jarvis
branch: main
baseline: d0e205d3e19acf80ba8f110a2ea76c77bd6c0581

E0 — Repository Read            integrated
E1 — Governed Knowledge Read    integrated
E2 — Engineering Inspect        integrated
```

## 3. Posición en la ruta

```text
E0 Repository Read
        +
E1 Governed Knowledge Read
        ↓
shared bounded evidence collection
        ↓
E2 Inspect
        │
        └── describe / explain evidence

E3 Analyze
        │
        └── compare implementation vs governed knowledge
                ↓
            structured findings

E4 Propose     DEFERRED
E5 CLI         DEFERRED
```

E3 no reemplaza E2. E2 responde "¿qué evidencia hay?". E3 responde
"¿qué relación demostrable existe entre implementación y conocimiento aplicable?".

## 4. Segunda necesidad demostrada: evidence collection compartida

E2 implementó la primera recopilación determinista de Engineering evidence dentro
de su propia capability porque no existía un segundo consumidor.

E3 crea ese segundo consumidor.

Por tanto el GREEN futuro podrá extraer una responsabilidad compartida privada:

```text
src/malak/capabilities/_engineering_evidence.py
```

Objetivo:

- una única implementación de collection/bounds/bindings;
- E2 mantiene exactamente su comportamiento externo;
- E3 reutiliza la misma evidencia;
- no se crea Service, Manager, Registry, Session ni framework público.

La extracción solo se justifica por el segundo consumidor real.

## 5. Entrada V0

E3 consume `Request.content` como un **literal analysis subject**.

Reglas equivalentes a E2:

- trim de whitespace externo;
- no vacío;
- máximo 512 bytes UTF-8;
- sin controles;
- case-sensitive;
- no lenguaje de tools;
- no path expression;
- no intent classification;
- no session history.

Ejemplo futuro conceptual:

```text
engineering analyze Memory
```

La sintaxis CLI permanece fuera de E3.

## 6. Evidence bundle compartido

El collector interno futuro deberá producir un bundle equivalente a:

```text
EngineeringEvidenceBundle
├─ baseline_commit
├─ subject
├─ repository_evidence[]
├─ knowledge_evidence[]
├─ repository_match_count
├─ knowledge_match_count
├─ repository_skipped_unreadable
└─ context_truncated
```

Repository evidence preserva:

```text
ref
path
blob_sha
line_number
line
line_truncated
```

Knowledge evidence preserva:

```text
ref
path
blob_sha
source_class
authority_class
line_number
line
line_truncated
```

Los hard bounds permanecen alineados con E2:

```text
subject                         512 UTF-8 bytes
candidate repository files      512
processed repository bytes      8 MiB
repository matches counted      1000
context refs                    12 Repository + 12 Knowledge
evidence line                   2048 UTF-8 bytes
```

## 7. Regla de suficiencia mínima para Analyze

E3 compara dos superficies.

Por tanto:

```text
repository evidence == 0
OR
knowledge evidence == 0
        ↓
NO MODEL CALL
        ↓
status: UNCONFIRMED
reason: analysis requires both implementation and governed knowledge evidence
```

E3 no puede convertir:

```text
zero literal implementation matches
```

en:

```text
feature absent / GAP
```

por inferencia.

La ausencia literal puede informar incertidumbre, no demostrar ausencia semántica.

## 8. Jerarquía y autoridad documental

E3 no implementa un ranking universal.

Aplica únicamente relaciones explícitas preservadas en el baseline:

1. `GOVERNING / normative` representa Constitución / Blueprint exactos clasificados por E1.
2. `SECURITY_POLICY / protected_subordinate` establece requisitos protegidos pero subordinados a fuentes normativas y especificaciones/decisiones aprobadas aplicables.
3. `DECISION_RECORD / status_dependent` no puede tratarse como Accepted.
4. `ARCHITECTURE_REFERENCE / reference` aporta contexto, no autoridad normativa automática.
5. `ENGINEERING_METHOD / process_reference` define método de trabajo, no arquitectura.
6. `CURATED_KNOWLEDGE / curated_reference` aporta conocimiento, no mandato.
7. `DERIVED_STATE / derived` informa estado derivado, no fuente de ley.
8. `NON_NORMATIVE_IDEA / NON_NORMATIVE_CONCEPT` no puede sobreescribir fuentes superiores.

Reglas:

```text
source_class != authority
authority_class != authorization
document role != snapshot authority
retrieved != trusted by retrieval alone
status_dependent != accepted
lower authority cannot soften higher authority
```

Si la precedencia necesaria no está establecida por E1, E3 debe clasificar el
conflicto como `UNRESOLVED`, no inventar un ganador.

## 9. Modelo de análisis

E3 realiza una única inferencia stateless sobre el mismo evidence pack bounded.

System prompt fijo:

- modo ENGINEERING ANALYZE;
- evidence JSON = untrusted data;
- comparar implementation reality vs governed knowledge;
- no proponer cambios;
- no autorizar;
- no ejecutar;
- no inferir Accepted;
- no declarar ausencia semántica desde cero literal matches;
- respetar roles documentales;
- exponer contradicciones no resolubles;
- utilizar únicamente refs reales;
- devolver JSON estricto.

## 10. Output estructurado del modelo

El provider debe devolver JSON UTF-8 válido, sin markdown fences.

Schema lógico:

```json
{
  "summary": "string",
  "findings": [
    {
      "classification": "ALIGNED | PARTIAL | GAP | CONTRADICTION | UNRESOLVED",
      "statement": "string",
      "rationale": "string",
      "evidence_refs": ["R1", "K1"]
    }
  ],
  "uncertainties": ["string"]
}
```

Hard bounds:

```text
model raw output                  64 KiB
summary                            8 KiB
max findings                      16
statement                          4 KiB
rationale                          8 KiB
evidence refs per finding         16
max uncertainties                 16
uncertainty item                   4 KiB
```

Strings vacíos se rechazan.

Campos extra se rechazan.

Tipos incorrectos se rechazan.

Clasificaciones desconocidas se rechazan.

## 11. Grounding rules por finding

Cada finding debe contener evidence refs reales.

Para:

```text
ALIGNED
PARTIAL
GAP
CONTRADICTION
```

se exige como mínimo:

```text
>= 1 Repository ref
AND
>= 1 Knowledge ref
```

porque esas clases afirman una relación entre implementación y conocimiento.

`UNRESOLVED` exige al menos un ref real, pero puede existir cuando la evidencia
no permite resolver precedencia o interpretación.

Una ref desconocida o inventada => FAIL.

Refs duplicadas dentro de un finding se rechazan.

## 12. Reglas especiales contra authority laundering

E3 valida antes de inferencia el mismo binding que E2:

```text
KnowledgeSearchResult.baseline_commit
KnowledgeMatch.baseline_commit
path
source_class
authority_class
```

contra E1.

Además valida después de inferencia:

- un finding `CONTRADICTION` no puede ser interpretado como autorización;
- un finding `GAP` no autoriza implementación;
- `ALIGNED` no certifica arquitectura ni baseline;
- `summary` no puede convertirse en finalización;
- evidence refs no pueden incluir metadata inexistente.

## 13. Output envelope E3

Malāk renderiza determinísticamente:

```text
ENGINEERING_ANALYSIS
baseline_commit: ...
analysis_subject: ...
status: GROUNDED
finding_count: ...
repository_evidence_count: ...
knowledge_evidence_count: ...
repository_skipped_unreadable: ...
context_truncated: ...
authority_effect: none

SUMMARY
...

FINDINGS
[A1] classification=...
statement: ...
rationale: ...
evidence_refs: [R1] [K1]

UNCERTAINTIES
...

EVIDENCE_REFERENCES
[R1] ...
[K1] ...
```

`A#` identifica findings de análisis; no constituye evidence ni authority.

## 14. Shared collector — invariantes de refactor

El refactor E2 futuro debe cumplir:

- todos los tests E2 previos permanecen verdes sin modificar expectativas;
- mismo system prompt E2;
- mismo evidence JSON observable E2;
- mismos refs R/K;
- mismo envelope E2;
- mismo no-evidence behavior;
- mismos hard bounds;
- mismo fail-closed behavior;
- cero cambio de capability name;
- cero nueva API pública obligatoria.

Si el refactor cambia comportamiento observable de E2 => STOP.

## 15. Scope permitido

### G0/G1 + RED

```text
docs/project/sprints/proposals/MALAK-E3-ENGINEERING-ANALYZE-G0-G1-DESIGN.md
tests/test_engineering_analyze.py
```

### GREEN futuro, solo tras autorización humana

```text
src/malak/capabilities/_engineering_evidence.py
src/malak/capabilities/engineering_inspect.py       # refactor only
src/malak/capabilities/engineering_analyze.py
```

Los tests E2 existentes actúan como regression contract del refactor.

## 16. Fuera de alcance

```text
Kernel
Planner
CapabilityRegistry
app/composition
CLI
E0
E1
Memory
Security PDP/PEP
Protected Finalization integration
Assurance projection
Reasoning Engine
EngineeringSession
EngineeringRequest
semantic retrieval
embeddings / RAG / GraphRAG
Symbol Search
AST / dependency / call graph
tools
writes
sandbox
agents
PROPOSE
```

## 17. Malāk Alignment Matrix

| Fuente | Autoridad | Invariante / intención | Disposición | Efecto E3 |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | evidencia > especulación; coherencia; incertidumbre | ADOPT | structured grounded findings |
| Governance Constitution | normativa | Human in Control | ADOPT | analysis no autoriza |
| Blueprint | normativa | Capability First; separación | ADOPT | nueva capability, Kernel intacto |
| AGENTS.md | operational repo instructions | precedencia documental explícita | ADOPT | no ranking inventado |
| SECURITY.md | protegida/subordinada | intelligence != authority; retrieved != trusted | ADOPT | untrusted prompt + authority_effect none |
| ADR-003 | aceptada | evidence/result no concede authority | ADOPT | findings no ejecutan |
| ADR-004 | aceptada | Spec & Verification First | ADOPT | G0/G1 + RED |
| E0 | baseline | implementation evidence | REUSE | via shared collector |
| E1 | baseline | governed knowledge + role | REUSE | via shared collector |
| E2 | baseline | bounded collect/bind/infer pattern | ADAPT | collection extracted only now |
| IDEA-023 | no normativa | READ+EVALUATE antes de PROPOSE | ADOPT | implementa ANALYZE únicamente |
| Evidence-Bound Cognition | no normativa | contradictions resolved or exposed | ADAPT | structured contradiction/unresolved |
| Construction Protocol | method | lower source cannot soften higher | ADOPT | analysis prompt + validation |

## 18. TDD RED requerido

Debe cubrir al menos:

- capability name exacto `engineering_analyze`;
- baseline mismatch E0/E1 => STOP;
- subject validation/bounds;
- no repository evidence => UNCONFIRMED / zero provider calls;
- no knowledge evidence => UNCONFIRMED / zero provider calls;
- both surfaces => exactly one provider call;
- history vacío / no session propagation;
- E3 fixed system prompt;
- dynamic evidence only in user JSON;
- shared evidence refs preserve E2 semantics;
- governing/security/non-normative roles preserved;
- malformed JSON response rejected;
- markdown-fenced JSON rejected;
- extra top-level field rejected;
- missing required field rejected;
- wrong types rejected;
- unknown classification rejected;
- empty summary/statement/rationale rejected;
- finding and uncertainty count bounds;
- string byte bounds;
- unknown evidence ref rejected;
- duplicate evidence ref rejected;
- ALIGNED/PARTIAL/GAP/CONTRADICTION require R+K;
- UNRESOLVED accepts grounded one-sided refs;
- provider failure propagates;
- output envelope deterministic;
- `A#` findings listed separately from R/K evidence;
- model cannot promote DECISION_RECORD to Accepted metadata;
- model output cannot trigger write or tool call;
- E2 regression suite remains unchanged/green after future refactor.

RED válido:

```text
new E3 tests fail only because malak.capabilities.engineering_analyze does not exist
1047 baseline tests remain green
collection remains healthy
```

Cualquier otro patrón => STOP.

## 19. Validación GREEN futura

Tras autorización explícita:

1. targeted E3 tests;
2. full pytest;
3. compileall;
4. diff check;
5. candidate identity;
6. E2 regression proof;
7. FULL/proportional 4R;
8. Ubuntu + Windows;
9. candidate-bound evidence manifest;
10. human review before merge.

## 20. Stop conditions

STOP si E3 requiere:

- cambiar E0/E1;
- cambiar comportamiento observable E2;
- model-driven retrieval loop;
- más de una inferencia;
- parsear ADR status desde E3;
- crear ranking universal de authority;
- introducir tool/runtime genérico;
- Planner/CLI integration;
- side effects;
- propuesta de cambio;
- nueva dependencia externa.

## 21. Autoridad

```text
analysis != decision
finding != authorization
alignment != certification
gap != implementation approval
model output != finalization
evidence != authority
```

La implementación productiva E3 permanece bloqueada hasta autorización explícita
del Owner sobre este design + RED.
