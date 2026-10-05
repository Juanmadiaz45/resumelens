# Test Cases

Every scenario below is covered by an automated test. The last column names the test file (and
the test function where it helps to find the case). Run the whole suite with `pytest` from the
project root; it currently passes 99 tests.

## Stage 1 — Extraction (`tests/test_extraction.py`)

| ID | Scenario | Input | Expected result | Covered by |
|---|---|---|---|---|
| E1 | Well-formed résumé, skills on one line | `data/sample_resumes/wednesday_addams.txt` | every listed skill extracted as a raw string | `test_wednesday_addams_matches_assignment_example` |
| E2 | Résumé with no skills section | "Hobbies: chess, cooking." | empty lists, no crash | `test_resume_without_a_skills_section_gives_empty_lists_not_an_error` |
| E3 | Mixed naming formats in the same list | `JS, React.js, NodeJS` | each detected as a separate raw string | `test_mixed_naming_formats_are_detected_as_separate_raw_strings` |
| E4 | Years of experience in different phrasings | "3 years", "4+ years", "1 year" of experience | value correctly captured | `test_experience_years_in_different_phrasings` |
| E5 | Education degree ending in a period, field followed by a newline | `B.Sc. in Computer Science` then a heading | degree `B.Sc.`, field `Computer Science` (no bleed into the next line) | `test_education_is_captured_without_bleeding_into_the_next_line` |

## Stage 2 — Normalization (`tests/test_normalization.py`)

| ID | Scenario | Input | Expected result | Covered by |
|---|---|---|---|---|
| N1 | Known variants of the same term | `JS`, `Javascript` | both map to `JAVASCRIPT` | `test_known_language_variants_map_to_the_same_canonical_term` |
| N2 | Term not recognized by any transducer | `COBOL` | dropped from the normalized list | `test_normalize_drops_unrecognized_terms_from_the_list` |
| N3 | Canonical ordering per profile | unordered list | reordered by the profile's canonical order | `test_full_stack_example_matches_the_assignment_statement` |
| N4 | Order of the input doesn't change the result | same terms, scrambled | identical sorted output | `test_sort_is_independent_of_input_order` |
| N5 | Terms outside the profile are kept, appended at the end | `REACT` in the data engineer order | kept, after the profile's own terms | `test_terms_outside_the_profile_are_kept_and_appended_at_the_end` |

## Stage 3 — Classification (`tests/test_classification.py`)

| ID | Scenario | Input | Expected result | Covered by |
|---|---|---|---|---|
| C1 | Candidate matches Full Stack Developer | `wednesday_addams.txt` | `ACCEPTED` for Full Stack only | `test_wednesday_addams_is_accepted_for_full_stack` |
| C2 | Candidate matches Machine Learning Engineer | `mary_jane_watson.txt`, and the assignment's own sequence | `ACCEPTED` for ML Engineer | `test_mary_jane_watson_is_accepted_for_ml_engineer`, `test_assignment_ml_engineer_sequence_is_accepted` |
| C3 | Candidate matches DevOps Engineer | `tony_stark.txt` | `ACCEPTED` for DevOps only | `test_sample_resume_classification[tony_stark.txt]` |
| C4 | Candidate matches Data Engineer | `hermione_granger.txt` | `ACCEPTED` for Data Engineer only | `test_sample_resume_classification[hermione_granger.txt]` |
| C5 | Candidate matches no profile | `rick_sanchez.txt` | `REJECTED` on all four | `test_candidate_matching_nothing_is_rejected_on_every_profile` |
| C6 | Candidate matches more than one profile | `daenerys_targaryen.txt` (Full Stack + DevOps), `eleven.txt` (ML + Data) | `ACCEPTED` on both | `test_sample_resume_classification[daenerys_targaryen.txt]`, `[eleven.txt]` |
| C7 | Optional qualification missing doesn't block acceptance | ML candidate without Scikit-learn; DevOps candidate without Linux | `ACCEPTED` anyway | `test_optional_qualification_missing_does_not_block_acceptance`, `test_sample_resume_classification[michael_scott.txt]` |
| C8 | Database slot accepts any recognized database term | `POSTGRESQL` in place of `SQL` | `ACCEPTED` for Full Stack | `test_database_slot_accepts_any_recognized_database_term` |
| C9 | Extra qualifications after the pattern don't reject | the required chain plus `DOCKER`, `AWS` | `ACCEPTED` | `test_extra_qualifications_after_the_pattern_do_not_reject_the_candidate` |
| C10 | A required slot is missing | Full Stack without a database | `REJECTED` | `test_missing_required_slot_rejects_the_candidate` |
| C11 | Empty input | `[]` | `REJECTED` everywhere | `test_empty_input_is_rejected_everywhere` |
| C12 | Automaton is deterministic by construction | conflicting spec rows | `ValueError` | `test_build_dfa_rejects_a_spec_that_would_be_nondeterministic` |

