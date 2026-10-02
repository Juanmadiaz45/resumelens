# Formalization — Stage 3: Finite Automata

For each profile: the complete 5-tuple M = (Q, Σ, δ, q0, F), the automaton type (DFA/NFA/NFA-λ)
with justification, a transition diagram, an explanation of the pattern it represents, and a
pointer to its implementation in `resumelens/classification/automata.py` (pyformlang).

Following the notation used in class (see `class_notation_reference.md`): the transition
relation is written **δ** when it is a function Q × Σ → Q (deterministic, one state in, one
state out) and **Δ** when it is a relation Q × Σ → ℘(Q) (non-deterministic, one state in, a set
of possible states out). λ-transitions extend the domain to Q × (Σ ∪ {λ}); an automaton with
them is called an **NFA-λ** here, not "ε-NFA", again to match the course's own terminology.

## Automaton: Full Stack Developer

- **Q (states):** _(pending)_
- **Σ (alphabet):** _(pending — canonical terms coming out of stage 2)_
- **δ / Δ (transition function/relation):** _(pending — use δ if deterministic, Δ if not)_
- **q0 (initial state):** _(pending)_
- **F (accepting states):** _(pending)_
- **Type:** DFA / NFA / NFA-λ — _(justify based on whether the transition relation is
  single-valued, multi-valued, or includes λ)_
- **Pattern represented:** _(explain)_
- **Diagram:** _(add)_

## Automaton: Machine Learning Engineer

_(same structure)_

## Automaton: DevOps Engineer

_(same structure)_

## Automaton: Data Engineer

_(same structure)_

## Classification example

```
Input (from stage 2): PYTHON, PANDAS, TENSORFLOW, POSTGRESQL, GIT
Profile pattern: MACHINE_LEARNING_ENGINEER
Output: ACCEPTED
```
