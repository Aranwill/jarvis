---
title: Sprint 7.2 — Calibración real del runtime
status: borrador preliminar
authority: no normativa
as_of_commit: 71d13fc0ee431b9574fcfb5dbc52baf8cb6e4c4c
language: es
---

# Sprint 7.2 — Calibración real del runtime

## Autoridad y dependencia

Documento derivado y no normativo. No autoriza implementación. Depende de mediciones reales y reproducibles obtenidas tras el Sprint 7.1.

## Objetivo preliminar

Caracterizar el rendimiento de los modelos locales y proponer perfiles de ejecución basados en evidencia, sin alterar políticas automáticamente.

## Alcance preliminar

- Medir carga inicial, tiempo hasta el primer resultado y tiempo total.
- Registrar métricas disponibles de generación y rendimiento por modelo.
- Comparar modelos bajo condiciones documentadas.
- Evaluar timeout y TTL según el hardware observado.
- Proponer perfiles inmutables y trazables por modelo.
- Preservar la separación entre medición, recomendación y configuración efectiva.

## Fuera de alcance

- Optimización automática o autoajuste no autorizado.
- Cambios silenciosos de timeout, TTL o modelo.
- Incorporar nuevas dependencias sin aprobación.
- Persistir prompts o información sensible innecesaria.

## Criterios preliminares de aceptación

- Metodología, hardware y condiciones de prueba documentados.
- Muestras normalizadas y resultados reproducibles.
- Recomendaciones separadas de las decisiones de configuración.
- Errores y datos incompletos representados explícitamente.
- Suite completa en verde y rollback documentado.

## Riesgo

Riesgo: bajo a medio. La principal amenaza es convertir observaciones locales en políticas generales sin evidencia suficiente.
