---
name: skill-library-curator
description: Reviews, prunes, and catalogs a collection of Claude Code skills for quality, redundancy, and discoverability; use when a user wants to audit an existing skill library or decide whether a new skill is worth adding to one.
---

# Skill Library Curator

This skill helps assess a collection of Claude Code skills (SKILL.md files, whether custom-written or pulled from third-party sources) and keep the collection healthy: easy to search, free of near-duplicates, and made up of skills that actually earn their place.

## When to apply this

Apply this skill when:

- A user asks to review, clean up, or organize a folder of skills (e.g. `.claude/skills/`, a `library/` directory, or similar).
- A user is deciding whether a newly drafted or discovered skill should be added to an existing collection.
- A user wants a catalog, index, or summary of what skills exist and what each one does.
- A user suspects two or more skills overlap and wants to know whether to merge, deprecate, or keep them separate.

## Step-by-step guidance

### 1. Inventory the collection

- Locate every `SKILL.md` (or equivalent) file in the target directory, including nested subdirectories.
- For each one, extract its `name`, `description`, and a short read of the body to understand its actual scope (descriptions can be stale or over-broad — verify against the body).
- Build a simple table: name, one-line purpose, rough size (short/medium/long), and any obvious red flags (missing frontmatter, placeholder text, dead references to files or URLs that don't exist).

### 2. Check for redundancy

- Group skills by the problem they solve, not just by keyword overlap in their names.
- Two skills are candidates for merging if invoking either one in a real scenario would produce materially the same guidance.
- Two skills that sound similar but apply to different scopes (e.g. one for reviewing plans, one for reviewing shipped code) should usually stay separate — note the distinction explicitly so future readers don't re-merge them by mistake.
- When redundancy is found, recommend one of: merge into a single skill, deprecate the weaker one, or keep both but tighten each description so the trigger conditions no longer overlap.

### 3. Evaluate quality

For each skill, check:

- **Trigger clarity**: does the `description` field say precisely when to use it? A vague description ("helps with code") means Claude may never invoke it, or invoke it too often.
- **Self-containment**: does the body avoid depending on external URLs, files that may not exist, or assumed prior context?
- **Actionability**: does the body give concrete steps, not just abstract principles? A skill that only states philosophy without guidance on what to actually do is low value.
- **No dead weight**: flag skills with placeholder sections, TODO markers, or copy-pasted boilerplate that was never filled in.

### 4. Decide: keep, prune, or merge

For each skill, reach one of three verdicts:

- **Keep as-is**: clear trigger, self-contained, actionable, no overlap.
- **Prune**: redundant with a stronger skill, too vague to ever trigger reliably, or covers a need that no longer exists.
- **Merge or rewrite**: valuable content but poorly scoped, overlapping description, or missing steps — fix rather than discard.

### 5. Produce a catalog

When asked for a catalog or index, produce a compact list grouped by category (e.g. planning, review, design, ops) rather than a flat alphabetical dump. For each entry, give: name, one-line purpose, and when to reach for it instead of a neighboring skill. This is the artifact a future user or Claude session should be able to scan in under a minute to pick the right skill.

## Notes for applying judgment

- Favor a small number of clearly-scoped skills over a large number of overlapping ones — a bigger library is not automatically a better one.
- When unsure whether two skills overlap, imagine the specific user request that would trigger each one; if the same request plausibly triggers both, that's a sign to consolidate.
- Preserve any skill-specific knowledge (edge cases, hard-won lessons) when merging or rewriting — don't let curation silently delete institutional knowledge.
