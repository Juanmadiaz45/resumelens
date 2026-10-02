"""Run stage 2 normalization over the stage 1 output already sitting in
data/extracted/*.json, and write the result to data/normalized/<name>.json.

Qualifications aren't sorted by a profile's canonical order here, since picking a
profile is stage 3's job (classification) — this script only shows what comes out of
the transducers themselves: raw terms in, canonical terms out, unrecognized terms
dropped.

Usage: python scripts/normalize_samples.py (run scripts/extract_samples.py first)
"""

import json
from pathlib import Path

from resumelens.normalization.transducers import normalize

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = ROOT / "data" / "extracted"
OUTPUT_DIR = ROOT / "data" / "normalized"

# categories in extract_all()'s output that hold qualification strings as opposed to
# candidate data (name, contact, experience_years, education)
QUALIFICATION_KEYS = ["languages", "frameworks", "databases", "cloud_tools", "data_tools", "tools"]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for extracted_path in sorted(EXTRACTED_DIR.glob("*.json")):
        extracted = json.loads(extracted_path.read_text(encoding="utf-8"))
        raw_qualifications = [
            term for key in QUALIFICATION_KEYS for term in extracted[key]
        ]
        result = {
            "raw_qualifications": raw_qualifications,
            "normalized_qualifications": normalize(raw_qualifications),
        }
        output_path = OUTPUT_DIR / extracted_path.name
        output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"{extracted_path.name} -> {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
