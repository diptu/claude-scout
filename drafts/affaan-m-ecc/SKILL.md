---
name: agent-harness-optimization
description: Audit and tune a Claude Code (or similar coding agent) working environment — project instructions, skills, memory, and permissions — so the agent works faster, safer, and with less repeated context; use when a user asks to improve agent performance, reduce prompt friction, or set up a new repo for agent-assisted development.
---

# Agent Harness Optimization

This skill helps you systematically improve the environment a coding agent operates in, rather than the code itself. The premise: most agent underperformance comes from a poorly configured harness — missing project instructions, stale or bloated context files, absent skills for recurring tasks, and no memory of past corrections — not from model capability. Apply it when the user says things like "Claude keeps making the same mistake," "set this repo up for agent development," "why is the agent slow/wasteful," or "improve my CLAUDE.md / skills / settings."

## When to apply

- Setting up a new repository for agent-assisted work.
- The user reports repeated agent mistakes, re-explaining the same conventions, or excessive permission prompts.
- Auditing an existing agent configuration (instructions files, skills directory, settings) for drift or bloat.
- Before a large agent-driven effort (refactor, migration) where harness quality compounds.

Do not apply it to tune application performance or CI speed — this is about the agent's operating environment only.

## Step-by-step guidance

### 1. Inventory the current harness

Before changing anything, enumerate what exists:
- Project instruction files (e.g. `CLAUDE.md`, `AGENTS.md`, editor-specific rule files) at repo root and in subdirectories.
- A skills directory (e.g. `.claude/skills/`) and what each skill claims to do.
- Settings and permission files (e.g. `.claude/settings.json`, local variants).
- Any memory or notes directories the agent maintains.
- Hooks or automation that run around agent tool calls.

Report the inventory briefly so the user sees the surface area before edits begin.

### 2. Audit project instructions for the three failure modes

Read the instruction file(s) and check for:
- **Missing load-bearing facts**: build/test/run commands, directory layout, non-obvious constraints ("tests must run through the Makefile"), and project-specific conventions the agent cannot infer from code. Add these first — they have the highest payoff.
- **Bloat**: generic advice ("write clean code"), duplicated content, long prose the agent will skim past. Cut anything a competent engineer wouldn't need told. Instruction files should be dense and short; every line costs attention on every turn.
- **Staleness**: commands that no longer work, paths that moved, decisions that were reversed. Verify each concrete claim (run the commands, check the paths) before keeping it.

### 3. Convert repeated corrections into durable artifacts

Ask (or infer from history) what the user keeps re-telling the agent. Each recurring correction belongs in exactly one place:
- A **fact about the project** → project instructions file.
- A **multi-step procedure invoked on demand** (release process, review checklist, deployment) → a skill file with a clear name and a one-sentence description stating when to use it.
- A **behavior around tool use** ("always run lint after editing") → a hook or settings entry, since instructions alone are advisory while hooks are enforced.
- A **fact about the user or ongoing work** → agent memory, if the harness supports it.

Putting guidance in the wrong layer is the most common defect: procedures crammed into the instructions file bloat every session, while facts hidden in skills never load when needed.

### 4. Right-size the skills library

For each existing skill:
- Check the description says both *what it does* and *when to trigger it* — a skill with a vague description never fires.
- Merge near-duplicates; delete skills that restate general model knowledge.
- Confirm each skill is self-contained: no dead links, no placeholders, no steps that depend on tools the environment lacks.

Prefer a few sharp skills over a large catalog of generic role descriptions.

### 5. Reduce permission friction safely

Review permission settings for prompts the user approves every time:
- Allowlist clearly read-only or low-risk commands (test runners, linters, build tools) that recur.
- Do **not** allowlist destructive, network-publishing, or credential-touching commands just to reduce prompts — flag these to the user explicitly and leave them gated.

### 6. Establish a research-first default

Encode into the instructions a working order for nontrivial tasks: read the relevant code and docs before editing, run existing tests before and after changes, and verify claims empirically rather than from assumption. State it as a short, concrete rule (e.g. "before modifying a module, read its tests"), not as philosophy.

### 7. Verify and hand off

- Re-run the key commands documented in the instructions to confirm they work as written.
- Summarize what changed in each layer (instructions, skills, settings, hooks) and why.
- Recommend a cadence: re-audit the harness whenever the user notices a repeated correction, and prune instruction files whenever they exceed roughly a screenful of dense content.

## Principles

- The harness is configuration under version control: keep edits small, reviewable, and committed with the reasons.
- Every layer has a cost — context tokens, attention, permission risk. Add to a layer only when a recurring pain justifies it, and remove faster than you add.
- Enforcement beats exhortation: if a behavior must always happen, wire it as a hook or setting; if it's judgment, write it as guidance.
