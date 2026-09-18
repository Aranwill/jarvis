---
title: Malāk E0 — Repository Read Proof — G0/G1 Design
status: proposed
authority: non_normative
document_role: implementation design
language: es
created: 2026-09-18
baseline_commit: 39366da01f793cf8f5d3856c47457954ee758925
implementation_authorized: false
risk_class: 2
---

# Malāk E0 — Repository Read Proof — G0/G1 Design

## 1. Propósito

Definir la mínima frontera determinista y estrictamente read-only que permita a
Malāk obtener evidencia textual reproducible de su propio repositorio comprometido
sin introducir shell genérico, Git genérico, filesystem write, tools, agentes,
Knowledge runtime ni cambios en Kernel.

Pregunta de aceptación:

> ¿Puede Malāk obtener evidencia textual reproducible y baseline-bound de su
> propio repositorio mediante una frontera determinista y estrictamente read-only?

## 2. Baseline

```text
repository: Aranwill/jarvis
branch: main
baseline: 39366da01f793cf8f5d3856c47457954ee758925
```

## 3. Necesidad demostrada

La auditoría de alineación identificó dos gaps inmediatos para Engineering
Intelligence: Repository cognition y Knowledge runtime. E0 aborda únicamente el
primero.

La ruta futura preservada en IDEA-023 requiere:

```text
Repository + AKS + Evidence
        ↓
Engineering analysis
```

Hoy no existe ninguna frontera runtime bajo `src/malak/**` que permita inspección
del repositorio.

## 4. Ownership arquitectónico

La primitive pertenece a Infrastructure Layer porque provee un servicio técnico
de lectura. No es una Capability pública ni una operación de Execution.

Ruta candidata:

```text
src/malak/infrastructure/repository_reader.py
```

Kernel, Planner, Conversation, Memory, Security y Knowledge permanecen fuera de
alcance.

## 5. Invariantes E0

1. El reader queda ligado a un commit exacto capturado al inicializarse.
2. `repo_root` debe resolver exactamente al Git top-level; una subcarpeta no puede
   ampliar silenciosamente el scope al repositorio completo.
3. Toda lectura posterior utiliza objetos Git de ese snapshot, no el working tree.
4. Working-tree changes, staged changes y untracked files no alteran la evidencia.
5. Solo se aceptan paths lógicos POSIX, relativos, canónicos y trackeados en el
   snapshot capturado; backslashes, rutas absolutas y segmentos ambiguos se rechazan.
6. Symlinks trackeados pueden identificarse como entries, pero no se dereferencian
   ni se interpretan como documentos de texto; submodules no son documentos E0.
7. No existe API pública de shell, comando Git arbitrario ni subprocess arbitrario.
8. No existe ninguna operación de escritura.
9. Lectura textual: UTF-8 estricto, sin NUL y con techo absoluto de 256 KiB por blob.
10. Los límites configurables deben ser enteros positivos y solo pueden reducir los
    techos E0: 256 KiB por texto y 100 resultados de búsqueda.
11. Búsqueda: literal, por línea, determinista y bounded; consultas multilinea se
    rechazan y blobs oversized, binarios o no textuales se omiten sin invalidar
    el resto del snapshot.
12. El inventario Git debe usar una representación no ambigua de paths (NUL-delimited)
    y preservar nombres Unicode y espacios sin depender de quoting humano.
13. El resultado conserva procedencia suficiente para vincular contenido con
    baseline y path.
14. Fallos de repositorio, path, tamaño o contenido deben ser explícitos; no se
    convierten silenciosamente en evidencia válida.

## 6. API mínima candidata

La API exacta queda sujeta al RED/GREEN mínimo, pero el comportamiento verificable
esperado es equivalente a:

```text
GitRepositoryReader(repo_root)

baseline_commit

list_tracked_files()

read_text(path)
  -> baseline_commit
  -> path
  -> blob_sha
  -> content

search_text(query)
  -> baseline_commit
  -> matches[path, blob_sha, line_number, line]
  -> truncated
```

No se crea Protocol, Service, Manager, Registry ni abstracción adicional durante
E0 salvo necesidad demostrada por el candidate.

## 7. Scope permitido

### G0/G1 + RED

```text
docs/project/sprints/proposals/MALAK-E0-REPOSITORY-READ-PROOF-G0-G1-DESIGN.md
tests/test_repository_reader.py
```

### GREEN futuro, solo tras aprobación humana

```text
src/malak/infrastructure/repository_reader.py
```

