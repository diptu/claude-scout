---
name: long-horizon-task-orchestration
description: Breaks a long-running, multi-hour research/coding/creation task into a persistent plan with checkpointed memory and delegated subagent steps, so Claude can work through it reliably across many tool calls without losing track of progress or context.
---

# Long-Horizon Task Orchestration

Use this skill whenever a task is too large to finish in a single uninterrupted burst of tool calls — multi-step research reports, large refactors, multi-file builds, or "go build/investigate X" requests that will plausibly take many minutes to hours and many tool invocations. The goal is to keep the task coherent across a long working session: never lose track of what's done, what's next, or why a decision was made, even if context gets compacted or the session is resumed later.

## When to apply

Apply this when a request has any of these shapes:
- It names an end goal but not a fixed sequence of steps ("research X and write a report," "migrate the codebase to Y," "build a working prototype of Z").
- It will clearly require more exploration, iteration, or tool calls than fits comfortably in one focused pass.
- The user says things like "take your time," "this might take a while," or asks for something that spans multiple subsystems or sources.

Do not apply it to small, single-shot asks (a one-file fix, a quick question, a single lookup) — the overhead of planning and checkpointing isn't worth it there.

## Core approach

Treat the task as four layers working together: a **plan**, a **memory log**, **delegated execution**, and a **gateway back to the user**.

### 1. Decompose into a persistent plan

Before doing any work, break the goal into an ordered list of concrete, checkable steps (use the task-tracking tool if one is available; otherwise write the plan as a short numbered list in your first response). Each step should be small enough to verify independently — "fetch data from source A," not "do the research." Keep the plan visible and update it as you learn more; don't silently reorder or drop steps without noting why.

### 2. Keep a running memory of decisions, not just actions

As you work, maintain a short log of *why* choices were made, not just what was done — which sources were checked and rejected, which approach was tried and abandoned, what constraints were discovered mid-task. This matters most right before context is likely to be compacted or the task is paused: write down enough that a fresh read of the log (without the surrounding conversation) would let you or anyone else resume correctly. Prefer writing this into a durable artifact (a scratch file, a plan document, or a memory system if one exists) rather than trusting it to stay in the visible conversation.

### 3. Delegate bounded subtasks instead of doing everything inline

For steps that are self-contained and don't need the full running context — a broad codebase search, a research pass over many sources, a batch of independent file edits — delegate them as isolated subtasks (via a subagent, background task, or separate tool invocation) rather than doing them inline. This keeps the main thread's context focused on integration and decision-making instead of raw exploration output. When delegating:
- State the subtask's goal, the exact scope, and what "done" looks like.
- Don't delegate decisions that require the full context of prior steps — only hand off work that's genuinely self-contained.
- When a delegated subtask returns, verify its result against the plan before marking the step done; don't take a returned summary at face value if it's easy to spot-check.

### 4. Checkpoint and report incrementally, don't go dark

For long sessions, surface progress at natural checkpoints (finishing a plan step, hitting a blocker, making a consequential decision) rather than staying silent until the very end. If a step turns out to be blocked, wrong, or riskier than expected, stop and say so instead of pushing forward on a bad assumption for many more steps. When the task legitimately needs a long wait (a build, an external process, a scheduled check), use whatever scheduling/waiting mechanism is available rather than busy-polling or guessing.

### 5. Close out deliberately

When the plan's steps are all done, do a final pass: confirm every step in the plan was actually completed (not just attempted), reconcile the memory log against the end state, and give a concise summary of what changed and what, if anything, was descoped or deferred. Don't declare success on partial completion — either finish the remaining steps or explicitly flag them as unfinished.

## Key discipline

The value of this skill is in never losing the thread on a long task — favor writing plans and decision logs down over holding them only in working memory, favor delegating bounded independent work over doing it all inline, and favor surfacing blockers early over silently pushing through them.
