---
name: karpathy-coding-discipline
description: Apply Andrej Karpathy's observed anti-patterns for LLM-written code as a self-check before and after writing code, to keep changes minimal, verified, and honest about uncertainty rather than confidently wrong.
---

# Karpathy Coding Discipline

This skill encodes a set of recurring failure modes that large language
models exhibit when writing code, as observed by Andrej Karpathy across many
sessions of LLM-assisted coding. Apply it as a self-check discipline whenever
writing, editing, or reviewing code — not as a one-time read, but as a
running checklist to consult before submitting any change.

## When to apply

- Before writing any non-trivial code change, to plan the smallest version
  that could work.
- While writing code, to catch the urge to over-engineer, over-comment, or
  swallow errors.
- After writing code, before declaring it done, to verify it was actually
  run and actually works rather than merely "looks correct."
- Especially during long agentic sessions, where drift toward sprawling,
  unverified, defensively-padded code compounds turn over turn.

## The anti-patterns to guard against

1. **Confident fabrication over honest uncertainty.** LLMs tend to state
   things as fact — an API's shape, a library's behavior, a test's outcome —
   without having checked. Before asserting something is true, check it: read
   the actual source, run the actual command, look at the actual output. If
   you have not verified it, say "I believe" or "let me check," not "this
   works."

2. **Growing the diff instead of shrinking it.** Left unchecked, an LLM will
   pad a small fix with unrelated refactors, new helper functions, extra
   configuration options, and speculative abstractions. Before finishing a
   change, ask: what is the minimal diff that solves exactly the stated
   problem? Delete anything that doesn't serve that.

3. **Error handling that hides bugs instead of surfacing them.** A common
   tic is wrapping new code in broad try/except (or equivalent) blocks that
   catch and silently log or ignore errors. This makes code "look robust"
   while actually hiding the real failure. Only handle errors at genuine
   boundaries (user input, network calls, external processes) where a
   specific failure mode is expected and there's a specific recovery action.
   Let unexpected errors surface with their original stack trace.

4. **Writing code without running it.** An LLM can produce plausible-looking
   code for an entire feature without ever executing a single line. Plausible
   is not the same as correct. Before claiming a change works, actually run
   it — execute the function, run the test, start the server, hit the
   endpoint — and look at the real output, not just the code's structure.

5. **Comment noise.** LLMs over-explain via comments that restate what the
   code already says ("# increment counter" above `count += 1`), or leave
   comments referencing the current task ("# fixed per user request") that
   will be stale the moment the task is forgotten. Only comment on the parts
   a reader could not infer from the code itself: a non-obvious constraint,
   a workaround for a specific bug, an invariant that isn't locally visible.

6. **Defensive code for impossible cases.** Validating, null-checking, or
   type-guarding against inputs that cannot actually occur given the calling
   code adds bulk without adding safety, and it obscures what inputs are
   actually expected. Validate only at real system boundaries; trust internal
   invariants elsewhere.

7. **Premature abstraction.** Faced with two similar blocks of code, an LLM
   will often reach immediately for a shared helper or base class. A little
   duplication is cheaper to read and change than the wrong abstraction.
   Don't factor out shared structure until a third occurrence makes the
   pattern unambiguous.

8. **Treating "it compiles" or "it typechecks" as "it works."** Passing a
   linter, type checker, or compiler proves the code is well-formed, not that
   it does the right thing. Before reporting success, exercise the actual
   behavior the change was meant to produce and confirm the observed
   output matches intent.

9. **Losing the thread on long tasks.** Over a long session, an LLM can drift
   from the original ask — solving an adjacent problem, adding scope nobody
   requested, or forgetting a constraint stated many turns earlier. Before
   finishing a multi-step task, re-read the original request and confirm the
   final change actually addresses it, nothing more and nothing less.

## Step-by-step application

1. Before coding: restate the smallest change that satisfies the request.
   Resist adding anything beyond it.
2. While coding: for every new branch of error handling, ask "can this
   actually happen, and if so, what should happen next?" Delete branches that
   fail this test.
3. While coding: for every comment, ask "would a reader be confused without
   this?" Delete comments that fail this test.
4. After coding: run the code — the actual function, script, test, or
   server — and read the real output. Do not report success based on static
   inspection alone.
5. After coding: diff what changed against what was asked. Trim anything
   that isn't load-bearing for the original request.
6. When uncertain about a fact (an API signature, a library's default
   behavior, whether a file exists), verify it by reading the source or
   running a check, rather than stating it from assumption.
