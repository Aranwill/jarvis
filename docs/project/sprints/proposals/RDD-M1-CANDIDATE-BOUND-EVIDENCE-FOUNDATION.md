---
title: RDD-M1 — Candidate-Bound Evidence Foundation
status: autorizado_para_stage_1
authority: documentación operativa de admisión
as_of_date: 2026-09-08
baseline_commit: e8c1e5c14ee1b844fa23ca5cb342237f7aaaa8f0
branch: feat/rdd-m1-evidence-foundation
unit_id: RDD-M1
rdd_stage_from: 0
rdd_stage_to: 1
stage_2_authorized: false
language: es
---

# RDD-M1 — Candidate-Bound Evidence Foundation

## Estado

```text
UNIDAD RDD-M1 AUTORIZADA PARA STAGE 1
GATES G0–G6 AUTORIZADOS
STAGE 2 NO AUTORIZADO
```

El propietario aprobó explícitamente el 2026-09-08 avanzar con la incorporación
nativa de la lógica madura de Receipt-Driven Development al método de construcción
de Malāk, bajo las reglas, arquitectura y gobernanza propias de Malāk.

Esta autorización no constituye adopción de código, tooling, stores, runtimes,
provider bindings, lifecycle engines ni autoridad de delivery provenientes de
Gentle-AI u otra implementación externa.

La intención aprobada es:

```text
adoptar la lógica útil
→ expresarla mediante contratos propios de Malāk
→ reutilizar mecanismos ya existentes
→ introducir únicamente el mínimo tooling determinista faltante
→ medir utilidad real antes de promover infraestructura adicional
```

La promoción posterior a Stage 2 — Candidate-Bound Validation Receipt requiere
una admission review y autorización separadas.

---

# 1. Necesidad comprobada

Malāk ya posee de forma explícita en su Engineering Method y Construction Protocol:

- Candidate Identity;
- clasificación de riesgo;
- revisión proporcional 4R;
- separación Writer / Reviewer / Validator / Authority;
- Bounded Correction;
- Correction Budget;
- validación independiente;
- resultados PASS / FAIL / INCONCLUSIVE;
- evidencia de findings;
- gates de implementación;
- trazabilidad de especificación, tests, implementación y validación.

El gap actual no es metodológico.

El gap es de representación verificable:

```text
la evidencia existe
+
la identidad de candidato existe conceptualmente

pero

no existe todavía un artefacto estructurado mínimo
que ligue de forma determinista la evidencia
al candidato exacto evaluado
```

RDD-M1 cubre exclusivamente ese gap.

---

# 2. Objetivo

Promover el perfil RDD progresivo de Malāk desde:

```text
Stage 0 — Candidate Identity + evidencia actual
```

hacia:

```text
Stage 1 — Structured Evidence Manifest
```

mediante un contrato mínimo `MALAK-EVIDENCE-MANIFEST/v1` y tooling determinista
de desarrollo que permita comprobar candidate binding, trazabilidad y resultados
de validación sin modificar el runtime cognitivo ni el modelo de autoridad.

---

# 3. Invariantes no negociables

RDD-M1 queda gobernado por las siguientes invariantes.

## I1 — Authority flows downward only

```text
CONTROL / AUTHORITY / PERMISSIONS / COMMANDS
                    ↓
                    ↓
                    ↓
```

El control, la autoridad, las políticas, los permisos y las solicitudes operativas
fluyen exclusivamente desde componentes upstream con autoridad hacia componentes
downstream dentro de contratos autorizados.

## I2 — Prohibición absoluta de autoescalamiento

Ningún componente, helper, script, validator, reviewer, manifest, receipt futuro,
agente o proceso downstream puede:

- elevar sus propios permisos;
- modificar sus propios permisos;
- renovar unilateralmente su autoridad;
- ampliar su scope;
- reinterpretar una autorización;
- alterar Governance;
- modificar Constitución;
- modificar Blueprint;
- modificar Kernel;
- convertir un resultado de validación en autorización.

Si cualquier diseño permite alguno de estos comportamientos:

```text
DESIGN INVALID
→ STOP
```

## I3 — Upward information carries zero authority

Los resultados pueden retornar como información:

```text
RESULTS / FINDINGS / METRICS / EVIDENCE
                    ↑
                    ↑
                    ↑
```

La dirección ascendente representa exclusivamente información observada.

