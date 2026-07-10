---
name: architecture-decision-records
description: Draft, review, and maintain Architecture Decision Records (ADRs) to document significant technical decisions and their rationale; use when a user needs to record why an architectural choice was made, evaluate alternatives before committing to a design, or organize a project's existing decision history.
---

# Architecture Decision Records

This skill helps produce clear, consistent Architecture Decision Records (ADRs) — short documents that capture a significant technical or architectural decision, the context that led to it, the alternatives considered, and the consequences of the choice. ADRs exist so future contributors (including a future version of the same team) can understand *why* something was built a certain way without having to reconstruct the reasoning from commit history or tribal memory.

## When to apply this skill

Apply this skill when:

- A user is about to make (or has just made) a decision with long-term architectural consequences: choice of database, messaging pattern, API style, service boundary, major dependency, deployment topology, or similar.
- A user asks to "document this decision," "write an ADR," "record why we chose X," or similar.
- A user is reviewing or reorganizing a project's existing decision log and wants consistency across entries.
- A user is evaluating between multiple technical options and wants the tradeoffs captured in a durable, reviewable form rather than left in chat history.

Do not apply this skill to routine implementation details, bug fixes, or decisions with no lasting structural impact — ADRs are for choices that would be expensive to reverse or that future contributors would reasonably ask "why did we do it this way?" about.

## Where ADRs live

Unless the user specifies otherwise, ADRs belong in a `docs/adr/` or `docs/decisions/` directory at the project root, one file per decision, named with a zero-padded sequence number and a short slug, e.g. `0001-use-postgres-for-primary-storage.md`. Check for an existing ADR directory or numbering convention before creating a new one — match what's already there rather than introducing a second scheme.

## ADR structure

Each ADR should be a single markdown file with these sections:

1. **Title** — a short, descriptive name prefixed with the sequence number, e.g. `# 12. Use event sourcing for the billing ledger`.
2. **Status** — one of: `Proposed`, `Accepted`, `Deprecated`, `Superseded by ADR-NNNN`. An ADR's status can change over time; older ADRs should not be edited to pretend a past decision was always correct — instead, add a new ADR that supersedes it and update the old one's status.
3. **Context** — the problem being solved and the forces at play: technical constraints, business requirements, team capabilities, timelines. Write this section as if the reader has none of the conversation that led here — it should stand alone.
4. **Decision** — the choice that was made, stated plainly and unambiguously ("We will use PostgreSQL for the primary datastore," not "We are leaning towards...").
5. **Alternatives considered** — the other options that were seriously evaluated, and the specific reason each was rejected. Skip options that were never realistically on the table; padding this section with strawmen weakens the record.
6. **Consequences** — the resulting tradeoffs, both positive and negative. Every real decision has downsides; naming them here is what makes the record trustworthy rather than promotional. Include follow-up work or risks the decision introduces.

## Step-by-step guidance

1. **Identify the decision boundary.** Before writing, confirm with the user (or infer from context) what the actual decision is — scope it narrowly enough that it fits one ADR. A single ADR should cover one decision, not a bundle of related ones.
2. **Check existing ADRs first.** Look for a decisions directory and read a couple of existing entries to match tone, numbering, and section naming already in use. If none exist, propose the structure above and the file location before writing the first one.
3. **Gather the context honestly.** Ask what constraints actually drove the decision (deadline pressure, an existing system that couldn't change, a specific incident) rather than inventing generic-sounding justifications after the fact.
4. **Write the decision section first if it's already been made**, then work backward to context and alternatives — this keeps the document anchored to what actually happened rather than an idealized decision process.
5. **Name real alternatives with real rejection reasons.** "We considered X, but Y" is only useful if Y is the actual reason, not a rationalization. If the user doesn't remember why an alternative was rejected, say so plainly in the record rather than fabricating a reason.
6. **State consequences plainly, including negative ones.** A decision with no listed downsides should prompt a follow-up question — nearly every architectural choice trades something away.
7. **Cross-link related and superseding decisions.** If a new ADR reverses or narrows an earlier one, update the earlier ADR's status field and reference the new one; don't leave two contradictory "Accepted" decisions active at once.
8. **Keep it short.** An ADR is a record, not a design document — a page or less is typical. If the context section is ballooning, that's a signal the decision boundary from step 1 is too broad.
