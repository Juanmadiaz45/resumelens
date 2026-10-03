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
| N2 | Term not recognized by any transducer | `"COBOL"` | dropped from the normalized list (see `normalize()` in `transducers.py`) |
| N3 | Canonical ordering per profile | unordered list | list reordered according to the profile's canonical order |

## Stage 3 — Classification (automata)

| ID | Scenario | Input | Expected result |
|---|---|---|---|
| C1 | Candidate matches Full Stack Developer | `wednesday_addams.txt` | `ACCEPTED` for Full Stack |
| C2 | Candidate matches Machine Learning Engineer | `mary_jane_watson.txt` (the assignment's own example) | `ACCEPTED` for ML Engineer |
| C3 | Candidate matches DevOps Engineer | `tony_stark.txt` | `ACCEPTED` for DevOps |
| C4 | Candidate matches Data Engineer | `hermione_granger.txt` | `ACCEPTED` for Data Engineer |
| C5 | Candidate matches no profile | `rick_sanchez.txt` | `REJECTED` on all four profiles |
| C6 | Candidate matches more than one profile | `daenerys_targaryen.txt` (Full Stack + DevOps), `eleven.txt` (ML Engineer + Data Engineer) | `ACCEPTED` on more than one profile |
| C7 | Optional qualification missing doesn't block acceptance | `mary_jane_watson.txt` has no Scikit-learn; `michael_scott.txt` has no Linux | `ACCEPTED` for their respective profiles anyway |
| C8 | Database category accepts any recognized DB term, not just literally "SQL" | `wednesday_addams.txt` has `POSTGRESQL`, not `SQL` | `ACCEPTED` for Full Stack |

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
| I3 | `rick_sanchez.txt` through the full pipeline | `REJECTED` on all profiles, HTML still generated with the rejection noted |
