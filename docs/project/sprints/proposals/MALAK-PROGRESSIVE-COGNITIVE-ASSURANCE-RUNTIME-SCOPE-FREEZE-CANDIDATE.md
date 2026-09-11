---
title: Malāk Progressive Cognitive Assurance Runtime — Scope Freeze Candidate
status: gate_candidate
authority: planning_candidate
language: es
as_of_date: 2026-09-11
source_baseline: 5865da6a5e502fe71e35e2e38bc4cceaab9b3600
risk_class_if_promoted: 3
implementation_authorized: false
sprint_7_12_authorized: false
rdd_stage_2_authorized: false
candidate_content_identity_g2_authorized: false
persistence_authorization_authorized: false
related:
  - docs/governance/cognitive_constitution.md
  - docs/architecture/blueprint.md
  - docs/project/sprints/proposals/MALAK-COGNITIVE-ASSURANCE-G1-PROGRESSIVE-DESIGN.md
  - docs/project/concepts/MALAK_EVIDENCE_BOUND_COGNITION_FOUNDATION.md
  - docs/project/status/MALAK-POST-AUDIT-REBASELINE-20260911.md
---

# Malāk Progressive Cognitive Assurance Runtime — Scope Freeze Candidate

## 1. Estado de autoridad

Este documento prepara un posible gate posterior para materializar una frontera runtime mínima de Progressive Cognitive Assurance.

No constituye aprobación de implementación.

No constituye Sprint 7.12.

No concede permisos nuevos a ningún componente.

```text
Scope Freeze Candidate != Approved Scope
Approved Scope != Implementation Authorization
Implementation != Authority Expansion
```

---

## 2. Problema que intenta resolver

La Constitución Cognitiva vigente establece, entre otros, dos principios ya normativos:

```text
CC-011
Generation != Finalization
Candidate != Accepted Response
Evidence != Authority

CC-012
material response
→ applicable cognitive validation
→ evidence-bound finalization
```

El diseño G1 de Progressive Cognitive Assurance define además una dirección:

```text
probabilistic workers
        ↓
candidates / evidence / estimates
        ↓
deterministic + governed assurance rules
        ↓
ACCEPT | QUALIFY | ABSTAIN | BLOCK
        ↓
final response
```

Sin embargo, el runtime conversacional actual todavía no posee una frontera explícita que materialice esa separación.

Por tanto existe un gap real entre:

```text
normative cognitive law
and
runtime finalization behavior
```

---

## 3. Objetivo candidato

Diseñar e implementar, solo si recibe autorización posterior, la **mínima frontera runtime determinista y gobernada** capaz de evaluar un candidato de respuesta antes de su finalización.

La unidad debe probar una sola propiedad principal:

```text
candidate response
cannot become final response
without crossing the applicable assurance boundary
```

No debe intentar resolver en una sola unidad todo el futuro sistema de assurance.

---

## 4. Alcance candidato permitido

Si el Owner autoriza posteriormente la implementación, el scope máximo candidato sería:

1. contratos internos mínimos para representar:
   - candidato de respuesta;
   - contexto de assurance aplicable;
   - evidencia/señales disponibles sin introducir retrieval nuevo;
   - resultado de evaluación;
2. policy/evaluator determinista y puro para outcomes conceptuales equivalentes a:
   - ACCEPT;
   - QUALIFY;
   - ABSTAIN;
   - BLOCK;
3. reglas explícitas para:
   - no elevar evidencia débil mediante model confidence;
   - preservar contradicciones materiales;
   - impedir bypass de checks aplicables;
   - fallar de forma segura ante estado inválido;
4. integración mínima en una frontera de finalización existente, preferentemente fuera del Kernel;
5. tests positivos y negativos suficientes para demostrar que el bypass no es posible en la ruta integrada autorizada;
6. observabilidad solo si reutiliza contratos existentes y no amplía el scope de observabilidad.

---

## 5. Alcance explícitamente excluido

Este gate candidato NO debe incluir:

- Sprint 7.12 por mera numeración;
- modificación del Kernel salvo evidencia posterior de necesidad inevitable;
- modificación de SecurityContext;
- nuevo motor de autorización;
- Memory persistente;
- Persistence Authorization;
- Candidate Content Identity G2;
- retrieval;
- Knowledge operativo;
- RAG;
- web browsing;
- agentes;
- tools externas;
- MCP/A2A;
- Sandbox;
- navegación;
- provider/model concreto obligatorio;
- segundo modelo always-on;
- majority voting;
- scoring mágico único;
- Resource Governance completa;
- Model Governance completa;
- RDD Stage 2;
- nuevos privilegios;
- autoaprendizaje persistente;
- modificación constitucional adicional.

---

## 6. Invariantes obligatorios

Cualquier diseño posterior deberá preservar:

```text
Kernel First
Constitution First
Governance First
Capability First
Human in Control
Zero Trust
Model Agnostic
Runtime Independence
Security by Design
Everything is Observable
Everything is Auditable
```

Y además:

```text
Generation != Finalization
Evidence != Authority
Confidence != Evidence
QUALIFY != hidden downgrade
ABSTAIN != failure
BLOCK != uncertainty
required assurance != available resources
resource scarcity must not silently reduce assurance floor
```

---

## 7. Restricción arquitectónica principal

La frontera candidata no debe convertir el Kernel en un motor de evaluación cognitiva pesada ni en un orquestador de providers.