Se preserva:

```text
Evidence
!= Receipt
!= Validation
!= Decision
!= Authority
```

Un `PASS` no aprueba.
Un `FAIL` no concede autoridad de corrección.
Un finding no amplía scope.
Un manifest no mergea.
Un futuro receipt no autoriza delivery.

## I4 — Candidate-bound traceability

Toda evidencia material debe poder asociarse al candidato exacto que fue evaluado.

```text
candidate changes
→ candidate identity changes
→ previous candidate-bound evidence does not certify the new candidate
→ affected evidence must be revalidated
```

## I5 — External auditability

Un auditor independiente debe poder reconstruir, utilizando artefactos preservados
y referencias reproducibles:

```text
baseline
→ scope autorizado
→ candidato
→ validaciones ejecutadas
→ resultados
→ 4R aplicable
→ findings
→ bounded correction cuando exista
→ nuevo candidato cuando exista
→ revalidación
→ resultado terminal
→ decisión humana separada
```

La auditoría no debe depender de:

- memoria conversacional del agente;
- explicación posterior del Writer;
- confianza en una afirmación del modelo;
- permanencia de la misma terminal, sesión o context window;
- acceso al mismo proveedor o modelo que produjo el cambio.

Cuando una validación sea técnicamente reproducible, un auditor externo debe poder
repetirla y llegar a la misma conclusión observable dentro de las condiciones
documentadas.

## I6 — Auditability must not justify premature infrastructure

La exigencia de trazabilidad no autoriza por sí sola introducir:

- PKI;
- firmas criptográficas;
- Merkle trees;
- hash chaining;
- database de receipts;
- distributed ledger;
- hardware attestation;
- CAS authority store;
- immutable remote store;
- lifecycle engine.

Esas capacidades permanecen fuera de alcance hasta demostrar una necesidad real y
obtener autorización independiente.

---

# 4. Cuatro preguntas obligatorias de Malāk

## 4.1 ¿Respeta el Blueprint?

Sí, condicionado al alcance definido en este documento.

RDD-M1 es tooling de construcción y evidencia. No crea dependencias nuevas dentro
del runtime ni invierte el flujo de control. Los resultados y evidencia pueden
retornar upstream únicamente como información conforme a ADR-003.

## 4.2 ¿Respeta la Constitución Cognitiva?

Sí.

RDD-M1 no participa en:

- razonamiento;
- planificación cognitiva;
- conversación;
- Memory;
- Knowledge;
- contexto conversacional;
- selección de modelo;
- inferencia.

## 4.3 ¿Respeta la Constitución de Gobernanza?

Sí.

La autoridad final permanece separada del Writer, Reviewer, Validator y de los
artefactos de evidencia.

Los únicos resultados de validación admitidos son:

```text
PASS
FAIL
INCONCLUSIVE
```

Quedan prohibidos como estados de receipt o manifest:

```text
APPROVED
AUTHORIZED
MERGED
PROMOTED
RELEASED
```

## 4.4 ¿Mantiene el Kernel simple?

Sí, como condición obligatoria:

```text
Kernel delta = 0
```

El Kernel no debe importar, conocer, consultar ni depender del tooling RDD-M1.

---

# 5. Reutilización obligatoria

RDD-M1 no crea un nuevo sistema de review.

Debe reutilizar los mecanismos ya definidos por Malāk:

```text
Candidate Identity
Risk Classification
4R
Writer / Reviewer / Validator / Authority
Bounded Correction
Correction Budget
Fix Validator
PASS / FAIL / INCONCLUSIVE
Development Gates
Development Checklist
Git commit identity
```

Queda expresamente prohibido duplicarlos bajo nuevos nombres o capas.

No se justifican y por lo tanto no deben crearse:

```text
RDDService
RDDManager
CandidateManager
ReviewEngine
ReceiptStore
ValidationService
EvidenceRegistry
AuthorityStore
ReviewOrchestrator
```

---

# 6. Componentes y artefactos nuevos justificados

Stage 1 puede introducir únicamente:

1. un contrato estructurado mínimo:

```text
MALAK-EVIDENCE-MANIFEST/v1
```

2. tooling determinista auxiliar mínimo para crear y/o verificar ese contrato;

3. tests del contrato y del candidate binding;

4. evidencia piloto generada por el propio mecanismo.

