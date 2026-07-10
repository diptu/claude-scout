---
name: prefix-cache-stable-sessions
description: Structures long-running coding-agent sessions to keep prompt prefixes stable so cache hits stay high and latency/cost stay low; use when a session is expected to run for many turns, when context is getting expensive/slow, or when the user asks to keep an agent "running" continuously rather than restarting it per task.
---

# Prefix-Cache-Stable Sessions

Helps keep long-running coding-agent sessions fast and cheap by preserving a
stable, append-only prompt prefix instead of repeatedly rewriting earlier
context. Most LLM inference backends (including Claude's) cache the
key/value state for a prompt prefix and reuse it on the next call as long as
that prefix is byte-identical. Once anything earlier in the prompt changes —
a reordered instruction, an edited system message, a summary that got
rewritten — the cache is invalidated from that point forward, and everything
after it must be recomputed. A session that keeps its prefix stable turn
after turn gets cheaper and faster the longer it runs; a session that
rewrites its own history gets slower and more expensive the longer it runs.

## When to apply this

- The user says something like "leave it running," wants a long-lived
  coding-agent session, or is running many turns/tasks back-to-back in one
  conversation instead of one-off requests.
- The user reports a session getting slower or more expensive as it goes on.
- Before designing a system prompt, task-loop structure, or memory/context
  strategy for an agent that will run continuously.
- When deciding how to inject new information (files read, tool results,
  running notes) into an ongoing session.

## Core principle

Treat everything already in the context as immutable. Only ever append. Any
technique that "improves" context by editing, reordering, deleting, or
summarizing-in-place what came before pays for that improvement with a full
cache miss on the rest of the session.

## Step-by-step guidance

1. **Freeze the system/instruction prefix first.** Before the session starts
   producing turns, finalize the system prompt, tool definitions, and any
   fixed instructions. Don't plan to tweak these mid-session — a single edit
   invalidates the cache for the entire conversation that follows.

2. **Append, don't rewrite.** When new information needs to enter the
   context (a file's contents, a command's output, a decision made), add it
   as a new message or a new block at the end. Do not go back and edit an
   earlier message to "fix" or "tidy" it, even if it would read better that
   way — the cost of the rewrite outweighs the readability gain.

3. **Avoid in-place summarization of live context.** Compressing early
   turns into a shorter summary is sometimes necessary to fit a context
   window, but recognize it as a deliberate cache-reset, not a free cleanup.
   Do it only when actually needed (approaching a context limit), not
   proactively "to keep things tidy."

4. **Keep volatile data out of the stable prefix.** Things that change
   often — timestamps, random IDs, live counters, "current time" stamps —
   should live as late in the prompt as possible (ideally in the final
   user turn), never embedded in the system prompt or early fixed context.
   A single changing token near the front of the prompt breaks caching for
   everything after it.

5. **Batch related edits into one turn instead of many small ones.** Each
   new turn appended to a stable prefix is cheap; each turn that also
   forces a rewrite of prior content is expensive. When several small
   changes are needed, prefer doing them together in one appended step over
   several turns that each perturb earlier state.

6. **Keep tool/function schemas and their order fixed for the session's
   lifetime.** Reordering tools, renaming them, or changing their
   descriptions mid-session invalidates the cached prefix just like editing
   the system prompt does.

7. **Prefer long-lived sessions over restart-per-task when the work is
   related.** Repeatedly starting a fresh session for each small task
   throws away the accumulated cache benefit; continuing in the same
   session (appending the next task as a new turn) keeps the earlier
   prefix warm and reusable.

8. **When something earlier genuinely must change** (a wrong instruction,
   corrected fact), accept the one-time cache invalidation explicitly
   rather than trying to preserve caching around it — don't contort the
   session structure to avoid an edit that's actually necessary. Make the
   correction once, then return to append-only behavior for everything
   after.

## Signs the guidance is being violated

- Context is being "cleaned up" or reordered for readability partway
  through a long session.
- A summary of earlier turns is regenerated every few turns instead of
  once when actually needed.
- Timestamps, request IDs, or other changing values sit near the start of
  the prompt rather than the end.
- The session restarts frequently for closely related tasks that could
  have been appended to an existing one.
