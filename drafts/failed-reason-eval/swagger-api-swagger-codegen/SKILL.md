---
name: openapi-codegen-guide
description: Guides Claude through generating API clients, server stubs, and documentation from an OpenAPI/Swagger definition, including choosing a generation strategy and validating the spec first — use when a user has an OpenAPI/Swagger spec and wants client SDKs, server scaffolding, or API docs produced from it.
---

# OpenAPI/Swagger Code Generation Guide

This skill helps produce API clients, server stubs, and documentation from an OpenAPI (formerly Swagger) definition file. Apply it whenever a user has (or wants to create) an `openapi.yaml`/`openapi.json`/`swagger.json` spec and asks for generated code, SDKs, server scaffolding, or API reference docs derived from that spec.

## When to use this skill

- The user has an OpenAPI/Swagger definition and wants a client library generated for a specific language (Python, TypeScript, Java, Go, etc.).
- The user wants server-side route stubs or controller interfaces scaffolded from an API contract.
- The user wants human-readable API documentation generated from a spec.
- The user is designing a new API and wants help writing an OpenAPI definition that will later drive code generation.
- The user reports generated code that's out of sync with their spec and wants it regenerated or reconciled.

## Step-by-step guidance

### 1. Locate and validate the spec

- Find the OpenAPI/Swagger definition file in the project (commonly `openapi.yaml`, `openapi.json`, `swagger.yaml`, or under a `spec/`, `api/`, or `docs/` directory).
- Confirm the spec version (`swagger: "2.0"` vs `openapi: "3.x"`) — generation strategy and available fields differ between them. If asked to generate code and no spec exists yet, offer to draft one from the user's description before generating anything downstream.
- Check the spec is structurally valid: required top-level keys (`openapi`/`swagger`, `info`, `paths`), that every path operation has a unique `operationId`, and that referenced `$ref` schemas resolve within the document. Flag missing `operationId`s specifically — generators use them to name methods/functions, and without them tools fall back to auto-generated, often unreadable names.

### 2. Clarify the generation target

Before generating anything, confirm with the user (or infer from project context):

- **Output type**: API client SDK, server stub/scaffold, or documentation only.
- **Target language/framework**: e.g. TypeScript+fetch, Python+requests, Java+Spring, Go. Server stubs additionally need a target framework (Express, Flask, Spring Boot, etc.).
- **Output location**: where generated code should live in the project (a dedicated `generated/` or `client/` directory is preferable to mixing generated and hand-written code).
- **Regeneration expectations**: whether this is a one-time generation or something the user will re-run whenever the spec changes (affects whether to keep generated code untouched vs. wrap it so hand-edits survive regeneration).

### 3. Design the generated code structure

Regardless of target language, structure generated output so it separates concerns cleanly:

- **Models/schemas**: one type/class per schema definition in `components/schemas` (OpenAPI 3) or `definitions` (Swagger 2), matching field names, types, required/optional status, and enum values exactly as declared.
- **Operations/methods**: one method per path+HTTP-method operation, named from its `operationId`, with parameters split into path, query, header, and body per the spec, and a return type derived from the operation's success response schema.
- **Client/server plumbing**: shared code for auth (from `securitySchemes`), base URL/server config (from the spec's `servers` block), and error handling for non-2xx responses — write this once and have generated operations call into it, rather than duplicating request/response boilerplate per method.
- For server stubs, generate the routing/controller skeleton with method signatures and status codes matching the spec, leaving business logic as clearly marked stubs (e.g. a `NotImplementedError`/`TODO`-style stub the user fills in) rather than guessing at implementation.

### 4. Keep documentation in sync

If the user wants documentation:

- Derive a human-readable reference page (or docstrings/comments in generated code) directly from each operation's `summary`, `description`, and parameter/response descriptions in the spec — don't invent descriptions the spec doesn't provide.
- Group operations by their `tags` if the spec defines them, matching how the API's authors intended it to be navigated.
- Include example requests/responses only where the spec provides `example`/`examples` values; don't fabricate example payloads.

### 5. Validate the output

After generating code:

- Confirm every operation in the spec has a corresponding generated method/route — cross-check the operation count against generated output rather than spot-checking a few.
- Confirm generated model fields match the spec's required/optional and type constraints (don't silently make a required field optional or vice versa).
- If the target language has a compiler/type-checker/linter available in the project, run it against the generated code and fix any errors before considering the generation complete.
- Point out to the user any spec ambiguities encountered during generation (e.g. a schema using `oneOf`/`anyOf` that the target language can't cleanly represent, or a missing response schema for an operation) rather than silently picking an interpretation.

### 6. Handle spec changes over time

If the user later updates the OpenAPI spec and asks to regenerate:

- Diff the new spec against the previous version's operations and schemas to identify what changed (added/removed/renamed operations, changed parameter or field types).
- Regenerate only the affected generated files where possible, and flag any changes that would break existing callers of the generated client (removed operations, newly-required parameters, changed response shapes) so the user can assess impact before merging.
