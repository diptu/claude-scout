---
name: docusaurus-docs-site
description: Scaffolds, structures, and maintains a documentation website built with Docusaurus (versioned docs, sidebars, MDX, i18n, search, deployment); use when a user wants to create, organize, or troubleshoot a docs/knowledge-base site built on Docusaurus.
---

# Docusaurus Documentation Site

This skill helps set up and maintain a documentation website powered by Docusaurus, a static-site generator purpose-built for docs: versioned content, a left-nav sidebar generated from folder structure, MDX (Markdown + React components), built-in search, i18n, and one-command static builds deployable to any static host.

## When to apply this skill

Apply it when the user is:
- Starting a new documentation site from scratch ("set up docs for this project", "I need a docs website").
- Adding, reorganizing, or fixing content in an existing Docusaurus site (`docusaurus.config.js`/`.ts` present, or a `docs/` + `sidebars.js` pair with Docusaurus in `package.json`).
- Asking about sidebar ordering, versioning multiple releases of docs, adding a blog alongside docs, theming/branding, search integration, or deploying the built site.
- Migrating existing README/wiki content into a structured, navigable docs site.

## Core concepts to keep in mind

- **Docs vs. Blog vs. Pages**: Docusaurus has three content types — `docs/` (structured, sidebar-driven reference/guide content), `blog/` (reverse-chronological posts), and `src/pages/` (fully custom React/MDX pages, e.g. a landing page). Don't force blog-style content into `docs/` or vice versa.
- **Sidebar generation**: By default the sidebar mirrors the `docs/` folder structure and each file's front-matter (`sidebar_position`, `sidebar_label`). A `_category_.json` file in a folder controls that folder's label, position, and whether it collapses. Only hand-write `sidebars.js` when the default folder-derived sidebar isn't good enough (custom ordering across folders, hiding items, mixing in links).
- **Front matter matters**: Every doc page should have at least `id`/`title` (or rely on the first heading) and, when ordering matters, `sidebar_position`. `slug` overrides the generated URL path.
- **Versioning**: Docusaurus can snapshot the current `docs/` into a version (e.g. `1.0.0`) via its versioning command, after which `docs/` becomes "next"/unreleased and the snapshot is frozen under `versioned_docs/`. Only introduce versioning once a project actually ships doc-breaking releases — don't version a docs site prematurely.
- **MDX**: `.mdx` files can import and render React components inline (callouts, tabs, live code blocks). Plain `.md` is preferred unless a page genuinely needs interactivity.
- **i18n**: Translations live in a parallel `i18n/<locale>/` tree mirroring `docs/`; only set this up when multiple locales are actually required.

## Step-by-step guidance

1. **Clarify the goal first.** Ask (or infer from context) whether this is a brand-new site, a migration of existing content, or a fix/extension to an existing one. Check for `docusaurus.config.js`/`.ts` to determine which case applies.

2. **For a new site:**
   - Scaffold the standard structure: `docs/`, `blog/` (optional — omit if the user doesn't want a blog), `src/pages/`, `static/`, `docusaurus.config.js`, `sidebars.js`.
   - Fill in `docusaurus.config.js` with the project's real title, tagline, URL, and base path — never leave placeholder values like "My Site".
   - Group related docs into subfolders with a `_category_.json` per folder (`{"label": "...", "position": N}`) rather than hand-maintaining `sidebars.js`, unless custom cross-folder ordering is needed.
   - Start with a single `intro.md` (or equivalent) set as the sidebar's first item, and build out from there based on the project's actual features/APIs.

3. **For migrating existing content (README, wiki, Notion export, etc.):**
   - Don't dump the source as one giant page. Split it along its natural headings into separate doc pages, one topic per file, and let the folder structure express hierarchy.
   - Preserve existing internal links by converting them to relative Markdown links between doc files (Docusaurus rewrites these to the built URLs and can warn on broken links at build time — treat that warning as a checklist).
   - Carry over code samples as fenced code blocks with an explicit language tag so syntax highlighting works.

4. **For organizing/fixing an existing site:**
   - Read `sidebars.js` and the relevant `docs/` subfolder before changing ordering — prefer adjusting `sidebar_position` front matter or `_category_.json` over rewriting `sidebars.js` wholesale.
   - When a page needs interactive elements (tabs for multiple package managers, an embedded live code editor), convert it from `.md` to `.mdx` rather than reaching for raw HTML.
   - When docs need to describe multiple supported versions of a product, introduce versioning rather than duplicating pages by hand.

5. **Before finishing:**
   - Make sure every new doc page is reachable from the sidebar (no orphan pages) unless it's intentionally a landing page under `src/pages/`.
   - Check that internal cross-links use relative paths to other doc files, not hardcoded absolute URLs.
   - Confirm the site actually builds cleanly (no broken-link warnings, no missing front matter) before considering the docs work done.

## Guardrails

- Don't introduce versioning, i18n, or a custom React theme until the user's stated need actually requires it — each adds real maintenance overhead.
- Don't hand-author a fully custom `sidebars.js` when folder-based autogeneration with `_category_.json` files would do the same job with less upkeep.
- Keep generated/config values (site title, URL, GitHub edit links) accurate to the real project — never leave scaffold placeholder text in a finished site.
