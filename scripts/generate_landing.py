#!/usr/bin/env python3
"""Validate landing metadata and generate dynamic Quarto partials."""

from __future__ import annotations

import html
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1]
INSTANCES_FILE = ROOT / "data" / "instances.yml"
UI_FILE = ROOT / "data" / "ui.yml"
GENERATED_DIR = ROOT / "_generated"
HERO_ACTIONS_FILE = GENERATED_DIR / "hero-actions.qmd"
INSTANCES_BAND_FILE = GENERATED_DIR / "instances-band.qmd"


class ValidationError(ValueError):
    """Raised when YAML data fails validation."""


UI_DEFAULTS = {
    "hero_view_current_label": "View current instance",
    "hero_registration_open_label": "Registration open!",
    "current_instance_note_label": "Current course instance",
    "current_instance_open_label": "Open",
    "current_instance_registration_label": "Registration",
    "previous_instances_title": "Previous course instances",
    "no_previous_instances_label": "No previous instances published yet.",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def load_yaml_dict(path: Path) -> dict[str, Any]:
    content = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict):
        path_label = str(path)
        try:
            path_label = str(path.relative_to(ROOT))
        except ValueError:
            pass
        raise ValidationError(
            f"{path_label} must contain a top-level mapping/object."
        )
    return content


def load_ui_labels(path: Path) -> dict[str, str]:
    if not path.exists():
        return UI_DEFAULTS.copy()

    content = load_yaml_dict(path)
    unknown_keys = sorted(set(content.keys()) - set(UI_DEFAULTS.keys()))
    if unknown_keys:
        unknown_fmt = ", ".join(repr(key) for key in unknown_keys)
        raise ValidationError(
            "ui.yml contains unknown key(s): "
            f"{unknown_fmt}. Allowed keys: {', '.join(UI_DEFAULTS.keys())}."
        )

    labels = UI_DEFAULTS.copy()
    for key, default in UI_DEFAULTS.items():
        value = content.get(key, default)
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(
                f"ui.yml.{key} must be a non-empty string when provided."
            )
        labels[key] = value
    return labels


