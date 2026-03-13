# The SciLifeLab Course Template

This repository publishes one website with two layers:

- the landing page at the root
- one subdirectory per course instance

Examples:

- `main` publishes the landing page to `/`
- `release-0000` publishes the course instance to `/0000/`
- `release-2505` publishes the course instance to `/2505/`

## The Simple Model

- `main` = landing page source
- `release-YYMM` = one course instance
- `gh-pages` = published output only

Use `main` when you want to change the landing page.

Use a `release-YYMM` branch when you want to change the actual course materials for one run.

Do not work directly on `gh-pages` unless you are recovering from a deployment problem.

## What Gets Deployed

1. Push to `main`
   - GitHub Actions renders the landing page.
   - The landing is published to the root of `gh-pages`.
2. Push to `release-YYMM`
   - GitHub Actions renders that course instance.
   - The instance is published to `gh-pages/YYMM/`.

The landing page does not auto-discover release branches. If you create a new instance branch, you must also update `data/instances.yml` on `main` if you want that instance to appear on the landing page.

## Which Files To Edit

### Landing page on `main`

Edit these files for most landing-page changes:

- `index.qmd`: top-level page shell
- `_sections/*.qmd`: authored landing sections
- `styles.css`: landing design and layout
- `data/instances.yml`: current/previous instance links and visibility
- `data/ui.yml`: landing UI labels

Dynamic partials are generated automatically:

- `_generated/hero-actions.qmd`
- `_generated/instances-band.qmd`

Do not edit `_generated/*` manually.

### Course instance on `release-YYMM`

Edit the Quarto course files on that branch:

- course `.qmd` pages
- branch-local `_quarto.yml`
- images and other branch-local course assets

## Common Workflows

### 1. Change the landing page

1. Work on `main`.
2. Edit the landing sections, styles, or landing data.
3. Run local checks:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pytest -q
quarto render
```

4. Push `main`.
5. GitHub Actions publishes the updated landing root.

### 2. Create a new course instance

1. Create a new branch from `release-0000`.
2. Name it `release-YYMM`, for example `release-2505`.
3. Update the course content on that branch.
4. Push the branch.
5. GitHub Actions publishes that instance to `gh-pages/YYMM/`.
6. Update `data/instances.yml` on `main` so the landing page links to it.

### 3. Update an existing course instance

1. Checkout the relevant `release-YYMM` branch.
2. Edit the course materials.
3. Push the branch.
4. GitHub Actions republishes only that instance directory.

### 4. Change which instance is current on the landing page

Edit `data/instances.yml` on `main`.

Rules enforced by validation:

- exactly one instance must have `status: current`
- the current instance must have `visible: true`
- relative instance URLs must match the slug

## How The Landing Is Built

The landing page is built in three layers:

1. Authored content
   - `index.qmd`
   - `_sections/*.qmd`
2. Data and generated fragments
   - `data/instances.yml`
   - `data/ui.yml`
   - `scripts/generate_landing.py`
   - `_generated/*.qmd`
3. Presentation
   - `styles.css`

Render flow:

1. `quarto render` starts
2. Quarto runs `scripts/generate_landing.py` as a pre-render step
3. the generator validates YAML data and writes `_generated/*.qmd`
4. `index.qmd` includes the authored sections
5. those sections include the generated fragments where needed
6. Quarto writes the final site to `_site/`

## GitHub Actions

- `.github/workflows/validate-landing.yml`
  - runs on pull requests to `main`
  - runs tests, renders the landing, and checks that no raw YAML leaks into `_site`

- `.github/workflows/deploy-landing.yml`
  - runs on push to `main`
  - publishes only landing-owned root files to `gh-pages`

- `.github/workflows/main.yml` on `release-*` branches
  - runs on push to release branches
  - publishes only the matching instance directory to `gh-pages`

## Important Rules

- `gh-pages` is machine-managed output
- keep `.nojekyll` on `gh-pages`
- never use a root-level deploy sync like `rsync -a --delete _site/ gh-pages/`
- keep raw YAML out of published output
- update `data/instances.yml` on `main` when instance visibility changes

## Additional Docs

- `docs/landing-runbook.md`
- `docs/landing-migration-map.md`
