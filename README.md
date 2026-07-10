# claude-scout

A CLI that discovers Claude Code skills across GitHub, Reddit, X/Twitter, YouTube, and TikTok, drafts and tests them, and promotes the survivors into a curated local `library/`.

## Why

Skills show up faster than anyone can read or test them. This automates discovery and eval, then narrows the flood to a short "worth your time" list instead of another directory to dig through.

## Pipeline

**Harvest → Build → Eval → Committee → Council → Review → Library**

| Stage | What it does |
|---|---|
| `make harvest` | Pulls candidates into `candidates/`, deduped via `seen.txt`. GitHub works out of the box; Reddit/X/YouTube/TikTok need credentials (see Setup) or no-op. `LIMIT=N`, `GITHUB_ONLY=1`. |
| `make build` | `claude` CLI drafts a `SKILL.md` per candidate into `drafts/<name>/`, treating candidate content as untrusted. |
| `make eval` | Runs a test battery per draft via `claude`; pass/fail is exit-code/timeout only, never quality. |
| `make committee` | Five exec personas (CEO/CTO/Solution Architect/Security Lead/QA Lead) score each eval-passed draft 1–5. Below threshold → `trash/`. Hired drafts move to the council stage. |
| — council stage | Five-advisor-plus-chairman panel (mirrors `.claude/skills/llm-council`) checks a hired draft for redundancy against `library/`. Redundant → `trash/`. Novel → left in `drafts/` for review. Both stages log a verdict JSON. |
| `make review` | Interactive promote/trash for drafts left undecided (no quorum, or council-approved). |
| `make backfill` | One-off: scores `library/` entries with no `committee_score` yet. Safe to re-run. |
| `make insights` | Aggregates existing verdict JSON (`drafts/`, `trash/`, `library/`) into a report: decision funnel, per-voter averages, per-dimension averages, and whether committee's uniqueness score predicts council's call. Read-only. |
| `make digest` | Prints the top 10 `library/` entries ranked by `committee_score`. |
| `make scout` | Harvest + build + eval + committee in one shot. |

Also: `make search KEYWORD=...`, `make show NAME=...`, `make check` (lint + mypy + pylint + bandit + test). The `Makefile` is the source of truth.

## Setup

```
make install-dev
make check
make scout
```

Requires the `claude` CLI on PATH. GitHub needs no setup (`GITHUB_TOKEN` optional, raises the rate limit). Other sources no-op without credentials:

| Source | Env var(s) |
|---|---|
| Reddit | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` |
| X/Twitter | `TWITTER_BEARER_TOKEN` |
| YouTube | `YOUTUBE_API_KEY` |
| TikTok | `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` (Research API, needs approval) |

Thresholds, keywords, the committee rubric, and the council roster live in `defaults/config.yml`.

## Layout

`src/scout/` (`commands/`, `core/`, `services/`), mirrored by `tests/`. Data at repo root: `candidates/`, `drafts/`, `library/`, `trash/`, `prompts/`, `logs/`.

## Principles

90% of the value is in the loop, 10% in the code. Flat files over databases, `print()` over logging, duplication over premature abstraction, Claude Code as the only orchestrator. Eval only checks "does it run" — committee and council are the two sanctioned exceptions. Full constraints in `CLAUDE.md`.
