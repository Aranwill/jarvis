---
title: Sprint 7.6 — Secure Context Lifecycle Foundation
status: cerrado
authority: documentación operativa derivada
as_of_date: 2026-08-15
as_of_commit: 821497485f1b861cafa97cc5720616c3314b35bf
branch: main
language: es
---

# Sprint 7.6 — Secure Context Lifecycle Foundation

## Estado

```text
CERRADO
```

El Sprint 7.6 fue implementado mediante incrementos pequeños, secuenciales,
revisables y reversibles.

Cada incremento fue desarrollado mediante:

- Specification-Driven Development (SDD);
- Test-Driven Development (TDD);
- revisión 4R:
  - Risk;
  - Readability;
  - Reliability;
  - Resilience;
- validación independiente;
- aceptación humana explícita.

Riesgo asignado al sprint:

```text
Level 3 — High
```

## Baseline inicial

El Sprint 7.6 comenzó desde:

```text
a11617e4056325d593e3b1999baf07570cebd0d6
```

## Baseline técnico final

El candidate funcional final aprobado fue:

```text
aa06e98a2e1e20a5d81007bac83920a79f23092d
```

Después de la integración mediante Pull Requests, el baseline de `main`
revalidado es:

```text
821497485f1b861cafa97cc5720616c3314b35bf
```

El árbol funcional de `main` conserva el candidate aprobado del Sprint 7.6.

## Objetivo

Establecer una fundación mínima, determinista y desacoplada para el ciclo de
vida de `SecurityContext`, incorporando identidad contextual, tiempo de vida,
emisión, renovación, validación y propagación sin ampliar autoridad ni
introducir todavía identidad criptográfica, replay protection o un Secure
Message Bus.

## Incrementos implementados

### 7.6-A — SecurityContext Contract

Se amplió `SecurityContext` con:

- `context_id`;
- `session_id`;
- `subject_id`;
- `authenticated`;
- `issued_at`;
- `expires_at`;
- `parent_context_id | None`.

Invariantes establecidos:

- `SecurityContext` permanece inmutable;
- IDs obligatorios no pueden estar vacíos;
- `issued_at` y `expires_at` deben ser `datetime`;
- ambos timestamps deben ser timezone-aware;
- `expires_at > issued_at`;
- `parent_context_id`, cuando existe, no puede estar vacío.

### 7.6-B — Clock Boundary

Se introdujo una frontera temporal explícita:

- `Clock`;
- `SystemClock`.

`SystemClock` produce tiempos UTC timezone-aware.

La dependencia temporal puede inyectarse para pruebas deterministas.

### 7.6-C — SecurityContextValidator Boundary

Se incorporó `SecurityContextValidator`.

Su responsabilidad queda limitada a evaluar la vigencia temporal de un
`SecurityContext` mediante un `Clock` inyectado.

No concede permisos ni toma decisiones de autorización.

### 7.6-D — SecurityContextIssuer Boundary

Se incorporó `SecurityContextIssuer`.

Responsabilidades:

- generar un nuevo `context_id`;
- preservar `session_id`;
- preservar `subject_id`;
- preservar el estado `authenticated` recibido;
- registrar `issued_at`;
- calcular `expires_at`;
- permitir `parent_context_id` opcional;
- rechazar lifetimes no positivos.

El issuer no decide permisos ni autentica sujetos.

### 7.6-E — SecurityContextRenewer Boundary

Se incorporó `SecurityContextRenewer`.

La renovación:

- requiere que el contexto existente continúe vigente;
- conserva `session_id`;
- conserva `subject_id`;
- conserva `authenticated`;
- genera un nuevo `context_id`;
- utiliza el contexto anterior como `parent_context_id`;
- delega la emisión al `SecurityContextIssuer`.

La renovación no concede privilegios nuevos.

### 7.6-F — PDP SecurityContext Lifecycle Enforcement

`StaticPolicyDecisionPoint` ahora requiere un
`SecurityContextValidator` explícito.

Orden relevante de evaluación:

```text
authentication
→ lifecycle validation
→ policy lookup
→ policy decision
```

Un contexto temporalmente inválido se deniega antes de alcanzar una regla de
autorización.

El comportamiento permanece fail-closed.

No se modificó la lógica funcional del Policy Enforcement Point.

### 7.6-G — SecurityContext Validity Window Semantics

La vigencia temporal quedó formalizada como:

```text
issued_at <= now < expires_at
```

Por tanto:

- antes de `issued_at`: inválido;
- exactamente en `issued_at`: válido;
- durante la ventana: válido;
- exactamente en `expires_at`: inválido;
- después de `expires_at`: inválido.

Esto impide utilizar contextos antes de su emisión formal.

### 7.6-H — SecurityContext Propagation Contract

Se incorporó `SecurityContextEnvelope` como contrato mínimo de propagación en
memoria.

Propiedades:

- inmutable;
- contiene un `SecurityContext`;
- preserva la misma instancia recibida;
- no reconstruye sus campos;
- no emite contextos;
- no renueva contextos;
- no modifica autoridad;
- no serializa;
- no implementa transporte entre procesos.

## Arquitectura resultante

```text
Clock
  │
  ▼
SecurityContextIssuer
  │
  ▼
SecurityContext
  │
  ├──────────────► SecurityContextRenewer
  │
  ▼
SecurityContextValidator
  │
  ▼
Policy Decision Point
  │
  ▼
Policy Enforcement Point
```

La propagación contextual permanece separada:

