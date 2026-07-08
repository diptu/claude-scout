---
name: session-memory-capture
description: Captures key context, decisions, and unresolved threads from the current working session into a persistent memory file, then surfaces relevant entries at the start of future sessions so work can resume without re-deriving prior context.
---

# Session Memory Capture

This skill helps Claude maintain continuity across separate coding sessions on the same project by persisting a compact, curated record of what happened, why, and what's still open — then re-reading that record before starting new work.

## When to apply this skill

Use this skill when:

- The user asks Claude to "remember this," "pick up where we left off," or references work from a previous session.
- A session is ending (explicitly, or the conversation is wrapping up) and meaningful decisions, unresolved issues, or non-obvious context were produced that would otherwise be lost.
- Starting a new session in a project that has an existing memory file from this skill, so prior context can inform current work.
- The user wants to avoid repeating the same explanations, constraints, or rejected approaches across multiple sessions.

Do not apply this skill for information that is already recoverable from the codebase itself (file structure, git history, existing docs) — only capture what would otherwise be lost: reasoning, decisions, rejected approaches, and open threads.

## Where memory lives

Store captured context in a single file at the project root: `.claude/session-memory.md` (create it if it doesn't exist). Keep it flat and human-readable — no database, no nested structure beyond simple markdown sections. If the file grows past a few hundred lines, compress older entries into a short summary rather than deleting them outright, so long-running history isn't silently lost.

## Step-by-step guidance

### Capturing context (end of session, or after a significant milestone)

1. Review the session for information that is **non-obvious and would be expensive to re-derive**: decisions made and why, approaches tried and rejected (and why), constraints the user stated, open questions, and the next concrete step.
2. Skip anything derivable from reading the code or running `git log` — don't duplicate what's already durable elsewhere.
3. Write a new dated entry to `.claude/session-memory.md` using this structure:

   ```
   ## YYYY-MM-DD — <short topic>
   - Decision/fact: <what was decided or learned>
   - Why: <the reasoning or constraint behind it>
   - Open: <anything still unresolved, or "none">
   ```

4. Keep each entry tight — a few bullet lines, not a transcript. Compress rather than transcribe.
5. If an entry updates or contradicts an earlier one, edit the earlier entry instead of leaving both to avoid confusion later.

### Restoring context (start of session)

1. Before starting substantive work, check whether `.claude/session-memory.md` exists.
2. If it exists, read it and skim for entries relevant to the current request — prioritize the most recent entries and anything matching the topic at hand.
3. Treat entries as historical context, not current truth: if a memory claims a file, function, or approach exists, verify it against the actual codebase before relying on it, since code may have changed since the entry was written.
4. Use restored context to avoid re-asking questions the user already answered, re-proposing approaches already rejected, or losing track of open threads — but don't recite the memory file back to the user unless it's directly relevant to their current request.

### Keeping memory trustworthy

- Only write entries when there's something genuinely worth persisting — not a summary of every session.
- Prefer updating a stale or wrong entry over leaving it to accumulate alongside corrections.
- If the user says to forget something, find and remove the corresponding entry rather than appending a correction.
