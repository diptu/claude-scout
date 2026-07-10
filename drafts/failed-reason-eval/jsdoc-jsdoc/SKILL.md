---
name: jsdoc-documentation
description: Writes and maintains JSDoc comments for JavaScript/TypeScript code, and helps configure or troubleshoot JSDoc-based API documentation generation; use when annotating functions/classes with JSDoc tags or setting up a JSDoc documentation build.
---

# JSDoc Documentation

This skill helps write correct, complete JSDoc comments for JavaScript and TypeScript code, and helps set up or debug a JSDoc-based documentation generation pipeline (the kind produced by tools like the `jsdoc` CLI).

## When to apply this skill

- The user asks to "document this function/class/module" in a JS/TS codebase.
- Existing code has missing, incomplete, or outdated JSDoc comments.
- The user wants to generate an HTML API reference site from source comments.
- The user is configuring a `jsdoc.json`/`.jsdoc.json` config file, a `package.json` doc script, or troubleshooting why generated docs look wrong or incomplete.
- The user asks about JSDoc tag syntax (`@param`, `@returns`, `@typedef`, etc.) or how TypeScript types interact with JSDoc.

## Writing JSDoc comments

When annotating code, follow these steps:

1. **Identify the unit being documented** — function, class, method, constructor, module, or typedef — and place the comment block immediately above it, opened with `/**` and closed with `*/`.
2. **Write a one-line summary first.** The first sentence should stand alone and describe what the thing does, in imperative or descriptive form (e.g. "Parses a duration string into milliseconds.").
3. **Document every parameter** with `@param {Type} name - description`. For optional parameters use `@param {Type} [name]`, and for defaults use `@param {Type} [name=default]`. Destructured parameters should be documented as `@param {Object} options` followed by `@param {string} options.foo` for each property actually used.
4. **Document the return value** with `@returns {Type} description`. Omit `@returns` entirely for functions that return nothing (don't write `@returns {void}` unless the codebase already uses that convention consistently).
5. **Document thrown errors** with `@throws {ErrorType} description` when the function can throw in a way callers should anticipate.
6. **Add `@example` blocks** for non-obvious usage, especially for public/exported APIs, showing a realistic call and its result.
7. **Use structural tags where appropriate**:
   - `@class` / `@constructor` for constructor functions.
   - `@extends`/`@augments` for inheritance.
   - `@typedef {Object} Name` plus `@property` entries for shared object shapes, so they can be reused across multiple `@param`/`@returns` tags via `{Name}`.
   - `@module` at the top of a file to name it as a module, and `@private`/`@public`/`@protected` to mark visibility.
   - `@deprecated` with a short reason and, if applicable, the replacement API.
8. **Keep types accurate and specific.** Prefer `{string[]}` over `{Array}`, `{Object<string, number>}` over `{Object}`, and union types `{string|number}` when a parameter genuinely accepts multiple types. If the project is TypeScript, prefer relying on the actual type annotations and keep JSDoc prose-only (no redundant `{Type}` tags) unless the project's tooling (e.g. a `.js` file with `// @ts-check`) actually reads JSDoc types for type-checking — in that case keep the types precise, since they're load-bearing.
9. **Match existing style.** Before writing new comments, look at a few existing documented functions in the same file or repo to match tag ordering, indentation, and verbosity conventions already in use.
10. **Don't over-document.** Trivial one-line getters/setters or self-explanatory private helpers don't need a full tag block — a short summary line is enough, or nothing at all if the name is already unambiguous.

## Setting up or troubleshooting JSDoc generation

When the user wants to generate documentation output (not just write comments):

1. Check for an existing JSDoc config file (commonly `jsdoc.json`, `.jsdoc.json`, or a `"jsdoc"` key in `package.json`). If none exists, propose a minimal config specifying `source.include` (the directories/files to scan), `source.exclude` (e.g. `node_modules`, test files), and `opts.destination` (the output directory for generated HTML).
2. Confirm there's a way to invoke generation — typically a `jsdoc` CLI installed as a dev dependency and a corresponding `package.json` script (e.g. `"docs": "jsdoc -c jsdoc.json"`).
3. If documentation output looks wrong (missing members, broken links, wrong grouping), the most common causes are: a symbol not being exported/reachable from an included file, a missing or mismatched `@module`/`@memberof` tag causing misattachment, or the config's `source.include` not covering the file at all. Diagnose by checking which of these applies before suggesting larger config changes.
4. If the project uses a custom template or theme, note that it typically lives in `opts.template` in the config — check there before assuming a rendering bug is in the JSDoc comments themselves.
5. Keep the config and generation approach minimal: don't introduce a documentation build pipeline more complex than the project needs (e.g. don't add versioning, search plugins, or custom templates unless asked).