Dirección preferida a validar:

```text
Conversation/Capability result
        ↓
Response Candidate
        ↓
Cognitive Assurance Boundary
        ↓
Assurance Outcome
        ↓
Finalization Adapter
        ↓
Response
```

La ubicación exacta NO queda congelada por este documento.

Debe decidirse mediante inspección del código vigente y del ownership arquitectónico existente.

---

## 8. Política mínima candidata

La primera implementación, si se autoriza, debe privilegiar reglas simples y demostrables.

Ejemplo de semántica candidata:

```text
policy/security violation
→ BLOCK

material contradiction unresolved
→ QUALIFY or ABSTAIN

required evidence absent
→ QUALIFY or ABSTAIN

applicable checks passed
→ ACCEPT
```

No debe introducir todavía niveles `A0..A3` como API pública si no son necesarios para demostrar la frontera.

Los niveles del G1 continúan siendo placeholders de diseño hasta un gate específico.

---

## 9. Bounded cognition

La primera frontera runtime no debe crear loops cognitivos.

En esta unidad:

```text
no recursive self-review
no unbounded retries
no automatic verifier fan-out
no hidden second-pass LLM
```

Si una evaluación no puede alcanzar soporte suficiente con las entradas ya disponibles dentro del scope autorizado:

```text
QUALIFY | ABSTAIN | BLOCK
```

No se debe inventar evidencia ni ampliar el scope automáticamente.

---

## 10. Relación con Memory

La cadena episódica existente puede proporcionar fundamentos futuros de evidencia gobernada, pero esta unidad no debe conectarla todavía a Conversation/runtime por conveniencia.

```text
Episodic chain exists
!=
Assurance runtime may consume it automatically
```

La integración de Memory con Conversation requiere un gate separado.

---

## 11. Relación con Candidate Content Identity G2

Candidate Content Identity G2 continúa siendo una frontera independiente.

La primera materialización de assurance puede utilizar únicamente identidades y bindings ya existentes cuando sean suficientes para su scope.

No debe implementar G2 incidentalmente.

Si durante la inspección se demuestra que una propiedad crítica de assurance no puede cumplirse sin identidad de contenido más fuerte, la implementación debe detenerse y elevar esa dependencia como blocker explícito.

```text
missing prerequisite
→ stop / separate gate
not
→ silently implement adjacent architecture
```

---

## 12. Preguntas obligatorias antes de autorizar implementación

### Q1 — ¿Existe una necesidad real?

Sí, conceptualmente: CC-011/CC-012 ya exigen una separación que el runtime actual no materializa explícitamente.

Debe verificarse en código que no exista ya una frontera equivalente suficiente.

### Q2 — ¿Cuál es la mínima unidad útil?

Una única frontera de evaluación/finalización con policy determinista, outcomes cerrados y wiring mínimo en una ruta autorizada.

### Q3 — ¿Puede hacerse sin ampliar autoridad?

Debe poder hacerse reutilizando autoridad y contratos existentes. Si exige nuevos privilegios, el scope no es aceptable.

### Q4 — ¿Cómo se demuestra que funciona?

Como mínimo:

- candidate aceptable atraviesa la frontera y finaliza;
- candidate con evidencia insuficiente no finaliza como plenamente soportado;
- contradicción material no puede ocultarse mediante síntesis;
- policy/security block no puede ser bypassed;
- malformed/unknown state falla de manera segura;
- ningún path autorizado puede devolver una respuesta material saltando la frontera integrada;
- suite completa permanece verde;
- compileall PASS;
- git diff --check PASS;
- validación candidate-bound PASS.

---

## 13. Stop conditions

La implementación debe detenerse si aparece cualquiera de estas condiciones:

- requiere modificar Kernel sin justificación arquitectónica separada;
- requiere Candidate Content Identity G2;
- requiere Persistence Authorization;
- requiere retrieval/Knowledge/Memory wiring;
- requiere un nuevo motor de autoridad;
- requiere dependencias externas nuevas;
- introduce loops de verificación no acotados;
- obliga a seleccionar un provider/model específico;
- reduce silenciosamente el assurance requerido por límites de recursos;
- expande el cambio a refactors laterales no necesarios;
- la suite o CI deja de ser reproducible.

---

## 14. Secuencia candidata si el gate es aprobado

```text
G0 — inspect current runtime finalization path
        ↓
G1 — freeze exact contracts + ownership + invariants
        ↓
Owner approval
        ↓
G2 — minimal implementation candidate
        ↓
candidate-bound validation
        ↓
independent review
        ↓
Owner merge decision
```

La denominación G0/G1/G2 aquí describe gates internos de esta unidad y NO autoriza RDD Stage 2 ni Sprint 7.12.

---

## 15. Resultado de este documento

```text
candidate direction:
Progressive Cognitive Assurance Runtime Boundary

current decision:
READY FOR OWNER REVIEW OF SCOPE

implementation:
NOT AUTHORIZED

Sprint 7.12:
NOT AUTHORIZED

Candidate Content Identity G2:
NOT AUTHORIZED

Persistence Authorization:
NOT AUTHORIZED

RDD Stage 2:
NOT AUTHORIZED
```

El siguiente paso válido es revisar este scope contra el código real y las fuentes normativas vigentes. Solo después de esa inspección puede proponerse una especificación ejecutable y solicitarse autorización de implementación.
