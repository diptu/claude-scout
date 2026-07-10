---
name: awesome-claude-code-curator
description: Curates and vets third-party Claude Code resources (skills, subagents, slash commands, hooks, status lines, and plugins) before adopting them into a project or personal setup; use whenever a user wants to find, evaluate, or integrate a community-built Claude Code extension.
---

# Awesome Claude Code Curator

Helps evaluate and adopt community-built Claude Code extensions — skills, subagents, slash commands, hooks, status lines, and plugins — with the same rigor a maintainer would apply to a hand-picked "awesome list." Use this skill whenever a user wants to find something in the Claude Code ecosystem, decide whether a specific resource is worth adopting, or organize a growing collection of extensions so they stay discoverable and don't overlap.

## When to apply this skill

- The user asks "is there a skill/plugin for X?" or wants to find a community resource for a workflow they're trying to automate.
- The user has found a specific skill, subagent, hook, slash command, status line, or plugin (from a repo, gist, blog post, or forum) and wants an opinion on whether to add it.
- The user's project has accumulated several extensions (e.g. a `.claude/skills/` directory or a skills library) and wants them reviewed, deduplicated, or organized.
- The user wants to package their own work into one of these categories in a way that's consistent with ecosystem conventions.

## Categories to know

Community Claude Code resources generally fall into one of these buckets. Identify which one you're dealing with before evaluating it, since the vetting criteria differ:

- **Skills** — `SKILL.md` files (optionally with supporting scripts/references) that teach Claude a capability or workflow, invoked by name or auto-triggered by description.
- **Subagents** — specialized agent definitions with their own tools/model/system prompt, invoked via an agent-dispatch mechanism.
- **Slash commands** — short user-invoked prompts/macros bound to a `/name`.
- **Hooks** — shell commands wired into `settings.json` that fire automatically on events (pre-tool-use, post-tool-use, session-start, etc.).
- **Status lines** — scripts that render custom text in the CLI status bar.
- **Plugins** — bundles bundling any of the above together with a manifest, distributed as an installable unit.

## Step-by-step guidance

### 1. Clarify the goal before searching or judging

Ask (or infer from context) what workflow or pain point the user is trying to solve. Don't evaluate a resource in the abstract — evaluate it against a concrete need. If the user hasn't named one, ask what they're trying to accomplish first.

### 2. Vet a candidate resource before adopting it

For any specific skill/subagent/hook/plugin under consideration, check:

- **Scope fit**: does it do one coherent thing, or is it a grab-bag that will conflict with other extensions? Prefer narrow, composable resources over sprawling ones.
- **Trust boundary**: hooks and plugins can execute arbitrary shell commands automatically. Read exactly what commands a hook runs and when, before enabling it — never enable a hook you haven't read in full. Skills and slash commands are lower risk (they guide behavior, they don't auto-execute), but still read the full body, not just the description, since the description is what triggers it and can undersell or oversell what the body actually does.
- **Redundancy**: does an existing skill/subagent/command in the project already cover this? If so, prefer extending the existing one over adding a near-duplicate — a growing collection is only useful if entries stay non-overlapping.
- **Freshness and maintenance signal**: prefer resources that match current Claude Code conventions (correct frontmatter shape, no deprecated fields) over ones that look copy-pasted from an old format.
- **Self-containedness**: a good skill should work without requiring the user to have read some external document first. If a resource leans entirely on an external link with no inline explanation, treat that as a quality flag, not a blocker — summarize what it does before recommending it.

### 3. Decide: adopt, adapt, or skip

- **Adopt as-is** if it cleanly fits a real need, is scoped narrowly, and passes the trust check.
- **Adapt** if the core idea is right but the implementation is bloated, uses conventions that don't match the project, or bundles unrelated capabilities — extract just the useful part rather than importing the whole thing.
- **Skip** if it's redundant with something that already exists, or if it fails the trust boundary check (e.g. a hook running unreviewed commands) and the user has no strong reason to override that.

### 4. Keep the collection organized

When reviewing an existing set of extensions (not just one new candidate):

- Group by category (skills / subagents / commands / hooks / status lines / plugins) so it's easy to see what's covered and what's missing.
- Flag near-duplicates — two skills that trigger on overlapping descriptions will fight for auto-invocation and confuse Claude about which to use.
- Flag stale entries — resources referencing deprecated frontmatter fields, dead tool names, or workflows the project no longer uses.
- Prefer a short, curated list over an exhaustive one: every entry should earn its place by being distinct and currently useful, the same bar a well-maintained "awesome list" applies to its own entries.

### 5. Summarize the recommendation clearly

When reporting back, state plainly: what category the resource is, whether to adopt/adapt/skip, and the one or two reasons that drove the decision (scope fit, redundancy, or trust). Avoid hedging with a long pros/cons list when the decision is actually clear-cut.