## Stage 4 — DSL (`tests/test_dsl.py`)

| ID | Scenario | Input | Expected result | Covered by |
|---|---|---|---|---|
| D1 | Valid, complete candidate | `VALID_CANDIDATE` in the test module | parses; HTML and Markdown render | `test_valid_candidate_parses_into_a_model`, `test_html_render_contains_name_skills_and_verdicts` |
| D2 | Model missing a required section | no `skills` line, no `classification` line | rejected | `test_candidate_without_skills_section_is_rejected`, `test_candidate_without_classification_section_is_rejected` |
| D3 | Repeated experiences and educations | two `experience`, two `education` lines | parsed as lists in order | `test_multiple_experiences_and_educations_are_parsed` |
| D4 | Lexical and syntactic violations | lowercase skill, malformed email, unknown keyword, unknown degree, unknown profile | rejected with a message | `test_lowercase_skill_is_a_lexical_error`, `test_malformed_email_is_rejected`, `test_unknown_keyword_is_a_syntax_error`, `test_unknown_degree_is_rejected`, `test_unknown_profile_name_is_rejected` |
| D5 | Skill outside the canonical vocabulary (semantic rule) | `COBOL` as a skill | rejected: "not a canonical qualification" | `test_skill_outside_the_canonical_vocabulary_is_rejected_semantically` |
| D6 | HTML escapes user text | a name containing `<script>` | markup shown as text | `test_html_render_escapes_user_supplied_text` |
| D7 | Every sample resume yields a valid profile | all 10 samples | valid model, four classification results, HTML page | `test_every_sample_resume_produces_a_valid_candidate_profile` |

## End-to-end and command line (`tests/test_integration.py`)

| ID | Scenario | Expected result | Covered by |
|---|---|---|---|
| I1 | `wednesday_addams.txt` through the full pipeline | normalized list matches the assignment; accepted for Full Stack; HTML produced | `test_i1_wednesday_addams_end_to_end` |
| I2 | `mary_jane_watson.txt` through the full pipeline | accepted for ML Engineer; HTML produced | `test_i2_mary_jane_watson_end_to_end` |
| I3 | `rick_sanchez.txt` through the full pipeline | rejected everywhere, page still produced | `test_i3_rick_sanchez_is_rejected_everywhere_but_still_produces_a_page` |
| I4 | Résumé with no recognized skills reaches the DSL | the DSL rejects it; the pipeline raises `CandidateValidationError` | `test_pipeline_rejects_a_resume_with_no_recognized_skills` |
| I5 | CLI on a valid résumé | exit 0, HTML written, summary printed | `test_cli_writes_html_and_exits_zero` |
| I6 | CLI on a missing file | exit 2 with a message | `test_cli_returns_2_for_a_missing_file` |
| I7 | CLI on a résumé the grammar rejects | exit 1 with the grammar error | `test_cli_returns_1_when_the_grammar_rejects_the_candidate` |
