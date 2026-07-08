---
name: curate-claude-skills
description: Helps evaluate and organize a collection of Claude Code skills (custom or third-party) for quality, redundancy, and discoverability, and should be used when a user wants to review, prune, or catalog the skills available in a project or personal skill library.
---

# Curate Claude Skills

This skill helps assess and organize a collection of Claude Code skills so the
library stays high-quality, non-redundant, and easy to navigate. Apply it
when a user asks to review their skills directory, decide whether a new skill
is worth keeping, deduplicate overlapping skills, or produce a catalog/index
of what's available.

## When to apply this skill

- The user asks "do we have too many skills," "which of these overlap," or
  "should I keep this skill."
- A new skill is being added and it's unclear whether it duplicates existing
  functionality.
- The user wants a summary/index of all skills in a directory (e.g.
  `.claude/skills/`).
- The user wants to prune skills that are unused, broken, or superseded.

## Step-by-step guidance

1. **Inventory the skills.** List every `SKILL.md` file in the relevant
   directory. For each one, read its frontmatter (`name`, `description`) and
   skim the body to understand its actual scope — the description is a
   summary, not always the full picture.

2. **Check for structural quality on each skill:**
   - Frontmatter has exactly the expected keys and a description specific
     enough to disambiguate it from neighboring skills (a vague description
     like "helps with code" is a red flag).
   - The body gives concrete, actionable steps rather than generic advice
     ("write good code," "be careful") that adds no guidance beyond what the
     model would already do.
   - No dead references: file paths, tools, or commands the skill assumes
     exist should actually exist in the current environment.
   - No placeholder or TODO text left in.

3. **Detect overlap and redundancy.** Group skills by the trigger conditions
   in their descriptions. If two or more skills would plausibly fire on the
   same user request, decide:
   - Are they genuinely distinct (different scope, different output), and
     just need a sharper description to disambiguate? Tighten the wording.
   - Do they fully overlap? Recommend merging into one skill and removing
     the other, keeping whichever has the more complete/tested body.
   - Is one a narrower special case of another? Consider whether it should
     be a section within the broader skill instead of a standalone file.

4. **Flag low-value skills.** A skill is a candidate for removal if it
   restates default model behavior without adding project- or
   domain-specific knowledge, hasn't been triggered or referenced in recent
   work, or duplicates something already well-covered by the model's
   built-in capabilities.

5. **Produce output matched to the request:**
   - If asked for a catalog/index: a short table or list of skill name →
     one-line purpose, grouped by theme (e.g. review, research, ops, design).
   - If asked to prune: a list of specific skills to remove or merge, with a
     one-sentence reason for each, and what to merge them into if applicable.
   - If asked to evaluate a single new skill: a verdict (keep as-is / tighten
     description / merge with X / reject as redundant) with the reasoning.

6. **When adding a new skill inspired by an external source** (a blog post,
   a repo, a community list of prompts/workflows), don't copy it verbatim.
   Extract the underlying capability, verify it doesn't already exist in the
   current library per steps 1–3, and only then draft a new self-contained
   `SKILL.md` that follows the same structural quality bar described above.

## Principles to keep in mind

- Prefer fewer, sharply-scoped skills over many overlapping ones — overlap
  causes ambiguous triggering, not redundant coverage.
- A skill's value is in the concrete steps it adds, not in restating that a
  task should be done "carefully" or "well."
- Treat any external resource (repo, article, list) that inspired a skill as
  a source of ideas to adapt, not content to transcribe.
