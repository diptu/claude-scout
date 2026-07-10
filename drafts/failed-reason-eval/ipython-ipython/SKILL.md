---
name: ipython-interactive-debugging
description: Guides Claude in using IPython's interactive shell features (magic commands, tab completion, object introspection, and post-mortem debugging) to explore, debug, and profile Python code more effectively than with a plain Python REPL or script execution.
---

# IPython Interactive Debugging

This skill helps Claude make use of IPython's interactive shell when a task involves exploring unfamiliar Python code, diagnosing a runtime error, profiling performance, or iterating quickly on a snippet before it goes into a script or module. Apply it whenever the user is working in a Python project and asks to "debug this," "figure out why this fails," "profile this function," or "try this out interactively," rather than defaulting to editing files blind or writing throwaway `print()` statements.

## When to use this skill

- The user hits a traceback and wants to understand the failure, not just see the stack trace.
- The user wants to inspect an object's attributes, source code, or docstring without leaving the shell.
- The user wants a quick timing or profiling comparison between two implementations.
- The user is exploring an unfamiliar library or codebase and wants to poke at live objects.
- The user wants to iterate on a piece of logic before committing it to a file.

## Core capabilities to apply

### 1. Post-mortem debugging instead of guesswork
When a script raises an exception, prefer running it under IPython and dropping into the debugger at the point of failure rather than adding print statements and re-running repeatedly:
- Run the script with `ipython --pdb script.py`, or inside a running IPython session use the `%debug` magic immediately after a traceback to jump into `pdb` at the exact frame where the exception occurred.
- Once in the debugger, use `u`/`d` to move up/down stack frames, `p <expr>` or `pp <expr>` to print/pretty-print values, and `l` to list source around the current line — this reveals the actual state at failure time instead of relying on inference.
- If the error is rare or hard to reproduce, use `%pdb on` to make IPython auto-enter the debugger on every uncaught exception for the rest of the session.

### 2. Object introspection instead of reading source blind
Before assuming what a function, class, or module does:
- Use `object?` (single question mark) to show the docstring, signature, and type.
- Use `object??` (double question mark) to show the actual source code when available — faster than searching the filesystem for the definition.
- Use `%pdoc`, `%pdef`, and `%psource` as explicit equivalents when the `?` shorthand isn't available in the current context.
- Use tab completion (`object.<TAB>`) conceptually to enumerate available attributes/methods when reasoning about what an object supports, rather than guessing from naming conventions alone.

### 3. Timing and profiling instead of assuming performance
When the user asks which of two approaches is faster, or wants to find a bottleneck:
- Use `%timeit` for a single line, or `%%timeit` for a whole cell, to get a statistically meaningful timing rather than a single wall-clock measurement.
- Use `%prun` to run a full profiler over a function call and identify which sub-calls dominate runtime.
- Use `%time` for a one-off timing (single run) when the code has side effects that make repeated execution unsafe.
- Report actual measured numbers back to the user rather than asserting which approach "should" be faster.

### 4. Fast iteration instead of edit-run-edit cycles
When developing or testing a snippet before it's finalized:
- Use `%run script.py` to execute a script in the current namespace, so variables remain inspectable afterward.
- Use `%load` to pull a file's contents into the current cell for quick modification, and `%edit` to open an external editor on a piece of code mid-session.
- Use `%who` / `%whos` to see what variables are currently defined in the namespace, and `%reset` to clear it when starting a fresh experiment.
- Use `%history` to review what's already been tried in the session, avoiding repeating a failed approach.

## How to apply this in practice

1. When a traceback appears, don't stop at the printed stack trace — reconstruct the failing state (call `%debug` conceptually, or explain to the user how to do so, and reason about what `p <expr>` at the failing frame would reveal).
2. When asked "what does this do," prefer describing what `object?`/`object??` would surface (signature, docstring, source) over guessing from the name alone.
3. When asked to compare performance, frame the answer in terms of what `%timeit`/`%prun` would measure, and if you can execute code, actually run the timing rather than estimating.
4. When iterating on a fix, keep the working state in mind the way an IPython namespace would persist across cells — don't discard intermediate reasoning by starting over from scratch each time.
5. Prefer precise, inspectable steps (introspect, then act) over broad edits made on assumption.
