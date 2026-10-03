# Malāk Construction Preflight

Versión: 0.1.0

Estado: Activo

---

# 1. Propósito

Este documento define la barrera operativa de admisión que debe ejecutarse antes
de planificar, diseñar, implementar, revisar o cerrar una unidad material de
trabajo sobre Malāk.

Su objetivo es impedir que un actor avance apoyándose en memoria conversacional,
familiaridad aparente con el proyecto, resultados históricos o inferencias
plausibles sin haber reconstruido primero el estado aplicable desde el
repositorio oficial.

El preflight existe para transformar reglas conocidas en **precondiciones
demostrables**.

No crea una nueva autoridad arquitectónica y no reemplaza:

1. Constitución Cognitiva;
2. Constitución de Gobernanza;
3. Blueprint;
4. especificaciones aprobadas;
5. ADR aceptados;
6. contratos públicos;
7. Architecture Quality Gates;
8. `SECURITY.md`;
9. `docs/development/engineering_method.md`;
10. `docs/development/malak_construction_protocol.md`.

En caso de conflicto prevalece la jerarquía documental oficial.

---

# 2. Actores alcanzados

El preflight es obligatorio, según aplicabilidad, para cualquier actor que
participe materialmente en la construcción o revisión de Malāk:

- Owner asistido por tooling;
- asistentes conversacionales;
- modelos;
- agentes de desarrollo;
- reviewers;
- validators;
- automatizaciones de ingeniería.

Incluye expresamente al asistente utilizado por el Owner en sesiones de
ChatGPT/Jarvis cuando actúa sobre el repositorio de Malāk.

La capacidad de un modelo para recordar una regla no demuestra que la haya
aplicado.

Separación:

```text
model memory
conversation context
historical conclusion
prior PR state
        !=
current repository baseline
        !=
gate evidence
        !=
authority
```

La memoria y la conversación pueden utilizarse para localizar fuentes o formular
hipótesis de búsqueda. Toda conclusión material debe reconciliarse nuevamente
con el repositorio vigente.

---

# 3. Cuándo se ejecuta

Debe ejecutarse antes de:

- seleccionar o admitir una próxima implementación;
- congelar G0/G1;
- crear o modificar una Capability, componente, contrato, agent, tool, service,
  runtime, policy boundary o superficie arquitectónica;
- implementar un cambio material;
- abrir una PR material;
- ejecutar una revisión material del candidate;
- cerrar o promover una unidad material;
- reanudar una unidad cuando cambió materialmente su baseline, scope o fuente de
  autoridad aplicable.

Una consulta factual o lectura puntual que no diseña, modifica, promueve ni
cierra trabajo material puede usar una revisión proporcional.

Si durante una tarea inicialmente acotada aparece impacto material:

```text
scope becomes material
→ Construction Preflight required
→ no seguir por inercia
```

---

# 4. Principio fail-closed

Resultado terminal permitido:

```text
PASS
FAIL
INCONCLUSIVE
```

Regla:

```text
required evidence missing
OR authority ambiguous
OR baseline unresolved
OR scope unresolved
OR applicable invariant unresolved
        ↓
INCONCLUSIVE
        ↓
STOP
```

`INCONCLUSIVE` nunca equivale a `PASS`.

El actor no puede completar silenciosamente un campo faltante utilizando
memoria, experiencia previa, una conversación anterior o una implementación que
“parece coherente”.

---

# 5. P0 — Identidad y recuperación repository-first

Debe demostrarse, según aplicabilidad:

```text
repository
baseline exact
branch / ref
owner request
work type
current candidate cuando exista
last stable checkpoint cuando aplique
```

La primera fuente de recuperación es el repositorio oficial.

Secuencia:

```text
CURRENT REPOSITORY STATE
        ↓
document authority hierarchy
        ↓
applicable architecture / governance / security / method
        ↓
current code + tests + evidence
        ↓
conversation/memory only as non-authoritative support
```

Si no puede identificarse el baseline necesario para la decisión:

```text
P0 = INCONCLUSIVE
→ STOP
```

---

# 6. P1 — Fuentes obligatorias y jerarquía

