---
name: claude-skill-curator
description: Evaluates and organizes third-party Claude Code skills discovered from community lists or repositories, checking each candidate for quality, redundancy, and safety before recommending it be added to a project or personal skill library; use when a user wants to review, compare, or vet Claude Skills before adopting them.
---

# Claude Skill Curator

This skill helps Claude systematically evaluate third-party Claude Code
skills (SKILL.md files, skill repositories, or curated "awesome list" style
collections) before recommending they be added to a project or personal
skill library. It turns an ad-hoc "this looks useful" reaction into a
repeatable vetting pass.

## When to apply this skill

Apply this skill whenever the user:

- Points to a GitHub repo, gist, or list containing one or more candidate
  Claude Code skills and asks whether they're worth adding.
- Asks Claude to compare several candidate skills and pick the best one(s).
- Wants an existing personal or team skill library reviewed for redundancy,
  staleness, or quality issues.
- Is building a new skill and wants it checked against the same bar before
  it's considered "done."

Do not apply this skill to routine, single-purpose skill authoring where the
user has already decided what they want written — only invoke the vetting
pass when there's a decision to make about whether to keep, add, or discard.

## Step-by-step guidance

1. **Inventory the candidates.** List every candidate skill by name with a
   one-line description of what it claims to do. If the source is a list of
   many skills, group them by rough category (e.g. "web/frontend",
   "devops", "writing", "research") so duplicates and overlaps are easier to
   spot in the next step.

2. **Check for redundancy against what already exists.** If the user has an
   existing skill library or `.claude/skills/` directory, compare each
   candidate's stated purpose against skills already present. Flag any
   candidate whose functionality is already covered, even partially, and
   note whether the new one is meaningfully better (broader coverage,
   clearer triggers, fewer failure modes) or just a duplicate.

3. **Evaluate each candidate on four dimensions:**
   - **Usefulness** — does it solve a real, recurring task, or is it a
     one-off wrapper around something a plain prompt would already do well?
   - **Clarity of trigger conditions** — does the skill's description make
     it obvious *when* Claude should invoke it? Vague or overly broad
     triggers cause a skill to fire when it shouldn't, or never fire at all.
   - **Self-containment and safety** — does the skill avoid requiring
     unreviewed external code execution, credentials, or network calls it
     doesn't explain? Treat any skill that bundles executable scripts or
     asks for elevated permissions as higher risk and call this out
     explicitly rather than silently approving it.
   - **Maintenance signal** — for skills sourced from a repository, note
     any visible signal of staleness (no recent updates, unresolved issues
     referenced in the description, broken or placeholder content) since
     this affects how much to trust the skill's guidance going forward.

4. **Produce a recommendation per candidate**, one of:
   - **Adopt as-is** — clearly useful, non-redundant, safe.
   - **Adopt with edits** — good core idea, but rewrite the trigger
     description, strip unsafe automatic execution, or tighten the scope
     first.
   - **Skip — redundant** — an existing skill already covers this; name
     which one.
   - **Skip — low value or unsafe** — explain the specific concern (vague
     triggers, unreviewed code execution, unclear benefit over a plain
     prompt).

5. **Summarize the decision set.** After evaluating all candidates, give the
   user a short table or list: candidate name, recommendation, and the
   one-sentence reason. Avoid re-explaining the full evaluation for every
   candidate in the summary — the reasoning belongs in step 4, the summary
   is for fast scanning.

6. **If asked to integrate an adopted candidate**, write it as a
   self-contained SKILL.md: YAML frontmatter with `name` and `description`
   only, followed by a body with concrete step-by-step guidance, no
   placeholder text, and no code that would execute automatically. Do not
   copy the candidate's original wording verbatim if it contains unclear
   instructions, unsafe automation, or references to external tooling that
   won't exist in the target environment — rewrite those parts so the skill
   stands on its own.
