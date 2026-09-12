---
title: Episodic Candidate Content Identity Boundary — G2 Implementation Candidate Specification
status: g2_candidate_specification
authority: owner-authorized scope freeze
as_of_date: 2026-09-12
unit: Episodic Candidate Content Identity Boundary
gate: G2-SPEC
source_baseline: 5577c9b23de32bc914505bababe3576346dae4b3
source_design: docs/project/sprints/proposals/EPISODIC-CANDIDATE-CONTENT-IDENTITY-G0-G1-DESIGN.md
risk_class: 3
admission_disposition: ADOPT
scope_adaptation: current CI baseline is Ubuntu + Windows; macOS evidence is not claimed by this unit
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
g2_spec_authorized: true
implementation_authorized: false
persistent_memory_authorized: false
persistence_authorization_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
runtime_wiring_authorized: false
kernel_change_authorized: false
security_control_plane_change_authorized: false
language: es
---

# Episodic Candidate Content Identity Boundary — G2 Implementation Candidate Specification

## 1. Estado de autoridad

El Owner aprobó avanzar desde el diseño G0/G1 de `Episodic Candidate Content
Identity Boundary` hacia **G2-SPEC exclusivamente** sobre el baseline:

```text
Aranwill/jarvis
main
5577c9b23de32bc914505bababe3576346dae4b3
```

La disposición de admisión es:

```text
ADOPT
```

con una única adaptación de envelope de validación documentada en esta spec:

```text
historical G1 validation envelope: Ubuntu + Windows + macOS
current repository CI baseline:     Ubuntu + Windows
G2-SPEC requirement:                Ubuntu + Windows
macOS evidence claimed by G2:       NO
```

Esta autorización permite congelar el contrato candidato y preparar una futura
implementación mínima. **No autoriza código productivo ni tests todavía.**

Separaciones obligatorias:

```text
Specification != Implementation
Content identity != source authenticity
Content integrity != source trust
Content integrity != truth
Content integrity != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored Memory
Digest != Authority
Evidence != Authority
```

---

## 2. Problema exacto que resuelve G2

El baseline actual utiliza `candidate_id` como binding estructural a través de la
cadena episódica. Ese binding permite correlación lógica, pero no demuestra que
dos objetos con el mismo ID tengan el mismo contenido material.

El residual se expresa como:

```text
same candidate_id
!=
same EpisodicMemoryCandidate content
```

G2 congela una frontera que responde únicamente:

> ¿el `EpisodicMemoryCandidate` suministrado tiene exactamente el mismo contenido
> estructurado que el contenido representado por esta identidad sidecar?

No responde:

```text
is the source authentic?
is the content true?
is the content trusted?
should Admission return ELIGIBLE?
may this content be persisted?
may this content be retrieved?
```

---

## 3. Baseline material observado

`EpisodicMemoryCandidate` continúa materialmente compuesto por:

```text
candidate_id
origin
experience
control
created_at
```

La cadena episódica existente continúa utilizando `candidate_id` como binding en
fronteras posteriores, incluyendo governed projection y consumption.

La revisión de admisión previa a esta spec verificó además que los módulos
productivos de la cadena episódica no cambiaron materialmente desde el baseline
G0/G1 que originó este diseño.

Los desarrollos posteriores reforzaron, y no eliminaron, la necesidad de separar:

```text
candidate content identity
content identity propagation
persistence authorization
```

Por tanto, este G2 no reabre Admission, provenance, producer authorization,
projection ni consumption. Solo agrega una futura identidad sidecar pura.

---

## 4. Scope freeze

### 4.1. Archivos de futura implementación autorizables

Si un gate posterior autoriza implementación, el file budget queda congelado en:

```text
NEW  src/malak/memory/candidate_content_identity.py
NEW  tests/test_candidate_content_identity.py
```

### 4.2. Archivos que NO deben modificarse por esta unidad

```text
src/malak/memory/__init__.py
src/malak/memory/episodic_admission.py
src/malak/memory/assessment_provenance.py
src/malak/memory/assessment_producer_authorization.py
src/malak/memory/governed_input_projection.py
src/malak/memory/governed_projection_consumption.py
src/malak/security/**
src/malak/kernel/**
src/malak/services/**
src/malak/capabilities/**
```

