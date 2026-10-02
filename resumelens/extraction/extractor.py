"""Stage 1 of the ResumeLens pipeline: pull raw qualification strings and candidate
data out of a plain-text resume using regular expressions.

Nothing in this module decides whether two terms are equivalent (e.g. "JS" vs
"Javascript") or whether a candidate fits a profile. That happens in later stages.
This module only answers: does this piece of text appear in the resume, and what
does it look like exactly as written.
"""

import re

_NAME_RE = re.compile(
    r"^\s*([A-Za-z][A-Za-z.'-]*(?:\s+[A-Za-z][A-Za-z.'-]*)*)\s*$",
    re.MULTILINE,
)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

_PHONE_RE = re.compile(r"\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}")

_LINKEDIN_RE = re.compile(
    r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+", re.IGNORECASE
)

_GITHUB_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[\w-]+", re.IGNORECASE)

_EXPERIENCE_RE = re.compile(r"(\d+)\+?\s*years?\s+of\s+experience", re.IGNORECASE)

_LANGUAGE_RE = re.compile(
    r"\b(?:JavaScript|Javascript|JS|TypeScript|TS|Python|Java|C\+\+|C#|Go|Ruby|PHP|Bash)\b"
)

_FRAMEWORK_RE = re.compile(
    r"\b(?:React(?:\.js)?|ReactJS|Angular|Vue(?:\.js)?|Node(?:\.js)?|NodeJS|Django|"
    r"Spring\s?Boot|Flask|Express(?:\.js)?|Pandas|NumPy|Scikit-learn|sklearn|"
    r"scikit\s?learn|Tensor\s?Flow|Py\s?Torch|Keras)\b",
    re.IGNORECASE,
)

_DATABASE_RE = re.compile(
    r"\b(?:Postgres|PostgreSQL|MySQL|MongoDB|SQLite|Redis|Cassandra|SQL|NoSQL)\b",
    re.IGNORECASE,
)

_CLOUD_RE = re.compile(
    r"\b(?:Docker|Kubernetes|K8s|Terraform|Ansible|Jenkins|GitHub\s?Actions|"
    r"GitLab\s?CI|AWS|Azure|GCP|Google\s?Cloud|Linux)\b",
    re.IGNORECASE,
)

_DATA_TOOL_RE = re.compile(
    r"\b(?:Apache\s?Spark|Spark|Airflow|Kafka|Snowflake|BigQuery|Redshift)\b",
    re.IGNORECASE,
)

# note: no trailing \b after the degree group. "B.Sc." ends in a period, and a
# period followed by whitespace is a non-word/non-word transition, so \b would
# never match there and the whole pattern would silently fail to match.
# the field capture uses horizontal whitespace only ([ \t]) instead of \s, so it
# doesn't run past the end of the line into whatever heading comes next.
_EDUCATION_RE = re.compile(
    r"\b(Bachelor|Master|PhD|B\.?Sc\.?|M\.?Sc\.?)(?:[ \t]+(?:of|in))?[ \t]+"
    r"([A-Z][A-Za-z]*(?:[ \t]+[A-Z][A-Za-z]*)*)"
)

_GIT_RE = re.compile(r"\bGit\b", re.IGNORECASE)
_REST_API_RE = re.compile(r"\bREST\s?API\b", re.IGNORECASE)


def _find_all_unique(pattern: re.Pattern, text: str) -> list[str]:
    seen: list[str] = []
    for match in pattern.finditer(text):
        value = match.group(0)
        if value not in seen:
            seen.append(value)
    return seen


def extract_candidate_name(text: str) -> str | None:
    match = _NAME_RE.search(text)
    return match.group(1).strip() if match else None


def extract_contact_info(text: str) -> dict:
    email = _EMAIL_RE.search(text)
    phone = _PHONE_RE.search(text)
    linkedin = _LINKEDIN_RE.search(text)
    github = _GITHUB_RE.search(text)
    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "github": github.group(0) if github else None,
    }


def extract_experience_years(text: str) -> int | None:
    match = _EXPERIENCE_RE.search(text)
    return int(match.group(1)) if match else None


def extract_languages(text: str) -> list[str]:
    return _find_all_unique(_LANGUAGE_RE, text)


def extract_frameworks(text: str) -> list[str]:
    return _find_all_unique(_FRAMEWORK_RE, text)


def extract_databases(text: str) -> list[str]:
    return _find_all_unique(_DATABASE_RE, text)


def extract_cloud_tools(text: str) -> list[str]:
    return _find_all_unique(_CLOUD_RE, text)


def extract_data_tools(text: str) -> list[str]:
    return _find_all_unique(_DATA_TOOL_RE, text)


def extract_education(text: str) -> list[dict]:
    return [
        {"degree": match.group(1), "field": match.group(2).strip()}
        for match in _EDUCATION_RE.finditer(text)
    ]


def extract_tools(text: str) -> list[str]:
    tools = []
    if _GIT_RE.search(text):
        tools.append("Git")
    if _REST_API_RE.search(text):
        tools.append("REST API")
    return tools


def extract_all(text: str) -> dict:
    return {
        "name": extract_candidate_name(text),
        "contact": extract_contact_info(text),
        "experience_years": extract_experience_years(text),
        "languages": extract_languages(text),
        "frameworks": extract_frameworks(text),
        "databases": extract_databases(text),
        "cloud_tools": extract_cloud_tools(text),
        "data_tools": extract_data_tools(text),
        "education": extract_education(text),
        "tools": extract_tools(text),
    }
