from pathlib import Path

import pytest

from resumelens.extraction.extractor import (
    extract_all,
    extract_candidate_name,
    extract_cloud_tools,
    extract_contact_info,
    extract_data_tools,
    extract_databases,
    extract_education,
    extract_experience_years,
    extract_frameworks,
    extract_languages,
    extract_tools,
)

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_resumes"


def read_sample(name: str) -> str:
    return (SAMPLES_DIR / name).read_text(encoding="utf-8")


# --- assignment's own examples ---------------------------------------------


def test_wednesday_addams_matches_assignment_example():
    text = read_sample("wednesday_addams.txt")
    assert extract_candidate_name(text) == "Wednesday Addams"
    assert extract_experience_years(text) == 3
    assert extract_languages(text) == ["JS"]
    assert extract_frameworks(text) == ["React.js", "NodeJS"]
    assert extract_databases(text) == ["Postgres"]
    assert extract_tools(text) == ["Git"]


def test_mary_jane_watson_matches_assignment_example():
    text = read_sample("mary_jane_watson.txt")
    assert extract_candidate_name(text) == "Mary Jane Watson"
    assert extract_experience_years(text) == 2
    assert extract_languages(text) == ["Python"]
    assert extract_frameworks(text) == ["Pandas", "NumPy", "Scikit-learn", "TensorFlow"]
    assert extract_databases(text) == ["SQL"]


# --- contact information -----------------------------------------------------


def test_contact_info_picks_up_email_and_github():
    text = read_sample("peter_parker.txt")
    contact = extract_contact_info(text)
    assert contact["email"] == "peter.parker@example.com"
    assert contact["github"] == "github.com/peterparker"
    assert contact["phone"] is None
    assert contact["linkedin"] is None


def test_contact_info_picks_up_phone_and_linkedin():
    text = read_sample("tony_stark.txt")
    contact = extract_contact_info(text)
    assert contact["phone"] == "+1-555-010-2030"
    assert contact["linkedin"] == "linkedin.com/in/tonystark"


def test_contact_info_is_all_none_when_resume_has_no_contact_section():
    text = read_sample("wednesday_addams.txt")
    contact = extract_contact_info(text)
    assert contact == {"email": None, "phone": None, "linkedin": None, "github": None}


# --- education ----------------------------------------------------------------


def test_education_is_captured_without_bleeding_into_the_next_line():
    text = read_sample("peter_parker.txt")
    education = extract_education(text)
    assert education == [{"degree": "B.Sc.", "field": "Computer Science"}]


def test_education_handles_master_without_a_period():
    text = read_sample("hermione_granger.txt")
    education = extract_education(text)
    assert education == [{"degree": "Master", "field": "Data Science"}]


def test_education_is_empty_when_resume_has_no_education_section():
    text = read_sample("wednesday_addams.txt")
    assert extract_education(text) == []


# --- cloud / devops and data engineering categories ---------------------------


def test_cloud_tools_for_devops_resume():
    text = read_sample("tony_stark.txt")
    assert extract_cloud_tools(text) == [
        "Linux",
        "Docker",
        "Kubernetes",
        "Terraform",
        "Jenkins",
        "AWS",
    ]


def test_data_tools_for_data_engineer_resume():
    text = read_sample("hermione_granger.txt")
    assert extract_data_tools(text) == ["Apache Spark", "Airflow", "Snowflake"]


def test_apache_spark_is_matched_as_one_term_not_two():
    text = read_sample("hermione_granger.txt")
    data_tools = extract_data_tools(text)
    assert "Apache Spark" in data_tools
    assert "Spark" not in data_tools


# --- mixed / ambiguous candidates ----------------------------------------------


def test_mixed_resume_contains_qualifications_from_two_profiles():
    text = read_sample("daenerys_targaryen.txt")
    assert extract_languages(text) == ["JavaScript"]
    assert extract_frameworks(text) == ["React", "Node.js"]
    assert extract_cloud_tools(text) == ["Docker", "Kubernetes", "Terraform", "Jenkins", "AWS"]


# --- candidate with too few qualifications for any profile ---------------------


def test_insufficient_profile_resume_extracts_very_little():
    text = read_sample("rick_sanchez.txt")
    assert extract_languages(text) == ["Python", "Bash"]
    assert extract_frameworks(text) == []
    assert extract_cloud_tools(text) == []
    assert extract_data_tools(text) == []


# --- extract_all consolidation --------------------------------------------------


def test_extract_all_returns_every_category_as_a_key():
    text = read_sample("wednesday_addams.txt")
    result = extract_all(text)
    assert set(result.keys()) == {
        "name",
        "contact",
        "experience_years",
        "languages",
        "frameworks",
        "databases",
        "cloud_tools",
        "data_tools",
        "education",
        "tools",
    }


@pytest.mark.parametrize("filename", [p.name for p in SAMPLES_DIR.glob("*.txt")])
def test_extract_all_does_not_crash_on_any_sample_resume(filename):
    text = read_sample(filename)
    result = extract_all(text)
    assert result["name"] is not None


# --- edge cases from docs/test_cases.md --------------------------------------------


def test_resume_without_a_skills_section_gives_empty_lists_not_an_error():
    text = "Nobody Known\n2 years of experience.\nHobbies: chess, cooking.\n"
    assert extract_languages(text) == []
    assert extract_frameworks(text) == []
    assert extract_tools(text) == []
    assert extract_experience_years(text) == 2


def test_mixed_naming_formats_are_detected_as_separate_raw_strings():
    text = "Technical Skills:\nJS, React.js, NodeJS\n"
    assert extract_languages(text) == ["JS"]
    assert extract_frameworks(text) == ["React.js", "NodeJS"]


@pytest.mark.parametrize(
    "phrase, expected",
    [("3 years of experience", 3), ("4+ years of experience", 4), ("1 year of experience", 1)],
)
def test_experience_years_in_different_phrasings(phrase, expected):
    assert extract_experience_years(f"Summary: {phrase} building apps.") == expected
