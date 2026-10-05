"""Run the four ResumeLens stages in order on a single résumé.

Each stage's output is kept on the result object, so tests and the UI can look at any
intermediate value without running the pipeline again.
"""

from dataclasses import dataclass

from resumelens.classification.automata import classify
from resumelens.dsl.model import parse_candidate
from resumelens.dsl.render import render_html
from resumelens.dsl.serializer import serialize_candidate
from resumelens.extraction.extractor import extract_all
from resumelens.normalization.transducers import normalize

QUALIFICATION_KEYS = ["languages", "frameworks", "databases", "cloud_tools", "data_tools", "tools"]


@dataclass
class PipelineResult:
    extracted: dict
    normalized: list[str]
    classification: dict[str, str]
    candidate_text: str
    model: object
    html: str


def run(text: str) -> PipelineResult:
    extracted = extract_all(text)
    raw = [term for key in QUALIFICATION_KEYS for term in extracted[key]]
    normalized = normalize(raw)
    classification = classify(normalized)
    candidate_text = serialize_candidate(extracted, normalized, classification)
    model = parse_candidate(candidate_text)
    return PipelineResult(
        extracted=extracted,
        normalized=normalized,
        classification=classification,
        candidate_text=candidate_text,
        model=model,
        html=render_html(model),
    )
