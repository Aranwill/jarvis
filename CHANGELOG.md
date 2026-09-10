# Changelog

Todos los cambios importantes de Malāk se documentan en este archivo.

El formato sigue los principios de Keep a Changelog y Versionado Semántico.
La versión nominal vigente continúa siendo `v0.6.0-alpha`.

---

## [Unreleased]

### Added

- Sprint 7.11 incorporó una pipeline mínima de validación reproducible en
  GitHub Actions para candidatos exactos y para `main`, con permisos de solo
  lectura, Python 3.12, suite completa, `compileall` y `git diff --check`
  candidate-bound.
- Se declaró `pytest>=9,<10` como dependencia opcional de desarrollo sin añadir
  dependencias de runtime.
- Se incorporó `MALAK_RESEARCH_HORIZON_MAP.md` como referencia conceptual no
  normativa para reconciliar investigación, gaps y conceptos existentes sin
  promoverlos automáticamente a roadmap o implementación.
- G3 integró `Episodic Memory Admission Boundary` como primera materialización
  aislada de la Memory Layer: contratos inmutables, separación entre payload y
  metadata de control y policy determinista `REJECT | HOLD | ELIGIBLE`, sin
  wiring runtime, persistencia, retrieval ni dependencias externas.
- PR #82 integró `Episodic Admission Assessment Provenance Boundary`, una
  validación estructural aislada para ligar assessments a `assessment_id`,
  `candidate_id`, kind y producer role sin convertir provenance en identidad,
  truth, permiso o autoridad.
- PR #85 integró `Episodic Admission Assessment Producer Authorization Boundary`,
  reutilizando el Security Control Plane existente para validar evidencia de
  autorización scoped del productor sin crear un segundo motor de autoridad.
- PR #88 integró `Episodic Admission Governed Input Projection Boundary`, que
  reconstruye inputs efectivos de admisión desde assessments con provenance y
  autorización válidas más control temporal gobernado, con resultados
  `READY | HOLD | DENIED` y sin ejecutar la policy de admisión.
- PR #90 integró el design record G0/G1 de
  `Episodic Admission Governed Projection Consumption Boundary`.
- PR #91 integró la specification G2 de esa frontera, congelando
  `EVALUATED | BLOCKED`, reason codes, precedencia y el presupuesto de dos
  archivos para G3.
- PR #92 integró `Episodic Admission Governed Projection Consumption Boundary`,
  conectando una projection `READY` con la policy existente de Admission
  mediante una vista efímera del candidate construida con el
  `effective_context` gobernado, sin reabrir trust desde `candidate.control`.
- PR #93 integró G0/G1 de `Episodic Candidate Content Identity Boundary`, que
  identifica como siguiente hardening necesario una identidad de contenido
  determinista y versionada antes de considerar Persistence Authorization.

### Changed

- `SECURITY.md` fue reconciliado con el Security Control Plane y Secure Context
  Lifecycle ya implementados, separando controles vigentes, riesgo residual y
  requisitos obligatorios para futuras superficies sensibles.
- `AGENTS.md`, el Malāk Construction Protocol, el Development Checklist y el
  template de Pull Request fueron reforzados para exigir revisión explícita de
  `SECURITY.md` y `MALAK_RESEARCH_HORIZON_MAP.md` durante admisiones y análisis
  de próxima implementación cuando corresponda.
- La documentación derivada de proyecto se reconcilia al estado post-PR #93:
  Governed Projection Consumption ya está integrada y la siguiente frontera
  candidata es Content Identity G0/G1, todavía sin G2 ni implementación.

### Security

- La política activa preserva explícitamente Prompt & Context Trust Boundary,
  Memory/Knowledge poisoning defenses, AI supply-chain trust, identidad y
  delegación no expansiva, Compromise Containment & Trust Revocation, data
  disclosure, Resource Governance y límites de interoperabilidad como requisitos
  de seguridad proporcionales a futuras superficies.
- Deception, honeypots, forensics y respuesta defensiva permanecen limitados a
  capacidades futuras aprobadas e infraestructura propia o expresamente
  autorizada; no se autoriza `hack back` autónomo.
- Los requisitos futuros continúan separados de la implementación vigente:
  `security requirement != implemented control`.
- `candidate_id` continúa siendo identidad lógica/correlacional y no demuestra
  por sí solo identidad material del contenido. Antes de Persistence
  Authorization deberá existir un binding determinista del contenido y volver a
  evaluarse autenticidad/anti-replay cuando la superficie lo requiera.

### Validated

- Candidato final de Sprint 7.11: `388 passed`, `compileall: PASS`,
  `diff-check: PASS`, FULL 4R PASS e independent validation PASS.
- La ejecución post-merge de `Validation` sobre
  `3413e8ccb348440aea757d1feccde25c65be011f` concluyó con `success`.
- Candidate G3 original `e3e3c2aa6031d4a6a9ad8f3a3c529a9453cbbe9b`:
  `431 passed`, `compileall: PASS` y `diff-check: PASS`.
- El candidate de PR #88 `87a7e31e0735edd25a80a693cf3f437f7a1501fc`
  pasó `Validation` candidate-bound en `ubuntu-latest`, `windows-latest` y
  `macos-latest`.
- El candidate final de PR #92
  `5139d95aaa2c30971b3979ca7c3917067856a428` pasó `Validation` candidate-bound
  en Ubuntu, Windows y macOS; Ubuntu reportó `645 passed`, `compileall: PASS`,
  candidate identity PASS y diff-check PASS.
