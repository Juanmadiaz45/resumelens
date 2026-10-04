"""Stage 2 of the ResumeLens pipeline: pass each raw qualification string produced by
stage 1 through a finite-state transducer that maps it to its canonical form, then
reorder the normalized terms according to the profile's canonical category order.

See docs/formalization_fst.md for the formal 7-tuple definition of each transducer
below and the reasoning behind the canonical orders.
"""

from pyformlang.fst import FST

LANGUAGE_MAP = {
    "JS": "JAVASCRIPT",
    "Javascript": "JAVASCRIPT",
    "JavaScript": "JAVASCRIPT",
    "TypeScript": "TYPESCRIPT",
    "TS": "TYPESCRIPT",
    "Python": "PYTHON",
    "Java": "JAVA",
    "C++": "CPP",
    "C#": "CSHARP",
    "Go": "GO",
    "Ruby": "RUBY",
    "PHP": "PHP",
    "Bash": "BASH",
}

FRAMEWORK_MAP = {
    "React": "REACT",
    "React.js": "REACT",
    "ReactJS": "REACT",
    "Angular": "ANGULAR",
    "Vue": "VUE",
    "Vue.js": "VUE",
    "Node": "NODE_JS",
    "Node.js": "NODE_JS",
    "NodeJS": "NODE_JS",
    "Django": "DJANGO",
    "Spring Boot": "SPRING_BOOT",
    "SpringBoot": "SPRING_BOOT",
    "Flask": "FLASK",
    "Express": "EXPRESS",
    "Express.js": "EXPRESS",
    "Pandas": "PANDAS",
    "NumPy": "NUMPY",
    "Scikit-learn": "SCIKIT_LEARN",
    "sklearn": "SCIKIT_LEARN",
    "scikit learn": "SCIKIT_LEARN",
    "Tensor Flow": "TENSORFLOW",
    "TensorFlow": "TENSORFLOW",
    "Py Torch": "PYTORCH",
    "PyTorch": "PYTORCH",
    "Keras": "KERAS",
}

DATABASE_MAP = {
    "Postgres": "POSTGRESQL",
    "PostgreSQL": "POSTGRESQL",
    "MySQL": "MYSQL",
    "MongoDB": "MONGODB",
    "SQLite": "SQLITE",
    "Redis": "REDIS",
    "Cassandra": "CASSANDRA",
    "SQL": "SQL",
    "NoSQL": "NOSQL",
}

CLOUD_MAP = {
    "Docker": "DOCKER",
    "Kubernetes": "KUBERNETES",
    "K8s": "KUBERNETES",
    "Terraform": "TERRAFORM",
    "Ansible": "ANSIBLE",
    "Jenkins": "JENKINS",
    "GitHub Actions": "GITHUB_ACTIONS",
    "GitLab CI": "GITLAB_CI",
    "AWS": "AWS",
    "Azure": "AZURE",
    "GCP": "GCP",
    "Google Cloud": "GCP",
    "Linux": "LINUX",
}

DATA_TOOL_MAP = {
    "Spark": "SPARK",
    "Apache Spark": "SPARK",
    "Airflow": "AIRFLOW",
    "Kafka": "KAFKA",
    "Snowflake": "SNOWFLAKE",
    "BigQuery": "BIGQUERY",
    "Redshift": "REDSHIFT",
}

TOOLS_MAP = {
    "Git": "GIT",
    "REST API": "REST_API",
}

_ALL_MAPS = [
    LANGUAGE_MAP,
    FRAMEWORK_MAP,
    DATABASE_MAP,
    CLOUD_MAP,
    DATA_TOOL_MAP,
    TOOLS_MAP,
]

CANONICAL_TERMS = frozenset(term for mapping in _ALL_MAPS for term in mapping.values())
DATABASE_TERMS = frozenset(DATABASE_MAP.values())


