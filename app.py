"""ResumeLens web interface. Run with: streamlit run app.py"""

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import streamlit as st
from textx.exceptions import TextXSemanticError

from resumelens.classification.automata import classify, trace, transition_table
from resumelens.dsl.model import CandidateValidationError, parse_candidate
from resumelens.dsl.render import render_html, render_markdown
from resumelens.dsl.serializer import serialize_candidate
from resumelens.extraction.extractor import extract_all
from resumelens.normalization.transducers import (
    CANONICAL_TERMS,
    CLOUD_MAP,
    DATA_TOOL_MAP,
    DATABASE_MAP,
    DATABASE_TERMS,
    FRAMEWORK_MAP,
    LANGUAGE_MAP,
    PROFILE_ORDER,
    TOOLS_MAP,
    normalize,
    normalize_term,
)
from resumelens.pipeline.pipeline import QUALIFICATION_KEYS

SAMPLES_DIR = Path(__file__).parent / "data" / "sample_resumes"

PROFILE_NAMES = {
    "FULL_STACK_DEVELOPER": "Full Stack Developer",
    "MACHINE_LEARNING_ENGINEER": "Machine Learning Engineer",
    "DEVOPS_ENGINEER": "DevOps Engineer",
    "DATA_ENGINEER": "Data Engineer",
}

CATEGORY_NAMES = {
    "languages": "Programming languages",
    "frameworks": "Frameworks and libraries",
    "databases": "Databases",
    "cloud_tools": "Cloud and DevOps",
    "data_tools": "Data engineering",
    "tools": "Tools",
}

TRANSDUCERS = {
    "Language": LANGUAGE_MAP,
    "Framework and library": FRAMEWORK_MAP,
    "Database": DATABASE_MAP,
    "Cloud and DevOps": CLOUD_MAP,
    "Data engineering": DATA_TOOL_MAP,
    "Tools": TOOLS_MAP,
}

BLANK_RESUME = """Ada Lovelace
ada.lovelace@example.com
5 years of experience building data platforms.
B.Sc. in Computer Science
Technical Skills:
Python, PostgreSQL, Spark, Airflow, Kafka, Snowflake, Git.
"""

TEAL, NAVY, MUTED, LINE, RUST = "#2E6E68", "#173B5C", "#7B8794", "#C9C3B6", "#A4503A"


@dataclass
class Analysis:
    extracted: dict
    raw_terms: list[str]
    normalized: list[str]
    classification: dict[str, str]
    candidate_text: str | None
    error: str | None


def analyze(text: str) -> Analysis:
    extracted = extract_all(text)
    raw_terms = [term for key in QUALIFICATION_KEYS for term in extracted[key]]
    normalized = normalize(raw_terms)
    classification = classify(normalized)

    if extracted["name"] is None:
        return Analysis(extracted, raw_terms, normalized, classification, None,
                        "No candidate name was found. The first line of the résumé "
                        "should contain only the candidate's name.")

    candidate_text = serialize_candidate(extracted, normalized, classification)
    try:
        parse_candidate(candidate_text)
    except CandidateValidationError as error:
        message = str(error)
        if not normalized:
            message = ("No recognized qualifications were found. The grammar needs at least "
                       "one skill, so the candidate profile is rejected.")
        return Analysis(extracted, raw_terms, normalized, classification, candidate_text, message)
    return Analysis(extracted, raw_terms, normalized, classification, candidate_text, None)


def transducer_for(raw: str) -> str:
    key = raw.strip().casefold()
    for name, mapping in TRANSDUCERS.items():
        if key in {spelling.casefold() for spelling in mapping}:
            return name
    return "none"


def symbol_label(profile: str, symbols: set[str]) -> str:
    if symbols >= set(CANONICAL_TERMS):
        return "Σ"
    order = PROFILE_ORDER[profile]
    parts = []
    if DATABASE_TERMS <= symbols:
        symbols = symbols - DATABASE_TERMS
        parts.append("DB")
    parts += sorted(symbols, key=lambda s: order.index(s) if s in order else len(order))
    lines = [", ".join(parts[i:i + 2]) for i in range(0, len(parts), 2)]
    return "\\n".join(lines)


