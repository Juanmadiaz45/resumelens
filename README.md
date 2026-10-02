# ResumeLens

**Equipo:** Flux
**Curso:** Computación y Estructuras Discretas III — 2026-2, Integrative Task 1
**Integrantes:** _(agregar nombre completo)_

ResumeLens es un sistema de cribado de hojas de vida (résumés) basado en teoría de lenguajes
formales. Procesa un résumé en texto plano a través de cuatro etapas y determina si las
calificaciones identificadas satisfacen el patrón de uno o más perfiles profesionales.

> El sistema **no** rankea candidatos ni toma decisiones de contratación: solo valida si las
> calificaciones explícitas en el résumé cumplen un patrón formalmente definido.

## Perfiles soportados

1. **Full Stack Developer** (predefinido)
2. **Machine Learning Engineer** (predefinido)
3. _(perfil de software engineering a definir por el equipo)_
4. _(perfil de AI/data a definir por el equipo)_

## Pipeline

| Etapa | Modelo formal | Carpeta |
|---|---|---|
| 1. Extracción de información | Expresiones regulares (`re`) | `resumelens/extraction/` |
| 2. Normalización de calificaciones | Transductores de estados finitos (`pyformlang`) | `resumelens/normalization/` |
| 3. Reconocimiento de patrones de perfil | Autómatas finitos (`pyformlang`) | `resumelens/classification/` |
| 4. Lenguaje de perfil de candidato | Gramática libre de contexto (`textX`) | `resumelens/dsl/` |

`resumelens/pipeline/` orquesta las cuatro etapas en secuencia; `resumelens/ui/` expone una
interfaz (CLI) para correr el pipeline sobre un résumé y generar la visualización final.

## Estructura del repositorio

```
resumelens/          # código fuente del sistema
  extraction/         # Etapa 1 - regex
  normalization/       # Etapa 2 - FST
  classification/       # Etapa 3 - autómatas
  dsl/                   # Etapa 4 - gramática textX + render HTML/Markdown
  pipeline/               # orquestación de las 4 etapas
  ui/                       # interfaz de uso (CLI)
tests/                # pruebas unitarias e de integración (pytest)
data/sample_resumes/  # résumés de ejemplo usados para pruebas y demo
docs/                 # documentos de diseño y formalización (markdown)
poster/               # poster de investigación
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cómo correr (placeholder, se actualizará conforme avance la implementación)

```bash
python -m resumelens.ui.cli data/sample_resumes/<archivo>.txt
```

## Pruebas

```bash
pytest
```

## Herramientas usadas

- IDE: _(agregar, p. ej. VS Code / PyCharm)_
- Python 3.x
- [pyformlang](https://pyformlang.readthedocs.io/) para transductores y autómatas
- [textX](https://textx.github.io/textX/) para la gramática del DSL de perfil de candidato

## Documentación de diseño

Ver carpeta [`docs/`](docs/):

- `literature_review.md`
- `design_modules.md`
- `formalization_regex.md`
- `formalization_fst.md`
- `formalization_automata.md`
- `formalization_dsl.md`
- `test_cases.md`
