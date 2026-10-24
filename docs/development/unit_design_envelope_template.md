# Malāk — Unit Design Envelope (plantilla compacta)

**Rol:** soporte informativo para una única unidad. Completar antes de abrir la rama y reutilizar en el design record o body de la PR. **No crea gates, waivers, autorizaciones ni un archivo adicional obligatorio por unidad.** Las fuentes vigentes son `AGENTS.md`, Construction Preflight P0–P7, Construction Protocol (§5.1.1, §5.2, §5.5) y Engineering Method.

| Admisión / campo | Registro breve y evidencia enlazada |
| --- | --- |
| **P0 — Identidad** | `repository`, `baseline SHA/tree`, `work_unit`, `work_type`, `owner_instruction`; checkpoint previo cuando aplique. |
| **P1 — Fuentes** | CURRENT_STATE y fuentes aplicables por autoridad; ADR, contratos y documentos de ley; histórico/conceptual separado. |
| **P2/P3 — Invariantes y autoridad** | Blueprint/Constituciones/Kernel/SECURITY/ADR-003: compatible o conflicto; flujo de control, `authority_effect: none`; Ready/Merge Owner. |
| **P4 — Necesidad/reutilización** | Problema observable del baseline; REUSE/ADAPT/COMPOSE/NEW; coste, alternativa mínima y justificación. |
| **P5 — Riesgo** | `risk_class: 0..4` y razón en el **delta**, `critical_contract: YES/NO` contrastado con §5.2; 4R, RDD, G0/G1 y reviewer según aplicabilidad. |
| **P6 — Scope** | Resultado verificable, archivos/componentes permitidos y prohibidos, contratos invariantes, candidate identity, STOP y rollback. |
| **P7 — Disposición** | `PASS/FAIL/INCONCLUSIVE` con razón, findings vinculados materialmente y evidencia; sin inferir PASS de tests o antecedentes. |

## Decisión de topología — **antes de la rama**

| Pregunta | Disposición |
| --- | --- |
| ¿La unidad **material** requiere especificación formal G0/G1 y **posterior implementación**? | **Sí:** topología predeterminada **PR-A Design/Documentation → Owner Merge → PR-B Implementation**, conforme a §5.1.1. |
| ¿Es documentación autónoma, microcambio aprobado o unidad sin diseño formal previo aplicable? | **Sí, con fundamento registrado:** **una PR proporcional**. No inventar una Design PR artificial. |
| ¿Afecta un contrato crítico (§5.2), aunque el delta sea pequeño? | Preservar **íntegramente** §5.5, hardening, Design 4R pre-RED, FULL 4R post-GREEN, RDD/CI y validaciones aplicables. La plantilla no habilita omisiones. |
| ¿Hay finding histórico `INCONCLUSIVE/FAIL`? | Vincular y tratar como bloqueo sólo cuando exista **relación material con el scope actual** o una norma activa lo exija; conservar provenance y no reabrir issues automáticamente. |

**Topología elegida:** `ONE_PR / DESIGN_PLUS_IMPLEMENTATION` · **fundamento material:** `...` · **Owner aprueba apertura:** `...`.

**Contrato de ejecución:** RED/GREEN separados por evidencia y autorización del Owner cuando aplique; candidato corregido implica revalidación afectada; 4R, E2E, CI, RDD Stage 1/2 y revisión independiente se disponen según riesgo y contrato, no por inercia. `INCONCLUSIVE != PASS`; `gate != PR`; `reviewer != PR`; `Evidence != Authority`; Ready y Merge sólo del Owner.

**Uso:** esta ficha resume decisiones y apunta a evidencia fuente; **no sustituye** el Construction Preflight, la Alignment Matrix obligatoria cuando aplique, receipts, manifests ni validación sobre el candidate exacto. Las filas pueden enlazar evidencias existentes en vez de duplicarlas.
