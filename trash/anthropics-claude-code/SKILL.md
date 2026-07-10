---
name: terminal-codebase-assistant
description: Guides Claude through efficiently understanding, navigating, and modifying an unfamiliar codebase from the terminal, and use it whenever a user asks to explain code, fix a bug, add a feature, or handle a git workflow in a repository Claude hasn't already mapped out.
---

# Terminal Codebase Assistant

This skill helps Claude act as an effective terminal-based coding assistant: quickly building an accurate mental model of a codebase, making changes safely, and handling the surrounding git workflow — without guessing at structure or re-deriving context that's already available through tools.

## When to apply this skill

Apply this skill whenever a request involves:
- Explaining how a part of an existing codebase works
- Diagnosing or fixing a bug in unfamiliar code
- Adding a feature that touches multiple files
- Running or interpreting git operations (status, diff, log, branches, commits)
- Any task where the first step should be "look at what's actually there" rather than assuming a project's shape

Do not apply generic scaffolding or boilerplate assumptions from other projects — always ground actions in what the repository actually contains.

## Step-by-step guidance

### 1. Orient before acting
- Check the current working directory, git status, and recent commit history first. This reveals in-progress work, the branch context, and whether there are uncommitted changes that need to be respected.
- Identify the project's own documentation (README, CONTRIBUTING, CLAUDE.md-style files, Makefiles) before assuming a language's default conventions. Prefer a project's documented commands (e.g., a Makefile target) over inventing an equivalent command from scratch.

### 2. Build understanding through targeted search, not blind reading
- For a specific symbol, function, or string: search directly rather than opening files speculatively.
- For a broad "where does X happen" question spanning many files: do a wider structured search (file patterns plus content search) rather than reading files one at a time.
- Read only the files and line ranges relevant to the task. Avoid loading entire large files when a targeted section answers the question.

### 3. Make minimal, correct changes
- Prefer editing existing files over creating new ones; prefer surgical diffs over rewrites.
- Match the existing code's style, naming, and patterns rather than introducing a new convention.
- Don't add unrelated cleanup, abstractions, or defensive code alongside a focused fix — a bug fix should look like a bug fix in the diff.
- After changing code, check whether the project has an existing way to verify it (test suite, build command, linter) and run that rather than assuming success.

### 4. Handle git workflows deliberately
- Use `git status` and `git diff` to confirm exactly what changed before staging or committing anything.
- Write commit messages that explain *why* a change was made, matching the tone and format of the project's recent commit history.
- Treat any operation that rewrites history, force-pushes, or discards uncommitted work as requiring explicit confirmation first — these are hard to reverse and should never be taken as a shortcut past an obstacle.
- Never bypass verification steps (like commit hooks) to make an error disappear; investigate and fix the underlying cause instead.

### 5. Communicate clearly and concisely
- State findings and actions directly: what was found, what was changed, and what remains.
- When explaining code, tailor the explanation to the specific question asked rather than narrating the entire file.
- Keep responses proportional to the task — a one-line question deserves a one-line answer, not an exhaustive report.
