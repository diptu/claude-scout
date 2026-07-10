---
name: openapi-client-generation
description: Guides generating API client libraries, server stubs, and documentation from an OpenAPI/Swagger specification (v2 or v3) using the openapi-generator tool; use when a user has an OpenAPI spec and needs SDKs, server scaffolding, or API docs generated from it.
---

# OpenAPI Client & Server Generation

This skill helps produce API client libraries (SDKs), server stub code, and API documentation automatically from an OpenAPI (Swagger) specification, using the `openapi-generator` CLI/tool ecosystem.

## When to apply this skill

Apply this skill when the user:
- Has an OpenAPI/Swagger spec file (YAML or JSON, v2 or v3) and wants a client SDK generated in a specific language (TypeScript, Python, Go, Java, etc.).
- Wants server-side stub/scaffold code generated from an API spec so they can fill in business logic.
- Wants human-readable API documentation (HTML, Markdown) generated from a spec.
- Is trying to keep a hand-written client in sync with an evolving API spec and wants to regenerate instead of hand-editing.
- Asks how to turn a `.yaml`/`.json` OpenAPI file into working code.

Do not apply this skill for writing an OpenAPI spec from scratch (that's spec authoring, a different task) or for hand-writing a client without a spec — only apply once a spec already exists or is being created as part of the same task.

## Step-by-step guidance

1. **Locate or confirm the spec.** Find the OpenAPI/Swagger definition file in the project (commonly `openapi.yaml`, `openapi.json`, `swagger.yaml`, or under a `docs/`/`api/` directory). Confirm whether it's v2 (Swagger) or v3 — this affects which generator flags and templates apply. If no spec exists yet, tell the user one is required first.

2. **Validate the spec before generating anything.** Check for obvious structural problems: missing `info`, unresolved `$ref` pointers, inconsistent path parameters, missing response schemas. Generating from a broken spec produces broken or nonsensical code, so surface spec issues rather than silently generating around them.

3. **Confirm the target generator and output kind** with the user if ambiguous:
   - Client SDK (pick the target language/framework, e.g. `typescript-axios`, `python`, `go`, `java-okhttp`).
   - Server stub (pick the framework, e.g. `spring`, `express`, `fastapi`, `nodejs-express-server`).
   - Documentation only (e.g. `html2`, `markdown`).

4. **Determine invocation approach.** `openapi-generator` is typically run via its CLI (`openapi-generator-cli generate -i <spec> -g <generator> -o <output-dir>`), a Docker image, or a build-tool plugin (Maven/Gradle/npm). Prefer whatever the project already uses (check for existing config like `openapitools.json`, a Maven/Gradle plugin block, or an npm script) rather than introducing a new toolchain. If nothing exists yet, the CLI invocation is the simplest starting point.

5. **Use configuration options to shape the output** rather than manually editing generated code afterward:
   - Package/module name, namespace, and version via generator-specific config properties (e.g. `packageName`, `npmName`, `groupId`).
   - Enable/disable features like validation, auth handling, or async support if the generator supports it.
   - Use an `openapitools.json` or a generator config YAML/JSON file to keep the invocation reproducible and versioned in the repo, instead of a one-off command line only the user remembers.

6. **Never hand-edit generated output.** Generated client/server code is meant to be regenerated whenever the spec changes. If custom logic is needed, use the generator's supported extension points (templates, mustache overrides, or a wrapper module outside the generated directory) rather than editing generated files directly — direct edits get silently clobbered on the next regeneration.

7. **Re-generate on spec changes.** When the user updates the OpenAPI spec, regenerate the client/server/docs rather than manually patching the existing generated code, and diff the result to catch breaking changes (removed endpoints, changed types, renamed fields) before they reach consumers.

8. **Surface generator warnings.** Generation tools commonly print warnings about unsupported spec features, unresolvable schemas, or naming collisions — treat these as signals of spec problems worth relaying back to the user, not noise to suppress.
