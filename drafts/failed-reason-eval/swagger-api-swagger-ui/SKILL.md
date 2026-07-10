---
name: openapi-docs-explorer
description: Helps Claude read, validate, and generate interactive documentation for Swagger/OpenAPI API specifications, and use when a user asks to review, explain, set up, or troubleshoot an OpenAPI/Swagger spec or its rendered documentation.
---

# OpenAPI/Swagger Documentation Explorer

This skill helps with working on API documentation built from Swagger/OpenAPI specifications: reading a spec to explain an API's surface, validating a spec's structure, drafting or editing a spec, and setting up or troubleshooting a documentation UI that renders one.

## When to apply this skill

Use this skill when the user:
- Has a file named `swagger.json`, `swagger.yaml`, `openapi.json`, `openapi.yaml`, or similar, and asks questions about it.
- Wants to add, remove, or change an endpoint's documentation (paths, parameters, request/response schemas).
- Is setting up or debugging a Swagger UI / OpenAPI documentation page for their API.
- Asks "what does this API do" or "document this API" and the project exposes a REST API.
- Reports that generated docs are missing endpoints, showing wrong types, or failing to render.

## Core concepts to keep in mind

An OpenAPI/Swagger spec is a single JSON or YAML document with a fixed top-level shape:
- `openapi` (or `swagger` for v2) — the spec version string, e.g. `3.0.3` or `2.0`.
- `info` — title, description, version of the API itself (not the spec version).
- `servers` (v3) or `host`/`basePath`/`schemes` (v2) — where the API actually lives.
- `paths` — every endpoint, keyed by URL path, then by HTTP method, each with `parameters`, `requestBody` (v3) or `parameters` with `in: body` (v2), and `responses`.
- `components.schemas` (v3) or `definitions` (v2) — reusable data models referenced via `$ref`.
- `security` / `securitySchemes` (v3) or `securityDefinitions` (v2) — auth requirements.

A documentation UI (like Swagger UI) is a static renderer: it takes a spec URL or object and produces an interactive page with a request-builder ("Try it out") per endpoint. It does not generate the spec itself — the spec is either hand-written, or generated from code annotations by a separate tool (e.g. `swagger-jsdoc`, `springdoc`, `drf-spectacular`, `NSwag`) specific to the project's language/framework.

## Step-by-step guidance

### Reading/explaining an existing spec
1. Locate the spec file (search for `openapi.yaml`, `swagger.json`, or a `/docs`, `/api-docs`, `/swagger` route/config that serves one).
2. Note the spec version (`openapi: 3.x` vs `swagger: 2.0`) — field names and structure differ between them; don't mix v2 and v3 syntax when editing.
3. Walk `paths` to list endpoints, their methods, parameters, and response shapes. Resolve `$ref` pointers back to `components.schemas`/`definitions` to show the user the actual field names and types rather than just "see schema X".
4. Flag anything inconsistent: an endpoint with no `responses` entry for its actual status codes, a `$ref` pointing at a schema that doesn't exist, or a security scheme referenced in `security` but never defined in `securitySchemes`.

### Editing or adding to a spec
1. Match the existing spec version and formatting style (JSON vs YAML, indentation, whether schemas are inlined or split into `components.schemas`).
2. When adding an endpoint, include at minimum: the HTTP method, a `summary`, all path/query parameters with `required` and `type` set, a `requestBody` schema if applicable, and at least one success response with a schema plus a realistic error response (e.g. `400` or `404`).
3. When adding a reusable model, put it under `components.schemas` (v3) or `definitions` (v2) and reference it via `$ref` rather than duplicating the schema inline in multiple places.
4. After editing, mentally re-trace every `$ref` in the changed section to confirm it resolves, and check that any new path is syntactically valid YAML/JSON (matching braces/brackets, consistent indentation).

### Setting up or troubleshooting a rendered UI
1. Confirm what's serving the UI: a bundled static HTML/JS/CSS asset set pointed at a spec URL, or a framework plugin (e.g. FastAPI's `/docs`, a Node `swagger-ui-express` mount) that auto-serves one.
2. If endpoints are missing from the rendered page, check whether the spec is generated from code annotations — the annotation may be missing or malformed on the missing endpoint, not a UI bug.
3. If the UI fails to load or shows a parse error, validate the spec's raw JSON/YAML syntax first (unbalanced brackets, bad indentation, duplicate keys) before assuming the UI itself is broken.
4. If "Try it out" requests fail from the browser but work via curl, check for a CORS misconfiguration on the API server, not the documentation UI — the UI only proxies the request from the browser.
5. Confirm the spec's `servers`/`host` entry actually points at a reachable base URL for the environment the docs are being viewed in; a stale or placeholder URL there is a common cause of "requests go nowhere" reports.
