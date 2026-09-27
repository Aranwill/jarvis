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
- G3 integró `Episodic Memory Admission Boundary` como primera
  materialización aislada de la Memory Layer: contratos inmutables,
  separación entre payload y metadata de control y policy determinista
  `REJECT | HOLD | ELIGIBLE`, sin wiring runtime, persistencia, retrieval ni
  dependencias externas.
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
- PR #92 integró `Episodic Admission Governed Projection Consumption Boundary`,
  que consume únicamente projections gobernadas consumibles, construye una vista
  efectiva efímera del candidate y delega exactamente una vez a la policy de
  admisión, con resultado `EVALUATED | BLOCKED` y sin persistencia ni side effects.
- PR #93 integró el diseño G0/G1 de `Episodic Candidate Content Identity Boundary`;
  G2, implementación y propagación de identidad continúan no autorizados.
- PR #97 preservó `Malāk Evidence-Bound Cognition Foundation` como referencia
  conceptual no normativa; PR #98 y PR #99 integraron respectivamente G0 de
  investigación/costos y G1 de diseño de Progressive Cognitive Assurance, sin
  implementación runtime ni cambio constitucional en esos gates.
- PR #164 integró `Repository Structural Projection V0` y PR #166 integró
  `Repository Structural Lookup V0` como primitives deterministas, read-only y
  baseline-bound para hechos sintácticos de repositorio.
- PR #168 integró evidencia estructural `[S#]` exclusivamente en E2 Engineering
  Inspect y PR #170 incorporó observabilidad determinista de esa evidencia, sin
  propagarla a E3/E4 ni introducir authority delta.
- PR #177 integró `E2 Structural Evidence Evaluation Pack V0`, con seis casos
  A/B reproducibles, ground truth revisado separadamente, schema fail-closed y
  runner determinista; no añadió Capability, runtime productivo, persistencia,
  Kernel/Planner delta ni propagación estructural a E3/E4.
- PR #180 integró `Internal Interaction Trace V0`, con recorrido reconstruible,
  artefactos ligados al baseline y `authority_effect=none`.
- PR #182 integró `Live / Replay Visual Projection V0` y PR #184
  `Internal Interaction Test V0`, preservando equivalencia material
  LIVE/REPLAY y ejecución read-only del slice U01.
- PR #186 integró `Governed Engineering Evidence Focus V0`, con selectores
  deterministas, evidencia requerida/suplementaria, `focus_complete`
  fail-closed y continuidad de `evidence_set_digest`.
- PR #188 integró Live Elapsed, PR #189 Safe Diagnostics y PR #190 Runtime /
  Model Provenance, sin ampliar autoridad ni modificar Kernel o Planner.
- PR #194 integró `Analyze Structured Output Contract V0`.
- PR #197 integró `Runtime Generation Contract V0`, con contexto/output/
  thinking explícitos, `truncate=false`, `shift=false` y validación
  fail-closed de completion metadata.
- PR #201 integró `E4 Reference-Bounded Structured Output V0`, ligando
  dinámicamente los schemas de E4 a los identificadores exactos del packet.

### Changed

- `SECURITY.md` fue reconciliado con el Security Control Plane y Secure Context
  Lifecycle ya implementados, separando controles vigentes, riesgo residual y
  requisitos obligatorios para futuras superficies sensibles.
- `AGENTS.md`, el Malāk Construction Protocol, el Development Checklist y el
  template de Pull Request fueron reforzados para exigir revisión explícita de
  `SECURITY.md` y `MALAK_RESEARCH_HORIZON_MAP.md` durante admisiones y análisis
  de próxima implementación cuando corresponda.
- PR #96 reforzó `AGENTS.md` para exigir modificaciones acotadas, deterministas,
  observables y proporcionales al objetivo autorizado; refactors, limpiezas,
  simplificaciones o mejoras laterales requieren scope/gate separado.
- La documentación derivada de proyecto se reconcilia al baseline post-PR #177
  sin reescribir snapshots históricos, preservando la distinción entre runtime
  productivo, tooling de evaluación, diseño histórico y autoridad no concedida.
- PR #205 promovió KIC-01..KIC-07 a la Kernel Specification, aclarando que
  Kernel First es responsibility-centric y no exige singleton de objeto.
- PR #208 integró KAF-01: `docs/architecture/kernel.md` pasa a
  `APPROVED_SPECIFICATION / normative_subordinate` dentro de E1 y se vuelve
  evidencia requerida del foco U01.
- PR #209 integró E3 Epistemic Calibration, separando incertidumbre del estado
  actual, incompletitud histórica y riesgo prospectivo sin relajar
  `UNRESOLVED`.

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

### Validated

- Candidato final de Sprint 7.11: `388 passed`, `compileall: PASS`,
  `diff-check: PASS`, FULL 4R PASS e independent validation PASS.
