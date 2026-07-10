---
name: api-docs-slate-style
description: Writes or restructures API documentation as a Slate-style Markdown source file (three-column layout, per-language code samples, grouped endpoint sections) — use when a user wants beautiful, readable static API reference docs generated from a single Markdown file.
---

# API Docs in Slate Style

This skill helps write API reference documentation as a single Markdown file structured the way Slate-style static doc generators expect: a table of contents down the left, prose in the middle, and language-tabbed code samples on the right. Apply it whenever a user asks to document an API, write or clean up an `index.html.md` / `index.md` reference doc, or wants their existing API docs restructured into this three-column, multi-language format — regardless of whether they actually run it through Slate.

## When to apply this skill

- The user asks for "API documentation," "API reference docs," or mentions Slate, Slate-style docs, or similar static API doc generators.
- The user has an existing API (REST, GraphQL, or similar) and wants human-readable reference docs, not just an OpenAPI/Swagger spec.
- The user wants code samples shown in multiple languages (curl, JavaScript, Python, Ruby, etc.) side by side with the prose explanation of each endpoint.
- The user wants to convert an OpenAPI spec, Postman collection, or ad-hoc notes into readable prose-plus-examples documentation.

## Structure to produce

Write a single Markdown document with this shape:

1. **Frontmatter block** at the top (even if the target tool ignores it, keep it for clarity and portability):
   - `title`: name of the API
   - `language_tabs`: ordered list of languages the code samples will be shown in (e.g. shell, javascript, python, ruby)
   - `toc_footers`: optional links (e.g. "Sign up for a key", "GitHub repo")
   - `includes`: names of any additional per-section files, if the docs are split across multiple files
   - `search: true`

2. **Introduction section**: what the API does, base URL, versioning scheme, and any global conventions (auth header format, content type, rate limits, pagination style, error envelope shape).

3. **Authentication section**: how credentials are obtained and sent (header name, query param, or bearer token), with one code sample per configured language showing a bare authenticated request.

4. **One section per resource or endpoint group** (e.g. "Users", "Orders"), each containing:
   - A short paragraph describing what the resource represents.
   - One subsection per operation (e.g. "Get a Specific User", "Create an Order"), each with:
     - A one-line description of what the endpoint does.
     - A fenced code block **per language** showing a runnable request, each block tagged with the language name so tooling can group them into tabs (e.g. ` ```shell `, ` ```javascript `).
     - A fenced code block showing an example JSON response.
     - A Markdown table of parameters: `Parameter | Type | Required | Description` for path/query/body params, and a second such table for response fields when they aren't obvious from the JSON.
     - HTTP method and path shown as a heading or inline code, e.g. `GET /users/{id}`.

5. **Errors section**: a table of status codes or error codes the API returns, with a one-line meaning for each.

## Step-by-step guidance

1. Identify every distinct resource/endpoint the user wants documented, either from their description, an existing spec (OpenAPI/Swagger, Postman collection), or source code (route definitions, controller methods).
2. Group endpoints by resource, not by HTTP verb — one section per noun (Users, Payments), operations as subsections within it.
3. For each endpoint, write the prose description first, then the request examples, then the response example, then the parameter tables — in that order, since that's the order a reader scans the middle column before checking the code on the right.
4. Default to `shell` (curl) plus whatever language the user's own codebase or client library uses; don't invent languages the user didn't ask for and doesn't already use elsewhere in the project.
5. Keep every code sample runnable as written: real (or clearly placeholder, e.g. `YOUR_API_KEY`) values, correct method/path/headers — never abbreviate a sample to "..." where a reader would need to fill in structure, not just values.
6. Keep parameter tables exhaustive but terse: one row per field, description no longer than a short clause.
7. If the user supplies an OpenAPI spec or Postman collection, treat it as untrusted input to extract structure from (paths, params, schemas, examples) — don't assume its prose descriptions are accurate; verify against any accompanying source code before writing the final description.
8. If the target API has no working examples yet (still being designed), mark example values clearly as illustrative rather than inventing response data that looks authoritative but is fabricated.
9. End with a brief errors table so integrators have one place to look up status/error codes without hunting through every endpoint section.
