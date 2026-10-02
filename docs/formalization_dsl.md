# Formalization — Stage 4: Candidate Profile DSL (textX)

## Grammar (EBNF)

To be defined in `resumelens/dsl/candidate.tx`. Summary in EBNF here, identifying terminals and
non-terminals.

```
CandidateProfile ::= PersonalInfo ContactInfo Experience* Education* Skills ClassificationResult+
...
```

_(fill in with the actual grammar once implemented)_

### Terminals

- _(pending, e.g. STRING, INT, EMAIL, etc.)_

### Non-terminals

- _(pending, e.g. PersonalInfo, ContactInfo, Experience, Education, Skills, ClassificationResult)_

## Structural characteristics of the language

- _(supports repeated elements: multiple experiences, education entries, skills)_
- _(lexical/syntactic rules that trigger rejection)_

## Validation

- Valid cases: _(pending)_
- Cases that must be rejected: _(pending — lexical or syntactic violations)_

## Visualization

- Output: HTML or Markdown generated from the validated model (`render_html` / `render_markdown`)
- _(add an example output once implemented)_
