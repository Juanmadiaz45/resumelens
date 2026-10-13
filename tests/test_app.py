from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
SAMPLES = sorted((ROOT / "data" / "sample_resumes").glob("*.txt"))


@pytest.fixture
def app():
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()


def test_app_opens_on_the_assignment_example(app):
    assert not app.exception
    assert app.subheader[0].value == "Wednesday Addams"


@pytest.mark.parametrize("sample", SAMPLES, ids=lambda p: p.stem)
def test_every_sample_renders_without_errors(app, sample):
    app.sidebar.selectbox[0].set_value(sample).run()
    assert not app.exception
    assert not app.error


def test_written_resume_without_a_name_shows_a_message_instead_of_failing(app):
    app.sidebar.radio[1].set_value("Write one").run()
    app.sidebar.text_area[0].set_value("Technical Skills: Python, Git").run()
    assert not app.exception
    assert any("No candidate name" in w.value for w in app.warning)


def test_written_resume_without_skills_is_rejected_by_the_grammar(app):
    app.sidebar.radio[1].set_value("Write one").run()
    app.sidebar.text_area[0].set_value("Jane Roe\nNothing technical here.").run()
    assert not app.exception
    assert any("at least one skill" in w.value for w in app.warning)


def test_sample_set_view_summarizes_the_ten_resumes(app):
    app.sidebar.radio[0].set_value("Sample set").run()
    assert not app.exception
    summary = " ".join(m.value for m in app.markdown)
    assert "7 résumés match one profile, 2 match two, and 1 matches none" in summary