Modificar cualquiera de esas superficies exige STOP y nuevo análisis de alcance.

### 4.3. Dependencias

```text
external dependencies added = 0
```

La futura implementación deberá utilizar solamente Python stdlib y contratos ya
existentes.

---

## 5. Arquitectura congelada

La frontera futura será aditiva, pura y específica del dominio episódico:

```text
EpisodicMemoryCandidate
        ↓
explicit canonical payload v1
        ↓
canonical JSON bytes v1
        ↓
Malāk domain separation
        ↓
SHA-256
        ↓
EpisodicCandidateContentIdentity
```

Verificación:

```text
EpisodicMemoryCandidate
+
EpisodicCandidateContentIdentity
        ↓
recompute current v1 identity
        ↓
MATCH | MISMATCH
```

No existe en este scope:

```text
UniversalIntegrityManager
registry global
filesystem store
database
network call
secret key
HMAC
PKI
signature
nonce
replay cache
persistence
retrieval
runtime wiring
```

---

## 6. API pública candidata congelada

La futura implementación deberá exponer desde el módulo explícito
`malak.memory.candidate_content_identity` una API equivalente a:

```python
CANDIDATE_CONTENT_IDENTITY_POLICY_VERSION = (
    "episodic-candidate-content-identity/v1"
)
CANDIDATE_CONTENT_CANONICALIZATION_VERSION = (
    "episodic-memory-candidate-json/v1"
)
CANDIDATE_CONTENT_DIGEST_ALGORITHM = "sha256"
CANDIDATE_CONTENT_DOMAIN_SEPARATOR = (
    "MALAK:EPISODIC_CANDIDATE_CONTENT_IDENTITY:v1\n"
)

@dataclass(frozen=True, slots=True)
class EpisodicCandidateContentIdentity:
    candidate_id: str
    digest_algorithm: str
    digest_hex: str
    canonicalization_version: str
    policy_version: str

class CandidateContentIdentityVerification(StrEnum):
    MATCH = "match"
    MISMATCH = "mismatch"

def compute_episodic_candidate_content_identity(
    candidate: EpisodicMemoryCandidate,
) -> EpisodicCandidateContentIdentity:
    ...

def verify_episodic_candidate_content_identity(
    candidate: EpisodicMemoryCandidate,
    identity: EpisodicCandidateContentIdentity,
) -> CandidateContentIdentityVerification:
    ...
```

Los nombres anteriores quedan congelados para G2 salvo finding demostrado antes
de implementación.

El módulo no se reexportará inicialmente desde `malak.memory.__init__`; el import
explícito mantiene el file budget aditivo y evita ampliar superficie pública sin
necesidad demostrada.

---

## 7. Semántica del sidecar

`EpisodicCandidateContentIdentity` es evidencia estructural de contenido.

Sus campos significan:

```text
candidate_id
    correlación lógica conservada desde el candidate

digest_algorithm
    nombre textual del algoritmo usado para digest

digest_hex
    digest hexadecimal lowercase del byte stream canónico

canonicalization_version
    versión exacta del protocolo de canonicalización

policy_version
    versión exacta de esta frontera de identidad
```

No deberá incluir:

```text
computed_at
trusted
verified_source
authorized
eligible
persistable
retrievable
```

porque cualquiera de esos campos introduciría semántica no perteneciente a esta
unidad o rompería determinismo.

---

## 8. Validación del sidecar

La futura dataclass deberá ser inmutable (`frozen=True`, `slots=True`) y validar:

- todos los campos son `str`;
- `candidate_id` no es vacío ni tiene whitespace periférico;
- `digest_algorithm`, `canonicalization_version` y `policy_version` no son vacíos;
- `digest_hex` no es vacío;
- `digest_hex` contiene únicamente `[0-9a-f]`.

La dataclass **no** debe convertir automáticamente algoritmo/versiones desconocidos
en error de construcción. Esa decisión permite que la verificación trate de
forma fail-closed identidades incompatibles como `MISMATCH`.

La función de compute v1 siempre deberá producir exactamente:

