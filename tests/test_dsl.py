from pathlib import Path

import pytest

from resumelens.dsl.model import CandidateValidationError, parse_candidate, validate
from resumelens.dsl.render import render_html, render_markdown
from resumelens.dsl.serializer import serialize_candidate
from resumelens.pipeline.pipeline import run

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_resumes"

VALID_CANDIDATE = """\
candidate "Peter Parker"
contact email peter.parker@example.com github github.com/peterparker
experience 4 years
education B.Sc. "Computer Science"
skills TYPESCRIPT ANGULAR SPRING_BOOT MONGODB GIT REST_API
classification FULL_STACK_DEVELOPER ACCEPTED MACHINE_LEARNING_ENGINEER REJECTED DEVOPS_ENGINEER REJECTED DATA_ENGINEER REJECTED
"""


# --- D1: valid, complete candidate -------------------------------------------------


def test_valid_candidate_parses_into_a_model():
    model = parse_candidate(VALID_CANDIDATE)
    assert model.name == "Peter Parker"
    assert [s.name for s in model.skills] == [
        "TYPESCRIPT", "ANGULAR", "SPRING_BOOT", "MONGODB", "GIT", "REST_API",
    ]
    assert [(r.profile, r.verdict) for r in model.results][0] == (
        "FULL_STACK_DEVELOPER", "ACCEPTED",
    )


def test_validate_reports_success_for_a_valid_candidate():
    assert validate(VALID_CANDIDATE) == (True, [])


def test_html_render_contains_name_skills_and_verdicts():
    html_page = render_html(parse_candidate(VALID_CANDIDATE))
    assert "Peter Parker" in html_page
    assert 'class="skill">GIT<' in html_page
    assert '<li class="accepted">FULL_STACK_DEVELOPER: ACCEPTED</li>' in html_page
    assert '<li class="rejected">DATA_ENGINEER: REJECTED</li>' in html_page


def test_markdown_render_contains_name_and_skills():
    markdown = render_markdown(parse_candidate(VALID_CANDIDATE))
    assert markdown.startswith("# Peter Parker")
    assert "`GIT`" in markdown


def test_html_render_escapes_user_supplied_text():
    text = VALID_CANDIDATE.replace('"Peter Parker"', '"<script>alert(1)</script>"')
    html_page = render_html(parse_candidate(text))
    assert "<script>alert(1)</script>" not in html_page
    assert "&lt;script&gt;" in html_page


# --- D2: missing required section -------------------------------------------------


def test_candidate_without_skills_section_is_rejected():
    text = VALID_CANDIDATE.replace("skills TYPESCRIPT ANGULAR SPRING_BOOT MONGODB GIT REST_API\n", "")
    valid, errors = validate(text)
    assert not valid
    assert errors


def test_candidate_without_classification_section_is_rejected():
    text = VALID_CANDIDATE.rsplit("classification", 1)[0]
    assert not validate(text)[0]


# --- D3: repeated elements ---------------------------------------------------------


def test_multiple_experiences_and_educations_are_parsed():
    text = """\
candidate "Walter White"
contact
experience 6 years
experience 2 years
education Master "Data Science"
education B.Sc. "Chemistry"
skills PYTHON SQL GIT
classification DATA_ENGINEER ACCEPTED
"""
    model = parse_candidate(text)
    assert [e.years for e in model.experiences] == [6, 2]
    assert [(e.degree, e.field) for e in model.educations] == [
        ("Master", "Data Science"),
        ("B.Sc.", "Chemistry"),
    ]


# --- D4: lexical and syntactic violations -------------------------------------------


def test_lowercase_skill_is_a_lexical_error():
    text = VALID_CANDIDATE.replace("GIT", "git")
    valid, errors = validate(text)
    assert not valid
    assert "git" in errors[0] or "Expected" in errors[0]


def test_unknown_keyword_is_a_syntax_error():
    text = VALID_CANDIDATE.replace("experience 4 years", "seniority 4 years")
    assert not validate(text)[0]


def test_malformed_email_is_rejected():
    text = VALID_CANDIDATE.replace("peter.parker@example.com", "peter.parker@")
    assert not validate(text)[0]


def test_unknown_degree_is_rejected():
    text = VALID_CANDIDATE.replace("B.Sc.", "Diploma")
    assert not validate(text)[0]


def test_unknown_profile_name_is_rejected():
    text = VALID_CANDIDATE.replace("DATA_ENGINEER", "ASTRONAUT")
    assert not validate(text)[0]


# --- semantic rule: skills must be canonical terms ----------------------------------


def test_skill_outside_the_canonical_vocabulary_is_rejected_semantically():
    text = VALID_CANDIDATE.replace("GIT", "COBOL")
    valid, errors = validate(text)
    assert not valid
    assert "not a canonical qualification" in errors[0]


def test_parse_candidate_raises_a_domain_error_not_a_textx_error():
    with pytest.raises(CandidateValidationError):
        parse_candidate("candidate \"X\" skills COBOL classification DATA_ENGINEER ACCEPTED")


# --- serializer and end-to-end --------------------------------------------------------


@pytest.mark.parametrize("sample", sorted(p.name for p in SAMPLES_DIR.glob("*.txt")))
def test_every_sample_resume_produces_a_valid_candidate_profile(sample):
    result = run((SAMPLES_DIR / sample).read_text(encoding="utf-8"))
    assert result.model.name
    assert len(result.model.results) == 4
    assert "<html" in result.html


def test_serializer_maps_degree_abbreviations_to_the_grammar_spelling():
    extracted = {
        "name": "Ann",
        "contact": {"email": None, "phone": None, "linkedin": None, "github": None},
        "experience_years": None,
        "education": [{"degree": "bsc", "field": "Math"}],
    }
    text = serialize_candidate(extracted, ["GIT"], {"DATA_ENGINEER": "REJECTED"})
    assert "education B.Sc. \"Math\"" in text
    assert validate(text)[0]
