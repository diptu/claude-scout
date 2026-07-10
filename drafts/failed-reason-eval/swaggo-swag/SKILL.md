---
name: go-swagger-docs
description: Generates and maintains Swagger 2.0 / OpenAPI documentation for Go REST APIs by writing swag-style annotation comments above handler functions and structuring the docs generation workflow; use when a user is building a Go HTTP API and wants discoverable, auto-generated API documentation.
---

# Go Swagger API Documentation

This skill helps produce Swagger 2.0 (OpenAPI) documentation for Go REST APIs using the annotation-comment convention popularized by the `swag` toolchain (declarative comments above handlers that a generator turns into a `swagger.json`/`swagger.yaml` spec plus a `docs.go` file).

## When to apply this skill

Apply this skill when:
- A user is writing or modifying HTTP handlers in a Go web service (using `net/http`, Gin, Echo, Fiber, Chi, or similar) and wants API documentation.
- A user asks to "document this endpoint," "add Swagger docs," "generate OpenAPI spec," or mentions `swag init` / `swaggo`.
- A user wants a machine-readable API contract for a Go service so frontend consumers, API gateways, or Swagger UI can use it.
- A user is reviewing a Go API for missing or stale documentation and wants annotations added or corrected.

## Core concept: annotation comments

Documentation is expressed as structured comments directly above each handler function, using `@`-prefixed tags. Claude should treat each handler as needing two documentation layers:

1. **General API info** — a single block of comments (typically above `main()` or a dedicated `docs.go`) describing the whole API: title, version, base path, host, license, contact.
2. **Per-endpoint annotations** — a comment block directly above each handler function describing that one operation.

## Step-by-step guidance

1. **Locate the API entry point.** Find where the HTTP server/router is initialized (commonly `main.go` or a `cmd/` directory). Confirm whether general API info comments already exist above `main()`; if not, propose adding them with these tags:
   - `@title` — API name
   - `@version` — API version (e.g., `1.0`)
   - `@description` — short summary of the API's purpose
   - `@host` — host:port (e.g., `localhost:8080`)
   - `@BasePath` — base path prefix (e.g., `/api/v1`)

2. **Identify handler functions.** Locate the functions bound to routes (look for router registration calls like `router.GET(...)`, `mux.HandleFunc(...)`, `e.POST(...)`). For each handler that lacks documentation, or has stale documentation relative to its current signature, write an annotation block directly above the function.

3. **Write per-endpoint annotations** using these tags, matching the handler's actual behavior — never invent parameters, responses, or descriptions that aren't reflected in the code:
   - `@Summary` — one-line description of what the endpoint does
   - `@Description` — longer explanation if the summary isn't self-explanatory
   - `@Tags` — a grouping name (e.g., the resource name: `users`, `orders`)
   - `@Accept` — request content type (e.g., `json`)
   - `@Produce` — response content type (e.g., `json`)
   - `@Param` — one line per parameter: `name location type required "description"` (location is one of `path`, `query`, `header`, `body`, `formData`)
   - `@Success` — one line per success response: `code {type} model "description"`
   - `@Failure` — one line per error response: `code {type} model "description"`
   - `@Router` — the route path and HTTP method: `/path/to/resource [get]`

4. **Reflect real types, not placeholders.** For `@Param` and `@Success`/`@Failure` model references, use the actual Go struct names used in the handler's request binding and response encoding (e.g., `models.User`, `dto.CreateOrderRequest`). If a handler returns a raw map or an anonymous struct, note that inline documentation of fields may be needed, or suggest introducing a named struct for clarity — but only if the user wants that refactor, not as an unsolicited addition.

5. **Keep annotations synchronized with code.** When a user changes a handler's parameters, request body, or response shape, check whether the existing annotation comment above it needs updating to match. Treat annotation drift (docs describing behavior the code no longer has) as a bug to flag, not just a formatting nicety.

6. **Explain the generation step conceptually.** After writing annotations, tell the user that a generator command (conventionally run via a Makefile target or `go generate` directive) needs to be run to turn the comments into the actual spec files (`docs/swagger.json`, `docs/swagger.yaml`, `docs/docs.go`) — but let the user's own build tooling (or a Makefile target, per this repo's convention of centralizing commands) invoke it rather than running arbitrary generator binaries directly.

7. **Note common pitfalls** when reviewing existing annotations:
   - Missing `@Router` line (the most common cause of an endpoint silently not appearing in the generated spec).
   - Mismatched HTTP method in `@Router` vs. the actual route registration.
   - `@Param` entries for path parameters that don't match the route's actual path placeholders.
   - Comment block not directly adjacent to the function it documents (blank lines between them break the association in most generators).

## Output style

When adding or editing annotations, output them as ordinary Go comments (`//`) directly above the function signature, matching the surrounding file's existing comment style and indentation. Do not restructure unrelated code, and do not add documentation for endpoints the user didn't ask about unless they're clearly incomplete counterparts of ones just documented (e.g., documenting `POST /users` but leaving `GET /users` unannotated in the same file).
