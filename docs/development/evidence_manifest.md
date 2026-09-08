---
title: Malāk Evidence Manifest v1
status: experimental
authority: contrato operativo de desarrollo
version: 1
schema_id: MALAK-EVIDENCE-MANIFEST/v1
unit: RDD-M1
as_of_date: 2026-09-08
language: es
---

# Malāk Evidence Manifest v1

## 1. Propósito

`MALAK-EVIDENCE-MANIFEST/v1` es el contrato estructurado mínimo para ligar
evidencia de construcción y validación al candidato exacto evaluado.

El manifest implementa Stage 1 del perfil RDD progresivo de Malāk.

No es:

- un receipt de Stage 2;
- una decisión de aceptación;
- una autorización;
- un mecanismo de merge;
- un store;
- un registro de autoridad;
- una fuente de permisos;
- un componente del runtime cognitivo.

Invariante:

```text
Evidence != Receipt != Validation != Decision != Authority
```

---

# 2. Frontera de autoridad

El manifest solo puede describir evidencia observada.

```text
CONTROL / AUTHORITY / PERMISSIONS / COMMANDS
                    ↓

RESULTS / FINDINGS / METRICS / EVIDENCE
                    ↑
```

La flecha ascendente transporta información con efecto de autoridad igual a cero.

El campo obligatorio:

```json
"authority_effect": "none"
```

es una afirmación contractual verificable y no una concesión de autoridad.

Cualquier valor distinto vuelve inválido el manifest.

Quedan prohibidos como campos, resultados o semántica del contrato:

```text
approved
authorized
merged
promoted
released
authority_granted
permission_elevated
```

---

# 3. Identidad de candidato

La identidad primaria de Stage 1 es deliberadamente simple:

```text
repository
baseline_commit
candidate_commit
```

Para v1:

```text
repository = Aranwill/jarvis
baseline_commit = Git commit SHA completo de 40 caracteres hexadecimales
candidate_commit = Git commit SHA completo de 40 caracteres hexadecimales
```

No se incorporan en v1:

- tree hashes adicionales;
- hashes de changed paths;
- hash chaining;
- firmas;
- Merkle trees;
- attestation externa.

Principio:

```text
candidate changes
→ candidate_commit changes
→ previous manifest does not certify the new candidate
→ affected evidence must be revalidated
```

Un manifest histórico puede seguir siendo válido como evidencia de su candidato
original aunque `HEAD` haya avanzado. Por eso se distingue:

```text
structurally valid historical manifest
```

de:

```text
manifest bound to current HEAD
```

---

# 4. Forma canónica v1

El objeto JSON de nivel superior debe contener exactamente las claves siguientes:

```json
{
  "schema": "MALAK-EVIDENCE-MANIFEST/v1",
  "repository": "Aranwill/jarvis",
  "baseline_commit": "0000000000000000000000000000000000000000",
  "candidate_commit": "1111111111111111111111111111111111111111",
  "unit_id": "RDD-M1",
  "specification_reference": "docs/project/sprints/proposals/RDD-M1-CANDIDATE-BOUND-EVIDENCE-FOUNDATION.md",
  "gate": "G5",
  "risk_class": 3,
  "scope_reference": "docs/project/sprints/proposals/RDD-M1-CANDIDATE-BOUND-EVIDENCE-FOUNDATION.md",
  "validations": [
    {
      "id": "pytest",
      "method": "python -m pytest",
      "result": "PASS",
      "evidence_reference": "PR#64"
    }
  ],
  "four_r": {
    "risk": {
      "result": "PASS",
      "finding_refs": [],
      "evidence_reference": "PR#64"
    },
    "readability": {
      "result": "PASS",
      "finding_refs": [],
      "evidence_reference": "PR#64"
    },
    "reliability": {
      "result": "PASS",
      "finding_refs": [],
      "evidence_reference": "PR#64"
    },
    "resilience": {
      "result": "PASS",
      "finding_refs": [],
      "evidence_reference": "PR#64"
    }
  },
  "finding_refs": [],
  "correction_round": 0,
  "producer": "writer-identity",
  "validator": "validator-identity",
  "result": "PASS",
  "generated_at": "2026-09-08T18:00:00+00:00",
  "evidence_references": [
    "PR#64"
  ],
  "authority_effect": "none"
}
```

