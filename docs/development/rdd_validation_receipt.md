
---
id: MALAK-RDD-VALIDATION-RECEIPT-V1
title: RDD Stage 2 — Candidate-Bound Validation Receipt V1
status: active
authority: contrato operativo de desarrollo
version: 1
schema_id: MALAK-RDD-VALIDATION-RECEIPT/v1
as_of_date: 2026-10-10
language: es
---

# RDD Stage 2 — Candidate-Bound Validation Receipt V1

## Propósito

`MALAK-RDD-VALIDATION-RECEIPT/v1` materializa RDD Stage 2 como un artifact de
ingeniería externo al candidate. Preserva de forma determinista la identidad del
candidate, el digest del `MALAK-EVIDENCE-MANIFEST/v1` y el resultado terminal de
`RDD Stage 1 Candidate Conformance`.

No reejecuta Stage 1, no aprueba código y no concede autoridad.

```text
Evidence != Receipt != Validation != Decision != Authority
Receipt validator PASS != Candidate Conformance PASS
Candidate Conformance PASS != Owner approval
Receipt != Ready
Receipt != Merge
authority_effect = none
```

## Aplicabilidad

```text
risk_class 0  → Stage 2 NOT_APPLICABLE
risk_class 1  → Stage 2 NOT_APPLICABLE
risk_class 2  → OPTIONAL / explicit admission only
risk_class 3  → REQUIRED
risk_class 4  → REQUIRED
```

Para riesgo 3/4, human Ready sólo es técnicamente admisible cuando existe:

```text
valid MALAK-EVIDENCE-MANIFEST/v1
+
RDD Stage 1 Candidate Conformance PASS
+
valid applicable MALAK-RDD-VALIDATION-RECEIPT/v1
```

Esto sigue sin conceder Ready ni Merge.

## Schema

El contrato exacto es el aprobado por el Design integrado en PR #266. El Receipt
contiene exactamente:

```text
schema
repository
baseline_commit
candidate_commit
candidate_tree
unit_id
risk_class
specification_reference
scope_reference
stage1_manifest_schema
stage1_manifest_digest
stage1_manifest_result
candidate_conformance_result
candidate_conformance_reference
correction_round
finding_refs
validator
independence_reference
evidence_references
issued_at
receipt_digest
authority_effect
```

No se admiten keys extra o faltantes.

## Manifest ↔ Receipt

Los campos repetidos no son overrides del caller. Deben derivarse del Manifest o
coincidir exactamente:

```text
repository
baseline_commit
candidate_commit
unit_id
risk_class
specification_reference
scope_reference
correction_round
finding_refs
stage1_manifest_schema
stage1_manifest_result
```

`candidate_tree` se deriva por Git.
`stage1_manifest_digest` se recomputa sobre el Manifest canonicalizado.

`candidate_conformance_result` pertenece al checkpoint de Candidate Conformance y
no se iguala artificialmente con `manifest.result`.

## Strict JSON e integridad

Manifest y Receipt se parsean de forma estricta antes de canonicalización:

- duplicate keys rechazadas en cualquier object;
- `NaN`, `Infinity` y `-Infinity` rechazados;
- tipos, rangos y enums exactos;
- `bool` no se acepta como integer;
- SHA Git lowercase de 40 caracteres;
- SHA-256 lowercase de 64 caracteres;
- `issued_at` usa `YYYY-MM-DDTHH:MM:SSZ`;
- `authority_effect` es exactamente `none`.

Canonicalización:

```text
UTF-8
sort_keys = true
separators = (",", ":")
ensure_ascii = false
allow_nan = false
SHA-256
```

El `receipt_digest` excluye únicamente su propio campo.

```text
SHA-256 integrity / consistency
!= producer authenticity
!= independent actor identity
!= truth of external Evidence
!= Authority
```

## Candidate binding e invalidación

```text
candidate changes
→ prior Stage 1 Evidence no certifica el nuevo candidate
→ prior Candidate Conformance no certifica el nuevo candidate
→ prior Stage 2 Receipt no es aplicable al nuevo candidate
→ affected Evidence must be revalidated
→ new Receipt required when Stage 2 applies
```

El helper admite `--expected-candidate` y `--require-current`. Git unavailable o
errores de inspección que impidan establecer identidad producen
`INCONCLUSIVE` cuando corresponde al contrato Stage 1 reutilizado.

## Output

Por defecto, `issue` emite el Receipt por stdout. La redirección de stdout queda
fuera de la garantía de confinement del helper.

Con `--output`:

- `--repo-root` puede apuntar a la raíz o a una subcarpeta del repository; el helper deriva la raíz Git efectiva mediante `git rev-parse --show-toplevel`;
- el destino debe estar fuera de esa raíz Git efectiva, no sólo fuera del path declarado por el caller;
- se usa el path resuelto, no una comparación lexical;
- aliases/symlinks hacia el repo se rechazan cuando el sistema permite resolverlos;
- no se sobrescriben inputs ni archivos existentes;
- la publicación usa archivo temporal y replace/rename después de validar.

Escribir un archivo en el worktree no cambia retroactivamente un commit Git ya
existente; puede ensuciar el worktree y un commit futuro crear otra Candidate
Identity.

## CLI

Emisión:

```text
python scripts/malak_rdd_receipt.py issue \
  --manifest <manifest.json> \
  --repo-root . \
  --candidate-conformance-result PASS \
  --candidate-conformance-reference <ref> \
  --validator <provenance> \
  --independence-reference <ref> \
  --evidence-reference <ref> \
  --issued-at 2026-10-10T15:00:00Z
```

Validación:

```text
python scripts/malak_rdd_receipt.py validate \
  --receipt <receipt.json> \
  --manifest <manifest.json> \
  --repo-root . \
  --expected-candidate <sha>
```

## Fronteras

V1 no incorpora:

- network;
- registry/store/database;
- signatures/PKI;
- hash chains/Merkle;
- runtime consumption;
- Cognitive Receipt;
- Protected Finalization;
- Persistence Authorization;
- automatic Ready/Merge;
- RDD Stage 3+.

`MALAK-RDD-VALIDATION-RECEIPT/v1` es Evidence estructurada reusable con
`authority_effect = none`.
