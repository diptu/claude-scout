---
name: kubernetes-contribution-navigator
description: Guides a contributor through understanding and participating in the Kubernetes open-source project's community structure (SIGs, working groups, membership ladder, KEPs, and contribution workflow); use when a user wants to contribute to Kubernetes or a similarly-governed CNCF-style project, or wants to model their own project's governance/contributor process on Kubernetes' approach.
---

# Kubernetes Contribution Navigator

This skill helps a user understand how the Kubernetes project organizes itself and how to contribute effectively, or helps them adapt Kubernetes' governance patterns to their own open-source project.

## When to apply this skill

Use this skill when the user:
- Wants to make their first contribution to Kubernetes (code, docs, tests, or non-code work like triage/design).
- Is confused about Kubernetes-specific terms like SIG, KEP, OWNERS file, or the member/reviewer/approver ladder.
- Wants to propose a new feature and needs to know whether it requires a formal enhancement proposal.
- Wants to find the right place to raise an issue, ask a question, or request a review.
- Is designing governance, contributor tiers, or an enhancement-proposal process for their own project and wants a proven model to adapt.

## Core concepts to explain

When helping a user navigate this space, ground your guidance in these structural pieces:

1. **Special Interest Groups (SIGs) and Working Groups.** Kubernetes development is decentralized into SIGs (e.g., SIG Node, SIG Network, SIG API Machinery), each owning a domain of the codebase, holding its own regular meetings, and maintaining its own charter. Working Groups are temporary, cross-SIG efforts formed to solve a specific problem and dissolved once it's done. Before pointing a user at "the Kubernetes team," help them identify the specific SIG whose domain matches their interest — that SIG's charter and meeting notes are the actual source of truth, not a general project-wide process.

2. **The contributor ladder.** Kubernetes uses a staged trust model: Contributor → Member → Reviewer → Approver → Subproject Owner. Each stage grants more repository authority (from opening PRs, to being requested as a reviewer via `OWNERS` files, to having merge rights) and each stage has explicit, documented requirements (e.g., sustained contributions, sponsorship by two existing members). When advising a user on "how do I get more involved," map their actual goal onto the right rung of this ladder rather than assuming they need commit access to make progress — most impact happens at the Contributor/Member level.

3. **OWNERS files as the access-control mechanism.** Rather than a central admin list, each directory in the codebase carries an `OWNERS` file naming who can approve (`approvers`) and who can review (`reviewers`) changes in that path. When a user asks "who do I need to get sign-off from," the answer is almost always "check the nearest `OWNERS` file up the directory tree from the file being changed," not a person or a SIG in the abstract.

4. **Kubernetes Enhancement Proposals (KEPs).** Significant features go through a KEP — a structured design document covering motivation, goals, non-goals, design details, graduation criteria (alpha/beta/stable), and test plans — before implementation begins. Help the user judge scope honestly: a bug fix or small enhancement does not need a KEP; a new API, a cross-cutting behavior change, or anything affecting multiple SIGs almost always does. Steer them toward writing a KEP early rather than building first and justifying later, since KEPs are reviewed and can change the design substantially.

5. **Code of Conduct and community norms.** Kubernetes maintains an explicit code of conduct and community values (openness, inclusion, respect) that govern all interactions — issue discussions, PR reviews, SIG meetings. When drafting communication on the user's behalf (issue text, PR descriptions, meeting proposals), keep tone collaborative and assume good faith from maintainers who are volunteers with limited bandwidth.

## Step-by-step guidance for a first-time contributor

When a user says they want to contribute:

1. Ask what they want to work on (a specific bug, a feature idea, or just "get involved") and what skills they bring (Go, docs writing, testing, design).
2. Help them identify the most relevant SIG based on the area of the codebase or problem domain involved.
3. Point them to that SIG's contribution guide and meeting cadence as the concrete next step, rather than a generic "read the contributing guide" — general Kubernetes contribution docs cover process; the SIG covers substance.
4. If their change touches a specific file or directory, walk them to check the nearest `OWNERS` file for that path so they know who to loop in for review.
5. If the change is more than a small fix (new API surface, new flag with broad implications, cross-SIG behavior change), advise drafting a short design proposal (KEP-style: motivation, goals, non-goals, design, testing/graduation plan) before writing code, and getting SIG sign-off on the proposal first.
6. Remind them that non-code contributions (triage, documentation, testing, community management) are equally valid entry points and often faster ways to reach the "Member" rung than a first code PR.

## Step-by-step guidance for adapting this model to another project

When a user wants to borrow this governance style for their own project:

1. Help them decide if their project is large enough to benefit from splitting into SIG-like domains — this only pays off once a single maintainer group can no longer track every area; for small projects, recommend staying with a flat model instead.
2. Suggest an explicit, staged trust ladder (even a simplified 2-3 stage version) with written criteria for each stage, rather than an implicit "ask the maintainer" system — explicit criteria scale better and reduce bias.
3. Recommend directory-scoped ownership (an `OWNERS`-style file or equivalent in their tooling) if the codebase has areas with different natural experts, so review requests route to the right people automatically.
4. Suggest a lightweight design-proposal process gated by change size — only require it above a size/impact threshold the user defines, so it doesn't become bureaucratic overhead for small changes.
5. Recommend writing down community norms (a code of conduct, communication expectations) early, since retrofitting them after conflict arises is much harder than establishing them upfront.
