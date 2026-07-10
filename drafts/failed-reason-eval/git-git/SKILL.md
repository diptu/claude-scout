The user hasn't granted write permission for that path, and per this task I should only output the SKILL.md content directly rather than write a file. Here it is:

---
name: mailing-list-patch-workflow
description: Prepares and formats git commits as mailing-list-style patch submissions (git format-patch / git send-email conventions) for projects that accept contributions via email rather than pull requests; use when a user is contributing to a project that follows a SubmittingPatches-style process instead of GitHub PRs.
---

# Mailing-list patch workflow

Some large open-source projects (git itself being the canonical example) do not
accept contributions through GitHub pull requests at all. Instead, changes are
submitted as one or more emailed patches to a mailing list, reviewed inline via
email replies, and applied by a maintainer once accepted. GitHub mirrors of
these projects are often explicitly publish-only: any PR opened against them
gets closed or redirected, sometimes through a bridge tool (e.g.
GitGitGadget for git.git) that converts the PR into a mailing-list patch
series automatically.

Apply this skill when a user is working against a project that:
- Explicitly states its GitHub repo is a "mirror" or "publish-only"
- Points contributors to a `Documentation/SubmittingPatches`-style file, a
  mailing list address, or a PR→patch bridge tool
- Uses phrases like "send a patch," "patch series," "git send-email," or
  "reroll" in its contributing docs

## What good patches for this workflow look like

1. **One logical change per commit.** Never bundle unrelated fixes. If a
   change naturally splits into independent steps (refactor, then behavior
   change, then test), make each its own commit so reviewers can evaluate them
   individually.

2. **Commit message format matters as much as the diff**, since the commit
   message *is* the email body reviewers read:
   - Subject line: short, imperative mood, prefixed with the affected
     area/subsystem in parentheses if the project's log history uses that
     convention (check `git log --oneline` on the target file/directory first
     to confirm the local style before assuming one).
   - Body: explain *why* the change is needed and what the previous behavior
     was, not just what the diff does — a reviewer reading only the message
     should understand the motivation without opening the diff.
   - Wrap body text at ~72 columns (traditional email-friendly width), unless
     the project's own commits clearly don't bother.
   - Add a `Signed-off-by:` trailer if the project's contributing docs mention
     a Developer Certificate of Origin or `git commit -s` — check for this
     requirement before assuming it applies.

3. **Base the series on the right point.** Confirm which branch/tag upstream
   expects patches against (commonly a `next`/`master`/`main`-equivalent
   integration branch, not a stable release branch) before starting work, and
   rebase onto it before generating patches.

4. **Generate the patch series, don't paste a diff.** Guide the user to run
   `git format-patch <base>..<tip> -o <output-dir>` (add `--cover-letter` for
   a multi-patch series so there's a summary email for the whole set), rather
   than a plain `git diff`. Each output file is a properly formatted RFC-2822
   email with the commit message as the subject/body — this is what a
   maintainer expects to receive, review inline, and apply with `git am`.

5. **Rerolls stay numbered.** If a patch series is revised after review
   feedback, regenerate with `git format-patch --subject-prefix="PATCH v2"`
   (incrementing the version each round) rather than silently resending
   patches with the same subject — this is how reviewers track which round of
   feedback a given patch addresses.

6. **Don't open a PR as the actual contribution mechanism** if the project is
   publish-only — treat any PR as, at best, a way to get a bridge tool (like
   GitGitGadget) to turn it into a mailing-list submission, not as the review
   surface itself. Tell the user plainly if their target project doesn't
   accept PRs directly, so they don't wait on GitHub review that will never
   come.

## Step-by-step guidance for Claude

1. Check the target project's contributing documentation (a
   `CONTRIBUTING.md`, `Documentation/SubmittingPatches`, or similar file in
   the repo) for its actual patch-format and sign-off requirements before
   assuming any of the conventions above — projects vary in specifics even
   when they share the general mailing-list model.
2. Help the user split their work into logically separate commits with
   well-formed messages, following the guidance above.
3. Confirm the correct base branch and that the working branch is rebased
   cleanly onto it.
4. Produce the exact `git format-patch` (and `git send-email`, if the user
   wants to send directly) invocation for the user to run, including
   `--cover-letter` and `--subject-prefix` flags where relevant, rather than
   just describing the diff.
5. Never fabricate a `Signed-off-by` identity or mailing list address on the
   user's behalf — surface what's required and let the user supply their own
   identity/credentials.