Los SHA del ejemplo son placeholders y no constituyen candidatos reales.

---

# 5. Reglas de campos

## `schema`

Valor exacto:

```text
MALAK-EVIDENCE-MANIFEST/v1
```

## `repository`

Stage 1 se limita a:

```text
Aranwill/jarvis
```

La generalización multi-repositorio queda fuera de alcance hasta demostrar
necesidad.

## `baseline_commit`

Commit exacto desde el cual parte la unidad o candidato.

Debe ser SHA Git hexadecimal completo de 40 caracteres.

## `candidate_commit`

Commit exacto cuyo contenido fue evaluado.

Debe ser SHA Git hexadecimal completo de 40 caracteres.

## `unit_id`

Identificador no vacío de la unidad autorizada.

Ejemplo:

```text
RDD-M1
```

## `specification_reference`

Referencia no vacía a la especificación o admission record que define el
comportamiento esperado y sus criterios verificables.

No concede autoridad.

## `gate`

Gate al que corresponde la evidencia.

El valor es provenance operacional; no autoriza avanzar al gate siguiente.

## `risk_class`

Entero entre `0` y `4`, conforme al Engineering Method vigente.

## `scope_reference`

Referencia no vacía al alcance previamente autorizado.

El manifest no puede ampliar ese alcance.

## `validations`

Lista no vacía de validaciones relevantes para la conclusión terminal.

Cada entrada contiene exactamente:

```text
id
method
result
evidence_reference
```

`method` debe permitir identificar o reproducir la validación cuando sea
técnicamente viable.

No se deben almacenar secretos, tokens, credenciales ni argumentos sensibles en
`method` o `evidence_reference`.

## `four_r`

Objeto cuyas únicas claves posibles son:

```text
risk
readability
reliability
resilience
```

Cada lente presente contiene exactamente:

```text
result
finding_refs
evidence_reference
```

Reglas proporcionales:

```text
risk_class = 0
  → 4R puede estar vacío

risk_class = 1 o 2
  → al menos un lente debe estar registrado

risk_class = 3 o 4
  → Risk + Readability + Reliability + Resilience obligatorios
```

La presencia de más lentes por escalamiento dinámico es válida.

## `finding_refs`

Lista de identificadores o referencias de findings preservados.

El detalle del finding puede vivir en la ficha de unidad, PR o evidencia
referenciada. El manifest no crea un segundo finding store.

## `correction_round`

Entero mayor o igual a cero.

```text
0 = candidato sin bounded correction previa
1+ = candidato posterior a una o más rondas autorizadas
```

No concede permiso para iniciar una corrección.

## `producer`

Provenance no vacía del actor que produjo el candidato o consolidó su evidencia.

No representa authority.

## `validator`

Provenance no vacía del actor que realizó la validación terminal registrada.

El contrato no pretende demostrar por sí mismo independencia de identidad; esa
separación continúa siendo una obligación del Engineering Method y debe ser
auditable mediante evidencia externa.

## `result`

Únicamente:

```text
PASS
FAIL
INCONCLUSIVE
```

## `generated_at`

Timestamp ISO-8601 timezone-aware en UTC.

## `evidence_references`

Lista no vacía de referencias necesarias para reconstruir la conclusión.

Las referencias deben preservar provenance y no depender exclusivamente de una
explicación narrativa del Writer.

## `authority_effect`

Valor exacto:

```text
none
```

---

# 6. Semántica de resultados

Los únicos estados de evidencia terminal son:

```text
PASS
FAIL
INCONCLUSIVE
```

El resultado de nivel superior debe ser consistente con todas las validaciones y
lentes 4R registrados.

Agregación v1:

```text
si cualquier validation o 4R lens = FAIL
→ result = FAIL

si no existe FAIL y cualquier validation o 4R lens = INCONCLUSIVE
→ result = INCONCLUSIVE

si todas las validation y todos los 4R lens registrados = PASS
→ result = PASS
```

El tooling debe rechazar un manifest cuyo `result` contradiga esta agregación.

Esto evita que un productor transforme manualmente evidencia roja o inconclusa
en un `PASS` terminal.

Los findings no introducen un segundo algoritmo de agregación. Todo finding que
impida aceptación deberá reflejarse en la validación o lente correspondiente.

---

