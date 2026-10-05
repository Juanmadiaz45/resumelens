"""Command-line entry point: run the ResumeLens pipeline on one résumé file.

Usage: python -m resumelens.ui.cli <resume.txt> [--out-dir DIR]
"""

import argparse
import sys
from pathlib import Path

from resumelens.dsl.model import CandidateValidationError
from resumelens.pipeline.pipeline import PipelineResult, run


def print_summary(result: PipelineResult) -> None:
    print(f"candidate: {result.model.name}")
    print()
    print("stage 1 — extracted qualifications:")
    for key in ("languages", "frameworks", "databases", "cloud_tools", "data_tools", "tools"):
        values = result.extracted[key]
        print(f"  {key:12s} {', '.join(values) if values else '-'}")
    print()
    print("stage 2 — normalized qualifications:")
    print(f"  {', '.join(result.normalized) if result.normalized else '-'}")
    print()
    print("stage 3 — profile classification:")
    for profile, verdict in result.classification.items():
        print(f"  {profile:28s} {verdict}")
    print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="resumelens",
        description="Check a plain-text résumé against ResumeLens profile patterns.",
    )
    parser.add_argument("resume", type=Path, help="path to a plain-text résumé")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="directory for the HTML page (default: next to the résumé file)",
    )
    args = parser.parse_args(argv)

    if not args.resume.is_file():
        print(f"error: no such file: {args.resume}", file=sys.stderr)
        return 2

    text = args.resume.read_text(encoding="utf-8")
    try:
        result = run(text)
    except CandidateValidationError as error:
        print(f"error: the candidate profile was rejected by the grammar:\n{error}", file=sys.stderr)
        return 1

    print_summary(result)

    out_dir = args.out_dir or args.resume.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.resume.stem}.html"
    out_path.write_text(result.html, encoding="utf-8")
    print(f"html page written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
