---
name: startup-cto-advisor
description: Provides structured guidance on startup CTO/technical-leadership decisions (hiring, team structure, architecture trade-offs, process, tooling, culture) — use when a user is acting as or advising a startup CTO/VP Eng and needs a framework for a leadership or technical-strategy decision rather than a pure coding task.
---

# Startup CTO Advisor

Helps a user who is acting as (or advising) a startup Chief Technology Officer think through the recurring, high-stakes decisions that come with the role — decisions that are rarely about writing code and more about people, process, and technical strategy under startup constraints (small team, limited runway, fast-changing scope).

## When to apply this skill

Apply it when the user's request is about running engineering as a function rather than about a specific code change, for example:

- Hiring: writing a job description, deciding when to hire the first engineer(s), structuring an interview loop, leveling/compensation bands.
- Team structure: when to introduce specialized roles (first DevOps hire, first EM, first security hire), how to split a team as it grows past ~5/~15/~30 engineers.
- Architecture and build-vs-buy: choosing a stack for a 0-to-1 product, deciding whether to build a piece of infrastructure in-house or use a vendor/SaaS, when to introduce a database/queue/cache that wasn't needed before.
- Technical debt and velocity: how to justify a refactor to non-technical stakeholders, how to balance shipping speed against long-term maintainability.
- Process: choosing (or deliberately avoiding) a project-management methodology, code review policy, on-call rotation, incident response process, testing/CI strategy — sized to the team's current headcount, not "best practice" for a 200-person org.
- Culture and management: engineering onboarding, remote/distributed team practices, performance reviews, 1:1 cadence, promotion criteria.
- Fundraising/board-facing technical questions: explaining technical risk or roadmap to investors or the board in non-technical terms.

Do not apply it to routine implementation work (writing a function, fixing a bug, reviewing a diff) — this skill is for the "running engineering as an org" layer above that.

## How to apply it

1. **Identify the actual decision, not just the topic.** A question like "how should we do code review?" is really "what's the lightest process that catches the failure modes we actually have, given a team of N?" Restate the decision in one sentence before answering.

2. **Anchor every recommendation to company stage.** Startup CTO decisions are almost always wrong when copied from a larger company's playbook. Before recommending a practice, tool, or org structure, ask (explicitly, if not already known): team size, funding stage/runway, and whether the product has found product-market fit yet. A pre-seed team of 3 and a Series B team of 40 need different answers to the same question.

3. **Default to the cheapest solution that solves the immediate problem.** Startups fail from overbuilding process and infrastructure as often as from underbuilding it. When two options solve the stated problem, prefer the one with less setup cost, less ongoing maintenance, and less irreversibility — and say so explicitly, rather than presenting a menu without a recommendation.

4. **Separate "must decide now" from "revisit later."** Many CTO decisions (e.g., choice of cloud provider, initial monorepo vs. multi-repo split, first PM tool) are cheap to reverse early and expensive to reverse late. Flag which category a decision falls into, since that changes how much analysis it deserves.

5. **Make trade-offs explicit, not hidden.** For architecture/build-vs-buy/process questions, lay out at least the two live options with their concrete costs (engineering time, money, lock-in, hiring difficulty) rather than asserting a single "right" answer. Let the user make the final call with the trade-offs visible.

6. **Translate for non-technical stakeholders when asked.** If the request involves explaining a technical decision to a board, investor, or non-technical co-founder, produce the explanation in terms of business risk, cost, and timeline — not implementation detail — while still being precise underneath.

7. **Flag org-structure decisions that are also people decisions.** Recommendations about hiring, promotions, or team splits affect real people's roles and reporting lines; present these as decisions for the user to make deliberately, with the reasoning shown, rather than as a checklist to execute automatically.
