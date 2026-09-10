---
title: Episodic Candidate Content Identity Boundary — G0/G1 Design Record
status: g1_design_review
authority: owner-authorized design analysis
as_of_date: 2026-09-10
unit: Episodic Candidate Content Identity Boundary
gate: G1
source_baseline: 9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
risk_class: 3
vault_reconciliation_status_at_start: pass
vault_last_observed_malak_head: 9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
local_post_g3_validation_reported_by_owner: pass
canonical_derived_docs_reconciliation_required_before_g2: true
sdd_required: true
tdd_required_for_future_implementation: true
full_4r_required: true
rdd_stage_1: adopted
rdd_stage_2_authorized: false
implementation_authorized: false
g2_authorized: false
persistent_memory_authorized: false
persistence_authorization_authorized: false
retrieval_authorized: false
knowledge_implementation_authorized: false
runtime_wiring_authorized: false
sprint_7_12_authorized: false
language: es
---

# Episodic Candidate Content Identity Boundary — G0/G1 Design Record

## 1. Estado de autoridad

El Owner autorizó continuar con análisis y diseño después de integrar y validar
`Episodic Admission Governed Projection Consumption Boundary`.

Esta unidad candidata se denomina:

```text
Episodic Candidate Content Identity Boundary
```

Su responsabilidad propuesta es responder únicamente:

> ¿cómo puede Malāk demostrar de forma determinista que dos referencias a un
> `EpisodicMemoryCandidate` representan exactamente el mismo contenido
> estructurado, sin convertir integridad en trust, autenticidad, elegibilidad,
> autorización de persistencia o autoridad?

Esta autorización comprende G0/G1 exclusivamente.

No autoriza:

- código productivo;
- tests de implementación;
- G2;
- Persistence Authorization;
- Memory persistente;
- almacenamiento;
- retrieval;
- Knowledge;
- runtime wiring;
- cambios al Kernel;
- cambios al Security Control Plane;
- PKI;
- firmas digitales;
- nonce o replay protection;
- Sprint 7.12;
- RDD Stage 2;
- Ready for Review o merge sin decisión humana.

Separaciones obligatorias:

```text
Content identity != source authenticity
Content integrity != source trust
Content integrity != truth
Content integrity != Admission ELIGIBLE
Admission ELIGIBLE != Persistence Authorization
Persistence Authorization != Stored Memory
Evidence != Authority
```

---

## 2. Baseline exacto y evidencia observada

Baseline fuente congelado para este G0/G1:

```text
Aranwill/jarvis
main
9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
```

Ese commit integra PR #92 — `Episodic Admission Governed Projection Consumption Boundary`.

La cadena episódica aislada materializada es ahora:

```text
EpisodicMemoryCandidate
        ↓
AdmissionAssessment
        ↓
Assessment Provenance
        ↓
Assessment Producer Authorization
        ↓
Governed Input Projection
READY | HOLD | DENIED
        ↓
Governed Projection Consumption
BLOCKED | EVALUATED
        ↓
Episodic Admission
REJECT | HOLD | ELIGIBLE
        ↓
STOP
```

La validación candidate-bound de PR #92 concluyó PASS en Ubuntu, Windows y macOS.

El Owner reportó además validación local post-merge sobre el checkout de Malāk:

```text
HEAD: 9438c66e315faa2b4c8c3f0a99d4e1e9619992c3
pytest: 645 passed
compileall -f tests: PASS
compileall -f src tests scripts: PASS
git diff --check: PASS
working tree: clean
```

La evidencia local anterior es evidencia observada/reportada por el Owner; este
documento no la reinterpreta como ejecución realizada por un agente remoto.

El Project Vault fue reconciliado mediante el workflow manual-on-demand del Sync
Agent y su dry-run final reportó drift cero para el mismo HEAD.

---

## 3. Finding documental no funcional

Los documentos derivados canónicos:

```text
CHANGELOG.md
docs/project/project_context.md
docs/project/implementation_roadmap.md
docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md
```

aún contienen descripciones post-PR #88 en varias secciones y no reflejan por
completo G0/G1, G2 y G3 de Governed Projection Consumption.

Esto no invalida el código integrado ni este análisis, porque la fuente material
más reciente es Git y los documentos son derivados/no normativos.

Sin embargo:

```text
canonical derived docs reconciliation = REQUIRED BEFORE G2
```

