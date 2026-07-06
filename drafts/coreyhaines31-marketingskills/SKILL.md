---
name: marketing-growth-toolkit
description: Use when the user asks to improve conversion rates, audit or write marketing copy, plan SEO content strategy, or diagnose growth/analytics problems — covers CRO, copywriting, SEO, and growth analytics workflows.
---

# Marketing Growth Toolkit

This skill helps with marketing engineering tasks that sit at the intersection of copy, conversion, search visibility, and analytics: auditing a landing page for conversion issues, writing or rewriting sales/marketing copy, planning an SEO content strategy, or diagnosing why a growth metric moved (or didn't).

## When to apply this skill

Apply this skill when the user's request matches any of:
- "Review/audit this landing page" or "why isn't this page converting"
- "Write/rewrite this headline, hero copy, email, or ad copy"
- "Help me plan SEO content" or "what keywords should we target"
- "Our signups/conversion/traffic dropped — help me figure out why"
- General requests to "make this more persuasive" or "improve our funnel"

Do not apply it to unrelated engineering tasks (e.g., fixing a backend bug) even if the word "growth" or "conversion" appears incidentally.

## Conversion Rate Optimization (CRO)

When auditing or improving a page/flow for conversion:

1. **Identify the single primary action** the page should drive (signup, purchase, demo request). If there are multiple competing calls-to-action, flag that as a likely conversion leak before anything else.
2. **Check the above-the-fold value proposition**: does a visitor understand what the product does, who it's for, and why it matters within 5 seconds? If not, that's the first fix, ahead of button colors or micro-copy.
3. **Audit friction points in order**: form length and required fields, number of clicks to the goal, unnecessary account creation steps, unclear pricing, missing trust signals (testimonials, logos, guarantees, security badges).
4. **Look for mismatched intent**: does the traffic source's promise (ad copy, search query) match what the landing page actually delivers? Mismatch here kills conversion regardless of on-page polish.
5. **Prioritize by leverage, not novelty**: recommend fixes in order of estimated impact × ease, not in the order they were noticed. State the reasoning, don't just list changes.
6. **Never recommend a change without a stated hypothesis** ("moving the CTA above the fold should reduce scroll-drop-off") — vague "make it better" suggestions are not useful.

## Copywriting

When writing or rewriting marketing copy:

1. **Start from the reader's problem, not the product's features.** Lead with the pain point or desired outcome; introduce the product as the resolution.
2. **Match the target reading level and tone** to the audience (technical buyers tolerate density; consumer audiences need short sentences and concrete language).
3. **Prefer specific, falsifiable claims over vague superlatives.** "Cuts deploy time from 40 minutes to 6" beats "blazing fast."
4. **One idea per sentence, one argument per paragraph.** Cut qualifiers, hedges, and adverbs that dilute the claim.
5. **Always give a clear next action** at the end of copy (a single CTA, not several competing ones).
6. **When rewriting existing copy, preserve any facts, numbers, and compliance-sensitive claims exactly** — only change structure, clarity, and persuasion, never invent statistics or claims that weren't in the original.

## SEO strategy

When planning SEO content or auditing search visibility:

1. **Anchor on search intent, not just keyword volume.** Classify target queries as informational, navigational, commercial, or transactional, and match content format to intent (e.g., a comparison page for commercial-intent queries, a how-to guide for informational ones).
2. **Favor topic clusters over isolated pages**: a pillar page plus supporting cluster content that internally links tends to outperform disconnected one-off articles.
3. **Check for cannibalization** before recommending new content — if an existing page already targets the same query, recommend consolidating or differentiating rather than creating a competing page.
4. **Don't ignore technical SEO basics** when auditing: title tags, meta descriptions, header hierarchy, page speed, mobile rendering, and crawlability are prerequisites — content quality can't overcome a page search engines can't index.
5. **Recommend content structured for both human readers and answer-engine extraction**: clear headers, direct answers near the top, structured data where relevant.

## Growth analytics

When diagnosing a growth or funnel problem:

1. **Establish the baseline and the delta first**: what was the metric before, what is it now, over what time window — don't diagnose causes before confirming the change is real and not noise (sample size, seasonality, tracking gaps).
2. **Segment before theorizing**: break the metric down by channel, device, geography, and cohort to localize where the change originated, rather than guessing at a single root cause for an aggregate number.
3. **Check for instrumentation issues first** (tracking code changes, tagging errors, bot traffic) before assuming a behavioral or market cause — a broken pixel is a far more common explanation than a demand shift.
4. **Distinguish correlation from causation explicitly**: if a change coincided with a metric shift (a redesign, a pricing change, a campaign launch), state it as a hypothesis to test, not a confirmed cause.
5. **Recommend the smallest test that would falsify the leading hypothesis** rather than jumping straight to a full re-architecture of the funnel.

## General approach

Across all of the above, ground recommendations in the specific page/copy/data the user provides rather than generic best-practice lists. When information needed to give a concrete answer is missing (e.g., no analytics numbers, no existing copy to review), ask for it rather than fabricating plausible-sounding specifics.
