# AI Usage Log

The course's AI-use level for this task is "3. Collaboration with AI". The assignment requires a
record of the interactions with the AI, including the prompts used and the content written by
the student, and evidence that the student understood and could change the generated results.

**Status: draft.** This log was reconstructed from the conversation history of the working
session. The prompts below are paraphrased, not exact copies. Before submitting, the student
should replace each paraphrase with the exact prompt where it is available, and fill in the
"Student changes" field for each entry.

Tool used: Claude Code (Claude model), in the terminal, working in this repository.

## Interactions

| # | Date | Request (paraphrased) | What the AI produced | Student changes / decisions |
|---|---|---|---|---|
| 1 | 2026-10-01 | Summarize the assignment PDF and list what must be delivered. | Summary of the problem, the four stages, and the deliverables. | _(to be completed)_ |
| 2 | 2026-10-01 | Build a full plan and task list for solo work over the deadline. | Day-by-day plan with checklists. | _(to be completed)_ |
| 3 | 2026-10-01 | Set up the repository and folder structure. | Git repository, folder scaffold, `.gitignore`, `requirements.txt`, README and doc stubs. | _(to be completed)_ |
| 4 | 2026-10-01 | Translate all documentation to English and complete the day-2 deliverables (design of modules, sample résumés, regex categories). | English documentation, module signatures, eight sample résumés, regex draft. | _(to be completed)_ |
| 5 | 2026-10-02 | Use conventional commit messages in lowercase, without co-author lines, and publish to GitHub. | Rewritten commit messages and history, repository creation. | Chose repository visibility (public) and name. |
| 6 | 2026-10-02 | Implement stage 1 (regular expressions) and add test data. | Extractor, sample data extraction script, pytest suite. Two regex bugs were found and fixed. | _(to be completed)_ |
| 7 | 2026-10-02 | Align the notation with the class slides. | Text extraction from the lecture PDFs and a notation reference. | Provided the lecture slides. |
| 8 | 2026-10-02 | Formalize the six transducers (day 4). | Formal 7-tuples, transition tables, and diagrams for each transducer. | Followed the day-4 plan. _(to be completed)_ |
| 9 | 2026-10-02 | Implement stage 2 with pyformlang, plus ordering by profile (day 5). | Transducer code, ordering function, tests, normalization script. | _(to be completed)_ |
| 10 | 2026-10-02 | Formalize the four automata and check them against the sample résumés (day 6). | Simulation of the patterns, DFA formalization, and worked examples. The AI noticed that two mixed sample résumés did not match both profiles and changed their skills so they did. This change was made by the AI, not requested explicitly. | _(to be completed)_ |
| 11 | 2026-10-04 | Implement stage 3 with pyformlang (day 7). | Automata code, determinism check, tests, classification script. | _(to be completed)_ |
| 12 | 2026-10-05 | Implement stage 4 (day 8): textX grammar, parser, rendering. | `candidate.tx`, serializer, parser, HTML and Markdown rendering, tests. | _(to be completed)_ |
| 13 | 2026-10-05 | Complete the CLI, integration tests, test case table, and README (day 9). | CLI, integration tests, updated documentation. | _(to be completed)_ |
| 14 | 2026-10-05 | Review the project against the assignment. | List of missing deliverables and inconsistencies. | Decided which items to complete. |
| 15 | 2026-10-05 | Write the literature review, correct the regex and profile documentation, and draft the poster and presentation. | Literature review (references checked with web search), corrected regex and profile docs, `poster/poster.html`, `docs/presentation.md`, and this log. | _(to be completed)_ |

## Verification of AI output

- The pytest suite (99 tests) was run after each change, and the sample outputs were regenerated
  from the scripts.
- The references in `docs/literature_review.md` were checked with web search. Confirmed: Mohri
  (1997), *Computational Linguistics* 23(2), pp. 269–311; Dejanović et al. (2017), *Knowledge-Based
  Systems* 115; Beesley & Karttunen (2003), CSLI; Chomsky (1956), *IRE Transactions on Information
  Theory* 2(3), pp. 113–124; Fowler (2010), Addison-Wesley; Hopcroft, Motwani & Ullman (2006), 3rd
  edition, Addison-Wesley; Sipser (2012), 3rd edition, Cengage. Corrected during the check: the
  Sipser year (2012, not 2013) and the textX venue (*Knowledge-Based Systems*, not MODELSWARD).
  **Not confirmed:** the page range of Karttunen et al. (1996). The sources found give an
  impossible range, so the entry is marked "[page range not verified]". The student must find
  the page numbers before submission.
- The poster's guide (CWU library, research posters) was read through web fetch. Its layout
  numbers are the tool's summary of the guide, not a direct quotation.

## Corrections the student should know about

The AI made several mistakes during this work, which were caught by tests or by review:

- A regex in the education pattern silently failed on `B.Sc.` (fixed).
- A regex in the education pattern captured the next line as part of the field (fixed).
- The first version of the ML Engineer and Data Engineer orders accepted only the literal word
  `SQL`, not any database (fixed after finding the assignment's own example).
- A textX object processor signature was wrong on the first try (fixed).
- The initial reference for textX cited the wrong venue (corrected after a web search).
- Some documentation described the sample résumés as matching two profiles before the data
  actually did (corrected).

The student should review each of these and confirm they understand the fix.
