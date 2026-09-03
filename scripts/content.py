from pathlib import Path
import re
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT / "content"


def load_content_sections(content):
    sections = content.get("sections", [])

    result = []

    for section in sections:

        section_id = section["id"]
        section_dir = CONTENT_DIR / section_id

        if not section_dir.exists():
            raise ValueError(
                f"Content section '{section_id}' does not exist: "
                f"{section_dir}"
            )

        pages = []

        for path in section_dir.glob("*.qmd"):

            text = path.read_text(encoding="utf-8")

            title = extract_front_matter_value(text, "title")
            order = extract_front_matter_value(text, "order")

            if not title:
                raise ValueError(
                    f"Content page '{path}' is missing a title"
                )

            pages.append({
                "title": title,
                "path": path,
                "order": int(order) if order else None,
            })

        has_order = any(page["order"] is not None for page in pages)

        if has_order and any(page["order"] is None for page in pages):
            raise ValueError(
                f"Section '{section_id}' mixes pages with and without order"
            )

        if has_order:
            pages.sort(key=lambda page: page["order"])
        else:
            pages.sort(key=lambda page: page["path"].name.lower())

        result.append({
            "id": section_id,
            "label": section["label"],
            "title": section["title"],
            "pages": pages,
        })

    return result


def extract_front_matter_value(text, key):

    if not text.startswith("---"):
        return None

    parts = text.split("---", 2)

    if len(parts) != 3:
        return None

    front_matter = yaml.safe_load(parts[1]) or {}

    return front_matter.get(key)
