#!/usr/bin/env python3
"""Generate landing page qmd from YAML data files."""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
LANDING_FILE = ROOT / "data" / "landing.yml"
INSTANCES_FILE = ROOT / "data" / "instances.yml"
TEMPLATE_FILE = ROOT / "templates" / "index.template.qmd"
OUTPUT_FILE = ROOT / "index.qmd"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_yaml(path: Path) -> dict[str, Any]:
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    return content if isinstance(content, dict) else {}


def render_actions(actions: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for action in actions:
        label = esc(action.get("label", "Learn more"))
        href = esc(action.get("href", "#"))
        style = esc(action.get("style", "secondary"))
        parts.append(
            f'<a class="hero-cta hero-cta--{style}" href="{href}">{label}</a>'
        )
    return "\n".join(parts)


def render_card(card: dict[str, Any]) -> str:
    icon = esc(card.get("icon", "bi-square"))
    title = esc(card.get("title", ""))
    body_parts: list[str] = []

    for paragraph in card.get("paragraphs", []):
        body_parts.append(f"<p>{esc(paragraph)}</p>")

    ordered = card.get("ordered", [])
    if ordered:
        items = "".join(f"<li>{esc(item)}</li>" for item in ordered)
        body_parts.append(f"<ol>{items}</ol>")

    bullets = card.get("bullets", [])
    if bullets:
        items = "".join(f"<li>{esc(item)}</li>" for item in bullets)
        body_parts.append(f"<ul>{items}</ul>")

    body_html = "\n".join(body_parts)

    return f"""
<article class="info-card">
  <div class="card-headline">
    <i class="bi {icon}"></i>
    <h3>{title}</h3>
  </div>
  <div class="card-content">
    {body_html}
  </div>
</article>
""".strip()


def pick_current_instance(instances: list[dict[str, Any]]) -> dict[str, Any] | None:
    current = next((item for item in instances if item.get("status") == "current"), None)
    if current:
        return current
    if not instances:
        return None
    return sorted(instances, key=lambda item: item.get("sort_key", 0), reverse=True)[0]


def render_instance_button(instance: dict[str, Any]) -> str:
    label = esc(instance.get("label", instance.get("slug", "Instance")))
    url = esc(instance.get("instance_url", "#"))
    return f'<a class="instance-pill" href="{url}">{label}</a>'


def render_people(persons: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for person in persons:
        name = esc(person.get("name", ""))
        role = esc(person.get("role", ""))
        parts.append(f"<li><strong>{name}</strong><span>{role}</span></li>")
    return "\n".join(parts)


def main() -> None:
    landing = load_yaml(LANDING_FILE)
    instances_data = load_yaml(INSTANCES_FILE)

    visible_instances = [
        item
        for item in instances_data.get("instances", [])
        if isinstance(item, dict) and item.get("visible", True)
    ]

    current = pick_current_instance(visible_instances)
    previous = [item for item in visible_instances if item is not current]
    previous = sorted(previous, key=lambda item: item.get("sort_key", 0), reverse=True)

    cards = landing.get("cards", [])
    if not isinstance(cards, list):
        cards = []

    actions = landing.get("hero_actions", [])
    if not isinstance(actions, list):
        actions = []

    top_cards_html = "\n".join(
        render_card(card) for card in cards if isinstance(card, dict)
    )

    previous_cards_html = "\n".join(render_instance_button(item) for item in previous)
    if not previous_cards_html:
        previous_cards_html = "<p class=\"empty-note\">No previous instances published yet.</p>"

    current_registration_button = ""
    current_title = "No active instance"
    current_link = "#"

    if current:
        current_title = esc(current.get("label", current.get("slug", "Current instance")))
        current_link = esc(current.get("instance_url", "#"))
        registration_url = current.get("registration_url")
        if registration_url:
            current_registration_button = (
                '<a class="instance-register" href="{}">Registration</a>'.format(
                    esc(registration_url)
                )
            )

    course = landing.get("course", {}) if isinstance(landing.get("course"), dict) else {}
    footer = landing.get("footer", {}) if isinstance(landing.get("footer"), dict) else {}

    replacements = {
        "{{COURSE_TITLE}}": esc(course.get("title", "Course title")),
        "{{COURSE_SUBTITLE}}": esc(course.get("subtitle", "Course subtitle")),
        "{{COURSE_LOGO}}": esc(course.get("logo", "img/SciLifeLab_Logotype_NEG.png")),
        "{{CURRENT_INSTANCE_NOTE}}": esc(
            course.get("current_instance_note", "Current course instance")
        ),
        "{{HERO_ACTIONS}}": render_actions(actions),
        "{{TOP_CARDS}}": top_cards_html,
        "{{CURRENT_INSTANCE_TITLE}}": current_title,
        "{{CURRENT_INSTANCE_LINK}}": current_link,
        "{{CURRENT_REGISTRATION_BUTTON}}": current_registration_button,
        "{{PREVIOUS_INSTANCE_CARDS}}": previous_cards_html,
        "{{FOUNDERS_LIST}}": render_people(landing.get("founders", [])),
        "{{CONTRIBUTORS_LIST}}": render_people(landing.get("contributors", [])),
        "{{FOOTER_LICENSE}}": esc(footer.get("license", "")),
        "{{FOOTER_BUILT_WITH}}": esc(footer.get("built_with", "")),
        "{{FOOTER_GITHUB_URL}}": esc(footer.get("github_url", "#")),
    }

    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    for key, value in replacements.items():
        template = template.replace(key, value)

    OUTPUT_FILE.write_text(template, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
