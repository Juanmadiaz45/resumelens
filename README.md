# ResumeLens

**Team:** Flux
**Course:** Computación y Estructuras Discretas III — 2026-2, Integrative Task 1
**Members:** _(add full name)_

ResumeLens is a résumé-screening system built on formal language theory. It takes a résumé as
plain text, runs it through four processing stages, and determines whether the qualifications
found in it satisfy the pattern of one or more professional profiles.

The system does not rank candidates or make hiring decisions. It only checks whether the
qualifications explicitly stated in a résumé match a formally defined pattern.

## Supported profiles

See [`docs/profiles.md`](docs/profiles.md) for the full definition of each one.

1. **Full Stack Developer** (predefined by the assignment)
2. **Machine Learning Engineer** (predefined by the assignment)
3. **DevOps Engineer** (software engineering profile defined by the team)
4. **Data Engineer** (AI/data profile defined by the team)

## Pipeline

| Stage | Formal model | Folder |
|---|---|---|
| 1. Information extraction | Regular expressions (`re`) | `resumelens/extraction/` |
| 2. Qualification normalization | Finite-state transducers (`pyformlang`) | `resumelens/normalization/` |
| 3. Qualification pattern recognition | Finite automata (`pyformlang`) | `resumelens/classification/` |
| 4. Candidate profile language | Context-free grammar (`textX`) | `resumelens/dsl/` |

`resumelens/pipeline/` chains the four stages together. `resumelens/ui/` exposes a CLI to run
the pipeline on a résumé file and produce the final visualization.

## Repository structure

```
resumelens/            source code for the system
  extraction/           stage 1 - regex
  normalization/        stage 2 - finite-state transducers
  classification/       stage 3 - automata
  dsl/                  stage 4 - textX grammar + HTML/Markdown rendering
  pipeline/             chains the four stages together
  ui/                   CLI entry point
tests/                 unit and integration tests (pytest)
data/sample_resumes/   sample résumés used for development and demos
docs/                  design and formalization documents
poster/                research poster
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running it (placeholder, will be updated as the implementation progresses)

```bash
python -m resumelens.ui.cli data/sample_resumes/<file>.txt
```

## Tests

```bash
pytest
```

## Tooling

- IDE: _(add, e.g. VS Code / PyCharm)_
- Python 3.x
- [pyformlang](https://pyformlang.readthedocs.io/) for the transducers and automata
- [textX](https://textx.github.io/textX/) for the candidate-profile DSL

## Design documentation

See [`docs/`](docs/):

- `literature_review.md`
- `profiles.md`
- `class_notation_reference.md`
- `design_modules.md`
- `formalization_regex.md`
- `formalization_fst.md`
- `formalization_automata.md`
- `formalization_dsl.md`
- `test_cases.md`
