---
name: learn-x-in-y-minutes
description: Generates a concise, example-driven syntax reference for a programming language or tool, written as a single heavily-commented code file in the style of learnxinyminutes.com; use when a user wants a fast primer on a new language, a cheat sheet of core syntax, or a "just show me the code" quick reference instead of prose documentation.
---

# Learn X in Y Minutes

This skill produces fast, dense, code-first reference material for a programming
language, tool, or library — the same idea as learnxinyminutes.com: teach the
syntax by writing valid (or near-valid) source code where the comments *are*
the tutorial. It is for programmers who already know how to program and want
to see the shape of a new language quickly, not a beginner's step-by-step
prose guide.

## When to apply this skill

Use this skill when the user asks for things like:
- "Give me a quick reference / cheat sheet for `<language>`."
- "Show me the syntax for `<language>` — I already know how to code."
- "What does idiomatic `<language>` look like?"
- "Summarize `<language>`'s syntax in one file I can skim."
- A comparison of core syntax across two or more languages.

Do not use this skill when the user wants a deep conceptual explanation, a
step-by-step beginner tutorial, or prose documentation of a specific API/library
they're already using in their own codebase — those call for ordinary
explanation, not a code-as-documentation cheat sheet.

## How to produce the reference

1. **Pick the single runnable file convention.** The output should be one
   source file in the target language's real syntax and file extension
   (e.g. `.py`, `.rs`, `.go`), structured so that if it were actually run,
   it would execute top-to-bottom without errors (or clearly mark any
   snippet that can't run inline, e.g. inside a string or a clearly labeled
   comment block).

2. **Lead with a file-level comment block** giving the language name, a
   one-line description, and (if relevant) how to run/compile it — this
   mirrors the header every learnxinyminutes file uses.

3. **Order topics from foundational to advanced**, roughly:
   - comments, basic types, variables, operators
   - control flow (if/loops/switch)
   - core data structures (arrays/lists, maps/dicts, sets, tuples/structs)
   - functions (definition, closures, default/variadic args)
   - the language's standout or unusual features (what makes it *not* just
     another C-like language — e.g. ownership/borrowing in Rust, goroutines
     in Go, prototypes in JS)
   - basic object/module system if the language has one
   - error handling
   - a short pointer to further reading (official docs), only as a comment,
     not a required external step to use the reference itself

4. **Every line of syntax gets a same-line or immediately-preceding comment**
   explaining what it does — assume the reader can already program, so
   explain the *language's* way of doing something, not what the general
   concept is. Prefer terse, concrete comments over paragraphs.

5. **Show, don't just tell, gotchas.** Where a language has a common trap
   (mutable default arguments, integer division, hoisting, off-by-one in
   ranges), include a short code example demonstrating the trap right next
   to the correct usage, rather than describing it abstractly.

6. **Keep it self-contained and dependency-free.** Prefer standard-library-only
   examples. If a third-party library is genuinely the idiomatic way to do
   something in that ecosystem, name it in a comment but don't require it to
   understand the rest of the file.

7. **Scale to what was asked.** If the user wants "just the basics," stop
   after core syntax and data structures — don't force every section above
   into a quick answer. If they want a comprehensive reference, work through
   the full list before presenting the result.

8. **Present the result as a single code block** in the target language,
   ready to save as a file, rather than splitting it across prose sections
   with commentary in between.
