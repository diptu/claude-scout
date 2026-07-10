---
name: skill-authoring-spec
description: Use when writing or reviewing a Claude Code SKILL.md file, to ensure it follows Agent Skills specification conventions for frontmatter, structure, and discoverability.
---

# Skill Authoring Spec

This skill helps Claude author or review a `SKILL.md` file so it conforms to the Agent Skills specification: a lightweight, portable format for packaging procedural knowledge that an agent can discover and load on demand.

## When to apply this skill

Apply this skill whenever:
- A user asks Claude to create a new skill, slash command skill, or `SKILL.md` file.
- A user asks Claude to review, fix, or improve an existing skill file.
- Claude needs to decide whether a piece of guidance belongs in a skill versus inline instructions.

## Core structure of a valid SKILL.md

Every skill file has exactly two parts:

1. **YAML frontmatter**, delimited by `---` lines at the top of the file, containing:
   - `name`: a short, kebab-case identifier. It should match the skill's folder name if the skill lives in its own directory, be unique within the skill set it's loaded alongside, and be specific enough that it doesn't collide with an unrelated skill (e.g. `pdf-form-fill` rather than `pdf`).
   - `description`: one sentence written in the third person that states both *what the skill does* and *when to use it*. The description is the only part of the skill an agent sees before deciding to load it, so it must contain the trigger conditions explicitly (specific file types, task phrasing, keywords, or situations) rather than a vague summary. Avoid marketing language ("powerful", "comprehensive") — favor concrete nouns and verbs an agent can pattern-match against a request.

2. **Body content** in Markdown, which is only loaded into context after the agent has decided (from the description alone) that the skill is relevant. The body should:
   - Open with a short statement of the problem the skill solves.
   - Give explicit trigger conditions if they're more nuanced than the frontmatter description conveys (this doubles as documentation for humans maintaining the skill).
   - Provide concrete, step-by-step guidance rather than abstract principles — numbered steps, checklists, or decision trees the agent can follow directly.
   - Avoid duplicating information the agent can already derive from reading the target code or files itself.

## Step-by-step process for drafting a new skill

1. **Identify the trigger.** Before writing anything, articulate in one sentence: what request, file type, or situation should cause this skill to activate? If this can't be stated concretely, the skill is too broad or too vague to be discoverable — narrow it.
2. **Write the description first.** Draft the frontmatter `description` before the body. If the description can't fit in one sentence while still naming the trigger, split the skill into two narrower ones instead of writing a longer description.
3. **Draft the body as a runbook, not an essay.** Prefer imperative, numbered steps ("1. Check X. 2. If Y, do Z.") over prose explaining background theory. An agent executing the skill needs actions, not motivation.
4. **Keep it self-contained.** The skill body should not depend on external URLs, prior conversation state, or files that may not exist. If the skill needs reference material (e.g. a palette, a schema, a checklist), inline it directly in the body rather than pointing outside the file.
5. **Avoid overlapping skills.** Before finalizing, check whether an existing skill already covers the same trigger. If two skills would both plausibly fire on the same request, either merge them or sharpen both descriptions so their trigger conditions are mutually exclusive.
6. **Validate the frontmatter.** Confirm the file starts and ends its frontmatter block with a bare `---` line, contains exactly `name` and `description` keys (no extra keys unless the target platform explicitly supports them), and that `name` is lowercase kebab-case with no spaces or special characters.
7. **Review for scope creep.** A skill should do one job well. If the body accumulates multiple unrelated procedures ("also use this for X, and separately for Y"), split it into separate skills with separate trigger descriptions.

## Common mistakes to avoid

- **Vague descriptions** ("helps with documents") that give the agent no way to match the skill to a real request — always name concrete triggers.
- **Instructions to run automatically.** A skill is guidance for the agent to follow deliberately, not a script that executes itself; don't write it as if invoking it performs an action on its own.
- **Placeholder or TODO content.** Every skill should be complete and usable as written — no "fill this in later" sections.
- **Redundant restating of code.** Don't describe what a file does when the agent can just read the file; focus the body on decisions, conventions, and steps the agent wouldn't otherwise infer.
