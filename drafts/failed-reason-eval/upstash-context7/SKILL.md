---
name: current-library-docs
description: Verify library/framework API usage against the actual installed version's documentation instead of relying on potentially outdated training knowledge, and use when writing or reviewing code that calls a third-party package, SDK, or framework whose API may have changed since the model's training cutoff.
---

# Current Library Docs

Language models are frequently wrong about library APIs not because they don't
know the library, but because they know an *old* version of it — a function
signature that changed, an option that got renamed, a package that was
deprecated in favor of another. This skill is a discipline for catching that
class of error before it ships as code, by treating the locally installed
version as the source of truth instead of memory.

## When to apply this

Apply this whenever writing, reviewing, or debugging code that calls into a
third-party package, SDK, framework, or CLI tool — especially when:

- The project's dependency manifest (`package.json`, `requirements.txt`,
  `pyproject.toml`, `Gemfile`, `go.mod`, `Cargo.toml`, etc.) pins a specific
  version, and that version could plausibly postdate what was seen during
  training.
- The user reports that generated code doesn't work, throws an "unknown
  argument" / "no such method" error, or behaves differently than expected —
  a classic symptom of stale API knowledge.
- The library is one known for fast-moving or frequently-breaking APIs (web
  frameworks, cloud SDKs, AI/LLM client libraries, build tools).
- You're about to write an import or call for a library you haven't already
  confirmed the version of in this session.

Skip it for standard-library code, well-established APIs that haven't changed
in years, or trivial one-off scripts with no dependency manifest at all.

## Step-by-step guidance

1. **Identify the exact installed version first.** Before writing any call
   into a library, check the project's lockfile or manifest (`package-lock.json`,
   `poetry.lock`, `requirements.txt` with pinned versions, `go.sum`, etc.) or
   run the package manager's own version query (e.g. `pip show <pkg>`,
   `npm list <pkg>`) to get the concrete version in use. Don't assume "latest"
   or "whatever I was trained on."

2. **Prefer documentation shipped with the package over memory.** Installed
   packages frequently carry their own docs locally: docstrings, `.pyi` type
   stubs, TypeScript `.d.ts` files, a `CHANGELOG.md` or `HISTORY.md` in the
   package directory, or a `README` inside `node_modules/<pkg>` /
   `site-packages/<pkg>`. Read these directly — they describe the exact
   version installed, not some other one.

3. **Check type definitions and signatures directly in code.** If the
   language has static types (TypeScript `.d.ts`, Python type stubs, Go
   source), open the actual function/class signature in the installed
   package rather than trusting a remembered signature. This is the single
   most reliable way to catch a renamed parameter or changed return type.

4. **Look for a changelog entry between the version you remember and the
   version installed.** If unsure whether an API changed, scan the package's
   changelog for entries between those two versions — breaking changes are
   usually called out explicitly ("BREAKING:", "deprecated", "removed").

5. **When still uncertain, write a small verification step before relying on
   the API.** For a scripting language, this can be as simple as running
   `help(function)` / `console.log(Object.keys(module))` /
   inspecting the object at a REPL, or writing a minimal smoke-test call and
   running it, before building the full feature on top of an assumed
   signature.

6. **Flag version-sensitive assumptions explicitly to the user.** If no
   version could be confirmed (no lockfile, no local install) and the code
   must be written anyway, say so plainly rather than silently guessing —
   name the specific API surface being assumed so the user can correct it if
   their installed version differs.

7. **After making a change, re-run or re-check the affected code path** to
   confirm the assumed API actually behaves as expected, rather than trusting
   that the fix is correct because it looks plausible.

The underlying goal in every step is the same: reduce reliance on
possibly-stale memorized API knowledge by grounding every non-trivial library
call in something checkable — the installed version's own files, its type
definitions, its changelog, or a quick runtime check — before treating the
code as finished.
