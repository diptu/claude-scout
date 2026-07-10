---
name: mkdocs-material-docs
description: Helps set up, configure, and write content for documentation sites built with MkDocs and the Material theme; use when a user wants to create, structure, or troubleshoot a MkDocs-based documentation project.
---

# MkDocs Material Documentation Sites

This skill helps build and maintain documentation sites powered by MkDocs with the Material theme — a popular setup for project docs, wikis, and knowledge bases that renders Markdown into a fast, searchable, themeable static site.

## When to apply this skill

Apply this skill when the user wants to:
- Start a new documentation site from scratch
- Configure `mkdocs.yml` (navigation, theme options, plugins)
- Structure Markdown content using Material-specific features (admonitions, tabs, code annotations, diagrams)
- Fix build errors or broken navigation/links in an existing MkDocs project
- Improve site organization, search, or readability

## Step-by-step guidance

### 1. Setting up a new project

- Confirm Python and pip are available, since MkDocs is a Python package.
- The core dependencies are `mkdocs` and `mkdocs-material`. A `requirements.txt` or equivalent should pin both explicitly rather than relying on latest.
- A minimal project needs:
  - `mkdocs.yml` at the project root (site config)
  - a `docs/` directory containing `index.md` and other Markdown pages
- Recommend the standard local preview workflow (`mkdocs serve`) for iterating on content, and a build step (`mkdocs build`) that outputs a static `site/` directory for deployment. Don't run these commands automatically — describe them for the user to run.

### 2. Configuring `mkdocs.yml`

Key sections to get right:
- `site_name`, `site_url`, `repo_url` — identify the project and link back to source
- `theme.name: material` plus `theme.features` — enable only the features the content actually needs (e.g. `navigation.tabs`, `navigation.sections`, `content.code.copy`, `search.suggest`) rather than turning everything on by default
- `nav` — an explicit tree mapping page titles to file paths; keep it in sync whenever pages are added, renamed, or removed, since Material does not auto-discover pages into the nav
- `plugins` — commonly `search`, and `mkdocstrings` if the docs need to pull in API references from source code
- `markdown_extensions` — Material's richer content (admonitions, tabbed content, code annotations) depends on specific `pymdownx` extensions being enabled here; if a feature isn't rendering, check this list first before assuming a bug

### 3. Writing content with Material's Markdown extensions

Guide content authors toward these idiomatic patterns instead of plain Markdown workarounds:
- **Admonitions** (`!!! note`, `!!! warning`, `!!! tip`) for callout boxes instead of bold text or blockquotes
- **Content tabs** (`=== "Tab title"`) for showing the same concept across multiple languages or platforms
- **Code blocks with annotations** for walking through code line-by-line inline in the docs
- **Icons and emoji shortcodes** (e.g. `:material-check:`) since Material ships an icon set — favor these over inline images for simple glyphs

### 4. Diagnosing common problems

- Broken internal links usually trace back to a mismatch between the `nav` entries and actual file paths under `docs/` — check both.
- Extensions not rendering (tabs, admonitions showing as raw text) almost always mean the corresponding `markdown_extensions` entry is missing from `mkdocs.yml`.
- Search not returning expected results often means the `search` plugin is missing from `plugins`, or content is excluded via `.mkdocsignore`-style config.
- Slow builds on large doc sets are usually from unoptimized image assets or excessive use of plugins that reprocess every page (e.g. certain social-card or minification plugins) — suggest scoping these down before adding more content.

### 5. Reviewing structure

When asked to review or reorganize an existing docs site, check:
- Whether the `nav` reflects a logical reading order for a newcomer, not just alphabetical file order
- Whether there's a single clear entry point (`index.md`) that orients readers before they dive into reference pages
- Whether reference material (API docs, config schemas) is separated from narrative material (tutorials, guides), since mixing the two styles on one page tends to make both harder to scan