# 7. Validación estructural vs candidate binding

El tooling de Stage 1 debe distinguir dos preguntas.

## 7.1 ¿El manifest es estructuralmente válido?

Comprueba:

- schema;
- claves exactas;
- tipos;
- enums;
- SHA syntax;
- UTC timestamp;
- reglas 4R proporcionales;
- agregación del resultado;
- `authority_effect = none`.

## 7.2 ¿El manifest corresponde al candidato que quiero comprobar?

El auditor puede comprobar:

```text
manifest.candidate_commit == expected candidate
```

Cuando se solicita comprobar contra el `HEAD` actual:

```text
manifest.candidate_commit == git rev-parse HEAD
```

Si no coinciden:

```text
binding diagnostic = STALE_CANDIDATE
```

`STALE_CANDIDATE` es un diagnóstico del tooling, no un resultado permitido del
manifest.

Un manifest histórico no se reescribe porque `HEAD` haya cambiado.

---

# 8. Existencia Git

Cuando exista acceso al repositorio, el validator debe comprobar que:

```text
baseline_commit
candidate_commit
```

resuelven a commits Git existentes.

La ausencia de acceso suficiente no debe inventar un PASS.

Cuando la comprobación requerida no pueda realizarse:

```text
INCONCLUSIVE / diagnostic explícito
```

según el contexto de validación.

---

# 9. Auditabilidad externa

Un auditor independiente debe poder partir del manifest y responder:

```text
qué unidad se evaluó
qué alcance aplicaba
qué baseline se utilizó
qué commit fue el candidato
qué riesgo tenía
qué validaciones se ejecutaron
qué lentes 4R se aplicaron
qué findings existieron
cuántas correcciones ocurrieron
quién produjo
quién validó
qué evidencia respalda cada resultado
cuál fue el resultado terminal
```

El auditor no debe necesitar:

- memoria conversacional del Writer;
- chain-of-thought;
- la misma sesión;
- el mismo modelo;
- el mismo proveedor;
- una afirmación no verificable del productor.

Chain-of-thought no es evidencia canónica de RDD-M1.

---

# 10. Separación de dominios

Este contrato no reutiliza como dependencia:

```text
src/malak/security/audit.py
src/malak/observability/**
```

porque esos componentes pertenecen al comportamiento operacional del producto.

Tampoco depende de:

```text
Aranwill/malak-vault-sync-agent
```

El Sync Agent es downstream y derivado.

Se pueden adaptar patrones deterministas observados allí, pero Malāk no adquiere
dependencia funcional sobre el agente.

---

# 11. Ubicaciones de Stage 1

Para evitar nuevas familias documentales y `COVERAGE_DRIFT` innecesario:

```text
contract
  docs/development/evidence_manifest.md

helper
  scripts/malak_evidence.py

tests
  tests/test_malak_evidence.py

pilot manifest
  docs/project/sprints/proposals/RDD-M1-EVIDENCE-MANIFEST.json
```

No se crea `docs/project/evidence/**` en Stage 1.

---

# 12. Fuera de alcance del contrato v1

```text
receipt_id
manifest registry
receipt store
authority store
database
signatures
PKI
Merkle trees
hash chaining
CAS
remote immutable storage
provider binding
agent identity protocol
automatic correction
automatic approval
automatic merge
delivery enforcement
multi-repository generic schema
```

Cualquier necesidad futura para estos elementos requiere evidencia y admisión
separadas.

---

# 13. Criterios de aceptación G1

```text
[PASS] contrato candidate-bound explícito
[PASS] resultados limitados a PASS / FAIL / INCONCLUSIVE
[PASS] authority_effect fijado a none
[PASS] estados de delivery/authority prohibidos
[PASS] reglas 4R proporcionales preservadas
[PASS] provenance mínima preservada
[PASS] external auditability preservada
[PASS] historical evidence no se reescribe por cambio de HEAD
[PASS] no dependencia sobre runtime audit/observability
[PASS] no dependencia sobre Sync Agent
[PASS] new dependencies = 0
[PASS] Kernel delta = 0
[PASS] runtime delta = 0
```

```text
G1 RESULT = PASS
AUTHORIZED NEXT = G2 — Candidate Identity Binding
```

Este resultado no autoriza Stage 2 ni concede autoridad de aceptación al
manifest.
