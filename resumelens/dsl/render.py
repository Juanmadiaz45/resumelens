"""Render a validated candidate profile model as a short HTML page or Markdown document."""

import html

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; color: #1f2933; }}
h1 {{ margin-bottom: 0.25rem; }}
h2 {{ font-size: 1.05rem; border-bottom: 1px solid #d9e2ec; padding-bottom: 0.25rem; margin-top: 1.5rem; }}
ul {{ padding-left: 1.2rem; }}
.skill {{ display: inline-block; background: #e4ecf7; border-radius: 4px; padding: 0.15rem 0.5rem; margin: 0.15rem; font-family: ui-monospace, monospace; font-size: 0.85rem; }}
.accepted {{ color: #1b7f3b; font-weight: 600; }}
.rejected {{ color: #8a94a6; }}
</style>
</head>
<body>
<h1>{name}</h1>
{contact}
{experience}
{education}
<h2>Skills</h2>
<div>{skills}</div>
<h2>Profile classification</h2>
<ul>
{classification}
</ul>
</body>
</html>
"""


def _contact_html(contact_items: list[tuple[str, str]]) -> str:
    if not contact_items:
        return ""
    items = "".join(
        f"<li><strong>{html.escape(label)}:</strong> {html.escape(value)}</li>"
        for label, value in contact_items
    )
    return f"<h2>Contact</h2>\n<ul>{items}</ul>"


CONTACT_LABELS = {"email": "Email", "phone": "Phone", "linkedin": "LinkedIn", "github": "GitHub"}


def _contact_items(model) -> list[tuple[str, str]]:
    contact = model.contact
    items = []
    for attribute, label in CONTACT_LABELS.items():
        value = getattr(contact, attribute, None)
        if value:
            items.append((label, value))
    return items


def render_html(model) -> str:
    contact = _contact_html(_contact_items(model))

    experience = ""
    if model.experiences:
        years = ", ".join(f"{e.years} years" for e in model.experiences)
        experience = f"<h2>Experience</h2>\n<p>{html.escape(years)}</p>"

    education = ""
    if model.educations:
        entries = "".join(
            f"<li>{html.escape(e.degree)} in {html.escape(e.field)}</li>"
            for e in model.educations
        )
        education = f"<h2>Education</h2>\n<ul>{entries}</ul>"

    skills = "".join(f'<span class="skill">{html.escape(s.name)}</span>' for s in model.skills)

    classification = "".join(
        f'<li class="{r.verdict.lower()}">{html.escape(r.profile)}: {r.verdict}</li>'
        for r in model.results
    )

    return HTML_TEMPLATE.format(
        title=html.escape(f"{model.name} — ResumeLens"),
        name=html.escape(model.name),
        contact=contact,
        experience=experience,
        education=education,
        skills=skills,
        classification=classification,
    )


def render_markdown(model) -> str:
    lines = [f"# {model.name}", ""]

    contact_items = _contact_items(model)
    if contact_items:
        lines += ["## Contact", ""]
        lines += [f"- **{label}:** {value}" for label, value in contact_items]
        lines.append("")

    if model.experiences:
        lines += ["## Experience", ""]
        lines += [f"- {e.years} years" for e in model.experiences]
        lines.append("")

    if model.educations:
        lines += ["## Education", ""]
        lines += [f"- {e.degree} in {e.field}" for e in model.educations]
        lines.append("")

    lines += ["## Skills", "", " ".join(f"`{s.name}`" for s in model.skills), ""]

    lines += ["## Profile classification", ""]
    lines += [f"- {r.profile}: **{r.verdict}**" for r in model.results]

    return "\n".join(lines) + "\n"
