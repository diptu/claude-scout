---
name: research-repo-navigator
description: Guides Claude through locating, evaluating, and adapting reference implementations inside large multi-paper research monorepos (e.g. a repo that bundles hundreds of independent per-paper subdirectories); use when a user wants to find, understand, or reuse code tied to a specific research paper or technique buried in a sprawling research codebase.
---

# Research Repo Navigator

## What this skill helps with

Large research organizations often publish a single monorepo containing
hundreds of loosely related subdirectories, each corresponding to a different
paper, technique, or experiment. These repos have no single coherent
architecture — every subdirectory is effectively its own mini-project with
its own dependencies, conventions, and level of polish. Finding the right
code, understanding whether it's usable, and adapting it into a real project
requires a different approach than navigating a normal application codebase.

Apply this skill whenever a user:

- Asks to find code for a specific paper, technique, model, or algorithm
  inside a large research repository.
- Wants to know whether a research subdirectory is production-usable,
  experimental, or effectively abandoned.
- Wants to extract or adapt a specific technique from research code into
  their own project.
- Is trying to get unfamiliar, sparsely-documented research code running
  locally.

## How to approach it

### 1. Treat each subdirectory as an independent project, not a module

Do not assume shared build tooling, shared dependency versions, or shared
coding conventions across subdirectories. Before reading code inside a
candidate subdirectory:

- Look for a local `README.md` first — it usually names the paper, the
  expected way to run the code, and any caveats about its state (e.g.
  "code as-is, not maintained").
- Look for a local `requirements.txt`, `setup.py`, or `pyproject.toml`
  scoped to that subdirectory rather than assuming a repo-wide one applies.
- Check for a citation block or paper link in the README to confirm which
  publication the code actually implements — directory names are often
  abbreviated or reused loosely.

### 2. Locate the right subdirectory efficiently

With hundreds of subdirectories, don't browse sequentially:

- Search directory and file names for keywords from the paper title, author
  names, or technique name.
- Grep for the technique's distinctive terminology (a loss name, a model
  name, a dataset name) inside README files and top-level source files —
  this surfaces the right directory faster than guessing from names alone.
- If multiple subdirectories look related, prefer the one whose README
  explicitly names the paper or technique the user asked about over one
  that merely shares a keyword.

### 3. Triage usability before investing time

Research code varies wildly in quality and upkeep. Quickly assess:

- **Freshness**: does the subdirectory look actively touched, or does it
  read as a one-time snapshot released alongside a paper?
- **Runnability**: are there pinned dependency versions, a clear entry
  point script, and instructions for required data/checkpoints? Missing
  any of these is normal for research code — flag it to the user rather
  than assuming it "just works."
- **Scope**: is this a full training pipeline, or just a reference
  implementation of one algorithmic piece (e.g. a loss function or a
  model layer)? Many subdirectories are the latter — say so explicitly
  rather than treating a small reference snippet as a complete system.

### 4. Adapting code into a user's project

When pulling code out of a research subdirectory for reuse:

- Extract the minimal self-contained unit (a function, a model class, a
  loss) rather than importing the whole subdirectory's tree, since research
  code frequently has internal-only dependencies (proprietary data loaders,
  internal config systems) that won't run outside their original context.
- Rewrite any internal-only imports or config plumbing to fit the user's
  project rather than trying to vendor the original harness.
- Preserve attribution: note which paper/subdirectory the technique came
  from in a comment or in the user-facing explanation, since research code
  is usually tied to a specific publication's claims and reproducibility
  expectations.
- Flag any license file found in the subdirectory or repo root to the user
  before reuse, since research repos may mix licenses across subdirectories.

### 5. When the ask is exploratory rather than concrete

If the user is browsing rather than looking for one specific technique,
summarize what's available by grouping subdirectories by apparent research
area (e.g. vision, NLP, RL, systems) using README titles and folder names,
rather than listing every subdirectory — this keeps the response useful
instead of an undifferentiated directory dump.