```text
digest_algorithm         = "sha256"
canonicalization_version = "episodic-memory-candidate-json/v1"
policy_version            = "episodic-candidate-content-identity/v1"
digest_hex length         = 64
```

---

## 9. Payload material v1

La identidad cubre exactamente estos 17 campos materiales:

```text
01 candidate_id
02 origin.session_id
03 origin.request_id
04 origin.request_created_at
05 origin.provider
06 origin.model
07 experience.user_content
08 experience.assistant_content
09 control.subject_scope
10 control.domain
11 control.purpose
12 control.source_authority_classification
13 control.confidence_classification
14 control.sensitivity_classification
15 control.valid_from
16 control.valid_until
17 created_at
```

La representación primitiva previa a JSON queda congelada como:

```text
{
  "schema": "malak.episodic_memory_candidate/v1",
  "candidate_id": <string>,
  "origin": {
    "session_id": <string>,
    "request_id": <string>,
    "request_created_at": <timestamp-v1>,
    "provider": <string|null>,
    "model": <string|null>
  },
  "experience": {
    "user_content": <string>,
    "assistant_content": <string>
  },
  "control": {
    "subject_scope": <string>,
    "domain": <string>,
    "purpose": <string>,
    "source_authority_classification": <string|null>,
    "confidence_classification": <string|null>,
    "sensitivity_classification": <string|null>,
    "valid_from": <timestamp-v1|null>,
    "valid_until": <timestamp-v1|null>
  },
  "created_at": <timestamp-v1>
}
```

`schema` es metadata de domain typing del protocolo; no es un campo mutable del
candidate. Su valor v1 es constante.

---

## 10. Canonicalización JSON v1

### 10.1. Regla de construcción

La futura implementación deberá construir el payload primitivamente y de forma
explícita. Queda prohibido usar serialización automática de la dataclass completa.

Prohibido:

```text
repr(candidate)
str(candidate)
asdict(candidate) como contrato de wire format
pickle
hash(candidate)
vars(candidate) como wire contract
serialización implícita de objetos Python
```

### 10.2. Regla de serialización

El JSON canónico v1 será semánticamente equivalente a:

```python
json.dumps(
    payload,
    ensure_ascii=True,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False,
)
```

seguido por:

```python
canonical_json.encode("utf-8")
```

Propiedades congeladas:

```text
encoding              UTF-8
ASCII escaping        enabled
object key order      ascending lexicographic order
whitespace            none outside JSON string content
separator object      ':'
separator array       ','
trailing newline      none
Unicode normalization none
strip                 none
casefold              none
locale dependency     none
```

`ensure_ascii=True` es parte del protocolo v1. No representa normalización de
contenido: conserva code points diferentes como representaciones JSON diferentes,
incluyendo formas Unicode canónicamente equivalentes pero materialmente distintas.

### 10.3. `None`

Los opcionales `None` se serializan como JSON:

```text
null
```

Por tanto:

```text
None != ""
```

### 10.4. Strings vacíos

`experience.user_content` y `experience.assistant_content` pueden ser strings
vacíos porque el contrato actual los permite. Deben permanecer `""` y no
convertirse a `null` ni omitirse.

---

## 11. Timestamp v1

Todo `datetime` material del candidate ya debe ser UTC por contrato de
`episodic_admission.py`.

La representación v1 queda congelada a:

```text
YYYY-MM-DDTHH:MM:SS.ffffffZ
```

con exactamente seis dígitos de microsegundos, incluso cuando sean cero.

Referencia de implementación equivalente:

```python
value.astimezone(timezone.utc).isoformat(
    timespec="microseconds"
).replace("+00:00", "Z")
```

Ejemplos:

```text
2026-09-12T12:00:00.000000Z
2026-09-12T12:00:01.123456Z
```

No se permiten en canonicalización:

```text
naive datetime
local timezone rendering
locale formatting
implicit omission of microseconds
Unix timestamp float
```

La canonicalización no muta el candidate.

---

## 12. Domain separation v1

Antes de calcular el digest se antepone exactamente el byte sequence UTF-8 de:

```text
MALAK:EPISODIC_CANDIDATE_CONTENT_IDENTITY:v1\n
```