def _require_string(data: dict[str, Any], key: str, context: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{context}.{key} must be a non-empty string.")
    return value


def _is_http_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _is_relative_url(value: str) -> bool:
    return value.startswith("./") or (
        value.startswith("/") and not value.startswith("//")
    )


def _validate_slug(slug: str, context: str) -> None:
    if not re.fullmatch(r"\d{4}", slug):
        raise ValidationError(f"{context}.slug must be exactly 4 digits (got {slug!r}).")
    if slug == "0000":
        return

    month = int(slug[2:])
    if month < 1 or month > 12:
        raise ValidationError(
            f"{context}.slug month must be between 01 and 12 (got {slug!r})."
        )


def _validate_instance_url(url: str, context: str) -> None:
    if re.fullmatch(r"\./\d{4}/", url):
        return
    if _is_http_url(url):
        return
    raise ValidationError(
        f"{context}.instance_url must be './NNNN/' or an absolute http(s) URL."
    )


def _validate_registration_url(url: str, context: str) -> None:
    if not url:
        return
    if url.startswith("//"):
        raise ValidationError(
            f"{context}.registration_url must not be protocol-relative (//...)."
        )
    if _is_http_url(url) or _is_relative_url(url):
        return
    raise ValidationError(
        f"{context}.registration_url must be empty, relative, or absolute http(s)."
    )


def validate_instances_data(data: dict[str, Any]) -> list[dict[str, Any]]:
    instances = data.get("instances")
    if not isinstance(instances, list) or not instances:
        raise ValidationError("instances.yml must define a non-empty 'instances' list.")

    normalized: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()

    for index, raw in enumerate(instances):
        context = f"instances[{index}]"
        if not isinstance(raw, dict):
            raise ValidationError(f"{context} must be an object/mapping.")

        slug = _require_string(raw, "slug", context)
        _validate_slug(slug, context)
        if slug in seen_slugs:
            raise ValidationError(f"{context}.slug {slug!r} is duplicated.")
        seen_slugs.add(slug)

        label = _require_string(raw, "label", context)
        status = _require_string(raw, "status", context)
        if status not in {"current", "previous"}:
            raise ValidationError(f"{context}.status must be 'current' or 'previous'.")

        visible = raw.get("visible")
        if not isinstance(visible, bool):
            raise ValidationError(f"{context}.visible must be a boolean.")

        instance_url = _require_string(raw, "instance_url", context)
        _validate_instance_url(instance_url, context)
        if (
            re.fullmatch(r"\./\d{4}/", instance_url)
            and instance_url != f"./{slug}/"
        ):
            raise ValidationError(
                f"{context}.instance_url must match slug for relative links "
                f"(expected './{slug}/', got {instance_url!r})."
            )

        registration_url = raw.get("registration_url", "")
        if registration_url is None:
            registration_url = ""
        if not isinstance(registration_url, str):
            raise ValidationError(f"{context}.registration_url must be a string.")
        _validate_registration_url(registration_url, context)

        sort_key = raw.get("sort_key")
        if isinstance(sort_key, bool) or not isinstance(sort_key, int):
            raise ValidationError(f"{context}.sort_key must be an integer.")

        normalized.append(
            {
                "slug": slug,
                "label": label,
                "status": status,
                "visible": visible,
                "instance_url": instance_url,
                "registration_url": registration_url,
                "sort_key": sort_key,
            }
        )

    current_instances = [item for item in normalized if item["status"] == "current"]
    if len(current_instances) != 1:
        raise ValidationError("instances.yml must contain exactly one status='current' entry.")
    if not current_instances[0]["visible"]:
        raise ValidationError("The current instance must be visible: true.")

    return normalized


def _render_hero_actions(current: dict[str, Any], ui_labels: dict[str, str]) -> str:
    actions = [
        (
            '<a class="hero-cta hero-cta--secondary" href="{href}">{label}</a>'
        ).format(
            href=esc(current["instance_url"]),
            label=esc(ui_labels["hero_view_current_label"]),
        )
    ]
    if current["registration_url"]:
        actions.append(
            '<a class="hero-cta hero-cta--primary" href="{href}">{label}</a>'.format(
                href=esc(current["registration_url"]),
                label=esc(ui_labels["hero_registration_open_label"]),
            )
        )
    return "\n".join(actions) + "\n"


def _render_previous_instance_buttons(
    previous: list[dict[str, Any]], ui_labels: dict[str, str]
) -> str:
    if not previous:
        return '<p class="empty-note">{text}</p>'.format(
            text=esc(ui_labels["no_previous_instances_label"])
        )

    buttons = []
    for item in previous:
        buttons.append(
            '<a class="instance-pill" href="{href}">{label}</a>'.format(
                href=esc(item["instance_url"]),
                label=esc(item["label"]),
            )
        )
    return "\n".join(buttons)


def _render_instances_band(instances: list[dict[str, Any]], ui_labels: dict[str, str]) -> str:
    current = next(item for item in instances if item["status"] == "current")
    visible_instances = [item for item in instances if item["visible"]]
    previous = sorted(
        [item for item in visible_instances if item["slug"] != current["slug"]],
        key=lambda item: item["sort_key"],
        reverse=True,
    )

    current_registration_button = ""
    if current["registration_url"]:
        current_registration_button = (
            '<a class="instance-register" href="{href}">{label}</a>'.format(
                href=esc(current["registration_url"]),
                label=esc(ui_labels["current_instance_registration_label"]),
            )
        )

    previous_buttons = _render_previous_instance_buttons(previous, ui_labels)

    return f"""
<section class="instances-band">
  <div class="current-instance-card">
    <p class="instance-label">{esc(ui_labels["current_instance_note_label"])}</p>
    <h2 class="instance-title">{esc(current["label"])}</h2>
    <a class="instance-link" href="{esc(current["instance_url"])}">{esc(ui_labels["current_instance_open_label"])}</a>
    {current_registration_button}
  </div>

  <div class="previous-instances">
    <h2 class="section-title">{esc(ui_labels["previous_instances_title"])}</h2>
    <div class="instance-grid">
      {previous_buttons}
    </div>
  </div>
</section>
""".strip() + "\n"


def build_dynamic_partials(
    instances: list[dict[str, Any]], ui_labels: dict[str, str]
) -> tuple[str, str]:
    current = next(item for item in instances if item["status"] == "current")
    return _render_hero_actions(current, ui_labels), _render_instances_band(
        instances, ui_labels
    )


def write_generated_partials(
    instances: list[dict[str, Any]], ui_labels: dict[str, str]
) -> None:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    hero_actions, instances_band = build_dynamic_partials(instances, ui_labels)
    HERO_ACTIONS_FILE.write_text(hero_actions, encoding="utf-8")
    INSTANCES_BAND_FILE.write_text(instances_band, encoding="utf-8")


def main() -> None:
    instances_data = load_yaml_dict(INSTANCES_FILE)
    instances = validate_instances_data(instances_data)
    ui_labels = load_ui_labels(UI_FILE)
    write_generated_partials(instances, ui_labels)
    print(
        "Generated dynamic partials:",
        HERO_ACTIONS_FILE.relative_to(ROOT),
        INSTANCES_BAND_FILE.relative_to(ROOT),
    )


if __name__ == "__main__":
    try:
        main()
    except ValidationError as exc:
        print(f"ValidationError: {exc}")
        raise SystemExit(1) from exc
