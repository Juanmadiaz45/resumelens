"""Turn the outputs of stages 1-3 into candidate profile DSL text.

The text is then parsed by model.parse_candidate. Keeping serialization separate from
parsing means the grammar is the only thing that decides whether a candidate profile is
well-formed, not the code that produced it.
"""

DEGREE_NAMES = {
    "b.sc.": "B.Sc.",
    "bsc": "B.Sc.",
    "m.sc.": "M.Sc.",
    "msc": "M.Sc.",
    "bachelor": "Bachelor",
    "master": "Master",
    "phd": "PhD",
}


def _quote(value: str) -> str:
    return '"' + value.replace('"', "'") + '"'


def _degree(raw: str) -> str:
    return DEGREE_NAMES.get(raw.lower(), raw)


def serialize_candidate(extracted: dict, normalized: list[str], classification: dict) -> str:
    lines = [f"candidate {_quote(extracted['name'])}"]

    contact = extracted["contact"]
    contact_items = []
    if contact["email"]:
        contact_items.append(f"email {contact['email']}")
    if contact["phone"]:
        contact_items.append(f"phone {contact['phone']}")
    if contact["linkedin"]:
        contact_items.append(f"linkedin {contact['linkedin']}")
    if contact["github"]:
        contact_items.append(f"github {contact['github']}")
    lines.append(" ".join(["contact", *contact_items]))

    if extracted["experience_years"] is not None:
        lines.append(f"experience {extracted['experience_years']} years")

    for education in extracted["education"]:
        lines.append(
            f"education {_degree(education['degree'])} {_quote(education['field'])}"
        )

    lines.append("skills " + " ".join(normalized))

    results = " ".join(f"{profile} {verdict}" for profile, verdict in classification.items())
    lines.append(f"classification {results}")

    return "\n".join(lines) + "\n"
