"""Load the candidate profile grammar and turn candidate DSL text into validated models.

Syntax and lexical rules come from candidate.tx. The vocabulary check (a skill has to be
one of the canonical terms stage 2 can produce) is a textX object processor, so a skill
the grammar can't place in the vocabulary is rejected the same way a syntax error is.
"""

from pathlib import Path

from textx import metamodel_from_file
from textx.exceptions import TextXError, TextXSemanticError

from resumelens.normalization.transducers import CANONICAL_TERMS

GRAMMAR_PATH = Path(__file__).with_name("candidate.tx")


class CandidateValidationError(Exception):
    pass


def _check_canonical_term(value: str) -> str:
    if value not in CANONICAL_TERMS:
        raise TextXSemanticError(f"'{value}' is not a canonical qualification")
    return value


def _build_metamodel():
    metamodel = metamodel_from_file(str(GRAMMAR_PATH))
    metamodel.register_obj_processors({"CanonicalTerm": _check_canonical_term})
    return metamodel


_METAMODEL = _build_metamodel()


def parse_candidate(text: str):
    try:
        return _METAMODEL.model_from_str(text)
    except TextXError as error:
        raise CandidateValidationError(str(error)) from error


def validate(text: str) -> tuple[bool, list[str]]:
    try:
        parse_candidate(text)
    except CandidateValidationError as error:
        return False, [str(error)]
    return True, []
