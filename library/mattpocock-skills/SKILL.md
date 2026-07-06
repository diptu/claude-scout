---
name: typescript-strict-engineering
description: Apply senior-engineer TypeScript discipline (strict typing, no any/unknown escapes, exhaustive checks, minimal abstractions) when writing or reviewing TypeScript code, so output matches production-grade standards rather than tutorial-quality code.
---

# TypeScript Strict Engineering

This skill helps Claude write and review TypeScript the way an experienced,
detail-obsessed engineer would: type-safe by construction, resistant to
silent runtime failures, and free of unnecessary abstraction. Apply it any
time the task involves writing, refactoring, or reviewing TypeScript code —
not just when the user explicitly asks for "strict" or "clean" code.

## When to apply this skill

- Writing new TypeScript modules, functions, or types.
- Reviewing or refactoring existing TypeScript code.
- Answering questions about TypeScript type design, generics, or error
  handling patterns.
- Any task where the user's codebase has a `tsconfig.json` — check its
  `strict`/`noUncheckedIndexedAccess` settings and match or exceed them.

## Core principles to enforce

1. **No silent type escapes.** Never introduce `any` to make a type error go
   away. If a type is genuinely unknown, use `unknown` and narrow it with a
   type guard before use. Treat `as` casts as a last resort that requires a
   one-line comment explaining why the compiler can't infer it.

2. **Model illegal states as unrepresentable.** Prefer discriminated unions
   over optional fields when a type has mutually exclusive shapes (e.g. a
   `Result<T, E>`-style `{ success: true, data: T } | { success: false,
   error: E }` instead of `{ data?: T, error?: E }`). This eliminates a whole
   class of "forgot to check" bugs at the type level.

3. **Exhaustiveness over fallthrough.** When switching over a union or enum,
   add a `default` branch that assigns the remaining value to a variable
   typed `never` (or calls a small `assertUnreachable(x: never)` helper) so
   that adding a new union member causes a compile error at every unhandled
   switch, not a silent runtime gap.

4. **Infer, don't restate.** Derive types from a single source of truth
   (`typeof`, `ReturnType<>`, `Parameters<>`, `satisfies`) rather than
   hand-writing a parallel interface that can drift out of sync with the
   implementation. Use `satisfies` instead of a type annotation when you
   want literal-type inference preserved alongside a structural check.

5. **Narrow at the boundary, trust internally.** Validate and narrow
   external input (API responses, user input, environment variables) once,
   at the edge of the system. Once a value has a precise type, do not
   re-validate it deeper in the call stack — trust the type system.

6. **Errors are values or exceptions, not both.** Pick one error-handling
   strategy per boundary (thrown exceptions for programmer errors and truly
   exceptional cases, `Result`-style return values for expected failure
   modes like validation or network errors) and apply it consistently
   within that module rather than mixing styles.

7. **No premature generics or abstractions.** Only introduce a generic type
   parameter, a shared interface, or a helper utility once the same pattern
   appears at least three times. Two similar-looking functions are cheaper
   to read than one abstraction that almost fits both.

## Step-by-step guidance when writing code

1. Check for an existing `tsconfig.json` and match its strictness; if none
   exists, default to writing code that would pass under `strict: true` and
   `noUncheckedIndexedAccess: true`.
2. Design the types first: sketch the shape of the data (including
   exclusive/impossible states) before writing the function bodies.
3. Write the implementation, deriving types from runtime values wherever
   possible instead of duplicating them.
4. Add exhaustiveness checks to every `switch`/conditional chain over a
   union type.
5. Re-read the diff looking specifically for `any`, unchecked `as` casts,
   and optional fields that are actually mutually exclusive with another
   field — fix these before considering the code done.

## Step-by-step guidance when reviewing code

1. Grep for `any`, `as any`, `@ts-ignore`, and `@ts-expect-error` — each one
   needs either removal or a justifying comment.
2. Check every `switch` over a union for a `never`-typed exhaustiveness
   check.
3. Look for optional-field structs that should be discriminated unions.
4. Flag hand-written types that duplicate something inferable via `typeof`,
   `ReturnType<>`, or `satisfies`.
5. Flag any new generic parameter, base class, or shared utility introduced
   for a single call site — suggest inlining until a third occurrence
   justifies the abstraction.
