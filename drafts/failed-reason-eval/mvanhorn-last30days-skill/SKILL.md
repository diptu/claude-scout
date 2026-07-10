---
name: topic-pulse-research
description: Researches what people are currently saying about a topic by synthesizing recent discussion across social platforms, forums, and the web into a grounded, cited summary; use when a user wants a snapshot of current sentiment, discourse, or news around a topic rather than a single-source answer.
---

# Topic Pulse Research

This skill helps Claude produce a grounded, multi-source summary of what people are currently saying about a topic — pulling signal from social platforms (Reddit, X/Twitter, YouTube comments/discussion), forums (Hacker News), prediction markets (Polymarket-style signals), and general web search, then synthesizing it into one coherent, cited answer rather than a single-source take.

## When to apply this skill

Apply this skill when the user asks things like:
- "What's the current buzz/sentiment around X?"
- "What are people saying about X lately?"
- "Summarize recent discussion/reaction to X."
- "Is there controversy/hype around X right now?"
- Any request for a "pulse check," trend summary, or cross-platform synthesis on a recent topic, product, event, or person.

Do not apply this skill for questions that have a single authoritative answer (documentation lookups, factual reference questions, code questions) — it's for questions where the answer is "what does the discourse look like," which requires triangulating multiple, possibly conflicting sources.

## Step-by-step guidance

1. **Clarify scope first.** Confirm (or reasonably assume) the topic, the time window (default to the last 30 days unless the user specifies otherwise), and whether they want a specific angle (sentiment, factual developments, controversy, market/financial signal, etc.).

2. **Search broadly across source types, not just one.** Treat each of the following as a distinct lens on the topic, and pull from as many as are reasonably accessible:
   - **Social/short-form discussion** (X/Twitter-style): captures real-time reaction, hot takes, and breaking sentiment.
   - **Community forums** (Reddit-style, Hacker News-style): captures longer-form debate, technical critique, and community consensus or disagreement.
   - **Video/long-form commentary** (YouTube-style): captures explainer and analysis content, plus top-comment sentiment.
   - **Prediction markets** (Polymarket-style): if the topic has a quantifiable future outcome, note the current implied probability as a distinct, numeric signal — separate from opinion-based sources.
   - **General web search**: news articles, blog posts, and official statements for factual grounding and dates.

3. **Weight recency.** Prioritize the most recent material within the requested window. Note explicitly if a source is stale or if you're relying on older context to fill a gap.

4. **Separate fact from opinion.** When synthesizing, distinguish:
   - Verified/reported facts (what happened, with approximate dates).
   - Aggregate sentiment or opinion (what people think about what happened), noting where sentiment is split or contested rather than flattening it into a false consensus.
   - Market-implied signals (numeric, if applicable), kept distinct from narrative opinion.

5. **Attribute and ground every claim.** Every non-trivial claim in the final summary should be traceable to a source type or specific source. If a claim can't be grounded, flag it as speculative rather than presenting it as established.

6. **Note gaps and conflicts honestly.** If sources disagree, say so and describe the disagreement rather than picking a side silently. If a platform yielded little or no relevant material, say that too rather than padding the summary.

7. **Synthesize, don't just list.** The final output should read as one coherent summary organized by theme or by source-of-signal (e.g., "what happened," "how social media is reacting," "what forums are debating," "market odds," "outstanding uncertainty") — not a raw dump of individual posts.

8. **Close with a dated freshness note.** State the approximate date range the research covers, since discourse on a topic can shift quickly and the reader should know how current the snapshot is.
