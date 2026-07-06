---
name: karpathy-coding-discipline
description: Applies a set of anti-slop coding habits — minimal diffs, no speculative abstraction, no defensive bloat — whenever writing or modifying code in an existing codebase.

---

# Karpathy-Style Coding Discipline

This skill counteracts the most common failure modes of LLM-assisted coding: over-engineering, defensive bloat, scope creep, and code that ignores the conventions of the codebase it lands in. Apply it whenever writing new code, modifying existing code, or reviewing a diff you just produced — especially in an established codebase where changes should blend in rather than stand out.

## When to apply

- Any time you are about to write or edit code in a project that already has source files.
- Before presenting a diff, as a final self-review pass.
- When a request is small ("fix this bug", "add this flag") and the temptation is to also refactor, restructure, or "improve" surrounding code.

## Core principles

1. **The best code is the least code.** Every line you add is a line someone must read, review, and maintain. Prefer the smallest change that correctly solves the stated problem.
2. **Solve the problem that was asked, not the problem you imagine.** Do not add features, options, configurability, or generality that the request did not call for.
3. **Match the codebase, don't impose on it.** Existing style, naming, error-handling idioms, and comment density win over your defaults.
4. **Don't guess APIs.** If you are not certain a function, parameter, or library behavior exists, check the actual code or documentation before using it.

## Step-by-step guidance

### Before writing code

1. Read the surrounding code first. Note its naming conventions, error-handling style, comment density, and how similar problems are already solved in this codebase.
2. Restate the task to yourself in one sentence. If your planned change does more than that sentence, cut the extra.
3. Look for an existing function, helper, or pattern that already does part of the job. Reuse beats reimplementation.

### While writing code

4. **No speculative abstraction.** Do not introduce a base class, interface, plugin system, or config option for a second use case that does not exist yet. Two concrete duplicated implementations are cheaper than one premature abstraction; abstract at the third occurrence, not the second.
5. **No defensive bloat.** Do not wrap code in try/except (or try/catch) unless there is a specific, expected failure with a specific, correct recovery. Letting an unexpected error propagate loudly is better than swallowing it or returning a silent fallback value that hides the bug.
6. **No dead-weight ceremony.** Skip getters/setters that do nothing, wrapper functions that only call one other function, type gymnastics that add no safety, and "manager"/"factory"/"handler" layers with a single caller.
7. **No fallback chains.** Avoid patterns like "try A, and if that fails try B, and if that fails return a default" unless each branch is genuinely required. Fallbacks mask failures and make debugging miserable.
8. **Comments explain *why*, not *what*.** Do not narrate the code ("increment the counter"). Do not leave comments addressed to the reviewer ("changed this to fix the bug"). Only comment constraints and reasons the code cannot express itself.
9. **Keep names boring and local conventions intact.** If the codebase uses `snake_case` and short names, do not introduce `camelCase` or verbose Java-style names.

### After writing code — the self-review pass

10. Reread your full diff and ask, for each hunk: "Did the task require this?" Delete every hunk where the answer is no — drive-by reformatting, import reordering, renamed variables, and "while I was here" refactors all count as no.
11. Check for leftover scaffolding: debug prints, commented-out code, unused imports, unused variables, placeholder text.
12. Ask: "Could this be half the length and still correct?" If yes, shorten it. Fewer branches, fewer parameters, fewer files touched.
13. Verify every API call you were not 100% sure about against the real source or docs — do not ship a plausible-sounding method name.
14. Confirm the change actually runs or is exercised by a test. Code that has never been executed should be labeled as such, not presented as done.

## Common failure smells to catch

- A "small fix" diff that touches five files.
- A new `utils.py` / `helpers.ts` created to hold one function.
- An error handler whose body is `pass`, a bare log line, or `return None`.
- A config option with exactly one value ever used.
- A docstring longer than the function it documents.
- Code that handles inputs the caller can never produce.

## The one-sentence test

Before finalizing any change, state in one sentence what it does and why it was needed. If you cannot, the change is doing too much — split it or shrink it.
