"""Run the full pipeline over data/sample_resumes/*.txt and write each candidate's
profile to data/profiles/: the validated DSL text (.candidate), an HTML page (.html),
and a Markdown page (.md).

Usage: python scripts/build_profiles.py
"""

from pathlib import Path

from resumelens.dsl.render import render_markdown
from resumelens.pipeline.pipeline import run

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "data" / "sample_resumes"
OUTPUT_DIR = ROOT / "data" / "profiles"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for resume_path in sorted(SAMPLES_DIR.glob("*.txt")):
        result = run(resume_path.read_text(encoding="utf-8"))
        stem = resume_path.stem
        (OUTPUT_DIR / f"{stem}.candidate").write_text(result.candidate_text, encoding="utf-8")
        (OUTPUT_DIR / f"{stem}.html").write_text(result.html, encoding="utf-8")
        (OUTPUT_DIR / f"{stem}.md").write_text(render_markdown(result.model), encoding="utf-8")
        print(f"{resume_path.name} -> data/profiles/{stem}.{{candidate,html,md}}")


if __name__ == "__main__":
    main()
