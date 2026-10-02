"""Run stage 1 extraction over every resume in data/sample_resumes/ and write the
result to data/extracted/<name>.json. Used to inspect and sanity-check the regex
patterns against the sample corpus, and to produce evidence that stage 1 runs
correctly end to end on all ten sample resumes.

Usage: python scripts/extract_samples.py
"""

import json
from pathlib import Path

from resumelens.extraction.extractor import extract_all

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "data" / "sample_resumes"
OUTPUT_DIR = ROOT / "data" / "extracted"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for resume_path in sorted(SAMPLES_DIR.glob("*.txt")):
        text = resume_path.read_text(encoding="utf-8")
        extracted = extract_all(text)
        output_path = OUTPUT_DIR / f"{resume_path.stem}.json"
        output_path.write_text(json.dumps(extracted, indent=2) + "\n", encoding="utf-8")
        print(f"{resume_path.name} -> {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
