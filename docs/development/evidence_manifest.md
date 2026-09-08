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

## Propósito

`MALAK-EVIDENCE-MANIFEST/v1` liga evidencia de construcción al candidato exacto
evaluado. Implementa Stage 1 del perfil RDD progresivo.

No es un receipt de Stage 2, decisión, autorización, store, mecanismo de merge ni
componente del runtime.

```text
Evidence != Receipt != Validation != Decision != Authority
```

---

## Autoridad

El manifest solo describe evidencia observada.

```text
CONTROL / AUTHORITY / PERMISSIONS / COMMANDS
                    ↓

RESULTS / FINDINGS / METRICS / EVIDENCE
                    ↑
```

El retorno ascendente tiene efecto de autoridad cero.

Campo obligatorio:

```json
"authority_effect": "none"
```

Cualquier otro valor invalida el manifest. Estados o campos de authority/delivery
como `approved`, `authorized`, `merged`, `promoted` o `released` quedan fuera del
contrato v1.

---

## Candidate Identity v1

Stage 1 usa únicamente:

```text
repository = Aranwill/jarvis
baseline_commit = lowercase Git SHA de 40 caracteres
candidate_commit = lowercase Git SHA de 40 caracteres
```

Ambos commits deben existir y:

```text
baseline_commit must be ancestor of candidate_commit
```

No se añaden tree hashes, path digests, firmas, Merkle ni hash chaining.

```text
candidate changes
→ identity changes
→ previous manifest does not certify the new candidate
→ affected evidence must be revalidated
```

Un manifest histórico sigue describiendo su candidato original aunque `HEAD`
avance.

---

## Forma v1

El objeto JSON debe contener exactamente estas claves:

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
  "evidence_references": ["PR#64"],
  "authority_effect": "none"
}
```

Los SHA del ejemplo son placeholders.

---

## Reglas de validación

### Identidad y provenance

- `schema` debe ser exactamente `MALAK-EVIDENCE-MANIFEST/v1`.
- `repository` debe ser exactamente `Aranwill/jarvis`.
- `baseline_commit` y `candidate_commit` son SHA lowercase de 40 caracteres.
- `unit_id`, `specification_reference`, `gate`, `scope_reference`, `producer` y
  `validator` deben ser strings no vacíos sin whitespace periférico.
- `risk_class` es entero `0..4`.
- `correction_round` es entero `>= 0`.
- `generated_at` es ISO-8601 timezone-aware en UTC.
- `evidence_references` es una lista no vacía.

`producer` y `validator` son provenance, no permisos. La independencia real entre
roles se prueba mediante evidencia externa y el Engineering Method, no por confiar
en dos strings diferentes.

### Validations

`validations` es una lista no vacía. Cada entrada contiene exactamente:

```text
id
method
result
evidence_reference
```

`id`, `method` y `evidence_reference` no pueden estar vacíos. Los IDs de
validación son únicos dentro del manifest.

`method` debe identificar o permitir reproducir la validación cuando sea viable y
no debe contener secretos, tokens o credenciales.

### 4R proporcional

`four_r` solo admite:

```text
risk
readability
reliability
resilience
```

Cada lente contiene exactamente:

```text
result
finding_refs
evidence_reference
```

Reglas:

```text
risk_class 0     → four_r puede estar vacío
risk_class 1–2   → al menos un lente
risk_class 3–4   → FULL 4R obligatorio
```

### Resultados

El único enum permitido es:

```text
PASS
FAIL
INCONCLUSIVE
```

Agregación terminal:

```text
any validation/4R FAIL
→ FAIL

no FAIL + any INCONCLUSIVE
→ INCONCLUSIVE