- La ejecución post-merge de `Validation` sobre
  `3413e8ccb348440aea757d1feccde25c65be011f` concluyó con `success`.
- Candidate G3 `e3e3c2aa6031d4a6a9ad8f3a3c529a9453cbbe9b`: `431 passed`,
  `compileall: PASS` y `diff-check: PASS`.
- La validación post-merge de G3 sobre `2d5fe87c304927baeab29e5649f2383030e1a1fd` concluyó con `success`.
- El candidate de PR #88 `87a7e31e0735edd25a80a693cf3f437f7a1501fc`
  pasó `Validation` candidate-bound en `ubuntu-latest`, `windows-latest` y
  `macos-latest`, incluyendo identidad exacta, suite, `compileall` y diff-check.
- El candidate de PR #92 `5139d95aaa2c30971b3979ca7c3917067856a428`
  pasó `Validation` candidate-bound en Ubuntu, Windows y macOS; Ubuntu reportó
  `645 passed`, `compileall: PASS` y `git diff --check: PASS`.
- La validación local post-G3 reportada por el Owner sobre el HEAD integrado de
  PR #92 concluyó con `645 passed`, forced `compileall` PASS, diff-check PASS y
  árbol de trabajo limpio.
- Validation #428 revalidó post-merge `main@e29d3dc79445506aa9bb4e59a8383524d627db68`
  después de PR #177: `1278 passed` en Ubuntu y Windows, `compileall: PASS` y
  diff validation PASS.
- Governed Engineering Evidence Focus V0 cerró con Validation #495:
  `1493 passed` en Ubuntu y Windows.
- Live Elapsed cerró con Validation #502: `1501 passed` en Ubuntu y Windows.
- Safe Diagnostics cerró con Validation #513: `1518 passed` en Ubuntu y Windows.
- Runtime / Model Provenance cerró con Validation #541: `1535 passed` en Ubuntu y Windows.
- Analyze Structured Output cerró con Validation #565: `1554 passed` en Ubuntu y Windows.
- Runtime Generation Contract cerró con Validation #597: `1578 passed` en Ubuntu y Windows.
- E4 Reference-Bounded Structured Output cerró con Validation #611:
  `1583 passed` en Ubuntu y Windows.
- KAF-01 cerró con Validation #630: `1588 passed` en Ubuntu y Windows.
- E3 Epistemic Calibration cerró con Validation #634:
  `1599 passed` en Ubuntu y Windows.
- Las validaciones finales anteriores pasaron con candidate identity,
  `compileall` y candidate diff en PASS según sus gates.

### Notes

- Sprint 7.11 permanece como el último sprint numerado integrado.
- Dentro de la cadena episódica/Memory aislada, la última unidad funcional
  integrada continúa siendo `Episodic Admission Governed Projection Consumption
  Boundary` (PR #92), precedida por Governed Input Projection, Assessment
  Producer Authorization, Assessment Provenance y Episodic Memory Admission;
  esa cadena permanece aislada de Conversation/runtime y sin persistencia o
  retrieval.
- `Projection READY != Admission ELIGIBLE != Stored != Authority` y
  `Consumption EVALUATED != persistence authorization != Authority`.
- `candidate_id` binding no equivale a identidad criptográfica del contenido;
  Candidate Content Identity permanece únicamente en G0/G1 y su G2 no está
  autorizado.
- PR #97–#99 conservan el origen G0/G1 de Progressive Cognitive Assurance; ese
  estado es histórico y no describe por sí solo el baseline CURRENT. Las
  promociones y foundations posteriores deben consultarse en las fuentes CURRENT.
- Structural Evidence permanece limitada a E2; su propagación a E3/E4 y
  `Structural Delta` continúan diferidas y requieren gates separados.
- Seventh U01 (`bootstrap-u01-20260926-007`) terminó `INCONCLUSIVE` con
  `3 ALIGNED + 3 UNRESOLVED`; ese resultado histórico no se reescribe.
- Los findings posteriores fueron tratados mediante U007-F05, KAF-01 y
  E3 Epistemic Calibration.
- La integración de esas correcciones no autoriza por sí sola un Octavo U01.
- Eighth U01 continúa requiriendo admission review, preflight local, identidad
  exacta de runtime/modelo y autorización explícita del Owner.
- `acceptance PASS != cognitive PASS`.
- `Evidence != Authority`.
- Self-modification continúa no autorizada.
- Sprint 7.10 permanece como la última ruta conversacional/runtime integrada.
- RDD Stage 1 permanece adoptado y RDD Stage 2 continúa no autorizado.
- Ningún cambio de versión, tag, merge o promoción de release queda autorizado
  únicamente por esta sección.
- Esta reconciliación documental no autoriza Sprint 7.12, Candidate Content
  Identity G2, Persistence Authorization, Memory persistente, runtime wiring,
  agentes, tools, Sandbox, navegación, MCP/A2A ni ampliación de autoridad.

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