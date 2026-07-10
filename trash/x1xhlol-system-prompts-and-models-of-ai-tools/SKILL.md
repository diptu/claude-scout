---
name: ai-tool-system-prompt-design
description: Design or review system prompts and tool-use instructions for AI coding agents/assistants by applying structural patterns common to production AI tools; use when writing a new agent system prompt, a tool description, or auditing an existing prompt for gaps.
---

# AI Tool System Prompt Design

This skill helps Claude write, review, or improve system prompts for AI coding
agents and assistants — the kind of instructions that define an agent's role,
its available tools, its constraints, and its output conventions. Apply it
when a user asks to draft a system prompt for a custom agent, write tool
descriptions, add guardrails to an existing agent, or review why an agent's
prompt is producing bad behavior (over-eager tool calls, ignoring
constraints, inconsistent output format, etc).

Production AI coding tools (IDE agents, autonomous coding agents, browser
agents) converge on a recognizable set of structural patterns because they
solve the same problems: keeping an LLM grounded in a specific role, using
tools correctly, respecting safety boundaries, and producing consistent
output. This skill captures those patterns as reusable design guidance.

## When to apply

- A user asks you to write or draft a system prompt for an agent, assistant, or bot.
- A user asks you to write tool/function descriptions for an agent's tool schema.
- A user is debugging an existing agent that misuses tools, ignores instructions, or behaves inconsistently, and the root cause looks like a prompt structure problem rather than a code bug.
- A user asks how to add guardrails (safety, scope limits, escalation rules) to an agent's instructions.

## Structural pattern to follow

When drafting or reviewing a system prompt, check that it covers these
sections, roughly in this order. Not every agent needs every section — match
depth to the agent's actual scope — but each omitted section should be a
deliberate choice, not an oversight.

1. **Identity and scope.** One or two sentences stating what the agent is,
   what it operates on, and what its boundaries are. Vague identity
   ("You are a helpful assistant") produces vague behavior; a specific
   identity ("You are a code-review agent that only reads diffs and never
   modifies files") constrains the model's choices from the first token.

2. **Environment and context.** Facts the agent needs but shouldn't
   re-derive every turn: what platform it runs on, what state persists
   between calls, what it can and cannot assume about the user's setup.
   Production agents front-load this so the model doesn't waste turns
   discovering it (e.g. asking the user what OS they're on).

3. **Tool definitions and when to use each one.** For every tool, state not
   just what it does but *when* to prefer it over alternatives and when not
   to use it at all. The most common failure mode in agent prompts is tools
   with accurate descriptions but no disambiguation guidance, which causes
   the model to pick the wrong tool for a task that two tools could both
   technically handle. Write tool guidance as decision rules: "use X for Y,
   not Z" rather than isolated capability lists.

4. **Operating procedure.** A short ordered checklist of how the agent
   should approach a typical task: gather context, form a plan, act, verify.
   Agents given only a goal and a tool list tend to skip verification steps;
   naming the steps explicitly (even briefly) measurably improves follow-through.

5. **Constraints and guardrails.** Explicit "never do X" and "always do Y"
   rules for the specific failure modes that matter for this agent: scope
   creep, destructive actions without confirmation, fabricating results,
   ignoring user corrections. State the boundary and, where it's non-obvious,
   the reason — a bare rule gets rationalized away in edge cases, a rule with
   a reason survives them.

6. **Output format and tone.** How the agent should structure responses:
   length, use of code blocks/markdown, whether to narrate its steps, when to
   ask clarifying questions versus proceeding with reasonable assumptions.
   This section is what makes an agent feel consistent across many
   invocations instead of stylistically random.

7. **Examples (optional, for hard-to-specify behavior).** When a rule is
   easier to show than state precisely — formatting edge cases, tone
   calibration, disambiguating similar tools — include one or two short
   examples rather than trying to write an exhaustive rule.

## Review checklist for an existing prompt

When asked to audit or debug an existing agent prompt, check for these
common gaps, since they map to the most frequent real-world failure modes:

- Tools with overlapping capabilities but no guidance on which to prefer.
- Constraints stated once but not reinforced near the relevant tool
  definitions (a "never delete without confirmation" rule buried in a
  general section is easier for the model to miss than one placed next to
  the delete-capable tool itself).
- No stated escalation path for ambiguous or risky situations — agents
  without one tend to either over-ask (annoying) or silently guess
  (dangerous), depending on training bias.
- Output format specified nowhere, causing turn-to-turn inconsistency.
- Identity/scope so broad that the agent has no basis for declining
  out-of-scope requests.

## How to apply this when drafting

Start from the identity and scope section and work down the list, writing
only as much as the agent's actual complexity warrants — a narrow
single-tool agent may need three short sections, while a multi-tool
autonomous agent needs all seven. Prefer concrete, situational phrasing
("when the user asks to delete a branch, confirm first") over abstract
principles ("be careful with destructive actions"), since concrete rules are
what actually change model behavior at decision points.
