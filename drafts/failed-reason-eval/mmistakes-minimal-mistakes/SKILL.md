---
name: jekyll-minimal-mistakes-site
description: Scaffolds and configures a Jekyll personal site, blog, or portfolio using the Minimal Mistakes theme conventions, and should be used when a user wants to set up, customize, or troubleshoot a Jekyll-based site with theme skins, author profiles, navigation, and post/page layouts.
---

# Jekyll Minimal Mistakes Site

## Purpose

This skill helps set up and customize a Jekyll static site (personal site, blog, project documentation, or portfolio) that follows the conventions popularized by the Minimal Mistakes Jekyll theme: a `_config.yml`-driven skin system, author sidebar profiles, multiple post/page layouts, and taxonomy-based navigation (categories/tags/collections).

Apply this skill when a user asks to:
- Start a new Jekyll blog or portfolio site from scratch
- Add or customize a Minimal Mistakes-style theme skin (color palette)
- Configure author/sidebar metadata, navigation links, or social profiles
- Choose or set up a page layout (single, single with sidebar, splash, archive, collection)
- Set up categories, tags, or custom collections for content organization
- Debug common Jekyll/Liquid front-matter or build issues on a site using this theme structure

## When to use

Trigger this skill whenever the user's request involves building or maintaining a Jekyll site and mentions any of: Jekyll theme setup, GitHub Pages personal site, blog scaffolding with front matter, "minimal mistakes," author sidebar/profile config, post archive layouts, or site skins/color palettes.

## Core concepts to apply

1. **Config-driven customization**: Nearly all site-wide behavior (title, author, skin, navigation, plugins, pagination, SEO) is controlled through a single `_config.yml` at the site root, not scattered across templates. When customizing, prefer editing `_config.yml` over hardcoding values in layouts.

2. **Skins as a palette layer**: The theme ships with multiple pre-built color skins (e.g., "air", "contrast", "dark", "dirt", "neon", "mint", "plum", "sunrise") selected via a single `minimal_mistakes_skin` key in `_config.yml`. When a user wants to change the site's look and feel without a full redesign, recommend switching or authoring a skin variable set rather than rewriting CSS from scratch.

3. **Front matter drives layout and metadata**: Every post and page uses YAML front matter to declare `layout`, `title`, `categories`, `tags`, `author_profile`, `toc` (table of contents), `classes` (e.g., `wide` for full-width), and `header` (for hero images). When drafting a new post/page, always start with front matter that matches the intended layout's expected keys.

4. **Layout types map to content purpose**:
   - `single` — a standard post/page with sidebar
   - `single` with `classes: wide` — full-width content, no sidebar
   - `splash` — a landing/home page with a hero and feature rows
   - `archive`/`categories`/`tags` — auto-generated listing pages
   - `collection` — custom content types beyond posts/pages (e.g., portfolio items, docs)

   When a user describes what a page is for, pick the layout that matches its purpose rather than defaulting to `single` for everything.

5. **Navigation and author data live in `_data/`**: Sidebar links, main navigation menus, and multi-author profiles are typically defined as YAML files under `_data/navigation.yml` and `_data/authors.yml` (or an `author:` block in `_config.yml` for single-author sites), not hardcoded into layout files. Point users here when they want to add a nav link or contributor bio.

6. **Content organization via collections**: Beyond the default `_posts` folder, custom collections (declared under a `collections:` key in `_config.yml`) let a site hold structured content like portfolio pieces, documentation pages, or team profiles, each with their own layout and permalink pattern.

## Step-by-step guidance

When asked to set up a new site:
1. Confirm the site's purpose (blog, portfolio, docs, personal site) — this determines which layouts and collections are needed.
2. Establish `_config.yml` first: site title, description, URL, author info, and a chosen skin.
3. Set up `_data/navigation.yml` for top-level nav links.
4. Create an initial post or page with front matter matching the chosen layout.
5. If the site needs custom content types (e.g., a portfolio), define a collection in `_config.yml` before creating collection items.

When asked to customize an existing site:
1. Locate `_config.yml` first to understand current skin, plugins, and collections before making changes.
2. Check whether the desired change belongs in `_config.yml` (site-wide), `_data/` (navigation/authors), or front matter (per-page) — avoid editing layout/include files for things that are meant to be data-driven.
3. When changing visual appearance, prefer the skin variable/system over ad hoc CSS overrides, unless the user explicitly wants a one-off style.

When troubleshooting build or rendering issues:
1. Check front matter syntax first (missing `---` delimiters, incorrect `layout` name, malformed YAML) — this is the most common source of Jekyll build failures.
2. Verify that any referenced collection, category, or tag is properly declared/spelled consistently between `_config.yml` and the content files that reference it.
3. Confirm plugin-dependent features (pagination, SEO tags, sitemap) have their corresponding plugin listed under the `plugins:` key in `_config.yml`.
