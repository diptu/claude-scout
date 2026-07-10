---
name: azure-docs-style
description: Write or revise Microsoft Azure technical documentation (how-to guides, quickstarts, tutorials, conceptual articles) that follows Microsoft Docs conventions for structure, metadata, and terminology; use when a user asks for Azure documentation, a README covering an Azure service, or wants existing Azure-related docs brought in line with Microsoft's documentation style.

---

# Azure Docs Style

Helps produce Azure-related technical documentation that reads like it belongs in Microsoft's official docs set: consistent structure, correct service terminology, and metadata that makes the content usable inside a docs pipeline (search, TOC generation, versioning). Apply this skill whenever a user asks to write, restructure, or clean up documentation about an Azure service, feature, or workflow — not when they're asking for help configuring Azure itself (that's an operations task, not a docs task).

## When to apply

- The user asks for a new doc page (quickstart, how-to, tutorial, concept, or reference) about an Azure service.
- The user pastes existing Azure-related documentation and asks for it to be cleaned up, restructured, or made consistent.
- The user asks for a README or wiki page describing how to use an Azure service, and wants it to read like professional product documentation rather than a casual note.
- Do NOT apply this for hands-on Azure CLI/Portal troubleshooting, cost estimation, or architecture design — those are engineering tasks, not documentation tasks, even if Azure is involved.

## Article types and when to use each

Pick the type that matches what the reader is trying to do, and don't blend them:

- **Quickstart** — get one specific thing running fast, minimal explanation, numbered steps, a clear "clean up resources" step at the end.
- **How-to guide** — accomplish one task an experienced user already understands the context for; task-focused, assumes prior familiarity with the service.
- **Tutorial** — walk a newcomer through a multi-step scenario end-to-end, with more explanation of *why* at each step than a how-to.
- **Conceptual article** — explain how a feature or service works, its architecture, and tradeoffs, with no step-by-step instructions.
- **Reference** — exhaustive, structured listing (CLI parameters, REST API fields, config options) with minimal prose.

## Structure to follow

1. **Title** — starts with a verb for task-based articles ("Create a...", "Configure...", "Deploy..."), or a noun phrase for conceptual/reference articles.
2. **Short intro (1–3 sentences)** — states what the reader will accomplish or learn, and why it matters, before any steps begin. No filler like "In this article, we will discuss."
3. **Prerequisites** — a bulleted list of what the reader needs before starting (subscription, CLI version, permissions, prior resources). Omit this section entirely for conceptual articles rather than leaving it empty.
4. **Body** — numbered steps for task-based articles; use `##` headings to break long procedures into logical phases (e.g., "Create the resource group," "Deploy the service," "Verify the deployment"). Each step should be independently actionable — a reader should be able to tell from the heading alone what phase they're in.
5. **Verification step** — for how-tos, quickstarts, and tutorials, include an explicit way for the reader to confirm the thing worked (a command to run, an expected output, a portal blade to check).
6. **Clean-up section** — for quickstarts and tutorials that create billable resources, include a final section on how to delete/deallocate them so the reader isn't left with a running bill.
7. **Next steps** — a short list of links or pointers to logically related content (not required to be resolvable URLs when drafting; placeholders like "link to the X how-to" are acceptable and should be flagged as such).

## Terminology and tone conventions

- Use exact, capitalized Azure product names as Microsoft does (e.g., "Azure Blob Storage," not "blob storage" or "Azure Blobs"; "Azure Kubernetes Service (AKS)," spelling it out on first use then using the acronym).
- Prefer second person ("you create a resource group") over first person plural ("we create...") or passive voice ("a resource group is created").
- Use present tense for describing behavior, imperative mood for instructions ("Select **Create**," not "You should select Create" or "Click on Create").
- Bold UI element names exactly as they appear on screen (e.g., select **Review + create**).
- Use code formatting for anything the reader types or that the system outputs literally: resource names, CLI commands, file paths, environment variable names, config keys.
- Avoid marketing language ("powerful," "seamless," "cutting-edge") — Azure docs are technical reference material, not sales copy.
- Spell out acronyms on first use per article, even common ones, since docs are indexed and read independently of each other.

## Metadata block

When the target format supports front matter (Markdown docs meant for a docs pipeline, not a plain README), include a metadata block at the top with at minimum:
- `title` — the page title, ideally under 60 characters for search-result display.
- `description` — a one-sentence summary distinct from the title, written for search snippets (under ~160 characters).
- `ms.topic` or equivalent — the article type from the list above (quickstart, how-to, tutorial, conceptual, reference), so downstream tooling can group and route it correctly.

If the target is a plain README or wiki page without a docs pipeline, skip the metadata block but still keep the title/description discipline in the opening lines.

## Step-by-step process for drafting or revising

1. Identify the article type from what the user is asking for (quickstart vs. how-to vs. tutorial vs. conceptual vs. reference) — ask if it's ambiguous, since the structure differs meaningfully.
2. Identify the specific Azure service(s) involved and confirm the exact, correctly capitalized product name(s) to use throughout.
3. Draft the intro sentence(s) stating the reader's goal, then the prerequisites list.
4. Write the body using the structural pattern for that article type, keeping each step independently actionable and using imperative mood.
5. Add a verification step and, if the article provisions billable resources, a clean-up section.
6. Review the draft against the terminology conventions above — check product name capitalization, UI element bolding, and code formatting consistency.
7. If revising existing content rather than drafting new content, preserve the original's technical facts and only change structure, terminology, and tone — flag anything that looks factually questionable rather than silently rewriting it.
