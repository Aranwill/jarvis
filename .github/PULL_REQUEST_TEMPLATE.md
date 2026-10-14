\# Pull Request



\## Descripción



Describa brevemente el objetivo de este Pull Request.



\---



\## Tipo de cambio



\- \[ ] Feature

\- \[ ] Bug Fix

\- \[ ] Refactor

\- \[ ] Documentation

\- \[ ] Test

\- \[ ] Performance

\- \[ ] Security



\---



\## Arquitectura



¿Este cambio respeta los principios definidos en:



\- \[ ] Blueprint

\- \[ ] Cognitive Constitution

\- \[ ] Governance Constitution

\- \[ ] Kernel Specification

\- \[ ] `SECURITY.md` cuando el cambio afecta seguridad, autoridad, identidad, contexto, persistencia, red, agents, tools, modelos, datos o integraciones externas.

\- \[ ] Si este PR propone una nueva superficie o próxima implementación, revisé `docs/project/concepts/MALAK_RESEARCH_HORIZON_MAP.md` y las referencias conceptuales aplicables.

\- \[ ] Distinguí explícitamente `security requirement != implemented control` y `research gap != implementation authorization`.



\---



\## Validación



\- \[ ] Probado localmente

\- \[ ] Sin errores

\- \[ ] No rompe funcionalidades existentes

\- \[ ] Los cambios de seguridad incluyen casos negativos / fail-closed proporcionales cuando corresponde.



\---



\## Documentación



\- \[ ] Se actualizó la documentación correspondiente.

\- \[ ] No requiere cambios en la documentación.

\- \[ ] Revisé impacto sobre documentos `CURRENT_STATE` definidos en `AGENTS.md`.

\- \[ ] Si cambió una política o límite de seguridad, `SECURITY.md` fue reconciliado.

\- \[ ] Si cambió una visión, gap o clasificación conceptual, revisé `MALAK_RESEARCH_HORIZON_MAP.md`, `docs/project/concepts/README.md` y las ideas relacionadas.

\- \[ ] Si este PR cierra o integra un Sprint, `README.md` fue revisado y reconciliado con el baseline resultante, o se justificó explícitamente por qué no requiere cambios.

\- \[ ] Si este PR cierra o integra un Sprint, las fuentes `CURRENT_STATE` aplicables fueron reconciliadas post-merge o existe un corrective packet explícito para completar ese cierre antes de declarar terminado el Sprint.

\- \[ ] Las referencias históricas/legacy no fueron reinterpretadas como estado vigente.

\- \[ ] Nuevas rutas documentales relevantes tienen clasificación, owner y cobertura interna explícitos.



\---



\## Governed Construction



Identifique el rol de este PR dentro del Construction Protocol.



\- \[ ] Design / Documentation PR

\- \[ ] Implementation / Governed Construction Cycle PR

\- \[ ] Cambio proporcional al que no aplica el modelo de dos fases; razón documentada abajo.



\### Identidad y lineage



\- Baseline exacto: `<sha>`

\- Candidate actual: `<sha>`

\- Design PR / specification reference: `<ref o N/A con razón>`

\- Risk class: `<0..4>`

\- Critical contract: `YES | NO`

\- Authority effect: `none`



\### Gate ledger



Para Design / Documentation PR, registrar según aplicabilidad:



```text
Construction Preflight:
G0 / admission:
G1 design:
Malāk Alignment Matrix:
Critical Contract Hardening:
Cuatro preguntas de ley:
Design 4R:
RDD Stage 1 Design Check:
Human review:
Ready / Merge: OWNER ONLY
```



Para Implementation PR, registrar según aplicabilidad:



```text
RED candidate:
RED result:
Owner GREEN authorization:
GREEN candidate:
targeted validation:
Candidate FULL 4R:
Bounded Correction / Fix Validator:
E2E / integration:
CI / candidate-bound evidence:
independent validation:
RDD Stage 1 Candidate Conformance:
Human review:
Ready / Merge: OWNER ONLY
post-merge validation: NOT EXECUTED until merge
```



\### Invariantes del ledger



\- \[ ] `gate separation != PR separation`.

\- \[ ] RED y GREEN conservan candidate identity y Evidence propias.

\- \[ ] Compartir branch o PR no se interpreta como autorización para avanzar.

\- \[ ] El body referencia Evidence; no la sustituye ni crea Authority.

\- \[ ] La Implementation PR permanece Draft hasta promoción manual del Owner.

\- \[ ] Una PR adicional para la misma unidad tiene frontera material o excepción explícita documentada.

\- \[ \] RDD Stage 2 se aplicó conforme al riesgo y admission vigentes: risk 0/1 = `NOT_APPLICABLE`; risk 2 = `OPTIONAL` con admission explícita; risk 3/4 = `REQUIRED`. Stage 3+ permanece `NOT_AUTHORIZED`.



\---



\## Observaciones



Agregar cualquier comentario adicional.

