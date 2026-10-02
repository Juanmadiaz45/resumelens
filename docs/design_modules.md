# Design — Modules

## Pipeline overview

```
raw résumé (txt)
      │
      ▼
[1] extraction  ──► lista de strings crudos por categoría
      │
      ▼
[2] normalization ──► calificaciones canónicas, ordenadas por perfil
      │
      ▼
[3] classification ──► {perfil: ACCEPTED | REJECTED} para los 4 perfiles
      │
      ▼
[4] dsl (textX) ──► modelo de candidato validado + visualización HTML/Markdown
```

## Module: `resumelens.extraction`

| Función | Input | Output |
|---|---|---|
| `extract_contact(text: str)` | texto crudo del résumé | `dict` con email, teléfono, LinkedIn/GitHub |
| `extract_languages(text: str)` | texto crudo | `list[str]` lenguajes de programación detectados |
| `extract_frameworks(text: str)` | texto crudo | `list[str]` frameworks/librerías |
| `extract_databases(text: str)` | texto crudo | `list[str]` bases de datos |
| `extract_experience(text: str)` | texto crudo | `dict` años de experiencia, roles |
| `extract_education(text: str)` | texto crudo | `list[dict]` formación académica |
| `extract_tools(text: str)` | texto crudo | `list[str]` herramientas (Git, Docker, etc.) |
| `extract_all(text: str)` | texto crudo | `dict` consolidado de todas las anteriores |

## Module: `resumelens.normalization`

| Función | Input | Output |
|---|---|---|
| `normalize(raw_terms: list[str])` | strings crudos de la Etapa 1 | `list[str]` términos canónicos (vía FST) |
| `sort_by_profile_order(terms: list[str], profile: str)` | términos normalizados + nombre de perfil | `list[str]` ordenados canónicamente |

## Module: `resumelens.classification`

| Función | Input | Output |
|---|---|---|
| `classify(sequence: list[str])` | secuencia normalizada y ordenada | `dict[str, str]` resultado ACCEPTED/REJECTED por los 4 perfiles |

## Module: `resumelens.dsl`

| Función | Input | Output |
|---|---|---|
| `build_candidate_model(extracted, normalized, classification)` | resultados de las etapas 1–3 | instancia de modelo textX (`.candidate`) |
| `validate(model)` | modelo textX | `bool` + errores si los hay |
| `render_html(model)` / `render_markdown(model)` | modelo validado | string HTML/Markdown |

## Module: `resumelens.pipeline`

| Función | Input | Output |
|---|---|---|
| `run(text: str)` | texto crudo del résumé | reporte final (dict + HTML generado) |

## Module: `resumelens.ui`

- CLI: `python -m resumelens.ui.cli <ruta_resume.txt>` — corre el pipeline completo e imprime
  el resultado de cada etapa + abre/guarda el HTML final.

## Diagrama de flujo de datos

_(agregar imagen o diagrama Mermaid una vez cerrado el diseño de cada etapa)_