```text
SecurityContext
      │
      ▼
SecurityContextEnvelope
```

## Separación de responsabilidades

### SecurityContext

Representa identidad contextual y límites de lifecycle.

No concede permisos.

### Clock

Proporciona la fuente temporal.

No decide vigencia ni autorización.

### SecurityContextValidator

Evalúa exclusivamente vigencia temporal.

No decide políticas.

### SecurityContextIssuer

Construye nuevos contextos.

No autentica sujetos ni concede privilegios.

### SecurityContextRenewer

Renueva contextos todavía válidos y conserva lineage.

No eleva autoridad.

### Policy Decision Point

Continúa siendo responsable de autorización.

La validez temporal es una precondición, no una decisión de policy.

### Policy Enforcement Point

Permanece responsable del enforcement de decisiones válidas.

No recibió cambios funcionales durante este sprint.

### SecurityContextEnvelope

Transporta un contexto existente en memoria.

No modifica ni interpreta su autoridad.

## Invariantes de seguridad preservados

- denegación por defecto;
- comportamiento fail-closed;
- Human in Control;
- Zero Trust;
- separación entre autenticación, lifecycle, autorización y enforcement;
- ningún componente puede autoelevar autoridad;
- ningún LLM participa en decisiones de seguridad;
- no existe estado global mutable nuevo;
- Kernel permanece fuera del lifecycle;
- Planner permanece fuera del lifecycle;
- runtimes permanecen fuera del lifecycle;
- el contexto no puede utilizarse antes de `issued_at`;
- el contexto no puede utilizarse desde `expires_at` en adelante;
- la renovación no revive un contexto expirado;
- la propagación no reconstruye silenciosamente identidad o autoridad.

## Relación con ADR-003

El sprint respeta `ADR-003 — Directional Communication and Authority Flow`.

Los componentes pueden transportar contexto o retornar información sin que
ello implique transferencia de autoridad.

Ningún componente downstream obtiene capacidad para:

- autorizarse;
- elevar privilegios;
- modificar políticas;
- controlar componentes upstream;
- alterar documentos de ley.

## Fuera de alcance

Permanecen expresamente fuera del Sprint 7.6:

- nonce;
- replay protection;
- prevención persistente de replay;
- firmas criptográficas;
- PKI;
- identidad criptográfica de componentes;
- MFA;
- Identity & Trust Framework completo;
- Secure Context Manager criptográfico completo;
- Secure Message Bus;
- serialización entre procesos;
- IPC seguro;
- receipts;
- Receipt-Driven Development completo;
- persistencia de contextos;
- agentes;
- navegación;
- herramientas externas;
- cambios en Kernel;
- cambios en Planner;
- rutas operativas reales de alto riesgo.

## Integración

La integración funcional del Sprint 7.6 se realizó mediante:

- PR #39 — SecurityContext lifecycle contract;
- PR #40 — integración acumulada hasta PDP lifecycle enforcement;
- PR #41 — SecurityContext validity window;
- PR #42 — SecurityContext propagation contract.

HEAD de `main` después de la integración:

```text
821497485f1b861cafa97cc5720616c3314b35bf
```

## Validación final

La validación directa sobre `main` después de integrar el sprint produjo:

```text
339 passed
compileall: PASS
git diff --check: PASS
working tree: clean
```

No se detectaron blockers funcionales ni arquitectónicos durante la revisión
integral.

## Revisión 4R

Resultado final:

| Dimensión | Resultado |
|---|---|
| Risk | PASS |
| Readability | PASS |
| Reliability | PASS |
| Resilience | PASS |

Todos los incrementos fueron revisados individualmente antes de ser aceptados
como nuevos puntos estables.

## Cuatro preguntas obligatorias

### 1. ¿Respeta el Blueprint?

Sí.

El lifecycle permanece desacoplado del Kernel y las responsabilidades están
separadas.

### 2. ¿Respeta la Constitución Cognitiva?

Sí.

La cognición no adquiere autoridad sobre identidad, lifecycle ni permisos.

### 3. ¿Respeta la Gobernanza?

Sí.

El sprint fue diseñado, implementado, validado y aceptado incrementalmente con
aprobación humana explícita.

### 4. ¿Hace al Kernel más simple o más complejo?

No aumenta su complejidad.

El Kernel no fue modificado.

## Riesgos residuales

El sprint establece únicamente la fundación del lifecycle.

Persisten para fases posteriores:

- autenticidad criptográfica del contexto;
- protección frente a replay;
- identidad fuerte de componentes;
- transporte autenticado entre procesos;
- revocación;
- políticas avanzadas de trust;
- persistencia segura;
- auditoría criptográficamente protegida.

Estos elementos no invalidan el alcance aprobado de esta fundación.

## Rollback

El Sprint 7.6 fue desarrollado mediante commits incrementales y reversibles.

El baseline anterior al sprint permanece identificado por:

```text
a11617e4056325d593e3b1999baf07570cebd0d6
```

Cualquier rollback debe evaluarse respetando las dependencias introducidas por
cada incremento y no debe ejecutarse automáticamente.

## Cierre

```text
Sprint 7.6 — Secure Context Lifecycle Foundation
Estado: CERRADO
Baseline técnico integrado: main@821497485f1b861cafa97cc5720616c3314b35bf
Suite validada: 339 passed
```

El cierre de Sprint 7.6 **no autoriza automáticamente Sprint 7.7 ni ninguna
implementación posterior**.
