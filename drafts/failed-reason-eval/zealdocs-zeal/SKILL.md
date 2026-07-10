---
name: offline-docset-lookup
description: Look up API and library documentation from local Zeal/Dash-style offline docsets instead of the web, and guide setup of a docset library when a project needs offline-first reference lookup.
---

# Offline Docset Lookup

This skill helps Claude answer documentation questions (API signatures, method behavior, configuration options, language/library references) by using a local offline documentation browser and its docset library, instead of assuming web access is available or guessing from training data alone.

## When to apply this skill

- The user is working in an environment with no or unreliable internet access and needs authoritative reference documentation for a language, framework, or library.
- The user explicitly mentions Zeal, Dash, docsets, or an "offline docs" workflow.
- Claude needs to verify an exact API signature, method name, or config option and a local docset is a faster or more reliable source than searching the web.
- The user wants to set up, organize, or query a personal offline reference library for repeated use across projects.

Do not apply this skill when the user has normal internet access and simply wants a quick web search — offline docsets are for cases where local, authoritative, versioned documentation is preferable or required.

## Background: what a docset is

A docset is a self-contained bundle of documentation for a single library, framework, or language (e.g. Python stdlib, a specific version of React, PostgreSQL) plus a search index, stored entirely on disk. An offline documentation browser like Zeal loads a directory of these docsets and lets you search across all of them by keyword, jumping straight to the matching page — no network round-trip, no ads, no version drift from "latest docs online" when you need an older API.

## Step-by-step guidance

1. **Determine if a local docset library exists.** Check for a conventional docset storage location (a `Zeal/Zeal/docsets` or `Dash/DocSets` style directory under the user's application data/config folder, or a project-local `docsets/` directory the user has pointed to). If the user hasn't said where their docsets live, ask before assuming a path.

2. **Identify the exact library/version needed.** Before searching, pin down which docset applies — e.g. "Python 3.11" vs "Python 2", or a specific framework major version — since offline docsets are versioned snapshots and picking the wrong one gives stale or wrong answers.

3. **Search within the relevant docset first, not generic training knowledge.** When a docset for the technology in question is available, treat it as the source of truth for exact signatures, parameter names, return types, and deprecation notes. Prefer quoting or paraphrasing what the docset actually says over recalling from memory, since local docs reflect the exact installed/pinned version the user cares about.

4. **If no matching docset exists locally, say so explicitly** rather than silently falling back to a web search or unstated assumptions. Offer to either use general knowledge with a clear caveat that it isn't verified against the installed version, or help the user add the missing docset (see below).

5. **Helping set up or extend a docset library:**
   - Confirm which languages/frameworks the user wants offline references for.
   - Explain that docsets are typically obtained through the offline browser's built-in docset manager (a searchable catalog of official docsets to download), or generated from a project's own documentation output for private/internal libraries.
   - Suggest organizing docsets by keeping only the versions actually in active use, since stale duplicate versions make search results ambiguous.

6. **When answering, cite which docset/version supplied the information** (e.g. "per the Python 3.11 docset") so the user can tell offline-verified answers apart from general knowledge, and so they know immediately if they need to update a docset when the installed library version changes.

7. **Flag staleness risk.** If the user's installed library version has changed since the docset was downloaded, note that the docset may be out of date and suggest refreshing it before relying on it for a subtle or version-sensitive question.
