---
name: markdown-to-ebook
description: Converts a collection of Markdown (or similar plain-text) chapters into a polished EPUB, MOBI, or PDF ebook, complete with cover, table of contents, and metadata; use when a user wants to package documentation, a book manuscript, or a long-form guide into a distributable ebook file.

---

# Markdown to Ebook

## What this skill helps with

This skill guides Claude through turning a set of Markdown source files (chapters,
sections, or a single long document) into a properly structured ebook in EPUB,
MOBI, and/or PDF format — the kind of output produced by ebook-generator
projects for technical books. It covers assembling chapter order, generating a
table of contents, attaching metadata (title, author, language, cover image),
and producing the final build artifacts with a document-conversion tool such as
Pandoc (or an equivalent already available in the environment).

## When to apply this skill

Apply this skill when the user asks to:

- "turn these markdown files into an ebook / EPUB / MOBI / PDF"
- "build a book from this documentation"
- "package this guide so people can read it offline"
- "generate a downloadable version of this manual"
- assemble a multi-chapter technical document into a single distributable file

Do not apply it for simple one-off PDF exports of a single short document with
no chapter structure — that's a lighter task than a full ebook build. Do not
apply it when the user just wants a PDF made from an existing single Markdown
file (a plain document-to-PDF conversion, not a book) — a simple export
tool is a better fit than a full ebook workflow.

## Step-by-step guidance

1. **Inventory the source material.**
   - Find all Markdown (or text/HTML) files that should become chapters.
   - Determine the intended reading order — check for existing numbering
     (`01-intro.md`, `02-setup.md`, ...), a `SUMMARY.md`/`README.md` table of
     contents, or ask the user if the order is ambiguous.
   - Note any images, diagrams, or code blocks referenced by the chapters and
     confirm their paths resolve relative to the source files.

2. **Collect or confirm metadata.**
   - Title, author/organization, language, and publication date are the
     minimum needed for a valid EPUB.
   - Ask the user for a cover image if one isn't already present in the
     repository; if none is available, proceed without one rather than
     inventing placeholder art.
   - If the source has front matter (YAML headers) with title/author fields
     already, reuse those instead of asking again.

3. **Normalize the Markdown before conversion.**
   - Ensure each chapter starts with a single top-level heading (`#`) — most
     converters use these headings to build the table of contents and split
     chapters.
   - Flatten or fix heading levels that skip (e.g. `#` directly to `###`)
     since that breaks generated navigation.
   - Verify internal links between chapters use relative paths that will
     still resolve once files are concatenated or bundled.

4. **Build the table of contents.**
   - Prefer a converter's built-in TOC generation driven by heading levels
     over hand-writing one, since it stays in sync with the actual chapter
     structure.
   - If the source already has a `SUMMARY.md` or similar index file, use it
     to drive both chapter order and TOC labels.

5. **Generate each requested format.**
   - EPUB: assemble chapters in reading order, embed metadata and cover,
     and validate that the result opens cleanly in an EPUB reader (structure
     check, not a manual read-through).
   - MOBI: typically produced by converting the EPUB output, since most
     conversion tools treat MOBI as a secondary target format.
   - PDF: apply a print-oriented stylesheet if one exists in the project;
     otherwise use sane defaults (readable margins, page numbers, a title
     page) rather than an unstyled raw dump.
   - Prefer a single conversion tool capable of all three targets (such as
     Pandoc) over stitching together multiple unrelated tools, to keep
     metadata and TOC consistent across formats.

6. **Validate the output.**
   - Confirm the generated file(s) exist at the expected output path and are
     non-empty.
   - Spot-check that the TOC lists all chapters in the right order and that
     the first few pages render the title/cover as expected.
   - Report to the user which formats were produced and where they were
     written, along with any chapters that had to be skipped or fixed up
     (e.g. broken links, missing images) so they can review those manually.

7. **Keep source and output separate.**
   - Write generated ebook files to a distinct output directory (e.g.
     `dist/` or `build/`) rather than mixing them into the Markdown source
     tree, so regenerating the book is a clean, repeatable step.