El `\n` anterior representa un único byte LF (`0x0A`).

El digest input exacto es:

```text
UTF8("MALAK:EPISODIC_CANDIDATE_CONTENT_IDENTITY:v1\n")
+
UTF8(canonical_json_v1)
```

No hay NUL separator, BOM, trailing LF, timestamp de cálculo, random ni nonce.

---

## 13. Digest algorithm v1

G2 confirma la selección G1:

```text
SHA-256
```

La futura implementación utilizará `hashlib.sha256` de stdlib.

Salida:

```text
64 lowercase hexadecimal characters
```

SHA-256 se utiliza aquí para identidad/integridad de contenido, no autenticidad.

```text
SHA-256 digest present
!=
authentic source
!=
trusted source
!=
authorized persistence
```

---

## 14. Semántica de compute

`compute_episodic_candidate_content_identity(candidate)` deberá:

1. exigir `candidate` como `EpisodicMemoryCandidate`;
2. construir explícitamente payload v1;
3. convertir datetimes mediante timestamp v1;
4. serializar JSON canónico v1;
5. anteponer domain separator v1;
6. calcular SHA-256;
7. devolver un sidecar inmutable con metadata v1.

La función será:

```text
pure
deterministic
side-effect free
I/O free
network free
filesystem free
clock free
random free
```

No deberá leer `POLICY_VERSION` de Admission como autoridad implícita. Esta unidad
tiene su propio `policy_version` porque Admission y Content Identity son fronteras
diferentes.

---

## 15. Semántica de verify

`verify_episodic_candidate_content_identity(candidate, identity)` deberá exigir
tipos válidos y devolver solamente:

```text
MATCH
MISMATCH
```

Orden fail-closed recomendado:

```text
identity.candidate_id != candidate.candidate_id
    -> MISMATCH

identity.digest_algorithm != "sha256"
    -> MISMATCH

identity.canonicalization_version != "episodic-memory-candidate-json/v1"
    -> MISMATCH

identity.policy_version != "episodic-candidate-content-identity/v1"
    -> MISMATCH

recomputed.digest_hex != identity.digest_hex
    -> MISMATCH

otherwise
    -> MATCH
```

`MISMATCH` no debe convertirse dentro de esta función en:

```text
Admission REJECT
Admission HOLD
security DENY
persistence DENY
quarantine
incident
```

Esas decisiones pertenecen a futuros consumers con gates propios.

---

## 16. Exact test vectors v1

Los siguientes vectores quedan normativos para una futura implementación. Un
mismatch de estos valores es STOP, no un test que deba actualizarse para hacer
pasar la implementación.

### 16.1. Vector A — campos completos + Unicode

Entrada material:

```text
candidate_id = candidate-001
origin.session_id = session-001
origin.request_id = request-001
origin.request_created_at = 2026-09-12T12:00:00.000000Z
origin.provider = ollama
origin.model = qwen3:8b
experience.user_content = Hola Malāk
experience.assistant_content = Hola. ¿En qué puedo ayudarte?
control.subject_scope = conversation
control.domain = general
control.purpose = episodic_memory_candidate
control.source_authority_classification = user_asserted
control.confidence_classification = observed
control.sensitivity_classification = internal
control.valid_from = 2026-09-12T12:00:00.000000Z
control.valid_until = 2026-09-13T12:00:00.000000Z
created_at = 2026-09-12T12:00:01.123456Z
```

Canonical JSON v1 exacto:

```json
{"candidate_id":"candidate-001","control":{"confidence_classification":"observed","domain":"general","purpose":"episodic_memory_candidate","sensitivity_classification":"internal","source_authority_classification":"user_asserted","subject_scope":"conversation","valid_from":"2026-09-12T12:00:00.000000Z","valid_until":"2026-09-13T12:00:00.000000Z"},"created_at":"2026-09-12T12:00:01.123456Z","experience":{"assistant_content":"Hola. \u00bfEn qu\u00e9 puedo ayudarte?","user_content":"Hola Mal\u0101k"},"origin":{"model":"qwen3:8b","provider":"ollama","request_created_at":"2026-09-12T12:00:00.000000Z","request_id":"request-001","session_id":"session-001"},"schema":"malak.episodic_memory_candidate/v1"}
```