def automaton_dot(profile: str, path: list[str], accepted: bool) -> str:
    table = transition_table(profile)
    edges: dict[tuple[str, str], set[str]] = {}
    for source, moves in table.items():
        for symbol, target in moves.items():
            edges.setdefault((source, target), set()).add(symbol)

    states = {s for pair in edges for s in pair}
    walked = set(zip(path, path[1:]))
    visited = set(path)
    stuck = path[-1] if not accepted else None

    out = [
        "digraph {",
        'rankdir=LR; bgcolor="transparent"; pad=0.2; nodesep=0.35; ranksep=0.45;',
        f'node [shape=circle, fontname="IBM Plex Mono", fontsize=13, color="{LINE}", '
        f'fontcolor="{NAVY}", width=0.8, fixedsize=true, penwidth=1.2];',
        f'edge [fontname="IBM Plex Mono", fontsize=11, color="{LINE}", fontcolor="{MUTED}", '
        'arrowsize=0.7, penwidth=1.1];',
        '__start [shape=point, width=0.05, color="#52606D"];',
    ]
    for state in sorted(states):
        attrs = ['shape=doublecircle' if state == "qf" else ""]
        if state == stuck:
            attrs += [f'color="{RUST}"', f'fontcolor="{RUST}"', "penwidth=2"]
        elif state in visited:
            attrs += [f'color="{TEAL}"', 'style=filled', 'fillcolor="#E3EFEC"', "penwidth=1.8"]
        out.append(f'"{state}" [{", ".join(a for a in attrs if a)}];')

    start_color = TEAL if path else LINE
    out.append(f'__start -> "q0" [color="{start_color}"];')
    for (source, target), symbols in edges.items():
        attrs = [f'label="{symbol_label(profile, symbols)}"']
        if (source, target) in walked:
            attrs += [f'color="{TEAL}"', f'fontcolor="{TEAL}"', "penwidth=2"]
        out.append(f'"{source}" -> "{target}" [{", ".join(attrs)}];')
    out.append("}")
    return "\n".join(out)


def explain_run(sorted_terms: list[str], path: list[str], accepted: bool) -> str:
    if accepted:
        return (f"Read all {len(sorted_terms)} symbols and ended in **qf**, "
                "the accepting state.")
    if not sorted_terms:
        return "There are no qualifications to read, and **q0** is not an accepting state."
    read = len(path) - 1
    if read < len(sorted_terms):
        return (f"Stopped in **{path[-1]}**: δ({path[-1]}, {sorted_terms[read]}) is not "
                "defined, so the input is rejected.")
    return f"Read every symbol but ended in **{path[-1]}**, which is not an accepting state."


def readable_error(message: str) -> str:
    return re.sub(r"^None:(\d+):(\d+):\s*", r"Line \1, column \2: ", message)


def badge(verdict: str) -> str:
    return ":green-badge[Accepted]" if verdict == "ACCEPTED" else ":gray-badge[Rejected]"


def sample_label(path: Path) -> str:
    return path.stem.replace("_", " ").title()