def _build_fst(mapping: dict) -> FST:
    """Build a 2-state FST (q0 -> qf) with one transition per entry in `mapping`.

    Transition symbols are case-folded here, even though the formal alphabet in
    formalization_fst.md lists the canonical-cased spelling of each synonym — stage 1's
    regexes are case-insensitive, so the raw token handed to this transducer could show
    up in any casing. Case-folding both the transducer's symbols and the query term
    keeps that variation from needing a separate transition per casing.
    """
    transducer = FST()
    transducer.add_transitions(
        [("q0", raw.casefold(), "qf", [canonical]) for raw, canonical in mapping.items()]
    )
    transducer.add_start_state("q0")
    transducer.add_final_state("qf")
    return transducer


_TRANSDUCERS = [_build_fst(mapping) for mapping in _ALL_MAPS]


def normalize_term(raw_term: str) -> str | None:
    """Run a single raw qualification string through the six transducers and return
    its canonical form. Returns None if no transducer has a transition for it — the
    term stays in q0, which is not an accepting state, so it's rejected rather than
    silently passed through unchanged.
    """
    term = raw_term.strip().casefold()
    for transducer in _TRANSDUCERS:
        outputs = list(transducer.translate([term]))
        if outputs:
            return outputs[0][0]
    return None


def normalize(raw_terms: list[str]) -> list[str]:
    """Normalize a list of raw qualification strings, dropping any term that none of
    the transducers recognize. Dropping (rather than keeping an "UNKNOWN" placeholder)
    was the simplest option that didn't change stage 3's job: an unrecognized term
    can't be part of any profile pattern anyway, since every automaton's alphabet is
    built from canonical terms only.
    """
    normalized = []
    for raw_term in raw_terms:
        canonical = normalize_term(raw_term)
        if canonical is not None:
            normalized.append(canonical)
    return normalized


PROFILE_ORDER = {
    "FULL_STACK_DEVELOPER": [
        "JAVASCRIPT", "TYPESCRIPT",
        "REACT", "ANGULAR", "VUE",
        "NODE_JS", "DJANGO", "SPRING_BOOT",
        "SQL", "NOSQL", "POSTGRESQL", "MYSQL", "MONGODB", "SQLITE", "REDIS", "CASSANDRA",
        "REST_API",
        "GIT",
    ],
    "MACHINE_LEARNING_ENGINEER": [
        "PYTHON",
        "PANDAS", "NUMPY",
        "SCIKIT_LEARN",
        "TENSORFLOW", "PYTORCH",
        "SQL", "NOSQL", "POSTGRESQL", "MYSQL", "MONGODB", "SQLITE", "REDIS", "CASSANDRA",
        "GIT",
    ],
    "DEVOPS_ENGINEER": [
        "LINUX",
        "DOCKER",
        "KUBERNETES",
        "TERRAFORM", "ANSIBLE",
        "JENKINS", "GITHUB_ACTIONS", "GITLAB_CI",
        "AWS", "AZURE", "GCP",
        "GIT",
    ],
    "DATA_ENGINEER": [
        "PYTHON",
        "SQL", "NOSQL", "POSTGRESQL", "MYSQL", "MONGODB", "SQLITE", "REDIS", "CASSANDRA",
        "SPARK", "AIRFLOW", "KAFKA",
        "SNOWFLAKE", "BIGQUERY", "REDSHIFT",
        "GIT",
    ],
}


def sort_by_profile_order(terms: list[str], profile: str) -> list[str]:
    """Reorder normalized terms according to the profile's canonical category order
    (see docs/formalization_fst.md), so the result doesn't depend on the order the
    candidate happened to list their skills in. Terms that aren't part of the given
    profile's qualification list are kept, appended at the end in their original
    relative order, since they might still matter for a different profile's automaton.
    """
    order = PROFILE_ORDER.get(profile, [])
    order_index = {term: i for i, term in enumerate(order)}
    return sorted(terms, key=lambda term: order_index.get(term, len(order)))