Expected SHA-256:

```text
d1f3634721a53840b93c62c1331be335cd1d793a115c449c41e614b0ae2799e4
```

### 16.2. Vector B — opcionales `None` + contents vacíos

Entrada material:

```text
candidate_id = candidate-002
origin.session_id = session-002
origin.request_id = request-002
origin.request_created_at = 2026-09-12T00:00:00.000000Z
origin.provider = None
origin.model = None
experience.user_content = ""
experience.assistant_content = ""
control.subject_scope = session
control.domain = test
control.purpose = identity_vector
control.source_authority_classification = None
control.confidence_classification = None
control.sensitivity_classification = None
control.valid_from = None
control.valid_until = None
created_at = 2026-09-12T00:00:00.000000Z
```

Expected SHA-256:

```text
101e9168491febb2ba9d45244b911971ed154ea414cce4f272ff8e72f245aeb2
```

### 16.3. Vector C — Unicode compuesto vs descompuesto

C1 parte **exactamente del Vector B** y modifica únicamente:

```text
candidate_id = candidate-unicode
experience.user_content = U+00E9  # é
```

Expected SHA-256:

```text
ea2f7d8c891cacd28eac11bebd5ad1c9c39c9601e7f88ab075f46def9dcb80d9
```

C2 parte exactamente de C1 y modifica únicamente:

```text
experience.user_content = U+0065 U+0301  # e + combining acute
```

Expected SHA-256:

```text
6b3b89a8c33fbdacbdeed4eeea45768948fb9aab00ec93a0d35c9a137ccda730
```

Regla demostrada:

```text
Unicode canonical equivalence
!=
content identity equivalence
```

G2 no aplica Unicode normalization.

---

## 17. TDD contract congelado

Una futura implementación deberá comenzar por tests y cubrir, como mínimo:

### 17.1. Construcción y determinismo

- mismo candidate -> misma identidad completa;
- misma identidad en recomputaciones sucesivas;
- constants v1 exactas;
- digest lowercase de 64 caracteres;
- sidecar inmutable;
- no `computed_at`;
- vector A exacto;
- vector B exacto;
- vectores C1/C2 exactos y distintos.

### 17.2. Material field mutation matrix

Debe existir cobertura que demuestre que cambiar individualmente cada uno de los
17 campos materiales cambia el digest:

```text
candidate_id
origin.session_id
origin.request_id
origin.request_created_at
origin.provider
origin.model
experience.user_content
experience.assistant_content
control.subject_scope
control.domain
control.purpose
control.source_authority_classification
control.confidence_classification
control.sensitivity_classification
control.valid_from
control.valid_until
created_at
```

Cuando un campo opcional se pruebe, deberán cubrirse al menos transiciones:

```text
None -> value
value -> different value
```

### 17.3. Distinciones estructurales

- `None != ""` donde el tipo permita ambos estados conceptualmente;
- newline dentro de content modifica digest;
- whitespace dentro de content modifica digest;
- composed Unicode != decomposed Unicode;
- microsecond difference modifica digest;
- provider/model differences modifican digest;
- control trust-sensitive metadata changes modifican digest sin adquirir trust.

### 17.4. Verification

- exact sidecar -> `MATCH`;
- mismo `candidate_id` + payload distinto -> `MISMATCH`;
- candidate ID distinto -> `MISMATCH`;
- algorithm distinto -> `MISMATCH`;
- canonicalization version distinta -> `MISMATCH`;
- policy version distinta -> `MISMATCH`;
- digest distinto -> `MISMATCH`;
- `MISMATCH` no invoca Admission ni Security.

### 17.5. Invalid API inputs

- compute con tipo incorrecto -> `TypeError`;
- verify con candidate incorrecto -> `TypeError`;
- verify con identity incorrecta -> `TypeError`;
- sidecar con strings vacíos prohibidos -> error;
- sidecar con digest fuera de lowercase hex -> error.

---

## 18. Platform validation envelope