El actor debe identificar y reconciliar las fuentes que gobiernan la unidad.

Conjunto mínimo según aplicabilidad:

```text
AGENTS.md
Cognitive Constitution
Governance Constitution
Blueprint
Kernel specification
Architecture Quality Gates
SECURITY.md
accepted ADRs
applicable specifications / contracts
engineering_method.md
malak_construction_protocol.md
development_checklist.md
implementation roadmap
ideas.md
research horizon / concepts
current code
current tests
current evidence
```

Una fuente inferior no puede reinterpretar una obligación superior.

Debe quedar explícito qué fuente:

- obliga;
- restringe;
- informa;
- es histórica;
- es conceptual/no normativa;
- queda no aplicable con razón.

La lectura del preflight no sustituye el File Coverage Ledger cuando el
Construction Protocol exige cobertura exhaustiva.

---

# 7. P2 — Invariantes arquitectónicas y de gobernanza

Antes de admitir el diseño o cambio debe existir disposición explícita para los
invariantes aplicables, incluyendo como mínimo cuando corresponda:

- Human in Control;
- Kernel First;
- Capability First;
- contratos públicos;
- ausencia de bypass;
- ausencia de ciclos;
- Runtime Independence;
- mínimo privilegio;
- separación de responsabilidades;
- Zero Trust;
- límites de side effects;
- trazabilidad;
- dirección de autoridad de ADR-003.

Si una regla aplicable no puede evaluarse con la evidencia disponible:

```text
P2 = INCONCLUSIVE
→ STOP
```

---

# 8. P3 — Dirección de comunicación y autoridad

Para toda superficie que comunique componentes, delegue trabajo, transporte
evidencia o pueda afectar decisiones, debe reconciliarse explícitamente
`ADR-003 — Directional Communication and Authority Flow` y las reglas
correspondientes del Blueprint.

Semántica obligatoria:

```text
CONTROL / AUTHORITY / PERMISSIONS / POLICY / OPERATIONAL REQUESTS
Upstream
   ↓
Downstream


RESULTS / ERRORS / STATUS / METRICS / FINDINGS / EVENTS / EVIDENCE
Upstream
   ↑
Downstream

upward information authority_effect = none
```

Debe verificarse:

```text
upward control path              NONE
authority self-elevation         NONE
hidden command through event     NONE
layer bypass                     NONE
control/authority cycle          NONE
downstream policy mutation       NONE
result interpreted as authority  NONE
```

Una necesidad de información o validación administrada upstream no autoriza al
componente downstream a controlar esa capa. Debe utilizar el contrato, broker,
policy service, request tipado u orquestación aprobada.

Si la topología de autoridad no es clara:

```text
P3 = INCONCLUSIVE
→ redesign or clarify
→ no implementation
```

Este control no prohíbe el retorno ascendente de resultados o evidencia.

---

# 9. P4 — Necesidad, reutilización y complejidad

Antes de aceptar una superficie nueva deben ejecutarse los controles definidos
por `AGENTS.md` y el Construction Protocol:

```text
Component / Logic Reuse Review
        ↓
REUSE | ADAPT | COMPOSE | NEW
        ↓
Necessity & Complexity Review
        ↓
NEW Component Justification cuando corresponda
```

Un componente nuevo no es admisible sólo porque sea técnicamente viable.

Cuando `NEW` no pueda demostrarse:

```text
NEW
→ NOT ADMISSIBLE
→ REUSE / ADAPT / COMPOSE o STOP
```

El preflight registra el resultado; no reemplaza la evidencia detallada exigida
por el proceso correspondiente.

---

# 10. P5 — Riesgo y profundidad de revisión

Antes de implementación o PR material debe declararse:

```text
risk_class
risk_rationale
critical_contract              YES | NO
required_review_depth
Design 4R applicability
Candidate FULL 4R applicability
RDD Stage 1 applicability
independent validation needs
```

Las cuatro lentes deben recibir disposición explícita:

```text
Risk
Readability
Reliability
Resilience
```

La proporcionalidad modifica profundidad, no permite omisión silenciosa.

Para contratos críticos debe preservarse la secuencia canónica de
`malak_construction_protocol.md §5.5`.