No se iniciará G2 de esta unidad mientras ese drift documental siga abierto.

---

## 4. Resultado formal G0 — necesidad real

G2/G3 de Governed Projection Consumption dejaron explícitamente el residual:

```text
candidate_id binding
!=
cryptographic candidate content integrity
```

El baseline actual utiliza `candidate_id` como binding estructural a través de
varias fronteras. Esa identidad es útil para correlación, pero no demuestra que
el contenido estructurado del candidate sea el mismo.

Dos objetos distintos pueden compartir:

```text
candidate_id == "candidate-1"
```

y diferir en:

```text
origin
experience
control
created_at
```

`@dataclass(frozen=True)` protege una instancia contra mutación ordinaria después
de construcción. No impide construir otra instancia válida con el mismo ID y
contenido diferente.

Por tanto:

```text
object immutability
!=
content identity
```

Mientras la cadena termina en una decisión pura sin side effects, este residual
fue aceptable y quedó documentado.

Cuando se considere Persistence Authorization, la situación cambia. Una futura
operación durable deberá poder demostrar que el payload que pretende almacenar
es exactamente el candidate al que se refiere la cadena de evidencia y decisión,
no únicamente otro objeto con el mismo `candidate_id`.

SECURITY.md exige reevaluar explícitamente identidad, integridad y límites antes
de Memory persistente, y además establece:

```text
Having access to data
!=
permission to persist or reuse it
```

Conclusión G0:

```text
Persistence Authorization is NOT yet admissible as the next implementation.
```

Antes debe existir una identidad de contenido determinista que permita posteriores
bindings fuertes sin depender de identidad textual opaca solamente.

Disposición:

```text
G0 RESULT: PASS
candidate disposition: HARDEN
risk class: 3 — HIGH
blocking findings for design: 0
implementation authorized: false
```

---

## 5. Qué problema NO intenta resolver esta unidad

Esta unidad no intenta probar:

- quién originó realmente el candidate;
- que la fuente sea confiable;
- que el contenido sea verdadero;
- que un assessment sea correcto;
- que una firma pertenezca a una identidad real;
- freshness operacional;
- anti-replay;
- unicidad global de `candidate_id`;
- autorización para persistir;
- autorización para recuperar;
- promoción a Knowledge.

La frontera propuesta resuelve solamente:

```text
same structured candidate content?
```

No resuelve:

```text
should this content be trusted or stored?
```

---

## 6. Alternativas evaluadas en G0

### 6.1. Alternativa A — continuar usando solo `candidate_id`

Disposición:

```text
REJECT
```

Motivo:

- no detecta reconstrucción con mismo ID y distinto payload;
- no permite binding durable fuerte;
- hereda por silencio el residual que G2/G3 exigieron reevaluar.

### 6.2. Alternativa B — confiar en `frozen=True`

Disposición:

```text
REJECT
```

Motivo:

- frozen evita modificación ordinaria de una instancia;
- no convierte el objeto en content-addressed;
- no impide otra instancia con IDs iguales y campos diferentes.

### 6.3. Alternativa C — convertir `candidate_id` en hash del contenido

Disposición:

```text
REJECT FOR CURRENT UNIT
```

Motivo:

- cambia la semántica pública ya utilizada por contratos y tests;
- mezcla correlación lógica con identidad material;
- exige refactor transversal prematuro;
- dificulta preservación de IDs externos o de workflow cuando éstos sean útiles.

### 6.4. Alternativa D — introducir PKI, firma digital y anti-replay ahora

Disposición:

```text
DEFER
```

Motivo:

- resuelve autenticidad y transporte además de integridad;
- excede la necesidad inmediata;
- interactúa con el riesgo residual de SecurityContext;
- requiere threat model y autoridad propia;
- no es necesario para establecer una identidad determinista local del contenido.

### 6.5. Alternativa E — identidad de contenido sidecar, determinista y versionada

Disposición:

```text
SELECT
```

Concepto:

```text
EpisodicMemoryCandidate
        ↓
canonical candidate representation v1
        ↓
cryptographic digest
        ↓
EpisodicCandidateContentIdentity
```

La identidad se mantiene separada de `candidate_id` y de toda decisión de trust.

---

## 7. Decisión G1 — arquitectura candidata

G1 selecciona una frontera aditiva, pura y específica del dominio episódico.

Conceptualmente:

```text
EpisodicMemoryCandidate
        ↓
compute candidate content identity
        ↓
immutable identity sidecar
```

