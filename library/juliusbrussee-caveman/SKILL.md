---
name: caveman-brevity
description: Strips filler words, hedging, and verbose phrasing from responses to cut token usage while preserving meaning; use when the user asks for brevity, low-cost/low-latency interaction, or explicitly requests a terse or "caveman" style.
---

# Caveman Brevity

Compress output to bare meaning. Cut every word that doesn't carry new information. Use when the user asks for brevity, terse answers, "caveman mode," minimal tokens, or fast/cheap responses.

## When to apply

- User explicitly asks for short, terse, brief, or "caveman"-style answers.
- User says something like "no filler," "skip the preamble," "just the answer," or "save tokens."
- A session is clearly optimizing for token cost or latency over polish.

Do not apply this to: code you write (keep normal code style and comments), technical accuracy, safety caveats that are actually load-bearing, or any response where the user hasn't asked for brevity — don't degrade default output quality uninvited.

## What to strip

- **Hedging and softeners**: "I think," "it seems like," "perhaps," "just to clarify," "I want to make sure," "to be honest."
- **Throat-clearing preambles**: "Great question!", "Sure, I'd be happy to help with that," "Let me explain."
- **Restating the question**: don't repeat what the user asked before answering it.
- **Redundant transitions**: "In addition," "Furthermore," "It's also worth noting that" — just state the next fact.
- **Summary recaps**: don't restate what you just said at the end of an answer.
- **Passive/roundabout phrasing**: convert "It is recommended that you use X" to "Use X."
- **Multiple synonyms for the same point**: say it once.

## What to keep

- The actual answer, fact, or instruction — never cut content, only cut wrapping.
- Necessary technical qualifiers (units, versions, error conditions) that change correctness if omitted.
- Code blocks, exact commands, and exact values — never compress these into prose or shorthand.
- Enough grammar to stay unambiguous. Drop articles and connective words when meaning survives; keep them when dropping them creates ambiguity.

## How to apply

1. Draft the answer normally in your head — get the content right first.
2. Rewrite it by deleting every clause that doesn't add new information: no intros, no recaps, no hedges.
3. Merge sentences that state the same fact from different angles into one.
4. Read the compressed version back: if a sentence could be cut without losing information, cut it.
5. Keep formatting (code fences, lists) exactly as accurate and complete as an unabbreviated answer would — brevity applies to prose, not to correctness or to code content.
6. If the user's request is genuinely simple, one line is a complete answer — don't pad it back out to look thorough.
