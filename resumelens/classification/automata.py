"""Stage 3 of the ResumeLens pipeline: decide, for each supported profile, whether the
sorted canonical qualification sequence satisfies that profile's pattern.

Each profile is a deterministic finite automaton built with pyformlang. The formal
definitions, state names, and diagrams are in docs/formalization_automata.md.
"""

from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State

from resumelens.normalization.transducers import (
    CANONICAL_TERMS,
    DATABASE_TERMS as DB,
    sort_by_profile_order,
)

FRONTEND_LANGUAGES = {"JAVASCRIPT", "TYPESCRIPT"}
FRONTEND_FRAMEWORKS = {"REACT", "ANGULAR", "VUE"}
BACKEND_FRAMEWORKS = {"NODE_JS", "DJANGO", "SPRING_BOOT"}
ML_DATA_LIBRARIES = {"PANDAS", "NUMPY"}
ML_MODEL_LIBRARIES = {"TENSORFLOW", "PYTORCH"}
IAC_TOOLS = {"TERRAFORM", "ANSIBLE"}
CI_CD_TOOLS = {"JENKINS", "GITHUB_ACTIONS", "GITLAB_CI"}
CLOUD_PROVIDERS = {"AWS", "AZURE", "GCP"}
PIPELINE_TOOLS = {"SPARK", "AIRFLOW", "KAFKA"}
WAREHOUSES = {"SNOWFLAKE", "BIGQUERY", "REDSHIFT"}


def _build_dfa(start: str, accepting: str, transitions: list[tuple]) -> DeterministicFiniteAutomaton:
    """Build a DFA from (source, symbols, target) rows.

    Raises if two rows give the same (state, symbol) pair different targets, so a
    typo in the spec can't silently turn the DFA into something nondeterministic.
    The accepting state gets a self-loop on every canonical term, which is what lets
    extra qualifications after the required pattern leave a candidate accepted.
    """
    table: dict[tuple[str, str], str] = {}
    for source, symbols, target in transitions:
        for symbol in symbols:
            key = (source, symbol)
            if key in table and table[key] != target:
                raise ValueError(f"nondeterministic spec: {key} -> {table[key]} and {target}")
            table[key] = target
    for symbol in CANONICAL_TERMS:
        table.setdefault((accepting, symbol), accepting)

    states = {State(name) for name in {s for s, _ in table} | set(table.values())}
    dfa = DeterministicFiniteAutomaton(
        states=states,
        input_symbols=set(CANONICAL_TERMS),
        start_state=State(start),
        final_states={State(accepting)},
    )
    dfa.add_transitions(
        [(State(s), sym, State(t)) for (s, sym), t in table.items()]
    )
    return dfa


def _full_stack_developer() -> DeterministicFiniteAutomaton:
    return _build_dfa(
        start="q0",
        accepting="qf",
        transitions=[
            ("q0", FRONTEND_LANGUAGES, "q_lang"),
            ("q_lang", FRONTEND_LANGUAGES, "q_lang"),
            ("q_lang", FRONTEND_FRAMEWORKS, "q_front"),
            ("q_front", FRONTEND_FRAMEWORKS, "q_front"),
            ("q_front", BACKEND_FRAMEWORKS, "q_back"),
            ("q_back", BACKEND_FRAMEWORKS, "q_back"),
            ("q_back", DB, "q_db"),
            ("q_db", DB | {"REST_API"}, "q_db"),
            ("q_db", {"GIT"}, "qf"),
        ],
    )


def _machine_learning_engineer() -> DeterministicFiniteAutomaton:
    return _build_dfa(
        start="q0",
        accepting="qf",
        transitions=[
            ("q0", {"PYTHON"}, "q_py"),
            ("q_py", {"PYTHON"}, "q_py"),
            ("q_py", ML_DATA_LIBRARIES, "q_arr"),
            ("q_arr", ML_DATA_LIBRARIES | {"SCIKIT_LEARN"}, "q_arr"),
            ("q_arr", ML_MODEL_LIBRARIES, "q_ml"),
            ("q_ml", ML_MODEL_LIBRARIES, "q_ml"),
            ("q_ml", DB, "q_db"),
            ("q_db", DB, "q_db"),
            ("q_db", {"GIT"}, "qf"),
        ],
    )


def _devops_engineer() -> DeterministicFiniteAutomaton:
    return _build_dfa(
        start="q0",
        accepting="qf",
        transitions=[
            ("q0", {"LINUX"}, "q0"),
            ("q0", {"DOCKER"}, "q_docker"),
            ("q_docker", {"DOCKER"}, "q_docker"),
            ("q_docker", {"KUBERNETES"}, "q_k8s"),
            ("q_k8s", {"KUBERNETES"}, "q_k8s"),
            ("q_k8s", IAC_TOOLS, "q_iac"),
            ("q_iac", IAC_TOOLS, "q_iac"),
            ("q_iac", CI_CD_TOOLS, "q_ci"),
            ("q_ci", CI_CD_TOOLS, "q_ci"),
            ("q_ci", CLOUD_PROVIDERS, "q_cloud"),
            ("q_cloud", CLOUD_PROVIDERS, "q_cloud"),
            ("q_cloud", {"GIT"}, "qf"),
        ],
    )


def _data_engineer() -> DeterministicFiniteAutomaton:
    return _build_dfa(
        start="q0",
        accepting="qf",
        transitions=[
            ("q0", {"PYTHON"}, "q_py"),
            ("q_py", {"PYTHON"}, "q_py"),
            ("q_py", DB, "q_db"),
            ("q_db", DB, "q_db"),
            ("q_db", PIPELINE_TOOLS, "q_pipe"),
            ("q_pipe", PIPELINE_TOOLS | WAREHOUSES, "q_pipe"),
            ("q_pipe", {"GIT"}, "qf"),
        ],
    )


PROFILE_AUTOMATA = {
    "FULL_STACK_DEVELOPER": _full_stack_developer(),
    "MACHINE_LEARNING_ENGINEER": _machine_learning_engineer(),
    "DEVOPS_ENGINEER": _devops_engineer(),
    "DATA_ENGINEER": _data_engineer(),
}


def accepts(profile: str, normalized_terms: list[str]) -> bool:
    """Return True if the normalized terms, sorted for `profile`, are accepted by that
    profile's automaton."""
    sorted_terms = sort_by_profile_order(normalized_terms, profile)
    return PROFILE_AUTOMATA[profile].accepts(sorted_terms)


def classify(normalized_terms: list[str]) -> dict[str, str]:
    """Run the four profile automata over a candidate's normalized qualifications.
    Each automaton gets its own canonical ordering, so the result doesn't depend on
    the order the candidate wrote their skills in.
    """
    return {
        profile: "ACCEPTED" if accepts(profile, normalized_terms) else "REJECTED"
        for profile in PROFILE_AUTOMATA
    }
