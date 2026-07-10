---
name: current-docs-lookup
description: Use when a user asks how to use a library, framework, or API and correct usage depends on the current version rather than what was memorized during training — guides Claude to verify against up-to-date documentation instead of guessing from stale training data.
---

# Current Docs Lookup

Library and framework APIs change constantly: functions get renamed, deprecated, or replaced; default behaviors shift between major versions; new idiomatic patterns replace old ones. Training data has a cutoff, so recalled usage for a fast-moving package (a JS framework, a Python ML library, a cloud SDK, etc.) may be stale, deprecated, or simply wrong for the version the user is actually running. This skill applies whenever code correctness depends on "what does this library's API look like right now," not on general programming knowledge.

## When to apply this

Apply this skill when:
- The user asks "how do I do X with library Y" and Y is a third-party package, framework, or API (not a language built-in).
- Code the user pastes calls a library function and something looks off, outdated, or uncertain.
- Claude is about to write new code against an SDK, framework, or API and isn't fully confident the remembered method signatures, import paths, or config keys are current.
- The user explicitly says a library's behavior differs from what Claude just produced (a strong signal that memorized knowledge is stale).

Do not apply it for standard library features of well-established languages, general algorithms, or anything where the answer hasn't meaningfully changed in years (basic string manipulation, list comprehensions, etc.) — verifying those adds no value.

## Step-by-step guidance

1. **Name the version, not just the library.** Before answering, check the project's manifest (`package.json`, `requirements.txt`, `pyproject.toml`, `Gemfile`, `go.mod`, etc.) or ask the user which major version they're on. API answers are version-specific; "how do I use X" without a version is an incomplete question.

2. **Check the repo first.** Before trusting memorized API shape, look for evidence already present locally:
   - Search `node_modules/<pkg>`, the installed Python package's source, or vendored source for the actual current function signatures, exported types, and docstrings.
   - Grep the codebase for existing working usages of the same library — these are ground truth for this exact version, more reliable than memory.
   - Check for a `CHANGELOG.md`, `MIGRATION.md`, or `UPGRADING.md` in the package's own installed files, which often lists exactly what changed between versions.

3. **When local evidence is insufficient**, and the user has given permission to browse or fetch external resources, prefer the library's own official documentation site or repository over general web search results, and prefer a page/version selector matching the user's installed version over the latest docs.

4. **Flag uncertainty explicitly rather than guessing confidently.** If Claude cannot verify current API shape through the repo or through a permitted fetch, say so plainly: state which parts of the answer are based on possibly-stale training knowledge, and suggest the user double-check the specific function/class names against the library's changelog or docs before relying on the code.

5. **Prefer minimal, verifiable claims.** When writing example code against an unfamiliar or fast-moving API, favor patterns that can be checked against the installed package's actual exports (e.g., import the module and inspect it, or read its type definitions) over reproducing a remembered code snippet verbatim.

6. **After verifying, note the source.** When an answer relied on checking installed package source, a changelog, or fetched docs rather than memory, mention that briefly so the user knows the claim was verified rather than recalled — this distinction matters most right after a major version bump.
