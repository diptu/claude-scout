---
name: persona-review-suite
description: Runs a fixed panel of role-based reviews (CEO, Designer, Eng Manager, Release Manager, Doc Engineer, QA) over a piece of work before it ships, catching the blind spots any single perspective misses; use when a plan, PR, feature, or release is close to done and needs a final multi-angle sanity check before landing.
---

# Persona Review Suite

## What this skill helps with

A single reviewer (human or AI) tends to catch the class of problem they're already primed to look for: an engineer reviewing their own PR checks "does it work," not "does it look right" or "will support tickets spike." This skill runs the same piece of work through several fixed, opinionated personas in sequence, each with a narrow mandate, so blind spots from any one lens get caught by another before the work ships.

Use it as a final gate on work that's otherwise "done" — a feature branch ready to merge, a plan ready to execute, a release ready to cut — not as a substitute for normal development or as an early-stage brainstorming tool.

## When to apply

Apply this when the user asks for a final review, a "does this look ready to ship" check, or a pre-release/pre-merge sanity pass on non-trivial work — typically a feature, a PR, a plan, or a release candidate. Skip it for small, low-risk changes (typo fixes, config tweaks, one-line bug fixes) where the overhead of six review passes exceeds the risk being guarded against.

## The personas and their mandate

Run each persona as a distinct pass over the same artifact (diff, plan, or release). Each persona should only comment within its lane — resist the urge to let the CEO persona comment on code style, or the QA persona comment on business strategy. Keep each pass short and concrete: a handful of findings, not an essay.

1. **CEO** — Does this actually serve the user/business goal? Is scope right-sized (not gold-plated, not cutting a corner that matters)? Would this be embarrassing to explain to a customer or the board?
2. **Designer** — Is the UI/UX/copy consistent, intentional, and free of "AI slop" defaults (unstyled spacing, generic microcopy, inconsistent hierarchy)? Does it match the product's existing visual language?
3. **Eng Manager** — Is the implementation appropriately scoped and maintainable? Any obvious tech debt being introduced without acknowledgment? Is the diff reviewable, or does it need to be split?
4. **Release Manager** — Is this safe to ship right now? Are there migration, rollout, feature-flag, or rollback concerns? Does it depend on anything not yet deployed?
5. **Doc Engineer** — Does documentation (README, CHANGELOG, inline comments, API docs) reflect the new behavior? Will a future reader or user be able to figure out what changed and why?
6. **QA** — What's the failure mode? Walk the golden path and the obvious edge cases (empty input, concurrent access, network failure, permission denial) and flag anything untested or unhandled.

## Step-by-step guidance

1. Confirm the scope of the review with the user: a diff, a plan document, or a release bundle. Read the actual artifact — don't review from memory or from a description of the change.
2. Run each of the six persona passes in order, one at a time. For each persona, state its mandate in one line, then list concrete findings (or "no concerns" if genuinely clean) — cite specific files, lines, or plan sections, not vague impressions.
3. After all six passes, synthesize: separate findings into "must fix before shipping" versus "worth noting but not blocking." Don't let every persona's nitpick become a blocker — use judgment about severity.
4. Present the synthesis to the user as a short punch list, not six separate essays. Let the user decide what to act on; this skill surfaces gaps, it doesn't unilaterally block or auto-fix them.
5. If the user asks to act on findings, treat that as a separate, explicit follow-up task — don't start editing code or documents mid-review.
