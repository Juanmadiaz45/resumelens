from pathlib import Path

import pytest

from resumelens.dsl.model import CandidateValidationError
from resumelens.pipeline.pipeline import run
from resumelens.ui.cli import main

SAMPLES_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_resumes"


def accepted(result) -> list[str]:
    return [profile for profile, verdict in result.classification.items() if verdict == "ACCEPTED"]


def test_i1_wednesday_addams_end_to_end():
    result = run((SAMPLES_DIR / "wednesday_addams.txt").read_text(encoding="utf-8"))
    assert result.model.name == "Wednesday Addams"
    assert result.normalized == ["JAVASCRIPT", "REACT", "NODE_JS", "POSTGRESQL", "GIT"]
    assert accepted(result) == ["FULL_STACK_DEVELOPER"]
    assert "<html" in result.html and "Wednesday Addams" in result.html


def test_i2_mary_jane_watson_end_to_end():
    result = run((SAMPLES_DIR / "mary_jane_watson.txt").read_text(encoding="utf-8"))
    assert result.model.name == "Mary Jane Watson"
    assert accepted(result) == ["MACHINE_LEARNING_ENGINEER"]
    assert "<html" in result.html


def test_i3_rick_sanchez_is_rejected_everywhere_but_still_produces_a_page():
    result = run((SAMPLES_DIR / "rick_sanchez.txt").read_text(encoding="utf-8"))
    assert accepted(result) == []
    assert set(result.classification.values()) == {"REJECTED"}
    assert "<html" in result.html


def test_pipeline_rejects_a_resume_with_no_recognized_skills():
    with pytest.raises(CandidateValidationError):
        run("Nobody Known\n2 years of experience.\nTechnical Skills:\nCooking, Painting.\n")


# --- command-line interface -----------------------------------------------------------


def test_cli_writes_html_and_exits_zero(tmp_path, capsys):
    resume = SAMPLES_DIR / "wednesday_addams.txt"
    exit_code = main([str(resume), "--out-dir", str(tmp_path)])
    assert exit_code == 0
    assert (tmp_path / "wednesday_addams.html").read_text(encoding="utf-8").startswith("<!doctype html>")
    output = capsys.readouterr().out
    assert "FULL_STACK_DEVELOPER" in output and "ACCEPTED" in output


def test_cli_returns_2_for_a_missing_file(tmp_path, capsys):
    exit_code = main([str(tmp_path / "does_not_exist.txt")])
    assert exit_code == 2
    assert "no such file" in capsys.readouterr().err


def test_cli_returns_1_when_the_grammar_rejects_the_candidate(tmp_path, capsys):
    resume = tmp_path / "no_skills.txt"
    resume.write_text("Nobody Known\n2 years of experience.\nCooking, Painting.\n", encoding="utf-8")
    exit_code = main([str(resume)])
    assert exit_code == 1
    assert "rejected by the grammar" in capsys.readouterr().err
