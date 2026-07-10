---
name: wiki-docs-structuring
description: Helps design, organize, and write collaborative wiki/documentation content using a Confluence/Notion-style structure (spaces, nested pages, permissions, comments) — use when a user is setting up a team wiki, migrating docs into a wiki tool like Docmost/Confluence/Notion, or needs help organizing sprawling documentation into a navigable hierarchy.

## What this skill helps with

Team wikis and documentation sites (tools like Docmost, Confluence, Notion, Outline) share a common information architecture: a top-level **space** per team or product area, a **nested page tree** within each space, inline **comments** for review discussion, and **permissions** scoped per space or page. This skill helps Claude apply that structure well — whether the user is standing up a new wiki from scratch, reorganizing an existing pile of docs, or writing individual pages that fit cleanly into a larger hierarchy.

Apply this skill when the user:
- Is setting up a new team wiki or documentation site and asks how to organize it
- Has a flat pile of docs (markdown files, Google Docs, loose notes) and wants them restructured into a coherent hierarchy
- Is migrating content into a wiki tool (Docmost, Confluence, Notion, Outline, etc.) and needs the target structure planned out first
- Asks for help writing a single doc/page and wants it to fit naturally into an existing space/page hierarchy
- Wants a review or feedback pass on documentation structure (duplicate pages, orphaned pages, unclear ownership)

## Step-by-step guidance

1. **Identify the scope first.** Ask (or infer from context) how many distinct audiences or teams the documentation serves. Each distinct audience or product area typically maps to one **space** — don't put engineering runbooks and marketing brand guidelines in the same space just because one wiki tool hosts both.

2. **Design the space list before the page tree.** List out the spaces needed (e.g., "Engineering," "Product," "People Ops") before drilling into any single space's pages. Keep the space count small — a wiki with 20 near-empty spaces is worse than one with 4 well-populated ones.

3. **Build each space's page tree 2-3 levels deep, no deeper.** A common, navigable pattern:
   - Level 1: a landing/overview page for the space (what's here, who owns it, how to contribute)
   - Level 2: major topic pages (e.g., "Onboarding," "Architecture," "Incident Response")
   - Level 3: individual detail pages nested under their topic
   
   If a page tree wants to go to level 4+, that's usually a sign the level-2 topic needs to be split into two, not that nesting should go deeper — deep nesting makes pages hard to find via browsing.

4. **Give every page a single clear owner and a single clear purpose.** Before writing a page, state in one sentence what question it answers. If a page tries to answer multiple unrelated questions, split it. If a page's answer already lives on another page, link instead of duplicating — duplicated content silently drifts out of sync as one copy gets updated and the other doesn't.

5. **Write pages to be found, not just read.** Use a descriptive, search-friendly title (not "Notes" or "Misc"), and open with a one- or two-sentence summary of what the page covers before diving into detail — this lets someone scanning search results or a page tree confirm relevance without opening the full page.

6. **Use comments for discussion, not for content.** If feedback in a comment thread changes the actual guidance, fold that resolution into the page body and note it was updated; don't leave the real answer buried in a comment thread that new readers won't see.

7. **Set permissions at the space level by default, page level only as an exception.** Recommend page-level permission overrides only for genuinely sensitive individual pages (e.g., a compensation doc inside an otherwise-open People Ops space) — space-level permissions are far easier to reason about and audit than a patchwork of per-page rules.

8. **When restructuring existing docs**, do it in two passes: first inventory everything (list every existing doc/page and one-line description of what it covers), then propose the new space/page tree and show which old doc maps to which new location — including explicit call-outs for anything that's now a duplicate and can be merged or deleted, and anything that's orphaned (no clear owner or home) and needs a decision from the user before being placed.

9. **Flag structural problems proactively**, even if not asked: pages with no incoming links (orphaned), two pages that appear to answer the same question (duplicates), or a space with no landing page (no entry point). These are the failure modes that make wikis rot into unusable archives over time.