def show_header() -> None:
    st.markdown(
        """
        <style>
        .block-container { padding-top: 2.4rem; max-width: 1180px; }
        h1 { letter-spacing: -0.02em; }
        .rl-sub { color: #52606D; font-size: 1.05rem; margin: -0.6rem 0 1.6rem 0; }
        .rl-label { color: #7B8794; font-size: 0.78rem; text-transform: uppercase;
                    letter-spacing: 0.06em; margin-bottom: 0.15rem; }
        .rl-path { font-family: "IBM Plex Mono", monospace; font-size: 0.8rem; color: #52606D; }
        .stTextArea textarea { font-family: "IBM Plex Mono", monospace; font-size: 0.85rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("ResumeLens")
    st.markdown(
        '<p class="rl-sub">Checks the qualifications written in a résumé against four '
        "profile patterns, using regular expressions, finite-state transducers, finite "
        "automata and a context-free grammar.</p>",
        unsafe_allow_html=True,
    )


def read_input() -> tuple[str | None, str]:
    st.sidebar.divider()
    source = st.sidebar.radio("Résumé", ["From the samples", "Upload a .txt file", "Write one"])
    if source == "From the samples":
        samples = sorted(SAMPLES_DIR.glob("*.txt"))
        default = next(i for i, p in enumerate(samples) if p.stem == "wednesday_addams")
        chosen = st.sidebar.selectbox("Sample", samples, index=default, format_func=sample_label)
        return chosen.read_text(encoding="utf-8"), chosen.stem
    if source == "Upload a .txt file":
        uploaded = st.sidebar.file_uploader("Plain-text résumé", type=["txt"])
        if uploaded is None:
            return None, "upload"
        return uploaded.getvalue().decode("utf-8", errors="replace"), Path(uploaded.name).stem
    text = st.sidebar.text_area("Résumé text", BLANK_RESUME, height=260)
    return text, "custom"


def show_profile_row(result: Analysis) -> None:
    columns = st.columns(4)
    for column, (profile, verdict) in zip(columns, result.classification.items()):
        sorted_terms, path = trace(profile, result.normalized)
        with column.container(border=True):
            st.markdown(f'<div class="rl-label">{PROFILE_NAMES[profile]}</div>', unsafe_allow_html=True)
            st.markdown(badge(verdict))
            if verdict == "ACCEPTED":
                note = " → ".join(s for i, s in enumerate(path) if i == 0 or s != path[i - 1])
            else:
                note = f"stopped in {path[-1]}"
            st.markdown(f'<div class="rl-path">{note}</div>', unsafe_allow_html=True)


def show_extraction(result: Analysis) -> None:
    left, right = st.columns([2, 3], gap="large")
    extracted = result.extracted
    with left:
        st.markdown("**Candidate data**")
        contact = extracted["contact"]
        rows = [
            ("Name", extracted["name"]),
            ("Email", contact["email"]),
            ("Phone", contact["phone"]),
            ("LinkedIn", contact["linkedin"]),
            ("GitHub", contact["github"]),
            ("Experience", f"{extracted['experience_years']} years"
             if extracted["experience_years"] is not None else None),
        ]
        rows += [("Education", f"{e['degree']} in {e['field']}") for e in extracted["education"]]
        st.dataframe(
            pd.DataFrame([(k, v if v else "not found") for k, v in rows], columns=["Field", "Value"]),
            hide_index=True, width="stretch",
        )
    with right:
        st.markdown("**Qualifications found**")
        table = pd.DataFrame(
            [(CATEGORY_NAMES[k], ", ".join(extracted[k]) or "none") for k in QUALIFICATION_KEYS],
            columns=["Category", "Strings matched"],
        )
        st.dataframe(table, hide_index=True, width="stretch")
    st.caption("Stage 1 only finds strings. Whether two of them mean the same thing is decided "
               "in stage 2.")


def show_normalization(result: Analysis) -> None:
    if not result.raw_terms:
        st.info("No qualifications were extracted, so there is nothing to normalize.")
        return
    rows = []
    for raw in result.raw_terms:
        canonical = normalize_term(raw)
        rows.append((raw, transducer_for(raw), canonical or "dropped (no transition)"))
    st.markdown("**Each string through its transducer**")
    st.dataframe(pd.DataFrame(rows, columns=["Raw string", "Transducer", "Output"]),
                 hide_index=True, width="stretch")

    st.markdown("**Sorted into each profile's order**")
    sorted_rows = [(PROFILE_NAMES[p], ", ".join(trace(p, result.normalized)[0]) or "empty")
                   for p in PROFILE_NAMES]
    st.dataframe(pd.DataFrame(sorted_rows, columns=["Profile", "Input to the automaton"]),
                 hide_index=True, width="stretch")
    st.caption("Sorting makes the result independent of the order the candidate wrote the "
               "skills in. Terms outside a profile go to the end.")


def show_classification(result: Analysis) -> None:
    profile = st.segmented_control(
        "Profile", list(PROFILE_NAMES), format_func=PROFILE_NAMES.get,
        default="FULL_STACK_DEVELOPER", label_visibility="collapsed",
    ) or "FULL_STACK_DEVELOPER"
    accepted = result.classification[profile] == "ACCEPTED"
    sorted_terms, path = trace(profile, result.normalized)

    with st.container(border=True):
        st.graphviz_chart(automaton_dot(profile, path, accepted), width="stretch")
    left, right = st.columns([2, 3], gap="large")
    with left:
        st.markdown(f"**{PROFILE_NAMES[profile]}** {badge(result.classification[profile])}")
        st.markdown(explain_run(sorted_terms, path, accepted))
    with right:
        steps = [("", path[0])] + list(zip(sorted_terms, path[1:]))
        st.dataframe(pd.DataFrame(steps, columns=["Symbol read", "State"]),
                     hide_index=True, width="stretch")
    st.caption("DB stands for any of the eight database terms. Σ is every canonical term: once "
               "the pattern is complete, extra qualifications don't change the verdict.")


def show_candidate_profile(result: Analysis, key: str, stem: str) -> None:
    if result.candidate_text is None:
        st.error(result.error)
        return

    left, right = st.columns([1, 1], gap="large")
    with left:
        st.markdown("**Candidate profile in the DSL**")
        edited = st.text_area("Candidate profile", result.candidate_text, height=230,
                              key=f"dsl-{key}", label_visibility="collapsed")
        try:
            model = parse_candidate(edited)
        except CandidateValidationError as error:
            model = None
            if isinstance(error.__cause__, TextXSemanticError):
                st.error("Rejected: a skill is not in the canonical vocabulary.")
            else:
                st.error("Rejected: the text does not follow the grammar.")
            st.code(readable_error(str(error)), language=None, wrap_lines=True)
        else:
            st.success("Valid candidate profile.")
        st.caption("You can edit the text to see how the grammar reacts, for example by "
                   "writing a skill in lowercase or adding COBOL.")

    with right:
        st.markdown("**Rendered page**")
        if model is None:
            st.info("The preview appears when the profile is valid.")
            return
        page = render_html(model)
        st.iframe(page, height=430)
        a, b, c = st.columns(3)
        a.download_button("HTML", page, f"{stem}.html", "text/html", width="stretch")
        b.download_button("Markdown", render_markdown(model), f"{stem}.md", "text/markdown",
                          width="stretch")
        c.download_button("DSL", edited, f"{stem}.candidate", "text/plain", width="stretch")


def show_single_resume() -> None:
    text, stem = read_input()
    if not text:
        st.info("Upload a plain-text résumé from the sidebar to start.")
        return

    result = analyze(text)
    name = result.extracted["name"] or "Unnamed candidate"
    st.subheader(name)
    show_profile_row(result)
    if result.error:
        st.warning(result.error)

    tabs = st.tabs(["Résumé", "1  Extraction", "2  Normalization", "3  Classification",
                    "4  Candidate profile"])
    with tabs[0]:
        st.code(text, language=None, wrap_lines=True)
    with tabs[1]:
        show_extraction(result)
    with tabs[2]:
        show_normalization(result)
    with tabs[3]:
        show_classification(result)
    with tabs[4]:
        show_candidate_profile(result, f"{stem}-{hash(text)}", stem)


def show_sample_set() -> None:
    st.subheader("The ten sample résumés")
    rows = []
    for path in sorted(SAMPLES_DIR.glob("*.txt")):
        result = analyze(path.read_text(encoding="utf-8"))
        rows.append({"Résumé": result.extracted["name"] or sample_label(path),
                     **{PROFILE_NAMES[p]: v.capitalize() for p, v in result.classification.items()}})
    table = pd.DataFrame(rows)
    matches = (table[list(PROFILE_NAMES.values())] == "Accepted").sum(axis=1)
    st.markdown(
        f"{(matches == 1).sum()} résumés match one profile, {(matches == 2).sum()} match two, "
        f"and {(matches == 0).sum()} matches none. Each profile is checked by its own automaton, "
        "so a candidate can fit more than one."
    )
    styled = table.style.map(
        lambda v: (f"background-color: #DCEBE8; color: {TEAL}; font-weight: 600"
                   if v == "Accepted" else "color: #A3ACB6"),
        subset=list(PROFILE_NAMES.values()),
    )
    st.dataframe(styled, hide_index=True, width="stretch", height=(len(table) + 1) * 35 + 3)
    st.caption("Wednesday Addams and Mary Jane Watson are the two examples from the assignment. "
               "The other eight were written to cover the four profiles and the mixed cases.")


st.set_page_config(page_title="ResumeLens", layout="wide")
show_header()

st.sidebar.markdown("### ResumeLens")
view = st.sidebar.radio("View", ["One résumé", "Sample set"], horizontal=True)

if view == "One résumé":
    show_single_resume()
else:
    show_sample_set()

st.sidebar.divider()
st.sidebar.caption("Team Flux · Computación y Estructuras Discretas III · 2026-2  \n"
                   "[Source code](https://github.com/Juanmadiaz45/resumelens)")
