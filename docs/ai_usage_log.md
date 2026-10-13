# AI Usage Log

The AI-use level for this task is "3. Colaboración con IAG": the AI may be used to complete tasks
and develop deliverables, as long as the student keeps a record of the interactions (the
student's own input and the prompts used) and can modify the generated results.

The tool was Claude Code, used from the terminal inside this repository. The prompts below are
copied as they were written, in Spanish, except for the last one, which is summarized because it
was a long list of changes. Times are local (UTC−5).

## Interactions

| # | Date | Prompt | What the AI did | Student's input and decisions |
|---|---|---|---|---|
| 1 | 2026-10-01 | "En esta carpeta se encuentra el documento de la tarea integradora, dame un resumen a detalle de que trata y de todo lo que se debe hacer y entregar de manera completa" | Summarized the assignment: the four stages and the list of deliverables. | Provided the assignment statement and used the summary as the checklist for the rest of the project. |
| 2 | 2026-10-01 | "Dame una planeacion completa, y tareas para realizar de manera completa el proyecto, estoy trabajando individual, yo solo" | Proposed a day-by-day plan with tasks. | Decided to work alone and to follow the plan one day at a time, asking for each day separately. |
| 3 | 2026-10-01 | "Empieza con el setup del repo y la estructura de carpetas, por cierto, le puse 'Flux' al nombre de mi equipo que soy yo solo" | Created the folder structure, `requirements.txt`, and the first README. | Chose the team name. |
| 4 | 2026-10-01 | "no veo que lo hayas subido a github. y otra cosa, siempre que hagas un commit no te pongas de co author, y siempre en standard, todo en minuscula" | Published the repository to GitHub. | Set the commit rules for the whole project: conventional commits, lowercase, no co-author line. |
| 5 | 2026-10-01 | "toda la documentacion, readme y demas en ingles, entonces actualizalo. y de paso, quiero que hagas y definas de manera correcta, en un lenguaje natural que no parezca ia, todo lo del dia 2 [...]" (followed by the day 2 tasks: module design, 8 to 10 sample résumés covering the four profiles and mixed cases, first draft of the regex categories) | Wrote the day 2 documents in English: module signatures, sample résumés, and the first regex draft. | Decided that all documentation would be in English and asked for plain, natural writing. Defined the scope of day 2, including mixed-profile résumés. |
| 6 | 2026-10-01 | "te pedi los commits en standard, es decir con la convencion doc, feat, fix, etc, actualiza los dos commits que hay a eso" | Rewrote the two existing commit messages. | Noticed that the first two commits didn't follow the convention and asked for them to be fixed. |
| 7 | 2026-10-02 | "Si, sigue con el dia 3. Pero otra cosa que olvide mencionar, la idea es que la implementacion y teoria de esta tarea integradora, este basada en lo explicado en clase, para esto, he puesto en la carpeta '~/Desktop/Universiad/CyDIII/' todas las diapositivas de la clase [...]" | Implemented stage 1 (regular expressions) with its tests. Read the slides and wrote `class_notation_reference.md`. | Required that the theory and the implementation follow the course, and provided the lecture slides. Because of this, the documents use the class notation: δ and Δ, λ instead of ε, and NFA-λ instead of ε-NFA. |
| 8 | 2026-10-02 | "si, sigue con el dia 4" | Wrote the formal definition of the six transducers. | Approved the day 3 results and asked to continue. |
| 9 | 2026-10-02 | "sigue con el dia 5" | Implemented stage 2 with pyformlang, the ordering by profile, and its tests. | Approved the transducer formalization and asked to continue. |
| 10 | 2026-10-02 | "si, sigue con el dia 6" and "continua donde quedaste" | Formalized the four automata and simulated them on the samples. The simulation showed that the ML Engineer and Data Engineer orders only accepted the literal `SQL`, while the assignment's own example uses `POSTGRESQL`, so the database category was widened. It also showed that two résumés meant to match two profiles matched only one, so those résumés were completed. | Accepted both corrections. |
| 11 | 2026-10-04 | "continua con el dia 7" | Implemented stage 3 with pyformlang, including a check that rejects any automaton that is not deterministic, and its tests. | Approved the automata formalization and asked to continue. |
| 12 | 2026-10-05 | "continua con el dia 8" | Implemented stage 4: the textX grammar, the serializer, the parser, and the HTML and Markdown output, with tests. | Approved stage 3 and asked to continue. |
| 13 | 2026-10-05 | "si, sigue con el dia 9" | Wrote the command-line interface, the integration tests, and the test case table. | Approved stage 4 and asked to continue. |
| 14 | 2026-10-05 | "Ya esta completo y comprobado? Haz un revision de todo comparado a la consigna", then "que es lo que falta", "no entiendo que es lo del poster, explicamelo", and "esta es la guia, revisala 'https://libguides.lib.cwu.edu/c.php?g=1014481&p=7347852' [...]" | Compared the project with the assignment and listed what was missing. Explained what the poster should contain, based on the guide. | Asked for an explicit check against the assignment instead of assuming the project was finished. Found and provided the poster guide. |
| 15 | 2026-10-05 | "haz los entregables que faltan y la documentacion por corregir" | Wrote the literature review, a first version of the poster, and the corrections to the regex and profile documents. | Decided which missing items to complete. |
| 16 | 2026-10-05 | "y por que no buscaste las referencias? si la idea era hacer el prompt pero con busquedas e informacion veridica siguiendo tal cual como dice la consigna" | Checked every reference with web searches. Corrected the year of Sipser's book (2012, not 2013) and the venue of the textX article (*Knowledge-Based Systems*). | Noticed that only three of the nine references had been checked and required all of them to be verified against real sources, as the assignment asks. |
| 17 | 2026-10-11 | "dame un estado completo de como esta el proyecto frente a lo que se debe entregar" | Gave a status report against the assignment, including the commit timing. | Used the report to decide the final changes. |
| 18 | 2026-10-12 | Summary: use fewer dashes in the documentation, revise this log, remove the presentation script, move the assignment PDF to `docs/`, resolve the missing page range of Karttunen et al. (1996), and record Visual Studio Code as the IDE. | Edited the documents, found the page range on the publisher's site, and updated this log and the README. | Decided the writing style of the final documents, decided that the presentation script should not be part of the repository, and confirmed the IDE. |

## How the AI output was checked

The pytest suite (99 tests) was run after every change, and the sample outputs in `data/` were
regenerated with the scripts. The two worked examples in the assignment statement (Wednesday
Addams and the ML Engineer sequence) were used as reference cases, and the pipeline reproduces
both.

All references in `literature_review.md` were checked against the publisher or an index. Mohri
(1997), *Computational Linguistics* 23(2), pp. 269–311; Dejanović et al. (2017),
*Knowledge-Based Systems* 115; Beesley and Karttunen (2003), CSLI Publications; Chomsky (1956),
*IRE Transactions on Information Theory* 2(3), pp. 113–124; Fowler (2010), Addison-Wesley;
Hopcroft, Motwani and Ullman (2006), 3rd edition, Addison-Wesley; Sipser (2012), 3rd edition,
Cengage; and Karttunen et al. (1996), *Natural Language Engineering* 2(4), pp. 305–328, confirmed
on Cambridge Core (DOI 10.1017/S1351324997001563). Some secondary sources give a wrong page range
for this last article, so the publisher's page was used.

The poster guide (CWU library) was read through a tool that summarizes web pages, so its layout
figures should be checked against the original page.

## Errors found during the work

Several errors in the AI's first versions were caught by the tests or by review, and each one is
worth understanding. The education pattern failed on `B.Sc.` because of a trailing `\b` after a
period, and it also captured the next line as part of the field because it used `\s`. The ML
Engineer and Data Engineer orders first accepted only the literal word `SQL` and not any
database, which contradicted the assignment's own example. The first textX object processor had
the wrong number of parameters. The first citation for textX named the wrong venue. Some
documents described two sample résumés as matching two profiles before the data actually did.
All of these were fixed, and the fixes are described in the corresponding documents.
