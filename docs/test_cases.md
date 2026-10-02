# Test Cases

Scenarios covered by `tests/`. This gets filled in as each stage is implemented; for now it
lists the cases the implementation will need to handle.

## Stage 1 — Extraction

| ID | Scenario | Input | Expected result |
|---|---|---|---|
| E1 | Well-formed résumé, skills on one line | see `data/sample_resumes/wednesday_addams.txt` | all listed skills extracted as raw strings |
| E2 | Résumé with no skills section | _(pending)_ | empty lists, no crash |
| E3 | Mixed naming formats in the same list | `JS, React.js, NodeJS` | all three detected as separate raw strings |
| E4 | Years of experience in different phrasings | `"3 years of experience"`, `"4+ years"` | experience value correctly captured |

## Stage 2 — Normalization (FST)

| ID | Scenario | Input | Expected result |
|---|---|---|---|
| N1 | Known variants of the same term | `JS`, `Javascript` | both map to `JAVASCRIPT` |
| N2 | Term not recognized by any transducer | _(pending)_ | handled explicitly (dropped or flagged `UNKNOWN`) |
| N3 | Canonical ordering per profile | unordered list | list reordered according to the profile's canonical order |

## Stage 3 — Classification (automata)

| ID | Scenario | Input | Expected result |
|---|---|---|---|
| C1 | Candidate matches Full Stack Developer | full sequence | `ACCEPTED` for Full Stack |
| C2 | Candidate matches Machine Learning Engineer | sequence from the assignment example | `ACCEPTED` for ML Engineer |
| C3 | Candidate matches DevOps Engineer | see `devops_1.txt` | `ACCEPTED` for DevOps |
| C4 | Candidate matches Data Engineer | see `data_engineer_1.txt` | `ACCEPTED` for Data Engineer |
| C5 | Candidate matches no profile | see `insufficient_profile.txt` | `REJECTED` on all four profiles |
| C6 | Candidate matches more than one profile | see `mixed_ml_data.txt` | `ACCEPTED` on more than one profile |

## Stage 4 — DSL (textX)

| ID | Scenario | Input | Expected result |
|---|---|---|---|
| D1 | Valid, complete candidate model | _(pending)_ | validates successfully, HTML generated |
| D2 | Model missing a required field | _(pending)_ | validation error, rejected |
| D3 | Model with multiple experiences / education entries | _(pending)_ | repeated elements parsed correctly |
| D4 | Model with a syntax error (invalid token) | _(pending)_ | rejected by textX |

## End-to-end integration

| ID | Scenario | Expected result |
|---|---|---|
| I1 | `wednesday_addams.txt` through the full pipeline | `ACCEPTED` for Full Stack, valid HTML output |
| I2 | `mary_jane_watson.txt` through the full pipeline | `ACCEPTED` for ML Engineer, valid HTML output |
| I3 | `insufficient_profile.txt` through the full pipeline | `REJECTED` on all profiles, HTML still generated with the rejection noted |