Estos elementos están justificados porque cubren una capacidad inexistente:
convertir evidencia hoy principalmente documental en evidencia estructurada,
reproducible y ligada a un candidato exacto.

El tooling no se considera un componente arquitectónico del runtime de Malāk.

---

# 7. Regla de simplicidad

RDD-M1 debe preferir la forma mínima que satisfaga el requisito.

Para Stage 1 la identidad primaria del candidato será inicialmente:

```text
repository
baseline_commit
candidate_commit
```

No se incorporarán anticipadamente:

```text
candidate tree hashing adicional
changed-path hashing obligatorio
stable payload cryptographic chaining
receipt lineage engines
stores de autoridad
```

Si Git commit identity resulta insuficiente, la insuficiencia deberá demostrarse
mediante evidencia antes de ampliar el contrato.

Dependencias nuevas objetivo:

```text
0
```

---

# 8. Alcance autorizado

## IN SCOPE

- contrato `MALAK-EVIDENCE-MANIFEST/v1`;
- candidate binding basado inicialmente en Git commit;
- validación estructural del manifest;
- detección de evidencia ligada a candidato distinto;
- referencias a scope/specification/gate;
- riesgo;
- validaciones ejecutadas;
- resultados 4R cuando correspondan;
- findings;
- correction round;
- provenance mínima de producer/validator;
- `PASS | FAIL | INCONCLUSIVE`;
- referencias de evidencia;
- auditabilidad externa reproducible cuando sea técnicamente viable;
- tests automatizados;
- dogfood sobre un candidato real;
- medición de utilidad y overhead.

## OUT OF SCOPE

- Kernel;
- Planner;
- CapabilityRegistry;
- ConversationService;
- ConversationContext;
- Memory;
- Knowledge;
- Security Control Plane;
- PDP / PEP;
- runtimes;
- providers;
- agentes;
- autonomous review;
- autonomous correction;
- auto-merge;
- delivery governance;
- branch protection;
- database;
- authority store;
- lifecycle engine;
- provider transport bindings;
- PKI;
- firmas criptográficas;
- Merkle trees;
- hash chaining;
- remote immutable storage;
- distributed ledger;
- hardware-backed attestation;
- Stage 2 receipts estables.

---

# 9. Manifest mínimo candidato

La forma exacta se cerrará en Gate 1, pero el contrato debe permanecer cercano a:

```yaml
schema: MALAK-EVIDENCE-MANIFEST/v1

repository:
baseline_commit:
candidate_commit:

unit:
specification:
gate:
risk_class:
scope_reference:

validations:
four_r:
findings:
correction_round:

producer:
validator:

result: PASS | FAIL | INCONCLUSIVE
generated_at:
evidence_references:

authority_effect: none
```

`producer` y `validator` representan provenance, no privilegios ni autoridad.

---

# 10. Cadena de auditoría requerida

La evidencia debe permitir contestar como mínimo:

```text
qué se hizo
quién o qué produjo el cambio o evidencia
sobre qué candidato
contra qué baseline
bajo qué alcance
con qué permisos previamente concedidos
qué validación se ejecutó
qué resultado produjo
qué findings existieron
qué correcciones fueron autorizadas
qué cambió después
quién validó
quién conservó la autoridad final
```

Cuando exista una secuencia:

```text
candidate A
→ FAIL
→ finding F-001
→ correction autorizada
→ candidate B
→ PASS
```

la evidencia de A debe preservarse como historia y no reescribirse para aparentar
que certificó B.

---

# 11. Gates autorizados

## G0 — Admission & Baseline Review

Objetivo:

- verificar baseline exacto;
- completar inventario y cobertura exigidos por el Construction Protocol;
- confirmar necesidad, scope, riesgos y rollback;
- comprobar ausencia de drift bloqueante.

STOP si el inventario revela conflicto normativo, solución ya existente suficiente,
drift crítico no resuelto o necesidad de ampliar el alcance autorizado.

## G1 — Evidence Contract v1

Definir el contrato mínimo sin implementar infraestructura adicional.

STOP si el contrato necesita expresar autoridad o delivery state.

## G2 — Candidate Identity Binding

Implementar la comprobación mínima basada en Git commit.

STOP si requiere modificar runtime, Kernel, seguridad o contratos cognitivos.

## G3 — Manifest Validation Tooling

