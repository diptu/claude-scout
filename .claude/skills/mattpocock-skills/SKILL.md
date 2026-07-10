---
name: pragmatic-engineering-standards
description: Apply pragmatic, no-nonsense senior-engineer standards to any coding task — favor simple working code over cleverness, verify behavior before declaring done, and cut scope creep; use whenever writing, reviewing, or refactoring code.
---

# Pragmatic Engineering Standards

This skill encodes the habits of an experienced, no-nonsense engineer: ship the smallest correct change, verify it actually works, and resist the pull toward premature abstraction or unnecessary polish.

## When to apply

Use this skill whenever writing new code, reviewing a diff, refactoring existing code, or deciding how to scope a task — especially when there's temptation to over-engineer, add speculative flexibility, or skip verification because "it should work."

## Core rules

1. **Solve the actual problem, not the imagined future one.** Write the code the current requirement needs. Don't add config options, abstraction layers, or extensibility hooks for use cases that haven't been asked for.
2. **Duplication beats the wrong abstraction.** If two pieces of code look similar but serve different call sites, leave them duplicated. Only extract a shared helper once a clear, stable pattern repeats at least three times.
3. **Prefer the boring, obvious solution.** Reach for standard library functions, well-known patterns, and existing project conventions before introducing a new dependency, framework, or clever one-liner. Cleverness that requires a comment to explain itself is a signal to simplify.
4. **Types and signatures should make illegal states unrepresentable where it's cheap to do so** — but don't chase perfect type safety at the cost of readability or velocity. A `TODO` disguised as a type assertion is still a `TODO`.
5. **No dead code, no speculative branches.** If a code path can't currently be reached, delete it rather than guarding it "just in case."
6. **Small, reviewable units of change.** Prefer a sequence of focused commits/diffs over one sprawling change that mixes refactor with feature.

## Step-by-step workflow

1. **Restate the requirement in one sentence.** If it can't be stated in one sentence, the task is probably too broad — split it before writing code.
2. **Check for existing patterns first.** Look at how the surrounding codebase already solves similar problems (naming, error handling, test structure) and match that style rather than inventing a new one.
3. **Write the minimal implementation.** Resist adding configuration, options, or generality beyond what's needed right now.
4. **Verify behavior, don't assume it.** Run the code, run the relevant tests, or otherwise exercise the actual change before calling it done. A type-check or lint pass is not the same as confirming the feature works.
5. **Re-read the diff as a reviewer would.** Look specifically for: leftover debug statements, unused imports/variables, inconsistent naming, and any comment that explains *what* the code does instead of *why* a non-obvious decision was made.
6. **Trim before finishing.** Remove anything added while exploring the solution that isn't needed in the final version — helper functions that ended up unused, alternate code paths that were tried and abandoned, extra logging.

## Red flags to catch in review

- A function or class that takes flags/parameters to switch between unrelated behaviors — likely two functions pretending to be one.
- New abstractions (base classes, interfaces, plugin registries) introduced for a single concrete use case.
- Error handling or validation for inputs that structurally cannot occur given the caller's guarantees.
- Comments restating the code rather than explaining a non-obvious constraint.
- Claims that something "works" without having actually run it end-to-end.
