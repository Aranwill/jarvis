---
id: STD-001
title: Coding Standards

artifact_type: Standard

status: Published
version: 1.0.1

domain: Development

technologies:
  - Python

tags:
  - Coding
  - Standards
  - Development

related:
  - DOC-AKS-002
  - DOC-AKS-003

author: Hector Rodriguez
reviewed_by:

created_at: 2026-07-09
updated_at: 2026-10-03
language: es
---

# Descripción general

## Propósito

Definir los estándares mínimos de código que toda contribución a Malāk debe
cumplir.

---

## Alcance

Estos estándares aplican a todo el código fuente incorporado al proyecto.

---

# Contenido

## Principios generales

- priorizar legibilidad sobre ingenio innecesario;
- preferir código explícito sobre comportamiento implícito;
- mantener las funciones enfocadas en una única responsabilidad;
- evitar lógica duplicada;
- utilizar nombres significativos;
- favorecer composición sobre herencia innecesaria;
- escribir código fácil de probar.

## Documentación

- los módulos públicos deberían incluir documentación;
- las decisiones complejas deberían documentarse en el AKS;
- todo cambio arquitectónico debe ser trazable.

## Testing

- la funcionalidad nueva debería incluir los tests correspondientes;
- los tests existentes deben continuar pasando;
- las regresiones deberían corregirse antes del merge.

---

# Consideraciones de diseño

Estos estándares definen la calidad mínima de ingeniería esperada en el
proyecto.

Podrán agregarse estándares adicionales en futuras revisiones.

---

# Artefactos relacionados

- DOC-AKS-002
- DOC-AKS-003

---

# Referencias

- Clean Code — Robert C. Martin
- The Pragmatic Programmer

---

# Historial de revisiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0.0 | 2026-07-09 | Versión inicial. |
| 1.0.1 | 2026-10-03 | Normalización del contenido explicativo al español, preservando términos técnicos canónicos en su idioma original. |
