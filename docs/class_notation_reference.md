# Class Notation Reference

Notes pulled from the course slides (Computación y Estructuras Discretas III, 2026-2) so the
formalization documents and the implementation follow the same conventions used in class,
instead of generic textbook notation that happens to differ in small but grading-relevant ways.
This is a reference for writing the other `docs/formalization_*.md` files, not a deliverable on
its own.

## Finite automata

The slides define a DFA as:

> M = (Σ, Q, q0, F, δ), where δ : Q × Σ → Q

and an NFA as:

> M = (Σ, Q, q0, F, Δ), where Δ : Q × Σ → ℘(Q)

Two things worth carrying over into our docs even though the assignment statement writes the
tuple in a different order (Q, Σ, δ, q0, F):

- The class **uses a capital Δ for the non-deterministic transition relation** and reserves
  lowercase δ for the deterministic transition function. That distinction is a clean way to
  answer the assignment's "what type of automaton is this and why" question — if the alphabet
  maps each (state, symbol) pair to a single state, it's δ and the automaton is a DFA; if it maps
  to a set of states, it's Δ and the automaton is an NFA.
- λ-transitions are **not** called "ε-NFA" in class, they're called **NFA-λ**, and the λ symbol
  (not ε) is used throughout. The transition relation for an NFA-λ is
  Δ : Q × (Σ ∪ {λ}) → ℘(Q).

We keep the assignment's required tuple order, M = (Q, Σ, δ, q0, F), in
`formalization_automata.md`, but use δ/Δ and λ consistently with what was taught.

## Finite-state transducers

The class definition matches the assignment's tuple order exactly:

> Deterministic FST: M = (Q, Σ, Γ, δ, ω, q0, F)
> δ : Q × (Σ ∪ {λ}) → Q
> ω : Q × (Σ ∪ {λ}) → Γ
>
> Non-deterministic FST: same tuple, but
> δ : Q × (Σ ∪ {λ}) → ℘(Q)
> ω : Q × (Σ ∪ {λ}) → Γ ∪ {λ}

So for `formalization_fst.md`, no reordering is needed — just write δ and ω with λ in the domain
instead of ε, matching the automata notation above.

## pyformlang — automata (stage 3)

```python
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State

q0 = State("q0")
q1 = State("q1")

dfa = DeterministicFiniteAutomaton(
    states={q0, q1},
    input_symbols={"0", "1"},
    start_state=q0,
    final_states={q0},
)
dfa.add_transitions([(q0, "0", q1), (q0, "1", q1), (q1, "0", q0), (q1, "1", q0)])
dfa.accepts("00")
```

```python
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

nfa = NondeterministicFiniteAutomaton()
nfa.add_transition("q0", "a", "q1")
nfa.add_start_state("q0")
nfa.add_final_state("q1")
nfa.accepts("a")
```

```python
from pyformlang.finite_automaton import EpsilonNFA

enfa = EpsilonNFA()
enfa.add_transition("q0", "a", "q1")
enfa.add_transition("q1", "epsilon", "q2")  # the library's literal string for a λ-transition
```

For ResumeLens, states will be named after the normalized qualification they represent (e.g.
`q_python`, `q_pandas`) and the input symbols will be the canonical terms coming out of stage 2
— not single characters — which pyformlang supports as-is since symbols are just strings.

## pyformlang — finite-state transducers (stage 2)

```python
from pyformlang.fst import FST

transducer = FST()
transducer.add_transitions([
    ("q0", "a", "q1", ["x"]),
    ("q1", "b", "q2", ["y"]),
])
transducer.add_start_state("q0")
transducer.add_final_state("q2")
list(transducer.translate("ab"))  # generator of output sequences
```

Two details confirmed directly from the slides' own examples:

- A transition's input symbol doesn't have to be a single character — the professor's own
  example uses whole substrings (`"llor"`, `"ar"`) as one transition. That's exactly what we
  need: one transition per raw qualification string (`"JS"`, `"Javascript"`) mapping straight to
  its canonical form (`"JAVASCRIPT"`), no need to go character by character.
- λ-transitions in `pyformlang.fst.FST` are written with the literal string `"epsilon"`, not
  `"lambda"` — that's a library quirk to keep in mind even though the course calls them
  λ-transitions in the theory.

## textX (stage 4)

```python
from textx import metamodel_from_file

candidate_mm = metamodel_from_file("candidate.tx")
candidate_model = candidate_mm.model_from_file("example.candidate")
```

Grammar rule conventions used in the class examples:

```
InitialCommand:
    'initial' x=INT ',' y=INT
;

MoveCommand:
    direction=Direction (steps=INT)?
;

Direction:
    "up" | "down" | "left" | "right"
;

Comment:
    /\/\/.*$/
;
```

Relevant for our DSL: attribute assignment (`field=Type`), optional elements (`(...)?`), choice
between quoted literals for enums (`Direction`), and a regex-based terminal when a plain literal
isn't enough. Model objects are accessed from Python by attribute name and by iterating list
attributes (e.g. `model.commands`), and the class type of an instance is checked via
`obj.__class__.__name__` — useful for `render_html`/`render_markdown` when walking the model
tree.

A meta-model can be visualized with `textx generate candidate.tx --target dot`, producing a
`.dot` file that can be rendered to PNG with `pydot`. Worth doing once the grammar is stable, as
supporting material for the presentation.

## Scope note on normal forms (CNF/GNF, CYK)

The course covers Chomsky Normal Form, Greibach Normal Form, and the CYK algorithm in later
decks, which maps to RAA3. The ResumeLens assignment itself, however, does not ask for the
candidate-profile grammar to be converted to a normal form or parsed with CYK — stage 4 only
asks for an EBNF definition, a textX implementation, validation, and a rendered visualization.
No normal-form conversion is planned for the deliverable unless the assignment is revised to ask
for one explicitly.