El workflow actual de `main` valida candidate identity de Git, instala Python
3.12 y ejecuta suite, `compileall` y diff-check en:

```text
ubuntu-latest
windows-latest
```

G2 congela para esta unidad:

```text
required candidate-bound CI platforms = Ubuntu + Windows
```

No se reintroduce macOS silenciosamente dentro de Content Identity.

Si el Owner decide restaurar macOS al workflow general, será un cambio separado
con scope, evidencia y revisión propios.

Por tanto:

```text
Ubuntu PASS + Windows PASS
!=
macOS evidence
```

La futura closure debe decir explícitamente qué plataformas fueron observadas.

---

## 19. Correction Budget

El presupuesto máximo de implementación queda congelado en:

```yaml
production_files_new: 1
test_files_new: 1
existing_production_files_modified: 0
external_dependencies_added: 0

kernel_delta: 0
security_delta: 0
conversation_delta: 0
persistence_delta: 0
retrieval_delta: 0
authority_delta: 0

production_loc_guardrail: 220
test_loc_guardrail: 500
max_fix_rounds_before_escalation: 2
```

Los guardrails LOC no son objetivos a consumir. Son límites de revisión.

Exceder cualquier delta o requerir un tercer archivo funcional produce:

```text
STOP
→ explain demonstrated need
→ owner review
→ new scope decision
```

---

## 20. RDD Stage 1

Esta unidad permanece en:

```text
RDD Stage 1 — ADOPTED
RDD Stage 2 — NOT AUTHORIZED
```

Una futura implementación candidata deberá producir evidencia candidate-bound
con `MALAK-EVIDENCE-MANIFEST/v1` según el Construction Protocol.

El manifest deberá ligarse al SHA exacto evaluado y registrar como mínimo:

```text
candidate SHA
base SHA
risk class
4R evidence
pytest result
compileall result
diff-check result
platform observations
file budget observation
```

Stage 1 evidence:

```text
!= independent reviewer authority
!= independent validator authority
!= merge authority
```

---

## 21. FULL 4R requerido

Por `risk_class = 3`, la closure futura exige FULL 4R.

### 21.1. Risk

Pregunta:

> ¿puede la implementación hacer que un digest sea interpretado como trust,
> authority, Admission o Persistence Authorization?

Criterio PASS:

- API solo produce identity/verification;
- no llama Security, Admission consumers, DB o runtime;
- mismatch no produce decisiones externas;
- test vectors exactos demuestran canonicalización estable.

### 21.2. Readability

Pregunta:

> ¿puede un reviewer reconstruir exactamente los bytes hasheados sin inferir
> comportamiento implícito?

Criterio PASS:

- payload explícito;
- constants versionadas;
- timestamp format visible;
- JSON rules visibles;
- domain separator visible;
- no magic serialization.

### 21.3. Reliability

Pregunta:

> ¿produce la misma identidad para el mismo candidate entre ejecuciones y las
> plataformas soportadas por CI?

Criterio PASS:

- vectors A/B/C exactos;
- Ubuntu PASS;
- Windows PASS;
- repeated computation PASS;
- mutation matrix PASS.

### 21.4. Resilience

Pregunta:

> ¿falla de forma cerrada ante identidad alterada, metadata incompatible o
> sustitución de payload con mismo `candidate_id`?

Criterio PASS:

- todos esos casos retornan `MISMATCH`;
- no existe fallback permisivo;
- no existe downgrade de canonicalization version;
- no existe aceptación por `candidate_id` solamente.

---

## 22. Security review proporcional

Amenazas dentro de alcance:

- same-ID payload substitution;
- accidental omission of a material field;
- ambiguous `None` vs empty representation;
- timestamp representation drift;
- Unicode normalization drift;
- serializer ordering drift;
- digest metadata downgrade;
- hash interpreted as trust.

Mitigaciones:

- 17-field coverage freeze;
- explicit primitive payload;
- exact canonical JSON rules;
- exact timestamp v1;
- domain separation;
- SHA-256 stdlib;
- algorithm/version checks before MATCH;
- exact vectors;
- fail-closed `MISMATCH`.

Fuera de alcance y no resuelto:

