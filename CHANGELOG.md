# Changelog

Todos los cambios importantes de Malāk se documentan en este archivo.

El formato sigue los principios de Keep a Changelog y Versionado Semántico.
La versión nominal vigente continúa siendo `v0.6.0-alpha`.

---

## [Unreleased]

### Notes

- Sprint 7.8 permanece como el último sprint funcional completado del baseline actual.
- Ningún cambio de versión, tag, merge o promoción de release queda autorizado
  únicamente por esta sección.

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
