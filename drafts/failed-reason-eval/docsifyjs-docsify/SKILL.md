---
name: docsify-docs-site
description: Sets up and maintains a Docsify-powered documentation site (dynamic markdown-rendered docs with no static build step) — use when a user wants to scaffold a lightweight docs site, add pages/navigation to an existing one, or convert a folder of markdown files into a browsable site.
---

# Docsify Documentation Site

Docsify is a documentation site generator that renders Markdown files into a
website *at load time*, directly in the browser — there is no static build
step, no generated HTML files to commit, and no bundler. A docs site is just
a folder of `.md` files plus a single `index.html` that loads the docsify
runtime from a CDN (or a locally vendored copy) and points it at that folder.

Apply this skill when the user wants to:
- Start a new lightweight documentation site for a project.
- Turn an existing folder of Markdown notes/docs into a browsable site.
- Add navigation (sidebar, navbar), search, or plugins to a docsify site.
- Debug why pages, links, or sidebar entries aren't showing up in docsify.

## Core mental model

Docsify does NOT pre-render Markdown into HTML files. Instead:
1. The browser loads `index.html`, which contains a small `window.$docsify`
   config object and a `<script>` tag pulling in the docsify runtime.
2. Docsify reads the current URL hash (e.g. `#/guide/install`), maps it to a
   Markdown file path (e.g. `guide/install.md`) relative to the docs root,
   fetches that file via HTTP, and renders it client-side.
3. Because rendering happens per-request in the browser, editing a `.md` file
   and refreshing the page is enough to see changes — no build/compile step.

This means: the site *must* be served over HTTP (docsify fetches files via
`fetch`/XHR), not opened as a raw `file://` path, or the markdown fetches
will fail silently or be blocked by the browser.

## Step-by-step: scaffolding a new docsify site

1. Create the docs root folder (commonly `docs/`) if it doesn't exist.
2. Create `docs/index.html` with:
   - A `window.$docsify = { name: '<project name>', repo: '<repo url if any>' }`
     config object (add more keys as needed — see Configuration below).
   - A `<div id="app"></div>` mount point.
   - A `<script>` tag loading `//cdn.jsdelivr.net/npm/docsify@4/lib/docsify.min.js`
     (or a pinned version) placed after the config script, right before
     `</body>`.
3. Create `docs/README.md` — this is the homepage content, rendered for `/`.
4. Optionally create `docs/_sidebar.md` for a custom sidebar (a Markdown
   bullet list of links) and set `loadSidebar: true` in the config to enable
   it. Without this file, docsify auto-generates a flat list from headings.
5. Optionally create `docs/_navbar.md` for a top navbar, and set
   `loadNavbar: true`.
6. Optionally create `docs/_coverpage.md` for a landing/cover page, and set
   `coverpage: true`.
7. Tell the user how to preview locally: any static file server pointed at
   the `docs/` folder works (e.g. `docsify-cli`'s `docsify serve docs`, or
   any generic HTTP static server) — just not `file://` directly, per the
   note above.

## Step-by-step: adding a page to an existing docsify site

1. Locate the docs root (the folder containing `index.html` and `README.md`
   for a docsify site — check `window.$docsify.basePath` in `index.html` if
   it's not the default).
2. Add the new `.md` file at the appropriate path relative to that root.
3. If the site uses a manual `_sidebar.md` (check `loadSidebar` in the
   config), add a link to the new page there — docsify will NOT show it
   automatically once a custom sidebar file exists.
4. If the site uses auto-generated sidebars, no extra step is needed; the
   page becomes reachable via its URL hash (`#/path/to/page`) and will
   appear in generated navigation once linked from elsewhere.

## Common configuration keys (in `window.$docsify`)

- `name` — site title shown in the sidebar.
- `repo` — GitHub repo URL, renders a corner ribbon link.
- `loadSidebar` / `loadNavbar` — enable `_sidebar.md` / `_navbar.md`.
- `subMaxLevel` — how deep headings are auto-included in sidebar nav.
- `auto2top` — scroll to top on page navigation.
- `search` — enable the built-in full-text search plugin (requires including
  its script tag too, e.g. `docsify/lib/plugins/search.min.js`).
- `alias` — map custom URL paths to markdown files (useful for shared pages
  like a single CHANGELOG.md linked from multiple sections).
- `basePath` — set if docs are served from a subpath or a different origin
  than `index.html`.

## Troubleshooting checklist

- Blank page / nothing renders → confirm the site is served via HTTP, not
  opened as a local file.
- Sidebar missing entries → check whether `_sidebar.md` exists and
  `loadSidebar` is set; a stale manual sidebar is the most common cause of
  "I added a page but it's not showing."
- 404s for pages that exist → check `basePath`/routing mode (hash vs history
  mode) and confirm the file path matches the URL hash exactly, including
  case.
- Styling/plugins not applying → confirm the corresponding CDN `<script>`
  (or vendored file) is actually included in `index.html`, since each
  docsify feature (search, plugins, themes) is an opt-in separate script.
