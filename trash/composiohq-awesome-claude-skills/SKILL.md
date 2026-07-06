---
name: claude-skills-curator
description: Curates and evaluates third-party Claude Code skills discovered from community lists and repositories, helping decide which ones are worth adopting, adapting, or skipping — use when the user wants to survey available skills for a capability, compare multiple candidate skills, or vet a skill before adding it to a project.
---

# Claude Skills Curator

This skill helps evaluate and organize third-party Claude Code skills (SKILL.md files, skill bundles, or skill collections) so a project only accumulates skills that are genuinely useful, non-redundant, and safe to run.

## When to apply this skill

Apply this skill when:

- The user asks "is there a skill for X?" or wants to survey what skills exist for a given capability (e.g. testing, deployment, copywriting, data viz).
- The user has found one or more candidate skills (from a GitHub repo, a curated list, a Reddit post, or similar) and wants help deciding whether to adopt them.
- The user wants to compare two or more skills that appear to overlap in purpose.
- The user wants to clean up or consolidate an existing collection of skills that has grown ad hoc.

Do not apply this skill to writing new skills from scratch with no existing candidate to evaluate — that is authoring, not curation.

## Step-by-step guidance

1. **Inventory what exists.** Before evaluating a new candidate, check what skills are already available (in the project's `.claude/skills/` directory, any skill library folder, or the list of skills already surfaced in context). Note names and one-line descriptions.

2. **Extract the candidate's real capability.** Read the candidate skill's frontmatter `description` and body. Identify concretely: what task does it perform, what triggers should invoke it, and what tools or external services (if any) does it assume are available. Ignore marketing language ("awesome", "powerful", "production-grade") and focus on the literal capability.

3. **Check for overlap.** Compare the candidate against the existing inventory from step 1:
   - If an existing skill already covers the same trigger conditions and capability, recommend skipping the candidate or merging any genuinely new guidance into the existing skill rather than adding a duplicate.
   - If the candidate covers a narrower or broader scope than an existing skill, note the boundary explicitly (e.g. "this one is React-specific, the existing one is general frontend") so both can coexist without ambiguity about which applies when.

4. **Vet for self-containment and safety.** A good skill should:
   - Work without requiring external URLs to be fetched at use-time.
   - Contain no placeholder or TODO text.
   - Not embed code that executes automatically — skills are guidance, not scripts. Flag any skill that bundles auto-running scripts, especially ones that shell out, fetch remote content, or modify files without an explicit user-invoked step.
   - Have a description specific enough to reliably trigger only when relevant (vague descriptions like "helps with coding" cause a skill to fire too often or never).

5. **Decide: adopt, adapt, or skip.**
   - **Adopt as-is** if the candidate is self-contained, non-overlapping, and well-scoped.
   - **Adapt** if the core idea is good but the description is too broad/narrow, the guidance references external tools not present in this project, or it needs trimming to remove fluff. Rewrite the frontmatter description and tighten the body rather than keeping bloat.
   - **Skip** if it duplicates existing coverage, depends on unavailable infrastructure, or fails the safety check in step 4.

6. **Keep the collection lean.** When recommending adoption, prefer editing or extending an existing skill over adding a near-duplicate. A skill collection with fewer, well-scoped skills is more reliable than a large collection with overlapping, vaguely-triggered ones — overlap causes ambiguity about which skill should fire for a given request.

7. **Summarize the decision.** When reporting back, state clearly: what the candidate does, whether it overlaps with anything existing, and the adopt/adapt/skip recommendation with a one-sentence reason. This keeps the decision auditable if revisited later.