- El Owner reportó validación local post-merge sobre
  `main@9438c66e315faa2b4c8c3f0a99d4e1e9619992c3`: `645 passed`,
  `compileall -f tests: PASS`, `compileall -f src tests scripts: PASS`,
  `git diff --check: PASS` y working tree limpio.
- El candidate docs-only de PR #93
  `4d41776b62fd4f001c850396cb35d365c59a6e0a` pasó el workflow `Validation`.

### Notes

- Sprint 7.11 permanece como el último sprint numerado integrado.
- Sprint 7.10 permanece como la última ruta conversacional/runtime integrada.
- La unidad de código de producto integrada más reciente es
  `Episodic Admission Governed Projection Consumption Boundary` (PR #92).
- La cadena episódica aislada actual termina en Admission:
  `Projection READY → Consumption EVALUATED → Admission REJECT|HOLD|ELIGIBLE → STOP`.
- `Projection READY != Admission ELIGIBLE != Persistence Authorization != Stored != Authority`.
- El design G0/G1 de Content Identity está integrado mediante PR #93, pero
  `G2`, implementación y propagación del digest todavía no están autorizados.
- RDD Stage 1 permanece adoptado y RDD Stage 2 continúa no autorizado.
- Ningún cambio de versión, tag, merge o promoción de release queda autorizado
  únicamente por esta sección.
- Esta reconciliación documental no autoriza Sprint 7.12, Memory persistente,
  Persistence Authorization, retrieval, Knowledge, agentes, tools, Sandbox,
  navegación, MCP/A2A, PKI, firmas ni ampliación de autoridad.

---

## [v0.6.0-alpha]

Fecha inicial: 2026-07-05
Estado actualizado para certificación interna: 2026-08-16

### Added

- Documento institucional `PROJECT.md`.
- Identidad oficial de **Malāk** y trazabilidad de la migración desde **Jarvis**.
- CLI interactiva y pipeline de conversación desacoplado.
- Abstracción de runtime mediante `LLMRuntime` y runtime Ollama integrado sin
  acoplar el Kernel a un proveedor concreto.
- Contratos y persistencia de métricas operativas para observabilidad.
- Security Control Plane con contratos de autorización, PDP, PEP y auditoría.
- Secure Context Lifecycle con emisión, validación temporal, renovación y
  propagación de `SecurityContext`.
- Evidencia y documentación operativa para certificación de baseline mediante
  Sprint 7.7.

### Changed

- El nombre oficial del proyecto pasó de **Jarvis** a **Malāk**.
- El namespace Python operativo fue migrado a `malak`.
- La documentación institucional, de arquitectura y de proyecto fue
  reconciliada con la identidad y el estado actual de Malāk.
- El descubrimiento de paquetes de setuptools quedó restringido explícitamente
  a `malak*`.
- `/build/` quedó tratado como artefacto generado e ignorado por Git.
- La documentación derivada de proyecto fue reconciliada durante Sprint 7.7
  para distinguir baseline integrado, candidate de certificación y estado de
  promoción.

### Validated

- Suite completa: `339 passed`.
- `compileall`: PASS.
- `pip check`: PASS.
- Build aislado PEP 517: PASS.
- Boundary del wheel: PASS; sin paquetes top-level inesperados.
- Security Control Plane: default-deny y fail-closed validados.
- Confirmación humana, binding de decisiones y auditoría previa a operaciones
  protegidas cuentan con cobertura negativa.
- Secure Context Lifecycle cuenta con validación temporal, renovación y
  propagación cubiertas por tests.
- Arquitectura y documentación fueron reconciliadas sin cambios al Kernel,
  Blueprint, Constituciones ni ADR aceptados durante el corrective packet
  documental de Sprint 7.7.

### Security

- El baseline mantiene un riesgo residual aceptado: `SecurityContext` todavía
  no posee una raíz criptográfica fuerte de identidad/provenance.
- Nonce, replay protection, PKI, identidad criptográfica, Secure Message Bus,
  MFA y un Secure Context Manager criptográfico completo permanecen fuera del
  alcance de Sprint 7.7 y no deben interpretarse como capacidades ya
  implementadas.

### Notes

- `0.6.0-alpha` es normalizado por la metadata Python como `0.6.0a0`.
- La referencia histórica a **Jarvis** se conserva únicamente donde es necesaria
  para trazabilidad.
- Esta entrada describe el contenido material del candidate bajo certificación;
  no constituye por sí sola una promoción de release, un tag ni un cambio de
  baseline.

---

## [v0.5.0-alpha] - 2026-06-28

### Added

- Arquitectura Base congelada.
- Blueprint v0.5.0-alpha.
- Cognitive Constitution.
- Governance Constitution.
- Kernel Specification.
- Filosofía Operativa.
- Arquitectura orientada a eventos.
- Separación entre Memory y Knowledge.
- Modelo Capability First.
- Modelo Kernel First.
- Zero Trust.
- Human in Control.
- Model Agnostic.
- Estructura inicial del repositorio.
- Configuración inicial de GitHub.

---

## [v0.5.0-alpha-kernel-mvp]

### Added

- Python development environment.
- `pyproject.toml`.
- Virtual environment (`.venv`).
- Core Request model.
- Core Response model.
- Minimal Kernel implementation.
- First automated tests.
- Pytest configuration.

### Validated

- First executable Kernel.
- 2 automated tests passing.
- Zero warnings.