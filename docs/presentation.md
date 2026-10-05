# Presentation Script — ResumeLens (10 minutes)

This is the speaker script for the 10-minute technical presentation. It follows the poster
(`poster/poster.html`) and covers the points the assignment requires: the problem, the formal
model behind each component, the design decisions, the results with examples of detection,
classification, transformation and validation, and the limitations.

| # | Slide | Time | Cumulative |
|---|---|---|---|
| 1 | Title and team | 0:30 | 0:30 |
| 2 | Problem | 1:00 | 1:30 |
| 3 | Architecture: four stages, four formal models | 1:00 | 2:30 |
| 4 | Stage 1: regular expressions | 1:15 | 3:45 |
| 5 | Stage 2: finite-state transducers | 1:15 | 5:00 |
| 6 | Stage 3: finite automata | 1:30 | 6:30 |
| 7 | Stage 4: the candidate grammar (textX) | 1:15 | 7:45 |
| 8 | Results: one résumé end to end, then all ten | 1:15 | 9:00 |
| 9 | Limitations and improvements | 0:45 | 9:45 |
| 10 | Questions (closing line) | 0:15 | 10:00 |

---

## Slide 1 — Title and team (0:30)

"Good morning. We are team Flux, and this is ResumeLens: a system that checks whether the
qualifications in a résumé match formally defined professional profiles."

Say the team names and the course. Then state the one-sentence claim: the system does not rank
candidates; it checks explicit qualifications against patterns.

## Slide 2 — Problem (1:00)

Points to make:
- Recruiters read many résumés, and the same skill is written in different ways: `JS`,
  `Javascript`, `JavaScript`.
- Before a pattern can be checked, the strings have to be recognized and made equivalent.
- The problem therefore has several layers: finding the strings, deciding which ones mean the
  same thing, deciding which profile pattern they satisfy, and describing the result in a
  structured form.

End with: "Each of these layers maps to a formal model we studied in the course."

## Slide 3 — Architecture (1:00)

Show the four-box pipeline from the poster:

1. Extraction — regular expressions
2. Normalization — finite-state transducers
3. Classification — finite automata (deterministic)
4. Description — context-free grammar, implemented in textX

Explain the interface between stages: each stage takes the previous stage's output and returns
a new value. Nothing is shared between stages except that value, which is what lets each stage be
tested alone.

## Slide 4 — Stage 1: regular expressions (1:15)

- Each category has one pattern: contact information, languages, frameworks, databases, cloud
  tools, data tools, education, experience, Git and REST API.
- Show one pattern from `formalization_regex.md`, for example the education pattern. Say that the
  first version failed on `B.Sc.` because of the trailing word boundary, and that the fix came
  from reasoning about how `\b` behaves next to a period.
- State the decision that is easiest to question: language names are case-sensitive, so the word
  "go" is not extracted as the Go language. The cost is that lowercase `python` is missed.

## Slide 5 — Stage 2: finite-state transducers (1:15)

- A transducer maps each recognized spelling to its canonical term. Show the `JAVASCRIPT`
  transducer from `formalization_fst.md`: two states, one transition per spelling.
- Explain why there are two states and not a character-level machine: stage 1 already produces
  whole tokens, so each token is one transition.
- Unrecognized terms have no transition, so they are dropped. Rejection comes directly from the
  model.
- Show the ordering step: the candidate's terms are sorted by each profile's category order, so
  the order the candidate wrote them in does not change the result.

## Slide 6 — Stage 3: finite automata (1:30)

- Each profile is a DFA over the canonical alphabet. Show the Full Stack automaton diagram.
- The key argument: stage 2 has already sorted the terms and the categories are disjoint, so for
  every state and symbol there is at most one next state. That makes the automaton deterministic.
  NFA or NFA-λ would be needed only if one symbol could fit two slots, which does not happen here.
- Optional qualifications are self-loops or skipped categories; the accepting state loops on the
  whole alphabet, so extra qualifications don't reject a candidate.
- The implementation checks this claim in code: building an automaton with two different targets
  for the same state and symbol raises an error.

## Slide 7 — Stage 4: the candidate grammar (1:15)

- The grammar describes one candidate: name, contact, repeatable experience and education, skills,
  and one classification result per profile.
- Show a few EBNF productions from `formalization_dsl.md`, and identify terminals (`Email`,
  `CanonicalTerm`) and non-terminals (`CandidateProfile`, `Contact`).
- Explain three validation layers: lexical (a lowercase skill fails the regex), syntactic (a
  missing section fails the grammar), and semantic (a skill outside the vocabulary fails a textX
  object processor).
- The design choice to name: the vocabulary check lives in the semantic processor, not in the
  grammar, to avoid listing 51 terms in two places.

## Slide 8 — Results (1:15)

First, one résumé end to end (Wednesday Addams):
- Raw: `JS, React.js, NodeJS, Postgres, Git`
- Normalized and sorted: `JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT`
- Classified: Full Stack Developer accepted.
- Described: a validated candidate profile and an HTML page.

Then the ten-résumé table from the poster. Point out the two cases built to match two profiles
(Full Stack + DevOps, ML + Data) and the one that matches nothing (Rick Sanchez). Note that
these results come from running the pipeline, and that the tests check them.

Examples of validation: a lowercase skill is a lexical error; `COBOL` is a semantic error.

## Slide 9 — Limitations and improvements (0:45)

- Only ten hand-written résumés were tested; no real data.
- Name extraction assumes the name is on the first line.
- Phone matching is loose and can match non-phone digits.
- Adding a new term requires changing the regex and the transducer; a shared vocabulary file
  would remove the duplication.
- Experience is one summary number, not a parsed employment history.
- Improvement: a larger, labeled résumé set, and a way to measure extraction and classification
  errors against it.

## Slide 10 — Closing and questions (0:15)

"ResumeLens is a demonstration of four formal models working as one pipeline, with each design
decision checked against its model. Thank you. We're happy to take questions."

---

## Delivery notes

- The presentation is in English. Keep the sentences short and say each formal term once when it
  first appears.
- Rehearse with a timer. The slide times add up to 10 minutes, with a small margin.
- Have the terminal ready with `python -m resumelens.ui.cli data/sample_resumes/wednesday_addams.txt`
  as a backup if a live demo is wanted.
