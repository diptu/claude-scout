---
name: api-docs-lookup
description: Quickly locate and summarize API/library documentation for a given language, framework, or package by consulting official docs, changelogs, and reference pages, mirroring how DevDocs aggregates and searches multi-language API documentation; use when the user needs accurate, current API signatures, method behavior, configuration options, or usage examples for a specific library or platform.

## Purpose

This skill helps Claude answer "how do I use X in library/framework Y" questions accurately, the way a fast offline API documentation browser (like DevDocs) would: by going straight to the authoritative reference for the relevant language or package, extracting the precise signature/behavior, and presenting it concisely with a working example — instead of relying on possibly-stale training knowledge or guessing at method names and parameters.

## When to apply this skill

Apply this skill whenever the user:
- Asks how to use a specific function, class, method, CLI flag, or configuration option in a named library, framework, or language standard library.
- Reports an error that looks like a misuse of an API (wrong argument count, deprecated method, unknown property) and needs the correct current usage.
- Asks to compare behavior or signatures across versions of a library.
- Wants a quick reference summary for a package they're integrating (e.g. "what are the options for `useEffect`" or "what does `fetch`'s `init` object support").
- Is working with an unfamiliar or fast-moving API surface (frontend frameworks, cloud SDKs, CLI tools) where getting the exact syntax right matters more than general explanation.

Do not apply this skill for open-ended conceptual questions ("what is REST") or when the user already has the exact syntax and just wants help debugging their own logic.

## Step-by-step guidance

1. **Identify the exact target**: pin down the language/framework/package name and, if relevant, its version, before searching or answering. If the user didn't specify a version, check the project's dependency file (`package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, etc.) if one is available in the working directory, so the answer matches what they actually have installed.

2. **Prefer the authoritative source**: for the identified package, mentally (or via available tools) prioritize the project's official reference documentation over blog posts, forum answers, or general knowledge. If web search or fetch tools are available, use them to pull the current official docs page rather than answering purely from memory, especially for APIs known to change frequently (frontend frameworks, cloud provider SDKs, CLI tools).

3. **Extract precisely, don't paraphrase loosely**: report the exact function/method signature (parameter names, types, defaults, required vs optional), not an approximation. If the API takes an options object, list the actual option keys and what each does.

4. **Note version-specific behavior**: if the API differs across versions (renamed, deprecated, changed defaults), say so explicitly and state which version the answer applies to, rather than presenting one version's behavior as universal.

5. **Give a minimal working example**: after stating the signature/behavior, show a short, runnable usage example in the same language, using realistic values rather than placeholder names like `foo`/`bar` where possible.

6. **Flag deprecation or better alternatives**: if the API the user asked about is deprecated or superseded, say so and point to the current recommended replacement, rather than only answering the literal question asked.

7. **Be explicit about uncertainty**: if authoritative documentation isn't available (no web access, obscure/internal library) and the answer relies on training knowledge that may be stale, say so plainly rather than presenting a guess as verified fact.

8. **Keep answers scoped**: answer the specific API question asked; don't dump the entire reference page. Link the user toward the specific relevant section conceptually (e.g. "this is documented under the `Response` object's `headers` property") rather than reproducing unrelated parts of the docs.