No se selecciona un `UniversalIntegrityManager`, registry global ni servicio
central de hashing.

La futura API deberá ser importable desde un módulo explícito de `malak.memory`
y permanecer independiente de Kernel, SecurityContext, filesystem, network y DB.

---

## 8. Propiedades obligatorias de la identidad

La futura identidad deberá ser:

- determinista;
- reproducible entre procesos y plataformas;
- versionada;
- independiente del `repr(...)` de Python;
- independiente de orden accidental de diccionarios;
- independiente de direcciones de memoria;
- sin timestamps de cálculo;
- sin random/nonce;
- sin dependencia de locale;
- sin dependencia de filesystem;
- sin dependencia de red;
- basada únicamente en el candidate suministrado y una especificación canónica.

Principio:

```text
same candidate fields + same canonicalization version
=
same digest
```

Y:

```text
any material field difference
=>
different digest
```

---

## 9. Alcance material de canonicalización candidato

G1 establece que la identidad debe cubrir el candidate completo, no solo el
texto conversacional.

Como mínimo deberán quedar representados de forma explícita y ordenada:

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

Incluir campos trust-sensitive de `control` en la identidad **no les concede
trust**. Solo hace detectable que el objeto cambió.

```text
hashed untrusted metadata
!=
trusted metadata
```

La proyección gobernada seguirá siendo la única fuente válida de effective
trust-sensitive admission inputs cuando corresponda.

---

## 10. Canonicalización — restricciones G1

G1 no congela todavía el byte layout final; eso pertenece a G2.

Sí congela estas restricciones:

- esquema de canonicalización con versión explícita;
- domain separation específica de Malāk y del tipo de artefacto;
- UTF-8 explícito;
- representación determinista de `None`;
- representación determinista de datetimes UTC;
- nombres de campos explícitos;
- no usar `pickle`;
- no usar `repr`;
- no usar `str(dataclass)`;
- no depender de serialización implícita de enums/dataclasses;
- no normalizar silenciosamente el contenido textual del usuario o assistant;
- no aplicar `.strip()`, case-folding ni Unicode normalization adicional durante
  hashing salvo que una futura G2 lo justifique expresamente.

El objetivo es identidad exacta, no equivalencia semántica.

---

## 11. Algoritmo criptográfico candidato

Para G1, SHA-256 del estándar de Python (`hashlib.sha256`) es el candidato
preferido porque:

- no agrega dependencias;
- es determinista y multiplataforma;
- es apropiado para detectar cambios de contenido;
- no pretende proporcionar autenticidad por sí mismo.

G2 deberá confirmar o rechazar esta elección antes de implementación.

No se introducen:

```text
HMAC
private keys
public keys
certificates
signatures
key rotation
nonce
replay cache
```

por esta unidad.

---

## 12. Contrato conceptual candidato

G1 propone, sin congelar aún nombres finales de API, un contrato equivalente a:

```text
EpisodicCandidateContentIdentity
    candidate_id
    digest_algorithm
    digest_hex
    canonicalization_version
    policy_version
```

No debe incluir `computed_at`, porque el mismo candidate debe producir la misma
identidad independientemente del instante de cálculo.

Una futura operación de verificación deberá distinguir explícitamente:

```text
MATCH
MISMATCH
```

y no convertir mismatch en Admission `REJECT` ni en decisión de Persistence.

---

## 13. Relación con la cadena existente

Esta frontera por sí sola no autoriza a modificar inmediatamente todos los
contratos existentes.

La maduración prevista es incremental:

```text
Candidate Content Identity
        ↓
separate future propagation/binding design
        ↓
assessment / temporal / projection / consumption binding hardening
        ↓
Persistence Authorization design
```

Por tanto:

```text
content identity implemented
!=
end-to-end integrity binding complete
```

Antes de Persistence Authorization deberá demostrarse explícitamente que la
identidad de contenido queda vinculada a suficiente evidencia downstream para
impedir sustitución del candidate por otro objeto con el mismo ID.

No se considera cerrado ese problema por el solo hecho de calcular un hash.

---

## 14. Riesgos y límites

### Riesgo R1 — hash confundido con trust

Mitigación:

```text
identity != trust
```

El contrato y documentación deberán repetir esa separación.

### Riesgo R2 — canonicalización accidentalmente inestable

Mitigación:

