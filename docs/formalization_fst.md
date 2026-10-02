# Formalization — Stage 2: Finite-State Transducers

For each transducer: the complete 7-tuple M = (Q, Σ, Γ, δ, ω, q0, F), a diagram, and a pointer
to its implementation in `resumelens/normalization/transducers.py` (pyformlang).

This matches the definition used in class (see `class_notation_reference.md`) exactly, including
the tuple order. Per that definition: δ : Q × (Σ ∪ {λ}) → Q and ω : Q × (Σ ∪ {λ}) → Γ for a
deterministic FST; for a non-deterministic one, δ : Q × (Σ ∪ {λ}) → ℘(Q) and
ω : Q × (Σ ∪ {λ}) → Γ ∪ {λ}. Use λ (not ε) consistently, same as the automata docs.

## Transducer: `<name, e.g. Programming Language Normalizer>`

- **Q (states):** _(pending)_
- **Σ (input alphabet):** _(pending)_
- **Γ (output alphabet):** _(pending)_
- **δ (transition relation, domain includes λ):** _(pending)_
- **ω (output relation, domain includes λ):** _(pending)_
- **q0 (initial state):** _(pending)_
- **F (accepting states):** _(pending)_
- **Transformations covered:** `(e.g. JS → JAVASCRIPT, Javascript → JAVASCRIPT, ...)`
- **Diagram:** _(add image or Mermaid)_

## Transducer: `<next category>`

_(repeat the structure above — at least one transducer is needed per qualification category:
programming languages, frameworks, databases, cloud/DevOps tools, data engineering tools)_

## Canonical order per profile (`sort_by_profile_order`)

| Profile | Canonical order |
|---|---|
| Full Stack Developer | Frontend → Backend → Database → Version control |
| Machine Learning Engineer | _(pending)_ |
| DevOps Engineer | _(pending)_ |
| Data Engineer | _(pending)_ |
