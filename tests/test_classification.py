from pathlib import Path

import pytest
from pyformlang.finite_automaton import DeterministicFiniteAutomaton

from resumelens.classification.automata import PROFILE_AUTOMATA, _build_dfa, accepts, classify
from resumelens.extraction.extractor import extract_all
from resumelens.normalization.transducers import normalize

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_resumes"
QUALIFICATION_KEYS = ["languages", "frameworks", "databases", "cloud_tools", "data_tools", "tools"]


def normalized_from_sample(name: str) -> list[str]:
    extracted = extract_all((SAMPLES_DIR / name).read_text(encoding="utf-8"))
    raw = [term for key in QUALIFICATION_KEYS for term in extracted[key]]
    return normalize(raw)


def accepted_profiles(name: str) -> list[str]:
    result = classify(normalized_from_sample(name))
    return [profile for profile, verdict in result.items() if verdict == "ACCEPTED"]


# --- the automata themselves ---------------------------------------------------------


def test_every_profile_is_a_deterministic_finite_automaton():
    for dfa in PROFILE_AUTOMATA.values():
        assert isinstance(dfa, DeterministicFiniteAutomaton)


@pytest.mark.parametrize(
    "profile, expected_states",
    [
        ("FULL_STACK_DEVELOPER", 6),
        ("MACHINE_LEARNING_ENGINEER", 6),
        ("DEVOPS_ENGINEER", 7),
        ("DATA_ENGINEER", 5),
    ],
)
def test_state_counts_match_formalization_doc(profile, expected_states):
    assert len(PROFILE_AUTOMATA[profile].states) == expected_states


def test_build_dfa_rejects_a_spec_that_would_be_nondeterministic():
    with pytest.raises(ValueError, match="nondeterministic"):
        _build_dfa(
            start="q0",
            accepting="qf",
            transitions=[
                ("q0", {"PYTHON"}, "q1"),
                ("q0", {"PYTHON"}, "q2"),
            ],
        )


# --- assignment examples ----------------------------------------------------------------


def test_assignment_ml_engineer_sequence_is_accepted():
    sequence = ["PYTHON", "PANDAS", "TENSORFLOW", "POSTGRESQL", "GIT"]
    assert accepts("MACHINE_LEARNING_ENGINEER", sequence)


def test_wednesday_addams_is_accepted_for_full_stack():
    assert accepted_profiles("wednesday_addams.txt") == ["FULL_STACK_DEVELOPER"]


def test_mary_jane_watson_is_accepted_for_ml_engineer():
    assert accepted_profiles("mary_jane_watson.txt") == ["MACHINE_LEARNING_ENGINEER"]


# --- one case per sample resume, matching docs/formalization_automata.md -----------------


@pytest.mark.parametrize(
    "sample, expected",
    [
        ("peter_parker.txt", ["FULL_STACK_DEVELOPER"]),
        ("tony_stark.txt", ["DEVOPS_ENGINEER"]),
        ("michael_scott.txt", ["DEVOPS_ENGINEER"]),
        ("hermione_granger.txt", ["DATA_ENGINEER"]),
        ("walter_white.txt", ["DATA_ENGINEER"]),
        ("daenerys_targaryen.txt", ["FULL_STACK_DEVELOPER", "DEVOPS_ENGINEER"]),
        ("eleven.txt", ["MACHINE_LEARNING_ENGINEER", "DATA_ENGINEER"]),
        ("rick_sanchez.txt", []),
    ],
)
def test_sample_resume_classification(sample, expected):
    assert accepted_profiles(sample) == expected


# --- behaviours called out in docs/test_cases.md ------------------------------------------


def test_candidate_matching_nothing_is_rejected_on_every_profile():
    result = classify(["PYTHON", "BASH", "GIT"])
    assert set(result.values()) == {"REJECTED"}


def test_optional_qualification_missing_does_not_block_acceptance():
    sequence = ["PYTHON", "PANDAS", "TENSORFLOW", "SQL", "GIT"]
    assert accepts("MACHINE_LEARNING_ENGINEER", sequence)


def test_database_slot_accepts_any_recognized_database_term():
    for db in ["SQL", "POSTGRESQL", "MONGODB", "NOSQL"]:
        assert accepts("FULL_STACK_DEVELOPER", ["JAVASCRIPT", "REACT", "NODE_JS", db, "GIT"])


def test_extra_qualifications_after_the_pattern_do_not_reject_the_candidate():
    sequence = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT", "DOCKER", "AWS"]
    assert accepts("FULL_STACK_DEVELOPER", sequence)


def test_missing_required_slot_rejects_the_candidate():
    sequence = ["JAVASCRIPT", "REACT", "NODE_JS", "GIT"]
    assert not accepts("FULL_STACK_DEVELOPER", sequence)


def test_order_of_input_does_not_change_the_result():
    forward = ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    scrambled = ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT"]
    assert classify(forward) == classify(scrambled)


def test_empty_input_is_rejected_everywhere():
    assert set(classify([]).values()) == {"REJECTED"}
