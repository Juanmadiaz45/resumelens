# Literature Review

ResumeLens uses four formal models in sequence: regular expressions, finite-state transducers,
finite automata, and context-free grammars. This review covers the background for each one and
records how it shaped the design. It was written before the implementation, as the assignment
asks, and the design decisions below point back to it.

## 1. Regular expressions for extraction

A regular expression describes a regular language, the class of languages recognized by finite
automata (Hopcroft, Motwani & Ullman, 2006; Sipser, 2013). In practice, regular expressions are
the standard tool for pulling fixed kinds of tokens out of semi-structured text. Karttunen et al.
(1996) show that many steps in natural language engineering, from tokenization to light parsing,
can be written in a regular-expression calculus compiled into finite-state transducers. Their
work is the closest precedent for using regular expressions as the first layer of a text
pipeline rather than as the whole solution.

**Design consequence.** Stage 1 only extracts raw strings. It doesn't decide whether two strings
mean the same thing, and it doesn't decide whether a candidate fits a profile. Keeping that line
strict lets each stage be tested on its own. The patterns use word boundaries, so that `JS` is
not found inside another word, and they use alternations for the known vocabulary. Extraction
stays case-insensitive because résumés are inconsistent about capitalization.

## 2. Finite-state transducers for normalization

A finite-state transducer is an automaton whose transitions carry an output symbol as well as an
input symbol, so it defines a relation between strings instead of a set (Mohri, 1997). Mohri's
survey describes sequential transducers and the algorithms that make them efficient to
determinize and minimize. Karttunen et al. (1996) use the same machinery for mapping
surface forms to canonical ones. Beesley and Karttunen (2003) apply finite-state transducers to
morphology, where many surface forms map to one lexical form, which is the same situation as
`Javascript`, `JS`, and `JavaScript` all meaning `JAVASCRIPT`.

**Design consequence.** Each normalization category is a small transducer with two states. Each
recognized spelling is one transition that reads the whole token and emits the canonical term.
This is possible because stage 1 already produces whole tokens, so the transducer doesn't need to
read character by character. Terms with no transition are dropped, which is the rejection
behavior the transducer model gives for free. Canonical orders per profile are applied after
normalization.

## 3. Finite automata for qualification patterns

Deterministic and nondeterministic finite automata accept the same class of languages, and every
NFA has an equivalent DFA (Hopcroft, Motwani & Ullman, 2006). A nondeterministic automaton, with
or without λ-transitions, is often easier to write, but a deterministic one is easier to check
and to implement. The choice depends on whether the input could be read in more than one way.

**Design consequence.** The four profile patterns are category sequences such as "one or more
programming languages, then one or more frontend frameworks, then one or more backend frameworks,
then a database, then Git". Stage 2 already sorts terms into the profile's category order, and
each category is disjoint from the others. So for every state and symbol there is at most one
next state. That makes each profile automaton a DFA, and `_build_dfa` checks this explicitly.
NFA or NFA-λ would be needed if the same symbol could fit two slots, or if the input weren't
sorted. Neither is the case here.

## 4. Context-free grammars and domain-specific languages

A context-free grammar generates the languages recognized by pushdown automata and is the usual
formalism for the syntax of programming languages and data formats (Chomsky, 1956; Hopcroft,
Motwani & Ullman, 2006). A domain-specific language is a small language designed for one
problem, where the grammar makes invalid descriptions impossible to write (Fowler, 2010).
textX is a Python tool that builds a parser and a metamodel from one grammar description, and
produces an object graph that conforms to that metamodel (Dejanović et al., 2017).

**Design consequence.** The candidate profile is a DSL with a fixed section order, repeatable
experience and education entries, and a closed set of degrees, profile names, and verdicts. Its
grammar is written in EBNF and implemented in textX. Membership in the canonical vocabulary is
not in the grammar itself. It is a textX object processor that uses the same `CANONICAL_TERMS`
set as the transducers. A context-free grammar could list all the terms as alternatives, but
that would duplicate the vocabulary in two places. Vocabulary violations are reported as semantic
errors, separately from syntax errors.

## 5. Tools

- **pyformlang** (Python library) implements finite automata, finite-state transducers, and
  context-free grammars. The API used in the implementation follows the examples in the course
  slides (see `class_notation_reference.md`).
- **textX** (Python library) parses DSL text into Python objects, as described above.

## 6. Gaps

- The résumé-screening literature (automated hiring, résumé parsing) was not reviewed in depth.
  The problem here is narrower: checking explicit qualifications against formal patterns. It does
  not rank candidates, and it does not use learned models. This review only covers the formal
  language background that the design depends on.
- No empirical comparison with other screening methods is included. The evaluation is limited to
  ten hand-written sample résumés.

## References

- Beesley, K. R., & Karttunen, L. (2003). *Finite State Morphology*. CSLI Publications.
- Chomsky, N. (1956). Three models for the description of language. *IRE Transactions on
  Information Theory*, 2(3), 113–124.
- Dejanović, I., Vaderna, R., Milosavljević, G., & Vuković, Ž. (2017). TextX: A Python tool for
  Domain-Specific Languages implementation. *Knowledge-Based Systems*, 115, 1–4.
- Fowler, M. (2010). *Domain-Specific Languages*. Addison-Wesley.
- Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory,
  Languages, and Computation* (3rd ed.). Addison-Wesley.
- Karttunen, L., Chanod, J.-P., Grefenstette, G., & Schiller, A. (1996). Regular expressions for
  language engineering. *Natural Language Engineering*, 2(4), 305–328.
- Mohri, M. (1997). Finite-state transducers in language and speech processing. *Computational
  Linguistics*, 23(2), 269–311.
- Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
- pyformlang documentation. https://pyformlang.readthedocs.io/
- textX documentation. https://textx.github.io/textX/
