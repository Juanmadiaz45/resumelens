# ResumeLens

**Team:** Flux

**Course:** Computación y Estructuras Discretas III, 2026-2, Integrative Task 1

**Members:** Juan Manuel Diaz Moreno (A00394477)

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

| Stage | Formal model | Implementation |
|---|---|---|
| 1. Information extraction | Regular expressions | `resumelens/extraction/extractor.py` (`re`) |
| 2. Qualification normalization | Finite-state transducers | `resumelens/normalization/transducers.py` (`pyformlang.fst`) |
| 3. Qualification pattern recognition | Deterministic finite automata | `resumelens/classification/automata.py` (`pyformlang`) |
| 4. Candidate profile language | Context-free grammar (EBNF) | `resumelens/dsl/candidate.tx` (`textX`) |

`resumelens/pipeline/pipeline.py` chains the four stages. `resumelens/ui/cli.py` is the command
line entry point.

## Setup

Python 3.10 or newer is required (the code uses `X | None` type hints).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running it

Screen a résumé and write its HTML page next to the input file:

```bash
python -m resumelens.ui.cli data/sample_resumes/wednesday_addams.txt
```

Write the page to a different folder with `--out-dir`:

```bash
python -m resumelens.ui.cli data/sample_resumes/mary_jane_watson.txt --out-dir output/
```

The command prints the output of each stage (extracted qualifications, normalized
qualifications, and a profile-by-profile verdict), then writes `<name>.html`. Exit codes:
`0` success, `1` the candidate profile was rejected by the grammar, `2` the input file doesn't
exist.

To regenerate the evidence files for the ten sample résumés, run the scripts in order:

```bash
python -m scripts.extract_samples     # data/extracted/
python -m scripts.normalize_samples   # data/normalized/
python -m scripts.classify_samples    # data/classified/
python -m scripts.build_profiles      # data/profiles/  (DSL, HTML, Markdown)
```

## Tests

```bash
pytest
```

The suite has 99 tests across all four stages and the command line. `docs/test_cases.md` maps
each scenario to the test that covers it.

## Repository structure

```
resumelens/            source code
  extraction/          stage 1: regular expressions
  normalization/       stage 2: finite-state transducers and canonical ordering
  classification/      stage 3: profile automata
  dsl/                 stage 4: textX grammar, serializer, parser, HTML/Markdown rendering
  pipeline/            chains the four stages
  ui/                  command-line interface
tests/                 pytest suite
data/sample_resumes/   ten sample résumés (two from the assignment statement)
data/extracted/        stage 1 output for each sample
data/normalized/       stage 2 output for each sample
data/classified/       stage 3 output for each sample
data/profiles/         stage 4 output for each sample (.candidate, .html, .md)
scripts/               regenerate the data/ outputs
docs/                  design and formalization documents
poster/                research poster
```

## Tooling

The project was developed in Visual Studio Code with Python 3.14. It uses
[pyformlang](https://pyformlang.readthedocs.io/) for the transducers and automata,
[textX](https://textx.github.io/textX/) for the candidate-profile grammar, and pytest for the
test suite.

## Design documentation

All documents are in [`docs/`](docs/):

| Document | Content |
|---|---|
| `Integrative-Task1-2026-2_CyED3.pdf` | Assignment statement |
| `literature_review.md` | Background on the four formal models and the references used |
| `profiles.md` | Definition of the four professional profiles |
| `class_notation_reference.md` | Notation and library APIs taken from the course slides |
| `design_modules.md` | Module design and interfaces between stages |
| `formalization_regex.md` | Stage 1 regular expressions |
| `formalization_fst.md` | Stage 2 transducers |
| `formalization_automata.md` | Stage 3 automata |
| `formalization_dsl.md` | Stage 4 grammar in EBNF |
| `test_cases.md` | Test scenarios and the tests that cover them |
| `ai_usage_log.md` | Record of the interactions with AI |

The research poster is in `poster/poster.html` (print it as an A1 landscape PDF from a browser).
