---
name: docs-to-skill-converter
description: Converts external documentation (websites, GitHub repositories, PDFs, or other reference material) into a well-formed Claude Code skill, checking for conflicts with existing skills before finalizing; use when a user wants to turn a library's docs, a repo's README/wiki, or a technical PDF into a reusable SKILL.md.
---

# Docs-to-Skill Converter

This skill helps turn an external body of documentation into a properly
structured Claude Code skill (a `SKILL.md` file), so that knowledge currently
locked in a website, repository, or PDF becomes something Claude can apply
directly in future sessions without re-reading the source material each time.

## When to apply this skill

Apply this skill when the user asks to:
- "Turn these docs into a skill"
- "Make a skill out of this GitHub repo/README/wiki"
- "Convert this PDF/manual into something Claude can use"
- Build a reusable skill from any reference material that is currently just
  prose, a spec, or a set of pages rather than actionable guidance

Do not apply this skill when the user just wants a summary of the source
material, or wants code copied verbatim — the goal here is specifically to
produce actionable, reusable *guidance*, not a copy of the source.

## Step-by-step process

1. **Identify the source and its shape.**
   Determine whether the source is primarily conceptual (explains ideas),
   procedural (step-by-step how-tos), reference (API/CLI listings), or mixed.
   This shapes how the resulting skill should be organized — conceptual
   material becomes background context in the skill body, procedural material
   becomes numbered steps, reference material becomes a lookup section.

2. **Extract the core capability, not the whole document.**
   Do not try to transcribe the entire source. Identify the 3-7 recurring
   tasks or questions the source actually helps with, and organize the skill
   around those tasks. Skip incidental material (changelogs, marketing copy,
   installation instructions unrelated to the skill's actual use, license
   text).

3. **Draft the skill in standard SKILL.md form:**
   - YAML frontmatter with exactly `name` (short kebab-case slug) and
     `description` (one sentence stating what the skill does and when to use
     it — specific enough that it's clear when this skill should trigger vs.
     a neighboring one).
   - A body that states: what the skill helps with, when to apply it, and
     concrete step-by-step guidance or a decision framework.
   - Self-contained: no links back to the original source are required to
     use the skill. If exact syntax, error messages, or option names from the
     source are essential, inline the specific detail rather than referring
     the reader back to "the docs."
   - No placeholder text or TODO markers — every section should be usable
     as-is.
   - No auto-executing code. Code snippets may appear as illustrative
     examples within the guidance, but the skill itself is instructions for
     Claude to follow, not a script to run.

4. **Check for conflicts with existing skills before finalizing.**
   Before treating the draft as done, compare it against skills already
   available in the current environment (and any project-local skill
   directories):
   - **Name collision**: does another skill already use the same or a
     confusingly similar `name` slug? If so, rename to something more
     specific (e.g. prefer `stripe-webhook-setup` over the generic
     `webhook-setup` if a general webhook skill already exists).
   - **Description overlap**: does another skill's description cover the
     same triggering situations? If two skills would both plausibly fire for
     the same user request, either narrow both descriptions so their
     triggers are mutually exclusive, or fold the new material into the
     existing skill instead of creating a duplicate.
   - **Contradictory guidance**: does the new skill recommend an approach
     that conflicts with an existing skill's recommendation for overlapping
     situations (e.g. one says "always use library X," another says "avoid
     library X")? Flag this explicitly to the user rather than silently
     picking one side.
   - If no conflict is found, say so briefly and proceed; if a conflict is
     found, propose the specific resolution (rename, merge, narrow scope)
     before finalizing the skill.

5. **Validate scope before finishing.**
   Re-read the draft's description and body and confirm: a reader who has
   never seen the original source could follow this skill and get correct,
   useful results. If any step depends on knowledge that only exists in the
   original source and wasn't inlined, add it explicitly rather than leaving
   an implicit dependency.

## Notes on quality

- Prefer a smaller number of clearly-explained steps over an exhaustive
  transcription of every detail in the source — skills that try to cover
  everything become unreadable and are less likely to be applied correctly.
- When the source material is itself a collection of many small facts (e.g.
  a large API reference), consider whether the skill should teach a general
  *lookup strategy* (how to find the right section, what naming conventions
  to expect) rather than enumerating every entry.
- When in doubt about whether something belongs in the skill, prefer
  leaving it out and noting it as a follow-up rather than padding the skill
  with marginal content.
