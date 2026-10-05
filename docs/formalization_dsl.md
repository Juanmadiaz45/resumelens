# Formalization — Stage 4: Candidate Profile DSL (textX)

The last stage turns the outputs of stages 1–3 into a small domain-specific language that
describes one candidate. The grammar lives in `resumelens/dsl/candidate.tx`; this document is
the formal description of that grammar and the reasoning behind its shape.

The stage is not there to decide anything. Extraction, normalization, and classification have
already decided what the candidate's qualifications are and which profiles they satisfy. The
DSL's job is to represent that result in a fixed, checkable structure, and to reject any
representation that breaks the structure. Keeping those two responsibilities apart is also why
serialization (`dsl/serializer.py`) and parsing (`dsl/model.py`) are separate: the code that
produces candidate text is not trusted to produce valid text, and the grammar is the only thing
that decides it.

## EBNF

Non-terminals are written in CamelCase, terminals in quotes or as named lexical rules.
Repetition is `{ … }` (zero or more), `{ … }+` (one or more), and optional is `[ … ]`.

```ebnf
CandidateProfile  = "candidate" , Name ,
                    Contact ,
                    { Experience } ,
                    { Education } ,
                    "skills" , Skill , { Skill } ,
                    "classification" , ProfileResult , { ProfileResult } ;

Name              = STRING ;

Contact           = "contact" ,
                    [ "email" , Email ] ,
                    [ "phone" , Phone ] ,
                    [ "linkedin" , LinkedinUrl ] ,
                    [ "github" , GithubUrl ] ;

Experience        = "experience" , INT , "years" ;

Education         = "education" , Degree , STRING ;

Skill             = CanonicalTerm ;

ProfileResult     = ProfileName , Verdict ;

Degree            = "B.Sc." | "M.Sc." | "Bachelor" | "Master" | "PhD" ;

ProfileName       = "FULL_STACK_DEVELOPER" | "MACHINE_LEARNING_ENGINEER"
                  | "DEVOPS_ENGINEER"      | "DATA_ENGINEER" ;

Verdict           = "ACCEPTED" | "REJECTED" ;
```

The grammar in `candidate.tx` writes the same productions in textX syntax (`attr=Rule`,
`attr*=Rule`, `attr+=Rule`, and `( … )?` for the optional groups). The only differences are
cosmetic: textX requires `*=` and `+=` for repeated attributes, and it expresses the optional
contact fields as individual optional groups rather than as an EBNF bracket.

### Terminals

