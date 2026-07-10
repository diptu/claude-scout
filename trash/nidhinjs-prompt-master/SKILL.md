---
name: prompt-master
description: Helps craft precise, well-structured prompts for AI tools and models by clarifying intent, adding necessary context, and applying prompt-engineering best practices; use when a user wants to write, refine, or troubleshoot a prompt before sending it to any AI system.
---

# Prompt Master

This skill helps produce accurate, effective prompts for any AI tool or model. Use it whenever a user asks for help writing a prompt, wants to improve an existing prompt, is unsure how to phrase a request to get better AI output, or is troubleshooting why an AI tool gave a poor or off-target response.

## When to apply this skill

- The user explicitly asks for a prompt to be written or improved ("write me a prompt for...", "help me prompt X to do Y").
- The user shares a prompt that produced bad or inconsistent results and wants it fixed.
- The user is building a system prompt, agent instructions, or a reusable prompt template.
- The user is switching a task between AI tools (e.g., moving a workflow from one assistant to another) and needs the prompt adapted.

## Core approach

1. **Clarify the goal before writing anything.** Identify: what output is wanted, what format it should take, who/what will consume the output, and any constraints (length, tone, technical level, forbidden content). If the user's request is ambiguous or missing key details, ask targeted questions rather than guessing — a vague prompt produces vague output.

2. **Establish context and memory.** Gather relevant background the target AI needs to succeed: prior conversation history, domain-specific terminology, examples of desired output, and any constraints from earlier decisions. Carry this context forward explicitly in the prompt rather than assuming the target model will infer it — most AI tools have no memory of context outside what's given to them directly.

3. **Structure the prompt deliberately.** A strong prompt typically includes, in order:
   - **Role/framing**: who or what the AI should act as, if relevant.
   - **Task**: a single, unambiguous instruction stating exactly what to do.
   - **Context**: background facts, data, or prior state needed to complete the task correctly.
   - **Constraints**: format, length, tone, things to avoid, edge cases to handle.
   - **Examples** (if helpful): one or two concrete input/output pairs to anchor the desired style or structure.
   - **Output format**: explicit shape of the answer (plain text, JSON schema, bullet list, code block, etc.).

4. **Eliminate waste.** Cut filler, redundant qualifiers, and repeated instructions that don't change behavior — every extra sentence costs tokens and dilutes the signal of what actually matters. Prefer concrete, specific language ("respond in under 150 words as three bullet points") over vague guidance ("be concise").

5. **Make it tool-agnostic when needed.** If the user wants the prompt to work across different AI tools, avoid syntax or conventions specific to one platform (e.g., a particular system-message format) unless the user has named a specific target tool. When a target tool is named, adapt terminology and structure to match that tool's conventions.

6. **Iterate from feedback.** If the user reports that a prompt didn't produce the desired result, diagnose which part likely failed — ambiguous task framing, missing context, absent constraints, or no output-format specification are the most common causes — and revise that specific part rather than rewriting from scratch.

7. **Deliver the final prompt clearly.** Present the finished prompt as a distinct, copy-ready block, separate from any explanation of why it's structured that way. If the user only wants the prompt, skip meta-commentary and give just the prompt.

## Output quality checklist

Before presenting a finished prompt, verify it:
- States one clear task, not several competing ones.
- Includes all context needed for someone with zero prior knowledge of the conversation to understand the request.
- Specifies the desired output format explicitly.
- Contains no unnecessary words, hedges, or repeated instructions.
- Uses concrete constraints (numbers, formats, examples) instead of vague adjectives like "good" or "detailed."