## 8. Fuera de alcance

```text
Kernel changes
Planner changes
CapabilityRegistry changes
Conversation changes
Security PDP/PEP integration
Memory
Knowledge runtime
EngineeringCapability
CLI
Repository Knowledge Map
Symbol Search
AST / dependency / call graph
vector DB / embeddings / GraphRAG
generic Tool Runner
generic shell
Git write
filesystem write
Sandbox
Task State
agents
mission orchestration
RDD Stage 2
```

## 9. Malāk Alignment Matrix

| Fuente | Autoridad | Invariante / intención | Disposición | Efecto E0 |
| --- | --- | --- | --- | --- |
| Cognitive Constitution | normativa | proporcionalidad y minimización cognitiva | ADOPT | primitive mínima, sin capas especulativas |
| Governance Constitution | normativa | Human in Control y separación | ADOPT | lectura sin autoridad ni side effects |
| Blueprint | normativa | Capability First, Kernel pequeño, Infrastructure técnica | ADAPT | primitive Infrastructure; consumer Capability queda para E2 |
| SECURITY.md | protegida/subordinada | Zero Trust, capability != permission, contenido != autoridad | ADOPT | repo content es evidencia/contexto, nunca autoridad |
| ADR-003 | aceptada | resultados/evidencia no conceden autoridad upstream | ADOPT | reader devuelve evidencia, no decisiones |
| ADR-004 | aceptada | Specification & Verification First, proporcional | ADOPT | G0/G1 + TDD RED antes del GREEN |
| IDEA-013 | no normativa | Repository Knowledge Map mínimo y retrieval futuro | OBSERVE | no map/index persistente en E0 |
| IDEA-023 | no normativa, planificación futura | Repository + AKS + Evidence para engineering | ADAPT | E0 construye solo Repository Read |
| Research Horizon | no normativa | engineering intelligence emerge de capabilities | ADOPT | no mega-componente / no agentes |
| Runtime actual | baseline | no Repository cognition implementada | ADOPT | gap material demostrado |

## 10. TDD RED requerido

El RED debe demostrar al menos:

- captura exacta de HEAD;
- listado determinista de tracked files del snapshot;
- lectura del blob comprometido exacto;
- working-tree modification invisible;
- staged-but-uncommitted modification invisible;
- untracked file invisible;
- avance posterior de HEAD no muta el snapshot ya capturado;
- absolute path rechazado;
- traversal rechazado;
- path inexistente/no trackeado rechazado;
- blob demasiado grande rechazado;
- contenido no UTF-8 rechazado;
- búsqueda literal devuelve path + línea + baseline;
- búsqueda permanece snapshot-bound;
- límite de resultados produce señal `truncated`;
- repositorio Git inválido falla explícitamente;
- repo root distinto del Git top-level se rechaza;
- backslash y paths no canónicos se rechazan;
- límites no positivos se rechazan;
- búsqueda omite blobs no UTF-8 y oversized de forma determinista;
- symlink blob no se dereferencia ni se trata como documento;
- consultas multilinea se rechazan;
- paths Unicode y con espacios se preservan sin ambigüedad;
- UTF-8 con NUL se trata como binario y se rechaza/omite;
- los hard bounds E0 no pueden elevarse por configuración.

RED válido:

```text
new E0 tests fail because malak.infrastructure.repository_reader does not exist
pre-existing tests remain green
collection remains healthy
```

Cualquier otro patrón de fallo requiere STOP.

## 11. Validación GREEN futura

Cuando el Owner autorice implementación:

1. targeted E0 tests;
2. full pytest;
3. compileall;
4. diff check;
5. candidate identity;
6. FULL 4R por tratarse de unidad material;
7. validación independiente;
8. E2E equivalente de snapshot-bound repository read;
9. evidencia RDD Stage 1;
10. revisión humana antes de merge.

## 12. Stop conditions

STOP si:

- se necesita modificar Kernel;
- aparece necesidad de shell/genérico Git runner;
- se requiere write access;
- la implementation necesita una nueva dependencia;
- la primitive no puede permanecer snapshot-bound;
- un finding exige ampliar el scope más allá del correction budget;
- los fallos RED no quedan aislados a la ausencia de la implementación E0.

## 13. Autoridad

```text
design proposal != implementation authorization
RED evidence != approval
GREEN tests != authority
```

La implementación productiva permanece bloqueada hasta aprobación humana explícita
del Owner sobre este design/RED scope.