- schema version;
- test vectors exactos;
- representación explícita;
- validación Windows/Linux/macOS.

### Riesgo R3 — hash correcto sobre objeto equivocado

Mitigación:

La identidad solo demuestra qué contenido fue hasheado. La propagación y binding
contra assessments/decisions sigue siendo trabajo separado y bloqueante antes de
persistencia.

### Riesgo R4 — sobreingeniería criptográfica

Mitigación:

No firmas, PKI, HMAC, nonce ni replay protection en esta unidad.

### Riesgo R5 — falsa seguridad por `candidate_id`

Mitigación:

Nunca usar igualdad de ID como sustituto de igualdad de digest cuando una futura
frontera exija identidad material.

---

## 15. Necessity & Complexity Review

### ¿Es necesaria?

Sí. El residual fue identificado y congelado antes de Persistence Authorization.

### ¿Puede resolverse sin nueva frontera?

No de forma limpia. Cambiar semántica de `candidate_id` o insertar hashing dentro
de Admission mezclaría responsabilidades existentes.

### ¿La frontera propuesta es mínima?

Sí en G1: una identidad sidecar específica y pura, sin almacenamiento, runtime ni
autoridad.

### ¿Es permanente?

Sí. Toda futura persistencia, auditoría durable o evidencia candidate-bound puede
necesitar una identidad material estable aunque la forma exacta de propagación se
madure después.

Resultado:

```text
NECESSARY: yes
MINIMAL: yes
PERMANENT RESPONSIBILITY: yes
AUTHORITY DELTA: 0
```

---

## 16. FULL 4R preliminar

### Risk

```text
PASS WITH REQUIRED FOLLOW-UP
```

Reduce el riesgo de candidate substitution, pero no cierra todavía replay,
autenticidad ni binding end-to-end.

### Readability

```text
PASS
```

Responsabilidad única: identidad determinista de contenido episódico.

### Reliability

```text
PASS IF G2 FREEZES CANONICAL BYTES + TEST VECTORS
```

Sin byte layout y vectores exactos no debe implementarse.

### Resilience

```text
PASS WITH FAIL-CLOSED VERIFICATION
```

Una futura verificación mismatch no podrá caer silenciosamente a `candidate_id`.

---

## 17. Precondiciones obligatorias para G2

G2 no queda autorizado por este documento.

Antes de G2 deberán cumplirse todos estos gates:

```text
1. human review / merge de este design record
2. reconciliación de canonical derived docs post-PR #92
3. Project Vault reconciliado al nuevo HEAD resultante
4. baseline main verificado
5. Owner authorization explícita para G2
```

G2 deberá congelar, como mínimo:

- módulo exacto;
- contratos exactos;
- canonicalization version;
- domain separator;
- byte representation exacta;
- datetime representation exacta;
- digest algorithm exacto;
- lowercase/uppercase hex policy;
- constructor invariants;
- verify semantics;
- type/error behavior;
- test vectors cross-platform;
- file budget;
- FULL 4R;
- candidate-bound validation.

---

## 18. Fuera de alcance

Continúa expresamente fuera de alcance:

```text
Persistence Authorization
persistent Memory
Memory store
retrieval
RAG / GraphRAG
Knowledge promotion
Conversation/runtime wiring
Kernel changes
SecurityContext changes
PKI / signatures / HMAC
nonce / replay protection
MFA
agents / tools / network
Sandbox
MCP / A2A
Sprint 7.12
RDD Stage 2
```

---

## 19. Disposición G1

```text
G0: PASS / HARDEN
G1: PASS
selected direction: additive versioned candidate content identity sidecar
implementation_authorized: false
G2_authorized: false
Persistence_Authorization_authorized: false
persistent_Memory_authorized: false
Sprint_7_12_authorized: false
RDD_Stage_2_authorized: false
```

La siguiente acción permitida después de revisión humana de este record es
reconciliar el drift documental derivado post-PR #92 y, únicamente después de
cerrar ese gate y el Vault correspondiente, evaluar autorización separada de G2.

---

## 20. Invariante de cierre

```text
candidate_id
!=
candidate content identity

candidate content identity
!=
source authenticity
!=
source trust
!=
truth
!=
Admission eligibility
!=
Persistence Authorization
!=
Stored Memory
!=
Authority
```

El propósito de esta frontera es hacer más fuerte el binding futuro sin crear una
nueva fuente de autoridad.