| Terminal | Definition | Recognizes |
|---|---|---|
| `STRING` | textX built-in: double-quoted string | `"Peter Parker"`, `"Computer Science"` |
| `INT` | textX built-in: integer | `4`, `6` |
| `Email` | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` | `peter.parker@example.com` |
| `Phone` | `\+?\d[\d\-.\s()]{6,}\d` | `+1-555-010-2030` |
| `LinkedinUrl` | `(https?://)?(www\.)?linkedin\.com/in/[\w-]+` | `linkedin.com/in/tonystark` |
| `GithubUrl` | `(https?://)?(www\.)?github\.com/[\w-]+` | `github.com/peterparker` |
| `CanonicalTerm` | `[A-Z][A-Z0-9_]*` (uppercase snake case) | `GIT`, `NODE_JS`, `POSTGRESQL` |
| keywords | `candidate`, `contact`, `email`, `phone`, `linkedin`, `github`, `experience`, `years`, `education`, `skills`, `classification`, the degree literals, the profile names, and the verdicts | fixed strings |

`CanonicalTerm` is a lexical rule, not a list of 51 alternatives. A lowercase raw term such as
`javascript` doesn't match it at all, so it's a lexical error. A term that matches the pattern
but isn't in the canonical vocabulary (`COBOL`) gets through the lexer and is rejected by a
semantic check, described below.

### Non-terminals

`CandidateProfile` (the root), `Contact`, `Experience`, `Education`, `Skill`, `ProfileResult`.
`Name`, `Degree`, `ProfileName`, and `Verdict` are also non-terminals in the EBNF, but in textX
they're represented as attributes or match rules rather than as separate classes.

## Structural characteristics

- **Fixed section order.** The sections come in the order `candidate`, `contact`,
  experiences, educations, `skills`, `classification`. A representation that puts `skills` before
  `contact` is a syntax error. This is a deliberate choice: the order is the language, and a
  fixed order makes every candidate file look the same, which matters once several candidates
  are being compared or rendered side by side.
- **Repeated elements.** Experiences and educations can each repeat zero or more times
  (`{ Experience }`, `{ Education }`). Skills and classification results need at least one
  entry, because a candidate with no skills has no profile to classify.
- **Optional contact fields.** Each contact field may be absent, but the `contact` keyword is
  always present, so an empty contact section is still a valid section.
- **Closed vocabularies.** Degrees, profile names, and verdicts are finite enumerations written
  directly in the grammar. Skills are the one open-ended category, constrained by the
  vocabulary check below.

## Validation layers

A representation can fail for three different reasons, and the grammar catches them at three
different levels.

1. **Lexical.** A token doesn't match any terminal. Example: `skills javascript` (lowercase)
   or `email peter@` (no top-level domain). textX raises a syntax error at the position of the
   bad token.
2. **Syntactic.** The tokens are individually valid, but the sequence isn't. Example: a `skills`
   section with no skills, a `classification` section that comes before `skills`, or an unknown
   keyword such as `seniority`.
3. **Semantic.** The sequence parses, but one value doesn't mean anything for ResumeLens.
   Example: `COBOL` as a skill. The `CanonicalTerm` object processor in `dsl/model.py` checks
   the value against `CANONICAL_TERMS` (the output alphabet of the stage 2 transducers) and
   raises a semantic error if it isn't a member.

The third layer is a choice worth being explicit about. A context-free grammar can't express "a
string that is one of these 51 specific words" without listing all 51 as alternatives. That's
technically possible, but it would tie the grammar file to the transducer tables, so any new
canonical term would have to be added in two places. Moving the membership check to a semantic
processor keeps the grammar about structure, and keeps the vocabulary in one place, the
transducers. The cost is that vocabulary violations are reported as semantic errors rather than
syntax errors, which the tests check explicitly.

`parse_candidate` converts textX's exceptions into a single `CandidateValidationError`, so a
caller only has to handle one exception type whatever layer rejected the input. `validate`
wraps the same call and returns `(valid, errors)`.

## Rejection cases

| Case | Example | Layer | Result |
|---|---|---|---|
| Lowercase skill | `skills javascript` | lexical | rejected |
| Malformed email | `email peter@` | lexical | rejected |
| Unknown keyword | `seniority 4 years` | syntactic | rejected |
| Missing skills section | no `skills` line | syntactic | rejected |
| Skill outside vocabulary | `skills COBOL` | semantic | rejected: `'COBOL' is not a canonical qualification` |
| Unknown degree | `education Diploma "…"` | syntactic | rejected |
| Unknown profile name | `ASTRONAUT ACCEPTED` | syntactic | rejected |

## Rendered output

A validated model is rendered two ways (`dsl/render.py`). The HTML page has a title, the contact
details, the experience and education summaries, the skills as tags, and the classification as
a list with accepted profiles highlighted. The Markdown version has the same sections as plain
headings and lists. Every value that comes from the candidate's text is escaped before it goes
into the HTML, so a name containing markup is shown as text instead of being interpreted.

## What the grammar doesn't enforce

- **Not every profile has to appear.** `classification` needs at least one `ProfileResult`, but
  the pipeline always writes all four, so this is a choice of the serializer, not of the grammar.
- **Experience isn't attributed.** An `Experience` records a number of years, not an employer or
  role, because stage 1 extracts only the summary sentence. The grammar could carry more detail
  later without changing the existing productions.
- **Skill order isn't enforced.** The grammar accepts skills in any order. Canonical ordering is
  stage 2's responsibility and is applied per profile before classification. The DSL keeps the
  order it is given, which is the extraction order (languages, then frameworks, databases, cloud
  tools, data tools, and tools), not the order the skills appear in the résumé text.
