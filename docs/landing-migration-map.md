# Landing Migration Map

This map documents how legacy `data/landing.yml` fields map to the current Quarto-first landing model.

## Legacy to new ownership

| Legacy field | New source of truth | Notes |
| --- | --- | --- |
| `course.title` | `_sections/hero.qmd` (`<h1>`) | Static authored copy. |
| `course.subtitle` | `_sections/hero.qmd` (`<p class="hero__subtitle">`) | Static authored copy. |
| `course.logo` | `_sections/hero.qmd` (`<img src=...>`) | Static authored asset reference. |
| `hero_actions[0].label` | `data/ui.yml` (`hero_view_current_label`) | Label is editable without Python changes. |
| `hero_actions[0].href` | `data/instances.yml` current `instance_url` | Derived dynamically; no manual duplication. |
| `hero_actions[0].style` | `scripts/generate_landing.py` template class (`hero-cta--secondary`) | Presentation class is fixed in generator output. |
| `hero_actions[1].label` | `data/ui.yml` (`hero_registration_open_label`) | Used only when current instance has registration URL. |
| `hero_actions[1].href` | `data/instances.yml` current `registration_url` | Button omitted when empty. |
| `hero_actions[1].style` | `scripts/generate_landing.py` template class (`hero-cta--primary`) | Presentation class is fixed in generator output. |
| `instances.title` | `data/ui.yml` (`instances_band_title`) | Controls the banner heading above the instance pills. |
| `cards[*]` content | `_sections/top-cards.qmd` | Static authored copy/structure. |
| `founders[*]` | `_sections/bottom-cards.qmd` | Static authored copy/structure. |
| `contributors[*]` | `_sections/bottom-cards.qmd` | Static authored copy/structure. |
| `footer.license` | `_sections/footer.qmd` | Static authored copy. |
| `footer.built_with` | `_sections/footer.qmd` | Static authored copy. |
| `footer.github_url` | `_sections/footer.qmd` | Static authored URL. |

## New dynamic-only labels

These labels did not exist as explicit legacy keys but are now configurable in `data/ui.yml`:

- `instances_band_title`

## Removed legacy file

- `data/landing.yml` is intentionally removed.
- Landing copy now lives in `_sections/*.qmd`.
- Dynamic elements are generated into `_generated/*.qmd` from validated metadata.
