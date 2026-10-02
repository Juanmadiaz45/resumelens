# Test Cases

> Escenarios cubiertos por `tests/`. Actualizar conforme se implementa cada etapa.

## Stage 1 — Extraction

| ID | Escenario | Input | Resultado esperado |
|---|---|---|---|
| E1 | Résumé bien formado, skills en una línea | _(pendiente)_ | lista de términos extraídos correcta |
| E2 | Résumé sin sección de skills | _(pendiente)_ | listas vacías, sin error |
| E3 | Formatos mixtos (JS, React.js, NodeJS) | _(pendiente)_ | todos detectados como strings crudos |

## Stage 2 — Normalization (FST)

| ID | Escenario | Input | Resultado esperado |
|---|---|---|---|
| N1 | Variantes conocidas de un mismo término | `JS`, `Javascript` | ambos → `JAVASCRIPT` |
| N2 | Término no reconocido por ningún FST | _(pendiente)_ | manejo explícito (ignorar / marcar `UNKNOWN`) |
| N3 | Orden canónico por perfil | lista desordenada | lista reordenada según el perfil |

## Stage 3 — Classification (Automata)

| ID | Escenario | Input | Resultado esperado |
|---|---|---|---|
| C1 | Candidato cumple Full Stack | secuencia completa | `ACCEPTED` para Full Stack |
| C2 | Candidato cumple Machine Learning Engineer | secuencia del ejemplo del enunciado | `ACCEPTED` para ML Engineer |
| C3 | Candidato no cumple ningún perfil | secuencia incompleta/irrelevante | `REJECTED` en los 4 perfiles |
| C4 | Candidato cumple más de un perfil simultáneamente | _(pendiente)_ | `ACCEPTED` en más de uno |

## Stage 4 — DSL (textX)

| ID | Escenario | Input | Resultado esperado |
|---|---|---|---|
| D1 | Modelo de candidato válido y completo | _(pendiente)_ | validación exitosa + HTML generado |
| D2 | Modelo con campo obligatorio faltante | _(pendiente)_ | error de validación, rechazado |
| D3 | Modelo con múltiples experiencias/educación | _(pendiente)_ | parseo correcto de listas repetidas |
| D4 | Modelo con error sintáctico (token inválido) | _(pendiente)_ | rechazado por textX |

## Integración end-to-end

| ID | Escenario | Resultado esperado |
|---|---|---|
| I1 | Résumé de ejemplo del enunciado (Wednesday Addams) | pipeline completo produce `ACCEPTED` para Full Stack y HTML válido |
| I2 | Résumé de ejemplo del enunciado (Mary Jane Watson) | pipeline completo produce `ACCEPTED` para ML Engineer y HTML válido |
