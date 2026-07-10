---
name: seo-audit-and-strategy
description: Guides Claude through auditing, diagnosing, and improving a website's search and generative-engine visibility — covering technical SEO, on-page/E-E-A-T signals, structured data, local/international SEO, and content strategy — and should be used whenever a user asks to audit, fix, or improve SEO, rankings, crawlability, schema markup, or visibility in AI answer engines.

# SEO Audit and Strategy

This skill helps Claude act as an SEO practitioner: diagnosing why a site underperforms in search and AI-answer surfaces, and producing concrete, prioritized fixes rather than generic advice.

## When to apply this skill

Use this whenever the user asks about any of the following:

- "Why isn't my site ranking / getting traffic?"
- Technical SEO audits (crawlability, indexing, site speed, Core Web Vitals, redirects, canonicalization)
- On-page optimization (titles, meta descriptions, headings, internal linking, content quality)
- Structured data / schema markup (Product, Article, FAQ, LocalBusiness, Organization, Breadcrumb, etc.)
- E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals
- GEO/AEO — Generative Engine Optimization / Answer Engine Optimization (visibility in AI-generated answers from tools like ChatGPT, Perplexity, or AI Overviews)
- Local SEO (Google Business Profile, NAP consistency, local landing pages, maps ranking factors)
- International SEO (hreflang, geotargeting, multi-region content strategy)
- E-commerce SEO (category/product page structure, faceted navigation, duplicate content from filters)
- Backlink strategy and link-quality assessment
- Semantic content clustering and topical authority (pillar pages, content silos)
- Turning raw crawl/analytics data into a written report

## Step-by-step approach

### 1. Establish scope and context first

Before diagnosing anything, determine:
- What type of site is this (e-commerce, blog/publisher, SaaS, local business, multi-region)? The right checklist differs sharply by type.
- What's the actual goal — more organic traffic, better rankings for specific keywords, more local foot traffic, or visibility in AI-generated answers?
- What data is available (analytics exports, crawl reports, search console data, competitor URLs) versus what must be inferred from the site's code/content directly?

Never run a generic "SEO checklist" against every site — tailor the audit to the site type and stated goal.

### 2. Technical SEO pass

Check for, in priority order (a technical block upstream makes everything downstream irrelevant):
- **Crawlability**: robots.txt blocking important paths, broken/missing XML sitemaps, orphaned pages with no internal links pointing to them.
- **Indexability**: unintended `noindex` tags, canonical tags pointing to the wrong URL, duplicate content across parameterized/faceted URLs.
- **Rendering**: content that depends on client-side JavaScript that a crawler might not execute (verify by checking if the content exists in the raw HTML response, not just the rendered DOM).
- **Performance**: Core Web Vitals (LCP, INP, CLS) — flag render-blocking resources, unoptimized images, and layout shift sources.
- **URL structure**: unnecessary redirect chains, inconsistent trailing slashes/protocol (http vs https, www vs non-www), broken internal links (404s).

### 3. On-page and content pass

- Title tags: unique per page, front-load the primary keyword/intent, appropriate length (roughly 50-60 characters to avoid truncation).
- Meta descriptions: compelling and unique — they don't directly affect rankings but affect click-through rate.
- Heading hierarchy: one H1 per page, logical H2/H3 nesting that mirrors the content's actual structure (not keyword-stuffed).
- Content depth and originality: does the page answer the query completely, or is it thin/duplicative of a competitor? Flag content that exists mainly to rank rather than to genuinely help the reader — this is the single biggest E-E-A-T risk.
- Internal linking: are related pages linked to and from with descriptive anchor text, forming clear topical clusters rather than an isolated page?

### 4. E-E-A-T and trust signals

- Author attribution: real named authors with visible credentials/bios for expertise-sensitive topics (health, finance, legal).
- Evidence of first-hand experience where relevant (original photos, data, testing) rather than purely aggregated/rewritten content.
- Trust signals: clear contact information, privacy/terms pages, HTTPS, and citations/sources for factual claims.
- Consistency of NAP (Name, Address, Phone) across the site and any external listings, for local businesses.

### 5. Structured data (schema markup)

Recommend the schema types that match the page's actual content — don't suggest schema that misrepresents the page (this risks manual penalties):
- `Article` / `NewsArticle` / `BlogPosting` for editorial content, including `author`, `datePublished`, `headline`.
- `Product` and `Offer` for e-commerce, including price, availability, and aggregate rating only if genuine reviews exist.
- `FAQPage` only for content that is genuinely formatted as Q&A on the page (not invisible/hidden Q&A stuffed in for rich results).
- `LocalBusiness` with accurate `address`, `geo`, and `openingHours` for local SEO.
- `BreadcrumbList` to reinforce site hierarchy.
- `Organization` on key pages to strengthen entity recognition.

Always validate that the proposed structured data reflects content actually visible on the page — schema that describes content the page doesn't have is a policy violation, not an optimization.

### 6. GEO/AEO — visibility in AI-generated answers

Generative engines favor content that is:
- Directly extractable: clear, self-contained statements that answer a specific question near the top of the page, rather than requiring the reader to piece the answer together.
- Well-attributed: content tied to a credible, named source, since AI answer engines tend to prefer citable, authoritative-sounding sources.
- Structured: use of clear headings, lists, and tables that make it easy for a model to extract a discrete fact or step.
- Not purely promotional: answer engines tend to downrank content that reads as an ad rather than as an explanation.

Recommend restructuring key pages so the direct answer to the page's core question appears within the first few sentences, followed by supporting depth.

### 7. Backlink and authority assessment

When link data is available, prioritize:
- Relevance of the linking domain's topic to the target site's topic over raw link count.
- Diversity of linking domains over volume of links from a single domain.
- Anchor text naturalness — a profile dominated by exact-match commercial anchors is a red flag, not a strength.
Flag any signs of purchased or clearly manipulative link schemes as a risk rather than a strategy to replicate.

### 8. International and local considerations

- For multi-region sites: verify `hreflang` tags are reciprocal and correctly targeted (language-region pairs), and that there isn't a single generic page trying to serve all regions.
- For local businesses: check for consistent NAP, presence of location-specific landing pages (not one generic "locations" page), and genuine local content (not just a city name swapped into a template).

### 9. Prioritize and report

Don't dump every finding with equal weight. Structure the final output as:
1. **Critical/blocking issues** — things actively preventing indexing or ranking (robots.txt blocks, noindex accidents, broken canonicals).
2. **High-impact opportunities** — content gaps, missing schema, poor title tags on high-traffic pages.
3. **Longer-term strategy** — topical clustering, backlink strategy, E-E-A-T investment.

For each finding, state: what's wrong, why it matters (in terms of the user's stated goal), and the concrete fix — not just "improve your titles" but the specific rewritten title.

## Guardrails

- Never recommend manipulative tactics: cloaking, hidden text, doorway pages, purchased link schemes, or schema markup that misrepresents page content. These risk search-engine penalties and should be flagged as risks if the user is already doing them.
- Don't assume a generic best-practices checklist applies uniformly — site type, industry, and stated goal should shape which checks matter most.
- When uncertain about current data (traffic, rankings, competitor behavior), say so explicitly rather than inventing numbers — base recommendations on what can actually be observed in the provided content/code, not assumed analytics.
