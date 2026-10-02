from resumelens.normalization.transducers import (
    normalize,
    normalize_term,
    sort_by_profile_order,
)


# --- normalize_term: known variants ------------------------------------------------


def test_known_language_variants_map_to_the_same_canonical_term():
    assert normalize_term("JS") == "JAVASCRIPT"
    assert normalize_term("Javascript") == "JAVASCRIPT"
    assert normalize_term("JavaScript") == "JAVASCRIPT"


def test_known_framework_variants_map_to_the_same_canonical_term():
    assert normalize_term("React.js") == "REACT"
    assert normalize_term("ReactJS") == "REACT"
    assert normalize_term("sklearn") == "SCIKIT_LEARN"
    assert normalize_term("scikit learn") == "SCIKIT_LEARN"
    assert normalize_term("Scikit-learn") == "SCIKIT_LEARN"


def test_cloud_and_data_tool_abbreviations():
    assert normalize_term("K8s") == "KUBERNETES"
    assert normalize_term("Kubernetes") == "KUBERNETES"
    assert normalize_term("Apache Spark") == "SPARK"
    assert normalize_term("Spark") == "SPARK"


def test_normalize_term_is_case_insensitive():
    assert normalize_term("js") == "JAVASCRIPT"
    assert normalize_term("PYTHON") == "PYTHON"
    assert normalize_term("git") == "GIT"


def test_already_canonical_terms_still_pass_through_their_transducer():
    assert normalize_term("SQL") == "SQL"
    assert normalize_term("NoSQL") == "NOSQL"


# --- normalize_term: unknown terms --------------------------------------------------


def test_unrecognized_term_returns_none():
    assert normalize_term("COBOL") is None
    assert normalize_term("Microsoft Word") is None


def test_normalize_drops_unrecognized_terms_from_the_list():
    result = normalize(["Python", "COBOL", "Git"])
    assert result == ["PYTHON", "GIT"]


def test_normalize_on_empty_list_returns_empty_list():
    assert normalize([]) == []


# --- end-to-end against the assignment's own examples --------------------------------


def test_full_stack_example_matches_the_assignment_statement():
    raw = ["Git", "NodeJS", "JS", "Postgres", "React.js"]
    normalized = normalize(raw)
    sorted_terms = sort_by_profile_order(normalized, "FULL_STACK_DEVELOPER")
    assert sorted_terms == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]


def test_ml_engineer_example_matches_the_assignment_statement():
    raw = ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Git"]
    normalized = normalize(raw)
    sorted_terms = sort_by_profile_order(normalized, "MACHINE_LEARNING_ENGINEER")
    assert sorted_terms == [
        "PYTHON", "PANDAS", "NUMPY", "SCIKIT_LEARN", "TENSORFLOW", "SQL", "GIT",
    ]


# --- sort_by_profile_order -----------------------------------------------------------


def test_sort_is_independent_of_input_order():
    forward = sort_by_profile_order(
        ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"], "FULL_STACK_DEVELOPER"
    )
    backward = sort_by_profile_order(
        ["GIT", "POSTGRESQL", "NODE_JS", "REACT", "JAVASCRIPT"], "FULL_STACK_DEVELOPER"
    )
    assert forward == backward


def test_terms_outside_the_profile_are_kept_and_appended_at_the_end():
    result = sort_by_profile_order(["GIT", "KAFKA", "PYTHON"], "DATA_ENGINEER")
    assert result == ["PYTHON", "KAFKA", "GIT"]
    # a term from a different profile's vocabulary (REACT) isn't part of
    # DATA_ENGINEER's order, so it should still show up, just unsorted at the end
    result_with_outsider = sort_by_profile_order(["GIT", "REACT", "PYTHON"], "DATA_ENGINEER")
    assert result_with_outsider == ["PYTHON", "GIT", "REACT"]


def test_sort_with_unknown_profile_returns_terms_unchanged_in_relative_order():
    terms = ["GIT", "PYTHON", "REACT"]
    assert sort_by_profile_order(terms, "NOT_A_REAL_PROFILE") == terms
