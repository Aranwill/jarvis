> [!WARNING]
> **Registro histórico / legacy**
>
> Este archivo conserva decisiones tomadas durante etapas tempranas del proyecto
> Jarvis y se mantiene exclusivamente por trazabilidad histórica.
>
> No representa el registro vigente de decisiones arquitectónicas de Malāk y no
> debe utilizarse como fuente normativa, operativa ni de planificación actual.
>
> Los ADR aceptados vigentes se encuentran en:
>
> `docs/architecture/adr/`
>
> El índice vigente de decisiones arquitectónicas se encuentra en:
>
> `docs/architecture/decisions/decision-index.md`
>
> Las referencias históricas contenidas aquí, incluyendo nombres de ADR,
> tecnologías, modelos o componentes, no sustituyen ni modifican las decisiones
> canónicas actuales.

# Decisiones Arquitectónicas

## 2026-05-30

Se adopta Open WebUI como interfaz principal.

Motivo:
- Integración nativa con Ollama.
- Soporte RAG.
- Gestión de conocimiento.

---

## 2026-05-30

Se adopta Qwen3.5:9B como modelo principal.

Motivo:
- Mejor rendimiento que Qwen2.5.
- Mejor razonamiento.
- Compatible con RTX 2060 12GB.

---

## 2026-05-30

Se adopta DeepSeek-Coder como agente de programación.

Motivo:
- Especializado en código.

## DEC-003

Fecha:
2026-05-31

Decisión:
Utilizar Git local para control de versiones.

Motivo:
Versionar documentación, scripts y arquitectura de Jarvis.

Estado:
Aceptada

---

## DEC-004

Fecha:
2026-05-31

Decisión:
Implementar backups automáticos durante el cierre de Jarvis.

Motivo:
Garantizar recuperación de documentación y memoria vectorial.

Estado:
Aceptada

---

## DEC-005

Fecha:
2026-05-31

Decisión:
Mantener ChromaDB integrado en Open WebUI.

Motivo:
La instalación actual ya proporciona persistencia vectorial suficiente para la fase actual.

Estado:
Aceptada

---

# ADR-001 — Código fuente bajo src

Fecha: 2026-06-28  
Estado: Aprobado  
Sprint: Sprint 2 — Foundation Implementation

## Decisión

Todo el código fuente de Jarvis deberá residir dentro de:

```text
src/