all recorded validation/4R PASS
→ PASS
```

El validator debe rechazar un `result` superior que contradiga esa agregación.
Así un productor no puede convertir evidencia roja o inconclusa en PASS.

Los findings no crean un segundo algoritmo: un finding bloqueante debe quedar
reflejado en la validación o lente correspondiente.

---

## Candidate binding

El helper responde dos preguntas distintas.

### Validez histórica

Por defecto verifica:

```text
schema + fields + enums
baseline exists
candidate exists
baseline ancestor of candidate
result aggregation
```

Esto permite auditar manifests históricos sin exigir que su candidate sea el
`HEAD` actual.

### Binding contra candidato esperado

```text
--expected-candidate <SHA>
```

exige:

```text
manifest.candidate_commit == expected SHA
```

### Binding contra HEAD actual

```text
--require-current
```

exige:

```text
worktree clean
manifest.candidate_commit == git rev-parse HEAD
```

Si no coincide:

```text
STALE_CANDIDATE
```

`STALE_CANDIDATE`, `DIRTY_WORKTREE` y otros códigos son diagnósticos del helper,
no nuevos estados del manifest.

### Regla anti-recursión de identidad

El manifest activo que certifica un candidato debe existir **fuera del candidate
worktree** mientras se ejecuta la validación. Esto aplica especialmente a
`--require-current`: no se crean excepciones que ignoren archivos dirty.

```text
validate candidate A
→ manifest activo bound to A permanece externo
→ candidate A no cambia por producir su evidencia
```

Si después se preserva una copia dentro del repositorio, esa copia es únicamente
**evidencia histórica del candidato A**. El commit que incorpora esa copia es un
candidato distinto B y la copia **no certifica B ni el commit que la contiene**.
Nunca debe reinterpretarse una copia histórica como evidencia candidate-bound del
HEAD posterior.

```text
A validated
→ historical copy committed
→ HEAD becomes B
→ historical copy still describes A only
```

Cualquier certificación de B requiere evidencia ligada explícitamente a B según
las reglas normales de Candidate Identity. Stage 1 no introduce un store externo
ni infraestructura adicional para resolver esta propiedad. Un PR comment,
artefacto de una herramienta de validación o soporte equivalente puede preservar
el manifest activo siempre que sea accesible, auditable y esté ligado al SHA
exacto; su ubicación no le concede autoridad.

---

## Git y fallo cerrado

Cuando Git está disponible:

```text
missing baseline/candidate commit
→ FAIL

baseline not ancestor of candidate
→ FAIL

required binding mismatch
→ FAIL

dirty worktree with --require-current
→ FAIL
```

Si el entorno impide realizar una comprobación requerida:

```text
INCONCLUSIVE
```

Nunca `PASS` por defecto.

---

## External auditability

Desde un manifest un auditor debe poder reconstruir:

```text
unit / scope / specification
baseline / candidate
risk
validations / 4R
findings / correction round
producer / validator provenance
evidence references
terminal result
```

La reconstrucción no debe depender de memoria conversacional, chain-of-thought,
la misma sesión, modelo o proveedor.

Chain-of-thought no es evidencia canónica.

---

## Separación de dominios

RDD-M1 no depende de:

```text
src/malak/security/audit.py
src/malak/observability/**
Aranwill/malak-vault-sync-agent
```

Los dos primeros pertenecen al runtime. El Sync Agent es downstream. Se adaptan
patrones deterministas cuando aportan valor, nunca se introduce una dependencia
upstream hacia ellos.

---

## Ubicaciones Stage 1

```text
contract:       docs/development/evidence_manifest.md
helper:         scripts/malak_evidence.py
tests:          tests/test_malak_evidence.py
pilot manifest: externo al candidate durante validación;
                copia histórica opcional en docs/project/sprints/proposals/**
```

Una copia histórica in-repo conserva provenance del candidato que describe y no
certifica el commit que la contiene. No se crea `docs/project/evidence/**` ni se
modifica el Sync Agent.

---

## Fuera de alcance v1

```text
receipt_id / receipt store / manifest registry
authority store / database
signatures / PKI / Merkle / hash chaining / CAS
remote immutable storage / attestation
provider bindings / agents
automatic correction / approval / merge
delivery enforcement
multi-repository generic schema
```

---

## Criterio de aceptación G1

```text
candidate-bound contract             PASS
authority_effect = none              PASS
PASS/FAIL/INCONCLUSIVE only          PASS
4R proportionality                   PASS
result anti-greenwashing             PASS
historical auditability              PASS
runtime dependency                   0
Sync Agent dependency                0
new external dependencies            0
Kernel delta                         0
```

```text
G1 RESULT = PASS
```

G1 no autoriza Stage 2 ni convierte el manifest en autoridad.
