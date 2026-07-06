# Eval test prompts

A fixed battery of smoke-test prompts run against each draft skill. Each
double-quoted string below is sent to `claude -p` together with the draft's
SKILL.md content; the eval gate only checks that the CLI exits cleanly
(does it explode), never whether the answers are good (see TODO.md
principle 6 — quality judgment stays with manual review).

CAUTION: every double-quoted string in this file becomes a test prompt
(eval.py extracts them by regex), so only the prompts themselves may use
double quotes.

1. "Read the following SKILL.md and summarize in one sentence what the skill does and when it should be used."
2. "List the concrete steps this skill instructs Claude to follow, as a numbered list."
3. "Name one task where applying this skill would be a mistake, and explain why in one sentence."