Crear tooling determinista mínimo y tests.

STOP ante cualquier dependencia externa no autorizada o expansión hacia lifecycle,
stores o agentes.

## G4 — Existing-Method Binding

Representar en el manifest resultados provenientes del método existente:
4R, findings y bounded correction, sin recrear esos mecanismos.

STOP ante duplicación de responsabilidades existentes.

## G5 — Dogfood Pilot

Aplicar el mecanismo al candidato real de RDD-M1 y demostrar candidate binding,
stale evidence detection y auditabilidad.

## G6 — Closure & Utility Review

Validar suite completa, review proporcional, evidencia y overhead.

Decidir si Stage 1 queda adoptado, adaptado, observado o rechazado.

Stage 2 no se habilita automáticamente.

---

# 12. Métricas mínimas

RDD-M1 deberá medir al menos:

```text
candidate_binding_detection
stale_evidence_detection
manifest_validation_failures
manual_steps_required
new_dependencies
runtime_delta
kernel_delta
authority_effects
review_overhead
external_reconstruction_feasibility
```

Objetivos obligatorios:

```text
candidate_binding_detection = 100%
stale_evidence_detection = 100%
new_dependencies = 0
runtime_delta = 0
kernel_delta = 0
authority_effects = 0
false authority states = 0
```

---

# 13. Stop conditions globales

Detener y escalar si cualquier gate requiere:

```text
modificar Kernel
modificar Governance
modificar Blueprint
modificar Security authority
crear una Capability
introducir una database
introducir dependencia externa no autorizada
convertir evidencia en autoridad
permitir autoescalamiento
permitir self-authorization
bloquear delivery mediante un receipt
hacer auto-fix fuera de Correction Budget
hacer auto-merge
ocultar o reescribir evidencia histórica de FAIL
ampliar scope de implementación desde un finding
```

Ante evidencia insuficiente:

```text
INCONCLUSIVE
```

Nunca PASS por defecto.

---

# 14. Rollback

RDD-M1 debe ser reversible sin migración del runtime.

El rollback puede retirar:

- contrato del manifest;
- tooling auxiliar;
- tests específicos;
- integración documental asociada.

Debe dejar sin cambios funcionales:

- Kernel;
- runtime cognitivo;
- seguridad;
- conversación;
- Memory;
- Knowledge;
- estado del usuario.

La evidencia histórica ya producida puede conservarse como registro documental.

---

# 15. Definition of Done

RDD-M1 Stage 1 solo puede declararse completado cuando exista evidencia verificable
de que:

```text
[ ] las cuatro preguntas obligatorias continúan en PASS
[ ] el Kernel no fue modificado
[ ] el runtime cognitivo no fue modificado
[ ] no se introdujeron dependencias externas
[ ] existe MALAK-EVIDENCE-MANIFEST/v1
[ ] el manifest está ligado a un candidato exacto
[ ] un candidato diferente invalida la suficiencia de evidencia previa
[ ] PASS / FAIL / INCONCLUSIVE son los únicos resultados terminales
[ ] la evidencia no expresa autoridad
[ ] ningún componente puede modificar o elevar sus propios permisos
[ ] los resultados ascendentes son exclusivamente información
[ ] findings y correcciones permanecen trazables
[ ] la historia de FAIL no se reescribe ni oculta
[ ] Writer / Reviewer / Validator / Authority permanecen separados
[ ] un auditor externo puede reconstruir la cadena de validación
[ ] las validaciones reproducibles pueden repetirse cuando corresponde
[ ] candidate_binding_detection = 100%
[ ] stale_evidence_detection = 100%
[ ] authority_effects = 0
[ ] suite aplicable = PASS
[ ] compileall = PASS
[ ] git diff --check = PASS
[ ] utilidad y overhead fueron medidos
[ ] cierre y promoción posterior requieren decisión humana explícita
```

---

# 16. Frontera de autorización

La autorización vigente cubre únicamente:

```text
Stage 0
→
Stage 1

G0 → G6
```

No cubre:

```text
Stage 1
→
Stage 2
```

Ni autoriza:

- Candidate-Bound Validation Receipt estable;
- Candidate Evidence Package;
- Integrity Hardening;
- agent-produced candidates;
- governed multi-agent evaluation.

Cada promoción futura requiere necesidad demostrada, admission review y aprobación
explícita e independiente del propietario.