El preflight no replica esa secuencia.

---

# 11. P6 — Scope y Candidate Identity

Antes de una modificación material debe existir:

```text
baseline                      EXACT
scope                         FROZEN
allowed files/components      DECLARED cuando corresponda
forbidden/out-of-scope        DECLARED
candidate identity strategy   DEFINED
stop conditions               DEFINED
rollback/checkpoint           DEFINED cuando corresponda
```

Un cambio posterior de scope no se absorbe silenciosamente.

```text
new need discovered
→ record
→ separate admission/gate
→ no implicit scope expansion
```

---

# 12. P7 — Registro de resultado

El preflight debe producir evidencia mínima equivalente a:

```text
preflight_version
repository
baseline
work_unit
work_type
owner_instruction
sources_reconciled
applicable_adrs
architecture_invariants
authority_flow_disposition
reuse_disposition
necessity_disposition
risk_class
critical_contract
4R_profile
RDD_stage_1_applicability
scope_status
candidate_identity_strategy
findings
result
reason
authority_effect
```

Reglas:

```text
authority_effect = none
result = PASS | FAIL | INCONCLUSIVE
```

No es obligatorio crear un archivo nuevo para cada ejecución si la misma
evidencia queda trazable en un design record, admission review, PR body o
artefacto equivalente.

---

# 13. Condición de PASS

`PASS` sólo significa:

> existe evidencia suficiente para entrar al gate o flujo de construcción que
> corresponda.

No significa:

```text
design approved
implementation authorized beyond current scope
tests passed
4R passed
RDD conformance passed
candidate accepted
Ready authorized
merge authorized
```

Separación obligatoria:

```text
Construction Preflight PASS
!= G0/G1 PASS
!= RED
!= GREEN
!= Design 4R PASS
!= Candidate FULL 4R PASS
!= RDD Stage 1 Candidate Conformance PASS
!= E2E / CI PASS
!= human review
!= Owner Ready
!= Owner Merge
```

---

# 14. Invalidación y revalidación

Debe revalidarse la parte afectada del preflight cuando cambie materialmente:

- baseline;
- branch/ref;
- scope;
- componente o responsabilidad objetivo;
- fuente normativa o ADR aplicable;
- clasificación de riesgo;
- clasificación de contrato crítico;
- estrategia de Candidate Identity;
- una evidencia que sostenía un PASS.

No debe repetirse trabajo no afectado sin razón. La revalidación es
proporcional al cambio y debe conservar trazabilidad.

---

# 15. Regla para asistentes y agentes

Cuando un asistente o agente reciba una instrucción como:

```text
revisa Malāk y avancemos
continuemos con la implementación
sigamos con el próximo componente
retoma el trabajo anterior
```

no debe interpretar la continuidad conversacional como prueba de estado.

Debe:

```text
recover current repository state
        ↓
execute/revalidate Construction Preflight
        ↓
identify exact applicable gate
        ↓
only then propose or perform the authorized next action
```

El Owner no necesita reiterar en cada sesión:

- repository-first;
- jerarquía documental;
- Human in Control;
- Capability First / Kernel First;
- ADR-003;
- reutilización y necesidad;
- clasificación de riesgo;
- 4R;
- RDD Stage 1;
- scope freeze;
- Candidate Identity;
- STOP ante evidencia insuficiente.

Estas obligaciones nacen del repositorio y deben aplicarse automáticamente.

---

# 16. Relación con el flujo canónico

Este documento responde:

> ¿Existe evidencia suficiente y reconciliada para entrar correctamente al
> proceso?

El Construction Protocol responde:

> ¿Cuál es la secuencia obligatoria una vez admitida la unidad?

El Engineering Method responde:

> ¿Cómo se especifica, prueba, revisa, corrige y valida el cambio?

El Development Checklist responde:

> ¿Qué condiciones deben demostrarse antes de considerar completo el trabajo?

Ninguno sustituye a los demás.

Regla final:

```text
known rule != enforced rule

therefore:

material Malāk work
→ repository-first preflight
→ fail-closed admission
→ canonical construction flow
→ candidate-bound evidence
→ human authority
```