- source authentication;
- signed provenance;
- compromised producer;
- collision-resistant signatures;
- replay protection;
- malicious but stable content;
- persistent storage integrity;
- end-to-end downstream identity propagation.

---

## 23. Reversibility y rollback

Esta unidad está diseñada para rollback trivial porque no introduce schema
persistente, migración, side effects ni modificación de contratos existentes.

Si una implementación futura debe revertirse antes de propagación:

```text
delete src/malak/memory/candidate_content_identity.py
delete tests/test_candidate_content_identity.py
revert implementing commit
```

No existe:

```text
data migration
data repair
stored hash backfill
external compatibility contract
runtime migration
```

Por tanto la reversibilidad esperada es alta mientras se mantenga este scope.

---

## 24. Stop conditions

La implementación futura deberá detenerse inmediatamente si se descubre que para
cumplir esta spec es necesario cualquiera de los siguientes cambios:

- modificar `EpisodicMemoryCandidate`;
- cambiar semántica de `candidate_id`;
- modificar Admission precedence;
- modificar provenance o producer authorization;
- modificar governed projection/consumption;
- tocar Kernel;
- tocar Security/PDP/PEP;
- introducir persistence o retrieval;
- introducir secrets, HMAC, signatures o PKI;
- agregar dependency externa;
- usar un tercer archivo funcional no previsto;
- normalizar content para hacer pasar test vectors;
- actualizar expected digest porque la implementación produce otro valor;
- aceptar identidad por `candidate_id` solamente;
- requerir content identity propagation para considerar esta unidad terminada;
- necesitar más de dos fix rounds materiales dentro del Correction Budget.

Ante cualquiera de ellos:

```text
STOP
→ preserve evidence
→ report mismatch
→ return to owner
```

---

## 25. Criterios de implementación futura PASS

Una futura implementación podrá considerarse candidata a review solamente si:

```text
file budget: PASS
TDD contract: PASS
exact vectors: PASS
17-field mutation matrix: PASS
verification fail-closed: PASS
pytest full suite: PASS
compileall src/tests/scripts: PASS
git diff --check: PASS
Ubuntu candidate-bound CI: PASS
Windows candidate-bound CI: PASS
FULL 4R: PASS
RDD Stage 1 evidence manifest: PASS
scope expansion: NONE
```

Nada de lo anterior concede merge authority automáticamente.

---

## 26. Lo que G2 completion NO autoriza

Incluso con implementación y validación completas:

```text
Candidate Content Identity G2 complete
        ↓
STOP
```

No autoriza automáticamente:

- propagar digest por assessments;
- modificar evidence contracts;
- modificar projection bindings;
- persistir episodic candidates;
- crear un Memory store;
- retrieval;
- vector database;
- Knowledge promotion;
- cambiar Security authority;
- runtime wiring.

El siguiente problema material sigue separado:

```text
Content Identity Propagation / Binding
```

porque:

```text
correctly computing a candidate digest
!=
proving downstream evidence and decisions refer to that same content
```

Solo después de diseñar y demostrar binding end-to-end suficiente puede evaluarse
un gate separado de:

```text
Persistence Authorization
```

---

## 27. Decisión G2-SPEC

```text
UNIT:
Episodic Candidate Content Identity Boundary

BASELINE:
5577c9b23de32bc914505bababe3576346dae4b3

RISK:
3 — HIGH

G0/G1:
PASS

G2-SPEC DISPOSITION:
ADOPT

CANONICALIZATION:
explicit primitive payload
+ canonical JSON v1
+ UTF-8
+ Malāk domain separator
+ SHA-256

FUTURE FILE BUDGET:
2 new files
0 existing production files modified

RDD:
Stage 1 adopted
Stage 2 not authorized

VALIDATION ENVELOPE:
Ubuntu + Windows candidate-bound
macOS not claimed

IMPLEMENTATION:
NOT AUTHORIZED BY THIS DOCUMENT

PERSISTENCE:
NOT AUTHORIZED

RETRIEVAL:
NOT AUTHORIZED

NEXT ACTION:
owner review of this G2 specification
```

La spec congela el diseño implementable. Cualquier código posterior requiere una
nueva autorización explícita del Owner.
