"""Run stage 3 classification over the stage 2 output in data/normalized/*.json and
write the per-profile verdicts to data/classified/<name>.json.

Usage: python scripts/classify_samples.py (run scripts/normalize_samples.py first)
"""

import json
from pathlib import Path

from resumelens.classification.automata import classify

ROOT = Path(__file__).resolve().parent.parent
NORMALIZED_DIR = ROOT / "data" / "normalized"
OUTPUT_DIR = ROOT / "data" / "classified"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for normalized_path in sorted(NORMALIZED_DIR.glob("*.json")):
        normalized = json.loads(normalized_path.read_text(encoding="utf-8"))
        result = {
            "normalized_qualifications": normalized["normalized_qualifications"],
            "profiles": classify(normalized["normalized_qualifications"]),
        }
        output_path = OUTPUT_DIR / normalized_path.name
        output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        accepted = [p for p, v in result["profiles"].items() if v == "ACCEPTED"]
        print(f"{normalized_path.name} -> {accepted}")


if __name__ == "__main__":
    main()
