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

### Changed

- `SECURITY.md` fue reconciliado con el Security Control Plane y Secure Context
  Lifecycle ya implementados, separando controles vigentes, riesgo residual y
  requisitos obligatorios para futuras superficies sensibles.
- `AGENTS.md`, el Malāk Construction Protocol, el Development Checklist y el
  template de Pull Request fueron reforzados para exigir revisión explícita de
  `SECURITY.md` y `MALAK_RESEARCH_HORIZON_MAP.md` durante admisiones y análisis
  de próxima implementación cuando corresponda.

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

### Notes

- Sprint 7.11 permanece como el último sprint numerado integrado.
- G3 — `Episodic Memory Admission Boundary` es la unidad de código de producto
  integrada más reciente, pero permanece aislada y sin wiring runtime,
  persistencia o retrieval.
- Sprint 7.10 permanece como la última ruta conversacional/runtime integrada.
- No existe actualmente una unidad posterior a G3 autorizada.
- RDD Stage 1 permanece adoptado y RDD Stage 2 continúa no autorizado.
- Ningún cambio de versión, tag, merge o promoción de release queda autorizado
  únicamente por esta sección.
- Esta reconciliación documental no autoriza un nuevo sprint, Memory persistente,
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