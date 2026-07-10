---
name: openapi-doc-authoring
description: Author, review, and refine OpenAPI/Swagger specification files so they render into clear, complete API reference documentation; use when a user asks to write, fix, or improve an OpenAPI spec, generate API docs from an existing spec, or diagnose why generated API reference docs look incomplete or poorly organized.
---

# OpenAPI Doc Authoring

This skill helps produce OpenAPI (Swagger) specification files that generate clean, navigable API reference documentation — the kind of output tools like Redoc render from a spec. It applies whenever the task involves writing a new OpenAPI/Swagger YAML or JSON file, editing an existing one, or reviewing generated API documentation for gaps caused by an underspecified schema.

## When to apply

- The user asks to document a REST API and mentions OpenAPI, Swagger, or "API reference docs."
- A repository contains an `openapi.yaml`, `openapi.json`, `swagger.yaml`, or similar spec file that needs edits or additions.
- Generated API documentation (from any renderer) looks sparse, missing examples, or has poorly described endpoints — the root cause is almost always the underlying spec, not the renderer.
- The user wants to add a new endpoint, request/response schema, or authentication scheme to an existing API and have it show up correctly in generated docs.

## Step-by-step guidance

1. **Locate or create the spec file.** Look for `openapi.yaml`, `openapi.json`, `swagger.yaml`, or a similarly named file at the repo root, in `docs/`, or in `api/`. If none exists and the user wants one created, start from the minimal required structure: `openapi` version string, `info` block, `paths`, and `components`.

2. **Fill in the `info` block completely.** Every spec needs `title`, `version`, and `description`. A good `description` uses Markdown and briefly explains what the API does, since this text becomes the landing content of the generated reference page.

3. **Model each endpoint under `paths` with full detail, not just the shape.** For every operation (`get`, `post`, etc.):
   - Write a concise `summary` (shows in navigation) and a longer `description` (shows in the body).
   - Declare `operationId` so tooling and cross-references stay stable.
   - Define every parameter (`path`, `query`, `header`) with `description`, `required`, and a `schema`.
   - Define `requestBody` and every response status code under `responses`, each with its own `description` and `content` schema — don't only document the 200 case; error responses matter for a complete reference.

4. **Push reusable shapes into `components/schemas` and reference them.** Duplicate inline schemas across endpoints produce inconsistent-looking docs and are harder to maintain. Define a schema once under `components.schemas`, then use `$ref` everywhere it's reused, including for common error-response bodies.

5. **Add realistic examples.** Use `example` or `examples` on schemas, parameters, and responses. Generated reference docs lean heavily on examples to make an endpoint understandable at a glance — a schema without an example is much less useful to a reader than one with a realistic sample payload.

6. **Document authentication under `components/securitySchemes` and apply it via `security`.** State clearly whether auth is API-key, bearer token, OAuth2, etc., and which endpoints require it versus which are public.

7. **Group related endpoints with `tags`.** Add a top-level `tags` array with a `name` and `description` for each logical grouping (e.g., "Users", "Orders"), and tag each operation accordingly. This becomes the sidebar/navigation structure in generated docs, so a spec with no tags tends to produce a flat, hard-to-scan reference.

8. **Validate structurally before calling it done.** Check that every `$ref` resolves, every path parameter listed in the URL template has a matching `parameters` entry, and required fields (`openapi`, `info.title`, `info.version`, at least one path) are present. Inconsistencies here are the most common cause of broken or missing sections in rendered documentation.

9. **When reviewing existing docs that look incomplete**, trace the gap back to the spec first: a missing description in the docs means a missing `description` field in the spec, not a renderer bug. Fix the spec, then regenerate.

10. **Keep the spec as the single source of truth.** Avoid hand-editing generated HTML/static doc output — any fix belongs in the OpenAPI file itself so it persists across regenerations.
